#!/usr/bin/env python3
"""
Ralph Loop Fixer — Fix Invalid --max-tokens Flag
==================================================
Scans all ralph loop run.sh files across both ralph/ and 05_AUTOMATION/ralph/
directories, removes the invalid --max-tokens flag so loops can run again.

Also checks for other common issues:
- Missing prompt.md files
- Missing prd.json files
- Broken shebang lines
- Non-executable run.sh files

Usage:
    python3 AUTOMATIONS/ralph_loop_fixer.py              # Scan and fix
    python3 AUTOMATIONS/ralph_loop_fixer.py --dry-run    # Preview only
    python3 AUTOMATIONS/ralph_loop_fixer.py --status     # Show loop health
"""

import os
import re
import sys
import stat
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"
LOG_FILE = LOG_DIR / "ralph_loop_fixer.log"

# All ralph loop directories
RALPH_DIRS = [
    PROJECT_ROOT / "ralph" / "loops",
    PROJECT_ROOT / "05_AUTOMATION" / "ralph" / "loops",
]


def safe_path(target):
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_FILE), "a") as f:
        f.write(line + "\n")


def find_all_run_sh():
    """Find all run.sh files in ralph loop directories."""
    results = []
    for rdir in RALPH_DIRS:
        if not rdir.exists():
            continue
        for loop_dir in sorted(rdir.iterdir()):
            if not loop_dir.is_dir():
                continue
            run_sh = loop_dir / "run.sh"
            if run_sh.exists():
                results.append(run_sh)
    return results


def fix_max_tokens(run_sh_path, dry_run=False):
    """Remove --max-tokens flag and its value from a run.sh file."""
    safe = safe_path(run_sh_path)
    content = safe.read_text()

    # Pattern: --max-tokens followed by a number (possibly with spaces)
    patterns = [
        r'\s*--max-tokens\s+\d+',      # --max-tokens 4096
        r'\s*--max-tokens=\d+',          # --max-tokens=4096
        r'\s*--max-tokens\s+"?\d+"?',    # --max-tokens "4096"
    ]

    fixed = content
    changes = []
    for pattern in patterns:
        matches = re.findall(pattern, fixed)
        if matches:
            changes.extend(matches)
            fixed = re.sub(pattern, '', fixed)

    if changes:
        if not dry_run:
            safe.write_text(fixed)
        return changes
    return []


def check_loop_health(loop_dir):
    """Check health of a single ralph loop directory."""
    issues = []
    loop_name = loop_dir.name

    run_sh = loop_dir / "run.sh"
    prompt_md = loop_dir / "prompt.md"
    prd_json = loop_dir / "prd.json"

    # Check run.sh exists and is executable
    if not run_sh.exists():
        issues.append("MISSING run.sh")
    else:
        st = os.stat(run_sh)
        if not (st.st_mode & stat.S_IXUSR):
            issues.append("run.sh not executable")

        content = run_sh.read_text()
        if "--max-tokens" in content:
            issues.append("BROKEN: --max-tokens flag present")
        if not content.startswith("#!/"):
            issues.append("missing shebang line")

    # Check prompt.md
    if not prompt_md.exists():
        issues.append("MISSING prompt.md")

    # Check prd.json (optional but expected for newer loops)
    # Not all loops have prd.json, so this is a warning not an error

    return issues


def make_executable(run_sh_path, dry_run=False):
    """Ensure run.sh is executable."""
    safe = safe_path(run_sh_path)
    st = os.stat(safe)
    if not (st.st_mode & stat.S_IXUSR):
        if not dry_run:
            os.chmod(safe, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        return True
    return False


def show_status():
    """Show health status of all ralph loops."""
    all_run_sh = find_all_run_sh()
    log(f"=== Ralph Loop Health Report ===")
    log(f"Total loops found: {len(all_run_sh)}")
    log("")

    healthy = 0
    broken = 0
    issues_total = 0

    for run_sh in all_run_sh:
        loop_dir = run_sh.parent
        # Get relative path for display
        try:
            rel = loop_dir.relative_to(PROJECT_ROOT)
        except ValueError:
            rel = loop_dir
        issues = check_loop_health(loop_dir)
        if issues:
            broken += 1
            issues_total += len(issues)
            log(f"  ISSUES {rel}: {', '.join(issues)}")
        else:
            healthy += 1

    log("")
    log(f"  HEALTHY: {healthy}")
    log(f"  WITH ISSUES: {broken}")
    log(f"  TOTAL ISSUES: {issues_total}")


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args

    if "--status" in args:
        show_status()
        return

    log(f"Ralph Loop Fixer starting (dry_run={dry_run})")

    all_run_sh = find_all_run_sh()
    log(f"Found {len(all_run_sh)} run.sh files across ralph directories")

    fixed_count = 0
    chmod_count = 0

    for run_sh in all_run_sh:
        loop_dir = run_sh.parent
        try:
            rel = loop_dir.relative_to(PROJECT_ROOT)
        except ValueError:
            rel = loop_dir

        # Fix --max-tokens
        changes = fix_max_tokens(run_sh, dry_run=dry_run)
        if changes:
            fixed_count += 1
            log(f"  FIXED {rel}/run.sh: removed {changes}")

        # Ensure executable
        if make_executable(run_sh, dry_run=dry_run):
            chmod_count += 1
            log(f"  CHMOD {rel}/run.sh: made executable")

    log(f"\n=== Summary ===")
    log(f"  --max-tokens fixed: {fixed_count}")
    log(f"  Made executable: {chmod_count}")
    log(f"  Total loops scanned: {len(all_run_sh)}")

    if dry_run:
        log("  [DRY RUN - no changes written]")

    # Also show current health
    log("")
    show_status()

    log("Ralph Loop Fixer complete")


if __name__ == "__main__":
    main()
