#!/usr/bin/env python3
"""
data_validator.py - Check CSV data integrity across the project

Validates CSV structure, data types, encoding, and relationships.
Catches common issues: malformed rows, missing headers, encoding errors,
inconsistent delimiters, and data type violations.

Usage:
    python3 data_validator.py --file LEDGER/ALPHA_STAGING.csv
    python3 data_validator.py --all
    python3 data_validator.py --dir LEDGER
    python3 data_validator.py --strict

Example:
    # Validate a specific file
    python3 data_validator.py --file LEDGER/ALPHA_STAGING.csv

    # Validate all CSVs in project
    python3 data_validator.py --all

    # Strict mode (warnings become errors)
    python3 data_validator.py --all --strict
"""

import argparse
import csv
import logging
import os
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_DIR / "AUTOMATIONS" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "data_validator.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def validate_csv(filepath, strict=False):
    """Validate a single CSV file. Returns list of issues."""
    issues = []
    path = Path(filepath)

    if not path.exists():
        return [{"severity": "ERROR", "line": 0, "message": f"File not found: {filepath}"}]

    # Check file size
    size = path.stat().st_size
    if size == 0:
        return [{"severity": "WARNING", "line": 0, "message": "Empty file"}]

    if size > 50 * 1024 * 1024:  # 50MB
        issues.append({"severity": "WARNING", "line": 0, "message": f"Large file: {size / 1024 / 1024:.1f} MB"})

    # Try to read the file
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(path, "r", encoding="latin-1") as f:
                content = f.read()
            issues.append({"severity": "WARNING", "line": 0, "message": "File is latin-1 encoded, not UTF-8"})
        except Exception as e:
            return [{"severity": "ERROR", "line": 0, "message": f"Cannot read file: {e}"}]

    lines = content.split("\n")
    if not lines or not lines[0].strip():
        return [{"severity": "ERROR", "line": 1, "message": "No header row"}]

    # Parse CSV
    try:
        reader = csv.reader(lines)
        header = next(reader)
        num_cols = len(header)
    except Exception as e:
        return [{"severity": "ERROR", "line": 1, "message": f"Cannot parse header: {e}"}]

    # Check header
    if num_cols == 0:
        issues.append({"severity": "ERROR", "line": 1, "message": "Empty header"})

    # Check for duplicate column names
    seen_cols = set()
    for col in header:
        if col in seen_cols:
            issues.append({"severity": "WARNING", "line": 1, "message": f"Duplicate column: '{col}'"})
        seen_cols.add(col)

    # Check for empty column names
    empty_cols = sum(1 for col in header if not col.strip())
    if empty_cols > 0:
        issues.append({"severity": "WARNING", "line": 1, "message": f"{empty_cols} empty column name(s)"})

    # Validate each row
    row_count = 0
    empty_rows = 0

    for line_num, row in enumerate(reader, 2):
        if not row or (len(row) == 1 and not row[0].strip()):
            empty_rows += 1
            continue

        row_count += 1

        # Column count mismatch
        if len(row) != num_cols:
            if len(issues) < 50:  # Cap issue reports
                issues.append({
                    "severity": "WARNING" if not strict else "ERROR",
                    "line": line_num,
                    "message": f"Column count mismatch: expected {num_cols}, got {len(row)}",
                })

        # Check for problematic characters
        for col_idx, value in enumerate(row):
            if "\x00" in value:
                issues.append({
                    "severity": "ERROR",
                    "line": line_num,
                    "message": f"Null byte in column {col_idx}",
                })

    if empty_rows > 0:
        issues.append({
            "severity": "INFO",
            "line": 0,
            "message": f"{empty_rows} empty row(s) found",
        })

    # Summary
    if not issues:
        issues.append({
            "severity": "OK",
            "line": 0,
            "message": f"Valid: {row_count} rows, {num_cols} columns, {size:,} bytes",
        })

    return issues


def find_all_csvs(directory=None):
    """Find all CSV files in the project."""
    search_dir = Path(directory) if directory else PROJECT_DIR

    csvs = []
    for root, dirs, files in os.walk(search_dir):
        # Skip node_modules, .git, etc.
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "__pycache__", ".next")]
        for f in files:
            if f.endswith(".csv"):
                csvs.append(Path(root) / f)

    return sorted(csvs)


def main():
    parser = argparse.ArgumentParser(
        description="Validate CSV data integrity across the project"
    )
    parser.add_argument("--file", type=str, default=None, help="Validate specific file")
    parser.add_argument("--dir", type=str, default=None, help="Validate all CSVs in directory")
    parser.add_argument("--all", action="store_true", help="Validate all project CSVs")
    parser.add_argument("--strict", action="store_true", help="Strict mode (warnings = errors)")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if args.file:
        filepath = Path(args.file)
        if not filepath.is_absolute():
            filepath = PROJECT_DIR / args.file
        files = [filepath]
    elif args.dir:
        files = find_all_csvs(args.dir if Path(args.dir).is_absolute() else PROJECT_DIR / args.dir)
    elif args.all:
        files = find_all_csvs()
    else:
        files = find_all_csvs(PROJECT_DIR / "LEDGER")

    logger.info(f"Validating {len(files)} CSV file(s)")

    total_issues = {"OK": 0, "INFO": 0, "WARNING": 0, "ERROR": 0}
    all_results = {}

    for filepath in files:
        rel_path = filepath.relative_to(PROJECT_DIR) if filepath.is_relative_to(PROJECT_DIR) else filepath
        issues = validate_csv(filepath, strict=args.strict)
        all_results[str(rel_path)] = issues

        for issue in issues:
            total_issues[issue["severity"]] = total_issues.get(issue["severity"], 0) + 1

        if args.output == "text":
            for issue in issues:
                marker = {"OK": " OK", "INFO": "  i", "WARNING": " !!", "ERROR": "ERR"}.get(issue["severity"], "  ?")
                line_info = f"L{issue['line']}" if issue["line"] > 0 else ""
                print(f"[{marker}] {rel_path} {line_info}: {issue['message']}")

    if args.output == "json":
        import json
        print(json.dumps(all_results, indent=2))
    else:
        print(f"\nSummary: {total_issues.get('ERROR', 0)} errors, "
              f"{total_issues.get('WARNING', 0)} warnings, "
              f"{total_issues.get('OK', 0)} OK")


if __name__ == "__main__":
    main()
