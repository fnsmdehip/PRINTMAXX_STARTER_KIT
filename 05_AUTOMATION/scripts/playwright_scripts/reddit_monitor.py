#!/usr/bin/env python3
"""
Reddit Monitoring Automation
=============================
Monitors subreddits for keywords and logs opportunities.
Finds posts/comments where PRINTMAXX services could add value.

Features:
- Monitors subreddits from HIGH_SIGNAL_SOURCES.csv
- Keyword matching for opportunity detection
- CSV logging of all opportunities found
- Human-like browsing behavior
- Proxy support
- No posting (research/monitoring only)

Usage:
    python reddit_monitor.py --subreddits SideProject,juststart --keywords "automation,side project,passive income"

Safety:
    - Read-only (no posting, commenting, or voting)
    - Rate limited browsing
    - Logs opportunities for manual review
    - Human-like delays between pages
"""

import os
import sys
import csv
import json
import time
import random
import logging
import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Set

try:
    from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
except ImportError:
    print("Error: playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)


# =============================================================================
# Configuration
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
SOURCES_CSV = PROJECT_ROOT / "LEDGER" / "HIGH_SIGNAL_SOURCES.csv"
LOG_DIR = PROJECT_ROOT / "OPS" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

OPPORTUNITIES_CSV = PROJECT_ROOT / "LEDGER" / "REDDIT_OPPORTUNITIES.csv"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "reddit_monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("reddit_monitor")

# User agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

VIEWPORTS = [
    {"width": 1280, "height": 720},
    {"width": 1366, "height": 768},
    {"width": 1920, "height": 1080},
]

# Default subreddits to monitor (from HIGH_SIGNAL_SOURCES)
DEFAULT_SUBREDDITS = [
    "SideProject",
    "EntrepreneurRideAlong",
    "juststart",
    "coldemail",
    "indiehackers",
    "AppBusiness",
    "growthhacking",
    "affiliatemarketing",
]

# Default keywords to match
DEFAULT_KEYWORDS = [
    # Problem indicators
    "struggling with",
    "need help",
    "looking for",
    "how do i",
    "how to",
    "best way to",
    "recommendation",
    "advice",
    "anyone know",

    # Our solution space
    "automation",
    "content creation",
    "side project",
    "passive income",
    "landing page",
    "email list",
    "cold email",
    "seo",
    "affiliate",
    "solopreneur",
    "indie hacker",
    "app idea",
    "mvp",
    "launch",
    "marketing",
    "growth hack",
]

# Opportunity scoring keywords (higher score = better opportunity)
HIGH_VALUE_KEYWORDS = [
    "paying for",
    "budget",
    "willing to pay",
    "need a tool",
    "need a service",
    "hire",
    "contractor",
    "freelancer",
    "agency",
]


# =============================================================================
# Helper Functions
# =============================================================================

def load_subreddits_from_sources() -> List[str]:
    """Load subreddit names from HIGH_SIGNAL_SOURCES.csv."""
    subreddits = []

    if not SOURCES_CSV.exists():
        logger.warning(f"Sources file not found: {SOURCES_CSV}")
        return DEFAULT_SUBREDDITS

    with open(SOURCES_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('source_type', '') == 'Subreddit':
                # Extract subreddit name from url or name
                name = row.get('source_name', '').replace('r/', '')
                if name:
                    subreddits.append(name)

    return subreddits if subreddits else DEFAULT_SUBREDDITS


def score_opportunity(title: str, body: str, keywords: List[str]) -> int:
    """
    Score an opportunity based on keyword matches.
    Higher score = more relevant opportunity.
    """
    score = 0
    text = (title + " " + body).lower()

    # Base keywords
    for keyword in keywords:
        if keyword.lower() in text:
            score += 1

    # High value keywords (worth more)
    for keyword in HIGH_VALUE_KEYWORDS:
        if keyword.lower() in text:
            score += 3

    return score


def log_opportunity(
    subreddit: str,
    post_title: str,
    post_url: str,
    post_body: str,
    score: int,
    matched_keywords: List[str]
):
    """Log a found opportunity to CSV."""
    OPPORTUNITIES_CSV.parent.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "subreddit": subreddit,
        "title": post_title[:200],
        "url": post_url,
        "body_preview": post_body[:300] if post_body else "",
        "score": score,
        "matched_keywords": "|".join(matched_keywords[:10]),
        "status": "NEW",
        "notes": "",
    }

    file_exists = OPPORTUNITIES_CSV.exists()

    with open(OPPORTUNITIES_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=log_entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_entry)

    logger.info(f"Logged opportunity: r/{subreddit} - {post_title[:50]}... (score: {score})")


def extract_matched_keywords(text: str, keywords: List[str]) -> List[str]:
    """Find which keywords matched in the text."""
    matched = []
    text_lower = text.lower()

    for keyword in keywords:
        if keyword.lower() in text_lower:
            matched.append(keyword)

    return matched


# =============================================================================
# Main Monitor Class
# =============================================================================

class RedditMonitor:
    """Monitor Reddit subreddits for opportunities."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize monitor.

        Args:
            config: Dictionary containing:
                - subreddits: List of subreddit names to monitor
                - keywords: List of keywords to match
                - proxy: Optional proxy config
                - headless: Run headless (default True for monitoring)
                - max_posts: Max posts to check per subreddit
                - min_score: Minimum score to log opportunity
        """
        self.config = config
        self.subreddits = config.get("subreddits", DEFAULT_SUBREDDITS)
        self.keywords = config.get("keywords", DEFAULT_KEYWORDS)
        self.proxy = config.get("proxy")
        self.headless = config.get("headless", True)
        self.max_posts = config.get("max_posts", 25)
        self.min_score = config.get("min_score", 2)

        self.user_agent = random.choice(USER_AGENTS)
        self.viewport = random.choice(VIEWPORTS)

        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

        # Track what we've seen (avoid duplicates)
        self.seen_urls: Set[str] = set()

        # Stats
        self.stats = {
            "subreddits_scanned": 0,
            "posts_checked": 0,
            "opportunities_found": 0,
            "errors": 0,
        }

        logger.info(f"RedditMonitor initialized with {len(self.subreddits)} subreddits, {len(self.keywords)} keywords")

    # -------------------------------------------------------------------------
    # Browser Control
    # -------------------------------------------------------------------------

    def _start_browser(self) -> None:
        """Start browser with stealth settings."""
        self._playwright = sync_playwright().start()

        launch_options = {
            "headless": self.headless,
        }

        if self.proxy:
            launch_options["proxy"] = self.proxy
            logger.info(f"Using proxy: {self.proxy.get('server', 'configured')}")

        self.browser = self._playwright.chromium.launch(**launch_options)

        context_options = {
            "user_agent": self.user_agent,
            "viewport": self.viewport,
            "locale": "en-US",
        }

        self.context = self.browser.new_context(**context_options)
        self.page = self.context.new_page()

        # Block unnecessary resources for speed
        self.page.route("**/*.{png,jpg,jpeg,gif,svg,webp}", lambda route: route.abort())
        self.page.route("**/advertisement*", lambda route: route.abort())

        logger.info("Browser started")

    def _stop_browser(self) -> None:
        """Stop browser."""
        if self.browser:
            self.browser.close()
        if hasattr(self, '_playwright'):
            self._playwright.stop()

        logger.info("Browser stopped")

    # -------------------------------------------------------------------------
    # Human-Like Behavior
    # -------------------------------------------------------------------------

    def human_delay(self, min_sec: float = 2.0, max_sec: float = 5.0) -> None:
        """Wait with human-like timing."""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def random_scroll(self) -> None:
        """Scroll page randomly."""
        scroll_amount = random.randint(300, 700)
        self.page.mouse.wheel(0, scroll_amount)
        self.human_delay(1, 2)

    # -------------------------------------------------------------------------
    # Core Monitoring
    # -------------------------------------------------------------------------

    def scan_subreddit(self, subreddit: str) -> int:
        """
        Scan a subreddit for opportunities.

        Args:
            subreddit: Subreddit name (without r/)

        Returns:
            Number of opportunities found
        """
        opportunities = 0

        try:
            # Use old.reddit.com for easier scraping (simpler HTML)
            url = f"https://old.reddit.com/r/{subreddit}/new/"
            self.page.goto(url, wait_until="networkidle", timeout=30000)
            self.human_delay(2, 4)

            # Check if subreddit exists
            if "search results" in self.page.content().lower() or "banned" in self.page.content().lower():
                logger.warning(f"Subreddit r/{subreddit} not accessible")
                return 0

            logger.info(f"Scanning r/{subreddit}...")

            posts_checked = 0
            scroll_count = 0
            max_scrolls = 5

            while posts_checked < self.max_posts and scroll_count < max_scrolls:
                # Find post entries
                posts = self.page.locator('div.thing.link').all()

                for post in posts:
                    if posts_checked >= self.max_posts:
                        break

                    try:
                        # Extract post data
                        title_elem = post.locator('a.title')
                        if not title_elem.count():
                            continue

                        title = title_elem.inner_text()
                        post_url = title_elem.get_attribute('href')

                        # Make URL absolute if relative
                        if post_url and not post_url.startswith('http'):
                            post_url = f"https://old.reddit.com{post_url}"

                        # Skip if already seen
                        if post_url in self.seen_urls:
                            continue
                        self.seen_urls.add(post_url)

                        # Get self-text preview if available
                        body = ""
                        expando = post.locator('div.expando')
                        if expando.count():
                            try:
                                body = expando.inner_text()[:500]
                            except:
                                pass

                        posts_checked += 1
                        self.stats["posts_checked"] += 1

                        # Check for keyword matches
                        full_text = title + " " + body
                        matched = extract_matched_keywords(full_text, self.keywords)

                        if matched:
                            score = score_opportunity(title, body, self.keywords)

                            if score >= self.min_score:
                                log_opportunity(
                                    subreddit=subreddit,
                                    post_title=title,
                                    post_url=post_url,
                                    post_body=body,
                                    score=score,
                                    matched_keywords=matched
                                )
                                opportunities += 1
                                self.stats["opportunities_found"] += 1

                    except Exception as e:
                        logger.debug(f"Error processing post: {e}")
                        continue

                # Scroll for more posts
                self.random_scroll()
                scroll_count += 1

            logger.info(f"r/{subreddit}: checked {posts_checked} posts, found {opportunities} opportunities")
            self.stats["subreddits_scanned"] += 1

            return opportunities

        except Exception as e:
            logger.error(f"Error scanning r/{subreddit}: {e}")
            self.stats["errors"] += 1
            return opportunities

    def run(self) -> Dict[str, Any]:
        """
        Run monitoring session across all subreddits.

        Returns:
            Summary statistics
        """
        result = {
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "subreddits_scanned": 0,
            "posts_checked": 0,
            "opportunities_found": 0,
            "errors": 0,
        }

        try:
            self._start_browser()

            logger.info(f"Starting Reddit monitoring: {len(self.subreddits)} subreddits")

            for subreddit in self.subreddits:
                self.scan_subreddit(subreddit)

                # Delay between subreddits
                self.human_delay(5, 10)

            # Build result
            result["success"] = True
            result["subreddits_scanned"] = self.stats["subreddits_scanned"]
            result["posts_checked"] = self.stats["posts_checked"]
            result["opportunities_found"] = self.stats["opportunities_found"]
            result["errors"] = self.stats["errors"]

            logger.info(
                f"Monitoring complete: {result['subreddits_scanned']} subreddits, "
                f"{result['posts_checked']} posts, {result['opportunities_found']} opportunities"
            )

            return result

        except Exception as e:
            logger.error(f"Monitoring session failed: {e}")
            result["errors"] += 1
            return result

        finally:
            self._stop_browser()


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Monitor Reddit subreddits for opportunities"
    )
    parser.add_argument(
        "--subreddits", "-s",
        help="Comma-separated list of subreddit names (no r/ prefix)"
    )
    parser.add_argument(
        "--keywords", "-k",
        help="Comma-separated list of keywords to match"
    )
    parser.add_argument(
        "--max-posts", "-m",
        type=int,
        default=25,
        help="Maximum posts to check per subreddit (default: 25)"
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=2,
        help="Minimum score to log opportunity (default: 2)"
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run with visible browser (default is headless)"
    )
    parser.add_argument(
        "--proxy",
        help="Proxy server URL (e.g., http://user:pass@proxy:port)"
    )
    parser.add_argument(
        "--use-sources",
        action="store_true",
        help="Load subreddits from HIGH_SIGNAL_SOURCES.csv"
    )

    args = parser.parse_args()

    # Build config
    config = {
        "max_posts": args.max_posts,
        "min_score": args.min_score,
        "headless": not args.headed,
    }

    # Set subreddits
    if args.use_sources:
        config["subreddits"] = load_subreddits_from_sources()
    elif args.subreddits:
        config["subreddits"] = [s.strip() for s in args.subreddits.split(",")]
    else:
        config["subreddits"] = DEFAULT_SUBREDDITS

    # Set keywords
    if args.keywords:
        config["keywords"] = [k.strip() for k in args.keywords.split(",")]
    else:
        config["keywords"] = DEFAULT_KEYWORDS

    # Proxy
    if args.proxy:
        config["proxy"] = {"server": args.proxy}

    # Run monitor
    monitor = RedditMonitor(config)
    result = monitor.run()

    # Output result
    print(json.dumps(result, indent=2))
    print(f"\nOpportunities saved to: {OPPORTUNITIES_CSV}")
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
