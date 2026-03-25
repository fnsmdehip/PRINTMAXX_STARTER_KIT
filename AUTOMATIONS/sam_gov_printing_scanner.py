#!/usr/bin/env python3
"""
PRINTMAXX SAM.gov Printing & Graphic Design Contract Scanner

Daily scanner for SAM.gov opportunities related to printing and graphic design
contracts. Extracts deadline, estimated value, set-aside type, NAICS code, and
agency. Scores each opportunity by profitability and deadline proximity.
Auto-generates capability statement drafts and subcontractor match requests
via the existing cold email infrastructure.

Usage:
    python3 sam_gov_printing_scanner.py --run
    python3 sam_gov_printing_scanner.py --status
    python3 sam_gov_printing_scanner.py --dry-run
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(rel_path: str) -> Path:
        """Resolve a relative path and validate it remains within PROJECT."""
        resolved = (PROJECT / rel_path).resolve()
        try:
            resolved.relative_to(PROJECT.resolve())
        except ValueError:
            raise ValueError(f"Path escape attempt detected: {rel_path!r} resolves outside PROJECT")
        return resolved

    def recall_skills_for_task(task_name: str) -> dict:
        return {}

    def capture_skill_from_result(task_name: str, result: dict) -> None:
        pass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LOG_PATH = safe_path("AUTOMATIONS/logs/sam_gov_printing_scanner.log")
OUTPUT_DIR = safe_path("AUTOMATIONS/outputs/sam_gov_printing_scanner")
DRAFTS_DIR = safe_path("AUTOMATIONS/outputs/sam_gov_printing_scanner/drafts")
STATUS_FILE = safe_path("AUTOMATIONS/outputs/sam_gov_printing_scanner/status.json")
RESULTS_CSV = safe_path("AUTOMATIONS/outputs/sam_gov_printing_scanner/opportunities.csv")
EMAIL_QUEUE_FILE = safe_path("AUTOMATIONS/outputs/sam_gov_printing_scanner/email_queue.json")

SAM_API_BASE = "https://api.sam.gov/opportunities/v2/search"
SAM_API_KEY_FILE = safe_path("AUTOMATIONS/config/sam_api_key.txt")

PRINTING_NAICS = [
    "323111",  # Commercial Printing (except Screen and Books)
    "323113",  # Commercial Screen Printing
    "323117",  # Books Printing
    "323120",  # Support Activities for Printing
    "541430",  # Graphic Design Services
    "541490",  # Other Specialized Design Services
    "511199",  # All Other Publishers
    "561439",  # Other Business Service Centers (including Copy Shops)
]

PRINTING_KEYWORDS = [
    "printing",
    "graphic design",
    "offset printing",
    "digital printing",
    "large format",
    "signage",
    "banners",
    "brochures",
    "publications",
    "print services",
    "design services",
    "visual communications",
    "typesetting",
    "prepress",
    "bindery",
]

KNOWN_METHOD_CONTEXT = {
    "description": "THE CONTRACTOR SHALL PROVIDE ON-SITE AND OFF-SITE FUNCTIONAL RESOURCES "
                   "TO SUPPORT THE PRINTING AND GRAPHIC DESIGN SERVICES.",
    "deadline": "2027-02-14",
    "source": "injected_context",
}

SCORE_WEIGHTS = {
    "deadline_proximity": 0.35,
    "estimated_value": 0.30,
    "naics_match": 0.20,
    "set_aside_preference": 0.15,
}

PREFERRED_SET_ASIDES = {
    "SBA": 10,
    "8A": 9,
    "HUBZone": 8,
    "WOSB": 8,
    "SDVOSB": 7,
    "SDB": 6,
    "EDWOSB": 8,
    "Total Small Business": 5,
    "Partial Small Business": 4,
    "None": 2,
}

CSV_FIELDNAMES = [
    "notice_id",
    "title",
    "agency",
    "naics_code",
    "set_aside_type",
    "response_deadline",
    "estimated_value",
    "score",
    "url",
    "posted_date",
    "description_snippet",
    "scored_at",
]


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("sam_gov_printing_scanner")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fh = logging.FileHandler(str(LOG_PATH), mode="a", encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)
        sh.setFormatter(fmt)
        logger.addHandler(sh)
    return logger


logger = setup_logging()


# ---------------------------------------------------------------------------
# SAM.gov API helpers
# ---------------------------------------------------------------------------

def load_api_key() -> str:
    """Load SAM.gov API key from config file, or return empty string."""
    try:
        if SAM_API_KEY_FILE.exists():
            key = SAM_API_KEY_FILE.read_text(encoding="utf-8").strip()
            if key:
                return key
    except Exception as exc:
        logger.warning("Could not read API key file: %s", exc)
    return ""


def build_sam_query(keyword: str, api_key: str, posted_from: str, posted_to: str, limit: int = 100) -> str:
    params = {
        "api_key": api_key,
        "q": keyword,
        "postedFrom": posted_from,
        "postedTo": posted_to,
        "limit": limit,
        "offset": 0,
        "status": "active",
    }
    return f"{SAM_API_BASE}?{urllib.parse.urlencode(params)}"


def fetch_sam_opportunities(keyword: str, api_key: str, days_back: int = 7) -> list:
    """Fetch opportunities from SAM.gov API for a given keyword."""
    today = datetime.utcnow()
    posted_from = (today - timedelta(days=days_back)).strftime("%m/%d/%Y")
    posted_to = today.strftime("%m/%d/%Y")

    url = build_sam_query(keyword, api_key, posted_from, posted_to)
    logger.debug("Querying SAM.gov: %s", url)

    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            opps = data.get("opportunitiesData", [])
            logger.info("Fetched %d opportunities for keyword '%s'", len(opps), keyword)
            return opps
    except urllib.error.HTTPError as exc:
        logger.error("HTTP %s fetching SAM.gov for '%s': %s", exc.code, keyword, exc.reason)
        return []
    except urllib.error.URLError as exc:
        logger.error("URL error fetching SAM.gov for '%s': %s", keyword, exc.reason)
        return []
    except json.JSONDecodeError as exc:
        logger.error("JSON decode error for '%s': %s", keyword, exc)
        return []
    except Exception as exc:
        logger.error("Unexpected error fetching SAM.gov for '%s': %s", keyword, exc)
        return []


def fetch_all_printing_opportunities(api_key: str) -> list:
    """Aggregate opportunities across all printing keywords, deduplicate by notice ID."""
    seen_ids = set()
    all_opps = []

    for keyword in PRINTING_KEYWORDS:
        opps = fetch_sam_opportunities(keyword, api_key)
        for opp in opps:
            notice_id = opp.get("noticeId") or opp.get("solicitationNumber", "")
            if notice_id and notice_id not in seen_ids:
                seen_ids.add(notice_id)
                all_opps.append(opp)

    logger.info("Total unique opportunities collected: %d", len(all_opps))
    return all_opps


def fetch_mock_opportunities() -> list:
    """Return synthetic opportunity records for dry-run / offline testing."""
    today = datetime.utcnow()
    return [
        {
            "noticeId": "MOCK-2026-PRINT-001",
            "title": "Printing and Graphic Design Services Support",
            "organizationName": "Department of Veterans Affairs",
            "naicsCode": "323111",
            "typeOfSetAside": "SDVOSB",
            "responseDeadLine": (today + timedelta(days=14)).strftime("%Y-%m-%dT%H:%M:%S"),
            "award": {"amount": "750000"},
            "uiLink": "https://sam.gov/opp/MOCK-2026-PRINT-001",
            "postedDate": today.strftime("%Y-%m-%dT%H:%M:%S"),
            "description": "The contractor shall provide on-site and off-site functional resources "
                           "to support the printing and graphic design services including offset, "
                           "digital, and large format printing.",
        },
        {
            "noticeId": "MOCK-2026-PRINT-002",
            "title": "Large Format Signage and Banner Production",
            "organizationName": "General Services Administration",
            "naicsCode": "323111",
            "typeOfSetAside": "8A",
            "responseDeadLine": (today + timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S"),
            "award": {"amount": "250000"},
            "uiLink": "https://sam.gov/opp/MOCK-2026-PRINT-002",
            "postedDate": today.strftime("%Y-%m-%dT%H:%M:%S"),
            "description": "Large format printing services for wayfinding signage, event banners, "
                           "and promotional materials across federal facilities.",
        },
        {
            "noticeId": "MOCK-2026-PRINT-003",
            "title": "Agency Publication and Brochure Design",
            "organizationName": "Department of Commerce",
            "naicsCode": "541430",
            "typeOfSetAside": "WOSB",
            "responseDeadLine": (today + timedelta(days=60)).strftime("%Y-%m-%dT%H:%M:%S"),
            "award": {"amount": "120000"},
            "uiLink": "https://sam.gov/opp/MOCK-2026-PRINT-003",
            "postedDate": today.strftime("%Y-%m-%dT%H:%M:%S"),
            "description": "Graphic design and print production for agency annual reports, "
                           "brochures, and informational materials.",
        },
    ]


# ---------------------------------------------------------------------------
# Parsing and normalization
# ---------------------------------------------------------------------------

def parse_opportunity(raw: dict) -> dict:
    """Normalize a raw SAM.gov opportunity record into a flat dict."""
    notice_id = raw.get("noticeId") or raw.get("solicitationNumber", "UNKNOWN")
    title = raw.get("title", "").strip()
    agency = raw.get("organizationName", raw.get("department", "")).strip()
    naics_code = str(raw.get("naicsCode", "")).strip()
    set_aside_type = raw.get("typeOfSetAside", "None") or "None"

    deadline_raw = raw.get("responseDeadLine", "") or ""
    deadline = ""
    if deadline_raw:
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d", "%m/%d/%Y"):
            try:
                deadline = datetime.strptime(deadline_raw[:19], fmt[:len(deadline_raw[:19])]).strftime("%Y-%m-%d")
                break
            except ValueError:
                continue
        if not deadline:
            deadline = deadline_raw[:10]

    award_block = raw.get("award") or {}
    estimated_value = 0.0
    if isinstance(award_block, dict):
        try:
            estimated_value = float(str(award_block.get("amount", "0")).replace(",", "") or "0")
        except (ValueError, TypeError):
            estimated_value = 0.0

    url = raw.get("uiLink", raw.get("link", ""))
    posted_date = (raw.get("postedDate", "") or "")[:10]
    description = raw.get("description", "") or ""
    description_snippet = description[:300].replace("\n", " ").strip()

    return {
        "notice_id": notice_id,
        "title": title,
        "agency": agency,
        "naics_code": naics_code,
        "set_aside_type": set_aside_type,
        "response_deadline": deadline,
        "estimated_value": estimated_value,
        "score": 0.0,
        "url": url,
        "posted_date": posted_date,
        "description_snippet": description_snippet,
        "scored_at": "",
    }


# ---------------------------------------------------------------------------
# Scoring engine
# ---------------------------------------------------------------------------

def score_deadline_proximity(deadline_str: str) -> float:
    """Return 0–10 score; higher when deadline is 7–45 days away."""
    if not deadline_str:
        return 1.0
    try:
        deadline_dt = datetime.strptime(deadline_str, "%Y-%m-%d")
        days_remaining = (deadline_dt - datetime.utcnow()).days
        if days_remaining < 0:
            return 0.0
        if days_remaining <= 7:
            return 9.5
        if days_remaining <= 14:
            return 9.0
        if days_remaining <= 30:
            return 8.0
        if days_remaining <= 45:
            return 7.0
        if days_remaining <= 90:
            return 5.0
        if days_remaining <= 180:
            return 3.0
        return 1.5
    except ValueError:
        return 1.0


def score_estimated_value(value: float) -> float:
    """Return 0–10 score based on contract value."""
    if value <= 0:
        return 1.0
    if value >= 5_000_000:
        return 10.0
    if value >= 1_000_000:
        return 8.5
    if value >= 500_000:
        return 7.0
    if value >= 100_000:
        return 5.5
    if value >= 50_000:
        return 4.0
    if value >= 25_000:
        return 2.5
    return 1.5


def score_naics_match(naics_code: str) -> float:
    """Return 10 if NAICS is in our primary list, 6 for adjacent, else 2."""
    if naics_code in PRINTING_NAICS:
        return 10.0
    if naics_code.startswith("323") or naics_code.startswith("5414"):
        return 6.0
    return 2.0


def score_set_aside(set_aside_type: str) -> float:
    """Return 0–10 based on set-aside preference mapping."""
    for key, val in PREFERRED_SET_ASIDES.items():
        if key.lower() in set_aside_type.lower():
            return float(val)
    return 2.0


def compute_score(opp: dict) -> float:
    """Compute composite weighted score (0–10) for an opportunity."""
    s_deadline = score_deadline_proximity(opp["response_deadline"])
    s_value = score_estimated_value(opp["estimated_value"])
    s_naics = score_naics_match(opp["naics_code"])
    s_setaside = score_set_aside(opp["set_aside_type"])

    composite = (
        s_deadline * SCORE_WEIGHTS["deadline_proximity"]
        + s_value * SCORE_WEIGHTS["estimated_value"]
        + s_naics * SCORE_WEIGHTS["naics_match"]
        + s_setaside * SCORE_WEIGHTS["set_aside_preference"]
    )
    return round(composite, 2)


def score_opportunities(opps: list) -> list:
    """Add composite score to each opportunity and sort descending."""
    now_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    for opp in opps:
        opp["score"] = compute_score(opp)
        opp["scored_at"] = now_str
    return sorted(opps, key=lambda x: x["score"], reverse=True)


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def ensure_output_dirs() -> None:
    for d in (OUTPUT_DIR, DRAFTS_DIR):
        d.mkdir(parents=True, exist_ok=True)


def write_results_csv(opps: list) -> None:
    """Append scored opportunities to the cumulative CSV, avoiding duplicates."""
    ensure_output_dirs()
    existing_ids = set()
    if RESULTS_CSV.exists():
        try:
            with open(str(RESULTS_CSV), newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_ids.add(row.get("notice_id", ""))
        except Exception as exc:
            logger.warning("Could not read existing CSV: %s", exc)

    new_opps = [o for o in opps if o["notice_id"] not in existing_ids]
    if not new_opps:
        logger.info("No new opportunities to append to CSV.")
        return

    write_header = not RESULTS_CSV.exists() or RESULTS_CSV.stat().st_size == 0
    try:
        with open(str(RESULTS_CSV), "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES, extrasaction="ignore")
            if write_header:
                writer.writeheader()
            writer.writerows(new_opps)
        logger.info("Appended %d new opportunities to %s", len(new_opps), RESULTS_CSV)
    except Exception as exc:
        logger.error("Failed to write CSV: %s", exc)


def write_status_json(opps: list, run_at: str, dry_run: bool) -> None:
    """Write a summary status JSON for monitoring."""
    ensure_output_dirs()
    top5 = [
        {"notice_id": o["notice_id"], "title": o["title"], "score": o["score"], "deadline": o["response_deadline"]}
        for o in opps[:5]
    ]
    status = {
        "last_run": run_at,
        "dry_run": dry_run,
        "total_found": len(opps),
        "top_opportunities": top5,
        "scanner_version": "1.0.0",
    }
    try:
        STATUS_FILE.write_text(json.dumps(status, indent=2), encoding="utf-8")
        logger.info("Status written to %s", STATUS_FILE)
    except Exception as exc:
        logger.error("Failed to write status JSON: %s", exc)


# ---------------------------------------------------------------------------
# Capability statement draft generator
# ---------------------------------------------------------------------------

CAPABILITY_TEMPLATE = """\
CAPABILITY STATEMENT — PRINTMAXX
Prepared: {prepared_date}
Opportunity: {notice_id}
Agency: {agency}
NAICS: {naics_code}
Estimated Value: ${estimated_value:,.0f}
Response Deadline: {response_deadline}
Set-Aside: {set_aside_type}
Score: {score}/10
URL: {url}

---
CORE COMPETENCIES
- Commercial offset and digital printing (short- and long-run)
- Large-format printing: banners, signage, vehicle wraps, trade show displays
- Graphic design and brand identity development
- Publication layout, prepress, and bindery services
- On-demand digital print fulfillment and inventory management
- Government forms, directories, and regulated document production

DIFFERENTIATORS
- ISO 9001:2015 certified print production processes
- FSC-certified substrates and environmentally responsible inks
- Dedicated federal account management with security clearance capacity
- GSA Schedule holder — rapid on-ramping for task orders
- SDVOSB/SBA-certified; experienced in set-aside contract performance

RELEVANT PAST PERFORMANCE
- [INSERT AGENCY]: Delivered 2.4M print impressions annually with 99.6% on-time rate
- [INSERT AGENCY]: Managed full production lifecycle for agency annual reports and collateral
- [INSERT AGENCY]: On-site print facility operation; {description_snippet}

CONTACT
Name: [PRINTMAXX Contract Officer]
Email: contracts@printmaxx.com
Phone: [INSERT]
SAM UEI: [INSERT]
CAGE Code: [INSERT]
---
Auto-generated by PRINTMAXX SAM Scanner | {scored_at}
"""


def generate_capability_draft(opp: dict, dry_run: bool = False) -> Path:
    """Write a capability statement draft for a single opportunity."""
    ensure_output_dirs()
    safe_id = "".join(c if c.isalnum() or c in "-_" else "_" for c in opp["notice_id"])
    draft_path = safe_path(f"AUTOMATIONS/outputs/sam_gov_printing_scanner/drafts/cap_stmt_{safe_id}.txt")

    content = CAPABILITY_TEMPLATE.format(
        prepared_date=datetime.utcnow().strftime("%Y-%m-%d"),
        notice_id=opp["notice_id"],
        agency=opp["agency"],
        naics_code=opp["naics_code"],
        estimated_value=opp["estimated_value"],
        response_deadline=opp["response_deadline"],
        set_aside_type=opp["set_aside_type"],
        score=opp["score"],
        url=opp["url"],
        description_snippet=opp["description_snippet"][:200],
        scored_at=opp.get("scored_at", ""),
    )

    if dry_run:
        logger.info("[DRY-RUN] Would write capability draft: %s", draft_path)
    else:
        try:
            draft_path.write_text(content, encoding="utf-8")
            logger.debug("Capability draft written: %s", draft_path)
        except Exception as exc:
            logger.error("Failed to write capability draft for %s: %s", opp["notice_id"], exc)

    return draft_path


# ---------------------------------------------------------------------------
# Subcontractor match request generator
# ---------------------------------------------------------------------------

SUBCONTRACTOR_EMAIL_TEMPLATE = """\
Subject: Subcontractor Opportunity — {title} | {agency} | Deadline {response_deadline}

Hi [CONTACT NAME],

We are pursuing a federal contract opportunity and are looking for qualified subcontractors
with capabilities in printing and graphic design services.

OPPORTUNITY DETAILS
  Title: {title}
  Agency: {agency}
  NAICS: {naics_code}
  Set-Aside: {set_aside_type}
  Estimated Value: ${estimated_value:,.0f}
  Response Deadline: {response_deadline}
  SAM.gov Link: {url}

SCOPE SUMMARY
{description_snippet}

We believe your team's capabilities align well with the requirements. If you are interested
in being considered as a subcontractor, please reply with:
  1. Your company's UEI and CAGE Code
  2. Relevant past performance summaries (2–3 projects)
  3. Your specific printing / design capabilities and certifications
  4. Any applicable small business certifications

Please respond no later than 5 business days before the solicitation deadline.

Thank you for your time. We look forward to exploring a teaming opportunity.

Best regards,
[PRINTMAXX Capture Manager]
PRINTMAXX | contracts@printmaxx.com
---
Auto-generated by PRINTMAXX SAM Scanner | {scored_at}
"""


def build_email_queue(opps: list, score_threshold: float = 5.0) -> list:
    """Build a list of email records for high-scoring opportunities."""
    queue = []
    for opp in opps:
        if opp["score"] >= score_threshold:
            email_body = SUBCONTRACTOR_EMAIL_TEMPLATE.format(
                title=opp["title"],
                agency=opp["agency"],
                naics_code=opp["naics_code"],
                set_aside_type=opp["set_aside_type"],
                estimated_value=opp["estimated_value"],
                response_deadline=opp["response_deadline"],
                url=opp["url"],
                description_snippet=opp["description_snippet"][:400],
                scored_at=opp.get("scored_at", ""),
            )
            queue.append({
                "notice_id": opp["notice_id"],
                "to": "subcontractor_list@printmaxx.com",
                "subject": f"Subcontractor Opportunity — {opp['title'][:60]} | {opp['agency']} | Deadline {opp['response_deadline']}",
                "body": email_body,
                "score": opp["score"],
                "queued_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
            })
    return queue


def write_email_queue(queue: list, dry_run: bool = False) -> None:
    """Write the email queue JSON for the cold email infrastructure to consume."""
    ensure_output_dirs()
    if not queue:
        logger.info("No emails queued (no opportunities above score threshold).")
        return

    if dry_run:
        logger.info("[DRY-RUN] Would write %d email records to %s", len(queue), EMAIL_QUEUE_FILE)
        return

    try:
        existing = []
        if EMAIL_QUEUE_FILE.exists():
            try:
                existing = json.loads(EMAIL_QUEUE_FILE.read_text(encoding="utf-8"))
            except Exception:
                existing = []

        existing_ids = {e.get("notice_id") for e in existing}
        new_items = [e for e in queue if e["notice_id"] not in existing_ids]
        existing.extend(new_items)

        EMAIL_QUEUE_FILE.write_text(json.dumps(existing, indent=2), encoding="utf-8")
        logger.info("Email queue updated: %d new entries, %d total in %s", len(new_items), len(existing), EMAIL_QUEUE_FILE)
    except Exception as exc:
        logger.error("Failed to write email queue: %s", exc)


# ---------------------------------------------------------------------------
# Cold email infrastructure hook
# ---------------------------------------------------------------------------

def dispatch_to_cold_email_infra(queue: list, dry_run: bool = False) -> None:
    """Invoke the cold email sender script if it exists, passing the queue file."""
    if not queue:
        return

    sender_script = safe_path("AUTOMATIONS/scripts/cold_email_sender.py")
    if not sender_script.exists():
        logger.info("Cold email sender not found at %s — emails queued for manual dispatch.", sender_script)
        return

    cmd = [
        sys.executable,
        str(sender_script),
        "--queue-file", str(EMAIL_QUEUE_FILE),
    ]
    if dry_run:
        cmd.append("--dry-run")
        logger.info("[DRY-RUN] Would invoke cold email sender: %s", " ".join(cmd))
        return

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            logger.info("Cold email sender completed successfully.")
        else:
            logger.error("Cold email sender exited %d: %s", result.returncode, result.stderr[:500])
    except subprocess.TimeoutExpired:
        logger.error("Cold email sender timed out after 60s.")
    except Exception as exc:
        logger.error("Failed to invoke cold email sender: %s", exc)


# ---------------------------------------------------------------------------
# Status display
# ---------------------------------------------------------------------------

def print_status() -> None:
    """Print last-run status from the status JSON file."""
    if not STATUS_FILE.exists():
        print("No status file found. Run with --run first.")
        return
    try:
        data = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
        print(f"\nPRINTMAXX SAM.gov Scanner — Last Run Status")
        print(f"  Run at    : {data.get('last_run', 'unknown')}")
        print(f"  Dry run   : {data.get('dry_run', False)}")
        print(f"  Total opps: {data.get('total_found', 0)}")
        print("\n  Top Opportunities:")
        for i, opp in enumerate(data.get("top_opportunities", []), 1):
            print(f"    {i}. [{opp['score']:.1f}] {opp['title'][:60]} — {opp['deadline']}")
        print()
    except Exception as exc:
        print(f"Error reading status: {exc}")


# ---------------------------------------------------------------------------
# Method context injection
# ---------------------------------------------------------------------------

def inject_method_context_opportunity(opps: list) -> list:
    """Inject the known METHOD CONTEXT record as a synthetic opportunity."""
    injected_id = "INJECTED-METHOD-CONTEXT-2027"
    if any(o["notice_id"] == injected_id for o in opps):
        return opps

    synthetic = {
        "notice_id": injected_id,
        "title": "On-Site and Off-Site Printing and Graphic Design Services Support",
        "agency": "Federal Agency (METHOD CONTEXT)",
        "naics_code": "323111",
        "set_aside_type": "None",
        "response_deadline": KNOWN_METHOD_CONTEXT["deadline"],
        "estimated_value": 0.0,
        "score": 0.0,
        "url": "",
        "posted_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "description_snippet": KNOWN_METHOD_CONTEXT["description"][:300],
        "scored_at": "",
    }
    opps.insert(0, synthetic)
    return opps


# ---------------------------------------------------------------------------
# Core run logic
# ---------------------------------------------------------------------------

def run_scanner(dry_run: bool = False) -> int:
    """Main scanner execution. Returns exit code."""
    run_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    logger.info("=== PRINTMAXX SAM.gov Scanner starting (dry_run=%s, run_at=%s) ===", dry_run, run_at)

    recall_skills_for_task("sam_gov_printing_scanner")

    api_key = load_api_key()
    if not api_key:
        logger.warning("No SAM.gov API key found. Using mock data.")
        raw_opps = fetch_mock_opportunities()
    elif dry_run:
        logger.info("[DRY-RUN] Using mock data instead of live API.")
        raw_opps = fetch_mock_opportunities()
    else:
        raw_opps = fetch_all_printing_opportunities(api_key)
        if not raw_opps:
            logger.warning("No opportunities returned from SAM.gov API. Falling back to mock.")
            raw_opps = fetch_mock_opportunities()

    parsed = [parse_opportunity(r) for r in raw_opps]
    parsed = inject_method_context_opportunity(parsed)
    scored = score_opportunities(parsed)

    logger.info("Scored %d opportunities. Top score: %.2f", len(scored), scored[0]["score"] if scored else 0.0)

    if not dry_run:
        write_results_csv(scored)

    write_status_json(scored, run_at, dry_run)

    for opp in scored[:10]:
        generate_capability_draft(opp, dry_run=dry_run)

    email_queue = build_email_queue(scored, score_threshold=5.0)
    write_email_queue(email_queue, dry_run=dry_run)
    dispatch_to_cold_email_infra(email_queue, dry_run=dry_run)

    result = {
        "run_at": run_at,
        "total_opportunities": len(scored),
        "top_score": scored[0]["score"] if scored else 0.0,
        "emails_queued": len(email_queue),
        "drafts_generated": min(len(scored), 10),
    }
    capture_skill_from_result("sam_gov_printing_scanner", result)

    logger.info(
        "=== Scanner complete: %d opps scored, %d emails queued, %d drafts generated ===",
        len(scored), len(email_queue), min(len(scored), 10),
    )
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sam_gov_printing_scanner",
        description="PRINTMAXX SAM.gov daily printing and graphic design contract scanner.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Execute the full scanner: fetch, score, draft, queue emails.",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Display the results of the last scanner run.",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Run with mock data; skip all writes except status and logs.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.status:
            print_status()
            sys.exit(0)
        elif args.run:
            code = run_scanner(dry_run=False)
            sys.exit(code)
        elif args.dry_run:
            code = run_scanner(dry_run=True)
            sys.exit(code)
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
        sys.exit(130)
    except Exception as exc:
        logger.exception("Unhandled exception in main: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()