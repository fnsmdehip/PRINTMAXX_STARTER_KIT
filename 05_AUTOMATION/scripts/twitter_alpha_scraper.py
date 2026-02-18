#!/usr/bin/env python3
"""
Twitter Alpha Scraper - Automated bookmark and high-signal account extraction
Uses existing Chrome profile to avoid login/permissions

Usage:
    python3 twitter_alpha_scraper.py --bookmarks
    python3 twitter_alpha_scraper.py --accounts
    python3 twitter_alpha_scraper.py --all
"""

import asyncio
import json
import csv
import re
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright
import argparse

# Paths
PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_DIR / "LEDGER"
ALPHA_STAGING = LEDGER_DIR / "ALPHA_STAGING.csv"
HIGH_SIGNAL_SOURCES = LEDGER_DIR / "HIGH_SIGNAL_SOURCES.csv"
OUTPUT_DIR = PROJECT_DIR / "AUTOMATIONS" / "twitter_scraper_output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Chrome profile path (macOS default)
CHROME_USER_DATA = Path.home() / "Library/Application Support/Google/Chrome"

class TwitterScraper:
    def __init__(self):
        self.existing_urls = self.load_existing_urls()
        self.next_alpha_id = self.get_next_alpha_id()

    def load_existing_urls(self):
        """Load existing source URLs to avoid duplicates"""
        urls = set()
        if ALPHA_STAGING.exists():
            with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('source_url'):
                        urls.add(row['source_url'])
        return urls

    def get_next_alpha_id(self):
        """Get next available ALPHA ID"""
        max_id = 0
        if ALPHA_STAGING.exists():
            with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    alpha_id = row.get('alpha_id', '')
                    match = re.match(r'ALPHA(\d+)', alpha_id)
                    if match:
                        max_id = max(max_id, int(match.group(1)))
        return max_id + 1

    async def scrape_bookmarks(self, page):
        """Scrape Twitter bookmarks"""
        print("📚 Navigating to Twitter bookmarks...")
        await page.goto("https://x.com/i/bookmarks", wait_until="networkidle")
        await asyncio.sleep(3)

        bookmarks = []
        seen_urls = set()
        scroll_attempts = 0
        max_scrolls = 20

        print("📜 Scrolling and extracting bookmarks...")

        while scroll_attempts < max_scrolls:
            # Extract tweets on current viewport
            tweets = await page.query_selector_all('article[data-testid="tweet"]')

            for tweet in tweets:
                try:
                    # Extract tweet URL
                    link = await tweet.query_selector('a[href*="/status/"]')
                    if link:
                        href = await link.get_attribute('href')
                        full_url = f"https://x.com{href}" if href.startswith('/') else href

                        # Skip if already seen or in existing alpha
                        if full_url in seen_urls or full_url in self.existing_urls:
                            continue

                        seen_urls.add(full_url)

                        # Extract text content
                        text_elem = await tweet.query_selector('[data-testid="tweetText"]')
                        text = await text_elem.inner_text() if text_elem else ""

                        # Only keep if it looks like business/tech content
                        if self.is_business_content(text):
                            bookmarks.append({
                                'url': full_url,
                                'text': text,
                                'handle': self.extract_handle(href)
                            })
                            print(f"  ✓ Found: {full_url[:60]}...")

                except Exception as e:
                    continue

            # Scroll down
            await page.evaluate("window.scrollBy(0, 1000)")
            await asyncio.sleep(2)
            scroll_attempts += 1

            print(f"  Scrolled {scroll_attempts}/{max_scrolls}, found {len(bookmarks)} new bookmarks")

        return bookmarks

    async def scrape_account(self, page, handle):
        """Scrape recent posts from a Twitter account"""
        print(f"🔍 Scraping @{handle}...")
        await page.goto(f"https://x.com/{handle}", wait_until="networkidle")
        await asyncio.sleep(3)

        posts = []
        seen_urls = set()
        scroll_attempts = 0
        max_scrolls = 5  # Fewer scrolls per account

        while scroll_attempts < max_scrolls:
            tweets = await page.query_selector_all('article[data-testid="tweet"]')

            for tweet in tweets:
                try:
                    link = await tweet.query_selector('a[href*="/status/"]')
                    if link:
                        href = await link.get_attribute('href')
                        full_url = f"https://x.com{href}" if href.startswith('/') else href

                        if full_url in seen_urls or full_url in self.existing_urls:
                            continue

                        seen_urls.add(full_url)

                        text_elem = await tweet.query_selector('[data-testid="tweetText"]')
                        text = await text_elem.inner_text() if text_elem else ""

                        if self.is_business_content(text):
                            posts.append({
                                'url': full_url,
                                'text': text,
                                'handle': handle
                            })

                except Exception as e:
                    continue

            await page.evaluate("window.scrollBy(0, 800)")
            await asyncio.sleep(1.5)
            scroll_attempts += 1

        print(f"  ✓ Found {len(posts)} new posts from @{handle}")
        return posts

    def is_business_content(self, text):
        """Filter for business/tech content only"""
        if len(text) < 50:
            return False

        business_keywords = [
            'revenue', 'mrr', 'arr', 'users', 'growth', 'launch', 'build',
            'app', 'saas', 'startup', 'indie', 'maker', 'founder',
            'email', 'seo', 'marketing', 'conversion', 'funnel',
            'automation', 'ai', 'tool', 'product', 'api', 'code'
        ]

        text_lower = text.lower()
        return any(keyword in text_lower for keyword in business_keywords)

    def extract_handle(self, url):
        """Extract @handle from URL"""
        match = re.search(r'/([^/]+)/status/', url)
        return match.group(1) if match else "unknown"

    def categorize_content(self, text):
        """Auto-categorize based on content"""
        text_lower = text.lower()

        if any(word in text_lower for word in ['app', 'mobile', 'ios', 'android', 'store']):
            return 'APP_FACTORY'
        elif any(word in text_lower for word in ['email', 'cold', 'outbound', 'deliverability']):
            return 'COLD_OUTBOUND'
        elif any(word in text_lower for word in ['seo', 'search', 'google', 'ranking']):
            return 'SEO_GEO_ASO'
        elif any(word in text_lower for word in ['content', 'tiktok', 'instagram', 'youtube']):
            return 'CONTENT_FARM'
        elif any(word in text_lower for word in ['ai', 'automation', 'tool', 'api']):
            return 'TOOL_ALPHA'
        elif any(word in text_lower for word in ['revenue', 'pricing', 'monetization', 'paywall']):
            return 'MONETIZATION'
        elif any(word in text_lower for word in ['growth', 'traffic', 'viral', 'distribution']):
            return 'GROWTH_HACK'
        else:
            return 'GENERAL'

    def save_to_csv(self, data, source_type):
        """Save extracted data to ALPHA_STAGING.csv"""
        if not data:
            print(f"⚠️  No new {source_type} to save")
            return

        print(f"💾 Saving {len(data)} {source_type} to ALPHA_STAGING.csv...")

        # Read existing file to preserve header
        rows = []
        if ALPHA_STAGING.exists():
            with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
                rows = list(csv.DictReader(f))

        # Add new entries
        for item in data:
            alpha_id = f"ALPHA{self.next_alpha_id}"
            self.next_alpha_id += 1

            category = self.categorize_content(item['text'])

            row = {
                'alpha_id': alpha_id,
                'source': f"@{item['handle']} ({source_type})",
                'source_url': item['url'],
                'category': category,
                'tactic': item['text'][:200] + '...' if len(item['text']) > 200 else item['text'],
                'full_description': item['text'],
                'actionable_steps': '',  # Human fills in during review
                'roi_potential': 'MEDIUM',
                'implementation_complexity': 'MEDIUM',
                'legal_risk': 'LOW',
                'applicable_methods': category,
                'status': 'PENDING_REVIEW',
                'priority': '',
                'reviewer_notes': f"Auto-scraped from Twitter {source_type}. Needs human review."
            }
            rows.append(row)

        # Write back
        fieldnames = [
            'alpha_id', 'source', 'source_url', 'category', 'tactic',
            'full_description', 'actionable_steps', 'roi_potential',
            'implementation_complexity', 'legal_risk', 'applicable_methods',
            'status', 'priority', 'reviewer_notes'
        ]

        with open(ALPHA_STAGING, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"✅ Saved {len(data)} new entries (ALPHA{self.next_alpha_id - len(data)}-ALPHA{self.next_alpha_id - 1})")

    def load_high_signal_accounts(self):
        """Load Twitter accounts marked auto_monitor=TRUE"""
        accounts = []
        with open(HIGH_SIGNAL_SOURCES, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('platform') == 'Twitter' and row.get('auto_monitor') == 'TRUE':
                    handle = row.get('source_name', '').replace('@', '')
                    if handle:
                        accounts.append({
                            'handle': handle,
                            'signal_quality': row.get('signal_quality', 'MEDIUM')
                        })

        # Sort by signal quality (HIGHEST first)
        priority = {'HIGHEST': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        accounts.sort(key=lambda x: priority.get(x['signal_quality'], 4))

        return accounts

async def main():
    parser = argparse.ArgumentParser(description='Twitter Alpha Scraper')
    parser.add_argument('--bookmarks', action='store_true', help='Scrape bookmarks')
    parser.add_argument('--accounts', action='store_true', help='Scrape high-signal accounts')
    parser.add_argument('--all', action='store_true', help='Scrape everything')
    parser.add_argument('--limit', type=int, default=20, help='Max accounts to scrape')
    args = parser.parse_args()

    if not any([args.bookmarks, args.accounts, args.all]):
        print("❌ Specify --bookmarks, --accounts, or --all")
        return

    scraper = TwitterScraper()

    async with async_playwright() as p:
        # Launch browser - headless with fresh profile (logs in via cookies)
        print("🚀 Launching Chrome...")
        try:
            # Try with user profile first
            browser = await p.chromium.launch_persistent_context(
                user_data_dir=str(CHROME_USER_DATA / "AutomationProfile"),
                headless=False,
                channel="chrome",
                viewport={'width': 1920, 'height': 1080}
            )
        except Exception as e:
            print(f"⚠️  Could not use profile (Chrome may be open). Using headless mode.")
            print(f"   You may need to log into Twitter manually in the automation window.")
            browser = await p.chromium.launch(
                headless=False,
                channel="chrome",
                viewport={'width': 1920, 'height': 1080}
            )

        page = await browser.new_page()

        try:
            # Scrape bookmarks
            if args.bookmarks or args.all:
                bookmarks = await scraper.scrape_bookmarks(page)
                scraper.save_to_csv(bookmarks, 'bookmarks')

                # Save raw JSON backup
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                with open(OUTPUT_DIR / f"bookmarks_{timestamp}.json", 'w') as f:
                    json.dump(bookmarks, f, indent=2)

            # Scrape high-signal accounts
            if args.accounts or args.all:
                accounts = scraper.load_high_signal_accounts()
                print(f"\n📋 Found {len(accounts)} high-signal accounts to scrape")

                all_posts = []
                for i, account in enumerate(accounts[:args.limit], 1):
                    print(f"\n[{i}/{min(args.limit, len(accounts))}] ", end='')
                    posts = await scraper.scrape_account(page, account['handle'])
                    all_posts.extend(posts)

                    # Small delay between accounts
                    await asyncio.sleep(3)

                scraper.save_to_csv(all_posts, 'high-signal-accounts')

                # Save raw JSON backup
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                with open(OUTPUT_DIR / f"accounts_{timestamp}.json", 'w') as f:
                    json.dump(all_posts, f, indent=2)

            print("\n✅ SCRAPING COMPLETE")
            print(f"📊 Total new entries added: {scraper.next_alpha_id - scraper.get_next_alpha_id()}")
            print(f"📁 Check: {ALPHA_STAGING}")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
