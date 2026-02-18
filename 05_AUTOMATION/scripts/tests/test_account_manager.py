#!/usr/bin/env python3
"""
Account Manager Test Suite
==========================
Comprehensive tests for the AccountManager class.

Features:
- Account loading tests (JSON/CSV)
- Rate limit enforcement tests
- Proxy assignment tests
- Cooldown tracking tests
- Account status management tests

Usage:
    python -m pytest test_account_manager.py -v
    python test_account_manager.py --unit
"""

import os
import sys
import json
import csv
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

try:
    from account_manager import (
        AccountManager, Account, DEFAULT_RATE_LIMITS,
        create_sample_config
    )
except ImportError:
    AccountManager = None
    Account = None
    DEFAULT_RATE_LIMITS = {}
    create_sample_config = None

# Test output directory
TEST_OUTPUT_DIR = Path(__file__).parent / "test_output"
TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class TestAccountDataclass(unittest.TestCase):
    """Tests for Account dataclass."""

    def test_account_creation_with_defaults(self):
        """Test Account creation with minimal fields."""
        if not Account:
            self.skipTest("Account not importable")

        account = Account(
            id="test_account",
            platform="X",
            handle="@test",
            niche="AI"
        )
        self.assertEqual(account.id, "test_account")
        self.assertEqual(account.platform, "X")
        self.assertEqual(account.handle, "@test")
        self.assertEqual(account.niche, "AI")
        self.assertEqual(account.status, "active")
        self.assertEqual(account.posts_today, 0)
        self.assertEqual(account.proxy, {})

    def test_account_to_dict(self):
        """Test Account serialization to dict."""
        if not Account:
            self.skipTest("Account not importable")

        account = Account(
            id="test",
            platform="X",
            handle="@test",
            niche="AI",
            proxy={"server": "http://proxy:8080"},
            status="active"
        )
        d = account.to_dict()

        self.assertIsInstance(d, dict)
        self.assertEqual(d["id"], "test")
        self.assertEqual(d["platform"], "X")
        self.assertEqual(d["proxy"], {"server": "http://proxy:8080"})

    def test_account_from_dict(self):
        """Test Account creation from dict."""
        if not Account:
            self.skipTest("Account not importable")

        data = {
            "id": "test",
            "platform": "Instagram",
            "handle": "@insta_test",
            "niche": "Fitness",
            "proxy": {"server": "http://proxy:9000"},
            "status": "active",
            "posts_today": 3
        }
        account = Account.from_dict(data)

        self.assertEqual(account.id, "test")
        self.assertEqual(account.platform, "Instagram")
        self.assertEqual(account.posts_today, 3)

    def test_account_from_dict_ignores_extra_fields(self):
        """Test Account.from_dict ignores unknown fields."""
        if not Account:
            self.skipTest("Account not importable")

        data = {
            "id": "test",
            "platform": "X",
            "handle": "@test",
            "niche": "AI",
            "unknown_field": "should be ignored",
            "another_unknown": 123
        }
        # Should not raise
        account = Account.from_dict(data)
        self.assertEqual(account.id, "test")


class TestAccountManagerInit(unittest.TestCase):
    """Tests for AccountManager initialization."""

    def test_init_without_config(self):
        """Test manager initialization without config file."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager()
        self.assertEqual(len(manager.accounts), 0)
        self.assertIsNone(manager.config_path)

    def test_init_with_nonexistent_file(self):
        """Test manager initialization with nonexistent file."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager("/nonexistent/path/config.json")
        self.assertEqual(len(manager.accounts), 0)

    def test_init_creates_lock(self):
        """Test manager creates threading lock."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager()
        self.assertIsNotNone(manager._lock)


class TestAccountManagerLoadJSON(unittest.TestCase):
    """Tests for loading accounts from JSON."""

    def setUp(self):
        """Create test JSON files."""
        self.temp_files = []

    def tearDown(self):
        """Clean up temp files."""
        for f in self.temp_files:
            try:
                os.unlink(f)
            except:
                pass

    def _create_temp_json(self, data):
        """Create a temporary JSON file."""
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(data, f)
        f.close()
        self.temp_files.append(f.name)
        return f.name

    def test_load_json_list_format(self):
        """Test loading JSON with list of accounts."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        data = [
            {"id": "x_test", "platform": "X", "handle": "@test", "niche": "AI"},
            {"id": "ig_test", "platform": "Instagram", "handle": "@ig", "niche": "Fitness"}
        ]
        config_path = self._create_temp_json(data)

        manager = AccountManager(config_path)
        self.assertEqual(len(manager.accounts), 2)
        self.assertIn("x_test", manager.accounts)
        self.assertIn("ig_test", manager.accounts)

    def test_load_json_dict_format(self):
        """Test loading JSON with dict containing accounts key."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        data = {
            "accounts": [
                {"id": "x_test", "platform": "X", "handle": "@test", "niche": "AI"}
            ],
            "last_updated": "2024-01-01"
        }
        config_path = self._create_temp_json(data)

        manager = AccountManager(config_path)
        self.assertEqual(len(manager.accounts), 1)

    def test_load_json_with_proxy(self):
        """Test loading accounts with proxy configuration."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        data = [{
            "id": "x_test",
            "platform": "X",
            "handle": "@test",
            "niche": "AI",
            "proxy": {
                "server": "http://proxy.example.com:8080",
                "username": "user",
                "password": "pass"
            }
        }]
        config_path = self._create_temp_json(data)

        manager = AccountManager(config_path)
        account = manager.accounts["x_test"]
        self.assertEqual(account.proxy["server"], "http://proxy.example.com:8080")

    def test_load_invalid_json(self):
        """Test handling of invalid JSON."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        f = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        f.write("invalid json {{{")
        f.close()
        self.temp_files.append(f.name)

        # Should not raise, just log error
        manager = AccountManager(f.name)
        self.assertEqual(len(manager.accounts), 0)


class TestAccountManagerLoadCSV(unittest.TestCase):
    """Tests for loading accounts from CSV."""

    def setUp(self):
        """Create test CSV files."""
        self.temp_files = []

    def tearDown(self):
        """Clean up temp files."""
        for f in self.temp_files:
            try:
                os.unlink(f)
            except:
                pass

    def _create_temp_csv(self, rows, fieldnames):
        """Create a temporary CSV file."""
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='')
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        f.close()
        self.temp_files.append(f.name)
        return f.name

    def test_load_csv_format(self):
        """Test loading accounts from CSV."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        rows = [
            {"Platform": "X", "Handle": "@daily_anchor", "Niche": "Faith", "Status": "ACTIVE"},
            {"Platform": "Instagram", "Handle": "@fitness_daily", "Niche": "Fitness", "Status": "PENDING"}
        ]
        fieldnames = ["Platform", "Handle", "Niche", "Status", "ProxyUsed", "CreatedDate", "Notes"]
        config_path = self._create_temp_csv(rows, fieldnames)

        manager = AccountManager(config_path)
        self.assertEqual(len(manager.accounts), 2)

    def test_csv_generates_account_id(self):
        """Test CSV loading generates correct account IDs."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        rows = [
            {"Platform": "X", "Handle": "@test_handle", "Niche": "AI", "Status": "ACTIVE"}
        ]
        fieldnames = ["Platform", "Handle", "Niche", "Status"]
        config_path = self._create_temp_csv(rows, fieldnames)

        manager = AccountManager(config_path)
        # ID should be platform_handle (lowercase, no @)
        self.assertIn("x_test_handle", manager.accounts)

    def test_csv_proxy_parsing_url(self):
        """Test CSV proxy URL parsing."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        rows = [
            {"Platform": "X", "Handle": "@test", "Niche": "AI", "Status": "ACTIVE",
             "ProxyUsed": "http://proxy.example.com:8080"}
        ]
        fieldnames = ["Platform", "Handle", "Niche", "Status", "ProxyUsed"]
        config_path = self._create_temp_csv(rows, fieldnames)

        manager = AccountManager(config_path)
        account = manager.accounts["x_test"]
        self.assertEqual(account.proxy.get("server"), "http://proxy.example.com:8080")


class TestAccountManagerRateLimits(unittest.TestCase):
    """Tests for rate limit enforcement."""

    def test_can_post_active_account(self):
        """Test can_post returns True for active account."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager()
        account = Account(
            id="test",
            platform="X",
            handle="@test",
            niche="AI",
            status="active"
        )
        manager.accounts["test"] = account

        self.assertTrue(manager.can_post("test"))

    def test_can_post_inactive_account(self):
        """Test can_post returns False for inactive account."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager()
        account = Account(
            id="test",
            platform="X",
            handle="@test",
            niche="AI",
            status="suspended"
        )
        manager.accounts["test"] = account

        self.assertFalse(manager.can_post("test"))

    def test_can_post_daily_limit(self):
        """Test can_post respects daily post limit."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager()
        account = Account(
            id="test",
            platform="X",
            handle="@test",
            niche="AI",
            status="active",
            posts_today=DEFAULT_RATE_LIMITS["X"]["posts_per_day"],
            last_reset_date=datetime.now().date().isoformat()
        )
        manager.accounts["test"] = account

        self.assertFalse(manager.can_post("test"))

    def test_can_post_interval_limit(self):
        """Test can_post respects minimum interval."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager()
        # Last post was 5 minutes ago
        last_post = datetime.now() - timedelta(minutes=5)
        account = Account(
            id="test",
            platform="X",
            handle="@test",
            niche="AI",
            status="active",
            last_post_time=last_post.isoformat()
        )
        manager.accounts["test"] = account

        # X requires 30 min interval
        self.assertFalse(manager.can_post("test"))

    def test_can_post_after_interval(self):
        """Test can_post allows posting after interval."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager()
        # Last post was 2 hours ago
        last_post = datetime.now() - timedelta(hours=2)
        account = Account(
            id="test",
            platform="X",
            handle="@test",
            niche="AI",
            status="active",
            last_post_time=last_post.isoformat()
        )
        manager.accounts["test"] = account

        self.assertTrue(manager.can_post("test"))

    def test_daily_counter_resets(self):
        """Test daily counter resets on new day."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager()
        yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
        account = Account(
            id="test",
            platform="X",
            handle="@test",
            niche="AI",
            status="active",
            posts_today=15,
            last_reset_date=yesterday
        )
        manager.accounts["test"] = account

        # Should reset and allow posting
        self.assertTrue(manager.can_post("test"))
        self.assertEqual(account.posts_today, 0)

    def test_can_post_nonexistent_account(self):
        """Test can_post returns False for nonexistent account."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager()
        self.assertFalse(manager.can_post("nonexistent"))


class TestAccountManagerRecordPost(unittest.TestCase):
    """Tests for recording posts."""

    def test_record_post_updates_time(self):
        """Test record_post updates last_post_time."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager()
        account = Account(
            id="test",
            platform="X",
            handle="@test",
            niche="AI"
        )
        manager.accounts["test"] = account

        before = datetime.now()
        manager.record_post("test", success=True)

        self.assertIsNotNone(account.last_post_time)
        post_time = datetime.fromisoformat(account.last_post_time)
        self.assertGreaterEqual(post_time, before)

    def test_record_post_increments_counter(self):
        """Test record_post increments posts_today."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager()
        account = Account(
            id="test",
            platform="X",
            handle="@test",
            niche="AI"
        )
        manager.accounts["test"] = account

        self.assertEqual(account.posts_today, 0)
        manager.record_post("test", success=True)
        self.assertEqual(account.posts_today, 1)
        manager.record_post("test", success=True)
        self.assertEqual(account.posts_today, 2)

    def test_record_post_failed_no_increment(self):
        """Test failed posts don't increment counter."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager()
        account = Account(
            id="test",
            platform="X",
            handle="@test",
            niche="AI"
        )
        manager.accounts["test"] = account

        manager.record_post("test", success=False)
        self.assertEqual(account.posts_today, 0)


class TestAccountManagerQueries(unittest.TestCase):
    """Tests for account query methods."""

    def setUp(self):
        """Set up test accounts."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        self.manager = AccountManager()
        self.manager.accounts = {
            "x_faith": Account(id="x_faith", platform="X", handle="@faith", niche="Faith", status="active"),
            "x_ai": Account(id="x_ai", platform="X", handle="@ai", niche="AI", status="active"),
            "ig_faith": Account(id="ig_faith", platform="Instagram", handle="@faith", niche="Faith", status="active"),
            "ig_ai": Account(id="ig_ai", platform="Instagram", handle="@ai", niche="AI", status="suspended"),
        }

    def test_get_account(self):
        """Test get_account retrieves correct account."""
        account = self.manager.get_account("x_faith")
        self.assertEqual(account.handle, "@faith")

    def test_get_account_nonexistent(self):
        """Test get_account returns None for nonexistent."""
        account = self.manager.get_account("nonexistent")
        self.assertIsNone(account)

    def test_get_accounts_for_platform(self):
        """Test filtering by platform."""
        x_accounts = self.manager.get_accounts_for_platform("X")
        self.assertEqual(len(x_accounts), 2)

        ig_accounts = self.manager.get_accounts_for_platform("Instagram")
        # Only 1 active Instagram account
        self.assertEqual(len(ig_accounts), 1)

    def test_get_accounts_for_niche(self):
        """Test filtering by niche."""
        faith_accounts = self.manager.get_accounts_for_niche("Faith")
        self.assertEqual(len(faith_accounts), 2)

        ai_accounts = self.manager.get_accounts_for_niche("AI")
        # Only 1 active AI account (ig_ai is suspended)
        self.assertEqual(len(ai_accounts), 1)

    def test_get_active_accounts(self):
        """Test getting all active accounts."""
        active = self.manager.get_active_accounts()
        self.assertEqual(len(active), 3)

    def test_get_next_available(self):
        """Test getting next available account."""
        account = self.manager.get_next_available(platform="X")
        self.assertIsNotNone(account)
        self.assertEqual(account.platform, "X")

    def test_get_next_available_with_filters(self):
        """Test get_next_available with platform and niche."""
        account = self.manager.get_next_available(platform="X", niche="Faith")
        self.assertIsNotNone(account)
        self.assertEqual(account.id, "x_faith")


class TestAccountManagerStatus(unittest.TestCase):
    """Tests for account status management."""

    def test_set_account_status(self):
        """Test changing account status."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager()
        account = Account(
            id="test",
            platform="X",
            handle="@test",
            niche="AI",
            status="active"
        )
        manager.accounts["test"] = account

        manager.set_account_status("test", "suspended")
        self.assertEqual(account.status, "suspended")

    def test_add_account(self):
        """Test adding a new account."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager()
        account = Account(
            id="new_account",
            platform="TikTok",
            handle="@tiktok",
            niche="AI"
        )

        manager.add_account(account)
        self.assertIn("new_account", manager.accounts)

    def test_remove_account(self):
        """Test removing an account."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager()
        account = Account(
            id="to_remove",
            platform="X",
            handle="@remove",
            niche="AI"
        )
        manager.accounts["to_remove"] = account

        manager.remove_account("to_remove")
        self.assertNotIn("to_remove", manager.accounts)


class TestAccountManagerStats(unittest.TestCase):
    """Tests for statistics methods."""

    def test_get_stats(self):
        """Test getting account statistics."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager()
        manager.accounts = {
            "x_faith": Account(id="x_faith", platform="X", handle="@f", niche="Faith", status="active"),
            "x_ai": Account(id="x_ai", platform="X", handle="@a", niche="AI", status="active"),
            "ig_faith": Account(id="ig_faith", platform="Instagram", handle="@f", niche="Faith", status="suspended"),
        }

        stats = manager.get_stats()

        self.assertEqual(stats["total_accounts"], 3)
        self.assertEqual(stats["active_accounts"], 2)
        self.assertEqual(stats["by_platform"]["X"], 2)
        self.assertEqual(stats["by_platform"]["Instagram"], 1)
        self.assertEqual(stats["by_niche"]["Faith"], 2)
        self.assertEqual(stats["by_niche"]["AI"], 1)

    def test_get_posting_schedule(self):
        """Test getting posting schedule."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        manager = AccountManager()
        account = Account(
            id="test",
            platform="X",
            handle="@test",
            niche="AI",
            status="active"
        )
        manager.accounts["test"] = account

        schedule = manager.get_posting_schedule()

        self.assertEqual(len(schedule), 1)
        self.assertEqual(schedule[0]["account_id"], "test")
        self.assertIn("next_available", schedule[0])
        self.assertIn("can_post_now", schedule[0])


class TestAccountManagerSave(unittest.TestCase):
    """Tests for saving accounts."""

    def test_save_accounts_to_json(self):
        """Test saving accounts to JSON file."""
        if not AccountManager:
            self.skipTest("AccountManager not importable")

        output_path = TEST_OUTPUT_DIR / "test_save.json"

        manager = AccountManager()
        manager.config_path = str(output_path)
        manager.accounts = {
            "test": Account(id="test", platform="X", handle="@test", niche="AI")
        }

        manager.save_accounts()

        self.assertTrue(output_path.exists())

        with open(output_path) as f:
            data = json.load(f)

        self.assertIn("accounts", data)
        self.assertEqual(len(data["accounts"]), 1)

        # Clean up
        output_path.unlink()


class TestCreateSampleConfig(unittest.TestCase):
    """Tests for sample config creation."""

    def test_create_sample_config(self):
        """Test creating sample configuration file."""
        if not create_sample_config:
            self.skipTest("create_sample_config not importable")

        output_path = TEST_OUTPUT_DIR / "sample_config.json"

        create_sample_config(str(output_path))

        self.assertTrue(output_path.exists())

        with open(output_path) as f:
            data = json.load(f)

        self.assertIn("accounts", data)
        self.assertIn("rate_limits", data)

        # Clean up
        output_path.unlink()


def run_tests(test_type: str = "all") -> Dict[str, Any]:
    """Run tests and return results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestAccountDataclass))
    suite.addTests(loader.loadTestsFromTestCase(TestAccountManagerInit))
    suite.addTests(loader.loadTestsFromTestCase(TestAccountManagerLoadJSON))
    suite.addTests(loader.loadTestsFromTestCase(TestAccountManagerLoadCSV))
    suite.addTests(loader.loadTestsFromTestCase(TestAccountManagerRateLimits))
    suite.addTests(loader.loadTestsFromTestCase(TestAccountManagerRecordPost))
    suite.addTests(loader.loadTestsFromTestCase(TestAccountManagerQueries))
    suite.addTests(loader.loadTestsFromTestCase(TestAccountManagerStatus))
    suite.addTests(loader.loadTestsFromTestCase(TestAccountManagerStats))
    suite.addTests(loader.loadTestsFromTestCase(TestAccountManagerSave))
    suite.addTests(loader.loadTestsFromTestCase(TestCreateSampleConfig))

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

    parser = argparse.ArgumentParser(description="Account Manager Test Suite")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--output", "-o", help="Output results to JSON file")

    args = parser.parse_args()

    results = run_tests()

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")

    sys.exit(0 if results["success"] else 1)
