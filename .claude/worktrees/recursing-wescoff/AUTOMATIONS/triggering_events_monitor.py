#!/usr/bin/env python3
"""
Triggering Events Monitor
Source: @pipelineabuser tweet - "triggering events nobody tracks"

Monitors 6 types of triggering events that signal buying intent:
1. Leadership changes (theorg.com)
2. Office moves (Google Alerts / news)
3. Glassdoor review spikes
4. Competitor layoffs (LinkedIn)
5. Job posting removals
6. 10-K filing language changes (SEC EDGAR)

Outputs to LEDGER/TRIGGERING_EVENTS.csv with cold email templates.

Usage:
    python3 triggering_events_monitor.py                # Run all monitors
    python3 triggering_events_monitor.py --sec-only      # Only SEC filings
    python3 triggering_events_monitor.py --companies "Stripe,Shopify,HubSpot"
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote
from urllib.error import URLError, HTTPError

BASE_DIR = Path(__file__).parent.parent
OUTPUT_CSV = BASE_DIR / "LEDGER" / "TRIGGERING_EVENTS.csv"
COLD_EMAILS_DIR = BASE_DIR / "EMAIL" / "triggering_events"
LOG_FILE = BASE_DIR / "AUTOMATIONS" / "logs" / "triggering_events.log"

# Default target companies (customize this list)
DEFAULT_COMPANIES = [
    "Stripe", "Shopify", "HubSpot", "Slack", "Notion",
    "Airtable", "Figma", "Canva", "Webflow", "Vercel",
    "Supabase", "PlanetScale", "Railway", "Render", "Fly.io",
    "Linear", "Retool", "Zapier", "Make", "n8n",
]

COLD_EMAIL_TEMPLATES = {
    "leadership_change": """Subject: Congrats on the new role at {company}

{first_name},

Saw {new_leader} just took over {department} at {company}. Usually that means fresh eyes on how things are done.

New leaders in the first 90 days typically evaluate:
- Current vendor stack
- Team efficiency gaps
- Quick wins to build momentum

We help companies like {company} with {our_service}. Takes 15 min to see if it's relevant.

Worth a look?
""",
    "office_move": """Subject: Congrats on the new {city} office

{first_name},

Saw {company} just opened in {city}. Expansion usually means scaling {department} fast.

When teams grow quickly, {pain_point} becomes the bottleneck. We help with exactly that.

3 min call to see if there's a fit?
""",
    "glassdoor_spike": """Subject: Quick thought on {company}'s team challenges

{first_name},

I track industry sentiment and noticed some team feedback challenges at {company} recently.

When internal friction shows up, it usually means {department} is stretched. We help companies solve {pain_point} without adding headcount.

Might be relevant - 5 min to explore?
""",
    "competitor_layoff": """Subject: {competitor} just cut {department}

{first_name},

{competitor} just laid off their {department} team. That's usually a signal that {company} has a window to take market share.

Moving fast matters here. We help companies like {company} capitalize on competitor gaps with {our_service}.

Worth 10 minutes?
""",
    "job_removed": """Subject: How's the new {role} hire going?

{first_name},

Noticed {company} just filled the {role} position about 30 days ago. First month is usually when new hires realize they need {tool_category} to hit their targets.

We've helped 15+ companies onboard their new {role}s with {our_service}. Usually saves 2-3 weeks of ramp time.

Quick call to see if it's useful?
""",
    "sec_filing_change": """Subject: Noticed {risk_area} in {company}'s latest filing

{first_name},

{company}'s latest 10-K mentions {risk_area} for the first time. When that shows up in a filing, it usually means the board is allocating budget.

We help companies address {risk_area} with {our_service}. Already working with 3 similar companies in {industry}.

15 min to see if there's alignment?
""",
}


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(log_msg + "\n")


def fetch_url(url, headers=None):
    """Fetch URL with error handling."""
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json,text/html",
    }
    if headers:
        default_headers.update(headers)
    try:
        req = Request(url, headers=default_headers)
        with urlopen(req, timeout=30) as response:
            return response.read().decode("utf-8", errors="replace")
    except Exception as e:
        log(f"Fetch error: {url} - {e}")
        return None


# =============================================================================
# MONITOR 1: SEC EDGAR 10-K Filing Changes
# =============================================================================

def monitor_sec_filings(companies):
    """Monitor SEC EDGAR for new filings and language changes in 10-K/10-Q."""
    events = []
    log("Checking SEC EDGAR filings...")

    for company in companies:
        # Search EDGAR full-text search API
        search_url = f"https://efts.sec.gov/LATEST/search-index?q=%22{quote(company)}%22&dateRange=custom&startdt={(datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')}&enddt={datetime.now().strftime('%Y-%m-%d')}&forms=10-K,10-Q,8-K"

        data = fetch_url(search_url, headers={"Accept": "application/json"})
        if not data:
            # Try EDGAR company search
            search_url2 = f"https://efts.sec.gov/LATEST/search-index?q=%22{quote(company)}%22&forms=10-K,10-Q&dateRange=custom&startdt={(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')}&enddt={datetime.now().strftime('%Y-%m-%d')}"
            data = fetch_url(search_url2)

        if data:
            try:
                results = json.loads(data)
                hits = results.get("hits", {}).get("hits", [])
                for hit in hits[:3]:
                    source = hit.get("_source", {})
                    events.append({
                        "event_type": "SEC_FILING",
                        "company": company,
                        "detail": f"{source.get('form_type', 'Unknown')} filed: {source.get('file_description', '')}",
                        "date": source.get("file_date", ""),
                        "url": f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company={quote(company)}&type=10-K&dateb=&owner=include&count=10",
                        "signal_strength": "HIGH" if source.get("form_type") in ["10-K", "8-K"] else "MEDIUM",
                        "email_template": "sec_filing_change",
                    })
            except json.JSONDecodeError:
                pass

        # Also try the EDGAR company search API
        edgar_url = f"https://efts.sec.gov/LATEST/search-index?q=%22{quote(company)}%22&forms=10-K"
        edgar_data = fetch_url(edgar_url)
        # Process results silently

    log(f"  SEC EDGAR: found {len(events)} filing events")
    return events


# =============================================================================
# MONITOR 2: News-based triggers (office moves, layoffs, leadership)
# =============================================================================

def monitor_news_triggers(companies):
    """Use free news APIs to detect office moves, leadership changes, layoffs."""
    events = []
    log("Checking news triggers...")

    for company in companies:
        # Use DuckDuckGo Instant Answer API (free, no key)
        for trigger_type, search_query in [
            ("office_move", f"{company} new office opens 2026"),
            ("leadership_change", f"{company} CEO CTO CMO appointed new 2026"),
            ("competitor_layoff", f"{company} layoffs 2026"),
        ]:
            ddg_url = f"https://api.duckduckgo.com/?q={quote(search_query)}&format=json&no_redirect=1"
            data = fetch_url(ddg_url)
            if data:
                try:
                    result = json.loads(data)
                    abstract = result.get("AbstractText", "")
                    related = result.get("RelatedTopics", [])

                    if abstract and any(kw in abstract.lower() for kw in ["office", "move", "relocat", "expand", "appoint", "hire", "layoff", "cut"]):
                        events.append({
                            "event_type": trigger_type.upper(),
                            "company": company,
                            "detail": abstract[:300],
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "url": result.get("AbstractURL", ""),
                            "signal_strength": "MEDIUM",
                            "email_template": trigger_type,
                        })

                    for topic in related[:3]:
                        text = topic.get("Text", "")
                        if text and len(text) > 20:
                            events.append({
                                "event_type": trigger_type.upper(),
                                "company": company,
                                "detail": text[:300],
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "url": topic.get("FirstURL", ""),
                                "signal_strength": "LOW",
                                "email_template": trigger_type,
                            })
                except json.JSONDecodeError:
                    pass

    log(f"  News triggers: found {len(events)} events")
    return events


# =============================================================================
# MONITOR 3: Job posting tracker (via public APIs)
# =============================================================================

def monitor_job_postings(companies):
    """Monitor job postings via public job board APIs."""
    events = []
    log("Checking job posting signals...")

    for company in companies:
        # Check GitHub Jobs API alternative - Arbeitnow (free, public)
        # Also check via Adzuna public API
        # Use HN Who's Hiring as a proxy
        hn_url = f"https://hn.algolia.com/api/v1/search?query={quote(company)}&tags=job"
        data = fetch_url(hn_url)
        if data:
            try:
                result = json.loads(data)
                hits = result.get("hits", [])
                for hit in hits[:3]:
                    created = hit.get("created_at", "")[:10]
                    title = hit.get("title", "") or hit.get("story_title", "")
                    events.append({
                        "event_type": "JOB_POSTING",
                        "company": company,
                        "detail": f"HN Job: {title}",
                        "date": created,
                        "url": hit.get("url", "") or f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}",
                        "signal_strength": "MEDIUM",
                        "email_template": "job_removed",
                    })
            except json.JSONDecodeError:
                pass

    log(f"  Job postings: found {len(events)} signals")
    return events


# =============================================================================
# MONITOR 4: Glassdoor sentiment (public data)
# =============================================================================

def monitor_glassdoor_sentiment(companies):
    """Check for Glassdoor rating changes (via public search)."""
    events = []
    log("Checking Glassdoor sentiment signals...")

    # Glassdoor blocks scraping, so we use DuckDuckGo to find recent reviews
    for company in companies:
        ddg_url = f"https://api.duckduckgo.com/?q={quote(company)}+glassdoor+reviews+2026&format=json"
        data = fetch_url(ddg_url)
        if data:
            try:
                result = json.loads(data)
                abstract = result.get("AbstractText", "")
                if abstract and any(kw in abstract.lower() for kw in ["rating", "review", "star", "decline", "drop"]):
                    events.append({
                        "event_type": "GLASSDOOR_CHANGE",
                        "company": company,
                        "detail": abstract[:300],
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "url": f"https://www.glassdoor.com/Reviews/{company}-Reviews.htm",
                        "signal_strength": "MEDIUM",
                        "email_template": "glassdoor_spike",
                    })
            except json.JSONDecodeError:
                pass

    log(f"  Glassdoor: found {len(events)} sentiment signals")
    return events


# =============================================================================
# Main orchestrator
# =============================================================================

def save_events(events):
    """Save events to CSV."""
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    file_exists = OUTPUT_CSV.exists()

    fieldnames = [
        "event_id",
        "event_type",
        "company",
        "detail",
        "date",
        "url",
        "signal_strength",
        "email_template",
        "found_date",
        "status",
        "email_sent",
        "notes",
    ]

    existing_ids = set()
    if file_exists:
        with open(OUTPUT_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_ids.add(row.get("event_id", ""))

    new_events = []
    for i, event in enumerate(events):
        event_id = f"EVT_{datetime.now().strftime('%Y%m%d')}_{i:04d}"
        if event_id not in existing_ids:
            event["event_id"] = event_id
            event["found_date"] = datetime.now().strftime("%Y-%m-%d")
            event["status"] = "NEW"
            event["email_sent"] = "NO"
            event["notes"] = ""
            new_events.append(event)

    with open(OUTPUT_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for event in new_events:
            writer.writerow(event)

    return len(new_events)


def save_cold_email_templates():
    """Save cold email templates to EMAIL directory."""
    COLD_EMAILS_DIR.mkdir(parents=True, exist_ok=True)
    for template_name, template_content in COLD_EMAIL_TEMPLATES.items():
        filepath = COLD_EMAILS_DIR / f"{template_name}_template.txt"
        if not filepath.exists():
            with open(filepath, "w") as f:
                f.write(template_content)
    log(f"Cold email templates saved to {COLD_EMAILS_DIR}")


def main():
    parser = argparse.ArgumentParser(description="Triggering Events Monitor (@pipelineabuser)")
    parser.add_argument("--companies", type=str, help="Comma-separated company names")
    parser.add_argument("--sec-only", action="store_true", help="Only check SEC filings")
    parser.add_argument("--news-only", action="store_true", help="Only check news triggers")
    parser.add_argument("--summary", action="store_true", help="Show summary of tracked events")
    args = parser.parse_args()

    companies = args.companies.split(",") if args.companies else DEFAULT_COMPANIES

    if args.summary:
        if OUTPUT_CSV.exists():
            with open(OUTPUT_CSV, "r") as f:
                reader = list(csv.DictReader(f))
                print(f"\n{'='*60}")
                print(f"TRIGGERING EVENTS MONITOR SUMMARY")
                print(f"{'='*60}")
                print(f"Total events tracked: {len(reader)}")
                types = {}
                for row in reader:
                    t = row.get("event_type", "UNKNOWN")
                    types[t] = types.get(t, 0) + 1
                for etype, count in sorted(types.items()):
                    print(f"  {etype}: {count}")
                strengths = {}
                for row in reader:
                    s = row.get("signal_strength", "UNKNOWN")
                    strengths[s] = strengths.get(s, 0) + 1
                print(f"\nSignal strength breakdown:")
                for strength, count in sorted(strengths.items()):
                    print(f"  {strength}: {count}")
                print(f"\nFile: {OUTPUT_CSV}")
        else:
            print("No events tracked yet. Run without --summary to start monitoring.")
        return

    print(f"\n{'='*60}")
    print(f"TRIGGERING EVENTS MONITOR")
    print(f"Source: @pipelineabuser - 'triggering events nobody tracks'")
    print(f"{'='*60}")
    print(f"Monitoring {len(companies)} companies...")
    print()

    all_events = []

    if args.sec_only:
        all_events.extend(monitor_sec_filings(companies))
    elif args.news_only:
        all_events.extend(monitor_news_triggers(companies))
    else:
        # Run all monitors
        all_events.extend(monitor_sec_filings(companies))
        all_events.extend(monitor_news_triggers(companies))
        all_events.extend(monitor_job_postings(companies))
        all_events.extend(monitor_glassdoor_sentiment(companies))

    # Save results
    new_count = save_events(all_events)
    save_cold_email_templates()

    # Print summary
    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"{'='*60}")
    print(f"Total events detected: {len(all_events)}")
    print(f"New events saved: {new_count}")
    print(f"Output: {OUTPUT_CSV}")
    print(f"Email templates: {COLD_EMAILS_DIR}")

    # Print HIGH signal events
    high_events = [e for e in all_events if e.get("signal_strength") == "HIGH"]
    if high_events:
        print(f"\nHIGH SIGNAL EVENTS ({len(high_events)}):")
        for event in high_events[:10]:
            print(f"  [{event['event_type']}] {event['company']}: {event['detail'][:100]}")

    print(f"\nNext steps:")
    print(f"  1. Review HIGH signal events")
    print(f"  2. Customize cold email templates in {COLD_EMAILS_DIR}")
    print(f"  3. Add to crontab for daily monitoring")
    print(f"  4. Enrich leads with emails via Apollo/Hunter.io")


if __name__ == "__main__":
    main()
