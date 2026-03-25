#!/usr/bin/env python3
"""
PRINTMAXX Opportunity Radar - Continuous Discovery Engine
==========================================================
Scans multiple sources for new opportunities and cross-references
with existing ops to find synergies.

Sources:
  - Product Hunt daily launches (gaps in market)
  - GitHub trending repos (MIT repos to fork/adapt)
  - Hacker News "Show HN" (validated ideas with traction)
  - Reddit r/SideProject, r/indiehackers (what's making money)

Outputs to: LEDGER/OPPORTUNITY_RADAR.csv

Usage:
    python3 AUTOMATIONS/opportunity_radar.py --scan              # Full scan all sources
    python3 AUTOMATIONS/opportunity_radar.py --scan --source ph  # Product Hunt only
    python3 AUTOMATIONS/opportunity_radar.py --scan --source gh  # GitHub trending only
    python3 AUTOMATIONS/opportunity_radar.py --scan --source hn  # Hacker News only
    python3 AUTOMATIONS/opportunity_radar.py --scan --source rd  # Reddit only
    python3 AUTOMATIONS/opportunity_radar.py --daily             # Daily digest
    python3 AUTOMATIONS/opportunity_radar.py --weekly-report     # Weekly summary
    python3 AUTOMATIONS/opportunity_radar.py --integrate         # Cross-ref with ops
    python3 AUTOMATIONS/opportunity_radar.py --history           # View past scans
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote_plus

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip3 install requests")
    sys.exit(1)

# ============================================================
# PATH SAFETY
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER = PROJECT_ROOT / "LEDGER"
OUTPUT_CSV = LEDGER / "OPPORTUNITY_RADAR.csv"
HISTORY_DIR = LEDGER / "OPPORTUNITY_RADAR_HISTORY"
SCAN_LOG = HISTORY_DIR / "scan_log.jsonl"

def safe_path(target):
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} outside project root")
    return resolved

# ============================================================
# EXISTING OPS (for synergy cross-reference)
# ============================================================
EXISTING_OPS = {
    "mcp": ["OP_MCP", "D12"],
    "ai_agent": ["OP_AGENT_CONSULT", "S04"],
    "vibe_coding": ["OP_VIBE_PRODUCTS"],
    "community": ["OP_COMMUNITY", "M02"],
    "clipping": ["OP_CLIP_SERVICE", "C09", "N26"],
    "infrastructure": ["OP_INFRA_SERVICE", "S02"],
    "api": ["OP_API_ARB", "D09", "A04"],
    "freelance": ["S01", "S18"],
    "digital_products": ["D01", "N02"],
    "content": ["C01", "C05", "C07"],
    "apps": ["A01", "A02"],
    "persona": ["P01", "P02"],
    "ecom": ["E01", "E02", "E03"],
    "newsletter": ["C05", "C12"],
    "seo": ["C11", "C13", "S12"],
    "automation": ["S04", "G05"],
    "saas": ["A02", "A09", "D09"],
    "chrome_extension": ["D05", "N55"],
    "notion": ["D02"],
    "print_on_demand": ["E02"],
    "trading": ["A11", "I01"],
    "voice": ["N39", "N59"],
}

# Keywords that map to our ops for synergy detection
SYNERGY_KEYWORDS = {
    "mcp": ["mcp", "model context protocol", "claude tool", "claude plugin"],
    "ai_agent": ["ai agent", "autonomous agent", "crewai", "langgraph", "autogen",
                  "agent framework", "agent workflow"],
    "vibe_coding": ["vibe coding", "claude code", "cursor", "lovable", "bolt",
                     "ai coding", "code generation"],
    "community": ["skool", "community", "membership", "paid group", "discord premium"],
    "clipping": ["clip", "stream highlight", "video edit", "opusclip", "short form"],
    "api": ["api wrapper", "api arbitrage", "llm router", "openrouter", "litellm"],
    "freelance": ["freelance", "upwork", "fiverr", "freelancer", "side hustle"],
    "digital_products": ["digital product", "gumroad", "template", "ebook", "course",
                          "info product"],
    "content": ["content", "tiktok", "youtube", "instagram", "social media"],
    "apps": ["app", "mobile app", "pwa", "indie app"],
    "saas": ["saas", "micro saas", "subscription", "mrr"],
    "newsletter": ["newsletter", "substack", "beehiiv", "email list"],
    "seo": ["seo", "programmatic seo", "search engine", "organic traffic"],
    "automation": ["automation", "n8n", "zapier", "make.com", "workflow"],
    "chrome_extension": ["chrome extension", "browser extension"],
    "notion": ["notion template", "notion"],
    "print_on_demand": ["print on demand", "pod", "merch", "t-shirt"],
    "trading": ["trading bot", "algo trading", "crypto bot"],
    "voice": ["voice clone", "text to speech", "elevenlabs", "tts"],
}

# HTTP session with retry
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "PRINTMAXX-OpportunityRadar/1.0 (research-bot)"
})
REQUEST_TIMEOUT = 15


# ============================================================
# SCANNING FUNCTIONS
# ============================================================

def scan_product_hunt():
    """Scan Product Hunt for recent launches via their public API/feed."""
    print("\n[Product Hunt] Scanning recent launches...")
    opportunities = []

    try:
        # Use Product Hunt's undocumented feed endpoint
        url = "https://www.producthunt.com/frontend/graphql"
        # Fallback: scrape the homepage
        resp = SESSION.get("https://www.producthunt.com/", timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200:
            print(f"  [PH] HTTP {resp.status_code} - trying alternative...")
            # Try the API
            resp = SESSION.get(
                "https://api.producthunt.com/v2/api/graphql",
                timeout=REQUEST_TIMEOUT
            )

        # Parse what we can from the HTML
        text = resp.text

        # Extract product names and taglines from meta/og tags and structured data
        titles = re.findall(r'"name"\s*:\s*"([^"]+)"', text)
        taglines = re.findall(r'"tagline"\s*:\s*"([^"]+)"', text)

        seen = set()
        for i, title in enumerate(titles[:20]):
            if title in seen or len(title) < 3 or title in ("Product Hunt", "Posts"):
                continue
            seen.add(title)
            tagline = taglines[i] if i < len(taglines) else ""
            synergies = find_synergies(f"{title} {tagline}")
            opportunities.append({
                "source": "ProductHunt",
                "title": title,
                "description": tagline,
                "url": f"https://www.producthunt.com/search?q={quote_plus(title)}",
                "score": 0,
                "synergies": synergies,
                "category": categorize_opportunity(f"{title} {tagline}"),
                "discovered": datetime.now().isoformat(),
            })

        print(f"  [PH] Found {len(opportunities)} items")

    except requests.RequestException as e:
        print(f"  [PH] Error: {e}")

    # Fallback: use known Product Hunt categories relevant to us
    if len(opportunities) < 3:
        print("  [PH] Using category-based scan...")
        categories = [
            "developer-tools", "artificial-intelligence", "saas",
            "productivity", "no-code", "marketing"
        ]
        for cat in categories:
            try:
                resp = SESSION.get(
                    f"https://www.producthunt.com/categories/{cat}",
                    timeout=REQUEST_TIMEOUT
                )
                if resp.status_code == 200:
                    cat_titles = re.findall(r'<h3[^>]*>([^<]+)</h3>', resp.text)
                    for title in cat_titles[:5]:
                        title = title.strip()
                        if title and title not in seen and len(title) > 3:
                            seen.add(title)
                            synergies = find_synergies(title)
                            opportunities.append({
                                "source": "ProductHunt",
                                "title": title,
                                "description": f"Category: {cat}",
                                "url": f"https://www.producthunt.com/categories/{cat}",
                                "score": 0,
                                "synergies": synergies,
                                "category": cat.replace("-", "_"),
                                "discovered": datetime.now().isoformat(),
                            })
                time.sleep(1)  # rate limit
            except requests.RequestException:
                continue

        print(f"  [PH] Total after category scan: {len(opportunities)} items")

    return opportunities


def scan_github_trending():
    """Scan GitHub trending repos for MIT-licensed forkable projects."""
    print("\n[GitHub] Scanning trending repositories...")
    opportunities = []

    # GitHub trending API (unofficial but stable)
    languages = ["python", "javascript", "typescript", ""]
    seen = set()

    for lang in languages:
        try:
            # Use GitHub's search API sorted by stars, recent
            since = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            query = f"created:>{since}"
            if lang:
                query += f" language:{lang}"

            resp = SESSION.get(
                "https://api.github.com/search/repositories",
                params={
                    "q": query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 15,
                },
                timeout=REQUEST_TIMEOUT,
            )

            if resp.status_code == 200:
                data = resp.json()
                for repo in data.get("items", [])[:10]:
                    name = repo.get("full_name", "")
                    if name in seen:
                        continue
                    seen.add(name)

                    license_info = repo.get("license") or {}
                    license_key = license_info.get("key", "unknown")
                    is_permissive = license_key in ("mit", "apache-2.0", "bsd-2-clause",
                                                      "bsd-3-clause", "unlicense", "0bsd")

                    desc = repo.get("description", "") or ""
                    stars = repo.get("stargazers_count", 0)
                    lang_used = repo.get("language", "unknown")

                    synergies = find_synergies(f"{name} {desc}")

                    opportunities.append({
                        "source": "GitHub",
                        "title": name,
                        "description": f"[{lang_used}] {desc} ({stars} stars, {license_key})",
                        "url": repo.get("html_url", ""),
                        "score": min(stars // 10, 100),  # rough score from stars
                        "synergies": synergies,
                        "category": "open_source",
                        "license": license_key,
                        "is_forkable": is_permissive,
                        "stars": stars,
                        "discovered": datetime.now().isoformat(),
                    })

            time.sleep(2)  # GitHub rate limit: 10 req/min unauthenticated

        except requests.RequestException as e:
            print(f"  [GH] Error for {lang or 'all'}: {e}")

    # Also check trending page for AI/developer tools specifically
    try:
        ai_query = "ai agent OR mcp OR claude OR llm created:>" + since
        resp = SESSION.get(
            "https://api.github.com/search/repositories",
            params={"q": ai_query, "sort": "stars", "order": "desc", "per_page": 10},
            timeout=REQUEST_TIMEOUT,
        )
        if resp.status_code == 200:
            for repo in resp.json().get("items", [])[:10]:
                name = repo.get("full_name", "")
                if name in seen:
                    continue
                seen.add(name)
                desc = repo.get("description", "") or ""
                stars = repo.get("stargazers_count", 0)
                license_info = repo.get("license") or {}
                license_key = license_info.get("key", "unknown")
                is_permissive = license_key in ("mit", "apache-2.0", "bsd-2-clause",
                                                  "bsd-3-clause", "unlicense")
                synergies = find_synergies(f"{name} {desc}")
                opportunities.append({
                    "source": "GitHub",
                    "title": name,
                    "description": f"[AI] {desc} ({stars} stars, {license_key})",
                    "url": repo.get("html_url", ""),
                    "score": min(stars // 10, 100),
                    "synergies": synergies,
                    "category": "ai_tools",
                    "license": license_key,
                    "is_forkable": is_permissive,
                    "stars": stars,
                    "discovered": datetime.now().isoformat(),
                })
    except requests.RequestException:
        pass

    print(f"  [GH] Found {len(opportunities)} trending repos")
    return opportunities


def scan_hacker_news():
    """Scan Hacker News 'Show HN' for validated ideas."""
    print("\n[Hacker News] Scanning Show HN posts...")
    opportunities = []

    try:
        # HN Search API (Algolia)
        resp = SESSION.get(
            "https://hn.algolia.com/api/v1/search",
            params={
                "query": "Show HN",
                "tags": "story",
                "numericFilters": f"created_at_i>{int(time.time()) - 7*86400}",
                "hitsPerPage": 30,
            },
            timeout=REQUEST_TIMEOUT,
        )

        if resp.status_code == 200:
            data = resp.json()
            for hit in data.get("hits", []):
                title = hit.get("title", "")
                if not title.startswith("Show HN"):
                    continue

                url = hit.get("url", "") or f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}"
                points = hit.get("points", 0) or 0
                num_comments = hit.get("num_comments", 0) or 0

                # Clean title
                clean_title = title.replace("Show HN: ", "").replace("Show HN:", "").strip()
                synergies = find_synergies(clean_title)

                opportunities.append({
                    "source": "HackerNews",
                    "title": clean_title,
                    "description": f"Show HN: {points} points, {num_comments} comments",
                    "url": url,
                    "score": min(points, 100),
                    "synergies": synergies,
                    "category": categorize_opportunity(clean_title),
                    "points": points,
                    "comments": num_comments,
                    "discovered": datetime.now().isoformat(),
                })

        print(f"  [HN] Found {len(opportunities)} Show HN posts")

    except requests.RequestException as e:
        print(f"  [HN] Error: {e}")

    # Also scan "Ask HN: What are you working on?" threads
    try:
        resp = SESSION.get(
            "https://hn.algolia.com/api/v1/search",
            params={
                "query": "making money side project revenue",
                "tags": "story",
                "numericFilters": f"created_at_i>{int(time.time()) - 14*86400}",
                "hitsPerPage": 15,
            },
            timeout=REQUEST_TIMEOUT,
        )
        if resp.status_code == 200:
            for hit in resp.json().get("hits", []):
                title = hit.get("title", "")
                points = hit.get("points", 0) or 0
                if points < 5:
                    continue
                synergies = find_synergies(title)
                opportunities.append({
                    "source": "HackerNews",
                    "title": title,
                    "description": f"Revenue discussion: {points} points",
                    "url": f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}",
                    "score": min(points // 2, 100),
                    "synergies": synergies,
                    "category": "discussion",
                    "points": points,
                    "discovered": datetime.now().isoformat(),
                })
    except requests.RequestException:
        pass

    return opportunities


def scan_reddit():
    """Scan Reddit for side projects making money."""
    print("\n[Reddit] Scanning side project subreddits...")
    opportunities = []

    subreddits = [
        "SideProject",
        "indiehackers",
        "microsaas",
        "Entrepreneur",
        "SaaS",
    ]

    for sub in subreddits:
        try:
            # Reddit JSON API (no auth needed)
            resp = SESSION.get(
                f"https://www.reddit.com/r/{sub}/hot.json",
                params={"limit": 15, "t": "week"},
                timeout=REQUEST_TIMEOUT,
            )

            if resp.status_code == 200:
                data = resp.json()
                posts = data.get("data", {}).get("children", [])
                for post in posts:
                    pdata = post.get("data", {})
                    title = pdata.get("title", "")
                    score = pdata.get("score", 0)
                    url = pdata.get("url", "")
                    selftext = (pdata.get("selftext", "") or "")[:200]
                    num_comments = pdata.get("num_comments", 0)
                    permalink = pdata.get("permalink", "")

                    # Filter for revenue/money related posts
                    revenue_signals = [
                        "$", "revenue", "mrr", "income", "profit", "earning",
                        "making money", "launched", "built", "shipping",
                        "subscribers", "customers", "users"
                    ]
                    text_lower = f"{title} {selftext}".lower()
                    has_signal = any(s in text_lower for s in revenue_signals)

                    if not has_signal and score < 20:
                        continue

                    synergies = find_synergies(f"{title} {selftext}")

                    opportunities.append({
                        "source": f"Reddit/r/{sub}",
                        "title": title[:120],
                        "description": selftext[:150].replace("\n", " ") if selftext else f"Score: {score}, Comments: {num_comments}",
                        "url": f"https://reddit.com{permalink}" if permalink else url,
                        "score": min(score, 100),
                        "synergies": synergies,
                        "category": categorize_opportunity(f"{title} {selftext}"),
                        "upvotes": score,
                        "comments": num_comments,
                        "discovered": datetime.now().isoformat(),
                    })

            time.sleep(2)  # Reddit rate limit

        except requests.RequestException as e:
            print(f"  [Reddit] Error for r/{sub}: {e}")

    print(f"  [Reddit] Found {len(opportunities)} relevant posts")
    return opportunities


# ============================================================
# ANALYSIS FUNCTIONS
# ============================================================

def find_synergies(text):
    """Find synergies between an opportunity and existing ops."""
    text_lower = text.lower()
    found = []
    for category, keywords in SYNERGY_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                ops = EXISTING_OPS.get(category, [])
                for op in ops:
                    if op not in found:
                        found.append(op)
                break  # one match per category is enough
    return found


def categorize_opportunity(text):
    """Auto-categorize an opportunity."""
    text_lower = text.lower()
    categories = {
        "ai_tools": ["ai", "llm", "gpt", "claude", "machine learning", "ml"],
        "saas": ["saas", "subscription", "mrr", "recurring"],
        "developer_tools": ["developer", "dev tool", "api", "sdk", "framework"],
        "content": ["content", "video", "youtube", "tiktok", "social"],
        "ecommerce": ["ecommerce", "shop", "store", "product", "sell"],
        "productivity": ["productivity", "workflow", "automate", "time"],
        "marketing": ["marketing", "seo", "email", "outreach", "growth"],
        "education": ["course", "learn", "tutorial", "bootcamp"],
        "fintech": ["payment", "finance", "trading", "crypto", "fintech"],
        "design": ["design", "ui", "ux", "template", "figma"],
    }
    for cat, keywords in categories.items():
        for kw in keywords:
            if kw in text_lower:
                return cat
    return "other"


def score_opportunity(opp):
    """Score an opportunity based on relevance to PRINTMAXX."""
    score = opp.get("score", 0)

    # Bonus for synergies (each synergy = +10 points)
    synergy_bonus = len(opp.get("synergies", [])) * 10
    score += synergy_bonus

    # Bonus for AI-related (our core competency)
    if opp.get("category") in ("ai_tools", "developer_tools"):
        score += 15

    # Bonus for high engagement
    points = opp.get("points", opp.get("upvotes", opp.get("stars", 0)))
    if points > 100:
        score += 20
    elif points > 50:
        score += 10

    # Bonus for forkable repos
    if opp.get("is_forkable"):
        score += 10

    # Cap at 100
    return min(score, 100)


# ============================================================
# OUTPUT FUNCTIONS
# ============================================================

def save_opportunities(opportunities):
    """Save opportunities to CSV."""
    os.makedirs(LEDGER, exist_ok=True)
    output = safe_path(OUTPUT_CSV)

    # Read existing to avoid duplicates
    existing_titles = set()
    if output.exists():
        try:
            with open(output, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_titles.add(row.get("title", ""))
        except Exception:
            pass

    new_count = 0
    mode = "a" if output.exists() else "w"
    with open(output, mode, newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if mode == "w":
            writer.writerow([
                "timestamp", "source", "title", "description", "url",
                "relevance_score", "synergy_ops", "category",
                "engagement", "action_taken"
            ])

        for opp in opportunities:
            if opp["title"] in existing_titles:
                continue
            existing_titles.add(opp["title"])

            rel_score = score_opportunity(opp)
            engagement = opp.get("points", opp.get("upvotes", opp.get("stars", 0)))
            synergy_str = "|".join(opp.get("synergies", []))

            writer.writerow([
                opp.get("discovered", datetime.now().isoformat()),
                opp.get("source", ""),
                opp.get("title", ""),
                opp.get("description", "")[:200],
                opp.get("url", ""),
                rel_score,
                synergy_str,
                opp.get("category", ""),
                engagement,
                "",  # action_taken - to be filled manually
            ])
            new_count += 1

    print(f"\nSaved {new_count} new opportunities to {output}")
    return new_count


def save_scan_log(source_counts):
    """Log scan results for history tracking."""
    os.makedirs(HISTORY_DIR, exist_ok=True)
    log = safe_path(SCAN_LOG)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "sources": source_counts,
        "total": sum(source_counts.values()),
    }

    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def print_digest(opportunities, title="OPPORTUNITY RADAR"):
    """Print a formatted digest of opportunities."""
    print(f"\n{'='*75}")
    print(f"  {title} - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  {len(opportunities)} opportunities scanned")
    print(f"{'='*75}\n")

    # Score and sort
    for opp in opportunities:
        opp["relevance_score"] = score_opportunity(opp)
    opportunities.sort(key=lambda x: -x["relevance_score"])

    # Top opportunities
    print("TOP OPPORTUNITIES (by relevance to PRINTMAXX):")
    print(f"  {'#':>3} {'SCORE':>5} {'SOURCE':<15} {'TITLE':<45} {'SYNERGIES':<20}")
    print(f"  {'-'*3} {'-'*5} {'-'*15} {'-'*45} {'-'*20}")

    for i, opp in enumerate(opportunities[:20], 1):
        syn_str = ", ".join(opp.get("synergies", [])[:3])
        title_str = opp["title"][:44]
        source = opp["source"][:14]
        score = opp["relevance_score"]

        # Color by score
        if score >= 60:
            color = "\033[92m"
        elif score >= 30:
            color = "\033[93m"
        else:
            color = "\033[0m"

        print(f"  {i:>3} {color}{score:>5}\033[0m {source:<15} {title_str:<45} {syn_str:<20}")

    # Source breakdown
    print(f"\nSOURCE BREAKDOWN:")
    sources = {}
    for opp in opportunities:
        src = opp["source"].split("/")[0]
        sources[src] = sources.get(src, 0) + 1
    for src, count in sorted(sources.items(), key=lambda x: -x[1]):
        print(f"  {src:<15} {count:>4} items")

    # Synergy analysis
    print(f"\nSYNERGY HITS (opportunities that align with existing ops):")
    synergy_count = {}
    for opp in opportunities:
        for syn in opp.get("synergies", []):
            synergy_count[syn] = synergy_count.get(syn, 0) + 1

    for syn, count in sorted(synergy_count.items(), key=lambda x: -x[1])[:10]:
        print(f"  {syn:<18} {count:>3} opportunities match")

    # Category breakdown
    print(f"\nCATEGORY BREAKDOWN:")
    cats = {}
    for opp in opportunities:
        cat = opp.get("category", "other")
        cats[cat] = cats.get(cat, 0) + 1
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {cat:<20} {count:>4} items")

    print(f"\n{'='*75}\n")


# ============================================================
# CLI COMMANDS
# ============================================================

def cmd_scan(args):
    """Run a full scan across all or specified sources."""
    all_opportunities = []
    source_counts = {}

    source = args.source if hasattr(args, "source") and args.source else "all"

    if source in ("all", "ph"):
        opps = scan_product_hunt()
        all_opportunities.extend(opps)
        source_counts["ProductHunt"] = len(opps)

    if source in ("all", "gh"):
        opps = scan_github_trending()
        all_opportunities.extend(opps)
        source_counts["GitHub"] = len(opps)

    if source in ("all", "hn"):
        opps = scan_hacker_news()
        all_opportunities.extend(opps)
        source_counts["HackerNews"] = len(opps)

    if source in ("all", "rd"):
        opps = scan_reddit()
        all_opportunities.extend(opps)
        source_counts["Reddit"] = len(opps)

    # Print digest
    print_digest(all_opportunities)

    # Save
    new_count = save_opportunities(all_opportunities)
    save_scan_log(source_counts)

    # --- Feed high-scoring findings into ALPHA_STAGING for Capital Genesis scoring ---
    if all_opportunities:
        try:
            from _alpha_staging_writer import stage_findings_batch

            # Category mapping for opportunity types
            _cat_map = {
                "ai_tools": "APP_FACTORY",
                "developer_tools": "APP_FACTORY",
                "saas": "APP_FACTORY",
                "open_source": "APP_FACTORY",
                "productivity": "APP_FACTORY",
                "marketing": "MONETIZATION",
                "ecom": "MONETIZATION",
                "content": "CONTENT",
                "community": "CONTENT",
                "freelance": "MONETIZATION",
                "newsletter": "CONTENT",
            }

            scored = [(opp, score_opportunity(opp)) for opp in all_opportunities]
            high_value = [(opp, s) for opp, s in scored if s >= 40]
            high_value.sort(key=lambda x: -x[1])

            findings = []
            for opp, s in high_value[:25]:
                cat = _cat_map.get(opp.get("category", ""), "MARKET_SIGNAL")
                synergies = opp.get("synergies", [])
                findings.append({
                    "content": (
                        f"Opportunity: {opp.get('title', '')[:120]} | "
                        f"{opp.get('description', '')[:150]} | "
                        f"Score: {s}/100 | Synergies: {', '.join(synergies) if synergies else 'none'}"
                    ),
                    "source": f"opportunity_radar/{opp.get('source', 'unknown')}",
                    "source_url": opp.get("url", ""),
                    "category": cat,
                    "roi_potential": "HIGH" if s >= 60 else "MEDIUM",
                    "applicable_methods": ",".join(synergies) if synergies else "",
                    "reviewer_notes": f"Relevance {s}/100. Auto-staged from opportunity_radar.",
                })
            if findings:
                staged = stage_findings_batch(findings)
                print(f"  Staged {staged} high-scoring opportunities to ALPHA_STAGING.csv")
        except ImportError:
            pass

    print(f"SCAN COMPLETE: {len(all_opportunities)} total, {new_count} new")


def cmd_daily(args):
    """Daily digest - same as scan but with daily framing."""
    print("\n[DAILY DIGEST]")
    cmd_scan(args)


def cmd_weekly_report(args):
    """Generate weekly summary from scan history."""
    print(f"\n{'='*70}")
    print(f"  WEEKLY OPPORTUNITY REPORT - {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'='*70}\n")

    # Read scan log
    log_path = safe_path(SCAN_LOG)
    if not log_path.exists():
        print("No scan history found. Run --scan first.")
        return

    week_ago = datetime.now() - timedelta(days=7)
    scans = []
    with open(log_path, "r") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                ts = datetime.fromisoformat(entry["timestamp"])
                if ts >= week_ago:
                    scans.append(entry)
            except (json.JSONDecodeError, KeyError, ValueError):
                continue

    print(f"Scans this week: {len(scans)}")
    total_opps = sum(e.get("total", 0) for e in scans)
    print(f"Total opportunities discovered: {total_opps}")

    # Read current CSV for top items
    csv_path = safe_path(OUTPUT_CSV)
    if csv_path.exists():
        top_items = []
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        ts = datetime.fromisoformat(row.get("timestamp", ""))
                        if ts >= week_ago:
                            top_items.append(row)
                    except (ValueError, TypeError):
                        continue
        except Exception:
            pass

        if top_items:
            # Sort by relevance score
            top_items.sort(key=lambda x: -int(x.get("relevance_score", 0)))
            print(f"\nTOP 10 OPPORTUNITIES THIS WEEK:")
            for i, item in enumerate(top_items[:10], 1):
                print(f"  {i}. [{item.get('source', '')}] {item.get('title', '')[:60]}")
                print(f"     Score: {item.get('relevance_score', 0)} | "
                      f"Synergies: {item.get('synergy_ops', 'none')}")
    else:
        print("\nNo opportunity data found. Run --scan first.")

    # Source distribution
    if scans:
        source_totals = {}
        for scan in scans:
            for src, count in scan.get("sources", {}).items():
                source_totals[src] = source_totals.get(src, 0) + count
        print(f"\nSOURCE DISTRIBUTION:")
        for src, count in sorted(source_totals.items(), key=lambda x: -x[1]):
            print(f"  {src:<15} {count:>4} items")

    print(f"\n{'='*70}\n")


def cmd_integrate(args):
    """Cross-reference opportunities with existing ops."""
    csv_path = safe_path(OUTPUT_CSV)
    if not csv_path.exists():
        print("No opportunity data found. Run --scan first.")
        return

    print(f"\n{'='*70}")
    print(f"  SYNERGY INTEGRATION ANALYSIS")
    print(f"{'='*70}\n")

    # Read opportunities
    items = []
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            items = list(csv.DictReader(f))
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Group by synergy op
    op_matches = {}
    for item in items:
        synergies = item.get("synergy_ops", "").split("|")
        for syn in synergies:
            syn = syn.strip()
            if syn:
                if syn not in op_matches:
                    op_matches[syn] = []
                op_matches[syn].append(item)

    print(f"SYNERGY MATCHES ({len(op_matches)} ops have matching opportunities):\n")
    for op, matches in sorted(op_matches.items(), key=lambda x: -len(x[1])):
        print(f"  {op} ({len(matches)} matches):")
        # Show top 3 by score
        matches.sort(key=lambda x: -int(x.get("relevance_score", 0)))
        for m in matches[:3]:
            print(f"    - [{m.get('source', '')}] {m.get('title', '')[:55]} "
                  f"(score: {m.get('relevance_score', 0)})")
        if len(matches) > 3:
            print(f"    ... +{len(matches)-3} more")
        print()

    # Unmatched opportunities (potential new ops)
    unmatched = [i for i in items if not i.get("synergy_ops", "").strip()]
    if unmatched:
        print(f"UNMATCHED OPPORTUNITIES (potential NEW ops):")
        unmatched.sort(key=lambda x: -int(x.get("relevance_score", 0)))
        for item in unmatched[:10]:
            print(f"  - [{item.get('source', '')}] {item.get('title', '')[:55]} "
                  f"(score: {item.get('relevance_score', 0)}, cat: {item.get('category', '')})")

    print(f"\n{'='*70}\n")


def cmd_history(args):
    """View past scan history."""
    log_path = safe_path(SCAN_LOG)
    if not log_path.exists():
        print("No scan history found. Run --scan first.")
        return

    print(f"\nSCAN HISTORY:")
    print(f"{'TIMESTAMP':<24} {'TOTAL':>6}  SOURCES")
    print(f"{'-'*24} {'-'*6}  {'-'*40}")

    with open(log_path, "r") as f:
        entries = []
        for line in f:
            try:
                entries.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue

    for entry in entries[-20:]:  # last 20 scans
        ts = entry.get("timestamp", "")[:19]
        total = entry.get("total", 0)
        sources = ", ".join(f"{k}:{v}" for k, v in entry.get("sources", {}).items())
        print(f"{ts:<24} {total:>6}  {sources}")

    print(f"\nTotal scans: {len(entries)}")
    print()


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Opportunity Radar - Continuous Discovery Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --scan                    Full scan all sources
  %(prog)s --scan --source gh        GitHub trending only
  %(prog)s --scan --source hn        Hacker News only
  %(prog)s --scan --source rd        Reddit only
  %(prog)s --scan --source ph        Product Hunt only
  %(prog)s --daily                   Daily digest
  %(prog)s --weekly-report           Weekly summary report
  %(prog)s --integrate               Cross-reference with existing ops
  %(prog)s --history                 View past scan results
        """
    )
    parser.add_argument("--scan", action="store_true",
                        help="Scan all sources for opportunities")
    parser.add_argument("--source", choices=["ph", "gh", "hn", "rd", "all"],
                        default="all", help="Specific source to scan")
    parser.add_argument("--daily", action="store_true",
                        help="Daily digest scan")
    parser.add_argument("--weekly-report", action="store_true",
                        help="Weekly summary report")
    parser.add_argument("--integrate", action="store_true",
                        help="Cross-reference opportunities with existing ops")
    parser.add_argument("--history", action="store_true",
                        help="View past scan history")

    args = parser.parse_args()

    if args.scan:
        cmd_scan(args)
    elif args.daily:
        cmd_daily(args)
    elif args.weekly_report:
        cmd_weekly_report(args)
    elif args.integrate:
        cmd_integrate(args)
    elif args.history:
        cmd_history(args)
    else:
        # Default: scan
        print("No command specified. Running full scan...")
        args.source = "all"
        cmd_scan(args)


if __name__ == "__main__":
    main()
