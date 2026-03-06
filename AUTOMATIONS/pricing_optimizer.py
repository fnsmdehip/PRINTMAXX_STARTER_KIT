#!/usr/bin/env python3
"""
PRINTMAXX Pricing Optimizer
=============================
Dynamic pricing intelligence for solopreneur products.

Scans competitor prices, calculates elasticity, generates A/B test
variants, and applies psychological pricing tactics.

Usage:
    python3 AUTOMATIONS/pricing_optimizer.py --scan gumroad
    python3 AUTOMATIONS/pricing_optimizer.py --optimize "Python Automation Pack"
    python3 AUTOMATIONS/pricing_optimizer.py --ab-test "Cold Email Templates"
    python3 AUTOMATIONS/pricing_optimizer.py --competitive-analysis
"""

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

try:
    import numpy as np
except ImportError:
    print("ERROR: numpy required. Install with: pip3 install numpy")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent.parent
FINANCIALS = BASE_DIR / "FINANCIALS"
REVENUE_CSV = FINANCIALS / "REVENUE_TRACKER.csv"
PRODUCTS_DIR = BASE_DIR / "PRODUCTS"
DIGITAL_DIR = BASE_DIR / "DIGITAL_PRODUCTS"
PRICING_CACHE = FINANCIALS / "pricing_cache.json"

W = 76


# ---------------------------------------------------------------------------
# Competitor price databases (reference data for offline analysis)
# ---------------------------------------------------------------------------

GUMROAD_BENCHMARKS = {
    "templates": {
        "low": 5, "median": 19, "high": 49, "premium": 99,
        "examples": [
            {"name": "Notion Template Pack", "price": 19, "tier": "starter"},
            {"name": "Cold Email Swipe File", "price": 27, "tier": "pro"},
            {"name": "Landing Page Templates", "price": 39, "tier": "pro"},
            {"name": "SaaS Boilerplate", "price": 49, "tier": "premium"},
            {"name": "Full Business Kit", "price": 79, "tier": "premium"},
        ],
    },
    "courses": {
        "low": 19, "median": 49, "high": 149, "premium": 299,
        "examples": [
            {"name": "Beginner Python Course", "price": 19, "tier": "starter"},
            {"name": "Freelance Mastery", "price": 49, "tier": "pro"},
            {"name": "Cold Outreach System", "price": 97, "tier": "pro"},
            {"name": "Full Stack Bootcamp", "price": 149, "tier": "premium"},
            {"name": "Agency Builder Program", "price": 297, "tier": "premium"},
        ],
    },
    "ebooks": {
        "low": 5, "median": 12, "high": 29, "premium": 49,
        "examples": [
            {"name": "Side Hustle Guide", "price": 7, "tier": "starter"},
            {"name": "Automation Playbook", "price": 14, "tier": "pro"},
            {"name": "Revenue Operations Manual", "price": 27, "tier": "pro"},
            {"name": "Enterprise Sales Bible", "price": 47, "tier": "premium"},
        ],
    },
    "tools": {
        "low": 9, "median": 29, "high": 79, "premium": 149,
        "examples": [
            {"name": "Spreadsheet Tracker", "price": 9, "tier": "starter"},
            {"name": "Python Script Bundle", "price": 29, "tier": "pro"},
            {"name": "Chrome Extension", "price": 49, "tier": "pro"},
            {"name": "Full SaaS Starter Kit", "price": 99, "tier": "premium"},
            {"name": "AI Agent Framework", "price": 149, "tier": "premium"},
        ],
    },
}

FIVERR_BENCHMARKS = {
    "web_development": {
        "basic": {"price": 50, "delivery": "3 days", "revisions": 1},
        "standard": {"price": 150, "delivery": "5 days", "revisions": 3},
        "premium": {"price": 400, "delivery": "7 days", "revisions": "unlimited"},
    },
    "data_scraping": {
        "basic": {"price": 25, "delivery": "1 day", "revisions": 1},
        "standard": {"price": 75, "delivery": "2 days", "revisions": 2},
        "premium": {"price": 200, "delivery": "3 days", "revisions": 3},
    },
    "automation": {
        "basic": {"price": 40, "delivery": "2 days", "revisions": 1},
        "standard": {"price": 120, "delivery": "4 days", "revisions": 2},
        "premium": {"price": 350, "delivery": "7 days", "revisions": 3},
    },
    "content_writing": {
        "basic": {"price": 20, "delivery": "1 day", "revisions": 1},
        "standard": {"price": 60, "delivery": "3 days", "revisions": 2},
        "premium": {"price": 150, "delivery": "5 days", "revisions": 3},
    },
    "graphic_design": {
        "basic": {"price": 30, "delivery": "2 days", "revisions": 2},
        "standard": {"price": 80, "delivery": "3 days", "revisions": 3},
        "premium": {"price": 200, "delivery": "5 days", "revisions": "unlimited"},
    },
}

UPWORK_BENCHMARKS = {
    "python_developer": {"low": 25, "median": 50, "high": 100, "expert": 150},
    "web_scraping": {"low": 20, "median": 40, "high": 75, "expert": 120},
    "automation_engineer": {"low": 30, "median": 55, "high": 100, "expert": 150},
    "data_analyst": {"low": 25, "median": 45, "high": 85, "expert": 130},
    "full_stack_dev": {"low": 30, "median": 60, "high": 120, "expert": 180},
    "ai_ml_engineer": {"low": 40, "median": 75, "high": 150, "expert": 250},
    "devops": {"low": 35, "median": 65, "high": 120, "expert": 175},
    "technical_writer": {"low": 20, "median": 40, "high": 70, "expert": 100},
}

SAAS_BENCHMARKS = {
    "micro_saas": {
        "free_tier": True,
        "starter": {"price": 9, "billing": "monthly"},
        "pro": {"price": 29, "billing": "monthly"},
        "business": {"price": 79, "billing": "monthly"},
    },
    "dev_tools": {
        "free_tier": True,
        "starter": {"price": 19, "billing": "monthly"},
        "pro": {"price": 49, "billing": "monthly"},
        "enterprise": {"price": 199, "billing": "monthly"},
    },
    "productivity": {
        "free_tier": True,
        "starter": {"price": 7, "billing": "monthly"},
        "pro": {"price": 15, "billing": "monthly"},
        "team": {"price": 25, "billing": "monthly", "per_user": True},
    },
}


# ---------------------------------------------------------------------------
# Price elasticity estimation
# ---------------------------------------------------------------------------

def estimate_elasticity(category, current_price):
    """Estimate price elasticity for a product category.

    Uses benchmark data to estimate how demand changes with price.
    Returns elasticity coefficient (negative = demand drops as price rises).

    Elasticity = -1.0 means 10% price increase = 10% demand decrease.
    Digital products typically range from -0.5 to -2.0.
    """
    benchmarks = GUMROAD_BENCHMARKS.get(category, GUMROAD_BENCHMARKS.get("tools"))

    low = benchmarks["low"]
    high = benchmarks["premium"]
    median = benchmarks["median"]

    # Position in price range (0 = lowest, 1 = highest)
    position = (current_price - low) / (high - low) if high != low else 0.5
    position = max(0, min(1, position))

    # Elasticity varies by position:
    # - Below median: less elastic (people are less price-sensitive at low prices)
    # - Above median: more elastic (demand drops faster at higher prices)
    if current_price <= median:
        elasticity = -0.5 - (position * 0.5)  # -0.5 to -1.0
    else:
        elasticity = -1.0 - ((position - 0.5) * 2.0)  # -1.0 to -2.0

    return round(elasticity, 2)


def demand_curve(base_price, base_demand, elasticity, price_range):
    """Generate demand curve points."""
    points = []
    for price in price_range:
        pct_change = (price - base_price) / base_price
        demand_change = 1 + (pct_change * elasticity)
        demand = max(0, base_demand * demand_change)
        revenue = price * demand
        points.append({
            "price": round(price, 2),
            "demand": round(demand, 1),
            "revenue": round(revenue, 2),
        })
    return points


def find_optimal_price(base_price, base_demand, elasticity, min_price, max_price):
    """Find revenue-maximizing price using calculus approach.

    Revenue = P * D(P) = P * D0 * (1 + e * (P-P0)/P0)
    dR/dP = 0 when P_optimal = P0 * (1 + 1/e) / 2 (approximately)
    """
    prices = np.linspace(min_price, max_price, 200)
    best_price = base_price
    best_revenue = 0

    for p in prices:
        pct_change = (p - base_price) / base_price if base_price > 0 else 0
        demand = max(0, base_demand * (1 + pct_change * elasticity))
        revenue = p * demand
        if revenue > best_revenue:
            best_revenue = revenue
            best_price = p

    return round(float(best_price), 2), round(float(best_revenue), 2)


# ---------------------------------------------------------------------------
# Psychological pricing tactics
# ---------------------------------------------------------------------------

def apply_charm_pricing(price):
    """Apply charm pricing (prices ending in 7 or 9).

    Research shows prices ending in 9 outsell rounded prices by 8-24%.
    Prices ending in 7 signal insider/premium pricing.
    """
    rounded = math.ceil(price)
    variants = []

    # .97 variant (insider pricing)
    p97 = rounded - 0.03 if rounded > price else rounded + 0.97
    variants.append({"price": round(p97, 2), "tactic": "charm_97", "psychology": "Insider pricing feel"})

    # .99 variant (classic charm)
    p99 = rounded - 0.01 if rounded > price else rounded + 0.99
    variants.append({"price": round(p99, 2), "tactic": "charm_99", "psychology": "Left-digit effect"})

    # Just-under variant (e.g., $49 -> $47)
    if price >= 10:
        under = int(price) - (int(price) % 10) + 7
        if under < price:
            variants.append({"price": float(under), "tactic": "just_under", "psychology": "Below psychological barrier"})

    return variants


def apply_anchoring(price, category=None):
    """Generate anchor pricing (show a higher reference price).

    The decoy effect: show 3 options where middle is the target.
    """
    anchors = []

    # High anchor (original/compare price)
    high_anchor = round(price * 2.5, -1) if price >= 10 else round(price * 3, 2)
    anchors.append({
        "anchor_price": high_anchor,
        "sale_price": price,
        "discount_pct": round((1 - price / high_anchor) * 100),
        "tactic": "high_anchor",
        "psychology": "Contrast effect makes real price feel like a deal",
    })

    # Was/Now pricing
    was_price = round(price * 1.67, 2)
    anchors.append({
        "anchor_price": was_price,
        "sale_price": price,
        "discount_pct": round((1 - price / was_price) * 100),
        "tactic": "was_now",
        "psychology": "Loss aversion - feel like saving money",
    })

    return anchors


def apply_decoy(target_price, category=None):
    """Create decoy pricing (3-tier with target as clear best value).

    The decoy (middle option) is priced to make the target look optimal.
    """
    # Tier 1: Basic (stripped down, priced to feel like bad value)
    basic_price = round(target_price * 0.6, 2)

    # Tier 2: Pro (the target - best value)
    pro_price = target_price

    # Tier 3: Premium (expensive, makes pro look reasonable)
    premium_price = round(target_price * 2.2, 2)

    return {
        "basic": {
            "price": basic_price,
            "value_items": 3,
            "psychology": "Exists to make Pro look like a deal",
        },
        "pro": {
            "price": pro_price,
            "value_items": 8,
            "psychology": "TARGET. Best perceived value (most features per $)",
            "is_target": True,
        },
        "premium": {
            "price": premium_price,
            "value_items": 10,
            "psychology": "Anchors high. Makes Pro feel affordable. Some will buy anyway.",
        },
        "tactic": "decoy_effect",
        "expected_distribution": "15% basic, 60% pro, 25% premium",
    }


# ---------------------------------------------------------------------------
# A/B test variant generation
# ---------------------------------------------------------------------------

def generate_ab_variants(product_name, base_price, category="tools"):
    """Generate A/B test pricing variants with statistical recommendations."""
    elasticity = estimate_elasticity(category, base_price)
    benchmarks = GUMROAD_BENCHMARKS.get(category, GUMROAD_BENCHMARKS.get("tools"))

    variants = []

    # Variant A: Current price (control)
    variants.append({
        "variant": "A_CONTROL",
        "price": base_price,
        "rationale": "Current price. Baseline measurement.",
    })

    # Variant B: Charm pricing
    charm = apply_charm_pricing(base_price)
    if charm:
        best_charm = charm[0]
        variants.append({
            "variant": "B_CHARM",
            "price": best_charm["price"],
            "rationale": f"{best_charm['tactic']}: {best_charm['psychology']}",
        })

    # Variant C: Higher price (test inelasticity)
    higher = round(base_price * 1.3, 2)
    # Apply charm to higher
    higher_charm = apply_charm_pricing(higher)
    if higher_charm:
        higher = higher_charm[0]["price"]
    variants.append({
        "variant": "C_PREMIUM",
        "price": higher,
        "rationale": f"30% increase. Tests price ceiling. Elasticity est: {elasticity}",
    })

    # Variant D: Lower price (test volume)
    lower = round(base_price * 0.7, 2)
    lower_charm = apply_charm_pricing(lower)
    if lower_charm:
        lower = lower_charm[0]["price"]
    variants.append({
        "variant": "D_VOLUME",
        "price": lower,
        "rationale": f"30% decrease. Tests if volume compensates. Needs >{abs(int(elasticity * 30))}% more sales to win.",
    })

    # Variant E: Optimal (from elasticity model)
    opt_price, opt_rev = find_optimal_price(
        base_price, 100, elasticity,
        benchmarks["low"], benchmarks["premium"]
    )
    if abs(opt_price - base_price) > 1:
        variants.append({
            "variant": "E_OPTIMAL",
            "price": opt_price,
            "rationale": f"Elasticity-optimized. Model predicts max revenue at this point.",
        })

    # Statistical requirements
    min_sample = 100  # per variant for basic significance
    recommended_sample = 385  # for 95% CI, 5% margin

    return {
        "product": product_name,
        "category": category,
        "base_price": base_price,
        "elasticity_estimate": elasticity,
        "variants": variants,
        "stats": {
            "min_sample_per_variant": min_sample,
            "recommended_sample_per_variant": recommended_sample,
            "test_duration_estimate": f"{len(variants) * 7} days minimum",
            "significance_level": 0.05,
            "power": 0.80,
        },
    }


# ---------------------------------------------------------------------------
# Display functions
# ---------------------------------------------------------------------------

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


def cmd_scan(category):
    """Scan competitor prices for a category."""
    category = category.lower().strip()

    print_header(f"COMPETITIVE PRICE SCAN: {category.upper()}")

    # Gumroad
    if category in GUMROAD_BENCHMARKS or category == "gumroad":
        cats = [category] if category in GUMROAD_BENCHMARKS else list(GUMROAD_BENCHMARKS.keys())
        for cat in cats:
            data = GUMROAD_BENCHMARKS[cat]
            print_section(f"GUMROAD - {cat.upper()}")
            print(f"  Price Range:   ${data['low']} - ${data['premium']}")
            print(f"  Median:        ${data['median']}")
            print(f"  Examples:")
            for ex in data["examples"]:
                print(f"    ${ex['price']:>6}  {ex['name']:<35} [{ex['tier']}]")
            print()

    # Fiverr
    if category in FIVERR_BENCHMARKS or category == "fiverr":
        cats = [category] if category in FIVERR_BENCHMARKS else list(FIVERR_BENCHMARKS.keys())
        for cat in cats:
            data = FIVERR_BENCHMARKS[cat]
            print_section(f"FIVERR - {cat.upper()}")
            for tier, info in data.items():
                rev = info["revisions"]
                rev_str = str(rev) if isinstance(rev, int) else rev
                print(f"    {tier.upper():<10} ${info['price']:>6}  Delivery: {info['delivery']}  Revisions: {rev_str}")
            print()

    # Upwork
    if category in UPWORK_BENCHMARKS or category == "upwork":
        cats = [category] if category in UPWORK_BENCHMARKS else list(UPWORK_BENCHMARKS.keys())
        for cat in cats:
            data = UPWORK_BENCHMARKS[cat]
            print_section(f"UPWORK HOURLY - {cat.upper()}")
            print(f"    Entry:    ${data['low']}/hr")
            print(f"    Median:   ${data['median']}/hr")
            print(f"    Senior:   ${data['high']}/hr")
            print(f"    Expert:   ${data['expert']}/hr")
            # Monthly estimate (20 billable hrs/week)
            monthly_median = data["median"] * 80
            monthly_high = data["high"] * 80
            print(f"    Monthly (80hrs): ${monthly_median:,.0f} - ${monthly_high:,.0f}")
            print()

    # SaaS
    if category in SAAS_BENCHMARKS or category == "saas":
        cats = [category] if category in SAAS_BENCHMARKS else list(SAAS_BENCHMARKS.keys())
        for cat in cats:
            data = SAAS_BENCHMARKS[cat]
            print_section(f"SAAS - {cat.upper()}")
            print(f"    Free Tier: {'Yes' if data.get('free_tier') else 'No'}")
            for tier, info in data.items():
                if tier == "free_tier":
                    continue
                per_user = " (per user)" if info.get("per_user") else ""
                print(f"    {tier.upper():<12} ${info['price']}/mo{per_user}")
            print()

    # Summary recommendation
    print_section("PRICING STRATEGY RECOMMENDATIONS")
    print("  1. Price at or slightly above median to signal quality")
    print("  2. Use charm pricing ($X.97 or $X7) for all price points")
    print("  3. Offer 3 tiers with decoy effect on middle tier")
    print("  4. Annual discount of 20% to improve LTV")
    print("  5. Launch at intro price (30% off) to build social proof")
    print()
    print(hr())


def cmd_optimize(product_name):
    """Optimize pricing for a specific product."""
    print_header(f"PRICING OPTIMIZATION: {product_name.upper()}")

    # Try to find the product in revenue data
    revenue_rows = []
    if REVENUE_CSV.exists():
        try:
            with open(REVENUE_CSV, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if product_name.lower() in (row.get("notes", "") + row.get("source", "")).lower():
                        revenue_rows.append(row)
        except Exception:
            pass

    # Default assumptions if no data
    base_price = 29.0
    category = "tools"
    if revenue_rows:
        prices = [float(r.get("revenue", 0)) for r in revenue_rows if float(r.get("revenue", 0)) > 0]
        if prices:
            base_price = float(np.median(prices))

    print_section("CURRENT ANALYSIS")
    print(f"  Product:       {product_name}")
    print(f"  Base Price:    ${base_price:.2f}")
    print(f"  Category:      {category}")
    print(f"  Data Points:   {len(revenue_rows)}")
    print()

    # Elasticity
    elasticity = estimate_elasticity(category, base_price)
    print_section("PRICE ELASTICITY")
    print(f"  Estimated Elasticity: {elasticity}")
    print(f"  Interpretation: {abs(elasticity) * 10:.0f}% demand drop per 10% price increase")
    if abs(elasticity) < 1:
        print(f"  Classification: INELASTIC - raise prices (demand drops less than price rises)")
    else:
        print(f"  Classification: ELASTIC - test carefully (demand drops more than price rises)")
    print()

    # Demand curve
    benchmarks = GUMROAD_BENCHMARKS.get(category, GUMROAD_BENCHMARKS["tools"])
    prices_range = np.linspace(benchmarks["low"], benchmarks["premium"], 20)
    curve = demand_curve(base_price, 100, elasticity, prices_range)

    print_section("DEMAND CURVE (base demand = 100 units)")
    print(f"  {'PRICE':>8} {'DEMAND':>8} {'REVENUE':>10} {'CHART'}")
    max_rev = max(p["revenue"] for p in curve) if curve else 1
    for p in curve:
        bar_len = int(p["revenue"] / max_rev * 30) if max_rev > 0 else 0
        bar = "#" * bar_len
        marker = " <-- CURRENT" if abs(p["price"] - base_price) < 2 else ""
        marker = " <-- OPTIMAL" if p["revenue"] == max_rev else marker
        print(f"  ${p['price']:>7.2f} {p['demand']:>7.1f} ${p['revenue']:>9.2f} {bar}{marker}")
    print()

    # Optimal price
    opt_price, opt_rev = find_optimal_price(base_price, 100, elasticity,
                                            benchmarks["low"], benchmarks["premium"])
    current_rev = base_price * 100
    uplift = ((opt_rev - current_rev) / current_rev * 100) if current_rev > 0 else 0

    print_section("OPTIMAL PRICE")
    print(f"  Current:     ${base_price:.2f}  (est. revenue index: ${current_rev:,.0f})")
    print(f"  Optimal:     ${opt_price:.2f}  (est. revenue index: ${opt_rev:,.0f})")
    print(f"  Uplift:      {uplift:+.1f}%")
    print()

    # Psychological pricing
    print_section("PSYCHOLOGICAL PRICING VARIANTS")
    charm = apply_charm_pricing(opt_price)
    for c in charm:
        print(f"  ${c['price']:>8.2f}  [{c['tactic']}]  {c['psychology']}")
    print()

    anchors = apply_anchoring(opt_price)
    print_section("ANCHOR PRICING")
    for a in anchors:
        print(f"  [{a['tactic']}]  Was ${a['anchor_price']:.2f}  Now ${a['sale_price']:.2f}  ({a['discount_pct']}% off)")
        print(f"    {a['psychology']}")
    print()

    decoy = apply_decoy(opt_price)
    print_section("DECOY PRICING (3-TIER)")
    for tier in ["basic", "pro", "premium"]:
        d = decoy[tier]
        target = " *** TARGET ***" if d.get("is_target") else ""
        print(f"  {tier.upper():<10} ${d['price']:>8.2f}  ({d['value_items']} items)  {d['psychology']}{target}")
    print(f"  Expected Split: {decoy['expected_distribution']}")

    print()
    print(hr())


def cmd_ab_test(product_name):
    """Generate A/B test variants for a product."""
    print_header(f"A/B TEST PLAN: {product_name.upper()}")

    # Try to infer price from revenue data
    base_price = 29.0
    category = "tools"

    result = generate_ab_variants(product_name, base_price, category)

    print_section("TEST CONFIGURATION")
    print(f"  Product:              {result['product']}")
    print(f"  Category:             {result['category']}")
    print(f"  Base Price:           ${result['base_price']:.2f}")
    print(f"  Elasticity Estimate:  {result['elasticity_estimate']}")
    print()

    print_section("VARIANTS")
    for v in result["variants"]:
        pct_diff = ((v["price"] - base_price) / base_price * 100) if base_price > 0 else 0
        diff_str = f"({pct_diff:+.0f}%)" if v["variant"] != "A_CONTROL" else "(baseline)"
        print(f"  {v['variant']:<15} ${v['price']:>8.2f} {diff_str}")
        print(f"    {v['rationale']}")
        print()

    print_section("STATISTICAL REQUIREMENTS")
    stats = result["stats"]
    print(f"  Min Sample/Variant:      {stats['min_sample_per_variant']}")
    print(f"  Recommended/Variant:     {stats['recommended_sample_per_variant']}")
    print(f"  Significance Level:      {stats['significance_level']}")
    print(f"  Statistical Power:       {stats['power']}")
    print(f"  Est. Duration:           {stats['test_duration_estimate']}")
    print()

    total_visitors = stats["recommended_sample_per_variant"] * len(result["variants"])
    print_section("IMPLEMENTATION GUIDE")
    print(f"  Total Visitors Needed:   {total_visitors:,}")
    print(f"  Number of Variants:      {len(result['variants'])}")
    print()
    print("  Setup Steps:")
    print("  1. Create separate product pages/links for each variant")
    print("  2. Use UTM params to track: ?variant=A_CONTROL, ?variant=B_CHARM, etc.")
    print("  3. Split traffic evenly across variants")
    print("  4. Track: page views, add-to-cart, purchases, revenue per visitor")
    print("  5. Run for minimum test duration before drawing conclusions")
    print("  6. Use chi-squared test to validate significance")
    print()

    print_section("EXPECTED OUTCOMES")
    print(f"  If elasticity = {result['elasticity_estimate']}:")
    for v in result["variants"]:
        pct_change = ((v["price"] - base_price) / base_price) if base_price > 0 else 0
        demand_change = 1 + pct_change * result["elasticity_estimate"]
        rev_index = v["price"] * max(0, demand_change) * 100
        print(f"    {v['variant']:<15} Price ${v['price']:>7.2f}  "
              f"Demand {demand_change:>5.2f}x  Revenue Index ${rev_index:>8,.0f}")

    print()
    print(hr())


def cmd_competitive_analysis():
    """Full competitive analysis across all categories."""
    print_header("COMPETITIVE PRICING ANALYSIS")

    # Gumroad landscape
    print_section("GUMROAD DIGITAL PRODUCTS")
    print(f"  {'CATEGORY':<15} {'LOW':>6} {'MEDIAN':>8} {'HIGH':>6} {'PREMIUM':>8}")
    for cat, data in sorted(GUMROAD_BENCHMARKS.items()):
        print(f"  {cat:<15} ${data['low']:>5} ${data['median']:>7} ${data['high']:>5} ${data['premium']:>7}")
    print()

    # Fiverr landscape
    print_section("FIVERR GIG PRICING (3-TIER)")
    print(f"  {'CATEGORY':<20} {'BASIC':>8} {'STANDARD':>10} {'PREMIUM':>10}")
    for cat, tiers in sorted(FIVERR_BENCHMARKS.items()):
        print(f"  {cat:<20} ${tiers['basic']['price']:>7} ${tiers['standard']['price']:>9} ${tiers['premium']['price']:>9}")
    print()

    # Upwork landscape
    print_section("UPWORK HOURLY RATES")
    print(f"  {'SKILL':<25} {'ENTRY':>8} {'MEDIAN':>8} {'SENIOR':>8} {'EXPERT':>8}")
    for skill, data in sorted(UPWORK_BENCHMARKS.items()):
        print(f"  {skill:<25} ${data['low']:>7} ${data['median']:>7} ${data['high']:>7} ${data['expert']:>7}")
    print()

    # SaaS landscape
    print_section("SAAS MONTHLY PRICING")
    for cat, data in sorted(SAAS_BENCHMARKS.items()):
        tiers_str = "  ".join(
            f"{t.upper()}: ${info['price']}" for t, info in data.items()
            if t != "free_tier" and isinstance(info, dict)
        )
        free = "FREE + " if data.get("free_tier") else ""
        print(f"  {cat:<15} {free}{tiers_str}")
    print()

    # Cross-platform analysis
    print_section("CROSS-PLATFORM ARBITRAGE OPPORTUNITIES")
    print("  1. Fiverr basic gigs ($25-50) can be packaged as Gumroad tools ($29-49)")
    print("     Margin: Sell template of your Fiverr delivery process")
    print("  2. Upwork hourly ($50-100/hr) vs productized service ($500-2000 flat)")
    print("     Margin: 2-3x if you systematize delivery to < 5 hours")
    print("  3. Gumroad ebooks ($7-27) repurposed as email courses ($47-97)")
    print("     Margin: Same content, different packaging, 2-4x price")
    print("  4. SaaS micro ($9-29/mo) built from scripts you already have")
    print("     Margin: Infinite after build cost, recurring revenue")
    print()

    # Pricing psychology summary
    print_section("UNIVERSAL PRICING TACTICS")
    print("  CHARM PRICING:  End in .97 or .99 (8-24% lift proven)")
    print("  ANCHORING:      Show 'was' price 2-2.5x higher")
    print("  DECOY:          3 tiers, middle = target (60% of buyers)")
    print("  SCARCITY:       'First 50 customers' or 'Price goes up Friday'")
    print("  BUNDLING:       3 products at 60% of sum (feels like 40% off)")
    print("  PENNIES/DAY:    '$97 = less than $3.23/day' reframe")
    print("  ROUND NUMBERS:  Use for premium ($100 not $97). Signals quality.")
    print("  ODD NUMBERS:    Use for value ($47 not $50). Signals deal.")

    print()
    print(hr())
    print(f"  Analysis generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(hr())


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Pricing Optimizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Categories for --scan:
  gumroad, fiverr, upwork, saas
  templates, courses, ebooks, tools
  web_development, data_scraping, automation, content_writing
  python_developer, web_scraping, ai_ml_engineer
  micro_saas, dev_tools, productivity

Examples:
  python3 AUTOMATIONS/pricing_optimizer.py --scan gumroad
  python3 AUTOMATIONS/pricing_optimizer.py --scan fiverr
  python3 AUTOMATIONS/pricing_optimizer.py --optimize "Python Automation Pack"
  python3 AUTOMATIONS/pricing_optimizer.py --ab-test "Cold Email Templates"
  python3 AUTOMATIONS/pricing_optimizer.py --competitive-analysis
        """,
    )
    parser.add_argument("--scan", metavar="CATEGORY", help="Scan competitor prices for category")
    parser.add_argument("--optimize", metavar="PRODUCT", help="Optimize pricing for a product")
    parser.add_argument("--ab-test", metavar="PRODUCT", help="Generate A/B test variants")
    parser.add_argument("--competitive-analysis", action="store_true", help="Full competitive analysis")

    args = parser.parse_args()

    if args.scan:
        cmd_scan(args.scan)
    elif args.optimize:
        cmd_optimize(args.optimize)
    elif args.ab_test:
        cmd_ab_test(args.ab_test)
    elif args.competitive_analysis:
        cmd_competitive_analysis()
    else:
        cmd_competitive_analysis()


if __name__ == "__main__":
    main()
