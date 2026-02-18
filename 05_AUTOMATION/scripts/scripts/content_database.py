#!/usr/bin/env python3
"""
Content Database System for PRINTMAXX

SQLite-based content storage with CRUD operations and CLI interface.
Tracks scraped content, posting status, and engagement metrics.

Database location: /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/LEDGER/content.db

Usage:
    python content_database.py add "source" "platform" "text"
    python content_database.py pending
    python content_database.py posted 123 "account_name"
    python content_database.py search "keyword"
    python content_database.py stats
    python content_database.py export output.csv
    python content_database.py import input.csv
    python content_database.py dedupe
"""

import argparse
import csv
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


# Database configuration
DB_PATH = Path("/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/LEDGER/content.db")


def get_connection() -> sqlite3.Connection:
    """Get database connection with row factory for dict-like access."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def create_db() -> None:
    """Initialize the database with content table and indexes."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    # Create content table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            platform TEXT NOT NULL,
            text TEXT NOT NULL,
            media_url TEXT,
            likes INTEGER DEFAULT 0,
            rts INTEGER DEFAULT 0,
            views INTEGER DEFAULT 0,
            scraped_at TEXT NOT NULL,
            posted_at TEXT,
            account_used TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create indexes for common queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_source ON content(source)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_scraped_at ON content(scraped_at)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_platform ON content(platform)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_posted_at ON content(posted_at)
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")


def add_content(
    source: str,
    platform: str,
    text: str,
    media_url: Optional[str] = None,
    metrics: Optional[Dict[str, int]] = None
) -> int:
    """
    Add new content to the database.

    Args:
        source: Content source (e.g., @username, subreddit, website)
        platform: Platform where content was found (e.g., twitter, reddit, tiktok)
        text: Content text
        media_url: Optional URL to media (image, video)
        metrics: Optional dict with 'likes', 'rts', 'views' keys

    Returns:
        ID of the inserted content
    """
    conn = get_connection()
    cursor = conn.cursor()

    likes = metrics.get("likes", 0) if metrics else 0
    rts = metrics.get("rts", 0) if metrics else 0
    views = metrics.get("views", 0) if metrics else 0
    scraped_at = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO content (source, platform, text, media_url, likes, rts, views, scraped_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (source, platform, text, media_url, likes, rts, views, scraped_at))

    content_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return content_id


def get_pending() -> List[Dict[str, Any]]:
    """Get all content that has not been posted yet."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM content
        WHERE posted_at IS NULL
        ORDER BY scraped_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def mark_posted(content_id: int, account: str) -> bool:
    """
    Mark content as posted.

    Args:
        content_id: ID of the content to mark
        account: Account name used for posting

    Returns:
        True if update was successful, False otherwise
    """
    conn = get_connection()
    cursor = conn.cursor()

    posted_at = datetime.now().isoformat()

    cursor.execute("""
        UPDATE content
        SET posted_at = ?, account_used = ?
        WHERE id = ?
    """, (posted_at, account, content_id))

    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()

    return updated


def get_by_source(source: str) -> List[Dict[str, Any]]:
    """
    Get all content from a specific source.

    Args:
        source: Source to filter by (partial match supported)

    Returns:
        List of content records
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM content
        WHERE source LIKE ?
        ORDER BY scraped_at DESC
    """, (f"%{source}%",))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def search(query: str) -> List[Dict[str, Any]]:
    """
    Full text search across content text.

    Args:
        query: Search query (case-insensitive partial match)

    Returns:
        List of matching content records
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM content
        WHERE text LIKE ?
        ORDER BY scraped_at DESC
    """, (f"%{query}%",))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def export_csv(filepath: str) -> int:
    """
    Export all content to CSV file.

    Args:
        filepath: Path to output CSV file

    Returns:
        Number of records exported
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM content ORDER BY scraped_at DESC")
    rows = cursor.fetchall()

    if not rows:
        conn.close()
        return 0

    # Get column names from first row
    columns = rows[0].keys()

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(row))

    conn.close()
    return len(rows)


def import_csv(filepath: str) -> Tuple[int, int]:
    """
    Import content from CSV file.

    Args:
        filepath: Path to input CSV file

    Returns:
        Tuple of (records imported, records skipped)
    """
    conn = get_connection()
    cursor = conn.cursor()

    imported = 0
    skipped = 0

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                # Required fields
                source = row.get("source", "")
                platform = row.get("platform", "")
                text = row.get("text", "")

                if not source or not platform or not text:
                    skipped += 1
                    continue

                # Optional fields
                media_url = row.get("media_url") or None
                likes = int(row.get("likes", 0) or 0)
                rts = int(row.get("rts", 0) or 0)
                views = int(row.get("views", 0) or 0)
                scraped_at = row.get("scraped_at") or datetime.now().isoformat()
                posted_at = row.get("posted_at") or None
                account_used = row.get("account_used") or None

                cursor.execute("""
                    INSERT INTO content
                    (source, platform, text, media_url, likes, rts, views, scraped_at, posted_at, account_used)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (source, platform, text, media_url, likes, rts, views, scraped_at, posted_at, account_used))

                imported += 1

            except Exception as e:
                print(f"Error importing row: {e}")
                skipped += 1

    conn.commit()
    conn.close()

    return imported, skipped


def dedupe() -> int:
    """
    Remove duplicate content based on text field.
    Keeps the first occurrence (lowest ID).

    Returns:
        Number of duplicates removed
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Find duplicates, keeping the lowest ID for each unique text
    cursor.execute("""
        DELETE FROM content
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM content
            GROUP BY text
        )
    """)

    removed = cursor.rowcount
    conn.commit()
    conn.close()

    return removed


def stats() -> Dict[str, Any]:
    """
    Get content statistics by source and platform.

    Returns:
        Dictionary with stats breakdown
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Total count
    cursor.execute("SELECT COUNT(*) as total FROM content")
    total = cursor.fetchone()["total"]

    # Pending count
    cursor.execute("SELECT COUNT(*) as pending FROM content WHERE posted_at IS NULL")
    pending = cursor.fetchone()["pending"]

    # Posted count
    cursor.execute("SELECT COUNT(*) as posted FROM content WHERE posted_at IS NOT NULL")
    posted = cursor.fetchone()["posted"]

    # By source
    cursor.execute("""
        SELECT source, COUNT(*) as count
        FROM content
        GROUP BY source
        ORDER BY count DESC
    """)
    by_source = {row["source"]: row["count"] for row in cursor.fetchall()}

    # By platform
    cursor.execute("""
        SELECT platform, COUNT(*) as count
        FROM content
        GROUP BY platform
        ORDER BY count DESC
    """)
    by_platform = {row["platform"]: row["count"] for row in cursor.fetchall()}

    # By account used
    cursor.execute("""
        SELECT account_used, COUNT(*) as count
        FROM content
        WHERE account_used IS NOT NULL
        GROUP BY account_used
        ORDER BY count DESC
    """)
    by_account = {row["account_used"]: row["count"] for row in cursor.fetchall()}

    conn.close()

    return {
        "total": total,
        "pending": pending,
        "posted": posted,
        "by_source": by_source,
        "by_platform": by_platform,
        "by_account": by_account
    }


def get_content_by_id(content_id: int) -> Optional[Dict[str, Any]]:
    """
    Get a single content record by ID.

    Args:
        content_id: ID of the content

    Returns:
        Content record or None if not found
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM content WHERE id = ?", (content_id,))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def delete_content(content_id: int) -> bool:
    """
    Delete content by ID.

    Args:
        content_id: ID of the content to delete

    Returns:
        True if deleted, False if not found
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM content WHERE id = ?", (content_id,))
    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted


def update_metrics(content_id: int, likes: int = None, rts: int = None, views: int = None) -> bool:
    """
    Update engagement metrics for content.

    Args:
        content_id: ID of the content
        likes: New likes count (optional)
        rts: New retweets/shares count (optional)
        views: New views count (optional)

    Returns:
        True if updated, False if not found
    """
    updates = []
    values = []

    if likes is not None:
        updates.append("likes = ?")
        values.append(likes)
    if rts is not None:
        updates.append("rts = ?")
        values.append(rts)
    if views is not None:
        updates.append("views = ?")
        values.append(views)

    if not updates:
        return False

    values.append(content_id)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        UPDATE content
        SET {', '.join(updates)}
        WHERE id = ?
    """, tuple(values))

    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()

    return updated


def format_content_row(row: Dict[str, Any], verbose: bool = False) -> str:
    """Format a content row for display."""
    text_preview = row["text"][:80] + "..." if len(row["text"]) > 80 else row["text"]
    status = "POSTED" if row["posted_at"] else "PENDING"

    if verbose:
        return (
            f"ID: {row['id']}\n"
            f"  Source: {row['source']}\n"
            f"  Platform: {row['platform']}\n"
            f"  Text: {text_preview}\n"
            f"  Media: {row['media_url'] or 'None'}\n"
            f"  Metrics: {row['likes']} likes, {row['rts']} RTs, {row['views']} views\n"
            f"  Scraped: {row['scraped_at']}\n"
            f"  Status: {status}\n"
            f"  Account: {row['account_used'] or 'N/A'}"
        )
    else:
        return f"[{row['id']}] [{status}] @{row['source']} ({row['platform']}): {text_preview}"


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Content Database System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python content_database.py init
    python content_database.py add "@levelsio" "twitter" "shipped 12 products this year"
    python content_database.py add "@levelsio" "twitter" "text" --media "https://..." --likes 500
    python content_database.py pending
    python content_database.py posted 123 "niche_account_1"
    python content_database.py search "automation"
    python content_database.py source "@levelsio"
    python content_database.py stats
    python content_database.py export backup.csv
    python content_database.py import data.csv
    python content_database.py dedupe
    python content_database.py delete 123
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # init command
    subparsers.add_parser("init", help="Initialize the database")

    # add command
    add_parser = subparsers.add_parser("add", help="Add new content")
    add_parser.add_argument("source", help="Content source (e.g., @username)")
    add_parser.add_argument("platform", help="Platform (e.g., twitter, reddit)")
    add_parser.add_argument("text", help="Content text")
    add_parser.add_argument("--media", help="Media URL")
    add_parser.add_argument("--likes", type=int, default=0, help="Likes count")
    add_parser.add_argument("--rts", type=int, default=0, help="Retweets/shares count")
    add_parser.add_argument("--views", type=int, default=0, help="Views count")

    # pending command
    pending_parser = subparsers.add_parser("pending", help="Get pending content")
    pending_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    pending_parser.add_argument("-n", "--limit", type=int, help="Limit results")

    # posted command
    posted_parser = subparsers.add_parser("posted", help="Mark content as posted")
    posted_parser.add_argument("id", type=int, help="Content ID")
    posted_parser.add_argument("account", help="Account used for posting")

    # search command
    search_parser = subparsers.add_parser("search", help="Search content")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    # source command
    source_parser = subparsers.add_parser("source", help="Filter by source")
    source_parser.add_argument("source", help="Source to filter by")
    source_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    # stats command
    subparsers.add_parser("stats", help="Show content statistics")

    # export command
    export_parser = subparsers.add_parser("export", help="Export to CSV")
    export_parser.add_argument("filepath", help="Output CSV file path")

    # import command
    import_parser = subparsers.add_parser("import", help="Import from CSV")
    import_parser.add_argument("filepath", help="Input CSV file path")

    # dedupe command
    subparsers.add_parser("dedupe", help="Remove duplicate content")

    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete content by ID")
    delete_parser.add_argument("id", type=int, help="Content ID to delete")

    # get command
    get_parser = subparsers.add_parser("get", help="Get content by ID")
    get_parser.add_argument("id", type=int, help="Content ID")

    args = parser.parse_args()

    # Ensure database exists for all commands except init
    if args.command != "init" and not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}")
        print("Run 'python content_database.py init' first")
        return

    if args.command == "init":
        create_db()

    elif args.command == "add":
        metrics = {"likes": args.likes, "rts": args.rts, "views": args.views}
        content_id = add_content(
            args.source,
            args.platform,
            args.text,
            media_url=args.media,
            metrics=metrics
        )
        print(f"Added content with ID: {content_id}")

    elif args.command == "pending":
        rows = get_pending()
        if args.limit:
            rows = rows[:args.limit]

        if not rows:
            print("No pending content")
        else:
            print(f"Pending content ({len(rows)} items):\n")
            for row in rows:
                print(format_content_row(row, args.verbose))
                if args.verbose:
                    print()

    elif args.command == "posted":
        if mark_posted(args.id, args.account):
            print(f"Marked content {args.id} as posted by {args.account}")
        else:
            print(f"Content {args.id} not found")

    elif args.command == "search":
        rows = search(args.query)
        if not rows:
            print(f"No results for '{args.query}'")
        else:
            print(f"Found {len(rows)} results:\n")
            for row in rows:
                print(format_content_row(row, args.verbose))
                if args.verbose:
                    print()

    elif args.command == "source":
        rows = get_by_source(args.source)
        if not rows:
            print(f"No content from '{args.source}'")
        else:
            print(f"Content from '{args.source}' ({len(rows)} items):\n")
            for row in rows:
                print(format_content_row(row, args.verbose))
                if args.verbose:
                    print()

    elif args.command == "stats":
        s = stats()
        print("Content Database Statistics")
        print("=" * 40)
        print(f"Total: {s['total']}")
        print(f"Pending: {s['pending']}")
        print(f"Posted: {s['posted']}")
        print()

        if s["by_source"]:
            print("By Source:")
            for source, count in list(s["by_source"].items())[:10]:
                print(f"  {source}: {count}")
            if len(s["by_source"]) > 10:
                print(f"  ... and {len(s['by_source']) - 10} more")
        print()

        if s["by_platform"]:
            print("By Platform:")
            for platform, count in s["by_platform"].items():
                print(f"  {platform}: {count}")
        print()

        if s["by_account"]:
            print("By Account Used:")
            for account, count in s["by_account"].items():
                print(f"  {account}: {count}")

    elif args.command == "export":
        count = export_csv(args.filepath)
        print(f"Exported {count} records to {args.filepath}")

    elif args.command == "import":
        imported, skipped = import_csv(args.filepath)
        print(f"Imported {imported} records, skipped {skipped}")

    elif args.command == "dedupe":
        removed = dedupe()
        print(f"Removed {removed} duplicate records")

    elif args.command == "delete":
        if delete_content(args.id):
            print(f"Deleted content {args.id}")
        else:
            print(f"Content {args.id} not found")

    elif args.command == "get":
        row = get_content_by_id(args.id)
        if row:
            print(format_content_row(row, verbose=True))
        else:
            print(f"Content {args.id} not found")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
