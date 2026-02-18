#!/usr/bin/env python3
"""
X.com Bookmark Extractor - Interactive Version
Opens Chromium, waits for user to login and navigate to bookmarks, then auto-extracts.
"""

import asyncio
import json
import csv
from datetime import datetime
from playwright.async_api import async_playwright

# Filter criteria - skip these types of content
SKIP_PATTERNS = [
    'meme', 'lol', 'lmao', 'just vibing', 'mood',
    'political take', 'hot take', 'unpopular opinion',
    'ratio', 'based', 'cringe',
]

# Focus on these topics
FOCUS_KEYWORDS = [
    'tech', 'ai', 'automation', 'workflow', 'productivity',
    'business', 'startup', 'solopreneur', 'entrepreneur',
    'marketing', 'growth', 'distribution', 'sales',
    'social media', 'content', 'seo', 'affiliate',
    'coding', 'dev', 'tool', 'hack', 'tip', 'strategy',
    'playbook', 'framework', 'system', 'process'
]

async def wait_for_bookmarks_page(page):
    """Wait for user to navigate to bookmarks page"""
    print("⏳ Waiting for you to navigate to bookmarks...")
    print("   (The URL should contain '/bookmarks')")

    max_wait = 300  # 5 minutes
    waited = 0

    while waited < max_wait:
        url = page.url
        if '/bookmarks' in url:
            print(f"✅ Detected bookmarks page: {url}")
            await asyncio.sleep(3)  # Wait for page to fully load
            return True

        await asyncio.sleep(2)
        waited += 2

        if waited % 20 == 0:
            print(f"   Still waiting... ({waited}s elapsed)")

    return False

async def extract_bookmarks():
    async with async_playwright() as p:
        print("🚀 Launching Chromium...")
        print("📌 Please:")
        print("   1. Login to X.com")
        print("   2. Navigate to your bookmarks page")
        print("   3. Script will auto-detect and start extracting\n")

        browser = await p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )

        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )

        page = await context.new_page()

        # Navigate to X.com
        await page.goto('https://x.com')

        # Wait for user to navigate to bookmarks
        detected = await wait_for_bookmarks_page(page)

        if not detected:
            print("❌ Timeout waiting for bookmarks page. Exiting...")
            await browser.close()
            return []

        print("\n⏳ Extracting bookmarks...")

        # Scroll and collect bookmarks
        bookmarks = []
        prev_count = 0
        scroll_attempts = 0
        max_scrolls = 100  # Increased for larger collections

        while scroll_attempts < max_scrolls:
            # Extract tweets from current view
            tweets = await page.query_selector_all('[data-testid="tweet"]')

            for tweet in tweets:
                try:
                    # Extract text content
                    text_elem = await tweet.query_selector('[data-testid="tweetText"]')
                    text = await text_elem.inner_text() if text_elem else ""

                    # Extract author
                    author_elem = await tweet.query_selector('[data-testid="User-Name"]')
                    author = await author_elem.inner_text() if author_elem else ""

                    # Extract timestamp
                    time_elem = await tweet.query_selector('time')
                    timestamp = await time_elem.get_attribute('datetime') if time_elem else ""

                    # Extract URL
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

                except Exception as e:
                    continue

            # Remove duplicates
            unique_bookmarks = {b['url']: b for b in bookmarks}
            bookmarks = list(unique_bookmarks.values())

            current_count = len(bookmarks)

            if current_count != prev_count:
                print(f"📊 Collected {current_count} bookmarks...")

            # Check if we got new bookmarks
            if current_count == prev_count:
                print("✅ No new bookmarks found. Extraction complete!")
                break

            prev_count = current_count

            # Scroll down
            await page.evaluate('window.scrollBy(0, window.innerHeight)')
            await asyncio.sleep(1.5)
            scroll_attempts += 1

        print(f"\n📦 Total bookmarks extracted: {len(bookmarks)}")

        # Filter bookmarks
        print("\n🔍 Filtering for actionable content...")
        filtered_bookmarks = []

        for bm in bookmarks:
            text_lower = bm['text'].lower()

            # Skip if matches skip patterns
            skip = False
            for pattern in SKIP_PATTERNS:
                if pattern in text_lower:
                    skip = True
                    break

            if skip:
                continue

            # Skip if it's just a photo/selfie (short text, no keywords)
            words = bm['text'].split()
            has_focus_keyword = any(kw in text_lower for kw in FOCUS_KEYWORDS)

            if len(words) < 10 and not has_focus_keyword:
                continue

            # Include if has focus keywords or substantial content
            if has_focus_keyword or len(words) > 30:
                bm['category'] = 'actionable'
                filtered_bookmarks.append(bm)

        print(f"✅ Filtered to {len(filtered_bookmarks)} actionable bookmarks")

        # Save to files
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_path = '/Users/macbookpro/Downloads/PRINTMAXX_STARTER_KIT/AUTOMATIONS/x_bookmarks'

        # Save all bookmarks (raw)
        raw_json_path = f'{base_path}/bookmarks_raw_{timestamp_str}.json'
        with open(raw_json_path, 'w', encoding='utf-8') as f:
            json.dump(bookmarks, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved raw JSON: {raw_json_path}")

        # Save filtered bookmarks JSON
        json_path = f'{base_path}/bookmarks_filtered_{timestamp_str}.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(filtered_bookmarks, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved filtered JSON: {json_path}")

        # Save filtered CSV
        csv_path = f'{base_path}/bookmarks_filtered_{timestamp_str}.csv'
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            if filtered_bookmarks:
                writer = csv.DictWriter(f, fieldnames=['text', 'author', 'timestamp', 'url', 'category', 'extracted_at'])
                writer.writeheader()
                writer.writerows(filtered_bookmarks)
        print(f"💾 Saved filtered CSV: {csv_path}")

        print("\n✅ Extraction complete!")
        print("   Browser will close in 10 seconds...")
        await asyncio.sleep(10)

        await browser.close()

        return filtered_bookmarks, timestamp_str

if __name__ == "__main__":
    results = asyncio.run(extract_bookmarks())
    if results:
        filtered, ts = results
        print(f"\n🎯 Ready for analysis: {len(filtered)} actionable bookmarks saved")
