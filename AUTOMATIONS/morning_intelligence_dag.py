#!/usr/bin/env python3
"""
Morning Intelligence DAG -- Parallel scraper pipeline replacing 3 separate crons.
================================================================================

Replaces the individual 6:00 AM / 6:15 AM cron entries for twitter, reddit, and
HN scrapers with a single DAG that:

  1. Runs ALL scrapers in parallel (twitter + reddit + hn)
  2. Merges results
  3. Feeds into alpha_auto_processor
  4. Then intelligence_router
  5. Then capital_genesis_ranker

Single cron entry at 6 AM:
  0 6 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/morning_intelligence_dag.py >> ~/.claude/logs/morning_dag.log 2>&1

Usage:
  python3 AUTOMATIONS/morning_intelligence_dag.py             # Run full DAG
  python3 AUTOMATIONS/morning_intelligence_dag.py --status    # Show last run status
  python3 AUTOMATIONS/morning_intelligence_dag.py --dry-run   # Show DAG without executing
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

# Ensure sibling modules are importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent_resilience import TrajectoryLogger

# Sovrun modules -- graceful fallback
_SOVRUN_PATH = str(Path(__file__).resolve().parent.parent / "OPEN_SOURCE" / "agent-soul")
if _SOVRUN_PATH not in sys.path:
    sys.path.insert(0, _SOVRUN_PATH)

_SOVRUN_AVAILABLE = False
try:
    from core.orchestration import DAGOrchestrator, AgentStep, StepStatus, ParallelExecutor
    _SOVRUN_AVAILABLE = True
except ImportError:
    DAGOrchestrator = None  # type: ignore[assignment, misc]
    AgentStep = None  # type: ignore[assignment, misc]
    StepStatus = None  # type: ignore[assignment, misc]
    ParallelExecutor = None  # type: ignore[assignment, misc]

_trajectory = TrajectoryLogger("morning_dag")

# === Paths ===
PROJECT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
AUTOMATIONS = PROJECT / "AUTOMATIONS"
PYTHON = sys.executable or "python3"
DAG_STATE_FILE = AUTOMATIONS / "agent" / "morning_dag_state.json"
CHECKPOINT_FILE = AUTOMATIONS / "agent" / "morning_dag_checkpoint.json"


def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [MORNING_DAG] [{level}] {msg}")


def safe_path(p: str | Path) -> Path:
    resolved = Path(p).resolve()
    if not str(resolved).startswith(str(PROJECT.resolve())):
        raise ValueError(f"BLOCKED: {resolved} outside {PROJECT}")
    return resolved


def run_script(script: str, args: str = "", timeout_sec: int = 300) -> tuple[bool, str]:
    """Run a PRINTMAXX automation script. Returns (success, output)."""
    full_path = AUTOMATIONS / script
    if not full_path.exists():
        return False, f"Script not found: {full_path}"

    cmd = f"{PYTHON} {full_path} {args}".strip()
    log(f"Running: {script} {args}")

    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=timeout_sec, cwd=str(PROJECT)
        )
        output = (result.stdout or "") + (result.stderr or "")
        output = output[-2000:]
        success = result.returncode == 0
        if success:
            log(f"  OK: {script}")
        else:
            log(f"  FAIL: {script} (rc={result.returncode})", "WARN")
        return success, output
    except subprocess.TimeoutExpired:
        log(f"  TIMEOUT: {script} after {timeout_sec}s", "WARN")
        return False, f"Timeout after {timeout_sec}s"
    except Exception as e:
        log(f"  ERROR: {script}: {e}", "ERROR")
        return False, str(e)[:500]


# === DAG Step Functions ===
# Each step receives a dict of completed step results keyed by step name.

def _scrape_twitter(results: dict[str, Any]) -> dict[str, Any]:
    """Scrape Twitter alpha (133 accounts)."""
    ok, output = run_script("twitter_alpha_scraper.py", "--all", timeout_sec=300)
    return {"status": "ok" if ok else "failed", "output_tail": output[-300:]}


def _scrape_reddit(results: dict[str, Any]) -> dict[str, Any]:
    """Scrape Reddit (18 subreddits)."""
    ok, output = run_script("background_reddit_scraper.py", "--scrape", timeout_sec=300)
    return {"status": "ok" if ok else "failed", "output_tail": output[-300:]}


def _scrape_hn(results: dict[str, Any]) -> dict[str, Any]:
    """Scrape HN + ProductHunt."""
    ok, output = run_script("hn_ph_scraper.py", "", timeout_sec=300)
    return {"status": "ok" if ok else "failed", "output_tail": output[-300:]}


def _merge_results(results: dict[str, Any]) -> dict[str, Any]:
    """Merge scraper results and report counts."""
    twitter = results.get("scrape_twitter", {})
    reddit = results.get("scrape_reddit", {})
    hn = results.get("scrape_hn", {})

    merged = {
        "twitter": twitter.get("status", "skipped"),
        "reddit": reddit.get("status", "skipped"),
        "hn": hn.get("status", "skipped"),
        "merged_at": datetime.now().isoformat(),
    }

    ok_count = sum(1 for v in [twitter, reddit, hn] if v.get("status") == "ok")
    merged["scrapers_ok"] = ok_count
    merged["scrapers_total"] = 3

    log(f"Merge: {ok_count}/3 scrapers succeeded")
    return merged


def _run_alpha_processor(results: dict[str, Any]) -> dict[str, Any]:
    """Process new alpha entries from all scrapers."""
    ok, output = run_script("alpha_auto_processor.py", "--process-new", timeout_sec=180)
    return {"status": "ok" if ok else "failed", "output_tail": output[-300:]}


def _run_intelligence_router(results: dict[str, Any]) -> dict[str, Any]:
    """Route processed alpha through intelligence router."""
    ok, output = run_script("intelligence_router.py", "--refresh", timeout_sec=120)
    return {"status": "ok" if ok else "failed", "output_tail": output[-300:]}


def _run_capital_genesis_ranker(results: dict[str, Any]) -> dict[str, Any]:
    """Rank all methods by Capital Genesis scoring."""
    ok, output = run_script("capital_genesis_ranker.py", "--rank --report", timeout_sec=120)
    return {"status": "ok" if ok else "failed", "output_tail": output[-300:]}


def build_dag_steps() -> list:
    """Build the morning intelligence DAG steps with dependencies."""
    if not _SOVRUN_AVAILABLE:
        return []

    return [
        # Layer 1: Parallel scrapers (no dependencies)
        AgentStep(name="scrape_twitter", fn=_scrape_twitter,
                  depends_on=[], timeout_seconds=360, retry_count=1),
        AgentStep(name="scrape_reddit", fn=_scrape_reddit,
                  depends_on=[], timeout_seconds=360, retry_count=1),
        AgentStep(name="scrape_hn", fn=_scrape_hn,
                  depends_on=[], timeout_seconds=360, retry_count=1),

        # Layer 2: Merge (depends on all scrapers)
        AgentStep(name="merge_results", fn=_merge_results,
                  depends_on=["scrape_twitter", "scrape_reddit", "scrape_hn"],
                  timeout_seconds=30),

        # Layer 3: Alpha processor (depends on merge)
        AgentStep(name="alpha_processor", fn=_run_alpha_processor,
                  depends_on=["merge_results"],
                  timeout_seconds=240, retry_count=1),

        # Layer 4: Intelligence router (depends on alpha processor)
        AgentStep(name="intelligence_router", fn=_run_intelligence_router,
                  depends_on=["alpha_processor"],
                  timeout_seconds=180),

        # Layer 5: Capital Genesis ranker (depends on intelligence router)
        AgentStep(name="capital_genesis_ranker", fn=_run_capital_genesis_ranker,
                  depends_on=["intelligence_router"],
                  timeout_seconds=180),
    ]


def run_dag() -> dict[str, Any]:
    """Execute the full morning intelligence DAG."""
    start = time.time()
    log("=== Morning Intelligence DAG starting ===")

    if _SOVRUN_AVAILABLE:
        steps = build_dag_steps()
        dag = DAGOrchestrator(
            steps=steps,
            max_workers=3,  # 3 scrapers in parallel
            timeout_seconds=1800,  # 30 min overall
            checkpoint_file=CHECKPOINT_FILE,
        )

        log("DAG structure:")
        log("  Layer 1 (parallel): scrape_twitter | scrape_reddit | scrape_hn")
        log("  Layer 2: merge_results")
        log("  Layer 3: alpha_processor")
        log("  Layer 4: intelligence_router")
        log("  Layer 5: capital_genesis_ranker")

        results = dag.run()

        # Collect step statuses
        step_report = {}
        for s in steps:
            step_report[s.name] = {
                "status": s.status.value,
                "duration_ms": s.duration_ms,
                "error": s.error,
            }

    else:
        # Fallback: run sequentially without sovrun
        log("Sovrun not available, running sequentially", "WARN")
        results = {}

        # Scrapers in parallel using threads (basic fallback)
        import concurrent.futures
        scraper_fns = {
            "scrape_twitter": _scrape_twitter,
            "scrape_reddit": _scrape_reddit,
            "scrape_hn": _scrape_hn,
        }

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            futures = {name: pool.submit(fn, {}) for name, fn in scraper_fns.items()}
            for name, fut in futures.items():
                try:
                    results[name] = fut.result(timeout=360)
                except Exception as e:
                    results[name] = {"status": "failed", "error": str(e)[:200]}

        # Sequential pipeline
        results["merge_results"] = _merge_results(results)
        results["alpha_processor"] = _run_alpha_processor(results)
        results["intelligence_router"] = _run_intelligence_router(results)
        results["capital_genesis_ranker"] = _run_capital_genesis_ranker(results)

        step_report = {k: {"status": v.get("status", "unknown")} for k, v in results.items()}

    elapsed = round(time.time() - start, 1)

    # Save state
    state = {
        "last_run": datetime.now().isoformat(),
        "elapsed_seconds": elapsed,
        "steps": step_report,
    }
    DAG_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    DAG_STATE_FILE.write_text(json.dumps(state, indent=2))

    log(f"=== Morning Intelligence DAG complete ({elapsed}s) ===")
    for name, info in step_report.items():
        status = info.get("status", "?")
        dur = info.get("duration_ms", 0)
        err = info.get("error", "")
        log(f"  [{status:>8}] {name:<25} {dur:>6}ms{f'  ERR: {err[:50]}' if err else ''}")

    _trajectory.log("morning_dag_complete", state)
    return state


def show_status() -> None:
    """Show status from last DAG run."""
    if not DAG_STATE_FILE.exists():
        print("No morning DAG state found. Run the DAG first.")
        return

    state = json.loads(DAG_STATE_FILE.read_text())
    print("\n=== Morning Intelligence DAG Status ===\n")
    print(f"Last run: {state.get('last_run', '?')}")
    print(f"Duration: {state.get('elapsed_seconds', '?')}s")
    print()
    for name, info in state.get("steps", {}).items():
        status = info.get("status", "?")
        dur = info.get("duration_ms", 0)
        err = info.get("error", "")
        print(f"  [{status:>8}] {name:<25} {dur:>6}ms{f'  ERR: {err[:50]}' if err else ''}")
    print()


def show_dry_run() -> None:
    """Show the DAG structure without executing."""
    print("\n=== Morning Intelligence DAG (dry run) ===\n")
    print("Layer 1 (PARALLEL):")
    print("  scrape_twitter     -- twitter_alpha_scraper.py --all (300s timeout, 1 retry)")
    print("  scrape_reddit      -- background_reddit_scraper.py --scrape (300s timeout, 1 retry)")
    print("  scrape_hn          -- hn_ph_scraper.py (300s timeout, 1 retry)")
    print()
    print("Layer 2 (after all scrapers):")
    print("  merge_results      -- combine scraper outputs, report counts")
    print()
    print("Layer 3 (after merge):")
    print("  alpha_processor    -- alpha_auto_processor.py --process-new (180s timeout)")
    print()
    print("Layer 4 (after alpha):")
    print("  intelligence_router -- intelligence_router.py --refresh (120s timeout)")
    print()
    print("Layer 5 (after router):")
    print("  capital_genesis_ranker -- capital_genesis_ranker.py --rank --report (120s timeout)")
    print()
    print("Total timeout: 1800s (30 min)")
    print(f"Sovrun available: {_SOVRUN_AVAILABLE}")
    print()
    print("Cron entry (replaces 3 separate entries):")
    print("  0 6 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && "
          "python3 AUTOMATIONS/morning_intelligence_dag.py "
          ">> ~/.claude/logs/morning_dag.log 2>&1")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Morning Intelligence DAG -- parallel scraper pipeline"
    )
    parser.add_argument("--status", action="store_true",
                        help="Show last DAG run status")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show DAG structure without executing")
    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.dry_run:
        show_dry_run()
    else:
        run_dag()


if __name__ == "__main__":
    main()
