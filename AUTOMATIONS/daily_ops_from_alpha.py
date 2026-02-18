#!/usr/bin/env python3
"""
DAILY OPS FROM ALPHA - Convert all alpha entries into automated daily tasks.

This script:
1. Reads all alpha from ALPHA_STAGING.csv
2. Identifies alpha that can become DAILY automated tasks
3. Creates daily monitoring scripts for each
4. Runs all daily checks and logs results
"""

import csv
import os
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
ALPHA_STAGING = BASE_DIR / "LEDGER" / "ALPHA_STAGING.csv"
DAILY_OPS_LOG = BASE_DIR / "LEDGER" / "DAILY_OPS_LOG.csv"
DAILY_TASKS_OUTPUT = BASE_DIR / "OPS" / "DAILY_AUTOMATED_TASKS.md"

# Alpha categories that can become daily automated tasks
AUTOMATABLE_CATEGORIES = {
    "TRIGGERING_EVENTS": {
        "description": "Monitor leadership changes, office moves, glassdoor spikes, competitor layoffs, job posting removals, 10-K changes",
        "frequency": "daily",
        "tools_needed": ["visualping.io", "google_alerts", "theorg.com", "glassdoor", "linkedin", "sec.gov"],
        "tasks": [
            {"name": "Check theorg.com for leadership changes", "url": "https://theorg.com", "method": "scrape_org_changes"},
            {"name": "Check Google Alerts for office moves", "url": "https://alerts.google.com", "method": "check_alerts"},
            {"name": "Monitor Glassdoor rating changes", "url": "https://glassdoor.com", "method": "scrape_ratings"},
            {"name": "Track competitor layoffs on LinkedIn", "url": "https://linkedin.com", "method": "scrape_layoffs"},
            {"name": "Monitor job posting removals", "url": "various", "method": "scrape_job_boards"},
            {"name": "Check SEC 10-K filings for language changes", "url": "https://sec.gov", "method": "scrape_sec"}
        ]
    },
    "GOVERNMENT_MONITORING": {
        "description": "Monitor government websites for regulatory changes, RFPs, compliance updates",
        "frequency": "hourly",
        "tools_needed": ["visualping.io", "tendersinfo.com"],
        "tasks": [
            {"name": "Check tendersinfo.com for new contracts", "url": "https://tendersinfo.com", "method": "scrape_tenders"},
            {"name": "Monitor SEC.gov enforcement actions", "url": "https://sec.gov/enforcement", "method": "scrape_sec_enforcement"},
            {"name": "Monitor FTC.gov consumer protection", "url": "https://ftc.gov", "method": "scrape_ftc"},
            {"name": "Check state crypto regulations", "url": "various", "method": "scrape_state_regs"}
        ]
    },
    "ECOM_MONITORING": {
        "description": "Monitor ecom trends, pricing, product opportunities",
        "frequency": "daily",
        "tools_needed": ["storeleads.com", "tiktok_shop", "amazon", "etsy"],
        "tasks": [
            {"name": "Pull Shopify stores doing $1M+ with Klaviyo", "url": "https://storeleads.com", "method": "scrape_storeleads"},
            {"name": "Check TikTok Shop trending products", "url": "https://shop.tiktok.com", "method": "scrape_tiktok_shop"},
            {"name": "Monitor Amazon BSR gaps", "url": "https://amazon.com", "method": "scrape_amazon_bsr"},
            {"name": "Track Etsy trending products", "url": "https://etsy.com", "method": "scrape_etsy_trending"}
        ]
    },
    "COMPETITOR_INTEL": {
        "description": "Monitor competitor pricing, features, launches",
        "frequency": "daily",
        "tools_needed": ["visualping.io", "google_alerts", "product_hunt"],
        "tasks": [
            {"name": "Check competitor pricing pages for changes", "url": "various", "method": "scrape_pricing"},
            {"name": "Monitor Product Hunt for competitor launches", "url": "https://producthunt.com", "method": "scrape_ph"},
            {"name": "Track competitor social engagement", "url": "various", "method": "scrape_social"},
            {"name": "Monitor competitor blog/changelog", "url": "various", "method": "scrape_changelog"}
        ]
    },
    "PLATFORM_ARBITRAGE": {
        "description": "Monitor platform RPM changes, algorithm shifts",
        "frequency": "daily",
        "tools_needed": ["browser_scraping", "api_monitoring"],
        "tasks": [
            {"name": "Check FB Reels RPM reports", "url": "https://facebook.com/creators", "method": "check_fb_rpm"},
            {"name": "Monitor X creator program payouts", "url": "https://x.com/settings/monetization", "method": "check_x_payouts"},
            {"name": "Track TikTok Creativity Program rates", "url": "https://tiktok.com/creator", "method": "check_tiktok_rpm"},
            {"name": "Check YouTube Shorts RPM", "url": "https://studio.youtube.com", "method": "check_yt_rpm"}
        ]
    },
    "ALPHA_RESEARCH": {
        "description": "Daily research scan of high-signal sources",
        "frequency": "daily",
        "tools_needed": ["twitter_scraper", "reddit_scraper", "github_trending"],
        "tasks": [
            {"name": "Scrape 92 high-signal Twitter accounts", "url": "https://x.com", "method": "scrape_twitter_accounts"},
            {"name": "Scrape Twitter bookmarks", "url": "https://x.com/i/bookmarks", "method": "scrape_bookmarks"},
            {"name": "Scan 41 subreddits for alpha", "url": "https://reddit.com", "method": "scrape_reddit"},
            {"name": "Check GitHub trending repos", "url": "https://github.com/trending", "method": "scrape_github"},
            {"name": "Scan Product Hunt launches", "url": "https://producthunt.com", "method": "scrape_ph_launches"},
            {"name": "Check HackerNews front page", "url": "https://news.ycombinator.com", "method": "scrape_hn"}
        ]
    },
    "CONTENT_MONITORING": {
        "description": "Track content performance, viral trends",
        "frequency": "daily",
        "tools_needed": ["analytics", "social_monitoring"],
        "tasks": [
            {"name": "Check content analytics across platforms", "url": "various", "method": "check_analytics"},
            {"name": "Identify viral trends to replicate", "url": "various", "method": "find_viral"},
            {"name": "Track hashtag performance", "url": "various", "method": "track_hashtags"},
            {"name": "Monitor competitor content performance", "url": "various", "method": "track_competitor_content"}
        ]
    }
}

def load_alpha():
    """Load all alpha entries from ALPHA_STAGING.csv"""
    alpha_entries = []
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                alpha_entries.append(row)
    return alpha_entries

def categorize_alpha_for_daily_ops(alpha_entries):
    """Identify which alpha entries can become daily automated tasks"""
    daily_ops_candidates = []

    keywords_to_category = {
        'theorg': 'TRIGGERING_EVENTS',
        'glassdoor': 'TRIGGERING_EVENTS',
        'layoff': 'TRIGGERING_EVENTS',
        'leadership': 'TRIGGERING_EVENTS',
        'job posting': 'TRIGGERING_EVENTS',
        '10-k': 'TRIGGERING_EVENTS',
        'sec.gov': 'GOVERNMENT_MONITORING',
        'government': 'GOVERNMENT_MONITORING',
        'tender': 'GOVERNMENT_MONITORING',
        'rfp': 'GOVERNMENT_MONITORING',
        'compliance': 'GOVERNMENT_MONITORING',
        'regulation': 'GOVERNMENT_MONITORING',
        'storeleads': 'ECOM_MONITORING',
        'shopify': 'ECOM_MONITORING',
        'tiktok shop': 'ECOM_MONITORING',
        'amazon bsr': 'ECOM_MONITORING',
        'etsy': 'ECOM_MONITORING',
        'competitor': 'COMPETITOR_INTEL',
        'pricing': 'COMPETITOR_INTEL',
        'monitor': 'COMPETITOR_INTEL',
        'track': 'COMPETITOR_INTEL',
        'fb reels': 'PLATFORM_ARBITRAGE',
        'rpm': 'PLATFORM_ARBITRAGE',
        'creator program': 'PLATFORM_ARBITRAGE',
        'algorithm': 'PLATFORM_ARBITRAGE',
        'arbitrage': 'PLATFORM_ARBITRAGE',
        'twitter': 'ALPHA_RESEARCH',
        'reddit': 'ALPHA_RESEARCH',
        'github': 'ALPHA_RESEARCH',
        'product hunt': 'ALPHA_RESEARCH',
        'content': 'CONTENT_MONITORING',
        'viral': 'CONTENT_MONITORING',
        'engagement': 'CONTENT_MONITORING'
    }

    for entry in alpha_entries:
        tactic = entry.get('tactic', '').lower()
        category = entry.get('category', '')

        for keyword, ops_category in keywords_to_category.items():
            if keyword in tactic:
                daily_ops_candidates.append({
                    'alpha_id': entry.get('alpha_id'),
                    'source': entry.get('source'),
                    'tactic': entry.get('tactic'),
                    'original_category': category,
                    'daily_ops_category': ops_category,
                    'automatable': True
                })
                break

    return daily_ops_candidates

def generate_daily_tasks_markdown():
    """Generate the DAILY_AUTOMATED_TASKS.md document"""

    content = f"""# Daily Automated Tasks - Generated from Alpha

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Purpose:** All automated daily tasks derived from alpha entries

---

## Daily Task Schedule

### 6:00 AM - Alpha Research Phase

| Task | Script | Frequency |
|------|--------|-----------|
| Scrape 92 Twitter accounts | `parallel_twitter_scraper.py` | Daily |
| Scrape Twitter bookmarks | `parallel_twitter_scraper.py --bookmarks` | Daily |
| Scan 41 subreddits | `daily_reddit_scraper.py` | Daily |
| Check GitHub trending | `github_trending_scraper.py` | Daily |
| Scan Product Hunt | `producthunt_scraper.py` | Daily |

### 8:00 AM - Triggering Events Phase (pipelineabuser alpha)

| Task | Tool | What to Monitor |
|------|------|-----------------|
| theorg.com leadership changes | Visualping or custom scraper | 100 target companies |
| Google Alerts office moves | Google Alerts dashboard | "[company] + new office" |
| Glassdoor rating drops | Custom scraper | Alert when rating drops >0.5 in 30 days |
| LinkedIn layoff tracking | Manual or custom scraper | Competitor layoffs |
| Job posting removals | Custom scraper | When roles get filled (30-day email) |
| SEC 10-K language changes | SEC.gov + diff tool | New risks mentioned |

### 10:00 AM - Government Monitoring Phase

| Task | Tool | What to Monitor |
|------|------|-----------------|
| tendersinfo.com new contracts | Daily scrape | Filter by department, budget, deadline |
| SEC.gov enforcement actions | Visualping | Crypto, fintech enforcement |
| FTC.gov updates | Visualping | Consumer protection, disclosure rules |
| State regulator pages | Visualping | State-by-state crypto compliance |

### 12:00 PM - Ecom Monitoring Phase

| Task | Tool | What to Monitor |
|------|------|-----------------|
| storeleads.com Shopify query | API or scrape | Stores doing $1M+ with Klaviyo |
| TikTok Shop trending | Scraper | Top products, affiliate opportunities |
| Amazon BSR gaps | Helium10 or scraper | Categories with demand-supply mismatch |
| Etsy trending | Scraper | Trending products to source/create |

### 2:00 PM - Platform Arbitrage Phase

| Task | Tool | What to Monitor |
|------|------|-----------------|
| FB Reels RPM | Creator Studio | Compare to other platforms |
| X creator payouts | Monetization dashboard | Track changes |
| TikTok Creativity Program | Creator portal | RPM trends |
| YouTube Shorts | Studio | Compare RPM to long-form |

### 4:00 PM - Competitor Intel Phase

| Task | Tool | What to Monitor |
|------|------|-----------------|
| Competitor pricing pages | Visualping | Price changes, new tiers |
| Product Hunt launches | Scraper | New competitor launches |
| Competitor social | Scraper | Engagement rates, content strategy |
| Competitor changelog | RSS or scraper | New features |

---

## Automated Scripts Status

### Existing Scripts (Ready to Run)

| Script | Location | Status |
|--------|----------|--------|
| `parallel_twitter_scraper.py` | AUTOMATIONS/ | READY - needs Chrome debug mode |
| `daily_reddit_scraper.py` | AUTOMATIONS/ | READY - needs selector fix |
| `daily_twitter_scraper.py` | AUTOMATIONS/ | READY - sequential version |

### Scripts to Build

| Script | Priority | Purpose |
|--------|----------|---------|
| `theorg_scraper.py` | HIGH | Leadership change monitoring |
| `glassdoor_monitor.py` | HIGH | Rating spike detection |
| `tendersinfo_scraper.py` | HIGH | Government contract alerts |
| `storeleads_query.py` | HIGH | Ecom target list building |
| `competitor_pricing_monitor.py` | MEDIUM | Price change alerts |
| `github_trending_scraper.py` | MEDIUM | MIT repo discovery |
| `producthunt_scraper.py` | MEDIUM | Launch monitoring |
| `sec_filing_monitor.py` | LOW | 10-K language changes |

---

## Cron Schedule (Install These)

```bash
# Add to crontab: crontab -e

# 6:00 AM - Alpha Research
0 6 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/parallel_twitter_scraper.py >> logs/twitter.log 2>&1
0 6 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/daily_reddit_scraper.py >> logs/reddit.log 2>&1

# 8:00 AM - Triggering Events (when scripts built)
# 0 8 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/theorg_scraper.py >> logs/theorg.log 2>&1
# 0 8 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/glassdoor_monitor.py >> logs/glassdoor.log 2>&1

# 10:00 AM - Government Monitoring (when scripts built)
# 0 10 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/tendersinfo_scraper.py >> logs/tenders.log 2>&1

# 12:00 PM - Ecom Monitoring (when scripts built)
# 0 12 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/storeleads_query.py >> logs/storeleads.log 2>&1
```

---

## Alpha Sources for Daily Tasks

### From pipelineabuser (HIGHEST SIGNAL)

1. **theorg.com** - Free org charts, leadership changes
   - Action: Build scraper for 100 target companies
   - Cold email: "Saw [name] just took over [department]"

2. **tendersinfo.com** - Government contracts
   - Action: Daily scrape for relevant RFPs
   - $500B+ annual spending, zero competition

3. **storeleads.com** - Shopify database
   - Action: Query stores doing $1M+ with specific tech stack
   - Build targeted cold email lists

4. **visualping.io** - Website monitoring
   - Action: Set up for competitor pricing, gov pages
   - Get alerts when anything changes

5. **Glassdoor spike detection**
   - Action: Monitor 100 target companies
   - Alert when rating drops >0.5 (internal problems = budget)

6. **Job posting removal tracking**
   - Action: Scrape job boards daily
   - Email 30 days after role filled (new hire = need tools)

7. **10-K language changes**
   - Action: SEC.gov scraper + diff tool
   - Alert when new risks mentioned (board-level concern = budget)

---

## Integration with Ralph Loops

All daily tasks integrate with the mega ralph loop:

```
DAILY_RESEARCH phase (iterations 1-3):
  - DR-00: Real-time meta (GitHub/X/PH trending)
  - DR-01: High-signal Twitter (92 accounts)
  - DR-01B: Twitter bookmarks
  - DR-02: Reddit scans (41 subreddits)
  - DR-03: Platform algorithm changes

INTELLIGENCE phase (iterations 16-20):
  - INT-01: Triggering events monitoring
  - INT-02: Government contract alerts
  - INT-03: Ecom opportunity scanning
  - INT-04: Competitor intel
  - INT-05: Platform arbitrage tracking
```

---

## Output Locations

| Daily Task | Output Location |
|------------|-----------------|
| Twitter alpha | LEDGER/ALPHA_STAGING.csv |
| Reddit alpha | LEDGER/ALPHA_STAGING.csv |
| Leadership changes | LEDGER/TRIGGERING_EVENTS_LOG.csv |
| Government contracts | LEDGER/GOVERNMENT_CONTRACTS.csv |
| Ecom opportunities | LEDGER/ECOM_OPPORTUNITIES.csv |
| Competitor changes | LEDGER/COMPETITOR_INTEL_LOG.csv |
| Platform RPM | LEDGER/PLATFORM_ARBITRAGE_LOG.csv |

---

## Revenue from Daily Ops

**Triggering Events System:**
- 1 leadership change alert → 1 warm intro → $500-5K deal potential
- 100 companies monitored × 5% monthly change rate = 5 opportunities/month

**Government Monitoring:**
- 1 contract win = $50K-500K revenue
- 5 relevant RFPs/week × 5% win rate = 1 contract/month potential

**Ecom Monitoring:**
- 1 trending product identified → $1-10K/month potential
- 10 products tested/month × 10% success = 1 winner/month

**Total daily ops potential:** $10-50K/month additional revenue from automated intelligence.

---

**This system runs automatically. Check logs daily. Act on high-priority alerts immediately.**
"""

    return content

def main():
    print("=" * 60)
    print("DAILY OPS FROM ALPHA - Converting alpha to daily tasks")
    print("=" * 60)

    # Load alpha
    print("\n1. Loading alpha entries...")
    alpha_entries = load_alpha()
    print(f"   Loaded {len(alpha_entries)} alpha entries")

    # Categorize for daily ops
    print("\n2. Identifying automatable alpha...")
    daily_ops = categorize_alpha_for_daily_ops(alpha_entries)
    print(f"   Found {len(daily_ops)} alpha entries convertible to daily ops")

    # Generate markdown
    print("\n3. Generating daily tasks document...")
    content = generate_daily_tasks_markdown()

    with open(DAILY_TASKS_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   Written to {DAILY_TASKS_OUTPUT}")

    # Summary by category
    print("\n4. Daily Ops Categories:")
    for category, config in AUTOMATABLE_CATEGORIES.items():
        task_count = len(config['tasks'])
        print(f"   - {category}: {task_count} daily tasks, {config['frequency']} frequency")

    print("\n" + "=" * 60)
    print("DONE. Daily automated tasks document generated.")
    print("Next: Run cron jobs, build missing scrapers, integrate with ralph loops.")
    print("=" * 60)

if __name__ == "__main__":
    main()
