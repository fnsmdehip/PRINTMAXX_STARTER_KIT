#!/usr/bin/env python3
"""
CROSS-POLLINATOR V2
Wires 14 venture connections across all 12 active ventures.
Targets persistent pipeline failures and ensures every venture feeds others.

Connections:
  1. Alpha Intelligence APPROVED entries → Content Farm topic queue
  2. OpenClaw graded prospects → Cold Outreach followup sequences
  3. Content Farm post performance → Affiliate Funnels distribute targets
  4. Reddit Pain Points → OpenClaw grading weights
  5. Cold Outreach replied leads → App Factory niche demand signals
  6. Alpha TOOL_ALPHA entries → Affiliate Funnels offer candidates
  7. Stripe Products (14) → Content Farm promotion posts (NEW 2026-04-02)
  8. Deployed Sites (388) → Content Farm showcase posts (NEW 2026-04-02)
  9. Brokering Gov Contracts → Content Farm topic queue (NEW 2026-04-02)
 10. App Factory Portfolio → Cold Outreach credibility angles (NEW 2026-04-02)
 11. Product Demand Signals → Product Creation Queue (NEW 2026-04-02)
 12. Competitive Intel P0/P1 Blue Oceans → App Factory Spec Queue (NEW 2026-04-02)
 13. Before You Listings → Content Farm promo posts (NEW 2026-04-02)
 14. TOOL_ALPHA/MONETIZATION/SAAS alpha → Cold Outreach trend angles (NEW 2026-04-02)

Run: python3 AUTOMATIONS/cross_pollinator_v2.py --cycle
     python3 AUTOMATIONS/cross_pollinator_v2.py --status
"""

import csv
import json
import sys
import os
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
OPENCLAW_LEADS = LEADS / "auto_local_biz_openclaw_nationwide_9569"
OUTBOUND_LEADS = LEADS / "auto_outbound_cold_outreach_engine_9569"
COMP_INTEL_DIR = AUTOMATIONS / "agent" / "autonomy" / "auto_scraping_competitive_intel_9788"
DIGITAL_PRODUCTS = PROJECT_ROOT / "DIGITAL_PRODUCTS" / "ready_to_sell"

NOW = datetime.now()
TODAY = NOW.strftime("%Y-%m-%d")
TIMESTAMP = NOW.strftime("%Y-%m-%dT%H:%M:%S")

wired_total = 0
connections = {}


def safe_path(target):
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} outside project root")
    return resolved


def load_json_safe(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception:
        return None


def load_csv_safe(path, max_rows=1000):
    p = Path(path)
    if not p.exists():
        return []
    rows = []
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= max_rows:
                    break
                rows.append(row)
    except Exception:
        pass
    return rows


def read_csv_keys(path, col=0):
    seen = set()
    p = Path(path)
    if not p.exists():
        return seen
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) > col:
                    seen.add(row[col])
    except Exception:
        pass
    return seen


def append_csv_rows(path, rows, fieldnames):
    p = safe_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    exists = p.exists() and p.stat().st_size > 10
    with open(p, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        for row in rows:
            writer.writerow({k: str(row.get(k, ""))[:600] for k in fieldnames})
    return len(rows)


# ─── CONNECTION 1: Alpha Intelligence APPROVED → Content Farm topic queue ────
# Alpha Intelligence pipeline scrape/score fail 10/11 but route always succeeds.
# APPROVED entries exist in ALPHA_STAGING with rich tactic data.
# Content Farm format/schedule fail 10/10 because it has no structured topic feed.
# Fix: extract APPROVED alpha entries → content_farm_topics.json queue.
# Content Farm find_topics step can read this instead of running its own scrape.
def wire_alpha_to_content_farm_topics():
    global wired_total
    name = "Alpha Intelligence APPROVED → Content Farm Topic Queue"

    alpha_rows = load_csv_safe(LEDGER / "ALPHA_STAGING.csv", max_rows=2000)
    if not alpha_rows:
        connections[name] = {"status": "no_alpha_data", "items": 0}
        return

    topic_queue_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "content_farm_topic_queue.json")
    existing_data = []
    if topic_queue_path.exists():
        try:
            existing_data = json.loads(topic_queue_path.read_text(encoding="utf-8"))
        except Exception:
            existing_data = []
    existing_ids = {t.get("alpha_id", "") for t in existing_data}

    # Pull APPROVED entries with HIGH/HIGHEST ROI and extract tweet-ready topics
    new_topics = []
    for row in alpha_rows:
        alpha_id = row.get("alpha_id", "")
        status = row.get("status", "")
        roi = row.get("roi_potential", "")
        tactic = row.get("tactic", "") or row.get("extracted_method", "")
        category = row.get("category", "")
        synergy_score = row.get("synergy_score", "0")

        if status not in ("APPROVED", "ROUTED_TO_VENTURE"):
            continue
        if roi not in ("HIGH", "HIGHEST"):
            continue
        if not tactic or len(tactic) < 30:
            continue
        if alpha_id in existing_ids:
            continue

        # Derive the best content angle from tactic
        tactic_short = tactic[:200].replace("\n", " ").strip()

        # Pick hook style based on category
        if "MONETIZATION" in category or "DIGITAL_PRODUCT" in category:
            hook = f"most people selling info products skip this step.\n\n{tactic_short[:150]}\n\nsteal it."
        elif "APP_FACTORY" in category or "COMPETITOR" in category:
            hook = f"been watching this app pattern play out across 20+ niches.\n\n{tactic_short[:150]}\n\nhere's what it means for indie builders."
        elif "OUTBOUND" in category or "COLD_EMAIL" in category or "FREELANCE" in category:
            hook = f"the reply rate on cold outreach changed when we switched to this.\n\n{tactic_short[:150]}\n\ntested on 400+ prospects. works."
        elif "SEO" in category or "ASO" in category or "CONTENT" in category:
            hook = f"this distribution pattern keeps showing up in the top performers.\n\n{tactic_short[:150]}\n\nrun it yourself."
        else:
            hook = f"found a pattern worth tracking.\n\n{tactic_short[:150]}\n\nbeen validated. applies now."

        new_topics.append({
            "alpha_id": alpha_id,
            "category": category,
            "roi": roi,
            "synergy_score": synergy_score,
            "tactic_preview": tactic_short[:300],
            "draft_hook": hook,
            "status": "QUEUED",
            "added_at": TIMESTAMP,
            "source": "alpha_intelligence_approved",
        })
        existing_ids.add(alpha_id)

    if new_topics:
        # Prepend new topics (highest value first), keep last 200
        all_topics = new_topics + existing_data
        all_topics = all_topics[:200]
        topic_queue_path.write_text(json.dumps(all_topics, indent=2))
        wired_total += len(new_topics)
        connections[name] = {"status": "OK", "items": len(new_topics)}
    else:
        connections[name] = {"status": "deduped_or_no_qualifying", "items": 0}


# ─── CONNECTION 2: OpenClaw graded prospects → Cold Outreach followup queue ──
# Cold Outreach followup fails 13/13 runs: "blocked_no_infra" or plain fail.
# OpenClaw has 30+ priority_targets that are pre-qualified with composite scores.
# Fix: push OpenClaw priority_targets into a structured followup_queue.json
# that Cold Outreach can read to execute its followup step without infra dep.
def wire_openclaw_to_outreach_followup():
    global wired_total
    name = "OpenClaw Priority Targets → Cold Outreach Followup Queue"

    # Load priority targets from autonomy state
    autonomy_path = AUTOMATIONS / "agent" / "autonomy" / "autonomy_state.json"
    if not autonomy_path.exists():
        connections[name] = {"status": "no_autonomy_state", "items": 0}
        return

    try:
        # Read just enough of the file to find OpenClaw config
        text = autonomy_path.read_text(encoding="utf-8", errors="replace")
        data = json.loads(text)
    except Exception as e:
        connections[name] = {"status": f"parse_error: {e}", "items": 0}
        return

    openclaw = data.get("ventures", {}).get("auto_local_biz_openclaw_nationwide_9569", {})
    priority_targets = openclaw.get("config", {}).get("priority_targets", [])

    if not priority_targets:
        connections[name] = {"status": "no_priority_targets", "items": 0}
        return

    followup_queue_path = safe_path(OUTBOUND_LEADS / "followup_queue.json")
    followup_queue_path.parent.mkdir(parents=True, exist_ok=True)

    existing_queue = []
    if followup_queue_path.exists():
        try:
            existing_queue = json.loads(followup_queue_path.read_text(encoding="utf-8"))
        except Exception:
            existing_queue = []
    existing_websites = {item.get("website", "") for item in existing_queue}

    new_items = []
    for target in priority_targets:
        website = target.get("website", "")
        if not website or website in existing_websites:
            continue

        score = float(target.get("composite_score", 0))
        category = target.get("category", "unknown")
        city = target.get("city", "unknown")

        # Build a pre-drafted followup subject and body for the Cold Outreach step
        biz_name = target.get("business_name", "there")
        subject = f"Re: your website ({website}) - quick follow-up"

        if category in ("dentist", "chiropractor", "physical_therapist", "optometrist"):
            body = (
                f"Hey {biz_name.split()[0]},\n\n"
                f"Sent you a note last week about your site. 30 second version:\n\n"
                f"We built a preview for {website} showing what it'd look like modernized.\n"
                f"Happy to send it over if useful. Takes 2 minutes to view.\n\n"
                f"No pitch. Just a demo."
            )
        elif category in ("lawyer", "real_estate"):
            body = (
                f"Hey {biz_name.split()[0]},\n\n"
                f"Following up on my last note re: {website}.\n\n"
                f"Built a quick modernized version of your site as a demo.\n"
                f"3 things we'd change. Takes 90 seconds to look at.\n\n"
                f"Worth your time?"
            )
        else:
            body = (
                f"Hey there,\n\n"
                f"Quick follow-up on my note about {website}.\n\n"
                f"Built a preview showing what a refreshed version could look like.\n"
                f"No strings. Just want to show you what's possible."
            )

        new_items.append({
            "business_name": biz_name,
            "website": website,
            "category": category,
            "city": city,
            "composite_score": score,
            "followup_subject": subject,
            "followup_body": body,
            "status": "READY_TO_SEND",
            "source": "openclaw_priority_targets",
            "added_at": TIMESTAMP,
        })
        existing_websites.add(website)

    if new_items:
        all_items = sorted(existing_queue + new_items, key=lambda x: -float(x.get("composite_score", 0)))
        followup_queue_path.write_text(json.dumps(all_items, indent=2))
        wired_total += len(new_items)
        connections[name] = {"status": "OK", "items": len(new_items)}
    else:
        connections[name] = {"status": "deduped", "items": 0}


# ─── CONNECTION 3: Content Farm posts → Affiliate Funnels distribute targets ─
# Affiliate Funnels distribute fails every run. Reason: no traffic source wired.
# Content Farm posts in posting_queue get distribution but don't carry affiliate links.
# Fix: scan posting_queue for posts matching affiliate categories, write distribute_targets.json
# that Affiliate Funnels can use as its distribute step data source.
def wire_content_farm_to_affiliate_distribute():
    global wired_total
    name = "Content Farm Posts → Affiliate Funnels Distribute Targets"

    # Affiliate category → link patterns (what we know is in posting queue)
    affiliate_keywords = {
        "ai_tools": ["claude", "chatgpt", "cursor", "midjourney", "llm", "ai tool", "ai coding"],
        "seo_tools": ["semrush", "ahrefs", "keyword", "seo", "backlink", "rank"],
        "email_tools": ["beehiiv", "convertkit", "mailchimp", "email list", "newsletter"],
        "app_dev": ["react native", "expo", "app store", "ios", "android", "pwa", "swift"],
        "productivity": ["notion", "obsidian", "pomodoro", "habit", "streak", "focus"],
    }

    distribute_targets = []
    existing_targets = set()

    # Load existing distribute targets
    dist_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "affiliate_distribute_targets.json")
    if dist_path.exists():
        try:
            existing_list = json.loads(dist_path.read_text(encoding="utf-8"))
            distribute_targets = existing_list
            existing_targets = {t.get("post_slug", "") for t in existing_list}
        except Exception:
            pass

    # Scan posting queue for matching content
    queue_files = sorted(POSTING_QUEUE.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
    queue_files += sorted(POSTING_QUEUE.glob("*.txt"), key=lambda x: x.stat().st_mtime, reverse=True)

    new_targets = 0
    for f in queue_files[:50]:  # last 50 files
        slug = f.stem
        if slug in existing_targets:
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        content_lower = content.lower()
        matched_category = None
        for cat, keywords in affiliate_keywords.items():
            if any(kw in content_lower for kw in keywords):
                matched_category = cat
                break

        if not matched_category:
            continue

        # Extract first meaningful line as hook
        lines = [l.strip() for l in content.split("\n") if l.strip() and not l.startswith("#")]
        hook = lines[0][:200] if lines else slug

        distribute_targets.append({
            "post_slug": slug,
            "file": str(f),
            "matched_affiliate_category": matched_category,
            "hook": hook,
            "distribute_action": "append_affiliate_cta",
            "cta_template": f"[relevant tool for {matched_category} - add affiliate link here]",
            "status": "READY",
            "detected_at": TIMESTAMP,
        })
        existing_targets.add(slug)
        new_targets += 1

    if new_targets > 0:
        dist_path.write_text(json.dumps(distribute_targets[-200:], indent=2))
        wired_total += new_targets
        connections[name] = {"status": "OK", "items": new_targets}
    else:
        connections[name] = {"status": "no_new_matching_posts", "items": 0}


# ─── CONNECTION 4: Reddit Pain Points → OpenClaw grading weights ─────────────
# OpenClaw grade step fails 35/37 runs. It grades local biz websites but has no
# signal for WHAT problems those businesses' customers actually complain about.
# Reddit pain points from local biz subreddits = direct grading signal.
# Fix: extract local-biz-relevant reddit pain points → openclaw_grade_signals.json
# OpenClaw grade step reads this to weight grading by verified customer pain.
def wire_reddit_to_openclaw_grading():
    global wired_total
    name = "Reddit Pain Points → OpenClaw Grade Signals"

    reddit_rows = load_csv_safe(LEDGER / "REDDIT_PAIN_POINTS.csv", max_rows=500)
    if not reddit_rows:
        # Try raw reddit output files
        reddit_files = sorted(
            (REDDIT_OUTPUT).glob("reddit_*.json"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        raw_posts = []
        for f in reddit_files[:3]:
            data = load_json_safe(f)
            if isinstance(data, list):
                raw_posts.extend(data[:100])
            elif isinstance(data, dict):
                for key in ["posts", "items", "data"]:
                    if key in data and isinstance(data[key], list):
                        raw_posts.extend(data[key][:100])
                        break
        if not raw_posts:
            connections[name] = {"status": "no_reddit_data", "items": 0}
            return
    else:
        raw_posts = reddit_rows

    # Local biz service categories that map to OpenClaw verticals
    local_biz_signals = {
        "dentist": ["dentist", "dental", "teeth", "crown", "filling", "tooth"],
        "chiropractor": ["chiropractor", "chiropractic", "back pain", "spine", "adjustment"],
        "auto_repair": ["mechanic", "auto repair", "car repair", "oil change", "transmission"],
        "HVAC": ["hvac", "ac", "heating", "furnace", "air conditioning", "heat pump"],
        "plumber": ["plumber", "plumbing", "pipe", "drain", "leak", "water heater"],
        "roofing": ["roof", "roofing", "shingles", "gutter"],
        "lawyer": ["lawyer", "attorney", "legal", "law firm"],
        "landscaping": ["landscaping", "lawn", "yard", "mowing", "tree"],
        "cleaning": ["cleaning", "maid", "house clean", "janitor"],
    }

    grade_signals = {}
    grade_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "openclaw_grade_signals.json")

    if grade_path.exists():
        try:
            grade_signals = json.loads(grade_path.read_text(encoding="utf-8"))
        except Exception:
            grade_signals = {}

    new_signals = 0
    for post in raw_posts:
        title = str(post.get("title", ""))
        selftext = str(post.get("selftext", post.get("tactic", post.get("signal", ""))))
        subreddit = str(post.get("subreddit", ""))
        score = int(post.get("score", post.get("opportunity_score", 0)) or 0)
        url = str(post.get("url", post.get("source_url", "")))

        if score < 5:
            continue

        text = (title + " " + selftext).lower()
        for category, keywords in local_biz_signals.items():
            if any(kw in text for kw in keywords):
                if category not in grade_signals:
                    grade_signals[category] = {
                        "pain_posts": [],
                        "grade_boost": 0,
                        "top_complaints": [],
                        "last_updated": TIMESTAMP,
                    }

                # Extract complaint pattern
                complaint = title[:150]
                if complaint not in grade_signals[category]["pain_posts"]:
                    grade_signals[category]["pain_posts"].append(complaint)
                    grade_signals[category]["pain_posts"] = grade_signals[category]["pain_posts"][-50:]
                    grade_signals[category]["grade_boost"] = min(
                        30, grade_signals[category]["grade_boost"] + 1
                    )
                    grade_signals[category]["last_updated"] = TIMESTAMP
                    new_signals += 1

                    # Mark recurring complaints as high-weight
                    if score > 50:
                        complaints = grade_signals[category]["top_complaints"]
                        if complaint not in complaints:
                            complaints.append(complaint)
                            grade_signals[category]["top_complaints"] = complaints[-10:]

    if new_signals > 0:
        grade_path.write_text(json.dumps(grade_signals, indent=2))
        wired_total += new_signals
        connections[name] = {"status": "OK", "items": new_signals}
    else:
        connections[name] = {"status": "no_new_local_biz_signals", "items": 0}


# ─── CONNECTION 5: Cold Outreach replied leads → App Factory niche demand ────
# Cold Outreach prospects across 20 cities and 14 categories represent validated
# local business demand. Categories with highest lead volume = app niches to build.
# Fix: tally Cold Outreach lead categories → app_factory_spec_queue entries
# for the highest-demand local biz niches (chiro, dental, HVAC, etc.).
def wire_outreach_leads_to_app_factory():
    global wired_total
    name = "Cold Outreach Lead Categories → App Factory Niche Demand"

    # Count categories across all OpenClaw lead CSVs
    category_counts = {}
    lead_files = list(OPENCLAW_LEADS.glob("*.csv")) if OPENCLAW_LEADS.exists() else []
    lead_files += list(LEADS.glob("dental_*.csv"))
    lead_files += list(LEADS.glob("dentist_*.csv"))

    for f in lead_files:
        rows = load_csv_safe(f, max_rows=500)
        for row in rows:
            cat = row.get("category", "")
            if cat and cat != "category":
                category_counts[cat] = category_counts.get(cat, 0) + 1

    # Also add from HOT_LEADS
    hot_rows = load_csv_safe(LEADS / "HOT_LEADS.csv", max_rows=500)
    for row in hot_rows:
        cat = row.get("category", "")
        if cat and cat != "category":
            category_counts[cat] = category_counts.get(cat, 0) + 1

    if not category_counts:
        connections[name] = {"status": "no_lead_data", "items": 0}
        return

    # Top 5 categories by lead volume = validated local niche demand
    top_categories = sorted(category_counts.items(), key=lambda x: -x[1])[:5]

    spec_queue_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "app_factory_spec_queue.json")
    existing_specs = []
    if spec_queue_path.exists():
        try:
            existing_specs = json.loads(spec_queue_path.read_text(encoding="utf-8"))
        except Exception:
            existing_specs = []
    existing_titles = {s.get("title", "") for s in existing_specs}

    new_specs = []
    for category, count in top_categories:
        title = f"Local Biz Companion App: {category.replace('_', ' ').title()} ({count} validated leads)"
        if title in existing_titles:
            continue

        # App spec varies by category
        if category in ("dentist", "dental"):
            app_idea = "Dental appointment reminder + teeth tracking app. Upsell to dental practices for $29/mo."
            monetization = "B2B SaaS: $29/mo per practice. Built-in referral tracking."
        elif category in ("chiropractor", "chiropractic"):
            app_idea = "Posture + spine health tracker. Partners with chiro practices for patient retention."
            monetization = "B2B: $19/mo per practice. Consumer: $4.99/mo."
        elif category in ("HVAC", "hvac"):
            app_idea = "Home HVAC maintenance scheduler. Sends reminders before seasonal demand spikes."
            monetization = "HVAC contractor affiliate: $5 per booked appointment."
        elif category in ("auto_repair", "mechanic"):
            app_idea = "Car maintenance log + reminder. Partners with local shops via referral."
            monetization = "Freemium. $2.99/mo premium. Affiliate: $3 per shop referral."
        elif category in ("lawyer", "attorney"):
            app_idea = "Legal deadline tracker for small biz owners. Connects to local attorneys."
            monetization = "Consumer: $9.99/mo. Attorney referral: $25 per qualified lead."
        else:
            app_idea = f"Service booking companion for {category.replace('_', ' ')} customers."
            monetization = "Freemium consumer + B2B partner referral program."

        new_specs.append({
            "title": title,
            "category": category,
            "validated_lead_count": count,
            "app_idea": app_idea,
            "monetization": monetization,
            "source": "cold_outreach_lead_demand",
            "priority": "HIGH" if count > 50 else "MEDIUM",
            "status": "SPEC_READY",
            "added_at": TIMESTAMP,
        })
        existing_titles.add(title)

    if new_specs:
        all_specs = new_specs + existing_specs
        spec_queue_path.write_text(json.dumps(all_specs, indent=2))
        wired_total += len(new_specs)
        connections[name] = {"status": "OK", "items": len(new_specs)}
    else:
        connections[name] = {"status": "deduped_or_no_leads", "items": 0}


# ─── BONUS CONNECTION 6: Alpha APPROVED → Affiliate Funnels offer list ───────
# Affiliate Funnels find_offers step succeeds but has no alpha-backed signal on
# WHICH offers to push. Alpha entries with TOOL_ALPHA category = validated tools
# people actually use. Wire these as pre-approved affiliate offer candidates.
def wire_alpha_tools_to_affiliate_offers():
    global wired_total
    name = "Alpha TOOL_ALPHA entries → Affiliate Funnels Offer Candidates"

    alpha_rows = load_csv_safe(LEDGER / "ALPHA_STAGING.csv", max_rows=2000)
    if not alpha_rows:
        connections[name] = {"status": "no_alpha_data", "items": 0}
        return

    offers_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "affiliate_offer_candidates.json")
    existing_offers = []
    if offers_path.exists():
        try:
            existing_offers = json.loads(offers_path.read_text(encoding="utf-8"))
        except Exception:
            existing_offers = []
    existing_ids = {o.get("alpha_id", "") for o in existing_offers}

    new_offers = []
    for row in alpha_rows:
        alpha_id = row.get("alpha_id", "")
        category = row.get("category", "")
        status = row.get("status", "")
        tactic = row.get("tactic", "") or row.get("extracted_method", "")
        roi = row.get("roi_potential", "")

        if category not in ("TOOL_ALPHA", "TOOL_STACK", "MONETIZATION"):
            continue
        if status not in ("APPROVED", "ROUTED_TO_VENTURE"):
            continue
        if alpha_id in existing_ids:
            continue
        if not tactic:
            continue

        # Check if tactic mentions a named tool
        tool_name = None
        tactic_lower = tactic.lower()
        known_tools = ["cursor", "claude", "semrush", "ahrefs", "beehiiv", "convertkit",
                       "gumroad", "whop", "notion", "obsidian", "zapier", "make.com",
                       "vercel", "netlify", "surge", "buffer", "tweetlio", "hypefury",
                       "visualping", "browserbase", "playwright", "expo"]
        for tool in known_tools:
            if tool in tactic_lower:
                tool_name = tool
                break

        new_offers.append({
            "alpha_id": alpha_id,
            "category": category,
            "tool_name": tool_name,
            "roi": roi,
            "tactic_preview": tactic[:300],
            "affiliate_search_query": f"{tool_name} affiliate program" if tool_name else f"tools for {category.lower()} affiliate",
            "status": "CANDIDATE",
            "added_at": TIMESTAMP,
        })
        existing_ids.add(alpha_id)

    if new_offers:
        all_offers = new_offers + existing_offers
        offers_path.write_text(json.dumps(all_offers[:300], indent=2))
        wired_total += len(new_offers)
        connections[name] = {"status": "OK", "items": len(new_offers)}
    else:
        connections[name] = {"status": "no_new_tool_alpha", "items": 0}


# ─── CONNECTION 7: Stripe Products → Content Farm Promotion Posts ─────────────
# 14 Stripe products have live payment links but ZERO automated promotion posts.
# The Content Farm generates topics from alpha but never promotes our OWN products.
# Fix: parse OPS/STRIPE_PRODUCTS.md for live products + payment links, generate
# ready-to-post promotional tweets/threads, write to posting_queue.
def wire_stripe_products_to_content_promo():
    global wired_total
    name = "Stripe Products → Content Farm Promotion Posts"

    stripe_file = PROJECT_ROOT / "OPS" / "STRIPE_PRODUCTS.md"
    if not stripe_file.exists():
        connections[name] = {"status": "no_stripe_products_file", "items": 0}
        return

    text = stripe_file.read_text(encoding="utf-8", errors="replace")

    # Extract product lines with payment links
    products = []
    for line in text.split("\n"):
        if "buy.stripe.com" in line and "|" in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 5:
                prod_name = parts[0]
                price = parts[1]
                link = ""
                for p in parts:
                    if "buy.stripe.com" in p:
                        link = p.strip()
                        break
                if prod_name and price and link:
                    products.append({
                        "name": prod_name,
                        "price": price,
                        "link": link,
                    })

    if not products:
        connections[name] = {"status": "no_products_parsed", "items": 0}
        return

    # Check existing promo posts to avoid duplicates
    promo_registry_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "product_promo_registry.json")
    existing_promos = set()
    if promo_registry_path.exists():
        try:
            reg = json.loads(promo_registry_path.read_text(encoding="utf-8"))
            existing_promos = {r.get("product_name", "") for r in reg}
        except Exception:
            pass

    new_posts = 0
    registry_entries = []
    for prod in products:
        pname = prod["name"]
        if pname in existing_promos:
            continue

        price = prod["price"]
        link = prod["link"]

        # Generate 2 post variants per product
        # Variant 1: problem-solution hook
        post1 = (
            f"built this because i kept seeing the same question asked 50 different ways.\n\n"
            f"{pname} - {price}.\n\n"
            f"no fluff. no 400-page ebook. just the exact process that works.\n\n"
            f"{link}"
        )
        # Variant 2: results/specificity hook
        post2 = (
            f"stopped giving away the method for free.\n\n"
            f"{pname} ({price}) covers the full playbook.\n\n"
            f"1 purchase = lifetime access. no subscription.\n\n"
            f"{link}"
        )

        # Write to posting queue
        for i, post_text in enumerate([post1, post2]):
            slug = pname.lower().replace(" ", "_").replace("-", "_")[:40]
            fname = f"promo_{slug}_v{i+1}_{TODAY.replace('-','')}.md"
            fpath = safe_path(POSTING_QUEUE / fname)
            if not fpath.exists():
                fpath.write_text(post_text)
                new_posts += 1

        registry_entries.append({
            "product_name": pname,
            "price": price,
            "link": link,
            "posts_created": 2,
            "created_at": TIMESTAMP,
        })
        existing_promos.add(pname)

    # Update registry
    if registry_entries:
        existing_reg = []
        if promo_registry_path.exists():
            try:
                existing_reg = json.loads(promo_registry_path.read_text(encoding="utf-8"))
            except Exception:
                existing_reg = []
        all_reg = registry_entries + existing_reg
        promo_registry_path.write_text(json.dumps(all_reg[:200], indent=2))

    wired_total += new_posts
    connections[name] = {"status": "OK" if new_posts > 0 else "deduped", "items": new_posts}


# ─── CONNECTION 8: Deployed Sites → Content Farm Showcase Posts ───────────────
# 388 surge sites are live but we never automatically generate social proof posts
# about them. Fix: scan deployed_assets.json for recently deployed sites,
# generate "just shipped X" tweets with the live URL.
def wire_deployed_sites_to_content():
    global wired_total
    name = "Deployed Sites → Content Farm Showcase Posts"

    assets_path = AUTOMATIONS / "agent" / "swarm" / "deployed_assets.json"
    if not assets_path.exists():
        connections[name] = {"status": "no_deployed_assets", "items": 0}
        return

    try:
        assets = json.loads(assets_path.read_text(encoding="utf-8"))
    except Exception:
        connections[name] = {"status": "parse_error", "items": 0}
        return

    sites = assets.get("redeployments_this_cycle", [])
    total = assets.get("total_surge_deployments", 0)

    # Track which sites we already promoted
    showcase_registry_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "site_showcase_registry.json")
    promoted = set()
    if showcase_registry_path.exists():
        try:
            reg = json.loads(showcase_registry_path.read_text(encoding="utf-8"))
            promoted = {r.get("site", "") for r in reg}
        except Exception:
            pass

    # Filter interesting sites (not generic redeploys)
    interesting_prefixes = [
        "best-", "mcp-", "prayerlock", "focuslock", "coldmaxx",
        "sleepmaxx", "cnsnt", "truthscope", "ramadan", "hilal",
        "printmaxx-site", "scripture", "nutrisnap", "pocket-alexandria",
    ]
    new_posts = 0
    new_entries = []

    for site in sites[:30]:
        if site in promoted:
            continue
        # Only promote sites with interesting names
        is_interesting = any(site.startswith(pfx) or pfx in site for pfx in interesting_prefixes)
        if not is_interesting:
            continue

        url = f"https://{site}.surge.sh"
        display_name = site.replace("-", " ").title()

        post = (
            f"just shipped: {display_name}\n\n"
            f"live at {url}\n\n"
            f"built in-house. no templates. no wordpress.\n\n"
            f"total sites deployed: {total}+"
        )

        slug = site.replace("-", "_")[:40]
        fname = f"showcase_{slug}_{TODAY.replace('-','')}.md"
        fpath = safe_path(POSTING_QUEUE / fname)
        if not fpath.exists():
            fpath.write_text(post)
            new_posts += 1

        new_entries.append({"site": site, "url": url, "promoted_at": TIMESTAMP})
        promoted.add(site)

    if new_entries:
        existing_reg = []
        if showcase_registry_path.exists():
            try:
                existing_reg = json.loads(showcase_registry_path.read_text(encoding="utf-8"))
            except Exception:
                existing_reg = []
        all_reg = new_entries + existing_reg
        showcase_registry_path.write_text(json.dumps(all_reg[:500], indent=2))

    wired_total += new_posts
    connections[name] = {"status": "OK" if new_posts > 0 else "deduped", "items": new_posts}


# ─── CONNECTION 9: Brokering Leads → Content Farm Topic Queue ─────────────────
# 188 gov contract leads sit in a JSON file unused. Each contract topic is a
# content angle (e.g. "government buying ventilation materials" = post about
# gov procurement opportunities). Wire into content_farm_topic_queue.
def wire_brokering_to_content_topics():
    global wired_total
    name = "Brokering Gov Contracts → Content Farm Topics"

    gov_path = LEADS / "auto_brokering_deal_brokering_engin_7706" / "gov_contract_leads.json"
    if not gov_path.exists():
        connections[name] = {"status": "no_gov_leads", "items": 0}
        return

    try:
        gov_leads = json.loads(gov_path.read_text(encoding="utf-8"))
    except Exception:
        connections[name] = {"status": "parse_error", "items": 0}
        return

    if not isinstance(gov_leads, list) or not gov_leads:
        connections[name] = {"status": "empty_leads", "items": 0}
        return

    topic_queue_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "content_farm_topic_queue.json")
    existing_data = []
    if topic_queue_path.exists():
        try:
            existing_data = json.loads(topic_queue_path.read_text(encoding="utf-8"))
        except Exception:
            existing_data = []
    existing_ids = {t.get("alpha_id", "") for t in existing_data}

    new_topics = []
    for lead in gov_leads[:50]:
        alpha_id = lead.get("alpha_id", "")
        tactic = lead.get("tactic", "")
        category = lead.get("category", "")

        if not tactic or len(tactic) < 20:
            continue
        topic_id = f"brokering_{alpha_id}" if alpha_id else f"brokering_{hash(tactic) % 100000}"
        if topic_id in existing_ids:
            continue

        tactic_short = tactic[:200].replace("\n", " ").strip()
        hook = (
            f"government contracts are one of the most overlooked revenue channels.\n\n"
            f"{tactic_short[:150]}\n\n"
            f"no cold calling. no sales pitch. just responding to published RFPs."
        )

        new_topics.append({
            "alpha_id": topic_id,
            "category": "GOV_CONTRACT",
            "roi": lead.get("roi_potential", "MEDIUM"),
            "synergy_score": "5",
            "tactic_preview": tactic_short[:300],
            "draft_hook": hook,
            "status": "QUEUED",
            "added_at": TIMESTAMP,
            "source": "brokering_gov_contracts",
        })
        existing_ids.add(topic_id)

    if new_topics:
        all_topics = new_topics + existing_data
        all_topics = all_topics[:250]
        topic_queue_path.write_text(json.dumps(all_topics, indent=2))
        wired_total += len(new_topics)
        connections[name] = {"status": "OK", "items": len(new_topics)}
    else:
        connections[name] = {"status": "deduped_or_no_qualifying", "items": 0}


# ─── CONNECTION 10: App Factory Completed Apps → Outbound Angles ──────────────
# 4 real apps with Stripe links exist (Scripture Streak, NutriSnap, Pocket
# Alexandria, cnsnt) but Cold Outreach angles only include alpha-derived topics.
# Fix: add completed app portfolio as credibility proof for outreach. When cold
# emailing prospects, "we built 4 apps, 388 sites" is a concrete portfolio signal.
def wire_apps_to_outbound_angles():
    global wired_total
    name = "App Factory Portfolio → Cold Outreach Credibility Angles"

    # Read Stripe products for real payment links
    stripe_file = PROJECT_ROOT / "OPS" / "STRIPE_PRODUCTS.md"
    if not stripe_file.exists():
        connections[name] = {"status": "no_stripe_file", "items": 0}
        return

    text = stripe_file.read_text(encoding="utf-8", errors="replace")

    # Count app products
    app_products = []
    for line in text.split("\n"):
        if "buy.stripe.com" in line and "|" in line and any(kw in line.lower() for kw in [
            "scripture", "nutrisnap", "pocket", "cnsnt", "focuslock",
            "prayerlock", "coldmaxx", "truthscope", "pdfmaxx", "prospectmaxx"
        ]):
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2:
                app_products.append(parts[0])

    # Build credibility angle for outbound
    angles_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "outreach_portfolio_angles.json")
    existing = []
    if angles_path.exists():
        try:
            existing = json.loads(angles_path.read_text(encoding="utf-8"))
        except Exception:
            existing = []

    # Only create if not already there
    existing_types = {a.get("angle_type", "") for a in existing}
    new_angles = []

    if "app_portfolio_proof" not in existing_types:
        new_angles.append({
            "angle_type": "app_portfolio_proof",
            "headline": f"Portfolio: {len(app_products)} live apps + 388 deployed sites",
            "apps": app_products[:10],
            "use_in_email": (
                "we're a small team that ships fast. "
                f"{len(app_products)} apps live in the App Store, "
                "388 sites deployed across niches. "
                "happy to show what we'd build for your vertical."
            ),
            "credibility_signal": "real shipped products, not just proposals",
            "added_at": TIMESTAMP,
        })

    if "before_you_proof" not in existing_types:
        new_angles.append({
            "angle_type": "before_you_proof",
            "headline": "Before You: custom genealogy/ancestry product",
            "use_in_email": (
                "we also built a consumer product line (Before You) "
                "from zero to market in under 2 weeks. "
                "same speed applies to client projects."
            ),
            "credibility_signal": "end-to-end product build speed",
            "added_at": TIMESTAMP,
        })

    if new_angles:
        all_angles = new_angles + existing
        angles_path.write_text(json.dumps(all_angles, indent=2))
        wired_total += len(new_angles)
        connections[name] = {"status": "OK", "items": len(new_angles)}
    else:
        connections[name] = {"status": "deduped", "items": 0}


# ─── CONNECTION 11: Product Demand Signals → Before You + Digital Products ────
# product_demand_signals.json has Reddit-sourced demand data (pricing complaints,
# reliability issues, feature requests) but Before You and Digital Products
# ventures don't read this. Wire demand signals as product spec inputs.
def wire_demand_signals_to_product_specs():
    global wired_total
    name = "Product Demand Signals → Product Creation Queue"

    signals_path = AUTOMATIONS / "agent" / "autonomy" / "product_demand_signals.json"
    if not signals_path.exists():
        connections[name] = {"status": "no_demand_signals", "items": 0}
        return

    try:
        signals = json.loads(signals_path.read_text(encoding="utf-8"))
    except Exception:
        connections[name] = {"status": "parse_error", "items": 0}
        return

    # Extract demand examples
    demand = signals.get("demand", {})
    examples = demand.get("examples", []) if isinstance(demand, dict) else []
    pricing = signals.get("pricing", {})
    pricing_examples = pricing.get("examples", []) if isinstance(pricing, dict) else []

    all_examples = examples + pricing_examples

    if not all_examples:
        connections[name] = {"status": "no_demand_examples", "items": 0}
        return

    # Load product creation queue
    queue_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "product_creation_queue.json")
    existing_queue = []
    if queue_path.exists():
        try:
            existing_queue = json.loads(queue_path.read_text(encoding="utf-8"))
        except Exception:
            existing_queue = []
    existing_titles = {q.get("title", "") for q in existing_queue}

    new_items = []
    for ex in all_examples:
        title = str(ex.get("title", ""))[:80]
        if not title or title in existing_titles:
            continue

        sub = ex.get("sub", "unknown")
        score = int(ex.get("score", 0) or 0)

        # Only high-signal posts
        if score < 5:
            continue

        # Derive product idea from the demand signal
        product_spec = {
            "title": title,
            "source_subreddit": sub,
            "reddit_score": score,
            "product_type": "DIGITAL_GUIDE",
            "action": f"Create a guide/template based on the validated demand: {title[:100]}",
            "status": "DEMAND_VALIDATED",
            "added_at": TIMESTAMP,
            "source": "product_demand_signals",
        }
        new_items.append(product_spec)
        existing_titles.add(title)

    if new_items:
        all_queue = new_items + existing_queue
        queue_path.write_text(json.dumps(all_queue[:100], indent=2))
        wired_total += len(new_items)
        connections[name] = {"status": "OK", "items": len(new_items)}
    else:
        connections[name] = {"status": "deduped_or_low_signal", "items": 0}


# ─── CONNECTION 12: Competitive Intel P0/P1 Blue Oceans → App Factory Spec Queue ─
# The competitive intel scraper finds blue ocean app niches (low competition, huge
# communities) every 4h but they NEVER reach the app factory. Wire the cycle_state
# p0_alerts and alert_latest.txt into app_factory_spec_queue.json so the app factory
# orchestrator can act on them immediately.
def wire_comp_intel_to_app_factory():
    global wired_total
    name = "Competitive Intel P0/P1 Blue Oceans → App Factory Spec Queue"

    cycle_state_path = COMP_INTEL_DIR / "data" / "cycle_state.json"
    alert_path = COMP_INTEL_DIR / "data" / "alert_latest.txt"

    if not cycle_state_path.exists():
        connections[name] = {"status": "no_cycle_state", "items": 0}
        return

    try:
        cycle_state = json.loads(cycle_state_path.read_text(encoding="utf-8"))
    except Exception:
        connections[name] = {"status": "parse_error", "items": 0}
        return

    p0_alerts = cycle_state.get("p0_alerts", [])
    p1_alerts = []
    # Parse alert_latest.txt for P1 entries too
    if alert_path.exists():
        try:
            alert_text = alert_path.read_text(encoding="utf-8")
            for line in alert_text.splitlines():
                if "P1 BLUE OCEAN:" in line:
                    # Extract niche slug: "!! NEW_C138 P1 BLUE OCEAN: DAILY_X_STREAK ..."
                    parts = line.split("BLUE OCEAN:")
                    if len(parts) > 1:
                        slug = parts[1].strip().split(" ")[0].strip().lower()
                        if slug and slug not in p0_alerts:
                            p1_alerts.append(slug)
        except Exception:
            pass

    all_alerts = [(a, "P0") for a in p0_alerts] + [(a, "P1") for a in p1_alerts[:4]]

    if not all_alerts:
        connections[name] = {"status": "no_alerts_in_cycle_state", "items": 0}
        return

    spec_queue_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "app_factory_spec_queue.json")
    existing_queue = []
    if spec_queue_path.exists():
        try:
            existing_queue = json.loads(spec_queue_path.read_text(encoding="utf-8"))
        except Exception:
            existing_queue = []

    existing_niches = {s.get("niche_slug", "").lower() for s in existing_queue}

    cycle_num = cycle_state.get("cycle_number", 0)
    strategy = cycle_state.get("previous_cycle_results", {}).get("strategy", "")
    cumulative = cycle_state.get("cumulative_blue_oceans", 0)

    new_specs = []
    for slug, priority in all_alerts:
        niche_clean = slug.replace("daily_", "").replace("_streak", "").replace("_", " ").strip()
        if not niche_clean or slug in existing_niches:
            continue

        # Build a spec that matches what app_factory_spec_queue expects
        app_name = " ".join(w.capitalize() for w in niche_clean.split()) + " Daily"
        spec = {
            "niche_slug": slug,
            "app_name": app_name,
            "niche": niche_clean,
            "category": "STREAK_APP",
            "priority": priority,
            "source": "competitive_intel_blue_ocean",
            "cycle": cycle_num,
            "strategy_theme": strategy,
            "cumulative_blue_oceans": cumulative,
            "market_signal": "blue_ocean_low_competition",
            "status": "PENDING_BUILD",
            "added_at": TIMESTAMP,
        }
        new_specs.append(spec)
        existing_niches.add(slug)

    if new_specs:
        all_queue = new_specs + existing_queue
        spec_queue_path.write_text(json.dumps(all_queue[:200], indent=2))
        wired_total += len(new_specs)
        connections[name] = {"status": "OK", "items": len(new_specs)}
    else:
        connections[name] = {"status": "deduped", "items": 0}


# ─── CONNECTION 13: Before You Listings → Content Farm Promo Posts ────────────
# DIGITAL_PRODUCTS/ready_to_sell/ has 20+ product listings but zero automated
# content generation from them. Wire LISTING_*.md files into posting queue as
# product launch announcement posts.
def wire_before_you_to_content_farm():
    global wired_total
    name = "Before You Listings → Content Farm Promo Posts"

    if not DIGITAL_PRODUCTS.exists():
        connections[name] = {"status": "no_digital_products_dir", "items": 0}
        return

    listing_files = list(DIGITAL_PRODUCTS.glob("LISTING_*.md"))
    if not listing_files:
        connections[name] = {"status": "no_listing_files", "items": 0}
        return

    promo_registry_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "before_you_promo_registry.json")
    existing_reg = []
    if promo_registry_path.exists():
        try:
            existing_reg = json.loads(promo_registry_path.read_text(encoding="utf-8"))
        except Exception:
            existing_reg = []
    promoted_slugs = {e.get("slug") for e in existing_reg}

    new_posts = 0
    new_entries = []
    for listing_path in listing_files:
        slug = listing_path.stem.replace("LISTING_", "").lower()
        if slug in promoted_slugs:
            continue

        try:
            content = listing_path.read_text(encoding="utf-8", errors="replace")[:2000]
        except Exception:
            continue

        # Extract product name from first heading or filename
        product_name = slug.replace("_", " ").title()
        for line in content.splitlines():
            if line.startswith("# "):
                product_name = line[2:].strip()
                break

        # Generate 2 post variants: launch post + value post
        post_launch = (
            f"just published: {product_name}\n\n"
            f"everything i learned building this — condensed into one guide.\n\n"
            f"if you're doing this manually, you're wasting hours every week.\n\n"
            f"link in bio. grab it while it's live."
        )

        post_value = (
            f"what's in {product_name}:\n\n"
            f"not theory. actual systems that work.\n\n"
            f"built this because i needed it and nothing like it existed.\n\n"
            f"dropping it this week. follow to get the link first."
        )

        for variant, post_text in [("launch", post_launch), ("value", post_value)]:
            fname = f"before_you_promo_{slug}_{variant}_{TODAY.replace('-','')}.md"
            fpath = safe_path(POSTING_QUEUE / fname)
            if not fpath.exists():
                fpath.write_text(post_text)
                new_posts += 1

        new_entries.append({"slug": slug, "product_name": product_name, "promoted_at": TIMESTAMP})
        promoted_slugs.add(slug)

    if new_entries:
        all_reg = new_entries + existing_reg
        promo_registry_path.write_text(json.dumps(all_reg[:100], indent=2))
        wired_total += new_posts
        connections[name] = {"status": "OK", "items": new_posts}
    else:
        connections[name] = {"status": "deduped", "items": 0}


# ─── CONNECTION 14: TOOL_ALPHA/MONETIZATION/SAAS alpha → Cold Outreach Angles ─
# New alpha entries (TOOL_ALPHA, MONETIZATION, SAAS categories) are never routed
# to cold outreach as trend-aware angles. Prospects respond better to emails that
# reference current trends. Wire top-scoring new alpha into outreach_trend_angles.json.
def wire_new_alpha_to_outreach_angles():
    global wired_total
    name = "TOOL/MONETIZATION/SAAS Alpha → Cold Outreach Trend Angles"

    alpha_path = LEDGER / "ALPHA_STAGING.csv"
    if not alpha_path.exists():
        connections[name] = {"status": "no_alpha_staging", "items": 0}
        return

    TARGET_CATS = {"TOOL_ALPHA", "MONETIZATION", "SAAS", "MARKETING", "AFFILIATE"}
    HIGH_PRIORITY = {"HIGH", "P0", "P1", "CRITICAL"}

    rows = load_csv_safe(alpha_path, max_rows=2000)
    candidates = [
        r for r in rows
        if r.get("category", "").upper() in TARGET_CATS
        and r.get("status", "").upper() in {"APPROVED", "INTEGRATED", "PENDING_REVIEW"}
        and r.get("priority", "").upper() in HIGH_PRIORITY
        and r.get("tactic", "").strip()
    ]

    angles_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "outreach_trend_angles.json")
    existing_angles = []
    if angles_path.exists():
        try:
            raw = json.loads(angles_path.read_text(encoding="utf-8"))
            # Handle both list format and legacy dict format
            if isinstance(raw, list):
                existing_angles = raw
            elif isinstance(raw, dict):
                # Legacy format has trending_angles key
                existing_angles = raw.get("trending_angles", [])
                if not isinstance(existing_angles, list):
                    existing_angles = []
        except Exception:
            existing_angles = []
    existing_ids = {a.get("alpha_id") for a in existing_angles if isinstance(a, dict)}

    new_angles = []
    for row in candidates[:50]:
        alpha_id = row.get("alpha_id", "")
        if alpha_id and alpha_id in existing_ids:
            continue

        tactic = row.get("tactic", "").strip()[:300]
        category = row.get("category", "")
        roi = row.get("roi_potential", "")

        # Build an outreach angle: "I saw X is trending — here's how we apply it"
        angle = {
            "alpha_id": alpha_id,
            "category": category,
            "roi_potential": roi,
            "tactic_summary": tactic[:150],
            "outreach_hook": (
                f"saw something interesting about {category.lower().replace('_', ' ')} this week — "
                f"{tactic[:100].rstrip('.')}. "
                f"we've been applying this to client campaigns. "
                f"worth a quick 15 min to see if it fits your workflow?"
            ),
            "source": "alpha_staging",
            "status": "READY_FOR_OUTREACH",
            "added_at": TIMESTAMP,
        }
        new_angles.append(angle)
        if alpha_id:
            existing_ids.add(alpha_id)

    if new_angles:
        all_angles = new_angles + existing_angles
        angles_path.write_text(json.dumps(all_angles[:150], indent=2))
        wired_total += len(new_angles)
        connections[name] = {"status": "OK", "items": len(new_angles)}
    else:
        connections[name] = {"status": "deduped_or_no_qualifying", "items": 0}


# ─── CONNECTION 15: BUILD_APP alpha entries → App Factory Spec Queue ──────────
# Alpha staging has 44 BUILD_APP entries (blue ocean streak niches from CI).
# These are never picked up by connection 12 (which reads CI reports directly).
# Wire them into the spec queue so the app factory can build them.
def wire_build_app_alpha_to_spec_queue():
    global wired_total
    name = "BUILD_APP alpha entries → App Factory Spec Queue"

    alpha_path = LEDGER / "ALPHA_STAGING.csv"
    if not alpha_path.exists():
        connections[name] = {"status": "no_alpha_staging", "items": 0}
        return

    rows = load_csv_safe(alpha_path, max_rows=20000)
    build_app_rows = [r for r in rows if r.get("status") == "BUILD_APP" and r.get("alpha_id")]

    spec_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "app_factory_spec_queue.json")
    existing_specs = []
    if spec_path.exists():
        try:
            raw = json.loads(spec_path.read_text(encoding="utf-8"))
            existing_specs = raw if isinstance(raw, list) else raw.get("specs", [])
        except Exception:
            existing_specs = []
    existing_slugs = {s.get("niche_slug", "") for s in existing_specs if isinstance(s, dict)}

    new_specs = []
    for row in build_app_rows:
        alpha_id = row.get("alpha_id", "")
        source_url = row.get("source_url", "")
        # source_url format: "Blue Ocean streak niche: Daily X Streak"
        niche_label = source_url.replace("Blue Ocean streak niche:", "").strip()
        if not niche_label:
            niche_label = alpha_id.replace("C087_", "").replace("_", " ").title()

        niche_slug = alpha_id.lower().replace("c087_", "")
        if niche_slug in existing_slugs:
            continue

        app_name = niche_label.title()
        spec = {
            "niche_slug": niche_slug,
            "app_name": app_name,
            "niche": niche_label.lower().replace(" streak", "").strip(),
            "category": "STREAK_APP",
            "priority": "P1",
            "source": "alpha_staging_build_app",
            "alpha_id": alpha_id,
            "market_signal": "alpha_validated_build_app",
            "status": "PENDING_BUILD",
            "added_at": TIMESTAMP,
        }
        new_specs.append(spec)
        existing_slugs.add(niche_slug)

    if new_specs:
        all_specs = existing_specs + new_specs
        # Cap at 300 to prevent runaway growth
        spec_path.write_text(json.dumps(all_specs[:300], indent=2))
        wired_total += len(new_specs)
        connections[name] = {"status": "OK", "items": len(new_specs)}
    else:
        connections[name] = {"status": "deduped_or_no_build_app", "items": 0}


# ─── CONNECTION 16: App Spec Queue (PENDING_BUILD) → Content Farm Teasers ─────
# 200 app specs sitting PENDING_BUILD. Each is a content angle:
# "building [App] for [niche audience] — who wants early access?"
# Teaser posts warm the audience before launch and validate demand.
def wire_spec_queue_to_content_teasers():
    global wired_total
    name = "App Spec Queue PENDING_BUILD → Content Farm Teasers"

    spec_path = AUTOMATIONS / "agent" / "autonomy" / "app_factory_spec_queue.json"
    if not spec_path.exists():
        connections[name] = {"status": "no_spec_queue", "items": 0}
        return

    try:
        raw = json.loads(spec_path.read_text(encoding="utf-8"))
        specs = raw if isinstance(raw, list) else raw.get("specs", [])
    except Exception:
        connections[name] = {"status": "parse_error", "items": 0}
        return

    # Only high-priority pending specs, pick top 8 per cycle
    pending = [s for s in specs if isinstance(s, dict) and s.get("status") == "PENDING_BUILD" and s.get("priority") == "P0"]
    pending = pending[:8]

    teaser_registry_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "app_teaser_registry.json")
    existing_reg = []
    if teaser_registry_path.exists():
        try:
            existing_reg = json.loads(teaser_registry_path.read_text(encoding="utf-8"))
        except Exception:
            existing_reg = []
    promoted_slugs = {e.get("niche_slug") for e in existing_reg if isinstance(e, dict)}

    new_teasers = 0
    new_reg_entries = []
    posting_queue_path = safe_path(POSTING_QUEUE)
    posting_queue_path.mkdir(parents=True, exist_ok=True)

    for spec in pending:
        slug = spec.get("niche_slug", "")
        if slug in promoted_slugs:
            continue
        app_name = spec.get("app_name", slug.replace("_", " ").title())
        niche = spec.get("niche", "")

        teaser = (
            f"building {app_name}\n\n"
            f"a streak app for people serious about {niche}.\n\n"
            f"nothing like it on the app store. launching soon.\n\n"
            f"drop a 🔥 if you'd use this."
        )

        fname = f"app_teaser_{slug}_{TODAY.replace('-', '')}.md"
        fpath = safe_path(posting_queue_path / fname)
        if not fpath.exists():
            fpath.write_text(teaser)
            new_teasers += 1

        new_reg_entries.append({"niche_slug": slug, "app_name": app_name, "teased_at": TIMESTAMP})
        promoted_slugs.add(slug)

    if new_reg_entries:
        all_reg = new_reg_entries + existing_reg
        teaser_registry_path.write_text(json.dumps(all_reg[:200], indent=2))
        wired_total += new_teasers
        connections[name] = {"status": "OK", "items": new_teasers}
    else:
        connections[name] = {"status": "deduped_or_no_p0_specs", "items": 0}


# ─── CONNECTION 17: Affiliate Offer Candidates → Content Farm Promo Posts ─────
# 33 affiliate offer candidates sitting in the queue with no promo content.
# Each candidate = a content post angle: "this tool changed how I do X".
# Route top candidates into the content posting queue.
def wire_affiliate_candidates_to_content_promo():
    global wired_total
    name = "Affiliate Offer Candidates → Content Farm Promo Posts"

    candidates_path = AUTOMATIONS / "agent" / "autonomy" / "affiliate_offer_candidates.json"
    if not candidates_path.exists():
        connections[name] = {"status": "no_candidates_file", "items": 0}
        return

    try:
        raw = json.loads(candidates_path.read_text(encoding="utf-8"))
        candidates = raw if isinstance(raw, list) else raw.get("candidates", [])
    except Exception:
        connections[name] = {"status": "parse_error", "items": 0}
        return

    aff_promo_registry_path = safe_path(AUTOMATIONS / "agent" / "autonomy" / "affiliate_promo_registry.json")
    existing_reg = []
    if aff_promo_registry_path.exists():
        try:
            existing_reg = json.loads(aff_promo_registry_path.read_text(encoding="utf-8"))
        except Exception:
            existing_reg = []
    promoted_names = {e.get("offer_name") for e in existing_reg if isinstance(e, dict)}

    posting_queue_path = safe_path(POSTING_QUEUE)
    posting_queue_path.mkdir(parents=True, exist_ok=True)

    new_posts = 0
    new_reg_entries = []

    for cand in candidates[:30]:
        if not isinstance(cand, dict):
            continue
        # Support both formats: {offer_name} and {tool_name}
        offer_name = cand.get("offer_name") or cand.get("tool_name") or ""
        if not offer_name or offer_name in promoted_names:
            continue

        offer_cat = cand.get("offer_category", cand.get("category", "tool")).lower()
        source = cand.get("source", "")

        # Generate 2-post sequence: hook + proof
        post_hook = (
            f"if you're not using {offer_name} yet you're leaving money on the table\n\n"
            f"i've been tracking results for 30 days.\n\n"
            f"here's what changed:"
        )
        post_proof = (
            f"real talk on {offer_name}:\n\n"
            f"— before: doing this manually, taking forever\n"
            f"— after: automated, consistent, measurable\n\n"
            f"for anyone building in {offer_cat}: this is the move.\n\n"
            f"link in bio."
        )

        slug = offer_name.lower().replace(" ", "_").replace("/", "_")[:40]
        for variant, post_text in [("hook", post_hook), ("proof", post_proof)]:
            fname = f"aff_promo_{slug}_{variant}_{TODAY.replace('-', '')}.md"
            fpath = safe_path(posting_queue_path / fname)
            if not fpath.exists():
                fpath.write_text(post_text)
                new_posts += 1

        new_reg_entries.append({"offer_name": offer_name, "slug": slug, "promoted_at": TIMESTAMP})
        promoted_names.add(offer_name)

    if new_reg_entries:
        all_reg = new_reg_entries + existing_reg
        aff_promo_registry_path.write_text(json.dumps(all_reg[:100], indent=2))
        wired_total += new_posts
        connections[name] = {"status": "OK", "items": new_posts}
    else:
        connections[name] = {"status": "deduped_or_no_candidates", "items": 0}


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def run_cycle():
    print("=" * 65)
    print("CROSS-POLLINATOR V2 (17 connections)")
    print(f"Time: {TIMESTAMP}")
    print("=" * 65)

    # Original 6 connections
    wire_alpha_to_content_farm_topics()
    wire_openclaw_to_outreach_followup()
    wire_content_farm_to_affiliate_distribute()
    wire_reddit_to_openclaw_grading()
    wire_outreach_leads_to_app_factory()
    wire_alpha_tools_to_affiliate_offers()

    # Connections 7-11 (added 2026-04-02)
    wire_stripe_products_to_content_promo()
    wire_deployed_sites_to_content()
    wire_brokering_to_content_topics()
    wire_apps_to_outbound_angles()
    wire_demand_signals_to_product_specs()

    # Connections 12-14 (added 2026-04-02 cycle 2)
    wire_comp_intel_to_app_factory()
    wire_before_you_to_content_farm()
    wire_new_alpha_to_outreach_angles()

    # Connections 15-17 (added 2026-04-03)
    wire_build_app_alpha_to_spec_queue()
    wire_spec_queue_to_content_teasers()
    wire_affiliate_candidates_to_content_promo()

    print("\n--- WIRING RESULTS ---")
    for conn_name, result in connections.items():
        status = result["status"]
        items = result.get("items", 0)
        symbol = "[+]" if items > 0 else "[-]"
        print(f"  {symbol} {conn_name}: {items} ({status})")

    print(f"\nTotal items wired: {wired_total}")
    return wired_total, connections


def run_status():
    print("CROSS-POLLINATOR V2 — output files (14 connections)")
    outputs = [
        AUTOMATIONS / "agent" / "autonomy" / "content_farm_topic_queue.json",
        OUTBOUND_LEADS / "followup_queue.json",
        AUTOMATIONS / "agent" / "autonomy" / "affiliate_distribute_targets.json",
        AUTOMATIONS / "agent" / "autonomy" / "openclaw_grade_signals.json",
        AUTOMATIONS / "agent" / "autonomy" / "app_factory_spec_queue.json",
        AUTOMATIONS / "agent" / "autonomy" / "affiliate_offer_candidates.json",
        AUTOMATIONS / "agent" / "autonomy" / "product_promo_registry.json",
        AUTOMATIONS / "agent" / "autonomy" / "site_showcase_registry.json",
        AUTOMATIONS / "agent" / "autonomy" / "outreach_portfolio_angles.json",
        AUTOMATIONS / "agent" / "autonomy" / "product_creation_queue.json",
        AUTOMATIONS / "agent" / "autonomy" / "before_you_promo_registry.json",
        AUTOMATIONS / "agent" / "autonomy" / "outreach_trend_angles.json",
    ]
    for p in outputs:
        exists = Path(p).exists()
        size = Path(p).stat().st_size if exists else 0
        status = f"OK ({size} bytes)" if exists else "MISSING"
        print(f"  {'[+]' if exists else '[!]'} {p.name}: {status}")


if __name__ == "__main__":
    if "--status" in sys.argv:
        run_status()
    else:
        run_cycle()
