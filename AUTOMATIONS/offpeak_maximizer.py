#!/usr/bin/env python3
"""OFFPEAK MAXIMIZER — Restructure all automations for Anthropic 2x window.

Anthropic March 2026 promo: 2x usage outside 8 AM - 2 PM ET, through March 27.
Weekends: 24/7 doubled.

This script:
1. Detects if we're in the 2x window
2. Schedules heavy-duty ralph loops during off-peak
3. Runs lightweight maintenance during on-peak (8 AM - 2 PM ET)
4. Goes HARD on weekends (full 24/7 doubled)

Usage:
  python3 AUTOMATIONS/offpeak_maximizer.py --status     # Show current window
  python3 AUTOMATIONS/offpeak_maximizer.py --schedule    # Install optimized cron
  python3 AUTOMATIONS/offpeak_maximizer.py --run-heavy   # Trigger heavy ralph loops NOW
  python3 AUTOMATIONS/offpeak_maximizer.py --revert      # Restore normal schedule
"""
from __future__ import annotations
import argparse, json, subprocess, sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
AUTO = PROJECT / "AUTOMATIONS"
STATE_FILE = AUTO / "offpeak_state.json"

PROMO_END = datetime(2026, 3, 27, 23, 59, 59)
PEAK_START_HOUR = 8   # 8 AM ET
PEAK_END_HOUR = 14    # 2 PM ET


def is_weekend() -> bool:
    return datetime.now().weekday() >= 5  # Sat=5, Sun=6


def is_offpeak() -> bool:
    if datetime.now() > PROMO_END:
        return False
    if is_weekend():
        return True  # weekends are ALL doubled
    hour = datetime.now().hour
    return hour < PEAK_START_HOUR or hour >= PEAK_END_HOUR


def promo_active() -> bool:
    return datetime.now() <= PROMO_END


def hours_remaining() -> float:
    delta = PROMO_END - datetime.now()
    return max(0, delta.total_seconds() / 3600)


def status():
    now = datetime.now()
    print(f"Current time: {now.strftime('%Y-%m-%d %H:%M %Z')} ({'Weekend' if is_weekend() else 'Weekday'})")
    print(f"Promo active: {'YES' if promo_active() else 'NO (expired)'}")
    print(f"Hours remaining: {hours_remaining():.1f}h ({hours_remaining()/24:.1f} days)")
    print(f"Current window: {'2x OFF-PEAK (doubled)' if is_offpeak() else 'ON-PEAK (normal)'}")
    if not is_weekend() and promo_active():
        if is_offpeak():
            if now.hour < PEAK_START_HOUR:
                mins_left = (PEAK_START_HOUR - now.hour) * 60 - now.minute
                print(f"2x window ends in: {mins_left} min (peak starts at {PEAK_START_HOUR}:00)")
            else:
                mins_left = (24 - now.hour + PEAK_START_HOUR) * 60 - now.minute
                print(f"2x window ends in: {mins_left} min (peak starts at {PEAK_START_HOUR}:00 tomorrow)")
        else:
            mins_left = (PEAK_END_HOUR - now.hour) * 60 - now.minute
            print(f"Peak ends in: {mins_left} min (2x resumes at {PEAK_END_HOUR}:00)")

    # What should be running
    if is_offpeak():
        print("\nSHOULD BE RUNNING: Heavy ralph loops, app building, content refinement,")
        print("  research synthesis, product generation, distribution optimization")
    else:
        print("\nSHOULD BE RUNNING: Light maintenance only (data janitor, system healer)")


# Heavy operations to run during off-peak
HEAVY_OPS = [
    {
        "name": "Research Deep Dive",
        "cmd": "python3 AUTOMATIONS/daily_research_orchestrator.py --full",
        "desc": "Full research pipeline — all scrapers + analysis",
    },
    {
        "name": "Alpha Processing",
        "cmd": "python3 AUTOMATIONS/alpha_auto_processor.py --process-new --batch 200",
        "desc": "Process 200 alpha entries (vs normal 50)",
    },
    {
        "name": "Content Generation Loop",
        "cmd": "python3 AUTOMATIONS/shakespeare_agent.py --generate --batch 20",
        "desc": "Generate 20 content pieces (vs normal 5)",
    },
    {
        "name": "Intelligence Router Full Scan",
        "cmd": "python3 AUTOMATIONS/intelligence_router.py --venture ALL --task general --json",
        "desc": "Full intelligence routing across all ventures",
    },
    {
        "name": "App Factory Pipeline",
        "cmd": "python3 AUTOMATIONS/app_factory_autopilot.py --run",
        "desc": "Full app factory autopilot — scrape, approve, spec, queue",
    },
    {
        "name": "Growth Strategist",
        "cmd": "python3 AUTOMATIONS/growth_strategist.py",
        "desc": "Generate growth strategies for all ventures",
    },
    {
        "name": "CEO Agent Cycle",
        "cmd": "python3 AUTOMATIONS/ceo_agent.py --cycle",
        "desc": "Full CEO orchestration cycle (16 phases)",
    },
    {
        "name": "Loop Closer Full",
        "cmd": "python3 AUTOMATIONS/loop_closer.py --cycle",
        "desc": "Close all open loops (decisions + feedback + pipeline + drift)",
    },
    {
        "name": "Venture Autonomy",
        "cmd": "python3 AUTOMATIONS/venture_autonomy.py --run-all",
        "desc": "Execute all 8 venture pipelines",
    },
    {
        "name": "Quality Gate",
        "cmd": "python3 AUTOMATIONS/quality_gate.py --gate",
        "desc": "Quality review all pending outputs",
    },
]


def install_offpeak_cron():
    """Install optimized cron entries that run heavy ops during 2x window."""
    if not promo_active():
        print("Promo expired. Not installing.")
        return

    new_entries = [
        "# === OFFPEAK MAXIMIZER (2x window through Mar 27) ===",
        "# Heavy ops: 2 PM - 8 AM ET weekdays + all day weekends",
        "",
        "# Every 2h during off-peak: full research pipeline",
        "0 14,16,18,20,22,0,2,4,6 * * 1-5 cd $BASE && $PYTHON AUTOMATIONS/daily_research_orchestrator.py --full >> AUTOMATIONS/logs/offpeak_research.log 2>&1",
        "",
        "# Every 3h during off-peak: alpha processing (200 batch)",
        "30 14,17,20,23,2,5 * * 1-5 cd $BASE && $PYTHON AUTOMATIONS/alpha_auto_processor.py --process-new --batch 200 >> AUTOMATIONS/logs/offpeak_alpha.log 2>&1",
        "",
        "# Every 2h during off-peak: content generation",
        "15 15,17,19,21,23,1,3,5,7 * * 1-5 cd $BASE && $PYTHON AUTOMATIONS/shakespeare_agent.py --generate --batch 20 >> AUTOMATIONS/logs/offpeak_content.log 2>&1",
        "",
        "# Every 4h during off-peak: app factory",
        "45 14,18,22,2,6 * * 1-5 cd $BASE && $PYTHON AUTOMATIONS/app_factory_autopilot.py --run >> AUTOMATIONS/logs/offpeak_appfactory.log 2>&1",
        "",
        "# Every 3h during off-peak: CEO cycle + loop closer",
        "0 15,18,21,0,3,6 * * 1-5 cd $BASE && $PYTHON AUTOMATIONS/ceo_agent.py --cycle >> AUTOMATIONS/logs/offpeak_ceo.log 2>&1",
        "20 15,18,21,0,3,6 * * 1-5 cd $BASE && $PYTHON AUTOMATIONS/loop_closer.py --cycle >> AUTOMATIONS/logs/offpeak_loops.log 2>&1",
        "",
        "# Weekend BLITZ — every 90 min, everything runs",
        "0 */2 * * 0,6 cd $BASE && $PYTHON AUTOMATIONS/daily_research_orchestrator.py --full >> AUTOMATIONS/logs/weekend_research.log 2>&1",
        "15 */2 * * 0,6 cd $BASE && $PYTHON AUTOMATIONS/alpha_auto_processor.py --process-new --batch 200 >> AUTOMATIONS/logs/weekend_alpha.log 2>&1",
        "30 */2 * * 0,6 cd $BASE && $PYTHON AUTOMATIONS/shakespeare_agent.py --generate --batch 20 >> AUTOMATIONS/logs/weekend_content.log 2>&1",
        "45 */2 * * 0,6 cd $BASE && $PYTHON AUTOMATIONS/venture_autonomy.py --run-all >> AUTOMATIONS/logs/weekend_ventures.log 2>&1",
        "0 */3 * * 0,6 cd $BASE && $PYTHON AUTOMATIONS/app_factory_autopilot.py --run >> AUTOMATIONS/logs/weekend_appfactory.log 2>&1",
        "30 */3 * * 0,6 cd $BASE && $PYTHON AUTOMATIONS/ceo_agent.py --cycle >> AUTOMATIONS/logs/weekend_ceo.log 2>&1",
        "0 */4 * * 0,6 cd $BASE && $PYTHON AUTOMATIONS/growth_strategist.py >> AUTOMATIONS/logs/weekend_growth.log 2>&1",
        "",
        "# === END OFFPEAK MAXIMIZER ===",
    ]

    # Get current crontab
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        current = result.stdout
    except Exception:
        current = ""

    # Remove old offpeak entries if any
    lines = current.splitlines()
    filtered = []
    in_offpeak = False
    for line in lines:
        if "OFFPEAK MAXIMIZER" in line and "===" in line:
            in_offpeak = not in_offpeak
            continue
        if not in_offpeak:
            filtered.append(line)

    # Add new entries
    new_cron = "\n".join(filtered) + "\n" + "\n".join(new_entries) + "\n"

    # Install
    proc = subprocess.run(["crontab", "-"], input=new_cron, text=True, capture_output=True)
    if proc.returncode == 0:
        print(f"Installed {len(new_entries)} offpeak cron entries")
        print(f"Heavy ops run 2 PM - 8 AM ET weekdays + ALL DAY weekends")
        print(f"Promo ends: March 27, 2026 ({hours_remaining():.0f}h remaining)")

        # Save state
        STATE_FILE.write_text(json.dumps({
            "installed": True,
            "installed_at": datetime.now().isoformat(),
            "promo_ends": "2026-03-27T23:59:59",
        }, indent=2))
    else:
        print(f"Failed to install cron: {proc.stderr}")


def revert_cron():
    """Remove offpeak cron entries."""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        lines = result.stdout.splitlines()
    except Exception:
        print("No crontab to revert")
        return

    filtered = []
    in_offpeak = False
    for line in lines:
        if "OFFPEAK MAXIMIZER" in line and "===" in line:
            in_offpeak = not in_offpeak
            continue
        if not in_offpeak:
            filtered.append(line)

    new_cron = "\n".join(filtered) + "\n"
    subprocess.run(["crontab", "-"], input=new_cron, text=True)
    print("Removed all offpeak cron entries. Back to normal schedule.")

    if STATE_FILE.exists():
        STATE_FILE.unlink()


def main():
    parser = argparse.ArgumentParser(description="Offpeak Maximizer for Anthropic 2x promo")
    parser.add_argument("--status", action="store_true", help="Show current window status")
    parser.add_argument("--schedule", action="store_true", help="Install optimized off-peak cron")
    parser.add_argument("--revert", action="store_true", help="Remove off-peak cron entries")
    parser.add_argument("--run-heavy", action="store_true", help="Trigger heavy ops NOW")
    args = parser.parse_args()

    if args.status:
        status()
    elif args.schedule:
        install_offpeak_cron()
    elif args.revert:
        revert_cron()
    elif args.run_heavy:
        if not is_offpeak():
            print("WARNING: Currently in peak window (8 AM - 2 PM ET). Running anyway but tokens are NOT doubled.")
        for op in HEAVY_OPS:
            print(f"\n{'='*60}")
            print(f"Running: {op['name']}")
            print(f"  {op['desc']}")
            subprocess.Popen(
                f"cd {PROJECT} && {op['cmd']} >> AUTOMATIONS/logs/offpeak_manual.log 2>&1",
                shell=True,
            )
            print(f"  Launched in background")
    else:
        status()


if __name__ == "__main__":
    main()
