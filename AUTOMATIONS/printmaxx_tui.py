"""
PRINTMAXX Portfolio Terminal - Interactive Textual TUI
Bloomberg-style dashboard with drill-down sub-dashboards per category and method.
Health scoring, pipeline funnel, revenue velocity, live clock.

Run: python3 AUTOMATIONS/printmaxx_tui.py
"""
from __future__ import annotations


import csv
import subprocess
import sys
from pathlib import Path
from datetime import datetime, date
from typing import List, Dict, Optional, Any

# Ensure AUTOMATIONS is on sys.path so portfolio package imports work
AUTOMATIONS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = AUTOMATIONS_DIR.parent
if str(AUTOMATIONS_DIR) not in sys.path:
    sys.path.insert(0, str(AUTOMATIONS_DIR))

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Header, Footer, Static, DataTable, TabbedContent, TabPane, Label, Button,
)
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.binding import Binding
from textual import on
from rich.text import Text

# ---------------------------------------------------------------------------
# Data layer imports
# ---------------------------------------------------------------------------
try:
    from portfolio.data_layer import (
        load_all_positions, load_financial_summary, load_alpha_entries,
        load_content_metrics, load_revenue_history,
        load_expense_breakdown, load_social_accounts, load_daily_ops,
        load_content_pipeline_detailed, load_signal_sources,
        load_active_investments, load_synergies, load_growth_tactics, load_growth_services,
    )
    from portfolio.risk_engine import calculate_portfolio_risk
    from portfolio.hierarchy import (
        METHOD_HIERARCHY, CATEGORY_DISPLAY_NAMES, CATEGORY_ICONS,
        get_category_for_method, get_methods_in_category, get_all_categories,
        get_sub_methods, get_parent_method, is_sub_method,
        SUB_METHOD_PARENTS,
    )
    from portfolio.health_scoring import (
        compute_method_health, compute_pipeline_funnel,
        compute_top_opportunities, compute_revenue_velocity,
    )
except ImportError as exc:
    print(f"Import error: {exc}")
    METHOD_HIERARCHY = {}
    CATEGORY_DISPLAY_NAMES = {}
    CATEGORY_ICONS = {}
    SUB_METHOD_PARENTS = {}

    def get_category_for_method(m): return "UNCATEGORIZED"
    def get_methods_in_category(c): return []
    def get_all_categories(): return []
    def get_sub_methods(p): return []
    def get_parent_method(c): return None
    def is_sub_method(m): return False
    def load_all_positions(): return []
    def load_financial_summary():
        from dataclasses import dataclass
        @dataclass
        class _FS:
            total_revenue: float = 0.0; total_expenses: float = 0.0
            net_profit: float = 0.0; mtd_revenue: float = 0.0
            mtd_expenses: float = 0.0; burn_rate_monthly: float = 0.0
            runway_months: float = 0.0; tool_costs_monthly: float = 0.0
            active_subscriptions: int = 0
        return _FS()
    def load_alpha_entries(): return []
    def load_content_metrics(): return None
    def load_revenue_history(): return []
    def load_expense_breakdown(): return {}
    def load_social_accounts(): return []
    def load_daily_ops(): return []
    def load_content_pipeline_detailed(): return []
    def load_signal_sources(): return []
    def calculate_portfolio_risk(positions, revenue_history, platform_revenue, niche_revenue):
        from portfolio.risk_engine import PortfolioRisk
        return PortfolioRisk()
    def compute_method_health(mid, pos, alpha, files): return {"score": 0, "breakdown": {}, "grade": "F", "color": "red"}
    def compute_pipeline_funnel(pos): return {"stages": {}, "conversions": {}, "total_methods": 0}
    def compute_top_opportunities(pos, alpha, files): return []
    def compute_revenue_velocity(fin, pos): return {"daily_burn": 0, "monthly_burn": 0, "methods_with_revenue": 0, "methods_without_revenue": 0, "total_invested": 0, "total_revenue": 0, "roi_pct": 0, "revenue_per_method": 0}
    def load_active_investments(): return []
    def load_synergies(): return []
    def load_growth_tactics(): return []
    def load_growth_services(): return []


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def _fc(val: float) -> str:
    if val == 0:
        return "$0"
    return f"${val:,.0f}"

def _fp(val: float) -> str:
    return f"{val:.1f}%"

def _trunc(s: str, n: int = 40) -> str:
    if not s:
        return ""
    return s[:n - 3] + "..." if len(s) > n else s

def _parse_budget(val: str) -> int:
    """Parse budget tier string like '$150' to int. Returns 0 for free/$0."""
    try:
        return int(val.replace("$", "").replace(",", "").strip())
    except (ValueError, TypeError):
        return 0


SPARK_BLOCKS = "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588"  # ▁▂▃▄▅▆▇█

def _sparkline(values: list, width: int = 8) -> str:
    """Generate a sparkline string from a list of numeric values."""
    if not values:
        return ""
    recent = values[-width:]
    mn, mx = min(recent), max(recent)
    if mn == mx:
        return SPARK_BLOCKS[4] * len(recent)
    scaled = [(v - mn) / (mx - mn) for v in recent]
    return "".join(SPARK_BLOCKS[int(s * 7)] for s in scaled)

def _health_grade(score: float) -> tuple:
    """Return (grade_label, color) for a 0-100 health score."""
    if score >= 80:
        return ("A", "green")
    elif score >= 60:
        return ("B", "cyan")
    elif score >= 40:
        return ("C", "yellow")
    elif score >= 20:
        return ("D", "#cc6600")
    else:
        return ("F", "red")


def _method_dir(method_id: str) -> Optional[Path]:
    """Find the MONEY_METHODS directory for a method, if it exists."""
    name_map = {
        "MM001": "APP_FACTORY", "MM002": "INFO_PRODUCTS", "MM003": "AFFILIATE_SITES",
        "MM004": "SAAS", "MM005": "AGENCY_SERVICES", "MM006": "CONTENT_FARM",
        "MM007": "COLD_OUTBOUND", "MM008": "UGC_ARBITRAGE", "MM009": "AI_INFLUENCER",
        "MM010": "STREAMER_CLIPS", "MM011": "ROBLOX_GAMES", "MM012": "ALGO_TRADING",
        "MM013": "PAID_ADS", "MM014": "YOUTUBE_LONGFORM", "MM015": "NEWSLETTER",
        "MM016": "TIKTOK_SHOP", "MM022": "ECOM_DROPSHIP", "MM024": "PRINT_ON_DEMAND",
        "MM025": "DIGITAL_PRODUCTS", "MM026": "AMAZON_KDP", "MM036": "ETSY_DIGITAL",
        "PEMF_WEBERMAXX": "PEMF",
    }
    dirname = name_map.get(method_id)
    if dirname:
        d = PROJECT_ROOT / "MONEY_METHODS" / dirname
        if d.exists():
            return d
    d = PROJECT_ROOT / "MONEY_METHODS" / method_id
    return d if d.exists() else None


def _scan_method_files(method_id: str) -> List[Dict[str, Any]]:
    """Scan filesystem for files related to a method."""
    d = _method_dir(method_id)
    if not d:
        return []
    files = []
    for f in sorted(d.rglob("*")):
        if f.is_file() and not f.name.startswith(".") and "node_modules" not in str(f):
            try:
                size = f.stat().st_size
            except OSError:
                size = 0
            files.append({
                "name": str(f.relative_to(d)),
                "size": size,
                "ext": f.suffix,
            })
    return files[:50]


# ---------------------------------------------------------------------------
# Per-method tool recommendations
# ---------------------------------------------------------------------------

METHOD_TOOLS = {
    "MM001": ["Xcode/Android Studio", "RevenueCat", "Firebase", "TestFlight", "ASO tools"],
    "MM002": ["Gumroad", "Notion", "Canva", "ConvertKit", "Stripe"],
    "MM003": ["WordPress", "Ahrefs/SEMrush", "ShareASale", "Amazon Associates"],
    "MM004": ["Vercel/Railway", "Stripe", "PostHog", "Crisp chat"],
    "MM005": ["GoHighLevel", "Calendly", "Stripe", "Loom"],
    "MM006": ["Buffer/Publer", "Canva", "CapCut", "Later"],
    "MM007": ["Instantly/Smartlead", "Apollo.io", "Hunter.io", "Calendly"],
    "MM008": ["Fiverr", "HeyGen", "ElevenLabs", "CapCut"],
    "MM009": ["ComfyUI/Leonardo.ai", "ElevenLabs", "HeyGen", "Anti-detect browser"],
    "MM010": ["yt-dlp", "Whisper", "FFmpeg", "Claude"],
    "MM011": ["Roblox Studio", "Luau", "DevForum"],
    "MM012": ["Alpaca API", "QuantConnect", "TradingView"],
    "MM013": ["Meta Ads Manager", "TikTok Ads", "Google Ads"],
    "MM014": ["Premiere Pro/DaVinci", "TubeBuddy", "vidIQ"],
    "MM015": ["Beehiiv", "ConvertKit", "Buttondown"],
    "MM016": ["TikTok Seller Center", "CJ Dropshipping"],
    "MM022": ["Shopify", "DSers", "CJ Dropshipping"],
    "MM024": ["Printful/Printify", "Canva", "Etsy/Shopify"],
    "MM025": ["Gumroad", "Notion", "Canva", "Whop"],
    "MM026": ["Amazon KDP", "Canva", "Kindle Create"],
    "MM029": ["Google My Business", "CallRail", "GoHighLevel"],
    "MM070": ["Python scrapers", "Claude API", "SMTP"],
}

METHOD_GTM = {
    "MM001": ["App Store SEO (ASO)", "Product Hunt", "Reddit", "Twitter/X", "TikTok demos"],
    "MM002": ["Twitter/X threads", "Gumroad discovery", "Newsletter", "Medium/Substack"],
    "MM003": ["SEO/GEO", "Pinterest", "Reddit", "Niche forums"],
    "MM004": ["Product Hunt", "Hacker News", "Twitter/X", "Cold email"],
    "MM005": ["LinkedIn outreach", "Cold email", "Twitter DMs", "Upwork/referrals"],
    "MM006": ["Platform organic", "Cross-posting", "Hashtag strategy", "Engagement pods"],
    "MM007": ["Multi-inbox cold email", "LinkedIn automation", "Apollo sequences"],
    "MM009": ["Twitter/X", "Fanvue/Fansly", "Reddit", "Telegram"],
    "MM013": ["Meta Ads", "TikTok Ads", "Google Ads", "Retargeting"],
    "MM015": ["Beehiiv recommendations", "Twitter/X CTA", "Cross-promotion"],
    "MM024": ["Etsy SEO", "Pinterest", "TikTok organic", "Instagram Reels"],
    "MM025": ["Gumroad discovery", "Twitter/X", "Reddit", "Newsletter"],
    "MM029": ["Google Maps SEO", "Cold calling", "Door-to-door", "Facebook groups"],
    "MM070": ["Cold email", "LinkedIn outreach", "Local SEO directories"],
}


# ---------------------------------------------------------------------------
# Shared CSS for all screens
# ---------------------------------------------------------------------------

SHARED_CSS = """
Screen {
    background: #0a0a0a;
}
Header {
    background: #001a1a;
    color: #00cccc;
}
Footer {
    background: #001a1a;
}
TabbedContent {
    background: #0a0a0a;
}
TabPane {
    background: #0a0a0a;
    padding: 0;
}
ContentSwitcher {
    background: #0a0a0a;
}
.banner {
    width: 1fr;
    height: 3;
    background: #001a2a;
    color: #00cccc;
    text-align: center;
    padding: 1;
    text-style: bold;
}
.sub-banner {
    width: 1fr;
    height: 3;
    background: #1a0a2a;
    color: #cc99ff;
    text-align: center;
    padding: 1;
    text-style: bold;
}
.stat-row {
    layout: horizontal;
    height: auto;
    width: 1fr;
    margin: 0 0 1 0;
}
.stat-box {
    width: 1fr;
    height: 5;
    border: solid #004444;
    content-align: center middle;
    margin: 0 1;
    padding: 0 1;
    background: #0a1a1a;
}
.stat-box-green {
    width: 1fr;
    height: 5;
    border: solid #004400;
    content-align: center middle;
    margin: 0 1;
    padding: 0 1;
    background: #0a1a0a;
}
.stat-box-red {
    width: 1fr;
    height: 5;
    border: solid #440000;
    content-align: center middle;
    margin: 0 1;
    padding: 0 1;
    background: #1a0a0a;
}
.stat-box-yellow {
    width: 1fr;
    height: 5;
    border: solid #444400;
    content-align: center middle;
    margin: 0 1;
    padding: 0 1;
    background: #1a1a0a;
}
.section-title {
    margin: 1 1 0 1;
    color: #00cccc;
    text-style: bold;
}
DataTable {
    height: 1fr;
    background: #0a0a0a;
}
DataTable > .datatable--header {
    background: #001a2a;
    color: #00cccc;
    text-style: bold;
}
DataTable > .datatable--cursor {
    background: #002a2a;
}
DataTable > .datatable--even-row {
    background: #0d0d0d;
}
.detail-panel {
    height: 1fr;
    border: solid #004444;
    margin: 1;
    background: #0a1a1a;
}
.detail-title {
    margin: 0 1;
    color: #cccc00;
    text-style: bold;
}
.filter-bar {
    layout: horizontal;
    height: 3;
    width: 1fr;
    margin: 0 1;
}
.filter-btn {
    width: auto;
    min-width: 12;
    margin: 0 1;
    background: #0a1a1a;
    border: solid #004444;
    color: #aaaaaa;
}
.filter-btn-active {
    width: auto;
    min-width: 12;
    margin: 0 1;
    background: #002a2a;
    border: solid #00cccc;
    color: #00cccc;
    text-style: bold;
}
.ops-group-title {
    margin: 1 1 0 1;
    color: #cccc00;
    text-style: bold;
}
.scroll-area {
    height: 1fr;
    width: 1fr;
}
.back-btn {
    margin: 0 1;
    background: #1a0a1a;
    border: solid #440044;
    color: #cc99ff;
    width: auto;
    min-width: 16;
}
/* Health grade indicators */
.health-excellent { color: #00ff88; }
.health-good { color: #88cc00; }
.health-fair { color: #cccc00; }
.health-poor { color: #cc6600; }
.health-critical { color: #ff3333; }
/* Automation launcher */
.auto-btn-row {
    layout: horizontal;
    height: auto;
    width: 1fr;
    margin: 0 0 1 0;
}
.auto-btn {
    width: 1fr;
    margin: 0 1;
    min-width: 18;
    background: #0a1a1a;
    border: solid #004444;
    color: #00cccc;
}
.auto-btn-warn {
    width: 1fr;
    margin: 0 1;
    min-width: 18;
    background: #1a1a0a;
    border: solid #444400;
    color: #cccc00;
}
.auto-btn-safe {
    width: 1fr;
    margin: 0 1;
    min-width: 18;
    background: #0a1a0a;
    border: solid #004400;
    color: #00ff88;
}
.auto-log-box {
    height: 12;
    width: 1fr;
    border: solid #002a2a;
    margin: 0 1;
    padding: 1;
    background: #050a0a;
    color: #888888;
    overflow-y: auto;
}
.auto-schedule-box {
    height: auto;
    width: 1fr;
    border: solid #004444;
    margin: 0 1;
    padding: 1;
    background: #0a1a1a;
}
"""


# ============================================================================
# SUB-DASHBOARD: Method Detail Screen
# ============================================================================

class MethodScreen(Screen):
    """Full sub-dashboard for a single method with deep drill-down data."""

    BINDINGS = [
        Binding("escape", "pop_screen", "Back"),
        Binding("q", "quit", "Quit"),
    ]

    CSS = SHARED_CSS

    def __init__(self, method_id: str, positions, alpha, **kwargs):
        super().__init__(**kwargs)
        self._method_id = method_id
        self._positions = positions
        self._alpha = alpha
        self._pos = None
        for p in positions:
            if p.method_id == method_id:
                self._pos = p
                break

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(
            Static("", id="method-banner", classes="sub-banner"),
            Button("<< Back to Category", id="back-btn", classes="back-btn"),
            Horizontal(
                Static("", id="m-status", classes="stat-box"),
                Static("", id="m-phase", classes="stat-box"),
                Static("", id="m-revenue", classes="stat-box-green"),
                Static("", id="m-expenses", classes="stat-box-red"),
                classes="stat-row",
            ),
            Horizontal(
                Static("", id="m-profit", classes="stat-box"),
                Static("", id="m-potential", classes="stat-box-yellow"),
                Static("", id="m-category", classes="stat-box"),
                Static("", id="m-parent", classes="stat-box"),
                classes="stat-row",
            ),
            Horizontal(
                Static("", id="m-files-count", classes="stat-box"),
                Static("", id="m-subs-count", classes="stat-box"),
                Static("", id="m-alpha-count", classes="stat-box"),
                Static("", id="m-health", classes="stat-box"),
                classes="stat-row",
            ),
            Label("PRIORITY ACTIONS", classes="section-title"),
            DataTable(id="method-actions"),
            Label("METHOD DETAILS", classes="section-title"),
            DataTable(id="method-details"),
            Label("", id="alpha-summary", classes="section-title"),
            DataTable(id="method-alpha"),
            Label("", id="files-summary", classes="section-title"),
            DataTable(id="method-files"),
            Label("", id="sub-methods-title", classes="section-title"),
            DataTable(id="method-subs"),
            Label("", id="siblings-title", classes="section-title"),
            DataTable(id="method-siblings"),
            Label("RECOMMENDED TOOLS", classes="section-title"),
            DataTable(id="method-tools"),
            Label("GTM CHANNELS", classes="section-title"),
            DataTable(id="method-gtm"),
            Label("SYNERGIES", classes="section-title"),
            DataTable(id="method-synergies"),
            classes="scroll-area",
        )
        yield Footer()

    def on_mount(self) -> None:
        p = self._pos
        mid = self._method_id
        name = p.name if p else mid
        positions_by_id = {pos.method_id: pos for pos in self._positions}

        self.query_one("#method-banner", Static).update(f"METHOD: {mid} - {name}")

        status = p.status if p else "Unknown"
        phase = p.phase if p else ""
        rev = p.revenue_total if p else 0.0
        exp = p.expenses_total if p else 0.0
        profit = p.profit if p else 0.0
        pot_lo = p.monthly_potential_low if p else 0.0
        pot_hi = p.monthly_potential_high if p else 0.0
        cat = get_category_for_method(mid) or "N/A"
        cat_display = CATEGORY_DISPLAY_NAMES.get(cat, cat)
        parent = get_parent_method(mid)
        children = get_sub_methods(mid)
        method_files = _scan_method_files(mid)

        # Related alpha
        mid_lower = mid.lower()
        name_lower = (name or "").lower()
        related_alpha = []
        for a in self._alpha:
            tactic = str(getattr(a, "tactic", "")).lower()
            a_cat = str(getattr(a, "category", "")).lower()
            if mid_lower in tactic or mid_lower in a_cat or (name_lower and len(name_lower) > 3 and name_lower in tactic):
                related_alpha.append(a)

        sibling_ids = [s for s in get_methods_in_category(cat) if s != mid] if cat and cat != "N/A" else []

        # Health score
        health = compute_method_health(mid, p, self._alpha, method_files)

        # Row 1
        status_color = "green" if status == "Active" else "cyan" if status == "Building" else "yellow" if status == "Research" else "dim"
        self.query_one("#m-status", Static).update(Text.from_markup(f"[bold {status_color}]STATUS[/]\n{status}"))
        self.query_one("#m-phase", Static).update(Text.from_markup(f"[bold]PHASE[/]\n{phase or 'N/A'}"))
        self.query_one("#m-revenue", Static).update(Text.from_markup(f"[bold green]REVENUE[/]\n{_fc(rev)}"))
        self.query_one("#m-expenses", Static).update(Text.from_markup(f"[bold red]EXPENSES[/]\n{_fc(exp)}"))

        # Row 2
        pnl_color = "green" if profit >= 0 else "red"
        self.query_one("#m-profit", Static).update(Text.from_markup(f"[bold {pnl_color}]PROFIT[/]\n{_fc(profit)}"))
        pot_str = f"${pot_lo/1000:.0f}K-${pot_hi/1000:.0f}K/mo" if (pot_lo > 0 or pot_hi > 0) else "N/A"
        self.query_one("#m-potential", Static).update(Text.from_markup(f"[bold yellow]POTENTIAL[/]\n{pot_str}"))
        self.query_one("#m-category", Static).update(Text.from_markup(f"[bold]CATEGORY[/]\n{cat_display}"))
        self.query_one("#m-parent", Static).update(Text.from_markup(f"[bold]PARENT[/]\n{parent or 'Top-level'}"))

        # Row 3
        self.query_one("#m-files-count", Static).update(Text.from_markup(f"[bold]FILES ON DISK[/]\n{len(method_files)}"))
        self.query_one("#m-subs-count", Static).update(Text.from_markup(f"[bold]SUB-METHODS[/]\n{len(children)}"))
        alpha_pending = sum(1 for a in related_alpha if (getattr(a, "status", "") or "").upper() == "PENDING_REVIEW")
        self.query_one("#m-alpha-count", Static).update(Text.from_markup(f"[bold]RELATED ALPHA[/]\n{len(related_alpha)}"))
        h_grade, h_color = _health_grade(health["score"])
        self.query_one("#m-health", Static).update(Text.from_markup(f"[bold {h_color}]HEALTH[/]\n{health['score']}/100 ({h_grade})"))

        # Priority actions
        actions_table = self.query_one("#method-actions", DataTable)
        actions_table.clear(columns=True)
        actions_table.add_columns("#", "Priority", "Action")
        action_items = []
        if rev == 0:
            action_items.append(("CRITICAL", "No revenue yet - ship or activate this method"))
        if (status or "").lower() == "building":
            action_items.append(("HIGH", "Still in Building phase - complete and launch"))
        if (status or "").lower() == "research":
            action_items.append(("HIGH", "Still in Research - move to Building"))
        if not method_files:
            action_items.append(("HIGH", "No files in MONEY_METHODS/ - nothing built yet"))
        if alpha_pending > 0:
            action_items.append(("MEDIUM", f"Review {alpha_pending} related pending alpha entries"))
        if children:
            active_children = sum(1 for cid in children if (getattr(positions_by_id.get(cid), "status", "") or "").lower() == "active")
            if active_children == 0:
                action_items.append(("MEDIUM", "No active sub-methods - activate at least one"))
        if (pot_hi > 5000 or pot_lo > 5000) and rev == 0:
            action_items.append(("HIGH", "High potential method earning $0 - prioritize"))
        if exp > 0 and rev == 0:
            action_items.append(("MEDIUM", f"${exp:,.0f} expenses with $0 revenue - check ROI"))
        if not action_items:
            action_items.append(("INFO", "No critical actions identified"))
        for i, (pri, action) in enumerate(action_items, 1):
            actions_table.add_row(str(i), pri, action)

        # Method details table
        details_table = self.query_one("#method-details", DataTable)
        details_table.clear(columns=True)
        details_table.add_columns("Field", "Value")
        details_table.add_row("method_id", mid)
        details_table.add_row("name", name or "N/A")
        details_table.add_row("status", status)
        details_table.add_row("phase", phase or "N/A")
        details_table.add_row("revenue_total", _fc(rev))
        details_table.add_row("expenses_total", _fc(exp))
        details_table.add_row("profit", _fc(profit))
        details_table.add_row("monthly_potential_low", _fc(pot_lo))
        details_table.add_row("monthly_potential_high", _fc(pot_hi))
        details_table.add_row("category", f"{cat} ({cat_display})")
        details_table.add_row("parent_method", parent or "None (top-level)")
        details_table.add_row("is_sub_method", str(is_sub_method(mid)))
        details_table.add_row("health_score", f"{health['score']}/100 ({health['grade']})")

        # Related alpha
        alpha_approved = sum(1 for a in related_alpha if (getattr(a, "status", "") or "").upper() == "APPROVED")
        self.query_one("#alpha-summary", Label).update(
            f"RELATED ALPHA - {len(related_alpha)} entries ({alpha_pending} pending, {alpha_approved} approved)"
        )
        alpha_table = self.query_one("#method-alpha", DataTable)
        alpha_table.clear(columns=True)
        alpha_table.add_columns("ID", "Tactic", "ROI", "Status")
        if related_alpha:
            for a in related_alpha[:30]:
                alpha_table.add_row(
                    str(getattr(a, "alpha_id", "")),
                    _trunc(str(getattr(a, "tactic", "")), 50),
                    str(getattr(a, "roi_potential", "")),
                    str(getattr(a, "status", "")),
                )
        else:
            alpha_table.add_row("--", "No related alpha found", "", "")

        # Filesystem deep dive
        files_summary_label = self.query_one("#files-summary", Label)
        files_table = self.query_one("#method-files", DataTable)
        files_table.clear(columns=True)
        files_table.add_columns("File", "Size", "Type")
        if method_files:
            total_size = sum(f["size"] for f in method_files)
            ext_counts: Dict[str, int] = {}
            for f in method_files:
                ext = f["ext"] if f["ext"] else "(none)"
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
            ext_parts = sorted(ext_counts.items(), key=lambda x: -x[1])
            ext_breakdown = ", ".join(f"{cnt} {ext}" for ext, cnt in ext_parts[:6])
            if total_size < 1024:
                total_size_str = f"{total_size}B"
            elif total_size < 1_048_576:
                total_size_str = f"{total_size/1024:.1f}KB"
            else:
                total_size_str = f"{total_size/1_048_576:.1f}MB"
            files_summary_label.update(f"FILESYSTEM - {len(method_files)} files, {total_size_str} ({ext_breakdown})")
            for f in method_files:
                if f["size"] < 1024:
                    size_str = f"{f['size']}B"
                elif f["size"] < 1_048_576:
                    size_str = f"{f['size']/1024:.1f}KB"
                else:
                    size_str = f"{f['size']/1_048_576:.1f}MB"
                files_table.add_row(_trunc(f["name"], 55), size_str, f["ext"] or "(none)")
        else:
            files_summary_label.update("FILESYSTEM - 0 files")
            files_table.add_row("--", "--", f"No files for {mid}")

        # Sub-methods
        sub_title = self.query_one("#sub-methods-title", Label)
        sub_table = self.query_one("#method-subs", DataTable)
        sub_table.clear(columns=True)
        if children:
            active_subs = sum(1 for cid in children if (getattr(positions_by_id.get(cid), "status", "") or "").lower() == "active")
            building_subs = sum(1 for cid in children if (getattr(positions_by_id.get(cid), "status", "") or "").lower() == "building")
            sub_title.update(f"SUB-METHODS ({len(children)}) - {active_subs} active, {building_subs} building")
            sub_table.add_columns("ID", "Name", "Status", "Revenue", "Phase")
            for cid in children:
                cp = positions_by_id.get(cid)
                sub_table.add_row(cid, _trunc(cp.name if cp else cid, 30), cp.status if cp else "Unknown", _fc(cp.revenue_total if cp else 0), cp.phase if cp else "")
        else:
            sub_title.update("")

        # Siblings
        siblings_title = self.query_one("#siblings-title", Label)
        siblings_table = self.query_one("#method-siblings", DataTable)
        siblings_table.clear(columns=True)
        if sibling_ids:
            siblings_title.update(f"SIBLING METHODS ({len(sibling_ids)}) - {cat_display}")
            siblings_table.add_columns("ID", "Name", "Status", "Revenue")
            for sid in sibling_ids[:10]:
                sp = positions_by_id.get(sid)
                siblings_table.add_row(sid, _trunc(sp.name if sp else sid, 30), sp.status if sp else "Unknown", _fc(sp.revenue_total if sp else 0))
        else:
            siblings_title.update("")

        # Recommended tools
        tools_table = self.query_one("#method-tools", DataTable)
        tools_table.clear(columns=True)
        tools_table.add_columns("#", "Tool")
        tools_list = METHOD_TOOLS.get(mid, [])
        if tools_list:
            for i, tool in enumerate(tools_list, 1):
                tools_table.add_row(str(i), tool)
        else:
            tools_table.add_row("--", f"No tools mapped for {mid}")

        # GTM channels
        gtm_table = self.query_one("#method-gtm", DataTable)
        gtm_table.clear(columns=True)
        gtm_table.add_columns("#", "Channel")
        gtm_list = METHOD_GTM.get(mid, [])
        if gtm_list:
            for i, ch in enumerate(gtm_list, 1):
                gtm_table.add_row(str(i), ch)
        else:
            gtm_table.add_row("--", f"No GTM channels mapped for {mid}")

        # Method synergies
        syn_table = self.query_one("#method-synergies", DataTable)
        syn_table.clear(columns=True)
        syn_table.add_columns("Score", "Combo", "Name", "Multiplier")
        syn_table.add_row("--", "See Overview tab", "Synergies cross-reference", "--")

    @on(Button.Pressed, "#back-btn")
    def go_back(self) -> None:
        self.app.pop_screen()

    def action_pop_screen(self) -> None:
        self.app.pop_screen()


# ============================================================================
# SUB-DASHBOARD: Category Detail Screen
# ============================================================================

class CategoryScreen(Screen):
    """Full sub-dashboard for a venture category with health scoring,
    priority actions, status breakdown, alpha pipeline, and filesystem summary."""

    BINDINGS = [
        Binding("escape", "pop_screen", "Back"),
        Binding("q", "quit", "Quit"),
    ]

    CSS = SHARED_CSS

    def __init__(self, category: str, positions, alpha, **kwargs):
        super().__init__(**kwargs)
        self._category = category
        self._positions = positions
        self._alpha = alpha

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(
            Static("", id="cat-banner", classes="sub-banner"),
            Button("<< Back to Ventures", id="back-btn", classes="back-btn"),
            # Row 1: Methods, Active, Building, Revenue
            Horizontal(
                Static("", id="cat-methods", classes="stat-box"),
                Static("", id="cat-active", classes="stat-box-green"),
                Static("", id="cat-building", classes="stat-box"),
                Static("", id="cat-revenue", classes="stat-box-green"),
                classes="stat-row",
            ),
            # Row 2: Expenses, Profit, Avg Potential, Category Health
            Horizontal(
                Static("", id="cat-expenses", classes="stat-box-red"),
                Static("", id="cat-profit", classes="stat-box"),
                Static("", id="cat-potential", classes="stat-box-yellow"),
                Static("", id="cat-health", classes="stat-box"),
                classes="stat-row",
            ),
            # Row 3: Files total, With builds, Zero files, Pending alpha
            Horizontal(
                Static("", id="cat-files-total", classes="stat-box"),
                Static("", id="cat-methods-with-builds", classes="stat-box-green"),
                Static("", id="cat-methods-zero-files", classes="stat-box-red"),
                Static("", id="cat-alpha-pending", classes="stat-box-yellow"),
                classes="stat-row",
            ),
            Label("PRIORITY ACTIONS", classes="section-title"),
            DataTable(id="cat-actions-table"),
            Label("METHODS (click to drill in)", classes="section-title"),
            DataTable(id="cat-methods-table"),
            Label("STATUS BREAKDOWN", classes="section-title"),
            Static("", id="cat-status-breakdown"),
            Label("", id="cat-alpha-title", classes="section-title"),
            Horizontal(
                Static("", id="cat-alpha-total", classes="stat-box"),
                Static("", id="cat-alpha-pending-box", classes="stat-box-yellow"),
                Static("", id="cat-alpha-approved-box", classes="stat-box-green"),
                classes="stat-row",
            ),
            DataTable(id="cat-alpha-table"),
            Label("", id="cat-fs-title", classes="section-title"),
            DataTable(id="cat-fs-table"),
            classes="scroll-area",
        )
        yield Footer()

    def on_mount(self) -> None:
        cat = self._category
        display_name = CATEGORY_DISPLAY_NAMES.get(cat, cat)
        icon = CATEGORY_ICONS.get(cat, "")

        self.query_one("#cat-banner", Static).update(f"{icon} {display_name} - CATEGORY DASHBOARD")

        method_ids = get_methods_in_category(cat)
        positions_by_id = {p.method_id: p for p in self._positions}

        # Aggregate category metrics
        cat_rev = 0.0
        cat_exp = 0.0
        cat_profit = 0.0
        active_count = 0
        building_count = 0
        research_count = 0
        other_count = 0
        pots_lo = []
        pots_hi = []
        health_scores = []
        total_files = 0
        methods_with_builds = 0
        methods_zero_files = 0
        method_file_data = {}

        for mid in method_ids:
            pos = positions_by_id.get(mid)
            rev = pos.revenue_total if pos else 0.0
            exp = pos.expenses_total if pos else 0.0
            profit_val = pos.profit if pos else 0.0
            status = (pos.status or "").lower() if pos else ""
            pot_lo = pos.monthly_potential_low if pos else 0.0
            pot_hi = pos.monthly_potential_high if pos else 0.0

            cat_rev += rev
            cat_exp += exp
            cat_profit += profit_val

            if status == "active":
                active_count += 1
            elif status == "building":
                building_count += 1
            elif status == "research":
                research_count += 1
            else:
                other_count += 1

            if pot_lo > 0 or pot_hi > 0:
                pots_lo.append(pot_lo)
                pots_hi.append(pot_hi)

            mfiles = _scan_method_files(mid)
            method_file_data[mid] = mfiles
            fcount = len(mfiles)
            total_files += fcount
            if fcount > 0:
                methods_with_builds += 1
            else:
                methods_zero_files += 1

            # Health score
            h_data = compute_method_health(mid, pos, self._alpha, mfiles)
            health_scores.append(h_data["score"])

        # Related alpha
        cat_lower = cat.lower()
        display_lower = display_name.lower()
        related_alpha = [
            a for a in self._alpha
            if cat_lower in str(getattr(a, "category", "")).lower()
            or display_lower in str(getattr(a, "category", "")).lower()
        ]
        alpha_pending = sum(1 for a in related_alpha if (getattr(a, "status", "") or "").upper() == "PENDING_REVIEW")
        alpha_approved = sum(1 for a in related_alpha if (getattr(a, "status", "") or "").upper() == "APPROVED")
        avg_health = sum(health_scores) / len(health_scores) if health_scores else 0

        # --- Stat boxes ---
        self.query_one("#cat-methods", Static).update(Text.from_markup(f"[bold]METHODS[/]\n{len(method_ids)}"))
        self.query_one("#cat-active", Static).update(Text.from_markup(f"[bold green]ACTIVE[/]\n{active_count}"))
        self.query_one("#cat-building", Static).update(Text.from_markup(f"[bold cyan]BUILDING[/]\n{building_count}"))
        self.query_one("#cat-revenue", Static).update(Text.from_markup(f"[bold green]TOTAL REVENUE[/]\n{_fc(cat_rev)}"))

        self.query_one("#cat-expenses", Static).update(Text.from_markup(f"[bold red]TOTAL EXPENSES[/]\n{_fc(cat_exp)}"))
        pnl_color = "green" if cat_profit >= 0 else "red"
        self.query_one("#cat-profit", Static).update(Text.from_markup(f"[bold {pnl_color}]NET PROFIT[/]\n{_fc(cat_profit)}"))
        pot_str = f"${sum(pots_lo)/len(pots_lo)/1000:.0f}K-${sum(pots_hi)/len(pots_hi)/1000:.0f}K/mo" if pots_hi else "N/A"
        self.query_one("#cat-potential", Static).update(Text.from_markup(f"[bold yellow]AVG POTENTIAL[/]\n{pot_str}"))
        h_color = "green" if avg_health >= 70 else "yellow" if avg_health >= 40 else "red"
        self.query_one("#cat-health", Static).update(Text.from_markup(f"[bold {h_color}]HEALTH[/]\n{avg_health:.0f}/100"))

        self.query_one("#cat-files-total", Static).update(Text.from_markup(f"[bold]FILES ON DISK[/]\n{total_files}"))
        self.query_one("#cat-methods-with-builds", Static).update(Text.from_markup(f"[bold green]WITH BUILDS[/]\n{methods_with_builds}"))
        self.query_one("#cat-methods-zero-files", Static).update(Text.from_markup(f"[bold red]ZERO FILES[/]\n{methods_zero_files}"))
        self.query_one("#cat-alpha-pending", Static).update(Text.from_markup(f"[bold yellow]PENDING ALPHA[/]\n{alpha_pending}"))

        # --- Priority actions ---
        actions_table = self.query_one("#cat-actions-table", DataTable)
        actions_table.clear(columns=True)
        actions_table.add_columns("#", "Priority", "Action")
        action_items = []

        if cat_rev == 0:
            action_items.append(("CRITICAL", "Entire category earning $0 - ship something"))
        for mid in method_ids:
            pos = positions_by_id.get(mid)
            if pos and (pos.status or "").lower() == "building":
                action_items.append(("HIGH", f"Complete {mid} ({_trunc(pos.name, 25)}) - still building"))
        for mid in method_ids:
            pos = positions_by_id.get(mid)
            if pos:
                pot = max(pos.monthly_potential_low, pos.monthly_potential_high)
                if pos.revenue_total == 0 and pot > 5000:
                    action_items.append(("HIGH", f"High potential {mid} earning $0 (pot ${pot/1000:.0f}K/mo)"))
        for mid in method_ids:
            if not method_file_data.get(mid):
                pos = positions_by_id.get(mid)
                action_items.append(("MEDIUM", f"{mid} ({_trunc((pos.name if pos else mid), 25)}) has no build files"))
        if alpha_pending > 0:
            action_items.append(("MEDIUM", f"Review {alpha_pending} pending alpha entries"))
        for mid in method_ids:
            pos = positions_by_id.get(mid)
            if pos and (pos.status or "").lower() == "research":
                action_items.append(("MEDIUM", f"{mid} still in Research phase"))
        if not action_items:
            action_items.append(("INFO", "No critical actions identified"))
        for i, (pri, action) in enumerate(action_items, 1):
            actions_table.add_row(str(i), pri, action)

        # --- Methods table with health score ---
        methods_table = self.query_one("#cat-methods-table", DataTable)
        methods_table.clear(columns=True)
        methods_table.cursor_type = "row"
        methods_table.add_columns("ID", "Name", "Status", "Revenue", "Expenses", "Profit", "Potential", "Phase", "Files", "Health")

        for idx, mid in enumerate(method_ids):
            pos = positions_by_id.get(mid)
            is_sub = mid in SUB_METHOD_PARENTS
            prefix = "  " if is_sub else ""
            name = pos.name if pos else mid
            status = pos.status if pos else "Unknown"
            rev = pos.revenue_total if pos else 0.0
            exp = pos.expenses_total if pos else 0.0
            profit_val = pos.profit if pos else 0.0
            pot_lo = pos.monthly_potential_low if pos else 0.0
            pot_hi = pos.monthly_potential_high if pos else 0.0
            phase = pos.phase if pos else ""
            fcount = len(method_file_data.get(mid, []))
            h = health_scores[idx] if idx < len(health_scores) else 0

            pot_str = f"${pot_lo/1000:.0f}K-${pot_hi/1000:.0f}K" if (pot_lo > 0 or pot_hi > 0) else ""
            if h >= 70:
                health_text = Text(str(h), style="bold green")
            elif h >= 40:
                health_text = Text(str(h), style="bold yellow")
            else:
                health_text = Text(str(h), style="bold red")

            methods_table.add_row(
                f"{prefix}{mid}", _trunc(f"{prefix}{name}", 30), status,
                _fc(rev), _fc(exp), _fc(profit_val), pot_str, phase,
                str(fcount) if fcount > 0 else "", health_text, key=mid,
            )

        # --- Status breakdown bar chart ---
        total_methods = len(method_ids)
        max_bar = 20
        parts = [("Active", active_count, "green"), ("Building", building_count, "cyan"),
                 ("Research", research_count, "yellow"), ("Other", other_count, "dim")]
        breakdown_lines = []
        for label, count, color in parts:
            if count > 0:
                bar_len = max(1, round(count / total_methods * max_bar)) if total_methods > 0 else 0
                bar = "\u2588" * bar_len
                breakdown_lines.append(f"[{color}]{label} {bar} {count}[/{color}]")
        self.query_one("#cat-status-breakdown", Static).update(
            Text.from_markup("  ".join(breakdown_lines) if breakdown_lines else "No methods")
        )

        # --- Alpha pipeline ---
        self.query_one("#cat-alpha-title", Label).update(f"CATEGORY ALPHA PIPELINE ({len(related_alpha)} entries)")
        self.query_one("#cat-alpha-total", Static).update(Text.from_markup(f"[bold]TOTAL[/]\n{len(related_alpha)}"))
        self.query_one("#cat-alpha-pending-box", Static).update(Text.from_markup(f"[bold yellow]PENDING[/]\n{alpha_pending}"))
        self.query_one("#cat-alpha-approved-box", Static).update(Text.from_markup(f"[bold green]APPROVED[/]\n{alpha_approved}"))

        alpha_table = self.query_one("#cat-alpha-table", DataTable)
        alpha_table.clear(columns=True)
        alpha_table.add_columns("ID", "Tactic", "ROI", "Status")
        if related_alpha:
            for a in related_alpha[:30]:
                alpha_table.add_row(
                    str(getattr(a, "alpha_id", "")), _trunc(str(getattr(a, "tactic", "")), 50),
                    str(getattr(a, "roi_potential", "")), str(getattr(a, "status", "")),
                )
        else:
            alpha_table.add_row("--", "No alpha tagged to this category", "", "")

        # --- Filesystem summary ---
        self.query_one("#cat-fs-title", Label).update(f"FILESYSTEM ({total_files} files across {methods_with_builds} methods)")
        fs_table = self.query_one("#cat-fs-table", DataTable)
        fs_table.clear(columns=True)
        fs_table.add_columns("ID", "Has Dir", "Files", "Size", "Extensions")
        for mid in method_ids:
            mfiles = method_file_data.get(mid, [])
            mdir = _method_dir(mid)
            has_dir = "Y" if (mdir and mdir.exists()) else "N"
            fcount = len(mfiles)
            total_size = sum(f["size"] for f in mfiles)
            if total_size == 0:
                size_str = "0B"
            elif total_size < 1024:
                size_str = f"{total_size}B"
            elif total_size < 1_048_576:
                size_str = f"{total_size / 1024:.1f}KB"
            else:
                size_str = f"{total_size / 1_048_576:.1f}MB"
            ext_counts = {}
            for f in mfiles:
                ext = f["ext"] if f["ext"] else "(none)"
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
            ext_str = ", ".join(f"{cnt}{ext}" for ext, cnt in sorted(ext_counts.items(), key=lambda x: -x[1])[:4])
            fs_table.add_row(mid, has_dir, str(fcount), size_str, ext_str)

    @on(DataTable.RowSelected, "#cat-methods-table")
    def on_method_selected(self, event: DataTable.RowSelected) -> None:
        row_key = event.row_key
        if row_key and row_key.value:
            self.app.push_screen(MethodScreen(row_key.value, self._positions, self._alpha))

    @on(Button.Pressed, "#back-btn")
    def go_back(self) -> None:
        self.app.pop_screen()

    def action_pop_screen(self) -> None:
        self.app.pop_screen()


# ============================================================================
# MAIN APP
# ============================================================================

VENTURE_SORT_CYCLE = ["name", "revenue", "profit", "potential"]


class PrintmaxxTUI(App):
    """PRINTMAXX Portfolio Terminal."""

    TITLE = "PRINTMAXX PORTFOLIO TERMINAL"
    SUB_TITLE = "Jane Street Edition"

    CSS = SHARED_CSS

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("s", "sort_ventures", "Sort Ventures"),
        Binding("1", "tab_1", "Overview", show=False),
        Binding("2", "tab_2", "Ventures", show=False),
        Binding("3", "tab_3", "Alpha", show=False),
        Binding("4", "tab_4", "Research", show=False),
        Binding("5", "tab_5", "Social", show=False),
        Binding("6", "tab_6", "Financial", show=False),
        Binding("7", "tab_7", "Risk", show=False),
        Binding("8", "tab_8", "Health Lab", show=False),
        Binding("9", "tab_9", "GTM", show=False),
        Binding("0", "tab_0", "Infra", show=False),
        Binding("a", "tab_auto", "Automations", show=False),
    ]

    def __init__(self):
        super().__init__()
        self._positions = []
        self._financial = None
        self._alpha = []
        self._content = None
        self._risk = None
        self._social = []
        self._daily_ops = []
        self._signal_sources = []
        self._expense_breakdown = {}
        self._alpha_filter = "ALL"
        self._venture_sort_key = "name"
        self._health_data = []
        self._gtm_map = {}
        self._infra_tools = []
        self._ab_tests = []
        self._content_calendar = []
        self._outreach_pipeline = []
        self._account_health = []
        self._health_checklist = []
        self._investments = []
        self._synergies = []
        self._growth_tactics = []
        self._growth_services = []

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(
            "Overview", "Ventures", "Alpha",
            "Research", "Social", "Financial", "Risk",
            "Health Lab", "GTM", "Infra", "Automations",
            id="tabs",
        ):
            # Tab 1: Overview
            with TabPane("Overview", id="tab-overview"):
                yield ScrollableContainer(
                    Static("", id="overview-banner", classes="banner"),
                    Horizontal(
                        Static("", id="stat-revenue", classes="stat-box-green"),
                        Static("", id="stat-expenses", classes="stat-box-red"),
                        Static("", id="stat-pnl", classes="stat-box"),
                        Static("", id="stat-burn", classes="stat-box-yellow"),
                        classes="stat-row",
                    ),
                    Horizontal(
                        Static("", id="stat-active", classes="stat-box"),
                        Static("", id="stat-building", classes="stat-box"),
                        Static("", id="stat-alpha", classes="stat-box"),
                        Static("", id="stat-content", classes="stat-box"),
                        classes="stat-row",
                    ),
                    Horizontal(
                        Static("", id="stat-sharpe", classes="stat-box"),
                        Static("", id="stat-var", classes="stat-box"),
                        Static("", id="stat-hhi", classes="stat-box"),
                        Static("", id="stat-methods", classes="stat-box"),
                        classes="stat-row",
                    ),
                    Horizontal(
                        Static("", id="stat-content-ready", classes="stat-box-green"),
                        Static("", id="stat-outreach-leads", classes="stat-box"),
                        Static("", id="stat-ops-active", classes="stat-box"),
                        Static("", id="stat-edge-alive", classes="stat-box-yellow"),
                        classes="stat-row",
                    ),
                    Label("PRIORITY ACTIONS", classes="section-title"),
                    DataTable(id="overview-actions"),
                    Label("PIPELINE FUNNEL", classes="section-title"),
                    DataTable(id="overview-pipeline"),
                    Label("TOP OPPORTUNITIES (highest potential, lowest readiness)", classes="section-title"),
                    DataTable(id="overview-opportunities"),
                    Label("REVENUE VELOCITY", classes="section-title"),
                    Horizontal(
                        Static("", id="vel-daily-burn", classes="stat-box-red"),
                        Static("", id="vel-monthly-burn", classes="stat-box-red"),
                        Static("", id="vel-roi", classes="stat-box"),
                        Static("", id="vel-rev-per-method", classes="stat-box-green"),
                        classes="stat-row",
                    ),
                    Horizontal(
                        Static("", id="vel-with-rev", classes="stat-box-green"),
                        Static("", id="vel-without-rev", classes="stat-box-yellow"),
                        Static("", id="vel-total-invested", classes="stat-box"),
                        Static("", id="vel-total-revenue", classes="stat-box-green"),
                        classes="stat-row",
                    ),
                    Label("ACTIVE INVESTMENTS", classes="section-title"),
                    DataTable(id="investments-table"),
                    Label("TOP SYNERGIES", classes="section-title"),
                    DataTable(id="synergies-table"),
                    classes="scroll-area",
                )

            # Tab 2: Ventures
            with TabPane("Ventures", id="tab-ventures"):
                yield ScrollableContainer(
                    Label("VENTURE CATEGORIES (Enter/click to open dashboard | S to sort)", classes="section-title"),
                    DataTable(id="ventures-table"),
                    classes="scroll-area",
                )

            # Tab 3: Alpha
            with TabPane("Alpha", id="tab-alpha"):
                yield Vertical(
                    Horizontal(
                        Button("All", id="filter-all", variant="primary", classes="filter-btn-active"),
                        Button("Pending", id="filter-pending", classes="filter-btn"),
                        Button("Approved", id="filter-approved", classes="filter-btn"),
                        Button("Rejected", id="filter-rejected", classes="filter-btn"),
                        classes="filter-bar",
                    ),
                    Horizontal(
                        Static("", id="alpha-total", classes="stat-box"),
                        Static("", id="alpha-pending", classes="stat-box-yellow"),
                        Static("", id="alpha-approved", classes="stat-box-green"),
                        Static("", id="alpha-rejected", classes="stat-box-red"),
                        classes="stat-row",
                    ),
                    DataTable(id="alpha-table"),
                )

            # Tab 4: Ops Center (Research + Operations + Automation)
            with TabPane("Research", id="tab-research"):
                yield ScrollableContainer(
                    Label("DAILY OPS CHECKLIST (click row to toggle status)", classes="section-title"),
                    Label("Daily", classes="ops-group-title"),
                    DataTable(id="ops-daily"),
                    Label("Weekly", classes="ops-group-title"),
                    DataTable(id="ops-weekly"),
                    Label("Monthly / Continuous", classes="ops-group-title"),
                    DataTable(id="ops-monthly"),
                    Label("AUTOMATION LAUNCHER", classes="section-title"),
                    Horizontal(
                        Button("Alpha Scan", id="run-alpha-scan", variant="primary"),
                        Button("Reddit Scrape", id="run-reddit-scrape", variant="primary"),
                        Button("GitHub Trending", id="run-github-trending", variant="primary"),
                        Button("Refresh All", id="run-refresh-all", variant="warning"),
                        classes="stat-row",
                    ),
                    Label("PLATFORM DAILY LIMITS REFERENCE", classes="section-title"),
                    DataTable(id="platform-limits"),
                    Label("EDGE TACTICS STATUS (Jan 2026)", classes="section-title"),
                    DataTable(id="edge-tactics"),
                    Label("SIGNAL SOURCES (Top 20)", classes="section-title"),
                    DataTable(id="signal-sources"),
                    Label("SUGGESTED RESEARCH", classes="section-title"),
                    Static("", id="research-suggestions"),
                    classes="scroll-area",
                )

            # Tab 5: Social & Growth
            with TabPane("Social", id="tab-social"):
                yield ScrollableContainer(
                    Label("SOCIAL ACCOUNTS BY NICHE", classes="section-title"),
                    DataTable(id="social-table"),
                    Label("ACCOUNT HEALTH MONITOR", classes="section-title"),
                    DataTable(id="account-health-table"),
                    Label("CONTENT PIPELINE", classes="section-title"),
                    Horizontal(
                        Static("", id="content-total-posts", classes="stat-box"),
                        Static("", id="content-pending", classes="stat-box-yellow"),
                        Static("", id="content-published", classes="stat-box-green"),
                        Static("", id="content-niches", classes="stat-box"),
                        classes="stat-row",
                    ),
                    Label("OUTREACH PIPELINE", classes="section-title"),
                    Horizontal(
                        Static("", id="outreach-total", classes="stat-box"),
                        Static("", id="outreach-active", classes="stat-box-green"),
                        Static("", id="outreach-pipeline-value", classes="stat-box-yellow"),
                        Static("", id="outreach-qualified", classes="stat-box-green"),
                        classes="stat-row",
                    ),
                    DataTable(id="outreach-table"),
                    Label("GROWTH TACTICS BY PLATFORM", classes="section-title"),
                    DataTable(id="growth-tactics-table"),
                    Label("GROWTH SERVICES & PRICING", classes="section-title"),
                    DataTable(id="growth-services-table"),
                    classes="scroll-area",
                )

            # Tab 6: Financial (upgraded)
            with TabPane("Financial", id="tab-financial"):
                yield ScrollableContainer(
                    Label("P&L SUMMARY", classes="section-title"),
                    Horizontal(
                        Static("", id="fin-revenue", classes="stat-box-green"),
                        Static("", id="fin-expenses", classes="stat-box-red"),
                        Static("", id="fin-net", classes="stat-box"),
                        Static("", id="fin-burn", classes="stat-box-yellow"),
                        classes="stat-row",
                    ),
                    DataTable(id="financial-pnl"),
                    Label("EXPENSE ROI BY METHOD", classes="section-title"),
                    DataTable(id="expense-roi-method"),
                    Label("COST EFFICIENCY METRICS", classes="section-title"),
                    Horizontal(
                        Static("", id="fin-cost-per-method", classes="stat-box"),
                        Static("", id="fin-cost-per-active", classes="stat-box"),
                        Static("", id="fin-cash-efficiency", classes="stat-box"),
                        Static("", id="fin-expense-concentration", classes="stat-box-yellow"),
                        classes="stat-row",
                    ),
                    Label("EXPENSE TIMELINE (Recent 20)", classes="section-title"),
                    DataTable(id="expense-timeline"),
                    Label("TOOL COSTS & SUBSCRIPTIONS", classes="section-title"),
                    Horizontal(
                        Static("", id="fin-tool-costs", classes="stat-box"),
                        Static("", id="fin-active-subs", classes="stat-box"),
                        Static("", id="fin-burn-rate", classes="stat-box"),
                        Static("", id="fin-runway", classes="stat-box"),
                        classes="stat-row",
                    ),
                    Label("EXPENSE BREAKDOWN BY CATEGORY", classes="section-title"),
                    DataTable(id="expense-breakdown"),
                    classes="scroll-area",
                )

            # Tab 7: Risk
            with TabPane("Risk", id="tab-risk"):
                yield ScrollableContainer(
                    Label("PORTFOLIO RISK METRICS", classes="section-title"),
                    DataTable(id="risk-table"),
                    classes="scroll-area",
                )

            # Tab 8: Health Lab
            with TabPane("Health Lab", id="tab-health"):
                yield ScrollableContainer(
                    Label("HEALTH & PERFORMANCE STACK", classes="section-title"),
                    Horizontal(
                        Static("", id="health-active", classes="stat-box-green"),
                        Static("", id="health-cost", classes="stat-box-yellow"),
                        Static("", id="health-protocols", classes="stat-box"),
                        Static("", id="health-biomarkers", classes="stat-box"),
                        classes="stat-row",
                    ),
                    Label("ACTIVE SUPPLEMENTS", classes="section-title"),
                    DataTable(id="health-supplements"),
                    Label("PROTOCOLS", classes="section-title"),
                    DataTable(id="health-protocols-table"),
                    Label("BIOMARKER TRACKING", classes="section-title"),
                    DataTable(id="health-biomarkers-table"),
                    Label("DIET FRAMEWORK", classes="section-title"),
                    DataTable(id="health-diet-table"),
                    Label("QUEUED (NEXT UP)", classes="section-title"),
                    DataTable(id="health-queued"),
                    Label("DAILY HEALTH CHECKLIST (click row to toggle)", classes="section-title"),
                    Horizontal(
                        Static("", id="health-done-count", classes="stat-box-green"),
                        Static("", id="health-pending-count", classes="stat-box-yellow"),
                        Static("", id="health-streak-max", classes="stat-box"),
                        Static("", id="health-completion-pct", classes="stat-box-green"),
                        classes="stat-row",
                    ),
                    DataTable(id="health-daily-checklist"),
                    classes="scroll-area",
                )

            # Tab 9: GTM Synergies
            with TabPane("GTM", id="tab-gtm"):
                yield ScrollableContainer(
                    Label("GTM SYNERGY MAP (Venture -> Channel Stacks)", classes="section-title"),
                    Horizontal(
                        Static("", id="gtm-total-channels", classes="stat-box"),
                        Static("", id="gtm-active-channels", classes="stat-box-green"),
                        Static("", id="gtm-est-cost", classes="stat-box-yellow"),
                        Static("", id="gtm-categories", classes="stat-box"),
                        classes="stat-row",
                    ),
                    Label("VENTURE GTM STACKS (category -> recommended channels + cost)", classes="section-title"),
                    DataTable(id="gtm-venture-map"),
                    Label("CHANNEL DIRECTORY", classes="section-title"),
                    DataTable(id="gtm-channel-dir"),
                    classes="scroll-area",
                )

            # Tab 10: Infra Command Center (reads TOOLS_SERVICES_MASTER.csv + STACK_AB_TESTS.csv)
            with TabPane("Infra", id="tab-infra"):
                yield ScrollableContainer(
                    Label("INFRASTRUCTURE COMMAND CENTER", classes="section-title"),
                    Horizontal(
                        Static("", id="infra-total", classes="stat-box"),
                        Static("", id="infra-active", classes="stat-box-green"),
                        Static("", id="infra-free", classes="stat-box-green"),
                        Static("", id="infra-monthly-cost", classes="stat-box-yellow"),
                        classes="stat-row",
                    ),
                    Horizontal(
                        Static("", id="infra-ab-running", classes="stat-box"),
                        Static("", id="infra-categories", classes="stat-box"),
                        Static("", id="infra-upgrades-count", classes="stat-box-yellow"),
                        Static("", id="infra-budget-tier", classes="stat-box-green"),
                        classes="stat-row",
                    ),
                    Label("CURRENT ACTIVE STACK", classes="section-title"),
                    DataTable(id="infra-active-stack"),
                    Label("RECOMMENDED UPGRADES (highest priority available)", classes="section-title"),
                    DataTable(id="infra-upgrades-table"),
                    Label("BUDGET TIER PROGRESSION", classes="section-title"),
                    DataTable(id="infra-budget-tiers"),
                    Label("STACK A/B TESTS", classes="section-title"),
                    DataTable(id="infra-ab-tests"),
                    Label("PER-VENTURE RECOMMENDED STACKS", classes="section-title"),
                    DataTable(id="infra-venture-stacks"),
                    Label("FULL TOOL DIRECTORY", classes="section-title"),
                    DataTable(id="infra-all-tools"),
                    classes="scroll-area",
                )

            # Tab 11: Automations Command Center
            with TabPane("Automations", id="tab-automations"):
                yield ScrollableContainer(
                    Label("AUTOMATION COMMAND CENTER", classes="section-title"),
                    Horizontal(
                        Static("", id="auto-total-runs", classes="stat-box"),
                        Static("", id="auto-last-run", classes="stat-box-green"),
                        Static("", id="auto-next-run", classes="stat-box"),
                        Static("", id="auto-watchdog-status", classes="stat-box-green"),
                        classes="stat-row",
                    ),
                    Label("DAILY AUTOMATIONS", classes="section-title"),
                    Horizontal(
                        Button("Morning Sync", id="auto-morning", classes="auto-btn"),
                        Button("Content Gen", id="auto-content", classes="auto-btn"),
                        Button("Outreach", id="auto-outreach", classes="auto-btn"),
                        Button("Evening Digest", id="auto-digest", classes="auto-btn"),
                        classes="auto-btn-row",
                    ),
                    Horizontal(
                        Button("Nightly Backup", id="auto-backup", classes="auto-btn-safe"),
                        Button("Overnight Sprint", id="auto-overnight", classes="auto-btn-warn"),
                        Button("Status Check", id="auto-status", classes="auto-btn"),
                        Button("Refresh Data", id="auto-refresh-data", classes="auto-btn"),
                        classes="auto-btn-row",
                    ),
                    Label("PERIODIC AUTOMATIONS", classes="section-title"),
                    Horizontal(
                        Button("Weekly Tasks", id="auto-weekly", classes="auto-btn-warn"),
                        Button("Monthly Tasks", id="auto-monthly", classes="auto-btn-warn"),
                        Button("Full Validation", id="auto-validate", classes="auto-btn-safe"),
                        Button("Run ALL Quick", id="auto-run-all-quick", classes="auto-btn-warn"),
                        classes="auto-btn-row",
                    ),
                    Label("RESEARCH AUTOMATIONS", classes="section-title"),
                    Horizontal(
                        Button("Alpha Scan", id="auto-alpha-scan", classes="auto-btn"),
                        Button("Reddit Scrape", id="auto-reddit", classes="auto-btn"),
                        Button("GitHub Trending", id="auto-github", classes="auto-btn"),
                        Button("Competitor Intel", id="auto-competitor", classes="auto-btn"),
                        classes="auto-btn-row",
                    ),
                    Label("ACTIVE SCHEDULE (launchd)", classes="section-title"),
                    Static("", id="auto-schedule-display", classes="auto-schedule-box"),
                    Label("RECENT WATCHDOG LOGS", classes="section-title"),
                    Static("", id="auto-log-display", classes="auto-log-box"),
                    Label("SAFETY WATCHDOG THRESHOLDS", classes="section-title"),
                    Static("", id="auto-thresholds", classes="auto-schedule-box"),
                    classes="scroll-area",
                )

        yield Footer()

    def on_mount(self) -> None:
        self._load_data()
        self._populate_all()
        self._update_tab_badges()
        self.set_interval(1, self._update_clock)

    def _update_clock(self) -> None:
        """Live clock + stats in banner and header subtitle."""
        now = datetime.now().strftime("%H:%M:%S")
        pending = sum(1 for a in self._alpha if (getattr(a, "status", "") or "").upper() == "PENDING_REVIEW")
        active_count = sum(1 for p in self._positions if (getattr(p, "status", "") or "").lower() == "active")
        total_methods = len(self._positions)

        try:
            banner = self.query_one("#overview-banner", Static)
            banner.update(
                f"PRINTMAXX PORTFOLIO TERMINAL | {now} | "
                f"{total_methods} methods | {active_count} active | "
                f"{pending} alpha pending"
            )
        except Exception:
            pass

        fin = self._financial
        if fin:
            rev = getattr(fin, "total_revenue", 0.0)
            exp = getattr(fin, "total_expenses", 0.0)
            pnl = getattr(fin, "net_profit", 0.0)
            self.sub_title = f"R: {_fc(rev)} | E: {_fc(exp)} | P&L: {_fc(pnl)} | Methods: {total_methods}"

    def _update_tab_badges(self) -> None:
        """Add count badges to tab labels."""
        try:
            from textual.widgets import Tab
        except ImportError:
            return

        health_active = sum(1 for r in self._health_data if r.get("status", "").upper() == "ACTIVE")
        badge_data = {
            "tab-ventures": len(get_all_categories()),
            "tab-alpha": len(self._alpha),
            "tab-research": len(self._daily_ops),
            "tab-social": len(self._social),
            "tab-health": health_active,
            "tab-gtm": len(self._gtm_channels),
            "tab-infra": len(self._infra_tools),
        }
        tab_names = {
            "tab-ventures": "Ventures",
            "tab-alpha": "Alpha",
            "tab-research": "Research",
            "tab-social": "Social",
            "tab-health": "Health Lab",
            "tab-gtm": "GTM",
            "tab-infra": "Infra",
        }
        for pane_id, count in badge_data.items():
            tab_id = f"--content-tab-{pane_id}"
            try:
                tab_widget = self.query_one(f"#{tab_id}", Tab)
                base_name = tab_names.get(pane_id, pane_id)
                tab_widget.label = f"{base_name} ({count})"
            except Exception:
                pass

    def _load_data(self) -> None:
        self._positions = load_all_positions()
        self._financial = load_financial_summary()
        self._alpha = load_alpha_entries()
        self._content = load_content_metrics()
        self._social = load_social_accounts()
        self._daily_ops = load_daily_ops()
        # S-tier sources from copy-style.md get absolute priority in the list
        _s_tier_handles = {"pipelineabuser", "tom777kruise", "codyschneiderxx", "bluecow009",
                           "caiden_cole", "knoxtwts", "levelsio", "dannypostmaa", "marc_louvion"}
        _quality_rank = {"HIGHEST": 1, "HIGH": 2, "MEDIUM": 3, "LOW": 4}
        def _source_sort_key(s):
            name = getattr(s, "source_name", "").lower().lstrip("@")
            tier = 0 if name in _s_tier_handles else _quality_rank.get(getattr(s, "signal_quality", "LOW"), 9)
            return (tier, name)
        self._signal_sources = sorted(load_signal_sources(), key=_source_sort_key)
        self._expense_breakdown = load_expense_breakdown()
        self._investments = load_active_investments()
        self._synergies = load_synergies()
        self._growth_tactics = load_growth_tactics()
        self._growth_services = load_growth_services()

        rev_history = load_revenue_history()
        platform_revenue: Dict[str, float] = {}
        niche_revenue: Dict[str, float] = {}
        for r in rev_history:
            plat = (r.get("platform", "") or "OTHER").strip()
            amt = 0.0
            try:
                amt = float(r.get("revenue", 0) or 0)
            except (ValueError, TypeError):
                pass
            platform_revenue[plat] = platform_revenue.get(plat, 0.0) + amt
            niche = (r.get("niche", "") or "OTHER").strip()
            niche_revenue[niche] = niche_revenue.get(niche, 0.0) + amt

        self._risk = calculate_portfolio_risk(
            self._positions, rev_history, platform_revenue, niche_revenue
        )

        # Health stack data
        health_csv = PROJECT_ROOT / "LEDGER" / "HEALTH_STACK.csv"
        self._health_data = []
        if health_csv.exists():
            try:
                with open(health_csv, newline="", encoding="utf-8") as f:
                    self._health_data = list(csv.DictReader(f))
            except Exception:
                pass

        # GTM channels
        channels_csv = PROJECT_ROOT / "LEDGER" / "MARKETING_CHANNELS_MASTER.csv"
        self._gtm_channels = []
        if channels_csv.exists():
            try:
                with open(channels_csv, newline="", encoding="utf-8") as f:
                    self._gtm_channels = list(csv.DictReader(f))
            except Exception:
                pass

        # Infra tools (from TOOLS_SERVICES_MASTER.csv)
        tools_csv = PROJECT_ROOT / "LEDGER" / "TOOLS_SERVICES_MASTER.csv"
        self._infra_tools = []
        if tools_csv.exists():
            try:
                with open(tools_csv, newline="", encoding="utf-8") as f:
                    self._infra_tools = list(csv.DictReader(f))
            except Exception:
                pass

        # Stack A/B tests (from STACK_AB_TESTS.csv)
        ab_csv = PROJECT_ROOT / "LEDGER" / "STACK_AB_TESTS.csv"
        self._ab_tests = []
        if ab_csv.exists():
            try:
                with open(ab_csv, newline="", encoding="utf-8") as f:
                    self._ab_tests = list(csv.DictReader(f))
            except Exception:
                pass

        # Content calendar (CONTENT_CALENDAR_30DAY.csv)
        cal_csv = PROJECT_ROOT / "LEDGER" / "CONTENT_CALENDAR_30DAY.csv"
        self._content_calendar = []
        if cal_csv.exists():
            try:
                with open(cal_csv, newline="", encoding="utf-8") as f:
                    self._content_calendar = list(csv.DictReader(f))
            except Exception:
                pass

        # Outreach pipeline
        outreach_csv = PROJECT_ROOT / "LEDGER" / "OUTREACH_PIPELINE.csv"
        self._outreach_pipeline = []
        if outreach_csv.exists():
            try:
                with open(outreach_csv, newline="", encoding="utf-8") as f:
                    self._outreach_pipeline = list(csv.DictReader(f))
            except Exception:
                pass

        # Account health
        acct_health_csv = PROJECT_ROOT / "LEDGER" / "ACCOUNT_HEALTH_DAILY.csv"
        self._account_health = []
        if acct_health_csv.exists():
            try:
                with open(acct_health_csv, newline="", encoding="utf-8") as f:
                    self._account_health = list(csv.DictReader(f))
            except Exception:
                pass

        # Health daily checklist
        health_cl_csv = PROJECT_ROOT / "LEDGER" / "HEALTH_DAILY_CHECKLIST.csv"
        self._health_checklist = []
        if health_cl_csv.exists():
            try:
                with open(health_cl_csv, newline="", encoding="utf-8") as f:
                    self._health_checklist = list(csv.DictReader(f))
            except Exception:
                pass

    def _populate_all(self) -> None:
        self._populate_overview()
        self._populate_ventures()
        self._populate_alpha()
        self._populate_research()
        self._populate_social()
        self._populate_financial()
        self._populate_risk()
        self._populate_health()
        self._populate_gtm()
        self._populate_infra()
        self._populate_automations()

    # -------------------------------------------------------------------
    # TAB 1: OVERVIEW
    # -------------------------------------------------------------------

    def _populate_overview(self) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.query_one("#overview-banner", Static).update(
            f"PRINTMAXX PORTFOLIO TERMINAL | {now}"
        )

        fin = self._financial
        total_rev = getattr(fin, "total_revenue", 0.0) if fin else 0.0
        total_exp = getattr(fin, "total_expenses", 0.0) if fin else 0.0
        net_pnl = getattr(fin, "net_profit", 0.0) if fin else 0.0
        burn = getattr(fin, "burn_rate_monthly", 0.0) if fin else 0.0

        self.query_one("#stat-revenue", Static).update(Text.from_markup(f"[bold green]REVENUE[/]\n{_fc(total_rev)}"))
        self.query_one("#stat-expenses", Static).update(Text.from_markup(f"[bold red]EXPENSES[/]\n{_fc(total_exp)}"))
        pnl_color = "green" if net_pnl >= 0 else "red"
        self.query_one("#stat-pnl", Static).update(Text.from_markup(f"[bold {pnl_color}]NET P&L[/]\n{_fc(net_pnl)}"))
        self.query_one("#stat-burn", Static).update(Text.from_markup(f"[bold yellow]BURN RATE/MO[/]\n{_fc(burn)}"))

        active_count = sum(1 for p in self._positions if (getattr(p, "status", "") or "").lower() == "active")
        building_count = sum(1 for p in self._positions if (getattr(p, "status", "") or "").lower() == "building")
        alpha_pending = sum(1 for a in self._alpha if (getattr(a, "status", "") or "").upper() == "PENDING_REVIEW")
        content_queued = getattr(self._content, "queued", 0) if self._content else 0

        self.query_one("#stat-active", Static).update(Text.from_markup(f"[bold cyan]ACTIVE METHODS[/]\n{active_count}"))
        self.query_one("#stat-building", Static).update(Text.from_markup(f"[bold cyan]BUILDING[/]\n{building_count}"))
        self.query_one("#stat-alpha", Static).update(Text.from_markup(f"[bold yellow]ALPHA PENDING[/]\n{alpha_pending}"))
        self.query_one("#stat-content", Static).update(Text.from_markup(f"[bold cyan]CONTENT QUEUED[/]\n{content_queued}"))

        risk = self._risk
        sharpe = getattr(risk, "portfolio_sharpe", 0.0) if risk else 0.0
        var95 = getattr(risk, "var_95", 0.0) if risk else 0.0
        hhi = getattr(risk, "hhi_method", 0.0) if risk else 0.0
        total_methods = len(self._positions)

        self.query_one("#stat-sharpe", Static).update(Text.from_markup(f"[bold]SHARPE[/]\n{sharpe:.2f}"))
        self.query_one("#stat-var", Static).update(Text.from_markup(f"[bold]VaR 95%[/]\n{_fp(var95)}"))
        hhi_label = "Diversified" if hhi < 0.15 else "Moderate" if hhi < 0.25 else "Concentrated"
        self.query_one("#stat-hhi", Static).update(Text.from_markup(f"[bold]HHI[/]\n{hhi:.2f} ({hhi_label})"))
        self.query_one("#stat-methods", Static).update(Text.from_markup(f"[bold]TOTAL METHODS[/]\n{total_methods}"))

        # Content / outreach / ops / edge summary row
        content_ready = sum(1 for c in self._content_calendar if c.get("status", "").lower() == "pending")
        outreach_leads = len(self._outreach_pipeline)
        ops_active = sum(1 for o in self._daily_ops if (getattr(o, "status", "") or "").upper() == "ACTIVE")
        edge_alive = sum(1 for _, s, _, _ in self.EDGE_TACTICS_STATUS if s in ("ALIVE", "WORKING", "ESSENTIAL", "SAFE"))

        self.query_one("#stat-content-ready", Static).update(Text.from_markup(f"[bold green]CONTENT READY[/]\n{content_ready}"))
        self.query_one("#stat-outreach-leads", Static).update(Text.from_markup(f"[bold cyan]OUTREACH LEADS[/]\n{outreach_leads}"))
        self.query_one("#stat-ops-active", Static).update(Text.from_markup(f"[bold cyan]OPS ACTIVE[/]\n{ops_active}"))
        self.query_one("#stat-edge-alive", Static).update(Text.from_markup(f"[bold yellow]EDGE TACTICS[/]\n{edge_alive} alive"))

        # Priority actions
        actions_table = self.query_one("#overview-actions", DataTable)
        actions_table.clear(columns=True)
        actions_table.add_columns("#", "Priority", "Action", "Source")
        todos = self._generate_priority_actions()
        for i, (pri, action, source) in enumerate(todos, 1):
            actions_table.add_row(str(i), pri, action, source)

        # Pipeline funnel
        self._populate_pipeline_funnel()
        # Top opportunities
        self._populate_top_opportunities()
        # Revenue velocity
        self._populate_revenue_velocity()

        # Active investments
        inv_table = self.query_one("#investments-table", DataTable)
        inv_table.clear(columns=True)
        inv_table.add_columns("Priority", "ID", "Method", "Description", "Capital", "Status", "Next Action")
        sorted_inv = sorted(self._investments, key=lambda i: {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}.get(getattr(i, "priority", ""), 4))
        for inv in sorted_inv:
            pri = getattr(inv, "priority", "")
            pri_color = "!!" if pri == "CRITICAL" else ">>" if pri == "HIGH" else "--"
            inv_table.add_row(
                f"{pri_color} {pri}",
                str(getattr(inv, "inv_id", "")),
                str(getattr(inv, "method_id", "")),
                _trunc(str(getattr(inv, "description", "")), 35),
                _fc(getattr(inv, "capital_allocated", 0)),
                str(getattr(inv, "status", "")),
                _trunc(str(getattr(inv, "next_action", "")), 40),
            )
        if not self._investments:
            inv_table.add_row("--", "--", "No investments", "--", "$0", "--", "Check ACTIVE_INVESTMENTS.csv")

        # Top synergies
        syn_table = self.query_one("#synergies-table", DataTable)
        syn_table.clear(columns=True)
        syn_table.add_columns("Score", "Methods", "Synergy", "Multiplier")
        for s in self._synergies[:15]:
            syn_table.add_row(
                str(getattr(s, "score", 0)),
                _trunc(str(getattr(s, "method_combo", "")), 35),
                _trunc(str(getattr(s, "synergy_name", "")), 40),
                f"{getattr(s, 'multiplier', 1.0):.1f}x",
            )
        if not self._synergies:
            syn_table.add_row("--", "No synergies", "--", "--")

    def _generate_priority_actions(self):
        actions = []
        fin = self._financial
        total_rev = getattr(fin, "total_revenue", 0.0) if fin else 0.0

        if total_rev == 0:
            actions.append(("CRITICAL", "No revenue yet - ship first product", "FINANCIALS"))

        building = [p for p in self._positions if (getattr(p, "status", "") or "").lower() == "building"]
        for p in building[:3]:
            actions.append(("HIGH", f"Complete {p.method_id} ({p.name}) - still Building", "POSITIONS"))

        pending_alpha = sum(1 for a in self._alpha if (getattr(a, "status", "") or "").upper() == "PENDING_REVIEW")
        if pending_alpha > 0:
            actions.append(("MEDIUM", f"Review {pending_alpha} pending alpha entries", "ALPHA"))

        not_started = [o for o in self._daily_ops if (getattr(o, "status", "") or "").upper() == "NOT_STARTED"]
        if not_started:
            actions.append(("MEDIUM", f"{len(not_started)} daily ops never run", "OPS"))

        total_exp = getattr(fin, "total_expenses", 0.0) if fin else 0.0
        if total_exp > 0 and total_rev == 0:
            actions.append(("HIGH", f"${total_exp:,.0f} spent, $0 earned - prioritize shipping", "FINANCIALS"))

        content_total = getattr(self._content, "total_pieces", 0) if self._content else 0
        if content_total > 0:
            actions.append(("MEDIUM", f"{content_total} content pieces in pipeline", "CONTENT"))

        # Content calendar ready posts
        pending_posts = sum(1 for c in self._content_calendar if c.get("status", "").lower() == "pending")
        if pending_posts > 0:
            actions.append(("HIGH", f"{pending_posts} posts ready to publish - upload to Buffer", "CONTENT_CAL"))

        # Outreach pipeline qualified leads
        qualified_leads = [l for l in self._outreach_pipeline if l.get("status", "").lower() == "qualified"]
        if qualified_leads:
            value = sum(float(l.get("deal_value", 0) or 0) for l in qualified_leads)
            actions.append(("HIGH", f"{len(qualified_leads)} qualified leads ({_fc(value)} pipeline)", "OUTREACH"))

        # Health checklist incomplete
        health_done = sum(1 for h in self._health_checklist if h.get("today_status", "").upper() == "DONE")
        health_total = len(self._health_checklist)
        if health_total > 0 and health_done < health_total:
            actions.append(("LOW", f"Health: {health_done}/{health_total} habits done today", "HEALTH"))

        if not actions:
            actions.append(("INFO", "All systems nominal", "SYSTEM"))
        return actions

    def _populate_pipeline_funnel(self) -> None:
        funnel = compute_pipeline_funnel(self._positions)
        table = self.query_one("#overview-pipeline", DataTable)
        table.clear(columns=True)
        table.add_columns("Stage", "Count", "Conversion to Next")

        stage_order = ["Research", "Planning", "Building", "Active", "Paused", "Other"]
        conv_map = {
            "Research": funnel["conversions"].get("Research>Planning", 0.0),
            "Planning": funnel["conversions"].get("Planning>Building", 0.0),
            "Building": funnel["conversions"].get("Building>Active", 0.0),
        }

        for stage in stage_order:
            count = funnel["stages"].get(stage, 0)
            if count == 0 and stage in ("Paused", "Other"):
                continue
            conv = conv_map.get(stage)
            conv_str = f"{conv * 100:.1f}%" if conv is not None else ""
            table.add_row(stage, str(count), conv_str)
        table.add_row("TOTAL", str(funnel["total_methods"]), "")

    def _populate_top_opportunities(self) -> None:
        method_files_map = {}
        for p in self._positions:
            method_files_map[p.method_id] = _scan_method_files(p.method_id)

        opps = compute_top_opportunities(self._positions, self._alpha, method_files_map)

        table = self.query_one("#overview-opportunities", DataTable)
        table.clear(columns=True)
        table.add_columns("Rank", "Method", "Name", "Health", "Grade", "Potential/mo", "Opp Score")

        for i, opp in enumerate(opps[:15], 1):
            pot_str = f"${opp['potential']/1000:.0f}K" if opp["potential"] >= 1000 else f"${opp['potential']:.0f}"
            table.add_row(
                str(i), opp["method_id"], _trunc(opp["name"], 28),
                str(opp["health_score"]), opp["grade"], pot_str,
                str(opp["opportunity_score"]),
            )

    def _populate_revenue_velocity(self) -> None:
        vel = compute_revenue_velocity(self._financial, self._positions)

        self.query_one("#vel-daily-burn", Static).update(Text.from_markup(f"[bold red]DAILY BURN[/]\n{_fc(vel['daily_burn'])}"))
        self.query_one("#vel-monthly-burn", Static).update(Text.from_markup(f"[bold red]MONTHLY BURN[/]\n{_fc(vel['monthly_burn'])}"))
        roi_color = "green" if vel["roi_pct"] >= 0 else "red"
        self.query_one("#vel-roi", Static).update(Text.from_markup(f"[bold {roi_color}]ROI[/]\n{vel['roi_pct']:.1f}%"))
        self.query_one("#vel-rev-per-method", Static).update(Text.from_markup(f"[bold green]REV/METHOD[/]\n{_fc(vel['revenue_per_method'])}"))
        self.query_one("#vel-with-rev", Static).update(Text.from_markup(f"[bold green]W/ REVENUE[/]\n{vel['methods_with_revenue']}"))
        self.query_one("#vel-without-rev", Static).update(Text.from_markup(f"[bold yellow]W/O REVENUE[/]\n{vel['methods_without_revenue']}"))
        self.query_one("#vel-total-invested", Static).update(Text.from_markup(f"[bold]TOTAL INVESTED[/]\n{_fc(vel['total_invested'])}"))
        self.query_one("#vel-total-revenue", Static).update(Text.from_markup(f"[bold green]TOTAL REVENUE[/]\n{_fc(vel['total_revenue'])}"))

    # -------------------------------------------------------------------
    # TAB 2: VENTURES
    # -------------------------------------------------------------------

    def _populate_ventures(self) -> None:
        table = self.query_one("#ventures-table", DataTable)
        table.clear(columns=True)
        table.cursor_type = "row"
        table.add_columns("Category", "Methods", "Active", "Building", "Revenue", "Expenses", "Profit", "Avg Potential")

        positions_by_id = {p.method_id: p for p in self._positions}

        for cat_key in get_all_categories():
            display_name = CATEGORY_DISPLAY_NAMES.get(cat_key, cat_key)
            icon = CATEGORY_ICONS.get(cat_key, "")
            method_ids = get_methods_in_category(cat_key)

            cat_rev = 0.0
            cat_exp = 0.0
            cat_profit = 0.0
            active = 0
            building = 0
            pots_lo = []
            pots_hi = []

            for mid in method_ids:
                pos = positions_by_id.get(mid)
                if pos:
                    cat_rev += pos.revenue_total
                    cat_exp += pos.expenses_total
                    cat_profit += pos.profit
                    if (pos.status or "").lower() == "active":
                        active += 1
                    elif (pos.status or "").lower() == "building":
                        building += 1
                    if pos.monthly_potential_low > 0 or pos.monthly_potential_high > 0:
                        pots_lo.append(pos.monthly_potential_low)
                        pots_hi.append(pos.monthly_potential_high)

            avg_pot = ""
            if pots_hi:
                avg_pot = f"${sum(pots_lo)/len(pots_lo)/1000:.0f}K-${sum(pots_hi)/len(pots_hi)/1000:.0f}K"

            table.add_row(
                f"{icon} {display_name}", str(len(method_ids)), str(active),
                str(building), _fc(cat_rev), _fc(cat_exp), _fc(cat_profit),
                avg_pot, key=cat_key,
            )

        # Uncategorized
        all_categorized = set()
        for methods in METHOD_HIERARCHY.values():
            all_categorized.update(methods)
        uncategorized = [p for p in self._positions if p.method_id not in all_categorized]
        if uncategorized:
            table.add_row(
                "? Uncategorized", str(len(uncategorized)),
                str(sum(1 for p in uncategorized if (p.status or "").lower() == "active")),
                str(sum(1 for p in uncategorized if (p.status or "").lower() == "building")),
                _fc(sum(p.revenue_total for p in uncategorized)),
                _fc(sum(p.expenses_total for p in uncategorized)),
                _fc(sum(p.profit for p in uncategorized)),
                "", key="UNCATEGORIZED",
            )

    def _populate_ventures_sorted(self) -> None:
        """Re-populate ventures table with current sort applied."""
        table = self.query_one("#ventures-table", DataTable)
        table.clear(columns=True)
        table.cursor_type = "row"
        table.add_columns("Category", "Methods", "Active", "Building", "Revenue", "Expenses", "Profit", "Avg Potential")

        positions_by_id = {p.method_id: p for p in self._positions}
        rows = []

        for cat_key in get_all_categories():
            display_name = CATEGORY_DISPLAY_NAMES.get(cat_key, cat_key)
            icon = CATEGORY_ICONS.get(cat_key, "")
            method_ids = get_methods_in_category(cat_key)

            cat_rev = 0.0
            cat_exp = 0.0
            cat_profit = 0.0
            active = 0
            building = 0
            pots_lo = []
            pots_hi = []

            for mid in method_ids:
                pos = positions_by_id.get(mid)
                if pos:
                    cat_rev += pos.revenue_total
                    cat_exp += pos.expenses_total
                    cat_profit += pos.profit
                    if (pos.status or "").lower() == "active":
                        active += 1
                    elif (pos.status or "").lower() == "building":
                        building += 1
                    if pos.monthly_potential_low > 0 or pos.monthly_potential_high > 0:
                        pots_lo.append(pos.monthly_potential_low)
                        pots_hi.append(pos.monthly_potential_high)

            avg_pot_val = (sum(pots_hi) / len(pots_hi)) if pots_hi else 0.0
            avg_pot_str = f"${sum(pots_lo)/len(pots_lo)/1000:.0f}K-${sum(pots_hi)/len(pots_hi)/1000:.0f}K" if pots_hi else ""

            rows.append({
                "cat_key": cat_key, "display": f"{icon} {display_name}",
                "methods": len(method_ids), "active": active, "building": building,
                "revenue": cat_rev, "expenses": cat_exp, "profit": cat_profit,
                "potential": avg_pot_val, "potential_str": avg_pot_str,
            })

        sort_key = self._venture_sort_key
        if sort_key == "name":
            rows.sort(key=lambda r: r["display"].lower())
        elif sort_key == "revenue":
            rows.sort(key=lambda r: r["revenue"], reverse=True)
        elif sort_key == "profit":
            rows.sort(key=lambda r: r["profit"], reverse=True)
        elif sort_key == "potential":
            rows.sort(key=lambda r: r["potential"], reverse=True)

        for r in rows:
            table.add_row(
                r["display"], str(r["methods"]), str(r["active"]),
                str(r["building"]), _fc(r["revenue"]), _fc(r["expenses"]),
                _fc(r["profit"]), r["potential_str"], key=r["cat_key"],
            )

    @on(DataTable.RowSelected, "#ventures-table")
    def on_ventures_row_selected(self, event: DataTable.RowSelected) -> None:
        row_key = event.row_key
        if row_key and row_key.value:
            self.push_screen(CategoryScreen(row_key.value, self._positions, self._alpha))

    # -------------------------------------------------------------------
    # TAB 3: ALPHA
    # -------------------------------------------------------------------

    def _populate_alpha(self) -> None:
        total = len(self._alpha)
        pending = sum(1 for a in self._alpha if (getattr(a, "status", "") or "").upper() == "PENDING_REVIEW")
        approved = sum(1 for a in self._alpha if (getattr(a, "status", "") or "").upper() == "APPROVED")
        rejected = sum(1 for a in self._alpha if (getattr(a, "status", "") or "").upper() == "REJECTED")

        self.query_one("#alpha-total", Static).update(Text.from_markup(f"[bold]TOTAL[/]\n{total}"))
        self.query_one("#alpha-pending", Static).update(Text.from_markup(f"[bold yellow]PENDING[/]\n{pending}"))
        self.query_one("#alpha-approved", Static).update(Text.from_markup(f"[bold green]APPROVED[/]\n{approved}"))
        self.query_one("#alpha-rejected", Static).update(Text.from_markup(f"[bold red]REJECTED[/]\n{rejected}"))
        self._refresh_alpha_table()

    def _refresh_alpha_table(self) -> None:
        table = self.query_one("#alpha-table", DataTable)
        table.clear(columns=True)
        table.add_columns("ID", "Source", "Category", "Tactic", "ROI", "Status", "Days")

        filtered = self._alpha
        if self._alpha_filter == "PENDING":
            filtered = [a for a in self._alpha if (getattr(a, "status", "") or "").upper() == "PENDING_REVIEW"]
        elif self._alpha_filter == "APPROVED":
            filtered = [a for a in self._alpha if (getattr(a, "status", "") or "").upper() == "APPROVED"]
        elif self._alpha_filter == "REJECTED":
            filtered = [a for a in self._alpha if (getattr(a, "status", "") or "").upper() == "REJECTED"]

        for a in filtered[:200]:
            table.add_row(
                str(getattr(a, "alpha_id", "")),
                _trunc(str(getattr(a, "source", "")), 20),
                _trunc(str(getattr(a, "category", "")), 16),
                _trunc(str(getattr(a, "tactic", "")), 40),
                str(getattr(a, "roi_potential", "")),
                str(getattr(a, "status", "")),
                str(getattr(a, "days_since_discovery", "")),
            )

    @on(Button.Pressed, "#filter-all")
    def filter_all(self) -> None:
        self._alpha_filter = "ALL"
        self._update_filter_buttons()
        self._refresh_alpha_table()

    @on(Button.Pressed, "#filter-pending")
    def filter_pending(self) -> None:
        self._alpha_filter = "PENDING"
        self._update_filter_buttons()
        self._refresh_alpha_table()

    @on(Button.Pressed, "#filter-approved")
    def filter_approved(self) -> None:
        self._alpha_filter = "APPROVED"
        self._update_filter_buttons()
        self._refresh_alpha_table()

    @on(Button.Pressed, "#filter-rejected")
    def filter_rejected(self) -> None:
        self._alpha_filter = "REJECTED"
        self._update_filter_buttons()
        self._refresh_alpha_table()

    def _update_filter_buttons(self) -> None:
        btn_map = {
            "ALL": "#filter-all", "PENDING": "#filter-pending",
            "APPROVED": "#filter-approved", "REJECTED": "#filter-rejected",
        }
        for key, sel in btn_map.items():
            btn = self.query_one(sel, Button)
            btn.set_classes("filter-btn-active" if key == self._alpha_filter else "filter-btn")

    # -------------------------------------------------------------------
    # TAB 4: RESEARCH
    # -------------------------------------------------------------------

    def _populate_research(self) -> None:
        ops = self._daily_ops
        daily_ops = [o for o in ops if (getattr(o, "frequency", "") or "").lower() == "daily"]
        weekly_ops = [o for o in ops if (getattr(o, "frequency", "") or "").lower() == "weekly"]
        other_ops = [o for o in ops if (getattr(o, "frequency", "") or "").lower() not in ("daily", "weekly")]

        for table_id, op_list in [("ops-daily", daily_ops), ("ops-weekly", weekly_ops), ("ops-monthly", other_ops)]:
            table = self.query_one(f"#{table_id}", DataTable)
            table.clear(columns=True)
            table.cursor_type = "row"
            table.add_columns("Status", "ID", "Op Name", "Tool", "Last Run", "Duration")
            for o in op_list:
                status_str = getattr(o, "status", "")
                icon = "[+]" if status_str.upper() == "COMPLETED" else "[~]" if status_str.upper() == "ACTIVE" else "[ ]"
                ops_id = str(getattr(o, "ops_id", ""))
                table.add_row(
                    icon, ops_id, str(getattr(o, "ops_name", "")),
                    _trunc(str(getattr(o, "tool_required", "")), 20),
                    str(getattr(o, "last_run", "")),
                    f"{getattr(o, 'duration_min', 0)}m",
                    key=ops_id,
                )

        # Platform daily limits reference table
        pl_table = self.query_one("#platform-limits", DataTable)
        pl_table.clear(columns=True)
        pl_table.add_columns("Platform", "Action", "New Account", "Warmed", "Aggressive", "Risk")
        for row in self.PLATFORM_LIMITS:
            pl_table.add_row(*row)

        # Edge tactics status table
        et_table = self.query_one("#edge-tactics", DataTable)
        et_table.clear(columns=True)
        et_table.add_columns("Tactic", "Status", "Risk", "Notes")
        for tactic, status, risk, notes in self.EDGE_TACTICS_STATUS:
            et_table.add_row(tactic, status, risk, notes)

        # Signal sources
        src_table = self.query_one("#signal-sources", DataTable)
        src_table.clear(columns=True)
        src_table.add_columns("Source", "Platform", "Category", "Quality")
        for s in self._signal_sources[:20]:
            src_table.add_row(
                _trunc(str(getattr(s, "source_name", "")), 25),
                str(getattr(s, "platform", "")),
                _trunc(str(getattr(s, "category", "")), 16),
                str(getattr(s, "signal_quality", "")),
            )

        # Research suggestions
        suggestions = self.query_one("#research-suggestions", Static)
        not_run_ops = [o for o in ops if (getattr(o, "status", "") or "").upper() == "NOT_STARTED"]
        if not_run_ops:
            lines = [f"  -> {getattr(o, 'ops_name', '')} ({getattr(o, 'frequency', '')})" for o in not_run_ops[:5]]
            suggestions.update(Text.from_markup("[yellow]These ops have never been run:[/]\n" + "\n".join(lines)))
        else:
            suggestions.update(Text.from_markup("[green]All ops have been run at least once.[/]"))

    # -------------------------------------------------------------------
    # TAB 5: SOCIAL
    # -------------------------------------------------------------------

    def _populate_social(self) -> None:
        table = self.query_one("#social-table", DataTable)
        table.clear(columns=True)
        table.add_columns("Niche", "Platform", "Handle", "Email", "Status", "Created", "Notes")

        accounts = sorted(self._social, key=lambda a: (getattr(a, "niche", "") or "", getattr(a, "platform", "") or ""))
        for a in accounts:
            table.add_row(
                str(getattr(a, "niche", "")), str(getattr(a, "platform", "")),
                str(getattr(a, "handle", "")), _trunc(str(getattr(a, "email", "")), 25),
                str(getattr(a, "status", "")), str(getattr(a, "created_date", "")),
                _trunc(str(getattr(a, "notes", "")), 30),
            )
        if not accounts:
            table.add_row("--", "--", "No accounts found", "", "", "", "")

        # Account health monitor
        ah_table = self.query_one("#account-health-table", DataTable)
        ah_table.clear(columns=True)
        ah_table.add_columns("Date", "Platform", "Account", "Status", "Restrictions", "Reputation", "Reach %", "Shadowban", "Actions")
        for h in self._account_health:
            status = h.get("status_ok", "PENDING")
            ah_table.add_row(
                h.get("date", ""),
                h.get("platform", ""),
                h.get("account", ""),
                status,
                h.get("restrictions", "NONE"),
                h.get("reputation_score", "0"),
                h.get("reach_vs_baseline_pct", "0") + "%",
                h.get("shadowban_check", "NOT_CHECKED"),
                _trunc(h.get("action_items", ""), 30),
            )
        if not self._account_health:
            ah_table.add_row("--", "--", "No health data", "--", "--", "--", "--", "--", "Edit ACCOUNT_HEALTH_DAILY.csv")

        # Content pipeline stats
        cal = self._content_calendar
        total_posts = len(cal)
        pending_posts = sum(1 for c in cal if c.get("status", "").lower() == "pending")
        published_posts = sum(1 for c in cal if c.get("status", "").lower() in ("published", "posted"))
        niches = set(c.get("niche", "") for c in cal if c.get("niche", ""))

        self.query_one("#content-total-posts", Static).update(
            Text.from_markup(f"[bold cyan]TOTAL POSTS[/]\n{total_posts}")
        )
        self.query_one("#content-pending", Static).update(
            Text.from_markup(f"[bold yellow]PENDING[/]\n{pending_posts}")
        )
        self.query_one("#content-published", Static).update(
            Text.from_markup(f"[bold green]PUBLISHED[/]\n{published_posts}")
        )
        self.query_one("#content-niches", Static).update(
            Text.from_markup(f"[bold cyan]NICHES[/]\n{len(niches)}")
        )

        # Outreach pipeline
        leads = self._outreach_pipeline
        total_leads = len(leads)
        active_leads = sum(1 for l in leads if l.get("status", "").lower() in ("qualified", "discovery", "nurture"))
        qualified = sum(1 for l in leads if l.get("status", "").lower() == "qualified")
        pipeline_value = 0.0
        for l in leads:
            try:
                pipeline_value += float(l.get("deal_value", 0) or 0)
            except (ValueError, TypeError):
                pass

        self.query_one("#outreach-total", Static).update(
            Text.from_markup(f"[bold cyan]TOTAL LEADS[/]\n{total_leads}")
        )
        self.query_one("#outreach-active", Static).update(
            Text.from_markup(f"[bold green]ACTIVE[/]\n{active_leads}")
        )
        self.query_one("#outreach-pipeline-value", Static).update(
            Text.from_markup(f"[bold yellow]PIPELINE VALUE[/]\n{_fc(pipeline_value)}")
        )
        self.query_one("#outreach-qualified", Static).update(
            Text.from_markup(f"[bold green]QUALIFIED[/]\n{qualified}")
        )

        or_table = self.query_one("#outreach-table", DataTable)
        or_table.clear(columns=True)
        or_table.add_columns("ID", "Company", "Contact", "Offer", "Status", "Deal $", "Last Response", "Notes")
        for l in leads:
            or_table.add_row(
                l.get("prospect_id", ""),
                _trunc(l.get("company", ""), 18),
                _trunc(l.get("contact_name", ""), 18),
                _trunc(l.get("offer_type", ""), 22),
                l.get("status", ""),
                _fc(float(l.get("deal_value", 0) or 0)),
                l.get("last_response", "") or "-",
                _trunc(l.get("notes", ""), 35),
            )
        if not leads:
            or_table.add_row("--", "No leads", "--", "--", "--", "$0", "--", "Edit OUTREACH_PIPELINE.csv")

        # Growth tactics table
        gt_table = self.query_one("#growth-tactics-table", DataTable)
        gt_table.clear(columns=True)
        gt_table.add_columns("Platform", "Tactic", "Safety", "Limits", "Details", "Status")
        for t in self._growth_tactics:
            safety = getattr(t, "safety", "")
            gt_table.add_row(
                str(getattr(t, "platform", "")),
                _trunc(str(getattr(t, "tactic", "")), 40),
                str(safety),
                str(getattr(t, "limits", "")),
                _trunc(str(getattr(t, "details", "")), 50),
                str(getattr(t, "status", "")),
            )
        if not self._growth_tactics:
            gt_table.add_row("--", "No growth tactics loaded", "--", "--", "--", "--")

        # Growth services table
        gs_table = self.query_one("#growth-services-table", DataTable)
        gs_table.clear(columns=True)
        gs_table.add_columns("Platform", "Service", "Price", "Description", "Safety", "Expected Results")
        for s in self._growth_services:
            gs_table.add_row(
                str(getattr(s, "platform", "")),
                str(getattr(s, "name", "")),
                str(getattr(s, "price", "")),
                _trunc(str(getattr(s, "description", "")), 35),
                str(getattr(s, "safety_rating", "")),
                _trunc(str(getattr(s, "expected_results", "")), 35),
            )
        if not self._growth_services:
            gs_table.add_row("--", "No services loaded", "--", "--", "--", "--")

    # -------------------------------------------------------------------
    # TAB 6: FINANCIAL (Upgraded with ROI, efficiency, timeline)
    # -------------------------------------------------------------------

    def _populate_financial(self) -> None:
        fin = self._financial

        # P&L stat boxes
        total_rev = getattr(fin, "total_revenue", 0.0) if fin else 0.0
        total_exp = getattr(fin, "total_expenses", 0.0) if fin else 0.0
        net_profit = getattr(fin, "net_profit", 0.0) if fin else 0.0
        burn_rate = getattr(fin, "burn_rate_monthly", 0.0) if fin else 0.0

        self.query_one("#fin-revenue", Static).update(Text.from_markup(f"[bold green]REVENUE[/]\n{_fc(total_rev)}"))
        self.query_one("#fin-expenses", Static).update(Text.from_markup(f"[bold red]EXPENSES[/]\n{_fc(total_exp)}"))
        pnl_color = "green" if net_profit >= 0 else "red"
        self.query_one("#fin-net", Static).update(Text.from_markup(f"[bold {pnl_color}]NET P&L[/]\n{_fc(net_profit)}"))
        self.query_one("#fin-burn", Static).update(Text.from_markup(f"[bold yellow]BURN RATE/MO[/]\n{_fc(burn_rate)}"))

        # P&L table
        pnl_table = self.query_one("#financial-pnl", DataTable)
        pnl_table.clear(columns=True)
        pnl_table.add_columns("Metric", "Total", "MTD")
        if fin:
            pnl_table.add_row("Revenue", _fc(fin.total_revenue), _fc(fin.mtd_revenue))
            pnl_table.add_row("Expenses", _fc(fin.total_expenses), _fc(fin.mtd_expenses))
            pnl_table.add_row("Net P&L", _fc(fin.net_profit), _fc(fin.mtd_revenue - fin.mtd_expenses))

        # Expense ROI by method
        roi_table = self.query_one("#expense-roi-method", DataTable)
        roi_table.clear(columns=True)
        roi_table.add_columns("Method ID", "Name", "Expenses", "Revenue", "ROI %", "Status")

        methods_with_expenses = sorted(
            [p for p in self._positions if p.expenses_total > 0],
            key=lambda p: p.expenses_total, reverse=True
        )

        for p in methods_with_expenses:
            roi_pct = ((p.revenue_total - p.expenses_total) / p.expenses_total) * 100.0 if p.expenses_total > 0 else 0.0
            if p.revenue_total > p.expenses_total:
                roi_status = "PROFITABLE"
            elif p.revenue_total > 0:
                roi_status = "PARTIAL"
            else:
                roi_status = "NO REVENUE"
            roi_table.add_row(p.method_id, _trunc(p.name, 25), _fc(p.expenses_total), _fc(p.revenue_total), _fp(roi_pct), roi_status)

        if not methods_with_expenses:
            roi_table.add_row("--", "No methods with expenses", "$0", "$0", "0.0%", "--")

        # Cost efficiency metrics
        methods_with_exp_count = len(methods_with_expenses)
        active_exp_count = sum(1 for p in methods_with_expenses if (p.status or "").lower() == "active")

        cost_per_method = total_exp / methods_with_exp_count if methods_with_exp_count > 0 else 0.0
        cost_per_active = total_exp / active_exp_count if active_exp_count > 0 else 0.0
        cash_efficiency = total_rev / total_exp if total_exp > 0 else 0.0

        expenses = self._expense_breakdown
        total_exp_breakdown = sum(float(v) for v in expenses.values()) if expenses else 0
        sorted_exp = sorted(expenses.items(), key=lambda x: float(x[1]), reverse=True) if expenses else []
        if sorted_exp and total_exp_breakdown > 0:
            top_cat_name, top_cat_amt = sorted_exp[0]
            expense_concentration = (float(top_cat_amt) / total_exp_breakdown) * 100.0
            concentration_label = f"{_fp(expense_concentration)}\n({top_cat_name})"
        else:
            concentration_label = "N/A"

        self.query_one("#fin-cost-per-method", Static).update(Text.from_markup(f"[bold]COST/METHOD[/]\n{_fc(cost_per_method)}"))
        self.query_one("#fin-cost-per-active", Static).update(Text.from_markup(f"[bold]COST/ACTIVE[/]\n{_fc(cost_per_active)}"))
        eff_color = "green" if cash_efficiency >= 1.0 else "red"
        self.query_one("#fin-cash-efficiency", Static).update(Text.from_markup(f"[bold {eff_color}]CASH EFFICIENCY[/]\n{cash_efficiency:.2f}x"))
        self.query_one("#fin-expense-concentration", Static).update(Text.from_markup(f"[bold yellow]TOP CATEGORY[/]\n{concentration_label}"))

        # Expense timeline from CSV
        timeline_table = self.query_one("#expense-timeline", DataTable)
        timeline_table.clear(columns=True)
        timeline_table.add_columns("Date", "Category", "Item", "Amount", "Method", "Recurring", "Notes")

        expense_csv_path = PROJECT_ROOT / "FINANCIALS" / "EXPENSE_TRACKER.csv"
        expense_rows = []
        if expense_csv_path.exists():
            with open(expense_csv_path, newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    expense_rows.append(row)

        expense_rows.sort(key=lambda r: r.get("date", ""), reverse=True)

        for row in expense_rows[:20]:
            amt_val = 0.0
            cleaned = (row.get("amount", "$0") or "0").strip().replace("$", "").replace(",", "")
            try:
                amt_val = float(cleaned)
            except ValueError:
                pass
            recurring = (row.get("recurring", "") or "").strip().upper()
            recurring_display = "Yes" if recurring in ("TRUE", "YES", "1") else "No"
            timeline_table.add_row(
                row.get("date", ""), _trunc(row.get("category", ""), 18),
                _trunc(row.get("item", ""), 30), _fc(amt_val),
                row.get("method_id", ""), recurring_display,
                _trunc(row.get("notes", ""), 30),
            )

        if not expense_rows:
            timeline_table.add_row("--", "--", "No expenses recorded", "$0", "--", "--", "--")

        # Tool costs
        tool_costs = getattr(fin, "tool_costs_monthly", 0.0) if fin else 0.0
        active_subs = getattr(fin, "active_subscriptions", 0) if fin else 0
        runway = getattr(fin, "runway_months", 0.0) if fin else 0.0

        self.query_one("#fin-tool-costs", Static).update(Text.from_markup(f"[bold]TOOL COSTS/MO[/]\n{_fc(tool_costs)}"))
        self.query_one("#fin-active-subs", Static).update(Text.from_markup(f"[bold]ACTIVE SUBS[/]\n{active_subs}"))
        self.query_one("#fin-burn-rate", Static).update(Text.from_markup(f"[bold yellow]BURN RATE/MO[/]\n{_fc(burn_rate)}"))
        runway_str = f"{runway:.1f} mo" if runway < float("inf") else "INF"
        self.query_one("#fin-runway", Static).update(Text.from_markup(f"[bold]RUNWAY[/]\n{runway_str}"))

        # Expense breakdown
        exp_table = self.query_one("#expense-breakdown", DataTable)
        exp_table.clear(columns=True)
        exp_table.add_columns("Category", "Amount", "% of Total")
        for cat, amt in sorted_exp:
            pct = (float(amt) / total_exp_breakdown * 100) if total_exp_breakdown > 0 else 0
            exp_table.add_row(str(cat), _fc(float(amt)), _fp(pct))
        if sorted_exp:
            exp_table.add_row("TOTAL", _fc(total_exp_breakdown), "100.0%")

    # -------------------------------------------------------------------
    # TAB 7: RISK
    # -------------------------------------------------------------------

    def _populate_risk(self) -> None:
        table = self.query_one("#risk-table", DataTable)
        table.clear(columns=True)
        table.add_columns("Metric", "Value", "Status")

        risk = self._risk
        if not risk:
            table.add_row("No risk data", "N/A", "Insufficient data")
            return

        sharpe = risk.portfolio_sharpe
        sortino = risk.portfolio_sortino
        data_months = risk.sharpe_data_months

        if data_months > 0:
            sharpe_status = f"Based on {data_months}mo data"
            if data_months >= 12:
                sharpe_status = "OK" if sharpe > 0 else "Negative"
        else:
            sharpe_status = "Insufficient data"
        table.add_row("Sharpe Ratio", f"{sharpe:.2f}", sharpe_status)

        sortino_status = ("OK" if sortino > 0 else "Negative") if data_months > 0 else "Insufficient data"
        table.add_row("Sortino Ratio", f"{sortino:.2f}", sortino_status)

        ci = risk.sharpe_ci
        if ci and (ci[0] != 0 or ci[1] != 0):
            table.add_row("Sharpe 95% CI", f"[{ci[0]:.2f}, {ci[1]:.2f}]", "")

        table.add_row("VaR (95%)", _fp(risk.var_95), "Parametric")
        table.add_row("VaR (99%)", _fp(risk.var_99), "Parametric")
        if risk.var_95_historical > 0:
            table.add_row("VaR (95%) Hist", _fp(risk.var_95_historical), "Historical")
        if risk.var_99_historical > 0:
            table.add_row("VaR (99%) Hist", _fp(risk.var_99_historical), "Historical")

        table.add_row("CVaR (95%)", _fp(risk.cvar_95), "Expected Shortfall")
        table.add_row("CVaR (99%)", _fp(risk.cvar_99), "Expected Shortfall")

        dd_status = "Below threshold" if risk.max_drawdown < 20 else "Warning" if risk.max_drawdown < 40 else "Critical"
        table.add_row("Max Drawdown", _fp(risk.max_drawdown), dd_status)
        if risk.current_drawdown > 0:
            table.add_row("Current Drawdown", _fp(risk.current_drawdown), f"{risk.drawdown_duration} periods")

        for label, hhi_val in [("HHI (Method)", risk.hhi_method), ("HHI (Platform)", risk.hhi_platform), ("HHI (Niche)", risk.hhi_niche)]:
            hhi_status = "Diversified" if hhi_val < 0.15 else "Moderate" if hhi_val < 0.25 else "Concentrated"
            table.add_row(label, f"{hhi_val:.4f}", hhi_status)

        max_method, max_method_pct = risk.concentration_max_method
        if max_method:
            table.add_row("Max Method Conc.", f"{max_method}: {max_method_pct:.1f}%", "")
        max_plat, max_plat_pct = risk.concentration_max_platform
        if max_plat:
            table.add_row("Max Platform Conc.", f"{max_plat}: {max_plat_pct:.1f}%", "")

        table.add_row("Beta", f"{risk.beta:.2f}", risk.beta_confidence)

        if risk.ic_sample_size > 0:
            table.add_row("Information Coeff.", f"{risk.ic:.3f}", f"Hit rate: {risk.ic_hit_rate:.1f}% (n={risk.ic_sample_size})")
        else:
            table.add_row("Information Coeff.", "N/A", "No deployed alpha")

    # -------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------

    def action_refresh(self) -> None:
        self._load_data()
        self._populate_all()
        self._update_tab_badges()
        self.notify("Data refreshed", severity="information")

    def action_sort_ventures(self) -> None:
        try:
            idx = VENTURE_SORT_CYCLE.index(self._venture_sort_key)
        except ValueError:
            idx = -1
        self._venture_sort_key = VENTURE_SORT_CYCLE[(idx + 1) % len(VENTURE_SORT_CYCLE)]
        self._populate_ventures_sorted()
        self.notify(f"Ventures sorted by: {self._venture_sort_key}", severity="information")

    def action_tab_1(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-overview"

    def action_tab_2(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-ventures"

    def action_tab_3(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-alpha"

    def action_tab_4(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-research"

    def action_tab_5(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-social"

    def action_tab_6(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-financial"

    def action_tab_7(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-risk"

    def action_tab_8(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-health"

    def action_tab_9(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-gtm"

    def action_tab_0(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-infra"

    def action_tab_auto(self) -> None:
        self.query_one("#tabs", TabbedContent).active = "tab-automations"

    # -------------------------------------------------------------------
    # Interactive Ops Checklist (toggle status on row click, write to CSV)
    # -------------------------------------------------------------------

    def _toggle_ops_status(self, ops_id: str) -> None:
        """Toggle ops status: NOT_STARTED -> ACTIVE -> COMPLETED -> NOT_STARTED and write to CSV."""
        csv_path = PROJECT_ROOT / "LEDGER" / "DAILY_OPS_TRACKER.csv"
        if not csv_path.exists():
            return
        rows = []
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row.get("ops_id", "") == ops_id:
                    status = row.get("status", "NOT_STARTED").upper()
                    if status == "NOT_STARTED":
                        row["status"] = "ACTIVE"
                        row["last_run"] = date.today().isoformat()
                    elif status == "ACTIVE":
                        row["status"] = "COMPLETED"
                        row["last_run"] = date.today().isoformat()
                    else:
                        row["status"] = "NOT_STARTED"
                rows.append(row)
        if fieldnames:
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        # Reload and refresh
        self._daily_ops = load_daily_ops()
        self._populate_research()
        self.notify(f"Toggled {ops_id}", severity="information")

    @on(DataTable.RowSelected, "#ops-daily")
    def on_ops_daily_selected(self, event: DataTable.RowSelected) -> None:
        if event.row_key and event.row_key.value:
            self._toggle_ops_status(event.row_key.value)

    @on(DataTable.RowSelected, "#ops-weekly")
    def on_ops_weekly_selected(self, event: DataTable.RowSelected) -> None:
        if event.row_key and event.row_key.value:
            self._toggle_ops_status(event.row_key.value)

    @on(DataTable.RowSelected, "#ops-monthly")
    def on_ops_monthly_selected(self, event: DataTable.RowSelected) -> None:
        if event.row_key and event.row_key.value:
            self._toggle_ops_status(event.row_key.value)

    # -------------------------------------------------------------------
    # Interactive Health Checklist (toggle done/pending on row click)
    # -------------------------------------------------------------------

    @on(DataTable.RowSelected, "#health-daily-checklist")
    def on_health_checklist_selected(self, event: DataTable.RowSelected) -> None:
        if not (event.row_key and event.row_key.value):
            return
        habit_id = event.row_key.value
        csv_path = PROJECT_ROOT / "LEDGER" / "HEALTH_DAILY_CHECKLIST.csv"
        if not csv_path.exists():
            return
        rows = []
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row.get("habit_id", "") == habit_id:
                    if row.get("today_status", "PENDING").upper() == "DONE":
                        row["today_status"] = "PENDING"
                        try:
                            streak = int(row.get("streak", 0) or 0)
                            row["streak"] = str(max(0, streak - 1))
                        except (ValueError, TypeError):
                            pass
                    else:
                        row["today_status"] = "DONE"
                        try:
                            streak = int(row.get("streak", 0) or 0)
                            row["streak"] = str(streak + 1)
                        except (ValueError, TypeError):
                            row["streak"] = "1"
                rows.append(row)
        if fieldnames:
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        # Reload checklist and refresh health tab
        health_cl_csv = PROJECT_ROOT / "LEDGER" / "HEALTH_DAILY_CHECKLIST.csv"
        self._health_checklist = []
        if health_cl_csv.exists():
            try:
                with open(health_cl_csv, newline="", encoding="utf-8") as f:
                    self._health_checklist = list(csv.DictReader(f))
            except Exception:
                pass
        self._populate_health()
        self.notify(f"Toggled {habit_id}", severity="information")

    # -------------------------------------------------------------------
    # Automation Launcher (run scripts from terminal)
    # -------------------------------------------------------------------

    @on(Button.Pressed, "#run-alpha-scan")
    def run_alpha_scan(self) -> None:
        script = AUTOMATIONS_DIR / "alpha_screening.py"
        if script.exists():
            subprocess.Popen([sys.executable, str(script), "--pending"],
                             cwd=str(PROJECT_ROOT), start_new_session=True)
            self.notify("Alpha scan launched", severity="information")
        else:
            self.notify("alpha_screening.py not found", severity="warning")

    @on(Button.Pressed, "#run-reddit-scrape")
    def run_reddit_scrape(self) -> None:
        script = AUTOMATIONS_DIR / "background_reddit_scraper.py"
        if script.exists():
            subprocess.Popen([sys.executable, str(script), "--scrape"],
                             cwd=str(PROJECT_ROOT), start_new_session=True)
            self.notify("Reddit scrape launched", severity="information")
        else:
            self.notify("background_reddit_scraper.py not found", severity="warning")

    @on(Button.Pressed, "#run-github-trending")
    def run_github_trending(self) -> None:
        script = AUTOMATIONS_DIR / "niche_meta_detector.py"
        if script.exists():
            subprocess.Popen([sys.executable, str(script)],
                             cwd=str(PROJECT_ROOT), start_new_session=True)
            self.notify("GitHub trending scan launched", severity="information")
        else:
            self.notify("niche_meta_detector.py not found", severity="warning")

    @on(Button.Pressed, "#run-refresh-all")
    def run_refresh_all(self) -> None:
        self._load_data()
        self._populate_all()
        self._update_tab_badges()
        self.notify("Full data refresh complete", severity="information")

    # -------------------------------------------------------------------
    # TAB 8: HEALTH LAB
    # -------------------------------------------------------------------

    def _populate_health(self) -> None:
        data = self._health_data

        active_supps = [r for r in data if r.get("category") == "Supplement" and r.get("status", "").upper() == "ACTIVE"]
        queued = [r for r in data if r.get("status", "").upper() == "QUEUED"]
        protocols = [r for r in data if r.get("category") == "Protocol"]
        biomarkers = [r for r in data if r.get("category") == "Biomarker"]
        diet = [r for r in data if r.get("category") == "Diet"]
        fermented = [r for r in data if r.get("category") == "Fermented" and r.get("status", "").upper() == "ACTIVE"]
        active_all = [r for r in data if r.get("status", "").upper() == "ACTIVE"]

        total_cost = 0.0
        for r in active_all:
            try:
                total_cost += float(r.get("cost_monthly", 0) or 0)
            except (ValueError, TypeError):
                pass

        # Stat boxes
        self.query_one("#health-active", Static).update(
            Text.from_markup(f"[bold green]ACTIVE ITEMS[/]\n{len(active_all)}")
        )
        self.query_one("#health-cost", Static).update(
            Text.from_markup(f"[bold yellow]MONTHLY COST[/]\n{_fc(total_cost)}")
        )
        self.query_one("#health-protocols", Static).update(
            Text.from_markup(f"[bold cyan]PROTOCOLS[/]\n{len(protocols)}")
        )
        self.query_one("#health-biomarkers", Static).update(
            Text.from_markup(f"[bold cyan]BIOMARKERS[/]\n{len(biomarkers)}")
        )

        # Supplements table (active + fermented)
        supp_table = self.query_one("#health-supplements", DataTable)
        supp_table.clear(columns=True)
        supp_table.add_columns("ID", "Name", "Dose", "Freq", "Time", "$/mo", "Rating", "Notes")
        for r in active_supps + fermented:
            rating = r.get("subjective_rating", "")
            rating_str = f"{rating}/10" if rating else "-"
            cost = r.get("cost_monthly", "0")
            try:
                cost_str = _fc(float(cost)) if float(cost) > 0 else "Free"
            except (ValueError, TypeError):
                cost_str = "-"
            supp_table.add_row(
                r.get("item_id", ""),
                _trunc(r.get("item_name", ""), 30),
                r.get("dose", ""),
                r.get("frequency", ""),
                r.get("time_of_day", ""),
                cost_str,
                rating_str,
                _trunc(r.get("notes", ""), 50),
            )

        # Protocols table
        proto_table = self.query_one("#health-protocols-table", DataTable)
        proto_table.clear(columns=True)
        proto_table.add_columns("ID", "Protocol", "Dose/Duration", "Frequency", "Time", "Status", "Notes")
        for r in protocols:
            proto_table.add_row(
                r.get("item_id", ""),
                r.get("item_name", ""),
                r.get("dose", ""),
                r.get("frequency", ""),
                r.get("time_of_day", ""),
                r.get("status", ""),
                _trunc(r.get("notes", ""), 60),
            )

        # Biomarkers table
        bio_table = self.query_one("#health-biomarkers-table", DataTable)
        bio_table.clear(columns=True)
        bio_table.add_columns("ID", "Biomarker", "Frequency", "Time", "Target / Notes")
        for r in biomarkers:
            bio_table.add_row(
                r.get("item_id", ""),
                r.get("item_name", ""),
                r.get("frequency", ""),
                r.get("time_of_day", ""),
                _trunc(r.get("notes", ""), 60),
            )

        # Diet table
        diet_table = self.query_one("#health-diet-table", DataTable)
        diet_table.clear(columns=True)
        diet_table.add_columns("ID", "Framework", "Target", "Frequency", "Notes")
        for r in diet:
            diet_table.add_row(
                r.get("item_id", ""),
                r.get("item_name", ""),
                r.get("dose", ""),
                r.get("frequency", ""),
                _trunc(r.get("notes", ""), 60),
            )

        # Queued items
        q_table = self.query_one("#health-queued", DataTable)
        q_table.clear(columns=True)
        q_table.add_columns("ID", "Category", "Item", "Dose", "Frequency", "Notes")
        for r in queued:
            q_table.add_row(
                r.get("item_id", ""),
                r.get("category", ""),
                r.get("item_name", ""),
                r.get("dose", ""),
                r.get("frequency", ""),
                _trunc(r.get("notes", ""), 60),
            )

        # Daily health checklist
        cl = self._health_checklist
        done_count = sum(1 for h in cl if h.get("today_status", "").upper() == "DONE")
        pending_count = sum(1 for h in cl if h.get("today_status", "").upper() != "DONE")
        max_streak = 0
        for h in cl:
            try:
                s = int(h.get("streak", 0) or 0)
                if s > max_streak:
                    max_streak = s
            except (ValueError, TypeError):
                pass
        completion_pct = (done_count / len(cl) * 100) if cl else 0

        self.query_one("#health-done-count", Static).update(
            Text.from_markup(f"[bold green]DONE TODAY[/]\n{done_count}/{len(cl)}")
        )
        self.query_one("#health-pending-count", Static).update(
            Text.from_markup(f"[bold yellow]REMAINING[/]\n{pending_count}")
        )
        self.query_one("#health-streak-max", Static).update(
            Text.from_markup(f"[bold cyan]BEST STREAK[/]\n{max_streak} days")
        )
        comp_color = "green" if completion_pct >= 80 else "yellow" if completion_pct >= 50 else "red"
        self.query_one("#health-completion-pct", Static).update(
            Text.from_markup(f"[bold {comp_color}]COMPLETION[/]\n{completion_pct:.0f}%")
        )

        cl_table = self.query_one("#health-daily-checklist", DataTable)
        cl_table.clear(columns=True)
        cl_table.cursor_type = "row"
        cl_table.add_columns("Status", "Habit", "Category", "Target", "Time", "Streak", "Notes")
        for h in cl:
            status = h.get("today_status", "PENDING").upper()
            icon = "[+]" if status == "DONE" else "[ ]"
            cl_table.add_row(
                icon,
                h.get("habit_name", ""),
                h.get("category", ""),
                h.get("target", ""),
                h.get("time_of_day", ""),
                h.get("streak", "0") + "d",
                _trunc(h.get("notes", ""), 40),
                key=h.get("habit_id", ""),
            )

    # -------------------------------------------------------------------
    # TAB 9: GTM SYNERGIES
    # -------------------------------------------------------------------

    GTM_VENTURE_STACKS = {
        "APPS_SOFTWARE": {
            "channels": ["Twitter/X Organic", "Product Hunt", "Reddit", "ASO", "Cold Email", "YouTube Shorts"],
            "cost_low": 0, "cost_high": 200,
            "priority": "HIGH",
            "notes": "ASO-first for apps. Product Hunt launch for SaaS. Reddit for dev communities.",
        },
        "CONTENT_MEDIA": {
            "channels": ["Twitter/X Organic", "TikTok Organic", "YouTube Organic", "Pinterest", "Instagram Reels"],
            "cost_low": 0, "cost_high": 100,
            "priority": "HIGHEST",
            "notes": "Zero-cost content distribution. Cross-post everywhere. Clip army model.",
        },
        "AI_PERSONAS": {
            "channels": ["Twitter/X Organic", "Fanvue/Fansly", "Reddit", "Telegram", "TikTok Organic"],
            "cost_low": 50, "cost_high": 300,
            "priority": "HIGH",
            "notes": "Platform arbitrage. Anti-detect browser + proxies. Warmed accounts critical.",
        },
        "ECOMMERCE": {
            "channels": ["TikTok Shop", "Pinterest Affiliate", "SEO/Blog", "Amazon KDP", "Etsy Ads", "Facebook Ads"],
            "cost_low": 100, "cost_high": 500,
            "priority": "HIGH",
            "notes": "Paid ads for ecom. TikTok Shop nano-influencers 20-25% commission.",
        },
        "OUTBOUND_SERVICES": {
            "channels": ["Cold Email", "LinkedIn", "Cold DM", "Upwork/Fiverr", "Local SEO"],
            "cost_low": 50, "cost_high": 400,
            "priority": "HIGHEST",
            "notes": "Email warmup + SOAX proxies. DeliverOn/EmailBison for inbox warming.",
        },
        "FINANCIAL_TRADING": {
            "channels": ["Twitter/X Organic", "Discord", "Telegram", "Newsletter"],
            "cost_low": 0, "cost_high": 50,
            "priority": "LOW",
            "notes": "Signal channels for community. Memecoin = Twitter alpha only.",
        },
        "GROWTH_HACKING": {
            "channels": ["Twitter/X Organic", "Reddit", "Indie Hackers", "Medium", "Substack"],
            "cost_low": 0, "cost_high": 100,
            "priority": "MEDIUM",
            "notes": "Build-in-public content. Cross-post blog to Medium + Substack.",
        },
        "INFO_PRODUCTS": {
            "channels": ["Twitter/X Organic", "Gumroad", "Newsletter", "YouTube", "TikTok Organic"],
            "cost_low": 0, "cost_high": 150,
            "priority": "HIGH",
            "notes": "Gumroad for digital products. Newsletter funnel. Free content -> paid upsell.",
        },
    }

    def _populate_gtm(self) -> None:
        channels = self._gtm_channels
        active_ch = [c for c in channels if (c.get("status", "").upper() == "ACTIVE")]
        categories = list(self.GTM_VENTURE_STACKS.keys())

        total_cost_low = sum(v["cost_low"] for v in self.GTM_VENTURE_STACKS.values())
        total_cost_high = sum(v["cost_high"] for v in self.GTM_VENTURE_STACKS.values())

        self.query_one("#gtm-total-channels", Static).update(
            Text.from_markup(f"[bold cyan]TOTAL CHANNELS[/]\n{len(channels)}")
        )
        self.query_one("#gtm-active-channels", Static).update(
            Text.from_markup(f"[bold green]ACTIVE[/]\n{len(active_ch)}")
        )
        self.query_one("#gtm-est-cost", Static).update(
            Text.from_markup(f"[bold yellow]EST. MONTHLY GTM[/]\n${total_cost_low}-${total_cost_high}")
        )
        self.query_one("#gtm-categories", Static).update(
            Text.from_markup(f"[bold cyan]VENTURE CATS[/]\n{len(categories)}")
        )

        # Venture GTM map
        v_table = self.query_one("#gtm-venture-map", DataTable)
        v_table.clear(columns=True)
        v_table.add_columns("Category", "GTM Channels", "Est. $/mo", "Priority", "Notes")
        for cat, info in self.GTM_VENTURE_STACKS.items():
            ch_str = ", ".join(info["channels"][:4])
            if len(info["channels"]) > 4:
                ch_str += f" +{len(info['channels']) - 4}"
            cost_str = f"${info['cost_low']}-${info['cost_high']}"
            v_table.add_row(
                cat.replace("_", " ").title(),
                ch_str,
                cost_str,
                info["priority"],
                _trunc(info["notes"], 55),
            )

        # Channel directory from CSV
        ch_table = self.query_one("#gtm-channel-dir", DataTable)
        ch_table.clear(columns=True)
        ch_table.add_columns("ID", "Channel", "Platform", "Type", "ROI", "Priority", "Status")
        for c in channels:
            ch_table.add_row(
                c.get("channel_id", ""),
                _trunc(c.get("channel_name", ""), 25),
                c.get("platform", ""),
                c.get("channel_type", ""),
                c.get("roi_potential", ""),
                c.get("priority", ""),
                c.get("status", ""),
            )


    # -------------------------------------------------------------------
    # TAB 10: INFRA
    # -------------------------------------------------------------------

    # Platform daily action limits (platform, action, new_account, warmed, aggressive, risk_level)
    PLATFORM_LIMITS = [
        ("Instagram", "Follows/day", "10-20", "30-50", "80-100", "HIGH"),
        ("Instagram", "Likes/day", "50-80", "100-150", "300+", "MEDIUM"),
        ("Instagram", "DMs/day", "5-10", "10-20", "50+", "HIGH"),
        ("Instagram", "Comments/day", "20-30", "50-80", "150+", "MEDIUM"),
        ("Instagram", "Stories/day", "5-8", "10-15", "20+", "LOW"),
        ("TikTok", "Follows/day", "30-50", "100-200", "300+", "MEDIUM"),
        ("TikTok", "Likes/day", "100-200", "300-500", "1000+", "LOW"),
        ("TikTok", "Comments/day", "20-50", "50-100", "200+", "MEDIUM"),
        ("TikTok", "Posts/day", "1-3", "3-5", "5+", "LOW"),
        ("X/Twitter", "Follows/day", "50-100", "200-400", "500+", "MEDIUM"),
        ("X/Twitter", "Likes/day", "100-300", "500-1000", "2000+", "LOW"),
        ("X/Twitter", "DMs/day", "20-30", "50-100", "200+", "MEDIUM"),
        ("X/Twitter", "Posts/day", "3-5", "10-20", "30+", "LOW"),
        ("LinkedIn", "Connections/day", "10-20", "20-30", "50+", "HIGH"),
        ("LinkedIn", "Messages/day", "10-20", "25-50", "100+", "HIGH"),
        ("LinkedIn", "Posts/day", "1", "1-2", "3+", "MEDIUM"),
        ("Email", "Sends/day (new)", "5-10", "25-30", "50+", "HIGH"),
        ("Email", "Sends/day (warmed)", "30-50", "75-100", "200+", "MEDIUM"),
        ("YouTube", "Videos/week", "1-2", "3-5", "7+", "LOW"),
        ("YouTube", "Comments/day", "10-20", "30-50", "100+", "LOW"),
    ]

    # Edge / grey-hat tactics status (tactic, status, risk, notes)
    EDGE_TACTICS_STATUS = [
        ("Engagement pods", "DYING", "HIGH", "Detected by Meta AI. Max 5-7 members same niche"),
        ("Follow/unfollow auto", "DEAD", "CRITICAL", "Meta AI nullified. Don't waste time"),
        ("Bot farms/followers", "DEAD", "CRITICAL", "Detected instantly. Kills brand deals"),
        ("Paid growth (IG)", "ALIVE", "MED-HIGH", "Verify real followers. Audit engagement"),
        ("Paid growth (TikTok)", "ALIVE", "MEDIUM", "Cost varies. Evaluate ROI carefully"),
        ("Account warming", "ESSENTIAL", "LOW", "2-4 weeks before any automation"),
        ("Email warmup", "ESSENTIAL", "LOW", "TrulyInbox = free forever. Non-negotiable"),
        ("Multi-account ops", "ALIVE", "MEDIUM", "Manual safer than automation"),
        ("Aged account buys", "RISKY", "HIGH", "ToS violation. Detection improving"),
        ("Cross-platform repost", "SAFE", "LOW", "Native content preferred but works"),
        ("Reels-first (IG)", "WORKING", "LOW", "3-5/week + trending audio + 3s hooks"),
        ("Carousel posts (IG)", "WORKING", "LOW", "12% more interactions than Reels"),
        ("Trial Reels (IG)", "WORKING", "LOW", "Built-in A/B test with non-followers"),
        ("1-2 hashtags only", "WORKING", "LOW", "Beats 20+ hashtags. Following dying"),
        ("TikTok 60-180s video", "WORKING", "LOW", "1 quality/day > 5 low quality"),
    ]

    # Per-venture recommended tool categories (maps venture -> tool categories needed)
    VENTURE_TOOL_MAP = {
        "APPS_SOFTWARE": ["hosting", "analytics", "content", "monetization"],
        "CONTENT_MEDIA": ["social", "content", "newsletter", "analytics"],
        "AI_PERSONAS": ["anti_detect", "proxies", "content", "social", "accounts"],
        "ECOMMERCE": ["funnels", "analytics", "email", "social"],
        "OUTBOUND_SERVICES": ["email", "crm", "linkedin", "leads"],
        "FINANCIAL_TRADING": ["analytics", "automation", "hosting"],
        "GROWTH_DISTRIBUTION": ["social", "newsletter", "funnels", "content"],
        "INFO_EDUCATION": ["funnels", "newsletter", "content", "monetization"],
    }

    def _populate_infra(self) -> None:
        tools = self._infra_tools
        ab_tests = self._ab_tests

        # Counts
        total = len(tools)
        active = [t for t in tools if t.get("status", "").upper() == "ACTIVE"]
        free = [t for t in tools if t.get("free_tier", "").upper() == "YES"]
        categories = set(t.get("category", "") for t in tools)
        ab_running = [t for t in ab_tests if t.get("status", "").upper() == "RUNNING"]

        # Estimate monthly cost of active tools (parse paid_from for active non-free)
        monthly_cost = 0.0
        for t in active:
            if t.get("free_tier", "").upper() == "YES":
                continue
            paid = t.get("paid_from", "")
            try:
                monthly_cost += float(paid.replace("$", "").replace("/mo", "").replace("/user/mo", "").split("/")[0])
            except (ValueError, TypeError):
                pass

        # Current budget tier
        if monthly_cost == 0:
            tier_label = "$0 (Zero)"
        elif monthly_cost <= 50:
            tier_label = "$50 (Micro)"
        elif monthly_cost <= 150:
            tier_label = "$150 (Bootstrap)"
        else:
            tier_label = f"${monthly_cost:.0f} (Growth)"

        # Upgrades: HIGHEST priority tools that are AVAILABLE (not active)
        upgrades = [t for t in tools if t.get("status", "").upper() == "AVAILABLE"
                     and t.get("priority", "").upper() in ("HIGHEST", "HIGH")]

        # Stat boxes
        self.query_one("#infra-total", Static).update(
            Text.from_markup(f"[bold cyan]TOTAL TOOLS[/]\n{total}")
        )
        self.query_one("#infra-active", Static).update(
            Text.from_markup(f"[bold green]ACTIVE[/]\n{len(active)}")
        )
        self.query_one("#infra-free", Static).update(
            Text.from_markup(f"[bold green]FREE TIER[/]\n{len(free)}")
        )
        self.query_one("#infra-monthly-cost", Static).update(
            Text.from_markup(f"[bold yellow]MONTHLY COST[/]\n{_fc(monthly_cost)}")
        )
        self.query_one("#infra-ab-running", Static).update(
            Text.from_markup(f"[bold cyan]A/B TESTS[/]\n{len(ab_running)} running")
        )
        self.query_one("#infra-categories", Static).update(
            Text.from_markup(f"[bold cyan]CATEGORIES[/]\n{len(categories)}")
        )
        self.query_one("#infra-upgrades-count", Static).update(
            Text.from_markup(f"[bold yellow]UPGRADES[/]\n{len(upgrades)} available")
        )
        self.query_one("#infra-budget-tier", Static).update(
            Text.from_markup(f"[bold green]BUDGET TIER[/]\n{tier_label}")
        )

        # --- ACTIVE STACK TABLE ---
        act_table = self.query_one("#infra-active-stack", DataTable)
        act_table.clear(columns=True)
        act_table.add_columns("ID", "Tool", "Category", "Free Tier", "Paid", "Priority", "Notes")
        for t in active:
            free_detail = t.get("free_tier_detail", "") if t.get("free_tier", "").upper() == "YES" else "Paid"
            act_table.add_row(
                t.get("tool_id", ""),
                _trunc(t.get("tool_name", ""), 22),
                t.get("category", ""),
                _trunc(free_detail, 28),
                t.get("paid_from", ""),
                t.get("priority", ""),
                _trunc(t.get("notes", ""), 45),
            )
        if not active:
            act_table.add_row("--", "No active tools", "--", "--", "--", "--", "Edit TOOLS_SERVICES_MASTER.csv")

        # --- RECOMMENDED UPGRADES TABLE ---
        up_table = self.query_one("#infra-upgrades-table", DataTable)
        up_table.clear(columns=True)
        up_table.add_columns("ID", "Tool", "Category", "Free Tier", "Paid From", "Budget Tier", "Notes")
        for t in upgrades[:15]:
            up_table.add_row(
                t.get("tool_id", ""),
                _trunc(t.get("tool_name", ""), 22),
                t.get("category", ""),
                _trunc(t.get("free_tier_detail", ""), 28),
                t.get("paid_from", ""),
                t.get("budget_tier", ""),
                _trunc(t.get("notes", ""), 45),
            )

        # --- BUDGET TIERS TABLE (computed from CSV) ---
        bt_table = self.query_one("#infra-budget-tiers", DataTable)
        bt_table.clear(columns=True)
        bt_table.add_columns("Tier", "Monthly Cost", "Tools Available", "Key Additions")
        tier_levels = [("$0", 0), ("$50", 50), ("$150", 150), ("$500", 500)]
        for tier_name, threshold in tier_levels:
            tier_tools = [t for t in tools if _parse_budget(t.get("budget_tier", "$0")) <= threshold]
            additions = [t.get("tool_name", "") for t in tools
                         if _parse_budget(t.get("budget_tier", "$0")) == threshold and threshold > 0]
            add_str = ", ".join(additions[:4])
            if len(additions) > 4:
                add_str += f" +{len(additions) - 4}"
            if threshold == 0:
                add_str = "Full free-tier stack"
            bt_table.add_row(tier_name + "/mo", f"${threshold}", str(len(tier_tools)), add_str)

        # --- A/B TESTS TABLE ---
        ab_table = self.query_one("#infra-ab-tests", DataTable)
        ab_table.clear(columns=True)
        ab_table.add_columns("ID", "Category", "Stack A", "Stack B", "Metric", "Status", "Winner", "Notes")
        for t in ab_tests:
            status = t.get("status", "")
            winner = t.get("winner", "") or "-"
            ab_table.add_row(
                t.get("test_id", ""),
                t.get("category", ""),
                _trunc(t.get("stack_a", ""), 25),
                _trunc(t.get("stack_b", ""), 25),
                t.get("metric", ""),
                status,
                winner,
                _trunc(t.get("notes", ""), 45),
            )
        if not ab_tests:
            ab_table.add_row("--", "--", "--", "--", "--", "--", "--", "Edit STACK_AB_TESTS.csv")

        # --- PER-VENTURE STACKS TABLE ---
        vs_table = self.query_one("#infra-venture-stacks", DataTable)
        vs_table.clear(columns=True)
        vs_table.add_columns("Venture", "Recommended Tools", "$0 Tier", "$150 Tier")
        for venture, needed_cats in self.VENTURE_TOOL_MAP.items():
            zero_tools = [t.get("tool_name", "") for t in tools
                          if t.get("category", "") in needed_cats
                          and t.get("free_tier", "").upper() == "YES"
                          and t.get("priority", "").upper() in ("HIGHEST", "HIGH")]
            paid_tools = [t.get("tool_name", "") for t in tools
                          if t.get("category", "") in needed_cats
                          and _parse_budget(t.get("budget_tier", "$0")) <= 150
                          and t.get("priority", "").upper() in ("HIGHEST", "HIGH")]
            zero_str = ", ".join(zero_tools[:4]) or "None"
            if len(zero_tools) > 4:
                zero_str += f" +{len(zero_tools) - 4}"
            paid_str = ", ".join(paid_tools[:4]) or "None"
            if len(paid_tools) > 4:
                paid_str += f" +{len(paid_tools) - 4}"
            vs_table.add_row(
                venture.replace("_", " ").title(),
                str(len(needed_cats)) + " categories",
                _trunc(zero_str, 40),
                _trunc(paid_str, 40),
            )

        # --- FULL TOOL DIRECTORY ---
        all_table = self.query_one("#infra-all-tools", DataTable)
        all_table.clear(columns=True)
        all_table.add_columns("ID", "Tool", "Category", "Free?", "Free Detail", "Paid", "Status", "Priority", "Tier")
        for t in tools:
            all_table.add_row(
                t.get("tool_id", ""),
                _trunc(t.get("tool_name", ""), 20),
                t.get("category", ""),
                t.get("free_tier", ""),
                _trunc(t.get("free_tier_detail", ""), 28),
                t.get("paid_from", ""),
                t.get("status", ""),
                t.get("priority", ""),
                t.get("budget_tier", ""),
            )


    # -------------------------------------------------------------------
    # TAB 11: AUTOMATIONS COMMAND CENTER
    # -------------------------------------------------------------------

    def _run_automation(self, cmd: str, label: str, use_watchdog: bool = True) -> None:
        """Launch an automation command through the safety watchdog."""
        watchdog = AUTOMATIONS_DIR / "safety_watchdog.sh"
        cron = PROJECT_ROOT / "printmaxx_cron.sh"

        if use_watchdog and watchdog.exists() and cron.exists():
            full_cmd = ["bash", str(watchdog), f"./printmaxx_cron.sh {cmd}"]
        elif cron.exists():
            full_cmd = ["bash", str(cron), cmd]
        else:
            self.notify(f"printmaxx_cron.sh not found", severity="error")
            return

        try:
            subprocess.Popen(
                full_cmd,
                cwd=str(PROJECT_ROOT),
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            self.notify(f"{label} launched via watchdog", severity="information")
        except Exception as e:
            self.notify(f"Failed to launch {label}: {e}", severity="error")

    def _populate_automations(self) -> None:
        """Populate the automations tab with real yield data from AUTOMATION_RESULTS.csv."""
        import csv as _csv
        from datetime import datetime as _dt

        results_csv = PROJECT_ROOT / "LEDGER" / "AUTOMATION_RESULTS.csv"
        log_dir = PROJECT_ROOT / "logs"
        today = _dt.now().strftime("%Y-%m-%d")

        # Load all results
        results = []
        if results_csv.exists():
            try:
                with open(results_csv) as f:
                    results = list(_csv.DictReader(f))
            except Exception:
                pass

        # Today's results
        today_results = [r for r in results if today in r.get("timestamp", "")]
        total_runs = len(results)
        today_runs = len(today_results)

        # Aggregate today's yield
        today_alpha = sum(int(r.get("alpha_extracted", 0) or 0) for r in today_results)
        today_content = sum(int(r.get("content_generated", 0) or 0) for r in today_results)
        today_errors = sum(int(r.get("errors", 0) or 0) for r in today_results)
        today_buffer = sum(int(r.get("buffer_csvs", 0) or 0) for r in today_results)

        # Get latest revenue projection
        rev_30d = "$0"
        rev_annual = "$0"
        for r in reversed(results):
            rv = r.get("revenue_projected_30d", "")
            if rv and rv != "$0" and rv != "0":
                rev_30d = rv
                rev_annual = r.get("revenue_projected_annual", "$0")
                break

        # Stat boxes with real yield data
        self.query_one("#auto-total-runs", Static).update(
            f"Today's Runs\n{today_runs} ({total_runs} total)"
        )
        self.query_one("#auto-last-run", Static).update(
            f"Today's Alpha\n{today_alpha} extracted"
        )
        self.query_one("#auto-next-run", Static).update(
            f"Today's Content\n{today_content} pieces / {today_buffer} CSVs"
        )

        # Watchdog + Opus audit status
        halts_log = log_dir / "watchdog_halts.log"
        has_halts = halts_log.exists() and halts_log.stat().st_size > 0
        latest_verdict = ""
        if results:
            latest_verdict = results[-1].get("watchdog_verdict", "")
        if has_halts:
            self.query_one("#auto-watchdog-status", Static).update(
                f"Opus Audit\nHALT DETECTED"
            )
        elif latest_verdict:
            self.query_one("#auto-watchdog-status", Static).update(
                f"Opus Audit\n{latest_verdict[:20]}"
            )
        else:
            self.query_one("#auto-watchdog-status", Static).update(
                f"Opus Audit\nAWAITING FIRST RUN"
            )

        # Schedule display with revenue
        schedule_text = (
            f"Revenue Projection: 30d={rev_30d}  Annual={rev_annual}\n"
            f"\n"
            f"06:00  Morning Sync     - Alpha extract, organize, repair, revenue check\n"
            f"06:30  Content Gen      - 30-day calendar, Buffer CSVs, content queue\n"
            f"09:00  Outreach Queue   - QA routing, email sequences, pipeline check\n"
            f"18:00  Evening Digest   - Daily yield summary, log review\n"
            f"21:00  Nightly Backup   - Git commit, CSV snapshot, push to remote\n"
            f"22:00  Overnight Sprint - Launch 8 Ralph loops (parallel Claude agents)\n"
            f"MON    Weekly Tasks     - Backtest merge, calendar, QA, validation\n"
            f"1st    Monthly Tasks    - Revenue projection, method analysis, git bundle\n"
            f"\n"
            f"Claude Opus auto-audits every run with errors or anomalies."
        )
        self.query_one("#auto-schedule-display", Static).update(schedule_text)

        # Recent results - show actual yield per run
        if results:
            recent_text = ""
            for r in results[-8:]:
                ts = r.get("timestamp", "?")[:19]
                cmd = r.get("command", "?")
                dur = r.get("duration_secs", "?")
                alpha = r.get("alpha_extracted", "0")
                content = r.get("content_generated", "0")
                errs = r.get("errors", "0")
                verdict = r.get("watchdog_verdict", "")[:15]
                notes = r.get("notes", "")[:40]
                err_mark = " [!]" if int(errs or 0) > 0 else ""
                recent_text += f"{ts} | {cmd:10} | {dur:4}s | a:{alpha:>3} c:{content:>4} e:{errs}{err_mark} | {verdict or notes}\n"
            self.query_one("#auto-log-display", Static).update(recent_text.strip())
        else:
            self.query_one("#auto-log-display", Static).update(
                "No automation results yet.\n"
                "Click a button above to run an automation.\n"
                "Results will appear here with yield metrics."
            )

        # Thresholds + Opus audit info
        thresholds_text = (
            "SAFETY THRESHOLDS:\n"
            "  MAX_CSV_ROW_CHANGE: 200 rows  - Halt if any CSV gains/loses >200 rows\n"
            "  MAX_LEDGER_DELETED: 5 files    - Halt if >5 LEDGER files vanish\n"
            "  MIN_DISK_FREE:      5 GB       - Halt if disk space drops below 5GB\n"
            "  MAX_EXECUTION:      3600s      - Timeout for any single automation\n"
            "\n"
            "CLAUDE OPUS AUTO-AUDIT:\n"
            "  Model:   claude-opus-4-6 (latest Opus)\n"
            "  Trigger: Automatically on errors, exit code != 0, or CSV anomalies\n"
            "  Force:   --llm-check flag forces audit on every run\n"
            "  Output:  logs/watchdog_audit_*.txt + verdict in AUTOMATION_RESULTS.csv\n"
            f"  Status:  {'HALTS DETECTED - check logs/watchdog_halts.log' if has_halts else 'Clean - no halts'}"
        )
        self.query_one("#auto-thresholds", Static).update(thresholds_text)

    # --- Automation button handlers ---

    @on(Button.Pressed, "#auto-morning")
    def auto_morning(self) -> None:
        self._run_automation("morning", "Morning Sync")

    @on(Button.Pressed, "#auto-content")
    def auto_content(self) -> None:
        self._run_automation("content", "Content Gen")

    @on(Button.Pressed, "#auto-outreach")
    def auto_outreach(self) -> None:
        self._run_automation("outreach", "Outreach Pipeline")

    @on(Button.Pressed, "#auto-digest")
    def auto_digest(self) -> None:
        self._run_automation("digest", "Evening Digest")

    @on(Button.Pressed, "#auto-backup")
    def auto_backup(self) -> None:
        self._run_automation("backup", "Nightly Backup")

    @on(Button.Pressed, "#auto-overnight")
    def auto_overnight(self) -> None:
        self._run_automation("overnight", "Overnight Sprint")

    @on(Button.Pressed, "#auto-status")
    def auto_status_check(self) -> None:
        self._run_automation("status", "Status Check")

    @on(Button.Pressed, "#auto-refresh-data")
    def auto_refresh_data(self) -> None:
        self._load_data()
        self._populate_all()
        self._update_tab_badges()
        self.notify("Full data refresh complete", severity="information")

    @on(Button.Pressed, "#auto-weekly")
    def auto_weekly(self) -> None:
        self._run_automation("weekly", "Weekly Tasks")

    @on(Button.Pressed, "#auto-monthly")
    def auto_monthly(self) -> None:
        self._run_automation("monthly", "Monthly Tasks")

    @on(Button.Pressed, "#auto-validate")
    def auto_validate(self) -> None:
        """Run full CSV validation through watchdog."""
        script = AUTOMATIONS_DIR / "validate_all_csvs.sh"
        if script.exists():
            subprocess.Popen(
                ["bash", str(script)],
                cwd=str(PROJECT_ROOT),
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            self.notify("Full validation launched", severity="information")
        else:
            self._run_automation("status", "Validation (via status)")

    @on(Button.Pressed, "#auto-run-all-quick")
    def auto_run_all_quick(self) -> None:
        """Run morning + content + digest in sequence."""
        for cmd, label in [("morning", "Morning"), ("content", "Content"), ("digest", "Digest")]:
            self._run_automation(cmd, label)
        self.notify("All quick automations queued", severity="warning")

    @on(Button.Pressed, "#auto-alpha-scan")
    def auto_alpha_scan_btn(self) -> None:
        script = AUTOMATIONS_DIR / "alpha_screening.py"
        if script.exists():
            subprocess.Popen([sys.executable, str(script), "--pending"],
                             cwd=str(PROJECT_ROOT), start_new_session=True)
            self.notify("Alpha scan launched", severity="information")
        else:
            self.notify("alpha_screening.py not found", severity="warning")

    @on(Button.Pressed, "#auto-reddit")
    def auto_reddit_btn(self) -> None:
        script = AUTOMATIONS_DIR / "background_reddit_scraper.py"
        if script.exists():
            subprocess.Popen([sys.executable, str(script), "--scrape"],
                             cwd=str(PROJECT_ROOT), start_new_session=True)
            self.notify("Reddit scrape launched", severity="information")
        else:
            self.notify("background_reddit_scraper.py not found", severity="warning")

    @on(Button.Pressed, "#auto-github")
    def auto_github_btn(self) -> None:
        script = AUTOMATIONS_DIR / "niche_meta_detector.py"
        if script.exists():
            subprocess.Popen([sys.executable, str(script)],
                             cwd=str(PROJECT_ROOT), start_new_session=True)
            self.notify("GitHub trending scan launched", severity="information")
        else:
            self.notify("niche_meta_detector.py not found", severity="warning")

    @on(Button.Pressed, "#auto-competitor")
    def auto_competitor_btn(self) -> None:
        script = AUTOMATIONS_DIR / "competitor_monitor.py"
        if not script.exists():
            script = AUTOMATIONS_DIR / "niche_meta_detector.py"
        if script.exists():
            subprocess.Popen([sys.executable, str(script)],
                             cwd=str(PROJECT_ROOT), start_new_session=True)
            self.notify("Competitor intel launched", severity="information")
        else:
            self.notify("No competitor monitoring script found", severity="warning")


if __name__ == "__main__":
    app = PrintmaxxTUI()
    app.run()
