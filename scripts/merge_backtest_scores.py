#!/usr/bin/env python3
"""
Merge backtest scores from BACKTEST_RESULTS.csv into ALPHA_STAGING.csv
and append new alpha entries from NEW_ALPHA_DISCOVERED.csv.

This script:
1. Reads backtest results and builds alpha_id -> (best_score, decision) lookup
2. Reads ALPHA_STAGING.csv
3. Appends backtest_score and backtest_decision to reviewer_notes for matched entries
4. Appends 10 new alpha entries from NEW_ALPHA_DISCOVERED.csv
5. Writes updated ALPHA_STAGING.csv
"""

import csv
import os
import sys
from datetime import datetime
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = str(PROJECT_ROOT)
BACKTEST_FILE = os.path.join(BASE_DIR, "LEDGER/BACKTESTS/BACKTEST_RESULTS.csv")
ALPHA_STAGING_FILE = os.path.join(BASE_DIR, "LEDGER/ALPHA_STAGING.csv")
NEW_ALPHA_FILE = os.path.join(BASE_DIR, "OPS/NEW_ALPHA_DISCOVERED.csv")

def load_backtest_results():
    """Load backtest results, keeping the BEST score per alpha_id."""
    scores = {}
    with open(BACKTEST_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            alpha_id = row['alpha_id'].strip()
            score = int(row['backtest_score'])
            decision = row['decision'].strip()
            # Keep the best score for each alpha_id (duplicates exist)
            if alpha_id not in scores or score > scores[alpha_id][0]:
                scores[alpha_id] = (score, decision)
    return scores

def load_new_alpha():
    """Load new alpha entries from NEW_ALPHA_DISCOVERED.csv."""
    entries = []
    with open(NEW_ALPHA_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(row)
    return entries

def find_next_alpha_id(rows):
    """Find the next available numeric alpha ID."""
    max_id = 0
    for row in rows:
        alpha_id = row.get('alpha_id', '')
        # Only consider pure numeric ALPHA IDs (not hex ones)
        if alpha_id.startswith('ALPHA') and alpha_id[5:].isdigit():
            num = int(alpha_id[5:])
            if num > max_id:
                max_id = num
    # Also check backtest results for higher IDs
    with open(BACKTEST_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            alpha_id = row['alpha_id'].strip()
            if alpha_id.startswith('ALPHA') and alpha_id[5:].isdigit():
                num = int(alpha_id[5:])
                if num > max_id:
                    max_id = num
    return max_id + 1

def main():
    print(f"Loading backtest results from {BACKTEST_FILE}...")
    scores = load_backtest_results()
    print(f"  Loaded {len(scores)} unique alpha IDs with scores")

    # Show score distribution
    scale = sum(1 for s, d in scores.values() if d == 'SCALE')
    paper = sum(1 for s, d in scores.values() if d == 'PAPER_TRADE')
    kill = sum(1 for s, d in scores.values() if d == 'KILL')
    print(f"  Distribution: {scale} SCALE, {paper} PAPER_TRADE, {kill} KILL")

    print(f"\nLoading ALPHA_STAGING.csv...")
    rows = []
    fieldnames = None
    with open(ALPHA_STAGING_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)
    print(f"  Loaded {len(rows)} entries")

    # Merge backtest scores into reviewer_notes
    matched = 0
    for row in rows:
        alpha_id = row.get('alpha_id', '').strip()
        if alpha_id in scores:
            score, decision = scores[alpha_id]
            existing_notes = row.get('reviewer_notes', '') or ''
            # Don't add if already has backtest info
            if 'backtest_score:' not in existing_notes:
                if existing_notes:
                    new_notes = f"{existing_notes} | backtest_score:{score} backtest_decision:{decision}"
                else:
                    new_notes = f"backtest_score:{score} backtest_decision:{decision}"
                row['reviewer_notes'] = new_notes
                matched += 1

    print(f"  Updated {matched} entries with backtest scores")

    # Load new alpha entries
    print(f"\nLoading new alpha from {NEW_ALPHA_FILE}...")
    new_alpha = load_new_alpha()
    print(f"  Found {len(new_alpha)} new entries")

    # Find next available ID
    next_id = find_next_alpha_id(rows)
    print(f"  Next available alpha ID: ALPHA{next_id}")

    # Convert new alpha entries to ALPHA_STAGING format
    today = datetime.now().strftime('%Y-%m-%d')
    for i, entry in enumerate(new_alpha):
        new_row = {
            'alpha_id': f'ALPHA{next_id + i}',
            'source': entry.get('source', ''),
            'source_url': entry.get('source_url', ''),
            'category': entry.get('category', ''),
            'title': entry.get('title', ''),
            'description': entry.get('description', ''),
            'actionable_steps': entry.get('actionable_steps', ''),
            'effort_level': entry.get('effort_level', ''),
            'roi_potential': entry.get('roi_potential', ''),
            'risk_level': entry.get('risk_level', ''),
            'applies_to_niches': entry.get('applies_to_niches', ''),
            'status': 'PENDING_REVIEW',
            'reviewed_date': '',
            'reviewer_notes': f"confidence_score:{entry.get('confidence_score', '')} engagement_authenticity:{entry.get('engagement_authenticity', 'N/A')} earnings_verified:{entry.get('earnings_verified', 'N/A')} validation_sources:{entry.get('validation_sources', '')} cross_pollination:{entry.get('cross_pollination', '')} added_by:deep_alpha_research_{today}"
        }
        rows.append(new_row)
        print(f"  Added {new_row['alpha_id']}: {entry.get('title', '')[:60]}...")

    # Write updated ALPHA_STAGING.csv
    print(f"\nWriting updated ALPHA_STAGING.csv ({len(rows)} total entries)...")
    with open(ALPHA_STAGING_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"  Done! {matched} entries updated with backtest scores, {len(new_alpha)} new entries added.")
    print(f"\nSummary:")
    print(f"  Total entries: {len(rows)}")
    print(f"  Backtest scores merged: {matched}")
    print(f"  New alpha added: {len(new_alpha)} (ALPHA{next_id} - ALPHA{next_id + len(new_alpha) - 1})")
    print(f"  New entries IDs: {', '.join(f'ALPHA{next_id + i}' for i in range(len(new_alpha)))}")

if __name__ == '__main__':
    main()
