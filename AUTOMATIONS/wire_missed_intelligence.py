#!/usr/bin/env python3
"""
wire_missed_intelligence.py

Reads OPS/MISSED_INTELLIGENCE_SCAN.md, parses all file entries,
classifies them by venture type, and adds them to OPS/INTELLIGENCE_CATALOG.json.
Deduplicates by path and updates doc counts.
"""

import json
import re
import sys
from pathlib import Path

from agent_resilience import locked_file

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SCAN_PATH = PROJECT_ROOT / "OPS" / "MISSED_INTELLIGENCE_SCAN.md"
CATALOG_PATH = PROJECT_ROOT / "OPS" / "INTELLIGENCE_CATALOG.json"

# Directory-based venture classification rules
# Order matters: more specific paths first
CLASSIFICATION_RULES = [
    # MONEY_METHODS sub-directories
    ("MONEY_METHODS/APP_FACTORY/", "APP_FACTORY"),
    ("MONEY_METHODS/MICRO_SAAS/", "APP_FACTORY"),
    ("MONEY_METHODS/COLD_OUTBOUND/", "OUTBOUND"),
    ("MONEY_METHODS/CONTENT_FARM/", "CONTENT"),
    ("MONEY_METHODS/AI_INFLUENCER/", "CONTENT"),
    ("MONEY_METHODS/AI_CONTENT_AFFILIATE/", "CONTENT"),
    ("MONEY_METHODS/LOCAL_BIZ/", "LOCAL_BIZ"),
    ("MONEY_METHODS/NEWSLETTER/", "MONETIZATION"),
    ("MONEY_METHODS/SKOOL_COMMUNITY/", "MONETIZATION"),
    ("MONEY_METHODS/PLATFORM_ARBITRAGE/", "MONETIZATION"),
    ("MONEY_METHODS/SYNERGY_PACKAGES/", "MONETIZATION"),
    ("MONEY_METHODS/AI_AGENT_SERVICES/", "MONETIZATION"),
    ("MONEY_METHODS/AI_AGENTS_SERVICE/", "MONETIZATION"),

    # EMAIL
    ("EMAIL/", "OUTBOUND"),

    # PRODUCTS and DIGITAL_PRODUCTS
    ("PRODUCTS/", "PRODUCT"),
    ("DIGITAL_PRODUCTS/", "PRODUCT"),

    # RESEARCH
    ("RESEARCH/", "RESEARCH"),
    ("10_RESEARCH/", "RESEARCH"),

    # 06_OPERATIONS sub-directories
    ("06_OPERATIONS/growth/", "GROWTH"),
    ("06_OPERATIONS/gtm/", "MONETIZATION"),
    ("06_OPERATIONS/trend_intel/", "RESEARCH"),
    ("06_OPERATIONS/research/", "RESEARCH"),
    ("06_OPERATIONS/setup/", "APP_FACTORY"),

    # FINANCIALS
    ("FINANCIALS/", "MONETIZATION"),

    # 01_STRATEGY — cross-venture, put in MONETIZATION
    ("01_STRATEGY/", "MONETIZATION"),

    # ralph and .ralph — SCRAPING
    ("ralph/", "SCRAPING"),
    (".ralph/", "SCRAPING"),

    # 05_AUTOMATION/browser — SCRAPING
    ("05_AUTOMATION/browser/", "SCRAPING"),

    # MASTER_DOC — cross-venture, put in MONETIZATION
    ("MASTER_DOC/", "MONETIZATION"),

    # CONTENT directory
    ("CONTENT/", "CONTENT"),
]

# Root-level file classification by keyword patterns
ROOT_KEYWORDS = {
    "NICHE_CONTENT": "CONTENT",
    "CONTENT": "CONTENT",
    "CAPITAL_GENESIS": "MONETIZATION",
    "RBI": "RESEARCH",
    "RESEARCH": "RESEARCH",
    "METHOD": "MONETIZATION",
    "ecom_arb": "MONETIZATION",
    "APP_FACTORY": "APP_FACTORY",
    "ALPHA": "RESEARCH",
}


def classify_path(path: str) -> str:
    """Classify a file path into a venture type."""
    for prefix, venture in CLASSIFICATION_RULES:
        if path.startswith(prefix):
            return venture

    # Root-level files: classify by filename keywords
    if "/" not in path:
        for keyword, venture in ROOT_KEYWORDS.items():
            if keyword.lower() in path.lower():
                return venture
        # Default for unclassified root files
        return "MONETIZATION"

    # Fallback
    return "MONETIZATION"


def parse_scan_file(scan_path: Path) -> list:
    """Parse MISSED_INTELLIGENCE_SCAN.md and extract all file entries."""
    content = scan_path.read_text(encoding="utf-8")
    entries = []

    # Match lines like: - `path` -- [VALUE] -- description
    pattern = re.compile(
        r'^- `([^`]+)`\s*--\s*\[(\w+)\]\s*--\s*(.+)$',
        re.MULTILINE
    )

    for match in pattern.finditer(content):
        raw_path = match.group(1).strip()
        value = match.group(2).strip().upper()
        description = match.group(3).strip()

        # Skip directory-only entries (ending with /)
        if raw_path.endswith("/"):
            continue

        entries.append({
            "path": raw_path,
            "value": value,
            "summary": description,
        })

    return entries


def get_existing_paths(catalog: dict) -> set:
    """Get all paths already in the catalog across all ventures."""
    paths = set()

    # Check ventures dict
    ventures = catalog.get("ventures", {})
    for venture_name, venture_data in ventures.items():
        if isinstance(venture_data, dict):
            docs = venture_data.get("docs", [])
            for doc in docs:
                if isinstance(doc, dict):
                    paths.add(doc.get("path", ""))

    # Check cross_venture
    cross = catalog.get("cross_venture", {})
    if isinstance(cross, dict):
        for doc in cross.get("docs", []):
            if isinstance(doc, dict):
                paths.add(doc.get("path", ""))

    # Check unmapped
    unmapped = catalog.get("unmapped", [])
    for item in unmapped:
        if isinstance(item, dict):
            paths.add(item.get("path", ""))

    return paths


def main():
    # Read scan file
    if not SCAN_PATH.exists():
        print(f"ERROR: Scan file not found: {SCAN_PATH}")
        sys.exit(1)

    if not CATALOG_PATH.exists():
        print(f"ERROR: Catalog file not found: {CATALOG_PATH}")
        sys.exit(1)

    print(f"Reading scan file: {SCAN_PATH}")
    entries = parse_scan_file(SCAN_PATH)
    print(f"Parsed {len(entries)} file entries from scan")

    # Read catalog (under lock to prevent concurrent corruption)
    print(f"Reading catalog: {CATALOG_PATH}")
    with locked_file(CATALOG_PATH, mode="r") as f:
        catalog = json.load(f)

    existing_paths = get_existing_paths(catalog)
    print(f"Found {len(existing_paths)} existing paths in catalog")

    # Ensure all venture keys exist in catalog
    ventures = catalog.setdefault("ventures", {})
    for venture_type in ["CONTENT", "OUTBOUND", "APP_FACTORY", "LOCAL_BIZ",
                          "MONETIZATION", "PRODUCT", "RESEARCH", "GROWTH", "SCRAPING"]:
        if venture_type not in ventures:
            ventures[venture_type] = {"doc_count": 0, "docs": []}
        if "docs" not in ventures[venture_type]:
            ventures[venture_type]["docs"] = []

    # Classify and add entries
    added = 0
    skipped_dup = 0
    by_venture = {}

    for entry in entries:
        path = entry["path"]

        # Deduplicate
        if path in existing_paths:
            skipped_dup += 1
            continue

        venture = classify_path(path)
        doc = {
            "path": path,
            "summary": entry["summary"],
            "value": entry["value"],
            "source": "missed_scan_2026-03-07"
        }

        ventures[venture]["docs"].append(doc)
        existing_paths.add(path)  # Prevent intra-batch duplicates
        added += 1
        by_venture[venture] = by_venture.get(venture, 0) + 1

    print(f"\nAdded {added} new docs, skipped {skipped_dup} duplicates")
    print(f"\nNew docs per venture:")
    for v, count in sorted(by_venture.items()):
        print(f"  {v}: +{count}")

    # Update doc_count for each venture
    total = 0
    print(f"\nUpdated doc counts:")
    for venture_type, venture_data in ventures.items():
        old_count = venture_data.get("doc_count", 0)
        new_count = len(venture_data.get("docs", []))
        venture_data["doc_count"] = new_count
        total += new_count
        print(f"  {venture_type}: {old_count} -> {new_count}")

    # Also count cross_venture docs
    cross = catalog.get("cross_venture", {})
    if isinstance(cross, dict):
        cross_count = len(cross.get("docs", []))
        cross["doc_count"] = cross_count
        total += cross_count
        print(f"  cross_venture: {cross_count}")

    catalog["total_docs"] = total
    print(f"\nTotal docs in catalog: {total}")

    # Save (under lock to prevent concurrent corruption)
    with locked_file(CATALOG_PATH, mode="w") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(f"\nSaved updated catalog to {CATALOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
