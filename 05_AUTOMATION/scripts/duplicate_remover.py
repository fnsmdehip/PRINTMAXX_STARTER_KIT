#!/usr/bin/env python3
"""
duplicate_remover.py - Remove duplicate entries from LEDGER CSVs

Identifies and removes duplicates based on configurable matching rules:
- Exact match on key columns
- Fuzzy match on text content
- URL-based deduplication for alpha entries

Usage:
    python3 duplicate_remover.py --file LEDGER/ALPHA_STAGING.csv --key source_url
    python3 duplicate_remover.py --file LEDGER/ALPHA_STAGING.csv --key alpha_id
    python3 duplicate_remover.py --all --dry-run
    python3 duplicate_remover.py --file LEDGER/ALPHA_STAGING.csv --fuzzy --threshold 0.8

Example:
    # Find duplicates in ALPHA_STAGING by source_url
    python3 duplicate_remover.py --file LEDGER/ALPHA_STAGING.csv --key source_url --dry-run

    # Remove duplicates (keeps first occurrence)
    python3 duplicate_remover.py --file LEDGER/ALPHA_STAGING.csv --key source_url

    # Check all LEDGER files for duplicates
    python3 duplicate_remover.py --all --dry-run
"""

import argparse
import csv
import logging
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_DIR / "LEDGER"
LOG_DIR = PROJECT_DIR / "AUTOMATIONS" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "duplicate_remover.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Default dedup keys per file
DEFAULT_KEYS = {
    "ALPHA_STAGING.csv": "source_url",
    "ALPHA_STAGING_NEW.csv": "source_url",
    "MONEY_METHODS_TRACKER.csv": "method_id",
    "CONTENT_CALENDAR_2026.csv": None,
    "CONTENT_PIPELINE.csv": "ContentID",
    "HIGH_SIGNAL_SOURCES.csv": "handle",
    "CROSS_POLLINATION_MATRIX.csv": "method_id",
    "APP_CLONE_OPPORTUNITIES.csv": None,
    "OUTREACH_PIPELINE.csv": None,
}


def load_csv(filepath):
    """Load CSV file with fieldnames."""
    rows = []
    fieldnames = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for row in reader:
            rows.append(row)
    return rows, fieldnames


def find_duplicates(rows, key_column):
    """Find duplicate rows based on key column."""
    seen = {}
    duplicates = []
    unique = []

    for i, row in enumerate(rows):
        key_value = row.get(key_column, "").strip()
        if not key_value:
            unique.append(row)
            continue

        if key_value in seen:
            duplicates.append({
                "row_index": i,
                "key_value": key_value,
                "first_seen_at": seen[key_value],
                "row": row,
            })
        else:
            seen[key_value] = i
            unique.append(row)

    return unique, duplicates


def find_fuzzy_duplicates(rows, text_column="title", threshold=0.8):
    """Find fuzzy duplicates based on text similarity."""
    try:
        from difflib import SequenceMatcher
    except ImportError:
        logger.error("difflib not available")
        return rows, []

    duplicates = []
    keep_indices = set(range(len(rows)))

    for i in range(len(rows)):
        if i not in keep_indices:
            continue

        text_i = rows[i].get(text_column, "").lower().strip()
        if not text_i:
            continue

        for j in range(i + 1, len(rows)):
            if j not in keep_indices:
                continue

            text_j = rows[j].get(text_column, "").lower().strip()
            if not text_j:
                continue

            similarity = SequenceMatcher(None, text_i, text_j).ratio()
            if similarity >= threshold:
                keep_indices.discard(j)
                duplicates.append({
                    "row_index": j,
                    "similar_to": i,
                    "similarity": round(similarity, 3),
                    "text_kept": text_i[:60],
                    "text_removed": text_j[:60],
                })

    unique = [rows[i] for i in sorted(keep_indices)]
    return unique, duplicates


def remove_duplicates(filepath, key_column, dry_run=False, fuzzy=False, threshold=0.8):
    """Remove duplicates from a CSV file."""
    rows, fieldnames = load_csv(filepath)

    if fuzzy:
        unique, duplicates = find_fuzzy_duplicates(rows, key_column, threshold)
    else:
        unique, duplicates = find_duplicates(rows, key_column)

    logger.info(f"File: {filepath.name}")
    logger.info(f"Total rows: {len(rows)}")
    logger.info(f"Unique: {len(unique)}")
    logger.info(f"Duplicates: {len(duplicates)}")

    if duplicates:
        print(f"\n  Found {len(duplicates)} duplicate(s) in {filepath.name}:")
        for d in duplicates[:20]:
            if fuzzy:
                print(f"    Row {d['row_index']}: similarity {d['similarity']} to row {d['similar_to']}")
                print(f"      Kept:    {d['text_kept']}")
                print(f"      Removed: {d['text_removed']}")
            else:
                print(f"    Row {d['row_index']}: '{d['key_value']}' (first seen at row {d['first_seen_at']})")

        if len(duplicates) > 20:
            print(f"    ... and {len(duplicates) - 20} more")

    if dry_run:
        logger.info("DRY RUN - no changes made")
        return len(duplicates)

    if duplicates:
        # Write deduplicated file
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(unique)

        logger.info(f"Removed {len(duplicates)} duplicates from {filepath.name}")

    return len(duplicates)


def check_all_files(dry_run=True):
    """Check all known LEDGER files for duplicates."""
    total_dupes = 0

    for filename, default_key in DEFAULT_KEYS.items():
        filepath = LEDGER_DIR / filename
        if not filepath.exists():
            continue
        if not default_key:
            continue

        rows, fieldnames = load_csv(filepath)
        if default_key not in fieldnames:
            continue

        _, duplicates = find_duplicates(rows, default_key)
        if duplicates:
            total_dupes += len(duplicates)
            print(f"  {filename}: {len(duplicates)} duplicates on '{default_key}'")

    if total_dupes == 0:
        print("  No duplicates found in any tracked LEDGER file.")

    return total_dupes


def main():
    parser = argparse.ArgumentParser(
        description="Remove duplicate entries from LEDGER CSV files"
    )
    parser.add_argument("--file", type=str, default=None, help="CSV file to deduplicate")
    parser.add_argument("--key", type=str, default=None, help="Column to check for duplicates")
    parser.add_argument("--all", action="store_true", help="Check all LEDGER files")
    parser.add_argument("--dry-run", action="store_true", help="Preview without removing")
    parser.add_argument("--fuzzy", action="store_true", help="Use fuzzy matching")
    parser.add_argument("--threshold", type=float, default=0.8, help="Fuzzy match threshold (0-1)")
    args = parser.parse_args()

    if args.all:
        check_all_files(dry_run=True)
    elif args.file:
        filepath = Path(args.file)
        if not filepath.is_absolute():
            filepath = PROJECT_DIR / args.file

        if not filepath.exists():
            logger.error(f"File not found: {filepath}")
            sys.exit(1)

        key = args.key
        if not key:
            # Try default
            key = DEFAULT_KEYS.get(filepath.name)
            if not key:
                logger.error("No --key specified and no default for this file")
                sys.exit(1)

        remove_duplicates(filepath, key, dry_run=args.dry_run, fuzzy=args.fuzzy, threshold=args.threshold)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
