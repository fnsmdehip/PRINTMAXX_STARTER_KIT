#!/usr/bin/env python3
"""
PRINTMAXX Daily Agent Runner - Auto-orient any new agent in 10 seconds.

Usage:
    python3 AUTOMATIONS/daily_agent_runner.py --status       # Quick orientation
    python3 AUTOMATIONS/daily_agent_runner.py --priorities    # Full priority list
    python3 AUTOMATIONS/daily_agent_runner.py --learning "X"  # Log a learning
    python3 AUTOMATIONS/daily_agent_runner.py --execute       # Auto-execute top priority
"""

import os
import sys
import csv
import json
import glob
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
LEDGER = BASE / "LEDGER"
OPS = BASE / "OPS"
FINANCIALS = BASE / "FINANCIALS"
PRODUCTS = BASE / "PRODUCTS"
AUTOMATIONS = BASE / "AUTOMATIONS"
LEARNINGS = LEDGER / "RBI_STRATEGIC" / "LEARNINGS.jsonl"


def read_csv(path, max_rows=500):
    """Read CSV file, return list of dicts."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            return [row for i, row in enumerate(reader) if i < max_rows]
    except Exception:
        return []


def count_lines(path):
    try:
        with open(path, "r") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def file_age_hours(path):
    try:
        mtime = os.path.getmtime(path)
        return (datetime.now().timestamp() - mtime) / 3600
    except Exception:
        return 9999


def get_account_status():
    """Check LEDGER/ACCOUNTS.csv for created vs pending accounts."""
    rows = read_csv(LEDGER / "ACCOUNTS.csv")
    created = sum(1 for r in rows if r.get("status", "").upper() in ("CREATED", "ACTIVE", "WARMED"))
    total = len(rows)
    pending = total - created
    return {"created": created, "total": total, "pending": pending, "rows": rows}


def get_revenue():
    """Check FINANCIALS/REVENUE_TRACKER.csv for total revenue."""
    rows = read_csv(FINANCIALS / "REVENUE_TRACKER.csv")
    total = 0.0
    for r in rows:
        try:
            amt = r.get("amount", r.get("revenue", "0"))
            total += float(str(amt).replace("$", "").replace(",", ""))
        except (ValueError, TypeError):
            pass
    return total


def get_recent_files(hours=24):
    """Find files modified in last N hours."""
    recent = []
    for pattern in ["OPS/*.md", "PRODUCTS/**/*.md", "AUTOMATIONS/*.py",
                     "MONEY_METHODS/**/*.md", "DIGITAL_PRODUCTS/**/*.md",
                     "CONTENT/**/*.md", "LEDGER/*.csv"]:
        for f in glob.glob(str(BASE / pattern), recursive=True):
            if file_age_hours(f) < hours:
                recent.append((f, file_age_hours(f)))
    recent.sort(key=lambda x: x[1])
    return recent[:20]


def get_ready_to_list():
    """Check what products are ready to list but need accounts."""
    ready = []
    checks = [
        ("Gumroad (10 products)", PRODUCTS / "GUMROAD_READY_LISTINGS.md", "$500-10K/mo"),
        ("Fiverr (10 gigs)", PRODUCTS / "FREELANCE_LISTINGS_READY" / "FIVERR_GIGS_10.md", "$500-3K/mo"),
        ("Upwork (5 profiles)", PRODUCTS / "FREELANCE_LISTINGS_READY" / "UPWORK_PROFILES_5.md", "$1-5K/mo"),
        ("Etsy (full listings)", PRODUCTS / "ECOM_LISTINGS_READY" / "ETSY_LISTINGS_COMPLETE.md", "$200-2K/mo"),
        ("Buffer (1,278 posts)", AUTOMATIONS / "content_posting", "$0 (traffic)"),
    ]
    for name, path, rev in checks:
        exists = os.path.exists(path)
        ready.append({"name": name, "ready": exists, "potential": rev})
    return ready


def build_priorities():
    """Build prioritized action list."""
    priorities = []
    accts = get_account_status()
    revenue = get_revenue()

    # TIER 1: Revenue-blocking
    if accts["created"] < 3:
        priorities.append({
            "tier": 1, "action": "CREATE ACCOUNTS (Stripe → Gumroad → Fiverr)",
            "file": "OPS/ACCOUNT_CREATION_NOW.md",
            "reason": f"Only {accts['created']}/{accts['total']} accounts active. This blocks ALL revenue.",
            "est_revenue": "$500-10K/mo", "est_hours": 2.5, "human_required": True
        })

    # Check if Ramadan app deployed
    ramadan_dir = BASE / "ralph" / "loops" / "app_factory" / "output" / "ramadan-tracker"
    if ramadan_dir.exists():
        days_to_ramadan = (datetime(2026, 2, 28) - datetime.now()).days
        if days_to_ramadan > 0:
            priorities.append({
                "tier": 1, "action": f"DEPLOY RAMADAN APP ({days_to_ramadan} days until Ramadan!)",
                "file": "ralph/loops/app_factory/output/ramadan-tracker/",
                "reason": "App built, needs vercel deploy. Time-sensitive.",
                "est_revenue": "$200-2K (seasonal)", "est_hours": 0.5, "human_required": True
            })

    # TIER 2: Revenue-generating (need accounts first)
    if accts["created"] >= 1:
        for item in get_ready_to_list():
            if item["ready"]:
                priorities.append({
                    "tier": 2, "action": f"LIST: {item['name']}",
                    "file": str(item["name"]),
                    "reason": "Product ready, just needs copy-paste to platform",
                    "est_revenue": item["potential"], "est_hours": 0.5, "human_required": True
                })

    # TIER 3: Revenue-supporting (automatable)
    priorities.append({
        "tier": 3, "action": "POST CONTENT (1,278 posts ready)",
        "file": "AUTOMATIONS/content_posting/",
        "reason": "Upload Buffer CSVs for scheduled posting",
        "est_revenue": "$0 direct (traffic generation)", "est_hours": 1, "human_required": False
    })

    priorities.append({
        "tier": 3, "action": "RUN COLD EMAIL SEQUENCES",
        "file": "AUTOMATIONS/content_posting/cold_email_sequences_ready.csv",
        "reason": "Email sequences built, need email accounts + sending",
        "est_revenue": "$500-3K/mo", "est_hours": 2, "human_required": True
    })

    # TIER 4: Infrastructure
    priorities.append({
        "tier": 4, "action": "RUN RBI SCANNER",
        "file": "python3 AUTOMATIONS/daily_nocost_rbi_scanner.py --next-actions",
        "reason": "Check for new zero-cost opportunities",
        "est_revenue": "varies", "est_hours": 0.1, "human_required": False
    })

    return sorted(priorities, key=lambda x: (x["tier"], -len(x.get("est_revenue", ""))))


def print_status():
    """Print quick 10-second orientation."""
    now = datetime.now()
    accts = get_account_status()
    revenue = get_revenue()
    recent = get_recent_files(24)
    priorities = build_priorities()

    print(f"""
{'='*60}
  PRINTMAXX DAILY STATUS — {now.strftime('%Y-%m-%d %H:%M')}
{'='*60}

REVENUE: ${revenue:.2f} total (target: $1K/mo)
ACCOUNTS: {accts['created']}/{accts['total']} active {'⚠ BLOCKED' if accts['created'] < 3 else '✓'}
RAMADAN: {(datetime(2026, 2, 28) - now).days} days away (app built, needs deploy)
FILES MODIFIED (24h): {len(recent)}

{'─'*60}
TOP 5 PRIORITIES:
{'─'*60}""")

    for i, p in enumerate(priorities[:5], 1):
        human = " [HUMAN]" if p.get("human_required") else " [AUTO]"
        print(f"  {i}. [TIER {p['tier']}]{human} {p['action']}")
        print(f"     → {p['reason']}")
        print(f"     Est: {p['est_revenue']} | Time: {p['est_hours']}h")
        print(f"     File: {p['file']}")
        print()

    if recent:
        print(f"{'─'*60}")
        print("RECENT FILES (last 24h):")
        print(f"{'─'*60}")
        for path, age in recent[:10]:
            rel = os.path.relpath(path, BASE)
            print(f"  {age:5.1f}h ago  {rel}")

    print(f"""
{'─'*60}
NEXT ACTION: {priorities[0]['action'] if priorities else 'No priorities found'}
{'─'*60}
Read: OPS/AGENT_DAILY_PLAYBOOK.md for full guide
Run:  python3 AUTOMATIONS/venture_performance_tracker.py --recommend
{'='*60}
""")


def print_priorities():
    """Print full priority list."""
    priorities = build_priorities()
    print(f"\nFULL PRIORITY LIST ({len(priorities)} items):\n")
    for i, p in enumerate(priorities, 1):
        human = "HUMAN" if p.get("human_required") else "AUTO"
        print(f"  {i:2}. TIER {p['tier']} [{human}] {p['action']}")
        print(f"      Revenue: {p['est_revenue']} | Hours: {p['est_hours']}")
        print(f"      File: {p['file']}")
        print()


def log_learning(text):
    """Append learning to LEARNINGS.jsonl."""
    os.makedirs(LEARNINGS.parent, exist_ok=True)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "learning": text,
        "session": "agent_runner",
        "source": "daily_agent_runner.py"
    }
    with open(LEARNINGS, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"✓ Learning logged to {LEARNINGS.relative_to(BASE)}")
    print(f"  Total learnings: {count_lines(LEARNINGS)}")


def main():
    args = sys.argv[1:]

    if not args or "--status" in args:
        print_status()
    elif "--priorities" in args:
        print_priorities()
    elif "--learning" in args:
        idx = args.index("--learning")
        if idx + 1 < len(args):
            log_learning(args[idx + 1])
        else:
            print("Usage: --learning 'what you learned'")
    elif "--execute" in args:
        priorities = build_priorities()
        auto = [p for p in priorities if not p.get("human_required")]
        if auto:
            print(f"Auto-executing: {auto[0]['action']}")
            print(f"File: {auto[0]['file']}")
            # Could add subprocess execution here
        else:
            print("No auto-executable priorities. All require human action.")
            print("Top human action:", priorities[0]["action"] if priorities else "none")
    else:
        print("Usage: python3 daily_agent_runner.py [--status|--priorities|--learning 'text'|--execute]")


if __name__ == "__main__":
    main()
