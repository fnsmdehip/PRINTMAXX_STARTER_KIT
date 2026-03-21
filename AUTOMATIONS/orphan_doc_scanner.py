#!/usr/bin/env python3
"""
ORPHAN DOC SCANNER — Weekly scan for docs not consumed by any agent.

Finds documents in OPS/ and MONEY_METHODS/ that aren't referenced by:
  - Any automation script
  - System map
  - Intelligence catalog
  - KPI dashboard
  - Any agent config

6-step process per doc: read → relevant? → already covered? → wire in → archive → delete.

Outputs:
  - OPS/ORPHAN_DOC_REPORT.md — categorized report (actionable / outdated / duplicate)
  - Surfaces actionable ones in daily feed dashboard
  - Auto-archives docs older than 30 days with no references

Cron: 0 4 * * 0 (Sunday 4 AM weekly)

Usage:
  python3 AUTOMATIONS/orphan_doc_scanner.py --scan
  python3 AUTOMATIONS/orphan_doc_scanner.py --scan --auto-archive
  python3 AUTOMATIONS/orphan_doc_scanner.py --status
  python3 AUTOMATIONS/orphan_doc_scanner.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import PROJECT, safe_path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AUTOMATIONS = PROJECT / "AUTOMATIONS"
OPS = PROJECT / "OPS"
LEDGER = PROJECT / "LEDGER"
MONEY_METHODS = PROJECT / "MONEY_METHODS"
LOG_FILE = AUTOMATIONS / "logs" / "orphan_doc_scanner.log"
REPORT_FILE = OPS / "ORPHAN_DOC_REPORT.md"
ARCHIVE_DIR = OPS / "archive" / "orphans"
SYSTEM_MAP = OPS / "PRINTMAXX_SYSTEM_MAP.md"
INTEL_CATALOG = OPS / "INTELLIGENCE_CATALOG.json"
KPI_DASHBOARD = OPS / "KPI_DASHBOARD.md"
NAV_INDEX = OPS / "NAV_INDEX.md"

# Directories to scan for orphans
SCAN_DIRS = [OPS, MONEY_METHODS]

# Extensions that count as "docs"
DOC_EXTENSIONS = {".md", ".txt", ".csv", ".json", ".html"}

# Files that are NEVER orphans (infrastructure)
NEVER_ORPHAN = {
    "PRINTMAXX_SYSTEM_MAP.md", "INTELLIGENCE_CATALOG.json", "KPI_DASHBOARD.md",
    "NAV_INDEX.md", "PERSISTENT_TASK_TRACKER.md", "SESSION_BRIEFING.md",
    "DAILY_TACTICAL_PLAN.md", "DAILY_DIGEST.md", "ACTIONABLE_QUEUE.md",
    "HEARTBEAT.md", "SESSION_LOG.md", "CURRENT_STATUS.md", "CODEBASE_GRAMMAR.md",
    "SESSION_HANDOFF_20260320.md", "ORPHAN_DOC_REPORT.md",
    "CAPITAL_GENESIS_PRIORITY_STACK.md", "AUTONOMOUS_TASK_QUEUE.jsonl",
    "META_PLAN.json", "PROMPT_META_REVIEW.md",
    "APP_FACTORY_ALPHA_COMMAND_CENTER.md", "SYSTEM_VISUAL.html",
    "GREY_HAT_EDGE_GROWTH_MASTER.md", "DEFINITIVE_GROWTH_STACK.md",
    "USER_VOICE_MODEL.json", "INTEGRATION_GAP_REPORT.md",
    "MULTI_ACCOUNT_INFRASTRUCTURE.md", "GROWTH_ALPHA_SOURCES.md",
}

# Directories to search for references
REFERENCE_SOURCES = [
    AUTOMATIONS,  # Python scripts
    PROJECT / ".claude",  # Claude rules
    OPS / "PRINTMAXX_SYSTEM_MAP.md",  # System map
]

MAX_AGE_DAYS = 90  # Auto-archive docs older than this with zero references


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [ORPHAN-SCAN] [{level}] {msg}"
    print(line)
    safe_path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_FILE), "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# Reference detection
# ---------------------------------------------------------------------------

def build_reference_index() -> set[str]:
    """Scan all automation scripts and rules for file references. Returns set of referenced filenames."""
    referenced: set[str] = set()

    # Scan Python scripts in AUTOMATIONS
    for py_file in AUTOMATIONS.rglob("*.py"):
        try:
            content = py_file.read_text(errors="replace")
            # Look for file references — quoted strings containing .md, .csv, .json
            import re
            for match in re.findall(r'["\']([^"\']+\.(?:md|csv|json|txt|html))["\']', content):
                referenced.add(Path(match).name)
                # Also add the full relative path
                referenced.add(match)
        except Exception:
            continue

    # Scan Claude rules
    rules_dir = PROJECT / ".claude" / "rules"
    if rules_dir.exists():
        for rule_file in rules_dir.rglob("*.md"):
            try:
                content = rule_file.read_text(errors="replace")
                import re
                for match in re.findall(r'`([^`]+\.(?:md|csv|json|txt|html))`', content):
                    referenced.add(Path(match).name)
                    referenced.add(match)
            except Exception:
                continue

    # Scan system map
    if SYSTEM_MAP.exists():
        try:
            content = SYSTEM_MAP.read_text(errors="replace")
            import re
            for match in re.findall(r'`?([A-Z_]+\.(?:md|csv|json|txt|html))`?', content):
                referenced.add(match)
        except Exception:
            pass

    # Scan intelligence catalog
    if INTEL_CATALOG.exists():
        try:
            catalog = json.loads(INTEL_CATALOG.read_text())
            if isinstance(catalog, dict):
                for key in ("documents", "entries", "files"):
                    docs = catalog.get(key, [])
                    if isinstance(docs, list):
                        for doc in docs:
                            if isinstance(doc, dict):
                                fp = doc.get("file_path") or doc.get("path") or ""
                                if fp:
                                    referenced.add(Path(fp).name)
                            elif isinstance(doc, str):
                                referenced.add(Path(doc).name)
        except Exception:
            pass

    # Scan KPI dashboard
    if KPI_DASHBOARD.exists():
        try:
            content = KPI_DASHBOARD.read_text(errors="replace")
            import re
            for match in re.findall(r'[A-Z_]+\.(?:md|csv|json|py)', content):
                referenced.add(match)
        except Exception:
            pass

    # Scan nav index
    if NAV_INDEX.exists():
        try:
            content = NAV_INDEX.read_text(errors="replace")
            import re
            for match in re.findall(r'`([^`]+)`', content):
                referenced.add(Path(match).name)
        except Exception:
            pass

    return referenced


def find_orphan_docs() -> list[dict]:
    """Find all docs not referenced by any automation or system file."""
    referenced = build_reference_index()
    log(f"Reference index built: {len(referenced)} referenced filenames")

    orphans = []
    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue
        for doc_path in scan_dir.rglob("*"):
            if not doc_path.is_file():
                continue
            if doc_path.suffix.lower() not in DOC_EXTENSIONS:
                continue
            if doc_path.name in NEVER_ORPHAN:
                continue
            # Skip archive dirs
            if "archive" in str(doc_path).lower():
                continue

            # Check if referenced
            is_referenced = (
                doc_path.name in referenced
                or str(doc_path.relative_to(PROJECT)) in referenced
                or any(doc_path.name in ref for ref in referenced)
            )

            if not is_referenced:
                # Get file age
                try:
                    mtime = doc_path.stat().st_mtime
                    age_days = (time.time() - mtime) / 86400
                except Exception:
                    age_days = 999

                # Get file size
                try:
                    size_kb = doc_path.stat().st_size / 1024
                except Exception:
                    size_kb = 0

                orphans.append({
                    "path": str(doc_path.relative_to(PROJECT)),
                    "name": doc_path.name,
                    "age_days": round(age_days, 1),
                    "size_kb": round(size_kb, 1),
                    "directory": str(doc_path.parent.relative_to(PROJECT)),
                    "extension": doc_path.suffix,
                })

    # Sort by size descending (biggest orphans first = most wasted context)
    orphans.sort(key=lambda x: x["size_kb"], reverse=True)
    return orphans


def categorize_orphans(orphans: list[dict]) -> dict[str, list[dict]]:
    """Categorize orphans into actionable / outdated / duplicate groups."""
    categories: dict[str, list[dict]] = {
        "actionable": [],     # Contains useful info, should be wired in
        "outdated": [],       # Old, likely superseded
        "small_noise": [],    # Tiny files, likely notes or stubs
        "large_unwired": [],  # Big docs with no consumer — highest priority
    }

    for orphan in orphans:
        age = orphan["age_days"]
        size = orphan["size_kb"]

        if age > MAX_AGE_DAYS:
            categories["outdated"].append(orphan)
        elif size > 50:
            categories["large_unwired"].append(orphan)
        elif size < 2:
            categories["small_noise"].append(orphan)
        else:
            categories["actionable"].append(orphan)

    return categories


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(orphans: list[dict], categories: dict[str, list[dict]]) -> str:
    """Generate the orphan doc report."""
    report = f"# Orphan Doc Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    report += f"**Total orphans:** {len(orphans)}\n"
    report += f"**Total size:** {sum(o['size_kb'] for o in orphans):.0f} KB\n\n"

    for cat_name, cat_docs in categories.items():
        if not cat_docs:
            continue
        report += f"## {cat_name.upper().replace('_', ' ')} ({len(cat_docs)} docs)\n\n"
        for doc in cat_docs[:50]:  # Limit per category
            report += f"- `{doc['path']}` ({doc['size_kb']:.0f} KB, {doc['age_days']:.0f} days old)\n"
        if len(cat_docs) > 50:
            report += f"- ... and {len(cat_docs) - 50} more\n"
        report += "\n"

    report += "## Action Items\n\n"
    report += "1. **LARGE UNWIRED** — Wire into agents or intelligence catalog\n"
    report += "2. **ACTIONABLE** — Review and wire or archive\n"
    report += "3. **OUTDATED** — Auto-archive (--auto-archive flag)\n"
    report += "4. **SMALL NOISE** — Delete or consolidate\n"

    return report


# ---------------------------------------------------------------------------
# Auto-archive
# ---------------------------------------------------------------------------

def auto_archive_old(orphans: list[dict], dry_run: bool = False) -> int:
    """Move orphans older than MAX_AGE_DAYS to archive directory."""
    archived = 0
    for orphan in orphans:
        if orphan["age_days"] < MAX_AGE_DAYS:
            continue

        src = PROJECT / orphan["path"]
        if not src.exists():
            continue

        if dry_run:
            log(f"[DRY-RUN] Would archive: {orphan['path']}")
            archived += 1
            continue

        safe_path(ARCHIVE_DIR).mkdir(parents=True, exist_ok=True)
        dst = safe_path(ARCHIVE_DIR / orphan["name"])

        # Avoid overwrite
        if dst.exists():
            stem = dst.stem
            dst = safe_path(ARCHIVE_DIR / f"{stem}_{int(time.time())}{dst.suffix}")

        try:
            import shutil
            shutil.move(str(src), str(dst))
            archived += 1
            log(f"Archived: {orphan['path']} → {dst.name}")
        except Exception as e:
            log(f"Archive failed for {orphan['path']}: {e}", "ERROR")

    return archived


# ---------------------------------------------------------------------------
# Alpha staging integration — feed orphans into the pipeline
# ---------------------------------------------------------------------------

ALPHA_STAGING = LEDGER / "ALPHA_STAGING.csv"
ALPHA_FIELDS = [
    "alpha_id", "source", "source_url", "category", "tactic",
    "roi_potential", "priority", "status", "applicable_methods",
    "applicable_niches", "synergy_score", "cross_sell_products",
    "implementation_priority", "engagement_authenticity",
    "earnings_verified", "extracted_method", "compliance_notes",
    "reviewer_notes", "created_at", "ops_generated",
]


def _get_existing_alpha_ids() -> set[str]:
    ids: set[str] = set()
    if not ALPHA_STAGING.exists():
        return ids
    try:
        import csv
        with open(ALPHA_STAGING) as f:
            for row in csv.DictReader(f):
                aid = row.get("alpha_id", "")
                if aid:
                    ids.add(aid)
    except Exception:
        pass
    return ids


def _read_doc_summary(doc_path: Path, max_chars: int = 500) -> str:
    """Read first N chars of a doc for the alpha entry."""
    try:
        text = doc_path.read_text(errors="replace")[:max_chars]
        return text.replace("\n", " ").strip()
    except Exception:
        return ""


def stage_orphans_as_alpha(orphans: list[dict], dry_run: bool = False) -> int:
    """Stage large/actionable orphan docs as alpha entries for the integration pipeline."""
    import csv
    import hashlib

    if not orphans:
        return 0

    existing_ids = _get_existing_alpha_ids()
    new_entries = []

    for orphan in orphans[:85]:  # Cap at 85 per run
        doc_path = PROJECT / orphan["path"]
        if not doc_path.exists():
            continue

        alpha_id = f"ORPHAN{hashlib.md5(orphan['path'].encode()).hexdigest()[:8].upper()}"
        if alpha_id in existing_ids:
            continue

        summary = _read_doc_summary(doc_path)
        if not summary or len(summary) < 20:
            continue

        # Determine category from path
        path_lower = orphan["path"].lower()
        if "money_method" in path_lower:
            category = "REVENUE_METHOD"
            roi = "MEDIUM"
        elif "growth" in path_lower or "marketing" in path_lower:
            category = "GROWTH_TACTIC"
            roi = "MEDIUM"
        elif "tool" in path_lower or "catalog" in path_lower:
            category = "TOOL_DISCOVERY"
            roi = "LOW"
        elif "alpha" in path_lower or "research" in path_lower:
            category = "RESEARCH"
            roi = "MEDIUM"
        else:
            category = "ORPHAN_DOC"
            roi = "LOW"

        entry = {
            "alpha_id": alpha_id,
            "source": "orphan_doc_scanner",
            "source_url": orphan["path"],
            "category": category,
            "tactic": f"Orphan doc: {orphan['name']} ({orphan['size_kb']:.0f}KB)",
            "roi_potential": roi,
            "priority": "P1" if orphan["size_kb"] > 50 else "P2",
            "status": "PENDING_REVIEW",
            "applicable_methods": "",
            "applicable_niches": "",
            "synergy_score": str(min(int(orphan["size_kb"]), 100)),
            "cross_sell_products": "",
            "implementation_priority": "P1" if orphan["size_kb"] > 50 else "P2",
            "engagement_authenticity": "N/A",
            "earnings_verified": "N/A",
            "extracted_method": summary[:300],
            "compliance_notes": "Internal doc — no compliance issues",
            "reviewer_notes": f"Orphan doc {orphan['size_kb']:.0f}KB, {orphan['age_days']:.0f} days old",
            "created_at": datetime.now().isoformat(),
            "ops_generated": "no",
        }
        new_entries.append(entry)

    if not new_entries:
        return 0

    if dry_run:
        log(f"[DRY-RUN] Would stage {len(new_entries)} orphan docs as alpha")
        return len(new_entries)

    file_exists = ALPHA_STAGING.exists()
    with open(safe_path(ALPHA_STAGING), "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ALPHA_FIELDS)
        if not file_exists:
            writer.writeheader()
        for entry in new_entries:
            writer.writerow(entry)

    return len(new_entries)


# ---------------------------------------------------------------------------
# Scanner pipeline
# ---------------------------------------------------------------------------

def run_scan(auto_archive: bool = False, dry_run: bool = False) -> dict:
    """Run the full orphan doc scan."""
    log("Starting orphan doc scan...")

    orphans = find_orphan_docs()
    categories = categorize_orphans(orphans)

    log(f"Found {len(orphans)} orphan docs: "
        f"{len(categories['large_unwired'])} large unwired, "
        f"{len(categories['actionable'])} actionable, "
        f"{len(categories['outdated'])} outdated, "
        f"{len(categories['small_noise'])} small noise")

    # Generate report
    report = generate_report(orphans, categories)
    if not dry_run:
        safe_path(REPORT_FILE).write_text(report)
        log(f"Report written to {REPORT_FILE.name}")

    # Feed large unwired + actionable docs into ALPHA_STAGING for integration
    staged = 0
    if not dry_run:
        staged = stage_orphans_as_alpha(
            categories["large_unwired"] + categories["actionable"][:50],
            dry_run=dry_run,
        )
        log(f"Staged {staged} orphan docs as alpha entries for integration pipeline")

    # Auto-archive if requested
    archived = 0
    if auto_archive:
        archived = auto_archive_old(orphans, dry_run=dry_run)
        log(f"Auto-archived {archived} outdated docs")

    summary = {
        "total_orphans": len(orphans),
        "large_unwired": len(categories["large_unwired"]),
        "actionable": len(categories["actionable"]),
        "outdated": len(categories["outdated"]),
        "small_noise": len(categories["small_noise"]),
        "total_size_kb": round(sum(o["size_kb"] for o in orphans), 1),
        "archived": archived,
        "staged_to_alpha": staged,
    }

    return summary


def show_status() -> None:
    print("=" * 60)
    print("ORPHAN DOC SCANNER — Status")
    print("=" * 60)

    if REPORT_FILE.exists():
        try:
            age_h = (time.time() - REPORT_FILE.stat().st_mtime) / 3600
            print(f"\nLast report: {age_h:.1f}h ago")
            # Read first 20 lines for summary
            lines = REPORT_FILE.read_text().splitlines()[:20]
            for line in lines:
                print(f"  {line}")
        except Exception:
            print("Last report: error reading")
    else:
        print("No scan history (first run)")

    archived_count = 0
    if ARCHIVE_DIR.exists():
        archived_count = len(list(ARCHIVE_DIR.iterdir()))
    print(f"\nArchived orphans: {archived_count}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Orphan Doc Scanner")
    parser.add_argument("--scan", action="store_true", help="Run full scan")
    parser.add_argument("--auto-archive", action="store_true", help="Auto-archive outdated docs")
    parser.add_argument("--dry-run", action="store_true", help="Preview without changes")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--run", action="store_true", help="Alias for --scan")

    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.scan or args.run or args.dry_run:
        run_scan(auto_archive=args.auto_archive, dry_run=args.dry_run)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
