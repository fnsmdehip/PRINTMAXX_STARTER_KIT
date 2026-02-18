#!/usr/bin/env python3
"""
Proxy Tester Test Suite
=======================
Comprehensive tests for the ProxyTester class.

Features:
- Connectivity check tests
- Geolocation lookup tests
- Rotation tests
- Speed test tests
- Platform access tests

Usage:
    python -m pytest test_proxy_tester.py -v
    python test_proxy_tester.py --unit
"""

import os
import sys
import json
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

try:
    from proxy_tester import ProxyTester, load_proxies_from_file, PLATFORM_URLS, IP_CHECK_URLS
except ImportError:
    ProxyTester = None
    load_proxies_from_file = None
    PLATFORM_URLS = {}
    IP_CHECK_URLS = []

# Test output directory
TEST_OUTPUT_DIR = Path(__file__).parent / "test_output"
TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class TestProxyTesterInit(unittest.TestCase):
    """Tests for ProxyTester initialization."""

    def test_init_with_defaults(self):
        """Test tester initialization with defaults."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        tester = ProxyTester()
        self.assertEqual(tester.timeout, 30)
        self.assertEqual(tester.results_cache, {})

    def test_init_with_custom_timeout(self):
        """Test tester with custom timeout."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        tester = ProxyTester(timeout=60)
        self.assertEqual(tester.timeout, 60)


class TestProxyURLParsing(unittest.TestCase):
    """Tests for proxy URL parsing."""

    def setUp(self):
        """Set up tester."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")
        self.tester = ProxyTester()

    def test_parse_proxy_string(self):
        """Test parsing proxy URL string."""
        proxy = "http://user:pass@proxy.example.com:8080"
        result = self.tester._parse_proxy_url(proxy)

        self.assertEqual(result["server"], "http://proxy.example.com:8080")
        self.assertEqual(result["username"], "user")
        self.assertEqual(result["password"], "pass")

    def test_parse_proxy_dict(self):
        """Test parsing proxy dict passes through."""
        proxy = {
            "server": "http://proxy.example.com:8080",
            "username": "user",
            "password": "pass"
        }
        result = self.tester._parse_proxy_url(proxy)

        self.assertEqual(result, proxy)

    def test_build_proxy_url_with_auth(self):
        """Test building proxy URL with authentication."""
        proxy = {
            "server": "http://proxy.example.com:8080",
            "username": "user",
            "password": "pass"
        }
        result = self.tester._build_proxy_url(proxy)

        self.assertEqual(result, "http://user:pass@proxy.example.com:8080")

    def test_build_proxy_url_without_auth(self):
        """Test building proxy URL without authentication."""
        proxy = {"server": "http://proxy.example.com:8080"}
        result = self.tester._build_proxy_url(proxy)

        self.assertEqual(result, "http://proxy.example.com:8080")


class TestProxyConnectivity(unittest.TestCase):
    """Tests for connectivity checks."""

    def setUp(self):
        """Set up tester."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")
        self.tester = ProxyTester(timeout=5)

    @patch('proxy_tester.requests')
    def test_connectivity_success(self, mock_requests):
        """Test successful connectivity check."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests.get.return_value = mock_response

        proxy = {"server": "http://proxy.example.com:8080"}
        result = self.tester.test_connectivity(proxy)

        self.assertTrue(result["success"])
        self.assertIsNotNone(result["latency_ms"])
        self.assertEqual(result["test"], "connectivity")

    @patch('proxy_tester.requests')
    def test_connectivity_proxy_error(self, mock_requests):
        """Test connectivity with proxy error."""
        mock_requests.get.side_effect = mock_requests.exceptions.ProxyError("Connection refused")
        mock_requests.exceptions.ProxyError = Exception

        proxy = {"server": "http://bad.proxy:8080"}
        result = self.tester.test_connectivity(proxy)

        self.assertFalse(result["success"])
        self.assertIn("error", result)

    @patch('proxy_tester.requests')
    def test_connectivity_timeout(self, mock_requests):
        """Test connectivity with timeout."""
        mock_requests.get.side_effect = mock_requests.exceptions.ConnectTimeout("Timeout")
        mock_requests.exceptions.ConnectTimeout = Exception

        proxy = {"server": "http://slow.proxy:8080"}
        result = self.tester.test_connectivity(proxy)

        self.assertFalse(result["success"])

    def test_connectivity_no_requests(self):
        """Test connectivity when requests not available."""
        with patch.object(self.tester, 'test_connectivity') as mock:
            mock.return_value = {"success": False, "error": "requests not installed"}
            result = mock({"server": "http://proxy:8080"})
            self.assertFalse(result["success"])


class TestProxyIPInfo(unittest.TestCase):
    """Tests for IP information retrieval."""

    def setUp(self):
        """Set up tester."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")
        self.tester = ProxyTester(timeout=5)

    @patch('proxy_tester.requests')
    def test_get_ip_info_success(self, mock_requests):
        """Test successful IP info retrieval."""
        # Mock IP response
        mock_ip_response = MagicMock()
        mock_ip_response.status_code = 200
        mock_ip_response.json.return_value = {"ip": "123.45.67.89"}

        # Mock geo response
        mock_geo_response = MagicMock()
        mock_geo_response.status_code = 200
        mock_geo_response.json.return_value = {
            "country_name": "United States",
            "country_code": "US",
            "region": "California",
            "city": "Los Angeles",
            "org": "Test ISP",
            "asn": "AS12345"
        }

        mock_requests.get.side_effect = [mock_ip_response, mock_geo_response]

        proxy = {"server": "http://proxy:8080"}
        result = self.tester.get_ip_info(proxy)

        self.assertTrue(result["success"])
        self.assertEqual(result["ip"], "123.45.67.89")
        self.assertIsNotNone(result["geo"])
        self.assertEqual(result["geo"]["country"], "United States")
        self.assertEqual(result["geo"]["city"], "Los Angeles")

    @patch('proxy_tester.requests')
    def test_get_ip_info_ip_only(self, mock_requests):
        """Test IP info when geo lookup fails."""
        mock_ip_response = MagicMock()
        mock_ip_response.status_code = 200
        mock_ip_response.json.return_value = {"ip": "123.45.67.89"}

        mock_geo_response = MagicMock()
        mock_geo_response.status_code = 429  # Rate limited

        mock_requests.get.side_effect = [mock_ip_response, mock_geo_response]

        proxy = {"server": "http://proxy:8080"}
        result = self.tester.get_ip_info(proxy)

        self.assertTrue(result["success"])
        self.assertEqual(result["ip"], "123.45.67.89")
        self.assertIsNone(result["geo"])


class TestProxyPlatformAccess(unittest.TestCase):
    """Tests for platform accessibility checks."""

    def setUp(self):
        """Set up tester."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")
        self.tester = ProxyTester(timeout=10)

    def test_platform_urls_defined(self):
        """Test platform URLs are defined."""
        self.assertIn("x", PLATFORM_URLS)
        self.assertIn("instagram", PLATFORM_URLS)
        self.assertIn("tiktok", PLATFORM_URLS)

    @patch('proxy_tester.sync_playwright')
    def test_platform_access_success(self, mock_playwright):
        """Test successful platform access."""
        # Mock playwright
        mock_pw_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()
        mock_response = MagicMock()

        mock_playwright.return_value.__enter__.return_value = mock_pw_instance
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        mock_page.goto.return_value = mock_response
        mock_page.content.return_value = "<html>Normal page content</html>"
        mock_response.ok = True
        mock_response.status = 200

        proxy = {"server": "http://proxy:8080"}
        result = self.tester.test_platform_access(proxy, "x")

        self.assertTrue(result["success"])
        self.assertFalse(result["blocked"])
        self.assertEqual(result["platform"], "x")

    @patch('proxy_tester.sync_playwright')
    def test_platform_access_blocked(self, mock_playwright):
        """Test blocked platform access."""
        mock_pw_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()
        mock_response = MagicMock()

        mock_playwright.return_value.__enter__.return_value = mock_pw_instance
        mock_pw_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        mock_page.goto.return_value = mock_response
        mock_page.content.return_value = "<html>Access denied - Please verify you are human</html>"
        mock_response.ok = True
        mock_response.status = 200

        proxy = {"server": "http://proxy:8080"}
        result = self.tester.test_platform_access(proxy, "instagram")

        self.assertTrue(result["blocked"])
        self.assertFalse(result["success"])
        self.assertIn("block_reason", result)

    def test_platform_access_unknown_platform(self):
        """Test access check for unknown platform."""
        proxy = {"server": "http://proxy:8080"}
        result = self.tester.test_platform_access(proxy, "unknown_platform")

        self.assertFalse(result["success"])
        self.assertIn("Unknown platform", result["error"])


class TestProxyRotation(unittest.TestCase):
    """Tests for proxy rotation checks."""

    def setUp(self):
        """Set up tester."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")
        self.tester = ProxyTester(timeout=5)

    @patch('proxy_tester.requests')
    def test_rotation_static_ip(self, mock_requests):
        """Test rotation check with static IP."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ip": "1.2.3.4"}
        mock_requests.get.return_value = mock_response

        proxy = {"server": "http://static.proxy:8080"}
        result = self.tester.test_rotation(proxy, requests_count=3, delay=0.01)

        self.assertTrue(result["success"])
        self.assertEqual(result["unique_ips"], 1)
        self.assertFalse(result["rotates"])
        self.assertEqual(len(result["ips"]), 3)

    @patch('proxy_tester.requests')
    def test_rotation_rotating_ip(self, mock_requests):
        """Test rotation check with rotating IP."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        # Return different IPs each call
        mock_response.json.side_effect = [
            {"ip": "1.1.1.1"},
            {"ip": "2.2.2.2"},
            {"ip": "3.3.3.3"}
        ]
        mock_requests.get.return_value = mock_response

        proxy = {"server": "http://rotating.proxy:8080"}
        result = self.tester.test_rotation(proxy, requests_count=3, delay=0.01)

        self.assertTrue(result["success"])
        self.assertEqual(result["unique_ips"], 3)
        self.assertTrue(result["rotates"])

    @patch('proxy_tester.requests')
    def test_rotation_partial_failure(self, mock_requests):
        """Test rotation with some failed requests."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ip": "1.1.1.1"}

        # Fail on second request
        mock_requests.get.side_effect = [
            mock_response,
            Exception("Connection failed"),
            mock_response
        ]

        proxy = {"server": "http://unstable.proxy:8080"}
        result = self.tester.test_rotation(proxy, requests_count=3, delay=0.01)

        self.assertFalse(result["success"])  # Didn't complete all requests
        self.assertIn("error", result)


class TestProxySpeed(unittest.TestCase):
    """Tests for speed testing."""

    def setUp(self):
        """Set up tester."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")
        self.tester = ProxyTester(timeout=10)

    @patch('proxy_tester.requests')
    def test_speed_test_success(self, mock_requests):
        """Test successful speed test."""
        # Mock streaming response with 1MB of data
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b'x' * 8192] * 122  # ~1MB

        mock_requests.get.return_value = mock_response

        proxy = {"server": "http://fast.proxy:8080"}
        result = self.tester.test_speed(proxy, test_size="1MB")

        self.assertTrue(result["success"])
        self.assertIsNotNone(result["download_speed_mbps"])
        self.assertIn("elapsed_seconds", result)
        self.assertIn("bytes_downloaded", result)

    def test_speed_test_invalid_size(self):
        """Test speed test with invalid size."""
        proxy = {"server": "http://proxy:8080"}
        result = self.tester.test_speed(proxy, test_size="invalid")

        self.assertFalse(result["success"])
        self.assertIn("Unknown test size", result["error"])


class TestProxyFullTest(unittest.TestCase):
    """Tests for full test suite."""

    def setUp(self):
        """Set up tester."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")
        self.tester = ProxyTester(timeout=5)

    @patch.object(ProxyTester, 'test_connectivity')
    @patch.object(ProxyTester, 'get_ip_info')
    @patch.object(ProxyTester, 'test_platform_access')
    @patch.object(ProxyTester, 'test_speed')
    def test_full_test_all_pass(self, mock_speed, mock_platform, mock_ip, mock_connectivity):
        """Test full test suite with all passing."""
        mock_connectivity.return_value = {"success": True, "latency_ms": 100}
        mock_ip.return_value = {"success": True, "ip": "1.2.3.4", "geo": {"country": "US"}}
        mock_platform.return_value = {"success": True, "blocked": False}
        mock_speed.return_value = {"success": True, "download_speed_mbps": 50}

        proxy = {"server": "http://good.proxy:8080"}
        result = self.tester.full_test(proxy, platforms=["x"])

        self.assertEqual(result["summary"]["overall"], "GOOD")
        self.assertGreaterEqual(result["summary"]["passed"], 4)
        self.assertEqual(result["summary"]["failed"], 0)

    @patch.object(ProxyTester, 'test_connectivity')
    @patch.object(ProxyTester, 'get_ip_info')
    @patch.object(ProxyTester, 'test_platform_access')
    @patch.object(ProxyTester, 'test_speed')
    def test_full_test_partial_fail(self, mock_speed, mock_platform, mock_ip, mock_connectivity):
        """Test full test suite with some failures."""
        mock_connectivity.return_value = {"success": True}
        mock_ip.return_value = {"success": True, "ip": "1.2.3.4"}
        mock_platform.return_value = {"success": False, "blocked": True}
        mock_speed.return_value = {"success": False, "error": "Timeout"}

        proxy = {"server": "http://slow.proxy:8080"}
        result = self.tester.full_test(proxy, platforms=["x"])

        self.assertEqual(result["summary"]["overall"], "PARTIAL")

    @patch.object(ProxyTester, 'test_connectivity')
    @patch.object(ProxyTester, 'get_ip_info')
    @patch.object(ProxyTester, 'test_platform_access')
    @patch.object(ProxyTester, 'test_speed')
    def test_full_test_all_fail(self, mock_speed, mock_platform, mock_ip, mock_connectivity):
        """Test full test suite with all failing."""
        mock_connectivity.return_value = {"success": False}
        mock_ip.return_value = {"success": False}
        mock_platform.return_value = {"success": False}
        mock_speed.return_value = {"success": False}

        proxy = {"server": "http://bad.proxy:8080"}
        result = self.tester.full_test(proxy, platforms=["x"])

        self.assertEqual(result["summary"]["overall"], "POOR")


class TestProxyBatchTest(unittest.TestCase):
    """Tests for batch testing."""

    def setUp(self):
        """Set up tester."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")
        self.tester = ProxyTester(timeout=5)

    @patch.object(ProxyTester, 'full_test')
    def test_batch_test_sequential(self, mock_full_test):
        """Test batch testing sequentially."""
        mock_full_test.return_value = {"summary": {"overall": "GOOD"}}

        proxies = [
            {"server": "http://proxy1:8080"},
            {"server": "http://proxy2:8080"}
        ]

        results = self.tester.batch_test(proxies, parallel=False)

        self.assertEqual(len(results), 2)
        self.assertEqual(mock_full_test.call_count, 2)

    @patch.object(ProxyTester, 'full_test')
    def test_batch_test_parallel(self, mock_full_test):
        """Test batch testing in parallel."""
        mock_full_test.return_value = {"summary": {"overall": "GOOD"}}

        proxies = [
            {"server": "http://proxy1:8080"},
            {"server": "http://proxy2:8080"},
            {"server": "http://proxy3:8080"}
        ]

        results = self.tester.batch_test(proxies, parallel=True, max_workers=2)

        self.assertEqual(len(results), 3)


class TestLoadProxiesFromFile(unittest.TestCase):
    """Tests for loading proxies from file."""

    def test_load_proxies_list_format(self):
        """Test loading proxies from list format JSON."""
        if not load_proxies_from_file:
            self.skipTest("load_proxies_from_file not importable")

        # Create temp file
        temp_path = TEST_OUTPUT_DIR / "proxies_list.json"
        data = [
            {"server": "http://proxy1:8080"},
            {"server": "http://proxy2:8080"}
        ]
        with open(temp_path, 'w') as f:
            json.dump(data, f)

        proxies = load_proxies_from_file(str(temp_path))

        self.assertEqual(len(proxies), 2)

        # Clean up
        temp_path.unlink()

    def test_load_proxies_dict_format(self):
        """Test loading proxies from dict format JSON."""
        if not load_proxies_from_file:
            self.skipTest("load_proxies_from_file not importable")

        temp_path = TEST_OUTPUT_DIR / "proxies_dict.json"
        data = {
            "proxies": [
                {"server": "http://proxy1:8080"},
                {"server": "http://proxy2:8080"}
            ],
            "metadata": {}
        }
        with open(temp_path, 'w') as f:
            json.dump(data, f)

        proxies = load_proxies_from_file(str(temp_path))

        self.assertEqual(len(proxies), 2)

        # Clean up
        temp_path.unlink()


class MockProxyFixtures(unittest.TestCase):
    """Tests demonstrating mock proxy usage."""

    def test_mock_proxy_config(self):
        """Test creating mock proxy configurations."""
        mock_proxy = {
            "server": "http://mock.proxy.local:8080",
            "username": "test_user",
            "password": "test_pass"
        }

        self.assertEqual(mock_proxy["server"], "http://mock.proxy.local:8080")
        self.assertEqual(mock_proxy["username"], "test_user")

    def test_mock_soax_proxy(self):
        """Test creating mock Soax proxy configuration."""
        mock_soax = {
            "server": "http://proxy.soax.com:9000",
            "username": "user-mobile-country-US-sessionduration-30",
            "password": "soax_password"
        }

        self.assertIn("soax.com", mock_soax["server"])
        self.assertIn("mobile", mock_soax["username"])
        self.assertIn("country-US", mock_soax["username"])


def run_tests(test_type: str = "all") -> Dict[str, Any]:
    """Run tests and return results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestProxyTesterInit))
    suite.addTests(loader.loadTestsFromTestCase(TestProxyURLParsing))
    suite.addTests(loader.loadTestsFromTestCase(TestProxyConnectivity))
    suite.addTests(loader.loadTestsFromTestCase(TestProxyIPInfo))
    suite.addTests(loader.loadTestsFromTestCase(TestProxyPlatformAccess))
    suite.addTests(loader.loadTestsFromTestCase(TestProxyRotation))
    suite.addTests(loader.loadTestsFromTestCase(TestProxySpeed))
    suite.addTests(loader.loadTestsFromTestCase(TestProxyFullTest))
    suite.addTests(loader.loadTestsFromTestCase(TestProxyBatchTest))
    suite.addTests(loader.loadTestsFromTestCase(TestLoadProxiesFromFile))
    suite.addTests(loader.loadTestsFromTestCase(MockProxyFixtures))

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

    parser = argparse.ArgumentParser(description="Proxy Tester Test Suite")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--output", "-o", help="Output results to JSON file")

    args = parser.parse_args()

    results = run_tests()

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")

    sys.exit(0 if results["success"] else 1)
