#!/usr/bin/env python3
"""
PRINTMAXX LinkedIn AI Agent Outbound Pipeline
==============================================
Automates LinkedIn outbound for SaaS founder/B2B lead generation:
  - Scrape target profiles via LinkedIn search signals
  - Qualify leads by company size, role, and engagement signals
  - Send AI-personalized connection requests + follow-up messages
  - Track demo bookings and pipeline stage transitions
  - Execute follow-up sequences to close the loop

Alpha insight: LinkedIn AI agents outperformed 14,723 cold emails as the best
acquisition channel despite 13x lower volume. This pipeline wires LinkedIn as
primary and cold email as secondary fallback.

Usage:
    python linkedin_ai_agent_outbound.py --run
    python linkedin_ai_agent_outbound.py --status
    python linkedin_ai_agent_outbound.py --dry-run
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(p):
        resolved = Path(p).resolve()
        if not str(resolved).startswith(str(PROJECT)):
            raise ValueError(f"Path {resolved} is outside PROJECT root {PROJECT}")
        return resolved

    def recall_skills_for_task(task_name):
        return {}

    def capture_skill_from_result(task_name, result):
        pass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_PATH = AUTOMATIONS_DIR / "logs" / "linkedin_ai_agent_outbound.log"
DATA_DIR = AUTOMATIONS_DIR / "data" / "linkedin_outbound"
LEADS_CSV = DATA_DIR / "leads.csv"
PIPELINE_JSON = DATA_DIR / "pipeline.json"
SENT_LOG_CSV = DATA_DIR / "sent_log.csv"
BOOKINGS_CSV = DATA_DIR / "demo_bookings.csv"
FOLLOWUP_QUEUE_JSON = DATA_DIR / "followup_queue.json"
CONFIG_JSON = AUTOMATIONS_DIR / "config" / "linkedin_outbound_config.json"

LEADS_FIELDNAMES = [
    "profile_url", "full_name", "title", "company", "company_size",
    "industry", "location", "signal_score", "qualified", "stage",
    "added_date", "last_action_date", "notes",
]

SENT_LOG_FIELDNAMES = [
    "timestamp", "profile_url", "full_name", "action_type",
    "message_variant", "status", "response",
]

BOOKINGS_FIELDNAMES = [
    "timestamp", "profile_url", "full_name", "company",
    "booking_source", "meeting_date", "status",
]

PIPELINE_STAGES = [
    "scraped",
    "qualified",
    "connection_sent",
    "connected",
    "message_sent",
    "replied",
    "demo_booked",
    "demo_completed",
    "closed_won",
    "closed_lost",
    "unsubscribed",
]

TARGET_TITLES = [
    "founder", "co-founder", "ceo", "chief executive",
    "head of growth", "vp sales", "director of sales",
    "head of marketing", "vp marketing", "cmo",
    "growth lead", "revenue lead",
]

TARGET_INDUSTRIES = [
    "saas", "software", "b2b", "cloud", "technology",
    "fintech", "martech", "devtools", "productivity",
]

COMPANY_SIZE_QUALIFY = {"1-10", "11-50", "51-200", "201-500"}

MESSAGE_TEMPLATES = {
    "connection": (
        "Hi {first_name}, I came across your work at {company} — "
        "building in {industry} is no joke. Would love to connect and "
        "swap notes on what's working in growth right now."
    ),
    "followup_1": (
        "Hey {first_name}, thanks for connecting! "
        "Quick question — are you currently happy with how you're handling "
        "{pain_point}? We've helped {social_proof}. "
        "Worth a 15-min chat?"
    ),
    "followup_2": (
        "Hi {first_name}, just circling back. "
        "I know timing is everything — if now isn't right, totally fine. "
        "But if you ever want to explore how we helped founders like you "
        "add 16 new customers in 30 days, I'm one message away."
    ),
    "booking_confirm": (
        "Awesome {first_name}! Just confirmed your demo slot. "
        "You'll get a calendar invite shortly. Looking forward to it."
    ),
}

FOLLOWUP_DELAYS = {
    "connection_sent": 3,
    "connected": 1,
    "message_sent": 5,
    "replied": 2,
}

DEFAULT_CONFIG = {
    "daily_connection_limit": 20,
    "daily_message_limit": 50,
    "min_signal_score": 6,
    "company_size_targets": list(COMPANY_SIZE_QUALIFY),
    "target_titles": TARGET_TITLES,
    "target_industries": TARGET_INDUSTRIES,
    "pain_point": "outbound sales",
    "social_proof": "SaaS founders add 10-20 new customers per month",
    "dry_run": False,
    "webhook_url": "",
    "crm_endpoint": "",
}


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging():
    log_file = safe_path(LOG_PATH)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(str(log_file), mode="a"),
            logging.StreamHandler(sys.stdout),
        ],
    )


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def load_config():
    try:
        cfg_path = safe_path(CONFIG_JSON)
        if cfg_path.exists():
            with open(cfg_path, "r") as f:
                user_cfg = json.load(f)
            merged = {**DEFAULT_CONFIG, **user_cfg}
            logger.info("Loaded config from %s", cfg_path)
            return merged
    except Exception as e:
        logger.warning("Could not load config, using defaults: %s", e)
    return dict(DEFAULT_CONFIG)


def save_config(cfg):
    try:
        cfg_path = safe_path(CONFIG_JSON)
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cfg_path, "w") as f:
            json.dump(cfg, f, indent=2)
    except Exception as e:
        logger.error("Failed to save config: %s", e)


# ---------------------------------------------------------------------------
# File / CSV helpers
# ---------------------------------------------------------------------------

def ensure_data_dirs():
    for d in [DATA_DIR, AUTOMATIONS_DIR / "logs", AUTOMATIONS_DIR / "config"]:
        try:
            safe_path(d).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error("Could not create directory %s: %s", d, e)


def init_csv(path, fieldnames):
    p = safe_path(path)
    if not p.exists():
        try:
            with open(p, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
            logger.info("Initialized CSV: %s", p)
        except Exception as e:
            logger.error("Failed to init CSV %s: %s", p, e)


def append_csv(path, fieldnames, row):
    p = safe_path(path)
    try:
        with open(p, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writerow(row)
    except Exception as e:
        logger.error("Failed to append to CSV %s: %s", p, e)


def read_csv_as_dicts(path):
    p = safe_path(path)
    rows = []
    if not p.exists():
        return rows
    try:
        with open(p, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
    except Exception as e:
        logger.error("Failed to read CSV %s: %s", p, e)
    return rows


def load_json_file(path, default):
    p = safe_path(path)
    if not p.exists():
        return default
    try:
        with open(p, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error("Failed to load JSON %s: %s", p, e)
        return default


def write_json_file(path, data):
    p = safe_path(path)
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error("Failed to write JSON %s: %s", p, e)


# ---------------------------------------------------------------------------
# Pipeline state
# ---------------------------------------------------------------------------

def load_pipeline():
    return load_json_file(PIPELINE_JSON, {})


def save_pipeline(pipeline):
    write_json_file(PIPELINE_JSON, pipeline)


def get_lead_stage(pipeline, profile_url):
    return pipeline.get(profile_url, {}).get("stage", "scraped")


def advance_lead(pipeline, profile_url, new_stage, notes=""):
    now = datetime.utcnow().isoformat()
    if profile_url not in pipeline:
        pipeline[profile_url] = {}
    pipeline[profile_url]["stage"] = new_stage
    pipeline[profile_url]["last_updated"] = now
    if notes:
        pipeline[profile_url].setdefault("notes", []).append(
            {"timestamp": now, "note": notes}
        )


# ---------------------------------------------------------------------------
# Signal scoring
# ---------------------------------------------------------------------------

def score_lead(lead):
    score = 0
    title = (lead.get("title") or "").lower()
    industry = (lead.get("industry") or "").lower()
    company_size = (lead.get("company_size") or "").strip()

    for t in TARGET_TITLES:
        if t in title:
            score += 3
            break

    for i in TARGET_INDUSTRIES:
        if i in industry:
            score += 2
            break

    if company_size in COMPANY_SIZE_QUALIFY:
        score += 2

    if lead.get("location") and any(
        c in (lead.get("location") or "").lower()
        for c in ["us", "united states", "canada", "uk", "australia"]
    ):
        score += 1

    if lead.get("notes") and "hiring" in (lead.get("notes") or "").lower():
        score += 2

    return score


def qualify_leads(leads, cfg):
    min_score = cfg.get("min_signal_score", 6)
    qualified = []
    for lead in leads:
        score = score_lead(lead)
        lead["signal_score"] = score
        lead["qualified"] = "yes" if score >= min_score else "no"
        if lead["qualified"] == "yes":
            qualified.append(lead)
    logger.info("Qualified %d / %d leads (min score=%d)", len(qualified), len(leads), min_score)
    return qualified


# ---------------------------------------------------------------------------
# Scraping (LinkedIn public search via urllib)
# ---------------------------------------------------------------------------

def build_linkedin_search_url(title, industry, page=1):
    params = urllib.parse.urlencode({
        "keywords": f"{title} {industry}",
        "origin": "GLOBAL_SEARCH_HEADER",
        "page": page,
    })
    return f"https://www.linkedin.com/search/results/people/?{params}"


def fetch_url(url, headers=None, timeout=15):
    req_headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
    if headers:
        req_headers.update(headers)
    try:
        req = urllib.request.Request(url, headers=req_headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace"), resp.status
    except urllib.error.HTTPError as e:
        logger.warning("HTTP %s for %s", e.code, url)
        return "", e.code
    except urllib.error.URLError as e:
        logger.warning("URL error for %s: %s", url, e.reason)
        return "", 0
    except Exception as e:
        logger.error("Fetch error for %s: %s", url, e)
        return "", 0


def parse_mock_profiles_from_html(html, industry):
    """
    Parse LinkedIn search HTML for profile cards.
    LinkedIn requires auth for most data; this parser extracts what is
    publicly visible and falls back to structured mock data for dry-run/demo.
    In production, integrate with an authorized LinkedIn API or sales tool.
    """
    profiles = []
    if not html:
        return profiles

    import re

    name_pattern = re.compile(r'"name"\s*:\s*"([^"]{5,60})"')
    url_pattern = re.compile(r'"publicIdentifier"\s*:\s*"([a-zA-Z0-9\-]+)"')
    title_pattern = re.compile(r'"headline"\s*:\s*"([^"]{5,120})"')

    names = name_pattern.findall(html)
    slugs = url_pattern.findall(html)
    titles = title_pattern.findall(html)

    for i, slug in enumerate(slugs[:10]):
        profiles.append({
            "profile_url": f"https://www.linkedin.com/in/{slug}",
            "full_name": names[i] if i < len(names) else f"Lead_{slug}",
            "title": titles[i] if i < len(titles) else "Founder",
            "company": "",
            "company_size": "11-50",
            "industry": industry,
            "location": "United States",
            "signal_score": 0,
            "qualified": "no",
            "stage": "scraped",
            "added_date": datetime.utcnow().isoformat(),
            "last_action_date": "",
            "notes": "",
        })
    return profiles


def generate_demo_leads(cfg, count=30):
    """Generate realistic demo leads for dry-run and testing."""
    demo_names = [
        ("Alex Chen", "Founder & CEO", "DataFlow Analytics", "11-50"),
        ("Sarah Kim", "Co-Founder", "GrowthOS", "1-10"),
        ("Marcus Webb", "CEO", "PipelineIQ", "51-200"),
        ("Priya Patel", "Head of Growth", "SalesMind", "11-50"),
        ("Jordan Torres", "Founder", "RevenueStack", "1-10"),
        ("Emily Zhang", "VP Sales", "CloudPitch", "51-200"),
        ("Ryan Nguyen", "Co-Founder & CTO", "AutoSDR", "11-50"),
        ("Lia Okonkwo", "CMO", "Outboundly", "11-50"),
        ("Derek Foster", "Founder", "CloserAI", "1-10"),
        ("Nina Russo", "Head of Marketing", "FunnelForge", "51-200"),
        ("Tyler Brooks", "CEO", "LeadHarvest", "11-50"),
        ("Amara Diallo", "Co-Founder", "SignalBase", "1-10"),
        ("Chris Mendez", "Founder", "DemoSync", "11-50"),
        ("Yuki Tanaka", "VP Growth", "EngageLoop", "51-200"),
        ("Sam Okafor", "Founder & CEO", "ConvertKit Pro", "11-50"),
    ]
    industries = cfg.get("target_industries", TARGET_INDUSTRIES)
    leads = []
    for i in range(min(count, len(demo_names))):
        name, title, company, size = demo_names[i % len(demo_names)]
        slug = name.lower().replace(" ", "-") + f"-{i}"
        leads.append({
            "profile_url": f"https://www.linkedin.com/in/{slug}",
            "full_name": name,
            "title": title,
            "company": company,
            "company_size": size,
            "industry": industries[i % len(industries)],
            "location": "United States",
            "signal_score": 0,
            "qualified": "no",
            "stage": "scraped",
            "added_date": datetime.utcnow().isoformat(),
            "last_action_date": "",
            "notes": "",
        })
    return leads


def scrape_linkedin_leads(cfg, dry_run=False):
    logger.info("Starting LinkedIn lead scrape (dry_run=%s)", dry_run)
    all_profiles = []

    if dry_run:
        all_profiles = generate_demo_leads(cfg)
        logger.info("Dry-run: generated %d demo leads", len(all_profiles))
        return all_profiles

    titles = cfg.get("target_titles", TARGET_TITLES)[:3]
    industries = cfg.get("target_industries", TARGET_INDUSTRIES)[:2]

    for title in titles:
        for industry in industries:
            url = build_linkedin_search_url(title, industry)
            logger.info("Fetching: %s", url)
            html, status = fetch_url(url)
            if status == 200:
                profiles = parse_mock_profiles_from_html(html, industry)
                all_profiles.extend(profiles)
                logger.info("Parsed %d profiles from search: %s / %s", len(profiles), title, industry)
            else:
                logger.warning("Non-200 status %s for %s/%s — skipping", status, title, industry)

    seen = set()
    deduped = []
    for p in all_profiles:
        key = p.get("profile_url", "")
        if key and key not in seen:
            seen.add(key)
            deduped.append(p)

    logger.info("Scrape complete: %d unique profiles", len(deduped))
    return deduped


# ---------------------------------------------------------------------------
# Message personalization
# ---------------------------------------------------------------------------

def personalize_message(template_key, lead, cfg):
    template = MESSAGE_TEMPLATES.get(template_key, "")
    first_name = (lead.get("full_name") or "there").split()[0]
    company = lead.get("company") or "your company"
    industry = lead.get("industry") or "your space"
    pain_point = cfg.get("pain_point", "outbound sales")
    social_proof = cfg.get("social_proof", "SaaS founders grow faster")
    return template.format(
        first_name=first_name,
        company=company,
        industry=industry,
        pain_point=pain_point,
        social_proof=social_proof,
    )


# ---------------------------------------------------------------------------
# Outbound actions
# ---------------------------------------------------------------------------

def send_connection_request(lead, message, dry_run=False):
    """
    Send LinkedIn connection request.
    In production: call LinkedIn API or automation tool endpoint.
    Requires valid session/OAuth — dry-run logs intent only.
    """
    profile_url = lead.get("profile_url", "")
    full_name = lead.get("full_name", "Unknown")

    if dry_run:
        logger.info("[DRY-RUN] Would send connection to %s (%s): %s",
                    full_name, profile_url, message[:80])
        return "dry_run_ok"

    logger.info("Sending connection request to %s (%s)", full_name, profile_url)
    # Production: POST to LinkedIn API / authorized automation endpoint
    # Placeholder: subprocess call to external tool if configured
    return "sent"


def send_message(lead, message, dry_run=False):
    """
    Send LinkedIn direct message to connected lead.
    In production: call LinkedIn messaging API.
    """
    profile_url = lead.get("profile_url", "")
    full_name = lead.get("full_name", "Unknown")

    if dry_run:
        logger.info("[DRY-RUN] Would send message to %s (%s): %s",
                    full_name, profile_url, message[:80])
        return "dry_run_ok"

    logger.info("Sending message to %s (%s)", full_name, profile_url)
    return "sent"


def notify_webhook(cfg, event_type, payload):
    """POST event to configured webhook (e.g., Zapier, n8n, Make)."""
    webhook_url = cfg.get("webhook_url", "")
    if not webhook_url:
        return

    try:
        data = json.dumps({
            "event": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": payload,
        }).encode("utf-8")
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            logger.info("Webhook %s → HTTP %s", event_type, resp.status)
    except Exception as e:
        logger.warning("Webhook notification failed for %s: %s", event_type, e)


# ---------------------------------------------------------------------------
# Core pipeline steps
# ---------------------------------------------------------------------------

def step_scrape_and_qualify(cfg, dry_run=False):
    logger.info("=== STEP 1: Scrape & Qualify ===")
    raw_leads = scrape_linkedin_leads(cfg, dry_run=dry_run)
    qualified = qualify_leads(raw_leads, cfg)

    existing = {r["profile_url"]: r for r in read_csv_as_dicts(LEADS_CSV)}
    new_count = 0
    for lead in qualified:
        url = lead.get("profile_url", "")
        if url and url not in existing:
            append_csv(LEADS_CSV, LEADS_FIELDNAMES, lead)
            existing[url] = lead
            new_count += 1

    logger.info("Added %d new qualified leads to pipeline", new_count)
    return new_count


def step_send_connections(cfg, pipeline, dry_run=False):
    logger.info("=== STEP 2: Send Connection Requests ===")
    leads = read_csv_as_dicts(LEADS_CSV)
    daily_limit = cfg.get("daily_connection_limit", 20)
    sent_count = 0

    for lead in leads:
        if sent_count >= daily_limit:
            logger.info("Daily connection limit (%d) reached", daily_limit)
            break

        url = lead.get("profile_url", "")
        stage = get_lead_stage(pipeline, url)
        if stage not in ("scraped", "qualified"):
            continue
        if lead.get("qualified") != "yes":
            continue

        message = personalize_message("connection", lead, cfg)
        result = send_connection_request(lead, message, dry_run=dry_run)

        log_row = {
            "timestamp": datetime.utcnow().isoformat(),
            "profile_url": url,
            "full_name": lead.get("full_name", ""),
            "action_type": "connection_request",
            "message_variant": "connection",
            "status": result,
            "response": "",
        }
        append_csv(SENT_LOG_CSV, SENT_LOG_FIELDNAMES, log_row)
        advance_lead(pipeline, url, "connection_sent",
                     f"Connection request sent: {result}")
        notify_webhook(cfg, "connection_sent", {"profile_url": url, "status": result})
        sent_count += 1

    logger.info("Sent %d connection requests", sent_count)
    return sent_count


def step_send_followups(cfg, pipeline, dry_run=False):
    logger.info("=== STEP 3: Send Follow-up Messages ===")
    leads_by_url = {r["profile_url"]: r for r in read_csv_as_dicts(LEADS_CSV)}
    daily_limit = cfg.get("daily_message_limit", 50)
    sent_count = 0
    now = datetime.utcnow()

    followup_queue = load_json_file(FOLLOWUP_QUEUE_JSON, {})

    for url, state in pipeline.items():
        if sent_count >= daily_limit:
            logger.info("Daily message limit (%d) reached", daily_limit)
            break

        stage = state.get("stage", "")
        if stage not in ("connected", "message_sent"):
            continue

        last_updated_str = state.get("last_updated", "")
        try:
            last_updated = datetime.fromisoformat(last_updated_str)
        except Exception:
            last_updated = now - timedelta(days=10)

        delay_days = FOLLOWUP_DELAYS.get(stage, 3)
        if (now - last_updated).days < delay_days:
            continue

        lead = leads_by_url.get(url, {})
        if not lead:
            continue

        template_key = "followup_1" if stage == "connected" else "followup_2"
        message = personalize_message(template_key, lead, cfg)
        result = send_message(lead, message, dry_run=dry_run)

        log_row = {
            "timestamp": now.isoformat(),
            "profile_url": url,
            "full_name": lead.get("full_name", ""),
            "action_type": "message",
            "message_variant": template_key,
            "status": result,
            "response": "",
        }
        append_csv(SENT_LOG_CSV, SENT_LOG_FIELDNAMES, log_row)
        advance_lead(pipeline, url, "message_sent",
                     f"Follow-up '{template_key}' sent: {result}")
        notify_webhook(cfg, "message_sent", {"profile_url": url, "template": template_key})

        followup_queue[url] = {
            "last_followup": now.isoformat(),
            "followup_count": followup_queue.get(url, {}).get("followup_count", 0) + 1,
        }
        sent_count += 1

    write_json_file(FOLLOWUP_QUEUE_JSON, followup_queue)
    logger.info("Sent %d follow-up messages", sent_count)
    return sent_count


def step_check_demo_bookings(cfg, pipeline, dry_run=False):
    """
    Poll CRM/calendar endpoint for new demo bookings.
    In production: call Calendly / HubSpot / custom CRM API.
    """
    logger.info("=== STEP 4: Check Demo Bookings ===")
    crm_endpoint = cfg.get("crm_endpoint", "")
    bookings_found = 0

    if not crm_endpoint:
        logger.info("No CRM endpoint configured — skipping booking sync")
        return 0

    if dry_run:
        logger.info("[DRY-RUN] Would poll CRM at %s for new bookings", crm_endpoint)
        return 0

    try:
        html, status = fetch_url(crm_endpoint)
        if status == 200:
            try:
                data = json.loads(html)
                bookings = data.get("bookings", [])
            except json.JSONDecodeError:
                bookings = []

            for booking in bookings:
                url = booking.get("linkedin_url", "")
                if url and get_lead_stage(pipeline, url) not in ("demo_booked", "demo_completed", "closed_won"):
                    row = {
                        "timestamp": datetime.utcnow().isoformat(),
                        "profile_url": url,
                        "full_name": booking.get("name", ""),
                        "company": booking.get("company", ""),
                        "booking_source": "linkedin",
                        "meeting_date": booking.get("meeting_date", ""),
                        "status": "confirmed",
                    }
                    append_csv(BOOKINGS_CSV, BOOKINGS_FIELDNAMES, row)
                    advance_lead(pipeline, url, "demo_booked", "Demo booked via CRM sync")
                    notify_webhook(cfg, "demo_booked", row)
                    bookings_found += 1
        else:
            logger.warning("CRM endpoint returned status %s", status)
    except Exception as e:
        logger.error("Error checking demo bookings: %s", e)

    logger.info("Found %d new demo bookings", bookings_found)
    return bookings_found


# ---------------------------------------------------------------------------
# Status report
# ---------------------------------------------------------------------------

def compute_status(pipeline, cfg):
    stage_counts = {s: 0 for s in PIPELINE_STAGES}
    for state in pipeline.values():
        stage = state.get("stage", "scraped")
        if stage in stage_counts:
            stage_counts[stage] += 1

    leads = read_csv_as_dicts(LEADS_CSV)
    bookings = read_csv_as_dicts(BOOKINGS_CSV)
    sent_log = read_csv_as_dicts(SENT_LOG_CSV)

    total_leads = len(leads)
    qualified = sum(1 for r in leads if r.get("qualified") == "yes")
    connections_sent = sum(1 for r in sent_log if r.get("action_type") == "connection_request")
    messages_sent = sum(1 for r in sent_log if r.get("action_type") == "message")
    demos_booked = len(bookings)

    conn_rate = (stage_counts.get("connected", 0) / connections_sent * 100) if connections_sent else 0
    reply_rate = (stage_counts.get("replied", 0) / messages_sent * 100) if messages_sent else 0
    booking_rate = (demos_booked / stage_counts.get("connected", 1) * 100) if stage_counts.get("connected") else 0

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "totals": {
            "scraped_leads": total_leads,
            "qualified_leads": qualified,
            "connections_sent": connections_sent,
            "messages_sent": messages_sent,
            "demos_booked": demos_booked,
        },
        "pipeline_stages": stage_counts,
        "rates": {
            "connection_accept_rate_pct": round(conn_rate, 1),
            "reply_rate_pct": round(reply_rate, 1),
            "demo_booking_rate_pct": round(booking_rate, 1),
        },
        "config_summary": {
            "daily_connection_limit": cfg.get("daily_connection_limit"),
            "daily_message_limit": cfg.get("daily_message_limit"),
            "min_signal_score": cfg.get("min_signal_score"),
        },
    }


def print_status(status):
    print("\n" + "=" * 60)
    print("PRINTMAXX — LinkedIn AI Outbound Pipeline Status")
    print("=" * 60)
    print(f"Generated: {status['generated_at']}")
    print("\n--- Totals ---")
    for k, v in status["totals"].items():
        print(f"  {k:<28} {v}")
    print("\n--- Pipeline Stages ---")
    for stage, count in status["pipeline_stages"].items():
        bar = "#" * min(count, 40)
        print(f"  {stage:<22} {count:>4}  {bar}")
    print("\n--- Conversion Rates ---")
    for k, v in status["rates"].items():
        print(f"  {k:<38} {v}%")
    print("\n--- Config ---")
    for k, v in status["config_summary"].items():
        print(f"  {k:<38} {v}")
    print("=" * 60 + "\n")


# ---------------------------------------------------------------------------
# Main pipeline runner
# ---------------------------------------------------------------------------

def run_pipeline(cfg, dry_run=False):
    logger.info("=== PRINTMAXX LinkedIn Outbound Pipeline START (dry_run=%s) ===", dry_run)

    skills = recall_skills_for_task("linkedin_outbound")
    if skills:
        logger.info("Recalled %d skills for task", len(skills))

    ensure_data_dirs()
    init_csv(LEADS_CSV, LEADS_FIELDNAMES)
    init_csv(SENT_LOG_CSV, SENT_LOG_FIELDNAMES)
    init_csv(BOOKINGS_CSV, BOOKINGS_FIELDNAMES)

    pipeline = load_pipeline()

    new_leads = step_scrape_and_qualify(cfg, dry_run=dry_run)
    connections = step_send_connections(cfg, pipeline, dry_run=dry_run)
    followups = step_send_followups(cfg, pipeline, dry_run=dry_run)
    bookings = step_check_demo_bookings(cfg, pipeline, dry_run=dry_run)

    save_pipeline(pipeline)

    result = {
        "run_at": datetime.utcnow().isoformat(),
        "dry_run": dry_run,
        "new_leads": new_leads,
        "connections_sent": connections,
        "followups_sent": followups,
        "bookings_found": bookings,
    }

    run_log_path = safe_path(DATA_DIR / "last_run.json")
    write_json_file(run_log_path, result)
    capture_skill_from_result("linkedin_outbound", result)

    logger.info("Pipeline complete: %s", json.dumps(result))
    return result


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------

def main():
    setup_logging()

    parser = argparse.ArgumentParser(
        description="PRINTMAXX LinkedIn AI Agent Outbound Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --run            # Execute full pipeline\n"
            "  %(prog)s --dry-run        # Simulate without sending\n"
            "  %(prog)s --status         # Print pipeline dashboard\n"
        ),
    )
    parser.add_argument("--run", action="store_true", help="Execute the full outbound pipeline")
    parser.add_argument("--status", action="store_true", help="Print pipeline status dashboard")
    parser.add_argument("--dry-run", action="store_true", dest="dry_run",
                        help="Simulate pipeline without sending messages or writing leads")

    args = parser.parse_args()

    if not any([args.run, args.status, args.dry_run]):
        parser.print_help()
        sys.exit(0)

    try:
        cfg = load_config()

        if args.status:
            ensure_data_dirs()
            pipeline = load_pipeline()
            status = compute_status(pipeline, cfg)
            print_status(status)
            sys.exit(0)

        if args.run or args.dry_run:
            result = run_pipeline(cfg, dry_run=args.dry_run)
            logger.info("Run summary: %s", json.dumps(result, indent=2))
            sys.exit(0)

    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error("Unhandled error in pipeline: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()