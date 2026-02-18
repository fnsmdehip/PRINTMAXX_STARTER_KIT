#!/usr/bin/env python3
"""
PRINTMAXX MEGA SHEET BUILDER
Consolidates all LEDGER CSVs into 10 tab files for Google Sheets import.
"""

import csv
import os
import sys
from collections import OrderedDict

BASE = "/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/LEDGER"
OUT = os.path.join(BASE, "MEGA_SHEET")
os.makedirs(OUT, exist_ok=True)

def is_header_row(first_line):
    """Heuristic: if first field starts with a letter and looks like a column name, it's a header."""
    parts = next(csv.reader([first_line]))
    if not parts:
        return False
    first = parts[0].strip()
    # If first field starts with a known ID pattern (ALPHA###, N###, etc.), it's data not header
    if any(first.startswith(prefix) for prefix in ['ALPHA', 'N0', 'N1', 'N2', 'N3', 'MM', 'CF', 'AI0', 'EDGE', 'ECOM', 'EXP', 'LEAD', 'AFF', 'T0', 'CH0', 'CS0', 'SRC', 'MSAAS']):
        return False
    return True

# Known headers for headerless files
KNOWN_HEADERS = {
    'ALPHA_STAGING_NEW_ENTRIES.csv': ['alpha_id', 'source', 'source_url', 'category', 'title', 'description', 'actionable_steps', 'effort_level', 'roi_potential', 'risk_level', 'applies_to_niches', 'status', 'reviewed_date', 'reviewer_notes'],
    'NICHES_NEW_ENTRIES.csv': ['niche_id', 'niche_name', 'target_demo', 'content_themes', 'offer_stack', 'applicable_methods', 'priority'],
}

def read_csv_safe(filepath):
    """Read a CSV file, return list of dicts. Handle missing files and headerless files gracefully."""
    if not os.path.exists(filepath):
        print(f"  SKIP (not found): {filepath}")
        return [], []
    rows = []
    headers = []
    basename = os.path.basename(filepath)
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            # Skip comment lines starting with #
            lines = []
            for line in f:
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    lines.append(line)
            if not lines:
                print(f"  SKIP (empty): {filepath}")
                return [], []

            # Check if file is headerless
            force_headers = KNOWN_HEADERS.get(basename, None)
            if force_headers is not None or not is_header_row(lines[0]):
                # Headerless file - use known headers or alpha staging headers as fallback
                if force_headers is None:
                    force_headers = ['alpha_id', 'source', 'source_url', 'category', 'title', 'description', 'actionable_steps', 'effort_level', 'roi_potential', 'risk_level', 'applies_to_niches', 'status', 'reviewed_date', 'reviewer_notes']
                headers = force_headers
                reader = csv.DictReader(lines, fieldnames=force_headers)
                for row in reader:
                    rows.append(row)
            else:
                reader = csv.DictReader(lines)
                headers = reader.fieldnames or []
                for row in reader:
                    rows.append(row)
    except Exception as e:
        print(f"  ERROR reading {filepath}: {e}")
        return [], []
    print(f"  OK: {filepath} ({len(rows)} rows, {len(headers)} cols)")
    return rows, headers

def write_csv(filepath, rows, fieldnames):
    """Write rows to CSV with given fieldnames."""
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"  WROTE: {filepath} ({len(rows)} rows, {len(fieldnames)} cols)")

def get_source_basename(filepath):
    return os.path.basename(filepath)

def merge_rows_add_source(filepath):
    """Read CSV and add source_file column."""
    rows, headers = read_csv_safe(filepath)
    basename = get_source_basename(filepath)
    for row in rows:
        row['source_file'] = basename
    if 'source_file' not in headers:
        headers.append('source_file')
    return rows, headers

def union_headers(*header_lists):
    """Get union of all headers preserving order."""
    seen = set()
    result = []
    for hlist in header_lists:
        for h in hlist:
            if h not in seen:
                seen.add(h)
                result.append(h)
    return result


# ============================================================
# TAB 1: MONEY_METHODS_MASTER
# ============================================================
def build_tab1():
    print("\n=== TAB 1: MONEY_METHODS_MASTER ===")

    # Read money methods tracker
    mm_rows, mm_headers = merge_rows_add_source(os.path.join(BASE, "MONEY_METHODS_TRACKER.csv"))

    # Read cross-pollination matrix
    cp_rows, cp_headers = read_csv_safe(os.path.join(BASE, "CROSS_POLLINATION_MATRIX_UPDATED.csv"))

    # Build lookup from cross-pollination by method_id
    cp_lookup = {}
    for row in cp_rows:
        mid = row.get('method_id', '')
        cp_lookup[mid] = row

    # Parse monthly_potential into low/high
    # Some rows have format "$1k-50k", some have just a number
    for row in mm_rows:
        mp = row.get('monthly_potential', '') or ''
        row['monthly_potential_low'] = ''
        row['monthly_potential_high'] = ''
        if '-' in mp:
            parts = mp.split('-')
            row['monthly_potential_low'] = parts[0].strip()
            row['monthly_potential_high'] = parts[1].strip() if len(parts) > 1 else ''
        elif mp:
            row['monthly_potential_low'] = mp
            row['monthly_potential_high'] = mp

        # Add cross-pollination data
        mid = row.get('method_id', '')
        cp_data = cp_lookup.get(mid, {})
        row['stacks_with'] = cp_data.get('synergy_partners', '')
        row['synergy_score'] = cp_data.get('synergy_score', '')
        row['synergy_type'] = cp_data.get('synergy_type', '')
        row['cross_sell_products'] = cp_data.get('cross_sell_products', '')
        row['shared_audience'] = cp_data.get('shared_audience', '')
        row['automation_combo'] = cp_data.get('automation_combo', '')
        row['revenue_multiplier'] = cp_data.get('revenue_multiplier', '')
        row['synergy_notes'] = cp_data.get('notes', '')

    # Build final headers
    final_headers = list(mm_headers)
    for h in ['monthly_potential_low', 'monthly_potential_high', 'stacks_with', 'synergy_score',
              'synergy_type', 'cross_sell_products', 'shared_audience', 'automation_combo',
              'revenue_multiplier', 'synergy_notes']:
        if h not in final_headers:
            final_headers.append(h)

    write_csv(os.path.join(OUT, "TAB1_MONEY_METHODS_MASTER.csv"), mm_rows, final_headers)


# ============================================================
# TAB 2: NICHES_MASTER
# ============================================================
def build_tab2():
    print("\n=== TAB 2: NICHES_MASTER ===")

    rows1, h1 = merge_rows_add_source(os.path.join(BASE, "NICHES.csv"))
    rows2, h2 = merge_rows_add_source(os.path.join(BASE, "NICHES_NEW_ENTRIES.csv"))

    # Deduplicate by niche_id
    seen_ids = set()
    final_rows = []
    for row in rows1:
        nid = row.get('niche_id', row.get(h1[0] if h1 else '', ''))
        if nid and nid not in seen_ids:
            seen_ids.add(nid)
            final_rows.append(row)
        elif not nid:
            final_rows.append(row)

    for row in rows2:
        nid = row.get('niche_id', '')
        # Try first column if niche_id not found
        if not nid and h2:
            nid = row.get(h2[0], '')
        if nid and nid not in seen_ids:
            seen_ids.add(nid)
            final_rows.append(row)

    headers = union_headers(h1, h2)
    write_csv(os.path.join(OUT, "TAB2_NICHES_MASTER.csv"), final_rows, headers)


# ============================================================
# TAB 3: ALPHA_MASTER
# ============================================================
def build_tab3():
    print("\n=== TAB 3: ALPHA_MASTER ===")

    files = [
        os.path.join(BASE, "ALPHA_STAGING.csv"),
        os.path.join(BASE, "ALPHA_STAGING_NEW.csv"),
        os.path.join(BASE, "ALPHA_STAGING_NEW_ENTRIES.csv"),
        os.path.join(BASE, "ALPHA_STAGING_NEW_BATCH.csv"),
        os.path.join(BASE, "ALPHA_HUNTER_FINDINGS.csv"),
        os.path.join(BASE, "AI_INFLUENCER_RESEARCH_FINDINGS.csv"),
    ]

    all_rows = []
    all_headers = []

    for filepath in files:
        rows, headers = merge_rows_add_source(filepath)
        all_rows.extend(rows)
        all_headers.append(headers)

    headers = union_headers(*all_headers)

    # Deduplicate by alpha_id AND source_url
    seen_keys = set()
    final_rows = []
    for row in all_rows:
        aid = row.get('alpha_id', row.get('finding_id', ''))
        surl = row.get('source_url', '')
        key = (aid, surl)
        # Also check just alpha_id for exact dupes
        if aid and key in seen_keys:
            continue
        if aid:
            seen_keys.add(key)
        final_rows.append(row)

    write_csv(os.path.join(OUT, "TAB3_ALPHA_MASTER.csv"), final_rows, headers)


# ============================================================
# TAB 4: TOOLS_CHANNELS_MASTER
# ============================================================
def build_tab4():
    print("\n=== TAB 4: TOOLS_CHANNELS_MASTER ===")

    # Tools
    rows1, h1 = merge_rows_add_source(os.path.join(BASE, "TOOLS_SERVICES_MASTER.csv"))
    for r in rows1:
        r['record_type'] = 'tool'

    # Channels
    rows2, h2 = merge_rows_add_source(os.path.join(BASE, "MARKETING_CHANNELS_MASTER.csv"))
    for r in rows2:
        r['record_type'] = 'channel'

    # MCP Servers
    rows3, h3 = merge_rows_add_source(os.path.join(BASE, "MCP_SERVER_ECOSYSTEM.csv"))
    for r in rows3:
        r['record_type'] = 'mcp_server'

    all_rows = rows1 + rows2 + rows3
    headers = union_headers(h1, h2, h3)
    if 'record_type' not in headers:
        headers.insert(0, 'record_type')

    write_csv(os.path.join(OUT, "TAB4_TOOLS_CHANNELS_MASTER.csv"), all_rows, headers)


# ============================================================
# TAB 5: CONTENT_MASTER
# ============================================================
def build_tab5():
    print("\n=== TAB 5: CONTENT_MASTER ===")

    files = [
        os.path.join(BASE, "CONTENT_PIPELINE.csv"),
        os.path.join(BASE, "CONTENT_CALENDAR_2026.csv"),
        os.path.join(BASE, "WINNING_CONTENT_STRUCTURES.csv"),
        os.path.join(BASE, "NEW_CONTENT_STRUCTURES_2026-01-24.csv"),
        os.path.join(BASE, "HASHTAG_LIBRARY.csv"),
    ]

    all_rows = []
    all_headers = []

    for filepath in files:
        rows, headers = merge_rows_add_source(filepath)
        # Add content_section tag
        basename = get_source_basename(filepath)
        if 'PIPELINE' in basename.upper():
            section = 'pipeline'
        elif 'CALENDAR' in basename.upper():
            section = 'calendar'
        elif 'CONTENT_STRUCTURES' in basename.upper() or 'WINNING' in basename.upper():
            section = 'content_structure'
        elif 'HASHTAG' in basename.upper():
            section = 'hashtag_library'
        else:
            section = 'other'
        for r in rows:
            r['content_section'] = section
        if 'content_section' not in headers:
            headers.append('content_section')
        all_rows.extend(rows)
        all_headers.append(headers)

    # Deduplicate content structures by structure_id
    seen_sids = set()
    final_rows = []
    for row in all_rows:
        sid = row.get('structure_id', '')
        if sid:
            if sid in seen_sids:
                continue
            seen_sids.add(sid)
        final_rows.append(row)

    headers = union_headers(*all_headers)
    if 'content_section' not in headers:
        headers.insert(0, 'content_section')

    write_csv(os.path.join(OUT, "TAB5_CONTENT_MASTER.csv"), final_rows, headers)


# ============================================================
# TAB 6: APPS_ECOM_MASTER
# ============================================================
def build_tab6():
    print("\n=== TAB 6: APPS_ECOM_MASTER ===")

    files = [
        os.path.join(BASE, "APP_FACTORY_METHODS.csv"),
        os.path.join(BASE, "APP_CLONE_OPPORTUNITIES.csv"),
        os.path.join(BASE, "ECOM_ARB_OPPORTUNITIES.csv"),
        os.path.join(BASE, "MICRO_SAAS_IDEAS.csv"),
    ]

    all_rows = []
    all_headers = []

    for filepath in files:
        rows, headers = merge_rows_add_source(filepath)
        # Add section tag
        basename = get_source_basename(filepath)
        if 'APP_FACTORY' in basename.upper():
            section = 'app_factory_method'
        elif 'CLONE' in basename.upper():
            section = 'app_clone_opportunity'
        elif 'ECOM' in basename.upper():
            section = 'ecom_arb_opportunity'
        elif 'MICRO_SAAS' in basename.upper():
            section = 'micro_saas_idea'
        else:
            section = 'other'
        for r in rows:
            r['record_section'] = section
        if 'record_section' not in headers:
            headers.append('record_section')
        all_rows.extend(rows)
        all_headers.append(headers)

    headers = union_headers(*all_headers)
    if 'record_section' not in headers:
        headers.insert(0, 'record_section')

    write_csv(os.path.join(OUT, "TAB6_APPS_ECOM_MASTER.csv"), all_rows, headers)


# ============================================================
# TAB 7: SOURCES_ACCOUNTS
# ============================================================
def build_tab7():
    print("\n=== TAB 7: SOURCES_ACCOUNTS ===")

    rows1, h1 = merge_rows_add_source(os.path.join(BASE, "HIGH_SIGNAL_SOURCES.csv"))
    for r in rows1:
        r['record_type'] = 'signal_source'

    rows2, h2 = merge_rows_add_source(os.path.join(BASE, "ACCOUNTS.csv"))
    for r in rows2:
        r['record_type'] = 'account'

    all_rows = rows1 + rows2
    headers = union_headers(h1, h2)
    if 'record_type' not in headers:
        headers.insert(0, 'record_type')

    write_csv(os.path.join(OUT, "TAB7_SOURCES_ACCOUNTS.csv"), all_rows, headers)


# ============================================================
# TAB 8: OPERATIONS
# ============================================================
def build_tab8():
    print("\n=== TAB 8: OPERATIONS ===")

    files = [
        os.path.join(BASE, "GTM_OPTIMIZATION_PRIORITIES.csv"),
        os.path.join(BASE, "AFFILIATES_MASTER.csv"),
        os.path.join(BASE, "OUTREACH_PIPELINE.csv"),
        os.path.join(BASE, "WARMUP_DEVICE_MATRIX.csv"),
    ]

    all_rows = []
    all_headers = []

    for filepath in files:
        rows, headers = merge_rows_add_source(filepath)
        basename = get_source_basename(filepath)
        if 'GTM' in basename.upper():
            section = 'gtm_priorities'
        elif 'AFFILIATES' in basename.upper():
            section = 'affiliates'
        elif 'OUTREACH' in basename.upper():
            section = 'outreach_pipeline'
        elif 'WARMUP' in basename.upper():
            section = 'warmup_matrix'
        else:
            section = 'other'
        for r in rows:
            r['ops_section'] = section
        if 'ops_section' not in headers:
            headers.append('ops_section')
        all_rows.extend(rows)
        all_headers.append(headers)

    headers = union_headers(*all_headers)
    if 'ops_section' not in headers:
        headers.insert(0, 'ops_section')

    write_csv(os.path.join(OUT, "TAB8_OPERATIONS.csv"), all_rows, headers)


# ============================================================
# TAB 9: EXPERIMENTS_METRICS
# ============================================================
def build_tab9():
    print("\n=== TAB 9: EXPERIMENTS_METRICS ===")

    files = [
        os.path.join(BASE, "AB_TESTS_MASTER.csv"),
        os.path.join(BASE, "AB_EXPERIMENTS_MASTER.csv"),
        os.path.join(BASE, "EXPERIMENTS_AB.csv"),
        os.path.join(BASE, "FUNNEL_METRICS.csv"),
        os.path.join(BASE, "METRICS_DASH.csv"),
        os.path.join(BASE, "COMPLIANCE_LOG.csv"),
    ]

    all_rows = []
    all_headers = []

    for filepath in files:
        rows, headers = merge_rows_add_source(filepath)
        basename = get_source_basename(filepath)
        if 'AB_TESTS' in basename.upper():
            section = 'ab_tests'
        elif 'AB_EXPERIMENTS' in basename.upper():
            section = 'ab_experiments'
        elif 'EXPERIMENTS_AB' in basename.upper():
            section = 'experiments_ab'
        elif 'FUNNEL' in basename.upper():
            section = 'funnel_metrics'
        elif 'METRICS_DASH' in basename.upper():
            section = 'metrics_dashboard'
        elif 'COMPLIANCE' in basename.upper():
            section = 'compliance_log'
        else:
            section = 'other'
        for r in rows:
            r['data_section'] = section
        if 'data_section' not in headers:
            headers.append('data_section')
        all_rows.extend(rows)
        all_headers.append(headers)

    headers = union_headers(*all_headers)
    if 'data_section' not in headers:
        headers.insert(0, 'data_section')

    write_csv(os.path.join(OUT, "TAB9_EXPERIMENTS_METRICS.csv"), all_rows, headers)


# ============================================================
# TAB 10: RESEARCH_MISC
# ============================================================
def build_tab10():
    print("\n=== TAB 10: RESEARCH_MISC ===")

    files = [
        os.path.join(BASE, "COMPREHENSIVE_RESEARCH_2026-01-25.csv"),
        os.path.join(BASE, "CONTENT_FARM_ALPHA_2026-01-24.csv"),
        os.path.join(BASE, "SEO_GEO_ASO_RESEARCH_2026.csv"),
        os.path.join(BASE, "SCRAPED_TWEETS_ALPHA.csv"),
        os.path.join(BASE, "GITHUB_CLAUDE_REPOS.csv"),
        os.path.join(BASE, "NEW_STACKS_CSV_IMPORT.csv"),
    ]

    all_rows = []
    all_headers = []

    for filepath in files:
        rows, headers = merge_rows_add_source(filepath)
        basename = get_source_basename(filepath)
        if 'COMPREHENSIVE' in basename.upper():
            section = 'comprehensive_research'
        elif 'CONTENT_FARM' in basename.upper():
            section = 'content_farm_alpha'
        elif 'SEO_GEO' in basename.upper():
            section = 'seo_geo_aso_research'
        elif 'SCRAPED_TWEETS' in basename.upper():
            section = 'scraped_tweets'
        elif 'GITHUB' in basename.upper():
            section = 'github_repos'
        elif 'NEW_STACKS' in basename.upper():
            section = 'new_stacks'
        else:
            section = 'other'
        for r in rows:
            r['research_section'] = section
        if 'research_section' not in headers:
            headers.append('research_section')
        all_rows.extend(rows)
        all_headers.append(headers)

    headers = union_headers(*all_headers)
    if 'research_section' not in headers:
        headers.insert(0, 'research_section')

    write_csv(os.path.join(OUT, "TAB10_RESEARCH_MISC.csv"), all_rows, headers)


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("PRINTMAXX MEGA SHEET BUILDER")
    print("=" * 60)

    build_tab1()
    build_tab2()
    build_tab3()
    build_tab4()
    build_tab5()
    build_tab6()
    build_tab7()
    build_tab8()
    build_tab9()
    build_tab10()

    print("\n" + "=" * 60)
    print("COMPLETE. Files written to:")
    print(OUT)
    print("=" * 60)

    # List output files
    for f in sorted(os.listdir(OUT)):
        if f.endswith('.csv'):
            fpath = os.path.join(OUT, f)
            size = os.path.getsize(fpath)
            print(f"  {f}: {size:,} bytes")
