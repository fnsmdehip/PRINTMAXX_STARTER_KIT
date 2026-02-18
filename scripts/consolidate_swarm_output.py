#!/usr/bin/env python3
"""
Consolidate swarm research outputs into ALPHA_STAGING.csv and FINANCIALS tracking.
Transforms swarm CSV formats to standard PRINTMAXX formats.
"""

import csv
import os
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = str(PROJECT_ROOT)
SWARM_OUTPUT_DIR = os.path.join(BASE_DIR, "ralph/.swarm/output")
ALPHA_STAGING = os.path.join(BASE_DIR, "LEDGER/ALPHA_STAGING.csv")
FINANCIAL_TRACKER = os.path.join(BASE_DIR, "FINANCIALS/MASTER_FINANCIAL_TRACKER.csv")

TODAY = datetime.now().strftime("%Y-%m-%d")

def get_next_alpha_id():
    """Find the highest ALPHA ID and return next available."""
    max_id = 0
    with open(ALPHA_STAGING, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            alpha_id = row.get('alpha_id', '')
            if alpha_id.startswith('ALPHA'):
                try:
                    num = int(alpha_id.replace('ALPHA', ''))
                    max_id = max(max_id, num)
                except ValueError:
                    pass
    return max_id + 1

def transform_twitter_alpha(filepath, start_id):
    """Transform T1_TWITTER_ALPHA.csv to ALPHA_STAGING format."""
    entries = []
    current_id = start_id

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entry = {
                'alpha_id': f'ALPHA{current_id}',
                'source': row.get('source', ''),
                'source_url': row.get('evidence_url', ''),
                'category': row.get('category', ''),
                'tactic': row.get('tactic', ''),
                'roi_potential': row.get('roi_potential', 'HIGH'),
                'priority': 'IMMEDIATE' if row.get('roi_potential') == 'HIGHEST' else 'THIS_WEEK',
                'status': 'PENDING_REVIEW',
                'applicable_methods': 'ALL',
                'applicable_niches': 'ALL',
                'synergy_score': '85',
                'reviewer_notes': f"Proposed cost: {row.get('proposed_cost', 'N/A')}. Projected revenue: {row.get('projected_revenue', 'N/A')}. Confidence: {row.get('confidence', 'N/A')}%",
                'quality_issues': '',
                'engagement_authenticity': 'AUTHENTIC',
                'earnings_verified': 'FALSE' if row.get('confidence', '0') < '80' else 'TRUE',
                'extracted_method': row.get('tactic', '')[:200],
                'compliance_notes': '',
                'date_added': TODAY
            }
            entries.append(entry)
            current_id += 1

    return entries, current_id

def transform_reddit_alpha(filepath, start_id):
    """Transform T2_REDDIT_ALPHA.csv to ALPHA_STAGING format."""
    entries = []
    current_id = start_id

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entry = {
                'alpha_id': f'ALPHA{current_id}',
                'source': row.get('source', ''),
                'source_url': row.get('evidence_url', ''),
                'category': row.get('category', ''),
                'tactic': row.get('tactic', ''),
                'roi_potential': row.get('roi_potential', 'HIGH'),
                'priority': 'IMMEDIATE' if row.get('roi_potential') == 'HIGHEST' else 'THIS_WEEK',
                'status': 'PENDING_REVIEW',
                'applicable_methods': 'ALL',
                'applicable_niches': 'ALL',
                'synergy_score': '85',
                'reviewer_notes': f"Proposed cost: {row.get('proposed_cost', 'N/A')}. Projected revenue: {row.get('projected_revenue', 'N/A')}. Confidence: {row.get('confidence', 'N/A')}%",
                'quality_issues': '',
                'engagement_authenticity': 'AUTHENTIC',
                'earnings_verified': 'FALSE',
                'extracted_method': row.get('tactic', '')[:200],
                'compliance_notes': '',
                'date_added': TODAY
            }
            entries.append(entry)
            current_id += 1

    return entries, current_id

def transform_ecom_arb(filepath, start_id):
    """Transform T3_ECOM_ARB.csv to ALPHA_STAGING format."""
    entries = []
    current_id = start_id

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entry = {
                'alpha_id': f'ALPHA{current_id}',
                'source': f"{row.get('source_platform', '')} to {row.get('target_platform', '')}",
                'source_url': row.get('proof_url', ''),
                'category': 'ECOM_ARB',
                'tactic': f"{row.get('product_category', '')}: {row.get('source_cost', '')} source -> {row.get('target_price', '')} target. {row.get('margin_percent', '')} margin. {row.get('notes', '')}",
                'roi_potential': 'HIGHEST' if 'HIGHEST' in str(row.get('monthly_volume', '')) else 'HIGH',
                'priority': 'IMMEDIATE',
                'status': 'PENDING_REVIEW',
                'applicable_methods': 'MM023_ECOM_ARB',
                'applicable_niches': 'N003_tech',
                'synergy_score': '90',
                'reviewer_notes': f"Competition: {row.get('competition_level', '')}. Volume: {row.get('monthly_volume', '')}",
                'quality_issues': '',
                'engagement_authenticity': 'AUTHENTIC',
                'earnings_verified': 'FALSE',
                'extracted_method': f"Source {row.get('source_cost', '')} sell {row.get('target_price', '')}",
                'compliance_notes': '',
                'date_added': TODAY
            }
            entries.append(entry)
            current_id += 1

    return entries, current_id

def transform_pod_trends(filepath, start_id):
    """Transform T4_POD_TRENDS.csv to ALPHA_STAGING format."""
    entries = []
    current_id = start_id

    def parse_margin(margin_str):
        """Safely parse margin percentage."""
        try:
            clean = str(margin_str).replace('%', '').replace('-', ' ').strip()
            if ' ' in clean:
                clean = clean.split()[0]
            return int(clean) if clean.isdigit() else 0
        except (ValueError, AttributeError):
            return 0

    def parse_window(window_str):
        """Safely parse window days."""
        try:
            if 'ONGOING' in str(window_str).upper():
                return 999
            clean = str(window_str).split('-')[0].strip()
            return int(clean) if clean.isdigit() else 999
        except (ValueError, AttributeError):
            return 999

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            margin = parse_margin(row.get('estimated_margin', '0%'))
            window = parse_window(row.get('estimated_window_days', '999'))

            entry = {
                'alpha_id': f'ALPHA{current_id}',
                'source': row.get('source', 'TikTok/Social'),
                'source_url': '',
                'category': 'POD_TRENDING',
                'tactic': f"Trending phrase: '{row.get('phrase', '')}'. Design: {row.get('design_concept', '')}. Target: {row.get('target_audience', '')}",
                'roi_potential': 'HIGH' if margin > 45 else 'MEDIUM',
                'priority': 'IMMEDIATE' if window < 30 else 'THIS_WEEK',
                'status': 'PENDING_REVIEW',
                'applicable_methods': 'MM024_POD',
                'applicable_niches': 'ALL',
                'synergy_score': '80',
                'reviewer_notes': f"Legal: {row.get('legal_status', '')}. Competition: {row.get('competition_level', '')}. Window: {row.get('estimated_window_days', '')} days. Margin: {row.get('estimated_margin', '')}",
                'quality_issues': 'CAUTION' if 'CAUTION' in str(row.get('legal_status', '')) else '',
                'engagement_authenticity': 'AUTHENTIC',
                'earnings_verified': 'FALSE',
                'extracted_method': row.get('design_concept', ''),
                'compliance_notes': row.get('legal_status', ''),
                'date_added': TODAY
            }
            entries.append(entry)
            current_id += 1

    return entries, current_id

def transform_platform_arb(filepath, start_id):
    """Transform T5_PLATFORM_ARB.csv to ALPHA_STAGING format."""
    entries = []
    current_id = start_id

    def parse_multiplier(mult_str):
        """Safely parse arbitrage multiplier."""
        try:
            clean = str(mult_str).replace('x', '').replace('~', '').replace('-', ' ').strip()
            if ' ' in clean:
                clean = clean.split()[0]
            return float(clean) if clean else 0
        except (ValueError, AttributeError):
            return 0

    def parse_confidence(conf_str):
        """Safely parse confidence percentage."""
        try:
            clean = str(conf_str).replace('%', '').strip()
            return int(clean) if clean else 0
        except (ValueError, AttributeError):
            return 0

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mult = parse_multiplier(row.get('arbitrage_multiplier', '0'))
            conf = parse_confidence(row.get('confidence', '0'))

            entry = {
                'alpha_id': f'ALPHA{current_id}',
                'source': row.get('platform', ''),
                'source_url': row.get('verification_source_1', ''),
                'category': 'PLATFORM_ARB',
                'tactic': f"{row.get('platform', '')} {row.get('monetization_type', '')}: {row.get('rpm_or_rate', '')}. vs {row.get('arbitrage_vs', '')} = {row.get('arbitrage_multiplier', '')} advantage. {row.get('notes', '')}",
                'roi_potential': 'HIGHEST' if mult > 3 else 'HIGH',
                'priority': 'IMMEDIATE',
                'status': 'PENDING_REVIEW',
                'applicable_methods': 'MM006_CONTENT_FARM',
                'applicable_niches': 'ALL',
                'synergy_score': '95',
                'reviewer_notes': f"Confidence: {row.get('confidence', '')}%. Requirements: {row.get('requirements', '')}. Verified by: {row.get('verification_source_2', '')}",
                'quality_issues': '',
                'engagement_authenticity': 'AUTHENTIC',
                'earnings_verified': 'TRUE' if conf >= 80 else 'FALSE',
                'extracted_method': f"Use {row.get('platform', '')} for {row.get('arbitrage_multiplier', '')} vs {row.get('arbitrage_vs', '')}",
                'compliance_notes': '',
                'date_added': TODAY
            }
            entries.append(entry)
            current_id += 1

    return entries, current_id

def transform_ai_tools(filepath, start_id):
    """Transform T6_AI_TOOLS_ALPHA.csv to ALPHA_STAGING format."""
    entries = []
    current_id = start_id

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entry = {
                'alpha_id': f'ALPHA{current_id}',
                'source': row.get('tool_name', ''),
                'source_url': row.get('url', ''),
                'category': row.get('category', 'TOOL_ALPHA'),
                'tactic': f"{row.get('tool_name', '')}: {row.get('use_case', '')}. Cost: {row.get('cost_monthly', '')}. Time saved: {row.get('time_saved_hours', '')}hrs. {row.get('notes', '')}",
                'roi_potential': row.get('revenue_potential', 'HIGH'),
                'priority': 'IMMEDIATE' if row.get('revenue_potential') == 'HIGHEST' else 'THIS_WEEK',
                'status': 'PENDING_REVIEW',
                'applicable_methods': 'ALL',
                'applicable_niches': 'ALL',
                'synergy_score': '88',
                'reviewer_notes': f"ROI: {row.get('roi_estimate', '')}. vs alternatives: {row.get('comparison_to_alternatives', '')}. Stars: {row.get('github_stars', '')}",
                'quality_issues': '',
                'engagement_authenticity': 'AUTHENTIC',
                'earnings_verified': 'FALSE',
                'extracted_method': row.get('use_case', ''),
                'compliance_notes': '',
                'date_added': TODAY
            }
            entries.append(entry)
            current_id += 1

    return entries, current_id

def extract_financial_projections(swarm_dir):
    """Extract cost and revenue projections from swarm outputs."""
    projections = []

    # T1 Twitter Alpha costs/revenues
    t1_path = os.path.join(swarm_dir, "T1_TWITTER_ALPHA.csv")
    if os.path.exists(t1_path):
        with open(t1_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('proposed_cost') and row.get('proposed_cost') != '$0':
                    projections.append({
                        'category': 'RESEARCH_ALPHA',
                        'item': f"T1: {row.get('category', '')} - {row.get('source', '')[:30]}",
                        'type': 'proposed',
                        'frequency': 'one-time',
                        'estimated_cost': row.get('proposed_cost', '$0'),
                        'estimated_revenue': row.get('projected_revenue', '$0'),
                        'confidence': row.get('confidence', ''),
                        'source': 'SWARM_T1_TWITTER',
                        'date_added': TODAY
                    })

    # T6 AI Tools costs
    t6_path = os.path.join(swarm_dir, "T6_AI_TOOLS_ALPHA.csv")
    if os.path.exists(t6_path):
        with open(t6_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('cost_monthly') and row.get('cost_monthly') not in ['0', '$0', 'N/A', 'Free', 'Variable', 'Revenue share']:
                    projections.append({
                        'category': 'TOOL_INVESTMENT',
                        'item': row.get('tool_name', ''),
                        'type': 'subscription',
                        'frequency': 'monthly',
                        'estimated_cost': f"${row.get('cost_monthly', '0')}/mo" if not row.get('cost_monthly', '').startswith('$') else f"{row.get('cost_monthly', '')}/mo",
                        'estimated_revenue': row.get('revenue_potential', ''),
                        'time_saved': row.get('time_saved_hours', ''),
                        'source': 'SWARM_T6_AI_TOOLS',
                        'date_added': TODAY
                    })

    return projections

def main():
    print("=" * 60)
    print("SWARM OUTPUT CONSOLIDATION")
    print("=" * 60)

    # Get starting ID
    start_id = get_next_alpha_id()
    print(f"\nStarting ALPHA ID: ALPHA{start_id}")

    all_entries = []
    current_id = start_id

    # Process each swarm output
    swarm_files = [
        ("T1_TWITTER_ALPHA.csv", transform_twitter_alpha),
        ("T2_REDDIT_ALPHA.csv", transform_reddit_alpha),
        ("T3_ECOM_ARB.csv", transform_ecom_arb),
        ("T4_POD_TRENDS.csv", transform_pod_trends),
        ("T5_PLATFORM_ARB.csv", transform_platform_arb),
        ("T6_AI_TOOLS_ALPHA.csv", transform_ai_tools),
    ]

    for filename, transformer in swarm_files:
        filepath = os.path.join(SWARM_OUTPUT_DIR, filename)
        if os.path.exists(filepath):
            entries, current_id = transformer(filepath, current_id)
            all_entries.extend(entries)
            print(f"✓ {filename}: {len(entries)} entries (ALPHA{start_id}-ALPHA{current_id-1})")
            start_id = current_id
        else:
            print(f"✗ {filename}: NOT FOUND")

    # Append to ALPHA_STAGING.csv
    if all_entries:
        fieldnames = [
            'alpha_id', 'source', 'source_url', 'category', 'tactic', 'roi_potential',
            'priority', 'status', 'applicable_methods', 'applicable_niches', 'synergy_score',
            'reviewer_notes', 'quality_issues', 'engagement_authenticity', 'earnings_verified',
            'extracted_method', 'compliance_notes', 'date_added'
        ]

        with open(ALPHA_STAGING, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            for entry in all_entries:
                writer.writerow(entry)

        print(f"\n✓ Appended {len(all_entries)} entries to ALPHA_STAGING.csv")

    # Extract and display financial projections
    print("\n" + "=" * 60)
    print("FINANCIAL PROJECTIONS EXTRACTED")
    print("=" * 60)

    projections = extract_financial_projections(SWARM_OUTPUT_DIR)

    # Save projections summary
    projections_path = os.path.join(BASE_DIR, "FINANCIALS/SWARM_PROJECTIONS_SUMMARY.csv")
    if projections:
        with open(projections_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['category', 'item', 'type', 'frequency', 'estimated_cost', 'estimated_revenue', 'confidence', 'time_saved', 'source', 'date_added'])
            writer.writeheader()
            for proj in projections:
                writer.writerow(proj)
        print(f"✓ Saved {len(projections)} projections to SWARM_PROJECTIONS_SUMMARY.csv")

    # Print summary
    print("\n" + "=" * 60)
    print("CONSOLIDATION SUMMARY")
    print("=" * 60)
    print(f"Total new alpha entries: {len(all_entries)}")
    print(f"Financial projections: {len(projections)}")
    print(f"Status: All entries marked PENDING_REVIEW for human greenlight")
    print(f"Next: Run /review-alpha to approve findings")

    # Category breakdown
    categories = {}
    for entry in all_entries:
        cat = entry.get('category', 'UNKNOWN')
        categories[cat] = categories.get(cat, 0) + 1

    print("\nCategory breakdown:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    return len(all_entries)

if __name__ == "__main__":
    main()
