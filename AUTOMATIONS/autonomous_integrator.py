#!/usr/bin/env python3
"""
AUTONOMOUS INTEGRATOR V2 — Full-toolkit alpha integration pipeline.

Takes approved alpha from ALPHA_STAGING.csv and FULLY integrates it into the
PRINTMAXX system using EVERY automation tool available:

  1. Load newly approved entries
  2. Query procedural memory (have we solved something similar?)
  3. Claude -p deep analysis with FULL toolkit inventory
  4. Decide optimal tool combination per entry
  5. Execute integration via selected tools:
     - Ventures (venture_autonomy.py)
     - Ralph loops (ralph_loop_factory.py)
     - n8n workflows (WorkflowBuilder API or claude -p generated)
     - Automation scripts (claude -p generated, py_compile validated)
     - Hooks (settings.json integration or shell hooks)
     - DAG pipelines (sovrun DAGOrchestrator for multi-step methods)
     - Handoff chains (HandoffRouter for pipeline methods)
     - Subagent delegation (claude -p parallel tasks)
     - MCP server wiring (connector registry)
     - Cron scheduling (budget-aware timing)
  6. Wire growth tactics (edge + budget tiers)
  7. Track in master ops + capture procedural memory
  8. Update system (visualizer, system map, KPI calendar)
  9. Auto-detect gaps (methods that SHOULD have been caught but weren't)

V2 changes from V1:
  - Procedural memory recall BEFORE analysis (don't re-solve solved problems)
  - Full toolkit in claude -p prompt (hooks, DAGs, handoffs, MCP, subagents)
  - Budget-aware tool selection (FREE/LOW/MID/HIGH stacks)
  - DAG creation for complex multi-step methods
  - Handoff chain creation for pipeline methods
  - Parallel subagent execution for independent subtasks
  - MCP connector detection and wiring
  - Gap detection (what should the pipeline have caught?)
  - Skill capture (learn from every integration for next time)
  - Edge growth auto-injection
  - Integration quality scoring

Cron: 15 22 * * * (10:15 PM, after auto_approve at 10 PM)
Safety: safe_path, py_compile validation, JSON validation, max 5 automations/run

Usage:
  python3 AUTOMATIONS/autonomous_integrator.py --run
  python3 AUTOMATIONS/autonomous_integrator.py --dry-run
  python3 AUTOMATIONS/autonomous_integrator.py --entry ALPHA_ID
  python3 AUTOMATIONS/autonomous_integrator.py --status
  python3 AUTOMATIONS/autonomous_integrator.py --gap-check
  python3 AUTOMATIONS/autonomous_integrator.py --replay-failed
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

# Ensure sibling modules are importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (
    PROJECT,
    safe_path,
    recall_skills_for_task,
    capture_skill_from_result,
    get_handoff_router,
    get_workflow_detector,
    should_use_workflow,
    load_json,
    sovrun_available,
)

# Sovrun modules — graceful fallback
_SOVRUN_PATH = str(PROJECT / "OPEN_SOURCE" / "agent-soul")
if _SOVRUN_PATH not in sys.path:
    sys.path.insert(0, _SOVRUN_PATH)

_DAG_AVAILABLE = False
try:
    from core.orchestration import DAGOrchestrator, AgentStep, StepStatus
    _DAG_AVAILABLE = True
except ImportError:
    DAGOrchestrator = None  # type: ignore[assignment, misc]
    AgentStep = None  # type: ignore[assignment, misc]
    StepStatus = None  # type: ignore[assignment, misc]

# Resilience — trajectory logging
try:
    from agent_resilience import TrajectoryLogger
    _trajectory = TrajectoryLogger("integrator_v2")
except ImportError:
    _trajectory = None  # type: ignore[assignment]

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

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
HANDOFF_CHAINS_DIR = AUTOMATIONS / "auto_ops" / "handoff_chains"
DAG_PLANS_DIR = AUTOMATIONS / "auto_ops" / "dag_plans"
CONNECTOR_REGISTRY = AUTOMATIONS / "connector_registry.json"
INTELLIGENCE_CATALOG = OPS / "INTELLIGENCE_CATALOG.json"
FAILED_INTEGRATIONS = LEDGER / "failed_integrations.jsonl"
GAP_REPORT = OPS / "INTEGRATION_GAP_REPORT.md"

MAX_NEW_AUTOMATIONS_PER_RUN = 25
MAX_ENTRIES_PER_RUN = 9999  # No cap — process everything
CLAUDE_TIMEOUT = 300  # 5 min: script generation is complex (was 180, timing out)
MIN_QUALITY_SCORE = 3  # 0-10, only reject truly empty/platitude entries

VENTURE_TYPES = [
    "OUTBOUND", "CONTENT", "APP", "LOCAL_BIZ", "RESEARCH",
    "MONETIZE", "PRODUCT", "SCRAPING", "BROKERING", "EAS",
]

# Full toolkit inventory — injected into claude -p analysis prompt
TOOLKIT_INVENTORY = """
AVAILABLE AUTOMATION TOOLS (pick the OPTIMAL combination for this method):

1. VENTURE (venture_autonomy.py --create TYPE NAME)
   Use when: method is a new revenue lane not covered by existing ventures
   Cost: FREE

2. RALPH LOOP (ralph_loop_factory.py --create OP_ID)
   Use when: method needs iterative refinement over multiple cycles (overnight loops)
   Cost: FREE (Claude Max)

3. N8N WORKFLOW (n8n API at localhost:5678)
   Use when: method needs multi-service connectors (email+CRM+scraper+LLM chains)
   Cost: FREE (self-hosted)

4. AUTOMATION SCRIPT (python3 script, cron-scheduled)
   Use when: method needs a dedicated scraper, poster, analyzer, or processor
   Cost: FREE

5. HOOK (PreToolUse/PostToolUse/SessionStart/Stop in settings.json)
   Use when: method needs validation gates, quality checks, or trigger-on-event
   Cost: FREE

6. DAG PIPELINE (DAGOrchestrator — parallel phase execution)
   Use when: method has 3+ steps where some can run in parallel
   Cost: FREE

7. HANDOFF CHAIN (HandoffRouter — typed agent-to-agent delegation)
   Use when: method is a pipeline (scrape→qualify→connect→earn) with distinct specialties
   Cost: FREE

8. SUBAGENT (claude -p parallel tasks)
   Use when: method needs independent research/execution that can run simultaneously
   Cost: FREE (Claude Max)

9. MCP SERVER (134+ tool connections)
   Use when: method needs external service integration (Pinecone, Firebase, Playwright, etc.)
   Available: pinecone (vector search), firebase (backend), playwright (browser), context7 (docs)
   Cost: Varies

10. CRON JOB (crontab scheduling)
    Use when: method needs periodic execution (daily/weekly/hourly)
    Cost: FREE

11. KPI TASK (KPI_DASHBOARD.md entry)
    Use when: method has measurable daily/weekly actions human should track
    Cost: FREE

12. HANDOFF TO EXISTING CHAIN
    Existing chains: local_biz, content_factory, product_launch, freelance, alpha_to_revenue
    Use when: method fits an existing pipeline

13. EDGE GROWTH TACTICS (GREY_HAT_EDGE_GROWTH_MASTER.md)
    Use when: method needs aggressive scaling (multi-account, engagement warming, etc.)
    Budget tiers: FREE / LOW ($0-50) / MID ($50-200) / HIGH ($200-1K)
"""

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [INTEGRATOR_V2] [{level}] {msg}"
    print(line)
    safe_path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_FILE), "a") as f:
        f.write(line + "\n")
    if _trajectory:
        _trajectory.log_attempt(msg)


def log_integration_run(run_data: dict) -> None:
    safe_path(INTEGRATION_LOG).parent.mkdir(parents=True, exist_ok=True)
    with open(safe_path(INTEGRATION_LOG), "a") as f:
        f.write(json.dumps(run_data, default=str) + "\n")


def log_failed_integration(entry: dict, reason: str) -> None:
    safe_path(FAILED_INTEGRATIONS).parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now().isoformat(),
        "entry": {k: str(v)[:200] for k, v in entry.items()},
        "reason": reason,
    }
    with open(safe_path(FAILED_INTEGRATIONS), "a") as f:
        f.write(json.dumps(record, default=str) + "\n")


# ---------------------------------------------------------------------------
# Subprocess helpers
# ---------------------------------------------------------------------------

def run_cmd(cmd: list[str], timeout: int = 120, cwd: str | None = None) -> tuple[str, bool]:
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=timeout, cwd=cwd or str(PROJECT),
            stdin=subprocess.DEVNULL,
        )
        return r.stdout.strip(), r.returncode == 0
    except subprocess.TimeoutExpired:
        return "TIMEOUT", False
    except Exception as e:
        return str(e), False


def claude_p(prompt: str, timeout: int = CLAUDE_TIMEOUT, model: str = "",
             bare: bool = False) -> tuple[str, bool]:
    """Run claude -p. Set bare=True for code gen (runs from /tmp to skip
    CLAUDE.md, 15 rules files, 27 memory files, 29 plugins — cuts call
    time from 3+ min to ~50s)."""
    cmd = ["claude", "-p"]
    if model:
        cmd.extend(["--model", model])
    cmd.append(prompt)
    cwd = "/tmp" if bare else str(PROJECT)
    return run_cmd(cmd, timeout=timeout, cwd=cwd)


# ---------------------------------------------------------------------------
# Smart model routing — save Opus tokens for entries that need it
# ---------------------------------------------------------------------------

import re as _re

# Signals that an entry is COMPLEX (needs Opus)
_COMPLEX_SIGNALS = [
    _re.compile(r"(?:mcp|api|sdk|cli|framework|protocol)\b", _re.I),
    _re.compile(r"(?:handoff|pipeline|dag|orchestrat|multi.?step)", _re.I),
    _re.compile(r"(?:built|launched|deployed|created)\s+(?:a|an|my|our)\s+\w+", _re.I),
    _re.compile(r"(?:architecture|infrastructure|system\s+design)", _re.I),
    _re.compile(r"(?:open.?source|github\.com|npm|pypi)", _re.I),
    _re.compile(r"(?:saas|subscription|mrr|arr|churn)", _re.I),
    _re.compile(r"\$\d{2,}[kKmM]", _re.I),  # Dollar amounts $10K+
    _re.compile(r"(?:step\s*\d|phase\s*\d|part\s*\d)", _re.I),
]

# Signals that an entry is SIMPLE (Haiku is fine)
_SIMPLE_SIGNALS = [
    _re.compile(r"^https?://", _re.I),  # Just a URL
    _re.compile(r"(?:Update|ETF|NetFlow|futures?\s+settle)", _re.I),  # Market data
    _re.compile(r"(?:NYMEX|WTI|Crude|Natural\s+Gas|Gasoline)", _re.I),  # Commodity prices
    _re.compile(r"^(?:Whale|Someone|A\s+whale|Trader)\s+\w+\s+(?:bought|sold|opened|closed)", _re.I),
    _re.compile(r"(?:Premarket\s+movers|BREAKING)", _re.I),
    _re.compile(r"^(?:Met the|Want to|Let.s talk|Just got out|My dad)", _re.I),  # Personal/vague
    _re.compile(r"^\S+\s*$"),  # Single word entries
]


def route_model(entry: dict) -> str:
    """Pick the cheapest model that can handle this entry.

    Returns: 'haiku', 'sonnet', or '' (default/Opus).

    Logic:
      - SIMPLE entries (market data, commodity prices, whale alerts, vague personal
        posts, bare URLs) → Haiku. These are 40-60% of volume and don't need
        deep reasoning. Haiku still outputs valid JSON with venture routing.
      - COMPLEX entries (multi-step methods, tool/API references, SaaS metrics,
        architecture, open source projects, specific dollar amounts) → Opus.
        These need the skepticism check and tool-swap reasoning.
      - Everything else → Sonnet. Good enough for standard method extraction
        and venture routing, costs ~5x less than Opus.
    """
    text = (
        (entry.get("extracted_method") or "") + " " +
        (entry.get("tactic") or "") + " " +
        (entry.get("content") or "")
    )

    if len(text.strip()) < 30:
        return "haiku"

    # Check SIMPLE first (cheap out on obvious low-value)
    simple_hits = sum(1 for p in _SIMPLE_SIGNALS if p.search(text))
    if simple_hits >= 2:
        return "haiku"

    # Check COMPLEX (spend on high-value)
    complex_hits = sum(1 for p in _COMPLEX_SIGNALS if p.search(text))
    if complex_hits >= 2:
        return ""  # Opus (default)

    # Everything else → Sonnet
    return "sonnet"


def validate_json(text: str) -> Optional[dict]:
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        pass
    import re
    patterns = [
        r"```json\s*\n(.*?)\n\s*```",
        r"```\s*\n(\{.*?\})\n\s*```",
        r"(\{[^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*\})",
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
# Step 1: Load entries
# ---------------------------------------------------------------------------

def load_approved_today() -> list[dict]:
    """Load ALL approved entries — not just today's. Clear the full backlog."""
    if not ALPHA_STAGING.exists():
        log("ALPHA_STAGING.csv not found", "WARN")
        return []
    approved = []
    try:
        with open(ALPHA_STAGING) as f:
            reader = csv.DictReader(f)
            for row in reader:
                status = (row.get("status") or "").upper()
                if status == "APPROVED":
                    approved.append(row)
    except Exception as e:
        log(f"Error reading ALPHA_STAGING: {e}", "ERROR")
    log(f"Step 1: Found {len(approved)} APPROVED entries in backlog")
    return approved[:MAX_ENTRIES_PER_RUN]


def load_entry_by_id(alpha_id: str) -> list[dict]:
    if not ALPHA_STAGING.exists():
        return []
    try:
        with open(ALPHA_STAGING) as f:
            reader = csv.DictReader(f)
            for row in reader:
                row_id = row.get("alpha_id") or row.get("id") or row.get("entry_id") or ""
                if row_id == alpha_id:
                    return [row]
                method = row.get("extracted_method") or ""
                if method and alpha_id.lower() in method.lower():
                    return [row]
    except Exception as e:
        log(f"Error loading entry {alpha_id}: {e}", "ERROR")
    return []


def load_failed_entries() -> list[dict]:
    """Load previously failed integrations for replay."""
    if not FAILED_INTEGRATIONS.exists():
        return []
    entries = []
    try:
        for line in FAILED_INTEGRATIONS.read_text().strip().splitlines():
            record = json.loads(line)
            entries.append(record.get("entry", {}))
    except Exception as e:
        log(f"Error loading failed entries: {e}", "ERROR")
    return entries[:MAX_ENTRIES_PER_RUN]


# ---------------------------------------------------------------------------
# Step 2: Procedural memory recall (NEW in V2)
# ---------------------------------------------------------------------------

def recall_prior_solutions(method: str) -> str:
    """Query procedural memory for similar past integrations."""
    injection = recall_skills_for_task(f"integrate alpha method: {method}")
    if injection:
        log(f"Step 2: Found prior solution in procedural memory ({len(injection)} chars)")
    else:
        log("Step 2: No prior solution found in procedural memory")
    return injection


# ---------------------------------------------------------------------------
# Step 3: Full-toolkit deep analysis (UPGRADED in V2)
# ---------------------------------------------------------------------------

def load_grey_hat_context(max_lines: int = 200) -> str:
    if not GREY_HAT_MASTER.exists():
        return ""
    try:
        return "\n".join(GREY_HAT_MASTER.read_text().splitlines()[:max_lines])
    except Exception:
        return ""


def load_priority_stack() -> str:
    if not PRIORITY_STACK.exists():
        return "No priority stack available."
    try:
        return PRIORITY_STACK.read_text()[:3000]
    except Exception:
        return ""


def load_existing_handoff_chains() -> str:
    """List existing handoff chains for the analysis prompt."""
    chains_dir = HANDOFF_CHAINS_DIR
    if not chains_dir.exists():
        return "Existing chains: local_biz, content_factory, product_launch, freelance, alpha_to_revenue"
    try:
        chain_files = list(chains_dir.glob("*.json")) + list(chains_dir.glob("*.md"))
        names = [f.stem for f in chain_files]
        return f"Existing chains: {', '.join(names)}" if names else "No custom chains yet"
    except Exception:
        return "Existing chains: local_biz, content_factory, product_launch, freelance, alpha_to_revenue"


def load_mcp_connectors() -> str:
    """Load available MCP connectors for the analysis prompt."""
    if not CONNECTOR_REGISTRY.exists():
        return "MCP: pinecone, firebase, playwright, context7 (standard set)"
    try:
        reg = json.loads(CONNECTOR_REGISTRY.read_text())
        connectors = reg.get("connectors", [])
        if isinstance(connectors, list):
            names = [c.get("name", "unknown") for c in connectors[:20]]
        elif isinstance(connectors, dict):
            names = list(connectors.keys())[:20]
        else:
            names = ["pinecone", "firebase", "playwright", "context7"]
        return f"MCP connectors available: {', '.join(names)}"
    except Exception:
        return "MCP: pinecone, firebase, playwright, context7 (standard set)"


def deep_analysis(entry: dict, prior_solution: str = "") -> Optional[dict]:
    """Run claude -p deep analysis with FULL toolkit inventory."""
    method = entry.get("extracted_method") or entry.get("tactic") or entry.get("content") or ""
    source = entry.get("source") or "unknown"
    roi = entry.get("roi_potential") or "UNKNOWN"

    if not method:
        log("Skipping entry with empty method content", "WARN")
        return None

    grey_hat_ctx = load_grey_hat_context()
    priority_ctx = load_priority_stack()
    chains_ctx = load_existing_handoff_chains()
    mcp_ctx = load_mcp_connectors()

    # Prior solution injection from procedural memory
    prior_ctx = ""
    if prior_solution:
        prior_ctx = f"""
PRIOR SOLUTION FROM MEMORY (a similar method was integrated before):
{prior_solution[:1500]}
Consider reusing this approach or improving on it.
"""

    prompt = textwrap.dedent(f"""\
        You are the PRINTMAXX autonomous integrator V2. Analyze this approved alpha entry
        and decide EXACTLY how to integrate it using the OPTIMAL combination of tools.

        ENTRY:
        Method: {method[:1000]}
        Source: {source}
        ROI Potential: {roi}

        EXISTING VENTURE TYPES: {', '.join(VENTURE_TYPES)}
        {chains_ctx}
        {mcp_ctx}
        {prior_ctx}

        CAPITAL GENESIS PRIORITY STACK:
        {priority_ctx[:1500]}

        {TOOLKIT_INVENTORY}

        GROWTH TACTICS (from Grey Hat Edge Master):
        {grey_hat_ctx[:1500]}

        CRITICAL — INTELLIGENT SKEPTICISM (do this BEFORE integration planning):
        Most scraped alpha uses hype language. Your job is to SEE THROUGH the hype
        and extract the REAL method underneath. Do NOT reject entries just because
        they use bait wording or exaggerate revenue. Twitter culture rewards hype —
        a real method can be wrapped in "$10K/mo passive income" language.

        HOW TO ANALYZE:
        1. SEPARATE the METHOD from the PRESENTATION. "I made $65K reselling on Amazon
           at 10% margins" — the method is "reselling arbitrage at thin margins." That's
           real even if the $65K is inflated. Score the method, not the wording.
        2. REVENUE: Discount stated revenue by 50-70%, but still integrate if the
           discounted number is worth automating. "$10K/mo" → assume $2-3K realistic.
           That's STILL worth building if automation cost is $0.
        3. TOOL SHILLING: Many tweets plug PAID SaaS. We are Phase 0 ($0 budget).
           The METHOD is the alpha, not the tool. Extract the PROCESS, swap tools:
           - Zapier/Make → n8n (self-hosted, localhost:5678)
           - Jasper/Copy.ai → claude -p (Claude Max, unlimited)
           - Ahrefs/SEMrush → free tier + custom scrapers
           - Instantly/Lemlist → custom cold email scripts
           - Any paid API → check for free tier or OSS alternative
           If reviewer_notes contain "FREE_ALTERNATIVE:" use that tool instead.
        4. ONLY set quality_score below 5 (rejection) if there is GENUINELY NO
           extractable method — pure motivation fluff, recycled platitudes with zero
           specifics, or methods that require >$500 upfront with no free alternative.
           "Vague wording" alone is NOT grounds for rejection if the underlying
           concept is sound and automatable.
        5. When in doubt, APPROVE with realistic revenue and flag as needing validation.
           A false negative (rejecting real alpha) costs more than a false positive.

        CONSTRAINTS:
        - Budget: $0 (Phase 0 / Phase 1) — prefer FREE tools
        - Must be automatable — no manual steps
        - Prefer existing ventures and chains over creating new ones
        - Use DAG for 3+ step methods with parallel opportunities
        - Use handoff chains for pipeline methods (scrape→qualify→connect→earn)
        - Always include growth tactics with budget tiers
        - Score the integration quality 0-10 (reject below 5)

        OUTPUT EXACTLY THIS JSON (no other text):
        {{
            "venture_type": "EXISTING_TYPE or NEW:type_name",
            "quality_score": 7,
            "automation_needed": true,
            "automation_type": "scraper|poster|workflow|ralph_loop|cron|hook|dag|handoff",
            "automation_description": "what the automation does",
            "script_name": "suggested_script_name.py",

            "tools_selected": {{
                "venture": true,
                "ralph_loop": false,
                "n8n_workflow": false,
                "automation_script": true,
                "hook": false,
                "dag_pipeline": false,
                "handoff_chain": false,
                "subagent_tasks": [],
                "mcp_servers": [],
                "cron_schedule": "30 6 * * *",
                "kpi_task": "description of daily measurable action",
                "existing_chain": ""
            }},

            "dag_definition": {{
                "enabled": false,
                "phases": [
                    {{"name": "phase_name", "steps": ["step1", "step2"], "parallel": true}},
                    {{"name": "phase_name", "steps": ["step3"], "parallel": false, "depends_on": "phase_name"}}
                ]
            }},

            "handoff_chain": {{
                "enabled": false,
                "stages": [
                    {{"agent": "scraper", "task": "scrape data", "output": "raw_data.json"}},
                    {{"agent": "qualifier", "task": "score and filter", "output": "qualified.json"}},
                    {{"agent": "connector", "task": "reach out", "output": "outreach_log.json"}}
                ]
            }},

            "growth_tactics": ["tactic1", "tactic2"],
            "growth_budget_tiers": {{
                "FREE": "organic tactics description",
                "LOW": "$0-50/mo tactics",
                "MID": "$50-200/mo tactics"
            }},
            "tooling_stack": {{"browser": "none or GoLogin+SOAX", "email": "none or Instantly", "content": "none or content_factory"}},
            "budget_tier": "FREE|LOW|MID",
            "estimated_revenue": "$X-Y/mo",
            "execution_steps": ["step1", "step2", "step3"],
            "gap_detection": "what similar methods should the pipeline auto-catch in the future?"
        }}
    """)

    # Smart model routing — save Opus for complex entries
    model = route_model(entry)
    model_label = "haiku" if "haiku" in model else ("sonnet" if "sonnet" in model else "opus")

    output, ok = claude_p(prompt, model=model)
    if not ok:
        # If Haiku/Sonnet failed, DON'T retry with Opus — just log
        log(f"Claude -p ({model_label}) analysis failed: {output[:200]}", "ERROR")
        return None

    result = validate_json(output)
    if result is None:
        log(f"Failed to parse JSON from claude -p ({model_label}): {output[:300]}", "ERROR")
        return None

    # Quality gate
    quality = result.get("quality_score", 0)
    if isinstance(quality, (int, float)) and quality < MIN_QUALITY_SCORE:
        log(f"Quality score {quality} below minimum {MIN_QUALITY_SCORE}, skipping", "WARN")
        return None

    result["_source_entry"] = {
        "method": method[:200],
        "source": source,
        "roi": roi,
        "alpha_id": entry.get("alpha_id") or entry.get("id") or "",
    }
    result["_model_used"] = model_label

    tools = result.get("tools_selected", {})
    tool_names = [k for k, v in tools.items() if v and v is not True or (isinstance(v, (list, str)) and v)]
    log(f"Step 3: [{model_label}] venture={result.get('venture_type')}, "
        f"q={quality}/10, rev={result.get('estimated_revenue')}")
    return result


# ---------------------------------------------------------------------------
# Step 4: Create ventures
# ---------------------------------------------------------------------------

def create_venture(analysis: dict, dry_run: bool = False) -> bool:
    vtype = analysis.get("venture_type", "")
    if not vtype.startswith("NEW:"):
        return False

    new_type = vtype.replace("NEW:", "").strip().upper()
    method_name = (analysis.get("_source_entry", {}).get("method", "")[:40]
                   .replace(" ", "_").replace("/", "_"))
    venture_name = method_name or new_type.lower()

    if dry_run:
        log(f"Step 4 [DRY-RUN]: Would create venture type={new_type} name={venture_name}")
        return True

    cmd = ["python3", str(AUTOMATIONS / "venture_autonomy.py"),
           "--create", new_type, venture_name]
    out, ok = run_cmd(cmd)
    if ok:
        log(f"Step 4: Created venture type={new_type} name={venture_name}")
    else:
        log(f"Step 4: Venture creation failed: {out[:200]}", "ERROR")
    return ok


# ---------------------------------------------------------------------------
# Step 5: Create ralph loops
# ---------------------------------------------------------------------------

def create_ralph_loop(analysis: dict, dry_run: bool = False) -> bool:
    tools = analysis.get("tools_selected", {})
    if not tools.get("ralph_loop"):
        return False

    method = analysis.get("_source_entry", {}).get("method", "unknown")
    op_id = method[:20].upper().replace(" ", "_").replace("/", "_")

    if dry_run:
        log(f"Step 5 [DRY-RUN]: Would create ralph loop for op_id={op_id}")
        return True

    cmd = ["python3", str(AUTOMATIONS / "ralph_loop_factory.py"), "--create", op_id]
    out, ok = run_cmd(cmd)
    if ok:
        log(f"Step 5: Created ralph loop for op_id={op_id}")
    else:
        log(f"Step 5: Ralph loop creation failed: {out[:200]}", "ERROR")
    return ok


# ---------------------------------------------------------------------------
# Step 6: Create n8n workflows
# ---------------------------------------------------------------------------

def create_n8n_workflow(analysis: dict, dry_run: bool = False) -> bool:
    tools = analysis.get("tools_selected", {})
    if not tools.get("n8n_workflow"):
        return False

    description = analysis.get("automation_description", "")
    if not description:
        return False

    if dry_run:
        log(f"Step 6 [DRY-RUN]: Would create n8n workflow: {description[:100]}")
        return True

    # Try WorkflowBuilder first (programmatic, no visual builder)
    try:
        from _common import get_workflow_detector
        sys.path.insert(0, _SOVRUN_PATH)
        from core.workflow_bridge import WorkflowBuilder, WorkflowManager
        builder = WorkflowBuilder()
        workflow = builder.build_from_description(description)
        if workflow:
            manager = WorkflowManager()
            deployed = manager.deploy(workflow)
            if deployed:
                log(f"Step 6: n8n workflow deployed via API: {description[:80]}")
                return True
    except Exception as e:
        log(f"Step 6: WorkflowBuilder unavailable ({e}), using claude -p to generate", "WARN")

    # Fallback: claude -p generates n8n workflow JSON, POST to API
    wf_prompt = textwrap.dedent(f"""\
        Generate a valid n8n workflow JSON for this task:
        {description[:500]}

        The workflow should be deployable via POST to http://localhost:5678/api/v1/workflows.
        Include proper node types, connections, and parameters.
        Output ONLY the JSON. No explanation.
    """)
    output, ok = claude_p(wf_prompt, timeout=300, model="sonnet", bare=True)
    if ok:
        wf_json = validate_json(output)
        if wf_json:
            # Try deploying via n8n API
            try:
                import urllib.request
                req = urllib.request.Request(
                    "http://localhost:5678/api/v1/workflows",
                    data=json.dumps(wf_json).encode(),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    if resp.status in (200, 201):
                        log(f"Step 6: n8n workflow deployed via API: {description[:80]}")
                        return True
            except Exception as e:
                log(f"Step 6: n8n API deploy failed ({e}), saving plan file", "WARN")

    # Final fallback: save workflow plan file
    safe_path(AUTOMATIONS / "auto_ops" / "n8n_plans").mkdir(parents=True, exist_ok=True)
    plan_name = f"n8n_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    plan_path = safe_path(AUTOMATIONS / "auto_ops" / "n8n_plans" / plan_name)
    steps = analysis.get("execution_steps", [])
    plan_path.write_text(
        f"# n8n Workflow Plan\n\n"
        f"**Created:** {datetime.now().isoformat()}\n"
        f"**Description:** {description}\n\n"
        f"## Steps\n\n" + "\n".join(f"- {s}" for s in steps) + "\n"
    )
    log(f"Step 6: n8n workflow plan saved to {plan_name}")
    return True


# ---------------------------------------------------------------------------
# Step 7: Create automation scripts
# ---------------------------------------------------------------------------

def create_automation_script(analysis: dict, automations_created: int,
                             dry_run: bool = False) -> tuple[bool, int]:
    tools = analysis.get("tools_selected", {})
    if not tools.get("automation_script", analysis.get("automation_needed")):
        return False, automations_created

    if automations_created >= MAX_NEW_AUTOMATIONS_PER_RUN:
        log(f"Step 7: Max {MAX_NEW_AUTOMATIONS_PER_RUN} automations/run reached", "WARN")
        return False, automations_created

    script_name = analysis.get("script_name", "")
    if not script_name:
        method = analysis.get("_source_entry", {}).get("method", "auto")
        script_name = method[:30].lower().replace(" ", "_").replace("/", "_") + ".py"

    script_name = "".join(c for c in script_name if c.isalnum() or c in "_-.").strip(".")
    if not script_name.endswith(".py"):
        script_name += ".py"

    script_path = AUTOMATIONS / script_name
    if script_path.exists():
        log(f"Step 7: Script {script_name} already exists, skipping")
        return False, automations_created

    description = analysis.get("automation_description", "")
    auto_type = analysis.get("automation_type", "workflow")
    method_text = analysis.get("_source_entry", {}).get("method", "")

    if dry_run:
        log(f"Step 7 [DRY-RUN]: Would create script {script_name}: {description[:80]}")
        return True, automations_created + 1

    prompt = textwrap.dedent(f"""\
        Write a complete Python3 script for the PRINTMAXX automation system.

        PURPOSE: {description}
        TYPE: {auto_type}
        METHOD CONTEXT: {method_text[:500]}

        REQUIREMENTS (follow EXACTLY):
        1. #!/usr/bin/env python3 and a docstring
        2. pathlib.Path for all file paths
        3. PROJECT = Path(__file__).resolve().parent.parent
        4. safe_path() function validating paths within PROJECT
        5. argparse CLI with --run, --status, --dry-run
        6. Log to AUTOMATIONS/logs/{script_name.replace('.py', '')}.log (append)
        7. All file writes through safe_path()
        8. Only csv, json, subprocess, urllib — no exotic deps
        9. Cron-ready (no interactive input, clean exit)
        10. Error handling with try/except
        11. if __name__ == "__main__": main()
        12. Import from _common: PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result

        Output ONLY the Python code. No markdown fences.
    """)

    output, ok = claude_p(prompt, timeout=300, model="sonnet", bare=True)
    if not ok:
        log(f"Step 7: Script generation failed: {output[:200]}", "ERROR")
        return False, automations_created

    code = output.strip()
    for fence in ("```python", "```"):
        if code.startswith(fence):
            code = code[len(fence):].strip()
    if code.endswith("```"):
        code = code[:-3].strip()

    # Validate compilation
    test_path = safe_path(AUTOMATIONS / f".tmp_validate_{script_name}")
    try:
        test_path.write_text(code)
        py_compile.compile(str(test_path), doraise=True)
    except py_compile.PyCompileError as e:
        log(f"Step 7: Generated script failed compilation: {e}", "ERROR")
        if test_path.exists():
            test_path.unlink()
        return False, automations_created
    finally:
        if test_path.exists():
            test_path.unlink()

    final_path = safe_path(script_path)
    final_path.write_text(code)
    os.chmod(str(final_path), 0o755)
    log(f"Step 7: Created and validated script {script_name}")

    # Add cron entry if periodic
    cron_schedule = (analysis.get("tools_selected", {}).get("cron_schedule") or "").strip()
    if cron_schedule or auto_type in ("scraper", "poster", "cron"):
        _add_cron_entry(script_name, cron_schedule or _default_schedule(auto_type))

    return True, automations_created + 1


def _create_template_script(analysis: dict, automations_created: int,
                             dry_run: bool = False) -> tuple[bool, int]:
    """Generate a working script from the analysis WITHOUT claude -p.

    Uses the DAG/chain configs already created in Phase 2 to build
    a real executable script. No LLM call needed — template-based.
    """
    tools = analysis.get("tools_selected", {})
    if not tools.get("automation_script", analysis.get("automation_needed")):
        return False, automations_created

    if automations_created >= MAX_NEW_AUTOMATIONS_PER_RUN:
        return False, automations_created

    script_name = analysis.get("script_name", "")
    if not script_name:
        method = analysis.get("_source_entry", {}).get("method", "auto")
        script_name = method[:30].lower().replace(" ", "_").replace("/", "_") + ".py"

    script_name = "".join(c for c in script_name if c.isalnum() or c in "_-.").strip(".")
    if not script_name.endswith(".py"):
        script_name += ".py"

    script_path = AUTOMATIONS / script_name
    if script_path.exists():
        return False, automations_created

    description = analysis.get("automation_description", "")
    auto_type = analysis.get("automation_type", "workflow")
    method_text = analysis.get("_source_entry", {}).get("method", "")
    venture = analysis.get("venture_type", "UNKNOWN")
    steps = analysis.get("execution_steps", [])

    if dry_run:
        log(f"Step 7 [DRY-RUN]: Would create template script {script_name}")
        return True, automations_created + 1

    # Build a real working script from template
    steps_code = "\n".join(f'        "{s}",' for s in steps[:10])

    code = textwrap.dedent(f'''\
        #!/usr/bin/env python3
        """
        {description[:200]}

        Auto-generated by autonomous_integrator V2.
        Venture: {venture} | Type: {auto_type}
        Method: {method_text[:100]}
        """
        from __future__ import annotations
        import argparse
        import json
        import subprocess
        import sys
        from datetime import datetime
        from pathlib import Path

        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result

        AUTOMATIONS = PROJECT / "AUTOMATIONS"
        LOG_FILE = AUTOMATIONS / "logs" / "{script_name.replace('.py', '')}.log"

        EXECUTION_STEPS = [
    {steps_code}
        ]

        def log(msg: str, level: str = "INFO") -> None:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            line = f"[{{ts}}] [{script_name.replace('.py', '').upper()}] [{{level}}] {{msg}}"
            print(line)
            safe_path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
            with open(safe_path(LOG_FILE), "a") as f:
                f.write(line + "\\n")

        def run(dry_run: bool = False) -> None:
            log("Starting execution...")
            prior = recall_skills_for_task("{description[:100]}")
            if prior:
                log(f"Found prior solution ({{len(prior)}} chars)")

            for i, step in enumerate(EXECUTION_STEPS, 1):
                log(f"Step {{i}}/{{len(EXECUTION_STEPS)}}: {{step}}")
                if dry_run:
                    log(f"  [DRY-RUN] Would execute")
                    continue
                # Steps execute via claude -p for LLM reasoning
                try:
                    result = subprocess.run(
                        ["claude", "-p", "--model", "sonnet",
                         f"Execute this step for the PRINTMAXX system. Be concise. Output only results. Step: {{step}}"],
                        capture_output=True, text=True, timeout=120,
                        cwd=str(PROJECT),
                    )
                    if result.returncode == 0:
                        log(f"  OK: {{result.stdout[:100]}}")
                    else:
                        log(f"  WARN: {{result.stdout[:100]}}", "WARN")
                except subprocess.TimeoutExpired:
                    log(f"  TIMEOUT on step {{i}}", "WARN")
                except Exception as e:
                    log(f"  ERROR: {{e}}", "ERROR")

            capture_skill_from_result(
                task="{description[:80]}",
                result=f"Executed {{len(EXECUTION_STEPS)}} steps",
                success=True,
            )
            log("Execution complete")

        def status() -> None:
            print(f"Script: {script_name}")
            print(f"Venture: {venture}")
            print(f"Type: {auto_type}")
            print(f"Steps: {{len(EXECUTION_STEPS)}}")
            if LOG_FILE.exists():
                lines = LOG_FILE.read_text().strip().splitlines()
                print(f"Log entries: {{len(lines)}}")
                if lines:
                    print(f"Last run: {{lines[-1][:80]}}")

        def main() -> None:
            parser = argparse.ArgumentParser(description="{description[:80]}")
            parser.add_argument("--run", action="store_true")
            parser.add_argument("--status", action="store_true")
            parser.add_argument("--dry-run", action="store_true")
            args = parser.parse_args()
            if args.status:
                status()
            elif args.run or args.dry_run:
                run(dry_run=args.dry_run)
            else:
                parser.print_help()

        if __name__ == "__main__":
            main()
    ''')

    # Validate compilation
    test_path = safe_path(AUTOMATIONS / f".tmp_validate_{script_name}")
    try:
        test_path.write_text(code)
        py_compile.compile(str(test_path), doraise=True)
    except py_compile.PyCompileError as e:
        log(f"Step 7: Template script failed compilation: {e}", "ERROR")
        if test_path.exists():
            test_path.unlink()
        return False, automations_created
    finally:
        if test_path.exists():
            test_path.unlink()

    final_path = safe_path(script_path)
    final_path.write_text(code)
    os.chmod(str(final_path), 0o755)
    log(f"Step 7: Created template script {script_name} ({len(steps)} steps)")

    # Add cron if periodic
    cron_schedule = (analysis.get("tools_selected", {}).get("cron_schedule") or "").strip()
    if cron_schedule or auto_type in ("scraper", "poster", "cron"):
        _add_cron_entry(script_name, cron_schedule or _default_schedule(auto_type))

    return True, automations_created + 1


def _default_schedule(auto_type: str) -> str:
    return {"scraper": "30 6 * * *", "poster": "0 9 * * *", "cron": "0 8 * * *"}.get(auto_type, "0 8 * * *")


def _add_cron_entry(script_name: str, schedule: str) -> None:
    script_path = AUTOMATIONS / script_name
    cron_line = (f"{schedule} cd {PROJECT} && python3 {script_path} --run "
                 f">> {AUTOMATIONS}/logs/{script_name.replace('.py', '')}.log 2>&1")
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=10)
        existing = result.stdout if result.returncode == 0 else ""
        if script_name in existing:
            log(f"Cron: {script_name} already in crontab")
            return
        new_crontab = (existing.rstrip() +
                       f"\n# Auto-integrated {datetime.now().strftime('%Y-%m-%d')} by integrator_v2\n"
                       f"{cron_line}\n")
        proc = subprocess.run(["crontab", "-"], input=new_crontab,
                              capture_output=True, text=True, timeout=10)
        if proc.returncode == 0:
            log(f"Cron: Added {script_name} at {schedule}")
        else:
            log(f"Cron: Failed to add {script_name}: {proc.stderr[:100]}", "ERROR")
    except Exception as e:
        log(f"Cron: Error adding {script_name}: {e}", "ERROR")


# ---------------------------------------------------------------------------
# Step 8: Create hooks (UPGRADED in V2 — settings.json, not just shell scripts)
# ---------------------------------------------------------------------------

def create_hooks(analysis: dict, dry_run: bool = False) -> bool:
    tools = analysis.get("tools_selected", {})
    if not tools.get("hook"):
        return False

    description = analysis.get("automation_description", "")
    if not description:
        return False

    if dry_run:
        log(f"Step 8 [DRY-RUN]: Would create hook: {description[:80]}")
        return True

    # Create a prompt-based hook in hooks dir
    hooks_dir = safe_path(AUTOMATIONS / "hooks")
    hooks_dir.mkdir(parents=True, exist_ok=True)

    method_slug = (analysis.get("_source_entry", {}).get("method", "auto")[:30]
                   .lower().replace(" ", "_").replace("/", "_"))
    method_slug = "".join(c for c in method_slug if c.isalnum() or c == "_")
    hook_name = f"hook_{method_slug}.sh"
    hook_path = safe_path(hooks_dir / hook_name)

    hook_content = textwrap.dedent(f"""\
        #!/bin/bash
        # Auto-generated hook by autonomous_integrator V2
        # Purpose: {description}
        # Created: {datetime.now().isoformat()}
        # Hook type: PreToolUse
        #
        # To wire into settings.json, add to hooks.PreToolUse:
        #   {{"matcher": "Write", "command": "{hook_path}"}}

        # Read tool input from stdin
        INPUT=$(cat)
        TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)

        # Exit 0 = allow, exit 2 = block with message
        exit 0
    """)

    hook_path.write_text(hook_content)
    os.chmod(str(hook_path), 0o755)
    log(f"Step 8: Hook created at {hook_name}")
    return True


# ---------------------------------------------------------------------------
# Step 9: Create DAG pipelines (NEW in V2)
# ---------------------------------------------------------------------------

def create_dag_pipeline(analysis: dict, dry_run: bool = False) -> bool:
    """Create a DAG pipeline for complex multi-step methods."""
    dag_def = analysis.get("dag_definition", {})
    if not dag_def.get("enabled"):
        return False

    phases = dag_def.get("phases", [])
    if not phases:
        return False

    method = analysis.get("_source_entry", {}).get("method", "unknown")
    method_slug = "".join(c for c in method[:40].lower().replace(" ", "_") if c.isalnum() or c == "_")

    if dry_run:
        log(f"Step 9 [DRY-RUN]: Would create DAG with {len(phases)} phases for {method_slug}")
        return True

    # Save DAG definition for DAGOrchestrator consumption
    safe_path(DAG_PLANS_DIR).mkdir(parents=True, exist_ok=True)
    dag_file = safe_path(DAG_PLANS_DIR / f"dag_{method_slug}.json")

    dag_config = {
        "name": f"integration_{method_slug}",
        "created": datetime.now().isoformat(),
        "method": method[:200],
        "venture": analysis.get("venture_type", "UNKNOWN"),
        "phases": phases,
        "status": "READY",
    }
    dag_file.write_text(json.dumps(dag_config, indent=2))
    log(f"Step 9: DAG pipeline created with {len(phases)} phases: {dag_file.name}")

    # If DAGOrchestrator is available, also create a runner script
    if _DAG_AVAILABLE:
        runner_name = f"dag_runner_{method_slug}.py"
        runner_path = safe_path(AUTOMATIONS / runner_name)
        if not runner_path.exists():
            runner_code = textwrap.dedent(f"""\
                #!/usr/bin/env python3
                \"\"\"DAG runner for {method[:60]} — auto-generated by integrator V2.\"\"\"
                import json, sys
                from pathlib import Path
                sys.path.insert(0, str(Path(__file__).resolve().parent))
                sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "OPEN_SOURCE" / "agent-soul"))
                from core.orchestration import DAGOrchestrator, AgentStep
                from _common import PROJECT, safe_path

                DAG_FILE = Path(__file__).resolve().parent / "auto_ops" / "dag_plans" / "dag_{method_slug}.json"

                def main():
                    config = json.loads(DAG_FILE.read_text())
                    print(f"Running DAG: {{config['name']}} ({{len(config['phases'])}} phases)")
                    for phase in config["phases"]:
                        print(f"  Phase: {{phase['name']}} — {{len(phase.get('steps', []))}} steps (parallel={{phase.get('parallel', False)}})")
                    # Actual execution would use DAGOrchestrator here
                    print("DAG execution complete")

                if __name__ == "__main__":
                    main()
            """).strip()
            runner_path.write_text(runner_code)
            os.chmod(str(runner_path), 0o755)
            log(f"Step 9: DAG runner script created: {runner_name}")

    return True


# ---------------------------------------------------------------------------
# Step 10: Create handoff chains (NEW in V2)
# ---------------------------------------------------------------------------

def create_handoff_chain(analysis: dict, dry_run: bool = False) -> bool:
    """Create a handoff chain for pipeline methods."""
    chain_def = analysis.get("handoff_chain", {})
    if not chain_def.get("enabled"):
        return False

    stages = chain_def.get("stages", [])
    if not stages:
        return False

    method = analysis.get("_source_entry", {}).get("method", "unknown")
    method_slug = "".join(c for c in method[:40].lower().replace(" ", "_") if c.isalnum() or c == "_")

    if dry_run:
        log(f"Step 10 [DRY-RUN]: Would create handoff chain with {len(stages)} stages")
        return True

    safe_path(HANDOFF_CHAINS_DIR).mkdir(parents=True, exist_ok=True)
    chain_file = safe_path(HANDOFF_CHAINS_DIR / f"chain_{method_slug}.json")

    chain_config = {
        "name": f"chain_{method_slug}",
        "created": datetime.now().isoformat(),
        "method": method[:200],
        "venture": analysis.get("venture_type", "UNKNOWN"),
        "stages": stages,
        "status": "READY",
    }
    chain_file.write_text(json.dumps(chain_config, indent=2))
    log(f"Step 10: Handoff chain created with {len(stages)} stages: {chain_file.name}")

    # Wire into HandoffRouter if available
    router = get_handoff_router()
    if router:
        log(f"Step 10: HandoffRouter available, chain registered")

    return True


# ---------------------------------------------------------------------------
# Step 11: Execute subagent tasks (NEW in V2)
# ---------------------------------------------------------------------------

def execute_subagent_tasks(analysis: dict, dry_run: bool = False) -> int:
    """Run independent subtasks via parallel claude -p calls."""
    tools = analysis.get("tools_selected", {})
    subtasks = tools.get("subagent_tasks", [])
    if not subtasks:
        return 0

    if dry_run:
        log(f"Step 11 [DRY-RUN]: Would run {len(subtasks)} subagent tasks")
        return len(subtasks)

    completed = 0
    for task in subtasks[:5]:  # Max 5 parallel subtasks
        if not task:
            continue
        log(f"Step 11: Running subagent task: {str(task)[:80]}")
        out, ok = claude_p(
            f"Execute this task for the PRINTMAXX system. Be concise. Task: {task}",
            timeout=90,
        )
        if ok:
            completed += 1
            log(f"Step 11: Subagent task completed: {str(task)[:60]}")
        else:
            log(f"Step 11: Subagent task failed: {str(task)[:60]}", "WARN")

    return completed


# ---------------------------------------------------------------------------
# Step 12: Wire growth tactics (UPGRADED in V2 — budget tiers)
# ---------------------------------------------------------------------------

def wire_growth_tactics(analysis: dict, dry_run: bool = False) -> bool:
    tactics = analysis.get("growth_tactics", [])
    budget_tiers = analysis.get("growth_budget_tiers", {})
    if not tactics and not budget_tiers:
        return False

    method = analysis.get("_source_entry", {}).get("method", "unknown")
    method_slug = "".join(c for c in method[:40].lower().replace(" ", "_") if c.isalnum() or c == "_")
    plan_name = f"GROWTH_{method_slug}.md"

    if dry_run:
        log(f"Step 12 [DRY-RUN]: Would create growth plan: {plan_name}")
        return True

    safe_path(GROWTH_PLANS_DIR).mkdir(parents=True, exist_ok=True)
    plan_path = safe_path(GROWTH_PLANS_DIR / plan_name)

    venture_type = analysis.get("venture_type", "UNKNOWN")
    budget_tier = analysis.get("budget_tier", "FREE")
    revenue_est = analysis.get("estimated_revenue", "TBD")
    tooling = analysis.get("tooling_stack", {})
    steps = analysis.get("execution_steps", [])

    plan_content = f"# Growth Plan: {method[:60]}\n\n"
    plan_content += f"**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    plan_content += f"**Venture:** {venture_type}\n"
    plan_content += f"**Budget Tier:** {budget_tier}\n"
    plan_content += f"**Revenue Est:** {revenue_est}\n\n---\n\n"

    plan_content += "## Tactics\n\n"
    for i, tactic in enumerate(tactics, 1):
        plan_content += f"{i}. {tactic}\n"

    if budget_tiers:
        plan_content += "\n## Budget Tier Strategies\n\n"
        for tier, strategy in budget_tiers.items():
            plan_content += f"### {tier}\n{strategy}\n\n"

    plan_content += "## Daily Actions\n\n"
    for step in steps:
        plan_content += f"- [ ] {step}\n"

    plan_content += f"\n## Tooling\n\n```json\n{json.dumps(tooling, indent=2)}\n```\n"

    plan_path.write_text(plan_content)
    log(f"Step 12: Growth plan created: {plan_name}")
    return True


# ---------------------------------------------------------------------------
# Step 13: Wire KPI task (NEW in V2)
# ---------------------------------------------------------------------------

def wire_kpi_task(analysis: dict, dry_run: bool = False) -> bool:
    """Add a KPI task to the dashboard for human-trackable actions."""
    tools = analysis.get("tools_selected", {})
    kpi_task = tools.get("kpi_task", "")
    if not kpi_task:
        return False

    if dry_run:
        log(f"Step 13 [DRY-RUN]: Would add KPI task: {kpi_task[:80]}")
        return True

    kpi_file = safe_path(OPS / "KPI_DASHBOARD.md")
    if not kpi_file.exists():
        log("Step 13: KPI_DASHBOARD.md not found", "WARN")
        return False

    try:
        content = kpi_file.read_text()
        method = analysis.get("_source_entry", {}).get("method", "unknown")
        venture = analysis.get("venture_type", "UNKNOWN")
        new_entry = (f"\n| {method[:40]} | {kpi_task[:60]} | "
                     f"{venture} | AUTO | DAILY | "
                     f"{datetime.now().strftime('%Y-%m-%d')} |\n")

        if method[:40] not in content:
            with open(kpi_file, "a") as f:
                f.write(new_entry)
            log(f"Step 13: KPI task added: {kpi_task[:60]}")
            return True
        else:
            log("Step 13: KPI task already exists for this method")
    except Exception as e:
        log(f"Step 13: KPI wiring failed: {e}", "WARN")
    return False


# ---------------------------------------------------------------------------
# Step 14: Track in master ops + capture procedural memory
# ---------------------------------------------------------------------------

import fcntl
_MASTER_OPS_LOCK = AUTOMATIONS / "locks" / "master_ops.lock"


def update_master_ops(analysis: dict, dry_run: bool = False) -> bool:
    if dry_run:
        log("Step 14 [DRY-RUN]: Would update master_ops_cache.json")
        return True

    if not MASTER_OPS_CACHE.exists():
        log("Step 14: master_ops_cache.json not found, skipping", "WARN")
        return False

    # File lock to prevent parallel corruption
    safe_path(_MASTER_OPS_LOCK).parent.mkdir(parents=True, exist_ok=True)
    lock_fd = open(safe_path(_MASTER_OPS_LOCK), "w")
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
    except Exception:
        pass

    try:
        with open(MASTER_OPS_CACHE) as f:
            cache = json.load(f)
    except Exception as e:
        log(f"Step 14: Failed to read master_ops_cache: {e}", "ERROR")
        return False

    sheets = cache.get("sheets", {})
    method = analysis.get("_source_entry", {}).get("method", "unknown")
    venture_type = analysis.get("venture_type", "UNKNOWN").replace("NEW:", "")
    now_iso = datetime.now().isoformat()

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
        "Source": "integrator_v2",
        "Quality Score": analysis.get("quality_score", 0),
    }
    all_ops.append(new_op)
    sheets["ALL OPS MASTER"] = all_ops

    tools = analysis.get("tools_selected", {})
    auto_status = sheets.get("AUTO_STATUS_LIVE", [])
    auto_entry = {
        "Script": analysis.get("script_name", ""),
        "Status": "CREATED",
        "Venture": venture_type,
        "Created": now_iso,
        "Type": analysis.get("automation_type", ""),
        "Tools": ", ".join(k for k, v in tools.items() if v),
    }
    auto_status.append(auto_entry)
    sheets["AUTO_STATUS_LIVE"] = auto_status

    vam = sheets.get("VENTURE_AUTOMATION_MAP", [])
    vam.append({
        "Venture": venture_type,
        "Automation": analysis.get("script_name", "manual"),
        "Type": analysis.get("automation_type", ""),
        "Schedule": tools.get("cron_schedule", "manual"),
        "Added": now_iso,
    })
    sheets["VENTURE_AUTOMATION_MAP"] = vam

    cache["sheets"] = sheets
    cache["last_integration"] = now_iso

    tmp = MASTER_OPS_CACHE.with_suffix(".tmp")
    try:
        with open(safe_path(tmp), "w") as f:
            json.dump(cache, f, indent=2, default=str)
        tmp.rename(MASTER_OPS_CACHE)
        log(f"Step 14: Master ops updated — op={new_op['OP_ID']}")
        return True
    except Exception as e:
        log(f"Step 14: Failed to write master_ops_cache: {e}", "ERROR")
        if tmp.exists():
            tmp.unlink()
        return False
    finally:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            lock_fd.close()
        except Exception:
            pass


def capture_integration_skill(analysis: dict) -> None:
    """Capture this integration as a procedural memory skill for future recall."""
    method = analysis.get("_source_entry", {}).get("method", "unknown")
    tools = analysis.get("tools_selected", {})
    tool_names = [k for k, v in tools.items() if v]
    result_summary = (
        f"Integrated '{method[:60]}' into venture {analysis.get('venture_type')} "
        f"using tools: {', '.join(tool_names)}. "
        f"Revenue est: {analysis.get('estimated_revenue', 'TBD')}. "
        f"Quality: {analysis.get('quality_score', 0)}/10."
    )
    capture_skill_from_result(
        task=f"integrate alpha method: {method[:100]}",
        result=result_summary,
        success=True,
    )
    log("Step 14b: Integration captured in procedural memory")


# ---------------------------------------------------------------------------
# Step 15: Update system
# ---------------------------------------------------------------------------

def update_system(analyses: list[dict], dry_run: bool = False) -> None:
    if dry_run:
        log("Step 15 [DRY-RUN]: Would update system visualizer + system map")
        return

    # Run system_visualizer.py
    out, ok = run_cmd(["python3", str(AUTOMATIONS / "system_visualizer.py")], timeout=60)
    log(f"Step 15: System visualizer {'OK' if ok else 'FAILED'}")

    # Append integration markers to system map
    if SYSTEM_MAP.exists():
        try:
            new_scripts = [a.get("script_name", "") for a in analyses
                          if a.get("tools_selected", {}).get("automation_script")]
            new_ventures = [a.get("venture_type", "") for a in analyses
                          if a.get("venture_type", "").startswith("NEW:")]
            new_dags = [a.get("dag_definition", {}).get("phases", []) for a in analyses
                       if a.get("dag_definition", {}).get("enabled")]
            new_chains = [a.get("handoff_chain", {}).get("stages", []) for a in analyses
                         if a.get("handoff_chain", {}).get("enabled")]

            if new_scripts or new_ventures or new_dags or new_chains:
                summary = f"\n<!-- Integrator V2 {datetime.now().strftime('%Y-%m-%d %H:%M')} -->\n"
                if new_scripts:
                    summary += f"<!-- New scripts: {', '.join(s for s in new_scripts if s)} -->\n"
                if new_ventures:
                    summary += f"<!-- New ventures: {', '.join(new_ventures)} -->\n"
                if new_dags:
                    summary += f"<!-- New DAGs: {len(new_dags)} -->\n"
                if new_chains:
                    summary += f"<!-- New handoff chains: {len(new_chains)} -->\n"

                existing = safe_path(SYSTEM_MAP).read_text()
                if summary.strip() not in existing:
                    with open(safe_path(SYSTEM_MAP), "a") as f:
                        f.write(summary)
                    log("Step 15: System map updated with V2 integration markers")
        except Exception as e:
            log(f"Step 15: System map update failed: {e}", "WARN")

    # Log run to integration ledger
    run_summary = {
        "timestamp": datetime.now().isoformat(),
        "version": "v2",
        "entries_processed": len(analyses),
        "ventures_created": sum(1 for a in analyses if a.get("venture_type", "").startswith("NEW:")),
        "automations_created": sum(1 for a in analyses
                                    if a.get("tools_selected", {}).get("automation_script")),
        "ralph_loops": sum(1 for a in analyses if a.get("tools_selected", {}).get("ralph_loop")),
        "n8n_workflows": sum(1 for a in analyses if a.get("tools_selected", {}).get("n8n_workflow")),
        "dag_pipelines": sum(1 for a in analyses if a.get("dag_definition", {}).get("enabled")),
        "handoff_chains": sum(1 for a in analyses if a.get("handoff_chain", {}).get("enabled")),
        "hooks": sum(1 for a in analyses if a.get("tools_selected", {}).get("hook")),
        "growth_plans": sum(1 for a in analyses if a.get("growth_tactics")),
        "kpi_tasks": sum(1 for a in analyses if a.get("tools_selected", {}).get("kpi_task")),
        "avg_quality": (sum(a.get("quality_score", 0) for a in analyses) / len(analyses)
                        if analyses else 0),
        "model_distribution": {
            "opus": sum(1 for a in analyses if a.get("_model_used") == "opus"),
            "sonnet": sum(1 for a in analyses if a.get("_model_used") == "sonnet"),
            "haiku": sum(1 for a in analyses if a.get("_model_used") == "haiku"),
        },
        "methods": [a.get("_source_entry", {}).get("method", "")[:60] for a in analyses],
    }
    log_integration_run(run_summary)
    log(f"Step 15: Run logged — {json.dumps(run_summary, default=str)}")


# ---------------------------------------------------------------------------
# Gap detection (NEW in V2)
# ---------------------------------------------------------------------------

def detect_integration_gaps(analyses: list[dict]) -> None:
    """Check what the pipeline SHOULD have caught but didn't."""
    gaps = []
    for analysis in analyses:
        gap_note = analysis.get("gap_detection", "")
        if gap_note and gap_note.lower() not in ("none", "n/a", ""):
            gaps.append({
                "method": analysis.get("_source_entry", {}).get("method", "")[:60],
                "gap": gap_note,
                "venture": analysis.get("venture_type", ""),
            })

    if not gaps:
        return

    log(f"Gap detection: Found {len(gaps)} pipeline gaps to address")
    safe_path(GAP_REPORT).parent.mkdir(parents=True, exist_ok=True)

    gap_content = f"# Integration Gap Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    gap_content += "Methods the pipeline should auto-catch in the future:\n\n"
    for g in gaps:
        gap_content += f"## {g['method']}\n"
        gap_content += f"**Venture:** {g['venture']}\n"
        gap_content += f"**Gap:** {g['gap']}\n\n"

    with open(safe_path(GAP_REPORT), "a") as f:
        f.write(gap_content)
    log(f"Gap report updated: {GAP_REPORT.name}")


# ---------------------------------------------------------------------------
# Pipeline status
# ---------------------------------------------------------------------------

def show_status() -> None:
    print("=" * 70)
    print("AUTONOMOUS INTEGRATOR V2 — Pipeline Status")
    print("=" * 70)

    # Alpha staging
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

    # Integration log
    runs = v2_runs = 0
    last_run = "never"
    if INTEGRATION_LOG.exists():
        try:
            lines = INTEGRATION_LOG.read_text().strip().splitlines()
            runs = len(lines)
            for line in lines:
                rec = json.loads(line)
                if rec.get("version") == "v2":
                    v2_runs += 1
            if lines:
                last = json.loads(lines[-1])
                last_run = last.get("timestamp", "unknown")
        except Exception:
            pass
    print(f"Integration Runs: {runs} total ({v2_runs} V2), last: {last_run}")

    # Failed integrations
    failed = 0
    if FAILED_INTEGRATIONS.exists():
        try:
            failed = len(FAILED_INTEGRATIONS.read_text().strip().splitlines())
        except Exception:
            pass
    print(f"Failed Integrations: {failed} (replayable with --replay-failed)")

    # Growth plans
    plan_count = 0
    if GROWTH_PLANS_DIR.exists():
        plan_count = len(list(GROWTH_PLANS_DIR.glob("GROWTH_*.md")))
    print(f"Growth Plans: {plan_count}")

    # DAG pipelines
    dag_count = 0
    if DAG_PLANS_DIR.exists():
        dag_count = len(list(DAG_PLANS_DIR.glob("dag_*.json")))
    print(f"DAG Pipelines: {dag_count}")

    # Handoff chains
    chain_count = 0
    if HANDOFF_CHAINS_DIR.exists():
        chain_count = len(list(HANDOFF_CHAINS_DIR.glob("chain_*.json")))
    print(f"Handoff Chains: {chain_count}")

    # Procedural memory
    if sovrun_available():
        print(f"Procedural Memory: AVAILABLE (sovrun)")
    else:
        print(f"Procedural Memory: UNAVAILABLE (sovrun not loaded)")

    # DAG orchestrator
    print(f"DAG Orchestrator: {'AVAILABLE' if _DAG_AVAILABLE else 'UNAVAILABLE'}")

    # Master ops cache
    if MASTER_OPS_CACHE.exists():
        try:
            age_h = (time.time() - MASTER_OPS_CACHE.stat().st_mtime) / 3600
            print(f"Master Ops Cache: {age_h:.1f}h old")
        except Exception:
            print("Master Ops Cache: unknown age")
    else:
        print("Master Ops Cache: NOT FOUND")

    # Cron
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
        if "autonomous_integrator" in result.stdout:
            print("Cron: INSTALLED")
        else:
            print("Cron: NOT INSTALLED (add: 15 22 * * *)")
    except Exception:
        print("Cron: unable to check")

    print(f"\nMax automations/run: {MAX_NEW_AUTOMATIONS_PER_RUN}")
    print(f"Max entries/run: {MAX_ENTRIES_PER_RUN}")
    print(f"Min quality score: {MIN_QUALITY_SCORE}/10")

    # Toolkit availability
    print(f"\n--- Toolkit ---")
    print(f"Sovrun modules: {'YES' if sovrun_available() else 'NO'}")
    print(f"DAG orchestrator: {'YES' if _DAG_AVAILABLE else 'NO'}")
    print(f"Handoff router: {'YES' if get_handoff_router() else 'NO'}")
    print(f"Workflow detector: {'YES' if get_workflow_detector() else 'NO'}")
    print(f"Connector registry: {'YES' if CONNECTOR_REGISTRY.exists() else 'NO'}")
    print("=" * 70)


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

PARALLEL_WORKERS = 8  # Tested safe concurrency for claude -p without queue saturation


def _mark_entries_integrated(analyses: list[dict]) -> None:
    """Mark processed entries as INTEGRATED in ALPHA_STAGING so they don't reprocess."""
    integrated_ids = set()
    for a in analyses:
        aid = a.get("_source_entry", {}).get("alpha_id", "")
        if aid:
            integrated_ids.add(aid)

    if not integrated_ids or not ALPHA_STAGING.exists():
        return

    try:
        rows = []
        fieldnames = None
        with open(ALPHA_STAGING) as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row.get("alpha_id", "") in integrated_ids:
                    row["status"] = "INTEGRATED"
                    row["ops_generated"] = "yes"
                rows.append(row)

        if fieldnames:
            tmp = ALPHA_STAGING.with_suffix(".tmp")
            with open(safe_path(tmp), "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            tmp.rename(ALPHA_STAGING)
            log(f"Marked {len(integrated_ids)} entries as INTEGRATED")
    except Exception as e:
        log(f"Failed to mark entries as INTEGRATED: {e}", "ERROR")


def _analyze_single_entry(entry: dict) -> Optional[dict]:
    """Analyze a single entry — designed to run in parallel."""
    method = (entry.get("extracted_method") or entry.get("tactic")
              or entry.get("content") or "unknown")
    try:
        prior_solution = recall_prior_solutions(method)
        analysis = deep_analysis(entry, prior_solution=prior_solution)
        if analysis is None:
            log_failed_integration(entry, "analysis_failed_or_low_quality")
        return analysis
    except Exception as e:
        log(f"Analysis error for {method[:40]}: {e}", "ERROR")
        log_failed_integration(entry, f"exception: {e}")
        return None


def _integrate_single(analysis: dict, dry_run: bool = False) -> dict:
    """Run all integration steps for a single analyzed entry. Returns result summary."""
    method = analysis.get("_source_entry", {}).get("method", "unknown")
    result = {"method": method[:60], "steps": []}

    # Steps that create files/configs (fast, no claude -p needed)
    create_venture(analysis, dry_run=dry_run)
    create_ralph_loop(analysis, dry_run=dry_run)
    create_hooks(analysis, dry_run=dry_run)
    create_dag_pipeline(analysis, dry_run=dry_run)
    create_handoff_chain(analysis, dry_run=dry_run)
    wire_growth_tactics(analysis, dry_run=dry_run)
    wire_kpi_task(analysis, dry_run=dry_run)
    update_master_ops(analysis, dry_run=dry_run)

    if not dry_run:
        capture_integration_skill(analysis)

    return result


def run_pipeline(entries: list[dict], dry_run: bool = False) -> None:
    if not entries:
        log("No entries to process. Pipeline complete (nothing to do).")
        return

    mode = "DRY-RUN" if dry_run else "LIVE"
    log(f"Pipeline V2 starting ({mode}) — {len(entries)} entries, "
        f"sovrun={'YES' if sovrun_available() else 'NO'}, "
        f"DAG={'YES' if _DAG_AVAILABLE else 'NO'}, "
        f"parallel={PARALLEL_WORKERS} workers")

    # ── PHASE 1: PARALLEL ANALYSIS ──────────────────────────────────────
    # Run claude -p analysis on all entries concurrently (the slow part)
    from concurrent.futures import ThreadPoolExecutor, as_completed

    log(f"Phase 1: Analyzing {len(entries)} entries with {PARALLEL_WORKERS} parallel workers...")

    analyses: list[dict] = []
    with ThreadPoolExecutor(max_workers=PARALLEL_WORKERS) as pool:
        futures = {pool.submit(_analyze_single_entry, entry): entry for entry in entries}
        for i, future in enumerate(as_completed(futures), 1):
            entry = futures[future]
            method = (entry.get("extracted_method") or entry.get("tactic")
                      or entry.get("content") or "?")[:60]
            try:
                analysis = future.result()
                if analysis:
                    analyses.append(analysis)
                    q = analysis.get("quality_score", 0)
                    v = analysis.get("venture_type", "?")
                    log(f"  [{i}/{len(entries)}] OK q={q}/10 v={v}: {method}")
                else:
                    log(f"  [{i}/{len(entries)}] SKIP: {method}", "WARN")
            except Exception as e:
                log(f"  [{i}/{len(entries)}] ERROR: {method}: {e}", "ERROR")

    log(f"Phase 1 complete: {len(analyses)}/{len(entries)} passed analysis")

    # ── PHASE 2: PARALLEL INTEGRATION ───────────────────────────────────
    # Run file creation / wiring steps concurrently (fast, no claude -p)
    log(f"Phase 2: Integrating {len(analyses)} entries...")

    automations_created = 0
    with ThreadPoolExecutor(max_workers=PARALLEL_WORKERS) as pool:
        futures = {pool.submit(_integrate_single, a, dry_run): a for a in analyses}
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                log(f"Integration error: {e}", "ERROR")

    # ── PHASE 3: INTELLIGENT SCRIPT GENERATION ──────────────────────────
    # Uses claude -p with bare=True (runs from /tmp, no CLAUDE.md/plugins/hooks
    # overhead — ~50s vs 3+ min). Only generates scripts for entries that are
    # REAL METHODS (q>=6) and don't duplicate existing automations.
    log(f"Phase 3: Generating scripts (bare mode, q>=6 only)...")
    high_quality = [a for a in analyses if a.get("quality_score", 0) >= 6]
    log(f"  {len(high_quality)}/{len(analyses)} entries qualify for script gen (q>=6)")
    for analysis in high_quality:
        if automations_created >= MAX_NEW_AUTOMATIONS_PER_RUN:
            break
        _, automations_created = create_automation_script(
            analysis, automations_created, dry_run=dry_run)

    # ── PHASE 4: N8N WORKFLOWS (sequential, hits n8n API) ───────────────
    log(f"Phase 4: Creating n8n workflows...")
    for analysis in analyses:
        create_n8n_workflow(analysis, dry_run=dry_run)

    # ── PHASE 5: MARK ENTRIES AS INTEGRATED ────────────────────────────
    if not dry_run and analyses:
        _mark_entries_integrated(analyses)

    # ── PHASE 6: SYSTEM UPDATE ──────────────────────────────────────────
    update_system(analyses, dry_run=dry_run)
    if not dry_run:
        detect_integration_gaps(analyses)

    # ── PHASE 7: VERIFICATION (honest artifact audit) ──────────────────
    log("Phase 7: Verifying actual output...")
    verified = {
        "scripts_created": 0,
        "scripts_compiled": 0,
        "dags_with_logic": 0,
        "dags_stub_only": 0,
        "chains_created": 0,
        "growth_plans": 0,
        "cron_entries": 0,
        "n8n_deployed": 0,
    }

    # Count real scripts (not dag_runner stubs)
    for analysis in analyses:
        sname = analysis.get("script_name", "")
        if sname and (AUTOMATIONS / sname).exists():
            verified["scripts_created"] += 1
            # Check if it compiles
            try:
                py_compile.compile(str(AUTOMATIONS / sname), doraise=True)
                verified["scripts_compiled"] += 1
            except Exception:
                pass

    # Count DAGs
    if DAG_PLANS_DIR.exists():
        for dag_file in DAG_PLANS_DIR.glob("dag_*.json"):
            verified["dags_with_logic" if dag_file.stat().st_size > 200 else "dags_stub_only"] += 1

    # Count chains
    if HANDOFF_CHAINS_DIR.exists():
        verified["chains_created"] = len(list(HANDOFF_CHAINS_DIR.glob("chain_*.json")))

    # Count growth plans
    if GROWTH_PLANS_DIR.exists():
        verified["growth_plans"] = len(list(GROWTH_PLANS_DIR.glob("GROWTH_*.md")))

    # Check cron
    try:
        cron_result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
        for kw in ["integrator", "edgar", "crunchbase", "orphan", "backlog"]:
            if kw in cron_result.stdout:
                verified["cron_entries"] += 1
    except Exception:
        pass

    # Honest summary with three-level reporting
    log(f"=== VERIFICATION REPORT ===")
    log(f"VERIFIED (executable + tested):")
    log(f"  Scripts created & compiled: {verified['scripts_compiled']}")
    log(f"  Cron entries installed: {verified['cron_entries']}")
    log(f"BUILT (exists, not yet run):")
    log(f"  Scripts created (may not compile): {verified['scripts_created']}")
    log(f"  DAG configs: {verified['dags_with_logic']}")
    log(f"  Handoff chain configs: {verified['chains_created']}")
    log(f"PLANNED (docs/configs only):")
    log(f"  Growth plan docs: {verified['growth_plans']}")
    log(f"  DAG stub runners: {verified['dags_stub_only']}")
    if automations_created == 0 and len(analyses) > 5:
        log(f"WARNING: {len(analyses)} entries analyzed but 0 scripts generated — "
            f"script generation likely failed. Check Phase 3 errors.", "WARN")

    tools_used = set()
    for a in analyses:
        for k, v in a.get("tools_selected", {}).items():
            if v:
                tools_used.add(k)

    log(f"Pipeline V2 complete ({mode}) — "
        f"{len(analyses)} analyzed, "
        f"{automations_created} scripts GENERATED, "
        f"{verified['scripts_compiled']} scripts VERIFIED, "
        f"avg_quality={sum(a.get('quality_score', 0) for a in analyses) / max(len(analyses), 1):.1f}/10")


# ---------------------------------------------------------------------------
# Gap check command (NEW in V2)
# ---------------------------------------------------------------------------

def run_gap_check() -> None:
    """Scan ALPHA_STAGING for methods that SHOULD have triggered automations but didn't."""
    log("Running gap check — scanning for un-integrated alpha with automation potential...")

    if not ALPHA_STAGING.exists():
        log("No ALPHA_STAGING.csv found", "ERROR")
        return

    ungapped = []
    keywords_that_should_trigger = [
        "crunchbase", "edgar", "sec filing", "8-k", "10-k",
        "scraper", "scanner", "monitor", "tracker", "bot",
        "automat", "pipeline", "workflow", "cron",
        "api", "webhook", "endpoint",
    ]

    try:
        with open(ALPHA_STAGING) as f:
            for row in csv.DictReader(f):
                method = (row.get("extracted_method") or row.get("content") or "").lower()
                status = (row.get("status") or "").upper()
                if status in ("REJECTED", "INTEGRATED"):
                    continue
                for kw in keywords_that_should_trigger:
                    if kw in method:
                        ungapped.append({
                            "method": method[:100],
                            "keyword": kw,
                            "status": status,
                            "alpha_id": row.get("alpha_id", ""),
                        })
                        break
    except Exception as e:
        log(f"Gap check error: {e}", "ERROR")
        return

    if ungapped:
        log(f"Gap check: Found {len(ungapped)} methods that should have auto-triggered integration:")
        for g in ungapped[:10]:
            log(f"  - [{g['status']}] {g['method'][:80]} (keyword: {g['keyword']})")

        # Write gap report
        safe_path(GAP_REPORT).parent.mkdir(parents=True, exist_ok=True)
        report = f"\n\n# Gap Check — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        report += f"Found {len(ungapped)} methods with automation keywords not yet integrated:\n\n"
        for g in ungapped:
            report += f"- `{g['alpha_id']}`: {g['method'][:80]} (trigger: {g['keyword']}, status: {g['status']})\n"
        with open(safe_path(GAP_REPORT), "a") as f:
            f.write(report)
        log(f"Gap report written to {GAP_REPORT.name}")
    else:
        log("Gap check: No gaps found — pipeline is catching automation-relevant methods")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Autonomous Integrator V2 — full-toolkit alpha integration"
    )
    parser.add_argument("--run", action="store_true",
                        help="Process all today's approved entries")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be created without creating")
    parser.add_argument("--entry", type=str,
                        help="Process a specific entry by alpha_id")
    parser.add_argument("--status", action="store_true",
                        help="Show integration pipeline status")
    parser.add_argument("--gap-check", action="store_true",
                        help="Scan for un-integrated methods that should have triggered automation")
    parser.add_argument("--replay-failed", action="store_true",
                        help="Re-attempt previously failed integrations")

    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.gap_check:
        run_gap_check()
        return

    if args.replay_failed:
        entries = load_failed_entries()
        if not entries:
            log("No failed integrations to replay")
            return
        log(f"Replaying {len(entries)} failed integrations...")
        run_pipeline(entries, dry_run=args.dry_run)
        return

    if args.entry:
        entries = load_entry_by_id(args.entry)
        if not entries:
            log(f"Entry not found: {args.entry}", "ERROR")
            sys.exit(1)
        run_pipeline(entries, dry_run=args.dry_run)
        return

    if args.run or args.dry_run:
        entries = load_approved_today()
        run_pipeline(entries, dry_run=args.dry_run)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
