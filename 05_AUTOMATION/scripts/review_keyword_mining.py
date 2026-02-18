#!/usr/bin/env python3
"""
Review Keyword Mining Script

Scrapes competitor app reviews from App Store and Google Play,
extracts common phrases, and identifies keyword opportunities.

Usage:
    python review_keyword_mining.py --app "Hallow" --platform ios --limit 500
    python review_keyword_mining.py --app "Opal" --platform android --limit 500
    python review_keyword_mining.py --batch configs/competitor_apps.json

Output:
    - CSV file with extracted keywords and frequencies
    - Markdown report with keyword opportunities
"""

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Optional

# Try to import optional dependencies
try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.util import ngrams
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False


# Configuration
OUTPUT_DIR = Path(__file__).parent.parent / "MONEY_METHODS" / "APP_FACTORY" / "aso" / "keyword_research"
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "been",
    "be", "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "can", "need", "dare", "ought",
    "used", "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
    "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself",
    "she", "her", "hers", "herself", "it", "its", "itself", "they", "them",
    "their", "theirs", "themselves", "what", "which", "who", "whom", "this",
    "that", "these", "those", "am", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "having", "do", "does", "did", "doing",
    "would", "could", "should", "might", "must", "shall", "will", "can",
    "cannot", "won't", "don't", "doesn't", "didn't", "isn't", "aren't",
    "wasn't", "weren't", "hasn't", "haven't", "hadn't", "won't", "wouldn't",
    "couldn't", "shouldn't", "mightn't", "mustn't", "let's", "that's", "who's",
    "what's", "here's", "there's", "when's", "where's", "why's", "how's",
    "app", "apps", "very", "really", "just", "so", "too", "also", "only",
    "even", "still", "already", "always", "never", "ever", "yet", "well",
    "back", "now", "then", "here", "there", "where", "when", "how", "all",
    "each", "every", "both", "few", "more", "most", "other", "some", "such",
    "no", "nor", "not", "own", "same", "than", "too", "very", "just",
    "about", "above", "after", "again", "against", "all", "any", "because",
    "before", "below", "between", "both", "during", "each", "few", "further",
    "into", "more", "most", "off", "once", "only", "other", "out", "over",
    "same", "some", "such", "through", "under", "until", "up", "while",
    "use", "using", "used", "like", "get", "got", "getting", "make", "makes",
    "made", "making", "one", "two", "first", "new", "way", "thing", "things",
    "time", "times", "day", "days", "week", "month", "year", "much", "many",
    "great", "good", "best", "better", "love", "loved", "loves", "loving",
    "nice", "amazing", "awesome", "wonderful", "excellent", "fantastic",
    "recommend", "recommended", "recommends", "thanks", "thank", "please"
}


def clean_text(text: str) -> str:
    """Clean review text for analysis."""
    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)

    # Remove special characters but keep spaces
    text = re.sub(r'[^a-z\s]', ' ', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def extract_phrases(text: str, min_words: int = 2, max_words: int = 4) -> list:
    """Extract meaningful phrases from text."""
    words = text.split()

    # Filter out stop words for phrase extraction
    filtered_words = [w for w in words if w not in STOP_WORDS and len(w) > 2]

    phrases = []

    # Extract n-grams
    for n in range(min_words, max_words + 1):
        for i in range(len(filtered_words) - n + 1):
            phrase = ' '.join(filtered_words[i:i+n])
            phrases.append(phrase)

    return phrases


def extract_single_keywords(text: str) -> list:
    """Extract single keywords from text."""
    words = text.split()
    return [w for w in words if w not in STOP_WORDS and len(w) > 3]


def scrape_app_store_reviews(app_id: str, limit: int = 500) -> list:
    """
    Scrape reviews from Apple App Store.

    Note: This is a placeholder. In production, use:
    - App Store Connect API (official)
    - Sensortower/AppAnnie APIs (paid)
    - Manual collection for compliance
    """
    if not HAS_PLAYWRIGHT:
        print("Warning: Playwright not installed. Using sample data.")
        return get_sample_reviews("ios")

    reviews = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # App Store review page URL pattern
            url = f"https://apps.apple.com/us/app/id{app_id}#see-all/reviews"
            page.goto(url, wait_until="networkidle")

            # Wait for reviews to load
            page.wait_for_selector(".we-customer-review", timeout=10000)

            # Extract reviews
            review_elements = page.query_selector_all(".we-customer-review")

            for element in review_elements[:limit]:
                try:
                    title = element.query_selector(".we-customer-review__title")
                    body = element.query_selector(".we-customer-review__body")
                    rating = element.query_selector(".we-star-rating")

                    review_text = ""
                    if title:
                        review_text += title.inner_text() + " "
                    if body:
                        review_text += body.inner_text()

                    if review_text.strip():
                        reviews.append({
                            "text": review_text.strip(),
                            "rating": extract_rating(rating.get_attribute("aria-label") if rating else ""),
                            "source": "app_store"
                        })
                except Exception as e:
                    continue

            browser.close()

    except Exception as e:
        print(f"Error scraping App Store: {e}")
        print("Falling back to sample data...")
        return get_sample_reviews("ios")

    return reviews


def scrape_google_play_reviews(package_name: str, limit: int = 500) -> list:
    """
    Scrape reviews from Google Play Store.

    Note: This is a placeholder. In production, use:
    - Google Play Developer API (official)
    - Sensortower/AppAnnie APIs (paid)
    - Manual collection for compliance
    """
    if not HAS_PLAYWRIGHT:
        print("Warning: Playwright not installed. Using sample data.")
        return get_sample_reviews("android")

    reviews = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            url = f"https://play.google.com/store/apps/details?id={package_name}&hl=en_US"
            page.goto(url, wait_until="networkidle")

            # Click "See all reviews" if available
            try:
                see_all = page.query_selector('text="See all reviews"')
                if see_all:
                    see_all.click()
                    page.wait_for_load_state("networkidle")
            except:
                pass

            # Scroll to load more reviews
            for _ in range(10):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(1000)

            # Extract reviews
            review_elements = page.query_selector_all('[data-reviewid]')

            for element in review_elements[:limit]:
                try:
                    body = element.query_selector('.h3YV2d')
                    rating = element.query_selector('[role="img"]')

                    if body:
                        reviews.append({
                            "text": body.inner_text(),
                            "rating": extract_rating(rating.get_attribute("aria-label") if rating else ""),
                            "source": "google_play"
                        })
                except:
                    continue

            browser.close()

    except Exception as e:
        print(f"Error scraping Google Play: {e}")
        print("Falling back to sample data...")
        return get_sample_reviews("android")

    return reviews


def extract_rating(rating_text: str) -> int:
    """Extract numeric rating from text."""
    if not rating_text:
        return 0

    match = re.search(r'(\d)', rating_text)
    return int(match.group(1)) if match else 0


def get_sample_reviews(platform: str) -> list:
    """Return sample reviews for testing without scraping."""

    sample_reviews = {
        "ios": [
            {"text": "Love this prayer app! Helps me start my morning with faith instead of scrolling. The daily devotionals are perfect.", "rating": 5, "source": "sample"},
            {"text": "Great for building a prayer habit. The lock feature actually works and I pray more now.", "rating": 5, "source": "sample"},
            {"text": "Good concept but crashes sometimes. Wish it had more bible verses. Prayer timer is helpful.", "rating": 3, "source": "sample"},
            {"text": "This app changed my morning routine. No more doom scrolling, just prayer time.", "rating": 5, "source": "sample"},
            {"text": "Perfect for phone addiction recovery. Forces me to pray before I can use social media.", "rating": 5, "source": "sample"},
            {"text": "Decent app for christian focus. Could use more meditation features like Hallow.", "rating": 4, "source": "sample"},
            {"text": "Love the screen time blocking for faith. Finally an app that prioritizes prayer.", "rating": 5, "source": "sample"},
            {"text": "The accountability feature with my small group is amazing. We all pray together now.", "rating": 5, "source": "sample"},
            {"text": "Needs offline mode. Also wish it had audio prayers for when I'm driving.", "rating": 3, "source": "sample"},
            {"text": "Best christian app I've used. Simple and effective for daily devotion time.", "rating": 5, "source": "sample"},
            {"text": "Phone blocker works great but wish I could customize the unlock prayers more.", "rating": 4, "source": "sample"},
            {"text": "Started using this during Lent and now I can't stop. Great spiritual discipline tool.", "rating": 5, "source": "sample"},
            {"text": "My kids love it too. Great for the whole family to build prayer habits.", "rating": 5, "source": "sample"},
            {"text": "Would be 5 stars if it had a widget. Otherwise perfect morning prayer companion.", "rating": 4, "source": "sample"},
            {"text": "Finally broke my Instagram addiction with this. Prayer first, scroll later works!", "rating": 5, "source": "sample"},
        ],
        "android": [
            {"text": "Amazing step counter that actually motivates me to walk. Love that phone locks until I hit my goal.", "rating": 5, "source": "sample"},
            {"text": "Great fitness motivation app. The walk to unlock feature is genius for phone addiction.", "rating": 5, "source": "sample"},
            {"text": "Good concept but battery drain is an issue. Step counting seems accurate though.", "rating": 3, "source": "sample"},
            {"text": "Lost 10 pounds since using this! Having to walk before using phone really works.", "rating": 5, "source": "sample"},
            {"text": "Perfect for sedentary office workers like me. Forces me to take walking breaks.", "rating": 5, "source": "sample"},
            {"text": "Love the health gamification aspect. Way better than sweatcoin rewards system.", "rating": 4, "source": "sample"},
            {"text": "Screen time blocker plus fitness tracker in one. Exactly what I needed.", "rating": 5, "source": "sample"},
            {"text": "Wish it synced with my Fitbit. Otherwise great for morning walk motivation.", "rating": 4, "source": "sample"},
            {"text": "The daily step goal feature changed my life. Now I actually look forward to walking.", "rating": 5, "source": "sample"},
            {"text": "Better than Opal because it's positive reinforcement not just blocking.", "rating": 5, "source": "sample"},
            {"text": "Good for digital detox combined with fitness. Two birds one stone.", "rating": 5, "source": "sample"},
            {"text": "Pedometer accuracy could be better but the concept is solid.", "rating": 3, "source": "sample"},
            {"text": "My morning routine is so much better now. Walk the dog, earn my phone.", "rating": 5, "source": "sample"},
            {"text": "Great for anyone trying to reduce screen time and exercise more.", "rating": 5, "source": "sample"},
            {"text": "The health phone lock is perfect. Should have found this app sooner.", "rating": 5, "source": "sample"},
        ]
    }

    return sample_reviews.get(platform, sample_reviews["ios"])


def analyze_reviews(reviews: list) -> dict:
    """Analyze reviews and extract keywords and phrases."""

    all_text = ""
    positive_text = ""  # 4-5 star reviews
    negative_text = ""  # 1-3 star reviews

    for review in reviews:
        cleaned = clean_text(review["text"])
        all_text += cleaned + " "

        if review.get("rating", 0) >= 4:
            positive_text += cleaned + " "
        else:
            negative_text += cleaned + " "

    # Extract keywords and phrases
    all_keywords = extract_single_keywords(all_text)
    all_phrases = extract_phrases(all_text)
    positive_keywords = extract_single_keywords(positive_text)
    positive_phrases = extract_phrases(positive_text)
    negative_keywords = extract_single_keywords(negative_text)
    negative_phrases = extract_phrases(negative_text)

    # Count frequencies
    keyword_counts = Counter(all_keywords)
    phrase_counts = Counter(all_phrases)
    positive_keyword_counts = Counter(positive_keywords)
    positive_phrase_counts = Counter(positive_phrases)
    negative_keyword_counts = Counter(negative_keywords)
    negative_phrase_counts = Counter(negative_phrases)

    return {
        "total_reviews": len(reviews),
        "positive_reviews": sum(1 for r in reviews if r.get("rating", 0) >= 4),
        "negative_reviews": sum(1 for r in reviews if r.get("rating", 0) < 4),
        "top_keywords": keyword_counts.most_common(50),
        "top_phrases": phrase_counts.most_common(50),
        "positive_keywords": positive_keyword_counts.most_common(30),
        "positive_phrases": positive_phrase_counts.most_common(30),
        "negative_keywords": negative_keyword_counts.most_common(30),
        "negative_phrases": negative_phrase_counts.most_common(30),
    }


def generate_csv_report(app_name: str, analysis: dict, output_path: Path):
    """Generate CSV report with keyword data."""

    csv_path = output_path / f"{app_name.lower().replace(' ', '_')}_mined_keywords.csv"

    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["keyword_or_phrase", "frequency", "type", "sentiment", "priority"])

        # Write top keywords
        for keyword, count in analysis["top_keywords"]:
            sentiment = "positive" if keyword in dict(analysis["positive_keywords"]) else "neutral"
            priority = "high" if count >= 5 else "medium" if count >= 3 else "low"
            writer.writerow([keyword, count, "single", sentiment, priority])

        # Write top phrases
        for phrase, count in analysis["top_phrases"]:
            sentiment = "positive" if phrase in dict(analysis["positive_phrases"]) else "neutral"
            priority = "high" if count >= 3 else "medium" if count >= 2 else "low"
            writer.writerow([phrase, count, "phrase", sentiment, priority])

    print(f"CSV report saved to: {csv_path}")
    return csv_path


def generate_markdown_report(app_name: str, analysis: dict, output_path: Path):
    """Generate markdown report with keyword opportunities."""

    md_path = output_path / f"{app_name.lower().replace(' ', '_')}_keyword_opportunities.md"

    report = f"""# Keyword mining report: {app_name}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## Summary

- Total reviews analyzed: {analysis['total_reviews']}
- Positive reviews (4-5 stars): {analysis['positive_reviews']}
- Negative reviews (1-3 stars): {analysis['negative_reviews']}

---

## Top keywords (single words)

Keywords mentioned frequently across all reviews:

| Keyword | Frequency | Priority |
|---------|-----------|----------|
"""

    for keyword, count in analysis["top_keywords"][:25]:
        priority = "High" if count >= 5 else "Medium" if count >= 3 else "Low"
        report += f"| {keyword} | {count} | {priority} |\n"

    report += """
---

## Top phrases (2-4 words)

Meaningful phrases that appear in reviews:

| Phrase | Frequency | Priority |
|--------|-----------|----------|
"""

    for phrase, count in analysis["top_phrases"][:25]:
        priority = "High" if count >= 3 else "Medium" if count >= 2 else "Low"
        report += f"| {phrase} | {count} | {priority} |\n"

    report += """
---

## Positive sentiment keywords

Keywords from 4-5 star reviews (what users love):

| Keyword | Frequency |
|---------|-----------|
"""

    for keyword, count in analysis["positive_keywords"][:15]:
        report += f"| {keyword} | {count} |\n"

    report += """
---

## Negative sentiment keywords

Keywords from 1-3 star reviews (pain points and opportunities):

| Keyword | Frequency |
|---------|-----------|
"""

    for keyword, count in analysis["negative_keywords"][:15]:
        report += f"| {keyword} | {count} |\n"

    report += """
---

## Recommended actions

### High-priority keywords to target

Based on frequency and sentiment, prioritize these in your ASO:

"""

    high_priority = [k for k, c in analysis["top_keywords"][:10] if c >= 3]
    for kw in high_priority[:5]:
        report += f"1. **{kw}** - Add to keyword field, include in description\n"

    report += """
### Feature opportunities

From negative reviews, users want:

"""

    for phrase, count in analysis["negative_phrases"][:5]:
        report += f"- {phrase} (mentioned {count}x)\n"

    report += """
---

## Integration with ASO tracking

Add these keywords to ASO_TRACKING.csv for monitoring:

```csv
"""

    for keyword, count in analysis["top_keywords"][:10]:
        report += f"appname,{keyword},{datetime.now().strftime('%Y-%m-%d')},0,0,mined from competitor reviews\n"

    report += """```

---

Last updated: """ + datetime.now().strftime('%Y-%m-%d')

    with open(md_path, 'w') as f:
        f.write(report)

    print(f"Markdown report saved to: {md_path}")
    return md_path


def main():
    parser = argparse.ArgumentParser(description="Mine keywords from competitor app reviews")
    parser.add_argument("--app", type=str, help="App name or ID to analyze")
    parser.add_argument("--platform", type=str, choices=["ios", "android"], default="ios")
    parser.add_argument("--limit", type=int, default=500, help="Maximum reviews to scrape")
    parser.add_argument("--batch", type=str, help="Path to JSON config for batch processing")
    parser.add_argument("--output", type=str, help="Output directory (default: aso/keyword_research)")
    parser.add_argument("--sample", action="store_true", help="Use sample data instead of scraping")

    args = parser.parse_args()

    # Set output directory
    output_path = Path(args.output) if args.output else OUTPUT_DIR
    output_path.mkdir(parents=True, exist_ok=True)

    if args.batch:
        # Batch processing mode
        with open(args.batch) as f:
            config = json.load(f)

        for app_config in config.get("apps", []):
            print(f"\nProcessing: {app_config['name']}")

            if args.sample:
                reviews = get_sample_reviews(app_config.get("platform", "ios"))
            elif app_config.get("platform") == "ios":
                reviews = scrape_app_store_reviews(app_config["app_id"], args.limit)
            else:
                reviews = scrape_google_play_reviews(app_config["package_name"], args.limit)

            analysis = analyze_reviews(reviews)
            generate_csv_report(app_config["name"], analysis, output_path)
            generate_markdown_report(app_config["name"], analysis, output_path)

    elif args.app:
        # Single app mode
        print(f"Analyzing: {args.app}")

        if args.sample:
            reviews = get_sample_reviews(args.platform)
        elif args.platform == "ios":
            reviews = scrape_app_store_reviews(args.app, args.limit)
        else:
            reviews = scrape_google_play_reviews(args.app, args.limit)

        analysis = analyze_reviews(reviews)
        generate_csv_report(args.app, analysis, output_path)
        generate_markdown_report(args.app, analysis, output_path)

        # Print summary
        print(f"\n{'='*50}")
        print(f"Analysis complete for: {args.app}")
        print(f"Reviews analyzed: {analysis['total_reviews']}")
        print(f"\nTop 10 keywords:")
        for keyword, count in analysis["top_keywords"][:10]:
            print(f"  - {keyword}: {count}")
        print(f"\nTop 5 phrases:")
        for phrase, count in analysis["top_phrases"][:5]:
            print(f"  - {phrase}: {count}")

    else:
        # Demo mode with sample data
        print("Running demo with sample data...")
        print("Use --app 'AppName' --platform ios/android for real analysis")
        print("Use --sample flag to test with sample data")

        for platform in ["ios", "android"]:
            reviews = get_sample_reviews(platform)
            analysis = analyze_reviews(reviews)

            app_name = f"Sample_{platform.upper()}"
            generate_csv_report(app_name, analysis, output_path)
            generate_markdown_report(app_name, analysis, output_path)

            print(f"\n{platform.upper()} Sample Analysis:")
            print(f"  Top keywords: {[k for k, c in analysis['top_keywords'][:5]]}")


if __name__ == "__main__":
    main()
