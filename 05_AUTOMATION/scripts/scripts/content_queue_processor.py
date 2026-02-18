#!/usr/bin/env python3
"""
Content Calendar Queue Processor
=================================
Processes scheduled content from CONTENT_CALENDAR_2026.csv.

Reads today's scheduled posts, loads content from markdown files,
and hands off to platform-specific posters.

Usage:
    python content_queue_processor.py --today
    python content_queue_processor.py --date 2026-01-25
    python content_queue_processor.py --dry-run
    python content_queue_processor.py --process
"""

import os
import sys
import csv
import json
import logging
import random
import time
from datetime import datetime, date
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging
LOG_DIR = Path(__file__).parent.parent.parent / "OPS" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "content_queue_processor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("content_queue_processor")


# Paths
BASE_DIR = Path(__file__).parent.parent.parent
LEDGER_DIR = BASE_DIR / "LEDGER"
CONTENT_DIR = BASE_DIR / "CONTENT"
CALENDAR_PATH = LEDGER_DIR / "CONTENT_CALENDAR_2026.csv"
PERFORMANCE_PATH = LEDGER_DIR / "CONTENT_PERFORMANCE_TRACKER.csv"


@dataclass
class CalendarEntry:
    """Represents a scheduled content calendar entry."""
    date: str
    platform: str
    account: str
    niche: str
    content_type: str
    content_path: str
    caption: str
    hashtags: str
    status: str
    posted_url: str
    notes: str

    @classmethod
    def from_csv_row(cls, row: Dict[str, str]) -> "CalendarEntry":
        """Create entry from CSV row."""
        return cls(
            date=row.get("date", ""),
            platform=row.get("platform", ""),
            account=row.get("account", ""),
            niche=row.get("niche", ""),
            content_type=row.get("content_type", ""),
            content_path=row.get("content_path", ""),
            caption=row.get("caption", ""),
            hashtags=row.get("hashtags", ""),
            status=row.get("status", "pending"),
            posted_url=row.get("posted_url", ""),
            notes=row.get("notes", "")
        )

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for CSV writing."""
        return {
            "date": self.date,
            "platform": self.platform,
            "account": self.account,
            "niche": self.niche,
            "content_type": self.content_type,
            "content_path": self.content_path,
            "caption": self.caption,
            "hashtags": self.hashtags,
            "status": self.status,
            "posted_url": self.posted_url,
            "notes": self.notes
        }


class ContentQueueProcessor:
    """Process content calendar and post to platforms."""

    def __init__(self, calendar_path: str = None):
        """Initialize the processor."""
        self.calendar_path = Path(calendar_path or CALENDAR_PATH)
        self.content_dir = CONTENT_DIR
        self.base_dir = BASE_DIR

        # Lazy load posters to avoid import errors if not installed
        self._x_poster = None
        self._ig_poster = None

        logger.info(f"Content queue processor initialized")
        logger.info(f"  Calendar: {self.calendar_path}")

    def load_calendar(self) -> List[CalendarEntry]:
        """Load all entries from calendar CSV."""
        entries = []

        if not self.calendar_path.exists():
            logger.error(f"Calendar not found: {self.calendar_path}")
            return entries

        try:
            with open(self.calendar_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    entry = CalendarEntry.from_csv_row(row)
                    entries.append(entry)

            logger.info(f"Loaded {len(entries)} calendar entries")

        except Exception as e:
            logger.error(f"Error loading calendar: {e}")

        return entries

    def get_entries_for_date(self, target_date: date) -> List[CalendarEntry]:
        """Get all entries scheduled for a specific date."""
        entries = self.load_calendar()
        target_str = target_date.strftime("%Y-%m-%d")

        scheduled = [e for e in entries if e.date == target_str and e.status == "pending"]
        logger.info(f"Found {len(scheduled)} pending entries for {target_str}")

        return scheduled

    def get_todays_entries(self) -> List[CalendarEntry]:
        """Get all entries scheduled for today."""
        return self.get_entries_for_date(date.today())

    def load_content_from_file(self, content_path: str) -> str:
        """
        Load content from a markdown file.

        Args:
            content_path: Relative path from project root (e.g., CONTENT/social/faith/devotional_01.md)

        Returns:
            Content text, stripped of headers and cleaned
        """
        full_path = self.base_dir / content_path

        if not full_path.exists():
            logger.warning(f"Content file not found: {full_path}")
            return ""

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            # Remove markdown header if present (# Title line)
            lines = content.split('\n')
            if lines and lines[0].startswith('# '):
                lines = lines[1:]

            # Clean up and join
            content = '\n'.join(line for line in lines if line.strip())

            return content.strip()

        except Exception as e:
            logger.error(f"Error reading content file {full_path}: {e}")
            return ""

    def prepare_post_content(self, entry: CalendarEntry) -> str:
        """
        Prepare the full post content from calendar entry.

        If caption is provided, use it. Otherwise load from content file.
        Appends hashtags if provided.
        """
        # Use caption if provided, otherwise load from file
        if entry.caption:
            content = entry.caption
        else:
            content = self.load_content_from_file(entry.content_path)

        if not content:
            logger.warning(f"No content for entry: {entry.content_path}")
            return ""

        # Add hashtags if not already in content
        if entry.hashtags and entry.hashtags not in content:
            content = f"{content}\n\n{entry.hashtags}"

        return content

    def get_poster_for_platform(self, platform: str, account: str):
        """Get the appropriate poster instance for a platform."""
        platform_lower = platform.lower()

        try:
            if platform_lower == "x":
                from x_poster import XPoster
                config = {
                    "account_id": account,
                    "headless": os.getenv("HEADLESS", "false").lower() == "true",
                    "session_path": str(BASE_DIR / "sessions" / f"{account.replace('@', '')}.json")
                }
                return XPoster(config)

            elif platform_lower == "instagram":
                from ig_poster import IGPoster
                config = {
                    "account_id": account,
                    "headless": os.getenv("HEADLESS", "false").lower() == "true",
                    "session_path": str(BASE_DIR / "sessions" / f"{account.replace('@', '')}.json")
                }
                return IGPoster(config)

            else:
                logger.warning(f"Platform not yet supported: {platform}")
                return None

        except ImportError as e:
            logger.error(f"Could not import poster for {platform}: {e}")
            return None

    def post_entry(self, entry: CalendarEntry, dry_run: bool = False) -> Dict[str, Any]:
        """
        Post a single calendar entry.

        Args:
            entry: The calendar entry to post
            dry_run: If True, don't actually post

        Returns:
            Result dictionary
        """
        result = {
            "date": entry.date,
            "platform": entry.platform,
            "account": entry.account,
            "content_type": entry.content_type,
            "success": False,
            "error": None,
            "posted_url": "",
            "timestamp": datetime.now().isoformat()
        }

        # Prepare content
        content = self.prepare_post_content(entry)
        if not content:
            result["error"] = "No content available"
            return result

        result["content_preview"] = content[:100] + "..." if len(content) > 100 else content

        if dry_run:
            logger.info(f"[DRY RUN] Would post to {entry.platform} via {entry.account}")
            logger.info(f"  Content: {content[:100]}...")
            result["success"] = True
            result["dry_run"] = True
            return result

        # Get poster
        poster = self.get_poster_for_platform(entry.platform, entry.account)
        if not poster:
            result["error"] = f"No poster available for {entry.platform}"
            return result

        # Post
        try:
            logger.info(f"Posting to {entry.platform} via {entry.account}...")
            post_result = poster.post(content)

            result["success"] = post_result.get("success", False)
            result["posted_url"] = post_result.get("url", "")

            if not result["success"]:
                result["error"] = post_result.get("error", "Unknown error")

        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Error posting: {e}")

        return result

    def update_calendar_status(
        self,
        entry: CalendarEntry,
        status: str,
        posted_url: str = ""
    ) -> None:
        """Update the status of a calendar entry."""
        if not self.calendar_path.exists():
            return

        try:
            # Read all entries
            entries = []
            fieldnames = None

            with open(self.calendar_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                for row in reader:
                    # Match entry by date, platform, account, content_path
                    if (row["date"] == entry.date and
                        row["platform"] == entry.platform and
                        row["account"] == entry.account and
                        row["content_path"] == entry.content_path):
                        row["status"] = status
                        if posted_url:
                            row["posted_url"] = posted_url
                    entries.append(row)

            # Write back
            with open(self.calendar_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(entries)

            logger.info(f"Updated calendar entry status to: {status}")

        except Exception as e:
            logger.error(f"Error updating calendar: {e}")

    def log_to_performance_tracker(self, result: Dict[str, Any]) -> None:
        """Log post result to performance tracker CSV."""
        tracker_path = PERFORMANCE_PATH

        write_header = not tracker_path.exists()

        try:
            with open(tracker_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if write_header:
                    writer.writerow([
                        "post_id", "platform", "account", "posted_at",
                        "impressions", "engagement", "clicks", "conversions", "notes"
                    ])

                post_id = f"{result['date']}_{result['platform']}_{result['account']}"
                writer.writerow([
                    post_id,
                    result["platform"],
                    result["account"],
                    result["timestamp"],
                    0,  # impressions - to be updated later
                    0,  # engagement
                    0,  # clicks
                    0,  # conversions
                    "Posted via automation" if result["success"] else result.get("error", "")
                ])

        except Exception as e:
            logger.error(f"Error logging to performance tracker: {e}")

    def process_entries(
        self,
        entries: List[CalendarEntry],
        dry_run: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Process a list of calendar entries.

        Args:
            entries: List of entries to process
            dry_run: If True, don't actually post

        Returns:
            List of results
        """
        results = []

        for i, entry in enumerate(entries):
            logger.info(f"Processing entry {i+1}/{len(entries)}: {entry.platform} - {entry.account}")

            result = self.post_entry(entry, dry_run=dry_run)
            results.append(result)

            if not dry_run:
                # Update calendar
                status = "posted" if result["success"] else "failed"
                self.update_calendar_status(entry, status, result.get("posted_url", ""))

                # Log to performance tracker
                self.log_to_performance_tracker(result)

                # Delay between posts (avoid rate limits)
                if i < len(entries) - 1:
                    delay = random.uniform(30, 120)  # 30 seconds to 2 minutes
                    logger.info(f"Waiting {delay:.0f} seconds before next post...")
                    time.sleep(delay)

        return results

    def process_today(self, dry_run: bool = False) -> List[Dict[str, Any]]:
        """Process all of today's scheduled posts."""
        entries = self.get_todays_entries()

        if not entries:
            logger.info("No pending entries for today")
            return []

        return self.process_entries(entries, dry_run=dry_run)

    def process_date(self, target_date: date, dry_run: bool = False) -> List[Dict[str, Any]]:
        """Process all posts scheduled for a specific date."""
        entries = self.get_entries_for_date(target_date)

        if not entries:
            logger.info(f"No pending entries for {target_date}")
            return []

        return self.process_entries(entries, dry_run=dry_run)

    def get_calendar_stats(self) -> Dict[str, Any]:
        """Get statistics about the content calendar."""
        entries = self.load_calendar()

        stats = {
            "total": len(entries),
            "by_status": {},
            "by_platform": {},
            "by_niche": {},
            "by_content_type": {},
            "upcoming_days": {}
        }

        today = date.today()

        for entry in entries:
            # By status
            stats["by_status"][entry.status] = stats["by_status"].get(entry.status, 0) + 1

            # By platform
            stats["by_platform"][entry.platform] = stats["by_platform"].get(entry.platform, 0) + 1

            # By niche
            stats["by_niche"][entry.niche] = stats["by_niche"].get(entry.niche, 0) + 1

            # By content type
            stats["by_content_type"][entry.content_type] = stats["by_content_type"].get(entry.content_type, 0) + 1

            # Upcoming by day (next 7 days)
            try:
                entry_date = datetime.strptime(entry.date, "%Y-%m-%d").date()
                days_until = (entry_date - today).days
                if 0 <= days_until <= 7 and entry.status == "pending":
                    stats["upcoming_days"][entry.date] = stats["upcoming_days"].get(entry.date, 0) + 1
            except ValueError:
                pass

        return stats


def print_results(results: List[Dict[str, Any]]) -> None:
    """Print processing results in a readable format."""
    print("\n" + "=" * 60)
    print("PROCESSING RESULTS")
    print("=" * 60)

    success_count = sum(1 for r in results if r.get("success"))
    fail_count = len(results) - success_count

    print(f"\nTotal: {len(results)} | Success: {success_count} | Failed: {fail_count}")
    print("-" * 60)

    for r in results:
        status = "OK" if r.get("success") else "FAIL"
        dry = " [DRY RUN]" if r.get("dry_run") else ""
        print(f"  [{status}]{dry} {r['platform']} via {r['account']}")
        if r.get("error"):
            print(f"         Error: {r['error']}")
        if r.get("content_preview"):
            preview = r["content_preview"][:60] + "..." if len(r.get("content_preview", "")) > 60 else r.get("content_preview", "")
            print(f"         Content: {preview}")

    print("=" * 60 + "\n")


# CLI
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process content calendar queue")
    parser.add_argument("--today", action="store_true", help="Process today's scheduled posts")
    parser.add_argument("--date", help="Process posts for specific date (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without posting")
    parser.add_argument("--process", action="store_true", help="Actually process and post")
    parser.add_argument("--stats", action="store_true", help="Show calendar statistics")
    parser.add_argument("--list", action="store_true", help="List upcoming posts")
    parser.add_argument("--calendar", help="Path to calendar CSV")

    args = parser.parse_args()

    # Initialize processor
    processor = ContentQueueProcessor(calendar_path=args.calendar)

    if args.stats:
        stats = processor.get_calendar_stats()
        print("\n" + "=" * 50)
        print("CONTENT CALENDAR STATISTICS")
        print("=" * 50)
        print(f"\nTotal entries: {stats['total']}")

        print("\nBy Status:")
        for status, count in sorted(stats["by_status"].items()):
            print(f"  {status}: {count}")

        print("\nBy Platform:")
        for platform, count in sorted(stats["by_platform"].items()):
            print(f"  {platform}: {count}")

        print("\nBy Niche:")
        for niche, count in sorted(stats["by_niche"].items()):
            print(f"  {niche}: {count}")

        print("\nBy Content Type:")
        for ctype, count in sorted(stats["by_content_type"].items()):
            print(f"  {ctype}: {count}")

        if stats["upcoming_days"]:
            print("\nUpcoming (next 7 days):")
            for day, count in sorted(stats["upcoming_days"].items()):
                print(f"  {day}: {count} posts")

        print("=" * 50 + "\n")

    elif args.list:
        entries = processor.get_todays_entries()
        print(f"\n Today's scheduled posts ({len(entries)}):")
        print("-" * 60)
        for e in entries:
            print(f"  {e.platform} | {e.account} | {e.content_type} | {e.niche}")
        print()

    elif args.today or args.process:
        dry_run = args.dry_run or not args.process
        results = processor.process_today(dry_run=dry_run)
        print_results(results)

    elif args.date:
        try:
            target = datetime.strptime(args.date, "%Y-%m-%d").date()
            dry_run = args.dry_run or not args.process
            results = processor.process_date(target, dry_run=dry_run)
            print_results(results)
        except ValueError:
            print(f"Invalid date format: {args.date}. Use YYYY-MM-DD")
            sys.exit(1)

    else:
        parser.print_help()
