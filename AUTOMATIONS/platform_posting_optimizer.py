#!/usr/bin/env python3
"""
Platform-Specific Posting Schedule Optimizer
Sources:
  ALPHA263 - TikTok algo: completion rate threshold + follower-first testing
  ALPHA264 - First hour determines TikTok distribution
  ALPHA265 - Systems vs outcomes messaging trend
  ALPHA266 - YouTube Shorts: search SEO now matters + 50-60 sec sweet spot
  ALPHA267 - 18-22 Shorts/month optimal + trending audio first 5 sec
  ALPHA268 - IG: DM shares = new priority metric + first 2 seconds critical
  ALPHA269 - IG Originality Score penalty + remove TikTok watermarks + 3-5/week
  ALPHA273 - TikTok search: text overlays boost discoverability

Generates platform-optimized posting schedules with 2026 algorithm specifications.

Usage:
    python3 platform_posting_optimizer.py                   # Show all schedules
    python3 platform_posting_optimizer.py --platform tiktok  # TikTok only
    python3 platform_posting_optimizer.py --export-csv       # Export calendar
"""

import argparse
import csv
import json
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUTPUT_CSV = BASE_DIR / "LEDGER" / "POSTING_SCHEDULE_2026.csv"
REPORT_FILE = BASE_DIR / "OPS" / "POSTING_SCHEDULE_REPORT.md"

# Platform specifications (compiled from all alpha)
PLATFORM_SPECS = {
    "tiktok": {
        "name": "TikTok",
        "algo_signals_2026": [
            "Completion rate threshold INCREASED (watch full video)",
            "Follower-first testing (shows to followers before FYP)",
            "First hour determines distribution fate",
            "Text overlays boost search discoverability",
            "Active creator signal = new ranking factor",
            "Tutorials/how-to content winning",
            "Systems vs outcomes messaging resonating",
        ],
        "optimal_frequency": "1-3 per day",
        "optimal_length": "30-60 seconds (completion rate > length)",
        "best_times_utc": ["13:00", "17:00", "21:00"],
        "best_days": ["Tuesday", "Thursday", "Saturday"],
        "content_rules": [
            "Hook in first 1.5 seconds (text overlay + visual)",
            "Use trending audio in first 5 seconds",
            "Text overlays throughout for search SEO",
            "End with loop or strong CTA",
            "Post during active hours (triggers creator signal)",
            "Include searchable keywords in caption",
            "DO NOT cross-post with watermarks from other platforms",
        ],
        "monthly_target": 30,
        "weekly_target": 7,
    },
    "youtube_shorts": {
        "name": "YouTube Shorts",
        "algo_signals_2026": [
            "Search SEO now affects Shorts discoverability (NEW)",
            "50-60 second sweet spot for engagement",
            "18-22 Shorts per month = top creator benchmark",
            "Trending audio in first 5 seconds helps",
            "Titles and descriptions now indexed for search",
        ],
        "optimal_frequency": "5 per week (18-22 per month)",
        "optimal_length": "50-60 seconds",
        "best_times_utc": ["14:00", "18:00"],
        "best_days": ["Monday", "Wednesday", "Friday", "Saturday"],
        "content_rules": [
            "50-60 seconds (not shorter, not longer)",
            "Strong hook in first 2 seconds",
            "Include searchable title (SEO matters now)",
            "Description with keywords (gets indexed)",
            "Trending audio in opening 5 seconds",
            "Vertical format (9:16)",
            "Add end screen CTA to subscribe",
        ],
        "monthly_target": 20,
        "weekly_target": 5,
    },
    "instagram_reels": {
        "name": "Instagram Reels",
        "algo_signals_2026": [
            "DM shares = new PRIORITY metric (higher than likes)",
            "First 2 seconds critical for retention",
            "Originality Score penalty for cross-posted content",
            "Remove TikTok watermarks or get penalized",
            "Watch time still #1 overall signal",
            "3-5 posts per week optimal",
        ],
        "optimal_frequency": "3-5 per week",
        "optimal_length": "15-30 seconds (shareable > long)",
        "best_times_utc": ["11:00", "14:00", "19:00"],
        "best_days": ["Monday", "Wednesday", "Friday"],
        "content_rules": [
            "First 2 seconds MUST hook (text + visual)",
            "Optimize for DM shareability (relatable > informational)",
            "NEVER use TikTok watermark",
            "Original audio or trending IG audio (not TikTok audio)",
            "Short and shareable > long and educational",
            "Use Collab feature for reach",
            "Carousel posts still outperform for saves",
        ],
        "monthly_target": 16,
        "weekly_target": 4,
    },
    "twitter_x": {
        "name": "Twitter/X",
        "algo_signals_2026": [
            "Self-reply gets shown first by algorithm (ALPHA334)",
            "Comments/replies > likes for distribution",
            "Thread format still effective for authority",
            "Images increase engagement 2-3x",
            "Posting during peak hours matters more than ever",
        ],
        "optimal_frequency": "3-5 per day",
        "optimal_length": "Under 200 chars for tweets, 5-7 for threads",
        "best_times_utc": ["13:00", "16:00", "20:00", "23:00"],
        "best_days": ["Monday", "Tuesday", "Wednesday", "Thursday"],
        "content_rules": [
            "Consequence-first hooks (not explanations)",
            "Self-reply with value for 3-5x CTR",
            "Engage in replies for 30 min after posting",
            "Use specific numbers not vague claims",
            "No em dashes, no AI language",
            "Lowercase casual > polished professional",
            "Ask questions to drive comments",
        ],
        "monthly_target": 90,
        "weekly_target": 21,
    },
    "linkedin": {
        "name": "LinkedIn",
        "algo_signals_2026": [
            "Dwell time (time spent reading) is primary signal",
            "Comments weight more than reactions",
            "Native document posts get highest reach",
            "Consistency matters more than virality",
        ],
        "optimal_frequency": "3-5 per week",
        "optimal_length": "1200-1500 chars (readable in feed)",
        "best_times_utc": ["12:00", "14:00"],
        "best_days": ["Tuesday", "Wednesday", "Thursday"],
        "content_rules": [
            "Hook line then line break then story",
            "Personal stories > generic advice",
            "End with a question for comments",
            "Native documents/carousels for reach",
            "No external links in post (put in comments)",
            "Consistent posting schedule",
        ],
        "monthly_target": 16,
        "weekly_target": 4,
    },
}

# Weekly content mix by platform
CONTENT_MIX = {
    "twitter_x": {
        "value_posts": 10,  # Insights, numbers, frameworks
        "engagement_posts": 5,  # Questions, hot takes
        "threads": 3,  # Deep dives
        "personal_updates": 3,  # Building in public
    },
    "tiktok": {
        "tutorials": 3,  # How-to content (winning format)
        "trends": 2,  # Trending format/sound participation
        "storytelling": 2,  # Personal stories, results
    },
    "youtube_shorts": {
        "tutorials": 2,
        "quick_tips": 2,
        "behind_scenes": 1,
    },
    "instagram_reels": {
        "shareable_relatable": 2,  # DM share optimization
        "carousels": 1,
        "reels": 1,
    },
    "linkedin": {
        "insight_posts": 2,
        "story_posts": 1,
        "document_posts": 1,
    },
}


def generate_weekly_schedule():
    """Generate a weekly posting schedule across all platforms."""
    schedule = []
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())

    for day_offset in range(7):
        date = start_of_week + timedelta(days=day_offset)
        day_name = date.strftime("%A")

        for platform, specs in PLATFORM_SPECS.items():
            if day_name in specs["best_days"]:
                for time_str in specs["best_times_utc"][:2]:  # Max 2 posts per time
                    schedule.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "day": day_name,
                        "platform": platform,
                        "time_utc": time_str,
                        "content_type": "TBD",
                        "length": specs["optimal_length"],
                        "notes": specs["content_rules"][0],
                    })

    return schedule


def generate_30_day_calendar():
    """Generate a 30-day content calendar."""
    calendar = []
    today = datetime.now()

    for day in range(30):
        date = today + timedelta(days=day)
        day_name = date.strftime("%A")

        for platform, specs in PLATFORM_SPECS.items():
            # Calculate daily posts
            daily_target = specs["weekly_target"] / 7

            # Post on best days for this platform
            if day_name in specs["best_days"]:
                posts_today = max(1, round(daily_target * 1.5))
            else:
                posts_today = max(0, round(daily_target * 0.5))

            for post_num in range(min(posts_today, len(specs["best_times_utc"]))):
                time_slot = specs["best_times_utc"][post_num % len(specs["best_times_utc"])]

                # Determine content type from mix
                mix = CONTENT_MIX.get(platform, {})
                mix_types = list(mix.keys())
                content_type = mix_types[day % len(mix_types)] if mix_types else "value_post"

                calendar.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "day": day_name,
                    "platform": specs["name"],
                    "time_utc": time_slot,
                    "content_type": content_type,
                    "length": specs["optimal_length"],
                    "key_rule": specs["content_rules"][post_num % len(specs["content_rules"])],
                    "status": "PENDING",
                })

    return calendar


def print_platform_report(platform=None):
    """Print detailed platform report."""
    platforms = {platform: PLATFORM_SPECS[platform]} if platform and platform in PLATFORM_SPECS else PLATFORM_SPECS

    print(f"\n{'='*70}")
    print("PLATFORM POSTING OPTIMIZER - 2026 Algorithm Intelligence")
    print(f"{'='*70}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Sources: ALPHA263-269, ALPHA273, ALPHA334")

    for name, specs in platforms.items():
        print(f"\n{'='*70}")
        print(f" {specs['name'].upper()}")
        print(f"{'='*70}")

        print(f"\n  Frequency: {specs['optimal_frequency']}")
        print(f"  Length: {specs['optimal_length']}")
        print(f"  Best days: {', '.join(specs['best_days'])}")
        print(f"  Best times (UTC): {', '.join(specs['best_times_utc'])}")
        print(f"  Monthly target: {specs['monthly_target']} posts")
        print(f"  Weekly target: {specs['weekly_target']} posts")

        print(f"\n  2026 Algorithm Signals:")
        for signal in specs['algo_signals_2026']:
            print(f"    - {signal}")

        print(f"\n  Content Rules:")
        for rule in specs['content_rules']:
            print(f"    - {rule}")

        if name in CONTENT_MIX:
            print(f"\n  Weekly Content Mix:")
            for ctype, count in CONTENT_MIX[name].items():
                print(f"    - {ctype.replace('_', ' ').title()}: {count}/week")

    # Total monthly content needed
    print(f"\n{'='*70}")
    print("MONTHLY TOTALS")
    print(f"{'='*70}")
    total = 0
    for name, specs in PLATFORM_SPECS.items():
        print(f"  {specs['name']}: {specs['monthly_target']} posts")
        total += specs['monthly_target']
    print(f"  TOTAL: {total} posts/month ({total // 30} per day)")
    print(f"{'='*70}\n")


def export_calendar_csv():
    """Export 30-day calendar as CSV."""
    calendar = generate_30_day_calendar()

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["date", "day", "platform", "time_utc", "content_type", "length", "key_rule", "status"])
        writer.writeheader()
        writer.writerows(calendar)

    print(f"\n30-day calendar exported to: {OUTPUT_CSV}")
    print(f"Total posts scheduled: {len(calendar)}")

    # Stats
    by_platform = {}
    for entry in calendar:
        p = entry["platform"]
        by_platform[p] = by_platform.get(p, 0) + 1

    print(f"\nBy platform:")
    for p, count in sorted(by_platform.items()):
        print(f"  {p}: {count} posts")

    return calendar


def main():
    parser = argparse.ArgumentParser(description="Platform Posting Schedule Optimizer")
    parser.add_argument("--platform", type=str, help="Platform: tiktok, youtube_shorts, instagram_reels, twitter_x, linkedin")
    parser.add_argument("--export-csv", action="store_true", help="Export 30-day calendar as CSV")
    parser.add_argument("--weekly", action="store_true", help="Show weekly schedule only")
    args = parser.parse_args()

    if args.export_csv:
        export_calendar_csv()
    elif args.weekly:
        schedule = generate_weekly_schedule()
        print(f"\nWeekly schedule: {len(schedule)} posts")
        for s in schedule:
            print(f"  {s['day']} {s['time_utc']} - {s['platform']}")
    else:
        print_platform_report(args.platform)
        if not args.platform:
            export_calendar_csv()


if __name__ == "__main__":
    main()
