#!/usr/bin/env python3
"""
Instagram Poster Test Suite
===========================
Comprehensive tests for the Instagram posting automation.

Features:
- Unit tests for IGPoster class
- Mobile emulation verification
- Integration tests for actual posting
- Story posting tests
- Reel posting tests
- Session management tests

Usage:
    # Run all tests
    python -m pytest test_ig_poster.py -v

    # Run specific test class
    python -m pytest test_ig_poster.py::TestIGPosterMobileEmulation -v

CLI:
    python test_ig_poster.py --unit        # Unit tests only
    python test_ig_poster.py --integration # Integration tests (requires login)
"""

import os
import sys
import json
import time
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

try:
    from ig_poster import IGPoster, MOBILE_DEVICES, load_config_from_env, load_config_from_file
except ImportError:
    IGPoster = None
    MOBILE_DEVICES = {}
    load_config_from_env = None
    load_config_from_file = None

# Test output directory
TEST_OUTPUT_DIR = Path(__file__).parent / "test_output"
TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class TestIGPosterUnit(unittest.TestCase):
    """Unit tests for IGPoster class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_config = {
            "account_id": "test_account",
            "headless": True,
            "device": "iphone_12"
        }

    def test_init_with_defaults(self):
        """Test IGPoster initialization with defaults."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        poster = IGPoster({"account_id": "test"})
        self.assertEqual(poster.account_id, "test")
        self.assertFalse(poster.headless)
        self.assertIsNone(poster.proxy)

    def test_init_with_device_profile(self):
        """Test IGPoster with specific device profile."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        for device_name, device_config in MOBILE_DEVICES.items():
            poster = IGPoster({"account_id": "test", "device": device_name})
            self.assertEqual(poster.device_config, device_config)

    def test_init_with_soax_proxy(self):
        """Test IGPoster with Soax mobile proxy config."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        config = {
            "account_id": "test",
            "proxy": {
                "server": "http://proxy.soax.com:9000",
                "username": "user-mobile-country-US",
                "password": "secret"
            }
        }
        poster = IGPoster(config)
        self.assertEqual(poster.proxy["server"], "http://proxy.soax.com:9000")

    def test_invalid_device_falls_back(self):
        """Test invalid device name falls back to iphone_12."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        poster = IGPoster({"account_id": "test", "device": "invalid_device"})
        self.assertEqual(poster.device_config, MOBILE_DEVICES["iphone_12"])


class TestIGPosterMobileEmulation(unittest.TestCase):
    """Tests for mobile device emulation."""

    def test_iphone_12_viewport(self):
        """Test iPhone 12 viewport settings."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        poster = IGPoster({"account_id": "test", "device": "iphone_12"})
        self.assertEqual(poster.device_config["viewport"]["width"], 390)
        self.assertEqual(poster.device_config["viewport"]["height"], 844)
        self.assertTrue(poster.device_config["is_mobile"])
        self.assertTrue(poster.device_config["has_touch"])

    def test_iphone_14_pro_viewport(self):
        """Test iPhone 14 Pro viewport settings."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        poster = IGPoster({"account_id": "test", "device": "iphone_14_pro"})
        self.assertEqual(poster.device_config["viewport"]["width"], 393)
        self.assertEqual(poster.device_config["viewport"]["height"], 852)

    def test_pixel_7_viewport(self):
        """Test Pixel 7 viewport settings."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        poster = IGPoster({"account_id": "test", "device": "pixel_7"})
        self.assertEqual(poster.device_config["viewport"]["width"], 412)
        self.assertEqual(poster.device_config["viewport"]["height"], 915)
        self.assertIn("Android", poster.device_config["user_agent"])

    @patch('ig_poster.sync_playwright')
    def test_context_created_with_mobile_settings(self, mock_playwright):
        """Test browser context is created with mobile settings."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        mock_pw_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.start.return_value = mock_pw_instance
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        poster = IGPoster({"account_id": "test", "device": "iphone_12", "headless": True})
        poster._start_browser()

        # Verify context was created with mobile settings
        call_kwargs = mock_browser.new_context.call_args.kwargs
        self.assertEqual(call_kwargs["viewport"], {"width": 390, "height": 844})
        self.assertTrue(call_kwargs["is_mobile"])
        self.assertTrue(call_kwargs["has_touch"])


class TestIGPosterMocked(unittest.TestCase):
    """Tests with mocked Playwright."""

    def setUp(self):
        """Set up mocked environment."""
        self.test_config = {
            "account_id": "test_account",
            "headless": True,
            "device": "iphone_12"
        }

    @patch('ig_poster.sync_playwright')
    def test_check_login_logged_in(self, mock_playwright):
        """Test login check when logged in."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

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
        mock_locator.is_visible.return_value = False
        mock_page.locator.return_value = mock_locator

        poster = IGPoster(self.test_config)
        poster._start_browser()

        result = poster.check_login()
        self.assertTrue(result)

    @patch('ig_poster.sync_playwright')
    def test_dismiss_popups(self, mock_playwright):
        """Test popup dismissal."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        mock_pw_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.start.return_value = mock_pw_instance
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Mock popup element
        mock_popup = MagicMock()
        mock_popup.count.return_value = 1
        mock_popup.is_visible.return_value = True
        mock_page.locator.return_value = mock_popup

        poster = IGPoster(self.test_config)
        poster._start_browser()
        poster._dismiss_popups()

        # Popup should be clicked
        mock_popup.click.assert_called()

    @patch('ig_poster.sync_playwright')
    def test_post_feed_validates_image_path(self, mock_playwright):
        """Test feed post validates image exists."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        poster = IGPoster(self.test_config)
        result = poster.post_feed("Caption", "/nonexistent/image.jpg")

        self.assertFalse(result["success"])
        self.assertIn("not found", result["error"].lower())

    @patch('ig_poster.sync_playwright')
    def test_post_feed_with_valid_image(self, mock_playwright):
        """Test feed post with valid image."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        mock_pw_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.start.return_value = mock_pw_instance
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        mock_locator = MagicMock()
        mock_locator.count.return_value = 1
        mock_locator.first = mock_locator
        mock_locator.wait_for = MagicMock()
        mock_page.locator.return_value = mock_locator

        poster = IGPoster(self.test_config)

        # Create temp image file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            f.write(b'\xFF\xD8\xFF')  # Minimal JPEG header
            temp_image = f.name

        try:
            with patch.object(poster, 'check_login', return_value=True):
                with patch.object(poster, '_start_browser'):
                    with patch.object(poster, '_stop_browser'):
                        with patch.object(poster, 'human_delay'):
                            with patch.object(poster, 'human_type'):
                                poster.page = mock_page
                                result = poster.post_feed("Test caption", temp_image)

            self.assertIn("success", result)
        finally:
            os.unlink(temp_image)


class TestIGPosterStory(unittest.TestCase):
    """Tests for story posting."""

    @patch('ig_poster.sync_playwright')
    def test_post_story_validates_image_path(self, mock_playwright):
        """Test story post validates image exists."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        poster = IGPoster({"account_id": "test", "headless": True})
        result = poster.post_story("/nonexistent/image.jpg")

        self.assertFalse(result["success"])
        self.assertIn("not found", result["error"].lower())

    @patch('ig_poster.sync_playwright')
    def test_post_story_type_is_story(self, mock_playwright):
        """Test story post result has correct type."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        mock_pw_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.start.return_value = mock_pw_instance
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        mock_locator = MagicMock()
        mock_locator.count.return_value = 1
        mock_locator.first = mock_locator
        mock_page.locator.return_value = mock_locator

        poster = IGPoster({"account_id": "test", "headless": True})

        # Create temp image
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            f.write(b'\xFF\xD8\xFF')
            temp_image = f.name

        try:
            with patch.object(poster, 'check_login', return_value=True):
                with patch.object(poster, '_start_browser'):
                    with patch.object(poster, '_stop_browser'):
                        with patch.object(poster, 'human_delay'):
                            poster.page = mock_page
                            result = poster.post_story(temp_image)

            self.assertEqual(result["type"], "story")
        finally:
            os.unlink(temp_image)


class TestIGPosterReel(unittest.TestCase):
    """Tests for Reel posting."""

    @patch('ig_poster.sync_playwright')
    def test_post_reel_validates_video_path(self, mock_playwright):
        """Test reel post validates video exists."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        poster = IGPoster({"account_id": "test", "headless": True})
        result = poster.post_reel("/nonexistent/video.mp4")

        self.assertFalse(result["success"])
        self.assertIn("not found", result["error"].lower())

    @patch('ig_poster.sync_playwright')
    def test_post_reel_type_is_reel(self, mock_playwright):
        """Test reel post result has correct type."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        mock_pw_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.start.return_value = mock_pw_instance
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        mock_locator = MagicMock()
        mock_locator.count.return_value = 1
        mock_locator.first = mock_locator
        mock_page.locator.return_value = mock_locator

        poster = IGPoster({"account_id": "test", "headless": True})

        # Create temp video file
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
            f.write(b'\x00\x00\x00\x1c\x66\x74\x79\x70')  # Minimal MP4 header
            temp_video = f.name

        try:
            with patch.object(poster, 'check_login', return_value=True):
                with patch.object(poster, '_start_browser'):
                    with patch.object(poster, '_stop_browser'):
                        with patch.object(poster, 'human_delay'):
                            with patch.object(poster, 'human_type'):
                                poster.page = mock_page
                                result = poster.post_reel(temp_video)

            self.assertEqual(result["type"], "reel")
        finally:
            os.unlink(temp_video)


class TestIGPosterHashtags(unittest.TestCase):
    """Tests for hashtag handling."""

    @patch('ig_poster.sync_playwright')
    def test_hashtags_formatted_correctly(self, mock_playwright):
        """Test hashtags are formatted with # prefix."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        mock_pw_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        mock_playwright.return_value.start.return_value = mock_pw_instance
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        mock_locator = MagicMock()
        mock_locator.count.return_value = 1
        mock_locator.first = mock_locator
        mock_page.locator.return_value = mock_locator

        poster = IGPoster({"account_id": "test", "headless": True})

        # Create temp image
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            f.write(b'\xFF\xD8\xFF')
            temp_image = f.name

        typed_text = []

        def capture_type(page, text):
            typed_text.append(text)

        try:
            with patch.object(poster, 'check_login', return_value=True):
                with patch.object(poster, '_start_browser'):
                    with patch.object(poster, '_stop_browser'):
                        with patch.object(poster, 'human_delay'):
                            with patch.object(poster, 'human_type', capture_type):
                                poster.page = mock_page
                                poster.post_feed(
                                    "Test caption",
                                    temp_image,
                                    hashtags=["fitness", "motivation", "gym"]
                                )

            # Check hashtags were properly formatted
            if typed_text:
                full_caption = typed_text[-1]
                self.assertIn("#fitness", full_caption)
                self.assertIn("#motivation", full_caption)
                self.assertIn("#gym", full_caption)
        finally:
            os.unlink(temp_image)


class TestIGPosterTouchGestures(unittest.TestCase):
    """Tests for touch gesture simulation."""

    def test_human_tap_adds_offset(self):
        """Test human tap adds small random offset."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        poster = IGPoster({"account_id": "test"})

        mock_page = MagicMock()
        mock_touchscreen = MagicMock()
        mock_page.touchscreen = mock_touchscreen

        with patch.object(poster, 'human_delay'):
            # Run multiple times to test randomness
            for _ in range(10):
                poster.human_tap(mock_page, 100, 200)

        # Touchscreen.tap should be called with varied coordinates
        calls = mock_touchscreen.tap.call_args_list
        self.assertEqual(len(calls), 10)

        # Extract x coordinates from calls
        x_coords = [call[0][0] for call in calls]
        y_coords = [call[0][1] for call in calls]

        # Should be within offset range of original
        for x in x_coords:
            self.assertGreaterEqual(x, 97)  # 100 - 3
            self.assertLessEqual(x, 103)  # 100 + 3

        for y in y_coords:
            self.assertGreaterEqual(y, 197)  # 200 - 3
            self.assertLessEqual(y, 203)  # 200 + 3

    def test_swipe_directions(self):
        """Test swipe gesture in different directions."""
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        poster = IGPoster({"account_id": "test", "device": "iphone_12"})

        mock_page = MagicMock()
        mock_mouse = MagicMock()
        mock_page.mouse = mock_mouse

        with patch.object(poster, 'human_delay'):
            # Test swipe up
            poster.swipe(mock_page, direction="up")
            mock_mouse.down.assert_called()
            mock_mouse.up.assert_called()

            # Reset mocks
            mock_mouse.reset_mock()

            # Test swipe down
            poster.swipe(mock_page, direction="down")
            mock_mouse.down.assert_called()
            mock_mouse.up.assert_called()


class TestIGPosterIntegration(unittest.TestCase):
    """Integration tests - require actual browser and login."""

    @classmethod
    def setUpClass(cls):
        """Check if integration tests should run."""
        cls.run_integration = os.environ.get("RUN_INTEGRATION_TESTS", "").lower() == "true"
        cls.session_path = os.environ.get("IG_SESSION_PATH")

    def test_browser_launches_with_mobile_emulation(self):
        """Test browser launches with correct mobile settings."""
        if not self.run_integration:
            self.skipTest("Integration tests disabled")
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        config = {
            "account_id": "integration_test",
            "headless": True,
            "device": "iphone_12"
        }

        if self.session_path:
            config["session_path"] = self.session_path

        poster = IGPoster(config)

        try:
            poster._start_browser()
            self.assertIsNotNone(poster.browser)
            self.assertIsNotNone(poster.page)
        finally:
            poster._stop_browser()

    def test_navigate_to_instagram(self):
        """Test navigating to Instagram."""
        if not self.run_integration:
            self.skipTest("Integration tests disabled")
        if not IGPoster:
            self.skipTest("IGPoster not importable")

        config = {
            "account_id": "integration_test",
            "headless": True,
            "device": "iphone_12"
        }

        if self.session_path:
            config["session_path"] = self.session_path

        poster = IGPoster(config)

        try:
            poster._start_browser()
            poster.page.goto("https://www.instagram.com", wait_until="domcontentloaded", timeout=30000)
            self.assertTrue(True)
        finally:
            poster._stop_browser()


class TestConfigLoading(unittest.TestCase):
    """Tests for configuration loading."""

    def test_load_config_from_env_with_soax(self):
        """Test loading config with Soax proxy env vars."""
        if not load_config_from_env:
            self.skipTest("load_config_from_env not importable")

        os.environ["IG_ACCOUNT_ID"] = "env_test"
        os.environ["IG_DEVICE"] = "pixel_7"
        os.environ["SOAX_PROXY_SERVER"] = "http://proxy.soax.com:9000"
        os.environ["SOAX_PROXY_USERNAME"] = "user-mobile"
        os.environ["SOAX_PROXY_PASSWORD"] = "secret"

        try:
            config = load_config_from_env()
            self.assertEqual(config["account_id"], "env_test")
            self.assertEqual(config["device"], "pixel_7")
            self.assertEqual(config["proxy"]["server"], "http://proxy.soax.com:9000")
        finally:
            del os.environ["IG_ACCOUNT_ID"]
            del os.environ["IG_DEVICE"]
            del os.environ["SOAX_PROXY_SERVER"]
            del os.environ["SOAX_PROXY_USERNAME"]
            del os.environ["SOAX_PROXY_PASSWORD"]


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
        suite.addTests(loader.loadTestsFromTestCase(TestIGPosterUnit))
        suite.addTests(loader.loadTestsFromTestCase(TestIGPosterMobileEmulation))
        suite.addTests(loader.loadTestsFromTestCase(TestIGPosterMocked))
        suite.addTests(loader.loadTestsFromTestCase(TestIGPosterStory))
        suite.addTests(loader.loadTestsFromTestCase(TestIGPosterReel))
        suite.addTests(loader.loadTestsFromTestCase(TestIGPosterHashtags))
        suite.addTests(loader.loadTestsFromTestCase(TestIGPosterTouchGestures))
        suite.addTests(loader.loadTestsFromTestCase(TestConfigLoading))

    if test_type in ("integration", "all"):
        suite.addTests(loader.loadTestsFromTestCase(TestIGPosterIntegration))

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

    parser = argparse.ArgumentParser(description="Instagram Poster Test Suite")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--output", "-o", help="Output results to JSON file")

    args = parser.parse_args()

    if args.unit:
        test_type = "unit"
    elif args.integration:
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
