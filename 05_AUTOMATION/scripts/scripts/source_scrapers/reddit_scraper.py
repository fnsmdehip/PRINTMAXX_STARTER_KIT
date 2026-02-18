#!/usr/bin/env python3
"""
Reddit Scraper - Playwright-based scraper for Reddit
Scans specified subreddits (SideProject, startups, Entrepreneur, etc.)
Extracts high-engagement posts and filters for actionable tactics.

Usage:
    scraper = RedditScraper(headless=True)
    await scraper.initialize()
    posts = await scraper.scrape_subreddit('https://reddit.com/r/SideProject', max_posts=10)
    await scraper.close()
"""

import asyncio
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Literal
from urllib.parse import urlparse

try:
    from playwright.async_api import async_playwright, Browser, Page, BrowserContext
except ImportError:
    raise ImportError("Playwright not installed. Run: pip install playwright && playwright install chromium")

logger = logging.getLogger('RedditScraper')


class RedditScraper:
    """Playwright-based Reddit scraper."""

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
        self._min_delay = 3.0  # Reddit is stricter

    async def initialize(self):
        """Initialize browser and context."""
        self._playwright = await async_playwright().start()

        launch_options = {
            'headless': self.headless,
            'args': [
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox'
            ]
        }

        if self.proxy_config.get('server'):
            launch_options['proxy'] = {
                'server': self.proxy_config['server']
            }
            if self.proxy_config.get('username'):
                launch_options['proxy']['username'] = self.proxy_config['username']
                launch_options['proxy']['password'] = self.proxy_config.get('password', '')

        self._browser = await self._playwright.chromium.launch(**launch_options)

        self._context = await self._browser.new_context(
            user_agent=self.user_agent,
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/New_York'
        )

        # Stealth mode
        await self._context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)

        self._page = await self._context.new_page()
        self._page.set_default_timeout(self.timeout)

        logger.info("Reddit scraper initialized")

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

        logger.info("Reddit scraper closed")

    async def _rate_limit(self):
        """Enforce rate limiting between requests."""
        if self._last_request:
            elapsed = (datetime.now() - self._last_request).total_seconds()
            if elapsed < self._min_delay:
                await asyncio.sleep(self._min_delay - elapsed)
        self._last_request = datetime.now()

    async def scrape_subreddit(
        self,
        subreddit_url: str,
        max_posts: int = 10,
        sort: Literal['hot', 'new', 'top', 'rising'] = 'hot',
        time_filter: Literal['hour', 'day', 'week', 'month', 'year', 'all'] = 'week',
        min_upvotes: int = 10
    ) -> list[dict]:
        """
        Scrape posts from a subreddit.

        Args:
            subreddit_url: Full URL or subreddit name (e.g., r/SideProject)
            max_posts: Maximum number of posts to extract
            sort: Sort order (hot, new, top, rising)
            time_filter: Time filter for 'top' sort
            min_upvotes: Minimum upvotes to include post

        Returns:
            List of post dictionaries
        """
        if not self._page:
            raise RuntimeError("Scraper not initialized. Call initialize() first.")

        await self._rate_limit()

        # Normalize URL
        if not subreddit_url.startswith('http'):
            subreddit_url = f"https://reddit.com{subreddit_url}"

        # Add sort parameter
        if sort:
            base_url = subreddit_url.rstrip('/')
            if sort == 'top':
                url = f"{base_url}/top/?t={time_filter}"
            else:
                url = f"{base_url}/{sort}/"
        else:
            url = subreddit_url

        posts = []
        subreddit_name = self._extract_subreddit(subreddit_url)

        try:
            logger.debug(f"Navigating to {url}")
            await self._page.goto(url, wait_until='networkidle')

            # Wait for posts to load (new Reddit)
            try:
                await self._page.wait_for_selector(
                    'shreddit-post, [data-testid="post-container"], article',
                    timeout=10000
                )
            except Exception:
                logger.warning(f"No posts found for {subreddit_name}")
                return posts

            # Extract posts
            scroll_attempts = 0
            while len(posts) < max_posts and scroll_attempts < 5:
                post_elements = await self._page.query_selector_all(
                    'shreddit-post, [data-testid="post-container"], article'
                )

                for element in post_elements:
                    if len(posts) >= max_posts:
                        break

                    try:
                        post_data = await self._extract_post(element, subreddit_name)
                        if post_data and post_data['url'] not in [p['url'] for p in posts]:
                            # Apply upvote filter
                            if post_data['upvotes'] >= min_upvotes:
                                posts.append(post_data)
                    except Exception as e:
                        logger.debug(f"Error extracting post: {e}")

                # Scroll for more posts
                if len(posts) < max_posts:
                    await self._page.evaluate("window.scrollBy(0, 1000)")
                    await asyncio.sleep(2)
                    scroll_attempts += 1

            logger.info(f"Extracted {len(posts)} posts from {subreddit_name}")

        except Exception as e:
            logger.error(f"Error scraping {subreddit_url}: {e}")
            raise

        return posts

    async def _extract_post(self, element, subreddit: str) -> Optional[dict]:
        """Extract data from a single post element."""
        try:
            # Try new Reddit (shreddit-post) first
            is_shreddit = 'shreddit-post' in (await element.evaluate('e => e.tagName.toLowerCase()') or '')

            if is_shreddit:
                return await self._extract_shreddit_post(element, subreddit)
            else:
                return await self._extract_classic_post(element, subreddit)

        except Exception as e:
            logger.debug(f"Post extraction error: {e}")
            return None

    async def _extract_shreddit_post(self, element, subreddit: str) -> Optional[dict]:
        """Extract from new Reddit shreddit-post element."""
        try:
            # Get title
            title_element = await element.query_selector('[slot="title"], h1, h3')
            title = await title_element.inner_text() if title_element else ""

            if not title or len(title) < 10:
                return None

            # Get post URL
            permalink = await element.get_attribute('permalink')
            post_url = f"https://reddit.com{permalink}" if permalink else ""

            # Get upvotes
            score_element = await element.query_selector('faceplate-number, [data-click-id="upvote"] ~ *')
            upvotes = 0
            if score_element:
                score_text = await score_element.inner_text()
                upvotes = self._parse_count(score_text)

            # Get comment count
            comment_element = await element.query_selector('[slot="commentCount"], [data-click-id="comments"]')
            comments = 0
            if comment_element:
                comment_text = await comment_element.inner_text()
                comments = self._parse_count(comment_text)

            # Get post body (if visible)
            body_element = await element.query_selector('[slot="text-body"], .RichTextJSON-root')
            body = await body_element.inner_text() if body_element else ""

            return {
                'title': title.strip(),
                'body': body.strip()[:2000] if body else "",
                'url': post_url,
                'subreddit': subreddit,
                'upvotes': upvotes,
                'comments': comments,
                'upvote_ratio': 0.0,  # Not easily available
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.debug(f"Shreddit extraction error: {e}")
            return None

    async def _extract_classic_post(self, element, subreddit: str) -> Optional[dict]:
        """Extract from classic Reddit post container."""
        try:
            # Get title
            title_element = await element.query_selector('h3, a[data-click-id="body"]')
            title = await title_element.inner_text() if title_element else ""

            if not title or len(title) < 10:
                return None

            # Get post link
            link_element = await element.query_selector('a[href*="/comments/"]')
            post_url = ""
            if link_element:
                href = await link_element.get_attribute('href')
                if href:
                    post_url = f"https://reddit.com{href}" if not href.startswith('http') else href

            # Get score
            score_element = await element.query_selector('[class*="score"], [data-testid="score"]')
            upvotes = 0
            if score_element:
                upvotes = self._parse_count(await score_element.inner_text())

            # Get comments
            comment_element = await element.query_selector('[data-click-id="comments"]')
            comments = 0
            if comment_element:
                comments = self._parse_count(await comment_element.inner_text())

            return {
                'title': title.strip(),
                'body': "",
                'url': post_url,
                'subreddit': subreddit,
                'upvotes': upvotes,
                'comments': comments,
                'upvote_ratio': 0.0,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.debug(f"Classic extraction error: {e}")
            return None

    async def get_post_content(self, post_url: str) -> Optional[dict]:
        """
        Get full content of a specific post.

        Args:
            post_url: Full URL to the Reddit post

        Returns:
            Post dictionary with full body text
        """
        if not self._page:
            raise RuntimeError("Scraper not initialized. Call initialize() first.")

        await self._rate_limit()

        try:
            logger.debug(f"Fetching post: {post_url}")
            await self._page.goto(post_url, wait_until='networkidle')

            # Wait for content
            await self._page.wait_for_selector(
                '[slot="text-body"], .Post, [data-testid="post-content"]',
                timeout=10000
            )

            # Get title
            title_element = await self._page.query_selector('h1, [slot="title"]')
            title = await title_element.inner_text() if title_element else ""

            # Get body
            body_element = await self._page.query_selector(
                '[slot="text-body"], .RichTextJSON-root, [data-testid="post-content"]'
            )
            body = await body_element.inner_text() if body_element else ""

            # Get score
            score_element = await self._page.query_selector('faceplate-number, [class*="score"]')
            upvotes = 0
            if score_element:
                upvotes = self._parse_count(await score_element.inner_text())

            return {
                'title': title.strip(),
                'body': body.strip()[:5000],
                'url': post_url,
                'upvotes': upvotes,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error fetching post content: {e}")
            return None

    async def search_reddit(
        self,
        query: str,
        subreddit: Optional[str] = None,
        max_posts: int = 20,
        sort: Literal['relevance', 'hot', 'top', 'new', 'comments'] = 'relevance',
        time_filter: Literal['hour', 'day', 'week', 'month', 'year', 'all'] = 'week'
    ) -> list[dict]:
        """
        Search Reddit for posts matching a query.

        Args:
            query: Search query string
            subreddit: Limit to specific subreddit (optional)
            max_posts: Maximum posts to return
            sort: Sort order
            time_filter: Time filter for results

        Returns:
            List of matching post dictionaries
        """
        if not self._page:
            raise RuntimeError("Scraper not initialized. Call initialize() first.")

        await self._rate_limit()

        # Build search URL
        encoded_query = query.replace(' ', '%20')
        if subreddit:
            search_url = f"https://reddit.com/r/{subreddit}/search/?q={encoded_query}&restrict_sr=1&sort={sort}&t={time_filter}"
        else:
            search_url = f"https://reddit.com/search/?q={encoded_query}&sort={sort}&t={time_filter}"

        posts = []

        try:
            logger.debug(f"Searching: {query}")
            await self._page.goto(search_url, wait_until='networkidle')

            # Wait for results
            try:
                await self._page.wait_for_selector(
                    'shreddit-post, [data-testid="post-container"]',
                    timeout=10000
                )
            except Exception:
                logger.warning(f"No results for: {query}")
                return posts

            # Extract results
            post_elements = await self._page.query_selector_all(
                'shreddit-post, [data-testid="post-container"]'
            )

            for element in post_elements[:max_posts]:
                try:
                    post_data = await self._extract_post(element, subreddit or "search")
                    if post_data:
                        posts.append(post_data)
                except Exception:
                    continue

            logger.info(f"Found {len(posts)} results for '{query}'")

        except Exception as e:
            logger.error(f"Search error: {e}")
            raise

        return posts

    @staticmethod
    def _parse_count(text: str) -> int:
        """Parse count from text (e.g., '1.2k' -> 1200)."""
        if not text:
            return 0

        text = text.strip().lower()

        # Extract numbers
        match = re.search(r'([\d.]+)\s*([km])?', text)
        if not match:
            return 0

        try:
            num = float(match.group(1))
            suffix = match.group(2)

            if suffix == 'k':
                return int(num * 1000)
            elif suffix == 'm':
                return int(num * 1000000)
            else:
                return int(num)
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def _extract_subreddit(url: str) -> str:
        """Extract subreddit name from URL."""
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        parts = path.split('/')

        for i, part in enumerate(parts):
            if part == 'r' and i + 1 < len(parts):
                return f"r/{parts[i + 1]}"

        return url


# Standalone test
async def _test():
    """Test the Reddit scraper."""
    scraper = RedditScraper(headless=False)
    try:
        await scraper.initialize()

        # Test subreddit scrape
        posts = await scraper.scrape_subreddit(
            'https://reddit.com/r/SideProject',
            max_posts=5,
            sort='hot'
        )
        print(f"\n=== r/SideProject posts ({len(posts)}) ===")
        for p in posts:
            print(f"  - [{p['upvotes']}] {p['title'][:60]}...")

    finally:
        await scraper.close()


if __name__ == '__main__':
    asyncio.run(_test())
