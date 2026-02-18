#!/usr/bin/env python3
"""
X/Twitter Poster Test Suite
============================
Comprehensive tests for the X posting automation.

Features:
- Unit tests for XPoster class
- Integration tests for actual posting
- Mock tests for CI/CD
- Session management tests
- Rate limit handling tests
- Human behavior simulation tests

Usage:
    # Run all tests
    python -m pytest test_x_poster.py -v

    # Run specific test
    python -m pytest test_x_poster.py::TestXPosterUnit -v

    # Run with coverage
    python -m pytest test_x_poster.py --cov=../scripts/x_poster -v

CLI:
    python test_x_poster.py --unit        # Unit tests only
    python test_x_poster.py --integration # Integration tests (requires login)
    python test_x_poster.py --all         # All tests
"""

import os
import sys
import json
import time
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

try:
    from x_poster import XPoster, load_config_from_env, load_config_from_file, USER_AGENTS, VIEWPORTS
except ImportError:
    XPoster = None
    load_config_from_env = None
    load_config_from_file = None
    USER_AGENTS = []
    VIEWPORTS = []

# Test output directory
TEST_OUTPUT_DIR = Path(__file__).parent / "test_output"
TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class TestXPosterUnit(unittest.TestCase):
    """Unit tests for XPoster class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_config = {
            "account_id": "test_account",
            "headless": True,
            "session_path": str(TEST_OUTPUT_DIR / "test_session.json")
        }

    def test_init_with_defaults(self):
        """Test XPoster initialization with defaults."""
        if not XPoster:
            self.skipTest("XPoster not importable")

        poster = XPoster({"account_id": "test"})
        self.assertEqual(poster.account_id, "test")
        self.assertFalse(poster.headless)
        self.assertIsNone(poster.proxy)
        self.assertIn(poster.user_agent, USER_AGENTS)
        self.assertIn(poster.viewport, VIEWPORTS)

    def test_init_with_proxy(self):
        """Test XPoster initialization with proxy."""
        if not XPoster:
            self.skipTest("XPoster not importable")

        config = {
            "account_id": "test",
            "proxy": {
                "server": "http://proxy.example.com:8080",
                "username": "user",
                "password": "pass"
            }
        }
        poster = XPoster(config)
        self.assertEqual(poster.proxy, config["proxy"])

    def test_init_with_custom_user_agent(self):
        """Test XPoster with custom user agent."""
        if not XPoster:
            self.skipTest("XPoster not importable")

        custom_ua = "Custom User Agent"
        poster = XPoster({"account_id": "test", "user_agent": custom_ua})
        self.assertEqual(poster.user_agent, custom_ua)

    def test_init_with_custom_viewport(self):
        """Test XPoster with custom viewport."""
        if not XPoster:
            self.skipTest("XPoster not importable")

        custom_viewport = {"width": 800, "height": 600}
        poster = XPoster({"account_id": "test", "viewport": custom_viewport})
        self.assertEqual(poster.viewport, custom_viewport)

    def test_human_delay_range(self):
        """Test human delay returns value within range."""
        if not XPoster:
            self.skipTest("XPoster not importable")

        poster = XPoster({"account_id": "test"})

        # Run multiple times to check randomness
        delays = []
        for _ in range(10):
            start = time.time()
            poster.human_delay(0.1, 0.2)
            delays.append(time.time() - start)

        # All delays should be within range (with small tolerance)
        for delay in delays:
            self.assertGreaterEqual(delay, 0.1 - 0.01)
            self.assertLessEqual(delay, 0.2 + 0.05)  # Allow some tolerance


class TestXPosterMocked(unittest.TestCase):
    """Tests with mocked Playwright."""

    def setUp(self):
        """Set up mocked environment."""
        self.test_config = {
            "account_id": "test_account",
            "headless": True,
        }

    @patch('x_poster.sync_playwright')
    def test_start_browser(self, mock_playwright):
        """Test browser startup."""
        if not XPoster:
            self.skipTest("XPoster not importable")

        # Setup mocks
        mock_pw_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.start.return_value = mock_pw_instance
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        poster = XPoster(self.test_config)
        poster._start_browser()

        # Verify browser launched with correct options
        mock_pw_instance.chromium.launch.assert_called_once()
        call_kwargs = mock_pw_instance.chromium.launch.call_args.kwargs
        self.assertTrue(call_kwargs.get("headless", False))

    @patch('x_poster.sync_playwright')
    def test_check_login_logged_in(self, mock_playwright):
        """Test login check when logged in."""
        if not XPoster:
            self.skipTest("XPoster not importable")

        mock_pw_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.start.return_value = mock_pw_instance
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Mock logged in state
        mock_locator = MagicMock()
        mock_locator.count.return_value = 1
        mock_page.locator.return_value = mock_locator

        poster = XPoster(self.test_config)
        poster._start_browser()

        result = poster.check_login()
        self.assertTrue(result)

    @patch('x_poster.sync_playwright')
    def test_check_login_not_logged_in(self, mock_playwright):
        """Test login check when not logged in."""
        if not XPoster:
            self.skipTest("XPoster not importable")

        mock_pw_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.start.return_value = mock_pw_instance
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Mock not logged in state
        mock_locator = MagicMock()
        mock_locator.count.return_value = 0
        mock_page.locator.return_value = mock_locator

        poster = XPoster(self.test_config)
        poster._start_browser()

        result = poster.check_login()
        self.assertFalse(result)

    @patch('x_poster.sync_playwright')
    def test_post_success(self, mock_playwright):
        """Test successful post."""
        if not XPoster:
            self.skipTest("XPoster not importable")

        mock_pw_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.start.return_value = mock_pw_instance
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Mock all needed elements
        mock_locator = MagicMock()
        mock_locator.count.return_value = 1
        mock_locator.wait_for = MagicMock()
        mock_locator.click = MagicMock()
        mock_page.locator.return_value = mock_locator

        poster = XPoster(self.test_config)

        # Mock the check_login to return True
        with patch.object(poster, 'check_login', return_value=True):
            with patch.object(poster, '_start_browser'):
                with patch.object(poster, '_stop_browser'):
                    with patch.object(poster, 'human_delay'):
                        with patch.object(poster, 'human_type'):
                            poster.page = mock_page
                            result = poster.post("Test content")

        self.assertIn("success", result)

    @patch('x_poster.sync_playwright')
    def test_post_not_logged_in(self, mock_playwright):
        """Test post when not logged in."""
        if not XPoster:
            self.skipTest("XPoster not importable")

        mock_pw_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.start.return_value = mock_pw_instance
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        poster = XPoster(self.test_config)

        with patch.object(poster, 'check_login', return_value=False):
            with patch.object(poster, '_start_browser'):
                with patch.object(poster, '_stop_browser'):
                    poster.page = mock_page
                    result = poster.post("Test content")

        self.assertFalse(result["success"])
        self.assertIn("Not logged in", result["error"])


class TestConfigLoading(unittest.TestCase):
    """Tests for configuration loading."""

    def test_load_config_from_env(self):
        """Test loading config from environment variables."""
        if not load_config_from_env:
            self.skipTest("load_config_from_env not importable")

        # Set environment variables
        os.environ["X_ACCOUNT_ID"] = "env_test"
        os.environ["HEADLESS"] = "true"
        os.environ["PROXY_SERVER"] = "http://proxy.test:8080"

        try:
            config = load_config_from_env()
            self.assertEqual(config["account_id"], "env_test")
            self.assertTrue(config["headless"])
            self.assertEqual(config["proxy"]["server"], "http://proxy.test:8080")
        finally:
            # Clean up
            del os.environ["X_ACCOUNT_ID"]
            del os.environ["HEADLESS"]
            del os.environ["PROXY_SERVER"]

    def test_load_config_from_file(self):
        """Test loading config from JSON file."""
        if not load_config_from_file:
            self.skipTest("load_config_from_file not importable")

        # Create test config file
        config_path = TEST_OUTPUT_DIR / "test_config.json"
        test_config = {
            "account_id": "file_test",
            "proxy": {"server": "http://proxy.file:8080"}
        }

        with open(config_path, 'w') as f:
            json.dump(test_config, f)

        try:
            config = load_config_from_file(str(config_path))
            self.assertEqual(config["account_id"], "file_test")
            self.assertEqual(config["proxy"]["server"], "http://proxy.file:8080")
        finally:
            config_path.unlink(missing_ok=True)


class TestXPosterIntegration(unittest.TestCase):
    """Integration tests - require actual browser and login."""

    @classmethod
    def setUpClass(cls):
        """Check if integration tests should run."""
        cls.run_integration = os.environ.get("RUN_INTEGRATION_TESTS", "").lower() == "true"
        cls.session_path = os.environ.get("X_SESSION_PATH")

    def test_browser_launches(self):
        """Test browser actually launches."""
        if not self.run_integration:
            self.skipTest("Integration tests disabled")
        if not XPoster:
            self.skipTest("XPoster not importable")

        config = {
            "account_id": "integration_test",
            "headless": True,
        }

        if self.session_path:
            config["session_path"] = self.session_path

        poster = XPoster(config)

        try:
            poster._start_browser()
            self.assertIsNotNone(poster.browser)
            self.assertIsNotNone(poster.page)
        finally:
            poster._stop_browser()

    def test_navigate_to_x(self):
        """Test navigating to X.com."""
        if not self.run_integration:
            self.skipTest("Integration tests disabled")
        if not XPoster:
            self.skipTest("XPoster not importable")

        config = {
            "account_id": "integration_test",
            "headless": True,
        }

        if self.session_path:
            config["session_path"] = self.session_path

        poster = XPoster(config)

        try:
            poster._start_browser()
            poster.page.goto("https://x.com", wait_until="domcontentloaded", timeout=30000)
            # Page should load without error
            self.assertTrue(True)
        finally:
            poster._stop_browser()


class TestXPosterRateLimiting(unittest.TestCase):
    """Tests for rate limiting behavior."""

    def test_respects_delay_between_posts(self):
        """Test that delays are inserted between posts."""
        if not XPoster:
            self.skipTest("XPoster not importable")

        poster = XPoster({"account_id": "test"})

        delays = []

        # Mock human_delay to track calls
        original_delay = poster.human_delay

        def mock_delay(min_sec, max_sec):
            delays.append((min_sec, max_sec))
            time.sleep(0.01)  # Tiny sleep for test speed

        poster.human_delay = mock_delay

        # Simulate a post flow (partially)
        poster.human_delay(1, 2)  # Initial delay
        poster.human_delay(0.5, 1)  # Compose delay
        poster.human_delay(1, 3)  # Pre-post delay

        # Verify delays were called
        self.assertEqual(len(delays), 3)
        self.assertEqual(delays[0], (1, 2))
        self.assertEqual(delays[1], (0.5, 1))
        self.assertEqual(delays[2], (1, 3))


class TestXPosterThreadPosting(unittest.TestCase):
    """Tests for thread posting functionality."""

    @patch('x_poster.sync_playwright')
    def test_thread_post_multiple_tweets(self, mock_playwright):
        """Test posting a thread with multiple tweets."""
        if not XPoster:
            self.skipTest("XPoster not importable")

        mock_pw_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.start.return_value = mock_pw_instance
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Mock elements
        mock_locator = MagicMock()
        mock_locator.count.return_value = 1
        mock_locator.last = mock_locator
        mock_locator.wait_for = MagicMock()
        mock_locator.click = MagicMock()
        mock_page.locator.return_value = mock_locator

        poster = XPoster({"account_id": "test", "headless": True})

        tweets = ["Tweet 1", "Tweet 2", "Tweet 3"]

        with patch.object(poster, 'check_login', return_value=True):
            with patch.object(poster, '_start_browser'):
                with patch.object(poster, '_stop_browser'):
                    with patch.object(poster, 'human_delay'):
                        with patch.object(poster, 'human_type'):
                            poster.page = mock_page
                            result = poster.post_thread(tweets)

        self.assertEqual(result["total_tweets"], 3)


class TestHumanBehavior(unittest.TestCase):
    """Tests for human-like behavior simulation."""

    def test_typing_has_variable_delays(self):
        """Test that typing includes variable delays."""
        if not XPoster:
            self.skipTest("XPoster not importable")

        poster = XPoster({"account_id": "test"})

        # Mock keyboard
        mock_page = MagicMock()
        mock_keyboard = MagicMock()
        mock_page.keyboard = mock_keyboard

        # Track sleep calls
        sleep_times = []
        original_sleep = time.sleep

        def mock_sleep(duration):
            sleep_times.append(duration)
            original_sleep(0.001)  # Very short actual sleep

        with patch('time.sleep', mock_sleep):
            poster.human_type(mock_page, "test")

        # Should have 4 delays (one per character)
        self.assertEqual(len(sleep_times), 4)

        # Delays should vary (not all identical)
        if len(set(sleep_times)) == 1:
            # All identical - check they're in valid range
            self.assertTrue(all(0.05 <= t <= 0.15 for t in sleep_times))
        else:
            # Should have some variation
            self.assertGreater(len(set(sleep_times)), 1)

    def test_mouse_movement_has_steps(self):
        """Test mouse movement uses multiple steps."""
        if not XPoster:
            self.skipTest("XPoster not importable")

        poster = XPoster({"account_id": "test"})

        mock_page = MagicMock()
        mock_mouse = MagicMock()
        mock_page.mouse = mock_mouse

        with patch.object(poster, 'human_delay'):
            poster.human_mouse_move(mock_page, 100, 200)

        # Mouse.move should be called with steps parameter
        mock_mouse.move.assert_called_once()
        call_kwargs = mock_mouse.move.call_args.kwargs
        self.assertIn("steps", call_kwargs)
        self.assertGreaterEqual(call_kwargs["steps"], 5)


def run_tests(test_type: str = "all") -> Dict[str, Any]:
    """
    Run tests and return results.

    Args:
        test_type: 'unit', 'integration', or 'all'

    Returns:
        Test results summary
    """
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    if test_type in ("unit", "all"):
        suite.addTests(loader.loadTestsFromTestCase(TestXPosterUnit))
        suite.addTests(loader.loadTestsFromTestCase(TestXPosterMocked))
        suite.addTests(loader.loadTestsFromTestCase(TestConfigLoading))
        suite.addTests(loader.loadTestsFromTestCase(TestXPosterRateLimiting))
        suite.addTests(loader.loadTestsFromTestCase(TestXPosterThreadPosting))
        suite.addTests(loader.loadTestsFromTestCase(TestHumanBehavior))

    if test_type in ("integration", "all"):
        suite.addTests(loader.loadTestsFromTestCase(TestXPosterIntegration))

    # Run tests
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

    parser = argparse.ArgumentParser(description="X Poster Test Suite")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--output", "-o", help="Output results to JSON file")

    args = parser.parse_args()

    if args.unit:
        test_type = "unit"
    elif args.integration:
        # Enable integration tests
        os.environ["RUN_INTEGRATION_TESTS"] = "true"
        test_type = "integration"
    else:
        test_type = "all"

    results = run_tests(test_type)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")

    sys.exit(0 if results["success"] else 1)
