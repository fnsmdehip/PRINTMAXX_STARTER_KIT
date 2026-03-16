#!/usr/bin/env python3
"""
User-Simulated Autonomous Refiner — "What Would Alex Prompt Next?"

Reads the user's extracted prompting meta-rules, cognitive architecture,
and bias-null protocol. Then simulates what the user would most likely
criticize about the current state of a venture. Executes the fix.
Saves with git versioning so everything is revertible.

This is the perpetual improvement loop that applies the user's own
thinking discipline autonomously.

Usage:
    python3 user_sim_refiner.py --venture EAS --cycle       # Run one refinement cycle on EAS
    python3 user_sim_refiner.py --venture EAS --loop N       # Run N cycles
    python3 user_sim_refiner.py --venture EAS --status       # Show refinement history
    python3 user_sim_refiner.py --venture EAS --revert HASH  # Revert to specific git commit
    python3 user_sim_refiner.py --list-ventures              # Show available ventures

Ralph loop:
    while true; do python3 AUTOMATIONS/user_sim_refiner.py --venture EAS --cycle; sleep 300; done

Cron (daily at 4 AM):
    0 4 * * * cd $BASE && $PYTHON AUTOMATIONS/user_sim_refiner.py --venture EAS --cycle >> AUTOMATIONS/logs/user_sim_refiner.log 2>&1
"""

import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"
LOGS_DIR.mkdir(exist_ok=True)
REFINER_LOG = LOGS_DIR / "user_sim_refiner_history.jsonl"

# Venture configs — what files to review per venture
VENTURES = {
    "EAS": {
        "name": "Enterprise Automation Solutions",
        "root": "MONEY_METHODS/EAS",
        "review_files": [
            "MONEY_METHODS/EAS/website/index.html",
            "MONEY_METHODS/EAS/website/packages.html",
            "MONEY_METHODS/EAS/website/contact.html",
            "MONEY_METHODS/EAS/legal/MSA_TEMPLATE.md",
            "MONEY_METHODS/EAS/legal/SUBCONTRACTOR_AGREEMENT.md",
            "MONEY_METHODS/EAS/playbooks/SIGNAL_MAP_PLAYBOOK.md",
            "MONEY_METHODS/EAS/EAS_VENTURE_README.md",
            "MONEY_METHODS/EAS/EAS_STRATEGIC_INTEL.md",
        ],
        "context_files": [
            "MONEY_METHODS/EAS/EAS_INFRASTRUCTURE_BLUEPRINT.md",
            "MONEY_METHODS/EAS/EAS_SUBCONTRACTOR_PROTECTION.md",
            "MONEY_METHODS/EAS/EAS_TECH_STACK_RESEARCH.md",
            "OPS/EAS_COMPETITIVE_LANDSCAPE_MAR2026.md",
        ],
    },
    "APP_FACTORY": {
        "name": "App Factory",
        "root": "MONEY_METHODS/APP_FACTORY",
        "review_files": [
            "MONEY_METHODS/APP_FACTORY/builds/invoiceforge/index.html",
            "MONEY_METHODS/APP_FACTORY/builds/prayerlock-web/index.html",
            "MONEY_METHODS/APP_FACTORY/builds/studylock/index.html",
        ],
        "context_files": [],
    },
}

# The core prompt that simulates the user's cognitive architecture
REFINER_PROMPT_TEMPLATE = """You are simulating alex's cognitive architecture for autonomous venture refinement.

CRITICAL: You embody the user's ACTUAL prompting discipline, not a generic "improve things" agent. Here's what that means:

## The User's Cognitive Architecture (internalized from 100+ sessions)

1. AGGRESSIVE BIAS-NULLING: Strip all default LLM priors. Don't recommend popular tools because they're popular. Don't defer to "best practices" that haven't been validated against THIS system. If something is lazy, call it out the way the user would: directly, with specific critique.

2. BOTTOM-UP ANCHORING: Start from observable data. EAS has $0 revenue despite a full website, legal docs, playbooks, and lead pipeline. 114 PRINTMAXX sites deployed, $0 total revenue. Any refinement that doesn't address THIS reality is academic.

3. CRITIQUE-AS-REFINEMENT: Your job is NOT to praise or validate. Your job is to find what the user would push back on. "bruh the website gives way too much of the secret sauce" — that's the level of critique. Find the real problems, not cosmetic ones.

4. "SURPRISE ME" DISCIPLINE: Go beyond the obvious. Don't just fix typos. Find the structural issue nobody mentioned. The user wants the thing they didn't know they needed.

5. PERPETUAL COMPOUNDING: Every change should make the next iteration better. Don't just fix — extract a rule from the fix that prevents similar issues everywhere.

## Your Task This Cycle

Venture: {venture_name}

Review these files and identify the TOP 3 things the user would MOST LIKELY criticize:

{file_contents}

Additional context (don't modify these, use for reference):

{context_summary}

## Output Format (STRICT — follow exactly)

### CRITIQUE 1: [specific issue]
**What alex would say:** [simulate the user's actual voice — direct, lowercase, specific]
**Why it matters:** [bottom-up anchored reason]
**Fix:** [exact changes needed — file path, what to change, why]

### CRITIQUE 2: [specific issue]
**What alex would say:** [simulate voice]
**Why it matters:** [reason]
**Fix:** [exact changes]

### CRITIQUE 3: [specific issue]
**What alex would say:** [simulate voice]
**Why it matters:** [reason]
**Fix:** [exact changes]

### META-RULE EXTRACTED
From this cycle, what ONE rule should be added to prevent similar issues?
Rule: [one-line rule]

### NEXT CYCLE PRIORITY
What should the NEXT refinement cycle focus on?
Priority: [specific focus area]

DO NOT:
- Give generic improvement suggestions ("make the copy more engaging")
- Praise anything — only critique
- Recommend popular tools without justifying why they're BETTER than what exists
- Suggest changes that move $0 revenue farther from $1 revenue
- Be diplomatic when the issue is clear
"""


def get_file_contents(venture_key):
    """Read all review files for a venture."""
    venture = VENTURES[venture_key]
    contents = []
    for rel_path in venture["review_files"]:
        full_path = PROJECT_ROOT / rel_path
        if full_path.exists():
            text = full_path.read_text()
            # Truncate large files to avoid blowing context
            if len(text) > 8000:
                text = text[:4000] + "\n\n[...TRUNCATED...]\n\n" + text[-4000:]
            contents.append(f"=== {rel_path} ({len(text)} chars) ===\n{text}")
        else:
            contents.append(f"=== {rel_path} === FILE NOT FOUND")
    return "\n\n".join(contents)


def get_context_summary(venture_key):
    """Read context files and produce brief summary."""
    venture = VENTURES[venture_key]
    summaries = []
    for rel_path in venture["context_files"]:
        full_path = PROJECT_ROOT / rel_path
        if full_path.exists():
            text = full_path.read_text()
            # Just first 500 chars as context hint
            summaries.append(f"--- {rel_path} ---\n{text[:500]}...")
    return "\n\n".join(summaries) if summaries else "No additional context files."


def git_snapshot(venture_key, message):
    """Create a git commit snapshot before/after changes for revertibility."""
    venture = VENTURES[venture_key]
    venture_root = PROJECT_ROOT / venture["root"]
    try:
        subprocess.run(
            ["git", "add", str(venture_root)],
            cwd=str(PROJECT_ROOT), capture_output=True, timeout=30
        )
        subprocess.run(
            ["git", "commit", "-m", f"[user-sim-refiner] {venture_key}: {message}",
             "--allow-empty"],
            cwd=str(PROJECT_ROOT), capture_output=True, timeout=30
        )
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(PROJECT_ROOT), capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()[:12]
    except Exception as e:
        return f"git-error: {e}"


def run_cycle(venture_key):
    """Run one refinement cycle on a venture."""
    if venture_key not in VENTURES:
        print(f"Unknown venture: {venture_key}. Available: {', '.join(VENTURES.keys())}")
        return

    venture = VENTURES[venture_key]
    print(f"\n{'='*60}")
    print(f"USER-SIM REFINER — {venture['name']} — Cycle {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")

    # Snapshot before
    before_hash = git_snapshot(venture_key, "pre-refinement snapshot")
    print(f"Pre-snapshot: {before_hash}")

    # Build the prompt
    file_contents = get_file_contents(venture_key)
    context_summary = get_context_summary(venture_key)
    prompt = REFINER_PROMPT_TEMPLATE.format(
        venture_name=venture["name"],
        file_contents=file_contents,
        context_summary=context_summary,
    )

    # Write prompt to temp file
    prompt_file = LOGS_DIR / f"user_sim_prompt_{venture_key}.md"
    prompt_file.write_text(prompt)

    # Run claude -p
    print("Running claude -p with user-sim prompt...")
    try:
        result = subprocess.run(
            ["claude", "-p", str(prompt_file), "--output-format", "text"],
            capture_output=True, text=True, timeout=300,
            cwd=str(PROJECT_ROOT),
        )
        output = result.stdout.strip()
        if not output:
            output = result.stderr.strip()
            if not output:
                output = "No output from claude -p"
    except subprocess.TimeoutExpired:
        output = "TIMEOUT: claude -p exceeded 5 minute limit"
    except FileNotFoundError:
        # claude CLI not available, use a simpler approach
        output = "claude CLI not available. Install Claude Code or use API directly."

    # Save output
    output_file = LOGS_DIR / f"user_sim_output_{venture_key}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    output_file.write_text(output)

    # Snapshot after (if any files changed)
    after_hash = git_snapshot(venture_key, "post-refinement")

    # Log the cycle
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "venture": venture_key,
        "before_hash": before_hash,
        "after_hash": after_hash,
        "output_file": str(output_file.relative_to(PROJECT_ROOT)),
        "output_preview": output[:500],
    }
    with open(REFINER_LOG, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"\nOutput saved: {output_file.name}")
    print(f"Post-snapshot: {after_hash}")
    print(f"Revert command: python3 AUTOMATIONS/user_sim_refiner.py --venture {venture_key} --revert {before_hash}")
    print(f"\n--- Output Preview ---")
    print(output[:1000])
    if len(output) > 1000:
        print(f"\n[...{len(output) - 1000} more chars in {output_file.name}]")

    return output


def show_status(venture_key):
    """Show refinement history for a venture."""
    if not REFINER_LOG.exists():
        print("No refinement history yet.")
        return

    print(f"\n=== User-Sim Refiner History: {venture_key} ===\n")
    entries = []
    for line in REFINER_LOG.read_text().strip().split("\n"):
        try:
            entry = json.loads(line)
            if entry.get("venture") == venture_key:
                entries.append(entry)
        except json.JSONDecodeError:
            continue

    if not entries:
        print(f"No cycles run for {venture_key} yet.")
        return

    for e in entries[-10:]:  # Last 10
        print(f"  [{e['timestamp'][:16]}] {e['before_hash']} → {e['after_hash']}")
        print(f"    Output: {e.get('output_file', 'N/A')}")
        preview = e.get("output_preview", "")[:200]
        if preview:
            print(f"    Preview: {preview[:100]}...")
        print()

    print(f"Total cycles: {len(entries)}")


def revert(venture_key, commit_hash):
    """Revert venture files to a specific git commit."""
    venture = VENTURES[venture_key]
    venture_root = venture["root"]
    print(f"Reverting {venture_key} to commit {commit_hash}...")
    result = subprocess.run(
        ["git", "checkout", commit_hash, "--", venture_root],
        cwd=str(PROJECT_ROOT), capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        print(f"Reverted {venture_root} to {commit_hash}")
        git_snapshot(venture_key, f"reverted to {commit_hash}")
    else:
        print(f"Revert failed: {result.stderr}")


def list_ventures():
    """List all configured ventures."""
    print("\n=== Configured Ventures for User-Sim Refiner ===\n")
    for key, v in VENTURES.items():
        file_count = len([f for f in v["review_files"] if (PROJECT_ROOT / f).exists()])
        total = len(v["review_files"])
        print(f"  {key}: {v['name']} ({file_count}/{total} files exist)")


if __name__ == "__main__":
    args = sys.argv[1:]

    venture = None
    for i, arg in enumerate(args):
        if arg == "--venture" and i + 1 < len(args):
            venture = args[i + 1].upper()

    if "--list-ventures" in args:
        list_ventures()
    elif "--cycle" in args and venture:
        run_cycle(venture)
    elif "--loop" in args and venture:
        idx = args.index("--loop")
        n = int(args[idx + 1]) if idx + 1 < len(args) else 3
        for i in range(n):
            print(f"\n{'#'*60}")
            print(f"LOOP ITERATION {i+1}/{n}")
            print(f"{'#'*60}")
            run_cycle(venture)
    elif "--status" in args and venture:
        show_status(venture)
    elif "--revert" in args and venture:
        idx = args.index("--revert")
        commit_hash = args[idx + 1] if idx + 1 < len(args) else None
        if commit_hash:
            revert(venture, commit_hash)
        else:
            print("Usage: --revert COMMIT_HASH")
    else:
        print("User-Simulated Autonomous Refiner")
        print("Applies your cognitive architecture to continuously improve ventures.\n")
        print("Usage:")
        print("  --venture NAME --cycle        Run one refinement cycle")
        print("  --venture NAME --loop N        Run N cycles")
        print("  --venture NAME --status        Show history")
        print("  --venture NAME --revert HASH   Revert to commit")
        print("  --list-ventures                Show available ventures")
        print()
        print("Ralph loop:")
        print("  while true; do python3 AUTOMATIONS/user_sim_refiner.py --venture EAS --cycle; sleep 300; done")
