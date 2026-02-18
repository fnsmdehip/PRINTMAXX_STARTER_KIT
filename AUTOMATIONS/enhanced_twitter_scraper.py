#!/usr/bin/env python3
"""
ENHANCED TWITTER SCRAPER - Gets tweets AND top replies for reply funnel analysis.
Detects self-reply funnels (when top reply is from same user).
Runs headless in background.
"""

import asyncio
import csv
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).parent.parent
HIGH_SIGNAL_SOURCES = BASE_DIR / "LEDGER" / "HIGH_SIGNAL_SOURCES.csv"
ALPHA_STAGING = BASE_DIR / "LEDGER" / "ALPHA_STAGING.csv"
CHROME_PROFILE = Path.home() / ".printmaxx-chrome-profile"

def load_accounts():
    """Load Twitter accounts to scrape"""
    accounts = []
    with open(HIGH_SIGNAL_SOURCES, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('platform') in ['X', 'Twitter'] and row.get('auto_monitor') == 'TRUE':
                handle = row.get('source_name', '').replace('@', '').strip()
                if handle:
                    accounts.append(handle)
    return accounts

def get_next_alpha_id():
    """Get next alpha ID from staging file"""
    if not ALPHA_STAGING.exists():
        return 1
    with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if len(lines) <= 1:
            return 1
        try:
            last_id = lines[-1].split(',')[0]
            return int(last_id.replace('ALPHA', '')) + 1
        except:
            return 9000

async def analyze_tweet_replies(page, tweet_url, original_handle):
    """
    Navigate to tweet and analyze replies for:
    1. Self-reply funnel detection (top reply from same user)
    2. Top 3 replies for additional insight
    """
    try:
        await page.goto(tweet_url, timeout=30000)
        await page.wait_for_timeout(3000)

        # Expand any "Show more" buttons
        try:
            await page.evaluate("""
                () => {
                    document.querySelectorAll('[data-testid="tweet-text-show-more-link"]').forEach(btn => {
                        try { btn.click(); } catch(e) {}
                    });
                }
            """)
        except:
            pass

        await page.wait_for_timeout(1000)

        # Extract tweet content and replies
        data = await page.evaluate("""
            (originalHandle) => {
                const result = {
                    tweet_content: null,
                    is_self_reply_funnel: false,
                    self_reply_content: null,
                    top_replies: [],
                    reply_insights: []
                };

                // Get all tweet articles
                const articles = document.querySelectorAll('article[data-testid="tweet"]');

                if (articles.length > 0) {
                    // First article is the main tweet
                    const mainTweet = articles[0];
                    const mainText = mainTweet.querySelector('[data-testid="tweetText"]');
                    if (mainText) {
                        result.tweet_content = mainText.innerText;
                    }
                }

                // Check replies (articles after the first one)
                for (let i = 1; i < Math.min(articles.length, 5); i++) {
                    const reply = articles[i];
                    try {
                        // Get reply author
                        const authorLinks = reply.querySelectorAll('a[role="link"]');
                        let replyHandle = null;
                        for (const link of authorLinks) {
                            const href = link.getAttribute('href');
                            if (href && href.startsWith('/') && !href.includes('/status/')) {
                                replyHandle = href.replace('/', '').toLowerCase();
                                break;
                            }
                        }

                        // Get reply text
                        const replyText = reply.querySelector('[data-testid="tweetText"]');
                        const text = replyText ? replyText.innerText : '';

                        if (text.length > 10) {
                            // Check if self-reply (same author as original)
                            const isSelfReply = replyHandle &&
                                replyHandle.toLowerCase() === originalHandle.toLowerCase();

                            if (i === 1 && isSelfReply) {
                                // First reply is self-reply = funnel detected!
                                result.is_self_reply_funnel = true;
                                result.self_reply_content = text.substring(0, 500);
                            }

                            result.top_replies.push({
                                handle: replyHandle || 'unknown',
                                text: text.substring(0, 300),
                                is_self_reply: isSelfReply
                            });

                            // Extract any links or CTAs from replies
                            if (text.match(/gumroad|link|dm me|reply|bio|check out/i)) {
                                result.reply_insights.push(`CTA detected: ${text.substring(0, 100)}`);
                            }
                        }
                    } catch(e) {}
                }

                return result;
            }
        """, original_handle)

        return data

    except Exception as e:
        print(f"      Error analyzing replies: {e}")
        return {
            'tweet_content': None,
            'is_self_reply_funnel': False,
            'self_reply_content': None,
            'top_replies': [],
            'reply_insights': []
        }

async def scrape_account_with_replies(page, handle, batch_num):
    """Scrape tweets + analyze replies from a single account"""
    tweets = []
    try:
        print(f"[BATCH {batch_num}] Scraping @{handle}...")
        await page.goto(f"https://x.com/{handle}", timeout=30000)
        await page.wait_for_timeout(3000)

        # Scroll and extract tweets
        for scroll in range(2):
            # Click "show more" buttons
            try:
                await page.evaluate("""
                    () => {
                        document.querySelectorAll('[data-testid="tweet-text-show-more-link"]').forEach(btn => {
                            try { btn.click(); } catch(e) {}
                        });
                    }
                """)
            except:
                pass

            await page.wait_for_timeout(500)

            # Extract tweets
            extracted = await page.evaluate("""
                () => {
                    const tweets = [];
                    const articles = document.querySelectorAll('article[data-testid="tweet"]');

                    articles.forEach(article => {
                        try {
                            const link = article.querySelector('a[href*="/status/"]');
                            const textElem = article.querySelector('[data-testid="tweetText"]');

                            if (link && textElem) {
                                const text = textElem.innerText;

                                // Filter for actionable business content
                                const hasValue = (
                                    text.length > 50 &&
                                    (
                                        /\\.(com|io|ai|app|co)\\b/.test(text) ||
                                        /\\$\\d+|revenue|mrr|arr|\\d+%|\\d+x/.test(text.toLowerCase()) ||
                                        /step\\s+\\d+|how\\s+to|framework|playbook|guide/.test(text.toLowerCase()) ||
                                        /filter\\s+by|database|pull\\s+every|install|tech\\s+stack/.test(text.toLowerCase()) ||
                                        /cold\\s+email|outreach|dm|lead|funnel/.test(text.toLowerCase())
                                    )
                                );

                                if (hasValue) {
                                    tweets.push({ url: link.href, text });
                                }
                            }
                        } catch(e) {}
                    });

                    return tweets;
                }
            """)

            tweets.extend(extracted)

            # Scroll
            await page.evaluate("window.scrollBy(0, 800)")
            await page.wait_for_timeout(1000)

        # Dedupe
        seen = set()
        unique = []
        for tweet in tweets:
            if tweet['url'] not in seen:
                seen.add(tweet['url'])
                tweet['handle'] = handle
                unique.append(tweet)

        # For top tweets, analyze replies (limit to top 3 to save time)
        analyzed_tweets = []
        for tweet in unique[:3]:
            print(f"[BATCH {batch_num}]   Analyzing replies for tweet...")
            reply_data = await analyze_tweet_replies(page, tweet['url'], handle)

            analyzed_tweets.append({
                'handle': handle,
                'url': tweet['url'],
                'text': tweet['text'],
                'tweet_content': reply_data.get('tweet_content'),
                'is_self_reply_funnel': reply_data.get('is_self_reply_funnel', False),
                'self_reply_content': reply_data.get('self_reply_content'),
                'top_replies': reply_data.get('top_replies', []),
                'reply_insights': reply_data.get('reply_insights', [])
            })

            await page.wait_for_timeout(1000)

        # Add remaining tweets without reply analysis
        for tweet in unique[3:]:
            analyzed_tweets.append({
                'handle': handle,
                'url': tweet['url'],
                'text': tweet['text'],
                'tweet_content': None,
                'is_self_reply_funnel': False,
                'self_reply_content': None,
                'top_replies': [],
                'reply_insights': []
            })

        funnel_count = sum(1 for t in analyzed_tweets if t.get('is_self_reply_funnel'))
        print(f"[BATCH {batch_num}]   Found {len(analyzed_tweets)} tweets, {funnel_count} self-reply funnels")
        return analyzed_tweets

    except Exception as e:
        print(f"[BATCH {batch_num}]   Error scraping @{handle}: {e}")
        return []

async def main():
    print("=" * 60)
    print("ENHANCED TWITTER SCRAPER - Tweets + Reply Funnel Analysis")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    accounts = load_accounts()
    print(f"Loaded {len(accounts)} accounts to scrape")

    if not CHROME_PROFILE.exists():
        print(f"ERROR: Chrome profile not found at {CHROME_PROFILE}")
        print("Run Chrome with --user-data-dir first and log into Twitter")
        return

    all_tweets = []

    async with async_playwright() as p:
        print("\nLaunching headless browser with saved session...")

        try:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(CHROME_PROFILE),
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                ]
            )

            # Create pages for parallel scraping
            num_parallel = 3  # Reduced for stability with reply analysis
            pages = [await context.new_page() for _ in range(num_parallel)]

            # Split accounts into batches
            batches = [accounts[i::num_parallel] for i in range(num_parallel)]

            # Scrape in parallel batches
            for batch_idx, batch in enumerate(batches):
                page = pages[batch_idx]
                for handle in batch[:10]:  # Limit per batch for testing
                    tweets = await scrape_account_with_replies(page, handle, batch_idx + 1)
                    all_tweets.extend(tweets)

            await context.close()

        except Exception as e:
            print(f"Error with persistent context: {e}")
            return

    # Save to CSV
    print(f"\n{'=' * 60}")
    print(f"Total tweets found: {len(all_tweets)}")

    # Count self-reply funnels
    funnel_tweets = [t for t in all_tweets if t.get('is_self_reply_funnel')]
    print(f"Self-reply funnels detected: {len(funnel_tweets)}")

    if all_tweets:
        # Load existing URLs to dedupe
        existing_urls = set()
        if ALPHA_STAGING.exists():
            with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('source_url'):
                        existing_urls.add(row['source_url'])

        new_tweets = [t for t in all_tweets if t['url'] not in existing_urls]
        print(f"New unique tweets (not in staging): {len(new_tweets)}")

        if new_tweets:
            alpha_id = get_next_alpha_id()

            with open(ALPHA_STAGING, 'a', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'alpha_id', 'source', 'source_url', 'category', 'tactic',
                    'roi_potential', 'priority', 'status', 'applicable_methods',
                    'applicable_niches', 'synergy_score', 'reviewer_notes',
                    'quality_issues', 'engagement_authenticity', 'earnings_verified',
                    'extracted_method', 'compliance_notes', 'date_added'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                for tweet in new_tweets:
                    # Build enhanced tactic with reply analysis
                    tactic = f"TWEET: {tweet['text'][:300]}"

                    # Add self-reply funnel info if detected
                    if tweet.get('is_self_reply_funnel'):
                        tactic += f" | SELF-REPLY FUNNEL: {tweet.get('self_reply_content', '')[:200]}"

                    # Add top replies for context
                    for i, reply in enumerate(tweet.get('top_replies', [])[:2]):
                        if not reply.get('is_self_reply'):  # Don't duplicate self-reply
                            tactic += f" | REPLY{i+1}(@{reply.get('handle', 'unknown')}): {reply.get('text', '')[:150]}"

                    # Add any insights
                    if tweet.get('reply_insights'):
                        tactic += f" | INSIGHTS: {'; '.join(tweet.get('reply_insights', []))}"

                    # Auto-categorize
                    text_lower = tweet['text'].lower()
                    if any(k in text_lower for k in ['cold email', 'outreach', 'email']):
                        category = 'COLD_OUTBOUND'
                    elif any(k in text_lower for k in ['app', 'ios', 'android', 'mobile']):
                        category = 'APP_FACTORY'
                    elif any(k in text_lower for k in ['content', 'tiktok', 'youtube', 'video']):
                        category = 'CONTENT_FARM'
                    elif any(k in text_lower for k in ['$', 'revenue', 'mrr', 'money']):
                        category = 'MONETIZATION'
                    elif any(k in text_lower for k in ['tool', 'api', 'automation']):
                        category = 'TOOL_ALPHA'
                    else:
                        category = 'GROWTH_HACK'

                    # Note if self-reply funnel detected
                    reviewer_notes = ""
                    if tweet.get('is_self_reply_funnel'):
                        reviewer_notes = "SELF-REPLY FUNNEL DETECTED - Check for CTA/product link"

                    writer.writerow({
                        'alpha_id': f'ALPHA{alpha_id:04d}',
                        'source': f'@{tweet["handle"]} (Twitter)',
                        'source_url': tweet['url'],
                        'category': category,
                        'tactic': tactic[:1500],
                        'roi_potential': 'MEDIUM',
                        'priority': 'HIGH' if tweet.get('is_self_reply_funnel') else 'MEDIUM',
                        'status': 'PENDING_REVIEW',
                        'applicable_methods': '',
                        'applicable_niches': '',
                        'synergy_score': '',
                        'reviewer_notes': reviewer_notes,
                        'quality_issues': '',
                        'engagement_authenticity': 'UNKNOWN',
                        'earnings_verified': 'FALSE',
                        'extracted_method': '',
                        'compliance_notes': '',
                        'date_added': datetime.now().strftime('%Y-%m-%d')
                    })
                    alpha_id += 1

            print(f"Saved {len(new_tweets)} new entries to ALPHA_STAGING.csv")
            print(f"  - {len([t for t in new_tweets if t.get('is_self_reply_funnel')])} with self-reply funnels")

    print("=" * 60)
    print("DONE - Enhanced Twitter scraper with reply analysis complete")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
