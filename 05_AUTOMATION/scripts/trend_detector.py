#!/usr/bin/env python3
"""
trend_detector.py - Identify trending topics, methods, and opportunities

Analyzes ALPHA_STAGING.csv entries, content performance data, and method
tracking to detect trends. Identifies rising methods, hot niches,
and emerging opportunities.

Usage:
    python3 trend_detector.py
    python3 trend_detector.py --days 7
    python3 trend_detector.py --category APP_FACTORY
    python3 trend_detector.py --output json

Example:
    # Detect trends from last 14 days of alpha
    python3 trend_detector.py --days 14

    # Detect trends in a specific category
    python3 trend_detector.py --category OUTBOUND

    # Get trends as JSON for other scripts
    python3 trend_detector.py --output json
"""

import argparse
import csv
import json
import logging
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_DIR / "LEDGER"
LOG_DIR = PROJECT_DIR / "AUTOMATIONS" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "trend_detector.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def load_csv(filepath):
    """Load CSV safely."""
    if not filepath.exists():
        return []
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def extract_topics(entries):
    """Extract topic keywords from alpha entries."""
    topic_words = Counter()
    # Important business/tech terms to track
    signal_words = {
        "mcp", "ai", "agent", "tiktok", "instagram", "youtube", "facebook",
        "reels", "shorts", "cold email", "newsletter", "gumroad", "whop",
        "stripe", "subscription", "paywall", "freemium", "notion", "template",
        "saas", "micro", "automation", "scraper", "persona", "ugc", "faceless",
        "affiliate", "seo", "geo", "aso", "app", "mobile", "react native",
        "next.js", "remix", "astro", "supabase", "vercel", "cloudflare",
        "vibe coding", "cursor", "claude", "chatgpt", "gemini", "midjourney",
        "kling", "suno", "heygen", "d-id", "remotion", "skool", "community",
        "course", "coaching", "consulting", "arbitrage", "print on demand",
        "dropship", "amazon", "ebay", "etsy", "pinterest", "linkedin",
        "threads", "bluesky", "podcast", "webinar", "funnel",
    }

    for entry in entries:
        text = (
            entry.get("title", "") + " " +
            entry.get("description", "") + " " +
            entry.get("category", "")
        ).lower()

        for word in signal_words:
            if word in text:
                topic_words[word] += 1

    return topic_words


def detect_category_trends(entries, days=14):
    """Detect trending categories from alpha entries."""
    now = datetime.now()
    cutoff = now - timedelta(days=days)

    recent = []
    older = []

    for entry in entries:
        # Try to determine entry date from alpha_id or reviewed_date
        reviewed = entry.get("reviewed_date", "")
        try:
            entry_date = datetime.strptime(reviewed, "%Y-%m-%d")
        except ValueError:
            # Estimate from alpha_id number
            alpha_id = entry.get("alpha_id", "")
            match = re.search(r"\d+", alpha_id)
            if match:
                num = int(match.group())
                # Rough heuristic: recent entries have higher numbers
                if num > 400:
                    recent.append(entry)
                else:
                    older.append(entry)
            continue

        if entry_date >= cutoff:
            recent.append(entry)
        else:
            older.append(entry)

    recent_cats = Counter(e.get("category", "UNKNOWN") for e in recent)
    older_cats = Counter(e.get("category", "UNKNOWN") for e in older)

    trends = []
    all_cats = set(list(recent_cats.keys()) + list(older_cats.keys()))

    for cat in all_cats:
        recent_count = recent_cats.get(cat, 0)
        older_count = older_cats.get(cat, 0)

        if older_count > 0:
            growth = ((recent_count - older_count) / older_count) * 100
        elif recent_count > 0:
            growth = 100
        else:
            growth = 0

        trends.append({
            "category": cat,
            "recent_entries": recent_count,
            "older_entries": older_count,
            "growth_pct": round(growth, 1),
            "direction": "UP" if growth > 20 else "DOWN" if growth < -20 else "STABLE",
        })

    trends.sort(key=lambda x: x["growth_pct"], reverse=True)
    return trends


def detect_roi_trends(entries):
    """Identify which ROI categories are trending."""
    roi_counts = Counter()
    for entry in entries:
        roi = entry.get("roi_potential", "UNKNOWN")
        roi_counts[roi] += 1

    return dict(roi_counts)


def detect_source_trends(entries):
    """Identify which sources are producing the most alpha."""
    sources = Counter()
    for entry in entries:
        source = entry.get("source", "unknown")
        # Clean up source
        if source.startswith("@"):
            sources[source] += 1
        else:
            sources[source.split("/")[0] if "/" in source else source] += 1

    return sources.most_common(15)


def detect_emerging_methods(entries):
    """Find methods that appear frequently in recent alpha but aren't in our tracker."""
    methods = load_csv(LEDGER_DIR / "MONEY_METHODS_TRACKER.csv")
    known_methods = {m.get("method_name", "").lower() for m in methods}

    # Look for method-like patterns in descriptions
    method_mentions = Counter()
    for entry in entries:
        text = (entry.get("description", "") + " " + entry.get("title", "")).lower()
        # Common method patterns
        patterns = [
            r"(\w+ as a service)", r"(\w+ arbitrage)", r"(\w+ agency)",
            r"(\w+ automation)", r"ai (\w+)", r"(\w+ bots?)",
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if match not in known_methods and len(match) > 3:
                    method_mentions[match] += 1

    return method_mentions.most_common(10)


def print_trend_report(category_trends, topics, roi, sources, emerging, days):
    """Print formatted trend report."""
    print("\n" + "=" * 70)
    print(f"  PRINTMAXX TREND DETECTOR (Last {days} days)")
    print("=" * 70)

    # Category trends
    print(f"\n  {'--- CATEGORY TRENDS ---':^70}")
    for t in category_trends[:10]:
        direction = {"UP": "^", "DOWN": "v", "STABLE": "="}[t["direction"]]
        print(
            f"  {direction} {t['category']:<25} "
            f"Recent: {t['recent_entries']:>3} | "
            f"Older: {t['older_entries']:>3} | "
            f"Growth: {t['growth_pct']:>+6.1f}%"
        )

    # Hot topics
    print(f"\n  {'--- HOT TOPICS ---':^70}")
    for topic, count in topics.most_common(15):
        bar = "#" * min(count, 30)
        print(f"  {topic:<20} {count:>4} {bar}")

    # Top sources
    print(f"\n  {'--- TOP SOURCES ---':^70}")
    for source, count in sources:
        print(f"  {source:<30} {count:>4} entries")

    # ROI distribution
    print(f"\n  {'--- ROI DISTRIBUTION ---':^70}")
    for roi_level, count in sorted(roi.items()):
        print(f"  {roi_level:<15} {count:>4}")

    # Emerging methods
    if emerging:
        print(f"\n  {'--- EMERGING METHODS ---':^70}")
        for method, count in emerging:
            print(f"  {method:<35} mentioned {count}x")

    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Detect trends in alpha entries and method performance"
    )
    parser.add_argument("--days", type=int, default=14, help="Lookback period in days")
    parser.add_argument("--category", type=str, default=None, help="Filter by category")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    entries = load_csv(LEDGER_DIR / "ALPHA_STAGING.csv")

    if args.category:
        entries = [e for e in entries if e.get("category") == args.category]

    logger.info(f"Analyzing {len(entries)} alpha entries")

    category_trends = detect_category_trends(entries, args.days)
    topics = extract_topics(entries)
    roi = detect_roi_trends(entries)
    sources = detect_source_trends(entries)
    emerging = detect_emerging_methods(entries)

    if args.output == "json":
        result = {
            "category_trends": category_trends,
            "hot_topics": dict(topics.most_common(20)),
            "roi_distribution": roi,
            "top_sources": sources,
            "emerging_methods": emerging,
        }
        print(json.dumps(result, indent=2))
    else:
        print_trend_report(category_trends, topics, roi, sources, emerging, args.days)


if __name__ == "__main__":
    main()
