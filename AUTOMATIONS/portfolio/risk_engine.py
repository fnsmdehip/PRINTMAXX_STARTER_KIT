"""
risk_engine.py - Portfolio risk analytics engine (Jane Street / Two Sigma style)

Standalone module that calculates institutional-grade risk metrics for the
PRINTMAXX solopreneur portfolio. All math ported from printmaxx_quant_terminal.py
with identical implementations.

Metrics: Sharpe, Sortino, VaR (parametric + historical), CVaR, max drawdown,
HHI concentration, beta, information coefficient.
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional


@dataclass
class PortfolioRisk:
    """Portfolio-level risk metrics - Jane Street / Two Sigma style.

    All fields default to safe zero values so the dataclass is usable
    even when there is no revenue history yet.
    """
    total_revenue: float = 0.0
    portfolio_sharpe: float = 0.0
    portfolio_sortino: float = 0.0
    sharpe_ci: Tuple[float, float] = (0.0, 0.0)
    sharpe_data_months: int = 0
    var_95: float = 0.0
    var_99: float = 0.0
    var_95_historical: float = 0.0
    var_99_historical: float = 0.0
    cvar_95: float = 0.0
    cvar_99: float = 0.0
    max_drawdown: float = 0.0
    current_drawdown: float = 0.0
    drawdown_duration: int = 0
    hhi_method: float = 0.0
    hhi_platform: float = 0.0
    hhi_niche: float = 0.0
    concentration_max_method: Tuple[str, float] = ("", 0.0)
    concentration_max_platform: Tuple[str, float] = ("", 0.0)
    beta: float = 0.0
    beta_confidence: str = "N/A"
    ic: float = 0.0
    ic_hit_rate: float = 0.0
    ic_sample_size: int = 0


# ---------------------------------------------------------------------------
# Individual risk functions
# ---------------------------------------------------------------------------

def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.05) -> float:
    """Calculate annualized Sharpe ratio from a monthly returns series.

    Sharpe = (mean_excess_return / std_dev) * sqrt(12)

    The risk-free rate is divided by 12 to get the monthly rate.
    Population std dev is used (dividing by N, not N-1) to match the
    original implementation.

    Args:
        returns: Monthly percentage returns (e.g. 0.10 = 10%).
        risk_free_rate: Annual risk-free rate (default 5%).

    Returns:
        Annualized Sharpe ratio rounded to 2 decimals.
        0.0 if fewer than 2 data points.
    """
    if len(returns) < 2:
        return 0.0

    mean_return = sum(returns) / len(returns)
    variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
    std_dev = math.sqrt(variance) if variance > 0 else 0.001

    excess_return = mean_return - (risk_free_rate / 12)
    sharpe = (excess_return / std_dev) * math.sqrt(12) if std_dev > 0 else 0.0
    return round(sharpe, 2)


def calculate_sortino_ratio(returns: List[float], risk_free_rate: float = 0.05) -> float:
    """Calculate annualized Sortino ratio (penalizes downside volatility only).

    Sortino = (mean_excess_return / downside_deviation) * sqrt(12)

    Downside deviation only considers returns that fall below the target
    (monthly risk-free rate). This rewards strategies with positive
    skew (big wins, small losses).

    Args:
        returns: Monthly percentage returns.
        risk_free_rate: Annual risk-free rate (default 5%).

    Returns:
        Annualized Sortino ratio rounded to 2 decimals.
        0.0 if fewer than 2 data points.
    """
    if len(returns) < 2:
        return 0.0

    mean_return = sum(returns) / len(returns)
    target = risk_free_rate / 12

    downside_returns = [min(0, r - target) ** 2 for r in returns]
    downside_variance = sum(downside_returns) / len(downside_returns)
    downside_dev = math.sqrt(downside_variance) if downside_variance > 0 else 0.001

    excess_return = mean_return - target
    sortino = (excess_return / downside_dev) * math.sqrt(12) if downside_dev > 0 else 0.0
    return round(sortino, 2)


def calculate_sharpe_confidence_interval(
    returns: List[float], sharpe: float
) -> Tuple[float, float]:
    """Calculate 95% confidence interval for the Sharpe ratio.

    Uses the Lo (2002) simplified formula for IID returns:
        SE(SR) = sqrt((1 + SR^2 / 2) / n)

    Critical when sample size < 12 months -- a Sharpe of 2.0 with 3 months
    of data has a CI wide enough to include negative values.

    Args:
        returns: The returns series used to compute `sharpe`.
        sharpe: Pre-computed Sharpe ratio.

    Returns:
        (lower_bound, upper_bound) of the 95% CI, each rounded to 2 decimals.
        (0.0, 0.0) if fewer than 2 data points.
    """
    n = len(returns)
    if n < 2:
        return (0.0, 0.0)

    se = math.sqrt((1 + sharpe ** 2 / 2) / n)

    lower = sharpe - 1.96 * se
    upper = sharpe + 1.96 * se

    return (round(lower, 2), round(upper, 2))


def calculate_max_drawdown(revenues: List[float]) -> Tuple[float, float, int]:
    """Calculate maximum and current drawdown from a revenue series.

    Builds a cumulative equity curve from the revenue sequence, then
    tracks peak-to-trough declines.

    Args:
        revenues: Ordered revenue values (e.g. monthly revenue amounts).

    Returns:
        (max_drawdown_pct, current_drawdown_pct, periods_in_drawdown)
        Drawdowns expressed as positive percentages (e.g. 15.0 = 15%).
        (0.0, 0.0, 0) if fewer than 2 data points or all non-positive.
    """
    if len(revenues) < 2:
        return (0.0, 0.0, 0)

    cumulative: List[float] = []
    total = 0.0
    for r in revenues:
        total += r
        cumulative.append(total)

    if not cumulative or max(cumulative) <= 0:
        return (0.0, 0.0, 0)

    peak = cumulative[0]
    max_dd = 0.0
    current_dd = 0.0
    periods_in_dd = 0
    dd_start = 0

    for i, value in enumerate(cumulative):
        if value > peak:
            peak = value
            dd_start = i

        if peak > 0:
            dd = (peak - value) / peak
            if dd > max_dd:
                max_dd = dd

            if i == len(cumulative) - 1:
                current_dd = dd
                periods_in_dd = i - dd_start if dd > 0 else 0

    return (round(max_dd * 100, 2), round(current_dd * 100, 2), periods_in_dd)


def calculate_parametric_var(returns: List[float], confidence: float = 0.95) -> float:
    """Calculate parametric Value at Risk assuming normal distribution.

    VaR answers: "What is the maximum expected loss over a period at
    a given confidence level?"

    Formula: VaR = -(mean - z * std_dev)

    Uses population std dev (N denominator). Common confidence levels:
    95% (z=1.645) and 99% (z=2.326).

    Args:
        returns: Monthly percentage returns.
        confidence: Confidence level (0.95 or 0.99).

    Returns:
        VaR as a positive percentage (e.g. 12.5 = 12.5% potential loss).
        0.0 if fewer than 2 data points.
    """
    if len(returns) < 2:
        return 0.0

    mean_return = sum(returns) / len(returns)
    variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
    std_dev = math.sqrt(variance) if variance > 0 else 0.0

    z_scores = {0.95: 1.645, 0.99: 2.326}
    z = z_scores.get(confidence, 1.645)

    var = -(mean_return - z * std_dev)
    return max(0, round(var * 100, 2))


def calculate_historical_var(returns: List[float], confidence: float = 0.95) -> float:
    """Calculate historical Value at Risk from actual return distribution.

    Instead of assuming normality, uses the empirical distribution.
    More robust when returns have fat tails (common in indie hacker revenue).

    Requires at least 20 data points for meaningful percentile estimation.

    Args:
        returns: Monthly percentage returns.
        confidence: Confidence level (0.95 or 0.99).

    Returns:
        VaR as a positive percentage.
        0.0 if fewer than 20 data points.
    """
    if len(returns) < 20:
        return 0.0

    sorted_returns = sorted(returns)
    index = int((1 - confidence) * len(sorted_returns))

    var = -sorted_returns[index] if sorted_returns[index] < 0 else 0.0
    return max(0, round(var * 100, 2))


def calculate_cvar(returns: List[float], confidence: float = 0.95) -> float:
    """Calculate Conditional VaR (Expected Shortfall).

    CVaR answers: "If we're in the worst (1-confidence)% of outcomes,
    what is the average loss?"

    Always >= VaR. Better captures tail risk than VaR alone because it
    considers the magnitude of extreme losses, not just the threshold.

    Args:
        returns: Monthly percentage returns.
        confidence: Confidence level (0.95 or 0.99).

    Returns:
        CVaR as a positive percentage.
        0.0 if fewer than 2 data points.
    """
    if len(returns) < 2:
        return 0.0

    sorted_returns = sorted(returns)
    cutoff_index = int((1 - confidence) * len(sorted_returns))

    if cutoff_index == 0:
        cutoff_index = 1

    tail_returns = sorted_returns[:cutoff_index]
    if not tail_returns:
        return 0.0

    avg_tail = sum(tail_returns) / len(tail_returns)
    return max(0, round(-avg_tail * 100, 2))


def calculate_hhi(weights: List[float]) -> float:
    """Calculate Herfindahl-Hirschman Index for concentration measurement.

    HHI = sum of squared market-share weights (after normalising to 1.0).

    Interpretation:
        < 0.15  -> Well diversified
        0.15-0.25 -> Moderate concentration
        > 0.25 -> Highly concentrated (single-method risk)

    Perfect diversification across N methods gives HHI = 1/N.
    Complete concentration in one method gives HHI = 1.0.

    Args:
        weights: Raw revenue (or share) values per category. Need not
                 sum to 1 -- they are normalised internally.

    Returns:
        HHI rounded to 4 decimals.
        0.0 if weights are empty or all zero.
    """
    if not weights:
        return 0.0
    # Filter to non-negative weights only (negative weights are invalid for HHI)
    weights = [max(0.0, w) for w in weights]
    total = sum(weights)
    if total == 0:
        return 0.0
    normalized = [w / total for w in weights]

    return round(sum(w ** 2 for w in normalized), 4)


def calculate_beta(
    method_returns: List[float], market_returns: List[float]
) -> Tuple[float, str]:
    """Calculate beta (sensitivity of method returns to market returns).

    Beta = Cov(method, market) / Var(market)

    Interpretation:
        < 1 -> Less volatile than the market proxy
        = 1 -> Moves 1:1 with the market
        > 1 -> More volatile than the market

    Market proxy for indie hackers would be an aggregate revenue index.
    Requires at least 6 aligned observations.

    Args:
        method_returns: Monthly returns for the method.
        market_returns: Monthly returns for the market proxy.

    Returns:
        (beta, confidence_level) where confidence is
        "HIGH" (>=24 months), "MEDIUM" (>=12), "LOW" (>=6),
        "INSUFFICIENT_DATA" (<6), or "ZERO_VARIANCE".
    """
    n = min(len(method_returns), len(market_returns))

    if n < 6:
        return (0.0, "INSUFFICIENT_DATA")

    method_returns = method_returns[-n:]
    market_returns = market_returns[-n:]

    mean_method = sum(method_returns) / n
    mean_market = sum(market_returns) / n

    covariance = sum(
        (method_returns[i] - mean_method) * (market_returns[i] - mean_market)
        for i in range(n)
    ) / n
    market_variance = sum((r - mean_market) ** 2 for r in market_returns) / n

    if market_variance < 1e-12:
        return (0.0, "ZERO_VARIANCE")

    beta = covariance / market_variance

    if n >= 24:
        confidence = "HIGH"
    elif n >= 12:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    return (round(beta, 2), confidence)


def calculate_information_coefficient(
    predictions: List[Tuple[str, float, float]],
) -> Tuple[float, float, int]:
    """Calculate Information Coefficient for deployed alpha quality.

    IC = Pearson correlation between predicted backtest scores and actual
    revenue outcomes. Measures whether our screening process actually
    predicts real-world performance.

    Hit rate = percentage where high-scoring alpha (>50) generated
    positive revenue OR low-scoring alpha (<=50) generated zero/negative.

    Args:
        predictions: List of (alpha_id, backtest_score, actual_revenue).

    Returns:
        (ic, hit_rate_pct, sample_size)
        (0.0, 0.0, len) if fewer than 5 predictions.
    """
    if len(predictions) < 5:
        return (0.0, 0.0, len(predictions))

    predicted = [p[1] for p in predictions]
    actual = [p[2] for p in predictions]

    n = len(predictions)
    mean_pred = sum(predicted) / n
    mean_actual = sum(actual) / n

    numerator = sum(
        (predicted[i] - mean_pred) * (actual[i] - mean_actual) for i in range(n)
    )

    pred_variance = sum((p - mean_pred) ** 2 for p in predicted)
    actual_variance = sum((a - mean_actual) ** 2 for a in actual)

    denominator = math.sqrt(pred_variance * actual_variance)

    if denominator == 0:
        ic = 0.0
    else:
        ic = numerator / denominator

    hits = sum(
        1
        for i in range(n)
        if (predicted[i] > 50 and actual[i] > 0)
        or (predicted[i] <= 50 and actual[i] <= 0)
    )
    hit_rate = hits / n * 100

    return (round(ic, 3), round(hit_rate, 1), n)


# ---------------------------------------------------------------------------
# Main portfolio risk aggregator
# ---------------------------------------------------------------------------

def calculate_portfolio_risk(
    positions: list,
    revenue_history: List[dict],
    platform_revenue: Dict[str, float],
    niche_revenue: Dict[str, float],
) -> PortfolioRisk:
    """Calculate all portfolio-level risk metrics from raw data.

    This is the main entry point. It orchestrates every risk calculation
    and returns a single PortfolioRisk dataclass with all fields populated.

    Args:
        positions: Objects with .revenue_total (float) and .method_id (str).
        revenue_history: Raw rows from REVENUE_TRACKER.csv. Each dict should
                         contain a 'revenue' key with a numeric string/float.
        platform_revenue: Revenue totals keyed by platform name
                          (e.g. {"TWITTER": 500.0, "GUMROAD": 300.0}).
        niche_revenue: Revenue totals keyed by niche name
                       (e.g. {"FAITH": 200.0, "TECH": 400.0}).

    Returns:
        Fully populated PortfolioRisk dataclass.
    """

    # ------------------------------------------------------------------
    # 1. METHOD CONCENTRATION (HHI)
    # ------------------------------------------------------------------
    total = sum(getattr(p, "revenue_total", 0) for p in positions)

    method_weights: List[float] = []
    max_method_name = ""
    max_method_pct = 0.0

    for p in positions:
        rev = getattr(p, "revenue_total", 0)
        if total > 0:
            pct = rev / total
            method_weights.append(pct)
            if pct > max_method_pct:
                max_method_pct = pct
                max_method_name = getattr(p, "method_id", "")

    hhi_method = calculate_hhi(method_weights) if method_weights else 0.0

    # ------------------------------------------------------------------
    # 2. PLATFORM CONCENTRATION
    # ------------------------------------------------------------------
    platform_weights = list(platform_revenue.values())
    hhi_platform = calculate_hhi(platform_weights) if platform_weights else 0.0

    max_platform = ""
    max_platform_pct = 0.0
    total_platform = sum(platform_weights) if platform_weights else 0

    if total_platform > 0:
        for plat, rev in platform_revenue.items():
            pct = rev / total_platform
            if pct > max_platform_pct:
                max_platform_pct = pct
                max_platform = plat

    # ------------------------------------------------------------------
    # 3. NICHE CONCENTRATION
    # ------------------------------------------------------------------
    niche_weights = list(niche_revenue.values())
    hhi_niche = calculate_hhi(niche_weights) if niche_weights else 0.0

    # ------------------------------------------------------------------
    # 4. EXTRACT REVENUE TIME SERIES
    # ------------------------------------------------------------------
    revenues: List[float] = []
    for row in revenue_history:
        try:
            revenue = float(row.get("revenue", 0) or 0)
            revenues.append(revenue)
        except (ValueError, TypeError, AttributeError):
            pass

    # ------------------------------------------------------------------
    # 5. SHARPE & SORTINO (with CI when < 12 months)
    # ------------------------------------------------------------------
    sharpe = 0.0
    sortino = 0.0
    sharpe_ci = (0.0, 0.0)
    data_months = len(revenues)
    returns: List[float] = []

    if len(revenues) >= 2:
        for i in range(1, len(revenues)):
            if revenues[i - 1] > 0:
                ret = (revenues[i] - revenues[i - 1]) / revenues[i - 1]
                returns.append(ret)
            elif revenues[i] > 0:
                returns.append(1.0)  # Growth from 0 = 100%

        if len(returns) >= 2:
            sharpe = calculate_sharpe_ratio(returns)
            sortino = calculate_sortino_ratio(returns)

            if data_months < 12:
                sharpe_ci = calculate_sharpe_confidence_interval(returns, sharpe)

    # ------------------------------------------------------------------
    # 6. MAXIMUM DRAWDOWN
    # ------------------------------------------------------------------
    max_dd, current_dd, dd_duration = calculate_max_drawdown(revenues)

    # ------------------------------------------------------------------
    # 7. VALUE AT RISK (Parametric + Historical)
    # ------------------------------------------------------------------
    var_95_param = 0.0
    var_99_param = 0.0
    var_95_hist = 0.0
    var_99_hist = 0.0

    if len(returns) >= 2:
        var_95_param = calculate_parametric_var(returns, 0.95)
        var_99_param = calculate_parametric_var(returns, 0.99)

    if len(returns) >= 20:
        var_95_hist = calculate_historical_var(returns, 0.95)
        var_99_hist = calculate_historical_var(returns, 0.99)

    # ------------------------------------------------------------------
    # 8. CONDITIONAL VAR (Expected Shortfall)
    # ------------------------------------------------------------------
    cvar_95 = 0.0
    cvar_99 = 0.0

    if len(returns) >= 2:
        cvar_95 = calculate_cvar(returns, 0.95)
        cvar_99 = calculate_cvar(returns, 0.99)

    # ------------------------------------------------------------------
    # 9. BETA -- no market proxy available yet
    # ------------------------------------------------------------------
    beta_val = 0.0
    beta_conf = "NO_MARKET_DATA"

    # ------------------------------------------------------------------
    # 10. INFORMATION COEFFICIENT -- no deployed alpha tracked yet
    # ------------------------------------------------------------------
    ic_val = 0.0
    ic_hr = 0.0
    ic_n = 0

    # ------------------------------------------------------------------
    # BUILD RESULT
    # ------------------------------------------------------------------
    return PortfolioRisk(
        total_revenue=total,
        portfolio_sharpe=sharpe,
        portfolio_sortino=sortino,
        sharpe_ci=sharpe_ci,
        sharpe_data_months=data_months,
        var_95=var_95_param,
        var_99=var_99_param,
        var_95_historical=var_95_hist,
        var_99_historical=var_99_hist,
        cvar_95=cvar_95,
        cvar_99=cvar_99,
        max_drawdown=max_dd,
        current_drawdown=current_dd,
        drawdown_duration=dd_duration,
        hhi_method=hhi_method,
        hhi_platform=hhi_platform,
        hhi_niche=hhi_niche,
        concentration_max_method=(max_method_name, round(max_method_pct * 100, 2)),
        concentration_max_platform=(max_platform, round(max_platform_pct * 100, 2)),
        beta=beta_val,
        beta_confidence=beta_conf,
        ic=ic_val,
        ic_hit_rate=ic_hr,
        ic_sample_size=ic_n,
    )
