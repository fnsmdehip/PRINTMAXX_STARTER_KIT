#!/usr/bin/env python3
"""
Paper Trade Results -> Method Tracker Integration (IR-002)
When paper trades complete, auto-update MONEY_METHODS_TRACKER.csv
with performance data and flag scaling/killing decisions.

Integration points:
- Reads: LEDGER/PAPER_TRADES/PAPER_TRADE_RESULTS.csv (completed trades)
- Reads: LEDGER/MONEY_METHODS_TRACKER.csv (current method status)
- Writes: LEDGER/MONEY_METHODS_TRACKER.csv (updated with performance data)
- Writes: FINANCIALS/REVENUE_TRACKER.csv (revenue from paper trades)
- Writes: FINANCIALS/EXPENSE_TRACKER.csv (costs from paper trades)
- Writes: OPS/CAPITAL_GENESIS_DASHBOARD_STATUS.csv (lane status updates)

Usage:
    python3 scripts/paper_trade_to_tracker.py              # Sync all completed trades
    python3 scripts/paper_trade_to_tracker.py --trade-id PAPER_TRADE_001
    python3 scripts/paper_trade_to_tracker.py --dry-run     # Show changes without writing
"""

import csv
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

PROJECT_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_DIR / "LEDGER"
FINANCIALS_DIR = PROJECT_DIR / "FINANCIALS"
PAPER_TRADE_DIR = LEDGER_DIR / "PAPER_TRADES"


def load_paper_trade_results(trade_id: Optional[str] = None) -> List[Dict]:
    """Load completed paper trade results."""
    results_file = PAPER_TRADE_DIR / "PAPER_TRADE_RESULTS.csv"
    results = []

    if not results_file.exists():
        print("No paper trade results file found.")
        return results

    try:
        with open(results_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if trade_id and row.get('trade_id') != trade_id:
                    continue
                results.append(row)
    except Exception as e:
        print(f"Error loading paper trade results: {e}")

    return results


def load_methods_tracker() -> tuple:
    """Load MONEY_METHODS_TRACKER.csv and return (rows, fieldnames)."""
    tracker_file = LEDGER_DIR / "MONEY_METHODS_TRACKER.csv"
    rows = []
    fieldnames = []

    if not tracker_file.exists():
        print("ERROR: MONEY_METHODS_TRACKER.csv not found")
        return rows, fieldnames

    try:
        with open(tracker_file, 'r') as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames or [])
            for row in reader:
                rows.append(row)
    except Exception as e:
        print(f"Error loading methods tracker: {e}")

    return rows, fieldnames


def get_already_synced() -> set:
    """Get set of paper trade IDs already synced to tracker."""
    sync_log = PAPER_TRADE_DIR / "SYNC_LOG.csv"
    synced = set()

    if not sync_log.exists():
        return synced

    try:
        with open(sync_log, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                synced.add(row.get('trade_id', ''))
    except Exception as e:
        print(f"Warning: Error reading sync log: {e}")

    return synced


def log_sync(trade_id: str, actions: List[str]) -> None:
    """Log which trade was synced and what actions were taken."""
    sync_log = PAPER_TRADE_DIR / "SYNC_LOG.csv"
    file_exists = sync_log.exists()

    with open(sync_log, 'a', newline='') as f:
        fieldnames = ['trade_id', 'synced_at', 'actions']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'trade_id': trade_id,
            'synced_at': datetime.now().isoformat(),
            'actions': '; '.join(actions),
        })


def update_methods_tracker(result: Dict, dry_run: bool = False) -> List[str]:
    """Update MONEY_METHODS_TRACKER.csv with paper trade results."""
    actions = []
    method_id = result.get('method_id', '')

    # Extract the base method_id (before underscore-name, e.g. MM007 from MM007_COLD_OUTBOUND)
    base_method_id = method_id.split('_')[0] if '_' in method_id else method_id

    rows, fieldnames = load_methods_tracker()

    if not rows:
        return actions

    # Add performance columns if they don't exist
    new_columns = [
        'paper_trade_revenue_per_hour',
        'paper_trade_scalability',
        'paper_trade_platform_risk',
        'paper_trade_decision',
        'paper_trade_roi_pct',
        'paper_trade_date',
        'paper_trade_id',
    ]

    columns_added = False
    for col in new_columns:
        if col not in fieldnames:
            fieldnames.append(col)
            columns_added = True

    if columns_added:
        actions.append(f"Added columns: {', '.join(new_columns)}")

    # Find and update the matching method
    updated = False
    for row in rows:
        row_method = row.get('method_id', '')
        if row_method == base_method_id or row_method == method_id:
            # Update with paper trade data
            row['paper_trade_revenue_per_hour'] = result.get('revenue_per_hour', '0')
            row['paper_trade_scalability'] = result.get('scalability_score', '5')
            row['paper_trade_platform_risk'] = result.get('platform_risk', '5')
            row['paper_trade_decision'] = result.get('decision', 'UNKNOWN')
            row['paper_trade_roi_pct'] = result.get('roi_percent', '0')
            row['paper_trade_date'] = datetime.now().strftime('%Y-%m-%d')
            row['paper_trade_id'] = result.get('trade_id', '')

            # Update method status based on decision
            decision = result.get('decision', '')
            if decision == 'SCALE':
                if row.get('status') in ('Planning', 'New', 'Research'):
                    row['status'] = 'Active'
                    actions.append(f"Method {row_method} status: {row.get('status', 'N/A')} -> Active (SCALE)")
                actions.append(f"Method {row_method}: revenue/hr=${result.get('revenue_per_hour', 0)}, ROI={result.get('roi_percent', 0)}%")
            elif decision == 'KILL':
                actions.append(f"Method {row_method}: KILLED (revenue/hr=${result.get('revenue_per_hour', 0)})")
                row['notes'] = (row.get('notes', '') + f" | PAPER_TRADE_KILLED {datetime.now().strftime('%Y-%m-%d')}").strip(' |')

            updated = True
            break

    if not updated:
        actions.append(f"WARNING: Method {method_id} not found in tracker (tried {base_method_id})")
        return actions

    # Write updated tracker
    if not dry_run:
        tracker_file = LEDGER_DIR / "MONEY_METHODS_TRACKER.csv"
        with open(tracker_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                # Ensure all new columns have defaults
                for col in new_columns:
                    if col not in row:
                        row[col] = ''
                writer.writerow(row)

        actions.append(f"Updated {tracker_file}")

    return actions


def update_financials(result: Dict, dry_run: bool = False) -> List[str]:
    """Update FINANCIALS tracking with paper trade data."""
    actions = []

    revenue = float(result.get('total_revenue', 0))
    investment = float(result.get('total_investment', 0))
    method_id = result.get('method_id', '')
    trade_id = result.get('trade_id', '')

    # Add revenue if any
    if revenue > 0 and not dry_run:
        revenue_file = FINANCIALS_DIR / "REVENUE_TRACKER.csv"
        with open(revenue_file, 'a', newline='') as f:
            fieldnames = [
                'date', 'method_id', 'method_name', 'source_platform',
                'transaction_type', 'amount', 'currency', 'fees',
                'net_amount', 'customer_id', 'product_name', 'recurring', 'notes'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({
                'date': datetime.now().strftime('%Y-%m-%d'),
                'method_id': method_id.split('_')[0] if '_' in method_id else method_id,
                'method_name': method_id,
                'source_platform': 'paper_trade',
                'transaction_type': 'paper_trade_revenue',
                'amount': revenue,
                'currency': 'USD',
                'fees': 0,
                'net_amount': revenue,
                'customer_id': trade_id,
                'product_name': f'Paper Trade {trade_id}',
                'recurring': 'FALSE',
                'notes': f'Paper trade validation revenue. Decision: {result.get("decision", "N/A")}',
            })
        actions.append(f"Revenue tracked: ${revenue} from {trade_id}")

    # Add expense if any investment
    if investment > 0 and not dry_run:
        expense_file = FINANCIALS_DIR / "EXPENSE_TRACKER.csv"
        with open(expense_file, 'a', newline='') as f:
            fieldnames = [
                'date', 'category', 'vendor', 'description', 'amount',
                'currency', 'payment_method', 'recurring', 'frequency',
                'method_id', 'tax_deductible', 'receipt_url', 'notes'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({
                'date': datetime.now().strftime('%Y-%m-%d'),
                'category': 'paper_trade',
                'vendor': 'Paper Trade Test',
                'description': f'Paper trade {trade_id} for {method_id}',
                'amount': investment,
                'currency': 'USD',
                'payment_method': 'various',
                'recurring': 'FALSE',
                'frequency': 'one_time',
                'method_id': method_id.split('_')[0] if '_' in method_id else method_id,
                'tax_deductible': 'TRUE',
                'receipt_url': '',
                'notes': f'Paper trade validation cost. Decision: {result.get("decision", "N/A")}',
            })
        actions.append(f"Expense tracked: ${investment} for {trade_id}")

    return actions


def update_capital_genesis_status(result: Dict, dry_run: bool = False) -> List[str]:
    """Update capital genesis lane status based on paper trade decision."""
    actions = []
    decision = result.get('decision', '')
    method_id = result.get('method_id', '')
    trade_id = result.get('trade_id', '')

    status_file = LEDGER_DIR / "CAPITAL_GENESIS_LANE_STATUS.csv"
    file_exists = status_file.exists()

    if not dry_run:
        with open(status_file, 'a', newline='') as f:
            fieldnames = [
                'date', 'method_id', 'trade_id', 'decision',
                'revenue_per_hour', 'scalability', 'platform_risk',
                'roi_pct', 'lane_action'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            lane_action = 'MONITOR'
            if decision == 'SCALE':
                lane_action = 'SCALE_2X'
            elif decision == 'KILL':
                lane_action = 'KILL_LANE'
            elif decision == 'ITERATE':
                lane_action = 'ADJUST_AND_RETEST'

            writer.writerow({
                'date': datetime.now().strftime('%Y-%m-%d'),
                'method_id': method_id,
                'trade_id': trade_id,
                'decision': decision,
                'revenue_per_hour': result.get('revenue_per_hour', 0),
                'scalability': result.get('scalability_score', 5),
                'platform_risk': result.get('platform_risk', 5),
                'roi_pct': result.get('roi_percent', 0),
                'lane_action': lane_action,
            })

        actions.append(f"Capital genesis lane status: {method_id} -> {lane_action}")

    return actions


def main():
    parser = argparse.ArgumentParser(
        description='Sync paper trade results to method tracker and financials'
    )
    parser.add_argument(
        '--trade-id', type=str, default=None,
        help='Sync specific trade ID only'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Show changes without writing'
    )
    parser.add_argument(
        '--force', action='store_true',
        help='Re-sync already synced trades'
    )

    args = parser.parse_args()

    print(f"Paper Trade -> Tracker Sync - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

    # Load completed results
    results = load_paper_trade_results(trade_id=args.trade_id)
    print(f"Found {len(results)} completed paper trade(s)")

    if not results:
        print("No paper trade results to sync.")
        return

    # Check which are already synced
    already_synced = get_already_synced()

    total_actions = []
    synced_count = 0

    for result in results:
        trade_id = result.get('trade_id', '')

        if trade_id in already_synced and not args.force:
            print(f"  {trade_id}: Already synced (use --force to re-sync)")
            continue

        print(f"\nProcessing {trade_id}:")
        print(f"  Method: {result.get('method_id', 'N/A')}")
        print(f"  Decision: {result.get('decision', 'N/A')}")
        print(f"  Revenue/Hr: ${result.get('revenue_per_hour', 0)}")
        print(f"  ROI: {result.get('roi_percent', 0)}%")

        actions = []

        # 1. Update MONEY_METHODS_TRACKER.csv
        tracker_actions = update_methods_tracker(result, dry_run=args.dry_run)
        actions.extend(tracker_actions)

        # 2. Update FINANCIALS
        financial_actions = update_financials(result, dry_run=args.dry_run)
        actions.extend(financial_actions)

        # 3. Update Capital Genesis lane status
        genesis_actions = update_capital_genesis_status(result, dry_run=args.dry_run)
        actions.extend(genesis_actions)

        # Log the sync
        if not args.dry_run:
            log_sync(trade_id, actions)

        for action in actions:
            print(f"  -> {action}")

        total_actions.extend(actions)
        synced_count += 1

    # Summary
    print("\n" + "=" * 50)
    print("PAPER TRADE SYNC SUMMARY")
    print("=" * 50)
    print(f"Trades processed: {synced_count}")
    print(f"Actions taken: {len(total_actions)}")
    if args.dry_run:
        print("MODE: DRY RUN (no files modified)")
    print("=" * 50)


if __name__ == "__main__":
    main()
