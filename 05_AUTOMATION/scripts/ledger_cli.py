#!/usr/bin/env python3
"""
LEDGER Query CLI - Fast querying across all PRINTMAXX LEDGER CSV files.

Usage:
    python3 ledger_cli.py query ALPHA_STAGING --status PENDING_REVIEW
    python3 ledger_cli.py query ALPHA_STAGING --category APP_FACTORY --limit 10
    python3 ledger_cli.py count ALPHA_STAGING --status APPROVED
    python3 ledger_cli.py list                  # List all LEDGER CSVs
    python3 ledger_cli.py schema ALPHA_STAGING  # Show column headers
    python3 ledger_cli.py stats                 # Summary stats across all files
    python3 ledger_cli.py search "cold email"   # Full-text search across all CSVs
    python3 ledger_cli.py dupes ALPHA_STAGING --column source_url  # Find duplicates
    python3 ledger_cli.py export ALPHA_STAGING --format json       # Export as JSON
"""

import csv
import json
import argparse
import sys
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Optional, Any

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_DIR / "LEDGER"


def load_csv(filename: str, exit_on_missing: bool = True) -> tuple[list[str], list[dict]]:
    """Load a CSV file and return headers and rows."""
    filepath = LEDGER_DIR / f"{filename}.csv"
    if not filepath.exists():
        # Try with .csv already appended
        filepath = LEDGER_DIR / filename
        if not filepath.exists():
            if exit_on_missing:
                print(f"Error: File not found: {filepath}")
                sys.exit(1)
            else:
                raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)
    return headers, rows


def cmd_list(args):
    """List all LEDGER CSV files with row counts."""
    csv_files = sorted(LEDGER_DIR.glob("*.csv"))
    print(f"\n{'File':<50} {'Rows':>8} {'Size':>10}")
    print("-" * 70)
    total_rows = 0
    for f in csv_files:
        try:
            with open(f, 'r', encoding='utf-8', errors='replace') as fh:
                row_count = sum(1 for _ in fh) - 1  # minus header
            size_kb = f.stat().st_size / 1024
            print(f"{f.name:<50} {row_count:>8} {size_kb:>8.1f}KB")
            total_rows += row_count
        except Exception as e:
            print(f"{f.name:<50} {'ERROR':>8} {str(e)[:20]}")
    print("-" * 70)
    print(f"{'TOTAL':<50} {total_rows:>8} {len(csv_files)} files")


def cmd_schema(args):
    """Show column headers for a CSV file."""
    headers, rows = load_csv(args.file)
    print(f"\nSchema for {args.file}:")
    print(f"Rows: {len(rows)}")
    print(f"\nColumns ({len(headers)}):")
    for i, h in enumerate(headers, 1):
        # Sample values
        samples = [r.get(h, '') for r in rows[:5] if r.get(h)]
        sample_str = ", ".join(samples[:3])
        if len(sample_str) > 60:
            sample_str = sample_str[:57] + "..."
        print(f"  {i:>3}. {h:<35} samples: {sample_str}")


def cmd_query(args):
    """Query a CSV file with filters."""
    headers, rows = load_csv(args.file)

    # Apply filters
    filtered = rows
    if args.filters:
        for filt in args.filters:
            if '=' in filt:
                key, value = filt.split('=', 1)
                key = key.strip('-').strip()
                filtered = [r for r in filtered if value.lower() in r.get(key, '').lower()]

    # Apply limit
    if args.limit:
        filtered = filtered[:args.limit]

    # Output
    if args.format == 'json':
        print(json.dumps(filtered, indent=2))
    elif args.format == 'csv':
        if filtered:
            writer = csv.DictWriter(sys.stdout, fieldnames=headers)
            writer.writeheader()
            writer.writerows(filtered)
    else:
        # Table format
        if not filtered:
            print("No results found.")
            return

        # Pick display columns (first 6 or specified)
        display_cols = headers[:6]
        if args.columns:
            display_cols = [c for c in args.columns.split(',') if c in headers]

        # Print header
        col_widths = {c: max(len(c), 10) for c in display_cols}
        header_line = " | ".join(f"{c:<{col_widths[c]}}" for c in display_cols)
        print(f"\n{header_line}")
        print("-" * len(header_line))

        for row in filtered:
            line = " | ".join(
                f"{str(row.get(c, ''))[:col_widths[c]]:<{col_widths[c]}}"
                for c in display_cols
            )
            print(line)

        print(f"\n{len(filtered)} results (of {len(rows)} total)")


def cmd_count(args):
    """Count rows matching filters."""
    headers, rows = load_csv(args.file)

    if args.group_by and args.group_by in headers:
        counter = Counter(r.get(args.group_by, 'N/A') for r in rows)
        print(f"\nCounts by {args.group_by} in {args.file}:")
        for value, count in counter.most_common():
            print(f"  {value:<40} {count:>6}")
        print(f"  {'TOTAL':<40} {len(rows):>6}")
    else:
        # Apply filters
        filtered = rows
        if args.filters:
            for filt in args.filters:
                if '=' in filt:
                    key, value = filt.split('=', 1)
                    key = key.strip('-').strip()
                    filtered = [r for r in filtered if value.lower() in r.get(key, '').lower()]
        print(f"{len(filtered)} rows match (of {len(rows)} total)")


def cmd_search(args):
    """Full-text search across all LEDGER CSVs."""
    query = args.query.lower()
    results = []

    csv_files = sorted(LEDGER_DIR.glob("*.csv"))
    for filepath in csv_files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    row_text = ' '.join(str(v) for v in row.values()).lower()
                    if query in row_text:
                        results.append({
                            'file': filepath.name,
                            'row': i + 1,
                            'match': {k: v for k, v in row.items() if query in str(v).lower()}
                        })
        except Exception:
            continue

    print(f"\nSearch results for '{args.query}': {len(results)} matches\n")
    for r in results[:args.limit]:
        print(f"  [{r['file']}] Row {r['row']}:")
        for k, v in r['match'].items():
            val = str(v)
            if len(val) > 80:
                val = val[:77] + "..."
            print(f"    {k}: {val}")
        print()


def cmd_dupes(args):
    """Find duplicate values in a column."""
    headers, rows = load_csv(args.file)
    column = args.column

    if column not in headers:
        print(f"Error: Column '{column}' not found. Available: {', '.join(headers)}")
        sys.exit(1)

    counter = Counter(r.get(column, '') for r in rows if r.get(column))
    dupes = {v: c for v, c in counter.items() if c > 1}

    if not dupes:
        print(f"No duplicates found in {args.file}.{column}")
        return

    print(f"\nDuplicates in {args.file}.{column}:")
    for value, count in sorted(dupes.items(), key=lambda x: -x[1]):
        val_display = value[:80] + "..." if len(value) > 80 else value
        print(f"  {count}x  {val_display}")
    print(f"\n{len(dupes)} duplicate values found ({sum(dupes.values()) - len(dupes)} extra rows)")


def cmd_stats(args):
    """Summary stats across all LEDGER files."""
    csv_files = sorted(LEDGER_DIR.glob("*.csv"))

    print("\n=== LEDGER System Stats ===\n")

    total_rows = 0
    total_size = 0
    file_stats = []

    for filepath in csv_files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []
                rows = list(reader)
            size = filepath.stat().st_size
            file_stats.append({
                'name': filepath.name,
                'rows': len(rows),
                'columns': len(headers),
                'size': size
            })
            total_rows += len(rows)
            total_size += size
        except Exception:
            continue

    print(f"Total files: {len(file_stats)}")
    print(f"Total rows: {total_rows}")
    print(f"Total size: {total_size / 1024:.1f}KB")

    # Alpha staging stats
    try:
        _, alpha_rows = load_csv("ALPHA_STAGING")
        status_counts = Counter(r.get('status', 'N/A') for r in alpha_rows)
        print(f"\nAlpha Staging:")
        for status, count in status_counts.most_common():
            print(f"  {status}: {count}")
    except Exception:
        pass

    # Revenue tracker stats (in FINANCIALS, not LEDGER)
    try:
        rev_path = PROJECT_DIR / "FINANCIALS" / "REVENUE_TRACKER.csv"
        if rev_path.exists():
            with open(rev_path, 'r', encoding='utf-8', errors='replace') as f:
                reader = csv.DictReader(f)
                rev_rows = list(reader)
            real_rows = [r for r in rev_rows if r.get('customer_id') != 'EXAMPLE']
            print(f"\nRevenue Tracker: {len(real_rows)} real entries")
    except Exception:
        pass

    # Largest files
    print("\nLargest files:")
    for fs in sorted(file_stats, key=lambda x: -x['size'])[:5]:
        print(f"  {fs['name']}: {fs['rows']} rows, {fs['size']/1024:.1f}KB")


def cmd_export(args):
    """Export a CSV file to another format."""
    headers, rows = load_csv(args.file)

    if args.format == 'json':
        output = json.dumps(rows, indent=2)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Exported {len(rows)} rows to {args.output}")
        else:
            print(output)
    elif args.format == 'markdown':
        if not rows:
            print("No data to export.")
            return
        # Table header
        display_cols = headers[:8]  # Limit columns for readability
        header = " | ".join(display_cols)
        separator = " | ".join("---" for _ in display_cols)
        lines = [f"| {header} |", f"| {separator} |"]
        for row in rows:
            line = " | ".join(str(row.get(c, ''))[:30] for c in display_cols)
            lines.append(f"| {line} |")
        output = "\n".join(lines)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Exported {len(rows)} rows to {args.output}")
        else:
            print(output)


def main():
    parser = argparse.ArgumentParser(
        description='LEDGER Query CLI - Query PRINTMAXX tracking data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                                      List all CSV files
  %(prog)s schema ALPHA_STAGING                      Show column headers
  %(prog)s query ALPHA_STAGING status=PENDING_REVIEW Query with filter
  %(prog)s count ALPHA_STAGING --group-by category   Count by category
  %(prog)s search "cold email"                       Search all files
  %(prog)s dupes ALPHA_STAGING --column source_url   Find duplicates
  %(prog)s stats                                     System-wide stats
  %(prog)s export ALPHA_STAGING --format json        Export as JSON
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # list
    sub_list = subparsers.add_parser('list', help='List all LEDGER CSV files')
    sub_list.set_defaults(func=cmd_list)

    # schema
    sub_schema = subparsers.add_parser('schema', help='Show CSV column headers')
    sub_schema.add_argument('file', help='CSV filename (without .csv extension)')
    sub_schema.set_defaults(func=cmd_schema)

    # query
    sub_query = subparsers.add_parser('query', help='Query a CSV with filters')
    sub_query.add_argument('file', help='CSV filename')
    sub_query.add_argument('filters', nargs='*', help='Filters as key=value pairs')
    sub_query.add_argument('--limit', type=int, default=50, help='Max rows to show')
    sub_query.add_argument('--format', choices=['table', 'json', 'csv'], default='table')
    sub_query.add_argument('--columns', help='Comma-separated columns to display')
    sub_query.set_defaults(func=cmd_query)

    # count
    sub_count = subparsers.add_parser('count', help='Count rows matching filters')
    sub_count.add_argument('file', help='CSV filename')
    sub_count.add_argument('filters', nargs='*', help='Filters as key=value pairs')
    sub_count.add_argument('--group-by', dest='group_by', help='Group counts by column')
    sub_count.set_defaults(func=cmd_count)

    # search
    sub_search = subparsers.add_parser('search', help='Full-text search across all CSVs')
    sub_search.add_argument('query', help='Search query')
    sub_search.add_argument('--limit', type=int, default=20, help='Max results')
    sub_search.set_defaults(func=cmd_search)

    # dupes
    sub_dupes = subparsers.add_parser('dupes', help='Find duplicate values')
    sub_dupes.add_argument('file', help='CSV filename')
    sub_dupes.add_argument('--column', required=True, help='Column to check for dupes')
    sub_dupes.set_defaults(func=cmd_dupes)

    # stats
    sub_stats = subparsers.add_parser('stats', help='System-wide statistics')
    sub_stats.set_defaults(func=cmd_stats)

    # export
    sub_export = subparsers.add_parser('export', help='Export CSV to another format')
    sub_export.add_argument('file', help='CSV filename')
    sub_export.add_argument('--format', choices=['json', 'markdown'], default='json')
    sub_export.add_argument('--output', '-o', help='Output file path')
    sub_export.set_defaults(func=cmd_export)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
