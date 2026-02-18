#!/usr/bin/env python3
"""
Analyzes X bookmarks and fetches full content from external article links.
Usage: python3 analyze_and_fetch_articles.py <bookmarks.json>
"""

import sys
import json
import csv
import re
import requests
from datetime import datetime
from collections import defaultdict
from pathlib import Path
from bs4 import BeautifulSoup
import time

# Skip patterns
SKIP_PATTERNS = [
    r'\bmeme\b', r'\blol\b', r'\blmao\b', r'just vibing', r'\bmood\b',
    r'political take', r'hot take', r'unpopular opinion',
    r'\bratio\b', r'\bbased\b', r'\bcringe\b',
    r'selfie', r'ootd', r'fit check', r'🔥', r'vibes only'
]

# Focus categories
CATEGORIES = {
    'ai_automation': ['ai', 'llm', 'gpt', 'claude', 'chatgpt', 'automation', 'agent', 'prompt', 'rag'],
    'dev_tools': ['coding', 'developer', 'github', 'vscode', 'cursor', 'api', 'python', 'javascript'],
    'productivity': ['workflow', 'productivity', 'efficiency', 'optimization', 'habit', 'system', 'process'],
    'business': ['business', 'startup', 'revenue', 'profit', 'growth', 'scale', 'customer', 'mvp'],
    'marketing': ['marketing', 'seo', 'traffic', 'conversion', 'funnel', 'landing page', 'email'],
    'social_media': ['twitter', 'tiktok', 'instagram', 'youtube', 'viral', 'engagement', 'algorithm'],
    'monetization': ['affiliate', 'monetize', 'income', 'earn', 'passive', 'saas', 'subscription'],
    'solopreneur': ['solopreneur', 'indie hacker', 'bootstrapped', 'solo founder', 'side hustle']
}

def should_skip(text):
    """Check if bookmark should be skipped"""
    text_lower = text.lower()

    # Skip short posts
    if len(text.split()) < 8:
        return True

    # Skip if matches patterns
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, text_lower):
            return True

    return False

def categorize(text):
    """Categorize bookmark"""
    text_lower = text.lower()
    categories = []

    for cat, keywords in CATEGORIES.items():
        if any(kw in text_lower for kw in keywords):
            categories.append(cat)

    return categories if categories else ['general']

def extract_insights(text):
    """Extract insight types"""
    insights = []

    if re.search(r'(tip|hack|trick|secret):', text, re.I):
        insights.append('contains_tip')

    if re.search(r'(use|try|check out|recommend)', text, re.I):
        insights.append('tool_recommendation')

    if re.search(r'\d+[%xX]|\$\d+|[\d,]+\s*(views|followers|revenue|users)', text):
        insights.append('has_metrics')

    if re.search(r'how\s+to|step\s+\d+|here\'s how', text, re.I):
        insights.append('how_to_guide')

    if re.search(r'(framework|system|process|method|strategy|playbook)', text, re.I):
        insights.append('framework_strategy')

    return insights

def fetch_article_content(url, timeout=10):
    """Fetch and extract article content"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script in soup(['script', 'style', 'nav', 'footer', 'header']):
            script.decompose()

        # Try common article selectors
        article = None
        selectors = [
            'article',
            '[role="article"]',
            '.article-content',
            '.post-content',
            'main',
            '.entry-content'
        ]

        for selector in selectors:
            article = soup.select_one(selector)
            if article:
                break

        if not article:
            article = soup.find('body')

        if article:
            text = article.get_text(separator='\n', strip=True)
            # Clean up
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            clean_text = '\n'.join(lines)

            # Get title
            title = soup.find('title')
            title_text = title.get_text() if title else ''

            return {
                'title': title_text,
                'content': clean_text[:5000],  # Limit to 5000 chars
                'word_count': len(clean_text.split()),
                'success': True
            }

    except Exception as e:
        return {
            'error': str(e),
            'success': False
        }

    return {'success': False}

def analyze_bookmarks(json_file, fetch_articles=True):
    """Main analysis function"""

    print(f"📂 Loading: {json_file}\n")

    with open(json_file, 'r', encoding='utf-8') as f:
        bookmarks = json.load(f)

    print(f"📊 Total bookmarks: {len(bookmarks)}\n")

    # Filter and analyze
    filtered = []
    category_counts = defaultdict(int)
    articles_to_fetch = []

    print("🔍 Filtering and categorizing...\n")

    for i, bm in enumerate(bookmarks):
        text = bm.get('text', '')

        if should_skip(text):
            continue

        # Categorize
        categories = categorize(text)
        for cat in categories:
            category_counts[cat] += 1

        # Extract insights
        insights = extract_insights(text)

        # Check for external link
        external_link = bm.get('external_link', '')

        result = {
            **bm,
            'categories': ','.join(categories),
            'insights': ','.join(insights),
            'analyzed_at': datetime.now().isoformat()
        }

        filtered.append(result)

        # Queue article fetch if has external link
        if external_link and fetch_articles:
            articles_to_fetch.append((i, external_link, result))

        if (i + 1) % 50 == 0:
            print(f"   Processed {i + 1}/{len(bookmarks)}...")

    print(f"\n✅ Filtered to {len(filtered)} actionable bookmarks\n")

    # Category breakdown
    print("📈 Category Breakdown:")
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {cat}: {count}")

    # Fetch article content
    if fetch_articles and articles_to_fetch:
        print(f"\n🌐 Fetching {len(articles_to_fetch)} external articles...")
        print("   (This may take a while...)\n")

        for idx, (i, url, bm) in enumerate(articles_to_fetch[:50]):  # Limit to 50
            print(f"   [{idx+1}/{min(len(articles_to_fetch), 50)}] Fetching: {url[:60]}...")

            content = fetch_article_content(url)

            if content['success']:
                bm['article_title'] = content.get('title', '')
                bm['article_content'] = content.get('content', '')
                bm['article_word_count'] = content.get('word_count', 0)
                print(f"       ✅ Got {content.get('word_count', 0)} words")
            else:
                print(f"       ❌ Failed: {content.get('error', 'Unknown')}")

            time.sleep(1)  # Rate limit

    # Save results
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    base = Path('/Users/macbookpro/Downloads/PRINTMAXX_STARTER_KIT/AUTOMATIONS/x_bookmarks')

    # Save filtered JSON
    output_json = base / f'analyzed_{ts}.json'
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(filtered, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Saved: {output_json}")

    # Save CSV
    output_csv = base / f'analyzed_{ts}.csv'
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        if filtered:
            # Get all unique keys
            all_keys = set()
            for bm in filtered:
                all_keys.update(bm.keys())

            writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
            writer.writeheader()
            writer.writerows(filtered)
    print(f"💾 Saved: {output_csv}")

    # Generate insights summary
    print("\n🎯 Quick Insights:")

    all_insights = []
    for bm in filtered:
        all_insights.extend(bm.get('insights', '').split(','))

    insight_counts = defaultdict(int)
    for insight in all_insights:
        if insight:
            insight_counts[insight] += 1

    for insight, count in sorted(insight_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   {insight}: {count}")

    # Articles with content
    with_articles = len([b for b in filtered if b.get('article_content')])
    if with_articles:
        print(f"\n📄 Successfully fetched {with_articles} article contents")

    return filtered, output_json

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_and_fetch_articles.py <bookmarks.json>")
        print("\nLooking for JSON files...")

        import glob
        json_files = glob.glob('/Users/macbookpro/Downloads/PRINTMAXX_STARTER_KIT/AUTOMATIONS/x_bookmarks/*.json')

        if json_files:
            print(f"Found {len(json_files)} file(s):")
            for f in sorted(json_files)[-5:]:
                print(f"  - {Path(f).name}")

            latest = max(json_files, key=lambda x: Path(x).stat().st_mtime)
            print(f"\nUsing most recent: {Path(latest).name}")
            analyze_bookmarks(latest)
        else:
            print("No JSON files found.")
            sys.exit(1)
    else:
        analyze_bookmarks(sys.argv[1])
