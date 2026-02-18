#!/usr/bin/env python3
"""
PRINTMAXX Compliance Deadline Tracker — Regulatory Milestone Monitor
====================================================================
Tracks ALL regulatory deadlines affecting PRINTMAXX operations.
Generates alerts when deadlines approach. Auto-checks for new regulations
via web scraping. Outputs digest + CSV for quant terminal integration.

Sources: OPS/PLATFORM_ALGORITHM_RESEARCH_FEB2026.md, OPS/NEW_METHODS_TO_ADD.csv,
         MONEY_METHODS/AI_INFLUENCER/, OPS/COLD_EMAIL_LAUNCH_CHECKLIST.md

Usage:
    python3 compliance_deadline_tracker.py --check       # Show all deadlines + alerts
    python3 compliance_deadline_tracker.py --upcoming     # Next 90 days only
    python3 compliance_deadline_tracker.py --scan         # Scrape for new regulations
    python3 compliance_deadline_tracker.py --digest       # Generate OPS/ digest
    python3 compliance_deadline_tracker.py --status       # Quick 1-line status
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

# --- Paths ---
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
LEDGER_DIR = BASE_DIR / "LEDGER"
OPS_DIR = BASE_DIR / "OPS"
LOG_DIR = SCRIPT_DIR / "logs"
DEADLINE_CSV = LEDGER_DIR / "COMPLIANCE_DEADLINES.csv"
ALPHA_CSV = LEDGER_DIR / "ALPHA_STAGING.csv"

# --- Colors ---
G = "\033[92m"; R = "\033[91m"; Y = "\033[93m"; B = "\033[94m"
M = "\033[95m"; C = "\033[96m"; W = "\033[97m"; D = "\033[0m"; BOLD = "\033[1m"

# ============================================================
# REGULATORY DEADLINES DATABASE
# ============================================================
# Each entry: id, regulation, jurisdiction, effective_date, category,
#             impact_level, status, penalties, action_required, source_url, alpha_id

DEADLINES = [
    # --- ACTIVE NOW (already in effect) ---
    {
        "id": "REG001",
        "regulation": "Platform AI Content Labeling",
        "jurisdiction": "YouTube/TikTok/Meta (Global)",
        "effective_date": "2026-01-19",
        "category": "AI_DISCLOSURE",
        "impact": "CRITICAL",
        "status": "ACTIVE",
        "penalties": "YouTube Partner Program suspension, account restrictions",
        "action_required": "Label ALL AI-generated content on YouTube, TikTok, Meta. Visible disclosure for synthetic people/events/voices.",
        "source_url": "https://influencermarketinghub.com/ai-disclosure-rules/",
        "alpha_id": "ALPHA807",
    },
    {
        "id": "REG002",
        "regulation": "UK HFSS Advertising Ban",
        "jurisdiction": "United Kingdom",
        "effective_date": "2026-01-05",
        "category": "ADVERTISING",
        "impact": "MEDIUM",
        "status": "ACTIVE",
        "penalties": "UK advertising violations, fines",
        "action_required": "No HFSS food/drink advertising in influencer content targeting UK audiences. Check brand deals for HFSS products.",
        "source_url": "https://www.netinfluencer.com/global-creator-economy-regulation-what-is-scheduled-for-2026/",
        "alpha_id": "ALPHA808",
    },
    {
        "id": "REG003",
        "regulation": "FTC Synthetic Media Enforcement (Expanded)",
        "jurisdiction": "United States (Federal)",
        "effective_date": "2026-01-01",
        "category": "FTC",
        "impact": "CRITICAL",
        "status": "ACTIVE",
        "penalties": "FTC fines (higher than previous), enforcement actions",
        "action_required": "AI disclosure on all AI-generated content. FTC expanding to child-directed content, podcast ads, affiliate links. Review all affiliate links for proper disclosure.",
        "source_url": "https://www.netinfluencer.com/global-creator-economy-regulation-what-is-scheduled-for-2026/",
        "alpha_id": "ALPHA804",
    },
    {
        "id": "REG004",
        "regulation": "Colorado AI Act (SB21-169)",
        "jurisdiction": "Colorado",
        "effective_date": "2026-01-01",
        "category": "AI_REGULATION",
        "impact": "MEDIUM",
        "status": "ACTIVE",
        "penalties": "$20K/violation",
        "action_required": "Impact assessments for high-risk AI systems. Disclosure when AI used in consequential decisions. Compliance programs required.",
        "source_url": "https://www.dbllawyers.com/how-to-be-an-ai-compliant-business-in-2026/",
        "alpha_id": "ALPHA805",
    },
    {
        "id": "REG005",
        "regulation": "Virginia AI Act",
        "jurisdiction": "Virginia",
        "effective_date": "2026-01-01",
        "category": "AI_REGULATION",
        "impact": "MEDIUM",
        "status": "ACTIVE",
        "penalties": "$20K/violation",
        "action_required": "AI transparency requirements for businesses operating in VA. Similar to CO framework.",
        "source_url": "https://www.dbllawyers.com/how-to-be-an-ai-compliant-business-in-2026/",
        "alpha_id": "",
    },
    {
        "id": "REG006",
        "regulation": "Maryland AI Act",
        "jurisdiction": "Maryland",
        "effective_date": "2026-01-01",
        "category": "AI_REGULATION",
        "impact": "MEDIUM",
        "status": "ACTIVE",
        "penalties": "$20K/violation",
        "action_required": "AI transparency and disclosure requirements for MD businesses.",
        "source_url": "https://www.dbllawyers.com/how-to-be-an-ai-compliant-business-in-2026/",
        "alpha_id": "",
    },
    # --- UPCOMING (next 6 months) ---
    {
        "id": "REG007",
        "regulation": "CAN-SPAM: Enhanced Email Authentication",
        "jurisdiction": "United States (Federal)",
        "effective_date": "2026-02-01",
        "category": "EMAIL",
        "impact": "HIGH",
        "status": "ACTIVE",
        "penalties": "$51,744 per violation, domain blacklisting",
        "action_required": "SPF, DKIM, DMARC mandatory for all bulk senders. Google/Microsoft enforce stricter sender reputation. 2-week warmup from 5 emails/day.",
        "source_url": "https://support.google.com/mail/answer/81126",
        "alpha_id": "",
    },
    {
        "id": "REG008",
        "regulation": "South Korea AI Advertisement Labeling",
        "jurisdiction": "South Korea",
        "effective_date": "2026-03-01",
        "category": "AI_DISCLOSURE",
        "impact": "LOW",
        "status": "UPCOMING",
        "penalties": "TBD — Korean advertising authority enforcement",
        "action_required": "Clear AI identification in synthetic ads. Korea distribution = compliance needed.",
        "source_url": "https://www.netinfluencer.com/global-creator-economy-regulation-what-is-scheduled-for-2026/",
        "alpha_id": "ALPHA809",
    },
    {
        "id": "REG009",
        "regulation": "New York Synthetic Performers Disclosure Law",
        "jurisdiction": "New York",
        "effective_date": "2026-06-09",
        "category": "AI_DISCLOSURE",
        "impact": "CRITICAL",
        "status": "UPCOMING",
        "penalties": "$1,000 first offense, $5,000 subsequent",
        "action_required": "Clear and conspicuous disclosure of AI-generated performers in digital content. Label synthetic performers. Nationwide reach = compliance needed.",
        "source_url": "https://natlawreview.com/article/what-digital-marketers-need-know-about-new-yorks-new-ai-disclosure-law",
        "alpha_id": "ALPHA805",
    },
    {
        "id": "REG010",
        "regulation": "EU AI Act Article 50 (Transparency Obligations)",
        "jurisdiction": "European Union",
        "effective_date": "2026-08-02",
        "category": "AI_REGULATION",
        "impact": "CRITICAL",
        "status": "UPCOMING",
        "penalties": "EU fines (up to 3% global revenue or €15M) + platform restrictions",
        "action_required": "ALL AI-generated audio, images, video, text must be labeled in machine-readable format. Transparency obligations for all AI systems. Applies to any content distributed in EU.",
        "source_url": "https://www.ecija.com/en/news-and-insights/las-empresas-deberan-etiquetar-los-contenidos-generados-por-ia-a-partir-de-agosto-de-2026/",
        "alpha_id": "ALPHA806",
    },
    {
        "id": "REG011",
        "regulation": "California AI Transparency Act (AB853)",
        "jurisdiction": "California",
        "effective_date": "2026-08-02",
        "category": "AI_REGULATION",
        "impact": "CRITICAL",
        "status": "UPCOMING",
        "penalties": "State enforcement + platform restrictions",
        "action_required": "Latent + manifest disclosures in AI-generated content. Must make available AI-detection tool. Applies to California distribution.",
        "source_url": "https://www.mayerbrown.com/en/insights/publications/2025/10/new-obligations-under-the-california-ai-transparency-act-and-companion-chatbot-law-add-to-the-compliance-list",
        "alpha_id": "ALPHA810",
    },
    # --- BUSINESS DEADLINES ---
    {
        "id": "REG018",
        "regulation": "Ramadan 2026 App Launch Window",
        "jurisdiction": "Global (Muslim Markets)",
        "effective_date": "2026-02-28",
        "category": "BUSINESS",
        "impact": "CRITICAL",
        "status": "UPCOMING",
        "penalties": "Missed 10x app install window. Muslim Pro makes $30-50M ARR during Ramadan.",
        "action_required": "Deploy Hilal (Ramadan Tracker) app BEFORE Feb 28. Bilingual EN/AR, RTL ready at ralph/loops/app_factory/output/ramadan-tracker/.",
        "source_url": "",
        "alpha_id": "",
    },
    {
        "id": "REG019",
        "regulation": "Apple ASO Battery Optimization Ranking Factor",
        "jurisdiction": "Global (Apple Ecosystem)",
        "effective_date": "2026-03-01",
        "category": "PLATFORM",
        "impact": "HIGH",
        "status": "UPCOMING",
        "penalties": "App search ranking demotion for battery-heavy apps",
        "action_required": "Audit all 6 PWA apps for battery optimization. Battery consumption now affects App Store search rankings.",
        "source_url": "",
        "alpha_id": "",
    },
    {
        "id": "REG020",
        "regulation": "Google Core Update (March 2026)",
        "jurisdiction": "Global",
        "effective_date": "2026-03-15",
        "category": "SEO",
        "impact": "HIGH",
        "status": "UPCOMING",
        "penalties": "SEO ranking changes, possible traffic drops for thin/AI content",
        "action_required": "Audit 600 programmatic SEO pages for content quality. Ensure unique value on each page. Check for AI content flags.",
        "source_url": "",
        "alpha_id": "",
    },
    {
        "id": "REG021",
        "regulation": "Google Core Update (June 2026 - Helpful Content)",
        "jurisdiction": "Global",
        "effective_date": "2026-06-15",
        "category": "SEO",
        "impact": "MEDIUM",
        "status": "UPCOMING",
        "penalties": "Helpful Content refinement, possible ranking adjustments",
        "action_required": "Review all published content for helpfulness signals. Add unique data/insights to thin pages.",
        "source_url": "",
        "alpha_id": "",
    },
    # --- ONGOING COMPLIANCE ---
    {
        "id": "REG012",
        "regulation": "FTC Affiliate Disclosure Requirements",
        "jurisdiction": "United States (Federal)",
        "effective_date": "2024-01-01",
        "category": "FTC",
        "impact": "HIGH",
        "status": "ACTIVE",
        "penalties": "FTC enforcement actions, fines per violation",
        "action_required": "Clear and conspicuous affiliate link disclosure. No 'hidden' affiliate links. Disclosure must be near the recommendation, not buried in footer.",
        "source_url": "https://www.ftc.gov/legal-library/browse/rules/endorsement-guides",
        "alpha_id": "",
    },
    {
        "id": "REG013",
        "regulation": "GDPR (General Data Protection Regulation)",
        "jurisdiction": "European Union",
        "effective_date": "2018-05-25",
        "category": "PRIVACY",
        "impact": "HIGH",
        "status": "ACTIVE",
        "penalties": "Up to 4% global revenue or €20M",
        "action_required": "Cookie consent, privacy policy, data processing agreements, right to deletion. Applies if collecting EU user data (apps, websites, email lists).",
        "source_url": "https://gdpr.eu/",
        "alpha_id": "",
    },
    {
        "id": "REG014",
        "regulation": "CCPA/CPRA (California Consumer Privacy Act)",
        "jurisdiction": "California",
        "effective_date": "2023-01-01",
        "category": "PRIVACY",
        "impact": "HIGH",
        "status": "ACTIVE",
        "penalties": "$2,500/unintentional, $7,500/intentional violation",
        "action_required": "Privacy policy, opt-out of data sale, data access rights. Applies if 50K+ CA consumers, $25M+ revenue, or 50%+ revenue from selling data.",
        "source_url": "https://oag.ca.gov/privacy/ccpa",
        "alpha_id": "",
    },
    {
        "id": "REG015",
        "regulation": "COPPA (Children's Online Privacy Protection Act)",
        "jurisdiction": "United States (Federal)",
        "effective_date": "2000-04-21",
        "category": "PRIVACY",
        "impact": "HIGH",
        "status": "ACTIVE",
        "penalties": "$50,120 per violation (2024 rate)",
        "action_required": "No data collection from children under 13 without verifiable parental consent. Applies to apps/websites directed at children or that knowingly collect child data.",
        "source_url": "https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa",
        "alpha_id": "",
    },
    {
        "id": "REG016",
        "regulation": "Apple App Store Guidelines 4.7 (AI Apps)",
        "jurisdiction": "Global (Apple Ecosystem)",
        "effective_date": "2024-06-01",
        "category": "PLATFORM",
        "impact": "HIGH",
        "status": "ACTIVE",
        "penalties": "App rejection, removal from App Store",
        "action_required": "AI-generated content must be moderated. No deepfakes. Content filters required. Privacy manifests (PrivacyInfo.xcprivacy). User-generated AI content must have reporting mechanism.",
        "source_url": "https://developer.apple.com/app-store/review/guidelines/",
        "alpha_id": "",
    },
    {
        "id": "REG017",
        "regulation": "EU Digital Services Act (DSA)",
        "jurisdiction": "European Union",
        "effective_date": "2024-02-17",
        "category": "PLATFORM",
        "impact": "MEDIUM",
        "status": "ACTIVE",
        "penalties": "Up to 6% global turnover",
        "action_required": "Transparency reports, content moderation, advertising transparency. Applies to platforms with EU users.",
        "source_url": "https://digital-strategy.ec.europa.eu/en/policies/digital-services-act-package",
        "alpha_id": "",
    },
]

# ============================================================
# NEWS SOURCES TO SCAN FOR NEW REGULATIONS
# ============================================================
REGULATION_NEWS_FEEDS = [
    {"name": "FTC Press Releases", "url": "https://www.ftc.gov/news-events/news/press-releases/feed", "type": "rss"},
    {"name": "NetInfluencer Regulation", "url": "https://www.netinfluencer.com/category/regulation/feed/", "type": "rss"},
    {"name": "National Law Review AI", "url": "https://natlawreview.com/topic/artificial-intelligence-ai/feed", "type": "rss"},
]

REGULATION_KEYWORDS = [
    "AI disclosure", "synthetic media", "deepfake", "AI transparency",
    "AI regulation", "content labeling", "AI act", "FTC enforcement",
    "influencer disclosure", "affiliate disclosure", "CAN-SPAM",
    "COPPA", "CCPA", "GDPR enforcement", "AI compliance",
    "digital services act", "platform regulation",
]


def days_until(date_str):
    """Calculate days from today to a date string."""
    try:
        target = datetime.strptime(date_str, "%Y-%m-%d")
        delta = target - datetime.now()
        return delta.days
    except (ValueError, TypeError):
        return None


def urgency_color(days):
    """Color code by urgency."""
    if days is None:
        return W
    if days < 0:
        return G  # past = active
    if days <= 30:
        return R  # red = imminent
    if days <= 90:
        return Y  # yellow = upcoming
    return B  # blue = future


def urgency_label(days):
    """Human label for urgency."""
    if days is None:
        return "ONGOING"
    if days < 0:
        return f"ACTIVE ({abs(days)}d ago)"
    if days == 0:
        return "TODAY"
    if days <= 7:
        return f"THIS WEEK ({days}d)"
    if days <= 30:
        return f"THIS MONTH ({days}d)"
    if days <= 90:
        return f"NEXT 90 DAYS ({days}d)"
    return f"IN {days} DAYS"


def check_all_deadlines(upcoming_only=False, days_limit=90):
    """Display all compliance deadlines with urgency indicators."""
    today = datetime.now()
    print(f"\n{BOLD}{W}{'='*70}")
    print(f"  PRINTMAXX COMPLIANCE DEADLINE TRACKER")
    print(f"  {today.strftime('%Y-%m-%d %H:%M')} | {len(DEADLINES)} regulations tracked")
    print(f"{'='*70}{D}\n")

    # Sort by effective date
    sorted_deadlines = sorted(DEADLINES, key=lambda d: d["effective_date"])

    # Group by urgency
    critical_now = []
    upcoming = []
    future = []

    for dl in sorted_deadlines:
        days = days_until(dl["effective_date"])
        if days is not None and days < 0:
            critical_now.append((dl, days))
        elif days is not None and days <= days_limit:
            upcoming.append((dl, days))
        elif not upcoming_only:
            future.append((dl, days))

    # --- ACTIVE NOW ---
    if critical_now:
        print(f"{BOLD}{R}  ACTIVE NOW ({len(critical_now)} regulations in effect){D}")
        print(f"  {'-'*66}")
        for dl, days in critical_now:
            impact_c = R if dl["impact"] == "CRITICAL" else Y if dl["impact"] == "HIGH" else W
            print(f"  {G}[{dl['id']}]{D} {BOLD}{dl['regulation']}{D}")
            print(f"    Jurisdiction: {dl['jurisdiction']}")
            print(f"    Impact: {impact_c}{dl['impact']}{D} | Status: {G}ACTIVE{D}")
            print(f"    Penalties: {Y}{dl['penalties']}{D}")
            print(f"    Action: {dl['action_required'][:120]}")
            print()

    # --- UPCOMING ---
    if upcoming:
        print(f"\n{BOLD}{Y}  UPCOMING ({len(upcoming)} deadlines in next {days_limit} days){D}")
        print(f"  {'-'*66}")
        for dl, days in upcoming:
            uc = urgency_color(days)
            impact_c = R if dl["impact"] == "CRITICAL" else Y if dl["impact"] == "HIGH" else W
            print(f"  {uc}[{dl['id']}]{D} {BOLD}{dl['regulation']}{D}")
            print(f"    Deadline: {uc}{dl['effective_date']} ({urgency_label(days)}){D}")
            print(f"    Jurisdiction: {dl['jurisdiction']}")
            print(f"    Impact: {impact_c}{dl['impact']}{D}")
            print(f"    Penalties: {Y}{dl['penalties']}{D}")
            print(f"    Action: {dl['action_required'][:120]}")
            print()

    # --- FUTURE ---
    if future and not upcoming_only:
        print(f"\n{BOLD}{B}  FUTURE ({len(future)} longer-term regulations){D}")
        print(f"  {'-'*66}")
        for dl, days in future:
            label = urgency_label(days)
            print(f"  {B}[{dl['id']}]{D} {dl['regulation']} — {dl['jurisdiction']} — {label}")

    # --- SUMMARY ---
    critical_count = sum(1 for dl in DEADLINES if dl["impact"] == "CRITICAL")
    active_count = sum(1 for dl in DEADLINES if dl["status"] == "ACTIVE")
    upcoming_count = sum(1 for dl in DEADLINES if dl["status"] == "UPCOMING")
    next_deadline = None
    for dl in sorted_deadlines:
        days = days_until(dl["effective_date"])
        if days is not None and days > 0:
            next_deadline = (dl, days)
            break

    print(f"\n{BOLD}{W}  SUMMARY{D}")
    print(f"  {'-'*66}")
    print(f"  Total regulations tracked: {len(DEADLINES)}")
    print(f"  CRITICAL impact: {R}{critical_count}{D}")
    print(f"  Currently active: {G}{active_count}{D}")
    print(f"  Upcoming: {Y}{upcoming_count}{D}")
    if next_deadline:
        nd, nd_days = next_deadline
        print(f"  Next deadline: {Y}{nd['regulation']}{D} in {R}{nd_days} days{D} ({nd['effective_date']})")
    print()

    return sorted_deadlines


def scan_for_new_regulations():
    """Scrape RSS feeds for new regulatory developments."""
    if not requests:
        print(f"{R}ERROR: requests library not available{D}")
        return []

    print(f"\n{BOLD}Scanning {len(REGULATION_NEWS_FEEDS)} regulation news feeds...{D}\n")
    findings = []

    for feed in REGULATION_NEWS_FEEDS:
        try:
            headers = {"User-Agent": "PRINTMAXX-ComplianceBot/1.0"}
            resp = requests.get(feed["url"], headers=headers, timeout=15)
            if resp.status_code != 200:
                print(f"  {Y}[SKIP]{D} {feed['name']} — HTTP {resp.status_code}")
                continue

            # Parse RSS items
            items = re.findall(r'<item>(.*?)</item>', resp.text, re.DOTALL)
            matched = 0
            for item in items[:20]:
                title_m = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
                link_m = re.search(r'<link>(.*?)</link>', item, re.DOTALL)
                pubdate_m = re.search(r'<pubDate>(.*?)</pubDate>', item, re.DOTALL)

                if not title_m:
                    continue
                title = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', title_m.group(1)).strip()
                link = link_m.group(1).strip() if link_m else ""
                pubdate = pubdate_m.group(1).strip() if pubdate_m else ""

                # Check against regulation keywords
                title_lower = title.lower()
                matching_kw = [kw for kw in REGULATION_KEYWORDS if kw.lower() in title_lower]
                if matching_kw:
                    findings.append({
                        "source": feed["name"],
                        "title": title,
                        "url": link,
                        "date": pubdate,
                        "keywords": matching_kw,
                    })
                    matched += 1

            print(f"  {G}[OK]{D} {feed['name']} — {len(items)} items, {matched} regulation matches")

        except Exception as e:
            print(f"  {R}[ERR]{D} {feed['name']} — {str(e)[:60]}")

    if findings:
        print(f"\n{BOLD}{Y}  {len(findings)} NEW REGULATION SIGNALS FOUND:{D}\n")
        for i, f in enumerate(findings, 1):
            print(f"  {i}. [{f['source']}] {f['title']}")
            print(f"     Keywords: {', '.join(f['keywords'])}")
            print(f"     URL: {f['url']}")
            print()

        # Append to ALPHA_STAGING.csv
        appended = append_findings_to_alpha(findings)
        if appended > 0:
            print(f"  {G}Appended {appended} new entries to ALPHA_STAGING.csv{D}")
    else:
        print(f"\n  {G}No new regulation signals found.{D}")

    return findings


def append_findings_to_alpha(findings):
    """Append regulation findings to ALPHA_STAGING.csv."""
    if not ALPHA_CSV.exists():
        return 0

    # Get next ALPHA ID
    existing_ids = set()
    try:
        with open(ALPHA_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                aid = row.get("alpha_id", "")
                m = re.match(r'ALPHA(\d+)', aid)
                if m:
                    existing_ids.add(int(m.group(1)))
    except Exception:
        pass

    next_id = max(existing_ids, default=10000) + 1
    appended = 0

    # Check for duplicates by URL
    existing_urls = set()
    try:
        with open(ALPHA_CSV, 'r') as f:
            for line in f:
                for finding in findings:
                    if finding["url"] in line:
                        existing_urls.add(finding["url"])
    except Exception:
        pass

    try:
        with open(ALPHA_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            for finding in findings:
                if finding["url"] in existing_urls:
                    continue
                alpha_id = f"ALPHA{next_id}"
                next_id += 1
                writer.writerow([
                    alpha_id,
                    finding["source"],
                    finding["url"],
                    "COMPLIANCE",
                    finding["title"],
                    "HIGH",
                    "NOW",
                    "PENDING_REVIEW",
                    "",
                    "ALL",
                    75,
                    f"Regulation signal: {', '.join(finding['keywords'])}",
                    "None",
                    "N/A",
                    "N/A",
                    finding["title"],
                    "None",
                    datetime.now().strftime("%Y-%m-%d"),
                ])
                appended += 1
    except Exception as e:
        print(f"  {R}Error appending to ALPHA_STAGING: {e}{D}")

    return appended


def save_deadline_csv():
    """Save all deadlines to CSV for quant terminal integration."""
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)

    with open(DEADLINE_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "id", "regulation", "jurisdiction", "effective_date", "category",
            "impact", "status", "days_remaining", "urgency", "penalties",
            "action_required", "source_url", "alpha_id"
        ])
        for dl in sorted(DEADLINES, key=lambda d: d["effective_date"]):
            days = days_until(dl["effective_date"])
            writer.writerow([
                dl["id"], dl["regulation"], dl["jurisdiction"],
                dl["effective_date"], dl["category"], dl["impact"],
                dl["status"], days if days is not None else "N/A",
                urgency_label(days), dl["penalties"],
                dl["action_required"], dl["source_url"], dl.get("alpha_id", "")
            ])

    print(f"  {G}Saved {len(DEADLINES)} deadlines to {DEADLINE_CSV}{D}")


def generate_digest():
    """Generate compliance digest at OPS/COMPLIANCE_DEADLINE_DIGEST_*.md."""
    today = datetime.now()
    digest_path = OPS_DIR / f"COMPLIANCE_DEADLINE_DIGEST_{today.strftime('%Y_%m_%d')}.md"

    sorted_deadlines = sorted(DEADLINES, key=lambda d: d["effective_date"])

    lines = [
        f"# Compliance Deadline Digest",
        f"",
        f"Generated: {today.strftime('%Y-%m-%d %H:%M:%S')}",
        f"",
        f"Total regulations tracked: {len(DEADLINES)}",
        f"",
        f"---",
        f"",
    ]

    # Active Now
    active = [(dl, days_until(dl["effective_date"])) for dl in sorted_deadlines
              if days_until(dl["effective_date"]) is not None and days_until(dl["effective_date"]) < 0]
    if active:
        lines.append(f"## ACTIVE NOW ({len(active)} regulations in effect)")
        lines.append("")
        for dl, days in active:
            lines.append(f"### [{dl['id']}] {dl['regulation']}")
            lines.append(f"- **Jurisdiction:** {dl['jurisdiction']}")
            lines.append(f"- **Impact:** {dl['impact']}")
            lines.append(f"- **In effect since:** {dl['effective_date']}")
            lines.append(f"- **Penalties:** {dl['penalties']}")
            lines.append(f"- **Action required:** {dl['action_required']}")
            lines.append(f"- **Source:** {dl['source_url']}")
            lines.append("")

    # Upcoming (next 180 days)
    upcoming = [(dl, days_until(dl["effective_date"])) for dl in sorted_deadlines
                if days_until(dl["effective_date"]) is not None and 0 <= days_until(dl["effective_date"]) <= 180]
    if upcoming:
        lines.append(f"## UPCOMING ({len(upcoming)} deadlines in next 6 months)")
        lines.append("")
        lines.append(f"| Days | Regulation | Jurisdiction | Impact | Date |")
        lines.append(f"|------|-----------|-------------|--------|------|")
        for dl, days in upcoming:
            urgency = "**IMMINENT**" if days <= 30 else "SOON" if days <= 90 else ""
            lines.append(f"| {days} {urgency} | {dl['regulation']} | {dl['jurisdiction']} | {dl['impact']} | {dl['effective_date']} |")
        lines.append("")

    # Action items
    lines.append(f"## Recommended Actions")
    lines.append("")
    critical_upcoming = [dl for dl, d in upcoming if dl["impact"] == "CRITICAL" and d is not None and d <= 180]
    for i, dl in enumerate(critical_upcoming, 1):
        days = days_until(dl["effective_date"])
        lines.append(f"{i}. **{dl['regulation']}** ({days}d) — {dl['action_required'][:100]}")
    if not critical_upcoming:
        lines.append("No critical upcoming deadlines in the next 180 days.")
    lines.append("")

    # Category breakdown
    categories = {}
    for dl in DEADLINES:
        cat = dl["category"]
        categories[cat] = categories.get(cat, 0) + 1
    lines.append(f"## Category Breakdown")
    lines.append("")
    lines.append(f"| Category | Count |")
    lines.append(f"|----------|-------|")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        lines.append(f"| {cat} | {count} |")

    content = "\n".join(lines)

    with open(digest_path, 'w') as f:
        f.write(content)

    print(f"  {G}Digest saved to {digest_path}{D}")
    return digest_path


def quick_status():
    """One-line status for cron/dashboard integration."""
    active_count = sum(1 for dl in DEADLINES if dl["status"] == "ACTIVE")
    upcoming_count = sum(1 for dl in DEADLINES if dl["status"] == "UPCOMING")
    critical_count = sum(1 for dl in DEADLINES if dl["impact"] == "CRITICAL")

    # Find next deadline
    next_dl = None
    for dl in sorted(DEADLINES, key=lambda d: d["effective_date"]):
        days = days_until(dl["effective_date"])
        if days is not None and days > 0:
            next_dl = (dl, days)
            break

    next_str = f"next: {next_dl[0]['regulation']} in {next_dl[1]}d" if next_dl else "no upcoming"
    print(f"[Compliance: {len(DEADLINES)} tracked | {active_count} active | {upcoming_count} upcoming | {critical_count} CRITICAL | {next_str}]")


def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Compliance Deadline Tracker")
    parser.add_argument("--check", action="store_true", help="Show all deadlines with urgency indicators")
    parser.add_argument("--upcoming", action="store_true", help="Show only upcoming deadlines (next 90 days)")
    parser.add_argument("--scan", action="store_true", help="Scrape news feeds for new regulations")
    parser.add_argument("--digest", action="store_true", help="Generate OPS/ compliance digest")
    parser.add_argument("--status", action="store_true", help="Quick one-line status")
    parser.add_argument("--days", type=int, default=90, help="Days ahead to check (default: 90)")
    parser.add_argument("--save-csv", action="store_true", help="Save deadlines to LEDGER CSV")

    args = parser.parse_args()

    if not any([args.check, args.upcoming, args.scan, args.digest, args.status, args.save_csv]):
        args.check = True  # Default

    if args.status:
        quick_status()
        return

    if args.check:
        check_all_deadlines(upcoming_only=False, days_limit=args.days)
        save_deadline_csv()

    if args.upcoming:
        check_all_deadlines(upcoming_only=True, days_limit=args.days)

    if args.scan:
        scan_for_new_regulations()

    if args.digest:
        generate_digest()
        save_deadline_csv()

    if args.save_csv:
        save_deadline_csv()


if __name__ == "__main__":
    main()
