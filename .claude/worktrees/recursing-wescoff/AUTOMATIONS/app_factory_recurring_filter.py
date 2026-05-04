#!/usr/bin/env python3
"""
PRINTMAXX Automation: App Factory Recurring Filter Hook

Pre-build validation hook that scores app factory candidates against
recurring-painpoint criteria. Rejects one-time-problem apps before a
build slot is allocated, improving hit rate on $500+ MRR apps.

Usage:
    python app_factory_recurring_filter.py --run
    python app_factory_recurring_filter.py --status
    python app_factory_recurring_filter.py --dry-run
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: try importing from _common; fall back to local stubs so the
# script still runs standalone during initial setup.
# ---------------------------------------------------------------------------
try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result  # noqa: F401
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(p: Path) -> Path:
        """Validate that *p* resolves inside PROJECT and return it."""
        resolved = Path(p).resolve()
        if not str(resolved).startswith(str(PROJECT.resolve())):
            raise ValueError(f"Path escape detected: {resolved} is outside {PROJECT}")
        return resolved

    def recall_skills_for_task(task: str) -> list:
        """Stub: return an empty skill list when _common is unavailable."""
        return []

    def capture_skill_from_result(task: str, result: dict) -> None:
        """Stub: no-op when _common is unavailable."""
        pass


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR = safe_path(PROJECT / "AUTOMATIONS")
LOG_DIR = safe_path(AUTOMATIONS_DIR / "logs")
LOG_FILE = safe_path(LOG_DIR / "app_factory_recurring_filter.log")
CANDIDATES_CSV = safe_path(AUTOMATIONS_DIR / "data" / "app_candidates.csv")
RESULTS_JSON = safe_path(AUTOMATIONS_DIR / "data" / "recurring_filter_results.json")
REJECTED_JSON = safe_path(AUTOMATIONS_DIR / "data" / "rejected_candidates.json")

# ---------------------------------------------------------------------------
# Scoring constants
# ---------------------------------------------------------------------------
RECURRING_KEYWORDS = [
    "weekly", "monthly", "daily", "every week", "every month", "recurring",
    "ongoing", "regular", "repeat", "subscription", "routine", "schedule",
    "frequent", "periodic", "continuous", "always", "constantly", "again",
]
ONE_TIME_KEYWORDS = [
    "one-time", "once", "single", "one time", "never again", "just once",
    "won't happen again", "unique situation", "rare", "occasional",
    "one off", "one-off", "isolated", "special case",
]

RECURRENCE_PASS_THRESHOLD = 60  # score out of 100 required to pass


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def setup_logging(dry_run: bool = False) -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("recurring_filter")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        # Always write to file (append) unless dry-run
        if not dry_run:
            fh = logging.FileHandler(safe_path(LOG_FILE), mode="a", encoding="utf-8")
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(fmt)
            logger.addHandler(fh)
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)
        sh.setFormatter(fmt)
        logger.addHandler(sh)
    return logger


# ---------------------------------------------------------------------------
# Candidate loading
# ---------------------------------------------------------------------------

CANDIDATE_CSV_FIELDS = ("id", "name", "problem_description", "frequency_claim", "target_mrr")


def load_candidates(logger: logging.Logger) -> list:
    """Load app candidates from CSV.  Returns list of dicts."""
    if not CANDIDATES_CSV.exists():
        logger.warning("Candidates CSV not found at %s — using built-in demo data.", CANDIDATES_CSV)
        return _demo_candidates()
    candidates = []
    try:
        with open(safe_path(CANDIDATES_CSV), newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                candidates.append(dict(row))
        logger.info("Loaded %d candidates from %s", len(candidates), CANDIDATES_CSV)
    except Exception as exc:
        logger.error("Failed to read candidates CSV: %s", exc)
    return candidates


def _demo_candidates() -> list:
    """Return a small set of demo candidates for first-run / testing."""
    return [
        {
            "id": "C001",
            "name": "Invoice Reminder SaaS",
            "problem_description": "Freelancers forget to chase late invoices every month and lose money.",
            "frequency_claim": "Happens monthly for every freelancer with clients",
            "target_mrr": "800",
        },
        {
            "id": "C002",
            "name": "Wedding Seating Planner",
            "problem_description": "Couple needs to arrange seating once for their wedding.",
            "frequency_claim": "One-time event, never happens again",
            "target_mrr": "200",
        },
        {
            "id": "C003",
            "name": "Inventory Reorder Alert",
            "problem_description": "Small shop owners run out of stock weekly and miss sales.",
            "frequency_claim": "Weekly recurring pain for every retailer",
            "target_mrr": "600",
        },
        {
            "id": "C004",
            "name": "New-Employee Onboarding Kit",
            "problem_description": "HR needs to onboard each new hire but hires are rare and irregular.",
            "frequency_claim": "Occasional, isolated per new hire",
            "target_mrr": "150",
        },
        {
            "id": "C005",
            "name": "Social Media Scheduler",
            "problem_description": "Solopreneurs need to post consistently every week across platforms.",
            "frequency_claim": "Recurring daily/weekly posting requirement",
            "target_mrr": "700",
        },
    ]


# ---------------------------------------------------------------------------
# Scoring engine
# ---------------------------------------------------------------------------

def score_recurrence(candidate: dict) -> dict:
    """Score a candidate on recurring-pain criteria.  Returns enriched dict."""
    text = " ".join([
        candidate.get("problem_description", ""),
        candidate.get("frequency_claim", ""),
    ]).lower()

    recurring_hits = [kw for kw in RECURRING_KEYWORDS if kw in text]
    one_time_hits = [kw for kw in ONE_TIME_KEYWORDS if kw in text]

    recurrence_score = min(len(recurring_hits) * 20, 80)
    one_time_penalty = min(len(one_time_hits) * 25, 80)
    raw_score = max(0, recurrence_score - one_time_penalty)

    # Bonus: explicit high-frequency words give a bump
    high_freq_bonus = 20 if any(kw in text for kw in ("weekly", "daily", "monthly", "every")) else 0
    final_score = min(100, raw_score + high_freq_bonus)

    passed = final_score >= RECURRENCE_PASS_THRESHOLD

    try:
        target_mrr = float(candidate.get("target_mrr", 0))
    except (ValueError, TypeError):
        target_mrr = 0.0

    return {
        "id": candidate.get("id", "unknown"),
        "name": candidate.get("name", "unnamed"),
        "problem_description": candidate.get("problem_description", ""),
        "frequency_claim": candidate.get("frequency_claim", ""),
        "target_mrr": target_mrr,
        "recurrence_score": final_score,
        "recurring_keywords_found": recurring_hits,
        "one_time_keywords_found": one_time_hits,
        "passed": passed,
        "rejection_reason": None if passed else (
            "Score %d below threshold %d — problem does not appear to recur regularly."
            % (final_score, RECURRENCE_PASS_THRESHOLD)
        ),
        "evaluated_at": datetime.utcnow().isoformat() + "Z",
    }


# ---------------------------------------------------------------------------
# Result persistence
# ---------------------------------------------------------------------------

def save_results(results: list, dry_run: bool, logger: logging.Logger) -> None:
    passed = [r for r in results if r["passed"]]
    rejected = [r for r in results if not r["passed"]]

    if dry_run:
        logger.info("[DRY-RUN] Would write %d passed and %d rejected results.", len(passed), len(rejected))
        return

    try:
        RESULTS_JSON.parent.mkdir(parents=True, exist_ok=True)
        with open(safe_path(RESULTS_JSON), "w", encoding="utf-8") as fh:
            json.dump({"generated_at": datetime.utcnow().isoformat() + "Z", "results": passed}, fh, indent=2)
        logger.info("Saved %d passed candidates to %s", len(passed), RESULTS_JSON)
    except Exception as exc:
        logger.error("Failed to write results JSON: %s", exc)

    try:
        with open(safe_path(REJECTED_JSON), "w", encoding="utf-8") as fh:
            json.dump({"generated_at": datetime.utcnow().isoformat() + "Z", "rejected": rejected}, fh, indent=2)
        logger.info("Saved %d rejected candidates to %s", len(rejected), REJECTED_JSON)
    except Exception as exc:
        logger.error("Failed to write rejected JSON: %s", exc)


# ---------------------------------------------------------------------------
# Optional: notify via webhook (no exotic deps — plain urllib)
# ---------------------------------------------------------------------------

def _maybe_notify(results: list, logger: logging.Logger) -> None:
    """Post a summary to a webhook URL stored in AUTOMATIONS/config/webhook.json, if present."""
    webhook_cfg = safe_path(AUTOMATIONS_DIR / "config" / "webhook.json")
    if not webhook_cfg.exists():
        return
    try:
        with open(safe_path(webhook_cfg), encoding="utf-8") as fh:
            cfg = json.load(fh)
        url = cfg.get("recurring_filter_webhook_url", "")
        if not url:
            return
        passed_count = sum(1 for r in results if r["passed"])
        rejected_count = len(results) - passed_count
        payload = json.dumps({
            "hook": "app_factory_recurring_filter",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "passed": passed_count,
            "rejected": rejected_count,
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            logger.info("Webhook notified — HTTP %s", resp.status)
    except urllib.error.URLError as exc:
        logger.warning("Webhook notification failed (network): %s", exc)
    except Exception as exc:
        logger.warning("Webhook notification failed: %s", exc)


# ---------------------------------------------------------------------------
# Sub-commands
# ---------------------------------------------------------------------------

def run(dry_run: bool, logger: logging.Logger) -> int:
    """Score all candidates and persist results."""
    logger.info("=== App Factory Recurring Filter — %s ===", "DRY-RUN" if dry_run else "RUN")

    # Optional: pull latest candidates via git if inside a repo
    try:
        subprocess.run(
            ["git", "-C", str(PROJECT), "pull", "--ff-only", "--quiet"],
            capture_output=True, timeout=30, check=False,
        )
    except Exception:
        pass  # Not a blocking failure; local data is fine

    candidates = load_candidates(logger)
    if not candidates:
        logger.warning("No candidates to evaluate.")
        return 0

    results = []
    for candidate in candidates:
        scored = score_recurrence(candidate)
        status = "PASS" if scored["passed"] else "REJECT"
        logger.info(
            "[%s] %s | score=%d | mrr=$%s | %s",
            status,
            scored["name"],
            scored["recurrence_score"],
            scored["target_mrr"],
            scored.get("rejection_reason") or "qualifies for build slot",
        )
        results.append(scored)

    passed = [r for r in results if r["passed"]]
    rejected = [r for r in results if not r["passed"]]
    logger.info(
        "Summary: %d/%d passed recurrence filter (threshold=%d).",
        len(passed), len(results), RECURRENCE_PASS_THRESHOLD,
    )

    # Capture skill insight for future runs (no-op when _common is absent)
    try:
        capture_skill_from_result(
            "recurring_painpoint_filter",
            {
                "passed": len(passed),
                "rejected": len(rejected),
                "threshold": RECURRENCE_PASS_THRESHOLD,
                "top_rejected": [r["name"] for r in rejected[:3]],
            },
        )
    except Exception:
        pass

    save_results(results, dry_run, logger)
    _maybe_notify(results, logger)
    return 0


def status(logger: logging.Logger) -> int:
    """Print status of last filter run from persisted JSON files."""
    logger.info("=== App Factory Recurring Filter — STATUS ===")
    for label, path in [("Passed", RESULTS_JSON), ("Rejected", REJECTED_JSON)]:
        if not path.exists():
            logger.info("%s results file not found: %s", label, path)
            continue
        try:
            with open(safe_path(path), encoding="utf-8") as fh:
                data = json.load(fh)
            key = "results" if "results" in data else "rejected"
            entries = data.get(key, [])
            generated = data.get("generated_at", "unknown")
            logger.info(
                "%s: %d entries (generated %s)",
                label, len(entries), generated,
            )
            for entry in entries:
                logger.info(
                    "  • [%s] score=%d mrr=$%s",
                    entry.get("name", "?"),
                    entry.get("recurrence_score", 0),
                    entry.get("target_mrr", "?"),
                )
        except Exception as exc:
            logger.error("Failed to read %s: %s", path, exc)
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX – App Factory Recurring Filter Hook",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Scores app factory candidates on recurring-pain criteria.\n"
            "Rejects one-time-problem apps before build slots are allocated."
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", action="store_true", help="Score candidates and persist results.")
    group.add_argument("--status", action="store_true", help="Show results from the last run.")
    group.add_argument("--dry-run", action="store_true", help="Score candidates without writing files.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    dry_run = args.dry_run
    logger = setup_logging(dry_run=dry_run)

    try:
        if args.run or args.dry_run:
            sys.exit(run(dry_run=dry_run, logger=logger))
        elif args.status:
            sys.exit(status(logger=logger))
    except KeyboardInterrupt:
        logger.info("Interrupted.")
        sys.exit(0)
    except Exception as exc:
        logging.getLogger("recurring_filter").error("Unhandled error: %s", exc, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()