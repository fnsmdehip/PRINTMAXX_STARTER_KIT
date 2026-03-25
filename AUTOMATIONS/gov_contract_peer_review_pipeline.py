#!/usr/bin/env python3
"""
PRINTMAXX Automation System - GOV CONTRACT Peer Review Pipeline

SAM.gov opportunity scanner that detects peer review / evaluation support
contracts, generates capability statements via Claude API, and queues
proposal sections for human review before submission.

Target:  BJA PEER REVIEW SUPPORT SERVICES
Agency:  Bureau of Justice Assistance
Deadline: 2026-04-17
Type:    handoff
"""

import argparse
import csv
import json
import logging
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# _common import with local fallback
# ---------------------------------------------------------------------------
try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path) -> Path:
        """Validate that *path* resolves within the PROJECT root."""
        resolved = Path(path).resolve()
        try:
            resolved.relative_to(PROJECT)
        except ValueError:
            raise ValueError(
                f"Path '{resolved}' is outside PROJECT root '{PROJECT}'"
            )
        return resolved

    def recall_skills_for_task(task: str) -> list:
        return []

    def capture_skill_from_result(task: str, result: dict) -> None:
        pass

# ---------------------------------------------------------------------------
# Directory / file constants
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOGS_DIR        = AUTOMATIONS_DIR / "logs"
DATA_DIR        = AUTOMATIONS_DIR / "data"  / "gov_contract"
QUEUE_DIR       = AUTOMATIONS_DIR / "queue" / "gov_contract"
LOG_FILE        = LOGS_DIR / "gov_contract_peer_review_pipeline.log"

# ---------------------------------------------------------------------------
# Opportunity / API constants
# ---------------------------------------------------------------------------
OPPORTUNITY_KEYWORDS = [
    "peer review support",
    "peer review",
    "evaluation support",
    "grant review",
    "technical review",
    "peer evaluation",
    "review support services",
]

SAM_API_BASE    = "https://api.sam.gov/opportunities/v2/search"
SAM_KEY_ENV     = "SAM_GOV_API_KEY"
CLAUDE_KEY_ENV  = "ANTHROPIC_API_KEY"
CLAUDE_API_URL  = "https://api.anthropic.com/v1/messages"
CLAUDE_MODEL    = "claude-opus-4-6"

TARGET = {
    "title":    "BJA PEER REVIEW SUPPORT SERVICES",
    "agency":   "Bureau of Justice Assistance",
    "deadline": "2026-04-17",
    "type":     "handoff",
}

PROPOSAL_SECTIONS = [
    ("technical_approach", "Technical Approach and Methodology"),
    ("management_plan",    "Management Plan and Key Personnel"),
    ("past_performance",   "Past Performance and Relevant Experience"),
    ("price_volume",       "Price / Cost Volume Summary"),
]


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
def setup_logging() -> logging.Logger:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_path = safe_path(LOG_FILE)
    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=fmt,
        handlers=[
            logging.FileHandler(str(log_path), mode="a", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger("printmaxx.gov_contract")


# ---------------------------------------------------------------------------
# Disk-space pre-flight (subprocess)
# ---------------------------------------------------------------------------
def check_disk_space(logger: logging.Logger) -> None:
    """Log available disk space for the PROJECT volume."""
    try:
        result = subprocess.run(
            ["df", "-h", str(PROJECT)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            lines = result.stdout.strip().splitlines()
            if len(lines) >= 2:
                logger.info(f"Disk space — {lines[-1]}")
        else:
            logger.warning(f"df returned non-zero: {result.stderr.strip()}")
    except (subprocess.SubprocessError, FileNotFoundError, OSError) as exc:
        logger.debug(f"Disk-space check skipped: {exc}")


# ---------------------------------------------------------------------------
# SAM.gov scanning
# ---------------------------------------------------------------------------
def _sam_url(keyword: str, api_key: str, posted_from: str = "01/01/2026") -> str:
    params = {
        "api_key":    api_key,
        "keywords":   keyword,
        "postedFrom": posted_from,
        "limit":      "50",
        "offset":     "0",
        "noticeType": "o,p,k,r",
    }
    return f"{SAM_API_BASE}?{urllib.parse.urlencode(params)}"


def _fetch_keyword(keyword: str, api_key: str, logger: logging.Logger) -> list:
    url = _sam_url(keyword, api_key)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PRINTMAXX/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            opps = data.get("opportunitiesData", [])
            logger.info(f"SAM.gov '{keyword}': {len(opps)} result(s)")
            return opps
    except urllib.error.HTTPError as exc:
        logger.error(f"SAM.gov HTTP {exc.code} for '{keyword}': {exc.reason}")
    except urllib.error.URLError as exc:
        logger.error(f"SAM.gov URL error for '{keyword}': {exc.reason}")
    except json.JSONDecodeError as exc:
        logger.error(f"SAM.gov JSON error for '{keyword}': {exc}")
    except Exception as exc:
        logger.error(f"SAM.gov unexpected error for '{keyword}': {exc}")
    return []


def _is_match(opp: dict) -> bool:
    combined = (
        (opp.get("title") or "") + " " + (opp.get("description") or "")
    ).lower()
    return any(kw.lower() in combined for kw in OPPORTUNITY_KEYWORDS)


def _mock_opportunity() -> dict:
    return {
        "noticeId":           "BJA-PEER-REVIEW-2026-MOCK",
        "title":              TARGET["title"],
        "organizationName":   TARGET["agency"],
        "responseDeadLine":   TARGET["deadline"],
        "type":               "Solicitation",
        "fullParentPathName": "DEPT OF JUSTICE.OJP.BJA",
        "description":        (
            "Peer review and evaluation support services for BJA grant programs, "
            "including coordination of subject-matter expert reviewers, scoring "
            "normalization, and final evaluation report compilation."
        ),
        "uiLink": "https://sam.gov",
    }


def scan_sam_gov(api_key: str, logger: logging.Logger, dry_run: bool = False) -> list:
    """Return de-duplicated peer-review opportunities from SAM.gov."""
    logger.info("Scanning SAM.gov for peer review / evaluation support opportunities…")
    found: list  = []
    seen:  set   = set()

    for kw in OPPORTUNITY_KEYWORDS[:3]:          # limit to avoid rate caps
        if dry_run:
            logger.info(f"[DRY RUN] Would query SAM.gov: '{kw}'")
            opp = _mock_opportunity()
            if opp["noticeId"] not in seen:
                found.append(opp)
                seen.add(opp["noticeId"])
            continue

        for opp in _fetch_keyword(kw, api_key, logger):
            nid = opp.get("noticeId") or opp.get("solicitationNumber", "")
            if nid and nid not in seen and _is_match(opp):
                found.append(opp)
                seen.add(nid)

    logger.info(f"Scan complete — {len(found)} matching opportunity(ies) found.")
    return found


# ---------------------------------------------------------------------------
# Claude API helpers
# ---------------------------------------------------------------------------
def _claude_request(prompt: str, api_key: str, logger: logging.Logger) -> str:
    payload = json.dumps({
        "model":      CLAUDE_MODEL,
        "max_tokens": 2048,
        "messages":   [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = urllib.request.Request(
        CLAUDE_API_URL,
        data=payload,
        method="POST",
        headers={
            "Content-Type":      "application/json",
            "x-api-key":         api_key,
            "anthropic-version": "2023-06-01",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["content"][0]["text"]
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        logger.error(f"Claude HTTP {exc.code}: {body[:300]}")
    except urllib.error.URLError as exc:
        logger.error(f"Claude URL error: {exc.reason}")
    except (json.JSONDecodeError, KeyError, IndexError) as exc:
        logger.error(f"Claude response parse error: {exc}")
    except Exception as exc:
        logger.error(f"Claude unexpected error: {exc}")
    return ""


# ---------------------------------------------------------------------------
# Capability statement
# ---------------------------------------------------------------------------
def _capability_prompt(opp: dict) -> str:
    return (
        "You are a proposal writer for PRINTMAXX, a professional-services firm "
        "specializing in peer review coordination, evaluation support, and grant "
        "program management.\n\n"
        "Generate a concise capability statement (400–600 words) for:\n\n"
        f"OPPORTUNITY : {opp.get('title', 'Unknown')}\n"
        f"AGENCY      : {opp.get('organizationName', 'Unknown')}\n"
        f"DEADLINE    : {opp.get('responseDeadLine', 'Unknown')}\n"
        f"DESCRIPTION : {(opp.get('description') or '')[:800]}\n\n"
        "Include:\n"
        "1. Company overview and core competencies for peer review support\n"
        "2. Three relevant past-performance examples (generalized/anonymized)\n"
        "3. Key-personnel qualifications and subject-matter expertise\n"
        "4. Differentiators — why PRINTMAXX is uniquely qualified\n"
        "5. Technical-approach summary aligned to the opportunity\n\n"
        "Format as professional proposal prose ready for human review before submission."
    )


def generate_capability_statement(
    opp: dict, api_key: str, logger: logging.Logger, dry_run: bool = False
) -> str:
    title = opp.get("title", "Unknown")
    logger.info(f"Generating capability statement for: {title}")
    if dry_run:
        logger.info("[DRY RUN] Skipping Claude API call.")
        return (
            f"[DRY RUN] Capability statement placeholder for: {title}\n\n"
            "**[REVIEW REQUIRED: replace with production-generated content]**"
        )
    text = _claude_request(_capability_prompt(opp), api_key, logger)
    if not text:
        logger.warning(f"Empty capability statement for: {title}")
        return f"[ERROR] Generation failed for: {title}"
    logger.info(f"Capability statement generated ({len(text):,} chars).")
    return text


# ---------------------------------------------------------------------------
# Proposal sections
# ---------------------------------------------------------------------------
def _section_prompt(key: str, title: str, opp: dict) -> str:
    return (
        f"You are a senior proposal writer for PRINTMAXX.\n\n"
        f"Write the '{title}' section for a proposal responding to:\n\n"
        f"OPPORTUNITY : {opp.get('title', 'Unknown')}\n"
        f"AGENCY      : {opp.get('organizationName', 'Unknown')}\n"
        f"DESCRIPTION : {(opp.get('description') or '')[:600]}\n\n"
        "Guidelines:\n"
        "- 300–500 words, formal government-proposal style\n"
        "- Address evaluation criteria typical for peer-review / evaluation-support services\n"
        "- Use placeholders like [INSERT METRIC] or [CONFIRM WITH PM] where firm data is needed\n"
        "- Flag items needing human verification with: **[REVIEW REQUIRED: <reason>]**\n\n"
        "This draft will be reviewed and approved by a human before submission."
    )


def generate_proposal_sections(
    opp: dict, api_key: str, logger: logging.Logger, dry_run: bool = False
) -> dict:
    sections: dict = {}
    for key, title in PROPOSAL_SECTIONS:
        logger.info(f"  Drafting section: {title}")
        if dry_run:
            sections[key] = (
                f"[DRY RUN] Draft for '{title}'\n\n"
                "**[REVIEW REQUIRED: dry-run placeholder — replace before submission]**"
            )
            continue
        content = _claude_request(_section_prompt(key, title, opp), api_key, logger)
        sections[key] = content if content else f"[ERROR] Generation failed: {title}"
    return sections


# ---------------------------------------------------------------------------
# File I/O helpers
# ---------------------------------------------------------------------------
_CSV_FIELDS = [
    "noticeId", "title", "organizationName", "responseDeadLine",
    "type", "fullParentPathName", "uiLink", "scanned_at",
]


def write_opportunity_csv(
    opportunities: list, logger: logging.Logger, dry_run: bool = False
) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ts   = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    path = safe_path(DATA_DIR / f"opportunities_{ts}.csv")

    if dry_run:
        logger.info(f"[DRY RUN] Would write {len(opportunities)} row(s) → {path}")
        return path

    now_iso = datetime.now(timezone.utc).isoformat()
    try:
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=_CSV_FIELDS, extrasaction="ignore")
            writer.writeheader()
            for opp in opportunities:
                row = {k: opp.get(k, "") for k in _CSV_FIELDS}
                row["scanned_at"] = now_iso
                writer.writerow(row)
        logger.info(f"Wrote {len(opportunities)} opportunity row(s) → {path}")
    except OSError as exc:
        logger.error(f"CSV write failed: {exc}")

    return path


def queue_for_review(
    opp: dict,
    capability_statement: str,
    sections: dict,
    logger: logging.Logger,
    dry_run: bool = False,
) -> Path:
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    notice_id = (opp.get("noticeId") or "UNKNOWN").replace("/", "-")
    ts        = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    path      = safe_path(QUEUE_DIR / f"review_{notice_id}_{ts}.json")

    package = {
        "queued_at":           datetime.now(timezone.utc).isoformat(),
        "status":              "pending_review",
        "opportunity":         opp,
        "capability_statement": capability_statement,
        "proposal_sections":   sections,
        "deadline":            opp.get("responseDeadLine", TARGET["deadline"]),
        "submission_type":     TARGET["type"],
        "review_checklist": [
            "Verify past-performance examples are accurate and documented",
            "Confirm key-personnel availability and any required clearances",
            "Validate pricing against current labor-rate cards",
            "Legal review: teaming / subcontracting arrangements",
            "Compliance matrix review against final solicitation",
            "Sign and date all certifications and representations",
        ],
    }

    if dry_run:
        logger.info(f"[DRY RUN] Would write review package → {path}")
        return path

    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(package, fh, indent=2, ensure_ascii=False)
        logger.info(f"Review package queued → {path}")
    except OSError as exc:
        logger.error(f"Queue write failed: {exc}")

    return path


# ---------------------------------------------------------------------------
# Status report
# ---------------------------------------------------------------------------
def report_status(logger: logging.Logger) -> None:
    logger.info("─" * 60)
    logger.info("PIPELINE STATUS REPORT")
    logger.info("─" * 60)

    if QUEUE_DIR.exists():
        packages = sorted(QUEUE_DIR.glob("review_*.json"))
        logger.info(f"Queue dir    : {QUEUE_DIR}")
        logger.info(f"Pending pkgs : {len(packages)}")
        for pkg_path in packages:
            try:
                with open(pkg_path, encoding="utf-8") as fh:
                    pkg = json.load(fh)
                title    = pkg.get("opportunity", {}).get("title", "Unknown")
                status   = pkg.get("status", "unknown")
                deadline = pkg.get("deadline", "unknown")
                logger.info(f"  [{status}] {title} | deadline: {deadline} | {pkg_path.name}")
            except (OSError, json.JSONDecodeError) as exc:
                logger.warning(f"  Cannot read {pkg_path.name}: {exc}")
    else:
        logger.info("Queue directory does not exist. Run --run to start pipeline.")

    if DATA_DIR.exists():
        csvs = list(DATA_DIR.glob("opportunities_*.csv"))
        logger.info(f"Scan files   : {len(csvs)}")
    else:
        logger.info("No scan-data directory found.")

    if LOG_FILE.exists():
        size = LOG_FILE.stat().st_size
        logger.info(f"Log file     : {LOG_FILE} ({size:,} bytes)")

    logger.info("─" * 60)


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def run_pipeline(logger: logging.Logger, dry_run: bool = False) -> int:
    marker = "[DRY RUN] " if dry_run else ""
    logger.info("=" * 60)
    logger.info(f"PRINTMAXX GOV CONTRACT PIPELINE {marker}STARTED")
    logger.info(f"Target   : {TARGET['title']}")
    logger.info(f"Deadline : {TARGET['deadline']}")
    logger.info("=" * 60)

    # Pre-flight
    check_disk_space(logger)

    sam_key    = os.environ.get(SAM_KEY_ENV, "")
    claude_key = os.environ.get(CLAUDE_KEY_ENV, "")

    if not sam_key and not dry_run:
        logger.warning(f"{SAM_KEY_ENV} not set — SAM.gov API calls may fail.")
    if not claude_key and not dry_run:
        logger.error(f"{CLAUDE_KEY_ENV} not set — cannot generate proposal content.")
        return 1

    # Step 1 — recall skills
    logger.info("Step 1/5 — Recalling relevant skills…")
    try:
        skills = recall_skills_for_task(
            "government contract peer review proposal writing capability statement"
        )
        logger.info(f"           {len(skills)} skill(s) recalled.")
    except Exception as exc:
        logger.debug(f"recall_skills_for_task skipped: {exc}")

    # Step 2 — SAM.gov scan
    logger.info("Step 2/5 — Scanning SAM.gov…")
    opportunities = scan_sam_gov(sam_key, logger, dry_run=dry_run)

    if not opportunities:
        logger.warning("No opportunities returned — using built-in target as fallback.")
        opportunities = [_mock_opportunity()]

    # Step 3 — write CSV
    logger.info("Step 3/5 — Persisting scan results…")
    csv_path = write_opportunity_csv(opportunities, logger, dry_run=dry_run)

    # Step 4 — generate content & queue
    logger.info("Step 4/5 — Generating capability statements and proposal sections…")
    queued = 0
    for opp in opportunities:
        title = opp.get("title", "Unknown")
        logger.info(f"  Processing: {title}")
        try:
            cap   = generate_capability_statement(opp, claude_key, logger, dry_run)
            sects = generate_proposal_sections(opp, claude_key, logger, dry_run)
            pkg   = queue_for_review(opp, cap, sects, logger, dry_run)
            queued += 1

            try:
                capture_skill_from_result(
                    "gov_contract_peer_review",
                    {
                        "opportunity": title,
                        "package":     str(pkg),
                        "sections":    list(sects.keys()),
                    },
                )
            except Exception as exc:
                logger.debug(f"capture_skill_from_result skipped: {exc}")

        except Exception as exc:
            logger.error(f"Failed to process '{title}': {exc}")

    # Step 5 — summary
    logger.info("Step 5/5 — Pipeline summary")
    logger.info("=" * 60)
    logger.info(f"Packages queued for human review : {queued}")
    logger.info(f"Review queue directory           : {QUEUE_DIR}")
    logger.info(f"Opportunity CSV                  : {csv_path}")
    logger.info(f"Next action                      : human review → submission by {TARGET['deadline']}")
    logger.info("=" * 60)
    return 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        prog="gov_contract_peer_review_pipeline",
        description="PRINTMAXX — GOV CONTRACT Peer Review Opportunity Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --run\n"
            "  %(prog)s --run --dry-run\n"
            "  %(prog)s --status\n"
        ),
    )
    parser.add_argument("--run",     action="store_true", help="Execute the full pipeline")
    parser.add_argument("--status",  action="store_true", help="Report current queue status")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without API calls or file writes")

    args = parser.parse_args()

    if not (args.run or args.status):
        parser.print_help()
        sys.exit(0)

    logger    = setup_logging()
    exit_code = 0

    try:
        if args.status:
            report_status(logger)
        if args.run:
            exit_code = run_pipeline(logger, dry_run=args.dry_run)
    except KeyboardInterrupt:
        logging.getLogger("printmaxx.gov_contract").info("Interrupted.")
        sys.exit(130)
    except Exception as exc:
        logging.getLogger("printmaxx.gov_contract").exception(f"Unhandled error: {exc}")
        sys.exit(1)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()