#!/usr/bin/env python3

from __future__ import annotations
"""
ALPHA QUERY — Pull relevant intelligence for any venture/task.

When building something, agents should query this FIRST to base decisions
on accumulated alpha intelligence, not default LLM knowledge.

Usage:
    python3 alpha_query.py --venture APP_FACTORY         # All app-related alpha
    python3 alpha_query.py --venture OUTBOUND             # All outbound/cold email alpha
    python3 alpha_query.py --venture CONTENT              # Content strategy alpha
    python3 alpha_query.py --venture LOCAL_BIZ            # Local business alpha
    python3 alpha_query.py --venture MONETIZATION         # Revenue/pricing alpha
    python3 alpha_query.py --category TOOL_ALPHA          # By category
    python3 alpha_query.py --search "mobile app pricing"  # Keyword search across all fields
    python3 alpha_query.py --top 20                       # Top 20 by ROI potential
    python3 alpha_query.py --venture APP_FACTORY --status APPROVED --top 10
    python3 alpha_query.py --stats                        # Show alpha distribution stats
    python3 alpha_query.py --untagged                     # Show entries needing categorization
"""

import argparse
import csv
csv.field_size_limit(10 * 1024 * 1024)
import json
import re
import sys
from pathlib import Path
from collections import Counter

PROJECT = Path(__file__).resolve().parent.parent
ALPHA_CSV = PROJECT / "LEDGER" / "ALPHA_STAGING.csv"

# Maps venture types to relevant alpha categories and keywords
VENTURE_ALPHA_MAP = {
    "APP_FACTORY": {
        "categories": ["APP_FACTORY", "MONETIZATION", "SEO_GEO_ASO"],
        "keywords": ["app", "mobile", "ios", "android", "aso", "app store", "play store",
                      "pwa", "react native", "flutter", "download", "install", "streak",
                      "tracker", "subscription", "in-app", "freemium", "retention"],
        "methods": ["APP_FACTORY", "APP"],
    },
    "OUTBOUND": {
        "categories": ["OUTBOUND", "FREELANCE"],
        "keywords": ["cold email", "outbound", "lead gen", "prospecting", "reply rate",
                      "email sequence", "warmup", "deliverability", "instantly", "smartlead",
                      "cold dm", "linkedin", "b2b", "pipeline", "close rate"],
        "methods": ["OUTBOUND", "COLD_EMAIL", "FREELANCE"],
    },
    "CONTENT": {
        "categories": ["CONTENT_FORMAT", "CONTENT_FARM", "GROWTH_HACK"],
        "keywords": ["content", "twitter", "thread", "viral", "hook", "engagement",
                      "posting", "social media", "distribution", "newsletter", "audience",
                      "niche account", "faceless", "ugc", "youtube", "tiktok", "reels",
                      "boomer", "55-70", "facebook page", "long-form", "educational",
                      "authoritative", "voiceover"],
        "methods": ["CONTENT", "CONTENT_FARM", "SOCIAL"],
    },
    "LOCAL_BIZ": {
        "categories": ["FREELANCE", "OUTBOUND"],
        "keywords": ["local business", "small business", "smb", "agency", "web design",
                      "seo", "google business", "local seo", "plumber", "dentist",
                      "restaurant", "contractor", "hvac", "landscaping", "demo site"],
        "methods": ["LOCAL_BIZ", "OPENCLAW"],
    },
    "MONETIZATION": {
        "categories": ["MONETIZATION", "ECOM", "ECOM_ARB"],
        "keywords": ["revenue", "pricing", "monetize", "gumroad", "whop", "stripe",
                      "subscription", "saas", "mrr", "arr", "convert", "funnel",
                      "checkout", "payment", "affiliate", "commission", "passive",
                      "boomer", "55-70", "disposable income", "health supplements",
                      "golf", "fishing", "tools", "faceless", "aov", "cpm",
                      "api arbitrage", "api wrapper", "mcp marketplace", "mcphub",
                      "featured listing", "pod", "print on demand", "tiktok shop",
                      "platform arbitrage", "cross-post", "beehiiv affiliate",
                      "semrush affiliate", "instantly affiliate", "cookie duration"],
        "methods": ["DIGITAL_PRODUCTS", "MONETIZE", "ECOM"],
    },
    "RESEARCH": {
        "categories": ["TOOL_ALPHA", "AI_ALPHA", "GENERAL"],
        "keywords": ["ai", "automation", "tool", "scraper", "api", "workflow",
                      "claude", "gpt", "agent", "llm", "prompt", "pipeline"],
        "methods": ["RESEARCH", "AI_ALPHA"],
    },
    "PRODUCT": {
        "categories": ["MONETIZATION", "ECOM"],
        "keywords": ["product", "digital product", "ebook", "template", "course",
                      "pdf", "notion", "playbook", "toolkit", "bundle", "gumroad",
                      "api wrapper", "github repurpose", "splice", "mit license",
                      "mcp server", "mcp marketplace", "pod", "merch", "t-shirt",
                      "redbubble", "etsy", "printful", "printify", "synergy stack"],
        "methods": ["DIGITAL_PRODUCTS", "PRODUCT"],
    },
    "SCRAPING": {
        "categories": ["TOOL_ALPHA", "AI_ALPHA"],
        "keywords": ["scrape", "scraper", "crawl", "monitor", "extract", "data",
                      "competitor", "intelligence", "signal", "alert"],
        "methods": ["SCRAPING", "RESEARCH"],
    },
}

ROI_ORDER = {"HIGHEST": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
VALID_ROI = {"HIGHEST", "HIGH", "MEDIUM", "LOW"}
VALID_STATUS = {"APPROVED", "PENDING_REVIEW", "ENGAGEMENT_BAIT", "REJECTED",
                "REPURPOSE_ONLY", "ARCHIVED", "UNCHECKED", "AUTHENTIC",
                "AUTO_APPROVED", "INTEGRATED", "FLAGGED_FOR_HUMAN",
                "ROUTED_TO_VENTURE", "COMPLIANCE_RISK", "SATIRICAL_ABSURDIST",
                "EXAGGERATED_BUT_SIGNAL"}


def normalize_roi(val):
    """Fix corrupted ROI values from CSV misalignment."""
    if not val:
        return ""
    v = val.strip().upper()
    if v in VALID_ROI:
        return v
    # Try to extract a valid ROI from a corrupted field
    for roi in VALID_ROI:
        if v.startswith(roi):
            return roi
    return ""


def load_alpha():
    """Load all alpha entries from CSV, fixing known data quality issues."""
    if not ALPHA_CSV.exists():
        print(f"ERROR: {ALPHA_CSV} not found")
        sys.exit(1)

    entries = []
    with open(ALPHA_CSV, newline='', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Normalize corrupted ROI values
            row["roi_potential"] = normalize_roi(row.get("roi_potential", ""))
            entries.append(row)
    return entries


def score_entry(entry, venture_config):
    """Score how relevant an alpha entry is to a venture type."""
    score = 0
    category = (entry.get("category") or "").upper()
    methods = (entry.get("applicable_methods") or "").upper()
    tactic = (entry.get("tactic") or "").lower()
    extracted = (entry.get("extracted_method") or "").lower()
    notes = (entry.get("reviewer_notes") or "").lower()
    full_text = f"{tactic} {extracted} {notes}"

    # Category match
    if category in venture_config["categories"]:
        score += 30

    # Method match
    for m in venture_config["methods"]:
        if m in methods:
            score += 20
            break

    # Keyword match (count how many keywords hit)
    keyword_hits = sum(1 for kw in venture_config["keywords"] if kw in full_text)
    score += keyword_hits * 5

    # ROI bonus
    roi = (entry.get("roi_potential") or "").upper()
    score += ROI_ORDER.get(roi, 0) * 5

    # Status bonus (APPROVED > others)
    status = (entry.get("status") or "").upper()
    if status == "APPROVED":
        score += 10
    elif status == "ENGAGEMENT_BAIT":
        score -= 5

    # Authenticity bonus
    auth = (entry.get("engagement_authenticity") or "").upper()
    if auth == "AUTHENTIC":
        score += 5
    elif auth == "SUSPICIOUS":
        score -= 3

    return score


def query_venture(entries, venture_type, status_filter=None, limit=20):
    """Query alpha entries relevant to a venture type."""
    venture_type = venture_type.upper()
    if venture_type not in VENTURE_ALPHA_MAP:
        print(f"Unknown venture: {venture_type}")
        print(f"Available: {', '.join(VENTURE_ALPHA_MAP.keys())}")
        sys.exit(1)

    config = VENTURE_ALPHA_MAP[venture_type]
    scored = []

    for entry in entries:
        if status_filter:
            if (entry.get("status") or "").upper() != status_filter.upper():
                continue
        s = score_entry(entry, config)
        if s > 0:
            scored.append((s, entry))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:limit]


def keyword_search(entries, query, limit=20):
    """Full-text keyword search across all alpha fields."""
    query_lower = query.lower()
    terms = query_lower.split()
    results = []

    for entry in entries:
        full_text = " ".join(str(v).lower() for v in entry.values())
        hits = sum(1 for t in terms if t in full_text)
        if hits > 0:
            score = hits * 10
            roi = (entry.get("roi_potential") or "").upper()
            score += ROI_ORDER.get(roi, 0) * 3
            if (entry.get("status") or "").upper() == "APPROVED":
                score += 5
            results.append((score, entry))

    results.sort(key=lambda x: x[0], reverse=True)
    return results[:limit]


def query_by_category(entries, category, limit=20):
    """Query by exact category match."""
    results = []
    for entry in entries:
        if (entry.get("category") or "").upper() == category.upper():
            roi = (entry.get("roi_potential") or "").upper()
            score = ROI_ORDER.get(roi, 0) * 10
            if (entry.get("status") or "").upper() == "APPROVED":
                score += 20
            results.append((score, entry))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:limit]


def top_alpha(entries, limit=20):
    """Get top alpha entries by ROI potential."""
    scored = []
    for entry in entries:
        if (entry.get("status") or "").upper() in ("REJECTED", "ARCHIVED"):
            continue
        roi = (entry.get("roi_potential") or "").upper()
        score = ROI_ORDER.get(roi, 0) * 10
        if (entry.get("status") or "").upper() == "APPROVED":
            score += 20
        auth = (entry.get("engagement_authenticity") or "").upper()
        if auth == "AUTHENTIC":
            score += 5
        scored.append((score, entry))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:limit]


def show_stats(entries):
    """Show alpha distribution stats."""
    cats = Counter((e.get("category") or "UNKNOWN").upper() for e in entries)
    statuses = Counter((e.get("status") or "UNKNOWN").upper() for e in entries)
    rois = Counter((e.get("roi_potential") or "UNKNOWN").upper() for e in entries)
    methods = Counter()
    for e in entries:
        m = (e.get("applicable_methods") or "").strip()
        if m and m != "N/A":
            for part in m.split("|"):
                methods[part.strip().upper()] += 1

    print(f"\nALPHA INTELLIGENCE STATS")
    print(f"{'='*50}")
    print(f"Total entries: {len(entries)}")
    print(f"\nBy Category:")
    for cat, count in cats.most_common(15):
        print(f"  {cat:25s} {count:5d}")
    print(f"\nBy Status:")
    for s, count in statuses.most_common(10):
        print(f"  {s:25s} {count:5d}")
    print(f"\nBy ROI Potential:")
    for r, count in rois.most_common():
        print(f"  {r:25s} {count:5d}")
    print(f"\nBy Applicable Method (top 15):")
    for m, count in methods.most_common(15):
        print(f"  {m:25s} {count:5d}")

    # Coverage analysis
    untagged = sum(1 for e in entries
                   if not (e.get("applicable_methods") or "").strip()
                   or (e.get("applicable_methods") or "").strip() == "N/A")
    print(f"\nCoverage:")
    print(f"  Tagged with methods:    {len(entries) - untagged:5d} ({(len(entries)-untagged)/len(entries)*100:.0f}%)")
    print(f"  Untagged (need routing): {untagged:5d} ({untagged/len(entries)*100:.0f}%)")


def format_result(score, entry, verbose=False):
    """Format a single result for display."""
    alpha_id = entry.get("alpha_id", "?")
    category = entry.get("category", "?")
    roi = entry.get("roi_potential", "?")
    status = entry.get("status", "?")
    tactic = (entry.get("tactic") or "")[:120]
    method = entry.get("extracted_method") or ""

    print(f"\n  [{score:3d}] {alpha_id} | {category} | ROI:{roi} | {status}")
    print(f"        {tactic}")
    if verbose and method:
        print(f"        METHOD: {method[:150]}")


def main():
    parser = argparse.ArgumentParser(description="Query alpha intelligence by venture/topic")
    parser.add_argument("--venture", type=str, help="Venture type to query for")
    parser.add_argument("--category", type=str, help="Query by exact category")
    parser.add_argument("--search", type=str, help="Keyword search across all fields")
    parser.add_argument("--top", type=int, default=10, help="Number of results (default 10)")
    parser.add_argument("--status", type=str, help="Filter by status (APPROVED, PENDING_REVIEW, etc)")
    parser.add_argument("--stats", action="store_true", help="Show alpha distribution stats")
    parser.add_argument("--untagged", action="store_true", help="Show entries needing method tagging")
    parser.add_argument("--json", action="store_true", help="Output as JSON (for agent consumption)")
    parser.add_argument("--verbose", action="store_true", help="Show extracted methods")
    args = parser.parse_args()

    entries = load_alpha()

    if args.stats:
        show_stats(entries)
        return

    if args.untagged:
        untagged = [e for e in entries
                    if not (e.get("applicable_methods") or "").strip()
                    or (e.get("applicable_methods") or "").strip() == "N/A"]
        print(f"\n{len(untagged)} entries need method tagging")
        for e in untagged[:args.top]:
            alpha_id = e.get("alpha_id", "?")
            cat = e.get("category", "?")
            tactic = (e.get("tactic") or "")[:100]
            print(f"  {alpha_id} | {cat} | {tactic}")
        return

    results = []
    query_desc = ""

    if args.venture:
        results = query_venture(entries, args.venture, args.status, args.top)
        query_desc = f"venture={args.venture}"
    elif args.category:
        results = query_by_category(entries, args.category, args.top)
        query_desc = f"category={args.category}"
    elif args.search:
        results = keyword_search(entries, args.search, args.top)
        query_desc = f"search='{args.search}'"
    else:
        results = top_alpha(entries, args.top)
        query_desc = "top by ROI"

    if args.json:
        output = []
        for score, entry in results:
            output.append({
                "score": score,
                "alpha_id": entry.get("alpha_id"),
                "category": entry.get("category"),
                "tactic": entry.get("tactic"),
                "roi_potential": entry.get("roi_potential"),
                "status": entry.get("status"),
                "extracted_method": entry.get("extracted_method"),
                "applicable_methods": entry.get("applicable_methods"),
            })
        print(json.dumps(output, indent=2))
        return

    print(f"\nALPHA QUERY: {query_desc} (top {args.top})")
    print(f"{'='*60}")
    if not results:
        print("  No matching alpha found.")
    for score, entry in results:
        format_result(score, entry, args.verbose)
    print(f"\n  Total matches shown: {len(results)}")


if __name__ == "__main__":
    main()
