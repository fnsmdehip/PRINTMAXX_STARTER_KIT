#!/usr/bin/env python3
"""
Auto-Backtest Trigger (IR-001)
Wires quant infrastructure into mega ralph REFLECTION phase.

Scans ALPHA_STAGING.csv for entries without backtest scores,
runs backtest_alpha.py on them, and writes prioritized results
that the mega ralph REFLECTION phase can consume.

This script is called:
1. Automatically during mega ralph REFLECTION phase (iteration 4)
2. Manually: python3 scripts/auto_backtest_trigger.py

Integration points:
- Reads: LEDGER/ALPHA_STAGING.csv (new alpha entries)
- Reads: LEDGER/BACKTESTS/BACKTEST_RESULTS.csv (already backtested)
- Writes: LEDGER/BACKTESTS/BACKTEST_RESULTS.csv (new scores)
- Writes: ralph/loops/mega/.ralph/priorities.md (priority updates)
- Writes: LEDGER/BACKTEST_PRIORITY_QUEUE.csv (sorted queue for EXECUTION)

Usage:
    python3 scripts/auto_backtest_trigger.py              # Backtest all unscored
    python3 scripts/auto_backtest_trigger.py --since 24    # Only last 24 hours
    python3 scripts/auto_backtest_trigger.py --dry-run     # Show what would be backtested
"""

import csv
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Set, Tuple

PROJECT_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_DIR / "LEDGER"
BACKTEST_DIR = LEDGER_DIR / "BACKTESTS"
MEGA_RALPH_DIR = PROJECT_DIR / "ralph" / "loops" / "mega"

# Ensure directories exist
BACKTEST_DIR.mkdir(parents=True, exist_ok=True)

# Add AUTOMATIONS to path for backtest_alpha import
sys.path.insert(0, str(PROJECT_DIR / "AUTOMATIONS"))

try:
    from backtest_alpha import AlphaBacktester
except ImportError:
    print("ERROR: Could not import backtest_alpha from AUTOMATIONS/")
    print("Ensure AUTOMATIONS/backtest_alpha.py exists")
    sys.exit(1)


def get_already_backtested() -> Set[str]:
    """Get set of alpha_ids that already have backtest scores."""
    backtested = set()
    results_file = BACKTEST_DIR / "BACKTEST_RESULTS.csv"

    if not results_file.exists():
        return backtested

    try:
        with open(results_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                alpha_id = row.get('alpha_id', '').strip()
                if alpha_id:
                    backtested.add(alpha_id)
    except Exception as e:
        print(f"Warning: Error reading backtest results: {e}")

    return backtested


def get_pending_alpha(since_hours: int = None) -> List[Dict]:
    """Get alpha entries that need backtesting."""
    alpha_file = LEDGER_DIR / "ALPHA_STAGING.csv"
    if not alpha_file.exists():
        print("ERROR: ALPHA_STAGING.csv not found")
        return []

    already_backtested = get_already_backtested()
    pending = []
    cutoff = None

    if since_hours:
        cutoff = datetime.now() - timedelta(hours=since_hours)

    try:
        with open(alpha_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                alpha_id = row.get('alpha_id', '').strip()

                # Skip if already backtested
                if alpha_id in already_backtested:
                    continue

                # Skip empty IDs
                if not alpha_id:
                    continue

                # Skip if filtering by time and entry is too old
                if cutoff and row.get('reviewed_date'):
                    try:
                        entry_date = datetime.strptime(
                            row['reviewed_date'][:10], '%Y-%m-%d'
                        )
                        if entry_date < cutoff:
                            continue
                    except (ValueError, TypeError):
                        pass  # Include if date parsing fails

                pending.append({
                    'alpha_id': alpha_id,
                    'category': row.get('category', 'UNKNOWN'),
                    'status': row.get('status', 'UNKNOWN'),
                    'roi_potential': row.get('roi_potential', 'UNKNOWN'),
                })
    except Exception as e:
        print(f"ERROR reading ALPHA_STAGING.csv: {e}")

    return pending


def run_backtests(pending: List[Dict]) -> List[Dict]:
    """Run backtests on pending alpha entries."""
    backtester = AlphaBacktester()
    results = []

    alpha_ids = [entry['alpha_id'] for entry in pending]

    if not alpha_ids:
        print("No entries to backtest.")
        return results

    print(f"Running backtests on {len(alpha_ids)} entries...")

    for alpha_id in alpha_ids:
        try:
            result = backtester.backtest_alpha(alpha_id)
            if 'error' not in result:
                results.append(result)
                score = result.get('backtest_score', 0)
                decision = result.get('decision', 'N/A')
                print(f"  {alpha_id}: Score {score} -> {decision}")
            else:
                print(f"  {alpha_id}: {result['error']}")
        except Exception as e:
            print(f"  {alpha_id}: ERROR - {e}")

    # Save results
    if results:
        backtester.save_results(results)

    return results


def generate_priority_queue(results: List[Dict]) -> None:
    """Generate prioritized backtest queue for EXECUTION phase."""
    priority_file = LEDGER_DIR / "BACKTEST_PRIORITY_QUEUE.csv"

    # Load all backtest results (new + existing)
    all_results = []
    results_file = BACKTEST_DIR / "BACKTEST_RESULTS.csv"

    if results_file.exists():
        try:
            with open(results_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    all_results.append(row)
        except Exception as e:
            print(f"Warning: Error reading results: {e}")

    # Sort by score descending
    all_results.sort(
        key=lambda x: int(x.get('backtest_score', 0)),
        reverse=True
    )

    # Write priority queue
    with open(priority_file, 'w', newline='') as f:
        fieldnames = [
            'rank', 'alpha_id', 'backtest_score', 'decision',
            'category', 'source', 'action_required'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for rank, entry in enumerate(all_results, 1):
            score = int(entry.get('backtest_score', 0))
            decision = entry.get('decision', 'KILL')

            if decision == 'SCALE':
                action = 'Deploy to EXECUTION phase immediately'
            elif decision == 'PAPER_TRADE':
                action = 'Start paper trade with $50-100 budget, 14 days'
            else:
                action = 'Deprioritize in priorities.md'

            writer.writerow({
                'rank': rank,
                'alpha_id': entry.get('alpha_id', ''),
                'backtest_score': score,
                'decision': decision,
                'category': entry.get('category', ''),
                'source': entry.get('source', ''),
                'action_required': action,
            })

    print(f"Priority queue written to {priority_file}")
    print(f"  Total entries: {len(all_results)}")

    scale_count = sum(1 for r in all_results if r.get('decision') == 'SCALE')
    paper_count = sum(1 for r in all_results if r.get('decision') == 'PAPER_TRADE')
    kill_count = sum(1 for r in all_results if r.get('decision') == 'KILL')

    print(f"  SCALE: {scale_count}")
    print(f"  PAPER_TRADE: {paper_count}")
    print(f"  KILL: {kill_count}")


def update_mega_ralph_priorities(results: List[Dict]) -> None:
    """Inject backtest results into mega ralph priorities.md."""
    priorities_file = MEGA_RALPH_DIR / ".ralph" / "priorities.md"

    if not priorities_file.exists():
        print(f"Warning: {priorities_file} does not exist, creating it")
        priorities_file.parent.mkdir(parents=True, exist_ok=True)

    # Categorize results
    scale_entries = [r for r in results if r.get('decision') == 'SCALE']
    paper_entries = [r for r in results if r.get('decision') == 'PAPER_TRADE']
    kill_entries = [r for r in results if r.get('decision') == 'KILL']

    # Build priority injection block
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    block = f"""

## Quant Backtest Results (Auto-Generated {now})

### SCALE-Scored Alpha (Score >= 70) - Deploy in EXECUTION Phase
"""
    if scale_entries:
        for entry in scale_entries:
            block += f"- {entry['alpha_id']}: Score {entry['backtest_score']} ({entry.get('category', 'N/A')}) - DEPLOY NOW\n"
    else:
        block += "- No SCALE-scored alpha in this batch\n"

    block += """
### PAPER_TRADE-Scored Alpha (Score 50-69) - Test with $50-100
"""
    if paper_entries:
        for entry in paper_entries:
            block += f"- {entry['alpha_id']}: Score {entry['backtest_score']} ({entry.get('category', 'N/A')}) - START PAPER TRADE\n"
    else:
        block += "- No PAPER_TRADE-scored alpha in this batch\n"

    block += f"""
### KILL-Scored Alpha (Score < 50) - Deprioritized
- {len(kill_entries)} entries scored below threshold. See BACKTEST_PRIORITY_QUEUE.csv for details.
"""

    # Read existing priorities
    existing_content = ""
    if priorities_file.exists():
        with open(priorities_file, 'r') as f:
            existing_content = f.read()

    # Remove old quant backtest section if present
    marker = "## Quant Backtest Results (Auto-Generated"
    if marker in existing_content:
        # Find the section and remove it
        start_idx = existing_content.index(marker)
        # Find next ## section or end of file
        next_section = existing_content.find('\n## ', start_idx + len(marker))
        if next_section != -1:
            existing_content = existing_content[:start_idx] + existing_content[next_section:]
        else:
            existing_content = existing_content[:start_idx]

    # Append new block
    with open(priorities_file, 'w') as f:
        f.write(existing_content.rstrip() + "\n" + block)

    print(f"Updated {priorities_file} with backtest results")


def print_summary(results: List[Dict], total_pending: int) -> None:
    """Print summary of backtest run."""
    print("\n" + "=" * 50)
    print("AUTO-BACKTEST TRIGGER SUMMARY")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Entries scanned: {total_pending}")
    print(f"Backtests completed: {len(results)}")

    if results:
        scores = [r.get('backtest_score', 0) for r in results]
        avg_score = sum(scores) / len(scores)
        print(f"Average score: {avg_score:.1f}")

        decisions = {}
        for r in results:
            d = r.get('decision', 'UNKNOWN')
            decisions[d] = decisions.get(d, 0) + 1

        for decision, count in sorted(decisions.items()):
            pct = count / len(results) * 100
            print(f"  {decision}: {count} ({pct:.1f}%)")

    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description='Auto-backtest trigger for mega ralph integration'
    )
    parser.add_argument(
        '--since', type=int, default=None,
        help='Only backtest alpha from last N hours (default: all unscored)'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Show what would be backtested without running'
    )
    parser.add_argument(
        '--skip-priorities', action='store_true',
        help='Skip updating mega ralph priorities.md'
    )

    args = parser.parse_args()

    print(f"Auto-Backtest Trigger - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

    # Get pending entries
    pending = get_pending_alpha(since_hours=args.since)
    print(f"Found {len(pending)} unscored alpha entries")

    if args.dry_run:
        print("\nDRY RUN - Would backtest:")
        for entry in pending[:20]:
            print(f"  {entry['alpha_id']} ({entry['category']}) - status: {entry['status']}")
        if len(pending) > 20:
            print(f"  ... and {len(pending) - 20} more")
        return

    if not pending:
        print("No entries need backtesting. All alpha already scored.")
        return

    # Run backtests
    results = run_backtests(pending)

    # Generate priority queue
    generate_priority_queue(results)

    # Update mega ralph priorities
    if not args.skip_priorities:
        update_mega_ralph_priorities(results)

    # Print summary
    print_summary(results, len(pending))


if __name__ == "__main__":
    main()
