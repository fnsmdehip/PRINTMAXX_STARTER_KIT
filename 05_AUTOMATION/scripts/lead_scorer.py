#!/usr/bin/env python3
"""
lead_scorer.py - Score leads for outreach prioritization

Reads lead data from LEDGER/leads.csv or outreach pipeline,
scores each lead based on multiple signals (company size, industry,
engagement, timing), and outputs a prioritized list.

Usage:
    python3 lead_scorer.py
    python3 lead_scorer.py --file LEDGER/leads.csv
    python3 lead_scorer.py --threshold 50
    python3 lead_scorer.py --top 20

Example:
    # Score all leads
    python3 lead_scorer.py

    # Show only leads scoring above 50
    python3 lead_scorer.py --threshold 50

    # Top 20 leads for immediate outreach
    python3 lead_scorer.py --top 20
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
LOG_DIR = PROJECT_DIR / "AUTOMATIONS" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "lead_scorer.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Industry value scores (higher = more likely to buy)
INDUSTRY_SCORES = {
    "saas": 25, "software": 25, "tech": 20, "fintech": 25,
    "ecommerce": 20, "agency": 20, "marketing": 20,
    "healthcare": 15, "legal": 15, "real estate": 15,
    "finance": 15, "consulting": 20, "education": 10,
    "retail": 10, "manufacturing": 5, "nonprofit": 5,
}

# Email domain quality scores
DOMAIN_SCORES = {
    "gmail.com": 5, "yahoo.com": 3, "hotmail.com": 3,
    "outlook.com": 5, "icloud.com": 5,
}


def load_leads(filepath=None):
    """Load leads from CSV."""
    if filepath:
        path = Path(filepath)
        if not path.is_absolute():
            path = PROJECT_DIR / filepath
    else:
        # Try multiple locations
        for candidate in [
            LEDGER_DIR / "leads.csv",
            LEDGER_DIR / "OUTREACH_PIPELINE.csv",
        ]:
            if candidate.exists():
                path = candidate
                break
        else:
            logger.error("No lead file found")
            return []

    if not path.exists():
        logger.error(f"File not found: {path}")
        return []

    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def score_lead(lead):
    """Score a single lead (0-100)."""
    score = 0
    signals = []

    # 1. Email quality (0-15)
    email = lead.get("email", "").lower()
    if email:
        domain = email.split("@")[-1] if "@" in email else ""
        if domain in DOMAIN_SCORES:
            score += DOMAIN_SCORES[domain]
            signals.append(f"personal_email:{DOMAIN_SCORES[domain]}")
        elif domain:
            score += 15  # Custom domain = business email
            signals.append("business_email:15")

    # 2. Industry match (0-25)
    industry = lead.get("industry", lead.get("niche", "")).lower()
    for ind, ind_score in INDUSTRY_SCORES.items():
        if ind in industry:
            score += ind_score
            signals.append(f"industry:{ind_score}")
            break

    # 3. Has website/company (0-10)
    if lead.get("website") or lead.get("company"):
        score += 10
        signals.append("has_company:10")

    # 4. Source quality (0-15)
    source = lead.get("source", "").lower()
    if source in ("referral", "inbound"):
        score += 15
        signals.append("warm_source:15")
    elif source in ("cold_email", "linkedin"):
        score += 5
        signals.append("cold_source:5")
    elif source in ("organic", "seo"):
        score += 10
        signals.append("organic_source:10")

    # 5. Engagement signals (0-20)
    if lead.get("opened_email", "").upper() == "TRUE":
        score += 10
        signals.append("opened:10")
    if lead.get("clicked_link", "").upper() == "TRUE":
        score += 10
        signals.append("clicked:10")
    if lead.get("replied", "").upper() == "TRUE":
        score += 20
        signals.append("replied:20")

    # 6. Recency (0-15)
    date_str = lead.get("date", lead.get("created_date", ""))
    if date_str:
        try:
            lead_date = datetime.strptime(date_str, "%Y-%m-%d")
            days_old = (datetime.now() - lead_date).days
            if days_old <= 3:
                score += 15
                signals.append("very_recent:15")
            elif days_old <= 7:
                score += 10
                signals.append("recent:10")
            elif days_old <= 30:
                score += 5
                signals.append("this_month:5")
        except ValueError:
            pass

    return min(100, score), signals


def score_all_leads(leads):
    """Score all leads and return sorted results."""
    results = []
    for lead in leads:
        score, signals = score_lead(lead)
        results.append({
            "email": lead.get("email", ""),
            "name": lead.get("name", lead.get("first_name", "")),
            "company": lead.get("company", ""),
            "industry": lead.get("industry", lead.get("niche", "")),
            "source": lead.get("source", ""),
            "score": score,
            "signals": signals,
            "priority": get_priority(score),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def get_priority(score):
    """Determine priority tier."""
    if score >= 70:
        return "HOT"
    if score >= 50:
        return "WARM"
    if score >= 30:
        return "COOL"
    return "COLD"


def print_results(results, top=None, threshold=None):
    """Print scored leads."""
    if threshold is not None:
        results = [r for r in results if r["score"] >= threshold]
    if top:
        results = results[:top]

    print("\n" + "=" * 80)
    print("  LEAD SCORING RESULTS")
    print("=" * 80)
    print(f"  {'Score':>5} {'Pri':<5} {'Email':<30} {'Company':<20} Signals")
    print("-" * 80)

    for r in results:
        signals_str = ", ".join(r["signals"][:3])
        print(
            f"  {r['score']:>5} "
            f"{r['priority']:<5} "
            f"{r['email']:<30} "
            f"{r['company'][:20]:<20} "
            f"{signals_str}"
        )

    # Summary
    hot = len([r for r in results if r["priority"] == "HOT"])
    warm = len([r for r in results if r["priority"] == "WARM"])
    cool = len([r for r in results if r["priority"] == "COOL"])
    cold = len([r for r in results if r["priority"] == "COLD"])

    print("-" * 80)
    print(f"  Total: {len(results)} | HOT: {hot} | WARM: {warm} | COOL: {cool} | COLD: {cold}")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Score and prioritize leads for outreach"
    )
    parser.add_argument("--file", type=str, default=None, help="Lead CSV file path")
    parser.add_argument("--top", type=int, default=None, help="Show top N leads")
    parser.add_argument("--threshold", type=int, default=None, help="Minimum score to show")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    leads = load_leads(args.file)
    if not leads:
        logger.error("No leads loaded")
        sys.exit(1)

    results = score_all_leads(leads)

    if args.output == "json":
        if args.threshold:
            results = [r for r in results if r["score"] >= args.threshold]
        if args.top:
            results = results[:args.top]
        print(json.dumps(results, indent=2))
    else:
        print_results(results, top=args.top, threshold=args.threshold)


if __name__ == "__main__":
    main()
