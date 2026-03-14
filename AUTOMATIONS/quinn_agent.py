#!/usr/bin/env python3
"""
QUINN AGENT — Warm Outreach Generation (Swan AI GTM T015)
==========================================================

Generates personalized warm outreach messages for inbound leads detected
by observer_agent.py. Each message references the specific engagement
signal from the lead's row in INBOUND_LEADS.csv.

NOT cold templates. Every message references actual engagement:
  "Saw you [specific engagement] on [post topic]. That's exactly the
  [challenge] we solve at EAS. Worth a 15-min chat?"

A/B testing built in: 50% Quinn warm outreach, 50% standard cold sequence.

Usage:
    python3 quinn_agent.py --process       # Process NEW leads from INBOUND_LEADS.csv
    python3 quinn_agent.py --status        # Show outreach stats
    python3 quinn_agent.py --dry-run       # Preview without writing

Output: LEDGER/OUTREACH_QUEUE.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import sys
from datetime import datetime
from hashlib import md5
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
INBOUND_LEADS = PROJECT / "LEDGER" / "INBOUND_LEADS.csv"
OUTREACH_QUEUE = PROJECT / "LEDGER" / "OUTREACH_QUEUE.csv"
STATE_FILE = AUTOMATIONS / "agent" / "quinn_state.json"

OUTREACH_HEADER = [
    "timestamp", "lead_username", "platform", "message",
    "template_type", "source_engagement", "status", "ab_group",
]

# ── Engagement Type to Verb Mapping ──────────────────────────────────
ENGAGEMENT_VERBS = {
    "reply": "replied to our post about",
    "keyword_mention": "posted about",
    "like": "engaged with our content on",
    "retweet": "shared our take on",
    "quote": "quoted our thoughts on",
    "mention": "mentioned us while discussing",
    "follow": "followed us after seeing our content on",
    "dm": "reached out about",
}

# ── Topic Extraction from Source Post ────────────────────────────────
TOPIC_KEYWORDS = {
    "AI automation": "AI automation systems",
    "agent system": "autonomous agent architecture",
    "Claude Code": "Claude Code for solopreneurs",
    "autonomous": "autonomous business operations",
    "solopreneur": "solopreneur leverage",
    "cold email": "cold outreach automation",
    "scraping": "data scraping pipelines",
    "pipeline": "automated pipelines",
    "revenue": "revenue automation",
    "build in public": "building in public",
    "agent swarm": "multi-agent systems",
    "implementation gap": "the implementation gap",
    "printmaxx": "the PRINTMAXX system",
}

# ── Challenge Mapping by Lead Type ───────────────────────────────────
CHALLENGE_MAP = {
    "agency_founder": [
        "scaling without adding headcount",
        "automating client delivery",
        "building systems that run without you",
        "reducing operational overhead",
    ],
    "agency_employee": [
        "doing more with less resources",
        "automating repetitive workflows",
        "proving ROI on automation investments",
        "streamlining multi-client operations",
    ],
    "consultant": [
        "productizing your expertise",
        "scaling beyond billable hours",
        "building leverage through systems",
        "creating recurring revenue from knowledge",
    ],
    "other": [
        "building without a team",
        "automating the boring parts",
        "going from $0 to first dollar",
        "turning knowledge into systems",
    ],
}


# ── Message Generation ───────────────────────────────────────────────

def extract_topic(source_post: str) -> str:
    """Extract a topic from the source post text."""
    source_lower = source_post.lower()
    for keyword, topic in TOPIC_KEYWORDS.items():
        if keyword.lower() in source_lower:
            return topic
    # Fallback: extract first meaningful phrase
    words = source_post.split()[:8]
    if len(words) >= 3:
        return " ".join(words[:5]).rstrip(".,!?")
    return "AI-driven business automation"


def generate_warm_message(lead: dict[str, str]) -> str:
    """Generate a personalized warm outreach message based on the lead's
    engagement signal. NOT a cold template."""

    username = lead.get("username", "").strip()
    engagement_type = lead.get("engagement_type", "keyword_mention").strip()
    source_post = lead.get("source_post", "").strip()
    lead_type = lead.get("lead_type", "other").strip()

    # Get the engagement verb
    verb = ENGAGEMENT_VERBS.get(engagement_type, "engaged with content about")

    # Extract the topic from source post
    topic = extract_topic(source_post)

    # Pick a challenge relevant to their lead type
    challenges = CHALLENGE_MAP.get(lead_type, CHALLENGE_MAP["other"])
    challenge = random.choice(challenges)

    # Build the message
    if source_post and len(source_post) > 20:
        # Specific message referencing their actual engagement
        templates = [
            (
                f"saw you {verb} {topic}. "
                f"that's exactly the kind of {challenge} problem we've been solving with "
                f"autonomous agent systems. 33 agents, $200/mo, zero employees. "
                f"worth a 15-min chat to compare notes?"
            ),
            (
                f"noticed your take on {topic}. "
                f"we built a system that handles {challenge} automatically. "
                f"CEO agent orchestrates 25 operational agents across 8 ventures. "
                f"happy to share the architecture if you're interested. 15 min?"
            ),
            (
                f"your post about {topic} caught my attention. "
                f"we've been tackling {challenge} with a different approach. "
                f"fully autonomous pipeline: scrape, score, route, build, deploy. "
                f"zero human hours after setup. want to see how it works?"
            ),
        ]
    else:
        # More general but still warm message (for vague engagement signals)
        templates = [
            (
                f"noticed you're in the {lead_type.replace('_', ' ')} space. "
                f"we've built a system for {challenge} that runs on 33 autonomous agents. "
                f"total cost: $200/mo. no team needed. "
                f"worth a quick chat?"
            ),
            (
                f"saw your engagement in the AI automation space. "
                f"we're solving {challenge} with autonomous agent swarms. "
                f"everything from scraping to content generation to lead routing runs 24/7. "
                f"15 min to compare approaches?"
            ),
            (
                f"looks like you're building in the automation space too. "
                f"we went deep on {challenge} with a multi-agent architecture. "
                f"happy to share what's working and what isn't. no pitch, just real talk."
            ),
        ]

    message = random.choice(templates)
    return message


def generate_cold_message(lead: dict[str, str]) -> str:
    """Generate a standard cold outreach message (for A/B control group)."""
    lead_type = lead.get("lead_type", "other").strip()
    challenges = CHALLENGE_MAP.get(lead_type, CHALLENGE_MAP["other"])
    challenge = random.choice(challenges)

    templates = [
        (
            f"hi, we help {lead_type.replace('_', ' ')}s with {challenge}. "
            f"using AI agent systems to automate operations. "
            f"would you be open to a 15-minute call?"
        ),
        (
            f"reaching out because we work with {lead_type.replace('_', ' ')}s "
            f"looking to solve {challenge}. "
            f"our system runs 33 autonomous agents for $200/mo. "
            f"worth exploring?"
        ),
    ]

    return random.choice(templates)


def assign_ab_group(username: str) -> str:
    """Deterministically assign A/B group based on username hash.
    This ensures the same lead always gets the same group."""
    hash_val = int(md5(username.encode()).hexdigest(), 16)
    return "WARM_QUINN" if hash_val % 2 == 0 else "COLD_STANDARD"


# ── CSV Helpers ──────────────────────────────────────────────────────

def ensure_outreach_csv() -> None:
    """Create OUTREACH_QUEUE.csv with header if it doesn't exist."""
    if not OUTREACH_QUEUE.exists():
        OUTREACH_QUEUE.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTREACH_QUEUE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(OUTREACH_HEADER)
        log(f"Created {OUTREACH_QUEUE.name}", tag="QUINN")


def load_outreach_queue() -> list[dict[str, str]]:
    """Load existing outreach queue to check for duplicates."""
    rows = []
    if OUTREACH_QUEUE.exists():
        try:
            with open(OUTREACH_QUEUE, newline="", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(row)
        except Exception:
            pass
    return rows


def write_outreach(entry: dict[str, Any]) -> None:
    """Append an outreach entry to OUTREACH_QUEUE.csv."""
    ensure_outreach_csv()
    safe_path(OUTREACH_QUEUE)
    with open(OUTREACH_QUEUE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            entry.get("timestamp", datetime.now().isoformat()),
            entry.get("lead_username", ""),
            entry.get("platform", "twitter"),
            entry.get("message", ""),
            entry.get("template_type", "WARM"),
            entry.get("source_engagement", "")[:200],
            entry.get("status", "PENDING_REVIEW"),
            entry.get("ab_group", "WARM_QUINN"),
        ])


def load_inbound_leads() -> list[dict[str, str]]:
    """Load leads from INBOUND_LEADS.csv."""
    leads = []
    if not INBOUND_LEADS.exists():
        log("INBOUND_LEADS.csv not found. Run observer_agent.py --scan first.", tag="QUINN")
        return leads
    try:
        with open(INBOUND_LEADS, newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                leads.append(row)
    except Exception as e:
        log(f"Error reading INBOUND_LEADS.csv: {e}", level="ERROR", tag="QUINN")
    return leads


def update_lead_status(username: str, new_status: str) -> None:
    """Update a lead's status in INBOUND_LEADS.csv."""
    if not INBOUND_LEADS.exists():
        return

    rows = []
    updated = False
    try:
        with open(INBOUND_LEADS, newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row.get("username", "") == username and row.get("status", "").upper() == "NEW":
                    row["status"] = new_status
                    updated = True
                rows.append(row)
    except Exception:
        return

    if updated and fieldnames:
        safe_path(INBOUND_LEADS)
        with open(INBOUND_LEADS, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


# ── State Management ─────────────────────────────────────────────────

def load_state() -> dict[str, Any]:
    state = load_json(STATE_FILE, {})
    if not state:
        state = {
            "total_processed": 0,
            "total_warm": 0,
            "total_cold": 0,
            "last_process_date": None,
            "ab_distribution": {"WARM_QUINN": 0, "COLD_STANDARD": 0},
        }
    return state


def save_state(state: dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    safe_path(STATE_FILE)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# ── CLI Commands ─────────────────────────────────────────────────────

def cmd_process(dry_run: bool = False) -> None:
    """Process NEW leads from INBOUND_LEADS.csv and generate outreach."""
    log("Processing new inbound leads for warm outreach", tag="QUINN")

    leads = load_inbound_leads()
    if not leads:
        print("No leads found. Run observer_agent.py --scan first.")
        return

    # Filter to NEW status only
    new_leads = [l for l in leads if l.get("status", "").upper() == "NEW"]
    if not new_leads:
        print(f"No NEW leads to process ({len(leads)} total leads, all already processed).")
        return

    log(f"Found {len(new_leads)} NEW leads to process", tag="QUINN")

    # Check existing outreach queue for duplicates
    existing_outreach = load_outreach_queue()
    existing_usernames = {r.get("lead_username", "") for r in existing_outreach}

    state = load_state()
    processed = 0
    warm_count = 0
    cold_count = 0

    for lead in new_leads:
        username = lead.get("username", "").strip()
        if not username:
            continue

        # Skip if already in outreach queue
        if username in existing_usernames:
            log(f"Skipping @{username}, already in outreach queue", tag="QUINN")
            continue

        # A/B assignment
        ab_group = assign_ab_group(username)

        # Generate message based on A/B group
        if ab_group == "WARM_QUINN":
            message = generate_warm_message(lead)
            template_type = "WARM"
            warm_count += 1
        else:
            message = generate_cold_message(lead)
            template_type = "COLD"
            cold_count += 1

        source_engagement = lead.get("source_post", lead.get("engagement_type", ""))

        if dry_run:
            print(f"\n  [DRY RUN] @{username} ({ab_group})")
            print(f"  Type: {template_type} | Lead: {lead.get('lead_type', '?')}")
            print(f"  Message: {message[:150]}...")
        else:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "lead_username": username,
                "platform": lead.get("platform", "twitter"),
                "message": message,
                "template_type": template_type,
                "source_engagement": source_engagement[:200],
                "status": "PENDING_REVIEW",
                "ab_group": ab_group,
            }
            write_outreach(entry)
            update_lead_status(username, "OUTREACH_QUEUED")

        processed += 1
        existing_usernames.add(username)

    # Update state
    state["total_processed"] = state.get("total_processed", 0) + processed
    state["total_warm"] = state.get("total_warm", 0) + warm_count
    state["total_cold"] = state.get("total_cold", 0) + cold_count
    state["last_process_date"] = datetime.now().strftime("%Y-%m-%d")
    ab_dist = state.get("ab_distribution", {"WARM_QUINN": 0, "COLD_STANDARD": 0})
    ab_dist["WARM_QUINN"] = ab_dist.get("WARM_QUINN", 0) + warm_count
    ab_dist["COLD_STANDARD"] = ab_dist.get("COLD_STANDARD", 0) + cold_count
    state["ab_distribution"] = ab_dist
    save_state(state)

    action = "Would process" if dry_run else "Processed"
    print(f"\n{action} {processed} leads:")
    print(f"  WARM_QUINN (personalized):  {warm_count}")
    print(f"  COLD_STANDARD (control):    {cold_count}")
    if not dry_run:
        print(f"  Output: {OUTREACH_QUEUE}")


def cmd_status() -> None:
    """Show outreach stats."""
    state = load_state()
    print("QUINN AGENT STATUS")
    print("=" * 50)
    print(f"  Total processed:    {state.get('total_processed', 0)}")
    print(f"  Warm messages:      {state.get('total_warm', 0)}")
    print(f"  Cold messages:      {state.get('total_cold', 0)}")
    print(f"  Last process date:  {state.get('last_process_date', 'never')}")

    # A/B distribution
    ab = state.get("ab_distribution", {})
    total_ab = sum(ab.values())
    if total_ab > 0:
        warm_pct = ab.get("WARM_QUINN", 0) / total_ab * 100
        cold_pct = ab.get("COLD_STANDARD", 0) / total_ab * 100
        print(f"\n  A/B Distribution:")
        print(f"    WARM_QUINN:     {ab.get('WARM_QUINN', 0)} ({warm_pct:.0f}%)")
        print(f"    COLD_STANDARD:  {ab.get('COLD_STANDARD', 0)} ({cold_pct:.0f}%)")

    # Outreach queue summary
    outreach = load_outreach_queue()
    if outreach:
        pending = sum(1 for r in outreach if r.get("status", "").upper() == "PENDING_REVIEW")
        sent = sum(1 for r in outreach if r.get("status", "").upper() == "SENT")
        print(f"\n  Outreach Queue:")
        print(f"    Total:           {len(outreach)}")
        print(f"    PENDING_REVIEW:  {pending}")
        print(f"    SENT:            {sent}")
    else:
        print(f"\n  Outreach queue: empty")

    # Inbound leads status
    leads = load_inbound_leads()
    if leads:
        new = sum(1 for l in leads if l.get("status", "").upper() == "NEW")
        queued = sum(1 for l in leads if l.get("status", "").upper() == "OUTREACH_QUEUED")
        print(f"\n  Inbound Leads:")
        print(f"    Total:           {len(leads)}")
        print(f"    NEW (unprocessed): {new}")
        print(f"    OUTREACH_QUEUED: {queued}")
    else:
        print(f"\n  No inbound leads found. Run observer_agent.py --scan first.")

    # Dependencies
    print(f"\n  Intelligence router:  {'AVAILABLE' if _ROUTER_AVAILABLE else 'NOT AVAILABLE'}")
    print(f"  Master ops bridge:    {'AVAILABLE' if _BRIDGE_AVAILABLE else 'NOT AVAILABLE'}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Quinn Agent -- Warm outreach generation for inbound leads"
    )
    parser.add_argument("--process", action="store_true",
                        help="Process NEW leads from INBOUND_LEADS.csv")
    parser.add_argument("--status", action="store_true",
                        help="Show outreach stats")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without writing")
    args = parser.parse_args()

    if args.process:
        cmd_process(dry_run=args.dry_run)
    elif args.status:
        cmd_status()
    else:
        cmd_status()


if __name__ == "__main__":
    main()
