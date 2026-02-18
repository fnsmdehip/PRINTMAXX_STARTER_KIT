#!/usr/bin/env python3
"""
Live Agent Progress Monitor - Jane Street Style
Real-time dashboard for all running agents and tasks

Usage:
    python3 agent_monitor.py

Monitors:
- Running agents (from /private/tmp/claude tasks)
- Ralph loops
- ALPHA_STAGING.csv growth
- Method performance
- Cross-pollination discovery
"""

import os
import time
import json
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.text import Text

console = Console()

# Paths
TASK_DIR = Path("/private/tmp/claude-501/-Users-macbookpro-Documents-p-PRINTMAXX-STARTER-KITttttt/tasks")
PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
ALPHA_STAGING = PROJECT_DIR / "LEDGER/ALPHA_STAGING.csv"
RALPH_DIR = PROJECT_DIR / "ralph/loops/mega"

class AgentMonitor:
    def __init__(self):
        self.start_time = datetime.now()

    def get_running_agents(self):
        """Get all running agent tasks"""
        agents = []
        if not TASK_DIR.exists():
            return agents

        for task_file in TASK_DIR.glob("*.output"):
            task_id = task_file.stem

            # Get file size and last modified
            size = task_file.stat().st_size
            modified = datetime.fromtimestamp(task_file.stat().st_mtime)

            # Read last 50 lines for status
            try:
                with open(task_file, 'r') as f:
                    lines = f.readlines()
                    last_lines = lines[-50:] if len(lines) > 50 else lines

                # Estimate progress from output
                progress = self.estimate_progress(last_lines)
                status = self.parse_status(last_lines)

                agents.append({
                    'id': task_id,
                    'size': size,
                    'modified': modified,
                    'progress': progress,
                    'status': status,
                    'active': (datetime.now() - modified).seconds < 30
                })
            except Exception as e:
                continue

        return agents

    def estimate_progress(self, lines):
        """Estimate progress from output lines"""
        text = ''.join(lines).lower()

        # Look for progress indicators
        if 'complete' in text or 'finished' in text:
            return 100
        elif 'error' in text or 'failed' in text:
            return -1
        elif 'processing' in text or 'extracting' in text:
            # Try to find numbers like "5/10" or "50%"
            import re
            matches = re.findall(r'(\d+)/(\d+)', text)
            if matches:
                current, total = map(int, matches[-1])
                return int((current / total) * 100)

            percent_matches = re.findall(r'(\d+)%', text)
            if percent_matches:
                return int(percent_matches[-1])

            # Default mid-progress
            return 50
        else:
            return 25

    def parse_status(self, lines):
        """Parse status from recent output"""
        text = ''.join(lines[-10:])

        if 'complete' in text.lower():
            return 'COMPLETE'
        elif 'error' in text.lower() or 'failed' in text.lower():
            return 'ERROR'
        elif 'processing' in text.lower():
            return 'PROCESSING'
        else:
            return 'RUNNING'

    def get_alpha_stats(self):
        """Get ALPHA_STAGING.csv stats"""
        if not ALPHA_STAGING.exists():
            return {'total': 0, 'pending': 0, 'approved': 0}

        total = 0
        pending = 0
        approved = 0

        with open(ALPHA_STAGING, 'r') as f:
            for line in f:
                total += 1
                if 'PENDING_REVIEW' in line:
                    pending += 1
                elif 'APPROVED' in line:
                    approved += 1

        return {
            'total': total - 1,  # Subtract header
            'pending': pending,
            'approved': approved
        }

    def get_ralph_status(self):
        """Get ralph loop status"""
        progress_file = RALPH_DIR / ".ralph/progress.md"

        if not progress_file.exists():
            return None

        with open(progress_file, 'r') as f:
            content = f.read()

        # Parse progress
        import re
        iteration_match = re.search(r'Iteration (\d+)/(\d+)', content)
        phase_match = re.search(r'Current phase: (\w+)', content)

        if iteration_match and phase_match:
            current, total = map(int, iteration_match.groups())
            phase = phase_match.group(1)

            return {
                'iteration': current,
                'total': total,
                'phase': phase,
                'progress': int((current / total) * 100)
            }

        return None

    def create_dashboard(self):
        """Create dashboard layout"""
        layout = Layout()

        # Split into sections
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )

        layout["main"].split_row(
            Layout(name="agents"),
            Layout(name="stats")
        )

        # Header
        header_text = Text("PRINTMAXX Agent Monitor", style="bold magenta")
        header_text.append(" | ", style="white")
        header_text.append(f"Runtime: {(datetime.now() - self.start_time).seconds}s", style="cyan")
        layout["header"].update(Panel(header_text, border_style="magenta"))

        # Agents table
        agents = self.get_running_agents()
        agent_table = Table(title="Running Agents", show_header=True)
        agent_table.add_column("ID", style="cyan")
        agent_table.add_column("Status", style="green")
        agent_table.add_column("Progress", style="yellow")
        agent_table.add_column("Active", style="white")

        for agent in agents:
            status_color = "green" if agent['status'] == 'COMPLETE' else "red" if agent['status'] == 'ERROR' else "yellow"
            active_icon = "🟢" if agent['active'] else "🔴"

            progress_bar = "█" * (agent['progress'] // 5) + "░" * (20 - agent['progress'] // 5)

            agent_table.add_row(
                agent['id'][:8],
                f"[{status_color}]{agent['status']}[/{status_color}]",
                f"{progress_bar} {agent['progress']}%",
                active_icon
            )

        layout["agents"].update(Panel(agent_table, border_style="cyan"))

        # Stats panel
        alpha_stats = self.get_alpha_stats()
        ralph_status = self.get_ralph_status()

        stats_table = Table(show_header=False, box=None)
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")

        stats_table.add_row("Alpha Entries", str(alpha_stats['total']))
        stats_table.add_row("Pending Review", str(alpha_stats['pending']))
        stats_table.add_row("Approved", str(alpha_stats['approved']))

        if ralph_status:
            stats_table.add_row("", "")
            stats_table.add_row("Ralph Iteration", f"{ralph_status['iteration']}/{ralph_status['total']}")
            stats_table.add_row("Current Phase", ralph_status['phase'])
            stats_table.add_row("Ralph Progress", f"{ralph_status['progress']}%")

        layout["stats"].update(Panel(stats_table, title="Stats", border_style="green"))

        # Footer
        footer_text = Text("Press Ctrl+C to exit", style="dim")
        layout["footer"].update(Panel(footer_text, border_style="dim"))

        return layout

    def run(self):
        """Run live monitor"""
        console.clear()

        with Live(self.create_dashboard(), refresh_per_second=2, console=console) as live:
            try:
                while True:
                    time.sleep(0.5)
                    live.update(self.create_dashboard())
            except KeyboardInterrupt:
                console.print("\n[yellow]Monitor stopped[/yellow]")

if __name__ == "__main__":
    monitor = AgentMonitor()
    monitor.run()
