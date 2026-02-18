#!/usr/bin/env python3
"""
BACKGROUND TWITTER SCRAPER
==========================
Extracts cookies from Brave Browser and injects into a headless browser.
Your Brave stays open and untouched.

How it works:
- Reads Twitter cookies from Brave's encrypted cookie database
- Decrypts using cached Keychain key (.brave_cookie_key)
- Launches a fresh headless Chromium, injects cookies
- Scrapes high-signal accounts for actionable content
- Saves to ALPHA_STAGING.csv

Usage:
    python3 background_twitter_scraper.py --scrape       # Top 20 accounts
    python3 background_twitter_scraper.py --full          # ALL accounts
    python3 background_twitter_scraper.py --limit 5       # Custom limit
    nohup python3 background_twitter_scraper.py --full > /tmp/twitter_scrape.log 2>&1 &
"""

import asyncio
import csv
import re
import json
import argparse
import hashlib
import sqlite3
import shutil
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime, timedelta, timezone
from playwright.async_api import async_playwright

try:
    from Crypto.Cipher import AES
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False
    print("WARNING: pycryptodome not installed. Run: pip3 install pycryptodome")

# Paths
PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_DIR / "LEDGER"
ALPHA_STAGING = LEDGER_DIR / "ALPHA_STAGING.csv"
HIGH_SIGNAL_SOURCES = LEDGER_DIR / "HIGH_SIGNAL_SOURCES.csv"
OUTPUT_DIR = PROJECT_DIR / "AUTOMATIONS" / "twitter_scraper_output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Brave Browser paths
BRAVE_USER_DATA = Path.home() / "Library/Application Support/BraveSoftware/Brave-Browser"
BRAVE_KEY_FILE = PROJECT_DIR / "AUTOMATIONS" / ".brave_cookie_key"


def extract_twitter_cookies():
    """Extract and decrypt Twitter cookies from Brave's cookie database."""
    if not HAS_CRYPTO:
        print("ERROR: pycryptodome required. Run: pip3 install pycryptodome")
        return []

    cookie_db = BRAVE_USER_DATA / "Default" / "Cookies"
    if not cookie_db.exists():
        print(f"ERROR: Cookie database not found at {cookie_db}")
        return []

    # Get decryption key: cached file first, then Keychain
    keychain_pass = None
    if BRAVE_KEY_FILE.exists():
        keychain_pass = BRAVE_KEY_FILE.read_text().strip()

    if not keychain_pass:
        try:
            result = subprocess.run(
                ["security", "find-generic-password", "-s", "Brave Safe Storage", "-w"],
                capture_output=True, text=True, timeout=15
            )
            keychain_pass = result.stdout.strip()
            if keychain_pass:
                BRAVE_KEY_FILE.write_text(keychain_pass)
        except subprocess.TimeoutExpired:
            print("ERROR: Keychain timed out. Run manually:")
            print(f"  security find-generic-password -s 'Brave Safe Storage' -w > {BRAVE_KEY_FILE}")
            return []
        except Exception as e:
            print(f"ERROR: Keychain failed: {e}")
            return []

    if not keychain_pass:
        print("ERROR: No Brave cookie key available")
        return []

    # Derive AES key
    aes_key = hashlib.pbkdf2_hmac('sha1', keychain_pass.encode('utf-8'), b'saltysalt', 1003, dklen=16)

    # Copy cookie DB (Brave locks it while running)
    temp_db = tempfile.mktemp(suffix=".db", prefix="brave_cookies_")
    shutil.copy2(str(cookie_db), temp_db)

    cookies = []
    try:
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        # Get Twitter/X cookies
        cursor.execute(
            "SELECT host_key, name, path, encrypted_value, is_secure, is_httponly, "
            "expires_utc, samesite FROM cookies WHERE host_key = '.x.com' OR host_key = 'x.com'"
        )

        for row in cursor.fetchall():
            host_key, name, path, encrypted_value, is_secure, is_httponly, expires_utc, samesite = row

            value = ""
            if encrypted_value and encrypted_value[:3] == b'v10':
                iv = b' ' * 16
                enc_data = encrypted_value[3:]
                if len(enc_data) % 16 != 0:
                    enc_data += b'\x00' * (16 - len(enc_data) % 16)
                try:
                    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
                    decrypted = cipher.decrypt(enc_data)
                    pad_len = decrypted[-1]
                    if 0 < pad_len <= 16:
                        decrypted = decrypted[:-pad_len]
                    else:
                        decrypted = decrypted.rstrip(b'\x00')
                    # Strip 32-byte Brave header
                    if len(decrypted) > 32:
                        value = decrypted[32:].decode('utf-8', errors='replace')
                    else:
                        value = decrypted.decode('utf-8', errors='replace')
                except Exception:
                    continue

            value = value.strip('\x00').strip()
            if not value:
                continue

            # Chromium timestamp to Unix
            if expires_utc and expires_utc > 0:
                epoch_start = datetime(1601, 1, 1, tzinfo=timezone.utc)
                expires = (epoch_start + timedelta(microseconds=expires_utc)).timestamp()
            else:
                expires = -1

            # SameSite mapping (None requires Secure)
            if samesite in (-1, 0):
                ss = "None" if is_secure else "Lax"
            elif samesite == 1:
                ss = "Lax"
            else:
                ss = "Strict"

            cookie = {
                "name": name, "value": value, "domain": host_key,
                "path": path, "secure": bool(is_secure),
                "httpOnly": bool(is_httponly), "sameSite": ss,
            }
            if expires > 0:
                cookie["expires"] = expires
            cookies.append(cookie)

        conn.close()
    finally:
        Path(temp_db).unlink(missing_ok=True)

    print(f"   Extracted {len(cookies)} Twitter cookies from Brave")
    return cookies


def load_twitter_accounts(limit=None):
    """Load Twitter accounts marked for auto-monitoring"""
    accounts = []
    with open(HIGH_SIGNAL_SOURCES, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('platform') in ['X', 'Twitter'] and row.get('auto_monitor') == 'TRUE':
                handle = row.get('source_name', '').replace('@', '').strip()
                if handle:
                    accounts.append({
                        'handle': handle,
                        'signal_quality': row.get('signal_quality', 'MEDIUM'),
                        'focus_area': row.get('focus_area', '')
                    })

    quality_order = {'HIGHEST': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    accounts.sort(key=lambda x: quality_order.get(x['signal_quality'], 2))

    if limit:
        accounts = accounts[:limit]

    print(f"Loaded {len(accounts)} Twitter accounts to scrape")
    return accounts


def get_next_alpha_id():
    """Get next available ALPHA ID"""
    max_id = 0
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                alpha_id = row.get('alpha_id', '')
                match = re.match(r'ALPHA(\d+)', alpha_id)
                if match:
                    max_id = max(max_id, int(match.group(1)))
    return max_id + 1


def load_existing_urls():
    """Load existing URLs to avoid duplicates"""
    urls = set()
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('source_url'):
                    urls.add(row['source_url'])
    return urls


def categorize_tweet(text):
    """Auto-categorize tweet based on content"""
    text_lower = text.lower()
    if any(kw in text_lower for kw in ['cold email', 'outbound', 'deliverability', 'inbox', 'smtp']):
        return 'COLD_OUTBOUND'
    elif any(kw in text_lower for kw in ['app store', 'ios', 'android', 'mobile app', 'react native']):
        return 'APP_FACTORY'
    elif any(kw in text_lower for kw in ['mcp', 'claude', 'gpt', 'llm', 'ai agent', 'automation']):
        return 'TOOL_ALPHA'
    elif any(kw in text_lower for kw in ['tiktok', 'reels', 'youtube', 'shorts', 'content']):
        return 'CONTENT_FARM'
    elif any(kw in text_lower for kw in ['saas', 'mrr', 'arr', 'subscription', 'churn']):
        return 'SAAS'
    elif any(kw in text_lower for kw in ['seo', 'google', 'ranking', 'traffic', 'organic']):
        return 'SEO_GEO'
    elif any(kw in text_lower for kw in ['$', 'revenue', 'profit', 'income', 'monetiz']):
        return 'MONETIZATION'
    elif any(kw in text_lower for kw in ['growth', 'viral', 'followers', 'engagement']):
        return 'GROWTH_HACK'
    elif any(kw in text_lower for kw in ['ecom', 'dropship', 'amazon', 'etsy', 'shopify']):
        return 'ECOM_ARB'
    else:
        return 'ALPHA_GENERAL'


def estimate_roi(text):
    """Estimate ROI potential based on content signals"""
    text_lower = text.lower()
    score = 0
    if re.search(r'\$[\d,]+k?', text_lower): score += 3
    if re.search(r'\d+%', text_lower): score += 2
    if re.search(r'\d+x', text_lower): score += 2
    if any(kw in text_lower for kw in ['step 1', 'how to', 'framework', 'playbook', 'guide']): score += 2
    if re.search(r'\.(com|io|ai|app|co)\b', text): score += 1
    if score >= 5: return 'HIGHEST'
    elif score >= 3: return 'HIGH'
    elif score >= 1: return 'MEDIUM'
    else: return 'LOW'


async def scrape_accounts(accounts, headless=True):
    """Scrape Twitter accounts using cookie injection."""
    existing_urls = load_existing_urls()
    next_id = get_next_alpha_id()
    new_entries = []

    print(f"\n{'='*60}")
    print(f"BACKGROUND TWITTER SCRAPER")
    print(f"{'='*60}")
    print(f"Mode: {'HEADLESS' if headless else 'VISIBLE'}")
    print(f"Accounts: {len(accounts)}")
    print(f"Starting ID: ALPHA{next_id}")
    print(f"{'='*60}\n")

    # Extract cookies from Brave
    print("Extracting Twitter cookies from Brave...")
    cookies = extract_twitter_cookies()
    if not cookies:
        print("ERROR: No Twitter cookies. Log into Twitter in Brave first.")
        return []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=headless,
            args=["--disable-blink-features=AutomationControlled", "--no-first-run"]
        )
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )

        # Inject cookies
        injected = 0
        for cookie in cookies:
            try:
                await context.add_cookies([cookie])
                injected += 1
            except Exception:
                pass
        print(f"   {injected}/{len(cookies)} cookies injected")

        page = await context.new_page()

        # Check login
        await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(5)

        if 'login' in page.url.lower() or 'flow' in page.url.lower():
            print("Not logged in. Make sure Twitter is logged in via Brave Browser.")
            await browser.close()
            return []

        print("Session valid - starting scrape...\n")

        for i, account in enumerate(accounts):
            handle = account['handle']
            try:
                print(f"[{i+1}/{len(accounts)}] @{handle} ({account['signal_quality']})...")

                await page.goto(f"https://x.com/{handle}", wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(2)

                for _ in range(2):
                    await page.evaluate("window.scrollBy(0, 1000)")
                    await asyncio.sleep(1)

                tweets = await page.evaluate("""
                    () => {
                        const tweets = [];
                        const articles = document.querySelectorAll('article[data-testid="tweet"]');
                        articles.forEach(article => {
                            try {
                                const link = article.querySelector('a[href*="/status/"]');
                                const textElem = article.querySelector('[data-testid="tweetText"]');
                                if (link && textElem) {
                                    const text = textElem.innerText;
                                    const url = link.href;
                                    if (text.length > 50) {
                                        const hasSignal = (
                                            /\\$\\d+|revenue|mrr|arr|\\d+%|\\d+x/i.test(text) ||
                                            /how\\s+to|step\\s+\\d|framework|playbook/i.test(text) ||
                                            /\\.(com|io|ai|app|co)\\b/.test(text) ||
                                            /launch|ship|build|automat|tool|saas/i.test(text)
                                        );
                                        if (hasSignal) {
                                            tweets.push({ url, text: text.substring(0, 1000) });
                                        }
                                    }
                                }
                            } catch(e) {}
                        });
                        return tweets;
                    }
                """)

                for tweet in tweets:
                    if tweet['url'] not in existing_urls:
                        existing_urls.add(tweet['url'])
                        entry = {
                            'alpha_id': f'ALPHA{next_id}',
                            'source': f"@{handle}",
                            'source_url': tweet['url'],
                            'tactic': tweet['text'][:500],
                            'category': categorize_tweet(tweet['text']),
                            'roi_potential': estimate_roi(tweet['text']),
                            'status': 'PENDING_REVIEW',
                            'engagement_authenticity': 'UNCHECKED',
                            'earnings_verified': 'N/A',
                            'created_at': datetime.now().isoformat(),
                            'notes': f"Auto-scraped from {account['signal_quality']} signal account"
                        }
                        new_entries.append(entry)
                        next_id += 1

                print(f"    Found {len(tweets)} actionable tweets")
                await asyncio.sleep(1.5)

            except Exception as e:
                print(f"    Error: {str(e)[:50]}")
                continue

        await browser.close()

    # Save results
    if new_entries:
        fieldnames = ['alpha_id', 'source', 'source_url', 'tactic', 'category',
                      'roi_potential', 'status', 'engagement_authenticity',
                      'earnings_verified', 'created_at', 'notes']

        file_exists = ALPHA_STAGING.exists()
        with open(ALPHA_STAGING, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            if not file_exists:
                writer.writeheader()
            writer.writerows(new_entries)

        print(f"\n{'='*60}")
        print(f"SCRAPE COMPLETE")
        print(f"{'='*60}")
        print(f"New entries: {len(new_entries)}")
        print(f"Saved to: {ALPHA_STAGING}")

        json_path = OUTPUT_DIR / f"scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_path, 'w') as f:
            json.dump(new_entries, f, indent=2)
        print(f"JSON backup: {json_path}")
    else:
        print("\nNo new entries found (all duplicates or no actionable content)")

    return new_entries


async def main():
    parser = argparse.ArgumentParser(description='Background Twitter Scraper')
    parser.add_argument('--scrape', action='store_true', help='Scrape top 20 accounts')
    parser.add_argument('--full', action='store_true', help='Scrape ALL accounts')
    parser.add_argument('--visible', action='store_true', help='Show browser (debugging)')
    parser.add_argument('--limit', type=int, help='Limit number of accounts')

    args = parser.parse_args()

    if args.scrape or args.full:
        limit = args.limit or (20 if args.scrape else None)
        accounts = load_twitter_accounts(limit=limit)
        await scrape_accounts(accounts, headless=not args.visible)
    else:
        parser.print_help()
        print("\n\nQuick start:")
        print("  python3 background_twitter_scraper.py --scrape       # Top 20 accounts")
        print("  python3 background_twitter_scraper.py --full          # All accounts")
        print("  python3 background_twitter_scraper.py --scrape --limit 5  # Just 5")


if __name__ == "__main__":
    asyncio.run(main())
