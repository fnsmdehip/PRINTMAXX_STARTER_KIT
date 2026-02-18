#!/usr/bin/env python3
"""
Viral Content Scanner - Monitors meme/viral accounts for particularly viral content
Detects viral tweets based on engagement thresholds and prepares repurposing queue.

Features:
- Viral detection (10K+ likes, 2K+ retweets, 500K+ views, 5%+ engagement ratio)
- Media download (images/videos from viral tweets)
- Repurpose queue generation with reply-bait captions
- Scheduled posting times across peak engagement windows
- Breaking news detection (viral velocity in last 2 hours)

Usage:
    python3 viral_content_scanner.py --scan                # Scan all meme accounts
    python3 viral_content_scanner.py --scan --limit 5      # Scan first 5 accounts
    python3 viral_content_scanner.py --breaking            # Breaking viral content (last 2h)
    python3 viral_content_scanner.py --schedule            # Generate scheduled posting queue
    python3 viral_content_scanner.py --download            # Download media from viral queue
    python3 viral_content_scanner.py --stats               # Show viral content stats
"""

import asyncio
import json
import csv
import re
import subprocess
import shutil
import tempfile
import sqlite3
import hashlib
import urllib.request
import random
from pathlib import Path
from datetime import datetime, timedelta, timezone
from playwright.async_api import async_playwright
import argparse

try:
    from Crypto.Cipher import AES
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False
    print("WARNING: pycryptodome not installed. Run: pip3 install pycryptodome")

# Paths
PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_DIR / "LEDGER"
MEME_ACCOUNTS_CSV = LEDGER_DIR / "MEME_REPURPOSE_ACCOUNTS.csv"
VIRAL_DIR = PROJECT_DIR / "AUTOMATIONS" / "viral_content"
MEDIA_DIR = VIRAL_DIR / "media"
SCAN_HISTORY_DIR = VIRAL_DIR / "scan_history"
REPURPOSE_QUEUE = VIRAL_DIR / "repurpose_queue.csv"
BREAKING_ALERTS = VIRAL_DIR / "breaking_alerts.json"

# Create directories
VIRAL_DIR.mkdir(exist_ok=True)
MEDIA_DIR.mkdir(exist_ok=True)
SCAN_HISTORY_DIR.mkdir(exist_ok=True)

# Brave Browser paths (SAME AS twitter_alpha_scraper.py)
BRAVE_USER_DATA = Path.home() / "Library/Application Support/BraveSoftware/Brave-Browser"
BRAVE_KEY_FILE = PROJECT_DIR / "AUTOMATIONS" / ".brave_cookie_key"

# Viral thresholds
VIRAL_LIKES = 10000
VIRAL_RETWEETS = 2000
VIRAL_VIEWS = 500000
VIRAL_ENGAGEMENT_RATIO = 0.05  # 5%

# Breaking news thresholds (last 2 hours)
BREAKING_HOURS = 2
BREAKING_VELOCITY = 500  # likes per hour

# Peak engagement time slots
TIME_SLOTS = [
    (8, 11),   # 8am-11am
    (12, 14),  # 12pm-2pm
    (17, 20),  # 5pm-8pm
    (21, 23),  # 9pm-11pm
]
MAX_POSTS_PER_DAY = 8

# Reply-bait caption templates by content type
CAPTION_TEMPLATES = {
    'funny': [
        "no way 💀",
        "this is crazy",
        "bro what",
        "i can't 😭",
        "not this",
        "why tho",
        "lmaooo",
        "nah fr",
    ],
    'nature': [
        "how is this real",
        "nature is wild",
        "insane",
        "beautiful",
        "mind blown",
    ],
    'science': [
        "how is this real",
        "this changes everything",
        "crazy",
        "wild",
    ],
    'drama': [
        "thoughts?",
        "wild",
        "no way",
        "this is insane",
        "what do you think",
    ],
    'default': [
        "no way",
        "this is crazy",
        "insane",
        "wild",
        "thoughts?",
    ],
}

# JS to extract tweets with engagement metrics (SAME AS twitter_alpha_scraper.py)
EXTRACT_TWEETS_JS = """
() => {
    const results = [];
    const articles = document.querySelectorAll('article[data-testid="tweet"]');
    articles.forEach(article => {
        try {
            const link = article.querySelector('a[href*="/status/"]');
            const textElem = article.querySelector('[data-testid="tweetText"]');
            if (!link) return;

            const url = link.href;
            const text = textElem ? textElem.innerText : '';

            // Engagement metrics from aria-labels
            const getMetric = (testId) => {
                const btn = article.querySelector(`[data-testid="${testId}"]`);
                if (!btn) return 0;
                const label = btn.getAttribute('aria-label') || btn.closest('[aria-label]')?.getAttribute('aria-label') || '';
                const match = label.match(/([\\d,\\.]+[KMkm]?)\\s/);
                if (!match) return 0;
                let val = match[1].replace(/,/g, '');
                if (val.endsWith('K') || val.endsWith('k')) return parseFloat(val) * 1000;
                if (val.endsWith('M') || val.endsWith('m')) return parseFloat(val) * 1000000;
                return parseInt(val) || 0;
            };

            const likes = getMetric('like') || getMetric('unlike');
            const retweets = getMetric('retweet');
            const replies = getMetric('reply');

            // Views
            let views = 0;
            const analyticsLink = article.querySelector('a[href*="/analytics"]');
            if (analyticsLink) {
                const viewLabel = analyticsLink.getAttribute('aria-label') || '';
                const viewMatch = viewLabel.match(/([\\d,\\.]+[KMkm]?)\\s/);
                if (viewMatch) {
                    let v = viewMatch[1].replace(/,/g, '');
                    if (v.endsWith('K') || v.endsWith('k')) views = parseFloat(v) * 1000;
                    else if (v.endsWith('M') || v.endsWith('m')) views = parseFloat(v) * 1000000;
                    else views = parseInt(v) || 0;
                }
            }

            // Media URLs (images)
            const images = [];
            article.querySelectorAll('img[src*="pbs.twimg.com/media/"]').forEach(img => {
                let src = img.src;
                if (src.includes('?')) src = src.split('?')[0] + '?format=jpg&name=large';
                else src += '?format=jpg&name=large';
                images.push(src);
            });

            // Video detection
            const hasVideo = article.querySelector('video') !== null ||
                           article.querySelector('[data-testid="videoPlayer"]') !== null;

            // Handle extraction
            const handleMatch = url.match(/x\\.com\\/([^/]+)\\/status/);
            const handle = handleMatch ? handleMatch[1] : 'unknown';

            // Timestamp
            const timeElem = article.querySelector('time');
            const timestamp = timeElem ? timeElem.getAttribute('datetime') : '';

            results.push({
                url, text, handle, timestamp,
                likes, retweets, replies, views,
                images, hasVideo,
                engagement_ratio: views > 0 ? ((likes + retweets + replies) / views) : 0
            });
        } catch(e) {}
    });
    return results;
}
"""


def extract_brave_cookies(domain_filter=".x.com"):
    """Extract and decrypt cookies from Brave's cookie database.
    EXACT COPY from twitter_alpha_scraper.py"""
    if not HAS_CRYPTO:
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
        except (subprocess.TimeoutExpired, Exception) as e:
            print(f"ERROR: Keychain failed: {e}")
            return []

    if not keychain_pass:
        return []

    aes_key = hashlib.pbkdf2_hmac('sha1', keychain_pass.encode('utf-8'), b'saltysalt', 1003, dklen=16)

    temp_db = tempfile.mktemp(suffix=".db", prefix="brave_cookies_")
    shutil.copy2(str(cookie_db), temp_db)
    journal = str(cookie_db) + "-journal"
    if Path(journal).exists():
        shutil.copy2(journal, temp_db + "-journal")

    cookies = []
    try:
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT host_key, name, path, encrypted_value, is_secure, is_httponly, "
            "expires_utc, samesite FROM cookies WHERE host_key = ? OR host_key = ?",
            (domain_filter, domain_filter.lstrip('.')),
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
                    if len(decrypted) > 32:
                        value = decrypted[32:].decode('utf-8', errors='replace')
                    else:
                        value = decrypted.decode('utf-8', errors='replace')
                except Exception:
                    continue

            value = value.strip('\x00').strip()
            if not value:
                continue

            if expires_utc and expires_utc > 0:
                epoch_start = datetime(1601, 1, 1, tzinfo=timezone.utc)
                expires = (epoch_start + timedelta(microseconds=expires_utc)).timestamp()
            else:
                expires = -1

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
        Path(temp_db + "-journal").unlink(missing_ok=True)

    return cookies


async def launch_browser_with_cookies():
    """Launch headless Chromium with Brave's Twitter cookies injected.
    EXACT COPY from twitter_alpha_scraper.py"""
    print("🔑 Extracting Twitter cookies from Brave Browser...")
    cookies = extract_brave_cookies(".x.com")
    cookies += extract_brave_cookies(".twitter.com")

    if not cookies:
        print("ERROR: No Twitter cookies found. Make sure you're logged into Twitter in Brave.")
        return None, None, None

    print(f"   Got {len(cookies)} cookies")

    p = await async_playwright().start()
    browser = await p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-first-run"]
    )
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    )

    injected = 0
    for cookie in cookies:
        try:
            await context.add_cookies([cookie])
            injected += 1
        except Exception:
            pass
    print(f"   {injected}/{len(cookies)} cookies injected")

    page = await context.new_page()

    # Verify login
    print("🔍 Checking Twitter login...")
    await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=60000)
    await asyncio.sleep(5)

    if "login" in page.url.lower() or "flow" in page.url.lower():
        print("❌ Not logged in. Make sure Twitter is logged in via Brave Browser.")
        await browser.close()
        await p.stop()
        return None, None, None

    print("✅ Logged into Twitter\n")
    return p, browser, page


class ViralContentScanner:
    def __init__(self):
        self.meme_accounts = self._load_meme_accounts()
        self.viral_tweets = []
        self.account_stats = {}  # Track each account's average engagement

    def _load_meme_accounts(self):
        """Load meme accounts from MEME_REPURPOSE_ACCOUNTS.csv"""
        accounts = []
        if not MEME_ACCOUNTS_CSV.exists():
            print(f"ERROR: {MEME_ACCOUNTS_CSV} not found")
            return []

        with open(MEME_ACCOUNTS_CSV, 'r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                handle = row.get('handle', '').replace('@', '').strip()
                if handle:
                    accounts.append({
                        'handle': handle,
                        'content_type': row.get('content_type', 'mixed'),
                        'download_priority': row.get('download_priority', 'MEDIUM'),
                    })
        return accounts

    def _is_viral(self, tweet, account_avg=None):
        """Check if tweet meets viral thresholds"""
        likes = tweet.get('likes', 0)
        retweets = tweet.get('retweets', 0)
        views = tweet.get('views', 0)
        engagement_ratio = tweet.get('engagement_ratio', 0)

        # Absolute thresholds
        if (likes >= VIRAL_LIKES or
            retweets >= VIRAL_RETWEETS or
            views >= VIRAL_VIEWS or
            engagement_ratio >= VIRAL_ENGAGEMENT_RATIO):
            return True

        # Relative to account average (2x outlier)
        if account_avg and likes >= account_avg * 2:
            return True

        return False

    def _calculate_viral_score(self, tweet):
        """Calculate viral score (0-100)"""
        score = 0

        likes = tweet.get('likes', 0)
        retweets = tweet.get('retweets', 0)
        views = tweet.get('views', 0)
        engagement_ratio = tweet.get('engagement_ratio', 0)

        # Likes score (max 30)
        if likes >= 100000: score += 30
        elif likes >= 50000: score += 25
        elif likes >= 20000: score += 20
        elif likes >= VIRAL_LIKES: score += 15
        elif likes >= 5000: score += 10
        elif likes >= 1000: score += 5

        # Retweets score (max 25)
        if retweets >= 20000: score += 25
        elif retweets >= 10000: score += 20
        elif retweets >= 5000: score += 15
        elif retweets >= VIRAL_RETWEETS: score += 10
        elif retweets >= 500: score += 5

        # Views score (max 25)
        if views >= 5000000: score += 25
        elif views >= 2000000: score += 20
        elif views >= 1000000: score += 15
        elif views >= VIRAL_VIEWS: score += 10
        elif views >= 100000: score += 5

        # Engagement ratio score (max 20)
        if engagement_ratio >= 0.10: score += 20
        elif engagement_ratio >= 0.07: score += 15
        elif engagement_ratio >= VIRAL_ENGAGEMENT_RATIO: score += 10
        elif engagement_ratio >= 0.03: score += 5

        return min(score, 100)

    def _calculate_viral_velocity(self, tweet):
        """Calculate viral velocity (engagement per hour)"""
        timestamp = tweet.get('timestamp', '')
        if not timestamp:
            return 0

        try:
            posted_at = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            hours_ago = (now - posted_at).total_seconds() / 3600

            if hours_ago < 0.1:  # Less than 6 minutes
                hours_ago = 0.1

            likes = tweet.get('likes', 0)
            velocity = likes / hours_ago

            return velocity
        except Exception:
            return 0

    def _is_breaking(self, tweet):
        """Check if tweet is breaking news (high viral velocity in last 2 hours)"""
        timestamp = tweet.get('timestamp', '')
        if not timestamp:
            return False

        try:
            posted_at = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            hours_ago = (now - posted_at).total_seconds() / 3600

            if hours_ago > BREAKING_HOURS:
                return False

            velocity = self._calculate_viral_velocity(tweet)
            return velocity >= BREAKING_VELOCITY

        except Exception:
            return False

    def _generate_caption(self, tweet, content_type):
        """Generate reply-bait style caption"""
        # Detect content type from text if not provided
        text_lower = tweet.get('text', '').lower()

        if 'funny' in content_type or any(w in text_lower for w in ['lol', 'lmao', 'funny', 'wtf']):
            templates = CAPTION_TEMPLATES['funny']
        elif 'nature' in content_type or any(w in text_lower for w in ['nature', 'animal', 'planet']):
            templates = CAPTION_TEMPLATES['nature']
        elif 'science' in content_type or any(w in text_lower for w in ['science', 'research', 'study']):
            templates = CAPTION_TEMPLATES['science']
        elif 'drama' in content_type or any(w in text_lower for w in ['drama', 'beef', 'controversy']):
            templates = CAPTION_TEMPLATES['drama']
        else:
            templates = CAPTION_TEMPLATES['default']

        return random.choice(templates)

    def _determine_repurpose_type(self, tweet):
        """Determine best repurpose strategy"""
        has_media = len(tweet.get('images', [])) > 0 or tweet.get('hasVideo', False)
        text_length = len(tweet.get('text', ''))

        if has_media and text_length < 50:
            return 'MEDIA_REPOST'
        elif has_media:
            return 'REPOST_WITH_CAPTION'
        elif text_length > 100:
            return 'QUOTE_TWEET'
        else:
            return 'REPLY_BAIT'

    async def scan_account(self, page, account, max_scrolls=10):
        """Scan account for viral content"""
        handle = account['handle']
        content_type = account['content_type']

        print(f"  Scanning @{handle}...")

        try:
            await page.goto(f"https://x.com/{handle}", wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(3)

            all_tweets = []
            seen_urls = set()

            for scroll in range(max_scrolls):
                tweets = await page.evaluate(EXTRACT_TWEETS_JS)

                for t in tweets:
                    if t['url'] not in seen_urls:
                        seen_urls.add(t['url'])
                        t['handle'] = handle
                        t['content_type'] = content_type
                        all_tweets.append(t)

                await page.evaluate("window.scrollBy(0, 1000)")
                await asyncio.sleep(1.5)

            # Calculate account average engagement
            if all_tweets:
                avg_likes = sum(t.get('likes', 0) for t in all_tweets) / len(all_tweets)
                self.account_stats[handle] = avg_likes
            else:
                avg_likes = 0

            # Filter for viral tweets
            viral = []
            for tweet in all_tweets:
                if self._is_viral(tweet, avg_likes):
                    tweet['viral_score'] = self._calculate_viral_score(tweet)
                    tweet['viral_velocity'] = self._calculate_viral_velocity(tweet)
                    tweet['suggested_caption'] = self._generate_caption(tweet, content_type)
                    tweet['repurpose_type'] = self._determine_repurpose_type(tweet)
                    viral.append(tweet)

            print(f"    Found {len(viral)} viral tweets (avg likes: {int(avg_likes)})")
            return viral

        except Exception as e:
            print(f"    Error: {str(e)[:80]}")
            return []

    async def download_media(self, tweet):
        """Download media from a viral tweet"""
        handle = tweet.get('handle', 'unknown').replace('@', '')
        tweet_id = tweet['url'].split('/')[-1] if '/' in tweet['url'] else 'unknown'

        save_dir = MEDIA_DIR / handle / tweet_id
        save_dir.mkdir(parents=True, exist_ok=True)

        # Save tweet metadata
        metadata_path = save_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(tweet, f, indent=2, default=str)

        # Download images
        images = tweet.get('images', [])
        downloaded = []

        for i, img_url in enumerate(images):
            try:
                filename = f"image_{i+1}.jpg"
                filepath = save_dir / filename
                if not filepath.exists():
                    urllib.request.urlretrieve(img_url, str(filepath))
                    downloaded.append(str(filepath))
            except Exception:
                continue

        # Log video URL for manual download with yt-dlp
        if tweet.get('hasVideo'):
            video_log = save_dir / "video_url.txt"
            with open(video_log, 'w') as f:
                f.write(f"{tweet['url']}\n")
            downloaded.append(str(video_log))

        return downloaded

    def generate_repurpose_queue(self, schedule=False):
        """Generate repurpose queue CSV"""
        if not self.viral_tweets:
            print("No viral tweets to queue")
            return

        rows = []
        scheduled_times = []

        if schedule:
            # Generate random posting times across the day
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            for _ in range(min(len(self.viral_tweets), MAX_POSTS_PER_DAY)):
                slot = random.choice(TIME_SLOTS)
                hour = random.randint(slot[0], slot[1])
                minute = random.randint(0, 59)
                scheduled_time = today + timedelta(hours=hour, minutes=minute)
                scheduled_times.append(scheduled_time)

            # Shuffle to avoid posting in scrape order
            random.shuffle(scheduled_times)

        for i, tweet in enumerate(self.viral_tweets):
            handle = tweet.get('handle', 'unknown')
            tweet_id = tweet['url'].split('/')[-1] if '/' in tweet['url'] else 'unknown'

            # Find media path
            media_path = MEDIA_DIR / handle.replace('@', '') / tweet_id
            media_path_str = str(media_path) if media_path.exists() else ''

            row = {
                'original_handle': f"@{handle}",
                'original_tweet_id': tweet_id,
                'original_url': tweet['url'],
                'content_text': tweet.get('text', '')[:500],
                'media_path': media_path_str,
                'engagement_score': f"{tweet.get('likes', 0)}L {tweet.get('retweets', 0)}RT {tweet.get('views', 0)}V",
                'viral_score': tweet.get('viral_score', 0),
                'suggested_caption': tweet.get('suggested_caption', ''),
                'repurpose_type': tweet.get('repurpose_type', 'MEDIA_REPOST'),
                'status': 'PENDING',
                'scheduled_time': scheduled_times[i].isoformat() if schedule and i < len(scheduled_times) else '',
            }
            rows.append(row)

        # Write to CSV
        fieldnames = ['original_handle', 'original_tweet_id', 'original_url', 'content_text',
                      'media_path', 'engagement_score', 'viral_score', 'suggested_caption',
                      'repurpose_type', 'status', 'scheduled_time']

        with open(REPURPOSE_QUEUE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"\n✅ Generated repurpose queue: {REPURPOSE_QUEUE}")
        print(f"   {len(rows)} viral tweets queued")
        if schedule:
            print(f"   Scheduled across {len(TIME_SLOTS)} time slots")

    def save_breaking_alerts(self):
        """Save breaking viral content to JSON"""
        breaking = [t for t in self.viral_tweets if self._is_breaking(t)]

        if not breaking:
            print("No breaking viral content found")
            return

        # Sort by viral velocity
        breaking.sort(key=lambda t: t.get('viral_velocity', 0), reverse=True)

        with open(BREAKING_ALERTS, 'w') as f:
            json.dump(breaking, f, indent=2, default=str)

        print(f"\n🚨 Breaking alerts saved: {BREAKING_ALERTS}")
        print(f"   {len(breaking)} breaking viral tweets (last {BREAKING_HOURS}h)")

        for tweet in breaking[:5]:
            velocity = tweet.get('viral_velocity', 0)
            print(f"   @{tweet['handle']}: {int(velocity)} likes/hour")

    def show_stats(self):
        """Show viral content statistics"""
        if not REPURPOSE_QUEUE.exists():
            print("No repurpose queue found. Run --scan first.")
            return

        with open(REPURPOSE_QUEUE, 'r', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))

        print(f"\n{'='*60}")
        print(f"VIRAL CONTENT STATS")
        print(f"{'='*60}")
        print(f"Total viral tweets: {len(rows)}")

        # Group by account
        by_account = {}
        for row in rows:
            handle = row['original_handle']
            by_account.setdefault(handle, []).append(row)

        print(f"\nBy account:")
        for handle in sorted(by_account.keys(), key=lambda h: len(by_account[h]), reverse=True):
            print(f"  {handle}: {len(by_account[handle])} viral tweets")

        # Group by repurpose type
        by_type = {}
        for row in rows:
            rtype = row['repurpose_type']
            by_type.setdefault(rtype, []).append(row)

        print(f"\nBy repurpose type:")
        for rtype in sorted(by_type.keys()):
            print(f"  {rtype}: {len(by_type[rtype])}")

        # Top viral scores
        print(f"\nTop 5 viral scores:")
        sorted_rows = sorted(rows, key=lambda r: int(r.get('viral_score', 0)), reverse=True)
        for row in sorted_rows[:5]:
            print(f"  {row['viral_score']}: @{row['original_handle']} - {row['content_text'][:60]}...")

        print(f"{'='*60}\n")


async def main():
    parser = argparse.ArgumentParser(description='Viral Content Scanner - Monitor and repurpose viral content')
    parser.add_argument('--scan', action='store_true', help='Scan all meme accounts for viral content')
    parser.add_argument('--limit', type=int, help='Limit number of accounts to scan')
    parser.add_argument('--breaking', action='store_true', help='Check for breaking viral content (last 2h)')
    parser.add_argument('--schedule', action='store_true', help='Generate scheduled posting queue')
    parser.add_argument('--download', action='store_true', help='Download media from viral queue')
    parser.add_argument('--stats', action='store_true', help='Show viral content stats')
    args = parser.parse_args()

    if not any([args.scan, args.breaking, args.schedule, args.download, args.stats]):
        parser.print_help()
        print("\nExamples:")
        print("  python3 viral_content_scanner.py --scan                # Scan all meme accounts")
        print("  python3 viral_content_scanner.py --scan --limit 5      # Scan first 5 accounts")
        print("  python3 viral_content_scanner.py --breaking            # Breaking viral (last 2h)")
        print("  python3 viral_content_scanner.py --schedule            # Generate scheduled queue")
        print("  python3 viral_content_scanner.py --download            # Download media")
        print("  python3 viral_content_scanner.py --stats               # Show stats")
        return

    scanner = ViralContentScanner()

    # Stats mode (no browser needed)
    if args.stats:
        scanner.show_stats()
        return

    # Scan mode (requires browser)
    if args.scan or args.breaking:
        p, browser, page = await launch_browser_with_cookies()
        if not page:
            return

        try:
            accounts = scanner.meme_accounts
            if args.limit:
                accounts = accounts[:args.limit]

            print(f"\n🎭 Scanning {len(accounts)} meme/viral accounts...\n")

            for i, account in enumerate(accounts, 1):
                print(f"[{i}/{len(accounts)}] @{account['handle']}...", end=' ')
                viral = await scanner.scan_account(page, account)
                scanner.viral_tweets.extend(viral)
                await asyncio.sleep(2)

            print(f"\n{'='*60}")
            print(f"SCAN COMPLETE")
            print(f"{'='*60}")
            print(f"Total viral tweets found: {len(scanner.viral_tweets)}")
            print(f"Accounts scanned: {len(accounts)}")
            print(f"{'='*60}\n")

            # Save scan history
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            history_file = SCAN_HISTORY_DIR / f"scan_{timestamp}.json"
            with open(history_file, 'w') as f:
                json.dump({
                    'timestamp': timestamp,
                    'accounts_scanned': len(accounts),
                    'viral_tweets_found': len(scanner.viral_tweets),
                    'account_stats': scanner.account_stats,
                    'tweets': scanner.viral_tweets,
                }, f, indent=2, default=str)
            print(f"Scan history saved: {history_file}\n")

            # Generate repurpose queue
            if scanner.viral_tweets:
                scanner.generate_repurpose_queue(schedule=False)

            # Breaking alerts
            if args.breaking:
                scanner.save_breaking_alerts()

        finally:
            await browser.close()
            await p.stop()

    # Schedule mode (update existing queue)
    if args.schedule:
        if REPURPOSE_QUEUE.exists():
            # Reload viral tweets from queue
            with open(REPURPOSE_QUEUE, 'r', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    scanner.viral_tweets.append({
                        'url': row['original_url'],
                        'handle': row['original_handle'].replace('@', ''),
                        'text': row['content_text'],
                        'suggested_caption': row['suggested_caption'],
                        'repurpose_type': row['repurpose_type'],
                        'viral_score': int(row['viral_score']) if row['viral_score'] else 0,
                    })

            scanner.generate_repurpose_queue(schedule=True)
        else:
            print("ERROR: No repurpose queue found. Run --scan first.")

    # Download mode
    if args.download:
        if not REPURPOSE_QUEUE.exists():
            print("ERROR: No repurpose queue found. Run --scan first.")
            return

        print("\n📥 Downloading media from viral queue...\n")

        with open(REPURPOSE_QUEUE, 'r', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))

        # Reload tweets from history for download
        latest_history = sorted(SCAN_HISTORY_DIR.glob("scan_*.json"), reverse=True)
        if latest_history:
            with open(latest_history[0], 'r') as f:
                history = json.load(f)
                tweets = history.get('tweets', [])

                print(f"Downloading media for {len(tweets)} tweets...\n")

                for i, tweet in enumerate(tweets, 1):
                    print(f"[{i}/{len(tweets)}] @{tweet['handle']}...", end=' ')
                    downloaded = await scanner.download_media(tweet)
                    if downloaded:
                        print(f"{len(downloaded)} files downloaded")
                    else:
                        print("no media")

                print(f"\n✅ Media download complete")
                print(f"Media saved to: {MEDIA_DIR}")
        else:
            print("ERROR: No scan history found. Run --scan first.")


if __name__ == "__main__":
    asyncio.run(main())
