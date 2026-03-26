#!/usr/bin/env python3
"""
App Factory Auto-Orchestrator
Runs the full pipeline autonomously: scan → generate → test → queue for submission → distribute

Cron: daily 6:30 AM
No human prompting required. Human does: account creation, final review, payments.
System does: everything else.
"""

import subprocess
import sys
import json
import csv
import os
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
APP_FACTORY = PROJECT_ROOT / "AUTOMATIONS" / "app_factory"
BUILDS = PROJECT_ROOT / "MONEY_METHODS" / "APP_FACTORY" / "builds"
LEDGER = PROJECT_ROOT / "LEDGER"
OPS = PROJECT_ROOT / "OPS"
LOG_DIR = APP_FACTORY / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_DIR / "orchestrator.log", "a") as f:
        f.write(line + "\n")

def run_script(name: str, args: list, timeout: int = 300) -> tuple:
    """Run a pipeline script and return (success, output)"""
    script = APP_FACTORY / name
    if not script.exists():
        log(f"SKIP: {name} not found")
        return False, f"{name} not found"

    cmd = [sys.executable, str(script)] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=str(PROJECT_ROOT))
        output = result.stdout + result.stderr
        success = result.returncode == 0
        if not success:
            log(f"WARN: {name} exited with code {result.returncode}")
        return success, output
    except subprocess.TimeoutExpired:
        log(f"TIMEOUT: {name} exceeded {timeout}s")
        return False, f"Timeout after {timeout}s"
    except Exception as e:
        log(f"ERROR: {name} failed: {e}")
        return False, str(e)

def stage_scan():
    """Stage 1: Scan for opportunities"""
    log("=== STAGE 1: Opportunity Scan ===")
    success, output = run_script("opportunity_scanner.py", ["--scan", "--sources", "alpha,appstore"], timeout=120)

    opp_file = LEDGER / "APP_FACTORY_OPPORTUNITIES.csv"
    if opp_file.exists():
        with open(opp_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            high_score = [r for r in rows if float(r.get('score', 0)) >= 70]
            log(f"Found {len(rows)} total opportunities, {len(high_score)} scored >=70")
            return high_score
    else:
        log("No opportunities file generated")
        return []

def stage_generate(opportunities: list, max_apps: int = 2):
    """Stage 2: Generate apps from top opportunities"""
    log("=== STAGE 2: App Generation ===")
    generated = []

    for opp in opportunities[:max_apps]:
        niche = opp.get('niche', 'health_fitness')
        name = opp.get('suggested_name', opp.get('keyword', 'NewApp')).replace(' ', '')

        # Check if app already exists
        slug = name.lower().replace(' ', '-')
        if (BUILDS / slug).exists():
            log(f"SKIP: {slug} already exists in builds/")
            continue

        log(f"Generating: {name} (niche: {niche})")
        success, output = run_script("app_generator.py", [
            "--generate", "--niche", niche, "--name", name
        ], timeout=60)

        if success:
            generated.append(slug)
            log(f"Generated: {slug}")
        else:
            log(f"FAIL: Could not generate {name}")

    return generated

def stage_deep_qa(app_slugs: list = None):
    """Stage 3a: Deep functional QA"""
    log("=== STAGE 3a: Deep QA ===")

    if app_slugs:
        for slug in app_slugs:
            app_path = BUILDS / slug
            if app_path.exists():
                success, output = run_script("deep_qa.py", [
                    "--test", str(app_path)
                ], timeout=120)
                log(f"Deep QA {slug}: {'PASS' if success else 'ISSUES FOUND'}")
    else:
        success, output = run_script("deep_qa.py", ["--test-all"], timeout=300)
        log(f"Deep QA all: {'PASS' if success else 'SOME ISSUES'}")

def stage_test(app_slugs: list = None):
    """Stage 3b: Static rejection tests"""
    log("=== STAGE 3b: Static Testing ===")

    if app_slugs:
        results = {}
        for slug in app_slugs:
            app_path = BUILDS / slug
            if app_path.exists():
                success, output = run_script("test_runner.py", [
                    "--test", str(app_path), "--static-only"
                ], timeout=120)
                # Parse pass/fail from output
                passed = "PASS" in output.split('\n')[-5:] if output else False
                results[slug] = passed
                log(f"Test {slug}: {'PASS' if passed else 'FAIL'}")
    else:
        success, output = run_script("test_runner.py", ["--test-all", "--static-only"], timeout=300)
        results = {"all": success}
        log(f"Test all: {'PASS' if success else 'SOME FAILURES'}")

    return results

def stage_distribute(app_slugs: list = None):
    """Stage 4: Generate distribution assets"""
    log("=== STAGE 4: Distribution ===")

    targets = app_slugs or []
    if not targets:
        # Distribute for all existing builds
        if BUILDS.exists():
            targets = [d.name for d in BUILDS.iterdir() if d.is_dir() and (d / "app.json").exists()]

    for slug in targets:
        app_path = BUILDS / slug
        if app_path.exists():
            log(f"Generating distribution for: {slug}")
            success, output = run_script("distribution_engine.py", [
                "--full", str(app_path)
            ], timeout=120)
            if success:
                log(f"Distribution assets created for {slug}")
            else:
                log(f"Distribution failed for {slug}: check logs")

def stage_optimize():
    """Stage 5: Portfolio optimization (weekly)"""
    log("=== STAGE 5: Portfolio Optimization ===")

    # Only run on Mondays or if forced
    if datetime.now().weekday() != 0:  # 0 = Monday
        log("SKIP: Portfolio optimization runs on Mondays only")
        return

    success, output = run_script("portfolio_optimizer.py", ["--optimize"], timeout=120)
    if success:
        log("Portfolio optimization complete")
    else:
        log("Portfolio optimization failed")

def log_session_decisions(decisions: dict):
    """Log all decisions made this run to the audit CSV"""
    csv_path = LEDGER / "APP_FACTORY_DECISIONS.csv"
    file_exists = csv_path.exists()

    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "stage", "action", "target", "details"])

        ts = datetime.now().isoformat()
        for stage, actions in decisions.items():
            if isinstance(actions, list):
                for action in actions:
                    writer.writerow([ts, stage, action.get("action", ""), action.get("target", ""), action.get("details", "")])
            elif isinstance(actions, dict):
                for target, result in actions.items():
                    writer.writerow([ts, stage, "result", target, str(result)])

def run_full_pipeline(dry_run: bool = False):
    """Execute the full autonomous pipeline"""
    log("=" * 60)
    log("APP FACTORY AUTO-ORCHESTRATOR starting")
    log(f"Dry run: {dry_run}")
    log("=" * 60)

    decisions = {}

    # Stage 1: Scan
    opportunities = stage_scan()
    decisions["scan"] = [{"action": "found", "target": "opportunities", "details": f"{len(opportunities)} high-score opportunities"}]

    # Stage 2: Generate (only if new high-score opportunities)
    generated = []
    if opportunities and not dry_run:
        generated = stage_generate(opportunities, max_apps=2)
        decisions["generate"] = [{"action": "generated", "target": slug, "details": "new app"} for slug in generated]

    # Stage 3a: Deep functional QA
    stage_deep_qa(generated if generated else None)

    # Stage 3b: Static rejection tests
    test_results = stage_test(generated if generated else None)
    decisions["test"] = test_results

    # Stage 4: Distribution assets for new apps
    if generated and not dry_run:
        stage_distribute(generated)
        decisions["distribute"] = [{"action": "distributed", "target": slug, "details": "assets created"} for slug in generated]

    # Stage 5: Weekly optimization
    stage_optimize()

    # Log decisions
    log_session_decisions(decisions)

    # Summary
    log("")
    log("=" * 60)
    log("PIPELINE COMPLETE")
    log(f"  Opportunities found: {len(opportunities)}")
    log(f"  Apps generated: {len(generated)}")
    log(f"  Tests run: {len(test_results)}")
    log(f"  Decisions logged to: LEDGER/APP_FACTORY_DECISIONS.csv")
    log("=" * 60)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="App Factory Auto-Orchestrator")
    parser.add_argument("--full", action="store_true", help="Run full pipeline")
    parser.add_argument("--scan-only", action="store_true", help="Only run opportunity scanner")
    parser.add_argument("--test-only", action="store_true", help="Only run tests on existing apps")
    parser.add_argument("--distribute-only", action="store_true", help="Only generate distribution assets")
    parser.add_argument("--optimize-only", action="store_true", help="Only run portfolio optimizer")
    parser.add_argument("--dry-run", action="store_true", help="Don't generate new apps or submit")
    parser.add_argument("--status", action="store_true", help="Show pipeline status")
    args = parser.parse_args()

    if args.status:
        log_file = LOG_DIR / "orchestrator.log"
        if log_file.exists():
            lines = log_file.read_text().strip().split('\n')
            print(f"Last 20 log entries:")
            for line in lines[-20:]:
                print(f"  {line}")

        # Show app counts
        if BUILDS.exists():
            apps = [d.name for d in BUILDS.iterdir() if d.is_dir() and (d / "app.json").exists()]
            print(f"\nApps in builds/: {len(apps)}")
            for app in sorted(apps):
                print(f"  - {app}")

        # Show opportunity count
        opp_file = LEDGER / "APP_FACTORY_OPPORTUNITIES.csv"
        if opp_file.exists():
            with open(opp_file) as f:
                count = sum(1 for _ in csv.DictReader(f))
            print(f"\nOpportunities tracked: {count}")

        return

    if args.scan_only:
        stage_scan()
    elif args.test_only:
        stage_test()
    elif args.distribute_only:
        stage_distribute()
    elif args.optimize_only:
        stage_optimize()
    else:
        run_full_pipeline(dry_run=args.dry_run)

if __name__ == "__main__":
    main()
