#!/usr/bin/env python3
"""App Factory Portfolio Optimizer.

Portfolio-level optimization for the app factory:
  - Track revenue per app (Stripe MCP integration + CSV tracking)
  - Kill underperformers (< $100 MRR after 60 days)
  - Double down on winners (> $500 MRR with 20%+ growth)
  - Cross-promote between apps
  - Calculate portfolio metrics (total MRR, growth, churn)
  - A/B test pricing across portfolio
  - Generate portfolio dashboard

Usage:
  python3 AUTOMATIONS/app_factory/portfolio_optimizer.py --status
  python3 AUTOMATIONS/app_factory/portfolio_optimizer.py --optimize
  python3 AUTOMATIONS/app_factory/portfolio_optimizer.py --revenue-check
  python3 AUTOMATIONS/app_factory/portfolio_optimizer.py --dashboard
  python3 AUTOMATIONS/app_factory/portfolio_optimizer.py --help
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT = Path(__file__).resolve().parent.parent.parent
AUTOMATIONS = PROJECT / "AUTOMATIONS"
LEDGER = PROJECT / "LEDGER"
OPS = PROJECT / "OPS"
LOG_DIR = AUTOMATIONS / "app_factory" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

BUILDS_CSV = LEDGER / "APP_FACTORY_BUILDS.csv"
REVENUE_CSV = LEDGER / "APP_FACTORY_REVENUE.csv"
PORTFOLIO_DASH = OPS / "APP_FACTORY_PORTFOLIO.md"
DECISIONS_CSV = LEDGER / "APP_FACTORY_DECISIONS.csv"
LOGFILE = LOG_DIR / "portfolio_optimizer.log"

# Kill / scale thresholds (from Capital Genesis ethos)
KILL_THRESHOLD_MRR = 100      # Kill if < $100 MRR
KILL_THRESHOLD_DAYS = 60      # After 60 days live
SCALE_THRESHOLD_MRR = 500     # Scale if > $500 MRR
SCALE_THRESHOLD_GROWTH = 0.20 # With 20%+ month-over-month growth

REVENUE_CSV_FIELDS = [
    "timestamp", "app_slug", "app_name", "period", "mrr", "downloads",
    "trials_started", "paid_conversions", "churn_rate", "source",
]

DECISION_FIELDS = [
    "timestamp", "app_slug", "decision", "reason", "mrr", "growth_rate",
    "days_live", "action_taken",
]


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT}")
    return resolved


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOGFILE, "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# Revenue Data Collection
# ---------------------------------------------------------------------------
def load_revenue_data() -> dict[str, list[dict]]:
    """Load revenue data per app from CSV."""
    data: dict[str, list[dict]] = {}

    if not REVENUE_CSV.exists():
        return data

    try:
        with open(REVENUE_CSV, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                slug = row.get("app_slug", "")
                if slug not in data:
                    data[slug] = []
                data[slug].append(row)
    except Exception as e:
        log(f"Error loading revenue data: {e}")

    return data


def record_revenue(
    app_slug: str,
    app_name: str,
    mrr: float,
    downloads: int = 0,
    trials: int = 0,
    paid: int = 0,
    churn: float = 0.0,
    source: str = "manual",
    dry_run: bool = False,
) -> None:
    """Record a revenue data point for an app."""
    if dry_run:
        log(f"DRY RUN: Would record MRR=${mrr} for {app_slug}")
        return

    row = {
        "timestamp": datetime.now().isoformat(),
        "app_slug": app_slug,
        "app_name": app_name,
        "period": datetime.now().strftime("%Y-%m"),
        "mrr": str(mrr),
        "downloads": str(downloads),
        "trials_started": str(trials),
        "paid_conversions": str(paid),
        "churn_rate": str(churn),
        "source": source,
    }

    path = safe_path(REVENUE_CSV)
    write_header = not path.exists()
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=REVENUE_CSV_FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    log(f"Recorded MRR=${mrr} for {app_slug} ({source})")


def check_stripe_revenue() -> dict[str, float]:
    """Query Stripe for revenue per product (uses Stripe MCP if available)."""
    revenue: dict[str, float] = {}

    # Try to read from Stripe via subprocess to printmaxx CLI
    # This is a fallback -- the Stripe MCP tools are preferred
    try:
        # Check if we can reach Stripe via env
        stripe_key = os.environ.get("STRIPE_SECRET_KEY", "")
        if not stripe_key:
            log("No STRIPE_SECRET_KEY set. Skipping Stripe check.")
            return revenue

        # Use stripe CLI or API
        import urllib.request
        req = urllib.request.Request(
            "https://api.stripe.com/v1/charges?limit=100",
            headers={
                "Authorization": f"Bearer {stripe_key}",
            }
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())

        for charge in data.get("data", []):
            if charge.get("status") == "succeeded":
                product = charge.get("description", "unknown")
                amount = charge.get("amount", 0) / 100  # cents to dollars
                revenue[product] = revenue.get(product, 0) + amount

        log(f"Stripe: found revenue for {len(revenue)} products")

    except Exception as e:
        log(f"Stripe check failed: {e}")

    return revenue


# ---------------------------------------------------------------------------
# Portfolio Analysis
# ---------------------------------------------------------------------------
def load_builds() -> list[dict]:
    """Load all builds from CSV."""
    if not BUILDS_CSV.exists():
        return []
    try:
        with open(BUILDS_CSV, "r", newline="") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


def calculate_app_metrics(slug: str, revenue_data: dict[str, list[dict]]) -> dict[str, Any]:
    """Calculate metrics for a single app."""
    records = revenue_data.get(slug, [])
    if not records:
        return {
            "mrr": 0.0,
            "growth_rate": 0.0,
            "total_revenue": 0.0,
            "months_tracked": 0,
            "trend": "NO_DATA",
        }

    # Sort by timestamp
    records.sort(key=lambda r: r.get("timestamp", ""))

    mrr_values = [float(r.get("mrr", 0)) for r in records]
    current_mrr = mrr_values[-1] if mrr_values else 0

    # Calculate growth rate (last 2 periods)
    growth_rate = 0.0
    if len(mrr_values) >= 2 and mrr_values[-2] > 0:
        growth_rate = (mrr_values[-1] - mrr_values[-2]) / mrr_values[-2]

    # Calculate total revenue
    total_revenue = sum(mrr_values)

    # Determine trend
    if len(mrr_values) < 2:
        trend = "NEW"
    elif growth_rate > 0.20:
        trend = "ROCKET"
    elif growth_rate > 0.05:
        trend = "GROWING"
    elif growth_rate > -0.05:
        trend = "STABLE"
    elif growth_rate > -0.20:
        trend = "DECLINING"
    else:
        trend = "TANKING"

    return {
        "mrr": current_mrr,
        "growth_rate": growth_rate,
        "total_revenue": total_revenue,
        "months_tracked": len(mrr_values),
        "trend": trend,
    }


def days_since_launch(build_row: dict) -> int:
    """Calculate days since app was launched."""
    ts = build_row.get("timestamp", "")
    if not ts:
        return 0
    try:
        launch_date = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return (datetime.now() - launch_date.replace(tzinfo=None)).days
    except (ValueError, TypeError):
        return 0


# ---------------------------------------------------------------------------
# Decision Engine
# ---------------------------------------------------------------------------
def make_portfolio_decisions(
    builds: list[dict],
    revenue_data: dict[str, list[dict]],
    dry_run: bool = False,
) -> list[dict]:
    """Make kill/scale/maintain decisions for each app."""
    decisions = []

    for build in builds:
        slug = build.get("slug", "")
        name = build.get("name", slug)
        status = build.get("status", "")

        # Skip apps not yet live
        if status not in ("SUBMITTED", "LIVE", "BUILDING", "GENERATED"):
            continue

        metrics = calculate_app_metrics(slug, revenue_data)
        days_live = days_since_launch(build)

        decision = _evaluate_app(slug, name, metrics, days_live, status)
        decisions.append(decision)

        if not dry_run:
            _log_decision(decision)

    return decisions


def _evaluate_app(
    slug: str,
    name: str,
    metrics: dict,
    days_live: int,
    status: str,
) -> dict:
    """Evaluate a single app and return a decision."""
    mrr = metrics.get("mrr", 0)
    growth = metrics.get("growth_rate", 0)
    trend = metrics.get("trend", "NO_DATA")

    decision = {
        "timestamp": datetime.now().isoformat(),
        "app_slug": slug,
        "app_name": name,
        "mrr": mrr,
        "growth_rate": round(growth, 3),
        "days_live": days_live,
        "trend": trend,
        "status": status,
        "decision": "MAINTAIN",
        "reason": "",
        "actions": [],
    }

    # KILL decision
    if days_live > KILL_THRESHOLD_DAYS and mrr < KILL_THRESHOLD_MRR:
        decision["decision"] = "KILL"
        decision["reason"] = f"Below ${KILL_THRESHOLD_MRR} MRR after {days_live} days"
        decision["actions"] = [
            "Deprecate in App Store (don't delete -- keep as portfolio padding)",
            "Stop distribution spend",
            "Redirect traffic to better-performing app in same niche",
            "Harvest any remaining users with cross-promotion push",
        ]

    # SCALE decision
    elif mrr >= SCALE_THRESHOLD_MRR and growth >= SCALE_THRESHOLD_GROWTH:
        decision["decision"] = "SCALE"
        decision["reason"] = f"${mrr} MRR with {growth*100:.0f}% growth"
        decision["actions"] = [
            "Increase Apple Search Ads budget by 2x",
            "Reach out to 20 niche influencers",
            "A/B test higher pricing tiers",
            "Add 2-3 premium features from user requests",
            "Create dedicated landing page",
            "Cross-promote from all other PRINTMAXX apps",
        ]

    # BOOST decision (promising but not yet at scale threshold)
    elif mrr >= 100 and growth > 0:
        decision["decision"] = "BOOST"
        decision["reason"] = f"${mrr} MRR, positive growth ({growth*100:.0f}%)"
        decision["actions"] = [
            "Run pricing experiment (test 20% higher)",
            "Add one feature from top user request",
            "Increase posting frequency for this app",
        ]

    # WATCH decision (too early to tell)
    elif days_live < KILL_THRESHOLD_DAYS:
        decision["decision"] = "WATCH"
        decision["reason"] = f"Only {days_live} days live. Need {KILL_THRESHOLD_DAYS} for evaluation."
        decision["actions"] = [
            "Continue current distribution plan",
            "Monitor weekly metrics",
        ]

    # MAINTAIN (default)
    else:
        decision["decision"] = "MAINTAIN"
        decision["reason"] = f"${mrr} MRR, {trend} trend"
        decision["actions"] = [
            "Continue current strategy",
            "Minor optimization: ASO keywords, screenshots",
        ]

    return decision


def _log_decision(decision: dict) -> None:
    """Log a decision to the decisions CSV."""
    path = safe_path(DECISIONS_CSV)
    row = {
        "timestamp": decision["timestamp"],
        "app_slug": decision["app_slug"],
        "decision": decision["decision"],
        "reason": decision["reason"],
        "mrr": str(decision["mrr"]),
        "growth_rate": str(decision["growth_rate"]),
        "days_live": str(decision["days_live"]),
        "action_taken": "; ".join(decision.get("actions", [])[:2]),
    }

    write_header = not path.exists()
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=DECISION_FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


# ---------------------------------------------------------------------------
# Cross-Promotion Matrix
# ---------------------------------------------------------------------------
def generate_cross_promotion_matrix(builds: list[dict]) -> dict[str, list[str]]:
    """Generate cross-promotion recommendations between apps."""
    # Group apps by niche
    niche_groups: dict[str, list[dict]] = {}
    for build in builds:
        niche = build.get("niche", "general")
        if niche not in niche_groups:
            niche_groups[niche] = []
        niche_groups[niche].append(build)

    matrix: dict[str, list[str]] = {}

    for build in builds:
        slug = build.get("slug", "")
        niche = build.get("niche", "general")
        recommendations = []

        # Promote apps in related niches
        related_niches = _get_related_niches(niche)
        for related in related_niches:
            for other in niche_groups.get(related, []):
                if other.get("slug") != slug:
                    recommendations.append(other.get("slug", ""))

        # Also promote apps in same niche (complementary)
        for other in niche_groups.get(niche, []):
            if other.get("slug") != slug:
                recommendations.append(other.get("slug", ""))

        matrix[slug] = recommendations[:5]  # Max 5 cross-promotions

    return matrix


def _get_related_niches(niche: str) -> list[str]:
    """Get related niches for cross-promotion."""
    relations: dict[str, list[str]] = {
        "health_fitness": ["wellness", "food_health", "mental_health"],
        "wellness": ["health_fitness", "mental_health", "religious_spiritual"],
        "religious_spiritual": ["wellness", "mental_health", "education"],
        "productivity": ["education", "finance", "health_fitness"],
        "education": ["productivity", "religious_spiritual"],
        "food_health": ["health_fitness", "wellness"],
        "mental_health": ["wellness", "health_fitness", "religious_spiritual"],
        "finance": ["productivity"],
    }
    return relations.get(niche, [])


# ---------------------------------------------------------------------------
# Dashboard Generator
# ---------------------------------------------------------------------------
def generate_dashboard(
    builds: list[dict],
    revenue_data: dict[str, list[dict]],
    decisions: list[dict],
) -> str:
    """Generate portfolio dashboard markdown."""
    total_apps = len(builds)
    live_apps = sum(1 for b in builds if b.get("status") in ("LIVE", "SUBMITTED"))
    generated_apps = sum(1 for b in builds if b.get("status") == "GENERATED")

    # Calculate portfolio metrics
    total_mrr = 0.0
    app_metrics = []
    for build in builds:
        slug = build.get("slug", "")
        metrics = calculate_app_metrics(slug, revenue_data)
        total_mrr += metrics["mrr"]
        app_metrics.append({
            "slug": slug,
            "name": build.get("name", slug),
            "niche": build.get("niche", "?"),
            "status": build.get("status", "?"),
            **metrics,
        })

    # Sort by MRR
    app_metrics.sort(key=lambda m: -m.get("mrr", 0))

    # Decision counts
    decision_counts: dict[str, int] = {}
    for d in decisions:
        dec = d.get("decision", "UNKNOWN")
        decision_counts[dec] = decision_counts.get(dec, 0) + 1

    lines = [
        "# App Factory Portfolio Dashboard",
        f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Portfolio Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total Apps | {total_apps} |",
        f"| Live/Submitted | {live_apps} |",
        f"| Generated (not yet built) | {generated_apps} |",
        f"| **Total Portfolio MRR** | **${total_mrr:.2f}** |",
        "",
    ]

    # Decision summary
    if decision_counts:
        lines.extend([
            "## Latest Decisions",
            "",
            "| Decision | Count |",
            "|----------|-------|",
        ])
        for dec, count in sorted(decision_counts.items()):
            icon = {
                "KILL": "X", "SCALE": ">>", "BOOST": ">",
                "WATCH": "?", "MAINTAIN": "=",
            }.get(dec, "?")
            lines.append(f"| {icon} {dec} | {count} |")
        lines.append("")

    # Per-app table
    lines.extend([
        "## App Performance",
        "",
        "| App | Niche | Status | MRR | Growth | Trend | Decision |",
        "|-----|-------|--------|-----|--------|-------|----------|",
    ])

    for m in app_metrics:
        growth_pct = f"{m.get('growth_rate', 0)*100:.0f}%" if m.get('growth_rate') else "N/A"
        # Find decision for this app
        app_decision = "N/A"
        for d in decisions:
            if d.get("app_slug") == m["slug"]:
                app_decision = d.get("decision", "N/A")
                break

        lines.append(
            f"| {m['name'][:25]} | {m['niche'][:15]} | {m['status']} | "
            f"${m.get('mrr', 0):.0f} | {growth_pct} | {m.get('trend', '?')} | {app_decision} |"
        )

    # Cross-promotion opportunities
    cross_promo = generate_cross_promotion_matrix(builds)
    if cross_promo:
        lines.extend([
            "",
            "## Cross-Promotion Matrix",
            "",
            "| App | Promote To |",
            "|-----|-----------|",
        ])
        for slug, targets in cross_promo.items():
            if targets:
                lines.append(f"| {slug} | {', '.join(targets[:3])} |")

    # Action items
    action_items = [d for d in decisions if d.get("decision") in ("KILL", "SCALE")]
    if action_items:
        lines.extend([
            "",
            "## Priority Actions",
            "",
        ])
        for d in action_items:
            lines.append(f"### {d.get('decision')}: {d.get('app_name', d.get('app_slug', '?'))}")
            lines.append(f"Reason: {d.get('reason', '')}")
            for action in d.get("actions", []):
                lines.append(f"- [ ] {action}")
            lines.append("")

    # Kill list
    kills = [d for d in decisions if d.get("decision") == "KILL"]
    if kills:
        lines.extend([
            "## Kill List (underperformers to deprecate)",
            "",
        ])
        for k in kills:
            lines.append(f"- {k.get('app_name', k.get('app_slug', '?'))}: {k.get('reason', '')}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="App Factory Portfolio Optimizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 AUTOMATIONS/app_factory/portfolio_optimizer.py --status
  python3 AUTOMATIONS/app_factory/portfolio_optimizer.py --optimize
  python3 AUTOMATIONS/app_factory/portfolio_optimizer.py --revenue-check
  python3 AUTOMATIONS/app_factory/portfolio_optimizer.py --dashboard
  python3 AUTOMATIONS/app_factory/portfolio_optimizer.py --record-revenue --app fitstreak --mrr 150
        """,
    )
    parser.add_argument("--status", action="store_true", help="Show portfolio status")
    parser.add_argument("--optimize", action="store_true", help="Run optimization (kill/scale decisions)")
    parser.add_argument("--revenue-check", action="store_true", help="Check Stripe for latest revenue")
    parser.add_argument("--dashboard", action="store_true", help="Generate portfolio dashboard")
    parser.add_argument("--record-revenue", action="store_true", help="Record revenue data point")
    parser.add_argument("--app", help="App slug (for --record-revenue)")
    parser.add_argument("--mrr", type=float, help="MRR amount (for --record-revenue)")
    parser.add_argument("--dry-run", action="store_true", help="Don't write files")

    args = parser.parse_args()

    if not any([args.status, args.optimize, args.revenue_check, args.dashboard, args.record_revenue]):
        parser.print_help()
        return

    builds = load_builds()
    revenue_data = load_revenue_data()

    if args.record_revenue:
        if not args.app or args.mrr is None:
            log("ERROR: --app and --mrr required for --record-revenue")
            return
        # Find app name from builds
        name = args.app
        for b in builds:
            if b.get("slug") == args.app:
                name = b.get("name", args.app)
                break
        record_revenue(args.app, name, args.mrr, source="manual", dry_run=args.dry_run)
        return

    if args.revenue_check:
        log("Checking Stripe for revenue data...")
        stripe_data = check_stripe_revenue()
        if stripe_data:
            for product, amount in stripe_data.items():
                log(f"  {product}: ${amount:.2f}")
        else:
            log("No Stripe revenue data found (or STRIPE_SECRET_KEY not set)")
        return

    if args.status:
        log(f"Portfolio: {len(builds)} apps")
        for build in builds:
            slug = build.get("slug", "?")
            status = build.get("status", "?")
            metrics = calculate_app_metrics(slug, revenue_data)
            log(f"  {slug}: {status} | MRR=${metrics['mrr']:.0f} | {metrics['trend']}")
        return

    if args.optimize:
        log("Running portfolio optimization...")
        decisions = make_portfolio_decisions(builds, revenue_data, dry_run=args.dry_run)

        for d in decisions:
            icon = {"KILL": "X", "SCALE": ">>", "BOOST": ">", "WATCH": "?", "MAINTAIN": "="}.get(d["decision"], "?")
            log(f"  [{icon}] {d['app_slug']}: {d['decision']} -- {d['reason']}")

        log(f"Total decisions: {len(decisions)}")

        # Also generate dashboard if optimizing
        if not args.dry_run:
            dashboard = generate_dashboard(builds, revenue_data, decisions)
            dash_path = safe_path(PORTFOLIO_DASH)
            with open(dash_path, "w") as f:
                f.write(dashboard)
            log(f"Dashboard updated: {dash_path}")

    if args.dashboard:
        decisions = make_portfolio_decisions(builds, revenue_data, dry_run=True)
        dashboard = generate_dashboard(builds, revenue_data, decisions)

        if args.dry_run:
            print(dashboard)
        else:
            dash_path = safe_path(PORTFOLIO_DASH)
            with open(dash_path, "w") as f:
                f.write(dashboard)
            log(f"Dashboard saved: {dash_path}")
            print(dashboard)


if __name__ == "__main__":
    main()
