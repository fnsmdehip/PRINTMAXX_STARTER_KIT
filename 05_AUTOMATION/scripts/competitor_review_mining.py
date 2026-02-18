#!/usr/bin/env python3
"""
Competitor Review Mining Script

Scrapes app store reviews for competitor apps, extracts insights,
and generates opportunity reports.

Usage:
    python competitor_review_mining.py --niche faith
    python competitor_review_mining.py --niche all --output report.md
    python competitor_review_mining.py --app "Hallow" --count 500

Dependencies:
    pip install playwright pandas openai python-dotenv
"""

import argparse
import asyncio
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Warning: Playwright not installed. Install with: pip install playwright")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: Pandas not installed. Install with: pip install pandas")

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI not installed. Install with: pip install openai")

from dotenv import load_dotenv

load_dotenv()

# Configuration
BASE_DIR = Path(__file__).parent.parent
COMPETITIVE_DIR = BASE_DIR / "MONEY_METHODS" / "APP_FACTORY" / "competitive"
OUTPUT_DIR = COMPETITIVE_DIR / "review_reports"

# Competitor app IDs (App Store)
COMPETITOR_APPS = {
    "faith": {
        "Hallow": {
            "ios_id": "1542800043",
            "android_id": "com.hallow.app",
            "category": "faith"
        },
        "Pray.com": {
            "ios_id": "1234567890",  # Replace with actual ID
            "android_id": "com.pray.app",
            "category": "faith"
        },
        "Abide": {
            "ios_id": "908866608",
            "android_id": "com.carpenterscodeco.abidev",
            "category": "faith"
        },
        "YouVersion": {
            "ios_id": "282935706",
            "android_id": "com.sirma.mobile.bible.android",
            "category": "faith"
        }
    },
    "fitness": {
        "Strava": {
            "ios_id": "426826309",
            "android_id": "com.strava",
            "category": "fitness"
        },
        "Nike Run Club": {
            "ios_id": "387771637",
            "android_id": "com.nike.plusgps",
            "category": "fitness"
        },
        "Fitbit": {
            "ios_id": "462638897",
            "android_id": "com.fitbit.FitbitMobile",
            "category": "fitness"
        },
        "MyFitnessPal": {
            "ios_id": "341232718",
            "android_id": "com.myfitnesspal.android",
            "category": "fitness"
        }
    },
    "productivity": {
        "Forest": {
            "ios_id": "866450515",
            "android_id": "cc.forestapp",
            "category": "productivity"
        },
        "Freedom": {
            "ios_id": "1269788228",
            "android_id": "to.freedom.android2",
            "category": "productivity"
        },
        "Opal": {
            "ios_id": "1497465230",
            "android_id": None,  # iOS only
            "category": "productivity"
        },
        "One Sec": {
            "ios_id": "1532875441",
            "android_id": None,  # iOS only
            "category": "productivity"
        }
    }
}

# Review sentiment keywords
COMPLAINT_KEYWORDS = [
    "crash", "bug", "broken", "expensive", "price", "subscription",
    "annoying", "notification", "spam", "battery", "slow", "confusing",
    "complicated", "useless", "waste", "disappointed", "frustrating",
    "removed", "worse", "downgrade", "paywall", "ads", "privacy"
]

REQUEST_KEYWORDS = [
    "wish", "please add", "would love", "need", "want", "should have",
    "missing", "feature request", "suggestion", "hope they add",
    "it would be nice", "can you add", "why doesn't", "where is"
]

PRAISE_KEYWORDS = [
    "love", "amazing", "best", "perfect", "excellent", "helpful",
    "changed my life", "recommend", "5 stars", "fantastic", "great",
    "simple", "easy", "intuitive", "beautiful", "peaceful"
]


class ReviewMiner:
    """Mines and analyzes competitor app reviews."""

    def __init__(self, output_dir: Path = OUTPUT_DIR):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.reviews = []
        self.client = None

        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            self.client = OpenAI()

    async def scrape_ios_reviews(
        self,
        app_name: str,
        app_id: str,
        count: int = 200,
        country: str = "us"
    ) -> list:
        """
        Scrape reviews from iOS App Store.

        Note: Apple's RSS feed provides limited reviews.
        For production, consider using App Store Connect API or third-party services.
        """
        if not PLAYWRIGHT_AVAILABLE:
            print(f"Skipping {app_name} - Playwright not available")
            return []

        reviews = []
        url = f"https://itunes.apple.com/{country}/rss/customerreviews/id={app_id}/sortBy=mostRecent/json"

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                await page.goto(url, timeout=30000)
                content = await page.content()

                # Extract JSON from page
                json_match = re.search(r'<pre[^>]*>(.*?)</pre>', content, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group(1))
                    entries = data.get("feed", {}).get("entry", [])

                    for entry in entries[:count]:
                        if isinstance(entry, dict) and "content" in entry:
                            review = {
                                "app": app_name,
                                "platform": "ios",
                                "title": entry.get("title", {}).get("label", ""),
                                "content": entry.get("content", {}).get("label", ""),
                                "rating": int(entry.get("im:rating", {}).get("label", 0)),
                                "author": entry.get("author", {}).get("name", {}).get("label", ""),
                                "date": entry.get("updated", {}).get("label", ""),
                                "version": entry.get("im:version", {}).get("label", "")
                            }
                            reviews.append(review)

                print(f"Scraped {len(reviews)} reviews for {app_name} (iOS)")

            except Exception as e:
                print(f"Error scraping {app_name}: {e}")

            await browser.close()

        return reviews

    async def scrape_android_reviews(
        self,
        app_name: str,
        package_id: str,
        count: int = 200
    ) -> list:
        """
        Scrape reviews from Google Play Store.

        Note: Google Play doesn't have a public API for reviews.
        For production, consider using google-play-scraper or third-party services.
        """
        if not PLAYWRIGHT_AVAILABLE:
            print(f"Skipping {app_name} - Playwright not available")
            return []

        reviews = []
        url = f"https://play.google.com/store/apps/details?id={package_id}&hl=en&gl=us"

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                await page.goto(url, timeout=30000)
                await page.wait_for_timeout(3000)  # Wait for dynamic content

                # Click "See all reviews" if available
                try:
                    see_all = await page.query_selector('text="See all reviews"')
                    if see_all:
                        await see_all.click()
                        await page.wait_for_timeout(2000)
                except:
                    pass

                # Scroll to load more reviews
                for _ in range(5):
                    await page.evaluate("window.scrollBy(0, 1000)")
                    await page.wait_for_timeout(1000)

                # Extract reviews
                review_elements = await page.query_selector_all('[data-review-id]')

                for elem in review_elements[:count]:
                    try:
                        content_elem = await elem.query_selector('.h3YV2d')
                        rating_elem = await elem.query_selector('[role="img"]')
                        author_elem = await elem.query_selector('.X43Kjb')
                        date_elem = await elem.query_selector('.bp9Aid')

                        content = await content_elem.inner_text() if content_elem else ""
                        rating_text = await rating_elem.get_attribute('aria-label') if rating_elem else ""
                        rating = int(re.search(r'(\d)', rating_text).group(1)) if rating_text else 0
                        author = await author_elem.inner_text() if author_elem else ""
                        date = await date_elem.inner_text() if date_elem else ""

                        review = {
                            "app": app_name,
                            "platform": "android",
                            "title": "",
                            "content": content,
                            "rating": rating,
                            "author": author,
                            "date": date,
                            "version": ""
                        }
                        reviews.append(review)
                    except:
                        continue

                print(f"Scraped {len(reviews)} reviews for {app_name} (Android)")

            except Exception as e:
                print(f"Error scraping {app_name} Android: {e}")

            await browser.close()

        return reviews

    def analyze_sentiment(self, reviews: list) -> dict:
        """Categorize reviews by sentiment and extract insights."""

        analysis = {
            "complaints": [],
            "feature_requests": [],
            "praise": [],
            "neutral": []
        }

        for review in reviews:
            content = (review.get("content", "") + " " + review.get("title", "")).lower()
            rating = review.get("rating", 3)

            # Check for complaints
            complaint_matches = [kw for kw in COMPLAINT_KEYWORDS if kw in content]
            if complaint_matches or rating <= 2:
                analysis["complaints"].append({
                    **review,
                    "matched_keywords": complaint_matches
                })
                continue

            # Check for feature requests
            request_matches = [kw for kw in REQUEST_KEYWORDS if kw in content]
            if request_matches:
                analysis["feature_requests"].append({
                    **review,
                    "matched_keywords": request_matches
                })
                continue

            # Check for praise
            praise_matches = [kw for kw in PRAISE_KEYWORDS if kw in content]
            if praise_matches or rating >= 4:
                analysis["praise"].append({
                    **review,
                    "matched_keywords": praise_matches
                })
                continue

            analysis["neutral"].append(review)

        return analysis

    def extract_themes(self, reviews: list) -> dict:
        """Extract common themes from reviews."""

        themes = {
            "pricing": [],
            "bugs_crashes": [],
            "ui_ux": [],
            "features": [],
            "content": [],
            "community": [],
            "notifications": [],
            "performance": []
        }

        theme_keywords = {
            "pricing": ["price", "expensive", "subscription", "pay", "cost", "money", "free", "premium"],
            "bugs_crashes": ["crash", "bug", "broken", "error", "fix", "glitch", "freeze"],
            "ui_ux": ["design", "interface", "confusing", "simple", "easy", "intuitive", "ugly", "beautiful"],
            "features": ["feature", "add", "missing", "need", "want", "wish", "option"],
            "content": ["content", "meditation", "prayer", "workout", "session", "audio", "video"],
            "community": ["friend", "social", "share", "community", "group", "partner"],
            "notifications": ["notification", "reminder", "alert", "push", "spam"],
            "performance": ["slow", "battery", "drain", "sync", "offline", "loading"]
        }

        for review in reviews:
            content = (review.get("content", "") + " " + review.get("title", "")).lower()

            for theme, keywords in theme_keywords.items():
                if any(kw in content for kw in keywords):
                    themes[theme].append(review)

        return themes

    def generate_insights_with_ai(self, reviews: list, app_name: str) -> str:
        """Use AI to generate deeper insights from reviews."""

        if not self.client:
            return "AI analysis not available (OpenAI not configured)"

        # Prepare sample reviews for analysis
        complaints = [r for r in reviews if r.get("rating", 3) <= 2][:20]
        requests = [r for r in reviews if any(kw in r.get("content", "").lower() for kw in REQUEST_KEYWORDS)][:20]

        prompt = f"""Analyze these app reviews for {app_name} and extract actionable insights.

COMPLAINTS (1-2 star reviews):
{json.dumps([{"rating": r["rating"], "content": r["content"][:300]} for r in complaints], indent=2)}

FEATURE REQUESTS:
{json.dumps([{"content": r["content"][:300]} for r in requests], indent=2)}

Provide:
1. Top 5 user pain points (specific, actionable)
2. Top 5 feature requests (specific features users want)
3. 3 market opportunities these reviews reveal
4. 3 messaging angles we could use to attract these users

Be specific and actionable. No generic advice."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Use cheaper model for analysis
                messages=[
                    {"role": "system", "content": "You are a product analyst extracting insights from app reviews."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI analysis error: {e}"

    def generate_report(self, app_name: str, reviews: list, analysis: dict, themes: dict) -> str:
        """Generate markdown report for a competitor."""

        report = f"""# {app_name} Review Analysis Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Total Reviews Analyzed:** {len(reviews)}
**Platform:** iOS + Android

---

## Summary Statistics

| Category | Count | Percentage |
|----------|-------|------------|
| Complaints (1-2 stars) | {len(analysis['complaints'])} | {len(analysis['complaints'])/len(reviews)*100:.1f}% |
| Feature Requests | {len(analysis['feature_requests'])} | {len(analysis['feature_requests'])/len(reviews)*100:.1f}% |
| Praise (4-5 stars) | {len(analysis['praise'])} | {len(analysis['praise'])/len(reviews)*100:.1f}% |
| Neutral | {len(analysis['neutral'])} | {len(analysis['neutral'])/len(reviews)*100:.1f}% |

---

## Theme Distribution

| Theme | Mentions |
|-------|----------|
| Pricing | {len(themes['pricing'])} |
| Bugs/Crashes | {len(themes['bugs_crashes'])} |
| UI/UX | {len(themes['ui_ux'])} |
| Features | {len(themes['features'])} |
| Content | {len(themes['content'])} |
| Community | {len(themes['community'])} |
| Notifications | {len(themes['notifications'])} |
| Performance | {len(themes['performance'])} |

---

## Top Complaints

"""
        # Add top complaints
        for i, complaint in enumerate(analysis['complaints'][:10], 1):
            content = complaint['content'][:200].replace('\n', ' ')
            report += f"{i}. **[{complaint['rating']} stars]** {content}...\n"
            if complaint.get('matched_keywords'):
                report += f"   *Keywords: {', '.join(complaint['matched_keywords'])}*\n"
            report += "\n"

        report += """
---

## Feature Requests

"""
        for i, request in enumerate(analysis['feature_requests'][:10], 1):
            content = request['content'][:200].replace('\n', ' ')
            report += f"{i}. {content}...\n\n"

        report += """
---

## What Users Love

"""
        for i, praise in enumerate(analysis['praise'][:10], 1):
            content = praise['content'][:200].replace('\n', ' ')
            report += f"{i}. **[{praise['rating']} stars]** {content}...\n\n"

        # Add AI insights if available
        ai_insights = self.generate_insights_with_ai(reviews, app_name)
        report += f"""
---

## AI-Generated Insights

{ai_insights}

---

## Opportunities for Us

Based on this analysis, here are opportunities to differentiate:

1. **Pricing:** If complaints mention price, position as more affordable
2. **Simplicity:** If UI complaints exist, emphasize our simple design
3. **Missing Features:** Build what they're asking for
4. **Community:** If no community features, add accountability
5. **Performance:** If performance issues, emphasize reliability

---

*Report generated by competitor_review_mining.py*
"""

        return report

    async def mine_competitor(
        self,
        app_name: str,
        ios_id: Optional[str],
        android_id: Optional[str],
        count: int = 200
    ) -> dict:
        """Mine reviews for a single competitor."""

        all_reviews = []

        if ios_id:
            ios_reviews = await self.scrape_ios_reviews(app_name, ios_id, count)
            all_reviews.extend(ios_reviews)

        if android_id:
            android_reviews = await self.scrape_android_reviews(app_name, android_id, count)
            all_reviews.extend(android_reviews)

        if not all_reviews:
            print(f"No reviews found for {app_name}")
            return {"app": app_name, "reviews": [], "analysis": {}, "themes": {}}

        analysis = self.analyze_sentiment(all_reviews)
        themes = self.extract_themes(all_reviews)

        # Generate and save report
        report = self.generate_report(app_name, all_reviews, analysis, themes)
        report_path = self.output_dir / f"{app_name.lower().replace(' ', '_')}_review_report.md"
        report_path.write_text(report)
        print(f"Report saved to: {report_path}")

        return {
            "app": app_name,
            "reviews": all_reviews,
            "analysis": analysis,
            "themes": themes,
            "report_path": str(report_path)
        }

    async def mine_niche(self, niche: str, count: int = 200) -> list:
        """Mine reviews for all competitors in a niche."""

        if niche not in COMPETITOR_APPS:
            print(f"Unknown niche: {niche}")
            return []

        results = []
        for app_name, app_info in COMPETITOR_APPS[niche].items():
            result = await self.mine_competitor(
                app_name,
                app_info.get("ios_id"),
                app_info.get("android_id"),
                count
            )
            results.append(result)

        return results

    async def mine_all(self, count: int = 100) -> dict:
        """Mine reviews for all competitors across all niches."""

        all_results = {}
        for niche in COMPETITOR_APPS.keys():
            print(f"\n{'='*50}")
            print(f"Mining {niche.upper()} niche...")
            print('='*50)
            all_results[niche] = await self.mine_niche(niche, count)

        # Generate summary report
        self.generate_summary_report(all_results)

        return all_results

    def generate_summary_report(self, all_results: dict) -> None:
        """Generate a summary report across all niches."""

        report = f"""# Competitor Review Mining Summary

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## Overview

"""

        for niche, results in all_results.items():
            report += f"### {niche.title()} Niche\n\n"

            for result in results:
                app = result["app"]
                review_count = len(result["reviews"])
                complaints = len(result.get("analysis", {}).get("complaints", []))

                if review_count > 0:
                    complaint_pct = complaints / review_count * 100
                    report += f"- **{app}:** {review_count} reviews, {complaint_pct:.1f}% complaints\n"
                else:
                    report += f"- **{app}:** No reviews scraped\n"

            report += "\n"

        report += """
---

## Cross-Niche Patterns

### Common Complaints Across All Apps
1. Subscription fatigue / pricing concerns
2. Feature changes after updates
3. Notification spam
4. Sync/performance issues
5. Paywalls blocking core features

### Universal Feature Requests
1. Better offline support
2. Family/sharing features
3. Simpler interfaces
4. More customization
5. Accountability/social features

### Our Differentiation Opportunities
1. Lower price point ($29 vs $50-100)
2. Simplicity as a feature
3. Built-in accountability (no one does this well)
4. Cross-platform parity from day one
5. Privacy-respecting approach

---

## Action Items

- [ ] Review individual app reports for specific opportunities
- [ ] Update feature roadmap based on requests
- [ ] Refine positioning based on competitor weaknesses
- [ ] Create marketing content addressing pain points
- [ ] Schedule next review mining (monthly)

---

*Generated by competitor_review_mining.py*
"""

        summary_path = self.output_dir / "REVIEW_MINING_SUMMARY.md"
        summary_path.write_text(report)
        print(f"\nSummary report saved to: {summary_path}")


async def main():
    parser = argparse.ArgumentParser(description="Mine competitor app reviews")
    parser.add_argument("--niche", choices=["faith", "fitness", "productivity", "all"],
                       default="all", help="Niche to analyze")
    parser.add_argument("--app", type=str, help="Specific app name to analyze")
    parser.add_argument("--count", type=int, default=200, help="Number of reviews per app")
    parser.add_argument("--output", type=str, help="Custom output file path")

    args = parser.parse_args()

    miner = ReviewMiner()

    if args.app:
        # Find the app in our configuration
        for niche, apps in COMPETITOR_APPS.items():
            if args.app in apps:
                app_info = apps[args.app]
                await miner.mine_competitor(
                    args.app,
                    app_info.get("ios_id"),
                    app_info.get("android_id"),
                    args.count
                )
                return
        print(f"App '{args.app}' not found in configuration")
        return

    if args.niche == "all":
        await miner.mine_all(args.count)
    else:
        await miner.mine_niche(args.niche, args.count)


if __name__ == "__main__":
    asyncio.run(main())
