#!/usr/bin/env python3
"""
ALPHA MONITOR — 24/7 Automated Tactic & Growth Hack Research
=============================================================
Monitors subreddits, forums, news sites, and Twitter accounts for
actionable growth tactics, algorithm changes, and revenue alpha.

Feeds into ALPHA_STAGING.csv and daily research pipeline.

Sources monitored:
  - Reddit: r/Entrepreneur, r/juststart, r/sweatystartup, r/SideProject,
            r/digital_marketing, r/socialmedia, r/Affiliatemarketing,
            r/indiehackers, r/EntrepreneurRideAlong, r/webdev, r/SaaS
  - Forums: BlackHatWorld, GrowthHackers, IndieHackers, Warrior Forum
  - News: TechCrunch, The Verge, FTC.gov, AdTechRadar
  - Twitter: @Cluely, @levelsio, @dannypostmaa, @tdinh_me, @GergelyOrosz,
             + all HIGH_SIGNAL_SOURCES.csv accounts

Usage:
    python3 alpha_monitor.py --full           # Full scan all sources
    python3 alpha_monitor.py --reddit         # Reddit only
    python3 alpha_monitor.py --forums         # Forums only
    python3 alpha_monitor.py --news           # News/platform changes only
    python3 alpha_monitor.py --status         # Show last scan results
    python3 alpha_monitor.py --cron           # Lightweight cron mode

Cron entry:
    0 */4 * * * cd $BASE && python3 AUTOMATIONS/alpha_monitor.py --cron >> AUTOMATIONS/logs/alpha_monitor.log 2>&1
"""

import argparse
import csv
import hashlib
import json
import logging
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

# ─── Paths ──────────────────────────────────────────────────
PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
AUTOMATIONS = PROJECT_DIR / "AUTOMATIONS"
LEDGER = PROJECT_DIR / "LEDGER"
OPS = PROJECT_DIR / "OPS"
LOGS = AUTOMATIONS / "logs"
LOGS.mkdir(exist_ok=True)

ALPHA_STAGING = LEDGER / "ALPHA_STAGING.csv"
HIGH_SIGNAL_SOURCES = LEDGER / "HIGH_SIGNAL_SOURCES.csv"
MONITOR_OUTPUT = AUTOMATIONS / "alpha_monitor_output"
MONITOR_OUTPUT.mkdir(exist_ok=True)

# ─── Logging ────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOGS / "alpha_monitor.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("alpha_monitor")

# ─── Reddit Sources ─────────────────────────────────────────
REDDIT_TACTIC_SUBS = [
    "Entrepreneur",           # tactics, case studies
    "juststart",              # affiliate, SEO
    "sweatystartup",          # growth hacks
    "SideProject",            # what's working
    "digital_marketing",      # platform updates
    "socialmedia",            # algorithm changes
    "Affiliatemarketing",     # affiliate tactics
    "indiehackers",           # revenue numbers
    "EntrepreneurRideAlong",  # case studies with numbers
    "webdev",                 # tech alpha
    "SaaS",                   # SaaS tactics
    "startups",               # funding/growth patterns
    "growthacking",           # growth tactics
    "SEO",                    # SEO changes
    "PPC",                    # ad platform changes
    "ecommerce",              # ecom tactics
    "dropship",               # dropship alpha
    "Flipping",               # arbitrage
    "WorkOnline",             # remote income
    "beermoney",              # micro income hacks
]

# ─── Forum Sources ──────────────────────────────────────────
FORUM_SOURCES = {
    "BlackHatWorld": {
        "url": "https://www.blackhatworld.com/forums/",
        "sections": ["making-money", "social-networking", "search-engine-optimization"],
        "filter": "legal_only",  # Filter for legal tactics only
    },
    "GrowthHackers": {
        "url": "https://growthhackers.com/posts",
        "sections": ["growth", "marketing", "product"],
        "filter": "case_studies",
    },
    "IndieHackers": {
        "url": "https://www.indiehackers.com",
        "sections": ["post"],
        "filter": "revenue_numbers",
    },
    "WarriorForum": {
        "url": "https://www.warriorforum.com/",
        "sections": ["main-internet-marketing-discussion-forum"],
        "filter": "affiliate_marketing",
    },
}

# ─── News Sources (Platform Policy & Regulation) ────────────
NEWS_SOURCES = {
    "TechCrunch": {
        "rss": "https://techcrunch.com/feed/",
        "keywords": ["platform policy", "algorithm", "creator", "monetization",
                     "app store", "tiktok", "instagram", "youtube", "twitter",
                     "affiliate", "FTC", "regulation", "AI"],
    },
    "TheVerge": {
        "rss": "https://www.theverge.com/rss/index.xml",
        "keywords": ["regulation", "platform", "creator economy", "social media",
                     "algorithm", "ban", "policy", "AI", "Apple", "Google"],
    },
    "FTC": {
        "url": "https://www.ftc.gov/news-events/news/press-releases",
        "keywords": ["enforcement", "settlement", "advertising", "disclosure",
                     "social media", "influencer", "affiliate"],
    },
}

# ─── Twitter Accounts to Monitor ────────────────────────────
PRIORITY_TWITTER_ACCOUNTS = [
    "Cluely",           # watch their tactics
    "levelsio",         # indie hackers
    "dannypostmaa",     # growth tactics
    "tdinh_me",         # technical marketing
    "GergelyOrosz",     # tech industry
    "paborenstein",     # pipeline tactics
    "seanb2b",          # cold email
    "GrowthTactics",    # growth
    "alexgarcia_atx",   # content strategy
    "JamesonCamp",      # AI apps
]

# ─── App Factory Research Sources ────────────────────────────
APP_FACTORY_SOURCES = {
    "ASO_keywords": [
        "focus timer", "habit tracker", "prayer times", "meal planner",
        "sleep tracker", "walk tracker", "productivity", "fitness",
    ],
    "competitor_apps_to_monitor": [
        "Forest", "Headspace", "MyFitnessPal", "Strava",
        "Muslim Pro", "Calm", "Habitica", "WaterMinder",
    ],
    "review_mining_keywords": [
        "wish it had", "missing feature", "would pay for",
        "switched from", "better than", "doesn't work",
    ],
}


def safe_path(target):
    """Verify path is within project root."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_DIR)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root")
    return resolved


def get_next_alpha_id():
    """Get next ALPHA ID from staging CSV."""
    if not ALPHA_STAGING.exists():
        return "ALPHA0001"
    max_id = 0
    with open(ALPHA_STAGING, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            aid = row.get("alpha_id", "")
            match = re.match(r"ALPHA(\d+)", aid)
            if match:
                max_id = max(max_id, int(match.group(1)))
    return f"ALPHA{max_id + 1:04d}"


def content_hash(text):
    """Generate hash to detect duplicate entries."""
    return hashlib.md5(text.strip().lower().encode()).hexdigest()[:12]


def scrape_reddit_sub(subreddit, sort="hot", limit=25):
    """Scrape a subreddit using Reddit JSON API (no auth needed)."""
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}"
    headers = {"User-Agent": "PRINTMAXX-AlphaMonitor/1.0"}

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())

        posts = []
        for child in data.get("data", {}).get("children", []):
            post = child.get("data", {})
            posts.append({
                "title": post.get("title", ""),
                "selftext": post.get("selftext", "")[:500],
                "score": post.get("score", 0),
                "num_comments": post.get("num_comments", 0),
                "url": f"https://reddit.com{post.get('permalink', '')}",
                "author": post.get("author", ""),
                "created_utc": post.get("created_utc", 0),
                "subreddit": subreddit,
            })
        return posts
    except Exception as e:
        log.warning(f"Failed to scrape r/{subreddit}: {e}")
        return []


def scrape_rss_feed(url, keywords):
    """Scrape RSS feed and filter by keywords."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PRINTMAXX-AlphaMonitor/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="replace")

        # Simple XML parsing for RSS items
        items = []
        item_blocks = re.findall(r"<item>(.*?)</item>", content, re.DOTALL)
        if not item_blocks:
            item_blocks = re.findall(r"<entry>(.*?)</entry>", content, re.DOTALL)

        for block in item_blocks[:30]:
            title = re.search(r"<title[^>]*>(.*?)</title>", block, re.DOTALL)
            link = re.search(r"<link[^>]*>(.*?)</link>", block, re.DOTALL)
            if not link:
                link = re.search(r'<link[^>]*href="([^"]+)"', block)
            desc = re.search(r"<description>(.*?)</description>", block, re.DOTALL)

            title_text = title.group(1).strip() if title else ""
            # Strip CDATA
            title_text = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", title_text)

            link_text = ""
            if link:
                link_text = link.group(1).strip()
                link_text = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", link_text)

            desc_text = ""
            if desc:
                desc_text = desc.group(1).strip()[:300]
                desc_text = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", desc_text)
                desc_text = re.sub(r"<[^>]+>", "", desc_text)

            # Keyword filter
            combined = f"{title_text} {desc_text}".lower()
            if any(kw.lower() in combined for kw in keywords):
                items.append({
                    "title": title_text,
                    "url": link_text,
                    "description": desc_text,
                    "source": url,
                })

        return items
    except Exception as e:
        log.warning(f"Failed to scrape RSS {url}: {e}")
        return []


def score_reddit_post(post):
    """Score a Reddit post for alpha value (0-100)."""
    score = 0
    text = f"{post['title']} {post['selftext']}".lower()

    # Revenue/number signals (high value)
    if re.search(r"\$\d+", text):
        score += 25
    if re.search(r"\d+%", text):
        score += 15
    if re.search(r"\d+k|\d+K", text):
        score += 10

    # Actionable signals
    action_words = ["how i", "step by step", "here's how", "tutorial",
                    "case study", "breakdown", "exactly how", "my results",
                    "i built", "i made", "launched", "first sale"]
    for word in action_words:
        if word in text:
            score += 10
            break

    # Tool/tactic signals
    tool_words = ["api", "automation", "script", "scraper", "tool",
                  "template", "framework", "system", "pipeline", "stack"]
    for word in tool_words:
        if word in text:
            score += 8
            break

    # Engagement signals (social proof)
    if post["score"] > 100:
        score += 15
    elif post["score"] > 50:
        score += 10
    elif post["score"] > 20:
        score += 5

    if post["num_comments"] > 50:
        score += 10
    elif post["num_comments"] > 20:
        score += 5

    # Recency bonus
    age_hours = (time.time() - post.get("created_utc", 0)) / 3600
    if age_hours < 24:
        score += 10
    elif age_hours < 72:
        score += 5

    # Penalty for low-effort
    if len(post["selftext"]) < 50 and post["score"] < 10:
        score -= 20

    return min(100, max(0, score))


def categorize_alpha(text):
    """Auto-categorize alpha entry."""
    text_lower = text.lower()
    categories = {
        "APP_FACTORY": ["app", "ios", "android", "aso", "app store", "mobile"],
        "CONTENT_FORMAT": ["content", "post", "thread", "video", "tiktok", "reel"],
        "OUTBOUND": ["cold email", "outreach", "dm", "lead gen", "b2b"],
        "GROWTH_HACK": ["growth", "hack", "viral", "algorithm", "organic"],
        "TOOL_ALPHA": ["tool", "software", "api", "automation", "script"],
        "MONETIZATION": ["revenue", "monetiz", "pricing", "subscription", "saas"],
        "SEO_GEO_ASO": ["seo", "keyword", "search", "rank", "backlink", "aso"],
        "ECOM": ["ecom", "shopify", "amazon", "product", "dropship", "pod"],
        "FREELANCE": ["freelance", "fiverr", "upwork", "client", "service"],
        "AFFILIATE": ["affiliate", "commission", "referral", "partner"],
    }

    for cat, keywords in categories.items():
        if any(kw in text_lower for kw in keywords):
            return cat
    return "GROWTH_HACK"


def run_reddit_scan():
    """Scan all monitored subreddits for alpha."""
    log.info(f"Scanning {len(REDDIT_TACTIC_SUBS)} subreddits...")
    all_posts = []

    for sub in REDDIT_TACTIC_SUBS:
        posts = scrape_reddit_sub(sub, sort="hot", limit=15)
        time.sleep(1.5)  # Rate limit: be respectful

        for post in posts:
            post["alpha_score"] = score_reddit_post(post)
            if post["alpha_score"] >= 30:  # Only keep promising posts
                all_posts.append(post)

        log.info(f"  r/{sub}: {len(posts)} posts, {sum(1 for p in posts if score_reddit_post(p) >= 30)} promising")

    # Sort by score
    all_posts.sort(key=lambda x: x["alpha_score"], reverse=True)

    # Save raw results
    output_file = safe_path(MONITOR_OUTPUT / f"reddit_scan_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
    with open(output_file, "w") as f:
        json.dump(all_posts, f, indent=2)

    log.info(f"Reddit scan complete: {len(all_posts)} promising posts from {len(REDDIT_TACTIC_SUBS)} subs")
    return all_posts


def run_news_scan():
    """Scan news RSS feeds for platform policy changes and opportunities."""
    log.info("Scanning news sources...")
    all_items = []

    for source_name, config in NEWS_SOURCES.items():
        if "rss" in config:
            items = scrape_rss_feed(config["rss"], config["keywords"])
            for item in items:
                item["source_name"] = source_name
            all_items.extend(items)
            log.info(f"  {source_name}: {len(items)} relevant items")
            time.sleep(1)

    # Save results
    output_file = safe_path(MONITOR_OUTPUT / f"news_scan_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
    with open(output_file, "w") as f:
        json.dump(all_items, f, indent=2)

    log.info(f"News scan complete: {len(all_items)} relevant items")
    return all_items


def append_to_alpha_staging(entries):
    """Append new alpha entries to ALPHA_STAGING.csv (canonical schema)."""
    if not entries:
        return 0

    if not ALPHA_STAGING.exists():
        log.error("ALPHA_STAGING.csv not found. Run alpha_staging_migrate.py / ensure ledger exists.")
        return 0

    # Load header and validate.
    try:
        with open(ALPHA_STAGING, "r", encoding="utf-8", errors="replace", newline="") as f:
            header = next(csv.reader(f))
    except Exception as e:
        log.error(f"ALPHA_STAGING.csv unreadable: {e}")
        return 0

    required = {"alpha_id", "source", "source_url", "category", "tactic", "roi_potential", "status", "created_at"}
    if not required.issubset(set(header)):
        log.error("ALPHA_STAGING header missing required columns. Run alpha_staging_migrate.py first.")
        return 0

    # Read existing hashes to avoid duplicates + compute max id.
    existing_hashes = set()
    max_id = 0
    with open(ALPHA_STAGING, "r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            aid = (row.get("alpha_id") or "").strip()
            m = re.match(r"ALPHA(\d+)", aid)
            if m:
                try:
                    max_id = max(max_id, int(m.group(1)))
                except Exception:
                    pass
            h = content_hash((row.get("source_url", "") or "") + (row.get("tactic", "") or "") + (row.get("source", "") or ""))
            existing_hashes.add(h)

    new_count = 0
    to_write = []

    def _priority_from_roi(roi: str) -> str:
        r = (roi or "").strip().upper()
        if r in {"HIGHEST", "HIGH"}:
            return "HIGH"
        if r == "MEDIUM":
            return "MEDIUM"
        return "LOW"

    for entry in entries:
        summary = (entry.get("summary") or entry.get("tactic") or "").strip()
        source = (entry.get("source") or "").strip()
        cat = (entry.get("category") or "GROWTH_HACK").strip()
        roi = (entry.get("roi_potential") or "MEDIUM").strip().upper()
        source_url = (entry.get("source_url") or entry.get("url") or "").strip()
        reviewer_notes = (entry.get("reviewer_notes") or "").strip()

        h = content_hash(source_url + summary + source)
        if h in existing_hashes:
            continue

        max_id += 1
        row = {k: "" for k in header}
        row["alpha_id"] = f"ALPHA{max_id}"
        row["source"] = source
        row["source_url"] = source_url
        row["category"] = cat
        row["tactic"] = summary[:500]
        row["roi_potential"] = roi
        if "priority" in row:
            row["priority"] = _priority_from_roi(roi)
        row["status"] = (entry.get("status") or "PENDING_REVIEW").strip().upper()
        if "reviewer_notes" in row:
            row["reviewer_notes"] = reviewer_notes
        row["created_at"] = datetime.now().isoformat()
        if "ops_generated" in row:
            row["ops_generated"] = "FALSE"
        if "earnings_verified" in row and not row.get("earnings_verified"):
            row["earnings_verified"] = "N/A"
        if "engagement_authenticity" in row and not row.get("engagement_authenticity"):
            row["engagement_authenticity"] = "UNKNOWN"

        to_write.append(row)
        existing_hashes.add(h)
        new_count += 1

    if not to_write:
        return 0

    with open(ALPHA_STAGING, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        writer.writerows(to_write)

    return new_count


def generate_digest(reddit_posts, news_items):
    """Generate daily monitoring digest."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    digest_path = safe_path(OPS / f"ALPHA_MONITOR_DIGEST_{date_str}.md")

    lines = [
        f"# Alpha Monitor Digest — {date_str}",
        f"",
        f"**Scan time:** {datetime.now().strftime('%H:%M')}",
        f"**Reddit posts scanned:** {len(reddit_posts)}",
        f"**News items found:** {len(news_items)}",
        f"",
        f"---",
        f"",
        f"## Top Reddit Alpha (Score >= 50)",
        f"",
    ]

    top_posts = [p for p in reddit_posts if p.get("alpha_score", 0) >= 50]
    for post in top_posts[:20]:
        lines.append(f"### [{post['title'][:80]}]({post['url']})")
        lines.append(f"**r/{post['subreddit']}** | Score: {post['score']} | "
                     f"Comments: {post['num_comments']} | Alpha: {post['alpha_score']}/100")
        if post.get("selftext"):
            lines.append(f"> {post['selftext'][:200]}...")
        lines.append("")

    if not top_posts:
        lines.append("*No posts scored >= 50 this scan*\n")

    lines.extend([
        "---",
        "",
        "## Platform & Policy News",
        "",
    ])

    for item in news_items[:15]:
        lines.append(f"- **[{item.get('source_name', 'Unknown')}]** "
                     f"[{item['title'][:80]}]({item.get('url', '')})")
        if item.get("description"):
            lines.append(f"  > {item['description'][:150]}")
        lines.append("")

    if not news_items:
        lines.append("*No relevant news items this scan*\n")

    lines.extend([
        "---",
        "",
        "## App Factory Intel",
        "",
        "### Keywords to Monitor (ASO)",
        "",
    ])
    for kw in APP_FACTORY_SOURCES["ASO_keywords"]:
        lines.append(f"- `{kw}`")

    lines.extend([
        "",
        "### Review Mining Keywords (Check App Store Reviews)",
        "",
    ])
    for kw in APP_FACTORY_SOURCES["review_mining_keywords"]:
        lines.append(f"- \"{kw}\"")

    lines.extend([
        "",
        "---",
        f"*Generated by alpha_monitor.py at {datetime.now().isoformat()}*",
    ])

    with open(digest_path, "w") as f:
        f.write("\n".join(lines))

    log.info(f"Digest written to {digest_path}")
    return digest_path


def run_full_scan():
    """Run complete monitoring scan."""
    log.info("=" * 60)
    log.info("ALPHA MONITOR — Full Scan Starting")
    log.info("=" * 60)

    # Reddit scan
    reddit_posts = run_reddit_scan()

    # News scan
    news_items = run_news_scan()

    # Convert top Reddit posts to alpha entries
    alpha_entries = []
    for post in reddit_posts:
        if post.get("alpha_score", 0) >= 40:
            alpha_entries.append({
                "source": f"r/{post['subreddit']} ({post['url']})",
                "category": categorize_alpha(f"{post['title']} {post['selftext']}"),
                "summary": f"{post['title']}. {post['selftext'][:200]}",
                "roi_potential": "HIGH" if post["alpha_score"] >= 70 else "MEDIUM",
                "alpha_score": post["alpha_score"],
                "reviewer_notes": f"Auto-scored {post['alpha_score']}/100. "
                                 f"Upvotes: {post['score']}, Comments: {post['num_comments']}",
            })

    # Convert news items to alpha entries
    for item in news_items:
        alpha_entries.append({
            "source": f"{item.get('source_name', 'News')} ({item.get('url', '')})",
            "category": "GROWTH_HACK",
            "summary": f"[PLATFORM UPDATE] {item['title']}. {item.get('description', '')}",
            "roi_potential": "MEDIUM",
            "alpha_score": 45,
            "reviewer_notes": "Auto-captured platform/policy update. Review for impact on active methods.",
        })

    # Append to staging
    new_count = append_to_alpha_staging(alpha_entries)
    log.info(f"Added {new_count} new alpha entries to ALPHA_STAGING.csv")

    # Generate digest
    digest_path = generate_digest(reddit_posts, news_items)

    # Summary
    log.info("=" * 60)
    log.info(f"SCAN COMPLETE")
    log.info(f"  Reddit: {len(reddit_posts)} promising posts from {len(REDDIT_TACTIC_SUBS)} subs")
    log.info(f"  News: {len(news_items)} relevant items")
    log.info(f"  New alpha entries: {new_count}")
    log.info(f"  Digest: {digest_path}")
    log.info("=" * 60)

    return {
        "reddit_posts": len(reddit_posts),
        "news_items": len(news_items),
        "new_alpha": new_count,
        "digest": str(digest_path),
    }


def show_status():
    """Show last scan results."""
    scan_files = sorted(MONITOR_OUTPUT.glob("reddit_scan_*.json"), reverse=True)
    news_files = sorted(MONITOR_OUTPUT.glob("news_scan_*.json"), reverse=True)

    print("=" * 50)
    print("ALPHA MONITOR STATUS")
    print("=" * 50)

    if scan_files:
        latest = scan_files[0]
        with open(latest) as f:
            data = json.load(f)
        mod_time = datetime.fromtimestamp(latest.stat().st_mtime)
        print(f"\nLast Reddit scan: {mod_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"  Posts found: {len(data)}")
        if data:
            top = data[0]
            print(f"  Top post: [{top.get('alpha_score', 0)}/100] {top['title'][:60]}")
    else:
        print("\nNo Reddit scans yet. Run: python3 alpha_monitor.py --reddit")

    if news_files:
        latest = news_files[0]
        with open(latest) as f:
            data = json.load(f)
        mod_time = datetime.fromtimestamp(latest.stat().st_mtime)
        print(f"\nLast news scan: {mod_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"  Items found: {len(data)}")
    else:
        print("\nNo news scans yet. Run: python3 alpha_monitor.py --news")

    # Alpha staging count
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING) as f:
            total = sum(1 for _ in f) - 1  # minus header
        print(f"\nTotal alpha entries: {total}")

    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Alpha Monitor")
    parser.add_argument("--full", action="store_true", help="Full scan all sources")
    parser.add_argument("--reddit", action="store_true", help="Reddit scan only")
    parser.add_argument("--forums", action="store_true", help="Forums scan only (placeholder)")
    parser.add_argument("--news", action="store_true", help="News/RSS scan only")
    parser.add_argument("--status", action="store_true", help="Show last scan results")
    parser.add_argument("--cron", action="store_true", help="Lightweight cron mode")

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.reddit:
        posts = run_reddit_scan()
        entries = []
        for p in posts:
            if p.get("alpha_score", 0) >= 40:
                entries.append({
                    "source": f"r/{p['subreddit']}",
                    "category": categorize_alpha(f"{p['title']} {p['selftext']}"),
                    "summary": f"{p['title']}. {p['selftext'][:200]}",
                    "roi_potential": "HIGH" if p["alpha_score"] >= 70 else "MEDIUM",
                    "alpha_score": p["alpha_score"],
                    "reviewer_notes": f"Score {p['alpha_score']}/100, {p['score']} upvotes",
                })
        new = append_to_alpha_staging(entries)
        print(f"Reddit scan: {len(posts)} posts, {new} new alpha entries")
    elif args.news:
        items = run_news_scan()
        entries = []
        for item in items:
            entries.append({
                "source": item.get("source_name", "News"),
                "category": "GROWTH_HACK",
                "summary": f"[PLATFORM UPDATE] {item['title']}",
                "roi_potential": "MEDIUM",
                "alpha_score": 45,
                "reviewer_notes": "Platform/policy update",
            })
        new = append_to_alpha_staging(entries)
        print(f"News scan: {len(items)} items, {new} new alpha entries")
    elif args.cron:
        # Lightweight: skip if already ran in last 3 hours
        scan_files = sorted(MONITOR_OUTPUT.glob("reddit_scan_*.json"), reverse=True)
        if scan_files:
            latest_time = datetime.fromtimestamp(scan_files[0].stat().st_mtime)
            if datetime.now() - latest_time < timedelta(hours=3):
                log.info("Skipping cron run — last scan was less than 3 hours ago")
                return
        run_full_scan()
    elif args.full:
        run_full_scan()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
