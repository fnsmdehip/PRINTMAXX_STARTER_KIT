#!/usr/bin/env python3
"""
AUTONOMOUS INTEGRATOR — Master pipeline that takes approved alpha and FULLY
integrates it into the PRINTMAXX system.

Not surface level. Deep integration using every automation tool available.

10-step pipeline:
  1. Load newly approved entries from ALPHA_STAGING.csv
  2. Claude -p (Opus) deep analysis per entry (venture routing, growth tactics, tooling)
  3. Create new ventures if needed (venture_autonomy.py --create)
  4. Create ralph loops if needed (ralph_loop_factory.py --create)
  5. Create n8n workflows if needed (workflow_bridge)
  6. Create new automation scripts if needed (claude -p generated)
  7. Create hooks if needed
  8. Wire growth tactics (GREY_HAT_EDGE_GROWTH_MASTER.md based plans)
  9. Track in master ops (master_ops_cache.json update)
  10. Update system (system_visualizer, system map, KPI calendar, log)

Cron: 15 22 * * * (10:15 PM, after auto_approve at 10 PM)
Safety: safe_path, py_compile validation, JSON validation, max 5 automations/run

Usage:
  python3 AUTOMATIONS/autonomous_integrator.py --run
  python3 AUTOMATIONS/autonomous_integrator.py --dry-run
  python3 AUTOMATIONS/autonomous_integrator.py --entry ALPHA_ID
  python3 AUTOMATIONS/autonomous_integrator.py --status
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import py_compile
import subprocess
import sys
import textwrap
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT / "AUTOMATIONS"
LEDGER = PROJECT / "LEDGER"
OPS = PROJECT / "OPS"
LOG_FILE = AUTOMATIONS / "logs" / "autonomous_integrator.log"
GROWTH_PLANS_DIR = AUTOMATIONS / "auto_ops" / "growth_plans"
ALPHA_STAGING = LEDGER / "ALPHA_STAGING.csv"
GREY_HAT_MASTER = OPS / "GREY_HAT_EDGE_GROWTH_MASTER.md"
PRIORITY_STACK = OPS / "CAPITAL_GENESIS_PRIORITY_STACK.md"
MASTER_OPS_CACHE = AUTOMATIONS / "master_ops_cache.json"
SYSTEM_MAP = OPS / "PRINTMAXX_SYSTEM_MAP.md"
INTEGRATION_LOG = LEDGER / "integration_runs.jsonl"

MAX_NEW_AUTOMATIONS_PER_RUN = 5
MAX_ENTRIES_PER_RUN = 15
CLAUDE_TIMEOUT = 90

VENTURE_TYPES = [
    "OUTBOUND", "CONTENT", "APP", "LOCAL_BIZ", "RESEARCH",
    "MONETIZE", "PRODUCT", "SCRAPING", "BROKERING",
]

# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------

def safe_path(target: Path | str) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT}")
    return resolved


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [INTEGRATOR] [{level}] {msg}"
    print(line)
    safe_path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_FILE), "a") as f:
        f.write(line + "\n")


def log_integration_run(run_data: dict) -> None:
    """Append a structured record of this integration run to the JSONL ledger."""
    safe_path(INTEGRATION_LOG).parent.mkdir(parents=True, exist_ok=True)
    with open(safe_path(INTEGRATION_LOG), "a") as f:
        f.write(json.dumps(run_data, default=str) + "\n")


# ---------------------------------------------------------------------------
# Subprocess helpers
# ---------------------------------------------------------------------------

def run_cmd(cmd: list[str], timeout: int = 120, cwd: str | None = None) -> tuple[str, bool]:
    """Run a command, return (stdout, success)."""
    try:
        r = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd or str(PROJECT),
        )
        return r.stdout.strip(), r.returncode == 0
    except subprocess.TimeoutExpired:
        return "TIMEOUT", False
    except Exception as e:
        return str(e), False


def claude_p(prompt: str, timeout: int = CLAUDE_TIMEOUT) -> tuple[str, bool]:
    """Run claude -p with a prompt. Returns (output, success)."""
    return run_cmd(["claude", "-p", prompt], timeout=timeout)


def validate_json(text: str) -> Optional[dict]:
    """Extract and validate JSON from claude -p output. Returns parsed dict or None."""
    # Try direct parse first
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        pass

    # Try to find JSON block in output (claude often wraps in markdown)
    import re
    patterns = [
        r"```json\s*\n(.*?)\n\s*```",
        r"```\s*\n(\{.*?\})\n\s*```",
        r"(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})",
    ]
    for pat in patterns:
        match = re.search(pat, text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except (json.JSONDecodeError, TypeError):
                continue
    return None


# ---------------------------------------------------------------------------
# Step 1: Load newly approved entries
# ---------------------------------------------------------------------------

def load_approved_today() -> list[dict]:
    """Read ALPHA_STAGING.csv for entries approved today."""
    if not ALPHA_STAGING.exists():
        log("ALPHA_STAGING.csv not found", "WARN")
        return []

    today = datetime.now().strftime("%Y-%m-%d")
    approved = []
    try:
        with open(ALPHA_STAGING) as f:
            reader = csv.DictReader(f)
            for row in reader:
                status = (row.get("status") or "").upper()
                notes = row.get("reviewer_notes") or ""
                if status == "APPROVED" and today in notes:
                    approved.append(row)
    except Exception as e:
        log(f"Error reading ALPHA_STAGING: {e}", "ERROR")

    log(f"Step 1: Found {len(approved)} entries approved today ({today})")
    return approved[:MAX_ENTRIES_PER_RUN]


def load_entry_by_id(alpha_id: str) -> list[dict]:
    """Load a specific entry by its alpha_id field."""
    if not ALPHA_STAGING.exists():
        return []
    try:
        with open(ALPHA_STAGING) as f:
            reader = csv.DictReader(f)
            for row in reader:
                row_id = row.get("alpha_id") or row.get("id") or row.get("entry_id") or ""
                if row_id == alpha_id:
                    return [row]
                # Also match on extracted_method if id not found
                method = row.get("extracted_method") or ""
                if method and alpha_id.lower() in method.lower():
                    return [row]
    except Exception as e:
        log(f"Error loading entry {alpha_id}: {e}", "ERROR")
    return []


# ---------------------------------------------------------------------------
# Step 2: Claude -p deep analysis
# ---------------------------------------------------------------------------

def load_grey_hat_context(max_lines: int = 200) -> str:
    """Load first N lines of GREY_HAT_EDGE_GROWTH_MASTER.md for context injection."""
    if not GREY_HAT_MASTER.exists():
        return ""
    try:
        lines = GREY_HAT_MASTER.read_text().splitlines()[:max_lines]
        return "\n".join(lines)
    except Exception:
        return ""


def load_priority_stack() -> str:
    """Load current Capital Genesis priority stack."""
    if not PRIORITY_STACK.exists():
        return "No priority stack available."
    try:
        return PRIORITY_STACK.read_text()[:3000]
    except Exception:
        return ""


def deep_analysis(entry: dict) -> Optional[dict]:
    """Run claude -p deep analysis on a single alpha entry. Returns structured JSON."""
    method = entry.get("extracted_method") or entry.get("tactic") or entry.get("content") or ""
    source = entry.get("source") or "unknown"
    roi = entry.get("roi_potential") or "UNKNOWN"

    if not method:
        log("Skipping entry with empty method content", "WARN")
        return None

    grey_hat_ctx = load_grey_hat_context()
    priority_ctx = load_priority_stack()

    prompt = textwrap.dedent(f"""\
        You are the PRINTMAXX autonomous integrator. Analyze this approved alpha entry
        and decide EXACTLY how to integrate it into the system.

        ENTRY:
        Method: {method[:800]}
        Source: {source}
        ROI Potential: {roi}

        EXISTING VENTURE TYPES: {', '.join(VENTURE_TYPES)}

        CAPITAL GENESIS PRIORITY STACK (current):
        {priority_ctx[:1500]}

        GROWTH TACTICS AVAILABLE (from Grey Hat Edge Master):
        {grey_hat_ctx[:2000]}

        CONSTRAINTS:
        - Budget: $0 (Phase 0 / Phase 1)
        - Must be automatable
        - Prefer existing ventures over creating new ones
        - New ventures only if method genuinely doesn't fit any existing type

        OUTPUT EXACTLY THIS JSON (no other text):
        {{
            "venture_type": "EXISTING_TYPE or NEW:type_name",
            "automation_needed": true or false,
            "automation_type": "scraper|poster|workflow|ralph_loop|cron|hook",
            "automation_description": "what the automation does",
            "script_name": "suggested_script_name.py",
            "growth_tactics": ["tactic1", "tactic2"],
            "tooling_stack": {{"browser": "GoLogin+SOAX or none", "email": "Instantly or none", "content": "content_factory or none"}},
            "budget_tier": "FREE|LOW|MID",
            "n8n_workflow_needed": true or false,
            "n8n_workflow_description": "what the workflow does or empty string",
            "ralph_loop_needed": true or false,
            "ralph_loop_op_id": "OP_ID or empty string",
            "estimated_revenue": "$X-Y/mo",
            "execution_steps": ["step1", "step2", "step3"]
        }}
    """)

    output, ok = claude_p(prompt)
    if not ok:
        log(f"Claude -p analysis failed: {output[:200]}", "ERROR")
        return None

    result = validate_json(output)
    if result is None:
        log(f"Failed to parse JSON from claude -p output: {output[:300]}", "ERROR")
        return None

    # Attach original entry metadata
    result["_source_entry"] = {
        "method": method[:200],
        "source": source,
        "roi": roi,
        "alpha_id": entry.get("alpha_id") or entry.get("id") or "",
    }

    log(f"Step 2: Analysis complete -> venture={result.get('venture_type')}, "
        f"automation={result.get('automation_needed')}, "
        f"revenue={result.get('estimated_revenue')}")
    return result


# ---------------------------------------------------------------------------
# Step 3: Create new ventures if needed
# ---------------------------------------------------------------------------

def create_venture(analysis: dict, dry_run: bool = False) -> bool:
    """Create a new venture if venture_type starts with NEW:."""
    vtype = analysis.get("venture_type", "")
    if not vtype.startswith("NEW:"):
        return False

    new_type = vtype.replace("NEW:", "").strip().upper()
    method_name = (analysis.get("_source_entry", {}).get("method", "")[:40]
                   .replace(" ", "_").replace("/", "_"))
    venture_name = method_name or new_type.lower()

    if dry_run:
        log(f"Step 3 [DRY-RUN]: Would create venture type={new_type} name={venture_name}")
        return True

    cmd = ["python3", str(AUTOMATIONS / "venture_autonomy.py"),
           "--create", new_type, venture_name]
    out, ok = run_cmd(cmd)
    if ok:
        log(f"Step 3: Created venture type={new_type} name={venture_name}")
    else:
        log(f"Step 3: Venture creation failed: {out[:200]}", "ERROR")
    return ok


# ---------------------------------------------------------------------------
# Step 4: Create ralph loops if needed
# ---------------------------------------------------------------------------

def create_ralph_loop(analysis: dict, dry_run: bool = False) -> bool:
    """Create a ralph loop if ralph_loop_needed is True."""
    if not analysis.get("ralph_loop_needed"):
        return False

    op_id = analysis.get("ralph_loop_op_id", "")
    if not op_id:
        # Generate an op_id from the method
        method = analysis.get("_source_entry", {}).get("method", "unknown")
        op_id = method[:20].upper().replace(" ", "_").replace("/", "_")

    if dry_run:
        log(f"Step 4 [DRY-RUN]: Would create ralph loop for op_id={op_id}")
        return True

    cmd = ["python3", str(AUTOMATIONS / "ralph_loop_factory.py"), "--create", op_id]
    out, ok = run_cmd(cmd)
    if ok:
        log(f"Step 4: Created ralph loop for op_id={op_id}")
    else:
        log(f"Step 4: Ralph loop creation failed: {out[:200]}", "ERROR")
    return ok


# ---------------------------------------------------------------------------
# Step 5: Create n8n workflows if needed
# ---------------------------------------------------------------------------

def create_n8n_workflow(analysis: dict, dry_run: bool = False) -> bool:
    """Create an n8n workflow using workflow_bridge if needed."""
    if not analysis.get("n8n_workflow_needed"):
        return False

    description = analysis.get("n8n_workflow_description", "")
    if not description:
        return False

    if dry_run:
        log(f"Step 5 [DRY-RUN]: Would create n8n workflow: {description[:100]}")
        return True

    # Try sovrun WorkflowBuilder first
    try:
        sys.path.insert(0, str(PROJECT / "OPEN_SOURCE" / "agent-soul"))
        from core.workflow_bridge import WorkflowBuilder, WorkflowManager
        builder = WorkflowBuilder()
        workflow = builder.build_from_description(description)
        if workflow:
            manager = WorkflowManager()
            deployed = manager.deploy(workflow)
            if deployed:
                log(f"Step 5: n8n workflow deployed: {description[:80]}")
                return True
    except Exception as e:
        log(f"Step 5: WorkflowBuilder not available ({e}), falling back to plan file", "WARN")

    # Fallback: write workflow plan for manual creation
    plan_dir = safe_path(AUTOMATIONS / "auto_ops" / "n8n_plans")
    plan_dir.mkdir(parents=True, exist_ok=True)
    plan_name = f"n8n_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    plan_path = safe_path(plan_dir / plan_name)
    plan_path.write_text(
        f"# n8n Workflow Plan\n\n"
        f"**Created:** {datetime.now().isoformat()}\n"
        f"**Description:** {description}\n\n"
        f"## Execution Steps\n\n"
        + "\n".join(f"- {s}" for s in analysis.get("execution_steps", []))
        + f"\n\n## Tooling\n\n{json.dumps(analysis.get('tooling_stack', {}), indent=2)}\n"
    )
    log(f"Step 5: n8n workflow plan saved to {plan_name}")
    return True


# ---------------------------------------------------------------------------
# Step 6: Create new automation scripts if needed
# ---------------------------------------------------------------------------

def create_automation_script(analysis: dict, automations_created: int,
                             dry_run: bool = False) -> tuple[bool, int]:
    """Generate a new Python automation script using claude -p."""
    if not analysis.get("automation_needed"):
        return False, automations_created

    if automations_created >= MAX_NEW_AUTOMATIONS_PER_RUN:
        log(f"Step 6: Skipping — max {MAX_NEW_AUTOMATIONS_PER_RUN} automations/run reached", "WARN")
        return False, automations_created

    script_name = analysis.get("script_name", "")
    if not script_name:
        method = analysis.get("_source_entry", {}).get("method", "auto")
        script_name = method[:30].lower().replace(" ", "_").replace("/", "_") + ".py"

    # Sanitize script name
    script_name = "".join(c for c in script_name if c.isalnum() or c in "_-.").strip(".")
    if not script_name.endswith(".py"):
        script_name += ".py"

    script_path = AUTOMATIONS / script_name
    if script_path.exists():
        log(f"Step 6: Script {script_name} already exists, skipping creation")
        return False, automations_created

    description = analysis.get("automation_description", "")
    auto_type = analysis.get("automation_type", "workflow")
    method_text = analysis.get("_source_entry", {}).get("method", "")

    if dry_run:
        log(f"Step 6 [DRY-RUN]: Would create script {script_name} ({auto_type}): {description[:80]}")
        return True, automations_created + 1

    prompt = textwrap.dedent(f"""\
        Write a complete Python3 script for the PRINTMAXX automation system.

        PURPOSE: {description}
        TYPE: {auto_type}
        METHOD CONTEXT: {method_text[:500]}

        REQUIREMENTS (follow these EXACTLY):
        1. Start with #!/usr/bin/env python3 and a docstring
        2. Use pathlib.Path for all file paths
        3. Define PROJECT = Path(__file__).resolve().parent.parent
        4. Include safe_path() function that validates paths are within PROJECT
        5. Include argparse CLI with at least --run and --status
        6. Log to AUTOMATIONS/logs/{script_name.replace('.py', '')}.log using append mode
        7. All file writes go through safe_path()
        8. Use csv, json, subprocess — no exotic dependencies
        9. Be cron-ready (no interactive input, exit cleanly)
        10. Handle errors gracefully with try/except
        11. Include if __name__ == "__main__": main() block

        Output ONLY the Python code. No markdown fences. No explanation.
    """)

    output, ok = claude_p(prompt, timeout=120)
    if not ok:
        log(f"Step 6: Script generation failed: {output[:200]}", "ERROR")
        return False, automations_created

    # Strip markdown fences if present
    code = output.strip()
    if code.startswith("```python"):
        code = code[len("```python"):].strip()
    if code.startswith("```"):
        code = code[3:].strip()
    if code.endswith("```"):
        code = code[:-3].strip()

    # Validate the generated code compiles
    test_path = safe_path(AUTOMATIONS / f".tmp_validate_{script_name}")
    try:
        test_path.write_text(code)
        py_compile.compile(str(test_path), doraise=True)
    except py_compile.PyCompileError as e:
        log(f"Step 6: Generated script failed compilation: {e}", "ERROR")
        if test_path.exists():
            test_path.unlink()
        return False, automations_created
    finally:
        if test_path.exists():
            test_path.unlink()

    # Write the validated script
    final_path = safe_path(script_path)
    final_path.write_text(code)
    os.chmod(str(final_path), 0o755)
    log(f"Step 6: Created and validated script {script_name}")

    # Add to crontab if it's a periodic automation
    if auto_type in ("scraper", "poster", "cron"):
        _add_cron_entry(script_name, analysis)

    return True, automations_created + 1


def _add_cron_entry(script_name: str, analysis: dict) -> None:
    """Add a cron entry for a new automation script."""
    script_path = AUTOMATIONS / script_name

    # Pick a cron schedule based on automation type
    auto_type = analysis.get("automation_type", "cron")
    schedules = {
        "scraper": "30 6 * * *",    # 6:30 AM daily
        "poster": "0 9 * * *",      # 9 AM daily
        "cron": "0 8 * * *",        # 8 AM daily
    }
    schedule = schedules.get(auto_type, "0 8 * * *")

    cron_line = f"{schedule} cd {PROJECT} && python3 {script_path} --run >> {AUTOMATIONS}/logs/{script_name.replace('.py', '')}.log 2>&1"

    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=10)
        existing = result.stdout if result.returncode == 0 else ""

        # Check if already in crontab
        if script_name in existing:
            log(f"Cron: {script_name} already in crontab")
            return

        new_crontab = existing.rstrip() + f"\n# Auto-integrated {datetime.now().strftime('%Y-%m-%d')} by autonomous_integrator\n{cron_line}\n"

        proc = subprocess.run(
            ["crontab", "-"],
            input=new_crontab,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if proc.returncode == 0:
            log(f"Cron: Added {script_name} at {schedule}")
        else:
            log(f"Cron: Failed to add {script_name}: {proc.stderr[:100]}", "ERROR")
    except Exception as e:
        log(f"Cron: Error adding {script_name}: {e}", "ERROR")


# ---------------------------------------------------------------------------
# Step 7: Create hooks if needed
# ---------------------------------------------------------------------------

def create_hooks(analysis: dict, dry_run: bool = False) -> bool:
    """Create PreToolUse hooks if the method needs validation/gating."""
    auto_type = analysis.get("automation_type", "")
    if auto_type != "hook":
        return False

    description = analysis.get("automation_description", "")
    if not description:
        return False

    if dry_run:
        log(f"Step 7 [DRY-RUN]: Would create hook: {description[:80]}")
        return True

    hooks_dir = safe_path(AUTOMATIONS / "hooks")
    hooks_dir.mkdir(parents=True, exist_ok=True)

    hook_name = f"hook_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sh"
    hook_path = safe_path(hooks_dir / hook_name)

    hook_content = textwrap.dedent(f"""\
        #!/bin/bash
        # Auto-generated hook by autonomous_integrator
        # Purpose: {description}
        # Created: {datetime.now().isoformat()}
        #
        # Hook type: PreToolUse
        # This hook is a placeholder. Review and customize before enabling.

        # Exit 0 = allow, exit 1 = block
        exit 0
    """)

    hook_path.write_text(hook_content)
    os.chmod(str(hook_path), 0o755)
    log(f"Step 7: Hook placeholder created at {hook_name} (review before enabling)")
    return True


# ---------------------------------------------------------------------------
# Step 8: Wire growth tactics
# ---------------------------------------------------------------------------

def wire_growth_tactics(analysis: dict, dry_run: bool = False) -> bool:
    """Create a growth plan file with specific tactics from the analysis."""
    tactics = analysis.get("growth_tactics", [])
    if not tactics:
        return False

    method = analysis.get("_source_entry", {}).get("method", "unknown")
    method_slug = method[:40].lower().replace(" ", "_").replace("/", "_")
    method_slug = "".join(c for c in method_slug if c.isalnum() or c == "_")

    plan_name = f"GROWTH_{method_slug}.md"

    if dry_run:
        log(f"Step 8 [DRY-RUN]: Would create growth plan: {plan_name}")
        return True

    safe_path(GROWTH_PLANS_DIR).mkdir(parents=True, exist_ok=True)
    plan_path = safe_path(GROWTH_PLANS_DIR / plan_name)

    venture_type = analysis.get("venture_type", "UNKNOWN")
    budget_tier = analysis.get("budget_tier", "FREE")
    revenue_est = analysis.get("estimated_revenue", "TBD")
    tooling = analysis.get("tooling_stack", {})
    steps = analysis.get("execution_steps", [])

    plan_content = textwrap.dedent(f"""\
        # Growth Plan: {method[:60]}

        **Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
        **Venture:** {venture_type}
        **Budget Tier:** {budget_tier}
        **Estimated Revenue:** {revenue_est}
        **Source:** {analysis.get('_source_entry', {}).get('source', 'unknown')}

        ---

        ## Tactics

    """)
    for i, tactic in enumerate(tactics, 1):
        plan_content += f"{i}. {tactic}\n"

    plan_content += "\n## Account Tiers\n\n"
    plan_content += "| Tier | Approach | Risk |\n"
    plan_content += "|------|----------|------|\n"
    plan_content += "| SAFE | Organic growth, official APIs, platform-compliant | NONE |\n"
    plan_content += "| MEDIUM | Multi-account, light automation, engagement warming | Shadowban |\n"
    plan_content += "| AGGRESSIVE | Full automation, proxy rotation, high-volume outreach | Account ban |\n"

    plan_content += "\n## Daily Actions\n\n"
    for i, step in enumerate(steps, 1):
        plan_content += f"- [ ] {step}\n"

    plan_content += f"\n## Tooling Stack\n\n```json\n{json.dumps(tooling, indent=2)}\n```\n"

    plan_path.write_text(plan_content)
    log(f"Step 8: Growth plan created: {plan_name}")
    return True


# ---------------------------------------------------------------------------
# Step 9: Track in master ops
# ---------------------------------------------------------------------------

def update_master_ops(analysis: dict, dry_run: bool = False) -> bool:
    """Add entries to master_ops_cache.json under the appropriate sheets."""
    if dry_run:
        log("Step 9 [DRY-RUN]: Would update master_ops_cache.json")
        return True

    if not MASTER_OPS_CACHE.exists():
        log("Step 9: master_ops_cache.json not found, skipping", "WARN")
        return False

    try:
        with open(MASTER_OPS_CACHE) as f:
            cache = json.load(f)
    except Exception as e:
        log(f"Step 9: Failed to read master_ops_cache: {e}", "ERROR")
        return False

    sheets = cache.get("sheets", {})
    method = analysis.get("_source_entry", {}).get("method", "unknown")
    venture_type = analysis.get("venture_type", "UNKNOWN").replace("NEW:", "")
    now_iso = datetime.now().isoformat()

    # Add to ALL OPS MASTER
    all_ops = sheets.get("ALL OPS MASTER", [])
    new_op = {
        "OP_ID": f"AUTO_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "Category": venture_type,
        "Op Name": method[:60],
        "Status": "QUEUED",
        "Priority": "P1",
        "Revenue Potential": analysis.get("estimated_revenue", "TBD"),
        "Budget": analysis.get("budget_tier", "FREE"),
        "Added": now_iso,
        "Source": "autonomous_integrator",
    }
    all_ops.append(new_op)
    sheets["ALL OPS MASTER"] = all_ops

    # Add to AUTO_STATUS_LIVE
    auto_status = sheets.get("AUTO_STATUS_LIVE", [])
    auto_entry = {
        "Script": analysis.get("script_name", ""),
        "Status": "CREATED" if analysis.get("automation_needed") else "N/A",
        "Venture": venture_type,
        "Created": now_iso,
        "Type": analysis.get("automation_type", ""),
    }
    auto_status.append(auto_entry)
    sheets["AUTO_STATUS_LIVE"] = auto_status

    # Add to VENTURE_AUTOMATION_MAP
    vam = sheets.get("VENTURE_AUTOMATION_MAP", [])
    vam_entry = {
        "Venture": venture_type,
        "Automation": analysis.get("script_name", "manual"),
        "Type": analysis.get("automation_type", ""),
        "Schedule": "daily" if analysis.get("automation_needed") else "manual",
        "Added": now_iso,
    }
    vam.append(vam_entry)
    sheets["VENTURE_AUTOMATION_MAP"] = vam

    cache["sheets"] = sheets
    cache["last_integration"] = now_iso

    # Atomic write
    tmp = MASTER_OPS_CACHE.with_suffix(".tmp")
    try:
        with open(safe_path(tmp), "w") as f:
            json.dump(cache, f, indent=2, default=str)
        tmp.rename(MASTER_OPS_CACHE)
        log(f"Step 9: Master ops updated — op={new_op['OP_ID']}, venture={venture_type}")
        return True
    except Exception as e:
        log(f"Step 9: Failed to write master_ops_cache: {e}", "ERROR")
        if tmp.exists():
            tmp.unlink()
        return False


# ---------------------------------------------------------------------------
# Step 10: Update system
# ---------------------------------------------------------------------------

def update_system(analyses: list[dict], dry_run: bool = False) -> None:
    """Run system visualizer, update system map, log the run."""
    if dry_run:
        log("Step 10 [DRY-RUN]: Would update system visualizer + system map")
        return

    # Run system_visualizer.py
    out, ok = run_cmd(["python3", str(AUTOMATIONS / "system_visualizer.py")], timeout=60)
    log(f"Step 10: System visualizer {'OK' if ok else 'FAILED'}")

    # Append integration summary to system map
    if SYSTEM_MAP.exists():
        try:
            new_scripts = [a.get("script_name", "") for a in analyses
                          if a.get("automation_needed") and a.get("script_name")]
            new_ventures = [a.get("venture_type", "") for a in analyses
                          if a.get("venture_type", "").startswith("NEW:")]

            if new_scripts or new_ventures:
                summary = f"\n<!-- Auto-integrated {datetime.now().strftime('%Y-%m-%d %H:%M')} -->\n"
                if new_scripts:
                    summary += f"<!-- New scripts: {', '.join(new_scripts)} -->\n"
                if new_ventures:
                    summary += f"<!-- New ventures: {', '.join(new_ventures)} -->\n"

                existing = safe_path(SYSTEM_MAP).read_text()
                if summary.strip() not in existing:
                    with open(safe_path(SYSTEM_MAP), "a") as f:
                        f.write(summary)
                    log("Step 10: System map updated with integration markers")
        except Exception as e:
            log(f"Step 10: System map update failed: {e}", "WARN")

    # Log the complete run to integration ledger
    run_summary = {
        "timestamp": datetime.now().isoformat(),
        "entries_processed": len(analyses),
        "ventures_created": sum(1 for a in analyses if a.get("venture_type", "").startswith("NEW:")),
        "automations_created": sum(1 for a in analyses if a.get("automation_needed")),
        "ralph_loops": sum(1 for a in analyses if a.get("ralph_loop_needed")),
        "n8n_workflows": sum(1 for a in analyses if a.get("n8n_workflow_needed")),
        "growth_plans": sum(1 for a in analyses if a.get("growth_tactics")),
        "methods": [a.get("_source_entry", {}).get("method", "")[:60] for a in analyses],
    }
    log_integration_run(run_summary)
    log(f"Step 10: Integration run logged — {json.dumps(run_summary, default=str)}")


# ---------------------------------------------------------------------------
# Pipeline status
# ---------------------------------------------------------------------------

def show_status() -> None:
    """Show current integration pipeline status."""
    print("=" * 70)
    print("AUTONOMOUS INTEGRATOR — Pipeline Status")
    print("=" * 70)

    # Check alpha staging
    pending = approved_today = total = 0
    if ALPHA_STAGING.exists():
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            with open(ALPHA_STAGING) as f:
                for row in csv.DictReader(f):
                    total += 1
                    status = (row.get("status") or "").upper()
                    notes = row.get("reviewer_notes") or ""
                    if status == "PENDING_REVIEW":
                        pending += 1
                    elif status == "APPROVED" and today in notes:
                        approved_today += 1
        except Exception:
            pass

    print(f"\nAlpha Staging: {total} total, {pending} pending, {approved_today} approved today")

    # Check integration log
    runs = 0
    last_run = "never"
    if INTEGRATION_LOG.exists():
        try:
            lines = INTEGRATION_LOG.read_text().strip().splitlines()
            runs = len(lines)
            if lines:
                last = json.loads(lines[-1])
                last_run = last.get("timestamp", "unknown")
        except Exception:
            pass

    print(f"Integration Runs: {runs} total, last run: {last_run}")

    # Check growth plans
    plan_count = 0
    if GROWTH_PLANS_DIR.exists():
        plan_count = len(list(GROWTH_PLANS_DIR.glob("GROWTH_*.md")))
    print(f"Growth Plans: {plan_count}")

    # Check master ops cache freshness
    if MASTER_OPS_CACHE.exists():
        try:
            age_h = (time.time() - MASTER_OPS_CACHE.stat().st_mtime) / 3600
            print(f"Master Ops Cache: {age_h:.1f}h old")
        except Exception:
            print("Master Ops Cache: unknown age")
    else:
        print("Master Ops Cache: NOT FOUND")

    # Check cron entry
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
        if "autonomous_integrator" in result.stdout:
            print("Cron: INSTALLED")
        else:
            print("Cron: NOT INSTALLED (add: 15 22 * * *)")
    except Exception:
        print("Cron: unable to check")

    print(f"\nMax automations per run: {MAX_NEW_AUTOMATIONS_PER_RUN}")
    print(f"Max entries per run: {MAX_ENTRIES_PER_RUN}")
    print("=" * 70)


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_pipeline(entries: list[dict], dry_run: bool = False) -> None:
    """Execute the full 10-step integration pipeline on a list of approved entries."""
    if not entries:
        log("No entries to process. Pipeline complete (nothing to do).")
        return

    mode = "DRY-RUN" if dry_run else "LIVE"
    log(f"Pipeline starting ({mode}) — {len(entries)} entries to process")

    analyses: list[dict] = []
    automations_created = 0

    for i, entry in enumerate(entries, 1):
        method = entry.get("extracted_method") or entry.get("tactic") or entry.get("content") or "unknown"
        log(f"--- Entry {i}/{len(entries)}: {method[:60]} ---")

        # Step 2: Deep analysis
        analysis = deep_analysis(entry)
        if analysis is None:
            log(f"Skipping entry {i} — analysis failed", "WARN")
            continue

        analyses.append(analysis)

        # Step 3: Create new ventures
        create_venture(analysis, dry_run=dry_run)

        # Step 4: Create ralph loops
        create_ralph_loop(analysis, dry_run=dry_run)

        # Step 5: Create n8n workflows
        create_n8n_workflow(analysis, dry_run=dry_run)

        # Step 6: Create automation scripts
        _, automations_created = create_automation_script(
            analysis, automations_created, dry_run=dry_run
        )

        # Step 7: Create hooks
        create_hooks(analysis, dry_run=dry_run)

        # Step 8: Wire growth tactics
        wire_growth_tactics(analysis, dry_run=dry_run)

        # Step 9: Track in master ops
        update_master_ops(analysis, dry_run=dry_run)

    # Step 10: Update system (once, after all entries)
    update_system(analyses, dry_run=dry_run)

    log(f"Pipeline complete ({mode}) — "
        f"{len(analyses)} analyzed, "
        f"{automations_created} automations created, "
        f"{sum(1 for a in analyses if a.get('ralph_loop_needed'))} ralph loops, "
        f"{sum(1 for a in analyses if a.get('growth_tactics'))} growth plans")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Autonomous Integrator — deep alpha integration pipeline"
    )
    parser.add_argument("--run", action="store_true",
                        help="Process all today's approved entries")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be created without creating")
    parser.add_argument("--entry", type=str,
                        help="Process a specific entry by alpha_id")
    parser.add_argument("--status", action="store_true",
                        help="Show integration pipeline status")

    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.entry:
        entries = load_entry_by_id(args.entry)
        if not entries:
            log(f"Entry not found: {args.entry}", "ERROR")
            sys.exit(1)
        run_pipeline(entries, dry_run=args.dry_run)
        return

    if args.run or args.dry_run:
        # Step 1: Load approved entries
        entries = load_approved_today()
        run_pipeline(entries, dry_run=args.dry_run)
        return

    # Default: show status
    parser.print_help()


if __name__ == "__main__":
    main()
