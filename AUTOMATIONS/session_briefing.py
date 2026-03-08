#!/usr/bin/env python3
"""
SESSION BRIEFING -- Fast briefing at session start.

Reads existing files (no LLM calls) to produce a concise briefing:
1. Automation Report: What cron/launchd agents did since last session
2. Changes Since Last Session: git diff summary (excluding guardian commits)
3. Actionable Queue: Prioritized list from PERSISTENT_TASK_TRACKER.md
4. Prompt Review Summary: Findings from last prompt_meta_review
5. Unblocked Items: Anything previously blocked that is now unblocked

Outputs to OPS/SESSION_BRIEFING.md and stdout. Must finish in < 30 seconds.

Usage:
    python3 AUTOMATIONS/session_briefing.py              # Print briefing
    python3 AUTOMATIONS/session_briefing.py --save       # Also save to OPS/
    python3 AUTOMATIONS/session_briefing.py --json       # JSON output
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

PROJECT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT / "AUTOMATIONS"
OPS = PROJECT / "OPS"
LEDGER = PROJECT / "LEDGER"
LOGS = AUTOMATIONS / "logs"

# Key input files
DIGEST_FILE = OPS / "DAILY_DIGEST.md"
TACTICAL_PLAN = OPS / "DAILY_TACTICAL_PLAN.md"
TRACKER_FILE = OPS / "PERSISTENT_TASK_TRACKER.md"
META_REVIEW = OPS / "PROMPT_META_REVIEW.md"
ACTIONABLE_QUEUE = OPS / "ACTIONABLE_QUEUE.md"
HEARTBEAT = OPS / "HEARTBEAT.md"
SESSION_LOG = OPS / "SESSION_LOG.md"
BRIEFING_STATE = OPS / "_state" / "session_briefing_state.json"

# Agent outputs
SWARM_REPORTS = AUTOMATIONS / "agent" / "swarm" / "reports"
CEO_DECISIONS = AUTOMATIONS / "agent" / "ceo_agent" / "decisions.jsonl"
LOOP_LOG = AUTOMATIONS / "agent" / "swarm" / "loop_closer.jsonl"
SWARM_STATE = AUTOMATIONS / "agent" / "swarm" / "swarm_state.json"
CEO_STATE = AUTOMATIONS / "agent" / "ceo_agent" / "ceo_state.json"

OUTPUT_FILE = OPS / "SESSION_BRIEFING.md"
LOG_FILE = LOGS / "session_briefing.log"


def safe_path(target: str | Path) -> Path:
    """Verify path is within project root."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT}")
    return resolved


def log_to_file(msg: str) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_FILE), "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")


def read_file_safe(path: Path, max_lines: int = 0) -> str:
    """Read a file safely, return empty string on failure."""
    try:
        if not path.exists():
            return ""
        text = path.read_text(encoding="utf-8", errors="replace")
        if max_lines > 0:
            lines = text.split("\n")
            return "\n".join(lines[:max_lines])
        return text
    except Exception:
        return ""


def load_state() -> dict[str, Any]:
    """Load last session briefing state."""
    state_path = safe_path(BRIEFING_STATE)
    if state_path.exists():
        try:
            return json.loads(state_path.read_text())
        except Exception:
            pass
    return {"last_briefing": None, "last_session_ts": None}


def save_state(state: dict[str, Any]) -> None:
    """Save session briefing state."""
    state_path = safe_path(BRIEFING_STATE)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)


def get_last_session_ts(state: dict[str, Any]) -> datetime:
    """Get timestamp of last session, default 24h ago."""
    ts_str = state.get("last_session_ts")
    if ts_str:
        try:
            return datetime.fromisoformat(ts_str)
        except (ValueError, TypeError):
            pass
    return datetime.now() - timedelta(hours=24)


def automation_report(since: datetime) -> str:
    """What did the autonomous system do since last session?"""
    lines: list[str] = []
    lines.append("## Automation Report")
    lines.append("")

    # 1. Daily digest summary (first 30 lines)
    digest = read_file_safe(DIGEST_FILE, max_lines=30)
    if digest:
        lines.append("### Daily Digest (latest)")
        # Extract key stats
        for dline in digest.split("\n"):
            dline_stripped = dline.strip()
            if dline_stripped.startswith("- **") or dline_stripped.startswith("Revenue:"):
                lines.append(dline_stripped)
        lines.append("")

    # 2. Recent swarm reports
    if SWARM_REPORTS.exists():
        since_str = since.strftime("%Y%m%d")
        recent_reports: list[str] = []
        for f in sorted(SWARM_REPORTS.iterdir(), reverse=True):
            if f.is_file() and f.suffix == ".md":
                try:
                    mtime = datetime.fromtimestamp(f.stat().st_mtime)
                    if mtime >= since:
                        recent_reports.append(f.name)
                except Exception:
                    continue
        if recent_reports:
            lines.append(f"### Agent Reports ({len(recent_reports)} since last session)")
            for r in recent_reports[:15]:
                lines.append(f"- {r}")
            if len(recent_reports) > 15:
                lines.append(f"- ... and {len(recent_reports) - 15} more")
            lines.append("")

    # 3. CEO decisions since last session
    if CEO_DECISIONS.exists():
        recent_decisions: list[dict[str, Any]] = []
        try:
            with open(CEO_DECISIONS, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        ts_str = d.get("ts", "")
                        ts = datetime.fromisoformat(ts_str) if ts_str else None
                        if ts and ts >= since:
                            recent_decisions.append(d)
                    except (json.JSONDecodeError, ValueError):
                        continue
        except Exception:
            pass

        if recent_decisions:
            lines.append(f"### CEO Decisions ({len(recent_decisions)})")
            for dec in recent_decisions[-10:]:
                dtype = dec.get("type", "?")
                summary = dec.get("summary", dec.get("action", "?"))
                if isinstance(summary, str):
                    summary = summary[:120]
                lines.append(f"- [{dtype}] {summary}")
            lines.append("")

    # 4. Loop closer actions
    if LOOP_LOG.exists():
        recent_loops: list[dict[str, Any]] = []
        try:
            with open(LOOP_LOG, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        ts_str = entry.get("ts", "")
                        ts = datetime.fromisoformat(ts_str) if ts_str else None
                        if ts and ts >= since:
                            recent_loops.append(entry)
                    except (json.JSONDecodeError, ValueError):
                        continue
        except Exception:
            pass

        if recent_loops:
            lines.append(f"### Loop Closer ({len(recent_loops)} actions)")
            for lp in recent_loops[-8:]:
                action = lp.get("action", "?")
                target = lp.get("target", "?")
                result = lp.get("result", "?")
                lines.append(f"- {action}: {target} -> {result}")
            lines.append("")

    # 5. Heartbeat
    heartbeat = read_file_safe(HEARTBEAT, max_lines=10)
    if heartbeat:
        lines.append("### System Heartbeat")
        for hline in heartbeat.split("\n"):
            hline_stripped = hline.strip()
            if hline_stripped and not hline_stripped.startswith("#"):
                lines.append(hline_stripped)
        lines.append("")

    if len(lines) <= 2:
        lines.append("No automation activity detected since last session.")
        lines.append("")

    return "\n".join(lines)


def changes_since_last_session(since: datetime) -> str:
    """Summarize git changes since last session, excluding guardian commits."""
    lines: list[str] = []
    lines.append("## Changes Since Last Session")
    lines.append("")

    try:
        since_str = since.strftime("%Y-%m-%d %H:%M")
        # Get non-guardian commits
        result = subprocess.run(
            ["git", "log", f"--since={since_str}", "--oneline", "--no-merges", "-30"],
            capture_output=True, text=True, timeout=10,
            cwd=str(PROJECT),
        )
        if result.returncode == 0 and result.stdout.strip():
            commits = result.stdout.strip().split("\n")
            # Filter out guardian/auto commits
            human_commits: list[str] = []
            auto_commits: list[str] = []
            for c in commits:
                lower = c.lower()
                if any(kw in lower for kw in ["guardian", "auto-commit", "safety commit", "cron"]):
                    auto_commits.append(c)
                else:
                    human_commits.append(c)

            if human_commits:
                lines.append(f"### Human/Agent Commits ({len(human_commits)})")
                for c in human_commits[:15]:
                    lines.append(f"- {c}")
                lines.append("")

            if auto_commits:
                lines.append(f"### Automated Commits ({len(auto_commits)})")
                lines.append(f"- {len(auto_commits)} guardian/safety commits")
                lines.append("")

            # Quick diffstat
            diff_result = subprocess.run(
                ["git", "diff", "--stat", f"HEAD~{min(len(commits), 20)}..HEAD"],
                capture_output=True, text=True, timeout=10,
                cwd=str(PROJECT),
            )
            if diff_result.returncode == 0 and diff_result.stdout.strip():
                stat_lines = diff_result.stdout.strip().split("\n")
                # Just show the summary line (last line)
                if stat_lines:
                    lines.append(f"**Diff summary:** {stat_lines[-1].strip()}")
                    lines.append("")
        else:
            lines.append("No git commits since last session (or not a git repo).")
            lines.append("")
    except Exception as e:
        lines.append(f"Git check failed: {e}")
        lines.append("")

    return "\n".join(lines)


def actionable_queue() -> str:
    """Extract prioritized actionable items from tracker."""
    lines: list[str] = []
    lines.append("## Actionable Queue")
    lines.append("")

    # Check dedicated actionable queue first
    if ACTIONABLE_QUEUE.exists():
        queue_text = read_file_safe(ACTIONABLE_QUEUE, max_lines=60)
        if queue_text:
            lines.append(queue_text)
            lines.append("")
            return "\n".join(lines)

    # Fall back to tracker
    tracker = read_file_safe(TRACKER_FILE)
    if not tracker:
        lines.append("No task tracker found.")
        lines.append("")
        return "\n".join(lines)

    # Extract recent entries (top of file is most recent)
    tracker_lines = tracker.split("\n")
    human_actions: list[str] = []
    recent_tasks: list[str] = []

    for tline in tracker_lines[:100]:
        tline_stripped = tline.strip()
        lower = tline_stripped.lower()
        if "human" in lower or "blocker" in lower or "p0" in lower:
            human_actions.append(tline_stripped)
        elif tline_stripped.startswith("- ") or tline_stripped.startswith("### "):
            recent_tasks.append(tline_stripped)

    if human_actions:
        lines.append("### Human Actions Required")
        for h in human_actions[:10]:
            lines.append(h)
        lines.append("")

    if recent_tasks:
        lines.append("### Recent Tasks")
        for t in recent_tasks[:15]:
            lines.append(t)
        lines.append("")

    return "\n".join(lines)


def prompt_review_summary() -> str:
    """Include findings from the last prompt meta-review."""
    lines: list[str] = []

    if not META_REVIEW.exists():
        return ""

    review = read_file_safe(META_REVIEW)
    if not review:
        return ""

    # Check if it was generated recently (within last 3 days)
    try:
        mtime = datetime.fromtimestamp(META_REVIEW.stat().st_mtime)
        age_hours = (datetime.now() - mtime).total_seconds() / 3600
        if age_hours > 72:
            return ""
    except Exception:
        return ""

    lines.append("## Prompt Review Findings")
    lines.append(f"(from {mtime.strftime('%Y-%m-%d %H:%M')})")
    lines.append("")

    # Extract key sections
    current_section = ""
    section_lines: dict[str, list[str]] = {}
    for rline in review.split("\n"):
        if rline.startswith("## "):
            current_section = rline.strip()
            section_lines[current_section] = []
        elif current_section and rline.strip():
            section_lines.setdefault(current_section, []).append(rline.strip())

    # Include Lost Threads and Recurring Frustrations
    for key in ["## Lost Threads", "## Recurring Frustrations", "## Actionable Items"]:
        if key in section_lines and section_lines[key]:
            lines.append(key)
            for sl in section_lines[key][:8]:
                lines.append(sl)
            lines.append("")

    return "\n".join(lines)


def unblocked_items(since: datetime) -> str:
    """Check for items that were blocked but may now be unblocked."""
    lines: list[str] = []

    # Check if key files have been modified since last session (indicating progress)
    check_files: dict[str, str] = {
        "Twitter warmup state": str(AUTOMATIONS / "agent" / "twitter_warmup_state.json"),
        "Swarm state": str(SWARM_STATE),
        "CEO state": str(CEO_STATE),
        "Autonomy state": str(AUTOMATIONS / "agent" / "autonomy" / "autonomy_state.json"),
    }

    updated: list[str] = []
    for label, fpath in check_files.items():
        fp = Path(fpath)
        if fp.exists():
            try:
                mtime = datetime.fromtimestamp(fp.stat().st_mtime)
                if mtime >= since:
                    updated.append(f"- {label} (updated {mtime.strftime('%H:%M')})")
            except Exception:
                continue

    if updated:
        lines.append("## Recently Updated State")
        lines.append("")
        for u in updated:
            lines.append(u)
        lines.append("")

    return "\n".join(lines)


def build_briefing(save: bool = False, as_json: bool = False) -> str:
    """Build the full session briefing."""
    state = load_state()
    since = get_last_session_ts(state)
    now = datetime.now()

    hours_since_last = (now - since).total_seconds() / 3600

    sections: list[str] = []
    sections.append(f"# SESSION BRIEFING -- {now.strftime('%Y-%m-%d %H:%M')}")
    sections.append(f"Last session: {since.strftime('%Y-%m-%d %H:%M')} ({hours_since_last:.1f}h ago)")
    sections.append("")
    sections.append("---")
    sections.append("")

    # Build all sections
    sections.append(automation_report(since))
    sections.append(changes_since_last_session(since))
    sections.append(actionable_queue())

    review = prompt_review_summary()
    if review:
        sections.append(review)

    unblocked = unblocked_items(since)
    if unblocked:
        sections.append(unblocked)

    briefing = "\n".join(sections)

    # Update state
    state["last_session_ts"] = now.isoformat()
    state["last_briefing"] = now.isoformat()

    if save:
        out_path = safe_path(OUTPUT_FILE)
        out_path.write_text(briefing, encoding="utf-8")
        save_state(state)

    if as_json:
        result: dict[str, Any] = {
            "generated": now.isoformat(),
            "last_session": since.isoformat(),
            "hours_since_last": round(hours_since_last, 1),
            "briefing": briefing,
        }
        return json.dumps(result, indent=2)

    return briefing


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Session briefing generator")
    parser.add_argument("--save", action="store_true", help="Save to OPS/SESSION_BRIEFING.md")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    briefing = build_briefing(save=args.save, as_json=args.json)
    print(briefing)

    log_to_file(f"Briefing generated, save={args.save}")


if __name__ == "__main__":
    main()
