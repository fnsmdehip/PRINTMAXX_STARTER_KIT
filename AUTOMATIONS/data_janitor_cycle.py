#!/usr/bin/env python3

from __future__ import annotations
"""
DATA JANITOR CYCLE - PRINTMAXX
Comprehensive data cleaning, deduplication, and archival.
Runs every 12 hours via cron.
"""

import csv
import json
import os
import gzip
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import hashlib

BASE_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = BASE_DIR / "LEDGER"
LOGS_DIR = BASE_DIR / "AUTOMATIONS" / "logs"
AGENT_DIR = BASE_DIR / "AUTOMATIONS" / "agent"
REPORTS_DIR = BASE_DIR / "AUTOMATIONS" / "agent" / "swarm" / "reports"

# Ensure reports dir exists
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

class DataJanitor:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d")
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "deduplication": {},
            "stale_data": {},
            "archive": {},
            "json_validation": {},
            "orphans": {"missing_refs": [], "unreferenced_files": []},
            "size_report": {}
        }
        self.errors = []

    def deduplicate_csv(self, csv_path: Path) -> dict:
        """Deduplicate CSV by removing duplicate rows, keeping newest."""
        if not csv_path.exists():
            return {"status": "file_not_found", "path": str(csv_path)}

        try:
            # Read CSV
            rows = []
            with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                if not fieldnames:
                    return {"status": "empty_file", "path": str(csv_path)}
                rows = list(reader)

            original_count = len(rows)

            # Define key columns for deduplication (URL-based or content-based)
            key_cols = []
            if 'source_url' in fieldnames:
                key_cols = ['source_url']
            elif 'url' in fieldnames:
                key_cols = ['url']
            elif 'link' in fieldnames:
                key_cols = ['link']

            if not key_cols:
                return {"status": "no_key_column", "path": str(csv_path), "count": original_count}

            # Deduplicate: keep last occurrence (newest)
            seen = {}
            for i, row in enumerate(rows):
                key_val = tuple(row.get(col, '') for col in key_cols)
                seen[key_val] = i

            deduped = [rows[i] for key_val, i in seen.items()]
            deduped_count = len(deduped)
            removed = original_count - deduped_count

            if removed > 0:
                # Backup original
                backup_path = csv_path.with_suffix(f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
                shutil.copy2(csv_path, backup_path)

                # Write deduped CSV
                with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(deduped)

            return {
                "status": "success",
                "path": str(csv_path),
                "original_rows": original_count,
                "deduped_rows": deduped_count,
                "removed": removed,
                "backup": str(backup_path) if removed > 0 else None
            }
        except Exception as e:
            self.errors.append(f"Error deduplicating {csv_path}: {str(e)}")
            return {"status": "error", "path": str(csv_path), "error": str(e)}

    def check_stale_pending_review(self) -> dict:
        """Find PENDING_REVIEW entries in ALPHA_STAGING.csv older than 7 days."""
        alpha_file = LEDGER_DIR / "ALPHA_STAGING.csv"
        if not alpha_file.exists():
            return {"status": "file_not_found"}

        try:
            stale_count = 0
            recent_count = 0
            threshold_date = datetime.now() - timedelta(days=7)

            with open(alpha_file, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('status') == 'PENDING_REVIEW':
                        try:
                            created_at = datetime.fromisoformat(row.get('created_at', ''))
                            if created_at < threshold_date:
                                stale_count += 1
                            else:
                                recent_count += 1
                        except:
                            pass

            return {
                "status": "success",
                "pending_review_stale_7d": stale_count,
                "pending_review_recent": recent_count,
                "threshold_date": threshold_date.isoformat()
            }
        except Exception as e:
            self.errors.append(f"Error checking stale data: {str(e)}")
            return {"status": "error", "error": str(e)}

    def archive_old_logs(self) -> dict:
        """Compress log files older than 3 days."""
        if not LOGS_DIR.exists():
            return {"status": "logs_dir_not_found"}

        try:
            threshold = datetime.now() - timedelta(days=3)
            compressed_count = 0
            total_size_before = 0
            total_size_after = 0

            for log_file in LOGS_DIR.glob("*.log"):
                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                if mtime < threshold:
                    try:
                        total_size_before += log_file.stat().st_size
                        gz_path = log_file.with_suffix('.log.gz')

                        with open(log_file, 'rb') as f_in:
                            with gzip.open(gz_path, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)

                        # Delete original if compression successful
                        if gz_path.exists():
                            log_file.unlink()
                            compressed_count += 1
                            total_size_after += gz_path.stat().st_size
                    except Exception as e:
                        self.errors.append(f"Error archiving {log_file}: {str(e)}")

            return {
                "status": "success",
                "files_compressed": compressed_count,
                "size_before_mb": round(total_size_before / 1024 / 1024, 2),
                "size_after_mb": round(total_size_after / 1024 / 1024, 2),
                "compression_ratio": round(total_size_after / total_size_before, 2) if total_size_before > 0 else 0
            }
        except Exception as e:
            self.errors.append(f"Error archiving logs: {str(e)}")
            return {"status": "error", "error": str(e)}

    def validate_json_files(self) -> dict:
        """Validate all JSON state files for corruption."""
        json_files = list(AGENT_DIR.glob("**/*.json")) + list(LEDGER_DIR.glob("**/*.json"))

        results = {
            "total_files": len(json_files),
            "valid": 0,
            "invalid": [],
            "empty": []
        }

        for json_file in json_files:
            try:
                if json_file.stat().st_size == 0:
                    results["empty"].append(str(json_file))
                else:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        json.load(f)
                    results["valid"] += 1
            except json.JSONDecodeError as e:
                results["invalid"].append({"file": str(json_file), "error": str(e)})
                self.errors.append(f"Invalid JSON in {json_file}: {str(e)}")
            except Exception as e:
                results["invalid"].append({"file": str(json_file), "error": str(e)})

        return results

    def size_report(self) -> dict:
        """Generate size report for key directories."""
        dirs_to_check = [
            BASE_DIR / "LEDGER",
            BASE_DIR / "AUTOMATIONS",
            BASE_DIR / "AUTOMATIONS" / "logs",
            BASE_DIR / "MEDIA",
            BASE_DIR / "CONTENT"
        ]

        report = {}
        for dir_path in dirs_to_check:
            if dir_path.exists():
                size_bytes = sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
                size_mb = round(size_bytes / 1024 / 1024, 2)
                report[str(dir_path.name)] = {
                    "path": str(dir_path),
                    "size_mb": size_mb,
                    "size_gb": round(size_mb / 1024, 2),
                    "flag": size_mb > 50 * 1024  # Flag if > 50GB
                }

        return report

    def find_orphan_files(self) -> dict:
        """Find orphan files and unreferenced configs."""
        results = {
            "missing_file_references": [],
            "config_files": {
                "app_factory_specs": 0,
                "venture_configs": 0
            }
        }

        # Check if referenced files exist
        config_refs = [
            AGENT_DIR / "autonomy" / "app_factory_spec_queue.json",
            BASE_DIR / "OPS" / "PERSISTENT_TASK_TRACKER.md"
        ]

        for ref_file in config_refs:
            if ref_file.exists():
                try:
                    if ref_file.suffix == '.json':
                        with open(ref_file, 'r') as f:
                            data = json.load(f)
                            # Quick scan for file references
                            if isinstance(data, dict):
                                results["config_files"]["app_factory_specs"] += len(data)
                except:
                    pass

        return results

    def run_all(self):
        """Execute full data janitor cycle."""
        print("🧹 DATA JANITOR CYCLE STARTING")
        print(f"   Timestamp: {self.report['timestamp']}")

        # 1. DEDUPLICATE CSVs
        print("\n📊 DEDUPLICATING CSVs...")
        csv_files = [
            LEDGER_DIR / "ALPHA_STAGING.csv",
            LEDGER_DIR / "USER_PROMPTS.jsonl",
            LEDGER_DIR / "COMPETITIVE_INTEL.csv",
            LEDGER_DIR / "REDDIT_PAIN_POINTS.csv",
            LEDGER_DIR / "TREND_SIGNALS.csv"
        ]

        for csv_file in csv_files:
            if csv_file.exists():
                result = self.deduplicate_csv(csv_file)
                self.report["deduplication"][str(csv_file.name)] = result
                if result.get("removed", 0) > 0:
                    print(f"   ✓ {csv_file.name}: Removed {result['removed']} dupes")

        # 2. CHECK STALE DATA
        print("\n⏱️  CHECKING STALE DATA...")
        self.report["stale_data"] = self.check_stale_pending_review()
        if self.report["stale_data"].get("pending_review_stale_7d", 0) > 0:
            print(f"   ⚠️  {self.report['stale_data']['pending_review_stale_7d']} entries >7 days old")

        # 3. ARCHIVE LOGS
        print("\n📦 ARCHIVING LOGS...")
        self.report["archive"] = self.archive_old_logs()
        if self.report["archive"].get("files_compressed", 0) > 0:
            print(f"   ✓ Compressed {self.report['archive']['files_compressed']} log files")

        # 4. VALIDATE JSON
        print("\n✅ VALIDATING JSON...")
        self.report["json_validation"] = self.validate_json_files()
        print(f"   ✓ {self.report['json_validation']['valid']} valid JSON files")
        if self.report["json_validation"]["invalid"]:
            print(f"   ⚠️  {len(self.report['json_validation']['invalid'])} invalid files")

        # 5. SIZE REPORT
        print("\n📈 GENERATING SIZE REPORT...")
        self.report["size_report"] = self.size_report()
        for name, info in self.report["size_report"].items():
            if info.get("flag"):
                print(f"   🚩 {name}: {info['size_gb']}GB (exceeds 50GB)")

        # 6. ORPHAN FILES
        print("\n🔍 CHECKING ORPHAN FILES...")
        self.report["orphans"] = self.find_orphan_files()

        # 7. WRITE REPORT
        report_path = REPORTS_DIR / f"data_janitor_report_{self.timestamp}.md"
        self._write_markdown_report(report_path)
        print(f"\n✅ CYCLE COMPLETE - Report: {report_path}")

        if self.errors:
            print(f"\n⚠️  {len(self.errors)} errors encountered")
            for err in self.errors[:5]:
                print(f"   - {err}")

        return self.report

    def _write_markdown_report(self, path: Path):
        """Write human-readable markdown report."""
        content = f"""# Data Janitor Report — {self.timestamp}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

- **Deduplication:** {sum(1 for v in self.report['deduplication'].values() if v.get('removed', 0) > 0)} CSVs processed
- **Stale Data:** {self.report['stale_data'].get('pending_review_stale_7d', 0)} PENDING_REVIEW entries >7 days
- **Logs Compressed:** {self.report['archive'].get('files_compressed', 0)} files
- **JSON Validation:** {self.report['json_validation'].get('valid', 0)} valid / {len(self.report['json_validation'].get('invalid', []))} invalid
- **Errors:** {len(self.errors)}

## Deduplication Results

| File | Original | Deduped | Removed | Status |
|------|----------|---------|---------|--------|
"""

        for filename, result in self.report['deduplication'].items():
            if result['status'] == 'success':
                content += f"| {filename} | {result.get('original_rows', '?')} | {result.get('deduped_rows', '?')} | {result.get('removed', 0)} | ✓ |\n"
            else:
                content += f"| {filename} | — | — | — | {result['status']} |\n"

        content += f"""
## Stale Data
- PENDING_REVIEW (>7 days): {self.report['stale_data'].get('pending_review_stale_7d', 0)}
- PENDING_REVIEW (recent): {self.report['stale_data'].get('pending_review_recent', 0)}

## Archive Status
- Files Compressed: {self.report['archive'].get('files_compressed', 0)}
- Size Before: {self.report['archive'].get('size_before_mb', 0)}MB
- Size After: {self.report['archive'].get('size_after_mb', 0)}MB
- Ratio: {self.report['archive'].get('compression_ratio', 0)}x

## JSON Validation
- Valid Files: {self.report['json_validation'].get('valid', 0)}
- Invalid Files: {len(self.report['json_validation'].get('invalid', []))}
- Empty Files: {len(self.report['json_validation'].get('empty', []))}

## Size Report (Largest Directories)

| Directory | Size | Status |
|-----------|------|--------|
"""

        for name, info in sorted(self.report['size_report'].items(), key=lambda x: x[1].get('size_gb', 0), reverse=True):
            flag = "🚩" if info.get('flag') else "✓"
            content += f"| {name} | {info['size_gb']}GB | {flag} |\n"

        content += f"""
## Errors ({len(self.errors)})

"""
        if self.errors:
            for err in self.errors:
                content += f"- {err}\n"
        else:
            content += "None.\n"

        path.write_text(content)

if __name__ == "__main__":
    janitor = DataJanitor()
    janitor.run_all()
