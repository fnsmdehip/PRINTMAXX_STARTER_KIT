#!/usr/bin/env python3
"""
Deep funnel analysis: profiles, replies, engagement, monetization
"""

import asyncio
import json
import re
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime

INPUT_FILE = "deep_scrape_output/extracted_alpha.json"
OUTPUT_DIR = Path("deep_scrape_output")

async def analyze_profile(page, username, url):
    """Deep dive into profile monetization setup"""
    try:
        # Navigate to profile
        profile_url = f"https://x.com/{username.lstrip('@')}"
        await page.goto(profile_url, wait_until="load", timeout=15000)
        await asyncio.sleep(2)
        
        profile_data = {
            'username': username,
            'source_url': url,
            'bio': '',
            'funnel_links': [],
            'pinned_tweet': '',
            'profile_pic_style': '',
            'banner_style': '',
            'follower_count': '',
            'following_count': '',
            'tweet_count': ''
        }
        
        # Get bio
        try:
            bio_elem = page.locator('div[data-testid="UserDescription"]').first
            if await bio_elem.count() > 0:
                profile_data['bio'] = await bio_elem.inner_text()
        except:
            pass
        
        # Get links in bio
        try:
            link_elems = await page.locator('a[href*="//t.co/"]').all()
            for link in link_elems[:5]:
                href = await link.get_attribute('href')
                if href and 't.co' in href:
                    profile_data['funnel_links'].append(href)
        except:
            pass
        
        # Get stats
        try:
            # Followers
            follower_elem = page.locator('a[href*="/verified_followers"] span').first
            if await follower_elem.count() > 0:
                profile_data['follower_count'] = await follower_elem.inner_text()
        except:
            pass
        
        # Get pinned tweet
        try:
            pinned = page.locator('div[data-testid="tweet"]:has-text("Pinned")').first
            if await pinned.count() > 0:
                pinned_text = await pinned.locator('[data-testid="tweetText"]').first.inner_text()
                profile_data['pinned_tweet'] = pinned_text[:500]
        except:
            pass
        
        # Screenshot profile
        try:
            screenshot_path = OUTPUT_DIR / f"profile_{username.replace('@', '').replace(' ', '_')}.png"
            await page.screenshot(path=str(screenshot_path), full_page=False)
            profile_data['screenshot'] = str(screenshot_path)
        except:
            pass
        
        return profile_data
        
    except Exception as e:
        print(f"  ❌ Profile error: {e}")
        return None

async def analyze_post_replies(page, post_url):
    """Analyze replies for funnel links and engagement quality"""
    try:
        await page.goto(post_url, wait_until="load", timeout=15000)
        await asyncio.sleep(3)
        
        # Scroll to load more replies
        for _ in range(3):
            await page.evaluate("window.scrollBy(0, 800)")
            await asyncio.sleep(1)
        
        replies_data = {
            'total_visible_replies': 0,
            'author_replies': [],
            'offer_links_found': [],
            'dm_triggers': [],
            'engagement_quality': 'unknown'
        }
        
        # Get all reply tweets
        reply_tweets = await page.locator('article[data-testid="tweet"]').all()
        replies_data['total_visible_replies'] = len(reply_tweets)
        
        for tweet in reply_tweets[:20]:  # Check first 20 replies
            try:
                # Get author
                author_elem = tweet.locator('[data-testid="User-Name"]').first
                author_text = await author_elem.inner_text() if await author_elem.count() > 0 else ""
                
                # Get reply text
                text_elem = tweet.locator('[data-testid="tweetText"]').first
                reply_text = await text_elem.inner_text() if await text_elem.count() > 0 else ""
                
                # Check if author is replying to their own thread (funnel)
                if reply_text:
                    # Look for offer links
                    link_patterns = ['gumroad', 'lemonsqueezy', 'stripe', 'checkout', 'buy', 'shop']
                    if any(pattern in reply_text.lower() for pattern in link_patterns):
                        replies_data['author_replies'].append({
                            'author': author_text.split('\n')[0] if author_text else '',
                            'text': reply_text[:300],
                            'type': 'offer_link'
                        })
                    
                    # Check for DM triggers
                    dm_patterns = ['dm me', 'send me a dm', 'reply and i\'ll dm', 'like and repost', 
                                   'comment below', 'drop a', 'reply with']
                    if any(pattern in reply_text.lower() for pattern in dm_patterns):
                        replies_data['dm_triggers'].append({
                            'text': reply_text[:200],
                            'trigger_type': next((p for p in dm_patterns if p in reply_text.lower()), 'unknown')
                        })
                    
                    # Extract URLs
                    urls = re.findall(r'https?://\S+', reply_text)
                    if urls:
                        replies_data['offer_links_found'].extend(urls[:3])
                        
            except:
                continue
        
        # Assess engagement quality (basic heuristic)
        if replies_data['total_visible_replies'] > 10:
            # Check for bot patterns
            unique_authors = set()
            for reply in replies_data['author_replies']:
                unique_authors.add(reply.get('author', ''))
            
            if len(unique_authors) > 5:
                replies_data['engagement_quality'] = 'authentic'
            elif len(unique_authors) <= 2:
                replies_data['engagement_quality'] = 'suspicious_bot_farm'
            else:
                replies_data['engagement_quality'] = 'moderate'
        
        return replies_data
        
    except Exception as e:
        print(f"  ❌ Replies error: {e}")
        return None

async def analyze_engagement_metrics(page, post_url):
    """Extract engagement metrics to filter bot activity"""
    try:
        await page.goto(post_url, wait_until="load", timeout=15000)
        await asyncio.sleep(2)
        
        metrics = {
            'likes': 0,
            'retweets': 0,
            'replies': 0,
            'views': 0,
            'engagement_ratio': 0
        }
        
        # Get metrics
        try:
            # Likes
            like_btn = page.locator('button[data-testid="like"]').first
            if await like_btn.count() > 0:
                like_text = await like_btn.inner_text()
                metrics['likes'] = parse_metric(like_text)
            
            # Retweets
            retweet_btn = page.locator('button[data-testid="retweet"]').first
            if await retweet_btn.count() > 0:
                rt_text = await retweet_btn.inner_text()
                metrics['retweets'] = parse_metric(rt_text)
            
            # Replies
            reply_btn = page.locator('button[data-testid="reply"]').first
            if await reply_btn.count() > 0:
                reply_text = await reply_btn.inner_text()
                metrics['replies'] = parse_metric(reply_text)
            
            # Calculate ratio (higher = more authentic)
            if metrics['likes'] > 0:
                metrics['engagement_ratio'] = (metrics['replies'] + metrics['retweets']) / metrics['likes']
        
        except:
            pass
        
        return metrics
        
    except Exception as e:
        return None

def parse_metric(text):
    """Parse engagement numbers like '1.2K' to integers"""
    try:
        text = text.strip().upper()
        if 'K' in text:
            return int(float(text.replace('K', '')) * 1000)
        elif 'M' in text:
            return int(float(text.replace('M', '')) * 1000000)
        else:
            return int(text) if text.isdigit() else 0
    except:
        return 0

async def main():
    # Load extracted alpha
    with open(INPUT_FILE, 'r') as f:
        alpha = json.load(f)
    
    # Combine all high-value posts
    all_posts = []
    all_posts.extend(alpha['revenue_playbooks'][:10])  # Top 10 revenue
    all_posts.extend(alpha['technical_playbooks'][:5])  # Top 5 technical
    
    print(f"🔍 Deep analyzing {len(all_posts)} high-value posts...")
    print("   - Profile monetization setup")
    print("   - Reply funnel analysis")
    print("   - Engagement authenticity")
    print("   - DM trigger strategies\n")
    
    async with async_playwright() as p:
        # Connect to Brave
        print("🔌 Connecting to Brave...")
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            print("✅ Connected!\n")
        except Exception as e:
            print(f"❌ Could not connect: {e}")
            return
        
        contexts = browser.contexts
        if not contexts:
            print("❌ No browser contexts")
            return
        
        context = contexts[0]
        pages = context.pages
        page = pages[0] if pages else await context.new_page()
        
        results = []
        
        for i, post in enumerate(all_posts, 1):
            author = post['author']
            url = post['url']
            
            print(f"[{i}/{len(all_posts)}] Analyzing: {author}")
            print(f"   URL: {url}")
            
            analysis = {
                'author': author,
                'url': url,
                'profile': None,
                'replies': None,
                'engagement': None
            }
            
            # 1. Profile analysis
            try:
                username = author.split()[0] if author else ''
                profile = await analyze_profile(page, username, url)
                if profile:
                    analysis['profile'] = profile
                    print(f"   ✅ Profile: {len(profile.get('funnel_links', []))} funnel links")
            except Exception as e:
                print(f"   ❌ Profile failed: {e}")
            
            await asyncio.sleep(1)
            
            # 2. Reply analysis
            try:
                replies = await analyze_post_replies(page, url)
                if replies:
                    analysis['replies'] = replies
                    print(f"   ✅ Replies: {replies['total_visible_replies']} found, {len(replies['dm_triggers'])} DM triggers")
            except Exception as e:
                print(f"   ❌ Replies failed: {e}")
            
            await asyncio.sleep(1)
            
            # 3. Engagement metrics
            try:
                metrics = await analyze_engagement_metrics(page, url)
                if metrics:
                    analysis['engagement'] = metrics
                    print(f"   ✅ Engagement: {metrics['likes']} likes, ratio {metrics['engagement_ratio']:.2f}")
            except Exception as e:
                print(f"   ❌ Metrics failed: {e}")
            
            results.append(analysis)
            
            # Rate limit
            await asyncio.sleep(2)
            print()
        
        # Save results
        output_file = OUTPUT_DIR / f"funnel_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Analysis complete!")
        print(f"📁 Saved to: {output_file}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
