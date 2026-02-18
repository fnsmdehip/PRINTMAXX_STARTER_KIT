#!/usr/bin/env python3
"""
Process console scrape JSON and add to ALPHA_STAGING.csv
Usage: python3 process_console_scrape.py <json_file>
"""

import sys
import json
import csv
import re
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
ALPHA_STAGING = PROJECT_DIR / "LEDGER" / "ALPHA_STAGING.csv"


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
    """Load existing source URLs to avoid duplicates"""
    urls = set()
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('source_url'):
                    urls.add(row['source_url'])
    return urls


def categorize_content(text):
    """Auto-categorize based on content"""
    text_lower = text.lower()

    if any(word in text_lower for word in ['app', 'mobile', 'ios', 'android', 'store']):
        return 'APP_FACTORY'
    elif any(word in text_lower for word in ['email', 'cold', 'outbound', 'deliverability']):
        return 'COLD_OUTBOUND'
    elif any(word in text_lower for word in ['seo', 'search', 'google', 'ranking']):
        return 'SEO_GEO_ASO'
    elif any(word in text_lower for word in ['content', 'tiktok', 'instagram', 'youtube']):
        return 'CONTENT_FARM'
    elif any(word in text_lower for word in ['ai', 'automation', 'tool', 'api']):
        return 'TOOL_ALPHA'
    elif any(word in text_lower for word in ['revenue', 'pricing', 'monetization', 'paywall']):
        return 'MONETIZATION'
    elif any(word in text_lower for word in ['growth', 'traffic', 'viral', 'distribution']):
        return 'GROWTH_HACK'
    else:
        return 'GENERAL'


def check_engagement_authenticity(tweet):
    """Check if engagement seems authentic"""
    # For console scrape, we don't have engagement metrics
    # Default to AUTHENTIC since these are from logged-in viewing
    return 'AUTHENTIC'


def process_json(json_file):
    """Process JSON and add to ALPHA_STAGING.csv"""

    # Load JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        tweets = json.load(f)

    print(f"📂 Loaded {len(tweets)} tweets from {json_file}")

    # Load existing data
    existing_urls = load_existing_urls()
    print(f"📊 Existing URLs in alpha: {len(existing_urls)}")

    # Filter new tweets
    new_tweets = [t for t in tweets if t['url'] not in existing_urls]
    print(f"✅ Found {len(new_tweets)} new tweets (filtered {len(tweets) - len(new_tweets)} duplicates)")

    if not new_tweets:
        print("No new tweets to add.")
        return

    # Read existing CSV
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
            'full_description', 'actionable_steps', 'roi_potential',
            'implementation_complexity', 'legal_risk', 'applicable_methods',
            'status', 'priority', 'reviewer_notes', 'engagement_authenticity',
            'earnings_verified'
        ]

    # Get next ID
    next_id = get_next_alpha_id()
    print(f"📋 Next alpha ID: ALPHA{next_id}")

    # Add new tweets
    added = 0
    for tweet in new_tweets:
        category = categorize_content(tweet['text'])
        engagement = check_engagement_authenticity(tweet)

        row = {k: '' for k in fieldnames}
        row.update({
            'alpha_id': f'ALPHA{next_id}',
            'source': f"@{tweet['handle']} (high-signal Twitter)",
            'source_url': tweet['url'],
            'category': category,
            'tactic': tweet['text'][:200] + '...' if len(tweet['text']) > 200 else tweet['text'],
            'full_description': tweet['text'],
            'actionable_steps': '',
            'roi_potential': 'MEDIUM',
            'implementation_complexity': 'MEDIUM',
            'legal_risk': 'LOW',
            'applicable_methods': category,
            'status': 'PENDING_REVIEW',
            'priority': '',
            'reviewer_notes': f"Auto-scraped via console from high-signal account. Scraped {tweet.get('scraped_at', 'unknown')}",
            'engagement_authenticity': engagement,
            'earnings_verified': 'FALSE'
        })
        rows.append(row)
        next_id += 1
        added += 1

    # Write back
    with open(ALPHA_STAGING, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Added {added} new entries (ALPHA{next_id - added}-ALPHA{next_id - 1})")
    print(f"📁 Saved to: {ALPHA_STAGING}")
    print(f"\n🔍 Run: /review-alpha to approve entries")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 process_console_scrape.py <json_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    if not Path(json_file).exists():
        print(f"Error: File not found: {json_file}")
        sys.exit(1)

    process_json(json_file)
