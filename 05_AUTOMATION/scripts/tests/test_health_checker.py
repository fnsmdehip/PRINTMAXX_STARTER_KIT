#!/usr/bin/env python3
"""
Health Checker Test Suite
=========================
Comprehensive tests for the HealthChecker class.

Features:
- Login status check tests
- Restriction detection tests
- Shadowban detection tests
- Health report generation tests
- Platform-specific health check tests

Usage:
    python -m pytest test_health_checker.py -v
    python test_health_checker.py --unit
"""

import os
import sys
import json
import csv
import tempfile
import shutil
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

try:
    from health_checker import HealthChecker, HealthStatus
except ImportError:
    HealthChecker = None
    HealthStatus = None

# Test output directory
TEST_OUTPUT_DIR = Path(__file__).parent / "test_output" / "health"
TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class TestHealthStatus(unittest.TestCase):
    """Tests for HealthStatus constants."""

    def test_health_status_values(self):
        """Test HealthStatus has expected values."""
        if not HealthStatus:
            self.skipTest("HealthStatus not importable")

        self.assertEqual(HealthStatus.HEALTHY, "healthy")
        self.assertEqual(HealthStatus.WARNING, "warning")
        self.assertEqual(HealthStatus.CRITICAL, "critical")
        self.assertEqual(HealthStatus.BANNED, "banned")
        self.assertEqual(HealthStatus.UNKNOWN, "unknown")


class TestHealthCheckerInit(unittest.TestCase):
    """Tests for HealthChecker initialization."""

    def test_init_with_defaults(self):
        """Test checker initialization with defaults."""
        if not HealthChecker:
            self.skipTest("HealthChecker not importable")

        checker = HealthChecker()
        self.assertIsNotNone(checker.accounts_path)

    def test_init_with_custom_paths(self):
        """Test checker with custom paths."""
        if not HealthChecker:
            self.skipTest("HealthChecker not importable")

        sessions_dir = str(TEST_OUTPUT_DIR / "sessions")
        checker = HealthChecker(sessions_dir=sessions_dir)

        self.assertEqual(checker.sessions_dir, sessions_dir)


class TestHealthCheckerDetermineStatus(unittest.TestCase):
    """Tests for status determination."""

    def setUp(self):
        """Set up checker."""
        if not HealthChecker:
            self.skipTest("HealthChecker not importable")
        self.checker = HealthChecker()

    def test_status_healthy(self):
        """Test determining healthy status."""
        result = {
            "login_ok": True,
            "restricted": False,
            "shadowban": False,
            "warnings": []
        }
        status = self.checker._determine_status(result)
        self.assertEqual(status, HealthStatus.HEALTHY)

    def test_status_banned(self):
        """Test determining banned status."""
        result = {
            "login_ok": True,
            "restricted": True,
            "shadowban": False,
            "warnings": []
        }
        status = self.checker._determine_status(result)
        self.assertEqual(status, HealthStatus.BANNED)

    def test_status_shadowban(self):
        """Test determining warning status from shadowban."""
        result = {
            "login_ok": True,
            "restricted": False,
            "shadowban": True,
            "warnings": []
        }
        status = self.checker._determine_status(result)
        self.assertEqual(status, HealthStatus.WARNING)

    def test_status_critical_no_login(self):
        """Test determining critical status from login failure."""
        result = {
            "login_ok": False,
            "restricted": False,
            "shadowban": False,
            "warnings": []
        }
        status = self.checker._determine_status(result)
        self.assertEqual(status, HealthStatus.CRITICAL)

    def test_status_warning_with_warnings(self):
        """Test determining warning status from warnings."""
        result = {
            "login_ok": True,
            "restricted": False,
            "shadowban": False,
            "warnings": ["Some warning detected"]
        }
        status = self.checker._determine_status(result)
        self.assertEqual(status, HealthStatus.WARNING)


class TestHealthCheckerPlatformDetection(unittest.TestCase):
    """Tests for platform detection from account ID."""

    def setUp(self):
        """Set up checker."""
        if not HealthChecker:
            self.skipTest("HealthChecker not importable")
        self.checker = HealthChecker()
        self.checker.account_manager = None  # Disable account manager

    def test_detect_x_platform(self):
        """Test detecting X platform from account ID."""
        result = self.checker.check_account("x_faith_main", use_session=False)
        self.assertEqual(result["platform"], "X")

    def test_detect_instagram_platform(self):
        """Test detecting Instagram platform from account ID."""
        result = self.checker.check_account("ig_fitness_main", use_session=False)
        self.assertEqual(result["platform"], "Instagram")

    def test_detect_tiktok_platform(self):
        """Test detecting TikTok platform from account ID."""
        result = self.checker.check_account("tiktok_ai_main", use_session=False)
        self.assertEqual(result["platform"], "TikTok")


class TestHealthCheckerXAccount(unittest.TestCase):
    """Tests for X/Twitter account health checking."""

    def setUp(self):
        """Set up checker."""
        if not HealthChecker:
            self.skipTest("HealthChecker not importable")
        self.checker = HealthChecker()

    @patch('health_checker.sync_playwright')
    def test_x_logged_in(self, mock_playwright):
        """Test X account logged in detection."""
        mock_pw = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.__enter__.return_value = mock_pw
        mock_pw.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Mock logged in state
        mock_locator = MagicMock()
        mock_locator.count.return_value = 1
        mock_page.locator.return_value = mock_locator
        mock_page.content.return_value = "<html>Normal content</html>"

        result = {
            "account_id": "x_test",
            "timestamp": datetime.now().isoformat(),
            "platform": "X",
            "status": HealthStatus.UNKNOWN,
            "login_ok": False,
            "restricted": False,
            "shadowban": False,
            "warnings": [],
            "metrics": {},
            "notes": "",
            "error": None
        }

        result = self.checker._check_x_account(None, result, use_session=False)

        self.assertTrue(result["login_ok"])

    @patch('health_checker.sync_playwright')
    def test_x_not_logged_in(self, mock_playwright):
        """Test X account not logged in detection."""
        mock_pw = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.__enter__.return_value = mock_pw
        mock_pw.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Mock not logged in state
        mock_locator = MagicMock()
        mock_locator.count.return_value = 0
        mock_page.locator.return_value = mock_locator
        mock_page.content.return_value = "<html>Login form</html>"

        result = {
            "account_id": "x_test",
            "timestamp": datetime.now().isoformat(),
            "platform": "X",
            "status": HealthStatus.UNKNOWN,
            "login_ok": False,
            "restricted": False,
            "shadowban": False,
            "warnings": [],
            "metrics": {},
            "notes": "",
            "error": None
        }

        result = self.checker._check_x_account(None, result, use_session=False)

        self.assertFalse(result["login_ok"])
        self.assertIn("Not logged in", result["warnings"])

    @patch('health_checker.sync_playwright')
    def test_x_restriction_detected(self, mock_playwright):
        """Test X account restriction detection."""
        mock_pw = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.__enter__.return_value = mock_pw
        mock_pw.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        mock_locator = MagicMock()
        mock_locator.count.return_value = 1
        mock_page.locator.return_value = mock_locator
        mock_page.content.return_value = "<html>Your account is suspended please appeal</html>"

        result = {
            "account_id": "x_test",
            "timestamp": datetime.now().isoformat(),
            "platform": "X",
            "status": HealthStatus.UNKNOWN,
            "login_ok": False,
            "restricted": False,
            "shadowban": False,
            "warnings": [],
            "metrics": {},
            "notes": "",
            "error": None
        }

        result = self.checker._check_x_account(None, result, use_session=False)

        self.assertTrue(result["restricted"])


class TestHealthCheckerInstagramAccount(unittest.TestCase):
    """Tests for Instagram account health checking."""

    def setUp(self):
        """Set up checker."""
        if not HealthChecker:
            self.skipTest("HealthChecker not importable")
        self.checker = HealthChecker()

    @patch('health_checker.sync_playwright')
    def test_instagram_logged_in(self, mock_playwright):
        """Test Instagram logged in detection."""
        mock_pw = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.__enter__.return_value = mock_pw
        mock_pw.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        mock_locator = MagicMock()
        mock_locator.count.return_value = 1
        mock_page.locator.return_value = mock_locator
        mock_page.content.return_value = '<html><svg aria-label="Home"></svg></html>'

        result = {
            "account_id": "ig_test",
            "timestamp": datetime.now().isoformat(),
            "platform": "Instagram",
            "status": HealthStatus.UNKNOWN,
            "login_ok": False,
            "restricted": False,
            "shadowban": False,
            "warnings": [],
            "metrics": {},
            "notes": "",
            "error": None
        }

        result = self.checker._check_instagram_account(None, result, use_session=False)

        self.assertTrue(result["login_ok"])

    @patch('health_checker.sync_playwright')
    def test_instagram_action_blocked(self, mock_playwright):
        """Test Instagram action blocked detection."""
        mock_pw = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.__enter__.return_value = mock_pw
        mock_pw.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        mock_locator = MagicMock()
        mock_locator.count.return_value = 1
        mock_page.locator.return_value = mock_locator
        mock_page.content.return_value = "<html>Action blocked try again later</html>"

        result = {
            "account_id": "ig_test",
            "timestamp": datetime.now().isoformat(),
            "platform": "Instagram",
            "status": HealthStatus.UNKNOWN,
            "login_ok": False,
            "restricted": False,
            "shadowban": False,
            "warnings": [],
            "metrics": {},
            "notes": "",
            "error": None
        }

        result = self.checker._check_instagram_account(None, result, use_session=False)

        self.assertTrue(result["restricted"])


class TestHealthCheckerTikTokAccount(unittest.TestCase):
    """Tests for TikTok account health checking."""

    def setUp(self):
        """Set up checker."""
        if not HealthChecker:
            self.skipTest("HealthChecker not importable")
        self.checker = HealthChecker()

    @patch('health_checker.sync_playwright')
    def test_tiktok_banned_detection(self, mock_playwright):
        """Test TikTok ban detection."""
        mock_pw = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.__enter__.return_value = mock_pw
        mock_pw.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        mock_locator = MagicMock()
        mock_locator.count.return_value = 0
        mock_page.locator.return_value = mock_locator
        mock_page.content.return_value = "<html>Your account has been permanently banned</html>"

        result = {
            "account_id": "tiktok_test",
            "timestamp": datetime.now().isoformat(),
            "platform": "TikTok",
            "status": HealthStatus.UNKNOWN,
            "login_ok": False,
            "restricted": False,
            "shadowban": False,
            "warnings": [],
            "metrics": {},
            "notes": "",
            "error": None
        }

        result = self.checker._check_tiktok_account(None, result, use_session=False)

        self.assertTrue(result["restricted"])


class TestHealthCheckerCheckAll(unittest.TestCase):
    """Tests for checking all accounts."""

    def setUp(self):
        """Set up checker."""
        if not HealthChecker:
            self.skipTest("HealthChecker not importable")
        self.checker = HealthChecker()

    def test_check_all_no_manager(self):
        """Test check_all_accounts with no account manager."""
        self.checker.account_manager = None
        results = self.checker.check_all_accounts()
        self.assertEqual(len(results), 0)

    @patch.object(HealthChecker, 'check_account')
    def test_check_all_with_filter(self, mock_check):
        """Test check_all_accounts with platform filter."""
        mock_check.return_value = {"status": HealthStatus.HEALTHY}

        # Mock account manager
        mock_account1 = MagicMock()
        mock_account1.id = "x_test"
        mock_account1.platform = "X"
        mock_account1.niche = "AI"

        mock_account2 = MagicMock()
        mock_account2.id = "ig_test"
        mock_account2.platform = "Instagram"
        mock_account2.niche = "AI"

        self.checker.account_manager = MagicMock()
        self.checker.account_manager.get_active_accounts.return_value = [mock_account1, mock_account2]

        # Test platform filter
        with patch('time.sleep'):
            results = self.checker.check_all_accounts(platform="X")

        self.assertEqual(len(results), 1)


class TestHealthCheckerReport(unittest.TestCase):
    """Tests for health report generation."""

    def setUp(self):
        """Set up checker."""
        if not HealthChecker:
            self.skipTest("HealthChecker not importable")
        self.checker = HealthChecker()

    def test_generate_report_from_results(self):
        """Test generating report from results."""
        results = [
            {
                "account_id": "x_test1",
                "platform": "X",
                "status": HealthStatus.HEALTHY,
                "warnings": []
            },
            {
                "account_id": "x_test2",
                "platform": "X",
                "status": HealthStatus.WARNING,
                "warnings": ["Some warning"]
            },
            {
                "account_id": "ig_test",
                "platform": "Instagram",
                "status": HealthStatus.BANNED,
                "warnings": ["Account banned"]
            }
        ]

        report = self.checker.generate_report(results)

        self.assertEqual(report["total_accounts"], 3)
        self.assertEqual(report["summary"][HealthStatus.HEALTHY], 1)
        self.assertEqual(report["summary"][HealthStatus.WARNING], 1)
        self.assertEqual(report["summary"][HealthStatus.BANNED], 1)
        self.assertEqual(report["by_platform"]["X"]["total"], 2)
        self.assertEqual(report["by_platform"]["Instagram"]["total"], 1)
        self.assertEqual(len(report["issues"]), 2)  # 2 accounts with warnings

    def test_generate_report_recommendations(self):
        """Test report generates appropriate recommendations."""
        results = [
            {
                "account_id": "x_banned",
                "platform": "X",
                "status": HealthStatus.BANNED,
                "warnings": ["Banned"]
            },
            {
                "account_id": "x_critical",
                "platform": "X",
                "status": HealthStatus.CRITICAL,
                "warnings": []
            }
        ]

        report = self.checker.generate_report(results)

        self.assertGreater(len(report["recommendations"]), 0)
        # Should have recommendation about banned accounts
        recommendations_text = " ".join(report["recommendations"])
        self.assertIn("banned", recommendations_text.lower())


class TestHealthCheckerLogging(unittest.TestCase):
    """Tests for health check logging."""

    def setUp(self):
        """Set up checker and temp log."""
        if not HealthChecker:
            self.skipTest("HealthChecker not importable")

        self.temp_log = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        self.temp_log.close()
        self.checker = HealthChecker()

    def tearDown(self):
        """Clean up temp files."""
        try:
            os.unlink(self.temp_log.name)
        except:
            pass

    def test_log_health_check(self):
        """Test logging a health check result."""
        # Patch the log path
        with patch('health_checker.HEALTH_LOG_PATH', Path(self.temp_log.name)):
            # Initialize log file
            with open(self.temp_log.name, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "account_id", "platform", "status",
                    "login_ok", "restricted", "shadowban", "warnings", "notes"
                ])

            result = {
                "timestamp": datetime.now().isoformat(),
                "account_id": "x_test",
                "platform": "X",
                "status": HealthStatus.HEALTHY,
                "login_ok": True,
                "restricted": False,
                "shadowban": False,
                "warnings": [],
                "notes": "Test check"
            }

            self.checker._log_health_check(result)

        # Verify log entry
        with open(self.temp_log.name) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["account_id"], "x_test")
        self.assertEqual(rows[0]["status"], "healthy")


class TestHealthCheckerQuickStatus(unittest.TestCase):
    """Tests for quick status check."""

    def setUp(self):
        """Set up checker."""
        if not HealthChecker:
            self.skipTest("HealthChecker not importable")
        self.checker = HealthChecker()

    def test_quick_status_no_recent(self):
        """Test quick status with no recent checks."""
        with patch.object(self.checker, '_load_recent_checks', return_value=[]):
            status = self.checker.quick_status()

        self.assertEqual(status["status"], "unknown")

    def test_quick_status_all_healthy(self):
        """Test quick status with all healthy accounts."""
        recent_checks = [
            {"account_id": "x_test1", "status": HealthStatus.HEALTHY, "timestamp": datetime.now().isoformat()},
            {"account_id": "x_test2", "status": HealthStatus.HEALTHY, "timestamp": datetime.now().isoformat()}
        ]

        with patch.object(self.checker, '_load_recent_checks', return_value=recent_checks):
            status = self.checker.quick_status()

        self.assertEqual(status["status"], "ok")
        self.assertEqual(status["healthy"], 2)
        self.assertEqual(status["with_issues"], 0)

    def test_quick_status_with_issues(self):
        """Test quick status with some issues."""
        recent_checks = [
            {"account_id": "x_test1", "status": HealthStatus.HEALTHY, "timestamp": datetime.now().isoformat()},
            {"account_id": "x_test2", "status": HealthStatus.WARNING, "timestamp": datetime.now().isoformat()}
        ]

        with patch.object(self.checker, '_load_recent_checks', return_value=recent_checks):
            status = self.checker.quick_status()

        self.assertEqual(status["status"], "issues")
        self.assertEqual(status["healthy"], 1)
        self.assertEqual(status["with_issues"], 1)


class TestHealthCheckerLoadRecentChecks(unittest.TestCase):
    """Tests for loading recent checks from log."""

    def setUp(self):
        """Set up checker and temp log."""
        if not HealthChecker:
            self.skipTest("HealthChecker not importable")

        self.temp_dir = TEST_OUTPUT_DIR / "health_logs"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.temp_log = self.temp_dir / "health_log.csv"
        self.checker = HealthChecker()

    def tearDown(self):
        """Clean up temp files."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_load_recent_checks(self):
        """Test loading recent health checks."""
        # Create log with recent and old entries
        recent_time = datetime.now().isoformat()
        old_time = (datetime.now() - timedelta(days=5)).isoformat()

        with open(self.temp_log, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "timestamp", "account_id", "platform", "status",
                "login_ok", "restricted", "shadowban", "warnings", "notes"
            ])
            writer.writeheader()
            writer.writerow({
                "timestamp": recent_time,
                "account_id": "x_recent",
                "platform": "X",
                "status": "healthy",
                "login_ok": "True",
                "restricted": "False",
                "shadowban": "False",
                "warnings": "",
                "notes": ""
            })
            writer.writerow({
                "timestamp": old_time,
                "account_id": "x_old",
                "platform": "X",
                "status": "healthy",
                "login_ok": "True",
                "restricted": "False",
                "shadowban": "False",
                "warnings": "",
                "notes": ""
            })

        with patch('health_checker.HEALTH_LOG_PATH', self.temp_log):
            results = self.checker._load_recent_checks(days=1)

        # Should only load recent entry
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["account_id"], "x_recent")


def run_tests(test_type: str = "all") -> Dict[str, Any]:
    """Run tests and return results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestHealthStatus))
    suite.addTests(loader.loadTestsFromTestCase(TestHealthCheckerInit))
    suite.addTests(loader.loadTestsFromTestCase(TestHealthCheckerDetermineStatus))
    suite.addTests(loader.loadTestsFromTestCase(TestHealthCheckerPlatformDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestHealthCheckerXAccount))
    suite.addTests(loader.loadTestsFromTestCase(TestHealthCheckerInstagramAccount))
    suite.addTests(loader.loadTestsFromTestCase(TestHealthCheckerTikTokAccount))
    suite.addTests(loader.loadTestsFromTestCase(TestHealthCheckerCheckAll))
    suite.addTests(loader.loadTestsFromTestCase(TestHealthCheckerReport))
    suite.addTests(loader.loadTestsFromTestCase(TestHealthCheckerLogging))
    suite.addTests(loader.loadTestsFromTestCase(TestHealthCheckerQuickStatus))
    suite.addTests(loader.loadTestsFromTestCase(TestHealthCheckerLoadRecentChecks))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return {
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "success": result.wasSuccessful(),
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Health Checker Test Suite")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--output", "-o", help="Output results to JSON file")

    args = parser.parse_args()

    results = run_tests()

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")

    sys.exit(0 if results["success"] else 1)
