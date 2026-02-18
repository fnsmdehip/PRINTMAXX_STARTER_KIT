#!/usr/bin/env python3
"""
TikTok Trend Scraper
====================
Scrapes trending sounds, hashtags, and content patterns from TikTok.
Research tool for content strategy - no posting or interaction.

Features:
- Scrape trending sounds in niches
- Scrape trending hashtags
- Extract content patterns (hooks, formats)
- CSV logging of all findings
- Proxy support (recommended for TikTok)
- Human-like browsing

Usage:
    python tiktok_scraper.py --hashtags "solopreneur,sideproject" --max-videos 20

Safety:
    - Read-only (no posting, liking, or following)
    - Research/analytics purposes only
    - Rate limited browsing
    - Proxy recommended (TikTok blocks aggressively)
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
LOG_DIR = PROJECT_ROOT / "OPS" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

TRENDS_CSV = PROJECT_ROOT / "LEDGER" / "TIKTOK_TRENDS.csv"
SOUNDS_CSV = PROJECT_ROOT / "LEDGER" / "TIKTOK_SOUNDS.csv"
HASHTAGS_CSV = PROJECT_ROOT / "LEDGER" / "TIKTOK_HASHTAGS.csv"
CONTENT_PATTERNS_CSV = PROJECT_ROOT / "LEDGER" / "TIKTOK_CONTENT_PATTERNS.csv"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "tiktok_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("tiktok_scraper")

# User agents (mobile for TikTok)
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
]

# Mobile viewports
VIEWPORTS = [
    {"width": 390, "height": 844},  # iPhone 14
    {"width": 393, "height": 873},  # Pixel 7
    {"width": 414, "height": 896},  # iPhone 11
]

# Default hashtags to track by niche
NICHE_HASHTAGS = {
    "business": [
        "solopreneur",
        "sideproject",
        "passiveincome",
        "onlinebusiness",
        "smallbusiness",
        "entrepreneurlife",
    ],
    "tech": [
        "coding",
        "webdev",
        "techstartup",
        "indiehacker",
        "buildinpublic",
        "saas",
    ],
    "faith": [
        "christiancontent",
        "faithcontent",
        "christian",
        "biblestudy",
        "prayerlife",
    ],
    "fitness": [
        "fitnessmotivation",
        "workout",
        "gymlife",
        "healthylifestyle",
        "fitnessjourney",
    ],
}


# =============================================================================
# Helper Functions
# =============================================================================

def log_trend(
    trend_type: str,
    name: str,
    url: str,
    metrics: Dict[str, Any],
    niche: str = ""
):
    """Log a trend to CSV."""
    TRENDS_CSV.parent.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "trend_type": trend_type,
        "name": name,
        "url": url,
        "views": metrics.get("views", ""),
        "videos": metrics.get("videos", ""),
        "niche": niche,
        "notes": metrics.get("notes", ""),
    }

    file_exists = TRENDS_CSV.exists()

    with open(TRENDS_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=log_entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_entry)


def log_sound(
    sound_name: str,
    sound_url: str,
    artist: str,
    usage_count: str,
    sample_videos: List[str]
):
    """Log a sound to CSV."""
    SOUNDS_CSV.parent.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "sound_name": sound_name[:200],
        "sound_url": sound_url,
        "artist": artist,
        "usage_count": usage_count,
        "sample_videos": "|".join(sample_videos[:5]),
    }

    file_exists = SOUNDS_CSV.exists()

    with open(SOUNDS_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=log_entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_entry)


def log_hashtag(
    hashtag: str,
    hashtag_url: str,
    view_count: str,
    video_count: str,
    sample_videos: List[str]
):
    """Log a hashtag to CSV."""
    HASHTAGS_CSV.parent.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "hashtag": hashtag,
        "url": hashtag_url,
        "view_count": view_count,
        "video_count": video_count,
        "sample_videos": "|".join(sample_videos[:5]),
    }

    file_exists = HASHTAGS_CSV.exists()

    with open(HASHTAGS_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=log_entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_entry)


def log_content_pattern(
    video_url: str,
    hook_type: str,
    format_type: str,
    description: str,
    engagement: str
):
    """Log a content pattern to CSV."""
    CONTENT_PATTERNS_CSV.parent.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "video_url": video_url,
        "hook_type": hook_type,
        "format_type": format_type,
        "description": description[:300],
        "engagement": engagement,
    }

    file_exists = CONTENT_PATTERNS_CSV.exists()

    with open(CONTENT_PATTERNS_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=log_entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_entry)


def parse_count(count_str: str) -> int:
    """Parse TikTok count strings (e.g., '1.2M', '500K') to integers."""
    if not count_str:
        return 0

    count_str = count_str.strip().upper()

    try:
        if 'M' in count_str:
            return int(float(count_str.replace('M', '').replace(',', '')) * 1_000_000)
        elif 'K' in count_str:
            return int(float(count_str.replace('K', '').replace(',', '')) * 1_000)
        elif 'B' in count_str:
            return int(float(count_str.replace('B', '').replace(',', '')) * 1_000_000_000)
        else:
            return int(count_str.replace(',', ''))
    except:
        return 0


def detect_hook_type(video_text: str) -> str:
    """Detect the type of hook used in video."""
    text_lower = video_text.lower()

    if any(phrase in text_lower for phrase in ['you need to', 'you should', 'stop doing']):
        return "direct_command"
    elif any(phrase in text_lower for phrase in ['did you know', 'most people', 'the truth about']):
        return "curiosity_gap"
    elif any(phrase in text_lower for phrase in ['this is why', "here's why", 'the reason']):
        return "explanation"
    elif any(phrase in text_lower for phrase in ['made $', 'earned', 'my results', 'income']):
        return "results_proof"
    elif any(phrase in text_lower for phrase in ['pov:', 'when you', 'that feeling']):
        return "relatable_scenario"
    elif any(phrase in text_lower for phrase in ['step 1', 'how to', 'tutorial']):
        return "how_to"
    else:
        return "unknown"


def detect_format_type(video_elements: Dict) -> str:
    """Detect content format type."""
    # This would need video analysis in practice
    # For now, infer from available metadata
    return "talking_head"  # Default


# =============================================================================
# Main Scraper Class
# =============================================================================

class TikTokScraper:
    """Scrape TikTok for trending content, sounds, and hashtags."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize scraper.

        Args:
            config: Dictionary containing:
                - proxy: Proxy config (recommended)
                - headless: Run headless
                - hashtags: List of hashtags to scrape
                - niches: List of niches to scrape
                - max_videos: Max videos to analyze per hashtag
        """
        self.config = config
        self.proxy = config.get("proxy")
        self.headless = config.get("headless", True)
        self.hashtags = config.get("hashtags", [])
        self.niches = config.get("niches", ["business"])
        self.max_videos = config.get("max_videos", 20)

        self.user_agent = random.choice(USER_AGENTS)
        self.viewport = random.choice(VIEWPORTS)

        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

        # Track seen items
        self.seen_sounds: Set[str] = set()
        self.seen_hashtags: Set[str] = set()

        # Stats
        self.stats = {
            "hashtags_scraped": 0,
            "videos_analyzed": 0,
            "sounds_found": 0,
            "patterns_logged": 0,
            "errors": 0,
        }

        logger.info("TikTokScraper initialized")

    # -------------------------------------------------------------------------
    # Browser Control
    # -------------------------------------------------------------------------

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

        # Mobile context for TikTok
        context_options = {
            "user_agent": self.user_agent,
            "viewport": self.viewport,
            "locale": "en-US",
            "is_mobile": True,
            "has_touch": True,
        }

        self.context = self.browser.new_context(**context_options)
        self.page = self.context.new_page()

        logger.info("Browser started (mobile mode)")

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
        """Human-like delay."""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def scroll_feed(self, times: int = 3) -> None:
        """Scroll through feed like a user."""
        for _ in range(times):
            # Swipe up (mobile style)
            self.page.evaluate("""
                window.scrollBy({
                    top: window.innerHeight * 0.8,
                    behavior: 'smooth'
                });
            """)
            self.human_delay(2, 4)

    # -------------------------------------------------------------------------
    # Scraping Functions
    # -------------------------------------------------------------------------

    def scrape_hashtag(self, hashtag: str) -> Dict[str, Any]:
        """
        Scrape a hashtag page for videos and trends.

        Args:
            hashtag: Hashtag without #

        Returns:
            Dict with hashtag stats and videos found
        """
        result = {
            "hashtag": hashtag,
            "videos_found": 0,
            "sounds_found": [],
            "top_videos": [],
        }

        try:
            # Navigate to hashtag page
            url = f"https://www.tiktok.com/tag/{hashtag}"
            self.page.goto(url, wait_until="networkidle", timeout=45000)
            self.human_delay(3, 5)

            # Check if page loaded (TikTok can be finicky)
            if "captcha" in self.page.content().lower():
                logger.warning(f"Captcha detected for #{hashtag}")
                self.stats["errors"] += 1
                return result

            logger.info(f"Scraping #{hashtag}...")

            # Get hashtag stats if available
            view_count = ""
            video_count = ""

            try:
                # Try to get view count from header
                stats_elem = self.page.locator('[data-e2e="hashtag-view-count"], .challenge-stats')
                if stats_elem.count():
                    view_count = stats_elem.inner_text()
            except:
                pass

            # Scroll to load more videos
            self.scroll_feed(times=3)

            # Find video cards
            video_cards = self.page.locator('[data-e2e="challenge-item"], div[class*="DivItemContainer"]').all()

            sample_videos = []

            for i, card in enumerate(video_cards[:self.max_videos]):
                if i >= self.max_videos:
                    break

                try:
                    # Get video link
                    link_elem = card.locator('a')
                    video_url = link_elem.get_attribute('href') if link_elem.count() else ""

                    if video_url and not video_url.startswith('http'):
                        video_url = f"https://www.tiktok.com{video_url}"

                    if video_url:
                        sample_videos.append(video_url)
                        result["videos_found"] += 1

                    # Try to get engagement metrics
                    try:
                        views_elem = card.locator('[data-e2e="video-views"], strong')
                        if views_elem.count():
                            views = views_elem.first.inner_text()
                    except:
                        views = ""

                    self.stats["videos_analyzed"] += 1

                except Exception as e:
                    logger.debug(f"Error processing video card: {e}")
                    continue

            # Log hashtag
            log_hashtag(
                hashtag=hashtag,
                hashtag_url=url,
                view_count=view_count,
                video_count=str(result["videos_found"]),
                sample_videos=sample_videos
            )

            result["top_videos"] = sample_videos
            self.stats["hashtags_scraped"] += 1

            logger.info(f"#{hashtag}: found {result['videos_found']} videos")
            return result

        except Exception as e:
            logger.error(f"Error scraping #{hashtag}: {e}")
            self.stats["errors"] += 1
            return result

    def scrape_discover_page(self) -> List[Dict[str, str]]:
        """
        Scrape the discover/trending page for current trends.

        Returns:
            List of trending items
        """
        trends = []

        try:
            self.page.goto("https://www.tiktok.com/explore", wait_until="networkidle", timeout=45000)
            self.human_delay(3, 5)

            logger.info("Scraping discover page...")

            # Scroll to load content
            self.scroll_feed(times=2)

            # Find trending sections
            # TikTok structure changes frequently, so we cast a wide net
            trend_cards = self.page.locator('[class*="trending"], [class*="discover-item"]').all()

            for card in trend_cards[:20]:
                try:
                    # Try to extract trend info
                    text = card.inner_text()
                    link = card.locator('a').get_attribute('href') if card.locator('a').count() else ""

                    if text and link:
                        trend = {
                            "name": text[:100],
                            "url": link if link.startswith('http') else f"https://www.tiktok.com{link}",
                        }
                        trends.append(trend)

                except Exception as e:
                    continue

            logger.info(f"Found {len(trends)} trending items")
            return trends

        except Exception as e:
            logger.error(f"Error scraping discover page: {e}")
            self.stats["errors"] += 1
            return trends

    def analyze_video(self, video_url: str) -> Optional[Dict[str, Any]]:
        """
        Analyze a single video for patterns.

        Args:
            video_url: TikTok video URL

        Returns:
            Dict with video analysis or None
        """
        try:
            self.page.goto(video_url, wait_until="networkidle", timeout=45000)
            self.human_delay(2, 4)

            # Get video description
            desc_elem = self.page.locator('[data-e2e="browse-video-desc"], [class*="DivContainer"]')
            description = desc_elem.inner_text() if desc_elem.count() else ""

            # Get engagement
            likes = ""
            try:
                likes_elem = self.page.locator('[data-e2e="like-count"]')
                likes = likes_elem.inner_text() if likes_elem.count() else ""
            except:
                pass

            # Get sound info
            sound_name = ""
            try:
                sound_elem = self.page.locator('[data-e2e="browse-music"], [class*="music-info"]')
                sound_name = sound_elem.inner_text() if sound_elem.count() else ""
            except:
                pass

            # Analyze patterns
            hook_type = detect_hook_type(description)
            format_type = detect_format_type({})

            analysis = {
                "url": video_url,
                "description": description[:500],
                "likes": likes,
                "sound": sound_name,
                "hook_type": hook_type,
                "format_type": format_type,
            }

            # Log pattern
            log_content_pattern(
                video_url=video_url,
                hook_type=hook_type,
                format_type=format_type,
                description=description,
                engagement=likes
            )
            self.stats["patterns_logged"] += 1

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing video: {e}")
            return None

    def run(self) -> Dict[str, Any]:
        """
        Run scraping session.

        Returns:
            Summary statistics
        """
        result = {
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "hashtags_scraped": 0,
            "videos_analyzed": 0,
            "sounds_found": 0,
            "patterns_logged": 0,
            "errors": 0,
        }

        try:
            self._start_browser()

            # Build hashtag list from config or niches
            all_hashtags = list(self.hashtags)

            for niche in self.niches:
                if niche in NICHE_HASHTAGS:
                    all_hashtags.extend(NICHE_HASHTAGS[niche])

            # Remove duplicates
            all_hashtags = list(set(all_hashtags))

            logger.info(f"Starting scrape: {len(all_hashtags)} hashtags")

            # Scrape each hashtag
            for hashtag in all_hashtags:
                self.scrape_hashtag(hashtag)
                self.human_delay(8, 15)  # Longer delay between hashtags

            # Scrape discover page
            self.scrape_discover_page()

            # Build result
            result["success"] = True
            result["hashtags_scraped"] = self.stats["hashtags_scraped"]
            result["videos_analyzed"] = self.stats["videos_analyzed"]
            result["sounds_found"] = self.stats["sounds_found"]
            result["patterns_logged"] = self.stats["patterns_logged"]
            result["errors"] = self.stats["errors"]

            logger.info(
                f"Scrape complete: {result['hashtags_scraped']} hashtags, "
                f"{result['videos_analyzed']} videos"
            )

            return result

        except Exception as e:
            logger.error(f"Scraping session failed: {e}")
            result["errors"] += 1
            return result

        finally:
            self._stop_browser()


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Scrape TikTok for trending sounds, hashtags, and content patterns"
    )
    parser.add_argument(
        "--hashtags", "-t",
        help="Comma-separated list of hashtags to scrape (no #)"
    )
    parser.add_argument(
        "--niches", "-n",
        help="Comma-separated list of niches: business, tech, faith, fitness"
    )
    parser.add_argument(
        "--max-videos", "-m",
        type=int,
        default=20,
        help="Max videos per hashtag (default: 20)"
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run with visible browser"
    )
    parser.add_argument(
        "--proxy",
        help="Proxy server URL (recommended for TikTok)"
    )

    args = parser.parse_args()

    # Build config
    config = {
        "max_videos": args.max_videos,
        "headless": not args.headed,
    }

    # Hashtags
    if args.hashtags:
        config["hashtags"] = [h.strip().replace('#', '') for h in args.hashtags.split(",")]
    else:
        config["hashtags"] = []

    # Niches
    if args.niches:
        config["niches"] = [n.strip() for n in args.niches.split(",")]
    else:
        config["niches"] = ["business"]

    # Proxy (strongly recommended)
    if args.proxy:
        config["proxy"] = {"server": args.proxy}
    else:
        logger.warning("No proxy configured. TikTok may block your IP.")

    # Run
    scraper = TikTokScraper(config)
    result = scraper.run()

    # Output
    print(json.dumps(result, indent=2))
    print(f"\nTrends logged to: {TRENDS_CSV}")
    print(f"Sounds logged to: {SOUNDS_CSV}")
    print(f"Hashtags logged to: {HASHTAGS_CSV}")
    print(f"Patterns logged to: {CONTENT_PATTERNS_CSV}")
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
