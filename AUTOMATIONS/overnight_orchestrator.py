#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Overnight Pipeline Orchestrator
3-phase dependency-aware pipeline. Each phase runs tasks in parallel.
Phase 2 waits for Phase 1. Phase 3 waits for Phase 2.

Usage:
    python3 overnight_orchestrator.py --run          # full orchestration
    python3 overnight_orchestrator.py --dry-run      # show execution plan
    python3 overnight_orchestrator.py --status        # last run results
    python3 overnight_orchestrator.py --phase 2       # run only phase 2
    python3 overnight_orchestrator.py --task closed_loop_pipeline  # single task
"""
import argparse, fcntl, json, logging, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
LOCK_FILE = BASE / ".overnight_orchestrator.lock"
LOG_DIR = BASE / "logs"
TODAY = datetime.now().strftime("%Y-%m-%d")
LOG_PATH = LOG_DIR / f"overnight_orchestrator_{TODAY}.log"
STATUS_PATH = LOG_DIR / f"overnight_status_{TODAY}.json"

TASK_TIMEOUT = 1800   # 30 min per task
TOTAL_TIMEOUT = 10800 # 3 hours total
RETRY_DELAY = 60      # seconds before retry

PHASES = {
    1: [
        ("closed_loop_pipeline", "closed_loop_pipeline.py",
         ["--cycles", "5", "--batch", "2000"]),
        ("intelligent_lead_qualifier", "intelligent_lead_qualifier.py",
         ["--analyze", "--batch", "2000"]),
        ("memory_manager_full", "memory_manager.py", ["--full"]),
    ],
    2: [
        ("generate_cold_emails", "generate_cold_emails.py",
         ["--input", "leads/qualified/HOT_LEADS_QUALIFIED.csv"]),
        ("personalize_demos", "personalize_demos.py", ["--top", "200"]),
        ("seo_competitor_analyzer", "seo_competitor_analyzer.py",
         ["--all-hot", "--summary"]),
    ],
    3: [
        ("refresh_dashboard", "refresh_dashboard.py", ["--no-open"]),
        ("auto_content_from_metrics", "auto_content_from_metrics.py", []),
        ("memory_manager_log", "memory_manager.py",
         ["--log", "Overnight run complete"]),
    ],
}

ALL_TASKS = {name: (script, args) for tasks in PHASES.values()
             for name, script, args in tasks}

# --- Logging ---
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger = logging.getLogger("overnight")
logger.setLevel(logging.DEBUG)
_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
_fh = logging.FileHandler(LOG_PATH); _fh.setFormatter(_fmt); logger.addHandler(_fh)
_ch = logging.StreamHandler(sys.stdout); _ch.setFormatter(_fmt); logger.addHandler(_ch)

# --- Lock ---
_lock_fd = None

def acquire_lock() -> bool:
    global _lock_fd
    try:
        _lock_fd = open(LOCK_FILE, "w")
        fcntl.flock(_lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        _lock_fd.write(f"{datetime.now(timezone.utc).isoformat()}\npid={sys.argv}\n")
        _lock_fd.flush()
        return True
    except (IOError, OSError):
        return False

def release_lock():
    global _lock_fd
    if _lock_fd:
        try: fcntl.flock(_lock_fd, fcntl.LOCK_UN); _lock_fd.close()
        except Exception: pass
        try: LOCK_FILE.unlink(missing_ok=True)
        except Exception: pass
        _lock_fd = None

# --- Task execution ---

def _result(name, status, details, ts, elapsed):
    return {"task": name, "status": status, "details": details,
            "time": ts, "elapsed_s": elapsed}

def run_task(name: str, script: str, args: list, attempt: int = 1) -> dict:
    cmd = [sys.executable, str(BASE / script)] + args
    start = time.monotonic()
    ts = datetime.now(timezone.utc).isoformat()
    logger.info("START %s (attempt %d): %s", name, attempt, " ".join(cmd))
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=TASK_TIMEOUT, cwd=str(BASE))
        elapsed = round(time.monotonic() - start, 1)
        if proc.returncode == 0:
            logger.info("OK    %s in %.1fs", name, elapsed)
            return _result(name, "SUCCESS", f"exit 0 in {elapsed}s", ts, elapsed)
        detail = f"exit {proc.returncode} in {elapsed}s"
        stderr_tail = (proc.stderr or "")[-300:].strip()
        if stderr_tail:
            detail += f" | {stderr_tail}"
        logger.warning("FAIL  %s: %s", name, detail)
        return _result(name, "FAILED", detail, ts, elapsed)
    except subprocess.TimeoutExpired:
        elapsed = round(time.monotonic() - start, 1)
        logger.error("TIMEOUT %s after %.1fs", name, elapsed)
        return _result(name, "TIMEOUT", f"exceeded {TASK_TIMEOUT}s", ts, elapsed)
    except Exception as exc:
        elapsed = round(time.monotonic() - start, 1)
        logger.error("ERROR %s: %s", name, exc)
        return _result(name, "ERROR", str(exc)[:300], ts, elapsed)

# --- Phase runner ---

def run_phase(phase_num: int, results: list) -> bool:
    tasks = PHASES[phase_num]
    logger.info("=" * 60)
    logger.info("PHASE %d -- %d tasks", phase_num, len(tasks))
    logger.info("=" * 60)

    phase_results = []
    with ThreadPoolExecutor(max_workers=len(tasks)) as pool:
        futures = {pool.submit(run_task, n, s, a): n for n, s, a in tasks}
        for f in as_completed(futures):
            phase_results.append(f.result())

    # Retry failed tasks once
    to_retry = [r for r in phase_results if r["status"] != "SUCCESS"]
    if to_retry:
        logger.info("Retrying %d failed task(s) after %ds...",
                     len(to_retry), RETRY_DELAY)
        time.sleep(RETRY_DELAY)
        retry_results = []
        for r in to_retry:
            script, args = ALL_TASKS[r["task"]]
            retry_results.append(run_task(r["task"], script, args, attempt=2))
        retried = {r["task"] for r in retry_results}
        phase_results = [r for r in phase_results if r["task"] not in retried]
        phase_results.extend(retry_results)

    results.extend(phase_results)
    failed = [r for r in phase_results if r["status"] != "SUCCESS"]
    if failed:
        logger.warning("PHASE %d: %d failure(s): %s", phase_num,
                        len(failed), ", ".join(r["task"] for r in failed))
        return False
    logger.info("PHASE %d -- ALL OK", phase_num)
    return True

# --- Summary display ---

def _print_summary(summary: dict):
    print(f"\n{'='*60}")
    print(f"  OVERNIGHT ORCHESTRATOR -- {summary['run_date']}")
    print(f"{'='*60}")
    print(f"  Total time : {summary['total_elapsed_s']}s")
    print(f"  Tasks      : {summary['succeeded']}/{summary['tasks_run']} succeeded")
    print(f"  Phases     : {summary['phases_run']}")
    print(f"{'='*60}")
    for t in summary["tasks"]:
        icon = "OK" if t["status"] == "SUCCESS" else "XX"
        print(f"  [{icon}] {t['task']:<35s} {t['status']:<10s}"
              f" {t.get('elapsed_s',0):>7.1f}s")
    print(f"{'='*60}")
    print(f"  Log    : {LOG_PATH}")
    print(f"  Status : {STATUS_PATH}\n")

# --- Full orchestration ---

def run_full(phase_filter=None):
    if not acquire_lock():
        logger.error("Lock file exists -- another run is active. Aborting.")
        print(f"ERROR: Another orchestrator is running. Lock: {LOCK_FILE}")
        sys.exit(1)

    t0 = time.monotonic()
    results = []
    phases = [phase_filter] if phase_filter else [1, 2, 3]

    try:
        logger.info("OVERNIGHT ORCHESTRATOR START -- phases %s", phases)
        for p in phases:
            if time.monotonic() - t0 > TOTAL_TIMEOUT:
                logger.error("Total timeout exceeded. Stopping."); break
            run_phase(p, results)

        elapsed = round(time.monotonic() - t0, 1)
        ok = sum(1 for r in results if r["status"] == "SUCCESS")
        summary = {
            "run_date": TODAY,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "total_elapsed_s": elapsed, "tasks_run": len(results),
            "succeeded": ok, "failed": len(results) - ok,
            "phases_run": phases, "tasks": results,
        }
        STATUS_PATH.write_text(json.dumps(summary, indent=2) + "\n")
        logger.info("DONE -- %d/%d in %.1fs", ok, len(results), elapsed)
        _print_summary(summary)
    finally:
        release_lock()

# --- Single-task runner ---

def run_single_task(task_name: str):
    if task_name not in ALL_TASKS:
        print(f"ERROR: Unknown task '{task_name}'")
        print(f"Available: {', '.join(sorted(ALL_TASKS))}"); sys.exit(1)
    script, args = ALL_TASKS[task_name]
    res = run_task(task_name, script, args)
    if res["status"] != "SUCCESS":
        logger.info("Retrying %s after %ds...", task_name, RETRY_DELAY)
        time.sleep(RETRY_DELAY)
        res = run_task(task_name, script, args, attempt=2)
    icon = "OK" if res["status"] == "SUCCESS" else "XX"
    print(f"[{icon}] {res['task']}: {res['status']} ({res['elapsed_s']:.1f}s)")
    print(f"  {res['details']}")

# --- Dry run ---

def dry_run():
    print(f"\n{'='*60}")
    print(f"  OVERNIGHT ORCHESTRATOR -- DRY RUN")
    print(f"  Date        : {TODAY}")
    print(f"  Task timeout: {TASK_TIMEOUT}s ({TASK_TIMEOUT//60} min)")
    print(f"  Total timeout: {TOTAL_TIMEOUT}s ({TOTAL_TIMEOUT//3600} hr)")
    print(f"  Retry delay : {RETRY_DELAY}s")
    print(f"  Lock file   : {LOCK_FILE}")
    print(f"  Log file    : {LOG_PATH}")
    print(f"  Status file : {STATUS_PATH}")
    print(f"{'='*60}")
    for pn in sorted(PHASES):
        deps = "no deps" if pn == 1 else f"after phase {pn - 1}"
        print(f"\n  PHASE {pn} (parallel, {deps}) -- {len(PHASES[pn])} tasks:")
        print(f"  {'-'*56}")
        for name, script, args in PHASES[pn]:
            print(f"    {name:<35s} python3 {script} {' '.join(args)}")
        print(f"  {'-'*56}")
    print(f"\n  Execution order:")
    print(f"    Phase 1 (3 parallel) -> Phase 2 (3 parallel) -> Phase 3 (3 parallel)")
    print(f"  Total: {sum(len(t) for t in PHASES.values())} tasks, 3 phases")
    print(f"  Failed tasks retry once after {RETRY_DELAY}s\n")

# --- Status display ---

def show_status():
    candidates = sorted(LOG_DIR.glob("overnight_orchestrator_*.json"), reverse=True)
    if not candidates:
        candidates = sorted(LOG_DIR.glob("overnight_status_*.json"), reverse=True)
    if not candidates:
        print("No previous run found."); sys.exit(0)
    path = candidates[0]
    raw = path.read_text()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = None
    if isinstance(data, dict) and "tasks" in data:
        _print_summary(data); return
    # Legacy JSONL format
    print(f"\n  Last run status from: {path.name}")
    entries = data if isinstance(data, list) else []
    if not entries:
        for line in raw.strip().split("\n"):
            line = line.strip().rstrip(",")
            if not line or line in ("[]", "[", "]"): continue
            try: entries.append(json.loads(line))
            except json.JSONDecodeError: continue
    ok = sum(1 for e in entries if e.get("status") == "SUCCESS")
    print(f"  {ok}/{len(entries)} succeeded\n")
    for e in entries:
        s = e.get("status", "?")
        n = e.get("script", e.get("task", "?"))
        icon = "OK" if s == "SUCCESS" else "XX"
        print(f"  [{icon}] {n:<35s} {s}")
    print()

# --- CLI ---

def main():
    p = argparse.ArgumentParser(
        description="PRINTMAXX Overnight Pipeline Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="  python3 overnight_orchestrator.py --run\n"
               "  python3 overnight_orchestrator.py --dry-run\n"
               "  python3 overnight_orchestrator.py --phase 2\n"
               "  python3 overnight_orchestrator.py --task generate_cold_emails")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--run", action="store_true", help="Execute full orchestration")
    g.add_argument("--dry-run", action="store_true", help="Show execution plan")
    g.add_argument("--status", action="store_true", help="Show last run results")
    g.add_argument("--phase", type=int, choices=[1, 2, 3], help="Run single phase")
    g.add_argument("--task", type=str, help="Run single task by name")
    args = p.parse_args()
    if args.dry_run: dry_run()
    elif args.status: show_status()
    elif args.task: run_single_task(args.task)
    elif args.phase: run_full(phase_filter=args.phase)
    elif args.run: run_full()

if __name__ == "__main__":
    main()
