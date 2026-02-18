#!/usr/bin/env python3
"""
Test Twitter Scraper Setup

Validates that all components are installed and configured correctly
before running the daily scraper.

Usage:
    python3 test_twitter_setup.py
"""

import sys
from pathlib import Path

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'


def check(name, test_func):
    """Run a test and print result."""
    try:
        result = test_func()
        if result:
            print(f"  {GREEN}✓{RESET} {name}")
            return True
        else:
            print(f"  {RED}✗{RESET} {name}")
            return False
    except Exception as e:
        print(f"  {RED}✗{RESET} {name}: {e}")
        return False


def test_python_version():
    """Check Python version is 3.8+"""
    version = sys.version_info
    return version.major == 3 and version.minor >= 8


def test_playwright_installed():
    """Check if Playwright is installed"""
    try:
        import playwright
        return True
    except ImportError:
        return False


def test_requests_installed():
    """Check if requests is installed"""
    try:
        import requests
        return True
    except ImportError:
        return False


def test_bs4_installed():
    """Check if BeautifulSoup4 is installed"""
    try:
        import bs4
        return True
    except ImportError:
        return False


def test_files_exist():
    """Check if required files exist"""
    base_dir = Path(__file__).parent.parent.parent
    required_files = [
        'AUTOMATIONS/scripts/source_scrapers/twitter_scraper.py',
        'AUTOMATIONS/daily_research/twitter_scanner.py',
        'AUTOMATIONS/scripts/daily_timeline_scraper.py',
        'AUTOMATIONS/x_bookmarks/extract_alpha_from_bookmarks.py',
        'LEDGER/HIGH_SIGNAL_SOURCES.csv',
        'LEDGER/ALPHA_STAGING.csv'
    ]

    for file_path in required_files:
        full_path = base_dir / file_path
        if not full_path.exists():
            print(f"    Missing: {file_path}")
            return False

    return True


def test_chromium_installed():
    """Check if Playwright Chromium browser is installed"""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()
        return True
    except Exception:
        return False


def test_high_signal_sources():
    """Check if HIGH_SIGNAL_SOURCES.csv has X accounts"""
    base_dir = Path(__file__).parent.parent.parent
    csv_file = base_dir / 'LEDGER' / 'HIGH_SIGNAL_SOURCES.csv'

    try:
        import csv
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            x_accounts = [row for row in reader if row['platform'] == 'X']
        return len(x_accounts) > 0
    except Exception:
        return False


def test_logs_directory():
    """Check if logs directory exists"""
    base_dir = Path(__file__).parent.parent.parent
    logs_dir = base_dir / 'AUTOMATIONS' / 'logs'

    if not logs_dir.exists():
        logs_dir.mkdir(parents=True, exist_ok=True)
        print(f"    Created logs directory: {logs_dir}")

    return logs_dir.exists()


def check_proxy_config():
    """Check if proxy is configured (optional)"""
    import os
    has_soax = bool(os.getenv('SOAX_USERNAME') and os.getenv('SOAX_PASSWORD'))
    has_smartproxy = bool(os.getenv('SMARTPROXY_USERNAME') and os.getenv('SMARTPROXY_PASSWORD'))

    if has_soax or has_smartproxy:
        return f"Configured ({'Soax' if has_soax else 'Smartproxy'})"
    else:
        return "Not configured (will run without proxy)"


def main():
    print("\n" + "="*60)
    print("Twitter Scraper Setup Validation")
    print("="*60 + "\n")

    tests = [
        ("Python 3.8+", test_python_version),
        ("Playwright installed", test_playwright_installed),
        ("Requests library installed", test_requests_installed),
        ("BeautifulSoup4 installed", test_bs4_installed),
        ("Required files exist", test_files_exist),
        ("Chromium browser installed", test_chromium_installed),
        ("HIGH_SIGNAL_SOURCES.csv has X accounts", test_high_signal_sources),
        ("Logs directory exists", test_logs_directory),
    ]

    print("Core Requirements:")
    results = [check(name, func) for name, func in tests]

    print("\nOptional Configuration:")
    proxy_status = check_proxy_config()
    print(f"  Proxy: {proxy_status}")

    print("\n" + "="*60)

    if all(results):
        print(f"{GREEN}✓ All tests passed!{RESET}")
        print("\nNext steps:")
        print("  1. Run test scrape:")
        print("     python3 AUTOMATIONS/scripts/daily_timeline_scraper.py --dry-run")
        print("\n  2. If successful, run for real:")
        print("     python3 AUTOMATIONS/scripts/daily_timeline_scraper.py")
        print("\n  3. Review findings:")
        print("     open LEDGER/ALPHA_STAGING.csv")
        return 0
    else:
        print(f"{RED}✗ Some tests failed{RESET}")
        print("\nTo fix:")

        if not results[1]:  # Playwright
            print("  pip install playwright")
        if not results[2]:  # Requests
            print("  pip install requests")
        if not results[3]:  # BS4
            print("  pip install beautifulsoup4")
        if not results[5]:  # Chromium
            print("  playwright install chromium")

        return 1


if __name__ == '__main__':
    sys.exit(main())
