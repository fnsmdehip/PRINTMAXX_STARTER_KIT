#!/usr/bin/env python3
"""
X Bookmarks Scraper - Automated Playwright Version
Scrolls back 6 months and extracts all bookmarks
"""

import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path
from playwright.async_api import async_playwright

# Configuration
BOOKMARKS_URL = "https://x.com/i/bookmarks"
OUTPUT_DIR = Path(__file__).parent
MONTHS_BACK = 6
MAX_SCROLLS = 500
SCROLL_PAUSE = 1.0  # seconds between scrolls

async def scrape_bookmarks():
    from datetime import timezone
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=30 * MONTHS_BACK)
    print(f"🚀 Starting X bookmarks scraper...")
    print(f"📅 Extracting bookmarks from {cutoff_date.strftime('%Y-%m-%d')} onwards")

    async with async_playwright() as p:
        # Connect to existing Brave browser via CDP (Chrome DevTools Protocol)
        print("🔌 Connecting to existing Brave browser...")
        print("⚠️  Make sure Brave is running with remote debugging:")
        print("    Close Brave, then run:")
        print("    /Applications/Brave\\ Browser.app/Contents/MacOS/Brave\\ Browser --remote-debugging-port=9222")

        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            print("✅ Connected to existing Brave instance!")
        except Exception as e:
            print(f"❌ Could not connect: {e}")
            print("\n💡 Run this in Terminal first:")
            print("    /Applications/Brave\\ Browser.app/Contents/MacOS/Brave\\ Browser --remote-debugging-port=9222")
            return

        # Use the first context (your existing session)
        contexts = browser.contexts
        if not contexts:
            print("❌ No browser contexts found. Make sure Brave is running.")
            return

        context = contexts[0]

        # Use existing page or create new one
        pages = context.pages
        if pages:
            page = pages[0]
        else:
            page = await context.new_page()

        try:
            # Check if already on bookmarks page
            current_url = page.url
            if "bookmarks" not in current_url:
                print(f"📱 Navigating to {BOOKMARKS_URL}...")
                await page.goto(BOOKMARKS_URL, wait_until="load", timeout=60000)
                await asyncio.sleep(3)
            else:
                print(f"✅ Already on bookmarks page!")
                await asyncio.sleep(1)

            bookmarks = []
            scroll_count = 0
            prev_count = 0
            stale_scrolls = 0
            reached_cutoff = False

            print("📜 Starting scroll extraction...")

            while scroll_count < MAX_SCROLLS and not reached_cutoff:
                # Click all "Show more" buttons to expand truncated tweets
                try:
                    show_more_buttons = await page.locator('[data-testid="tweet"] [role="button"]').all()
                    for btn in show_more_buttons:
                        text = await btn.inner_text()
                        if "Show" in text or "more" in text:
                            try:
                                await btn.click(timeout=500)
                                await asyncio.sleep(0.05)
                            except:
                                pass
                except:
                    pass

                # Extract all visible tweets
                tweets = await page.locator('[data-testid="tweet"]').all()

                for tweet in tweets:
                    try:
                        # Extract text (use .first to avoid strict mode violation)
                        text_elem = tweet.locator('[data-testid="tweetText"]').first
                        text = await text_elem.inner_text() if await text_elem.count() > 0 else ""

                        # Extract author
                        author_elem = tweet.locator('[data-testid="User-Name"]').first
                        author_text = await author_elem.inner_text() if await author_elem.count() > 0 else ""
                        lines = author_text.split('\n')
                        author = lines[0] if lines else ""
                        handle = next((l for l in lines if l.startswith('@')), "")

                        # Extract timestamp
                        time_elem = tweet.locator('time')
                        timestamp = await time_elem.get_attribute('datetime') if await time_elem.count() > 0 else ""
                        display_time = await time_elem.inner_text() if await time_elem.count() > 0 else ""

                        # Extract URL
                        link_elem = tweet.locator('a[href*="/status/"]').first
                        url = await link_elem.get_attribute('href') if await link_elem.count() > 0 else ""
                        if url and not url.startswith('http'):
                            url = f"https://x.com{url}"

                        # Extract external link (article/site)
                        card_elem = tweet.locator('[data-testid="card.wrapper"] a')
                        external_url = await card_elem.get_attribute('href') if await card_elem.count() > 0 else ""

                        # Check for media
                        images = await tweet.locator('[data-testid="tweetPhoto"] img').all()
                        image_count = len([img for img in images if 'profile' not in await img.get_attribute('src')])
                        has_video = await tweet.locator('video').count() > 0

                        if text and url and timestamp:
                            tweet_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

                            # Check if we've gone past cutoff
                            if tweet_date < cutoff_date:
                                reached_cutoff = True
                                print(f"⏹️  Reached {MONTHS_BACK}-month cutoff at {tweet_date.strftime('%Y-%m-%d')}")

                            # Only add if within date range
                            if tweet_date >= cutoff_date:
                                bookmarks.append({
                                    'text': text,
                                    'author': author,
                                    'handle': handle,
                                    'timestamp': timestamp,
                                    'display_time': display_time,
                                    'url': url,
                                    'external_link': external_url,
                                    'has_images': image_count > 0,
                                    'image_count': image_count,
                                    'has_video': has_video,
                                    'word_count': len(text.split()),
                                    'date': tweet_date.strftime('%Y-%m-%d')
                                })

                    except Exception as e:
                        print(f"⚠️  Error processing tweet: {e}")
                        continue

                # Dedupe
                unique = {b['url']: b for b in bookmarks}
                current_count = len(unique)

                if scroll_count % 10 == 0:
                    oldest = min([datetime.fromisoformat(b['timestamp'].replace('Z', '+00:00')) for b in unique.values()]) if unique else datetime.now()
                    print(f"📊 Scroll {scroll_count}: {current_count} bookmarks | Oldest: {oldest.strftime('%Y-%m-%d')}")

                # Check if stuck
                if current_count == prev_count:
                    stale_scrolls += 1
                    if stale_scrolls >= 20 and not reached_cutoff:  # Increased from 5 to 20
                        print("⚠️  No new bookmarks found after 20 scrolls. Stopping.")
                        break
                else:
                    stale_scrolls = 0

                prev_count = current_count

                # Scroll down more aggressively
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(SCROLL_PAUSE * 1.5)  # Longer pause to let X load
                scroll_count += 1

                # Periodic pause to let X catch up
                if scroll_count % 50 == 0:
                    print("⏸️  Brief pause to let X load...")
                    await asyncio.sleep(2)

            # Final dedupe and sort
            final = list({b['url']: b for b in bookmarks}.values())
            final.sort(key=lambda x: x['timestamp'], reverse=True)

            # Save to JSON
            output_file = OUTPUT_DIR / f"x_bookmarks_{datetime.now().strftime('%Y-%m-%d')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(final, f, indent=2, ensure_ascii=False)

            print(f"\n✅ EXTRACTION COMPLETE!")
            print(f"📊 Saved {len(final)} bookmarks to {output_file.name}")
            if final:
                print(f"📅 Date range: {final[-1]['date']} to {final[0]['date']}")
                print(f"📈 Stats:")
                print(f"   - With external links: {len([b for b in final if b['external_link']])}")
                print(f"   - With images: {len([b for b in final if b['has_images']])}")
                print(f"   - With videos: {len([b for b in final if b['has_video']])}")
                print(f"   - Long threads (100+ words): {len([b for b in final if b['word_count'] >= 100])}")

        finally:
            # Don't close the browser - just disconnect
            await browser.close()
            print("👋 Disconnected from Brave (browser still running)")

if __name__ == "__main__":
    asyncio.run(scrape_bookmarks())
