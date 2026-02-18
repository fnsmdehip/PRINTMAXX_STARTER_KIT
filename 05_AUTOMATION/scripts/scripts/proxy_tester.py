#!/usr/bin/env python3
"""
Proxy Tester
============
Test proxy connectivity, speed, and compatibility with target platforms.

Features:
- Test proxy connectivity
- Measure latency and speed
- Check IP geolocation
- Verify platform accessibility (X, Instagram, TikTok)
- Test proxy rotation
- Batch test multiple proxies

Usage:
    from proxy_tester import ProxyTester

    tester = ProxyTester()

    # Test a single proxy
    result = tester.test_proxy({
        "server": "http://proxy.example.com:8080",
        "username": "user",
        "password": "pass"
    })

    # Test platform access
    result = tester.test_platform_access(proxy_config, "instagram")

CLI:
    python proxy_tester.py --proxy "http://user:pass@proxy.com:8080"
    python proxy_tester.py --config proxies.json --platform instagram
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse
import socket
import concurrent.futures

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    sync_playwright = None
    PlaywrightTimeout = Exception

try:
    import requests
except ImportError:
    requests = None


# Configure logging
LOG_DIR = Path(__file__).parent.parent.parent / "OPS" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "proxy_tester.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("proxy_tester")


# Test URLs
IP_CHECK_URLS = [
    "https://api.ipify.org?format=json",
    "https://ifconfig.me/ip",
    "https://icanhazip.com",
]

PLATFORM_URLS = {
    "x": "https://x.com",
    "twitter": "https://twitter.com",
    "instagram": "https://www.instagram.com",
    "tiktok": "https://www.tiktok.com",
    "youtube": "https://www.youtube.com",
    "linkedin": "https://www.linkedin.com",
}


class ProxyTester:
    """Test proxy connectivity and performance."""

    def __init__(self, timeout: int = 30):
        """
        Initialize the proxy tester.

        Args:
            timeout: Default timeout in seconds for tests
        """
        self.timeout = timeout
        self.results_cache: Dict[str, Any] = {}

        logger.info("Proxy tester initialized")

    def _parse_proxy_url(self, proxy_config: Dict[str, str]) -> Dict[str, str]:
        """Parse proxy configuration into standardized format."""
        if isinstance(proxy_config, str):
            # Parse URL format: http://user:pass@host:port
            parsed = urlparse(proxy_config)
            return {
                "server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}",
                "username": parsed.username or "",
                "password": parsed.password or ""
            }
        return proxy_config

    def _build_proxy_url(self, proxy_config: Dict[str, str]) -> str:
        """Build full proxy URL with auth."""
        config = self._parse_proxy_url(proxy_config)
        server = config.get("server", "")
        username = config.get("username", "")
        password = config.get("password", "")

        if username and password:
            # Insert auth into URL
            parsed = urlparse(server)
            return f"{parsed.scheme}://{username}:{password}@{parsed.hostname}:{parsed.port}"
        return server

    def test_connectivity(self, proxy_config: Dict[str, str]) -> Dict[str, Any]:
        """
        Test basic proxy connectivity.

        Args:
            proxy_config: Proxy configuration dict

        Returns:
            Test result with connectivity status
        """
        result = {
            "test": "connectivity",
            "success": False,
            "latency_ms": None,
            "error": None,
            "timestamp": datetime.now().isoformat()
        }

        if not requests:
            result["error"] = "requests library not installed"
            return result

        proxy_url = self._build_proxy_url(proxy_config)
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }

        for url in IP_CHECK_URLS:
            try:
                start = time.time()
                response = requests.get(
                    url,
                    proxies=proxies,
                    timeout=self.timeout,
                    verify=True
                )
                latency = (time.time() - start) * 1000

                if response.status_code == 200:
                    result["success"] = True
                    result["latency_ms"] = round(latency, 2)
                    result["test_url"] = url
                    logger.info(f"Connectivity test passed: {latency:.0f}ms")
                    break

            except requests.exceptions.ProxyError as e:
                result["error"] = f"Proxy error: {str(e)}"
            except requests.exceptions.ConnectTimeout:
                result["error"] = "Connection timeout"
            except requests.exceptions.ConnectionError as e:
                result["error"] = f"Connection error: {str(e)}"
            except Exception as e:
                result["error"] = str(e)

        return result

    def get_ip_info(self, proxy_config: Dict[str, str]) -> Dict[str, Any]:
        """
        Get IP address and geolocation info through proxy.

        Args:
            proxy_config: Proxy configuration dict

        Returns:
            IP information
        """
        result = {
            "test": "ip_info",
            "success": False,
            "ip": None,
            "geo": None,
            "error": None
        }

        if not requests:
            result["error"] = "requests library not installed"
            return result

        proxy_url = self._build_proxy_url(proxy_config)
        proxies = {"http": proxy_url, "https": proxy_url}

        # Get IP
        try:
            response = requests.get(
                "https://api.ipify.org?format=json",
                proxies=proxies,
                timeout=self.timeout
            )
            if response.status_code == 200:
                result["ip"] = response.json().get("ip")
                result["success"] = True
        except Exception as e:
            result["error"] = str(e)
            return result

        # Get geo info
        if result["ip"]:
            try:
                geo_response = requests.get(
                    f"https://ipapi.co/{result['ip']}/json/",
                    proxies=proxies,
                    timeout=self.timeout
                )
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    result["geo"] = {
                        "country": geo_data.get("country_name"),
                        "country_code": geo_data.get("country_code"),
                        "region": geo_data.get("region"),
                        "city": geo_data.get("city"),
                        "isp": geo_data.get("org"),
                        "asn": geo_data.get("asn")
                    }
            except:
                pass  # Geo info is optional

        return result

    def test_platform_access(
        self,
        proxy_config: Dict[str, str],
        platform: str
    ) -> Dict[str, Any]:
        """
        Test if proxy can access a specific platform.

        Args:
            proxy_config: Proxy configuration dict
            platform: Platform name (x, instagram, tiktok, etc.)

        Returns:
            Test result with platform accessibility status
        """
        result = {
            "test": "platform_access",
            "platform": platform,
            "success": False,
            "load_time_ms": None,
            "blocked": False,
            "error": None,
            "timestamp": datetime.now().isoformat()
        }

        platform_url = PLATFORM_URLS.get(platform.lower())
        if not platform_url:
            result["error"] = f"Unknown platform: {platform}"
            return result

        if not sync_playwright:
            result["error"] = "playwright not installed"
            return result

        config = self._parse_proxy_url(proxy_config)

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    proxy={
                        "server": config.get("server", ""),
                        "username": config.get("username", ""),
                        "password": config.get("password", "")
                    }
                )

                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                )

                page = context.new_page()

                start = time.time()
                response = page.goto(platform_url, timeout=self.timeout * 1000)
                load_time = (time.time() - start) * 1000

                result["load_time_ms"] = round(load_time, 2)
                result["status_code"] = response.status if response else None

                # Check for blocks/challenges
                page_content = page.content().lower()
                block_indicators = [
                    "blocked",
                    "access denied",
                    "captcha",
                    "verify you are human",
                    "unusual traffic",
                    "rate limited",
                    "temporarily banned"
                ]

                for indicator in block_indicators:
                    if indicator in page_content:
                        result["blocked"] = True
                        result["block_reason"] = indicator
                        break

                result["success"] = not result["blocked"] and response and response.ok

                browser.close()

                logger.info(f"Platform test {platform}: {'OK' if result['success'] else 'BLOCKED/FAILED'}")

        except PlaywrightTimeout:
            result["error"] = "Page load timeout"
        except Exception as e:
            result["error"] = str(e)

        return result

    def test_rotation(
        self,
        proxy_config: Dict[str, str],
        requests_count: int = 5,
        delay: float = 1.0
    ) -> Dict[str, Any]:
        """
        Test proxy IP rotation.

        Args:
            proxy_config: Proxy configuration dict
            requests_count: Number of requests to make
            delay: Delay between requests in seconds

        Returns:
            Rotation test results
        """
        result = {
            "test": "rotation",
            "success": False,
            "requests": requests_count,
            "unique_ips": 0,
            "ips": [],
            "rotates": False,
            "error": None
        }

        if not requests:
            result["error"] = "requests library not installed"
            return result

        proxy_url = self._build_proxy_url(proxy_config)
        proxies = {"http": proxy_url, "https": proxy_url}

        ips = []
        for i in range(requests_count):
            try:
                response = requests.get(
                    "https://api.ipify.org?format=json",
                    proxies=proxies,
                    timeout=self.timeout
                )
                if response.status_code == 200:
                    ip = response.json().get("ip")
                    ips.append(ip)
                    logger.info(f"Request {i+1}/{requests_count}: {ip}")

                time.sleep(delay)

            except Exception as e:
                result["error"] = str(e)
                break

        result["ips"] = ips
        result["unique_ips"] = len(set(ips))
        result["rotates"] = len(set(ips)) > 1
        result["success"] = len(ips) == requests_count

        return result

    def test_speed(
        self,
        proxy_config: Dict[str, str],
        test_size: str = "1MB"
    ) -> Dict[str, Any]:
        """
        Test proxy download speed.

        Args:
            proxy_config: Proxy configuration dict
            test_size: Test file size (1MB, 10MB, 100MB)

        Returns:
            Speed test results
        """
        result = {
            "test": "speed",
            "success": False,
            "download_speed_mbps": None,
            "test_size": test_size,
            "error": None
        }

        if not requests:
            result["error"] = "requests library not installed"
            return result

        # Test files from Cloudflare
        test_urls = {
            "1MB": "https://speed.cloudflare.com/__down?bytes=1000000",
            "10MB": "https://speed.cloudflare.com/__down?bytes=10000000",
            "100MB": "https://speed.cloudflare.com/__down?bytes=100000000",
        }

        url = test_urls.get(test_size)
        if not url:
            result["error"] = f"Unknown test size: {test_size}"
            return result

        proxy_url = self._build_proxy_url(proxy_config)
        proxies = {"http": proxy_url, "https": proxy_url}

        try:
            start = time.time()
            response = requests.get(
                url,
                proxies=proxies,
                timeout=self.timeout * 2,
                stream=True
            )

            total_bytes = 0
            for chunk in response.iter_content(chunk_size=8192):
                total_bytes += len(chunk)

            elapsed = time.time() - start

            # Calculate speed in Mbps
            speed_mbps = (total_bytes * 8) / (elapsed * 1000000)

            result["success"] = True
            result["download_speed_mbps"] = round(speed_mbps, 2)
            result["elapsed_seconds"] = round(elapsed, 2)
            result["bytes_downloaded"] = total_bytes

            logger.info(f"Speed test: {speed_mbps:.2f} Mbps")

        except Exception as e:
            result["error"] = str(e)

        return result

    def full_test(
        self,
        proxy_config: Dict[str, str],
        platforms: List[str] = None
    ) -> Dict[str, Any]:
        """
        Run a full suite of proxy tests.

        Args:
            proxy_config: Proxy configuration dict
            platforms: List of platforms to test (default: x, instagram)

        Returns:
            Complete test results
        """
        platforms = platforms or ["x", "instagram"]

        results = {
            "timestamp": datetime.now().isoformat(),
            "proxy_server": proxy_config.get("server", ""),
            "tests": {},
            "summary": {
                "passed": 0,
                "failed": 0,
                "overall": "unknown"
            }
        }

        # Basic connectivity
        results["tests"]["connectivity"] = self.test_connectivity(proxy_config)
        if results["tests"]["connectivity"]["success"]:
            results["summary"]["passed"] += 1
        else:
            results["summary"]["failed"] += 1

        # IP info
        results["tests"]["ip_info"] = self.get_ip_info(proxy_config)
        if results["tests"]["ip_info"]["success"]:
            results["summary"]["passed"] += 1
        else:
            results["summary"]["failed"] += 1

        # Platform access
        results["tests"]["platforms"] = {}
        for platform in platforms:
            result = self.test_platform_access(proxy_config, platform)
            results["tests"]["platforms"][platform] = result
            if result["success"]:
                results["summary"]["passed"] += 1
            else:
                results["summary"]["failed"] += 1

        # Speed test (smaller file for quick testing)
        results["tests"]["speed"] = self.test_speed(proxy_config, "1MB")
        if results["tests"]["speed"]["success"]:
            results["summary"]["passed"] += 1
        else:
            results["summary"]["failed"] += 1

        # Determine overall status
        total = results["summary"]["passed"] + results["summary"]["failed"]
        pass_rate = results["summary"]["passed"] / total if total > 0 else 0

        if pass_rate >= 0.8:
            results["summary"]["overall"] = "GOOD"
        elif pass_rate >= 0.5:
            results["summary"]["overall"] = "PARTIAL"
        else:
            results["summary"]["overall"] = "POOR"

        return results

    def batch_test(
        self,
        proxies: List[Dict[str, str]],
        parallel: bool = True,
        max_workers: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Test multiple proxies.

        Args:
            proxies: List of proxy configurations
            parallel: Run tests in parallel
            max_workers: Maximum parallel workers

        Returns:
            List of test results
        """
        results = []

        if parallel and len(proxies) > 1:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(self.full_test, proxy): proxy
                    for proxy in proxies
                }
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        proxy = futures[future]
                        results.append({
                            "proxy_server": proxy.get("server"),
                            "error": str(e)
                        })
        else:
            for proxy in proxies:
                result = self.full_test(proxy)
                results.append(result)

        return results


def load_proxies_from_file(file_path: str) -> List[Dict[str, str]]:
    """Load proxy configurations from a JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)

    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        return data.get("proxies", [])
    return []


# CLI usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Proxy Tester")
    parser.add_argument("--proxy", "-p", help="Proxy URL (http://user:pass@host:port)")
    parser.add_argument("--config", "-c", help="JSON file with proxy configurations")
    parser.add_argument("--test", choices=["connectivity", "ip", "platform", "speed", "rotation", "full"],
                        default="full", help="Test type to run")
    parser.add_argument("--platform", default="x", help="Platform to test access for")
    parser.add_argument("--platforms", nargs="+", help="Multiple platforms to test")
    parser.add_argument("--timeout", type=int, default=30, help="Test timeout in seconds")
    parser.add_argument("--output", "-o", help="Output results to JSON file")
    parser.add_argument("--parallel", action="store_true", help="Run batch tests in parallel")

    args = parser.parse_args()

    tester = ProxyTester(timeout=args.timeout)

    # Determine proxies to test
    proxies = []
    if args.proxy:
        proxies = [{"server": args.proxy}]
    elif args.config:
        proxies = load_proxies_from_file(args.config)

    if not proxies:
        print("Error: Provide --proxy or --config with proxy configuration")
        parser.print_help()
        sys.exit(1)

    # Run tests
    results = []
    platforms = args.platforms or [args.platform]

    for proxy in proxies:
        print(f"\nTesting proxy: {proxy.get('server', proxy)}")
        print("-" * 50)

        if args.test == "connectivity":
            result = tester.test_connectivity(proxy)
        elif args.test == "ip":
            result = tester.get_ip_info(proxy)
        elif args.test == "platform":
            result = tester.test_platform_access(proxy, args.platform)
        elif args.test == "speed":
            result = tester.test_speed(proxy)
        elif args.test == "rotation":
            result = tester.test_rotation(proxy)
        else:  # full
            result = tester.full_test(proxy, platforms)

        results.append(result)

        # Print summary
        if args.test == "full":
            print(f"  Overall: {result['summary']['overall']}")
            print(f"  Passed: {result['summary']['passed']}, Failed: {result['summary']['failed']}")
            if result["tests"].get("ip_info", {}).get("ip"):
                ip_info = result["tests"]["ip_info"]
                print(f"  IP: {ip_info['ip']}")
                if ip_info.get("geo"):
                    print(f"  Location: {ip_info['geo'].get('city', 'N/A')}, {ip_info['geo'].get('country', 'N/A')}")
        else:
            print(f"  Success: {result.get('success', False)}")
            if result.get("error"):
                print(f"  Error: {result['error']}")

    # Output to file if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results if len(results) > 1 else results[0], f, indent=2)
        print(f"\nResults saved to: {args.output}")
