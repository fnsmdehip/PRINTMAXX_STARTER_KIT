#!/usr/bin/env python3
"""
PRINTMAXX Closed-Loop Lead Pipeline
====================================
Implements OpenClaw crash-recovery pattern: active-tasks.md as persistent state.

Runs the full cycle:
  1. Qualify leads (website analysis, batch N from pre-filtered pool)
  2. Generate cold emails for new hot leads
  3. Update pipeline tracker
  4. Log metrics to daily memory file
  5. Update active-tasks.md for crash recovery

Designed to run unattended via cron. If interrupted, picks up exactly where it
left off on next invocation. No human review needed for the loop itself.

Usage:
    python3 AUTOMATIONS/closed_loop_pipeline.py                   # Run one cycle
    python3 AUTOMATIONS/closed_loop_pipeline.py --cycles 5        # Run 5 cycles
    python3 AUTOMATIONS/closed_loop_pipeline.py --batch 2000      # 2000 leads per cycle
    python3 AUTOMATIONS/closed_loop_pipeline.py --workers 30      # 30 parallel HTTP workers
    python3 AUTOMATIONS/closed_loop_pipeline.py --status          # Show pipeline state
    python3 AUTOMATIONS/closed_loop_pipeline.py --dry-run         # Preview what would run
    python3 AUTOMATIONS/closed_loop_pipeline.py --industry dental # Filter to industry

Memory files (OpenClaw pattern):
    OPS/active-tasks.md           — Crash recovery: what's running NOW
    AUTOMATIONS/logs/daily/       — Daily execution logs (append-only)
    AUTOMATIONS/leads/qualified/  — Long-term: all qualified lead data
"""

import csv
import json
import os
import subprocess
import sys
import time
import signal
from datetime import datetime, date
from pathlib import Path
from collections import Counter

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------

BASE = Path(__file__).resolve().parent.parent
AUTOMATIONS = BASE / "AUTOMATIONS"
OPS = BASE / "OPS"
LEADS_DIR = AUTOMATIONS / "leads"
QUALIFIED_DIR = LEADS_DIR / "qualified"
OUTREACH_DIR = AUTOMATIONS / "outreach"
LOGS = AUTOMATIONS / "logs"
DAILY_LOGS = LOGS / "daily"
CONTENT_POSTING = AUTOMATIONS / "content_posting"

PYTHON = sys.executable
TODAY = date.today().isoformat()

# Memory files (OpenClaw pattern)
ACTIVE_TASKS = OPS / "active-tasks.md"
DAILY_LOG = DAILY_LOGS / f"{TODAY}.md"
PROGRESS_FILE = QUALIFIED_DIR / "progress.json"
PIPELINE_METRICS = QUALIFIED_DIR / "pipeline_metrics.jsonl"

# Ensure dirs
for d in [QUALIFIED_DIR, OUTREACH_DIR, DAILY_LOGS, LOGS]:
    d.mkdir(parents=True, exist_ok=True)

# Graceful shutdown
shutdown_requested = False
def handle_signal(signum, frame):
    global shutdown_requested
    shutdown_requested = True
    log("SHUTDOWN REQUESTED — finishing current step then saving state")

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)


# ---------------------------------------------------------------------------
# LOGGING (dual: console + daily file)
# ---------------------------------------------------------------------------

def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(DAILY_LOG, "a") as f:
        f.write(line + "\n")


def log_metric(metric: dict):
    """Append metric to JSONL file (long-term memory)."""
    metric["timestamp"] = datetime.now().isoformat()
    metric["date"] = TODAY
    with open(PIPELINE_METRICS, "a") as f:
        f.write(json.dumps(metric) + "\n")


# ---------------------------------------------------------------------------
# ACTIVE TASKS — Crash Recovery (OpenClaw pattern)
# ---------------------------------------------------------------------------

def read_active_tasks() -> dict:
    """Read active-tasks.md and parse current state."""
    if not ACTIVE_TASKS.exists():
        return {}
    text = ACTIVE_TASKS.read_text()
    state = {}
    # Parse simple key: value pairs from markdown
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("- **") and ":**" in line:
            key = line.split("**")[1].rstrip(":")
            val = line.split(":**", 1)[1].strip()
            state[key] = val
    return state


def write_active_tasks(phase: str, details: dict):
    """Write current task state for crash recovery."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# Active Tasks — {now}",
        "",
        f"## Currently Running: {phase}",
        "",
    ]
    for k, v in details.items():
        lines.append(f"- **{k}:** {v}")
    lines.append("")
    lines.append("## Recent Pipeline State")
    lines.append("")

    # Add pipeline snapshot
    progress = load_progress()
    if progress:
        pf = progress.get("prefilter", {})
        an = progress.get("analysis", {})
        lines.append(f"- **Total pre-filtered:** {pf.get('unique_domains', '?'):,}")
        lines.append(f"- **Analyzed so far:** {an.get('total_analyzed', 0):,}")
        hot = count_csv_rows(QUALIFIED_DIR / "HOT_LEADS_QUALIFIED.csv")
        warm = count_csv_rows(QUALIFIED_DIR / "WARM_LEADS_QUALIFIED.csv")
        lines.append(f"- **Hot leads:** {hot:,}")
        lines.append(f"- **Warm leads:** {warm:,}")
    lines.append("")
    lines.append("---")
    lines.append(f"*Last updated: {now}*")

    ACTIVE_TASKS.write_text("\n".join(lines))


def clear_active_tasks():
    """Clear after successful completion."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ACTIVE_TASKS.write_text(
        f"# Active Tasks — {now}\n\n"
        f"No tasks currently running. Pipeline idle.\n\n"
        f"Last successful run: {now}\n"
    )


# ---------------------------------------------------------------------------
# UTILITIES
# ---------------------------------------------------------------------------

def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {}


def count_csv_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with open(path, "r") as f:
        return sum(1 for _ in f) - 1  # minus header


def run_script(cmd: list, timeout: int = 600, label: str = "") -> tuple:
    """Run a script, capture output. Returns (success, stdout)."""
    log(f"  EXEC: {' '.join(cmd[:6])}...")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(BASE),
        )
        if result.returncode == 0:
            log(f"  OK: {label}")
            return True, result.stdout
        else:
            log(f"  FAIL ({result.returncode}): {label}")
            if result.stderr:
                log(f"  STDERR: {result.stderr[:500]}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        log(f"  TIMEOUT ({timeout}s): {label}")
        return False, "TIMEOUT"
    except Exception as e:
        log(f"  ERROR: {e}")
        return False, str(e)


def get_new_hot_leads_since(last_count: int) -> int:
    """How many new hot leads since last cycle."""
    current = count_csv_rows(QUALIFIED_DIR / "HOT_LEADS_QUALIFIED.csv")
    return max(0, current - last_count)


# ---------------------------------------------------------------------------
# PIPELINE STEPS
# ---------------------------------------------------------------------------

def step_qualify_leads(batch_size: int = 1000, workers: int = 20, industry: str = "") -> dict:
    """Step 1: Run lead qualification batch."""
    hot_before = count_csv_rows(QUALIFIED_DIR / "HOT_LEADS_QUALIFIED.csv")
    warm_before = count_csv_rows(QUALIFIED_DIR / "WARM_LEADS_QUALIFIED.csv")

    cmd = [
        PYTHON, str(AUTOMATIONS / "intelligent_lead_qualifier.py"),
        "--analyze",
        "--batch", str(batch_size),
        "--workers", str(workers),
    ]
    if industry:
        cmd.extend(["--industry", industry])

    success, output = run_script(cmd, timeout=900, label=f"Qualify {batch_size} leads")

    hot_after = count_csv_rows(QUALIFIED_DIR / "HOT_LEADS_QUALIFIED.csv")
    warm_after = count_csv_rows(QUALIFIED_DIR / "WARM_LEADS_QUALIFIED.csv")

    result = {
        "step": "qualify",
        "success": success,
        "batch_size": batch_size,
        "new_hot": hot_after - hot_before,
        "new_warm": warm_after - warm_before,
        "total_hot": hot_after,
        "total_warm": warm_after,
    }
    log_metric(result)
    return result


def step_generate_emails(industry: str = "", min_score: int = 60) -> dict:
    """Step 2: Generate cold emails for hot leads."""
    # Check if we have the input file
    input_file = QUALIFIED_DIR / "HOT_LEADS_QUALIFIED.csv"
    if not input_file.exists():
        return {"step": "email_gen", "success": False, "reason": "No hot leads file"}

    hot_count = count_csv_rows(input_file)
    if hot_count == 0:
        return {"step": "email_gen", "success": False, "reason": "0 hot leads"}

    # Output per industry or general
    output_dir = BASE / "output" / "cold_emails"
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        PYTHON, str(AUTOMATIONS / "generate_cold_emails.py"),
        "--input", str(input_file),
        "--output", str(output_dir),
        "--format", "instantly",
        "--min-score", str(min_score),
    ]
    if industry:
        cmd.extend(["--industry", industry])

    success, output = run_script(cmd, timeout=300, label=f"Generate emails (industry={industry or 'all'})")

    # Count output files
    email_files = list(output_dir.glob("*.csv"))
    total_emails = sum(count_csv_rows(f) for f in email_files)

    result = {
        "step": "email_gen",
        "success": success,
        "hot_leads_input": hot_count,
        "email_files": len(email_files),
        "total_emails_generated": total_emails,
    }
    log_metric(result)
    return result


def step_update_pipeline_tracker() -> dict:
    """Step 3: Update pipeline tracker with new qualified leads."""
    tracker_file = OUTREACH_DIR / "PIPELINE_TRACKER.csv"
    hot_file = QUALIFIED_DIR / "HOT_LEADS_QUALIFIED.csv"

    if not hot_file.exists():
        return {"step": "pipeline_update", "success": False, "reason": "No hot leads"}

    # Read existing pipeline entries
    existing_domains = set()
    if tracker_file.exists():
        with open(tracker_file, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                domain = row.get("domain", row.get("website", "")).strip().lower()
                if domain:
                    existing_domains.add(domain)

    # Read hot leads
    new_entries = []
    with open(hot_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            domain = row.get("domain", "").strip().lower()
            if domain and domain not in existing_domains:
                new_entries.append({
                    "domain": domain,
                    "business_name": row.get("name", ""),
                    "category": row.get("category", ""),
                    "city": row.get("city", ""),
                    "state": row.get("state", ""),
                    "email": row.get("email", ""),
                    "phone": row.get("phone", ""),
                    "total_score": row.get("total_score", ""),
                    "status": "QUALIFIED",
                    "added_date": TODAY,
                    "email_sent": "FALSE",
                    "response": "",
                    "notes": "",
                })

    # Append new entries
    if new_entries:
        write_header = not tracker_file.exists() or tracker_file.stat().st_size == 0
        with open(tracker_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(new_entries[0].keys()))
            if write_header:
                writer.writeheader()
            writer.writerows(new_entries)

    result = {
        "step": "pipeline_update",
        "success": True,
        "new_entries": len(new_entries),
        "total_pipeline": len(existing_domains) + len(new_entries),
    }
    log_metric(result)
    return result


def step_report_metrics() -> dict:
    """Step 4: Calculate and report cycle metrics."""
    progress = load_progress()
    pf = progress.get("prefilter", {})
    an = progress.get("analysis", {})

    total_pool = pf.get("unique_domains", 0)
    analyzed = an.get("total_analyzed", 0)
    remaining = total_pool - analyzed
    hot = count_csv_rows(QUALIFIED_DIR / "HOT_LEADS_QUALIFIED.csv")
    warm = count_csv_rows(QUALIFIED_DIR / "WARM_LEADS_QUALIFIED.csv")

    # Calculate rates
    hot_rate = (hot / analyzed * 100) if analyzed > 0 else 0
    warm_rate = (warm / analyzed * 100) if analyzed > 0 else 0

    # Read pipeline tracker
    pipeline_count = count_csv_rows(OUTREACH_DIR / "PIPELINE_TRACKER.csv")

    # Read email output
    email_dir = BASE / "output" / "cold_emails"
    email_count = sum(count_csv_rows(f) for f in email_dir.glob("*.csv")) if email_dir.exists() else 0

    metrics = {
        "step": "metrics",
        "total_pool": total_pool,
        "analyzed": analyzed,
        "remaining": remaining,
        "pct_complete": round(analyzed / total_pool * 100, 1) if total_pool > 0 else 0,
        "hot_leads": hot,
        "warm_leads": warm,
        "hot_rate_pct": round(hot_rate, 1),
        "warm_rate_pct": round(warm_rate, 1),
        "pipeline_entries": pipeline_count,
        "emails_generated": email_count,
    }
    log_metric(metrics)
    return metrics


# ---------------------------------------------------------------------------
# MAIN CYCLE
# ---------------------------------------------------------------------------

def run_cycle(batch_size: int = 1000, workers: int = 20, industry: str = "",
              min_score: int = 60, dry_run: bool = False) -> dict:
    """Run one complete pipeline cycle."""
    cycle_start = time.time()
    cycle_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    log(f"\n{'='*60}")
    log(f"CYCLE {cycle_id} — batch={batch_size}, workers={workers}")
    log(f"{'='*60}")

    if dry_run:
        progress = load_progress()
        pf = progress.get("prefilter", {})
        an = progress.get("analysis", {})
        remaining = pf.get("unique_domains", 0) - an.get("total_analyzed", 0)
        log(f"DRY RUN — would analyze {min(batch_size, remaining)} of {remaining:,} remaining leads")
        log(f"Current: {count_csv_rows(QUALIFIED_DIR / 'HOT_LEADS_QUALIFIED.csv'):,} hot, "
            f"{count_csv_rows(QUALIFIED_DIR / 'WARM_LEADS_QUALIFIED.csv'):,} warm")
        return {"dry_run": True}

    results = {}

    # Step 1: Qualify leads
    write_active_tasks("Lead Qualification", {
        "batch_size": str(batch_size),
        "workers": str(workers),
        "industry": industry or "all",
        "cycle_id": cycle_id,
    })
    log("\n--- STEP 1: QUALIFY LEADS ---")
    results["qualify"] = step_qualify_leads(batch_size, workers, industry)
    log(f"  +{results['qualify']['new_hot']} hot, +{results['qualify']['new_warm']} warm")

    if shutdown_requested:
        log("Shutdown requested — saving state and exiting")
        write_active_tasks("INTERRUPTED", {"last_step": "qualify", "cycle_id": cycle_id})
        return results

    # Step 2: Generate cold emails
    write_active_tasks("Cold Email Generation", {"cycle_id": cycle_id})
    log("\n--- STEP 2: GENERATE COLD EMAILS ---")
    results["email_gen"] = step_generate_emails(industry, min_score)
    log(f"  {results['email_gen'].get('total_emails_generated', 0)} emails ready")

    if shutdown_requested:
        log("Shutdown requested — saving state and exiting")
        write_active_tasks("INTERRUPTED", {"last_step": "email_gen", "cycle_id": cycle_id})
        return results

    # Step 3: Update pipeline tracker
    write_active_tasks("Pipeline Update", {"cycle_id": cycle_id})
    log("\n--- STEP 3: UPDATE PIPELINE ---")
    results["pipeline"] = step_update_pipeline_tracker()
    log(f"  +{results['pipeline']['new_entries']} new pipeline entries")

    # Step 4: Report metrics
    log("\n--- STEP 4: METRICS ---")
    results["metrics"] = step_report_metrics()
    m = results["metrics"]
    log(f"  Pool: {m['analyzed']:,}/{m['total_pool']:,} analyzed ({m['pct_complete']}%)")
    log(f"  Hot: {m['hot_leads']:,} ({m['hot_rate_pct']}%)  Warm: {m['warm_leads']:,} ({m['warm_rate_pct']}%)")
    log(f"  Pipeline: {m['pipeline_entries']:,}  Emails: {m['emails_generated']:,}")

    # Step 5: Auto-generate content from metrics (Max Squeeze)
    log("\n--- STEP 5: AUTO-CONTENT + MEMORY ---")
    content_cmd = [PYTHON, str(AUTOMATIONS / "auto_content_from_metrics.py")]
    run_script(content_cmd, timeout=30, label="Auto-content from metrics")
    # Update memory/heartbeat
    memory_cmd = [PYTHON, str(AUTOMATIONS / "memory_manager.py"), "--heartbeat"]
    run_script(memory_cmd, timeout=30, label="Heartbeat update")

    cycle_time = time.time() - cycle_start
    log(f"\nCycle completed in {cycle_time:.0f}s")

    # Clear active tasks on success
    clear_active_tasks()

    return results


def show_status():
    """Show full pipeline status."""
    progress = load_progress()
    pf = progress.get("prefilter", {})
    an = progress.get("analysis", {})

    total = pf.get("unique_domains", 0)
    analyzed = an.get("total_analyzed", 0)
    hot = count_csv_rows(QUALIFIED_DIR / "HOT_LEADS_QUALIFIED.csv")
    warm = count_csv_rows(QUALIFIED_DIR / "WARM_LEADS_QUALIFIED.csv")
    pipeline = count_csv_rows(OUTREACH_DIR / "PIPELINE_TRACKER.csv")

    email_dir = BASE / "output" / "cold_emails"
    emails = sum(count_csv_rows(f) for f in email_dir.glob("*.csv")) if email_dir.exists() else 0

    print(f"""
╔══════════════════════════════════════════════════════════╗
║           PRINTMAXX CLOSED-LOOP PIPELINE STATUS          ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Lead Pool:       {total:>10,} unique domains              ║
║  Analyzed:        {analyzed:>10,} ({analyzed/total*100 if total else 0:>5.1f}%)                  ║
║  Remaining:       {total-analyzed:>10,}                              ║
║                                                          ║
║  Hot Leads:       {hot:>10,} (score >= 65)                 ║
║  Warm Leads:      {warm:>10,} (score 45-64)                ║
║  Hot Rate:        {hot/analyzed*100 if analyzed else 0:>9.1f}%                            ║
║                                                          ║
║  Pipeline:        {pipeline:>10,} entries                    ║
║  Emails Ready:    {emails:>10,}                              ║
║                                                          ║
║  Speed:           ~12 sites/sec @ 30 workers              ║
║  ETA (all):       ~{(total-analyzed)/12/3600:.0f} hours ({(total-analyzed)/12/3600/24:.0f} days)                        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")

    # Show active task if any
    if ACTIVE_TASKS.exists():
        state = read_active_tasks()
        if state:
            print("Active task state:")
            for k, v in state.items():
                print(f"  {k}: {v}")

    # Show recent metrics
    if PIPELINE_METRICS.exists():
        print("\nRecent metrics (last 5):")
        lines = PIPELINE_METRICS.read_text().strip().split("\n")
        for line in lines[-5:]:
            try:
                m = json.loads(line)
                if m.get("step") == "metrics":
                    print(f"  [{m['timestamp'][:16]}] analyzed={m['analyzed']:,} hot={m['hot_leads']:,} "
                          f"warm={m['warm_leads']:,} pipeline={m['pipeline_entries']:,}")
            except:
                pass


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description='PRINTMAXX Closed-Loop Lead Pipeline')
    parser.add_argument('--cycles', type=int, default=1, help='Number of cycles to run (default: 1)')
    parser.add_argument('--batch', type=int, default=1000, help='Leads per cycle (default: 1000)')
    parser.add_argument('--workers', type=int, default=20, help='Parallel HTTP workers (default: 20)')
    parser.add_argument('--industry', type=str, default='', help='Filter to industry')
    parser.add_argument('--min-score', type=int, default=60, help='Min score for email gen (default: 60)')
    parser.add_argument('--status', action='store_true', help='Show pipeline status')
    parser.add_argument('--dry-run', action='store_true', help='Preview only')
    parser.add_argument('--cool-down', type=int, default=30, help='Seconds between cycles (default: 30)')

    args = parser.parse_args()

    if args.status:
        show_status()
        return

    log(f"PRINTMAXX Closed-Loop Pipeline — {args.cycles} cycle(s), batch={args.batch}")
    log(f"Date: {TODAY}")

    for i in range(args.cycles):
        if shutdown_requested:
            log(f"Shutdown requested before cycle {i+1}")
            break

        if i > 0:
            log(f"\nCooling down {args.cool_down}s before next cycle...")
            time.sleep(args.cool_down)

        log(f"\n{'='*60}")
        log(f"CYCLE {i+1}/{args.cycles}")
        log(f"{'='*60}")

        results = run_cycle(
            batch_size=args.batch,
            workers=args.workers,
            industry=args.industry,
            min_score=args.min_score,
            dry_run=args.dry_run,
        )

        if args.dry_run:
            break

    log(f"\nAll cycles complete.")


if __name__ == "__main__":
    main()
