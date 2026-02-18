#!/usr/bin/env python3
"""
PRINTMAXX Mega Ralph Tracker Dashboard
========================================
Reads LEDGER/MEGA_RALPH_TRACKER.csv and ralph loop state files to generate
a summary dashboard with task completion stats, findings count, quality scores,
and phase progress.

Usage:
    python3 generate_dashboard.py                    # Full dashboard
    python3 generate_dashboard.py --phase EXECUTION  # Filter by phase
    python3 generate_dashboard.py --day-cycle 1      # Filter by day cycle
    python3 generate_dashboard.py --compact           # Short summary only

Output: ralph/loops/mega/output/dashboard_summary.md
"""

import csv
import os
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MEGA_TRACKER_CSV = PROJECT_ROOT / "LEDGER" / "MEGA_RALPH_TRACKER.csv"
MEGA_LOOP_DIR = PROJECT_ROOT / "ralph" / "loops" / "mega"
PROGRESS_FILE = MEGA_LOOP_DIR / ".ralph" / "progress.md"
PRIORITIES_FILE = MEGA_LOOP_DIR / ".ralph" / "priorities.md"
GUARDRAILS_FILE = MEGA_LOOP_DIR / ".ralph" / "guardrails.md"
ACTIVITY_LOG = MEGA_LOOP_DIR / ".ralph" / "activity.log"
ERRORS_LOG = MEGA_LOOP_DIR / ".ralph" / "errors.log"
CHECKPOINTS_DIR = MEGA_LOOP_DIR / "checkpoints"
OUTPUT_FILE = MEGA_LOOP_DIR / "output" / "dashboard_summary.md"


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def load_tracker() -> list:
    """Load mega ralph tracker entries."""
    entries = []
    if not MEGA_TRACKER_CSV.exists():
        log(f"Tracker not found: {MEGA_TRACKER_CSV}")
        return entries

    with open(MEGA_TRACKER_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(row)

    return entries


def read_file_safe(filepath: Path) -> str:
    """Read file contents or return empty string."""
    if filepath.exists():
        try:
            return filepath.read_text(encoding="utf-8")
        except Exception:
            return ""
    return ""


def count_checkpoint_items() -> dict:
    """Count pending items in checkpoint files."""
    counts = {}
    if not CHECKPOINTS_DIR.exists():
        return counts

    for cp_file in CHECKPOINTS_DIR.glob("PENDING_*.md"):
        content = read_file_safe(cp_file)
        # Count non-empty, non-header lines (rough item count)
        lines = [l for l in content.strip().split("\n")
                 if l.strip() and not l.startswith("#") and not l.startswith("---")]
        counts[cp_file.stem] = len(lines)

    return counts


def analyze_tasks(entries: list) -> dict:
    """Analyze task data from tracker."""
    stats = {
        "total": len(entries),
        "completed": 0,
        "in_progress": 0,
        "pending": 0,
        "blocked": 0,
        "by_phase": {},
        "by_category": {},
        "by_day_cycle": {},
        "by_status": {},
        "total_findings": 0,
        "total_duration": 0,
        "quality_scores": [],
        "priority_scores": [],
    }

    for entry in entries:
        status = entry.get("status", "PENDING").upper()
        phase = entry.get("phase", "UNKNOWN")
        category = entry.get("category", "UNKNOWN")
        day_cycle = entry.get("day_cycle", "0")

        # Status counts
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        if status == "COMPLETED":
            stats["completed"] += 1
        elif status in ("IN_PROGRESS", "RUNNING"):
            stats["in_progress"] += 1
        elif status == "BLOCKED":
            stats["blocked"] += 1
        else:
            stats["pending"] += 1

        # Phase breakdown
        if phase not in stats["by_phase"]:
            stats["by_phase"][phase] = {"total": 0, "completed": 0, "pending": 0}
        stats["by_phase"][phase]["total"] += 1
        if status == "COMPLETED":
            stats["by_phase"][phase]["completed"] += 1
        else:
            stats["by_phase"][phase]["pending"] += 1

        # Category breakdown
        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1

        # Day cycle breakdown
        stats["by_day_cycle"][day_cycle] = stats["by_day_cycle"].get(day_cycle, 0) + 1

        # Numeric fields
        try:
            findings = int(entry.get("findings_count", "0") or "0")
            stats["total_findings"] += findings
        except ValueError:
            pass

        try:
            duration = float(entry.get("duration_mins", "0") or "0")
            stats["total_duration"] += duration
        except ValueError:
            pass

        try:
            quality = float(entry.get("quality_score", "0") or "0")
            if quality > 0:
                stats["quality_scores"].append(quality)
        except ValueError:
            pass

        try:
            priority = float(entry.get("priority_score", "0") or "0")
            if priority > 0:
                stats["priority_scores"].append(priority)
        except ValueError:
            pass

    return stats


def generate_dashboard(
    entries: list,
    phase_filter: str = "",
    day_cycle_filter: str = "",
    compact: bool = False,
) -> str:
    """Generate the dashboard markdown."""

    # Apply filters
    filtered = entries
    if phase_filter:
        filtered = [e for e in filtered if e.get("phase", "").upper() == phase_filter.upper()]
    if day_cycle_filter:
        filtered = [e for e in filtered if e.get("day_cycle", "") == day_cycle_filter]

    stats = analyze_tasks(filtered)
    checkpoint_items = count_checkpoint_items()

    # Read state files
    progress_content = read_file_safe(PROGRESS_FILE)
    priorities_content = read_file_safe(PRIORITIES_FILE)

    # Count errors
    errors_content = read_file_safe(ERRORS_LOG)
    error_count = len([l for l in errors_content.split("\n") if l.strip()]) if errors_content else 0

    # Count activity log lines
    activity_content = read_file_safe(ACTIVITY_LOG)
    activity_count = len([l for l in activity_content.split("\n") if l.strip()]) if activity_content else 0

    lines = [
        "# MEGA RALPH LOOP DASHBOARD",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    ]

    if phase_filter:
        lines.append(f"**Filter:** Phase = {phase_filter}")
    if day_cycle_filter:
        lines.append(f"**Filter:** Day Cycle = {day_cycle_filter}")

    lines.append("")

    if compact:
        # Short summary
        completion_pct = (stats["completed"] / max(stats["total"], 1)) * 100
        avg_quality = sum(stats["quality_scores"]) / max(len(stats["quality_scores"]), 1)
        lines.extend([
            f"Tasks: {stats['completed']}/{stats['total']} ({completion_pct:.0f}%)",
            f"Findings: {stats['total_findings']}",
            f"Avg Quality: {avg_quality:.1f}/10",
            f"Errors: {error_count}",
            f"Checkpoints: {sum(checkpoint_items.values())} pending",
        ])
        return "\n".join(lines)

    # Full dashboard
    lines.append("---")
    lines.append("")

    # Overview Cards
    completion_pct = (stats["completed"] / max(stats["total"], 1)) * 100
    avg_quality = sum(stats["quality_scores"]) / max(len(stats["quality_scores"]), 1)
    avg_priority = sum(stats["priority_scores"]) / max(len(stats["priority_scores"]), 1)

    lines.extend([
        "## Overview",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total Tasks | {stats['total']} |",
        f"| Completed | {stats['completed']} ({completion_pct:.0f}%) |",
        f"| In Progress | {stats['in_progress']} |",
        f"| Pending | {stats['pending']} |",
        f"| Blocked | {stats['blocked']} |",
        f"| Total Findings | {stats['total_findings']} |",
        f"| Total Duration | {stats['total_duration']:.0f} min |",
        f"| Avg Quality Score | {avg_quality:.1f}/10 |",
        f"| Avg Priority Score | {avg_priority:.1f}/10 |",
        f"| Activity Log Entries | {activity_count} |",
        f"| Errors Logged | {error_count} |",
        "",
    ])

    # Progress Bar (visual)
    bar_length = 30
    filled = int(bar_length * completion_pct / 100)
    bar = "#" * filled + "-" * (bar_length - filled)
    lines.extend([
        f"### Completion Progress",
        f"```",
        f"[{bar}] {completion_pct:.0f}%",
        f"```",
        "",
    ])

    # Phase Breakdown
    lines.extend([
        "## Phase Breakdown",
        "",
        "| Phase | Total | Completed | Pending | Completion |",
        "|-------|-------|-----------|---------|------------|",
    ])

    phase_order = ["DAILY_RESEARCH", "REFLECTION", "CONTENT_GENERATION", "EXECUTION", "INTELLIGENCE", "CHECKPOINT"]
    for phase in phase_order:
        if phase in stats["by_phase"]:
            p = stats["by_phase"][phase]
            pct = (p["completed"] / max(p["total"], 1)) * 100
            lines.append(f"| {phase} | {p['total']} | {p['completed']} | {p['pending']} | {pct:.0f}% |")

    # Also show any phases not in the standard order
    for phase, p in stats["by_phase"].items():
        if phase not in phase_order:
            pct = (p["completed"] / max(p["total"], 1)) * 100
            lines.append(f"| {phase} | {p['total']} | {p['completed']} | {p['pending']} | {pct:.0f}% |")

    lines.append("")

    # Category Breakdown
    lines.extend([
        "## Category Breakdown",
        "",
        "| Category | Tasks |",
        "|----------|-------|",
    ])
    for category, count in sorted(stats["by_category"].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {category} | {count} |")
    lines.append("")

    # Human Checkpoints
    lines.extend([
        "## Human Checkpoints (Action Required)",
        "",
    ])
    if checkpoint_items:
        lines.append("| Checkpoint | Pending Items |")
        lines.append("|-----------|---------------|")
        for name, count in sorted(checkpoint_items.items()):
            display_name = name.replace("PENDING_", "").replace("_", " ").title()
            lines.append(f"| {display_name} | {count} |")
        lines.append("")
        total_pending = sum(checkpoint_items.values())
        if total_pending > 0:
            lines.append(f"**Action needed:** {total_pending} items awaiting human review.")
            lines.append(f"Check: `ralph/loops/mega/checkpoints/`")
    else:
        lines.append("No pending checkpoint items.")
    lines.append("")

    # Recent Tasks (last 10 by task_id)
    lines.extend([
        "## Recent Tasks",
        "",
    ])
    recent = sorted(filtered, key=lambda x: x.get("task_id", ""), reverse=True)[:10]
    if recent:
        lines.append("| Task ID | Phase | Category | Status | Priority | Notes |")
        lines.append("|---------|-------|----------|--------|----------|-------|")
        for task in recent:
            notes = (task.get("notes", "") or "")[:40]
            lines.append(
                f"| {task.get('task_id', '')} | {task.get('phase', '')} | "
                f"{task.get('category', '')} | {task.get('status', '')} | "
                f"{task.get('priority_score', '')} | {notes} |"
            )
    lines.append("")

    # Current Progress (from progress.md)
    if progress_content:
        lines.extend([
            "## Current Loop Progress",
            "",
            "```",
            progress_content[:500],
            "```",
            "",
        ])

    # Top Priorities (from priorities.md)
    if priorities_content:
        # Show first 10 lines
        priority_lines = priorities_content.strip().split("\n")[:15]
        lines.extend([
            "## Priority Queue (Top Items)",
            "",
        ])
        for pl in priority_lines:
            lines.append(pl)
        lines.append("")

    # Error Summary
    if error_count > 0:
        lines.extend([
            "## Error Summary",
            f"**Total errors:** {error_count}",
            "",
        ])
        # Show last 5 errors
        error_lines = errors_content.strip().split("\n")
        last_errors = error_lines[-5:] if len(error_lines) > 5 else error_lines
        lines.append("**Recent errors:**")
        for el in last_errors:
            if el.strip():
                lines.append(f"- {el.strip()[:100]}")
        lines.append("")

    # Efficiency Metrics
    if stats["completed"] > 0 and stats["total_duration"] > 0:
        avg_duration = stats["total_duration"] / stats["completed"]
        findings_per_hour = (stats["total_findings"] / stats["total_duration"]) * 60

        lines.extend([
            "## Efficiency Metrics",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Avg task duration | {avg_duration:.1f} min |",
            f"| Findings per hour | {findings_per_hour:.1f} |",
            f"| Tasks per day cycle | {stats['total'] / max(len(stats['by_day_cycle']), 1):.1f} |",
            "",
        ])

    # Footer
    lines.extend([
        "---",
        f"*Dashboard generated by PRINTMAXX Mega Ralph Dashboard Tool*",
        f"*Data source: LEDGER/MEGA_RALPH_TRACKER.csv*",
        f"*Loop state: ralph/loops/mega/.ralph/*",
    ])

    return "\n".join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="PRINTMAXX Mega Ralph Tracker Dashboard")
    parser.add_argument("--phase", default="", help="Filter by phase name")
    parser.add_argument("--day-cycle", default="", help="Filter by day cycle number")
    parser.add_argument("--compact", action="store_true", help="Short summary only")
    parser.add_argument("--output", default=None, help="Custom output path")
    args = parser.parse_args()

    log("PRINTMAXX Mega Ralph Tracker Dashboard starting")

    # Load data
    entries = load_tracker()
    log(f"Loaded {len(entries)} tracker entries")

    # Generate dashboard
    dashboard = generate_dashboard(
        entries,
        phase_filter=args.phase,
        day_cycle_filter=args.day_cycle,
        compact=args.compact,
    )

    # Print to stdout
    print(dashboard)

    # Save to file
    output_path = Path(args.output) if args.output else OUTPUT_FILE
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(dashboard, encoding="utf-8")
    log(f"Dashboard saved to {output_path}")

    log("Done.")


if __name__ == "__main__":
    main()
