#!/usr/bin/env python3
"""
PRINTMAXX Validation Script

Validates:
1. CSV files have headers and proper structure
2. Markdown files have no broken internal links
3. Copy-style violations (em dashes, banned words)
4. Missing required files per app

Usage:
    python scripts/validate.py              # Run all validations
    python scripts/validate.py --csv-only   # CSV validation only
    python scripts/validate.py --copy-only  # Copy style only
    python scripts/validate.py --links-only # Link validation only
    python scripts/validate.py --apps-only  # App file validation only
"""

import os
import sys
import csv
import re
import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Set

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Banned AI vocabulary from copy-style.md
BANNED_WORDS = [
    "additionally", "moreover", "furthermore",
    "testament", "landscape", "paradigm",
    "leverage", "utilize", "delve", "dive into", "unpack",
    "comprehensive", "robust", "streamlined",
    "game-changer", "unlock", "elevate",
    "cutting-edge", "innovative", "revolutionary",
    "empower", "enable", "foster",
    "seamless", "frictionless",
    "journey"  # unless actual travel
]

# Em dash pattern
EM_DASH_PATTERN = re.compile(r'—')

# "It's not just X, it's Y" pattern
NOT_JUST_PATTERN = re.compile(r"it'?s not just .+, it'?s", re.IGNORECASE)

# Required files for each app
APP_REQUIRED_FILES = [
    "README.md",
    "package.json",
]

class ValidationResult:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.passed: int = 0
        self.failed: int = 0

    def add_error(self, msg: str):
        self.errors.append(msg)
        self.failed += 1

    def add_warning(self, msg: str):
        self.warnings.append(msg)

    def add_pass(self):
        self.passed += 1

    def print_summary(self, title: str):
        print(f"\n=== {title} ===")
        print(f"Passed: {self.passed} | Failed: {self.failed} | Warnings: {len(self.warnings)}")

        if self.errors:
            print("\nERRORS:")
            for err in self.errors[:20]:  # Limit to 20
                print(f"  - {err}")
            if len(self.errors) > 20:
                print(f"  ... and {len(self.errors) - 20} more errors")

        if self.warnings:
            print("\nWARNINGS:")
            for warn in self.warnings[:10]:  # Limit to 10
                print(f"  - {warn}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more warnings")


def validate_csv_files() -> ValidationResult:
    """Validate all CSV files in LEDGER have headers and proper structure."""
    result = ValidationResult()
    ledger_dir = PROJECT_ROOT / "LEDGER"

    if not ledger_dir.exists():
        result.add_error("LEDGER directory not found")
        return result

    csv_files = list(ledger_dir.glob("*.csv"))

    if not csv_files:
        result.add_warning("No CSV files found in LEDGER")
        return result

    for csv_file in csv_files:
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                # Check if file is empty
                content = f.read().strip()
                if not content:
                    result.add_error(f"{csv_file.name}: Empty file")
                    continue

                # Reset and parse as CSV
                f.seek(0)
                reader = csv.reader(f)
                rows = list(reader)

                if len(rows) == 0:
                    result.add_error(f"{csv_file.name}: No rows found")
                    continue

                # Check header exists (first row should have content)
                header = rows[0]
                if not header or all(cell.strip() == '' for cell in header):
                    result.add_error(f"{csv_file.name}: Missing or empty header row")
                    continue

                # Check for consistent column count
                header_len = len(header)
                for i, row in enumerate(rows[1:], start=2):
                    if len(row) != header_len and len(row) > 0:
                        result.add_warning(f"{csv_file.name}:{i}: Column count mismatch (expected {header_len}, got {len(row)})")

                result.add_pass()

        except Exception as e:
            result.add_error(f"{csv_file.name}: Failed to parse - {str(e)}")

    return result


def validate_markdown_links() -> ValidationResult:
    """Validate internal links in markdown files."""
    result = ValidationResult()

    # Find all markdown files
    md_files = list(PROJECT_ROOT.glob("**/*.md"))

    # Build set of existing files for link validation
    existing_files: Set[str] = set()
    for f in PROJECT_ROOT.glob("**/*"):
        if f.is_file():
            # Store relative paths
            rel_path = str(f.relative_to(PROJECT_ROOT))
            existing_files.add(rel_path)
            # Also store without extension for flexibility
            existing_files.add(rel_path.rsplit('.', 1)[0] if '.' in rel_path else rel_path)

    # Internal link pattern: [text](path) where path doesn't start with http
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            links = link_pattern.findall(content)
            file_dir = md_file.parent

            for text, link in links:
                # Skip external links
                if link.startswith(('http://', 'https://', 'mailto:', '#')):
                    continue

                # Skip anchor-only links
                if link.startswith('#'):
                    continue

                # Handle relative links
                link_path = link.split('#')[0]  # Remove anchors
                if not link_path:
                    continue

                # Try to resolve the link
                if link_path.startswith('/'):
                    # Absolute from project root
                    target = PROJECT_ROOT / link_path.lstrip('/')
                else:
                    # Relative to current file
                    target = file_dir / link_path

                # Check if target exists
                if not target.exists():
                    # Also check without extension
                    if not (target.with_suffix('.md')).exists():
                        rel_file = md_file.relative_to(PROJECT_ROOT)
                        result.add_warning(f"{rel_file}: Broken link [{text}]({link})")

            result.add_pass()

        except Exception as e:
            result.add_error(f"{md_file.name}: Failed to validate - {str(e)}")

    return result


def validate_copy_style() -> ValidationResult:
    """Validate copy style in content files."""
    result = ValidationResult()

    # Check content directories
    content_dirs = [
        PROJECT_ROOT / "CONTENT",
        PROJECT_ROOT / "MONEY_METHODS",
    ]

    md_files = []
    for content_dir in content_dirs:
        if content_dir.exists():
            md_files.extend(content_dir.glob("**/*.md"))

    # Also check email sequences and social content
    for pattern in ["**/*email*.md", "**/*post*.md", "**/*thread*.md"]:
        md_files.extend(PROJECT_ROOT.glob(pattern))

    # Deduplicate
    md_files = list(set(md_files))

    violations: Dict[str, List[str]] = {}

    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            file_violations = []
            rel_path = str(md_file.relative_to(PROJECT_ROOT))

            # Check for em dashes
            em_dashes = EM_DASH_PATTERN.findall(content)
            if em_dashes:
                file_violations.append(f"Em dash found ({len(em_dashes)} occurrences)")

            # Check for banned words (case insensitive)
            content_lower = content.lower()
            for word in BANNED_WORDS:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(word.lower()) + r'\b'
                matches = re.findall(pattern, content_lower)
                if matches:
                    file_violations.append(f"Banned word '{word}' ({len(matches)}x)")

            # Check for "It's not just X, it's Y" pattern
            not_just = NOT_JUST_PATTERN.findall(content)
            if not_just:
                file_violations.append(f"'It's not just X, it's Y' pattern found")

            if file_violations:
                violations[rel_path] = file_violations
                result.add_error(f"{rel_path}: {', '.join(file_violations)}")
            else:
                result.add_pass()

        except Exception as e:
            result.add_warning(f"{md_file.name}: Could not validate - {str(e)}")

    return result


def validate_app_files() -> ValidationResult:
    """Validate required files exist for each app."""
    result = ValidationResult()

    apps_dir = PROJECT_ROOT / "MONEY_METHODS" / "APP_FACTORY" / "builds"

    if not apps_dir.exists():
        result.add_warning("APP_FACTORY/builds directory not found")
        return result

    apps = [d for d in apps_dir.iterdir() if d.is_dir()]

    if not apps:
        result.add_warning("No apps found in builds/")
        return result

    for app_dir in apps:
        app_name = app_dir.name
        missing = []

        for required_file in APP_REQUIRED_FILES:
            if not (app_dir / required_file).exists():
                missing.append(required_file)

        if missing:
            result.add_error(f"{app_name}: Missing required files: {', '.join(missing)}")
        else:
            result.add_pass()

    return result


def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Validation Script")
    parser.add_argument("--csv-only", action="store_true", help="Validate CSV files only")
    parser.add_argument("--copy-only", action="store_true", help="Validate copy style only")
    parser.add_argument("--links-only", action="store_true", help="Validate links only")
    parser.add_argument("--apps-only", action="store_true", help="Validate app files only")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    # If no specific flag, run all
    run_all = not (args.csv_only or args.copy_only or args.links_only or args.apps_only)

    total_errors = 0
    total_warnings = 0

    print("=" * 50)
    print("PRINTMAXX VALIDATION")
    print("=" * 50)

    if run_all or args.csv_only:
        result = validate_csv_files()
        result.print_summary("CSV Validation")
        total_errors += result.failed
        total_warnings += len(result.warnings)

    if run_all or args.links_only:
        result = validate_markdown_links()
        result.print_summary("Link Validation")
        total_errors += result.failed
        total_warnings += len(result.warnings)

    if run_all or args.copy_only:
        result = validate_copy_style()
        result.print_summary("Copy Style Validation")
        total_errors += result.failed
        total_warnings += len(result.warnings)

    if run_all or args.apps_only:
        result = validate_app_files()
        result.print_summary("App Files Validation")
        total_errors += result.failed
        total_warnings += len(result.warnings)

    print("\n" + "=" * 50)
    print(f"TOTAL: {total_errors} errors, {total_warnings} warnings")
    print("=" * 50)

    # Exit with error code if there are errors
    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
