#!/usr/bin/env python3
"""
Extract Alpha from X/Twitter Bookmarks

Parses bookmarks JSON exported from browser and extracts actionable alpha
to ALPHA_STAGING.csv for review and integration.

Usage:
    python3 extract_alpha_from_bookmarks.py <bookmarks.json>
    python3 extract_alpha_from_bookmarks.py --latest
    python3 extract_alpha_from_bookmarks.py x_bookmarks_2026-01-22.json --dry-run

Workflow:
    1. Export bookmarks via browser console (see QUICK_START.md)
    2. Run this script to extract alpha
    3. Review ALPHA_STAGING.csv (status=PENDING_REVIEW)
    4. Approve/reject findings
"""

import json
import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from daily_research.twitter_scanner import TwitterScanner, Tweet
except ImportError:
    print("Error: Could not import TwitterScanner")
    print("Make sure daily_research/twitter_scanner.py exists")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('bookmark_alpha_extractor')

# Paths
BOOKMARKS_DIR = Path(__file__).parent
LEDGER_DIR = Path(__file__).parent.parent.parent / 'LEDGER'
ALPHA_STAGING = LEDGER_DIR / 'ALPHA_STAGING.csv'

# =============================================================================
# CONTENT FILTERING
# =============================================================================
# Note: User bookmarks contain diverse content for algorithm training (politics,
# memes, jokes, etc.) to avoid echo chambers. We ONLY want solopreneur/tech/
# business/finance alpha. Everything else gets filtered out.
# =============================================================================

# Keywords that indicate RELEVANT solopreneur/tech/business content (INCLUDE)
INCLUDE_KEYWORDS = [
    # Revenue and money
    'mrr', 'arr', 'revenue', 'profit', 'income', '$', 'k/mo', '/mo', 'k/month',
    'sold for', 'making', 'earned', 'revenue', 'monetize', 'monetization',

    # Building and launching
    'launched', 'shipped', 'built', 'building', 'launch', 'startup', 'saas',
    'side project', 'indie', 'solopreneur', 'founder', 'bootstrap', 'mvp',

    # Growth and marketing
    'growth hack', 'seo', 'traffic', 'conversions', 'subscribers', 'users',
    'customers', 'leads', 'outbound', 'cold email', 'funnel', 'landing page',

    # Tech and tools
    'api', 'automation', 'workflow', 'no-code', 'low-code', 'ai tool', 'gpt',
    'cursor', 'claude', 'vercel', 'supabase', 'stripe', 'revenueCat',

    # Apps and products
    'app store', 'play store', 'ios', 'android', 'mobile app', 'web app',
    'chrome extension', 'plugin', 'template', 'notion', 'airtable',

    # Business tactics
    'pricing', 'paywall', 'subscription', 'freemium', 'affiliate', 'sponsor',
    'newsletter', 'course', 'ebook', 'info product', 'digital product',

    # Metrics and data
    'case study', 'breakdown', 'thread', 'how i', 'step by step', 'playbook',
    'framework', 'strategy', 'tactic', 'hack', 'tip', 'lesson learned',
]

# Keywords that indicate IRRELEVANT content (EXCLUDE) - politics, memes, etc.
EXCLUDE_KEYWORDS = [
    # Politics (left, right, and general)
    'trump', 'biden', 'maga', 'democrat', 'republican', 'liberal', 'conservative',
    'left wing', 'right wing', 'woke', 'anti-woke', 'election', 'congress',
    'senate', 'government', 'politician', 'political', 'politics', 'policy',
    'immigration', 'border', 'abortion', 'gun control', 'climate change debate',
    'vaccine mandate', 'lockdown', 'mandate', 'blm', 'antifa', 'proud boys',

    # Culture war topics
    'cancel culture', 'cancelled', 'triggered', 'snowflake', 'sjw', 'wokeness',
    'gender identity', 'pronouns', 'trans rights', 'lgbtq debate', 'dei',
    'affirmative action', 'critical race', 'white privilege', 'systemic racism',

    # Memes and jokes (not business-related)
    'ratio', 'based', 'cope', 'seethe', 'mid', 'fr fr', 'no cap', 'bussin',
    'ong', 'its giving', 'slay', 'ate that', 'delulu', 'villain arc',
    'main character', 'roman empire', 'gaslight', 'gatekeep', 'girlboss',

    # Entertainment/celebrity gossip
    'kardashian', 'kanye', 'celebrity', 'hollywood', 'netflix drama', 'reality tv',
    'bachelor', 'housewives', 'influencer drama', 'tea', 'spill the tea',

    # Sports (unless business angle)
    'touchdown', 'home run', 'goal scored', 'championship', 'playoffs',
    'fantasy football', 'fantasy basketball', 'drafted', 'traded player',

    # Random viral content
    'cursed image', 'aita', 'tifu', 'eli5', 'unpopular opinion',
    'hot take', 'controversial take', 'conspiracy', 'flat earth',

    # News/current events (non-business)
    'breaking news', 'just in', 'alert', 'tragedy', 'disaster', 'shooting',
    'earthquake', 'hurricane', 'war', 'invasion', 'military',
]

def is_relevant_content(text: str) -> tuple[bool, str]:
    """
    Filter bookmark content to only include solopreneur/tech/business alpha.
    Returns (is_relevant, reason).

    User's bookmarks include diverse content to train the algorithm and avoid
    echo chambers. We filter to ONLY extract business/tech alpha.
    """
    text_lower = text.lower()

    # First check for exclude keywords (politics, memes, etc.)
    for keyword in EXCLUDE_KEYWORDS:
        if keyword in text_lower:
            return False, f"Excluded: contains '{keyword}' (non-business content)"

    # Then check if it has ANY include keywords (business/tech signals)
    has_relevant_keyword = False
    matched_keyword = None
    for keyword in INCLUDE_KEYWORDS:
        if keyword in text_lower:
            has_relevant_keyword = True
            matched_keyword = keyword
            break

    if not has_relevant_keyword:
        return False, "Excluded: no solopreneur/tech/business keywords detected"

    return True, f"Included: contains '{matched_keyword}'"


def find_latest_bookmark_file() -> Optional[Path]:
    """
    Find the most recent bookmark JSON file.
    """
    bookmark_files = list(BOOKMARKS_DIR.glob('x_bookmarks_*.json'))

    if not bookmark_files:
        return None

    # Sort by modification time, return newest
    latest = max(bookmark_files, key=lambda p: p.stat().st_mtime)
    return latest


def load_bookmarks(file_path: Path) -> list:
    """
    Load bookmarks from JSON file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Handle both list and dict formats
        if isinstance(data, list):
            bookmarks = data
        elif isinstance(data, dict) and 'bookmarks' in data:
            bookmarks = data['bookmarks']
        else:
            logger.error(f"Unexpected JSON format in {file_path}")
            return []

        logger.info(f"Loaded {len(bookmarks)} bookmarks from {file_path.name}")
        return bookmarks

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return []


def parse_bookmark_timestamp(timestamp_str: str) -> datetime:
    """
    Parse timestamp from bookmark JSON.
    """
    try:
        # Try ISO format first
        return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    except:
        try:
            # Try common formats
            for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
                try:
                    return datetime.strptime(timestamp_str, fmt)
                except:
                    continue
        except:
            pass

    # Default to now if parsing fails
    return datetime.now()


def extract_alpha_from_bookmarks(
    bookmarks_file: Path,
    dry_run: bool = False,
    min_length: int = 50
) -> list:
    """
    Extract actionable alpha from bookmarks and save to ALPHA_STAGING.csv

    Args:
        bookmarks_file: Path to bookmarks JSON file
        dry_run: Preview findings without saving
        min_length: Minimum tweet length to consider (filter out short posts)

    Returns:
        List of AlphaFinding objects
    """
    bookmarks = load_bookmarks(bookmarks_file)

    if not bookmarks:
        logger.warning("No bookmarks to process")
        return []

    scanner = TwitterScanner()
    findings = []
    filtered_count = 0
    filtered_reasons = {}

    logger.info("Analyzing bookmarks for alpha signals...")
    logger.info("Note: Filtering out politics, memes, jokes - only extracting business/tech alpha")

    for idx, bookmark in enumerate(bookmarks, 1):
        # Extract bookmark fields (handle various JSON formats)
        text = bookmark.get('text', '') or bookmark.get('content', '')
        author = bookmark.get('author', '') or bookmark.get('handle', '') or '@unknown'
        url = bookmark.get('url', '') or bookmark.get('link', '')
        timestamp_str = bookmark.get('timestamp', '') or bookmark.get('created_at', '')

        # Skip if missing essential data
        if not text or not url:
            logger.debug(f"Skipping bookmark {idx}: missing text or URL")
            continue

        # Skip if too short (likely not valuable alpha)
        if len(text) < min_length:
            logger.debug(f"Skipping bookmark {idx}: too short ({len(text)} chars)")
            continue

        # CRITICAL: Filter out non-business content (politics, memes, jokes, etc.)
        # User bookmarks contain diverse content for algo training - we only want alpha
        is_relevant, filter_reason = is_relevant_content(text)
        if not is_relevant:
            logger.debug(f"Skipping bookmark {idx}: {filter_reason}")
            filtered_count += 1
            # Track filter reasons for summary
            reason_key = filter_reason.split(':')[0] if ':' in filter_reason else filter_reason
            filtered_reasons[reason_key] = filtered_reasons.get(reason_key, 0) + 1
            continue

        # Parse timestamp
        timestamp = parse_bookmark_timestamp(timestamp_str) if timestamp_str else datetime.now()

        # Convert to Tweet object
        tweet_id = url.split('/')[-1] if url else f"bookmark_{idx}"
        tweet = Tweet(
            id=tweet_id,
            author=author,
            content=text,
            url=url,
            timestamp=timestamp,
            engagement={},  # Bookmarks don't include engagement metrics
            media_urls=[]
        )

        # Create source info
        source_info = {
            'name': author,
            'focus_area': 'Bookmarked content',
            'signal_quality': 'HIGH',  # User pre-filtered by bookmarking
            'notes': 'User-curated bookmark'
        }

        # Analyze for alpha
        finding = scanner.analyze_tweet_for_alpha(tweet, source_info)

        if finding:
            findings.append(finding)
            logger.info(f"  [{idx}/{len(bookmarks)}] ✓ Alpha: {finding.title[:60]}...")
        else:
            logger.debug(f"  [{idx}/{len(bookmarks)}] No alpha detected")

    # Save findings
    if not dry_run and findings:
        saved_count = scanner.save_findings(findings)
        logger.info(f"\n✓ Saved {saved_count} new alpha findings to ALPHA_STAGING.csv")
    elif dry_run:
        logger.info(f"\nDRY RUN: Would save {len(findings)} findings")
        print("\nPreview of findings:")
        for finding in findings[:10]:  # Show first 10
            print(f"  - [{finding.category}] {finding.title[:70]}...")

    # Summary
    print("\n" + "="*60)
    print("BOOKMARK ALPHA EXTRACTION SUMMARY")
    print("="*60)
    print(f"Total bookmarks: {len(bookmarks)}")
    print(f"Filtered out (non-business): {filtered_count}")
    if filtered_reasons:
        print("  Filter breakdown:")
        for reason, count in sorted(filtered_reasons.items(), key=lambda x: -x[1]):
            print(f"    - {reason}: {count}")
    print(f"Alpha findings: {len(findings)}")
    if not dry_run and findings:
        print(f"New alpha saved: {saved_count}")
    analyzed = len(bookmarks) - filtered_count
    if analyzed > 0:
        print(f"Extraction rate: {len(findings)/analyzed*100:.1f}% (of relevant content)")
    print("="*60)

    if findings and not dry_run:
        print(f"\n✓ Review findings in: {ALPHA_STAGING}")
        print("  Status: PENDING_REVIEW")
        print("  Filter by source containing '@' to see bookmark entries")

    return findings


def main():
    parser = argparse.ArgumentParser(
        description='Extract alpha from X/Twitter bookmarks JSON'
    )
    parser.add_argument(
        'bookmarks_file',
        nargs='?',
        help='Path to bookmarks JSON file (e.g., x_bookmarks_2026-01-22.json)'
    )
    parser.add_argument(
        '--latest',
        action='store_true',
        help='Use the most recent bookmark file in current directory'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview findings without saving to ALPHA_STAGING.csv'
    )
    parser.add_argument(
        '--min-length',
        type=int,
        default=50,
        help='Minimum tweet length to consider (default: 50)'
    )

    args = parser.parse_args()

    # Determine which file to use
    if args.latest:
        bookmarks_file = find_latest_bookmark_file()
        if not bookmarks_file:
            logger.error("No bookmark files found matching x_bookmarks_*.json")
            return 1
        logger.info(f"Using latest bookmark file: {bookmarks_file.name}")
    elif args.bookmarks_file:
        bookmarks_file = Path(args.bookmarks_file)
        if not bookmarks_file.exists():
            logger.error(f"File not found: {bookmarks_file}")
            return 1
    else:
        # Try to find latest if no file specified
        bookmarks_file = find_latest_bookmark_file()
        if not bookmarks_file:
            parser.print_help()
            print("\nNo bookmark file specified and no x_bookmarks_*.json files found")
            return 1
        logger.info(f"No file specified, using latest: {bookmarks_file.name}")

    # Extract alpha
    findings = extract_alpha_from_bookmarks(
        bookmarks_file=bookmarks_file,
        dry_run=args.dry_run,
        min_length=args.min_length
    )

    return 0 if findings else 1


if __name__ == '__main__':
    sys.exit(main())
