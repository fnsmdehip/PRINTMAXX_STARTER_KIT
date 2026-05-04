#!/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
"""
DAILY AUTOMATED REDDIT SCRAPER
Scrapes top posts + top comments from all tracked subreddits
Runs daily via cron
"""

import asyncio
import csv
import re
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

# Paths
BASE_DIR = Path(__file__).parent.parent
RESEARCH_SUBREDDITS = BASE_DIR / "LEDGER" / "RESEARCH_SUBREDDITS.csv"
ALPHA_STAGING = BASE_DIR / "LEDGER" / "ALPHA_STAGING.csv"
CHROME_PROFILE = Path.home() / "Library/Application Support/Google/Chrome/Default"

def load_subreddits():
    """Load all auto_monitor subreddits"""
    subreddits = []
    with open(RESEARCH_SUBREDDITS, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('auto_monitor') == 'TRUE':
                name = row.get('subreddit_name', '').replace('r/', '').strip()
                if name:
                    subreddits.append(name)
    return subreddits

async def scrape_subreddit(page, subreddit):
    """Scrape top posts + comments from subreddit"""
    print(f"🔍 r/{subreddit}")

    try:
        # Go to top posts this week
        await page.goto(f"https://reddit.com/r/{subreddit}/top/?t=week", timeout=30000)
        await page.wait_for_timeout(3000)

        posts = []

        # Get top 10 posts
        post_elements = await page.query_selector_all('div[data-testid="post-container"]')

        for post_elem in post_elements[:10]:
            try:
                # Get post title and link
                title_elem = await post_elem.query_selector('a[data-click-id="body"]')
                if not title_elem:
                    continue

                title = await title_elem.text_content()
                href = await title_elem.get_attribute('href')

                # Make full URL
                if href.startswith('/r/'):
                    url = f"https://reddit.com{href}"
                else:
                    url = href

                # Filter for business content
                has_value = (
                    len(title) > 20 and
                    any(kw in title.lower() for kw in [
                        'revenue', 'mrr', 'arr', '$', 'made', 'launch', 'build',
                        'saas', 'app', 'startup', 'tool', 'product', 'sell',
                        'growth', 'traffic', 'seo', 'marketing', 'users'
                    ])
                )

                if has_value:
                    # Click into post to get top comments
                    await title_elem.click()
                    await page.wait_for_timeout(2000)

                    # Get top 3 comments
                    comments = []
                    comment_elements = await page.query_selector_all('[data-testid="comment"]')

                    for comment_elem in comment_elements[:3]:
                        try:
                            comment_text_elem = await comment_elem.query_selector('[data-testid="comment-text"]')
                            if comment_text_elem:
                                comment_text = await comment_text_elem.text_content()
                                if len(comment_text) > 50:
                                    comments.append(comment_text)
                        except Exception:
                            pass  # Comment element extraction is best-effort

                    # Go back
                    await page.go_back()
                    await page.wait_for_timeout(1500)

                    posts.append({
                        'subreddit': subreddit,
                        'url': url,
                        'title': title,
                        'top_comments': comments
                    })

            except Exception as e:
                continue

        print(f"  ✓ {len(posts)} actionable posts")
        return posts

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return []

def get_next_alpha_id():
    """Get next available ALPHA ID"""
    max_id = 0
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                match = re.match(r'ALPHA(\d+)', row.get('alpha_id', ''))
                if match:
                    max_id = max(max_id, int(match.group(1)))
    return max_id + 1

def load_existing_urls():
    """Load existing URLs"""
    urls = set()
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row.get('source_url', '').strip()
                if url:
                    urls.add(url)
    return urls

def categorize(text):
    """Auto-categorize"""
    t = text.lower()
    if any(w in t for w in ['app', 'mobile', 'ios']):
        return 'APP_FACTORY'
    elif any(w in t for w in ['email', 'cold']):
        return 'COLD_OUTBOUND'
    elif any(w in t for w in ['seo', 'search']):
        return 'SEO_GEO_ASO'
    elif any(w in t for w in ['content', 'tiktok']):
        return 'CONTENT_FARM'
    elif any(w in t for w in ['ai', 'automation', 'tool']):
        return 'TOOL_ALPHA'
    elif any(w in t for w in ['revenue', 'pricing', '$']):
        return 'MONETIZATION'
    elif any(w in t for w in ['growth', 'traffic']):
        return 'GROWTH_HACK'
    return 'GENERAL'

def save_to_csv(all_posts):
    """Save to ALPHA_STAGING.csv"""
    existing_urls = load_existing_urls()

    new_posts = [p for p in all_posts if p['url'] not in existing_urls]

    if not new_posts:
        print("\n✓ No new posts (all already in CSV)")
        return

    print(f"\n💾 Saving {len(new_posts)} new posts...")

    # Read existing
    rows = []
    fieldnames = []
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            rows = list(reader)
    else:
        fieldnames = [
            'alpha_id', 'source', 'source_url', 'category', 'tactic',
            'roi_potential', 'priority', 'status', 'applicable_methods',
            'applicable_niches', 'synergy_score', 'reviewer_notes',
            'quality_issues', 'engagement_authenticity', 'earnings_verified',
            'extracted_method', 'compliance_notes', 'date_added'
        ]

    # Add new
    next_id = get_next_alpha_id()
    for post in new_posts:
        cat = categorize(post['title'])

        # Combine title + top comment insights
        tactic = f"{post['title']}"
        if post['top_comments']:
            tactic += f"\n\nTop insight: {post['top_comments'][0][:200]}"

        row = {k: '' for k in fieldnames}
        row.update({
            'alpha_id': f'ALPHA{next_id}',
            'source': f"r/{post['subreddit']} (daily scraper)",
            'source_url': post['url'],
            'category': cat,
            'tactic': tactic[:500],
            'roi_potential': 'MEDIUM',
            'priority': 'SOON',
            'status': 'PENDING_REVIEW',
            'applicable_methods': 'ALL',
            'applicable_niches': 'ALL',
            'synergy_score': '75',
            'reviewer_notes': f"Daily Reddit scrape {datetime.now().isoformat()}",
            'quality_issues': '',
            'engagement_authenticity': 'AUTHENTIC',
            'earnings_verified': 'FALSE',
            'extracted_method': '',
            'compliance_notes': '',
            'date_added': datetime.now().isoformat()
        })
        rows.append(row)
        next_id += 1

    # Write
    with open(ALPHA_STAGING, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Added ALPHA{next_id - len(new_posts)}-ALPHA{next_id - 1}")

async def main():
    """Main scraper"""
    print("🚀 DAILY REDDIT SCRAPER")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    subreddits = load_subreddits()
    print(f"📋 {len(subreddits)} subreddits to scrape\n")

    all_posts = []

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(CHROME_PROFILE),
            headless=True,
            args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
        )

        page = await context.new_page()

        for i, subreddit in enumerate(subreddits, 1):
            print(f"[{i}/{len(subreddits)}]", end=' ')
            posts = await scrape_subreddit(page, subreddit)
            all_posts.extend(posts)

            await asyncio.sleep(2)

        await context.close()

    print(f"\n📊 Total actionable posts: {len(all_posts)}")
    save_to_csv(all_posts)

    print("\n✅ DAILY REDDIT SCRAPE COMPLETE")
    print(f"📁 Check: {ALPHA_STAGING}")

if __name__ == "__main__":
    asyncio.run(main())
