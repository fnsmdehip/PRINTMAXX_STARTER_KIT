#!/usr/bin/env python3
"""
Quant Reflection Engine - Integrates backtesting + paper trading into mega ralph REFLECTION phase.

Runs during REFLECTION (iteration 4 each day cycle) to:
1. Auto-backtest new PENDING_REVIEW alpha entries
2. Flag high-scoring alpha for paper trading
3. Check active paper trades for completion
4. Generate method stack recommendations from cross-pollination data
5. Update priority queue based on quantitative signals

Usage:
    python3 quant_reflection.py run          # Full reflection cycle
    python3 quant_reflection.py backtest     # Only run backtesting
    python3 quant_reflection.py paper-check  # Check paper trade status
    python3 quant_reflection.py stacks       # Generate stack recommendations
    python3 quant_reflection.py summary      # Print reflection summary
"""

import csv
import json
import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Any, Optional

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_DIR / "LEDGER"
AUTOMATIONS_DIR = PROJECT_DIR / "AUTOMATIONS"
BACKTEST_DIR = LEDGER_DIR / "BACKTESTS"
PAPER_TRADE_DIR = LEDGER_DIR / "PAPER_TRADES"
MEGA_RALPH_DIR = PROJECT_DIR / "ralph" / "loops" / "mega"

BACKTEST_DIR.mkdir(exist_ok=True)
PAPER_TRADE_DIR.mkdir(exist_ok=True)


def load_csv(filepath: Path) -> tuple:
    """Load a CSV and return (headers, rows)."""
    if not filepath.exists():
        return [], []
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)
    return headers, rows


def append_csv(filepath: Path, row: dict, fieldnames: list):
    """Append a row to a CSV file."""
    file_exists = filepath.exists() and filepath.stat().st_size > 0
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def score_alpha_entry(entry: dict) -> dict:
    """
    Score an alpha entry 0-100 for deployment readiness.
    Based on backtest_alpha.py scoring criteria.
    """
    score = 0
    details = {}

    # 1. Source credibility (0-15)
    source = entry.get('source', '').lower()
    source_score = 5  # default
    high_cred = ['@levelsio', '@tdinh_me', '@pipelineabuser', '@codyschneiderxx',
                 'reddit.com', 'producthunt', 'github.com', 'ycombinator']
    for hc in high_cred:
        if hc in source:
            source_score = 15
            break
    if 'verified' in source or 'official' in source:
        source_score = 12
    score += source_score
    details['source_credibility'] = source_score

    # 2. Specificity (0-20)
    desc = entry.get('description', '') + entry.get('title', '') + entry.get('actionable_steps', '')
    specificity = 0
    # Has dollar amounts
    if '$' in desc:
        specificity += 5
    # Has percentages
    if '%' in desc:
        specificity += 5
    # Has specific numbers
    import re
    numbers = re.findall(r'\d+', desc)
    if len(numbers) >= 3:
        specificity += 5
    elif len(numbers) >= 1:
        specificity += 3
    # Has named tools/platforms
    tools = ['revenueCat', 'stripe', 'gumroad', 'beehiiv', 'whop', 'claude', 'cursor',
             'remotion', 'expo', 'react native', 'tiktok shop', 'notion', 'substack']
    for tool in tools:
        if tool.lower() in desc.lower():
            specificity += 5
            break
    specificity = min(20, specificity)
    score += specificity
    details['specificity'] = specificity

    # 3. Actionability (0-20)
    steps = entry.get('actionable_steps', '')
    action_score = 0
    if steps:
        step_count = len([s for s in steps.split(',') if s.strip()])
        if step_count >= 5:
            action_score = 20
        elif step_count >= 3:
            action_score = 15
        elif step_count >= 1:
            action_score = 10
    else:
        # Check description for action words
        action_words = ['build', 'create', 'launch', 'ship', 'deploy', 'set up', 'configure',
                       'write', 'generate', 'post', 'send', 'automate']
        for word in action_words:
            if word in desc.lower():
                action_score += 3
        action_score = min(20, action_score)
    score += action_score
    details['actionability'] = action_score

    # 4. ROI potential (0-20)
    roi = entry.get('roi_potential', 'MEDIUM').upper()
    roi_map = {'HIGHEST': 20, 'HIGH': 15, 'MEDIUM': 10, 'LOW': 5}
    roi_score = roi_map.get(roi, 10)
    score += roi_score
    details['roi_potential'] = roi_score

    # 5. Cross-pollination potential (0-15)
    niches = entry.get('applies_to_niches', '')
    category = entry.get('category', '')
    xpol_score = 0
    if niches:
        niche_count = len([n for n in niches.split(',') if n.strip()])
        xpol_score = min(15, niche_count * 3)
    # Methods that apply broadly
    broad_cats = ['TOOL_ALPHA', 'GROWTH_HACK', 'MONETIZATION', 'PLATFORM_UPDATE']
    if category in broad_cats:
        xpol_score = max(xpol_score, 10)
    score += xpol_score
    details['cross_pollination'] = xpol_score

    # 6. Timeliness (0-10)
    time_score = 5  # default moderate
    time_words = ['2026', 'january', 'february', 'this week', 'just launched',
                  'trending', 'new', 'breaking', 'closing window']
    for tw in time_words:
        if tw.lower() in desc.lower():
            time_score = 10
            break
    score += time_score
    details['timeliness'] = time_score

    # Decision
    if score >= 70:
        decision = 'SCALE'
    elif score >= 50:
        decision = 'PAPER_TRADE'
    else:
        decision = 'KILL'

    return {
        'alpha_id': entry.get('alpha_id', ''),
        'score': score,
        'decision': decision,
        'details': details,
        'category': category,
        'title': entry.get('title', '')[:80],
    }


def cmd_backtest(args):
    """Auto-backtest new PENDING_REVIEW entries."""
    _, alpha_rows = load_csv(LEDGER_DIR / "ALPHA_STAGING.csv")

    # Filter to PENDING_REVIEW
    pending = [r for r in alpha_rows if r.get('status', '').upper() == 'PENDING_REVIEW']

    # Check which have already been backtested
    backtest_file = BACKTEST_DIR / "BACKTEST_RESULTS.csv"
    _, existing_bt = load_csv(backtest_file)
    already_tested = {r.get('alpha_id', '') for r in existing_bt}

    to_test = [r for r in pending if r.get('alpha_id', '') not in already_tested]

    if not to_test:
        print("No new PENDING_REVIEW entries to backtest.")
        return

    print(f"\nBacktesting {len(to_test)} new entries...\n")

    bt_fields = ['alpha_id', 'score', 'decision', 'category', 'title',
                 'source_credibility', 'specificity', 'actionability',
                 'roi_potential', 'cross_pollination', 'timeliness',
                 'backtested_at']

    results = {'SCALE': 0, 'PAPER_TRADE': 0, 'KILL': 0}

    for entry in to_test:
        result = score_alpha_entry(entry)
        results[result['decision']] += 1

        row = {
            'alpha_id': result['alpha_id'],
            'score': result['score'],
            'decision': result['decision'],
            'category': result['category'],
            'title': result['title'],
            'backtested_at': datetime.now().isoformat(),
        }
        row.update(result['details'])
        append_csv(backtest_file, row, bt_fields)

        symbol = {'SCALE': '+', 'PAPER_TRADE': '~', 'KILL': '-'}[result['decision']]
        print(f"  [{symbol}] {result['alpha_id']}: {result['score']}/100 -> {result['decision']}")

    print(f"\nResults: {results['SCALE']} SCALE, {results['PAPER_TRADE']} PAPER_TRADE, {results['KILL']} KILL")
    print(f"Written to {backtest_file}")

    # Flag high-scorers for paper trading
    scale_entries = [e for e in to_test if score_alpha_entry(e)['decision'] == 'SCALE']
    if scale_entries:
        print(f"\n{len(scale_entries)} entries ready to SCALE (score >= 70):")
        for e in scale_entries[:10]:
            r = score_alpha_entry(e)
            print(f"  {r['alpha_id']}: {r['score']}/100 - {r['title']}")


def cmd_paper_check(args):
    """Check status of active paper trades."""
    paper_trade_file = PAPER_TRADE_DIR / "ACTIVE_TRADES.csv"
    _, trades = load_csv(paper_trade_file)

    if not trades:
        print("No active paper trades.")
        return

    now = datetime.now()
    print(f"\nActive Paper Trades ({len(trades)}):\n")

    for trade in trades:
        start = trade.get('start_date', '')
        end = trade.get('end_date', '')
        method = trade.get('method', '')
        alpha = trade.get('alpha_id', '')
        budget = trade.get('budget', '0')
        revenue = trade.get('revenue', '0')
        status = trade.get('status', 'ACTIVE')

        # Check if trade has expired
        if end:
            try:
                end_dt = datetime.fromisoformat(end)
                if now > end_dt and status == 'ACTIVE':
                    print(f"  EXPIRED: {alpha} ({method}) - Budget: ${budget}, Revenue: ${revenue}")
                    print(f"    -> Needs completion review")
                    continue
            except ValueError:
                pass

        if status == 'ACTIVE':
            try:
                rev_f = float(revenue)
                budget_f = float(budget)
                time_hrs = float(trade.get('time_invested_hours', '0'))
                rev_per_hr = rev_f / time_hrs if time_hrs > 0 else 0
                print(f"  ACTIVE: {alpha} ({method})")
                print(f"    Budget: ${budget} | Revenue: ${revenue} | Rev/hr: ${rev_per_hr:.2f}")
                print(f"    Period: {start} to {end}")
            except ValueError:
                print(f"  ACTIVE: {alpha} ({method}) - ${budget} budget")


def cmd_stacks(args):
    """Generate method stack recommendations from cross-pollination data."""
    xpol_file = LEDGER_DIR / "CROSS_POLLINATION_MATRIX.csv"
    _, xpol_rows = load_csv(xpol_file)

    if not xpol_rows:
        print("No cross-pollination data available.")
        return

    # Find high-synergy stacks
    print("\nTop Method Stacks (Synergy Score >= 90):\n")

    high_stacks = []
    for row in xpol_rows:
        try:
            score = int(row.get('synergy_score', row.get('score', '0')))
        except ValueError:
            continue
        if score >= 90:
            high_stacks.append(row)

    high_stacks.sort(key=lambda x: int(x.get('synergy_score', x.get('score', '0'))), reverse=True)

    for stack in high_stacks[:15]:
        score = stack.get('synergy_score', stack.get('score', ''))
        method = stack.get('method_id', stack.get('primary_method', 'N/A'))
        partner = stack.get('synergy_partners', stack.get('secondary_method', 'N/A'))
        desc = stack.get('description', stack.get('notes', ''))[:80]
        print(f"  Score {score}: {method} x {partner}")
        if desc:
            print(f"    {desc}")

    # Generate recommendations based on recent alpha
    _, alpha_rows = load_csv(LEDGER_DIR / "ALPHA_STAGING.csv")
    approved = [r for r in alpha_rows if r.get('status', '').upper() == 'APPROVED']

    # Count categories in approved alpha
    cat_counts = Counter(r.get('category', 'UNKNOWN') for r in approved)
    print(f"\nApproved Alpha by Category:")
    for cat, count in cat_counts.most_common(10):
        print(f"  {cat}: {count}")

    # Recommend stacks that align with highest-alpha categories
    print(f"\nRecommended Focus Areas (based on approved alpha concentration):")
    top_cats = [c for c, _ in cat_counts.most_common(3)]
    for cat in top_cats:
        matching_stacks = [s for s in high_stacks
                          if cat.lower() in str(s).lower()]
        if matching_stacks:
            stack = matching_stacks[0]
            print(f"  {cat}: Stack with {stack.get('synergy_partners', stack.get('secondary_method', 'N/A'))}")


def cmd_run(args):
    """Full reflection cycle - runs all quant checks."""
    print("=" * 60)
    print("QUANT REFLECTION ENGINE - Full Cycle")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)

    # 1. Backtest new entries
    print("\n--- PHASE 1: Auto-Backtest New Alpha ---")
    cmd_backtest(args)

    # 2. Check paper trades
    print("\n--- PHASE 2: Paper Trade Status ---")
    cmd_paper_check(args)

    # 3. Stack recommendations
    print("\n--- PHASE 3: Stack Recommendations ---")
    cmd_stacks(args)

    # 4. Generate summary
    print("\n--- PHASE 4: Reflection Summary ---")
    cmd_summary(args)


def cmd_summary(args):
    """Generate reflection summary for mega ralph progress.md."""
    # Alpha stats
    _, alpha_rows = load_csv(LEDGER_DIR / "ALPHA_STAGING.csv")
    status_counts = Counter(r.get('status', 'UNKNOWN') for r in alpha_rows)

    # Backtest stats
    _, bt_rows = load_csv(BACKTEST_DIR / "BACKTEST_RESULTS.csv")
    bt_decisions = Counter(r.get('decision', 'UNKNOWN') for r in bt_rows)

    # Paper trade stats
    pt_file = PAPER_TRADE_DIR / "ACTIVE_TRADES.csv"
    _, pt_rows = load_csv(pt_file)
    active_trades = [r for r in pt_rows if r.get('status', '').upper() == 'ACTIVE']

    # Method tracker stats
    _, methods = load_csv(LEDGER_DIR / "MONEY_METHODS_TRACKER.csv")

    # Cross-pollination stats
    _, xpol = load_csv(LEDGER_DIR / "CROSS_POLLINATION_MATRIX.csv")
    high_synergy = [r for r in xpol
                    if int(r.get('synergy_score', r.get('score', '0')) or '0') >= 90]

    # Mega ralph tracker
    _, mega_tasks = load_csv(LEDGER_DIR / "MEGA_RALPH_TRACKER.csv")
    completed_tasks = [t for t in mega_tasks if t.get('status', '').upper() == 'COMPLETED']

    print(f"\n{'=' * 50}")
    print(f"QUANT REFLECTION SUMMARY")
    print(f"{'=' * 50}")
    print(f"\nAlpha Pipeline:")
    for status, count in status_counts.most_common():
        print(f"  {status}: {count}")
    print(f"  TOTAL: {len(alpha_rows)}")

    print(f"\nBacktest Results ({len(bt_rows)} tested):")
    for decision, count in bt_decisions.most_common():
        print(f"  {decision}: {count}")

    print(f"\nPaper Trades: {len(active_trades)} active")
    print(f"Methods Tracked: {len(methods)}")
    print(f"High-Synergy Stacks (>=90): {len(high_synergy)}")
    print(f"Mega Ralph Tasks Completed: {len(completed_tasks)}")

    # Generate priority recommendations
    print(f"\nPriority Recommendations:")

    # Recommend backtesting for high-count pending
    pending = status_counts.get('PENDING_REVIEW', 0)
    if pending > 20:
        print(f"  ALERT: {pending} entries PENDING_REVIEW. Run batch review.")

    # Recommend paper trading for SCALE decisions
    scale_count = bt_decisions.get('SCALE', 0)
    if scale_count > 0 and len(active_trades) < 3:
        print(f"  RECOMMEND: {scale_count} alpha scored SCALE. Start paper trades.")

    # Check for expired paper trades
    now = datetime.now()
    for trade in pt_rows:
        end = trade.get('end_date', '')
        if end and trade.get('status', '').upper() == 'ACTIVE':
            try:
                if now > datetime.fromisoformat(end):
                    print(f"  EXPIRED: Paper trade {trade.get('trade_id', '')} needs completion review.")
            except ValueError:
                pass

    print()


def main():
    parser = argparse.ArgumentParser(
        description='Quant Reflection Engine - Integrate quant infrastructure into mega ralph',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s run            Full reflection cycle
  %(prog)s backtest       Auto-backtest pending alpha
  %(prog)s paper-check    Check paper trade status
  %(prog)s stacks         Stack recommendations
  %(prog)s summary        Print summary
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    sub_run = subparsers.add_parser('run', help='Full reflection cycle')
    sub_run.set_defaults(func=cmd_run)

    sub_bt = subparsers.add_parser('backtest', help='Auto-backtest pending alpha')
    sub_bt.set_defaults(func=cmd_backtest)

    sub_pt = subparsers.add_parser('paper-check', help='Check paper trade status')
    sub_pt.set_defaults(func=cmd_paper_check)

    sub_st = subparsers.add_parser('stacks', help='Stack recommendations')
    sub_st.set_defaults(func=cmd_stacks)

    sub_sum = subparsers.add_parser('summary', help='Print reflection summary')
    sub_sum.set_defaults(func=cmd_summary)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
