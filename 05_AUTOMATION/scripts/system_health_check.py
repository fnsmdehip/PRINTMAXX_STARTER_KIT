#!/usr/bin/env python3
"""
System Health Check - Validate PRINTMAXX infrastructure integrity.

Checks:
1. LEDGER CSV validity (parseable, correct headers, no corruption)
2. Duplicate detection across key files
3. Missing required fields
4. Cross-reference validation (alpha IDs, method IDs)
5. Ralph loop infrastructure completeness
6. File system consistency
7. Data freshness (stale files)

Usage:
    python3 system_health_check.py           # Full health check
    python3 system_health_check.py --ledger  # LEDGER files only
    python3 system_health_check.py --ralph   # Ralph loops only
    python3 system_health_check.py --apps    # App builds only
    python3 system_health_check.py --fix     # Auto-fix what's possible
"""

import csv
import json
import argparse
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_DIR / "LEDGER"
RALPH_DIR = PROJECT_DIR / "ralph" / "loops"
BUILDS_DIR = PROJECT_DIR / "MONEY_METHODS" / "APP_FACTORY" / "builds"
FINANCIALS_DIR = PROJECT_DIR / "FINANCIALS"


class HealthChecker:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.passes = []

    def add_issue(self, severity: str, component: str, message: str):
        entry = {"severity": severity, "component": component, "message": message}
        if severity == "ERROR":
            self.issues.append(entry)
        elif severity == "WARNING":
            self.warnings.append(entry)
        else:
            self.passes.append(entry)

    def check_csv_validity(self, filepath: Path) -> Tuple[bool, str]:
        """Check if a CSV file is valid and parseable."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            if not content.strip():
                return False, "Empty file"

            lines = content.strip().split('\n')
            if len(lines) < 1:
                return False, "No header row"

            # Try parsing
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                if not headers:
                    return False, "No headers found"

                row_count = 0
                for row in reader:
                    row_count += 1
                    # Check for field count mismatch
                    if len(row) != len(headers):
                        return False, f"Row {row_count + 1}: field count mismatch ({len(row)} vs {len(headers)} headers)"

            return True, f"OK ({row_count} rows, {len(headers)} columns)"

        except csv.Error as e:
            return False, f"CSV parse error: {e}"
        except Exception as e:
            return False, f"Read error: {e}"

    def check_ledger(self):
        """Validate all LEDGER CSV files."""
        print("\n=== LEDGER Health Check ===\n")

        csv_files = sorted(LEDGER_DIR.glob("*.csv"))
        if not csv_files:
            self.add_issue("ERROR", "LEDGER", "No CSV files found in LEDGER/")
            return

        for filepath in csv_files:
            valid, message = self.check_csv_validity(filepath)
            if valid:
                self.add_issue("PASS", f"LEDGER/{filepath.name}", message)
            else:
                self.add_issue("ERROR", f"LEDGER/{filepath.name}", message)

        # Check ALPHA_STAGING specifically
        self._check_alpha_staging()

        # Check for duplicate files
        self._check_duplicate_alpha_files()

        # Check cross-references
        self._check_cross_references()

    def _check_alpha_staging(self):
        """Deep check on ALPHA_STAGING.csv."""
        filepath = LEDGER_DIR / "ALPHA_STAGING.csv"
        if not filepath.exists():
            self.add_issue("ERROR", "ALPHA_STAGING", "File missing")
            return

        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            # Check required fields
            required = ['alpha_id', 'source', 'category', 'status']
            headers = reader.fieldnames or []
            for field in required:
                if field not in headers:
                    self.add_issue("ERROR", "ALPHA_STAGING", f"Missing required column: {field}")

            # Check for duplicate alpha_ids
            ids = [r.get('alpha_id', '') for r in rows if r.get('alpha_id')]
            dupes = [id for id, count in Counter(ids).items() if count > 1]
            if dupes:
                self.add_issue("WARNING", "ALPHA_STAGING", f"Duplicate alpha_ids: {dupes[:5]}")

            # Check for duplicate source_urls
            urls = [r.get('source_url', '') for r in rows if r.get('source_url')]
            url_dupes = [u for u, c in Counter(urls).items() if c > 1 and u]
            if url_dupes:
                self.add_issue("WARNING", "ALPHA_STAGING", f"{len(url_dupes)} duplicate source_urls found")

            # Check status distribution
            statuses = Counter(r.get('status', 'MISSING') for r in rows)
            pending = statuses.get('PENDING_REVIEW', 0)
            if pending > 100:
                self.add_issue("WARNING", "ALPHA_STAGING", f"{pending} entries PENDING_REVIEW (consider batch review)")

            # Stats
            self.add_issue("PASS", "ALPHA_STAGING",
                          f"Total: {len(rows)}, Statuses: {dict(statuses)}")

        except Exception as e:
            self.add_issue("ERROR", "ALPHA_STAGING", f"Check failed: {e}")

    def _check_duplicate_alpha_files(self):
        """Check for stray alpha files that should be consolidated."""
        alpha_files = list(LEDGER_DIR.glob("ALPHA_STAGING*.csv"))
        if len(alpha_files) > 1:
            extras = [f.name for f in alpha_files if f.name != "ALPHA_STAGING.csv"]
            self.add_issue("WARNING", "LEDGER",
                          f"Multiple alpha files found (should consolidate): {extras}")

    def _check_cross_references(self):
        """Check that referenced IDs exist across files."""
        # Check method IDs in various files
        try:
            tracker_path = LEDGER_DIR / "MONEY_METHODS_TRACKER.csv"
            if tracker_path.exists():
                with open(tracker_path, 'r', encoding='utf-8', errors='replace') as f:
                    reader = csv.DictReader(f)
                    valid_methods = {r.get('method_id', '') for r in reader}

                # Check REVENUE_TRACKER references
                rev_path = FINANCIALS_DIR / "REVENUE_TRACKER.csv"
                if rev_path.exists():
                    with open(rev_path, 'r', encoding='utf-8', errors='replace') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            mid = row.get('method_id', '')
                            if mid and mid not in valid_methods and mid != 'EXAMPLE' and mid != 'NONE':
                                self.add_issue("WARNING", "CROSS_REF",
                                             f"REVENUE_TRACKER references unknown method: {mid}")
        except Exception as e:
            self.add_issue("WARNING", "CROSS_REF", f"Cross-reference check failed: {e}")

    def check_ralph(self):
        """Validate ralph loop infrastructure."""
        print("\n=== Ralph Loop Health Check ===\n")

        if not RALPH_DIR.exists():
            self.add_issue("ERROR", "RALPH", "Ralph loops directory missing")
            return

        loops = sorted([d for d in RALPH_DIR.iterdir() if d.is_dir()])

        for loop_dir in loops:
            name = loop_dir.name

            # Check prompt.md
            if not (loop_dir / "prompt.md").exists():
                self.add_issue("ERROR", f"ralph/{name}", "Missing prompt.md")
            else:
                # Check prompt is not empty
                size = (loop_dir / "prompt.md").stat().st_size
                if size < 100:
                    self.add_issue("WARNING", f"ralph/{name}", f"prompt.md suspiciously small ({size} bytes)")
                else:
                    self.add_issue("PASS", f"ralph/{name}", f"prompt.md OK ({size} bytes)")

            # Check run.sh
            if not (loop_dir / "run.sh").exists():
                self.add_issue("ERROR", f"ralph/{name}", "Missing run.sh")
            else:
                # Check executable
                if not os.access(loop_dir / "run.sh", os.X_OK):
                    self.add_issue("WARNING", f"ralph/{name}", "run.sh not executable")
                else:
                    self.add_issue("PASS", f"ralph/{name}", "run.sh OK")

            # Check .ralph directory
            ralph_state = loop_dir / ".ralph"
            if not ralph_state.exists():
                self.add_issue("WARNING", f"ralph/{name}", "Missing .ralph/ state directory")
            else:
                # Check progress.md
                if not (ralph_state / "progress.md").exists():
                    self.add_issue("WARNING", f"ralph/{name}", "Missing .ralph/progress.md")

            # Check output directory
            if not (loop_dir / "output").exists():
                self.add_issue("WARNING", f"ralph/{name}", "Missing output/ directory")

    def check_apps(self):
        """Validate app build infrastructure."""
        print("\n=== App Build Health Check ===\n")

        if not BUILDS_DIR.exists():
            self.add_issue("ERROR", "APPS", "Builds directory missing")
            return

        sdk54_apps = sorted([d for d in BUILDS_DIR.iterdir()
                            if d.is_dir() and d.name.endswith('-sdk54')])
        legacy_apps = sorted([d for d in BUILDS_DIR.iterdir()
                             if d.is_dir() and not d.name.endswith('-sdk54')
                             and d.name not in ['node_modules']
                             and not d.name.startswith('.')])

        for app_dir in sdk54_apps:
            name = app_dir.name

            # Check package.json
            pkg_path = app_dir / "package.json"
            if not pkg_path.exists():
                self.add_issue("ERROR", f"apps/{name}", "Missing package.json")
                continue

            try:
                with open(pkg_path) as f:
                    pkg = json.load(f)
            except json.JSONDecodeError:
                self.add_issue("ERROR", f"apps/{name}", "Invalid package.json")
                continue

            # Check app.json
            app_json_path = app_dir / "app.json"
            if not app_json_path.exists():
                self.add_issue("WARNING", f"apps/{name}", "Missing app.json")
            else:
                try:
                    with open(app_json_path) as f:
                        app_config = json.load(f)
                    self.add_issue("PASS", f"apps/{name}", "app.json valid")
                except json.JSONDecodeError:
                    self.add_issue("ERROR", f"apps/{name}", "Invalid app.json")

            # Check eas.json
            if not (app_dir / "eas.json").exists():
                self.add_issue("WARNING", f"apps/{name}", "Missing eas.json (needed for builds)")

            # Check node_modules
            if not (app_dir / "node_modules").exists():
                self.add_issue("WARNING", f"apps/{name}", "node_modules not installed")
            else:
                self.add_issue("PASS", f"apps/{name}", "Dependencies installed")

            # Check for TypeScript config
            if not (app_dir / "tsconfig.json").exists():
                self.add_issue("WARNING", f"apps/{name}", "Missing tsconfig.json")

        # Summary
        self.add_issue("PASS", "APPS",
                      f"SDK54 apps: {len(sdk54_apps)}, Legacy apps: {len(legacy_apps)}")

    def check_financials(self):
        """Validate financial tracking files."""
        print("\n=== Financial Health Check ===\n")

        required_files = [
            "REVENUE_TRACKER.csv",
            "EXPENSE_TRACKER.csv",
            "P_AND_L_MONTHLY.csv",
            "INVESTMENT_PORTFOLIO.csv",
            "TAX_DEDUCTIONS_2026.csv",
        ]

        for filename in required_files:
            filepath = FINANCIALS_DIR / filename
            if not filepath.exists():
                self.add_issue("ERROR", f"FINANCIALS/{filename}", "File missing")
            else:
                valid, msg = self.check_csv_validity(filepath)
                if valid:
                    self.add_issue("PASS", f"FINANCIALS/{filename}", msg)
                else:
                    self.add_issue("ERROR", f"FINANCIALS/{filename}", msg)

    def check_data_freshness(self):
        """Check if key files are stale."""
        print("\n=== Data Freshness Check ===\n")

        stale_threshold = datetime.now() - timedelta(days=7)

        critical_files = [
            LEDGER_DIR / "ALPHA_STAGING.csv",
            LEDGER_DIR / "HIGH_SIGNAL_SOURCES.csv",
            PROJECT_DIR / "OPS" / "SESSION_HANDOFF.md",
            PROJECT_DIR / "ralph" / "loops" / "mega" / ".ralph" / "progress.md",
        ]

        for filepath in critical_files:
            if not filepath.exists():
                self.add_issue("WARNING", "FRESHNESS", f"Missing: {filepath.name}")
                continue

            mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
            age_days = (datetime.now() - mtime).days

            if mtime < stale_threshold:
                self.add_issue("WARNING", "FRESHNESS",
                             f"{filepath.name} is {age_days} days old")
            else:
                self.add_issue("PASS", "FRESHNESS",
                             f"{filepath.name} updated {age_days} day(s) ago")

    def print_report(self):
        """Print the health check report."""
        print("\n" + "=" * 70)
        print("   PRINTMAXX SYSTEM HEALTH REPORT")
        print(f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

        if self.issues:
            print(f"\n  ERRORS ({len(self.issues)}):")
            for issue in self.issues:
                print(f"    [ERROR] {issue['component']}: {issue['message']}")

        if self.warnings:
            print(f"\n  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"    [WARN]  {warning['component']}: {warning['message']}")

        print(f"\n  PASSES ({len(self.passes)}):")
        for p in self.passes:
            print(f"    [OK]    {p['component']}: {p['message']}")

        print(f"\n  Summary: {len(self.issues)} errors, {len(self.warnings)} warnings, {len(self.passes)} passes")

        # Overall status
        if self.issues:
            print("\n  STATUS: NEEDS ATTENTION - Fix errors before proceeding")
        elif self.warnings:
            print("\n  STATUS: MOSTLY HEALTHY - Review warnings")
        else:
            print("\n  STATUS: ALL GREEN")

        print("=" * 70)

    def save_report(self, filepath: Path):
        """Save report to file."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "errors": self.issues,
            "warnings": self.warnings,
            "passes": self.passes,
            "summary": {
                "error_count": len(self.issues),
                "warning_count": len(self.warnings),
                "pass_count": len(self.passes),
                "status": "ERROR" if self.issues else "WARNING" if self.warnings else "HEALTHY"
            }
        }
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved to {filepath}")


def main():
    parser = argparse.ArgumentParser(description='PRINTMAXX System Health Check')
    parser.add_argument('--ledger', action='store_true', help='Check LEDGER files only')
    parser.add_argument('--ralph', action='store_true', help='Check ralph loops only')
    parser.add_argument('--apps', action='store_true', help='Check app builds only')
    parser.add_argument('--financials', action='store_true', help='Check financial files only')
    parser.add_argument('--freshness', action='store_true', help='Check data freshness only')
    parser.add_argument('--save', help='Save report to file')

    args = parser.parse_args()

    checker = HealthChecker()

    # If no specific flag, run all checks
    run_all = not any([args.ledger, args.ralph, args.apps, args.financials, args.freshness])

    if args.ledger or run_all:
        checker.check_ledger()
    if args.ralph or run_all:
        checker.check_ralph()
    if args.apps or run_all:
        checker.check_apps()
    if args.financials or run_all:
        checker.check_financials()
    if args.freshness or run_all:
        checker.check_data_freshness()

    checker.print_report()

    if args.save:
        checker.save_report(Path(args.save))


if __name__ == "__main__":
    main()
