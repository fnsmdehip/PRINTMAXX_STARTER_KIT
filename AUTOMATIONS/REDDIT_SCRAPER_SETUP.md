## Reddit Alpha Scraper - Implementation Guide

**Current Status:** Template structure created, needs Reddit API integration

**What It Does:**
1. **Daily scraping** of research + launch subreddits (40 total)
2. **Meta detection** - identifies trending topics, viral products, meme coins
3. **Alpha extraction** - tactics, tools, methods from high-signal posts/comments
4. **Meme coin signals** - detects early mentions for backtesting trading patterns
5. **Content opportunities** - trending topics to repost for social media visibility

---

## Implementation Options

### Option 1: PRAW (Python Reddit API Wrapper) - RECOMMENDED

**Pros:**
- Official Reddit API wrapper
- Rate limiting handled automatically
- Authentication built-in
- Most reliable

**Setup:**
```bash
pip install praw
```

**Reddit API Credentials (Manual Setup Required):**
1. Go to https://www.reddit.com/prefs/apps
2. Click "create another app..."
3. Select "script"
4. Name: "PRINTMAXX Research Bot"
5. Redirect URI: http://localhost:8080
6. Copy client_id, client_secret

**Add to .env:**
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=PRINTMAXX/1.0
```

**Code Integration:**
Replace `scrape_subreddit()` in reddit_alpha_scraper.py:

```python
import praw
import os

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

def scrape_subreddit(subreddit_name: str, time_filter: str = 'week') -> List[Dict]:
    """Scrape top posts from a subreddit using PRAW."""
    posts = []

    subreddit = reddit.subreddit(subreddit_name.replace('r/', ''))

    for post in subreddit.top(time_filter=time_filter, limit=25):
        posts.append({
            'post_id': post.id,
            'title': post.title,
            'selftext': post.selftext,
            'url': f"https://reddit.com{post.permalink}",
            'score': post.score,
            'num_comments': post.num_comments,
            'created_utc': post.created_utc,
            'author': str(post.author),
            'subreddit': subreddit_name,
        })

    return posts

def scrape_post_comments(post_url: str, depth: int = 2) -> List[Dict]:
    """Scrape comments from a post using PRAW."""
    comments = []

    submission = reddit.submission(url=post_url)
    submission.comments.replace_more(limit=0)  # Flatten comment tree

    def extract_comment(comment, current_depth=1):
        if current_depth > depth:
            return

        comments.append({
            'comment_id': comment.id,
            'body': comment.body,
            'score': comment.score,
            'author': str(comment.author),
            'created_utc': comment.created_utc,
            'depth': current_depth,
        })

        for reply in comment.replies:
            extract_comment(reply, current_depth + 1)

    for top_comment in submission.comments:
        extract_comment(top_comment)

    return comments
```

---

### Option 2: Reddit JSON API (No Auth) - QUICK START

**Pros:**
- No Reddit account needed
- No API credentials
- Works immediately

**Cons:**
- Rate limited (60 requests/min)
- No voting, posting, commenting capabilities
- Less reliable long-term

**Code Integration:**
```python
import requests
import time

def scrape_subreddit(subreddit_name: str, time_filter: str = 'week') -> List[Dict]:
    """Scrape using public JSON API."""
    url = f"https://www.reddit.com{subreddit_name}/top.json?t={time_filter}&limit=25"

    headers = {'User-Agent': 'PRINTMAXX/1.0'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        log(f"Error: {response.status_code}")
        return []

    data = response.json()
    posts = []

    for post_data in data['data']['children']:
        post = post_data['data']
        posts.append({
            'post_id': post['id'],
            'title': post['title'],
            'selftext': post.get('selftext', ''),
            'url': f"https://reddit.com{post['permalink']}",
            'score': post['score'],
            'num_comments': post['num_comments'],
            'created_utc': post['created_utc'],
            'author': post['author'],
            'subreddit': subreddit_name,
        })

    time.sleep(1)  # Rate limiting
    return posts

def scrape_post_comments(post_url: str, depth: int = 2) -> List[Dict]:
    """Scrape comments using JSON API."""
    url = f"{post_url}.json"

    headers = {'User-Agent': 'PRINTMAXX/1.0'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    data = response.json()
    comments = []

    def extract_comments(comment_list, current_depth=1):
        if current_depth > depth or not comment_list:
            return

        for item in comment_list:
            if item['kind'] == 't1':  # Comment type
                c = item['data']
                comments.append({
                    'comment_id': c['id'],
                    'body': c['body'],
                    'score': c['score'],
                    'author': c['author'],
                    'created_utc': c['created_utc'],
                    'depth': current_depth,
                })

                if 'replies' in c and c['replies']:
                    extract_comments(
                        c['replies']['data']['children'],
                        current_depth + 1
                    )

    if len(data) > 1:
        extract_comments(data[1]['data']['children'])

    time.sleep(1)  # Rate limiting
    return comments
```

---

### Option 3: Playwright Browser Automation - MOST RELIABLE

**Pros:**
- No API limits
- Handles Reddit login (can access private subs if needed)
- Most human-like behavior (less likely to be rate limited)

**Cons:**
- Slower than API
- More complex

**Setup:**
```bash
pip install playwright
playwright install chromium
```

**Code Integration:**
Similar to twitter_alpha_scraper.py - use Chrome MCP or Playwright to navigate Reddit pages and extract data.

---

## Meta Detection Signals

### 1. Meme Coin Signals (For Backtesting)

**Patterns to detect:**
- New coin mentions with "agent", "AI", specific character names
- Launch timing (presale, drop date mentions)
- Community velocity (rapid comment growth in 1-2 hours)

**Backtesting approach:**
1. Log every coin mention with timestamp
2. Track price action from CoinGecko/DEXScreener
3. Identify patterns: "First Reddit mention → Price 10x within 24h"
4. Test: If pattern appears, what's optimal entry/exit?

**Historical examples to backtest:**
- Molt bot agent coin (mentioned in your message)
- Studio Ghibli coin
- Other agent/AI themed coins

**Output:** `LEDGER/MEME_COIN_SIGNALS.csv`

### 2. Meta of the Day/Week Detection

**What makes something "meta":**
- 3+ posts in top 25 of different subreddits mentioning same topic within 24h
- Rapid upvote velocity (1K+ upvotes in <6h)
- Cross-platform confirmation (Reddit + Twitter both buzzing)

**Categories:**
- AI products (Claude MCP, new tools)
- Viral apps/tools (went viral on Product Hunt)
- Platform changes (TikTok algorithm update)
- Arbitrage opportunities (underpriced service/product)

**Use cases:**
- **Trading:** Meme coin early entry signals
- **Content:** Repost trending topics for visibility on social media
- **Alpha:** Extract tactics before they're mainstream

**Output:** `LEDGER/META_TRACKER.csv`

---

## Daily Workflow

**Run daily (automated via cron or ralph loop):**

```bash
# Full scrape (all 40 subreddits)
python3 AUTOMATIONS/reddit_alpha_scraper.py

# Then review findings
python3 AUTOMATIONS/organize_alpha.py  # Categorize new alpha
tail -50 LEDGER/META_TRACKER.csv       # Check trending meta
tail -20 LEDGER/MEME_COIN_SIGNALS.csv  # Check coin signals
```

**Integration with existing workflow:**
1. Reddit scraper runs daily (like Twitter scraper)
2. New alpha → ALPHA_STAGING.csv (PENDING_REVIEW)
3. Meta signals → META_TRACKER.csv (track trends)
4. Meme coins → MEME_COIN_SIGNALS.csv (backtest for trading)
5. Human reviews via `/review-alpha`

---

## Content Repurposing Strategy

**When meta is detected, auto-generate content:**

### Example: "Molt bot agent coin" meta detected

**Immediate actions:**
1. **Twitter/X post:**
   ```
   molt bot went from reddit meme to $2M market cap in 18 hours

   pattern: AI agent launches → community spawns token →
   early mentions = 10-50x window

   [link to analysis]
   ```

2. **Thread breakdown:**
   - How it started (bot announcement)
   - Community reaction velocity
   - Coin launch timing
   - Price action timeline
   - Lessons for next time

3. **Medium article:**
   "How Reddit Memes Become Million-Dollar Tokens: The Molt Bot Case Study"

4. **Newsletter angle:**
   "Meta of the Week: AI Agent Tokens"

5. **Trading signal (if backtested pattern confirmed):**
   - Alert on new agent launches
   - Entry criteria: First Reddit mention + >100 upvotes in 1h
   - Exit criteria: 10x or 24h elapsed

---

## Next Steps (Manual)

**To activate Reddit scraper:**

1. **Choose implementation option** (PRAW recommended)
2. **Get Reddit API credentials** (5 min manual setup)
3. **Add credentials to .env**
4. **Replace template functions** with chosen implementation
5. **Test on 1-2 subreddits first**
6. **Run full scrape**
7. **Automate via cron** or add to ralph loop

**Estimated setup time:** 30-60 minutes for full implementation

---

## Output Files

| File | Purpose |
|------|---------|
| `LEDGER/ALPHA_STAGING.csv` | Actionable alpha (tactics, tools, methods) |
| `LEDGER/META_TRACKER.csv` | Trending topics/meta (3+ mentions in 24h) |
| `LEDGER/MEME_COIN_SIGNALS.csv` | Early coin mentions for backtesting |
| `AUTOMATIONS/reddit_scraper_output/*.json` | Raw JSON backups |
| `AUTOMATIONS/logs/reddit_scraper.log` | Execution logs |

---

## Meme Coin Backtesting Framework

**Goal:** Identify profitable entry patterns for agent/AI themed meme coins

**Data to collect:**
- First Reddit mention timestamp
- Post score at detection
- Comment velocity (comments per hour)
- Coin launch timestamp (if mentioned)
- Price data from CoinGecko/DEXScreener

**Patterns to test:**
1. "First mention on r/CryptoCurrency with >100 upvotes → Buy within 1h"
2. "Agent bot announcement → Community creates coin → Buy when first mentioned"
3. "3+ related posts in 6h → Probable pump incoming"

**Backtest metrics:**
- Win rate (% of signals that 2x+)
- Average return per signal
- Time to peak (median hours from detection to ATH)
- False positive rate (% that go to zero)

**Implementation:**
1. Log every signal to CSV with timestamp
2. Manually add price data after 7 days
3. Calculate returns from entry to 24h/48h/7d
4. Identify winning patterns
5. Build automated alert system for future signals
