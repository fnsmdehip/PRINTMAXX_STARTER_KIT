# Twitter/X Alpha Scraping Strategy

Playwright-based approach for scraping high-signal X accounts to extract actionable alpha. Integrates with existing `LEDGER/HIGH_SIGNAL_SOURCES.csv` and outputs to `LEDGER/ALPHA_STAGING.csv`.

---

## Overview

This strategy uses Playwright (not X API) to scrape tweets from 56+ high-signal accounts, looking for revenue numbers, launch tactics, tools, growth hacks, and failed experiments. Built on existing infrastructure in `AUTOMATIONS/scripts/source_scrapers/twitter_scraper.py` and `AUTOMATIONS/daily_research/twitter_scanner.py`.

**Key advantages of Playwright approach:**
- No API rate limits
- No API costs ($100/mo X API avoided)
- Can access more data than API provides
- Works with logged-in session for higher quality results
- Can scrape bookmarks and timeline

---

## Architecture

### Existing Infrastructure (Reuse)

1. **`AUTOMATIONS/scripts/source_scrapers/twitter_scraper.py`**
   - Playwright-based scraper with proxy support
   - Handles profile scraping, search, trending topics
   - Anti-detection measures built in
   - Rate limiting (2 second minimum delay)
   - Engagement metric extraction

2. **`AUTOMATIONS/daily_research/twitter_scanner.py`**
   - Alpha detection logic already implemented
   - Filters for revenue mentions, tools, tactics, numbers
   - Saves to ALPHA_STAGING.csv with correct format
   - Deduplication via seen_ids cache
   - Category classification (APP_FACTORY, OUTBOUND, etc.)

3. **`LEDGER/HIGH_SIGNAL_SOURCES.csv`**
   - 56+ accounts already tracked
   - Signal quality tiers (HIGHEST, HIGH, MEDIUM)
   - Focus areas defined
   - 11 X accounts marked for auto_monitor=TRUE

### What's Already Working

```python
# Profile scraping
scraper = TwitterScraper(headless=True, proxy_config={...})
await scraper.initialize()
tweets = await scraper.scrape_account('https://x.com/levelsio', max_tweets=10)

# Alpha detection
scanner = TwitterScanner()
findings = scanner.scan_all_sources(tier_filter='HIGHEST')
scanner.save_findings(findings)
```

---

## Three Scraping Modes

### Mode 1: High-Signal Account Timeline Scraping (Primary)

**Target:** 11 HIGHEST-tier X accounts from `HIGH_SIGNAL_SOURCES.csv`

**What to scrape:**
- @levelsio - Indie hacking numbers, revenue
- @tdinh_me - Technical solopreneur, indie apps
- @dannypostmaa - Honest failures
- @caiden_cole - Cold email deliverability (HIGHEST)
- @godofprompt - Prompt engineering AI
- @dansugcmodels - Eastern EU UGC sourcing (HIGHEST)
- @xivy0k - Mobile app marketing solopreneur
- @knoxtwts - App marketing content formats (HIGHEST)
- @pipelineabuser - Cold email outbound mastery (HIGHEST)
- @purpdevvv - App dev indie strategies (HIGHEST)
- @Hightrafficsite - SEO traffic growth tactics (HIGHEST)
- @iamgdsa - Creator marketing app virality (HIGHEST)
- @jasoncfox - Marketing funnels growth hacks (HIGHEST)

**Frequency:** Daily for HIGHEST, 3x/week for HIGH

**Implementation:**
```python
# AUTOMATIONS/scripts/daily_timeline_scraper.py

import asyncio
from source_scrapers.twitter_scraper import TwitterScraper
from daily_research.twitter_scanner import TwitterScanner

async def scrape_high_signal_accounts():
    """
    Scrape timelines of HIGHEST-tier accounts daily.
    """
    scanner = TwitterScanner()
    sources = scanner.get_x_sources(tier_filter='HIGHEST')

    scraper = TwitterScraper(
        headless=True,
        proxy_config=get_proxy_config(),  # Residential proxy
        timeout=30000
    )

    try:
        await scraper.initialize()

        all_tweets = []
        for source in sources:
            print(f"Scraping {source['name']}...")

            # Get last 20 tweets (covers ~1-3 days depending on account)
            tweets = await scraper.scrape_account(
                profile_url=source['url'],
                max_tweets=20,
                include_replies=False  # Skip replies, focus on original content
            )

            all_tweets.extend(tweets)

            # Rate limit between accounts (human-like)
            await asyncio.sleep(random.uniform(3, 8))

        # Analyze for alpha
        findings = []
        for tweet in all_tweets:
            # Convert tweet dict to Tweet object
            tweet_obj = Tweet(
                id=tweet['url'].split('/')[-1],
                author=tweet['handle'],
                content=tweet['text'],
                url=tweet['url'],
                timestamp=datetime.fromisoformat(tweet['timestamp']) if tweet['timestamp'] else datetime.now(),
                engagement={
                    'likes': tweet['likes'],
                    'retweets': tweet['retweets'],
                    'replies': tweet['replies']
                },
                media_urls=[]
            )

            source_info = next(s for s in sources if s['name'] == tweet['handle'])
            finding = scanner.analyze_tweet_for_alpha(tweet_obj, source_info)
            if finding:
                findings.append(finding)

        # Save to ALPHA_STAGING.csv
        saved = scanner.save_findings(findings)
        print(f"Saved {saved} new alpha findings")

    finally:
        await scraper.close()

if __name__ == '__main__':
    asyncio.run(scrape_high_signal_accounts())
```

---

### Mode 2: Bookmark Scraping (Batch Research)

**Target:** User's X bookmarks (high-signal content they've already curated)

**Why:** Bookmarks are pre-filtered alpha. User has already done first-pass curation.

**Frequency:** Weekly or on-demand

**Implementation:** Use existing `AUTOMATIONS/x_bookmarks/extract_bookmarks.py`

**Workflow:**
1. User runs browser console script from `x_bookmarks/QUICK_START.md`
2. Downloads JSON to `x_bookmarks/` folder
3. Run `analyze_bookmarks.py` to filter and categorize
4. Extract alpha to ALPHA_STAGING.csv

**Enhancement needed:**
```python
# AUTOMATIONS/x_bookmarks/extract_alpha_from_bookmarks.py

import json
import csv
from pathlib import Path
from daily_research.twitter_scanner import TwitterScanner

def extract_alpha_from_bookmarks(bookmarks_json_path):
    """
    Parse bookmarks JSON and extract alpha to ALPHA_STAGING.csv
    """
    with open(bookmarks_json_path, 'r') as f:
        bookmarks = json.load(f)

    scanner = TwitterScanner()
    findings = []

    for bookmark in bookmarks:
        # Convert bookmark to Tweet object
        tweet = Tweet(
            id=bookmark['url'].split('/')[-1],
            author=bookmark.get('author', ''),
            content=bookmark['text'],
            url=bookmark['url'],
            timestamp=datetime.fromisoformat(bookmark['timestamp']) if bookmark.get('timestamp') else datetime.now(),
            engagement={},
            media_urls=[]
        )

        # Analyze for alpha
        source_info = {
            'name': bookmark.get('author', '@unknown'),
            'focus_area': 'Bookmarked content',
            'signal_quality': 'HIGH'
        }

        finding = scanner.analyze_tweet_for_alpha(tweet, source_info)
        if finding:
            findings.append(finding)

    saved = scanner.save_findings(findings)
    print(f"Extracted {saved} alpha findings from {len(bookmarks)} bookmarks")

# Usage:
# python extract_alpha_from_bookmarks.py x_bookmarks_2026-01-22.json
```

---

### Mode 3: Keyword/Topic Search (Targeted Research)

**Target:** Specific keywords or trending topics for deep research

**Use cases:**
- "mrr" OR "revenue" OR "$XXk/mo" - Find revenue mentions
- "launched" OR "shipped" - New product launches
- "cold email deliverability" - Specific tactic research
- Trending topics from explore page

**Frequency:** On-demand or when researching specific topics

**Implementation:**
```python
# Use existing search_tweets() method

async def search_for_revenue_mentions():
    """
    Search for revenue/MRR mentions across X.
    """
    scraper = TwitterScraper(headless=True)
    await scraper.initialize()

    queries = [
        '"$10k/mo"',
        '"$50k mrr"',
        '"revenue" OR "mrr"',
        'launched app making',
        'cold email deliverability'
    ]

    for query in queries:
        tweets = await scraper.search_tweets(
            query=query,
            max_tweets=20,
            sort='Latest'  # Get most recent
        )

        # Process and analyze...
```

---

## Alpha Detection Signals (Enhanced)

### Existing Detection (Already Implemented)

From `twitter_scanner.py`:
- Revenue/money keywords: revenue, $, mrr, arr, conversion
- App keywords: downloads, installs, launched, shipped
- Tool keywords: tool, app, framework, playbook
- Content keywords: views, viral, hook
- Outbound keywords: cold email, reply rate, open rate

### Enhanced Detection Patterns (Add These)

**1. Numbers + Context = High Signal**
```python
# Add to analyze_tweet_for_alpha()

import re

def extract_revenue_mentions(content):
    """
    Extract specific revenue numbers and context.
    Examples:
    - "$50k MRR" -> 50000
    - "10k/month" -> 10000
    - "hit $100k" -> 100000
    """
    patterns = [
        r'\$(\d+)k?\s*(mrr|arr|revenue|/mo|/month)',
        r'(\d+)k\s*mrr',
        r'making\s+\$(\d+)k',
        r'hit\s+\$(\d+)k'
    ]

    matches = []
    for pattern in patterns:
        found = re.findall(pattern, content.lower())
        if found:
            matches.extend(found)

    return matches

# Flag tweets with specific numbers as HIGHEST priority
if extract_revenue_mentions(tweet.content):
    roi_potential = 'HIGHEST'
```

**2. Launch Announcements**
```python
launch_patterns = [
    'just launched',
    'shipped',
    'live on product hunt',
    'now available',
    'releasing',
    'beta access'
]

if any(pattern in content.lower() for pattern in launch_patterns):
    category = 'APP_FACTORY'
    # Extract what was launched, how, and early results
```

**3. Failed Experiments (High Value)**
```python
failure_patterns = [
    'failed',
    'didn\'t work',
    'waste of time',
    'avoid',
    'mistake',
    'learned the hard way'
]

# Failures are valuable - extract lessons learned
if any(pattern in content.lower() for pattern in failure_patterns):
    title = f"[FAILURE] {title}"
    # Tag for review - failures teach what not to do
```

**4. Tool/Service Mentions**
```python
def extract_tools(content):
    """
    Extract mentioned tools/services.
    Common patterns:
    - "I use [Tool]"
    - "switched to [Tool]"
    - "[Tool] for [use case]"
    """
    # Look for capitalized words or URLs
    tools = re.findall(r'\b[A-Z][a-z]+(?:\.[a-z]{2,})?\b', content)
    urls = re.findall(r'https?://[^\s]+', content)

    return tools + urls
```

**5. Engagement Threshold**
```python
def is_high_engagement(tweet, author_avg_engagement=None):
    """
    Determine if tweet has unusually high engagement.

    High engagement = higher quality alpha signal.
    """
    total_engagement = sum(tweet.engagement.values())

    # Thresholds by follower count (estimate)
    if total_engagement > 1000:  # Likely viral
        return True

    if total_engagement > 100:  # Above average
        return True

    # Compare to author's typical engagement if available
    if author_avg_engagement and total_engagement > author_avg_engagement * 2:
        return True

    return False
```

---

## Proxy Strategy

### Residential Proxies Required

X is aggressive with rate limiting and bot detection. Use residential proxies from Soax or Decodo.

**Recommended setup:**
```python
# AUTOMATIONS/config/proxy_config.py

PROXY_CONFIG = {
    'server': 'http://proxy.soax.com:9000',  # or smartproxy.com
    'username': 'user-residential-country-US-sessionduration-30',
    'password': os.getenv('SOAX_PASSWORD')
}

# Sticky session (30 min) keeps same IP
# US geo for consistency with account location
```

**Cost:**
- Decodo: $12.50/GB (recommended for social scraping)
- Soax: $6.60/GB (cheaper but smaller pool)
- Budget: $25-50/mo for daily scraping of 11 accounts

**Mobile proxies for main account:**
If using logged-in session for bookmark scraping, consider mobile proxy:
- Soax mobile: $99/mo for 3GB
- Higher trust, lower ban risk
- See `SOAX_MOBILE_PROXIES.md`

---

## Rate Limiting & Anti-Detection

### Built-in Measures (Already Implemented)

From `twitter_scraper.py`:
1. **Minimum 2-second delay** between requests
2. **Stealth browser settings** (disable automation flags)
3. **Random user agents**
4. **Human-like viewport sizes**
5. **JavaScript stealth injections** (hide webdriver)

### Enhanced Anti-Detection

**1. Variable Delays**
```python
import random

async def human_delay(min_sec=2, max_sec=5):
    """
    Random delay that mimics human browsing patterns.
    """
    delay = random.gauss((min_sec + max_sec) / 2, (max_sec - min_sec) / 6)
    delay = max(min_sec, min(max_sec, delay))  # Clamp
    await asyncio.sleep(delay)

# Use between accounts
await human_delay(3, 8)
```

**2. Scroll Behavior**
```python
async def human_scroll(page):
    """
    Scroll like a human (variable speed, pauses).
    """
    scroll_positions = [0.3, 0.5, 0.7, 0.9]

    for position in scroll_positions:
        await page.evaluate(f"window.scrollTo(0, document.body.scrollHeight * {position})")
        await asyncio.sleep(random.uniform(0.5, 1.5))
```

**3. Session Persistence**
```python
# Save logged-in session for bookmark scraping
await context.storage_state(path='sessions/x_session.json')

# Reuse later
context = await browser.new_context(
    storage_state='sessions/x_session.json'
)
```

**4. Time-of-Day Variation**
```python
# Don't scrape at exact same time daily
# Add random offset to cron schedule

import random
from datetime import datetime, timedelta

def get_next_run_time(base_hour=9):
    """
    Calculate next run time with random offset.
    Run around 9 AM ± 2 hours.
    """
    now = datetime.now()
    next_run = now.replace(hour=base_hour, minute=0, second=0) + timedelta(days=1)
    offset = timedelta(hours=random.uniform(-2, 2))
    return next_run + offset
```

---

## Error Handling & Resilience

### Common Failures

1. **Rate limited** - Twitter shows "Try again later"
2. **Logged out** - Session expired
3. **Content unavailable** - Account suspended or protected
4. **Network timeout** - Slow proxy or poor connection

### Retry Strategy

```python
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def scrape_with_retry(scraper, url):
    """
    Retry scraping with exponential backoff.
    """
    try:
        return await scraper.scrape_account(url, max_tweets=20)
    except Exception as e:
        logger.warning(f"Scrape failed for {url}: {e}")
        raise
```

### Graceful Degradation

```python
async def scrape_all_accounts_with_fallback():
    """
    Continue scraping even if some accounts fail.
    """
    sources = scanner.get_x_sources(tier_filter='HIGHEST')

    results = []
    failed = []

    for source in sources:
        try:
            tweets = await scrape_with_retry(scraper, source['url'])
            results.extend(tweets)
        except Exception as e:
            failed.append((source['name'], str(e)))
            continue  # Don't let one failure stop the rest

    # Log failures
    if failed:
        logger.error(f"Failed to scrape {len(failed)} accounts: {failed}")

    return results
```

---

## Output Format

All findings append to `LEDGER/ALPHA_STAGING.csv` with this format:

```csv
alpha_id,source,source_url,category,title,description,actionable_steps,effort_level,roi_potential,risk_level,applies_to_niches,status,reviewed_date,reviewer_notes
```

### Field Definitions

- **alpha_id:** ALPHA[NNN] (auto-increment from last entry)
- **source:** @handle of X account
- **source_url:** Direct URL to tweet
- **category:** APP_FACTORY | CONTENT_FORMAT | OUTBOUND | GROWTH_HACK | TOOL_ALPHA | MONETIZATION
- **title:** First 100 chars of tweet or extracted summary
- **description:** Full tweet text (up to 500 chars)
- **actionable_steps:** Specific steps to implement (manual review adds detail)
- **effort_level:** LOW | MEDIUM | HIGH
- **roi_potential:** LOW | MEDIUM | HIGH | HIGHEST
- **risk_level:** LOW | MEDIUM | HIGH
- **applies_to_niches:** AI | Faith | Fitness | ALL
- **status:** PENDING_REVIEW (human approves before integration)
- **reviewed_date:** Set after human review
- **reviewer_notes:** Human adds context/decisions

### Alpha ID Generation

```python
import hashlib

def generate_alpha_id(tweet_url):
    """
    Generate unique alpha ID from tweet URL.
    Format: ALPHA[6-char hash]
    """
    hash_obj = hashlib.md5(tweet_url.encode())
    return f"ALPHA{hash_obj.hexdigest()[:6].upper()}"

# Example: ALPHA3F2A1C
```

---

## Automation Schedule

### Daily (Automated via Cron)

**Time:** 9 AM ± 2 hours (random offset)

**Script:** `AUTOMATIONS/scripts/daily_timeline_scraper.py`

**Targets:**
- 11 HIGHEST-tier accounts
- Last 20 tweets per account
- ~220 tweets total
- Runtime: ~15-20 minutes

**Cron entry:**
```bash
# Add to crontab
0 9 * * * cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT && /usr/bin/python3 AUTOMATIONS/scripts/daily_timeline_scraper.py >> AUTOMATIONS/logs/daily_scraper.log 2>&1
```

### Weekly (Automated)

**Time:** Sunday 10 AM

**Script:** `AUTOMATIONS/scripts/weekly_bookmark_sync.py`

**Workflow:**
1. User manually exports bookmarks via browser console (5 min)
2. Places JSON in `x_bookmarks/` folder
3. Cron job extracts alpha from latest bookmark file
4. Appends to ALPHA_STAGING.csv

### On-Demand (Manual)

**Targeted searches:**
```bash
# Search for specific topics
python AUTOMATIONS/scripts/search_alpha.py --query "cold email deliverability" --max-tweets 50

# Search for revenue mentions
python AUTOMATIONS/scripts/search_alpha.py --query '"$50k mrr"' --sort Latest --max-tweets 100
```

---

## Monitoring & Quality Control

### Logging

```python
# AUTOMATIONS/logs/scraper.log

import logging

logging.basicConfig(
    filename='AUTOMATIONS/logs/scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log key events
logger.info(f"Scraped {len(tweets)} tweets from {account}")
logger.warning(f"Rate limited, waiting 60s")
logger.error(f"Failed to scrape {account}: {error}")
```

### Metrics to Track

```python
# AUTOMATIONS/logs/scraper_metrics.json

{
    "last_run": "2026-01-22T09:15:00",
    "accounts_scraped": 11,
    "tweets_collected": 218,
    "alpha_findings": 14,
    "alpha_saved": 9,  # After dedup
    "failures": 0,
    "runtime_seconds": 1235
}
```

### Quality Checks

```python
def validate_findings(findings):
    """
    Quality checks before saving to ALPHA_STAGING.csv
    """
    valid = []

    for finding in findings:
        # Must have description
        if not finding.description or len(finding.description) < 50:
            logger.warning(f"Rejected: Description too short for {finding.alpha_id}")
            continue

        # Must have source URL
        if not finding.source_url or 'x.com' not in finding.source_url:
            logger.warning(f"Rejected: Invalid source URL for {finding.alpha_id}")
            continue

        # Must have valid category
        valid_categories = ['APP_FACTORY', 'CONTENT_FORMAT', 'OUTBOUND', 'GROWTH_HACK', 'TOOL_ALPHA', 'MONETIZATION']
        if finding.category not in valid_categories:
            logger.warning(f"Rejected: Invalid category '{finding.category}' for {finding.alpha_id}")
            continue

        valid.append(finding)

    return valid
```

---

## Integration with Daily Research Workflow

### Current Workflow (See `ralph_tasks/00_daily_alpha_research.md`)

1. **Scan sources** - Daily scraper runs automatically
2. **Extract findings** - Twitter scanner analyzes tweets
3. **Append to ALPHA_STAGING.csv** - Auto-save with PENDING_REVIEW status
4. **Human review** - User reviews ALPHA_STAGING.csv daily
5. **Approve/reject** - User changes status to APPROVED or REJECTED
6. **Integrate** - Approved alpha moves to master files:
   - `APP_FACTORY_METHODS.csv`
   - `MARKETING_CHANNELS_MASTER.csv`
   - `WINNING_CONTENT_STRUCTURES.csv`
   - `TOOL_STACK.csv`

### Twitter Scraper Enhancements

**Add to daily research command:**
```bash
# .claude/commands/daily-research.sh

#!/bin/bash
set -e

echo "Running daily alpha research..."

# 1. Scrape Twitter accounts
python3 AUTOMATIONS/scripts/daily_timeline_scraper.py

# 2. Process bookmarks (if new file exists)
latest_bookmark=$(ls -t AUTOMATIONS/x_bookmarks/x_bookmarks_*.json 2>/dev/null | head -1)
if [ -f "$latest_bookmark" ]; then
    python3 AUTOMATIONS/x_bookmarks/extract_alpha_from_bookmarks.py "$latest_bookmark"
fi

# 3. Scrape Reddit (existing)
python3 AUTOMATIONS/scripts/reddit_scraper.py

# 4. Generate daily report
python3 AUTOMATIONS/scripts/daily_report_generator.py

echo "Alpha research complete. Review LEDGER/ALPHA_STAGING.csv"
```

---

## Advanced Features (Future Enhancements)

### 1. Thread Unwinding

Extract full Twitter threads (not just single tweets):

```python
async def scrape_full_thread(scraper, tweet_url):
    """
    Follow thread and extract all tweets in conversation.
    """
    await scraper._page.goto(tweet_url)

    # Click "Show more replies" until all loaded
    while True:
        show_more = await scraper._page.query_selector('button:has-text("Show more replies")')
        if not show_more:
            break
        await show_more.click()
        await asyncio.sleep(1)

    # Extract all tweets in thread
    thread_tweets = await scraper._page.query_selector_all('[data-testid="tweet"]')
    # Process...
```

### 2. Media/Image Analysis

Extract images and analyze for charts, screenshots, data:

```python
async def extract_tweet_images(element):
    """
    Extract images from tweet for OCR or visual analysis.
    """
    images = await element.query_selector_all('img[alt="Image"]')
    urls = []

    for img in images:
        src = await img.get_attribute('src')
        if src and 'media' in src:
            urls.append(src)

    return urls

# Use OCR to extract text from screenshots
import pytesseract
from PIL import Image
import requests

def ocr_tweet_image(image_url):
    """
    Extract text from tweet screenshot using OCR.
    """
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    text = pytesseract.image_to_string(img)
    return text
```

### 3. Sentiment Analysis

Classify tweet sentiment to prioritize positive case studies over complaints:

```python
from textblob import TextBlob

def analyze_sentiment(text):
    """
    Determine if tweet is positive (success) or negative (failure).
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.1:
        return 'POSITIVE'  # Success story
    elif polarity < -0.1:
        return 'NEGATIVE'  # Failure or complaint
    else:
        return 'NEUTRAL'

# Tag findings with sentiment
finding.sentiment = analyze_sentiment(tweet.content)
```

### 4. Link Expansion

Follow links in tweets to extract full articles/threads:

```python
async def expand_links_in_tweet(tweet_text):
    """
    Extract URLs and fetch content for additional context.
    """
    urls = re.findall(r'https?://[^\s]+', tweet_text)

    expanded = []
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            # Extract title, description, or full text
            expanded.append({
                'url': url,
                'title': extract_title(response.text),
                'content': extract_content(response.text)[:500]
            })
        except:
            continue

    return expanded
```

---

## Testing & Validation

### Test Script

```python
# AUTOMATIONS/tests/test_twitter_scraper.py

import asyncio
from scripts.source_scrapers.twitter_scraper import TwitterScraper

async def test_scraper():
    """
    Test scraper on known account.
    """
    scraper = TwitterScraper(headless=False)  # Visible for debugging

    try:
        await scraper.initialize()

        # Test profile scrape
        tweets = await scraper.scrape_account('https://x.com/levelsio', max_tweets=5)

        print(f"\n=== Test Results ===")
        print(f"Tweets scraped: {len(tweets)}")

        for tweet in tweets:
            print(f"\n{tweet['handle']}: {tweet['text'][:100]}...")
            print(f"  Engagement: {tweet['likes']} likes, {tweet['retweets']} RTs")
            print(f"  URL: {tweet['url']}")

        assert len(tweets) > 0, "Should scrape at least 1 tweet"
        assert all('text' in t for t in tweets), "All tweets should have text"
        assert all('url' in t for t in tweets), "All tweets should have URL"

        print("\n✅ All tests passed")

    finally:
        await scraper.close()

if __name__ == '__main__':
    asyncio.run(test_scraper())
```

### Run Tests

```bash
# Test scraper functionality
python3 AUTOMATIONS/tests/test_twitter_scraper.py

# Test alpha detection
python3 AUTOMATIONS/tests/test_alpha_detection.py

# Test full pipeline
python3 AUTOMATIONS/tests/test_daily_pipeline.py
```

---

## Troubleshooting

### Problem: Scraper gets rate limited

**Solution:**
```python
# Increase delays between requests
self._min_delay = 5.0  # Up from 2.0

# Add random sleep between accounts
await asyncio.sleep(random.uniform(10, 20))

# Use residential proxy (not datacenter)
# Check proxy IP reputation
```

### Problem: Tweets not loading

**Solution:**
```python
# Increase timeout
page.set_default_timeout(60000)  # 60 seconds

# Wait for network idle longer
await page.goto(url, wait_until='networkidle', timeout=60000)

# Scroll to trigger lazy loading
await page.evaluate("window.scrollBy(0, 500)")
await asyncio.sleep(2)
```

### Problem: Session expired (logged out)

**Solution:**
```python
# Save session more frequently
await context.storage_state(path='sessions/x_session.json')

# Re-login flow
async def ensure_logged_in(page):
    """
    Check if logged in, re-auth if needed.
    """
    await page.goto('https://x.com/home')

    # Check for login page
    login_button = await page.query_selector('a[href="/login"]')
    if login_button:
        logger.warning("Session expired, need to re-login")
        # Trigger manual login or use stored credentials
        raise Exception("Login required")
```

### Problem: Proxy blocked by Twitter

**Solution:**
```python
# Rotate to fresh proxy
# Check proxy quality at whoer.net

# Switch to mobile proxy for critical accounts
PROXY_CONFIG = {
    'server': 'http://proxy.soax.com:9000',
    'username': 'user-mobile-country-US-sessionduration-30',
    'password': os.getenv('SOAX_PASSWORD')
}

# Test proxy before scraping
async def test_proxy():
    page = await context.new_page()
    await page.goto('https://whoer.net')
    # Check if IP is clean
```

---

## Security & Compliance

### Account Safety

1. **Use burner account** for scraping (not main @PRINTMAXXER account)
2. **Warm account** for 7-14 days before automation (see `ACCOUNT_WARMING_SOP.md`)
3. **Residential proxy** assigned to account (log in `LEDGER/proxy_assignments.csv`)
4. **Human-like behavior** (variable delays, scrolling)

### Rate Limit Respect

- Max 100 requests per hour per account
- Max 20 tweets per account per scrape
- Min 2 seconds between requests
- Min 3 seconds between accounts

### Data Privacy

- Don't scrape private accounts
- Don't scrape DMs
- Only public timeline data
- Respect robots.txt (X doesn't allow scraping, but this is for research)

### Legal Considerations

**This is a grey area.** Twitter TOS prohibits scraping. Mitigation:
- Use for personal research only (not commercial resale)
- Scrape public data only
- Rate limit aggressively
- Don't bypass authentication
- Stop if account flagged

**Alternative:** Use X API if budget allows ($100/mo Basic tier). This scraper is backup/fallback.

---

## Cost Analysis

### Infrastructure Costs

| Component | Monthly Cost | Notes |
|-----------|--------------|-------|
| Residential proxy (Decodo 5GB) | $50 | Daily scraping of 11 accounts |
| Mobile proxy (Soax 3GB) | $99 | Optional for bookmark scraping |
| VPS for automation (optional) | $0-20 | Only if running 24/7 |
| **Total (minimal)** | **$50** | Just residential proxy |
| **Total (recommended)** | **$149** | Residential + mobile |

### Alternative: X API Costs

| Tier | Monthly Cost | Limits |
|------|--------------|--------|
| Free | $0 | 1,500 tweets/month (useless) |
| Basic | $100 | 10,000 tweets/month |
| Pro | $5,000 | 1M tweets/month |

**Playwright scraping saves $100+/mo vs X API Basic.**

---

## Migration Path (API → Scraping)

If currently using X API and want to migrate:

**Step 1:** Keep API for low-volume, high-value use cases
- Posting from @PRINTMAXXER account
- Real-time mentions monitoring
- Direct engagement

**Step 2:** Use scraping for high-volume research
- Daily timeline scraping (11 accounts × 20 tweets = 220/day)
- Bookmark batch processing
- Search queries

**Step 3:** Monitor for rate limits
- If scraped account gets flagged, pause 7 days
- If repeated issues, fall back to API for that account

**Hybrid approach is best:** API for critical features, scraping for research.

---

## Related Documents

- `AUTOMATIONS/SOCIAL_AUTOMATION_STRATEGY.md` - Overall automation approach
- `AUTOMATIONS/ACCOUNT_WARMING_SOP.md` - Account warming before automation
- `AUTOMATIONS/SOAX_MOBILE_PROXIES.md` - Mobile proxy setup for IG/TikTok (applicable to X)
- `AUTOMATIONS/PROXY_COMPARISON.md` - Decodo vs Soax comparison
- `AUTOMATIONS/x_bookmarks/QUICK_START.md` - Manual bookmark extraction
- `LEDGER/HIGH_SIGNAL_SOURCES.csv` - 56+ tracked sources
- `LEDGER/ALPHA_STAGING.csv` - Alpha findings output
- `ralph_tasks/00_daily_alpha_research.md` - Daily research workflow

---

## Quick Start

### Immediate Setup (Today)

1. **Install dependencies:**
```bash
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT
pip install playwright requests beautifulsoup4 tenacity
playwright install chromium
```

2. **Test scraper:**
```bash
python3 AUTOMATIONS/tests/test_twitter_scraper.py
```

3. **Run first scrape:**
```bash
python3 AUTOMATIONS/scripts/daily_timeline_scraper.py
```

4. **Review findings:**
```bash
# Open LEDGER/ALPHA_STAGING.csv
# Review new entries with status=PENDING_REVIEW
```

5. **Set up cron (optional):**
```bash
crontab -e
# Add daily scraper job
0 9 * * * cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT && /usr/bin/python3 AUTOMATIONS/scripts/daily_timeline_scraper.py >> AUTOMATIONS/logs/daily_scraper.log 2>&1
```

---

**Last updated:** 2026-01-22
**Status:** Ready for implementation
**Next steps:** Test scraper → Set up proxy → Run daily for 7 days → Evaluate quality
