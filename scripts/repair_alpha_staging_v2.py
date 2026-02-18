#!/usr/bin/env python3
"""
Repair corrupted ALPHA_STAGING.csv file - Version 2.

Simpler approach: read line by line, parse with CSV reader,
handle errors gracefully, pad/truncate to fix column counts.

Usage:
    python3 scripts/repair_alpha_staging_v2.py
"""

import csv
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional


def validate_alpha_row(
    row_dict: Dict[str, str],
    existing_ids: Optional[Set[str]] = None,
    existing_urls: Optional[Set[str]] = None
) -> Tuple[bool, str]:
    """Validate an alpha row before insertion."""
    # Check alpha_id
    alpha_id = row_dict.get('alpha_id', '').strip()
    if not alpha_id:
        return False, "Missing alpha_id"
    if not re.match(r'^ALPHA\d+$', alpha_id):
        return False, f"Invalid alpha_id format: {alpha_id}"

    # Check for duplicate alpha_id
    if existing_ids is not None and alpha_id in existing_ids:
        return False, f"Duplicate alpha_id: {alpha_id}"

    # Check for duplicate source_url (if provided)
    source_url = row_dict.get('source_url', '').strip()
    if source_url and existing_urls is not None and source_url in existing_urls:
        return False, f"Duplicate source_url: {source_url}"

    # Must have status
    status = row_dict.get('status', '').strip()
    if not status:
        return False, "Missing status"

    return True, ""


def repair_csv_simple(input_path: Path, output_path: Path) -> Dict[str, int]:
    """
    Repair CSV using line-by-line approach.
    """
    print(f"Reading file: {input_path}")

    # Read header
    with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
        header_line = f.readline()
        reader = csv.reader([header_line])
        headers = next(reader)
        expected_cols = len(headers)

    print(f"Headers ({expected_cols} columns): {headers}")

    stats = {
        'total_lines': 0,
        'valid_rows': 0,
        'corrupted_fixed': 0,
        'duplicate_ids': 0,
        'duplicate_urls': 0,
        'parse_errors': 0,
        'final_count': 0
    }

    seen_ids: Set[str] = set()
    seen_urls: Set[str] = set()
    valid_rows: List[Dict[str, str]] = []

    # Read file line by line, handle errors manually
    with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
        # Skip header
        f.readline()

        line_num = 1
        while True:
            line = f.readline()
            if not line:
                break

            line_num += 1
            stats['total_lines'] += 1

            # Skip empty lines
            if not line.strip():
                continue

            # Try to parse with CSV reader
            try:
                reader = csv.reader([line], quoting=csv.QUOTE_MINIMAL)
                row = next(reader)

                # Fix column count
                if len(row) < expected_cols:
                    row.extend([''] * (expected_cols - len(row)))
                    stats['corrupted_fixed'] += 1
                elif len(row) > expected_cols:
                    row = row[:expected_cols]
                    stats['corrupted_fixed'] += 1

                # Create dict
                row_dict = dict(zip(headers, row))

                # Validate
                alpha_id = row_dict.get('alpha_id', '').strip()
                if not alpha_id or not re.match(r'^ALPHA\d+$', alpha_id):
                    # Not a valid row, skip
                    stats['parse_errors'] += 1
                    continue

                # Check duplicates
                if alpha_id in seen_ids:
                    stats['duplicate_ids'] += 1
                    continue

                source_url = row_dict.get('source_url', '').strip()
                if source_url and source_url in seen_urls:
                    stats['duplicate_urls'] += 1
                    continue

                # Add to valid rows
                valid_rows.append(row_dict)
                seen_ids.add(alpha_id)
                if source_url:
                    seen_urls.add(source_url)
                stats['valid_rows'] += 1

            except Exception as e:
                stats['parse_errors'] += 1
                if stats['parse_errors'] <= 10:  # Only print first 10
                    print(f"Parse error line {line_num}: {str(e)[:100]}")
                continue

    stats['final_count'] = len(valid_rows)

    # Write repaired file
    print(f"\nWriting repaired file to: {output_path}")
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(valid_rows)

    return stats


def main():
    """Main entry point."""
    project_root = Path(__file__).parent.parent
    input_path = project_root / 'LEDGER' / 'ALPHA_STAGING.csv'
    output_path = project_root / 'LEDGER' / 'ALPHA_STAGING_REPAIRED.csv'

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        return

    print("="*80)
    print("ALPHA_STAGING.csv Repair Script v2 - Simple Line-by-Line")
    print("="*80)

    stats = repair_csv_simple(input_path, output_path)

    print("\n" + "="*80)
    print("REPAIR COMPLETE")
    print("="*80)
    print(f"Total lines processed: {stats['total_lines']}")
    print(f"Valid rows: {stats['valid_rows']}")
    print(f"Corrupted rows fixed: {stats['corrupted_fixed']}")
    print(f"Parse errors: {stats['parse_errors']}")
    print(f"Duplicate IDs removed: {stats['duplicate_ids']}")
    print(f"Duplicate URLs removed: {stats['duplicate_urls']}")
    print(f"Final count: {stats['final_count']}")
    print(f"\nRepaired file saved to: {output_path}")
    print("="*80)

    if stats['total_lines'] > 0:
        corruption_pct = ((stats['corrupted_fixed'] + stats['parse_errors'] +
                          stats['duplicate_ids'] + stats['duplicate_urls']) /
                         stats['total_lines'] * 100)
        print(f"Issues resolved: {corruption_pct:.1f}%")

    print("\nNext steps:")
    print("1. Review the repaired file")
    print("2. If satisfied, backup and replace:")
    print("   mv LEDGER/ALPHA_STAGING.csv LEDGER/ALPHA_STAGING_BACKUP.csv")
    print("   mv LEDGER/ALPHA_STAGING_REPAIRED.csv LEDGER/ALPHA_STAGING.csv")


if __name__ == '__main__':
    main()
