#!/usr/bin/env python3
"""
Account Manager
===============
Manages multiple social media accounts with proxy assignment and posting schedules.

Features:
- Load accounts from JSON/CSV configuration
- Assign dedicated proxies per account
- Track last post time to prevent over-posting
- Rate limit enforcement
- Account health tracking

Usage:
    from account_manager import AccountManager

    manager = AccountManager("LEDGER/social_accounts.json")
    accounts = manager.get_accounts_for_platform("X")

    for account in accounts:
        if manager.can_post(account["id"]):
            # Post content
            manager.record_post(account["id"])
"""

import os
import sys
import json
import csv
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict, field
import threading


# Configure logging
LOG_DIR = Path(__file__).parent.parent.parent / "OPS" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "account_manager.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("account_manager")


# Default rate limits per platform (posts per day)
DEFAULT_RATE_LIMITS = {
    "X": {"posts_per_day": 15, "min_interval_minutes": 30},
    "Instagram": {"posts_per_day": 5, "min_interval_minutes": 180},
    "TikTok": {"posts_per_day": 3, "min_interval_minutes": 180},
    "YouTube": {"posts_per_day": 2, "min_interval_minutes": 360},
    "LinkedIn": {"posts_per_day": 3, "min_interval_minutes": 240},
    "default": {"posts_per_day": 5, "min_interval_minutes": 60},
}


@dataclass
class Account:
    """Represents a social media account."""
    id: str
    platform: str
    handle: str
    niche: str
    proxy: Dict[str, str] = field(default_factory=dict)
    session_path: str = ""
    status: str = "active"
    created_date: str = ""
    last_post_time: Optional[str] = None
    posts_today: int = 0
    last_reset_date: Optional[str] = None
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Account":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class AccountManager:
    """Manage multiple social media accounts."""

    def __init__(self, config_path: str = None):
        """
        Initialize the account manager.

        Args:
            config_path: Path to accounts configuration (JSON or CSV)
        """
        self.accounts: Dict[str, Account] = {}
        self.config_path = config_path
        self._lock = threading.Lock()

        if config_path:
            self.load_accounts(config_path)

    def load_accounts(self, config_path: str) -> None:
        """Load accounts from configuration file."""
        path = Path(config_path)

        if not path.exists():
            logger.warning(f"Config file not found: {config_path}")
            return

        if path.suffix == ".json":
            self._load_from_json(path)
        elif path.suffix == ".csv":
            self._load_from_csv(path)
        else:
            logger.error(f"Unsupported config format: {path.suffix}")

    def _load_from_json(self, path: Path) -> None:
        """Load accounts from JSON file."""
        try:
            with open(path, 'r') as f:
                data = json.load(f)

            if isinstance(data, list):
                # List of account objects
                for acc_data in data:
                    account = Account.from_dict(acc_data)
                    self.accounts[account.id] = account
            elif isinstance(data, dict):
                # Dict with accounts key
                for acc_data in data.get("accounts", []):
                    account = Account.from_dict(acc_data)
                    self.accounts[account.id] = account

            logger.info(f"Loaded {len(self.accounts)} accounts from {path}")

        except Exception as e:
            logger.error(f"Error loading JSON config: {e}")

    def _load_from_csv(self, path: Path) -> None:
        """Load accounts from CSV file (matches LEDGER/ACCOUNTS.csv format)."""
        try:
            with open(path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Map CSV columns to Account fields
                    account_id = f"{row.get('Platform', '').lower()}_{row.get('Handle', '').replace('@', '')}"

                    account = Account(
                        id=account_id,
                        platform=row.get("Platform", ""),
                        handle=row.get("Handle", ""),
                        niche=row.get("Niche", ""),
                        proxy=self._parse_proxy(row.get("ProxyUsed", "")),
                        session_path=f"sessions/{account_id}.json",
                        status=row.get("Status", "PENDING").lower(),
                        created_date=row.get("CreatedDate", ""),
                        notes=row.get("Notes", "")
                    )
                    self.accounts[account.id] = account

            logger.info(f"Loaded {len(self.accounts)} accounts from {path}")

        except Exception as e:
            logger.error(f"Error loading CSV config: {e}")

    def _parse_proxy(self, proxy_str: str) -> Dict[str, str]:
        """Parse proxy configuration string."""
        if not proxy_str:
            return {}

        # Check for predefined proxy configs from environment
        proxy_env_key = f"{proxy_str.upper().replace('-', '_')}_PROXY"
        proxy_server = os.getenv(proxy_env_key)

        if proxy_server:
            proxy_config = {"server": proxy_server}
            proxy_user = os.getenv(f"{proxy_env_key}_USER")
            proxy_pass = os.getenv(f"{proxy_env_key}_PASS")
            if proxy_user and proxy_pass:
                proxy_config["username"] = proxy_user
                proxy_config["password"] = proxy_pass
            return proxy_config

        # If it looks like a URL, use directly
        if "://" in proxy_str:
            return {"server": proxy_str}

        return {"name": proxy_str}

    def save_accounts(self, config_path: str = None) -> None:
        """Save accounts to configuration file."""
        path = Path(config_path or self.config_path)

        if path.suffix == ".json":
            self._save_to_json(path)
        else:
            logger.error("Only JSON save is supported currently")

    def _save_to_json(self, path: Path) -> None:
        """Save accounts to JSON file."""
        with self._lock:
            data = {
                "accounts": [acc.to_dict() for acc in self.accounts.values()],
                "last_updated": datetime.now().isoformat()
            }
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved {len(self.accounts)} accounts to {path}")

    def get_account(self, account_id: str) -> Optional[Account]:
        """Get account by ID."""
        return self.accounts.get(account_id)

    def get_accounts_for_platform(self, platform: str) -> List[Account]:
        """Get all accounts for a specific platform."""
        return [
            acc for acc in self.accounts.values()
            if acc.platform.lower() == platform.lower() and acc.status == "active"
        ]

    def get_accounts_for_niche(self, niche: str) -> List[Account]:
        """Get all accounts for a specific niche."""
        return [
            acc for acc in self.accounts.values()
            if acc.niche.lower() == niche.lower() and acc.status == "active"
        ]

    def get_active_accounts(self) -> List[Account]:
        """Get all active accounts."""
        return [acc for acc in self.accounts.values() if acc.status == "active"]

    def can_post(self, account_id: str) -> bool:
        """
        Check if an account can post based on rate limits.

        Args:
            account_id: The account ID to check

        Returns:
            True if posting is allowed, False otherwise
        """
        account = self.accounts.get(account_id)
        if not account:
            logger.error(f"Account not found: {account_id}")
            return False

        if account.status != "active":
            logger.warning(f"Account {account_id} is not active (status: {account.status})")
            return False

        # Get rate limits for platform
        limits = DEFAULT_RATE_LIMITS.get(account.platform, DEFAULT_RATE_LIMITS["default"])

        # Reset daily counter if needed
        today = datetime.now().date().isoformat()
        if account.last_reset_date != today:
            account.posts_today = 0
            account.last_reset_date = today

        # Check daily limit
        if account.posts_today >= limits["posts_per_day"]:
            logger.warning(f"Account {account_id} hit daily limit ({limits['posts_per_day']})")
            return False

        # Check minimum interval
        if account.last_post_time:
            last_post = datetime.fromisoformat(account.last_post_time)
            min_interval = timedelta(minutes=limits["min_interval_minutes"])

            if datetime.now() - last_post < min_interval:
                next_allowed = last_post + min_interval
                logger.warning(f"Account {account_id} must wait until {next_allowed.isoformat()}")
                return False

        return True

    def record_post(self, account_id: str, success: bool = True) -> None:
        """
        Record a post attempt for rate limiting.

        Args:
            account_id: The account ID
            success: Whether the post was successful
        """
        with self._lock:
            account = self.accounts.get(account_id)
            if not account:
                return

            if success:
                account.last_post_time = datetime.now().isoformat()
                account.posts_today += 1
                logger.info(f"Recorded post for {account_id} (total today: {account.posts_today})")

            # Save updated state
            if self.config_path and self.config_path.endswith(".json"):
                self.save_accounts()

    def get_next_available(self, platform: str = None, niche: str = None) -> Optional[Account]:
        """
        Get the next account available for posting.

        Args:
            platform: Filter by platform (optional)
            niche: Filter by niche (optional)

        Returns:
            Account that can post, or None if all are rate-limited
        """
        candidates = self.get_active_accounts()

        if platform:
            candidates = [a for a in candidates if a.platform.lower() == platform.lower()]
        if niche:
            candidates = [a for a in candidates if a.niche.lower() == niche.lower()]

        # Sort by last post time (oldest first)
        def sort_key(acc):
            if acc.last_post_time:
                return datetime.fromisoformat(acc.last_post_time)
            return datetime.min

        candidates.sort(key=sort_key)

        for account in candidates:
            if self.can_post(account.id):
                return account

        return None

    def set_account_status(self, account_id: str, status: str) -> None:
        """Update account status."""
        with self._lock:
            account = self.accounts.get(account_id)
            if account:
                account.status = status
                logger.info(f"Account {account_id} status changed to: {status}")

                if self.config_path and self.config_path.endswith(".json"):
                    self.save_accounts()

    def add_account(self, account: Account) -> None:
        """Add a new account."""
        with self._lock:
            self.accounts[account.id] = account
            logger.info(f"Added account: {account.id}")

            if self.config_path and self.config_path.endswith(".json"):
                self.save_accounts()

    def remove_account(self, account_id: str) -> None:
        """Remove an account."""
        with self._lock:
            if account_id in self.accounts:
                del self.accounts[account_id]
                logger.info(f"Removed account: {account_id}")

                if self.config_path and self.config_path.endswith(".json"):
                    self.save_accounts()

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about all accounts."""
        stats = {
            "total_accounts": len(self.accounts),
            "active_accounts": len([a for a in self.accounts.values() if a.status == "active"]),
            "by_platform": {},
            "by_niche": {},
            "posts_today": sum(a.posts_today for a in self.accounts.values()),
        }

        for account in self.accounts.values():
            # By platform
            if account.platform not in stats["by_platform"]:
                stats["by_platform"][account.platform] = 0
            stats["by_platform"][account.platform] += 1

            # By niche
            if account.niche not in stats["by_niche"]:
                stats["by_niche"][account.niche] = 0
            stats["by_niche"][account.niche] += 1

        return stats

    def get_posting_schedule(self) -> List[Dict[str, Any]]:
        """
        Get a schedule of when each account can next post.

        Returns:
            List of accounts with their next available posting time
        """
        schedule = []

        for account in self.get_active_accounts():
            limits = DEFAULT_RATE_LIMITS.get(account.platform, DEFAULT_RATE_LIMITS["default"])
            min_interval = timedelta(minutes=limits["min_interval_minutes"])

            if account.last_post_time:
                last_post = datetime.fromisoformat(account.last_post_time)
                next_available = last_post + min_interval
            else:
                next_available = datetime.now()

            # Check daily limit
            today = datetime.now().date().isoformat()
            if account.last_reset_date == today and account.posts_today >= limits["posts_per_day"]:
                # Next available is tomorrow
                tomorrow = datetime.now().date() + timedelta(days=1)
                next_available = datetime.combine(tomorrow, datetime.min.time())

            schedule.append({
                "account_id": account.id,
                "platform": account.platform,
                "niche": account.niche,
                "next_available": next_available.isoformat(),
                "can_post_now": next_available <= datetime.now(),
                "posts_today": account.posts_today,
                "daily_limit": limits["posts_per_day"],
            })

        # Sort by next available time
        schedule.sort(key=lambda x: x["next_available"])

        return schedule


def create_sample_config(output_path: str) -> None:
    """Create a sample accounts configuration file."""
    sample = {
        "accounts": [
            {
                "id": "x_faith_main",
                "platform": "X",
                "handle": "@daily_anchor_faith",
                "niche": "Faith",
                "proxy": {
                    "server": "http://proxy.example.com:8080",
                    "username": "user",
                    "password": "pass"
                },
                "session_path": "sessions/x_faith_main.json",
                "status": "active",
                "notes": "Main faith account"
            },
            {
                "id": "ig_ai_main",
                "platform": "Instagram",
                "handle": "@aiworkflowsdaily",
                "niche": "AI",
                "proxy": {
                    "server": "http://proxy.soax.com:9000",
                    "username": "user-mobile-country-US-sessionduration-30",
                    "password": "pass"
                },
                "session_path": "sessions/ig_ai_main.json",
                "status": "active",
                "notes": "AI niche Instagram"
            }
        ],
        "rate_limits": DEFAULT_RATE_LIMITS,
        "last_updated": datetime.now().isoformat()
    }

    with open(output_path, 'w') as f:
        json.dump(sample, f, indent=2)

    print(f"Sample config created: {output_path}")


# CLI usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Account Manager")
    parser.add_argument("--config", "-c", help="Path to accounts config file")
    parser.add_argument("--list", "-l", action="store_true", help="List all accounts")
    parser.add_argument("--stats", "-s", action="store_true", help="Show account statistics")
    parser.add_argument("--schedule", action="store_true", help="Show posting schedule")
    parser.add_argument("--platform", "-p", help="Filter by platform")
    parser.add_argument("--niche", "-n", help="Filter by niche")
    parser.add_argument("--create-sample", help="Create sample config file at path")
    parser.add_argument("--check", help="Check if account can post")

    args = parser.parse_args()

    if args.create_sample:
        create_sample_config(args.create_sample)
        sys.exit(0)

    # Default config path
    config_path = args.config or "LEDGER/social_accounts.json"

    manager = AccountManager(config_path)

    if args.list:
        accounts = manager.get_active_accounts()
        if args.platform:
            accounts = [a for a in accounts if a.platform.lower() == args.platform.lower()]
        if args.niche:
            accounts = [a for a in accounts if a.niche.lower() == args.niche.lower()]

        print(f"\nAccounts ({len(accounts)}):")
        print("-" * 60)
        for acc in accounts:
            print(f"  {acc.id}: {acc.handle} ({acc.platform}/{acc.niche}) - {acc.status}")

    elif args.stats:
        stats = manager.get_stats()
        print("\nAccount Statistics:")
        print("-" * 40)
        print(f"  Total accounts: {stats['total_accounts']}")
        print(f"  Active accounts: {stats['active_accounts']}")
        print(f"  Posts today: {stats['posts_today']}")
        print(f"\n  By Platform:")
        for platform, count in stats["by_platform"].items():
            print(f"    {platform}: {count}")
        print(f"\n  By Niche:")
        for niche, count in stats["by_niche"].items():
            print(f"    {niche}: {count}")

    elif args.schedule:
        schedule = manager.get_posting_schedule()
        print("\nPosting Schedule:")
        print("-" * 70)
        for item in schedule:
            status = "READY" if item["can_post_now"] else "WAIT"
            print(f"  [{status}] {item['account_id']}: {item['next_available']} "
                  f"({item['posts_today']}/{item['daily_limit']} today)")

    elif args.check:
        can_post = manager.can_post(args.check)
        print(f"Account {args.check} can post: {can_post}")

    else:
        parser.print_help()
