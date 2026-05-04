---
title: "How to run 24/7 agent loops safely for data scraping | PrintMaxx"
description: "Autonomous scraping without destroying your IP. Rate limits, rotating proxies, dead-man switches. Architecture inside."
keywords: ["agent loops", "data scraping", "automation", "Playwright", "rate limiting"]
author: "PrintMaxx Team"
date: "2026-01-21"
published: true
canonical: "/longtail/how-to-run-24-7-agent-loops-safely-data-scraping"
---

# How to run 24/7 agent loops safely for data scraping

## Quick Answer

Use Playwright + cron + rotating proxies. Rate limit to 1 request per 3 seconds. Check for errors every 6 hours. Kill the loop if IP gets blocked. Cost: $0 (free Playwright + cron) to $50/mo (rotating proxies).

Running a scraper 24/7 without safeguards will get you blocked in 48 hours. This guide keeps you safe.

## The Danger

Most solopreneurs kill their scraper fast because they:
- Don't rotate proxies (IP gets burned)
- Don't respect rate limits (get 429s)
- Don't monitor for failures (scraper runs blindly)
- Don't have exit conditions (loop runs forever even after block)

Result: Dead IP in days. Wasted time.

## Safe Setup

### 1. Playwright + Cron Job

```bash
# Run every 3 hours, check for success
0 */3 * * * /usr/bin/python3 /path/to/scraper.py >> /var/log/scraper.log 2>&1
```

The cron runs your script periodically instead of continuously. If the script fails, cron retries at the next interval.

### 2. Rate Limiting (Critical)

```python
import time

def safe_scrape(urls):
    for url in urls:
        # Fetch one URL every 3 seconds
        time.sleep(3)  # Wait 3 seconds between requests
        response = playwright.get(url)

        # If 429 (rate limit), back off
        if response.status == 429:
            time.sleep(300)  # Wait 5 minutes, try again
            continue
```

One request per 3 seconds = 1,200 requests per hour = 28,800 per day. That's safe.

### 3. Rotating Proxies (Optional but Safer)

If scraping publicly:
- Soax.com: $5-20/mo for residential proxies
- Bright Data: $100/mo (overkill for most)
- Free option: Use 3-4 VPNs (less reliable)

```python
from playwright.async_api import async_playwright

async def scrape_with_proxy(url):
    proxy = "http://proxy-ip:port"
    async with async_playwright() as p:
        browser = await p.chromium.launch(proxy={"server": proxy})
```

Rotate proxy every 50 requests.

### 4. Dead-Man Switch (Prevent Runaway Loops)

```python
import time
import os

MAX_CONSECUTIVE_FAILURES = 3
consecutive_failures = 0

for url in urls:
    try:
        response = playwright.get(url)
        if response.status >= 400:
            consecutive_failures += 1
        else:
            consecutive_failures = 0  # Reset on success
    except Exception as e:
        consecutive_failures += 1

    # Kill loop if 3 failures in a row
    if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
        print("IP likely blocked. Stopping.")
        exit(1)  # Exit, cron won't retry
```

### 5. Monitoring (Check Every 6 Hours)

Create a simple health check:

```python
# At the start of each run
def check_health():
    test_url = "https://httpbin.org/status/200"
    try:
        response = playwright.get(test_url)
        return response.status == 200
    except:
        return False

if not check_health():
    print("Network failure. Exiting.")
    exit(1)
```

Log every run:
```
2026-01-21 09:00 - Fetched 47 URLs, 0 errors
2026-01-21 12:00 - Fetched 48 URLs, 0 errors
2026-01-21 15:00 - ERROR: 3 consecutive failures, exiting
```

## Real Example: Safe Scraper

```python
import time
import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def scrape_safely(urls):
    consecutive_failures = 0
    proxies = ["proxy1", "proxy2", "proxy3"]
    proxy_idx = 0

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        for i, url in enumerate(urls):
            try:
                # Rotate proxy every 50 requests
                if i % 50 == 0:
                    proxy = proxies[proxy_idx % len(proxies)]
                    proxy_idx += 1

                # Rate limit
                time.sleep(3)

                # Fetch
                page.goto(url)
                data = page.inner_html("body")

                logger.info(f"Success: {url}")
                consecutive_failures = 0

            except Exception as e:
                consecutive_failures += 1
                logger.warning(f"Fail #{consecutive_failures}: {url}")

                if consecutive_failures >= 3:
                    logger.error("Too many failures. Exiting.")
                    browser.close()
                    exit(1)

        browser.close()

if __name__ == "__main__":
    urls = ["url1", "url2", "url3"]  # Load from CSV
    scrape_safely(urls)
```

## Cost Breakdown

- Playwright: Free
- Cron (Linux/Mac): Free
- Rotating proxies (Soax): $5-20/mo
- Bandwidth: Free (if self-hosted)

Total: $5-20/mo if using proxies, $0 if scraping your own data.

## Red Flags

- Getting 429s (rate limit too high)
- Getting 403s (IP blocked, need proxy)
- Script runs for 12+ hours without exiting (infinite loop bug)
- No logs (can't debug)

## Related

- [How to schedule data scraping automation with cron + Playwright](/longtail/how-to-schedule-data-scraping-cron-playwright)
- [Best open-source tools for data scraping automation](/truth/best-open-source-tools-data-scraping)

## Next Steps

1. Pick 100 URLs to scrape
2. Write safe scraper (copy code above)
3. Test with rate limit 3 sec, no proxy
4. Add proxies if getting blocked
5. Set cron to run every 3 hours
6. Monitor logs for 1 week
7. Scale to 1000+ URLs once stable
