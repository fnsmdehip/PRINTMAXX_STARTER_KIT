#!/usr/bin/env python3
"""Find potentially dead Python scripts in AUTOMATIONS"""

from pathlib import Path
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT_ROOT / "AUTOMATIONS"

def get_active_scripts():
    """Extract scripts called from cron and code"""
    active = set()

    # Check crontab
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "python3" in line and ".py" in line:
                # Extract script name
                parts = line.split("python3")
                if len(parts) > 1:
                    script = parts[1].strip().split()[0]
                    if script.endswith(".py"):
                        # Get just the filename
                        active.add(Path(script).name)
    except:
        pass

    # Check CLAUDE.md for referenced scripts
    claude_md = PROJECT_ROOT / ".claude" / "CLAUDE.md"
    if claude_md.exists():
        content = claude_md.read_text()
        # Simple pattern: python3 AUTOMATIONS/script.py
        import re
        matches = re.findall(r'AUTOMATIONS/([a-zA-Z0-9_.-]+\.py)', content)
        active.update(matches)

    # Check common orchestrator/main scripts
    main_scripts = [
        "agent_swarm.py",
        "venture_autonomy.py",
        "ceo_agent.py",
        "loop_closer.py",
        "decision_engine.py",
        "autonomous_orchestrator.py",
        "control_panel.py",
        "data_janitor_v2.py",
    ]
    active.update(main_scripts)

    return active

def analyze_scripts():
    """Analyze which scripts are potentially dead"""
    all_scripts = sorted([f.name for f in AUTOMATIONS.glob("*.py")])
    active = get_active_scripts()
    potentially_dead = [s for s in all_scripts if s not in active and not s.startswith("_")]

    print(f"Total scripts in AUTOMATIONS: {len(all_scripts)}")
    print(f"Scripts called by cron/code: {len(active)}")
    print(f"Potentially dead scripts: {len(potentially_dead)}\n")

    if potentially_dead:
        print("Dead scripts (showing first 20):")
        for script in potentially_dead[:20]:
            size_kb = (AUTOMATIONS / script).stat().st_size / 1024
            print(f"  - {script} ({size_kb:.1f}KB)")

    return len(potentially_dead)

if __name__ == "__main__":
    analyze_scripts()
