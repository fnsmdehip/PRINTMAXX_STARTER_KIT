# Playwright Automation Scripts

Social media automation tools for engagement and research.

These scripts are designed for **quality engagement** and **market research**, not spam.

---

## Setup

### Prerequisites

1. Python 3.11+
2. Playwright installed

### Installation

```bash
# Install dependencies
pip install playwright

# Download browser binaries
playwright install chromium
```

### Session Setup

Before running engagement scripts, you need to manually log in and save a session.

```bash
# Create sessions directory
mkdir -p sessions

# Launch browser to login manually
python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); b = p.chromium.launch(headless=False); c = b.new_context(); page = c.new_page(); page.goto('https://x.com/login'); input('Press Enter after logging in...'); c.storage_state(path='sessions/twitter.json'); b.close(); p.stop()"
```

This saves your login session to `sessions/twitter.json` for reuse.

---

## Scripts

### 1. twitter_engagement.py

Engages with tweets from HIGH_SIGNAL_SOURCES accounts.

**What it does:**
- Likes tweets from tracked accounts
- Replies with genuine, contextual comments
- Logs all actions to CSV

**Usage:**
```bash
# Basic usage
python twitter_engagement.py --session sessions/twitter.json

# With limits
python twitter_engagement.py --session sessions/twitter.json --max-likes 15 --max-replies 5

# With proxy
python twitter_engagement.py --session sessions/twitter.json --proxy "http://user:pass@proxy:port"
```

**Options:**
- `--session, -s`: Path to session file (required)
- `--max-likes, -l`: Max likes this session (default: 10)
- `--max-replies, -r`: Max replies this session (default: 3)
- `--headless`: Run without visible browser
- `--proxy`: Proxy server URL

**Logs to:**
- `LEDGER/ENGAGEMENT_LOG.csv`

---

### 2. reddit_monitor.py

Monitors subreddits for opportunities and keywords.

**What it does:**
- Scans subreddits for keyword matches
- Scores opportunities by relevance
- Logs all findings for manual review
- Read-only (no posting or voting)

**Usage:**
```bash
# Use subreddits from HIGH_SIGNAL_SOURCES.csv
python reddit_monitor.py --use-sources

# Custom subreddits
python reddit_monitor.py --subreddits "SideProject,indiehackers" --keywords "automation,passive income"

# With proxy
python reddit_monitor.py --use-sources --proxy "http://user:pass@proxy:port"
```

**Options:**
- `--subreddits, -s`: Comma-separated subreddit names
- `--keywords, -k`: Comma-separated keywords to match
- `--max-posts, -m`: Posts per subreddit (default: 25)
- `--min-score`: Minimum score to log (default: 2)
- `--headed`: Show browser window
- `--proxy`: Proxy server URL
- `--use-sources`: Load from HIGH_SIGNAL_SOURCES.csv

**Logs to:**
- `LEDGER/REDDIT_OPPORTUNITIES.csv`

---

### 3. youtube_commenter.py

Finds relevant YouTube videos and optionally leaves comments.

**What it does:**
- Searches for videos by keywords
- Logs videos found for analysis
- Posts contextual comments (if not research-only)
- Simulates watching for legitimacy

**Usage:**
```bash
# Research only (safe mode)
python youtube_commenter.py --research-only --search "indie hacker tutorial"

# With commenting
python youtube_commenter.py --session sessions/youtube.json --search "solopreneur tools" --max-comments 2

# Multiple searches
python youtube_commenter.py --session sessions/youtube.json --search "side project" --search "passive income"
```

**Options:**
- `--session, -s`: Path to session file (required for commenting)
- `--search`: Search query (can use multiple)
- `--max-comments, -c`: Max comments (default: 3)
- `--research-only, -r`: Find videos but don't comment
- `--headless`: Run without browser
- `--proxy`: Proxy server URL

**Logs to:**
- `LEDGER/YOUTUBE_VIDEOS_FOUND.csv`
- `LEDGER/YOUTUBE_COMMENTS_LOG.csv`

---

### 4. tiktok_scraper.py

Scrapes TikTok for trending sounds, hashtags, and content patterns.

**What it does:**
- Scrapes hashtag pages for videos
- Tracks trending sounds
- Analyzes content hook types
- Read-only research tool

**Usage:**
```bash
# Scrape by niche
python tiktok_scraper.py --niches "business,tech"

# Scrape specific hashtags
python tiktok_scraper.py --hashtags "solopreneur,sideproject"

# With proxy (strongly recommended)
python tiktok_scraper.py --niches "business" --proxy "http://user:pass@proxy:port"
```

**Options:**
- `--hashtags, -t`: Comma-separated hashtags (no #)
- `--niches, -n`: business, tech, faith, fitness
- `--max-videos, -m`: Videos per hashtag (default: 20)
- `--headed`: Show browser
- `--proxy`: Proxy server URL (recommended)

**Logs to:**
- `LEDGER/TIKTOK_TRENDS.csv`
- `LEDGER/TIKTOK_SOUNDS.csv`
- `LEDGER/TIKTOK_HASHTAGS.csv`
- `LEDGER/TIKTOK_CONTENT_PATTERNS.csv`

---

## Proxy Setup

### Why Use Proxies

- Avoid IP bans (especially TikTok/Instagram)
- Appear as different users
- Geographic targeting
- Rate limit distribution

### Proxy Providers

See `AUTOMATIONS/PROXY_COMPARISON.md` for detailed comparison.

**Recommended:**
- **Residential**: Soax, Decodo
- **Mobile** (Instagram/TikTok): Soax Mobile

### Proxy Format

```bash
# HTTP proxy
--proxy "http://username:password@proxy.example.com:port"

# SOCKS5 proxy
--proxy "socks5://username:password@proxy.example.com:port"
```

---

## Rate Limits

These scripts have conservative built-in rate limits to avoid detection.

| Platform | Action | Delay | Daily Max |
|----------|--------|-------|-----------|
| Twitter | Like | 5-12s | 50 |
| Twitter | Reply | 30-60s | 15 |
| Reddit | Page load | 2-5s | - |
| YouTube | Comment | 60-120s | 5 |
| TikTok | Hashtag scrape | 8-15s | - |

**Exceeding these limits risks account flags or bans.**

---

## CSV Log Files

All scripts log to LEDGER CSVs for tracking and review.

| Script | Output File |
|--------|-------------|
| twitter_engagement.py | ENGAGEMENT_LOG.csv |
| reddit_monitor.py | REDDIT_OPPORTUNITIES.csv |
| youtube_commenter.py | YOUTUBE_VIDEOS_FOUND.csv, YOUTUBE_COMMENTS_LOG.csv |
| tiktok_scraper.py | TIKTOK_*.csv |

---

## Safety Guidelines

### Do

- Start with research-only modes
- Use proxies for TikTok/Instagram
- Review opportunities before acting
- Maintain human-like timing
- Log everything for audit

### Don't

- Run 24/7 unattended
- Use on main/personal accounts
- Exceed daily limits
- Spam or low-value comments
- Ignore captcha warnings

---

## Troubleshooting

### "Not logged in"

Session may be expired. Re-run manual login to save new session.

### Captcha detected

- Use residential/mobile proxy
- Reduce frequency
- Take longer breaks

### Element not found

TikTok/YouTube update frequently. Selectors may need updating.

### Proxy blocked

- Try different proxy location
- Switch proxy provider
- Use mobile proxy for strict platforms

---

## Architecture

```
playwright_scripts/
├── twitter_engagement.py    # Engagement automation
├── reddit_monitor.py        # Opportunity monitoring
├── youtube_commenter.py     # Video research + comments
├── tiktok_scraper.py        # Trend scraping
└── README.md               # This file

sessions/                    # Saved browser sessions (gitignored)
├── twitter.json
├── youtube.json
└── ...

LEDGER/                      # CSV output logs
├── ENGAGEMENT_LOG.csv
├── REDDIT_OPPORTUNITIES.csv
├── YOUTUBE_*.csv
└── TIKTOK_*.csv
```

---

## Related Files

- `AUTOMATIONS/SOCIAL_AUTOMATION_STRATEGY.md` - Strategy overview
- `AUTOMATIONS/PROXY_COMPARISON.md` - Proxy provider comparison
- `AUTOMATIONS/ACCOUNT_WARMING_SOP.md` - Account warming protocols
- `LEDGER/HIGH_SIGNAL_SOURCES.csv` - Target accounts/sources
- `AUTOMATIONS/social/twitter_warmup.py` - Account warmup script

---

Last updated: 2026-01-21
