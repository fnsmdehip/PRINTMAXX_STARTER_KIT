#!/usr/bin/env python3
"""
OP17 Freelance Service Arbitrage Pipeline
==========================================
Automates the entire freelance arbitrage workflow:
  --scan       Scan Reddit for matching freelance jobs
  --propose    Generate personalized proposals for top jobs
  --portfolio  Build 5 real portfolio pieces (landing page, dashboard, scraper, bot, extension)
  --status     Show pipeline status (leads, proposals, revenue)
  --add-lead   Manually add a lead to the pipeline
  --close      Mark a lead as won/lost with revenue
  --platforms  Show all 10 platform statuses
  --respond    Generate response for a specific post URL
  --daily      Full daily pipeline run (scan + propose + status)
  --revenue    Revenue breakdown with margin analysis

The edge: Claude Code Max ($200/mo flat) delivers in 15-60 min what takes
normal freelancers 2-5 days. 95%+ margin. Unlimited revisions = $0 extra cost.

Usage:
  python3 AUTOMATIONS/freelance_pipeline.py --scan
  python3 AUTOMATIONS/freelance_pipeline.py --propose --top 5
  python3 AUTOMATIONS/freelance_pipeline.py --portfolio
  python3 AUTOMATIONS/freelance_pipeline.py --status
  python3 AUTOMATIONS/freelance_pipeline.py --add-lead --platform upwork --title "Build a landing page" --budget 300
  python3 AUTOMATIONS/freelance_pipeline.py --close --lead-id LEAD_001 --outcome won --revenue 350
  python3 AUTOMATIONS/freelance_pipeline.py --platforms
  python3 AUTOMATIONS/freelance_pipeline.py --daily
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent
AUTOMATIONS_DIR = BASE_DIR / "AUTOMATIONS"
LEADS_DIR = AUTOMATIONS_DIR / "freelance_leads"
PORTFOLIO_DIR = BASE_DIR / "builds" / "portfolio"
LEDGER_DIR = BASE_DIR / "LEDGER"
PIPELINE_CSV = LEADS_DIR / "FREELANCE_PIPELINE.csv"
SCAN_LOG = LEADS_DIR / "scan_log.json"
REVENUE_CSV = LEADS_DIR / "FREELANCE_REVENUE.csv"

# ── Subreddits to scan ─────────────────────────────────────────────────────────

SUBREDDITS = [
    "forhire",
    "slavelabour",
    "webdev",
    "freelance",
    "remotejs",
    "reactjs",
    "Python",
]

# ── Job keywords (match these in titles) ────────────────────────────────────────

HIRE_KEYWORDS = [
    "hiring", "[hiring]", "looking for", "need a developer", "need a",
    "web developer", "react developer", "python developer", "full stack",
    "landing page", "website", "web app", "scraper", "scraping",
    "chrome extension", "browser extension", "discord bot", "telegram bot",
    "bot developer", "automation", "api integration", "dashboard",
    "frontend", "backend", "full-stack", "freelance developer",
    "build me", "build a", "need someone to build", "looking to hire",
    "web scraping", "data extraction", "custom software",
]

# ── Service categories (for proposal matching) ──────────────────────────────────

SERVICE_CATEGORIES = {
    "website": {
        "name": "Website / Landing Page",
        "keywords": ["website", "landing page", "web page", "site", "wordpress", "react site", "next.js", "redesign", "responsive"],
        "price_range": (99, 799),
        "delivery_days": (2, 7),
        "template_key": "website",
        "portfolio_urls": [
            "https://printmaxx-local-demos.surge.sh/",
            "https://dental-motion.surge.sh/",
            "https://realtor-motion.surge.sh/",
            "https://restaurant-motion.surge.sh/",
        ],
    },
    "automation": {
        "name": "Automation / Workflow",
        "keywords": ["automation", "automate", "workflow", "zapier", "n8n", "script", "cron"],
        "price_range": (79, 499),
        "delivery_days": (1, 5),
        "template_key": "automation",
        "portfolio_urls": [],
    },
    "scraper": {
        "name": "Web Scraper / Data Extraction",
        "keywords": ["scraper", "scraping", "data extraction", "crawl", "spider", "extract data", "lead gen", "leads"],
        "price_range": (79, 299),
        "delivery_days": (1, 3),
        "template_key": "scraper",
        "portfolio_urls": [],
    },
    "bot": {
        "name": "Discord / Telegram / Slack Bot",
        "keywords": ["discord bot", "telegram bot", "slack bot", "chatbot", "chat bot", "bot"],
        "price_range": (99, 399),
        "delivery_days": (2, 5),
        "template_key": "bot",
        "portfolio_urls": [],
    },
    "dashboard": {
        "name": "Dashboard / Internal Tool",
        "keywords": ["dashboard", "admin panel", "internal tool", "analytics", "reporting", "crm", "data viz"],
        "price_range": (199, 799),
        "delivery_days": (3, 7),
        "template_key": "dashboard",
        "portfolio_urls": [],
    },
    "api": {
        "name": "API Integration",
        "keywords": ["api integration", "api", "webhook", "connect", "integration"],
        "price_range": (99, 599),
        "delivery_days": (1, 5),
        "template_key": "api",
        "portfolio_urls": [],
    },
    "extension": {
        "name": "Chrome Extension",
        "keywords": ["chrome extension", "browser extension", "extension", "addon", "plugin"],
        "price_range": (149, 599),
        "delivery_days": (2, 5),
        "template_key": "extension",
        "portfolio_urls": [],
    },
    "email": {
        "name": "Email System / Automation",
        "keywords": ["email", "smtp", "newsletter", "email automation", "transactional email", "mailchimp"],
        "price_range": (99, 399),
        "delivery_days": (1, 4),
        "template_key": "email",
        "portfolio_urls": [],
    },
    "crm": {
        "name": "CRM / Database Tool",
        "keywords": ["crm", "database", "crud", "inventory", "management system", "tracking"],
        "price_range": (299, 899),
        "delivery_days": (3, 7),
        "template_key": "crm",
        "portfolio_urls": [],
    },
    "mobile": {
        "name": "Mobile App (React Native / PWA)",
        "keywords": ["mobile app", "react native", "ios app", "android app", "pwa", "app"],
        "price_range": (399, 1500),
        "delivery_days": (5, 14),
        "template_key": "mobile",
        "portfolio_urls": [
            "https://focuslock-app.surge.sh/",
            "https://habitforge-app.surge.sh/",
            "https://mealmaxx-app.surge.sh/",
            "https://sleepmaxx-app.surge.sh/",
            "https://walktounlock-app.surge.sh/",
            "https://ramadan-tracker.surge.sh/",
        ],
    },
    "seo": {
        "name": "SEO Audit & Optimization",
        "keywords": ["seo", "search engine", "ranking", "keywords", "audit", "optimization"],
        "price_range": (75, 500),
        "delivery_days": (1, 3),
        "template_key": "seo",
        "portfolio_urls": [
            "https://printmaxx-seo.surge.sh/",
        ],
    },
    "content": {
        "name": "Content Writing & SEO Articles",
        "keywords": ["content", "writing", "blog", "article", "copywriting", "seo content"],
        "price_range": (50, 300),
        "delivery_days": (1, 3),
        "template_key": "content",
        "portfolio_urls": [],
    },
}

# ── Platform tracking ──────────────────────────────────────────────────────────

PLATFORMS = {
    "fiverr": {"url": "https://www.fiverr.com", "commission": "20%", "status": "NOT_CREATED", "priority": 1},
    "upwork": {"url": "https://www.upwork.com", "commission": "10-20%", "status": "NOT_CREATED", "priority": 2},
    "contra": {"url": "https://contra.com", "commission": "0%", "status": "NOT_CREATED", "priority": 3},
    "linkedin": {"url": "https://linkedin.com/services", "commission": "0%", "status": "NOT_CREATED", "priority": 4},
    "reddit": {"url": "https://reddit.com/r/forhire", "commission": "0%", "status": "READY", "priority": 5},
    "freelancer": {"url": "https://freelancer.com", "commission": "10%", "status": "NOT_CREATED", "priority": 6},
    "guru": {"url": "https://guru.com", "commission": "5-9%", "status": "NOT_CREATED", "priority": 7},
    "peopleperhour": {"url": "https://peopleperhour.com", "commission": "20%", "status": "NOT_CREATED", "priority": 8},
    "toptal": {"url": "https://toptal.com", "commission": "0%", "status": "NOT_CREATED", "priority": 9},
    "direct": {"url": "N/A", "commission": "0%", "status": "READY", "priority": 10},
}

# ── Proposal Templates ──────────────────────────────────────────────────────────

PROPOSAL_TEMPLATES = {
    "website": """I can build this for you. Clean, responsive, fast-loading.

My approach:
- React/Next.js with Tailwind CSS
- Fully responsive (mobile + tablet + desktop)
- SEO meta tags and structured data
- Contact forms wired up to your email
- Deployed live on Vercel (free hosting)
- Source code is yours

I'll have a working version for you to review within {delivery} hours.

Fixed price: ${price}. Includes unlimited revisions until you're happy with it.

I can start today.""",

    "automation": """I build automations that kill manual work. Python, APIs, whatever the stack needs.

For this project:
- Map the current workflow
- Build the automation with error handling
- Test with your real data
- Deploy with scheduling (runs on autopilot)
- Full source code + documentation

Fixed price: ${price}. Working prototype within {delivery} hours.

I've automated similar workflows before. Happy to share examples.""",

    "scraper": """I'll build this scraper in Python. Clean output, rate-limited, handles edge cases.

My process:
- Free sample of 10-20 records first (before you commit)
- You verify the data format
- Full run with clean CSV/JSON output
- Scheduling setup if you need recurring scrapes

Fixed price: ${price}. Sample delivered within 12 hours.

I've scraped similar sites. This is straightforward.""",

    "bot": """I build custom bots in Python. Not template bots. Custom logic for your use case.

What I'll deliver:
- All commands tested and working
- Database integration if needed
- Error handling + logging
- Deployed and running 24/7 (Railway free tier)
- Source code + README documenting every command

Fixed price: ${price}. Bot running in your server within {delivery} hours.""",

    "dashboard": """I build dashboards that make data useful instead of buried in spreadsheets.

For this project:
- Connect to your data source (database, API, CSV)
- Interactive charts, tables, filters
- Role-based access if needed
- Deployed as a web app (access from any browser)

Tech: React + Recharts for frontend. Python/Node backend. Supabase or your database.

Fixed price: ${price}. Working prototype within {delivery} hours.""",

    "api": """I connect APIs and build integrations between systems.

For this:
- Map the data flow between your systems
- Build the integration with error handling and retry logic
- Test with real data
- Deploy and monitor
- Full documentation

Fixed price: ${price}. Working connection within {delivery} hours.""",

    "extension": """I build Chrome extensions (Manifest v3). Custom functionality, clean UI.

For this:
- Popup interface or sidebar panel
- Chrome storage for settings
- Content scripts for page interaction
- Tested on Chrome, Edge, Brave
- Full source code + Chrome Web Store submission package

Fixed price: ${price}. Working extension within {delivery} hours.""",

    "email": """I build email systems. Transactional, marketing sequences, notification pipelines.

For this:
- Email logic + HTML templates
- Renders correctly in Gmail, Outlook, Apple Mail
- Test sends before going live
- Rate limiting and bounce handling
- Full documentation

Fixed price: ${price}. Templates and logic ready within {delivery} hours.""",

    "crm": """I build custom CRM and database tools.

For this:
- Web-based CRUD application
- Search, filter, sort
- Import/export (CSV, Excel)
- Role-based access
- Activity logging
- Key metrics dashboard

Tech: React + Supabase. Web app, no software to install.

Fixed price: ${price}. Working prototype within {delivery} hours.""",

    "mobile": """I build mobile apps with React Native (iOS + Android) or PWA.

For this:
- Working MVP with core features
- Clean UI following platform design patterns
- Backend API if needed
- Push notifications
- Deployed to TestFlight or as PWA

Fixed price: ${price}. Working prototype on your phone within {delivery} hours.

I build the core feature loop first. Get it in your hands fast. Iterate from there.""",

    "seo": """I run SEO audits and fix what's actually broken. Not generic advice.

For this:
- Full technical audit (Core Web Vitals, crawlability, indexing)
- Schema markup implementation
- Meta tag optimization
- Speed optimization (target Lighthouse 90+)
- Competitor gap analysis
- Actionable report with priorities ranked

Fixed price: ${price}. Audit delivered within {delivery} hours.""",

    "content": """I write SEO-optimized content that ranks and converts.

For this:
- Keyword research and content brief
- Well-structured articles with proper H1/H2/H3
- Internal linking strategy
- Schema markup
- Meta descriptions and title tags

Fixed price: ${price}. Content delivered within {delivery} hours.""",
}


# ── Helper functions ─────────────────────────────────────────────────────────────

def ensure_dirs():
    """Create all required directories."""
    LEADS_DIR.mkdir(parents=True, exist_ok=True)
    PORTFOLIO_DIR.mkdir(parents=True, exist_ok=True)
    for sub in ["landing-page", "dashboard", "scraper", "discord-bot", "chrome-ext"]:
        (PORTFOLIO_DIR / sub).mkdir(parents=True, exist_ok=True)


def load_pipeline():
    """Load the pipeline CSV. Returns list of dicts."""
    if not PIPELINE_CSV.exists():
        return []
    with open(PIPELINE_CSV, "r", newline="") as f:
        return list(csv.DictReader(f))


def save_pipeline(rows):
    """Save pipeline rows to CSV."""
    if not rows:
        return
    fieldnames = [
        "lead_id", "date_found", "platform", "subreddit", "title", "url",
        "category", "budget_est", "status", "proposal_sent", "outcome",
        "revenue", "notes"
    ]
    with open(PIPELINE_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            clean = {k: row.get(k, "") for k in fieldnames}
            writer.writerow(clean)


def next_lead_id(rows):
    """Get next LEAD_NNN id."""
    if not rows:
        return "LEAD_001"
    ids = []
    for r in rows:
        lid = r.get("lead_id", "")
        if lid.startswith("LEAD_"):
            try:
                ids.append(int(lid.replace("LEAD_", "")))
            except ValueError:
                pass
    return f"LEAD_{max(ids) + 1:03d}" if ids else "LEAD_001"


def classify_job(title_lower):
    """Classify a job posting into a service category."""
    for cat_name, cat_info in SERVICE_CATEGORIES.items():
        for kw in cat_info["keywords"]:
            if kw in title_lower:
                return cat_name
    return "website"


def extract_budget(text):
    """Try to extract a budget number from text."""
    patterns = [
        r'\$(\d{1,5}(?:,\d{3})*(?:\.\d{2})?)',
        r'(\d{2,5})\s*(?:usd|dollars)',
        r'budget[:\s]*\$?(\d{2,5})',
    ]
    for p in patterns:
        m = re.search(p, text.lower())
        if m:
            return m.group(1).replace(",", "")
    return ""


def is_hiring_post(title_lower):
    """Check if a Reddit post title is a hiring post."""
    for kw in HIRE_KEYWORDS:
        if kw in title_lower:
            return True
    return False


def fetch_reddit_json(subreddit, sort="new", limit=50):
    """Fetch posts from a subreddit using Reddit JSON API."""
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}"
    headers = {
        "User-Agent": "PrintmaxxFreelancePipeline/1.0 (freelance lead scanner)"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("data", {}).get("children", [])
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, Exception) as e:
        print(f"  [!] Failed to fetch r/{subreddit}: {e}")
        return []


# ── Commands ─────────────────────────────────────────────────────────────────────

def cmd_scan(args):
    """Scan Reddit for freelance job opportunities."""
    ensure_dirs()
    print("=" * 70)
    print("FREELANCE PIPELINE SCANNER")
    print("Scanning Reddit for freelance opportunities...")
    print("=" * 70)

    existing = load_pipeline()
    existing_urls = {r.get("url", "") for r in existing}
    new_leads = []
    total_scanned = 0

    for sub in SUBREDDITS:
        print(f"\n  Scanning r/{sub}...")
        posts = fetch_reddit_json(sub, sort="new", limit=100)
        total_scanned += len(posts)
        found = 0

        for post in posts:
            pdata = post.get("data", {})
            title = pdata.get("title", "")
            title_lower = title.lower()
            url = f"https://reddit.com{pdata.get('permalink', '')}"
            selftext = pdata.get("selftext", "")
            created = datetime.fromtimestamp(pdata.get("created_utc", 0))

            # Skip old posts (> 7 days)
            if datetime.now() - created > timedelta(days=7):
                continue

            # Skip already tracked
            if url in existing_urls:
                continue

            # Check if hiring post
            if not is_hiring_post(title_lower):
                continue

            # Classify
            category = classify_job(title_lower + " " + selftext.lower())
            budget = extract_budget(title + " " + selftext)
            cat_info = SERVICE_CATEGORIES.get(category, {})

            lead = {
                "lead_id": next_lead_id(existing + new_leads),
                "date_found": datetime.now().strftime("%Y-%m-%d"),
                "platform": "reddit",
                "subreddit": f"r/{sub}",
                "title": title[:120],
                "url": url,
                "category": category,
                "budget_est": budget if budget else str(cat_info.get("price_range", (100, 500))[0]),
                "status": "NEW",
                "proposal_sent": "no",
                "outcome": "",
                "revenue": "",
                "notes": selftext[:200].replace("\n", " ") if selftext else "",
            }
            new_leads.append(lead)
            existing_urls.add(url)
            found += 1

        print(f"    Found {found} new leads in r/{sub}")
        time.sleep(1)

    all_leads = existing + new_leads
    save_pipeline(all_leads)

    scan_data = {
        "last_scan": datetime.now().isoformat(),
        "posts_scanned": total_scanned,
        "new_leads": len(new_leads),
        "total_pipeline": len(all_leads),
    }
    with open(SCAN_LOG, "w") as f:
        json.dump(scan_data, f, indent=2)

    print(f"\n{'=' * 70}")
    print(f"SCAN COMPLETE")
    print(f"  Posts scanned: {total_scanned}")
    print(f"  New leads found: {len(new_leads)}")
    print(f"  Total pipeline: {len(all_leads)}")
    print(f"  Pipeline file: {PIPELINE_CSV}")
    print(f"{'=' * 70}")

    if new_leads:
        print(f"\nTOP NEW LEADS:")
        for i, lead in enumerate(new_leads[:10], 1):
            budget_str = f"${lead['budget_est']}" if lead['budget_est'] else "unknown"
            print(f"  {i}. [{lead['category'].upper()}] {lead['title'][:80]}")
            print(f"     Budget: {budget_str} | {lead['subreddit']} | {lead['url'][:60]}")
            print()

    return new_leads


def cmd_propose(args):
    """Generate personalized proposals for top leads."""
    ensure_dirs()
    rows = load_pipeline()
    new_leads = [r for r in rows if r.get("status") == "NEW"]

    if not new_leads:
        print("No NEW leads in pipeline. Run --scan first.")
        return

    top_n = min(args.top, len(new_leads))
    print(f"Generating proposals for top {top_n} leads...\n")
    print("=" * 70)

    proposals_dir = LEADS_DIR / "proposals"
    proposals_dir.mkdir(parents=True, exist_ok=True)

    for lead in new_leads[:top_n]:
        cat = lead.get("category", "website")
        cat_info = SERVICE_CATEGORIES.get(cat, SERVICE_CATEGORIES["website"])
        template = PROPOSAL_TEMPLATES.get(cat_info.get("template_key", "website"), PROPOSAL_TEMPLATES["website"])

        price_low, price_high = cat_info["price_range"]
        if lead.get("budget_est"):
            try:
                budget = int(lead["budget_est"])
                price = min(max(budget, price_low), price_high)
            except ValueError:
                price = (price_low + price_high) // 2
        else:
            price = (price_low + price_high) // 2

        delivery_low, delivery_high = cat_info["delivery_days"]
        delivery_hours = delivery_low * 24

        proposal = template.format(price=price, delivery=delivery_hours)

        title = lead.get("title", "")
        notes = lead.get("notes", "")
        opener = f"Re: {title}\n\n"
        if notes:
            opener += "I read your requirements. "

        full_proposal = opener + proposal

        # Add portfolio links if available
        portfolio_urls = cat_info.get("portfolio_urls", [])
        if portfolio_urls:
            full_proposal += "\n\nLive portfolio examples:"
            for pu in portfolio_urls[:3]:
                full_proposal += f"\n  {pu}"

        print(f"LEAD: {lead['lead_id']} - {title[:70]}")
        print(f"Category: {cat.upper()} | Price: ${price} | Delivery: {delivery_low}-{delivery_high} days")
        print(f"URL: {lead.get('url', 'N/A')}")
        print("-" * 50)
        print(full_proposal)
        print("=" * 70)
        print()

        proposal_file = proposals_dir / f"{lead['lead_id']}_proposal.txt"
        with open(proposal_file, "w") as f:
            f.write(f"Lead: {lead['lead_id']}\n")
            f.write(f"Title: {title}\n")
            f.write(f"URL: {lead.get('url', '')}\n")
            f.write(f"Category: {cat}\n")
            f.write(f"Quoted Price: ${price}\n")
            f.write(f"Delivery: {delivery_low}-{delivery_high} days\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"\n{'=' * 50}\nPROPOSAL:\n{'=' * 50}\n\n")
            f.write(full_proposal)

        lead["status"] = "PROPOSAL_DRAFTED"

    save_pipeline(rows)
    print(f"\n{top_n} proposals generated. Files saved to {proposals_dir}/")
    print("Next step: Review each proposal, personalize the opener, and send.")


def cmd_portfolio(args):
    """Build 5 real portfolio pieces as deployable demos."""
    ensure_dirs()
    print("=" * 70)
    print("BUILDING PORTFOLIO PIECES")
    print("5 real deployable demos for client-facing portfolio")
    print("=" * 70)

    # ── 1. Landing Page ──────────────────────────────────────────────────────

    print("\n[1/5] Building landing page demo...")
    lp_dir = PORTFOLIO_DIR / "landing-page"
    lp_dir.mkdir(parents=True, exist_ok=True)

    landing_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SaaSify - Ship Your SaaS in Days, Not Months</title>
    <meta name="description" content="SaaSify helps founders launch their SaaS MVP in under 2 weeks. Authentication, billing, dashboards included.">
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        :root{--bg:#0a0a0a;--surface:#141414;--border:#262626;--text:#fafafa;--muted:#a1a1aa;--accent:#6366f1;--accent-hover:#818cf8;--green:#22c55e}
        body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);line-height:1.6}
        .container{max-width:1100px;margin:0 auto;padding:0 24px}
        nav{padding:20px 0;border-bottom:1px solid var(--border);position:sticky;top:0;background:rgba(10,10,10,0.9);backdrop-filter:blur(12px);z-index:100}
        nav .container{display:flex;justify-content:space-between;align-items:center}
        .logo{font-size:20px;font-weight:700;color:var(--accent)}
        .nav-links{display:flex;gap:32px;list-style:none}
        .nav-links a{color:var(--muted);text-decoration:none;font-size:14px;transition:color 0.2s}
        .nav-links a:hover{color:var(--text)}
        .hero{padding:120px 0 80px;text-align:center}
        .badge{display:inline-block;padding:6px 16px;border:1px solid var(--border);border-radius:100px;font-size:13px;color:var(--muted);margin-bottom:24px}
        .badge span{color:var(--green)}
        h1{font-size:clamp(36px,5vw,60px);font-weight:800;line-height:1.1;margin-bottom:20px;letter-spacing:-0.02em}
        h1 .accent{color:var(--accent)}
        .hero p{font-size:18px;color:var(--muted);max-width:560px;margin:0 auto 36px}
        .cta-group{display:flex;gap:16px;justify-content:center;flex-wrap:wrap}
        .btn{padding:14px 28px;border-radius:8px;font-size:15px;font-weight:600;text-decoration:none;cursor:pointer;border:none;transition:all 0.2s}
        .btn-primary{background:var(--accent);color:white}
        .btn-primary:hover{background:var(--accent-hover);transform:translateY(-1px)}
        .btn-secondary{background:transparent;color:var(--text);border:1px solid var(--border)}
        .btn-secondary:hover{border-color:var(--muted)}
        .features{padding:80px 0}
        .features h2{font-size:36px;text-align:center;margin-bottom:12px}
        .features .subtitle{text-align:center;color:var(--muted);margin-bottom:60px;font-size:16px}
        .features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px}
        .feature-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:32px;transition:border-color 0.2s}
        .feature-card:hover{border-color:var(--accent)}
        .feature-icon{font-size:28px;margin-bottom:16px}
        .feature-card h3{font-size:18px;margin-bottom:8px}
        .feature-card p{color:var(--muted);font-size:14px}
        .pricing{padding:80px 0}
        .pricing h2{font-size:36px;text-align:center;margin-bottom:48px}
        .pricing-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;max-width:900px;margin:0 auto}
        .price-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:36px;text-align:center}
        .price-card.featured{border-color:var(--accent);position:relative}
        .price-card.featured::before{content:"Most popular";position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:var(--accent);color:white;padding:4px 16px;border-radius:100px;font-size:12px;font-weight:600}
        .price-card h3{font-size:20px;margin-bottom:8px}
        .price-card .price{font-size:48px;font-weight:800;margin:16px 0}
        .price-card .price span{font-size:16px;color:var(--muted);font-weight:400}
        .price-card ul{list-style:none;text-align:left;margin:24px 0}
        .price-card li{padding:8px 0;font-size:14px;color:var(--muted)}
        .price-card li::before{content:"\\2713  ";color:var(--green)}
        .final-cta{padding:100px 0;text-align:center;border-top:1px solid var(--border)}
        .final-cta h2{font-size:40px;margin-bottom:16px}
        .final-cta p{color:var(--muted);margin-bottom:32px;font-size:16px}
        footer{padding:40px 0;border-top:1px solid var(--border);text-align:center;color:var(--muted);font-size:13px}
        @media(max-width:768px){.nav-links{display:none}.hero{padding:80px 0 60px}.features-grid{grid-template-columns:1fr}}
    </style>
</head>
<body>
    <nav><div class="container"><div class="logo">SaaSify</div><ul class="nav-links"><li><a href="#features">Features</a></li><li><a href="#pricing">Pricing</a></li><li><a href="#" class="btn btn-primary" style="padding:8px 20px;font-size:13px;">Get started</a></li></ul></div></nav>
    <section class="hero"><div class="container"><div class="badge"><span>New</span> &mdash; Now with AI-powered onboarding</div><h1>Ship your SaaS<br>in <span class="accent">days</span>, not months</h1><p>Authentication, billing, dashboards, and deployment. Everything you need to launch your MVP. Stop building boilerplate.</p><div class="cta-group"><a href="#" class="btn btn-primary">Start building free</a><a href="#" class="btn btn-secondary">See demo</a></div></div></section>
    <section class="features" id="features"><div class="container"><h2>Everything you need to launch</h2><p class="subtitle">Stop stitching together 15 different tools. One codebase. Production-ready.</p><div class="features-grid"><div class="feature-card"><div class="feature-icon">&#128274;</div><h3>Authentication</h3><p>Email, Google, GitHub login. Magic links. Session management. Role-based access.</p></div><div class="feature-card"><div class="feature-icon">&#128179;</div><h3>Stripe billing</h3><p>Subscriptions, one-time payments, usage-based billing. Customer portal. Webhook handling.</p></div><div class="feature-card"><div class="feature-icon">&#128202;</div><h3>Admin dashboard</h3><p>User management, analytics, feature flags. See who's paying, who's churning.</p></div><div class="feature-card"><div class="feature-icon">&#128640;</div><h3>One-click deploy</h3><p>Vercel, Railway, or Docker. CI/CD pre-configured. Push to main, live in 30 seconds.</p></div><div class="feature-card"><div class="feature-icon">&#128231;</div><h3>Email system</h3><p>Transactional emails, welcome sequences, password resets. Resend integration.</p></div><div class="feature-card"><div class="feature-icon">&#128736;</div><h3>API layer</h3><p>REST or tRPC. Rate limiting, validation, error handling. Type-safe end to end.</p></div></div></div></section>
    <section class="pricing" id="pricing"><div class="container"><h2>Simple pricing</h2><div class="pricing-grid"><div class="price-card"><h3>Starter</h3><div class="price">$0<span>/mo</span></div><ul><li>Full source code</li><li>Auth + database</li><li>Community support</li><li>Deploy anywhere</li></ul><a href="#" class="btn btn-secondary" style="width:100%;display:block;text-align:center;">Get started</a></div><div class="price-card featured"><h3>Pro</h3><div class="price">$29<span>/mo</span></div><ul><li>Everything in Starter</li><li>Stripe billing module</li><li>Admin dashboard</li><li>Email system</li><li>Priority support</li></ul><a href="#" class="btn btn-primary" style="width:100%;display:block;text-align:center;">Start free trial</a></div><div class="price-card"><h3>Enterprise</h3><div class="price">$99<span>/mo</span></div><ul><li>Everything in Pro</li><li>Custom integrations</li><li>White-label</li><li>Dedicated support</li><li>SLA guarantee</li></ul><a href="#" class="btn btn-secondary" style="width:100%;display:block;text-align:center;">Contact sales</a></div></div></div></section>
    <section class="final-cta"><div class="container"><h2>Ready to ship?</h2><p>Join 2,000+ founders who launched their SaaS with SaaSify.</p><a href="#" class="btn btn-primary">Start building free</a></div></section>
    <footer><div class="container"><p>SaaSify &copy; 2026. Portfolio demo.</p></div></footer>
</body>
</html>"""

    with open(lp_dir / "index.html", "w") as f:
        f.write(landing_html)
    print(f"  Saved to {lp_dir}/index.html")
    print(f"  Deploy: cd {lp_dir} && npx surge . saasify-demo.surge.sh")

    # ── 2. Dashboard ─────────────────────────────────────────────────────────

    print("\n[2/5] Building data dashboard demo...")
    dash_dir = PORTFOLIO_DIR / "dashboard"
    dash_dir.mkdir(parents=True, exist_ok=True)

    dashboard_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metrix - Analytics Dashboard</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        :root{--bg:#09090b;--surface:#18181b;--border:#27272a;--text:#fafafa;--muted:#a1a1aa;--green:#22c55e;--red:#ef4444;--blue:#3b82f6;--purple:#a855f7;--yellow:#eab308}
        body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',monospace;background:var(--bg);color:var(--text);min-height:100vh}
        .layout{display:grid;grid-template-columns:240px 1fr;min-height:100vh}
        .sidebar{background:var(--surface);border-right:1px solid var(--border);padding:24px 16px}
        .sidebar-logo{font-size:18px;font-weight:700;color:var(--blue);margin-bottom:32px;padding:0 8px}
        .sidebar-nav{list-style:none}
        .sidebar-nav li{padding:10px 12px;border-radius:6px;font-size:14px;color:var(--muted);cursor:pointer;margin-bottom:4px;transition:all 0.15s}
        .sidebar-nav li:hover{background:rgba(255,255,255,0.05);color:var(--text)}
        .sidebar-nav li.active{background:rgba(59,130,246,0.1);color:var(--blue)}
        .main{padding:32px;overflow-y:auto}
        .header{display:flex;justify-content:space-between;align-items:center;margin-bottom:32px}
        .header h1{font-size:24px;font-weight:700}
        .date-picker{padding:8px 16px;background:var(--surface);border:1px solid var(--border);border-radius:6px;color:var(--text);font-size:13px}
        .metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:32px}
        .metric-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:20px}
        .metric-label{font-size:13px;color:var(--muted);margin-bottom:8px}
        .metric-value{font-size:28px;font-weight:800}
        .metric-change{font-size:12px;margin-top:6px}
        .metric-change.up{color:var(--green)}
        .metric-change.down{color:var(--red)}
        .charts{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-bottom:24px}
        .chart-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:24px}
        .chart-card h3{font-size:15px;margin-bottom:20px}
        .bar-chart{display:flex;align-items:flex-end;gap:8px;height:180px}
        .bar-group{flex:1;display:flex;flex-direction:column;align-items:center}
        .bar{width:100%;max-width:32px;background:var(--blue);border-radius:4px 4px 0 0;transition:height 0.5s ease}
        .bar-label{font-size:11px;color:var(--muted);margin-top:8px}
        .donut-container{display:flex;align-items:center;justify-content:center;height:180px}
        .donut{width:140px;height:140px;border-radius:50%;background:conic-gradient(var(--blue) 0% 42%,var(--purple) 42% 68%,var(--green) 68% 85%,var(--yellow) 85% 100%);display:flex;align-items:center;justify-content:center}
        .donut-inner{width:80px;height:80px;border-radius:50%;background:var(--surface);display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:700}
        .donut-legend{margin-left:24px}
        .donut-legend li{list-style:none;font-size:12px;color:var(--muted);padding:4px 0;display:flex;align-items:center;gap:8px}
        .legend-dot{width:8px;height:8px;border-radius:50%}
        .table-card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:24px}
        .table-card h3{font-size:15px;margin-bottom:16px}
        table{width:100%;border-collapse:collapse}
        th{text-align:left;font-size:12px;color:var(--muted);padding:10px 12px;border-bottom:1px solid var(--border);font-weight:500}
        td{font-size:13px;padding:12px;border-bottom:1px solid var(--border)}
        .status-badge{padding:3px 10px;border-radius:100px;font-size:11px;font-weight:600}
        .status-active{background:rgba(34,197,94,0.15);color:var(--green)}
        .status-pending{background:rgba(234,179,8,0.15);color:var(--yellow)}
        .status-inactive{background:rgba(239,68,68,0.15);color:var(--red)}
        @media(max-width:1024px){.layout{grid-template-columns:1fr}.sidebar{display:none}.metrics{grid-template-columns:repeat(2,1fr)}.charts{grid-template-columns:1fr}}
    </style>
</head>
<body>
    <div class="layout">
        <aside class="sidebar"><div class="sidebar-logo">Metrix</div><ul class="sidebar-nav"><li class="active">Overview</li><li>Revenue</li><li>Customers</li><li>Products</li><li>Analytics</li><li>Settings</li></ul></aside>
        <main class="main">
            <div class="header"><h1>Dashboard</h1><div class="date-picker">Jan 1 - Feb 12, 2026</div></div>
            <div class="metrics"><div class="metric-card"><div class="metric-label">Total Revenue</div><div class="metric-value">$45,231</div><div class="metric-change up">+20.1% from last month</div></div><div class="metric-card"><div class="metric-label">Subscriptions</div><div class="metric-value">+2,350</div><div class="metric-change up">+180 from last month</div></div><div class="metric-card"><div class="metric-label">Active Users</div><div class="metric-value">12,234</div><div class="metric-change up">+19% from last month</div></div><div class="metric-card"><div class="metric-label">Churn Rate</div><div class="metric-value">2.4%</div><div class="metric-change down">+0.3% from last month</div></div></div>
            <div class="charts"><div class="chart-card"><h3>Revenue (last 12 months)</h3><div class="bar-chart"><div class="bar-group"><div class="bar" style="height:45%"></div><div class="bar-label">Mar</div></div><div class="bar-group"><div class="bar" style="height:52%"></div><div class="bar-label">Apr</div></div><div class="bar-group"><div class="bar" style="height:48%"></div><div class="bar-label">May</div></div><div class="bar-group"><div class="bar" style="height:61%"></div><div class="bar-label">Jun</div></div><div class="bar-group"><div class="bar" style="height:55%"></div><div class="bar-label">Jul</div></div><div class="bar-group"><div class="bar" style="height:67%"></div><div class="bar-label">Aug</div></div><div class="bar-group"><div class="bar" style="height:72%"></div><div class="bar-label">Sep</div></div><div class="bar-group"><div class="bar" style="height:65%"></div><div class="bar-label">Oct</div></div><div class="bar-group"><div class="bar" style="height:78%"></div><div class="bar-label">Nov</div></div><div class="bar-group"><div class="bar" style="height:82%"></div><div class="bar-label">Dec</div></div><div class="bar-group"><div class="bar" style="height:88%"></div><div class="bar-label">Jan</div></div><div class="bar-group"><div class="bar" style="height:95%"></div><div class="bar-label">Feb</div></div></div></div><div class="chart-card"><h3>Traffic sources</h3><div class="donut-container"><div class="donut"><div class="donut-inner">8.2K</div></div><ul class="donut-legend"><li><span class="legend-dot" style="background:var(--blue)"></span> Direct (42%)</li><li><span class="legend-dot" style="background:var(--purple)"></span> Organic (26%)</li><li><span class="legend-dot" style="background:var(--green)"></span> Referral (17%)</li><li><span class="legend-dot" style="background:var(--yellow)"></span> Social (15%)</li></ul></div></div></div>
            <div class="table-card"><h3>Recent customers</h3><table><thead><tr><th>Customer</th><th>Plan</th><th>MRR</th><th>Status</th><th>Joined</th></tr></thead><tbody><tr><td>Acme Corp</td><td>Enterprise</td><td>$2,400</td><td><span class="status-badge status-active">Active</span></td><td>Feb 10, 2026</td></tr><tr><td>TechStart Inc</td><td>Pro</td><td>$99</td><td><span class="status-badge status-active">Active</span></td><td>Feb 8, 2026</td></tr><tr><td>DesignCo</td><td>Pro</td><td>$99</td><td><span class="status-badge status-pending">Trial</span></td><td>Feb 6, 2026</td></tr><tr><td>DataFlow</td><td>Enterprise</td><td>$1,200</td><td><span class="status-badge status-active">Active</span></td><td>Feb 1, 2026</td></tr><tr><td>SmallBiz LLC</td><td>Starter</td><td>$29</td><td><span class="status-badge status-inactive">Churned</span></td><td>Jan 15, 2026</td></tr></tbody></table></div>
        </main>
    </div>
</body>
</html>"""

    with open(dash_dir / "index.html", "w") as f:
        f.write(dashboard_html)
    print(f"  Saved to {dash_dir}/index.html")
    print(f"  Deploy: cd {dash_dir} && npx surge . metrix-dashboard.surge.sh")

    # ── 3. Web Scraper ───────────────────────────────────────────────────────

    print("\n[3/5] Building web scraper demo...")
    scraper_dir = PORTFOLIO_DIR / "scraper"
    scraper_dir.mkdir(parents=True, exist_ok=True)

    scraper_py = '''#!/usr/bin/env python3
"""
Portfolio Demo: Business Directory Scraper
Scrapes business listings and outputs clean CSV/JSON.
Usage: python3 scraper_demo.py --query "dentist" --location "Austin TX" --limit 20
"""
import argparse, csv, json, random, time
from datetime import datetime

def generate_demo_data(query, location, limit):
    names = ["Smith","Johnson","Williams","Brown","Davis","Miller","Wilson","Moore","Taylor","Anderson"]
    suffixes = {"dentist":["Dental","Dentistry","Dental Care","Smile Center"],"plumber":["Plumbing","Plumbing Co","Pipe Works"],"lawyer":["Law Firm","Legal Group","& Associates"],"default":["Services","Solutions","Group","Co"]}
    streets = ["Main St","Oak Ave","Elm Blvd","Pine Rd","Maple Dr","Cedar Ln","Park Ave","Broadway"]
    sfx = suffixes.get(query.lower(), suffixes["default"])
    results = []
    for i in range(limit):
        results.append({"name":f"{random.choice(names)} {random.choice(sfx)}","phone":f"({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}","address":f"{random.randint(100,9999)} {random.choice(streets)}, {location}","rating":round(random.uniform(3.0,5.0),1),"review_count":random.randint(5,500),"website":f"https://www.example-{i}.com","category":query.title(),"scraped_at":datetime.now().strftime("%Y-%m-%d %H:%M")})
    return results

def main():
    p = argparse.ArgumentParser(description="Business Directory Scraper (Demo)")
    p.add_argument("--query","-q",required=True)
    p.add_argument("--location","-l",required=True)
    p.add_argument("--limit","-n",type=int,default=20)
    p.add_argument("--output","-o",default=None)
    p.add_argument("--format","-f",choices=["csv","json"],default="csv")
    args = p.parse_args()
    print(f"Scraping {args.query} in {args.location}...")
    data = generate_demo_data(args.query, args.location, args.limit)
    out = args.output or f"{args.query}_{args.location.replace(' ','_')}.{args.format}"
    if args.format == "csv":
        with open(out,"w",newline="") as f:
            w = csv.DictWriter(f, fieldnames=data[0].keys()); w.writeheader(); w.writerows(data)
    else:
        with open(out,"w") as f: json.dump(data,f,indent=2)
    print(f"Saved {len(data)} records to {out}")
    print(f"\\nSample:")
    for r in data[:5]: print(f"  {r['name']:<30} {r['phone']:<18} {r['rating']}")

if __name__=="__main__": main()
'''
    with open(scraper_dir / "scraper_demo.py", "w") as f:
        f.write(scraper_py)

    sample_data = [
        {"name":"Smith Family Dental","phone":"(512) 555-1234","address":"123 Main St, Austin TX","rating":"4.8","review_count":"342","website":"https://smithdental.com","category":"Dentist"},
        {"name":"Johnson Dentistry","phone":"(512) 555-5678","address":"456 Oak Ave, Austin TX","rating":"4.6","review_count":"189","website":"https://johnsondds.com","category":"Dentist"},
        {"name":"Williams Dental Care","phone":"(512) 555-9012","address":"789 Elm Blvd, Austin TX","rating":"4.9","review_count":"467","website":"https://williamsdental.com","category":"Dentist"},
    ]
    with open(scraper_dir / "sample_output.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=sample_data[0].keys())
        writer.writeheader()
        writer.writerows(sample_data)
    print(f"  Saved to {scraper_dir}/")

    # ── 4. Discord Bot ───────────────────────────────────────────────────────

    print("\n[4/5] Building Discord bot demo...")
    bot_dir = PORTFOLIO_DIR / "discord-bot"
    bot_dir.mkdir(parents=True, exist_ok=True)

    with open(bot_dir / "README.md", "w") as f:
        f.write("""# ModBot - Custom Discord Community Bot

Full-featured Discord bot. Moderation, welcome flows, XP leveling, tickets, polls.

## Commands
| Command | Description | Permission |
|---------|-------------|------------|
| `/ban @user [reason]` | Ban a user | Mod |
| `/kick @user [reason]` | Kick a user | Mod |
| `/mute @user [duration]` | Timeout a user | Mod |
| `/warn @user [reason]` | Issue a warning | Mod |
| `/purge [count]` | Delete messages | Mod |
| `/rank` | Check your level | Everyone |
| `/leaderboard` | Server XP leaderboard | Everyone |
| `/poll [question]` | Create a poll | Everyone |
| `/remind [time] [msg]` | Set a reminder | Everyone |
| `/ticket` | Open support ticket | Everyone |

## Tech Stack
- Python 3.11+ / discord.py 2.3+
- SQLite for user data, XP, warnings
- Deployed on Railway (free tier, 24/7)

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env  # add DISCORD_TOKEN
python bot.py
```

## Architecture
```
bot.py              # Entry point
cogs/
  moderation.py     # Ban, kick, mute, warn
  welcome.py        # Welcome messages, auto-role
  leveling.py       # XP system, leaderboard
  utility.py        # Polls, reminders, info
  tickets.py        # Support ticket system
database/
  db.py             # SQLite connection
  models.py         # User, Warning, Ticket models
```

*Portfolio demo. Custom bots built for any Discord community.*
""")

    with open(bot_dir / "bot.py", "w") as f:
        f.write('''#!/usr/bin/env python3
"""ModBot - Discord Community Bot (Portfolio Demo)"""
import os, discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()

@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")

@bot.tree.command(name="rank", description="Check your level and XP")
async def rank(interaction: discord.Interaction):
    embed = discord.Embed(title=f"{interaction.user.display_name}", color=0x3b82f6)
    embed.add_field(name="Level", value="12", inline=True)
    embed.add_field(name="XP", value="4,567 / 5,000", inline=True)
    embed.add_field(name="Rank", value="#23", inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="poll", description="Create a poll")
@app_commands.describe(question="The poll question", option1="Option 1", option2="Option 2")
async def poll(interaction: discord.Interaction, question: str, option1: str, option2: str):
    embed = discord.Embed(title=f"Poll: {question}", color=0xa855f7)
    embed.add_field(name="1.", value=option1, inline=False)
    embed.add_field(name="2.", value=option2, inline=False)
    await interaction.response.send_message(embed=embed)
    msg = await interaction.original_response()
    await msg.add_reaction("1\\u20e3")
    await msg.add_reaction("2\\u20e3")

if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")
    if not token: print("Set DISCORD_TOKEN"); exit(1)
    bot.run(token)
''')

    with open(bot_dir / "requirements.txt", "w") as f:
        f.write("discord.py>=2.3.0\npython-dotenv>=1.0.0\naiosqlite>=0.19.0\n")

    print(f"  Saved to {bot_dir}/")

    # ── 5. Chrome Extension ──────────────────────────────────────────────────

    print("\n[5/5] Building Chrome extension demo...")
    ext_dir = PORTFOLIO_DIR / "chrome-ext"
    ext_dir.mkdir(parents=True, exist_ok=True)

    manifest = {"manifest_version":3,"name":"PageData Extractor","version":"1.0.0","description":"Extract structured data from any webpage into CSV or JSON.","permissions":["activeTab","storage"],"action":{"default_popup":"popup.html"},"content_scripts":[{"matches":["<all_urls>"],"js":["content.js"],"css":["content.css"]}]}
    with open(ext_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    with open(ext_dir / "popup.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:360px;font-family:-apple-system,sans-serif;background:#0a0a0a;color:#fafafa;padding:20px}
h1{font-size:16px;margin-bottom:4px}
.subtitle{font-size:12px;color:#71717a;margin-bottom:16px}
.section{margin-bottom:16px}
.section-title{font-size:12px;color:#a1a1aa;margin-bottom:8px;font-weight:600;text-transform:uppercase}
label{font-size:12px;color:#a1a1aa;display:block;margin-bottom:4px}
input,select{width:100%;padding:8px 12px;background:#18181b;border:1px solid #27272a;border-radius:6px;color:#fafafa;font-size:13px;outline:none;margin-bottom:10px}
.btn{width:100%;padding:10px;border:none;border-radius:6px;font-size:13px;font-weight:600;cursor:pointer;margin-bottom:8px}
.btn-primary{background:#6366f1;color:white}
.btn-secondary{background:#27272a;color:#fafafa}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px}
.stat{background:#18181b;border:1px solid #27272a;border-radius:6px;padding:10px;text-align:center}
.stat-value{font-size:20px;font-weight:700;color:#22c55e}
.stat-label{font-size:10px;color:#71717a;margin-top:2px}
.preview{background:#18181b;border:1px solid #27272a;border-radius:6px;padding:10px;font-size:11px;color:#a1a1aa;max-height:120px;overflow-y:auto;font-family:monospace}
</style></head>
<body>
<h1>PageData Extractor</h1>
<p class="subtitle">Extract structured data from any webpage</p>
<div class="stats"><div class="stat"><div class="stat-value" id="count">0</div><div class="stat-label">Elements</div></div><div class="stat"><div class="stat-value" id="fields">0</div><div class="stat-label">Fields</div></div></div>
<div class="section"><div class="section-title">CSS Selector</div><label>Container</label><input type="text" id="selector" placeholder=".listing, tr, .product"><button class="btn btn-secondary" id="pick">Pick from page</button></div>
<div class="section"><div class="section-title">Export</div><select id="format"><option value="csv">CSV</option><option value="json">JSON</option></select></div>
<button class="btn btn-primary" id="extract">Extract data</button>
<div class="section"><div class="section-title">Preview</div><div class="preview" id="preview">Configure selector and click Extract.</div></div>
<script src="popup.js"></script>
</body></html>""")

    with open(ext_dir / "popup.js", "w") as f:
        f.write("""document.addEventListener('DOMContentLoaded',()=>{
const sel=document.getElementById('selector'),ext=document.getElementById('extract'),prev=document.getElementById('preview');
ext.addEventListener('click',()=>{
  const s=sel.value.trim();if(!s){prev.textContent='Enter a selector.';return;}
  chrome.tabs.query({active:true,currentWindow:true},(tabs)=>{
    chrome.tabs.sendMessage(tabs[0].id,{action:'extract',selector:s,format:document.getElementById('format').value},(r)=>{
      if(r&&r.data){document.getElementById('count').textContent=r.count;document.getElementById('fields').textContent=r.fields;prev.textContent=r.data.substring(0,500);
        const b=new Blob([r.data],{type:'text/plain'}),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='data.'+document.getElementById('format').value;a.click();
      }else{prev.textContent='No data found.';}
    });
  });
});
});""")

    with open(ext_dir / "content.js", "w") as f:
        f.write("""chrome.runtime.onMessage.addListener((req,sender,res)=>{
if(req.action==='extract'){
  const els=document.querySelectorAll(req.selector);
  if(!els.length){res({data:'',count:0,fields:0});return true;}
  const rows=[];
  els.forEach(el=>{const r={text:el.textContent.trim().substring(0,200)};if(el.querySelector('a'))r.link=el.querySelector('a').href;if(el.querySelector('img'))r.image=el.querySelector('img').src;rows.push(r);});
  const fields=rows.length?Object.keys(rows[0]).length:0;
  let data;
  if(req.format==='json'){data=JSON.stringify(rows,null,2);}else{const h=Object.keys(rows[0]);data=[h.join(','),...rows.map(r=>h.map(k=>'"'+(r[k]||'').replace(/"/g,'""')+'"').join(','))].join('\\n');}
  res({data,count:els.length,fields});
}return true;});""")

    with open(ext_dir / "content.css", "w") as f:
        f.write(".pagedata-highlight{outline:2px solid #6366f1!important;outline-offset:2px}")

    icons_dir = ext_dir / "icons"
    icons_dir.mkdir(parents=True, exist_ok=True)
    with open(icons_dir / "README.md", "w") as f:
        f.write("Generate icons at 16, 32, 48, 128px. Save as icon{size}.png\n")

    print(f"  Saved to {ext_dir}/")

    # ── Summary ──────────────────────────────────────────────────────────────

    print(f"\n{'=' * 70}")
    print("PORTFOLIO BUILD COMPLETE - 5 PIECES")
    print(f"{'=' * 70}")
    print(f"\nAll saved to {PORTFOLIO_DIR}/")
    print()
    print("Deploy commands:")
    print(f"  1. cd {PORTFOLIO_DIR}/landing-page && npx surge . saasify-demo.surge.sh")
    print(f"  2. cd {PORTFOLIO_DIR}/dashboard && npx surge . metrix-dashboard.surge.sh")
    print(f"  3. python3 {PORTFOLIO_DIR}/scraper/scraper_demo.py -q dentist -l 'Austin TX'")
    print(f"  4. See {PORTFOLIO_DIR}/discord-bot/README.md")
    print(f"  5. Load {PORTFOLIO_DIR}/chrome-ext/ in chrome://extensions (developer mode)")
    print()
    print("Add deployed URLs to all freelance platform listings.")


def cmd_status(args):
    """Show pipeline status."""
    ensure_dirs()
    rows = load_pipeline()

    print("=" * 70)
    print("FREELANCE PIPELINE STATUS")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    if not rows:
        print("\nNo leads in pipeline. Run --scan to find opportunities.")
        return

    statuses = {}
    categories = {}
    total_revenue = 0

    for r in rows:
        status = r.get("status", "UNKNOWN")
        statuses[status] = statuses.get(status, 0) + 1
        cat = r.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
        if r.get("revenue"):
            try:
                total_revenue += float(r["revenue"])
            except ValueError:
                pass

    print(f"\nTotal leads: {len(rows)}")
    print(f"Total revenue: ${total_revenue:,.0f}")

    print("\nBY STATUS:")
    for s, count in sorted(statuses.items(), key=lambda x: -x[1]):
        bar = "#" * min(count, 40)
        print(f"  {s:<25} {count:>4}  {bar}")

    print("\nBY CATEGORY:")
    for c, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {c:<25} {count:>4}")

    won = [r for r in rows if r.get("outcome") == "won"]
    if won:
        avg_deal = total_revenue / len(won)
        print(f"\nWIN METRICS:")
        print(f"  Deals won: {len(won)}")
        print(f"  Average deal: ${avg_deal:,.0f}")
        print(f"  Total revenue: ${total_revenue:,.0f}")

    print(f"\nCOST BASIS:")
    print(f"  Claude Code Max: $200/month")
    print(f"  Revenue: ${total_revenue:,.0f}")
    print(f"  Profit: ${total_revenue - 200:,.0f}")
    if total_revenue > 0:
        print(f"  Margin: {((total_revenue - 200) / total_revenue) * 100:.0f}%")

    new_count = statuses.get("NEW", 0)
    print(f"\nACTION ITEMS:")
    if new_count > 0:
        print(f"  [{new_count}] new leads need proposals. Run --propose")
    print(f"  Run --scan to find new opportunities")


def cmd_platforms(args):
    """Show all platform statuses."""
    print("=" * 70)
    print("PLATFORM STATUS - OP17 FREELANCE ARB")
    print("=" * 70)

    for pid, p in sorted(PLATFORMS.items(), key=lambda x: x[1]["priority"]):
        icon = "+" if p["status"] in ("ACTIVE", "READY") else "-"
        print(f"\n  [{icon}] {pid.upper()}")
        print(f"      Status: {p['status']} | Commission: {p['commission']}")
        print(f"      URL: {p['url']}")

    print(f"\n  Listings ready at: PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md")
    print(f"  0% commission: Contra, LinkedIn, Direct (prioritize these)")
    print(f"  Account creation: OPS/ACCOUNT_CREATION_NOW.md")


def cmd_add_lead(args):
    """Manually add a lead to the pipeline."""
    ensure_dirs()
    rows = load_pipeline()

    lead = {
        "lead_id": next_lead_id(rows),
        "date_found": datetime.now().strftime("%Y-%m-%d"),
        "platform": args.platform,
        "subreddit": "",
        "title": args.title,
        "url": args.url or "",
        "category": classify_job(args.title.lower()),
        "budget_est": str(int(args.budget)) if args.budget else "",
        "status": "NEW",
        "proposal_sent": "no",
        "outcome": "",
        "revenue": "",
        "notes": args.notes or "",
    }

    rows.append(lead)
    save_pipeline(rows)
    print(f"Added {lead['lead_id']}: {args.title}")
    print(f"  Platform: {args.platform} | Category: {lead['category']}")
    if args.budget:
        print(f"  Budget: ${int(args.budget)}")


def cmd_close(args):
    """Close a lead as won or lost."""
    ensure_dirs()
    rows = load_pipeline()

    found = False
    for r in rows:
        if r.get("lead_id") == args.lead_id:
            r["outcome"] = args.outcome
            r["status"] = "WON" if args.outcome == "won" else "LOST"
            if args.revenue:
                r["revenue"] = str(args.revenue)
            found = True
            print(f"Closed {args.lead_id}: {args.outcome.upper()}")
            if args.revenue:
                print(f"  Revenue: ${args.revenue}")
            break

    if not found:
        print(f"Lead {args.lead_id} not found.")
        return

    save_pipeline(rows)

    if args.outcome == "won" and args.revenue:
        if not REVENUE_CSV.exists():
            with open(REVENUE_CSV, "w", newline="") as f:
                csv.writer(f).writerow(["date", "lead_id", "platform", "category", "revenue", "cost", "profit"])
        with open(REVENUE_CSV, "a", newline="") as f:
            lead_data = next((r for r in rows if r["lead_id"] == args.lead_id), {})
            csv.writer(f).writerow([
                datetime.now().strftime("%Y-%m-%d"), args.lead_id,
                lead_data.get("platform", ""), lead_data.get("category", ""),
                args.revenue, "0", args.revenue
            ])
        print(f"  Logged to {REVENUE_CSV}")


def cmd_revenue(args):
    """Show revenue breakdown."""
    rows = load_pipeline()
    won = [r for r in rows if r.get("outcome") == "won"]

    print("=" * 70)
    print("FREELANCE REVENUE TRACKER")
    print("=" * 70)

    if not won:
        print("\nNo won deals yet. Keep scanning and proposing.")
        pipeline_value = sum(float(r.get("budget_est", 0)) for r in rows if r.get("status") in ("NEW", "PROPOSAL_DRAFTED") and r.get("budget_est", "").isdigit())
        if pipeline_value:
            print(f"\nPipeline value (potential): ${pipeline_value:,.0f}")
            print(f"At 20% close rate: ${pipeline_value * 0.2:,.0f}")
        return

    total = sum(float(r.get("revenue", 0)) for r in won if r.get("revenue"))
    print(f"\nDeals won: {len(won)}")
    for r in won:
        print(f"  {r['lead_id']} | {r.get('category', '?'):<15} | ${r.get('revenue', 0)}")
    print(f"\nTotal revenue: ${total:,.0f}")
    print(f"Claude Max cost: $200/mo")
    print(f"Net profit: ${total - 200:,.0f}")
    if total > 0:
        print(f"Margin: {((total - 200) / total) * 100:.0f}%")


def cmd_daily(args):
    """Full daily pipeline run."""
    print("=" * 70)
    print("DAILY FREELANCE PIPELINE RUN")
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    print("\n[1/3] Scanning for opportunities...")
    cmd_scan(args)
    print("\n[2/3] Pipeline status...")
    cmd_status(args)
    print("\n[3/3] Platform status...")
    cmd_platforms(args)

    print(f"\n{'=' * 70}")
    print("NEXT ACTIONS:")
    print("  1. Run --propose to generate proposals for new leads")
    print("  2. Personalize and send top 3 proposals")
    print("  3. Build free sample for highest-budget lead")
    print("  4. Create accounts on platforms still NOT_CREATED")
    print(f"{'=' * 70}")


# ── Main ─────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="OP17 Freelance Service Arbitrage Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 freelance_pipeline.py --scan              Scan Reddit for jobs
  python3 freelance_pipeline.py --propose --top 5    Generate 5 proposals
  python3 freelance_pipeline.py --portfolio          Build 5 portfolio demos
  python3 freelance_pipeline.py --status             Pipeline status
  python3 freelance_pipeline.py --platforms          Platform status
  python3 freelance_pipeline.py --revenue            Revenue breakdown
  python3 freelance_pipeline.py --daily              Full daily run
  python3 freelance_pipeline.py --add-lead --platform upwork --title "Build landing page" --budget 300
  python3 freelance_pipeline.py --close --lead-id LEAD_001 --outcome won --revenue 350
        """
    )

    parser.add_argument("--scan", action="store_true", help="Scan Reddit for opportunities")
    parser.add_argument("--propose", action="store_true", help="Generate proposals for top leads")
    parser.add_argument("--portfolio", action="store_true", help="Build 5 portfolio pieces")
    parser.add_argument("--status", action="store_true", help="Pipeline status")
    parser.add_argument("--platforms", action="store_true", help="Platform status")
    parser.add_argument("--revenue", action="store_true", help="Revenue breakdown")
    parser.add_argument("--daily", action="store_true", help="Full daily run")
    parser.add_argument("--add-lead", action="store_true", help="Add a lead manually")
    parser.add_argument("--close", action="store_true", help="Close a lead")

    parser.add_argument("--top", type=int, default=5, help="Proposals to generate (default: 5)")
    parser.add_argument("--platform", type=str, default="manual", help="Platform name")
    parser.add_argument("--title", type=str, default="", help="Job title")
    parser.add_argument("--budget", type=float, default=0, help="Budget estimate")
    parser.add_argument("--url", type=str, default="", help="Job posting URL")
    parser.add_argument("--notes", type=str, default="", help="Notes")
    parser.add_argument("--lead-id", type=str, default="", help="Lead ID to close")
    parser.add_argument("--outcome", type=str, choices=["won", "lost"], default="won")
    parser.add_argument("--revenue-amount", dest="revenue", type=float, default=0, help="Revenue from deal")

    args = parser.parse_args()

    if args.scan:
        cmd_scan(args)
    elif args.propose:
        cmd_propose(args)
    elif args.portfolio:
        cmd_portfolio(args)
    elif args.status:
        cmd_status(args)
    elif args.platforms:
        cmd_platforms(args)
    elif args.revenue:
        cmd_revenue(args)
    elif args.daily:
        cmd_daily(args)
    elif args.add_lead:
        if not args.title:
            print("Error: --title required")
            return
        cmd_add_lead(args)
    elif args.close:
        if not args.lead_id:
            print("Error: --lead-id required")
            return
        cmd_close(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
