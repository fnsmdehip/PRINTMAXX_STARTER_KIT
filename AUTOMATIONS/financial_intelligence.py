#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Financial Intelligence Engine
=========================================
Hedge-fund-grade financial tracking and analysis.

Reads all CSV trackers, runs Monte Carlo simulations, Kelly Criterion
capital allocation, and Markowitz-style portfolio optimization.

Usage:
    python3 AUTOMATIONS/financial_intelligence.py --dashboard
    python3 AUTOMATIONS/financial_intelligence.py --pnl
    python3 AUTOMATIONS/financial_intelligence.py --projection 12
    python3 AUTOMATIONS/financial_intelligence.py --allocate 5000
    python3 AUTOMATIONS/financial_intelligence.py --kelly
    python3 AUTOMATIONS/financial_intelligence.py --monte-carlo
"""

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

try:
    import numpy as np
except ImportError:
    print("ERROR: numpy required. Install with: pip3 install numpy")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent.parent
FINANCIALS = BASE_DIR / "FINANCIALS"
REVENUE_CSV = FINANCIALS / "REVENUE_TRACKER.csv"
EXPENSE_CSV = FINANCIALS / "EXPENSE_TRACKER.csv"
LEDGER = BASE_DIR / "LEDGER"
METHODS_CSV = LEDGER / "MEGA_SHEET" / "TAB1_MONEY_METHODS_MASTER.csv"


# ---------------------------------------------------------------------------
# Data loading utilities
# ---------------------------------------------------------------------------

def safe_float(val, default=0.0):
    """Parse a float from a string, stripping $ and commas."""
    if val is None:
        return default
    s = str(val).strip().replace("$", "").replace(",", "")
    if not s:
        return default
    try:
        return float(s)
    except (ValueError, TypeError):
        return default


def load_csv(path):
    """Load a CSV file into a list of dicts. Returns [] on failure."""
    if not path.exists():
        return []
    rows = []
    try:
        with open(path, "r", newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except Exception:
        pass
    return rows


def load_revenue():
    """Load revenue tracker. Returns list of dicts with parsed fields."""
    rows = load_csv(REVENUE_CSV)
    parsed = []
    for r in rows:
        try:
            d = datetime.strptime(r.get("date", ""), "%Y-%m-%d").date()
        except (ValueError, KeyError):
            continue
        parsed.append({
            "date": d,
            "method_id": r.get("method_id", "UNKNOWN"),
            "method_name": r.get("method_name", r.get("method_id", "UNKNOWN")),
            "revenue": safe_float(r.get("revenue")),
            "expenses": safe_float(r.get("expenses")),
            "profit": safe_float(r.get("profit")),
            "source": r.get("source", ""),
            "notes": r.get("notes", ""),
        })
    return parsed


def load_expenses():
    """Load expense tracker. Returns list of dicts with parsed fields."""
    rows = load_csv(EXPENSE_CSV)
    parsed = []
    for r in rows:
        try:
            d = datetime.strptime(r.get("date", ""), "%Y-%m-%d").date()
        except (ValueError, KeyError):
            continue
        parsed.append({
            "date": d,
            "category": r.get("category", "UNCATEGORIZED"),
            "item": r.get("item", ""),
            "amount": safe_float(r.get("amount")),
            "recurring": r.get("recurring", "FALSE").upper() == "TRUE",
            "frequency": r.get("frequency", "one-time"),
            "method_id": r.get("method_id", ""),
            "notes": r.get("notes", ""),
        })
    return parsed


def load_all_financials():
    """Load and merge revenue + expenses for unified analysis."""
    revenue = load_revenue()
    expenses = load_expenses()
    return revenue, expenses


# ---------------------------------------------------------------------------
# P&L per venture/op
# ---------------------------------------------------------------------------

def compute_pnl(revenue_rows, expense_rows):
    """Compute P&L per method/venture and overall."""
    # Revenue by method
    method_rev = defaultdict(lambda: {"revenue": 0.0, "expenses": 0.0, "profit": 0.0, "txns": 0})
    for r in revenue_rows:
        mid = r["method_id"]
        method_rev[mid]["revenue"] += r["revenue"]
        method_rev[mid]["expenses"] += r["expenses"]
        method_rev[mid]["profit"] += r["profit"]
        method_rev[mid]["txns"] += 1

    # Expenses by method
    method_exp = defaultdict(float)
    unattributed_exp = 0.0
    for e in expense_rows:
        mid = e["method_id"]
        if mid:
            method_exp[mid] += e["amount"]
        else:
            unattributed_exp += e["amount"]

    # Merge
    all_methods = set(method_rev.keys()) | set(method_exp.keys())
    pnl = {}
    for m in sorted(all_methods):
        rev = method_rev[m]["revenue"]
        direct_exp = method_rev[m]["expenses"]
        overhead_exp = method_exp.get(m, 0.0)
        total_exp = direct_exp + overhead_exp
        profit = rev - total_exp
        margin = (profit / rev * 100) if rev > 0 else 0.0
        pnl[m] = {
            "revenue": rev,
            "direct_expenses": direct_exp,
            "overhead_expenses": overhead_exp,
            "total_expenses": total_exp,
            "profit": profit,
            "margin": margin,
            "txns": method_rev[m]["txns"],
        }

    total_rev = sum(d["revenue"] for d in pnl.values())
    total_exp = sum(d["total_expenses"] for d in pnl.values()) + unattributed_exp
    total_profit = total_rev - total_exp

    return pnl, {
        "total_revenue": total_rev,
        "total_expenses": total_exp,
        "total_profit": total_profit,
        "unattributed_expenses": unattributed_exp,
        "margin": (total_profit / total_rev * 100) if total_rev > 0 else 0.0,
    }


# ---------------------------------------------------------------------------
# Revenue attribution
# ---------------------------------------------------------------------------

def compute_attribution(revenue_rows):
    """Attribute revenue to sources and methods."""
    by_source = defaultdict(lambda: {"revenue": 0.0, "count": 0, "methods": set()})
    by_method_source = defaultdict(lambda: defaultdict(float))

    for r in revenue_rows:
        src = r["source"] or "DIRECT"
        mid = r["method_id"]
        by_source[src]["revenue"] += r["revenue"]
        by_source[src]["count"] += 1
        by_source[src]["methods"].add(mid)
        by_method_source[mid][src] += r["revenue"]

    return by_source, by_method_source


# ---------------------------------------------------------------------------
# CAC calculation
# ---------------------------------------------------------------------------

def compute_cac(revenue_rows, expense_rows):
    """Calculate customer acquisition cost per method.

    CAC = (total expenses for method) / (number of revenue transactions).
    Time invested is estimated from transaction frequency.
    """
    method_expenses = defaultdict(float)
    method_txns = defaultdict(int)

    for r in revenue_rows:
        method_txns[r["method_id"]] += 1

    for r in revenue_rows:
        method_expenses[r["method_id"]] += r["expenses"]

    for e in expense_rows:
        if e["method_id"]:
            method_expenses[e["method_id"]] += e["amount"]

    cac = {}
    for mid in sorted(set(method_expenses.keys()) | set(method_txns.keys())):
        txns = method_txns.get(mid, 0)
        exp = method_expenses.get(mid, 0.0)
        cac[mid] = {
            "total_cost": exp,
            "transactions": txns,
            "cac": (exp / txns) if txns > 0 else exp,
            "efficiency": "HIGH" if txns > 0 and (exp / txns) < 50 else
                          "MEDIUM" if txns > 0 and (exp / txns) < 200 else "LOW",
        }
    return cac


# ---------------------------------------------------------------------------
# LTV projection
# ---------------------------------------------------------------------------

def compute_ltv(revenue_rows):
    """Project lifetime value per customer type (source/method combo).

    Uses average revenue per transaction * estimated retention (based on
    repeat transaction frequency).
    """
    # Group by source+method to identify customer types
    customer_types = defaultdict(lambda: {"revenues": [], "dates": []})
    for r in revenue_rows:
        key = f"{r['method_id']}|{r['source'] or 'DIRECT'}"
        customer_types[key]["revenues"].append(r["revenue"])
        customer_types[key]["dates"].append(r["date"])

    ltv = {}
    for key, data in sorted(customer_types.items()):
        revs = data["revenues"]
        dates = sorted(data["dates"])
        avg_rev = sum(revs) / len(revs) if revs else 0
        total_rev = sum(revs)

        # Estimate repeat rate: if multiple txns, compute avg gap
        if len(dates) > 1:
            gaps = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
            avg_gap = sum(gaps) / len(gaps) if gaps else 365
            # Estimated monthly transactions
            monthly_rate = 30.0 / max(avg_gap, 1)
            # Assume 12-month LTV window
            projected_ltv = avg_rev * monthly_rate * 12
            repeat = True
        else:
            projected_ltv = avg_rev  # single transaction, LTV = that transaction
            monthly_rate = 0
            repeat = False

        ltv[key] = {
            "avg_transaction": round(avg_rev, 2),
            "total_revenue": round(total_rev, 2),
            "transactions": len(revs),
            "repeat_customer": repeat,
            "monthly_rate": round(monthly_rate, 2),
            "projected_12mo_ltv": round(projected_ltv, 2),
        }
    return ltv


# ---------------------------------------------------------------------------
# Burn rate tracking
# ---------------------------------------------------------------------------

def compute_burn_rate(expense_rows):
    """Track monthly burn rate by category. Identifies recurring costs."""
    monthly = defaultdict(lambda: defaultdict(float))
    recurring_items = []

    for e in expense_rows:
        month_key = e["date"].strftime("%Y-%m")
        monthly[month_key][e["category"]] += e["amount"]
        monthly[month_key]["TOTAL"] += e["amount"]

        if e["recurring"]:
            # Annualize based on frequency
            freq = e["frequency"].lower()
            if "month" in freq:
                monthly_cost = e["amount"]
            elif "year" in freq:
                monthly_cost = e["amount"] / 12
            elif "week" in freq:
                monthly_cost = e["amount"] * 4.33
            elif "quarter" in freq:
                monthly_cost = e["amount"] / 3
            else:
                monthly_cost = e["amount"]

            recurring_items.append({
                "item": e["item"],
                "category": e["category"],
                "monthly_cost": round(monthly_cost, 2),
                "frequency": e["frequency"],
                "raw_amount": e["amount"],
            })

    # Sort months
    sorted_months = sorted(monthly.keys())

    # Average monthly burn (last 3 months or all available)
    recent = sorted_months[-3:] if len(sorted_months) >= 3 else sorted_months
    avg_burn = sum(monthly[m]["TOTAL"] for m in recent) / len(recent) if recent else 0

    # Recurring monthly total
    recurring_monthly = sum(r["monthly_cost"] for r in recurring_items)

    return {
        "monthly_breakdown": dict(monthly),
        "avg_monthly_burn": round(avg_burn, 2),
        "recurring_monthly": round(recurring_monthly, 2),
        "recurring_items": sorted(recurring_items, key=lambda x: x["monthly_cost"], reverse=True),
        "months_tracked": len(sorted_months),
    }


# ---------------------------------------------------------------------------
# Monte Carlo simulation for revenue projections
# ---------------------------------------------------------------------------

def monte_carlo_projection(revenue_rows, months=12, n_simulations=1000):
    """Run Monte Carlo simulation for revenue projections.

    Uses historical monthly revenue to parameterize log-normal distribution.
    Returns percentile bands (P10, P25, P50, P75, P90) for each future month.
    """
    # Aggregate monthly revenue
    monthly_rev = defaultdict(float)
    for r in revenue_rows:
        key = r["date"].strftime("%Y-%m")
        monthly_rev[key] += r["revenue"]

    sorted_months = sorted(monthly_rev.keys())
    if len(sorted_months) < 1:
        return None

    values = [monthly_rev[m] for m in sorted_months]

    # If we only have one month, use it as baseline with assumed volatility
    if len(values) == 1:
        mean_rev = values[0]
        std_rev = mean_rev * 0.3  # assume 30% volatility
    else:
        mean_rev = float(np.mean(values))
        std_rev = float(np.std(values, ddof=1))

    # Prevent zero std
    if std_rev < 0.01:
        std_rev = mean_rev * 0.2 if mean_rev > 0 else 100.0

    # Growth rate estimation (simple linear)
    if len(values) >= 2:
        growth_rates = []
        for i in range(1, len(values)):
            if values[i-1] > 0:
                growth_rates.append((values[i] - values[i-1]) / values[i-1])
        avg_growth = float(np.mean(growth_rates)) if growth_rates else 0.0
    else:
        avg_growth = 0.05  # assume 5% monthly growth for new ops

    # Cap growth rate to prevent insane projections
    avg_growth = max(-0.5, min(avg_growth, 1.0))

    np.random.seed(42)
    simulations = np.zeros((n_simulations, months))

    for sim in range(n_simulations):
        current = mean_rev
        for m in range(months):
            # Apply growth + random noise (normal distribution)
            noise = np.random.normal(0, std_rev)
            current = max(0, current * (1 + avg_growth) + noise)
            simulations[sim, m] = current

    # Compute percentiles
    percentiles = {}
    for p in [10, 25, 50, 75, 90]:
        percentiles[f"P{p}"] = [round(float(v), 2) for v in np.percentile(simulations, p, axis=0)]

    # Summary stats
    final_month = simulations[:, -1]
    cumulative = np.sum(simulations, axis=1)

    return {
        "months_projected": months,
        "simulations": n_simulations,
        "historical_mean": round(mean_rev, 2),
        "historical_std": round(std_rev, 2),
        "estimated_growth": round(avg_growth * 100, 1),
        "percentiles": percentiles,
        "final_month_stats": {
            "P10": round(float(np.percentile(final_month, 10)), 2),
            "P25": round(float(np.percentile(final_month, 25)), 2),
            "P50": round(float(np.percentile(final_month, 50)), 2),
            "P75": round(float(np.percentile(final_month, 75)), 2),
            "P90": round(float(np.percentile(final_month, 90)), 2),
            "mean": round(float(np.mean(final_month)), 2),
        },
        "cumulative_stats": {
            "P10": round(float(np.percentile(cumulative, 10)), 2),
            "P50": round(float(np.percentile(cumulative, 50)), 2),
            "P90": round(float(np.percentile(cumulative, 90)), 2),
            "mean": round(float(np.mean(cumulative)), 2),
        },
    }


# ---------------------------------------------------------------------------
# Kelly Criterion for capital allocation
# ---------------------------------------------------------------------------

def kelly_criterion(revenue_rows, expense_rows):
    """Apply Kelly Criterion to determine optimal capital allocation.

    For each method:
      - p = win rate (profitable transactions / total transactions)
      - b = avg win / avg loss ratio
      - Kelly% = p - (1 - p) / b

    Capped at half-Kelly for safety.
    """
    method_data = defaultdict(lambda: {"wins": [], "losses": []})

    for r in revenue_rows:
        mid = r["method_id"]
        if r["profit"] > 0:
            method_data[mid]["wins"].append(r["profit"])
        elif r["profit"] < 0:
            method_data[mid]["losses"].append(abs(r["profit"]))
        # Zero profit ignored

    # Include expense-only methods as all-loss
    method_costs = defaultdict(float)
    for e in expense_rows:
        if e["method_id"]:
            method_costs[e["method_id"]] += e["amount"]

    for mid, cost in method_costs.items():
        if mid not in method_data or (not method_data[mid]["wins"] and not method_data[mid]["losses"]):
            method_data[mid]["losses"].append(cost)

    kelly = {}
    for mid, data in sorted(method_data.items()):
        wins = data["wins"]
        losses = data["losses"]
        total = len(wins) + len(losses)

        if total == 0:
            continue

        p = len(wins) / total  # probability of winning
        q = 1 - p

        avg_win = float(np.mean(wins)) if wins else 0
        avg_loss = float(np.mean(losses)) if losses else 1

        # Win/loss ratio
        b = avg_win / avg_loss if avg_loss > 0 else float("inf")

        # Kelly formula: f* = p - q/b
        if b > 0 and b != float("inf"):
            kelly_pct = p - (q / b)
        elif b == float("inf"):
            kelly_pct = p  # no losses recorded
        else:
            kelly_pct = 0

        # Half-Kelly for safety
        half_kelly = kelly_pct / 2

        # Clamp
        kelly_pct = max(0, min(1, kelly_pct))
        half_kelly = max(0, min(0.5, half_kelly))

        kelly[mid] = {
            "win_rate": round(p * 100, 1),
            "avg_win": round(avg_win, 2),
            "avg_loss": round(avg_loss, 2),
            "win_loss_ratio": round(b, 2) if b != float("inf") else "INF",
            "kelly_pct": round(kelly_pct * 100, 1),
            "half_kelly_pct": round(half_kelly * 100, 1),
            "recommendation": (
                "AGGRESSIVE" if kelly_pct > 0.3 else
                "MODERATE" if kelly_pct > 0.1 else
                "CAUTIOUS" if kelly_pct > 0 else
                "AVOID"
            ),
            "total_bets": total,
        }

    return kelly


# ---------------------------------------------------------------------------
# Portfolio optimization (Markowitz efficient frontier)
# ---------------------------------------------------------------------------

def portfolio_optimization(revenue_rows, budget=None, n_portfolios=5000):
    """Markowitz-style efficient frontier for ops allocation.

    Treats each method as an asset. Uses monthly returns to compute
    expected return, variance, and covariance matrix. Generates random
    portfolios to approximate the efficient frontier.
    """
    # Monthly returns per method
    method_monthly = defaultdict(lambda: defaultdict(float))
    all_months = set()

    for r in revenue_rows:
        month_key = r["date"].strftime("%Y-%m")
        method_monthly[r["method_id"]][month_key] += r["profit"]
        all_months.add(month_key)

    sorted_months = sorted(all_months)
    methods = sorted(method_monthly.keys())

    if len(methods) < 2:
        return None  # Need at least 2 methods for portfolio optimization

    # Build return matrix: rows = months, cols = methods
    n_months = len(sorted_months)
    n_methods = len(methods)

    returns_matrix = np.zeros((n_months, n_methods))
    for j, mid in enumerate(methods):
        for i, month in enumerate(sorted_months):
            returns_matrix[i, j] = method_monthly[mid].get(month, 0.0)

    # Expected returns (mean of monthly returns)
    expected_returns = np.mean(returns_matrix, axis=0)

    # Covariance matrix
    if n_months > 1:
        cov_matrix = np.cov(returns_matrix, rowvar=False)
    else:
        # Single month: use diagonal with assumed variance
        variances = np.var(returns_matrix, axis=0)
        variances = np.where(variances == 0, 100, variances)
        cov_matrix = np.diag(variances)

    # Ensure cov_matrix is 2D
    if cov_matrix.ndim == 0:
        cov_matrix = np.array([[float(cov_matrix)]])
    elif cov_matrix.ndim == 1:
        cov_matrix = np.diag(cov_matrix)

    # Generate random portfolios
    np.random.seed(42)
    results = np.zeros((n_portfolios, 3 + n_methods))

    for i in range(n_portfolios):
        weights = np.random.dirichlet(np.ones(n_methods))
        port_return = np.dot(weights, expected_returns)
        port_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe = port_return / port_vol if port_vol > 0 else 0

        results[i, 0] = port_return
        results[i, 1] = port_vol
        results[i, 2] = sharpe
        results[i, 3:] = weights

    # Find optimal portfolios
    max_sharpe_idx = np.argmax(results[:, 2])
    min_vol_idx = np.argmin(results[:, 1])

    # Max return portfolio (highest return with acceptable risk)
    high_return_mask = results[:, 0] > np.percentile(results[:, 0], 90)
    if np.any(high_return_mask):
        high_return_indices = np.where(high_return_mask)[0]
        max_return_idx = high_return_indices[np.argmin(results[high_return_indices, 1])]
    else:
        max_return_idx = np.argmax(results[:, 0])

    def format_portfolio(idx, label):
        weights = results[idx, 3:]
        allocations = {}
        for j, mid in enumerate(methods):
            if weights[j] > 0.01:  # Only show > 1%
                allocations[mid] = round(float(weights[j]) * 100, 1)
        budget_alloc = {}
        if budget:
            for mid, pct in allocations.items():
                budget_alloc[mid] = round(budget * pct / 100, 2)
        return {
            "label": label,
            "expected_monthly_return": round(float(results[idx, 0]), 2),
            "volatility": round(float(results[idx, 1]), 2),
            "sharpe_ratio": round(float(results[idx, 2]), 4),
            "allocations_pct": allocations,
            "budget_allocations": budget_alloc if budget else None,
        }

    return {
        "methods": methods,
        "months_analyzed": n_months,
        "expected_returns": {mid: round(float(er), 2) for mid, er in zip(methods, expected_returns)},
        "max_sharpe": format_portfolio(max_sharpe_idx, "MAX_SHARPE"),
        "min_volatility": format_portfolio(min_vol_idx, "MIN_VOLATILITY"),
        "max_return": format_portfolio(max_return_idx, "MAX_RETURN"),
        "portfolios_simulated": n_portfolios,
    }


# ---------------------------------------------------------------------------
# Display functions
# ---------------------------------------------------------------------------

W = 76  # terminal width


def hr(char="="):
    return char * W


def print_header(title):
    print(hr())
    print(f"  {title}".center(W))
    print(hr())
    print()


def print_section(title):
    print(f"  {title}")
    print(f"  {'-' * (W - 4)}")


def cmd_dashboard():
    """Full financial dashboard."""
    revenue, expenses = load_all_financials()
    pnl, totals = compute_pnl(revenue, expenses)
    burn = compute_burn_rate(expenses)

    print_header("PRINTMAXX FINANCIAL INTELLIGENCE DASHBOARD")

    # Overall P&L
    print_section("OVERALL P&L")
    print(f"  Total Revenue:      ${totals['total_revenue']:>12,.2f}")
    print(f"  Total Expenses:     ${totals['total_expenses']:>12,.2f}")
    print(f"  Net Profit:         ${totals['total_profit']:>12,.2f}")
    print(f"  Margin:             {totals['margin']:>12.1f}%")
    print(f"  Unattributed Exp:   ${totals['unattributed_expenses']:>12,.2f}")
    print()

    # Burn rate
    print_section("BURN RATE")
    print(f"  Avg Monthly Burn:   ${burn['avg_monthly_burn']:>12,.2f}")
    print(f"  Recurring Monthly:  ${burn['recurring_monthly']:>12,.2f}")
    if burn["recurring_items"]:
        print(f"  Top Recurring Costs:")
        for item in burn["recurring_items"][:5]:
            print(f"    ${item['monthly_cost']:>8,.2f}/mo  {item['item'][:40]}  ({item['frequency']})")
    print()

    # Revenue by method
    if pnl:
        print_section("P&L BY METHOD")
        print(f"  {'METHOD':<30} {'REVENUE':>10} {'EXPENSES':>10} {'PROFIT':>10} {'MARGIN':>7}")
        for mid, data in sorted(pnl.items(), key=lambda x: x[1]["profit"], reverse=True):
            print(f"  {mid:<30} ${data['revenue']:>9,.2f} ${data['total_expenses']:>9,.2f} "
                  f"${data['profit']:>9,.2f} {data['margin']:>6.1f}%")
    print()

    # Quick Monte Carlo preview
    mc = monte_carlo_projection(revenue, months=6, n_simulations=500)
    if mc:
        print_section("6-MONTH REVENUE PROJECTION (500 simulations)")
        print(f"  Historical Mean:    ${mc['historical_mean']:>12,.2f}/mo")
        print(f"  Growth Estimate:    {mc['estimated_growth']:>12.1f}%/mo")
        fs = mc["final_month_stats"]
        print(f"  Month 6 Forecast:   P10=${fs['P10']:,.0f}  P50=${fs['P50']:,.0f}  P90=${fs['P90']:,.0f}")
        cs = mc["cumulative_stats"]
        print(f"  6-Month Cumulative: P10=${cs['P10']:,.0f}  P50=${cs['P50']:,.0f}  P90=${cs['P90']:,.0f}")
    print()

    # Kelly quick view
    kelly = kelly_criterion(revenue, expenses)
    if kelly:
        print_section("KELLY CRITERION (Capital Allocation Signal)")
        print(f"  {'METHOD':<30} {'WIN%':>6} {'KELLY%':>8} {'HALF-K%':>8} {'SIGNAL':<10}")
        for mid, data in sorted(kelly.items(), key=lambda x: x[1]["half_kelly_pct"], reverse=True):
            print(f"  {mid:<30} {data['win_rate']:>5.1f}% {data['kelly_pct']:>7.1f}% "
                  f"{data['half_kelly_pct']:>7.1f}% {data['recommendation']:<10}")

    print()
    print(hr())
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(hr())


def cmd_pnl():
    """Detailed P&L report."""
    revenue, expenses = load_all_financials()
    pnl, totals = compute_pnl(revenue, expenses)
    attribution_src, attribution_method = compute_attribution(revenue)
    cac = compute_cac(revenue, expenses)
    ltv = compute_ltv(revenue)

    print_header("PROFIT & LOSS REPORT")

    # Overall
    print_section("CONSOLIDATED P&L")
    print(f"  Revenue:            ${totals['total_revenue']:>12,.2f}")
    print(f"  COGS/Direct:        ${sum(d['direct_expenses'] for d in pnl.values()):>12,.2f}")
    gross = totals['total_revenue'] - sum(d['direct_expenses'] for d in pnl.values())
    print(f"  Gross Profit:       ${gross:>12,.2f}")
    print(f"  Overhead:           ${sum(d['overhead_expenses'] for d in pnl.values()):>12,.2f}")
    print(f"  Unattributed:       ${totals['unattributed_expenses']:>12,.2f}")
    print(f"  Net Profit:         ${totals['total_profit']:>12,.2f}")
    print(f"  Net Margin:         {totals['margin']:>12.1f}%")
    print()

    # Per method detail
    print_section("PER-METHOD DETAIL")
    for mid, data in sorted(pnl.items(), key=lambda x: x[1]["revenue"], reverse=True):
        if data["revenue"] == 0 and data["total_expenses"] == 0:
            continue
        print(f"\n  {mid}")
        print(f"    Revenue:        ${data['revenue']:>10,.2f}  ({data['txns']} transactions)")
        print(f"    Direct Costs:   ${data['direct_expenses']:>10,.2f}")
        print(f"    Overhead:       ${data['overhead_expenses']:>10,.2f}")
        print(f"    Net Profit:     ${data['profit']:>10,.2f}  (margin: {data['margin']:.1f}%)")
    print()

    # Revenue attribution
    print_section("REVENUE ATTRIBUTION BY SOURCE")
    for src, data in sorted(attribution_src.items(), key=lambda x: x[1]["revenue"], reverse=True):
        methods_str = ", ".join(sorted(data["methods"]))
        print(f"  {src:<30} ${data['revenue']:>10,.2f}  ({data['count']} txns)  Methods: {methods_str}")
    print()

    # CAC
    print_section("CUSTOMER ACQUISITION COST")
    print(f"  {'METHOD':<30} {'TOTAL COST':>10} {'TXNS':>6} {'CAC':>10} {'EFF':>6}")
    for mid, data in sorted(cac.items(), key=lambda x: x[1]["cac"]):
        print(f"  {mid:<30} ${data['total_cost']:>9,.2f} {data['transactions']:>6} "
              f"${data['cac']:>9,.2f} {data['efficiency']:>6}")
    print()

    # LTV
    print_section("LIFETIME VALUE PROJECTIONS")
    print(f"  {'TYPE':<40} {'AVG TXN':>8} {'12MO LTV':>10} {'RPT':>4}")
    for key, data in sorted(ltv.items(), key=lambda x: x[1]["projected_12mo_ltv"], reverse=True):
        rpt = "Y" if data["repeat_customer"] else "N"
        print(f"  {key:<40} ${data['avg_transaction']:>7,.2f} ${data['projected_12mo_ltv']:>9,.2f} {rpt:>4}")

    print()
    print(hr())


def cmd_projection(months):
    """Monte Carlo revenue projection."""
    revenue = load_revenue()

    print_header(f"MONTE CARLO REVENUE PROJECTION ({months} MONTHS)")

    mc = monte_carlo_projection(revenue, months=months, n_simulations=1000)
    if not mc:
        print("  No revenue data available for projection.")
        print(hr())
        return

    print_section("SIMULATION PARAMETERS")
    print(f"  Simulations:        {mc['simulations']:>10,}")
    print(f"  Historical Mean:    ${mc['historical_mean']:>10,.2f}/mo")
    print(f"  Historical StdDev:  ${mc['historical_std']:>10,.2f}")
    print(f"  Growth Estimate:    {mc['estimated_growth']:>10.1f}%/mo")
    print()

    # ASCII chart of projection bands
    print_section("PROJECTION BANDS")
    p50 = mc["percentiles"]["P50"]
    p10 = mc["percentiles"]["P10"]
    p90 = mc["percentiles"]["P90"]

    max_val = max(p90) if p90 else 1
    chart_height = 12
    chart_width = min(months, 60)

    # Scale months to chart width
    if months > chart_width:
        step = months / chart_width
        indices = [int(i * step) for i in range(chart_width)]
    else:
        indices = list(range(months))
        chart_width = months

    for row in range(chart_height, 0, -1):
        threshold = (row / chart_height) * max_val
        if row == chart_height:
            label = f"${max_val:>8,.0f} "
        elif row == 1:
            label = f"${'0':>8} "
        else:
            label = " " * 10

        line = label + "|"
        for idx in indices:
            v90 = p90[idx]
            v50 = p50[idx]
            v10 = p10[idx]
            bar_90 = (v90 / max_val) * chart_height if max_val > 0 else 0
            bar_50 = (v50 / max_val) * chart_height if max_val > 0 else 0
            bar_10 = (v10 / max_val) * chart_height if max_val > 0 else 0

            if bar_90 >= row and bar_50 >= row:
                line += "#"
            elif bar_90 >= row:
                line += ":"
            elif bar_10 >= row:
                line += "."
            else:
                line += " "
        print(line)

    print(" " * 10 + "+" + "-" * chart_width)
    print(f"  {'Legend: # = P50 (median)  : = P90 (optimistic)  . = P10 (pessimistic)'}")
    print()

    # Monthly table
    print_section("MONTHLY FORECAST TABLE")
    print(f"  {'MONTH':>6} {'P10':>10} {'P25':>10} {'P50':>10} {'P75':>10} {'P90':>10}")
    for m in range(months):
        month_label = (datetime.now().date().replace(day=1) + timedelta(days=32 * (m + 1))).strftime("%b %y")
        print(f"  {month_label:>6} "
              f"${mc['percentiles']['P10'][m]:>9,.0f} "
              f"${mc['percentiles']['P25'][m]:>9,.0f} "
              f"${mc['percentiles']['P50'][m]:>9,.0f} "
              f"${mc['percentiles']['P75'][m]:>9,.0f} "
              f"${mc['percentiles']['P90'][m]:>9,.0f}")
    print()

    # Final month summary
    print_section(f"MONTH {months} FORECAST")
    fs = mc["final_month_stats"]
    print(f"  Pessimistic (P10):  ${fs['P10']:>12,.2f}")
    print(f"  Conservative (P25): ${fs['P25']:>12,.2f}")
    print(f"  Expected (P50):     ${fs['P50']:>12,.2f}")
    print(f"  Optimistic (P75):   ${fs['P75']:>12,.2f}")
    print(f"  Best Case (P90):    ${fs['P90']:>12,.2f}")
    print(f"  Mean:               ${fs['mean']:>12,.2f}")
    print()

    # Cumulative
    print_section(f"CUMULATIVE {months}-MONTH REVENUE")
    cs = mc["cumulative_stats"]
    print(f"  Pessimistic (P10):  ${cs['P10']:>12,.2f}")
    print(f"  Expected (P50):     ${cs['P50']:>12,.2f}")
    print(f"  Best Case (P90):    ${cs['P90']:>12,.2f}")
    print(f"  Mean:               ${cs['mean']:>12,.2f}")

    print()
    print(hr())


def cmd_allocate(budget):
    """Portfolio optimization with budget allocation."""
    revenue = load_revenue()

    print_header(f"PORTFOLIO OPTIMIZATION (Budget: ${budget:,.2f})")

    result = portfolio_optimization(revenue, budget=budget)
    if not result:
        print("  Need at least 2 methods with revenue data for portfolio optimization.")
        print("  Log more revenue entries to enable this feature.")
        print(hr())
        return

    print_section("METHODS ANALYZED")
    for mid in result["methods"]:
        er = result["expected_returns"][mid]
        print(f"  {mid:<30} Expected Monthly Return: ${er:>10,.2f}")
    print(f"  Months of data: {result['months_analyzed']}")
    print(f"  Portfolios simulated: {result['portfolios_simulated']:,}")
    print()

    for portfolio_key in ["max_sharpe", "min_volatility", "max_return"]:
        p = result[portfolio_key]
        print_section(f"PORTFOLIO: {p['label']}")
        print(f"  Expected Monthly Return:  ${p['expected_monthly_return']:>10,.2f}")
        print(f"  Volatility (Risk):        ${p['volatility']:>10,.2f}")
        print(f"  Sharpe Ratio:             {p['sharpe_ratio']:>10.4f}")
        print(f"  Allocations:")
        for mid, pct in sorted(p["allocations_pct"].items(), key=lambda x: x[1], reverse=True):
            bar = "#" * int(pct / 2)
            budget_str = ""
            if p["budget_allocations"] and mid in p["budget_allocations"]:
                budget_str = f"  (${p['budget_allocations'][mid]:,.2f})"
            print(f"    {mid:<25} {pct:>5.1f}% {bar}{budget_str}")
        print()

    print(hr())


def cmd_kelly():
    """Kelly Criterion analysis."""
    revenue, expenses = load_all_financials()

    print_header("KELLY CRITERION CAPITAL ALLOCATION")

    kelly = kelly_criterion(revenue, expenses)
    if not kelly:
        print("  No transaction data available for Kelly analysis.")
        print(hr())
        return

    print_section("METHODOLOGY")
    print("  Kelly% = p - (1-p)/b  where p=win rate, b=win/loss ratio")
    print("  Half-Kelly used for safety (halves optimal bet size)")
    print("  Recommendation: allocate Half-Kelly% of capital to each method")
    print()

    print_section("KELLY ANALYSIS BY METHOD")
    print(f"  {'METHOD':<25} {'BETS':>5} {'WIN%':>6} {'AVG W':>8} {'AVG L':>8} {'W/L':>6} {'KELLY':>7} {'HALF-K':>7} {'SIGNAL':<10}")
    for mid, data in sorted(kelly.items(), key=lambda x: x[1]["half_kelly_pct"], reverse=True):
        wl = data["win_loss_ratio"]
        wl_str = f"{wl:>5.2f}" if isinstance(wl, float) else f"{wl:>5}"
        print(f"  {mid:<25} {data['total_bets']:>5} {data['win_rate']:>5.1f}% "
              f"${data['avg_win']:>7,.2f} ${data['avg_loss']:>7,.2f} {wl_str} "
              f"{data['kelly_pct']:>6.1f}% {data['half_kelly_pct']:>6.1f}% {data['recommendation']:<10}")
    print()

    # Allocation example
    total_kelly = sum(d["half_kelly_pct"] for d in kelly.values())
    if total_kelly > 0:
        print_section("NORMALIZED ALLOCATION (for $1000 example)")
        for mid, data in sorted(kelly.items(), key=lambda x: x[1]["half_kelly_pct"], reverse=True):
            if data["half_kelly_pct"] > 0:
                normalized = data["half_kelly_pct"] / total_kelly * 100
                amount = 1000 * normalized / 100
                bar = "#" * int(normalized / 2)
                print(f"  {mid:<25} {normalized:>5.1f}%  ${amount:>7,.2f}  {bar}")

    print()
    print(hr())


def cmd_monte_carlo():
    """Detailed Monte Carlo analysis with per-method breakdown."""
    revenue = load_revenue()

    print_header("MONTE CARLO SIMULATION ENGINE")

    # Overall projection
    mc = monte_carlo_projection(revenue, months=12, n_simulations=1000)
    if not mc:
        print("  No revenue data for simulation.")
        print(hr())
        return

    print_section("AGGREGATE 12-MONTH PROJECTION (1000 simulations)")
    print(f"  Historical Mean:    ${mc['historical_mean']:>10,.2f}/mo")
    print(f"  Growth Rate:        {mc['estimated_growth']:>10.1f}%/mo")
    print(f"  Volatility:         ${mc['historical_std']:>10,.2f}")
    print()

    # Risk metrics
    cs = mc["cumulative_stats"]
    expected = cs["P50"]
    downside = cs["P10"]
    var_95 = expected - downside
    print_section("RISK METRICS")
    print(f"  Expected 12mo Rev:  ${expected:>12,.2f}")
    print(f"  Value at Risk (P10):${var_95:>12,.2f}")
    print(f"  Downside Scenario:  ${downside:>12,.2f}")
    print(f"  Upside Scenario:    ${cs['P90']:>12,.2f}")
    print(f"  Upside/Downside:    {cs['P90']/max(downside,1):>12.2f}x")
    print()

    # Per-method simulation
    method_revenue = defaultdict(list)
    for r in revenue:
        method_revenue[r["method_id"]].append(r)

    if len(method_revenue) > 1:
        print_section("PER-METHOD PROJECTIONS (12 months)")
        print(f"  {'METHOD':<30} {'HIST/MO':>8} {'P10':>10} {'P50':>10} {'P90':>10}")
        for mid, rows in sorted(method_revenue.items()):
            method_mc = monte_carlo_projection(rows, months=12, n_simulations=500)
            if method_mc:
                fs = method_mc["final_month_stats"]
                print(f"  {mid:<30} ${method_mc['historical_mean']:>7,.0f} "
                      f"${fs['P10']:>9,.0f} ${fs['P50']:>9,.0f} ${fs['P90']:>9,.0f}")
        print()

    # Scenario analysis
    print_section("SCENARIO ANALYSIS")
    scenarios = [
        ("Bear Case (recession, -20% growth)", -0.20),
        ("Base Case (current trajectory)", 0),
        ("Bull Case (scaling, +20% growth)", 0.20),
        ("Moonshot (viral, +50% growth)", 0.50),
    ]

    monthly_rev = defaultdict(float)
    for r in revenue:
        key = r["date"].strftime("%Y-%m")
        monthly_rev[key] += r["revenue"]

    values = list(monthly_rev.values())
    base_mean = float(np.mean(values)) if values else 0
    base_std = float(np.std(values, ddof=1)) if len(values) > 1 else base_mean * 0.3

    np.random.seed(42)
    for label, growth_adj in scenarios:
        sims = np.zeros((500, 12))
        for s in range(500):
            current = base_mean
            for m in range(12):
                noise = np.random.normal(0, base_std)
                adj_growth = 0.05 + growth_adj / 12  # base + adjustment
                current = max(0, current * (1 + adj_growth) + noise)
                sims[s, m] = current
        cumulative = np.sum(sims, axis=1)
        p50 = float(np.percentile(cumulative, 50))
        print(f"  {label}")
        print(f"    12-Month Revenue: ${p50:>12,.2f}")

    print()
    print(hr())
    print(f"  Simulation complete: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(hr())


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Financial Intelligence Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 AUTOMATIONS/financial_intelligence.py --dashboard
  python3 AUTOMATIONS/financial_intelligence.py --pnl
  python3 AUTOMATIONS/financial_intelligence.py --projection 12
  python3 AUTOMATIONS/financial_intelligence.py --allocate 5000
  python3 AUTOMATIONS/financial_intelligence.py --kelly
  python3 AUTOMATIONS/financial_intelligence.py --monte-carlo
        """,
    )
    parser.add_argument("--dashboard", action="store_true", help="Full financial dashboard")
    parser.add_argument("--pnl", action="store_true", help="Detailed P&L report")
    parser.add_argument("--projection", type=int, metavar="MONTHS", help="Monte Carlo revenue projection")
    parser.add_argument("--allocate", type=float, metavar="BUDGET", help="Portfolio optimization with budget")
    parser.add_argument("--kelly", action="store_true", help="Kelly Criterion analysis")
    parser.add_argument("--monte-carlo", action="store_true", help="Full Monte Carlo simulation")

    args = parser.parse_args()

    if args.dashboard:
        cmd_dashboard()
    elif args.pnl:
        cmd_pnl()
    elif args.projection:
        cmd_projection(args.projection)
    elif args.allocate is not None:
        cmd_allocate(args.allocate)
    elif args.kelly:
        cmd_kelly()
    elif args.monte_carlo:
        cmd_monte_carlo()
    else:
        cmd_dashboard()


if __name__ == "__main__":
    main()
