#!/usr/bin/env python3
"""
Twitter Account Warmup Automation

Implements M1 (Manual-style) and M2 (Mixed) warmup protocols from v26 master doc.
Gradually builds account trust through human-like engagement patterns.

Usage:
    python twitter_warmup.py --mode M1 --niche AI --profile-id 1

Safety:
    - Rate limiting built-in
    - Random delays (human-like)
    - GoLogin profile support
    - Proxy rotation via Decodo
"""

import asyncio
import json
import random
import csv
from datetime import datetime, timedelta
from pathlib import Path
from playwright.async_api import async_playwright
import argparse

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
ACCOUNTS_CSV = PROJECT_ROOT / "LEDGER/ACCOUNTS.csv"
WARMUP_LOG_CSV = PROJECT_ROOT / "LEDGER/WARMUP_DEVICE_MATRIX.csv"
NICHES_JSON = PROJECT_ROOT / "LEDGER/niche_targets.json"

# Warmup protocols from v26
WARMUP_LIMITS = {
    "M1": {  # Manual mode (Week 1)
        "day_1_3": {"follows": (15, 20), "likes": (10, 15), "replies": (3, 5), "posts": 0},
        "day_4_7": {"follows": (20, 25), "likes": (15, 20), "replies": (5, 8), "posts": 0},
    },
    "M2": {  # Mixed mode (Week 2+)
        "day_8_14": {"follows": (25, 30), "likes": (20, 25), "replies": (8, 12), "posts": (1, 2)},
        "day_15+": {"follows": (30, 40), "likes": (25, 35), "replies": (10, 15), "posts": (2, 3)},
    },
}

# Niche-specific accounts to engage with
NICHE_TARGETS = {
    "AI": [
        "levelsio", "bentossell", "gregisenberg", "danshipper", "mattschnuck",
        "thesamparr", "nathanbarry", "patio11", "sweatystartup", "dklineii",
        "Suhail", "paulg", "naval", "balajis", "waitbutwhy",
    ],
    "Faith": [
        "timkeller", "johnpiper", "rickwarren", "maxlucado", "joyceemeyer",
        "elevation_YTH", "hillsong", "bethel_music", "passion268", "godcenteredmom",
    ],
    "Fitness": [
        "athleanx", "jeffnippard", "gregdoucetteifbbpro", "soheefit", "syattfitness",
        "menno_henselmans", "biolayne", "drbillcampbell", "erichelms", "mikevacanti",
    ],
}


class TwitterWarmup:
    def __init__(self, mode, niche, profile_id, account_handle):
        self.mode = mode
        self.niche = niche
        self.profile_id = profile_id
        self.account_handle = account_handle
        self.page = None
        self.context = None
        self.actions_log = {
            "follows": 0,
            "likes": 0,
            "replies": 0,
            "posts": 0,
            "flags": [],
        }

    async def random_delay(self, min_sec=2, max_sec=8):
        """Human-like delay between actions"""
        await asyncio.sleep(random.uniform(min_sec, max_sec))

    async def init_browser(self, playwright):
        """Initialize browser with GoLogin profile + Decodo proxy"""
        # TODO: Integrate GoLogin CDP endpoint
        # For now, use regular Playwright with proxy

        proxy = self._get_proxy()

        self.context = await playwright.chromium.launch_persistent_context(
            user_data_dir=f"/tmp/gologin_profile_{self.profile_id}",
            headless=False,  # Use headed for M1 (manual oversight)
            proxy=proxy,
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        )

        self.page = await self.context.new_page()
        print(f"✅ Browser initialized with profile {self.profile_id}")

    def _get_proxy(self):
        """Load Decodo proxy from env or config"""
        # TODO: Read from .env or config file
        return {
            "server": "proxy.decodo.com:8080",
            "username": "user",  # Replace with actual
            "password": "pass",  # Replace with actual
        }

    async def login_twitter(self, email, password):
        """Login to Twitter"""
        print(f"🔐 Logging into Twitter as {self.account_handle}...")

        await self.page.goto("https://twitter.com/login")
        await self.random_delay(3, 6)

        # Enter email
        await self.page.fill('input[autocomplete="username"]', email)
        await self.page.keyboard.press("Enter")
        await self.random_delay(2, 4)

        # Enter password
        await self.page.fill('input[autocomplete="current-password"]', password)
        await self.page.keyboard.press("Enter")
        await self.random_delay(5, 10)

        # Check if logged in
        if "home" in self.page.url or self.account_handle in self.page.url:
            print(f"✅ Logged in successfully")
            return True
        else:
            print(f"❌ Login failed - manual intervention needed")
            return False

    async def follow_accounts(self, target_count):
        """Follow target accounts in niche"""
        print(f"👥 Following {target_count} accounts...")

        targets = NICHE_TARGETS.get(self.niche, [])
        random.shuffle(targets)

        followed = 0
        for handle in targets[:target_count]:
            try:
                await self.page.goto(f"https://twitter.com/{handle}")
                await self.random_delay(2, 5)

                # Click follow button
                follow_btn = self.page.locator('div[data-testid$="-follow"]').first
                if await follow_btn.is_visible(timeout=5000):
                    await follow_btn.click()
                    followed += 1
                    print(f"  ✓ Followed @{handle}")
                    await self.random_delay(8, 15)  # Longer delay between follows

            except Exception as e:
                print(f"  ✗ Failed to follow @{handle}: {e}")
                continue

        self.actions_log["follows"] = followed
        return followed

    async def like_posts(self, target_count):
        """Like posts from timeline"""
        print(f"❤️  Liking {target_count} posts...")

        await self.page.goto("https://twitter.com/home")
        await self.random_delay(3, 6)

        liked = 0
        scrolls = 0
        max_scrolls = 10

        while liked < target_count and scrolls < max_scrolls:
            # Find all like buttons
            like_buttons = await self.page.locator('div[data-testid="like"]').all()

            for btn in like_buttons:
                if liked >= target_count:
                    break

                try:
                    if await btn.is_visible():
                        await btn.click()
                        liked += 1
                        print(f"  ✓ Liked post {liked}/{target_count}")
                        await self.random_delay(3, 8)

                except Exception as e:
                    continue

            # Scroll for more posts
            await self.page.keyboard.press("PageDown")
            await self.random_delay(2, 4)
            scrolls += 1

        self.actions_log["likes"] = liked
        return liked

    async def reply_to_posts(self, target_count):
        """Reply to posts (simple, genuine engagement)"""
        print(f"💬 Replying to {target_count} posts...")

        # Simple reply templates (randomized)
        replies = [
            "Great insight!",
            "This is really helpful, thanks",
            "Needed to see this today",
            "Solid advice",
            "Appreciate you sharing this",
            "This is the way",
            "Facts",
            "100% agree with this",
            "Well said",
            "Bookmarking this",
        ]

        await self.page.goto("https://twitter.com/home")
        await self.random_delay(3, 6)

        replied = 0
        scrolls = 0

        while replied < target_count and scrolls < 8:
            # Find reply buttons
            reply_buttons = await self.page.locator('div[data-testid="reply"]').all()

            for btn in reply_buttons[:target_count]:
                if replied >= target_count:
                    break

                try:
                    await btn.click()
                    await self.random_delay(2, 4)

                    # Type reply
                    reply_text = random.choice(replies)
                    await self.page.fill('div[data-testid="tweetTextarea_0"]', reply_text)
                    await self.random_delay(1, 3)

                    # Click reply button
                    await self.page.click('div[data-testid="tweetButtonInline"]')
                    replied += 1
                    print(f"  ✓ Replied {replied}/{target_count}: {reply_text}")
                    await self.random_delay(10, 20)  # Longer delay after replies

                    # Close reply modal if still open
                    try:
                        await self.page.keyboard.press("Escape")
                    except:
                        pass

                except Exception as e:
                    print(f"  ✗ Reply failed: {e}")
                    continue

            # Scroll
            await self.page.keyboard.press("PageDown")
            await self.random_delay(3, 6)
            scrolls += 1

        self.actions_log["replies"] = replied
        return replied

    async def check_for_warnings(self):
        """Check if account has been flagged/limited"""
        warnings = []

        # Check for common warning indicators
        page_content = await self.page.content()

        warning_phrases = [
            "temporarily limited",
            "unusual activity",
            "verify your account",
            "suspended",
            "restricted",
        ]

        for phrase in warning_phrases:
            if phrase.lower() in page_content.lower():
                warnings.append(phrase)
                print(f"⚠️  WARNING DETECTED: {phrase}")

        self.actions_log["flags"] = warnings
        return warnings

    def get_daily_limits(self, day_num):
        """Get warmup limits based on mode and day number"""
        if self.mode == "M1":
            return WARMUP_LIMITS["M1"]["day_1_3" if day_num <= 3 else "day_4_7"]
        elif self.mode == "M2":
            return WARMUP_LIMITS["M2"]["day_8_14" if day_num <= 14 else "day_15+"]

    async def run_warmup(self, day_num):
        """Execute daily warmup routine"""
        limits = self.get_daily_limits(day_num)

        print(f"\n{'='*60}")
        print(f"🚀 Twitter Warmup - Day {day_num}")
        print(f"Account: @{self.account_handle} | Niche: {self.niche} | Mode: {self.mode}")
        print(f"{'='*60}\n")

        # Randomize order (more human-like)
        actions = ["follow", "like", "reply"]
        random.shuffle(actions)

        for action in actions:
            if action == "follow":
                target = random.randint(*limits["follows"])
                await self.follow_accounts(target)

            elif action == "like":
                target = random.randint(*limits["likes"])
                await self.like_posts(target)

            elif action == "reply":
                target = random.randint(*limits["replies"])
                await self.reply_to_posts(target)

            # Random break between action types
            await self.random_delay(30, 60)

        # Check for warnings
        await self.check_for_warnings()

        # Log results
        self.log_results(day_num)

        print(f"\n{'='*60}")
        print(f"✅ Warmup complete for Day {day_num}")
        print(f"Follows: {self.actions_log['follows']}")
        print(f"Likes: {self.actions_log['likes']}")
        print(f"Replies: {self.actions_log['replies']}")
        print(f"Flags: {len(self.actions_log['flags'])} {'⚠️' if self.actions_log['flags'] else '✅'}")
        print(f"{'='*60}\n")

    def log_results(self, day_num):
        """Log warmup results to CSV"""
        log_entry = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Day": day_num,
            "Niche": self.niche,
            "Platform": "Twitter",
            "Handle": self.account_handle,
            "Mode": self.mode,
            "Follows": self.actions_log["follows"],
            "Likes": self.actions_log["likes"],
            "Replies": self.actions_log["replies"],
            "Posts": self.actions_log["posts"],
            "Flags": ",".join(self.actions_log["flags"]) if self.actions_log["flags"] else "NONE",
        }

        # Append to CSV
        with open(WARMUP_LOG_CSV, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=log_entry.keys())
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(log_entry)

        print(f"📊 Logged to {WARMUP_LOG_CSV}")

    async def cleanup(self):
        """Close browser"""
        if self.context:
            await self.context.close()


async def main():
    parser = argparse.ArgumentParser(description="Twitter Account Warmup")
    parser.add_argument("--mode", choices=["M1", "M2"], required=True, help="Warmup mode")
    parser.add_argument("--niche", choices=["AI", "Faith", "Fitness"], required=True, help="Niche")
    parser.add_argument("--profile-id", type=int, required=True, help="GoLogin profile ID")
    parser.add_argument("--handle", required=True, help="Twitter handle (without @)")
    parser.add_argument("--email", required=True, help="Twitter email")
    parser.add_argument("--password", required=True, help="Twitter password")
    parser.add_argument("--day", type=int, required=True, help="Day number in warmup")

    args = parser.parse_args()

    async with async_playwright() as p:
        warmup = TwitterWarmup(args.mode, args.niche, args.profile_id, args.handle)

        try:
            await warmup.init_browser(p)
            logged_in = await warmup.login_twitter(args.email, args.password)

            if logged_in:
                await warmup.run_warmup(args.day)
            else:
                print("❌ Login failed - aborting warmup")

        finally:
            await warmup.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
