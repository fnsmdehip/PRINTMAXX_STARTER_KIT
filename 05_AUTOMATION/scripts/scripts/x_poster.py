#!/usr/bin/env python3
"""
X/Twitter Posting Script
========================
Posts content to X/Twitter using Playwright with human-like behavior.

Features:
- Proxy support (residential/mobile)
- Session persistence
- Human-like typing delays
- Human-like mouse movement
- Rate limit handling
- Comprehensive logging

Usage:
    from x_poster import XPoster

    config = {
        "account_id": "x_faith_main",
        "proxy": {"server": "http://user:pass@proxy.com:port"},
        "session_path": "sessions/x_faith_main.json"
    }

    poster = XPoster(config)
    success = poster.post("Your content here")
"""

import os
import sys
import json
import time
import random
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
except ImportError:
    print("Error: playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)


# Configure logging
LOG_DIR = Path(__file__).parent.parent.parent / "OPS" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "x_poster.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("x_poster")


# User agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

# Viewport sizes for rotation
VIEWPORTS = [
    {"width": 1280, "height": 720},
    {"width": 1366, "height": 768},
    {"width": 1440, "height": 900},
    {"width": 1920, "height": 1080},
]


class XPoster:
    """Post content to X/Twitter with human-like behavior."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the poster with configuration.

        Args:
            config: Dictionary containing:
                - account_id: Unique identifier for this account
                - proxy: Optional proxy config {"server": "...", "username": "...", "password": "..."}
                - session_path: Path to save/load session state
                - headless: Run browser in headless mode (default: False)
                - user_agent: Custom user agent (optional, will rotate if not set)
                - viewport: Custom viewport (optional, will rotate if not set)
        """
        self.config = config
        self.account_id = config.get("account_id", "unknown")
        self.proxy = config.get("proxy")
        self.session_path = config.get("session_path")
        self.headless = config.get("headless", False)
        self.user_agent = config.get("user_agent", random.choice(USER_AGENTS))
        self.viewport = config.get("viewport", random.choice(VIEWPORTS))

        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

        logger.info(f"Initialized XPoster for account: {self.account_id}")

    def human_delay(self, min_sec: float = 0.5, max_sec: float = 2.0) -> None:
        """Wait for a random human-like duration."""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def human_type(self, page: Page, text: str, min_delay: float = 0.05, max_delay: float = 0.15) -> None:
        """
        Type text with human-like delays between keystrokes.
        Uses a normal distribution for more realistic timing.
        """
        for char in text:
            page.keyboard.type(char)
            # Normal distribution centered on average delay
            avg_delay = (min_delay + max_delay) / 2
            std_dev = (max_delay - min_delay) / 4
            delay = max(min_delay, random.gauss(avg_delay, std_dev))
            time.sleep(delay)

    def human_mouse_move(self, page: Page, x: int, y: int, steps: int = None) -> None:
        """Move mouse in human-like way with random steps."""
        if steps is None:
            steps = random.randint(5, 15)
        page.mouse.move(x, y, steps=steps)
        self.human_delay(0.1, 0.3)

    def random_scroll(self, page: Page) -> None:
        """Perform random scrolling to simulate human behavior."""
        scroll_amount = random.randint(100, 300)
        direction = random.choice([1, -1])
        page.mouse.wheel(0, scroll_amount * direction)
        self.human_delay(0.5, 1.5)

    def _start_browser(self) -> None:
        """Start browser with configured settings."""
        self._playwright = sync_playwright().start()

        launch_options = {
            "headless": self.headless,
        }

        if self.proxy:
            launch_options["proxy"] = self.proxy
            logger.info(f"Using proxy: {self.proxy.get('server', 'configured')}")

        self.browser = self._playwright.chromium.launch(**launch_options)

        # Create context with optional saved state
        context_options = {
            "user_agent": self.user_agent,
            "viewport": self.viewport,
        }

        if self.session_path and Path(self.session_path).exists():
            context_options["storage_state"] = self.session_path
            logger.info(f"Loaded session from: {self.session_path}")

        self.context = self.browser.new_context(**context_options)
        self.page = self.context.new_page()

        # Set extra headers for realism
        self.page.set_extra_http_headers({
            "Accept-Language": "en-US,en;q=0.9",
        })

        logger.info("Browser started successfully")

    def _stop_browser(self) -> None:
        """Stop browser and save session."""
        if self.context and self.session_path:
            # Ensure session directory exists
            session_dir = Path(self.session_path).parent
            session_dir.mkdir(parents=True, exist_ok=True)
            self.context.storage_state(path=self.session_path)
            logger.info(f"Session saved to: {self.session_path}")

        if self.browser:
            self.browser.close()
        if hasattr(self, '_playwright'):
            self._playwright.stop()

        logger.info("Browser stopped")

    def check_login(self) -> bool:
        """Check if already logged into X."""
        try:
            self.page.goto("https://x.com/home", wait_until="networkidle", timeout=30000)
            self.human_delay(2, 4)

            # Check for login indicators
            logged_in = self.page.locator('[data-testid="SideNav_NewTweet_Button"]').count() > 0

            if logged_in:
                logger.info("Already logged in to X")
            else:
                logger.warning("Not logged in to X")

            return logged_in
        except Exception as e:
            logger.error(f"Error checking login status: {e}")
            return False

    def post(self, content: str, media_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Post content to X/Twitter.

        Args:
            content: The text content to post
            media_path: Optional path to image/video to attach

        Returns:
            Dictionary with success status and details
        """
        result = {
            "success": False,
            "account_id": self.account_id,
            "timestamp": datetime.now().isoformat(),
            "content": content[:50] + "..." if len(content) > 50 else content,
            "error": None
        }

        try:
            self._start_browser()

            # Check login status
            if not self.check_login():
                result["error"] = "Not logged in. Please log in manually first."
                logger.error(result["error"])
                return result

            # Navigate to compose
            logger.info("Navigating to compose...")
            self.human_delay(1, 2)

            # Click compose button
            compose_button = self.page.locator('[data-testid="SideNav_NewTweet_Button"]')
            if compose_button.count() > 0:
                compose_button.click()
                self.human_delay(1, 2)
            else:
                # Try going directly to compose URL
                self.page.goto("https://x.com/compose/post", wait_until="networkidle")
                self.human_delay(2, 3)

            # Wait for compose box
            compose_box = self.page.locator('[data-testid="tweetTextarea_0"]')
            compose_box.wait_for(state="visible", timeout=10000)
            compose_box.click()
            self.human_delay(0.5, 1)

            # Type content with human-like delays
            logger.info("Typing content...")
            self.human_type(self.page, content)
            self.human_delay(1, 2)

            # Handle media upload if provided
            if media_path and Path(media_path).exists():
                logger.info(f"Uploading media: {media_path}")
                media_input = self.page.locator('input[type="file"][accept*="image"]')
                if media_input.count() > 0:
                    media_input.set_input_files(media_path)
                    self.human_delay(3, 5)  # Wait for upload

            # Random pause before posting (human behavior)
            self.human_delay(1, 3)

            # Click post button
            logger.info("Clicking post button...")
            post_button = self.page.locator('[data-testid="tweetButton"], [data-testid="tweetButtonInline"]')

            if post_button.count() == 0:
                result["error"] = "Post button not found"
                logger.error(result["error"])
                return result

            post_button.click()

            # Wait for post to complete
            self.human_delay(3, 5)

            # Verify post was successful by checking for toast/notification
            # or absence of compose modal
            success_indicators = [
                '[data-testid="toast"]',  # Success toast
            ]

            for indicator in success_indicators:
                if self.page.locator(indicator).count() > 0:
                    result["success"] = True
                    break

            # Alternative: check if compose modal closed
            if not result["success"]:
                compose_check = self.page.locator('[data-testid="tweetTextarea_0"]')
                if compose_check.count() == 0:
                    result["success"] = True

            if result["success"]:
                logger.info(f"Successfully posted content for {self.account_id}")
            else:
                result["error"] = "Could not verify post success"
                logger.warning(result["error"])

            return result

        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Error posting: {e}")
            return result

        finally:
            self._stop_browser()

    def post_thread(self, tweets: list[str]) -> Dict[str, Any]:
        """
        Post a thread (multiple connected tweets).

        Args:
            tweets: List of tweet contents

        Returns:
            Dictionary with success status and details
        """
        result = {
            "success": False,
            "account_id": self.account_id,
            "timestamp": datetime.now().isoformat(),
            "tweets_posted": 0,
            "total_tweets": len(tweets),
            "error": None
        }

        if not tweets:
            result["error"] = "No tweets provided"
            return result

        try:
            self._start_browser()

            if not self.check_login():
                result["error"] = "Not logged in"
                return result

            # Click compose
            compose_button = self.page.locator('[data-testid="SideNav_NewTweet_Button"]')
            compose_button.click()
            self.human_delay(1, 2)

            for i, tweet_content in enumerate(tweets):
                logger.info(f"Posting tweet {i+1}/{len(tweets)}")

                # Type content
                compose_box = self.page.locator('[data-testid="tweetTextarea_0"]').last
                compose_box.wait_for(state="visible", timeout=10000)
                compose_box.click()
                self.human_delay(0.5, 1)

                self.human_type(self.page, tweet_content)
                self.human_delay(1, 2)

                # Add next tweet in thread (except for last one)
                if i < len(tweets) - 1:
                    add_tweet_button = self.page.locator('[data-testid="addButton"]')
                    if add_tweet_button.count() > 0:
                        add_tweet_button.click()
                        self.human_delay(1, 2)

                result["tweets_posted"] += 1

            # Post the thread
            post_button = self.page.locator('[data-testid="tweetButton"]')
            post_button.click()

            self.human_delay(3, 5)

            result["success"] = True
            logger.info(f"Thread posted: {result['tweets_posted']} tweets")

            return result

        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Error posting thread: {e}")
            return result

        finally:
            self._stop_browser()


def load_config_from_env() -> Dict[str, Any]:
    """Load configuration from environment variables."""
    config = {
        "account_id": os.getenv("X_ACCOUNT_ID", "default"),
        "headless": os.getenv("HEADLESS", "false").lower() == "true",
    }

    # Proxy configuration
    proxy_server = os.getenv("PROXY_SERVER")
    if proxy_server:
        config["proxy"] = {"server": proxy_server}

        proxy_user = os.getenv("PROXY_USERNAME")
        proxy_pass = os.getenv("PROXY_PASSWORD")
        if proxy_user and proxy_pass:
            config["proxy"]["username"] = proxy_user
            config["proxy"]["password"] = proxy_pass

    # Session path
    session_path = os.getenv("SESSION_PATH")
    if session_path:
        config["session_path"] = session_path

    return config


def load_config_from_file(config_path: str) -> Dict[str, Any]:
    """Load configuration from JSON file."""
    with open(config_path, 'r') as f:
        return json.load(f)


# CLI usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Post to X/Twitter")
    parser.add_argument("--content", "-c", required=True, help="Content to post")
    parser.add_argument("--config", help="Path to JSON config file")
    parser.add_argument("--media", "-m", help="Path to media file to attach")
    parser.add_argument("--account-id", help="Account identifier")
    parser.add_argument("--session-path", help="Path to session file")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")

    args = parser.parse_args()

    # Build config
    if args.config:
        config = load_config_from_file(args.config)
    else:
        config = load_config_from_env()

    # Override with CLI args
    if args.account_id:
        config["account_id"] = args.account_id
    if args.session_path:
        config["session_path"] = args.session_path
    if args.headless:
        config["headless"] = True

    # Post
    poster = XPoster(config)
    result = poster.post(args.content, args.media)

    # Output result
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["success"] else 1)
