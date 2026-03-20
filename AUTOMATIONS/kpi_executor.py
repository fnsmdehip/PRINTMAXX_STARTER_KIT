#!/usr/bin/env python3
"""
PRINTMAXX KPI EXECUTOR — Auto-executes daily KPI tasks
========================================================

Meta-orchestrator that reads today's KPI tasks from the control_panel.py
daily_plans data structure, filters by tag (AUTO/SEMI/MANUAL), and executes
AUTO tasks automatically. SEMI tasks get queued for human review. MANUAL
tasks are logged as reminders.

Usage:
  python3 AUTOMATIONS/kpi_executor.py --run         # Execute all AUTO tasks for today
  python3 AUTOMATIONS/kpi_executor.py --status      # Show task breakdown
  python3 AUTOMATIONS/kpi_executor.py --review      # Show SEMI tasks needing review
  python3 AUTOMATIONS/kpi_executor.py --dry-run     # Preview without executing
  python3 AUTOMATIONS/kpi_executor.py --day 5       # Execute for a specific day

Cron: 30 7 * * * python3 AUTOMATIONS/kpi_executor.py --run
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths & Guards
# ---------------------------------------------------------------------------
PROJECT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT / "AUTOMATIONS"
OPS = PROJECT / "OPS"
LOGS_DIR = AUTOMATIONS / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOGS_DIR / "kpi_executor.log"
REPORT_FILE = OPS / "KPI_EXECUTOR_REPORT.md"
SEMI_QUEUE_FILE = OPS / "SEMI_REVIEW_QUEUE.md"

# Safety: only commands matching this pattern can execute
SAFE_CMD_PREFIX = "python3 AUTOMATIONS/"
CMD_TIMEOUT = 120        # seconds per command
MAX_RUNTIME = 30 * 60   # 30 minutes total

# Ensure sibling modules are importable
sys.path.insert(0, str(AUTOMATIONS))

try:
    from agent_resilience import TrajectoryLogger
    _trajectory = TrajectoryLogger("kpi_executor")
except ImportError:
    _trajectory = None  # type: ignore[assignment]

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logger = logging.getLogger("kpi_executor")
logger.setLevel(logging.INFO)

_file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
_file_handler.setFormatter(logging.Formatter(
    "%(asctime)s | %(levelname)-7s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
))
logger.addHandler(_file_handler)

_stream_handler = logging.StreamHandler()
_stream_handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(_stream_handler)


def safe_path(target: Path) -> Path:
    """Verify path is within project root."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT}")
    return resolved


# ---------------------------------------------------------------------------
# Daily Plans Data — fetched from control_panel.py API or subprocess
# ---------------------------------------------------------------------------
def _load_daily_plans() -> dict[int, dict[str, Any]]:
    """Load daily plans from the control_panel API or via subprocess fallback.

    Strategy 1: Hit the API if control_panel server is running (fast).
    Strategy 2: Run a subprocess that imports and serializes the data.
    """
    plans = _try_api_fetch()
    if plans is not None:
        return plans

    plans = _try_source_parse()
    if plans is not None:
        return plans

    logger.error("Could not load daily plans from API or source parse.")
    return {}


def _try_api_fetch() -> dict[int, dict[str, Any]] | None:
    """Try fetching from the running control panel API."""
    try:
        from urllib.request import urlopen
        resp = urlopen("http://localhost:9999/api/kpi/calendar", timeout=5)
        data = json.loads(resp.read())
        plans: dict[int, dict[str, Any]] = {}
        for day_data in data.get("days", []):
            day_num = day_data["day"]
            plans[day_num] = {
                "theme": day_data.get("theme", ""),
                "tasks": day_data.get("tasks", []),
                "revenue_target": day_data.get("revenue_target", "$0"),
            }
        return plans if plans else None
    except Exception:
        return None


def _try_source_parse() -> dict[int, dict[str, Any]] | None:
    """Parse daily_plans from control_panel.py source using ast.literal_eval.

    ast.literal_eval safely parses Python literal structures (dicts, lists,
    strings, numbers) without executing arbitrary code.

    The detail field strings contain literal braces like {business_name},
    so we must use a proper tokenizer-aware brace matcher that ignores
    braces inside string literals.
    """
    import ast
    import tokenize
    import io

    source_file = AUTOMATIONS / "control_panel.py"
    if not source_file.exists():
        logger.error("control_panel.py not found at %s", source_file)
        return None

    source = source_file.read_text(encoding="utf-8")

    def _find_dict_end(src: str, open_brace_pos: int) -> int:
        """Find the matching closing brace using Python tokenizer.

        This correctly ignores braces inside string literals.
        """
        # Tokenize starting from the open brace
        snippet = src[open_brace_pos:]
        depth = 0
        try:
            tokens = tokenize.generate_tokens(io.StringIO(snippet).readline)
            for tok in tokens:
                if tok.type == tokenize.OP:
                    if tok.string == "{":
                        depth += 1
                    elif tok.string == "}":
                        depth -= 1
                        if depth == 0:
                            # tok.end is (line, col) -- convert to offset
                            lines = snippet.split("\n")
                            offset = sum(len(lines[i]) + 1 for i in range(tok.end[0] - 1)) + tok.end[1]
                            return open_brace_pos + offset
        except tokenize.TokenError:
            pass
        return -1

    def _extract_dict(src: str, marker: str, search_from: int = 0) -> tuple[dict | None, int]:
        """Find a dict assignment in source and parse it with ast.literal_eval."""
        idx = src.find(marker, search_from)
        if idx == -1:
            return None, search_from
        eq_pos = src.find("=", idx)
        if eq_pos == -1:
            return None, search_from
        dict_start = src.find("{", eq_pos)
        if dict_start == -1:
            return None, search_from

        end_idx = _find_dict_end(src, dict_start)
        if end_idx == -1:
            logger.warning("Could not find matching brace for %s", marker.strip())
            return None, search_from

        dict_text = src[dict_start:end_idx]
        try:
            parsed = ast.literal_eval(dict_text)
            return parsed, end_idx
        except (ValueError, SyntaxError) as exc:
            logger.warning("ast.literal_eval failed for %s: %s", marker.strip(), exc)
            return None, end_idx

    # Extract daily_plans
    daily_plans, after_pos = _extract_dict(source, "    daily_plans = {")
    if daily_plans is None:
        logger.error("Could not parse daily_plans from control_panel.py")
        return None

    # Extract default_plan
    default_plan, _ = _extract_dict(source, "    default_plan = {", after_pos)

    # Fill in missing days with default_plan
    if default_plan:
        for day in range(1, 31):
            if day not in daily_plans:
                daily_plans[day] = default_plan

    return daily_plans


# ---------------------------------------------------------------------------
# Command extraction from task detail field
# ---------------------------------------------------------------------------
def extract_commands(detail: str) -> list[str]:
    """Extract executable commands from a task's detail field.

    Looks for lines starting with:
      - "Verify:" / "If missed:" / "Run:" / "Command:" / "Commands:"
      - Direct "python3 AUTOMATIONS/..." on its own line
    Extracts the `python3 ...` portion.
    """
    if not detail:
        return []

    commands: list[str] = []
    lines = detail.split("\n")

    for line in lines:
        stripped = line.strip()

        # Match prefixed command lines
        for prefix in ("Verify:", "If missed:", "Run:", "Command:", "Commands:"):
            if stripped.startswith(prefix):
                remainder = stripped[len(prefix):].strip()
                cmds = _extract_python_cmds(remainder)
                commands.extend(cmds)
                break
        else:
            # Also match bare python3 AUTOMATIONS/... lines
            cmds = _extract_python_cmds(stripped)
            commands.extend(cmds)

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for cmd in commands:
        if cmd not in seen:
            seen.add(cmd)
            unique.append(cmd)

    return unique


def _extract_python_cmds(text: str) -> list[str]:
    """Extract python3 AUTOMATIONS/... commands from a text line."""
    cmds: list[str] = []
    pattern = r"python3\s+AUTOMATIONS/[^\n;|&]+"
    for match in re.finditer(pattern, text):
        cmd = match.group(0).strip()
        # Remove trailing punctuation
        cmd = cmd.rstrip(".")
        if cmd:
            cmds.append(cmd)
    return cmds


def is_safe_command(cmd: str) -> bool:
    """Verify command starts with safe prefix and has no shell injection."""
    if not cmd.startswith(SAFE_CMD_PREFIX):
        return False
    # Block shell metacharacters
    dangerous = [";", "&&", "||", "|", "`", "$(", "${", ">", "<", "\n"]
    for d in dangerous:
        if d in cmd:
            return False
    return True


# ---------------------------------------------------------------------------
# Task execution
# ---------------------------------------------------------------------------
def execute_command(cmd: str, dry_run: bool = False) -> dict[str, Any]:
    """Execute a single command with timeout and safety checks."""
    result: dict[str, Any] = {
        "command": cmd,
        "status": "skipped",
        "output": "",
        "error": "",
        "duration_s": 0.0,
    }

    if not is_safe_command(cmd):
        result["status"] = "blocked"
        result["error"] = f"Command failed safety check: {cmd}"
        logger.warning("BLOCKED unsafe command: %s", cmd)
        return result

    if dry_run:
        result["status"] = "dry_run"
        logger.info("  [DRY-RUN] Would execute: %s", cmd)
        return result

    logger.info("  Executing: %s", cmd)
    start = time.time()
    try:
        proc = subprocess.run(
            cmd.split(),
            capture_output=True,
            text=True,
            timeout=CMD_TIMEOUT,
            cwd=str(PROJECT),
        )
        elapsed = time.time() - start
        result["duration_s"] = round(elapsed, 2)
        result["output"] = proc.stdout[-2000:] if proc.stdout else ""
        result["error"] = proc.stderr[-1000:] if proc.stderr else ""
        result["status"] = "success" if proc.returncode == 0 else "failed"
        result["returncode"] = proc.returncode

        if proc.returncode != 0:
            logger.warning("  FAILED (rc=%d): %s", proc.returncode, cmd)
        else:
            logger.info("  OK (%.1fs): %s", elapsed, cmd)

    except subprocess.TimeoutExpired:
        result["status"] = "timeout"
        result["error"] = f"Command timed out after {CMD_TIMEOUT}s"
        logger.error("  TIMEOUT: %s", cmd)
    except Exception as exc:
        result["status"] = "error"
        result["error"] = str(exc)
        logger.error("  ERROR: %s -- %s", cmd, exc)

    return result


# ---------------------------------------------------------------------------
# Core execution loop
# ---------------------------------------------------------------------------
def run_tasks(day: int | None = None, dry_run: bool = False) -> dict[str, Any]:
    """Execute all AUTO tasks for the specified day."""
    start_time = time.time()
    now = datetime.now()
    target_day = day if day is not None else now.day

    logger.info("=" * 60)
    logger.info("KPI EXECUTOR -- %s -- Day %d %s",
                now.strftime("%Y-%m-%d %H:%M:%S"), target_day,
                "(DRY RUN)" if dry_run else "")
    logger.info("=" * 60)

    plans = _load_daily_plans()
    if not plans:
        logger.error("No daily plans loaded. Aborting.")
        return {"error": "No daily plans available"}

    plan = plans.get(target_day)
    if not plan:
        logger.warning("No plan found for day %d, using default", target_day)
        return {"error": f"No plan for day {target_day}"}

    theme = plan.get("theme", "UNKNOWN")
    tasks = plan.get("tasks", [])
    logger.info("Theme: %s | Total tasks: %d", theme, len(tasks))

    auto_tasks = [t for t in tasks if t.get("tag") == "AUTO"]
    semi_tasks = [t for t in tasks if t.get("tag") == "SEMI"]
    manual_tasks = [t for t in tasks if t.get("tag") == "MANUAL"]

    logger.info("Breakdown: AUTO=%d | SEMI=%d | MANUAL=%d",
                len(auto_tasks), len(semi_tasks), len(manual_tasks))
    logger.info("-" * 60)

    # Execute AUTO tasks
    auto_results: list[dict[str, Any]] = []
    for i, task in enumerate(auto_tasks, 1):
        elapsed_total = time.time() - start_time
        if elapsed_total > MAX_RUNTIME:
            logger.error("MAX RUNTIME exceeded (%.0fs). Stopping.", elapsed_total)
            break

        text = task.get("text", "")
        detail = task.get("detail", "")
        logger.info("[AUTO %d/%d] %s", i, len(auto_tasks), text)

        commands = extract_commands(detail)
        task_result: dict[str, Any] = {
            "task": text,
            "tag": "AUTO",
            "commands": [],
            "status": "no_commands" if not commands else "pending",
        }

        if not commands:
            logger.info("  No executable commands found in detail. Skipped.")
            task_result["status"] = "no_commands"
        else:
            cmd_results: list[dict[str, Any]] = []
            all_ok = True
            for cmd in commands:
                cr = execute_command(cmd, dry_run=dry_run)
                cmd_results.append(cr)
                if cr["status"] not in ("success", "dry_run"):
                    all_ok = False
            task_result["commands"] = cmd_results
            if dry_run:
                task_result["status"] = "dry_run"
            elif all_ok:
                task_result["status"] = "success"
            else:
                task_result["status"] = "partial_failure"

        auto_results.append(task_result)

    # Process SEMI tasks: queue for review
    semi_results: list[dict[str, Any]] = []
    for task in semi_tasks:
        text = task.get("text", "")
        detail = task.get("detail", "")
        commands = extract_commands(detail)
        semi_results.append({
            "task": text,
            "tag": "SEMI",
            "detail_preview": detail[:200] if detail else "",
            "commands": commands,
            "status": "queued_for_review",
        })
    _write_semi_queue(semi_results, target_day, theme)

    # Log MANUAL tasks as reminders
    manual_reminders: list[dict[str, Any]] = []
    for task in manual_tasks:
        text = task.get("text", "")
        logger.info("[MANUAL REMINDER] %s", text)
        manual_reminders.append({
            "task": text,
            "tag": "MANUAL",
            "status": "reminder",
        })

    # Build summary
    total_elapsed = time.time() - start_time
    auto_success = sum(1 for r in auto_results if r["status"] == "success")
    auto_failed = sum(1 for r in auto_results if r["status"] in ("partial_failure", "failed"))
    auto_skipped = sum(1 for r in auto_results if r["status"] == "no_commands")
    auto_dry = sum(1 for r in auto_results if r["status"] == "dry_run")

    summary = {
        "date": now.strftime("%Y-%m-%d"),
        "day": target_day,
        "theme": theme,
        "dry_run": dry_run,
        "auto": {
            "total": len(auto_tasks),
            "success": auto_success,
            "failed": auto_failed,
            "skipped": auto_skipped,
            "dry_run": auto_dry,
        },
        "semi": {"total": len(semi_tasks), "queued": len(semi_results)},
        "manual": {"total": len(manual_tasks)},
        "runtime_s": round(total_elapsed, 2),
        "auto_results": auto_results,
        "semi_results": semi_results,
        "manual_reminders": manual_reminders,
    }

    logger.info("-" * 60)
    logger.info("SUMMARY: AUTO %d/%d succeeded | SEMI %d queued | MANUAL %d reminders | %.1fs",
                auto_success, len(auto_tasks), len(semi_results),
                len(manual_reminders), total_elapsed)

    # Write report
    _write_report(summary)

    if _trajectory:
        _trajectory.log_success("kpi_executor_run",
                                day=target_day,
                                auto_success=auto_success,
                                auto_total=len(auto_tasks),
                                semi_queued=len(semi_results),
                                runtime_s=round(total_elapsed, 2))

    return summary


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------
def _write_report(summary: dict[str, Any]) -> None:
    """Write executor report to OPS/KPI_EXECUTOR_REPORT.md."""
    safe_path(REPORT_FILE)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    auto = summary["auto"]
    semi = summary["semi"]
    manual = summary["manual"]

    lines = [
        f"# KPI Executor Report",
        f"",
        f"**Generated:** {now_str}",
        f"**Day:** {summary['day']} | **Theme:** {summary['theme']}",
        f"**Mode:** {'DRY RUN' if summary['dry_run'] else 'LIVE'}",
        f"**Runtime:** {summary['runtime_s']}s",
        f"",
        f"## Summary",
        f"",
        f"| Category | Total | Status |",
        f"|----------|-------|--------|",
        f"| AUTO     | {auto['total']} | {auto['success']} OK, {auto['failed']} FAILED, {auto['skipped']} skipped |",
        f"| SEMI     | {semi['total']} | {semi['queued']} queued for review |",
        f"| MANUAL   | {manual['total']} | logged as reminders |",
        f"",
    ]

    # AUTO results detail
    if summary.get("auto_results"):
        lines.append("## AUTO Task Results")
        lines.append("")
        for r in summary["auto_results"]:
            status_icon = {"success": "[OK]", "partial_failure": "[FAIL]",
                           "no_commands": "[SKIP]", "dry_run": "[DRY]"}.get(
                               r["status"], f"[{r['status'].upper()}]")
            lines.append(f"- {status_icon} **{r['task']}**")
            for cr in r.get("commands", []):
                cmd_icon = {"success": "v", "failed": "x", "timeout": "T",
                            "blocked": "!", "dry_run": "~"}.get(
                                cr["status"], "?")
                lines.append(f"  - [{cmd_icon}] `{cr['command']}` ({cr.get('duration_s', 0)}s)")
                if cr.get("error"):
                    lines.append(f"    - Error: {cr['error'][:200]}")
        lines.append("")

    # SEMI summary
    if summary.get("semi_results"):
        lines.append("## SEMI Tasks (Review Queue)")
        lines.append("")
        for r in summary["semi_results"]:
            lines.append(f"- [ ] **{r['task']}**")
            if r.get("commands"):
                for cmd in r["commands"]:
                    lines.append(f"  - `{cmd}`")
        lines.append("")

    # MANUAL reminders
    if summary.get("manual_reminders"):
        lines.append("## MANUAL Reminders")
        lines.append("")
        for r in summary["manual_reminders"]:
            lines.append(f"- [ ] {r['task']}")
        lines.append("")

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Report written to %s", REPORT_FILE)


def _write_semi_queue(semi_results: list[dict[str, Any]], day: int, theme: str) -> None:
    """Write SEMI tasks to review queue."""
    safe_path(SEMI_QUEUE_FILE)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        f"# SEMI Task Review Queue",
        f"",
        f"**Generated:** {now_str}",
        f"**Day {day}:** {theme}",
        f"**Tasks needing human review:** {len(semi_results)}",
        f"",
    ]

    for i, r in enumerate(semi_results, 1):
        lines.append(f"## {i}. {r['task']}")
        lines.append("")
        if r.get("detail_preview"):
            lines.append(f"```")
            lines.append(r["detail_preview"])
            lines.append(f"```")
            lines.append("")
        if r.get("commands"):
            lines.append("**Available commands:**")
            for cmd in r["commands"]:
                lines.append(f"- `{cmd}`")
            lines.append("")
        lines.append("**Status:** Awaiting review")
        lines.append("")

    SEMI_QUEUE_FILE.write_text("\n".join(lines), encoding="utf-8")
    logger.info("SEMI review queue written to %s (%d tasks)", SEMI_QUEUE_FILE, len(semi_results))


# ---------------------------------------------------------------------------
# Status / Review CLI
# ---------------------------------------------------------------------------
def show_status(day: int | None = None) -> None:
    """Show today's task breakdown."""
    now = datetime.now()
    target_day = day if day is not None else now.day

    plans = _load_daily_plans()
    plan = plans.get(target_day)
    if not plan:
        print(f"No plan found for day {target_day}")
        return

    tasks = plan.get("tasks", [])
    auto_tasks = [t for t in tasks if t.get("tag") == "AUTO"]
    semi_tasks = [t for t in tasks if t.get("tag") == "SEMI"]
    manual_tasks = [t for t in tasks if t.get("tag") == "MANUAL"]

    print(f"\nKPI EXECUTOR STATUS -- Day {target_day}")
    print(f"Theme: {plan.get('theme', 'UNKNOWN')}")
    print(f"Revenue Target: {plan.get('revenue_target', 'N/A')}")
    print(f"{'=' * 50}")
    print(f"  AUTO tasks:   {len(auto_tasks):3d}  (will execute automatically)")
    print(f"  SEMI tasks:   {len(semi_tasks):3d}  (queued for human review)")
    print(f"  MANUAL tasks: {len(manual_tasks):3d}  (human-only, logged as reminders)")
    print(f"  TOTAL:        {len(tasks):3d}")
    print()

    if auto_tasks:
        print("AUTO tasks:")
        for i, t in enumerate(auto_tasks, 1):
            cmds = extract_commands(t.get("detail", ""))
            cmd_count = len(cmds)
            print(f"  {i}. {t['text']} ({cmd_count} cmd{'s' if cmd_count != 1 else ''})")
        print()

    # Show last report if exists
    if REPORT_FILE.exists():
        mtime = datetime.fromtimestamp(REPORT_FILE.stat().st_mtime)
        print(f"Last report: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")


def show_review(day: int | None = None) -> None:
    """Show SEMI tasks needing review."""
    now = datetime.now()
    target_day = day if day is not None else now.day

    plans = _load_daily_plans()
    plan = plans.get(target_day)
    if not plan:
        print(f"No plan found for day {target_day}")
        return

    tasks = plan.get("tasks", [])
    semi_tasks = [t for t in tasks if t.get("tag") == "SEMI"]

    print(f"\nSEMI TASKS FOR REVIEW -- Day {target_day}")
    print(f"Theme: {plan.get('theme', 'UNKNOWN')}")
    print(f"{'=' * 50}")

    if not semi_tasks:
        print("  No SEMI tasks for today.")
        return

    for i, t in enumerate(semi_tasks, 1):
        print(f"\n  {i}. {t['text']}")
        detail = t.get("detail", "")
        cmds = extract_commands(detail)
        if cmds:
            print(f"     Commands:")
            for cmd in cmds:
                print(f"       $ {cmd}")
        # Show first 2 lines of detail
        if detail:
            preview_lines = detail.strip().split("\n")[:2]
            for line in preview_lines:
                print(f"     | {line.strip()}")

    print()


# ---------------------------------------------------------------------------
# Executor status for control panel API
# ---------------------------------------------------------------------------
def get_executor_status() -> dict[str, Any]:
    """Return latest executor report data for the control panel API."""
    status: dict[str, Any] = {
        "last_run": None,
        "report_exists": False,
        "summary": None,
    }

    if REPORT_FILE.exists():
        status["report_exists"] = True
        mtime = REPORT_FILE.stat().st_mtime
        status["last_run"] = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        content = REPORT_FILE.read_text(encoding="utf-8")
        for line in content.split("\n"):
            if "| AUTO" in line:
                status["summary"] = line.strip()
                break

    if SEMI_QUEUE_FILE.exists():
        content = SEMI_QUEUE_FILE.read_text(encoding="utf-8")
        pending = content.count("**Status:** Awaiting review")
        status["semi_pending"] = pending

    return status


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="KPI Executor -- auto-execute daily KPI tasks"
    )
    parser.add_argument("--run", action="store_true", help="Execute all AUTO tasks for today")
    parser.add_argument("--status", action="store_true", help="Show task breakdown")
    parser.add_argument("--review", action="store_true", help="Show SEMI tasks needing review")
    parser.add_argument("--dry-run", action="store_true", help="Preview without executing")
    parser.add_argument("--day", type=int, default=None, help="Specific day (1-30)")

    args = parser.parse_args()

    if args.status:
        show_status(args.day)
    elif args.review:
        show_review(args.day)
    elif args.run or args.dry_run:
        summary = run_tasks(day=args.day, dry_run=args.dry_run)
        auto = summary.get("auto", {})
        print(f"\nDone. AUTO: {auto.get('success', 0)}/{auto.get('total', 0)} succeeded. "
              f"SEMI: {summary.get('semi', {}).get('queued', 0)} queued. "
              f"Report: {REPORT_FILE}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
