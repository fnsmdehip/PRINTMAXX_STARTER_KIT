#!/usr/bin/env python3
"""
COMMUNITY INTELLIGENCE SCANNER
===============================
Monitors solopreneur/indie hacker communities for actionable intelligence.
Scrapes Reddit (JSON API), Hacker News (Firebase API), and Product Hunt.
Extracts revenue signals, platform changes, growth tactics, tool discoveries,
warning signals, pricing intel, and competition intel.

Usage:
    python3 community_intel_scanner.py --scan
    python3 community_intel_scanner.py --scan-reddit
    python3 community_intel_scanner.py --scan-hn
    python3 community_intel_scanner.py --scan-ph
    python3 community_intel_scanner.py --top 10
    python3 community_intel_scanner.py --platform tiktok
    python3 community_intel_scanner.py --signal-type revenue
    python3 community_intel_scanner.py --since 7
    python3 community_intel_scanner.py --api-json
    python3 community_intel_scanner.py --status
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install: pip3 install requests")
    sys.exit(1)

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
COMMUNITY_INTEL_CSV = LEDGER_DIR / "COMMUNITY_INTEL.csv"
ALPHA_STAGING_CSV = LEDGER_DIR / "ALPHA_STAGING.csv"

INTEL_CSV_HEADERS = [
    "source", "subreddit_or_community", "post_url", "title", "signal_type",
    "signal_text", "score", "extracted_numbers", "platform_mentioned",
    "timestamp", "processed"
]

# Rate limiting
MIN_REQUEST_INTERVAL = 0.35  # ~3 requests/sec max per domain
REQUEST_TIMEOUT = 10
MAX_RETRIES = 2

# User agent for Reddit JSON API
USER_AGENT = "CommunityIntelScanner/1.0 (research bot; educational use)"

# All 25 subreddits
ALL_SUBREDDITS = [
    "juststart", "SideProject", "EntrepreneurRideAlong", "Affiliatemarketing",
    "dropship", "TikTokShop", "AmazonFBA", "Flipping", "sweatystartup",
    "microsaas", "OSINT", "webdev", "reactnative", "SEO", "Emailmarketing",
    "GrowthHacking", "digital_marketing", "passive_income", "WorkOnline",
    "beermoney", "AppBusiness", "iOSProgramming", "androiddev", "indiehackers",
    "slavelabour"
]

# Signal types
SIGNAL_TYPES = [
    "revenue", "platform_change", "growth_tactic", "tool", "warning",
    "pricing", "competition"
]

# Platform keywords for detection
PLATFORM_KEYWORDS = {
    "tiktok": ["tiktok", "tik tok", "tt shop", "tiktok shop"],
    "instagram": ["instagram", "ig", "reels", "insta"],
    "youtube": ["youtube", "yt", "shorts"],
    "twitter": ["twitter", "x.com", "x/twitter", "tweets"],
    "shopify": ["shopify"],
    "amazon": ["amazon", "fba", "amz"],
    "etsy": ["etsy"],
    "gumroad": ["gumroad"],
    "stripe": ["stripe"],
    "google": ["google", "seo", "google ads", "adsense", "serp"],
    "facebook": ["facebook", "fb", "meta ads", "fb ads"],
    "reddit": ["reddit"],
    "linkedin": ["linkedin"],
    "apple": ["apple", "ios", "app store", "iphone"],
    "android": ["android", "play store", "google play"],
    "substack": ["substack"],
    "beehiiv": ["beehiiv"],
    "notion": ["notion"],
    "vercel": ["vercel"],
    "cloudflare": ["cloudflare"],
    "whop": ["whop"],
    "lemon_squeezy": ["lemon squeezy", "lemonsqueezy"],
    "fiverr": ["fiverr"],
    "upwork": ["upwork"],
}

# Revenue signal patterns
REVENUE_PATTERNS = [
    r'\$[\d,]+(?:\.\d{2})?(?:\s*(?:k|K|m|M))?(?:\s*/\s*(?:mo|month|year|yr|day|week|hr|hour))?',
    r'(?:revenue|income|profit|mrr|arr|earnings|made|earned|grossed|netted)\s*(?:of\s*)?\$[\d,]+',
    r'\$[\d,]+(?:\.\d{2})?\s*(?:mrr|arr|revenue|income|profit)',
    r'(?:making|earning|generating|pulling|clearing)\s*\$[\d,]+',
    r'\b\d+(?:k|K)\s*/\s*(?:mo|month|year)\b',
    r'(?:monthly|annual|yearly|weekly|daily)\s*(?:revenue|income|profit)\s*(?:of\s*)?\$[\d,]+',
]

# Platform change patterns
PLATFORM_CHANGE_PATTERNS = [
    r'(?:algorithm|algo)\s*(?:update|change|shift)',
    r'(?:new|updated|changed)\s*(?:policy|policies|tos|terms)',
    r'(?:deprecat|sunset|remov|discontinu)',
    r'(?:new feature|just launched|now available|rolling out)',
    r'(?:ban(?:ned)?|penalt|crack(?:ing)?\s*down|restrict)',
    r'(?:api|sdk)\s*(?:change|update|deprecat|v\d)',
]

# Growth tactic patterns
GROWTH_PATTERNS = [
    r'(?:grew|growth|scaled)\s*(?:from|to)\s*\d+',
    r'(?:hack|tactic|strategy|trick)\s*(?:that|which)\s*(?:worked|helped|got)',
    r'(?:conversion|ctr|open\s*rate|click)\s*(?:rate|of)?\s*\d+',
    r'(?:first|got)\s*\d+\s*(?:users|customers|subscribers|downloads)',
    r'\d+%\s*(?:increase|growth|boost|improvement)',
]

# Warning signal patterns
WARNING_PATTERNS = [
    r'(?:banned|suspended|terminated|shut\s*down|restricted)',
    r'(?:scam|fraud|fake|ponzi|rug\s*pull)',
    r'(?:penalty|penalized|flagged|shadowban)',
    r'(?:lost|losing)\s*(?:account|money|revenue|traffic)',
    r'(?:don\'?t|never|avoid|warning|careful|beware)',
]


# ============================================================================
# RATE LIMITER
# ============================================================================

class RateLimiter:
    """Per-domain rate limiter."""

    def __init__(self, min_interval: float = MIN_REQUEST_INTERVAL):
        self.min_interval = min_interval
        self.last_request_time: dict[str, float] = {}

    def wait(self, domain: str):
        now = time.time()
        last = self.last_request_time.get(domain, 0)
        elapsed = now - last
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time[domain] = time.time()


rate_limiter = RateLimiter()


# ============================================================================
# HTTP HELPERS
# ============================================================================

def safe_get(url: str, domain: str = "reddit.com", headers: Optional[dict] = None,
             retries: int = MAX_RETRIES) -> Optional[dict]:
    """Rate-limited GET request with retries."""
    if headers is None:
        headers = {"User-Agent": USER_AGENT}
    else:
        headers.setdefault("User-Agent", USER_AGENT)

    for attempt in range(retries + 1):
        try:
            rate_limiter.wait(domain)
            resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                wait_time = 5 * (attempt + 1)
                print(f"  [429] Rate limited on {domain}, waiting {wait_time}s...")
                time.sleep(wait_time)
                continue
            elif resp.status_code in (403, 404):
                return None
            else:
                if attempt < retries:
                    time.sleep(2)
                    continue
                return None
        except requests.exceptions.Timeout:
            if attempt < retries:
                time.sleep(2)
                continue
            return None
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            if attempt < retries:
                time.sleep(2)
                continue
            return None
    return None


# ============================================================================
# SIGNAL EXTRACTION
# ============================================================================

def extract_numbers(text: str) -> str:
    """Extract dollar amounts and percentages from text."""
    numbers = []
    # Dollar amounts
    dollar_matches = re.findall(r'\$[\d,]+(?:\.\d{2})?(?:\s*(?:k|K|m|M))?', text)
    numbers.extend(dollar_matches)
    # Percentages
    pct_matches = re.findall(r'\d+(?:\.\d+)?%', text)
    numbers.extend(pct_matches)
    # Plain numbers with k/m suffix
    km_matches = re.findall(r'\b\d+(?:\.\d+)?\s*(?:k|K|m|M)\b', text)
    numbers.extend(km_matches)
    return "; ".join(numbers[:10]) if numbers else ""


def detect_platforms(text: str) -> str:
    """Detect platforms mentioned in text."""
    text_lower = text.lower()
    found = []
    for platform, keywords in PLATFORM_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                found.append(platform)
                break
    return "; ".join(found[:5]) if found else ""


def classify_signal(title: str, text: str) -> list[tuple[str, str]]:
    """Classify text into signal types. Returns list of (type, signal_text)."""
    combined = f"{title} {text}".lower()
    signals = []

    # Revenue signals
    for pattern in REVENUE_PATTERNS:
        matches = re.findall(pattern, combined, re.IGNORECASE)
        if matches:
            # Extract the sentence containing the match
            for match in matches[:2]:
                idx = combined.find(match.lower())
                start = max(0, combined.rfind('.', 0, idx) + 1)
                end = combined.find('.', idx)
                if end == -1:
                    end = min(len(combined), idx + 200)
                sentence = combined[start:end].strip()[:300]
                if sentence:
                    signals.append(("revenue", sentence))
            break

    # Platform changes
    for pattern in PLATFORM_CHANGE_PATTERNS:
        if re.search(pattern, combined, re.IGNORECASE):
            signals.append(("platform_change", combined[:300]))
            break

    # Growth tactics
    for pattern in GROWTH_PATTERNS:
        if re.search(pattern, combined, re.IGNORECASE):
            signals.append(("growth_tactic", combined[:300]))
            break

    # Tool discoveries
    tool_patterns = [
        r'(?:found|discovered|using|switched to|recommend|try)\s+(?:a\s+)?(?:tool|app|service|api|platform)',
        r'(?:built|launched|shipped|released)\s+(?:a|my|an)\s+',
        r'(?:open\s*source|github|repo)',
    ]
    for pattern in tool_patterns:
        if re.search(pattern, combined, re.IGNORECASE):
            signals.append(("tool", combined[:300]))
            break

    # Warning signals
    for pattern in WARNING_PATTERNS:
        if re.search(pattern, combined, re.IGNORECASE):
            signals.append(("warning", combined[:300]))
            break

    # Pricing intel
    pricing_patterns = [
        r'(?:charg|pric|cost|fee|rate)\w*\s*(?:\$|for|at|is)',
        r'(?:how much|what.*(?:charge|pay|cost))',
        r'(?:market rate|going rate|typical price)',
    ]
    for pattern in pricing_patterns:
        if re.search(pattern, combined, re.IGNORECASE):
            signals.append(("pricing", combined[:300]))
            break

    # Competition intel
    comp_patterns = [
        r'(?:competitor|competing|market\s*shift|new\s*player)',
        r'(?:saturated|oversaturated|too\s*many)',
        r'(?:market\s*(?:share|size|opportunity))',
    ]
    for pattern in comp_patterns:
        if re.search(pattern, combined, re.IGNORECASE):
            signals.append(("competition", combined[:300]))
            break

    return signals if signals else [("general", combined[:300])]


def score_signal(signal_type: str, text: str, upvotes: int, num_comments: int,
                 created_utc: float) -> int:
    """Score a signal 0-100 based on specificity, recency, social proof, actionability."""
    score = 0

    # Specificity (0-30)
    specificity = 0
    dollar_matches = re.findall(r'\$[\d,]+', text)
    if dollar_matches:
        specificity += 15
    pct_matches = re.findall(r'\d+%', text)
    if pct_matches:
        specificity += 8
    number_matches = re.findall(r'\b\d{2,}\b', text)
    if len(number_matches) >= 2:
        specificity += 7
    score += min(specificity, 30)

    # Recency (0-25)
    now = time.time()
    age_hours = (now - created_utc) / 3600
    if age_hours < 24:
        score += 25
    elif age_hours < 72:
        score += 20
    elif age_hours < 168:  # 1 week
        score += 15
    elif age_hours < 720:  # 1 month
        score += 8
    else:
        score += 2

    # Social proof (0-25)
    if upvotes >= 500:
        score += 25
    elif upvotes >= 200:
        score += 20
    elif upvotes >= 100:
        score += 16
    elif upvotes >= 50:
        score += 12
    elif upvotes >= 20:
        score += 8
    elif upvotes >= 5:
        score += 4

    if num_comments >= 100:
        score += 5  # bonus for high comment count (capped at total 25)

    # Actionability (0-20)
    actionability = 0
    action_words = ['how to', 'step by step', 'here\'s how', 'tutorial',
                    'guide', 'template', 'framework', 'exact', 'specific',
                    'strategy', 'method', 'approach', 'workflow', 'system']
    text_lower = text.lower()
    for word in action_words:
        if word in text_lower:
            actionability += 5
    score += min(actionability, 20)

    # Signal type bonus
    type_bonus = {
        "revenue": 5,
        "platform_change": 4,
        "growth_tactic": 4,
        "tool": 3,
        "warning": 5,
        "pricing": 3,
        "competition": 2,
        "general": 0,
    }
    score += type_bonus.get(signal_type, 0)

    return min(score, 100)


def content_hash(text: str) -> str:
    """Generate a content hash for deduplication."""
    normalized = re.sub(r'\s+', ' ', text.lower().strip())[:500]
    return hashlib.md5(normalized.encode()).hexdigest()[:12]


# ============================================================================
# CSV MANAGEMENT
# ============================================================================

def load_existing_hashes() -> set:
    """Load content hashes from existing COMMUNITY_INTEL.csv for dedup."""
    hashes = set()
    if COMMUNITY_INTEL_CSV.exists():
        try:
            with open(COMMUNITY_INTEL_CSV, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sig = row.get("signal_text", "")
                    if sig:
                        hashes.add(content_hash(sig))
        except Exception:
            pass
    return hashes


def ensure_csv_exists():
    """Create COMMUNITY_INTEL.csv with headers if it doesn't exist."""
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    if not COMMUNITY_INTEL_CSV.exists():
        with open(COMMUNITY_INTEL_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(INTEL_CSV_HEADERS)


def append_signals(signals: list[dict]):
    """Append signals to COMMUNITY_INTEL.csv, deduplicating."""
    if not signals:
        return 0

    ensure_csv_exists()
    existing_hashes = load_existing_hashes()
    new_count = 0

    with open(COMMUNITY_INTEL_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=INTEL_CSV_HEADERS)
        for sig in signals:
            h = content_hash(sig.get("signal_text", ""))
            if h not in existing_hashes:
                existing_hashes.add(h)
                writer.writerow(sig)
                new_count += 1

    return new_count


def append_to_alpha_staging(signals: list[dict]):
    """Append high-scoring signals (>75) to ALPHA_STAGING.csv."""
    high_signals = [s for s in signals if s.get("score", 0) > 75]
    if not high_signals or not ALPHA_STAGING_CSV.exists():
        return 0

    # Read existing alpha IDs to find next ID
    max_id = 0
    try:
        with open(ALPHA_STAGING_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                aid = row.get("alpha_id", "")
                if aid.startswith("ALPHA"):
                    try:
                        num = int(aid.replace("ALPHA", ""))
                        max_id = max(max_id, num)
                    except ValueError:
                        pass
    except Exception:
        return 0

    # Read header from ALPHA_STAGING
    try:
        with open(ALPHA_STAGING_CSV, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            alpha_headers = next(reader)
    except Exception:
        return 0

    count = 0
    with open(ALPHA_STAGING_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=alpha_headers, extrasaction='ignore')
        for sig in high_signals:
            max_id += 1
            row = {h: "" for h in alpha_headers}
            row["alpha_id"] = f"ALPHA{max_id}"
            row["source"] = sig.get("source", "Community Intel")
            row["source_url"] = sig.get("post_url", "")
            row["category"] = _map_signal_to_category(sig.get("signal_type", ""))
            row["tactic"] = sig.get("title", "")[:200]
            row["roi_potential"] = "HIGH" if sig.get("score", 0) > 85 else "MEDIUM"
            row["status"] = "PENDING_REVIEW"
            row["engagement_authenticity"] = "AUTHENTIC"
            row["earnings_verified"] = ""
            row["extracted_method"] = sig.get("signal_text", "")[:300]
            row["reviewer_notes"] = f"Auto-imported from community_intel_scanner. Score: {sig.get('score', 0)}. Platform: {sig.get('platform_mentioned', 'N/A')}"
            row["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            if "date_added" in alpha_headers:
                row["date_added"] = datetime.now().strftime("%Y-%m-%d")
            writer.writerow(row)
            count += 1

    return count


def _map_signal_to_category(signal_type: str) -> str:
    mapping = {
        "revenue": "MONETIZATION",
        "platform_change": "GROWTH_HACK",
        "growth_tactic": "GROWTH_HACK",
        "tool": "TOOL_ALPHA",
        "warning": "GROWTH_HACK",
        "pricing": "MONETIZATION",
        "competition": "GROWTH_HACK",
        "general": "GROWTH_HACK",
    }
    return mapping.get(signal_type, "GROWTH_HACK")


# ============================================================================
# REDDIT SCANNER
# ============================================================================

def scan_subreddit(subreddit: str, existing_hashes: set) -> list[dict]:
    """Scan a single subreddit for signals."""
    signals = []
    base_url = f"https://www.reddit.com/r/{subreddit}"

    # Fetch hot posts (up to 25)
    print(f"  Scanning r/{subreddit} (hot)...")
    hot_data = safe_get(f"{base_url}/hot.json?limit=25&raw_json=1", domain="reddit.com")
    if hot_data and "data" in hot_data:
        posts = hot_data["data"].get("children", [])
        signals.extend(_process_reddit_posts(posts, subreddit, existing_hashes))

    # Fetch new posts (up to 10)
    print(f"  Scanning r/{subreddit} (new)...")
    new_data = safe_get(f"{base_url}/new.json?limit=10&raw_json=1", domain="reddit.com")
    if new_data and "data" in new_data:
        posts = new_data["data"].get("children", [])
        signals.extend(_process_reddit_posts(posts, subreddit, existing_hashes))

    return signals


def _process_reddit_posts(posts: list, subreddit: str, existing_hashes: set) -> list[dict]:
    """Process a list of Reddit posts and extract signals."""
    signals = []

    for post in posts:
        data = post.get("data", {})
        if not data:
            continue

        title = data.get("title", "")
        selftext = data.get("selftext", "")[:2000]
        upvotes = data.get("ups", 0)
        num_comments = data.get("num_comments", 0)
        created_utc = data.get("created_utc", time.time())
        permalink = data.get("permalink", "")
        post_url = f"https://reddit.com{permalink}" if permalink else ""

        combined_text = f"{title} {selftext}"
        h = content_hash(combined_text)
        if h in existing_hashes:
            continue
        existing_hashes.add(h)

        # Classify signals
        detected_signals = classify_signal(title, selftext)

        for signal_type, signal_text in detected_signals:
            if signal_type == "general" and upvotes < 5:
                continue  # Skip low-engagement general posts

            score = score_signal(signal_type, combined_text, upvotes, num_comments, created_utc)

            if score < 15:
                continue  # Skip very low scoring signals

            signals.append({
                "source": "reddit",
                "subreddit_or_community": f"r/{subreddit}",
                "post_url": post_url,
                "title": title[:300],
                "signal_type": signal_type,
                "signal_text": signal_text[:500],
                "score": score,
                "extracted_numbers": extract_numbers(combined_text),
                "platform_mentioned": detect_platforms(combined_text),
                "timestamp": datetime.fromtimestamp(created_utc, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "processed": "FALSE",
            })

        # Fetch top comments for interesting posts (score > 40 or many comments)
        if (upvotes >= 20 or num_comments >= 10) and permalink:
            _fetch_reddit_comments(permalink, subreddit, created_utc, existing_hashes, signals)

    return signals


def _fetch_reddit_comments(permalink: str, subreddit: str, post_created_utc: float,
                           existing_hashes: set, signals: list):
    """Fetch top 5 comments from a Reddit post for deeper intel."""
    url = f"https://www.reddit.com{permalink}.json?limit=5&sort=top&raw_json=1"
    data = safe_get(url, domain="reddit.com")
    if not data or not isinstance(data, list) or len(data) < 2:
        return

    comments_data = data[1].get("data", {}).get("children", [])
    for comment in comments_data[:5]:
        cdata = comment.get("data", {})
        if not cdata or comment.get("kind") != "t1":
            continue

        body = cdata.get("body", "")[:1500]
        c_ups = cdata.get("ups", 0)
        if not body or c_ups < 3:
            continue

        h = content_hash(body)
        if h in existing_hashes:
            continue
        existing_hashes.add(h)

        detected = classify_signal("", body)
        for signal_type, signal_text in detected:
            if signal_type == "general":
                continue  # Only extract classified signals from comments

            score = score_signal(signal_type, body, c_ups, 0, post_created_utc)
            if score < 20:
                continue

            signals.append({
                "source": "reddit_comment",
                "subreddit_or_community": f"r/{subreddit}",
                "post_url": f"https://reddit.com{permalink}",
                "title": f"[comment] {body[:100]}",
                "signal_type": signal_type,
                "signal_text": signal_text[:500],
                "score": score,
                "extracted_numbers": extract_numbers(body),
                "platform_mentioned": detect_platforms(body),
                "timestamp": datetime.fromtimestamp(post_created_utc, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "processed": "FALSE",
            })


def scan_reddit(subreddits: Optional[list[str]] = None) -> list[dict]:
    """Scan all Reddit communities for signals."""
    if subreddits is None:
        subreddits = ALL_SUBREDDITS

    print(f"\n{'='*60}")
    print(f"REDDIT SCAN — {len(subreddits)} subreddits")
    print(f"{'='*60}")

    existing_hashes = load_existing_hashes()
    all_signals = []
    total_subs = len(subreddits)

    for i, sub in enumerate(subreddits, 1):
        print(f"\n[{i}/{total_subs}] r/{sub}")
        try:
            signals = scan_subreddit(sub, existing_hashes)
            all_signals.extend(signals)
            print(f"  -> {len(signals)} signals extracted")
        except Exception as e:
            print(f"  -> ERROR: {e}")

    print(f"\nReddit scan complete: {len(all_signals)} total signals")
    return all_signals


# ============================================================================
# HACKER NEWS SCANNER
# ============================================================================

HN_API_BASE = "https://hacker-news.firebaseio.com/v0"


def fetch_hn_item(item_id: int) -> Optional[dict]:
    """Fetch a single HN item by ID."""
    return safe_get(f"{HN_API_BASE}/item/{item_id}.json", domain="hacker-news.firebaseio.com")


def scan_hn() -> list[dict]:
    """Scan Hacker News for signals."""
    print(f"\n{'='*60}")
    print("HACKER NEWS SCAN")
    print(f"{'='*60}")

    existing_hashes = load_existing_hashes()
    all_signals = []

    # Get top stories
    print("\nFetching top stories...")
    top_ids = safe_get(f"{HN_API_BASE}/topstories.json", domain="hacker-news.firebaseio.com")
    if top_ids:
        top_ids = top_ids[:30]
        print(f"  Processing {len(top_ids)} top stories...")
        for i, item_id in enumerate(top_ids):
            item = fetch_hn_item(item_id)
            if item:
                signals = _process_hn_item(item, existing_hashes)
                all_signals.extend(signals)
            if (i + 1) % 10 == 0:
                print(f"  Processed {i+1}/{len(top_ids)} top stories ({len(all_signals)} signals so far)")

    # Get new stories and filter for "Show HN"
    print("\nFetching new stories (filtering for Show HN)...")
    new_ids = safe_get(f"{HN_API_BASE}/newstories.json", domain="hacker-news.firebaseio.com")
    if new_ids:
        show_hn_count = 0
        for item_id in new_ids[:100]:  # Check first 100 new stories for Show HN
            item = fetch_hn_item(item_id)
            if item and item.get("title", "").lower().startswith("show hn"):
                signals = _process_hn_item(item, existing_hashes)
                all_signals.extend(signals)
                show_hn_count += 1
                if show_hn_count >= 30:
                    break
        print(f"  Found {show_hn_count} Show HN posts")

    # Search for money-related "Ask HN" posts
    print("\nFetching Ask HN stories...")
    ask_ids = safe_get(f"{HN_API_BASE}/askstories.json", domain="hacker-news.firebaseio.com")
    if ask_ids:
        money_keywords = ["money", "revenue", "income", "side project", "solo", "indie",
                          "saas", "profit", "freelance", "startup"]
        ask_count = 0
        for item_id in ask_ids[:50]:
            item = fetch_hn_item(item_id)
            if item:
                title_lower = item.get("title", "").lower()
                if any(kw in title_lower for kw in money_keywords):
                    signals = _process_hn_item(item, existing_hashes, fetch_comments=True)
                    all_signals.extend(signals)
                    ask_count += 1
                    if ask_count >= 10:
                        break
        print(f"  Found {ask_count} relevant Ask HN posts")

    print(f"\nHacker News scan complete: {len(all_signals)} total signals")
    return all_signals


def _process_hn_item(item: dict, existing_hashes: set,
                     fetch_comments: bool = False) -> list[dict]:
    """Process a single HN item into signals."""
    signals = []

    title = item.get("title", "")
    text = item.get("text", "") or ""
    text = re.sub(r'<[^>]+>', ' ', text)[:2000]  # Strip HTML
    url = item.get("url", "")
    item_id = item.get("id", 0)
    score_val = item.get("score", 0)
    descendants = item.get("descendants", 0)
    created_time = item.get("time", time.time())

    combined = f"{title} {text}"
    h = content_hash(combined)
    if h in existing_hashes:
        return signals
    existing_hashes.add(h)

    post_url = f"https://news.ycombinator.com/item?id={item_id}"

    detected = classify_signal(title, text)
    for signal_type, signal_text in detected:
        sig_score = score_signal(signal_type, combined, score_val, descendants, created_time)
        if sig_score < 15:
            continue

        signals.append({
            "source": "hackernews",
            "subreddit_or_community": "HN",
            "post_url": post_url,
            "title": title[:300],
            "signal_type": signal_type,
            "signal_text": signal_text[:500],
            "score": sig_score,
            "extracted_numbers": extract_numbers(combined),
            "platform_mentioned": detect_platforms(combined),
            "timestamp": datetime.fromtimestamp(created_time, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "processed": "FALSE",
        })

    # Fetch top comments if requested
    if fetch_comments:
        kids = item.get("kids", [])[:5]
        for kid_id in kids:
            kid = fetch_hn_item(kid_id)
            if kid and kid.get("text"):
                kid_text = re.sub(r'<[^>]+>', ' ', kid.get("text", ""))[:1500]
                kid_h = content_hash(kid_text)
                if kid_h in existing_hashes:
                    continue
                existing_hashes.add(kid_h)

                kid_detected = classify_signal("", kid_text)
                for sig_type, sig_text in kid_detected:
                    if sig_type == "general":
                        continue
                    kid_score = score_signal(sig_type, kid_text, score_val, 0, created_time)
                    if kid_score < 20:
                        continue
                    signals.append({
                        "source": "hackernews_comment",
                        "subreddit_or_community": "HN",
                        "post_url": post_url,
                        "title": f"[comment] {kid_text[:100]}",
                        "signal_type": sig_type,
                        "signal_text": sig_text[:500],
                        "score": kid_score,
                        "extracted_numbers": extract_numbers(kid_text),
                        "platform_mentioned": detect_platforms(kid_text),
                        "timestamp": datetime.fromtimestamp(created_time, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                        "processed": "FALSE",
                    })

    return signals


# ============================================================================
# PRODUCT HUNT SCANNER
# ============================================================================

def scan_ph() -> list[dict]:
    """Scan Product Hunt for signals via web scraping of their public pages."""
    print(f"\n{'='*60}")
    print("PRODUCT HUNT SCAN")
    print(f"{'='*60}")

    existing_hashes = load_existing_hashes()
    all_signals = []

    # PH doesn't have an easy public JSON API anymore (GraphQL requires token)
    # Try scraping the RSS/Atom feed or the leaderboard JSON
    # Using the unofficial embed/widget approach
    urls_to_try = [
        "https://www.producthunt.com/frontend/graphql",  # requires auth
    ]

    # Fallback: scrape the public posts page via their embed API
    # PH has a /posts endpoint that sometimes returns JSON
    print("\nAttempting Product Hunt scrape via public endpoints...")

    # Try the public upcoming/trending page
    try:
        rate_limiter.wait("producthunt.com")
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        }
        resp = requests.get(
            "https://www.producthunt.com/frontend/graphql",
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        # This will likely fail without auth, but we try
    except Exception:
        pass

    # Alternative: Use the HN-style approach - search HN for PH launches
    print("  Falling back to HN search for Product Hunt launches...")
    # Search HN for producthunt.com links
    hn_search_url = "https://hn.algolia.com/api/v1/search_by_date?query=producthunt.com&tags=story&hitsPerPage=20"
    try:
        rate_limiter.wait("hn.algolia.com")
        resp = requests.get(hn_search_url, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            hits = data.get("hits", [])
            print(f"  Found {len(hits)} PH-related stories on HN")

            for hit in hits:
                title = hit.get("title", "")
                url = hit.get("url", "")
                points = hit.get("points", 0)
                created_at = hit.get("created_at_i", time.time())
                objectID = hit.get("objectID", "")
                num_comments = hit.get("num_comments", 0)

                combined = f"{title} {url}"
                h = content_hash(combined)
                if h in existing_hashes:
                    continue
                existing_hashes.add(h)

                post_url = f"https://news.ycombinator.com/item?id={objectID}" if objectID else url

                detected = classify_signal(title, "")
                # Most PH posts are tool discoveries
                if not any(s[0] != "general" for s in detected):
                    detected = [("tool", f"Product Hunt launch: {title}")]

                for signal_type, signal_text in detected:
                    score = score_signal(signal_type, combined, points, num_comments, created_at)
                    if score < 10:
                        continue

                    all_signals.append({
                        "source": "producthunt",
                        "subreddit_or_community": "ProductHunt",
                        "post_url": url or post_url,
                        "title": title[:300],
                        "signal_type": signal_type,
                        "signal_text": signal_text[:500],
                        "score": score,
                        "extracted_numbers": extract_numbers(combined),
                        "platform_mentioned": detect_platforms(combined),
                        "timestamp": datetime.fromtimestamp(created_at, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                        "processed": "FALSE",
                    })
    except Exception as e:
        print(f"  PH/HN search error: {e}")

    # Also try Reddit for PH launches
    print("  Scanning Reddit for Product Hunt launches...")
    ph_reddit = safe_get(
        "https://www.reddit.com/r/ProductHunt/hot.json?limit=15&raw_json=1",
        domain="reddit.com"
    )
    if ph_reddit and "data" in ph_reddit:
        posts = ph_reddit["data"].get("children", [])
        for post in posts:
            data = post.get("data", {})
            title = data.get("title", "")
            selftext = data.get("selftext", "")[:1000]
            upvotes = data.get("ups", 0)
            num_comments = data.get("num_comments", 0)
            created_utc = data.get("created_utc", time.time())
            permalink = data.get("permalink", "")

            combined = f"{title} {selftext}"
            h = content_hash(combined)
            if h in existing_hashes:
                continue
            existing_hashes.add(h)

            detected = classify_signal(title, selftext)
            if not any(s[0] != "general" for s in detected):
                detected = [("tool", f"PH: {title}")]

            for signal_type, signal_text in detected:
                score = score_signal(signal_type, combined, upvotes, num_comments, created_utc)
                if score < 10:
                    continue
                all_signals.append({
                    "source": "producthunt",
                    "subreddit_or_community": "ProductHunt/Reddit",
                    "post_url": f"https://reddit.com{permalink}" if permalink else "",
                    "title": title[:300],
                    "signal_type": signal_type,
                    "signal_text": signal_text[:500],
                    "score": score,
                    "extracted_numbers": extract_numbers(combined),
                    "platform_mentioned": detect_platforms(combined),
                    "timestamp": datetime.fromtimestamp(created_utc, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                    "processed": "FALSE",
                })

    print(f"\nProduct Hunt scan complete: {len(all_signals)} total signals")
    return all_signals


# ============================================================================
# DISPLAY AND REPORTING
# ============================================================================

def display_top_signals(n: int = 10, platform_filter: str = None,
                        signal_filter: str = None, since_days: int = None):
    """Display top N signals from COMMUNITY_INTEL.csv."""
    if not COMMUNITY_INTEL_CSV.exists():
        print("No data yet. Run --scan first.")
        return

    signals = []
    with open(COMMUNITY_INTEL_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Apply filters
            if platform_filter:
                if platform_filter.lower() not in row.get("platform_mentioned", "").lower():
                    continue
            if signal_filter:
                if signal_filter.lower() != row.get("signal_type", "").lower():
                    continue
            if since_days:
                try:
                    ts = datetime.strptime(row.get("timestamp", ""), "%Y-%m-%d %H:%M:%S")
                    ts = ts.replace(tzinfo=timezone.utc)
                    if (datetime.now(tz=timezone.utc) - ts).days > since_days:
                        continue
                except (ValueError, TypeError):
                    pass

            try:
                row["score"] = int(row.get("score", 0))
            except (ValueError, TypeError):
                row["score"] = 0
            signals.append(row)

    # Sort by score descending
    signals.sort(key=lambda x: x.get("score", 0), reverse=True)
    signals = signals[:n]

    if not signals:
        print("No signals match your criteria.")
        return

    print(f"\n{'='*80}")
    print(f"TOP {len(signals)} COMMUNITY INTELLIGENCE SIGNALS")
    if platform_filter:
        print(f"  Platform filter: {platform_filter}")
    if signal_filter:
        print(f"  Signal type filter: {signal_filter}")
    if since_days:
        print(f"  Since: last {since_days} days")
    print(f"{'='*80}\n")

    for i, sig in enumerate(signals, 1):
        score = sig.get("score", 0)
        # Color-code score
        if score >= 75:
            score_indicator = "[!!!]"
        elif score >= 50:
            score_indicator = "[!! ]"
        elif score >= 30:
            score_indicator = "[!  ]"
        else:
            score_indicator = "[   ]"

        print(f"{i:2d}. {score_indicator} Score: {score}")
        print(f"    Source: {sig.get('source', 'N/A')} | {sig.get('subreddit_or_community', 'N/A')}")
        print(f"    Type: {sig.get('signal_type', 'N/A')}")
        print(f"    Title: {sig.get('title', 'N/A')[:120]}")
        if sig.get("extracted_numbers"):
            print(f"    Numbers: {sig.get('extracted_numbers')}")
        if sig.get("platform_mentioned"):
            print(f"    Platforms: {sig.get('platform_mentioned')}")
        print(f"    URL: {sig.get('post_url', 'N/A')}")
        print(f"    Time: {sig.get('timestamp', 'N/A')}")
        print()


def show_status():
    """Show monitoring scope and last run stats."""
    print(f"\n{'='*60}")
    print("COMMUNITY INTELLIGENCE SCANNER STATUS")
    print(f"{'='*60}")

    print(f"\nMonitoring Scope:")
    print(f"  Reddit subreddits: {len(ALL_SUBREDDITS)}")
    for sub in ALL_SUBREDDITS:
        print(f"    - r/{sub}")
    print(f"  Hacker News: top stories + Show HN + Ask HN (money-related)")
    print(f"  Product Hunt: via HN search + r/ProductHunt")

    print(f"\nSignal Types:")
    for st in SIGNAL_TYPES:
        print(f"    - {st}")

    print(f"\nOutput Files:")
    print(f"  COMMUNITY_INTEL.csv: {COMMUNITY_INTEL_CSV}")
    print(f"  ALPHA_STAGING.csv:   {ALPHA_STAGING_CSV}")

    if COMMUNITY_INTEL_CSV.exists():
        total = 0
        type_counts: dict[str, int] = {}
        source_counts: dict[str, int] = {}
        high_score = 0
        latest_ts = ""

        with open(COMMUNITY_INTEL_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += 1
                st = row.get("signal_type", "unknown")
                type_counts[st] = type_counts.get(st, 0) + 1
                src = row.get("source", "unknown")
                source_counts[src] = source_counts.get(src, 0) + 1
                try:
                    score = int(row.get("score", 0))
                    if score > 75:
                        high_score += 1
                except (ValueError, TypeError):
                    pass
                ts = row.get("timestamp", "")
                if ts > latest_ts:
                    latest_ts = ts

        print(f"\nLast Run Stats:")
        print(f"  Total signals: {total}")
        print(f"  High-score signals (>75): {high_score}")
        print(f"  Latest timestamp: {latest_ts}")

        print(f"\n  By signal type:")
        for st, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"    {st}: {count}")

        print(f"\n  By source:")
        for src, count in sorted(source_counts.items(), key=lambda x: -x[1]):
            print(f"    {src}: {count}")
    else:
        print(f"\n  No data yet. Run --scan first.")


def output_api_json(platform_filter: str = None, signal_filter: str = None,
                    since_days: int = None):
    """Output signals as JSON for webapp consumption."""
    if not COMMUNITY_INTEL_CSV.exists():
        print(json.dumps({"error": "No data. Run --scan first.", "signals": []}))
        return

    signals = []
    with open(COMMUNITY_INTEL_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if platform_filter:
                if platform_filter.lower() not in row.get("platform_mentioned", "").lower():
                    continue
            if signal_filter:
                if signal_filter.lower() != row.get("signal_type", "").lower():
                    continue
            if since_days:
                try:
                    ts = datetime.strptime(row.get("timestamp", ""), "%Y-%m-%d %H:%M:%S")
                    ts = ts.replace(tzinfo=timezone.utc)
                    if (datetime.now(tz=timezone.utc) - ts).days > since_days:
                        continue
                except (ValueError, TypeError):
                    pass
            try:
                row["score"] = int(row.get("score", 0))
            except (ValueError, TypeError):
                row["score"] = 0
            signals.append(row)

    signals.sort(key=lambda x: x.get("score", 0), reverse=True)

    output = {
        "generated_at": datetime.now().isoformat(),
        "total_signals": len(signals),
        "filters": {
            "platform": platform_filter,
            "signal_type": signal_filter,
            "since_days": since_days,
        },
        "signals": signals,
    }
    print(json.dumps(output, indent=2))


# ============================================================================
# MAIN CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Community Intelligence Scanner - Monitor solopreneur communities for actionable signals"
    )
    parser.add_argument("--scan", action="store_true",
                        help="Full scan of all communities (Reddit + HN + PH)")
    parser.add_argument("--scan-reddit", action="store_true",
                        help="Scan Reddit communities only")
    parser.add_argument("--scan-hn", action="store_true",
                        help="Scan Hacker News only")
    parser.add_argument("--scan-ph", action="store_true",
                        help="Scan Product Hunt only")
    parser.add_argument("--top", type=int, metavar="N",
                        help="Show top N signals by score")
    parser.add_argument("--platform", type=str, metavar="PLATFORM",
                        help="Filter by platform mentioned (e.g., tiktok, shopify)")
    parser.add_argument("--signal-type", type=str, metavar="TYPE",
                        choices=SIGNAL_TYPES + ["general"],
                        help="Filter by signal type")
    parser.add_argument("--since", type=int, metavar="DAYS",
                        help="Only signals from last N days")
    parser.add_argument("--api-json", action="store_true",
                        help="Output as JSON for webapp")
    parser.add_argument("--status", action="store_true",
                        help="Show monitoring scope and last run stats")
    parser.add_argument("--subreddits", type=str, metavar="LIST",
                        help="Comma-separated list of subreddits to scan (override default)")

    args = parser.parse_args()

    # Default to --status if no args
    if not any([args.scan, args.scan_reddit, args.scan_hn, args.scan_ph,
                args.top, args.api_json, args.status]):
        parser.print_help()
        return

    if args.status:
        show_status()
        return

    # If only display/filter flags (no scan), show from existing data
    is_scanning = any([args.scan, args.scan_reddit, args.scan_hn, args.scan_ph])

    if args.api_json and not is_scanning:
        output_api_json(
            platform_filter=args.platform,
            signal_filter=args.signal_type,
            since_days=args.since,
        )
        return

    if args.top and not is_scanning:
        display_top_signals(
            n=args.top,
            platform_filter=args.platform,
            signal_filter=args.signal_type,
            since_days=args.since,
        )
        return

    # SCAN modes
    all_signals = []
    start_time = time.time()

    subreddits_override = None
    if args.subreddits:
        subreddits_override = [s.strip() for s in args.subreddits.split(",")]

    if args.scan or args.scan_reddit:
        reddit_signals = scan_reddit(subreddits=subreddits_override)
        all_signals.extend(reddit_signals)

    if args.scan or args.scan_hn:
        hn_signals = scan_hn()
        all_signals.extend(hn_signals)

    if args.scan or args.scan_ph:
        ph_signals = scan_ph()
        all_signals.extend(ph_signals)

    # Save results
    if all_signals:
        new_count = append_signals(all_signals)
        alpha_count = append_to_alpha_staging(all_signals)
        elapsed = time.time() - start_time

        print(f"\n{'='*60}")
        print("SCAN COMPLETE")
        print(f"{'='*60}")
        print(f"  Total signals found:     {len(all_signals)}")
        print(f"  New signals saved:       {new_count}")
        print(f"  Duplicates skipped:      {len(all_signals) - new_count}")
        print(f"  High-score (>75) to alpha: {alpha_count}")
        print(f"  Time elapsed:            {elapsed:.1f}s")
        print(f"  Output: {COMMUNITY_INTEL_CSV}")
        if alpha_count > 0:
            print(f"  Alpha staging: {ALPHA_STAGING_CSV} (+{alpha_count})")
    else:
        print("\nNo signals found in this scan.")

    # Show top N after scan if --top was requested
    if args.top:
        display_top_signals(
            n=args.top,
            platform_filter=args.platform,
            signal_filter=args.signal_type,
            since_days=args.since,
        )
    elif all_signals:
        # Default: show top 10 from this scan
        top_signals = sorted(all_signals, key=lambda x: x.get("score", 0), reverse=True)[:10]
        print(f"\nTOP 10 SIGNALS FROM THIS SCAN:")
        print("-" * 50)
        for i, sig in enumerate(top_signals, 1):
            print(f"{i:2d}. [{sig.get('score', 0):3d}] [{sig.get('signal_type', 'N/A'):16s}] "
                  f"{sig.get('title', 'N/A')[:80]}")


if __name__ == "__main__":
    main()
