#!/usr/bin/env python3
"""
Post Queue Management

SQLite-based queue for scheduling and tracking social media posts.
Manages posts across multiple platforms and accounts.
"""

import argparse
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional


DB_PATH = Path("/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/LEDGER/queue.db")


def get_connection() -> sqlite3.Connection:
    """Get database connection with row factory."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def create_db() -> None:
    """Initialize queue database with schema."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id INTEGER NOT NULL,
            platform TEXT NOT NULL,
            account TEXT NOT NULL,
            scheduled_time TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            sent_at TEXT,
            error TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (content_id) REFERENCES content(id)
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_scheduled_time ON queue(scheduled_time)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_status ON queue(status)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_platform ON queue(platform)
    """)

    conn.commit()
    conn.close()
    print(f"Queue database created at {DB_PATH}")


def add_to_queue(
    content_id: int,
    platform: str,
    account: str,
    scheduled_time: str
) -> int:
    """
    Add post to queue.

    Args:
        content_id: ID from content database
        platform: Platform to post to (twitter, tiktok, instagram)
        account: Account to post from
        scheduled_time: ISO format datetime string

    Returns:
        Queue item ID
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO queue (content_id, platform, account, scheduled_time)
        VALUES (?, ?, ?, ?)
    """, (content_id, platform, account, scheduled_time))

    queue_id = cursor.lastrowid
    conn.commit()
    conn.close()

    print(f"Added to queue: ID {queue_id}")
    return queue_id


def get_due_posts(platform: Optional[str] = None) -> List[Dict]:
    """
    Get posts that are due to be sent.

    Args:
        platform: Optional platform filter

    Returns:
        List of due posts
    """
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.utcnow().isoformat()

    if platform:
        cursor.execute("""
            SELECT * FROM queue
            WHERE status = 'pending'
            AND scheduled_time <= ?
            AND platform = ?
            ORDER BY scheduled_time ASC
        """, (now, platform))
    else:
        cursor.execute("""
            SELECT * FROM queue
            WHERE status = 'pending'
            AND scheduled_time <= ?
            ORDER BY scheduled_time ASC
        """, (now,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def mark_sent(queue_id: int) -> bool:
    """
    Mark queue item as sent.

    Args:
        queue_id: Queue item ID

    Returns:
        True if updated, False otherwise
    """
    conn = get_connection()
    cursor = conn.cursor()

    sent_at = datetime.utcnow().isoformat()

    cursor.execute("""
        UPDATE queue
        SET status = 'sent', sent_at = ?
        WHERE id = ?
    """, (sent_at, queue_id))

    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()

    if updated:
        print(f"Marked queue item {queue_id} as sent")

    return updated


def mark_failed(queue_id: int, error: str) -> bool:
    """
    Mark queue item as failed.

    Args:
        queue_id: Queue item ID
        error: Error message

    Returns:
        True if updated, False otherwise
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE queue
        SET status = 'failed', error = ?
        WHERE id = ?
    """, (error, queue_id))

    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()

    if updated:
        print(f"Marked queue item {queue_id} as failed")

    return updated


def reschedule(queue_id: int, new_time: str) -> bool:
    """
    Reschedule a queued post.

    Args:
        queue_id: Queue item ID
        new_time: New scheduled time (ISO format)

    Returns:
        True if updated, False otherwise
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE queue
        SET scheduled_time = ?, status = 'pending'
        WHERE id = ?
    """, (new_time, queue_id))

    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()

    if updated:
        print(f"Rescheduled queue item {queue_id} to {new_time}")

    return updated


def delete_from_queue(queue_id: int) -> bool:
    """
    Delete item from queue.

    Args:
        queue_id: Queue item ID

    Returns:
        True if deleted, False otherwise
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM queue WHERE id = ?", (queue_id,))

    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()

    if deleted:
        print(f"Deleted queue item {queue_id}")

    return deleted


def get_pending_count(platform: Optional[str] = None) -> int:
    """
    Get count of pending posts.

    Args:
        platform: Optional platform filter

    Returns:
        Count of pending posts
    """
    conn = get_connection()
    cursor = conn.cursor()

    if platform:
        cursor.execute("""
            SELECT COUNT(*) as count FROM queue
            WHERE status = 'pending'
            AND platform = ?
        """, (platform,))
    else:
        cursor.execute("""
            SELECT COUNT(*) as count FROM queue
            WHERE status = 'pending'
        """)

    count = cursor.fetchone()["count"]
    conn.close()

    return count


def get_upcoming(limit: int = 20) -> List[Dict]:
    """
    Get upcoming scheduled posts.

    Args:
        limit: Max number to return

    Returns:
        List of upcoming posts
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM queue
        WHERE status = 'pending'
        ORDER BY scheduled_time ASC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_failed() -> List[Dict]:
    """
    Get all failed posts.

    Returns:
        List of failed posts
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM queue
        WHERE status = 'failed'
        ORDER BY scheduled_time DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def stats() -> Dict:
    """Get queue statistics."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM queue")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as count FROM queue WHERE status = 'pending'")
    pending = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) as count FROM queue WHERE status = 'sent'")
    sent = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) as count FROM queue WHERE status = 'failed'")
    failed = cursor.fetchone()["count"]

    cursor.execute("""
        SELECT platform, COUNT(*) as count
        FROM queue
        WHERE status = 'pending'
        GROUP BY platform
    """)
    by_platform = {row["platform"]: row["count"] for row in cursor.fetchall()}

    cursor.execute("""
        SELECT account, COUNT(*) as count
        FROM queue
        WHERE status = 'pending'
        GROUP BY account
    """)
    by_account = {row["account"]: row["count"] for row in cursor.fetchall()}

    conn.close()

    return {
        "total": total,
        "pending": pending,
        "sent": sent,
        "failed": failed,
        "by_platform": by_platform,
        "by_account": by_account
    }


def main():
    """CLI interface."""
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Post Queue Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python post_queue.py init
    python post_queue.py add 123 twitter @faith_account "2026-01-25T10:00:00"
    python post_queue.py due
    python post_queue.py due --platform twitter
    python post_queue.py sent 45
    python post_queue.py failed 45 "API error"
    python post_queue.py reschedule 45 "2026-01-25T12:00:00"
    python post_queue.py upcoming
    python post_queue.py stats
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # init
    subparsers.add_parser("init", help="Initialize queue database")

    # add
    add_parser = subparsers.add_parser("add", help="Add post to queue")
    add_parser.add_argument("content_id", type=int, help="Content ID")
    add_parser.add_argument("platform", help="Platform (twitter, tiktok, instagram)")
    add_parser.add_argument("account", help="Account name")
    add_parser.add_argument("scheduled_time", help="Scheduled time (ISO format)")

    # due
    due_parser = subparsers.add_parser("due", help="Get due posts")
    due_parser.add_argument("--platform", help="Filter by platform")

    # sent
    sent_parser = subparsers.add_parser("sent", help="Mark as sent")
    sent_parser.add_argument("id", type=int, help="Queue item ID")

    # failed
    failed_parser = subparsers.add_parser("failed", help="Mark as failed")
    failed_parser.add_argument("id", type=int, help="Queue item ID")
    failed_parser.add_argument("error", help="Error message")

    # reschedule
    reschedule_parser = subparsers.add_parser("reschedule", help="Reschedule post")
    reschedule_parser.add_argument("id", type=int, help="Queue item ID")
    reschedule_parser.add_argument("time", help="New scheduled time (ISO format)")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete from queue")
    delete_parser.add_argument("id", type=int, help="Queue item ID")

    # upcoming
    upcoming_parser = subparsers.add_parser("upcoming", help="Get upcoming posts")
    upcoming_parser.add_argument("--limit", type=int, default=20, help="Max results")

    # show-failed
    subparsers.add_parser("show-failed", help="Show failed posts")

    # stats
    subparsers.add_parser("stats", help="Show queue statistics")

    args = parser.parse_args()

    if args.command != "init" and not DB_PATH.exists():
        print(f"Queue database not found at {DB_PATH}")
        print("Run 'python post_queue.py init' first")
        return

    if args.command == "init":
        create_db()

    elif args.command == "add":
        add_to_queue(
            args.content_id,
            args.platform,
            args.account,
            args.scheduled_time
        )

    elif args.command == "due":
        posts = get_due_posts(args.platform)
        if not posts:
            print("No posts due")
        else:
            print(f"Posts due ({len(posts)} items):\n")
            for post in posts:
                print(f"ID {post['id']}: Content {post['content_id']}")
                print(f"  Platform: {post['platform']}")
                print(f"  Account: {post['account']}")
                print(f"  Scheduled: {post['scheduled_time']}")
                print()

    elif args.command == "sent":
        mark_sent(args.id)

    elif args.command == "failed":
        mark_failed(args.id, args.error)

    elif args.command == "reschedule":
        reschedule(args.id, args.time)

    elif args.command == "delete":
        delete_from_queue(args.id)

    elif args.command == "upcoming":
        posts = get_upcoming(args.limit)
        if not posts:
            print("No upcoming posts")
        else:
            print(f"Upcoming posts ({len(posts)} items):\n")
            for post in posts:
                print(f"ID {post['id']}: Content {post['content_id']}")
                print(f"  {post['platform']} via {post['account']}")
                print(f"  Scheduled: {post['scheduled_time']}")
                print()

    elif args.command == "show-failed":
        posts = get_failed()
        if not posts:
            print("No failed posts")
        else:
            print(f"Failed posts ({len(posts)} items):\n")
            for post in posts:
                print(f"ID {post['id']}: Content {post['content_id']}")
                print(f"  {post['platform']} via {post['account']}")
                print(f"  Error: {post['error']}")
                print()

    elif args.command == "stats":
        s = stats()
        print("Queue Statistics")
        print("=" * 40)
        print(f"Total: {s['total']}")
        print(f"Pending: {s['pending']}")
        print(f"Sent: {s['sent']}")
        print(f"Failed: {s['failed']}")
        print()

        if s["by_platform"]:
            print("Pending by platform:")
            for platform, count in s["by_platform"].items():
                print(f"  {platform}: {count}")
            print()

        if s["by_account"]:
            print("Pending by account:")
            for account, count in s["by_account"].items():
                print(f"  {account}: {count}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
