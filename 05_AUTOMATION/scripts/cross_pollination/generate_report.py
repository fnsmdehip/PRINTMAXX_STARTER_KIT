#!/usr/bin/env python3
"""
PRINTMAXX Cross-Pollination Report Generator
==============================================
Reads the CROSS_POLLINATION_MATRIX.csv and MONEY_METHODS_TRACKER.csv to generate
a human-readable report of highest-synergy stacks, underexploited combinations,
and actionable recommendations.

Usage:
    python3 generate_report.py                    # Full report
    python3 generate_report.py --min-score 85     # Only 85+ synergy scores
    python3 generate_report.py --method MM001     # Report for specific method
    python3 generate_report.py --active-only      # Only active methods
    python3 generate_report.py --output report.md # Custom output path
"""

import csv
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CROSS_POLLINATION_CSV = PROJECT_ROOT / "LEDGER" / "CROSS_POLLINATION_MATRIX.csv"
METHODS_TRACKER_CSV = PROJECT_ROOT / "LEDGER" / "MONEY_METHODS_TRACKER.csv"
MEGA_SHEET_METHODS = PROJECT_ROOT / "LEDGER" / "MEGA_SHEET" / "TAB1_MONEY_METHODS_MASTER.csv"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def load_methods_tracker() -> dict:
    """Load money methods with their status and details."""
    methods = {}

    # Try MEGA_SHEET first (more complete), fall back to tracker
    csv_path = MEGA_SHEET_METHODS if MEGA_SHEET_METHODS.exists() else METHODS_TRACKER_CSV

    if not csv_path.exists():
        log(f"Methods tracker not found at {csv_path}")
        return methods

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            method_id = row.get("method_id", "")
            if method_id:
                methods[method_id] = {
                    "method_id": method_id,
                    "method_name": row.get("method_name", ""),
                    "category": row.get("category", ""),
                    "status": row.get("status", ""),
                    "priority": row.get("priority", ""),
                    "revenue_model": row.get("revenue_model", ""),
                    "automation_level": row.get("automation_level", ""),
                    "monthly_potential": row.get("monthly_potential", ""),
                }

    log(f"Loaded {len(methods)} methods from {csv_path.name}")
    return methods


def load_cross_pollination() -> list:
    """Load cross-pollination matrix entries."""
    entries = []

    if not CROSS_POLLINATION_CSV.exists():
        log(f"Cross-pollination matrix not found at {CROSS_POLLINATION_CSV}")
        return entries

    with open(CROSS_POLLINATION_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entry = {
                "method_id": row.get("method_id", ""),
                "method_name": row.get("method_name", ""),
                "synergy_partners": row.get("synergy_partners", ""),
                "synergy_type": row.get("synergy_type", ""),
                "synergy_score": 0,
                "cross_sell_products": row.get("cross_sell_products", ""),
                "shared_audience": row.get("shared_audience", ""),
                "automation_combo": row.get("automation_combo", "").upper() == "TRUE",
                "notes": row.get("notes", ""),
            }

            # Parse synergy score
            try:
                entry["synergy_score"] = int(row.get("synergy_score", "0"))
            except ValueError:
                entry["synergy_score"] = 0

            # Parse partners into list
            partners_str = entry["synergy_partners"]
            entry["partner_list"] = [
                p.strip() for p in partners_str.split(",") if p.strip()
            ]

            entries.append(entry)

    log(f"Loaded {len(entries)} cross-pollination entries")
    return entries


def find_underexploited(entries: list, methods: dict) -> list:
    """Find methods that have high synergy scores but inactive partners."""
    underexploited = []

    for entry in entries:
        if entry["synergy_score"] < 80:
            continue

        # Check if primary method is active
        primary = methods.get(entry["method_id"], {})
        primary_status = primary.get("status", "").lower()

        # Check partner statuses
        inactive_partners = []
        active_partners = []
        for partner_id in entry["partner_list"]:
            partner = methods.get(partner_id, {})
            partner_status = partner.get("status", "").lower()
            partner_name = partner.get("method_name", partner_id)

            if partner_status in ("active", "building"):
                active_partners.append(partner_name)
            else:
                inactive_partners.append((partner_id, partner_name, partner_status))

        if inactive_partners:
            underexploited.append({
                "method_id": entry["method_id"],
                "method_name": entry["method_name"],
                "synergy_score": entry["synergy_score"],
                "primary_status": primary_status,
                "active_partners": active_partners,
                "inactive_partners": inactive_partners,
                "synergy_type": entry["synergy_type"],
                "potential": entry["cross_sell_products"],
            })

    # Sort by synergy score descending
    underexploited.sort(key=lambda x: x["synergy_score"], reverse=True)
    return underexploited


def find_automation_stacks(entries: list) -> list:
    """Find methods that can share automation infrastructure."""
    stacks = []
    for entry in entries:
        if entry["automation_combo"]:
            stacks.append({
                "method": entry["method_name"],
                "partners": entry["synergy_partners"],
                "score": entry["synergy_score"],
                "type": entry["synergy_type"],
            })
    stacks.sort(key=lambda x: x["score"], reverse=True)
    return stacks


def find_audience_overlaps(entries: list) -> dict:
    """Group methods by shared audience segments."""
    audiences = {}
    for entry in entries:
        audience = entry.get("shared_audience", "").strip()
        if audience:
            if audience not in audiences:
                audiences[audience] = []
            audiences[audience].append({
                "method": entry["method_name"],
                "score": entry["synergy_score"],
                "partners": entry["synergy_partners"],
            })
    return audiences


def generate_recommendations(entries: list, methods: dict, underexploited: list) -> list:
    """Generate prioritized recommendations."""
    recs = []

    # Rec 1: Activate high-synergy inactive partners
    for ue in underexploited[:5]:
        for partner_id, partner_name, partner_status in ue["inactive_partners"]:
            recs.append({
                "priority": "HIGH",
                "action": f"Activate {partner_name} ({partner_id})",
                "reason": f"Has {ue['synergy_score']} synergy score with {ue['method_name']}. "
                          f"Stack type: {ue['synergy_type']}",
                "expected_impact": ue["potential"],
            })

    # Rec 2: Build automation combos
    auto_stacks = find_automation_stacks(entries)
    for stack in auto_stacks[:3]:
        recs.append({
            "priority": "MEDIUM",
            "action": f"Automate {stack['method']} + {stack['partners']}",
            "reason": f"Automation combo with {stack['score']} synergy. "
                      f"Shared infrastructure reduces build time.",
            "expected_impact": stack["type"],
        })

    # Rec 3: Cross-sell opportunities
    high_score = [e for e in entries if e["synergy_score"] >= 90]
    for entry in high_score[:3]:
        if entry["cross_sell_products"]:
            recs.append({
                "priority": "HIGH",
                "action": f"Implement cross-sell: {entry['method_name']}",
                "reason": f"Score {entry['synergy_score']}. Cross-sell path: {entry['cross_sell_products']}",
                "expected_impact": f"Shared audience: {entry['shared_audience']}",
            })

    return recs


def generate_report(
    entries: list,
    methods: dict,
    min_score: int = 0,
    method_filter: str = "",
    active_only: bool = False,
) -> str:
    """Generate the full cross-pollination report."""

    # Apply filters
    filtered = entries
    if min_score > 0:
        filtered = [e for e in filtered if e["synergy_score"] >= min_score]
    if method_filter:
        filtered = [e for e in filtered if e["method_id"] == method_filter]
    if active_only:
        active_ids = {mid for mid, m in methods.items() if m.get("status", "").lower() in ("active", "building")}
        filtered = [e for e in filtered if e["method_id"] in active_ids]

    # Sort by synergy score
    filtered.sort(key=lambda x: x["synergy_score"], reverse=True)

    lines = [
        "# Cross-Pollination Report",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Methods tracked:** {len(methods)}",
        f"**Synergy pairs:** {len(entries)}",
        f"**Filters:** min_score={min_score}, method={method_filter or 'all'}, "
        f"active_only={active_only}",
        "",
    ]

    # Section 1: Top Synergy Stacks
    lines.append("## Top Synergy Stacks (Score 85+)")
    lines.append("")
    top_stacks = [e for e in filtered if e["synergy_score"] >= 85]
    if top_stacks:
        lines.append("| Method | Partners | Score | Stack Type | Automation |")
        lines.append("|--------|----------|-------|------------|------------|")
        for entry in top_stacks:
            auto = "Yes" if entry["automation_combo"] else "No"
            lines.append(
                f"| {entry['method_name']} | {entry['synergy_partners']} | "
                f"{entry['synergy_score']} | {entry['synergy_type'][:50]} | {auto} |"
            )
        lines.append("")
    else:
        lines.append("No stacks with score 85+.")
        lines.append("")

    # Section 2: Underexploited Combinations
    underexploited = find_underexploited(entries, methods)
    lines.append("## Underexploited Combinations")
    lines.append("High-synergy stacks where one or more partners are not yet active.")
    lines.append("")
    if underexploited:
        for ue in underexploited[:10]:
            lines.append(f"### {ue['method_name']} (Score: {ue['synergy_score']})")
            lines.append(f"- **Primary status:** {ue['primary_status']}")
            if ue['active_partners']:
                lines.append(f"- **Active partners:** {', '.join(ue['active_partners'])}")
            lines.append(f"- **Inactive partners needing activation:**")
            for pid, pname, pstatus in ue['inactive_partners']:
                lines.append(f"  - {pname} ({pid}) - Status: {pstatus}")
            lines.append(f"- **Stack type:** {ue['synergy_type']}")
            lines.append(f"- **Cross-sell potential:** {ue['potential']}")
            lines.append("")
    else:
        lines.append("All high-synergy partners are active.")
        lines.append("")

    # Section 3: Automation Stacks
    auto_stacks = find_automation_stacks(entries)
    lines.append("## Automation Stacks")
    lines.append("Methods that can share automation infrastructure (Playwright scripts, posting schedules, etc).")
    lines.append("")
    if auto_stacks:
        for stack in auto_stacks:
            lines.append(f"- **{stack['method']}** + {stack['partners']} (Score: {stack['score']})")
        lines.append("")
    else:
        lines.append("No automation combos identified.")
        lines.append("")

    # Section 4: Audience Overlap Map
    audiences = find_audience_overlaps(entries)
    lines.append("## Audience Overlap Map")
    lines.append("")
    if audiences:
        for audience, methods_list in sorted(audiences.items(), key=lambda x: len(x[1]), reverse=True):
            lines.append(f"### {audience}")
            for m in methods_list:
                lines.append(f"- {m['method']} (Score: {m['score']})")
            lines.append("")
    else:
        lines.append("No audience overlaps mapped.")
        lines.append("")

    # Section 5: Recommendations
    recs = generate_recommendations(entries, methods, underexploited)
    lines.append("## Recommendations")
    lines.append("")
    if recs:
        for i, rec in enumerate(recs, 1):
            lines.append(f"### {i}. [{rec['priority']}] {rec['action']}")
            lines.append(f"- **Why:** {rec['reason']}")
            lines.append(f"- **Impact:** {rec['expected_impact']}")
            lines.append("")
    else:
        lines.append("No recommendations generated.")
        lines.append("")

    # Section 6: Full Matrix Summary
    lines.append("## Full Matrix Summary")
    lines.append("")
    lines.append(f"| Score Range | Count |")
    lines.append(f"|-------------|-------|")
    score_ranges = {"90+": 0, "80-89": 0, "70-79": 0, "60-69": 0, "<60": 0}
    for entry in entries:
        s = entry["synergy_score"]
        if s >= 90:
            score_ranges["90+"] += 1
        elif s >= 80:
            score_ranges["80-89"] += 1
        elif s >= 70:
            score_ranges["70-79"] += 1
        elif s >= 60:
            score_ranges["60-69"] += 1
        else:
            score_ranges["<60"] += 1
    for range_name, count in score_ranges.items():
        lines.append(f"| {range_name} | {count} |")
    lines.append("")

    # Method status summary
    active_count = sum(1 for m in methods.values() if m.get("status", "").lower() in ("active", "building"))
    planning_count = sum(1 for m in methods.values() if m.get("status", "").lower() == "planning")
    other_count = len(methods) - active_count - planning_count

    lines.append("## Method Status Overview")
    lines.append(f"- Active/Building: {active_count}")
    lines.append(f"- Planning: {planning_count}")
    lines.append(f"- Other: {other_count}")
    lines.append(f"- Total: {len(methods)}")

    return "\n".join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="PRINTMAXX Cross-Pollination Report Generator")
    parser.add_argument("--min-score", type=int, default=0, help="Minimum synergy score to include")
    parser.add_argument("--method", default="", help="Filter to specific method ID (e.g., MM001)")
    parser.add_argument("--active-only", action="store_true", help="Only include active methods")
    parser.add_argument("--output", default=None, help="Output file path")
    args = parser.parse_args()

    log("PRINTMAXX Cross-Pollination Report Generator starting")

    # Load data
    methods = load_methods_tracker()
    entries = load_cross_pollination()

    if not entries:
        log("No cross-pollination data found. Check LEDGER/CROSS_POLLINATION_MATRIX.csv.")
        sys.exit(1)

    # Generate report
    report = generate_report(
        entries,
        methods,
        min_score=args.min_score,
        method_filter=args.method,
        active_only=args.active_only,
    )

    print(report)

    # Save to file
    output_path = Path(args.output) if args.output else None
    if not output_path:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = OUTPUT_DIR / f"cross_pollination_report_{datetime.now().strftime('%Y%m%d')}.md"

    output_path.write_text(report, encoding="utf-8")
    log(f"Report saved to {output_path}")

    # Quick stats
    high_synergy = sum(1 for e in entries if e["synergy_score"] >= 85)
    auto_combos = sum(1 for e in entries if e["automation_combo"])

    log(f"\n--- SUMMARY ---")
    log(f"Total synergy pairs: {len(entries)}")
    log(f"High synergy (85+): {high_synergy}")
    log(f"Automation combos: {auto_combos}")
    log(f"Methods tracked: {len(methods)}")
    log("Done.")


if __name__ == "__main__":
    main()
