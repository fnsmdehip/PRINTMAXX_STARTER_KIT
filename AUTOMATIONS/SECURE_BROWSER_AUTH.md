# Secure Browser Authentication (No Password Storage)

## The Problem
You need scrapers to run with your logged-in Twitter/Reddit accounts, but don't want passwords in env files or code.

## The Solution
**One-time manual login. Session persists. No passwords stored anywhere.**

---

## Setup (One Time - 5 Minutes)

### Step 1: Launch Chrome with Debugging + Separate Profile

```bash
# This creates a SEPARATE Chrome profile just for scraping
# Your main Chrome stays untouched

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.printmaxx-chrome-profile" \
  &
```

### Step 2: Log Into Your Accounts (Manual, One Time)

In the Chrome window that opens:
1. Go to twitter.com → Log in normally
2. Go to reddit.com → Log in normally
3. Check "Remember me" / "Stay logged in"
4. Close the browser

### Step 3: Done

The session cookies are now saved in `~/.printmaxx-chrome-profile/`

When you run the scraper, it uses this profile with your existing session. No login needed.

---

## Running Scrapers

### Option A: Launch Chrome with profile, then run scraper

```bash
# Terminal 1: Launch Chrome (runs in background)
./AUTOMATIONS/launch_chrome_debug.sh

# Terminal 2: Run scraper (connects to running Chrome)
python3 AUTOMATIONS/parallel_twitter_scraper.py
```

### Option B: Headless mode with saved profile

```python
# Uses saved cookies without opening visible browser
browser = await playwright.chromium.launch_persistent_context(
    user_data_dir="~/.printmaxx-chrome-profile",
    headless=True
)
```

---

## Security

**What's stored:** Session cookies (encrypted by Chrome)
**What's NOT stored:** Your password (never enters any file)
**If computer stolen:** Attacker would need your Mac password to access profile
**If Claude hacked:** No password to leak - only session tokens that expire

---

## Refreshing Session

If session expires (usually 30+ days):
1. Run `./AUTOMATIONS/launch_chrome_debug.sh`
2. Go to twitter.com, log in again
3. Close browser
4. Session refreshed for another 30+ days

---

## Quick Commands

```bash
# First time setup (creates profile + opens Chrome for login)
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.printmaxx-chrome-profile"

# Daily: Launch Chrome with saved session
./AUTOMATIONS/launch_chrome_debug.sh

# Daily: Run Twitter scraper
python3 AUTOMATIONS/parallel_twitter_scraper.py

# Daily: Run Reddit scraper
python3 AUTOMATIONS/daily_reddit_scraper.py
```

**No passwords. No env files. Just saved browser session.**
