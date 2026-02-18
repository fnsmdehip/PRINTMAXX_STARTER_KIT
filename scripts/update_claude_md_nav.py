#!/usr/bin/env python3
"""
CLAUDE.md Navigation Auto-Updater

Scans the project filesystem and compares against what's listed in CLAUDE.md.
Reports gaps (files that exist but aren't in CLAUDE.md navigation tables).
Optionally auto-appends new entries to the navigation tables.

Usage:
    python3 scripts/update_claude_md_nav.py --scan          # Report only
    python3 scripts/update_claude_md_nav.py --update        # Report + update CLAUDE.md
    python3 scripts/update_claude_md_nav.py --scan --verbose # Detailed output

No external dependencies. Pure stdlib Python.
"""

import os
import re
import sys
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Project root (two levels up from this script, or use env)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CLAUDE_MD_PATH = PROJECT_ROOT / ".claude" / "CLAUDE.md"

# Directories to exclude from scanning
EXCLUDE_DIRS = {
    "node_modules", ".git", "__pycache__", ".next", ".cache",
    "dist", "build", ".swarm", ".DS_Store", "venv", "env",
}

# File extensions we care about per directory
SCAN_CONFIG = {
    "MONEY_METHODS": {
        "extensions": {".md", ".py", ".csv"},
        "max_depth": 3,
        "description": "Money method playbooks and builds",
        "nav_category": "money_methods",
    },
    "ralph/loops": {
        "extensions": {".md", ".py", ".csv", ".html", ".json"},
        "max_depth": 4,
        "description": "Ralph loop outputs",
        "nav_category": "ralph_outputs",
        "focus_subdirs": ["output"],
    },
    "AUTOMATIONS": {
        "extensions": {".py"},
        "max_depth": 1,
        "description": "Automation scripts",
        "nav_category": "automations",
    },
    "AUTOMATIONS/content_posting": {
        "extensions": {".csv", ".md"},
        "max_depth": 1,
        "description": "Content posting assets",
        "nav_category": "content_posting",
    },
    "OPS": {
        "extensions": {".md"},
        "max_depth": 1,
        "description": "Operational docs",
        "nav_category": "ops_docs",
    },
    "LEDGER": {
        "extensions": {".csv"},
        "max_depth": 1,
        "description": "Tracking files",
        "nav_category": "ledger",
    },
    "PRODUCTS": {
        "extensions": {".md"},
        "max_depth": 1,
        "description": "Product listings",
        "nav_category": "products",
    },
    "CONTENT/social": {
        "extensions": {".md", ".csv"},
        "max_depth": 2,
        "description": "Social content",
        "nav_category": "social_content",
    },
    "scripts": {
        "extensions": {".py"},
        "max_depth": 2,
        "description": "Utility scripts",
        "nav_category": "scripts",
    },
    "FINANCIALS": {
        "extensions": {".csv", ".md"},
        "max_depth": 1,
        "description": "Financial tracking",
        "nav_category": "financials",
    },
    "builds": {
        "extensions": {".md", ".html", ".py"},
        "max_depth": 3,
        "description": "Build outputs",
        "nav_category": "builds",
    },
    "DIGITAL_PRODUCTS": {
        "extensions": {".md", ".csv", ".pdf"},
        "max_depth": 2,
        "description": "Digital product listings",
        "nav_category": "digital_products",
    },
}


def should_exclude(path_parts):
    """Check if any path component is in the exclude list."""
    for part in path_parts:
        if part in EXCLUDE_DIRS:
            return True
        if part.startswith(".") and part not in {".claude", ".ralph"}:
            return True
    return False


def scan_directory(base_dir, config):
    """Scan a directory for files matching the config criteria."""
    found_files = []
    full_base = PROJECT_ROOT / base_dir

    if not full_base.exists():
        return found_files

    extensions = config["extensions"]
    max_depth = config["max_depth"]
    focus_subdirs = config.get("focus_subdirs", None)

    for root, dirs, files in os.walk(full_base):
        root_path = Path(root)
        rel_root = root_path.relative_to(PROJECT_ROOT)
        depth = len(rel_root.parts) - len(Path(base_dir).parts)

        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not (d.startswith(".") and d not in {".ralph"})]

        if depth > max_depth:
            dirs.clear()
            continue

        # If focus_subdirs is set, only collect files from paths
        # that include one of the focus subdir names at any depth.
        # (e.g., focus_subdirs=["output"] means only scan inside */output/ dirs)
        if focus_subdirs:
            rel_parts = rel_root.relative_to(base_dir).parts if str(rel_root) != base_dir else ()
            in_focus = any(part in focus_subdirs for part in rel_parts)
            # At depth 0, allow traversal into all dirs (loop names)
            # At depth 1+, only keep dirs in focus_subdirs or already inside one
            if depth >= 1 and not in_focus:
                # Only keep dirs that are in focus_subdirs
                dirs[:] = [d for d in dirs if d in focus_subdirs]
                continue  # Don't collect files from non-focus dirs

        for f in sorted(files):
            fpath = Path(f)
            if fpath.suffix in extensions:
                rel_file = str(rel_root / f)
                found_files.append(rel_file)

    return found_files


def extract_paths_from_claude_md():
    """Extract all file paths mentioned in CLAUDE.md."""
    if not CLAUDE_MD_PATH.exists():
        print(f"ERROR: {CLAUDE_MD_PATH} not found")
        sys.exit(1)

    content = CLAUDE_MD_PATH.read_text(encoding="utf-8")
    paths = set()

    # Match backtick-wrapped paths like `MONEY_METHODS/ECOM/VIRAL_PRODUCT_ARB_PLAYBOOK.md`
    backtick_pattern = re.compile(r"`([A-Za-z0-9_./-]+\.[a-zA-Z]{1,5})`")
    for match in backtick_pattern.finditer(content):
        p = match.group(1)
        # Filter out things that are clearly not file paths
        if "/" in p or p.endswith((".md", ".csv", ".py", ".json", ".html", ".xlsx", ".sh", ".ts", ".tsx", ".js", ".jsonl")):
            # Normalize: strip leading ./ if present
            p = p.lstrip("./")
            paths.add(p)

    # Match backtick-wrapped directories like `MONEY_METHODS/ECOM/`
    dir_pattern = re.compile(r"`([A-Za-z0-9_/-]+/)`")
    for match in dir_pattern.finditer(content):
        p = match.group(1).rstrip("/")
        paths.add(p + "/")

    # Also match backtick paths without extensions (directories)
    dir_pattern2 = re.compile(r"`([A-Za-z0-9_./-]+)`")
    for match in dir_pattern2.finditer(content):
        p = match.group(1)
        if "/" in p and not any(p.endswith(ext) for ext in [".md", ".csv", ".py", ".json", ".html", ".xlsx", ".sh", ".ts", ".tsx", ".js", ".jsonl"]):
            paths.add(p.rstrip("/") + "/")

    return paths


def normalize_path(p):
    """Normalize a path for comparison."""
    p = p.strip().lstrip("./")
    return p


def is_path_covered(file_path, known_paths):
    """Check if a file path is covered by any known path (exact or directory match)."""
    normalized = normalize_path(file_path)

    # Exact match
    if normalized in known_paths:
        return True

    # Check if any known directory path covers this file
    for kp in known_paths:
        kp_clean = kp.rstrip("/")
        if normalized.startswith(kp_clean + "/"):
            return True
        # Also check if the file's directory is mentioned
        file_dir = str(Path(normalized).parent)
        if kp_clean == file_dir or kp_clean + "/" == file_dir + "/":
            return True

    return False


def categorize_gap(file_path):
    """Categorize a gap file for the report."""
    parts = Path(file_path).parts
    if parts[0] == "MONEY_METHODS":
        method = parts[1] if len(parts) > 1 else "ROOT"
        return f"MONEY_METHODS/{method}"
    elif parts[0] == "ralph":
        if len(parts) > 2:
            return f"ralph/loops/{parts[2]}"
        return "ralph"
    elif parts[0] == "AUTOMATIONS":
        return "AUTOMATIONS"
    elif parts[0] == "OPS":
        return "OPS"
    elif parts[0] == "LEDGER":
        return "LEDGER"
    elif parts[0] == "scripts":
        return "scripts"
    elif parts[0] == "PRODUCTS":
        return "PRODUCTS"
    elif parts[0] == "CONTENT":
        return "CONTENT"
    elif parts[0] == "FINANCIALS":
        return "FINANCIALS"
    elif parts[0] == "builds":
        return "builds"
    elif parts[0] == "DIGITAL_PRODUCTS":
        return "DIGITAL_PRODUCTS"
    return parts[0]


def generate_nav_entries(gaps_by_category):
    """Generate CLAUDE.md-formatted navigation entries for gaps."""
    entries_where = []
    entries_want = []

    for category, files in sorted(gaps_by_category.items()):
        if not files:
            continue

        # Generate "Where is..." entries for significant files
        for f in sorted(files):
            name = Path(f).stem.replace("_", " ").title()
            ext = Path(f).suffix

            # Skip minor/generated files
            if any(skip in f.lower() for skip in ["backup", "temp", "deprecated", "old_"]):
                continue

            if ext == ".md":
                entries_where.append(f'| **{name}** | `{f}` |')
            elif ext == ".py":
                entries_where.append(f'| **{name} script** | `{f}` |')
            elif ext == ".csv":
                entries_where.append(f'| **{name} data** | `{f}` |')
            elif ext == ".html":
                entries_where.append(f'| **{name} app** | `{f}` |')

    return entries_where, entries_want


def build_update_block(gaps_by_category, total_gaps):
    """Build the text block to append to CLAUDE.md."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = []
    lines.append("")
    lines.append(f"### Auto-Discovered Files ({timestamp}) - {total_gaps} new entries")
    lines.append("")
    lines.append("| Category | File | Type |")
    lines.append("|----------|------|------|")

    for category, files in sorted(gaps_by_category.items()):
        for f in sorted(files):
            ext = Path(f).suffix.lstrip(".")
            lines.append(f"| {category} | `{f}` | {ext} |")

    lines.append("")
    return "\n".join(lines)


def update_claude_md(gaps_by_category, total_gaps):
    """Insert auto-discovered entries into CLAUDE.md after the 'Where is...' table."""
    content = CLAUDE_MD_PATH.read_text(encoding="utf-8")

    update_block = build_update_block(gaps_by_category, total_gaps)

    # Find the end of the "Where is..." table section
    # Look for the line with the last entry before "### "I want to..."
    marker = '### "I want to..." (task router)'
    idx = content.find(marker)

    if idx == -1:
        # Fallback: append before "### Cross-reference checklist"
        marker = "### Cross-reference checklist"
        idx = content.find(marker)

    if idx == -1:
        # Last fallback: append at end
        content += "\n" + update_block
    else:
        content = content[:idx] + update_block + "\n" + content[idx:]

    CLAUDE_MD_PATH.write_text(content, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Scan project and find files missing from CLAUDE.md navigation"
    )
    parser.add_argument(
        "--scan", action="store_true",
        help="Report-only mode: show gaps without modifying CLAUDE.md"
    )
    parser.add_argument(
        "--update", action="store_true",
        help="Update mode: append missing entries to CLAUDE.md"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show all scanned files, not just gaps"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output gaps as JSON for integration with other tools"
    )

    args = parser.parse_args()

    if not args.scan and not args.update:
        parser.print_help()
        print("\nUse --scan for report only, or --update to modify CLAUDE.md")
        sys.exit(1)

    print("=" * 70)
    print("CLAUDE.md Navigation Scanner")
    print(f"Project: {PROJECT_ROOT}")
    print(f"CLAUDE.md: {CLAUDE_MD_PATH}")
    print("=" * 70)

    # Step 1: Extract all paths mentioned in CLAUDE.md
    print("\n[1/3] Extracting paths from CLAUDE.md...")
    known_paths = extract_paths_from_claude_md()
    print(f"  Found {len(known_paths)} referenced paths in CLAUDE.md")

    # Step 2: Scan filesystem
    print("\n[2/3] Scanning project filesystem...")
    all_found = {}
    total_files = 0
    for scan_dir, config in SCAN_CONFIG.items():
        files = scan_directory(scan_dir, config)
        all_found[scan_dir] = files
        total_files += len(files)
        if args.verbose:
            print(f"  {scan_dir}: {len(files)} files")

    print(f"  Scanned {len(SCAN_CONFIG)} directories, found {total_files} files")

    # Step 3: Find gaps
    print("\n[3/3] Finding gaps...")
    gaps_by_category = defaultdict(list)
    total_gaps = 0
    covered = 0

    for scan_dir, files in all_found.items():
        for f in files:
            if is_path_covered(f, known_paths):
                covered += 1
            else:
                category = categorize_gap(f)
                gaps_by_category[category].append(f)
                total_gaps += 1

    # Report
    print("\n" + "=" * 70)
    print(f"RESULTS: {total_gaps} files NOT in CLAUDE.md  |  {covered} files already covered")
    print("=" * 70)

    if total_gaps == 0:
        print("\nAll project files are accounted for in CLAUDE.md navigation. No gaps found.")
        return

    # Print gaps by category
    for category in sorted(gaps_by_category.keys()):
        files = gaps_by_category[category]
        print(f"\n  [{category}] ({len(files)} missing)")
        for f in sorted(files):
            print(f"    - {f}")

    # Summary stats
    print(f"\n{'=' * 70}")
    print("SUMMARY BY CATEGORY:")
    print(f"{'=' * 70}")
    for category in sorted(gaps_by_category.keys()):
        count = len(gaps_by_category[category])
        bar = "#" * min(count, 40)
        print(f"  {category:40s} {count:4d}  {bar}")
    print(f"  {'TOTAL':40s} {total_gaps:4d}")

    # JSON output
    if args.json:
        import json
        output = {
            "timestamp": datetime.now().isoformat(),
            "total_gaps": total_gaps,
            "total_covered": covered,
            "gaps_by_category": dict(gaps_by_category),
        }
        print("\n--- JSON OUTPUT ---")
        print(json.dumps(output, indent=2))

    # Update CLAUDE.md if requested
    if args.update:
        print(f"\nUpdating CLAUDE.md with {total_gaps} new entries...")
        success = update_claude_md(gaps_by_category, total_gaps)
        if success:
            print("CLAUDE.md updated successfully.")
            print(f"New entries added before the 'I want to...' table.")
        else:
            print("ERROR: Failed to update CLAUDE.md")
            sys.exit(1)
    else:
        print(f"\nRun with --update to add these {total_gaps} entries to CLAUDE.md")
        print(f"  python3 scripts/update_claude_md_nav.py --update")


if __name__ == "__main__":
    main()
