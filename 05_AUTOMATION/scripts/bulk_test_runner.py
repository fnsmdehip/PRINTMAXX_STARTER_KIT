#!/usr/bin/env python3
"""
Bulk Test Runner - Parallel Test Orchestrator
==============================================
Run all tests in parallel with configurable concurrency.

Features:
- Parallel test execution
- Test suite discovery
- Progress tracking
- Failure aggregation
- Retry logic
- Resource management
- Configurable workers

Usage:
    from bulk_test_runner import BulkTestRunner

    runner = BulkTestRunner(max_workers=4)
    results = runner.run_all()

CLI:
    python bulk_test_runner.py --all                    # Run all tests
    python bulk_test_runner.py --suite social           # Run social tests
    python bulk_test_runner.py --suite app              # Run app tests
    python bulk_test_runner.py --workers 8              # Custom parallelism
    python bulk_test_runner.py --retry 3               # Retry failed tests
"""

import os
import sys
import json
import time
import subprocess
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field, asdict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from enum import Enum
import threading

# Configure logging
LOG_DIR = Path(__file__).parent.parent / "OPS" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "bulk_test_runner.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("bulk_test_runner")


class TestStatus(Enum):
    """Test execution status."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


@dataclass
class TestDefinition:
    """Definition of a test to run."""
    name: str
    path: str
    suite: str
    command: List[str] = field(default_factory=list)
    timeout: int = 300  # 5 minutes default
    env: Dict[str, str] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    retry_on_failure: bool = True
    max_retries: int = 2


@dataclass
class TestResult:
    """Result of a test execution."""
    test_name: str
    status: TestStatus
    duration_seconds: float
    exit_code: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    error_message: Optional[str] = None
    attempt: int = 1
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class BulkTestResult:
    """Aggregated results of bulk test run."""
    total_tests: int
    passed: int
    failed: int
    errors: int
    skipped: int
    timeout: int
    duration_seconds: float
    results: List[TestResult] = field(default_factory=list)
    start_time: str = field(default_factory=lambda: datetime.now().isoformat())
    end_time: Optional[str] = None


class TestDiscovery:
    """Discover tests in the project."""

    def __init__(self, test_dir: Path = None):
        self.test_dir = test_dir or Path(__file__).parent / "tests"

    def discover_all(self) -> List[TestDefinition]:
        """Discover all test files."""
        tests = []

        # Social automation tests
        tests.extend(self._discover_social_tests())

        # App tests
        tests.extend(self._discover_app_tests())

        # Proxy tests
        tests.extend(self._discover_proxy_tests())

        return tests

    def discover_by_suite(self, suite: str) -> List[TestDefinition]:
        """Discover tests for a specific suite."""
        suite_map = {
            "social": self._discover_social_tests,
            "app": self._discover_app_tests,
            "proxy": self._discover_proxy_tests,
            "all": self.discover_all,
        }

        if suite not in suite_map:
            logger.warning(f"Unknown suite: {suite}")
            return []

        return suite_map[suite]()

    def _discover_social_tests(self) -> List[TestDefinition]:
        """Discover social media automation tests."""
        tests = []

        # X/Twitter poster tests
        x_test = self.test_dir / "test_x_poster.py"
        if x_test.exists():
            tests.append(TestDefinition(
                name="x_poster_unit",
                path=str(x_test),
                suite="social",
                command=["python", str(x_test), "--unit"],
                timeout=120,
            ))

        # Instagram poster tests
        ig_test = self.test_dir / "test_ig_poster.py"
        if ig_test.exists():
            tests.append(TestDefinition(
                name="ig_poster_unit",
                path=str(ig_test),
                suite="social",
                command=["python", str(ig_test), "--unit"],
                timeout=120,
            ))

        return tests

    def _discover_app_tests(self) -> List[TestDefinition]:
        """Discover app testing framework tests."""
        tests = []

        # App test runner tests
        app_runner = self.test_dir / "app_test_runner.py"
        if app_runner.exists():
            tests.append(TestDefinition(
                name="app_test_runner_import",
                path=str(app_runner),
                suite="app",
                command=["python", "-c", f"import sys; sys.path.insert(0, '{self.test_dir}'); from app_test_runner import AppTestRunner; print('Import OK')"],
                timeout=30,
            ))

        # Screenshot generator tests
        screenshot_gen = self.test_dir / "screenshot_generator.py"
        if screenshot_gen.exists():
            tests.append(TestDefinition(
                name="screenshot_generator_import",
                path=str(screenshot_gen),
                suite="app",
                command=["python", "-c", f"import sys; sys.path.insert(0, '{self.test_dir}'); from screenshot_generator import ScreenshotGenerator; print('Import OK')"],
                timeout=30,
            ))

        # Crash detector tests
        crash_detector = self.test_dir / "crash_detector.py"
        if crash_detector.exists():
            tests.append(TestDefinition(
                name="crash_detector_import",
                path=str(crash_detector),
                suite="app",
                command=["python", "-c", f"import sys; sys.path.insert(0, '{self.test_dir}'); from crash_detector import CrashDetector; print('Import OK')"],
                timeout=30,
            ))

        return tests

    def _discover_proxy_tests(self) -> List[TestDefinition]:
        """Discover proxy testing tests."""
        tests = []

        proxy_test = self.test_dir / "test_proxy_rotation.py"
        if proxy_test.exists():
            tests.append(TestDefinition(
                name="proxy_rotation_unit",
                path=str(proxy_test),
                suite="proxy",
                command=["python", str(proxy_test), "--unit"],
                timeout=180,
            ))

        return tests


class BulkTestRunner:
    """Run tests in parallel with orchestration."""

    def __init__(
        self,
        max_workers: int = 4,
        retry_failed: bool = True,
        max_retries: int = 2,
        timeout: int = 300
    ):
        """
        Initialize bulk test runner.

        Args:
            max_workers: Maximum parallel test executions
            retry_failed: Whether to retry failed tests
            max_retries: Maximum retry attempts
            timeout: Default test timeout in seconds
        """
        self.max_workers = max_workers
        self.retry_failed = retry_failed
        self.max_retries = max_retries
        self.default_timeout = timeout

        self.discovery = TestDiscovery()
        self.results: List[TestResult] = []
        self._lock = threading.Lock()
        self._progress_callback: Optional[Callable[[str, TestStatus], None]] = None

        logger.info(f"Bulk test runner initialized with {max_workers} workers")

    def set_progress_callback(self, callback: Callable[[str, TestStatus], None]):
        """Set callback for progress updates."""
        self._progress_callback = callback

    def _notify_progress(self, test_name: str, status: TestStatus):
        """Notify progress callback if set."""
        if self._progress_callback:
            try:
                self._progress_callback(test_name, status)
            except Exception as e:
                logger.error(f"Progress callback error: {e}")

    def _run_single_test(self, test: TestDefinition, attempt: int = 1) -> TestResult:
        """Run a single test."""
        logger.info(f"Running test: {test.name} (attempt {attempt})")
        self._notify_progress(test.name, TestStatus.RUNNING)

        result = TestResult(
            test_name=test.name,
            status=TestStatus.ERROR,
            duration_seconds=0,
            attempt=attempt
        )

        start_time = time.time()

        try:
            # Build environment
            env = os.environ.copy()
            env.update(test.env)

            # Run the test
            timeout = test.timeout or self.default_timeout

            process = subprocess.run(
                test.command,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
                cwd=str(Path(test.path).parent) if test.path else None
            )

            result.exit_code = process.returncode
            result.stdout = process.stdout[-10000:] if len(process.stdout) > 10000 else process.stdout
            result.stderr = process.stderr[-5000:] if len(process.stderr) > 5000 else process.stderr

            if process.returncode == 0:
                result.status = TestStatus.PASSED
            else:
                result.status = TestStatus.FAILED
                result.error_message = f"Exit code: {process.returncode}"

        except subprocess.TimeoutExpired:
            result.status = TestStatus.TIMEOUT
            result.error_message = f"Test timed out after {test.timeout}s"
            logger.warning(f"Test {test.name} timed out")

        except Exception as e:
            result.status = TestStatus.ERROR
            result.error_message = str(e)
            logger.error(f"Test {test.name} error: {e}")

        result.duration_seconds = time.time() - start_time

        self._notify_progress(test.name, result.status)
        logger.info(f"Test {test.name}: {result.status.value} ({result.duration_seconds:.2f}s)")

        return result

    def _run_with_retry(self, test: TestDefinition) -> TestResult:
        """Run a test with retry logic."""
        max_attempts = test.max_retries + 1 if test.retry_on_failure and self.retry_failed else 1

        for attempt in range(1, max_attempts + 1):
            result = self._run_single_test(test, attempt)

            if result.status == TestStatus.PASSED:
                return result

            if attempt < max_attempts:
                logger.info(f"Retrying test {test.name} (attempt {attempt + 1}/{max_attempts})")
                time.sleep(2)  # Brief pause before retry

        return result

    def run_tests(self, tests: List[TestDefinition]) -> BulkTestResult:
        """
        Run a list of tests in parallel.

        Args:
            tests: List of test definitions

        Returns:
            Aggregated test results
        """
        start_time = time.time()

        bulk_result = BulkTestResult(
            total_tests=len(tests),
            passed=0,
            failed=0,
            errors=0,
            skipped=0,
            timeout=0,
            duration_seconds=0
        )

        if not tests:
            logger.warning("No tests to run")
            return bulk_result

        logger.info(f"Running {len(tests)} tests with {self.max_workers} workers")

        # Group tests by dependencies
        independent_tests = [t for t in tests if not t.dependencies]
        dependent_tests = [t for t in tests if t.dependencies]

        # Run independent tests in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self._run_with_retry, test): test for test in independent_tests}

            for future in as_completed(futures):
                test = futures[future]
                try:
                    result = future.result()
                    with self._lock:
                        bulk_result.results.append(result)
                        self._update_counters(bulk_result, result)
                except Exception as e:
                    logger.error(f"Test {test.name} raised exception: {e}")
                    with self._lock:
                        error_result = TestResult(
                            test_name=test.name,
                            status=TestStatus.ERROR,
                            duration_seconds=0,
                            error_message=str(e)
                        )
                        bulk_result.results.append(error_result)
                        bulk_result.errors += 1

        # Run dependent tests sequentially (respecting dependencies)
        completed = {r.test_name for r in bulk_result.results if r.status == TestStatus.PASSED}

        for test in dependent_tests:
            # Check if dependencies passed
            deps_met = all(dep in completed for dep in test.dependencies)

            if not deps_met:
                logger.warning(f"Skipping {test.name} - dependencies not met")
                result = TestResult(
                    test_name=test.name,
                    status=TestStatus.SKIPPED,
                    duration_seconds=0,
                    error_message="Dependencies not met"
                )
            else:
                result = self._run_with_retry(test)
                if result.status == TestStatus.PASSED:
                    completed.add(test.name)

            bulk_result.results.append(result)
            self._update_counters(bulk_result, result)

        bulk_result.duration_seconds = time.time() - start_time
        bulk_result.end_time = datetime.now().isoformat()

        return bulk_result

    def _update_counters(self, bulk_result: BulkTestResult, result: TestResult):
        """Update result counters."""
        if result.status == TestStatus.PASSED:
            bulk_result.passed += 1
        elif result.status == TestStatus.FAILED:
            bulk_result.failed += 1
        elif result.status == TestStatus.ERROR:
            bulk_result.errors += 1
        elif result.status == TestStatus.SKIPPED:
            bulk_result.skipped += 1
        elif result.status == TestStatus.TIMEOUT:
            bulk_result.timeout += 1

    def run_all(self) -> BulkTestResult:
        """Run all discovered tests."""
        tests = self.discovery.discover_all()
        return self.run_tests(tests)

    def run_suite(self, suite: str) -> BulkTestResult:
        """Run tests for a specific suite."""
        tests = self.discovery.discover_by_suite(suite)
        return self.run_tests(tests)

    def run_custom(self, test_definitions: List[Dict[str, Any]]) -> BulkTestResult:
        """Run custom test definitions."""
        tests = [TestDefinition(**td) for td in test_definitions]
        return self.run_tests(tests)


class TestScheduler:
    """Schedule and manage test runs."""

    def __init__(self, runner: BulkTestRunner):
        self.runner = runner
        self.scheduled_runs: List[Dict[str, Any]] = []
        self._running = False

    def schedule_run(
        self,
        suite: str,
        time_str: str = None,
        interval_minutes: int = None
    ) -> str:
        """
        Schedule a test run.

        Args:
            suite: Test suite to run
            time_str: Time to run (HH:MM format)
            interval_minutes: Run every N minutes

        Returns:
            Schedule ID
        """
        schedule_id = f"sched_{int(time.time()*1000)}"
        self.scheduled_runs.append({
            "id": schedule_id,
            "suite": suite,
            "time": time_str,
            "interval": interval_minutes,
            "last_run": None,
            "next_run": None
        })
        return schedule_id

    def cancel_schedule(self, schedule_id: str) -> bool:
        """Cancel a scheduled run."""
        for i, run in enumerate(self.scheduled_runs):
            if run["id"] == schedule_id:
                self.scheduled_runs.pop(i)
                return True
        return False


def print_results(bulk_result: BulkTestResult):
    """Print formatted test results."""
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)

    print(f"\nTotal:    {bulk_result.total_tests}")
    print(f"Passed:   {bulk_result.passed} ({bulk_result.passed/bulk_result.total_tests*100:.1f}%)")
    print(f"Failed:   {bulk_result.failed}")
    print(f"Errors:   {bulk_result.errors}")
    print(f"Skipped:  {bulk_result.skipped}")
    print(f"Timeout:  {bulk_result.timeout}")
    print(f"Duration: {bulk_result.duration_seconds:.2f}s")

    # Print failures
    failures = [r for r in bulk_result.results if r.status in (TestStatus.FAILED, TestStatus.ERROR)]
    if failures:
        print("\n" + "-" * 40)
        print("FAILURES:")
        for result in failures:
            print(f"\n  {result.test_name}:")
            print(f"    Status: {result.status.value}")
            print(f"    Error: {result.error_message}")
            if result.stderr:
                print(f"    Stderr: {result.stderr[:200]}...")

    print("\n" + "=" * 60)


def save_results(bulk_result: BulkTestResult, output_path: str):
    """Save results to JSON file."""
    data = {
        "total_tests": bulk_result.total_tests,
        "passed": bulk_result.passed,
        "failed": bulk_result.failed,
        "errors": bulk_result.errors,
        "skipped": bulk_result.skipped,
        "timeout": bulk_result.timeout,
        "duration_seconds": bulk_result.duration_seconds,
        "start_time": bulk_result.start_time,
        "end_time": bulk_result.end_time,
        "results": [
            {
                "test_name": r.test_name,
                "status": r.status.value,
                "duration_seconds": r.duration_seconds,
                "exit_code": r.exit_code,
                "error_message": r.error_message,
                "attempt": r.attempt,
                "timestamp": r.timestamp
            }
            for r in bulk_result.results
        ]
    }

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    logger.info(f"Results saved to: {output_path}")


# CLI
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Bulk Test Runner")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--suite", "-s", help="Run specific suite (social, app, proxy)")
    parser.add_argument("--workers", "-w", type=int, default=4, help="Number of parallel workers")
    parser.add_argument("--retry", "-r", type=int, default=2, help="Max retries for failed tests")
    parser.add_argument("--timeout", "-t", type=int, default=300, help="Default test timeout")
    parser.add_argument("--output", "-o", help="Output JSON file for results")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    runner = BulkTestRunner(
        max_workers=args.workers,
        retry_failed=True,
        max_retries=args.retry,
        timeout=args.timeout
    )

    # Progress callback
    def progress(test_name: str, status: TestStatus):
        symbol = {
            TestStatus.RUNNING: "...",
            TestStatus.PASSED: "[OK]",
            TestStatus.FAILED: "[FAIL]",
            TestStatus.ERROR: "[ERR]",
            TestStatus.SKIPPED: "[SKIP]",
            TestStatus.TIMEOUT: "[TIME]"
        }.get(status, "[?]")
        print(f"  {symbol} {test_name}")

    runner.set_progress_callback(progress)

    # Run tests
    print("\nStarting test run...")

    if args.suite:
        bulk_result = runner.run_suite(args.suite)
    else:
        bulk_result = runner.run_all()

    # Print results
    print_results(bulk_result)

    # Save results
    if args.output:
        save_results(bulk_result, args.output)
    else:
        # Default output
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = str(LOG_DIR / f"bulk_test_results_{timestamp}.json")
        save_results(bulk_result, output_path)

    # Exit code
    if bulk_result.failed > 0 or bulk_result.errors > 0:
        sys.exit(1)
    sys.exit(0)
