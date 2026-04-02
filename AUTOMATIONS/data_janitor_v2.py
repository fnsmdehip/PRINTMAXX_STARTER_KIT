#!/usr/bin/env python3
"""DATA JANITOR v2 - Full data hygiene cycle for PRINTMAXX"""

import os
import json
import csv
import shutil
import gzip
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
LOGS_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"
STATE_DIR = PROJECT_ROOT / "AUTOMATIONS" / "agent"
REPORTS_DIR = PROJECT_ROOT / "AUTOMATIONS" / "agent" / "swarm" / "reports"

# Ensure reports dir exists
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

class DataJanitor:
    def __init__(self):
        self.report = []
        self.stats = {
            "duplicates_removed": 0,
            "stale_entries_archived": 0,
            "logs_compressed": 0,
            "json_files_validated": 0,
            "json_files_fixed": 0,
            "orphan_files_found": 0,
            "total_size_reduction_mb": 0,
        }
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log(self, msg):
        """Log message to report"""
        print(msg)
        self.report.append(msg)

    def section(self, title):
        """Start a report section"""
        self.log(f"\n{'='*60}")
        self.log(f"  {title}")
        self.log(f"{'='*60}")

    # ====== STEP 1: DEDUPLICATE CSVs ======
    def deduplicate_csvs(self):
        """Deduplicate rows in LEDGER CSVs"""
        self.section("STEP 1: DEDUPLICATE CSVs")

        csv_files = list(LEDGER_DIR.glob("*.csv"))
        self.log(f"Found {len(csv_files)} CSV files to scan")

        for csv_file in csv_files[:10]:  # Process first 10 to start
            try:
                # Read CSV
                rows = []
                with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.DictReader(f)
                    if not reader.fieldnames:
                        continue
                    rows = list(reader)

                if not rows:
                    continue

                # Detect key columns for deduplication
                key_cols = []
                if 'url' in reader.fieldnames:
                    key_cols.append('url')
                if 'source' in reader.fieldnames:
                    key_cols.append('source')
                if 'content' in reader.fieldnames:
                    key_cols.append('content')

                if not key_cols:
                    continue

                # Find duplicates
                seen = {}
                unique_rows = []
                dupes_found = 0

                for row in sorted(rows, key=lambda r: r.get('timestamp', ''), reverse=True):
                    key = tuple(row.get(col, '') for col in key_cols)
                    if key not in seen:
                        seen[key] = True
                        unique_rows.append(row)
                    else:
                        dupes_found += 1

                if dupes_found > 0:
                    self.log(f"  {csv_file.name}: Found {dupes_found} duplicates (kept {len(unique_rows)} unique)")

                    # Backup original
                    backup = csv_file.with_stem(csv_file.stem + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                    shutil.copy(csv_file, backup)

                    # Write deduplicated
                    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
                        writer.writeheader()
                        writer.writerows(unique_rows)

                    self.stats["duplicates_removed"] += dupes_found

            except Exception as e:
                self.log(f"  ERROR {csv_file.name}: {str(e)}")

    # ====== STEP 2: STALE DATA ARCHIVE ======
    def archive_stale_pending(self):
        """Archive PENDING_REVIEW entries older than 7 days"""
        self.section("STEP 2: ARCHIVE STALE PENDING_REVIEW ENTRIES")

        csv_file = LEDGER_DIR / "ALPHA_STAGING.csv"
        if not csv_file.exists():
            self.log(f"  {csv_file.name} not found, skipping")
            return

        try:
            rows = []
            with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                rows = list(reader)

            now = datetime.now()
            stale_threshold = now - timedelta(days=7)

            active_rows = []
            archived_rows = []

            for row in rows:
                try:
                    created_at = datetime.fromisoformat(row.get('created_at', ''))
                    status = row.get('status', 'PENDING_REVIEW')

                    if status == 'PENDING_REVIEW' and created_at < stale_threshold:
                        archived_rows.append(row)
                    else:
                        active_rows.append(row)
                except:
                    active_rows.append(row)

            if archived_rows:
                self.log(f"  Found {len(archived_rows)} stale PENDING_REVIEW entries (>7 days old)")

                # Backup
                backup = csv_file.with_stem(csv_file.stem + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                shutil.copy(csv_file, backup)

                # Archive to separate file
                archive_file = LEDGER_DIR / f"ALPHA_STAGING_ARCHIVE_{datetime.now().strftime('%Y%m%d')}.csv"
                with open(archive_file, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(archived_rows)

                # Update main file
                with open(csv_file, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(active_rows)

                self.log(f"  Archived to {archive_file.name}")
                self.stats["stale_entries_archived"] += len(archived_rows)

        except Exception as e:
            self.log(f"  ERROR: {str(e)}")

    # ====== STEP 3: ARCHIVE LOGS ======
    def archive_old_logs(self):
        """Compress log files older than 3 days"""
        self.section("STEP 3: ARCHIVE OLD LOGS")

        if not LOGS_DIR.exists():
            self.log(f"  Logs directory not found")
            return

        log_files = list(LOGS_DIR.glob("*.log"))
        self.log(f"  Found {len(log_files)} log files")

        now = datetime.now()
        threshold = now - timedelta(days=3)

        for log_file in log_files:
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            if mtime < threshold:
                try:
                    # Compress
                    gz_file = log_file.with_suffix('.log.gz')
                    with open(log_file, 'rb') as f_in:
                        with gzip.open(gz_file, 'wb') as f_out:
                            f_out.write(f_in.read())

                    size_before = log_file.stat().st_size / (1024*1024)
                    size_after = gz_file.stat().st_size / (1024*1024)
                    reduction = size_before - size_after

                    self.log(f"  Compressed {log_file.name}: {size_before:.2f}MB → {size_after:.2f}MB ({reduction:.2f}MB saved)")
                    self.stats["logs_compressed"] += 1
                    self.stats["total_size_reduction_mb"] += reduction

                    # Keep original for reference
                    log_file.unlink()

                except Exception as e:
                    self.log(f"  ERROR {log_file.name}: {str(e)}")

    # ====== STEP 4: VALIDATE JSON ======
    def validate_json_states(self):
        """Check all JSON state files for corruption"""
        self.section("STEP 4: VALIDATE JSON STATE FILES")

        json_files = list(STATE_DIR.rglob("*.json")) if STATE_DIR.exists() else []
        self.log(f"  Found {len(json_files)} JSON files to validate")

        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    json.load(f)
                self.stats["json_files_validated"] += 1

            except json.JSONDecodeError as e:
                self.log(f"  CORRUPTED: {json_file.name} - {str(e)}")
                # Try to fix with empty object
                try:
                    backup = json_file.with_suffix('.json.corrupt')
                    shutil.copy(json_file, backup)
                    with open(json_file, 'w') as f:
                        json.dump({}, f)
                    self.log(f"    Fixed: replaced with empty object")
                    self.stats["json_files_fixed"] += 1
                except Exception as fix_e:
                    self.log(f"    Could not fix: {str(fix_e)}")

    # ====== STEP 5: FIND ORPHANS ======
    def find_orphans(self):
        """Find orphan files and dead references"""
        self.section("STEP 5: FIND ORPHAN FILES")

        # Find all Python files that reference file paths
        config_files = list(PROJECT_ROOT.rglob("*.py")) + list(PROJECT_ROOT.rglob("*.json"))

        # This is a simple heuristic - look for very large directories
        large_dirs = []
        for d in [PROJECT_ROOT / "LEDGER", PROJECT_ROOT / "CONTENT", PROJECT_ROOT / "AUTOMATIONS"]:
            if d.exists():
                size_mb = sum(f.stat().st_size for f in d.rglob("*") if f.is_file()) / (1024*1024)
                if size_mb > 100:
                    large_dirs.append((d.name, size_mb))

        if large_dirs:
            self.log("  Large directories (>100MB):")
            for name, size_mb in sorted(large_dirs, key=lambda x: x[1], reverse=True):
                self.log(f"    {name}: {size_mb:.1f}MB")
                self.stats["orphan_files_found"] += 1

    # ====== STEP 6: SIZE REPORT ======
    def generate_size_report(self):
        """Analyze directory sizes"""
        self.section("STEP 6: DIRECTORY SIZE REPORT")

        dirs_to_scan = [
            "LEDGER",
            "AUTOMATIONS",
            "CONTENT",
            "MONEY_METHODS",
            "LANDING",
            "PRODUCTS",
            "DIGITAL_PRODUCTS"
        ]

        sizes = []
        for dir_name in dirs_to_scan:
            dir_path = PROJECT_ROOT / dir_name
            if dir_path.exists():
                size_mb = sum(f.stat().st_size for f in dir_path.rglob("*") if f.is_file()) / (1024*1024)
                sizes.append((dir_name, size_mb))

        self.log("\nTop directories by size:")
        for name, size_mb in sorted(sizes, key=lambda x: x[1], reverse=True):
            if size_mb > 1:
                self.log(f"  {name:30s}: {size_mb:10.1f}MB")

    # ====== FINAL REPORT ======
    def generate_report(self):
        """Write final report to file"""
        self.section("FINAL REPORT")

        report_file = REPORTS_DIR / f"data_janitor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        report_lines = [
            "# DATA JANITOR REPORT",
            f"\n**Generated:** {self.timestamp}",
            "\n## Statistics\n",
            f"- Duplicates removed: {self.stats['duplicates_removed']}",
            f"- Stale entries archived: {self.stats['stale_entries_archived']}",
            f"- Logs compressed: {self.stats['logs_compressed']}",
            f"- JSON files validated: {self.stats['json_files_validated']}",
            f"- JSON files fixed: {self.stats['json_files_fixed']}",
            f"- Large directories flagged: {self.stats['orphan_files_found']}",
            f"- Total size reduction: {self.stats['total_size_reduction_mb']:.2f}MB",
            "\n## Detailed Report\n",
            "\n".join(self.report)
        ]

        report_text = "\n".join(report_lines)

        with open(report_file, 'w') as f:
            f.write(report_text)

        self.log(f"\n✓ Report saved to: {report_file.name}")
        return report_file

    def run_full_cycle(self):
        """Execute full data janitor cycle"""
        self.log("🧹 DATA JANITOR v2 - Starting full cycle\n")

        # Run all steps
        self.deduplicate_csvs()
        self.archive_stale_pending()
        self.archive_old_logs()
        self.validate_json_states()
        self.find_orphans()
        self.generate_size_report()
        report_file = self.generate_report()

        self.log("\n" + "="*60)
        self.log("✓ DATA JANITOR CYCLE COMPLETE")
        self.log("="*60)
        return report_file

if __name__ == "__main__":
    janitor = DataJanitor()
    report_file = janitor.run_full_cycle()
