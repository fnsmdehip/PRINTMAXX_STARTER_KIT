#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Autonomous Orchestrator
===================================
The AI brain that closes the feedback loop between cron scripts and Claude sessions.

Architecture (Cursor hierarchy model):
  PLANNER: This script (gathers state, generates focused session prompts)
  WORKER:  Claude Code sessions (reads prompts, executes analysis, writes results)
  JUDGE:   auto_rebalancer.py + venture_performance_tracker.py

Flow:
  CRON → schedule_claude.sh → orchestrator --prep → Claude Code → orchestrator --post

Usage:
  python3 autonomous_orchestrator.py --prep morning|midday|evening
  python3 autonomous_orchestrator.py --auto morning|midday|evening
  python3 autonomous_orchestrator.py --post SESSION_LOG
  python3 autonomous_orchestrator.py --status
  python3 autonomous_orchestrator.py --plan morning|midday|evening
"""

import json
import os
import sys
import csv
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
AUTO = BASE / "AUTOMATIONS"
OPS = BASE / "OPS"
LEDGER = BASE / "LEDGER"
CONTENT = BASE / "CONTENT"
LOGS = AUTO / "logs"
PROMPTS_DIR = AUTO / "session_prompts"
CHECKPOINTS = OPS / "checkpoints"

for d in [PROMPTS_DIR, CHECKPOINTS, LOGS,
          CHECKPOINTS / "pending", CHECKPOINTS / "approved", CHECKPOINTS / "rejected",
          LOGS / "sessions", LOGS / "daily"]:
    d.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_file(path, default=""):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return default


def count_csv(path):
    try:
        with open(path) as f:
            return sum(1 for _ in f) - 1
    except Exception:
        return 0


def read_csv_tail(path, n=20):
    """Read last N rows of a CSV as list of dicts."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            return rows[-n:]
    except Exception:
        return []


def safe_write(path, content):
    tmp = Path(str(path) + ".tmp")
    try:
        tmp.write_text(content, encoding="utf-8")
        tmp.rename(path)
    except OSError as e:
        print(f"[ORCH] WARNING: write failed {path.name}: {e}")
        try:
            tmp.unlink(missing_ok=True)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Session checkpoint (exact-state resume)
# ---------------------------------------------------------------------------

SESSION_CHECKPOINT = LOGS / "session_checkpoint.json"


def save_checkpoint(session_type, task_index, state_snapshot):
    """Save exact session state so a crashed session can resume."""
    ckpt = {
        "session_type": session_type,
        "task_completed": task_index,
        "timestamp": datetime.now().isoformat(),
        "state": {k: v for k, v in state_snapshot.items()
                  if k not in ("overnight_status", "overnight_log", "rebalance")},
    }
    safe_write(SESSION_CHECKPOINT, json.dumps(ckpt, indent=2, default=str))


def load_checkpoint():
    """Load last checkpoint if it exists and is recent (< 2 hours old)."""
    if not SESSION_CHECKPOINT.exists():
        return None
    try:
        ckpt = json.loads(SESSION_CHECKPOINT.read_text())
        ts = datetime.fromisoformat(ckpt["timestamp"])
        if (datetime.now() - ts).total_seconds() > 7200:
            return None  # stale checkpoint
        return ckpt
    except Exception:
        return None


def clear_checkpoint():
    """Remove checkpoint after successful session completion."""
    try:
        SESSION_CHECKPOINT.unlink(missing_ok=True)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# System state gatherer
# ---------------------------------------------------------------------------

def gather_state():
    """Snapshot every data source the orchestrator cares about."""
    s = {}
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")

    # Heartbeat
    s["heartbeat"] = read_file(OPS / "HEARTBEAT.md").strip()
    s["active_tasks"] = read_file(OPS / "active-tasks.md").strip()

    # Overnight status
    for dt in [today, yesterday]:
        sf = LOGS / f"overnight_status_{dt}.json"
        if sf.exists():
            s["overnight_status"] = read_file(sf)[:3000]
            break
    else:
        s["overnight_status"] = "(none)"

    # Overnight log tail
    for dt in [today, yesterday]:
        lf = LOGS / f"overnight_{dt}.log"
        if lf.exists():
            lines = read_file(lf).strip().split("\n")
            s["overnight_log"] = "\n".join(lines[-40:])
            break
    else:
        s["overnight_log"] = "(none)"

    # Leads
    qdir = AUTO / "leads" / "qualified"
    s["hot"] = count_csv(qdir / "HOT_LEADS_QUALIFIED.csv")
    s["warm"] = count_csv(qdir / "WARM_LEADS_QUALIFIED.csv")
    s["analyzed"] = count_csv(qdir / "ANALYZED_LEADS.csv")

    # Alpha
    alpha_path = LEDGER / "ALPHA_STAGING.csv"
    rows = read_csv_tail(alpha_path, n=10000)
    s["alpha_pending"] = sum(1 for r in rows if r.get("status") == "PENDING_REVIEW")
    s["alpha_approved"] = sum(1 for r in rows if r.get("status") == "APPROVED")
    s["alpha_total"] = len(rows)

    # Revenue
    rev = BASE / "FINANCIALS" / "REVENUE_TRACKER.csv"
    rrows = read_csv_tail(rev, 1000)
    s["revenue"] = sum(float(r.get("amount", 0) or 0) for r in rrows)

    # Checkpoints
    s["ckpt_pending"] = [p.name for p in (CHECKPOINTS / "pending").glob("*.md")]

    # Disk
    try:
        out = subprocess.run(["df", "-k", str(BASE)], capture_output=True, text=True, timeout=5)
        parts = out.stdout.strip().split("\n")[-1].split()
        s["disk_gb"] = round(int(parts[3]) / 1048576, 1)
    except Exception:
        s["disk_gb"] = "?"

    # Rebalancer scores (if available)
    rb = AUTO / "logs" / "rebalance_latest.json"
    if rb.exists():
        try:
            s["rebalance"] = json.loads(read_file(rb))
        except Exception:
            s["rebalance"] = None
    else:
        s["rebalance"] = None

    s["hour"] = now.hour
    s["date"] = today
    s["ts"] = now.strftime("%Y-%m-%d %H:%M")
    return s


# ---------------------------------------------------------------------------
# Prompt generators — focused, no fluff, specific instructions
# ---------------------------------------------------------------------------

def _header(title, s):
    return f"""# {title} — {s['ts']}

## System Snapshot
```
{s['heartbeat']}
```
Pipeline: {s['hot']} hot | {s['warm']} warm | {s['analyzed']} analyzed
Alpha: {s['alpha_pending']} pending | {s['alpha_approved']} approved
Revenue: ${s['revenue']:.0f} | Disk: {s['disk_gb']}GB
Checkpoints: {len(s['ckpt_pending'])} pending
"""


def prompt_morning(s):
    return _header("PRINTMAXX Morning Briefing", s) + f"""
## Overnight Results
```
{s['overnight_status'][:2000]}
```

## Overnight Log (tail)
```
{s['overnight_log'][:2500]}
```

## ROUTING RULES (conditional branching)
- After each task, write a 1-line status to OPS/session_progress.json: {{"task": N, "result": "done|skipped|failed", "note": "..."}}
- If Task 2 (alpha review) finds 0 pending entries → SKIP Task 4 (content squeeze), route time to Task 3 (daily TODO) with extra detail
- If overnight log shows 0 failures → SKIP "failed scripts to fix" in Task 3
- If checkpoints pending > 0 → PRIORITIZE Task 5 (flag checkpoints) before Task 4

## TASKS (execute in order, apply routing rules)

### 1. Update HEARTBEAT
Read latest data. Rewrite OPS/HEARTBEAT.md with current numbers. Keep under 12 lines.

### 2. Review Alpha (up to 20 entries)
Open LEDGER/ALPHA_STAGING.csv. Find PENDING_REVIEW rows (newest first).
For each: set status to APPROVED, ENGAGEMENT_BAIT, or REJECTED.
Add reviewer_notes column with 1-line reason.
Follow .claude/rules/alpha-review.md strictly.

### 3. Daily TODO
Write OPS/DAILY_TODO_{s['date'].replace('-','_')}.md:
- Top 5 revenue-impact actions
- Failed overnight scripts to fix
- New hot leads worth contacting
- Content to publish

### 4. Content Squeeze (3 tweets + 1 thread)
From overnight data, generate @PRINTMAXXER content.
Save to CONTENT/social/auto_generated/morning_{s['date'].replace('-','_')}.md
Voice: .claude/rules/copy-style.md — consequence-first, specific numbers, no AI slop.

### 5. Flag Checkpoints
Anything needing human approval → OPS/checkpoints/pending/[TYPE]_[DESC].md

### 6. Update active-tasks.md
Write what you did + next priorities.
"""


def prompt_midday(s):
    return _header("PRINTMAXX Midday Analysis", s) + f"""
## ROUTING RULES (conditional branching)
- After each task, write a 1-line status to OPS/session_progress.json: {{"task": N, "result": "done|skipped|failed", "note": "..."}}
- If lead pipeline finds 0 new hot leads → SKIP Task 5 (outreach generation)
- If no approved checkpoints exist → SKIP Task 3 (process checkpoints)
- If rebalancer shows all methods >= 40 → SKIP kill checkpoint creation in Task 4

## TASKS

### 1. Run Lead Pipeline (2 cycles)
Execute: python3 AUTOMATIONS/closed_loop_pipeline.py --cycles 2 --batch 1000 --workers 20
Record results.

### 2. Venture Scoring
Execute: python3 AUTOMATIONS/venture_performance_tracker.py --recommend
Write 1-paragraph summary of recommendations to OPS/DAILY_TODO_{s['date'].replace('-','_')}.md (append).

### 3. Process Approved Checkpoints
Read OPS/checkpoints/approved/ for any human-approved actions.
Execute approved items within guardrails. Move processed files to OPS/checkpoints/done/.

### 4. Rebalancer Check
Execute: python3 AUTOMATIONS/auto_rebalancer.py --check
If any method below 20/100 for 3+ days → write checkpoint to pending/KILL_[name].md.

### 5. Generate Outreach for New Hot Leads
If new hot leads exist since morning:
Execute: python3 AUTOMATIONS/generate_cold_emails.py --input AUTOMATIONS/leads/qualified/HOT_LEADS_QUALIFIED.csv --dry-run
Log count.

### 6. Update HEARTBEAT + active-tasks.md
"""


def prompt_evening(s):
    rb_summary = ""
    if s["rebalance"]:
        rb_summary = "Rebalance scores: " + json.dumps(s["rebalance"][:5], indent=2)

    return _header("PRINTMAXX Evening Summary", s) + f"""
{rb_summary}

## ROUTING RULES (conditional branching)
- After each task, write a 1-line status to OPS/session_progress.json: {{"task": N, "result": "done|skipped|failed", "note": "..."}}
- If today had 0 content generated → SKIP Task 2 (content squeeze), write note explaining why
- If no overnight scripts need prep → abbreviate Task 3

## TASKS

### 1. Day Summary
Read AUTOMATIONS/logs/ for today.
Write OPS/DAILY_SUMMARY_{s['date'].replace('-','_')}.md:
- Scripts succeeded vs failed
- Leads generated today
- Alpha processed
- Content generated
- Key metric deltas

### 2. Content Squeeze (3 tweets)
From today's work, generate 3 @PRINTMAXXER tweets.
Append to CONTENT/social/auto_generated/evening_{s['date'].replace('-','_')}.md

### 3. Prep Overnight
Update OPS/active-tasks.md with overnight priorities.
Verify AUTOMATIONS/overnight_master_runner.sh is ready.

### 4. HEARTBEAT Final Update
Rewrite OPS/HEARTBEAT.md with end-of-day numbers.

### 5. Checkpoint Summary
Write OPS/checkpoints/DAILY_CHECKPOINT_SUMMARY.md with all pending items for human morning review.
"""


PROMPT_MAP = {
    "morning": prompt_morning,
    "midday": prompt_midday,
    "evening": prompt_evening,
}


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_prep(session_type):
    state = gather_state()
    prompt = PROMPT_MAP[session_type](state)
    out = PROMPTS_DIR / f"session_{session_type}.md"
    safe_write(out, prompt)
    print(f"[ORCH] Prompt written: {out}")
    print(f"[ORCH] State: {state['hot']} hot, {state['alpha_pending']} alpha pending, "
          f"${state['revenue']:.0f} rev, {state['disk_gb']}GB disk")
    return out


def cmd_post(log_path):
    """Post-session: log what happened.

    Counts tool calls using Claude CLI output markers. The --print output
    includes markers like 'Write(file_path)', 'Edit(file_path)', 'Bash(command)'.
    We count these structured markers first, fall back to keyword matching.
    """
    import re
    content = read_file(log_path)

    # Primary: count Claude CLI tool-call markers (structured output)
    write_markers = len(re.findall(r'(?:Write|write)\s*\(', content))
    edit_markers = len(re.findall(r'(?:Edit|edit)\s*\(', content))
    bash_markers = len(re.findall(r'(?:Bash|bash)\s*\(', content))

    # Secondary: count common output patterns as fallback signals
    wrote_files = len(re.findall(r'(?:wrote|created|saved)\s+(?:to\s+)?[`\'"]?\S+\.\w+', content, re.I))
    edited_files = len(re.findall(r'(?:edited|updated|modified)\s+(?:in\s+)?[`\'"]?\S+\.\w+', content, re.I))
    ran_commands = len(re.findall(r'(?:python3|bash|npm|node|pip3)\s+\S+', content))

    # Use max of structured vs fallback (avoids double-count)
    writes = max(write_markers, wrote_files)
    edits = max(edit_markers, edited_files)
    runs = max(bash_markers, ran_commands)

    # Count lines as rough session size metric
    line_count = content.count("\n")

    entry = (
        f"\n## Claude Session — {datetime.now().strftime('%H:%M')}\n"
        f"- Log: {log_path}\n"
        f"- Output: {line_count} lines\n"
        f"- Writes: ~{writes}, Edits: ~{edits}, Commands: ~{runs}\n"
    )

    daily_log = LOGS / "daily" / f"{datetime.now().strftime('%Y-%m-%d')}.md"
    try:
        with open(daily_log, "a") as f:
            f.write(entry)
    except OSError as e:
        print(f"[ORCH] WARNING: daily log append failed: {e}")

    print(f"[ORCH] Post-session logged. {line_count} lines, writes~{writes} edits~{edits} runs~{runs}")


def cmd_plan(session_type):
    """Show the planned session tasks for human pre-approval without executing."""
    state = gather_state()
    prompt = PROMPT_MAP[session_type](state)

    # Check for resume checkpoint
    ckpt = load_checkpoint()
    if ckpt and ckpt["session_type"] == session_type:
        print(f"[PLAN] RESUME available: last {session_type} crashed at task {ckpt['task_completed']}")
        print(f"[PLAN] Checkpoint from: {ckpt['timestamp']}")
        print()

    print(f"[PLAN] Session: {session_type} | {state['ts']}")
    print(f"[PLAN] State: {state['hot']} hot, {state['alpha_pending']} alpha pending, "
          f"${state['revenue']:.0f} rev, {state['disk_gb']}GB disk")
    print()
    print("=" * 60)
    print("PLANNED TASKS:")
    print("=" * 60)

    # Extract task headers from the prompt
    for line in prompt.split("\n"):
        if line.startswith("### "):
            print(f"  {line.replace('### ', '')}")
        elif line.startswith("## ROUTING"):
            print()
            print("ROUTING RULES:")
        elif line.startswith("- If ") or line.startswith("- After "):
            print(f"  {line}")

    print()
    print("[PLAN] To execute: --prep or --auto")
    print(f"[PLAN] Prompt would be written to: {PROMPTS_DIR / f'session_{session_type}.md'}")


def cmd_auto(session_type):
    """Full autonomous loop: prep → checkpoint → Claude Code → post → clear."""
    state = gather_state()

    # Check for resume from crashed session
    ckpt = load_checkpoint()
    if ckpt and ckpt["session_type"] == session_type:
        print(f"[ORCH] Resuming from checkpoint (task {ckpt['task_completed']})")

    prompt_file = cmd_prep(session_type)

    # Save checkpoint: session starting
    save_checkpoint(session_type, 0, state)

    # Auto-detect claude CLI location
    import shutil
    claude_path = shutil.which("claude")
    claude = Path(claude_path) if claude_path else Path.home() / ".local" / "bin" / "claude"
    if not claude.exists():
        print(f"[ORCH] Claude CLI not found at {claude}. Run manually:")
        print(f"  cat {prompt_file} | claude --print --dangerously-skip-permissions")
        return

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_log = LOGS / "sessions" / f"{session_type}_{ts}.log"

    print(f"[ORCH] Launching Claude Code ({session_type})...")
    try:
        with open(prompt_file) as pf, open(session_log, "w") as lf:
            result = subprocess.run(
                [str(claude), "--print", "--dangerously-skip-permissions"],
                stdin=pf, stdout=lf, stderr=subprocess.STDOUT,
                timeout=1800, cwd=str(BASE),
            )
        print(f"[ORCH] Session complete (exit {result.returncode})")
    except subprocess.TimeoutExpired:
        print("[ORCH] Session timed out (30 min)")
    except Exception as e:
        print(f"[ORCH] Session error: {e}")

    cmd_post(str(session_log))
    clear_checkpoint()
    print("[ORCH] Checkpoint cleared (session complete)")


def cmd_status():
    s = gather_state()
    print("=" * 60)
    print(f"PRINTMAXX AUTONOMOUS ORCHESTRATOR — {s['ts']}")
    print("=" * 60)
    print()
    print(s["heartbeat"])
    print()
    print(f"PIPELINE: {s['hot']} hot | {s['warm']} warm | {s['analyzed']} analyzed")
    print(f"ALPHA:    {s['alpha_pending']} pending | {s['alpha_approved']} approved | {s['alpha_total']} total")
    print(f"REVENUE:  ${s['revenue']:.0f}")
    print(f"DISK:     {s['disk_gb']}GB free")
    print(f"CHECKPTS: {len(s['ckpt_pending'])} pending")
    print()

    if s["ckpt_pending"]:
        print("PENDING HUMAN APPROVAL:")
        for name in s["ckpt_pending"]:
            print(f"  - {name}")
        print()

    hour = s["hour"]
    if hour < 10:
        rec = "morning"
    elif hour < 15:
        rec = "midday"
    else:
        rec = "evening"
    print(f"RECOMMENDED SESSION: --prep {rec}")

    if s["rebalance"]:
        print()
        print("REBALANCE (top 5):")
        for item in (s["rebalance"] or [])[:5]:
            name = item.get("method", "?")
            score = item.get("score", "?")
            action = item.get("action", "?")
            print(f"  {name}: {score}/100 → {action}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="PRINTMAXX Autonomous Orchestrator")
    p.add_argument("--prep", choices=["morning", "midday", "evening"])
    p.add_argument("--auto", choices=["morning", "midday", "evening"])
    p.add_argument("--plan", choices=["morning", "midday", "evening"],
                   help="Preview planned tasks without executing (pre-approval gate)")
    p.add_argument("--post", metavar="LOG")
    p.add_argument("--status", action="store_true")
    args = p.parse_args()

    if args.plan:
        cmd_plan(args.plan)
    elif args.prep:
        cmd_prep(args.prep)
    elif args.auto:
        cmd_auto(args.auto)
    elif args.post:
        cmd_post(args.post)
    else:
        cmd_status()
