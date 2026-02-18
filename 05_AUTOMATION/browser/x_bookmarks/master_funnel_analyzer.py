#!/usr/bin/env python3
"""
Master Funnel Analyzer - Uses existing Brave tabs
Analyzes: profiles, bios, replies, DMs, engagement, products
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime
import re

OUTPUT_DIR = Path("deep_scrape_output")
OUTPUT_DIR.mkdir(exist_ok=True)

async def analyze_account_complete(page, author, post_url):
    """Complete analysis: profile + replies + engagement"""

    username = author.split()[0].replace('@', '').strip() if author else ''
    if not username:
        return None

    result = {
        'author': author,
        'username': username,
        'post_url': post_url,
        'profile': {},
        'replies': {},
        'engagement': {},
        'funnel_setup': {}
    }

    print(f"\n{'='*80}")
    print(f"🎯 {author}")
    print(f"{'='*80}")

    try:
        # 1. PROFILE
        profile_url = f"https://x.com/{username}"
        print(f"\n📋 Profile: {profile_url}")
        await page.goto(profile_url, wait_until="load", timeout=15000)
        await asyncio.sleep(2)

        # Bio
        try:
            bio = await page.locator('div[data-testid="UserDescription"]').first.inner_text()
            result['profile']['bio'] = bio
            print(f"   Bio: {bio[:80]}...")
        except:
            result['profile']['bio'] = ''

        # Links
        links = []
        try:
            link_elems = await page.locator('a[href*="t.co"]').all()
            for link in link_elems[:3]:
                href = await link.get_attribute('href')
                if href and 't.co' in href:
                    links.append(href)
        except:
            pass
        result['profile']['links'] = links
        if links:
            print(f"   Links: {len(links)}")

        # Pinned
        try:
            pinned = await page.locator('article:has-text("Pinned")').first.locator('[data-testid="tweetText"]').first.inner_text()
            result['profile']['pinned'] = pinned[:500]
            print(f"   Pinned: {pinned[:80]}...")
        except:
            result['profile']['pinned'] = ''

        # Screenshot
        try:
            ss = OUTPUT_DIR / f"profile_{username}.png"
            await page.screenshot(path=str(ss))
            result['profile']['screenshot'] = str(ss)
            print(f"   📸 Saved")
        except:
            pass

        # 2. POST + REPLIES
        print(f"\n💬 Post: {post_url}")
        await page.goto(post_url, wait_until="load", timeout=15000)
        await asyncio.sleep(2)

        # Scroll replies
        for _ in range(3):
            await page.evaluate("window.scrollBy(0, 500)")
            await asyncio.sleep(0.5)

        # Engagement metrics
        try:
            like_btn = await page.locator('button[data-testid="like"]').first.get_attribute('aria-label')
            rt_btn = await page.locator('button[data-testid="retweet"]').first.get_attribute('aria-label')
            reply_btn = await page.locator('button[data-testid="reply"]').first.get_attribute('aria-label')

            result['engagement'] = {
                'likes': like_btn,
                'retweets': rt_btn,
                'replies': reply_btn
            }
            print(f"   Engagement captured")
        except:
            pass

        # Check author self-replies
        author_replies = []
        try:
            all_replies = await page.locator('article[data-testid="tweet"]').all()
            for reply in all_replies[:20]:
                try:
                    reply_author = await reply.locator('[data-testid="User-Name"]').first.inner_text()
                    reply_text = await reply.locator('[data-testid="tweetText"]').first.inner_text()

                    if username.lower() in reply_author.lower():
                        has_link = 'http' in reply_text or 'link' in reply_text.lower()
                        is_offer = any(w in reply_text.lower() for w in ['free', 'get', 'download', 'gumroad'])

                        if has_link or is_offer or len(reply_text) > 100:
                            author_replies.append({
                                'text': reply_text[:300],
                                'has_link': has_link,
                                'is_offer': is_offer
                            })
                except:
                    continue
        except:
            pass

        result['replies']['author_self_replies'] = author_replies
        if author_replies:
            print(f"   🎯 Self-replies with offers: {len(author_replies)}")

        # 3. FUNNEL ANALYSIS
        funnel = {
            'has_bio_link': len(links) > 0,
            'has_pinned_offer': bool(result['profile']['pinned'] and any(w in result['profile']['pinned'].lower() for w in ['link', 'free', 'get'])),
            'uses_reply_funnel': len(author_replies) > 0,
            'bio_style': 'link_in_bio' if links else 'no_link'
        }
        result['funnel_setup'] = funnel

        print(f"\n✅ Complete")
        print(f"   Bio link: {funnel['has_bio_link']}")
        print(f"   Pinned offer: {funnel['has_pinned_offer']}")
        print(f"   Reply funnel: {funnel['uses_reply_funnel']}")

    except Exception as e:
        print(f"\n❌ Error: {e}")

    return result

async def analyze_dms(page):
    """Analyze DMs for funnel examples"""

    print(f"\n{'='*80}")
    print("📬 ANALYZING DMS")
    print(f"{'='*80}\n")

    dm_funnels = []

    try:
        print("Opening DMs tab...")
        await page.goto("https://x.com/messages", wait_until="load", timeout=15000)
        await asyncio.sleep(3)

        # Get conversations
        convos = await page.locator('div[data-testid="conversation"]').all()
        print(f"Found {len(convos)} conversations\n")

        for i, convo in enumerate(convos[:15], 1):
            try:
                await convo.click()
                await asyncio.sleep(1.5)

                sender = "Unknown"
                try:
                    sender = await page.locator('h2').first.inner_text()
                except:
                    pass

                # SPAM FILTER - Skip OnlyFans/crypto/casino bots
                spam_keywords = [
                    'onlyfans', 'only fans', 'exclusive content', 'private pics',
                    'crypto', 'nft', 'trade', 'forex', 'casino', 'slots',
                    'dating', 'hook up', 'meet up', '🔞', '💋', '💦'
                ]
                if any(kw in sender.lower() for kw in spam_keywords):
                    print(f"[{i}] ⚠️  SKIPPED SPAM: {sender}")
                    continue

                print(f"[{i}] {sender}")

                # Read messages
                messages = await page.locator('div[data-testid="messageEntry"]').all()

                funnel_data = {
                    'sender': sender,
                    'messages': []
                }

                for msg in messages[-5:]:
                    try:
                        msg_text = await msg.locator('div[dir="auto"]').first.inner_text()

                        has_link = 'http' in msg_text
                        is_gumroad = 'gumroad' in msg_text.lower()
                        urls = re.findall(r'https?://\S+', msg_text)

                        if has_link or len(msg_text) > 50:
                            funnel_data['messages'].append({
                                'text': msg_text[:400],
                                'has_link': has_link,
                                'is_gumroad': is_gumroad,
                                'urls': urls[:2]
                            })
                    except:
                        continue

                if funnel_data['messages']:
                    dm_funnels.append(funnel_data)
                    print(f"    ✅ {len(funnel_data['messages'])} messages extracted")

            except Exception as e:
                print(f"    ❌ Error: {e}")
                continue

        print(f"\n✅ DM analysis complete: {len(dm_funnels)} funnels found")

    except Exception as e:
        print(f"❌ DM analysis error: {e}")

    return dm_funnels

async def main():
    print("🚀 MASTER FUNNEL ANALYZER")
    print("="*80)
    print("Using existing Brave session")
    print("="*80)

    # Load top accounts
    with open('deep_scrape_output/extracted_alpha.json', 'r') as f:
        alpha = json.load(f)

    top_accounts = alpha['revenue_playbooks'][:10]  # Top 10

    print(f"\nAnalyzing {len(top_accounts)} accounts + your DMs\n")

    async with async_playwright() as p:
        print("🔌 Connecting to existing Brave session...")

        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            print("✅ Connected!\n")
        except Exception as e:
            print(f"❌ Failed: {e}")
            return

        contexts = browser.contexts
        context = contexts[0] if contexts else None
        if not context:
            print("❌ No context")
            return

        pages = context.pages
        page = pages[0] if pages else await context.new_page()

        results = {
            'accounts': [],
            'dm_funnels': []
        }

        # 1. ANALYZE ACCOUNTS
        print("PHASE 1: Account Analysis")
        print("-"*80)

        for account in top_accounts:
            result = await analyze_account_complete(page, account['author'], account['url'])
            if result:
                results['accounts'].append(result)
            await asyncio.sleep(2)

        # 2. ANALYZE DMS
        print("\n\nPHASE 2: DM Funnel Analysis")
        print("-"*80)

        dm_funnels = await analyze_dms(page)
        results['dm_funnels'] = dm_funnels

        # SAVE
        output_file = OUTPUT_DIR / f"master_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\n\n{'='*80}")
        print("✅ COMPLETE")
        print(f"{'='*80}")
        print(f"📁 {output_file}")
        print(f"📊 {len(results['accounts'])} accounts analyzed")
        print(f"📬 {len(results['dm_funnels'])} DM funnels extracted")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
