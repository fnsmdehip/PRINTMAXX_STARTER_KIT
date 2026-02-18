#!/usr/bin/env python3
"""
Social Analytics Engine - Aggregate posting performance and content-to-engagement mapping.

Combines data from post_scheduler (content posted), social_metrics/collect_metrics
(follower growth), and LEDGER tracking to identify what content works and why.

Usage:
    python3 social_analytics.py overview          # Full analytics overview
    python3 social_analytics.py top-content       # Top performing content types
    python3 social_analytics.py platform-compare  # Compare platform performance
    python3 social_analytics.py niche-report      # Per-niche performance breakdown
    python3 social_analytics.py posting-cadence   # Analyze posting frequency vs growth
    python3 social_analytics.py recommendations   # AI-style recommendations
"""

import csv
import json
import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Any, Optional

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_DIR / "LEDGER"
AUTOMATIONS_DIR = PROJECT_DIR / "AUTOMATIONS"
POSTING_DIR = AUTOMATIONS_DIR / "content_posting"
SOCIAL_METRICS_CSV = LEDGER_DIR / "SOCIAL_METRICS.csv"
POSTING_QUEUE_CSV = POSTING_DIR / "posting_queue.csv"
CONTENT_STRUCTURES_CSV = LEDGER_DIR / "WINNING_CONTENT_STRUCTURES.csv"
QA_QUEUE_DIR = PROJECT_DIR / "OPS" / "CONTENT_QA_QUEUE"

# Niche definitions
NICHES = {
    "faith": {
        "accounts": ["@DailyGraceQuotes"],
        "platforms": ["x", "instagram", "tiktok"],
        "posting_goal_daily": 3,
    },
    "fitness": {
        "accounts": ["@5AMGainsClub"],
        "platforms": ["x", "instagram", "tiktok"],
        "posting_goal_daily": 3,
    },
    "ai": {
        "accounts": ["@TheStackReport"],
        "platforms": ["x", "instagram", "tiktok"],
        "posting_goal_daily": 3,
    },
}

PLATFORM_RPMS = {
    "x": {"rpm_low": 0.50, "rpm_high": 2.00, "note": "X Premium revenue share"},
    "tiktok": {"rpm_low": 0.01, "rpm_high": 0.50, "note": "TikTok Creativity Program"},
    "instagram": {"rpm_low": 0.50, "rpm_high": 3.00, "note": "Reels Play Bonus"},
    "facebook_reels": {"rpm_low": 4.00, "rpm_high": 5.00, "note": "FB Reels (highest RPM)"},
    "youtube_shorts": {"rpm_low": 0.05, "rpm_high": 0.25, "note": "YouTube Shorts"},
}


def load_csv_safe(filepath: Path) -> tuple:
    """Load a CSV file safely, returning headers and rows."""
    if not filepath.exists():
        return [], []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            rows = list(reader)
        return headers, rows
    except Exception:
        return [], []


def load_social_metrics() -> List[dict]:
    """Load social metrics history."""
    _, rows = load_csv_safe(SOCIAL_METRICS_CSV)
    return rows


def load_posting_queue() -> List[dict]:
    """Load posting queue data."""
    _, rows = load_csv_safe(POSTING_QUEUE_CSV)
    return rows


def load_qa_queue() -> List[dict]:
    """Load QA queue content files."""
    entries = []
    if not QA_QUEUE_DIR.exists():
        return entries
    for f in QA_QUEUE_DIR.glob("*.md"):
        entry = {
            "filename": f.name,
            "size_kb": f.stat().st_size / 1024,
            "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d"),
        }
        # Try to parse metadata from file
        try:
            content = f.read_text(encoding='utf-8', errors='replace')
            for line in content.split('\n')[:20]:
                line = line.strip()
                if line.startswith('platform:'):
                    entry['platform'] = line.split(':', 1)[1].strip()
                elif line.startswith('content_type:'):
                    entry['content_type'] = line.split(':', 1)[1].strip()
                elif line.startswith('status:'):
                    entry['status'] = line.split(':', 1)[1].strip()
        except Exception:
            pass
        entries.append(entry)
    return entries


def load_content_structures() -> List[dict]:
    """Load winning content structures."""
    _, rows = load_csv_safe(CONTENT_STRUCTURES_CSV)
    return rows


def count_generated_content() -> Dict[str, int]:
    """Count generated content files by type."""
    counts = defaultdict(int)
    content_dirs = [
        ("social_posts", PROJECT_DIR / "MONEY_METHODS" / "CONTENT_FARM" / "NICHE_ACCOUNTS" / "generated_content"),
        ("medium_articles", PROJECT_DIR / "CONTENT" / "medium_articles"),
        ("substack_posts", PROJECT_DIR / "CONTENT" / "substack_posts"),
        ("longtail_pages", PROJECT_DIR / "CONTENT" / "longtail_pages"),
        ("email_sequences", PROJECT_DIR / "CONTENT" / "email_sequences"),
        ("video_scripts", PROJECT_DIR / "MONEY_METHODS" / "AI_INFLUENCER" / "ugc_scripts"),
        ("newsletter", PROJECT_DIR / "MONEY_METHODS" / "NEWSLETTER" / "LAUNCH_ASSETS" / "generated"),
        ("gumroad_listings", PROJECT_DIR / "MONEY_METHODS" / "DIGITAL_PRODUCTS" / "listings"),
        ("reddit_posts", PROJECT_DIR / "CONTENT" / "reddit"),
        ("pinterest_pins", PROJECT_DIR / "CONTENT" / "pinterest_pins"),
    ]
    for name, path in content_dirs:
        if path.exists():
            counts[name] = sum(1 for f in path.glob("*.md"))
    return dict(counts)


def cmd_overview(args):
    """Full analytics overview."""
    print("\n" + "=" * 60)
    print("SOCIAL ANALYTICS OVERVIEW")
    print("=" * 60)

    # Content inventory
    content_counts = count_generated_content()
    total_content = sum(content_counts.values())
    print(f"\n--- Content Inventory ({total_content} total pieces) ---")
    for content_type, count in sorted(content_counts.items(), key=lambda x: -x[1]):
        print(f"  {content_type:<25} {count:>5}")

    # Posting queue status
    queue = load_posting_queue()
    if queue:
        print(f"\n--- Posting Queue ({len(queue)} entries) ---")
        status_counts = Counter(r.get('status', 'UNKNOWN') for r in queue)
        for status, count in status_counts.most_common():
            print(f"  {status:<20} {count:>5}")

        platform_counts = Counter(r.get('platform', 'UNKNOWN') for r in queue)
        print(f"\n  By platform:")
        for platform, count in platform_counts.most_common():
            print(f"    {platform:<18} {count:>5}")
    else:
        print(f"\n--- Posting Queue ---")
        print("  No posts scheduled yet. Run: python3 AUTOMATIONS/content_posting/post_scheduler.py")

    # QA queue status
    qa_entries = load_qa_queue()
    if qa_entries:
        print(f"\n--- QA Queue ({len(qa_entries)} items) ---")
        qa_statuses = Counter(e.get('status', 'UNKNOWN') for e in qa_entries)
        for status, count in qa_statuses.most_common():
            print(f"  {status:<20} {count:>5}")
    else:
        print(f"\n--- QA Queue ---")
        print("  No items in QA queue.")

    # Social metrics
    metrics = load_social_metrics()
    if metrics:
        print(f"\n--- Social Metrics ({len(metrics)} data points) ---")
        latest_by_account = {}
        for m in metrics:
            key = f"{m.get('handle', '')}_{m.get('platform', '')}"
            if key not in latest_by_account or m.get('date', '') > latest_by_account[key].get('date', ''):
                latest_by_account[key] = m

        total_followers = 0
        for key, m in sorted(latest_by_account.items()):
            followers = int(m.get('followers', 0)) if m.get('followers', '0').isdigit() else 0
            growth = m.get('growth_since_last', '0')
            total_followers += followers
            print(f"  {m.get('handle', '?'):<25} {m.get('platform', '?'):<12} "
                  f"{followers:>8} followers  ({growth:>+6})")

        print(f"\n  Total followers: {total_followers:,}")
    else:
        print(f"\n--- Social Metrics ---")
        print("  No metrics recorded yet. Run: python3 AUTOMATIONS/social_metrics/collect_metrics.py --manual")

    # Platform RPM comparison
    print(f"\n--- Platform Revenue Per 1K Views ---")
    for platform, data in sorted(PLATFORM_RPMS.items(), key=lambda x: -x[1]['rpm_high']):
        print(f"  {platform:<20} ${data['rpm_low']:.2f} - ${data['rpm_high']:.2f}  ({data['note']})")

    # Posting cadence check
    print(f"\n--- Posting Cadence (Goals) ---")
    for niche, config in NICHES.items():
        goal = config['posting_goal_daily']
        platforms = len(config['platforms'])
        daily_total = goal * platforms
        print(f"  {niche:<12} {goal}/day/platform x {platforms} platforms = {daily_total} posts/day")
    total_daily_goal = sum(n['posting_goal_daily'] * len(n['platforms']) for n in NICHES.values())
    print(f"  {'TOTAL':<12} {total_daily_goal} posts/day across all niches")

    # Recommendations
    print(f"\n--- Quick Recommendations ---")
    if not metrics:
        print("  1. Set up social accounts and start tracking metrics")
        print("     Run: python3 AUTOMATIONS/social_metrics/collect_metrics.py --manual")
    if not queue:
        print("  2. Generate posting queue from existing content")
        print("     Run: python3 AUTOMATIONS/content_posting/post_scheduler.py")
    if total_content < 50:
        print(f"  3. Generate more content ({total_content} pieces, target 100+)")
        print("     Run: python3 AUTOMATIONS/content_pipeline.py create --source 'topic' --category APP_FACTORY")
    if 'facebook_reels' not in [r.get('platform', '') for r in queue]:
        print("  4. PRIORITY: Cross-post to Facebook Reels ($4.40/1K = highest RPM)")
    print("")


def cmd_top_content(args):
    """Identify top performing content types."""
    print("\n" + "=" * 60)
    print("TOP CONTENT ANALYSIS")
    print("=" * 60)

    structures = load_content_structures()
    if structures:
        print(f"\n--- Winning Content Structures ({len(structures)} tracked) ---")
        # Sort by engagement if available
        for i, s in enumerate(structures[:20], 1):
            name = s.get('structure_name', s.get('name', 'Unknown'))
            platform = s.get('platform', 'multi')
            engagement = s.get('avg_engagement', s.get('engagement', 'N/A'))
            print(f"  {i:>3}. [{platform:<10}] {name[:50]:<50} eng: {engagement}")
    else:
        print("\n  No content structures tracked yet.")
        print("  Content structure data comes from LEDGER/WINNING_CONTENT_STRUCTURES.csv")

    # Content counts by type
    content_counts = count_generated_content()
    if content_counts:
        print(f"\n--- Content Production Volume ---")
        total = sum(content_counts.values())
        for ctype, count in sorted(content_counts.items(), key=lambda x: -x[1]):
            pct = (count / total * 100) if total > 0 else 0
            bar = "#" * int(pct / 2)
            print(f"  {ctype:<25} {count:>5} ({pct:>5.1f}%) {bar}")

    # Recommendations based on data
    print(f"\n--- Content Type Recommendations ---")
    print("  Based on platform RPM data:")
    print("  1. Facebook Reels - highest RPM ($4.40/1K). Repurpose ALL short-form here first.")
    print("  2. Instagram Reels - second highest RPM ($0.50-$3.00/1K).")
    print("  3. X/Twitter - engagement + follower growth + X Premium revenue.")
    print("  4. TikTok - volume play, low RPM but massive reach.")
    print("  5. YouTube Shorts - low RPM but compound effect with long-form channel.")
    print("")


def cmd_platform_compare(args):
    """Compare platform performance."""
    print("\n" + "=" * 60)
    print("PLATFORM COMPARISON")
    print("=" * 60)

    metrics = load_social_metrics()

    # Group by platform
    by_platform = defaultdict(list)
    for m in metrics:
        by_platform[m.get('platform', 'unknown')].append(m)

    if by_platform:
        print(f"\n--- Followers by Platform ---")
        platform_totals = {}
        for platform, entries in sorted(by_platform.items()):
            # Get latest per account
            latest = {}
            for e in entries:
                handle = e.get('handle', '')
                if handle not in latest or e.get('date', '') > latest[handle].get('date', ''):
                    latest[handle] = e

            total = sum(int(e.get('followers', 0)) for e in latest.values()
                        if e.get('followers', '0').isdigit())
            total_growth = sum(int(e.get('growth_since_last', 0)) for e in latest.values()
                               if e.get('growth_since_last', '0').lstrip('+-').isdigit())
            accounts = len(latest)
            platform_totals[platform] = total

            rpm = PLATFORM_RPMS.get(platform, {})
            rpm_str = f"${rpm.get('rpm_low', 0):.2f}-${rpm.get('rpm_high', 0):.2f}/1K" if rpm else "N/A"

            print(f"\n  {platform.upper()}")
            print(f"    Accounts: {accounts}")
            print(f"    Total followers: {total:,}")
            print(f"    Recent growth: {total_growth:+,}")
            print(f"    RPM range: {rpm_str}")

            for handle, e in sorted(latest.items()):
                followers = e.get('followers', '0')
                growth = e.get('growth_since_last', '0')
                print(f"      {handle:<25} {followers:>8} followers ({growth:>+6})")
    else:
        print("\n  No social metrics data available.")
        print("  Run: python3 AUTOMATIONS/social_metrics/collect_metrics.py --manual")

    # RPM comparison table
    print(f"\n--- Revenue Per 1K Views (Platform Ranking) ---")
    print(f"  {'Platform':<20} {'Low RPM':>10} {'High RPM':>10} {'Verdict':>15}")
    print(f"  {'-'*20} {'-'*10} {'-'*10} {'-'*15}")
    for platform, data in sorted(PLATFORM_RPMS.items(), key=lambda x: -x[1]['rpm_high']):
        verdict = "HIGHEST" if data['rpm_high'] >= 4 else "HIGH" if data['rpm_high'] >= 2 else "MEDIUM" if data['rpm_high'] >= 0.5 else "LOW"
        print(f"  {platform:<20} ${data['rpm_low']:>8.2f} ${data['rpm_high']:>8.2f} {verdict:>15}")

    print(f"\n  Action: Cross-post ALL content to Facebook Reels first (4-440x TikTok/YouTube Shorts)")
    print("")


def cmd_niche_report(args):
    """Per-niche performance breakdown."""
    print("\n" + "=" * 60)
    print("NICHE PERFORMANCE REPORT")
    print("=" * 60)

    metrics = load_social_metrics()
    queue = load_posting_queue()
    content_counts = count_generated_content()

    for niche, config in NICHES.items():
        print(f"\n{'=' * 40}")
        print(f"  NICHE: {niche.upper()}")
        print(f"{'=' * 40}")

        # Accounts
        accounts = config['accounts']
        print(f"\n  Accounts: {', '.join(accounts)}")
        print(f"  Platforms: {', '.join(config['platforms'])}")
        print(f"  Daily posting goal: {config['posting_goal_daily']}/platform")

        # Metrics for this niche
        niche_metrics = [m for m in metrics if m.get('niche', '').lower() == niche]
        if niche_metrics:
            latest = {}
            for m in niche_metrics:
                key = f"{m.get('handle', '')}_{m.get('platform', '')}"
                if key not in latest or m.get('date', '') > latest[key].get('date', ''):
                    latest[key] = m

            total_followers = sum(int(e.get('followers', 0)) for e in latest.values()
                                  if e.get('followers', '0').isdigit())
            print(f"\n  Total followers: {total_followers:,}")

            for key, m in sorted(latest.items()):
                print(f"    {m.get('handle', '?'):<20} {m.get('platform', '?'):<10} "
                      f"{m.get('followers', '0'):>8} followers")
        else:
            print(f"\n  No metrics recorded for this niche yet.")

        # Queued posts for this niche
        niche_queue = [q for q in queue if q.get('niche', '').lower() == niche]
        if niche_queue:
            print(f"\n  Queued posts: {len(niche_queue)}")
            by_status = Counter(q.get('status', 'UNKNOWN') for q in niche_queue)
            for status, count in by_status.most_common():
                print(f"    {status}: {count}")
        else:
            print(f"\n  No posts queued for this niche.")

    print("")


def cmd_posting_cadence(args):
    """Analyze posting frequency vs growth."""
    print("\n" + "=" * 60)
    print("POSTING CADENCE ANALYSIS")
    print("=" * 60)

    queue = load_posting_queue()
    metrics = load_social_metrics()

    if queue:
        # Posts by day of week
        print(f"\n--- Posts by Day of Week ---")
        by_day = Counter()
        for q in queue:
            scheduled = q.get('scheduled_time', q.get('date', ''))
            if scheduled:
                try:
                    dt = datetime.strptime(scheduled[:10], "%Y-%m-%d")
                    by_day[dt.strftime("%A")] += 1
                except ValueError:
                    pass

        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in days_order:
            count = by_day.get(day, 0)
            bar = "#" * min(count, 50)
            print(f"  {day:<12} {count:>5} {bar}")

        # Posts by platform
        print(f"\n--- Posts by Platform ---")
        by_platform = Counter(q.get('platform', 'unknown') for q in queue)
        for platform, count in by_platform.most_common():
            print(f"  {platform:<20} {count:>5}")

        # Posts by niche
        print(f"\n--- Posts by Niche ---")
        by_niche = Counter(q.get('niche', 'unknown') for q in queue)
        for niche, count in by_niche.most_common():
            print(f"  {niche:<20} {count:>5}")
    else:
        print("\n  No posting queue data available.")
        print("  Generate queue: python3 AUTOMATIONS/content_posting/post_scheduler.py")

    # Optimal posting times based on platform research
    print(f"\n--- Optimal Posting Times (Research-Based) ---")
    print(f"  {'Platform':<15} {'Best Times':>30} {'Best Days':>20}")
    print(f"  {'-'*15} {'-'*30} {'-'*20}")
    optimal_times = [
        ("X/Twitter", "8-9AM, 12-1PM, 5-6PM EST", "Tue, Wed, Thu"),
        ("Instagram", "11AM-1PM, 7-9PM EST", "Tue, Wed, Fri"),
        ("TikTok", "7-9AM, 12-3PM, 7-11PM EST", "Tue, Thu, Fri"),
        ("Facebook", "1-4PM EST", "Wed, Thu, Fri"),
        ("LinkedIn", "7-8AM, 12PM, 5-6PM EST", "Tue, Wed, Thu"),
    ]
    for platform, times, days in optimal_times:
        print(f"  {platform:<15} {times:>30} {days:>20}")

    print("")


def cmd_recommendations(args):
    """Generate actionable recommendations based on all available data."""
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS ENGINE")
    print("=" * 60)

    metrics = load_social_metrics()
    queue = load_posting_queue()
    content_counts = count_generated_content()
    total_content = sum(content_counts.values())

    recommendations = []
    priority = 0

    # Check if we have metrics
    if not metrics:
        priority += 1
        recommendations.append({
            "priority": priority,
            "category": "TRACKING",
            "action": "Start tracking social metrics immediately",
            "command": "python3 AUTOMATIONS/social_metrics/collect_metrics.py --manual",
            "impact": "Cannot optimize what you cannot measure",
        })

    # Check content volume
    if total_content < 50:
        priority += 1
        recommendations.append({
            "priority": priority,
            "category": "CONTENT",
            "action": f"Generate more content ({total_content} pieces, target 100+)",
            "command": "python3 AUTOMATIONS/content_pipeline.py create --source 'topic' --category APP_FACTORY",
            "impact": "More content = more posting slots = more reach",
        })

    # Check posting queue
    if not queue:
        priority += 1
        recommendations.append({
            "priority": priority,
            "category": "DISTRIBUTION",
            "action": "Create posting queue from existing content",
            "command": "python3 AUTOMATIONS/content_posting/post_scheduler.py",
            "impact": "Content without distribution is wasted effort",
        })

    # Facebook Reels arbitrage
    priority += 1
    recommendations.append({
        "priority": priority,
        "category": "PLATFORM_ARBITRAGE",
        "action": "Cross-post ALL short-form to Facebook Reels",
        "command": "Repurpose TikTok/Reels content to FB Reels",
        "impact": "FB Reels pays $4.40/1K views (4-440x TikTok/YouTube Shorts)",
    })

    # Content type diversity
    if content_counts:
        if content_counts.get('social_posts', 0) > total_content * 0.7:
            priority += 1
            recommendations.append({
                "priority": priority,
                "category": "DIVERSIFICATION",
                "action": "Diversify content types (too many social posts)",
                "command": "Create medium articles, newsletters, video scripts",
                "impact": "Different formats reach different audiences",
            })

    # Engagement optimization
    priority += 1
    recommendations.append({
        "priority": priority,
        "category": "ENGAGEMENT",
        "action": "Use reply-bait format for all social posts",
        "command": "See OPS/growth/ENGAGEMENT_FARMING_TACTICS.md",
        "impact": "Replies boost algorithmic reach 10x vs likes alone",
    })

    # Revenue optimization
    priority += 1
    recommendations.append({
        "priority": priority,
        "category": "REVENUE",
        "action": "Add product CTAs to top-performing content",
        "command": "Update posts with Gumroad/app links as self-replies",
        "impact": "Convert engagement into revenue (currently 0 monetization)",
    })

    # Print recommendations
    for rec in sorted(recommendations, key=lambda x: x['priority']):
        print(f"\n  [{rec['priority']}] {rec['category']}: {rec['action']}")
        print(f"      Command: {rec['command']}")
        print(f"      Impact: {rec['impact']}")

    print(f"\n  Total recommendations: {len(recommendations)}")
    print("")


def main():
    parser = argparse.ArgumentParser(
        description='Social Analytics Engine - Content performance and optimization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s overview            Full analytics dashboard
  %(prog)s top-content         Best performing content types
  %(prog)s platform-compare    RPM and growth comparison across platforms
  %(prog)s niche-report        Per-niche breakdown (faith/fitness/ai)
  %(prog)s posting-cadence     Posting frequency analysis
  %(prog)s recommendations     Actionable optimization recommendations
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    sub_overview = subparsers.add_parser('overview', help='Full analytics overview')
    sub_overview.set_defaults(func=cmd_overview)

    sub_top = subparsers.add_parser('top-content', help='Top performing content types')
    sub_top.set_defaults(func=cmd_top_content)

    sub_platform = subparsers.add_parser('platform-compare', help='Compare platform performance')
    sub_platform.set_defaults(func=cmd_platform_compare)

    sub_niche = subparsers.add_parser('niche-report', help='Per-niche performance breakdown')
    sub_niche.set_defaults(func=cmd_niche_report)

    sub_cadence = subparsers.add_parser('posting-cadence', help='Posting frequency analysis')
    sub_cadence.set_defaults(func=cmd_posting_cadence)

    sub_recs = subparsers.add_parser('recommendations', help='Actionable recommendations')
    sub_recs.set_defaults(func=cmd_recommendations)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
