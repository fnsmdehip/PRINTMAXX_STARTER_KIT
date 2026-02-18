#!/usr/bin/env python3
"""
Content Repurposing Pipeline - Automate the 15-output chain.

Takes content from one format and generates stubs/drafts for all 15 outputs.
Manages the QA queue and tracks content status.

Usage:
    python3 content_pipeline.py create --source "alpha finding text" --category APP_FACTORY
    python3 content_pipeline.py queue                    # Show QA queue
    python3 content_pipeline.py approve CONTENT_001      # Approve content
    python3 content_pipeline.py reject CONTENT_001       # Reject content
    python3 content_pipeline.py stats                    # Pipeline stats
    python3 content_pipeline.py schedule                 # Show posting schedule
"""

import csv
import json
import argparse
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_DIR / "LEDGER"
OPS_DIR = PROJECT_DIR / "OPS"
QA_QUEUE_DIR = OPS_DIR / "CONTENT_QA_QUEUE"
CONTENT_DIR = PROJECT_DIR / "CONTENT"
POSTING_QUEUE = PROJECT_DIR / "AUTOMATIONS" / "content_posting" / "posting_queue.csv"

# Ensure directories exist
QA_QUEUE_DIR.mkdir(parents=True, exist_ok=True)
(PROJECT_DIR / "AUTOMATIONS" / "content_posting").mkdir(parents=True, exist_ok=True)


def get_next_content_id() -> str:
    """Get the next content ID from QA queue."""
    existing = list(QA_QUEUE_DIR.glob("CONTENT_*.md"))
    if not existing:
        return "CONTENT_001"
    max_num = max(int(f.stem.split('_')[1]) for f in existing if f.stem.split('_')[1].isdigit())
    return f"CONTENT_{max_num + 1:03d}"


def create_content_chain(source_text: str, category: str, source_url: str = ""):
    """Create the 15-output content chain from a single source."""

    base_id = get_next_content_id()
    created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    outputs = [
        {
            "num": 1,
            "platform": "twitter",
            "content_type": "post",
            "description": "Hook post with reply bait",
            "template": f"""---
platform: twitter
content_type: post
source_intel: {category}
source_url: {source_url}
scheduled_time: TBD
status: PENDING_REVIEW
created: {created}
---

# Twitter/X Post

HOOK: [consequence-first hook from the intel]

BODY:
- [insight 1 with specific number]
- [insight 2 with specific number]
- [insight 3 with specific number]

CTA: reply '[KEYWORD]' and i'll send you the full breakdown

---
SOURCE INTEL:
{source_text[:500]}
"""
        },
        {
            "num": 2,
            "platform": "twitter",
            "content_type": "thread",
            "description": "5-7 tweet self-reply thread",
            "template": f"""---
platform: twitter
content_type: thread
source_intel: {category}
source_url: {source_url}
scheduled_time: TBD
status: PENDING_REVIEW
created: {created}
---

# Twitter/X Thread (5-7 tweets)

TWEET 1 (Hook):
[same as post hook, or variation]

TWEET 2:
[context/backstory with numbers]

TWEET 3:
[the method/framework]

TWEET 4:
[proof/results]

TWEET 5:
[the twist/contrarian take]

TWEET 6:
[summary + what this means]

TWEET 7 (CTA):
full breakdown on my gumroad (link in bio)
or: reply '[KEYWORD]' for the template

---
SOURCE INTEL:
{source_text[:500]}
"""
        },
        {
            "num": 3,
            "platform": "tiktok",
            "content_type": "video_script",
            "description": "Faceless video script (30-60s)",
            "template": f"""---
platform: tiktok
content_type: video_script
source_intel: {category}
scheduled_time: TBD
status: PENDING_REVIEW
created: {created}
---

# Faceless Video Script

DURATION: 30-60 seconds
FORMAT: Text-on-screen slideshow
AUDIO: [trending sound or lo-fi]

SLIDE 1 (0-5s): [Hook - same energy as tweet]
SLIDE 2 (5-15s): [Key insight 1]
SLIDE 3 (15-25s): [Key insight 2]
SLIDE 4 (25-35s): [Key insight 3]
SLIDE 5 (35-45s): [The method]
SLIDE 6 (45-60s): CTA - "full breakdown in bio" or "comment [KEYWORD]"

---
SOURCE INTEL:
{source_text[:300]}
"""
        },
        {
            "num": 4,
            "platform": "medium",
            "content_type": "article",
            "description": "1500-word Medium article",
        },
        {
            "num": 5,
            "platform": "substack",
            "content_type": "post",
            "description": "Substack cross-post + Notes",
        },
        {
            "num": 6,
            "platform": "beehiiv",
            "content_type": "newsletter",
            "description": "Newsletter issue",
        },
        {
            "num": 7,
            "platform": "gumroad",
            "content_type": "product_spec",
            "description": "Gumroad PDF spec ($7-12)",
        },
        {
            "num": 8,
            "platform": "blog",
            "content_type": "seo_page",
            "description": "Longtail SEO blog post",
        },
        {
            "num": 9,
            "platform": "skool",
            "content_type": "thread",
            "description": "Skool community thread",
        },
        {
            "num": 10,
            "platform": "multi",
            "content_type": "persona_posts",
            "description": "AI persona niche-angle posts",
        },
        {
            "num": 11,
            "platform": "multi",
            "content_type": "cross_niche",
            "description": "Cross-niche adaptations (faith/fitness/tech)",
        },
        {
            "num": 12,
            "platform": "twitter",
            "content_type": "dm_funnel",
            "description": "High-ticket DM funnel CTA",
        },
        {
            "num": 13,
            "platform": "instagram",
            "content_type": "carousel",
            "description": "10-slide carousel/infographic",
        },
        {
            "num": 14,
            "platform": "pinterest",
            "content_type": "pin",
            "description": "Evergreen Pinterest pin",
        },
        {
            "num": 15,
            "platform": "multi",
            "content_type": "content_farm",
            "description": "Niche-specific content farm clips",
        },
    ]

    created_files = []

    for output in outputs:
        num = output["num"]
        content_id = f"{base_id}_{num:02d}"
        filename = f"{content_id}_{output['platform']}_{output['content_type']}.md"
        filepath = QA_QUEUE_DIR / filename

        if "template" in output:
            content = output["template"]
        else:
            content = f"""---
platform: {output['platform']}
content_type: {output['content_type']}
source_intel: {category}
source_url: {source_url}
scheduled_time: TBD
status: PENDING_REVIEW
created: {created}
---

# {output['description']}

[Draft content here - adapt from source intel]

---
SOURCE INTEL:
{source_text[:300]}
"""

        with open(filepath, 'w') as f:
            f.write(content)
        created_files.append(filename)

    print(f"\nCreated {len(created_files)} content pieces in QA queue:")
    for f in created_files:
        print(f"  {f}")
    print(f"\nReview: ls {QA_QUEUE_DIR}/")
    print(f"Approve: python3 content_pipeline.py approve {base_id}")


def show_queue():
    """Show current QA queue status."""
    files = sorted(QA_QUEUE_DIR.glob("*.md"))

    if not files:
        print("QA queue is empty.")
        return

    status_counts = {"PENDING_REVIEW": 0, "APPROVED": 0, "NEEDS_EDIT": 0, "REJECTED": 0}

    print(f"\n{'ID':<25} {'Platform':<12} {'Type':<15} {'Status':<15}")
    print("-" * 70)

    for filepath in files:
        with open(filepath) as f:
            content = f.read()

        # Parse frontmatter
        status = "UNKNOWN"
        platform = "unknown"
        ctype = "unknown"

        for line in content.split('\n'):
            if line.startswith('status:'):
                status = line.split(':', 1)[1].strip()
            elif line.startswith('platform:'):
                platform = line.split(':', 1)[1].strip()
            elif line.startswith('content_type:'):
                ctype = line.split(':', 1)[1].strip()

        status_counts[status] = status_counts.get(status, 0) + 1
        print(f"{filepath.stem:<25} {platform:<12} {ctype:<15} {status:<15}")

    print("-" * 70)
    print(f"Total: {len(files)} | " + " | ".join(f"{k}: {v}" for k, v in status_counts.items() if v > 0))


def approve_content(content_id: str):
    """Approve content and move to posting queue."""
    files = list(QA_QUEUE_DIR.glob(f"{content_id}*.md"))
    if not files:
        print(f"No files found matching {content_id}")
        return

    approved = 0
    for filepath in files:
        with open(filepath) as f:
            content = f.read()

        content = content.replace("status: PENDING_REVIEW", "status: APPROVED")
        content = content.replace("status: NEEDS_EDIT", "status: APPROVED")

        with open(filepath, 'w') as f:
            f.write(content)
        approved += 1

    print(f"Approved {approved} content pieces matching {content_id}")

    # Add to posting queue
    _add_to_posting_queue(files)


def _add_to_posting_queue(files: List[Path]):
    """Add approved content to the posting queue CSV."""
    if not POSTING_QUEUE.exists():
        with open(POSTING_QUEUE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'content_id', 'platform', 'content_type', 'scheduled_time',
                'status', 'file_path', 'posted_at', 'post_url', 'notes'
            ])

    with open(POSTING_QUEUE, 'a', newline='') as f:
        writer = csv.writer(f)
        for filepath in files:
            # Parse metadata
            with open(filepath) as fh:
                content = fh.read()

            platform = "unknown"
            ctype = "unknown"
            for line in content.split('\n'):
                if line.startswith('platform:'):
                    platform = line.split(':', 1)[1].strip()
                elif line.startswith('content_type:'):
                    ctype = line.split(':', 1)[1].strip()

            writer.writerow([
                filepath.stem,
                platform,
                ctype,
                '',  # scheduled_time - to be filled
                'QUEUED',
                str(filepath),
                '',  # posted_at
                '',  # post_url
                ''   # notes
            ])


def reject_content(content_id: str, reason: str = ""):
    """Reject content."""
    files = list(QA_QUEUE_DIR.glob(f"{content_id}*.md"))
    if not files:
        print(f"No files found matching {content_id}")
        return

    for filepath in files:
        with open(filepath) as f:
            content = f.read()

        content = content.replace("status: PENDING_REVIEW", f"status: REJECTED")
        if reason:
            content = content.replace("notes:", f"notes: REJECTED - {reason}")

        with open(filepath, 'w') as f:
            f.write(content)

    print(f"Rejected {len(files)} content pieces matching {content_id}")


def pipeline_stats():
    """Show pipeline statistics."""
    files = list(QA_QUEUE_DIR.glob("*.md"))

    statuses = {"PENDING_REVIEW": 0, "APPROVED": 0, "NEEDS_EDIT": 0, "REJECTED": 0}
    platforms = {}

    for filepath in files:
        with open(filepath) as f:
            content = f.read()

        for line in content.split('\n'):
            if line.startswith('status:'):
                status = line.split(':', 1)[1].strip()
                statuses[status] = statuses.get(status, 0) + 1
            elif line.startswith('platform:'):
                platform = line.split(':', 1)[1].strip()
                platforms[platform] = platforms.get(platform, 0) + 1

    # Posting queue stats
    posted = 0
    queued = 0
    if POSTING_QUEUE.exists():
        with open(POSTING_QUEUE) as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('status') == 'POSTED':
                    posted += 1
                elif row.get('status') == 'QUEUED':
                    queued += 1

    print(f"\n=== Content Pipeline Stats ===\n")
    print(f"QA Queue: {len(files)} total")
    for status, count in statuses.items():
        if count > 0:
            print(f"  {status}: {count}")

    print(f"\nBy Platform:")
    for platform, count in sorted(platforms.items(), key=lambda x: -x[1]):
        print(f"  {platform}: {count}")

    print(f"\nPosting Queue:")
    print(f"  Queued: {queued}")
    print(f"  Posted: {posted}")


def main():
    parser = argparse.ArgumentParser(description='Content Repurposing Pipeline')
    subparsers = parser.add_subparsers(dest='command')

    # create
    sub_create = subparsers.add_parser('create', help='Create 15-output chain')
    sub_create.add_argument('--source', required=True, help='Source intel text')
    sub_create.add_argument('--category', required=True, help='Category (APP_FACTORY, etc)')
    sub_create.add_argument('--url', default='', help='Source URL')

    # queue
    subparsers.add_parser('queue', help='Show QA queue')

    # approve
    sub_approve = subparsers.add_parser('approve', help='Approve content')
    sub_approve.add_argument('content_id', help='Content ID to approve')

    # reject
    sub_reject = subparsers.add_parser('reject', help='Reject content')
    sub_reject.add_argument('content_id', help='Content ID to reject')
    sub_reject.add_argument('--reason', default='', help='Rejection reason')

    # stats
    subparsers.add_parser('stats', help='Pipeline statistics')

    # schedule
    subparsers.add_parser('schedule', help='Show posting schedule')

    args = parser.parse_args()

    if args.command == 'create':
        create_content_chain(args.source, args.category, args.url)
    elif args.command == 'queue':
        show_queue()
    elif args.command == 'approve':
        approve_content(args.content_id)
    elif args.command == 'reject':
        reject_content(args.content_id, getattr(args, 'reason', ''))
    elif args.command == 'stats':
        pipeline_stats()
    elif args.command == 'schedule':
        if POSTING_QUEUE.exists():
            with open(POSTING_QUEUE) as f:
                print(f.read())
        else:
            print("No posting queue yet. Create content first.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
