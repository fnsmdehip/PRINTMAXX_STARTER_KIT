#!/usr/bin/env python3
"""
Twitter/X Scraper - Playwright-based scraper for X.com
Extracts tweets from tracked accounts with proxy support.
Parses for tools, tactics, numbers.
Handles rate limits and anti-bot measures.

Usage:
    scraper = TwitterScraper(headless=True, proxy_config={...})
    await scraper.initialize()
    tweets = await scraper.scrape_account('https://x.com/levelsio', max_tweets=10)
    await scraper.close()
"""

import asyncio
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

try:
    from playwright.async_api import async_playwright, Browser, Page, BrowserContext
except ImportError:
    raise ImportError("Playwright not installed. Run: pip install playwright && playwright install chromium")

logger = logging.getLogger('TwitterScraper')


class TwitterScraper:
    """Playwright-based Twitter/X scraper with proxy support."""

    def __init__(
        self,
        headless: bool = True,
        proxy_config: Optional[dict] = None,
        user_agent: Optional[str] = None,
        timeout: int = 30000
    ):
        self.headless = headless
        self.proxy_config = proxy_config or {}
        self.timeout = timeout
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )

        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

        # Rate limiting
        self._last_request = None
        self._min_delay = 2.0  # Minimum seconds between requests

    async def initialize(self):
        """Initialize browser and context."""
        self._playwright = await async_playwright().start()

        # Browser launch options
        launch_options = {
            'headless': self.headless,
            'args': [
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--no-sandbox'
            ]
        }

        # Add proxy if configured
        if self.proxy_config.get('server'):
            launch_options['proxy'] = {
                'server': self.proxy_config['server']
            }
            if self.proxy_config.get('username'):
                launch_options['proxy']['username'] = self.proxy_config['username']
                launch_options['proxy']['password'] = self.proxy_config.get('password', '')

        self._browser = await self._playwright.chromium.launch(**launch_options)

        # Create context with stealth settings
        self._context = await self._browser.new_context(
            user_agent=self.user_agent,
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/New_York',
            java_script_enabled=True,
            ignore_https_errors=True
        )

        # Add stealth scripts
        await self._context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        """)

        self._page = await self._context.new_page()
        self._page.set_default_timeout(self.timeout)

        logger.info("Twitter scraper initialized")

    async def close(self):
        """Close browser and cleanup."""
        if self._page:
            await self._page.close()
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

        logger.info("Twitter scraper closed")

    async def _rate_limit(self):
        """Enforce rate limiting between requests."""
        if self._last_request:
            elapsed = (datetime.now() - self._last_request).total_seconds()
            if elapsed < self._min_delay:
                await asyncio.sleep(self._min_delay - elapsed)
        self._last_request = datetime.now()

    async def scrape_account(
        self,
        profile_url: str,
        max_tweets: int = 10,
        include_replies: bool = False
    ) -> list[dict]:
        """
        Scrape tweets from a Twitter/X profile.

        Args:
            profile_url: Full URL to X profile (e.g., https://x.com/levelsio)
            max_tweets: Maximum number of tweets to extract
            include_replies: Whether to include replies

        Returns:
            List of tweet dictionaries with text, engagement, url, timestamp
        """
        if not self._page:
            raise RuntimeError("Scraper not initialized. Call initialize() first.")

        await self._rate_limit()

        tweets = []
        handle = self._extract_handle(profile_url)

        try:
            logger.debug(f"Navigating to {profile_url}")
            await self._page.goto(profile_url, wait_until='networkidle')

            # Wait for tweets to load
            try:
                await self._page.wait_for_selector('[data-testid="tweet"]', timeout=10000)
            except Exception:
                logger.warning(f"No tweets found for {handle}")
                return tweets

            # Scroll to load more tweets
            scroll_attempts = 0
            while len(tweets) < max_tweets and scroll_attempts < 5:
                # Extract visible tweets
                tweet_elements = await self._page.query_selector_all('[data-testid="tweet"]')

                for element in tweet_elements:
                    if len(tweets) >= max_tweets:
                        break

                    try:
                        tweet_data = await self._extract_tweet(element, handle)
                        if tweet_data and tweet_data['url'] not in [t['url'] for t in tweets]:
                            # Skip replies unless requested
                            if not include_replies and tweet_data.get('is_reply'):
                                continue
                            tweets.append(tweet_data)
                    except Exception as e:
                        logger.debug(f"Error extracting tweet: {e}")
                        continue

                # Scroll down for more
                if len(tweets) < max_tweets:
                    await self._page.evaluate("window.scrollBy(0, 1000)")
                    await asyncio.sleep(1.5)
                    scroll_attempts += 1

            logger.info(f"Extracted {len(tweets)} tweets from {handle}")

        except Exception as e:
            logger.error(f"Error scraping {profile_url}: {e}")
            raise

        return tweets

    async def _extract_tweet(self, element, handle: str) -> Optional[dict]:
        """Extract data from a single tweet element."""
        try:
            # Get tweet text
            text_element = await element.query_selector('[data-testid="tweetText"]')
            text = await text_element.inner_text() if text_element else ""

            if not text or len(text) < 20:
                return None

            # Get timestamp and link
            time_element = await element.query_selector('time')
            timestamp = ""
            tweet_url = ""

            if time_element:
                timestamp = await time_element.get_attribute('datetime') or ""
                parent_link = await time_element.query_selector('xpath=ancestor::a')
                if parent_link:
                    href = await parent_link.get_attribute('href')
                    if href and '/status/' in href:
                        tweet_url = f"https://x.com{href}" if not href.startswith('http') else href

            # Get engagement metrics
            engagement = await self._extract_engagement(element)

            # Check if reply
            reply_indicator = await element.query_selector('[data-testid="socialContext"]')
            is_reply = reply_indicator is not None

            return {
                'text': text.strip(),
                'url': tweet_url,
                'timestamp': timestamp,
                'handle': handle,
                'likes': engagement.get('likes', 0),
                'retweets': engagement.get('retweets', 0),
                'replies': engagement.get('replies', 0),
                'views': engagement.get('views', 0),
                'is_reply': is_reply
            }

        except Exception as e:
            logger.debug(f"Tweet extraction error: {e}")
            return None

    async def _extract_engagement(self, element) -> dict:
        """Extract engagement metrics from tweet element."""
        engagement = {'likes': 0, 'retweets': 0, 'replies': 0, 'views': 0}

        try:
            # Like count
            like_element = await element.query_selector('[data-testid="like"] span span')
            if like_element:
                engagement['likes'] = self._parse_count(await like_element.inner_text())

            # Retweet count
            retweet_element = await element.query_selector('[data-testid="retweet"] span span')
            if retweet_element:
                engagement['retweets'] = self._parse_count(await retweet_element.inner_text())

            # Reply count
            reply_element = await element.query_selector('[data-testid="reply"] span span')
            if reply_element:
                engagement['replies'] = self._parse_count(await reply_element.inner_text())

            # View count (newer Twitter)
            view_element = await element.query_selector('[data-testid="app-text-transition-container"] span')
            if view_element:
                engagement['views'] = self._parse_count(await view_element.inner_text())

        except Exception as e:
            logger.debug(f"Engagement extraction error: {e}")

        return engagement

    @staticmethod
    def _parse_count(text: str) -> int:
        """Parse engagement count from text (e.g., '1.2K' -> 1200)."""
        if not text:
            return 0

        text = text.strip().upper()

        try:
            if 'K' in text:
                return int(float(text.replace('K', '').replace(',', '')) * 1000)
            elif 'M' in text:
                return int(float(text.replace('M', '').replace(',', '')) * 1000000)
            else:
                return int(text.replace(',', ''))
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def _extract_handle(url: str) -> str:
        """Extract handle from profile URL."""
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        # Handle URLs like x.com/user or x.com/user/status/123
        parts = path.split('/')
        return f"@{parts[0]}" if parts else url

    async def search_tweets(
        self,
        query: str,
        max_tweets: int = 20,
        sort: str = 'Top'
    ) -> list[dict]:
        """
        Search for tweets matching a query.

        Args:
            query: Search query string
            max_tweets: Maximum tweets to return
            sort: 'Top' or 'Latest'

        Returns:
            List of matching tweet dictionaries
        """
        if not self._page:
            raise RuntimeError("Scraper not initialized. Call initialize() first.")

        await self._rate_limit()

        # Encode query for URL
        encoded_query = query.replace(' ', '%20')
        search_url = f"https://x.com/search?q={encoded_query}&src=typed_query"

        if sort == 'Latest':
            search_url += '&f=live'

        tweets = []

        try:
            logger.debug(f"Searching: {query}")
            await self._page.goto(search_url, wait_until='networkidle')

            # Wait for results
            try:
                await self._page.wait_for_selector('[data-testid="tweet"]', timeout=10000)
            except Exception:
                logger.warning(f"No results for query: {query}")
                return tweets

            # Extract tweets
            tweet_elements = await self._page.query_selector_all('[data-testid="tweet"]')

            for element in tweet_elements[:max_tweets]:
                try:
                    tweet_data = await self._extract_tweet(element, "search")
                    if tweet_data:
                        tweets.append(tweet_data)
                except Exception as e:
                    logger.debug(f"Error extracting search result: {e}")

            logger.info(f"Found {len(tweets)} tweets for '{query}'")

        except Exception as e:
            logger.error(f"Search error: {e}")
            raise

        return tweets

    async def get_trending_topics(self) -> list[dict]:
        """Get current trending topics from X."""
        if not self._page:
            raise RuntimeError("Scraper not initialized. Call initialize() first.")

        await self._rate_limit()

        trends = []

        try:
            await self._page.goto('https://x.com/explore/tabs/trending', wait_until='networkidle')

            # Wait for trends to load
            await self._page.wait_for_selector('[data-testid="trend"]', timeout=10000)

            trend_elements = await self._page.query_selector_all('[data-testid="trend"]')

            for element in trend_elements[:20]:
                try:
                    # Get trend name
                    name_element = await element.query_selector('span')
                    if name_element:
                        name = await name_element.inner_text()
                        trends.append({
                            'name': name.strip(),
                            'timestamp': datetime.now().isoformat()
                        })
                except Exception:
                    continue

            logger.info(f"Found {len(trends)} trending topics")

        except Exception as e:
            logger.error(f"Error getting trends: {e}")

        return trends


# Standalone test
async def _test():
    """Test the Twitter scraper."""
    scraper = TwitterScraper(headless=False)
    try:
        await scraper.initialize()

        # Test profile scrape
        tweets = await scraper.scrape_account('https://x.com/levelsio', max_tweets=5)
        print(f"\n=== @levelsio tweets ({len(tweets)}) ===")
        for t in tweets:
            print(f"  - {t['text'][:80]}... ({t['likes']} likes)")

    finally:
        await scraper.close()


if __name__ == '__main__':
    asyncio.run(_test())
