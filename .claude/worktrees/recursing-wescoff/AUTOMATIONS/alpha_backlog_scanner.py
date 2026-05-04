#!/usr/bin/env python3
"""
ALPHA BACKLOG SCANNER — Sweep ALL historical alpha for unintegrated opportunities.

The pipeline catches NEW alpha daily but never goes back to mine the backlog.
This script scans all 15K+ alpha entries for methods that:
  - Describe tools/scanners/APIs we could build automations for
  - Mention revenue methods not yet wired into ventures
  - Suggest system improvements (security tools, monitoring, optimization)
  - Reference external services we could integrate via MCP/n8n
  - Match existing ventures that could be bolstered

Produces re-staged alpha entries with source=alpha_backlog_scanner so
auto_approve + autonomous_integrator V2 pick them up automatically.

Cron: 0 3 * * 1 (Monday 3 AM weekly — full backlog sweep)

Usage:
  python3 AUTOMATIONS/alpha_backlog_scanner.py --scan
  python3 AUTOMATIONS/alpha_backlog_scanner.py --scan --category tools
  python3 AUTOMATIONS/alpha_backlog_scanner.py --status
  python3 AUTOMATIONS/alpha_backlog_scanner.py --dry-run
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

csv.field_size_limit(10 * 1024 * 1024)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AUTOMATIONS = PROJECT / "AUTOMATIONS"
LEDGER = PROJECT / "LEDGER"
OPS = PROJECT / "OPS"
LOG_FILE = AUTOMATIONS / "logs" / "alpha_backlog_scanner.log"
ALPHA_STAGING = LEDGER / "ALPHA_STAGING.csv"
BACKLOG_REPORT = OPS / "ALPHA_BACKLOG_REPORT.md"
BACKLOG_STATE = AUTOMATIONS / "agent" / "alpha_backlog_state.json"
INTEGRATION_LOG = LEDGER / "integration_runs.jsonl"

ALPHA_FIELDS = [
    "alpha_id", "source", "source_url", "category", "tactic",
    "roi_potential", "priority", "status", "applicable_methods",
    "applicable_niches", "synergy_score", "cross_sell_products",
    "implementation_priority", "engagement_authenticity",
    "earnings_verified", "extracted_method", "compliance_notes",
    "reviewer_notes", "created_at", "ops_generated",
]

# Pattern categories — what we're hunting for in the backlog
OPPORTUNITY_PATTERNS = {
    "tool_scanner": {
        "description": "Tools, APIs, scanners, monitors that could become automations",
        "keywords": [
            r"(?:scan|scrape|monitor|track|crawl|watch)\w*\s+(?:for|the|daily|weekly)",
            r"(?:api|endpoint|webhook|rss|feed)\s+(?:for|to|that)",
            r"(?:crunchbase|edgar|sec\s+filing|8-k|10-k|s-1)",
            r"(?:google\s+alerts?|social\s+listening|brand\s+monitor)",
            r"(?:price\s+tracker|stock\s+screener|market\s+scanner)",
            r"(?:github|npm|pypi|product\s+hunt)\s+(?:trend|new|alert)",
            r"(?:whois|domain|dns)\s+(?:monitor|check|scan)",
            r"(?:uptime|health|status)\s+(?:monitor|check|ping)",
        ],
        "venture_boost": ["RESEARCH", "SCRAPING", "APP"],
        "priority": "P0",
    },
    "revenue_method": {
        "description": "Revenue methods not yet wired into ventures",
        "keywords": [
            r"(?:make|earn|generate)\s+\$?\d+",
            r"(?:monetize|revenue|income|profit)\s+(?:from|with|using)",
            r"(?:affiliate|dropship|print.on.demand|digital\s+product)",
            r"(?:saas|subscription|recurring\s+revenue|mrr)",
            r"(?:freelance|consulting|agency|service)",
            r"(?:arbitrage|flip|resell|wholesale)",
            r"(?:course|ebook|template|toolkit)\s+(?:sell|launch|create)",
            r"(?:newsletter|paid\s+community|membership)",
        ],
        "venture_boost": ["MONETIZE", "PRODUCT", "CONTENT", "OUTBOUND"],
        "priority": "P0",
    },
    "system_improvement": {
        "description": "Security tools, performance optimization, system hardening",
        "keywords": [
            r"(?:security|vulnerability|audit|pentest|hardening)",
            r"(?:optimize|performance|speed|cache|compress)",
            r"(?:backup|disaster\s+recovery|failover|redundancy)",
            r"(?:logging|monitoring|alerting|observability)",
            r"(?:rate\s+limit|throttle|queue|batch)",
            r"(?:docker|container|kubernetes|deploy)",
            r"(?:ci.cd|pipeline|github\s+actions|workflow)",
            r"(?:test|coverage|lint|type.check)",
        ],
        "venture_boost": ["APP", "RESEARCH"],
        "priority": "P1",
    },
    "integration_opportunity": {
        "description": "External services, APIs, platforms we could wire in via MCP/n8n",
        "keywords": [
            r"(?:zapier|make\.com|n8n|ifttt|integromat)\s+(?:alternative|workflow)",
            r"(?:stripe|gumroad|lemonsqueezy|paddle)\s+(?:api|webhook|integration)",
            r"(?:slack|discord|telegram|whatsapp)\s+(?:bot|automation|integration)",
            r"(?:notion|airtable|coda|spreadsheet)\s+(?:api|automation)",
            r"(?:openai|anthropic|claude|gpt|gemini)\s+(?:api|tool|agent)",
            r"(?:pinecone|weaviate|chroma|vector)\s+(?:db|search|index)",
            r"(?:supabase|firebase|postgres|mongo)\s+(?:api|function|trigger)",
            r"(?:cloudflare|vercel|netlify|railway)\s+(?:worker|function|edge)",
        ],
        "venture_boost": ["APP", "PRODUCT", "EAS"],
        "priority": "P1",
    },
    "growth_tactic": {
        "description": "Growth/marketing tactics applicable to existing ventures",
        "keywords": [
            r"(?:growth\s+hack|viral|referral\s+program|word.of.mouth)",
            r"(?:seo|backlink|guest\s+post|content\s+marketing)",
            r"(?:cold\s+email|outreach|lead\s+gen|prospecting)",
            r"(?:tiktok|instagram|youtube|twitter|linkedin)\s+(?:growth|strategy|hack)",
            r"(?:community|forum|reddit|quora)\s+(?:marketing|growth|engagement)",
            r"(?:launch|product\s+hunt|hacker\s+news|indie\s+hacker)",
            r"(?:conversion|funnel|landing\s+page|a.b\s+test)",
        ],
        "venture_boost": ["CONTENT", "OUTBOUND", "LOCAL_BIZ"],
        "priority": "P1",
    },
}


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [BACKLOG] [{level}] {msg}"
    print(line)
    safe_path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_FILE), "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# Backlog scanning
# ---------------------------------------------------------------------------

def load_all_alpha() -> list[dict]:
    """Load ALL alpha entries regardless of status."""
    if not ALPHA_STAGING.exists():
        return []
    entries = []
    try:
        with open(ALPHA_STAGING) as f:
            for row in csv.DictReader(f):
                entries.append(row)
    except Exception as e:
        log(f"Error loading alpha: {e}", "ERROR")
    return entries


def get_already_integrated_ids() -> set[str]:
    """Get IDs of entries already processed by the integrator."""
    ids: set[str] = set()
    if INTEGRATION_LOG.exists():
        try:
            for line in INTEGRATION_LOG.read_text().strip().splitlines():
                rec = json.loads(line)
                for method in rec.get("methods", []):
                    ids.add(method)
        except Exception:
            pass
    return ids


def get_already_scanned_ids() -> set[str]:
    """Load IDs already scanned in previous backlog runs."""
    if not BACKLOG_STATE.exists():
        return set()
    try:
        state = json.loads(safe_path(BACKLOG_STATE).read_text())
        return set(state.get("scanned_ids", []))
    except Exception:
        return set()


# Engagement bait red flags — entries matching these are likely surface-level noise
BAIT_RED_FLAGS = [
    r"(?:6|7)\s+figures?\s+(?:in|within)\s+\d+\s+(?:days?|weeks?|months?)",
    r"quit\s+(?:my|your|his|her)\s+(?:9.to.5|job|corporate)",
    r"(?:passive\s+income|make\s+money)\s+(?:while\s+you\s+sleep|on\s+autopilot)",
    r"(?:nobody|no\s+one)\s+(?:is\s+talking|talks)\s+about",
    r"(?:i|he|she)\s+made\s+\$\d+k?\s+(?:in|my|last)\s+(?:first|one)\s+(?:month|week|day)",
    r"this\s+(?:one\s+)?(?:trick|hack|secret)\s+(?:changed|will\s+change)",
    r"stop\s+(?:trading|exchanging)\s+(?:time|hours)\s+for\s+(?:money|dollars)",
    r"here.s?\s+(?:the|a)\s+(?:blueprint|roadmap|playbook)\s+(?:to|for)\s+\$",
    r"most\s+people\s+(?:don.t|won.t|will\s+never)\s+(?:know|understand|realize)",
    r"(?:copy|steal)\s+(?:this|my)\s+(?:exact|proven)\s+(?:system|method|strategy|funnel)",
]

# Specificity signals — entries matching these likely have REAL substance
SPECIFICITY_SIGNALS = [
    r"(?:api|endpoint|sdk|library|framework|cli)\b",
    r"(?:python|javascript|typescript|golang|rust|sql)\b",
    r"(?:step\s+\d|phase\s+\d|part\s+\d)",
    r"(?:pricing|plan|tier|free\s+tier|rate\s+limit)",
    r"(?:github\.com|npmjs\.com|pypi\.org|docs\.)",
    r"(?:curl|wget|pip\s+install|npm\s+install|brew\s+install)",
    r"(?:localhost|port\s+\d|https?://)",
    r"(?:cron|scheduled?|recurring|batch)\b",
]


def _is_likely_bait(text: str) -> bool:
    """Check if text matches engagement bait patterns."""
    bait_hits = sum(1 for p in BAIT_RED_FLAGS if re.search(p, text, re.IGNORECASE))
    spec_hits = sum(1 for p in SPECIFICITY_SIGNALS if re.search(p, text, re.IGNORECASE))
    # High bait signals AND low specificity = likely bait
    return bait_hits >= 2 and spec_hits == 0


def scan_entry(entry: dict) -> list[dict]:
    """Scan a single alpha entry against all opportunity patterns.
    Filters out engagement bait that sounds good but lacks substance.
    Returns list of matched opportunities.
    """
    text = (
        (entry.get("extracted_method") or "") + " " +
        (entry.get("tactic") or "") + " " +
        (entry.get("content") or "")
    ).lower()

    if len(text.strip()) < 20:
        return []

    # Skip entries already marked as engagement bait (unless they have specificity)
    status = (entry.get("status") or "").upper()
    if status == "ENGAGEMENT_BAIT" and not any(
        re.search(p, text, re.IGNORECASE) for p in SPECIFICITY_SIGNALS
    ):
        return []

    # Filter out likely bait
    if _is_likely_bait(text):
        return []

    matches = []
    for cat_name, config in OPPORTUNITY_PATTERNS.items():
        for pattern in config["keywords"]:
            if re.search(pattern, text, re.IGNORECASE):
                matches.append({
                    "category": cat_name,
                    "description": config["description"],
                    "pattern_matched": pattern,
                    "venture_boost": config["venture_boost"],
                    "priority": config["priority"],
                    "original_text": text[:300],
                    "original_id": entry.get("alpha_id", ""),
                    "original_source": entry.get("source", ""),
                    "original_status": entry.get("status", ""),
                })
                break  # One match per category is enough

    return matches


def run_scan(category_filter: str = "", dry_run: bool = False) -> dict:
    """Sweep ALL historical alpha for unintegrated opportunities."""
    log("Starting alpha backlog scan...")

    all_entries = load_all_alpha()
    log(f"Loaded {len(all_entries)} total alpha entries")

    already_scanned = get_already_scanned_ids()
    log(f"Already scanned in previous runs: {len(already_scanned)}")

    # Filter to entries not yet scanned by backlog
    entries_to_scan = [
        e for e in all_entries
        if e.get("alpha_id", "") not in already_scanned
    ]
    log(f"Entries to scan this run: {len(entries_to_scan)}")

    # Scan each entry
    all_matches: list[dict] = []
    scanned_ids: list[str] = list(already_scanned)

    for entry in entries_to_scan:
        entry_id = entry.get("alpha_id", "")
        matches = scan_entry(entry)

        if category_filter:
            matches = [m for m in matches if m["category"] == category_filter]

        all_matches.extend(matches)
        if entry_id:
            scanned_ids.append(entry_id)

    log(f"Found {len(all_matches)} opportunity matches across {len(entries_to_scan)} entries")

    # Group by category
    by_category: dict[str, list[dict]] = {}
    for match in all_matches:
        cat = match["category"]
        by_category.setdefault(cat, []).append(match)

    for cat, matches in by_category.items():
        log(f"  {cat}: {len(matches)} matches")

    # Stage top opportunities as new alpha entries for integration
    staged = _stage_matches(all_matches, dry_run=dry_run)

    # Save scan state
    if not dry_run:
        safe_path(BACKLOG_STATE).parent.mkdir(parents=True, exist_ok=True)
        state = {
            "last_scan": datetime.now().isoformat(),
            "total_scanned": len(scanned_ids),
            "matches_found": len(all_matches),
            "staged": staged,
            "scanned_ids": scanned_ids[-20000:],  # Keep last 20K to avoid unbounded growth
        }
        safe_path(BACKLOG_STATE).write_text(json.dumps(state, indent=2))

    # Write report
    if not dry_run:
        _write_report(all_matches, by_category, staged)

    summary = {
        "total_alpha": len(all_entries),
        "scanned": len(entries_to_scan),
        "matches": len(all_matches),
        "staged": staged,
        "by_category": {k: len(v) for k, v in by_category.items()},
    }

    log(f"Backlog scan complete: {len(all_matches)} matches, {staged} staged for integration")

    if staged > 0:
        capture_skill_from_result(
            task="alpha backlog scan for unintegrated opportunities",
            result=f"Scanned {len(entries_to_scan)} entries, found {len(all_matches)} matches, "
                   f"staged {staged} for integration",
            success=True,
        )

    return summary


def _stage_matches(matches: list[dict], dry_run: bool = False) -> int:
    """Stage matched opportunities as new alpha entries."""
    if not matches:
        return 0

    # Deduplicate by original_id + category
    seen: set[str] = set()
    unique = []
    for m in matches:
        key = f"{m['original_id']}_{m['category']}"
        if key not in seen:
            seen.add(key)
            unique.append(m)

    # Sort by priority (P0 first)
    unique.sort(key=lambda x: x.get("priority", "P2"))

    # Cap at 100 per run
    unique = unique[:100]

    existing_ids = set()
    if ALPHA_STAGING.exists():
        try:
            with open(ALPHA_STAGING) as f:
                for row in csv.DictReader(f):
                    existing_ids.add(row.get("alpha_id", ""))
        except Exception:
            pass

    new_entries = []
    for m in unique:
        key_str = m.get("original_id", "") + "_" + m.get("category", "")
        alpha_id = f"BL{hashlib.md5(key_str.encode()).hexdigest()[:8].upper()}"
        if alpha_id in existing_ids:
            continue

        entry = {
            "alpha_id": alpha_id,
            "source": "alpha_backlog_scanner",
            "source_url": f"backlog:{m.get('original_id', '')}",
            "category": m["category"].upper(),
            "tactic": f"Backlog find: {m['description'][:60]}",
            "roi_potential": "HIGH" if m["priority"] == "P0" else "MEDIUM",
            "priority": m["priority"],
            "status": "PENDING_REVIEW",
            "applicable_methods": "|".join(m.get("venture_boost", [])),
            "applicable_niches": m["category"],
            "synergy_score": "70" if m["priority"] == "P0" else "50",
            "cross_sell_products": "",
            "implementation_priority": m["priority"],
            "engagement_authenticity": "N/A",
            "earnings_verified": "N/A",
            "extracted_method": m.get("original_text", "")[:300],
            "compliance_notes": "From internal alpha backlog — no compliance issues",
            "reviewer_notes": (f"Backlog match: {m['category']}, "
                               f"pattern: {m.get('pattern_matched', '')[:50]}, "
                               f"original: {m.get('original_source', '')}"),
            "created_at": datetime.now().isoformat(),
            "ops_generated": "no",
        }
        new_entries.append(entry)

    if not new_entries:
        return 0

    if dry_run:
        log(f"[DRY-RUN] Would stage {len(new_entries)} backlog matches")
        for e in new_entries[:5]:
            log(f"  - {e['alpha_id']}: {e['tactic'][:80]}")
        return len(new_entries)

    file_exists = ALPHA_STAGING.exists()
    with open(safe_path(ALPHA_STAGING), "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ALPHA_FIELDS)
        if not file_exists:
            writer.writeheader()
        for entry in new_entries:
            writer.writerow(entry)

    return len(new_entries)


def _write_report(matches: list[dict], by_category: dict[str, list[dict]], staged: int) -> None:
    """Write the backlog scan report."""
    report = f"# Alpha Backlog Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    report += f"**Matches found:** {len(matches)}\n"
    report += f"**Staged for integration:** {staged}\n\n"

    for cat, cat_matches in sorted(by_category.items(), key=lambda x: len(x[1]), reverse=True):
        desc = OPPORTUNITY_PATTERNS.get(cat, {}).get("description", cat)
        report += f"## {cat.upper()} — {desc} ({len(cat_matches)} matches)\n\n"
        for m in cat_matches[:15]:
            report += f"- `{m.get('original_id', '?')}` ({m.get('original_source', '?')}): "
            report += f"{m.get('original_text', '')[:100]}\n"
        if len(cat_matches) > 15:
            report += f"- ... and {len(cat_matches) - 15} more\n"
        report += "\n"

    safe_path(BACKLOG_REPORT).write_text(report)
    log(f"Report written to {BACKLOG_REPORT.name}")


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def show_status() -> None:
    print("=" * 60)
    print("ALPHA BACKLOG SCANNER — Status")
    print("=" * 60)

    if BACKLOG_STATE.exists():
        try:
            state = json.loads(safe_path(BACKLOG_STATE).read_text())
            print(f"\nLast scan: {state.get('last_scan', 'never')}")
            print(f"Total scanned: {state.get('total_scanned', 0)}")
            print(f"Matches found: {state.get('matches_found', 0)}")
            print(f"Staged: {state.get('staged', 0)}")
        except Exception:
            print("State file corrupted")
    else:
        print("No previous scan")

    # Count alpha total
    if ALPHA_STAGING.exists():
        try:
            total = sum(1 for _ in open(ALPHA_STAGING)) - 1
            print(f"\nTotal alpha entries: {total}")
        except Exception:
            pass

    # Cron
    try:
        import subprocess
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
        if "alpha_backlog" in result.stdout:
            print("Cron: INSTALLED")
        else:
            print("Cron: NOT INSTALLED (recommended: 0 3 * * 1)")
    except Exception:
        print("Cron: unable to check")

    print("=" * 60)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Alpha Backlog Scanner — mine historical alpha")
    parser.add_argument("--scan", action="store_true", help="Run full backlog scan")
    parser.add_argument("--category", type=str, default="",
                        help="Filter by category (tool_scanner, revenue_method, system_improvement, "
                             "integration_opportunity, growth_tactic)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--run", action="store_true", help="Alias for --scan")

    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.scan or args.run or args.dry_run:
        run_scan(category_filter=args.category, dry_run=args.dry_run)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
