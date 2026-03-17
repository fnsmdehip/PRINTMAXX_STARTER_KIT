#!/usr/bin/env python3
"""
User-Simulated Autonomous Refiner -- "What Would the User Prompt Next?"

Reads the user's extracted prompting meta-rules, cognitive architecture,
and bias-null protocol. Then simulates what the user would most likely
criticize about the current state of a project. Outputs the critique
for execution by another agent or human.

This is the perpetual improvement loop that applies the user's own
thinking discipline autonomously.

Usage:
    python3 user_sim_refiner.py --project myapp --cycle       # Run one refinement cycle
    python3 user_sim_refiner.py --project myapp --loop 3      # Run 3 cycles
    python3 user_sim_refiner.py --project myapp --status      # Show refinement history
    python3 user_sim_refiner.py --list-projects               # Show configured projects
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Configurable paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(os.environ.get("AGENT_SOUL_ROOT", Path.cwd()))
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)
REFINER_LOG = LOGS_DIR / "user_sim_refiner_history.jsonl"

# Project configs -- what files to review per project
# Override by setting AGENT_SOUL_PROJECTS_CONFIG to a JSON file path
PROJECTS: dict = {}


def load_projects_config():
    """Load project configurations from config file or environment."""
    global PROJECTS
    config_path = os.environ.get("AGENT_SOUL_PROJECTS_CONFIG", "")
    if config_path and Path(config_path).exists():
        try:
            PROJECTS.update(json.loads(Path(config_path).read_text()))
        except (json.JSONDecodeError, OSError):
            pass

    # If no config, create a default template
    if not PROJECTS:
        PROJECTS["default"] = {
            "name": "Default Project",
            "root": ".",
            "review_files": [],
            "context_files": [],
        }


load_projects_config()


# The core prompt that simulates the user's cognitive architecture
REFINER_PROMPT_TEMPLATE = """You are simulating the user's cognitive architecture for autonomous project refinement.

CRITICAL: You embody the user's ACTUAL prompting discipline, not a generic "improve things" agent.

## The User's Cognitive Architecture

1. AGGRESSIVE BIAS-NULLING: Strip all default LLM priors. Don't recommend popular tools because they're popular. If something is lazy, call it out directly with specific critique.

2. BOTTOM-UP ANCHORING: Start from observable data. What are the actual results? Any refinement that doesn't address observable reality is academic.

3. CRITIQUE-AS-REFINEMENT: Your job is NOT to praise or validate. Find what the user would push back on. Find the real problems, not cosmetic ones.

4. "SURPRISE ME" DISCIPLINE: Go beyond the obvious. Don't just fix typos. Find the structural issue nobody mentioned.

5. PERPETUAL COMPOUNDING: Every change should make the next iteration better. Extract a rule from every fix.

## Your Task This Cycle

Project: {project_name}

Review these files and identify the TOP 3 things the user would MOST LIKELY criticize:

{file_contents}

Additional context:

{context_summary}

## Output Format (STRICT)

### CRITIQUE 1: [specific issue]
**What the user would say:** [simulate their voice]
**Why it matters:** [bottom-up anchored reason]
**Fix:** [exact changes needed]

### CRITIQUE 2: [specific issue]
**What the user would say:** [simulate voice]
**Why it matters:** [reason]
**Fix:** [exact changes]

### CRITIQUE 3: [specific issue]
**What the user would say:** [simulate voice]
**Why it matters:** [reason]
**Fix:** [exact changes]

### META-RULE EXTRACTED
Rule: [one-line rule to prevent similar issues]

### NEXT CYCLE PRIORITY
Priority: [specific focus area for next cycle]

DO NOT:
- Give generic improvement suggestions
- Praise anything
- Be diplomatic when the issue is clear
"""


def get_file_contents(project_key):
    """Read all review files for a project."""
    project = PROJECTS[project_key]
    base = Path(project.get("root", "."))
    if not base.is_absolute():
        base = PROJECT_ROOT / base

    contents = []
    for rel_path in project.get("review_files", []):
        full_path = base / rel_path
        if full_path.exists():
            text = full_path.read_text()
            if len(text) > 8000:
                text = text[:4000] + "\n\n[...TRUNCATED...]\n\n" + text[-4000:]
            contents.append(f"=== {rel_path} ({len(text)} chars) ===\n{text}")
        else:
            contents.append(f"=== {rel_path} === FILE NOT FOUND")
    return "\n\n".join(contents)


def get_context_summary(project_key):
    """Read context files and produce brief summary."""
    project = PROJECTS[project_key]
    base = Path(project.get("root", "."))
    if not base.is_absolute():
        base = PROJECT_ROOT / base

    summaries = []
    for rel_path in project.get("context_files", []):
        full_path = base / rel_path
        if full_path.exists():
            text = full_path.read_text()
            summaries.append(f"--- {rel_path} ---\n{text[:500]}...")
    return "\n\n".join(summaries) if summaries else "No additional context files."


def run_cycle(project_key):
    """Run one refinement cycle on a project."""
    if project_key not in PROJECTS:
        print(f"Unknown project: {project_key}. Available: {', '.join(PROJECTS.keys())}")
        return

    project = PROJECTS[project_key]
    print(f"\n{'='*60}")
    print(f"USER-SIM REFINER -- {project['name']} -- {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")

    file_contents = get_file_contents(project_key)
    context_summary = get_context_summary(project_key)
    prompt = REFINER_PROMPT_TEMPLATE.format(
        project_name=project["name"],
        file_contents=file_contents,
        context_summary=context_summary,
    )

    # Write prompt for inspection
    prompt_file = LOGS_DIR / f"user_sim_prompt_{project_key}.md"
    prompt_file.write_text(prompt)

    # Try to run via claude CLI
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
        output = "TIMEOUT: exceeded 5 minute limit"
    except FileNotFoundError:
        output = "claude CLI not available. Install Claude Code or provide a different executor."

    output_file = LOGS_DIR / f"user_sim_output_{project_key}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    output_file.write_text(output)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "project": project_key,
        "output_file": str(output_file),
        "output_preview": output[:500],
    }
    with open(REFINER_LOG, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"\nOutput saved: {output_file.name}")
    print(f"\n--- Output Preview ---")
    print(output[:1000])
    if len(output) > 1000:
        print(f"\n[...{len(output) - 1000} more chars in {output_file.name}]")

    return output


def show_status(project_key):
    """Show refinement history for a project."""
    if not REFINER_LOG.exists():
        print("No refinement history yet.")
        return

    print(f"\n=== User-Sim Refiner History: {project_key} ===\n")
    entries = []
    for line in REFINER_LOG.read_text().strip().split("\n"):
        try:
            entry = json.loads(line)
            if entry.get("project") == project_key:
                entries.append(entry)
        except json.JSONDecodeError:
            continue

    if not entries:
        print(f"No cycles run for {project_key} yet.")
        return

    for e in entries[-10:]:
        print(f"  [{e['timestamp'][:16]}]")
        print(f"    Output: {e.get('output_file', 'N/A')}")
        preview = e.get("output_preview", "")[:200]
        if preview:
            print(f"    Preview: {preview[:100]}...")
        print()

    print(f"Total cycles: {len(entries)}")


def list_projects():
    """List all configured projects."""
    print("\n=== Configured Projects for User-Sim Refiner ===\n")
    for key, v in PROJECTS.items():
        file_count = len(v.get("review_files", []))
        print(f"  {key}: {v['name']} ({file_count} review files configured)")


if __name__ == "__main__":
    args = sys.argv[1:]

    project = None
    for i, arg in enumerate(args):
        if arg == "--project" and i + 1 < len(args):
            project = args[i + 1]

    if "--list-projects" in args:
        list_projects()
    elif "--cycle" in args and project:
        run_cycle(project)
    elif "--loop" in args and project:
        idx = args.index("--loop")
        n = int(args[idx + 1]) if idx + 1 < len(args) else 3
        for i in range(n):
            print(f"\n{'#'*60}")
            print(f"LOOP ITERATION {i+1}/{n}")
            print(f"{'#'*60}")
            run_cycle(project)
    elif "--status" in args and project:
        show_status(project)
    else:
        print("User-Simulated Autonomous Refiner")
        print("Applies your cognitive architecture to continuously improve projects.\n")
        print("Usage:")
        print("  --project NAME --cycle        Run one refinement cycle")
        print("  --project NAME --loop N        Run N cycles")
        print("  --project NAME --status        Show history")
        print("  --list-projects                Show available projects")
