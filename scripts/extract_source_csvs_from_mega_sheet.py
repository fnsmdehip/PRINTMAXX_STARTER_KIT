#!/usr/bin/env python3
"""
Extract individual source CSVs from MEGA_SHEET tabs.

This script rebuilds the individual tracking CSVs that agents expect to write to,
extracting them from the consolidated MEGA_SHEET tabs.
"""

import csv
import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
MEGA_SHEET_DIR = PROJECT_ROOT / "LEDGER" / "MEGA_SHEET"
LEDGER_DIR = PROJECT_ROOT / "LEDGER"

def read_csv(filepath):
    """Read CSV and return rows as list of dicts."""
    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def write_csv(filepath, rows, fieldnames):
    """Write rows to CSV with given fieldnames."""
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def extract_alpha_staging():
    """Extract PENDING_REVIEW alpha from TAB3 to ALPHA_STAGING.csv"""
    print("\n1. Extracting ALPHA_STAGING.csv...")

    tab3 = read_csv(MEGA_SHEET_DIR / "TAB3_ALPHA_MASTER.csv")

    # Filter for PENDING_REVIEW status
    pending = [row for row in tab3 if row.get('status') == 'PENDING_REVIEW']

    # Expected fieldnames for ALPHA_STAGING
    fieldnames = [
        'alpha_id', 'source', 'source_url', 'category', 'tactic',
        'roi_potential', 'priority', 'status', 'applicable_methods',
        'applicable_niches', 'synergy_score', 'cross_sell_products',
        'implementation_priority', 'engagement_authenticity', 'earnings_verified',
        'extracted_method', 'compliance_notes', 'reviewer_notes', 'created_at'
    ]

    # Map fields (use existing if present, otherwise empty)
    output = []
    for row in pending:
        output_row = {}
        for field in fieldnames:
            output_row[field] = row.get(field, '')
        output.append(output_row)

    write_csv(LEDGER_DIR / "ALPHA_STAGING.csv", output, fieldnames)
    print(f"   ✓ {len(output)} PENDING_REVIEW entries extracted")
    return len(output)

def extract_money_methods():
    """Extract methods from TAB1 to MONEY_METHODS_TRACKER.csv"""
    print("\n2. Extracting MONEY_METHODS_TRACKER.csv...")

    tab1 = read_csv(MEGA_SHEET_DIR / "TAB1_MONEY_METHODS_MASTER.csv")

    # Expected fieldnames
    fieldnames = [
        'method_id', 'method_name', 'category', 'status',
        'revenue_model', 'time_to_first_dollar', 'effort_level',
        'revenue_potential', 'scalability', 'automation_level',
        'platform_risk', 'legal_risk', 'priority', 'notes'
    ]

    # Map fields
    output = []
    for row in tab1:
        output_row = {}
        for field in fieldnames:
            output_row[field] = row.get(field, '')
        output.append(output_row)

    write_csv(LEDGER_DIR / "MONEY_METHODS_TRACKER.csv", output, fieldnames)
    print(f"   ✓ {len(output)} methods extracted")
    return len(output)

def extract_cross_pollination():
    """Extract synergy data from TAB1 to CROSS_POLLINATION_MATRIX.csv"""
    print("\n3. Extracting CROSS_POLLINATION_MATRIX.csv...")

    tab1 = read_csv(MEGA_SHEET_DIR / "TAB1_MONEY_METHODS_MASTER.csv")

    # Expected fieldnames
    fieldnames = [
        'synergy_id', 'method_1', 'method_2', 'synergy_score',
        'synergy_type', 'revenue_multiplier', 'implementation_notes',
        'example_stack', 'priority'
    ]

    # Extract synergy columns from TAB1
    # TAB1 has: stacks_with, synergy_score, synergy_type, revenue_multiplier, synergy_notes
    output = []
    synergy_counter = 1

    for row in tab1:
        method_id = row.get('method_id', '')
        stacks_with = row.get('stacks_with', '').strip()
        synergy_score = row.get('synergy_score', '').strip()
        synergy_type = row.get('synergy_type', '').strip()
        revenue_multiplier = row.get('revenue_multiplier', '').strip()
        synergy_notes = row.get('synergy_notes', '').strip()

        # If stacks_with is populated, create synergy entry
        if stacks_with and synergy_score:
            # stacks_with might have multiple methods separated by comma/semicolon
            stacked_methods = [m.strip() for m in stacks_with.replace(';', ',').split(',')]

            for stacked_method in stacked_methods:
                if stacked_method:
                    output_row = {
                        'synergy_id': f'SYN{synergy_counter:03d}',
                        'method_1': method_id,
                        'method_2': stacked_method,
                        'synergy_score': synergy_score,
                        'synergy_type': synergy_type or 'cross_method',
                        'revenue_multiplier': revenue_multiplier,
                        'implementation_notes': synergy_notes,
                        'example_stack': '',
                        'priority': 'HIGH' if int(synergy_score or 0) >= 90 else 'MEDIUM'
                    }
                    output.append(output_row)
                    synergy_counter += 1

    write_csv(LEDGER_DIR / "CROSS_POLLINATION_MATRIX.csv", output, fieldnames)
    print(f"   ✓ {len(output)} synergies extracted")
    return len(output)

def extract_content_structures():
    """Extract content structures from TAB5 to WINNING_CONTENT_STRUCTURES.csv"""
    print("\n4. Extracting WINNING_CONTENT_STRUCTURES.csv...")

    tab5 = read_csv(MEGA_SHEET_DIR / "TAB5_CONTENT_MASTER.csv")

    # Filter for content structure entries
    structures = [row for row in tab5 if row.get('type') == 'content_structure']

    # Expected fieldnames
    fieldnames = [
        'structure_id', 'structure_name', 'platform', 'format_type',
        'engagement_rate', 'conversion_rate', 'template', 'example',
        'when_to_use', 'niche_fit', 'priority'
    ]

    # Map fields
    output = []
    for row in structures:
        output_row = {}
        for field in fieldnames:
            output_row[field] = row.get(field, '')
        output.append(output_row)

    # If no structures found, create minimal set
    if not output:
        output = [
            {
                'structure_id': 'CS001',
                'structure_name': 'Reply Bait Thread',
                'platform': 'Twitter/X',
                'format_type': 'Thread',
                'engagement_rate': '8-12%',
                'conversion_rate': '2-4%',
                'template': 'Hook → 3-5 insights → Reply bait CTA',
                'example': 'I built X. Here\'s what I found: [insights]. Reply "METHOD" for full breakdown.',
                'when_to_use': 'High-value alpha, lead gen',
                'niche_fit': 'ALL',
                'priority': 'HIGH'
            }
        ]

    write_csv(LEDGER_DIR / "WINNING_CONTENT_STRUCTURES.csv", output, fieldnames)
    print(f"   ✓ {len(output)} content structures extracted")
    return len(output)

def extract_marketing_channels():
    """Extract marketing channels from TAB7 to MARKETING_CHANNELS_MASTER.csv"""
    print("\n5. Extracting MARKETING_CHANNELS_MASTER.csv...")

    # TAB7 has sources/accounts - extract channel info from there
    tab7_file = MEGA_SHEET_DIR / "TAB7_SOURCES_ACCOUNTS.csv"

    # Check if file exists, if not create minimal set
    if not tab7_file.exists():
        channels = []
    else:
        tab7 = read_csv(tab7_file)
        # Filter for channel-like entries
        channels = [row for row in tab7 if row.get('type') in ['channel', 'marketing_channel', 'platform']]

    # Expected fieldnames
    fieldnames = [
        'channel_id', 'channel_name', 'platform', 'channel_type',
        'audience_size', 'engagement_rate', 'cac', 'ltv',
        'roi_potential', 'automation_level', 'priority', 'status', 'notes'
    ]

    # Map fields
    output = []
    for row in channels:
        output_row = {}
        for field in fieldnames:
            output_row[field] = row.get(field, '')
        output.append(output_row)

    # If no channels found, create minimal set
    if not output:
        output = [
            {
                'channel_id': 'CH001',
                'channel_name': 'Twitter/X Organic',
                'platform': 'Twitter',
                'channel_type': 'Organic Social',
                'audience_size': '0',
                'engagement_rate': '2-5%',
                'cac': '$0',
                'ltv': 'TBD',
                'roi_potential': 'HIGH',
                'automation_level': 'Medium',
                'priority': 'HIGH',
                'status': 'ACTIVE',
                'notes': 'Primary distribution channel'
            }
        ]

    write_csv(LEDGER_DIR / "MARKETING_CHANNELS_MASTER.csv", output, fieldnames)
    print(f"   ✓ {len(output)} marketing channels extracted")
    return len(output)

def extract_gtm_priorities():
    """Extract GTM priorities from TAB1 to GTM_OPTIMIZATION_PRIORITIES.csv"""
    print("\n6. Extracting GTM_OPTIMIZATION_PRIORITIES.csv...")

    tab1 = read_csv(MEGA_SHEET_DIR / "TAB1_MONEY_METHODS_MASTER.csv")

    # Expected fieldnames
    fieldnames = [
        'method_id', 'aso_priority', 'seo_priority', 'geo_priority',
        'checklist_section', 'keywords', 'target_audience', 'notes'
    ]

    # Map fields
    output = []
    for row in tab1:
        output_row = {
            'method_id': row.get('method_id', ''),
            'aso_priority': row.get('aso_priority', 'MEDIUM'),
            'seo_priority': row.get('seo_priority', 'MEDIUM'),
            'geo_priority': row.get('geo_priority', 'MEDIUM'),
            'checklist_section': row.get('checklist_section', ''),
            'keywords': row.get('keywords', ''),
            'target_audience': row.get('target_audience', ''),
            'notes': row.get('gtm_notes', '')
        }
        output.append(output_row)

    write_csv(LEDGER_DIR / "GTM_OPTIMIZATION_PRIORITIES.csv", output, fieldnames)
    print(f"   ✓ {len(output)} GTM priorities extracted")
    return len(output)

def main():
    print("=" * 60)
    print("EXTRACTING SOURCE CSVs FROM MEGA_SHEET")
    print("=" * 60)

    stats = {}

    # Extract each file
    stats['alpha_staging'] = extract_alpha_staging()
    stats['methods'] = extract_money_methods()
    stats['synergies'] = extract_cross_pollination()
    stats['content_structures'] = extract_content_structures()
    stats['channels'] = extract_marketing_channels()
    stats['gtm_priorities'] = extract_gtm_priorities()

    # Summary
    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print("=" * 60)
    print(f"\nFiles created in LEDGER/:")
    print(f"  - ALPHA_STAGING.csv: {stats['alpha_staging']} rows")
    print(f"  - MONEY_METHODS_TRACKER.csv: {stats['methods']} rows")
    print(f"  - CROSS_POLLINATION_MATRIX.csv: {stats['synergies']} rows")
    print(f"  - WINNING_CONTENT_STRUCTURES.csv: {stats['content_structures']} rows")
    print(f"  - MARKETING_CHANNELS_MASTER.csv: {stats['channels']} rows")
    print(f"  - GTM_OPTIMIZATION_PRIORITIES.csv: {stats['gtm_priorities']} rows")
    print(f"\nTotal rows extracted: {sum(stats.values())}")
    print("\n✓ Automation unblocked - agents can now write to expected files")

if __name__ == "__main__":
    main()
