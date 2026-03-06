#!/usr/bin/env python3
"""
PRINTMAXX Quant Infrastructure Dashboard
Jane Street / Renaissance Technologies style terminal interface

Full 6-panel Bloomberg-style dashboard:
1. Alpha Discovery Panel - live alpha feed
2. Method Performance Panel - revenue metrics by method
3. Agent Activity Panel - running agents
4. Portfolio View - capital allocation & diversification
5. Backtest Results Panel - alpha validation scores
6. Alerts & Notifications - degradation, opportunities, risks

Usage:
    python3 quant_dashboard.py
    python3 quant_dashboard.py --mode alpha  # Alpha Discovery only
    python3 quant_dashboard.py --mode methods  # Method Performance only
"""

import os
import csv
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, DataTable, Static, Log, ProgressBar
from textual.reactive import reactive
from textual import work
from rich.text import Text
from rich.table import Table
from rich.panel import Panel

# Paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_DIR / "LEDGER"
FINANCIALS_DIR = PROJECT_DIR / "FINANCIALS"
TASK_DIR = Path("/private/tmp/claude-501/-Users-macbookpro-Documents-p-PRINTMAXX-STARTER-KITttttt/tasks")
RALPH_DIR = PROJECT_DIR / "ralph/loops/mega"

class AlphaDiscoveryPanel(Static):
    """Live alpha feed - newest entries from ALPHA_STAGING.csv"""

    def compose(self) -> ComposeResult:
        yield Static("📡 Alpha Discovery Feed", classes="panel-title")
        yield DataTable(id="alpha-table")

    def on_mount(self) -> None:
        table = self.query_one("#alpha-table", DataTable)
        table.add_columns("ID", "Category", "ROI", "Source", "Age")
        self.load_alpha()

    def load_alpha(self) -> None:
        """Load recent alpha entries"""
        table = self.query_one("#alpha-table", DataTable)
        table.clear()

        alpha_file = LEDGER_DIR / "ALPHA_STAGING.csv"
        if not alpha_file.exists():
            return

        try:
            with open(alpha_file, 'r') as f:
                reader = csv.DictReader(f)
                entries = list(reader)

            # Get last 20 entries, most recent first
            recent = entries[-20:][::-1]

            for entry in recent:
                alpha_id = entry.get('alpha_id', 'N/A')
                category = entry.get('category', 'N/A')
                roi = entry.get('roi_potential', 'N/A')
                source = entry.get('source', 'N/A')

                # Calculate age
                created = entry.get('created_at', '')
                age = self._calculate_age(created)

                # Color code by ROI
                roi_style = "green" if roi == "HIGHEST" else "yellow" if roi == "HIGH" else "white"

                table.add_row(
                    alpha_id,
                    category[:20],
                    Text(roi, style=roi_style),
                    source[:20],
                    age
                )
        except Exception as e:
            table.add_row("ERROR", str(e), "", "", "")

    def _calculate_age(self, created_at: str) -> str:
        """Calculate how long ago entry was created"""
        if not created_at:
            return "N/A"
        try:
            created = datetime.fromisoformat(created_at)
            age = datetime.now() - created
            if age.days > 0:
                return f"{age.days}d"
            elif age.seconds > 3600:
                return f"{age.seconds // 3600}h"
            else:
                return f"{age.seconds // 60}m"
        except:
            return "N/A"


class MethodPerformancePanel(Static):
    """Method performance metrics - revenue, time, Sharpe ratio equivalent"""

    def compose(self) -> ComposeResult:
        yield Static("📊 Method Performance", classes="panel-title")
        yield DataTable(id="methods-table")

    def on_mount(self) -> None:
        table = self.query_one("#methods-table", DataTable)
        table.add_columns("Method", "Rev/mo", "Time/wk", "$/hr", "Win Rate", "Trend")
        self.load_methods()

    def load_methods(self) -> None:
        """Load method performance from REVENUE_TRACKER.csv and time tracking"""
        table = self.query_one("#methods-table", DataTable)
        table.clear()

        # For now, show placeholder data
        # TODO: Implement actual tracking when REVENUE_TRACKER.csv and time tracking exist

        methods = [
            ("APP_FACTORY", "$0", "15h", "$0", "0%", "→"),
            ("COLD_OUTBOUND", "$0", "8h", "$0", "0%", "→"),
            ("CONTENT_FARM", "$0", "12h", "$0", "0%", "→"),
            ("AI_INFLUENCER", "$0", "10h", "$0", "0%", "→"),
        ]

        for method, rev, time, rate, win, trend in methods:
            trend_style = "green" if trend == "↗" else "red" if trend == "↘" else "white"
            table.add_row(
                method,
                rev,
                time,
                rate,
                win,
                Text(trend, style=trend_style)
            )


class AgentActivityPanel(Static):
    """Running agents with live progress"""

    def compose(self) -> ComposeResult:
        yield Static("🤖 Agent Activity", classes="panel-title")
        yield DataTable(id="agents-table")

    def on_mount(self) -> None:
        table = self.query_one("#agents-table", DataTable)
        table.add_columns("Agent", "Status", "Progress", "Active")
        self.load_agents()

    def load_agents(self) -> None:
        """Load running agents from task directory"""
        table = self.query_one("#agents-table", DataTable)
        table.clear()

        if not TASK_DIR.exists():
            table.add_row("No tasks directory", "", "", "")
            return

        agents = []
        for task_file in TASK_DIR.glob("*.output"):
            task_id = task_file.stem
            size = task_file.stat().st_size
            modified = datetime.fromtimestamp(task_file.stat().st_mtime)
            age_seconds = (datetime.now() - modified).seconds

            try:
                with open(task_file, 'r') as f:
                    lines = f.readlines()
                    last_lines = lines[-50:] if len(lines) > 50 else lines

                progress = self._estimate_progress(last_lines)
                status = self._parse_status(last_lines)
                active = "🟢" if age_seconds < 30 else "🔴"

                agents.append((task_id[:12], status, f"{progress}%", active))
            except:
                continue

        if not agents:
            table.add_row("No active agents", "", "", "")
        else:
            for agent in agents[:10]:  # Show last 10
                table.add_row(*agent)

    def _estimate_progress(self, lines: List[str]) -> int:
        """Estimate progress from output lines"""
        text = ''.join(lines).lower()

        if 'complete' in text or 'finished' in text:
            return 100
        elif 'error' in text or 'failed' in text:
            return -1
        elif 'processing' in text:
            return 50
        else:
            return 25

    def _parse_status(self, lines: List[str]) -> str:
        """Parse status from recent output"""
        text = ''.join(lines[-10:]).lower()

        if 'complete' in text:
            return "COMPLETE"
        elif 'error' in text or 'failed' in text:
            return "ERROR"
        elif 'processing' in text:
            return "PROCESSING"
        else:
            return "RUNNING"


class PortfolioPanel(Static):
    """Portfolio view - diversification and capital allocation"""

    def compose(self) -> ComposeResult:
        yield Static("💼 Portfolio View", classes="panel-title")
        yield DataTable(id="portfolio-table")

    def on_mount(self) -> None:
        table = self.query_one("#portfolio-table", DataTable)
        table.add_columns("Method", "Capital", "Revenue %", "Risk", "Status")
        self.load_portfolio()

    def load_portfolio(self) -> None:
        """Load portfolio allocation"""
        table = self.query_one("#portfolio-table", DataTable)
        table.clear()

        # Placeholder data - will track actual capital allocation
        portfolio = [
            ("APP_FACTORY", "$200", "0%", "Medium", "Building"),
            ("CONTENT_FARM", "$100", "0%", "Low", "Planning"),
            ("COLD_OUTBOUND", "$150", "0%", "Low", "Planning"),
            ("AI_INFLUENCER", "$100", "0%", "Medium", "Planning"),
        ]

        for method, capital, rev_pct, risk, status in portfolio:
            risk_style = "red" if risk == "High" else "yellow" if risk == "Medium" else "green"
            table.add_row(
                method,
                capital,
                rev_pct,
                Text(risk, style=risk_style),
                status
            )


class BacktestPanel(Static):
    """Backtest results for alpha validation - reads from BACKTEST_RESULTS.csv"""

    def compose(self) -> ComposeResult:
        yield Static("🔬 Backtest Results", classes="panel-title")
        yield DataTable(id="backtest-table")

    def on_mount(self) -> None:
        table = self.query_one("#backtest-table", DataTable)
        table.add_columns("Alpha ID", "Score", "Category", "Valid 2026", "Decision")
        self.load_backtests()

    def load_backtests(self) -> None:
        """Load backtest results from BACKTEST_RESULTS.csv"""
        table = self.query_one("#backtest-table", DataTable)
        table.clear()

        backtest_file = LEDGER_DIR / "BACKTESTS" / "BACKTEST_RESULTS.csv"

        if not backtest_file.exists():
            table.add_row("No backtest data", "", "", "", "")
            return

        try:
            with open(backtest_file, 'r') as f:
                reader = csv.DictReader(f)
                entries = list(reader)

            # Show SCALE decisions first, then recent entries
            scale_entries = [e for e in entries if e.get('decision') == 'SCALE']
            paper_trade_entries = [e for e in entries if e.get('decision') == 'PAPER_TRADE']

            # Combine: SCALE first, then PAPER_TRADE, limit to 15
            display_entries = (scale_entries[:5] + paper_trade_entries[:5] + entries[-5:])[:15]

            for entry in display_entries:
                alpha_id = entry.get('alpha_id', 'N/A')
                try:
                    score = int(entry.get('backtest_score', 0) or 0)
                except:
                    score = 0
                category = entry.get('category', 'N/A')[:15]
                valid_2026 = entry.get('still_valid_2026', 'N/A')
                decision = entry.get('decision', 'N/A')

                # Color coding
                score_style = "green" if score >= 70 else "yellow" if score >= 50 else "red"
                decision_style = "green" if decision == "SCALE" else "yellow" if decision == "PAPER_TRADE" else "red"

                table.add_row(
                    alpha_id[:12],
                    Text(str(score), style=score_style),
                    category,
                    str(valid_2026),
                    Text(decision, style=decision_style)
                )
        except Exception as e:
            table.add_row("ERROR", str(e)[:20], "", "", "")


class AlertsPanel(Static):
    """Alerts and notifications - integrates with portfolio rebalancer"""

    def compose(self) -> ComposeResult:
        yield Static("🚨 Rebalance Alerts", classes="panel-title")
        yield Log(id="alerts-log")

    def on_mount(self) -> None:
        self.load_alerts()

    def load_alerts(self) -> None:
        """Load alerts from REBALANCE_RECOMMENDATIONS.csv"""
        log = self.query_one("#alerts-log", Log)
        log.clear()

        rebalance_file = LEDGER_DIR / "REBALANCE_RECOMMENDATIONS.csv"

        if not rebalance_file.exists():
            log.write_line("No rebalance recommendations yet")
            log.write_line("Run: python3 AUTOMATIONS/portfolio_rebalancer.py")
            return

        try:
            with open(rebalance_file, 'r') as f:
                reader = csv.DictReader(f)
                recommendations = list(reader)

            if not recommendations:
                log.write_line("No active recommendations")
                return

            # Group by action type
            for rec in recommendations:
                action = rec.get('action', 'UNKNOWN')
                method = rec.get('method_name', 'Unknown')[:25]
                reason = rec.get('reason', '')[:40]
                priority = rec.get('priority', 'LOW')

                # Color code by action
                if action == 'KILL':
                    log.write_line(f"🔴 KILL: {method}")
                    log.write_line(f"   {reason}")
                elif action == 'SCALE':
                    log.write_line(f"🟢 SCALE 2x: {method}")
                    log.write_line(f"   {reason}")
                elif action == 'REDUCE':
                    log.write_line(f"🟡 REDUCE: {method}")
                    log.write_line(f"   {reason}")
                elif action == 'ADD':
                    log.write_line(f"🟢 ADD: {method}")
                    log.write_line(f"   {reason}")
                else:
                    log.write_line(f"⚪ {action}: {method}")

            # Add timestamp
            try:
                mtime = rebalance_file.stat().st_mtime
                last_run = datetime.fromtimestamp(mtime)
                age = datetime.now() - last_run
                if age.total_seconds() < 3600:
                    age_str = f"{int(age.total_seconds() / 60)}m ago"
                elif age.total_seconds() < 86400:
                    age_str = f"{int(age.total_seconds() / 3600)}h ago"
                else:
                    age_str = f"{int(age.total_seconds() / 86400)}d ago"
                log.write_line(f"───────────────────────")
                log.write_line(f"Last rebalance: {age_str}")
            except:
                pass

        except Exception as e:
            log.write_line(f"Error loading recommendations: {str(e)}")


class QuantDashboard(App):
    """PRINTMAXX Quant Infrastructure Dashboard"""

    CSS = """
    Screen {
        background: $surface;
    }

    .panel-title {
        background: $boost;
        color: $text;
        padding: 1;
        text-align: center;
        text-style: bold;
    }

    DataTable {
        height: 100%;
    }

    Log {
        height: 100%;
        border: solid $primary;
    }

    #top-row {
        height: 40%;
    }

    #middle-row {
        height: 30%;
    }

    #bottom-row {
        height: 30%;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        # Top row: Alpha Discovery + Method Performance
        with Horizontal(id="top-row"):
            yield AlphaDiscoveryPanel()
            yield MethodPerformancePanel()

        # Middle row: Agent Activity + Portfolio
        with Horizontal(id="middle-row"):
            yield AgentActivityPanel()
            yield PortfolioPanel()

        # Bottom row: Backtests + Alerts
        with Horizontal(id="bottom-row"):
            yield BacktestPanel()
            yield AlertsPanel()

        yield Footer()

    def action_refresh(self) -> None:
        """Refresh all panels"""
        # Reload all panels
        for panel in self.query(AlphaDiscoveryPanel):
            panel.load_alpha()
        for panel in self.query(MethodPerformancePanel):
            panel.load_methods()
        for panel in self.query(AgentActivityPanel):
            panel.load_agents()
        for panel in self.query(PortfolioPanel):
            panel.load_portfolio()
        for panel in self.query(BacktestPanel):
            panel.load_backtests()
        for panel in self.query(AlertsPanel):
            panel.load_alerts()

    def on_mount(self) -> None:
        """Set up auto-refresh"""
        self.set_interval(5, self.action_refresh)  # Refresh every 5 seconds


if __name__ == "__main__":
    app = QuantDashboard()
    app.run()
