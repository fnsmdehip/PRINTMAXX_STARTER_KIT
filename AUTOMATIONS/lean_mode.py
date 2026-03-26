#!/usr/bin/env python3
"""
Lean Mode Toggle — Disables LLM-consuming crons to conserve subscription tokens.

Keeps all pure-Python scripts running (scrapers, rankers, RBI, loops = $0 cost).
Disables claude -p callers (integrator, ventures, refiner = burns tokens).
Unloads launchd agents that run Claude sessions.

Usage:
    python3 lean_mode.py --on       # Enable lean mode (conserve tokens)
    python3 lean_mode.py --off      # Disable lean mode (full power)
    python3 lean_mode.py --status   # Show current mode
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
STATE_FILE = PROJECT / "AUTOMATIONS" / "agent" / "lean_mode_state.json"
FULL_BACKUP = PROJECT / "AUTOMATIONS" / "agent" / "cron_full_mode_backup.txt"
LOG = PROJECT / "AUTOMATIONS" / "logs" / "lean_mode.log"

# Scripts that call claude -p and burn subscription tokens
LLM_SCRIPTS = [
    "auto_approve",           # 2 claude -p calls
    "autonomous_integrator",  # 23 claude -p calls (heaviest)
    "venture_autonomy",       # 8 claude -p calls
    "venture_pipeline_brokering",  # 4 claude -p calls
    "user_sim_refiner",       # 5 claude -p calls
    "security_audit",         # 4 claude -p calls
]

# Launchd agents that run background Claude sessions
LAUNCHD_AGENTS = [
    "com.printmaxx.claude-sessions",
    "com.printmaxx.swarm.swarm_brain",
    "com.printmaxx.swarm.system_healer",
]


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [LEAN-MODE] {msg}"
    print(line)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def get_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {"mode": "full", "since": None}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def enable_lean():
    state = get_state()
    if state["mode"] == "lean":
        log("Already in lean mode")
        return

    # 1. Backup current crontab
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        FULL_BACKUP.write_text(result.stdout)
        log(f"Backed up full crontab ({len(result.stdout.splitlines())} lines)")

    # 2. Comment out LLM-consuming cron entries
    lines = result.stdout.splitlines() if result.returncode == 0 else []
    new_lines = []
    disabled = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            new_lines.append(line)
            continue
        # Check if this line runs an LLM script
        is_llm = any(s in stripped for s in LLM_SCRIPTS)
        # Also disable usage_optimizer (it triggers bursts of LLM calls)
        is_llm = is_llm or "usage_optimizer" in stripped
        if is_llm:
            new_lines.append(f"# LEAN_DISABLED: {line}")
            disabled += 1
            log(f"  Disabled: {line[:80]}")
        else:
            new_lines.append(line)

    # Reinstall
    proc = subprocess.run(
        ["crontab", "-"], input="\n".join(new_lines) + "\n",
        capture_output=True, text=True, timeout=10
    )
    if proc.returncode != 0:
        log(f"ERROR: Failed to install lean crontab: {proc.stderr[:100]}")
        return

    log(f"Disabled {disabled} LLM-consuming cron entries")

    # 3. Unload launchd agents
    for agent in LAUNCHD_AGENTS:
        plist = Path.home() / "Library" / "LaunchAgents" / f"{agent}.plist"
        if plist.exists():
            subprocess.run(["launchctl", "unload", str(plist)], capture_output=True, timeout=10)
            log(f"  Unloaded: {agent}")

    # 4. Save state
    save_state({"mode": "lean", "since": datetime.now().isoformat(), "disabled_count": disabled})
    log(f"LEAN MODE ON — {disabled} crons disabled, {len(LAUNCHD_AGENTS)} agents unloaded")
    log("Pure Python scripts still running: scanners, rankers, RBI, loops, digest = $0 cost")


def disable_lean():
    state = get_state()
    if state["mode"] == "full":
        log("Already in full mode")
        return

    # 1. Restore full crontab from backup
    if FULL_BACKUP.exists():
        backup = FULL_BACKUP.read_text()
        proc = subprocess.run(
            ["crontab", "-"], input=backup,
            capture_output=True, text=True, timeout=10
        )
        if proc.returncode == 0:
            log(f"Restored full crontab ({len(backup.splitlines())} lines)")
        else:
            log(f"ERROR: Failed to restore: {proc.stderr[:100]}")
            return
    else:
        # Fallback: uncomment LEAN_DISABLED lines
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = []
            restored = 0
            for line in result.stdout.splitlines():
                if line.strip().startswith("# LEAN_DISABLED:"):
                    lines.append(line.replace("# LEAN_DISABLED: ", ""))
                    restored += 1
                else:
                    lines.append(line)
            subprocess.run(
                ["crontab", "-"], input="\n".join(lines) + "\n",
                capture_output=True, text=True, timeout=10
            )
            log(f"Uncommented {restored} entries (no backup found)")

    # 2. Reload launchd agents
    for agent in LAUNCHD_AGENTS:
        plist = Path.home() / "Library" / "LaunchAgents" / f"{agent}.plist"
        if plist.exists():
            subprocess.run(["launchctl", "load", str(plist)], capture_output=True, timeout=10)
            log(f"  Reloaded: {agent}")

    # 3. Save state
    save_state({"mode": "full", "since": datetime.now().isoformat()})
    log("FULL MODE ON — all crons restored, all agents reloaded")


def show_status():
    state = get_state()
    print(f"Mode: {state['mode'].upper()}")
    print(f"Since: {state.get('since', 'unknown')}")
    if state["mode"] == "lean":
        print(f"Disabled crons: {state.get('disabled_count', '?')}")
        print(f"Launchd agents: unloaded")
        print()
        print("RUNNING (free, $0 cost):")
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            active = [l for l in result.stdout.splitlines()
                      if l.strip() and not l.strip().startswith("#")
                      and not l.strip().startswith("SHELL")
                      and not l.strip().startswith("PATH")
                      and not l.strip().startswith("BASE")
                      and not l.strip().startswith("PYTHON")]
            for l in active:
                script = l.split("AUTOMATIONS/")[-1].split(" ")[0] if "AUTOMATIONS/" in l else l[:60]
                print(f"  {script}")
            print(f"\nTotal active: {len(active)} entries (all free)")
        print()
        print("DISABLED (burns tokens):")
        for s in LLM_SCRIPTS:
            print(f"  {s}")
        print("  usage_optimizer")
    else:
        print("All crons active, all agents loaded")
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            active = [l for l in result.stdout.splitlines()
                      if l.strip() and not l.strip().startswith("#")
                      and not l.strip().startswith("SHELL")
                      and not l.strip().startswith("PATH")
                      and not l.strip().startswith("BASE")
                      and not l.strip().startswith("PYTHON")]
            print(f"Total active: {len(active)} cron entries")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lean Mode Toggle")
    parser.add_argument("--on", action="store_true", help="Enable lean mode (conserve tokens)")
    parser.add_argument("--off", action="store_true", help="Disable lean mode (full power)")
    parser.add_argument("--status", action="store_true", help="Show current mode")
    args = parser.parse_args()

    if args.on:
        enable_lean()
    elif args.off:
        disable_lean()
    elif args.status:
        show_status()
    else:
        parser.print_help()
