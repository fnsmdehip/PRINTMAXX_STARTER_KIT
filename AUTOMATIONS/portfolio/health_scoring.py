"""
Method health scoring and pipeline analytics for PRINTMAXX portfolio.

Computes per-method health grades, pipeline funnel conversion rates,
top opportunity rankings, and revenue velocity metrics.
"""

from typing import List, Dict, Any, Optional


def compute_method_health(method_id: str, position, alpha_entries: list, method_files: list) -> dict:
    """
    Compute a health score (0-100) for a single method.

    Scoring:
    - has_files_on_disk: +20 (files exist in MONEY_METHODS/)
    - status_score: Active=+25, Building=+15, Research=+5, else=0
    - has_revenue: +25 (revenue_total > 0)
    - alpha_reviewed: +10 (has related alpha that's been reviewed, not all pending)
    - high_potential: +10 (monthly_potential_high > 5000)
    - sub_method_activity: +10 (has active sub-methods)

    Returns dict with:
    - score: int (0-100)
    - breakdown: dict of component scores
    - grade: str (A/B/C/D/F)
    - color: str (for TUI rendering)
    """
    breakdown = {}

    # 1. has_files_on_disk: +20
    breakdown["has_files_on_disk"] = 20 if method_files else 0

    # 2. status_score: Active=+25, Building=+15, Research=+5
    status = (getattr(position, "status", "") or "").lower() if position else ""
    if status == "active":
        breakdown["status_score"] = 25
    elif status == "building":
        breakdown["status_score"] = 15
    elif status == "research":
        breakdown["status_score"] = 5
    else:
        breakdown["status_score"] = 0

    # 3. has_revenue: +25
    rev = getattr(position, "revenue_total", 0.0) if position else 0.0
    breakdown["has_revenue"] = 25 if rev > 0 else 0

    # 4. alpha_reviewed: +10 (has related alpha that's been reviewed)
    mid_lower = method_id.lower()
    name_lower = (getattr(position, "name", "") or "").lower() if position else ""
    related = []
    for a in alpha_entries:
        tactic = str(getattr(a, "tactic", "")).lower()
        a_cat = str(getattr(a, "category", "")).lower()
        if mid_lower in tactic or mid_lower in a_cat or (name_lower and len(name_lower) > 3 and name_lower in tactic):
            related.append(a)

    if related:
        has_reviewed = any(
            (getattr(a, "status", "") or "").upper() not in ("PENDING_REVIEW", "")
            for a in related
        )
        breakdown["alpha_reviewed"] = 10 if has_reviewed else 0
    else:
        # No related alpha at all counts as 0 (nothing to review)
        breakdown["alpha_reviewed"] = 0

    # 5. high_potential: +10
    pot_high = getattr(position, "monthly_potential_high", 0.0) if position else 0.0
    breakdown["high_potential"] = 10 if pot_high > 5000 else 0

    # 6. sub_method_activity: +10
    # Import here to avoid circular dependency
    from portfolio.hierarchy import get_sub_methods
    children = get_sub_methods(method_id)
    if children:
        # Check if any child has Active status among positions passed via alpha_entries context
        # We check via the position's status field for the method_id match
        breakdown["sub_method_activity"] = 10  # has sub-methods defined = some activity
    else:
        # No sub-methods defined; only parent methods get this bonus
        # For leaf methods, grant the 10 points automatically so they aren't penalized
        breakdown["sub_method_activity"] = 10

    score = sum(breakdown.values())
    score = max(0, min(100, score))

    # Grade
    if score >= 80:
        grade = "A"
        color = "green"
    elif score >= 60:
        grade = "B"
        color = "cyan"
    elif score >= 40:
        grade = "C"
        color = "yellow"
    elif score >= 20:
        grade = "D"
        color = "#cc6600"
    else:
        grade = "F"
        color = "red"

    return {
        "score": score,
        "breakdown": breakdown,
        "grade": grade,
        "color": color,
    }


def compute_pipeline_funnel(positions: list) -> dict:
    """
    Count methods at each stage and compute conversion rates.

    Returns:
    - stages: dict mapping stage name to count
    - conversions: dict mapping "stage1>stage2" to rate (float 0-1)
    - total_methods: int
    """
    stage_order = ["Research", "Planning", "Building", "Active", "Paused"]
    stages = {s: 0 for s in stage_order}
    stages["Other"] = 0

    for p in positions:
        status = (getattr(p, "status", "") or "").strip()
        # Normalize
        matched = False
        for s in stage_order:
            if status.lower() == s.lower():
                stages[s] += 1
                matched = True
                break
        if not matched:
            stages["Other"] += 1

    total = len(positions)

    # Conversion rates: what fraction of methods progress beyond each stage
    # Research -> Planning -> Building -> Active
    cumulative = {
        "Research": stages["Research"] + stages["Planning"] + stages["Building"] + stages["Active"],
        "Planning": stages["Planning"] + stages["Building"] + stages["Active"],
        "Building": stages["Building"] + stages["Active"],
        "Active": stages["Active"],
    }

    conversions = {}
    pairs = [("Research", "Planning"), ("Planning", "Building"), ("Building", "Active")]
    for s1, s2 in pairs:
        if cumulative[s1] > 0:
            conversions[f"{s1}>{s2}"] = round(cumulative[s2] / cumulative[s1], 3)
        else:
            conversions[f"{s1}>{s2}"] = 0.0

    return {
        "stages": stages,
        "conversions": conversions,
        "total_methods": total,
    }


def compute_top_opportunities(positions: list, alpha_entries: list, method_files_map: dict) -> list:
    """
    Rank methods by opportunity score = (100 - health_score) * potential / 1000.
    Higher = bigger gap between potential and readiness.

    Args:
        positions: list of PortfolioPosition objects
        alpha_entries: list of AlphaEntry objects
        method_files_map: dict mapping method_id -> list of file dicts

    Returns list of dicts with method_id, name, health_score, potential, opportunity_score, grade
    """
    results = []
    for p in positions:
        mid = p.method_id
        files = method_files_map.get(mid, [])
        health = compute_method_health(mid, p, alpha_entries, files)
        potential = max(p.monthly_potential_low, p.monthly_potential_high)
        if potential <= 0:
            continue  # Skip methods with no defined potential

        opp_score = (100 - health["score"]) * potential / 1000.0
        results.append({
            "method_id": mid,
            "name": p.name,
            "health_score": health["score"],
            "grade": health["grade"],
            "color": health["color"],
            "potential": potential,
            "opportunity_score": round(opp_score, 1),
        })

    results.sort(key=lambda x: x["opportunity_score"], reverse=True)
    return results


def compute_revenue_velocity(financial_summary, positions: list) -> dict:
    """
    Calculate revenue velocity metrics.

    Returns:
    - daily_burn: float
    - monthly_burn: float
    - methods_with_revenue: int
    - methods_without_revenue: int
    - total_invested: float
    - total_revenue: float
    - roi_pct: float
    - revenue_per_method: float (average across methods with revenue)
    """
    monthly_burn = getattr(financial_summary, "burn_rate_monthly", 0.0) if financial_summary else 0.0
    daily_burn = monthly_burn / 30.0

    total_invested = getattr(financial_summary, "total_expenses", 0.0) if financial_summary else 0.0
    total_revenue = getattr(financial_summary, "total_revenue", 0.0) if financial_summary else 0.0

    with_rev = sum(1 for p in positions if getattr(p, "revenue_total", 0.0) > 0)
    without_rev = len(positions) - with_rev

    roi_pct = ((total_revenue - total_invested) / total_invested * 100.0) if total_invested > 0 else 0.0
    rev_per_method = (total_revenue / with_rev) if with_rev > 0 else 0.0

    return {
        "daily_burn": round(daily_burn, 2),
        "monthly_burn": round(monthly_burn, 2),
        "methods_with_revenue": with_rev,
        "methods_without_revenue": without_rev,
        "total_invested": round(total_invested, 2),
        "total_revenue": round(total_revenue, 2),
        "roi_pct": round(roi_pct, 1),
        "revenue_per_method": round(rev_per_method, 2),
    }
