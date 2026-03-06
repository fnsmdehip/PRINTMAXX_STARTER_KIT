#!/usr/bin/env python3
"""
Alpha Backtesting System
Validate tactics with historical data before deploying capital

Backtesting Framework:
1. Historical Validation - multiple sources, specific numbers, timeline
2. Proxy Metrics - engagement rate, conversion rate, retention
3. Scoring System (0-100) - only deploy methods with score >70
4. Decision: SCALE or KILL

Usage:
    python3 backtest_alpha.py ALPHA524
    python3 backtest_alpha.py --pending  # Backtest all PENDING_REVIEW
    python3 backtest_alpha.py --all      # Backtest all entries
"""

import csv
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict

PROJECT_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_DIR / "LEDGER"
BACKTEST_DIR = LEDGER_DIR / "BACKTESTS"
BACKTEST_DIR.mkdir(exist_ok=True)

class AlphaBacktester:
    """Backtest alpha entries before deployment"""

    def __init__(self):
        self.alpha_file = LEDGER_DIR / "ALPHA_STAGING.csv"
        self.backtest_output = BACKTEST_DIR / "BACKTEST_RESULTS.csv"

    def backtest_alpha(self, alpha_id: str) -> Dict[str, Any]:
        """
        Backtest a single alpha entry

        Returns backtest score (0-100) and decision (SCALE/KILL)
        """
        # Load alpha entry
        alpha = self._load_alpha(alpha_id)
        if not alpha:
            return {"error": f"Alpha {alpha_id} not found"}

        score = 0
        details = {}

        # 1. Historical Validation (60 points max)
        score += self._check_multiple_sources(alpha)  # 20 points
        score += self._check_specific_numbers(alpha)  # 20 points
        score += self._check_timeline(alpha)  # 15 points
        score += self._check_still_works_2026(alpha)  # 20 points

        # 2. Proxy Metrics (25 points max)
        score += self._check_engagement_data(alpha)  # 10 points
        score += self._check_conversion_data(alpha)  # 15 points

        # 3. Replicability Check (15 points max)
        score += self._check_replicability(alpha)  # 15 points

        # Decision logic
        decision = "SCALE" if score >= 70 else "KILL"
        if 50 <= score < 70:
            decision = "PAPER_TRADE"  # Test with minimal capital first

        result = {
            "alpha_id": alpha_id,
            "backtest_score": score,
            "decision": decision,
            "category": alpha.get("category", "N/A"),
            "source": alpha.get("source", "N/A"),
            "timestamp": datetime.now().isoformat(),
            "details": {
                "multiple_sources": self._check_multiple_sources(alpha) > 0,
                "has_numbers": self._check_specific_numbers(alpha) > 0,
                "has_timeline": self._check_timeline(alpha) > 0,
                "still_valid_2026": self._check_still_works_2026(alpha) > 0,
                "engagement_data": self._check_engagement_data(alpha) > 0,
                "conversion_data": self._check_conversion_data(alpha) > 0,
                "replicable": self._check_replicability(alpha) > 0,
            }
        }

        return result

    def _load_alpha(self, alpha_id: str) -> Dict[str, str]:
        """Load alpha entry from ALPHA_STAGING.csv"""
        try:
            with open(self.alpha_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('alpha_id') == alpha_id:
                        return row
        except Exception as e:
            print(f"Error loading alpha: {e}")
        return {}

    def _check_multiple_sources(self, alpha: Dict) -> int:
        """Check if tactic has multiple independent sources (20 points)"""
        # Check notes/description for mentions of multiple sources
        description = alpha.get('description', '') + alpha.get('reviewer_notes', '')

        # Keywords indicating multiple sources
        multi_source_keywords = [
            'multiple sources',
            'verified by',
            'confirmed by',
            'seen on',
            'case studies',
            'several people',
        ]

        if any(keyword in description.lower() for keyword in multi_source_keywords):
            return 20
        elif alpha.get('source_url'):  # At least one source
            return 10
        else:
            return 0

    def _check_specific_numbers(self, alpha: Dict) -> int:
        """Check if alpha has specific numbers (20 points)"""
        description = alpha.get('description', '') + alpha.get('tactic', '')

        # Look for revenue numbers
        revenue_indicators = ['$', 'revenue', 'made', 'earned', 'profit']
        has_revenue = any(ind in description.lower() for ind in revenue_indicators)

        # Look for percentage numbers
        has_percentages = '%' in description

        # Look for time numbers
        time_indicators = ['days', 'weeks', 'months', 'hours']
        has_time = any(ind in description.lower() for ind in time_indicators)

        if has_revenue and has_percentages and has_time:
            return 20
        elif has_revenue and (has_percentages or has_time):
            return 15
        elif has_revenue or has_percentages:
            return 10
        else:
            return 5

    def _check_timeline(self, alpha: Dict) -> int:
        """Check if there's a clear timeline (15 points)"""
        description = alpha.get('description', '') + alpha.get('tactic', '')

        # Timeline indicators
        timeline_keywords = [
            'in 30 days',
            'within weeks',
            'month',
            'after',
            'timeline',
            'took',
            'hours',
        ]

        if any(keyword in description.lower() for keyword in timeline_keywords):
            return 15
        else:
            return 0

    def _check_still_works_2026(self, alpha: Dict) -> int:
        """Check if method still works in 2026 (20 points)"""
        created_at = alpha.get('created_at', '')

        # If created in 2026, assume still valid
        if '2026' in created_at:
            return 20

        # Check for algorithm change warnings
        description = alpha.get('description', '') + alpha.get('reviewer_notes', '')
        dead_keywords = [
            'no longer works',
            'algorithm changed',
            'patched',
            'banned',
            'shut down',
        ]

        if any(keyword in description.lower() for keyword in dead_keywords):
            return 0

        # Check category - some have higher risk of obsolescence
        high_risk_categories = ['PLATFORM_ARBITRAGE', 'AUTOMATION_HACK']
        if alpha.get('category') in high_risk_categories:
            return 10  # Partial credit, needs verification

        return 15  # Default: probably still works

    def _check_engagement_data(self, alpha: Dict) -> int:
        """Check if has engagement/proxy metrics (10 points)"""
        description = alpha.get('description', '')

        engagement_keywords = [
            'engagement rate',
            'reply rate',
            'click rate',
            'view count',
            'impressions',
            'likes',
            'shares',
        ]

        if any(keyword in description.lower() for keyword in engagement_keywords):
            return 10
        else:
            return 0

    def _check_conversion_data(self, alpha: Dict) -> int:
        """Check if has conversion data (15 points)"""
        description = alpha.get('description', '')

        conversion_keywords = [
            'conversion rate',
            'conversion',
            'signup rate',
            'sale',
            'closed',
            'roi',
        ]

        if any(keyword in description.lower() for keyword in conversion_keywords):
            return 15
        else:
            return 0

    def _check_replicability(self, alpha: Dict) -> int:
        """Check if tactic is clearly replicable (15 points)"""
        tactic = alpha.get('tactic', '')

        # Check if has specific steps
        has_steps = any(str(i) in tactic for i in range(1, 6))  # Numbered steps

        # Check if has tools/platforms mentioned
        has_tools = any(word in tactic.lower() for word in [
            'using', 'with', 'via', 'tool', 'platform', 'api'
        ])

        # Check if has clear actionable verbs
        action_verbs = ['create', 'build', 'send', 'post', 'generate', 'use']
        has_actions = any(verb in tactic.lower() for verb in action_verbs)

        score = 0
        if has_steps:
            score += 8
        if has_tools:
            score += 4
        if has_actions:
            score += 3

        return min(score, 15)

    def backtest_batch(self, alpha_ids: List[str]) -> List[Dict]:
        """Backtest multiple alpha entries"""
        results = []
        for alpha_id in alpha_ids:
            result = self.backtest_alpha(alpha_id)
            results.append(result)
            print(f"Backtested {alpha_id}: Score {result.get('backtest_score', 0)} - {result.get('decision', 'N/A')}")

        return results

    def save_results(self, results: List[Dict]) -> None:
        """Save backtest results to CSV"""
        if not results:
            return

        # Check if file exists to determine if we need header
        file_exists = self.backtest_output.exists()

        with open(self.backtest_output, 'a', newline='') as f:
            fieldnames = [
                'alpha_id', 'backtest_score', 'decision', 'category', 'source',
                'timestamp', 'multiple_sources', 'has_numbers', 'has_timeline',
                'still_valid_2026', 'engagement_data', 'conversion_data', 'replicable'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            for result in results:
                # Flatten details
                row = {
                    'alpha_id': result['alpha_id'],
                    'backtest_score': result['backtest_score'],
                    'decision': result['decision'],
                    'category': result['category'],
                    'source': result['source'],
                    'timestamp': result['timestamp'],
                    **result['details']
                }
                writer.writerow(row)

        print(f"\nResults saved to {self.backtest_output}")

    def get_pending_alpha(self) -> List[str]:
        """Get all PENDING_REVIEW alpha IDs"""
        pending = []
        try:
            with open(self.alpha_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('status') == 'PENDING_REVIEW':
                        pending.append(row.get('alpha_id'))
        except Exception as e:
            print(f"Error loading pending alpha: {e}")

        return pending


def main():
    parser = argparse.ArgumentParser(description='Backtest alpha entries')
    parser.add_argument('alpha_id', nargs='?', help='Alpha ID to backtest (e.g. ALPHA524)')
    parser.add_argument('--pending', action='store_true', help='Backtest all PENDING_REVIEW entries')
    parser.add_argument('--all', action='store_true', help='Backtest all entries')
    parser.add_argument('--threshold', type=int, default=70, help='Score threshold for SCALE decision')

    args = parser.parse_args()

    backtester = AlphaBacktester()

    if args.pending:
        print("Backtesting all PENDING_REVIEW entries...")
        alpha_ids = backtester.get_pending_alpha()
        if not alpha_ids:
            print("No PENDING_REVIEW entries found")
            return

        results = backtester.backtest_batch(alpha_ids)
        backtester.save_results(results)

        # Summary stats
        total = len(results)
        scale = sum(1 for r in results if r['decision'] == 'SCALE')
        paper = sum(1 for r in results if r['decision'] == 'PAPER_TRADE')
        kill = sum(1 for r in results if r['decision'] == 'KILL')

        print(f"\n=== Backtest Summary ===")
        print(f"Total: {total}")
        print(f"SCALE: {scale} ({scale/total*100:.1f}%)")
        print(f"PAPER_TRADE: {paper} ({paper/total*100:.1f}%)")
        print(f"KILL: {kill} ({kill/total*100:.1f}%)")

    elif args.alpha_id:
        result = backtester.backtest_alpha(args.alpha_id)

        if 'error' in result:
            print(result['error'])
            return

        print(f"\n=== Backtest Result: {args.alpha_id} ===")
        print(f"Score: {result['backtest_score']}/100")
        print(f"Decision: {result['decision']}")
        print(f"Category: {result['category']}")
        print(f"Source: {result['source']}")
        print(f"\nDetails:")
        for key, value in result['details'].items():
            print(f"  {key}: {value}")

        backtester.save_results([result])

    else:
        print("Please specify an alpha ID or use --pending/--all")
        parser.print_help()


if __name__ == "__main__":
    main()
