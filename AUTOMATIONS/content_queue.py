#!/usr/bin/env python3
"""
PRINTMAXX Content Queue Manager
================================
Consolidates auto-generated content from multiple pipelines into a unified
posting queue. Reads from:
  - content_trend_pipeline.py output (trends_*.csv)
  - tweet_auto_drafter.py output (tweets_*.csv)
  - daily_research_pipeline.py output (auto_content_*.csv)
  - alpha_content markdown files (alpha_content_*.md)

Provides a single interface to see what's ready to post, mark items as posted,
and export batches for Buffer/Publer/Typefully upload.

Usage:
    python3 AUTOMATIONS/content_queue.py --status                     # queue stats
    python3 AUTOMATIONS/content_queue.py --next 10                    # show top 10 ready
    python3 AUTOMATIONS/content_queue.py --next 10 --account PRINTMAXXER  # filter by account
    python3 AUTOMATIONS/content_queue.py --export-buffer 20           # export 20 for Buffer CSV
    python3 AUTOMATIONS/content_queue.py --consolidate                # rebuild master queue
    python3 AUTOMATIONS/content_queue.py --mark-posted ID1 ID2       # mark items posted

Cron:
    0 */4 * * * cd $BASE && $PYTHON AUTOMATIONS/content_queue.py --consolidate >> AUTOMATIONS/logs/content_queue.log 2>&1
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTO_GEN_DIR = PROJECT_ROOT / "CONTENT" / "social" / "auto_generated"
QUEUE_CSV = PROJECT_ROOT / "CONTENT" / "social" / "CONTENT_QUEUE.csv"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"
EXPORT_DIR = PROJECT_ROOT / "CONTENT" / "social" / "exports"


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, file=sys.stderr)
    safe_path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_DIR / "content_queue.log"), "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# Queue schema
# ---------------------------------------------------------------------------
QUEUE_FIELDS = [
    "queue_id",       # unique hash-based ID
    "account",        # @PRINTMAXXER, @repscheme, etc.
    "content",        # the tweet/post text
    "source_pipeline", # trend_pipeline, tweet_drafter, research_pipeline
    "source_file",    # original CSV filename
    "source_alpha_id", # if from alpha
    "relevance",      # score if available
    "status",         # PENDING_REVIEW, READY, POSTED, REJECTED
    "created_at",     # when generated
    "posted_at",      # when marked posted
]


def content_hash(account: str, content: str) -> str:
    """Generate a short unique ID from account + content for dedup."""
    h = hashlib.md5(f"{account}:{content}".encode()).hexdigest()[:8]
    return f"CQ-{h}"


# ---------------------------------------------------------------------------
# Ingest from different pipeline formats
# ---------------------------------------------------------------------------
def ingest_trend_csv(csv_path: Path) -> list[dict]:
    """Read trends_*.csv format: account,draft,source_type,source_handle,relevance,generated_at,status"""
    items = []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            account = (row.get("account") or "").strip()
            content = (row.get("draft") or "").strip()
            if not account or not content:
                continue
            items.append({
                "account": account,
                "content": content,
                "source_pipeline": "trend_pipeline",
                "source_file": csv_path.name,
                "source_alpha_id": "",
                "relevance": row.get("relevance", ""),
                "status": row.get("status", "PENDING_REVIEW"),
                "created_at": row.get("generated_at", ""),
                "posted_at": "",
            })
    return items


def ingest_tweet_csv(csv_path: Path) -> list[dict]:
    """Read tweets_*.csv format: tweet_text,source_alpha_id,account,status,created_date"""
    items = []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            account = (row.get("account") or "").strip()
            content = (row.get("tweet_text") or "").strip()
            if not account or not content:
                continue
            items.append({
                "account": account,
                "content": content,
                "source_pipeline": "tweet_drafter",
                "source_file": csv_path.name,
                "source_alpha_id": row.get("source_alpha_id", ""),
                "relevance": "",
                "status": row.get("status", "PENDING_REVIEW"),
                "created_at": row.get("created_date", ""),
                "posted_at": "",
            })
    return items


def ingest_auto_content_csv(csv_path: Path) -> list[dict]:
    """Read auto_content_*.csv format: niche,platform,content,source_alpha,category,status,generated_at"""
    items = []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            niche = (row.get("niche") or "").strip().lower()
            content = (row.get("content") or "").strip()
            if not niche or not content:
                continue
            # Map niche names to account handles
            niche_to_account = {
                "printmaxxer": "@PRINTMAXXER",
                "faith": "@selahmoments",
                "fitness": "@repscheme",
                "tech": "@PRINTMAXXER",
                "aesthetic": "@drifthour",
                "esoteric": "@voidpilled",
            }
            account = niche_to_account.get(niche, f"@{niche}")
            items.append({
                "account": account,
                "content": content,
                "source_pipeline": "research_pipeline",
                "source_file": csv_path.name,
                "source_alpha_id": row.get("source_alpha", ""),
                "relevance": "",
                "status": row.get("status", "PENDING_REVIEW"),
                "created_at": row.get("generated_at", ""),
                "posted_at": "",
            })
    return items


# ---------------------------------------------------------------------------
# Consolidation
# ---------------------------------------------------------------------------
def load_existing_queue() -> dict[str, dict]:
    """Load existing queue by queue_id for dedup."""
    existing = {}
    queue_path = safe_path(QUEUE_CSV)
    if queue_path.exists():
        with open(queue_path, "r", newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                qid = row.get("queue_id", "")
                if qid:
                    existing[qid] = row
    return existing


def consolidate() -> int:
    """Scan auto_generated dir and add new items to the master queue."""
    existing = load_existing_queue()
    new_count = 0
    auto_dir = safe_path(AUTO_GEN_DIR)
    if not auto_dir.exists():
        log("Auto-generated content directory not found")
        return 0

    all_items = []

    for csv_file in sorted(auto_dir.glob("*.csv")):
        name = csv_file.name
        try:
            if name.startswith("trends_"):
                all_items.extend(ingest_trend_csv(csv_file))
            elif name.startswith("tweets_"):
                all_items.extend(ingest_tweet_csv(csv_file))
            elif name.startswith("auto_content_"):
                all_items.extend(ingest_auto_content_csv(csv_file))
        except Exception as e:
            log(f"Error reading {name}: {e}")

    # Assign queue IDs and dedup
    for item in all_items:
        qid = content_hash(item["account"], item["content"])
        if qid not in existing:
            item["queue_id"] = qid
            existing[qid] = item
            new_count += 1

    # Write back
    queue_path = safe_path(QUEUE_CSV)
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    with open(queue_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=QUEUE_FIELDS)
        writer.writeheader()
        for row in existing.values():
            writer.writerow({k: row.get(k, "") for k in QUEUE_FIELDS})

    log(f"Consolidation complete: {new_count} new items, {len(existing)} total")
    return new_count


# ---------------------------------------------------------------------------
# Query commands
# ---------------------------------------------------------------------------
def show_status():
    """Print queue stats."""
    existing = load_existing_queue()
    if not existing:
        print("Content queue is empty. Run --consolidate first.")
        return

    # Count by status
    status_counts = {}
    account_counts = {}
    pipeline_counts = {}
    for row in existing.values():
        s = row.get("status", "UNKNOWN")
        a = row.get("account", "UNKNOWN")
        p = row.get("source_pipeline", "UNKNOWN")
        status_counts[s] = status_counts.get(s, 0) + 1
        account_counts[a] = account_counts.get(a, 0) + 1
        pipeline_counts[p] = pipeline_counts.get(p, 0) + 1

    print(f"\n{'='*60}")
    print(f"  CONTENT QUEUE STATUS — {len(existing)} total items")
    print(f"{'='*60}\n")

    print("  By Status:")
    for s, c in sorted(status_counts.items(), key=lambda x: -x[1]):
        print(f"    {s:<20} {c:>5}")

    print("\n  By Account:")
    for a, c in sorted(account_counts.items(), key=lambda x: -x[1]):
        print(f"    {a:<20} {c:>5}")

    print("\n  By Pipeline:")
    for p, c in sorted(pipeline_counts.items(), key=lambda x: -x[1]):
        print(f"    {p:<20} {c:>5}")
    print()


def show_next(count: int = 10, account: str | None = None):
    """Show the top N items ready to post."""
    existing = load_existing_queue()
    ready = []
    for row in existing.values():
        if row.get("status") in ("PENDING_REVIEW", "READY"):
            if account and account.lower() not in (row.get("account") or "").lower():
                continue
            ready.append(row)

    # Sort by relevance (higher first), then by created_at (newer first)
    def sort_key(r):
        try:
            rel = float(r.get("relevance") or 0)
        except (ValueError, TypeError):
            rel = 0
        return (-rel, r.get("created_at", ""))

    ready.sort(key=sort_key)
    batch = ready[:count]

    if not batch:
        print("No items ready to post.")
        return

    acct_filter = f" for {account}" if account else ""
    print(f"\n{'='*60}")
    print(f"  NEXT {len(batch)} POSTS{acct_filter}")
    print(f"{'='*60}\n")

    for i, item in enumerate(batch, 1):
        content = item.get("content", "")
        # Truncate for display
        display = content[:120] + "..." if len(content) > 120 else content
        display = display.replace("\n", " ")
        print(f"  [{i}] {item.get('queue_id', '???')} | {item.get('account', '???')}")
        print(f"      {display}")
        print(f"      src: {item.get('source_pipeline', '?')} | alpha: {item.get('source_alpha_id', '-')}")
        print()


def export_buffer(count: int = 20, account: str | None = None):
    """Export items as a Buffer-compatible CSV."""
    existing = load_existing_queue()
    ready = []
    for row in existing.values():
        if row.get("status") in ("PENDING_REVIEW", "READY"):
            if account and account.lower() not in (row.get("account") or "").lower():
                continue
            ready.append(row)

    if not ready:
        print("No items to export.")
        return

    batch = ready[:count]
    export_path = safe_path(EXPORT_DIR)
    export_path.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    acct_slug = account.lower().lstrip("@") if account else "all"
    filename = f"buffer_export_{acct_slug}_{ts}.csv"
    filepath = export_path / filename

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Text"])  # Buffer CSV format
        for item in batch:
            writer.writerow([item.get("content", "")])

    print(f"Exported {len(batch)} posts to {filepath}")


def mark_posted(queue_ids: list[str]):
    """Mark queue items as POSTED."""
    existing = load_existing_queue()
    updated = 0
    ts = datetime.now().isoformat()
    for qid in queue_ids:
        if qid in existing:
            existing[qid]["status"] = "POSTED"
            existing[qid]["posted_at"] = ts
            updated += 1
        else:
            log(f"Queue ID not found: {qid}")

    # Write back
    queue_path = safe_path(QUEUE_CSV)
    with open(queue_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=QUEUE_FIELDS)
        writer.writeheader()
        for row in existing.values():
            writer.writerow({k: row.get(k, "") for k in QUEUE_FIELDS})

    log(f"Marked {updated} items as POSTED")
    print(f"Marked {updated} items as POSTED")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Content Queue Manager")
    parser.add_argument("--status", action="store_true", help="Show queue statistics")
    parser.add_argument("--next", type=int, metavar="N", help="Show next N items to post")
    parser.add_argument("--account", type=str, help="Filter by account handle")
    parser.add_argument("--consolidate", action="store_true", help="Scan auto_generated and rebuild queue")
    parser.add_argument("--export-buffer", type=int, metavar="N", help="Export N items as Buffer CSV")
    parser.add_argument("--mark-posted", nargs="+", metavar="ID", help="Mark queue IDs as POSTED")

    args = parser.parse_args()

    if args.consolidate:
        consolidate()
    elif args.status:
        show_status()
    elif args.next:
        show_next(args.next, args.account)
    elif args.export_buffer:
        export_buffer(args.export_buffer, args.account)
    elif args.mark_posted:
        mark_posted(args.mark_posted)
    else:
        # Default: consolidate + status
        consolidate()
        show_status()


if __name__ == "__main__":
    main()
