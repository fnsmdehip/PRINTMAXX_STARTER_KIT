"""
PRINTMAXX Portfolio Dashboard - Rich Renderers

All Rich-based rendering functions. Each takes data objects and returns
Rich renderables. Data classes come from data_layer.py (not defined here).
"""

from typing import Any, List, Dict, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich import box
from datetime import datetime


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fmt_currency(val: Any) -> str:
    """Format a number as $X,XXX. Returns '$0' for None/empty."""
    if val is None:
        return "$0"
    try:
        return f"${float(val):,.0f}"
    except (ValueError, TypeError):
        return "$0"


def _fmt_pct(val: Any) -> str:
    """Format a number as X.X%. Returns 'N/A' for None."""
    if val is None:
        return "N/A"
    try:
        return f"{float(val):.1f}%"
    except (ValueError, TypeError):
        return "N/A"


def _fmt_potential(low: Any, high: Any) -> str:
    """Format monthly potential as '$XK-$YK'."""
    try:
        lo = float(low) / 1000 if low else 0
        hi = float(high) / 1000 if high else 0
    except (ValueError, TypeError):
        return "N/A"
    if lo == 0 and hi == 0:
        return "N/A"
    return f"${lo:.0f}K-${hi:.0f}K"


def _safe_float(val: Any, default: float = 0.0) -> float:
    if val is None:
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def _safe_int(val: Any, default: int = 0) -> int:
    if val is None:
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def _status_style(status: str) -> str:
    """Return Rich style string for a given status."""
    s = (status or "").lower().strip()
    if s == "active":
        return "green"
    if s == "planning":
        return "yellow"
    if s == "building":
        return "cyan"
    if s == "paused":
        return "dim"
    return "white"


def _priority_style(priority: str) -> str:
    p = (priority or "").upper().strip()
    if p == "CRITICAL":
        return "bold red"
    if p == "HIGH":
        return "yellow"
    if p == "MEDIUM":
        return "cyan"
    if p == "LOW":
        return "dim"
    return "white"


def _truncate(text: str, max_len: int) -> str:
    if not text:
        return ""
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


# ---------------------------------------------------------------------------
# 1. Header
# ---------------------------------------------------------------------------

def render_header() -> Panel:
    """Bloomberg-style terminal header."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title_line = Text()
    title_line.append("  PRINTMAXX PORTFOLIO TERMINAL", style="bold cyan")
    title_line.append("  |  ", style="dim")
    title_line.append("Jane Street Edition", style="bold cyan")

    info_line = Text()
    info_line.append(f"  {now}", style="dim")
    info_line.append("  |  ", style="dim")
    info_line.append("All Data Live", style="dim")
    info_line.append("  |  ", style="dim")
    info_line.append("v2.0", style="dim")

    content = Text("\n")
    content.append_text(title_line)
    content.append("\n")
    content.append_text(info_line)
    content.append("\n")

    return Panel(content, box=box.DOUBLE, style="cyan")


# ---------------------------------------------------------------------------
# 2. Portfolio Overview
# ---------------------------------------------------------------------------

def render_portfolio_overview(positions: List[Any], financial: Any) -> Panel:
    """Rich table of portfolio positions sorted by status then revenue."""
    table = Table(
        title="PORTFOLIO POSITIONS",
        box=box.HEAVY_HEAD,
        show_lines=False,
        padding=(0, 1),
        expand=True,
    )

    table.add_column("ID", width=8, no_wrap=True)
    table.add_column("Method", width=20, no_wrap=True)
    table.add_column("Cat", width=8, no_wrap=True)
    table.add_column("Status", width=10, no_wrap=True)
    table.add_column("Revenue", width=10, justify="right")
    table.add_column("Expenses", width=10, justify="right")
    table.add_column("Profit", width=10, justify="right")
    table.add_column("Margin", width=8, justify="right")
    table.add_column("Mo. Potential", width=15, justify="right")
    table.add_column("Phase", width=8, no_wrap=True)

    if not positions:
        table.add_row("--", "No positions loaded", "", "", "", "", "", "", "", "")
        return Panel(table, box=box.ROUNDED)

    # Sort: active first, then revenue desc, then synergy desc
    def sort_key(p: Any) -> tuple:
        status = getattr(p, "status", "") or ""
        is_active = 0 if status.lower() == "active" else 1
        rev = -_safe_float(getattr(p, "revenue_total", 0))
        syn = -_safe_float(getattr(p, "synergy_score", 0))
        return (is_active, rev, syn)

    sorted_pos = sorted(positions, key=sort_key)

    total_rev = 0.0
    total_exp = 0.0
    total_profit = 0.0
    display_limit = 20
    shown = 0

    for p in sorted_pos[:display_limit]:
        rev = _safe_float(getattr(p, "revenue_total", 0))
        exp = _safe_float(getattr(p, "expenses_total", 0))
        profit = _safe_float(getattr(p, "profit", 0))
        margin = getattr(p, "margin_pct", None)
        status = getattr(p, "status", "") or ""
        style = _status_style(status)

        profit_style = "green" if profit >= 0 else "red"

        table.add_row(
            str(getattr(p, "method_id", "") or ""),
            _truncate(str(getattr(p, "name", "") or ""), 20),
            _truncate(str(getattr(p, "category", "") or ""), 8),
            Text(status, style=style),
            _fmt_currency(rev),
            _fmt_currency(exp),
            Text(_fmt_currency(profit), style=profit_style),
            _fmt_pct(margin),
            _fmt_potential(
                getattr(p, "monthly_potential_low", 0),
                getattr(p, "monthly_potential_high", 0),
            ),
            str(getattr(p, "phase", "") or ""),
        )

        total_rev += rev
        total_exp += exp
        total_profit += profit
        shown += 1

    remaining = len(sorted_pos) - display_limit
    if remaining > 0:
        # Sum remaining for totals
        for p in sorted_pos[display_limit:]:
            total_rev += _safe_float(getattr(p, "revenue_total", 0))
            total_exp += _safe_float(getattr(p, "expenses_total", 0))
            total_profit += _safe_float(getattr(p, "profit", 0))

        table.add_row(
            "", f"... and {remaining} more", "", "", "", "", "", "", "", "",
            style="dim",
        )

    # Total row
    total_margin = (total_profit / total_rev * 100) if total_rev > 0 else 0
    profit_style = "green" if total_profit >= 0 else "red"
    table.add_row(
        "",
        Text("TOTAL", style="bold"),
        "",
        "",
        Text(_fmt_currency(total_rev), style="bold"),
        Text(_fmt_currency(total_exp), style="bold"),
        Text(_fmt_currency(total_profit), style=f"bold {profit_style}"),
        Text(_fmt_pct(total_margin), style="bold"),
        "",
        "",
        end_section=True,
    )

    return Panel(table, box=box.ROUNDED)


# ---------------------------------------------------------------------------
# 3. Financial Panel
# ---------------------------------------------------------------------------

def render_financial_panel(financial: Any) -> Panel:
    """Two-column financial overview."""
    if financial is None:
        return Panel("No financial data loaded.", title="FINANCIAL OVERVIEW", box=box.ROUNDED)

    rev = _safe_float(getattr(financial, "total_revenue", 0))
    exp = _safe_float(getattr(financial, "total_expenses", 0))
    net = _safe_float(getattr(financial, "net_profit", 0))
    mtd_rev = _safe_float(getattr(financial, "mtd_revenue", 0))
    mtd_exp = _safe_float(getattr(financial, "mtd_expenses", 0))
    burn = _safe_float(getattr(financial, "burn_rate_monthly", 0))
    runway = getattr(financial, "runway_months", None)
    tool_costs = _safe_float(getattr(financial, "tool_costs_monthly", 0))
    active_subs = _safe_int(getattr(financial, "active_subscriptions", 0))

    # Left column: revenue / expenses / P&L
    left = Table(show_header=False, box=None, padding=(0, 1))
    left.add_column("label", width=16)
    left.add_column("value", width=14, justify="right")

    left.add_row("Total Revenue", Text(_fmt_currency(rev), style="green"))
    left.add_row("Total Expenses", Text(_fmt_currency(exp), style="red"))
    net_style = "bold green" if net >= 0 else "bold red"
    left.add_row("Net P&L", Text(_fmt_currency(net), style=net_style))
    left.add_row("", "")
    left.add_row("MTD Revenue", Text(_fmt_currency(mtd_rev), style="green"))
    left.add_row("MTD Expenses", Text(_fmt_currency(mtd_exp), style="red"))

    # Right column: burn rate / runway / tools
    right = Table(show_header=False, box=None, padding=(0, 1))
    right.add_column("label", width=16)
    right.add_column("value", width=14, justify="right")

    right.add_row("Burn Rate /mo", Text(_fmt_currency(burn), style="yellow"))
    runway_str = f"{runway:.1f} mo" if runway is not None else "N/A"
    runway_style = "green" if runway is not None and float(runway) > 6 else "yellow" if runway is not None and float(runway) > 3 else "red"
    right.add_row("Runway", Text(runway_str, style=runway_style))
    right.add_row("Tool Costs /mo", _fmt_currency(tool_costs))
    right.add_row("Active Subs", str(active_subs))

    cols = Columns([left, right], equal=True, expand=True)
    return Panel(cols, title="FINANCIAL OVERVIEW", box=box.ROUNDED)


# ---------------------------------------------------------------------------
# 4. Alpha Pipeline
# ---------------------------------------------------------------------------

def render_alpha_pipeline(alpha_entries: List[Any]) -> Panel:
    """Alpha pipeline counts by status and category, plus top pending."""
    if not alpha_entries:
        return Panel("No alpha entries loaded.", title="ALPHA PIPELINE", box=box.ROUNDED)

    # Count by status
    status_counts: Dict[str, int] = {}
    category_counts: Dict[str, int] = {}
    pending_highest: List[Any] = []

    for e in alpha_entries:
        st = str(getattr(e, "status", "UNKNOWN") or "UNKNOWN").upper()
        cat = str(getattr(e, "category", "OTHER") or "OTHER").upper()
        status_counts[st] = status_counts.get(st, 0) + 1
        category_counts[cat] = category_counts.get(cat, 0) + 1

        if st == "PENDING_REVIEW" and str(getattr(e, "roi_potential", "") or "").upper() == "HIGHEST":
            pending_highest.append(e)

    # Status table
    status_table = Table(show_header=False, box=None, padding=(0, 1))
    status_table.add_column("status", width=20)
    status_table.add_column("count", width=6, justify="right")

    status_order = ["PENDING_REVIEW", "APPROVED", "REJECTED", "ENGAGEMENT_BAIT", "REPURPOSE_ONLY"]
    for s in status_order:
        c = status_counts.get(s, 0)
        if c > 0 or s == "PENDING_REVIEW":
            style = "yellow" if s == "PENDING_REVIEW" else "green" if s == "APPROVED" else "dim"
            status_table.add_row(Text(s, style=style), str(c))

    # Category table
    cat_table = Table(show_header=False, box=None, padding=(0, 1))
    cat_table.add_column("category", width=20)
    cat_table.add_column("count", width=6, justify="right")

    cat_order = ["APP_FACTORY", "CONTENT_FORMAT", "OUTBOUND", "GROWTH_HACK", "TOOL_ALPHA", "MONETIZATION"]
    for cat in cat_order:
        c = category_counts.get(cat, 0)
        if c > 0:
            cat_table.add_row(cat, str(c))
    # Show any other categories not in the standard list
    for cat, c in sorted(category_counts.items()):
        if cat not in cat_order and c > 0:
            cat_table.add_row(cat, str(c))

    # Top 5 highest ROI pending
    top_table = Table(
        title="Top HIGHEST ROI Pending",
        box=None,
        show_header=True,
        padding=(0, 1),
    )
    top_table.add_column("ID", width=10)
    top_table.add_column("Source", width=16)
    top_table.add_column("Tactic", width=50)

    for entry in pending_highest[:5]:
        top_table.add_row(
            str(getattr(entry, "alpha_id", "")),
            _truncate(str(getattr(entry, "source", "")), 16),
            _truncate(str(getattr(entry, "tactic", "")), 50),
        )

    if not pending_highest:
        top_table.add_row("--", "--", "No HIGHEST ROI entries pending")

    # Combine
    parts = Text()
    parts.append(f"Total entries: {len(alpha_entries)}\n\n", style="bold")

    from rich.console import Group
    group = Group(
        Text(f"Total entries: {len(alpha_entries)}\n", style="bold"),
        Columns([status_table, cat_table], equal=True, expand=True),
        Text(""),
        top_table,
    )

    return Panel(group, title="ALPHA PIPELINE", box=box.ROUNDED)


# ---------------------------------------------------------------------------
# 5. Risk Panel
# ---------------------------------------------------------------------------

def render_risk_panel(risk: Any) -> Panel:
    """Portfolio risk metrics table."""
    if risk is None:
        return Panel("No risk data available.", title="RISK METRICS", box=box.ROUNDED)

    table = Table(box=box.SIMPLE_HEAVY, show_header=True, padding=(0, 1), expand=True)
    table.add_column("Metric", width=24)
    table.add_column("Value", width=16, justify="right")
    table.add_column("Status", width=24)

    sharpe = getattr(risk, "portfolio_sharpe", None)
    sortino = getattr(risk, "portfolio_sortino", None)
    data_months = _safe_int(getattr(risk, "sharpe_data_months", 0))
    sharpe_ci = getattr(risk, "sharpe_ci", None)
    var_95 = getattr(risk, "var_95", None)
    var_99 = getattr(risk, "var_99", None)
    cvar_95 = getattr(risk, "cvar_95", None)
    cvar_99 = getattr(risk, "cvar_99", None)
    max_dd = _safe_float(getattr(risk, "max_drawdown", 0))
    current_dd = _safe_float(getattr(risk, "current_drawdown", 0))
    dd_duration = getattr(risk, "drawdown_duration", None)
    hhi_method = _safe_float(getattr(risk, "hhi_method", 0))
    hhi_platform = _safe_float(getattr(risk, "hhi_platform", 0))
    hhi_niche = _safe_float(getattr(risk, "hhi_niche", 0))
    beta = getattr(risk, "beta", None)
    beta_conf = getattr(risk, "beta_confidence", None)
    ic = getattr(risk, "ic", None)
    ic_hit = getattr(risk, "ic_hit_rate", None)
    ic_sample = _safe_int(getattr(risk, "ic_sample_size", 0))

    # Sharpe
    if sharpe is not None and data_months > 0:
        sharpe_val = f"{float(sharpe):.2f}"
        if data_months < 12:
            ci_str = f" CI: {sharpe_ci}" if sharpe_ci else ""
            status = Text(f"Based on {data_months}mo data{ci_str}", style="yellow")
        else:
            style = "green" if float(sharpe) > 1.0 else "yellow" if float(sharpe) > 0 else "red"
            status = Text("OK" if float(sharpe) > 0 else "Negative", style=style)
    else:
        sharpe_val = "N/A"
        status = Text("Insufficient data", style="yellow")
    table.add_row("Sharpe Ratio", sharpe_val, status)

    # Sortino
    if sortino is not None and data_months > 0:
        sortino_val = f"{float(sortino):.2f}"
        style = "green" if float(sortino) > 1.5 else "yellow" if float(sortino) > 0 else "red"
        sortino_status = Text("OK", style=style)
    else:
        sortino_val = "N/A"
        sortino_status = Text("Insufficient data", style="yellow")
    table.add_row("Sortino Ratio", sortino_val, sortino_status)

    # VaR / CVaR (displayed as percentages, not currency)
    for label, val in [("VaR (95%)", var_95), ("VaR (99%)", var_99), ("CVaR (95%)", cvar_95), ("CVaR (99%)", cvar_99)]:
        fval = _safe_float(val)
        if fval > 0:
            table.add_row(label, _fmt_pct(fval), "")
        else:
            table.add_row(label, "N/A", "")

    # Max Drawdown
    dd_style = "green" if max_dd < 10 else "yellow" if max_dd < 25 else "red"
    dd_status_text = "Below threshold" if max_dd < 20 else "Warning" if max_dd < 40 else "Critical"
    table.add_row(
        "Max Drawdown",
        f"{max_dd:.1f}%",
        Text(dd_status_text, style=dd_style),
    )

    # Current Drawdown
    if current_dd > 0:
        dur_str = f" ({dd_duration})" if dd_duration else ""
        table.add_row("Current Drawdown", f"{current_dd:.1f}%{dur_str}", "")

    # HHI (concentration)
    for label, hhi_val in [("HHI (Method)", hhi_method), ("HHI (Platform)", hhi_platform), ("HHI (Niche)", hhi_niche)]:
        hhi_style = "green" if hhi_val < 0.15 else "yellow" if hhi_val < 0.25 else "red"
        hhi_status = "Diversified" if hhi_val < 0.15 else "Moderate" if hhi_val < 0.25 else "Concentrated"
        table.add_row(label, f"{hhi_val:.2f}", Text(hhi_status, style=hhi_style))

    # Beta
    if beta is not None:
        beta_str = f"{float(beta):.2f}"
        conf_str = f" ({beta_conf})" if beta_conf else ""
        table.add_row("Beta", beta_str, Text(f"Confidence{conf_str}", style="dim"))
    else:
        table.add_row("Beta", "N/A", Text("No market data", style="dim"))

    # IC
    if ic is not None and ic_sample > 0:
        ic_str = f"{float(ic):.3f}"
        hit_str = _fmt_pct(ic_hit) if ic_hit is not None else "N/A"
        table.add_row("IC", ic_str, Text(f"Hit rate: {hit_str} (n={ic_sample})", style="dim"))
    else:
        table.add_row("IC", "N/A", Text("No deployed alpha", style="dim"))

    return Panel(table, title="RISK METRICS", box=box.ROUNDED)


# ---------------------------------------------------------------------------
# 6. Content Metrics
# ---------------------------------------------------------------------------

def render_content_metrics(content: Any) -> Panel:
    """Simple content pipeline stats."""
    if content is None:
        return Panel("No content data loaded.", title="CONTENT PIPELINE", box=box.ROUNDED)

    total = _safe_int(getattr(content, "total_pieces", 0))
    queued = _safe_int(getattr(content, "queued", 0))
    published = _safe_int(getattr(content, "published", 0))
    calendar = _safe_int(getattr(content, "calendar_posts", 0))

    table = Table(show_header=True, box=box.SIMPLE, padding=(0, 2), expand=True)
    table.add_column("Total", justify="center")
    table.add_column("Queued", justify="center")
    table.add_column("Published", justify="center")
    table.add_column("Calendar", justify="center")

    table.add_row(
        Text(str(total), style="bold"),
        Text(str(queued), style="yellow"),
        Text(str(published), style="green"),
        Text(str(calendar), style="cyan"),
    )

    return Panel(table, title="CONTENT PIPELINE", box=box.ROUNDED)


# ---------------------------------------------------------------------------
# 7. PEMF Summary
# ---------------------------------------------------------------------------

def render_pemf_summary(pemf: Any) -> Panel:
    """Compact PEMF overview."""
    if pemf is None:
        return Panel("No PEMF data loaded.", title="PEMF VENTURE (WEBERMAXX)", box=box.ROUNDED)

    research_count = _safe_int(getattr(pemf, "research_files_count", 0))
    research_lines = _safe_int(getattr(pemf, "research_total_lines", 0))
    bootstrap = _safe_float(getattr(pemf, "bootstrap_cost", 0))
    cogs_low = _safe_float(getattr(pemf, "unit_cogs_low", 0))
    cogs_high = _safe_float(getattr(pemf, "unit_cogs_high", 0))
    price = _safe_float(getattr(pemf, "price_point", 0))
    margin_low = getattr(pemf, "margin_low", None)
    margin_high = getattr(pemf, "margin_high", None)
    inf_pod = _safe_int(getattr(pemf, "influencers_podcasters", 0))
    inf_tw = _safe_int(getattr(pemf, "influencers_twitter", 0))
    inf_tt = _safe_int(getattr(pemf, "influencers_tiktok", 0))
    inf_total = _safe_int(getattr(pemf, "influencers_total", 0))
    compliance = getattr(pemf, "compliance_path", "") or "N/A"
    mto_count = _safe_int(getattr(pemf, "mto_suppliers_count", 0))

    margin_str = ""
    if margin_low is not None and margin_high is not None:
        margin_str = f" ({_fmt_pct(margin_low)}-{_fmt_pct(margin_high)} margin)"
    elif margin_low is not None:
        margin_str = f" ({_fmt_pct(margin_low)} margin)"

    lines = [
        f"Research: {research_count}/16 files, {research_lines:,} lines",
        f"Bootstrap: {_fmt_currency(bootstrap)} total cost",
        f"Unit Economics: {_fmt_currency(cogs_low)}-{_fmt_currency(cogs_high)} COGS -> {_fmt_currency(price)} price{margin_str}",
        f"Influencers: {inf_pod} podcasters + {inf_tw} twitter + {inf_tt} tiktok = {inf_total}",
        f"Compliance: {compliance}",
        f"MTO Suppliers: {mto_count}",
    ]

    content = Text()
    for i, line in enumerate(lines):
        content.append(line)
        if i < len(lines) - 1:
            content.append("\n")

    return Panel(content, title="PEMF VENTURE (WEBERMAXX)", box=box.ROUNDED)


# ---------------------------------------------------------------------------
# 8. PEMF Deep Dive
# ---------------------------------------------------------------------------

def render_pemf_deep_dive(pemf: Any) -> Panel:
    """Detailed PEMF view with sub-tables."""
    if pemf is None:
        return Panel("No PEMF data loaded.", title="PEMF DEEP DIVE", box=box.ROUNDED)

    from rich.console import Group

    parts = []

    # a) Research file status
    files_status = getattr(pemf, "files_status", None)
    if files_status and isinstance(files_status, dict):
        file_table = Table(title="Research Files", box=box.SIMPLE, padding=(0, 1), expand=True)
        file_table.add_column("File", width=30)
        file_table.add_column("Lines", width=8, justify="right")
        file_table.add_column("Status", width=12)

        for fname, line_count in sorted(files_status.items()):
            lc = _safe_int(line_count)
            fstatus = "Complete" if lc > 0 else "Missing"
            style = "green" if lc > 0 else "red"
            file_table.add_row(fname, str(lc), Text(fstatus, style=style))

        parts.append(file_table)
        parts.append(Text(""))

    # b) Competitive Matrix
    comp_table = Table(title="Competitive Matrix", box=box.SIMPLE, padding=(0, 1), expand=True)
    comp_table.add_column("Competitor", width=14)
    comp_table.add_column("Price", width=12, justify="right")
    comp_table.add_column("Differentiator", width=26)
    comp_table.add_column("Our Advantage", width=28)

    competitors = [
        ("BEMER", "$4,990", "Only 2 freq, MLM", "$699, all frequencies"),
        ("Pulse PEMF", "$5,500+", "Robbins connection", "10x cheaper, Weber focus"),
        ("FluxHealth", "$150-450", "NASA pedigree", "Higher gauss, full body"),
        ("Webermaxx", "$699", "Weber-based, MTO", "Bradet techniques"),
    ]
    for name, price, diff, advantage in competitors:
        style = "bold cyan" if name == "Webermaxx" else ""
        comp_table.add_row(
            Text(name, style=style),
            price,
            diff,
            advantage,
        )

    parts.append(comp_table)
    parts.append(Text(""))

    # c) Influencer Pipeline
    inf_pod = _safe_int(getattr(pemf, "influencers_podcasters", 0))
    inf_tw = _safe_int(getattr(pemf, "influencers_twitter", 0))
    inf_tt = _safe_int(getattr(pemf, "influencers_tiktok", 0))
    inf_total = _safe_int(getattr(pemf, "influencers_total", 0))

    inf_table = Table(title="Influencer Pipeline", box=box.SIMPLE, padding=(0, 1))
    inf_table.add_column("Platform", width=14)
    inf_table.add_column("Count", width=8, justify="right")
    inf_table.add_row("Podcasters", str(inf_pod))
    inf_table.add_row("Twitter/X", str(inf_tw))
    inf_table.add_row("TikTok", str(inf_tt))
    inf_table.add_row(Text("Total", style="bold"), Text(str(inf_total), style="bold"))

    parts.append(inf_table)
    parts.append(Text(""))

    # d) Priority TODOs
    bradet_raw = getattr(pemf, "bradet_techniques", None) or []
    bradet = ", ".join(bradet_raw) if isinstance(bradet_raw, list) else str(bradet_raw)
    todos = [
        ("1", "CRITICAL", "Build PEMF prototype (Bradet coil)", "$62"),
        ("2", "CRITICAL", "FCC Part 18 pre-compliance testing", "$200-500"),
        ("3", "HIGH", "Contact MTO suppliers for quotes", "$0"),
        ("4", "HIGH", "Create landing page for pre-orders", "$0"),
        ("5", "MEDIUM", "Reach out to top 10 influencers", "$0"),
        ("6", "MEDIUM", f"Bradet techniques: {_truncate(bradet, 30)}", "$0"),
    ]

    todo_table = Table(title="PEMF Priority TODOs", box=box.SIMPLE, padding=(0, 1), expand=True)
    todo_table.add_column("#", width=3)
    todo_table.add_column("Priority", width=10)
    todo_table.add_column("Action", width=44)
    todo_table.add_column("Cost", width=10, justify="right")

    for num, pri, action, cost in todos:
        style = _priority_style(pri)
        todo_table.add_row(num, Text(pri, style=style), action, cost)

    parts.append(todo_table)

    group = Group(*parts)
    return Panel(group, title="PEMF DEEP DIVE", box=box.ROUNDED)


# ---------------------------------------------------------------------------
# 9. TODO Panel
# ---------------------------------------------------------------------------

def render_todo_panel(
    positions: Optional[List[Any]] = None,
    pemf: Any = None,
    financial: Any = None,
) -> Panel:
    """Priority-ordered TODO list."""
    table = Table(box=box.SIMPLE_HEAVY, show_header=True, padding=(0, 1), expand=True)
    table.add_column("#", width=3, justify="right")
    table.add_column("Priority", width=10)
    table.add_column("Action", width=42)
    table.add_column("Venture", width=12)
    table.add_column("Cost", width=12, justify="right")

    # Static priority list based on project state
    todos = [
        ("1", "CRITICAL", "Build PEMF prototype", "PEMF", "$62"),
        ("2", "CRITICAL", "Ship PrayerLock to Vercel", "APPS", "$0"),
        ("3", "HIGH", "Upload 130 tweets to Buffer", "CONTENT", "$0"),
        ("4", "HIGH", "Start cold outbound campaign", "OUTBOUND", "$50"),
        ("5", "HIGH", "Create Gumroad account + list templates", "PRODUCTS", "$0"),
        ("6", "MEDIUM", "Set up Beehiiv newsletters", "NEWSLETTER", "$0"),
        ("7", "MEDIUM", "Buy warmed X account for content farm", "CONTENT", "$30-50"),
        ("8", "LOW", "FCC Part 18 testing for PEMF", "PEMF", "$8K-23K"),
    ]

    for num, pri, action, venture, cost in todos:
        style = _priority_style(pri)
        table.add_row(
            num,
            Text(pri, style=style),
            action,
            venture,
            cost,
        )

    return Panel(table, title="PRIORITY ACTIONS", box=box.ROUNDED)


# ---------------------------------------------------------------------------
# 10. Expense Breakdown
# ---------------------------------------------------------------------------

def render_expense_breakdown(expenses: Optional[Dict[str, float]] = None) -> Panel:
    """Table by expense category showing sum per category."""
    table = Table(box=box.SIMPLE_HEAVY, show_header=True, padding=(0, 1), expand=True)
    table.add_column("Category", width=24)
    table.add_column("Amount", width=14, justify="right")
    table.add_column("% of Total", width=10, justify="right")

    if not expenses:
        table.add_row("No expense data", "", "")
        return Panel(table, title="EXPENSE BREAKDOWN", box=box.ROUNDED)

    total = sum(_safe_float(v) for v in expenses.values())

    # Sort by amount descending
    sorted_items = sorted(expenses.items(), key=lambda x: _safe_float(x[1]), reverse=True)

    for cat, amount in sorted_items:
        amt = _safe_float(amount)
        pct = (amt / total * 100) if total > 0 else 0
        table.add_row(
            str(cat),
            _fmt_currency(amt),
            _fmt_pct(pct),
        )

    # Total row
    table.add_row(
        Text("TOTAL", style="bold"),
        Text(_fmt_currency(total), style="bold"),
        Text("100.0%", style="bold"),
        end_section=True,
    )

    return Panel(table, title="EXPENSE BREAKDOWN", box=box.ROUNDED)
