#!/usr/bin/env python3
"""
source_scraper.py - Scrape high-signal accounts from HIGH_SIGNAL_SOURCES.csv

Reads the source list, identifies accounts marked for auto-monitoring,
and provides scraping infrastructure for Twitter, Reddit, and other platforms.
Outputs structured data to ALPHA_STAGING.csv.

Usage:
    python3 source_scraper.py --list
    python3 source_scraper.py --platform twitter --limit 20
    python3 source_scraper.py --platform reddit --subreddits SaaS,juststart
    python3 source_scraper.py --source @pipelineabuser

Example:
    # List all auto-monitor sources
    python3 source_scraper.py --list

    # Show top 20 Twitter sources to scrape
    python3 source_scraper.py --platform twitter --limit 20

    # Show Reddit sources
    python3 source_scraper.py --platform reddit
"""

import argparse
import csv
import json
import logging
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_DIR / "LEDGER"
SOURCES_FILE = LEDGER_DIR / "HIGH_SIGNAL_SOURCES.csv"
LOG_DIR = PROJECT_DIR / "AUTOMATIONS" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "source_scraper.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def load_sources():
    """Load HIGH_SIGNAL_SOURCES.csv."""
    if not SOURCES_FILE.exists():
        logger.error(f"Sources file not found: {SOURCES_FILE}")
        return []

    with open(SOURCES_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def filter_sources(sources, platform=None, auto_only=True, limit=None):
    """Filter sources by criteria."""
    filtered = []
    for s in sources:
        # Check auto_monitor
        if auto_only and s.get("auto_monitor", "").upper() != "TRUE":
            continue
        # Check platform
        if platform:
            source_platform = s.get("platform", "").lower()
            source_type = s.get("source_type", "").lower()
            if platform.lower() not in (source_platform, source_type):
                continue
        filtered.append(s)

    # Sort by signal quality if available
    try:
        filtered.sort(
            key=lambda x: int(x.get("signal_quality", 0)),
            reverse=True,
        )
    except (ValueError, TypeError):
        pass

    if limit:
        filtered = filtered[:limit]

    return filtered


def list_sources(sources):
    """Print formatted source list."""
    print("\n" + "=" * 90)
    print("  HIGH SIGNAL SOURCES")
    print("=" * 90)

    # Group by platform
    platforms = {}
    for s in sources:
        plat = s.get("platform", s.get("source_type", "unknown"))
        if plat not in platforms:
            platforms[plat] = []
        platforms[plat].append(s)

    for plat, items in sorted(platforms.items()):
        print(f"\n  --- {plat.upper()} ({len(items)} sources) ---")
        for s in items:
            handle = s.get("handle", s.get("source_name", ""))
            quality = s.get("signal_quality", "?")
            category = s.get("category", s.get("primary_category", ""))
            auto = "AUTO" if s.get("auto_monitor", "").upper() == "TRUE" else "    "
            print(f"  [{auto}] {handle:<30} Q:{quality:<3} Cat: {category}")

    total_auto = len([s for s in sources if s.get("auto_monitor", "").upper() == "TRUE"])
    print(f"\n  Total Sources: {len(sources)}")
    print(f"  Auto-Monitor: {total_auto}")
    print("=" * 90)


def generate_scrape_plan(sources, platform):
    """Generate a scraping plan for the given platform."""
    filtered = filter_sources(sources, platform=platform, auto_only=True)

    plan = {
        "platform": platform,
        "total_sources": len(filtered),
        "sources": [],
    }

    for s in filtered:
        handle = s.get("handle", s.get("source_name", ""))
        plan["sources"].append({
            "handle": handle,
            "url": s.get("url", s.get("source_url", "")),
            "category": s.get("category", s.get("primary_category", "")),
            "signal_quality": s.get("signal_quality", ""),
            "notes": s.get("notes", ""),
        })

    return plan


def generate_twitter_urls(sources):
    """Generate Twitter scraping URLs for all auto-monitor accounts."""
    filtered = filter_sources(sources, platform="twitter", auto_only=True)

    urls = []
    for s in filtered:
        handle = s.get("handle", "").lstrip("@")
        if handle:
            urls.append(f"https://x.com/{handle}")

    return urls


def main():
    parser = argparse.ArgumentParser(
        description="Manage and scrape high-signal sources for alpha extraction"
    )
    parser.add_argument("--list", action="store_true", help="List all sources")
    parser.add_argument(
        "--platform",
        type=str,
        default=None,
        help="Filter by platform (twitter, reddit, etc.)",
    )
    parser.add_argument("--limit", type=int, default=None, help="Limit results")
    parser.add_argument("--source", type=str, default=None, help="Show specific source details")
    parser.add_argument("--urls", action="store_true", help="Output scraping URLs")
    parser.add_argument("--plan", action="store_true", help="Generate scraping plan")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    sources = load_sources()

    if not sources:
        logger.error("No sources loaded")
        sys.exit(1)

    if args.list:
        if args.platform:
            sources = filter_sources(sources, platform=args.platform, auto_only=False, limit=args.limit)
        list_sources(sources)

    elif args.urls:
        urls = generate_twitter_urls(sources)
        if args.limit:
            urls = urls[:args.limit]
        for url in urls:
            print(url)
        logger.info(f"Generated {len(urls)} scraping URLs")

    elif args.plan:
        if not args.platform:
            args.platform = "twitter"
        plan = generate_scrape_plan(sources, args.platform)
        if args.output == "json":
            print(json.dumps(plan, indent=2))
        else:
            print(f"\n  Scraping Plan: {plan['platform'].upper()}")
            print(f"  Sources: {plan['total_sources']}")
            for s in plan["sources"]:
                print(f"    {s['handle']:<30} | {s['category']:<20} | Q:{s['signal_quality']}")

    elif args.source:
        matches = [
            s for s in sources
            if args.source.lower() in (
                s.get("handle", "").lower(),
                s.get("source_name", "").lower(),
            )
        ]
        if matches:
            for m in matches:
                print(json.dumps(m, indent=2))
        else:
            print(f"Source not found: {args.source}")

    else:
        list_sources(sources)


if __name__ == "__main__":
    main()
