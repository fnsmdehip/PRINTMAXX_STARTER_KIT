#!/usr/bin/env python3
"""
PROMPT META-REVIEW — Analyzes user prompts to find patterns, lost threads, and actionable items.

Reads LEDGER/USER_PROMPTS.jsonl, groups by session, and uses `claude -p` to produce:
  a. Intent Summary: What the user was trying to accomplish
  b. Lost Threads: Ideas/requests mentioned but never completed
  c. Actionable Items: Things that should be tracked but aren't
  d. Recurring Frustrations: Things the user keeps repeating
  e. Recommendations: System improvements based on prompting patterns

Usage:
    python3 AUTOMATIONS/prompt_meta_review.py                 # Last 48h, print only
    python3 AUTOMATIONS/prompt_meta_review.py --days 7        # Last 7 days
    python3 AUTOMATIONS/prompt_meta_review.py --save           # Save to OPS/
    python3 AUTOMATIONS/prompt_meta_review.py --dry-run        # Show prompts, skip LLM
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

from agent_resilience import sanitize_for_prompt

PROJECT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT / "AUTOMATIONS"
LEDGER = PROJECT / "LEDGER"
OPS = PROJECT / "OPS"
LOGS = AUTOMATIONS / "logs"

PROMPTS_FILE = LEDGER / "USER_PROMPTS.jsonl"
OUTPUT_FILE = OPS / "PROMPT_META_REVIEW.md"
TRACKER_FILE = OPS / "PERSISTENT_TASK_TRACKER.md"
LOG_FILE = LOGS / "prompt_meta_review.log"

# Gap threshold for session grouping (minutes)
SESSION_GAP_MINUTES = 30


def safe_path(target: str | Path) -> Path:
    """Verify path is within project root."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT}")
    return resolved


def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [PROMPT_REVIEW] [{level}] {msg}")


def log_to_file(msg: str) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_FILE), "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")


def load_prompts(days: int) -> list[dict[str, Any]]:
    """Load prompts from the last N days."""
    if not PROMPTS_FILE.exists():
        log("No prompts file found", "WARN")
        return []

    cutoff = datetime.now() - timedelta(days=days)
    prompts: list[dict[str, Any]] = []

    with open(PROMPTS_FILE, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                ts_str = entry.get("ts", "")
                try:
                    ts = datetime.fromisoformat(ts_str)
                except (ValueError, TypeError):
                    continue
                if ts >= cutoff:
                    entry["_dt"] = ts
                    prompts.append(entry)
            except json.JSONDecodeError:
                continue

    prompts.sort(key=lambda x: x["_dt"])
    return prompts


def group_by_session(prompts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Group prompts into sessions by session_id or time gap > 30 min."""
    if not prompts:
        return []

    sessions: list[dict[str, Any]] = []
    current_session: dict[str, Any] = {
        "session_id": prompts[0].get("session_id", "unknown"),
        "start": prompts[0]["_dt"],
        "end": prompts[0]["_dt"],
        "prompts": [prompts[0]],
    }

    for p in prompts[1:]:
        same_session = p.get("session_id") == current_session["session_id"]
        time_gap = (p["_dt"] - current_session["end"]).total_seconds() / 60

        if same_session and time_gap < SESSION_GAP_MINUTES:
            current_session["prompts"].append(p)
            current_session["end"] = p["_dt"]
        else:
            sessions.append(current_session)
            current_session = {
                "session_id": p.get("session_id", "unknown"),
                "start": p["_dt"],
                "end": p["_dt"],
                "prompts": [p],
            }

    sessions.append(current_session)
    return sessions


def build_analysis_prompt(sessions: list[dict[str, Any]], days: int) -> str:
    """Build the prompt for claude -p analysis."""
    lines: list[str] = []
    lines.append(f"Analyze these user prompts from the last {days} days of a PRINTMAXX autonomous business system.")
    lines.append("The user is building a hedge fund of revenue lanes with 33 autonomous agents, scrapers, and content pipelines.")
    lines.append("")
    lines.append("For each session, I'll show the prompts in order:")
    lines.append("")

    for i, sess in enumerate(sessions, 1):
        duration = (sess["end"] - sess["start"]).total_seconds() / 60
        lines.append(f"=== SESSION {i} ({sess['start'].strftime('%Y-%m-%d %H:%M')} - {sess['end'].strftime('%H:%M')}, {duration:.0f} min, {len(sess['prompts'])} prompts) ===")
        for j, p in enumerate(sess["prompts"], 1):
            prompt_text = p.get("prompt", "")
            # Sanitize + truncate user prompts before injection into analysis
            prompt_text = sanitize_for_prompt(prompt_text, max_length=2000)
            lines.append(f"  [{j}] {prompt_text}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("Produce a structured analysis with these EXACT sections:")
    lines.append("")
    lines.append("## Intent Summary")
    lines.append("What was the user trying to accomplish? What meta patterns emerge across sessions?")
    lines.append("")
    lines.append("## Lost Threads")
    lines.append("Ideas, requests, or topics mentioned but seemingly never completed or followed up on.")
    lines.append("For each: what was mentioned, which session, and what the likely intended outcome was.")
    lines.append("")
    lines.append("## Actionable Items")
    lines.append("Specific things discussed that should be tracked as tasks. Format each as:")
    lines.append("- [ ] TASK DESCRIPTION (Priority: P0/P1/P2/P3) — from Session X")
    lines.append("")
    lines.append("## Recurring Frustrations")
    lines.append("Things the user keeps having to repeat, re-explain, or fix. Patterns of friction.")
    lines.append("")
    lines.append("## Recommendations")
    lines.append("System improvements, automations, or workflow changes based on the prompting patterns observed.")
    lines.append("Be specific: name the script, cron job, or hook that should be created/modified.")
    lines.append("")
    lines.append("Keep it concise and actionable. No fluff. No AI vocabulary. Specific file paths and script names where relevant.")

    return "\n".join(lines)


def run_claude_analysis(prompt_text: str) -> str:
    """Run claude -p with the analysis prompt."""
    try:
        result = subprocess.run(
            ["claude", "-p", prompt_text],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(PROJECT),
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            log(f"claude -p failed: {result.stderr[:200]}", "ERROR")
            return f"[ERROR: claude -p failed with code {result.returncode}]"
    except FileNotFoundError:
        log("claude CLI not found", "ERROR")
        return "[ERROR: claude CLI not found]"
    except subprocess.TimeoutExpired:
        log("claude -p timed out after 120s", "ERROR")
        return "[ERROR: claude -p timed out]"


def extract_actionable_items(analysis: str) -> list[str]:
    """Extract actionable items from the analysis text."""
    items: list[str] = []
    in_actionable = False
    for line in analysis.split("\n"):
        stripped = line.strip()
        if "## Actionable Items" in stripped:
            in_actionable = True
            continue
        if stripped.startswith("## ") and in_actionable:
            break
        if in_actionable and stripped.startswith("- [ ]"):
            items.append(stripped)
    return items


def update_task_tracker(items: list[str]) -> int:
    """Append new actionable items to PERSISTENT_TASK_TRACKER.md if not already present."""
    tracker_path = safe_path(TRACKER_FILE)
    if not tracker_path.exists():
        return 0

    existing = tracker_path.read_text(encoding="utf-8")
    new_items: list[str] = []

    for item in items:
        # Simple dedup: check if the core text (minus checkbox) is already in tracker
        core = item.replace("- [ ] ", "").strip()[:80]
        if core and core.lower() not in existing.lower():
            new_items.append(item)

    if not new_items:
        return 0

    # Append to tracker
    addition = "\n\n### PROMPT META-REVIEW ITEMS \u2014 " + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n"
    addition += "\n".join(new_items) + "\n"

    with open(tracker_path, "a", encoding="utf-8") as f:
        f.write(addition)

    return len(new_items)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prompt meta-review: analyze user prompting patterns")
    parser.add_argument("--days", type=int, default=2, help="Number of days to analyze (default 2)")
    parser.add_argument("--save", action="store_true", help="Save to OPS/PROMPT_META_REVIEW.md and update tracker")
    parser.add_argument("--dry-run", action="store_true", help="Show prompts and stats only, skip LLM analysis")
    args = parser.parse_args()

    log(f"Loading prompts from last {args.days} days...")
    prompts = load_prompts(args.days)
    if not prompts:
        log("No prompts found in the specified time range.")
        print("No prompts found. Run some prompts first, then try again.")
        return

    sessions = group_by_session(prompts)
    total_prompts = sum(len(s["prompts"]) for s in sessions)
    log(f"Found {total_prompts} prompts across {len(sessions)} sessions")

    if args.dry_run:
        print(f"\n# Prompt Meta-Review (DRY RUN)")
        print(f"Period: last {args.days} days")
        print(f"Total prompts: {total_prompts}")
        print(f"Sessions: {len(sessions)}")
        print()
        for i, sess in enumerate(sessions, 1):
            duration = (sess["end"] - sess["start"]).total_seconds() / 60
            print(f"## Session {i}: {sess['start'].strftime('%Y-%m-%d %H:%M')} ({duration:.0f} min, {len(sess['prompts'])} prompts)")
            for j, p in enumerate(sess["prompts"], 1):
                text = p.get("prompt", "")[:200]
                print(f"  [{j}] {text}")
            print()
        return

    # Build and run analysis
    log("Building analysis prompt...")
    analysis_prompt = build_analysis_prompt(sessions, args.days)

    log("Running claude -p analysis (may take 30-60s)...")
    analysis = run_claude_analysis(analysis_prompt)

    # Build output
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    output_lines: list[str] = [
        f"# PROMPT META-REVIEW \u2014 {now}",
        f"Period: last {args.days} days ({total_prompts} prompts, {len(sessions)} sessions)",
        "",
        "---",
        "",
        analysis,
    ]
    output = "\n".join(output_lines)

    print(output)

    if args.save:
        out_path = safe_path(OUTPUT_FILE)
        out_path.write_text(output, encoding="utf-8")
        log(f"Saved to {out_path}")

        # Extract and update tracker
        items = extract_actionable_items(analysis)
        if items:
            added = update_task_tracker(items)
            log(f"Added {added} new items to PERSISTENT_TASK_TRACKER.md")
        else:
            log("No new actionable items extracted")

    log_to_file(f"Review complete: {total_prompts} prompts, {len(sessions)} sessions, days={args.days}, saved={args.save}")


if __name__ == "__main__":
    main()
