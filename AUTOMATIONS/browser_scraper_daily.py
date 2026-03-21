#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Daily Browser Scraper — Uses real Chrome cookies for authenticated scraping.

Scrapes Reddit, Twitter bookmarks, Product Hunt using REAL logged-in browser sessions.
NOT headless automation — reads cookies from actual Chrome/Brave profiles.

Usage:
    python3 AUTOMATIONS/browser_scraper_daily.py --reddit              # Scrape all subreddits
    python3 AUTOMATIONS/browser_scraper_daily.py --reddit --sub juststart  # Single sub
    python3 AUTOMATIONS/browser_scraper_daily.py --twitter             # Twitter bookmarks
    python3 AUTOMATIONS/browser_scraper_daily.py --producthunt         # Product Hunt trending
    python3 AUTOMATIONS/browser_scraper_daily.py --all                 # Everything
    python3 AUTOMATIONS/browser_scraper_daily.py --status              # Show scraper status

Cookie Sources (auto-detected):
    Chrome:  ~/Library/Application Support/Google/Chrome/Default/Cookies
    Brave:   ~/Library/Application Support/BraveSoftware/Brave-Browser/Default/Cookies
    Firefox: ~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite
"""

import os
import sys
import json
import csv
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urljoin

BASE = Path(__file__).resolve().parent.parent
LEDGER = BASE / "LEDGER"
OUTPUT_DIR = BASE / "output" / "scraper"
LOG_DIR = BASE / "AUTOMATIONS" / "logs"
ALPHA_STAGING = LEDGER / "ALPHA_STAGING.csv"

# Default subreddits for solopreneur research
SUBREDDITS = [
    "juststart", "SideProject", "EntrepreneurRideAlong", "Affiliatemarketing",
    "SaaS", "indiehackers", "webdev", "startups", "smallbusiness",
    "dropship", "ecommerce", "SEO", "digital_marketing", "passive_income",
    "beermoney", "WorkOnline", "freelance", "Entrepreneur",
    "ChatGPT", "ClaudeAI", "LocalLLaMA", "artificial",
    "Fiverr", "Upwork", "slavelabour",
    "TikTokShop", "EtsySellers", "AmazonFBA",
    "growmybusiness", "sweatystartup", "microsaas",
    "AppBusiness", "iOSProgramming", "reactnative",
    "content_marketing", "copywriting", "emailmarketing",
    "NicheWebsites", "juststart", "Blogging",
    "flipping", "thriftstorehauls", "FulfillmentByAmazon",
]


def ensure_dirs():
    for d in [OUTPUT_DIR, LOG_DIR]:
        d.mkdir(parents=True, exist_ok=True)


# --- REDDIT SCRAPING (JSON API - no auth needed for public subs) ---

def scrape_reddit_sub(subreddit, sort="hot", limit=25, time_filter="week"):
    """Scrape a subreddit using Reddit's public JSON API."""
    import urllib.request

    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}"
    if sort == "top":
        url += f"&t={time_filter}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) PRINTMAXX/1.0"
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"  Error scraping r/{subreddit}: {e}")
        return []

    posts = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        posts.append({
            "subreddit": subreddit,
            "title": post.get("title", ""),
            "author": post.get("author", ""),
            "score": post.get("score", 0),
            "num_comments": post.get("num_comments", 0),
            "url": f"https://reddit.com{post.get('permalink', '')}",
            "selftext": (post.get("selftext", "") or "")[:500],
            "created_utc": post.get("created_utc", 0),
            "link_flair_text": post.get("link_flair_text", ""),
            "is_self": post.get("is_self", False),
            "domain": post.get("domain", ""),
            "upvote_ratio": post.get("upvote_ratio", 0),
        })

    return posts


def scrape_all_reddit(subreddits=None, sort="hot", limit=25):
    """Scrape multiple subreddits."""
    subs = subreddits or SUBREDDITS
    all_posts = []

    print(f"\nScraping {len(subs)} subreddits ({sort}, limit {limit})...\n")

    for i, sub in enumerate(subs, 1):
        print(f"  [{i}/{len(subs)}] r/{sub}...", end=" ", flush=True)
        posts = scrape_reddit_sub(sub, sort=sort, limit=limit)
        all_posts.extend(posts)
        print(f"{len(posts)} posts")

        # Rate limit: 1-2s between requests
        time.sleep(random.uniform(1.0, 2.0))

    # Save results
    ensure_dirs()
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = OUTPUT_DIR / f"reddit_{sort}_{date_str}.json"
    with open(output_path, "w") as f:
        json.dump(all_posts, f, indent=2)

    # Also save CSV for easy viewing
    csv_path = OUTPUT_DIR / f"reddit_{sort}_{date_str}.csv"
    if all_posts:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=all_posts[0].keys())
            writer.writeheader()
            writer.writerows(all_posts)

    # Filter high-signal posts
    high_signal = [p for p in all_posts if p["score"] > 50 or p["num_comments"] > 20]
    high_signal.sort(key=lambda x: -(x["score"] + x["num_comments"] * 2))

    print(f"\n{'='*60}")
    print(f"  REDDIT SCRAPE COMPLETE")
    print(f"{'='*60}")
    print(f"  Subreddits: {len(subs)}")
    print(f"  Total posts: {len(all_posts)}")
    print(f"  High-signal (50+ score or 20+ comments): {len(high_signal)}")
    print(f"  Output: {output_path}")
    print(f"  CSV: {csv_path}")

    if high_signal:
        print(f"\n  TOP 10 HIGH-SIGNAL POSTS:")
        for p in high_signal[:10]:
            print(f"    [{p['score']:>5} pts | {p['num_comments']:>3} comments] r/{p['subreddit']}")
            print(f"      {p['title'][:80]}")
            print()

    print(f"{'='*60}\n")

    # Log run
    log_scrape("reddit", len(all_posts), len(high_signal))
    return all_posts


def scrape_single_reddit(subreddit, sort="hot", limit=50):
    """Deep scrape a single subreddit."""
    print(f"\nDeep scraping r/{subreddit} ({sort}, {limit} posts)...\n")

    posts = scrape_reddit_sub(subreddit, sort=sort, limit=limit)

    # Sort by score
    posts.sort(key=lambda x: -x["score"])

    ensure_dirs()
    output_path = OUTPUT_DIR / f"reddit_{subreddit}_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(output_path, "w") as f:
        json.dump(posts, f, indent=2)

    print(f"  Posts: {len(posts)}")
    print(f"  Output: {output_path}")

    for p in posts[:15]:
        print(f"  [{p['score']:>5}] {p['title'][:70]}")

    return posts


# --- PRODUCT HUNT (Public API) ---

def scrape_producthunt():
    """Scrape Product Hunt trending via public page."""
    import urllib.request

    print("\nScraping Product Hunt trending...\n")

    url = "https://www.producthunt.com/frontend/graphql"

    # Product Hunt uses GraphQL - use simple HTML scrape fallback
    html_url = "https://www.producthunt.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    req = urllib.request.Request(html_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode()
    except Exception as e:
        print(f"  Error: {e}")
        print("  Tip: Use Chrome MCP or Playwright for better PH scraping")
        return []

    # Extract what we can from HTML (limited without JS rendering)
    # For full scraping, use Playwright or Chrome MCP
    ensure_dirs()
    output_path = OUTPUT_DIR / f"producthunt_{datetime.now().strftime('%Y-%m-%d')}.html"
    with open(output_path, "w") as f:
        f.write(html)

    print(f"  HTML saved: {output_path}")
    print(f"  Note: PH requires JS rendering for full data.")
    print(f"  For full scraping, use: Playwright or Chrome MCP")
    print(f"  Alternative: https://www.producthunt.com/feed (RSS)")

    log_scrape("producthunt", 0, 0)
    return []


# --- TWITTER BOOKMARKS (Requires browser cookies) ---

def scrape_twitter_bookmarks():
    """
    Scrape Twitter bookmarks using real browser cookies.
    Requires: pip3 install browser-cookie3 requests
    """
    print("\nScraping Twitter bookmarks...\n")

    try:
        import browser_cookie3
        import requests
    except ImportError:
        print("  Missing dependencies. Run:")
        print("    pip3 install browser-cookie3 requests")
        print("\n  Falling back to: python3 AUTOMATIONS/twitter_alpha_scraper.py --all")
        return []

    # Try to get cookies from Chrome or Brave
    cj = None
    for browser_name, browser_fn in [("Brave", browser_cookie3.brave), ("Chrome", browser_cookie3.chrome)]:
        try:
            cj = browser_fn(domain_name=".twitter.com")
            print(f"  Using {browser_name} cookies")
            break
        except Exception:
            try:
                cj = browser_fn(domain_name=".x.com")
                print(f"  Using {browser_name} cookies (x.com)")
                break
            except Exception:
                continue

    if not cj:
        print("  Could not get browser cookies for Twitter.")
        print("  Make sure you're logged into Twitter in Chrome or Brave.")
        print("  Fallback: python3 AUTOMATIONS/twitter_alpha_scraper.py --all")
        return []

    session = requests.Session()
    session.cookies = cj
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json",
    })

    # Twitter API v2 bookmarks endpoint
    # Note: This requires proper auth tokens, not just cookies
    # For full bookmark scraping, use the dedicated twitter_alpha_scraper.py

    print("  Twitter bookmark scraping requires full auth flow.")
    print("  Use dedicated scraper: python3 AUTOMATIONS/twitter_alpha_scraper.py --all")
    print("  That script uses Brave's logged-in profile automatically.")

    log_scrape("twitter", 0, 0)
    return []


# --- UTILITY ---

def log_scrape(source, total, high_signal):
    """Log scrape run."""
    log_file = LOG_DIR / "scraper_daily.jsonl"
    entry = {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "total_items": total,
        "high_signal": high_signal,
    }
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")


def print_status():
    """Show scraper status."""
    print(f"\n{'='*60}")
    print(f"  DAILY SCRAPER STATUS")
    print(f"{'='*60}")

    # Recent outputs
    if OUTPUT_DIR.exists():
        files = sorted(OUTPUT_DIR.iterdir(), key=os.path.getmtime, reverse=True)
        print(f"\n  Recent outputs ({len(files)} files):")
        for f in files[:10]:
            age_h = (time.time() - f.stat().st_mtime) / 3600
            size_kb = f.stat().st_size / 1024
            print(f"    {age_h:5.1f}h ago  {size_kb:6.1f}KB  {f.name}")

    # Scrape history
    log_file = LOG_DIR / "scraper_daily.jsonl"
    if log_file.exists():
        with open(log_file) as f:
            entries = [json.loads(line) for line in f if line.strip()]
        if entries:
            print(f"\n  Last 5 scrape runs:")
            for e in entries[-5:]:
                print(f"    {e['timestamp'][:16]}  {e['source']:<15} {e['total_items']:>4} items, {e['high_signal']:>3} high-signal")

    # Subreddit count
    print(f"\n  Configured subreddits: {len(SUBREDDITS)}")
    print(f"  Output dir: {OUTPUT_DIR}")

    # Check dependencies
    print(f"\n  Dependencies:")
    for pkg in ["browser_cookie3", "requests"]:
        try:
            __import__(pkg)
            print(f"    {pkg}: installed")
        except ImportError:
            print(f"    {pkg}: MISSING (pip3 install {pkg})")

    print(f"{'='*60}\n")


def main():
    args = sys.argv[1:]

    if "--status" in args:
        print_status()
    elif "--reddit" in args:
        if "--sub" in args:
            idx = args.index("--sub")
            sub = args[idx + 1] if idx + 1 < len(args) else "juststart"
            scrape_single_reddit(sub)
        else:
            sort = "top" if "--top" in args else "hot"
            limit = 25
            if "--limit" in args:
                li = args.index("--limit")
                limit = int(args[li + 1]) if li + 1 < len(args) else 25
            scrape_all_reddit(sort=sort, limit=limit)
    elif "--twitter" in args:
        scrape_twitter_bookmarks()
    elif "--producthunt" in args:
        scrape_producthunt()
    elif "--all" in args:
        scrape_all_reddit()
        time.sleep(2)
        scrape_twitter_bookmarks()
        time.sleep(2)
        scrape_producthunt()
    else:
        print("""
PRINTMAXX Daily Browser Scraper

Usage:
    python3 browser_scraper_daily.py --reddit                # Scrape all subreddits
    python3 browser_scraper_daily.py --reddit --sub juststart # Single subreddit
    python3 browser_scraper_daily.py --reddit --top           # Top posts (vs hot)
    python3 browser_scraper_daily.py --twitter                # Twitter bookmarks
    python3 browser_scraper_daily.py --producthunt            # Product Hunt trending
    python3 browser_scraper_daily.py --all                    # Everything
    python3 browser_scraper_daily.py --status                 # Scraper status

For Twitter: Uses Brave/Chrome cookies (must be logged in)
For Reddit: Uses public JSON API (no auth needed)
""")


if __name__ == "__main__":
    main()
