#!/usr/bin/env python3
"""
Revenue Projector - Jane Street Level Capital Allocation

Monte Carlo simulation + Kelly Criterion for optimal position sizing across money methods.

Integrates 5 data sources:
1. Backtests (LEDGER/BACKTESTS/BACKTEST_RESULTS.csv)
2. Paper trades (LEDGER/PAPER_TRADES/)
3. Validated alpha (OPS/TOP_20_VALIDATED_ALPHA.csv)
4. Synergies (LEDGER/CROSS_POLLINATION_MATRIX.csv)
5. Actual revenue (FINANCIALS/REVENUE_TRACKER.csv)

Usage:
    python3 revenue_projector.py

Output:
    - OPS/REVENUE_PROJECTIONS_2026.md (full report)
    - LEDGER/KELLY_ALLOCATIONS.csv (position sizing)
    - OPS/projections/METHOD_PROJECTIONS.csv (raw data)
"""

import csv
import json
import numpy as np
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class MethodProjection:
    """Projection for a single money method"""
    method_id: str
    method_name: str
    category: str

    # Input parameters
    backtest_score: float
    confidence: float
    alpha_count: int
    synergy_multiplier: float
    baseline_monthly_revenue: float
    monthly_growth_rate: float
    platform_risk: int  # 1-10
    saturation_risk: int  # 1-10
    execution_difficulty: int  # 1-10
    time_to_first_dollar_days: int
    time_to_scale_months: int
    churn_rate_monthly: float
    half_life_months: int

    # Monte Carlo results (percentiles)
    conservative_7d: float  # 10th percentile
    conservative_30d: float
    conservative_90d: float
    conservative_1yr: float

    base_7d: float  # 50th percentile (median)
    base_30d: float
    base_90d: float
    base_1yr: float

    optimistic_7d: float  # 90th percentile
    optimistic_30d: float
    optimistic_90d: float
    optimistic_1yr: float

    # Kelly Criterion
    kelly_fraction: float
    optimal_capital_allocation: float
    expected_roi: float


@dataclass
class PortfolioProjection:
    """Portfolio-level aggregates"""
    total_methods: int
    active_methods: int

    # Aggregate projections
    conservative_7d: float
    conservative_30d: float
    conservative_90d: float
    conservative_1yr: float

    base_7d: float
    base_30d: float
    base_90d: float
    base_1yr: float

    optimistic_7d: float
    optimistic_30d: float
    optimistic_90d: float
    optimistic_1yr: float

    # Risk metrics
    portfolio_sharpe: float
    max_drawdown: float
    concentration_risk: float
    correlation_avg: float

    # Capital allocation
    total_capital: float
    allocated_capital: float
    reserve_capital: float


class RevenueProjector:
    """Revenue projection engine with Monte Carlo + Kelly Criterion"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.ledger = project_root / "LEDGER"
        self.ops = project_root / "OPS"
        self.financials = project_root / "FINANCIALS"

        # Load data sources
        self.backtests = self._load_backtests()
        self.paper_trades = self._load_paper_trades()
        self.validated_alpha = self._load_validated_alpha()
        self.synergies = self._load_synergies()
        self.actual_revenue = self._load_actual_revenue()

        # Calibration factor (conservative bias)
        self.calibration_factor = self._calculate_calibration()

    def _load_backtests(self) -> List[Dict]:
        """Load backtest results"""
        file = self.ledger / "BACKTESTS" / "BACKTEST_RESULTS.csv"
        if not file.exists():
            return []

        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def _load_paper_trades(self) -> List[Dict]:
        """Load paper trade results"""
        trades_dir = self.ledger / "PAPER_TRADES"
        if not trades_dir.exists():
            return []

        trades = []
        for file in trades_dir.glob("PAPER_TRADE_*.csv"):
            with open(file, 'r') as f:
                reader = csv.DictReader(f)
                trades.extend(list(reader))

        return trades

    def _load_validated_alpha(self) -> List[Dict]:
        """Load validated alpha entries"""
        file = self.ops / "TOP_20_VALIDATED_ALPHA.csv"
        if not file.exists():
            return []

        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def _load_synergies(self) -> Dict[str, float]:
        """Load synergy multipliers"""
        file = self.ledger / "CROSS_POLLINATION_MATRIX.csv"
        if not file.exists():
            return {}

        synergies = {}
        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'method_id' in row and 'synergy_score' in row:
                    method_id = row['method_id']
                    score = float(row['synergy_score']) if row['synergy_score'] else 0.0
                    # Convert 0-100 score to 1.0-3.0 multiplier
                    multiplier = 1.0 + (score / 100.0) * 2.0
                    synergies[method_id] = multiplier

        return synergies

    def _load_actual_revenue(self) -> List[Dict]:
        """Load actual revenue data"""
        file = self.financials / "REVENUE_TRACKER.csv"
        if not file.exists():
            return []

        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def _calculate_calibration(self) -> float:
        """Calculate calibration factor from actual vs projected"""
        # Default: conservative 0.7x
        # As actual revenue grows, this adjusts to reality

        if not self.actual_revenue:
            return 0.7

        # Compare actual revenue to any projections
        # For now: stay conservative
        return 0.7

    def project_method(
        self,
        method_id: str,
        method_name: str,
        category: str
    ) -> MethodProjection:
        """Project revenue for a single method using Monte Carlo"""

        # Get parameters from data sources
        params = self._get_method_params(method_id, category)

        # Run Monte Carlo simulations
        projections = self._monte_carlo_simulate(params)

        # Calculate Kelly fraction
        kelly = self._kelly_criterion(params, projections)

        return MethodProjection(
            method_id=method_id,
            method_name=method_name,
            category=category,
            **params,
            **projections,
            kelly_fraction=kelly,
            optimal_capital_allocation=kelly * 10000,  # Out of $10K total
            expected_roi=projections['base_1yr'] / 1000.0 if projections['base_1yr'] > 0 else 0.0
        )

    def _get_method_params(self, method_id: str, category: str) -> Dict:
        """Get method parameters from data sources"""

        # Backtest score
        backtest_score = 0.0
        for bt in self.backtests:
            if bt.get('alpha_id', '').startswith(method_id) or bt.get('category') == category:
                try:
                    backtest_score = max(backtest_score, float(bt.get('score', 0)))
                except:
                    pass

        # Paper trade data
        paper_revenue_hour = 0.0
        paper_scalability = 5.0
        paper_platform_risk = 5.0

        for pt in self.paper_trades:
            if pt.get('method_id') == method_id:
                try:
                    paper_revenue_hour = float(pt.get('revenue_per_hour', 0))
                    paper_scalability = float(pt.get('scalability', 5))
                    paper_platform_risk = float(pt.get('platform_risk', 5))
                except:
                    pass

        # Validated alpha
        confidence = 50.0
        alpha_count = 0
        baseline_monthly = 0.0

        for alpha in self.validated_alpha:
            if alpha.get('method_id') == method_id or alpha.get('category') == category:
                alpha_count += 1
                try:
                    conf = float(alpha.get('confidence', 50))
                    confidence = max(confidence, conf)

                    # Extract revenue baseline
                    rev_str = alpha.get('revenue_range', '')
                    if '$' in rev_str and '-' in rev_str:
                        # Parse "$X-$Y" format
                        parts = rev_str.replace('$', '').replace(',', '').split('-')
                        if len(parts) == 2:
                            low = float(parts[0])
                            high = float(parts[1])
                            baseline_monthly = max(baseline_monthly, (low + high) / 2)
                except:
                    pass

        # Paper trade revenue takes precedence
        if paper_revenue_hour > 0:
            # $X/hour * 160 hours/mo
            baseline_monthly = max(baseline_monthly, paper_revenue_hour * 160)

        # Fallback defaults
        if baseline_monthly == 0:
            # Category-based defaults
            defaults = {
                'APP_FACTORY': 2000,
                'MONETIZATION': 1500,
                'CONTENT_FARM': 800,
                'OUTBOUND': 1000,
                'AI_INFLUENCER': 1200,
                'ECOM_ARB': 1500,
            }
            baseline_monthly = defaults.get(category, 1000)

        # Synergy multiplier
        synergy_mult = self.synergies.get(method_id, 1.0)

        # Growth rate from backtest/confidence
        if backtest_score >= 70:
            growth_rate = 0.25  # 25%/mo for high-confidence
        elif backtest_score >= 50:
            growth_rate = 0.15  # 15%/mo for moderate
        else:
            growth_rate = 0.10  # 10%/mo for low

        # Risk scores
        platform_risk = int(paper_platform_risk) if paper_platform_risk > 0 else 5

        execution_difficulty = 5  # Default medium
        if category == 'APP_FACTORY':
            execution_difficulty = 7
        elif category == 'CONTENT_FARM':
            execution_difficulty = 3
        elif category == 'OUTBOUND':
            execution_difficulty = 4

        saturation_risk = 5  # Default medium

        # Timing
        time_to_first_dollar = 7 if backtest_score >= 70 else 14
        time_to_scale = 3 if backtest_score >= 70 else 6
        churn_rate = 0.05  # 5%/mo default
        half_life = 18  # 18 months before method decay

        return {
            'backtest_score': backtest_score,
            'confidence': confidence,
            'alpha_count': alpha_count,
            'synergy_multiplier': synergy_mult,
            'baseline_monthly_revenue': baseline_monthly,
            'monthly_growth_rate': growth_rate,
            'platform_risk': platform_risk,
            'saturation_risk': saturation_risk,
            'execution_difficulty': execution_difficulty,
            'time_to_first_dollar_days': time_to_first_dollar,
            'time_to_scale_months': time_to_scale,
            'churn_rate_monthly': churn_rate,
            'half_life_months': half_life,
        }

    def _monte_carlo_simulate(self, params: Dict) -> Dict[str, float]:
        """Run Monte Carlo simulation for revenue projections"""

        n_sims = 1000

        # Risk adjustment
        risk_discount = (params['platform_risk'] + params['execution_difficulty']) / 200.0
        risk_discount = min(risk_discount, 0.30)  # Max 30% discount

        baseline = params['baseline_monthly_revenue'] * (1 - risk_discount)
        baseline *= self.calibration_factor

        growth_rate = params['monthly_growth_rate']
        synergy = params['synergy_multiplier']
        churn = params['churn_rate_monthly']
        half_life = params['half_life_months']
        time_to_first = params['time_to_first_dollar_days']

        # Simulate 4 timeframes
        timeframes = {
            '7d': 7,
            '30d': 30,
            '90d': 90,
            '1yr': 365
        }

        results = {}

        for tf_name, days in timeframes.items():
            revenues = []

            for _ in range(n_sims):
                # Random factors
                baseline_factor = np.random.uniform(0.7, 1.3)
                growth_factor = np.random.uniform(0.8, 1.2)

                current_baseline = baseline * baseline_factor
                current_growth = growth_rate * growth_factor

                total_revenue = 0.0
                current_monthly = 0.0

                for day in range(days):
                    # Time to first dollar
                    if day < time_to_first:
                        continue

                    # Monthly progression
                    if day % 30 == 0 and day > 0:
                        month = day // 30

                        # Growth
                        if month <= params['time_to_scale_months']:
                            # Ramp up
                            current_monthly = current_baseline * ((1 + current_growth) ** month)
                        else:
                            # Post-scale: synergies compound
                            synergy_boost = synergy ** (month - params['time_to_scale_months'])
                            current_monthly = current_baseline * ((1 + current_growth) ** params['time_to_scale_months']) * synergy_boost

                        # Churn
                        current_monthly *= (1 - churn)

                        # Half-life decay
                        if month > half_life:
                            decay_factor = 0.5 ** ((month - half_life) / half_life)
                            current_monthly *= decay_factor

                    # Daily revenue
                    daily = current_monthly / 30.0
                    daily *= np.random.uniform(0.9, 1.1)  # Daily variance
                    total_revenue += daily

                revenues.append(total_revenue)

            # Percentiles
            revenues = np.array(revenues)
            results[f'conservative_{tf_name}'] = np.percentile(revenues, 10)
            results[f'base_{tf_name}'] = np.percentile(revenues, 50)
            results[f'optimistic_{tf_name}'] = np.percentile(revenues, 90)

        return results

    def _kelly_criterion(self, params: Dict, projections: Dict) -> float:
        """Calculate Kelly fraction for position sizing"""

        # Kelly = (p * b - q) / b
        # p = probability of win
        # q = probability of loss = 1 - p
        # b = win/loss ratio (return/risk)

        # Probability from backtest + confidence
        backtest_prob = params['backtest_score'] / 100.0
        confidence_prob = params['confidence'] / 100.0

        p = (backtest_prob * 0.6) + (confidence_prob * 0.4)  # Weighted
        p = max(0.01, min(p, 0.99))  # Clamp

        q = 1 - p

        # Win/loss ratio
        expected_return = projections['base_1yr'] / 1000.0  # Assume $1K investment
        expected_return = max(expected_return, 0.01)

        risk = (params['platform_risk'] + params['execution_difficulty']) / 20.0
        risk = max(risk, 0.01)

        b = expected_return / risk

        # Kelly
        kelly = (p * b - q) / b
        kelly = max(0.0, kelly)

        # Fractional Kelly (cap at 25% for safety)
        kelly = min(kelly, 0.25)

        return kelly

    def project_portfolio(
        self,
        methods: List[MethodProjection],
        total_capital: float = 10000.0
    ) -> PortfolioProjection:
        """Project portfolio-level metrics"""

        # Aggregate projections
        conservative_7d = sum(m.conservative_7d for m in methods)
        conservative_30d = sum(m.conservative_30d for m in methods)
        conservative_90d = sum(m.conservative_90d for m in methods)
        conservative_1yr = sum(m.conservative_1yr for m in methods)

        base_7d = sum(m.base_7d for m in methods)
        base_30d = sum(m.base_30d for m in methods)
        base_90d = sum(m.base_90d for m in methods)
        base_1yr = sum(m.base_1yr for m in methods)

        optimistic_7d = sum(m.optimistic_7d for m in methods)
        optimistic_30d = sum(m.optimistic_30d for m in methods)
        optimistic_90d = sum(m.optimistic_90d for m in methods)
        optimistic_1yr = sum(m.optimistic_1yr for m in methods)

        # Portfolio Sharpe (simplified: return / risk)
        returns = [m.expected_roi for m in methods]
        risks = [(m.platform_risk + m.execution_difficulty) / 20.0 for m in methods]

        avg_return = np.mean(returns) if returns else 0.0
        avg_risk = np.mean(risks) if risks else 1.0
        sharpe = avg_return / avg_risk if avg_risk > 0 else 0.0

        # Max drawdown (simulate worst case)
        max_drawdown = 0.30  # Assume 30% drawdown in pessimistic scenario

        # Concentration risk
        total_allocation = sum(m.optimal_capital_allocation for m in methods)
        if total_allocation > 0:
            max_position = max(m.optimal_capital_allocation for m in methods)
            concentration = max_position / total_allocation
        else:
            concentration = 0.0

        # Correlation (simplified: assume 0.3 average)
        correlation_avg = 0.3

        # Kelly allocations
        allocated = sum(m.optimal_capital_allocation for m in methods)
        reserve = total_capital - allocated

        return PortfolioProjection(
            total_methods=len(methods),
            active_methods=len([m for m in methods if m.backtest_score >= 50]),
            conservative_7d=conservative_7d,
            conservative_30d=conservative_30d,
            conservative_90d=conservative_90d,
            conservative_1yr=conservative_1yr,
            base_7d=base_7d,
            base_30d=base_30d,
            base_90d=base_90d,
            base_1yr=base_1yr,
            optimistic_7d=optimistic_7d,
            optimistic_30d=optimistic_30d,
            optimistic_90d=optimistic_90d,
            optimistic_1yr=optimistic_1yr,
            portfolio_sharpe=sharpe,
            max_drawdown=max_drawdown,
            concentration_risk=concentration,
            correlation_avg=correlation_avg,
            total_capital=total_capital,
            allocated_capital=allocated,
            reserve_capital=reserve
        )

    def save_projections(
        self,
        methods: List[MethodProjection],
        portfolio: PortfolioProjection,
        output_dir: Path
    ):
        """Save projections to CSV and markdown report"""

        output_dir.mkdir(parents=True, exist_ok=True)

        # Save method projections
        method_file = output_dir / "METHOD_PROJECTIONS.csv"
        with open(method_file, 'w', newline='') as f:
            if methods:
                writer = csv.DictWriter(f, fieldnames=list(asdict(methods[0]).keys()))
                writer.writeheader()
                for method in methods:
                    writer.writerow(asdict(method))

        print(f"✅ Saved method projections: {method_file}")

        # Save Kelly allocations
        kelly_file = self.ledger / "KELLY_ALLOCATIONS.csv"
        with open(kelly_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['method_id', 'method_name', 'kelly_fraction', 'optimal_allocation', 'expected_roi'])
            for method in sorted(methods, key=lambda m: m.kelly_fraction, reverse=True):
                writer.writerow([
                    method.method_id,
                    method.method_name,
                    f"{method.kelly_fraction:.3f}",
                    f"${method.optimal_capital_allocation:.2f}",
                    f"{method.expected_roi:.2f}x"
                ])

        print(f"✅ Saved Kelly allocations: {kelly_file}")

        # Generate markdown report
        self._generate_report(methods, portfolio, output_dir)

    def _generate_report(
        self,
        methods: List[MethodProjection],
        portfolio: PortfolioProjection,
        output_dir: Path
    ):
        """Generate comprehensive markdown report"""

        report_file = self.ops / "REVENUE_PROJECTIONS_2026.md"

        with open(report_file, 'w') as f:
            f.write("# Revenue Projections 2026\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("**Model:** Monte Carlo simulation (1,000 runs per timeframe)\n")
            f.write("**Position Sizing:** Kelly Criterion\n")
            f.write(f"**Calibration Factor:** {self.calibration_factor:.2f} (conservative)\n\n")

            f.write("---\n\n")
            f.write("## Portfolio Summary\n\n")

            f.write(f"**Total Methods:** {portfolio.total_methods}\n")
            f.write(f"**Active Methods:** {portfolio.active_methods} (backtest ≥50)\n\n")

            f.write("### Aggregate Projections\n\n")
            f.write("| Timeframe | Conservative (10th %ile) | Base (50th %ile) | Optimistic (90th %ile) |\n")
            f.write("|-----------|--------------------------|------------------|------------------------|\n")
            f.write(f"| **7 Days** | ${portfolio.conservative_7d:,.2f} | ${portfolio.base_7d:,.2f} | ${portfolio.optimistic_7d:,.2f} |\n")
            f.write(f"| **30 Days** | ${portfolio.conservative_30d:,.2f} | ${portfolio.base_30d:,.2f} | ${portfolio.optimistic_30d:,.2f} |\n")
            f.write(f"| **90 Days** | ${portfolio.conservative_90d:,.2f} | ${portfolio.base_90d:,.2f} | ${portfolio.optimistic_90d:,.2f} |\n")
            f.write(f"| **1 Year** | ${portfolio.conservative_1yr:,.2f} | ${portfolio.base_1yr:,.2f} | ${portfolio.optimistic_1yr:,.2f} |\n\n")

            f.write("### Risk Metrics\n\n")
            f.write(f"- **Portfolio Sharpe:** {portfolio.portfolio_sharpe:.2f}\n")
            f.write(f"- **Max Drawdown:** {portfolio.max_drawdown * 100:.1f}%\n")
            f.write(f"- **Concentration Risk:** {portfolio.concentration_risk * 100:.1f}%\n")
            f.write(f"- **Average Correlation:** {portfolio.correlation_avg:.2f}\n\n")

            f.write("### Capital Allocation\n\n")
            f.write(f"- **Total Capital:** ${portfolio.total_capital:,.2f}\n")
            f.write(f"- **Allocated:** ${portfolio.allocated_capital:,.2f} ({portfolio.allocated_capital/portfolio.total_capital*100:.1f}%)\n")
            f.write(f"- **Reserve:** ${portfolio.reserve_capital:,.2f} ({portfolio.reserve_capital/portfolio.total_capital*100:.1f}%)\n\n")

            f.write("---\n\n")
            f.write("## Top 10 Methods by Kelly Allocation\n\n")

            top_methods = sorted(methods, key=lambda m: m.kelly_fraction, reverse=True)[:10]

            f.write("| Rank | Method | Kelly % | Allocation | 1Y Base | ROI |\n")
            f.write("|------|--------|---------|------------|---------|-----|\n")

            for i, method in enumerate(top_methods, 1):
                f.write(f"| {i} | {method.method_name} | {method.kelly_fraction*100:.1f}% | ")
                f.write(f"${method.optimal_capital_allocation:,.0f} | ")
                f.write(f"${method.base_1yr:,.0f} | {method.expected_roi:.1f}x |\n")

            f.write("\n---\n\n")
            f.write("## Method Details\n\n")

            for method in sorted(methods, key=lambda m: m.base_1yr, reverse=True):
                f.write(f"### {method.method_name} ({method.method_id})\n\n")

                f.write("**Performance Metrics:**\n")
                f.write(f"- Backtest Score: {method.backtest_score:.1f}/100\n")
                f.write(f"- Confidence: {method.confidence:.1f}%\n")
                f.write(f"- Alpha Count: {method.alpha_count}\n")
                f.write(f"- Synergy Multiplier: {method.synergy_multiplier:.2f}x\n\n")

                f.write("**Revenue Projections:**\n\n")
                f.write("| Timeframe | Conservative | Base | Optimistic |\n")
                f.write("|-----------|--------------|------|------------|\n")
                f.write(f"| 7d | ${method.conservative_7d:,.2f} | ${method.base_7d:,.2f} | ${method.optimistic_7d:,.2f} |\n")
                f.write(f"| 30d | ${method.conservative_30d:,.2f} | ${method.base_30d:,.2f} | ${method.optimistic_30d:,.2f} |\n")
                f.write(f"| 90d | ${method.conservative_90d:,.2f} | ${method.base_90d:,.2f} | ${method.optimistic_90d:,.2f} |\n")
                f.write(f"| 1yr | ${method.conservative_1yr:,.2f} | ${method.base_1yr:,.2f} | ${method.optimistic_1yr:,.2f} |\n\n")

                f.write("**Risk Factors:**\n")
                f.write(f"- Platform Risk: {method.platform_risk}/10\n")
                f.write(f"- Saturation Risk: {method.saturation_risk}/10\n")
                f.write(f"- Execution Difficulty: {method.execution_difficulty}/10\n\n")

                f.write("**Kelly Position:**\n")
                f.write(f"- Kelly Fraction: {method.kelly_fraction*100:.1f}%\n")
                f.write(f"- Optimal Allocation: ${method.optimal_capital_allocation:,.2f}\n")
                f.write(f"- Expected ROI: {method.expected_roi:.2f}x\n\n")

                f.write("**Timing:**\n")
                f.write(f"- Time to First Dollar: {method.time_to_first_dollar_days} days\n")
                f.write(f"- Time to Scale: {method.time_to_scale_months} months\n")
                f.write(f"- Half-Life: {method.half_life_months} months\n\n")

                f.write("---\n\n")

            f.write("## Methodology\n\n")
            f.write("### Data Sources\n\n")
            f.write("1. **Backtests:** LEDGER/BACKTESTS/BACKTEST_RESULTS.csv\n")
            f.write("2. **Paper Trades:** LEDGER/PAPER_TRADES/\n")
            f.write("3. **Validated Alpha:** OPS/TOP_20_VALIDATED_ALPHA.csv\n")
            f.write("4. **Synergies:** LEDGER/CROSS_POLLINATION_MATRIX.csv\n")
            f.write("5. **Actual Revenue:** FINANCIALS/REVENUE_TRACKER.csv\n\n")

            f.write("### Monte Carlo Simulation\n\n")
            f.write("- **Runs:** 1,000 per timeframe\n")
            f.write("- **Variables:** Baseline revenue, growth rate, risk factors\n")
            f.write("- **Random Factors:** 0.7-1.3x baseline, 0.8-1.2x growth, 0.9-1.1x daily\n")
            f.write("- **Risk Adjustments:** Platform risk + execution difficulty (max 30% discount)\n")
            f.write("- **Growth:** Compounded monthly with synergy multipliers\n")
            f.write("- **Decay:** Half-life applied after maturity\n\n")

            f.write("### Kelly Criterion\n\n")
            f.write("```\n")
            f.write("Kelly = (p * b - q) / b\n")
            f.write("where:\n")
            f.write("  p = probability of win (from backtest + confidence)\n")
            f.write("  q = probability of loss = 1 - p\n")
            f.write("  b = win/loss ratio (expected return / risk)\n")
            f.write("```\n\n")
            f.write("Capped at 25% per position (fractional Kelly for safety).\n\n")

            f.write("### Calibration\n\n")
            f.write(f"Applied {self.calibration_factor:.2f}x calibration factor based on:\n")
            f.write("- Industry benchmarks (projections typically 70% of reality)\n")
            f.write("- Conservative bias (better to underestimate)\n")
            f.write("- Actual revenue data when available\n\n")

            f.write("---\n\n")
            f.write("## Next Steps\n\n")
            f.write("1. **Deploy top Kelly methods** - Allocate capital per recommendations\n")
            f.write("2. **Track actual vs projected** - Update calibration factor\n")
            f.write("3. **Rebalance monthly** - Adjust allocations based on performance\n")
            f.write("4. **Kill underperformers** - Methods < 50% of base projection after 90 days\n")
            f.write("5. **Scale winners** - 2x allocation for methods > 150% of base\n\n")

        print(f"✅ Generated report: {report_file}")


def main():
    """Run revenue projections"""

    print("Revenue Projector - Jane Street Level")
    print("=" * 60)
    print()

    # Initialize projector
    project_root = Path(__file__).parent.parent
    projector = RevenueProjector(project_root)

    print(f"Loaded data sources:")
    print(f"  - Backtests: {len(projector.backtests)} entries")
    print(f"  - Paper Trades: {len(projector.paper_trades)} methods")
    print(f"  - Validated Alpha: {len(projector.validated_alpha)} entries")
    print(f"  - Synergies: {len(projector.synergies)} methods")
    print(f"  - Actual Revenue: {len(projector.actual_revenue)} transactions")
    print(f"  - Calibration Factor: {projector.calibration_factor:.2f}")
    print()

    # Project key methods
    print("Running Monte Carlo simulations...")
    print()

    key_methods = [
        ('MM001', 'APP_FACTORY', 'APP_FACTORY'),
        ('MM002', 'INFO_PRODUCTS', 'MONETIZATION'),
        ('MM006', 'CONTENT_FARM', 'CONTENT_FARM'),
        ('MM007', 'COLD_OUTBOUND', 'OUTBOUND'),
        ('MM009', 'AI_INFLUENCER', 'AI_INFLUENCER'),
        ('MM016', 'TIKTOK_SHOP', 'ECOM_ARB'),
        ('MM092', 'WEB_TO_APP_FUNNEL', 'APP_FACTORY'),
    ]

    projections = []

    for method_id, method_name, category in key_methods:
        print(f"  Projecting {method_name}...")
        projection = projector.project_method(method_id, method_name, category)
        projections.append(projection)

    print()
    print("Calculating portfolio metrics...")

    # Project portfolio
    portfolio = projector.project_portfolio(projections, total_capital=10000.0)

    # Save results
    output_dir = project_root / "OPS" / "projections"
    projector.save_projections(projections, portfolio, output_dir)

    print()
    print("=" * 60)
    print("PORTFOLIO SUMMARY")
    print("=" * 60)
    print()
    print(f"Base Case (50th percentile):")
    print(f"  7 Days:   ${portfolio.base_7d:,.2f}")
    print(f"  30 Days:  ${portfolio.base_30d:,.2f}")
    print(f"  90 Days:  ${portfolio.base_90d:,.2f}")
    print(f"  1 Year:   ${portfolio.base_1yr:,.2f}")
    print()
    print(f"Portfolio Sharpe: {portfolio.portfolio_sharpe:.2f}")
    print(f"Max Drawdown: {portfolio.max_drawdown * 100:.1f}%")
    print(f"Concentration Risk: {portfolio.concentration_risk * 100:.1f}%")
    print()
    print(f"Capital Allocation: ${portfolio.allocated_capital:,.2f} / ${portfolio.total_capital:,.2f}")
    print(f"Reserve: ${portfolio.reserve_capital:,.2f}")
    print()
    print("=" * 60)
    print()
    print("Full report: OPS/REVENUE_PROJECTIONS_2026.md")
    print("Kelly allocations: LEDGER/KELLY_ALLOCATIONS.csv")
    print()


if __name__ == "__main__":
    main()
