#!/usr/bin/env python3
"""
CROSS-POLLINATOR: Wires venture outputs to venture inputs.

Each venture produces data that another venture needs.
This script moves data between them automatically.

Run: python3 AUTOMATIONS/cross_pollinator.py --cycle
"""

import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT_ROOT / "AUTOMATIONS"
LEDGER = PROJECT_ROOT / "LEDGER"
CONTENT = PROJECT_ROOT / "CONTENT" / "social"
LEADS = AUTOMATIONS / "leads"
REPORTS = AUTOMATIONS / "agent" / "swarm" / "reports"
POSTING_QUEUE = CONTENT / "posting_queue"
REDDIT_OUTPUT = AUTOMATIONS / "reddit_scraper_output"

def safe_path(target):
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} outside project root")
    return resolved


def load_csv(path, max_rows=500):
    path = safe_path(path)
    if not path.exists():
        return []
    rows = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= max_rows:
                break
            rows.append(row)
    return rows


def load_json(path):
    path = safe_path(path)
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)


def append_csv(path, rows, fieldnames):
    path = safe_path(path)
    exists = path.exists() and path.stat().st_size > 0
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)


# ─── CONNECTION 1: Competitive Intel → Content Farm ───────────────────────
# Competitor version changes become tweet-worthy content
def wire_competitive_intel_to_content():
    changes = load_csv(LEDGER / "COMPETITOR_CHANGES.csv")
    if not changes:
        return 0

    existing_posts = set()
    queue_dir = safe_path(POSTING_QUEUE)
    if queue_dir.exists():
        for f in queue_dir.iterdir():
            if f.suffix == ".txt":
                existing_posts.add(f.stem)

    new_posts = []
    for row in changes:
        name = row.get("name", "")
        change_type = row.get("change_type", "")
        summary = row.get("summary", "")
        status = row.get("status", "")
        change_id = row.get("change_id", row.get("detected_date", ""))

        # Only process actionable or new changes
        if status not in ("NEW", "ACTIONABLE", "MONITOR"):
            continue

        slug = f"intel_{name}_{change_id}".replace(" ", "_").replace("/", "_")[:60]
        if slug in existing_posts:
            continue

        # Generate tweet from competitor data
        if change_type == "VERSION_UPDATE" and name:
            tweet = f"{name} just shipped a new update.\n\nmost prayer app founders aren't watching competitor velocity.\n\ni track 20+ apps daily. version bumps tell you what features are winning.\n\nhere's what this means for indie builders:"
        elif "trending" in (row.get("category", "") or "").lower():
            tweet = f"github trending shifted again.\n\n{summary[:120]}\n\nthe tools that trend on github today become the SaaS products of next quarter. i monitor this daily."
        elif "pricing" in (row.get("category", "") or "").lower():
            tweet = f"caught a pricing change: {name}\n\n{summary[:100]}\n\nif you're not monitoring competitor pricing pages you're leaving money on the table."
        else:
            continue

        post_path = safe_path(queue_dir / f"{slug}.txt")
        post_path.parent.mkdir(parents=True, exist_ok=True)
        post_path.write_text(tweet, encoding="utf-8")
        new_posts.append(slug)

    return len(new_posts)


# ─── CONNECTION 2: Reddit Scraper → Cold Outreach ─────────────────────────
# Reddit posts from r/SideProject, r/forhire become outreach targets
def wire_reddit_to_outreach():
    reddit_dir = safe_path(REDDIT_OUTPUT)
    if not reddit_dir.exists():
        return 0

    # Get most recent reddit scrape
    json_files = sorted(
        [f for f in reddit_dir.iterdir() if f.name.startswith("reddit_") and f.suffix == ".json"],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    if not json_files:
        return 0

    latest = json_files[0]
    try:
        with open(latest) as f:
            posts = json.load(f)
    except (json.JSONDecodeError, ValueError):
        return 0

    if not isinstance(posts, list):
        return 0

    # Filter for outreach-worthy posts
    outreach_subs = {"forhire", "freelance", "smallbusiness", "entrepreneur",
                     "webdev", "startups", "SideProject", "indiehackers"}
    hiring_keywords = {"hiring", "looking for", "need a", "want someone", "budget",
                       "freelancer", "developer needed", "website", "redesign", "build me"}

    new_leads = []
    for post in posts:
        if not isinstance(post, dict):
            continue
        sub = post.get("subreddit", "")
        title = (post.get("title", "") or "").lower()
        body = (post.get("selftext", "") or "").lower()
        author = post.get("author", "")
        url = post.get("url", post.get("permalink", ""))
        score = post.get("score", 0)

        if sub not in outreach_subs:
            continue

        text = f"{title} {body}"
        if not any(kw in text for kw in hiring_keywords):
            continue

        # Don't add duplicates
        new_leads.append({
            "business_name": f"Reddit: {author}",
            "address": f"r/{sub}",
            "phone": "",
            "website": f"https://reddit.com{url}" if url.startswith("/") else url,
            "google_rating": "",
            "review_count": str(score),
            "website_score": "",
            "signals_detected": f"reddit_post;{sub};score:{score}",
            "email_if_found": "",
            "category": "reddit_lead",
            "city": "online",
            "scraped_at": datetime.now().isoformat()
        })

    if new_leads:
        master_path = LEADS / "MASTER_LEADS.csv"
        fieldnames = ["business_name", "address", "phone", "website", "google_rating",
                      "review_count", "website_score", "signals_detected", "email_if_found",
                      "category", "city", "scraped_at"]
        # Check for existing reddit leads to avoid duplicates
        existing = load_csv(master_path, max_rows=2000)
        existing_urls = {r.get("website", "") for r in existing}
        deduped = [l for l in new_leads if l["website"] not in existing_urls]
        if deduped:
            append_csv(master_path, deduped, fieldnames)

        return len(deduped)
    return 0


# ─── CONNECTION 3: Competitive Intel → App Factory ────────────────────────
# Competitor gaps feed app factory's find_gap pipeline
def wire_competitive_intel_to_app_factory():
    intel = load_csv(LEDGER / "COMPETITIVE_INTEL.csv", max_rows=200)
    if not intel:
        return 0

    # Find gaps: apps with low ratings, old versions, or missing features
    gaps = []
    for row in intel:
        try:
            rating = float(row.get("rating", "0") or "0")
        except (ValueError, TypeError):
            rating = 0.0
        try:
            rating_count = int(row.get("rating_count", "0") or "0")
        except (ValueError, TypeError):
            rating_count = 0
        name = row.get("name", "")
        category = row.get("category", "")
        notes = row.get("notes", "")
        last_updated = row.get("last_updated", "")

        # Gap signals: high reviews but mediocre rating, or stale app
        if rating_count > 1000 and rating < 4.5:
            gaps.append({
                "competitor": name,
                "category": category,
                "gap_type": "LOW_SATISFACTION",
                "signal": f"Rating {rating}/5 with {rating_count} reviews = user pain",
                "opportunity": f"Build better {category} app targeting {name}'s unhappy users",
                "detected_at": datetime.now().isoformat()
            })

        if last_updated and last_updated < "2025-06-01":
            gaps.append({
                "competitor": name,
                "category": category,
                "gap_type": "ABANDONED_APP",
                "signal": f"Last updated {last_updated} - possibly abandoned",
                "opportunity": f"Clone {name}'s value prop with modern stack",
                "detected_at": datetime.now().isoformat()
            })

    if gaps:
        gap_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "app_factory_gaps.json")
        gap_path.parent.mkdir(parents=True, exist_ok=True)

        existing_gaps = []
        if gap_path.exists():
            try:
                existing_gaps = json.loads(gap_path.read_text())
            except (json.JSONDecodeError, ValueError):
                existing_gaps = []

        existing_comps = {g.get("competitor", "") for g in existing_gaps}
        new_gaps = [g for g in gaps if g["competitor"] not in existing_comps]

        if new_gaps:
            all_gaps = existing_gaps + new_gaps
            gap_path.write_text(json.dumps(all_gaps, indent=2))

        return len(new_gaps)
    return 0


# ─── CONNECTION 4: Alpha Intelligence → Content Farm ─────────────────────
# Approved alpha entries become content topics
def wire_alpha_to_content():
    alpha_path = LEDGER / "ALPHA_STAGING.csv"
    if not alpha_path.exists():
        return 0

    # Read only recent approved entries (last 200 rows)
    all_rows = load_csv(alpha_path, max_rows=500)

    approved = [r for r in all_rows if r.get("status") == "APPROVED"
                and r.get("category") in ("TOOL_ALPHA", "GROWTH_HACK", "MONETIZATION", "CONTENT_FORMAT")]

    if not approved:
        return 0

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)

    existing_posts = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"} if queue_dir.exists() else set()
    created = 0

    for row in approved[-10:]:  # Last 10 approved
        alpha_id = row.get("alpha_id", "")
        tactic = row.get("tactic", "") or row.get("extracted_method", "")
        category = row.get("category", "")
        source = row.get("source", "")

        slug = f"alpha_{alpha_id}".lower()
        if slug in existing_posts:
            continue

        if not tactic:
            continue

        # Generate content from alpha
        tweet = f"found something interesting while scanning {source.lower()} today.\n\n{tactic[:200]}\n\nmost people skip past this. the ones printing money don't."

        post_path = safe_path(queue_dir / f"{slug}.txt")
        post_path.write_text(tweet, encoding="utf-8")
        created += 1

    return created


# ─── CONNECTION 5: OpenClaw (Local Biz) → Cold Outreach ──────────────────
# Discovered local businesses feed the outreach pipeline
def wire_openclaw_to_outreach():
    openclaw_dir = safe_path(LEADS / "auto_local_biz_openclaw_nationwide_9569")
    if not openclaw_dir.exists():
        return 0

    # Look for any lead CSVs in the openclaw venture dir
    csv_files = list(openclaw_dir.glob("*.csv"))
    if not csv_files:
        return 0

    master_path = LEADS / "MASTER_LEADS.csv"
    existing = load_csv(master_path, max_rows=2000)
    existing_websites = {r.get("website", "") for r in existing if r.get("website")}

    fieldnames = ["business_name", "address", "phone", "website", "google_rating",
                  "review_count", "website_score", "signals_detected", "email_if_found",
                  "category", "city", "scraped_at"]

    total_added = 0
    for csv_file in csv_files:
        rows = load_csv(csv_file, max_rows=200)
        new_leads = []
        for row in rows:
            website = row.get("website", "")
            if website and website not in existing_websites:
                # Normalize to master leads format
                lead = {fn: row.get(fn, "") for fn in fieldnames}
                lead["scraped_at"] = lead.get("scraped_at") or datetime.now().isoformat()
                lead["category"] = lead.get("category") or "openclaw_lead"
                new_leads.append(lead)
                existing_websites.add(website)

        if new_leads:
            append_csv(master_path, new_leads, fieldnames)
            total_added += len(new_leads)

    return total_added


# ─── CONNECTION 6: App Factory → Content Farm ─────────────────────────────
# Deployed apps generate promotional content
def wire_apps_to_content():
    pipeline = load_json(PROJECT_ROOT / "FINANCIALS" / "revenue_pipeline.json")
    apps = pipeline.get("categories", {}).get("apps_deployed", {}).get("apps", [])

    if not apps:
        return 0

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)
    existing_posts = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"} if queue_dir.exists() else set()

    created = 0
    for app_name in apps[:5]:  # Top 5 apps
        slug = f"app_promo_{app_name.lower().replace(' ', '_')}"
        if slug in existing_posts:
            continue

        app_slug = app_name.lower().replace(" ", "").replace("maxx", "maxx")
        tweet = (
            f"built {app_name} in one session with claude code.\n\n"
            f"55KB. offline-capable. zero dependencies.\n\n"
            f"the app store charges $99/yr for a developer account. "
            f"surge.sh is free. PWAs are free. your users don't care about the wrapper.\n\n"
            f"ship the thing."
        )

        post_path = safe_path(queue_dir / f"{slug}.txt")
        post_path.write_text(tweet, encoding="utf-8")
        created += 1

    return created


# ─── CONNECTION 7: Digital Products → Content Farm ────────────────────────
# Product catalog generates promotional content
def wire_products_to_content():
    pipeline = load_json(PROJECT_ROOT / "FINANCIALS" / "revenue_pipeline.json")
    products = pipeline.get("categories", {}).get("gumroad_products", {}).get("products", [])

    if not products:
        return 0

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)
    existing_posts = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"} if queue_dir.exists() else set()

    created = 0
    for product in products:
        name = product.get("name", "")
        price = product.get("price", 0)
        if not name or price == 0:
            continue

        slug = f"product_promo_{name.lower().replace(' ', '_').replace('/', '_')[:40]}"
        if slug in existing_posts:
            continue

        tweet = (
            f"just finished the {name}.\n\n"
            f"not a course. not a community. a ${price} PDF that gives you exactly what you need "
            f"and gets out of the way.\n\n"
            f"i spent 40+ hours building the systems inside it. you get the shortcut."
        )

        post_path = safe_path(queue_dir / f"{slug}.txt")
        post_path.write_text(tweet, encoding="utf-8")
        created += 1

    return created


# ─── CONNECTION 8: Leads pain points → Content topics ─────────────────────
# What leads struggle with becomes content
def wire_leads_to_content():
    hot_leads = load_csv(LEADS / "HOT_LEADS.csv", max_rows=50)
    if not hot_leads:
        return 0

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)
    existing_posts = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"} if queue_dir.exists() else set()

    # Analyze lead signals for pain points
    pain_signals = {}
    for lead in hot_leads:
        signals = lead.get("signals_detected", "")
        if "NOT_mobile" in signals:
            pain_signals["not_mobile"] = pain_signals.get("not_mobile", 0) + 1
        if "no_ssl" in signals or "NO_ssl" in signals:
            pain_signals["no_ssl"] = pain_signals.get("no_ssl", 0) + 1
        if "no_form" in signals:
            pain_signals["no_form"] = pain_signals.get("no_form", 0) + 1
        if "no_schema" in signals:
            pain_signals["no_schema"] = pain_signals.get("no_schema", 0) + 1

    created = 0
    pain_tweets = {
        "not_mobile": (
            "scraped 1,000+ local business websites this week.\n\n"
            f"{pain_signals.get('not_mobile', 0)} of them aren't mobile responsive.\n\n"
            "it's 2026. 70% of web traffic is mobile. these businesses are burning money.\n\n"
            "if you can fix this for $500 you're printing."
        ),
        "no_ssl": (
            f"found {pain_signals.get('no_ssl', 0)} local businesses still running without SSL.\n\n"
            "chrome literally shows 'NOT SECURE' to every visitor.\n\n"
            "a $0 Let's Encrypt cert takes 5 minutes. "
            "charge them $200 to 'secure their website.' easiest money in freelancing."
        ),
        "no_form": (
            f"{pain_signals.get('no_form', 0)} businesses with websites and ZERO contact forms.\n\n"
            "no form = no leads from their own website. "
            "they're paying for hosting and getting nothing.\n\n"
            "add a form + thank-you page + email notification. charge $300. done in 20 minutes."
        ),
    }

    for key, tweet in pain_tweets.items():
        count = pain_signals.get(key, 0)
        if count < 2:
            continue
        slug = f"lead_pain_{key}"
        if slug in existing_posts:
            continue
        post_path = safe_path(queue_dir / f"{slug}.txt")
        post_path.write_text(tweet, encoding="utf-8")
        created += 1

    return created


# ─── CONNECTION 9: Content Farm → Affiliate Funnels ───────────────────────
# Add affiliate CTAs to content that mentions tools
def wire_content_to_affiliate():
    """
    Scan existing content for tool mentions, add affiliate tracking data.
    This creates a mapping file that the distribution engine can use.
    """
    tool_affiliates = {
        "surge.sh": {"type": "free_tool", "cta": "free to deploy"},
        "claude code": {"type": "tool", "cta": "claude.ai"},
        "instantly.ai": {"type": "affiliate_candidate", "cta": "cold email infra"},
        "visualping": {"type": "affiliate_candidate", "cta": "competitor monitoring"},
        "buffer": {"type": "free_tool", "cta": "social scheduling"},
        "gumroad": {"type": "marketplace", "cta": "sell digital products"},
        "formsubmit": {"type": "free_tool", "cta": "free form backend"},
    }

    queue_dir = safe_path(POSTING_QUEUE)
    if not queue_dir.exists():
        return 0

    affiliate_matches = []
    for post_file in queue_dir.iterdir():
        if post_file.suffix != ".txt":
            continue
        content = post_file.read_text(encoding="utf-8").lower()
        for tool, info in tool_affiliates.items():
            if tool.lower() in content:
                affiliate_matches.append({
                    "post_file": post_file.name,
                    "tool_mentioned": tool,
                    "affiliate_type": info["type"],
                    "cta_suggestion": info["cta"],
                    "detected_at": datetime.now().isoformat()
                })

    if affiliate_matches:
        mapping_path = safe_path(AUTOMATIONS / "agent" / "swarm" / "affiliate_content_mapping.json")
        mapping_path.write_text(json.dumps(affiliate_matches, indent=2))

    return len(affiliate_matches)


# ─── CONNECTION 10: Swarm Leads → Master Leads ────────────────────────────
# Swarm agents generate scored leads that need to merge into master
def wire_swarm_leads_to_master():
    leads_dir = safe_path(LEADS)
    swarm_files = list(leads_dir.glob("swarm_leads_*.csv"))
    if not swarm_files:
        return 0

    master_path = LEADS / "MASTER_LEADS.csv"
    existing = load_csv(master_path, max_rows=2000)
    existing_names = {r.get("business_name", "") for r in existing if r.get("business_name")}

    master_fields = ["business_name", "address", "phone", "website", "google_rating",
                     "review_count", "website_score", "signals_detected", "email_if_found",
                     "category", "city", "scraped_at"]

    total_added = 0
    for sf in swarm_files:
        rows = load_csv(sf, max_rows=200)
        new_leads = []
        for row in rows:
            name = row.get("name", row.get("business_name", ""))
            if not name or name in existing_names:
                continue
            lead = {
                "business_name": name,
                "address": "",
                "phone": row.get("phone", ""),
                "website": row.get("website", row.get("domain", "")),
                "google_rating": row.get("google_rating", ""),
                "review_count": row.get("google_review_count", ""),
                "website_score": row.get("total_score", row.get("composite_score", "")),
                "signals_detected": row.get("pain_signals", ""),
                "email_if_found": row.get("email", ""),
                "category": row.get("category", "swarm_lead"),
                "city": row.get("city", ""),
                "scraped_at": datetime.now().isoformat()
            }
            new_leads.append(lead)
            existing_names.add(name)

        if new_leads:
            append_csv(master_path, new_leads, master_fields)
            total_added += len(new_leads)

    return total_added


# ─── CONNECTION 11: Competitor Counter-Content → Posting Queue ────────────
# Competitor stalker generates counter-content markdown that needs to be split
# into individual posting queue files
def wire_counter_content_to_queue():
    content_dir = safe_path(PROJECT_ROOT / "CONTENT" / "social")
    counter_files = list(content_dir.glob("competitor_counter_content_*.md"))
    if not counter_files:
        return 0

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)
    existing_posts = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"} if queue_dir.exists() else set()

    created = 0
    for cf in counter_files:
        date_part = cf.stem.replace("competitor_counter_content_", "")
        text = cf.read_text(encoding="utf-8")

        # Split on "## TWEET" or "## THREAD" headers
        import re
        sections = re.split(r'## (TWEET \d+|THREAD \d+)', text)

        tweet_num = 0
        for i in range(1, len(sections), 2):
            header = sections[i].strip()
            body = sections[i + 1].strip() if i + 1 < len(sections) else ""

            # Extract the tweet text: skip the title line (e.g. "-- Opal price shock")
            lines = body.split("\n")
            tweet_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("**") or stripped.startswith("#") or stripped.startswith("---"):
                    continue
                if stripped.startswith("-- "):
                    continue
                if stripped:
                    tweet_lines.append(stripped)

            if not tweet_lines:
                continue

            tweet_text = "\n\n".join(tweet_lines)
            tweet_num += 1
            slug = f"counter_{date_part}_{tweet_num}"

            if slug in existing_posts:
                continue

            post_path = safe_path(queue_dir / f"{slug}.txt")
            post_path.write_text(tweet_text, encoding="utf-8")
            created += 1

    return created


# ─── CONNECTION 12: OpenClaw Previews → Content Farm ─────────────────────
# Deployed preview sites become "look what I built" case study content
def wire_openclaw_previews_to_content():
    state = load_json(AUTOMATIONS / "agent" / "autonomy" / "autonomy_state.json")
    openclaw = state.get("ventures", {}).get("auto_local_biz_openclaw_nationwide_9569", {})
    results = openclaw.get("results", [])

    if not results:
        return 0

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)
    existing_posts = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"} if queue_dir.exists() else set()

    created = 0
    for result in results:
        city = result.get("city", "")
        deploy_urls = result.get("deploy_urls", [])
        businesses = result.get("businesses_discovered", 0)
        previews = result.get("previews_built", 0)
        cycle = result.get("cycle", 0)

        if not deploy_urls:
            continue

        slug = f"openclaw_casestudy_{city.lower()}_{cycle}"
        if slug in existing_posts:
            continue

        urls_text = "\n".join(deploy_urls)
        tweet = (
            f"scraped {businesses} local businesses in {city}.\n\n"
            f"graded their websites. found {previews} with D/F scores.\n\n"
            f"built replacement sites in 2 hours:\n{urls_text}\n\n"
            f"cold emailed them with the demo link. $500 flat fee, no monthly.\n\n"
            f"this is the openclaw playbook. find broken sites, fix them before asking."
        )

        post_path = safe_path(queue_dir / f"{slug}.txt")
        post_path.write_text(tweet, encoding="utf-8")
        created += 1

    return created


# ─── CONNECTION 13: Trend Synthesis → Content Farm ────────────────────────
# High-confidence patterns from trend_synthesizer become content
def wire_trends_to_content():
    reports_dir = safe_path(REPORTS)
    trend_files = sorted(reports_dir.glob("trend_synthesis_*.md"), reverse=True)
    if not trend_files:
        return 0

    latest = trend_files[0]
    text = latest.read_text(encoding="utf-8")
    date_part = latest.stem.replace("trend_synthesis_", "")

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)
    existing_posts = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"} if queue_dir.exists() else set()

    # Extract patterns (lines starting with ### PATTERN)
    import re
    patterns = re.findall(r'### (PATTERN \d+): (.+?) \(Confidence: (\d+)%\)', text)

    created = 0
    for match in patterns:
        pattern_id, title, confidence = match
        conf = int(confidence)
        if conf < 85:
            continue

        slug = f"trend_{date_part}_{title.lower().replace(' ', '_').replace('/', '_').replace('=', '').replace('(', '').replace(')', '')[:30]}"
        if slug in existing_posts:
            continue

        # Extract the "What's changing" section for this pattern
        pattern_section = re.search(
            rf'### {re.escape(match[0])}: {re.escape(title)}.*?\*\*What\'s changing:\*\* (.+?)(?:\n\n|\*\*)',
            text, re.DOTALL
        )
        change_text = pattern_section.group(1).strip()[:200] if pattern_section else title

        tweet = (
            f"{title.lower()}.\n\n"
            f"{change_text}\n\n"
            f"confidence: {conf}%. based on analyzing ~5,000 rows across 8 data streams.\n\n"
            f"most people won't notice this shift for another 6 months."
        )

        post_path = safe_path(queue_dir / f"{slug}.txt")
        post_path.write_text(tweet, encoding="utf-8")
        created += 1

    return created


# ─── CONNECTION 14: Revenue Pipeline Urgency → Content Farm ──────────────
# $0 revenue status becomes authentic "building in public" content
def wire_revenue_urgency_to_content():
    pipeline = load_json(PROJECT_ROOT / "FINANCIALS" / "revenue_pipeline.json")
    total_revenue = pipeline.get("total_revenue", 0)
    days_at_zero = pipeline.get("days_at_zero_revenue", 0)
    pipeline_value = pipeline.get("total_pipeline_value_monthly", 0)
    assets_built = pipeline.get("pipeline_summary", {}).get("assets_built", 0)

    if total_revenue > 0 or days_at_zero < 7:
        return 0

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)
    existing_posts = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"} if queue_dir.exists() else set()

    slug = f"bip_day{days_at_zero}_revenue"
    if slug in existing_posts:
        return 0

    tweet = (
        f"day {days_at_zero} at $0 revenue.\n\n"
        f"{assets_built} assets built. {pipeline_value} monthly pipeline value.\n\n"
        f"the bottleneck isn't building. it's activating.\n\n"
        f"accounts, listings, posting. the boring stuff nobody wants to do.\n\n"
        f"building is the easy part. shipping is the hard part."
    )

    post_path = safe_path(queue_dir / f"{slug}.txt")
    post_path.write_text(tweet, encoding="utf-8")
    return 1


# ─── CONNECTION 15: Competitive Intel → Outreach Talking Points ──────────
# Competitor data enriches cold email personalization
def wire_intel_to_outreach_context():
    intel = load_csv(LEDGER / "COMPETITIVE_INTEL.csv", max_rows=200)
    if not intel:
        return 0

    # Build competitor context by category for outreach agents
    context = {}
    for row in intel:
        cat = row.get("category", "unknown")
        name = row.get("name", "")
        rating = row.get("rating", "")
        price = row.get("price", "")
        if not name:
            continue

        if cat not in context:
            context[cat] = []
        context[cat].append({
            "name": name,
            "rating": rating,
            "price": price,
            "last_updated": row.get("last_updated", "")
        })

    if not context:
        return 0

    # Write context file for outreach agents to reference
    context_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "outreach_competitor_context.json")
    context_path.parent.mkdir(parents=True, exist_ok=True)

    existing = {}
    if context_path.exists():
        try:
            existing = json.loads(context_path.read_text())
        except (json.JSONDecodeError, ValueError):
            existing = {}

    # Only count newly added categories
    new_cats = sum(1 for cat in context if cat not in existing)
    context["updated_at"] = datetime.now().isoformat()
    context_path.write_text(json.dumps(context, indent=2))

    return new_cats + len(context) - 1  # -1 for updated_at key


# ─── CONNECTION 16: Swarm Brain Decisions → Venture Config ────────────────
# Brain interval decisions auto-adjust venture intervals in autonomy_state
def wire_brain_decisions_to_ventures():
    decisions_path = AUTOMATIONS / "agent" / "swarm" / "brain_decisions.jsonl"
    if not decisions_path.exists():
        return 0

    state_path = AUTOMATIONS / "agent" / "autonomy" / "autonomy_state.json"
    state = load_json(state_path)
    if not state or "ventures" not in state:
        return 0

    # Map agent names to venture IDs
    agent_to_venture = {
        "lead_machine": "auto_outbound_cold_outreach_engine_9569",
        "content_compounder": "auto_content_niche_content_farm_9569",
        "trend_synthesizer": "auto_research_alpha_intelligence_9565",
        "cross_pollinator": None,  # meta agent, not a venture
        "image_factory": None,
        "video_factory": None,
    }

    lines = decisions_path.read_text().strip().split("\n")
    applied = 0

    for line in lines:
        try:
            dec = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue

        if dec.get("decision") != "adjust_interval":
            continue

        agent = dec.get("agent", "")
        new_interval = dec.get("new_interval", "")
        if not new_interval:
            continue

        # Parse interval string (e.g. "4h" -> 4)
        hours = 0
        if new_interval.endswith("h"):
            try:
                hours = int(new_interval[:-1])
            except ValueError:
                continue

        if hours <= 0:
            continue

        # Find matching venture
        venture_id = agent_to_venture.get(agent)
        if not venture_id or venture_id not in state["ventures"]:
            continue

        current = state["ventures"][venture_id].get("interval_hours", 0)
        if current != hours:
            state["ventures"][venture_id]["interval_hours"] = hours
            applied += 1

    if applied > 0:
        safe_path(state_path).write_text(json.dumps(state, indent=2))

    return applied


# ─── CONNECTION 17: Gap Report → Human Action Queue ──────────────────────
# Parse gap report into a concise, prioritized action file for the human
def wire_gap_report_to_action_queue():
    import re
    report_files = sorted(REPORTS.glob("gap_report_*.md"), reverse=True)
    if not report_files:
        return 0

    latest = report_files[0]
    text = latest.read_text(encoding="utf-8")

    # Extract GAP sections with revenue impact
    gaps = re.findall(
        r'### GAP (\d+): (.+?) \((\w+)\)\n(.*?)(?=### GAP|\Z)',
        text, re.DOTALL
    )

    if not gaps:
        return 0

    action_queue = []
    for gap_num, title, severity, body in gaps:
        # Extract action line
        action_match = re.search(r'\*\*Action:\*\* (.+)', body)
        revenue_match = re.search(r'\*\*Revenue impact:\*\* (.+)', body)
        action = action_match.group(1).strip() if action_match else "See gap report"
        revenue = revenue_match.group(1).strip() if revenue_match else ""

        action_queue.append({
            "priority": int(gap_num),
            "title": title.strip(),
            "severity": severity,
            "action": action,
            "revenue_impact": revenue,
            "source": latest.name
        })

    if action_queue:
        queue_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "human_action_queue.json")
        queue_path.parent.mkdir(parents=True, exist_ok=True)

        existing = []
        if queue_path.exists():
            try:
                existing = json.loads(queue_path.read_text())
            except (json.JSONDecodeError, ValueError):
                existing = []

        existing_titles = {a.get("title", "") for a in existing}
        new_actions = [a for a in action_queue if a["title"] not in existing_titles]

        if new_actions:
            all_actions = existing + new_actions
            all_actions.sort(key=lambda x: x.get("priority", 99))
            queue_path.write_text(json.dumps(all_actions, indent=2))

        return len(new_actions)
    return 0


# ─── CONNECTION 18: Monetization Audit → Deployment Tasks ────────────────
# Parse monetization audit into agent-executable deployment tasks
def wire_monetization_audit_to_tasks():
    import re
    audit_files = sorted(REPORTS.glob("app_monetization_audit_*.md"), reverse=True)
    if not audit_files:
        return 0

    latest = audit_files[0]
    text = latest.read_text(encoding="utf-8")

    # Extract "WHAT AGENT CAN DO NOW" section
    agent_section = re.search(
        r'## WHAT AGENT CAN DO NOW.*?\n(.*?)(?=\n##|\Z)',
        text, re.DOTALL
    )

    tasks = []
    if agent_section:
        lines = agent_section.group(1).strip().split("\n")
        for line in lines:
            line = line.strip().lstrip("- ")
            if line and len(line) > 10:
                tasks.append({
                    "task": line,
                    "source": "monetization_audit",
                    "status": "PENDING",
                    "created_at": datetime.now().isoformat()
                })

    # Also extract PRIORITY FIXES
    fix_section = re.search(
        r'## PRIORITY FIXES\n(.*?)(?=\n##|\Z)',
        text, re.DOTALL
    )
    if fix_section:
        lines = fix_section.group(1).strip().split("\n")
        for line in lines:
            line = line.strip().lstrip("0123456789. ")
            if line and len(line) > 10:
                blocked = "blocked" in line.lower()
                tasks.append({
                    "task": line,
                    "source": "monetization_audit",
                    "status": "BLOCKED" if blocked else "PENDING",
                    "created_at": datetime.now().isoformat()
                })

    if tasks:
        task_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "monetization_tasks.json")
        task_path.parent.mkdir(parents=True, exist_ok=True)

        existing = []
        if task_path.exists():
            try:
                existing = json.loads(task_path.read_text())
            except (json.JSONDecodeError, ValueError):
                existing = []

        existing_tasks = {t.get("task", "") for t in existing}
        new_tasks = [t for t in tasks if t["task"] not in existing_tasks]

        if new_tasks:
            task_path.write_text(json.dumps(existing + new_tasks, indent=2))

        return len(new_tasks)
    return 0


# ─── CONNECTION 19: Reddit Pain Points → Product Demand Signals ──────────
# Aggregate Reddit complaints into product demand signals for Digital Products
def wire_reddit_to_product_demand():
    reddit_dir = safe_path(REDDIT_OUTPUT)
    if not reddit_dir.exists():
        return 0

    json_files = sorted(
        [f for f in reddit_dir.iterdir() if f.name.startswith("reddit_") and f.suffix == ".json"],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )[:3]  # Last 3 scrapes

    if not json_files:
        return 0

    pain_categories = {}
    pain_keywords = {
        "slow": "performance", "broken": "reliability", "expensive": "pricing",
        "complicated": "ux", "confusing": "ux", "wish": "feature_gap",
        "alternative": "competitor_gap", "hate": "frustration",
        "switched from": "churn_signal", "looking for": "demand",
        "need": "demand", "frustrated": "frustration", "annoying": "ux",
        "overpriced": "pricing", "cheaper": "pricing", "free": "pricing",
    }

    for jf in json_files:
        try:
            with open(jf) as f:
                posts = json.load(f)
        except (json.JSONDecodeError, ValueError):
            continue

        if not isinstance(posts, list):
            continue

        for post in posts:
            if not isinstance(post, dict):
                continue
            text = f"{post.get('title', '')} {post.get('selftext', '')}".lower()
            sub = post.get("subreddit", "")
            score = post.get("score", 0)

            for keyword, category in pain_keywords.items():
                if keyword in text:
                    if category not in pain_categories:
                        pain_categories[category] = {"count": 0, "examples": [], "subreddits": set()}
                    pain_categories[category]["count"] += 1
                    pain_categories[category]["subreddits"].add(sub)
                    if len(pain_categories[category]["examples"]) < 3 and score > 5:
                        pain_categories[category]["examples"].append({
                            "title": post.get("title", "")[:100],
                            "sub": sub,
                            "score": score
                        })

    if not pain_categories:
        return 0

    # Convert sets to lists for JSON
    for cat in pain_categories:
        pain_categories[cat]["subreddits"] = list(pain_categories[cat]["subreddits"])

    demand_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "product_demand_signals.json")
    demand_path.parent.mkdir(parents=True, exist_ok=True)

    existing = {}
    if demand_path.exists():
        try:
            existing = json.loads(demand_path.read_text())
        except (json.JSONDecodeError, ValueError):
            existing = {}

    # Merge: increment counts, add new examples
    for cat, data in pain_categories.items():
        if cat in existing:
            existing[cat]["count"] = existing[cat].get("count", 0) + data["count"]
            existing[cat]["subreddits"] = list(set(existing[cat].get("subreddits", []) + data["subreddits"]))
            ex_titles = {e.get("title", "") for e in existing[cat].get("examples", [])}
            for ex in data["examples"]:
                if ex["title"] not in ex_titles and len(existing[cat].get("examples", [])) < 5:
                    existing[cat].setdefault("examples", []).append(ex)
        else:
            existing[cat] = data

    existing["updated_at"] = datetime.now().isoformat()
    demand_path.write_text(json.dumps(existing, indent=2))

    return len(pain_categories)


# ─── CONNECTION 20: Content Farm → App Traffic (inject app URLs) ─────────
# Scan posting queue for app-related content and inject live app URLs
def wire_content_to_app_traffic():
    pipeline = load_json(PROJECT_ROOT / "FINANCIALS" / "revenue_pipeline.json")
    apps = pipeline.get("categories", {}).get("apps_deployed", {})
    app_urls = apps.get("urls", {})

    if not app_urls:
        return 0

    queue_dir = safe_path(POSTING_QUEUE)
    if not queue_dir.exists():
        return 0

    # Map keywords to app URLs
    app_keywords = {}
    for app_name, url in app_urls.items():
        keywords = app_name.lower().replace("-", " ").replace("_", " ").split()
        for kw in keywords:
            if len(kw) > 3:
                app_keywords[kw] = {"name": app_name, "url": url}

    injected = 0
    for post_file in queue_dir.iterdir():
        if post_file.suffix != ".txt":
            continue

        content = post_file.read_text(encoding="utf-8")
        if "surge.sh" in content or "http" in content:
            continue  # Already has URLs

        content_lower = content.lower()
        for kw, info in app_keywords.items():
            if kw in content_lower and info["url"] not in content:
                content += f"\n\n{info['url']}"
                post_file.write_text(content, encoding="utf-8")
                injected += 1
                break

    return injected


# ─── CONNECTION 21: Brain Priority Shifts → Content Farm ─────────────────
# Brain strategic decisions become "building in public" content
def wire_brain_insights_to_content():
    decisions_path = AUTOMATIONS / "agent" / "swarm" / "brain_decisions.jsonl"
    if not decisions_path.exists():
        return 0

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)
    existing_posts = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"} if queue_dir.exists() else set()

    lines = decisions_path.read_text().strip().split("\n")
    created = 0

    for line in lines:
        try:
            dec = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue

        if dec.get("decision") != "priority_shift":
            continue

        reason = dec.get("reason", "")
        ts = dec.get("ts", "")
        date_part = ts[:10].replace("-", "") if ts else "unknown"

        slug = f"brain_insight_{date_part}_{created}"
        if slug in existing_posts:
            continue

        # Extract key numbers from the reason
        tweet = reason[:280].replace("ENTIRE", "entire").replace("ALL", "all").replace("STOP", "stop")
        tweet = f"swarm brain cycle insight:\n\n{tweet}\n\nthis is what happens when you let AI agents manage themselves. they figure out what matters."

        if len(tweet) > 500:
            tweet = tweet[:497] + "..."

        post_path = safe_path(queue_dir / f"{slug}.txt")
        post_path.write_text(tweet, encoding="utf-8")
        created += 1

    return created


# ─── CONNECTION 22: Posting Queue → Buffer CSV ────────────────────────────
# Auto-formats queued posts into a Buffer-compatible CSV for scheduled posting
def wire_posting_queue_to_buffer():
    queue_dir = safe_path(POSTING_QUEUE)
    if not queue_dir.exists():
        return 0

    buffer_path = safe_path(CONTENT / "printmaxxer" / "BUFFER_EXPORT_20260308.csv")
    existing_slugs = set()
    if buffer_path.exists():
        existing = load_csv(buffer_path, max_rows=1000)
        existing_slugs = {r.get("slug", "") for r in existing}

    new_rows = []
    for f in sorted(queue_dir.iterdir()):
        if f.suffix != ".txt":
            continue
        if f.stem in existing_slugs:
            continue
        text = f.read_text(encoding="utf-8", errors="replace").strip()
        if not text or len(text) < 20:
            continue
        # Truncate to 280 chars for single tweets
        tweet_text = text[:280] if "\n\n" not in text[:100] else text
        new_rows.append({
            "slug": f.stem,
            "text": tweet_text[:500],
            "platform": "twitter",
            "status": "READY",
            "source_file": str(f.name),
            "added_at": datetime.now().isoformat()
        })

    if new_rows:
        fieldnames = ["slug", "text", "platform", "status", "source_file", "added_at"]
        append_csv(buffer_path, new_rows, fieldnames)

    return len(new_rows)


# ─── CONNECTION 23: Monetization Tasks → Asset Deployer Queue ─────────────
# Reads PENDING monetization tasks and creates an agent-executable task queue
def wire_monetization_tasks_to_deployer():
    tasks_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "monetization_tasks.json")
    if not tasks_path.exists():
        return 0

    try:
        tasks = json.loads(tasks_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return 0

    if not isinstance(tasks, list):
        return 0

    deployer_queue_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "deployer_task_queue.json")
    existing_tasks = []
    if deployer_queue_path.exists():
        try:
            existing_tasks = json.loads(deployer_queue_path.read_text())
        except (json.JSONDecodeError, ValueError):
            existing_tasks = []
    existing_ids = {t.get("task_id", "") for t in existing_tasks}

    new_tasks = []
    for task in tasks:
        status = task.get("status", "")
        task_id = task.get("task_id", task.get("task", "")[:40])
        if status == "PENDING" and task_id not in existing_ids:
            new_tasks.append({
                "task_id": task_id,
                "description": task.get("task", task.get("description", "")),
                "source": "monetization_audit",
                "priority": task.get("priority", "MEDIUM"),
                "status": "QUEUED",
                "queued_at": datetime.now().isoformat()
            })

    if new_tasks:
        all_tasks = existing_tasks + new_tasks
        deployer_queue_path.write_text(json.dumps(all_tasks, indent=2))

    return len(new_tasks)


# ─── CONNECTION 24: Product Demand Signals → Digital Products Config ──────
# Feeds demand signals into Digital Products venture config for find_demand step
def wire_demand_signals_to_products():
    signals_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "product_demand_signals.json")
    if not signals_path.exists():
        return 0

    try:
        signals = json.loads(signals_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return 0

    # Read autonomy state, inject demand signals into Digital Products config
    state_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "autonomy_state.json")
    if not state_path.exists():
        return 0

    try:
        state = json.loads(state_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return 0

    product_venture = state.get("ventures", {}).get("auto_product_digital_products_9788", {})
    config = product_venture.get("config", {})

    # Inject top demand categories into config
    demand_categories = []
    if isinstance(signals, dict):
        for cat, items in signals.items():
            if isinstance(items, list):
                demand_categories.append({
                    "category": cat,
                    "signal_count": len(items),
                    "top_signal": items[0] if items else ""
                })
    elif isinstance(signals, list):
        demand_categories = signals[:10]

    if not demand_categories:
        return 0

    existing_demand = config.get("demand_signals", [])
    existing_cats = {d.get("category", "") if isinstance(d, dict) else str(d) for d in existing_demand}
    new_demand = [d for d in demand_categories
                  if (d.get("category", "") if isinstance(d, dict) else str(d)) not in existing_cats]

    if new_demand:
        config["demand_signals"] = existing_demand + new_demand
        config["demand_updated"] = datetime.now().isoformat()
        product_venture["config"] = config
        state["ventures"]["auto_product_digital_products_9788"] = product_venture
        state_path.write_text(json.dumps(state, indent=2))

    return len(new_demand)


# ─── CONNECTION 25: Trend Signals → Cold Outreach Angles ─────────────────
# Hot trends become outreach angle briefs for the Cold Outreach Engine
def wire_trends_to_outreach():
    trends = load_csv(LEDGER / "TREND_SIGNALS.csv", max_rows=100)
    if not trends:
        return 0

    angles_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "outreach_trend_angles.json")
    existing_angles = []
    if angles_path.exists():
        try:
            existing_angles = json.loads(angles_path.read_text())
        except (json.JSONDecodeError, ValueError):
            existing_angles = []
    existing_signals = {a.get("signal", "") for a in existing_angles}

    new_angles = []
    for row in trends:
        score = 0
        try:
            score = int(row.get("score", "0") or "0")
        except (ValueError, TypeError):
            pass
        signal = row.get("signal", "")
        source = row.get("source", "")
        signal_type = row.get("signal_type", "")

        if score < 55 or not signal:
            continue
        if signal[:60] in existing_signals:
            continue
        # Filter for business-relevant subreddits via source
        biz_sources = {"smallbusiness", "entrepreneur", "saas", "sideproject",
                       "indiehackers", "webdev", "startups", "passive_income",
                       "microsaas", "freelance", "affiliatemarketing", "forhire",
                       "digitalnomad", "dropship"}
        source_lower = source.lower()
        is_biz = any(s in source_lower for s in biz_sources)
        if not is_biz:
            continue

        # Convert trend into outreach angle
        new_angles.append({
            "signal": signal[:60],
            "full_signal": signal[:200],
            "source": source,
            "signal_type": signal_type,
            "score": score,
            "outreach_angle": f"Re: {signal[:80]} — we build tools for this",
            "detected_at": datetime.now().isoformat()
        })

    if new_angles:
        all_angles = existing_angles + new_angles[-20:]  # cap at 20 new per cycle
        angles_path.parent.mkdir(parents=True, exist_ok=True)
        angles_path.write_text(json.dumps(all_angles, indent=2))

    return len(new_angles[:20])


# ─── CONNECTION 26: Alpha Clusters → Product Specs ───────────────────────
# When 10+ alpha entries share a topic, auto-generate a Gumroad product spec
def wire_alpha_clusters_to_product_specs():
    alpha = load_csv(LEDGER / "ALPHA_STAGING.csv", max_rows=500)
    if len(alpha) < 10:
        return 0

    # Cluster by category/tags
    clusters = {}
    for row in alpha:
        status = row.get("status", "")
        if status not in ("APPROVED", "ENGAGEMENT_BAIT", "REPURPOSE_ONLY"):
            continue
        category = row.get("category", row.get("route_target", "general"))
        if not category:
            category = "general"
        clusters.setdefault(category, []).append(row)

    specs_dir = safe_path(AUTOMATIONS / "agent" / "autonomy" / "product_specs")
    specs_dir.mkdir(parents=True, exist_ok=True)

    new_specs = 0
    for cat, items in clusters.items():
        if len(items) < 10:
            continue

        slug = cat.lower().replace(" ", "_").replace("/", "_")[:30]
        spec_path = specs_dir / f"spec_{slug}.json"
        if spec_path.exists():
            continue

        # Generate product spec from alpha cluster
        sample_titles = [
            (r.get("tactic", "") or r.get("extracted_method", "") or
             r.get("title", "") or r.get("signal", "") or r.get("reviewer_notes", ""))[:80]
            for r in items[:10]
        ]
        sample_titles = [s for s in sample_titles if s.strip()]
        spec = {
            "category": cat,
            "alpha_count": len(items),
            "sample_entries": sample_titles,
            "suggested_product": f"The Ultimate {cat.replace('_', ' ').title()} Playbook",
            "format": "PDF guide + templates",
            "price_range": "$19-39",
            "platform": "gumroad",
            "status": "SPEC_GENERATED",
            "generated_at": datetime.now().isoformat()
        }
        spec_path.write_text(json.dumps(spec, indent=2))
        new_specs += 1

    return new_specs


# ─── CONNECTION 27: Scored Leads → Content Farm Case Studies ──────────────
# High-scoring leads with deployed previews become case study content
def wire_leads_to_case_studies():
    leads = load_csv(LEADS / "SCORED_LEADS.csv", max_rows=200)
    if not leads:
        # Try master leads
        leads = load_csv(LEADS / "MASTER_LEADS.csv", max_rows=200)
    if not leads:
        return 0

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)

    existing_posts = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"}

    new_posts = 0
    for row in leads:
        biz_name = row.get("business_name", row.get("name", ""))
        city = row.get("city", "")
        grade = row.get("grade", row.get("website_grade", ""))
        deploy_url = row.get("deploy_url", row.get("preview_url", ""))

        if not biz_name or not city:
            continue

        slug = f"case_study_{biz_name}_{city}".replace(" ", "_").replace("/", "_")[:60].lower()
        if slug in existing_posts:
            continue

        # Only create case studies for leads where we built a preview
        if not deploy_url:
            continue

        tweet = (
            f"found a {grade or 'D'}-grade website for a {city} business.\n\n"
            f"rebuilt it in 20 minutes with ai. side by side comparison:\n\n"
            f"{deploy_url}\n\n"
            f"most local businesses have terrible websites and don't know it. "
            f"that's the opportunity."
        )

        post_path = queue_dir / f"{slug}.txt"
        post_path.write_text(tweet, encoding="utf-8")
        new_posts += 1

        if new_posts >= 5:
            break

    return new_posts


# ─── CONNECTION 28: Product Specs → Digital Products Pipeline ─────────────
# Auto-generated product specs feed the Digital Products venture's find_demand step
def wire_product_specs_to_digital_products():
    specs_dir = safe_path(AUTOMATIONS / "agent" / "autonomy" / "product_specs")
    if not specs_dir.exists():
        return 0

    spec_files = list(specs_dir.glob("spec_*.json"))
    if not spec_files:
        return 0

    state_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "autonomy_state.json")
    if not state_path.exists():
        return 0

    try:
        state = json.loads(state_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return 0

    product_venture = state.get("ventures", {}).get("auto_product_digital_products_9788", {})
    config = product_venture.get("config", {})
    existing_specs = config.get("product_specs", [])
    existing_names = {s.get("suggested_product", "") for s in existing_specs if isinstance(s, dict)}

    new_specs = []
    for sf in spec_files:
        try:
            spec = json.loads(sf.read_text())
        except (json.JSONDecodeError, ValueError):
            continue
        name = spec.get("suggested_product", "")
        if name and name not in existing_names:
            new_specs.append({
                "suggested_product": name,
                "category": spec.get("category", ""),
                "alpha_count": spec.get("alpha_count", 0),
                "price_range": spec.get("price_range", "$19-39"),
                "format": spec.get("format", "PDF"),
                "spec_file": sf.name
            })
            existing_names.add(name)

    if new_specs:
        config["product_specs"] = existing_specs + new_specs
        config["specs_updated"] = datetime.now().isoformat()
        product_venture["config"] = config
        state["ventures"]["auto_product_digital_products_9788"] = product_venture
        state_path.write_text(json.dumps(state, indent=2))

    return len(new_specs)


# ─── CONNECTION 29: Deployer Queue → Execution Manifest ──────────────────
# Reads deployer task queue and creates an execution manifest for asset_deployer
def wire_deployer_queue_to_manifest():
    queue_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "deployer_task_queue.json")
    if not queue_path.exists():
        return 0

    try:
        tasks = json.loads(queue_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return 0

    if not isinstance(tasks, list):
        return 0

    queued = [t for t in tasks if t.get("status") == "QUEUED"]
    if not queued:
        return 0

    manifest_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "execution_manifest.json")
    existing_manifest = []
    if manifest_path.exists():
        try:
            existing_manifest = json.loads(manifest_path.read_text())
        except (json.JSONDecodeError, ValueError):
            existing_manifest = []
    existing_ids = {m.get("task_id", "") for m in existing_manifest}

    new_entries = []
    for task in queued:
        tid = task.get("task_id", "")
        if tid and tid not in existing_ids:
            new_entries.append({
                "task_id": tid,
                "description": task.get("description", ""),
                "source": task.get("source", ""),
                "priority": task.get("priority", "MEDIUM"),
                "status": "READY_FOR_EXECUTION",
                "assigned_agent": "asset_deployer",
                "created_at": datetime.now().isoformat()
            })

    if new_entries:
        all_entries = existing_manifest + new_entries
        manifest_path.write_text(json.dumps(all_entries, indent=2))

    return len(new_entries)


# ─── CONNECTION 30: Compound Content → Posting Queue ─────────────────────
# Splits compound_content_*.md files into individual posting queue entries
def wire_compound_content_to_queue():
    import re
    content_dir = safe_path(PROJECT_ROOT / "CONTENT" / "social")
    compound_files = list(content_dir.glob("compound_content_*.md"))
    if not compound_files:
        return 0

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)
    existing_posts = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"} if queue_dir.exists() else set()

    created = 0
    for cf in compound_files:
        date_part = cf.stem.replace("compound_content_", "")
        text = cf.read_text(encoding="utf-8")

        # Split on ### Tweet headers
        tweet_sections = re.split(r'### Tweet \d+', text)
        tweet_num = 0

        for section in tweet_sections[1:]:
            tweet_num += 1
            lines = section.strip().split("\n")
            tweet_lines = []
            past_title = False
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    if past_title:
                        tweet_lines.append("")
                    continue
                if stripped.startswith("- ") and not past_title:
                    past_title = True
                    continue
                if stripped.startswith("#") or stripped.startswith("---"):
                    break
                past_title = True
                tweet_lines.append(stripped)

            tweet_text = "\n\n".join([l for l in tweet_lines if l]).strip()
            if not tweet_text or len(tweet_text) < 30:
                continue

            slug = f"compound_{date_part}_{tweet_num}"
            if slug in existing_posts:
                continue

            post_path = safe_path(queue_dir / f"{slug}.txt")
            post_path.write_text(tweet_text, encoding="utf-8")
            created += 1

    return created


# ─── CONNECTION 31: Qualified Leads → OpenClaw Priority Queue ────────────
# High-score qualified leads with emails feed OpenClaw for targeted preview builds
def wire_qualified_leads_to_openclaw():
    qualified_path = LEADS / "auto_outbound_cold_outreach_engine_9569" / "qualified.csv"
    if not qualified_path.exists():
        return 0

    qualified = load_csv(qualified_path, max_rows=100)
    if not qualified:
        return 0

    hot_targets = []
    for row in qualified:
        email = row.get("email", "")
        score = 0
        try:
            score = float(row.get("composite_score", "0") or "0")
        except (ValueError, TypeError):
            pass
        if email and score >= 7.5:
            hot_targets.append({
                "business_name": row.get("business_name", ""),
                "website": row.get("website", ""),
                "city": row.get("city", ""),
                "state": row.get("state", ""),
                "category": row.get("category", ""),
                "email": email,
                "composite_score": score,
                "issues": row.get("issues", ""),
                "estimated_value": row.get("estimated_value", ""),
                "source": "qualified_leads_crossfeed"
            })

    if not hot_targets:
        return 0

    priority_path = safe_path(LEADS / "auto_local_biz_openclaw_nationwide_9569" / "priority_targets.json")
    priority_path.parent.mkdir(parents=True, exist_ok=True)

    existing_targets = []
    if priority_path.exists():
        try:
            existing_targets = json.loads(priority_path.read_text())
        except (json.JSONDecodeError, ValueError):
            existing_targets = []
    existing_websites = {t.get("website", "") for t in existing_targets}

    new_targets = [t for t in hot_targets if t["website"] and t["website"] not in existing_websites]

    if new_targets:
        all_targets = existing_targets + new_targets
        all_targets.sort(key=lambda x: x.get("composite_score", 0), reverse=True)
        priority_path.write_text(json.dumps(all_targets, indent=2))

    return len(new_targets)


# ─── CONNECTION 32: Trend Synthesis → Venture Cross-Pollination Angles ───
# Extract cross-pollination directives from trend synthesis reports
def wire_trend_synthesis_to_ventures():
    import re
    reports_dir = safe_path(REPORTS)
    trend_files = sorted(reports_dir.glob("trend_synthesis_*.md"), reverse=True)
    if not trend_files:
        return 0

    latest = trend_files[0]
    text = latest.read_text(encoding="utf-8")

    cross_sections = re.findall(
        r'\*\*Cross-pollination:\*\*\s*(.+?)(?:\n\n|\n---|\n##)',
        text, re.DOTALL
    )

    if not cross_sections:
        return 0

    angles_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "trend_cross_pollination.json")
    existing = []
    if angles_path.exists():
        try:
            existing = json.loads(angles_path.read_text())
        except (json.JSONDecodeError, ValueError):
            existing = []
    existing_texts = {a.get("directive", "")[:60] for a in existing}

    new_angles = []
    for section in cross_sections:
        directives = [line.strip().lstrip("- ").lstrip("0123456789. ")
                      for line in section.strip().split("\n")
                      if line.strip() and len(line.strip()) > 20]

        for directive in directives:
            if directive[:60] not in existing_texts:
                affected = []
                lower = directive.lower()
                if any(kw in lower for kw in ["app", "build", "pwa"]):
                    affected.append("APP_FACTORY")
                if any(kw in lower for kw in ["content", "post", "thread", "tweet"]):
                    affected.append("CONTENT")
                if any(kw in lower for kw in ["product", "gumroad", "playbook"]):
                    affected.append("PRODUCT")
                if any(kw in lower for kw in ["outreach", "cold", "email", "client"]):
                    affected.append("OUTBOUND")
                if any(kw in lower for kw in ["monetiz", "affiliat", "revenue", "pricing"]):
                    affected.append("MONETIZE")

                new_angles.append({
                    "directive": directive[:200],
                    "affected_ventures": affected or ["ALL"],
                    "source": latest.name,
                    "detected_at": datetime.now().isoformat()
                })
                existing_texts.add(directive[:60])

    if new_angles:
        all_angles = (existing + new_angles)[-50:]
        angles_path.parent.mkdir(parents=True, exist_ok=True)
        angles_path.write_text(json.dumps(all_angles, indent=2))

    return len(new_angles)


# ─── CONNECTION 33: Alpha Content Cycles → Posting Queue ─────────────────
# Splits alpha_content_*.md and alpha_research_*.md into individual queue entries
def wire_alpha_content_to_queue():
    import re
    content_dir = safe_path(PROJECT_ROOT / "CONTENT" / "social")
    alpha_files = list(content_dir.glob("alpha_content_*.md")) + list(content_dir.glob("alpha_research_*.md"))
    if not alpha_files:
        return 0

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)
    existing_posts = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"} if queue_dir.exists() else set()

    created = 0
    for af in alpha_files:
        date_part = af.stem.replace("alpha_content_", "").replace("alpha_research_", "").replace("cycle_", "")
        text = af.read_text(encoding="utf-8")

        sections = re.split(r'###?\s+(?:Tweet|Post|TWEET|POST)\s*\d*', text)
        tweet_num = 0

        for section in sections[1:]:
            tweet_num += 1
            lines = section.strip().split("\n")
            tweet_lines = []
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    tweet_lines.append("")
                    continue
                if stripped.startswith("#") or stripped.startswith("---") or stripped.startswith("**Status"):
                    break
                if stripped.startswith("- ") and len(stripped) < 50:
                    continue
                tweet_lines.append(stripped)

            tweet_text = "\n\n".join([l for l in tweet_lines if l]).strip()
            if not tweet_text or len(tweet_text) < 30:
                continue

            slug = f"alphacontent_{date_part}_{tweet_num}"
            if slug in existing_posts:
                continue

            post_path = safe_path(queue_dir / f"{slug}.txt")
            post_path.write_text(tweet_text, encoding="utf-8")
            created += 1

    return created


# ─── CONNECTION 34: Freelance Responses → Content Farm ────────────────────
# Freelance response drafts become proof-of-work content for social
def wire_freelance_responses_to_content():
    responses_dir = safe_path(PROJECT_ROOT / "CONTENT" / "freelance_responses")
    if not responses_dir.exists():
        return 0

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)
    existing_posts = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"} if queue_dir.exists() else set()

    created = 0
    for resp_file in sorted(responses_dir.glob("response_*.md"))[-20:]:
        # Extract job title from filename
        name = resp_file.stem.replace("response_", "")
        date_part = name[-8:] if len(name) > 8 else ""
        title_part = name[:-9] if len(name) > 9 else name
        title_clean = title_part.replace("_", " ").strip()[:80]

        slug = f"freelance_proof_{date_part}_{hash(title_part) % 10000}"
        if slug in existing_posts:
            continue

        # Read first 200 chars to extract the gist
        try:
            content = resp_file.read_text(encoding="utf-8")[:500]
        except Exception:
            continue

        is_hiring = "[HIRING]" in title_clean.upper() or "[Hiring]" in title_clean
        if is_hiring:
            tweet = (
                f"spotted a live gig on reddit: {title_clean[:60]}\n\n"
                f"drafted a response in 3 minutes with ai-assisted portfolio generation.\n\n"
                f"most freelancers spend 30 min per application. i batch 10 in the same time.\n\n"
                f"the game is speed + volume + quality samples."
            )
        else:
            tweet = (
                f"another freelance opportunity processed: {title_clean[:60]}\n\n"
                f"automated pipeline: scrape → qualify → draft response → attach sample.\n\n"
                f"while other freelancers are manually browsing job boards, "
                f"my system surfaces and responds to opportunities automatically."
            )

        post_path = safe_path(queue_dir / f"{slug}.txt")
        post_path.write_text(tweet, encoding="utf-8")
        existing_posts.add(slug)
        created += 1

        if created >= 5:
            break

    return created


# ─── CONNECTION 35: Freelance Demand Scan → App Factory Gaps ──────────────
# What people pay for on r/forhire informs app factory about real demand
def wire_freelance_demand_to_app_factory():
    demand = load_csv(LEDGER / "FREELANCE_DEMAND_SCAN.csv", max_rows=500)
    if not demand:
        return 0

    # Aggregate demand signals by service type
    service_demand = {}
    for row in demand:
        services = row.get("matched_services", "")
        budget = row.get("budget", "0")
        score = row.get("score", "0")
        title = row.get("title", "")
        try:
            budget_num = int(str(budget).replace("$", "").replace(",", "").strip() or "0")
        except (ValueError, TypeError):
            budget_num = 0
        try:
            score_num = int(str(score).strip() or "0")
        except (ValueError, TypeError):
            score_num = 0

        for svc in services.split(","):
            svc = svc.strip()
            if not svc:
                continue
            if svc not in service_demand:
                service_demand[svc] = {"count": 0, "total_budget": 0, "max_score": 0, "examples": []}
            service_demand[svc]["count"] += 1
            service_demand[svc]["total_budget"] += budget_num
            service_demand[svc]["max_score"] = max(service_demand[svc]["max_score"], score_num)
            if len(service_demand[svc]["examples"]) < 3:
                service_demand[svc]["examples"].append(title[:80])

    if not service_demand:
        return 0

    # Convert to app factory gaps
    gaps = []
    for svc, data in sorted(service_demand.items(), key=lambda x: x[1]["count"], reverse=True):
        if data["count"] >= 3:  # At least 3 demand signals
            gaps.append({
                "service_type": svc,
                "demand_count": data["count"],
                "total_budget_seen": data["total_budget"],
                "max_score": data["max_score"],
                "gap_type": "FREELANCE_DEMAND",
                "opportunity": f"Productize '{svc}' service into SaaS/tool (seen {data['count']} times on r/forhire)",
                "examples": data["examples"],
                "detected_at": datetime.now().isoformat()
            })

    if not gaps:
        return 0

    gap_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "freelance_demand_gaps.json")
    gap_path.parent.mkdir(parents=True, exist_ok=True)

    existing = []
    if gap_path.exists():
        try:
            existing = json.loads(gap_path.read_text())
        except (json.JSONDecodeError, ValueError):
            existing = []

    existing_services = {g.get("service_type", "") for g in existing}
    new_gaps = [g for g in gaps if g["service_type"] not in existing_services]

    if new_gaps:
        all_gaps = existing + new_gaps
        gap_path.write_text(json.dumps(all_gaps, indent=2))

    return len(new_gaps)


# ─── CONNECTION 36: Auto-Ops App Specs → App Factory Queue ────────────────
# Auto-generated app specs feed into app factory's build queue
def wire_auto_ops_specs_to_app_factory():
    specs_dir = safe_path(AUTOMATIONS / "auto_ops" / "app_specs")
    if not specs_dir.exists():
        return 0

    spec_files = list(specs_dir.glob("APP_SPEC_*.md"))
    if not spec_files:
        return 0

    queue_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "app_factory_spec_queue.json")
    queue_path.parent.mkdir(parents=True, exist_ok=True)

    existing_queue = []
    if queue_path.exists():
        try:
            existing_queue = json.loads(queue_path.read_text())
        except (json.JSONDecodeError, ValueError):
            existing_queue = []
    existing_files = {e.get("source_file", "") for e in existing_queue}

    new_specs = []
    for sf in spec_files:
        if sf.name in existing_files:
            continue

        try:
            content = sf.read_text(encoding="utf-8")[:1000]
        except Exception:
            continue

        # Extract title from first heading
        title = sf.name
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip()
                break

        new_specs.append({
            "source_file": sf.name,
            "title": title[:100],
            "status": "QUEUED",
            "priority": "MEDIUM",
            "added_at": datetime.now().isoformat()
        })

    if new_specs:
        all_specs = existing_queue + new_specs
        queue_path.write_text(json.dumps(all_specs, indent=2))

    return len(new_specs)


# ─── CONNECTION 37: Auto-Ops Email Templates → Cold Outreach ─────────────
# Email templates feed into outreach engine's template library
def wire_auto_ops_emails_to_outreach():
    templates_dir = safe_path(AUTOMATIONS / "auto_ops" / "email_templates")
    if not templates_dir.exists():
        return 0

    template_files = list(templates_dir.glob("EMAIL_*.md"))
    if not template_files:
        return 0

    library_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "email_template_library.json")
    library_path.parent.mkdir(parents=True, exist_ok=True)

    existing_lib = []
    if library_path.exists():
        try:
            existing_lib = json.loads(library_path.read_text())
        except (json.JSONDecodeError, ValueError):
            existing_lib = []
    existing_files = {e.get("source_file", "") for e in existing_lib}

    new_templates = []
    for tf in template_files:
        if tf.name in existing_files:
            continue

        try:
            content = tf.read_text(encoding="utf-8")[:2000]
        except Exception:
            continue

        # Extract subject line if present
        subject = ""
        for line in content.split("\n"):
            lower = line.lower().strip()
            if lower.startswith("subject:") or lower.startswith("**subject"):
                subject = line.split(":", 1)[-1].strip().strip("*").strip()
                break

        new_templates.append({
            "source_file": tf.name,
            "subject": subject[:120] if subject else f"Template from {tf.name}",
            "content_preview": content[:300],
            "status": "AVAILABLE",
            "added_at": datetime.now().isoformat()
        })

    if new_templates:
        all_templates = existing_lib + new_templates
        library_path.write_text(json.dumps(all_templates, indent=2))

    return len(new_templates)


# ─── CONNECTION 38: Auto-Ops Tool Evals → Content Farm ───────────────────
# Tool evaluations become "tool of the day" social content
def wire_tool_evals_to_content():
    evals_dir = safe_path(AUTOMATIONS / "auto_ops" / "tool_evals")
    if not evals_dir.exists():
        return 0

    eval_files = list(evals_dir.glob("TOOL_*.md"))
    if not eval_files:
        return 0

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)
    existing_posts = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"} if queue_dir.exists() else set()

    created = 0
    for ef in sorted(eval_files, key=lambda x: x.stat().st_mtime, reverse=True)[:10]:
        slug = f"tooleval_{ef.stem}".lower()[:60]
        if slug in existing_posts:
            continue

        try:
            content = ef.read_text(encoding="utf-8")[:1500]
        except Exception:
            continue

        # Extract tool name from content
        tool_name = ef.stem.replace("TOOL_", "")
        first_heading = ""
        for line in content.split("\n"):
            if line.startswith("# "):
                first_heading = line[2:].strip()
                break

        display_name = first_heading if first_heading else tool_name

        tweet = (
            f"evaluated a new tool: {display_name[:60]}\n\n"
            f"i review 5-10 tools per week across scraping, automation, content, and monetization.\n\n"
            f"most tools people hype are mid. the ones that actually save time are the boring ones nobody talks about.\n\n"
            f"full eval in the vault."
        )

        post_path = safe_path(queue_dir / f"{slug}.txt")
        post_path.write_text(tweet, encoding="utf-8")
        existing_posts.add(slug)
        created += 1

        if created >= 5:
            break

    return created


# ─── CONNECTION 39: Freelance Demand → Digital Products ──────────────────
# High-demand freelance services inform productized service/template creation
def wire_freelance_demand_to_products():
    demand = load_csv(LEDGER / "FREELANCE_DEMAND_SCAN.csv", max_rows=500)
    if not demand:
        return 0

    # Find recurring high-budget categories
    category_stats = {}
    for row in demand:
        services = row.get("matched_services", "")
        budget = row.get("budget", "0")
        score = row.get("score", "0")
        typical_high = row.get("typical_price_high", "0")

        try:
            budget_num = int(str(budget).replace("$", "").replace(",", "").strip() or "0")
        except (ValueError, TypeError):
            budget_num = 0
        try:
            typical_high_num = int(str(typical_high).replace("$", "").replace(",", "").strip() or "0")
        except (ValueError, TypeError):
            typical_high_num = 0
        try:
            score_num = int(str(score).strip() or "0")
        except (ValueError, TypeError):
            score_num = 0

        for svc in services.split(","):
            svc = svc.strip()
            if not svc:
                continue
            if svc not in category_stats:
                category_stats[svc] = {"count": 0, "total_budget": 0, "max_price": 0, "avg_score": 0}
            category_stats[svc]["count"] += 1
            category_stats[svc]["total_budget"] += budget_num
            category_stats[svc]["max_price"] = max(category_stats[svc]["max_price"], typical_high_num)

    # Only productize services with 5+ demand signals
    product_ideas = []
    for svc, stats in sorted(category_stats.items(), key=lambda x: x[1]["count"], reverse=True):
        if stats["count"] < 5:
            continue

        avg_budget = stats["total_budget"] // stats["count"] if stats["count"] > 0 else 0
        product_ideas.append({
            "service_type": svc,
            "demand_signals": stats["count"],
            "avg_budget": avg_budget,
            "max_price_seen": stats["max_price"],
            "product_suggestion": f"Productized {svc} template/toolkit",
            "price_point": f"${min(avg_budget, 49)}" if avg_budget > 0 else "$19-39",
            "format": "Template + tutorial + automation script",
            "source": "FREELANCE_DEMAND_SCAN",
            "detected_at": datetime.now().isoformat()
        })

    if not product_ideas:
        return 0

    ideas_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "freelance_product_ideas.json")
    ideas_path.parent.mkdir(parents=True, exist_ok=True)

    existing = []
    if ideas_path.exists():
        try:
            existing = json.loads(ideas_path.read_text())
        except (json.JSONDecodeError, ValueError):
            existing = []

    existing_types = {e.get("service_type", "") for e in existing}
    new_ideas = [i for i in product_ideas if i["service_type"] not in existing_types]

    if new_ideas:
        all_ideas = existing + new_ideas
        ideas_path.write_text(json.dumps(all_ideas, indent=2))

    return len(new_ideas)


# ─── CONNECTION 40: Execution Manifest → Asset Deployer Trigger ──────────
# Asset deployer reads execution manifest on cycle start and marks tasks in-progress
def wire_execution_manifest_to_deployer():
    manifest_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "execution_manifest.json")
    if not manifest_path.exists():
        return 0

    try:
        manifest = json.loads(manifest_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return 0

    if not isinstance(manifest, list):
        return 0

    ready_tasks = [t for t in manifest if t.get("status") == "READY_FOR_EXECUTION"]
    if not ready_tasks:
        return 0

    # Create deployer trigger file that asset_deployer reads on startup
    trigger_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "deployer_trigger.json")
    existing_triggers = []
    if trigger_path.exists():
        try:
            existing_triggers = json.loads(trigger_path.read_text())
        except (json.JSONDecodeError, ValueError):
            existing_triggers = []
    existing_ids = {t.get("task_id", "") for t in existing_triggers}

    new_triggers = []
    for task in ready_tasks:
        tid = task.get("task_id", "")
        if tid and tid not in existing_ids:
            new_triggers.append({
                "task_id": tid,
                "description": task.get("description", ""),
                "priority": task.get("priority", "MEDIUM"),
                "status": "TRIGGERED",
                "triggered_at": datetime.now().isoformat()
            })

    if new_triggers:
        all_triggers = existing_triggers + new_triggers
        trigger_path.write_text(json.dumps(all_triggers, indent=2))

    return len(new_triggers)


# ─── CONNECTION 41: OpenClaw Priority Queue → Preview Build Trigger ──────
# High-score qualified leads feed OpenClaw's discover step as priority targets
def wire_priority_queue_to_openclaw_config():
    priority_path = safe_path(LEADS / "auto_local_biz_openclaw_nationwide_9569" / "priority_targets.json")
    if not priority_path.exists():
        return 0

    try:
        targets = json.loads(priority_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return 0

    if not isinstance(targets, list) or not targets:
        return 0

    # Inject priority cities into OpenClaw's config
    state_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "autonomy_state.json")
    if not state_path.exists():
        return 0

    try:
        state = json.loads(state_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return 0

    openclaw = state.get("ventures", {}).get("auto_local_biz_openclaw_nationwide_9569", {})
    config = openclaw.get("config", {})
    existing_priority = config.get("priority_targets", [])
    existing_websites = {t.get("website", "") for t in existing_priority if isinstance(t, dict)}

    new_priority = []
    for target in targets:
        website = target.get("website", "")
        if website and website not in existing_websites:
            new_priority.append({
                "business_name": target.get("business_name", ""),
                "website": website,
                "city": target.get("city", ""),
                "category": target.get("category", ""),
                "composite_score": target.get("composite_score", 0),
                "source": "cross_pollinator_priority"
            })
            existing_websites.add(website)

    if new_priority:
        config["priority_targets"] = existing_priority + new_priority
        config["priority_updated"] = datetime.now().isoformat()
        openclaw["config"] = config
        state["ventures"]["auto_local_biz_openclaw_nationwide_9569"] = openclaw
        state_path.write_text(json.dumps(state, indent=2))

    return len(new_priority)


# ─── CONNECTION 42: Freelance Product Ideas → Digital Products Config ────
# Wire freelance-derived product ideas into Digital Products venture config
def wire_freelance_ideas_to_products_config():
    ideas_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "freelance_product_ideas.json")
    if not ideas_path.exists():
        return 0

    try:
        ideas = json.loads(ideas_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return 0

    if not isinstance(ideas, list) or not ideas:
        return 0

    state_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "autonomy_state.json")
    if not state_path.exists():
        return 0

    try:
        state = json.loads(state_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return 0

    product_venture = state.get("ventures", {}).get("auto_product_digital_products_9788", {})
    config = product_venture.get("config", {})
    existing_specs = config.get("product_specs", [])
    existing_names = {s.get("suggested_product", "") for s in existing_specs if isinstance(s, dict)}

    new_specs = []
    for idea in ideas:
        name = idea.get("product_suggestion", "")
        if name and name not in existing_names:
            new_specs.append({
                "suggested_product": name,
                "category": idea.get("service_type", "FREELANCE"),
                "alpha_count": idea.get("demand_signals", 0),
                "price_range": idea.get("price_point", "$19-39"),
                "format": idea.get("format", "Template + tutorial"),
                "spec_file": f"freelance_{idea.get('service_type', 'general').lower()}"
            })
            existing_names.add(name)

    if new_specs:
        config["product_specs"] = existing_specs + new_specs
        config["freelance_specs_updated"] = datetime.now().isoformat()
        product_venture["config"] = config
        state["ventures"]["auto_product_digital_products_9788"] = product_venture
        state_path.write_text(json.dumps(state, indent=2))

    return len(new_specs)


# ─── CONNECTION 43: App Factory Spec Queue → App Factory Config ──────────
# Wire queued app specs into App Factory's find_gap step so it picks from queue
def wire_spec_queue_to_app_factory_config():
    queue_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "app_factory_spec_queue.json")
    if not queue_path.exists():
        return 0

    try:
        queue = json.loads(queue_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return 0

    if not isinstance(queue, list) or not queue:
        return 0

    queued_specs = [s for s in queue if s.get("status") == "QUEUED"]
    if not queued_specs:
        return 0

    state_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "autonomy_state.json")
    if not state_path.exists():
        return 0

    try:
        state = json.loads(state_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return 0

    app_venture = state.get("ventures", {}).get("auto_app_app_factory_9788", {})
    config = app_venture.get("config", {})
    existing_queue = config.get("spec_queue", [])
    existing_files = {s.get("source_file", "") for s in existing_queue if isinstance(s, dict)}

    new_queued = []
    for spec in queued_specs[:20]:  # Cap at 20 per cycle
        sf = spec.get("source_file", "")
        if sf and sf not in existing_files:
            new_queued.append({
                "source_file": sf,
                "title": spec.get("title", ""),
                "priority": spec.get("priority", "MEDIUM"),
                "status": "AVAILABLE_FOR_BUILD",
                "queued_at": datetime.now().isoformat()
            })
            existing_files.add(sf)

    if new_queued:
        config["spec_queue"] = existing_queue + new_queued
        config["spec_queue_updated"] = datetime.now().isoformat()
        app_venture["config"] = config
        state["ventures"]["auto_app_app_factory_9788"] = app_venture
        state_path.write_text(json.dumps(state, indent=2))

    return len(new_queued)


# ─── CONNECTION 44: Gap Reports → Content Farm ──────────────────────────
# Gap report findings become data-rich "building in public" content
def wire_gap_reports_to_content():
    import re
    reports_dir = safe_path(REPORTS)
    gap_files = sorted(reports_dir.glob("gap_report_*.md"), reverse=True)
    if not gap_files:
        return 0

    latest = gap_files[0]
    text = latest.read_text(encoding="utf-8")
    date_part = latest.stem.replace("gap_report_", "")

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)
    existing_posts = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"} if queue_dir.exists() else set()

    # Extract gap summaries
    gaps = re.findall(
        r'### GAP (\d+): (.+?) \((\w+)\)\n(.*?)(?=### GAP|\Z)',
        text, re.DOTALL
    )

    created = 0
    for gap_num, title, severity, body in gaps:
        if severity not in ("CRITICAL", "HIGH"):
            continue

        slug = f"gap_insight_{date_part}_{gap_num}"
        if slug in existing_posts:
            continue

        # Extract revenue impact
        revenue_match = re.search(r'\*\*Revenue impact:\*\* (.+)', body)
        revenue = revenue_match.group(1).strip()[:100] if revenue_match else ""

        tweet = (
            f"ran an automated gap analysis on our portfolio.\n\n"
            f"finding: {title.lower()[:80]}\n\n"
        )
        if revenue:
            tweet += f"revenue impact: {revenue.lower()}\n\n"
        tweet += (
            f"the system scans for gaps every 4 hours. "
            f"most founders don't know what's broken until revenue drops. "
            f"we know before it breaks."
        )

        post_path = safe_path(queue_dir / f"{slug}.txt")
        post_path.write_text(tweet, encoding="utf-8")
        created += 1

        if created >= 3:
            break

    return created


# ─── CONNECTION 45: Alpha Scoring → Content Farm ────────────────────────
# Alpha scoring sessions become "how I evaluate opportunities" content
def wire_alpha_scoring_to_content():
    import re
    reports_dir = safe_path(REPORTS)
    scoring_files = sorted(reports_dir.glob("alpha_scoring_*.md"), reverse=True)
    if not scoring_files:
        return 0

    latest = scoring_files[0]
    text = latest.read_text(encoding="utf-8")
    date_part = latest.stem.replace("alpha_scoring_", "")

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)
    existing_posts = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"} if queue_dir.exists() else set()

    slug = f"alpha_scoring_{date_part}"
    if slug in existing_posts:
        return 0

    # Extract key stats from scoring report
    total_match = re.search(r'(\d+)\s*(?:entries|items|alpha)', text)
    approved_match = re.search(r'(\d+)\s*(?:approved|APPROVED)', text)
    rejected_match = re.search(r'(\d+)\s*(?:rejected|REJECTED)', text)

    total = total_match.group(1) if total_match else "?"
    approved = approved_match.group(1) if approved_match else "?"
    rejected = rejected_match.group(1) if rejected_match else "?"

    tweet = (
        f"just scored {total} alpha entries.\n\n"
        f"{approved} approved. {rejected} rejected.\n\n"
        f"every entry gets: bot detection, earnings verification, method extraction, "
        f"ROI scoring, and venture routing.\n\n"
        f"most people bookmark stuff and forget it. "
        f"we have an automated pipeline that turns bookmarks into products."
    )

    post_path = safe_path(queue_dir / f"{slug}.txt")
    post_path.write_text(tweet, encoding="utf-8")
    return 1


# ─── CONNECTION 46: Engagement Bait Alpha → Niche Content ────────────────
# ENGAGEMENT_BAIT alpha entries are tagged "good for engagement" but never
# routed to content farm. This wire converts them into niche account posts.
def wire_engagement_bait_to_content():
    alpha_path = LEDGER / "ALPHA_STAGING.csv"
    if not alpha_path.exists():
        return 0

    all_rows = load_csv(alpha_path, max_rows=500)
    bait = [r for r in all_rows if r.get("status") == "ENGAGEMENT_BAIT"]
    if not bait:
        return 0

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)
    existing_posts = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"} if queue_dir.exists() else set()

    created = 0
    for row in bait[-15:]:  # Last 15 engagement bait entries
        alpha_id = row.get("alpha_id", "")
        tactic = row.get("tactic", "") or row.get("extracted_method", "") or row.get("signal", "")
        source = row.get("source", "")

        slug = f"engbait_{alpha_id}".lower()
        if slug in existing_posts or not tactic:
            continue

        # Format as engagement-first niche post (reply bait style)
        hook = tactic[:140].rstrip(".")
        tweet = f"{hook}\n\nmost people won't do this. that's why most people stay broke."
        post_path = safe_path(queue_dir / f"{slug}.txt")
        post_path.write_text(tweet, encoding="utf-8")
        created += 1

    return created


# ─── CONNECTION 47: Viral Scan History → Content Farm ────────────────────
# Viral content scans identify trending formats. Route to content creation.
def wire_viral_scans_to_content():
    scan_dir = safe_path(AUTOMATIONS / "viral_content" / "scan_history")
    if not scan_dir.exists():
        return 0

    scans = sorted(scan_dir.glob("scan_*.json"), reverse=True)
    if not scans:
        return 0

    queue_dir = safe_path(POSTING_QUEUE)
    queue_dir.mkdir(parents=True, exist_ok=True)
    existing = {f.stem for f in queue_dir.iterdir() if f.suffix == ".txt"} if queue_dir.exists() else set()

    created = 0
    for scan_file in scans[:3]:  # Last 3 scans
        data = load_json(scan_file)
        trends = data.get("trends", data.get("viral_content", []))
        if isinstance(trends, dict):
            trends = list(trends.values())
        if not isinstance(trends, list):
            continue

        date_part = scan_file.stem.replace("scan_", "")
        for i, trend in enumerate(trends[:5]):
            slug = f"viral_{date_part}_{i}"
            if slug in existing:
                continue

            if isinstance(trend, dict):
                topic = trend.get("topic", trend.get("title", trend.get("format", "")))
                engagement = trend.get("engagement", trend.get("views", ""))
            elif isinstance(trend, str):
                topic = trend
                engagement = ""
            else:
                continue

            if not topic:
                continue

            tweet = (
                f"this format is blowing up right now: {str(topic)[:120]}\n\n"
                f"{'engagement: ' + str(engagement) + '. ' if engagement else ''}"
                f"adapt it to your niche before everyone copies it."
            )
            post_path = safe_path(queue_dir / f"{slug}.txt")
            post_path.write_text(tweet, encoding="utf-8")
            created += 1

    return created


# ─── CONNECTION 48: Competitor Pricing → Outreach Angles ─────────────────
# When competitors change pricing, use that as a cold outreach hook.
def wire_competitor_pricing_to_outreach():
    changes = load_csv(LEDGER / "COMPETITOR_CHANGES.csv", max_rows=200)
    if not changes:
        return 0

    pricing_changes = [c for c in changes if "price" in (c.get("change_type", "") + c.get("field", "")).lower()]
    if not pricing_changes:
        return 0

    outreach_dir = safe_path(AUTOMATIONS / "leads" / "pricing_angles")
    outreach_dir.mkdir(parents=True, exist_ok=True)

    existing = {f.stem for f in outreach_dir.iterdir() if f.suffix == ".json"} if outreach_dir.exists() else set()
    created = 0

    for change in pricing_changes[-10:]:
        competitor = change.get("competitor", change.get("app", "unknown"))
        old_price = change.get("old_value", change.get("old_price", "?"))
        new_price = change.get("new_value", change.get("new_price", "?"))
        slug = f"price_{competitor}_{datetime.now().strftime('%Y%m%d')}".lower().replace(" ", "_")[:60]

        if slug in existing:
            continue

        angle = {
            "competitor": competitor,
            "old_price": old_price,
            "new_price": new_price,
            "outreach_angle": f"{competitor} just changed pricing from {old_price} to {new_price}. Their users might be looking for alternatives.",
            "target_audience": f"Users of {competitor} who are price-sensitive",
            "generated_at": datetime.now().isoformat()
        }

        path = safe_path(outreach_dir / f"{slug}.json")
        path.write_text(json.dumps(angle, indent=2))
        created += 1

    return created


# ─── MAIN CYCLE ───────────────────────────────────────────────────────────
def run_cycle():
    print("=" * 60)
    print("CROSS-POLLINATOR CYCLE")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)

    results = {}

    connections = [
        ("Competitive Intel → Content Farm", wire_competitive_intel_to_content),
        ("Reddit Scraper → Cold Outreach", wire_reddit_to_outreach),
        ("Competitive Intel → App Factory", wire_competitive_intel_to_app_factory),
        ("Alpha Intelligence → Content Farm", wire_alpha_to_content),
        ("OpenClaw → Cold Outreach", wire_openclaw_to_outreach),
        ("App Factory → Content Farm", wire_apps_to_content),
        ("Digital Products → Content Farm", wire_products_to_content),
        ("Lead Pain Points → Content Farm", wire_leads_to_content),
        ("Content Farm → Affiliate Funnels", wire_content_to_affiliate),
        ("Swarm Leads → Master Leads", wire_swarm_leads_to_master),
        ("Counter-Content → Posting Queue", wire_counter_content_to_queue),
        ("OpenClaw Previews → Content Farm", wire_openclaw_previews_to_content),
        ("Trend Synthesis → Content Farm", wire_trends_to_content),
        ("Revenue Urgency → Content Farm", wire_revenue_urgency_to_content),
        ("Competitive Intel → Outreach Context", wire_intel_to_outreach_context),
        ("Brain Decisions → Venture Config", wire_brain_decisions_to_ventures),
        ("Gap Report → Human Action Queue", wire_gap_report_to_action_queue),
        ("Monetization Audit → Deployment Tasks", wire_monetization_audit_to_tasks),
        ("Reddit Pain Points → Product Demand", wire_reddit_to_product_demand),
        ("Content Farm → App Traffic URLs", wire_content_to_app_traffic),
        ("Brain Insights → Content Farm", wire_brain_insights_to_content),
        ("Posting Queue → Buffer CSV", wire_posting_queue_to_buffer),
        ("Monetization Tasks → Deployer Queue", wire_monetization_tasks_to_deployer),
        ("Demand Signals → Products Config", wire_demand_signals_to_products),
        ("Trend Signals → Outreach Angles", wire_trends_to_outreach),
        ("Alpha Clusters → Product Specs", wire_alpha_clusters_to_product_specs),
        ("Scored Leads → Case Studies", wire_leads_to_case_studies),
        ("Product Specs → Digital Products", wire_product_specs_to_digital_products),
        ("Deployer Queue → Execution Manifest", wire_deployer_queue_to_manifest),
        ("Compound Content → Posting Queue", wire_compound_content_to_queue),
        ("Qualified Leads → OpenClaw Priority", wire_qualified_leads_to_openclaw),
        ("Trend Synthesis → Venture Angles", wire_trend_synthesis_to_ventures),
        ("Alpha Content → Posting Queue", wire_alpha_content_to_queue),
        ("Freelance Responses → Content Farm", wire_freelance_responses_to_content),
        ("Freelance Demand → App Factory Gaps", wire_freelance_demand_to_app_factory),
        ("Auto-Ops Specs → App Factory Queue", wire_auto_ops_specs_to_app_factory),
        ("Auto-Ops Emails → Outreach Templates", wire_auto_ops_emails_to_outreach),
        ("Tool Evals → Content Farm", wire_tool_evals_to_content),
        ("Freelance Demand → Digital Products", wire_freelance_demand_to_products),
        ("Execution Manifest → Deployer Trigger", wire_execution_manifest_to_deployer),
        ("Priority Queue → OpenClaw Config", wire_priority_queue_to_openclaw_config),
        ("Freelance Ideas → Products Config", wire_freelance_ideas_to_products_config),
        ("Spec Queue → App Factory Config", wire_spec_queue_to_app_factory_config),
        ("Gap Reports → Content Farm", wire_gap_reports_to_content),
        ("Alpha Scoring → Content Farm", wire_alpha_scoring_to_content),
        ("Engagement Bait → Niche Content", wire_engagement_bait_to_content),
        ("Viral Scans → Content Farm", wire_viral_scans_to_content),
        ("Competitor Pricing → Outreach Angles", wire_competitor_pricing_to_outreach),
    ]

    total_wired = 0
    for name, func in connections:
        try:
            count = func()
            results[name] = {"status": "OK", "items_wired": count}
            total_wired += count
            status = f"  {count} items" if count > 0 else "  0 (no new data)"
            print(f"  [{'+' if count > 0 else '-'}] {name}: {status}")
        except Exception as e:
            results[name] = {"status": "ERROR", "error": str(e)}
            print(f"  [!] {name}: ERROR - {e}")

    print(f"\nTotal items wired: {total_wired}")

    # Save cycle results
    cycle_log = {
        "timestamp": datetime.now().isoformat(),
        "total_wired": total_wired,
        "connections": results
    }

    log_path = safe_path(AUTOMATIONS / "agent" / "swarm" / "cross_pollinator_log.jsonl")
    with open(log_path, "a") as f:
        f.write(json.dumps(cycle_log) + "\n")

    return results, total_wired


def show_status():
    log_path = AUTOMATIONS / "agent" / "swarm" / "cross_pollinator_log.jsonl"
    if not log_path.exists():
        print("No cross-pollination cycles run yet.")
        return

    lines = log_path.read_text().strip().split("\n")
    last = json.loads(lines[-1])
    print(f"Last cycle: {last['timestamp']}")
    print(f"Total wired: {last['total_wired']}")
    print(f"Total cycles: {len(lines)}")
    for conn, info in last["connections"].items():
        status = info.get("status", "?")
        items = info.get("items_wired", 0)
        print(f"  {conn}: {status} ({items} items)")


if __name__ == "__main__":
    if "--cycle" in sys.argv:
        results, total = run_cycle()
    elif "--status" in sys.argv:
        show_status()
    else:
        print("Usage:")
        print("  python3 AUTOMATIONS/cross_pollinator.py --cycle    # Run all connections")
        print("  python3 AUTOMATIONS/cross_pollinator.py --status   # Show last run")
