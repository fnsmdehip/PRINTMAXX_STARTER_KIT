#!/usr/bin/env python3
"""
Daily Alpha Extractor - Multi-Platform Automated High-Signal Monitoring
Pulls latest content from HIGH_SIGNAL_SOURCES.csv accounts (X, Reddit, Web, YouTube)
Stages findings in ALPHA_STAGING.csv for human review

Usage:
    python3 daily_alpha_extractor.py                    # Run all auto_monitor accounts
    python3 daily_alpha_extractor.py --platform X       # Run only X/Twitter accounts
    python3 daily_alpha_extractor.py --platform Reddit  # Run only Reddit sources
    python3 daily_alpha_extractor.py --tier HIGHEST     # Run only HIGHEST signal accounts
    python3 daily_alpha_extractor.py --handles @levelsio @tdinh_me  # Specific accounts
    python3 daily_alpha_extractor.py --max 10           # Limit to 10 sources
    python3 daily_alpha_extractor.py --dry-run          # Preview without scraping
"""

import subprocess
import csv
import json
import time
import argparse
import re
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
LEDGER_DIR = BASE_DIR / "LEDGER"
HIGH_SIGNAL_FILE = LEDGER_DIR / "HIGH_SIGNAL_SOURCES.csv"
ALPHA_STAGING_FILE = LEDGER_DIR / "ALPHA_STAGING.csv"
SCRAPED_TWEETS_FILE = LEDGER_DIR / "SCRAPED_TWEETS_ALPHA.csv"

# Alpha classification keywords
ALPHA_CATEGORIES = {
    "APP_FACTORY": ["app", "mobile", "ios", "android", "flutter", "react native", "install", "download", "mrr", "arr", "paywall"],
    "CONTENT_FORMAT": ["hook", "format", "template", "thumbnail", "views", "viral", "algorithm", "carousel", "thread", "reel"],
    "OUTBOUND": ["cold email", "outbound", "deliverability", "open rate", "reply rate", "linkedin", "apollo", "instantly", "email list"],
    "GROWTH_HACK": ["growth", "hack", "organic", "tiktok", "reels", "shorts", "faceless", "ugc", "clipper", "distribution"],
    "TOOL_ALPHA": ["tool", "software", "api", "automation", "n8n", "zapier", "make", "workflow", "cursor", "lovable"],
    "COMPLIANCE": ["ftc", "disclosure", "legal", "compliance", "terms", "policy", "banned", "terminated"],
    "NICHE_INSIGHT": ["niche", "market", "women", "faith", "fitness", "opportunity", "underserved", "demographic"],
    "MONETIZATION": ["pricing", "offer", "upsell", "funnel", "conversion", "revenue", "monetize", "$", "flash sale", "paywall"],
    "ENGAGEMENT_FARM": ["passive", "autopilot", "mindset", "opportunities are insane", "believe", "anyone can"],
}

# Platform-specific extraction configs
PLATFORM_CONFIG = {
    "X": {
        "extractor": "applescript_x",
        "rate_limit": 3,  # seconds between accounts
    },
    "Reddit": {
        "extractor": "applescript_reddit",
        "rate_limit": 5,
    },
    "Web": {
        "extractor": "applescript_web",
        "rate_limit": 3,
    },
    "YouTube": {
        "extractor": "applescript_youtube",
        "rate_limit": 5,
    },
}


def applescript(script):
    """Run AppleScript and return output"""
    r = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return r.stdout.strip()


def navigate(url):
    """Navigate Brave to URL"""
    applescript(f'tell application "Brave Browser" to set URL of active tab of front window to "{url}"')


def get_page_text():
    """Get main text content from current page"""
    return applescript('tell application "Brave Browser" to execute active tab of front window javascript "document.body.innerText.substring(0, 5000)"')


# ============ X/TWITTER EXTRACTION ============
def get_x_tweets():
    """Get multiple recent tweets from X profile timeline"""
    return applescript('''tell application "Brave Browser" to execute active tab of front window javascript "
(function() {
    var tweets = document.querySelectorAll('[data-testid=tweet]');
    var results = [];
    for (var i = 0; i < Math.min(tweets.length, 5); i++) {
        var t = tweets[i];
        var text = t.querySelector('[data-testid=tweetText]');
        var time = t.querySelector('time');
        var link = t.querySelector('a[href*=\\"/status/\\"]');
        if (text) {
            results.push({
                text: text.innerText.substring(0, 500),
                timestamp: time ? time.getAttribute('datetime') : '',
                url: link ? 'https://x.com' + link.getAttribute('href') : ''
            });
        }
    }
    return JSON.stringify(results);
})()"''')


def extract_from_x(source, existing_urls):
    """Extract recent alpha from X/Twitter account"""
    findings = []
    handle = source['handle']
    profile_url = source['url']

    print(f"  Navigating to {handle}...", end=" ", flush=True)
    navigate(profile_url)
    time.sleep(4)

    tweets_json = get_x_tweets()
    try:
        tweets = json.loads(tweets_json) if tweets_json else []
    except json.JSONDecodeError:
        tweets = []

    if not tweets:
        print("No tweets found")
        return findings

    print(f"Found {len(tweets)} tweets")

    for tweet in tweets:
        text = tweet.get('text', '')
        url = tweet.get('url', '')
        timestamp = tweet.get('timestamp', '')

        if url in existing_urls or len(text) < 50:
            continue

        categories = classify_alpha(text)
        signal, signal_reason = assess_signal_quality(text)

        if signal == 'LOW':
            continue

        finding = create_finding(handle, url, text, categories, signal, signal_reason, source['focus'])
        findings.append(finding)
        existing_urls.add(url)
        print(f"    + Staged: {finding['title'][:40]}...")

    return findings


# ============ REDDIT EXTRACTION ============
def get_reddit_posts():
    """Get recent posts from Reddit subreddit"""
    return applescript('''tell application "Brave Browser" to execute active tab of front window javascript "
(function() {
    var posts = document.querySelectorAll('shreddit-post, [data-testid=post-container], article');
    var results = [];
    for (var i = 0; i < Math.min(posts.length, 10); i++) {
        var p = posts[i];
        var title = p.querySelector('h1, h3, [slot=title], a[data-click-id=body]');
        var link = p.querySelector('a[href*=\\"/r/\\"][href*=\\"/comments/\\"]');
        var score = p.querySelector('[data-click-id=upvote]~faceplate-number, shreddit-post') || {};
        if (title && link) {
            var href = link.getAttribute('href');
            if (!href.startsWith('http')) href = 'https://reddit.com' + href;
            results.push({
                title: title.innerText.substring(0, 200),
                url: href,
                score: score.innerText || ''
            });
        }
    }
    return JSON.stringify(results);
})()"''')


def get_reddit_post_body():
    """Get full body text from a Reddit post page"""
    return applescript('''tell application "Brave Browser" to execute active tab of front window javascript "
(function() {
    var body = document.querySelector('[slot=text-body], [data-click-id=text], .post-content, .RichTextJSON-root');
    return body ? body.innerText.substring(0, 2000) : '';
})()"''')


def extract_from_reddit(source, existing_urls):
    """Extract recent alpha from Reddit subreddit"""
    findings = []
    subreddit = source['handle']
    url = source['url']

    print(f"  Navigating to {subreddit}...", end=" ", flush=True)
    # Navigate to hot posts (most likely to have signal)
    navigate(url + "/hot/")
    time.sleep(5)

    posts_json = get_reddit_posts()
    try:
        posts = json.loads(posts_json) if posts_json else []
    except json.JSONDecodeError:
        posts = []

    if not posts:
        print("No posts found")
        return findings

    print(f"Found {len(posts)} posts")

    # Check top 3 posts for content
    for post in posts[:3]:
        post_url = post.get('url', '')
        title = post.get('title', '')

        if post_url in existing_urls or len(title) < 20:
            continue

        # Quick signal check on title
        categories = classify_alpha(title)
        signal, signal_reason = assess_signal_quality(title)

        if signal == 'LOW':
            continue

        # Navigate to post to get body
        navigate(post_url)
        time.sleep(3)
        body = get_reddit_post_body()

        full_text = f"{title}\n\n{body}" if body else title

        # Re-assess with full content
        categories = classify_alpha(full_text)
        signal, signal_reason = assess_signal_quality(full_text)

        if signal == 'LOW':
            continue

        finding = create_finding(subreddit, post_url, full_text, categories, signal, signal_reason, source['focus'])
        findings.append(finding)
        existing_urls.add(post_url)
        print(f"    + Staged: {finding['title'][:40]}...")

    return findings


# ============ WEB/TOOL EXTRACTION ============
def extract_from_web(source, existing_urls):
    """Extract content from web tools (Product Hunt, appkittie, etc.)"""
    findings = []
    name = source['handle']
    url = source['url']

    print(f"  Navigating to {name}...", end=" ", flush=True)
    navigate(url)
    time.sleep(4)

    # Get page content
    content = get_page_text()

    if not content or len(content) < 100:
        print("No content found")
        return findings

    print(f"Got {len(content)} chars")

    # For tools like Product Hunt, appkittie - look for trending items
    # This is a simplified version - specific tools may need custom extractors
    categories = classify_alpha(content)
    signal, signal_reason = assess_signal_quality(content)

    if signal != 'LOW' and url not in existing_urls:
        finding = create_finding(name, url, content[:1000], categories, signal, signal_reason, source['focus'])
        finding['reviewer_notes'] = f"Web content snapshot. Review for specific actionable items."
        findings.append(finding)
        existing_urls.add(url)
        print(f"    + Staged snapshot for review")

    return findings


# ============ YOUTUBE EXTRACTION ============
def extract_from_youtube(source, existing_urls):
    """Extract content from YouTube channels"""
    findings = []
    name = source['handle']
    url = source['url']

    print(f"  Navigating to {name}...", end=" ", flush=True)
    # Go to videos tab
    videos_url = url.rstrip('/') + '/videos'
    navigate(videos_url)
    time.sleep(4)

    # Get video titles from the page
    titles_json = applescript('''tell application "Brave Browser" to execute active tab of front window javascript "
(function() {
    var videos = document.querySelectorAll('#video-title');
    var results = [];
    for (var i = 0; i < Math.min(videos.length, 5); i++) {
        var v = videos[i];
        results.push({
            title: v.innerText,
            url: v.href || ''
        });
    }
    return JSON.stringify(results);
})()"''')

    try:
        videos = json.loads(titles_json) if titles_json else []
    except json.JSONDecodeError:
        videos = []

    if not videos:
        print("No videos found")
        return findings

    print(f"Found {len(videos)} videos")

    for video in videos[:3]:
        title = video.get('title', '')
        video_url = video.get('url', '')

        if video_url in existing_urls or len(title) < 10:
            continue

        categories = classify_alpha(title)
        signal, signal_reason = assess_signal_quality(title)

        # YouTube titles alone don't usually trigger high signal
        # But we still stage them for review if they match keywords
        if any(cat in ['APP_FACTORY', 'GROWTH_HACK', 'MONETIZATION'] for cat in categories):
            finding = create_finding(name, video_url, title, categories, 'MEDIUM', f"Video title match: {categories}", source['focus'])
            findings.append(finding)
            existing_urls.add(video_url)
            print(f"    + Staged: {title[:40]}...")

    return findings


# ============ COMMON UTILITIES ============
def classify_alpha(text):
    """Classify alpha content into categories"""
    text_lower = text.lower()
    categories = []
    for category, keywords in ALPHA_CATEGORIES.items():
        if any(kw in text_lower for kw in keywords):
            categories.append(category)
    return categories if categories else ["GENERAL"]


def assess_signal_quality(text):
    """Assess if content is high signal (actionable, specific numbers, etc.)"""
    # Check for specific numbers (revenue, conversion rates, etc.)
    has_numbers = bool(re.search(r'\$[\d,]+|\d+%|\d+k|\d+K|\d+x|\d+/mo|\d+ sales', text))

    # Check for actionable language
    actionable_words = ["step", "how to", "here's", "do this", "try this", "hack", "strategy", "tactic", "playbook", "framework"]
    has_actionable = any(word in text.lower() for word in actionable_words)

    # Check for fluff/noise
    noise_words = ["believe in yourself", "mindset", "grateful", "blessed", "motivation", "inspire", "journey"]
    is_noise = any(word in text.lower() for word in noise_words)

    # Check for engagement farm patterns
    farm_patterns = ["opportunities are insane", "passive income", "anyone can", "in just", "this one trick"]
    is_farm = any(pattern in text.lower() for pattern in farm_patterns)

    if is_noise:
        return "LOW", "Motivational/noise content"
    elif is_farm:
        return "MEDIUM", "Potential engagement farm - review for repurpose"
    elif has_numbers and has_actionable:
        return "HIGHEST", "Specific numbers + actionable"
    elif has_numbers:
        return "HIGH", "Contains specific numbers"
    elif has_actionable:
        return "MEDIUM", "Actionable but no specifics"
    else:
        return "LOW", "General content"


def create_finding(source_name, url, text, categories, signal, signal_reason, focus_area):
    """Create a standardized finding dict"""
    alpha_id = f"ALPHA_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash(url) % 1000:03d}"
    title = text[:60].replace('\n', ' ').strip() + "..."

    return {
        'alpha_id': alpha_id,
        'source': source_name,
        'source_url': url,
        'category': '|'.join(categories),
        'title': title,
        'description': text[:500].replace('\n', ' '),
        'actionable_steps': '',  # Human fills this
        'effort_level': 'MEDIUM',
        'roi_potential': signal,
        'risk_level': 'LOW',
        'applies_to_niches': 'ALL',
        'status': 'PENDING_REVIEW',
        'reviewed_date': '',
        'reviewer_notes': f"Auto-staged: {signal_reason}. Focus: {focus_area}"
    }


def load_sources(platform_filter=None, tier_filter=None, handles_filter=None, max_sources=None):
    """Load sources from HIGH_SIGNAL_SOURCES.csv"""
    sources = []
    with open(HIGH_SIGNAL_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only auto_monitor=TRUE
            if row.get('auto_monitor', '').upper() != 'TRUE':
                continue

            platform = row.get('platform', '')

            # Apply platform filter
            if platform_filter and platform != platform_filter:
                continue

            # Apply tier filter
            if tier_filter and row.get('signal_quality') != tier_filter:
                continue

            handle = row.get('source_name', '')
            if handles_filter and handle not in handles_filter:
                continue

            sources.append({
                'id': row.get('source_id'),
                'handle': handle,
                'url': row.get('url'),
                'platform': platform,
                'focus': row.get('focus_area'),
                'signal': row.get('signal_quality'),
                'notes': row.get('notes')
            })

    if max_sources:
        sources = sources[:max_sources]

    return sources


def load_existing_alpha():
    """Load existing alpha staging entries to avoid duplicates"""
    existing = set()
    if ALPHA_STAGING_FILE.exists():
        with open(ALPHA_STAGING_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('source_url'):
                    existing.add(row['source_url'])
    return existing


def save_alpha_staging(findings):
    """Append findings to ALPHA_STAGING.csv"""
    file_exists = ALPHA_STAGING_FILE.exists()

    fieldnames = [
        'alpha_id', 'source', 'source_url', 'category', 'title',
        'description', 'actionable_steps', 'effort_level', 'roi_potential',
        'risk_level', 'applies_to_niches', 'status', 'reviewed_date', 'reviewer_notes'
    ]

    with open(ALPHA_STAGING_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(findings)


def extract_from_source(source, existing_urls):
    """Route extraction to platform-specific handler"""
    platform = source['platform']

    extractors = {
        'X': extract_from_x,
        'Reddit': extract_from_reddit,
        'Web': extract_from_web,
        'YouTube': extract_from_youtube,
    }

    extractor = extractors.get(platform)
    if extractor:
        return extractor(source, existing_urls)
    else:
        print(f"  Skipping {source['handle']} - no extractor for platform: {platform}")
        return []


def main():
    parser = argparse.ArgumentParser(description='Daily Alpha Extractor - Multi-Platform')
    parser.add_argument('--platform', choices=['X', 'Reddit', 'Web', 'YouTube'], help='Filter by platform')
    parser.add_argument('--tier', choices=['HIGHEST', 'HIGH', 'MEDIUM'], help='Filter by signal tier')
    parser.add_argument('--handles', nargs='+', help='Specific handles to check')
    parser.add_argument('--max', type=int, help='Maximum sources to process')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be processed without extracting')
    args = parser.parse_args()

    print("=" * 60)
    print("DAILY ALPHA EXTRACTOR - Multi-Platform")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Load sources
    sources = load_sources(
        platform_filter=args.platform,
        tier_filter=args.tier,
        handles_filter=args.handles,
        max_sources=args.max
    )

    if not sources:
        print("No sources found matching criteria")
        return

    # Group by platform for display
    by_platform = {}
    for s in sources:
        p = s['platform']
        if p not in by_platform:
            by_platform[p] = []
        by_platform[p].append(s)

    print(f"\nSources to process: {len(sources)}")
    for platform, platform_sources in by_platform.items():
        print(f"\n  {platform} ({len(platform_sources)}):")
        for s in platform_sources[:5]:
            print(f"    - {s['handle']} ({s['signal']})")
        if len(platform_sources) > 5:
            print(f"    ... and {len(platform_sources) - 5} more")

    if args.dry_run:
        print("\n[DRY RUN] Would process the above sources")
        return

    # Load existing to avoid duplicates
    existing_urls = load_existing_alpha()
    print(f"\nExisting alpha entries: {len(existing_urls)}")

    # Extract from each source
    all_findings = []
    for i, source in enumerate(sources):
        print(f"\n[{i+1}/{len(sources)}] Processing {source['handle']} ({source['platform']})...")

        try:
            findings = extract_from_source(source, existing_urls)
            all_findings.extend(findings)
        except Exception as e:
            print(f"  ERROR: {e}")

        # Platform-specific rate limiting
        config = PLATFORM_CONFIG.get(source['platform'], {'rate_limit': 3})
        if i < len(sources) - 1:
            time.sleep(config['rate_limit'])

    # Save findings
    if all_findings:
        save_alpha_staging(all_findings)
        print(f"\n{'=' * 60}")
        print(f"COMPLETE: Staged {len(all_findings)} new alpha findings")
        print(f"Review at: {ALPHA_STAGING_FILE}")
    else:
        print(f"\n{'=' * 60}")
        print("No new high-signal alpha found this run")

    # Summary by category and platform
    if all_findings:
        print("\nFindings by category:")
        categories = {}
        for f in all_findings:
            for cat in f['category'].split('|'):
                categories[cat] = categories.get(cat, 0) + 1
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            print(f"  {cat}: {count}")

        print("\nFindings by source:")
        sources_count = {}
        for f in all_findings:
            sources_count[f['source']] = sources_count.get(f['source'], 0) + 1
        for src, count in sorted(sources_count.items(), key=lambda x: -x[1]):
            print(f"  {src}: {count}")


if __name__ == "__main__":
    main()
