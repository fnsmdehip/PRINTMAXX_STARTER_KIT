#!/usr/bin/env python3

from __future__ import annotations
"""
ALPHA_STAGING.csv Parser v2
Handles TWO different CSV formats:
  - 14-column format (bookmarks scraper): alpha_id,source,source_url,category,tactic,full_description,actionable_steps,roi_potential,implementation_complexity,legal_risk,applicable_methods,status,priority,reviewer_notes
  - 11-column format (account scraper): alpha_id,source,source_url,tactic,category,roi_potential,implementation_complexity,legal_risk,applicable_methods,timestamp,reviewer_notes
"""

import csv
import json
import sys
import os

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "LEDGER", "ALPHA_STAGING.csv")

# Known valid categories
VALID_CATEGORIES = {
    'APP_FACTORY', 'TOOL_ALPHA', 'COLD_OUTBOUND', 'SEO_GEO_ASO', 'GROWTH_HACK',
    'CONTENT_FARM', 'GENERAL', 'CONTENT_FORMAT', 'MONETIZATION', 'ALPHA_GENERAL',
    'AI_INFLUENCER', 'OUTBOUND', 'ENGAGEMENT_BAIT', 'NEW_METHOD', 'ECOM',
    'AFFILIATE', 'NEWSLETTER', 'SAAS', 'POD', 'DIGITAL_PRODUCTS',
    'INFO_PRODUCT', 'AGENCY', 'AUTOMATION', 'SOCIAL_MEDIA', 'TRADING',
    'CRYPTO', 'REAL_ESTATE', 'MEMECOIN', 'STREAMING', 'AI_MUSIC',
    'LOCAL_BIZ', 'WHOP', 'N/A', ''
}


def parse_alpha_csv(csv_path=CSV_PATH):
    """Parse ALPHA_STAGING.csv handling both 14-column and 11-column formats."""
    entries = []
    parse_errors = []
    format_14 = 0
    format_11 = 0
    format_13 = 0
    format_other = 0

    with open(csv_path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        header = next(reader)

        for row_num, row in enumerate(reader, start=2):
            try:
                ncols = len(row)

                if not row or not row[0].strip().startswith('ALPHA'):
                    parse_errors.append({
                        'line': row_num,
                        'issue': f'Does not start with ALPHA (cols={ncols})',
                        'content': str(row[:2]) if row else 'EMPTY'
                    })
                    continue

                alpha_id = row[0].strip()

                if ncols == 14:
                    # Original 14-column format (bookmarks scraper)
                    format_14 += 1
                    source = row[1].strip()
                    source_url = row[2].strip()
                    category = row[3].strip()
                    tactic = row[4].strip()
                    full_description = row[5].strip()
                    actionable_steps = row[6].strip()
                    roi_potential = row[7].strip()
                    status = row[11].strip()
                    priority = row[12].strip()
                    reviewer_notes = row[13].strip()

                elif ncols == 11:
                    # 11-column format (account scraper)
                    # Schema: alpha_id, source, source_url, tactic, category, roi_potential,
                    #         implementation_complexity, legal_risk, applicable_methods, timestamp, reviewer_notes
                    format_11 += 1
                    source = row[1].strip()
                    source_url = row[2].strip()
                    tactic = row[3].strip()
                    category = row[4].strip()
                    full_description = tactic  # Same as tactic in this format
                    actionable_steps = ''
                    roi_potential = row[5].strip()
                    status = 'PENDING_REVIEW'  # These don't have explicit status
                    priority = row[9].strip()  # timestamp used as priority proxy
                    reviewer_notes = row[10].strip()

                elif ncols == 13:
                    # 13-column format (variant)
                    format_13 += 1
                    source = row[1].strip()
                    source_url = row[2].strip()
                    category = row[3].strip()
                    tactic = row[4].strip()
                    full_description = row[5].strip()
                    actionable_steps = row[6].strip()
                    roi_potential = row[7].strip()
                    status = row[11].strip()
                    priority = row[12].strip() if ncols > 12 else ''
                    reviewer_notes = ''

                else:
                    format_other += 1
                    parse_errors.append({
                        'line': row_num,
                        'issue': f'Unexpected {ncols} columns for {alpha_id}',
                        'content': str(row[:3])
                    })
                    continue

                # Normalize category
                if category not in VALID_CATEGORIES:
                    # Try to find a valid category in the row
                    for cell in row:
                        cell_stripped = cell.strip()
                        if cell_stripped in VALID_CATEGORIES and cell_stripped != '':
                            category = cell_stripped
                            break

                # Truncate tactic for summary
                tactic_short = tactic[:200].replace('\n', ' ').replace('\r', ' ').strip()

                entries.append({
                    'alpha_id': alpha_id,
                    'source': source,
                    'source_url': source_url,
                    'category': category,
                    'tactic': tactic_short,
                    'full_tactic': tactic,
                    'full_description': full_description,
                    'roi_potential': roi_potential,
                    'status': status,
                    'priority': priority,
                    'reviewer_notes': reviewer_notes,
                    'actionable_steps': actionable_steps,
                    'format': f'{ncols}-col',
                })

            except Exception as e:
                parse_errors.append({
                    'line': row_num,
                    'issue': str(e),
                    'content': str(row[:2]) if row else 'EMPTY'
                })

    return entries, header, parse_errors, {
        '14-col': format_14, '11-col': format_11,
        '13-col': format_13, 'other': format_other
    }


def print_summary(entries, parse_errors, format_stats):
    """Print a summary report of parsing results."""

    print("=" * 70)
    print("ALPHA_STAGING.csv PARSING REPORT (v2 - Multi-Format)")
    print("=" * 70)

    print(f"\nTotal entries parsed successfully: {len(entries)}")
    print(f"Parse errors: {len(parse_errors)}")
    print(f"\nFormat breakdown:")
    for fmt, count in format_stats.items():
        print(f"  {fmt}: {count}")

    # Category breakdown
    categories = {}
    for e in entries:
        cat = e['category'] if e['category'] else 'EMPTY'
        categories[cat] = categories.get(cat, 0) + 1

    print(f"\n--- CATEGORY BREAKDOWN ({len(categories)} categories) ---")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    # Status breakdown
    statuses = {}
    for e in entries:
        st = e['status'] if e['status'] else 'EMPTY'
        statuses[st] = statuses.get(st, 0) + 1

    print(f"\n--- STATUS BREAKDOWN ---")
    for st, count in sorted(statuses.items(), key=lambda x: -x[1]):
        print(f"  {st}: {count}")

    # ROI breakdown
    rois = {}
    for e in entries:
        roi = e['roi_potential'] if e['roi_potential'] else 'EMPTY'
        rois[roi] = rois.get(roi, 0) + 1

    print(f"\n--- ROI POTENTIAL BREAKDOWN ---")
    for roi, count in sorted(rois.items(), key=lambda x: -x[1]):
        print(f"  {roi}: {count}")

    # Source breakdown (top 30)
    sources = {}
    for e in entries:
        src = e['source'] if e['source'] else 'EMPTY'
        src_base = src.split(' (')[0] if ' (' in src else src
        sources[src_base] = sources.get(src_base, 0) + 1

    print(f"\n--- TOP 30 SOURCES ---")
    for src, count in sorted(sources.items(), key=lambda x: -x[1])[:30]:
        print(f"  {src}: {count}")

    # Alpha ID range
    ids = []
    for e in entries:
        try:
            num = int(e['alpha_id'].replace('ALPHA', ''))
            ids.append(num)
        except Exception:
            pass  # Skip entries with non-numeric alpha_id

    if ids:
        print(f"\n--- ALPHA ID RANGE ---")
        print(f"  Min: ALPHA{min(ids)}")
        print(f"  Max: ALPHA{max(ids)}")
        print(f"  Total unique IDs: {len(set(ids))}")
        dupes = len(ids) - len(set(ids))
        if dupes:
            print(f"  DUPLICATE IDs: {dupes}")

    # Parse errors details
    if parse_errors:
        print(f"\n--- PARSE ERRORS (first 10) ---")
        for err in parse_errors[:10]:
            print(f"  Line {err['line']}: {err['issue']}")

    # PENDING_REVIEW entries
    pending = [e for e in entries if e['status'] == 'PENDING_REVIEW']
    print(f"\n--- PENDING_REVIEW ENTRIES: {len(pending)} ---")
    print(f"\nFirst 60 PENDING_REVIEW entries:")
    for i, e in enumerate(pending[:60]):
        print(f"  {i+1}. {e['alpha_id']} | {e['source'][:25]:<25} | {e['category']:<15} | {e['tactic'][:75]}")

    return pending


def save_clean_summary(entries, parse_errors, format_stats, output_path=None):
    """Save a clean JSON summary to a temp file."""
    if output_path is None:
        output_path = os.path.join(os.path.dirname(CSV_PATH), 'ALPHA_CLEAN_SUMMARY.json')

    summary = {
        'total_entries': len(entries),
        'parse_errors': len(parse_errors),
        'format_stats': format_stats,
        'entries': entries,
        'errors': parse_errors[:50]
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\nClean summary saved to: {output_path}")
    return output_path


if __name__ == '__main__':
    entries, header, parse_errors, format_stats = parse_alpha_csv()
    pending = print_summary(entries, parse_errors, format_stats)
    save_clean_summary(entries, parse_errors, format_stats)

    # Save pending entries
    pending_path = os.path.join(os.path.dirname(CSV_PATH), 'ALPHA_PENDING_REVIEW.json')
    pending_entries = [e for e in entries if e['status'] == 'PENDING_REVIEW']
    with open(pending_path, 'w', encoding='utf-8') as f:
        json.dump(pending_entries, f, indent=2, ensure_ascii=False)
    print(f"Pending review entries saved to: {pending_path} ({len(pending_entries)} entries)")
