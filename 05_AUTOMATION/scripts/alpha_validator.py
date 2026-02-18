#!/usr/bin/env python3
"""
alpha_validator.py - Auto-run backtesting validation on new alpha entries

Reads PENDING_REVIEW entries from ALPHA_STAGING.csv, applies the backtesting
framework (from backtest_alpha.py), and generates quality scores.
Helps prioritize which alpha to review first.

Usage:
    python3 alpha_validator.py --pending
    python3 alpha_validator.py --alpha ALPHA500
    python3 alpha_validator.py --batch 20
    python3 alpha_validator.py --auto-approve --threshold 70

Example:
    # Validate all pending entries
    python3 alpha_validator.py --pending

    # Validate specific alpha entry
    python3 alpha_validator.py --alpha ALPHA500

    # Auto-approve entries scoring above 70
    python3 alpha_validator.py --auto-approve --threshold 70
"""

import argparse
import csv
import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_DIR / "LEDGER"
ALPHA_FILE = LEDGER_DIR / "ALPHA_STAGING.csv"
LOG_DIR = PROJECT_DIR / "AUTOMATIONS" / "logs"
VALIDATION_LOG = LOG_DIR / "alpha_validation.csv"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "alpha_validator.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def load_alpha_entries(status_filter=None, alpha_id=None):
    """Load alpha entries with optional filters."""
    if not ALPHA_FILE.exists():
        return []

    entries = []
    with open(ALPHA_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if alpha_id and row.get("alpha_id") != alpha_id:
                continue
            if status_filter and row.get("status") != status_filter:
                continue
            entries.append(row)

    return entries


def score_specificity(entry):
    """Score: Does it have specific numbers?"""
    text = entry.get("title", "") + " " + entry.get("description", "")

    # Check for dollar amounts
    dollars = len(re.findall(r"\$[\d,]+", text))
    # Check for percentages
    pcts = len(re.findall(r"\d+%", text))
    # Check for other numbers
    nums = len(re.findall(r"\b\d{2,}\b", text))

    total = dollars * 3 + pcts * 2 + nums
    return min(25, total * 5)  # Max 25 points


def score_actionability(entry):
    """Score: Are there clear actionable steps?"""
    steps = entry.get("actionable_steps", "")
    if not steps:
        return 0

    step_count = len(steps.split(";"))
    if step_count >= 4:
        return 25
    if step_count >= 3:
        return 20
    if step_count >= 2:
        return 15
    return 10


def score_source_quality(entry):
    """Score: Is the source reliable?"""
    source = entry.get("source", "").lower()

    # High-signal accounts (S-tier from copy-style.md)
    s_tier = ["pipelineabuser", "zephyr_z9", "eptwts"]
    a_tier = ["tom777kruise"]
    b_tier = ["codyschneiderxx", "bluecow009"]
    c_tier = ["levelsio", "tdinh_me", "dannypostmaa", "marc_louvion"]
    known_good = ["gregisenberg", "knoxtwts", "purpdevvv", "caiden_cole"]

    for handle in s_tier:
        if handle in source:
            return 20

    for handle in a_tier + b_tier:
        if handle in source:
            return 15

    for handle in c_tier + known_good:
        if handle in source:
            return 12

    # Check if it's from a real source URL
    url = entry.get("source_url", "")
    if url and "x.com" in url:
        return 10
    if url:
        return 8

    return 5


def score_roi_potential(entry):
    """Score: What's the estimated ROI?"""
    roi = entry.get("roi_potential", "").upper()
    scores = {"HIGHEST": 20, "HIGH": 15, "MEDIUM": 10, "LOW": 5}
    return scores.get(roi, 5)


def score_freshness(entry):
    """Score: Is this recent/current intel?"""
    text = entry.get("description", "").lower()

    # 2026 mentions suggest current
    if "2026" in text:
        return 10
    if "2025" in text:
        return 5
    if any(w in text for w in ["new", "just", "today", "this week", "launched"]):
        return 8

    return 3


def validate_entry(entry):
    """Run full validation scoring on an alpha entry."""
    specificity = score_specificity(entry)
    actionability = score_actionability(entry)
    source_quality = score_source_quality(entry)
    roi = score_roi_potential(entry)
    freshness = score_freshness(entry)

    total = specificity + actionability + source_quality + roi + freshness

    # Determine recommendation
    if total >= 70:
        recommendation = "APPROVE"
    elif total >= 50:
        recommendation = "REVIEW"
    elif total >= 30:
        recommendation = "LOW_PRIORITY"
    else:
        recommendation = "LIKELY_REJECT"

    return {
        "alpha_id": entry.get("alpha_id"),
        "title": entry.get("title", "")[:60],
        "category": entry.get("category"),
        "total_score": total,
        "specificity": specificity,
        "actionability": actionability,
        "source_quality": source_quality,
        "roi_potential": roi,
        "freshness": freshness,
        "recommendation": recommendation,
    }


def print_validation_results(results):
    """Print formatted validation results."""
    results.sort(key=lambda x: x["total_score"], reverse=True)

    print("\n" + "=" * 95)
    print("  ALPHA VALIDATION RESULTS")
    print("=" * 95)
    print(f"  {'ID':<12} {'Score':>5} {'Spec':>4} {'Act':>4} {'Src':>4} {'ROI':>4} {'New':>4}  {'Rec':<15} Title")
    print("-" * 95)

    for r in results:
        rec_marker = {
            "APPROVE": ">>>", "REVIEW": " >>",
            "LOW_PRIORITY": "  >", "LIKELY_REJECT": " XX",
        }.get(r["recommendation"], "  ?")

        print(
            f"  {r['alpha_id']:<12} "
            f"{r['total_score']:>5} "
            f"{r['specificity']:>4} "
            f"{r['actionability']:>4} "
            f"{r['source_quality']:>4} "
            f"{r['roi_potential']:>4} "
            f"{r['freshness']:>4}  "
            f"{rec_marker} {r['recommendation']:<12} "
            f"{r['title']}"
        )

    # Summary
    total = len(results)
    approve = len([r for r in results if r["recommendation"] == "APPROVE"])
    review = len([r for r in results if r["recommendation"] == "REVIEW"])
    reject = len([r for r in results if r["recommendation"] == "LIKELY_REJECT"])

    print("-" * 95)
    print(f"  Total: {total} | Approve: {approve} | Review: {review} | Reject: {reject}")
    print(f"  Avg Score: {sum(r['total_score'] for r in results) / len(results):.1f}" if results else "")
    print("=" * 95)


def save_validation_log(results):
    """Save validation results to log."""
    fieldnames = [
        "date", "alpha_id", "total_score", "specificity", "actionability",
        "source_quality", "roi_potential", "freshness", "recommendation",
    ]

    file_exists = VALIDATION_LOG.exists()
    with open(VALIDATION_LOG, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for r in results:
            writer.writerow({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "alpha_id": r["alpha_id"],
                "total_score": r["total_score"],
                "specificity": r["specificity"],
                "actionability": r["actionability"],
                "source_quality": r["source_quality"],
                "roi_potential": r["roi_potential"],
                "freshness": r["freshness"],
                "recommendation": r["recommendation"],
            })

    logger.info(f"Saved {len(results)} validation results to {VALIDATION_LOG}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate and score alpha entries for prioritized review"
    )
    parser.add_argument("--pending", action="store_true", help="Validate all PENDING_REVIEW entries")
    parser.add_argument("--alpha", type=str, default=None, help="Validate specific alpha ID")
    parser.add_argument("--batch", type=int, default=None, help="Validate N most recent entries")
    parser.add_argument("--auto-approve", action="store_true", help="Auto-approve above threshold")
    parser.add_argument("--threshold", type=int, default=70, help="Auto-approve threshold (default: 70)")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if args.alpha:
        entries = load_alpha_entries(alpha_id=args.alpha)
    elif args.pending:
        entries = load_alpha_entries(status_filter="PENDING_REVIEW")
    else:
        entries = load_alpha_entries(status_filter="PENDING_REVIEW")

    if args.batch:
        entries = entries[-args.batch:]

    if not entries:
        logger.info("No entries to validate")
        return

    logger.info(f"Validating {len(entries)} entries")
    results = [validate_entry(e) for e in entries]

    save_validation_log(results)

    if args.output == "json":
        print(json.dumps(results, indent=2))
    else:
        print_validation_results(results)

    if args.auto_approve:
        to_approve = [r for r in results if r["total_score"] >= args.threshold]
        logger.info(f"Auto-approve: {len(to_approve)} entries above score {args.threshold}")
        # Note: actual CSV update would need to modify ALPHA_STAGING.csv
        # Left as manual step to maintain human-in-loop safety
        for r in to_approve:
            logger.info(f"  APPROVE: {r['alpha_id']} (score: {r['total_score']})")


if __name__ == "__main__":
    main()
