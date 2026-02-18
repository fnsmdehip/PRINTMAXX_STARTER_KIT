#!/usr/bin/env python3
"""
Paper Trading System - Test methods with minimal capital before full deployment

Like hedge funds paper trade before going live, test solopreneurship methods
with $0-100 budgets and 7-14 day validation windows.

Decision Matrix:
- Revenue/hour >$20 = SCALE
- Scalability score >7 = SCALE
- Platform risk <5 = SAFE
- Any metric fails = KILL or ITERATE

Usage:
    python3 paper_trade.py --method MM001_APP_FACTORY --budget 100 --days 14
    python3 paper_trade.py --list  # List all active paper trades
    python3 paper_trade.py --results PAPER_TRADE_001  # Get results
"""

import csv
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_DIR / "LEDGER"
PAPER_TRADE_DIR = LEDGER_DIR / "PAPER_TRADES"
PAPER_TRADE_DIR.mkdir(exist_ok=True)

@dataclass
class PaperTradeMetrics:
    """Metrics tracked during paper trade"""
    capital_invested: float
    time_invested_hours: float
    revenue_generated: float
    leads_generated: int
    conversion_rate: float
    revenue_per_hour: float
    scalability_score: int  # 1-10
    platform_risk: int  # 1-10

    def to_dict(self) -> Dict:
        return asdict(self)

    def passes_threshold(self) -> bool:
        """Check if metrics pass scale threshold"""
        passes = []

        # Revenue/hour threshold
        if self.revenue_per_hour >= 20:
            passes.append("revenue_per_hour")

        # Scalability threshold
        if self.scalability_score >= 7:
            passes.append("scalability")

        # Platform risk threshold (lower is better)
        if self.platform_risk <= 5:
            passes.append("platform_risk")

        # Need at least 2 of 3 criteria
        return len(passes) >= 2

@dataclass
class PaperTrade:
    """Paper trade experiment"""
    trade_id: str
    method_id: str  # MM001, CF003, AI005, etc
    alpha_id: str  # Which alpha is being tested
    budget: float
    duration_days: int
    start_date: str
    end_date: str
    status: str  # RUNNING, COMPLETE, KILLED
    metrics: PaperTradeMetrics
    decision: str  # SCALE, KILL, ITERATE
    notes: str

    def to_dict(self) -> Dict:
        result = asdict(self)
        result['metrics'] = self.metrics.to_dict()
        return result


class PaperTradeManager:
    """Manage paper trading experiments"""

    def __init__(self):
        self.trades_file = PAPER_TRADE_DIR / "PAPER_TRADES.csv"
        self.results_file = PAPER_TRADE_DIR / "PAPER_TRADE_RESULTS.csv"

    def start_paper_trade(
        self,
        method_id: str,
        alpha_id: str,
        budget: float,
        duration_days: int,
        notes: str = ""
    ) -> str:
        """Start a new paper trade"""

        # Generate trade ID
        trade_id = self._generate_trade_id()

        # Calculate dates
        start_date = datetime.now().isoformat()
        end_date = (datetime.now() + timedelta(days=duration_days)).isoformat()

        # Initialize empty metrics
        metrics = PaperTradeMetrics(
            capital_invested=budget,
            time_invested_hours=0,
            revenue_generated=0,
            leads_generated=0,
            conversion_rate=0.0,
            revenue_per_hour=0.0,
            scalability_score=5,
            platform_risk=5
        )

        # Create paper trade
        trade = PaperTrade(
            trade_id=trade_id,
            method_id=method_id,
            alpha_id=alpha_id,
            budget=budget,
            duration_days=duration_days,
            start_date=start_date,
            end_date=end_date,
            status="RUNNING",
            metrics=metrics,
            decision="PENDING",
            notes=notes
        )

        # Save to CSV
        self._save_trade(trade)

        print(f"Started paper trade: {trade_id}")
        print(f"Method: {method_id}")
        print(f"Budget: ${budget}")
        print(f"Duration: {duration_days} days")
        print(f"End date: {end_date[:10]}")

        return trade_id

    def update_metrics(
        self,
        trade_id: str,
        time_hours: float = None,
        revenue: float = None,
        leads: int = None,
        scalability: int = None,
        platform_risk: int = None
    ) -> None:
        """Update metrics for a running paper trade"""

        trade = self._load_trade(trade_id)
        if not trade:
            print(f"Trade {trade_id} not found")
            return

        # Update metrics
        if time_hours is not None:
            trade.metrics.time_invested_hours = time_hours
        if revenue is not None:
            trade.metrics.revenue_generated = revenue
        if leads is not None:
            trade.metrics.leads_generated = leads
        if scalability is not None:
            trade.metrics.scalability_score = scalability
        if platform_risk is not None:
            trade.metrics.platform_risk = platform_risk

        # Recalculate derived metrics
        if trade.metrics.time_invested_hours > 0:
            trade.metrics.revenue_per_hour = (
                trade.metrics.revenue_generated / trade.metrics.time_invested_hours
            )

        if trade.metrics.leads_generated > 0 and trade.metrics.revenue_generated > 0:
            # Rough conversion estimate (leads that became revenue)
            # This is a simplification - real conversion tracking is more complex
            trade.metrics.conversion_rate = min(
                1.0,
                (trade.metrics.revenue_generated / 100) / trade.metrics.leads_generated
            )

        # Save updated trade
        self._update_trade(trade)

        print(f"Updated metrics for {trade_id}")
        self._print_metrics(trade.metrics)

    def complete_paper_trade(self, trade_id: str) -> Dict:
        """Complete paper trade and make decision"""

        trade = self._load_trade(trade_id)
        if not trade:
            return {"error": f"Trade {trade_id} not found"}

        # Check if duration is complete
        end_date = datetime.fromisoformat(trade.end_date)
        if datetime.now() < end_date:
            days_remaining = (end_date - datetime.now()).days
            print(f"Warning: Paper trade ends in {days_remaining} days")

        # Make decision based on metrics
        if trade.metrics.passes_threshold():
            trade.decision = "SCALE"
            recommendation = f"SCALE: Increase budget 2x to ${trade.budget * 2}"
        else:
            # Check if close to threshold
            if trade.metrics.revenue_per_hour >= 15:
                trade.decision = "ITERATE"
                recommendation = "ITERATE: Close to threshold, adjust and retest"
            else:
                trade.decision = "KILL"
                recommendation = "KILL: Metrics don't justify scaling"

        trade.status = "COMPLETE"

        # Save results
        self._save_results(trade)
        self._update_trade(trade)

        result = {
            "trade_id": trade_id,
            "decision": trade.decision,
            "recommendation": recommendation,
            "metrics": trade.metrics.to_dict()
        }

        print(f"\n=== Paper Trade Complete: {trade_id} ===")
        print(f"Decision: {trade.decision}")
        print(f"Recommendation: {recommendation}")
        print(f"\nMetrics:")
        self._print_metrics(trade.metrics)

        return result

    def list_active_trades(self) -> List[Dict]:
        """List all active paper trades"""
        active = []

        if not self.trades_file.exists():
            return active

        try:
            with open(self.trades_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('status') == 'RUNNING':
                        # Calculate days remaining
                        end_date = datetime.fromisoformat(row['end_date'])
                        days_remaining = (end_date - datetime.now()).days

                        active.append({
                            'trade_id': row['trade_id'],
                            'method_id': row['method_id'],
                            'alpha_id': row['alpha_id'],
                            'budget': row['budget'],
                            'days_remaining': max(0, days_remaining),
                            'status': row['status']
                        })
        except Exception as e:
            print(f"Error loading trades: {e}")

        return active

    def get_results(self, trade_id: str = None) -> List[Dict]:
        """Get paper trade results"""
        results = []

        if not self.results_file.exists():
            return results

        try:
            with open(self.results_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if trade_id is None or row['trade_id'] == trade_id:
                        results.append(row)
        except Exception as e:
            print(f"Error loading results: {e}")

        return results

    def _generate_trade_id(self) -> str:
        """Generate unique trade ID"""
        # Count existing trades
        count = 0
        if self.trades_file.exists():
            with open(self.trades_file, 'r') as f:
                count = sum(1 for _ in f) - 1  # Subtract header

        return f"PAPER_TRADE_{count + 1:03d}"

    def _save_trade(self, trade: PaperTrade) -> None:
        """Save trade to CSV"""
        file_exists = self.trades_file.exists()

        with open(self.trades_file, 'a', newline='') as f:
            fieldnames = [
                'trade_id', 'method_id', 'alpha_id', 'budget', 'duration_days',
                'start_date', 'end_date', 'status', 'decision', 'notes',
                # Metrics
                'capital_invested', 'time_invested_hours', 'revenue_generated',
                'leads_generated', 'conversion_rate', 'revenue_per_hour',
                'scalability_score', 'platform_risk'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            # Flatten trade data
            row = {
                'trade_id': trade.trade_id,
                'method_id': trade.method_id,
                'alpha_id': trade.alpha_id,
                'budget': trade.budget,
                'duration_days': trade.duration_days,
                'start_date': trade.start_date,
                'end_date': trade.end_date,
                'status': trade.status,
                'decision': trade.decision,
                'notes': trade.notes,
                **trade.metrics.to_dict()
            }
            writer.writerow(row)

    def _update_trade(self, trade: PaperTrade) -> None:
        """Update existing trade in CSV"""
        if not self.trades_file.exists():
            return

        # Read all trades
        trades = []
        with open(self.trades_file, 'r') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row['trade_id'] == trade.trade_id:
                    # Update this row
                    row = {
                        'trade_id': trade.trade_id,
                        'method_id': trade.method_id,
                        'alpha_id': trade.alpha_id,
                        'budget': trade.budget,
                        'duration_days': trade.duration_days,
                        'start_date': trade.start_date,
                        'end_date': trade.end_date,
                        'status': trade.status,
                        'decision': trade.decision,
                        'notes': trade.notes,
                        **trade.metrics.to_dict()
                    }
                trades.append(row)

        # Write all trades back
        with open(self.trades_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(trades)

    def _load_trade(self, trade_id: str) -> PaperTrade:
        """Load trade from CSV"""
        if not self.trades_file.exists():
            return None

        try:
            with open(self.trades_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['trade_id'] == trade_id:
                        # Reconstruct PaperTrade object
                        metrics = PaperTradeMetrics(
                            capital_invested=float(row['capital_invested']),
                            time_invested_hours=float(row['time_invested_hours']),
                            revenue_generated=float(row['revenue_generated']),
                            leads_generated=int(row['leads_generated']),
                            conversion_rate=float(row['conversion_rate']),
                            revenue_per_hour=float(row['revenue_per_hour']),
                            scalability_score=int(row['scalability_score']),
                            platform_risk=int(row['platform_risk'])
                        )

                        return PaperTrade(
                            trade_id=row['trade_id'],
                            method_id=row['method_id'],
                            alpha_id=row['alpha_id'],
                            budget=float(row['budget']),
                            duration_days=int(row['duration_days']),
                            start_date=row['start_date'],
                            end_date=row['end_date'],
                            status=row['status'],
                            metrics=metrics,
                            decision=row['decision'],
                            notes=row['notes']
                        )
        except Exception as e:
            print(f"Error loading trade: {e}")

        return None

    def _save_results(self, trade: PaperTrade) -> None:
        """Save completed trade results"""
        file_exists = self.results_file.exists()

        with open(self.results_file, 'a', newline='') as f:
            fieldnames = [
                'trade_id', 'method_id', 'alpha_id', 'decision',
                'revenue_per_hour', 'scalability_score', 'platform_risk',
                'total_revenue', 'total_time_hours', 'total_investment',
                'roi_percent', 'completed_date', 'notes'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            # Calculate ROI
            roi = 0
            if trade.metrics.capital_invested > 0:
                roi = (trade.metrics.revenue_generated - trade.metrics.capital_invested) / trade.metrics.capital_invested * 100

            row = {
                'trade_id': trade.trade_id,
                'method_id': trade.method_id,
                'alpha_id': trade.alpha_id,
                'decision': trade.decision,
                'revenue_per_hour': trade.metrics.revenue_per_hour,
                'scalability_score': trade.metrics.scalability_score,
                'platform_risk': trade.metrics.platform_risk,
                'total_revenue': trade.metrics.revenue_generated,
                'total_time_hours': trade.metrics.time_invested_hours,
                'total_investment': trade.metrics.capital_invested,
                'roi_percent': roi,
                'completed_date': datetime.now().isoformat(),
                'notes': trade.notes
            }
            writer.writerow(row)

    def _print_metrics(self, metrics: PaperTradeMetrics) -> None:
        """Pretty print metrics"""
        print(f"  Capital Invested: ${metrics.capital_invested}")
        print(f"  Time Invested: {metrics.time_invested_hours}h")
        print(f"  Revenue Generated: ${metrics.revenue_generated}")
        print(f"  Revenue/Hour: ${metrics.revenue_per_hour:.2f}")
        print(f"  Leads Generated: {metrics.leads_generated}")
        print(f"  Conversion Rate: {metrics.conversion_rate*100:.1f}%")
        print(f"  Scalability Score: {metrics.scalability_score}/10")
        print(f"  Platform Risk: {metrics.platform_risk}/10")


def main():
    parser = argparse.ArgumentParser(description='Paper Trading System')
    parser.add_argument('--method', help='Method ID (e.g. MM001_APP_FACTORY)')
    parser.add_argument('--alpha', help='Alpha ID being tested')
    parser.add_argument('--budget', type=float, default=100, help='Budget ($0-100)')
    parser.add_argument('--days', type=int, default=14, help='Duration in days (7-14)')
    parser.add_argument('--notes', default='', help='Notes about this paper trade')

    parser.add_argument('--update', help='Update trade metrics (trade ID)')
    parser.add_argument('--time', type=float, help='Time invested (hours)')
    parser.add_argument('--revenue', type=float, help='Revenue generated ($)')
    parser.add_argument('--leads', type=int, help='Leads generated')
    parser.add_argument('--scalability', type=int, help='Scalability score (1-10)')
    parser.add_argument('--risk', type=int, help='Platform risk (1-10)')

    parser.add_argument('--complete', help='Complete paper trade (trade ID)')
    parser.add_argument('--list', action='store_true', help='List active paper trades')
    parser.add_argument('--results', nargs='?', const=True, help='Show results (optional trade ID)')

    args = parser.parse_args()

    manager = PaperTradeManager()

    if args.list:
        active = manager.list_active_trades()
        if not active:
            print("No active paper trades")
        else:
            print("\n=== Active Paper Trades ===")
            for trade in active:
                print(f"{trade['trade_id']}: {trade['method_id']} (${trade['budget']}, {trade['days_remaining']}d remaining)")

    elif args.results:
        trade_id = args.results if isinstance(args.results, str) else None
        results = manager.get_results(trade_id)

        if not results:
            print("No results found")
        else:
            print("\n=== Paper Trade Results ===")
            for result in results:
                print(f"\n{result['trade_id']} - {result['method_id']}")
                print(f"  Decision: {result['decision']}")
                print(f"  Revenue/Hour: ${result['revenue_per_hour']}")
                print(f"  ROI: {result['roi_percent']}%")
                print(f"  Scalability: {result['scalability_score']}/10")

    elif args.update:
        manager.update_metrics(
            trade_id=args.update,
            time_hours=args.time,
            revenue=args.revenue,
            leads=args.leads,
            scalability=args.scalability,
            platform_risk=args.risk
        )

    elif args.complete:
        manager.complete_paper_trade(args.complete)

    elif args.method and args.alpha:
        manager.start_paper_trade(
            method_id=args.method,
            alpha_id=args.alpha,
            budget=args.budget,
            duration_days=args.days,
            notes=args.notes
        )

    else:
        print("Please specify an action (--method + --alpha, --list, --update, --complete, or --results)")
        parser.print_help()


if __name__ == "__main__":
    main()
