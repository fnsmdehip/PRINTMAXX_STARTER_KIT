#!/usr/bin/env python3
"""
Alpha Review Bot — Automated PENDING_REVIEW Processor
=====================================================
Batch-processes PENDING_REVIEW entries in ALPHA_STAGING.csv.
Uses keyword/pattern matching for obvious cases, flags ambiguous ones.
Routes approved entries to category-specific integration targets.

Usage:
    python3 AUTOMATIONS/alpha_review_bot.py                  # Process 50 entries (default)
    python3 AUTOMATIONS/alpha_review_bot.py --batch 100      # Process 100 entries
    python3 AUTOMATIONS/alpha_review_bot.py --dry-run        # Preview without writing
    python3 AUTOMATIONS/alpha_review_bot.py --status         # Show backlog stats

Cron:
    0 6 * * * cd $BASE && python3 AUTOMATIONS/alpha_review_bot.py --batch 100 >> AUTOMATIONS/logs/alpha_review.log 2>&1
"""

import csv
import os
import re
import sys
import json
from datetime import datetime
from pathlib import Path

# --- Config ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ALPHA_STAGING = PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv"
REVIEW_LOG = PROJECT_ROOT / "LEDGER" / "ALPHA_REVIEW_LOG.csv"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"
LOG_FILE = LOG_DIR / "alpha_review.log"

# Integration targets for approved entries
INTEGRATION_TARGETS = {
    "APP_FACTORY": PROJECT_ROOT / "LEDGER" / "APP_FACTORY_METHODS.csv",
    "OUTBOUND": PROJECT_ROOT / "LEDGER" / "MARKETING_CHANNELS_MASTER.csv",
    "CONTENT_FORMAT": PROJECT_ROOT / "LEDGER" / "WINNING_CONTENT_STRUCTURES.csv",
    "CONTENT_FARM": PROJECT_ROOT / "LEDGER" / "WINNING_CONTENT_STRUCTURES.csv",
    "TOOL_ALPHA": PROJECT_ROOT / "LEDGER" / "TOOL_ALPHA_APPROVED.csv",
    "MONETIZATION": PROJECT_ROOT / "LEDGER" / "MONETIZATION_APPROVED.csv",
    "GROWTH_HACK": PROJECT_ROOT / "LEDGER" / "MARKETING_CHANNELS_MASTER.csv",
    "SEO_GEO_ASO": PROJECT_ROOT / "LEDGER" / "GTM_OPTIMIZATION_PRIORITIES.csv",
}

# --- Path Safety ---
def safe_path(target):
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_FILE), "a") as f:
        f.write(line + "\n")


# --- Pattern Matching ---

# Regex patterns for specific numbers (strong signal of real alpha)
SPECIFIC_NUMBERS_RE = re.compile(
    r'(\$[\d,]+\.?\d*)|(\d+%)|(\d+[KkMm]\b)|(\d+x\b)|(\d+\.\d+x)|(\d+/\d+)|(\d+ (days?|hours?|min|sec|weeks?|months?))',
    re.IGNORECASE
)

# Round number detection (possible inflation)
ROUND_NUMBERS_RE = re.compile(r'\$\d0,000|\$\d00K|\$\dM', re.IGNORECASE)

# Engagement bait indicators
ENGAGEMENT_BAIT_PHRASES = [
    "opportunities are insane",
    "the game has changed",
    "this changes everything",
    "you need to see this",
    "stop scrolling",
    "most people don't know",
    "secret to",
    "you won't believe",
    "the truth about",
    "nobody talks about",
    "they don't want you to know",
]

# Strong method indicators
METHOD_INDICATORS = [
    "step 1", "step 2", "step 3",
    "framework", "playbook", "template",
    "here's how", "here's what I did",
    "exact process", "breakdown",
    "cold email", "outreach", "funnel",
    "conversion rate", "reply rate",
    "pricing", "tier", "subscription",
]

# Categories that map to specific integration targets
CATEGORY_KEYWORDS = {
    "APP_FACTORY": ["app", "pwa", "ios", "android", "mobile", "revenueCat", "paywall", "onboarding"],
    "OUTBOUND": ["cold email", "outreach", "reply rate", "deliverability", "smtp", "warmup", "lead gen"],
    "CONTENT_FARM": ["tiktok", "youtube", "shorts", "reels", "instagram", "content", "posting", "algorithm"],
    "CONTENT_FORMAT": ["thread", "carousel", "hook", "caption", "viral", "format"],
    "TOOL_ALPHA": ["tool", "saas", "api", "mcp", "automation", "scraper", "n8n", "github"],
    "MONETIZATION": ["revenue", "pricing", "subscription", "affiliate", "gumroad", "stripe"],
    "GROWTH_HACK": ["growth", "hack", "organic", "acquisition", "seo", "aso"],
    "SEO_GEO_ASO": ["seo", "geo", "aso", "keyword", "ranking", "search"],
}


def classify_entry(row):
    """Classify a PENDING_REVIEW entry using pattern matching.
    Returns (status, category, confidence, reason)
    """
    tactic = (row.get("tactic", "") or "").lower()
    category = (row.get("category", "") or "").upper()
    reviewer_notes = (row.get("reviewer_notes", "") or "").lower()
    source = (row.get("source", "") or "").lower()
    roi = (row.get("roi_potential", "") or "").upper()
    combined_text = f"{tactic} {reviewer_notes} {source}"

    # Already has reviewer notes with clear signal
    if "approved" in reviewer_notes:
        return "APPROVED", category, 0.95, "Pre-approved in reviewer notes"

    # Check for specific numbers (strong signal)
    has_specific_numbers = bool(SPECIFIC_NUMBERS_RE.search(combined_text))
    has_round_numbers = bool(ROUND_NUMBERS_RE.search(combined_text))

    # Check for method indicators
    method_score = sum(1 for m in METHOD_INDICATORS if m in combined_text)

    # Check for engagement bait
    bait_score = sum(1 for b in ENGAGEMENT_BAIT_PHRASES if b in combined_text)

    # Determine category if not set
    if not category or category == "":
        for cat, keywords in CATEGORY_KEYWORDS.items():
            if any(kw in combined_text for kw in keywords):
                category = cat
                break
        if not category:
            category = "GENERAL"

    # Decision logic
    if bait_score >= 2 and method_score == 0:
        return "ENGAGEMENT_BAIT", category, 0.85, f"Engagement bait signals ({bait_score} phrases, 0 method indicators)"

    if has_specific_numbers and method_score >= 2:
        confidence = 0.90 if not has_round_numbers else 0.70
        return "APPROVED", category, confidence, f"Specific numbers + method indicators (method_score={method_score})"

    if has_specific_numbers and method_score >= 1:
        return "APPROVED", category, 0.75, f"Has numbers + partial method (method_score={method_score})"

    if method_score >= 3:
        return "APPROVED", category, 0.80, f"Strong method indicators ({method_score}) without specific numbers"

    if roi in ("HIGHEST", "HIGH") and has_specific_numbers:
        return "APPROVED", category, 0.70, f"High ROI + specific numbers"

    if roi in ("HIGHEST", "HIGH") and method_score >= 1:
        return "APPROVED", category, 0.65, f"High ROI + some method indicators"

    if has_specific_numbers:
        return "REPURPOSE_ONLY", category, 0.60, "Numbers present but no clear method"

    if bait_score >= 1:
        return "ENGAGEMENT_BAIT", category, 0.70, f"Some engagement bait signals ({bait_score})"

    # Ambiguous: flag for human review
    return "FLAGGED_FOR_HUMAN", category, 0.40, "Ambiguous: no strong signal either way"


def load_csv(path):
    safe = safe_path(path)
    if not safe.exists():
        return []
    with open(safe, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv(path, rows, fieldnames=None):
    safe = safe_path(path)
    if not rows:
        return
    if fieldnames is None:
        fieldnames = rows[0].keys()
    safe.parent.mkdir(parents=True, exist_ok=True)
    with open(safe, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_review_log(entry):
    safe = safe_path(REVIEW_LOG)
    safe.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["alpha_id", "old_status", "new_status", "category", "confidence", "reason", "reviewed_at"]
    write_header = not safe.exists()
    with open(safe, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(entry)


def show_status():
    rows = load_csv(ALPHA_STAGING)
    if not rows:
        log("ALPHA_STAGING.csv not found or empty")
        return

    status_counts = {}
    for r in rows:
        s = r.get("status", "UNKNOWN")
        status_counts[s] = status_counts.get(s, 0) + 1

    log("=== ALPHA_STAGING Backlog Status ===")
    total = len(rows)
    for status, count in sorted(status_counts.items(), key=lambda x: -x[1]):
        pct = (count / total * 100) if total > 0 else 0
        log(f"  {status}: {count} ({pct:.1f}%)")
    log(f"  TOTAL: {total}")

    pending = status_counts.get("PENDING_REVIEW", 0)
    if pending > 0:
        log(f"\n  At 100/day processing rate, backlog cleared in ~{(pending + 99) // 100} days")


def process_batch(batch_size=50, dry_run=False):
    rows = load_csv(ALPHA_STAGING)
    if not rows:
        log("ERROR: ALPHA_STAGING.csv not found or empty")
        return

    # Get fieldnames from the existing file
    with open(safe_path(ALPHA_STAGING), "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

    # Filter PENDING_REVIEW entries
    pending_indices = [i for i, r in enumerate(rows) if r.get("status", "").strip() == "PENDING_REVIEW"]
    log(f"Found {len(pending_indices)} PENDING_REVIEW entries")

    if not pending_indices:
        log("No PENDING_REVIEW entries to process")
        return

    # Process batch
    to_process = pending_indices[:batch_size]
    log(f"Processing batch of {len(to_process)} entries...")

    stats = {"APPROVED": 0, "ENGAGEMENT_BAIT": 0, "REPURPOSE_ONLY": 0, "FLAGGED_FOR_HUMAN": 0}

    for idx in to_process:
        row = rows[idx]
        alpha_id = row.get("alpha_id", f"row_{idx}")
        new_status, category, confidence, reason = classify_entry(row)

        stats[new_status] = stats.get(new_status, 0) + 1

        if not dry_run:
            # Update the row
            rows[idx]["status"] = new_status
            if not rows[idx].get("category"):
                rows[idx]["category"] = category
            rows[idx]["reviewer_notes"] = (
                f"[AUTO {datetime.now().strftime('%Y-%m-%d')}] {reason} (conf={confidence:.0%}). "
                + (row.get("reviewer_notes", "") or "")
            )

            # Log the review decision
            append_review_log({
                "alpha_id": alpha_id,
                "old_status": "PENDING_REVIEW",
                "new_status": new_status,
                "category": category,
                "confidence": f"{confidence:.2f}",
                "reason": reason,
                "reviewed_at": datetime.now().isoformat(),
            })

        log(f"  {alpha_id}: PENDING_REVIEW -> {new_status} ({category}, {confidence:.0%}) - {reason[:60]}")

    if not dry_run:
        write_csv(ALPHA_STAGING, rows, fieldnames=fieldnames)
        log(f"\nUpdated ALPHA_STAGING.csv")

    # Summary
    log(f"\n=== Batch Summary ===")
    for status, count in sorted(stats.items(), key=lambda x: -x[1]):
        log(f"  {status}: {count}")
    log(f"  TOTAL PROCESSED: {len(to_process)}")

    remaining = len(pending_indices) - len(to_process)
    log(f"  REMAINING PENDING_REVIEW: {remaining}")

    if dry_run:
        log("\n  [DRY RUN - no changes written]")


def main():
    args = sys.argv[1:]

    batch_size = 50
    dry_run = False

    i = 0
    while i < len(args):
        if args[i] == "--batch" and i + 1 < len(args):
            batch_size = int(args[i + 1])
            i += 2
        elif args[i] == "--dry-run":
            dry_run = True
            i += 1
        elif args[i] == "--status":
            show_status()
            return
        else:
            i += 1

    log(f"Alpha Review Bot starting (batch={batch_size}, dry_run={dry_run})")
    process_batch(batch_size=batch_size, dry_run=dry_run)
    log("Alpha Review Bot complete")


if __name__ == "__main__":
    main()
