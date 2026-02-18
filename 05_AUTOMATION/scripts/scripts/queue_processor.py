#!/usr/bin/env python3
"""
Content Queue Processor
=======================
Processes content queue from CSV, posting to appropriate platforms.

Features:
- Reads from LEDGER/content_queue.csv
- Routes content to correct platform poster
- Updates status after posting
- Logs results to LEDGER/post_log.csv
- Respects rate limits via AccountManager

Usage:
    from queue_processor import QueueProcessor

    processor = QueueProcessor()
    results = processor.process_pending()
    processor.process_scheduled()  # For scheduled posts

CLI:
    python queue_processor.py --process-pending
    python queue_processor.py --process-scheduled
    python queue_processor.py --add --platform X --content "Hello" --account x_main
"""

import os
import sys
import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))

from account_manager import AccountManager
from x_poster import XPoster
from ig_poster import IGPoster


# Configure logging
LOG_DIR = Path(__file__).parent.parent.parent / "OPS" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "queue_processor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("queue_processor")


# Default paths
LEDGER_DIR = Path(__file__).parent.parent.parent / "LEDGER"
CONTENT_QUEUE_PATH = LEDGER_DIR / "content_queue.csv"
POST_LOG_PATH = LEDGER_DIR / "post_log.csv"
ACCOUNTS_CONFIG_PATH = LEDGER_DIR / "social_accounts.json"


@dataclass
class QueueItem:
    """Represents a content queue item."""
    id: str
    account_id: str
    platform: str
    content: str
    media_path: str = ""
    hashtags: str = ""
    scheduled_time: str = ""
    status: str = "pending"
    posted_at: str = ""
    error: str = ""
    niche: str = ""
    content_type: str = "post"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_csv_row(cls, row: Dict[str, str]) -> "QueueItem":
        """Create QueueItem from CSV row (CONTENT_PIPELINE.csv format)."""
        # Map from CONTENT_PIPELINE.csv format
        return cls(
            id=row.get("ContentID", row.get("id", "")),
            account_id=row.get("account_id", ""),
            platform=row.get("Platform", row.get("platform", "")),
            content=row.get("Title", row.get("content", "")),  # Title is used as content summary
            media_path=row.get("media_path", ""),
            hashtags=row.get("hashtags", ""),
            scheduled_time=row.get("ScheduledDate", row.get("scheduled_time", "")),
            status=row.get("Status", row.get("status", "QUEUED")).lower(),
            posted_at=row.get("PublishedDate", row.get("posted_at", "")),
            niche=row.get("Niche", row.get("niche", "")),
            content_type=row.get("Type", row.get("type", "Post")).lower(),
        )


class QueueProcessor:
    """Process content queue and post to platforms."""

    def __init__(
        self,
        queue_path: str = None,
        log_path: str = None,
        accounts_path: str = None
    ):
        """
        Initialize the queue processor.

        Args:
            queue_path: Path to content queue CSV
            log_path: Path to post log CSV
            accounts_path: Path to accounts configuration
        """
        self.queue_path = Path(queue_path or CONTENT_QUEUE_PATH)
        self.log_path = Path(log_path or POST_LOG_PATH)
        self.accounts_path = accounts_path or str(ACCOUNTS_CONFIG_PATH)

        # Initialize account manager
        self.account_manager = AccountManager(self.accounts_path)

        # Initialize post log if it doesn't exist
        self._init_post_log()

        logger.info(f"Queue processor initialized")
        logger.info(f"  Queue: {self.queue_path}")
        logger.info(f"  Log: {self.log_path}")

    def _init_post_log(self) -> None:
        """Initialize post log CSV if it doesn't exist."""
        if not self.log_path.exists():
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "queue_id", "account_id", "platform",
                    "content_preview", "status", "error"
                ])
            logger.info(f"Created post log: {self.log_path}")

    def load_queue(self) -> List[QueueItem]:
        """Load all items from the content queue."""
        items = []

        if not self.queue_path.exists():
            logger.warning(f"Queue file not found: {self.queue_path}")
            return items

        try:
            with open(self.queue_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    item = QueueItem.from_csv_row(row)
                    items.append(item)

            logger.info(f"Loaded {len(items)} items from queue")

        except Exception as e:
            logger.error(f"Error loading queue: {e}")

        return items

    def get_pending_items(self) -> List[QueueItem]:
        """Get all pending items from the queue."""
        items = self.load_queue()
        pending = [item for item in items if item.status in ("pending", "queued")]
        logger.info(f"Found {len(pending)} pending items")
        return pending

    def get_scheduled_items(self) -> List[QueueItem]:
        """Get all items scheduled for now or earlier."""
        items = self.load_queue()
        now = datetime.now()

        scheduled = []
        for item in items:
            if item.status != "scheduled" or not item.scheduled_time:
                continue

            try:
                scheduled_dt = datetime.fromisoformat(item.scheduled_time)
                if scheduled_dt <= now:
                    scheduled.append(item)
            except ValueError:
                continue

        logger.info(f"Found {len(scheduled)} items ready to post")
        return scheduled

    def _get_poster_for_platform(self, platform: str, account_config: Dict[str, Any]):
        """Get the appropriate poster class for a platform."""
        platform_lower = platform.lower()

        if platform_lower == "x":
            return XPoster(account_config)
        elif platform_lower == "instagram":
            return IGPoster(account_config)
        elif platform_lower == "tiktok":
            # TikTok would need its own poster
            logger.warning("TikTok posting not yet implemented")
            return None
        elif platform_lower == "youtube":
            # YouTube needs API-based posting
            logger.warning("YouTube posting not yet implemented")
            return None
        else:
            logger.error(f"Unknown platform: {platform}")
            return None

    def _build_account_config(self, account) -> Dict[str, Any]:
        """Build configuration dict for a poster from Account object."""
        return {
            "account_id": account.id,
            "proxy": account.proxy if account.proxy else None,
            "session_path": account.session_path,
            "headless": os.getenv("HEADLESS", "false").lower() == "true",
        }

    def post_item(self, item: QueueItem) -> Dict[str, Any]:
        """
        Post a single queue item.

        Args:
            item: The queue item to post

        Returns:
            Result dictionary with success status
        """
        result = {
            "queue_id": item.id,
            "account_id": item.account_id,
            "platform": item.platform,
            "success": False,
            "error": None,
            "timestamp": datetime.now().isoformat()
        }

        # Find or assign account
        account = None
        if item.account_id:
            account = self.account_manager.get_account(item.account_id)

        if not account:
            # Try to find an available account for this platform/niche
            account = self.account_manager.get_next_available(
                platform=item.platform,
                niche=item.niche if item.niche else None
            )

        if not account:
            result["error"] = f"No available account for {item.platform}"
            logger.error(result["error"])
            return result

        # Check rate limits
        if not self.account_manager.can_post(account.id):
            result["error"] = f"Account {account.id} is rate limited"
            logger.warning(result["error"])
            return result

        # Build account config
        account_config = self._build_account_config(account)

        # Get appropriate poster
        poster = self._get_poster_for_platform(item.platform, account_config)
        if not poster:
            result["error"] = f"No poster available for {item.platform}"
            return result

        # Post the content
        try:
            logger.info(f"Posting item {item.id} to {item.platform} via {account.id}")

            if item.platform.lower() == "instagram":
                if item.media_path:
                    hashtags = item.hashtags.split() if item.hashtags else None
                    post_result = poster.post_feed(
                        item.content,
                        item.media_path,
                        hashtags
                    )
                else:
                    result["error"] = "Instagram requires media"
                    return result
            else:
                # X/Twitter and others
                post_result = poster.post(
                    item.content,
                    item.media_path if item.media_path else None
                )

            result["success"] = post_result.get("success", False)
            if not result["success"]:
                result["error"] = post_result.get("error", "Unknown error")

            # Record the post in account manager
            self.account_manager.record_post(account.id, result["success"])

        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Error posting item {item.id}: {e}")

        # Log the result
        self._log_post(result, item)

        return result

    def _log_post(self, result: Dict[str, Any], item: QueueItem) -> None:
        """Log a post result to the post log CSV."""
        try:
            with open(self.log_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    result.get("timestamp", datetime.now().isoformat()),
                    item.id,
                    result.get("account_id", ""),
                    item.platform,
                    item.content[:50] if item.content else "",
                    "success" if result.get("success") else "failed",
                    result.get("error", "")
                ])
        except Exception as e:
            logger.error(f"Error logging post: {e}")

    def update_queue_status(self, item_id: str, status: str, error: str = "") -> None:
        """Update the status of a queue item."""
        if not self.queue_path.exists():
            return

        try:
            # Read all items
            items = []
            with open(self.queue_path, 'r') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                for row in reader:
                    if row.get("ContentID", row.get("id")) == item_id:
                        row["Status"] = status.upper()
                        if status == "posted":
                            row["PublishedDate"] = datetime.now().isoformat()
                    items.append(row)

            # Write back
            with open(self.queue_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(items)

            logger.info(f"Updated item {item_id} status to {status}")

        except Exception as e:
            logger.error(f"Error updating queue status: {e}")

    def process_pending(self, limit: int = None, dry_run: bool = False) -> List[Dict[str, Any]]:
        """
        Process all pending items in the queue.

        Args:
            limit: Maximum number of items to process
            dry_run: If True, don't actually post

        Returns:
            List of results for each processed item
        """
        results = []
        pending = self.get_pending_items()

        if limit:
            pending = pending[:limit]

        logger.info(f"Processing {len(pending)} pending items (dry_run={dry_run})")

        for item in pending:
            if dry_run:
                logger.info(f"[DRY RUN] Would post: {item.id} to {item.platform}")
                results.append({
                    "queue_id": item.id,
                    "dry_run": True,
                    "platform": item.platform
                })
                continue

            result = self.post_item(item)
            results.append(result)

            # Update queue status
            new_status = "posted" if result["success"] else "failed"
            self.update_queue_status(item.id, new_status, result.get("error", ""))

            # Small delay between posts to avoid detection
            import time
            import random
            time.sleep(random.uniform(5, 15))

        return results

    def process_scheduled(self, dry_run: bool = False) -> List[Dict[str, Any]]:
        """
        Process items that are scheduled for now or earlier.

        Args:
            dry_run: If True, don't actually post

        Returns:
            List of results for each processed item
        """
        results = []
        scheduled = self.get_scheduled_items()

        logger.info(f"Processing {len(scheduled)} scheduled items")

        for item in scheduled:
            if dry_run:
                logger.info(f"[DRY RUN] Would post scheduled: {item.id}")
                continue

            result = self.post_item(item)
            results.append(result)

            new_status = "posted" if result["success"] else "failed"
            self.update_queue_status(item.id, new_status, result.get("error", ""))

            import time
            import random
            time.sleep(random.uniform(5, 15))

        return results

    def add_to_queue(
        self,
        platform: str,
        content: str,
        account_id: str = "",
        media_path: str = "",
        hashtags: str = "",
        scheduled_time: str = "",
        niche: str = ""
    ) -> str:
        """
        Add a new item to the content queue.

        Returns:
            The ID of the new queue item
        """
        # Generate new ID
        existing_items = self.load_queue()
        max_id = 0
        for item in existing_items:
            try:
                num = int(''.join(filter(str.isdigit, item.id)))
                max_id = max(max_id, num)
            except:
                pass
        new_id = f"Q{max_id + 1:04d}"

        # Determine status
        status = "scheduled" if scheduled_time else "pending"

        # Create new item
        new_item = QueueItem(
            id=new_id,
            account_id=account_id,
            platform=platform,
            content=content,
            media_path=media_path,
            hashtags=hashtags,
            scheduled_time=scheduled_time,
            status=status,
            niche=niche
        )

        # Append to CSV
        write_header = not self.queue_path.exists()

        with open(self.queue_path, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "ContentID", "Type", "Niche", "Platform", "Title", "Status",
                "ScheduledDate", "PublishedDate", "Engagement", "Notes",
                "account_id", "media_path", "hashtags"
            ])

            if write_header:
                writer.writeheader()

            writer.writerow({
                "ContentID": new_item.id,
                "Type": "Post",
                "Niche": niche,
                "Platform": platform,
                "Title": content,
                "Status": status.upper(),
                "ScheduledDate": scheduled_time,
                "PublishedDate": "",
                "Engagement": "0",
                "Notes": "",
                "account_id": account_id,
                "media_path": media_path,
                "hashtags": hashtags
            })

        logger.info(f"Added queue item: {new_id}")
        return new_id

    def get_queue_stats(self) -> Dict[str, Any]:
        """Get statistics about the queue."""
        items = self.load_queue()

        stats = {
            "total": len(items),
            "by_status": {},
            "by_platform": {},
            "by_niche": {},
        }

        for item in items:
            # By status
            status = item.status.lower()
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1

            # By platform
            platform = item.platform
            stats["by_platform"][platform] = stats["by_platform"].get(platform, 0) + 1

            # By niche
            if item.niche:
                stats["by_niche"][item.niche] = stats["by_niche"].get(item.niche, 0) + 1

        return stats


# CLI usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Content Queue Processor")
    parser.add_argument("--queue", help="Path to content queue CSV")
    parser.add_argument("--process-pending", action="store_true", help="Process pending items")
    parser.add_argument("--process-scheduled", action="store_true", help="Process scheduled items")
    parser.add_argument("--dry-run", action="store_true", help="Don't actually post")
    parser.add_argument("--limit", type=int, help="Limit number of items to process")
    parser.add_argument("--stats", action="store_true", help="Show queue statistics")
    parser.add_argument("--list", action="store_true", help="List queue items")
    parser.add_argument("--add", action="store_true", help="Add item to queue")
    parser.add_argument("--platform", help="Platform for new item")
    parser.add_argument("--content", help="Content for new item")
    parser.add_argument("--account", help="Account ID for new item")
    parser.add_argument("--media", help="Media path for new item")
    parser.add_argument("--hashtags", help="Hashtags for new item")
    parser.add_argument("--schedule", help="Scheduled time (ISO format)")
    parser.add_argument("--niche", help="Niche for new item")

    args = parser.parse_args()

    # Initialize processor
    processor = QueueProcessor(queue_path=args.queue)

    if args.process_pending:
        results = processor.process_pending(limit=args.limit, dry_run=args.dry_run)
        print(f"\nProcessed {len(results)} items:")
        for r in results:
            status = "OK" if r.get("success") or r.get("dry_run") else "FAIL"
            print(f"  [{status}] {r.get('queue_id')}: {r.get('error', 'Success')}")

    elif args.process_scheduled:
        results = processor.process_scheduled(dry_run=args.dry_run)
        print(f"\nProcessed {len(results)} scheduled items")

    elif args.stats:
        stats = processor.get_queue_stats()
        print("\nQueue Statistics:")
        print("-" * 40)
        print(f"  Total items: {stats['total']}")
        print("\n  By Status:")
        for status, count in stats["by_status"].items():
            print(f"    {status}: {count}")
        print("\n  By Platform:")
        for platform, count in stats["by_platform"].items():
            print(f"    {platform}: {count}")
        if stats["by_niche"]:
            print("\n  By Niche:")
            for niche, count in stats["by_niche"].items():
                print(f"    {niche}: {count}")

    elif args.list:
        items = processor.load_queue()
        print(f"\nQueue Items ({len(items)}):")
        print("-" * 70)
        for item in items[:20]:  # Show first 20
            status_icon = {"pending": ".", "queued": ".", "posted": "+", "failed": "x"}.get(item.status, "?")
            print(f"  [{status_icon}] {item.id}: {item.platform} - {item.content[:40]}...")

    elif args.add:
        if not args.platform or not args.content:
            print("Error: --platform and --content required for --add")
            sys.exit(1)

        new_id = processor.add_to_queue(
            platform=args.platform,
            content=args.content,
            account_id=args.account or "",
            media_path=args.media or "",
            hashtags=args.hashtags or "",
            scheduled_time=args.schedule or "",
            niche=args.niche or ""
        )
        print(f"Added to queue: {new_id}")

    else:
        parser.print_help()
