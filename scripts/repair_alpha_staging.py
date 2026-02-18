#!/usr/bin/env python3
"""
Repair corrupted ALPHA_STAGING.csv file.

Fixes:
- Unescaped multi-line content in CSV fields
- Broken rows that span multiple lines
- Duplicate alpha_ids
- Duplicate source_urls
- Validates column count

Usage:
    python3 scripts/repair_alpha_staging.py
"""

import csv
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional


def validate_alpha_row(
    row_dict: Dict[str, str],
    existing_ids: Optional[Set[str]] = None,
    existing_urls: Optional[Set[str]] = None,
    lenient: bool = False
) -> Tuple[bool, str]:
    """
    Validate an alpha row before insertion.

    Args:
        row_dict: Dictionary with alpha entry fields
        existing_ids: Set of existing alpha_ids to check for duplicates
        existing_urls: Set of existing source_urls to check for duplicates
        lenient: If True, only require alpha_id and status (repair mode)

    Returns:
        (is_valid, error_message) tuple
    """
    # Check required fields (lenient mode only requires alpha_id and status)
    if lenient:
        required_fields = ['alpha_id', 'status']
    else:
        required_fields = ['alpha_id', 'source', 'category', 'status']

    for field in required_fields:
        if field not in row_dict or not row_dict[field].strip():
            return False, f"Missing required field: {field}"

    # Validate alpha_id format
    alpha_id = row_dict['alpha_id'].strip()
    if not re.match(r'^ALPHA\d+$', alpha_id):
        return False, f"Invalid alpha_id format: {alpha_id}"

    # Check for duplicate alpha_id
    if existing_ids is not None and alpha_id in existing_ids:
        return False, f"Duplicate alpha_id: {alpha_id}"

    # Check for duplicate source_url (if provided)
    source_url = row_dict.get('source_url', '').strip()
    if source_url and existing_urls is not None and source_url in existing_urls:
        return False, f"Duplicate source_url: {source_url}"

    # Validate category (if it has a value)
    category = row_dict.get('category', '').strip()
    valid_categories = [
        'APP_FACTORY', 'CONTENT_FARM', 'COLD_OUTBOUND', 'AI_INFLUENCER',
        'STREAMER_CLIPS', 'PLATFORM_ARBITRAGE', 'ECOM_ARB', 'POD_TRENDING',
        'TOOL_ALPHA', 'GROWTH_HACK', 'MONETIZATION', 'SEO_GEO_ASO',
        'CONTENT_FORMAT', 'EMERGING_PLATFORMS', 'AFFILIATE', 'AUTOMATION_HACK',
        'MICRO_SAAS', 'MCP_SERVERS', 'AI_VIDEO', 'DISCOVERY', 'PLATFORM_META',
        'ENGAGEMENT_FARMING', 'AI_MUSIC', 'ALGO_TRADING', 'CROSS_POLLINATION',
        'OUTBOUND'  # Added for older entries
    ]
    if category and category not in valid_categories and not lenient:
        # Don't fail validation, just warn
        pass

    # Validate status (but be lenient with swarm research entries)
    status = row_dict.get('status', '').strip()
    valid_statuses = ['PENDING_REVIEW', 'APPROVED', 'REJECTED', 'ENGAGEMENT_BAIT',
                      'REPURPOSE_ONLY', 'COMPLIANCE_RISK', 'SATIRICAL_ABSURDIST',
                      'AUTHENTIC', 'UNCHECKED']  # Allow swarm research statuses
    if status and status not in valid_statuses:
        return False, f"Invalid status: {status}"

    return True, ""


def detect_header_columns(file_path: Path) -> Tuple[List[str], int]:
    """Read header row and return column names and expected count."""
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        # Split on comma, handling potential quotes
        reader = csv.reader([first_line])
        headers = next(reader)
        return headers, len(headers)


def is_valid_row_start(line: str, expected_cols: int) -> bool:
    """
    Check if a line looks like the start of a valid CSV row.
    Valid rows should start with ALPHA followed by digits OR have enough commas.
    """
    line = line.strip()

    # Check if starts with ALPHA followed by digits
    if re.match(r'^ALPHA\d+', line):
        return True

    # Also check if line has roughly the right number of commas (within reason)
    # This catches rows that start with a value but lost their alpha_id
    comma_count = line.count(',')
    if comma_count >= expected_cols - 5:  # Allow some missing columns
        return True

    return False


def repair_csv(input_path: Path, output_path: Path) -> Dict[str, int]:
    """
    Repair the corrupted CSV file.

    Returns statistics dictionary.
    """
    print(f"Reading file: {input_path}")

    # Detect header and expected column count
    headers, expected_cols = detect_header_columns(input_path)
    print(f"Headers: {headers}")
    print(f"Expected columns: {expected_cols}")

    stats = {
        'total_rows_read': 0,
        'valid_rows': 0,
        'corrupted_rows_fixed': 0,
        'duplicate_ids_removed': 0,
        'duplicate_urls_removed': 0,
        'final_count': 0
    }

    # Track seen IDs and URLs for deduplication
    seen_ids: Set[str] = set()
    seen_urls: Set[str] = set()

    # Read raw file and reconstruct rows
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"Total lines in file: {len(lines)}")

    # Skip header
    lines = lines[1:]
    stats['total_rows_read'] = len(lines)

    # Reconstruct rows
    reconstructed_rows = []
    current_row = []
    i = 0

    while i < len(lines):
        line = lines[i].rstrip('\n')

        # Check if this looks like the start of a new row
        if is_valid_row_start(line, expected_cols):
            # Save previous row if it exists
            if current_row:
                reconstructed_rows.append(''.join(current_row))
            # Start new row
            current_row = [line + '\n']
        else:
            # Continuation of previous row
            if current_row:
                current_row.append(line + '\n')
            else:
                # Orphaned line, skip it
                pass

        i += 1

    # Don't forget the last row
    if current_row:
        reconstructed_rows.append(''.join(current_row))

    print(f"Reconstructed {len(reconstructed_rows)} rows")

    # Parse reconstructed rows
    valid_rows = []
    for row_text in reconstructed_rows:
        try:
            # Use csv reader to properly parse the row
            reader = csv.reader([row_text])
            row = next(reader)

            # Check if we have the right number of columns
            if len(row) != expected_cols:
                # Try to fix by padding or truncating
                if len(row) < expected_cols:
                    row.extend([''] * (expected_cols - len(row)))
                else:
                    row = row[:expected_cols]
                stats['corrupted_rows_fixed'] += 1

            # Create dict from row
            row_dict = dict(zip(headers, row))

            # Check for duplicate alpha_id
            alpha_id = row_dict.get('alpha_id', '').strip()
            if alpha_id in seen_ids:
                stats['duplicate_ids_removed'] += 1
                continue

            # Check for duplicate source_url
            source_url = row_dict.get('source_url', '').strip()
            if source_url and source_url in seen_urls:
                stats['duplicate_urls_removed'] += 1
                continue

            # Validate row (lenient mode for repair)
            is_valid, error = validate_alpha_row(row_dict, seen_ids, seen_urls, lenient=True)
            if not is_valid:
                print(f"Skipping invalid row {alpha_id}: {error}")
                continue

            # Add to valid rows
            valid_rows.append(row_dict)
            if alpha_id:
                seen_ids.add(alpha_id)
            if source_url:
                seen_urls.add(source_url)
            stats['valid_rows'] += 1

        except Exception as e:
            print(f"Error parsing row: {e}")
            stats['corrupted_rows_fixed'] += 1
            continue

    stats['final_count'] = len(valid_rows)

    # Write repaired file
    print(f"Writing repaired file to: {output_path}")
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
    print("ALPHA_STAGING.csv Repair Script")
    print("="*80)

    stats = repair_csv(input_path, output_path)

    print("\n" + "="*80)
    print("REPAIR COMPLETE")
    print("="*80)
    print(f"Total rows read: {stats['total_rows_read']}")
    print(f"Valid rows: {stats['valid_rows']}")
    print(f"Corrupted rows fixed: {stats['corrupted_rows_fixed']}")
    print(f"Duplicate IDs removed: {stats['duplicate_ids_removed']}")
    print(f"Duplicate URLs removed: {stats['duplicate_urls_removed']}")
    print(f"Final count: {stats['final_count']}")
    print(f"\nRepaired file saved to: {output_path}")
    print("="*80)

    # Calculate corruption percentage
    if stats['total_rows_read'] > 0:
        corruption_pct = ((stats['corrupted_rows_fixed'] +
                          stats['duplicate_ids_removed'] +
                          stats['duplicate_urls_removed']) /
                         stats['total_rows_read'] * 100)
        print(f"Corruption rate: {corruption_pct:.1f}%")

    # Suggest next steps
    print("\nNext steps:")
    print("1. Review the repaired file: LEDGER/ALPHA_STAGING_REPAIRED.csv")
    print("2. If satisfied, backup original and replace:")
    print("   mv LEDGER/ALPHA_STAGING.csv LEDGER/ALPHA_STAGING_BACKUP.csv")
    print("   mv LEDGER/ALPHA_STAGING_REPAIRED.csv LEDGER/ALPHA_STAGING.csv")


if __name__ == '__main__':
    main()
