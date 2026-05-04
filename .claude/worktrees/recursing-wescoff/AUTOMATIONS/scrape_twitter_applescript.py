#!/usr/bin/env python3
"""
Scrape Twitter using AppleScript to control the user's already-open Chrome
Works with logged-in Chrome - no restart needed
"""

import subprocess
import time
import json
import csv
import re
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(__file__).resolve().parent.parent
ALPHA_STAGING = PROJECT_DIR / "LEDGER" / "ALPHA_STAGING.csv"
HIGH_SIGNAL_SOURCES = PROJECT_DIR / "LEDGER" / "HIGH_SIGNAL_SOURCES.csv"


def run_applescript(script):
    """Execute AppleScript and return output"""
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return result.stdout.strip()


def load_high_signal_accounts():
    """Load Twitter accounts to scrape"""
    accounts = []
    with open(HIGH_SIGNAL_SOURCES, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            platform = row.get('platform', '').strip()
            if platform in ['X', 'Twitter'] and row.get('auto_monitor') == 'TRUE':
                handle = row.get('source_name', '').replace('@', '')
                if handle:
                    accounts.append(handle)
    return accounts


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


def navigate_to_url(url):
    """Navigate Chrome to URL using AppleScript"""
    script = f'''
    tell application "Google Chrome"
        activate
        set URL of active tab of front window to "{url}"
    end tell
    '''
    run_applescript(script)
    time.sleep(3)


def extract_tweets_js():
    """JavaScript to extract tweets from current page"""
    return '''
    (function() {
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
                        const keywords = ['revenue', 'mrr', 'arr', 'users', 'growth', 'launch', 'build', 'app', 'saas', 'startup', 'email', 'seo', 'marketing', 'automation', 'ai', 'tool', 'product', 'api', 'code', '$'];
                        const lower = text.toLowerCase();
                        if (keywords.some(kw => lower.includes(kw))) {
                            tweets.push({ url, text });
                        }
                    }
                }
            } catch(e) {}
        });

        return JSON.stringify(tweets);
    })();
    '''


def execute_javascript(js_code):
    """Execute JavaScript in Chrome's active tab"""
    # Escape quotes and newlines for AppleScript
    js_escaped = js_code.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

    script = f'''
    tell application "Google Chrome"
        execute active tab of front window javascript "{js_escaped}"
    end tell
    '''
    result = run_applescript(script)
    return result


def scroll_page():
    """Scroll down the page"""
    js = "window.scrollBy(0, 800);"
    execute_javascript(js)
    time.sleep(1.5)


def scrape_account(handle):
    """Scrape tweets from a Twitter account"""
    print(f"🔍 Scraping @{handle}...")

    # Navigate to profile
    navigate_to_url(f"https://x.com/{handle}")

    all_tweets = []

    # Scroll and extract
    for scroll in range(5):
        # Extract tweets
        result = execute_javascript(extract_tweets_js())

        if result:
            try:
                tweets = json.loads(result)
                all_tweets.extend(tweets)
            except json.JSONDecodeError:
                pass

        # Scroll
        scroll_page()

    # Deduplicate by URL
    seen = set()
    unique_tweets = []
    for tweet in all_tweets:
        if tweet['url'] not in seen:
            seen.add(tweet['url'])
            unique_tweets.append(tweet)

    print(f"  ✓ Found {len(unique_tweets)} business tweets")
    return unique_tweets


def load_existing_urls():
    """Load existing URLs"""
    urls = set()
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('source_url'):
                    urls.add(row['source_url'])
    return urls


def categorize_content(text):
    """Auto-categorize based on content"""
    text_lower = text.lower()

    if any(word in text_lower for word in ['app', 'mobile', 'ios', 'android']):
        return 'APP_FACTORY'
    elif any(word in text_lower for word in ['email', 'cold', 'outbound']):
        return 'COLD_OUTBOUND'
    elif any(word in text_lower for word in ['seo', 'search', 'google']):
        return 'SEO_GEO_ASO'
    elif any(word in text_lower for word in ['content', 'tiktok', 'youtube']):
        return 'CONTENT_FARM'
    elif any(word in text_lower for word in ['ai', 'automation', 'tool']):
        return 'TOOL_ALPHA'
    elif any(word in text_lower for word in ['revenue', 'pricing', 'monetization']):
        return 'MONETIZATION'
    elif any(word in text_lower for word in ['growth', 'traffic', 'viral']):
        return 'GROWTH_HACK'
    else:
        return 'GENERAL'


def save_to_csv(tweets_by_account):
    """Save all tweets to ALPHA_STAGING.csv"""
    # Load existing URLs
    existing_urls = load_existing_urls()

    # Flatten and filter
    all_new_tweets = []
    for handle, tweets in tweets_by_account.items():
        for tweet in tweets:
            if tweet['url'] not in existing_urls:
                tweet['handle'] = handle
                all_new_tweets.append(tweet)

    if not all_new_tweets:
        print("No new tweets to add")
        return

    print(f"💾 Saving {len(all_new_tweets)} new tweets...")

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
            'full_description', 'actionable_steps', 'roi_potential',
            'implementation_complexity', 'legal_risk', 'applicable_methods',
            'status', 'priority', 'reviewer_notes', 'engagement_authenticity',
            'earnings_verified'
        ]

    # Add new entries
    next_id = get_next_alpha_id()
    for tweet in all_new_tweets:
        category = categorize_content(tweet['text'])

        row = {k: '' for k in fieldnames}
        row.update({
            'alpha_id': f'ALPHA{next_id}',
            'source': f"@{tweet['handle']} (AppleScript scrape)",
            'source_url': tweet['url'],
            'category': category,
            'tactic': tweet['text'][:200] + '...' if len(tweet['text']) > 200 else tweet['text'],
            'full_description': tweet['text'],
            'status': 'PENDING_REVIEW',
            'engagement_authenticity': 'AUTHENTIC',
            'earnings_verified': 'FALSE',
            'reviewer_notes': f"Auto-scraped via AppleScript. {datetime.now().isoformat()}"
        })
        rows.append(row)
        next_id += 1

    # Write back
    with open(ALPHA_STAGING, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Saved {len(all_new_tweets)} entries (ALPHA{next_id - len(all_new_tweets)}-ALPHA{next_id - 1})")


def main():
    print("🚀 Twitter AppleScript Scraper")
    print("Using your already-open, logged-in Chrome")
    print("=" * 60)

    # Load accounts
    accounts = load_high_signal_accounts()
    print(f"📋 Found {len(accounts)} accounts to scrape\n")

    # Scrape all accounts
    tweets_by_account = {}
    for i, handle in enumerate(accounts, 1):
        print(f"[{i}/{len(accounts)}]", end=' ')
        tweets = scrape_account(handle)
        tweets_by_account[handle] = tweets
        time.sleep(2)

    # Save to CSV
    save_to_csv(tweets_by_account)

    print("\n✅ SCRAPING COMPLETE")
    print(f"📁 Check: {ALPHA_STAGING}")


if __name__ == "__main__":
    main()
