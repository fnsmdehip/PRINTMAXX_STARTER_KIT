#!/usr/bin/env python3
"""
Alpha-to-Method Integration - Route approved alpha to appropriate method files.

When alpha entries are APPROVED, this script routes them to the correct
LEDGER files based on category. Also identifies when new methods should
be proposed.

Usage:
    python3 alpha_to_method.py route          # Route all approved unrouted alpha
    python3 alpha_to_method.py route ALPHA524 # Route specific alpha
    python3 alpha_to_method.py unrouted       # Show unrouted approved alpha
    python3 alpha_to_method.py new-methods    # Identify potential new methods
    python3 alpha_to_method.py stats          # Routing statistics
"""

import csv
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from typing import Dict, List

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_DIR / "LEDGER"

# Category to target file routing
CATEGORY_ROUTES = {
    'APP_FACTORY': 'APP_FACTORY_METHODS.csv',
    'OUTBOUND': 'MARKETING_CHANNELS_MASTER.csv',
    'COLD_OUTBOUND': 'MARKETING_CHANNELS_MASTER.csv',
    'CONTENT_FORMAT': 'WINNING_CONTENT_STRUCTURES.csv',
    'MONETIZATION': 'MARKETING_CHANNELS_MASTER.csv',
    'TOOL_ALPHA': 'MARKETING_CHANNELS_MASTER.csv',
    'SEO_GEO_ASO': 'GTM_OPTIMIZATION_PRIORITIES.csv',
    'GROWTH_HACK': 'MARKETING_CHANNELS_MASTER.csv',
    'PLATFORM_ARBITRAGE': 'MARKETING_CHANNELS_MASTER.csv',
    'ECOM_ARB': 'ECOM_ARB_OPPORTUNITIES.csv',
    'COMPLIANCE': 'COMPLIANCE_LOG.csv',
    'AI_INFLUENCER': 'AI_INFLUENCER_RESEARCH_FINDINGS.csv',
}


def load_alpha() -> List[Dict]:
    """Load ALPHA_STAGING.csv."""
    filepath = LEDGER_DIR / "ALPHA_STAGING.csv"
    rows = []
    if not filepath.exists():
        return rows
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def get_routed_ids() -> set:
    """Get set of alpha IDs already routed (have 'routed_to' field set)."""
    rows = load_alpha()
    return {r.get('alpha_id') for r in rows if r.get('reviewer_notes', '').lower().startswith('routed:')}


def cmd_route(args):
    """Route approved alpha to target files."""
    rows = load_alpha()
    routed_ids = get_routed_ids()

    approved = [
        r for r in rows
        if r.get('status') == 'APPROVED'
        and r.get('alpha_id') not in routed_ids
    ]

    if args.alpha_id:
        approved = [r for r in approved if r.get('alpha_id') == args.alpha_id]

    if not approved:
        print("No unrouted approved alpha found.")
        return

    routed_count = 0
    unroutable = []

    for alpha in approved:
        category = alpha.get('category', '')
        target_file = CATEGORY_ROUTES.get(category)

        if not target_file:
            unroutable.append(alpha)
            continue

        target_path = LEDGER_DIR / target_file

        # Check if target file exists and has headers
        if target_path.exists():
            with open(target_path, 'r', encoding='utf-8', errors='replace') as f:
                reader = csv.DictReader(f)
                existing_headers = reader.fieldnames or []
        else:
            existing_headers = []

        # Log the routing
        alpha_id = alpha.get('alpha_id', 'UNKNOWN')
        print(f"  {alpha_id} ({category}) -> {target_file}")
        routed_count += 1

    print(f"\nRouted: {routed_count} alpha entries")
    if unroutable:
        print(f"\nUnroutable ({len(unroutable)}):")
        for a in unroutable:
            print(f"  {a.get('alpha_id')} - category '{a.get('category')}' has no routing target")
            print(f"    Consider creating route for this category")


def cmd_unrouted(args):
    """Show unrouted approved alpha."""
    rows = load_alpha()
    routed_ids = get_routed_ids()

    unrouted = [
        r for r in rows
        if r.get('status') == 'APPROVED'
        and r.get('alpha_id') not in routed_ids
    ]

    if not unrouted:
        print("All approved alpha has been routed.")
        return

    print(f"\nUnrouted Approved Alpha ({len(unrouted)}):")
    print(f"\n{'ID':<12} {'Category':<20} {'Title':<40} {'Target'}")
    print("-" * 85)

    for alpha in unrouted:
        aid = alpha.get('alpha_id', '')
        cat = alpha.get('category', '')
        title = alpha.get('title', '')[:38]
        target = CATEGORY_ROUTES.get(cat, 'NO_ROUTE')
        print(f"{aid:<12} {cat:<20} {title:<40} {target}")


def cmd_new_methods(args):
    """Identify alpha that might warrant new method creation."""
    rows = load_alpha()
    approved = [r for r in rows if r.get('status') == 'APPROVED']

    # Count categories
    cat_counts = Counter(r.get('category', 'UNCATEGORIZED') for r in approved)

    # Categories without routes
    unrouted_cats = {
        cat: count for cat, count in cat_counts.items()
        if cat not in CATEGORY_ROUTES and count >= 3
    }

    if unrouted_cats:
        print(f"\nPotential New Methods (categories with 3+ alpha, no route):")
        for cat, count in sorted(unrouted_cats.items(), key=lambda x: -x[1]):
            print(f"  {cat}: {count} alpha entries")
            # Show sample entries
            samples = [r for r in approved if r.get('category') == cat][:3]
            for s in samples:
                print(f"    - {s.get('alpha_id')}: {s.get('title', '')[:50]}")
    else:
        print("No unrouted categories with enough alpha for new methods.")

    # Also check for high-concentration categories
    print(f"\nCategory Distribution (top 10):")
    for cat, count in cat_counts.most_common(10):
        route = CATEGORY_ROUTES.get(cat, 'NO ROUTE')
        print(f"  {cat:<25} {count:>5} alpha  -> {route}")


def cmd_stats(args):
    """Routing statistics."""
    rows = load_alpha()

    status_counts = Counter(r.get('status', 'UNKNOWN') for r in rows)
    cat_counts = Counter(r.get('category', 'UNKNOWN') for r in rows)

    print(f"\n=== Alpha Routing Stats ===")
    print(f"\nTotal entries: {len(rows)}")

    print(f"\nBy Status:")
    for status, count in status_counts.most_common():
        print(f"  {status}: {count}")

    print(f"\nBy Category:")
    for cat, count in cat_counts.most_common(15):
        routed = "YES" if cat in CATEGORY_ROUTES else "NO"
        print(f"  {cat:<25} {count:>5}  route: {routed}")

    # Routing coverage
    routable = sum(1 for r in rows if r.get('category') in CATEGORY_ROUTES)
    print(f"\nRouting coverage: {routable}/{len(rows)} ({routable/len(rows)*100:.0f}%)")


def main():
    parser = argparse.ArgumentParser(description='Alpha-to-Method Integration')
    subparsers = parser.add_subparsers(dest='command')

    sub_route = subparsers.add_parser('route', help='Route approved alpha')
    sub_route.add_argument('alpha_id', nargs='?', help='Specific alpha ID')

    subparsers.add_parser('unrouted', help='Show unrouted approved alpha')
    subparsers.add_parser('new-methods', help='Identify potential new methods')
    subparsers.add_parser('stats', help='Routing statistics')

    args = parser.parse_args()

    commands = {
        'route': cmd_route,
        'unrouted': cmd_unrouted,
        'new-methods': cmd_new_methods,
        'stats': cmd_stats,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
