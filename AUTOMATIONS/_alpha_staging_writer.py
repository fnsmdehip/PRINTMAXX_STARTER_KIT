#!/usr/bin/env python3
"""
Shared helper: append high-value findings to ALPHA_STAGING.csv.

Used by broker/arb/opportunity scripts to feed Capital Genesis Ranker.
Without this, 7 of 9 scanners wrote to their own CSVs but never
fed the central scoring pipeline.

Usage from any script:
    from _alpha_staging_writer import stage_finding, stage_findings_batch
    stage_finding(
        content="Posture corrector: $6 source, $24 sell, 58% margin on eBay",
        source="ecom_arb_engine",
        category="MONETIZATION",
        roi_potential="HIGH",
        applicable_methods="ECOM_ARB",
    )
"""

from __future__ import annotations

import csv
import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ALPHA_STAGING_CSV = PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv"

ALPHA_STAGING_HEADERS = [
    "alpha_id", "source", "source_url", "category", "tactic",
    "roi_potential", "priority", "status", "applicable_methods",
    "applicable_niches", "synergy_score", "cross_sell_products",
    "implementation_priority", "engagement_authenticity",
    "earnings_verified", "extracted_method", "compliance_notes",
    "reviewer_notes", "created_at", "ops_generated", "quality_issues",
    "date_added",
]

# Priority mapping from ROI potential
_ROI_TO_PRIORITY = {
    "HIGHEST": "IMMEDIATE",
    "HIGH": "HIGH",
    "MEDIUM": "MEDIUM",
    "LOW": "LOW",
}


def _generate_alpha_id(content: str, source: str) -> str:
    """Generate a deterministic alpha_id from content + source."""
    digest = hashlib.md5(f"{source}:{content}".encode()).hexdigest()[:8].upper()
    prefix = source.upper().replace(" ", "_")[:12]
    return f"ALPHA_{prefix}_{digest}"


def _load_existing_content() -> set[str]:
    """Load existing tactic/content values for dedup."""
    existing = set()
    if ALPHA_STAGING_CSV.exists():
        try:
            with open(ALPHA_STAGING_CSV, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    tactic = row.get("tactic", "")
                    if tactic:
                        existing.add(tactic.strip()[:200].lower())
        except Exception:
            pass
    return existing


def stage_finding(
    content: str,
    source: str,
    category: str,
    roi_potential: str = "MEDIUM",
    applicable_methods: str = "",
    source_url: str = "",
    applicable_niches: str = "",
    reviewer_notes: str = "",
) -> bool:
    """
    Append a single finding to ALPHA_STAGING.csv if not duplicate.

    Returns True if staged, False if duplicate or error.
    """
    return stage_findings_batch([{
        "content": content,
        "source": source,
        "category": category,
        "roi_potential": roi_potential,
        "applicable_methods": applicable_methods,
        "source_url": source_url,
        "applicable_niches": applicable_niches,
        "reviewer_notes": reviewer_notes,
    }]) > 0


def stage_findings_batch(findings: list[dict]) -> int:
    """
    Append multiple findings to ALPHA_STAGING.csv, deduplicating.

    Each finding dict keys:
        content (str): The finding text (maps to 'tactic' column)
        source (str): Source script/system name
        category (str): MONETIZATION, BROKERING, APP_FACTORY, etc.
        roi_potential (str): HIGHEST/HIGH/MEDIUM/LOW
        applicable_methods (str): e.g. ECOM_ARB, GOV_CONTRACTS
        source_url (str): optional URL
        applicable_niches (str): optional
        reviewer_notes (str): optional

    Returns count of newly staged entries.
    """
    if not findings:
        return 0

    ALPHA_STAGING_CSV.parent.mkdir(parents=True, exist_ok=True)
    existing = _load_existing_content()

    file_exists = ALPHA_STAGING_CSV.exists() and ALPHA_STAGING_CSV.stat().st_size > 0
    now_iso = datetime.now(timezone.utc).isoformat()
    today = datetime.now().strftime("%Y-%m-%d")
    staged = 0

    with open(ALPHA_STAGING_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ALPHA_STAGING_HEADERS, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()

        for finding in findings:
            content = finding.get("content", "").strip()
            if not content:
                continue

            # Dedup check on first 200 chars lowered
            dedup_key = content[:200].lower()
            if dedup_key in existing:
                continue
            existing.add(dedup_key)

            source = finding.get("source", "unknown")
            roi = finding.get("roi_potential", "MEDIUM").upper()
            category = finding.get("category", "MONETIZATION").upper()

            row = {
                "alpha_id": _generate_alpha_id(content, source),
                "source": source,
                "source_url": finding.get("source_url", ""),
                "category": category,
                "tactic": content[:500],
                "roi_potential": roi,
                "priority": _ROI_TO_PRIORITY.get(roi, "MEDIUM"),
                "status": "PENDING_REVIEW",
                "applicable_methods": finding.get("applicable_methods", ""),
                "applicable_niches": finding.get("applicable_niches", ""),
                "synergy_score": "",
                "cross_sell_products": "",
                "implementation_priority": "",
                "engagement_authenticity": "SYSTEMATIC_SCAN",
                "earnings_verified": "N/A",
                "extracted_method": content[:300],
                "compliance_notes": "",
                "reviewer_notes": finding.get("reviewer_notes", f"Auto-staged from {source}"),
                "created_at": now_iso,
                "ops_generated": "",
                "quality_issues": "",
                "date_added": today,
            }
            writer.writerow(row)
            staged += 1

    return staged
