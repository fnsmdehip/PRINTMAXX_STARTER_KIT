#!/usr/bin/env python3
"""
UNIFIED ALPHA MONITOR - Consolidates ALL scattered monitoring sources from .md files
into a single daily research automation.

Covers gaps NOT handled by existing scripts:
- daily_research_pipeline.py (Twitter + Reddit + bookmarks)
- ecom_arb_engine.py (Amazon/eBay prices)
- freelance_demand_scanner.py (Reddit hiring)
- trend_aggregator.py (Google Trends + PH)

THIS script handles:
1. ASO keyword tracking for all 7 apps
2. Competitor app monitoring (pricing, features, reviews)
3. Meme coin signal aggregation
4. Growth hack forum scanning (BlackHatWorld, GrowthHackers)
5. Newsletter/community alpha extraction
6. GitHub trending repo discovery (MIT license filter)
7. Product Hunt daily launches (LIVE scrape of homepage + /all page)
8. Subreddit monitoring for app-specific niches (faith, fitness, study, biohacking)
9. Entity SEO citation monitoring (ask AI about our niches)
10. Content freshness audit (flag stale content)
11. RSS news feed monitoring (TechCrunch, The Verge, FTC.gov) for platform policy changes
12. SAM.gov / USAspending.gov federal contract opportunities (NAICS-based)
13. Acquisition opportunity scanning via Reddit + HN Algolia

Built: 2026-02-15
Updated: 2026-02-17 (PH→RSS feed, SAM.gov→USAspending fallback, Acquisitions→Reddit+HN)
Cron: 0 6 * * * python3 AUTOMATIONS/unified_alpha_monitor.py --full
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote_plus

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER = PROJECT_ROOT / "LEDGER"
OPS = PROJECT_ROOT / "OPS"
AUTOMATIONS = PROJECT_ROOT / "AUTOMATIONS"
LOGS = AUTOMATIONS / "logs"

# Ensure dirs exist
LOGS.mkdir(parents=True, exist_ok=True)

# === CONFIGURATION: ALL SOURCES FROM .MD FILE AUDIT ===

# App-specific subreddits for niche monitoring (beyond the 41 in RESEARCH_SUBREDDITS.csv)
APP_NICHE_SUBREDDITS = {
    "PrayerLock": [
        "Christianity", "PrayerRequests", "Reformed", "TrueChristian",
        "Catholicism", "MuslimLounge", "islam", "Prayer"
    ],
    "WalkToUnlock": [
        "Fitness", "loseit", "10000steps", "walking", "running",
        "C25K", "bodyweightfitness"
    ],
    "StudyLock": [
        "GetStudying", "ADHD", "productivity", "college",
        "StudyTips", "GetMotivated", "nosurf"
    ],
    "BioMaxx": [
        "Biohackers", "Nootropics", "Supplements", "StackAdvice",
        "longevity", "Peptides"
    ],
    "RamadanTracker": [
        "islam", "Ramadan", "MuslimLounge", "progressive_islam"
    ],
    "FocusLock": [
        "nosurf", "digitalminimalism", "productivity", "ADHD",
        "GetDisciplined"
    ],
    "SleepMaxx": [
        "sleep", "insomnia", "SleepApnea", "biohacking"
    ],
    "General_AppFactory": [
        "InternetIsBeautiful", "SideProject", "indiehackers",
        "AppIdeas", "iOSProgramming"
    ]
}

# ASO keywords to track per app
ASO_KEYWORDS = {
    "PrayerLock": [
        "prayer app", "daily prayer", "prayer reminder", "christian app",
        "prayer timer", "lock phone prayer", "morning prayer", "bible app"
    ],
    "WalkToUnlock": [
        "step counter", "walking app", "fitness lock", "step tracker",
        "walk to unlock", "health tracker", "pedometer", "walking challenge"
    ],
    "StudyLock": [
        "study timer", "focus app", "app blocker", "study lock",
        "pomodoro", "screen time blocker", "focus timer", "study app"
    ],
    "BioMaxx": [
        "supplement tracker", "biohacking app", "nootropic tracker",
        "supplement log", "health optimization", "protocol tracker"
    ],
    "FocusLock": [
        "focus lock", "phone lock", "app blocker", "screen time",
        "digital detox", "phone addiction", "app timer"
    ],
    "SleepMaxx": [
        "sleep tracker", "sleep app", "sleep quality", "sleep score",
        "sleep optimization", "sleep sounds", "sleep diary"
    ]
}

# Competitor apps to monitor
COMPETITOR_APPS = {
    "PrayerLock": ["Hallow", "Abide", "PrayerMate", "Glorify", "YouVersion"],
    "WalkToUnlock": ["StepBet", "Sweatcoin", "Charity Miles", "Pedometer++"],
    "StudyLock": ["Forest", "Flora", "Flipd", "One Sec", "Opal"],
    "BioMaxx": ["Zero", "Examine.com", "MyFitnessPal", "Cronometer"],
    "FocusLock": ["Forest", "Freedom", "Cold Turkey", "AppBlock"],
    "SleepMaxx": ["Calm", "Headspace", "Sleep Cycle", "Pillow", "AutoSleep"]
}

# Growth hack forums to scan
GROWTH_HACK_SOURCES = [
    {"name": "BlackHatWorld - Making Money", "url": "https://www.blackhatworld.com/forums/making-money.30/", "type": "forum"},
    {"name": "BlackHatWorld - Social Media", "url": "https://www.blackhatworld.com/forums/social-media.59/", "type": "forum"},
    {"name": "BlackHatWorld - Email Marketing", "url": "https://www.blackhatworld.com/forums/email-marketing.52/", "type": "forum"},
    {"name": "GrowthHackers", "url": "https://growthhackers.com/posts", "type": "forum"},
    {"name": "Indie Hackers", "url": "https://www.indiehackers.com/", "type": "community"},
]

# GitHub search queries for MIT repos to clone/adapt
GITHUB_SEARCHES = [
    "prayer app license:mit stars:>50",
    "fitness tracker license:mit stars:>100",
    "study timer license:mit stars:>50",
    "supplement tracker license:mit stars:>20",
    "phone lock app license:mit stars:>30",
    "sleep tracker license:mit stars:>50",
    "react native health license:mit stars:>100",
    "expo fitness license:mit stars:>50",
    "PWA productivity license:mit stars:>100",
    "saas template license:mit stars:>200",
    "cold email tool license:mit stars:>50",
    "landing page template license:mit stars:>300",
]

# Content freshness thresholds
FRESHNESS_THRESHOLDS = {
    "critical": 7,     # days - truth pages, app pages
    "high": 30,         # days - playbooks, guides
    "medium": 90,       # days - reference docs
    "low": 180          # days - strategy docs
}

# Meme coin monitoring sources
MEME_COIN_SOURCES = {
    "twitter_accounts": [
        "WatcherGuru", "lookonchain", "whale_alert", "CoinGlass_com",
        "CryptoQuant_", "IntoTheBlock", "CryptoDiffer"
    ],
    "subreddits": [
        "CryptoCurrency", "CryptoMoonShots", "SatoshiStreetBets",
        "memecoin", "solana"
    ],
    "keywords": [
        "new meme coin", "just launched", "AI agent token",
        "viral crypto", "100x potential"
    ]
}

# RSS news sources for platform policy and regulation monitoring
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


def content_hash(text):
    """Generate hash to detect duplicate entries."""
    return hashlib.md5(text.strip().lower().encode()).hexdigest()[:12]


def scrape_rss_feed(url, keywords):
    """Scrape RSS feed and filter by keywords."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PRINTMAXX-AlphaMonitor/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="replace")

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
        log(f"  Failed to scrape RSS {url}: {e}", "WARN")
        return []


def categorize_alpha(text):
    """Auto-categorize alpha entry based on keyword matching."""
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
    for cat, kws in categories.items():
        if any(kw in text_lower for kw in kws):
            return cat
    return "GROWTH_HACK"


def log(msg, level="INFO"):
    """Log to console and file."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    log_file = LOGS / f"unified_alpha_{datetime.now().strftime('%Y-%m-%d')}.log"
    with open(log_file, "a") as f:
        f.write(line + "\n")


def scan_app_subreddits():
    """Scan app-specific subreddits for mentions, questions, and opportunities."""
    log("=== SCANNING APP-SPECIFIC SUBREDDITS ===")
    results = []

    for app_name, subs in APP_NICHE_SUBREDDITS.items():
        for sub in subs:
            try:
                import requests
                # Reddit JSON API - no auth needed
                url = f"https://www.reddit.com/r/{sub}/search.json"
                params = {
                    "q": app_name.lower().replace("lock", " lock").replace("maxx", ""),
                    "sort": "new",
                    "limit": 10,
                    "t": "week",
                    "restrict_sr": "on"
                }
                headers = {"User-Agent": "PRINTMAXX-AlphaMonitor/1.0"}
                resp = requests.get(url, params=params, headers=headers, timeout=10)

                if resp.status_code == 200:
                    data = resp.json()
                    posts = data.get("data", {}).get("children", [])
                    for post in posts:
                        p = post.get("data", {})
                        results.append({
                            "app": app_name,
                            "subreddit": sub,
                            "title": p.get("title", ""),
                            "score": p.get("score", 0),
                            "url": f"https://reddit.com{p.get('permalink', '')}",
                            "created": datetime.fromtimestamp(p.get("created_utc", 0)).strftime("%Y-%m-%d"),
                            "type": "app_mention"
                        })

                time.sleep(1)  # Rate limiting

            except Exception as e:
                log(f"  Error scanning r/{sub} for {app_name}: {e}", "WARN")

    # Also search for general app category questions
    category_queries = {
        "prayer app recommendation": "PrayerLock",
        "best focus app": "FocusLock",
        "step counter app": "WalkToUnlock",
        "study timer app": "StudyLock",
        "supplement tracking app": "BioMaxx",
        "sleep tracking app": "SleepMaxx",
        "ramadan app": "RamadanTracker"
    }

    for query, app in category_queries.items():
        try:
            import requests
            url = "https://www.reddit.com/search.json"
            params = {"q": query, "sort": "new", "limit": 5, "t": "week"}
            headers = {"User-Agent": "PRINTMAXX-AlphaMonitor/1.0"}
            resp = requests.get(url, params=params, headers=headers, timeout=10)

            if resp.status_code == 200:
                data = resp.json()
                posts = data.get("data", {}).get("children", [])
                for post in posts:
                    p = post.get("data", {})
                    results.append({
                        "app": app,
                        "subreddit": p.get("subreddit", "unknown"),
                        "title": p.get("title", ""),
                        "score": p.get("score", 0),
                        "url": f"https://reddit.com{p.get('permalink', '')}",
                        "created": datetime.fromtimestamp(p.get("created_utc", 0)).strftime("%Y-%m-%d"),
                        "type": "category_question"
                    })

            time.sleep(1)

        except Exception as e:
            log(f"  Error searching for '{query}': {e}", "WARN")

    log(f"  Found {len(results)} app-related Reddit posts")
    return results


def scan_github_trending():
    """Search GitHub for MIT-licensed repos matching our app categories."""
    log("=== SCANNING GITHUB FOR CLONEABLE REPOS ===")
    results = []

    try:
        import requests
    except ImportError:
        log("requests not installed, skipping GitHub scan", "WARN")
        return results

    for query in GITHUB_SEARCHES:
        try:
            url = "https://api.github.com/search/repositories"
            params = {
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": 5
            }
            headers = {"Accept": "application/vnd.github.v3+json"}
            resp = requests.get(url, params=params, headers=headers, timeout=15)

            if resp.status_code == 200:
                data = resp.json()
                for repo in data.get("items", []):
                    # Only include recently updated repos
                    updated = repo.get("updated_at", "")
                    if updated:
                        updated_date = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                        if (datetime.now(updated_date.tzinfo) - updated_date).days > 180:
                            continue

                    results.append({
                        "name": repo.get("full_name", ""),
                        "description": repo.get("description", "")[:200],
                        "stars": repo.get("stargazers_count", 0),
                        "license": repo.get("license", {}).get("spdx_id", "unknown") if repo.get("license") else "unknown",
                        "url": repo.get("html_url", ""),
                        "updated": updated[:10] if updated else "unknown",
                        "language": repo.get("language", "unknown"),
                        "query": query
                    })

            time.sleep(2)  # GitHub rate limiting

        except Exception as e:
            log(f"  Error searching GitHub for '{query[:40]}...': {e}", "WARN")

    log(f"  Found {len(results)} relevant GitHub repos")
    return results


def audit_content_freshness():
    """Audit all content files for staleness."""
    log("=== AUDITING CONTENT FRESHNESS ===")
    stale_files = []
    now = datetime.now()

    # Directories to check with their freshness requirements
    dirs_to_check = [
        (PROJECT_ROOT / "CONTENT" / "truth_pages", "critical", 7),
        (PROJECT_ROOT / "CONTENT" / "longtail_pages", "medium", 90),
        (PROJECT_ROOT / "builds", "high", 30),
        (PROJECT_ROOT / "MONEY_METHODS" / "APP_FACTORY", "high", 30),
        (PROJECT_ROOT / "OPS", "medium", 90),
    ]

    for dir_path, priority, max_days in dirs_to_check:
        if not dir_path.exists():
            continue

        for f in dir_path.rglob("*.md"):
            try:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                days_old = (now - mtime).days

                if days_old > max_days:
                    stale_files.append({
                        "file": str(f.relative_to(PROJECT_ROOT)),
                        "days_old": days_old,
                        "max_days": max_days,
                        "priority": priority,
                        "last_modified": mtime.strftime("%Y-%m-%d")
                    })
            except Exception:
                continue

    # Sort by priority then days old
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    stale_files.sort(key=lambda x: (priority_order.get(x["priority"], 9), -x["days_old"]))

    log(f"  Found {len(stale_files)} stale content files")
    return stale_files


def scan_product_hunt():
    """Parse Product Hunt Atom RSS feed for recent launches relevant to our niches."""
    log("=== SCANNING PRODUCT HUNT (RSS FEED) ===")
    results = []

    PH_KEYWORDS = [
        "prayer", "fitness", "study", "focus", "sleep",
        "biohacking", "productivity", "habit", "fasting",
        "cold email", "seo", "content", "newsletter",
        "health", "tracking", "ai", "automation", "saas",
        "mobile app", "ios", "android", "startup", "creator",
        "supplement", "meditation", "mindfulness", "workout",
        "agent", "llm", "gpt", "claude", "monitor", "analytics",
        "email", "outreach", "crm", "landing page", "template",
    ]

    try:
        # PH homepage blocks scrapers (403), but their Atom feed is public and reliable
        req = urllib.request.Request(
            "https://www.producthunt.com/feed",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "Accept": "application/atom+xml, application/xml, text/xml",
            },
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            xml_data = resp.read().decode("utf-8", errors="replace")

        # Parse Atom feed entries
        entries = re.findall(
            r'<entry>(.*?)</entry>',
            xml_data, re.DOTALL,
        )

        for entry in entries:
            title_match = re.search(r'<title>(.*?)</title>', entry)
            link_match = re.search(r'<link[^>]*rel="alternate"[^>]*href="([^"]+)"', entry)
            content_match = re.search(r'<content[^>]*>(.*?)</content>', entry, re.DOTALL)
            published_match = re.search(r'<published>(.*?)</published>', entry)
            author_match = re.search(r'<name>(.*?)</name>', entry)
            id_match = re.search(r'Post/(\d+)', entry)

            title = title_match.group(1).strip() if title_match else ""
            url = link_match.group(1).strip() if link_match else ""
            raw_content = content_match.group(1) if content_match else ""
            published = published_match.group(1).strip() if published_match else ""
            author = author_match.group(1).strip() if author_match else ""
            post_id = id_match.group(1) if id_match else ""

            # Clean HTML from content to get tagline
            description = re.sub(r'&lt;.*?&gt;', '', raw_content)
            description = re.sub(r'<[^>]+>', '', description)
            description = re.sub(r'Discussion\s*\|\s*Link', '', description).strip()[:200]

            # Derive slug from URL
            slug = url.rstrip("/").split("/")[-1] if url else ""

            combined_text = f"{title} {description} {slug}".lower()
            matched_keywords = [kw for kw in PH_KEYWORDS if kw.lower() in combined_text]

            # Include all entries (feed is curated and not huge), flag keyword matches
            results.append({
                "name": title,
                "slug": slug,
                "url": url,
                "description": description,
                "matched_keywords": ", ".join(matched_keywords) if matched_keywords else "top_launch",
                "post_id": post_id,
                "published": published,
                "author": author,
                "source": "ProductHunt",
                "scraped_at": datetime.now().isoformat(),
            })

            if len(results) >= 40:
                break

    except Exception as e:
        log(f"  Product Hunt RSS feed failed: {e}", "WARN")

    keyword_matched = sum(1 for r in results if r.get("matched_keywords") != "top_launch")
    log(f"  Product Hunt: {len(results)} launches found ({keyword_matched} keyword-matched)")
    return results


def scan_samgov_contracts():
    """Query SAM.gov API for small business contract opportunities.

    Requires SAM_GOV_API_KEY env var (free at https://sam.gov/content/entity-registration).
    Without API key, falls back to USAspending.gov public API (no key needed).
    """
    log("=== SCANNING SAM.GOV CONTRACTS ===")
    results = []

    SAM_QUERIES = [
        {"keyword": "mobile application development", "naics": "541511"},
        {"keyword": "website development", "naics": "541511"},
        {"keyword": "social media management", "naics": "541613"},
        {"keyword": "digital marketing", "naics": "541810"},
        {"keyword": "software development", "naics": "541511"},
        {"keyword": "IT support services", "naics": "541512"},
        {"keyword": "graphic design", "naics": "541430"},
    ]

    api_key = os.environ.get("SAM_GOV_API_KEY", "")

    if api_key:
        # With API key, use the official SAM.gov Opportunities API
        SAM_API_BASE = "https://api.sam.gov/opportunities/v2/search"
        for query_config in SAM_QUERIES:
            try:
                kw = query_config["keyword"]
                params = {
                    "api_key": api_key,
                    "limit": "10",
                    "postedFrom": (datetime.now() - timedelta(days=14)).strftime("%m/%d/%Y"),
                    "postedTo": datetime.now().strftime("%m/%d/%Y"),
                    "ptype": "o",
                    "title": kw,
                }
                param_str = "&".join(f"{k}={quote_plus(str(v))}" for k, v in params.items())
                url = f"{SAM_API_BASE}?{param_str}"

                req = urllib.request.Request(url, headers={
                    "User-Agent": "PRINTMAXX-AlphaMonitor/1.0",
                    "Accept": "application/json",
                })
                with urllib.request.urlopen(req, timeout=20) as resp:
                    data = json.loads(resp.read().decode("utf-8"))

                for opp in data.get("opportunitiesData", []):
                    results.append({
                        "title": opp.get("title", "")[:200],
                        "solicitation_number": opp.get("solicitationNumber", ""),
                        "opportunity_id": opp.get("noticeId", ""),
                        "url": opp.get("uiLink", f"https://sam.gov/opp/{opp.get('noticeId', '')}/view"),
                        "keyword": kw,
                        "naics": query_config.get("naics", ""),
                        "posted_date": opp.get("postedDate", ""),
                        "response_deadline": opp.get("responseDeadLine", ""),
                        "set_aside": opp.get("typeOfSetAside", ""),
                        "department": (opp.get("fullParentPathName", "") or "")[:100],
                        "source": "SAM.gov",
                        "scraped_at": datetime.now().isoformat(),
                    })
                time.sleep(1)
            except Exception as e:
                log(f"  SAM.gov API query '{kw}' failed: {e}", "WARN")
    else:
        # Fallback: USAspending.gov public API (no key needed)
        # Searches recent federal awards related to our NAICS codes
        log("  No SAM_GOV_API_KEY set. Using USAspending.gov fallback (no key needed)")
        log("  To enable SAM.gov: register free at https://sam.gov/content/entity-registration")

        usa_spending_url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
        naics_codes = list(set(q["naics"] for q in SAM_QUERIES))

        for naics in naics_codes:
            try:
                payload = json.dumps({
                    "filters": {
                        "time_period": [{"start_date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                                         "end_date": datetime.now().strftime("%Y-%m-%d")}],
                        "award_type_codes": ["A", "B", "C", "D"],  # Contracts
                        "naics_codes": {"require": [naics]},
                    },
                    "fields": ["Award ID", "Recipient Name", "Description", "Award Amount",
                               "Awarding Agency", "Start Date", "End Date"],
                    "limit": 10,
                    "page": 1,
                    "sort": "Award Amount",
                    "order": "desc",
                }).encode("utf-8")

                req = urllib.request.Request(
                    usa_spending_url,
                    data=payload,
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "PRINTMAXX-AlphaMonitor/1.0",
                    },
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=20) as resp:
                    data = json.loads(resp.read().decode("utf-8"))

                for award in data.get("results", []):
                    desc = award.get("Description", "") or ""
                    results.append({
                        "title": desc[:200] if desc else f"NAICS {naics} Award",
                        "opportunity_id": award.get("Award ID", ""),
                        "url": f"https://www.usaspending.gov/award/{award.get('internal_id', '')}",
                        "keyword": f"NAICS {naics}",
                        "naics": naics,
                        "posted_date": award.get("Start Date", ""),
                        "response_deadline": award.get("End Date", ""),
                        "set_aside": "",
                        "department": (award.get("Awarding Agency", "") or "")[:100],
                        "award_amount": award.get("Award Amount", ""),
                        "recipient": (award.get("Recipient Name", "") or "")[:100],
                        "source": "USAspending.gov",
                        "scraped_at": datetime.now().isoformat(),
                    })
                time.sleep(1)
            except Exception as e:
                log(f"  USAspending NAICS {naics} query failed: {e}", "WARN")

    # Deduplicate by opportunity ID
    seen_ids = set()
    deduped = []
    for r in results:
        oid = r.get("opportunity_id", "") or content_hash(r.get("title", ""))
        if oid not in seen_ids:
            seen_ids.add(oid)
            deduped.append(r)

    log(f"  SAM.gov/USAspending: {len(deduped)} contract opportunities found")
    return deduped


def scan_acquisitions():
    """Scan for acquisition opportunities via Reddit r/SideProject, r/MicroSaaS, and HN.

    Acquire.com and Flippa are JS-rendered SPAs that block urllib scrapers.
    Instead we scan Reddit communities where founders sell businesses directly,
    plus Hacker News for Show HN / acquisition posts.
    """
    log("=== SCANNING ACQUISITION OPPORTUNITIES ===")
    results = []

    ACQUISITION_KEYWORDS = [
        "saas", "app", "mobile", "ios", "android",
        "newsletter", "content", "community", "marketplace",
        "ecommerce", "shopify", "affiliate", "automation",
        "ai", "subscription", "productized service", "mrr",
        "selling", "for sale", "acquire", "buy", "revenue",
    ]

    # --- Reddit: communities where people sell side projects ---
    reddit_sources = [
        ("r/SideProject", "https://www.reddit.com/r/SideProject/new.json?limit=25"),
        ("r/microsaas", "https://www.reddit.com/r/microsaas/new.json?limit=25"),
        ("r/indiehackers", "https://www.reddit.com/r/indiehackers/new.json?limit=15"),
        ("r/startups", "https://www.reddit.com/r/startups/search.json?q=selling+OR+sale+OR+acquire&restrict_sr=on&sort=new&limit=15"),
    ]

    for source_name, url in reddit_sources:
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "PRINTMAXX-AlphaMonitor/1.0 (by /u/printmaxxer)",
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            posts = data.get("data", {}).get("children", [])
            for post in posts:
                pdata = post.get("data", {})
                title = pdata.get("title", "")
                selftext = pdata.get("selftext", "")[:300]
                permalink = pdata.get("permalink", "")
                score = pdata.get("score", 0)
                created = pdata.get("created_utc", 0)

                combined = f"{title} {selftext}".lower()

                # Check for sale/acquisition signals
                sale_signals = ["for sale", "selling my", "looking to sell", "want to buy",
                                "acquire", "acquisition", "mrr", "arr", "revenue",
                                "profitable", "selling a", "buy my"]
                is_sale = any(sig in combined for sig in sale_signals)

                matched = [kw for kw in ACQUISITION_KEYWORDS if kw in combined]

                if is_sale or len(matched) >= 2:
                    # Extract revenue/price mentions
                    revenue_match = re.search(r'\$[\d,]+(?:\.\d+)?(?:\s*/\s*(?:mo|month|yr|year))?', combined)
                    price_match = re.search(r'(?:asking|price|selling for)\s*\$?([\d,]+)', combined, re.IGNORECASE)

                    results.append({
                        "title": title[:200],
                        "url": f"https://www.reddit.com{permalink}",
                        "revenue": revenue_match.group(0) if revenue_match else "",
                        "asking_price": price_match.group(1) if price_match else "",
                        "matched_keywords": ", ".join(matched) if matched else "sale_signal",
                        "is_sale_post": is_sale,
                        "score": score,
                        "source": source_name,
                        "scraped_at": datetime.now().isoformat(),
                    })
            time.sleep(1)
        except Exception as e:
            log(f"  {source_name} scrape failed: {e}", "WARN")

    # --- Hacker News: Show HN posts about acquisitions/launches ---
    try:
        # HN Algolia API for recent "Show HN" and acquisition posts
        hn_queries = ["Show HN selling", "acquired my", "selling my saas", "for sale side project"]
        for q in hn_queries:
            hn_url = f"https://hn.algolia.com/api/v1/search_by_date?query={quote_plus(q)}&tags=story&numericFilters=created_at_i>{int(time.time()) - 14*86400}&hitsPerPage=10"
            req = urllib.request.Request(hn_url, headers={"User-Agent": "PRINTMAXX/1.0"})
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                for hit in data.get("hits", []):
                    title = hit.get("title", "")
                    story_url = hit.get("url", "") or f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}"
                    points = hit.get("points", 0)
                    combined = title.lower()
                    matched = [kw for kw in ACQUISITION_KEYWORDS if kw in combined]
                    if matched or points > 5:
                        results.append({
                            "title": title[:200],
                            "url": story_url,
                            "revenue": "",
                            "asking_price": "",
                            "matched_keywords": ", ".join(matched) if matched else "hn_post",
                            "score": points,
                            "source": "HackerNews",
                            "scraped_at": datetime.now().isoformat(),
                        })
            except Exception:
                pass
            time.sleep(0.5)
    except Exception as e:
        log(f"  HN acquisition scrape failed: {e}", "WARN")

    # Deduplicate by URL hash
    seen_hashes = set()
    deduped = []
    for r in results:
        h = content_hash(r.get("url", "") + r.get("title", ""))
        if h not in seen_hashes:
            seen_hashes.add(h)
            deduped.append(r)

    log(f"  Acquisitions: {len(deduped)} listings found (Reddit + HN)")
    return deduped


def scan_news_feeds():
    """Scan RSS news feeds for platform policy changes and opportunities."""
    log("=== SCANNING NEWS RSS FEEDS ===")
    all_items = []

    for source_name, config in NEWS_SOURCES.items():
        if "rss" in config:
            items = scrape_rss_feed(config["rss"], config["keywords"])
            for item in items:
                item["source_name"] = source_name
            all_items.extend(items)
            log(f"  {source_name}: {len(items)} relevant items")
            time.sleep(1)

    log(f"  News scan complete: {len(all_items)} relevant items")
    return all_items


def generate_aso_report():
    """Generate ASO keyword tracking report for all apps."""
    log("=== GENERATING ASO KEYWORD REPORT ===")
    report = []

    for app_name, keywords in ASO_KEYWORDS.items():
        for kw in keywords:
            report.append({
                "app": app_name,
                "keyword": kw,
                "status": "TRACKING",
                "note": "Manual check in App Store Connect / Sensor Tower"
            })

    log(f"  Tracking {len(report)} ASO keywords across {len(ASO_KEYWORDS)} apps")
    return report


def scan_competitor_apps():
    """Check competitor apps for pricing/feature changes."""
    log("=== SCANNING COMPETITOR APPS ===")
    results = []

    for app_name, competitors in COMPETITOR_APPS.items():
        for comp in competitors:
            results.append({
                "our_app": app_name,
                "competitor": comp,
                "check": "pricing_features_reviews",
                "frequency": "weekly",
                "tool": "AppFollow free tier or manual App Store check"
            })

    log(f"  Monitoring {len(results)} competitor apps across {len(COMPETITOR_APPS)} categories")
    return results


def aggregate_meme_signals():
    """Aggregate meme coin signals from configured sources."""
    log("=== CHECKING MEME COIN SIGNALS ===")
    results = []

    # Check if meme coin signal tracker exists and has recent data
    signals_file = LEDGER / "MEME_COIN_SIGNALS.csv"
    watchlist_file = LEDGER / "MEME_COIN_WATCHLIST.csv"

    if signals_file.exists():
        try:
            with open(signals_file) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    results.append(row)
            log(f"  Found {len(results)} existing meme coin signals")
        except Exception as e:
            log(f"  Error reading meme signals: {e}", "WARN")
    else:
        log("  No meme coin signals file found. Run meme_coin_signal_tracker.py first.", "WARN")

    return results


def generate_daily_digest(app_reddit, github_repos, stale_content, aso_report, competitor_report, meme_signals, news_items=None,
                          ph_launches=None, samgov_contracts=None, acquisitions=None):
    """Generate the unified daily alpha digest."""
    log("=== GENERATING DAILY DIGEST ===")

    date_str = datetime.now().strftime("%Y_%m_%d")
    digest_path = OPS / f"UNIFIED_ALPHA_DIGEST_{date_str}.md"

    lines = [
        f"# Unified Alpha Monitor Digest",
        f"",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"",
        f"---",
        f"",
    ]

    # Section 1: App-specific Reddit activity
    lines.append("## 1. App-Specific Reddit Activity")
    lines.append("")

    if app_reddit:
        # Group by app
        by_app = {}
        for r in app_reddit:
            app = r.get("app", "Unknown")
            if app not in by_app:
                by_app[app] = []
            by_app[app].append(r)

        for app, posts in by_app.items():
            lines.append(f"### {app} ({len(posts)} mentions)")
            lines.append("")
            for p in sorted(posts, key=lambda x: x.get("score", 0), reverse=True)[:5]:
                lines.append(f"- **r/{p['subreddit']}** (score: {p['score']}) [{p['type']}]")
                lines.append(f"  {p['title'][:100]}")
                lines.append(f"  {p['url']}")
                lines.append("")
    else:
        lines.append("No app-specific Reddit activity found this scan.")
        lines.append("")

    # Section 2: GitHub repos
    lines.append("## 2. Cloneable GitHub Repos (MIT)")
    lines.append("")

    if github_repos:
        for r in sorted(github_repos, key=lambda x: x.get("stars", 0), reverse=True)[:15]:
            lines.append(f"- **[{r['name']}]({r['url']})** ({r['stars']} stars, {r['language']})")
            lines.append(f"  {r['description']}")
            lines.append(f"  License: {r['license']} | Updated: {r['updated']} | Query: {r['query'][:40]}")
            lines.append("")
    else:
        lines.append("No new GitHub repos found this scan.")
        lines.append("")

    # Section 3: Stale content
    lines.append("## 3. Content Freshness Audit")
    lines.append("")

    if stale_content:
        critical = [f for f in stale_content if f["priority"] == "critical"]
        high = [f for f in stale_content if f["priority"] == "high"]

        if critical:
            lines.append(f"### CRITICAL ({len(critical)} files > {FRESHNESS_THRESHOLDS['critical']} days old)")
            lines.append("")
            for f in critical[:10]:
                lines.append(f"- `{f['file']}` ({f['days_old']}d old, last: {f['last_modified']})")
            lines.append("")

        if high:
            lines.append(f"### HIGH ({len(high)} files > {FRESHNESS_THRESHOLDS['high']} days old)")
            lines.append("")
            for f in high[:10]:
                lines.append(f"- `{f['file']}` ({f['days_old']}d old, last: {f['last_modified']})")
            lines.append("")

        lines.append(f"**Total stale files:** {len(stale_content)}")
        lines.append("")
    else:
        lines.append("All content is fresh.")
        lines.append("")

    # Section 4: ASO tracking summary
    lines.append("## 4. ASO Keyword Tracking")
    lines.append("")
    lines.append(f"Tracking {len(aso_report)} keywords across {len(ASO_KEYWORDS)} apps.")
    lines.append("")
    lines.append("| App | Keywords Tracked |")
    lines.append("|-----|-----------------|")
    for app, kws in ASO_KEYWORDS.items():
        lines.append(f"| {app} | {', '.join(kws[:3])}... ({len(kws)} total) |")
    lines.append("")
    lines.append("**Action:** Check App Store Connect weekly for ranking changes.")
    lines.append("")

    # Section 5: Competitor monitoring
    lines.append("## 5. Competitor App Monitoring")
    lines.append("")
    lines.append(f"Monitoring {len(competitor_report)} competitor apps.")
    lines.append("")
    for app, comps in COMPETITOR_APPS.items():
        lines.append(f"- **{app}**: {', '.join(comps)}")
    lines.append("")
    lines.append("**Action:** Weekly check for pricing changes, new features, new reviews.")
    lines.append("")

    # Section 6: Meme coin signals
    lines.append("## 6. Meme Coin Signal Summary")
    lines.append("")
    if meme_signals:
        lines.append(f"Active signals: {len(meme_signals)}")
        for s in meme_signals[:5]:
            lines.append(f"- {s}")
    else:
        lines.append("No active meme coin signals. Run `python3 AUTOMATIONS/meme_coin_signal_tracker.py` for detection.")
    lines.append("")

    # Section 7: Platform & Policy News
    lines.append("## 7. Platform & Policy News (RSS)")
    lines.append("")

    if news_items:
        for item in news_items[:15]:
            lines.append(f"- **[{item.get('source_name', 'Unknown')}]** "
                         f"[{item['title'][:80]}]({item.get('url', '')})")
            if item.get("description"):
                lines.append(f"  > {item['description'][:150]}")
            lines.append("")
        lines.append(f"**Total news items:** {len(news_items)}")
        lines.append("")
    else:
        lines.append("No relevant platform/policy news this scan.")
        lines.append("")

    # Section 8: Product Hunt Launches
    lines.append("## 8. Product Hunt Launches")
    lines.append("")

    if ph_launches:
        for launch in ph_launches[:15]:
            name = launch.get("name", "Unknown")
            url = launch.get("url", "")
            desc = launch.get("description", "")
            matched = launch.get("matched_keywords", "")
            lines.append(f"- **[{name}]({url})** [{matched}]")
            if desc:
                lines.append(f"  > {desc[:120]}")
            lines.append("")
        lines.append(f"**Total PH launches found:** {len(ph_launches)}")
        lines.append("")
    else:
        lines.append("No Product Hunt launches scraped this scan.")
        lines.append("")

    # Section 9: SAM.gov Government Contracts
    lines.append("## 9. SAM.gov Government Contracts")
    lines.append("")

    if samgov_contracts:
        for contract in samgov_contracts[:15]:
            title = contract.get("title", "Unknown")
            url = contract.get("url", "")
            kw = contract.get("keyword", "")
            deadline = contract.get("response_deadline", "")
            set_aside = contract.get("set_aside", "")
            deadline_str = f" | Deadline: {deadline}" if deadline else ""
            aside_str = f" | Set-aside: {set_aside}" if set_aside else ""
            lines.append(f"- **[{title[:80]}]({url})**")
            lines.append(f"  Keyword: {kw}{deadline_str}{aside_str}")
            lines.append("")
        lines.append(f"**Total contracts found:** {len(samgov_contracts)}")
        lines.append("")
    else:
        lines.append("No SAM.gov contract opportunities found this scan.")
        lines.append("")

    # Section 10: Acquisition Opportunities
    lines.append("## 10. Acquisition Opportunities (Reddit + HN)")
    lines.append("")

    if acquisitions:
        for listing in acquisitions[:15]:
            title = listing.get("title", "Unknown")
            url = listing.get("url", "")
            revenue = listing.get("revenue", "")
            price = listing.get("asking_price", "")
            source = listing.get("source", "")
            rev_str = f" | Revenue: ${revenue}" if revenue else ""
            price_str = f" | Asking: ${price}" if price else ""
            lines.append(f"- **[{title[:80]}]({url})** [{source}]")
            if rev_str or price_str:
                lines.append(f"  {rev_str}{price_str}")
            lines.append("")
        lines.append(f"**Total listings found:** {len(acquisitions)}")
        lines.append("")
    else:
        lines.append("No acquisition listings found this scan.")
        lines.append("")

    # Section 11: Action items
    lines.append("## 11. Recommended Actions")
    lines.append("")

    actions = []

    # Reddit opportunities
    high_score_posts = [p for p in app_reddit if p.get("score", 0) > 10 and p.get("type") == "category_question"]
    if high_score_posts:
        actions.append(f"REPLY to {len(high_score_posts)} high-score Reddit posts asking about our app categories (value-first, no promo)")

    # GitHub repos
    high_star_repos = [r for r in github_repos if r.get("stars", 0) > 200]
    if high_star_repos:
        actions.append(f"EVALUATE {len(high_star_repos)} high-star MIT repos for clone/adapt potential")

    # Stale content
    critical_stale = [f for f in stale_content if f["priority"] == "critical"]
    if critical_stale:
        actions.append(f"REFRESH {len(critical_stale)} critically stale content files (>7 days old)")

    # News-related actions
    if news_items:
        policy_items = [i for i in news_items if any(kw in i.get("title", "").lower() for kw in ["policy", "regulation", "ban", "ftc", "enforcement"])]
        if policy_items:
            actions.append(f"REVIEW {len(policy_items)} platform policy/regulation updates for impact on active methods")

    # Product Hunt actions
    if ph_launches:
        actions.append(f"EVALUATE {len(ph_launches)} Product Hunt launches for competitive intel or clone opportunities")

    # SAM.gov actions
    if samgov_contracts:
        actions.append(f"REVIEW {len(samgov_contracts)} gov contract opportunities for freelance/agency bid potential")

    # Acquisition actions
    if acquisitions:
        actions.append(f"SCAN {len(acquisitions)} acquisition listings for underpriced SaaS/app buy opportunities")

    # Default actions
    actions.extend([
        "RUN meme_coin_signal_tracker.py if crypto market is active",
        "CHECK competitor apps for pricing changes this week",
        "UPDATE ASO keywords in App Store Connect based on trending terms",
        "SCAN BlackHatWorld for new legal growth tactics",
    ])

    for i, action in enumerate(actions, 1):
        lines.append(f"{i}. {action}")
    lines.append("")

    # Write digest
    with open(digest_path, "w") as f:
        f.write("\n".join(lines))

    log(f"  Digest written to {digest_path}")
    return digest_path


def append_to_alpha_staging(app_reddit, github_repos, news_items=None,
                            ph_launches=None, samgov_contracts=None, acquisitions=None):
    """Append new findings to ALPHA_STAGING.csv using the canonical schema."""
    staging_file = LEDGER / "ALPHA_STAGING.csv"

    if not staging_file.exists():
        log("ALPHA_STAGING.csv not found, skipping append", "WARN")
        return

    # Read header and sanity-check.
    try:
        with open(staging_file, "r", encoding="utf-8", errors="replace", newline="") as f:
            header = next(csv.reader(f))
    except Exception as e:
        log(f"ALPHA_STAGING.csv unreadable: {e}", "ERROR")
        return

    required = {"alpha_id", "source", "source_url", "category", "tactic", "roi_potential", "status", "created_at"}
    if not required.issubset(set(header)):
        log("ALPHA_STAGING header missing required columns. Run alpha_staging_migrate.py first.", "ERROR")
        return

    # Get highest existing alpha_id and collect existing hashes for dedup.
    max_id = 0
    existing_hashes = set()
    try:
        with open(staging_file, "r", encoding="utf-8", errors="replace", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                aid = row.get("alpha_id", "") or ""
                m = re.match(r"ALPHA(\d+)", aid.strip())
                if m:
                    max_id = max(max_id, int(m.group(1)))
                # Dedup: source_url + tactic + source.
                h = content_hash((row.get("source_url", "") or "") + (row.get("tactic", "") or "") + (row.get("source", "") or ""))
                existing_hashes.add(h)
    except Exception:
        max_id = 999

    def _priority_from_roi(roi: str) -> str:
        r = (roi or "").strip().upper()
        if r in {"HIGHEST", "HIGH"}:
            return "HIGH"
        if r == "MEDIUM":
            return "MEDIUM"
        return "LOW"

    def _make_row(*, alpha_id: str, source: str, source_url: str, category: str, tactic: str, roi: str, reviewer_notes: str) -> dict:
        row = {k: "" for k in header}
        row["alpha_id"] = alpha_id
        row["source"] = source
        row["source_url"] = source_url
        row["category"] = category
        row["tactic"] = tactic
        row["roi_potential"] = roi
        if "priority" in row:
            row["priority"] = _priority_from_roi(roi)
        row["status"] = "PENDING_REVIEW"
        if "reviewer_notes" in row:
            row["reviewer_notes"] = reviewer_notes
        row["created_at"] = datetime.now().isoformat()
        if "ops_generated" in row:
            row["ops_generated"] = "FALSE"
        if "earnings_verified" in row and not row.get("earnings_verified"):
            row["earnings_verified"] = "N/A"
        if "engagement_authenticity" in row and not row.get("engagement_authenticity"):
            row["engagement_authenticity"] = "UNKNOWN"
        return row

    new_rows: list[dict] = []

    # High-value Reddit posts (category questions with score > 5)
    for post in app_reddit:
        if post.get("type") != "category_question":
            continue
        if post.get("score", 0) <= 5:
            continue

        tactic = f"[{post['app']}] Reddit opportunity: {post['title'][:160]}"
        source = f"r/{post['subreddit']}"
        source_url = post.get("url", "") or ""
        roi = "MEDIUM"
        h = content_hash(source_url + tactic + source)
        if h in existing_hashes:
            continue
        max_id += 1
        reviewer_notes = f"unified_alpha_monitor: reddit score={post.get('score', 0)}; reply with value-first content."
        new_rows.append(
            _make_row(
                alpha_id=f"ALPHA{max_id}",
                source=source,
                source_url=source_url,
                category="APP_FACTORY",
                tactic=tactic,
                roi=roi,
                reviewer_notes=reviewer_notes,
            )
        )
        existing_hashes.add(h)

    # High-star GitHub repos
    for repo in github_repos:
        if repo.get("stars", 0) <= 100:
            continue
        tactic = f"MIT repo: {repo['name']} ({repo['stars']} stars, {repo['language']})"
        source = "GitHub"
        source_url = repo.get("url", "") or ""
        roi = "HIGH"
        h = content_hash(source_url + tactic + source)
        if h in existing_hashes:
            continue
        max_id += 1
        reviewer_notes = f"unified_alpha_monitor: license={repo.get('license','')}; query={str(repo.get('query',''))[:60]}; evaluate for clone/adapt."
        new_rows.append(
            _make_row(
                alpha_id=f"ALPHA{max_id}",
                source=source,
                source_url=source_url,
                category="TOOL_ALPHA",
                tactic=tactic,
                roi=roi,
                reviewer_notes=reviewer_notes,
            )
        )
        existing_hashes.add(h)

    # News/platform policy items
    if news_items:
        for item in news_items:
            title = f"[PLATFORM UPDATE] {item['title'][:160]}"
            source = item.get("source_name", "News")
            source_url = item.get("url", "") or ""
            cat = categorize_alpha(f"{item.get('title','')} {item.get('description','')}")
            roi = "MEDIUM"
            h = content_hash(source_url + title + source)
            if h in existing_hashes:
                continue
            max_id += 1
            reviewer_notes = "unified_alpha_monitor: platform/policy update; review impact on active methods."
            new_rows.append(
                _make_row(
                    alpha_id=f"ALPHA{max_id}",
                    source=f"{source} ({source_url})" if source_url else source,
                    source_url=source_url,
                    category=cat,
                    tactic=title,
                    roi=roi,
                    reviewer_notes=reviewer_notes,
                )
            )
            existing_hashes.add(h)

    # Product Hunt launches
    if ph_launches:
        for launch in ph_launches:
            name = launch.get("name", "")
            slug = launch.get("slug", "")
            desc = launch.get("description", "")
            matched = launch.get("matched_keywords", "")
            tactic = f"[PH LAUNCH] {name}: {desc[:120]}" if desc else f"[PH LAUNCH] {name} ({matched})"
            source = launch.get("source", "ProductHunt")
            source_url = launch.get("url", "") or ""
            roi = "MEDIUM"
            h = content_hash(source_url + tactic + source)
            if h in existing_hashes:
                continue
            max_id += 1
            reviewer_notes = f"unified_alpha_monitor: PH launch; keywords={matched}; evaluate for competitive intel or clone opportunity."
            new_rows.append(
                _make_row(
                    alpha_id=f"ALPHA{max_id}",
                    source=source,
                    source_url=source_url,
                    category=categorize_alpha(f"{name} {desc} {matched}"),
                    tactic=tactic,
                    roi=roi,
                    reviewer_notes=reviewer_notes,
                )
            )
            existing_hashes.add(h)

    # SAM.gov contract opportunities
    if samgov_contracts:
        for contract in samgov_contracts:
            title = contract.get("title", "")
            kw = contract.get("keyword", "")
            deadline = contract.get("response_deadline", "")
            set_aside = contract.get("set_aside", "")
            tactic = f"[GOV CONTRACT] {title[:140]}"
            if deadline:
                tactic += f" (deadline: {deadline})"
            source = "SAM.gov"
            source_url = contract.get("url", "") or ""
            roi = "HIGH"
            h = content_hash(source_url + tactic + source)
            if h in existing_hashes:
                continue
            max_id += 1
            naics = contract.get("naics", "")
            reviewer_notes = (
                f"unified_alpha_monitor: gov contract; keyword={kw}; NAICS={naics}; "
                f"set_aside={set_aside}; evaluate for freelance/agency bid opportunity."
            )
            new_rows.append(
                _make_row(
                    alpha_id=f"ALPHA{max_id}",
                    source=source,
                    source_url=source_url,
                    category="FREELANCE",
                    tactic=tactic,
                    roi=roi,
                    reviewer_notes=reviewer_notes,
                )
            )
            existing_hashes.add(h)

    # Acquisition opportunities (Reddit + HN)
    if acquisitions:
        for listing in acquisitions:
            title = listing.get("title", "")
            revenue = listing.get("revenue", "")
            price = listing.get("asking_price", "")
            matched = listing.get("matched_keywords", "")
            price_str = f" (asking: ${price})" if price else ""
            rev_str = f" [rev: ${revenue}]" if revenue else ""
            tactic = f"[ACQUISITION] {title[:120]}{rev_str}{price_str}"
            source = listing.get("source", "Acquire.com")
            source_url = listing.get("url", "") or ""
            roi = "HIGH" if revenue else "MEDIUM"
            h = content_hash(source_url + tactic + source)
            if h in existing_hashes:
                continue
            max_id += 1
            reviewer_notes = (
                f"unified_alpha_monitor: acquisition listing; keywords={matched}; "
                f"evaluate for buy opportunity or competitive intel."
            )
            new_rows.append(
                _make_row(
                    alpha_id=f"ALPHA{max_id}",
                    source=source,
                    source_url=source_url,
                    category="MONETIZATION",
                    tactic=tactic,
                    roi=roi,
                    reviewer_notes=reviewer_notes,
                )
            )
            existing_hashes.add(h)

    if not new_rows:
        return

    try:
        with open(staging_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
            writer.writerows(new_rows)
        log(f"  Appended {len(new_rows)} new entries to ALPHA_STAGING.csv (deduped)")
    except Exception as e:
        log(f"  Error appending to ALPHA_STAGING: {e}", "ERROR")


def run_full_scan():
    """Run all monitoring modules."""
    log("=" * 60)
    log("UNIFIED ALPHA MONITOR - FULL SCAN STARTING")
    log("=" * 60)

    start = time.time()

    # 1. App-specific Reddit scanning
    app_reddit = scan_app_subreddits()

    # 2. GitHub trending repos
    github_repos = scan_github_trending()

    # 3. Content freshness audit
    stale_content = audit_content_freshness()

    # 4. ASO keyword report
    aso_report = generate_aso_report()

    # 5. Competitor app monitoring
    competitor_report = scan_competitor_apps()

    # 6. Meme coin signals
    meme_signals = aggregate_meme_signals()

    # 7. RSS news feed scanning
    news_items = scan_news_feeds()

    # 8. Product Hunt launches
    ph_launches = scan_product_hunt()

    # 9. SAM.gov / USAspending government contracts
    samgov_contracts = scan_samgov_contracts()

    # 10. Acquisition opportunities (Reddit + HN)
    acquisitions = scan_acquisitions()

    # 11. Generate daily digest
    digest_path = generate_daily_digest(
        app_reddit, github_repos, stale_content,
        aso_report, competitor_report, meme_signals, news_items,
        ph_launches, samgov_contracts, acquisitions
    )

    # 12. Append high-value findings to ALPHA_STAGING.csv
    append_to_alpha_staging(
        app_reddit, github_repos, news_items,
        ph_launches, samgov_contracts, acquisitions
    )

    elapsed = time.time() - start

    log("=" * 60)
    log(f"SCAN COMPLETE in {elapsed:.1f}s")
    log(f"  Reddit posts: {len(app_reddit)}")
    log(f"  GitHub repos: {len(github_repos)}")
    log(f"  News items: {len(news_items)}")
    log(f"  PH launches: {len(ph_launches)}")
    log(f"  SAM.gov contracts: {len(samgov_contracts)}")
    log(f"  Acquisitions: {len(acquisitions)}")
    log(f"  Stale files: {len(stale_content)}")
    log(f"  ASO keywords: {len(aso_report)}")
    log(f"  Competitors: {len(competitor_report)}")
    log(f"  Digest: {digest_path}")
    log("=" * 60)

    return {
        "reddit_posts": len(app_reddit),
        "github_repos": len(github_repos),
        "news_items": len(news_items),
        "ph_launches": len(ph_launches),
        "samgov_contracts": len(samgov_contracts),
        "acquisitions": len(acquisitions),
        "stale_files": len(stale_content),
        "aso_keywords": len(aso_report),
        "competitors": len(competitor_report),
        "digest": str(digest_path)
    }


def run_quick_scan():
    """Quick scan - only Reddit + content freshness."""
    log("UNIFIED ALPHA MONITOR - QUICK SCAN")

    stale = audit_content_freshness()
    critical = [f for f in stale if f["priority"] == "critical"]

    if critical:
        log(f"  WARNING: {len(critical)} critically stale content files!")
        for f in critical[:5]:
            log(f"    - {f['file']} ({f['days_old']}d old)")
    else:
        log("  All critical content is fresh.")

    log(f"  Total stale files: {len(stale)}")


def show_status():
    """Show current monitoring status."""
    print("\n=== UNIFIED ALPHA MONITOR STATUS ===\n")

    # Check last digest
    digests = sorted(OPS.glob("UNIFIED_ALPHA_DIGEST_*.md"), reverse=True)
    if digests:
        latest = digests[0]
        mtime = datetime.fromtimestamp(latest.stat().st_mtime)
        age = (datetime.now() - mtime).total_seconds() / 3600
        print(f"Last digest: {latest.name} ({age:.1f}h ago)")
    else:
        print("Last digest: NONE (run --full first)")

    # Check cron scheduling
    print(f"\nMonitoring scope:")
    print(f"  Subreddits (app-specific): {sum(len(v) for v in APP_NICHE_SUBREDDITS.values())}")
    print(f"  ASO keywords: {sum(len(v) for v in ASO_KEYWORDS.values())}")
    print(f"  Competitor apps: {sum(len(v) for v in COMPETITOR_APPS.values())}")
    print(f"  GitHub search queries: {len(GITHUB_SEARCHES)}")
    print(f"  Meme coin sources: {len(MEME_COIN_SOURCES['twitter_accounts'])} Twitter + {len(MEME_COIN_SOURCES['subreddits'])} subreddits")
    print(f"  Growth hack forums: {len(GROWTH_HACK_SOURCES)}")
    print(f"  News RSS feeds: {len([s for s in NEWS_SOURCES.values() if 'rss' in s])}")
    print(f"  Product Hunt: Atom RSS feed (keyword-matched launches)")
    print(f"  SAM.gov/USAspending: Federal contract opportunities (NAICS-based)")
    print(f"  Acquisitions: Reddit (r/SideProject, r/microsaas, r/indiehackers) + HN Algolia")

    # Check what's already automated
    print(f"\nRelated automations:")
    related = [
        "daily_research_pipeline.py",
        "ecom_arb_engine.py",
        "freelance_demand_scanner.py",
        "trend_aggregator.py",
        "twitter_alpha_scraper.py",
        "reddit_deep_scraper.py",
        "meme_coin_signal_tracker.py",
        "compliance_scanner.py",
        "system_health_monitor.py",
        "gov_contract_tweet_alerts.py",
    ]
    for script in related:
        path = AUTOMATIONS / script
        status = "EXISTS" if path.exists() else "MISSING"
        print(f"  [{status}] {script}")

    print()


def main():
    parser = argparse.ArgumentParser(description="Unified Alpha Monitor - Consolidates ALL monitoring sources")
    parser.add_argument("--full", action="store_true", help="Run full scan (all modules)")
    parser.add_argument("--quick", action="store_true", help="Quick scan (content freshness only)")
    parser.add_argument("--status", action="store_true", help="Show monitoring status")
    parser.add_argument("--reddit", action="store_true", help="Run app-specific Reddit scan only")
    parser.add_argument("--github", action="store_true", help="Run GitHub repo scan only")
    parser.add_argument("--freshness", action="store_true", help="Run content freshness audit only")
    parser.add_argument("--news", action="store_true", help="Run RSS news feed scan only")
    parser.add_argument("--aso", action="store_true", help="Generate ASO keyword report")
    parser.add_argument("--producthunt", action="store_true", help="Scan Product Hunt RSS feed for launches")
    parser.add_argument("--samgov", action="store_true", help="Query SAM.gov/USAspending for federal contracts")
    parser.add_argument("--acquisitions", action="store_true", help="Scan Reddit + HN for acquisition opportunities")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.full:
        result = run_full_scan()
        if args.json:
            print(json.dumps(result, indent=2))
    elif args.quick:
        run_quick_scan()
    elif args.reddit:
        results = scan_app_subreddits()
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"Found {len(results)} app-related Reddit posts")
    elif args.github:
        results = scan_github_trending()
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for r in results[:10]:
                print(f"  [{r['stars']}*] {r['name']} ({r['language']}) - {r['description'][:60]}")
    elif args.news:
        items = scan_news_feeds()
        if args.json:
            print(json.dumps(items, indent=2))
        else:
            for item in items:
                print(f"  [{item.get('source_name', '?')}] {item['title'][:70]}")
                if item.get("url"):
                    print(f"    {item['url']}")
            print(f"\n  Total: {len(items)} relevant news items")
    elif args.freshness:
        results = audit_content_freshness()
        for f in results[:20]:
            print(f"  [{f['priority'].upper()}] {f['file']} ({f['days_old']}d old)")
    elif args.aso:
        results = generate_aso_report()
        for app, kws in ASO_KEYWORDS.items():
            print(f"\n{app}:")
            for kw in kws:
                print(f"  - {kw}")
    elif args.producthunt:
        results = scan_product_hunt()
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for r in results[:20]:
                print(f"  [{r.get('matched_keywords', '')}] {r['name']}")
                print(f"    {r['url']}")
                if r.get("description"):
                    print(f"    {r['description'][:80]}")
            print(f"\n  Total: {len(results)} Product Hunt launches")
    elif args.samgov:
        results = scan_samgov_contracts()
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for r in results[:20]:
                print(f"  [{r.get('keyword', '')}] {r['title'][:70]}")
                print(f"    {r['url']}")
                if r.get("response_deadline"):
                    print(f"    Deadline: {r['response_deadline']}")
            print(f"\n  Total: {len(results)} SAM.gov contract opportunities")
    elif args.acquisitions:
        results = scan_acquisitions()
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for r in results[:20]:
                rev = f" (rev: ${r['revenue']})" if r.get("revenue") else ""
                price = f" asking: ${r['asking_price']}" if r.get("asking_price") else ""
                print(f"  [{r.get('source', '')}] {r['title'][:60]}{rev}{price}")
                print(f"    {r['url']}")
            print(f"\n  Total: {len(results)} acquisition listings")
    else:
        parser.print_help()
        print("\n\nExamples:")
        print("  python3 AUTOMATIONS/unified_alpha_monitor.py --full          # Full daily scan (all modules)")
        print("  python3 AUTOMATIONS/unified_alpha_monitor.py --status        # Check monitoring status")
        print("  python3 AUTOMATIONS/unified_alpha_monitor.py --quick         # Quick freshness check")
        print("  python3 AUTOMATIONS/unified_alpha_monitor.py --github        # GitHub repos only")
        print("  python3 AUTOMATIONS/unified_alpha_monitor.py --news          # RSS news feeds only")
        print("  python3 AUTOMATIONS/unified_alpha_monitor.py --producthunt   # Product Hunt RSS feed")
        print("  python3 AUTOMATIONS/unified_alpha_monitor.py --samgov        # Federal contracts (USAspending)")
        print("  python3 AUTOMATIONS/unified_alpha_monitor.py --acquisitions  # Reddit + HN opportunities")


if __name__ == "__main__":
    main()
