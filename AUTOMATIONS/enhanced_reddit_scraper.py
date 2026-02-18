#!/usr/bin/env python3
"""
ENHANCED REDDIT SCRAPER - Gets posts AND top comments for deeper insight.
Runs headless in background.
"""

import asyncio
import csv
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).parent.parent
ALPHA_STAGING = BASE_DIR / "LEDGER" / "ALPHA_STAGING.csv"

SUBREDDITS = [
    'SideProject', 'EntrepreneurRideAlong', 'juststart', 'coldemail',
    'indiehackers', 'SaaS', 'growthhacking', 'AppBusiness', 'Entrepreneur',
    'startups', 'smallbusiness', 'marketing', 'SEO', 'affiliatemarketing'
]

def get_next_alpha_id():
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

async def scrape_post_with_comments(page, post_url, subreddit):
    """Scrape a post AND its top 3 comments"""
    try:
        await page.goto(post_url, timeout=30000)
        await page.wait_for_timeout(2000)

        # Get post content and top comments
        data = await page.evaluate("""
            () => {
                const result = { post: null, comments: [] };

                // Get post text (self posts)
                const selftext = document.querySelector('.usertext-body');
                if (selftext) {
                    result.post = selftext.innerText.substring(0, 1000);
                }

                // Get top 3 comments
                const comments = document.querySelectorAll('.comment .usertext-body');
                for (let i = 0; i < Math.min(comments.length, 3); i++) {
                    const text = comments[i].innerText.substring(0, 500);
                    if (text.length > 20) {
                        result.comments.push(text);
                    }
                }

                return result;
            }
        """)

        return data

    except Exception as e:
        print(f"      Error getting comments: {e}")
        return {'post': None, 'comments': []}

async def scrape_subreddit_with_comments(page, subreddit):
    """Scrape top posts + their comments from a subreddit"""
    results = []
    try:
        print(f"  r/{subreddit}...")
        url = f"https://old.reddit.com/r/{subreddit}/top/?t=week"
        await page.goto(url, timeout=30000)
        await page.wait_for_timeout(2000)

        # Get top posts
        posts = await page.evaluate("""
            () => {
                const posts = [];
                const entries = document.querySelectorAll('.thing.link');

                for (let i = 0; i < Math.min(entries.length, 5); i++) {
                    const entry = entries[i];
                    try {
                        const titleElem = entry.querySelector('a.title');
                        const scoreElem = entry.querySelector('.score.unvoted');
                        const commentsLink = entry.querySelector('.comments');

                        if (titleElem) {
                            const title = titleElem.innerText;
                            const url = commentsLink ? commentsLink.href : titleElem.href;
                            const score = scoreElem ? scoreElem.innerText : '0';

                            // Filter for business content
                            const hasValue = (
                                title.length > 20 &&
                                (
                                    /\\$\\d+|\\d+k|revenue|mrr|arr|profit|sales/.test(title.toLowerCase()) ||
                                    /how\\s+(i|to|we)|step|guide|framework|launched|built|made/.test(title.toLowerCase()) ||
                                    /saas|app|product|startup|business|side\\s*project/.test(title.toLowerCase())
                                )
                            );

                            if (hasValue) {
                                posts.push({ title, url, score });
                            }
                        }
                    } catch(e) {}
                }
                return posts;
            }
        """)

        # For each post, get comments
        for post in posts[:3]:  # Top 3 posts per subreddit
            print(f"    Getting comments for: {post['title'][:50]}...")
            comment_data = await scrape_post_with_comments(page, post['url'], subreddit)

            results.append({
                'subreddit': subreddit,
                'title': post['title'],
                'url': post['url'],
                'score': post['score'],
                'post_content': comment_data['post'],
                'top_comments': comment_data['comments']
            })

            await page.wait_for_timeout(1000)

        print(f"    Found {len(results)} posts with comments")

    except Exception as e:
        print(f"    Error: {e}")

    return results

async def main():
    print("=" * 60)
    print("ENHANCED REDDIT SCRAPER - Posts + Top Comments")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    all_posts = []

    async with async_playwright() as p:
        print("\nLaunching headless browser...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await context.new_page()

        for sub in SUBREDDITS:
            posts = await scrape_subreddit_with_comments(page, sub)
            all_posts.extend(posts)
            await page.wait_for_timeout(500)

        await browser.close()

    print(f"\n{'=' * 60}")
    print(f"Total posts with comments: {len(all_posts)}")

    if all_posts:
        # Load existing URLs
        existing_urls = set()
        if ALPHA_STAGING.exists():
            with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('source_url'):
                        existing_urls.add(row['source_url'])

        new_posts = [p for p in all_posts if p['url'] not in existing_urls]
        print(f"New unique posts: {len(new_posts)}")

        if new_posts:
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

                for post in new_posts:
                    # Build tactic with comments
                    tactic = f"POST: {post['title'][:200]}"
                    if post['post_content']:
                        tactic += f" | CONTENT: {post['post_content'][:200]}"
                    if post['top_comments']:
                        for i, comment in enumerate(post['top_comments'][:2]):
                            tactic += f" | COMMENT{i+1}: {comment[:150]}"

                    writer.writerow({
                        'alpha_id': f'ALPHA{alpha_id:04d}',
                        'source': f"r/{post['subreddit']} (Reddit)",
                        'source_url': post['url'],
                        'category': 'GROWTH_HACK',
                        'tactic': tactic[:1500],
                        'roi_potential': 'MEDIUM',
                        'priority': 'MEDIUM',
                        'status': 'PENDING_REVIEW',
                        'applicable_methods': '',
                        'applicable_niches': '',
                        'synergy_score': '',
                        'reviewer_notes': f"Score: {post['score']} | Has {len(post['top_comments'])} comments analyzed",
                        'quality_issues': '',
                        'engagement_authenticity': 'AUTHENTIC',
                        'earnings_verified': 'FALSE',
                        'extracted_method': '',
                        'compliance_notes': '',
                        'date_added': datetime.now().strftime('%Y-%m-%d')
                    })
                    alpha_id += 1

            print(f"Saved {len(new_posts)} entries with comments to ALPHA_STAGING.csv")

    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
