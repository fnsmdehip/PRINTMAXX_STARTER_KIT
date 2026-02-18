#!/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
"""
DAILY AUTOMATED TWITTER SCRAPER
Runs daily via cron, scrapes all 92 accounts, adds to ALPHA_STAGING.csv
"""

import asyncio
import json
import csv
import re
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

# Paths
BASE_DIR = Path(__file__).parent.parent
HIGH_SIGNAL_SOURCES = BASE_DIR / "LEDGER" / "HIGH_SIGNAL_SOURCES.csv"
ALPHA_STAGING = BASE_DIR / "LEDGER" / "ALPHA_STAGING.csv"
CHROME_PROFILE = Path.home() / "Library/Application Support/Google/Chrome/Default"

def load_accounts():
    """Load all auto_monitor accounts"""
    accounts = []
    with open(HIGH_SIGNAL_SOURCES, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('platform') in ['X', 'Twitter'] and row.get('auto_monitor') == 'TRUE':
                handle = row.get('source_name', '').replace('@', '').strip()
                if handle:
                    accounts.append(handle)
    return accounts

async def scrape_account(page, handle):
    """Scrape one account timeline"""
    print(f"🔍 @{handle}")

    try:
        await page.goto(f"https://x.com/{handle}", timeout=30000)
        await page.wait_for_timeout(3000)

        tweets = []

        for _ in range(5):
            # Expand "show more" buttons
            await page.evaluate("""
                () => {
                    document.querySelectorAll('[data-testid="tweet-text-show-more-link"]').forEach(btn => {
                        try { btn.click(); } catch(e) {}
                    });
                }
            """)

            await page.wait_for_timeout(500)

            # Extract tweets
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

                                // Filter for actionable content
                                const hasValue = (
                                    text.length > 50 &&
                                    (
                                        /\\.(com|io|ai|app|co)\\b/.test(text) ||
                                        /\\$\\d+|revenue|mrr|arr|\\d+%|\\d+x/.test(text.toLowerCase()) ||
                                        /step\\s+\\d+|how\\s+to|framework|playbook|guide/.test(text.toLowerCase()) ||
                                        /filter\\s+by|database|pull\\s+every|install|tech\\s+stack/.test(text.toLowerCase())
                                    )
                                );

                                if (hasValue) {
                                    tweets.push({ url: link.href, text });
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

        # Dedupe
        seen = set()
        unique = []
        for tweet in tweets:
            if tweet['url'] not in seen:
                seen.add(tweet['url'])
                tweet['handle'] = handle
                unique.append(tweet)

        print(f"  ✓ {len(unique)} actionable tweets")
        return unique

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return []

def get_next_alpha_id():
    """Get next available ALPHA ID"""
    max_id = 0
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                match = re.match(r'ALPHA(\d+)', row.get('alpha_id', ''))
                if match:
                    max_id = max(max_id, int(match.group(1)))
    return max_id + 1

def load_existing_urls():
    """Load existing URLs to avoid duplicates"""
    urls = set()
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row.get('source_url', '').strip()
                if url:
                    urls.add(url)
    return urls

def categorize(text):
    """Auto-categorize tweet"""
    t = text.lower()
    if any(w in t for w in ['app', 'mobile', 'ios']):
        return 'APP_FACTORY'
    elif any(w in t for w in ['email', 'cold']):
        return 'COLD_OUTBOUND'
    elif any(w in t for w in ['seo', 'search']):
        return 'SEO_GEO_ASO'
    elif any(w in t for w in ['content', 'tiktok']):
        return 'CONTENT_FARM'
    elif any(w in t for w in ['ai', 'automation', 'tool']):
        return 'TOOL_ALPHA'
    elif any(w in t for w in ['revenue', 'pricing', '$']):
        return 'MONETIZATION'
    elif any(w in t for w in ['growth', 'traffic']):
        return 'GROWTH_HACK'
    return 'GENERAL'

def save_to_csv(all_tweets):
    """Save tweets to ALPHA_STAGING.csv"""
    existing_urls = load_existing_urls()

    # Filter new tweets
    new_tweets = [t for t in all_tweets if t['url'] not in existing_urls]

    if not new_tweets:
        print("\n✓ No new tweets (all already in CSV)")
        return

    print(f"\n💾 Saving {len(new_tweets)} new tweets...")

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
            'roi_potential', 'priority', 'status', 'applicable_methods',
            'applicable_niches', 'synergy_score', 'reviewer_notes',
            'quality_issues', 'engagement_authenticity', 'earnings_verified',
            'extracted_method', 'compliance_notes', 'date_added'
        ]

    # Add new entries
    next_id = get_next_alpha_id()
    for tweet in new_tweets:
        cat = categorize(tweet['text'])

        row = {k: '' for k in fieldnames}
        row.update({
            'alpha_id': f'ALPHA{next_id}',
            'source': f"@{tweet['handle']} (daily scraper)",
            'source_url': tweet['url'],
            'category': cat,
            'tactic': tweet['text'][:500],
            'roi_potential': 'MEDIUM',
            'priority': 'SOON',
            'status': 'PENDING_REVIEW',
            'applicable_methods': 'ALL',
            'applicable_niches': 'ALL',
            'synergy_score': '75',
            'reviewer_notes': f"Daily auto-scrape {datetime.now().isoformat()}",
            'quality_issues': '',
            'engagement_authenticity': 'AUTHENTIC',
            'earnings_verified': 'FALSE',
            'extracted_method': '',
            'compliance_notes': '',
            'date_added': datetime.now().isoformat()
        })
        rows.append(row)
        next_id += 1

    # Write back
    with open(ALPHA_STAGING, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Added ALPHA{next_id - len(new_tweets)}-ALPHA{next_id - 1}")

async def main():
    """Main scraper"""
    print("🚀 DAILY TWITTER SCRAPER")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    accounts = load_accounts()
    print(f"📋 {len(accounts)} accounts to scrape\n")

    all_tweets = []

    async with async_playwright() as p:
        # Launch with your Chrome profile
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(CHROME_PROFILE),
            headless=True,
            args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
        )

        page = await context.new_page()

        for i, handle in enumerate(accounts, 1):
            print(f"[{i}/{len(accounts)}]", end=' ')
            tweets = await scrape_account(page, handle)
            all_tweets.extend(tweets)

            # Brief pause between accounts
            await asyncio.sleep(2)

        await context.close()

    print(f"\n📊 Total actionable tweets: {len(all_tweets)}")
    save_to_csv(all_tweets)

    print("\n✅ DAILY SCRAPE COMPLETE")
    print(f"📁 Check: {ALPHA_STAGING}")

if __name__ == "__main__":
    asyncio.run(main())
