#!/usr/bin/env python3
"""
Proxy Rotation Test Suite
==========================
Tests for proxy rotation, failover, and health checking.

Features:
- Proxy connectivity tests
- Rotation verification
- Geolocation checks
- Platform access tests
- Failover handling
- Pool management tests

Usage:
    python -m pytest test_proxy_rotation.py -v

CLI:
    python test_proxy_rotation.py --unit
    python test_proxy_rotation.py --live --proxy "http://user:pass@proxy.com:8080"
"""

import os
import sys
import json
import time
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

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


class TestProxyTesterUnit(unittest.TestCase):
    """Unit tests for ProxyTester class."""

    def test_init_with_default_timeout(self):
        """Test ProxyTester initialization with default timeout."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        tester = ProxyTester()
        self.assertEqual(tester.timeout, 30)

    def test_init_with_custom_timeout(self):
        """Test ProxyTester with custom timeout."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        tester = ProxyTester(timeout=60)
        self.assertEqual(tester.timeout, 60)

    def test_parse_proxy_url_string(self):
        """Test parsing proxy URL from string."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        tester = ProxyTester()
        result = tester._parse_proxy_url("http://user:pass@proxy.com:8080")

        self.assertEqual(result["server"], "http://proxy.com:8080")
        self.assertEqual(result["username"], "user")
        self.assertEqual(result["password"], "pass")

    def test_parse_proxy_url_dict(self):
        """Test parsing proxy from dict format."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        tester = ProxyTester()
        config = {
            "server": "http://proxy.com:8080",
            "username": "user",
            "password": "pass"
        }
        result = tester._parse_proxy_url(config)
        self.assertEqual(result, config)

    def test_build_proxy_url_with_auth(self):
        """Test building full proxy URL with authentication."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        tester = ProxyTester()
        config = {
            "server": "http://proxy.com:8080",
            "username": "user",
            "password": "pass"
        }
        result = tester._build_proxy_url(config)
        self.assertEqual(result, "http://user:pass@proxy.com:8080")

    def test_build_proxy_url_without_auth(self):
        """Test building proxy URL without authentication."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        tester = ProxyTester()
        config = {"server": "http://proxy.com:8080"}
        result = tester._build_proxy_url(config)
        self.assertEqual(result, "http://proxy.com:8080")


class TestProxyConnectivity(unittest.TestCase):
    """Tests for proxy connectivity checking."""

    @patch('proxy_tester.requests')
    def test_connectivity_success(self, mock_requests):
        """Test successful connectivity check."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests.get.return_value = mock_response

        tester = ProxyTester()
        result = tester.test_connectivity({"server": "http://proxy.com:8080"})

        self.assertTrue(result["success"])
        self.assertIsNotNone(result["latency_ms"])

    @patch('proxy_tester.requests')
    def test_connectivity_timeout(self, mock_requests):
        """Test connectivity timeout handling."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        mock_requests.get.side_effect = mock_requests.exceptions.ConnectTimeout()

        tester = ProxyTester()
        result = tester.test_connectivity({"server": "http://proxy.com:8080"})

        self.assertFalse(result["success"])
        self.assertIn("timeout", result["error"].lower())

    @patch('proxy_tester.requests')
    def test_connectivity_proxy_error(self, mock_requests):
        """Test proxy error handling."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        mock_requests.get.side_effect = mock_requests.exceptions.ProxyError("Connection refused")
        mock_requests.exceptions.ProxyError = Exception  # Mock the exception class

        tester = ProxyTester()
        result = tester.test_connectivity({"server": "http://proxy.com:8080"})

        self.assertFalse(result["success"])
        self.assertIsNotNone(result["error"])


class TestIPInfo(unittest.TestCase):
    """Tests for IP information retrieval."""

    @patch('proxy_tester.requests')
    def test_get_ip_info_success(self, mock_requests):
        """Test successful IP info retrieval."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        # Mock IP check
        mock_ip_response = MagicMock()
        mock_ip_response.status_code = 200
        mock_ip_response.json.return_value = {"ip": "203.0.113.1"}

        # Mock geo check
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

        tester = ProxyTester()
        result = tester.get_ip_info({"server": "http://proxy.com:8080"})

        self.assertTrue(result["success"])
        self.assertEqual(result["ip"], "203.0.113.1")
        self.assertEqual(result["geo"]["country"], "United States")
        self.assertEqual(result["geo"]["city"], "Los Angeles")

    @patch('proxy_tester.requests')
    def test_get_ip_info_geo_failure(self, mock_requests):
        """Test IP info when geo lookup fails."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        # Mock IP check success
        mock_ip_response = MagicMock()
        mock_ip_response.status_code = 200
        mock_ip_response.json.return_value = {"ip": "203.0.113.1"}

        # Mock geo check failure
        mock_geo_response = MagicMock()
        mock_geo_response.status_code = 429  # Rate limited

        mock_requests.get.side_effect = [mock_ip_response, mock_geo_response]

        tester = ProxyTester()
        result = tester.get_ip_info({"server": "http://proxy.com:8080"})

        # Should still succeed, just without geo
        self.assertTrue(result["success"])
        self.assertEqual(result["ip"], "203.0.113.1")


class TestPlatformAccess(unittest.TestCase):
    """Tests for platform access checking."""

    @patch('proxy_tester.sync_playwright')
    def test_platform_access_success(self, mock_playwright):
        """Test successful platform access."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

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
        mock_page.content.return_value = "<html>Welcome to X</html>"
        mock_response.ok = True
        mock_response.status = 200

        tester = ProxyTester()
        result = tester.test_platform_access({"server": "http://proxy.com:8080"}, "x")

        self.assertTrue(result["success"])
        self.assertFalse(result["blocked"])

    @patch('proxy_tester.sync_playwright')
    def test_platform_access_blocked(self, mock_playwright):
        """Test blocked platform access detection."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

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
        mock_page.content.return_value = "<html>Access denied - unusual traffic detected</html>"
        mock_response.ok = True
        mock_response.status = 200

        tester = ProxyTester()
        result = tester.test_platform_access({"server": "http://proxy.com:8080"}, "x")

        self.assertFalse(result["success"])
        self.assertTrue(result["blocked"])

    def test_platform_access_unknown_platform(self):
        """Test error for unknown platform."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        tester = ProxyTester()
        result = tester.test_platform_access({"server": "http://proxy.com:8080"}, "unknown_platform")

        self.assertFalse(result["success"])
        self.assertIn("Unknown platform", result["error"])


class TestProxyRotation(unittest.TestCase):
    """Tests for proxy rotation verification."""

    @patch('proxy_tester.requests')
    def test_rotation_detects_ip_change(self, mock_requests):
        """Test rotation detection when IPs change."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        # Return different IPs
        ip_responses = []
        for ip in ["203.0.113.1", "203.0.113.2", "203.0.113.3", "203.0.113.4", "203.0.113.5"]:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"ip": ip}
            ip_responses.append(mock_response)

        mock_requests.get.side_effect = ip_responses

        tester = ProxyTester()
        result = tester.test_rotation(
            {"server": "http://rotating-proxy.com:8080"},
            requests_count=5,
            delay=0.01
        )

        self.assertTrue(result["success"])
        self.assertTrue(result["rotates"])
        self.assertEqual(result["unique_ips"], 5)
        self.assertEqual(len(result["ips"]), 5)

    @patch('proxy_tester.requests')
    def test_rotation_detects_no_rotation(self, mock_requests):
        """Test detection when proxy doesn't rotate."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        # Return same IP every time
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ip": "203.0.113.1"}
        mock_requests.get.return_value = mock_response

        tester = ProxyTester()
        result = tester.test_rotation(
            {"server": "http://static-proxy.com:8080"},
            requests_count=5,
            delay=0.01
        )

        self.assertTrue(result["success"])  # Test completed
        self.assertFalse(result["rotates"])  # But no rotation
        self.assertEqual(result["unique_ips"], 1)


class TestProxySpeed(unittest.TestCase):
    """Tests for proxy speed testing."""

    @patch('proxy_tester.requests')
    def test_speed_test_success(self, mock_requests):
        """Test successful speed test."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        # Mock chunked response (1MB = 1000000 bytes)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = [b'x' * 8192 for _ in range(122)]  # ~1MB

        mock_requests.get.return_value = mock_response

        tester = ProxyTester()
        result = tester.test_speed({"server": "http://proxy.com:8080"}, "1MB")

        self.assertTrue(result["success"])
        self.assertIsNotNone(result["download_speed_mbps"])
        self.assertGreater(result["bytes_downloaded"], 0)

    def test_speed_test_invalid_size(self):
        """Test speed test with invalid size."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        tester = ProxyTester()
        result = tester.test_speed({"server": "http://proxy.com:8080"}, "invalid")

        self.assertFalse(result["success"])
        self.assertIn("Unknown test size", result["error"])


class TestFullProxyTest(unittest.TestCase):
    """Tests for full proxy test suite."""

    @patch.object(ProxyTester, 'test_connectivity')
    @patch.object(ProxyTester, 'get_ip_info')
    @patch.object(ProxyTester, 'test_platform_access')
    @patch.object(ProxyTester, 'test_speed')
    def test_full_test_aggregation(self, mock_speed, mock_platform, mock_ip, mock_conn):
        """Test full test result aggregation."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        mock_conn.return_value = {"success": True, "latency_ms": 100}
        mock_ip.return_value = {"success": True, "ip": "203.0.113.1", "geo": {}}
        mock_platform.return_value = {"success": True, "blocked": False}
        mock_speed.return_value = {"success": True, "download_speed_mbps": 50}

        tester = ProxyTester()
        result = tester.full_test({"server": "http://proxy.com:8080"}, platforms=["x"])

        self.assertIn("summary", result)
        self.assertEqual(result["summary"]["passed"], 4)  # conn, ip, platform, speed
        self.assertEqual(result["summary"]["failed"], 0)
        self.assertEqual(result["summary"]["overall"], "GOOD")

    @patch.object(ProxyTester, 'test_connectivity')
    @patch.object(ProxyTester, 'get_ip_info')
    @patch.object(ProxyTester, 'test_platform_access')
    @patch.object(ProxyTester, 'test_speed')
    def test_full_test_partial_failure(self, mock_speed, mock_platform, mock_ip, mock_conn):
        """Test full test with partial failures."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        mock_conn.return_value = {"success": True}
        mock_ip.return_value = {"success": True, "ip": "203.0.113.1"}
        mock_platform.return_value = {"success": False, "blocked": True}  # Failed
        mock_speed.return_value = {"success": False, "error": "Timeout"}  # Failed

        tester = ProxyTester()
        result = tester.full_test({"server": "http://proxy.com:8080"}, platforms=["x"])

        self.assertEqual(result["summary"]["passed"], 2)
        self.assertEqual(result["summary"]["failed"], 2)
        self.assertEqual(result["summary"]["overall"], "PARTIAL")


class TestBatchTesting(unittest.TestCase):
    """Tests for batch proxy testing."""

    @patch.object(ProxyTester, 'full_test')
    def test_batch_test_sequential(self, mock_full_test):
        """Test sequential batch testing."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        mock_full_test.return_value = {
            "summary": {"passed": 4, "failed": 0, "overall": "GOOD"}
        }

        proxies = [
            {"server": "http://proxy1.com:8080"},
            {"server": "http://proxy2.com:8080"},
            {"server": "http://proxy3.com:8080"},
        ]

        tester = ProxyTester()
        results = tester.batch_test(proxies, parallel=False)

        self.assertEqual(len(results), 3)
        self.assertEqual(mock_full_test.call_count, 3)

    @patch.object(ProxyTester, 'full_test')
    def test_batch_test_parallel(self, mock_full_test):
        """Test parallel batch testing."""
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        mock_full_test.return_value = {
            "summary": {"passed": 4, "failed": 0, "overall": "GOOD"}
        }

        proxies = [
            {"server": "http://proxy1.com:8080"},
            {"server": "http://proxy2.com:8080"},
            {"server": "http://proxy3.com:8080"},
        ]

        tester = ProxyTester()
        results = tester.batch_test(proxies, parallel=True, max_workers=3)

        self.assertEqual(len(results), 3)


class TestProxyFileLoading(unittest.TestCase):
    """Tests for loading proxies from files."""

    def test_load_proxies_list_format(self):
        """Test loading proxies from list format JSON."""
        if not load_proxies_from_file:
            self.skipTest("load_proxies_from_file not importable")

        # Create test file
        test_file = TEST_OUTPUT_DIR / "test_proxies_list.json"
        proxies = [
            {"server": "http://proxy1.com:8080"},
            {"server": "http://proxy2.com:8080"},
        ]

        with open(test_file, 'w') as f:
            json.dump(proxies, f)

        try:
            loaded = load_proxies_from_file(str(test_file))
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded[0]["server"], "http://proxy1.com:8080")
        finally:
            test_file.unlink(missing_ok=True)

    def test_load_proxies_object_format(self):
        """Test loading proxies from object format JSON."""
        if not load_proxies_from_file:
            self.skipTest("load_proxies_from_file not importable")

        # Create test file
        test_file = TEST_OUTPUT_DIR / "test_proxies_obj.json"
        data = {
            "proxies": [
                {"server": "http://proxy1.com:8080"},
                {"server": "http://proxy2.com:8080"},
            ]
        }

        with open(test_file, 'w') as f:
            json.dump(data, f)

        try:
            loaded = load_proxies_from_file(str(test_file))
            self.assertEqual(len(loaded), 2)
        finally:
            test_file.unlink(missing_ok=True)


class TestLiveProxy(unittest.TestCase):
    """Live proxy tests - require actual proxy."""

    @classmethod
    def setUpClass(cls):
        """Check if live tests should run."""
        cls.run_live = os.environ.get("RUN_LIVE_PROXY_TESTS", "").lower() == "true"
        cls.proxy_url = os.environ.get("TEST_PROXY_URL")

    def test_live_connectivity(self):
        """Test live proxy connectivity."""
        if not self.run_live or not self.proxy_url:
            self.skipTest("Live proxy tests disabled or no proxy URL")
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        tester = ProxyTester(timeout=30)
        result = tester.test_connectivity({"server": self.proxy_url})

        print(f"\nConnectivity test: {'PASS' if result['success'] else 'FAIL'}")
        if result["latency_ms"]:
            print(f"Latency: {result['latency_ms']}ms")
        if result["error"]:
            print(f"Error: {result['error']}")

        self.assertTrue(result["success"])

    def test_live_ip_info(self):
        """Test live proxy IP info."""
        if not self.run_live or not self.proxy_url:
            self.skipTest("Live proxy tests disabled")
        if not ProxyTester:
            self.skipTest("ProxyTester not importable")

        tester = ProxyTester(timeout=30)
        result = tester.get_ip_info({"server": self.proxy_url})

        print(f"\nIP Info test: {'PASS' if result['success'] else 'FAIL'}")
        if result["ip"]:
            print(f"IP: {result['ip']}")
        if result.get("geo"):
            print(f"Location: {result['geo'].get('city', 'N/A')}, {result['geo'].get('country', 'N/A')}")

        self.assertTrue(result["success"])


def run_tests(test_type: str = "all") -> Dict[str, Any]:
    """
    Run tests and return results.

    Args:
        test_type: 'unit', 'live', or 'all'

    Returns:
        Test results summary
    """
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    if test_type in ("unit", "all"):
        suite.addTests(loader.loadTestsFromTestCase(TestProxyTesterUnit))
        suite.addTests(loader.loadTestsFromTestCase(TestProxyConnectivity))
        suite.addTests(loader.loadTestsFromTestCase(TestIPInfo))
        suite.addTests(loader.loadTestsFromTestCase(TestPlatformAccess))
        suite.addTests(loader.loadTestsFromTestCase(TestProxyRotation))
        suite.addTests(loader.loadTestsFromTestCase(TestProxySpeed))
        suite.addTests(loader.loadTestsFromTestCase(TestFullProxyTest))
        suite.addTests(loader.loadTestsFromTestCase(TestBatchTesting))
        suite.addTests(loader.loadTestsFromTestCase(TestProxyFileLoading))

    if test_type in ("live", "all"):
        suite.addTests(loader.loadTestsFromTestCase(TestLiveProxy))

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

    parser = argparse.ArgumentParser(description="Proxy Rotation Test Suite")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--live", action="store_true", help="Run live proxy tests")
    parser.add_argument("--proxy", help="Proxy URL for live tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--output", "-o", help="Output results to JSON file")

    args = parser.parse_args()

    if args.live:
        os.environ["RUN_LIVE_PROXY_TESTS"] = "true"
        if args.proxy:
            os.environ["TEST_PROXY_URL"] = args.proxy
        test_type = "live"
    elif args.unit:
        test_type = "unit"
    else:
        test_type = "all"

    results = run_tests(test_type)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")

    sys.exit(0 if results["success"] else 1)
