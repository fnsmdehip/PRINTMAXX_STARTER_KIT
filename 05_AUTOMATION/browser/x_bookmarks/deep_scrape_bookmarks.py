#!/usr/bin/env python3
"""
Deep scrape X bookmarks - get full threads, images, and expanded text
Uses Playwright to visit each URL and extract complete content
"""

import asyncio
import json
import base64
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime

# Configuration
INPUT_FILE = "x_bookmarks_2026-01-19.json"
OUTPUT_DIR = Path(__file__).parent / "deep_scrape_output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Prioritize high-value bookmarks
PRIORITY_PATTERNS = [
    'revenue', 'made', 'earned', '$', 'k/mo', 'k/month',
    'playbook', 'blueprint', 'framework', 'step-by-step',
    'infographic', 'breakdown', 'case study'
]

async def scrape_bookmark_deep(page, bookmark, index, total):
    """Visit bookmark URL and extract deep content"""
    url = bookmark['url']
    author = bookmark['author']
    
    print(f"\n[{index}/{total}] Scraping: {author}")
    print(f"URL: {url}")
    
    try:
        # Navigate to tweet (use "load" instead of "networkidle" for X's infinite scroll)
        await page.goto(url, wait_until="load", timeout=20000)
        await asyncio.sleep(3)  # Let content render
        
        # Click "Show more" buttons if present
        try:
            show_more_buttons = await page.locator('div[data-testid="tweet"] [role="button"]').all()
            for btn in show_more_buttons:
                text = await btn.inner_text()
                if "Show" in text or "more" in text:
                    try:
                        await btn.click(timeout=1000)
                        await asyncio.sleep(0.5)
                    except:
                        pass
        except:
            pass
        
        # Check if this is an X Article (longform)
        is_article = False
        article_text = ""
        try:
            # X Articles have different structure
            article_elem = page.locator('article[data-testid="article"], div[data-testid="article"]').first
            if await article_elem.count() > 0:
                is_article = True
                article_text = await article_elem.inner_text()
                print(f"  📰 Detected X Article ({len(article_text)} chars)")
        except:
            pass

        # Get full tweet text (after expanding)
        full_text = article_text if is_article else ""
        if not full_text:
            try:
                # Regular tweet text
                text_elems = await page.locator('div[data-testid="tweetText"]').all()
                texts = []
                for elem in text_elems:
                    t = await elem.inner_text()
                    if t:
                        texts.append(t)
                full_text = '\n\n'.join(texts) if texts else ""
            except:
                pass
        
        # Get all images
        images_data = []
        try:
            image_elems = await page.locator('div[data-testid="tweetPhoto"] img').all()
            for img in image_elems:
                try:
                    src = await img.get_attribute('src')
                    if src and 'profile' not in src:
                        images_data.append(src)
                except:
                    pass
        except:
            pass
        
        # Take screenshot if has images (for vision analysis later)
        screenshot_path = None
        if images_data or bookmark.get('has_images'):
            screenshot_path = OUTPUT_DIR / f"screenshot_{index}_{author.replace(' ', '_')[:20]}.png"
            try:
                await page.screenshot(path=str(screenshot_path), full_page=True)
                print(f"  📸 Screenshot saved: {screenshot_path.name}")
            except:
                screenshot_path = None
        
        # Check for threads (replies from same author)
        thread_tweets = []
        try:
            all_tweets = await page.locator('article[data-testid="tweet"]').all()
            for tweet in all_tweets[:10]:  # Max 10 tweets in thread
                try:
                    tweet_author = await tweet.locator('[data-testid="User-Name"]').first.inner_text()
                    if author in tweet_author:
                        tweet_text = await tweet.locator('[data-testid="tweetText"]').first.inner_text()
                        thread_tweets.append(tweet_text)
                except:
                    pass
        except:
            pass
        
        result = {
            'original': bookmark,
            'full_text': full_text if full_text else bookmark['text'],
            'image_urls': images_data,
            'screenshot_path': str(screenshot_path) if screenshot_path else None,
            'thread_tweets': thread_tweets,
            'thread_length': len(thread_tweets),
            'scraped_at': datetime.now().isoformat()
        }
        
        print(f"  ✅ Extracted: {len(full_text)} chars, {len(images_data)} images, {len(thread_tweets)} thread tweets")
        return result
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return {
            'original': bookmark,
            'error': str(e),
            'scraped_at': datetime.now().isoformat()
        }

async def main():
    # Load bookmarks
    with open(INPUT_FILE, 'r') as f:
        bookmarks = json.load(f)
    
    print(f"🚀 Deep scraping {len(bookmarks)} bookmarks...")
    
    # Prioritize bookmarks with revenue mentions, images, or long threads
    priority_bookmarks = []
    regular_bookmarks = []
    
    for bm in bookmarks:
        text_lower = bm['text'].lower()
        is_priority = (
            any(pattern in text_lower for pattern in PRIORITY_PATTERNS) or
            bm.get('has_images') or
            bm.get('word_count', 0) > 150
        )
        
        if is_priority:
            priority_bookmarks.append(bm)
        else:
            regular_bookmarks.append(bm)
    
    # Sort priority by value indicators
    priority_bookmarks.sort(key=lambda x: (
        x.get('has_images', False),
        x.get('word_count', 0)
    ), reverse=True)
    
    # Combine: priority first
    sorted_bookmarks = priority_bookmarks + regular_bookmarks
    
    print(f"📊 Priority bookmarks: {len(priority_bookmarks)}")
    print(f"📊 Regular bookmarks: {len(regular_bookmarks)}")
    
    async with async_playwright() as p:
        # Connect to existing Brave browser
        print("\n🔌 Connecting to Brave browser...")
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            print("✅ Connected!")
        except Exception as e:
            print(f"❌ Could not connect: {e}")
            print("Make sure Brave is running with: /Applications/Brave\\ Browser.app/Contents/MacOS/Brave\\ Browser --remote-debugging-port=9222")
            return
        
        contexts = browser.contexts
        if not contexts:
            print("❌ No browser contexts found")
            return
        
        context = contexts[0]
        pages = context.pages
        page = pages[0] if pages else await context.new_page()
        
        results = []
        total = len(sorted_bookmarks)
        
        # Scrape each bookmark
        for i, bm in enumerate(sorted_bookmarks, 1):
            result = await scrape_bookmark_deep(page, bm, i, total)
            results.append(result)
            
            # Save progress every 10 bookmarks
            if i % 10 == 0:
                temp_output = OUTPUT_DIR / f"progress_{i}_bookmarks.json"
                with open(temp_output, 'w') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                print(f"\n💾 Progress saved: {i}/{total} bookmarks")
            
            # Rate limiting
            await asyncio.sleep(1)
        
        # Save final results
        output_file = OUTPUT_DIR / f"x_bookmarks_deep_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n\n✅ DEEP SCRAPE COMPLETE!")
        print(f"📊 Scraped {len(results)} bookmarks")
        print(f"📁 Output: {output_file}")
        print(f"📸 Screenshots: {OUTPUT_DIR}/")
        
        # Stats
        with_images = len([r for r in results if r.get('image_urls')])
        with_threads = len([r for r in results if r.get('thread_length', 0) > 1])
        with_screenshots = len([r for r in results if r.get('screenshot_path')])
        
        print(f"\n📈 Results:")
        print(f"   - Bookmarks with images: {with_images}")
        print(f"   - Bookmarks with threads: {with_threads}")
        print(f"   - Screenshots captured: {with_screenshots}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
