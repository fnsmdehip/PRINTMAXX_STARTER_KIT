#!/usr/bin/env python3
"""
PRINTMAXX QUANT TERMINAL v4.0 - INSTITUTIONAL ACTION CENTER
=============================================================
Bloomberg-inspired 7-panel TUI with full risk infrastructure.

Inspired by:
- Jane Street: Incremental computation, OCaml-style precision
- Two Sigma: Data-as-code, versioned pipelines
- Renaissance Technologies: Single unified model, speed of iteration
- Bloomberg Terminal: Multi-panel real-time visualization

v4.0: Added RBI Scanner Dashboard, Zero-Cost Ops tracking,
      Revenue Pipeline projections (30/60/90 day),
      Social Setup loop integration, Master Ops audit integration,
      Account portfolio dashboard (49 accounts).
v3.0: Restored risk infra (Sharpe/Sortino/VaR/CVaR/HHI/Beta/IC),
      comprehensive tool/GTM maps for all 89 methods,
      ACTIVE_INVESTMENTS + CROSS_POLLINATION integration,
      edge growth services with pricing, interactive controls.

Built with Textual (34K stars) + Rich (55K stars)
"""

from __future__ import annotations
import asyncio
import csv
import json
import os
import sys
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import math
import re

# Third-party imports
try:
    from textual.app import App, ComposeResult
    from textual.binding import Binding
    from textual.containers import Container, Horizontal, Vertical, ScrollableContainer, Grid
    from textual.widgets import (
        DataTable, Footer, Header, Static, Label,
        TabbedContent, TabPane, ProgressBar,
        RichLog, Tree, Button, Input, ListView, ListItem
    )
    from textual.reactive import reactive
    from textual.timer import Timer
    from textual.message import Message
    from rich.text import Text
    from rich.panel import Panel
    from rich.table import Table
    from rich.console import Console
    from rich.style import Style
    from rich.markup import escape
    HAS_TEXTUAL = True
except ImportError:
    HAS_TEXTUAL = False
    from rich.text import Text
    from rich.panel import Panel
    from rich.table import Table
    from rich.console import Console
    from rich.style import Style
    from rich.markup import escape

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ROOT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
OPS_DIR = PROJECT_ROOT / "OPS"
FINANCIALS_DIR = PROJECT_ROOT / "FINANCIALS"
AUTOMATIONS_DIR = PROJECT_ROOT / "AUTOMATIONS"
GROWTH_DIR = PROJECT_ROOT / "06_OPERATIONS" / "growth"
MONEY_METHODS_DIR = PROJECT_ROOT / "MONEY_METHODS"
RBI_AUDITS_DIR = LEDGER_DIR / "RBI_AUDITS"
SOCIAL_SETUP_OUTPUT = PROJECT_ROOT / "ralph" / "loops" / "social_setup" / "output"
MASTER_OPS_OUTPUT = PROJECT_ROOT / "ralph" / "loops" / "master_ops_build" / "output"
MASTER_OPS_XLSX = PROJECT_ROOT / "PRINTMAXX_MASTER_OPS.xlsx"
ACCOUNTS_CSV = LEDGER_DIR / "ACCOUNTS.csv"

# Risk thresholds (Jane Street / Two Sigma style)
RISK_THRESHOLDS = {
    "sharpe_min": 1.5,
    "sharpe_good": 2.0,
    "max_drawdown": 0.15,
    "concentration_max": 0.40,
    "platform_max": 0.50,
    "alpha_decay_warn": 30,
    "alpha_decay_crit": 90,
}

# Color scheme (Bloomberg-inspired dark theme)
COLORS = {
    "bg": "#0a0a0a",
    "panel_bg": "#1a1a1a",
    "border": "#333333",
    "text": "#ffffff",
    "text_dim": "#888888",
    "green": "#00ff00",
    "red": "#ff4444",
    "yellow": "#ffff00",
    "blue": "#4488ff",
    "orange": "#ff8844",
    "purple": "#aa88ff",
    "cyan": "#00ffff",
}

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class PortfolioRisk:
    """Institutional-grade portfolio risk metrics (restored from v1)"""
    total_revenue: float = 0.0
    total_expenses: float = 0.0
    net_profit: float = 0.0
    portfolio_sharpe: float = 0.0
    portfolio_sortino: float = 0.0
    sharpe_confidence_interval: Tuple[float, float] = (0.0, 0.0)
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
    concentration_hhi: float = 0.0
    concentration_method_max: float = 0.0
    concentration_platform_hhi: float = 0.0
    concentration_platform_max: float = 0.0
    concentration_niche_hhi: float = 0.0
    beta: float = 0.0
    beta_confidence: str = "INSUFFICIENT_DATA"
    information_coefficient: float = 0.0
    ic_hit_rate: float = 0.0
    ic_sample_size: int = 0
    active_method_count: int = 0
    total_method_count: int = 0
    capital_deployed: float = 0.0
    capital_at_risk: float = 0.0


@dataclass
class MethodPerformance:
    """Performance metrics for a money method"""
    method_id: str
    method_name: str
    status: str
    category: str = ""
    revenue_model: str = ""
    priority: str = ""
    notes: str = ""
    revenue_total: float = 0.0
    revenue_mtd: float = 0.0
    hours_invested: float = 0.0
    tools_used: List[str] = field(default_factory=list)
    gtm_channels: List[str] = field(default_factory=list)
    launch_strategy: str = ""


@dataclass
class AlphaEntry:
    """Alpha signal entry"""
    alpha_id: str
    source: str
    category: str
    tactic: str
    roi_potential: str
    status: str
    backtest_score: int = 0
    days_since_discovery: int = 0
    alpha_decay_pct: float = 0.0


@dataclass
class Investment:
    """Active investment from ACTIVE_INVESTMENTS.csv"""
    investment_id: str
    method_id: str
    name: str
    category: str
    status: str
    capital_allocated: float
    time_invested_hrs: float
    revenue_to_date: float
    next_action: str
    priority: str
    notes: str


@dataclass
class Synergy:
    """Cross-pollination synergy pair"""
    synergy_id: str
    method_1: str
    method_2: str
    synergy_score: int
    synergy_type: str
    revenue_multiplier: float
    implementation_notes: str
    priority: str


@dataclass
class GrowthService:
    """Growth service with pricing"""
    platform: str
    service_name: str
    cost: str
    method: str
    safety: str
    notes: str


@dataclass
class GrowthTactic:
    """Platform growth tactic with limits"""
    platform: str
    tactic_name: str
    risk_level: str  # SAFE, GREY, DEAD
    daily_limit: str
    notes: str
    status: str  # WORKING, PATCHED, DEGRADED


@dataclass
class RecommendedAction:
    """Intelligent recommendation"""
    priority: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str  # REVENUE, RISK, ALPHA, EXECUTION, INVESTMENT
    action: str
    reason: str
    command: Optional[str] = None


@dataclass
class RBIScanResult:
    """Result from the RBI daily/weekly/monthly scanner"""
    scan_date: str = ""
    total_alpha: int = 0
    pending_alpha: int = 0
    high_roi_pending: int = 0
    active_methods: int = 0
    total_methods: int = 0
    content_total: int = 0
    content_queued: int = 0
    top_categories: Dict[str, int] = field(default_factory=dict)
    roi_distribution: Dict[str, int] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    underallocated_methods: List[Dict[str, str]] = field(default_factory=list)
    top_synergy_pairs: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class ZeroCostOp:
    """A zero-cost operation category from the audit"""
    category: str
    description: str
    status: str  # active, ready, not_started
    opportunity_count: int = 0
    revenue_potential_low: float = 0.0
    revenue_potential_high: float = 0.0
    gaps_found: int = 0


@dataclass
class AccountStatus:
    """Account from ACCOUNTS.csv"""
    niche: str
    platform: str
    handle: str
    status: str
    notes: str = ""


# =============================================================================
# RISK CALCULATIONS (Restored - Institutional Grade)
# =============================================================================

def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.05) -> float:
    """Sharpe ratio: (mean excess return) / std deviation. Annualized."""
    if len(returns) < 2:
        return 0.0
    excess_returns = [r - risk_free_rate / 12 for r in returns]
    mean_excess = sum(excess_returns) / len(excess_returns)
    variance = sum((r - mean_excess) ** 2 for r in excess_returns) / (len(excess_returns) - 1)
    std_dev = math.sqrt(variance) if variance > 0 else 0.001
    return (mean_excess / std_dev) * math.sqrt(12)


def calculate_sortino_ratio(returns: List[float], risk_free_rate: float = 0.05) -> float:
    """Sortino ratio: uses downside deviation only (penalizes losses, not gains)."""
    if len(returns) < 2:
        return 0.0
    excess_returns = [r - risk_free_rate / 12 for r in returns]
    mean_excess = sum(excess_returns) / len(excess_returns)
    downside = [min(0, r) for r in excess_returns]
    downside_var = sum(d ** 2 for d in downside) / len(downside) if downside else 0.001
    downside_dev = math.sqrt(downside_var) if downside_var > 0 else 0.001
    return (mean_excess / downside_dev) * math.sqrt(12)


def calculate_sharpe_confidence_interval(returns: List[float], sharpe: float) -> Tuple[float, float]:
    """Lo (2002) confidence interval for Sharpe ratio.
    SE = sqrt((1 + SR^2/2) / n) for IID returns."""
    n = len(returns)
    if n < 3:
        return (0.0, 0.0)
    se = math.sqrt((1 + sharpe ** 2 / 2) / n)
    z = 1.96  # 95% CI
    return (round(sharpe - z * se, 3), round(sharpe + z * se, 3))


def calculate_max_drawdown(revenues: List[float]) -> Tuple[float, float, int]:
    """Max drawdown from revenue series.
    Returns: (max_drawdown_pct, current_drawdown_pct, duration_periods)"""
    if len(revenues) < 2:
        return (0.0, 0.0, 0)
    cumulative = []
    running = 0.0
    for r in revenues:
        running += r
        cumulative.append(running)
    peak = cumulative[0]
    max_dd = 0.0
    current_dd = 0.0
    dd_start = 0
    max_duration = 0
    current_duration = 0
    for i, val in enumerate(cumulative):
        if val > peak:
            peak = val
            current_duration = 0
        dd = (peak - val) / peak if peak > 0 else 0
        if dd > max_dd:
            max_dd = dd
        current_dd = dd
        if dd > 0:
            current_duration += 1
            max_duration = max(max_duration, current_duration)
    return (round(max_dd, 4), round(current_dd, 4), max_duration)


def calculate_parametric_var(returns: List[float], confidence: float = 0.95) -> float:
    """Parametric VaR assuming normal distribution.
    Returns the loss threshold at given confidence level."""
    if len(returns) < 3:
        return 0.0
    mean_r = sum(returns) / len(returns)
    variance = sum((r - mean_r) ** 2 for r in returns) / (len(returns) - 1)
    std_dev = math.sqrt(variance)
    # Z-scores for common confidence levels
    z_map = {0.95: 1.645, 0.99: 2.326}
    z = z_map.get(confidence, 1.645)
    return round(abs(mean_r - z * std_dev), 4)


def calculate_historical_var(returns: List[float], confidence: float = 0.95) -> float:
    """Historical VaR using actual return distribution percentiles."""
    if len(returns) < 5:
        return 0.0
    sorted_returns = sorted(returns)
    index = int((1 - confidence) * len(sorted_returns))
    return round(abs(sorted_returns[max(0, index)]), 4)


def calculate_cvar(returns: List[float], confidence: float = 0.95) -> float:
    """Conditional VaR (Expected Shortfall).
    Average of losses beyond VaR threshold."""
    if len(returns) < 5:
        return 0.0
    sorted_returns = sorted(returns)
    cutoff = int((1 - confidence) * len(sorted_returns))
    if cutoff == 0:
        cutoff = 1
    tail = sorted_returns[:cutoff]
    return round(abs(sum(tail) / len(tail)), 4) if tail else 0.0


def calculate_hhi(weights: List[float]) -> float:
    """Herfindahl-Hirschman Index for concentration.
    0 = perfectly diversified, 10000 = single source."""
    if not weights:
        return 0.0
    total = sum(weights) if sum(weights) > 0 else 1.0
    shares = [w / total for w in weights]
    return round(sum(s ** 2 for s in shares) * 10000, 1)


def calculate_beta(method_returns: List[float], market_returns: List[float]) -> Tuple[float, str]:
    """Beta: method sensitivity to market returns.
    Returns (beta, confidence_level)."""
    n = min(len(method_returns), len(market_returns))
    if n < 5:
        return (1.0, "INSUFFICIENT_DATA")
    mr = method_returns[:n]
    mk = market_returns[:n]
    mean_mr = sum(mr) / n
    mean_mk = sum(mk) / n
    covariance = sum((mr[i] - mean_mr) * (mk[i] - mean_mk) for i in range(n)) / (n - 1)
    market_var = sum((mk[i] - mean_mk) ** 2 for i in range(n)) / (n - 1)
    if market_var == 0:
        return (1.0, "ZERO_VARIANCE")
    beta = covariance / market_var
    confidence = "HIGH" if n >= 24 else "MEDIUM" if n >= 12 else "LOW"
    return (round(beta, 3), confidence)


def calculate_information_coefficient(predictions: List[Tuple[str, float, float]]) -> Tuple[float, float, int]:
    """Information Coefficient from alpha predictions vs outcomes.
    predictions: [(alpha_id, predicted_roi, actual_roi), ...]
    Returns (IC, hit_rate, sample_size)."""
    if len(predictions) < 3:
        return (0.0, 0.0, 0)
    correct = sum(1 for _, pred, actual in predictions if (pred > 0) == (actual > 0))
    hit_rate = correct / len(predictions)
    # Rank correlation (simplified Spearman)
    pred_ranks = sorted(range(len(predictions)), key=lambda i: predictions[i][1])
    actual_ranks = sorted(range(len(predictions)), key=lambda i: predictions[i][2])
    n = len(predictions)
    d_sq = sum((pred_ranks[i] - actual_ranks[i]) ** 2 for i in range(n))
    ic = 1 - (6 * d_sq) / (n * (n ** 2 - 1)) if n > 1 else 0
    return (round(ic, 3), round(hit_rate, 3), n)


def calculate_portfolio_risk(
    methods: List[MethodPerformance],
    investments: List[Investment],
    revenue_data: List[Dict],
    expense_data: List[Dict],
    predictions: List[Tuple[str, float, float]] = None,
) -> PortfolioRisk:
    """Main risk orchestrator - calculates all portfolio metrics."""
    risk = PortfolioRisk()

    # Revenue/expense totals
    risk.total_revenue = sum(float(r.get('revenue', 0) or 0) for r in revenue_data)
    risk.total_expenses = sum(float(e.get('amount', '0').replace('$', '').replace(',', '')) for e in expense_data if e.get('amount'))
    risk.net_profit = risk.total_revenue - risk.total_expenses

    # Capital from investments
    risk.capital_deployed = sum(i.capital_allocated for i in investments)
    risk.capital_at_risk = risk.capital_deployed  # All capital at risk in bootstrapping

    # Method counts
    risk.active_method_count = len([m for m in methods if m.status in ('Active', 'ACTIVE')])
    risk.total_method_count = len(methods)

    # Monthly returns from revenue data
    monthly_returns = []
    for r in revenue_data:
        rev = float(r.get('revenue', 0) or 0)
        exp = float(r.get('expenses', 0) or 0)
        monthly_returns.append(rev - exp)

    risk.sharpe_data_months = len(monthly_returns)

    if len(monthly_returns) >= 2:
        risk.portfolio_sharpe = calculate_sharpe_ratio(monthly_returns)
        risk.portfolio_sortino = calculate_sortino_ratio(monthly_returns)
        risk.sharpe_confidence_interval = calculate_sharpe_confidence_interval(monthly_returns, risk.portfolio_sharpe)
        risk.var_95 = calculate_parametric_var(monthly_returns, 0.95)
        risk.var_99 = calculate_parametric_var(monthly_returns, 0.99)
        risk.var_95_historical = calculate_historical_var(monthly_returns, 0.95)
        risk.var_99_historical = calculate_historical_var(monthly_returns, 0.99)
        risk.cvar_95 = calculate_cvar(monthly_returns, 0.95)
        risk.cvar_99 = calculate_cvar(monthly_returns, 0.99)
        dd = calculate_max_drawdown([float(r.get('revenue', 0) or 0) for r in revenue_data])
        risk.max_drawdown, risk.current_drawdown, risk.drawdown_duration = dd

    # Concentration (revenue by method)
    method_revenues = {}
    for r in revenue_data:
        mid = r.get('method_id', 'UNKNOWN')
        method_revenues[mid] = method_revenues.get(mid, 0) + float(r.get('revenue', 0) or 0)
    if method_revenues:
        weights = list(method_revenues.values())
        risk.concentration_hhi = calculate_hhi(weights)
        total_rev = sum(weights) if sum(weights) > 0 else 1.0
        risk.concentration_method_max = max(w / total_rev for w in weights) if weights else 0

    # Information coefficient from predictions
    if predictions and len(predictions) >= 3:
        risk.information_coefficient, risk.ic_hit_rate, risk.ic_sample_size = \
            calculate_information_coefficient(predictions)

    return risk


# =============================================================================
# TOOL / GTM / REVENUE KNOWLEDGE BASE
# =============================================================================

# Comprehensive tool mappings for all 89 methods
TOOLS_MAP = {
    # CORE methods
    "MM001": ["Xcode", "Swift/SwiftUI", "RevenueCat", "App Store Connect", "Firebase", "TestFlight"],
    "MM002": ["Gumroad", "Notion", "Canva", "Lemon Squeezy", "Stripe"],
    "MM003": ["WordPress/Next.js", "Ahrefs", "SurferSEO", "Google Search Console"],
    "MM004": ["Next.js", "Stripe", "Vercel", "Supabase", "Prisma"],
    "MM005": ["Clay", "HeyGen", "CapCut", "Figma", "Calendly"],
    "MM006": ["Buffer", "Hypefury", "CapCut", "Remotion", "ffmpeg"],
    "MM007": ["Instantly", "Smartlead", "Apollo", "Clay", "DeliverOn"],
    "MM008": ["Fiverr", "OnlineJobs.ph", "CapCut", "Notion"],
    "MM009": ["ComfyUI", "Midjourney", "HeyGen", "ElevenLabs", "Stable Diffusion"],
    "MM010": ["OBS", "CapCut", "yt-dlp", "Whisper", "ffmpeg"],
    "MM011": ["Roblox Studio", "Luau", "Blender"],
    "MM012": ["Python", "TradingView", "Alpaca API", "pandas", "backtrader"],
    "MM013": ["Meta Ads Manager", "TikTok Ads", "Google Ads", "Analytics"],
    "MM014": ["Premiere Pro/DaVinci", "Remotion", "YouTube Studio", "TubeBuddy"],
    "MM015": ["Beehiiv", "ConvertKit", "Ghost", "Substack"],
    "MM016": ["TikTok Shop", "Printful", "Printify"],
    "MM017": ["Notion", "Fiverr", "Discord", "PayPal"],
    "MM018": ["RevenueCat", "Superwall", "Firebase A/B", "Statsig"],
    "MM019": ["Xcode", "SwiftUI", "RevenueCat", "Firebase"],
    "MM020": ["Twitter/X", "Gumroad", "Stripe"],
    "MM021": ["Twitter/X", "Blog/Next.js", "Google Search Console"],
    "MM022": ["Temu", "AliExpress", "eBay", "Amazon Seller Central"],
    "MM023": ["Jungle Scout", "Helium 10", "Google Trends"],
    "MM024": ["Printful", "Printify", "Canva", "Merch by Amazon"],
    "MM025": ["Gumroad", "Notion", "Canva", "Lemon Squeezy"],
    "MM026": ["Amazon KDP", "Canva", "BookBolt"],
    "MM027": ["OpenAI API", "Claude API", "Vercel", "Stripe"],
    "MM028": ["Next.js", "Supabase", "Stripe", "Vercel"],
    "MM029": ["Google Business Profile", "Ahrefs", "BrightLocal"],
    "MM030": ["Skool", "Teachable", "Kajabi", "Loom"],
    "MM031": ["Discord", "Skool", "Stripe"],
    "MM032": ["Substack", "Ghost", "Beehiiv"],
    "MM033": ["GoHighLevel", "Vendasta", "SaaS Reseller Tools"],
    "MM034": ["DEXScreener", "Jupiter", "Phantom Wallet", "TweetScout"],
    "MM035": ["Premiere Pro", "CapCut", "AI narration", "YouTube Studio"],
    "MM036": ["Etsy", "Canva", "Inkscape", "SVG tools"],
    "MM037": ["TikTok", "CapCut", "Trending sounds"],
    "MM038": ["Pinterest", "Canva", "Tailwind"],
    "MM039": ["AI narration", "Pexels/stock footage", "CapCut", "YouTube Studio"],
    "MM040": ["Twitter/X", "Stripe", "Gumroad"],
    "MM041": ["Next.js", "Airtable/Supabase", "Stripe"],
    "MM042": ["Lemonsqueezy", "Carrd", "Stripe"],
    "MM044": ["Lovable", "Bolt.new", "Cursor", "Vercel"],
    "MM045": ["GoDaddy Auctions", "Namecheap", "Afternic"],
    "MM046": ["Notion", "Gumroad", "Canva"],
    "MM050": ["Python", "Claude SDK", "npm", "TypeScript"],
    "MM051": ["Claude Code", "n8n", "Make.com", "HeyGen"],
    "MM052": ["HeyGen", "Kling AI", "ElevenLabs", "Cartesia"],
    "MM053": ["OBS", "Kick.com", "StreamElements"],
    "MM054": ["CapCut", "Remotion", "Facebook Creator Studio"],
    "MM055": ["TikTok Shop", "Sample products"],
    "MM056": ["Beehiiv", "SparkLoop"],
    "MM057": ["Fish Audio", "Cartesia", "ElevenLabs"],
    "MM058": ["Reddit", "Python requests", "Google Search Console"],
    "MM059": ["GitHub", "Vercel", "Stripe"],
    "MM060": ["Clay", "Apollo", "Smartlead"],
    "MM061": ["Claude Code", "Cursor", "Replit Agent"],
    "MM062": ["Reddit", "Google Forms"],
    "MM063": ["Threads", "Buffer"],
    "MM064": ["Bluesky", "AT Protocol"],
    "MM065": ["EU AI Act docs", "Compliance frameworks"],
    "MM068": ["n8n", "Docker", "Make.com"],
    "MM069": ["Lovable", "Bolt.new", "v0.dev", "Vercel"],
    # Content Farm
    "CF001": ["ffmpeg", "CapCut", "Remotion", "YouTube Studio", "Spotify"],
    "CF002": ["ffmpeg", "CapCut", "App affiliate links"],
    "CF003": ["RSS feeds", "Buffer", "CapCut"],
    "CF004": ["Meme generators", "CapCut", "Buffer"],
    "CF005": ["Canva", "CapCut", "Buffer"],
    "CF006": ["OBS", "CapCut", "yt-dlp"],
    "CF007": ["Canva", "Buffer", "Notion"],
    "CF008": ["TradingView embeds", "Buffer", "Substack"],
    "CF009": ["Screen recording", "CapCut", "Buffer"],
    "CF010": ["Sports APIs", "CapCut", "Buffer"],
    "CF011": ["CoinGecko API", "CapCut", "Buffer"],
    "CF013": ["CapCut", "Remotion", "YouTube Studio"],
    # AI Influencer
    "AI001": ["ComfyUI", "ChatGPT", "Notion", "Buffer"],
    "AI002": ["ComfyUI", "Leonardo.ai", "ElevenLabs", "Fanvue"],
    "AI003": ["ComfyUI", "Stable Diffusion", "Fanvue", "Fansly"],
    "AI004": ["ElevenLabs", "Whisper", "YouTube Studio"],
    "AI005": ["ComfyUI", "CapCut", "Notion"],
    "AI006": ["Midjourney", "Canva", "Instagram"],
    "AI007": ["OBS", "ComfyUI", "Twitch/Kick"],
    "AI008": ["ChatGPT", "Canva", "TikTok"],
    # Strategy
    "SWARM001": ["Multi-account manager", "Buffer", "Anti-detect browser"],
}

# GTM channel mappings
GTM_MAP = {
    "MM001": ["App Store ASO", "Product Hunt", "Twitter/X", "Reddit"],
    "MM002": ["Gumroad Discover", "Twitter/X", "SEO", "Email list"],
    "MM003": ["SEO", "Pinterest", "GEO", "Reddit"],
    "MM004": ["Product Hunt", "Twitter/X", "Cold email", "Indie Hackers"],
    "MM005": ["LinkedIn", "Cold email", "Referrals", "Upwork"],
    "MM006": ["TikTok", "YT Shorts", "IG Reels", "Twitter/X"],
    "MM007": ["Cold email", "LinkedIn DM", "Twitter DM", "Voice notes"],
    "MM008": ["Agency outbound", "Fiverr", "Upwork"],
    "MM009": ["Twitter/X", "Instagram", "Fanvue/Fansly", "TikTok"],
    "MM010": ["TikTok", "YouTube Shorts", "Twitter clips"],
    "MM011": ["Roblox discovery", "YouTube", "TikTok"],
    "MM013": ["Meta Ads", "TikTok Ads", "Google Ads"],
    "MM014": ["YouTube SEO", "Reddit", "Twitter/X"],
    "MM015": ["SEO", "Twitter/X", "SparkLoop referrals", "Beehiiv recommendations"],
    "MM016": ["TikTok organic", "TikTok Shop affiliate network"],
    "MM022": ["eBay", "Amazon", "Etsy", "Facebook Marketplace"],
    "MM024": ["Etsy", "Amazon Merch", "TikTok", "Pinterest"],
    "MM025": ["Gumroad Discover", "Twitter/X", "SEO", "Product Hunt"],
    "MM029": ["Google Maps SEO", "Local directories", "Cold outreach"],
    "MM035": ["YouTube SEO", "TikTok clips", "Reddit"],
    "MM039": ["YouTube SEO", "Reddit", "Pinterest"],
    "MM046": ["Gumroad Discover", "Twitter/X", "Reddit", "Pinterest"],
    "MM050": ["GitHub", "Twitter/X", "Anthropic marketplace"],
    "MM052": ["TikTok Shop", "Brand cold outreach", "Upwork"],
    "MM054": ["Facebook Reels", "Cross-post from TikTok/YT"],
    "MM055": ["TikTok organic", "TikTok Shop affiliate"],
    "MM056": ["SEO", "Twitter/X", "SparkLoop", "Beehiiv recommendations"],
    "MM058": ["Reddit organic", "Google SEO/GEO"],
    "MM061": ["Twitter/X", "LinkedIn", "Upwork", "Indie Hackers"],
    "MM068": ["YouTube tutorials", "Twitter/X", "n8n community"],
    "MM069": ["Product Hunt", "Twitter/X", "Indie Hackers"],
    "AI002": ["Twitter/X findom", "Fanvue", "Fansly", "Reddit", "FetLife"],
}

# Revenue models
REVENUE_MODELS = {
    "MM001": "IAP + Subscriptions ($2.99-$9.99/mo)",
    "MM002": "One-time sales ($9-$97) + bundles",
    "MM003": "Affiliate commission (3-50%)",
    "MM004": "MRR ($9-$99/mo/user)",
    "MM005": "Project ($2K-$15K) + retainer ($1.5K/mo)",
    "MM006": "Creator Fund + Affiliate + Sponsors",
    "MM007": "Per-lead ($50-$500) or retainer ($2K-$10K/mo)",
    "MM008": "Markup (300-500% on $3-25 UGC)",
    "MM009": "Subs ($10-$50/mo) + PPV + Custom + Tips",
    "MM010": "Creator Fund + Sponsorships",
    "MM013": "Traffic arbitrage (CPA - ad spend)",
    "MM015": "Subs ($5-$50/mo) + Sponsors ($20-$200 CPM) + Boosts",
    "MM022": "Markup ($0.73 -> $46 jewelry documented)",
    "MM024": "40-60% margins on POD",
    "MM025": "Digital products ($5-$97, zero marginal cost)",
    "MM029": "Rank-and-rent ($500-$3K/mo per site)",
    "MM046": "Notion templates ($5-$29, zero marginal cost)",
    "MM050": "API access + marketplace (MCP servers)",
    "MM052": "$50-$500/video (HeyGen + Kling)",
    "MM054": "$0.02-$0.60/1K views (FB Reels, debunked from $4.40)",
    "MM055": "5-20% commission (TikTok Shop)",
    "MM056": "Subs + Boosts + Sponsors (0% fee vs Substack 13%)",
    "MM058": "Traffic -> Affiliate (Reddit #2 in Google US)",
    "MM061": "$100-$500/hr (Claude Code, AI coding)",
    "MM069": "SaaS built + sold (Lovable $20M ARR in 2 months)",
    "AI002": "Tributes ($20-$500) + Custom ($50-$1000) + Subs ($10-$50/mo)",
}

# Launch strategies
LAUNCH_STRATEGIES = {
    "MM001": "TestFlight beta -> Product Hunt -> X building-in-public -> ASO",
    "MM006": "Viral hooks testing -> Algorithm optimization -> Cross-platform repurpose",
    "MM007": "21d warmup -> Intent targeting -> Multi-touch 4-email sequences",
    "MM009": "Character consistency -> Platform disclosure -> Fanvue/IG launch",
    "MM015": "SEO foundation -> Twitter growth -> Sponsor outreach at 1K subs",
    "MM022": "Source 5 products -> List on 2 platforms -> Test pricing -> Scale winners",
    "MM024": "Trending phrase capture -> Same-day design -> Multi-platform listing",
    "MM046": "Build 5 templates -> List on Gumroad -> Twitter/Reddit promotion",
    "MM050": "Build MCP server -> Open source -> Paid tier for advanced features",
    "MM052": "HeyGen + Kling setup -> 10 sample videos -> Cold outreach to brands",
    "MM054": "Cross-post ALL existing content to FB Reels immediately",
    "MM058": "Value-first Reddit posts -> Build karma -> Evergreen SEO traffic",
    "MM061": "Ship portfolio projects -> Twitter showcase -> Upwork/LinkedIn outreach",
    "AI002": "Leonardo.ai character -> 200+ images -> Fanvue tiers -> Twitter findom",
}


# =============================================================================
# DATA LOADERS
# =============================================================================

def load_csv(filepath: Path) -> List[Dict[str, str]]:
    """Load CSV file into list of dicts"""
    if not filepath.exists():
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception:
        return []


def load_alpha_staging() -> List[AlphaEntry]:
    """Load alpha entries from ALPHA_STAGING.csv"""
    rows = load_csv(LEDGER_DIR / "ALPHA_STAGING.csv")
    entries = []
    for row in rows:
        try:
            days = 0
            date_str = row.get('date_added') or row.get('date_discovered') or row.get('date', '')
            if date_str:
                try:
                    disc_date = datetime.strptime(date_str.strip().split()[0], '%Y-%m-%d')
                    days = (datetime.now() - disc_date).days
                except Exception:
                    pass
            decay = min(90, days * 0.375) if days > 0 else 0
            entries.append(AlphaEntry(
                alpha_id=row.get('alpha_id', 'UNKNOWN'),
                source=row.get('source', ''),
                category=row.get('category', ''),
                tactic=(row.get('tactic', '') or '')[:80],
                roi_potential=row.get('roi_potential', 'MEDIUM'),
                status=row.get('status', 'PENDING_REVIEW'),
                backtest_score=int(row.get('backtest_score', 0) or 0),
                days_since_discovery=days,
                alpha_decay_pct=decay,
            ))
        except Exception:
            continue
    return entries


def load_money_methods() -> List[MethodPerformance]:
    """Load all 89 money methods with tools/GTM from knowledge base"""
    rows = load_csv(LEDGER_DIR / "MONEY_METHODS_TRACKER.csv")
    methods = []
    for row in rows:
        try:
            mid = row.get('method_id', '')
            cat = row.get('category', 'CORE')
            # Get tools from knowledge base, with category fallback
            tools = TOOLS_MAP.get(mid, _category_tools(mid, cat))
            gtm = GTM_MAP.get(mid, _category_gtm(mid, cat))
            methods.append(MethodPerformance(
                method_id=mid,
                method_name=row.get('method_name', ''),
                status=row.get('status', 'New'),
                category=cat,
                revenue_model=REVENUE_MODELS.get(mid, row.get('revenue_model', 'TBD')),
                priority=row.get('priority', ''),
                notes=row.get('notes', ''),
                tools_used=tools,
                gtm_channels=gtm,
                launch_strategy=LAUNCH_STRATEGIES.get(mid, "Define GTM plan -> Build -> Launch -> Iterate"),
            ))
        except Exception:
            continue
    return methods


def _category_tools(method_id: str, category: str) -> List[str]:
    """Fallback tools by method category"""
    if 'CF' in method_id:
        return ["CapCut", "Buffer", "Remotion"]
    elif 'AI' in method_id:
        return ["ComfyUI", "HeyGen", "ElevenLabs"]
    elif category == 'CONTENT_FARM':
        return ["CapCut", "Buffer", "YouTube Studio"]
    elif category == 'AI_INFLUENCER':
        return ["ComfyUI", "Midjourney", "Social platforms"]
    return ["TBD - needs tool stack"]


def _category_gtm(method_id: str, category: str) -> List[str]:
    """Fallback GTM channels by category"""
    if 'CF' in method_id or category == 'CONTENT_FARM':
        return ["TikTok", "YouTube Shorts", "Instagram Reels"]
    elif 'AI' in method_id or category == 'AI_INFLUENCER':
        return ["Twitter/X", "Instagram", "Platform-specific"]
    return ["Twitter/X", "SEO", "Cold outreach"]


def load_active_investments() -> List[Investment]:
    """Load from ACTIVE_INVESTMENTS.csv"""
    rows = load_csv(LEDGER_DIR / "ACTIVE_INVESTMENTS.csv")
    investments = []
    for row in rows:
        try:
            cap = row.get('capital_allocated', '$0').replace('$', '').replace(',', '')
            investments.append(Investment(
                investment_id=row.get('investment_id', ''),
                method_id=row.get('method_id', ''),
                name=row.get('name', ''),
                category=row.get('category', ''),
                status=row.get('status', ''),
                capital_allocated=float(cap) if cap else 0.0,
                time_invested_hrs=float(row.get('time_invested_hrs', 0) or 0),
                revenue_to_date=float(row.get('revenue_to_date', '$0').replace('$', '').replace(',', '') or 0),
                next_action=row.get('next_action', ''),
                priority=row.get('priority', ''),
                notes=row.get('notes', ''),
            ))
        except Exception:
            continue
    return investments


def load_synergies() -> List[Synergy]:
    """Load cross-pollination synergies"""
    rows = load_csv(LEDGER_DIR / "CROSS_POLLINATION_MATRIX.csv")
    synergies = []
    for row in rows:
        try:
            synergies.append(Synergy(
                synergy_id=row.get('synergy_id', ''),
                method_1=row.get('method_1', ''),
                method_2=row.get('method_2', ''),
                synergy_score=int(row.get('synergy_score', 0) or 0),
                synergy_type=row.get('synergy_type', ''),
                revenue_multiplier=float(row.get('revenue_multiplier', 1.0) or 1.0),
                implementation_notes=row.get('implementation_notes', ''),
                priority=row.get('priority', ''),
            ))
        except Exception:
            continue
    return synergies


def load_growth_tactics() -> List[GrowthTactic]:
    """Comprehensive growth tactics from EDGE_GROWTH_TACTICS.md data"""
    return [
        # Instagram
        GrowthTactic("Instagram", "Reels (algorithm priority)", "SAFE", "3-5/day", "Best organic reach format 2026", "WORKING"),
        GrowthTactic("Instagram", "Story views automation", "SAFE", "Unlimited", "Undetectable, safe to scale", "WORKING"),
        GrowthTactic("Instagram", "Targeted likes (competitor followers)", "SAFE", "100-150/day aged", "Kicksta $49-99/mo or Growthoid $49-99/mo", "WORKING"),
        GrowthTactic("Instagram", "First-comment on big accounts", "SAFE", "20-30/day", "Authority building tactic", "WORKING"),
        GrowthTactic("Instagram", "Collab posts", "SAFE", "Unlimited", "Guest content on partner accounts", "WORKING"),
        GrowthTactic("Instagram", "Follow/Unfollow", "GREY", "30-50/day aged", "Mobile proxies REQUIRED. Residential flagged.", "WORKING"),
        GrowthTactic("Instagram", "Chrome extensions", "DEAD", "N/A", "Instant detection on all platforms since 2024", "PATCHED"),
        GrowthTactic("Instagram", "Mass DM automation", "DEAD", "N/A", "Restricted quickly, not worth risk", "PATCHED"),
        # TikTok
        GrowthTactic("TikTok", "Organic posting 3-5x/day", "SAFE", "3-5 posts/day", "ONLY recommended approach. Hook in 1s critical.", "WORKING"),
        GrowthTactic("TikTok", "Duet/Stitch viral content", "SAFE", "Unlimited", "Best organic traction method", "WORKING"),
        GrowthTactic("TikTok", "Trending sounds (within 48hr)", "SAFE", "Unlimited", "Critical timing window", "WORKING"),
        GrowthTactic("TikTok", "Native scheduler", "SAFE", "Unlimited", "Only safe scheduling method", "WORKING"),
        GrowthTactic("TikTok", "ALL automation tools", "DEAD", "N/A", "Detection too aggressive 2026. No VPN.", "PATCHED"),
        GrowthTactic("TikTok", "Bought views", "DEAD", "N/A", "Algorithm detects, account flagged", "PATCHED"),
        # Twitter/X
        GrowthTactic("Twitter/X", "Reply-guy strategy", "SAFE", "50-100/day", "First to reply on big accounts. Most lenient platform.", "WORKING"),
        GrowthTactic("Twitter/X", "Engagement pods", "SAFE", "Unlimited", "Private groups, legal", "WORKING"),
        GrowthTactic("Twitter/X", "Thread format (authority)", "SAFE", "4-8x/day tweets", "Self-reply funnels for CTAs", "WORKING"),
        GrowthTactic("Twitter/X", "Quote tweets with value", "SAFE", "20-50/day", "Builds on existing viral content", "WORKING"),
        GrowthTactic("Twitter/X", "Hypefury scheduling", "SAFE", "Unlimited", "$19-49/mo. Best for creators.", "WORKING"),
        # LinkedIn
        GrowthTactic("LinkedIn", "Carousels/documents", "SAFE", "3-5x/week", "Highest reach format 2026", "WORKING"),
        GrowthTactic("LinkedIn", "Voice notes DMs", "SAFE", "10-20/day", "3x higher response rate. BEST tactic.", "WORKING"),
        GrowthTactic("LinkedIn", "Comment before connecting", "SAFE", "10+ posts/day", "Engage 2+ weeks before outreach", "WORKING"),
        GrowthTactic("LinkedIn", "Cloud automation (Expandi)", "GREY", "50 connections/day max", "Expandi $99/mo. NO Chrome extensions.", "WORKING"),
        GrowthTactic("LinkedIn", "Dripify drip sequences", "GREY", "50/day", "Dripify $59/mo. Cloud-only.", "WORKING"),
        GrowthTactic("LinkedIn", "Chrome extensions", "DEAD", "N/A", "Instant detection. Cloud-only now.", "PATCHED"),
        GrowthTactic("LinkedIn", "Desktop automation", "DEAD", "N/A", "Jarvee/Phantombuster banned on LinkedIn", "PATCHED"),
        # Email
        GrowthTactic("Email", "Multi-inbox rotation (3-5)", "SAFE", "30/day/inbox", "Instantly $37-97/mo or Smartlead $39-94/mo", "WORKING"),
        GrowthTactic("Email", "Plain text only", "SAFE", "All sends", "HTML = instant spam flag 2026", "WORKING"),
        GrowthTactic("Email", "Open tracking OFF", "SAFE", "All sends", "Gmail shows warning label if tracked", "WORKING"),
        GrowthTactic("Email", "Intent-based timing", "SAFE", "Unlimited", "Within 48hr of trigger = 2-4x reply rate", "WORKING"),
        GrowthTactic("Email", "Subdomain isolation", "SAFE", "Always", "Never cold email from main domain", "WORKING"),
        GrowthTactic("Email", "Pre-warmed inboxes (DeliverOn)", "SAFE", "Instant start", "DeliverOn $49/mo. Skip DIY warmup.", "WORKING"),
        GrowthTactic("Email", "Single inbox campaigns", "DEAD", "N/A", "Domain burning certain in 2026", "PATCHED"),
        # Engagement bootstrapping
        GrowthTactic("Cross-platform", "Launch coordination", "SAFE", "Per launch", "Friends/community upvote. Legal.", "WORKING"),
        GrowthTactic("Cross-platform", "Shoutout trades", "SAFE", "Unlimited", "Exchange posts with similar accounts", "WORKING"),
        GrowthTactic("Cross-platform", "Paid shoutouts", "SAFE", "$20-500/post", "Pay accounts to mention you. Legal.", "WORKING"),
    ]


def load_growth_services() -> List[GrowthService]:
    """Growth services with real pricing from EDGE_GROWTH_TACTICS.md"""
    return [
        # Instagram
        GrowthService("Instagram", "Kicksta", "$49-99/mo", "AI-targeted likes/follows", "HIGH", "100-500 followers/mo"),
        GrowthService("Instagram", "Growthoid", "$49-99/mo", "Human team engagement", "HIGHEST", "200-800 followers/mo"),
        GrowthService("Instagram", "Upleap", "$59-99/mo", "Managed service", "HIGH", "300-1000 followers/mo"),
        GrowthService("Instagram", "Jarvee", "$30-70/mo + proxies", "Desktop automation", "MEDIUM", "Full control but risky"),
        # TikTok
        GrowthService("TikTok", "Manual only", "Free", "Content + engagement", "HIGHEST", "ONLY recommended approach"),
        # Twitter/X
        GrowthService("Twitter/X", "Hypefury", "$19-49/mo", "Scheduling + engagement", "HIGH", "Best for creators"),
        GrowthService("Twitter/X", "TweetHunter", "$49/mo", "AI tweets + CRM", "HIGH", "Growth-focused"),
        GrowthService("Twitter/X", "Buffer/Hootsuite", "Free-$15/mo", "Scheduling", "HIGHEST", "Safe option"),
        # LinkedIn
        GrowthService("LinkedIn", "Expandi", "$99/mo", "Cloud automation", "HIGHEST", "Safest automation"),
        GrowthService("LinkedIn", "Dripify", "$59/mo", "Drip sequences", "HIGH", "Good sequences"),
        GrowthService("LinkedIn", "Waalaxy", "$56/mo", "Multi-channel", "MEDIUM", "Also does email"),
        # Email
        GrowthService("Email", "Instantly", "$37-97/mo", "Warmup + sending", "HIGH", "Best all-in-one"),
        GrowthService("Email", "Smartlead", "$39-94/mo", "AI warmup + scale", "HIGH", "Good for volume"),
        GrowthService("Email", "DeliverOn", "$49/mo", "Pre-warmed inboxes", "HIGH", "Skip DIY warmup"),
        GrowthService("Email", "MailForge", "$3/inbox", "Bulk warm inboxes", "MEDIUM", "Scale option"),
        GrowthService("Email", "Warmbox", "$15-69/mo", "Standalone warmup", "MEDIUM", "Budget option"),
    ]


def load_revenue_data() -> List[Dict]:
    """Load revenue tracker"""
    return load_csv(FINANCIALS_DIR / "REVENUE_TRACKER.csv")


def load_expense_data() -> List[Dict]:
    """Load expense tracker"""
    return load_csv(FINANCIALS_DIR / "EXPENSE_TRACKER.csv")


def load_content_pipeline_stats() -> Dict[str, int]:
    """Get content pipeline counts"""
    rows = load_csv(LEDGER_DIR / "CONTENT_PIPELINE.csv")
    stats = {"total": len(rows), "queued": 0, "published": 0, "draft": 0}
    for row in rows:
        s = (row.get('status', '') or '').upper()
        if 'QUEUE' in s:
            stats["queued"] += 1
        elif 'PUBLISH' in s:
            stats["published"] += 1
        elif 'DRAFT' in s:
            stats["draft"] += 1
    return stats


def load_rbi_scan() -> RBIScanResult:
    """Load the most recent RBI audit scan from LEDGER/RBI_AUDITS/"""
    result = RBIScanResult()

    # Find most recent scan file (could be .md or .csv)
    if not RBI_AUDITS_DIR.exists():
        return result

    # Look for any RBI audit files, sorted by name (date-based naming)
    audit_files = sorted(RBI_AUDITS_DIR.glob("RBI_AUDIT_*.md"), reverse=True)
    if not audit_files:
        audit_files = sorted(RBI_AUDITS_DIR.glob("rbi_scan_*.csv"), reverse=True)

    if not audit_files:
        return result

    latest = audit_files[0]
    result.scan_date = latest.stem.replace("RBI_AUDIT_", "").replace("rbi_scan_", "").replace("_full", "").replace("_daily", "").replace("_weekly", "").replace("_monthly", "")

    # Parse the markdown audit report
    try:
        content = latest.read_text(encoding='utf-8', errors='replace')

        # Extract total alpha
        m = re.search(r'Total alpha entries:\s*(\d+)', content)
        if m:
            result.total_alpha = int(m.group(1))

        # Extract pending
        m = re.search(r'PENDING_REVIEW:\s*(\d+)', content)
        if m:
            result.pending_alpha = int(m.group(1))

        # Extract HIGH/HIGHEST ROI pending
        m = re.search(r'HIGH/HIGHEST ROI pending review:\s*(\d+)', content)
        if m:
            result.high_roi_pending = int(m.group(1))

        # Extract active methods
        m = re.search(r'Active methods:\s*(\d+)', content)
        if m:
            result.active_methods = int(m.group(1))

        # Extract total methods
        m = re.search(r'Total methods:\s*(\d+)', content)
        if m:
            result.total_methods = int(m.group(1))

        # Extract content stats
        m = re.search(r'Total content pieces:\s*(\d+)', content)
        if m:
            result.content_total = int(m.group(1))

        m = re.search(r'QUEUED:\s*(\d+)', content)
        if m:
            result.content_queued = int(m.group(1))

        # Extract categories
        cat_section = re.search(r'Top categories:\s*\n((?:\s+\w[\w_]*:?\s*\d+\n?)+)', content)
        if cat_section:
            for line in cat_section.group(1).strip().split('\n'):
                parts = line.strip().split(':')
                if len(parts) >= 2:
                    cat_name = parts[0].strip()
                    cat_count = parts[1].strip().split()[0] if parts[1].strip() else '0'
                    try:
                        result.top_categories[cat_name] = int(cat_count)
                    except ValueError:
                        pass

        # Extract ROI distribution
        roi_section = re.search(r'ROI distribution:\s*\n((?:\s+\w+:?\s*\d+\n?)+)', content)
        if roi_section:
            for line in roi_section.group(1).strip().split('\n'):
                parts = line.strip().split(':')
                if len(parts) >= 2:
                    roi_name = parts[0].strip()
                    roi_count = parts[1].strip().split()[0] if parts[1].strip() else '0'
                    try:
                        result.roi_distribution[roi_name] = int(roi_count)
                    except ValueError:
                        pass

        # Extract recommendations
        for line in content.split('\n'):
            if line.strip().startswith('- CRITICAL:') or line.strip().startswith('- IMPORTANT:') or line.strip().startswith('- OPPORTUNITY:') or line.strip().startswith('- EXECUTION'):
                result.recommendations.append(line.strip().lstrip('- '))

        # Extract underallocated methods
        underalloc_section = re.search(r'UNDERALLOCATED:.*?\n((?:\s+\w.*?\n?)+)', content)
        if underalloc_section:
            for line in underalloc_section.group(1).strip().split('\n'):
                line = line.strip()
                if ':' in line:
                    parts = line.split(':')
                    result.underallocated_methods.append({
                        "name": parts[0].strip(),
                        "potential": parts[1].strip() if len(parts) > 1 else "TBD",
                    })

        # Extract top synergy pairs
        syn_section = re.search(r'Top synergy pairs:\s*\n((?:\s+.*?\n?)+?)(?:\n\n|## )', content)
        if syn_section:
            for line in syn_section.group(1).strip().split('\n'):
                line = line.strip()
                m2 = re.match(r'(.+?)\s*[x×]\s*(.+?)\s*=\s*(.+?)x?\s*multiplier', line)
                if m2:
                    result.top_synergy_pairs.append({
                        "method_1": m2.group(1).strip(),
                        "method_2": m2.group(2).strip(),
                        "multiplier": m2.group(3).strip(),
                    })

    except Exception:
        pass

    # Also try to load JSON integrate file if it exists
    json_files = sorted(RBI_AUDITS_DIR.glob("rbi_integrate_*.json"), reverse=True)
    if json_files:
        try:
            data = json.loads(json_files[0].read_text())
            if isinstance(data, dict):
                result.total_alpha = data.get('total_alpha', result.total_alpha)
                result.pending_alpha = data.get('pending_alpha', result.pending_alpha)
                result.active_methods = data.get('active_methods', result.active_methods)
                result.total_methods = data.get('total_methods', result.total_methods)
        except Exception:
            pass

    return result


def load_zero_cost_ops() -> List[ZeroCostOp]:
    """Load zero-cost ops categories from the audit and existing data"""

    # The 8 gap categories from the full audit + operational categories
    ZERO_COST_CATEGORIES = [
        # From FULL_AUDIT_MISSING_OPS.md gap categories
        {"cat": "Meme Repurpose", "desc": "Cross-platform meme farming, rage bait, reply bait", "rev_low": 200, "rev_high": 5000},
        {"cat": "Ecom/Dropship", "desc": "Temu->eBay arb, TikTok Shop, print-on-demand", "rev_low": 500, "rev_high": 20000},
        {"cat": "Affiliate Networks", "desc": "Affiliate marketing, referral programs", "rev_low": 200, "rev_high": 10000},
        {"cat": "Community Platforms", "desc": "Whop, Skool, Telegram, Discord monetization", "rev_low": 1000, "rev_high": 50000},
        {"cat": "Clip Armies", "desc": "Coordinated distribution, clipper networks", "rev_low": 500, "rev_high": 54000},
        {"cat": "Growth Hacks", "desc": "Platform-specific organic growth tactics", "rev_low": 0, "rev_high": 0},
        {"cat": "Service/Agency", "desc": "Freelance arb, AI automation agency", "rev_low": 2000, "rev_high": 50000},
        {"cat": "Novel AI Methods", "desc": "AI companions, AI music, AI UGC", "rev_low": 500, "rev_high": 20000},
        # Operational zero-cost categories
        {"cat": "Content Farm", "desc": "Multi-niche content accounts (faith, fitness, AI, sleep)", "rev_low": 500, "rev_high": 10000},
        {"cat": "Newsletter", "desc": "Beehiiv newsletters (3 niches), SparkLoop referrals", "rev_low": 500, "rev_high": 68000},
        {"cat": "Digital Products", "desc": "Notion templates, Gumroad/Whop products", "rev_low": 200, "rev_high": 10000},
        {"cat": "Cold Outbound", "desc": "Email sequences, LinkedIn DMs, voice notes", "rev_low": 2000, "rev_high": 50000},
        {"cat": "AI Influencer", "desc": "SFW + NSFW AI personas, findom", "rev_low": 500, "rev_high": 50000},
        {"cat": "Personal Brand", "desc": "@PRINTMAXXER building-in-public", "rev_low": 0, "rev_high": 20000},
        {"cat": "App Factory", "desc": "PrayerLock, WalkToUnlock, StudyLock, biomaxx", "rev_low": 1000, "rev_high": 50000},
        {"cat": "SEO/GEO", "desc": "Truth pages, longtail content, Reddit SEO", "rev_low": 200, "rev_high": 20000},
        {"cat": "Freelance Arb", "desc": "Claude Code services on Fiverr/Upwork", "rev_low": 2000, "rev_high": 30000},
    ]

    ops = []

    # Load accounts to determine which categories have active accounts
    accounts = load_csv(ACCOUNTS_CSV)
    account_niches = set()
    account_statuses = {}
    for acc in accounts:
        niche = (acc.get('Niche', '') or '').lower()
        status = (acc.get('Status', '') or '').upper()
        account_niches.add(niche)
        key = f"{niche}_{acc.get('Platform', '')}"
        account_statuses[key] = status

    # Check social setup output for what has been built
    social_setup_files = set()
    if SOCIAL_SETUP_OUTPUT.exists():
        social_setup_files = {f.name for f in SOCIAL_SETUP_OUTPUT.iterdir() if f.is_file()}

    # Check master ops output
    master_ops_files = set()
    if MASTER_OPS_OUTPUT.exists():
        master_ops_files = {f.name for f in MASTER_OPS_OUTPUT.iterdir() if f.is_file()}

    # Load gap counts from FULL_AUDIT if available
    gap_counts = {}
    audit_path = SOCIAL_SETUP_OUTPUT / "FULL_AUDIT_MISSING_OPS.md"
    if audit_path.exists():
        try:
            audit_content = audit_path.read_text(encoding='utf-8', errors='replace')
            # Count GAP entries per category
            for gap_match in re.finditer(r'### GAP-\d+:.*?\n.*?Category:\*\*\s*(\w+)', audit_content):
                cat = gap_match.group(1)
                gap_counts[cat] = gap_counts.get(cat, 0) + 1
        except Exception:
            pass

    # Map category to status based on what's been built
    status_map = {
        "Content Farm": "ready" if "T3_sleep_tweets_50.md" in social_setup_files else "not_started",
        "Newsletter": "ready" if any("newsletter" in f.lower() for f in social_setup_files) else "not_started",
        "Digital Products": "ready" if "gumroad_spec.md" in master_ops_files else "not_started",
        "Cold Outbound": "ready" if any("outreach" in f.lower() for f in master_ops_files) else "not_started",
        "AI Influencer": "not_started",
        "Personal Brand": "ready" if any(s == 'PENDING' for k, s in account_statuses.items() if 'meta' in k) else "not_started",
        "App Factory": "ready",
        "SEO/GEO": "ready",
        "Freelance Arb": "ready" if MASTER_OPS_XLSX.exists() else "not_started",
        "Meme Repurpose": "ready" if "MEME_REPURPOSE_STRATEGY.md" in social_setup_files else "not_started",
        "Ecom/Dropship": "ready" if "ECOM_LAUNCH_PLAN.md" in social_setup_files else "not_started",
        "Affiliate Networks": "not_started",
        "Community Platforms": "not_started",
        "Clip Armies": "not_started",
        "Growth Hacks": "ready" if "T5_warmup_schedule.md" in social_setup_files else "not_started",
        "Service/Agency": "not_started",
        "Novel AI Methods": "not_started",
    }

    for cat_def in ZERO_COST_CATEGORIES:
        cat_name = cat_def["cat"]
        status = status_map.get(cat_name, "not_started")
        gaps = gap_counts.get(cat_name.lower().replace("/", "_").replace(" ", "_"), 0)

        ops.append(ZeroCostOp(
            category=cat_name,
            description=cat_def["desc"],
            status=status,
            opportunity_count=gaps if gaps > 0 else 1,
            revenue_potential_low=cat_def["rev_low"],
            revenue_potential_high=cat_def["rev_high"],
            gaps_found=gaps,
        ))

    return ops


def load_accounts() -> List[AccountStatus]:
    """Load account portfolio from ACCOUNTS.csv"""
    rows = load_csv(ACCOUNTS_CSV)
    accounts = []
    for row in rows:
        accounts.append(AccountStatus(
            niche=row.get('Niche', ''),
            platform=row.get('Platform', ''),
            handle=row.get('Handle', ''),
            status=row.get('Status', ''),
            notes=row.get('Notes', ''),
        ))
    return accounts


def load_social_setup_outputs() -> Dict[str, Any]:
    """Load summary of social setup loop outputs"""
    summary = {
        "total_files": 0,
        "bios_ready": False,
        "image_prompts_ready": False,
        "content_ready": False,
        "newsletters_ready": 0,
        "warmup_schedule": False,
        "posting_schedule": False,
        "accounts_updated": False,
        "ecom_plan": False,
        "meme_strategy": False,
        "cross_promo": False,
        "audit_complete": False,
        "files": [],
    }

    if not SOCIAL_SETUP_OUTPUT.exists():
        return summary

    files = [f for f in SOCIAL_SETUP_OUTPUT.iterdir() if f.is_file()]
    summary["total_files"] = len(files)
    summary["files"] = [f.name for f in files]

    for f in files:
        name = f.name.lower()
        if "bio" in name:
            summary["bios_ready"] = True
        if "image_prompt" in name:
            summary["image_prompts_ready"] = True
        if "tweet" in name or "video_script" in name or "calendar" in name:
            summary["content_ready"] = True
        if "newsletter" in name:
            summary["newsletters_ready"] += 1
        if "warmup" in name:
            summary["warmup_schedule"] = True
        if "posting_schedule" in name or "T8_posting" in name:
            summary["posting_schedule"] = True
        if "ACCOUNTS" in f.name:
            summary["accounts_updated"] = True
        if "ECOM" in f.name:
            summary["ecom_plan"] = True
        if "MEME" in f.name:
            summary["meme_strategy"] = True
        if "cross_promo" in name:
            summary["cross_promo"] = True
        if "FULL_AUDIT" in f.name:
            summary["audit_complete"] = True

    return summary


# =============================================================================
# RECOMMENDATIONS ENGINE
# =============================================================================

def generate_recommendations(
    methods: List[MethodPerformance],
    alpha: List[AlphaEntry],
    investments: List[Investment],
    synergies: List[Synergy],
    risk: PortfolioRisk,
    content_stats: Dict[str, int],
) -> List[RecommendedAction]:
    """Cross-references all data sources for intelligent recommendations"""
    recs = []

    # 1. CRITICAL: Investments with CRITICAL priority
    critical_invs = [i for i in investments if i.priority == 'CRITICAL' and i.status == 'READY']
    for inv in critical_invs:
        recs.append(RecommendedAction(
            priority="CRITICAL",
            category="INVESTMENT",
            action=f"Execute: {inv.name}",
            reason=f"${inv.capital_allocated} allocated, status READY. Next: {inv.next_action}",
        ))

    # 2. CRITICAL: Large pending alpha backlog
    pending = [a for a in alpha if a.status == 'PENDING_REVIEW']
    if len(pending) > 50:
        decaying = [a for a in pending if a.days_since_discovery > 30]
        recs.append(RecommendedAction(
            priority="CRITICAL",
            category="ALPHA",
            action=f"Review {len(pending)} pending alpha ({len(decaying)} decaying >30d)",
            reason="Alpha decay erodes value. Run /review-alpha",
            command="/review-alpha",
        ))

    # 3. HIGH: Ready investments
    ready_invs = [i for i in investments if i.priority == 'HIGH' and i.status == 'READY']
    for inv in ready_invs[:3]:
        recs.append(RecommendedAction(
            priority="HIGH",
            category="INVESTMENT",
            action=f"Launch: {inv.name}",
            reason=f"Next: {inv.next_action}",
        ))

    # 4. HIGH: Top synergies not yet exploited
    top_synergies = sorted(synergies, key=lambda s: s.synergy_score, reverse=True)[:5]
    active_ids = {m.method_id for m in methods if m.status in ('Active', 'ACTIVE')}
    for syn in top_synergies:
        if syn.method_1 in active_ids and syn.method_2 not in active_ids:
            recs.append(RecommendedAction(
                priority="HIGH",
                category="SYNERGY",
                action=f"Activate {syn.method_2} (synergy {syn.synergy_score}, {syn.revenue_multiplier}x multiplier with {syn.method_1})",
                reason=syn.implementation_notes[:80],
            ))

    # 5. MEDIUM: Content pipeline
    if content_stats.get("queued", 0) > 100 and content_stats.get("published", 0) == 0:
        recs.append(RecommendedAction(
            priority="MEDIUM",
            category="EXECUTION",
            action=f"Publish content ({content_stats['queued']} queued, 0 published)",
            reason="Content sitting idle. Upload Buffer CSVs.",
            command="Upload AUTOMATIONS/content_posting/*.csv to Buffer",
        ))

    # 6. MEDIUM: High-ROI approved alpha not deployed
    high_roi = [a for a in alpha if a.roi_potential == 'HIGHEST' and a.status == 'APPROVED']
    if high_roi:
        recs.append(RecommendedAction(
            priority="MEDIUM",
            category="ALPHA",
            action=f"Deploy {len(high_roi)} HIGHEST ROI approved alpha",
            reason="Backtested and approved. Execute now.",
        ))

    # 7. MEDIUM: Revenue concentration
    if risk.concentration_hhi > 5000:
        recs.append(RecommendedAction(
            priority="MEDIUM",
            category="RISK",
            action="Diversify revenue (HHI > 5000 = concentrated)",
            reason=f"HHI: {risk.concentration_hhi:.0f}. Target < 3000.",
        ))

    # 8. RBI Scanner recommendations
    rbi = load_rbi_scan()
    if rbi.scan_date:
        if rbi.high_roi_pending > 20:
            recs.append(RecommendedAction(
                priority="HIGH",
                category="ALPHA",
                action=f"RBI: {rbi.high_roi_pending} HIGH/HIGHEST ROI alpha pending",
                reason=f"Last scan: {rbi.scan_date}. Review before decay.",
                command="/review-alpha",
            ))
        for rec_text in rbi.recommendations[:2]:
            recs.append(RecommendedAction(
                priority="MEDIUM",
                category="RBI",
                action=f"RBI: {rec_text[:60]}",
                reason="From RBI scanner",
            ))

    # 9. Zero-cost ops with ready status
    zero_ops = load_zero_cost_ops()
    ready_ops = [op for op in zero_ops if op.status == "ready"]
    not_started = [op for op in zero_ops if op.status == "not_started"]
    if ready_ops:
        top_rev = sorted(ready_ops, key=lambda o: o.revenue_potential_high, reverse=True)[:3]
        for op in top_rev:
            recs.append(RecommendedAction(
                priority="HIGH",
                category="ZERO_COST",
                action=f"Launch {op.category} (READY, ${op.revenue_potential_low}-${op.revenue_potential_high}/mo)",
                reason=op.description[:60],
            ))

    if len(not_started) > 10:
        recs.append(RecommendedAction(
            priority="MEDIUM",
            category="ZERO_COST",
            action=f"{len(not_started)} zero-cost ops not started yet",
            reason="Activate highest-revenue ops first.",
        ))

    # 10. Account portfolio gaps
    accounts = load_accounts()
    needs_creation = [a for a in accounts if a.status == 'NEEDS_CREATION']
    blocking = [a for a in accounts if 'BLOCKING' in (a.notes or '')]
    if blocking:
        recs.append(RecommendedAction(
            priority="CRITICAL",
            category="ACCOUNTS",
            action=f"{len(blocking)} BLOCKING accounts need creation",
            reason=f"Revenue blocked. Platforms: {', '.join(set(a.platform for a in blocking[:5]))}",
        ))
    elif needs_creation:
        recs.append(RecommendedAction(
            priority="MEDIUM",
            category="ACCOUNTS",
            action=f"{len(needs_creation)} accounts need creation ({len(accounts)} total)",
            reason="Create accounts to unlock distribution channels.",
        ))

    # 11. LOW: Daily research cadence
    recs.append(RecommendedAction(
        priority="LOW",
        category="RESEARCH",
        action="Run daily research scan",
        reason="Alpha decays. Scan high-signal sources.",
        command="python3 AUTOMATIONS/twitter_alpha_scraper.py --all",
    ))

    return sorted(recs, key=lambda r: {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}.get(r.priority, 4))


# =============================================================================
# TUI APPLICATION
# =============================================================================

if HAS_TEXTUAL:

    class PrintmaxxQuantTerminal(App):
        """PRINTMAXX QUANT TERMINAL v4.0"""

        TITLE = "PRINTMAXX QUANT TERMINAL v4.0"
        SUB_TITLE = "Institutional Action Center"

        CSS = """
        Screen { background: #0a0a0a; }
        .panel {
            border: solid #333333;
            padding: 1;
            margin: 0 1;
            background: #1a1a1a;
        }
        Button { margin: 1 0; min-width: 30; }
        DataTable { height: 100%; }
        #main-grid {
            layout: grid;
            grid-size: 3 2;
            grid-gutter: 1;
            padding: 1;
        }
        """

        BINDINGS = [
            Binding("r", "refresh_all", "Refresh", show=True),
            Binding("e", "export_report", "Export", show=True),
            Binding("q", "quit", "Quit", show=True),
            Binding("1", "focus_tab('overview')", "Overview", show=False),
            Binding("2", "focus_tab('ventures')", "Ventures", show=False),
            Binding("3", "focus_tab('social')", "Social", show=False),
            Binding("4", "focus_tab('risk')", "Risk", show=False),
            Binding("5", "focus_tab('rbi')", "RBI/Ops", show=False),
        ]

        def __init__(self):
            super().__init__()
            self.alpha_entries: List[AlphaEntry] = []
            self.methods: List[MethodPerformance] = []
            self.investments: List[Investment] = []
            self.synergies: List[Synergy] = []
            self.growth_tactics: List[GrowthTactic] = []
            self.growth_services: List[GrowthService] = []
            self.recommendations: List[RecommendedAction] = []
            self.portfolio_risk: PortfolioRisk = PortfolioRisk()
            self.content_stats: Dict[str, int] = {}
            self.revenue_data: List[Dict] = []
            self.expense_data: List[Dict] = []
            self.rbi_scan: RBIScanResult = RBIScanResult()
            self.zero_cost_ops: List[ZeroCostOp] = []
            self.accounts: List[AccountStatus] = []
            self.social_setup: Dict[str, Any] = {}

        def compose(self) -> ComposeResult:
            yield Header(show_clock=True)

            with TabbedContent(initial="overview"):
                # TAB 1: OVERVIEW
                with TabPane("Overview", id="overview"):
                    with Grid(id="main-grid"):
                        with Container(classes="panel"):
                            yield Static("[bold cyan]QUICK ACTIONS[/]")
                            yield Button("Run Daily Research", id="btn-daily-research", variant="success")
                            yield Button("Run Overnight Loops", id="btn-overnight", variant="primary")
                            yield Button("Review Alpha", id="btn-review-alpha", variant="default")
                            yield Button("Export Report", id="btn-export", variant="default")
                            yield Button("Launch Ready Builds", id="btn-launch", variant="warning")

                        with Container(classes="panel"):
                            yield Static("[bold cyan]RECOMMENDATIONS[/]")
                            yield Static(id="recs-text")

                        with Container(classes="panel"):
                            yield Static("[bold cyan]ALPHA PIPELINE[/]")
                            yield DataTable(id="alpha-table")

                        with Container(classes="panel"):
                            yield Static("[bold cyan]ACTIVE INVESTMENTS[/]")
                            yield DataTable(id="investments-table")

                        with Container(classes="panel"):
                            yield Static("[bold cyan]PORTFOLIO SUMMARY[/]")
                            yield Static(id="portfolio-summary")

                        with Container(classes="panel"):
                            yield Static("[bold cyan]ALERTS[/]")
                            yield Static(id="alerts-text")

                # TAB 2: VENTURES
                with TabPane("Ventures", id="ventures"):
                    yield Static("[bold cyan]VENTURE PORTFOLIO - Tools / GTM / Launch Strategy[/]")
                    yield ScrollableContainer(Static(id="ventures-detail"))

                # TAB 3: SOCIAL GROWTH
                with TabPane("Social Growth", id="social"):
                    yield Static("[bold cyan]EDGE GROWTH TACTICS + SERVICES[/]")
                    yield DataTable(id="growth-table")
                    yield Static(id="services-text")

                # TAB 4: RISK
                with TabPane("Risk", id="risk"):
                    yield Static("[bold cyan]RISK MANAGEMENT - Institutional Grade[/]")
                    yield ScrollableContainer(Static(id="risk-detail"))

                # TAB 5: RBI / ZERO-COST OPS
                with TabPane("RBI / Ops", id="rbi"):
                    yield Static("[bold cyan]RBI SCANNER + ZERO-COST OPS DASHBOARD[/]")
                    yield ScrollableContainer(Static(id="rbi-detail"))

            yield Footer()

        async def on_mount(self) -> None:
            await self._load_all()
            self.set_interval(60.0, self._refresh)

        async def _load_all(self) -> None:
            self.alpha_entries = load_alpha_staging()
            self.methods = load_money_methods()
            self.investments = load_active_investments()
            self.synergies = load_synergies()
            self.growth_tactics = load_growth_tactics()
            self.growth_services = load_growth_services()
            self.revenue_data = load_revenue_data()
            self.expense_data = load_expense_data()
            self.content_stats = load_content_pipeline_stats()
            self.rbi_scan = load_rbi_scan()
            self.zero_cost_ops = load_zero_cost_ops()
            self.accounts = load_accounts()
            self.social_setup = load_social_setup_outputs()
            self.portfolio_risk = calculate_portfolio_risk(
                self.methods, self.investments, self.revenue_data, self.expense_data
            )
            self.recommendations = generate_recommendations(
                self.methods, self.alpha_entries, self.investments,
                self.synergies, self.portfolio_risk, self.content_stats,
            )
            self._populate_all()

        def _populate_all(self) -> None:
            self._populate_alpha_table()
            self._populate_investments_table()
            self._populate_portfolio_summary()
            self._populate_alerts()
            self._populate_recommendations()
            self._populate_ventures()
            self._populate_growth()
            self._populate_risk()
            self._populate_rbi()

        def _populate_alpha_table(self) -> None:
            try:
                t = self.query_one("#alpha-table", DataTable)
                t.clear(columns=True)
                t.add_columns("ID", "Category", "ROI", "Days", "Status")
                pending = [a for a in self.alpha_entries if a.status == 'PENDING_REVIEW']
                for e in pending[:12]:
                    age_style = "red" if e.days_since_discovery > 30 else "yellow" if e.days_since_discovery > 14 else "green"
                    t.add_row(
                        e.alpha_id, e.category[:15], e.roi_potential,
                        Text(str(e.days_since_discovery), style=age_style),
                        e.status[:12],
                    )
            except Exception:
                pass

        def _populate_investments_table(self) -> None:
            try:
                t = self.query_one("#investments-table", DataTable)
                t.clear(columns=True)
                t.add_columns("ID", "Name", "Capital", "Priority", "Next Action")
                for inv in self.investments:
                    pri_style = "red bold" if inv.priority == "CRITICAL" else "yellow" if inv.priority == "HIGH" else "dim"
                    t.add_row(
                        inv.investment_id,
                        inv.name[:18],
                        f"${inv.capital_allocated:.0f}",
                        Text(inv.priority, style=pri_style),
                        inv.next_action[:25],
                    )
            except Exception:
                pass

        def _populate_portfolio_summary(self) -> None:
            try:
                s = self.query_one("#portfolio-summary", Static)
                r = self.portfolio_risk
                active = len([m for m in self.methods if m.status in ('Active', 'ACTIVE')])
                planning = len([m for m in self.methods if m.status == 'Planning'])
                pending_alpha = len([a for a in self.alpha_entries if a.status == 'PENDING_REVIEW'])
                total_capital = sum(i.capital_allocated for i in self.investments)

                accounts_created = len([a for a in self.accounts if a.status not in ('NEEDS_CREATION', '')])
                accounts_total = len(self.accounts)
                ready_ops = len([o for o in self.zero_cost_ops if o.status == "ready"])
                total_ops = len(self.zero_cost_ops)

                text = f"""[bold]Methods:[/] {active} active / {planning} planning / {len(self.methods)} total
[bold]Investments:[/] {len(self.investments)} active, ${total_capital:.0f} deployed
[bold]Alpha:[/] {len(self.alpha_entries)} total, {pending_alpha} pending
[bold]Content:[/] {self.content_stats.get('total', 0)} pieces ({self.content_stats.get('queued', 0)} queued)
[bold]Revenue:[/] [green]${r.total_revenue:.0f}[/] (${r.net_profit:.0f} net)
[bold]Expenses:[/] [red]${r.total_expenses:.0f}[/]
[bold]Synergies:[/] {len(self.synergies)} pairs loaded
[bold]Accounts:[/] {accounts_created}/{accounts_total} created
[bold]Zero-Cost Ops:[/] {ready_ops}/{total_ops} ready to launch"""
                s.update(text)
            except Exception:
                pass

        def _populate_alerts(self) -> None:
            try:
                s = self.query_one("#alerts-text", Static)
                alerts = []
                pending = len([a for a in self.alpha_entries if a.status == 'PENDING_REVIEW'])
                if pending > 50:
                    alerts.append(f"[yellow]WARN:[/] {pending} alpha pending review (decay risk)")
                active = len([m for m in self.methods if m.status in ('Active', 'ACTIVE')])
                if active == 0:
                    alerts.append("[red]CRIT:[/] 0 methods active. Execution gap.")
                critical_inv = [i for i in self.investments if i.priority == 'CRITICAL' and i.status == 'READY']
                if critical_inv:
                    alerts.append(f"[red]CRIT:[/] {len(critical_inv)} CRITICAL investments READY to execute")
                if self.content_stats.get('queued', 0) > 100 and self.content_stats.get('published', 0) == 0:
                    alerts.append(f"[yellow]WARN:[/] {self.content_stats['queued']} content queued, 0 published")
                r = self.portfolio_risk
                if r.concentration_hhi > 5000:
                    alerts.append(f"[yellow]WARN:[/] Revenue concentration HHI {r.concentration_hhi:.0f}")
                if r.max_drawdown > RISK_THRESHOLDS["max_drawdown"]:
                    alerts.append(f"[red]CRIT:[/] Max drawdown {r.max_drawdown:.1%}")
                # Account alerts
                blocking_accs = [a for a in self.accounts if 'BLOCKING' in (a.notes or '')]
                if blocking_accs:
                    alerts.append(f"[red]CRIT:[/] {len(blocking_accs)} BLOCKING accounts need creation (revenue blocked)")
                needs_creation = [a for a in self.accounts if a.status == 'NEEDS_CREATION']
                if len(needs_creation) > 20:
                    alerts.append(f"[yellow]WARN:[/] {len(needs_creation)} accounts still need creation")
                # Zero-cost ops alerts
                ready_ops = [o for o in self.zero_cost_ops if o.status == "ready"]
                if ready_ops:
                    total_rev = sum(o.revenue_potential_high for o in ready_ops)
                    alerts.append(f"[yellow]WARN:[/] {len(ready_ops)} zero-cost ops READY but not launched (${total_rev:,.0f}/mo potential)")
                s.update("\n".join(alerts) if alerts else "[green]All systems nominal[/]")
            except Exception:
                pass

        def _populate_recommendations(self) -> None:
            try:
                s = self.query_one("#recs-text", Static)
                lines = []
                colors = {"CRITICAL": "red bold", "HIGH": "yellow bold", "MEDIUM": "blue", "LOW": "dim"}
                icons = {"CRITICAL": "!!", "HIGH": ">>", "MEDIUM": "--", "LOW": ".."}
                for rec in self.recommendations[:8]:
                    c = colors.get(rec.priority, "white")
                    i = icons.get(rec.priority, "-")
                    lines.append(f"[{c}]{i} {rec.action}[/]")
                    lines.append(f"   [dim]{rec.reason[:60]}[/]")
                    if rec.command:
                        lines.append(f"   [dim cyan]> {rec.command}[/]")
                s.update("\n".join(lines) if lines else "[dim]No recommendations[/]")
            except Exception:
                pass

        def _populate_ventures(self) -> None:
            try:
                s = self.query_one("#ventures-detail", Static)
                lines = []
                # Sort: Active first, then by priority
                sorted_methods = sorted(self.methods, key=lambda m: (
                    0 if m.status in ('Active', 'ACTIVE') else 1 if m.status == 'Planning' else 2,
                    m.method_id
                ))
                # Find synergies for each method
                syn_map = {}
                for syn in self.synergies:
                    syn_map.setdefault(syn.method_1, []).append(syn)
                    syn_map.setdefault(syn.method_2, []).append(syn)

                for method in sorted_methods[:30]:
                    sc = "green" if method.status in ('Active', 'ACTIVE') else "yellow" if method.status == 'Planning' else "dim"
                    lines.append(f"\n[bold {sc}]{'=' * 70}[/]")
                    lines.append(f"[bold cyan]{method.method_id}[/] - [bold]{method.method_name}[/]  [{sc}]{method.status}[/]  {method.category}")
                    lines.append(f"[bold]Revenue Model:[/] {method.revenue_model}")
                    lines.append(f"[bold]Tools:[/] {', '.join(method.tools_used)}")
                    lines.append(f"[bold]GTM Channels:[/] {', '.join(method.gtm_channels)}")
                    lines.append(f"[bold]Launch Strategy:[/] {method.launch_strategy}")

                    # Show investment data if exists
                    inv = next((i for i in self.investments if i.method_id == method.method_id), None)
                    if inv:
                        lines.append(f"[bold green]Investment:[/] {inv.investment_id} | ${inv.capital_allocated:.0f} allocated | {inv.priority}")
                        lines.append(f"  Next: {inv.next_action}")
                        if inv.notes:
                            lines.append(f"  [dim]{inv.notes[:80]}[/]")

                    # Show top synergies
                    method_syns = syn_map.get(method.method_id, [])[:3]
                    if method_syns:
                        lines.append(f"[bold purple]Synergies:[/]")
                        for syn in method_syns:
                            partner = syn.method_2 if syn.method_1 == method.method_id else syn.method_1
                            lines.append(f"  + {partner} (score:{syn.synergy_score}, {syn.revenue_multiplier}x)")

                    if method.notes:
                        lines.append(f"[dim]Notes: {method.notes[:100]}[/]")

                s.update("\n".join(lines))
            except Exception:
                pass

        def _populate_growth(self) -> None:
            try:
                # Growth tactics table
                t = self.query_one("#growth-table", DataTable)
                t.clear(columns=True)
                t.add_columns("Platform", "Tactic", "Risk", "Limit", "Status", "Notes")
                working = [g for g in self.growth_tactics if g.status == "WORKING"]
                for g in working:
                    rc = "green" if g.risk_level == "SAFE" else "yellow" if g.risk_level == "GREY" else "red"
                    t.add_row(
                        g.platform, g.tactic_name,
                        Text(g.risk_level, style=rc),
                        g.daily_limit, Text(g.status, style="green"),
                        g.notes[:40],
                    )
                # Add PATCHED items
                patched = [g for g in self.growth_tactics if g.status == "PATCHED"]
                for g in patched:
                    t.add_row(
                        g.platform, g.tactic_name,
                        Text("DEAD", style="red"), "N/A",
                        Text("PATCHED", style="red"),
                        g.notes[:40],
                    )

                # Services comparison
                s = self.query_one("#services-text", Static)
                lines = ["\n[bold cyan]SERVICES COMPARISON (Real Pricing)[/]\n"]
                by_platform = {}
                for svc in self.growth_services:
                    by_platform.setdefault(svc.platform, []).append(svc)
                for platform, svcs in by_platform.items():
                    lines.append(f"[bold]{platform}:[/]")
                    for svc in svcs:
                        safety_c = "green" if svc.safety == "HIGHEST" else "cyan" if svc.safety == "HIGH" else "yellow"
                        lines.append(f"  [{safety_c}]{svc.service_name}[/] {svc.cost} - {svc.method} [{safety_c}]{svc.safety}[/] ({svc.notes})")
                    lines.append("")

                lines.append("[bold]KEY 2026 CHANGES:[/]")
                lines.append("  - Chrome extensions DEAD on ALL platforms")
                lines.append("  - TikTok: NO automation. Manual + real phone only.")
                lines.append("  - Instagram: Mobile proxies REQUIRED (residential flagged)")
                lines.append("  - Email: 30/day/inbox new safe limit (down from 50)")
                lines.append("  - LinkedIn: Cloud-only automation (Expandi/Dripify)")
                lines.append(f"\n[dim]Source: 06_OPERATIONS/growth/EDGE_GROWTH_TACTICS.md (670 lines)[/]")
                s.update("\n".join(lines))
            except Exception:
                pass

        def _populate_risk(self) -> None:
            try:
                s = self.query_one("#risk-detail", Static)
                r = self.portfolio_risk
                lines = []

                lines.append("[bold cyan]PORTFOLIO RISK METRICS[/]")
                lines.append(f"{'=' * 60}\n")

                # Returns
                lines.append("[bold]Returns & Ratios[/]")
                sharpe_c = "green" if r.portfolio_sharpe >= 2.0 else "yellow" if r.portfolio_sharpe >= 1.0 else "red"
                lines.append(f"  Sharpe Ratio:  [{sharpe_c}]{r.portfolio_sharpe:.3f}[/] (>{RISK_THRESHOLDS['sharpe_good']} good)")
                lines.append(f"  Sortino Ratio: [{sharpe_c}]{r.portfolio_sortino:.3f}[/]")
                lines.append(f"  Sharpe 95% CI: [{sharpe_c}]{r.sharpe_confidence_interval}[/] (Lo 2002)")
                lines.append(f"  Data months:   {r.sharpe_data_months}")
                if r.sharpe_data_months < 6:
                    lines.append(f"  [yellow]WARNING: <6 months data. Sharpe unreliable.[/]")
                lines.append("")

                # VaR
                lines.append("[bold]Value at Risk (VaR)[/]")
                lines.append(f"  Parametric VaR 95%:  ${r.var_95:,.2f}")
                lines.append(f"  Parametric VaR 99%:  ${r.var_99:,.2f}")
                lines.append(f"  Historical VaR 95%:  ${r.var_95_historical:,.2f}")
                lines.append(f"  Historical VaR 99%:  ${r.var_99_historical:,.2f}")
                lines.append(f"  CVaR (ES) 95%:       ${r.cvar_95:,.2f}")
                lines.append(f"  CVaR (ES) 99%:       ${r.cvar_99:,.2f}")
                lines.append("")

                # Drawdown
                dd_c = "red" if r.max_drawdown > 0.15 else "yellow" if r.max_drawdown > 0.05 else "green"
                lines.append("[bold]Drawdown Analysis[/]")
                lines.append(f"  Max Drawdown:     [{dd_c}]{r.max_drawdown:.1%}[/] (<{RISK_THRESHOLDS['max_drawdown']:.0%} target)")
                lines.append(f"  Current Drawdown: [{dd_c}]{r.current_drawdown:.1%}[/]")
                lines.append(f"  Duration:         {r.drawdown_duration} periods")
                lines.append("")

                # Concentration
                hhi_c = "red" if r.concentration_hhi > 5000 else "yellow" if r.concentration_hhi > 3000 else "green"
                lines.append("[bold]Concentration Risk[/]")
                lines.append(f"  Method HHI:       [{hhi_c}]{r.concentration_hhi:.0f}[/] (<3000 diversified, >5000 concentrated)")
                lines.append(f"  Max single method: {r.concentration_method_max:.1%}")
                lines.append(f"  Platform HHI:     {r.concentration_platform_hhi:.0f}")
                lines.append("")

                # Beta & IC
                lines.append("[bold]Factor Analysis[/]")
                lines.append(f"  Beta:             {r.beta:.3f} ({r.beta_confidence})")
                lines.append(f"  Info Coefficient: {r.information_coefficient:.3f}")
                lines.append(f"  IC Hit Rate:      {r.ic_hit_rate:.1%}")
                lines.append(f"  IC Sample Size:   {r.ic_sample_size}")
                lines.append("")

                # Capital
                lines.append("[bold]Capital Deployment[/]")
                lines.append(f"  Total Deployed:   ${r.capital_deployed:,.0f}")
                lines.append(f"  Capital at Risk:  ${r.capital_at_risk:,.0f}")
                lines.append(f"  Total Revenue:    ${r.total_revenue:,.0f}")
                lines.append(f"  Total Expenses:   ${r.total_expenses:,.0f}")
                lines.append(f"  Net P&L:          ${r.net_profit:,.0f}")
                lines.append("")

                # Circuit breakers
                lines.append("[bold red]CIRCUIT BREAKERS[/]")
                breakers = []
                if r.max_drawdown > 0.25:
                    breakers.append("[red]TRIGGERED: Max drawdown >25%. HALT new investments.[/]")
                if r.concentration_hhi > 7500:
                    breakers.append("[red]TRIGGERED: Extreme concentration (HHI >7500). Diversify immediately.[/]")
                if r.portfolio_sharpe < 0 and r.sharpe_data_months >= 6:
                    breakers.append("[red]TRIGGERED: Negative Sharpe with 6+ months data. Review all methods.[/]")
                if not breakers:
                    breakers.append("[green]No circuit breakers triggered.[/]")
                for b in breakers:
                    lines.append(f"  {b}")

                s.update("\n".join(lines))
            except Exception:
                pass

        def _populate_rbi(self) -> None:
            try:
                s = self.query_one("#rbi-detail", Static)
                lines = []
                rbi = self.rbi_scan
                ops = self.zero_cost_ops
                accounts = self.accounts

                # ================ RBI SCANNER STATUS ================
                lines.append("[bold cyan]RBI SCANNER STATUS[/]")
                lines.append(f"{'=' * 65}\n")

                if rbi.scan_date:
                    lines.append(f"[bold]Last Scan:[/]  {rbi.scan_date}")
                    lines.append(f"[bold]Alpha:[/]      {rbi.total_alpha} total | {rbi.pending_alpha} pending | {rbi.high_roi_pending} HIGH/HIGHEST ROI")
                    lines.append(f"[bold]Methods:[/]    {rbi.active_methods} active / {rbi.total_methods} total")
                    lines.append(f"[bold]Content:[/]    {rbi.content_total} pieces | {rbi.content_queued} queued")
                else:
                    lines.append("[yellow]No RBI scan found. Run: python3 scripts/rbi_audit.py full[/]")

                # ROI distribution
                if rbi.roi_distribution:
                    lines.append(f"\n[bold]ROI Distribution:[/]")
                    for roi, count in sorted(rbi.roi_distribution.items(), key=lambda x: x[1], reverse=True):
                        bar_len = min(count, 40)
                        bar = "=" * bar_len
                        c = "green" if roi == "HIGHEST" else "cyan" if roi == "HIGH" else "yellow"
                        lines.append(f"  [{c}]{roi:10s}[/] [{c}]{bar}[/] {count}")

                # Category breakdown
                if rbi.top_categories:
                    lines.append(f"\n[bold]Alpha by Category:[/]")
                    for cat, count in sorted(rbi.top_categories.items(), key=lambda x: x[1], reverse=True)[:8]:
                        bar_len = min(count, 30)
                        bar = "=" * bar_len
                        lines.append(f"  {cat:20s} {bar} {count}")

                # ================ ACCOUNT PORTFOLIO ================
                lines.append(f"\n\n[bold cyan]ACCOUNT PORTFOLIO ({len(accounts)} accounts)[/]")
                lines.append(f"{'=' * 65}\n")

                if accounts:
                    by_status = {}
                    for acc in accounts:
                        by_status.setdefault(acc.status, []).append(acc)

                    for status in ['PENDING', 'NEEDS_CREATION', 'ACTIVE']:
                        accs = by_status.get(status, [])
                        if accs:
                            sc = "yellow" if status == 'PENDING' else "red" if status == 'NEEDS_CREATION' else "green"
                            lines.append(f"[{sc}]{status}[/] ({len(accs)}):")
                            by_niche = {}
                            for acc in accs:
                                by_niche.setdefault(acc.niche, []).append(acc)
                            for niche, niche_accs in sorted(by_niche.items()):
                                platforms = ", ".join(a.platform for a in niche_accs)
                                blocking = any('BLOCKING' in (a.notes or '') for a in niche_accs)
                                flag = " [red bold]BLOCKING[/]" if blocking else ""
                                lines.append(f"  {niche:12s} {platforms}{flag}")
                            lines.append("")

                # ================ ZERO-COST OPS DASHBOARD ================
                lines.append(f"\n[bold cyan]ZERO-COST OPS DASHBOARD (17 categories)[/]")
                lines.append(f"{'=' * 65}\n")

                active_ops = [o for o in ops if o.status == "active"]
                ready_ops = [o for o in ops if o.status == "ready"]
                not_started_ops = [o for o in ops if o.status == "not_started"]

                lines.append(f"[green]ACTIVE: {len(active_ops)}[/]  |  [yellow]READY: {len(ready_ops)}[/]  |  [red]NOT STARTED: {len(not_started_ops)}[/]\n")

                for op in sorted(ops, key=lambda o: ({"active": 0, "ready": 1, "not_started": 2}.get(o.status, 3), -o.revenue_potential_high)):
                    sc = "green" if op.status == "active" else "yellow" if op.status == "ready" else "dim"
                    status_icon = "[green]LIVE[/]" if op.status == "active" else "[yellow]READY[/]" if op.status == "ready" else "[dim]IDLE[/]"
                    rev_str = f"${op.revenue_potential_low:,.0f}-${op.revenue_potential_high:,.0f}/mo" if op.revenue_potential_high > 0 else "Growth op"
                    lines.append(f"  {status_icon} [{sc}]{op.category:20s}[/]  {rev_str:22s}  {op.description[:40]}")

                # ================ REVENUE PIPELINE ================
                lines.append(f"\n\n[bold cyan]REVENUE PIPELINE PROJECTIONS[/]")
                lines.append(f"{'=' * 65}\n")

                # Calculate projections based on zero-cost ops
                rev_30_low = sum(op.revenue_potential_low * 0.15 for op in ops if op.status in ("active", "ready"))
                rev_30_high = sum(op.revenue_potential_high * 0.08 for op in ops if op.status in ("active", "ready"))
                rev_60_low = sum(op.revenue_potential_low * 0.35 for op in ops if op.status in ("active", "ready"))
                rev_60_high = sum(op.revenue_potential_high * 0.18 for op in ops if op.status in ("active", "ready"))
                rev_90_low = sum(op.revenue_potential_low * 0.55 for op in ops if op.status in ("active", "ready"))
                rev_90_high = sum(op.revenue_potential_high * 0.30 for op in ops if op.status in ("active", "ready"))

                lines.append(f"  [bold]30 DAY:[/]  [green]${rev_30_low:>8,.0f} - ${rev_30_high:>8,.0f}[/]  (conservative - aggressive)")
                lines.append(f"  [bold]60 DAY:[/]  [green]${rev_60_low:>8,.0f} - ${rev_60_high:>8,.0f}[/]  (ramp-up phase)")
                lines.append(f"  [bold]90 DAY:[/]  [green]${rev_90_low:>8,.0f} - ${rev_90_high:>8,.0f}[/]  (compounding)")

                lines.append(f"\n  [dim]Projections assume 15%/35%/55% of low-end realized for conservative,")
                lines.append(f"  8%/18%/30% of high-end for aggressive. Based on {len(ready_ops)} ready + {len(active_ops)} active ops.[/]")

                # ================ NEXT ACTIONS ================
                lines.append(f"\n\n[bold cyan]TOP 10 NEXT ACTIONS[/]")
                lines.append(f"{'=' * 65}\n")

                actions = []

                # Blocking accounts first
                blocking_accs = [a for a in accounts if 'BLOCKING' in (a.notes or '')]
                for acc in blocking_accs[:3]:
                    actions.append(("CRITICAL", f"Create {acc.platform} account ({acc.niche})", acc.notes or "Revenue blocked"))

                # Ready zero-cost ops
                top_ready = sorted(ready_ops, key=lambda o: o.revenue_potential_high, reverse=True)
                for op in top_ready[:4]:
                    actions.append(("HIGH", f"Launch {op.category}", f"${op.revenue_potential_low}-${op.revenue_potential_high}/mo potential"))

                # RBI recommendations
                for rec in rbi.recommendations[:2]:
                    actions.append(("MEDIUM", rec[:60], "From RBI scanner"))

                # Not started high-rev ops
                top_not_started = sorted(not_started_ops, key=lambda o: o.revenue_potential_high, reverse=True)
                for op in top_not_started[:2]:
                    actions.append(("LOW", f"Setup {op.category}", f"${op.revenue_potential_low}-${op.revenue_potential_high}/mo when active"))

                for i, (priority, action, reason) in enumerate(actions[:10], 1):
                    pc = "red bold" if priority == "CRITICAL" else "yellow bold" if priority == "HIGH" else "blue" if priority == "MEDIUM" else "dim"
                    lines.append(f"  [{pc}]{i:2d}. [{priority:8s}][/] {action}")
                    lines.append(f"      [dim]{reason}[/]")

                # ================ SOCIAL SETUP STATUS ================
                ss = self.social_setup
                if ss.get("total_files", 0) > 0:
                    lines.append(f"\n\n[bold cyan]SOCIAL SETUP LOOP STATUS ({ss['total_files']} outputs)[/]")
                    lines.append(f"{'=' * 65}\n")

                    checks = [
                        ("Bios ready", ss.get("bios_ready", False)),
                        ("Image prompts ready", ss.get("image_prompts_ready", False)),
                        ("Content ready", ss.get("content_ready", False)),
                        (f"Newsletters ready ({ss.get('newsletters_ready', 0)})", ss.get("newsletters_ready", 0) > 0),
                        ("Warmup schedule", ss.get("warmup_schedule", False)),
                        ("Posting schedule", ss.get("posting_schedule", False)),
                        ("Accounts updated", ss.get("accounts_updated", False)),
                        ("Ecom launch plan", ss.get("ecom_plan", False)),
                        ("Meme strategy", ss.get("meme_strategy", False)),
                        ("Cross-promo plan", ss.get("cross_promo", False)),
                        ("67-ops audit", ss.get("audit_complete", False)),
                    ]

                    for label, done in checks:
                        icon = "[green]DONE[/]" if done else "[red]TODO[/]"
                        lines.append(f"  {icon} {label}")

                # ================ MASTER OPS BUILD STATUS ================
                if MASTER_OPS_OUTPUT.exists():
                    master_files = [f.name for f in MASTER_OPS_OUTPUT.iterdir() if f.is_file()]
                    if master_files:
                        lines.append(f"\n\n[bold cyan]MASTER OPS BUILD ({len(master_files)} outputs)[/]")
                        lines.append(f"{'=' * 65}\n")
                        for fname in sorted(master_files):
                            lines.append(f"  [green]OK[/] {fname}")

                if MASTER_OPS_XLSX.exists():
                    import os as _os
                    size = _os.path.getsize(MASTER_OPS_XLSX)
                    lines.append(f"\n  [green]MASTER OPS SPREADSHEET:[/] PRINTMAXX_MASTER_OPS.xlsx ({size // 1024}KB)")

                # Quick commands
                lines.append(f"\n\n[bold]QUICK COMMANDS[/]")
                lines.append(f"  python3 scripts/rbi_audit.py full              # Run full RBI audit")
                lines.append(f"  python3 AUTOMATIONS/printmaxx_quant_terminal.py --rbi  # This panel only")
                lines.append(f"  /review-alpha                                   # Review pending alpha")

                s.update("\n".join(lines))
            except Exception:
                pass

        def on_button_pressed(self, event: Button.Pressed) -> None:
            """Handle button presses (standard Textual pattern)"""
            bid = event.button.id
            if bid == "btn-daily-research":
                self.notify("Running daily research...")
                try:
                    subprocess.Popen(
                        ["python3", str(AUTOMATIONS_DIR / "twitter_alpha_scraper.py"), "--all"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    )
                    self.notify("Daily research started in background")
                except Exception as e:
                    self.notify(f"Error: {e}", severity="error")

            elif bid == "btn-overnight":
                self.notify("Launching overnight ralph loops...")
                try:
                    subprocess.Popen(
                        ["bash", str(PROJECT_ROOT / "ralph" / "run_all_loops.sh")],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    )
                    self.notify("Overnight loops started")
                except Exception as e:
                    self.notify(f"Error: {e}", severity="error")

            elif bid == "btn-review-alpha":
                self.notify("Run /review-alpha in Claude to review pending alpha")

            elif bid == "btn-export":
                self._export_report()

            elif bid == "btn-launch":
                ready = [i for i in self.investments if i.status == 'READY']
                if ready:
                    self.notify(f"{len(ready)} investments READY. Check Ventures tab for next actions.")
                else:
                    self.notify("No investments in READY status")

        def _export_report(self) -> None:
            path = OPS_DIR / f"QUANT_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            lines = [
                f"# PRINTMAXX Quant Report",
                f"Generated: {datetime.now().isoformat()}\n",
                "## Portfolio",
                f"- Methods: {self.portfolio_risk.active_method_count} active / {self.portfolio_risk.total_method_count} total",
                f"- Capital Deployed: ${self.portfolio_risk.capital_deployed:,.0f}",
                f"- Revenue: ${self.portfolio_risk.total_revenue:,.0f}",
                f"- Net P&L: ${self.portfolio_risk.net_profit:,.0f}\n",
                "## Risk",
                f"- Sharpe: {self.portfolio_risk.portfolio_sharpe:.3f}",
                f"- Max Drawdown: {self.portfolio_risk.max_drawdown:.1%}",
                f"- Concentration HHI: {self.portfolio_risk.concentration_hhi:.0f}\n",
                "## Investments",
            ]
            for inv in self.investments:
                lines.append(f"- [{inv.priority}] {inv.name}: ${inv.capital_allocated:.0f} - {inv.next_action}")
            lines.append("\n## Recommendations")
            for rec in self.recommendations:
                lines.append(f"- [{rec.priority}] {rec.action}: {rec.reason}")
            path.write_text("\n".join(lines))
            self.notify(f"Report: {path.name}")

        async def _refresh(self) -> None:
            await self._load_all()

        async def action_refresh_all(self) -> None:
            self.notify("Refreshing...")
            await self._load_all()

        def action_focus_tab(self, tab: str) -> None:
            try:
                self.query_one(TabbedContent).active = tab
            except Exception:
                pass

        async def action_export_report(self) -> None:
            self._export_report()


# =============================================================================
# SUMMARY MODE (Comprehensive CLI output)
# =============================================================================

def print_summary():
    """Print comprehensive system summary without launching TUI"""
    console = Console()
    console.print()
    console.print("[bold cyan]PRINTMAXX QUANT TERMINAL v4.0 - SYSTEM SUMMARY[/]")
    console.print(f"[dim]{datetime.now().strftime('%Y-%m-%d %H:%M')}[/]")
    console.print("=" * 70)

    # Load all data
    methods = load_money_methods()
    alpha = load_alpha_staging()
    investments = load_active_investments()
    synergies = load_synergies()
    revenue_data = load_revenue_data()
    expense_data = load_expense_data()
    content_stats = load_content_pipeline_stats()
    risk = calculate_portfolio_risk(methods, investments, revenue_data, expense_data)
    recs = generate_recommendations(methods, alpha, investments, synergies, risk, content_stats)

    # SECTION 1: Portfolio overview
    console.print("\n[bold]PORTFOLIO[/]")
    active = [m for m in methods if m.status in ('Active', 'ACTIVE')]
    planning = [m for m in methods if m.status == 'Planning']
    console.print(f"  Methods: {len(active)} active / {len(planning)} planning / {len(methods)} total")
    console.print(f"  Capital Deployed: ${risk.capital_deployed:,.0f}")
    console.print(f"  Revenue: ${risk.total_revenue:,.0f} | Expenses: ${risk.total_expenses:,.0f} | Net: ${risk.net_profit:,.0f}")

    # SECTION 2: Active investments
    console.print(f"\n[bold]ACTIVE INVESTMENTS ({len(investments)})[/]")
    for inv in investments:
        pri_c = "red" if inv.priority == "CRITICAL" else "yellow" if inv.priority == "HIGH" else "cyan"
        console.print(f"  [{pri_c}]{inv.priority:8s}[/] {inv.investment_id} {inv.name[:25]:25s} ${inv.capital_allocated:>6.0f}  {inv.status:8s}  {inv.next_action[:35]}")

    # SECTION 3: Alpha
    pending = [a for a in alpha if a.status == 'PENDING_REVIEW']
    approved = [a for a in alpha if a.status == 'APPROVED']
    console.print(f"\n[bold]ALPHA[/]")
    console.print(f"  Total: {len(alpha)} | Pending: {len(pending)} | Approved: {len(approved)}")
    if pending:
        decaying = [a for a in pending if a.days_since_discovery > 30]
        console.print(f"  Decaying (>30d): {len(decaying)}")
        by_cat = {}
        for a in pending[:200]:
            by_cat[a.category] = by_cat.get(a.category, 0) + 1
        top_cats = sorted(by_cat.items(), key=lambda x: x[1], reverse=True)[:5]
        if top_cats:
            console.print(f"  Top categories: {', '.join(f'{c}({n})' for c, n in top_cats)}")

    # SECTION 4: Content
    console.print(f"\n[bold]CONTENT[/]")
    console.print(f"  Total: {content_stats.get('total', 0)} | Queued: {content_stats.get('queued', 0)} | Published: {content_stats.get('published', 0)}")

    # SECTION 5: Risk
    console.print(f"\n[bold]RISK METRICS[/]")
    console.print(f"  Sharpe: {risk.portfolio_sharpe:.3f} | Sortino: {risk.portfolio_sortino:.3f}")
    console.print(f"  VaR 95%: ${risk.var_95:,.2f} | CVaR 95%: ${risk.cvar_95:,.2f}")
    console.print(f"  Max Drawdown: {risk.max_drawdown:.1%} | HHI: {risk.concentration_hhi:.0f}")
    if risk.sharpe_data_months < 6:
        console.print(f"  [yellow]Note: {risk.sharpe_data_months} months data. Need 6+ for reliable metrics.[/]")

    # SECTION 6: Top synergies
    top_syns = sorted(synergies, key=lambda s: s.synergy_score, reverse=True)[:5]
    if top_syns:
        console.print(f"\n[bold]TOP SYNERGIES[/]")
        for syn in top_syns:
            console.print(f"  {syn.method_1} + {syn.method_2}: score {syn.synergy_score}, {syn.revenue_multiplier}x multiplier")

    # SECTION 7: Recommendations
    console.print(f"\n[bold]RECOMMENDATIONS ({len(recs)})[/]")
    icons = {"CRITICAL": "[red]!![/]", "HIGH": "[yellow]>>[/]", "MEDIUM": "[blue]--[/]", "LOW": "[dim]..[/]"}
    for rec in recs[:10]:
        icon = icons.get(rec.priority, "-")
        console.print(f"  {icon} [{rec.priority:8s}] {rec.action}")
        if rec.command:
            console.print(f"     [dim cyan]> {rec.command}[/]")

    # SECTION 8: RBI Scanner Status
    rbi = load_rbi_scan()
    if rbi.scan_date:
        console.print(f"\n[bold]RBI SCANNER[/]")
        console.print(f"  Last scan: {rbi.scan_date}")
        console.print(f"  Alpha: {rbi.total_alpha} total | {rbi.pending_alpha} pending | {rbi.high_roi_pending} HIGH/HIGHEST ROI")
        console.print(f"  Methods: {rbi.active_methods} active / {rbi.total_methods} total")
        if rbi.recommendations:
            for rec_text in rbi.recommendations[:3]:
                console.print(f"  [yellow]>> {rec_text}[/]")

    # SECTION 9: Zero-Cost Ops Status
    zero_ops = load_zero_cost_ops()
    active_ops = [o for o in zero_ops if o.status == "active"]
    ready_ops = [o for o in zero_ops if o.status == "ready"]
    not_started_ops = [o for o in zero_ops if o.status == "not_started"]

    console.print(f"\n[bold]ZERO-COST OPS ({len(zero_ops)} categories)[/]")
    console.print(f"  [green]Active: {len(active_ops)}[/] | [yellow]Ready: {len(ready_ops)}[/] | [dim]Not started: {len(not_started_ops)}[/]")

    if ready_ops:
        top_ready = sorted(ready_ops, key=lambda o: o.revenue_potential_high, reverse=True)[:5]
        console.print(f"  [yellow]Ready to launch:[/]")
        for op in top_ready:
            rev = f"${op.revenue_potential_low:,.0f}-${op.revenue_potential_high:,.0f}/mo" if op.revenue_potential_high > 0 else "Growth op"
            console.print(f"    {op.category:20s} {rev}")

    # Revenue projections
    rev_30_low = sum(op.revenue_potential_low * 0.15 for op in zero_ops if op.status in ("active", "ready"))
    rev_30_high = sum(op.revenue_potential_high * 0.08 for op in zero_ops if op.status in ("active", "ready"))
    rev_90_low = sum(op.revenue_potential_low * 0.55 for op in zero_ops if op.status in ("active", "ready"))
    rev_90_high = sum(op.revenue_potential_high * 0.30 for op in zero_ops if op.status in ("active", "ready"))
    console.print(f"\n  [bold]Revenue Pipeline:[/]")
    console.print(f"    30-day: ${rev_30_low:,.0f} - ${rev_30_high:,.0f}")
    console.print(f"    90-day: ${rev_90_low:,.0f} - ${rev_90_high:,.0f}")

    # SECTION 10: Account Portfolio
    accounts = load_accounts()
    if accounts:
        created = len([a for a in accounts if a.status not in ('NEEDS_CREATION', '')])
        needs = len([a for a in accounts if a.status == 'NEEDS_CREATION'])
        blocking = len([a for a in accounts if 'BLOCKING' in (a.notes or '')])
        console.print(f"\n[bold]ACCOUNTS ({len(accounts)} total)[/]")
        console.print(f"  Created/Pending: {created} | Needs creation: {needs}")
        if blocking:
            console.print(f"  [red]BLOCKING: {blocking} accounts blocking revenue[/]")

    # SECTION 11: Social Setup Loop
    ss = load_social_setup_outputs()
    if ss.get("total_files", 0) > 0:
        console.print(f"\n[bold]SOCIAL SETUP LOOP ({ss['total_files']} outputs)[/]")
        done_count = sum(1 for v in [ss.get("bios_ready"), ss.get("content_ready"), ss.get("warmup_schedule"),
                                      ss.get("posting_schedule"), ss.get("ecom_plan"), ss.get("meme_strategy"),
                                      ss.get("audit_complete")] if v)
        console.print(f"  Milestones: {done_count}/7 complete")

    # SECTION 12: Quick commands
    console.print(f"\n[bold]QUICK COMMANDS[/]")
    console.print("  python3 AUTOMATIONS/printmaxx_quant_terminal.py           # Launch full TUI")
    console.print("  python3 AUTOMATIONS/printmaxx_quant_terminal.py --summary # This view")
    console.print("  python3 AUTOMATIONS/printmaxx_quant_terminal.py --rbi     # RBI/Ops dashboard")
    console.print("  python3 AUTOMATIONS/twitter_alpha_scraper.py --all        # Daily research")
    console.print("  python3 scripts/rbi_audit.py full                         # Run full RBI audit")
    console.print("  bash ralph/run_all_loops.sh                               # Overnight loops")

    console.print("\n" + "=" * 70)
    console.print("[bold cyan]PRINTMAXX[/] [dim]// the game rewards aggression not caution[/]\n")


# =============================================================================
# RBI STANDALONE DASHBOARD (--rbi flag)
# =============================================================================

def print_rbi_dashboard():
    """Print standalone RBI/zero-cost ops dashboard"""
    console = Console()
    console.print()
    console.print("[bold cyan]PRINTMAXX RBI + ZERO-COST OPS DASHBOARD[/]")
    console.print(f"[dim]{datetime.now().strftime('%Y-%m-%d %H:%M')}[/]")
    console.print("=" * 70)

    # RBI Scanner
    rbi = load_rbi_scan()
    console.print(f"\n[bold]RBI SCANNER STATUS[/]")
    if rbi.scan_date:
        console.print(f"  Last scan: {rbi.scan_date}")
        console.print(f"  Total alpha: {rbi.total_alpha} | Pending: {rbi.pending_alpha} | HIGH/HIGHEST ROI: {rbi.high_roi_pending}")
        console.print(f"  Methods: {rbi.active_methods} active / {rbi.total_methods} total")
        console.print(f"  Content: {rbi.content_total} pieces | {rbi.content_queued} queued")

        if rbi.roi_distribution:
            console.print(f"\n  [bold]ROI Distribution:[/]")
            for roi, count in sorted(rbi.roi_distribution.items(), key=lambda x: x[1], reverse=True):
                bar = "=" * min(count, 40)
                console.print(f"    {roi:10s} {bar} {count}")

        if rbi.top_categories:
            console.print(f"\n  [bold]Alpha by Category:[/]")
            for cat, count in sorted(rbi.top_categories.items(), key=lambda x: x[1], reverse=True)[:10]:
                bar = "=" * min(count, 30)
                console.print(f"    {cat:20s} {bar} {count}")

        if rbi.recommendations:
            console.print(f"\n  [bold]RBI Recommendations:[/]")
            for rec in rbi.recommendations:
                console.print(f"    [yellow]>> {rec}[/]")

        if rbi.underallocated_methods:
            console.print(f"\n  [bold]Underallocated Methods:[/]")
            for m in rbi.underallocated_methods[:5]:
                console.print(f"    {m['name']}: {m['potential']}")

        if rbi.top_synergy_pairs:
            console.print(f"\n  [bold]Top Synergies:[/]")
            for syn in rbi.top_synergy_pairs[:5]:
                console.print(f"    {syn['method_1']} x {syn['method_2']} = {syn['multiplier']}x")
    else:
        console.print("  [yellow]No RBI scan found. Run: python3 scripts/rbi_audit.py full[/]")

    # Account Portfolio
    accounts = load_accounts()
    console.print(f"\n[bold]ACCOUNT PORTFOLIO ({len(accounts)} accounts)[/]")

    by_status = {}
    for acc in accounts:
        by_status.setdefault(acc.status, []).append(acc)

    for status in ['PENDING', 'NEEDS_CREATION', 'ACTIVE']:
        accs = by_status.get(status, [])
        if accs:
            sc = "yellow" if status == 'PENDING' else "red" if status == 'NEEDS_CREATION' else "green"
            console.print(f"\n  [{sc}]{status}[/] ({len(accs)}):")
            by_niche = {}
            for acc in accs:
                by_niche.setdefault(acc.niche, []).append(acc)
            for niche, niche_accs in sorted(by_niche.items()):
                platforms = ", ".join(a.platform for a in niche_accs)
                blocking = any('BLOCKING' in (a.notes or '') for a in niche_accs)
                flag = " [red bold]BLOCKING[/]" if blocking else ""
                console.print(f"    {niche:12s} {platforms}{flag}")

    # Zero-Cost Ops
    zero_ops = load_zero_cost_ops()
    active_ops = [o for o in zero_ops if o.status == "active"]
    ready_ops = [o for o in zero_ops if o.status == "ready"]
    not_started_ops = [o for o in zero_ops if o.status == "not_started"]

    console.print(f"\n[bold]ZERO-COST OPS DASHBOARD ({len(zero_ops)} categories)[/]")
    console.print(f"  [green]Active: {len(active_ops)}[/] | [yellow]Ready: {len(ready_ops)}[/] | [dim]Not started: {len(not_started_ops)}[/]\n")

    for op in sorted(zero_ops, key=lambda o: ({"active": 0, "ready": 1, "not_started": 2}.get(o.status, 3), -o.revenue_potential_high)):
        sc = "green" if op.status == "active" else "yellow" if op.status == "ready" else "dim"
        status_icon = "LIVE " if op.status == "active" else "READY" if op.status == "ready" else "IDLE "
        rev_str = f"${op.revenue_potential_low:,.0f}-${op.revenue_potential_high:,.0f}/mo" if op.revenue_potential_high > 0 else "Growth op"
        console.print(f"  [{sc}]{status_icon}[/] [{sc}]{op.category:20s}[/]  {rev_str:22s}  {op.description[:40]}")

    # Revenue Pipeline
    rev_30_low = sum(op.revenue_potential_low * 0.15 for op in zero_ops if op.status in ("active", "ready"))
    rev_30_high = sum(op.revenue_potential_high * 0.08 for op in zero_ops if op.status in ("active", "ready"))
    rev_60_low = sum(op.revenue_potential_low * 0.35 for op in zero_ops if op.status in ("active", "ready"))
    rev_60_high = sum(op.revenue_potential_high * 0.18 for op in zero_ops if op.status in ("active", "ready"))
    rev_90_low = sum(op.revenue_potential_low * 0.55 for op in zero_ops if op.status in ("active", "ready"))
    rev_90_high = sum(op.revenue_potential_high * 0.30 for op in zero_ops if op.status in ("active", "ready"))

    console.print(f"\n[bold]REVENUE PIPELINE PROJECTIONS[/]")
    console.print(f"  30 DAY:  [green]${rev_30_low:>8,.0f} - ${rev_30_high:>8,.0f}[/]  (conservative - aggressive)")
    console.print(f"  60 DAY:  [green]${rev_60_low:>8,.0f} - ${rev_60_high:>8,.0f}[/]  (ramp-up)")
    console.print(f"  90 DAY:  [green]${rev_90_low:>8,.0f} - ${rev_90_high:>8,.0f}[/]  (compounding)")

    # Top 10 Next Actions
    console.print(f"\n[bold]TOP 10 NEXT ACTIONS[/]")
    actions = []

    blocking_accs = [a for a in accounts if 'BLOCKING' in (a.notes or '')]
    for acc in blocking_accs[:3]:
        actions.append(("CRITICAL", f"Create {acc.platform} account ({acc.niche})", acc.notes or ""))

    top_ready = sorted(ready_ops, key=lambda o: o.revenue_potential_high, reverse=True)
    for op in top_ready[:4]:
        actions.append(("HIGH", f"Launch {op.category}", f"${op.revenue_potential_low}-${op.revenue_potential_high}/mo"))

    for rec in rbi.recommendations[:2]:
        actions.append(("MEDIUM", rec[:60], "From RBI scanner"))

    top_ns = sorted(not_started_ops, key=lambda o: o.revenue_potential_high, reverse=True)
    for op in top_ns[:2]:
        actions.append(("LOW", f"Setup {op.category}", f"${op.revenue_potential_low}-${op.revenue_potential_high}/mo"))

    for i, (priority, action, reason) in enumerate(actions[:10], 1):
        pc = "red" if priority == "CRITICAL" else "yellow" if priority == "HIGH" else "blue" if priority == "MEDIUM" else "dim"
        console.print(f"  [{pc}]{i:2d}. [{priority:8s}] {action}[/]")
        if reason:
            console.print(f"      [dim]{reason[:60]}[/]")

    # Social Setup Summary
    ss = load_social_setup_outputs()
    if ss.get("total_files", 0) > 0:
        console.print(f"\n[bold]SOCIAL SETUP LOOP ({ss['total_files']} outputs)[/]")
        checks = [
            ("Bios", ss.get("bios_ready")), ("Image prompts", ss.get("image_prompts_ready")),
            ("Content", ss.get("content_ready")), ("Newsletters", ss.get("newsletters_ready", 0) > 0),
            ("Warmup schedule", ss.get("warmup_schedule")), ("Posting schedule", ss.get("posting_schedule")),
            ("Accounts CSV", ss.get("accounts_updated")), ("Ecom plan", ss.get("ecom_plan")),
            ("Meme strategy", ss.get("meme_strategy")), ("Cross-promo", ss.get("cross_promo")),
            ("67-ops audit", ss.get("audit_complete")),
        ]
        done = sum(1 for _, v in checks if v)
        console.print(f"  Progress: {done}/{len(checks)} milestones")
        for label, v in checks:
            icon = "[green]OK[/]" if v else "[red]--[/]"
            console.print(f"    {icon} {label}")

    # Master Ops
    if MASTER_OPS_XLSX.exists():
        console.print(f"\n  [green]Master Ops Spreadsheet: PRINTMAXX_MASTER_OPS.xlsx[/]")

    console.print(f"\n[bold]COMMANDS[/]")
    console.print("  python3 scripts/rbi_audit.py full                         # Full RBI audit")
    console.print("  python3 AUTOMATIONS/printmaxx_quant_terminal.py           # Full TUI")
    console.print("  python3 AUTOMATIONS/printmaxx_quant_terminal.py --summary # System summary")

    console.print("\n" + "=" * 70)
    console.print("[bold cyan]PRINTMAXX[/] [dim]// the game rewards aggression not caution[/]\n")


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="PRINTMAXX Quant Terminal v4.0")
    parser.add_argument("--summary", action="store_true", help="Print summary and exit")
    parser.add_argument("--rbi", action="store_true", help="Print RBI/zero-cost ops dashboard and exit")
    args = parser.parse_args()

    if args.rbi:
        print_rbi_dashboard()
        return

    if args.summary:
        print_summary()
        return

    if not HAS_TEXTUAL:
        print("Textual not installed. Install with: pip install textual rich")
        print("Running summary mode instead...\n")
        print_summary()
        return

    app = PrintmaxxQuantTerminal()
    app.run()


if __name__ == "__main__":
    main()
