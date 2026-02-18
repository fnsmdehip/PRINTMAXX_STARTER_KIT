#!/usr/bin/env python3
"""
PRINTMAXX Portfolio Rebalancer
Jane Street / Renaissance Technologies style automated rebalancing recommendations

Monitors all active methods and generates KILL/SCALE/REDUCE/ADD recommendations
based on performance data, risk limits, and portfolio theory.

Usage:
    python3 portfolio_rebalancer.py                    # Full analysis + recommendations
    python3 portfolio_rebalancer.py --weekly-report    # Generate weekly rebalance report
    python3 portfolio_rebalancer.py --simulate         # Dry run, no file writes
    python3 portfolio_rebalancer.py --alerts-only      # Only show critical alerts

Decision Thresholds (Quant Fund Style):
    - 90-day lookback for performance
    - 95% confidence before KILL
    - Scale gradually (2x, not 10x)

Risk Limits:
    - Max 40% in any single method
    - Max 50% on any single platform
    - Min 3 active methods (diversification)
"""

import os
import sys
import csv
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import statistics

# Paths
PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_DIR / "LEDGER"
FINANCIALS_DIR = PROJECT_DIR / "FINANCIALS"
AUTOMATIONS_DIR = PROJECT_DIR / "AUTOMATIONS"

# Output files
REBALANCE_RECOMMENDATIONS_FILE = LEDGER_DIR / "REBALANCE_RECOMMENDATIONS.csv"
WEEKLY_REPORT_DIR = LEDGER_DIR / "REBALANCE_REPORTS"

# Decision thresholds
KILL_THRESHOLD_REVENUE_PER_HOUR = 15.0  # Kill if < $15/hour for 30+ days
SCALE_THRESHOLD_REVENUE_PER_HOUR = 50.0  # Scale 2x if > $50/hour
SCALE_SHARPE_THRESHOLD = 2.0  # Require Sharpe > 2.0 for scaling
MAX_METHOD_CONCENTRATION = 0.40  # Max 40% in any single method
MAX_PLATFORM_CONCENTRATION = 0.50  # Max 50% on any single platform
MIN_ACTIVE_METHODS = 3  # Minimum diversification
LOOKBACK_DAYS = 90  # Performance lookback period
KILL_CONFIDENCE_THRESHOLD = 0.95  # 95% confidence before KILL
MIN_DATA_POINTS_FOR_KILL = 14  # Need at least 14 days of data before killing


@dataclass
class MethodMetrics:
    """Performance metrics for a single method"""
    method_id: str
    method_name: str
    category: str
    status: str
    platform: str = ""

    # Revenue metrics
    total_revenue: float = 0.0
    total_time_hours: float = 0.0
    revenue_per_hour: float = 0.0

    # Performance over time
    daily_revenues: List[float] = field(default_factory=list)
    win_rate: float = 0.0  # % of days with positive revenue
    sharpe_ratio: float = 0.0

    # Capital allocation
    capital_invested: float = 0.0
    revenue_percentage: float = 0.0

    # Metadata
    days_active: int = 0
    first_revenue_date: Optional[datetime] = None
    last_revenue_date: Optional[datetime] = None

    def calculate_derived_metrics(self):
        """Calculate Sharpe ratio and win rate from daily revenues"""
        if not self.daily_revenues:
            return

        # Revenue per hour
        if self.total_time_hours > 0:
            self.revenue_per_hour = self.total_revenue / self.total_time_hours

        # Win rate
        winning_days = sum(1 for r in self.daily_revenues if r > 0)
        self.win_rate = winning_days / len(self.daily_revenues) if self.daily_revenues else 0

        # Sharpe ratio (using daily revenue as returns)
        if len(self.daily_revenues) > 1:
            mean_return = statistics.mean(self.daily_revenues)
            std_return = statistics.stdev(self.daily_revenues)
            # Annualized Sharpe (assuming 252 trading days)
            if std_return > 0:
                self.sharpe_ratio = (mean_return / std_return) * (252 ** 0.5)
            else:
                self.sharpe_ratio = 0

        self.days_active = len(self.daily_revenues)


@dataclass
class RebalanceRecommendation:
    """A single rebalancing recommendation"""
    method_id: str
    method_name: str
    action: str  # KILL, SCALE, REDUCE, ADD, HOLD
    reason: str
    current_allocation: float  # Percentage
    recommended_allocation: float  # Percentage
    confidence: float  # 0-1
    priority: str  # CRITICAL, HIGH, MEDIUM, LOW
    metrics: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'method_id': self.method_id,
            'method_name': self.method_name,
            'action': self.action,
            'reason': self.reason,
            'current_allocation': f"{self.current_allocation:.1%}",
            'recommended_allocation': f"{self.recommended_allocation:.1%}",
            'confidence': f"{self.confidence:.0%}",
            'priority': self.priority,
            'revenue_per_hour': self.metrics.get('revenue_per_hour', 'N/A'),
            'sharpe_ratio': self.metrics.get('sharpe_ratio', 'N/A'),
            'win_rate': self.metrics.get('win_rate', 'N/A'),
            'days_active': self.metrics.get('days_active', 'N/A'),
            'timestamp': self.timestamp.isoformat()
        }


class PortfolioRebalancer:
    """
    Automated portfolio rebalancing recommendation system.

    Monitors all active methods and generates recommendations based on:
    - Revenue per hour thresholds
    - Sharpe ratio requirements
    - Concentration limits
    - Diversification minimums
    """

    def __init__(self, simulate: bool = False):
        self.simulate = simulate
        self.methods: Dict[str, MethodMetrics] = {}
        self.recommendations: List[RebalanceRecommendation] = []
        self.alerts: List[str] = []
        self.total_revenue = 0.0
        self.total_capital = 0.0

    def load_methods(self) -> None:
        """Load methods from MONEY_METHODS_TRACKER.csv"""
        tracker_file = LEDGER_DIR / "MONEY_METHODS_TRACKER.csv"

        if not tracker_file.exists():
            print(f"[ERROR] Methods tracker not found: {tracker_file}")
            return

        with open(tracker_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                method_id = row.get('method_id', '')
                if not method_id:
                    continue

                # Determine platform from method category or name
                platform = self._infer_platform(method_id, row.get('category', ''), row.get('method_name', ''))

                self.methods[method_id] = MethodMetrics(
                    method_id=method_id,
                    method_name=row.get('method_name', method_id),
                    category=row.get('category', 'UNKNOWN'),
                    status=row.get('status', 'New'),
                    platform=platform
                )

        print(f"[INFO] Loaded {len(self.methods)} methods from tracker")

    def _infer_platform(self, method_id: str, category: str, name: str) -> str:
        """Infer platform from method attributes"""
        name_lower = name.lower()
        id_lower = method_id.lower()

        platform_keywords = {
            'X_TWITTER': ['twitter', 'x_', 'tweet'],
            'TIKTOK': ['tiktok', 'tt_'],
            'YOUTUBE': ['youtube', 'yt_', 'shorts'],
            'INSTAGRAM': ['instagram', 'ig_', 'reels'],
            'GUMROAD': ['gumroad', 'digital_products', 'notion'],
            'APP_STORE': ['app_factory', 'app_', 'ios'],
            'EMAIL': ['cold_outbound', 'email', 'newsletter'],
            'AMAZON': ['amazon', 'kdp', 'fba'],
            'ETSY': ['etsy'],
            'LINKEDIN': ['linkedin'],
            'ROBLOX': ['roblox'],
            'TWITCH': ['twitch', 'streamer'],
        }

        for platform, keywords in platform_keywords.items():
            for kw in keywords:
                if kw in name_lower or kw in id_lower:
                    return platform

        return 'MULTI_PLATFORM'

    def load_revenue_data(self) -> None:
        """Load revenue data from REVENUE_TRACKER.csv"""
        revenue_file = FINANCIALS_DIR / "REVENUE_TRACKER.csv"

        if not revenue_file.exists():
            print(f"[WARN] Revenue tracker not found: {revenue_file}")
            print("[INFO] Creating sample data structure for demonstration")
            return

        with open(revenue_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if not rows:
            print("[INFO] Revenue tracker is empty, no performance data yet")
            return

        # Aggregate by method
        cutoff_date = datetime.now() - timedelta(days=LOOKBACK_DAYS)

        for row in rows:
            method_id = row.get('method_id', '')
            if method_id not in self.methods:
                continue

            try:
                date_str = row.get('date', '')
                date = datetime.fromisoformat(date_str) if date_str else None

                # Skip data outside lookback window
                if date and date < cutoff_date:
                    continue

                revenue = float(row.get('revenue', 0) or 0)
                profit = float(row.get('profit', 0) or 0)

                method = self.methods[method_id]
                method.total_revenue += revenue
                method.daily_revenues.append(profit if profit else revenue)

                if method.first_revenue_date is None or (date and date < method.first_revenue_date):
                    method.first_revenue_date = date
                if method.last_revenue_date is None or (date and date > method.last_revenue_date):
                    method.last_revenue_date = date

            except (ValueError, TypeError) as e:
                continue

        # Calculate total revenue for percentage calculations
        self.total_revenue = sum(m.total_revenue for m in self.methods.values())

        # Calculate derived metrics
        for method in self.methods.values():
            method.calculate_derived_metrics()
            if self.total_revenue > 0:
                method.revenue_percentage = method.total_revenue / self.total_revenue

    def load_paper_trade_data(self) -> None:
        """Load paper trade results to inform recommendations"""
        paper_trades_file = LEDGER_DIR / "PAPER_TRADES" / "PAPER_TRADE_RESULTS.csv"

        if not paper_trades_file.exists():
            print(f"[INFO] No paper trade results found")
            return

        with open(paper_trades_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                method_id = row.get('method_id', '')

                # Try to match method_id (may have suffix like _COLD_OUTBOUND)
                matched_method = None
                for m_id in self.methods:
                    if m_id in method_id or method_id in m_id:
                        matched_method = self.methods[m_id]
                        break

                if not matched_method:
                    continue

                try:
                    revenue_per_hour = float(row.get('revenue_per_hour', 0) or 0)
                    total_time = float(row.get('total_time_hours', 0) or 0)
                    total_revenue = float(row.get('total_revenue', 0) or 0)

                    # Use paper trade data if we don't have real data
                    if matched_method.total_revenue == 0 and total_revenue > 0:
                        matched_method.total_revenue = total_revenue
                        matched_method.total_time_hours = total_time
                        matched_method.revenue_per_hour = revenue_per_hour

                except (ValueError, TypeError):
                    continue

    def load_backtest_data(self) -> None:
        """Load backtest results to find high-scoring alpha to add"""
        backtest_file = LEDGER_DIR / "BACKTESTS" / "BACKTEST_RESULTS.csv"

        if not backtest_file.exists():
            print(f"[INFO] No backtest results found")
            return

        self.scalable_alpha = []

        with open(backtest_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    score = int(row.get('backtest_score', 0) or 0)
                    decision = row.get('decision', '')

                    if score >= 70 and decision == 'SCALE':
                        self.scalable_alpha.append({
                            'alpha_id': row.get('alpha_id', ''),
                            'category': row.get('category', ''),
                            'score': score,
                            'source': row.get('source', '')
                        })
                except (ValueError, TypeError):
                    continue

        print(f"[INFO] Found {len(self.scalable_alpha)} scalable alpha entries (score >= 70)")

    def analyze_concentration_risk(self) -> Dict[str, float]:
        """Analyze portfolio concentration by method and platform"""
        method_concentrations = {}
        platform_concentrations = defaultdict(float)

        if self.total_revenue == 0:
            # Use capital invested if no revenue
            return {'status': 'pre_revenue', 'methods': {}, 'platforms': {}}

        for method_id, method in self.methods.items():
            concentration = method.revenue_percentage
            method_concentrations[method_id] = concentration
            platform_concentrations[method.platform] += concentration

        return {
            'status': 'active',
            'methods': method_concentrations,
            'platforms': dict(platform_concentrations)
        }

    def generate_kill_recommendations(self) -> None:
        """Generate KILL recommendations for underperforming methods"""
        for method_id, method in self.methods.items():
            # Skip inactive methods
            if method.status not in ['Active', 'ACTIVE', 'active']:
                continue

            # Need sufficient data before killing
            if method.days_active < MIN_DATA_POINTS_FOR_KILL:
                continue

            # Check revenue per hour threshold
            if method.revenue_per_hour > 0 and method.revenue_per_hour < KILL_THRESHOLD_REVENUE_PER_HOUR:
                # Calculate confidence based on data points
                confidence = min(method.days_active / 30, 1.0)  # Max confidence at 30 days

                # Only recommend kill if confidence >= 95%
                if confidence >= KILL_CONFIDENCE_THRESHOLD:
                    self.recommendations.append(RebalanceRecommendation(
                        method_id=method_id,
                        method_name=method.method_name,
                        action='KILL',
                        reason=f"Revenue/hour ${method.revenue_per_hour:.2f} < ${KILL_THRESHOLD_REVENUE_PER_HOUR} threshold for {method.days_active}+ days",
                        current_allocation=method.revenue_percentage,
                        recommended_allocation=0.0,
                        confidence=confidence,
                        priority='HIGH',
                        metrics={
                            'revenue_per_hour': f"${method.revenue_per_hour:.2f}",
                            'sharpe_ratio': f"{method.sharpe_ratio:.2f}",
                            'win_rate': f"{method.win_rate:.0%}",
                            'days_active': method.days_active
                        }
                    ))
                    self.alerts.append(f"KILL: {method.method_name} - ${method.revenue_per_hour:.2f}/hr < $15 threshold")

    def generate_scale_recommendations(self) -> None:
        """Generate SCALE recommendations for high performers"""
        for method_id, method in self.methods.items():
            # Skip if already at max concentration
            if method.revenue_percentage >= MAX_METHOD_CONCENTRATION:
                continue

            # Check both revenue/hour AND Sharpe ratio thresholds
            if (method.revenue_per_hour >= SCALE_THRESHOLD_REVENUE_PER_HOUR and
                method.sharpe_ratio >= SCALE_SHARPE_THRESHOLD):

                # Calculate target allocation (2x current, capped at max)
                target_allocation = min(method.revenue_percentage * 2, MAX_METHOD_CONCENTRATION)

                # Confidence based on data quality
                confidence = min(method.days_active / 60, 0.95)  # Max 95% confidence

                self.recommendations.append(RebalanceRecommendation(
                    method_id=method_id,
                    method_name=method.method_name,
                    action='SCALE',
                    reason=f"Revenue/hour ${method.revenue_per_hour:.2f} >= ${SCALE_THRESHOLD_REVENUE_PER_HOUR} AND Sharpe {method.sharpe_ratio:.2f} >= {SCALE_SHARPE_THRESHOLD}",
                    current_allocation=method.revenue_percentage,
                    recommended_allocation=target_allocation,
                    confidence=confidence,
                    priority='HIGH',
                    metrics={
                        'revenue_per_hour': f"${method.revenue_per_hour:.2f}",
                        'sharpe_ratio': f"{method.sharpe_ratio:.2f}",
                        'win_rate': f"{method.win_rate:.0%}",
                        'days_active': method.days_active
                    }
                ))
                self.alerts.append(f"SCALE 2x: {method.method_name} - ${method.revenue_per_hour:.2f}/hr, Sharpe {method.sharpe_ratio:.2f}")

    def generate_reduce_recommendations(self) -> None:
        """Generate REDUCE recommendations for over-concentrated positions"""
        concentration = self.analyze_concentration_risk()

        if concentration['status'] == 'pre_revenue':
            return

        # Check method concentration
        for method_id, conc in concentration['methods'].items():
            if conc > MAX_METHOD_CONCENTRATION:
                method = self.methods.get(method_id)
                if not method:
                    continue

                self.recommendations.append(RebalanceRecommendation(
                    method_id=method_id,
                    method_name=method.method_name,
                    action='REDUCE',
                    reason=f"Concentration {conc:.1%} exceeds {MAX_METHOD_CONCENTRATION:.0%} limit",
                    current_allocation=conc,
                    recommended_allocation=MAX_METHOD_CONCENTRATION,
                    confidence=1.0,
                    priority='CRITICAL',
                    metrics={
                        'revenue_per_hour': f"${method.revenue_per_hour:.2f}" if method.revenue_per_hour else 'N/A',
                        'sharpe_ratio': f"{method.sharpe_ratio:.2f}" if method.sharpe_ratio else 'N/A'
                    }
                ))
                self.alerts.append(f"REDUCE: {method.method_name} - {conc:.1%} concentration > 40% limit")

        # Check platform concentration
        for platform, conc in concentration['platforms'].items():
            if conc > MAX_PLATFORM_CONCENTRATION:
                self.alerts.append(f"PLATFORM RISK: {platform} has {conc:.1%} concentration (> {MAX_PLATFORM_CONCENTRATION:.0%} limit)")

    def generate_add_recommendations(self) -> None:
        """Generate ADD recommendations for high-scoring alpha not yet deployed"""
        if not hasattr(self, 'scalable_alpha'):
            return

        # Check diversification requirement
        active_methods = sum(1 for m in self.methods.values()
                           if m.status in ['Active', 'ACTIVE', 'active'] and m.total_revenue > 0)

        if active_methods < MIN_ACTIVE_METHODS:
            self.alerts.append(f"DIVERSIFICATION: Only {active_methods} active methods (min {MIN_ACTIVE_METHODS})")

        # Recommend top scalable alpha
        for alpha in sorted(self.scalable_alpha, key=lambda x: x['score'], reverse=True)[:5]:
            self.recommendations.append(RebalanceRecommendation(
                method_id=alpha['alpha_id'],
                method_name=f"{alpha['category']} - {alpha['source'][:30]}",
                action='ADD',
                reason=f"Backtest score {alpha['score']} >= 70, ready to deploy",
                current_allocation=0.0,
                recommended_allocation=0.05,  # Start with 5%
                confidence=alpha['score'] / 100,
                priority='MEDIUM',
                metrics={
                    'backtest_score': alpha['score'],
                    'category': alpha['category']
                }
            ))

    def generate_hold_recommendations(self) -> None:
        """Generate HOLD recommendations for methods meeting criteria"""
        for method_id, method in self.methods.items():
            # Skip if already has a recommendation
            if any(r.method_id == method_id for r in self.recommendations):
                continue

            # Only for active methods with data
            if method.status not in ['Active', 'ACTIVE', 'active']:
                continue

            if method.days_active == 0:
                continue

            # If performance is acceptable, recommend HOLD
            if (method.revenue_per_hour >= KILL_THRESHOLD_REVENUE_PER_HOUR and
                method.revenue_per_hour < SCALE_THRESHOLD_REVENUE_PER_HOUR):

                self.recommendations.append(RebalanceRecommendation(
                    method_id=method_id,
                    method_name=method.method_name,
                    action='HOLD',
                    reason=f"Performance acceptable: ${method.revenue_per_hour:.2f}/hr",
                    current_allocation=method.revenue_percentage,
                    recommended_allocation=method.revenue_percentage,
                    confidence=0.8,
                    priority='LOW',
                    metrics={
                        'revenue_per_hour': f"${method.revenue_per_hour:.2f}",
                        'sharpe_ratio': f"{method.sharpe_ratio:.2f}",
                        'win_rate': f"{method.win_rate:.0%}",
                        'days_active': method.days_active
                    }
                ))

    def save_recommendations(self) -> None:
        """Save recommendations to CSV"""
        if self.simulate:
            print("[SIMULATE] Would save recommendations to:", REBALANCE_RECOMMENDATIONS_FILE)
            return

        # Ensure directory exists
        REBALANCE_RECOMMENDATIONS_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(REBALANCE_RECOMMENDATIONS_FILE, 'w', newline='') as f:
            fieldnames = [
                'method_id', 'method_name', 'action', 'reason',
                'current_allocation', 'recommended_allocation', 'confidence',
                'priority', 'revenue_per_hour', 'sharpe_ratio', 'win_rate',
                'days_active', 'timestamp'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for rec in self.recommendations:
                writer.writerow(rec.to_dict())

        print(f"[INFO] Saved {len(self.recommendations)} recommendations to {REBALANCE_RECOMMENDATIONS_FILE}")

    def generate_weekly_report(self) -> str:
        """Generate weekly rebalance report"""
        report_lines = [
            "=" * 80,
            "PRINTMAXX WEEKLY PORTFOLIO REBALANCE REPORT",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 80,
            "",
            "EXECUTIVE SUMMARY",
            "-" * 40,
            f"Total Methods Tracked: {len(self.methods)}",
            f"Active Methods: {sum(1 for m in self.methods.values() if m.status in ['Active', 'ACTIVE', 'active'])}",
            f"Total Revenue (90d): ${self.total_revenue:,.2f}",
            f"Recommendations Generated: {len(self.recommendations)}",
            "",
            "CRITICAL ALERTS",
            "-" * 40,
        ]

        critical_alerts = [a for a in self.alerts if 'CRITICAL' in a or 'KILL' in a or 'REDUCE' in a]
        if critical_alerts:
            for alert in critical_alerts:
                report_lines.append(f"  ! {alert}")
        else:
            report_lines.append("  No critical alerts")

        report_lines.extend([
            "",
            "REBALANCING RECOMMENDATIONS BY PRIORITY",
            "-" * 40,
        ])

        # Group by priority
        for priority in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            priority_recs = [r for r in self.recommendations if r.priority == priority]
            if priority_recs:
                report_lines.append(f"\n[{priority}]")
                for rec in priority_recs:
                    report_lines.append(
                        f"  {rec.action}: {rec.method_name}"
                    )
                    report_lines.append(f"    Reason: {rec.reason}")
                    report_lines.append(
                        f"    Allocation: {rec.current_allocation:.1%} -> {rec.recommended_allocation:.1%} "
                        f"(Confidence: {rec.confidence:.0%})"
                    )

        report_lines.extend([
            "",
            "CONCENTRATION ANALYSIS",
            "-" * 40,
        ])

        concentration = self.analyze_concentration_risk()
        if concentration['status'] == 'pre_revenue':
            report_lines.append("  Pre-revenue stage - no concentration data")
        else:
            report_lines.append("  Method Concentration:")
            for method_id, conc in sorted(concentration['methods'].items(),
                                          key=lambda x: x[1], reverse=True)[:10]:
                method = self.methods.get(method_id)
                name = method.method_name if method else method_id
                flag = " [OVER LIMIT]" if conc > MAX_METHOD_CONCENTRATION else ""
                report_lines.append(f"    {name}: {conc:.1%}{flag}")

            report_lines.append("\n  Platform Concentration:")
            for platform, conc in sorted(concentration['platforms'].items(),
                                         key=lambda x: x[1], reverse=True):
                flag = " [OVER LIMIT]" if conc > MAX_PLATFORM_CONCENTRATION else ""
                report_lines.append(f"    {platform}: {conc:.1%}{flag}")

        report_lines.extend([
            "",
            "RISK LIMITS STATUS",
            "-" * 40,
            f"  Max Method Concentration: {MAX_METHOD_CONCENTRATION:.0%}",
            f"  Max Platform Concentration: {MAX_PLATFORM_CONCENTRATION:.0%}",
            f"  Min Active Methods: {MIN_ACTIVE_METHODS}",
            f"  Kill Threshold: <${KILL_THRESHOLD_REVENUE_PER_HOUR}/hr for 30+ days",
            f"  Scale Threshold: >${SCALE_THRESHOLD_REVENUE_PER_HOUR}/hr AND Sharpe >{SCALE_SHARPE_THRESHOLD}",
            "",
            "SCALABLE ALPHA (Not Yet Deployed)",
            "-" * 40,
        ])

        if hasattr(self, 'scalable_alpha') and self.scalable_alpha:
            for alpha in sorted(self.scalable_alpha, key=lambda x: x['score'], reverse=True)[:10]:
                report_lines.append(
                    f"  {alpha['alpha_id']}: Score {alpha['score']} - {alpha['category']} ({alpha['source'][:30]})"
                )
        else:
            report_lines.append("  No scalable alpha found (score >= 70)")

        report_lines.extend([
            "",
            "=" * 80,
            "END OF REPORT",
            "=" * 80,
        ])

        report = "\n".join(report_lines)

        # Save report
        if not self.simulate:
            WEEKLY_REPORT_DIR.mkdir(parents=True, exist_ok=True)
            report_file = WEEKLY_REPORT_DIR / f"REBALANCE_REPORT_{datetime.now().strftime('%Y%m%d')}.md"
            with open(report_file, 'w') as f:
                f.write(report)
            print(f"[INFO] Saved weekly report to {report_file}")

        return report

    def print_alerts(self) -> None:
        """Print alerts to console"""
        if not self.alerts:
            print("\n[INFO] No alerts to report")
            return

        print("\n" + "=" * 60)
        print("PORTFOLIO REBALANCER ALERTS")
        print("=" * 60)

        for alert in self.alerts:
            if 'KILL' in alert or 'CRITICAL' in alert:
                print(f"  \033[91m! {alert}\033[0m")  # Red
            elif 'SCALE' in alert:
                print(f"  \033[92m+ {alert}\033[0m")  # Green
            elif 'REDUCE' in alert or 'RISK' in alert:
                print(f"  \033[93m* {alert}\033[0m")  # Yellow
            else:
                print(f"  - {alert}")

        print("=" * 60)

    def run(self, weekly_report: bool = False, alerts_only: bool = False) -> None:
        """Run full rebalancing analysis"""
        print("\n[PRINTMAXX Portfolio Rebalancer]")
        print("-" * 40)

        # Load data
        print("[1/6] Loading methods...")
        self.load_methods()

        print("[2/6] Loading revenue data...")
        self.load_revenue_data()

        print("[3/6] Loading paper trade data...")
        self.load_paper_trade_data()

        print("[4/6] Loading backtest data...")
        self.load_backtest_data()

        # Generate recommendations
        print("[5/6] Generating recommendations...")
        self.generate_kill_recommendations()
        self.generate_scale_recommendations()
        self.generate_reduce_recommendations()
        self.generate_add_recommendations()
        self.generate_hold_recommendations()

        # Sort by priority
        priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        self.recommendations.sort(key=lambda r: (priority_order.get(r.priority, 99), r.action))

        # Output
        print("[6/6] Generating output...")

        if alerts_only:
            self.print_alerts()
            return

        self.save_recommendations()

        if weekly_report:
            report = self.generate_weekly_report()
            print("\n" + report)
        else:
            self.print_alerts()

            # Print summary
            print("\nRECOMMENDATION SUMMARY")
            print("-" * 40)
            action_counts = defaultdict(int)
            for rec in self.recommendations:
                action_counts[rec.action] += 1
            for action, count in sorted(action_counts.items()):
                print(f"  {action}: {count}")

            print(f"\nOutput: {REBALANCE_RECOMMENDATIONS_FILE}")


def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Portfolio Rebalancer - Automated rebalancing recommendations"
    )
    parser.add_argument(
        '--weekly-report', action='store_true',
        help='Generate full weekly rebalance report'
    )
    parser.add_argument(
        '--simulate', action='store_true',
        help='Dry run - no file writes'
    )
    parser.add_argument(
        '--alerts-only', action='store_true',
        help='Only show critical alerts'
    )

    args = parser.parse_args()

    rebalancer = PortfolioRebalancer(simulate=args.simulate)
    rebalancer.run(
        weekly_report=args.weekly_report,
        alerts_only=args.alerts_only
    )


if __name__ == "__main__":
    main()
