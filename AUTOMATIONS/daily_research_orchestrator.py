#!/usr/bin/env python3
"""
Daily Research Orchestrator — PRINTMAXX
========================================
Cron: 0 5 * * * cd $BASE && $PYTHON AUTOMATIONS/daily_research_orchestrator.py --full >> AUTOMATIONS/logs/daily_research.log 2>&1

Orchestrates ALL daily research in one script:
  1. Calls existing scrapers (daily_research_pipeline.py, unified_alpha_monitor.py,
     background_reddit_scraper.py, trend_aggregator.py)
  2. Fills gaps: Hacker News (front page, Show HN, Ask HN), expanded subreddit scanning
     (15+ subs via Reddit public JSON API), Product Hunt daily top launches
  3. Deduplicates across all sources using content hashing (MD5)
  4. Scores findings by relevance to PrintMaxx niches
  5. Appends to ALPHA_STAGING.csv
  6. Generates daily digest markdown: AUTOMATIONS/logs/daily_digest_YYYY-MM-DD.md
  7. Logs to AUTOMATIONS/logs/daily_research.log

Usage:
  python3 AUTOMATIONS/daily_research_orchestrator.py --full       # Run everything
  python3 AUTOMATIONS/daily_research_orchestrator.py --gaps-only  # Only gap-filling scans (HN, expanded Reddit, PH)
  python3 AUTOMATIONS/daily_research_orchestrator.py --status     # Show last run stats
  python3 AUTOMATIONS/daily_research_orchestrator.py --dry-run    # Scan but don't write to ALPHA_STAGING
"""

import os
import sys
import csv
import json
import hashlib
import logging
import time
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import quote_plus

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT_ROOT / "AUTOMATIONS"
LEDGER = PROJECT_ROOT / "LEDGER"
LOGS = AUTOMATIONS / "logs"
ALPHA_CSV = LEDGER / "ALPHA_STAGING.csv"
LOCK_FILE = LOGS / "daily_research_orchestrator.lock"
STATE_FILE = LOGS / "daily_research_orchestrator_state.json"

# Ensure logs dir exists
LOGS.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------
LOG_FILE = LOGS / "daily_research.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(str(LOG_FILE), mode="a"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("orchestrator")

# ---------------------------------------------------------------------------
# LOCK FILE (prevent double-runs)
# ---------------------------------------------------------------------------
MAX_LOCK_AGE_MINUTES = 180  # 3 hours timeout


def acquire_lock() -> bool:
    if LOCK_FILE.exists():
        try:
            age = time.time() - LOCK_FILE.stat().st_mtime
            if age < MAX_LOCK_AGE_MINUTES * 60:
                log.warning("Lock file exists and is fresh (%d min old). Another run in progress.", int(age / 60))
                return False
            else:
                log.warning("Stale lock file (%d min old). Removing.", int(age / 60))
                LOCK_FILE.unlink()
        except Exception:
            pass
    LOCK_FILE.write_text(str(os.getpid()))
    return True


def release_lock():
    try:
        LOCK_FILE.unlink(missing_ok=True)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# HTTP HELPERS
# ---------------------------------------------------------------------------
USER_AGENT = "PRINTMAXX-Research/1.0 (research bot; contact: admin@printmaxx.dev)"
RATE_LIMIT_DELAY = 2.0  # seconds between requests (Reddit rate-limits at ~30 req/min)


def fetch_json(url: str, timeout: int = 30) -> dict | list | None:
    """Fetch JSON from URL with rate limiting and error handling."""
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
        time.sleep(RATE_LIMIT_DELAY)
        return data
    except (URLError, HTTPError, json.JSONDecodeError, Exception) as e:
        log.warning("Failed to fetch %s: %s", url, e)
        return None


def fetch_text(url: str, timeout: int = 30) -> str | None:
    """Fetch raw text/HTML from URL."""
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8", errors="replace")
        time.sleep(RATE_LIMIT_DELAY)
        return text
    except (URLError, HTTPError, Exception) as e:
        log.warning("Failed to fetch %s: %s", url, e)
        return None


# ---------------------------------------------------------------------------
# CONTENT HASHING & DEDUPLICATION
# ---------------------------------------------------------------------------
_seen_hashes: set[str] = set()


def content_hash(text: str) -> str:
    """MD5 hash of normalized text for deduplication."""
    normalized = re.sub(r"\s+", " ", text.lower().strip())
    return hashlib.md5(normalized.encode("utf-8")).hexdigest()[:16]


def load_existing_hashes():
    """Load content hashes from existing ALPHA_STAGING entries to avoid duplicates."""
    global _seen_hashes
    if not ALPHA_CSV.exists():
        return
    try:
        with open(ALPHA_CSV, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tactic = row.get("tactic", "")
                url = row.get("source_url", "")
                if tactic:
                    _seen_hashes.add(content_hash(tactic))
                if url:
                    _seen_hashes.add(content_hash(url))
    except Exception as e:
        log.warning("Error loading existing hashes: %s", e)
    log.info("Loaded %d existing content hashes for deduplication", len(_seen_hashes))


def is_duplicate(text: str, url: str = "") -> bool:
    """Check if content already exists in ALPHA_STAGING."""
    h1 = content_hash(text)
    h2 = content_hash(url) if url else ""
    if h1 in _seen_hashes:
        return True
    if h2 and h2 in _seen_hashes:
        return True
    return False


def mark_seen(text: str, url: str = ""):
    """Mark content as seen for this run."""
    _seen_hashes.add(content_hash(text))
    if url:
        _seen_hashes.add(content_hash(url))


# ---------------------------------------------------------------------------
# ALPHA_STAGING CSV HELPERS
# ---------------------------------------------------------------------------
ALPHA_HEADER = [
    "alpha_id", "source", "source_url", "category", "tactic", "roi_potential",
    "priority", "status", "applicable_methods", "applicable_niches",
    "synergy_score", "cross_sell_products", "implementation_priority",
    "engagement_authenticity", "earnings_verified", "extracted_method",
    "compliance_notes", "reviewer_notes", "created_at", "ops_generated",
]


def get_next_alpha_id() -> int:
    """Get the next alpha_id number from ALPHA_STAGING.csv."""
    max_id = 0
    if not ALPHA_CSV.exists():
        return 1
    try:
        with open(ALPHA_CSV, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                match = re.match(r"ALPHA(\d+)", line)
                if match:
                    num = int(match.group(1))
                    if num > max_id:
                        max_id = num
    except Exception:
        pass
    return max_id + 1


def append_alpha_entries(entries: list[dict], dry_run: bool = False) -> int:
    """Append entries to ALPHA_STAGING.csv. Returns count appended."""
    if not entries:
        return 0
    if dry_run:
        log.info("[DRY RUN] Would append %d entries to ALPHA_STAGING.csv", len(entries))
        return len(entries)

    file_exists = ALPHA_CSV.exists() and ALPHA_CSV.stat().st_size > 0
    try:
        with open(ALPHA_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=ALPHA_HEADER, extrasaction="ignore")
            if not file_exists:
                writer.writeheader()
            for entry in entries:
                writer.writerow(entry)
        return len(entries)
    except Exception as e:
        log.error("Failed to append to ALPHA_STAGING: %s", e)
        return 0


# ---------------------------------------------------------------------------
# SCORING & CATEGORIZATION
# ---------------------------------------------------------------------------
NICHE_KEYWORDS = {
    "APP_FACTORY": [
        "app", "ios", "android", "pwa", "mobile", "saas", "micro-saas",
        "microsaas", "subscription", "paywall", "revenue", "mrr", "arr",
        "indie", "solo dev", "side project", "build", "launch", "ship",
        "vibe code", "vibe-code", "clone", "wrapper", "api",
    ],
    "CONTENT_FORMAT": [
        "content", "viral", "thread", "tweet", "post", "hook", "engagement",
        "followers", "views", "impressions", "algorithm", "creator",
        "youtube", "tiktok", "reels", "shorts", "newsletter", "substack",
        "medium", "blog", "seo", "writing",
    ],
    "OUTBOUND": [
        "cold email", "outbound", "lead gen", "leads", "cold dm",
        "cold call", "outreach", "pipeline", "prospect", "reply rate",
        "open rate", "deliverability", "smtp", "warmup", "sequence",
    ],
    "GROWTH_HACK": [
        "growth hack", "hack", "trick", "shortcut", "loophole",
        "exploit", "arbitrage", "arb", "free traffic", "organic",
        "scrape", "automate", "automation", "scale", "10x", "100x",
    ],
    "TOOL_ALPHA": [
        "tool", "software", "platform", "framework", "library",
        "open source", "mit license", "github", "repo", "stack",
        "ai tool", "llm", "claude", "gpt", "cursor", "bolt",
    ],
    "MONETIZATION": [
        "monetiz", "revenue", "profit", "income", "earning",
        "pricing", "price", "charge", "sell", "product", "gumroad",
        "stripe", "payment", "affiliate", "commission", "ad revenue",
        "sponsor", "freemium", "premium", "upsell",
    ],
    "SEO_GEO_ASO": [
        "seo", "geo", "aso", "keyword", "ranking", "backlink",
        "search", "google", "app store", "play store", "optimization",
        "index", "crawl", "serp", "programmatic seo",
    ],
    "ECOM": [
        "ecom", "ecommerce", "dropship", "pod", "print on demand",
        "shopify", "etsy", "amazon", "ebay", "mercari", "product",
        "supplier", "wholesale", "private label", "fba",
    ],
    "FREELANCE": [
        "freelance", "upwork", "fiverr", "contract", "client",
        "agency", "service", "consulting", "gig", "hourly",
        "proposal", "portfolio",
    ],
    "AFFILIATE": [
        "affiliate", "referral", "commission", "partner program",
        "link", "coupon", "discount", "promo code",
    ],
}


def categorize_finding(text: str) -> str:
    """Categorize a finding based on keyword matching."""
    text_lower = text.lower()
    scores = {}
    for cat, keywords in NICHE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[cat] = score
    if not scores:
        return "GROWTH_HACK"  # default
    return max(scores, key=scores.get)


def score_finding(text: str, upvotes: int = 0, comments: int = 0) -> int:
    """Score a finding 0-100 for relevance and quality."""
    score = 0
    text_lower = text.lower()

    # Engagement signals
    if upvotes >= 500:
        score += 25
    elif upvotes >= 100:
        score += 20
    elif upvotes >= 50:
        score += 15
    elif upvotes >= 10:
        score += 10
    elif upvotes >= 5:
        score += 5

    if comments >= 100:
        score += 15
    elif comments >= 30:
        score += 10
    elif comments >= 10:
        score += 5

    # Specificity signals (numbers = specifics)
    numbers = re.findall(r"\$[\d,]+(?:\.\d+)?[kKmM]?|\d+%|\d+[kKmM]\b", text)
    score += min(len(numbers) * 5, 20)

    # Method signals
    method_keywords = [
        "framework", "template", "step by step", "how i", "how to",
        "case study", "exactly how", "here's what", "breakdown",
        "strategy", "tactic", "method", "system", "playbook",
    ]
    method_hits = sum(1 for kw in method_keywords if kw in text_lower)
    score += min(method_hits * 5, 15)

    # Proof signals
    proof_keywords = [
        "revenue", "mrr", "arr", "profit", "screenshot", "proof",
        "results", "data", "analytics", "conversion", "roi",
    ]
    proof_hits = sum(1 for kw in proof_keywords if kw in text_lower)
    score += min(proof_hits * 5, 15)

    # Actionability signals
    action_keywords = [
        "do this", "start with", "first", "then", "next",
        "sign up", "use", "install", "run", "build", "create",
    ]
    action_hits = sum(1 for kw in action_keywords if kw in text_lower)
    score += min(action_hits * 3, 10)

    return min(score, 100)


def score_to_status(score: int) -> str:
    """Convert score to alpha status."""
    if score >= 60:
        return "APPROVED"
    elif score >= 40:
        return "PENDING_REVIEW"
    elif score >= 25:
        return "ENGAGEMENT_BAIT"
    return "PENDING_REVIEW"


def score_to_roi(score: int) -> str:
    """Convert score to ROI potential."""
    if score >= 70:
        return "HIGHEST"
    elif score >= 50:
        return "HIGH"
    elif score >= 30:
        return "MEDIUM"
    return "LOW"


# ---------------------------------------------------------------------------
# PHASE 1: CALL EXISTING SCRAPERS
# ---------------------------------------------------------------------------
EXISTING_SCRIPTS = {
    "daily_research_pipeline": {
        "path": AUTOMATIONS / "daily_research_pipeline.py",
        "args": ["--cron"],
        "description": "Master scrape-extract-filter-repurpose pipeline (Twitter + Reddit)",
    },
    "unified_alpha_monitor": {
        "path": AUTOMATIONS / "unified_alpha_monitor.py",
        "args": ["--full"],
        "description": "Reddit niche + GitHub MIT + ASO + competitors + PH RSS + freshness",
    },
    "background_reddit_scraper": {
        "path": AUTOMATIONS / "background_reddit_scraper.py",
        "args": ["--full"],
        "description": "Reddit JSON API scraper for 20+ subreddits",
    },
    "trend_aggregator": {
        "path": AUTOMATIONS / "trend_aggregator.py",
        "args": ["--scan"],
        "description": "Google Trends + Reddit + Product Hunt trend detection",
    },
    "reddit_pain_point_miner": {
        "path": AUTOMATIONS / "reddit_pain_point_miner.py",
        "args": ["--scan"],
        "description": "Extract buying intent from 25 subreddits",
    },
}


def run_existing_scrapers() -> dict:
    """Run existing scraper scripts via subprocess. Returns run results."""
    results = {}
    python = sys.executable

    for name, info in EXISTING_SCRIPTS.items():
        script_path = info["path"]
        if not script_path.exists():
            log.warning("Script not found, skipping: %s", script_path)
            results[name] = {"status": "SKIPPED", "reason": "file not found"}
            continue

        log.info("Running %s: %s", name, info["description"])
        try:
            result = subprocess.run(
                [python, str(script_path)] + info["args"],
                capture_output=True,
                text=True,
                timeout=600,  # 10 min max per script
                cwd=str(PROJECT_ROOT),
            )
            if result.returncode == 0:
                log.info("  %s completed successfully", name)
                results[name] = {"status": "OK", "stdout_lines": len(result.stdout.splitlines())}
            else:
                log.warning("  %s exited with code %d", name, result.returncode)
                stderr_snippet = result.stderr[:500] if result.stderr else ""
                results[name] = {"status": "ERROR", "code": result.returncode, "stderr": stderr_snippet}
        except subprocess.TimeoutExpired:
            log.warning("  %s timed out after 10 minutes", name)
            results[name] = {"status": "TIMEOUT"}
        except Exception as e:
            log.warning("  %s failed: %s", name, e)
            results[name] = {"status": "EXCEPTION", "error": str(e)}

    return results


# ---------------------------------------------------------------------------
# PHASE 2: GAP-FILLING — HACKER NEWS
# ---------------------------------------------------------------------------
HN_ALGOLIA_BASE = "https://hn.algolia.com/api/v1"

# Subreddit lists for expanded scanning
EXPANDED_SUBREDDITS = [
    # Core solopreneur / indie hacker
    "entrepreneur", "SaaS", "indiehackers", "SideProject", "startups",
    "Entrepreneur", "smallbusiness", "sidehustle", "juststart",
    # App / dev specific
    "AppBusiness", "iOSProgramming", "reactnative", "nextjs", "webdev",
    # Marketing / growth
    "digital_marketing", "SEO", "PPC", "socialmedia", "emailmarketing",
    # Monetization
    "passive_income", "WorkOnline", "beermoney", "Affiliatemarketing",
    # Niche / vertical
    "digitalnomad", "freelance", "dropship", "AmazonFBA",
    # PrintMaxx app niches
    "productivity", "Fitness", "sleep", "intermittentfasting",
    "MuslimLounge", "NoFap",
    # Content / creator
    "NewTubers", "TikTokCreators",
    # Finance / crypto edge
    "cryptomarkets", "wallstreetbets",
    # AI / tools
    "ChatGPT", "ClaudeAI", "LocalLLaMA", "MachineLearning",
]


def scan_hacker_news() -> list[dict]:
    """Scan Hacker News for relevant stories using Algolia API."""
    findings = []
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)
    ts = int(yesterday.timestamp())

    # Search queries relevant to PrintMaxx
    queries = [
        "Show HN",
        "indie hacker revenue",
        "side project launch",
        "SaaS MRR",
        "cold email",
        "AI tool launch",
        "open source monetization",
        "mobile app revenue",
        "content creator income",
        "solopreneur",
    ]

    for query in queries:
        url = (
            f"{HN_ALGOLIA_BASE}/search_by_date?"
            f"query={quote_plus(query)}&tags=story&numericFilters=created_at_i>{ts}"
            f"&hitsPerPage=15"
        )
        data = fetch_json(url)
        if not data or "hits" not in data:
            continue

        for hit in data["hits"]:
            title = hit.get("title", "")
            story_url = hit.get("url", "") or f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}"
            points = hit.get("points", 0) or 0
            num_comments = hit.get("num_comments", 0) or 0
            author = hit.get("author", "")

            if not title or len(title) < 15:
                continue
            if is_duplicate(title, story_url):
                continue

            # Score it
            combined = f"{title} {query}"
            score = score_finding(combined, upvotes=points, comments=num_comments)

            if score < 20:
                continue

            category = categorize_finding(title)
            finding = {
                "source": f"HackerNews/{author}",
                "source_url": story_url,
                "category": category,
                "tactic": f"[HN] {title}",
                "score": score,
                "upvotes": points,
                "comments": num_comments,
                "roi_potential": score_to_roi(score),
                "status": score_to_status(score),
                "reviewer_notes": (
                    f"HN story. {points} points, {num_comments} comments. "
                    f"Query: '{query}'. Score: {score}/100."
                ),
            }
            findings.append(finding)
            mark_seen(title, story_url)

    # Deduplicate within this batch (by URL)
    seen_urls = set()
    unique = []
    for f in findings:
        if f["source_url"] not in seen_urls:
            seen_urls.add(f["source_url"])
            unique.append(f)

    log.info("Hacker News scan: %d findings (%d unique)", len(findings), len(unique))
    return unique


# ---------------------------------------------------------------------------
# PHASE 2: GAP-FILLING — EXPANDED REDDIT SCANNING
# ---------------------------------------------------------------------------
def scan_subreddit(sub: str, sort: str = "hot", limit: int = 25) -> list[dict]:
    """Scan a single subreddit via Reddit public JSON API."""
    url = f"https://www.reddit.com/r/{sub}/{sort}.json?limit={limit}&t=day"
    data = fetch_json(url, timeout=20)

    if not data or "data" not in data:
        return []

    findings = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        title = post.get("title", "")
        selftext = post.get("selftext", "")[:500]
        permalink = post.get("permalink", "")
        ups = post.get("ups", 0) or 0
        num_comments = post.get("num_comments", 0) or 0
        post_url = f"https://reddit.com{permalink}" if permalink else ""
        author = post.get("author", "[deleted]")

        if not title or len(title) < 10:
            continue
        if post.get("stickied"):
            continue
        if is_duplicate(title, post_url):
            continue

        combined = f"{title} {selftext}"
        score = score_finding(combined, upvotes=ups, comments=num_comments)

        if score < 15:
            continue

        category = categorize_finding(combined)
        preview = selftext[:200].replace("\n", " ").strip()

        finding = {
            "source": f"r/{sub}",
            "source_url": post_url,
            "category": category,
            "tactic": f"[r/{sub}] {title[:200]}",
            "score": score,
            "upvotes": ups,
            "comments": num_comments,
            "roi_potential": score_to_roi(score),
            "status": score_to_status(score),
            "reviewer_notes": (
                f"Reddit r/{sub}. {ups} upvotes, {num_comments} comments. "
                f"Score: {score}/100. Preview: {preview}"
            ),
        }
        findings.append(finding)
        mark_seen(title, post_url)

    return findings


def scan_expanded_subreddits() -> list[dict]:
    """Scan 30+ subreddits for alpha using Reddit JSON API."""
    all_findings = []
    success_count = 0
    fail_count = 0

    for sub in EXPANDED_SUBREDDITS:
        log.info("  Scanning r/%s ...", sub)
        try:
            findings = scan_subreddit(sub, sort="hot", limit=20)
            # Also scan top posts from past day
            top_findings = scan_subreddit(sub, sort="top", limit=10)
            combined = findings + top_findings

            # Dedupe within subreddit
            seen = set()
            unique = []
            for f in combined:
                if f["source_url"] not in seen:
                    seen.add(f["source_url"])
                    unique.append(f)

            all_findings.extend(unique)
            success_count += 1
            if unique:
                log.info("    Found %d posts from r/%s", len(unique), sub)
        except Exception as e:
            log.warning("    Failed r/%s: %s", sub, e)
            fail_count += 1

    log.info(
        "Expanded Reddit scan: %d total findings from %d/%d subreddits",
        len(all_findings), success_count, success_count + fail_count,
    )
    return all_findings


# ---------------------------------------------------------------------------
# PHASE 2: GAP-FILLING — PRODUCT HUNT DAILY TOP
# ---------------------------------------------------------------------------
def scan_product_hunt_daily() -> list[dict]:
    """Scan Product Hunt daily top launches via RSS/Atom feed and front page."""
    findings = []

    # Method 1: Atom feed
    feed_url = "https://www.producthunt.com/feed"
    feed_text = fetch_text(feed_url)
    if feed_text:
        # Parse Atom entries with regex
        entries = re.findall(
            r"<entry>.*?<title[^>]*>(.*?)</title>.*?<link[^>]*href=['\"]([^'\"]+)['\"].*?</entry>",
            feed_text,
            re.DOTALL,
        )
        for title, link in entries[:20]:
            title = re.sub(r"<[^>]+>", "", title).strip()
            if not title or is_duplicate(title, link):
                continue

            score = score_finding(title, upvotes=50, comments=10)
            if score < 15:
                continue

            category = categorize_finding(title)
            finding = {
                "source": "ProductHunt",
                "source_url": link,
                "category": category,
                "tactic": f"[PH Launch] {title}",
                "score": score,
                "upvotes": 0,
                "comments": 0,
                "roi_potential": score_to_roi(score),
                "status": "PENDING_REVIEW",
                "reviewer_notes": f"Product Hunt daily launch. Score: {score}/100.",
            }
            findings.append(finding)
            mark_seen(title, link)

    # Method 2: Front page JSON (unofficial)
    front_url = "https://www.producthunt.com/frontend/graphql"
    # Skip GraphQL — Atom feed is sufficient and more reliable

    log.info("Product Hunt scan: %d findings", len(findings))
    return findings


# ---------------------------------------------------------------------------
# PHASE 3: BUILD ALPHA ENTRIES
# ---------------------------------------------------------------------------
def build_alpha_entries(findings: list[dict], start_id: int) -> list[dict]:
    """Convert raw findings into ALPHA_STAGING.csv rows."""
    entries = []
    today = datetime.now().strftime("%Y-%m-%d")

    for i, f in enumerate(findings):
        alpha_id = f"ALPHA{start_id + i}"
        entry = {
            "alpha_id": alpha_id,
            "source": f.get("source", ""),
            "source_url": f.get("source_url", ""),
            "category": f.get("category", "GROWTH_HACK"),
            "tactic": f.get("tactic", ""),
            "roi_potential": f.get("roi_potential", "MEDIUM"),
            "priority": "BACKLOG",
            "status": f.get("status", "PENDING_REVIEW"),
            "applicable_methods": "",
            "applicable_niches": "",
            "synergy_score": "",
            "cross_sell_products": "",
            "implementation_priority": "",
            "engagement_authenticity": "",
            "earnings_verified": "",
            "extracted_method": "",
            "compliance_notes": "",
            "reviewer_notes": f.get("reviewer_notes", ""),
            "created_at": today,
            "ops_generated": "",
        }
        entries.append(entry)

    return entries


# ---------------------------------------------------------------------------
# PHASE 4: DAILY DIGEST GENERATION
# ---------------------------------------------------------------------------
def generate_daily_digest(
    scraper_results: dict,
    hn_findings: list[dict],
    reddit_findings: list[dict],
    ph_findings: list[dict],
    total_appended: int,
    dry_run: bool = False,
) -> str:
    """Generate a markdown digest of daily research results."""
    today = datetime.now().strftime("%Y-%m-%d")
    digest_path = LOGS / f"daily_digest_{today}.md"

    # Sort all findings by score descending
    all_gap_findings = hn_findings + reddit_findings + ph_findings
    all_gap_findings.sort(key=lambda x: x.get("score", 0), reverse=True)

    # Category distribution
    cat_counts: dict[str, int] = {}
    for f in all_gap_findings:
        cat = f.get("category", "OTHER")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    # Status distribution
    status_counts: dict[str, int] = {}
    for f in all_gap_findings:
        st = f.get("status", "PENDING_REVIEW")
        status_counts[st] = status_counts.get(st, 0) + 1

    lines = [
        f"# Daily Research Digest - {today}",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Mode:** {'DRY RUN' if dry_run else 'LIVE'}",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"- **Total new findings (gap-filling):** {len(all_gap_findings)}",
        f"  - Hacker News: {len(hn_findings)}",
        f"  - Expanded Reddit ({len(EXPANDED_SUBREDDITS)} subs): {len(reddit_findings)}",
        f"  - Product Hunt: {len(ph_findings)}",
        f"- **Appended to ALPHA_STAGING:** {total_appended}",
        "",
        "## Existing Scraper Results",
        "",
    ]

    for name, result in scraper_results.items():
        status = result.get("status", "UNKNOWN")
        emoji_map = {"OK": "[OK]", "ERROR": "[ERR]", "TIMEOUT": "[TIMEOUT]", "SKIPPED": "[SKIP]"}
        marker = emoji_map.get(status, "[?]")
        lines.append(f"- {marker} **{name}**: {status}")
        if "stderr" in result:
            lines.append(f"  - Error: {result['stderr'][:200]}")

    lines.extend([
        "",
        "## Category Distribution",
        "",
        "| Category | Count |",
        "|----------|-------|",
    ])
    for cat in sorted(cat_counts, key=cat_counts.get, reverse=True):
        lines.append(f"| {cat} | {cat_counts[cat]} |")

    lines.extend([
        "",
        "## Status Distribution",
        "",
        "| Status | Count |",
        "|--------|-------|",
    ])
    for st in sorted(status_counts, key=status_counts.get, reverse=True):
        lines.append(f"| {st} | {status_counts[st]} |")

    # Top findings
    top_20 = all_gap_findings[:20]
    if top_20:
        lines.extend([
            "",
            "## Top 20 Findings (by score)",
            "",
        ])
        for i, f in enumerate(top_20, 1):
            source = f.get("source", "?")
            tactic = f.get("tactic", "?")[:120]
            score = f.get("score", 0)
            ups = f.get("upvotes", 0)
            cmts = f.get("comments", 0)
            url = f.get("source_url", "")
            cat = f.get("category", "?")
            status = f.get("status", "?")
            lines.append(f"### {i}. [{cat}] Score: {score}/100 | {status}")
            lines.append(f"**{tactic}**")
            lines.append(f"Source: {source} | Upvotes: {ups} | Comments: {cmts}")
            if url:
                lines.append(f"URL: {url}")
            lines.append("")

    # Subreddit coverage
    sub_counts: dict[str, int] = {}
    for f in reddit_findings:
        src = f.get("source", "")
        sub_counts[src] = sub_counts.get(src, 0) + 1

    if sub_counts:
        lines.extend([
            "## Subreddit Coverage",
            "",
            "| Subreddit | Findings |",
            "|-----------|----------|",
        ])
        for sub in sorted(sub_counts, key=sub_counts.get, reverse=True):
            lines.append(f"| {sub} | {sub_counts[sub]} |")

    lines.extend([
        "",
        "---",
        f"*Generated by daily_research_orchestrator.py at {datetime.now().isoformat()}*",
    ])

    digest_content = "\n".join(lines)

    if not dry_run:
        digest_path.write_text(digest_content, encoding="utf-8")
        log.info("Daily digest written to %s", digest_path)
    else:
        log.info("[DRY RUN] Would write digest to %s", digest_path)

    return str(digest_path)


# ---------------------------------------------------------------------------
# STATE MANAGEMENT
# ---------------------------------------------------------------------------
def save_state(data: dict):
    """Save run state for --status queries."""
    try:
        STATE_FILE.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    except Exception as e:
        log.warning("Failed to save state: %s", e)


def load_state() -> dict | None:
    """Load last run state."""
    if not STATE_FILE.exists():
        return None
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def show_status():
    """Display last run status."""
    state = load_state()
    if not state:
        print("No previous run found.")
        return

    print(f"\n=== Daily Research Orchestrator — Last Run ===")
    print(f"Date:       {state.get('date', '?')}")
    print(f"Duration:   {state.get('duration_seconds', '?')}s")
    print(f"Mode:       {state.get('mode', '?')}")
    print(f"\nExisting scrapers:")
    for name, result in state.get("scraper_results", {}).items():
        print(f"  {name}: {result.get('status', '?')}")
    print(f"\nGap-filling results:")
    print(f"  HN findings:     {state.get('hn_count', 0)}")
    print(f"  Reddit findings:  {state.get('reddit_count', 0)}")
    print(f"  PH findings:      {state.get('ph_count', 0)}")
    print(f"  Total appended:   {state.get('total_appended', 0)}")
    print(f"  Digest:           {state.get('digest_path', 'N/A')}")
    print()


# ---------------------------------------------------------------------------
# MAIN ORCHESTRATION
# ---------------------------------------------------------------------------
def run_full(dry_run: bool = False, gaps_only: bool = False):
    """Run the full daily research orchestration."""
    start_time = time.time()
    today = datetime.now().strftime("%Y-%m-%d")

    log.info("=" * 60)
    log.info("DAILY RESEARCH ORCHESTRATOR — %s", today)
    log.info("Mode: %s", "DRY RUN" if dry_run else ("GAPS ONLY" if gaps_only else "FULL"))
    log.info("=" * 60)

    # Load existing hashes for deduplication
    load_existing_hashes()

    # Phase 1: Run existing scrapers (unless gaps-only)
    scraper_results = {}
    if not gaps_only:
        log.info("\n--- PHASE 1: Running existing scrapers ---")
        scraper_results = run_existing_scrapers()
        log.info("Existing scrapers complete: %d ran", len(scraper_results))
    else:
        log.info("\n--- PHASE 1: SKIPPED (gaps-only mode) ---")

    # Phase 2: Gap-filling scans
    log.info("\n--- PHASE 2: Gap-filling scans ---")

    log.info("\n[2a] Scanning Hacker News (Algolia API)...")
    hn_findings = scan_hacker_news()

    log.info("\n[2b] Scanning %d expanded subreddits (Reddit JSON API)...", len(EXPANDED_SUBREDDITS))
    reddit_findings = scan_expanded_subreddits()

    log.info("\n[2c] Scanning Product Hunt daily launches...")
    ph_findings = scan_product_hunt_daily()

    # Phase 3: Build and append alpha entries
    log.info("\n--- PHASE 3: Building alpha entries ---")
    all_findings = hn_findings + reddit_findings + ph_findings

    # Sort by score descending — best findings first
    all_findings.sort(key=lambda x: x.get("score", 0), reverse=True)

    next_id = get_next_alpha_id()
    entries = build_alpha_entries(all_findings, next_id)
    total_appended = append_alpha_entries(entries, dry_run=dry_run)

    log.info("Appended %d entries to ALPHA_STAGING.csv (starting ALPHA%d)", total_appended, next_id)

    # Phase 4: Generate daily digest
    log.info("\n--- PHASE 4: Generating daily digest ---")
    digest_path = generate_daily_digest(
        scraper_results, hn_findings, reddit_findings, ph_findings, total_appended, dry_run
    )

    # Save state
    duration = int(time.time() - start_time)
    state = {
        "date": today,
        "timestamp": datetime.now().isoformat(),
        "duration_seconds": duration,
        "mode": "DRY_RUN" if dry_run else ("GAPS_ONLY" if gaps_only else "FULL"),
        "scraper_results": scraper_results,
        "hn_count": len(hn_findings),
        "reddit_count": len(reddit_findings),
        "ph_count": len(ph_findings),
        "total_gap_findings": len(all_findings),
        "total_appended": total_appended,
        "digest_path": digest_path,
        "next_alpha_id_used": next_id,
    }
    save_state(state)

    # Final summary
    log.info("\n" + "=" * 60)
    log.info("ORCHESTRATION COMPLETE")
    log.info("  Duration: %d seconds (%d minutes)", duration, duration // 60)
    log.info("  Existing scrapers: %d ran", len(scraper_results))
    log.info("  HN findings: %d", len(hn_findings))
    log.info("  Reddit findings: %d (from %d subs)", len(reddit_findings), len(EXPANDED_SUBREDDITS))
    log.info("  PH findings: %d", len(ph_findings))
    log.info("  Total new entries: %d", total_appended)
    log.info("  Digest: %s", digest_path)
    log.info("=" * 60)

    return state


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Daily Research Orchestrator — runs all research, fills gaps, deduplicates, scores, appends to ALPHA_STAGING.csv"
    )
    parser.add_argument("--full", action="store_true", help="Run full orchestration (existing scrapers + gap-filling)")
    parser.add_argument("--gaps-only", action="store_true", help="Only run gap-filling scans (HN, expanded Reddit, PH)")
    parser.add_argument("--dry-run", action="store_true", help="Scan but don't write to ALPHA_STAGING.csv")
    parser.add_argument("--status", action="store_true", help="Show last run stats")
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if not args.full and not args.gaps_only:
        parser.print_help()
        print("\nUse --full for complete orchestration or --gaps-only for gap-filling scans only.")
        return

    if not acquire_lock():
        log.error("Could not acquire lock. Another instance may be running.")
        sys.exit(1)

    try:
        run_full(dry_run=args.dry_run, gaps_only=args.gaps_only)
    except KeyboardInterrupt:
        log.info("Interrupted by user.")
    except Exception as e:
        log.error("Orchestration failed: %s", e, exc_info=True)
    finally:
        release_lock()


if __name__ == "__main__":
    main()
