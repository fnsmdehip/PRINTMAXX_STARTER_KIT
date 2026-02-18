#!/usr/bin/env python3
"""
LEDGER Batch File Consolidation Script
Merges batch CSV files into canonical CSVs with deduplication.
"""

import csv
import os
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = str(PROJECT_ROOT / "LEDGER")

merge_log = []

def log(msg):
    print(msg)
    merge_log.append(msg)


def read_csv_rows(filepath):
    """Read CSV and return (header, rows) where rows are lists of strings."""
    rows = []
    header = None
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                header = row
            else:
                if row and any(cell.strip() for cell in row):  # skip empty rows
                    rows.append(row)
    return header, rows


def write_csv(filepath, header, rows):
    """Write header + rows to CSV."""
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


def get_alpha_ids(rows):
    """Extract alpha_id set from rows (column 0)."""
    return set(row[0].strip() for row in rows if row and row[0].strip())


def get_source_urls(rows, header):
    """Extract source_url set from rows."""
    try:
        idx = header.index('source_url')
    except ValueError:
        return set()
    return set(row[idx].strip() for row in rows if len(row) > idx and row[idx].strip())


def merge_alpha_file(batch_path, canonical_path):
    """Merge a batch alpha file into the canonical ALPHA_STAGING.csv."""
    batch_name = os.path.basename(batch_path)

    if not os.path.exists(batch_path):
        log(f"  SKIP: {batch_name} does not exist")
        return 0, 0, 0

    canon_header, canon_rows = read_csv_rows(canonical_path)
    batch_header, batch_rows = read_csv_rows(batch_path)

    if not batch_rows:
        log(f"  SKIP: {batch_name} has no data rows")
        os.remove(batch_path)
        log(f"  DELETED: {batch_name} (empty)")
        return 0, 0, 0

    # Check if batch file has a header row or starts with data
    has_header = False
    if batch_header:
        # If first cell looks like a header (contains alpha_id or similar)
        if batch_header[0].strip().lower() == 'alpha_id':
            has_header = True
        else:
            # First row is data, not header - treat it as a data row
            batch_rows.insert(0, batch_header)
            batch_header = canon_header  # use canonical header

    # Get existing identifiers for dedup
    existing_ids = get_alpha_ids(canon_rows)
    existing_urls = get_source_urls(canon_rows, canon_header)

    # Determine column mappings
    # Batch may have same or different column count - normalize to canonical
    canon_col_count = len(canon_header)

    new_rows = []
    dup_count = 0

    for row in batch_rows:
        if not row or not any(cell.strip() for cell in row):
            continue

        # Check alpha_id dedup
        alpha_id = row[0].strip() if row else ''
        if alpha_id in existing_ids:
            dup_count += 1
            continue

        # Check source_url dedup
        try:
            batch_url_idx = batch_header.index('source_url') if has_header else 2
        except ValueError:
            batch_url_idx = 2  # default position

        if len(row) > batch_url_idx:
            url = row[batch_url_idx].strip()
            if url and url in existing_urls:
                dup_count += 1
                continue

        # Normalize row length to canonical
        if len(row) < canon_col_count:
            row.extend([''] * (canon_col_count - len(row)))
        elif len(row) > canon_col_count:
            row = row[:canon_col_count]

        new_rows.append(row)
        existing_ids.add(alpha_id)
        if len(row) > batch_url_idx:
            existing_urls.add(row[batch_url_idx].strip())

    total = len(batch_rows)
    added = len(new_rows)

    if new_rows:
        canon_rows.extend(new_rows)
        write_csv(canonical_path, canon_header, canon_rows)

    # Delete batch file
    os.remove(batch_path)
    log(f"  MERGED: {batch_name} -> {total} total, {added} added, {dup_count} duplicates skipped")
    log(f"  DELETED: {batch_name}")

    return total, added, dup_count


def merge_cross_pollination():
    """Merge CROSS_POLLINATION_MATRIX_UPDATED.csv into CROSS_POLLINATION_MATRIX.csv."""
    canon_path = os.path.join(LEDGER_DIR, "CROSS_POLLINATION_MATRIX.csv")
    updated_path = os.path.join(LEDGER_DIR, "CROSS_POLLINATION_MATRIX_UPDATED.csv")

    if not os.path.exists(updated_path):
        log("  SKIP: CROSS_POLLINATION_MATRIX_UPDATED.csv does not exist")
        return

    canon_header, canon_rows = read_csv_rows(canon_path)
    updated_header, updated_rows = read_csv_rows(updated_path)

    log(f"\n--- CROSS_POLLINATION_MATRIX Comparison ---")
    log(f"  Canonical: {len(canon_rows)} rows, {len(canon_header)} columns")
    log(f"  Updated:   {len(updated_rows)} rows, {len(updated_header)} columns")
    log(f"  Canonical header: {canon_header}")
    log(f"  Updated header:   {updated_header}")

    # The updated file has an extra column: revenue_multiplier
    # It also has more methods covered with richer synergy_partners data
    # Strategy: Use updated as the new canonical since it's a superset

    # Check which method_ids exist in each
    canon_methods = set(row[0].strip() for row in canon_rows if row)
    updated_methods = set(row[0].strip() for row in updated_rows if row)

    only_in_canon = canon_methods - updated_methods
    only_in_updated = updated_methods - canon_methods
    in_both = canon_methods & updated_methods

    log(f"  Methods in both: {len(in_both)}")
    log(f"  Only in canonical: {len(only_in_canon)} - {only_in_canon if only_in_canon else 'none'}")
    log(f"  Only in updated: {len(only_in_updated)} - {only_in_updated if only_in_updated else 'none'}")

    # Build final merged dataset using updated as base, adding any canon-only entries
    # Normalize canon-only rows to updated header (add revenue_multiplier column)
    final_rows = list(updated_rows)

    if only_in_canon:
        # Find canon rows for methods only in canon
        for row in canon_rows:
            if row[0].strip() in only_in_canon:
                # Add empty revenue_multiplier column (position 8 in updated)
                extended_row = list(row)
                # Insert revenue_multiplier before notes (last column in both)
                # Canon: method_id,method_name,synergy_partners,synergy_type,synergy_score,cross_sell_products,shared_audience,automation_combo,notes
                # Updated: method_id,method_name,synergy_partners,synergy_type,synergy_score,cross_sell_products,shared_audience,automation_combo,revenue_multiplier,notes
                if len(extended_row) == len(canon_header):
                    notes = extended_row[-1]
                    extended_row[-1] = ''  # revenue_multiplier
                    extended_row.append(notes)
                else:
                    extended_row.append('')  # revenue_multiplier
                    extended_row.append('')  # notes
                final_rows.append(extended_row)
        log(f"  Added {len(only_in_canon)} canon-only entries to merged result")

    # Write merged result
    write_csv(canon_path, updated_header, final_rows)
    log(f"  REPLACED: CROSS_POLLINATION_MATRIX.csv with merged data ({len(final_rows)} rows, new header with revenue_multiplier)")

    # Delete updated file
    os.remove(updated_path)
    log(f"  DELETED: CROSS_POLLINATION_MATRIX_UPDATED.csv")


def merge_ecom():
    """Merge ECOM_OPPORTUNITIES_JAN_2026.csv into ECOM_ARB_OPPORTUNITIES.csv."""
    canon_path = os.path.join(LEDGER_DIR, "ECOM_ARB_OPPORTUNITIES.csv")
    batch_path = os.path.join(LEDGER_DIR, "ECOM_OPPORTUNITIES_JAN_2026.csv")

    if not os.path.exists(batch_path):
        log("  SKIP: ECOM_OPPORTUNITIES_JAN_2026.csv does not exist")
        return

    canon_header, canon_rows = read_csv_rows(canon_path)
    batch_header, batch_rows = read_csv_rows(batch_path)

    log(f"\n--- ECOM Merge ---")
    log(f"  Canonical: {len(canon_rows)} rows")
    log(f"  Batch:     {len(batch_rows)} rows")
    log(f"  Canonical header: {canon_header}")
    log(f"  Batch header:     {batch_header}")

    # Headers differ - need column mapping
    # Canonical: opportunity_id,category,product_name,source_platform,source_price,sell_platform,sell_price,margin_estimate,demand_proof,source_url,notes,date_found,status
    # Batch: opportunity_id,product_name,category,source_price_usd,sell_price_usd,margin_pct,platform_sell,platform_source,competition_level,trend_direction,notes

    # Get existing opportunity IDs and product names for dedup
    existing_ids = set(row[0].strip() for row in canon_rows if row)
    existing_products = set(row[2].strip().lower() for row in canon_rows if row and len(row) > 2)

    # Get highest ECOM number
    max_ecom_num = 0
    for oid in existing_ids:
        if oid.startswith('ECOM'):
            try:
                num = int(oid.replace('ECOM', ''))
                max_ecom_num = max(max_ecom_num, num)
            except ValueError:
                pass

    new_rows = []
    dup_count = 0
    next_id = max_ecom_num + 1

    for row in batch_rows:
        if not row or not any(cell.strip() for cell in row):
            continue

        # Map batch columns to canonical format
        # batch: opportunity_id,product_name,category,source_price_usd,sell_price_usd,margin_pct,platform_sell,platform_source,competition_level,trend_direction,notes
        batch_id = row[0].strip() if len(row) > 0 else ''
        product_name = row[1].strip() if len(row) > 1 else ''
        category = row[2].strip() if len(row) > 2 else ''
        source_price = row[3].strip() if len(row) > 3 else ''
        sell_price = row[4].strip() if len(row) > 4 else ''
        margin = row[5].strip() if len(row) > 5 else ''
        platform_sell = row[6].strip() if len(row) > 6 else ''
        platform_source = row[7].strip() if len(row) > 7 else ''
        competition = row[8].strip() if len(row) > 8 else ''
        trend = row[9].strip() if len(row) > 9 else ''
        notes = row[10].strip() if len(row) > 10 else ''

        # Check for duplicate by product name (case insensitive)
        if product_name.lower() in existing_products:
            dup_count += 1
            continue

        # Check for ID collision
        if batch_id in existing_ids:
            # Reassign ID
            new_id = f"ECOM{next_id:03d}"
            next_id += 1
        else:
            new_id = batch_id

        # Map to canonical format:
        # opportunity_id,category,product_name,source_platform,source_price,sell_platform,sell_price,margin_estimate,demand_proof,source_url,notes,date_found,status
        # Use source_price_usd as source_price with $ prefix
        source_price_fmt = f"${source_price}" if source_price and not source_price.startswith('$') else source_price
        sell_price_fmt = f"${sell_price}" if sell_price and not sell_price.startswith('$') else sell_price
        margin_fmt = margin if '%' in margin else f"{margin}%"

        canon_row = [
            new_id,
            category,
            product_name,
            platform_source,
            source_price_fmt,
            platform_sell,
            sell_price_fmt,
            margin_fmt,
            f"Competition: {competition}. Trend: {trend}",  # demand_proof
            '',  # source_url (not in batch)
            notes,
            '2026-01',  # date_found
            'NEW'  # status
        ]

        new_rows.append(canon_row)
        existing_ids.add(new_id)
        existing_products.add(product_name.lower())

    total = len(batch_rows)
    added = len(new_rows)

    if new_rows:
        canon_rows.extend(new_rows)
        write_csv(canon_path, canon_header, canon_rows)

    # Delete batch file
    os.remove(batch_path)
    log(f"  MERGED: ECOM_OPPORTUNITIES_JAN_2026.csv -> {total} total, {added} added, {dup_count} duplicates skipped")
    log(f"  DELETED: ECOM_OPPORTUNITIES_JAN_2026.csv")


def main():
    log("=" * 60)
    log("LEDGER BATCH CONSOLIDATION")
    log(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=" * 60)

    canonical_alpha = os.path.join(LEDGER_DIR, "ALPHA_STAGING.csv")

    # Pre-merge counts
    _, pre_alpha_rows = read_csv_rows(canonical_alpha)
    log(f"\nPre-merge ALPHA_STAGING.csv: {len(pre_alpha_rows)} rows")

    # ---- ALPHA MERGES ----
    log("\n--- ALPHA_STAGING Merges ---")

    alpha_batches = [
        "ALPHA_STAGING_NEW.csv",
        "ALPHA_STAGING_NEW_BATCH.csv",
        "ALPHA_STAGING_NEW_ENTRIES.csv",
        "ALPHA_STAGING_NEW_ENTRIES_2026-02-02.csv",
    ]

    total_added = 0
    total_dupes = 0
    total_processed = 0

    for batch_name in alpha_batches:
        batch_path = os.path.join(LEDGER_DIR, batch_name)
        log(f"\n  Processing: {batch_name}")
        t, a, d = merge_alpha_file(batch_path, canonical_alpha)
        total_processed += t
        total_added += a
        total_dupes += d

    # Post-merge count
    _, post_alpha_rows = read_csv_rows(canonical_alpha)
    log(f"\n  ALPHA_STAGING Summary:")
    log(f"    Before: {len(pre_alpha_rows)} rows")
    log(f"    After:  {len(post_alpha_rows)} rows")
    log(f"    Net added: {len(post_alpha_rows) - len(pre_alpha_rows)}")
    log(f"    Batch rows processed: {total_processed}")
    log(f"    Unique rows added: {total_added}")
    log(f"    Duplicates skipped: {total_dupes}")

    # ---- CROSS_POLLINATION MERGE ----
    merge_cross_pollination()

    # ---- ECOM MERGE ----
    merge_ecom()

    # ---- FINAL SUMMARY ----
    log("\n" + "=" * 60)
    log("CONSOLIDATION COMPLETE")
    log("=" * 60)

    # Verify no batch files remain
    remaining = []
    for f in os.listdir(LEDGER_DIR):
        if any(f.startswith(prefix) for prefix in [
            'ALPHA_STAGING_NEW',
            'CROSS_POLLINATION_MATRIX_UPDATED',
            'ECOM_OPPORTUNITIES_JAN'
        ]):
            remaining.append(f)

    if remaining:
        log(f"\nWARNING: Batch files still exist: {remaining}")
    else:
        log(f"\nAll batch files deleted successfully.")

    # Write merge log
    log_path = os.path.join(LEDGER_DIR, "BATCH_MERGE_LOG_FEB_2026.md")
    with open(log_path, 'w') as f:
        f.write("# LEDGER Batch Merge Log - February 2026\n\n")
        f.write(f"**Executed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Merge Operations\n\n```\n")
        for line in merge_log:
            f.write(line + "\n")
        f.write("```\n\n")
        f.write("## Files Merged\n\n")
        f.write("| Batch File | Target | Result |\n")
        f.write("|-----------|--------|--------|\n")
        f.write(f"| ALPHA_STAGING_NEW.csv | ALPHA_STAGING.csv | Merged + deleted |\n")
        f.write(f"| ALPHA_STAGING_NEW_BATCH.csv | ALPHA_STAGING.csv | Merged + deleted |\n")
        f.write(f"| ALPHA_STAGING_NEW_ENTRIES.csv | ALPHA_STAGING.csv | Merged + deleted |\n")
        f.write(f"| ALPHA_STAGING_NEW_ENTRIES_2026-02-02.csv | ALPHA_STAGING.csv | Merged + deleted |\n")
        f.write(f"| CROSS_POLLINATION_MATRIX_UPDATED.csv | CROSS_POLLINATION_MATRIX.csv | Verified + replaced + deleted |\n")
        f.write(f"| ECOM_OPPORTUNITIES_JAN_2026.csv | ECOM_ARB_OPPORTUNITIES.csv | Column-mapped + merged + deleted |\n")
        f.write("\n## Post-Merge State\n\n")

        # Read final counts
        _, final_alpha = read_csv_rows(canonical_alpha)
        _, final_cp = read_csv_rows(os.path.join(LEDGER_DIR, "CROSS_POLLINATION_MATRIX.csv"))
        _, final_ecom = read_csv_rows(os.path.join(LEDGER_DIR, "ECOM_ARB_OPPORTUNITIES.csv"))

        f.write(f"| Canonical File | Row Count |\n")
        f.write(f"|---------------|----------|\n")
        f.write(f"| ALPHA_STAGING.csv | {len(final_alpha)} |\n")
        f.write(f"| CROSS_POLLINATION_MATRIX.csv | {len(final_cp)} |\n")
        f.write(f"| ECOM_ARB_OPPORTUNITIES.csv | {len(final_ecom)} |\n")
        f.write("\n## Deduplication Strategy\n\n")
        f.write("- **ALPHA_STAGING**: Deduplicated by `alpha_id` (primary) and `source_url` (secondary)\n")
        f.write("- **CROSS_POLLINATION_MATRIX**: Updated file used as base (superset with `revenue_multiplier` column), canonical-only entries appended\n")
        f.write("- **ECOM_ARB_OPPORTUNITIES**: Deduplicated by `product_name` (case-insensitive), columns mapped from batch schema to canonical schema\n")

    log(f"\nMerge log written to: {log_path}")


if __name__ == '__main__':
    main()
