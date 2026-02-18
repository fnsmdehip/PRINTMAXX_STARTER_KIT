#!/usr/bin/env python3
"""
competitor_monitor.py - Track competitor changes and movements

Monitors competitor pricing, features, content, and social presence.
Logs changes to LEDGER for analysis and generates alerts.

Usage:
    python3 competitor_monitor.py --add "CompetitorName" --url https://competitor.com --niche fitness
    python3 competitor_monitor.py --check-all
    python3 competitor_monitor.py --report
    python3 competitor_monitor.py --list

Example:
    # Add a competitor to monitor
    python3 competitor_monitor.py --add "FitApp" --url https://fitapp.com --niche fitness --method MM001

    # Check all competitors for changes
    python3 competitor_monitor.py --check-all

    # Generate competitor report
    python3 competitor_monitor.py --report
"""

import argparse
import csv
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_DIR / "LEDGER"
LOG_DIR = PROJECT_DIR / "AUTOMATIONS" / "logs"
COMPETITOR_FILE = LOG_DIR / "competitor_tracking.csv"
CHANGE_LOG = LOG_DIR / "competitor_changes.csv"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "competitor_monitor.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def load_competitors():
    """Load competitor tracking list."""
    if not COMPETITOR_FILE.exists():
        return []
    with open(COMPETITOR_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def add_competitor(name, url, niche="", method="", notes=""):
    """Add a competitor to the tracking list."""
    fieldnames = [
        "competitor_id", "name", "url", "niche", "method_id",
        "added_date", "last_checked", "pricing", "features",
        "social_followers", "app_rating", "notes", "status",
    ]

    competitors = load_competitors()
    comp_id = f"COMP{len(competitors) + 1:03d}"

    entry = {
        "competitor_id": comp_id,
        "name": name,
        "url": url,
        "niche": niche,
        "method_id": method,
        "added_date": datetime.now().strftime("%Y-%m-%d"),
        "last_checked": "",
        "pricing": "",
        "features": "",
        "social_followers": "",
        "app_rating": "",
        "notes": notes,
        "status": "ACTIVE",
    }

    file_exists = COMPETITOR_FILE.exists()
    with open(COMPETITOR_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)

    logger.info(f"Added competitor: {comp_id} - {name} ({url})")
    return comp_id


def log_change(competitor_id, change_type, old_value, new_value, notes=""):
    """Log a detected change."""
    fieldnames = [
        "date", "competitor_id", "change_type", "old_value",
        "new_value", "notes", "impact",
    ]

    # Assess impact
    impact = "LOW"
    if change_type == "pricing":
        impact = "HIGH"
    elif change_type == "features":
        impact = "MEDIUM"

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "competitor_id": competitor_id,
        "change_type": change_type,
        "old_value": str(old_value)[:200],
        "new_value": str(new_value)[:200],
        "notes": notes,
        "impact": impact,
    }

    file_exists = CHANGE_LOG.exists()
    with open(CHANGE_LOG, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)

    logger.info(f"Logged change: {competitor_id} - {change_type} ({impact} impact)")


def check_competitors():
    """Check all competitors for changes (manual logging prompt)."""
    competitors = load_competitors()

    if not competitors:
        logger.info("No competitors tracked yet. Use --add to add competitors.")
        return

    print("\n" + "=" * 60)
    print("  COMPETITOR CHECK")
    print("=" * 60)

    for comp in competitors:
        if comp.get("status") != "ACTIVE":
            continue

        print(f"\n  [{comp.get('competitor_id')}] {comp.get('name')}")
        print(f"  URL: {comp.get('url')}")
        print(f"  Niche: {comp.get('niche')} | Method: {comp.get('method_id')}")
        print(f"  Last Checked: {comp.get('last_checked', 'NEVER')}")
        print(f"  Current Pricing: {comp.get('pricing', 'Unknown')}")
        print(f"  Rating: {comp.get('app_rating', 'Unknown')}")
        print("  ---")

    print(f"\n  Total Active Competitors: {len([c for c in competitors if c.get('status') == 'ACTIVE'])}")
    print("\n  To log a change:")
    print("  python3 competitor_monitor.py --log-change COMP001 --type pricing --old '$9.99' --new '$14.99'")
    print("=" * 60)


def generate_report():
    """Generate competitor intelligence report."""
    competitors = load_competitors()
    changes = []
    if CHANGE_LOG.exists():
        with open(CHANGE_LOG, newline="", encoding="utf-8") as f:
            changes = list(csv.DictReader(f))

    print("\n" + "=" * 70)
    print("  COMPETITOR INTELLIGENCE REPORT")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    # Summary
    active = [c for c in competitors if c.get("status") == "ACTIVE"]
    print(f"\n  Tracking: {len(active)} active competitors")

    # Recent changes
    recent = sorted(changes, key=lambda x: x.get("date", ""), reverse=True)[:10]
    if recent:
        print(f"\n  {'--- RECENT CHANGES ---':^70}")
        for change in recent:
            print(
                f"  [{change.get('date', '')}] {change.get('competitor_id')} "
                f"| {change.get('change_type')} "
                f"| {change.get('old_value', '')[:30]} -> {change.get('new_value', '')[:30]} "
                f"| Impact: {change.get('impact')}"
            )

    # By niche
    niches = {}
    for c in active:
        niche = c.get("niche", "unknown")
        if niche not in niches:
            niches[niche] = []
        niches[niche].append(c)

    if niches:
        print(f"\n  {'--- BY NICHE ---':^70}")
        for niche, comps in sorted(niches.items()):
            print(f"\n  {niche.upper()} ({len(comps)} competitors):")
            for c in comps:
                print(f"    - {c.get('name')} | {c.get('url')} | Pricing: {c.get('pricing', '?')}")

    print("\n" + "=" * 70)


def print_list():
    """Print list of tracked competitors."""
    competitors = load_competitors()
    if not competitors:
        print("No competitors tracked. Use --add to add one.")
        return

    print(f"\n{'ID':<10} {'Name':<25} {'Niche':<12} {'Method':<10} {'URL'}")
    print("-" * 80)
    for c in competitors:
        print(
            f"{c.get('competitor_id', ''):<10} "
            f"{c.get('name', ''):<25} "
            f"{c.get('niche', ''):<12} "
            f"{c.get('method_id', ''):<10} "
            f"{c.get('url', '')}"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Monitor competitor changes and generate intelligence"
    )
    parser.add_argument("--add", type=str, default=None, help="Add competitor by name")
    parser.add_argument("--url", type=str, default="", help="Competitor URL")
    parser.add_argument("--niche", type=str, default="", help="Competitor niche")
    parser.add_argument("--method", type=str, default="", help="Related method ID")
    parser.add_argument("--check-all", action="store_true", help="Check all competitors")
    parser.add_argument("--report", action="store_true", help="Generate competitor report")
    parser.add_argument("--list", action="store_true", help="List all competitors")
    parser.add_argument("--log-change", type=str, default=None, help="Log change for competitor ID")
    parser.add_argument("--type", type=str, default="", help="Change type (pricing/features/etc)")
    parser.add_argument("--old", type=str, default="", help="Old value")
    parser.add_argument("--new", type=str, default="", help="New value")
    parser.add_argument("--notes", type=str, default="", help="Notes")
    args = parser.parse_args()

    if args.add:
        add_competitor(args.add, args.url, args.niche, args.method, args.notes)
    elif args.check_all:
        check_competitors()
    elif args.report:
        generate_report()
    elif args.list:
        print_list()
    elif args.log_change:
        log_change(args.log_change, args.type, args.old, args.new, args.notes)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
