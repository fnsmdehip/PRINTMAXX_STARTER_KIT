#!/usr/bin/env python3
"""
PRINTMAXX Log Rotator — Keep logs under control.

Rotates logs by size (>1MB → archive), compresses old archives,
and prunes archives older than 30 days. Designed for cron.

Usage:
    python3 AUTOMATIONS/log_rotator.py                # dry-run (show what would happen)
    python3 AUTOMATIONS/log_rotator.py --rotate        # actually rotate
    python3 AUTOMATIONS/log_rotator.py --status        # show log sizes
    python3 AUTOMATIONS/log_rotator.py --prune 30      # delete archives older than N days

Cron:
    0 4 * * * cd $BASE && $PYTHON AUTOMATIONS/log_rotator.py --rotate >> AUTOMATIONS/logs/log_rotator.log 2>&1
"""

from __future__ import annotations

import argparse
import gzip
import os
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"
ARCHIVE_DIR = LOG_DIR / "archive"

# Rotate any log file larger than this (bytes)
ROTATE_THRESHOLD = 1_000_000  # 1 MB

# Never rotate these (they're append-only journals we want to keep intact)
SKIP_FILES = {"log_rotator.log"}

# Overnight logs — these are date-stamped already, just compress old ones
DATED_PATTERN = "overnight_"


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def get_log_files() -> list[Path]:
    """Get all .log files in the logs directory."""
    if not LOG_DIR.exists():
        return []
    return sorted(LOG_DIR.glob("*.log"))


def human_size(b: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if b < 1024:
            return f"{b:.1f}{unit}"
        b /= 1024
    return f"{b:.1f}TB"


def show_status():
    """Show current log sizes."""
    logs = get_log_files()
    if not logs:
        print("No log files found.")
        return

    total = 0
    over_threshold = 0
    print(f"\n{'='*60}")
    print(f"  LOG STATUS — {len(logs)} files in {LOG_DIR.relative_to(PROJECT_ROOT)}")
    print(f"{'='*60}\n")

    for lf in sorted(logs, key=lambda p: p.stat().st_size, reverse=True):
        size = lf.stat().st_size
        total += size
        marker = " ** ROTATE" if size > ROTATE_THRESHOLD and lf.name not in SKIP_FILES else ""
        if size > ROTATE_THRESHOLD:
            over_threshold += 1
        age_days = (datetime.now().timestamp() - lf.stat().st_mtime) / 86400
        print(f"  {human_size(size):>8}  {age_days:5.1f}d  {lf.name}{marker}")

    # Check archive dir
    archive_count = 0
    archive_size = 0
    if ARCHIVE_DIR.exists():
        for af in ARCHIVE_DIR.iterdir():
            archive_count += 1
            archive_size += af.stat().st_size

    print(f"\n  Total: {human_size(total)} across {len(logs)} active logs")
    print(f"  Over threshold (>{human_size(ROTATE_THRESHOLD)}): {over_threshold}")
    if archive_count:
        print(f"  Archive: {archive_count} files, {human_size(archive_size)}")
    print()


def rotate_logs(dry_run: bool = True) -> int:
    """Rotate logs over the threshold. Returns count of rotated files."""
    logs = get_log_files()
    rotated = 0
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    safe_path(ARCHIVE_DIR)
    if not dry_run:
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    for lf in logs:
        if lf.name in SKIP_FILES:
            continue
        size = lf.stat().st_size
        if size <= ROTATE_THRESHOLD:
            continue

        stem = lf.stem
        archive_name = f"{stem}_{ts}.log.gz"
        archive_path = ARCHIVE_DIR / archive_name

        if dry_run:
            print(f"  [DRY RUN] Would rotate {lf.name} ({human_size(size)}) → archive/{archive_name}")
        else:
            # Compress to archive
            with open(lf, "rb") as f_in:
                with gzip.open(safe_path(archive_path), "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            # Truncate original (keep the file for cron to append to)
            with open(lf, "w") as f:
                f.write(f"# Rotated at {ts}. Previous content archived to archive/{archive_name}\n")
            print(f"  Rotated {lf.name} ({human_size(size)}) → archive/{archive_name}")
        rotated += 1

    # Also compress old overnight logs (date-stamped, >7 days old)
    for lf in logs:
        if not lf.name.startswith(DATED_PATTERN):
            continue
        age_days = (datetime.now().timestamp() - lf.stat().st_mtime) / 86400
        if age_days < 7:
            continue
        size = lf.stat().st_size
        if size == 0:
            continue

        archive_name = f"{lf.stem}.log.gz"
        archive_path = ARCHIVE_DIR / archive_name

        if archive_path.exists():
            continue  # Already archived

        if dry_run:
            print(f"  [DRY RUN] Would archive old overnight {lf.name} ({human_size(size)}, {age_days:.0f}d old)")
        else:
            if not dry_run:
                ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
            with open(lf, "rb") as f_in:
                with gzip.open(safe_path(archive_path), "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            lf.unlink()
            print(f"  Archived overnight {lf.name} ({human_size(size)}, {age_days:.0f}d old)")
        rotated += 1

    return rotated


def prune_archives(max_age_days: int = 30, dry_run: bool = True) -> int:
    """Delete archives older than max_age_days."""
    if not ARCHIVE_DIR.exists():
        print("No archive directory found.")
        return 0

    pruned = 0
    cutoff = datetime.now().timestamp() - (max_age_days * 86400)

    for af in sorted(ARCHIVE_DIR.iterdir()):
        if af.stat().st_mtime < cutoff:
            size = af.stat().st_size
            if dry_run:
                print(f"  [DRY RUN] Would delete {af.name} ({human_size(size)})")
            else:
                af.unlink()
                print(f"  Deleted {af.name} ({human_size(size)})")
            pruned += 1

    return pruned


def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Log Rotator")
    parser.add_argument("--status", action="store_true", help="Show log sizes")
    parser.add_argument("--rotate", action="store_true", help="Rotate oversized logs")
    parser.add_argument("--prune", type=int, metavar="DAYS", help="Delete archives older than N days")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen (default when no flag)")
    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.rotate:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running log rotation...")
        count = rotate_logs(dry_run=False)
        print(f"  Rotated {count} files.")
        if args.prune:
            pruned = prune_archives(args.prune, dry_run=False)
            print(f"  Pruned {pruned} old archives.")
    elif args.prune is not None:
        print(f"\nPruning archives older than {args.prune} days...")
        pruned = prune_archives(args.prune, dry_run=False)
        print(f"  Pruned {pruned} archives.")
    else:
        # Default: dry-run showing what would happen
        show_status()
        print("DRY RUN — what rotation would do:")
        count = rotate_logs(dry_run=True)
        if count == 0:
            print("  Nothing to rotate.")
        print("\nRun with --rotate to actually rotate logs.")


if __name__ == "__main__":
    main()
