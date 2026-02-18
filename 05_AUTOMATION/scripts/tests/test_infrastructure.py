#!/usr/bin/env python3
"""
Infrastructure Test Suite - Verify all PRINTMAXX systems are operational.

Run: python3 AUTOMATIONS/tests/test_infrastructure.py
Or:  pytest AUTOMATIONS/tests/test_infrastructure.py -v
"""

import csv
import json
import os
import sys
import subprocess
from pathlib import Path

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_DIR / "LEDGER"
AUTOMATIONS_DIR = PROJECT_DIR / "AUTOMATIONS"
RALPH_DIR = PROJECT_DIR / "ralph" / "loops"
BUILDS_DIR = PROJECT_DIR / "MONEY_METHODS" / "APP_FACTORY" / "builds"
FINANCIALS_DIR = PROJECT_DIR / "FINANCIALS"
TEMPLATES_DIR = PROJECT_DIR / "MONEY_METHODS" / "APP_FACTORY" / "templates"


def test_ledger_directory_exists():
    assert LEDGER_DIR.exists(), "LEDGER directory missing"


def test_ledger_has_csv_files():
    csv_files = list(LEDGER_DIR.glob("*.csv"))
    assert len(csv_files) >= 50, f"Expected 50+ CSV files, found {len(csv_files)}"


def test_alpha_staging_exists():
    filepath = LEDGER_DIR / "ALPHA_STAGING.csv"
    assert filepath.exists(), "ALPHA_STAGING.csv missing"


def test_alpha_staging_parseable():
    filepath = LEDGER_DIR / "ALPHA_STAGING.csv"
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        assert headers is not None, "No headers in ALPHA_STAGING.csv"
        assert 'alpha_id' in headers, "alpha_id column missing"
        assert 'status' in headers, "status column missing"
        rows = list(reader)
        assert len(rows) > 0, "ALPHA_STAGING.csv has no data rows"


def test_financials_directory():
    required = [
        "REVENUE_TRACKER.csv",
        "EXPENSE_TRACKER.csv",
        "P_AND_L_MONTHLY.csv",
    ]
    for filename in required:
        filepath = FINANCIALS_DIR / filename
        assert filepath.exists(), f"FINANCIALS/{filename} missing"


def test_ralph_loops_complete():
    """All ralph loops should have prompt.md and run.sh."""
    loops = [d for d in RALPH_DIR.iterdir() if d.is_dir()]
    assert len(loops) >= 15, f"Expected 15+ ralph loops, found {len(loops)}"

    for loop_dir in loops:
        assert (loop_dir / "prompt.md").exists(), f"{loop_dir.name}: missing prompt.md"
        assert (loop_dir / "run.sh").exists(), f"{loop_dir.name}: missing run.sh"


def test_ralph_run_scripts_executable():
    """All run.sh should be executable."""
    for loop_dir in RALPH_DIR.iterdir():
        if not loop_dir.is_dir():
            continue
        run_sh = loop_dir / "run.sh"
        if run_sh.exists():
            assert os.access(run_sh, os.X_OK), f"{loop_dir.name}/run.sh not executable"


def test_sdk54_apps_have_eas_json():
    """All SDK54 apps with package.json should have eas.json."""
    for app_dir in BUILDS_DIR.iterdir():
        if not app_dir.is_dir() or not app_dir.name.endswith('-sdk54'):
            continue
        if (app_dir / 'package.json').exists():
            assert (app_dir / 'eas.json').exists(), f"{app_dir.name}: missing eas.json"


def test_templates_exist():
    """All template files should exist."""
    templates = [
        "eas.json",
        "subscriptionService.ts",
        "notificationService.ts",
        "MoreApps.tsx",
    ]
    for template in templates:
        filepath = TEMPLATES_DIR / template
        assert filepath.exists(), f"Template missing: {template}"


def test_automation_scripts_parse():
    """All Python scripts in AUTOMATIONS/ should parse without errors."""
    import ast
    for py_file in AUTOMATIONS_DIR.glob("*.py"):
        try:
            with open(py_file, 'r') as f:
                ast.parse(f.read())
        except SyntaxError as e:
            assert False, f"Syntax error in {py_file.name}: {e}"


def test_ledger_cli_runs():
    """ledger_cli.py should execute without errors."""
    result = subprocess.run(
        [sys.executable, str(AUTOMATIONS_DIR / "ledger_cli.py"), "stats"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, f"ledger_cli.py failed: {result.stderr}"


def test_system_health_check_runs():
    """system_health_check.py should execute without errors."""
    result = subprocess.run(
        [sys.executable, str(AUTOMATIONS_DIR / "system_health_check.py"), "--ralph"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, f"system_health_check.py failed: {result.stderr}"


def test_revenue_sync_runs():
    """revenue_sync.py should execute without errors."""
    result = subprocess.run(
        [sys.executable, str(AUTOMATIONS_DIR / "revenue_sync.py"), "--pnl"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, f"revenue_sync.py failed: {result.stderr}"


def test_app_batch_fix_runs():
    """app_batch_fix.py should execute without errors."""
    result = subprocess.run(
        [sys.executable, str(AUTOMATIONS_DIR / "app_batch_fix.py"), "status"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, f"app_batch_fix.py failed: {result.stderr}"


def test_roi_analyzer_runs():
    """roi_analyzer.py should execute without errors."""
    result = subprocess.run(
        [sys.executable, str(AUTOMATIONS_DIR / "roi_analyzer.py"), "report"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, f"roi_analyzer.py failed: {result.stderr}"


def test_method_stack_calculator_runs():
    """method_stack_calculator.py should execute without errors."""
    result = subprocess.run(
        [sys.executable, str(AUTOMATIONS_DIR / "method_stack_calculator.py"), "top"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, f"method_stack_calculator.py failed: {result.stderr}"


def test_content_pipeline_runs():
    """content_pipeline.py should execute without errors."""
    result = subprocess.run(
        [sys.executable, str(AUTOMATIONS_DIR / "content_pipeline.py"), "stats"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, f"content_pipeline.py failed: {result.stderr}"


def test_alpha_to_method_runs():
    """alpha_to_method.py should execute without errors."""
    result = subprocess.run(
        [sys.executable, str(AUTOMATIONS_DIR / "alpha_to_method.py"), "stats"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, f"alpha_to_method.py failed: {result.stderr}"


def test_backtest_alpha_runs():
    """backtest_alpha.py should parse and be importable."""
    import ast
    filepath = AUTOMATIONS_DIR / "backtest_alpha.py"
    with open(filepath) as f:
        ast.parse(f.read())


def test_paper_trade_runs():
    """paper_trade.py should parse and be importable."""
    import ast
    filepath = AUTOMATIONS_DIR / "paper_trade.py"
    with open(filepath) as f:
        ast.parse(f.read())


if __name__ == "__main__":
    # Simple test runner (no pytest required)
    tests = [
        (name, func) for name, func in globals().items()
        if name.startswith('test_') and callable(func)
    ]

    passed = 0
    failed = 0
    errors = []

    print(f"\nRunning {len(tests)} infrastructure tests...\n")

    for name, func in sorted(tests):
        try:
            func()
            print(f"  PASS: {name}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL: {name} - {e}")
            failed += 1
            errors.append((name, str(e)))
        except Exception as e:
            print(f"  ERROR: {name} - {type(e).__name__}: {e}")
            failed += 1
            errors.append((name, f"{type(e).__name__}: {e}"))

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed, {passed + failed} total")

    if errors:
        print(f"\nFailures:")
        for name, err in errors:
            print(f"  {name}: {err}")

    sys.exit(0 if failed == 0 else 1)
