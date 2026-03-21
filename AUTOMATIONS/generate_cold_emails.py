#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Cold Email Generator v2 — connects 2,170 leads to 16 live demo sites.

reads lead CSVs, auto-matches industry to surge.sh demo URLs, generates
personalized 3-email sequences with @pipelineabuser energy. no AI slop.

Usage:
    python3 AUTOMATIONS/generate_cold_emails.py                                    # all leads with emails
    python3 AUTOMATIONS/generate_cold_emails.py --min-score 60                     # score 60+ only
    python3 AUTOMATIONS/generate_cold_emails.py --industry dental --city Austin    # filter
    python3 AUTOMATIONS/generate_cold_emails.py --include-no-email                 # include leads without emails
    python3 AUTOMATIONS/generate_cold_emails.py --leads AUTOMATIONS/outreach/PIPELINE_TRACKER.csv --preview 3 --dry-run
    python3 AUTOMATIONS/generate_cold_emails.py --leads AUTOMATIONS/leads/ --output output/cold_emails/
    python3 AUTOMATIONS/generate_cold_emails.py --batch-cities Austin,Miami,Phoenix --min-score 60
    python3 AUTOMATIONS/generate_cold_emails.py --format instantly --output instantly_import.csv
    python3 AUTOMATIONS/generate_cold_emails.py --format mailshake --output mailshake_import.csv
    python3 AUTOMATIONS/generate_cold_emails.py --stats                            # stats only
    python3 AUTOMATIONS/generate_cold_emails.py --dry-run --preview 5              # preview 5 leads
    python3 AUTOMATIONS/generate_cold_emails.py --output-txt                       # individual .txt files
    python3 AUTOMATIONS/generate_cold_emails.py --list-industries                  # show demo URL mapping
"""

import csv
import hashlib
import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# defaults (overridable with --leads / --output)
DEFAULT_LEADS_DIR = BASE / "AUTOMATIONS" / "leads"
DEFAULT_OUTPUT_DIR = BASE / "output" / "cold_emails"
DEFAULT_PIPELINE = BASE / "AUTOMATIONS" / "outreach" / "PIPELINE_TRACKER.csv"
LOG_DIR = BASE / "AUTOMATIONS" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

# 16 live demo sites — surge.sh deployments
_DENTAL_CONFIG = {
    "demo_url": "https://dental-demo.surge.sh",
    "motion_url": "https://dental-motion.surge.sh",
    "keywords": ["dental", "dentist", "tooth", "teeth", "orthodont", "oral"],
}
_RESTAURANT_CONFIG = {
    "demo_url": "https://restaurant-site-demo.surge.sh",
    "motion_url": "https://restaurant-motion.surge.sh",
    "keywords": ["restaurant", "cafe", "bistro", "grill", "eatery", "food", "dining", "pizza", "sushi", "bar", "catering"],
}
_FITNESS_CONFIG = {
    "demo_url": "https://fitness-demo.surge.sh",
    "motion_url": None,
    "keywords": ["fitness", "gym", "crossfit", "yoga", "trainer", "workout", "pilates", "personal training"],
}
_LEGAL_CONFIG = {
    "demo_url": "https://legal-demo.surge.sh",
    "motion_url": None,
    "keywords": ["lawyer", "legal", "attorney", "law firm", "counsel", "litigation", "law office"],
}
_PLUMBER_CONFIG = {
    "demo_url": "https://plumber-demo.surge.sh",
    "motion_url": None,
    "keywords": ["plumber", "plumbing", "hvac", "heating", "cooling", "pipe", "drain"],
}
_REALTOR_CONFIG = {
    "demo_url": "https://realtor-demo.surge.sh",
    "motion_url": "https://realtor-motion.surge.sh",
    "keywords": ["realtor", "real estate", "realty", "property", "homes", "broker", "housing"],
}

INDUSTRY_MAP = {
    # Primary keys
    "dental": _DENTAL_CONFIG,
    "restaurant": _RESTAURANT_CONFIG,
    "fitness": _FITNESS_CONFIG,
    "legal": _LEGAL_CONFIG,
    "plumber": _PLUMBER_CONFIG,
    "realtor": _REALTOR_CONFIG,
    # Aliases (CSV categories often use these)
    "dentist": _DENTAL_CONFIG,
    "lawyer": _LEGAL_CONFIG,
    "plumbing": _PLUMBER_CONFIG,
    "real_estate": _REALTOR_CONFIG,
}

# sender placeholders — replaced when SECRETS/PAYMENT_INFO.md exists
SENDER = {
    "name": "{{MY_NAME}}",
    "phone": "{{MY_PHONE}}",
    "email": "{{MY_EMAIL}}",
    "company": "{{MY_COMPANY}}",
    "address": "{{MY_ADDRESS}}",
}

# CAN-SPAM compliant footer appended to every email
CANSPAM_FOOTER = (
    "\n---\n"
    f"{SENDER['company']} | {SENDER['address']}\n"
    "Reply STOP to unsubscribe from future emails.\n"
    "This is a one-time outreach. You will not be added to any mailing list."
)

# directories, job boards, government sites — not real leads
SKIP_KEYWORDS = [
    "best dentists", "top dentists", "reviews & ratings", "bureau of labor",
    "careerbuilder", "indeed.com", "ratemds", "realself", "yelp", "yellow pages",
    "search dentists", "occupational employment", "division of professions",
    "state bar of", "best lawyers", "best plumber near", "find a dentist",
    "dentists ranked", "top local", "plumbing supplies", "best restaurants",
    "top chicago culinary", "national restaurant association", "prep courses",
    "office of harris county", "state plumbing board", "crime radar",
    "colorado division", "price reduced", "practice for sale",
    "complete 2025 guide", "complete 2026 guide", "your complete",
]


def detect_industry(filename: str, category: str = "", business_name: str = "") -> str:
    """auto-detect industry from filename, category, or business name."""
    text = f"{filename} {category} {business_name}".lower()
    for industry, config in INDUSTRY_MAP.items():
        for kw in config["keywords"]:
            if kw in text:
                return industry
    return "general"


def build_issue_text(signals: str) -> str:
    """turn signal codes into human-readable pain points."""
    issues = []
    if "NOT_mobile" in signals:
        issues.append("doesn't work on phones")
    if "no_form" in signals:
        issues.append("no way for customers to contact you")
    if "no_schema" in signals:
        issues.append("invisible to google maps")
    if "slow" in signals or "ok:" in signals:
        m = re.search(r'(?:ok|slow):(\d+\.?\d*)s', signals)
        if m and float(m.group(1)) > 3:
            issues.append(f"takes {m.group(1)}s to load")
    if "OLD:" in signals:
        issues.append("running tech from 2015")
    return ", ".join(issues[:3]) if issues else "could use a refresh"


def _shorten_biz(name: str) -> str:
    """truncate long business names for subject/body use."""
    if not name:
        return "your business"
    # strip common noise
    for suffix in [" LLC", " Inc", " Corp", " Ltd", " PC", " PLLC", " DDS",
                   " DMD", " MD", " PA", " Named a", " Online Services",
                   " - Your Complete", " - Best", " for Sale", " **Price Reduced**"]:
        idx = name.lower().find(suffix.lower())
        if idx > 0:
            name = name[:idx]
    name = name.strip().strip('"').strip(",").strip("*").strip()
    if len(name) > 40:
        name = name[:37].rsplit(" ", 1)[0] + "..."
    return name


def generate_emails(lead: dict, industry: str) -> dict:
    """generate 3 emails for one lead. returns dict with subject, body, follow_up_1, follow_up_2."""
    biz = _shorten_biz(lead.get("business_name", "").strip().strip('"'))
    website = lead.get("website", "")
    city = lead.get("city", "")
    score = int(lead.get("website_score", 0) or 0)
    signals = lead.get("signals_detected", "")

    config = INDUSTRY_MAP.get(industry, INDUSTRY_MAP["dental"])
    demo_url = config["demo_url"]

    # premium prospects get motion upsell URL
    motion_url = config.get("motion_url")
    if score >= 80 and motion_url:
        demo_url = motion_url

    issue_text = build_issue_text(signals)

    # --- EMAIL 1: the hook (day 0) ---
    # score-based angle selection
    if score <= 10 or "unreachable" in signals:
        # no website angle
        subject = f"built this for {biz}"
        body = (
            f"searched for \"{biz}\" online. you don't show up.\n\n"
            f"your competitors in {city} do. they're getting the calls.\n\n"
            f"i built you a site: {demo_url}\n\n"
            f"loads in under 2 seconds. works on phones. click-to-call button front and center.\n\n"
            f"$500 flat. $50/mo hosting. cancel whenever.\n\n"
            f"want it live on your domain by friday? reply here.\n\n"
            f"{SENDER['name']}"
        )
    elif score < 60:
        # bad website angle
        subject = f"checked {biz}'s site on my phone"
        body = (
            f"pulled up {website if website else biz + chr(39) + 's site'} on mobile. it {issue_text}.\n\n"
            f"every extra second of load time costs you 7% in conversions. that's real money walking out the door.\n\n"
            f"i built a replacement: {demo_url}\n\n"
            f"under 2 seconds. click-to-call. mobile-first. google business schema baked in.\n\n"
            f"$500 to swap it. $50/mo to run it. i handle the domain transfer.\n\n"
            f"worth a 5-minute look?\n\n"
            f"{SENDER['name']}"
        )
    else:
        # good website, upgrade angle
        subject = f"quick win for {biz}"
        body = (
            f"your site{' at ' + website if website else ''} is solid. but i spotted a few things that would bring in more calls.\n\n"
            f"i put together a demo with those fixes: {demo_url}\n\n"
            f"mobile-optimized. click-to-call. structured data for google. fast.\n\n"
            f"not a rebuild. just the upgrades that typically bump calls 20-40%.\n\n"
            f"interested? takes 5 minutes to walk through.\n\n"
            f"{SENDER['name']}"
        )

    # --- EMAIL 2: follow-up with proof (day 3) ---
    follow_up_1_subject = f"re: {biz}"
    follow_up_1 = (
        f"following up on the site i built for you: {demo_url}\n\n"
        f"sites like this one typically load 3-5x faster than older designs. "
        f"faster load = more people stay on the page.\n\n"
        f"the site is done. i can have it live on your domain by friday.\n\n"
        f"if not, no worries. just thought it was worth showing you.\n\n"
        f"{SENDER['name']}"
    )

    # --- EMAIL 3: breakup (day 7) ---
    follow_up_2_subject = f"removing your demo site"
    follow_up_2 = (
        f"built a custom site for {biz} last week: {demo_url}\n\n"
        f"haven't heard back. i'll assume timing's off.\n\n"
        f"taking the demo down friday to free up the slot. "
        f"reply \"keep it\" if you want me to hold it.\n\n"
        f"either way, no hard feelings.\n\n"
        f"{SENDER['name']}"
    )

    return {
        "subject": subject,
        "body": body + CANSPAM_FOOTER,
        "follow_up_1_subject": follow_up_1_subject,
        "follow_up_1": follow_up_1 + CANSPAM_FOOTER,
        "follow_up_2_subject": follow_up_2_subject,
        "follow_up_2": follow_up_2 + CANSPAM_FOOTER,
        "demo_url": demo_url,
    }


def load_leads(leads_dir: Path, min_score: int = 0, industry_filter: str = "",
               city_filter: str = "", email_only: bool = True) -> list:
    """load and filter leads from CSV directory."""
    leads = []
    files = sorted(leads_dir.glob("*.csv"))
    # skip aggregated/non-lead files
    skip_names = {"MASTER_LEADS.csv", "HOT_LEADS.csv", "SCORED_LEADS.csv",
                  "android_clone_opportunities.csv", "g2_reviewer_leads.csv",
                  "gov_tenders_active.csv", "indeed_hiring_leads.csv",
                  "sam_gov_opportunities.csv", "usaspending_awards.csv"}

    for filepath in files:
        if filepath.name in skip_names:
            continue
        try:
            with open(filepath, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    industry = detect_industry(
                        filepath.name,
                        row.get("category", ""),
                        row.get("business_name", "")
                    )
                    row["_industry"] = industry
                    row["_source_file"] = filepath.name

                    # industry filter
                    if industry_filter and industry != industry_filter.lower():
                        continue

                    # city filter
                    if city_filter and city_filter.lower() not in (row.get("city", "") or "").lower():
                        continue

                    # score filter
                    score = int(row.get("website_score", 0) or 0)
                    if score < min_score:
                        continue

                    # email filter (default: only leads with emails)
                    if email_only and not (row.get("email_if_found", "") or row.get("email", "")).strip():
                        continue

                    # skip directories, job boards, etc.
                    biz = (row.get("business_name", "") or "").lower()
                    if any(kw in biz for kw in SKIP_KEYWORDS):
                        continue

                    # skip empty business names
                    if not row.get("business_name", "").strip():
                        continue

                    # normalize email field
                    row["_email"] = (row.get("email_if_found", "") or row.get("email", "")).strip()

                    leads.append(row)
        except Exception as e:
            print(f"  warning: {filepath.name}: {e}")

    return leads


def load_single_csv(filepath: Path, min_score: int = 0, industry_filter: str = "",
                     city_filter: str = "", email_only: bool = True) -> list:
    """load leads from a single CSV file (handles PIPELINE_TRACKER, MASTER_LEADS, SCORED_LEADS formats)."""
    leads = []
    if not filepath.exists():
        print(f"  ERROR: file not found: {filepath}")
        return leads

    # auto-detect column names
    FIELD_ALIASES = {
        "business_name": ["business_name", "name", "company", "biz_name"],
        "email":         ["email", "email_if_found", "to_email", "contact_email"],
        "industry":      ["industry", "category", "type", "niche"],
        "city":          ["city", "location", "area"],
        "website":       ["website", "url", "site", "domain"],
        "website_score": ["website_score", "score", "site_score", "total_score"],
        "top_issue":     ["top_issue", "issue", "issues"],
        "signals":       ["signals_detected", "signals", "pain_signals"],
        "phone":         ["phone", "phone_number"],
        "lead_id":       ["lead_id", "id", "lead"],
        "demo_url":      ["demo_url"],
    }

    try:
        with open(filepath, newline="", encoding="utf-8", errors="replace") as f:
            sample = f.read(8192)
            f.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",\t|;")
            except csv.Error:
                dialect = csv.excel

            reader = csv.reader(f, dialect)
            headers = next(reader)
            norm_headers = [h.strip().lower().replace(" ", "_").replace("-", "_") for h in headers]

            # map columns
            col_map = {}
            for field, aliases in FIELD_ALIASES.items():
                for alias in aliases:
                    if alias in norm_headers:
                        col_map[field] = norm_headers.index(alias)
                        break

            if "business_name" not in col_map:
                print(f"  ERROR: no business_name column found. columns: {headers}")
                return leads

            def _get(field, row):
                idx = col_map.get(field)
                if idx is None or idx >= len(row):
                    return ""
                return row[idx].strip()

            for row_num, row in enumerate(reader, start=2):
                if not row or len(row) < 2:
                    continue

                biz_name = _get("business_name", row)
                if not biz_name:
                    continue

                # skip junk
                biz_low = biz_name.lower()
                if any(kw in biz_low for kw in SKIP_KEYWORDS):
                    continue

                # email
                email = _get("email", row)
                if email_only and (not email or "@" not in email):
                    continue

                # score
                score_str = _get("website_score", row)
                try:
                    score = int(float(score_str)) if score_str else 0
                except (ValueError, TypeError):
                    score = 0
                if score < min_score:
                    continue

                # industry
                raw_industry = _get("industry", row)
                if not raw_industry:
                    raw_industry = detect_industry(filepath.name, "", biz_name)
                industry = raw_industry.lower().strip()
                if industry_filter and industry != industry_filter.lower():
                    continue

                # city
                city = _get("city", row)
                if city_filter and city_filter.lower() not in city.lower():
                    continue

                # demo URL from data or mapped
                demo_url = _get("demo_url", row)
                config = INDUSTRY_MAP.get(industry, INDUSTRY_MAP.get("dental", {}))
                if not demo_url:
                    demo_url = config.get("demo_url", "https://dental-demo.surge.sh")

                lead = {
                    "business_name": biz_name,
                    "website": _get("website", row),
                    "city": city,
                    "website_score": score,
                    "signals_detected": _get("signals", row) or _get("top_issue", row),
                    "email_if_found": email,
                    "_email": email,
                    "_industry": industry,
                    "_source_file": filepath.name,
                    "lead_id": _get("lead_id", row) or f"G-{row_num:05d}",
                    "demo_url": demo_url,
                }
                leads.append(lead)
    except Exception as e:
        print(f"  ERROR reading {filepath}: {e}")

    return leads


def deduplicate(leads: list) -> list:
    """remove duplicates by email address, then by website URL."""
    seen_emails = set()
    seen_websites = set()
    unique = []
    for lead in leads:
        email = lead.get("_email", "").lower()
        website = (lead.get("website", "") or "").strip().rstrip("/").lower()

        if email and email in seen_emails:
            continue
        if website and website in seen_websites:
            continue

        if email:
            seen_emails.add(email)
        if website:
            seen_websites.add(website)
        unique.append(lead)
    return unique


def write_ready_csv(leads: list, output_dir: Path, tag: str = "") -> Path:
    """write cold_emails_ready.csv in the format team-lead specified."""
    output_dir.mkdir(parents=True, exist_ok=True)
    suffix = f"_{tag}" if tag else ""
    filename = f"cold_emails_ready{suffix}.csv"
    output_path = output_dir / filename

    fieldnames = [
        "to_email", "subject", "body", "follow_up_1", "follow_up_2",
        "demo_url", "lead_score", "business_name", "city", "industry",
        "website", "follow_up_1_subject", "follow_up_2_subject",
    ]

    rows = []
    for lead in leads:
        industry = lead["_industry"]
        emails = generate_emails(lead, industry)
        rows.append({
            "to_email": lead["_email"],
            "subject": emails["subject"],
            "body": emails["body"],
            "follow_up_1": emails["follow_up_1"],
            "follow_up_2": emails["follow_up_2"],
            "demo_url": emails["demo_url"],
            "lead_score": lead.get("website_score", ""),
            "business_name": lead.get("business_name", "").strip().strip('"'),
            "city": lead.get("city", ""),
            "industry": industry,
            "website": lead.get("website", ""),
            "follow_up_1_subject": emails["follow_up_1_subject"],
            "follow_up_2_subject": emails["follow_up_2_subject"],
        })

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  output: {output_path} ({len(rows)} leads)")
    return output_path


def write_txt_files(leads: list, output_dir: Path, tag: str = "") -> Path:
    """write individual .txt files per lead."""
    suffix = f"_{tag}" if tag else ""
    txt_dir = output_dir / f"txt{suffix}"
    txt_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for lead in leads:
        industry = lead["_industry"]
        emails = generate_emails(lead, industry)
        biz = lead.get("business_name", "Unknown").strip().strip('"')
        city = (lead.get("city", "") or "unknown").replace(" ", "_")
        safe_name = re.sub(r'[^\w\s-]', '', biz).strip().replace(' ', '_')[:40]
        filename = f"{industry}_{city}_{safe_name}.txt"

        lines = [
            f"TO: {lead['_email']}",
            f"BUSINESS: {biz}",
            f"WEBSITE: {lead.get('website', '') or '(none)'}",
            f"CITY: {lead.get('city', '')}",
            f"INDUSTRY: {industry}",
            f"SCORE: {lead.get('website_score', '?')}",
            f"DEMO: {emails['demo_url']}",
            "",
            "=" * 60,
            "",
            f"--- EMAIL 1 (send now) ---",
            f"SUBJECT: {emails['subject']}",
            "",
            emails["body"],
            "",
            "=" * 60,
            "",
            f"--- EMAIL 2 (day 3) ---",
            f"SUBJECT: {emails['follow_up_1_subject']}",
            "",
            emails["follow_up_1"],
            "",
            "=" * 60,
            "",
            f"--- EMAIL 3 (day 7) ---",
            f"SUBJECT: {emails['follow_up_2_subject']}",
            "",
            emails["follow_up_2"],
            "",
            "=" * 60,
        ]

        with open(txt_dir / filename, "w") as f:
            f.write("\n".join(lines))
        count += 1

    print(f"  txt files: {txt_dir}/ ({count} files)")
    return txt_dir


def write_instantly_format(leads: list, output_dir: Path, tag: str = ""):
    """write Instantly.ai CSV import format."""
    output_dir.mkdir(parents=True, exist_ok=True)
    suffix = f"_{tag}" if tag else ""

    for step, field in [(1, "body"), (2, "follow_up_1"), (3, "follow_up_2")]:
        filename = f"instantly_step{step}{suffix}.csv"
        output_path = output_dir / filename
        fieldnames = ["email", "first_name", "company_name", "custom1", "custom2", "custom3"]

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for lead in leads:
                biz = lead.get("business_name", "").strip().strip('"')
                parts = biz.split()
                first = parts[0] if len(parts) == 2 and parts[0][0].isupper() and parts[1][0].isupper() else "there"

                industry = lead["_industry"]
                emails = generate_emails(lead, industry)

                writer.writerow({
                    "email": lead["_email"],
                    "first_name": first,
                    "company_name": biz,
                    "custom1": emails["demo_url"],
                    "custom2": lead.get("website", ""),
                    "custom3": lead.get("city", ""),
                })

        print(f"  instantly step {step}: {output_path} ({len(leads)} rows)")


def write_format_csv(leads: list, output_path: str):
    """write sequence CSV: lead_id, business_name, email, industry, demo_url, sequence_num, subject, body, send_delay_days."""
    fieldnames = [
        "lead_id", "business_name", "email", "industry", "city",
        "website_score", "demo_url", "sequence_num", "subject", "body",
        "send_delay_days",
    ]
    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
    rows = []
    for lead in leads:
        industry = lead["_industry"]
        emails_data = generate_emails(lead, industry)
        base = {
            "lead_id": lead.get("lead_id", ""),
            "business_name": lead.get("business_name", "").strip().strip('"'),
            "email": lead["_email"],
            "industry": industry,
            "city": lead.get("city", ""),
            "website_score": lead.get("website_score", ""),
            "demo_url": emails_data["demo_url"],
        }
        rows.append({**base, "sequence_num": 1, "subject": emails_data["subject"],
                      "body": emails_data["body"], "send_delay_days": 0})
        rows.append({**base, "sequence_num": 2, "subject": emails_data["follow_up_1_subject"],
                      "body": emails_data["follow_up_1"], "send_delay_days": 3})
        rows.append({**base, "sequence_num": 3, "subject": emails_data["follow_up_2_subject"],
                      "body": emails_data["follow_up_2"], "send_delay_days": 7})

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  output: {output_path} ({len(rows)} rows, {len(leads)} leads x 3)")


def write_format_instantly(leads: list, output_path: str):
    """write Instantly.ai format: one row per lead, step columns."""
    fieldnames = [
        "email", "first_name", "company_name", "city",
        "step1_subject", "step1_body", "step1_delay",
        "step2_subject", "step2_body", "step2_delay",
        "step3_subject", "step3_body", "step3_delay",
    ]
    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
    rows = []
    for lead in leads:
        industry = lead["_industry"]
        emails_data = generate_emails(lead, industry)
        biz = lead.get("business_name", "").strip().strip('"')
        parts = biz.split()
        first_name = parts[0] if len(parts) == 2 and parts[0][0].isupper() and parts[1][0].isupper() else ""
        rows.append({
            "email": lead["_email"],
            "first_name": first_name,
            "company_name": biz,
            "city": lead.get("city", ""),
            "step1_subject": emails_data["subject"],
            "step1_body": emails_data["body"],
            "step1_delay": 0,
            "step2_subject": emails_data["follow_up_1_subject"],
            "step2_body": emails_data["follow_up_1"],
            "step2_delay": 3,
            "step3_subject": emails_data["follow_up_2_subject"],
            "step3_body": emails_data["follow_up_2"],
            "step3_delay": 7,
        })

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  output (Instantly): {output_path} ({len(rows)} leads)")


def write_format_mailshake(leads: list, output_path: str):
    """write Mailshake format."""
    fieldnames = [
        "Email Address", "Full Name", "Company",
        "Subject", "Body", "Sequence Step", "Delay Days",
    ]
    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
    rows = []
    for lead in leads:
        industry = lead["_industry"]
        emails_data = generate_emails(lead, industry)
        biz = lead.get("business_name", "").strip().strip('"')
        for seq, subj_key, body_key, delay in [
            (1, "subject", "body", 0),
            (2, "follow_up_1_subject", "follow_up_1", 3),
            (3, "follow_up_2_subject", "follow_up_2", 7),
        ]:
            rows.append({
                "Email Address": lead["_email"],
                "Full Name": "",
                "Company": biz,
                "Subject": emails_data[subj_key],
                "Body": emails_data[body_key],
                "Sequence Step": seq,
                "Delay Days": delay,
            })

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  output (Mailshake): {output_path} ({len(rows)} rows)")


def preview_leads(leads: list, count: int):
    """preview N leads with full 3-email sequences."""
    for lead in leads[:count]:
        industry = lead["_industry"]
        emails_data = generate_emails(lead, industry)
        biz = lead.get("business_name", "?").strip().strip('"')
        score = lead.get("website_score", "?")
        city = lead.get("city", "?")

        print(f"\n{'='*70}")
        print(f"LEAD: {biz} ({industry}, {city})")
        print(f"TO: {lead['_email']}  |  SCORE: {score}  |  DEMO: {emails_data['demo_url']}")

        for seq_num, subj_key, body_key, delay in [
            (1, "subject", "body", 0),
            (2, "follow_up_1_subject", "follow_up_1", 3),
            (3, "follow_up_2_subject", "follow_up_2", 7),
        ]:
            print(f"\n--- SEQUENCE {seq_num}/3  |  DELAY: +{delay} days ---")
            print(f"SUBJECT: {emails_data[subj_key]}")
            print(f"{'-'*50}")
            print(emails_data[body_key])


def list_industries():
    """print all industry -> demo URL mappings."""
    print("\nindustry -> demo URL mappings:")
    for industry, config in sorted(INDUSTRY_MAP.items()):
        print(f"  {industry:<15} -> {config['demo_url']}")
        if config.get("motion_url"):
            print(f"  {industry + ' (motion)':<15} -> {config['motion_url']}")
        print(f"    keywords: {', '.join(config['keywords'])}")
    print()


def print_stats(leads: list):
    """print summary stats per city and industry."""
    print(f"\n{'='*60}")
    print(f"  LEAD STATS")
    print(f"{'='*60}")
    print(f"  total: {len(leads)} leads with email addresses")

    # by industry
    ind_counts = {}
    for lead in leads:
        ind = lead.get("_industry", "unknown")
        ind_counts[ind] = ind_counts.get(ind, 0) + 1
    print(f"\n  by industry:")
    for ind, count in sorted(ind_counts.items(), key=lambda x: -x[1]):
        demo = INDUSTRY_MAP.get(ind, {}).get("demo_url", "no demo")
        print(f"    {ind:<15} {count:>4}  {demo}")

    # by city
    city_counts = {}
    for lead in leads:
        city = lead.get("city", "unknown") or "unknown"
        city_counts[city] = city_counts.get(city, 0) + 1
    print(f"\n  by city:")
    for city, count in sorted(city_counts.items(), key=lambda x: -x[1])[:20]:
        print(f"    {city:<25} {count:>4}")

    # by score range
    ranges = {"0-29": 0, "30-59": 0, "60-79": 0, "80-100": 0}
    for lead in leads:
        score = int(lead.get("website_score", 0) or 0)
        if score < 30: ranges["0-29"] += 1
        elif score < 60: ranges["30-59"] += 1
        elif score < 80: ranges["60-79"] += 1
        else: ranges["80-100"] += 1
    print(f"\n  by score:")
    for rng, count in ranges.items():
        label = ""
        if rng == "80-100":
            label = " (gets motion upsell URL)"
        elif rng == "0-29":
            label = " (no-site angle)"
        elif rng == "30-59":
            label = " (bad-site angle)"
        else:
            label = " (upgrade angle)"
        print(f"    {rng:<10} {count:>4}{label}")

    # cross-tab: industry x city
    cross = {}
    for lead in leads:
        key = (lead.get("_industry", "?"), lead.get("city", "?"))
        cross[key] = cross.get(key, 0) + 1
    print(f"\n  top combos (industry + city):")
    for (ind, city), count in sorted(cross.items(), key=lambda x: -x[1])[:15]:
        print(f"    {ind:<12} {city:<20} {count:>4}")

    print(f"{'='*60}\n")


def parse_args(args: list) -> dict:
    """parse CLI arguments."""
    opts = {
        "leads_dir": DEFAULT_LEADS_DIR,
        "leads_file": None,  # single file mode
        "output_dir": DEFAULT_OUTPUT_DIR,
        "output_file": None,  # explicit output file
        "min_score": 0,
        "industry": "",
        "city": "",
        "batch_cities": "",
        "email_only": True,
        "dry_run": "--dry-run" in args,
        "stats_only": "--stats" in args,
        "output_txt": "--output-txt" in args,
        "list_industries": "--list-industries" in args,
        "preview": 0,
        "format": "csv",
    }

    if "--include-no-email" in args:
        opts["email_only"] = False

    def get_arg(flag):
        if flag in args:
            idx = args.index(flag)
            return args[idx + 1] if idx + 1 < len(args) else ""
        return ""

    leads_path = get_arg("--leads")
    if leads_path:
        p = Path(leads_path) if Path(leads_path).is_absolute() else BASE / leads_path
        if p.is_file():
            opts["leads_file"] = p
        elif p.is_dir():
            opts["leads_dir"] = p
        else:
            # might be relative to AUTOMATIONS
            p2 = BASE / "AUTOMATIONS" / leads_path
            if p2.exists():
                opts["leads_file"] = p2 if p2.is_file() else None
                opts["leads_dir"] = p2 if p2.is_dir() else opts["leads_dir"]
            else:
                opts["leads_file"] = p  # will error later

    output_path = get_arg("--output")
    if output_path:
        p = Path(output_path) if Path(output_path).is_absolute() else BASE / output_path
        if str(output_path).endswith(".csv"):
            opts["output_file"] = p
        else:
            opts["output_dir"] = p

    min_score = get_arg("--min-score")
    if min_score:
        opts["min_score"] = int(min_score)

    preview_str = get_arg("--preview")
    if preview_str:
        try:
            opts["preview"] = int(preview_str)
        except ValueError:
            opts["preview"] = 3

    fmt = get_arg("--format")
    if fmt and fmt in ("csv", "instantly", "mailshake"):
        opts["format"] = fmt

    opts["industry"] = get_arg("--industry")
    opts["city"] = get_arg("--city")
    opts["batch_cities"] = get_arg("--batch-cities")

    return opts


def main():
    opts = parse_args(sys.argv[1:])

    # list industries mode
    if opts["list_industries"]:
        list_industries()
        return

    # batch mode
    if opts["batch_cities"]:
        cities = [c.strip() for c in opts["batch_cities"].split(",")]
        print(f"\ncold email generator — batch mode")
        print(f"{'='*50}")
        print(f"  cities: {', '.join(cities)}")
        print(f"  min score: {opts['min_score']}")
        print(f"  industry: {opts['industry'] or 'all'}")
        print(f"  email only: {opts['email_only']}")
        print()

        all_leads = []
        for city in cities:
            city_leads = load_leads(opts["leads_dir"], opts["min_score"], opts["industry"], city, opts["email_only"])
            city_leads = deduplicate(city_leads)
            print(f"  {city}: {len(city_leads)} leads")
            all_leads.extend(city_leads)

        all_leads = deduplicate(all_leads)
        print(f"\n  total unique: {len(all_leads)}")

        if not all_leads:
            print("  no leads found matching criteria.")
            return

        print_stats(all_leads)

        tag = "_".join(c.replace(" ", "") for c in cities[:3])
        write_ready_csv(all_leads, opts["output_dir"], tag)
        write_instantly_format(all_leads, opts["output_dir"], tag)
        write_txt_files(all_leads, opts["output_dir"], tag)

        print(f"\n  done. {len(all_leads)} leads, 3 emails each.")
        return

    # determine source: single file or directory
    source_label = ""
    if opts["leads_file"]:
        source_label = str(opts["leads_file"])
    else:
        source_label = str(opts["leads_dir"])

    # normal mode
    print(f"\ncold email generator v2")
    print(f"{'='*50}")
    print(f"  leads: {source_label}")
    print(f"  output: {opts['output_file'] or opts['output_dir']}")
    print(f"  format: {opts['format']}")
    print(f"  min score: {opts['min_score']}")
    print(f"  industry: {opts['industry'] or 'all'}")
    print(f"  city: {opts['city'] or 'all'}")
    print(f"  email only: {opts['email_only']}")
    if opts["preview"]:
        print(f"  preview: {opts['preview']} leads")
    print()

    # load leads
    if opts["leads_file"]:
        leads = load_single_csv(opts["leads_file"], opts["min_score"], opts["industry"],
                                opts["city"], opts["email_only"])
    else:
        leads = load_leads(opts["leads_dir"], opts["min_score"], opts["industry"],
                           opts["city"], opts["email_only"])
    print(f"  loaded: {len(leads)} raw leads")

    leads = deduplicate(leads)
    print(f"  after dedup: {len(leads)} unique leads")

    if not leads:
        print("  no leads found matching criteria.")
        return

    print_stats(leads)

    if opts["stats_only"]:
        return

    # preview mode
    if opts["preview"] > 0:
        preview_leads(leads, opts["preview"])

    if opts["dry_run"]:
        if opts["preview"] == 0:
            # show brief preview if --preview not specified
            print("\ndry run — first 3 leads:\n")
            for lead in leads[:3]:
                industry = lead["_industry"]
                emails = generate_emails(lead, industry)
                biz = lead.get("business_name", "?").strip().strip('"')
                print(f"  --- {biz} ({industry}, {lead.get('city', '?')}, score {lead.get('website_score', '?')}) ---")
                print(f"  to: {lead['_email']}")
                print(f"  demo: {emails['demo_url']}")
                print(f"\n  email 1: {emails['subject']}")
                print(f"  {emails['body'][:150]}...\n")
                print(f"  email 2: {emails['follow_up_1_subject']}")
                print(f"  {emails['follow_up_1'][:100]}...\n")
                print(f"  email 3: {emails['follow_up_2_subject']}")
                print(f"  {emails['follow_up_2'][:100]}...\n")
        print(f"\n[DRY RUN] no files written. remove --dry-run to generate output.")
        return

    # generate and write based on format
    ts = datetime.now().strftime("%Y%m%d_%H%M")

    if opts["format"] == "instantly":
        output_path = str(opts["output_file"] or opts["output_dir"] / f"cold_emails_instantly_{ts}.csv")
        write_format_instantly(leads, output_path)
    elif opts["format"] == "mailshake":
        output_path = str(opts["output_file"] or opts["output_dir"] / f"cold_emails_mailshake_{ts}.csv")
        write_format_mailshake(leads, output_path)
    else:
        output_path = str(opts["output_file"] or opts["output_dir"] / f"cold_emails_generated_{ts}.csv")
        write_format_csv(leads, output_path)

    # also write legacy formats for compatibility
    write_ready_csv(leads, opts["output_dir"])
    write_instantly_format(leads, opts["output_dir"])

    if opts["output_txt"]:
        write_txt_files(leads, opts["output_dir"])

    # log
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "leads_processed": len(leads),
        "min_score": opts["min_score"],
        "industry": opts["industry"] or "all",
        "city": opts["city"] or "all",
        "format": opts["format"],
        "output": output_path,
    }
    log_path = LOG_DIR / "cold_email_generator.jsonl"
    with open(log_path, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"\n{'='*60}")
    print(f"  done. {len(leads)} leads processed.")
    print(f"  primary output: {output_path}")
    print(f"  replace {{{{MY_NAME}}}}, {{{{MY_PHONE}}}}, {{{{MY_EMAIL}}}} before sending.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
