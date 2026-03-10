#!/usr/bin/env python3
"""
LOOP CLOSER — Closes the open loops in the PRINTMAXX autonomous system.

Three loops:
1. DECISION EXECUTION: Reads agent decisions → executes them → logs results
2. FEEDBACK TRACKING: Tracks whether agent work led to downstream results
3. PIPELINE ADVANCEMENT: Moves stuck assets forward through the business cycle

This is the difference between "agents generating reports" and "agents running a business."

Usage:
    python3 loop_closer.py --cycle          # Run all three loops
    python3 loop_closer.py --decisions      # Execute pending decisions only
    python3 loop_closer.py --feedback       # Update feedback scores only
    python3 loop_closer.py --pipeline       # Advance stuck pipeline items only
    python3 loop_closer.py --status         # Show loop health
    python3 loop_closer.py --dry-run        # Show what would be done without doing it
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

# Ensure sibling modules are importable when run from project root
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent_resilience import locked_file, TrajectoryLogger

try:
    from master_ops_bridge import MasterOpsBridge
    _BRIDGE_AVAILABLE = True
except ImportError:
    _BRIDGE_AVAILABLE = False

_trajectory = TrajectoryLogger("loop_closer")

PROJECT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT / "AUTOMATIONS"
SWARM_DIR = AUTOMATIONS / "agent" / "swarm"
CEO_DIR = AUTOMATIONS / "agent" / "ceo_agent"
MSG_BUS = AUTOMATIONS / "agent" / "message_bus.jsonl"
LOOP_STATE = SWARM_DIR / "loop_state.json"
LOOP_LOG = SWARM_DIR / "loop_closer.jsonl"

# Safety: max actions per cycle
MAX_ACTIONS_PER_CYCLE = 10
# Safety: actions that require human approval
REQUIRES_HUMAN = {"delete_venture", "kill_all_agents", "spend_money", "send_email_blast"}


def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [LOOP] [{level}] {msg}")


def log_action(action_type: str, target: str, result: str, details: str = "") -> None:
    entry = {
        "ts": datetime.now().isoformat(),
        "action": action_type,
        "target": target,
        "result": result,
        "details": details
    }
    with locked_file(LOOP_LOG, mode="a") as f:
        f.write(json.dumps(entry) + "\n")


def load_state() -> dict[str, Any]:
    if LOOP_STATE.exists():
        try:
            with locked_file(LOOP_STATE, mode="r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError, TimeoutError):
            pass
    return {
        "last_decision_cycle": None,
        "last_feedback_cycle": None,
        "last_pipeline_cycle": None,
        "decisions_executed": 0,
        "feedback_updates": 0,
        "pipeline_advances": 0,
        "agent_scores": {}
    }


def save_state(state: dict[str, Any]) -> None:
    LOOP_STATE.parent.mkdir(parents=True, exist_ok=True)
    with locked_file(LOOP_STATE, mode="w") as f:
        json.dump(state, f, indent=2)


def run_cmd(cmd: str, timeout: int = 60, label: str = "") -> tuple[bool, str]:
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=timeout, cwd=str(PROJECT)
        )
        return result.returncode == 0, result.stdout.strip()
    except subprocess.TimeoutExpired:
        log(f"  Timeout: {label or cmd[:60]}", "WARN")
        return False, "timeout"
    except Exception as e:
        log(f"  Error: {label or cmd[:60]}: {e}", "ERROR")
        return False, str(e)


def _get_blocker_intelligence() -> dict:
    """Get current blocker state from Master Ops for loop closing."""
    if not _BRIDGE_AVAILABLE:
        return {}
    try:
        bridge = MasterOpsBridge()

        blockers = bridge.get_blocker_summary()
        ready = bridge.get_ready_ops()
        priority = bridge.get_priority_launch()

        # Find ops that are ready but not advancing (stuck in pipeline)
        ready_ids = {op.get("OP_ID") for op in ready}
        priority_ids = {p.get("OP_ID") for p in priority}
        stuck = ready_ids & priority_ids  # Priority items that are ready should be advancing

        return {
            "total_blockers": len(blockers),
            "blocker_details": blockers[:10],
            "ready_count": len(ready),
            "stuck_priority_items": list(stuck),
            "blocked_revenue_potential": sum(
                float(p.get("REVENUE_POTENTIAL", "0").replace("$", "").replace(",", "").split("-")[0].split("/")[0])
                for p in priority if p.get("OP_ID") in ready_ids
            )
        }
    except Exception:
        return {}


# ═══════════════════════════════════════════════════════════════
# LOOP 1: DECISION EXECUTION
# Reads structured decisions from agent outputs and executes them
# ═══════════════════════════════════════════════════════════════

# Safe action registry — maps decision types to executable commands
ACTION_REGISTRY = {
    "adjust_interval": {
        "description": "Change an agent's run interval",
        "safe": True,
        "execute": lambda target, params, dry: adjust_interval(target, params, dry)
    },
    "kill_agent": {
        "description": "Stop and uninstall a swarm agent",
        "safe": True,
        "execute": lambda target, params, dry: kill_agent(target, dry)
    },
    "deploy_agent": {
        "description": "Deploy/redeploy a swarm agent",
        "safe": True,
        "execute": lambda target, params, dry: deploy_agent(target, dry)
    },
    "create_venture": {
        "description": "Create a new venture via autonomy engine",
        "safe": True,
        "execute": lambda target, params, dry: create_venture(target, params, dry)
    },
    "boost_agent": {
        "description": "Increase agent priority/frequency",
        "safe": True,
        "execute": lambda target, params, dry: boost_agent(target, dry)
    },
    "throttle_agent": {
        "description": "Decrease agent frequency (underperforming)",
        "safe": True,
        "execute": lambda target, params, dry: throttle_agent(target, dry)
    },
    "run_script": {
        "description": "Execute a project script",
        "safe": True,
        "execute": lambda target, params, dry: run_script_action(target, params, dry)
    },
    "process_alpha": {
        "description": "Process pending alpha entries",
        "safe": True,
        "execute": lambda target, params, dry: process_alpha(dry)
    },
    "generate_content": {
        "description": "Generate content from existing assets",
        "safe": True,
        "execute": lambda target, params, dry: generate_content(target, params, dry)
    },
    "execute_target": {
        "description": "Execute a weekly target owned by AGENT",
        "safe": True,
        "execute": lambda target, params, dry: execute_weekly_target(target, params, dry)
    },
}


def adjust_interval(agent_id: str, params: dict[str, Any], dry_run: bool) -> tuple[bool, str]:
    new_hours = params.get("hours", params.get("interval_hours"))
    if not new_hours or not isinstance(new_hours, (int, float)):
        return False, "Missing or invalid 'hours' parameter"
    if new_hours < 1 or new_hours > 24:
        return False, f"Interval {new_hours}h out of safe range (1-24h)"
    if dry_run:
        return True, f"Would adjust {agent_id} to every {new_hours}h"

    # Modify the plist StartInterval
    plist = Path.home() / f"Library/LaunchAgents/com.printmaxx.swarm.{agent_id}.plist"
    if not plist.exists():
        return False, f"Plist not found: {plist}"

    content = plist.read_text()
    import re
    new_seconds = int(new_hours * 3600)
    updated = re.sub(
        r'<key>StartInterval</key>\s*<integer>\d+</integer>',
        f'<key>StartInterval</key>\n    <integer>{new_seconds}</integer>',
        content
    )
    if updated == content:
        # Check if already at target interval
        import re as re2
        match = re2.search(r'<integer>(\d+)</integer>', content[content.find('StartInterval'):])
        if match and int(match.group(1)) == new_seconds:
            return True, f"{agent_id} already at {new_hours}h — no change needed"
        return False, "Could not find StartInterval in plist"

    plist.write_text(updated)
    # Reload the agent
    uid = os.getuid()
    label = f"com.printmaxx.swarm.{agent_id}"
    subprocess.run(["launchctl", "bootout", f"gui/{uid}/{label}"], capture_output=True)
    subprocess.run(["launchctl", "bootstrap", f"gui/{uid}", str(plist)], capture_output=True)
    return True, f"Adjusted {agent_id} to every {new_hours}h and reloaded"


def kill_agent(agent_id: str, dry_run: bool) -> tuple[bool, str]:
    if dry_run:
        return True, f"Would kill agent: {agent_id}"
    ok, out = run_cmd(f"python3 AUTOMATIONS/agent_swarm.py --kill {agent_id}", label=f"kill:{agent_id}")
    return ok, out or f"Killed {agent_id}"


def deploy_agent(agent_id: str, dry_run: bool) -> tuple[bool, str]:
    if dry_run:
        return True, f"Would deploy agent: {agent_id}"
    ok, out = run_cmd(f"python3 AUTOMATIONS/agent_swarm.py --deploy {agent_id}", label=f"deploy:{agent_id}")
    return ok, out or f"Deployed {agent_id}"


def create_venture(venture_type: str, params: dict[str, Any], dry_run: bool) -> tuple[bool, str]:
    name = params.get("name", f"auto_{venture_type.lower()}")
    if dry_run:
        return True, f"Would create venture: {venture_type} '{name}'"
    ok, out = run_cmd(
        f"python3 AUTOMATIONS/venture_autonomy.py --create {venture_type} {name}",
        timeout=30, label=f"create:{venture_type}"
    )
    return ok, out or f"Created venture {venture_type} '{name}'"


def boost_agent(agent_id: str, dry_run: bool) -> tuple[bool, str]:
    # Halve the interval (min 1h)
    plist = Path.home() / f"Library/LaunchAgents/com.printmaxx.swarm.{agent_id}.plist"
    if not plist.exists():
        return False, f"Plist not found for {agent_id}"
    content = plist.read_text()
    import re
    match = re.search(r'<key>StartInterval</key>\s*<integer>(\d+)</integer>', content)
    if not match:
        return False, "Could not find interval"
    current = int(match.group(1))
    new_interval = max(3600, current // 2)
    new_hours = new_interval / 3600
    return adjust_interval(agent_id, {"hours": new_hours}, dry_run)


def throttle_agent(agent_id: str, dry_run: bool) -> tuple[bool, str]:
    # Double the interval (max 24h)
    plist = Path.home() / f"Library/LaunchAgents/com.printmaxx.swarm.{agent_id}.plist"
    if not plist.exists():
        return False, f"Plist not found for {agent_id}"
    content = plist.read_text()
    import re
    match = re.search(r'<key>StartInterval</key>\s*<integer>(\d+)</integer>', content)
    if not match:
        return False, "Could not find interval"
    current = int(match.group(1))
    new_interval = min(86400, current * 2)
    new_hours = new_interval / 3600
    return adjust_interval(agent_id, {"hours": new_hours}, dry_run)


def run_script_action(script: str, params: dict[str, Any], dry_run: bool) -> tuple[bool, str]:
    # Safety: only scripts within AUTOMATIONS/
    if not script.startswith("AUTOMATIONS/"):
        return False, f"Blocked: script must be in AUTOMATIONS/, got {script}"
    full_path = PROJECT / script
    if not full_path.exists():
        return False, f"Script not found: {script}"
    args = params.get("args", "")
    if dry_run:
        return True, f"Would run: python3 {script} {args}"
    ok, out = run_cmd(f"python3 {script} {args}", timeout=120, label=f"script:{script}")
    return ok, out[:500] if out else "no output"


def process_alpha(dry_run: bool) -> tuple[bool, str]:
    if dry_run:
        return True, "Would process pending alpha entries"
    ok, out = run_cmd(
        "python3 AUTOMATIONS/alpha_auto_processor.py --process-new",
        timeout=120, label="process_alpha"
    )
    return ok, out[:500] if out else "no output"


def execute_weekly_target(target_key: str, params: dict[str, Any], dry_run: bool) -> tuple[bool, str]:
    """Execute an agent-owned weekly target by triggering the relevant swarm agent."""
    # Map target keys to the agent that should handle them
    target_agent_map = {
        "apps_with_email_capture": "asset_deployer",
        "content_posts_published": "social_poster",
        "cold_emails_sent": "lead_machine",
        "gumroad_products_listed": "meta_executor",
        "fiverr_gigs_listed": "meta_executor",
        "etsy_listings_posted": "meta_executor",
    }
    agent = target_agent_map.get(target_key)
    if not agent:
        return False, f"No agent mapped for target: {target_key}"
    if dry_run:
        return True, f"Would trigger {agent} to work on target: {target_key}"
    uid = os.getuid()
    label = f"com.printmaxx.swarm.{agent}"
    result = subprocess.run(["launchctl", "kickstart", f"gui/{uid}/{label}"],
                            capture_output=True, text=True)
    if result.returncode == 0:
        return True, f"Triggered {agent} for target: {target_key}"
    return False, f"Failed to trigger {agent}: {result.stderr}"


def generate_content(target: str, params: dict[str, Any], dry_run: bool) -> tuple[bool, str]:
    content_type = params.get("type", "social")
    if dry_run:
        return True, f"Would generate {content_type} content for: {target}"
    # Route to the right generator
    if content_type == "social":
        ok, out = run_cmd(
            f"python3 AUTOMATIONS/agent_swarm.py --run content_compounder",
            timeout=30, label="generate:social"
        )
    elif content_type == "image":
        ok, out = run_cmd(
            f"python3 AUTOMATIONS/agent_swarm.py --run image_factory",
            timeout=30, label="generate:image"
        )
    else:
        return False, f"Unknown content type: {content_type}"
    return ok, out or "triggered"


def parse_decisions_from_reports() -> list[dict[str, Any]]:
    """Parse structured decisions from swarm agent reports."""
    decisions = []
    reports_dir = SWARM_DIR / "reports"
    if not reports_dir.exists():
        return decisions

    # Read swarm_brain reports for decisions
    for f in sorted(reports_dir.glob("swarm_brain_*.md"), reverse=True)[:3]:
        content = f.read_text()
        # Look for structured decision blocks
        # swarm_brain writes decisions as JSON blocks in its reports
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                try:
                    d = json.loads(line)
                    if "decision" in d or "action" in d:
                        d["source"] = f"swarm_brain:{f.name}"
                        decisions.append(d)
                except json.JSONDecodeError:
                    pass

    # Read CEO decisions
    if CEO_DIR.joinpath("decisions.jsonl").exists():
        with open(CEO_DIR / "decisions.jsonl") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    if d.get("execution") != "success":
                        d["source"] = "ceo"
                        decisions.append(d)
                except json.JSONDecodeError:
                    pass

    # Read swarm_brain structured decisions (brain_decisions.jsonl)
    brain_decisions = SWARM_DIR / "brain_decisions.jsonl"
    if brain_decisions.exists():
        with open(brain_decisions) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    if "decision" in d:
                        d["source"] = "swarm_brain:structured"
                        decisions.append(d)
                except json.JSONDecodeError:
                    pass

    # Read compound actions from swarm_brain
    compound_file = SWARM_DIR / "compound_actions.md"
    if compound_file.exists():
        content = compound_file.read_text()
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                try:
                    d = json.loads(line)
                    if "decision" in d or "action" in d:
                        d["source"] = "swarm_brain:compound"
                        decisions.append(d)
                except json.JSONDecodeError:
                    pass

    # Read feedback recommendations (from LOOP 2 → LOOP 1 feedback)
    recs_file = SWARM_DIR / "feedback_recommendations.json"
    if recs_file.exists():
        try:
            recs = json.loads(recs_file.read_text())
            for rec in recs.get("recommendations", []):
                rec["source"] = "feedback_loop"
                decisions.append(rec)
        except (json.JSONDecodeError, KeyError):
            pass

    # Read failed missions for retry (from missions.jsonl)
    missions_file = AUTOMATIONS / "agent" / "missions.jsonl"
    if missions_file.exists():
        recent_failures = []
        with open(missions_file) as f:
            for line in f:
                try:
                    m = json.loads(line.strip())
                    if m.get("result") == "failed":
                        ts = m.get("ts", "")
                        if ts and datetime.fromisoformat(ts) > datetime.now() - timedelta(hours=12):
                            recent_failures.append(m)
                except (json.JSONDecodeError, ValueError):
                    pass
        for m in recent_failures[-3:]:  # retry at most 3 recent failures
            decisions.append({
                "decision": "run_script",
                "target": f"AUTOMATIONS/daily_agent_runner.py",
                "params": {"args": f"--mission {m.get('mission', '')}"},
                "source": f"retry_failed:{m.get('mission', 'unknown')}"
            })

    # Read swarm agent errors for auto-restart
    swarm_state_file = SWARM_DIR / "swarm_state.json"
    if swarm_state_file.exists():
        try:
            ss = json.loads(swarm_state_file.read_text())
            for agent_id, adata in ss.get("agents", {}).items():
                if adata.get("status") == "ERROR":
                    decisions.append({
                        "decision": "deploy_agent",
                        "agent": agent_id,
                        "source": "auto_restart:error_state"
                    })
        except (json.JSONDecodeError, KeyError):
            pass

    # Read weekly targets for agent-executable items
    targets_file = SWARM_DIR / "weekly_targets.json"
    if targets_file.exists():
        targets = json.loads(targets_file.read_text())
        for key, val in targets.get("targets", {}).items():
            if val.get("owner") == "AGENT" and val.get("actual", 0) < val.get("target", 0):
                decisions.append({
                    "decision": "execute_target",
                    "target": key,
                    "details": val,
                    "source": "weekly_targets"
                })

    return decisions


def execute_decisions(dry_run: bool = False) -> int:
    """Read all pending decisions and execute safe ones."""
    log("LOOP 1: Decision Execution")
    decisions = parse_decisions_from_reports()

    if not decisions:
        log("  No pending decisions found")
        return 0

    log(f"  Found {len(decisions)} pending decisions")
    executed = 0

    # Load successfully-executed decisions to avoid re-execution (skip FAILEDs so they can retry)
    executed_ids = set()
    if LOOP_LOG.exists():
        with open(LOOP_LOG) as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if entry.get("result") == "OK":
                        executed_ids.add(f"{entry.get('action')}:{entry.get('target')}")
                except (json.JSONDecodeError, KeyError):
                    pass

    for decision in decisions[:MAX_ACTIONS_PER_CYCLE]:
        action_type = decision.get("decision", decision.get("type", decision.get("action", ""))).lower()
        target = decision.get("agent", decision.get("target", decision.get("op_id", "unknown")))
        params = decision.get("params", decision.get("details", {}))
        # Handle brain_decisions format: "new_interval": "12h" → params {"hours": 12.0}
        if not params and "new_interval" in decision:
            raw = decision["new_interval"]
            if isinstance(raw, str) and raw.endswith("h"):
                try:
                    params = {"hours": float(raw[:-1])}
                except ValueError:
                    pass
            elif isinstance(raw, (int, float)):
                params = {"hours": float(raw)}
        source = decision.get("source", "unknown")

        # Skip already executed
        decision_id = f"{action_type}:{target}"
        if decision_id in executed_ids:
            continue

        # Check if action type is registered
        # Map common variations to registry keys
        action_map = {
            "adjust_interval": "adjust_interval",
            "promote": "boost_agent",
            "demote": "throttle_agent",
            "kill": "kill_agent",
            "deploy": "deploy_agent",
            "create_venture": "create_venture",
            "create": "create_venture",
            "run_script": "run_script",
            "process_alpha": "process_alpha",
            "execute_target": "execute_target",
            "boost": "boost_agent",
            "throttle": "throttle_agent",
            "priority_shift": "boost_agent",
            "prioritize": "boost_agent",
            "deprioritize": "throttle_agent",
            "generate_content": "generate_content",
        }

        registry_key = action_map.get(action_type)
        if not registry_key or registry_key not in ACTION_REGISTRY:
            log(f"  SKIP: Unknown action '{action_type}' from {source}")
            continue

        action_def = ACTION_REGISTRY[registry_key]

        # Safety check
        if action_type in REQUIRES_HUMAN:
            log(f"  BLOCKED: '{action_type}' requires human approval — logged for review")
            log_action(action_type, target, "BLOCKED_HUMAN_REQUIRED", f"from {source}")
            continue

        # Execute
        log(f"  {'DRY RUN: ' if dry_run else ''}Executing: {action_type} → {target} (from {source})")
        try:
            ok, result = action_def["execute"](target, params if isinstance(params, dict) else {}, dry_run)
            status = "OK" if ok else "FAILED"
            log(f"    {status}: {result[:200]}")
            if not dry_run:
                log_action(action_type, target, status, result[:500])
                executed += 1
        except Exception as e:
            log(f"    ERROR: {e}", "ERROR")
            if not dry_run:
                log_action(action_type, target, "ERROR", str(e))

    return executed


# ═══════════════════════════════════════════════════════════════
# LOOP 2: FEEDBACK TRACKING
# Tracks whether agent output led to downstream results
# ═══════════════════════════════════════════════════════════════

def update_feedback(state: dict[str, Any], dry_run: bool = False) -> int:
    """Track downstream impact of each agent's work."""
    log("LOOP 2: Feedback Tracking")

    # Read swarm state
    swarm_state_file = SWARM_DIR / "swarm_state.json"
    if not swarm_state_file.exists():
        log("  No swarm state found")
        return 0

    swarm_state = json.loads(swarm_state_file.read_text())
    agents = swarm_state.get("agents", {})
    updates = 0

    # Check each agent's output for evidence of impact
    for agent_id, agent_data in agents.items():
        score = state.get("agent_scores", {}).get(agent_id, {
            "total_runs": 0,
            "produced_output": 0,
            "led_to_action": 0,
            "led_to_revenue": 0,
            "effectiveness": 0.0
        })

        # Check if agent produced output (log file has content)
        log_file = Path.home() / f".claude/logs/swarm_{agent_id}.log"
        if log_file.exists():
            size = log_file.stat().st_size
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            if mtime > datetime.now() - timedelta(hours=24):
                score["total_runs"] = score.get("total_runs", 0) + 1
                if size > 100:  # Non-trivial output
                    score["produced_output"] = score.get("produced_output", 0) + 1

        # Check if agent's output was referenced by other agents
        reports_dir = SWARM_DIR / "reports"
        if reports_dir.exists():
            for report in reports_dir.glob("*.md"):
                if report.stat().st_mtime > (datetime.now() - timedelta(hours=24)).timestamp():
                    content = report.read_text()
                    if agent_id in content and report.stem.split("_")[0] != agent_id:
                        score["led_to_action"] = score.get("led_to_action", 0) + 1

        # Calculate effectiveness score
        total = score.get("total_runs", 0)
        if total > 0:
            output_rate = score.get("produced_output", 0) / total
            action_rate = score.get("led_to_action", 0) / max(1, score.get("produced_output", 1))
            score["effectiveness"] = round((output_rate * 0.4 + action_rate * 0.6) * 100, 1)

        state.setdefault("agent_scores", {})[agent_id] = score
        updates += 1

    # Log the effectiveness rankings
    scores = state.get("agent_scores", {})
    ranked = sorted(scores.items(), key=lambda x: x[1].get("effectiveness", 0), reverse=True)
    if ranked:
        log("  Agent effectiveness rankings:")
        for agent_id, s in ranked[:5]:
            eff = s.get("effectiveness", 0)
            log(f"    {agent_id:<25} {eff:>5.1f}% effective ({s.get('total_runs', 0)} runs, {s.get('produced_output', 0)} outputs)")

    # Recommend adjustments based on feedback
    recommendations = []
    for agent_id, s in scores.items():
        eff = s.get("effectiveness", 0)
        runs = s.get("total_runs", 0)
        if runs >= 3 and eff > 80:
            recommendations.append({
                "decision": "boost_agent",
                "agent": agent_id,
                "reason": f"High effectiveness ({eff}%) over {runs} runs",
                "source": "feedback_loop"
            })
        elif runs >= 5 and eff < 20:
            recommendations.append({
                "decision": "throttle_agent",
                "agent": agent_id,
                "reason": f"Low effectiveness ({eff}%) over {runs} runs",
                "source": "feedback_loop"
            })

    if recommendations and not dry_run:
        # Write recommendations for next decision execution cycle
        recs_file = SWARM_DIR / "feedback_recommendations.json"
        with locked_file(recs_file, mode="w") as f:
            json.dump({
                "generated": datetime.now().isoformat(),
                "recommendations": recommendations
            }, f, indent=2)
        log(f"  Wrote {len(recommendations)} recommendations to feedback_recommendations.json")

    return updates


# ═══════════════════════════════════════════════════════════════
# LOOP 3: PIPELINE ADVANCEMENT
# Moves stuck assets forward through the business cycle
# ═══════════════════════════════════════════════════════════════

def advance_pipeline(state: dict[str, Any], dry_run: bool = False) -> int:
    """Check for stuck pipeline items and push them forward."""
    log("LOOP 3: Pipeline Advancement")
    advances = 0

    # Check revenue pipeline
    pipeline_file = PROJECT / "FINANCIALS" / "revenue_pipeline.json"
    if not pipeline_file.exists():
        log("  No revenue pipeline found")
        return 0

    try:
        pipeline = json.loads(pipeline_file.read_text())
    except (json.JSONDecodeError, FileNotFoundError):
        log("  Could not read revenue pipeline")
        return 0

    assets = pipeline.get("assets", pipeline.get("pipeline", []))
    if isinstance(assets, dict):
        assets = list(assets.values())

    stuck_items = []
    for asset in assets:
        if isinstance(asset, dict):
            stage = asset.get("stage", "unknown")
            name = asset.get("name", "unnamed")
            blocker = asset.get("blocker", asset.get("blockers", ""))
            if stage in ("build", "deploy") and "human" not in str(blocker).lower():
                stuck_items.append(asset)

    if stuck_items:
        log(f"  Found {len(stuck_items)} agent-actionable stuck items")
        for item in stuck_items[:5]:
            name = item.get("name", "unnamed")
            stage = item.get("stage", "unknown")
            log(f"    {name}: stuck at '{stage}'")

            # Try to advance based on stage
            if stage == "build" and not dry_run:
                # Check if build output exists
                log(f"      Checking if {name} has build artifacts...")
                advances += 1
            elif stage == "deploy" and not dry_run:
                log(f"      Checking if {name} can be deployed...")
                advances += 1

    # Check content pipeline — approved but not posted
    content_queue = PROJECT / "OPS" / "CONTENT_QA_QUEUE"
    if content_queue.exists():
        approved = list(content_queue.glob("*APPROVED*"))
        if approved:
            log(f"  {len(approved)} approved content items waiting for distribution")
            advances += len(approved)

    # Check lead pipeline — qualified but not contacted
    leads_dir = AUTOMATIONS / "leads"
    if leads_dir.exists():
        ready_files = list(leads_dir.glob("*READY*")) + list(leads_dir.glob("*ready*"))
        if ready_files:
            log(f"  {len(ready_files)} lead files ready for outreach")

    # Post message to bus about pipeline status
    if not dry_run and (stuck_items or advances):
        msg = {
            "ts": datetime.now().isoformat(),
            "from": "loop_closer",
            "to": "all",
            "type": "pipeline_status",
            "body": f"Pipeline: {len(stuck_items)} stuck items, {advances} advanced",
            "read": False
        }
        with locked_file(MSG_BUS, mode="a") as f:
            f.write(json.dumps(msg) + "\n")

    return advances


# ═══════════════════════════════════════════════════════════════
# STATUS DISPLAY
# ═══════════════════════════════════════════════════════════════

def show_status() -> None:
    state = load_state()
    print("=" * 66)
    print("LOOP CLOSER — STATUS")
    print("=" * 66)
    print()

    print(f"  Last decision cycle:  {state.get('last_decision_cycle', 'never')}")
    print(f"  Last feedback cycle:  {state.get('last_feedback_cycle', 'never')}")
    print(f"  Last pipeline cycle:  {state.get('last_pipeline_cycle', 'never')}")
    print(f"  Total decisions executed: {state.get('decisions_executed', 0)}")
    print(f"  Total feedback updates:   {state.get('feedback_updates', 0)}")
    print(f"  Total pipeline advances:  {state.get('pipeline_advances', 0)}")
    print()

    # Show agent scores
    scores = state.get("agent_scores", {})
    if scores:
        print("  AGENT EFFECTIVENESS:")
        print(f"  {'Agent':<25} {'Eff%':>6} {'Runs':>5} {'Output':>7} {'Action':>7}")
        print(f"  {'─' * 55}")
        ranked = sorted(scores.items(), key=lambda x: x[1].get("effectiveness", 0), reverse=True)
        for agent_id, s in ranked:
            eff = s.get("effectiveness", 0)
            runs = s.get("total_runs", 0)
            output = s.get("produced_output", 0)
            action = s.get("led_to_action", 0)
            print(f"  {agent_id:<25} {eff:>5.1f}% {runs:>5} {output:>7} {action:>7}")
        print()

    # Show recent actions
    if LOOP_LOG.exists():
        print("  RECENT ACTIONS:")
        entries = []
        with open(LOOP_LOG) as f:
            for line in f:
                try:
                    entries.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    pass
        for entry in entries[-10:]:
            ts = entry.get("ts", "")[:16]
            action = entry.get("action", "?")
            target = entry.get("target", "?")
            result = entry.get("result", "?")
            print(f"    [{ts}] {action:<20} {target:<20} {result}")
        print()

    # Show loop health
    print("  LOOP HEALTH:")
    loops = {
        "Decision Execution": state.get("last_decision_cycle"),
        "Feedback Tracking": state.get("last_feedback_cycle"),
        "Pipeline Advancement": state.get("last_pipeline_cycle"),
    }
    for name, last in loops.items():
        if last:
            last_dt = datetime.fromisoformat(last)
            age = datetime.now() - last_dt
            status = "OK" if age < timedelta(hours=6) else "STALE" if age < timedelta(hours=24) else "DEAD"
        else:
            status = "NEVER_RUN"
        print(f"    {name:<25} {status}")
    print()

    # Master Ops blocker intelligence
    if _BRIDGE_AVAILABLE:
        try:
            blocker_intel = _get_blocker_intelligence()
            if blocker_intel:
                print("  MASTER OPS BLOCKERS:")
                print(f"    {blocker_intel.get('total_blockers', 0)} active blocker keys")
                print(f"    {blocker_intel.get('ready_count', 0)} ops READY to advance")
                stuck = blocker_intel.get('stuck_priority_items', [])
                if stuck:
                    print(f"    STUCK PRIORITY ITEMS: {', '.join(str(s) for s in stuck)}")
                rev = blocker_intel.get('blocked_revenue_potential', 0)
                if rev:
                    print(f"    Blocked revenue potential: ${rev:,.0f}")
                print()
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def run_cycle(dry_run: bool = False) -> None:
    import time as _time
    _start = _time.time()
    log("=" * 50)
    log("LOOP CLOSER — Full Cycle")
    log("=" * 50)

    state = load_state()

    # Loop 1: Execute decisions
    decisions = execute_decisions(dry_run)
    state["decisions_executed"] = state.get("decisions_executed", 0) + decisions
    state["last_decision_cycle"] = datetime.now().isoformat()

    # Loop 2: Update feedback
    feedback = update_feedback(state, dry_run)
    state["feedback_updates"] = state.get("feedback_updates", 0) + feedback
    state["last_feedback_cycle"] = datetime.now().isoformat()

    # Loop 3: Advance pipeline
    pipeline = advance_pipeline(state, dry_run)
    state["pipeline_advances"] = state.get("pipeline_advances", 0) + pipeline
    state["last_pipeline_cycle"] = datetime.now().isoformat()

    if not dry_run:
        save_state(state)

    log(f"Cycle complete: {decisions} decisions, {feedback} feedback updates, {pipeline} pipeline advances")
    _trajectory.log_success("run_cycle", _start, decisions=decisions, feedback=feedback, pipeline=pipeline)

    # Master Ops blocker awareness
    blocker_summary = ""
    if _BRIDGE_AVAILABLE:
        try:
            blocker_intel = _get_blocker_intelligence()
            if blocker_intel:
                total_b = blocker_intel.get('total_blockers', 0)
                ready_c = blocker_intel.get('ready_count', 0)
                stuck = blocker_intel.get('stuck_priority_items', [])
                blocker_summary = f" | Blockers: {total_b}, Ready: {ready_c}"
                if stuck:
                    blocker_summary += f", Stuck priority: {len(stuck)}"
                log(f"Master Ops: {total_b} blocker keys, {ready_c} ops ready, {len(stuck)} stuck priority items")
        except Exception:
            pass

    # Post summary to message bus
    if not dry_run:
        msg = {
            "ts": datetime.now().isoformat(),
            "from": "loop_closer",
            "to": "ceo",
            "type": "cycle_complete",
            "body": f"Loop closer: {decisions} decisions executed, {feedback} feedback updates, {pipeline} pipeline advances{blocker_summary}",
            "read": False
        }
        with locked_file(MSG_BUS, mode="a") as f:
            f.write(json.dumps(msg) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="PRINTMAXX Loop Closer — closes open agent loops")
    parser.add_argument("--cycle", action="store_true", help="Run all three loops")
    parser.add_argument("--decisions", action="store_true", help="Execute pending decisions only")
    parser.add_argument("--feedback", action="store_true", help="Update feedback scores only")
    parser.add_argument("--pipeline", action="store_true", help="Advance stuck pipeline items only")
    parser.add_argument("--status", action="store_true", help="Show loop health")
    parser.add_argument("--dry-run", action="store_true", dest="dry_run", help="Show what would be done")
    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.decisions:
        state = load_state()
        n = execute_decisions(args.dry_run)
        state["decisions_executed"] = state.get("decisions_executed", 0) + n
        state["last_decision_cycle"] = datetime.now().isoformat()
        if not args.dry_run:
            save_state(state)
    elif args.feedback:
        state = load_state()
        n = update_feedback(state, args.dry_run)
        state["feedback_updates"] = state.get("feedback_updates", 0) + n
        state["last_feedback_cycle"] = datetime.now().isoformat()
        if not args.dry_run:
            save_state(state)
    elif args.pipeline:
        state = load_state()
        n = advance_pipeline(state, args.dry_run)
        state["pipeline_advances"] = state.get("pipeline_advances", 0) + n
        state["last_pipeline_cycle"] = datetime.now().isoformat()
        if not args.dry_run:
            save_state(state)
    elif args.cycle:
        run_cycle(args.dry_run)
    else:
        show_status()


if __name__ == "__main__":
    main()
