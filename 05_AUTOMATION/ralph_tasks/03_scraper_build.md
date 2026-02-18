---
task_id: SCRAPE-001
test_command: "python3 AUTOMATIONS/scripts/scrape_twitter_account.py --test"
max_iterations: 25
completion_signal: "SCRAPER_COMPLETE"
---

# Task: Build Twitter/X scraper for source accounts

## Context
- Read AUTOMATIONS/PROXY_COMPARISON.md for proxy setup
- Output to AUTOMATIONS/scripts/scrape_twitter_account.py
- Create directory if needed

## Requirements

### Core Functionality
1. Scrape tweets from given account handle
2. Extract: text, media URLs, engagement metrics (likes, RTs, views)
3. Save to CSV with metadata
4. Proxy support (Soax/Decodo format)
5. Rate limit handling
6. Human-like delays

### CLI Interface
```bash
# Basic usage
python scrape_twitter_account.py --account FearedBuck --count 100

# With proxy
python scrape_twitter_account.py --account kirawontmiss --count 50 --proxy user:pass@gate.soax.com:port

# Date range
python scrape_twitter_account.py --account HumansNoContext --days 30

# Test mode
python scrape_twitter_account.py --test
```

### Output Format (CSV)
```csv
id,account,text,media_urls,likes,retweets,replies,views,timestamp,scraped_at
```

## Technical Specs

### Playwright Setup
```python
from playwright.sync_api import sync_playwright
import random
import time

# Human-like delays
def human_delay():
    time.sleep(random.uniform(2, 5))

# Scroll behavior
def natural_scroll(page):
    page.mouse.wheel(0, random.randint(300, 700))
    human_delay()
```

### Proxy Configuration
```python
proxy_config = {
    "server": f"http://{proxy_host}:{proxy_port}",
    "username": proxy_user,
    "password": proxy_pass
}
browser = playwright.chromium.launch(proxy=proxy_config)
```

### Rate Limit Handling
- Max 100 tweets per scrape session
- 5-10 second delay between scroll actions
- Detect "rate limit" messages and back off
- Save progress incrementally

## Success Criteria
1. [ ] Script runs without errors
2. [ ] Scrapes at least 50 tweets from test account
3. [ ] Saves to CSV correctly
4. [ ] Proxy support works
5. [ ] --test flag runs basic validation
6. [ ] Human-like timing (no bot patterns)
7. [ ] Error handling for common failures

## File Structure
```python
#!/usr/bin/env python3
"""
Twitter/X Account Scraper
Scrapes tweets with engagement metrics for content repurposing.
"""

import argparse
import csv
import random
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

# ... implementation ...

if __name__ == "__main__":
    main()
```

## When complete
Run test: `python3 AUTOMATIONS/scripts/scrape_twitter_account.py --test`
If passes: <promise>SCRAPER_COMPLETE</promise>
