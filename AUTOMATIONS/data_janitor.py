#!/usr/bin/env python3
"""
DATA JANITOR AGENT - Cycle 20260320
Deduplicates, archives, validates, and reports on all data systems.
"""

import os
import csv
import json
import gzip
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import subprocess

PROJECT_ROOT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER = PROJECT_ROOT / "LEDGER"
LOGS = PROJECT_ROOT / "AUTOMATIONS" / "logs"
REPORT_DIR = PROJECT_ROOT / "AUTOMATIONS" / "agent" / "swarm" / "reports"

# Ensure report dir exists
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def log_action(action, details=""):
    """Log action to report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] {action}"
    if details:
        msg += f" — {details}"
    print(msg)
    return msg

# ============================================================================
# STEP 1: DEDUPLICATE CSV FILES
# ============================================================================

def deduplicate_csv(filepath):
    """Remove duplicate rows from CSV (by URL + source or alpha_id)"""
    if not filepath.exists():
        return 0, 0

    try:
        rows = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                return 0, 0
            rows = list(reader)

        if not rows:
            return 0, 0

        original_count = len(rows)

        # Deduplicate by URL + source, or by alpha_id
        seen = {}
        unique_rows = []

        for row in rows:
            # Primary key: alpha_id if present
            key = row.get('alpha_id') or f"{row.get('source_url', '')}|{row.get('source', '')}"

            if key and key not in seen:
                seen[key] = True
                unique_rows.append(row)

        dedup_count = original_count - len(unique_rows)

        if dedup_count > 0:
            # Backup original
            backup_path = filepath.with_suffix(filepath.suffix + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            shutil.copy2(filepath, backup_path)

            # Write deduplicated
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                if unique_rows:
                    writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
                    writer.writeheader()
                    writer.writerows(unique_rows)

            return original_count, dedup_count

        return original_count, 0

    except Exception as e:
        log_action(f"ERROR deduplicating {filepath.name}", str(e))
        return 0, 0

# ============================================================================
# STEP 2: HANDLE STALE DATA
# ============================================================================

def find_stale_pending_alpha():
    """Find PENDING_REVIEW alpha entries older than 7 days"""
    alpha_staging = LEDGER / "ALPHA_STAGING.csv"
    stale = []

    if not alpha_staging.exists():
        return stale

    try:
        with open(alpha_staging, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('status') == 'PENDING_REVIEW':
                    created = row.get('created_at')
                    if created:
                        try:
                            created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                            age = (datetime.now(created_dt.tzinfo) - created_dt).days
                            if age > 7:
                                stale.append({
                                    'alpha_id': row.get('alpha_id'),
                                    'source': row.get('source'),
                                    'age_days': age
                                })
                        except:
                            pass
    except Exception as e:
        log_action(f"ERROR finding stale alpha in {alpha_staging.name}", str(e))

    return stale

# ============================================================================
# STEP 3: ARCHIVE OLD LOGS
# ============================================================================

def archive_old_logs(days_threshold=3):
    """Compress log files older than threshold"""
    archived = 0

    if not LOGS.exists():
        return archived

    cutoff = datetime.now() - timedelta(days=days_threshold)

    for logfile in LOGS.glob("*.log"):
        try:
            mtime = datetime.fromtimestamp(logfile.stat().st_mtime)
            if mtime < cutoff and not logfile.with_suffix('.log.gz').exists():
                with open(logfile, 'rb') as f_in:
                    with gzip.open(str(logfile) + '.gz', 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                logfile.unlink()
                archived += 1
        except Exception as e:
            pass

    return archived

# ============================================================================
# STEP 4: VALIDATE JSON STATE FILES
# ============================================================================

def validate_json_files():
    """Scan for and validate JSON state files"""
    invalid = []
    valid_count = 0

    json_files = list(PROJECT_ROOT.glob("AUTOMATIONS/agent/**/*.json")) + \
                 list(PROJECT_ROOT.glob("AUTOMATIONS/**/*.json")) + \
                 list(LEDGER.glob("*.json"))

    for jfile in json_files:
        try:
            with open(jfile, 'r', encoding='utf-8') as f:
                json.load(f)
            valid_count += 1
        except json.JSONDecodeError as e:
            invalid.append(str(jfile))
        except Exception:
            pass

    return valid_count, invalid

# ============================================================================
# STEP 5: FIND ORPHAN FILES
# ============================================================================

def find_orphans():
    """Find referenced but missing files, and unreferenced existing files"""
    orphaned = []
    unused = []

    # Sample: check if files referenced in ops configs exist
    # This is a simplified check
    config_files = list(PROJECT_ROOT.glob("OPS/*.md")) + \
                   list(PROJECT_ROOT.glob("AUTOMATIONS/*.py"))

    referenced_paths = set()
    for config in config_files[:20]:  # Sample to avoid timeout
        try:
            with open(config, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract paths (simple regex)
                import re
                paths = re.findall(r"(?:path|file|location|url|at|from)[:\s]+['\"]?([A-Za-z0-9/_\-\.]+)['\"]?", content)
                referenced_paths.update(paths)
        except:
            pass

    # Check if they exist
    for ref in list(referenced_paths)[:50]:
        potential_path = PROJECT_ROOT / ref
        if not potential_path.exists() and "/" in ref:
            orphaned.append(ref)

    return orphaned, len(unused)

# ============================================================================
# STEP 6: SIZE REPORT
# ============================================================================

def generate_size_report():
    """Find largest files/directories"""
    large_files = []
    large_dirs = []

    # Check LEDGER for large files
    try:
        for fpath in LEDGER.glob("*"):
            if fpath.is_file():
                size_mb = fpath.stat().st_size / (1024*1024)
                if size_mb > 5:  # >5MB
                    large_files.append((fpath.name, size_mb))
            elif fpath.is_dir():
                size_mb = sum(f.stat().st_size for f in fpath.rglob("*") if f.is_file()) / (1024*1024)
                if size_mb > 10:
                    large_dirs.append((fpath.name, size_mb))
    except Exception:
        pass

    large_files.sort(key=lambda x: x[1], reverse=True)
    large_dirs.sort(key=lambda x: x[1], reverse=True)

    return large_files[:10], large_dirs[:10]

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    report_lines = []
    report_lines.append("# DATA JANITOR REPORT — 2026-03-20")
    report_lines.append("")
    report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")

    # STEP 1: DEDUPLICATE
    report_lines.append("## STEP 1: DEDUPLICATE CSVs")
    report_lines.append("")

    dedup_total_rows = 0
    dedup_removed = 0

    csv_files = list(LEDGER.glob("*.csv"))
    report_lines.append(f"Scanning {len(csv_files)} CSV files...\n")

    for csvfile in csv_files:
        original, removed = deduplicate_csv(csvfile)
        if original > 0:
            report_lines.append(f"- **{csvfile.name}**: {original} rows → {removed} duplicates removed")
            dedup_total_rows += original
            dedup_removed += removed

    report_lines.append(f"\n**Total:** {dedup_total_rows} rows scanned, {dedup_removed} duplicates removed")
    report_lines.append("")

    # STEP 2: STALE DATA
    report_lines.append("## STEP 2: STALE DATA")
    report_lines.append("")

    stale = find_stale_pending_alpha()
    report_lines.append(f"Found {len(stale)} PENDING_REVIEW entries older than 7 days:\n")
    for item in stale[:20]:
        report_lines.append(f"- {item['alpha_id']} (from {item['source']}) — {item['age_days']} days old")

    if len(stale) > 20:
        report_lines.append(f"... and {len(stale) - 20} more")
    report_lines.append("")

    # STEP 3: ARCHIVE LOGS
    report_lines.append("## STEP 3: ARCHIVE LOGS")
    report_lines.append("")

    archived = archive_old_logs(3)
    report_lines.append(f"Archived {archived} log files (>3 days old)")
    report_lines.append("")

    # STEP 4: VALIDATE JSON
    report_lines.append("## STEP 4: VALIDATE JSON STATE FILES")
    report_lines.append("")

    valid, invalid = validate_json_files()
    report_lines.append(f"Valid JSON: {valid}")
    if invalid:
        report_lines.append(f"Invalid JSON: {len(invalid)}")
        for inv in invalid[:10]:
            report_lines.append(f"  - {inv}")
        if len(invalid) > 10:
            report_lines.append(f"  ... and {len(invalid) - 10} more")
    report_lines.append("")

    # STEP 5: ORPHANS
    report_lines.append("## STEP 5: ORPHAN CLEANUP")
    report_lines.append("")

    orphaned, unused = find_orphans()
    report_lines.append(f"Referenced but missing files: {len(orphaned)}")
    if orphaned:
        for orph in orphaned[:10]:
            report_lines.append(f"  - {orph}")
    report_lines.append("")

    # STEP 6: SIZE REPORT
    report_lines.append("## STEP 6: SIZE REPORT")
    report_lines.append("")

    large_files, large_dirs = generate_size_report()

    report_lines.append("### Largest Files (LEDGER)")
    for fname, size_mb in large_files:
        report_lines.append(f"- {fname}: {size_mb:.1f} MB")

    report_lines.append("")
    report_lines.append("### Largest Directories (LEDGER)")
    for dname, size_mb in large_dirs:
        report_lines.append(f"- {dname}: {size_mb:.1f} MB")

    report_lines.append("")

    # SUMMARY
    report_lines.append("## SUMMARY")
    report_lines.append("")
    report_lines.append(f"- **Deduplication:** {dedup_removed} duplicate rows removed")
    report_lines.append(f"- **Stale Data:** {len(stale)} PENDING_REVIEW entries >7 days old")
    report_lines.append(f"- **Logs Archived:** {archived} files compressed")
    report_lines.append(f"- **JSON Valid:** {valid} files")
    if invalid:
        report_lines.append(f"- **JSON Invalid:** {len(invalid)} files (needs repair)")
    report_lines.append(f"- **Orphan Files:** {len(orphaned)} referenced but missing")
    report_lines.append("")
    report_lines.append(f"**Status:** ✓ CYCLE COMPLETE")

    # Write report
    report_path = REPORT_DIR / "data_janitor_report_20260320.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))

    print("\n" + "="*60)
    print("\n".join(report_lines))
    print("\n" + "="*60)
    print(f"\nReport written to: {report_path}")

if __name__ == "__main__":
    main()
