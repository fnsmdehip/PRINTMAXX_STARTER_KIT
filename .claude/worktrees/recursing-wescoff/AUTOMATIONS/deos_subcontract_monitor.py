#!/usr/bin/env python3
"""
PRINTMAXX Automation: DEOS Subcontract Monitor
----------------------------------------------
Monitors SAM.gov for Defense Enterprise Office Solutions (DEOS) subcontracting
opportunities, identifies prime contractors awarded under the DEOS vehicle,
scrapes their capability statements and contact info, and routes leads to the
cold outbound pipeline with gov-specific messaging.

Deadline: 2026-09-04
Method Context: [GOV CONTRACT] DEFENSE ENTERPRISE OFFICE SOLUTIONS (DEOS)
"""

import argparse
import csv
import json
import logging
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# _common bootstrap — import from shared module, fall back to local defs
# ---------------------------------------------------------------------------
try:
    from _common import (  # type: ignore[import]
        PROJECT,
        safe_path,
        recall_skills_for_task,
        capture_skill_from_result,
    )
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path: Path) -> Path:
        """Validate that *path* resolves within PROJECT; raise ValueError if not."""
        resolved = Path(path).resolve()
        try:
            resolved.relative_to(PROJECT)
        except ValueError:
            raise ValueError(
                f"Path escape detected: {resolved!r} is outside PROJECT {PROJECT!r}"
            )
        return resolved

    def recall_skills_for_task(task: str) -> list:  # type: ignore[misc]
        return []

    def capture_skill_from_result(task: str, result: dict) -> None:  # type: ignore[misc]
        pass


# ---------------------------------------------------------------------------
# Directory / file layout
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_DIR         = AUTOMATIONS_DIR / "logs"
DATA_DIR        = AUTOMATIONS_DIR / "data"  / "deos"
OUTPUT_DIR      = AUTOMATIONS_DIR / "output" / "deos"

LOG_FILE      = LOG_DIR   / "deos_subcontract_monitor.log"
STATE_FILE    = DATA_DIR  / "state.json"
LEADS_CSV     = OUTPUT_DIR / "deos_leads.csv"
PIPELINE_JSON = OUTPUT_DIR / "pipeline_queue.json"

# ---------------------------------------------------------------------------
# Domain constants
# ---------------------------------------------------------------------------
DEOS_KEYWORDS = [
    "DEOS",
    "Defense Enterprise Office Solutions",
    "enterprise office solutions",
    "DEOS subcontract",
    "DEOS teaming",
]

SAM_OPP_BASE    = "https://api.sam.gov/opportunities/v2/search"
SAM_ENTITY_BASE = "https://api.sam.gov/entity-information/v3/entities"

OUTBOUND_TEMPLATE = """\
Subject: PRINTMAXX — Print/Document Solutions for Your DEOS Task Order Team

Hello {salutation},

Congratulations on your award under the Defense Enterprise Office Solutions
(DEOS) IDIQ vehicle.

PRINTMAXX specializes in enterprise print and document management solutions
tailored to DoD and federal agency requirements — MFP fleets, secure print,
CAC-authenticated release, and DEOS-compatible managed print services.

We are actively seeking teaming arrangements and subcontracting opportunities
with DEOS prime contractors to support task order responses. Our capabilities:

  • DoD-compliant managed print services (unclassified / CUI environments)
  • DEOS-compatible MFP hardware supply and lifecycle management
  • Print security: pull-print, audit logging, CAC/PIV integration
  • Help desk + field service across CONUS/OCONUS installations
  • Past Performance: GSA MAS, Army, Navy installations

We would welcome a brief 15-minute introduction call to explore teaming on
upcoming DEOS task orders.

Best regards,
PRINTMAXX Government Solutions Team
"""

CSV_FIELDS = [
    "notice_id", "solicitation_number", "title", "posted_date",
    "response_deadline", "agency", "naics", "set_aside",
    "awardee_name", "awardee_uei", "awardee_cage", "awardee_address",
    "contact_name", "contact_email", "contact_phone",
    "award_number", "award_amount",
    "website", "capability_snippet",
    "pipeline_status", "queued_at", "url",
]

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    """Create append-mode file logger + stdout handler."""
    log_path = safe_path(LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("deos_monitor")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        fmt = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%SZ",
        )
        fh = logging.FileHandler(str(log_path), mode="a", encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)
        sh.setFormatter(fmt)
        logger.addHandler(sh)

    return logger


# ---------------------------------------------------------------------------
# State persistence
# ---------------------------------------------------------------------------

def load_state() -> dict:
    path = safe_path(STATE_FILE)
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "last_run": None,
        "processed_notices": [],
        "known_primes": [],
        "pipeline_count": 0,
    }


def save_state(state: dict, logger: logging.Logger) -> None:
    path = safe_path(STATE_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(state, fh, indent=2)
        logger.debug("State saved → %s", path)
    except OSError as exc:
        logger.error("State save failed: %s", exc)


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _fetch_url(url: str, headers: dict, logger: logging.Logger, retries: int = 3) -> bytes:
    """
    Attempt urllib GET with exponential back-off; fall back to curl subprocess
    on persistent failure.
    """
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except urllib.error.HTTPError as exc:
            logger.warning("HTTP %s attempt %d/%d: %s", exc.code, attempt, retries, url)
            if exc.code in (429, 503):
                time.sleep(5 * attempt)
            else:
                break
        except urllib.error.URLError as exc:
            logger.warning("URLError attempt %d/%d: %s", attempt, retries, exc.reason)
            time.sleep(3 * attempt)

    # curl fallback — avoids exotic third-party HTTP libs
    try:
        logger.debug("Falling back to curl for %s", url)
        result = subprocess.run(
            ["curl", "-sSL", "--max-time", "30", url],
            capture_output=True,
            timeout=35,
        )
        if result.returncode == 0:
            return result.stdout
    except (subprocess.SubprocessError, FileNotFoundError) as exc:
        logger.debug("curl fallback failed: %s", exc)

    return b""


def _sam_get(endpoint: str, params: dict, logger: logging.Logger) -> dict:
    """GET a SAM.gov endpoint and parse JSON response."""
    api_key = os.environ.get("SAM_API_KEY", "")
    if api_key:
        params = {**params, "api_key": api_key}

    url = f"{endpoint}?{urllib.parse.urlencode(params)}"
    headers = {
        "Accept": "application/json",
        "User-Agent": "PRINTMAXX-AutoBot/1.0",
    }
    raw = _fetch_url(url, headers, logger)
    if not raw:
        return {}
    try:
        return json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        logger.error("JSON parse error from %s: %s", endpoint, exc)
        return {}


# ---------------------------------------------------------------------------
# SAM.gov opportunity search
# ---------------------------------------------------------------------------

def search_deos_opportunities(logger: logging.Logger) -> list:
    """Return deduplicated SAM.gov opportunities matching DEOS keywords."""
    all_opps: list = []

    for keyword in DEOS_KEYWORDS:
        params = {
            "q": keyword,
            "index": "opp",
            "page": "0",
            "size": "100",
            "sort": "-modifiedDate",
            "status": "active,inactive,archived",
        }
        logger.info("SAM search: %r", keyword)
        data = _sam_get(SAM_OPP_BASE, params, logger)
        hits = data.get("opportunitiesData", [])
        logger.debug("  %d hits", len(hits))
        all_opps.extend(hits)
        time.sleep(1)

    seen: set = set()
    unique: list = []
    for opp in all_opps:
        nid = opp.get("noticeId") or opp.get("id", "")
        if nid and nid not in seen:
            seen.add(nid)
            unique.append(opp)

    logger.info("%d unique DEOS opportunities found", len(unique))
    return unique


# ---------------------------------------------------------------------------
# Award / prime-contractor extraction
# ---------------------------------------------------------------------------

def _str(val) -> str:
    return str(val) if val is not None else ""


def extract_award_data(opportunities: list, logger: logging.Logger) -> list:
    """Filter to award notices and parse prime contractor fields."""
    awards: list = []
    award_type_tokens = {"a", "award_notice", "award notice", "j&a"}

    for opp in opportunities:
        t_notice = _str(opp.get("type", "")).lower()
        t_base   = _str(opp.get("baseType", "")).lower()
        title    = _str(opp.get("title", "")).lower()

        is_award = (
            t_notice in award_type_tokens
            or t_base in award_type_tokens
            or "award" in title
        )
        if not is_award:
            continue

        awardee_block = opp.get("award", {}) or {}
        awardee_info  = awardee_block.get("awardee", {}) or {} if isinstance(awardee_block, dict) else {}
        loc           = awardee_info.get("location", {}) or {} if isinstance(awardee_info, dict) else {}

        city_name  = loc.get("city", {}).get("name", "")  if isinstance(loc.get("city"),  dict) else ""
        state_code = loc.get("state", {}).get("code", "") if isinstance(loc.get("state"), dict) else ""
        address    = ", ".join(filter(None, [_str(loc.get("streetAddress", "")), city_name, state_code]))

        poc_list = opp.get("pointOfContact") or []
        poc      = poc_list[0] if isinstance(poc_list, list) and poc_list and isinstance(poc_list[0], dict) else {}

        awards.append({
            "notice_id":           _str(opp.get("noticeId") or opp.get("id", "")),
            "title":               _str(opp.get("title", "")),
            "posted_date":         _str(opp.get("postedDate", "")),
            "response_deadline":   _str(opp.get("responseDeadLine", "")),
            "naics":               _str(opp.get("naicsCode", "")),
            "set_aside":           _str(opp.get("typeOfSetAsideDescription", "")),
            "agency":              _str(opp.get("fullParentPathName", opp.get("organizationHierarchy", ""))),
            "solicitation_number": _str(opp.get("solicitationNumber", "")),
            "award_number":        _str(awardee_block.get("number", "")) if isinstance(awardee_block, dict) else "",
            "award_amount":        _str(awardee_block.get("amount", "")) if isinstance(awardee_block, dict) else "",
            "awardee_name":        _str(awardee_info.get("name", "")) if isinstance(awardee_info, dict) else "",
            "awardee_uei":         _str(awardee_info.get("ueiSAM", "")) if isinstance(awardee_info, dict) else "",
            "awardee_cage":        _str(awardee_info.get("cageCode", "")) if isinstance(awardee_info, dict) else "",
            "awardee_address":     address,
            "contact_name":        _str(poc.get("fullName", "")),
            "contact_email":       _str(poc.get("email", "")),
            "contact_phone":       _str(poc.get("phone", "")),
            "description":         _str(opp.get("description", ""))[:500],
            "url":                 _str(opp.get("uiLink", "")),
        })

    logger.info("%d award records extracted", len(awards))
    return awards


# ---------------------------------------------------------------------------
# SAM.gov entity enrichment
# ---------------------------------------------------------------------------

def enrich_entity(uei: str, logger: logging.Logger) -> dict:
    """Pull entity registration data for a given UEI."""
    if not uei:
        return {}

    params = {
        "ueiSAM": uei,
        "includeSections": (
            "entityRegistration,coreData,assertions,"
            "repsAndCerts,pointsOfContact"
        ),
    }
    data = _sam_get(SAM_ENTITY_BASE, params, logger)
    entities = data.get("entityData", [])
    if not entities:
        return {}

    entity     = entities[0]
    reg        = entity.get("entityRegistration", {}) or {}
    core       = entity.get("coreData", {})            or {}
    assertions = entity.get("assertions", {})          or {}
    pocs       = entity.get("pointsOfContact", {})     or {}

    gvt_poc  = pocs.get("governmentBusinessPOC", {})  or {}
    elec_poc = pocs.get("electronicBusinessPOC", {})  or {}
    gns      = assertions.get("goodsAndServices", {}) or {}
    naics_l  = gns.get("naicsList") or []
    ent_info = core.get("entityInformation", {})       or {}

    return {
        "legal_name":       _str(reg.get("legalBusinessName", "")),
        "website":          _str(ent_info.get("entityURL", "")),
        "primary_naics":    _str(gns.get("primaryNaics", "")),
        "naics_list":       json.dumps([_str(n.get("naicsCode", "")) for n in naics_l if isinstance(n, dict)]),
        "cage_code":        _str(reg.get("cageCode", "")),
        "govt_poc_name":    f"{_str(gvt_poc.get('firstName',''))} {_str(gvt_poc.get('lastName',''))}".strip(),
        "govt_poc_email":   _str(gvt_poc.get("email", "")),
        "elec_poc_name":    f"{_str(elec_poc.get('firstName',''))} {_str(elec_poc.get('lastName',''))}".strip(),
        "elec_poc_email":   _str(elec_poc.get("email", "")),
    }


# ---------------------------------------------------------------------------
# Capability statement scraper
# ---------------------------------------------------------------------------

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE  = re.compile(r"\s+")

_CAP_PATHS = ["/capability-statement", "/capabilities", "/about", "/services", "/government"]


def scrape_capability_statement(website_url: str, logger: logging.Logger) -> str:
    """Attempt to extract a capability snippet from the company's public website."""
    if not website_url:
        return ""
    parsed = urllib.parse.urlparse(website_url)
    if parsed.scheme not in ("http", "https"):
        return ""

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; PRINTMAXX-Bot/1.0)",
        "Accept": "text/html",
    }
    base = f"{parsed.scheme}://{parsed.netloc}"

    for path in _CAP_PATHS:
        try:
            raw = _fetch_url(base + path, headers, logger)
            if not raw:
                continue
            html = raw[:16384].decode("utf-8", errors="replace")
            text = _TAG_RE.sub(" ", html)
            text = _WS_RE.sub(" ", text).strip()
            if len(text) > 80:
                snippet = text[:400]
                logger.debug("Capability snippet from %s%s", base, path)
                return snippet
        except Exception as exc:
            logger.debug("Scrape error %s%s: %s", base, path, exc)

    return ""


# ---------------------------------------------------------------------------
# Cold outbound message builder
# ---------------------------------------------------------------------------

def build_outbound_message(contact_name: str) -> str:
    salutation = contact_name.split()[0] if contact_name.strip() else "Team"
    return OUTBOUND_TEMPLATE.format(salutation=salutation)


# ---------------------------------------------------------------------------
# Pipeline management
# ---------------------------------------------------------------------------

def add_to_pipeline(leads: list, logger: logging.Logger, dry_run: bool = False) -> int:
    """Append new leads to the pipeline JSON queue; return count added."""
    path = safe_path(PIPELINE_JSON)
    existing: list = []
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as fh:
                existing = json.load(fh)
        except (json.JSONDecodeError, OSError):
            existing = []

    existing_ids = {r.get("notice_id") for r in existing}
    new_leads = [ld for ld in leads if ld.get("notice_id") not in existing_ids]

    ts = datetime.now(timezone.utc).isoformat()
    for lead in new_leads:
        lead["queued_at"]        = ts
        lead["outbound_message"] = build_outbound_message(lead.get("contact_name", ""))
        lead["pipeline_status"]  = "queued"

    if dry_run:
        logger.info("[DRY-RUN] Would queue %d new leads (no write)", len(new_leads))
        return len(new_leads)

    merged = existing + new_leads
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(safe_path(PIPELINE_JSON), "w", encoding="utf-8") as fh:
        json.dump(merged, fh, indent=2)
    logger.info("Pipeline: +%d new leads (%d total)", len(new_leads), len(merged))
    return len(new_leads)


# ---------------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------------

def write_leads_csv(leads: list, logger: logging.Logger, dry_run: bool = False) -> None:
    path = safe_path(LEADS_CSV)
    if dry_run:
        logger.info("[DRY-RUN] Would write %d rows to %s", len(leads), path)
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(leads)
        logger.info("CSV written: %s (%d rows)", path, len(leads))
    except OSError as exc:
        logger.error("CSV write error: %s", exc)


# ---------------------------------------------------------------------------
# Status report
# ---------------------------------------------------------------------------

def print_status(logger: logging.Logger) -> None:
    state  = load_state()
    p_path = safe_path(PIPELINE_JSON)
    total  = 0
    counts: dict = {}

    if p_path.exists():
        try:
            with open(p_path, "r", encoding="utf-8") as fh:
                leads = json.load(fh)
            total = len(leads)
            for ld in leads:
                s = ld.get("pipeline_status", "unknown")
                counts[s] = counts.get(s, 0) + 1
        except (json.JSONDecodeError, OSError) as exc:
            logger.error("Cannot read pipeline: %s", exc)

    bar = "=" * 60
    lines = [
        bar,
        "PRINTMAXX — DEOS Subcontract Monitor  |  Status Report",
        bar,
        f"  Last run           : {state.get('last_run', 'never')}",
        f"  Notices processed  : {len(state.get('processed_notices', []))}",
        f"  Known primes       : {len(state.get('known_primes', []))}",
        f"  Pipeline total     : {total}",
    ]
    for status, cnt in sorted(counts.items()):
        lines.append(f"    [{status}]: {cnt}")
    lines += [
        f"  Deadline           : 2026-09-04  (DEOS)",
        bar,
    ]
    print("\n".join(lines))


# ---------------------------------------------------------------------------
# Core run
# ---------------------------------------------------------------------------

def run(dry_run: bool, logger: logging.Logger) -> int:
    """
    Full pipeline execution:
      1. Load persistent state
      2. Search SAM.gov for DEOS opportunities
      3. Extract award / prime-contractor records
      4. Skip already-processed notice IDs
      5. Enrich each record via SAM Entity API
      6. Scrape capability statements from company websites
      7. Route enriched leads to the cold-outbound pipeline queue
      8. Export CSV
      9. Persist updated state
    """
    logger.info("=== DEOS Subcontract Monitor START  dry_run=%s ===", dry_run)
    recall_skills_for_task("deos_subcontract_monitor")

    state         = load_state()
    processed_ids = set(state.get("processed_notices", []))
    known_primes  = set(state.get("known_primes", []))

    # 1. Search SAM.gov
    try:
        opportunities = search_deos_opportunities(logger)
    except Exception as exc:
        logger.error("Opportunity search failed: %s", exc, exc_info=True)
        return 1

    # 2. Extract awards
    try:
        awards = extract_award_data(opportunities, logger)
    except Exception as exc:
        logger.error("Award extraction failed: %s", exc, exc_info=True)
        return 1

    # 3. Filter already-processed
    new_awards = [a for a in awards if a["notice_id"] not in processed_ids]
    logger.info("%d new unprocessed award records", len(new_awards))

    if not new_awards:
        logger.info("Nothing new to process.")
        state["last_run"] = datetime.now(timezone.utc).isoformat()
        if not dry_run:
            save_state(state, logger)
        return 0

    # 4–6. Enrich + scrape
    enriched: list = []
    for award in new_awards:
        lead = dict(award)

        try:
            entity = enrich_entity(lead.get("awardee_uei", ""), logger)
            lead.update(entity)
        except Exception as exc:
            logger.warning("Entity enrich failed UEI=%s: %s", lead.get("awardee_uei"), exc)

        website = lead.get("website", "")
        try:
            lead["capability_snippet"] = scrape_capability_statement(website, logger) if website else ""
        except Exception as exc:
            logger.warning("Cap-scrape failed %s: %s", website, exc)
            lead["capability_snippet"] = ""

        enriched.append(lead)
        time.sleep(0.5)

    # 7. Pipeline
    try:
        queued = add_to_pipeline(enriched, logger, dry_run=dry_run)
    except Exception as exc:
        logger.error("Pipeline update failed: %s", exc, exc_info=True)
        queued = 0

    # 8. CSV
    try:
        write_leads_csv(enriched, logger, dry_run=dry_run)
    except Exception as exc:
        logger.error("CSV export failed: %s", exc, exc_info=True)

    # 9. Update state
    for award in new_awards:
        nid   = award.get("notice_id", "")
        prime = award.get("awardee_name", "")
        if nid:
            processed_ids.add(nid)
        if prime:
            known_primes.add(prime)

    state["last_run"]           = datetime.now(timezone.utc).isoformat()
    state["processed_notices"]  = list(processed_ids)
    state["known_primes"]       = list(known_primes)
    state["pipeline_count"]     = state.get("pipeline_count", 0) + queued

    if not dry_run:
        save_state(state, logger)

    capture_skill_from_result("deos_subcontract_monitor", {"queued": queued, "processed": len(new_awards)})
    logger.info("=== Run complete: %d records processed, %d queued ===", len(new_awards), queued)
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="deos_subcontract_monitor",
        description=(
            "PRINTMAXX: Monitor SAM.gov for DEOS subcontracting opportunities "
            "and route prime-contractor leads to the cold outbound pipeline."
        ),
    )
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Execute the full monitoring and enrichment pipeline",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print current pipeline status and exit",
    )
    group.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Run full pipeline logic without writing any output files",
    )
    return p


def main() -> None:
    parser = build_parser()
    args   = parser.parse_args()
    logger = setup_logging()

    if args.status:
        print_status(logger)
        sys.exit(0)

    exit_code = run(dry_run=args.dry_run, logger=logger)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()