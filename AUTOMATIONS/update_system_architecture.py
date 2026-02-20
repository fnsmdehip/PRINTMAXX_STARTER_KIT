#!/usr/bin/env python3
"""
PRINTMAXX System Architecture Auto-Updater

Regenerates the "Current State" sections of OPS/SYSTEM_ARCHITECTURE.md
whenever called. Wire into cron for weekly updates, or call manually
after any architectural change.

Usage:
    python3 AUTOMATIONS/update_system_architecture.py              # Full update
    python3 AUTOMATIONS/update_system_architecture.py --dry-run    # Show changes without writing
    python3 AUTOMATIONS/update_system_architecture.py --status     # Show current stats only
    python3 AUTOMATIONS/update_system_architecture.py --section state  # Update only "Current state" line

Cron entry (weekly Sunday 4 AM):
    0 4 * * 0 cd $BASE && $PYTHON AUTOMATIONS/update_system_architecture.py >> AUTOMATIONS/logs/arch_update.log 2>&1
"""

import os
import sys
import re
import json
import csv
import glob
import argparse
from pathlib import Path
from datetime import datetime, date
from collections import Counter

# --- Path Safety ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ARCH_DOC = PROJECT_ROOT / "OPS" / "SYSTEM_ARCHITECTURE.md"
HEARTBEAT = PROJECT_ROOT / "OPS" / "HEARTBEAT.md"
QUEUE_PATH = PROJECT_ROOT / "OPS" / "AUTONOMOUS_TASK_QUEUE.jsonl"
CONFIG_PATH = PROJECT_ROOT / "OPS" / "AUTONOMOUS_WORKER_CONFIG.yaml"
CRONTAB_V2 = PROJECT_ROOT / "AUTOMATIONS" / "crontab_printmaxx_v2.txt"
AUTOMATIONS_DIR = PROJECT_ROOT / "AUTOMATIONS"
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
OPS_DIR = PROJECT_ROOT / "OPS"


def safe_path(target: Path) -> Path:
    """Verify path is within project root."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


# ============================================================
# Data Collection Functions
# ============================================================

def count_automation_scripts() -> int:
    """Count .py files in AUTOMATIONS/ (top-level only, not subdirs)."""
    count = 0
    for f in AUTOMATIONS_DIR.iterdir():
        if f.is_file() and f.suffix == ".py":
            count += 1
    return count


def count_all_automation_scripts() -> int:
    """Count all .py files in AUTOMATIONS/ recursively."""
    return len(list(AUTOMATIONS_DIR.rglob("*.py")))


def count_cron_jobs() -> tuple:
    """Count active cron entries and total lines in crontab file."""
    if not CRONTAB_V2.exists():
        return 0, 0
    lines = CRONTAB_V2.read_text().splitlines()
    total_lines = len(lines)
    active = 0
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith("SHELL") \
                and not stripped.startswith("PATH") and not stripped.startswith("BASE") \
                and not stripped.startswith("PYTHON"):
            active += 1
    return active, total_lines


def count_queue_tasks() -> dict:
    """Count tasks in queue by status."""
    counts = Counter()
    if not QUEUE_PATH.exists():
        return dict(counts)
    for line in QUEUE_PATH.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            task = json.loads(line)
            counts[task.get("status", "UNKNOWN")] += 1
        except json.JSONDecodeError:
            counts["PARSE_ERROR"] += 1
    return dict(counts)


def count_pipelines() -> int:
    """Count pipeline definitions in workflow_wirer.py."""
    wirer = AUTOMATIONS_DIR / "workflow_wirer.py"
    if not wirer.exists():
        return 0
    content = wirer.read_text()
    # Count top-level keys in PIPELINES dict
    matches = re.findall(r'^\s+"(\w+)":\s*\{', content, re.MULTILINE)
    return len(matches)


def read_heartbeat() -> dict:
    """Parse HEARTBEAT.md into structured data."""
    data = {}
    if not HEARTBEAT.exists():
        return data
    for line in HEARTBEAT.read_text().splitlines():
        line = line.strip()
        if line.startswith("# HEARTBEAT"):
            # Extract timestamp
            match = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", line)
            if match:
                data["timestamp"] = match.group(0)
        elif line.startswith("Leads:"):
            data["leads_line"] = line
        elif line.startswith("Revenue:"):
            data["revenue_line"] = line
        elif line.startswith("Content:"):
            data["content_line"] = line
        elif line.startswith("Apps:"):
            data["apps_line"] = line
        elif line.startswith("Alpha:"):
            data["alpha_line"] = line
        elif line.startswith("Accounts:"):
            data["accounts_line"] = line
        elif line.startswith("Scripts:"):
            data["scripts_line"] = line
        elif line.startswith("Blocker:"):
            data["blocker_line"] = line
    return data


def count_ledger_csvs() -> int:
    """Count CSV files in LEDGER/."""
    if not LEDGER_DIR.exists():
        return 0
    return len(list(LEDGER_DIR.glob("*.csv")))


def count_ops_files() -> int:
    """Count .md files in OPS/."""
    if not OPS_DIR.exists():
        return 0
    return len(list(OPS_DIR.glob("*.md")))


def count_ventures() -> int:
    """Count VENTURE_ALPHA*.md files in OPS/."""
    if not OPS_DIR.exists():
        return 0
    return len(list(OPS_DIR.glob("VENTURE_ALPHA*.md")))


def count_money_methods() -> int:
    """Count subdirectories in MONEY_METHODS/."""
    mm_dir = PROJECT_ROOT / "MONEY_METHODS"
    if not mm_dir.exists():
        return 0
    return len([d for d in mm_dir.iterdir() if d.is_dir()])


def get_live_sites() -> int:
    """Count deployed sites from DEPLOY_LOG.md if it exists."""
    deploy_log = OPS_DIR / "DEPLOY_LOG.md"
    if not deploy_log.exists():
        return 0
    content = deploy_log.read_text()
    return content.count("surge.sh")


# ============================================================
# Summary Builder
# ============================================================

def build_stats_summary() -> dict:
    """Collect all system statistics."""
    heartbeat = read_heartbeat()
    queue = count_queue_tasks()
    active_cron, total_cron_lines = count_cron_jobs()

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": date.today().isoformat(),
        "automation_scripts": count_automation_scripts(),
        "automation_scripts_all": count_all_automation_scripts(),
        "cron_jobs_active": active_cron,
        "cron_lines_total": total_cron_lines,
        "queue_total": sum(queue.values()),
        "queue_pending": queue.get("PENDING", 0),
        "queue_done": queue.get("DONE", 0),
        "queue_failed": queue.get("FAILED", 0),
        "pipelines": count_pipelines(),
        "ledger_csvs": count_ledger_csvs(),
        "ops_files": count_ops_files(),
        "ventures": count_ventures(),
        "money_methods": count_money_methods(),
        "live_sites": get_live_sites(),
        "heartbeat": heartbeat,
    }


def format_stats(stats: dict) -> str:
    """Format stats as readable text."""
    hb = stats["heartbeat"]
    lines = [
        f"System Statistics (as of {stats['timestamp']})",
        f"  Automation scripts:  {stats['automation_scripts']} (top-level), {stats['automation_scripts_all']} (all)",
        f"  Cron jobs:           {stats['cron_jobs_active']} active ({stats['cron_lines_total']} lines)",
        f"  Task queue:          {stats['queue_total']} total, {stats['queue_pending']} pending, {stats['queue_done']} done, {stats['queue_failed']} failed",
        f"  Pipelines:           {stats['pipelines']}",
        f"  LEDGER CSVs:         {stats['ledger_csvs']}",
        f"  OPS files:           {stats['ops_files']}",
        f"  Ventures:            {stats['ventures']}",
        f"  Money methods:       {stats['money_methods']}",
        f"  Live sites:          {stats['live_sites']}",
        "",
        "From HEARTBEAT.md:",
    ]
    for key in ["leads_line", "revenue_line", "content_line", "apps_line",
                "alpha_line", "accounts_line", "scripts_line", "blocker_line"]:
        if key in hb:
            lines.append(f"  {hb[key]}")

    return "\n".join(lines)


# ============================================================
# Document Updater
# ============================================================

def update_architecture_doc(stats: dict, dry_run: bool = False) -> str:
    """Update SYSTEM_ARCHITECTURE.md with current statistics."""
    if not ARCH_DOC.exists():
        return "ERROR: SYSTEM_ARCHITECTURE.md not found at " + str(ARCH_DOC)

    content = ARCH_DOC.read_text()
    original = content
    changes = []

    # 1. Update "Last Updated" line
    old_pattern = r"(\*\*Last Updated:\*\*) \d{4}-\d{2}-\d{2}"
    new_value = f"\\1 {stats['date']}"
    if re.search(old_pattern, content):
        content = re.sub(old_pattern, new_value, content)
        changes.append("Updated 'Last Updated' date")

    # 2. Update "Current state" block in Section 1
    hb = stats["heartbeat"]
    state_lines = []
    for key in ["leads_line", "revenue_line", "content_line", "apps_line",
                "alpha_line", "accounts_line", "scripts_line", "blocker_line"]:
        if key in hb:
            state_lines.append(f"- {hb[key]}")

    if state_lines:
        # Add cron stats
        state_lines.append(
            f"- Cron: {stats['cron_lines_total']}-line crontab (v2), ~{stats['cron_jobs_active']} active jobs"
        )

        new_state_block = "\n".join(state_lines)

        # Find and replace the state block between the markers
        state_pattern = (
            r"(\*\*Current state\*\* \(from HEARTBEAT\.md\):\n)"
            r"((?:- .*\n)+)"
        )
        match = re.search(state_pattern, content)
        if match:
            content = content[:match.start(2)] + new_state_block + "\n" + content[match.end(2):]
            changes.append("Updated 'Current state' block from HEARTBEAT.md")

    # 3. Update automation script count in Section 6
    script_pattern = r"(\*\*Total automation scripts:\*\*) \d+ Python files"
    script_replacement = f"\\1 {stats['automation_scripts']} Python files"
    if re.search(script_pattern, content):
        content = re.sub(script_pattern, script_replacement, content)
        changes.append(f"Updated script count to {stats['automation_scripts']}")

    # 4. Update task queue count in Section 4
    queue_pattern = r"(\*\*Current state:\*\*) \d+ tasks"
    queue_replacement = f"\\1 {stats['queue_total']} tasks"
    if re.search(queue_pattern, content):
        content = re.sub(queue_pattern, queue_replacement, content)
        changes.append(f"Updated queue count to {stats['queue_total']}")

    # 5. Update cron line count in Section 9
    cron_pattern = r"(\*\*File:\*\* `AUTOMATIONS/crontab_printmaxx_v2\.txt` \()\d+ lines, ~\d+ active jobs\)"
    cron_replacement = f"\\g<1>{stats['cron_lines_total']} lines, ~{stats['cron_jobs_active']} active jobs)"
    if re.search(cron_pattern, content):
        content = re.sub(cron_pattern, cron_replacement, content)
        changes.append(f"Updated cron stats to {stats['cron_lines_total']} lines, {stats['cron_jobs_active']} active")

    # 6. Update pipeline count in Section 4.2
    pipeline_pattern = r"Defines \d+ pipelines with \d+\+ tasks"
    pipeline_replacement = f"Defines {stats['pipelines']} pipelines with {stats['queue_total']}+ tasks"
    if re.search(pipeline_pattern, content):
        content = re.sub(pipeline_pattern, pipeline_replacement, content)
        changes.append(f"Updated pipeline count to {stats['pipelines']}")

    if content == original:
        return "No changes needed. Architecture doc is up to date."

    if dry_run:
        result = "DRY RUN - Changes that would be made:\n"
        for c in changes:
            result += f"  - {c}\n"
        return result

    # Write the updated content
    safe_path(ARCH_DOC)
    ARCH_DOC.write_text(content)

    result = f"Updated SYSTEM_ARCHITECTURE.md ({len(changes)} changes):\n"
    for c in changes:
        result += f"  - {c}\n"
    return result


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX System Architecture Auto-Updater"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show changes without writing"
    )
    parser.add_argument(
        "--status", action="store_true",
        help="Show current system stats only"
    )
    parser.add_argument(
        "--section", type=str, default=None,
        choices=["state", "scripts", "cron", "queue", "all"],
        help="Update specific section (default: all)"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output stats as JSON"
    )

    args = parser.parse_args()

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] PRINTMAXX Architecture Updater")
    print(f"  Project root: {PROJECT_ROOT}")
    print()

    # Collect stats
    stats = build_stats_summary()

    if args.json:
        # Remove non-serializable items
        output = {k: v for k, v in stats.items() if k != "heartbeat"}
        output["heartbeat"] = stats["heartbeat"]
        print(json.dumps(output, indent=2, default=str))
        return

    if args.status:
        print(format_stats(stats))
        return

    # Update the document
    result = update_architecture_doc(stats, dry_run=args.dry_run)
    print(result)

    if not args.dry_run:
        # Also log the update
        log_dir = PROJECT_ROOT / "AUTOMATIONS" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "arch_update.log"
        with open(safe_path(log_file), "a") as f:
            f.write(f"\n[{stats['timestamp']}] Architecture doc updated\n")
            f.write(f"  Scripts: {stats['automation_scripts']}, "
                    f"Cron: {stats['cron_jobs_active']}, "
                    f"Queue: {stats['queue_total']} ({stats['queue_pending']} pending), "
                    f"Pipelines: {stats['pipelines']}\n")


if __name__ == "__main__":
    main()
