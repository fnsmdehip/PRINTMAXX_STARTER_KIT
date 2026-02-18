#!/usr/bin/env python3
"""
Real-Time Ralph Loop Progress Monitor

Reads actual .ralph/progress.md files from all running loops
and displays live progress bars that update as work completes.
"""

import os
import re
import time
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.layout import Layout

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LOOPS_DIR = PROJECT_DIR / "ralph" / "loops"

console = Console()

LOOPS = [
    "niche_meta_detection",
    "comprehensive_alpha_research",
    "synergy_package_builder",
    "retardmaxx_execution",
    "meme_coin_backtest"
]

def parse_progress_file(loop_name):
    """Parse .ralph/progress.md and extract progress metrics."""
    progress_file = LOOPS_DIR / loop_name / ".ralph" / "progress.md"

    if not progress_file.exists():
        return {
            "status": "NOT_STARTED",
            "completed": 0,
            "total": 50,
            "current_task": "Waiting to start",
            "details": []
        }

    content = progress_file.read_text()

    # Extract status
    status_match = re.search(r'Status[:\s]+(\w+)', content, re.IGNORECASE)
    status = status_match.group(1) if status_match else "RUNNING"

    # Count completed checkboxes vs total checkboxes
    total_checkboxes = len(re.findall(r'- \[[ x]\]', content))
    completed_checkboxes = len(re.findall(r'- \[x\]', content, re.IGNORECASE))

    # Extract counts
    counts = {}
    for match in re.finditer(r'Count:\s*(\d+)', content):
        counts[match.start()] = int(match.group(1))

    # Sum all counts for progress
    total_count = sum(counts.values()) if counts else completed_checkboxes

    # Extract current task
    current_task = "Working..."
    if "Next" in content:
        next_match = re.search(r'Next[^:\n]*[:]\s*([^\n]+)', content)
        if next_match:
            current_task = next_match.group(1).strip()

    # Extract details (counts, patterns, etc)
    details = []

    # Niches scanned
    if "Niches Scanned" in content:
        niches = re.findall(r'N\d{3}', content)
        if niches:
            details.append(f"Niches: {len(niches)} scanned")

    # Alpha entries
    if "Alpha Entries" in content:
        alpha_match = re.search(r'Alpha Entries[^:]*:\s*(\d+)', content)
        if alpha_match:
            details.append(f"Alpha: {alpha_match.group(1)} entries")

    # Metas detected
    if "Metas Detected" in content:
        meta_match = re.search(r'Metas Detected[^:]*:\s*(\d+)', content)
        if meta_match:
            details.append(f"Metas: {meta_match.group(1)} detected")

    # Synergies found
    if "High-Synergy" in content:
        syn_match = re.search(r'High-Synergy[^:]*:\s*(\d+)', content)
        if syn_match:
            details.append(f"Synergies: {syn_match.group(1)} (90+)")

    # Deliverables
    if "Deliverables" in content:
        del_match = re.search(r'Deliverables[^:]*:\s*(\d+)', content)
        if del_match:
            details.append(f"Deliverables: {del_match.group(1)} created")

    # Backtests
    if "Backtests Completed" in content:
        back_match = re.search(r'Backtests Completed[^:]*:\s*(\d+)', content)
        if back_match:
            details.append(f"Backtests: {back_match.group(1)} done")

    # Calculate progress percentage
    if total_checkboxes > 0:
        progress_pct = (completed_checkboxes / total_checkboxes) * 100
    elif total_count > 0:
        progress_pct = min((total_count / 50) * 100, 100)  # Assume max 50 items per loop
    else:
        progress_pct = 0

    return {
        "status": status,
        "completed": total_count or completed_checkboxes,
        "total": 50,
        "progress_pct": progress_pct,
        "current_task": current_task,
        "details": details
    }

def check_if_loop_running(loop_name):
    """Check if a loop is actually running by looking for its process."""
    import subprocess
    try:
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True,
            text=True
        )
        return f"loops/{loop_name}" in result.stdout
    except:
        return False

def create_progress_table():
    """Create a rich table with all loop progress."""
    table = Table(
        show_header=True,
        header_style="bold cyan",
        title="🔥 PRINTMAXX Ralph Loops - Live Progress 🔥",
        title_style="bold magenta"
    )

    table.add_column("Loop", style="cyan", width=25)
    table.add_column("Status", width=12)
    table.add_column("Progress", width=40)
    table.add_column("Current Task", width=30)
    table.add_column("Details", width=25)

    for loop_name in LOOPS:
        data = parse_progress_file(loop_name)
        is_running = check_if_loop_running(loop_name)

        # Status with color
        if data["status"] == "COMPLETE":
            status_str = "[green]✓ COMPLETE[/green]"
        elif data["status"] == "RUNNING" and is_running:
            status_str = "[yellow]⚡ RUNNING[/yellow]"
        elif not is_running:
            status_str = "[red]⚠ STOPPED[/red]"
        else:
            status_str = f"[white]{data['status']}[/white]"

        # Progress bar
        pct = data["progress_pct"]
        bar_width = 30
        filled = int((pct / 100) * bar_width)
        bar = "█" * filled + "░" * (bar_width - filled)

        if pct >= 100:
            bar_color = "green"
        elif pct >= 50:
            bar_color = "yellow"
        else:
            bar_color = "cyan"

        progress_str = f"[{bar_color}]{bar}[/{bar_color}] {pct:.0f}%"

        # Current task (truncate if too long)
        task = data["current_task"][:28] + "..." if len(data["current_task"]) > 30 else data["current_task"]

        # Details
        details_str = "\n".join(data["details"][:3])  # Max 3 details

        table.add_row(
            loop_name.replace("_", " ").title(),
            status_str,
            progress_str,
            task,
            details_str
        )

    return table

def get_summary_stats():
    """Get overall summary statistics."""
    stats = {
        "total_loops": len(LOOPS),
        "running": 0,
        "complete": 0,
        "total_items": 0
    }

    for loop_name in LOOPS:
        data = parse_progress_file(loop_name)
        is_running = check_if_loop_running(loop_name)

        if data["status"] == "COMPLETE":
            stats["complete"] += 1
        elif is_running:
            stats["running"] += 1

        stats["total_items"] += data["completed"]

    return stats

def create_summary_panel():
    """Create summary panel with overall stats."""
    stats = get_summary_stats()

    summary = f"""
[bold cyan]Total Loops:[/bold cyan] {stats['total_loops']}
[bold yellow]Running:[/bold yellow] {stats['running']}
[bold green]Complete:[/bold green] {stats['complete']}
[bold magenta]Total Items Processed:[/bold magenta] {stats['total_items']}

[dim]Last updated: {datetime.now().strftime('%H:%M:%S')}[/dim]
"""

    return Panel(
        summary,
        title="📊 Summary",
        border_style="cyan"
    )

def main():
    """Main monitoring loop."""
    console.clear()

    console.print("\n[bold cyan]PRINTMAXX Ralph Loop Progress Monitor[/bold cyan]")
    console.print("[dim]Press Ctrl+C to exit[/dim]\n")

    try:
        with Live(console=console, refresh_per_second=2) as live:
            while True:
                # Create layout
                layout = Layout()
                layout.split_column(
                    Layout(name="summary", size=8),
                    Layout(name="progress")
                )

                layout["summary"].update(create_summary_panel())
                layout["progress"].update(create_progress_table())

                live.update(layout)
                time.sleep(2)

    except KeyboardInterrupt:
        console.print("\n[yellow]Monitoring stopped[/yellow]")
        console.print("\n[cyan]Final Progress:[/cyan]")
        console.print(create_progress_table())
        console.print("\n[dim]Check individual progress files:[/dim]")
        for loop in LOOPS:
            progress_file = LOOPS_DIR / loop / ".ralph" / "progress.md"
            console.print(f"  cat {progress_file}")

if __name__ == "__main__":
    main()
