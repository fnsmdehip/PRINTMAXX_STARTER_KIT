#!/usr/bin/env python3
"""
PRINTMAXX Content Queue Manager

Manages content scheduling and posting workflow.
Reads from LEDGER/content_queue.csv and updates status.

Usage:
    python scripts/content_queue.py --show-queue         # Show next items to post
    python scripts/content_queue.py --show-queue -n 20   # Show 20 items
    python scripts/content_queue.py --mark-posted A001   # Mark item as posted
    python scripts/content_queue.py --generate 10        # Generate queue entries
    python scripts/content_queue.py --stats              # Show queue statistics
    python scripts/content_queue.py --by-platform        # Show queue by platform
    python scripts/content_queue.py --by-niche           # Show queue by niche
"""

import os
import sys
import csv
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# File paths
CONTENT_QUEUE_FILE = PROJECT_ROOT / "LEDGER" / "content_queue.csv"
CONTENT_PIPELINE_FILE = PROJECT_ROOT / "LEDGER" / "CONTENT_PIPELINE.csv"
POST_LOG_FILE = PROJECT_ROOT / "LEDGER" / "post_log.csv"

# Status values
STATUS_QUEUED = "QUEUED"
STATUS_POSTED = "POSTED"
STATUS_SCHEDULED = "SCHEDULED"
STATUS_FAILED = "FAILED"
STATUS_DRAFT = "DRAFT"

# CSV headers
QUEUE_HEADERS = [
    "ContentID", "Type", "Niche", "Platform", "Title",
    "Status", "ScheduledDate", "PublishedDate", "Engagement", "Notes"
]


def ensure_queue_file_exists():
    """Create content queue file if it doesn't exist."""
    # Use CONTENT_PIPELINE.csv as the queue file if content_queue.csv doesn't exist
    if not CONTENT_QUEUE_FILE.exists():
        if CONTENT_PIPELINE_FILE.exists():
            print(f"Using {CONTENT_PIPELINE_FILE} as content queue")
            return CONTENT_PIPELINE_FILE
        else:
            # Create new queue file
            CONTENT_QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(CONTENT_QUEUE_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(QUEUE_HEADERS)
            print(f"Created new queue file: {CONTENT_QUEUE_FILE}")
            return CONTENT_QUEUE_FILE
    return CONTENT_QUEUE_FILE


def get_queue_file() -> Path:
    """Get the active queue file path."""
    if CONTENT_QUEUE_FILE.exists():
        return CONTENT_QUEUE_FILE
    elif CONTENT_PIPELINE_FILE.exists():
        return CONTENT_PIPELINE_FILE
    else:
        return ensure_queue_file_exists()


def read_queue() -> List[Dict]:
    """Read all entries from the content queue."""
    queue_file = get_queue_file()
    entries = []

    try:
        with open(queue_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                entries.append(row)
    except Exception as e:
        print(f"Error reading queue: {e}")
        return []

    return entries


def write_queue(entries: List[Dict]):
    """Write entries back to the queue file."""
    queue_file = get_queue_file()

    # Get headers from first entry or use defaults
    if entries:
        headers = list(entries[0].keys())
    else:
        headers = QUEUE_HEADERS

    try:
        with open(queue_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(entries)
    except Exception as e:
        print(f"Error writing queue: {e}")


def show_queue(n: int = 10, platform: Optional[str] = None, niche: Optional[str] = None):
    """Display next items to post."""
    entries = read_queue()

    # Filter for queued items
    queued = [e for e in entries if e.get('Status', '').upper() == STATUS_QUEUED]

    # Apply filters
    if platform:
        queued = [e for e in queued if e.get('Platform', '').lower() == platform.lower()]
    if niche:
        queued = [e for e in queued if e.get('Niche', '').lower() == niche.lower()]

    # Take first n
    to_show = queued[:n]

    if not to_show:
        print("No queued items found")
        return

    print(f"\n=== NEXT {len(to_show)} ITEMS TO POST ===\n")
    print(f"{'ID':<8} {'Platform':<10} {'Niche':<10} {'Type':<8} {'Title':<40}")
    print("-" * 80)

    for entry in to_show:
        content_id = entry.get('ContentID', 'N/A')[:7]
        platform = entry.get('Platform', 'N/A')[:9]
        niche = entry.get('Niche', 'N/A')[:9]
        content_type = entry.get('Type', 'N/A')[:7]
        title = entry.get('Title', 'N/A')[:39]

        print(f"{content_id:<8} {platform:<10} {niche:<10} {content_type:<8} {title:<40}")

    print(f"\nTotal queued: {len(queued)}")


def show_by_platform():
    """Show queue breakdown by platform."""
    entries = read_queue()
    queued = [e for e in entries if e.get('Status', '').upper() == STATUS_QUEUED]

    by_platform = defaultdict(int)
    for entry in queued:
        platform = entry.get('Platform', 'Unknown')
        by_platform[platform] += 1

    print("\n=== QUEUE BY PLATFORM ===\n")
    for platform, count in sorted(by_platform.items(), key=lambda x: -x[1]):
        print(f"  {platform:<15} {count:>4} items")


def show_by_niche():
    """Show queue breakdown by niche."""
    entries = read_queue()
    queued = [e for e in entries if e.get('Status', '').upper() == STATUS_QUEUED]

    by_niche = defaultdict(int)
    for entry in queued:
        niche = entry.get('Niche', 'Unknown')
        by_niche[niche] += 1

    print("\n=== QUEUE BY NICHE ===\n")
    for niche, count in sorted(by_niche.items(), key=lambda x: -x[1]):
        print(f"  {niche:<15} {count:>4} items")


def show_stats():
    """Show queue statistics."""
    entries = read_queue()

    status_counts = defaultdict(int)
    for entry in entries:
        status = entry.get('Status', 'Unknown').upper()
        status_counts[status] += 1

    print("\n=== QUEUE STATISTICS ===\n")
    print(f"Total entries: {len(entries)}")
    print()
    for status, count in sorted(status_counts.items()):
        print(f"  {status:<12} {count:>4}")

    # Show platform breakdown for queued items
    show_by_platform()
    show_by_niche()


def mark_posted(content_id: str):
    """Mark an item as posted."""
    entries = read_queue()
    found = False

    for entry in entries:
        if entry.get('ContentID', '').upper() == content_id.upper():
            entry['Status'] = STATUS_POSTED
            entry['PublishedDate'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            found = True
            break

    if found:
        write_queue(entries)
        print(f"Marked {content_id} as POSTED")

        # Also log to post_log.csv
        log_post(content_id)
    else:
        print(f"Content ID '{content_id}' not found")


def mark_multiple_posted(content_ids: List[str]):
    """Mark multiple items as posted."""
    entries = read_queue()
    marked = []

    for entry in entries:
        cid = entry.get('ContentID', '')
        if cid.upper() in [c.upper() for c in content_ids]:
            entry['Status'] = STATUS_POSTED
            entry['PublishedDate'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            marked.append(cid)

    if marked:
        write_queue(entries)
        print(f"Marked {len(marked)} items as POSTED: {', '.join(marked)}")

        # Log each
        for cid in marked:
            log_post(cid)
    else:
        print("No matching content IDs found")


def log_post(content_id: str):
    """Log a posted item to post_log.csv."""
    log_file = POST_LOG_FILE

    # Create log file if it doesn't exist
    if not log_file.exists():
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ContentID', 'PostedAt', 'Platform', 'Status'])

    # Append to log
    with open(log_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([content_id, datetime.now().isoformat(), '', 'SUCCESS'])


def generate_queue_entries(count: int):
    """Generate placeholder queue entries."""
    entries = read_queue()

    # Find highest existing ID
    max_id = 0
    for entry in entries:
        cid = entry.get('ContentID', '')
        # Extract number from ID like A001, F029, etc.
        if cid and len(cid) >= 4:
            try:
                num = int(cid[1:])
                max_id = max(max_id, num)
            except ValueError:
                pass

    # Generate new entries
    niches = ['AI', 'Faith', 'Fitness']
    platforms = ['X', 'TikTok', 'Instagram', 'YouTube']
    content_types = ['Post', 'Thread', 'Video']

    new_entries = []
    for i in range(count):
        idx = max_id + i + 1
        niche = niches[i % len(niches)]
        platform = platforms[i % len(platforms)]
        content_type = content_types[i % len(content_types)]

        prefix = niche[0].upper()
        content_id = f"{prefix}{idx:03d}"

        new_entries.append({
            'ContentID': content_id,
            'Type': content_type,
            'Niche': niche,
            'Platform': platform,
            'Title': f'[PLACEHOLDER] {niche} {content_type} #{idx}',
            'Status': STATUS_DRAFT,
            'ScheduledDate': '',
            'PublishedDate': '',
            'Engagement': '0',
            'Notes': 'Auto-generated placeholder'
        })

    # Add to existing entries
    entries.extend(new_entries)
    write_queue(entries)

    print(f"Generated {count} new queue entries (IDs: {new_entries[0]['ContentID']} - {new_entries[-1]['ContentID']})")
    print("Status: DRAFT (update to QUEUED when ready)")


def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Content Queue Manager")
    parser.add_argument("--show-queue", action="store_true", help="Show next items to post")
    parser.add_argument("-n", type=int, default=10, help="Number of items to show")
    parser.add_argument("--platform", type=str, help="Filter by platform")
    parser.add_argument("--niche", type=str, help="Filter by niche")
    parser.add_argument("--mark-posted", type=str, help="Mark content ID as posted")
    parser.add_argument("--mark-multiple", type=str, nargs='+', help="Mark multiple IDs as posted")
    parser.add_argument("--generate", type=int, help="Generate N placeholder queue entries")
    parser.add_argument("--stats", action="store_true", help="Show queue statistics")
    parser.add_argument("--by-platform", action="store_true", help="Show queue by platform")
    parser.add_argument("--by-niche", action="store_true", help="Show queue by niche")

    args = parser.parse_args()

    # Default action: show queue
    if not any([args.show_queue, args.mark_posted, args.mark_multiple,
                args.generate, args.stats, args.by_platform, args.by_niche]):
        args.show_queue = True

    if args.show_queue:
        show_queue(n=args.n, platform=args.platform, niche=args.niche)
    elif args.mark_posted:
        mark_posted(args.mark_posted)
    elif args.mark_multiple:
        mark_multiple_posted(args.mark_multiple)
    elif args.generate:
        generate_queue_entries(args.generate)
    elif args.stats:
        show_stats()
    elif args.by_platform:
        show_by_platform()
    elif args.by_niche:
        show_by_niche()


if __name__ == "__main__":
    main()
