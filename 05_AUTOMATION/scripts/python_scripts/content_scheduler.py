#!/usr/bin/env python3
"""
Content Scheduler - Schedule content across platforms via Buffer, native APIs, or CSV queue
Reads from CONTENT_PIPELINE.csv, schedules approved posts

Usage:
    python content_scheduler.py                              # Schedule all approved posts
    python content_scheduler.py --platform x                 # Only X/Twitter posts
    python content_scheduler.py --platform linkedin          # Only LinkedIn posts
    python content_scheduler.py --dry-run                    # Preview without posting
    python content_scheduler.py --queue-only                 # Add to queue CSV, don't post
    python content_scheduler.py --from-csv content.csv       # Schedule from custom CSV

Environment Variables:
    BUFFER_ACCESS_TOKEN: Buffer API token (optional)
    TWITTER_BEARER_TOKEN: Twitter/X API token (optional)
    LINKEDIN_ACCESS_TOKEN: LinkedIn API token (optional)
    LEDGER_DIR: Path to LEDGER directory (default: ../LEDGER)

Output:
    Updates CONTENT_PIPELINE.csv with scheduled status
    Creates SCHEDULED_QUEUE.csv if --queue-only
"""

import argparse
import csv
import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    exit(1)


# Paths
BASE_DIR = Path(__file__).parent.parent.parent
LEDGER_DIR = Path(os.getenv("LEDGER_DIR", BASE_DIR / "LEDGER"))
CONTENT_PIPELINE_CSV = LEDGER_DIR / "CONTENT_PIPELINE.csv"
SCHEDULED_QUEUE_CSV = LEDGER_DIR / "SCHEDULED_QUEUE.csv"

# Timezone for scheduling
TIMEZONE = ZoneInfo("America/New_York")

# Optimal posting times by platform (hour in local time)
OPTIMAL_TIMES = {
    "x": [7, 9, 12, 15, 18, 21],      # Twitter/X optimal hours
    "linkedin": [7, 8, 12, 17, 18],    # LinkedIn optimal hours
    "reddit": [9, 12, 15, 18],         # Reddit optimal hours
}

# Buffer API endpoints
BUFFER_API_BASE = "https://api.bufferapp.com/1"


class BufferScheduler:
    """Schedule posts via Buffer API"""

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.profiles = {}
        self._load_profiles()

    def _load_profiles(self):
        """Load Buffer profiles"""
        try:
            response = requests.get(
                f"{BUFFER_API_BASE}/profiles.json",
                params={"access_token": self.access_token},
                timeout=30
            )
            if response.status_code == 200:
                for profile in response.json():
                    service = profile.get("service", "").lower()
                    self.profiles[service] = profile.get("id")
        except Exception as e:
            print(f"Error loading Buffer profiles: {e}")

    def schedule_post(
        self,
        text: str,
        platform: str,
        scheduled_at: Optional[datetime] = None
    ) -> tuple[bool, str]:
        """Schedule a post via Buffer"""
        profile_id = self.profiles.get(platform)
        if not profile_id:
            return False, f"No Buffer profile for {platform}"

        payload = {
            "text": text,
            "profile_ids[]": profile_id,
            "access_token": self.access_token
        }

        if scheduled_at:
            payload["scheduled_at"] = scheduled_at.isoformat()

        try:
            response = requests.post(
                f"{BUFFER_API_BASE}/updates/create.json",
                data=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return True, data.get("update", {}).get("id", "scheduled")
            else:
                return False, f"Buffer error: {response.text}"

        except Exception as e:
            return False, f"Request error: {e}"


class TwitterScheduler:
    """Schedule posts via Twitter/X API v2"""

    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token

    def post_tweet(self, text: str) -> tuple[bool, str]:
        """Post a tweet (immediate, X doesn't support scheduling via API)"""
        try:
            response = requests.post(
                "https://api.twitter.com/2/tweets",
                headers={
                    "Authorization": f"Bearer {self.bearer_token}",
                    "Content-Type": "application/json"
                },
                json={"text": text},
                timeout=30
            )

            if response.status_code == 201:
                data = response.json()
                tweet_id = data.get("data", {}).get("id")
                return True, f"https://x.com/i/status/{tweet_id}"
            else:
                return False, f"Twitter error: {response.text}"

        except Exception as e:
            return False, f"Request error: {e}"


class LinkedInScheduler:
    """Schedule posts via LinkedIn API"""

    def __init__(self, access_token: str, person_id: str):
        self.access_token = access_token
        self.person_id = person_id

    def post_update(self, text: str) -> tuple[bool, str]:
        """Post a LinkedIn update"""
        try:
            payload = {
                "author": f"urn:li:person:{self.person_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": text},
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            response = requests.post(
                "https://api.linkedin.com/v2/ugcPosts",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                    "X-Restli-Protocol-Version": "2.0.0"
                },
                json=payload,
                timeout=30
            )

            if response.status_code == 201:
                return True, "Posted to LinkedIn"
            else:
                return False, f"LinkedIn error: {response.text}"

        except Exception as e:
            return False, f"Request error: {e}"


def load_approved_content(
    csv_path: Path,
    platform_filter: Optional[str] = None
) -> list[dict]:
    """Load approved but not yet scheduled content"""
    content = []

    if not csv_path.exists():
        print(f"ERROR: {csv_path} not found")
        return content

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only APPROVED status
            if row.get("status", "").upper() != "APPROVED":
                continue

            # Already scheduled
            if row.get("scheduled_at"):
                continue

            # Platform filter
            if platform_filter:
                # Check if this platform's content exists
                platform_col = f"{platform_filter}_post"
                if platform_col not in row or not row.get(platform_col):
                    continue

            content.append(row)

    return content


def calculate_next_slot(
    platform: str,
    existing_slots: list[datetime]
) -> datetime:
    """Calculate next available posting slot"""
    now = datetime.now(TIMEZONE)

    # Get optimal hours for platform
    optimal_hours = OPTIMAL_TIMES.get(platform, [9, 12, 18])

    # Start from tomorrow to ensure enough lead time
    check_date = now + timedelta(days=1)

    for day_offset in range(14):  # Look up to 2 weeks ahead
        check_day = check_date + timedelta(days=day_offset)

        for hour in optimal_hours:
            slot = check_day.replace(
                hour=hour,
                minute=random.randint(0, 30),  # Add some randomness
                second=0,
                microsecond=0
            )

            # Check if slot is free
            slot_taken = any(
                abs((slot - existing).total_seconds()) < 3600  # Within 1 hour
                for existing in existing_slots
            )

            if not slot_taken:
                return slot

    # Fallback: just use tomorrow at 9am
    return (now + timedelta(days=1)).replace(hour=9, minute=0, second=0)


def update_csv_status(
    csv_path: Path,
    source_url: str,
    status: str,
    scheduled_at: Optional[datetime] = None,
    post_url: Optional[str] = None
):
    """Update content status in CSV"""
    rows = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)

        # Add new columns if needed
        if "scheduled_at" not in fieldnames:
            fieldnames.append("scheduled_at")
        if "post_url" not in fieldnames:
            fieldnames.append("post_url")

        for row in reader:
            if row.get("source_url") == source_url:
                row["status"] = status
                if scheduled_at:
                    row["scheduled_at"] = scheduled_at.isoformat()
                if post_url:
                    row["post_url"] = post_url
            rows.append(row)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def add_to_queue(
    queue_path: Path,
    content: dict,
    platform: str,
    scheduled_at: datetime
):
    """Add to local queue CSV"""
    fieldnames = [
        "queue_id", "platform", "content", "scheduled_at",
        "source_url", "status", "created_at"
    ]

    file_exists = queue_path.exists()

    with open(queue_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "queue_id": f"Q_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(100,999)}",
            "platform": platform,
            "content": content.get(f"{platform}_post", ""),
            "scheduled_at": scheduled_at.isoformat(),
            "source_url": content.get("source_url", ""),
            "status": "QUEUED",
            "created_at": datetime.now().isoformat()
        })


def schedule_content(
    content: list[dict],
    platforms: list[str],
    buffer_token: Optional[str] = None,
    twitter_token: Optional[str] = None,
    linkedin_token: Optional[str] = None,
    linkedin_person_id: Optional[str] = None,
    dry_run: bool = False,
    queue_only: bool = False
) -> dict:
    """Schedule all approved content"""
    results = {
        "scheduled": 0,
        "failed": 0,
        "skipped": 0,
        "errors": []
    }

    # Initialize schedulers
    buffer = BufferScheduler(buffer_token) if buffer_token else None
    twitter = TwitterScheduler(twitter_token) if twitter_token else None
    linkedin = LinkedInScheduler(linkedin_token, linkedin_person_id) if linkedin_token and linkedin_person_id else None

    # Track scheduled slots per platform
    scheduled_slots = {p: [] for p in platforms}

    for item in content:
        source_url = item.get("source_url", "unknown")
        print(f"\nProcessing: {item.get('source_title', source_url)[:50]}...")

        for platform in platforms:
            post_col = f"{platform}_post"
            post_text = item.get(post_col, "").strip()

            if not post_text:
                print(f"  {platform}: No content, skipping")
                continue

            # Calculate slot
            slot = calculate_next_slot(platform, scheduled_slots[platform])
            scheduled_slots[platform].append(slot)

            print(f"  {platform}: Scheduling for {slot.strftime('%Y-%m-%d %H:%M')}")

            if dry_run:
                print(f"    [DRY RUN] Would schedule: {post_text[:50]}...")
                results["scheduled"] += 1
                continue

            if queue_only:
                add_to_queue(SCHEDULED_QUEUE_CSV, item, platform, slot)
                print(f"    Added to queue")
                results["scheduled"] += 1
                continue

            # Try to schedule via available method
            success = False
            post_url = None

            # Try Buffer first (supports scheduling)
            if buffer and platform in buffer.profiles:
                success, result = buffer.schedule_post(post_text, platform, slot)
                if success:
                    post_url = result
                    print(f"    Scheduled via Buffer: {result}")
                else:
                    print(f"    Buffer failed: {result}")

            # Fallback to native APIs (usually immediate post)
            elif platform == "x" and twitter:
                success, result = twitter.post_tweet(post_text)
                if success:
                    post_url = result
                    print(f"    Posted to X: {result}")
                else:
                    print(f"    X failed: {result}")

            elif platform == "linkedin" and linkedin:
                success, result = linkedin.post_update(post_text)
                if success:
                    print(f"    Posted to LinkedIn")
                else:
                    print(f"    LinkedIn failed: {result}")

            else:
                # No scheduler available, add to queue
                add_to_queue(SCHEDULED_QUEUE_CSV, item, platform, slot)
                print(f"    No API available, added to queue")
                results["scheduled"] += 1
                continue

            if success:
                results["scheduled"] += 1
                update_csv_status(
                    CONTENT_PIPELINE_CSV,
                    source_url,
                    "SCHEDULED",
                    slot,
                    post_url
                )
            else:
                results["failed"] += 1
                results["errors"].append(f"{platform}: {result}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Schedule content across platforms"
    )
    parser.add_argument(
        "--platform",
        choices=["x", "linkedin", "reddit"],
        help="Filter to specific platform"
    )
    parser.add_argument(
        "--from-csv",
        type=Path,
        help="Use custom CSV file instead of CONTENT_PIPELINE.csv"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview scheduling without posting"
    )
    parser.add_argument(
        "--queue-only",
        action="store_true",
        help="Add to queue CSV without posting"
    )
    parser.add_argument(
        "--platforms",
        nargs="+",
        default=["x", "linkedin"],
        help="Platforms to schedule for (default: x linkedin)"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("CONTENT SCHEDULER")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Load environment variables
    buffer_token = os.getenv("BUFFER_ACCESS_TOKEN")
    twitter_token = os.getenv("TWITTER_BEARER_TOKEN")
    linkedin_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    linkedin_person_id = os.getenv("LINKEDIN_PERSON_ID")

    # Determine which platforms we can actually schedule to
    available = []
    if buffer_token:
        available.append("Buffer (all platforms)")
    if twitter_token:
        available.append("X/Twitter (native)")
    if linkedin_token and linkedin_person_id:
        available.append("LinkedIn (native)")

    if available:
        print(f"\nAvailable schedulers: {', '.join(available)}")
    else:
        print("\nNo API tokens found. Will add to queue for manual posting.")
        args.queue_only = True

    # Load content
    csv_path = args.from_csv or CONTENT_PIPELINE_CSV
    platform_filter = args.platform

    content = load_approved_content(csv_path, platform_filter)

    if not content:
        print("\nNo approved content found to schedule")
        return

    print(f"\nContent to schedule: {len(content)} items")
    print(f"Platforms: {', '.join(args.platforms)}")

    if args.dry_run:
        print("\n[DRY RUN MODE]")
    if args.queue_only:
        print("\n[QUEUE ONLY MODE]")

    # Schedule content
    results = schedule_content(
        content=content,
        platforms=args.platforms if not platform_filter else [platform_filter],
        buffer_token=buffer_token,
        twitter_token=twitter_token,
        linkedin_token=linkedin_token,
        linkedin_person_id=linkedin_person_id,
        dry_run=args.dry_run,
        queue_only=args.queue_only
    )

    # Print summary
    print(f"\n{'=' * 60}")
    print("SCHEDULING SUMMARY")
    print("=" * 60)
    print(f"Scheduled: {results['scheduled']}")
    print(f"Failed: {results['failed']}")
    print(f"Skipped: {results['skipped']}")

    if results["errors"]:
        print("\nErrors:")
        for error in results["errors"][:5]:
            print(f"  - {error}")

    if args.queue_only or not (buffer_token or twitter_token or linkedin_token):
        print(f"\nQueue saved to: {SCHEDULED_QUEUE_CSV}")
        print("Use the queue CSV with Buffer dashboard or native schedulers")

    print(f"\n{'=' * 60}")
    print("COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
