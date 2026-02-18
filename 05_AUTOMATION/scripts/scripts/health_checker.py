#!/usr/bin/env python3
"""
Account Health Checker
======================
Check the health and status of social media accounts.

Features:
- Verify login status
- Check for account restrictions/bans
- Detect shadowbans
- Monitor engagement metrics
- Track account warnings
- Generate health reports

Usage:
    from health_checker import HealthChecker

    checker = HealthChecker()

    # Check single account
    health = checker.check_account("x_faith_main")

    # Check all accounts
    report = checker.check_all_accounts()

CLI:
    python health_checker.py --account x_faith_main
    python health_checker.py --all --platform X
    python health_checker.py --report
"""

import os
import sys
import json
import time
import random
import logging
import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional

try:
    from playwright.sync_api import sync_playwright, Page, TimeoutError as PlaywrightTimeout
except ImportError:
    sync_playwright = None
    PlaywrightTimeout = Exception

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from account_manager import AccountManager, Account
    from session_manager import SessionManager
except ImportError:
    AccountManager = None
    SessionManager = None


# Configure logging
LOG_DIR = Path(__file__).parent.parent.parent / "OPS" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "health_checker.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("health_checker")


# Default paths
LEDGER_DIR = Path(__file__).parent.parent.parent / "LEDGER"
HEALTH_LOG_PATH = LEDGER_DIR / "account_health_log.csv"
ACCOUNTS_CONFIG_PATH = LEDGER_DIR / "social_accounts.json"


# Health status levels
class HealthStatus:
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    BANNED = "banned"
    UNKNOWN = "unknown"


class HealthChecker:
    """Check health of social media accounts."""

    def __init__(
        self,
        accounts_path: str = None,
        sessions_dir: str = None
    ):
        """
        Initialize the health checker.

        Args:
            accounts_path: Path to accounts configuration
            sessions_dir: Path to sessions directory
        """
        self.accounts_path = accounts_path or str(ACCOUNTS_CONFIG_PATH)
        self.sessions_dir = sessions_dir

        # Initialize account and session managers
        self.account_manager = AccountManager(self.accounts_path) if AccountManager else None
        self.session_manager = SessionManager(self.sessions_dir) if SessionManager else None

        # Initialize health log
        self._init_health_log()

        logger.info("Health checker initialized")

    def _init_health_log(self) -> None:
        """Initialize health log CSV if it doesn't exist."""
        if not HEALTH_LOG_PATH.exists():
            HEALTH_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(HEALTH_LOG_PATH, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "account_id", "platform", "status",
                    "login_ok", "restricted", "shadowban", "warnings", "notes"
                ])

    def _log_health_check(self, result: Dict[str, Any]) -> None:
        """Log health check result to CSV."""
        try:
            with open(HEALTH_LOG_PATH, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    result.get("timestamp", datetime.now().isoformat()),
                    result.get("account_id", ""),
                    result.get("platform", ""),
                    result.get("status", HealthStatus.UNKNOWN),
                    result.get("login_ok", False),
                    result.get("restricted", False),
                    result.get("shadowban", False),
                    "|".join(result.get("warnings", [])),
                    result.get("notes", "")
                ])
        except Exception as e:
            logger.error(f"Error logging health check: {e}")

    def check_account(
        self,
        account_id: str,
        use_session: bool = True
    ) -> Dict[str, Any]:
        """
        Check the health of a specific account.

        Args:
            account_id: The account identifier
            use_session: Use saved session for checking

        Returns:
            Health check result
        """
        result = {
            "account_id": account_id,
            "timestamp": datetime.now().isoformat(),
            "platform": "unknown",
            "status": HealthStatus.UNKNOWN,
            "login_ok": False,
            "restricted": False,
            "shadowban": False,
            "warnings": [],
            "metrics": {},
            "notes": "",
            "error": None
        }

        # Get account info
        account = None
        if self.account_manager:
            account = self.account_manager.get_account(account_id)

        if account:
            result["platform"] = account.platform
        else:
            # Try to determine platform from account_id
            if account_id.startswith("x_"):
                result["platform"] = "X"
            elif account_id.startswith("ig_"):
                result["platform"] = "Instagram"
            elif account_id.startswith("tiktok_"):
                result["platform"] = "TikTok"

        # Route to platform-specific checker
        platform = result["platform"].lower()

        if platform == "x":
            result = self._check_x_account(account, result, use_session)
        elif platform == "instagram":
            result = self._check_instagram_account(account, result, use_session)
        elif platform == "tiktok":
            result = self._check_tiktok_account(account, result, use_session)
        else:
            result["error"] = f"Unknown platform: {platform}"
            result["status"] = HealthStatus.UNKNOWN

        # Determine overall status
        if not result.get("error"):
            result["status"] = self._determine_status(result)

        # Log the check
        self._log_health_check(result)

        return result

    def _determine_status(self, result: Dict[str, Any]) -> str:
        """Determine overall health status from check results."""
        if result.get("restricted"):
            return HealthStatus.BANNED

        if result.get("shadowban"):
            return HealthStatus.WARNING

        if not result.get("login_ok"):
            return HealthStatus.CRITICAL

        if result.get("warnings"):
            return HealthStatus.WARNING

        return HealthStatus.HEALTHY

    def _check_x_account(
        self,
        account: Optional[Account],
        result: Dict[str, Any],
        use_session: bool
    ) -> Dict[str, Any]:
        """Check X/Twitter account health."""
        if not sync_playwright:
            result["error"] = "playwright not installed"
            return result

        account_id = result["account_id"]
        session_path = None

        if use_session and self.session_manager:
            session_path = self.session_manager.get_session_path(account_id)
            if not Path(session_path).exists():
                session_path = None

        proxy = None
        if account and account.proxy:
            proxy = account.proxy

        try:
            with sync_playwright() as p:
                launch_opts = {"headless": True}
                if proxy:
                    launch_opts["proxy"] = proxy

                browser = p.chromium.launch(**launch_opts)

                context_opts = {}
                if session_path:
                    context_opts["storage_state"] = session_path

                context = browser.new_context(**context_opts)
                page = context.new_page()

                # Check login status
                page.goto("https://x.com/home", timeout=30000)
                time.sleep(random.uniform(3, 5))

                # Check for login
                logged_in = page.locator('[data-testid="SideNav_NewTweet_Button"]').count() > 0
                result["login_ok"] = logged_in

                if not logged_in:
                    result["warnings"].append("Not logged in")
                    browser.close()
                    return result

                # Check for account restrictions
                content = page.content().lower()
                restriction_indicators = [
                    "your account is suspended",
                    "your account has been locked",
                    "temporarily restricted",
                    "unusual activity",
                    "verify your identity"
                ]

                for indicator in restriction_indicators:
                    if indicator in content:
                        result["restricted"] = True
                        result["warnings"].append(f"Restriction detected: {indicator}")

                # Check for shadowban using profile
                if account and account.handle:
                    handle = account.handle.replace("@", "")
                    page.goto(f"https://x.com/{handle}", timeout=30000)
                    time.sleep(random.uniform(2, 4))

                    profile_content = page.content().lower()

                    # Shadowban indicators
                    if "account doesn't exist" in profile_content:
                        result["shadowban"] = True
                        result["warnings"].append("Profile not found (possible shadowban)")
                    elif "this account is suspended" in profile_content:
                        result["restricted"] = True
                        result["warnings"].append("Account suspended")

                    # Try to get metrics
                    try:
                        followers_elem = page.locator('[href*="/verified_followers"], [href*="/followers"]').first
                        if followers_elem.count() > 0:
                            followers_text = followers_elem.text_content()
                            result["metrics"]["followers_text"] = followers_text
                    except:
                        pass

                browser.close()

        except PlaywrightTimeout:
            result["error"] = "Page load timeout"
        except Exception as e:
            result["error"] = str(e)

        return result

    def _check_instagram_account(
        self,
        account: Optional[Account],
        result: Dict[str, Any],
        use_session: bool
    ) -> Dict[str, Any]:
        """Check Instagram account health."""
        if not sync_playwright:
            result["error"] = "playwright not installed"
            return result

        account_id = result["account_id"]
        session_path = None

        if use_session and self.session_manager:
            session_path = self.session_manager.get_session_path(account_id)
            if not Path(session_path).exists():
                session_path = None

        proxy = None
        if account and account.proxy:
            proxy = account.proxy

        try:
            with sync_playwright() as p:
                launch_opts = {"headless": True}
                if proxy:
                    launch_opts["proxy"] = proxy

                browser = p.chromium.launch(**launch_opts)

                # Use mobile emulation for Instagram
                context_opts = {
                    "viewport": {"width": 390, "height": 844},
                    "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15",
                    "is_mobile": True,
                    "has_touch": True,
                }
                if session_path:
                    context_opts["storage_state"] = session_path

                context = browser.new_context(**context_opts)
                page = context.new_page()

                # Check login status
                page.goto("https://www.instagram.com/", timeout=30000)
                time.sleep(random.uniform(3, 5))

                content = page.content().lower()

                # Check for login
                logged_in_indicators = [
                    'aria-label="home"',
                    'svg[aria-label="home"]',
                    'aria-label="new post"',
                ]

                for indicator in logged_in_indicators:
                    if page.locator(indicator).count() > 0:
                        result["login_ok"] = True
                        break

                # Also check if login form is present (means not logged in)
                if 'name="username"' in content:
                    result["login_ok"] = False
                    result["warnings"].append("Not logged in")

                # Check for restrictions
                restriction_indicators = [
                    "your account has been disabled",
                    "we've disabled your account",
                    "action blocked",
                    "try again later",
                    "unusual activity",
                    "confirm your identity"
                ]

                for indicator in restriction_indicators:
                    if indicator in content:
                        result["restricted"] = True
                        result["warnings"].append(f"Restriction: {indicator}")

                # Check profile if logged in
                if result["login_ok"] and account and account.handle:
                    handle = account.handle.replace("@", "")
                    page.goto(f"https://www.instagram.com/{handle}/", timeout=30000)
                    time.sleep(random.uniform(2, 4))

                    profile_content = page.content().lower()

                    if "page isn't available" in profile_content:
                        result["warnings"].append("Profile not accessible")
                    elif "user not found" in profile_content:
                        result["shadowban"] = True
                        result["warnings"].append("Profile not found")

                browser.close()

        except PlaywrightTimeout:
            result["error"] = "Page load timeout"
        except Exception as e:
            result["error"] = str(e)

        return result

    def _check_tiktok_account(
        self,
        account: Optional[Account],
        result: Dict[str, Any],
        use_session: bool
    ) -> Dict[str, Any]:
        """Check TikTok account health."""
        if not sync_playwright:
            result["error"] = "playwright not installed"
            return result

        account_id = result["account_id"]
        session_path = None

        if use_session and self.session_manager:
            session_path = self.session_manager.get_session_path(account_id)
            if not Path(session_path).exists():
                session_path = None

        proxy = None
        if account and account.proxy:
            proxy = account.proxy

        try:
            with sync_playwright() as p:
                launch_opts = {"headless": True}
                if proxy:
                    launch_opts["proxy"] = proxy

                browser = p.chromium.launch(**launch_opts)

                context_opts = {}
                if session_path:
                    context_opts["storage_state"] = session_path

                context = browser.new_context(**context_opts)
                page = context.new_page()

                # Check main page
                page.goto("https://www.tiktok.com/", timeout=30000)
                time.sleep(random.uniform(3, 5))

                content = page.content().lower()

                # Check for login (TikTok is tricky)
                login_indicators = [
                    'data-e2e="profile-icon"',
                    '"isLogin":true',
                ]

                for indicator in login_indicators:
                    if indicator in content or page.locator(f'[{indicator}]').count() > 0:
                        result["login_ok"] = True
                        break

                # Check for restrictions
                restriction_indicators = [
                    "account banned",
                    "your account has been permanently banned",
                    "temporarily suspended",
                    "violates our community guidelines"
                ]

                for indicator in restriction_indicators:
                    if indicator in content:
                        result["restricted"] = True
                        result["warnings"].append(f"Restriction: {indicator}")

                # Check profile
                if account and account.handle:
                    handle = account.handle.replace("@", "")
                    page.goto(f"https://www.tiktok.com/@{handle}", timeout=30000)
                    time.sleep(random.uniform(2, 4))

                    profile_content = page.content().lower()

                    if "couldn't find this account" in profile_content:
                        result["warnings"].append("Profile not found")
                    elif "account banned" in profile_content:
                        result["restricted"] = True

                browser.close()

        except PlaywrightTimeout:
            result["error"] = "Page load timeout"
        except Exception as e:
            result["error"] = str(e)

        return result

    def check_all_accounts(
        self,
        platform: str = None,
        niche: str = None
    ) -> List[Dict[str, Any]]:
        """
        Check health of all accounts.

        Args:
            platform: Filter by platform (optional)
            niche: Filter by niche (optional)

        Returns:
            List of health check results
        """
        results = []

        if not self.account_manager:
            logger.error("Account manager not available")
            return results

        accounts = self.account_manager.get_active_accounts()

        if platform:
            accounts = [a for a in accounts if a.platform.lower() == platform.lower()]
        if niche:
            accounts = [a for a in accounts if a.niche.lower() == niche.lower()]

        logger.info(f"Checking {len(accounts)} accounts")

        for account in accounts:
            logger.info(f"Checking account: {account.id}")
            result = self.check_account(account.id)
            results.append(result)

            # Small delay between checks to avoid detection
            time.sleep(random.uniform(5, 15))

        return results

    def generate_report(self, results: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate a health report from results or recent logs.

        Args:
            results: Optional list of health check results

        Returns:
            Health report summary
        """
        if results is None:
            results = self._load_recent_checks()

        report = {
            "generated_at": datetime.now().isoformat(),
            "total_accounts": len(results),
            "summary": {
                HealthStatus.HEALTHY: 0,
                HealthStatus.WARNING: 0,
                HealthStatus.CRITICAL: 0,
                HealthStatus.BANNED: 0,
                HealthStatus.UNKNOWN: 0
            },
            "by_platform": {},
            "issues": [],
            "recommendations": []
        }

        for result in results:
            # Count by status
            status = result.get("status", HealthStatus.UNKNOWN)
            if status in report["summary"]:
                report["summary"][status] += 1

            # Count by platform
            platform = result.get("platform", "unknown")
            if platform not in report["by_platform"]:
                report["by_platform"][platform] = {
                    "total": 0,
                    "healthy": 0,
                    "issues": 0
                }
            report["by_platform"][platform]["total"] += 1
            if status == HealthStatus.HEALTHY:
                report["by_platform"][platform]["healthy"] += 1
            elif status in (HealthStatus.WARNING, HealthStatus.CRITICAL, HealthStatus.BANNED):
                report["by_platform"][platform]["issues"] += 1

            # Collect issues
            if result.get("warnings"):
                for warning in result["warnings"]:
                    report["issues"].append({
                        "account_id": result.get("account_id"),
                        "platform": platform,
                        "issue": warning,
                        "status": status
                    })

        # Generate recommendations
        if report["summary"][HealthStatus.BANNED] > 0:
            report["recommendations"].append(
                "Some accounts are banned. Stop all automation on these accounts."
            )

        if report["summary"][HealthStatus.CRITICAL] > 0:
            report["recommendations"].append(
                "Critical issues detected. Check login credentials and session validity."
            )

        if report["summary"][HealthStatus.WARNING] > 0:
            report["recommendations"].append(
                "Warnings detected. Consider reducing automation frequency."
            )

        return report

    def _load_recent_checks(self, days: int = 1) -> List[Dict[str, Any]]:
        """Load recent health checks from log file."""
        results = []
        cutoff = datetime.now() - timedelta(days=days)

        if not HEALTH_LOG_PATH.exists():
            return results

        try:
            with open(HEALTH_LOG_PATH, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    timestamp = datetime.fromisoformat(row.get("timestamp", ""))
                    if timestamp >= cutoff:
                        results.append({
                            "account_id": row.get("account_id"),
                            "platform": row.get("platform"),
                            "status": row.get("status"),
                            "login_ok": row.get("login_ok") == "True",
                            "restricted": row.get("restricted") == "True",
                            "shadowban": row.get("shadowban") == "True",
                            "warnings": row.get("warnings", "").split("|") if row.get("warnings") else [],
                            "timestamp": row.get("timestamp")
                        })
        except Exception as e:
            logger.error(f"Error loading recent checks: {e}")

        return results

    def quick_status(self) -> Dict[str, Any]:
        """Get a quick status overview without running new checks."""
        results = self._load_recent_checks(days=1)

        if not results:
            return {
                "status": "unknown",
                "message": "No recent health checks found. Run a full check."
            }

        # Get most recent status per account
        latest = {}
        for result in results:
            account_id = result.get("account_id")
            if account_id not in latest:
                latest[account_id] = result

        healthy = sum(1 for r in latest.values() if r.get("status") == HealthStatus.HEALTHY)
        total = len(latest)

        return {
            "status": "ok" if healthy == total else "issues",
            "total_accounts": total,
            "healthy": healthy,
            "with_issues": total - healthy,
            "last_check": max(r.get("timestamp") for r in results) if results else None
        }


# CLI usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Account Health Checker")
    parser.add_argument("--account", "-a", help="Check specific account")
    parser.add_argument("--all", action="store_true", help="Check all accounts")
    parser.add_argument("--platform", "-p", help="Filter by platform")
    parser.add_argument("--niche", "-n", help="Filter by niche")
    parser.add_argument("--report", action="store_true", help="Generate health report")
    parser.add_argument("--status", action="store_true", help="Quick status check")
    parser.add_argument("--no-session", action="store_true", help="Don't use saved sessions")
    parser.add_argument("--output", "-o", help="Output results to JSON file")

    args = parser.parse_args()

    checker = HealthChecker()

    if args.account:
        result = checker.check_account(args.account, use_session=not args.no_session)
        print(f"\nHealth Check: {args.account}")
        print("-" * 50)
        print(f"  Status: {result['status']}")
        print(f"  Platform: {result['platform']}")
        print(f"  Login OK: {result['login_ok']}")
        print(f"  Restricted: {result['restricted']}")
        print(f"  Shadowban: {result['shadowban']}")
        if result.get("warnings"):
            print(f"  Warnings:")
            for w in result["warnings"]:
                print(f"    - {w}")
        if result.get("error"):
            print(f"  Error: {result['error']}")

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)

    elif args.all:
        results = checker.check_all_accounts(platform=args.platform, niche=args.niche)
        print(f"\nChecked {len(results)} accounts")
        print("-" * 50)
        for r in results:
            status_icon = {
                HealthStatus.HEALTHY: "+",
                HealthStatus.WARNING: "!",
                HealthStatus.CRITICAL: "X",
                HealthStatus.BANNED: "#",
                HealthStatus.UNKNOWN: "?"
            }.get(r.get("status"), "?")
            print(f"  [{status_icon}] {r['account_id']}: {r['status']}")

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)

    elif args.report:
        report = checker.generate_report()
        print("\nHealth Report")
        print("=" * 50)
        print(f"Generated: {report['generated_at']}")
        print(f"Total Accounts: {report['total_accounts']}")
        print("\nSummary:")
        for status, count in report["summary"].items():
            if count > 0:
                print(f"  {status}: {count}")
        print("\nBy Platform:")
        for platform, stats in report["by_platform"].items():
            print(f"  {platform}: {stats['healthy']}/{stats['total']} healthy")
        if report["issues"]:
            print("\nIssues:")
            for issue in report["issues"][:10]:
                print(f"  - {issue['account_id']}: {issue['issue']}")
        if report["recommendations"]:
            print("\nRecommendations:")
            for rec in report["recommendations"]:
                print(f"  * {rec}")

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(report, f, indent=2)

    elif args.status:
        status = checker.quick_status()
        print(f"\nQuick Status: {status['status'].upper()}")
        print(f"  Total accounts: {status.get('total_accounts', 'N/A')}")
        print(f"  Healthy: {status.get('healthy', 'N/A')}")
        print(f"  With issues: {status.get('with_issues', 'N/A')}")
        print(f"  Last check: {status.get('last_check', 'N/A')}")

    else:
        parser.print_help()
