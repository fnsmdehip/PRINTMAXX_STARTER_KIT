#!/usr/bin/env python3
"""
Analyze Deep Bookmark Exports

Processes the deep bookmark JSON from deep_bookmark_scraper.js and:
1. Extracts actionable alpha to ALPHA_STAGING.csv
2. Saves profile analysis to PROFILE_ANALYSIS.csv
3. Organizes images for repurposing
4. Identifies funnel patterns (what products pair with what content)

Usage:
    python3 analyze_deep_bookmarks.py x_bookmarks_deep_2026-01-22.json
    python3 analyze_deep_bookmarks.py --latest
"""

import json
import sys
import argparse
import logging
import csv
import re
from datetime import datetime
from pathlib import Path
from typing import Optional
from collections import Counter

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('deep_bookmark_analyzer')

# Paths
BOOKMARKS_DIR = Path(__file__).parent
LEDGER_DIR = Path(__file__).parent.parent.parent / 'LEDGER'
ALPHA_STAGING = LEDGER_DIR / 'ALPHA_STAGING.csv'
PROFILE_ANALYSIS = LEDGER_DIR / 'PROFILE_ANALYSIS.csv'
CONTENT_ASSETS = LEDGER_DIR / 'CONTENT_ASSETS.csv'
FUNNEL_PATTERNS = LEDGER_DIR / 'FUNNEL_PATTERNS.csv'


# =============================================================================
# FUNNEL DETECTION
# =============================================================================
# Keywords that indicate a post is funneling to a product/service

PRODUCT_FUNNEL_SIGNALS = [
    # Direct sales
    'link in bio', 'check link', 'grab it', 'get it here', 'available now',
    'launching', 'just dropped', 'now live', 'pre-order', 'buy now',

    # Lead magnets
    'free guide', 'free template', 'free course', 'download', 'get access',
    'sign up', 'join waitlist', 'newsletter', 'subscribe',

    # Service offers
    'dm me', 'book a call', 'schedule', 'consulting', 'agency',
    'we help', 'i help', 'work with me', 'hire me', 'open for',

    # Course/info product
    'cohort', 'course', 'masterclass', 'workshop', 'community',
    'membership', 'program', 'mentorship',

    # SaaS
    'try it free', 'free trial', 'beta access', 'early access',
    'launching soon', 'coming soon'
]

SERVICE_CATEGORIES = {
    'saas': ['saas', 'app', 'tool', 'software', 'platform', 'dashboard'],
    'course': ['course', 'cohort', 'masterclass', 'workshop', 'training'],
    'template': ['template', 'notion', 'airtable', 'figma', 'spreadsheet'],
    'agency': ['agency', 'done for you', 'we handle', 'full service'],
    'consulting': ['consulting', 'coaching', 'mentorship', '1:1', 'call'],
    'newsletter': ['newsletter', 'subscribe', 'weekly', 'daily email'],
    'community': ['community', 'discord', 'slack', 'membership', 'circle'],
    'ebook': ['ebook', 'guide', 'pdf', 'playbook', 'blueprint']
}


def detect_funnel(text: str) -> dict:
    """
    Detect if a post is funneling to a product/service.
    Returns funnel type and confidence.
    """
    text_lower = text.lower()

    signals_found = []
    for signal in PRODUCT_FUNNEL_SIGNALS:
        if signal in text_lower:
            signals_found.append(signal)

    if not signals_found:
        return {'is_funnel': False, 'confidence': 0, 'signals': [], 'category': None}

    # Determine category
    category = None
    for cat, keywords in SERVICE_CATEGORIES.items():
        for kw in keywords:
            if kw in text_lower:
                category = cat
                break
        if category:
            break

    confidence = min(len(signals_found) / 3, 1.0)  # Max confidence at 3+ signals

    return {
        'is_funnel': True,
        'confidence': confidence,
        'signals': signals_found,
        'category': category or 'unknown'
    }


def extract_bio_link(text: str) -> Optional[str]:
    """Extract URL mentioned in text."""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, text)
    # Filter out x.com/twitter URLs
    external_urls = [u for u in urls if 'x.com' not in u and 'twitter.com' not in u]
    return external_urls[0] if external_urls else None


def categorize_content(text: str) -> str:
    """Categorize content by topic."""
    text_lower = text.lower()

    categories = {
        'revenue_numbers': ['mrr', 'arr', '$', 'revenue', 'profit', 'k/mo'],
        'app_building': ['app store', 'ios', 'android', 'mobile app', 'shipped'],
        'growth_tactics': ['growth', 'viral', 'traffic', 'seo', 'followers'],
        'cold_outreach': ['cold email', 'outbound', 'leads', 'prospecting'],
        'content_creation': ['content', 'thread', 'newsletter', 'youtube'],
        'ai_tools': ['ai', 'gpt', 'claude', 'automation', 'cursor'],
        'saas': ['saas', 'subscription', 'churn', 'onboarding'],
        'indie_hacking': ['indie', 'solopreneur', 'bootstrap', 'side project']
    }

    for category, keywords in categories.items():
        for kw in keywords:
            if kw in text_lower:
                return category

    return 'general'


def find_latest_deep_file() -> Optional[Path]:
    """Find the most recent deep bookmark JSON file."""
    files = list(BOOKMARKS_DIR.glob('x_bookmarks_deep_*.json'))
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_mtime)


def load_deep_bookmarks(file_path: Path) -> dict:
    """Load deep bookmark JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return {}


def save_profile_analysis(profiles: list):
    """Save profile analysis to CSV."""
    if not profiles:
        return

    # Create file with headers if doesn't exist
    file_exists = PROFILE_ANALYSIS.exists()

    with open(PROFILE_ANALYSIS, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                'handle', 'profile_url', 'sample_post_url', 'content_category',
                'sample_content', 'bio', 'bio_link', 'banner_url', 'profile_pic_url',
                'follower_count', 'analyzed_date', 'notes'
            ])

        for profile in profiles:
            writer.writerow([
                profile.get('handle', ''),
                profile.get('profileUrl', ''),
                profile.get('samplePostUrl', ''),
                profile.get('contentCategory', ''),
                profile.get('sampleContent', '')[:200],
                profile.get('bio', ''),
                profile.get('bioLink', ''),
                profile.get('bannerUrl', ''),
                profile.get('profilePicUrl', ''),
                profile.get('followerCount', ''),
                datetime.now().strftime('%Y-%m-%d'),
                'Needs deep scrape' if profile.get('needsDeepScrape') else ''
            ])

    logger.info(f"Saved {len(profiles)} profiles to {PROFILE_ANALYSIS}")


def save_content_assets(images: list):
    """Save image assets for repurposing."""
    if not images:
        return

    file_exists = CONTENT_ASSETS.exists()

    with open(CONTENT_ASSETS, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                'asset_id', 'asset_type', 'url', 'source_post', 'author',
                'caption', 'category', 'repurpose_ideas', 'collected_date'
            ])

        for i, img in enumerate(images):
            asset_id = f"IMG{datetime.now().strftime('%Y%m%d')}{i:03d}"
            writer.writerow([
                asset_id,
                'image',
                img.get('url', ''),
                img.get('postUrl', ''),
                img.get('author', ''),
                img.get('caption', '')[:200],
                img.get('category', ''),
                '',  # repurpose_ideas - to be filled manually
                datetime.now().strftime('%Y-%m-%d')
            ])

    logger.info(f"Saved {len(images)} image assets to {CONTENT_ASSETS}")


def save_funnel_patterns(funnels: list):
    """Save funnel pattern analysis."""
    if not funnels:
        return

    file_exists = FUNNEL_PATTERNS.exists()

    with open(FUNNEL_PATTERNS, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                'pattern_id', 'content_type', 'funnel_category', 'signals_used',
                'example_post', 'author', 'confidence', 'replication_notes', 'analyzed_date'
            ])

        for i, funnel in enumerate(funnels):
            pattern_id = f"FNL{datetime.now().strftime('%Y%m%d')}{i:03d}"
            writer.writerow([
                pattern_id,
                funnel.get('content_category', ''),
                funnel.get('funnel_category', ''),
                ', '.join(funnel.get('signals', [])),
                funnel.get('post_url', ''),
                funnel.get('author', ''),
                funnel.get('confidence', 0),
                '',  # replication_notes - to be filled
                datetime.now().strftime('%Y-%m-%d')
            ])

    logger.info(f"Saved {len(funnels)} funnel patterns to {FUNNEL_PATTERNS}")


def analyze_deep_bookmarks(file_path: Path):
    """Main analysis function."""
    data = load_deep_bookmarks(file_path)

    if not data:
        logger.error("No data to analyze")
        return

    metadata = data.get('metadata', {})
    bookmarks = data.get('bookmarks', [])
    profiles = data.get('profiles', [])
    images = data.get('imageAssets', [])

    logger.info(f"Loaded {len(bookmarks)} bookmarks, {len(profiles)} profiles, {len(images)} images")

    # Analyze funnels
    funnels = []
    funnel_categories = Counter()
    content_categories = Counter()

    for bookmark in bookmarks:
        text = bookmark.get('fullText', '')

        # Categorize content
        content_cat = categorize_content(text)
        content_categories[content_cat] += 1

        # Detect funnel
        funnel = detect_funnel(text)
        if funnel['is_funnel']:
            funnel_categories[funnel['category']] += 1
            funnels.append({
                'content_category': content_cat,
                'funnel_category': funnel['category'],
                'signals': funnel['signals'],
                'confidence': funnel['confidence'],
                'post_url': bookmark.get('url', ''),
                'author': bookmark.get('author', '')
            })

    # Save all data
    save_profile_analysis(profiles)
    save_content_assets(images)
    save_funnel_patterns(funnels)

    # Print summary
    print("\n" + "=" * 60)
    print("DEEP BOOKMARK ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"\nSource: {file_path.name}")
    print(f"Total bookmarks: {metadata.get('totalBookmarks', len(bookmarks))}")
    print(f"Business content: {metadata.get('businessContent', len(bookmarks))}")
    print(f"Unique profiles: {len(profiles)}")
    print(f"Images collected: {len(images)}")
    print(f"Funnel posts detected: {len(funnels)}")

    print("\n📊 CONTENT CATEGORIES:")
    for cat, count in content_categories.most_common(10):
        print(f"  {cat}: {count}")

    print("\n🎯 FUNNEL TYPES (what products pair with content):")
    for cat, count in funnel_categories.most_common(10):
        print(f"  {cat}: {count}")

    print("\n📁 FILES CREATED:")
    print(f"  • {PROFILE_ANALYSIS}")
    print(f"  • {CONTENT_ASSETS}")
    print(f"  • {FUNNEL_PATTERNS}")

    print("\n📋 NEXT STEPS:")
    print("  1. Review PROFILE_ANALYSIS.csv for bio copy inspiration")
    print("  2. Review CONTENT_ASSETS.csv for repurposable images")
    print("  3. Review FUNNEL_PATTERNS.csv to see what products pair with content types")
    print("  4. Run profile_scraper.py to get full profile data (bio, banner, etc.)")
    print("=" * 60)

    return data


def main():
    parser = argparse.ArgumentParser(description='Analyze deep bookmark exports')
    parser.add_argument('file', nargs='?', help='Path to deep bookmark JSON')
    parser.add_argument('--latest', action='store_true', help='Use most recent file')

    args = parser.parse_args()

    if args.latest:
        file_path = find_latest_deep_file()
        if not file_path:
            logger.error("No deep bookmark files found")
            return 1
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return 1
    else:
        file_path = find_latest_deep_file()
        if not file_path:
            parser.print_help()
            return 1

    logger.info(f"Analyzing: {file_path.name}")
    analyze_deep_bookmarks(file_path)
    return 0


if __name__ == '__main__':
    sys.exit(main())
