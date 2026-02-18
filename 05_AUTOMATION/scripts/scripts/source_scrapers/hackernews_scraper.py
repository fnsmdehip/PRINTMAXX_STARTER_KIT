#!/usr/bin/env python3
"""
HackerNews Scraper - Playwright-based scraper for news.ycombinator.com
Scans front page and Show HN for new tools/launches.
Filters by points threshold.

Usage:
    scraper = HackerNewsScraper(headless=True)
    await scraper.initialize()
    items = await scraper.scrape_front_page(min_points=50)
    show_hn = await scraper.scrape_show_hn(min_points=20)
    await scraper.close()
"""

import asyncio
import logging
import re
from datetime import datetime
from typing import Optional, Literal

try:
    from playwright.async_api import async_playwright, Browser, Page, BrowserContext
except ImportError:
    raise ImportError("Playwright not installed. Run: pip install playwright && playwright install chromium")

logger = logging.getLogger('HackerNewsScraper')

# HN base URL
HN_BASE_URL = "https://news.ycombinator.com"


class HackerNewsScraper:
    """Playwright-based HackerNews scraper."""

    def __init__(
        self,
        headless: bool = True,
        timeout: int = 30000
    ):
        self.headless = headless
        self.timeout = timeout

        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

        # Rate limiting (HN is lenient but be respectful)
        self._last_request = None
        self._min_delay = 1.0

    async def initialize(self):
        """Initialize browser and context."""
        self._playwright = await async_playwright().start()

        self._browser = await self._playwright.chromium.launch(
            headless=self.headless,
            args=['--no-sandbox']
        )

        self._context = await self._browser.new_context(
            viewport={'width': 1200, 'height': 800},
            locale='en-US'
        )

        self._page = await self._context.new_page()
        self._page.set_default_timeout(self.timeout)

        logger.info("HackerNews scraper initialized")

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

        logger.info("HackerNews scraper closed")

    async def _rate_limit(self):
        """Enforce rate limiting between requests."""
        if self._last_request:
            elapsed = (datetime.now() - self._last_request).total_seconds()
            if elapsed < self._min_delay:
                await asyncio.sleep(self._min_delay - elapsed)
        self._last_request = datetime.now()

    async def scrape_front_page(
        self,
        min_points: int = 50,
        max_items: int = 30
    ) -> list[dict]:
        """
        Scrape the HackerNews front page.

        Args:
            min_points: Minimum points to include item
            max_items: Maximum items to return

        Returns:
            List of item dictionaries with title, url, points, comments
        """
        if not self._page:
            raise RuntimeError("Scraper not initialized. Call initialize() first.")

        await self._rate_limit()

        items = []

        try:
            logger.debug("Navigating to HN front page")
            await self._page.goto(f"{HN_BASE_URL}/news", wait_until='networkidle')

            # HN has a simple structure - each item is in a table row
            items = await self._extract_items(min_points, max_items)

            logger.info(f"Extracted {len(items)} items from front page")

        except Exception as e:
            logger.error(f"Error scraping front page: {e}")
            raise

        return items

    async def scrape_show_hn(
        self,
        min_points: int = 20,
        max_items: int = 20
    ) -> list[dict]:
        """
        Scrape Show HN section for new launches.

        Args:
            min_points: Minimum points to include item
            max_items: Maximum items to return

        Returns:
            List of Show HN items
        """
        if not self._page:
            raise RuntimeError("Scraper not initialized. Call initialize() first.")

        await self._rate_limit()

        items = []

        try:
            logger.debug("Navigating to Show HN")
            await self._page.goto(f"{HN_BASE_URL}/show", wait_until='networkidle')

            items = await self._extract_items(min_points, max_items)

            # Mark as Show HN
            for item in items:
                item['is_show_hn'] = True

            logger.info(f"Extracted {len(items)} items from Show HN")

        except Exception as e:
            logger.error(f"Error scraping Show HN: {e}")
            raise

        return items

    async def scrape_new(
        self,
        max_items: int = 30
    ) -> list[dict]:
        """
        Scrape newest submissions (no point filter since they're new).

        Args:
            max_items: Maximum items to return

        Returns:
            List of new items
        """
        if not self._page:
            raise RuntimeError("Scraper not initialized. Call initialize() first.")

        await self._rate_limit()

        items = []

        try:
            logger.debug("Navigating to HN newest")
            await self._page.goto(f"{HN_BASE_URL}/newest", wait_until='networkidle')

            items = await self._extract_items(min_points=0, max_items=max_items)

            logger.info(f"Extracted {len(items)} newest items")

        except Exception as e:
            logger.error(f"Error scraping newest: {e}")
            raise

        return items

    async def scrape_ask_hn(
        self,
        min_points: int = 20,
        max_items: int = 20
    ) -> list[dict]:
        """
        Scrape Ask HN section.

        Args:
            min_points: Minimum points to include
            max_items: Maximum items to return

        Returns:
            List of Ask HN items
        """
        if not self._page:
            raise RuntimeError("Scraper not initialized. Call initialize() first.")

        await self._rate_limit()

        items = []

        try:
            logger.debug("Navigating to Ask HN")
            await self._page.goto(f"{HN_BASE_URL}/ask", wait_until='networkidle')

            items = await self._extract_items(min_points, max_items)

            for item in items:
                item['is_ask_hn'] = True

            logger.info(f"Extracted {len(items)} items from Ask HN")

        except Exception as e:
            logger.error(f"Error scraping Ask HN: {e}")
            raise

        return items

    async def _extract_items(
        self,
        min_points: int,
        max_items: int
    ) -> list[dict]:
        """Extract items from current HN page."""
        items = []

        # HN structure: alternating rows for title and subtext
        # .athing = title row, .subtext = meta row
        title_rows = await self._page.query_selector_all('.athing')

        for row in title_rows[:max_items * 2]:  # Get extra in case some are filtered
            if len(items) >= max_items:
                break

            try:
                item = await self._extract_single_item(row)
                if item and item.get('points', 0) >= min_points:
                    items.append(item)
            except Exception as e:
                logger.debug(f"Error extracting item: {e}")
                continue

        return items

    async def _extract_single_item(self, row) -> Optional[dict]:
        """Extract data from a single HN item row."""
        try:
            # Get item ID
            item_id = await row.get_attribute('id')
            if not item_id:
                return None

            # Get title and link
            title_element = await row.query_selector('.titleline > a')
            if not title_element:
                return None

            title = await title_element.inner_text()
            link = await title_element.get_attribute('href')

            # Handle relative links
            if link and not link.startswith('http'):
                link = f"{HN_BASE_URL}/{link}"

            # Get domain (if external link)
            domain_element = await row.query_selector('.sitestr')
            domain = await domain_element.inner_text() if domain_element else ""

            # Get subtext row (next sibling row with meta info)
            subtext = await self._page.query_selector(f'#score_{item_id}')
            points = 0
            if subtext:
                points_text = await subtext.inner_text()
                points_match = re.search(r'(\d+)\s*point', points_text)
                if points_match:
                    points = int(points_match.group(1))

            # Get comments count
            comments = 0
            comment_link = await self._page.query_selector(
                f'.athing#{item_id} + tr .subline a:last-child'
            )
            if comment_link:
                comment_text = await comment_link.inner_text()
                comment_match = re.search(r'(\d+)\s*comment', comment_text)
                if comment_match:
                    comments = int(comment_match.group(1))

            # Get age
            age_element = await self._page.query_selector(
                f'.athing#{item_id} + tr .age'
            )
            timestamp = ""
            if age_element:
                timestamp = await age_element.inner_text()

            # Build HN discussion URL
            hn_url = f"{HN_BASE_URL}/item?id={item_id}"

            return {
                'id': item_id,
                'title': title.strip(),
                'url': link or hn_url,  # Use HN discussion if no external link
                'hn_url': hn_url,
                'domain': domain,
                'points': points,
                'comments': comments,
                'timestamp': timestamp,
                'scraped_at': datetime.now().isoformat(),
                'is_show_hn': title.lower().startswith('show hn:'),
                'is_ask_hn': title.lower().startswith('ask hn:')
            }

        except Exception as e:
            logger.debug(f"Item extraction error: {e}")
            return None

    async def get_item_comments(
        self,
        item_id: str,
        max_comments: int = 10
    ) -> list[dict]:
        """
        Get comments for a specific HN item.

        Args:
            item_id: HN item ID
            max_comments: Maximum comments to return

        Returns:
            List of comment dictionaries
        """
        if not self._page:
            raise RuntimeError("Scraper not initialized. Call initialize() first.")

        await self._rate_limit()

        comments = []

        try:
            logger.debug(f"Fetching comments for item {item_id}")
            await self._page.goto(
                f"{HN_BASE_URL}/item?id={item_id}",
                wait_until='networkidle'
            )

            # Get comment elements
            comment_elements = await self._page.query_selector_all('.comment')

            for element in comment_elements[:max_comments]:
                try:
                    # Get comment text
                    text_element = await element.query_selector('.commtext')
                    text = await text_element.inner_text() if text_element else ""

                    # Get author
                    author_element = await element.query_selector('.hnuser')
                    author = await author_element.inner_text() if author_element else ""

                    comments.append({
                        'text': text.strip()[:1000],
                        'author': author,
                        'item_id': item_id
                    })

                except Exception:
                    continue

            logger.info(f"Extracted {len(comments)} comments for item {item_id}")

        except Exception as e:
            logger.error(f"Error getting comments: {e}")

        return comments

    async def search_hn(
        self,
        query: str,
        max_items: int = 20,
        search_type: Literal['story', 'comment', 'all'] = 'story'
    ) -> list[dict]:
        """
        Search HackerNews using Algolia API (via hn.algolia.com).

        Args:
            query: Search query
            max_items: Maximum items to return
            search_type: Type of content to search

        Returns:
            List of matching items
        """
        if not self._page:
            raise RuntimeError("Scraper not initialized. Call initialize() first.")

        await self._rate_limit()

        items = []

        try:
            # Use Algolia HN search
            encoded_query = query.replace(' ', '%20')
            tags = ""
            if search_type == 'story':
                tags = "&tags=story"
            elif search_type == 'comment':
                tags = "&tags=comment"

            search_url = f"https://hn.algolia.com/?q={encoded_query}{tags}"

            logger.debug(f"Searching HN: {query}")
            await self._page.goto(search_url, wait_until='networkidle')

            # Wait for results
            await self._page.wait_for_selector('.Story, .Comment', timeout=10000)

            # Extract results
            result_elements = await self._page.query_selector_all('.Story, .Comment')

            for element in result_elements[:max_items]:
                try:
                    # Get title
                    title_element = await element.query_selector('.Story_title a, .Story_link')
                    title = await title_element.inner_text() if title_element else ""

                    # Get link
                    link = ""
                    if title_element:
                        link = await title_element.get_attribute('href')

                    # Get points
                    points_element = await element.query_selector('.Story_meta')
                    points = 0
                    if points_element:
                        meta_text = await points_element.inner_text()
                        points_match = re.search(r'(\d+)\s*point', meta_text)
                        if points_match:
                            points = int(points_match.group(1))

                    if title:
                        items.append({
                            'title': title.strip(),
                            'url': link,
                            'points': points,
                            'timestamp': datetime.now().isoformat()
                        })

                except Exception:
                    continue

            logger.info(f"Found {len(items)} results for '{query}'")

        except Exception as e:
            logger.error(f"Search error: {e}")

        return items


# Standalone test
async def _test():
    """Test the HackerNews scraper."""
    scraper = HackerNewsScraper(headless=False)
    try:
        await scraper.initialize()

        # Test front page
        print("\n=== Front Page ===")
        items = await scraper.scrape_front_page(min_points=100, max_items=5)
        for item in items:
            print(f"  [{item['points']}] {item['title'][:50]}...")

        # Test Show HN
        print("\n=== Show HN ===")
        show_items = await scraper.scrape_show_hn(min_points=10, max_items=5)
        for item in show_items:
            print(f"  [{item['points']}] {item['title'][:50]}...")

    finally:
        await scraper.close()


if __name__ == '__main__':
    asyncio.run(_test())
