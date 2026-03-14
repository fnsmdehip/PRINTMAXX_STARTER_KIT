#!/usr/bin/env python3
"""
OBSERVER AGENT — Inbound Lead Intelligence (Swan AI GTM T015)
==============================================================

Monitors Twitter/X and LinkedIn for inbound lead signals. Scores
engagement by lead type and routes high-value leads for follow-up.

Scoring:
  Agency founder:   10
  Agency employee:   7
  Consultant:        5
  Other:             2

Score > 7 -> write to LEDGER/INBOUND_LEADS.csv
Score > 9 -> write HIGH_VALUE alert to OPS/PENDING_HUMAN_APPROVAL.jsonl

Since we don't have direct API access yet, the agent scans existing
scraper output and logs what it would do when APIs are connected.

Runs every 2h via cron.

Usage:
    python3 observer_agent.py --scan          # Run engagement scan
    python3 observer_agent.py --status        # Show monitoring stats
    python3 observer_agent.py --leads         # Display current leads
    python3 observer_agent.py --dry-run       # Preview without writing
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# ── Sibling imports ───────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import PROJECT, safe_path, load_json, log, ts

try:
    from intelligence_router import get_intelligence
    _ROUTER_AVAILABLE = True
except ImportError:
    _ROUTER_AVAILABLE = False

try:
    from master_ops_bridge import MasterOpsBridge
    _BRIDGE_AVAILABLE = True
except ImportError:
    _BRIDGE_AVAILABLE = False

# ── Paths ─────────────────────────────────────────────────────────────
AUTOMATIONS = PROJECT / "AUTOMATIONS"
SCRAPER_OUTPUT = AUTOMATIONS / "twitter_scraper_output"
INBOUND_LEADS = PROJECT / "LEDGER" / "INBOUND_LEADS.csv"
PENDING_APPROVAL = PROJECT / "OPS" / "PENDING_HUMAN_APPROVAL.jsonl"
STATE_FILE = AUTOMATIONS / "agent" / "observer_state.json"

# ── Keyword Signals ──────────────────────────────────────────────────
KEYWORD_SIGNALS = [
    "AI automation",
    "agent system",
    "Claude Code solopreneur",
    "autonomous agent",
    "agent swarm",
    "solopreneur automation",
    "AI business OS",
    "claude max",
    "autonomous business",
    "33 agents",
    "implementation gap",
    "execution system",
    "build in public AI",
    "AI cold email",
    "AI scraping pipeline",
    "printmaxx",
    "PRINTMAXXER",
    "@PRINTMAXXER",
]

# Lead type patterns (bio/profile keywords -> classification)
LEAD_TYPE_PATTERNS = {
    "agency_founder": {
        "score": 10,
        "keywords": [
            "founder", "CEO", "agency owner", "co-founder",
            "started my agency", "running an agency", "built an agency",
            "digital agency", "marketing agency", "dev agency",
        ],
    },
    "agency_employee": {
        "score": 7,
        "keywords": [
            "work at", "team lead", "account manager", "strategist at",
            "developer at", "designer at", "growth at", "head of",
        ],
    },
    "consultant": {
        "score": 5,
        "keywords": [
            "consultant", "freelancer", "advisor", "coach",
            "helping", "I help", "consulting", "fractional",
        ],
    },
    "other": {
        "score": 2,
        "keywords": [],  # fallback
    },
}

INBOUND_LEADS_HEADER = [
    "timestamp", "username", "platform", "engagement_type",
    "source_post", "score", "lead_type", "status", "direction",
]


# ── Lead Scoring ─────────────────────────────────────────────────────

def classify_lead(bio: str, content: str) -> tuple[str, int]:
    """Classify a lead based on bio/content keywords. Returns (type, score)."""
    combined = (bio + " " + content).lower()

    for lead_type, config in LEAD_TYPE_PATTERNS.items():
        if lead_type == "other":
            continue
        for kw in config["keywords"]:
            if kw.lower() in combined:
                return lead_type, config["score"]

    return "other", LEAD_TYPE_PATTERNS["other"]["score"]


def has_keyword_signal(text: str) -> Optional[str]:
    """Check if text contains any of our monitored keyword signals.
    Returns the matched keyword or None."""
    text_lower = text.lower()
    for kw in KEYWORD_SIGNALS:
        if kw.lower() in text_lower:
            return kw
    return None


# ── CSV Helpers ──────────────────────────────────────────────────────

def ensure_leads_csv() -> None:
    """Create INBOUND_LEADS.csv with header if it doesn't exist."""
    if not INBOUND_LEADS.exists():
        INBOUND_LEADS.parent.mkdir(parents=True, exist_ok=True)
        with open(INBOUND_LEADS, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(INBOUND_LEADS_HEADER)
        log(f"Created {INBOUND_LEADS.name}", tag="OBSERVER")


def load_existing_leads() -> list[dict[str, str]]:
    """Load existing leads to avoid duplicates."""
    leads = []
    if INBOUND_LEADS.exists():
        try:
            with open(INBOUND_LEADS, newline="", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    leads.append(row)
        except Exception:
            pass
    return leads


def write_lead(lead: dict[str, Any]) -> None:
    """Append a lead row to INBOUND_LEADS.csv."""
    ensure_leads_csv()
    safe_path(INBOUND_LEADS)
    with open(INBOUND_LEADS, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            lead.get("timestamp", datetime.now().isoformat()),
            lead.get("username", ""),
            lead.get("platform", "twitter"),
            lead.get("engagement_type", ""),
            lead.get("source_post", "")[:200],
            lead.get("score", 0),
            lead.get("lead_type", "other"),
            lead.get("status", "NEW"),
            lead.get("direction", "INBOUND"),
        ])


def write_high_value_alert(lead: dict[str, Any]) -> None:
    """Write HIGH_VALUE lead alert to PENDING_HUMAN_APPROVAL.jsonl."""
    safe_path(PENDING_APPROVAL)
    PENDING_APPROVAL.parent.mkdir(parents=True, exist_ok=True)
    alert = {
        "timestamp": datetime.now().isoformat(),
        "type": "HIGH_VALUE_LEAD",
        "agent": "observer_agent",
        "username": lead.get("username", ""),
        "platform": lead.get("platform", "twitter"),
        "score": lead.get("score", 0),
        "lead_type": lead.get("lead_type", ""),
        "engagement_type": lead.get("engagement_type", ""),
        "source_post": lead.get("source_post", "")[:200],
        "action_needed": "Review and respond to high-value inbound lead",
        "status": "PENDING",
    }
    with open(PENDING_APPROVAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(alert) + "\n")


# ── Scanning ─────────────────────────────────────────────────────────

def scan_scraper_output() -> list[dict[str, Any]]:
    """Scan twitter_scraper_output/ for engagement signals in scraped data."""
    signals: list[dict[str, Any]] = []

    if not SCRAPER_OUTPUT.exists():
        log("Scraper output directory not found, skipping file scan", tag="OBSERVER")
        return signals

    # Scan JSON files from twitter scraper
    json_files = sorted(SCRAPER_OUTPUT.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
    csv_files = sorted(SCRAPER_OUTPUT.glob("*.csv"), key=lambda f: f.stat().st_mtime, reverse=True)

    # Process JSON scraper output
    for jf in json_files[:20]:  # last 20 files
        try:
            data = load_json(jf, [])
            if isinstance(data, dict):
                data = data.get("tweets", data.get("results", data.get("data", [])))
            if not isinstance(data, list):
                continue

            for item in data:
                if not isinstance(item, dict):
                    continue

                text = item.get("text", item.get("content", item.get("full_text", "")))
                username = item.get("username", item.get("user", item.get("author", "")))
                if isinstance(username, dict):
                    username = username.get("screen_name", username.get("username", ""))

                bio = item.get("bio", item.get("description", item.get("user_bio", "")))
                if isinstance(bio, dict):
                    bio = str(bio)

                if not text:
                    continue

                # Check for keyword signals
                matched_kw = has_keyword_signal(text)
                if matched_kw:
                    # Check if this is a reply/mention of us
                    is_reply_to_us = "@printmaxxer" in text.lower()
                    engagement_type = "reply" if is_reply_to_us else "keyword_mention"

                    lead_type, score = classify_lead(str(bio), text)

                    # Boost score for direct replies
                    if is_reply_to_us:
                        score = min(10, score + 2)

                    signals.append({
                        "username": str(username),
                        "platform": "twitter",
                        "engagement_type": engagement_type,
                        "source_post": text[:200],
                        "score": score,
                        "lead_type": lead_type,
                        "matched_keyword": matched_kw,
                        "source_file": jf.name,
                    })
        except Exception as e:
            log(f"Error processing {jf.name}: {e}", level="WARN", tag="OBSERVER")

    # Process CSV scraper output
    for cf in csv_files[:10]:
        try:
            with open(cf, newline="", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    text = row.get("text", row.get("content", row.get("tweet", "")))
                    username = row.get("username", row.get("user", row.get("author", "")))
                    bio = row.get("bio", row.get("description", ""))

                    if not text:
                        continue

                    matched_kw = has_keyword_signal(text)
                    if matched_kw:
                        is_reply_to_us = "@printmaxxer" in text.lower()
                        engagement_type = "reply" if is_reply_to_us else "keyword_mention"
                        lead_type, score = classify_lead(str(bio), text)

                        if is_reply_to_us:
                            score = min(10, score + 2)

                        signals.append({
                            "username": str(username),
                            "platform": "twitter",
                            "engagement_type": engagement_type,
                            "source_post": text[:200],
                            "score": score,
                            "lead_type": lead_type,
                            "matched_keyword": matched_kw,
                            "source_file": cf.name,
                        })
        except Exception as e:
            log(f"Error processing {cf.name}: {e}", level="WARN", tag="OBSERVER")

    return signals


def deduplicate_signals(
    signals: list[dict[str, Any]],
    existing_leads: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Remove signals that are already in leads CSV."""
    existing_keys = set()
    for lead in existing_leads:
        key = f"{lead.get('username', '')}|{lead.get('source_post', '')[:80]}"
        existing_keys.add(key)

    unique = []
    seen = set()
    for sig in signals:
        key = f"{sig.get('username', '')}|{sig.get('source_post', '')[:80]}"
        if key not in existing_keys and key not in seen:
            unique.append(sig)
            seen.add(key)

    return unique


# ── State Management ─────────────────────────────────────────────────

def load_state() -> dict[str, Any]:
    state = load_json(STATE_FILE, {})
    if not state:
        state = {
            "total_scans": 0,
            "total_leads_found": 0,
            "total_high_value": 0,
            "last_scan": None,
            "signals_by_keyword": {},
        }
    return state


def save_state(state: dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    safe_path(STATE_FILE)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# ── CLI Commands ─────────────────────────────────────────────────────

def cmd_scan(dry_run: bool = False) -> None:
    """Run engagement scan across available data sources."""
    log("Starting inbound engagement scan", tag="OBSERVER")

    # Check for MCP/API tools
    mcp_available = False  # placeholder until MCP tools are connected
    if mcp_available:
        log("MCP tools available, scanning live APIs", tag="OBSERVER")
        # TODO: Use MCP tools for live Twitter/LinkedIn scanning
    else:
        log("No MCP/API access. Scanning scraper output files.", tag="OBSERVER")

    # Scan existing scraper data
    signals = scan_scraper_output()
    log(f"Found {len(signals)} raw engagement signals", tag="OBSERVER")

    # Deduplicate against existing leads
    ensure_leads_csv()
    existing = load_existing_leads()
    unique_signals = deduplicate_signals(signals, existing)
    log(f"After dedup: {len(unique_signals)} new signals", tag="OBSERVER")

    if not unique_signals:
        log("No new engagement signals found", tag="OBSERVER")
        print("No new inbound signals detected.")

        # Log what we WOULD do with API access
        print("\nWith API access, observer would monitor:")
        print("  - Replies to @PRINTMAXXER posts")
        print(f"  - Mentions of: {', '.join(KEYWORD_SIGNALS[:5])} (+ {len(KEYWORD_SIGNALS) - 5} more)")
        print("  - Engagement from agency accounts")
        print("  - DMs containing keyword signals")

        state = load_state()
        state["total_scans"] = state.get("total_scans", 0) + 1
        state["last_scan"] = datetime.now().isoformat()
        save_state(state)
        return

    # Process signals
    leads_added = 0
    high_value_count = 0
    state = load_state()

    for sig in unique_signals:
        score = sig["score"]

        if score > 7:
            sig["status"] = "NEW"
            sig["direction"] = "INBOUND"
            sig["timestamp"] = datetime.now().isoformat()

            if dry_run:
                print(f"  [DRY RUN] Would add lead: @{sig['username']} "
                      f"(score={score}, type={sig['lead_type']}, "
                      f"keyword={sig.get('matched_keyword', '')})")
            else:
                write_lead(sig)
                leads_added += 1

            if score > 9:
                if dry_run:
                    print(f"  [DRY RUN] Would write HIGH_VALUE alert for @{sig['username']}")
                else:
                    write_high_value_alert(sig)
                    high_value_count += 1
                    log(f"HIGH VALUE LEAD: @{sig['username']} (score={score})",
                        level="ALERT", tag="OBSERVER")
        else:
            if dry_run:
                print(f"  [DRY RUN] Score {score} <= 7, skipping @{sig['username']}")

        # Track keyword frequency
        kw = sig.get("matched_keyword", "other")
        kw_counts = state.get("signals_by_keyword", {})
        kw_counts[kw] = kw_counts.get(kw, 0) + 1
        state["signals_by_keyword"] = kw_counts

    # Update state
    state["total_scans"] = state.get("total_scans", 0) + 1
    state["total_leads_found"] = state.get("total_leads_found", 0) + leads_added
    state["total_high_value"] = state.get("total_high_value", 0) + high_value_count
    state["last_scan"] = datetime.now().isoformat()
    save_state(state)

    action = "Would add" if dry_run else "Added"
    print(f"\nScan complete:")
    print(f"  Raw signals:     {len(signals)}")
    print(f"  New (deduped):   {len(unique_signals)}")
    print(f"  {action}:   {leads_added} leads (score > 7)")
    print(f"  High-value:      {high_value_count} (score > 9)")


def cmd_status() -> None:
    """Show monitoring stats."""
    state = load_state()
    print("OBSERVER AGENT STATUS")
    print("=" * 50)
    print(f"  Total scans:        {state.get('total_scans', 0)}")
    print(f"  Total leads found:  {state.get('total_leads_found', 0)}")
    print(f"  High-value alerts:  {state.get('total_high_value', 0)}")
    print(f"  Last scan:          {state.get('last_scan', 'never')}")

    # Keyword signal distribution
    kw_counts = state.get("signals_by_keyword", {})
    if kw_counts:
        print(f"\n  Keyword Signal Distribution:")
        for kw, count in sorted(kw_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"    {kw}: {count}")

    # Current leads summary
    existing = load_existing_leads()
    if existing:
        new_count = sum(1 for l in existing if l.get("status", "").upper() == "NEW")
        total = len(existing)
        inbound = sum(1 for l in existing if l.get("direction", "").upper() == "INBOUND")
        outbound = sum(1 for l in existing if l.get("direction", "").upper() == "OUTBOUND")
        print(f"\n  Leads Summary:")
        print(f"    Total:    {total}")
        print(f"    NEW:      {new_count}")
        print(f"    INBOUND:  {inbound}")
        print(f"    OUTBOUND: {outbound}")
    else:
        print(f"\n  No leads tracked yet.")

    # Data source availability
    print(f"\n  Data Sources:")
    print(f"    Scraper output dir:   {'EXISTS' if SCRAPER_OUTPUT.exists() else 'NOT FOUND'}")
    if SCRAPER_OUTPUT.exists():
        json_count = len(list(SCRAPER_OUTPUT.glob("*.json")))
        csv_count = len(list(SCRAPER_OUTPUT.glob("*.csv")))
        print(f"    JSON files:           {json_count}")
        print(f"    CSV files:            {csv_count}")
    print(f"    Intelligence router:  {'AVAILABLE' if _ROUTER_AVAILABLE else 'NOT AVAILABLE'}")
    print(f"    MCP tools:            NOT CONNECTED (scanning scraper output instead)")


def cmd_leads() -> None:
    """Display current leads."""
    existing = load_existing_leads()
    if not existing:
        print("No leads tracked yet.")
        print(f"Run --scan to find inbound engagement signals.")
        return

    print(f"INBOUND LEADS ({len(existing)} total)")
    print("=" * 80)
    print(f"{'Username':<20} {'Platform':<10} {'Type':<18} {'Score':<6} {'Status':<10} {'Direction':<10}")
    print("-" * 80)

    for lead in existing[-25:]:  # last 25
        username = lead.get("username", "?")[:18]
        platform = lead.get("platform", "?")[:8]
        lead_type = lead.get("lead_type", "?")[:16]
        score = lead.get("score", "?")
        status = lead.get("status", "?")[:8]
        direction = lead.get("direction", "?")[:8]
        print(f"  {username:<18} {platform:<10} {lead_type:<18} {score:<6} {status:<10} {direction:<10}")

    if len(existing) > 25:
        print(f"\n  ... showing last 25 of {len(existing)} leads")

    # Score distribution
    scores = []
    for l in existing:
        try:
            scores.append(int(l.get("score", 0)))
        except (ValueError, TypeError):
            pass
    if scores:
        print(f"\n  Score distribution:")
        print(f"    High (>9):  {sum(1 for s in scores if s > 9)}")
        print(f"    Medium (7-9): {sum(1 for s in scores if 7 <= s <= 9)}")
        print(f"    Low (<7):   {sum(1 for s in scores if s < 7)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Observer Agent -- Inbound lead intelligence monitor"
    )
    parser.add_argument("--scan", action="store_true",
                        help="Run engagement scan")
    parser.add_argument("--status", action="store_true",
                        help="Show monitoring stats")
    parser.add_argument("--leads", action="store_true",
                        help="Display current leads")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without writing")
    args = parser.parse_args()

    if args.scan:
        cmd_scan(dry_run=args.dry_run)
    elif args.leads:
        cmd_leads()
    elif args.status:
        cmd_status()
    else:
        cmd_status()


if __name__ == "__main__":
    main()
