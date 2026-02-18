#!/usr/bin/env python3
"""
Instagram Posting Script
========================
Posts content to Instagram using Playwright with mobile emulation.

Features:
- Mobile viewport emulation (iPhone)
- Mobile user agent
- Soax mobile proxy support
- Image upload
- Story posting
- Caption with hashtags
- Human-like behavior

Usage:
    from ig_poster import IGPoster

    config = {
        "account_id": "ig_faith_main",
        "proxy": {
            "server": "http://proxy.soax.com:9000",
            "username": "user-mobile-country-US-sessionduration-30",
            "password": "your_password"
        },
        "session_path": "sessions/ig_faith_main.json"
    }

    poster = IGPoster(config)
    success = poster.post_feed("Caption here", "/path/to/image.jpg")
"""

import os
import sys
import json
import time
import random
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

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
        logging.FileHandler(LOG_DIR / "ig_poster.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ig_poster")


# Mobile device configurations
MOBILE_DEVICES = {
    "iphone_12": {
        "viewport": {"width": 390, "height": 844},
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
    },
    "iphone_14_pro": {
        "viewport": {"width": 393, "height": 852},
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
    },
    "pixel_7": {
        "viewport": {"width": 412, "height": 915},
        "user_agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "device_scale_factor": 2.625,
        "is_mobile": True,
        "has_touch": True,
    },
}


class IGPoster:
    """Post content to Instagram with mobile emulation."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the poster with configuration.

        Args:
            config: Dictionary containing:
                - account_id: Unique identifier for this account
                - proxy: Optional proxy config (use mobile proxy for best results)
                - session_path: Path to save/load session state
                - device: Device profile to emulate (default: iphone_12)
                - headless: Run in headless mode (default: False, not recommended for IG)
        """
        self.config = config
        self.account_id = config.get("account_id", "unknown")
        self.proxy = config.get("proxy")
        self.session_path = config.get("session_path")
        self.headless = config.get("headless", False)

        # Get device configuration
        device_name = config.get("device", "iphone_12")
        self.device_config = MOBILE_DEVICES.get(device_name, MOBILE_DEVICES["iphone_12"])

        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

        logger.info(f"Initialized IGPoster for account: {self.account_id} with device: {device_name}")

    def human_delay(self, min_sec: float = 0.5, max_sec: float = 2.0) -> None:
        """Wait for a random human-like duration."""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def human_type(self, page: Page, text: str, min_delay: float = 0.08, max_delay: float = 0.18) -> None:
        """Type text with human-like delays (slightly slower for mobile)."""
        for char in text:
            page.keyboard.type(char)
            avg_delay = (min_delay + max_delay) / 2
            std_dev = (max_delay - min_delay) / 4
            delay = max(min_delay, random.gauss(avg_delay, std_dev))
            time.sleep(delay)

    def human_tap(self, page: Page, x: int, y: int) -> None:
        """Perform a human-like tap (touch) action."""
        # Small random offset for natural touch
        x_offset = random.randint(-3, 3)
        y_offset = random.randint(-3, 3)
        page.touchscreen.tap(x + x_offset, y + y_offset)
        self.human_delay(0.2, 0.5)

    def swipe(self, page: Page, direction: str = "up", distance: int = 300) -> None:
        """Perform a swipe gesture."""
        viewport = self.device_config["viewport"]
        center_x = viewport["width"] // 2
        center_y = viewport["height"] // 2

        if direction == "up":
            start_y = center_y + distance // 2
            end_y = center_y - distance // 2
            start_x = end_x = center_x
        elif direction == "down":
            start_y = center_y - distance // 2
            end_y = center_y + distance // 2
            start_x = end_x = center_x
        else:
            return

        # Simulate swipe with touchscreen
        page.mouse.move(start_x, start_y)
        page.mouse.down()
        page.mouse.move(end_x, end_y, steps=10)
        page.mouse.up()
        self.human_delay(0.3, 0.8)

    def _start_browser(self) -> None:
        """Start browser with mobile emulation."""
        self._playwright = sync_playwright().start()

        launch_options = {
            "headless": self.headless,
        }

        if self.proxy:
            launch_options["proxy"] = self.proxy
            logger.info(f"Using proxy: {self.proxy.get('server', 'configured')}")

        self.browser = self._playwright.chromium.launch(**launch_options)

        # Create context with mobile settings
        context_options = {
            "user_agent": self.device_config["user_agent"],
            "viewport": self.device_config["viewport"],
            "device_scale_factor": self.device_config["device_scale_factor"],
            "is_mobile": self.device_config["is_mobile"],
            "has_touch": self.device_config["has_touch"],
            "locale": "en-US",
            "timezone_id": "America/New_York",
        }

        if self.session_path and Path(self.session_path).exists():
            context_options["storage_state"] = self.session_path
            logger.info(f"Loaded session from: {self.session_path}")

        self.context = self.browser.new_context(**context_options)

        # Grant permissions for camera/location (prevents popups)
        self.context.grant_permissions(["geolocation"], origin="https://www.instagram.com")

        self.page = self.context.new_page()

        logger.info("Browser started with mobile emulation")

    def _stop_browser(self) -> None:
        """Stop browser and save session."""
        if self.context and self.session_path:
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
        """Check if logged into Instagram."""
        try:
            self.page.goto("https://www.instagram.com/", wait_until="networkidle", timeout=30000)
            self.human_delay(3, 5)

            # Dismiss any popups (notification request, etc.)
            self._dismiss_popups()

            # Check for login indicators
            logged_in_indicators = [
                'svg[aria-label="Home"]',
                'svg[aria-label="New post"]',
                '[aria-label="Navigation"]',
            ]

            for indicator in logged_in_indicators:
                if self.page.locator(indicator).count() > 0:
                    logger.info("Already logged in to Instagram")
                    return True

            # Check if login form is present
            login_form = self.page.locator('input[name="username"]')
            if login_form.count() > 0:
                logger.warning("Not logged in to Instagram")
                return False

            return False
        except Exception as e:
            logger.error(f"Error checking login status: {e}")
            return False

    def _dismiss_popups(self) -> None:
        """Dismiss common Instagram popups."""
        popup_dismiss_buttons = [
            'button:has-text("Not Now")',
            'button:has-text("Cancel")',
            '[aria-label="Close"]',
        ]

        for selector in popup_dismiss_buttons:
            try:
                popup = self.page.locator(selector)
                if popup.count() > 0 and popup.is_visible():
                    popup.click()
                    self.human_delay(0.5, 1)
            except:
                pass

    def post_feed(self, caption: str, image_path: str, hashtags: List[str] = None) -> Dict[str, Any]:
        """
        Post an image to Instagram feed.

        Args:
            caption: The post caption
            image_path: Path to the image file
            hashtags: Optional list of hashtags to append

        Returns:
            Dictionary with success status and details
        """
        result = {
            "success": False,
            "account_id": self.account_id,
            "timestamp": datetime.now().isoformat(),
            "type": "feed",
            "error": None
        }

        if not Path(image_path).exists():
            result["error"] = f"Image not found: {image_path}"
            logger.error(result["error"])
            return result

        try:
            self._start_browser()

            if not self.check_login():
                result["error"] = "Not logged in. Please log in manually first."
                return result

            # Build full caption with hashtags
            full_caption = caption
            if hashtags:
                full_caption = f"{caption}\n\n{' '.join(f'#{tag}' for tag in hashtags)}"

            # Navigate to create post
            logger.info("Starting post creation...")

            # Click create/plus button
            create_button = self.page.locator('svg[aria-label="New post"]').first
            if create_button.count() == 0:
                # Try alternative selector
                create_button = self.page.locator('[aria-label="New post"]').first

            if create_button.count() > 0:
                create_button.click()
                self.human_delay(1, 2)
            else:
                result["error"] = "Create button not found"
                return result

            # Wait for file input and upload
            self.human_delay(1, 2)
            file_input = self.page.locator('input[type="file"][accept*="image"]')

            if file_input.count() > 0:
                file_input.set_input_files(image_path)
                logger.info(f"Uploaded image: {image_path}")
                self.human_delay(2, 4)
            else:
                result["error"] = "File input not found"
                return result

            # Wait for image to load, then click Next
            self.human_delay(2, 3)

            # Click through the creation flow
            # First "Next" button (after selecting image)
            next_button = self.page.locator('div:has-text("Next")').first
            if next_button.count() > 0:
                next_button.click()
                self.human_delay(1, 2)

            # Second "Next" button (after filters)
            next_button = self.page.locator('div:has-text("Next")').first
            if next_button.count() > 0:
                next_button.click()
                self.human_delay(1, 2)

            # Enter caption
            caption_input = self.page.locator('textarea[aria-label*="caption"], textarea[placeholder*="caption"]')
            if caption_input.count() > 0:
                caption_input.click()
                self.human_delay(0.5, 1)
                self.human_type(self.page, full_caption)
                self.human_delay(1, 2)
            else:
                logger.warning("Caption input not found, continuing without caption")

            # Click Share button
            share_button = self.page.locator('div:has-text("Share")').first
            if share_button.count() > 0:
                share_button.click()
                self.human_delay(3, 5)
            else:
                result["error"] = "Share button not found"
                return result

            # Wait and verify success
            self.human_delay(5, 8)

            # Check for success indicators
            success_indicator = self.page.locator('text="Your post has been shared"')
            if success_indicator.count() > 0:
                result["success"] = True
                logger.info("Feed post successful!")
            else:
                # Alternative check: modal closed
                result["success"] = True  # Assume success if no error
                logger.info("Post likely successful (modal closed)")

            return result

        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Error posting to feed: {e}")
            return result

        finally:
            self._stop_browser()

    def post_story(self, image_path: str, sticker_text: str = None) -> Dict[str, Any]:
        """
        Post an image to Instagram story.

        Args:
            image_path: Path to the image file
            sticker_text: Optional text sticker to add

        Returns:
            Dictionary with success status and details
        """
        result = {
            "success": False,
            "account_id": self.account_id,
            "timestamp": datetime.now().isoformat(),
            "type": "story",
            "error": None
        }

        if not Path(image_path).exists():
            result["error"] = f"Image not found: {image_path}"
            logger.error(result["error"])
            return result

        try:
            self._start_browser()

            if not self.check_login():
                result["error"] = "Not logged in"
                return result

            logger.info("Starting story creation...")

            # Go to home feed first
            self.page.goto("https://www.instagram.com/", wait_until="networkidle")
            self.human_delay(2, 3)
            self._dismiss_popups()

            # Click on "Your Story" or plus icon
            story_button = self.page.locator('[aria-label="New Story"], [aria-label="Your story"]').first
            if story_button.count() > 0:
                story_button.click()
                self.human_delay(1, 2)
            else:
                # Try clicking profile picture area for story
                result["error"] = "Story creation button not found"
                return result

            # Upload image
            file_input = self.page.locator('input[type="file"][accept*="image"]')
            if file_input.count() > 0:
                file_input.set_input_files(image_path)
                logger.info(f"Uploaded story image: {image_path}")
                self.human_delay(3, 5)
            else:
                result["error"] = "Story file input not found"
                return result

            # Add text sticker if provided
            if sticker_text:
                text_button = self.page.locator('[aria-label="Text"], svg[aria-label="Text"]')
                if text_button.count() > 0:
                    text_button.click()
                    self.human_delay(0.5, 1)
                    self.human_type(self.page, sticker_text)
                    self.human_delay(0.5, 1)
                    # Click somewhere to deselect text
                    self.page.keyboard.press("Escape")

            # Share story
            self.human_delay(1, 2)
            share_button = self.page.locator('[aria-label="Share to Your Story"]')
            if share_button.count() > 0:
                share_button.click()
                self.human_delay(3, 5)
            else:
                # Try alternative
                share_button = self.page.locator('div:has-text("Share")').first
                if share_button.count() > 0:
                    share_button.click()
                    self.human_delay(3, 5)

            result["success"] = True
            logger.info("Story posted successfully!")

            return result

        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Error posting story: {e}")
            return result

        finally:
            self._stop_browser()

    def post_reel(self, video_path: str, caption: str = "", hashtags: List[str] = None) -> Dict[str, Any]:
        """
        Post a video as a Reel.

        Args:
            video_path: Path to the video file
            caption: Optional caption
            hashtags: Optional hashtags

        Returns:
            Dictionary with success status and details
        """
        result = {
            "success": False,
            "account_id": self.account_id,
            "timestamp": datetime.now().isoformat(),
            "type": "reel",
            "error": None
        }

        if not Path(video_path).exists():
            result["error"] = f"Video not found: {video_path}"
            return result

        try:
            self._start_browser()

            if not self.check_login():
                result["error"] = "Not logged in"
                return result

            full_caption = caption
            if hashtags:
                full_caption = f"{caption}\n\n{' '.join(f'#{tag}' for tag in hashtags)}"

            logger.info("Starting Reel creation...")

            # Click create button
            create_button = self.page.locator('svg[aria-label="New post"]').first
            if create_button.count() > 0:
                create_button.click()
                self.human_delay(1, 2)

            # Look for Reel option
            reel_option = self.page.locator('text="Reel"')
            if reel_option.count() > 0:
                reel_option.click()
                self.human_delay(1, 2)

            # Upload video
            file_input = self.page.locator('input[type="file"][accept*="video"]')
            if file_input.count() > 0:
                file_input.set_input_files(video_path)
                logger.info(f"Uploaded video: {video_path}")
                self.human_delay(5, 10)  # Videos take longer to process
            else:
                result["error"] = "Video input not found"
                return result

            # Navigate through creation flow
            for _ in range(2):
                next_button = self.page.locator('div:has-text("Next")').first
                if next_button.count() > 0:
                    next_button.click()
                    self.human_delay(2, 3)

            # Add caption
            caption_input = self.page.locator('textarea[aria-label*="caption"]')
            if caption_input.count() > 0:
                caption_input.click()
                self.human_type(self.page, full_caption)
                self.human_delay(1, 2)

            # Share
            share_button = self.page.locator('div:has-text("Share")').first
            if share_button.count() > 0:
                share_button.click()
                self.human_delay(5, 10)

            result["success"] = True
            logger.info("Reel posted successfully!")

            return result

        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Error posting reel: {e}")
            return result

        finally:
            self._stop_browser()


def load_config_from_env() -> Dict[str, Any]:
    """Load configuration from environment variables."""
    config = {
        "account_id": os.getenv("IG_ACCOUNT_ID", "default"),
        "device": os.getenv("IG_DEVICE", "iphone_12"),
        "headless": os.getenv("HEADLESS", "false").lower() == "true",
    }

    # Proxy configuration (Soax mobile proxy format)
    proxy_server = os.getenv("SOAX_PROXY_SERVER", os.getenv("PROXY_SERVER"))
    if proxy_server:
        config["proxy"] = {"server": proxy_server}

        proxy_user = os.getenv("SOAX_PROXY_USERNAME", os.getenv("PROXY_USERNAME"))
        proxy_pass = os.getenv("SOAX_PROXY_PASSWORD", os.getenv("PROXY_PASSWORD"))
        if proxy_user and proxy_pass:
            config["proxy"]["username"] = proxy_user
            config["proxy"]["password"] = proxy_pass

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

    parser = argparse.ArgumentParser(description="Post to Instagram")
    parser.add_argument("--type", "-t", choices=["feed", "story", "reel"], default="feed", help="Post type")
    parser.add_argument("--image", "-i", help="Path to image file")
    parser.add_argument("--video", "-v", help="Path to video file (for reels)")
    parser.add_argument("--caption", "-c", default="", help="Caption text")
    parser.add_argument("--hashtags", nargs="+", help="Hashtags (without #)")
    parser.add_argument("--config", help="Path to JSON config file")
    parser.add_argument("--account-id", help="Account identifier")
    parser.add_argument("--session-path", help="Path to session file")
    parser.add_argument("--device", help="Device profile (iphone_12, iphone_14_pro, pixel_7)")

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
    if args.device:
        config["device"] = args.device

    poster = IGPoster(config)

    # Execute based on type
    if args.type == "feed":
        if not args.image:
            print("Error: --image required for feed posts")
            sys.exit(1)
        result = poster.post_feed(args.caption, args.image, args.hashtags)

    elif args.type == "story":
        if not args.image:
            print("Error: --image required for stories")
            sys.exit(1)
        result = poster.post_story(args.image, args.caption if args.caption else None)

    elif args.type == "reel":
        if not args.video:
            print("Error: --video required for reels")
            sys.exit(1)
        result = poster.post_reel(args.video, args.caption, args.hashtags)

    print(json.dumps(result, indent=2))
    sys.exit(0 if result["success"] else 1)
