#!/usr/bin/env python3
"""Aggressive deduplication for high-volume CSVs"""

import csv
import shutil
from pathlib import Path
from datetime import datetime
import hashlib

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_ROOT / "LEDGER"

def hash_row(row):
    """Create hash of row content for exact deduplication"""
    content = str(sorted(row.items()))
    return hashlib.md5(content.encode()).hexdigest()

def deduplicate_csv(csv_file, key_cols=None):
    """Aggressively deduplicate a CSV file"""
    try:
        # Read all rows
        rows = []
        with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                return 0
            fieldnames = reader.fieldnames
            rows = list(reader)

        if not rows:
            return 0

        # Find duplicates by content hash
        seen_hashes = {}
        unique_rows = []
        dupes = 0

        # Sort by timestamp (newest first) if available
        if 'timestamp' in fieldnames:
            rows = sorted(rows, key=lambda r: r.get('timestamp', ''), reverse=True)

        for row in rows:
            row_hash = hash_row(row)
            if row_hash not in seen_hashes:
                seen_hashes[row_hash] = True
                unique_rows.append(row)
            else:
                dupes += 1

        if dupes > 0:
            # Backup
            backup = csv_file.with_stem(csv_file.stem + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            shutil.copy(csv_file, backup)

            # Write deduplicated
            with open(csv_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(unique_rows)

            print(f"  {csv_file.name}: {dupes} duplicates removed (kept {len(unique_rows)})")
            return dupes

        return 0

    except Exception as e:
        print(f"  ERROR {csv_file.name}: {str(e)}")
        return 0

def run_dedup():
    """Run aggressive deduplication on high-volume files"""
    print("Running aggressive deduplication on high-volume CSVs...\n")

    # Target the largest CSVs
    priority_files = [
        "ALPHA_STAGING.csv",
        "COMPETITIVE_INTEL.csv",
        "USER_PROMPTS.jsonl",  # Will skip if not CSV
        "OPPORTUNITY_MASTER.csv",
        "LEAD_MASTER.csv",
        "ENGAGEMENT_METRICS.csv",
    ]

    total_removed = 0

    for filename in priority_files:
        csv_file = LEDGER_DIR / filename
        if csv_file.exists() and csv_file.suffix == '.csv':
            removed = deduplicate_csv(csv_file)
            total_removed += removed

    # Also scan all CSVs with >5000 lines
    print("\nScanning large CSVs (>5000 lines)...")
    csv_files = list(LEDGER_DIR.glob("*.csv"))

    for csv_file in csv_files:
        try:
            with open(csv_file, 'r') as f:
                line_count = sum(1 for _ in f) - 1  # Subtract header

            if line_count > 5000:
                removed = deduplicate_csv(csv_file)
                total_removed += removed
        except:
            pass

    print(f"\n✓ Total duplicates removed: {total_removed}")
    return total_removed

if __name__ == "__main__":
    run_dedup()
