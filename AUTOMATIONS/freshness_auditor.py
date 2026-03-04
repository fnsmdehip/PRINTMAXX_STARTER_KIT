#!/usr/bin/env python3
"""
PRINTMAXX Freshness Auditor — Flag stale alpha entries.

Scans ALPHA_STAGING.csv for entries older than N days and marks them
as NEEDS_REVALIDATION. Helps prevent building on dead tactics.

Usage:
    python3 AUTOMATIONS/freshness_auditor.py              # default: flag entries >30 days old
    python3 AUTOMATIONS/freshness_auditor.py --days 14    # custom threshold
    python3 AUTOMATIONS/freshness_auditor.py --report     # show stale entries without modifying
    python3 AUTOMATIONS/freshness_auditor.py --prune      # archive INVALIDATED entries

Cron:
    30 2 * * 0 cd $BASE && $PYTHON AUTOMATIONS/freshness_auditor.py >> AUTOMATIONS/logs/freshness.log 2>&1
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ALPHA_FILE = PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv"
ARCHIVE_FILE = PROJECT_ROOT / "LEDGER" / "ALPHA_ARCHIVED.csv"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def load_alpha() -> list[dict]:
    safe_path(ALPHA_FILE)
    if not ALPHA_FILE.exists():
        print("No ALPHA_STAGING.csv found.")
        return []
    with open(ALPHA_FILE, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_alpha(rows: list[dict], path: Path):
    safe_path(path)
    if not rows:
        return
    fieldnames = rows[0].keys()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_date(date_str: str) -> datetime | None:
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None


def audit_freshness(rows: list[dict], max_age_days: int) -> tuple[list[dict], int]:
    cutoff = datetime.now() - timedelta(days=max_age_days)
    flagged = 0
    for row in rows:
        date_str = row.get("date") or row.get("created_at") or row.get("discovered_date") or ""
        entry_date = parse_date(date_str)
        if entry_date and entry_date < cutoff:
            status = row.get("status", "")
            if status in ("APPROVED", "PENDING_REVIEW"):
                row["status"] = "NEEDS_REVALIDATION"
                flagged += 1
    return rows, flagged


def report_stale(rows: list[dict], max_age_days: int):
    cutoff = datetime.now() - timedelta(days=max_age_days)
    stale = []
    for row in rows:
        date_str = row.get("date") or row.get("created_at") or row.get("discovered_date") or ""
        entry_date = parse_date(date_str)
        if entry_date and entry_date < cutoff:
            status = row.get("status", "")
            if status in ("APPROVED", "PENDING_REVIEW", "NEEDS_REVALIDATION"):
                age = (datetime.now() - entry_date).days
                stale.append((row.get("alpha_id", "?"), row.get("source", "?"), status, age, row.get("title", row.get("summary", ""))[:60]))

    if not stale:
        print(f"No entries older than {max_age_days} days need attention.")
        return

    print(f"\n{'='*70}")
    print(f"  FRESHNESS REPORT — {len(stale)} entries older than {max_age_days} days")
    print(f"{'='*70}\n")
    print(f"  {'ID':<12} {'Age':>5}  {'Status':<22} {'Source':<20} Title")
    print(f"  {'-'*10}  {'-'*4}  {'-'*20}  {'-'*18}  {'-'*30}")
    for alpha_id, source, status, age, title in sorted(stale, key=lambda x: -x[3]):
        print(f"  {alpha_id:<12} {age:>4}d  {status:<22} {source:<20} {title}")
    print()


def prune_invalidated(rows: list[dict]) -> tuple[list[dict], int]:
    keep = []
    archived = []
    for row in rows:
        if row.get("status") == "INVALIDATED":
            archived.append(row)
        else:
            keep.append(row)

    if archived:
        if ARCHIVE_FILE.exists():
            existing = []
            with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
                existing = list(csv.DictReader(f))
            archived = existing + archived
        save_alpha(archived, ARCHIVE_FILE)

    return keep, len(archived)


def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Freshness Auditor")
    parser.add_argument("--days", type=int, default=30, help="Flag entries older than N days (default: 30)")
    parser.add_argument("--report", action="store_true", help="Show stale entries without modifying")
    parser.add_argument("--prune", action="store_true", help="Archive INVALIDATED entries")
    args = parser.parse_args()

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{ts}] Freshness Auditor running (threshold: {args.days} days)...")

    rows = load_alpha()
    if not rows:
        print("  No alpha entries to audit.")
        return

    print(f"  Loaded {len(rows)} alpha entries.")

    if args.report:
        report_stale(rows, args.days)
        return

    if args.prune:
        rows, pruned = prune_invalidated(rows)
        if pruned:
            save_alpha(rows, ALPHA_FILE)
            print(f"  Archived {pruned} INVALIDATED entries to {ARCHIVE_FILE.name}")
        else:
            print("  No INVALIDATED entries to prune.")
        return

    # Default: flag stale entries
    rows, flagged = audit_freshness(rows, args.days)
    if flagged:
        save_alpha(rows, ALPHA_FILE)
        print(f"  Flagged {flagged} entries as NEEDS_REVALIDATION (>{args.days} days old).")
    else:
        print(f"  No entries need revalidation (all within {args.days} days).")

    # Always show report after flagging
    report_stale(rows, args.days)


if __name__ == "__main__":
    main()
