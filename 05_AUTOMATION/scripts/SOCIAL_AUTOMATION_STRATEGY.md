# Social Automation Strategy

How to automate posting using Claude in Chrome + Playwright.

---

## Automation Options Comparison

| Method | Safety | Speed | Setup | Best For |
|--------|--------|-------|-------|----------|
| Official APIs (Buffer/Hypefury) | Safest | Slow | Easy | Main accounts |
| Claude in Chrome Extension | Medium | Medium | Easy | Supervised automation |
| Playwright + Proxies | Risky | Fast | Complex | Burner/warmed accounts |
| Selenium | Risky | Fast | Complex | Legacy scripts |

---

## Option 1: Claude in Chrome (Recommended Start)

You have the Claude in Chrome MCP tools available. This is perfect for supervised automation.

### How It Works
1. You open browser with target site
2. Claude navigates and performs actions
3. You watch in real-time
4. Can intervene if anything goes wrong

### Use Cases
- Posting pre-written content to X/Twitter
- Scheduling posts via native schedulers
- Copying content between platforms
- Filling forms on multiple sites

### Example Flow: Post to X
```
1. Navigate to x.com
2. Find compose button
3. Type content
4. Click post
5. Verify posted
6. Move to next
```

### Safety Advantages
- Uses your real browser session
- Your real IP (no proxy detection)
- Your logged-in state
- Human timing (you control pace)

### Limitations
- Requires you to be present
- One browser at a time
- Can't run while sleeping

---

## Option 2: Playwright Headless (Scale)

For unattended, multi-account automation.

### Setup Requirements
```bash
# Install
pip install playwright
playwright install chromium

# Or with Node
npm init playwright@latest
```

### Basic X Posting Script Structure
```python
# AUTOMATIONS/scripts/x_poster.py

from playwright.sync_api import sync_playwright
import time
import random

def post_to_x(content: str, proxy: dict = None):
    """
    Post content to X/Twitter.

    proxy format: {
        "server": "http://user:pass@proxy.example.com:port",
    }
    """
    with sync_playwright() as p:
        # Browser config
        browser_args = []
        if proxy:
            browser = p.chromium.launch(
                headless=False,  # Set True for production
                proxy=proxy
            )
        else:
            browser = p.chromium.launch(headless=False)

        # Use persistent context (stays logged in)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
            viewport={"width": 1280, "height": 720}
        )

        page = context.new_page()

        # Navigate
        page.goto("https://x.com/compose/tweet")

        # Wait for compose box
        page.wait_for_selector('[data-testid="tweetTextarea_0"]')

        # Human-like typing delay
        for char in content:
            page.keyboard.type(char)
            time.sleep(random.uniform(0.05, 0.15))

        # Random pause before posting
        time.sleep(random.uniform(1, 3))

        # Click post
        page.click('[data-testid="tweetButton"]')

        # Verify
        time.sleep(2)

        browser.close()

# Usage
# post_to_x("Testing automated posting")
```

### Multi-Account Handler
```python
# AUTOMATIONS/scripts/multi_account_poster.py

import json
from pathlib import Path

ACCOUNTS_FILE = Path("LEDGER/social_accounts.json")
CONTENT_QUEUE = Path("LEDGER/content_queue.csv")

def load_accounts():
    """Load account configs with proxy assignments."""
    with open(ACCOUNTS_FILE) as f:
        return json.load(f)

def get_next_content(account_id: str):
    """Get next piece of content for this account."""
    # Read from queue, mark as used
    pass

def post_all_accounts():
    """Post to all accounts with appropriate delays."""
    accounts = load_accounts()

    for account in accounts:
        content = get_next_content(account["id"])
        if not content:
            continue

        # Load saved session
        post_with_session(
            session_path=account["session_path"],
            proxy=account["proxy"],
            content=content
        )

        # Delay between accounts (anti-detection)
        time.sleep(random.uniform(300, 600))  # 5-10 min
```

### Session Management
```python
# Save logged-in state
context.storage_state(path=f"sessions/{account_id}.json")

# Reuse later
context = browser.new_context(
    storage_state=f"sessions/{account_id}.json"
)
```

---

## Option 3: Hybrid Approach (Best)

Combine methods based on account importance:

### Main Accounts (Personal Brand)
- Method: Official APIs only (Buffer, Hypefury)
- Why: Zero ban risk, your reputation
- Automation: Scheduling, not posting

### Secondary Accounts (Niche Brands)
- Method: Claude in Chrome (supervised)
- Why: Can monitor, intervene
- Automation: Batch posting sessions

### Burner/Test Accounts
- Method: Playwright + residential proxies
- Why: Acceptable loss if banned
- Automation: Full unattended

---

## Content Queue System

### Structure
```
LEDGER/content_queue.csv

id,account_id,platform,content,media_path,scheduled_time,status,posted_at
1,faith_main,x,"Content here",/path/to/image.jpg,2026-01-21T09:00,pending,
2,fitness_main,x,"Content here",,2026-01-21T10:00,pending,
```

### Status Values
- `pending` - Ready to post
- `scheduled` - In platform scheduler
- `posted` - Successfully posted
- `failed` - Error, needs review
- `skipped` - Manually skipped

### Workflow
1. Generate content batch (I do this)
2. Review/approve (you do this)
3. Add to queue (automated)
4. Post via appropriate method
5. Update status
6. Track performance

---

## Anti-Detection Measures

### Browser Fingerprinting
```python
# Randomize viewport
viewport = {
    "width": random.choice([1280, 1366, 1440, 1920]),
    "height": random.choice([720, 768, 900, 1080])
}

# Realistic user agent
user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
]
```

### Human-Like Behavior
```python
# Variable delays
def human_delay(min_sec=1, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))

# Typing speed variation
def human_type(page, text):
    for char in text:
        page.keyboard.type(char)
        time.sleep(random.gauss(0.1, 0.03))  # Normal distribution

# Mouse movement
def human_mouse(page, target):
    # Move in steps, not instantly
    page.mouse.move(target.x, target.y, steps=random.randint(5, 15))
```

### Session Hygiene
- Different browser profile per account
- Consistent proxy per account
- Don't switch between accounts rapidly
- Maintain realistic activity patterns

---

## Deployment Checklist

### Local Development
- [ ] Python 3.11+ or Node 18+
- [ ] Playwright installed
- [ ] Browser drivers downloaded
- [ ] Test with single account first

### Production (If Running 24/7)
- [ ] VPS with GUI (for headed browser)
- [ ] Proxy rotation set up
- [ ] Session persistence
- [ ] Error logging
- [ ] Alert on failures

### Monitoring
- [ ] Track success/failure rate
- [ ] Monitor for rate limits
- [ ] Check account health daily
- [ ] Backup sessions regularly

---

## Quick Start: Post via Claude in Chrome

For immediate use with your MCP tools:

1. Open X in browser
2. Log in manually
3. Say: "Post this to X: [your content]"
4. I'll navigate and post
5. You verify success

This is the safest way to start. Graduate to Playwright once you have:
- Established accounts
- Proxy setup working
- Content queue built
- Time to monitor

---

Last updated: 2026-01-21
