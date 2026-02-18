#!/usr/bin/env python3
"""
Pytest Configuration and Shared Fixtures
=========================================
Provides shared fixtures and configuration for all test modules.

Features:
- Mock browser fixture
- Mock proxy fixture
- Test data generators
- Temporary file/directory fixtures
- Playwright mock factories
- Account and session mock factories

Usage:
    # Fixtures are automatically available to all tests
    def test_example(mock_browser, mock_proxy):
        # Use fixtures in tests
        pass
"""

import os
import sys
import json
import csv
import tempfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Generator
from unittest.mock import Mock, MagicMock, patch

import pytest

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

# Test output directory
TEST_OUTPUT_DIR = Path(__file__).parent / "test_output"
TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# Configuration Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def test_output_dir() -> Path:
    """Provide test output directory path."""
    TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return TEST_OUTPUT_DIR


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Provide a temporary directory for each test."""
    return tmp_path


# ============================================================================
# Mock Browser Fixtures
# ============================================================================

@pytest.fixture
def mock_playwright():
    """Create a mock Playwright instance."""
    mock_pw = MagicMock()
    mock_browser = MagicMock()
    mock_context = MagicMock()
    mock_page = MagicMock()

    mock_pw.chromium.launch.return_value = mock_browser
    mock_browser.new_context.return_value = mock_context
    mock_context.new_page.return_value = mock_page

    # Add common page methods
    mock_page.goto = MagicMock(return_value=MagicMock(ok=True, status=200))
    mock_page.content = MagicMock(return_value="<html></html>")
    mock_page.wait_for_selector = MagicMock()
    mock_page.wait_for_timeout = MagicMock()

    return {
        "playwright": mock_pw,
        "browser": mock_browser,
        "context": mock_context,
        "page": mock_page
    }


@pytest.fixture
def mock_browser(mock_playwright):
    """Create a mock browser."""
    return mock_playwright["browser"]


@pytest.fixture
def mock_page(mock_playwright):
    """Create a mock page."""
    return mock_playwright["page"]


@pytest.fixture
def mock_context(mock_playwright):
    """Create a mock browser context."""
    return mock_playwright["context"]


@pytest.fixture
def mock_locator():
    """Create a mock locator that can be configured."""
    locator = MagicMock()
    locator.count.return_value = 1
    locator.first = locator
    locator.last = locator
    locator.wait_for = MagicMock()
    locator.click = MagicMock()
    locator.fill = MagicMock()
    locator.text_content = MagicMock(return_value="")
    locator.is_visible = MagicMock(return_value=True)
    return locator


@pytest.fixture
def logged_in_page(mock_page, mock_locator):
    """Create a mock page that appears logged in."""
    mock_locator.count.return_value = 1
    mock_page.locator.return_value = mock_locator
    mock_page.content.return_value = "<html>Logged in content</html>"
    return mock_page


@pytest.fixture
def logged_out_page(mock_page, mock_locator):
    """Create a mock page that appears logged out."""
    mock_locator.count.return_value = 0
    mock_page.locator.return_value = mock_locator
    mock_page.content.return_value = '<html><input name="username"></html>'
    return mock_page


# ============================================================================
# Mock Proxy Fixtures
# ============================================================================

@pytest.fixture
def mock_proxy() -> Dict[str, str]:
    """Create a mock proxy configuration."""
    return {
        "server": "http://mock.proxy.local:8080",
        "username": "test_user",
        "password": "test_password"
    }


@pytest.fixture
def mock_soax_proxy() -> Dict[str, str]:
    """Create a mock Soax proxy configuration."""
    return {
        "server": "http://proxy.soax.com:9000",
        "username": "user-mobile-country-US-sessionduration-30",
        "password": "soax_test_password"
    }


@pytest.fixture
def mock_rotating_proxy() -> Dict[str, str]:
    """Create a mock rotating proxy configuration."""
    return {
        "server": "http://rotating.proxy.local:8080",
        "username": "rotating_user",
        "password": "rotating_pass",
        "type": "rotating"
    }


@pytest.fixture
def proxy_list() -> List[Dict[str, str]]:
    """Create a list of mock proxy configurations."""
    return [
        {"server": "http://proxy1.local:8080", "username": "user1", "password": "pass1"},
        {"server": "http://proxy2.local:8080", "username": "user2", "password": "pass2"},
        {"server": "http://proxy3.local:8080", "username": "user3", "password": "pass3"}
    ]


# ============================================================================
# Test Data Generators
# ============================================================================

@pytest.fixture
def sample_account_data() -> Dict[str, Any]:
    """Generate sample account data."""
    return {
        "id": "x_faith_main",
        "platform": "X",
        "handle": "@daily_anchor",
        "niche": "Faith",
        "status": "active",
        "proxy": {
            "server": "http://proxy.test:8080",
            "username": "user",
            "password": "pass"
        },
        "posts_today": 0,
        "last_post_time": None,
        "last_reset_date": datetime.now().date().isoformat()
    }


@pytest.fixture
def sample_accounts_list() -> List[Dict[str, Any]]:
    """Generate list of sample accounts."""
    return [
        {"id": "x_faith", "platform": "X", "handle": "@faith", "niche": "Faith", "status": "active"},
        {"id": "x_ai", "platform": "X", "handle": "@ai", "niche": "AI", "status": "active"},
        {"id": "ig_faith", "platform": "Instagram", "handle": "@faith", "niche": "Faith", "status": "active"},
        {"id": "ig_ai", "platform": "Instagram", "handle": "@ai", "niche": "AI", "status": "suspended"},
        {"id": "tiktok_ai", "platform": "TikTok", "handle": "@ai", "niche": "AI", "status": "active"}
    ]


@pytest.fixture
def sample_queue_item() -> Dict[str, Any]:
    """Generate sample queue item data."""
    return {
        "id": "Q0001",
        "account_id": "x_faith",
        "platform": "X",
        "content": "Test content for posting",
        "status": "pending",
        "scheduled_time": None,
        "hashtags": "ai tech automation",
        "niche": "AI",
        "type": "post"
    }


@pytest.fixture
def sample_queue_list() -> List[Dict[str, Any]]:
    """Generate list of sample queue items."""
    return [
        {"ContentID": "Q0001", "Platform": "X", "Title": "Post 1", "Status": "PENDING", "Niche": "AI"},
        {"ContentID": "Q0002", "Platform": "X", "Title": "Post 2", "Status": "QUEUED", "Niche": "AI"},
        {"ContentID": "Q0003", "Platform": "Instagram", "Title": "Post 3", "Status": "POSTED", "Niche": "Faith"},
        {"ContentID": "Q0004", "Platform": "X", "Title": "Post 4", "Status": "FAILED", "Niche": "Fitness"}
    ]


@pytest.fixture
def sample_session_data() -> Dict[str, Any]:
    """Generate sample session storage data."""
    return {
        "cookies": [
            {
                "name": "auth_token",
                "value": "mock_token_value",
                "domain": ".x.com",
                "path": "/",
                "expires": (datetime.now() + timedelta(days=30)).timestamp(),
                "httpOnly": True,
                "secure": True
            },
            {
                "name": "session_id",
                "value": "mock_session_id",
                "domain": ".x.com",
                "path": "/",
                "expires": -1,
                "httpOnly": False,
                "secure": True
            }
        ],
        "origins": [
            {
                "origin": "https://x.com",
                "localStorage": [
                    {"name": "theme", "value": "dark"}
                ]
            }
        ]
    }


# ============================================================================
# File Fixtures
# ============================================================================

@pytest.fixture
def temp_json_file(tmp_path) -> Generator[Path, None, None]:
    """Create a temporary JSON file."""
    file_path = tmp_path / "test_data.json"
    yield file_path
    if file_path.exists():
        file_path.unlink()


@pytest.fixture
def temp_csv_file(tmp_path) -> Generator[Path, None, None]:
    """Create a temporary CSV file."""
    file_path = tmp_path / "test_data.csv"
    yield file_path
    if file_path.exists():
        file_path.unlink()


@pytest.fixture
def accounts_json_file(tmp_path, sample_accounts_list) -> Path:
    """Create a temporary accounts JSON file."""
    file_path = tmp_path / "accounts.json"
    with open(file_path, 'w') as f:
        json.dump(sample_accounts_list, f)
    return file_path


@pytest.fixture
def accounts_csv_file(tmp_path, sample_accounts_list) -> Path:
    """Create a temporary accounts CSV file."""
    file_path = tmp_path / "accounts.csv"
    fieldnames = ["Platform", "Handle", "Niche", "Status", "ProxyUsed"]
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for account in sample_accounts_list:
            writer.writerow({
                "Platform": account["platform"],
                "Handle": account["handle"],
                "Niche": account["niche"],
                "Status": account["status"].upper(),
                "ProxyUsed": ""
            })
    return file_path


@pytest.fixture
def queue_csv_file(tmp_path, sample_queue_list) -> Path:
    """Create a temporary queue CSV file."""
    file_path = tmp_path / "queue.csv"
    fieldnames = ["ContentID", "Platform", "Title", "Status", "Niche", "ScheduledDate"]
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in sample_queue_list:
            row = {k: item.get(k, "") for k in fieldnames}
            writer.writerow(row)
    return file_path


@pytest.fixture
def session_json_file(tmp_path, sample_session_data) -> Path:
    """Create a temporary session JSON file."""
    file_path = tmp_path / "session.json"
    with open(file_path, 'w') as f:
        json.dump(sample_session_data, f)
    return file_path


# ============================================================================
# Mock Manager Fixtures
# ============================================================================

@pytest.fixture
def mock_account_manager(sample_accounts_list):
    """Create a mock AccountManager."""
    manager = MagicMock()

    # Create mock accounts
    accounts = {}
    for acc_data in sample_accounts_list:
        mock_acc = MagicMock()
        mock_acc.id = acc_data["id"]
        mock_acc.platform = acc_data["platform"]
        mock_acc.handle = acc_data["handle"]
        mock_acc.niche = acc_data["niche"]
        mock_acc.status = acc_data["status"]
        mock_acc.proxy = {}
        mock_acc.posts_today = 0
        accounts[acc_data["id"]] = mock_acc

    manager.accounts = accounts
    manager.get_account = MagicMock(side_effect=lambda x: accounts.get(x))
    manager.get_active_accounts = MagicMock(
        return_value=[a for a in accounts.values() if a.status == "active"]
    )
    manager.can_post = MagicMock(return_value=True)
    manager.record_post = MagicMock()

    return manager


@pytest.fixture
def mock_session_manager(tmp_path):
    """Create a mock SessionManager."""
    manager = MagicMock()

    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir()

    manager.sessions_dir = sessions_dir
    manager.backups_dir = sessions_dir / "backups"
    manager.backups_dir.mkdir()

    manager.get_session_path = MagicMock(
        side_effect=lambda x: str(sessions_dir / f"{x}.json")
    )
    manager.session_exists = MagicMock(return_value=True)
    manager.load_session = MagicMock(return_value={"cookies": []})
    manager.save_session = MagicMock(return_value=True)
    manager.validate_session = MagicMock(return_value={"valid": True, "expired": False})

    return manager


# ============================================================================
# Environment Fixtures
# ============================================================================

@pytest.fixture
def env_with_credentials(monkeypatch):
    """Set up environment variables with test credentials."""
    monkeypatch.setenv("X_ACCOUNT_ID", "env_test_account")
    monkeypatch.setenv("HEADLESS", "true")
    monkeypatch.setenv("PROXY_SERVER", "http://env.proxy:8080")
    monkeypatch.setenv("PROXY_USERNAME", "env_user")
    monkeypatch.setenv("PROXY_PASSWORD", "env_pass")


@pytest.fixture
def env_integration_enabled(monkeypatch):
    """Enable integration tests via environment."""
    monkeypatch.setenv("RUN_INTEGRATION_TESTS", "true")


# ============================================================================
# Cleanup Fixtures
# ============================================================================

@pytest.fixture(autouse=True)
def cleanup_test_output():
    """Clean up test output after each test."""
    yield
    # Clean up any files created in TEST_OUTPUT_DIR during tests
    for item in TEST_OUTPUT_DIR.iterdir():
        if item.is_file() and item.suffix in ['.json', '.csv', '.log']:
            try:
                item.unlink()
            except:
                pass


# ============================================================================
# Pytest Configuration
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (deselect with '-m \"not integration\"')"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "requires_browser: marks tests that require a real browser"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on markers."""
    # Skip integration tests by default unless flag is set
    if not os.environ.get("RUN_INTEGRATION_TESTS"):
        skip_integration = pytest.mark.skip(reason="Integration tests disabled. Set RUN_INTEGRATION_TESTS=true")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)


# ============================================================================
# Report Customization
# ============================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Customize test report output."""
    outcome = yield
    rep = outcome.get_result()

    # Add extra info for failed tests
    if rep.when == "call" and rep.failed:
        rep.longrepr = f"\n{rep.longrepr}\n\nTest file: {item.fspath}\nTest function: {item.name}"
