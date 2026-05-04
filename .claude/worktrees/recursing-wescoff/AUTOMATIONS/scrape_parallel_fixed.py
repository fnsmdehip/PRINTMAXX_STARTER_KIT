#!/usr/bin/env python3
"""
Parallel background Twitter scraper - FIXED version
Copies your Chrome profile to avoid conflicts
"""

import asyncio
import json
import csv
import re
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

# Paths
BASE_DIR = Path(__file__).parent.parent
HIGH_SIGNAL_SOURCES = BASE_DIR / "LEDGER" / "HIGH_SIGNAL_SOURCES.csv"
ALPHA_STAGING = BASE_DIR / "LEDGER" / "ALPHA_STAGING.csv"
OUTPUT_DIR = BASE_DIR / "AUTOMATIONS" / "scraper_output"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_accounts():
    """Load Twitter accounts"""
    accounts = []
    with open(HIGH_SIGNAL_SOURCES, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('platform') in ['X', 'Twitter'] and row.get('auto_monitor') == 'TRUE':
                handle = row.get('source_name', '').replace('@', '').strip()
                if handle:
                    accounts.append(handle)
    return accounts

async def scrape_account(handle, profile_dir):
    """Scrape one account"""
    output_file = OUTPUT_DIR / f"{handle}.json"

    print(f"🔍 [{handle}] Starting...")

    try:
        async with async_playwright() as p:
            # Use copied profile
            browser = await p.chromium.launch_persistent_context(
                user_data_dir=str(profile_dir),
                headless=True,
                args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
            )

            page = await browser.new_page()
            await page.goto(f"https://x.com/{handle}", timeout=30000)
            await page.wait_for_timeout(3000)

            tweets = []
            for _ in range(5):
                extracted = await page.evaluate("""
                    () => {
                        const tweets = [];
                        const articles = document.querySelectorAll('article[data-testid="tweet"]');

                        articles.forEach(article => {
                            try {
                                const link = article.querySelector('a[href*="/status/"]');
                                const textElem = article.querySelector('[data-testid="tweetText"]');

                                if (link && textElem) {
                                    const text = textElem.innerText;
                                    if (text.length > 50) {
                                        const keywords = ['revenue', 'mrr', 'users', 'growth',
                                                         'launch', 'build', 'app', 'saas',
                                                         'email', 'seo', 'marketing', 'ai',
                                                         'tool', 'product', 'code'];
                                        if (keywords.some(kw => text.toLowerCase().includes(kw))) {
                                            tweets.push({ url: link.href, text });
                                        }
                                    }
                                }
                            } catch(e) {}
                        });

                        return tweets;
                    }
                """)

                tweets.extend(extracted)
                await page.evaluate("window.scrollBy(0, 800)")
                await page.wait_for_timeout(1500)

            await browser.close()

            # Dedupe
            seen = set()
            unique = []
            for tweet in tweets:
                if tweet['url'] not in seen:
                    seen.add(tweet['url'])
                    tweet['handle'] = handle
                    unique.append(tweet)

            # Save
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(unique, f, indent=2, ensure_ascii=False)

            print(f"✅ [{handle}] {len(unique)} tweets")
            return len(unique)

    except Exception as e:
        print(f"❌ [{handle}] {e}")
        return 0

async def scrape_batch(accounts, profile_dir):
    """Scrape accounts in parallel"""
    tasks = [scrape_account(handle, profile_dir) for handle in accounts]
    results = await asyncio.gather(*tasks)
    return sum(results)

def consolidate():
    """Add results to ALPHA_STAGING.csv"""
    print("\n💾 Consolidating...")

    # Load existing
    existing_urls = set()
    max_id = 0
    rows = []
    fieldnames = []

    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                rows.append(row)
                existing_urls.add(row.get('source_url', ''))
                match = re.match(r'ALPHA(\d+)', row.get('alpha_id', ''))
                if match:
                    max_id = max(max_id, int(match.group(1)))
    else:
        fieldnames = [
            'alpha_id', 'source', 'source_url', 'category', 'tactic',
            'roi_potential', 'status', 'engagement_authenticity',
            'earnings_verified', 'reviewer_notes', 'added_at'
        ]

    next_id = max_id + 1
    new_count = 0

    # Process JSON files
    for json_file in OUTPUT_DIR.glob("*.json"):
        try:
            with open(json_file, 'r') as f:
                tweets = json.load(f)

            for tweet in tweets:
                if tweet['url'] not in existing_urls:
                    # Quick categorize
                    text_lower = tweet['text'].lower()
                    if 'app' in text_lower or 'mobile' in text_lower:
                        cat = 'APP_FACTORY'
                    elif 'email' in text_lower or 'cold' in text_lower:
                        cat = 'COLD_OUTBOUND'
                    elif 'seo' in text_lower:
                        cat = 'SEO_GEO_ASO'
                    elif 'content' in text_lower:
                        cat = 'CONTENT_FARM'
                    elif 'ai' in text_lower:
                        cat = 'TOOL_ALPHA'
                    elif 'revenue' in text_lower:
                        cat = 'MONETIZATION'
                    else:
                        cat = 'GENERAL'

                    row = {k: '' for k in fieldnames}
                    row.update({
                        'alpha_id': f'ALPHA{next_id}',
                        'source': f"@{tweet['handle']} (parallel)",
                        'source_url': tweet['url'],
                        'category': cat,
                        'tactic': tweet['text'][:200],
                        'roi_potential': 'MEDIUM',
                        'status': 'PENDING_REVIEW',
                        'engagement_authenticity': 'AUTHENTIC',
                        'earnings_verified': 'FALSE',
                        'reviewer_notes': f"Auto-scraped {datetime.now().isoformat()}",
                        'added_at': datetime.now().isoformat()
                    })
                    rows.append(row)
                    next_id += 1
                    new_count += 1

        except Exception as e:
            print(f"⚠️  {json_file.name}: {e}")

    # Write
    with open(ALPHA_STAGING, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Added {new_count} new entries")
    print(f"📊 Total: {len(rows)} entries")

async def main():
    print("🚀 PARALLEL BACKGROUND SCRAPER")
    print("=" * 60)

    # Load accounts
    accounts = load_accounts()
    print(f"📋 {len(accounts)} accounts to scrape\n")

    # Create temp profile copy
    chrome_profile = Path.home() / "Library/Application Support/Google/Chrome/Default"
    temp_profile = Path(tempfile.mkdtemp(prefix="chrome_profile_"))

    print("📁 Copying Chrome profile (logged-in state)...")

    # Copy only essential files (not everything - too slow)
    essential_files = ['Cookies', 'Local Storage', 'Network']
    for item in essential_files:
        src = chrome_profile / item
        if src.exists():
            dst = temp_profile / item
            if src.is_file():
                shutil.copy2(src, dst)
            else:
                shutil.copytree(src, dst, dirs_exist_ok=True)

    print("✅ Profile copied\n")

    # Batch and scrape (10 at a time)
    batch_size = 10
    total_tweets = 0

    for i in range(0, len(accounts), batch_size):
        batch = accounts[i:i + batch_size]
        batch_num = i // batch_size + 1
        print(f"📦 BATCH {batch_num}: {len(batch)} accounts...")

        batch_total = await scrape_batch(batch, temp_profile)
        total_tweets += batch_total

        print(f"✅ BATCH {batch_num}: {batch_total} tweets\n")

        if i + batch_size < len(accounts):
            await asyncio.sleep(5)

    # Cleanup
    shutil.rmtree(temp_profile, ignore_errors=True)

    print(f"\n🎉 DONE: {total_tweets} tweets")
    consolidate()
    print("\n🔍 Run: /review-alpha")

if __name__ == "__main__":
    asyncio.run(main())
