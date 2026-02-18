#!/usr/bin/env python3
"""
Test Runner for PRINTMAXX Automation Suite
==========================================
Comprehensive test runner with parallel execution, coverage reporting,
and HTML report generation.

Features:
- Parallel test execution
- Coverage reporting
- HTML report generation
- Selective test running by module
- CI/CD integration support
- JSON results export

Usage:
    # Run all tests
    python run_tests.py

    # Run specific module tests
    python run_tests.py --module x_poster

    # Run with coverage
    python run_tests.py --coverage

    # Generate HTML report
    python run_tests.py --html-report

    # Run in parallel
    python run_tests.py --parallel -n 4

    # Run only unit tests
    python run_tests.py --unit

    # Run integration tests
    python run_tests.py --integration

    # CI mode (all reports + exit code)
    python run_tests.py --ci
"""

import os
import sys
import json
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import shutil

# Test directory
TESTS_DIR = Path(__file__).parent
SCRIPTS_DIR = TESTS_DIR.parent / "scripts"
OUTPUT_DIR = TESTS_DIR / "test_output"
REPORTS_DIR = TESTS_DIR / "reports"

# Test modules
TEST_MODULES = [
    "test_x_poster",
    "test_ig_poster",
    "test_account_manager",
    "test_queue_processor",
    "test_session_manager",
    "test_proxy_tester",
    "test_health_checker"
]


def ensure_directories():
    """Ensure output directories exist."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def check_pytest_installed() -> bool:
    """Check if pytest is installed."""
    try:
        import pytest
        return True
    except ImportError:
        return False


def install_dependencies():
    """Install test dependencies."""
    deps = [
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "pytest-html>=4.0.0",
        "pytest-xdist>=3.0.0",
        "pytest-timeout>=2.0.0"
    ]

    print("Installing test dependencies...")
    for dep in deps:
        subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)


def run_pytest(
    modules: List[str] = None,
    parallel: bool = False,
    workers: int = 4,
    coverage: bool = False,
    html_report: bool = False,
    verbose: bool = True,
    markers: str = None,
    timeout: int = 300,
    extra_args: List[str] = None
) -> Dict[str, Any]:
    """
    Run pytest with specified configuration.

    Args:
        modules: List of test modules to run
        parallel: Enable parallel execution
        workers: Number of parallel workers
        coverage: Enable coverage reporting
        html_report: Generate HTML report
        verbose: Verbose output
        markers: Pytest markers to filter tests
        timeout: Test timeout in seconds
        extra_args: Additional pytest arguments

    Returns:
        Test results dictionary
    """
    cmd = [sys.executable, "-m", "pytest"]

    # Add test directory or specific modules
    if modules:
        cmd.extend([str(TESTS_DIR / f"{m}.py") for m in modules])
    else:
        cmd.append(str(TESTS_DIR))

    # Verbose output
    if verbose:
        cmd.append("-v")

    # Parallel execution
    if parallel:
        cmd.extend(["-n", str(workers)])

    # Coverage
    if coverage:
        cmd.extend([
            "--cov=" + str(SCRIPTS_DIR),
            "--cov-report=term-missing",
            "--cov-report=html:" + str(REPORTS_DIR / "coverage"),
            "--cov-report=json:" + str(REPORTS_DIR / "coverage.json")
        ])

    # HTML report
    if html_report:
        report_path = REPORTS_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        cmd.extend(["--html=" + str(report_path), "--self-contained-html"])

    # Markers
    if markers:
        cmd.extend(["-m", markers])

    # Timeout
    cmd.extend(["--timeout", str(timeout)])

    # JSON results
    json_report = REPORTS_DIR / "results.json"
    cmd.extend(["--json-report", "--json-report-file=" + str(json_report)])

    # Extra arguments
    if extra_args:
        cmd.extend(extra_args)

    # Run pytest
    print(f"\nRunning: {' '.join(cmd)}\n")
    print("=" * 70)

    start_time = datetime.now()

    try:
        result = subprocess.run(cmd, capture_output=False)
        return_code = result.returncode
    except Exception as e:
        print(f"Error running pytest: {e}")
        return_code = 1

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # Parse results
    results = {
        "timestamp": start_time.isoformat(),
        "duration_seconds": duration,
        "return_code": return_code,
        "success": return_code == 0
    }

    # Try to load JSON results
    if json_report.exists():
        try:
            with open(json_report) as f:
                json_results = json.load(f)
                results["summary"] = json_results.get("summary", {})
                results["tests"] = len(json_results.get("tests", []))
        except:
            pass

    print("=" * 70)
    print(f"\nTests completed in {duration:.2f} seconds")
    print(f"Result: {'PASSED' if results['success'] else 'FAILED'}")

    return results


def run_module_tests(module: str, **kwargs) -> Dict[str, Any]:
    """Run tests for a specific module."""
    if module not in TEST_MODULES and f"test_{module}" not in TEST_MODULES:
        # Try with test_ prefix
        module = f"test_{module}" if not module.startswith("test_") else module

    return run_pytest(modules=[module], **kwargs)


def run_all_tests(**kwargs) -> Dict[str, Any]:
    """Run all tests."""
    return run_pytest(modules=TEST_MODULES, **kwargs)


def run_unit_tests(**kwargs) -> Dict[str, Any]:
    """Run only unit tests (exclude integration)."""
    kwargs["markers"] = "not integration"
    return run_pytest(modules=TEST_MODULES, **kwargs)


def run_integration_tests(**kwargs) -> Dict[str, Any]:
    """Run integration tests."""
    os.environ["RUN_INTEGRATION_TESTS"] = "true"
    kwargs["markers"] = "integration"
    return run_pytest(modules=TEST_MODULES, **kwargs)


def generate_coverage_badge(coverage_percent: float) -> str:
    """Generate coverage badge markdown."""
    if coverage_percent >= 90:
        color = "brightgreen"
    elif coverage_percent >= 75:
        color = "green"
    elif coverage_percent >= 60:
        color = "yellow"
    else:
        color = "red"

    return f"![Coverage](https://img.shields.io/badge/coverage-{coverage_percent:.1f}%25-{color})"


def clean_reports():
    """Clean old reports."""
    if REPORTS_DIR.exists():
        shutil.rmtree(REPORTS_DIR)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def print_summary(results: Dict[str, Any]):
    """Print test summary."""
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    print(f"Timestamp: {results.get('timestamp', 'N/A')}")
    print(f"Duration: {results.get('duration_seconds', 0):.2f} seconds")
    print(f"Status: {'PASSED' if results.get('success') else 'FAILED'}")

    if "summary" in results:
        summary = results["summary"]
        print(f"\nTests Run: {summary.get('total', 'N/A')}")
        print(f"Passed: {summary.get('passed', 'N/A')}")
        print(f"Failed: {summary.get('failed', 'N/A')}")
        print(f"Skipped: {summary.get('skipped', 'N/A')}")
        print(f"Errors: {summary.get('error', 'N/A')}")

    print("=" * 70)


def ci_mode() -> int:
    """Run in CI mode with all reports."""
    print("\n" + "=" * 70)
    print("CI MODE - Running Full Test Suite")
    print("=" * 70 + "\n")

    # Clean old reports
    clean_reports()

    # Run tests with coverage and HTML report
    results = run_all_tests(
        coverage=True,
        html_report=True,
        parallel=True,
        workers=4
    )

    # Print summary
    print_summary(results)

    # Save results
    results_path = REPORTS_DIR / "ci_results.json"
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {results_path}")

    # List generated reports
    print("\nGenerated Reports:")
    for report in REPORTS_DIR.glob("*"):
        print(f"  - {report}")

    return 0 if results.get("success") else 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Automation Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_tests.py                      # Run all tests
    python run_tests.py --module x_poster    # Run x_poster tests
    python run_tests.py --coverage           # Run with coverage
    python run_tests.py --parallel -n 4      # Run in parallel
    python run_tests.py --ci                 # CI mode (all reports)
    python run_tests.py --unit               # Unit tests only
    python run_tests.py --integration        # Integration tests
        """
    )

    parser.add_argument(
        "--module", "-m",
        choices=TEST_MODULES + [m.replace("test_", "") for m in TEST_MODULES],
        help="Run tests for specific module"
    )
    parser.add_argument(
        "--coverage", "-c",
        action="store_true",
        help="Enable coverage reporting"
    )
    parser.add_argument(
        "--html-report", "--html",
        action="store_true",
        help="Generate HTML report"
    )
    parser.add_argument(
        "--parallel", "-p",
        action="store_true",
        help="Run tests in parallel"
    )
    parser.add_argument(
        "-n", "--workers",
        type=int,
        default=4,
        help="Number of parallel workers (default: 4)"
    )
    parser.add_argument(
        "--unit",
        action="store_true",
        help="Run only unit tests"
    )
    parser.add_argument(
        "--integration",
        action="store_true",
        help="Run integration tests"
    )
    parser.add_argument(
        "--ci",
        action="store_true",
        help="CI mode (full suite + all reports)"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean old reports before running"
    )
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Install test dependencies"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Test timeout in seconds (default: 300)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        default=True,
        help="Verbose output"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Quiet output"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output results to JSON file"
    )
    parser.add_argument(
        "extra_args",
        nargs="*",
        help="Additional pytest arguments"
    )

    args = parser.parse_args()

    # Ensure directories exist
    ensure_directories()

    # Install dependencies if requested
    if args.install_deps:
        install_dependencies()
        return 0

    # Check pytest is installed
    if not check_pytest_installed():
        print("pytest not installed. Run with --install-deps to install dependencies.")
        return 1

    # Clean old reports if requested
    if args.clean:
        clean_reports()

    # CI mode
    if args.ci:
        return ci_mode()

    # Determine verbosity
    verbose = not args.quiet

    # Build kwargs
    kwargs = {
        "parallel": args.parallel,
        "workers": args.workers,
        "coverage": args.coverage,
        "html_report": args.html_report,
        "verbose": verbose,
        "timeout": args.timeout,
        "extra_args": args.extra_args
    }

    # Run appropriate tests
    if args.module:
        results = run_module_tests(args.module, **kwargs)
    elif args.unit:
        results = run_unit_tests(**kwargs)
    elif args.integration:
        results = run_integration_tests(**kwargs)
    else:
        results = run_all_tests(**kwargs)

    # Print summary
    print_summary(results)

    # Save results if output specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")

    return 0 if results.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
