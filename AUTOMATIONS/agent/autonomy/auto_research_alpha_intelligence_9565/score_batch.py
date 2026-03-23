#!/usr/bin/env python3
"""
Alpha Intelligence Research - Automated Batch Scorer
Processes entries with priority='PENDING_REVIEW' from ALPHA_STAGING.csv using heuristic scoring.
Updates priority to IMMEDIATE/NOW/SOON/LATER/BACKLOG based on ROI and authenticity.
"""

import csv
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import tempfile

# Paths
PROJECT_ROOT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
ALPHA_STAGING = PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv"
VENTURE_DATA = PROJECT_ROOT / "AUTOMATIONS" / "agent" / "autonomy" / "auto_research_alpha_intelligence_9565" / "data"
VENTURE_DATA.mkdir(parents=True, exist_ok=True)

def score_roi_potential(entry: dict) -> str:
    """Heuristically score ROI potential based on tactic and category."""
    tactic = (entry.get("tactic") or "").lower()
    category = (entry.get("category") or "").lower()
    roi_field = (entry.get("roi_potential") or "").strip()

    # If already scored, trust it
    if roi_field in ["HIGHEST", "HIGH", "MEDIUM", "LOW"]:
        return roi_field

    # High-ROI categories/tactics
    high_roi_keywords = [
        "monetization", "revenue", "affiliate", "payment", "stripe",
        "subscription", "saas", "recurring", "product launch",
        "app factory"
    ]

    medium_roi_keywords = [
        "growth", "engagement", "content", "tool", "automation",
        "algorithm", "seo", "marketing", "conversion"
    ]

    # Check tactic for revenue signals
    if any(kw in tactic for kw in high_roi_keywords):
        if re.search(r"\$\d+[kK]", tactic):  # Mentions $XK
            return "HIGHEST"
        return "HIGH"

    if any(kw in tactic for kw in medium_roi_keywords):
        return "MEDIUM"

    # Default based on category
    if "app" in category or "product" in category or "monetization" in category:
        return "HIGH"
    elif "tool" in category or "research" in category:
        return "MEDIUM"
    elif "content" in category or "market" in category:
        return "MEDIUM"

    return "LOW"

def score_authenticity(entry: dict) -> str:
    """Score engagement authenticity based on available signals."""
    authenticity = (entry.get("engagement_authenticity") or "").strip()
    if authenticity in ["AUTHENTIC", "SUSPICIOUS", "MEDIUM"]:
        return authenticity

    # Check reviewer notes for red flags
    notes = (entry.get("reviewer_notes") or "").lower()

    if "bot" in notes or "fake" in notes or "purchased" in notes:
        return "SUSPICIOUS"
    if "authentic" in notes or "verified" in notes or "high engagement" in notes:
        return "AUTHENTIC"

    # Default to MEDIUM if uncertain
    return "MEDIUM"

def score_earnings_verified(entry: dict) -> str:
    """Score earnings claim verification."""
    verified = (entry.get("earnings_verified") or "").strip()
    if verified in ["TRUE", "FALSE", "SUSPICIOUS"]:
        return verified

    # Check reviewer notes for verification signals
    notes = (entry.get("reviewer_notes") or "").lower()
    tactic = (entry.get("tactic") or "").lower()

    # Claims with specific dollar amounts should be marked FALSE until verified
    if re.search(r"\$\d+[kK]", tactic) and "verified" not in notes and "confirmed" not in notes:
        return "FALSE"

    # If notes mention verification
    if "verified" in notes or "confirmed" in notes:
        return "TRUE"

    return "FALSE"

def score_priority_from_roi_and_auth(roi: str, authenticity: str) -> str:
    """Convert ROI score and authenticity to priority."""
    if roi == "HIGHEST":
        if authenticity == "SUSPICIOUS":
            return "SOON"
        return "IMMEDIATE"
    elif roi == "HIGH":
        if authenticity == "AUTHENTIC":
            return "NOW"
        else:
            return "SOON"
    elif roi == "MEDIUM":
        return "LATER"
    else:
        return "BACKLOG"

def process_batch(batch_size: int = 100) -> dict:
    """Process next batch of priority='PENDING_REVIEW' entries."""
    processed = 0
    scored = 0
    routed = 0
    priority_dist = defaultdict(int)

    # Read all rows
    rows = []
    fieldnames = None
    with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Process rows
    new_rows = []
    for row in rows:
        priority = (row.get('priority') or "").strip()

        # Only process PENDING_REVIEW
        if priority != "PENDING_REVIEW":
            new_rows.append(row)
            continue

        if processed >= batch_size:
            new_rows.append(row)
            continue

        try:
            # Score this entry
            roi = score_roi_potential(row)
            authenticity = score_authenticity(row)
            earnings = score_earnings_verified(row)
            new_priority = score_priority_from_roi_and_auth(roi, authenticity)

            # Update entry
            row['roi_potential'] = roi
            row['engagement_authenticity'] = authenticity
            row['earnings_verified'] = earnings
            row['priority'] = new_priority

            # Track results
            processed += 1
            scored += 1
            priority_dist[new_priority] += 1

            if roi in ["HIGHEST", "HIGH"]:
                routed += 1

            new_rows.append(row)

        except Exception as e:
            print(f"Error processing {row.get('alpha_id')}: {e}")
            new_rows.append(row)

    # Write back
    with open(ALPHA_STAGING, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_rows)

    return {
        "batch_processed": processed,
        "scored": scored,
        "routed_high_priority": routed,
        "priority_distribution": dict(priority_dist),
        "timestamp": datetime.now().isoformat()
    }

def save_cycle_state(results: dict):
    """Save cycle state for venture tracking."""
    state = {
        "venture": "Alpha Intelligence",
        "type": "RESEARCH",
        "cycle": 1,
        "step": "score",
        "status": "COMPLETED",
        "batch_results": results,
        "timestamp": datetime.now().isoformat()
    }

    state_file = VENTURE_DATA / "cycle_state.json"
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)

    return state_file

if __name__ == "__main__":
    print("Alpha Intelligence - Batch Scorer")
    print("=" * 60)
    print(f"Processing priority='PENDING_REVIEW' entries from ALPHA_STAGING.csv")
    print()

    results = process_batch(batch_size=100)

    print(f"Batch Results:")
    print(f"  Processed: {results['batch_processed']}")
    print(f"  Scored: {results['scored']}")
    print(f"  Routed (HIGH/HIGHEST): {results['routed_high_priority']}")
    print(f"\nNew Priority Distribution:")
    for priority, count in sorted(results['priority_distribution'].items()):
        print(f"  {priority:12s}: {count:3d}")

    # Save state
    state_file = save_cycle_state(results)
    print(f"\nCycle state saved: {state_file}")
    print("✓ Scoring batch complete!")
