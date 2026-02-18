#!/usr/bin/env python3
"""
post_scheduler.py - Auto-schedule content from CONTENT_CALENDAR CSV

Reads CONTENT_CALENDAR_2026.csv or CONTENT_PIPELINE.csv, picks pending posts,
generates optimal posting times per platform, and writes a scheduled posting
queue to content_posting/posting_queue.csv.

Usage:
    python3 post_scheduler.py --source calendar --days 7
    python3 post_scheduler.py --source pipeline --platform X --days 3
    python3 post_scheduler.py --dry-run --days 1

Example:
    # Schedule next 7 days from content calendar
    python3 post_scheduler.py --source calendar --days 7

    # Preview what would be scheduled without writing
    python3 post_scheduler.py --dry-run --days 3

    # Schedule only X/Twitter posts from pipeline
    python3 post_scheduler.py --source pipeline --platform X --days 7
"""

import argparse
import csv
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_DIR / "LEDGER"
AUTOMATIONS_DIR = PROJECT_DIR / "AUTOMATIONS"
POSTING_QUEUE = AUTOMATIONS_DIR / "content_posting" / "posting_queue.csv"
CONFIG_PATH = AUTOMATIONS_DIR / "config.json"
LOG_DIR = AUTOMATIONS_DIR / "logs"

# Ensure directories exist
LOG_DIR.mkdir(parents=True, exist_ok=True)
POSTING_QUEUE.parent.mkdir(parents=True, exist_ok=True)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "post_scheduler.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Optimal posting times per platform (UTC offsets from midnight)
# Based on engagement research from growth docs
DEFAULT_POSTING_TIMES = {
    "X": [8, 12, 17, 20],          # 8am, 12pm, 5pm, 8pm ET
    "Twitter": [8, 12, 17, 20],
    "TikTok": [7, 10, 14, 19],     # 7am, 10am, 2pm, 7pm ET
    "Instagram": [9, 12, 15, 19],   # 9am, 12pm, 3pm, 7pm ET
    "LinkedIn": [7, 10, 12, 17],    # 7am, 10am, 12pm, 5pm ET
    "YouTube": [9, 14, 17],         # 9am, 2pm, 5pm ET
    "Facebook": [9, 13, 16],        # 9am, 1pm, 4pm ET
    "Pinterest": [14, 20, 21],      # 2pm, 8pm, 9pm ET
    "Medium": [10, 14],             # 10am, 2pm ET
    "Substack": [10, 14],           # 10am, 2pm ET
}


def load_config():
    """Load config file if it exists."""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH) as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning("Config file malformed, using defaults")
    return {}


def load_content_calendar():
    """Load CONTENT_CALENDAR_2026.csv."""
    path = LEDGER_DIR / "CONTENT_CALENDAR_2026.csv"
    if not path.exists():
        logger.error(f"Content calendar not found: {path}")
        return []

    entries = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(row)
    logger.info(f"Loaded {len(entries)} entries from content calendar")
    return entries


def load_content_pipeline():
    """Load CONTENT_PIPELINE.csv."""
    path = LEDGER_DIR / "CONTENT_PIPELINE.csv"
    if not path.exists():
        logger.error(f"Content pipeline not found: {path}")
        return []

    entries = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(row)
    logger.info(f"Loaded {len(entries)} entries from content pipeline")
    return entries


def filter_pending(entries, source_type):
    """Filter for pending/queued entries."""
    pending = []
    status_field = "status" if source_type == "calendar" else "Status"
    for entry in entries:
        status = entry.get(status_field, "").lower().strip()
        if status in ("pending", "queued", "draft", "ready"):
            pending.append(entry)
    logger.info(f"Found {len(pending)} pending entries")
    return pending


def assign_schedule(entries, source_type, days, platform_filter=None):
    """Assign optimal posting times to entries."""
    config = load_config()
    posting_times = config.get("posting_times", DEFAULT_POSTING_TIMES)

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = today + timedelta(days=days)

    scheduled = []
    platform_counters = {}  # Track posts per platform per day

    for entry in entries:
        if source_type == "calendar":
            platform = entry.get("platform", "X")
            niche = entry.get("niche", "")
            content_type = entry.get("content_type", "post")
            content_path = entry.get("content_path", "")
            caption = entry.get("caption", "")
            account = entry.get("account", "")
        else:
            platform = entry.get("Platform", "X")
            niche = entry.get("Niche", "")
            content_type = entry.get("Type", "post")
            content_path = ""
            caption = entry.get("Title", "")
            account = ""

        # Apply platform filter
        if platform_filter and platform.lower() != platform_filter.lower():
            continue

        # Get available times for this platform
        times = posting_times.get(platform, [10, 14, 18])

        # Find next available slot
        day_key = f"{platform}_{niche}"
        if day_key not in platform_counters:
            platform_counters[day_key] = 0

        slot_index = platform_counters[day_key]
        day_offset = slot_index // len(times)
        time_index = slot_index % len(times)

        scheduled_date = today + timedelta(days=day_offset)
        if scheduled_date >= end_date:
            continue

        hour = times[time_index]
        scheduled_time = scheduled_date.replace(hour=hour, minute=0)

        scheduled.append({
            "scheduled_time": scheduled_time.strftime("%Y-%m-%d %H:%M"),
            "platform": platform,
            "account": account,
            "niche": niche,
            "content_type": content_type,
            "content_path": content_path,
            "caption": caption[:200] if caption else "",
            "hashtags": entry.get("hashtags", entry.get("Hashtags", "")),
            "status": "SCHEDULED",
            "source": source_type,
            "original_id": entry.get("ContentID", entry.get("date", "")),
        })

        platform_counters[day_key] = slot_index + 1

    logger.info(f"Scheduled {len(scheduled)} posts across {days} days")
    return scheduled


def write_posting_queue(scheduled, dry_run=False):
    """Write scheduled posts to posting_queue.csv."""
    if dry_run:
        logger.info("DRY RUN - Not writing to file")
        for post in scheduled:
            logger.info(
                f"  [{post['scheduled_time']}] {post['platform']} | "
                f"{post['niche']} | {post['caption'][:60]}..."
            )
        return

    fieldnames = [
        "scheduled_time", "platform", "account", "niche", "content_type",
        "content_path", "caption", "hashtags", "status", "source", "original_id",
    ]

    # Append to existing queue or create new
    file_exists = POSTING_QUEUE.exists()
    existing_times = set()

    if file_exists:
        with open(POSTING_QUEUE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_times.add(
                    f"{row.get('scheduled_time', '')}_{row.get('platform', '')}"
                )

    new_posts = []
    for post in scheduled:
        key = f"{post['scheduled_time']}_{post['platform']}"
        if key not in existing_times:
            new_posts.append(post)

    with open(POSTING_QUEUE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(new_posts)

    logger.info(f"Wrote {len(new_posts)} new posts to {POSTING_QUEUE}")
    logger.info(f"Skipped {len(scheduled) - len(new_posts)} duplicates")


def main():
    parser = argparse.ArgumentParser(
        description="Schedule content posts from LEDGER CSVs"
    )
    parser.add_argument(
        "--source",
        choices=["calendar", "pipeline"],
        default="calendar",
        help="Content source CSV (default: calendar)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days to schedule (default: 7)",
    )
    parser.add_argument(
        "--platform",
        type=str,
        default=None,
        help="Filter by platform (e.g., X, TikTok, Instagram)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview schedule without writing",
    )
    args = parser.parse_args()

    logger.info(f"Starting post scheduler: source={args.source}, days={args.days}")

    if args.source == "calendar":
        entries = load_content_calendar()
    else:
        entries = load_content_pipeline()

    if not entries:
        logger.error("No entries found. Exiting.")
        sys.exit(1)

    pending = filter_pending(entries, args.source)
    if not pending:
        logger.warning("No pending entries to schedule")
        sys.exit(0)

    scheduled = assign_schedule(pending, args.source, args.days, args.platform)
    write_posting_queue(scheduled, dry_run=args.dry_run)

    logger.info("Post scheduling complete")


if __name__ == "__main__":
    main()
