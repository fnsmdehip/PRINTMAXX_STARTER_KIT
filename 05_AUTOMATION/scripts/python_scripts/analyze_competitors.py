#!/usr/bin/env python3
"""
Competitor Content Analyzer - Scrape and analyze competitor content patterns
Uses Playwright for scraping, Claude for analysis

Usage:
    python analyze_competitors.py                          # Analyze all competitors
    python analyze_competitors.py --competitor zapier      # Specific competitor
    python analyze_competitors.py --platform x             # Only X/Twitter content
    python analyze_competitors.py --platform blog          # Only blog content
    python analyze_competitors.py --days 7                 # Content from last 7 days
    python analyze_competitors.py --analyze                # Include Claude analysis
    python analyze_competitors.py --output report.md       # Custom output file

Environment Variables:
    ANTHROPIC_API_KEY: Required for Claude analysis (optional)
    LEDGER_DIR: Path to LEDGER directory (default: ../LEDGER)

Output:
    CSV of competitor content: COMPETITOR_CONTENT.csv
    Analysis report: COMPETITOR_ANALYSIS.md (if --analyze)
"""

import argparse
import asyncio
import csv
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("ERROR: playwright not installed. Run: pip install playwright && playwright install")
    exit(1)


# Paths
BASE_DIR = Path(__file__).parent.parent.parent
LEDGER_DIR = Path(os.getenv("LEDGER_DIR", BASE_DIR / "LEDGER"))
COMPETITORS_CSV = LEDGER_DIR / "COMPETITORS.csv"
OUTPUT_CSV = LEDGER_DIR / "COMPETITOR_CONTENT.csv"
OUTPUT_REPORT = LEDGER_DIR / "COMPETITOR_ANALYSIS.md"

# Default competitors if no CSV exists
DEFAULT_COMPETITORS = [
    {
        "id": "COMP001",
        "name": "Zapier",
        "x_handle": "@zapier",
        "blog_url": "https://zapier.com/blog",
        "category": "automation"
    },
    {
        "id": "COMP002",
        "name": "Make",
        "x_handle": "@make_hq",
        "blog_url": "https://www.make.com/en/blog",
        "category": "automation"
    },
    {
        "id": "COMP003",
        "name": "Buffer",
        "x_handle": "@buffer",
        "blog_url": "https://buffer.com/resources",
        "category": "social"
    },
]


def load_competitors(competitor_filter: Optional[str] = None) -> list[dict]:
    """Load competitors from CSV or use defaults"""
    competitors = []

    if COMPETITORS_CSV.exists():
        with open(COMPETITORS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                competitors.append({
                    "id": row.get("competitor_id", ""),
                    "name": row.get("name", ""),
                    "x_handle": row.get("x_handle", ""),
                    "blog_url": row.get("blog_url", ""),
                    "category": row.get("category", "")
                })
    else:
        competitors = DEFAULT_COMPETITORS.copy()

    # Apply filter
    if competitor_filter:
        competitors = [
            c for c in competitors
            if competitor_filter.lower() in c["name"].lower()
        ]

    return competitors


async def scrape_x_content(page, handle: str, max_tweets: int = 20) -> list[dict]:
    """Scrape recent tweets from competitor X account"""
    content = []
    clean_handle = handle.lstrip("@")
    profile_url = f"https://x.com/{clean_handle}"

    try:
        await page.goto(profile_url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)

        # Scroll to load more
        for _ in range(3):
            await page.evaluate("window.scrollBy(0, 1500)")
            await asyncio.sleep(1)

        # Extract tweets
        tweets_data = await page.evaluate("""
            () => {
                const tweets = document.querySelectorAll('[data-testid="tweet"]');
                const results = [];

                for (let i = 0; i < Math.min(tweets.length, """ + str(max_tweets) + """); i++) {
                    const tweet = tweets[i];

                    const textEl = tweet.querySelector('[data-testid="tweetText"]');
                    const text = textEl ? textEl.innerText : '';

                    const timeEl = tweet.querySelector('time');
                    const timestamp = timeEl ? timeEl.getAttribute('datetime') : '';

                    const linkEl = tweet.querySelector('a[href*="/status/"]');
                    let url = '';
                    if (linkEl) {
                        const href = linkEl.getAttribute('href');
                        url = 'https://x.com' + href;
                    }

                    // Get engagement metrics
                    let likes = 0, retweets = 0, replies = 0, views = 0;
                    const metricsGroup = tweet.querySelector('[role="group"]');
                    if (metricsGroup) {
                        const spans = metricsGroup.querySelectorAll('span[data-testid]');
                        spans.forEach(span => {
                            const val = parseInt(span.innerText.replace(/[,K]/g, '')) || 0;
                            const mult = span.innerText.includes('K') ? 1000 : 1;
                            const testId = span.getAttribute('data-testid') || '';
                            if (testId.includes('like')) likes = val * mult;
                            else if (testId.includes('retweet')) retweets = val * mult;
                            else if (testId.includes('reply')) replies = val * mult;
                        });
                    }

                    // Check for media
                    const hasImage = tweet.querySelector('[data-testid="tweetPhoto"]') !== null;
                    const hasVideo = tweet.querySelector('[data-testid="videoPlayer"]') !== null;
                    const hasLink = tweet.querySelector('[data-testid="card.wrapper"]') !== null;

                    if (text) {
                        results.push({
                            text: text.substring(0, 1000),
                            timestamp: timestamp,
                            url: url,
                            likes: likes,
                            retweets: retweets,
                            replies: replies,
                            has_image: hasImage,
                            has_video: hasVideo,
                            has_link: hasLink
                        });
                    }
                }
                return results;
            }
        """)

        for tweet in (tweets_data or []):
            tweet["platform"] = "X"
            tweet["handle"] = handle
            content.append(tweet)

    except PlaywrightTimeout:
        print(f"    Timeout loading {handle}")
    except Exception as e:
        print(f"    Error: {e}")

    return content


async def scrape_blog_content(page, blog_url: str, max_posts: int = 10) -> list[dict]:
    """Scrape recent blog posts from competitor blog"""
    content = []

    try:
        await page.goto(blog_url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)

        # Try to find blog posts with common patterns
        posts_data = await page.evaluate("""
            () => {
                // Common blog post selectors
                const selectors = [
                    'article',
                    '[class*="post"]',
                    '[class*="blog"]',
                    '[class*="article"]',
                    '.card',
                    'a[href*="/blog/"]'
                ];

                const results = [];
                const seen = new Set();

                for (const selector of selectors) {
                    const elements = document.querySelectorAll(selector);

                    elements.forEach(el => {
                        // Find title
                        const titleEl = el.querySelector('h1, h2, h3, h4, [class*="title"]');
                        const title = titleEl ? titleEl.innerText.trim() : '';

                        // Find link
                        const linkEl = el.tagName === 'A' ? el : el.querySelector('a');
                        let url = linkEl ? linkEl.href : '';

                        // Find date
                        const dateEl = el.querySelector('time, [class*="date"], [datetime]');
                        const date = dateEl ? (dateEl.getAttribute('datetime') || dateEl.innerText) : '';

                        // Find excerpt
                        const excerptEl = el.querySelector('p, [class*="excerpt"], [class*="description"]');
                        const excerpt = excerptEl ? excerptEl.innerText.substring(0, 300) : '';

                        if (title && url && !seen.has(url) && title.length > 10) {
                            seen.add(url);
                            results.push({
                                title: title.substring(0, 200),
                                url: url,
                                date: date,
                                excerpt: excerpt
                            });
                        }
                    });

                    if (results.length >= """ + str(max_posts) + """) break;
                }

                return results.slice(0, """ + str(max_posts) + """);
            }
        """)

        for post in (posts_data or []):
            post["platform"] = "Blog"
            post["text"] = f"{post.get('title', '')}\n\n{post.get('excerpt', '')}"
            content.append(post)

    except PlaywrightTimeout:
        print(f"    Timeout loading {blog_url}")
    except Exception as e:
        print(f"    Error: {e}")

    return content


def analyze_content_patterns(content: list[dict]) -> dict:
    """Analyze content patterns without AI"""
    analysis = {
        "total_items": len(content),
        "by_platform": {},
        "by_competitor": {},
        "top_performing": [],
        "content_formats": {
            "with_image": 0,
            "with_video": 0,
            "with_link": 0,
            "text_only": 0
        },
        "topics": [],
        "posting_frequency": {}
    }

    for item in content:
        # Count by platform
        platform = item.get("platform", "Unknown")
        analysis["by_platform"][platform] = analysis["by_platform"].get(platform, 0) + 1

        # Count by competitor
        competitor = item.get("competitor_name", item.get("handle", "Unknown"))
        if competitor not in analysis["by_competitor"]:
            analysis["by_competitor"][competitor] = {"count": 0, "total_engagement": 0}
        analysis["by_competitor"][competitor]["count"] += 1

        # Engagement
        engagement = (
            item.get("likes", 0) +
            item.get("retweets", 0) * 2 +
            item.get("replies", 0) * 3
        )
        analysis["by_competitor"][competitor]["total_engagement"] += engagement

        # Content formats (X only)
        if platform == "X":
            if item.get("has_video"):
                analysis["content_formats"]["with_video"] += 1
            elif item.get("has_image"):
                analysis["content_formats"]["with_image"] += 1
            elif item.get("has_link"):
                analysis["content_formats"]["with_link"] += 1
            else:
                analysis["content_formats"]["text_only"] += 1

    # Sort top performing
    x_content = [c for c in content if c.get("platform") == "X"]
    x_content.sort(key=lambda x: x.get("likes", 0) + x.get("retweets", 0) * 2, reverse=True)
    analysis["top_performing"] = x_content[:10]

    return analysis


def generate_report(competitors: list[dict], content: list[dict], analysis: dict) -> str:
    """Generate markdown analysis report"""
    report = f"""# Competitor Content Analysis Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Competitors Analyzed:** {len(competitors)}
**Content Items:** {analysis['total_items']}

---

## Summary by Competitor

| Competitor | Posts | Avg Engagement |
|------------|-------|----------------|
"""

    for name, data in analysis["by_competitor"].items():
        avg_eng = data["total_engagement"] / data["count"] if data["count"] > 0 else 0
        report += f"| {name} | {data['count']} | {avg_eng:.0f} |\n"

    report += """

---

## Content Format Analysis (X/Twitter)

| Format | Count | % of Total |
|--------|-------|------------|
"""

    total_x = sum(analysis["content_formats"].values())
    for format_type, count in analysis["content_formats"].items():
        pct = (count / total_x * 100) if total_x > 0 else 0
        report += f"| {format_type.replace('_', ' ').title()} | {count} | {pct:.1f}% |\n"

    report += """

---

## Top Performing Content

"""

    for i, item in enumerate(analysis["top_performing"][:5], 1):
        text_preview = item.get("text", "")[:150].replace("\n", " ")
        engagement = item.get("likes", 0) + item.get("retweets", 0) * 2
        report += f"""### {i}. {item.get('handle', 'Unknown')} ({engagement} engagement)

> {text_preview}...

- Likes: {item.get('likes', 0)}
- Retweets: {item.get('retweets', 0)}
- Replies: {item.get('replies', 0)}
- [View post]({item.get('url', '#')})

"""

    report += """---

## Actionable Insights

Based on the analysis:

1. **Content format trends:** See which formats get most engagement
2. **Posting frequency:** Compare output volume across competitors
3. **Topic patterns:** Identify themes that resonate
4. **Engagement benchmarks:** Set targets based on competitor performance

---

*Generated by PRINTMAXX Competitor Analyzer*
"""

    return report


async def run_analysis(
    competitors: list[dict],
    platform_filter: Optional[str],
    days_filter: int,
    headless: bool = True
) -> list[dict]:
    """Run the competitor analysis"""
    all_content = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await context.new_page()

        for i, competitor in enumerate(competitors):
            name = competitor["name"]
            print(f"\n[{i+1}/{len(competitors)}] Analyzing {name}...")

            # Scrape X if no platform filter or filter is 'x'
            if (not platform_filter or platform_filter.lower() == "x") and competitor.get("x_handle"):
                print(f"  Scraping X: {competitor['x_handle']}")
                x_content = await scrape_x_content(page, competitor["x_handle"])
                for item in x_content:
                    item["competitor_id"] = competitor["id"]
                    item["competitor_name"] = name
                all_content.extend(x_content)
                print(f"    Found {len(x_content)} tweets")

            # Scrape blog if no platform filter or filter is 'blog'
            if (not platform_filter or platform_filter.lower() == "blog") and competitor.get("blog_url"):
                print(f"  Scraping blog: {competitor['blog_url']}")
                blog_content = await scrape_blog_content(page, competitor["blog_url"])
                for item in blog_content:
                    item["competitor_id"] = competitor["id"]
                    item["competitor_name"] = name
                all_content.extend(blog_content)
                print(f"    Found {len(blog_content)} posts")

            # Rate limiting
            if i < len(competitors) - 1:
                await asyncio.sleep(2)

        await browser.close()

    # Filter by date if specified
    if days_filter > 0:
        cutoff = datetime.now() - timedelta(days=days_filter)
        filtered = []
        for item in all_content:
            timestamp = item.get("timestamp") or item.get("date")
            if timestamp:
                try:
                    item_date = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                    if item_date.replace(tzinfo=None) >= cutoff:
                        filtered.append(item)
                except:
                    filtered.append(item)  # Keep if can't parse date
            else:
                filtered.append(item)  # Keep if no date
        all_content = filtered

    return all_content


def save_content_csv(content: list[dict], output_file: Path):
    """Save scraped content to CSV"""
    if not content:
        return

    fieldnames = [
        "competitor_id", "competitor_name", "platform", "handle",
        "text", "url", "timestamp", "likes", "retweets", "replies",
        "has_image", "has_video", "has_link", "title", "excerpt"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(content)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze competitor content patterns"
    )
    parser.add_argument(
        "--competitor",
        type=str,
        help="Filter to specific competitor (partial name match)"
    )
    parser.add_argument(
        "--platform",
        choices=["x", "blog"],
        help="Filter to specific platform"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=0,
        help="Only content from last N days (0 = all)"
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Generate analysis report (uses Claude if available)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_CSV,
        help=f"Output CSV file (default: {OUTPUT_CSV})"
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=OUTPUT_REPORT,
        help=f"Output report file (default: {OUTPUT_REPORT})"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        default=True,
        help="Run browser in headless mode (default)"
    )
    parser.add_argument(
        "--show-browser",
        action="store_true",
        help="Show browser window"
    )

    args = parser.parse_args()
    headless = not args.show_browser

    print("=" * 60)
    print("COMPETITOR CONTENT ANALYZER")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Load competitors
    competitors = load_competitors(args.competitor)

    if not competitors:
        print("No competitors found")
        return

    print(f"\nCompetitors to analyze: {len(competitors)}")
    for c in competitors:
        print(f"  - {c['name']}")

    if args.platform:
        print(f"Platform filter: {args.platform}")
    if args.days > 0:
        print(f"Date filter: last {args.days} days")

    # Run analysis
    content = asyncio.run(run_analysis(
        competitors=competitors,
        platform_filter=args.platform,
        days_filter=args.days,
        headless=headless
    ))

    print(f"\n{'=' * 60}")
    print(f"Scraped {len(content)} content items")

    # Save CSV
    save_content_csv(content, args.output)
    print(f"Saved to: {args.output}")

    # Generate report if requested
    if args.analyze and content:
        analysis = analyze_content_patterns(content)
        report = generate_report(competitors, content, analysis)

        with open(args.report, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"Report saved to: {args.report}")

        # Print quick summary
        print(f"\n{'=' * 60}")
        print("QUICK SUMMARY")
        print("=" * 60)
        print(f"Total content items: {analysis['total_items']}")
        print("\nBy platform:")
        for platform, count in analysis["by_platform"].items():
            print(f"  {platform}: {count}")
        print("\nTop performer:")
        if analysis["top_performing"]:
            top = analysis["top_performing"][0]
            print(f"  {top.get('handle')} - {top.get('likes', 0)} likes")
            print(f"  {top.get('text', '')[:100]}...")

    print(f"\n{'=' * 60}")
    print("COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
