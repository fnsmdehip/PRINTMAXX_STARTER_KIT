#!/usr/bin/env python3
"""
Institutional-Grade Paper Trading System
=========================================
Test solopreneurship methods with real statistical rigor before deploying capital.

Statistical Framework:
- Minimum 10 data points before SCALE/KILL decision
- 80% confidence interval requirement for revenue estimates
- Kelly Criterion position sizing for capital allocation
- Risk-adjusted returns (Sharpe-like ratio for revenue volatility)
- Drawdown tracking and maximum acceptable drawdown limits
- Automatic alerts when metrics deviate >2 sigma from projections

Decision Matrix:
- SCALE: Revenue/hour >= $20 AND confidence > 80% AND min_observations >= 10
- ITERATE: Close to threshold OR high variance (need more data)
- KILL: Revenue/hour < $15 with 80% confidence after 10+ observations

Integration:
- Reads from LEDGER/BACKTESTS/BACKTEST_RESULTS.csv for initial expectations
- Writes to FINANCIALS/REVENUE_TRACKER.csv for financial integration
- Outputs to LEDGER/PAPER_TRADES/ for screening system feedback

Usage:
    python3 paper_trade.py --method MM001_APP_FACTORY --alpha ALPHA524 --budget 100 --days 14
    python3 paper_trade.py --record PAPER_TRADE_001 --revenue 45 --hours 2 --leads 3
    python3 paper_trade.py --analyze PAPER_TRADE_001
    python3 paper_trade.py --complete PAPER_TRADE_001
    python3 paper_trade.py --list
    python3 paper_trade.py --alerts
"""

import csv
import json
import math
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field
from collections import defaultdict
import statistics

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_DIR / "LEDGER"
FINANCIALS_DIR = PROJECT_DIR / "FINANCIALS"
PAPER_TRADE_DIR = LEDGER_DIR / "PAPER_TRADES"
BACKTEST_DIR = LEDGER_DIR / "BACKTESTS"

# Ensure directories exist
PAPER_TRADE_DIR.mkdir(exist_ok=True)
FINANCIALS_DIR.mkdir(exist_ok=True)

# Statistical Constants
MIN_OBSERVATIONS = 10  # Minimum data points before decision
CONFIDENCE_THRESHOLD = 0.80  # 80% confidence required
SCALE_REVENUE_THRESHOLD = 20.0  # $/hour minimum to scale
KILL_REVENUE_THRESHOLD = 15.0  # $/hour below which we kill
MAX_DRAWDOWN_PERCENT = 50.0  # Maximum acceptable drawdown
ALERT_SIGMA_THRESHOLD = 2.0  # Alert when deviation > 2 sigma


@dataclass
class DataPoint:
    """Single observation in paper trade"""
    timestamp: str
    revenue: float
    hours: float
    leads: int
    conversion_rate: float
    notes: str = ""

    def revenue_per_hour(self) -> float:
        if self.hours > 0:
            return self.revenue / self.hours
        return 0.0


@dataclass
class StatisticalSummary:
    """Statistical summary of paper trade performance"""
    n_observations: int
    mean_revenue_per_hour: float
    std_revenue_per_hour: float
    confidence_interval_lower: float
    confidence_interval_upper: float
    confidence_level: float
    variance: float
    sharpe_ratio: float  # Risk-adjusted return
    max_drawdown_percent: float
    current_drawdown_percent: float
    total_revenue: float
    total_hours: float
    total_leads: int
    avg_conversion_rate: float

    def has_sufficient_data(self) -> bool:
        return self.n_observations >= MIN_OBSERVATIONS

    def passes_confidence_threshold(self) -> bool:
        """Check if lower bound of CI is above threshold"""
        return self.confidence_interval_lower >= SCALE_REVENUE_THRESHOLD

    def should_scale(self) -> bool:
        """SCALE decision: sufficient data + confidence + threshold met"""
        return (
            self.has_sufficient_data() and
            self.confidence_level >= CONFIDENCE_THRESHOLD and
            self.passes_confidence_threshold() and
            self.max_drawdown_percent <= MAX_DRAWDOWN_PERCENT
        )

    def should_kill(self) -> bool:
        """KILL decision: sufficient data + clearly below threshold"""
        return (
            self.has_sufficient_data() and
            self.confidence_interval_upper < KILL_REVENUE_THRESHOLD
        )


@dataclass
class PaperTrade:
    """Paper trade experiment with full tracking"""
    trade_id: str
    method_id: str
    alpha_id: str
    budget: float
    duration_days: int
    start_date: str
    end_date: str
    status: str  # RUNNING, COMPLETE, KILLED, SCALED
    expected_revenue_per_hour: float  # From backtest
    scalability_score: int  # 1-10
    platform_risk: int  # 1-10
    data_points: List[DataPoint] = field(default_factory=list)
    decision: str = "PENDING"
    decision_confidence: float = 0.0
    kelly_fraction: float = 0.0
    recommended_position_size: float = 0.0
    alerts: List[str] = field(default_factory=list)
    notes: str = ""


class StatisticalEngine:
    """Statistical calculations for paper trading"""

    @staticmethod
    def calculate_confidence_interval(
        data: List[float],
        confidence: float = 0.95
    ) -> Tuple[float, float, float]:
        """
        Calculate confidence interval using t-distribution
        Returns: (lower_bound, upper_bound, achieved_confidence)
        """
        n = len(data)
        if n < 2:
            return (0.0, 0.0, 0.0)

        mean = statistics.mean(data)
        std = statistics.stdev(data)

        # t-value approximation for common confidence levels
        # Using approximation: t ≈ 1.96 for 95%, 1.28 for 80%, 2.58 for 99%
        if confidence >= 0.99:
            t_value = 2.58
        elif confidence >= 0.95:
            t_value = 1.96
        elif confidence >= 0.90:
            t_value = 1.645
        else:
            t_value = 1.28  # 80%

        # Adjust for sample size (t increases as n decreases)
        if n < 30:
            # Simple adjustment for small samples
            t_value *= (1 + 10/n)

        margin = t_value * (std / math.sqrt(n))

        lower = mean - margin
        upper = mean + margin

        # Calculate achieved confidence based on data quality
        achieved = min(confidence, n / MIN_OBSERVATIONS)

        return (lower, upper, achieved)

    @staticmethod
    def calculate_sharpe_ratio(
        returns: List[float],
        risk_free_rate: float = 0.0
    ) -> float:
        """
        Sharpe-like ratio for revenue volatility
        Higher = better risk-adjusted returns
        """
        if len(returns) < 2:
            return 0.0

        mean_return = statistics.mean(returns)
        std_return = statistics.stdev(returns)

        if std_return == 0:
            return 10.0 if mean_return > 0 else 0.0

        return (mean_return - risk_free_rate) / std_return

    @staticmethod
    def calculate_max_drawdown(cumulative_revenue: List[float]) -> float:
        """Calculate maximum drawdown percentage"""
        if len(cumulative_revenue) < 2:
            return 0.0

        peak = cumulative_revenue[0]
        max_dd = 0.0

        for value in cumulative_revenue:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak * 100 if peak > 0 else 0
            max_dd = max(max_dd, drawdown)

        return max_dd

    @staticmethod
    def calculate_kelly_fraction(
        win_rate: float,
        avg_win: float,
        avg_loss: float
    ) -> float:
        """
        Kelly Criterion for position sizing
        f* = (p * b - q) / b
        where p = win prob, q = loss prob, b = win/loss ratio
        """
        if avg_loss == 0 or win_rate <= 0 or win_rate >= 1:
            return 0.0

        b = avg_win / abs(avg_loss) if avg_loss != 0 else 0
        if b == 0:
            return 0.0

        q = 1 - win_rate
        kelly = (win_rate * b - q) / b

        # Cap at 25% (half-Kelly is more conservative)
        return max(0, min(kelly * 0.5, 0.25))


class PaperTradeManager:
    """Manage institutional-grade paper trading"""

    def __init__(self):
        self.trades_file = PAPER_TRADE_DIR / "PAPER_TRADES.json"
        self.results_csv = PAPER_TRADE_DIR / "PAPER_TRADE_RESULTS.csv"
        self.datapoints_csv = PAPER_TRADE_DIR / "PAPER_TRADE_DATAPOINTS.csv"
        self.revenue_tracker = FINANCIALS_DIR / "REVENUE_TRACKER.csv"
        self.backtest_file = BACKTEST_DIR / "BACKTEST_RESULTS.csv"
        self.stats = StatisticalEngine()

    def start_paper_trade(
        self,
        method_id: str,
        alpha_id: str,
        budget: float,
        duration_days: int,
        scalability: int = 5,
        platform_risk: int = 5,
        notes: str = ""
    ) -> str:
        """Start a new paper trade with expected values from backtest"""

        # Load expected revenue from backtest if available
        expected_rph = self._get_expected_revenue_per_hour(alpha_id, method_id)

        # Generate trade ID
        trade_id = self._generate_trade_id()

        # Calculate dates
        start_date = datetime.now().isoformat()
        end_date = (datetime.now() + timedelta(days=duration_days)).isoformat()

        trade = PaperTrade(
            trade_id=trade_id,
            method_id=method_id,
            alpha_id=alpha_id,
            budget=budget,
            duration_days=duration_days,
            start_date=start_date,
            end_date=end_date,
            status="RUNNING",
            expected_revenue_per_hour=expected_rph,
            scalability_score=scalability,
            platform_risk=platform_risk,
            data_points=[],
            notes=notes
        )

        self._save_trade(trade)

        print(f"\n=== Paper Trade Started ===")
        print(f"Trade ID: {trade_id}")
        print(f"Method: {method_id}")
        print(f"Alpha: {alpha_id}")
        print(f"Budget: ${budget}")
        print(f"Duration: {duration_days} days (ends {end_date[:10]})")
        print(f"Expected Revenue/Hour: ${expected_rph:.2f}")
        print(f"\nNext Steps:")
        print(f"  1. Record each work session with revenue/hours/leads")
        print(f"  2. Run: python3 paper_trade.py --record {trade_id} --revenue X --hours Y --leads Z")
        print(f"  3. Minimum {MIN_OBSERVATIONS} observations required before SCALE/KILL decision")

        return trade_id

    def record_data_point(
        self,
        trade_id: str,
        revenue: float,
        hours: float,
        leads: int = 0,
        conversion_rate: float = 0.0,
        notes: str = ""
    ) -> Optional[StatisticalSummary]:
        """Record a single observation and return updated statistics"""

        trade = self._load_trade(trade_id)
        if not trade:
            print(f"Error: Trade {trade_id} not found")
            return None

        if trade.status != "RUNNING":
            print(f"Error: Trade {trade_id} is {trade.status}, not RUNNING")
            return None

        # Create data point
        dp = DataPoint(
            timestamp=datetime.now().isoformat(),
            revenue=revenue,
            hours=hours,
            leads=leads,
            conversion_rate=conversion_rate,
            notes=notes
        )

        trade.data_points.append(dp)

        # Calculate statistics
        summary = self._calculate_summary(trade)

        # Check for alerts
        alerts = self._check_alerts(trade, summary)
        trade.alerts.extend(alerts)

        # Save trade and data point
        self._save_trade(trade)
        self._append_datapoint_csv(trade_id, dp)

        # Print summary
        print(f"\n=== Data Point Recorded ===")
        print(f"Trade: {trade_id}")
        print(f"Observation #{len(trade.data_points)}")
        print(f"Revenue: ${revenue:.2f} | Hours: {hours:.1f} | Revenue/Hour: ${dp.revenue_per_hour():.2f}")
        print(f"\n--- Running Statistics ---")
        print(f"Observations: {summary.n_observations}/{MIN_OBSERVATIONS} minimum")
        print(f"Mean Revenue/Hour: ${summary.mean_revenue_per_hour:.2f}")
        print(f"Std Dev: ${summary.std_revenue_per_hour:.2f}")
        print(f"80% CI: [${summary.confidence_interval_lower:.2f}, ${summary.confidence_interval_upper:.2f}]")
        print(f"Sharpe Ratio: {summary.sharpe_ratio:.2f}")
        print(f"Max Drawdown: {summary.max_drawdown_percent:.1f}%")

        if alerts:
            print(f"\n⚠️  ALERTS:")
            for alert in alerts:
                print(f"  - {alert}")

        # Decision preview
        if summary.has_sufficient_data():
            print(f"\n--- Decision Preview ---")
            if summary.should_scale():
                print(f"SCALE: Revenue/hour CI lower bound (${summary.confidence_interval_lower:.2f}) >= ${SCALE_REVENUE_THRESHOLD}")
            elif summary.should_kill():
                print(f"KILL: Revenue/hour CI upper bound (${summary.confidence_interval_upper:.2f}) < ${KILL_REVENUE_THRESHOLD}")
            else:
                print(f"ITERATE: More data or adjustments needed")
        else:
            remaining = MIN_OBSERVATIONS - summary.n_observations
            print(f"\n{remaining} more observations needed before SCALE/KILL decision")

        return summary

    def analyze_trade(self, trade_id: str) -> Optional[Dict]:
        """Full statistical analysis of paper trade"""

        trade = self._load_trade(trade_id)
        if not trade:
            print(f"Error: Trade {trade_id} not found")
            return None

        summary = self._calculate_summary(trade)

        # Calculate Kelly and position sizing
        kelly = self._calculate_kelly_for_trade(trade)
        recommended_size = kelly * trade.budget * 10  # Scale up budget

        analysis = {
            "trade_id": trade_id,
            "method_id": trade.method_id,
            "alpha_id": trade.alpha_id,
            "status": trade.status,
            "days_elapsed": self._days_elapsed(trade),
            "days_remaining": self._days_remaining(trade),
            "statistics": {
                "n_observations": summary.n_observations,
                "mean_revenue_per_hour": summary.mean_revenue_per_hour,
                "std_revenue_per_hour": summary.std_revenue_per_hour,
                "variance": summary.variance,
                "confidence_interval": {
                    "lower": summary.confidence_interval_lower,
                    "upper": summary.confidence_interval_upper,
                    "level": summary.confidence_level
                },
                "sharpe_ratio": summary.sharpe_ratio,
                "max_drawdown_percent": summary.max_drawdown_percent,
                "current_drawdown_percent": summary.current_drawdown_percent,
            },
            "totals": {
                "revenue": summary.total_revenue,
                "hours": summary.total_hours,
                "leads": summary.total_leads,
                "conversion_rate": summary.avg_conversion_rate
            },
            "kelly_fraction": kelly,
            "recommended_position_size": recommended_size,
            "decision_ready": summary.has_sufficient_data(),
            "projected_decision": self._get_projected_decision(summary),
            "alerts": trade.alerts[-5:] if trade.alerts else [],
            "expected_vs_actual": {
                "expected_rph": trade.expected_revenue_per_hour,
                "actual_rph": summary.mean_revenue_per_hour,
                "deviation_percent": self._calculate_deviation(
                    trade.expected_revenue_per_hour,
                    summary.mean_revenue_per_hour
                )
            }
        }

        # Print analysis
        print(f"\n{'='*60}")
        print(f"PAPER TRADE ANALYSIS: {trade_id}")
        print(f"{'='*60}")
        print(f"\nMethod: {trade.method_id} | Alpha: {trade.alpha_id}")
        print(f"Status: {trade.status} | Days: {analysis['days_elapsed']}/{trade.duration_days}")

        print(f"\n--- Statistical Summary ({summary.n_observations} observations) ---")
        print(f"Mean Revenue/Hour:  ${summary.mean_revenue_per_hour:.2f}")
        print(f"Std Deviation:      ${summary.std_revenue_per_hour:.2f}")
        print(f"80% CI:             [${summary.confidence_interval_lower:.2f}, ${summary.confidence_interval_upper:.2f}]")
        print(f"Sharpe Ratio:       {summary.sharpe_ratio:.2f}")
        print(f"Max Drawdown:       {summary.max_drawdown_percent:.1f}%")

        print(f"\n--- Totals ---")
        print(f"Total Revenue:  ${summary.total_revenue:.2f}")
        print(f"Total Hours:    {summary.total_hours:.1f}")
        print(f"Total Leads:    {summary.total_leads}")

        print(f"\n--- Position Sizing (Kelly Criterion) ---")
        print(f"Kelly Fraction: {kelly:.1%}")
        print(f"Recommended Position: ${recommended_size:.2f}")

        print(f"\n--- Expected vs Actual ---")
        print(f"Expected R/H: ${trade.expected_revenue_per_hour:.2f}")
        print(f"Actual R/H:   ${summary.mean_revenue_per_hour:.2f}")
        print(f"Deviation:    {analysis['expected_vs_actual']['deviation_percent']:.1f}%")

        print(f"\n--- Decision Status ---")
        if summary.has_sufficient_data():
            print(f"READY for decision: {analysis['projected_decision']}")
        else:
            remaining = MIN_OBSERVATIONS - summary.n_observations
            print(f"NOT READY: Need {remaining} more observations")

        if trade.alerts:
            print(f"\n⚠️  Recent Alerts:")
            for alert in trade.alerts[-5:]:
                print(f"  - {alert}")

        return analysis

    def complete_trade(self, trade_id: str, force: bool = False) -> Optional[Dict]:
        """Complete paper trade and make final decision"""

        trade = self._load_trade(trade_id)
        if not trade:
            print(f"Error: Trade {trade_id} not found")
            return None

        summary = self._calculate_summary(trade)

        # Check minimum observations
        if not summary.has_sufficient_data() and not force:
            print(f"\nError: Only {summary.n_observations}/{MIN_OBSERVATIONS} observations.")
            print(f"Use --force to complete anyway (not recommended)")
            return None

        # Make decision
        if summary.should_scale():
            decision = "SCALE"
            trade.status = "SCALED"
        elif summary.should_kill():
            decision = "KILL"
            trade.status = "KILLED"
        else:
            decision = "ITERATE"
            trade.status = "COMPLETE"

        trade.decision = decision
        trade.decision_confidence = summary.confidence_level
        trade.kelly_fraction = self._calculate_kelly_for_trade(trade)
        trade.recommended_position_size = trade.kelly_fraction * trade.budget * 10

        # Save final state
        self._save_trade(trade)
        self._save_results_csv(trade, summary)

        # Write to revenue tracker if profitable
        if summary.total_revenue > 0:
            self._write_to_revenue_tracker(trade, summary)

        # Print decision
        print(f"\n{'='*60}")
        print(f"PAPER TRADE COMPLETE: {trade_id}")
        print(f"{'='*60}")
        print(f"\n🎯 DECISION: {decision}")
        print(f"Confidence: {summary.confidence_level:.0%}")

        if decision == "SCALE":
            print(f"\n✅ SCALE CRITERIA MET:")
            print(f"   - Mean R/H: ${summary.mean_revenue_per_hour:.2f} >= ${SCALE_REVENUE_THRESHOLD}")
            print(f"   - CI Lower: ${summary.confidence_interval_lower:.2f} >= ${SCALE_REVENUE_THRESHOLD}")
            print(f"   - Max DD: {summary.max_drawdown_percent:.1f}% <= {MAX_DRAWDOWN_PERCENT}%")
            print(f"\n📈 RECOMMENDED ACTION:")
            print(f"   - Increase position to ${trade.recommended_position_size:.2f}")
            print(f"   - Kelly fraction: {trade.kelly_fraction:.1%}")

        elif decision == "KILL":
            print(f"\n❌ KILL CRITERIA MET:")
            print(f"   - CI Upper: ${summary.confidence_interval_upper:.2f} < ${KILL_REVENUE_THRESHOLD}")
            print(f"\n📉 RECOMMENDED ACTION:")
            print(f"   - Discontinue this method")
            print(f"   - Reallocate capital to higher-performing methods")

        else:
            print(f"\n🔄 ITERATE:")
            print(f"   - Not confident enough to SCALE or KILL")
            print(f"   - Consider: More observations, different approach, or different method")

        print(f"\n--- Final Statistics ---")
        print(f"Observations: {summary.n_observations}")
        print(f"Total Revenue: ${summary.total_revenue:.2f}")
        print(f"Total Hours: {summary.total_hours:.1f}")
        print(f"Revenue/Hour: ${summary.mean_revenue_per_hour:.2f} ± ${summary.std_revenue_per_hour:.2f}")
        print(f"Sharpe: {summary.sharpe_ratio:.2f}")

        return {
            "trade_id": trade_id,
            "decision": decision,
            "confidence": summary.confidence_level,
            "summary": asdict(summary) if hasattr(summary, '__dict__') else str(summary),
            "recommended_position": trade.recommended_position_size
        }

    def list_trades(self, status_filter: str = None) -> List[Dict]:
        """List all paper trades with summary stats"""

        trades = self._load_all_trades()

        if status_filter:
            trades = [t for t in trades if t.status == status_filter.upper()]

        print(f"\n{'='*80}")
        print(f"PAPER TRADES")
        print(f"{'='*80}")

        for trade in trades:
            summary = self._calculate_summary(trade)
            days_left = self._days_remaining(trade)

            status_emoji = {
                "RUNNING": "🔄",
                "COMPLETE": "✅",
                "SCALED": "📈",
                "KILLED": "❌"
            }.get(trade.status, "❓")

            print(f"\n{status_emoji} {trade.trade_id}")
            print(f"   Method: {trade.method_id} | Alpha: {trade.alpha_id}")
            print(f"   Status: {trade.status} | Days Left: {max(0, days_left)}")
            print(f"   Observations: {summary.n_observations}/{MIN_OBSERVATIONS}")
            print(f"   R/H: ${summary.mean_revenue_per_hour:.2f} ± ${summary.std_revenue_per_hour:.2f}")
            print(f"   Total: ${summary.total_revenue:.2f} revenue, {summary.total_hours:.1f}h")

            if trade.decision != "PENDING":
                print(f"   Decision: {trade.decision} ({trade.decision_confidence:.0%} confidence)")

        return [asdict(t) if hasattr(t, '__dict__') else t for t in trades]

    def check_alerts(self) -> List[Dict]:
        """Check all running trades for alerts"""

        trades = self._load_all_trades()
        running = [t for t in trades if t.status == "RUNNING"]

        all_alerts = []

        print(f"\n{'='*60}")
        print(f"ALERT CHECK")
        print(f"{'='*60}")

        for trade in running:
            summary = self._calculate_summary(trade)
            alerts = self._check_alerts(trade, summary)

            if alerts:
                trade.alerts.extend(alerts)
                self._save_trade(trade)

                print(f"\n⚠️  {trade.trade_id}:")
                for alert in alerts:
                    print(f"   - {alert}")
                    all_alerts.append({
                        "trade_id": trade.trade_id,
                        "alert": alert,
                        "timestamp": datetime.now().isoformat()
                    })

        if not all_alerts:
            print(f"\n✅ No alerts. All {len(running)} running trades within expected parameters.")

        return all_alerts

    # ========== Private Methods ==========

    def _calculate_summary(self, trade: PaperTrade) -> StatisticalSummary:
        """Calculate full statistical summary from data points"""

        dps = trade.data_points
        n = len(dps)

        if n == 0:
            return StatisticalSummary(
                n_observations=0,
                mean_revenue_per_hour=0,
                std_revenue_per_hour=0,
                confidence_interval_lower=0,
                confidence_interval_upper=0,
                confidence_level=0,
                variance=0,
                sharpe_ratio=0,
                max_drawdown_percent=0,
                current_drawdown_percent=0,
                total_revenue=0,
                total_hours=0,
                total_leads=0,
                avg_conversion_rate=0
            )

        # Calculate revenue per hour for each observation
        rph_values = [dp.revenue_per_hour() for dp in dps]

        # Basic stats
        mean_rph = statistics.mean(rph_values) if rph_values else 0
        std_rph = statistics.stdev(rph_values) if n > 1 else 0
        variance = statistics.variance(rph_values) if n > 1 else 0

        # Confidence interval
        ci_lower, ci_upper, confidence = self.stats.calculate_confidence_interval(
            rph_values, confidence=CONFIDENCE_THRESHOLD
        )

        # Sharpe ratio
        sharpe = self.stats.calculate_sharpe_ratio(rph_values)

        # Drawdown
        cumulative = []
        running_total = 0
        for dp in dps:
            running_total += dp.revenue
            cumulative.append(running_total)

        max_dd = self.stats.calculate_max_drawdown(cumulative)

        # Current drawdown
        peak = max(cumulative) if cumulative else 0
        current = cumulative[-1] if cumulative else 0
        current_dd = (peak - current) / peak * 100 if peak > 0 else 0

        # Totals
        total_revenue = sum(dp.revenue for dp in dps)
        total_hours = sum(dp.hours for dp in dps)
        total_leads = sum(dp.leads for dp in dps)

        conv_rates = [dp.conversion_rate for dp in dps if dp.conversion_rate > 0]
        avg_conv = statistics.mean(conv_rates) if conv_rates else 0

        return StatisticalSummary(
            n_observations=n,
            mean_revenue_per_hour=mean_rph,
            std_revenue_per_hour=std_rph,
            confidence_interval_lower=ci_lower,
            confidence_interval_upper=ci_upper,
            confidence_level=confidence,
            variance=variance,
            sharpe_ratio=sharpe,
            max_drawdown_percent=max_dd,
            current_drawdown_percent=current_dd,
            total_revenue=total_revenue,
            total_hours=total_hours,
            total_leads=total_leads,
            avg_conversion_rate=avg_conv
        )

    def _check_alerts(self, trade: PaperTrade, summary: StatisticalSummary) -> List[str]:
        """Generate alerts for significant deviations"""

        alerts = []

        if summary.n_observations < 2:
            return alerts

        # Check deviation from expected
        if trade.expected_revenue_per_hour > 0:
            deviation = abs(summary.mean_revenue_per_hour - trade.expected_revenue_per_hour)
            if summary.std_revenue_per_hour > 0:
                sigma = deviation / summary.std_revenue_per_hour
                if sigma > ALERT_SIGMA_THRESHOLD:
                    direction = "above" if summary.mean_revenue_per_hour > trade.expected_revenue_per_hour else "below"
                    alerts.append(
                        f"Revenue/hour {sigma:.1f}σ {direction} expected "
                        f"(${summary.mean_revenue_per_hour:.2f} vs ${trade.expected_revenue_per_hour:.2f})"
                    )

        # Check drawdown
        if summary.max_drawdown_percent > MAX_DRAWDOWN_PERCENT * 0.8:
            alerts.append(
                f"Approaching max drawdown threshold: {summary.max_drawdown_percent:.1f}% "
                f"(max: {MAX_DRAWDOWN_PERCENT}%)"
            )

        # Check variance explosion
        if summary.n_observations >= 5 and summary.std_revenue_per_hour > summary.mean_revenue_per_hour:
            alerts.append(
                f"High variance warning: σ (${summary.std_revenue_per_hour:.2f}) > mean (${summary.mean_revenue_per_hour:.2f})"
            )

        # Check time running out
        days_left = self._days_remaining(trade)
        if days_left <= 2 and summary.n_observations < MIN_OBSERVATIONS:
            needed = MIN_OBSERVATIONS - summary.n_observations
            alerts.append(
                f"Time warning: {days_left} days left, need {needed} more observations"
            )

        return alerts

    def _calculate_kelly_for_trade(self, trade: PaperTrade) -> float:
        """Calculate Kelly fraction based on trade performance"""

        dps = trade.data_points
        if len(dps) < 3:
            return 0.05  # Conservative default

        # Calculate win rate (sessions with positive ROI)
        profitable = [dp for dp in dps if dp.revenue > 0]
        win_rate = len(profitable) / len(dps)

        # Calculate average win and loss
        profits = [dp.revenue for dp in dps if dp.revenue > 0]
        losses = [dp.revenue for dp in dps if dp.revenue <= 0]

        avg_win = statistics.mean(profits) if profits else 0
        avg_loss = statistics.mean(losses) if losses else -1

        kelly = self.stats.calculate_kelly_fraction(win_rate, avg_win, avg_loss)

        return kelly

    def _get_projected_decision(self, summary: StatisticalSummary) -> str:
        """Get projected decision based on current stats"""

        if summary.should_scale():
            return "SCALE"
        elif summary.should_kill():
            return "KILL"
        else:
            return "ITERATE"

    def _get_expected_revenue_per_hour(self, alpha_id: str, method_id: str) -> float:
        """Load expected revenue/hour from backtest results"""

        if not self.backtest_file.exists():
            return 0.0

        try:
            with open(self.backtest_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('alpha_id') == alpha_id:
                        # Use backtest score as proxy for expected quality
                        score = int(row.get('backtest_score', 0))
                        # Higher score = higher expected revenue
                        return score * 0.5  # Simple heuristic: score of 70 = $35/hr expected
        except Exception as e:
            print(f"Warning: Could not load backtest for {alpha_id}: {e}")

        return 20.0  # Default expectation

    def _calculate_deviation(self, expected: float, actual: float) -> float:
        """Calculate percent deviation from expected"""
        if expected == 0:
            return 0.0
        return ((actual - expected) / expected) * 100

    def _days_elapsed(self, trade: PaperTrade) -> int:
        """Calculate days elapsed since trade start"""
        start = datetime.fromisoformat(trade.start_date)
        return (datetime.now() - start).days

    def _days_remaining(self, trade: PaperTrade) -> int:
        """Calculate days remaining in trade"""
        end = datetime.fromisoformat(trade.end_date)
        return (end - datetime.now()).days

    def _generate_trade_id(self) -> str:
        """Generate unique trade ID"""
        trades = self._load_all_trades()
        return f"PAPER_TRADE_{len(trades) + 1:03d}"

    def _save_trade(self, trade: PaperTrade) -> None:
        """Save trade to JSON file"""
        trades = self._load_all_trades()

        # Update or add trade
        found = False
        for i, t in enumerate(trades):
            if t.trade_id == trade.trade_id:
                trades[i] = trade
                found = True
                break

        if not found:
            trades.append(trade)

        # Convert to serializable format
        data = []
        for t in trades:
            td = {
                "trade_id": t.trade_id,
                "method_id": t.method_id,
                "alpha_id": t.alpha_id,
                "budget": t.budget,
                "duration_days": t.duration_days,
                "start_date": t.start_date,
                "end_date": t.end_date,
                "status": t.status,
                "expected_revenue_per_hour": t.expected_revenue_per_hour,
                "scalability_score": t.scalability_score,
                "platform_risk": t.platform_risk,
                "decision": t.decision,
                "decision_confidence": t.decision_confidence,
                "kelly_fraction": t.kelly_fraction,
                "recommended_position_size": t.recommended_position_size,
                "alerts": t.alerts,
                "notes": t.notes,
                "data_points": [
                    {
                        "timestamp": dp.timestamp,
                        "revenue": dp.revenue,
                        "hours": dp.hours,
                        "leads": dp.leads,
                        "conversion_rate": dp.conversion_rate,
                        "notes": dp.notes
                    }
                    for dp in t.data_points
                ]
            }
            data.append(td)

        with open(self.trades_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_trade(self, trade_id: str) -> Optional[PaperTrade]:
        """Load a single trade by ID"""
        trades = self._load_all_trades()
        for t in trades:
            if t.trade_id == trade_id:
                return t
        return None

    def _load_all_trades(self) -> List[PaperTrade]:
        """Load all trades from JSON"""
        if not self.trades_file.exists():
            return []

        try:
            with open(self.trades_file, 'r') as f:
                data = json.load(f)

            trades = []
            for td in data:
                data_points = [
                    DataPoint(
                        timestamp=dp["timestamp"],
                        revenue=dp["revenue"],
                        hours=dp["hours"],
                        leads=dp.get("leads", 0),
                        conversion_rate=dp.get("conversion_rate", 0),
                        notes=dp.get("notes", "")
                    )
                    for dp in td.get("data_points", [])
                ]

                trade = PaperTrade(
                    trade_id=td["trade_id"],
                    method_id=td["method_id"],
                    alpha_id=td["alpha_id"],
                    budget=td["budget"],
                    duration_days=td["duration_days"],
                    start_date=td["start_date"],
                    end_date=td["end_date"],
                    status=td["status"],
                    expected_revenue_per_hour=td.get("expected_revenue_per_hour", 0),
                    scalability_score=td.get("scalability_score", 5),
                    platform_risk=td.get("platform_risk", 5),
                    data_points=data_points,
                    decision=td.get("decision", "PENDING"),
                    decision_confidence=td.get("decision_confidence", 0),
                    kelly_fraction=td.get("kelly_fraction", 0),
                    recommended_position_size=td.get("recommended_position_size", 0),
                    alerts=td.get("alerts", []),
                    notes=td.get("notes", "")
                )
                trades.append(trade)

            return trades

        except Exception as e:
            print(f"Error loading trades: {e}")
            return []

    def _append_datapoint_csv(self, trade_id: str, dp: DataPoint) -> None:
        """Append data point to CSV for external analysis"""

        file_exists = self.datapoints_csv.exists()

        with open(self.datapoints_csv, 'a', newline='') as f:
            fieldnames = [
                'trade_id', 'timestamp', 'revenue', 'hours',
                'revenue_per_hour', 'leads', 'conversion_rate', 'notes'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                'trade_id': trade_id,
                'timestamp': dp.timestamp,
                'revenue': dp.revenue,
                'hours': dp.hours,
                'revenue_per_hour': dp.revenue_per_hour(),
                'leads': dp.leads,
                'conversion_rate': dp.conversion_rate,
                'notes': dp.notes
            })

    def _save_results_csv(self, trade: PaperTrade, summary: StatisticalSummary) -> None:
        """Save final results to CSV for screening system integration"""

        file_exists = self.results_csv.exists()

        with open(self.results_csv, 'a', newline='') as f:
            fieldnames = [
                'trade_id', 'method_id', 'alpha_id', 'decision', 'decision_confidence',
                'n_observations', 'mean_revenue_per_hour', 'std_revenue_per_hour',
                'ci_lower', 'ci_upper', 'sharpe_ratio', 'max_drawdown_percent',
                'total_revenue', 'total_hours', 'total_leads',
                'kelly_fraction', 'recommended_position_size',
                'scalability_score', 'platform_risk',
                'budget', 'duration_days', 'completed_date'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                'trade_id': trade.trade_id,
                'method_id': trade.method_id,
                'alpha_id': trade.alpha_id,
                'decision': trade.decision,
                'decision_confidence': round(trade.decision_confidence, 3),
                'n_observations': summary.n_observations,
                'mean_revenue_per_hour': round(summary.mean_revenue_per_hour, 2),
                'std_revenue_per_hour': round(summary.std_revenue_per_hour, 2),
                'ci_lower': round(summary.confidence_interval_lower, 2),
                'ci_upper': round(summary.confidence_interval_upper, 2),
                'sharpe_ratio': round(summary.sharpe_ratio, 2),
                'max_drawdown_percent': round(summary.max_drawdown_percent, 1),
                'total_revenue': round(summary.total_revenue, 2),
                'total_hours': round(summary.total_hours, 1),
                'total_leads': summary.total_leads,
                'kelly_fraction': round(trade.kelly_fraction, 3),
                'recommended_position_size': round(trade.recommended_position_size, 2),
                'scalability_score': trade.scalability_score,
                'platform_risk': trade.platform_risk,
                'budget': trade.budget,
                'duration_days': trade.duration_days,
                'completed_date': datetime.now().isoformat()
            })

    def _write_to_revenue_tracker(self, trade: PaperTrade, summary: StatisticalSummary) -> None:
        """Write paper trade revenue to main revenue tracker"""

        file_exists = self.revenue_tracker.exists()

        with open(self.revenue_tracker, 'a', newline='') as f:
            fieldnames = [
                'date', 'method_id', 'method_name', 'revenue',
                'expenses', 'profit', 'source', 'notes'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            profit = summary.total_revenue - trade.budget

            writer.writerow({
                'date': datetime.now().strftime('%Y-%m-%d'),
                'method_id': trade.method_id,
                'method_name': trade.method_id,
                'revenue': round(summary.total_revenue, 2),
                'expenses': round(trade.budget, 2),
                'profit': round(profit, 2),
                'source': f"paper_trade:{trade.trade_id}",
                'notes': f"Paper trade {trade.trade_id} - Decision: {trade.decision}"
            })


def main():
    parser = argparse.ArgumentParser(
        description='Institutional-Grade Paper Trading System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Start new paper trade:
    python3 paper_trade.py --method MM001_APP_FACTORY --alpha ALPHA524 --budget 100 --days 14

  Record data point:
    python3 paper_trade.py --record PAPER_TRADE_001 --revenue 45 --hours 2 --leads 3

  Analyze trade:
    python3 paper_trade.py --analyze PAPER_TRADE_001

  Complete trade (make SCALE/KILL decision):
    python3 paper_trade.py --complete PAPER_TRADE_001

  List all trades:
    python3 paper_trade.py --list

  Check alerts:
    python3 paper_trade.py --alerts
        """
    )

    # Start new trade
    parser.add_argument('--method', help='Method ID (e.g., MM001_APP_FACTORY)')
    parser.add_argument('--alpha', help='Alpha ID being tested (e.g., ALPHA524)')
    parser.add_argument('--budget', type=float, default=100, help='Budget ($0-100, default: 100)')
    parser.add_argument('--days', type=int, default=14, help='Duration in days (7-30, default: 14)')
    parser.add_argument('--scalability', type=int, default=5, help='Scalability score (1-10)')
    parser.add_argument('--risk', type=int, default=5, help='Platform risk (1-10)')
    parser.add_argument('--notes', default='', help='Notes about this paper trade')

    # Record data point
    parser.add_argument('--record', help='Record data point for trade ID')
    parser.add_argument('--revenue', type=float, help='Revenue generated ($)')
    parser.add_argument('--hours', type=float, help='Hours spent')
    parser.add_argument('--leads', type=int, default=0, help='Leads generated')
    parser.add_argument('--conversion', type=float, default=0, help='Conversion rate (0-1)')

    # Actions
    parser.add_argument('--analyze', help='Full analysis of trade ID')
    parser.add_argument('--complete', help='Complete trade and make decision')
    parser.add_argument('--force', action='store_true', help='Force completion even with insufficient data')
    parser.add_argument('--list', action='store_true', help='List all paper trades')
    parser.add_argument('--alerts', action='store_true', help='Check all trades for alerts')
    parser.add_argument('--status', help='Filter list by status (RUNNING, COMPLETE, SCALED, KILLED)')

    args = parser.parse_args()

    manager = PaperTradeManager()

    if args.record:
        if args.revenue is None or args.hours is None:
            print("Error: --record requires --revenue and --hours")
            return
        manager.record_data_point(
            trade_id=args.record,
            revenue=args.revenue,
            hours=args.hours,
            leads=args.leads,
            conversion_rate=args.conversion,
            notes=args.notes
        )

    elif args.analyze:
        manager.analyze_trade(args.analyze)

    elif args.complete:
        manager.complete_trade(args.complete, force=args.force)

    elif args.list:
        manager.list_trades(status_filter=args.status)

    elif args.alerts:
        manager.check_alerts()

    elif args.method and args.alpha:
        manager.start_paper_trade(
            method_id=args.method,
            alpha_id=args.alpha,
            budget=args.budget,
            duration_days=args.days,
            scalability=args.scalability,
            platform_risk=args.risk,
            notes=args.notes
        )

    else:
        print("Please specify an action:")
        print("  --method + --alpha  Start new paper trade")
        print("  --record            Record data point")
        print("  --analyze           Full analysis")
        print("  --complete          Make SCALE/KILL decision")
        print("  --list              List all trades")
        print("  --alerts            Check for alerts")
        parser.print_help()


if __name__ == "__main__":
    main()
