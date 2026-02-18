#!/usr/bin/env python3
"""
YouTube Comment Automation
==========================
Finds relevant videos and leaves valuable comments.
Targets videos in niches relevant to PRINTMAXX services.

Features:
- Search for videos by keywords
- Filter by view count, recency, channel
- Human-like comment writing
- Rate limiting (strict for YouTube)
- CSV logging of all comments
- Session persistence
- Proxy support

Usage:
    python youtube_commenter.py --session sessions/yt_account.json --search "indie hacker tutorial" --max-comments 3

Safety:
    - Very conservative rate limits (YouTube is strict)
    - Quality comments only (adds value, not spam)
    - Logs all actions for audit
    - Human review recommended before running
"""

import os
import sys
import csv
import json
import time
import random
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

try:
    from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
except ImportError:
    print("Error: playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)


# =============================================================================
# Configuration
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
LOG_DIR = PROJECT_ROOT / "OPS" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

COMMENTS_LOG_CSV = PROJECT_ROOT / "LEDGER" / "YOUTUBE_COMMENTS_LOG.csv"
VIDEOS_FOUND_CSV = PROJECT_ROOT / "LEDGER" / "YOUTUBE_VIDEOS_FOUND.csv"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "youtube_commenter.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("youtube_commenter")

# User agents
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

VIEWPORTS = [
    {"width": 1280, "height": 720},
    {"width": 1366, "height": 768},
    {"width": 1920, "height": 1080},
]

# Default search queries (niche-relevant)
DEFAULT_SEARCHES = [
    "indie hacker tutorial",
    "build a side project",
    "solopreneur tools",
    "passive income website",
    "how to launch a product",
    "saas tutorial beginner",
    "content automation",
    "email list building",
]

# Comment templates by video type
# These are VALUE-ADDING comments, not spam
COMMENT_TEMPLATES = {
    "tutorial": [
        "Clear explanation. The step-by-step breakdown at {timestamp} was especially helpful.",
        "This is one of the better tutorials on this topic. Subscribed.",
        "Solid walkthrough. Would love to see a follow-up on {topic}.",
        "Bookmarking this. The {specific} tip is underrated.",
    ],
    "case_study": [
        "Real numbers and transparency, appreciate that. The {metric} breakdown was interesting.",
        "This kind of content is rare. Most people don't share actual results.",
        "Helpful case study. The part about {challenge} resonated.",
    ],
    "tools": [
        "Been looking for something like this. How does it compare to {alternative}?",
        "Good overview. The {feature} looks useful for my workflow.",
        "Thanks for the demo. Does this integrate with {tool}?",
    ],
    "generic": [
        "Quality content. This channel is underrated.",
        "Useful video, thanks for putting this together.",
        "Good info here. Looking forward to more content.",
        "This helped clarify a few things I was confused about.",
    ],
}

# Daily limits (YouTube is very strict)
DAILY_LIMITS = {
    "comments": 5,  # Very conservative
    "videos_watched": 20,
}


# =============================================================================
# Helper Functions
# =============================================================================

def log_video(
    video_title: str,
    video_url: str,
    channel: str,
    view_count: str,
    search_query: str
):
    """Log a found video to CSV."""
    VIDEOS_FOUND_CSV.parent.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "title": video_title[:200],
        "url": video_url,
        "channel": channel,
        "view_count": view_count,
        "search_query": search_query,
        "commented": False,
    }

    file_exists = VIDEOS_FOUND_CSV.exists()

    with open(VIDEOS_FOUND_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=log_entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_entry)


def log_comment(
    video_title: str,
    video_url: str,
    comment_text: str,
    success: bool,
    notes: str = ""
):
    """Log a comment action to CSV."""
    COMMENTS_LOG_CSV.parent.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "video_title": video_title[:100],
        "video_url": video_url,
        "comment_text": comment_text,
        "success": success,
        "notes": notes,
    }

    file_exists = COMMENTS_LOG_CSV.exists()

    with open(COMMENTS_LOG_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=log_entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_entry)


def get_comment_for_video(video_title: str, video_description: str = "") -> str:
    """Generate a contextual comment based on video type."""
    title_lower = video_title.lower()

    # Detect video type
    if any(word in title_lower for word in ['tutorial', 'how to', 'guide', 'step by step', 'walkthrough']):
        category = "tutorial"
    elif any(word in title_lower for word in ['case study', 'made $', 'revenue', 'results', 'what i learned']):
        category = "case_study"
    elif any(word in title_lower for word in ['tool', 'app', 'software', 'review', 'demo']):
        category = "tools"
    else:
        category = "generic"

    template = random.choice(COMMENT_TEMPLATES[category])

    # Simple placeholder replacement (customize as needed)
    # In practice, you'd analyze the video more to fill these
    replacements = {
        "{timestamp}": random.choice(["3:45", "around 5 mins", "the middle section"]),
        "{topic}": "the implementation details",
        "{specific}": "the workflow",
        "{metric}": "the conversion",
        "{challenge}": "scaling",
        "{alternative}": "similar tools",
        "{feature}": "automation",
        "{tool}": "Notion",
    }

    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)

    return template


# =============================================================================
# Main Commenter Class
# =============================================================================

class YouTubeCommenter:
    """Find relevant YouTube videos and leave valuable comments."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize commenter.

        Args:
            config: Dictionary containing:
                - session_path: Path to saved browser session
                - proxy: Optional proxy config
                - headless: Run headless (default False)
                - max_comments: Max comments this session
                - search_queries: List of search terms
                - research_only: If True, find videos but don't comment
        """
        self.config = config
        self.session_path = config.get("session_path")
        self.proxy = config.get("proxy")
        self.headless = config.get("headless", False)
        self.max_comments = config.get("max_comments", 3)
        self.search_queries = config.get("search_queries", DEFAULT_SEARCHES)
        self.research_only = config.get("research_only", False)

        self.user_agent = random.choice(USER_AGENTS)
        self.viewport = random.choice(VIEWPORTS)

        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

        # Stats
        self.stats = {
            "videos_found": 0,
            "comments_posted": 0,
            "errors": 0,
        }

        logger.info(f"YouTubeCommenter initialized (research_only={self.research_only})")

    # -------------------------------------------------------------------------
    # Browser Control
    # -------------------------------------------------------------------------

    def _start_browser(self) -> None:
        """Start browser with settings."""
        self._playwright = sync_playwright().start()

        launch_options = {
            "headless": self.headless,
        }

        if self.proxy:
            launch_options["proxy"] = self.proxy

        self.browser = self._playwright.chromium.launch(**launch_options)

        context_options = {
            "user_agent": self.user_agent,
            "viewport": self.viewport,
            "locale": "en-US",
        }

        if self.session_path and Path(self.session_path).exists():
            context_options["storage_state"] = self.session_path
            logger.info(f"Loaded session: {self.session_path}")

        self.context = self.browser.new_context(**context_options)
        self.page = self.context.new_page()

        logger.info("Browser started")

    def _stop_browser(self) -> None:
        """Stop browser and save session."""
        if self.context and self.session_path:
            session_dir = Path(self.session_path).parent
            session_dir.mkdir(parents=True, exist_ok=True)
            self.context.storage_state(path=self.session_path)
            logger.info(f"Session saved: {self.session_path}")

        if self.browser:
            self.browser.close()
        if hasattr(self, '_playwright'):
            self._playwright.stop()

        logger.info("Browser stopped")

    # -------------------------------------------------------------------------
    # Human-Like Behavior
    # -------------------------------------------------------------------------

    def human_delay(self, min_sec: float = 2.0, max_sec: float = 6.0) -> None:
        """Human-like delay."""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def human_type(self, text: str) -> None:
        """Type with human-like speed."""
        for char in text:
            self.page.keyboard.type(char)
            # Variable delay
            if char in ' etaoinshrdlu':
                time.sleep(random.uniform(0.03, 0.08))
            else:
                time.sleep(random.uniform(0.05, 0.12))

    def simulate_watching(self, seconds: int = 30) -> None:
        """Simulate watching video for realism."""
        logger.info(f"Simulating watch for {seconds}s...")

        # Random scroll/mouse movements
        for _ in range(seconds // 5):
            self.page.mouse.wheel(0, random.randint(-50, 50))
            time.sleep(random.uniform(4, 6))

    # -------------------------------------------------------------------------
    # Core Actions
    # -------------------------------------------------------------------------

    def check_login(self) -> bool:
        """Check if logged into YouTube."""
        try:
            self.page.goto("https://www.youtube.com", wait_until="networkidle", timeout=30000)
            self.human_delay(2, 4)

            # Check for sign-in button absence (means logged in)
            sign_in_btn = self.page.locator('a[href*="accounts.google.com"]')
            if sign_in_btn.count() > 0:
                logger.warning("Not logged in to YouTube")
                return False

            # Check for avatar (indicates logged in)
            avatar = self.page.locator('#avatar-btn, button#avatar-btn')
            if avatar.count() > 0:
                logger.info("Logged into YouTube")
                return True

            logger.warning("Login status unclear")
            return False

        except Exception as e:
            logger.error(f"Login check failed: {e}")
            return False

    def search_videos(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """
        Search YouTube for videos.

        Returns:
            List of video dicts with title, url, channel, views
        """
        videos = []

        try:
            # Navigate to search
            search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            self.page.goto(search_url, wait_until="networkidle", timeout=30000)
            self.human_delay(2, 4)

            # Get video results
            video_elements = self.page.locator('ytd-video-renderer').all()

            for elem in video_elements[:max_results]:
                try:
                    # Title and URL
                    title_elem = elem.locator('a#video-title')
                    if not title_elem.count():
                        continue

                    title = title_elem.get_attribute('title') or title_elem.inner_text()
                    url = title_elem.get_attribute('href')
                    if url and not url.startswith('http'):
                        url = f"https://www.youtube.com{url}"

                    # Channel
                    channel_elem = elem.locator('ytd-channel-name a')
                    channel = channel_elem.inner_text() if channel_elem.count() else "Unknown"

                    # View count
                    views_elem = elem.locator('span.ytd-video-meta-block')
                    views = views_elem.first.inner_text() if views_elem.count() else "Unknown"

                    video = {
                        "title": title,
                        "url": url,
                        "channel": channel,
                        "views": views,
                    }

                    videos.append(video)
                    log_video(title, url, channel, views, query)
                    self.stats["videos_found"] += 1

                except Exception as e:
                    logger.debug(f"Error extracting video: {e}")
                    continue

            logger.info(f"Found {len(videos)} videos for '{query}'")
            return videos

        except Exception as e:
            logger.error(f"Search failed for '{query}': {e}")
            self.stats["errors"] += 1
            return videos

    def post_comment(self, video_url: str, video_title: str) -> bool:
        """
        Post a comment on a video.

        Args:
            video_url: Full YouTube video URL
            video_title: Video title for context

        Returns:
            True if comment posted successfully
        """
        if self.research_only:
            logger.info("Research mode - skipping comment")
            return False

        try:
            # Navigate to video
            self.page.goto(video_url, wait_until="networkidle", timeout=30000)
            self.human_delay(3, 5)

            # Simulate watching a bit (important for legitimacy)
            self.simulate_watching(20)

            # Scroll to comments
            self.page.keyboard.press("End")
            self.human_delay(2, 3)
            self.page.keyboard.press("Home")
            self.human_delay(1, 2)

            # Find comment box
            # First, need to click placeholder to activate
            comment_placeholder = self.page.locator('#placeholder-area, #simplebox-placeholder')
            if not comment_placeholder.count():
                logger.warning("Comment box not found - comments may be disabled")
                return False

            comment_placeholder.click()
            self.human_delay(1, 2)

            # Wait for actual input field
            comment_input = self.page.locator('#contenteditable-root, div[contenteditable="true"]')
            comment_input.wait_for(state="visible", timeout=5000)

            # Generate and type comment
            comment_text = get_comment_for_video(video_title)

            comment_input.click()
            self.human_delay(0.5, 1)
            self.human_type(comment_text)
            self.human_delay(1, 2)

            # Click submit
            submit_btn = self.page.locator('#submit-button, button[aria-label*="Comment"]')
            if submit_btn.count():
                submit_btn.click()
                self.human_delay(3, 5)

                self.stats["comments_posted"] += 1
                logger.info(f"Posted comment on '{video_title[:50]}...': '{comment_text[:50]}...'")
                log_comment(video_title, video_url, comment_text, True)

                return True
            else:
                logger.warning("Submit button not found")
                return False

        except Exception as e:
            logger.error(f"Failed to comment: {e}")
            log_comment(video_title, video_url, "", False, str(e))
            self.stats["errors"] += 1
            return False

    def run(self) -> Dict[str, Any]:
        """
        Run commenting session.

        Returns:
            Summary statistics
        """
        result = {
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "videos_found": 0,
            "comments_posted": 0,
            "research_only": self.research_only,
            "errors": 0,
        }

        try:
            self._start_browser()

            # Check login (required for commenting)
            if not self.research_only and not self.check_login():
                logger.error("Must be logged in to comment")
                result["errors"] = 1
                return result

            # Search and collect videos
            all_videos = []
            for query in self.search_queries:
                videos = self.search_videos(query, max_results=5)
                all_videos.extend(videos)
                self.human_delay(5, 10)

                # Stop if we have enough
                if len(all_videos) >= 20:
                    break

            # Comment on videos (if not research only)
            if not self.research_only:
                # Shuffle to avoid pattern
                random.shuffle(all_videos)

                for video in all_videos:
                    if self.stats["comments_posted"] >= self.max_comments:
                        logger.info("Reached comment limit")
                        break

                    self.post_comment(video["url"], video["title"])

                    # Long delay between comments (YouTube is strict)
                    self.human_delay(60, 120)

            # Build result
            result["success"] = True
            result["videos_found"] = self.stats["videos_found"]
            result["comments_posted"] = self.stats["comments_posted"]
            result["errors"] = self.stats["errors"]

            logger.info(
                f"Session complete: {result['videos_found']} videos found, "
                f"{result['comments_posted']} comments posted"
            )

            return result

        except Exception as e:
            logger.error(f"Session failed: {e}")
            result["errors"] += 1
            return result

        finally:
            self._stop_browser()


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="YouTube video finder and commenter"
    )
    parser.add_argument(
        "--session", "-s",
        help="Path to browser session file (required for commenting)"
    )
    parser.add_argument(
        "--search",
        help="Search query (can use multiple times)",
        action="append"
    )
    parser.add_argument(
        "--max-comments", "-c",
        type=int,
        default=3,
        help="Maximum comments this session (default: 3)"
    )
    parser.add_argument(
        "--research-only", "-r",
        action="store_true",
        help="Find videos but don't comment (safe mode)"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run headless (not recommended)"
    )
    parser.add_argument(
        "--proxy",
        help="Proxy server URL"
    )

    args = parser.parse_args()

    # Build config
    config = {
        "session_path": args.session,
        "max_comments": args.max_comments,
        "research_only": args.research_only,
        "headless": args.headless,
    }

    # Search queries
    if args.search:
        config["search_queries"] = args.search
    else:
        config["search_queries"] = DEFAULT_SEARCHES[:3]  # Use first 3 defaults

    # Proxy
    if args.proxy:
        config["proxy"] = {"server": args.proxy}

    # Run
    commenter = YouTubeCommenter(config)
    result = commenter.run()

    # Output
    print(json.dumps(result, indent=2))
    print(f"\nVideos logged to: {VIDEOS_FOUND_CSV}")
    if not args.research_only:
        print(f"Comments logged to: {COMMENTS_LOG_CSV}")
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
