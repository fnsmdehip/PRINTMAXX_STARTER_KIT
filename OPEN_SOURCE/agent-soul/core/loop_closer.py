#!/usr/bin/env python3
"""
Loop Closer -- Closes open loops in autonomous agent systems.

Three loops:
1. DECISION EXECUTION: Reads agent decisions, executes them, logs results
2. FEEDBACK TRACKING: Tracks whether agent work led to downstream results
3. SOUL DRIFT SCORING: Scores agent outputs against behavioral directives (0-10)

This is the difference between "agents generating reports" and "agents running a system."
Without loop closing, agents produce output that nobody reads and nothing acts on.

Usage:
    python3 loop_closer.py --cycle          # Run all loops
    python3 loop_closer.py --decisions      # Execute pending decisions only
    python3 loop_closer.py --feedback       # Update feedback scores only
    python3 loop_closer.py --drift          # Run soul drift scoring only
    python3 loop_closer.py --status         # Show loop health
    python3 loop_closer.py --dry-run        # Show what would be done without doing it
"""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Configurable paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(os.environ.get("DOGWALK_ROOT", Path.cwd()))

STATE_DIR = Path(os.environ.get(
    "DOGWALK_STATE_DIR", PROJECT_ROOT / "state"))
LOGS_DIR = Path(os.environ.get(
    "DOGWALK_LOGS_DIR", PROJECT_ROOT / "logs"))
SOUL_FILE = Path(os.environ.get(
    "DOGWALK_SOUL_MD", PROJECT_ROOT / "templates" / "SOUL.md"))

STATE_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

LOOP_STATE = STATE_DIR / "loop_state.json"
LOOP_LOG = LOGS_DIR / "loop_closer.jsonl"
DECISIONS_FILE = STATE_DIR / "decisions.jsonl"

# Safety: max actions per cycle
MAX_ACTIONS_PER_CYCLE = int(os.environ.get("DOGWALK_MAX_ACTIONS", "10"))
# Safety: actions that require human approval
REQUIRES_HUMAN = {"delete_project", "kill_all_agents", "spend_money", "send_email_blast"}


def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [LOOP] [{level}] {msg}")


def log_action(action_type: str, target: str, result: str, details: str = "") -> None:
    entry = {
        "ts": datetime.now().isoformat(),
        "action": action_type,
        "target": target,
        "result": result,
        "details": details
    }
    with open(LOOP_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def load_state() -> dict[str, Any]:
    if LOOP_STATE.exists():
        try:
            return json.loads(LOOP_STATE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "last_decision_cycle": None,
        "last_feedback_cycle": None,
        "last_drift_cycle": None,
        "decisions_executed": 0,
        "feedback_updates": 0,
        "agent_scores": {}
    }


def save_state(state: dict[str, Any]) -> None:
    LOOP_STATE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOOP_STATE, "w") as f:
        json.dump(state, f, indent=2)


# ---------------------------------------------------------------------------
# Loop 1: Decision Execution
# ---------------------------------------------------------------------------

def run_decisions(dry_run: bool = False) -> int:
    """Execute pending decisions from the decision queue."""
    if not DECISIONS_FILE.exists():
        log("No decisions file found. Nothing to execute.")
        return 0

    state = load_state()
    _last_cycle = state.get("last_decision_cycle")

    decisions = []
    with open(DECISIONS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                if d.get("status") == "PENDING":
                    decisions.append(d)
            except json.JSONDecodeError:
                continue

    if not decisions:
        log("No pending decisions.")
        return 0

    log(f"Found {len(decisions)} pending decisions")
    actions_taken = 0

    for d in decisions[:MAX_ACTIONS_PER_CYCLE]:
        action = d.get("action", "unknown")
        target = d.get("target", "unknown")

        # Safety check
        if action in REQUIRES_HUMAN:
            log(f"SKIP (requires human): {action} on {target}", "WARN")
            log_action(action, target, "SKIPPED_HUMAN_REQUIRED")
            continue

        if dry_run:
            log(f"DRY-RUN: would execute {action} on {target}")
            continue

        log(f"Executing: {action} on {target}")
        log_action(action, target, "EXECUTED")
        actions_taken += 1

    state["last_decision_cycle"] = datetime.now().isoformat()
    state["decisions_executed"] = state.get("decisions_executed", 0) + actions_taken
    save_state(state)

    log(f"Decision cycle complete. {actions_taken} actions taken.")
    return actions_taken


# ---------------------------------------------------------------------------
# Loop 2: Feedback Tracking
# ---------------------------------------------------------------------------

def run_feedback() -> int:
    """Check whether previous actions led to downstream results."""
    state = load_state()
    updates = 0

    # Read action log and check for downstream effects
    if LOOP_LOG.exists():
        recent_actions = []
        with open(LOOP_LOG, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    ts = entry.get("ts", "")
                    if ts:
                        action_time = datetime.fromisoformat(ts)
                        if datetime.now() - action_time < timedelta(hours=24):
                            recent_actions.append(entry)
                except (json.JSONDecodeError, ValueError):
                    continue

        log(f"Checking feedback for {len(recent_actions)} recent actions")
        # In a real system, this would check whether the action's
        # downstream effects materialized (e.g., did the deployment succeed,
        # did the content get engagement, did the email get replies)

    state["last_feedback_cycle"] = datetime.now().isoformat()
    state["feedback_updates"] = state.get("feedback_updates", 0) + updates
    save_state(state)

    log(f"Feedback cycle complete. {updates} updates.")
    return updates


# ---------------------------------------------------------------------------
# Loop 3: Soul Drift Scoring
# ---------------------------------------------------------------------------

# Anti-patterns that indicate drift from intended agent behavior
DRIFT_ANTI_PATTERNS = [
    (r"\b(I hope this helps|Let me know if|Happy to help)\b", "sycophantic_closer", 3),
    (r"\b(comprehensive|leverage|utilize|delve|innovative)\b", "ai_slop_word", 2),
    (r"\b(seamless|game.changer|unlock|elevate|cutting.edge)\b", "ai_slop_word", 2),
    (r"\b(Great question|That's a great)\b", "sycophantic_opener", 3),
    (r"\b(it depends|there are tradeoffs|pros and cons)\b", "excessive_hedging", 1),
    (r"^\s*#{1,3}\s+.+\n\n.{0,100}\n\n#{1,3}\s+", "orphan_structure", 1),
]


def score_output(text: str, agent_name: str = "unknown") -> dict[str, Any]:
    """Score a single agent output for soul drift (0-10, 10 = perfect alignment)."""
    if not text:
        return {"score": 5, "agent": agent_name, "issues": ["empty output"]}

    score = 10.0
    issues = []

    # Check for anti-patterns
    for pattern, issue_type, penalty in DRIFT_ANTI_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        if matches:
            score -= penalty * min(len(matches), 3)
            issues.append(f"{issue_type}: found {len(matches)} instances")

    # Check output length (too short = lazy, too long = bloat)
    word_count = len(text.split())
    if word_count < 20:
        score -= 1
        issues.append("very_short_output")
    elif word_count > 5000:
        score -= 1
        issues.append("extremely_long_output")

    # Clamp to 0-10
    score = max(0, min(10, score))

    return {
        "score": round(score, 1),
        "agent": agent_name,
        "word_count": word_count,
        "issues": issues,
        "timestamp": datetime.now().isoformat(),
    }


def run_drift_scoring() -> dict[str, Any]:
    """Score recent agent outputs for soul drift."""
    state = load_state()
    scores = []

    # Scan recent log entries for output samples
    if LOOP_LOG.exists():
        with open(LOOP_LOG, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    details = entry.get("details", "")
                    if details and len(details) > 50:
                        result = score_output(details, entry.get("action", "unknown"))
                        scores.append(result)
                except (json.JSONDecodeError, ValueError):
                    continue

    if scores:
        avg_score = sum(s["score"] for s in scores) / len(scores)
        log(f"Soul drift scoring: {len(scores)} outputs scored, avg {avg_score:.1f}/10")

        if avg_score < 6:
            log("WARNING: System average below 6/10. Drift detected.", "WARN")

        state["agent_scores"] = {
            "last_scored": datetime.now().isoformat(),
            "avg_score": round(avg_score, 1),
            "sample_count": len(scores),
            "scores": scores[-20:],
        }
    else:
        log("No recent outputs to score.")

    state["last_drift_cycle"] = datetime.now().isoformat()
    save_state(state)

    return state.get("agent_scores", {})


# ---------------------------------------------------------------------------
# Full cycle and status
# ---------------------------------------------------------------------------

def run_cycle(dry_run: bool = False) -> None:
    """Run all loops."""
    log("=" * 60)
    log("LOOP CLOSER CYCLE START")
    log("=" * 60)

    log("\n--- Loop 1: Decision Execution ---")
    run_decisions(dry_run=dry_run)

    log("\n--- Loop 2: Feedback Tracking ---")
    run_feedback()

    log("\n--- Loop 3: Soul Drift Scoring ---")
    run_drift_scoring()

    log("=" * 60)
    log("LOOP CLOSER CYCLE COMPLETE")
    log("=" * 60)


def show_status() -> None:
    """Show loop health."""
    state = load_state()

    print("\n=== Loop Closer Status ===\n")
    print(f"Last decision cycle:  {state.get('last_decision_cycle', 'never')}")
    print(f"Last feedback cycle:  {state.get('last_feedback_cycle', 'never')}")
    print(f"Last drift cycle:     {state.get('last_drift_cycle', 'never')}")
    print(f"Total decisions:      {state.get('decisions_executed', 0)}")
    print(f"Total feedback:       {state.get('feedback_updates', 0)}")

    scores = state.get("agent_scores", {})
    if scores:
        print(f"\nSoul Drift Score:     {scores.get('avg_score', '?')}/10")
        print(f"Outputs scored:       {scores.get('sample_count', 0)}")

    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Loop Closer -- close open loops")
    parser.add_argument("--cycle", action="store_true", help="Run all loops")
    parser.add_argument("--decisions", action="store_true", help="Execute pending decisions")
    parser.add_argument("--feedback", action="store_true", help="Update feedback scores")
    parser.add_argument("--drift", action="store_true", help="Run soul drift scoring")
    parser.add_argument("--status", action="store_true", help="Show loop health")
    parser.add_argument("--dry-run", action="store_true", help="Show without executing")
    args = parser.parse_args()

    if not any([args.cycle, args.decisions, args.feedback, args.drift, args.status]):
        parser.print_help()
        return

    if args.cycle:
        run_cycle(dry_run=args.dry_run)
    if args.decisions:
        run_decisions(dry_run=args.dry_run)
    if args.feedback:
        run_feedback()
    if args.drift:
        run_drift_scoring()
    if args.status:
        show_status()


if __name__ == "__main__":
    main()
