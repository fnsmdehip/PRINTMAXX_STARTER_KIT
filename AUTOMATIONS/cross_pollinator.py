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
        rating = float(row.get("rating", "0") or "0")
        rating_count = int(row.get("rating_count", "0") or "0")
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
