#!/usr/bin/env python3
"""
PRINTMAXX MASTER PORTFOLIO DASHBOARD
=====================================
Jane Street-quality unified command center for ALL portfolio investments.
All data live from filesystem. No mock data. No pretend numbers.

Replaces: printmaxx_quant_terminal.py --summary + pemf_quant_dashboard.py

Usage:
    python3 AUTOMATIONS/master_portfolio_dashboard.py              # Full dashboard
    python3 AUTOMATIONS/master_portfolio_dashboard.py --summary    # Quick 20-line overview
    python3 AUTOMATIONS/master_portfolio_dashboard.py --portfolio   # Portfolio positions
    python3 AUTOMATIONS/master_portfolio_dashboard.py --pemf        # PEMF deep dive
    python3 AUTOMATIONS/master_portfolio_dashboard.py --risk        # Risk metrics
    python3 AUTOMATIONS/master_portfolio_dashboard.py --alpha       # Alpha pipeline
    python3 AUTOMATIONS/master_portfolio_dashboard.py --financial   # Financial breakdown
    python3 AUTOMATIONS/master_portfolio_dashboard.py --todo        # Priority actions
    python3 AUTOMATIONS/master_portfolio_dashboard.py --full        # All panels
"""

import argparse
import sys
from pathlib import Path

# Ensure AUTOMATIONS directory is on the path for portfolio package imports
AUTOMATIONS_DIR = Path(__file__).resolve().parent
if str(AUTOMATIONS_DIR) not in sys.path:
    sys.path.insert(0, str(AUTOMATIONS_DIR))

try:
    from rich.console import Console
    from rich.text import Text
    from rich.panel import Panel
    from rich import box
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
    from rich.console import Console
    from rich.text import Text
    from rich.panel import Panel
    from rich import box

from portfolio.data_layer import (
    load_all_positions,
    load_financial_summary,
    load_alpha_entries,
    load_pemf_metrics,
    load_content_metrics,
    load_revenue_history,
    load_expense_breakdown,
)
from portfolio.risk_engine import calculate_portfolio_risk
from portfolio.renderers import (
    render_header,
    render_portfolio_overview,
    render_financial_panel,
    render_alpha_pipeline,
    render_risk_panel,
    render_content_metrics,
    render_pemf_summary,
    render_pemf_deep_dive,
    render_todo_panel,
    render_expense_breakdown,
)


console = Console()


def render_summary(positions, financial, pemf, risk, alpha, content):
    """Quick 20-line summary mode for session start."""
    from datetime import datetime

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Header
    header = Text()
    header.append("PRINTMAXX PORTFOLIO TERMINAL", style="bold cyan")
    header.append(f" | {now}\n", style="dim")
    header.append("=" * 60 + "\n", style="dim")
    console.print(header)

    # Portfolio P&L
    pnl = Text()
    pnl.append("PORTFOLIO P&L\n", style="bold white")
    rev = financial.total_revenue
    exp = financial.total_expenses
    net = financial.net_profit
    net_style = "green" if net >= 0 else "red"
    pnl.append(f"  Revenue: ${rev:,.0f}", style="green")
    pnl.append(f" | Expenses: ${exp:,.0f}", style="red")
    pnl.append(f" | Net: ", style="white")
    pnl.append(f"${net:,.0f}\n", style=net_style)
    pnl.append(f"  Burn Rate: ${financial.burn_rate_monthly:,.0f}/mo", style="yellow")

    active_count = sum(1 for p in positions if p.status == "Active")
    building_count = sum(1 for p in positions if p.status == "Building")
    pnl.append(f" | Methods: {len(positions)} ({active_count} active, {building_count} building)\n")
    console.print(pnl)

    # Active positions
    pos_text = Text()
    pos_text.append("\nPOSITIONS (Active + Building)\n", style="bold white")
    shown = 0
    for p in positions:
        if p.status in ("Active", "Building"):
            status_style = "green" if p.status == "Active" else "cyan"
            pos_text.append(f"  {p.method_id:<18}", style="dim")
            pos_text.append(f"${p.revenue_total:>8,.0f}  ", style="white")
            pos_text.append(f"{p.phase:<8}  ", style="dim")
            pos_text.append(f"[{p.status}]", style=status_style)
            pos_text.append("\n")
            shown += 1
    if shown == 0:
        pos_text.append("  No active positions yet\n", style="dim")
    console.print(pos_text)

    # PEMF Venture
    pemf_text = Text()
    pemf_text.append("\nPEMF VENTURE (WEBERMAXX)\n", style="bold cyan")
    pemf_text.append(
        f"  Research: {pemf.research_files_count}/16 files | "
        f"{pemf.research_total_lines:,} lines | "
        f"Bootstrap: ${pemf.bootstrap_cost:,.0f}\n"
    )
    pemf_text.append(
        f"  Unit: ${pemf.unit_cogs_low:.0f}-${pemf.unit_cogs_high:.0f} COGS "
        f"-> ${pemf.price_point:.0f} price "
        f"({pemf.margin_low:.0f}-{pemf.margin_high:.0f}% margin)\n"
    )
    pemf_text.append(
        f"  Influencers: {pemf.influencers_total} found | "
        f"Compliance: {pemf.compliance_path}\n"
    )
    console.print(pemf_text)

    # Risk metrics
    risk_text = Text()
    risk_text.append("\nRISK METRICS\n", style="bold white")
    sharpe_str = f"{risk.portfolio_sharpe:.2f}" if risk.sharpe_data_months > 0 else "N/A (no data)"
    var_str = f"{risk.var_95:.1f}%" if risk.var_95 > 0 else "N/A"
    risk_text.append(f"  Sharpe: {sharpe_str}")
    risk_text.append(f" | VaR 95%: {var_str}")
    risk_text.append(f"\n  HHI Method: {risk.hhi_method:.2f}")
    risk_text.append(f" | Max Drawdown: {risk.max_drawdown:.1f}%\n")
    console.print(risk_text)

    # Alpha pipeline
    pending = sum(1 for a in alpha if a.status == "PENDING_REVIEW")
    approved = sum(1 for a in alpha if a.status == "APPROVED")
    alpha_text = Text()
    alpha_text.append("\nALPHA PIPELINE\n", style="bold white")
    alpha_text.append(f"  Total: {len(alpha)}")
    alpha_text.append(f" | Pending: {pending}", style="yellow")
    alpha_text.append(f" | Approved: {approved}\n", style="green")
    console.print(alpha_text)

    # Content
    content_text = Text()
    content_text.append("\nCONTENT\n", style="bold white")
    content_text.append(
        f"  Pipeline: {content.total_pieces} pieces | "
        f"Calendar: {content.calendar_posts} posts\n"
    )
    console.print(content_text)

    # Next actions
    actions = Text()
    actions.append("\nNEXT ACTIONS\n", style="bold yellow")
    todos = [
        ("1", "Build PEMF prototype ($62)"),
        ("2", "Ship PrayerLock PWA to Vercel"),
        ("3", "Upload 130 tweets to Buffer"),
        ("4", "Start cold outbound (MM007 SCALE decision)"),
        ("5", "Create Gumroad account + list templates"),
    ]
    for num, action in todos:
        actions.append(f"  {num}. {action}\n")
    console.print(actions)


def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Master Portfolio Dashboard - Jane Street Edition"
    )
    parser.add_argument("--summary", action="store_true", help="Quick 20-line overview")
    parser.add_argument("--portfolio", action="store_true", help="Portfolio positions table")
    parser.add_argument("--pemf", action="store_true", help="PEMF venture deep dive")
    parser.add_argument("--risk", action="store_true", help="Risk metrics panel")
    parser.add_argument("--alpha", action="store_true", help="Alpha pipeline view")
    parser.add_argument("--financial", action="store_true", help="Full financial breakdown")
    parser.add_argument("--todo", action="store_true", help="Priority todo list")
    parser.add_argument("--full", action="store_true", help="Show all panels")
    args = parser.parse_args()

    # If no flags specified, default to --full
    any_flag = any([
        args.summary, args.portfolio, args.pemf, args.risk,
        args.alpha, args.financial, args.todo, args.full
    ])
    if not any_flag:
        args.full = True

    # Load ALL data from live filesystem
    positions = load_all_positions()
    financial = load_financial_summary()
    alpha = load_alpha_entries()
    pemf = load_pemf_metrics()
    content = load_content_metrics()
    revenue_history = load_revenue_history()
    expenses = load_expense_breakdown()

    # Calculate risk metrics
    risk = calculate_portfolio_risk(positions, revenue_history, {}, {})

    # Render based on mode
    if args.summary:
        render_summary(positions, financial, pemf, risk, alpha, content)
        return

    if args.full:
        console.print(render_header())
        console.print(render_portfolio_overview(positions, financial))
        console.print(render_financial_panel(financial))
        console.print(render_risk_panel(risk))
        console.print(render_alpha_pipeline(alpha))
        console.print(render_pemf_summary(pemf))
        console.print(render_content_metrics(content))
        console.print(render_expense_breakdown(expenses))
        console.print(render_todo_panel(positions, pemf, financial))
        return

    # Individual panels
    console.print(render_header())

    if args.portfolio:
        console.print(render_portfolio_overview(positions, financial))

    if args.financial:
        console.print(render_financial_panel(financial))
        console.print(render_expense_breakdown(expenses))

    if args.risk:
        console.print(render_risk_panel(risk))

    if args.alpha:
        console.print(render_alpha_pipeline(alpha))

    if args.pemf:
        console.print(render_pemf_summary(pemf))
        console.print(render_pemf_deep_dive(pemf))

    if args.todo:
        console.print(render_todo_panel(positions, pemf, financial))


if __name__ == "__main__":
    main()
