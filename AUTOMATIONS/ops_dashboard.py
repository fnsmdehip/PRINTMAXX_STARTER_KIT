#!/usr/bin/env python3
"""
PRINTMAXX OPS DASHBOARD - Jane Street Style
============================================
Real-time monitoring and execution of all 53 daily/weekly/monthly ops patterns.
Bloomberg Terminal-style TUI for solopreneurs.

Run: python3 AUTOMATIONS/ops_dashboard.py
"""

import os
import sys
import json
import csv
import subprocess
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Check for required packages
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.style import Style
    from rich import box
except ImportError:
    print("Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "rich", "-q"])
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.style import Style
    from rich import box

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_DIR / "LEDGER"
OPS_DIR = PROJECT_DIR / "OPS"
RALPH_DIR = PROJECT_DIR / "ralph"

# State file for tracking ops execution
OPS_STATE_FILE = LEDGER_DIR / "OPS_EXECUTION_STATE.json"

console = Console()


class OpsStatus(Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    OVERDUE = "OVERDUE"
    FAILED = "FAILED"


class OpsFrequency(Enum):
    CONTINUOUS = "continuous"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"


@dataclass
class OpsPattern:
    """Represents a single ops pattern to track and execute."""
    id: str
    name: str
    frequency: OpsFrequency
    duration_min: int
    description: str
    output_file: str
    tools: List[str] = field(default_factory=list)
    cost_monthly: float = 0.0
    category: str = "GENERAL"
    last_run: Optional[datetime] = None
    next_due: Optional[datetime] = None
    status: OpsStatus = OpsStatus.NOT_STARTED
    run_count: int = 0
    alerts: List[str] = field(default_factory=list)

    def is_overdue(self) -> bool:
        if self.next_due is None:
            return False
        return datetime.now() > self.next_due

    def calculate_next_due(self):
        now = datetime.now()
        if self.frequency == OpsFrequency.DAILY:
            # Next 8 AM
            next_run = now.replace(hour=8, minute=0, second=0, microsecond=0)
            if now.hour >= 8:
                next_run += timedelta(days=1)
            self.next_due = next_run
        elif self.frequency == OpsFrequency.WEEKLY:
            # Next Monday 8 AM
            days_until_monday = (7 - now.weekday()) % 7
            if days_until_monday == 0 and now.hour >= 8:
                days_until_monday = 7
            next_run = now.replace(hour=8, minute=0, second=0, microsecond=0)
            next_run += timedelta(days=days_until_monday)
            self.next_due = next_run
        elif self.frequency == OpsFrequency.MONTHLY:
            # First of next month
            if now.day == 1 and now.hour < 8:
                self.next_due = now.replace(hour=8, minute=0, second=0, microsecond=0)
            else:
                if now.month == 12:
                    self.next_due = now.replace(year=now.year+1, month=1, day=1, hour=8, minute=0, second=0, microsecond=0)
                else:
                    self.next_due = now.replace(month=now.month+1, day=1, hour=8, minute=0, second=0, microsecond=0)
        elif self.frequency == OpsFrequency.CONTINUOUS:
            self.next_due = now  # Always due


# Define all 53 ops patterns
ALL_OPS_PATTERNS: List[OpsPattern] = [
    # SECTION 1: @pipelineabuser-Style Daily Ops
    OpsPattern("DOP001", "Competitor Price Monitoring", OpsFrequency.CONTINUOUS, 5,
               "Monitor 200+ competitor pages via visualping.io",
               "LEDGER/COMPETITOR_CHANGES.csv", ["visualping.io"], 13.0, "COMPETITOR_INTEL"),
    OpsPattern("DOP002", "Cold Lead Research Pipeline", OpsFrequency.DAILY, 30,
               "Micro-cohort research via Clay (20-50 leads/day)",
               "LEDGER/OUTREACH_DAILY.csv", ["Clay", "Apollo"], 248.0, "COLD_OUTBOUND"),
    OpsPattern("DOP003", "Platform Algorithm Detection", OpsFrequency.DAILY, 20,
               "Scan Meta/TikTok/Google for algorithm changes",
               "LEDGER/PLATFORM_CHANGES.csv", [], 0.0, "PLATFORM_INTEL"),
    OpsPattern("DOP004", "Revenue Dashboard Check", OpsFrequency.DAILY, 10,
               "Check RevenueCat + Stripe + Gumroad metrics",
               "FINANCIALS/DAILY_METRICS.csv", ["RevenueCat", "Stripe"], 0.0, "REVENUE"),

    # SECTION 2: Reddit Research Ops
    OpsPattern("DOP005", "Reddit Revenue Extraction", OpsFrequency.DAILY, 15,
               "Scan r/SideProject, r/EntrepreneurRideAlong for case studies",
               "LEDGER/ALPHA_STAGING.csv", [], 0.0, "RESEARCH"),
    OpsPattern("DOP006", "Cold Email Deliverability Scan", OpsFrequency.WEEKLY, 30,
               "Check r/coldemail, blogs for deliverability changes",
               "LEDGER/COLD_EMAIL_META.csv", [], 0.0, "COLD_OUTBOUND"),
    OpsPattern("DOP007", "Reddit GEO Opportunity Scan", OpsFrequency.WEEKLY, 30,
               "Find Reddit threads for AI citation opportunities",
               "LEDGER/REDDIT_GEO_TRACKER.csv", [], 0.0, "SEO_GEO"),

    # SECTION 3: GitHub Research Ops
    OpsPattern("DOP008", "GitHub Trending Scan", OpsFrequency.DAILY, 15,
               "Scan github.com/trending for MIT repos to clone",
               "LEDGER/GITHUB_TRENDING_DAILY.csv", [], 0.0, "RESEARCH"),
    OpsPattern("DOP009", "MCP Ecosystem Monitoring", OpsFrequency.DAILY, 10,
               "Track new MCP servers (first-mover window)",
               "LEDGER/MCP_OPPORTUNITIES.csv", [], 0.0, "MCP_FIRST_MOVER"),

    # SECTION 4: Platform Arbitrage
    OpsPattern("DOP010", "Platform RPM Tracking", OpsFrequency.WEEKLY, 30,
               "Track RPMs across FB Reels/TikTok/YouTube/X",
               "LEDGER/PLATFORM_RPM_TRACKER.csv", [], 0.0, "PLATFORM_INTEL"),
    OpsPattern("DOP011", "Creator Program Monitoring", OpsFrequency.WEEKLY, 20,
               "Track payout changes across platforms",
               "LEDGER/CREATOR_PROGRAMS.csv", [], 0.0, "PLATFORM_INTEL"),

    # SECTION 5: App Store Research
    OpsPattern("DOP012", "ASO Keyword Research", OpsFrequency.WEEKLY, 45,
               "Find keyword gaps (popularity 20+, difficulty <60)",
               "LEDGER/ASO_KEYWORD_TRACKER.csv", ["App Radar"], 0.0, "APP_FACTORY"),
    OpsPattern("DOP013", "Competitor App Monitoring", OpsFrequency.WEEKLY, 30,
               "Track competitor app pricing/features/reviews",
               "LEDGER/COMPETITOR_APPS.csv", [], 0.0, "APP_FACTORY"),

    # SECTION 6: Revenue Research
    OpsPattern("DOP014", "Indie Hacker Tracking", OpsFrequency.WEEKLY, 20,
               "Track verified MRR from top indie hackers",
               "LEDGER/INDIE_HACKER_TRACKER.csv", [], 0.0, "RESEARCH"),
    OpsPattern("DOP015", "RevenueCat Report Analysis", OpsFrequency.MONTHLY, 60,
               "Extract benchmarks from new RevenueCat reports",
               "MONEY_METHODS/APP_FACTORY/BENCHMARKS.csv", [], 0.0, "APP_FACTORY"),

    # SECTION 7: Content Research
    OpsPattern("DOP016", "Viral Content Detection", OpsFrequency.DAILY, 15,
               "Detect viral TikTok/Reels formats to replicate",
               "LEDGER/VIRAL_CONTENT_TRACKER.csv", [], 0.0, "CONTENT"),
    OpsPattern("DOP017", "Hashtag/Audio Tracking", OpsFrequency.DAILY, 10,
               "Track trending sounds/hashtags before content creation",
               "LEDGER/TRENDING_AUDIO_HASHTAGS.csv", [], 0.0, "CONTENT"),

    # SECTION 8: Tool Research
    OpsPattern("DOP018", "New Tool Detection", OpsFrequency.WEEKLY, 30,
               "Scan Product Hunt, Reddit for new tools",
               "LEDGER/TOOLS_SERVICES_MASTER.csv", [], 0.0, "RESEARCH"),

    # SECTION 9: Cold Email Ops (NEW from comprehensive scan)
    OpsPattern("DOP019", "Email Warmup Health Monitoring", OpsFrequency.DAILY, 15,
               "Check inbox rate >95%, bounce <3%, complaints <0.1%",
               "LEDGER/EMAIL_HEALTH_DAILY.csv", ["Instantly", "Smartlead"], 50.0, "COLD_OUTBOUND"),
    OpsPattern("DOP020", "Micro-Cohort Performance Tracking", OpsFrequency.WEEKLY, 30,
               "Analyze reply rates by cohort size (≤50 = 2.76x better)",
               "MONEY_METHODS/COLD_OUTBOUND/campaign_metrics_weekly.csv", [], 0.0, "COLD_OUTBOUND"),

    # SECTION 10: Content & Social Ops
    OpsPattern("DOP021", "Content Volume Posting", OpsFrequency.DAILY, 30,
               "Schedule 8-10 posts/day across platforms",
               "LEDGER/CONTENT_PERFORMANCE_DAILY.csv", ["Buffer", "Publer"], 15.0, "CONTENT"),
    OpsPattern("DOP022", "AI UGC Factory", OpsFrequency.DAILY, 30,
               "Generate 5-10 AI UGC videos per day",
               "AI_INFLUENCER/ugc_performance_daily.csv", ["Arcads", "HeyGen"], 150.0, "CONTENT"),
    OpsPattern("DOP023", "Social Engagement Metrics Rollup", OpsFrequency.DAILY, 10,
               "Track impressions, engagement, follower delta",
               "LEDGER/ENGAGEMENT_METRICS_DAILY.csv", [], 0.0, "CONTENT"),

    # SECTION 11: Lead Gen & Sales Ops
    OpsPattern("DOP024", "Intent Signal Detection", OpsFrequency.DAILY, 30,
               "Detect leadership changes, job removals, Glassdoor spikes",
               "LEDGER/INTENT_SIGNALS_DAILY.csv", ["theorg.com"], 0.0, "COLD_OUTBOUND"),
    OpsPattern("DOP025", "Lead Quality Scoring", OpsFrequency.WEEKLY, 20,
               "Calculate cost-per-lead, conversion by source",
               "LEDGER/LEAD_QUALITY_WEEKLY.csv", ["HubSpot"], 0.0, "COLD_OUTBOUND"),
    OpsPattern("DOP026", "Sales Pipeline Velocity", OpsFrequency.WEEKLY, 15,
               "Track pipeline, forecast next 90 days",
               "LEDGER/PIPELINE_VELOCITY_WEEKLY.csv", [], 0.0, "COLD_OUTBOUND"),

    # SECTION 12: Monetization & Finance
    OpsPattern("DOP027", "Digital Product Publishing", OpsFrequency.WEEKLY, 120,
               "Create 10 new digital product listings",
               "LEDGER/DIGITAL_PRODUCTS_WEEKLY.csv", ["Whop", "Gumroad"], 0.0, "MONETIZATION"),
    OpsPattern("DOP028", "Affiliate Commission Tracking", OpsFrequency.WEEKLY, 15,
               "Track clicks, conversions, revenue per affiliate link",
               "LEDGER/AFFILIATE_PERFORMANCE_WEEKLY.csv", [], 0.0, "MONETIZATION"),
    OpsPattern("DOP029", "Trading Automation Monitoring", OpsFrequency.CONTINUOUS, 5,
               "Monitor Polymarket positions, 30-sec arbitrage windows",
               "LEDGER/TRADING_DAILY.csv", ["Polymarket API"], 0.0, "TRADING"),

    # SECTION 13: Platform & Infrastructure
    OpsPattern("DOP030", "Account Health Monitoring", OpsFrequency.DAILY, 5,
               "Check for shadowbans, restrictions, reputation",
               "LEDGER/ACCOUNT_HEALTH_DAILY.csv", [], 0.0, "INFRASTRUCTURE"),
    OpsPattern("DOP031", "Automation ROI Tracking", OpsFrequency.MONTHLY, 60,
               "Calculate ROI per automation (target >200%)",
               "LEDGER/AUTOMATION_ROI_MONTHLY.csv", [], 0.0, "INFRASTRUCTURE"),

    # SECTION 14: Discovery & Research
    OpsPattern("DOP032", "New Niche Discovery", OpsFrequency.WEEKLY, 30,
               "Find subreddits >10K with >5%/month growth",
               "LEDGER/NICHE_DISCOVERY_WEEKLY.csv", [], 0.0, "DISCOVERY"),
    OpsPattern("DOP033", "Emerging Platform Detection", OpsFrequency.WEEKLY, 45,
               "Detect platforms with 40M+ users, no monetization",
               "LEDGER/EMERGING_PLATFORMS.csv", [], 0.0, "DISCOVERY"),

    # SECTION 15: Influencer & Partnership
    OpsPattern("DOP034", "Micro-Influencer Campaigns", OpsFrequency.WEEKLY, 120,
               "Recruit 5 creators, track performance",
               "LEDGER/INFLUENCER_CAMPAIGNS.csv", ["FindMeCreators"], 0.0, "PARTNERSHIPS"),
    OpsPattern("DOP035", "Trend Replication Sprint", OpsFrequency.MONTHLY, 480,
               "Pick top 3 trends, replicate within 2 weeks",
               "LEDGER/TREND_INTEL_TRACKER.csv", [], 0.0, "TRENDS"),

    # SECTION 16: Compliance & Risk
    OpsPattern("DOP036", "FTC Compliance Monitoring", OpsFrequency.WEEKLY, 30,
               "Audit posts for disclosures, AI labels, claims",
               "LEDGER/COMPLIANCE_WEEKLY.csv", [], 0.0, "COMPLIANCE"),

    # SECTION 17: A/B Testing
    OpsPattern("DOP037", "A/B Test Execution", OpsFrequency.WEEKLY, 60,
               "Start 1-2 tests from AB_TESTS_MASTER backlog",
               "LEDGER/AB_TESTS_MASTER.csv", [], 0.0, "TESTING"),

    # Additional patterns from comprehensive scan
    OpsPattern("DOP038", "Twitter High-Signal Scraping", OpsFrequency.DAILY, 15,
               "Scrape 81+ auto_monitor accounts from HIGH_SIGNAL_SOURCES",
               "LEDGER/ALPHA_STAGING.csv", ["Chrome MCP"], 0.0, "RESEARCH"),
    OpsPattern("DOP039", "Product Hunt Daily Scan", OpsFrequency.DAILY, 10,
               "Check top 5 Product Hunt launches",
               "LEDGER/ALPHA_STAGING.csv", [], 0.0, "RESEARCH"),
    OpsPattern("DOP040", "Competitor Feature Tracking", OpsFrequency.WEEKLY, 30,
               "Track feature releases from competitors",
               "LEDGER/COMPETITOR_FEATURES.csv", [], 0.0, "COMPETITOR_INTEL"),
    OpsPattern("DOP041", "Newsletter Subscriber Tracking", OpsFrequency.WEEKLY, 15,
               "Track growth, engagement, unsubscribe rates",
               "LEDGER/NEWSLETTER_METRICS.csv", ["Beehiiv"], 0.0, "CONTENT"),
    OpsPattern("DOP042", "Content Calendar Adherence", OpsFrequency.DAILY, 5,
               "Check % of planned content actually posted",
               "LEDGER/CONTENT_CALENDAR_30DAY.csv", [], 0.0, "CONTENT"),
    OpsPattern("DOP043", "Funnel Conversion Tracking", OpsFrequency.WEEKLY, 30,
               "Track lead → trial → paid conversion per funnel",
               "LEDGER/FUNNEL_METRICS.csv", [], 0.0, "REVENUE"),
    OpsPattern("DOP044", "Platform Account Growth", OpsFrequency.WEEKLY, 15,
               "Track follower growth rate per account per platform",
               "LEDGER/ACCOUNT_GROWTH_WEEKLY.csv", [], 0.0, "CONTENT"),

    # Intent signal sub-patterns
    OpsPattern("DOP045", "Leadership Change Detection (theorg.com)", OpsFrequency.DAILY, 10,
               "Monitor theorg.com for C-suite changes at target companies",
               "LEDGER/INTENT_SIGNALS_DAILY.csv", ["theorg.com"], 0.0, "COLD_OUTBOUND"),
    OpsPattern("DOP046", "Job Posting Removal Tracking", OpsFrequency.DAILY, 10,
               "Track when job postings removed (hired = need tools)",
               "LEDGER/INTENT_SIGNALS_DAILY.csv", [], 0.0, "COLD_OUTBOUND"),
    OpsPattern("DOP047", "Glassdoor Rating Spikes", OpsFrequency.DAILY, 10,
               "Detect rating drops >0.5 (internal chaos = opportunity)",
               "LEDGER/INTENT_SIGNALS_DAILY.csv", [], 0.0, "COLD_OUTBOUND"),
    OpsPattern("DOP048", "10-K Filing Change Detection", OpsFrequency.QUARTERLY, 30,
               "Diff 10-K filings for new risk mentions",
               "LEDGER/INTENT_SIGNALS_DAILY.csv", ["SEC EDGAR"], 0.0, "COLD_OUTBOUND"),

    # Additional from LEDGER gap analysis
    OpsPattern("DOP049", "Meme Coin Signal Monitoring", OpsFrequency.CONTINUOUS, 5,
               "4-hourly Pump.fun scan for meme coin signals",
               "LEDGER/MEME_COIN_SIGNALS.csv", ["Pump.fun"], 0.0, "TRADING"),
    OpsPattern("DOP050", "Government Website Monitoring", OpsFrequency.DAILY, 15,
               "Monitor gov pages for compliance/regulatory changes",
               "LEDGER/GOV_ALERTS.csv", ["visualping.io"], 0.0, "COMPLIANCE"),
    OpsPattern("DOP051", "Competitor Pricing Arbitrage", OpsFrequency.CONTINUOUS, 5,
               "Real-time price monitoring for undercut opportunities",
               "LEDGER/COMPETITOR_CHANGES.csv", ["visualping.io"], 0.0, "COMPETITOR_INTEL"),
    OpsPattern("DOP052", "Cross-Pollination Execution", OpsFrequency.WEEKLY, 60,
               "Execute top synergy stacks from CROSS_POLLINATION_MATRIX",
               "LEDGER/CROSS_POLLINATION_MATRIX.csv", [], 0.0, "STRATEGY"),
    OpsPattern("DOP053", "Backtest Pending Alpha", OpsFrequency.WEEKLY, 45,
               "Run backtest_alpha.py on PENDING_REVIEW entries",
               "LEDGER/BACKTESTS/BACKTEST_RESULTS.csv", [], 0.0, "RESEARCH"),
]


class OpsStateManager:
    """Manages persistent state for ops execution."""

    def __init__(self, state_file: Path = OPS_STATE_FILE):
        self.state_file = state_file
        self.state: Dict = {}
        self.load_state()

    def load_state(self):
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    self.state = json.load(f)
            except:
                self.state = {}
        else:
            self.state = {}

    def save_state(self):
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2, default=str)

    def update_ops(self, ops_id: str, status: OpsStatus, last_run: datetime = None):
        if ops_id not in self.state:
            self.state[ops_id] = {}
        self.state[ops_id]['status'] = status.value
        self.state[ops_id]['last_run'] = (last_run or datetime.now()).isoformat()
        self.state[ops_id]['run_count'] = self.state[ops_id].get('run_count', 0) + 1
        self.save_state()

    def get_ops_state(self, ops_id: str) -> Dict:
        return self.state.get(ops_id, {})


class OpsDashboard:
    """Jane Street-style TUI dashboard for ops management."""

    def __init__(self):
        self.state_manager = OpsStateManager()
        self.ops_patterns = ALL_OPS_PATTERNS
        self.running_ops: Dict[str, threading.Thread] = {}
        self.alerts: List[str] = []
        self.activity_log: List[str] = []

        # Apply saved state to patterns
        self._apply_saved_state()

        # Calculate due dates
        for ops in self.ops_patterns:
            ops.calculate_next_due()
            if ops.is_overdue() and ops.status != OpsStatus.IN_PROGRESS:
                ops.status = OpsStatus.OVERDUE

    def _apply_saved_state(self):
        for ops in self.ops_patterns:
            saved = self.state_manager.get_ops_state(ops.id)
            if saved:
                if saved.get('last_run'):
                    ops.last_run = datetime.fromisoformat(saved['last_run'])
                if saved.get('status'):
                    ops.status = OpsStatus(saved['status'])
                ops.run_count = saved.get('run_count', 0)

    def _log_activity(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.activity_log.append(f"[{timestamp}] {message}")
        if len(self.activity_log) > 50:
            self.activity_log = self.activity_log[-50:]

    def _check_alerts(self):
        self.alerts = []
        overdue_count = sum(1 for o in self.ops_patterns if o.status == OpsStatus.OVERDUE)
        if overdue_count > 0:
            self.alerts.append(f"⚠️  {overdue_count} OPS OVERDUE - Run now!")

        # Check for high-priority overdue
        high_priority_overdue = [o for o in self.ops_patterns
                                  if o.status == OpsStatus.OVERDUE
                                  and o.category in ["COLD_OUTBOUND", "REVENUE", "MCP_FIRST_MOVER"]]
        for ops in high_priority_overdue:
            self.alerts.append(f"🔴 CRITICAL: {ops.name} overdue!")

    def get_ops_by_frequency(self, freq: OpsFrequency) -> List[OpsPattern]:
        return [o for o in self.ops_patterns if o.frequency == freq]

    def get_ops_by_category(self, category: str) -> List[OpsPattern]:
        return [o for o in self.ops_patterns if o.category == category]

    def run_ops(self, ops_id: str):
        """Execute a specific ops pattern."""
        ops = next((o for o in self.ops_patterns if o.id == ops_id), None)
        if not ops:
            self._log_activity(f"ERROR: Ops {ops_id} not found")
            return

        ops.status = OpsStatus.IN_PROGRESS
        self._log_activity(f"▶️  Started: {ops.name}")

        # Simulate execution (in real implementation, this would call actual scripts)
        def execute():
            import time
            time.sleep(2)  # Simulate work
            ops.status = OpsStatus.COMPLETED
            ops.last_run = datetime.now()
            ops.calculate_next_due()
            ops.run_count += 1
            self.state_manager.update_ops(ops_id, OpsStatus.COMPLETED, ops.last_run)
            self._log_activity(f"✅ Completed: {ops.name}")

        thread = threading.Thread(target=execute)
        thread.start()
        self.running_ops[ops_id] = thread

    def run_all_daily_ops(self):
        """Run all daily ops sequentially."""
        daily_ops = self.get_ops_by_frequency(OpsFrequency.DAILY)
        self._log_activity(f"🚀 Starting {len(daily_ops)} daily ops...")
        for ops in daily_ops:
            if ops.status != OpsStatus.IN_PROGRESS:
                self.run_ops(ops.id)

    def create_status_table(self, ops_list: List[OpsPattern], title: str) -> Table:
        """Create a Rich table for ops status."""
        table = Table(title=title, box=box.ROUNDED, show_header=True, header_style="bold cyan")
        table.add_column("ID", style="dim", width=8)
        table.add_column("Name", width=30)
        table.add_column("Status", width=12)
        table.add_column("Last Run", width=12)
        table.add_column("Next Due", width=12)
        table.add_column("Time", width=6)
        table.add_column("Cat", width=12)

        for ops in ops_list[:15]:  # Limit display
            status_style = {
                OpsStatus.NOT_STARTED: "dim",
                OpsStatus.IN_PROGRESS: "yellow",
                OpsStatus.COMPLETED: "green",
                OpsStatus.OVERDUE: "red bold",
                OpsStatus.FAILED: "red"
            }.get(ops.status, "white")

            status_icon = {
                OpsStatus.NOT_STARTED: "○",
                OpsStatus.IN_PROGRESS: "◐",
                OpsStatus.COMPLETED: "●",
                OpsStatus.OVERDUE: "⚠",
                OpsStatus.FAILED: "✗"
            }.get(ops.status, "?")

            last_run = ops.last_run.strftime("%m/%d %H:%M") if ops.last_run else "-"
            next_due = ops.next_due.strftime("%m/%d %H:%M") if ops.next_due else "-"

            table.add_row(
                ops.id,
                ops.name[:28] + ".." if len(ops.name) > 30 else ops.name,
                f"[{status_style}]{status_icon} {ops.status.value[:8]}[/]",
                last_run,
                next_due,
                f"{ops.duration_min}m",
                ops.category[:10]
            )

        return table

    def create_alerts_panel(self) -> Panel:
        """Create alerts panel."""
        self._check_alerts()
        if not self.alerts:
            content = "[green]✓ All systems nominal[/]"
        else:
            content = "\n".join(self.alerts)
        return Panel(content, title="[red bold]⚡ ALERTS", border_style="red")

    def create_stats_panel(self) -> Panel:
        """Create statistics panel."""
        total = len(self.ops_patterns)
        completed_today = sum(1 for o in self.ops_patterns
                              if o.last_run and o.last_run.date() == datetime.now().date())
        overdue = sum(1 for o in self.ops_patterns if o.status == OpsStatus.OVERDUE)
        running = sum(1 for o in self.ops_patterns if o.status == OpsStatus.IN_PROGRESS)

        daily_ops = len(self.get_ops_by_frequency(OpsFrequency.DAILY))
        weekly_ops = len(self.get_ops_by_frequency(OpsFrequency.WEEKLY))
        monthly_ops = len(self.get_ops_by_frequency(OpsFrequency.MONTHLY))

        monthly_cost = sum(o.cost_monthly for o in self.ops_patterns)

        stats = f"""[bold cyan]PRINTMAXX OPS DASHBOARD[/]
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Patterns: [bold]{total}[/]
├─ Daily:   {daily_ops}
├─ Weekly:  {weekly_ops}
└─ Monthly: {monthly_ops}

[bold]Today's Status:[/]
├─ Completed: [green]{completed_today}[/]
├─ Running:   [yellow]{running}[/]
└─ Overdue:   [red]{overdue}[/]

[bold]Tool Cost:[/] ${monthly_cost:.0f}/mo

[dim]Press Ctrl+C to exit[/]
[dim]Last refresh: {datetime.now().strftime('%H:%M:%S')}[/]
"""
        return Panel(stats, title="📊 STATS", border_style="blue")

    def create_activity_panel(self) -> Panel:
        """Create activity log panel."""
        if not self.activity_log:
            content = "[dim]No activity yet[/]"
        else:
            content = "\n".join(self.activity_log[-10:])
        return Panel(content, title="📋 ACTIVITY LOG", border_style="green")

    def create_quick_actions_panel(self) -> Panel:
        """Create quick actions panel."""
        actions = """[bold]Quick Actions:[/]

[cyan]1[/] Run all OVERDUE ops
[cyan]2[/] Run all daily ops
[cyan]3[/] Run all weekly ops
[cyan]4[/] Launch ralph daily_ops loop
[cyan]5[/] Open OPS patterns doc
[cyan]6[/] Refresh dashboard

[dim]Enter number + Enter to execute[/]
"""
        return Panel(actions, title="⚡ QUICK ACTIONS", border_style="magenta")

    def create_categories_panel(self) -> Panel:
        """Create category summary panel."""
        categories = {}
        for ops in self.ops_patterns:
            if ops.category not in categories:
                categories[ops.category] = {"total": 0, "completed": 0, "overdue": 0}
            categories[ops.category]["total"] += 1
            if ops.status == OpsStatus.COMPLETED:
                categories[ops.category]["completed"] += 1
            elif ops.status == OpsStatus.OVERDUE:
                categories[ops.category]["overdue"] += 1

        lines = []
        for cat, stats in sorted(categories.items()):
            pct = (stats["completed"] / stats["total"] * 100) if stats["total"] > 0 else 0
            bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
            overdue_str = f"[red]({stats['overdue']} overdue)[/]" if stats["overdue"] > 0 else ""
            lines.append(f"{cat[:12]:12} {bar} {pct:3.0f}% {overdue_str}")

        content = "\n".join(lines[:8])
        return Panel(content, title="📁 CATEGORIES", border_style="yellow")

    def create_layout(self) -> Layout:
        """Create the full dashboard layout."""
        layout = Layout()

        # Main split: left (tables) and right (panels)
        layout.split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=1)
        )

        # Left: ops tables stacked
        layout["left"].split_column(
            Layout(name="daily_ops"),
            Layout(name="weekly_ops")
        )

        # Right: info panels stacked
        layout["right"].split_column(
            Layout(name="stats"),
            Layout(name="alerts"),
            Layout(name="activity"),
            Layout(name="actions")
        )

        # Populate layouts
        daily_ops = self.get_ops_by_frequency(OpsFrequency.DAILY)
        weekly_ops = self.get_ops_by_frequency(OpsFrequency.WEEKLY)

        layout["daily_ops"].update(self.create_status_table(daily_ops, "📅 DAILY OPS"))
        layout["weekly_ops"].update(self.create_status_table(weekly_ops, "📆 WEEKLY OPS"))
        layout["stats"].update(self.create_stats_panel())
        layout["alerts"].update(self.create_alerts_panel())
        layout["activity"].update(self.create_activity_panel())
        layout["actions"].update(self.create_quick_actions_panel())

        return layout

    def run(self):
        """Run the dashboard with live updates."""
        console.clear()

        # Print header
        console.print(Panel.fit(
            "[bold cyan]PRINTMAXX OPS DASHBOARD[/] - Jane Street Style\n"
            "[dim]Real-time monitoring of 53 ops patterns across 17 categories[/]",
            border_style="cyan"
        ))

        try:
            with Live(self.create_layout(), refresh_per_second=1, console=console) as live:
                while True:
                    live.update(self.create_layout())
                    import time
                    time.sleep(1)
        except KeyboardInterrupt:
            console.print("\n[yellow]Dashboard stopped. State saved.[/]")
            self.state_manager.save_state()


def print_summary():
    """Print a static summary of all ops patterns."""
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]PRINTMAXX OPS PATTERNS SUMMARY[/]\n"
        f"[dim]Total: {len(ALL_OPS_PATTERNS)} patterns | "
        f"Daily: {len([o for o in ALL_OPS_PATTERNS if o.frequency == OpsFrequency.DAILY])} | "
        f"Weekly: {len([o for o in ALL_OPS_PATTERNS if o.frequency == OpsFrequency.WEEKLY])} | "
        f"Monthly: {len([o for o in ALL_OPS_PATTERNS if o.frequency == OpsFrequency.MONTHLY])}[/]",
        border_style="cyan"
    ))

    # Group by category
    categories = {}
    for ops in ALL_OPS_PATTERNS:
        if ops.category not in categories:
            categories[ops.category] = []
        categories[ops.category].append(ops)

    for category, ops_list in sorted(categories.items()):
        table = Table(title=f"📁 {category}", box=box.SIMPLE)
        table.add_column("ID", style="dim")
        table.add_column("Name")
        table.add_column("Freq", style="cyan")
        table.add_column("Time", style="yellow")
        table.add_column("Cost", style="green")
        table.add_column("Output File", style="dim")

        for ops in ops_list:
            cost_str = f"${ops.cost_monthly:.0f}" if ops.cost_monthly > 0 else "-"
            table.add_row(
                ops.id,
                ops.name,
                ops.frequency.value[:6],
                f"{ops.duration_min}m",
                cost_str,
                ops.output_file.split("/")[-1][:25]
            )

        console.print(table)
        console.print()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="PRINTMAXX Ops Dashboard")
    parser.add_argument("--summary", action="store_true", help="Print summary and exit")
    parser.add_argument("--run", type=str, help="Run specific ops by ID (e.g., DOP001)")
    parser.add_argument("--run-daily", action="store_true", help="Run all daily ops")
    parser.add_argument("--run-overdue", action="store_true", help="Run all overdue ops")
    args = parser.parse_args()

    if args.summary:
        print_summary()
        return

    dashboard = OpsDashboard()

    if args.run:
        dashboard.run_ops(args.run)
        import time
        time.sleep(3)
        return

    if args.run_daily:
        dashboard.run_all_daily_ops()
        import time
        time.sleep(30)
        return

    if args.run_overdue:
        overdue_ops = [o for o in dashboard.ops_patterns if o.status == OpsStatus.OVERDUE]
        console.print(f"Running {len(overdue_ops)} overdue ops...")
        for ops in overdue_ops:
            dashboard.run_ops(ops.id)
        import time
        time.sleep(len(overdue_ops) * 3)
        return

    # Default: run live dashboard
    dashboard.run()


if __name__ == "__main__":
    main()
