#!/usr/bin/env python3
"""
Method Stack Calculator - Find optimal method combinations.

Analyzes CROSS_POLLINATION_MATRIX.csv to find highest-synergy stacks
and calculate revenue multipliers.

Usage:
    python3 method_stack_calculator.py top          # Top 10 stacks
    python3 method_stack_calculator.py for MM001    # Best stacks including MM001
    python3 method_stack_calculator.py niche faith  # Best stacks for faith niche
    python3 method_stack_calculator.py roi          # ROI-ranked stacks
    python3 method_stack_calculator.py graph        # Show method connection graph
"""

import csv
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_DIR / "LEDGER"


def load_cross_pollination() -> List[Dict]:
    """Load cross-pollination matrix."""
    filepath = LEDGER_DIR / "CROSS_POLLINATION_MATRIX.csv"
    if not filepath.exists():
        filepath = LEDGER_DIR / "CROSS_POLLINATION_MATRIX_UPDATED.csv"
    if not filepath.exists():
        print("Error: CROSS_POLLINATION_MATRIX.csv not found")
        return []

    rows = []
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def load_methods() -> Dict[str, Dict]:
    """Load method tracker."""
    filepath = LEDGER_DIR / "MONEY_METHODS_TRACKER.csv"
    if not filepath.exists():
        # Try MEGA_SHEET
        filepath = LEDGER_DIR / "MEGA_SHEET" / "TAB1_MONEY_METHODS_MASTER.csv"
    if not filepath.exists():
        return {}

    methods = {}
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mid = row.get('method_id', '')
            if mid:
                methods[mid] = row
    return methods


def get_synergy_score(row: Dict) -> int:
    """Extract synergy score from a cross-pollination row."""
    for key in ['synergy_score', 'score', 'synergy']:
        val = row.get(key, '')
        try:
            return int(float(val))
        except (ValueError, TypeError):
            continue
    return 0


def cmd_top(args):
    """Show top method stacks by synergy score."""
    rows = load_cross_pollination()
    if not rows:
        return

    # Sort by synergy score
    scored = [(row, get_synergy_score(row)) for row in rows]
    scored.sort(key=lambda x: -x[1])

    limit = args.limit if hasattr(args, 'limit') else 10

    print(f"\n{'Rank':<6} {'Method':<20} {'Partners':<25} {'Synergy':<10} {'Notes'}")
    print("-" * 90)

    for i, (row, score) in enumerate(scored[:limit], 1):
        # Support both formats: method_1/method_2 and method_id/synergy_partners
        m1 = row.get('method_id', row.get('method_1', row.get('primary_method', 'N/A')))
        m2 = row.get('synergy_partners', row.get('method_2', row.get('secondary_method', 'N/A')))
        notes = row.get('notes', row.get('description', ''))[:35]
        print(f"{i:<6} {m1:<20} {str(m2)[:23]:<25} {score:<10} {notes}")


def cmd_for_method(args):
    """Find best stacks including a specific method."""
    method = args.method.upper()
    rows = load_cross_pollination()
    if not rows:
        return

    matching = []
    for row in rows:
        # Support both CSV formats
        m1 = row.get('method_id', row.get('method_1', row.get('primary_method', '')))
        m2 = row.get('synergy_partners', row.get('method_2', row.get('secondary_method', '')))

        if method in m1.upper() or method in m2.upper():
            score = get_synergy_score(row)
            partner = m2 if method in m1.upper() else m1
            matching.append((partner, score, row))

    matching.sort(key=lambda x: -x[1])

    print(f"\nBest stacks for {method}:")
    print(f"\n{'Partner':<30} {'Synergy':<10} {'Notes'}")
    print("-" * 70)

    for partner, score, row in matching[:15]:
        notes = row.get('notes', row.get('description', ''))[:35]
        print(f"{partner:<30} {score:<10} {notes}")

    if not matching:
        print(f"No stacks found for {method}")


def cmd_niche(args):
    """Find best stacks for a specific niche."""
    niche = args.niche.lower()
    rows = load_cross_pollination()
    if not rows:
        return

    matching = []
    for row in rows:
        row_text = ' '.join(str(v) for v in row.values()).lower()
        if niche in row_text:
            score = get_synergy_score(row)
            m1 = row.get('method_1', row.get('primary_method', 'N/A'))
            m2 = row.get('method_2', row.get('secondary_method', 'N/A'))
            matching.append((m1, m2, score, row))

    matching.sort(key=lambda x: -x[2])

    print(f"\nBest stacks for '{niche}' niche:")
    print(f"\n{'Method 1':<25} {'Method 2':<25} {'Synergy':<10}")
    print("-" * 65)

    for m1, m2, score, row in matching[:15]:
        print(f"{m1:<25} {m2:<25} {score:<10}")

    if not matching:
        print(f"No stacks found for niche '{niche}'")


def cmd_roi(args):
    """ROI-ranked stacks based on effort vs potential."""
    rows = load_cross_pollination()
    methods = load_methods()

    if not rows:
        return

    # Score based on synergy + method status
    scored_stacks = []
    for row in rows:
        synergy = get_synergy_score(row)
        m1 = row.get('method_1', row.get('primary_method', ''))
        m2 = row.get('method_2', row.get('secondary_method', ''))

        # Boost score if methods are already active
        boost = 0
        for mid in [m1, m2]:
            if mid in methods:
                status = methods[mid].get('status', '').lower()
                if status == 'active':
                    boost += 10
                elif status == 'planning':
                    boost += 5

        total_score = synergy + boost
        scored_stacks.append((m1, m2, synergy, boost, total_score, row))

    scored_stacks.sort(key=lambda x: -x[4])

    print(f"\nROI-Ranked Method Stacks:")
    print(f"\n{'Rank':<6} {'Method 1':<22} {'Method 2':<22} {'Synergy':<10} {'Boost':<8} {'Total'}")
    print("-" * 75)

    for i, (m1, m2, synergy, boost, total, row) in enumerate(scored_stacks[:15], 1):
        print(f"{i:<6} {m1:<22} {m2:<22} {synergy:<10} +{boost:<7} {total}")


def cmd_graph(args):
    """Show method connection graph (text-based)."""
    rows = load_cross_pollination()
    if not rows:
        return

    connections = defaultdict(list)
    for row in rows:
        m1 = row.get('method_1', row.get('primary_method', ''))
        m2 = row.get('method_2', row.get('secondary_method', ''))
        score = get_synergy_score(row)
        if score >= 70:  # Only show strong connections
            connections[m1].append((m2, score))
            connections[m2].append((m1, score))

    print(f"\nMethod Connection Graph (synergy >= 70):\n")

    for method in sorted(connections.keys()):
        partners = sorted(connections[method], key=lambda x: -x[1])[:5]
        partner_str = ", ".join(f"{p}({s})" for p, s in partners)
        print(f"  {method}")
        for partner, score in partners:
            bar = "#" * (score // 10)
            print(f"    -> {partner:<25} [{bar:<10}] {score}")
        print()


def main():
    parser = argparse.ArgumentParser(description='Method Stack Calculator')
    subparsers = parser.add_subparsers(dest='command')

    # top
    sub_top = subparsers.add_parser('top', help='Top method stacks')
    sub_top.add_argument('--limit', type=int, default=10)

    # for
    sub_for = subparsers.add_parser('for', help='Stacks for a method')
    sub_for.add_argument('method', help='Method ID (e.g. MM001)')

    # niche
    sub_niche = subparsers.add_parser('niche', help='Stacks for a niche')
    sub_niche.add_argument('niche', help='Niche name (e.g. faith, fitness)')

    # roi
    subparsers.add_parser('roi', help='ROI-ranked stacks')

    # graph
    subparsers.add_parser('graph', help='Method connection graph')

    args = parser.parse_args()

    if args.command == 'top':
        cmd_top(args)
    elif args.command == 'for':
        cmd_for_method(args)
    elif args.command == 'niche':
        cmd_niche(args)
    elif args.command == 'roi':
        cmd_roi(args)
    elif args.command == 'graph':
        cmd_graph(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
