#!/usr/bin/env python3
"""
Parallel background Twitter scraper using headless Chrome with your profile
Runs in background - you can keep using your laptop normally
"""

import asyncio
import json
import csv
import re
import shutil
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

# Paths
BASE_DIR = Path(__file__).parent.parent
HIGH_SIGNAL_SOURCES = BASE_DIR / "LEDGER" / "HIGH_SIGNAL_SOURCES.csv"
ALPHA_STAGING = BASE_DIR / "LEDGER" / "ALPHA_STAGING.csv"
OUTPUT_DIR = BASE_DIR / "AUTOMATIONS" / "scraper_output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Chrome profile path (macOS)
CHROME_PROFILE = Path.home() / "Library/Application Support/Google/Chrome/Default"

async def load_accounts():
    """Load Twitter accounts to scrape"""
    accounts = []
    with open(HIGH_SIGNAL_SOURCES, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('platform') in ['X', 'Twitter'] and row.get('auto_monitor') == 'TRUE':
                handle = row.get('source_name', '').replace('@', '').strip()
                if handle:
                    accounts.append(handle)
    return accounts

async def scrape_account(playwright, handle, output_file):
    """Scrape one account in headless background Chrome"""
    print(f"🔍 [{handle}] Starting scrape...")

    try:
        # Launch headless Chrome with your profile
        browser = await playwright.chromium.launch_persistent_context(
            user_data_dir=str(CHROME_PROFILE),
            headless=True,  # Background mode
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )

        page = await browser.new_page()

        # Navigate to profile
        url = f"https://x.com/{handle}"
        await page.goto(url, wait_until='domcontentloaded', timeout=30000)
        await page.wait_for_timeout(3000)

        # Extract tweets
        tweets = []
        for scroll in range(5):
            # Get tweets
            extracted = await page.evaluate("""
                () => {
                    const tweets = [];
                    const articles = document.querySelectorAll('article[data-testid="tweet"]');

                    articles.forEach(article => {
                        try {
                            const link = article.querySelector('a[href*="/status/"]');
                            const textElem = article.querySelector('[data-testid="tweetText"]');

                            if (link && textElem) {
                                const url = link.href;
                                const text = textElem.innerText;

                                // Filter for business content
                                if (text.length > 50) {
                                    const keywords = ['revenue', 'mrr', 'arr', 'users', 'growth',
                                                     'launch', 'build', 'app', 'saas', 'startup',
                                                     'email', 'seo', 'marketing', 'automation',
                                                     'ai', 'tool', 'product', 'api', 'code'];
                                    const lower = text.toLowerCase();
                                    if (keywords.some(kw => lower.includes(kw))) {
                                        tweets.push({ url, text });
                                    }
                                }
                            }
                        } catch(e) {}
                    });

                    return tweets;
                }
            """)

            tweets.extend(extracted)

            # Scroll
            await page.evaluate("window.scrollBy(0, 800)")
            await page.wait_for_timeout(1500)

        # Deduplicate
        seen = set()
        unique = []
        for tweet in tweets:
            if tweet['url'] not in seen:
                seen.add(tweet['url'])
                tweet['handle'] = handle
                unique.append(tweet)

        # Save to individual file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(unique, f, indent=2, ensure_ascii=False)

        await browser.close()

        print(f"✅ [{handle}] Found {len(unique)} tweets")
        return len(unique)

    except Exception as e:
        print(f"❌ [{handle}] Error: {e}")
        return 0

async def scrape_batch(playwright, accounts, batch_num, batch_size):
    """Scrape a batch of accounts in parallel"""
    start = batch_num * batch_size
    end = start + batch_size
    batch = accounts[start:end]

    print(f"\n📦 BATCH {batch_num + 1}: Scraping {len(batch)} accounts in parallel...")

    tasks = []
    for handle in batch:
        output_file = OUTPUT_DIR / f"{handle}.json"
        task = scrape_account(playwright, handle, output_file)
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    total = sum(results)
    print(f"✅ BATCH {batch_num + 1} COMPLETE: {total} total tweets\n")
    return total

def consolidate_results():
    """Consolidate all JSON files into ALPHA_STAGING.csv"""
    print("\n💾 Consolidating results into ALPHA_STAGING.csv...")

    # Load existing URLs
    existing_urls = set()
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row.get('source_url', '').strip()
                if url:
                    existing_urls.add(url)

    # Get next alpha ID
    max_id = 0
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                match = re.match(r'ALPHA(\d+)', row.get('alpha_id', ''))
                if match:
                    max_id = max(max_id, int(match.group(1)))
    next_id = max_id + 1

    # Read existing CSV
    rows = []
    fieldnames = []
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            rows = list(reader)
    else:
        fieldnames = [
            'alpha_id', 'source', 'source_url', 'category', 'tactic',
            'roi_potential', 'priority', 'status', 'tags', 'reviewer_notes',
            'approved_at', 'engagement_authenticity', 'earnings_verified',
            'extracted_method', 'use_case', 'added_at'
        ]

    # Process all JSON files
    new_count = 0
    for json_file in OUTPUT_DIR.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                tweets = json.load(f)

            for tweet in tweets:
                url = tweet['url']
                if url not in existing_urls:
                    # Categorize
                    text_lower = tweet['text'].lower()
                    if any(w in text_lower for w in ['app', 'mobile', 'ios']):
                        category = 'APP_FACTORY'
                    elif any(w in text_lower for w in ['email', 'cold']):
                        category = 'COLD_OUTBOUND'
                    elif any(w in text_lower for w in ['seo', 'search']):
                        category = 'SEO_GEO_ASO'
                    elif any(w in text_lower for w in ['content', 'tiktok']):
                        category = 'CONTENT_FARM'
                    elif any(w in text_lower for w in ['ai', 'automation']):
                        category = 'TOOL_ALPHA'
                    elif any(w in text_lower for w in ['revenue', 'pricing']):
                        category = 'MONETIZATION'
                    elif any(w in text_lower for w in ['growth', 'traffic']):
                        category = 'GROWTH_HACK'
                    else:
                        category = 'GENERAL'

                    row = {k: '' for k in fieldnames}
                    row.update({
                        'alpha_id': f'ALPHA{next_id}',
                        'source': f"@{tweet['handle']} (parallel scraper)",
                        'source_url': url,
                        'category': category,
                        'tactic': tweet['text'][:200] + '...' if len(tweet['text']) > 200 else tweet['text'],
                        'roi_potential': 'MEDIUM',
                        'status': 'PENDING_REVIEW',
                        'engagement_authenticity': 'AUTHENTIC',
                        'earnings_verified': 'FALSE',
                        'reviewer_notes': f"Auto-scraped parallel. {datetime.now().isoformat()}",
                        'added_at': datetime.now().isoformat()
                    })
                    rows.append(row)
                    existing_urls.add(url)
                    next_id += 1
                    new_count += 1

        except Exception as e:
            print(f"⚠️  Error processing {json_file.name}: {e}")

    # Write back
    with open(ALPHA_STAGING, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Added {new_count} new entries to ALPHA_STAGING.csv")
    print(f"📊 Total entries: {len(rows)}")

async def main():
    """Main execution"""
    print("🚀 PARALLEL BACKGROUND TWITTER SCRAPER")
    print("=" * 60)
    print("Running in BACKGROUND - you can keep using your laptop\n")

    # Load accounts
    accounts = await load_accounts()
    print(f"📋 Found {len(accounts)} accounts to scrape\n")

    # Batch size (parallel)
    batch_size = 10  # 10 accounts at once
    num_batches = (len(accounts) + batch_size - 1) // batch_size

    print(f"🔄 Will run {num_batches} batches of {batch_size} parallel scrapers\n")

    async with async_playwright() as playwright:
        total_tweets = 0
        for batch_num in range(num_batches):
            batch_total = await scrape_batch(playwright, accounts, batch_num, batch_size)
            total_tweets += batch_total

            # Brief pause between batches
            if batch_num < num_batches - 1:
                print(f"⏸  Pausing 5s before next batch...")
                await asyncio.sleep(5)

    print(f"\n🎉 ALL SCRAPING COMPLETE")
    print(f"📊 Total tweets extracted: {total_tweets}")

    # Consolidate
    consolidate_results()

    print(f"\n✅ DONE - Check LEDGER/ALPHA_STAGING.csv")
    print("🔍 Run: /review-alpha")

if __name__ == "__main__":
    asyncio.run(main())
