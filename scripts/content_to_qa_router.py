#!/usr/bin/env python3
"""
Content -> QA Queue Auto-Router (IR-009)
Scans content generation directories for new files and creates
QA queue entries in OPS/CONTENT_QA_QUEUE/.

Also runs automated copy-style checks before queuing.

Integration points:
- Reads: CONTENT/social/*, CONTENT/email_sequences/*, CONTENT/medium_articles/*,
         CONTENT/substack_posts/*, CONTENT/reddit/*, CONTENT/content_farm/*,
         MONEY_METHODS/CONTENT_FARM/NICHE_ACCOUNTS/generated_content/*
- Writes: OPS/CONTENT_QA_QUEUE/*.md (queue entries with metadata)
- Writes: LEDGER/CONTENT_QA_LOG.csv (tracking of all routed content)

Usage:
    python3 scripts/content_to_qa_router.py                # Route all unqueued content
    python3 scripts/content_to_qa_router.py --check-style   # Also run copy-style checks
    python3 scripts/content_to_qa_router.py --dry-run       # Show what would be routed
"""

import csv
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

PROJECT_DIR = Path(__file__).resolve().parent.parent
QA_QUEUE_DIR = PROJECT_DIR / "OPS" / "CONTENT_QA_QUEUE"
LEDGER_DIR = PROJECT_DIR / "LEDGER"

# Ensure directories exist
QA_QUEUE_DIR.mkdir(parents=True, exist_ok=True)

# Content directories to scan with platform/type mappings
CONTENT_DIRS = [
    {
        'path': PROJECT_DIR / "CONTENT" / "social" / "faith",
        'platform': 'x_twitter',
        'content_type': 'post',
        'niche': 'faith',
    },
    {
        'path': PROJECT_DIR / "CONTENT" / "social" / "fitness",
        'platform': 'x_twitter',
        'content_type': 'post',
        'niche': 'fitness',
    },
    {
        'path': PROJECT_DIR / "CONTENT" / "social" / "ai",
        'platform': 'x_twitter',
        'content_type': 'post',
        'niche': 'tech',
    },
    {
        'path': PROJECT_DIR / "CONTENT" / "social" / "ai_productivity",
        'platform': 'x_twitter',
        'content_type': 'post',
        'niche': 'tech',
    },
    {
        'path': PROJECT_DIR / "CONTENT" / "social" / "threads",
        'platform': 'x_twitter',
        'content_type': 'thread',
        'niche': 'general',
    },
    {
        'path': PROJECT_DIR / "CONTENT" / "social" / "carousels",
        'platform': 'instagram',
        'content_type': 'carousel',
        'niche': 'general',
    },
    {
        'path': PROJECT_DIR / "CONTENT" / "email_sequences" / "cold",
        'platform': 'email',
        'content_type': 'email_sequence',
        'niche': 'outbound',
    },
    {
        'path': PROJECT_DIR / "CONTENT" / "medium_articles",
        'platform': 'medium',
        'content_type': 'article',
        'niche': 'general',
    },
    {
        'path': PROJECT_DIR / "CONTENT" / "substack_posts",
        'platform': 'substack',
        'content_type': 'article',
        'niche': 'general',
    },
    {
        'path': PROJECT_DIR / "CONTENT" / "reddit",
        'platform': 'reddit',
        'content_type': 'post',
        'niche': 'general',
    },
    {
        'path': PROJECT_DIR / "CONTENT" / "content_farm",
        'platform': 'tiktok',
        'content_type': 'video_script',
        'niche': 'content_farm',
    },
    {
        'path': PROJECT_DIR / "MONEY_METHODS" / "CONTENT_FARM" / "NICHE_ACCOUNTS" / "generated_content",
        'platform': 'x_twitter',
        'content_type': 'post',
        'niche': 'content_farm',
    },
]

# Copy-style banned words (from .claude/rules/copy-style.md)
BANNED_WORDS = [
    'leverage', 'utilize', 'delve', 'comprehensive', 'robust',
    'innovative', 'seamless', 'game-changer', 'unlock', 'empower',
    'cutting-edge', 'additionally', 'moreover', 'furthermore',
    'testament', 'landscape', 'paradigm', 'streamlined',
    'revolutionary', 'groundbreaking', 'breathtaking',
]

BANNED_PATTERNS = [
    r"it's not just .+, it's",  # "It's not just X, it's Y"
    r'experts say',
    r'studies show',
    r'—',  # Em dash
]


def get_already_queued() -> set:
    """Get set of file paths already in QA queue."""
    log_file = LEDGER_DIR / "CONTENT_QA_LOG.csv"
    queued = set()

    if not log_file.exists():
        return queued

    try:
        with open(log_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                queued.add(row.get('source_file', ''))
    except Exception as e:
        print(f"Warning: Error reading QA log: {e}")

    return queued


def scan_content_dirs() -> List[Dict]:
    """Scan all content directories for new files."""
    new_files = []
    already_queued = get_already_queued()

    for dir_config in CONTENT_DIRS:
        dir_path = dir_config['path']
        if not dir_path.exists():
            continue

        # Scan for markdown files
        for file_path in dir_path.glob('*.md'):
            relative_path = str(file_path.relative_to(PROJECT_DIR))

            if relative_path in already_queued:
                continue

            # Skip index/readme files
            if file_path.name.lower() in ('index.md', 'readme.md', 'email_sequences_index.md'):
                continue

            new_files.append({
                'file_path': str(file_path),
                'relative_path': relative_path,
                'platform': dir_config['platform'],
                'content_type': dir_config['content_type'],
                'niche': dir_config['niche'],
                'filename': file_path.name,
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
            })

    # Sort by modification time, newest first
    new_files.sort(key=lambda x: x['modified'], reverse=True)

    return new_files


def check_copy_style(file_path: str) -> Tuple[bool, List[str]]:
    """Run automated copy-style checks on content file."""
    violations = []

    try:
        with open(file_path, 'r') as f:
            content = f.read().lower()
    except Exception as e:
        return False, [f"Could not read file: {e}"]

    # Check banned words
    for word in BANNED_WORDS:
        if word in content:
            violations.append(f"Banned word: '{word}'")

    # Check banned patterns
    for pattern in BANNED_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            violations.append(f"Banned pattern: '{pattern}'")

    passes = len(violations) == 0
    return passes, violations


def suggest_posting_time(platform: str, niche: str) -> str:
    """Suggest optimal posting time based on platform and niche."""
    # Based on platform algorithm research
    time_map = {
        'x_twitter': {
            'faith': '06:00 EST',
            'fitness': '07:00 EST',
            'tech': '09:00 EST',
            'general': '08:00 EST',
            'content_farm': '12:00 EST',
            'outbound': 'N/A',
        },
        'instagram': {
            'default': '11:00 EST',
        },
        'tiktok': {
            'default': '19:00 EST',
        },
        'medium': {
            'default': '08:00 EST Tuesday',
        },
        'substack': {
            'default': '10:00 EST Tuesday',
        },
        'reddit': {
            'default': '09:00 EST',
        },
        'email': {
            'default': '09:30 EST Tuesday',
        },
    }

    platform_times = time_map.get(platform, {'default': '09:00 EST'})
    return platform_times.get(niche, platform_times.get('default', '09:00 EST'))


def create_qa_entry(file_info: Dict, style_passes: bool, violations: List[str]) -> str:
    """Create a QA queue markdown file."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    suggested_time = suggest_posting_time(file_info['platform'], file_info['niche'])

    status = 'PENDING_REVIEW'
    if not style_passes:
        status = 'NEEDS_STYLE_FIX'

    # Generate a clean queue filename
    safe_name = file_info['filename'].replace('.md', '').replace(' ', '_')
    queue_filename = f"QA_{now[:10]}_{safe_name}.md"
    queue_path = QA_QUEUE_DIR / queue_filename

    content = f"""---
platform: {file_info['platform']}
content_type: {file_info['content_type']}
niche: {file_info['niche']}
source_file: {file_info['relative_path']}
suggested_time: {suggested_time}
status: {status}
routed_date: {now}
style_check_passed: {style_passes}
---

# QA Review: {file_info['filename']}

**Platform:** {file_info['platform']}
**Content Type:** {file_info['content_type']}
**Niche:** {file_info['niche']}
**Source File:** `{file_info['relative_path']}`
**Suggested Post Time:** {suggested_time}
**Status:** {status}
"""

    if violations:
        content += f"""
## Copy Style Violations (FIX BEFORE PUBLISHING)
"""
        for v in violations:
            content += f"- {v}\n"

    content += f"""
## Review Checklist
- [ ] Content matches PRINTMAXXER voice (@pipelineabuser energy)
- [ ] No AI vocabulary (leverage, utilize, delve, etc.)
- [ ] No em dashes
- [ ] Consequence-first hook
- [ ] Specific numbers included
- [ ] Would @pipelineabuser actually post this?
- [ ] FTC compliant (disclosures if needed)

## Actions
- **APPROVED**: Move to posting queue
- **NEEDS_EDIT**: Note edits needed below
- **REJECTED**: Note reason below

## Notes
(Human reviewer: add notes here)

"""

    with open(queue_path, 'w') as f:
        f.write(content)

    return str(queue_path)


def log_routing(file_info: Dict, queue_path: str, style_passes: bool) -> None:
    """Log the routing to CONTENT_QA_LOG.csv."""
    log_file = LEDGER_DIR / "CONTENT_QA_LOG.csv"
    file_exists = log_file.exists()

    with open(log_file, 'a', newline='') as f:
        fieldnames = [
            'source_file', 'queue_file', 'platform', 'content_type',
            'niche', 'style_check_passed', 'status', 'routed_date',
            'reviewed_date', 'review_decision'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'source_file': file_info['relative_path'],
            'queue_file': str(Path(queue_path).relative_to(PROJECT_DIR)),
            'platform': file_info['platform'],
            'content_type': file_info['content_type'],
            'niche': file_info['niche'],
            'style_check_passed': style_passes,
            'status': 'PENDING_REVIEW' if style_passes else 'NEEDS_STYLE_FIX',
            'routed_date': datetime.now().isoformat(),
            'reviewed_date': '',
            'review_decision': '',
        })


def main():
    parser = argparse.ArgumentParser(
        description='Route generated content to QA queue'
    )
    parser.add_argument(
        '--check-style', action='store_true',
        help='Run copy-style checks on content'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Show what would be routed without creating queue entries'
    )
    parser.add_argument(
        '--limit', type=int, default=None,
        help='Limit number of files to process'
    )

    args = parser.parse_args()

    print(f"Content -> QA Router - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

    # Scan for new content
    new_files = scan_content_dirs()
    print(f"Found {len(new_files)} unqueued content files")

    if not new_files:
        print("All content already in QA queue.")
        return

    if args.limit:
        new_files = new_files[:args.limit]
        print(f"Processing first {args.limit} files")

    routed = 0
    style_failures = 0

    for file_info in new_files:
        # Run style check
        style_passes = True
        violations = []

        if args.check_style:
            style_passes, violations = check_copy_style(file_info['file_path'])
            if not style_passes:
                style_failures += 1

        if args.dry_run:
            status = "PASS" if style_passes else f"FAIL ({len(violations)} violations)"
            print(f"  Would route: {file_info['relative_path']} -> {file_info['platform']} [{status}]")
            continue

        # Create QA entry
        queue_path = create_qa_entry(file_info, style_passes, violations)

        # Log the routing
        log_routing(file_info, queue_path, style_passes)

        status_str = "PENDING_REVIEW" if style_passes else "NEEDS_STYLE_FIX"
        print(f"  Routed: {file_info['relative_path']} -> {status_str}")
        routed += 1

    # Summary
    print("\n" + "=" * 50)
    print("CONTENT ROUTING SUMMARY")
    print("=" * 50)
    print(f"Files scanned: {len(new_files)}")
    print(f"Files routed: {routed}")
    if args.check_style:
        print(f"Style check failures: {style_failures}")
    if args.dry_run:
        print("MODE: DRY RUN (no files created)")
    print(f"QA Queue: {QA_QUEUE_DIR}")
    print("=" * 50)


if __name__ == "__main__":
    main()
