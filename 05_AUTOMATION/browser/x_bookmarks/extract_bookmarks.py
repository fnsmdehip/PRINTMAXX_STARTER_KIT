#!/usr/bin/env python3
"""
X.com Bookmark Extractor
Opens Chromium, lets user login, then extracts bookmarks filtering for actionable content.
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

async def extract_bookmarks():
    async with async_playwright() as p:
        # Launch Chromium with persistent context so user can login
        print("🚀 Launching Chromium...")
        print("📌 Please login to X.com in the browser that opens")
        print("📌 Navigate to your bookmarks page")
        print("📌 Press ENTER here when ready to extract...")

        browser = await p.chromium.launch(
            headless=False,
            channel='chromium',  # Use system Chromium
            args=['--start-maximized']
        )

        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )

        page = await context.new_page()

        # Navigate to X.com
        await page.goto('https://x.com')

        # Wait for user to login and navigate to bookmarks
        input("\nPress ENTER when you're on the bookmarks page and ready to extract...")

        print("\n⏳ Extracting bookmarks...")

        # Scroll and collect bookmarks
        bookmarks = []
        prev_count = 0
        scroll_attempts = 0
        max_scrolls = 50  # Prevent infinite loops

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
                            'url': url
                        })

                except Exception as e:
                    continue

            # Remove duplicates
            unique_bookmarks = {b['url']: b for b in bookmarks}
            bookmarks = list(unique_bookmarks.values())

            current_count = len(bookmarks)
            print(f"📊 Collected {current_count} bookmarks so far...")

            # Check if we got new bookmarks
            if current_count == prev_count:
                print("✅ No new bookmarks found. Extraction complete!")
                break

            prev_count = current_count

            # Scroll down
            await page.evaluate('window.scrollBy(0, window.innerHeight)')
            await asyncio.sleep(2)  # Wait for content to load
            scroll_attempts += 1

        print(f"\n📦 Total bookmarks extracted: {len(bookmarks)}")

        # Filter bookmarks
        print("\n🔍 Filtering for actionable content...")
        filtered_bookmarks = []

        for bm in bookmarks:
            text_lower = bm['text'].lower()

            # Skip if matches skip patterns
            if any(pattern in text_lower for pattern in SKIP_PATTERNS):
                continue

            # Skip if it's just a photo/selfie (short text, no keywords)
            if len(bm['text'].split()) < 10 and not any(kw in text_lower for kw in FOCUS_KEYWORDS):
                continue

            # Include if has focus keywords
            if any(kw in text_lower for kw in FOCUS_KEYWORDS):
                filtered_bookmarks.append(bm)

        print(f"✅ Filtered to {len(filtered_bookmarks)} actionable bookmarks")

        # Save to files
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Save JSON
        json_path = f'/Users/macbookpro/Downloads/PRINTMAXX_STARTER_KIT/AUTOMATIONS/x_bookmarks/bookmarks_{timestamp_str}.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(filtered_bookmarks, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved JSON: {json_path}")

        # Save CSV
        csv_path = f'/Users/macbookpro/Downloads/PRINTMAXX_STARTER_KIT/AUTOMATIONS/x_bookmarks/bookmarks_{timestamp_str}.csv'
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            if filtered_bookmarks:
                writer = csv.DictWriter(f, fieldnames=['text', 'author', 'timestamp', 'url'])
                writer.writeheader()
                writer.writerows(filtered_bookmarks)
        print(f"💾 Saved CSV: {csv_path}")

        # Keep browser open for user to review
        input("\n✅ Extraction complete! Press ENTER to close browser...")

        await browser.close()

        return filtered_bookmarks

if __name__ == "__main__":
    asyncio.run(extract_bookmarks())
