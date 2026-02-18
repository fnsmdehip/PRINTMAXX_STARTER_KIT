#!/usr/bin/env python3
"""
HEADLESS REDDIT SCRAPER - No login needed, public posts/comments.
Runs in background, no visible browser.
"""

import asyncio
import csv
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).parent.parent
SUBREDDITS_FILE = BASE_DIR / "LEDGER" / "RESEARCH_SUBREDDITS.csv"
ALPHA_STAGING = BASE_DIR / "LEDGER" / "ALPHA_STAGING.csv"

# Default subreddits if file not found
DEFAULT_SUBREDDITS = [
    'SideProject', 'EntrepreneurRideAlong', 'juststart', 'coldemail',
    'indiehackers', 'SaaS', 'growthhacking', 'AppBusiness', 'Entrepreneur',
    'startups', 'smallbusiness', 'marketing', 'SEO', 'affiliatemarketing'
]

def load_subreddits():
    """Load subreddits to scrape"""
    subreddits = []
    if SUBREDDITS_FILE.exists():
        with open(SUBREDDITS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('auto_monitor') == 'TRUE':
                    sub = row.get('subreddit', row.get('name', '')).replace('r/', '').strip()
                    if sub:
                        subreddits.append(sub)
    return subreddits if subreddits else DEFAULT_SUBREDDITS

def get_next_alpha_id():
    """Get next alpha ID"""
    if not ALPHA_STAGING.exists():
        return "ALPHA0001"
    with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if len(lines) <= 1:
            return "ALPHA0001"
        try:
            last_id = lines[-1].split(',')[0]
            num = int(last_id.replace('ALPHA', ''))
            return f"ALPHA{num + 1:04d}"
        except:
            return "ALPHA9000"

async def scrape_subreddit(page, subreddit):
    """Scrape top posts from a subreddit"""
    posts = []
    try:
        print(f"  Scraping r/{subreddit}...")
        url = f"https://old.reddit.com/r/{subreddit}/top/?t=week"
        await page.goto(url, timeout=30000)
        await page.wait_for_timeout(2000)

        # Extract posts using old reddit (simpler HTML)
        extracted = await page.evaluate("""
            () => {
                const posts = [];
                const entries = document.querySelectorAll('.thing.link');

                for (let i = 0; i < Math.min(entries.length, 10); i++) {
                    const entry = entries[i];
                    try {
                        const titleElem = entry.querySelector('a.title');
                        const scoreElem = entry.querySelector('.score.unvoted');
                        const commentsElem = entry.querySelector('.comments');

                        if (titleElem) {
                            const title = titleElem.innerText;
                            const url = titleElem.href;
                            const score = scoreElem ? scoreElem.innerText : '0';
                            const comments = commentsElem ? commentsElem.innerText : '0 comments';

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
                                posts.push({ title, url, score, comments });
                            }
                        }
                    } catch(e) {}
                }
                return posts;
            }
        """)

        for post in extracted:
            post['subreddit'] = subreddit
        posts.extend(extracted)

        print(f"    Found {len(extracted)} actionable posts in r/{subreddit}")

    except Exception as e:
        print(f"    Error scraping r/{subreddit}: {e}")

    return posts

async def main():
    print("=" * 60)
    print("HEADLESS REDDIT SCRAPER - Background Mode (No Login)")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    subreddits = load_subreddits()
    print(f"Loaded {len(subreddits)} subreddits to scrape")

    all_posts = []

    async with async_playwright() as p:
        print("\nLaunching headless browser...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await context.new_page()

        for sub in subreddits:
            posts = await scrape_subreddit(page, sub)
            all_posts.extend(posts)
            await page.wait_for_timeout(1000)  # Rate limit

        await browser.close()

    print(f"\n{'=' * 60}")
    print(f"Total posts found: {len(all_posts)}")

    if all_posts:
        # Load existing URLs to dedupe
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
            alpha_id_start = int(get_next_alpha_id().replace('ALPHA', ''))

            with open(ALPHA_STAGING, 'a', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'alpha_id', 'source', 'source_url', 'category', 'tactic',
                    'roi_potential', 'priority', 'status', 'applicable_methods',
                    'applicable_niches', 'synergy_score', 'reviewer_notes',
                    'quality_issues', 'engagement_authenticity', 'earnings_verified',
                    'extracted_method', 'compliance_notes', 'date_added'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                for i, post in enumerate(new_posts):
                    # Auto-categorize
                    title_lower = post['title'].lower()
                    if 'email' in title_lower or 'outreach' in title_lower:
                        category = 'COLD_OUTBOUND'
                    elif 'app' in title_lower or 'mobile' in title_lower:
                        category = 'APP_FACTORY'
                    elif 'content' in title_lower or 'youtube' in title_lower:
                        category = 'CONTENT_FARM'
                    elif '$' in title_lower or 'revenue' in title_lower:
                        category = 'MONETIZATION'
                    elif 'seo' in title_lower:
                        category = 'SEO_GEO_ASO'
                    else:
                        category = 'GROWTH_HACK'

                    writer.writerow({
                        'alpha_id': f'ALPHA{alpha_id_start + i:04d}',
                        'source': f'r/{post["subreddit"]} (Reddit)',
                        'source_url': post['url'],
                        'category': category,
                        'tactic': f'{post["title"]} [Score: {post["score"]}]',
                        'roi_potential': 'MEDIUM',
                        'priority': 'MEDIUM',
                        'status': 'PENDING_REVIEW',
                        'applicable_methods': '',
                        'applicable_niches': '',
                        'synergy_score': '',
                        'reviewer_notes': '',
                        'quality_issues': '',
                        'engagement_authenticity': 'AUTHENTIC',
                        'earnings_verified': 'FALSE',
                        'extracted_method': '',
                        'compliance_notes': '',
                        'date_added': datetime.now().strftime('%Y-%m-%d')
                    })

            print(f"Saved {len(new_posts)} new entries to ALPHA_STAGING.csv")

    print("=" * 60)
    print("DONE - Reddit scraper ran in BACKGROUND")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
