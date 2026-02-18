#!/usr/bin/env python3
"""
X.com Bookmark Extractor - Brave Browser Version
Connects to existing Brave browser session where you're already logged in.
"""

import asyncio
import json
import csv
from datetime import datetime
from playwright.async_api import async_playwright

# Filter criteria
SKIP_PATTERNS = [
    'meme', 'lol', 'lmao', 'just vibing', 'mood',
    'political take', 'hot take', 'unpopular opinion',
    'ratio', 'based', 'cringe',
]

FOCUS_KEYWORDS = [
    'tech', 'ai', 'automation', 'workflow', 'productivity',
    'business', 'startup', 'solopreneur', 'entrepreneur',
    'marketing', 'growth', 'distribution', 'sales',
    'social media', 'content', 'seo', 'affiliate',
    'coding', 'dev', 'tool', 'hack', 'tip', 'strategy',
    'playbook', 'framework', 'system', 'process'
]

async def extract_bookmarks():
    async with async_playwright() as p:
        print("🔗 Connecting to Brave browser...")
        print("📌 Make sure you:")
        print("   1. Have Brave running")
        print("   2. Are logged into X.com")
        print("   3. Have navigated to your bookmarks page")
        print("")

        # Try to launch Brave with remote debugging
        try:
            # Launch Brave with debugging port
            browser = await p.chromium.launch_persistent_context(
                user_data_dir='/Users/macbookpro/Library/Application Support/BraveSoftware/Brave-Browser/Default',
                headless=False,
                channel='chrome',  # Brave uses chromium channel
                args=[
                    '--remote-debugging-port=9222',
                    '--start-maximized'
                ]
            )

            # Get or create page
            if len(browser.pages) > 0:
                page = browser.pages[0]
            else:
                page = await browser.new_page()

            current_url = page.url
            print(f"📍 Current URL: {current_url}")

            # Navigate to bookmarks if not there
            if '/bookmarks' not in current_url:
                print("📱 Navigating to bookmarks...")
                await page.goto('https://x.com/i/bookmarks')
                await asyncio.sleep(5)  # Wait for load

            print("\n⏳ Starting extraction...")

        except Exception as e:
            print(f"❌ Error: {e}")
            print("\nTrying alternative method...")

            # Alternative: just launch Brave normally
            browser = await p.chromium.launch(
                headless=False,
                executable_path='/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
                args=['--start-maximized']
            )

            context = await browser.new_context()
            page = await context.new_page()

            print("⚠️  Could not connect to existing session.")
            print("   Opened new Brave window - please login and navigate to bookmarks")
            await asyncio.sleep(10)

            await page.goto('https://x.com')
            print("   Waiting 30 seconds for you to login and go to bookmarks...")
            await asyncio.sleep(30)

        # Extract bookmarks
        bookmarks = []
        prev_count = 0
        scroll_attempts = 0
        max_scrolls = 100

        print("\n🔄 Scrolling and extracting...")

        while scroll_attempts < max_scrolls:
            tweets = await page.query_selector_all('[data-testid="tweet"]')

            for tweet in tweets:
                try:
                    text_elem = await tweet.query_selector('[data-testid="tweetText"]')
                    text = await text_elem.inner_text() if text_elem else ""

                    author_elem = await tweet.query_selector('[data-testid="User-Name"]')
                    author = await author_elem.inner_text() if author_elem else ""

                    time_elem = await tweet.query_selector('time')
                    timestamp = await time_elem.get_attribute('datetime') if time_elem else ""

                    link_elem = await tweet.query_selector('a[href*="/status/"]')
                    url = await link_elem.get_attribute('href') if link_elem else ""
                    if url and not url.startswith('http'):
                        url = f"https://x.com{url}"

                    if text and url:
                        bookmarks.append({
                            'text': text,
                            'author': author.split('\n')[0] if author else "",
                            'timestamp': timestamp,
                            'url': url,
                            'extracted_at': datetime.now().isoformat()
                        })

                except Exception:
                    continue

            unique_bookmarks = {b['url']: b for b in bookmarks}
            bookmarks = list(unique_bookmarks.values())

            current_count = len(bookmarks)

            if current_count != prev_count:
                print(f"📊 {current_count} bookmarks collected...")

            if current_count == prev_count:
                print("✅ Extraction complete!")
                break

            prev_count = current_count

            await page.evaluate('window.scrollBy(0, window.innerHeight)')
            await asyncio.sleep(1.5)
            scroll_attempts += 1

        print(f"\n📦 Total: {len(bookmarks)} bookmarks")

        # Filter
        print("\n🔍 Filtering for actionable content...")
        filtered = []

        for bm in bookmarks:
            text_lower = bm['text'].lower()

            if any(p in text_lower for p in SKIP_PATTERNS):
                continue

            words = bm['text'].split()
            has_keyword = any(kw in text_lower for kw in FOCUS_KEYWORDS)

            if len(words) < 10 and not has_keyword:
                continue

            if has_keyword or len(words) > 30:
                bm['category'] = 'actionable'
                filtered.append(bm)

        print(f"✅ Filtered to {len(filtered)} actionable bookmarks")

        # Save
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        base = '/Users/macbookpro/Downloads/PRINTMAXX_STARTER_KIT/AUTOMATIONS/x_bookmarks'

        raw_json = f'{base}/bookmarks_raw_{ts}.json'
        with open(raw_json, 'w', encoding='utf-8') as f:
            json.dump(bookmarks, f, indent=2, ensure_ascii=False)
        print(f"💾 Raw: {raw_json}")

        filt_json = f'{base}/bookmarks_filtered_{ts}.json'
        with open(filt_json, 'w', encoding='utf-8') as f:
            json.dump(filtered, f, indent=2, ensure_ascii=False)
        print(f"💾 Filtered JSON: {filt_json}")

        csv_path = f'{base}/bookmarks_filtered_{ts}.csv'
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            if filtered:
                writer = csv.DictWriter(f, fieldnames=['text', 'author', 'timestamp', 'url', 'category', 'extracted_at'])
                writer.writeheader()
                writer.writerows(filtered)
        print(f"💾 CSV: {csv_path}")

        print("\n✅ Done! Closing in 5 seconds...")
        await asyncio.sleep(5)

        try:
            await browser.close()
        except:
            pass

        return filtered, ts

if __name__ == "__main__":
    results = asyncio.run(extract_bookmarks())
    if results:
        filtered, ts = results
        print(f"\n🎯 {len(filtered)} actionable bookmarks ready for analysis")
