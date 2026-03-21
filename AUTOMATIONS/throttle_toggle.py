#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Agent Throttle System
================================
Controls agent invocation frequency across EFFICIENT and HIGH modes.
Modifies launchd plist StartInterval values and reloads agents.

Usage:
  python3 throttle_toggle.py --status
  python3 throttle_toggle.py --mode efficient
  python3 throttle_toggle.py --mode high
  python3 throttle_toggle.py --agent gap_hunter --off
  python3 throttle_toggle.py --agent gap_hunter --on
  python3 throttle_toggle.py --agent gap_hunter --interval 4
  python3 throttle_toggle.py --estimate
  python3 throttle_toggle.py --json
  python3 throttle_toggle.py --reapply
"""

import argparse
import json
import os
import plistlib
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTOMATIONS_DIR = PROJECT_ROOT / "AUTOMATIONS"
CONFIG_PATH = AUTOMATIONS_DIR / "throttle_config.json"
STATE_PATH = AUTOMATIONS_DIR / "throttle_state.json"
LA_DIR = Path.home() / "Library" / "LaunchAgents"


def safe_path(p: Path) -> bool:
    """Guardrail: only allow file ops within PROJECT_ROOT or LA_DIR."""
    resolved = p.resolve()
    return str(resolved).startswith(str(PROJECT_ROOT)) or str(resolved).startswith(str(LA_DIR))


def load_config() -> dict:
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def load_state() -> dict:
    if STATE_PATH.exists():
        with open(STATE_PATH, "r") as f:
            return json.load(f)
    return {
        "current_mode": "unknown",
        "overrides": {},
        "disabled_agents": [],
        "last_changed": None,
        "last_changed_by": None,
    }


def save_state(state: dict):
    if not safe_path(STATE_PATH):
        print(f"BLOCKED: {STATE_PATH} outside project root")
        return
    state["last_changed"] = datetime.now().isoformat()
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def get_plist_path(plist_name: str) -> Path:
    return LA_DIR / plist_name


def read_plist(plist_path: Path) -> dict:
    with open(plist_path, "rb") as f:
        return plistlib.load(f)


def write_plist(plist_path: Path, data: dict):
    if not safe_path(plist_path):
        print(f"BLOCKED: {plist_path} outside allowed dirs")
        return
    with open(plist_path, "wb") as f:
        plistlib.dump(data, f)


def get_current_interval_hours(plist_path: Path) -> float | None:
    """Read current StartInterval from plist, return in hours."""
    if not plist_path.exists():
        return None
    try:
        data = read_plist(plist_path)
        seconds = data.get("StartInterval")
        if seconds:
            return seconds / 3600
    except Exception:
        pass
    return None


def set_interval(agent_name: str, agent_cfg: dict, hours: float, reason: str = "") -> bool:
    """Set StartInterval in plist and reload the agent. Returns True on success."""
    plist_path = get_plist_path(agent_cfg["plist"])
    if not plist_path.exists():
        print(f"  SKIP {agent_name}: plist not found at {plist_path}")
        return False

    label = agent_cfg["label"]
    seconds = int(hours * 3600)

    # Read current plist
    try:
        data = read_plist(plist_path)
    except Exception as e:
        print(f"  ERROR reading {agent_name}: {e}")
        return False

    old_seconds = data.get("StartInterval", 0)
    if old_seconds == seconds:
        print(f"  OK   {agent_name}: already at {hours}h ({seconds}s)")
        return True

    # Unload
    subprocess.run(
        ["launchctl", "unload", str(plist_path)],
        capture_output=True,
        timeout=10,
    )

    # Modify
    data["StartInterval"] = seconds
    write_plist(plist_path, data)

    # Reload
    result = subprocess.run(
        ["launchctl", "load", str(plist_path)],
        capture_output=True,
        timeout=10,
    )

    old_h = old_seconds / 3600
    status = "OK" if result.returncode == 0 else "WARN"
    print(f"  {status}  {agent_name}: {old_h}h -> {hours}h ({seconds}s) {reason}")
    return result.returncode == 0


def unload_agent(agent_name: str, agent_cfg: dict) -> bool:
    plist_path = get_plist_path(agent_cfg["plist"])
    if not plist_path.exists():
        print(f"  SKIP {agent_name}: plist not found")
        return False
    result = subprocess.run(
        ["launchctl", "unload", str(plist_path)],
        capture_output=True,
        timeout=10,
    )
    print(f"  {'OK' if result.returncode == 0 else 'WARN'}  {agent_name}: unloaded")
    return result.returncode == 0


def load_agent(agent_name: str, agent_cfg: dict) -> bool:
    plist_path = get_plist_path(agent_cfg["plist"])
    if not plist_path.exists():
        print(f"  SKIP {agent_name}: plist not found")
        return False
    result = subprocess.run(
        ["launchctl", "load", str(plist_path)],
        capture_output=True,
        timeout=10,
    )
    print(f"  {'OK' if result.returncode == 0 else 'WARN'}  {agent_name}: loaded")
    return result.returncode == 0


def is_agent_loaded(label: str) -> bool:
    """Check if an agent is currently loaded in launchctl."""
    result = subprocess.run(
        ["launchctl", "list"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    return label in result.stdout


def apply_mode(mode: str, config: dict, state: dict):
    """Apply EFFICIENT or HIGH mode to all agents."""
    agents = config["agents"]
    key = f"{mode}_interval_hours"

    print(f"\n{'='*60}")
    print(f"  APPLYING MODE: {mode.upper()}")
    print(f"{'='*60}")

    success = 0
    fail = 0
    skip = 0

    for name, cfg in sorted(agents.items(), key=lambda x: x[1]["tier"]):
        hours = cfg[key]

        # Check for per-agent overrides
        if name in state.get("overrides", {}):
            override_h = state["overrides"][name]
            print(f"  OVER {name}: override {override_h}h (mode wants {hours}h)")
            hours = override_h

        # Check if agent is disabled
        if name in state.get("disabled_agents", []):
            print(f"  OFF  {name}: disabled, skipping")
            skip += 1
            continue

        ok = set_interval(name, cfg, hours)
        if ok:
            success += 1
        else:
            fail += 1

    state["current_mode"] = mode
    state["last_changed_by"] = "throttle_toggle.py"
    save_state(state)

    print(f"\n  Done: {success} updated, {fail} failed, {skip} skipped")
    print(f"  Mode saved: {mode.upper()}")
    print(f"  State file: {STATE_PATH}\n")


def show_status(config: dict, state: dict):
    """Show current throttle status for all agents."""
    agents = config["agents"]

    print(f"\n{'='*70}")
    print(f"  PRINTMAXX THROTTLE STATUS")
    print(f"  Mode: {state.get('current_mode', 'UNKNOWN').upper()}")
    print(f"  Last changed: {state.get('last_changed', 'never')}")
    print(f"{'='*70}")

    total_daily = 0
    by_tier = {1: [], 2: [], 3: []}

    for name, cfg in sorted(agents.items()):
        plist_path = get_plist_path(cfg["plist"])
        current_h = get_current_interval_hours(plist_path)
        loaded = is_agent_loaded(cfg["label"])
        disabled = name in state.get("disabled_agents", [])
        override = state.get("overrides", {}).get(name)

        if current_h and current_h > 0:
            daily_runs = 24 / current_h
        else:
            daily_runs = 0

        total_daily += daily_runs

        status_flags = []
        if disabled:
            status_flags.append("OFF")
        if not loaded:
            status_flags.append("UNLOADED")
        if override:
            status_flags.append(f"OVERRIDE={override}h")

        flags_str = f" [{', '.join(status_flags)}]" if status_flags else ""

        entry = {
            "name": name,
            "tier": cfg["tier"],
            "category": cfg["category"],
            "current_h": current_h,
            "daily_runs": daily_runs,
            "efficient_h": cfg["efficient_interval_hours"],
            "high_h": cfg["high_interval_hours"],
            "loaded": loaded,
            "flags": flags_str,
        }
        by_tier[cfg["tier"]].append(entry)

    for tier in [1, 2, 3]:
        tier_label = {1: "PRODUCTIVE", 2: "BLOCKED", 3: "SUPPORT"}[tier]
        entries = by_tier[tier]
        tier_daily = sum(e["daily_runs"] for e in entries)
        print(f"\n  TIER {tier} ({tier_label}) - {len(entries)} agents, ~{tier_daily:.0f} runs/day")
        print(f"  {'Agent':<50s} {'Now':>5s} {'Eff':>5s} {'High':>5s} {'Runs/d':>7s} {'Flags'}")
        print(f"  {'-'*50} {'-'*5} {'-'*5} {'-'*5} {'-'*7} {'-'*15}")
        for e in sorted(entries, key=lambda x: x["name"]):
            now_str = f"{e['current_h']:.0f}h" if e["current_h"] else "N/A"
            eff_str = f"{e['efficient_h']}h"
            high_str = f"{e['high_h']}h"
            runs_str = f"{e['daily_runs']:.1f}"
            print(f"  {e['name']:<50s} {now_str:>5s} {eff_str:>5s} {high_str:>5s} {runs_str:>7s} {e['flags']}")

    print(f"\n  TOTAL: ~{total_daily:.0f} invocations/day across {len(agents)} agents")
    print(f"{'='*70}\n")


def show_estimate(config: dict, state: dict):
    """Show token burn estimates for each mode."""
    agents = config["agents"]

    print(f"\n{'='*60}")
    print(f"  TOKEN BURN ESTIMATE")
    print(f"{'='*60}")

    for mode in ["efficient", "high"]:
        key = f"{mode}_interval_hours"
        total = 0
        for name, cfg in agents.items():
            hours = cfg[key]
            if name in state.get("overrides", {}) and state["current_mode"] == mode:
                hours = state["overrides"][name]
            if name not in state.get("disabled_agents", []):
                total += 24 / hours

        print(f"\n  {mode.upper()} mode:")
        print(f"    Daily invocations:  ~{total:.0f}")
        print(f"    Weekly invocations: ~{total * 7:.0f}")
        # Rough estimate: ~2K tokens per agent invocation average
        print(f"    Est. tokens/day:    ~{total * 2000:,.0f} (@ ~2K tokens/invocation)")
        print(f"    Est. tokens/month:  ~{total * 2000 * 30:,.0f}")

    print(f"\n  Savings (efficient vs high): ~{((1 - 45/193) * 100):.0f}% fewer invocations")
    print(f"{'='*60}\n")


def show_json(config: dict, state: dict):
    """Machine-readable JSON output for dashboard API."""
    agents = config["agents"]
    output = {
        "mode": state.get("current_mode", "unknown"),
        "last_changed": state.get("last_changed"),
        "last_changed_by": state.get("last_changed_by"),
        "agents": {},
        "summary": {
            "total_agents": len(agents),
            "total_daily_invocations": 0,
            "disabled_count": len(state.get("disabled_agents", [])),
            "override_count": len(state.get("overrides", {})),
        },
    }

    total_daily = 0
    for name, cfg in agents.items():
        plist_path = get_plist_path(cfg["plist"])
        current_h = get_current_interval_hours(plist_path)
        loaded = is_agent_loaded(cfg["label"])
        disabled = name in state.get("disabled_agents", [])
        override = state.get("overrides", {}).get(name)

        if current_h and current_h > 0:
            daily_runs = 24 / current_h
        else:
            daily_runs = 0
        total_daily += daily_runs

        output["agents"][name] = {
            "tier": cfg["tier"],
            "category": cfg["category"],
            "current_interval_hours": current_h,
            "efficient_interval_hours": cfg["efficient_interval_hours"],
            "high_interval_hours": cfg["high_interval_hours"],
            "daily_runs": round(daily_runs, 1),
            "loaded": loaded,
            "disabled": disabled,
            "override_hours": override,
        }

    output["summary"]["total_daily_invocations"] = round(total_daily, 0)
    print(json.dumps(output, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Agent Throttle System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --status                    Show all agent intervals
  %(prog)s --mode efficient            Switch to token-saving mode (~45/day)
  %(prog)s --mode high                 Switch to full-burn mode (~193/day)
  %(prog)s --agent gap_hunter --off    Disable gap_hunter
  %(prog)s --agent gap_hunter --on     Re-enable gap_hunter
  %(prog)s --agent gap_hunter --interval 4   Set gap_hunter to 4h
  %(prog)s --estimate                  Show token burn estimates
  %(prog)s --json                      Machine-readable status
  %(prog)s --reapply                   Re-apply current mode (after deploy overwrite)
        """,
    )

    parser.add_argument("--status", action="store_true", help="Show current mode and all agent intervals")
    parser.add_argument("--mode", choices=["efficient", "high"], help="Switch all agents to EFFICIENT or HIGH mode")
    parser.add_argument("--agent", type=str, help="Target a specific agent by name")
    parser.add_argument("--off", action="store_true", help="Unload and disable the specified agent")
    parser.add_argument("--on", action="store_true", help="Load and enable the specified agent")
    parser.add_argument("--interval", type=float, help="Set custom interval in hours for specified agent")
    parser.add_argument("--estimate", action="store_true", help="Show token burn estimates per mode")
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    parser.add_argument("--reapply", action="store_true", help="Re-apply current mode (after agent_swarm.py --deploy)")

    args = parser.parse_args()

    # Validate config exists
    if not CONFIG_PATH.exists():
        print(f"ERROR: Config not found at {CONFIG_PATH}")
        sys.exit(1)

    config = load_config()
    state = load_state()

    # --- Handle --status ---
    if args.status:
        show_status(config, state)
        return

    # --- Handle --estimate ---
    if args.estimate:
        show_estimate(config, state)
        return

    # --- Handle --json ---
    if args.json:
        show_json(config, state)
        return

    # --- Handle --mode ---
    if args.mode:
        apply_mode(args.mode, config, state)
        return

    # --- Handle --reapply ---
    if args.reapply:
        current = state.get("current_mode")
        if current not in ("efficient", "high"):
            print(f"ERROR: No mode previously set (current: {current}). Use --mode first.")
            sys.exit(1)
        print(f"Re-applying mode: {current}")
        apply_mode(current, config, state)
        return

    # --- Handle --agent operations ---
    if args.agent:
        agent_name = args.agent
        if agent_name not in config["agents"]:
            print(f"ERROR: Unknown agent '{agent_name}'. Available agents:")
            for name in sorted(config["agents"].keys()):
                print(f"  - {name}")
            sys.exit(1)

        agent_cfg = config["agents"][agent_name]

        if args.off:
            unload_agent(agent_name, agent_cfg)
            if agent_name not in state.get("disabled_agents", []):
                state.setdefault("disabled_agents", []).append(agent_name)
            state["last_changed_by"] = f"throttle_toggle.py --agent {agent_name} --off"
            save_state(state)
            print(f"  Agent {agent_name} disabled and state saved.")
            return

        if args.on:
            load_agent(agent_name, agent_cfg)
            if agent_name in state.get("disabled_agents", []):
                state["disabled_agents"].remove(agent_name)
            state["last_changed_by"] = f"throttle_toggle.py --agent {agent_name} --on"
            save_state(state)
            print(f"  Agent {agent_name} enabled and state saved.")
            return

        if args.interval is not None:
            hours = args.interval
            if hours <= 0:
                print("ERROR: Interval must be > 0")
                sys.exit(1)
            set_interval(agent_name, agent_cfg, hours, reason="(custom override)")
            state.setdefault("overrides", {})[agent_name] = hours
            state["last_changed_by"] = f"throttle_toggle.py --agent {agent_name} --interval {hours}"
            save_state(state)
            print(f"  Override saved for {agent_name}: {hours}h")
            return

        # No action specified for agent
        print(f"ERROR: Specify --off, --on, or --interval N with --agent")
        sys.exit(1)

    # No args at all
    parser.print_help()


if __name__ == "__main__":
    main()
