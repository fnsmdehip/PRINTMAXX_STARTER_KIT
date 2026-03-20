#!/usr/bin/env python3
"""
SYSTEM HEALER FIX SCRIPT
Remediates broken systems found in health check
"""
import subprocess
import os
import json
import time
from pathlib import Path

BASE = Path(__file__).parent.parent
AUTOMATIONS = BASE / "AUTOMATIONS"
LOGS = AUTOMATIONS / "logs"

def run_cmd(cmd, description):
    """Run a command and log results"""
    print(f"\n📋 {description}")
    print(f"   CMD: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.stdout:
            print(f"   OUT: {result.stdout[:200]}")
        if result.stderr:
            print(f"   ERR: {result.stderr[:200]}")
        print(f"   EXIT: {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        print(f"   EXCEPTION: {e}")
        return False

def fix_agent_swarm():
    """Deploy agent swarm"""
    return run_cmd(
        f"cd {BASE} && /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 AUTOMATIONS/agent_swarm.py --deploy --force",
        "Deploying agent swarm (this may take 2-3 min)"
    )

def fix_research_lock():
    """Unlock research orchestrator"""
    lock_files = [
        AUTOMATIONS / "research_orchestrator.lock",
        AUTOMATIONS / ".research_orchestrator.lock",
        AUTOMATIONS / "locks" / "research_orchestrator.lock",
    ]
    for lf in lock_files:
        if lf.exists():
            try:
                lf.unlink()
                print(f"✓ Removed lock file: {lf}")
                return True
            except Exception as e:
                print(f"✗ Failed to remove {lf}: {e}")
    print("ℹ️  No lock files found (or already cleaned)")
    return True

def test_decision_engine():
    """Test decision engine"""
    return run_cmd(
        f"cd {BASE} && /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 AUTOMATIONS/decision_engine.py --cycle --verbose 2>&1 | head -20",
        "Testing decision_engine"
    )

def check_python_env():
    """Verify Python environment"""
    return run_cmd(
        "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 --version",
        "Checking Python environment"
    )

def check_launchd_status():
    """Check launchd status"""
    return run_cmd(
        "launchctl list | grep -E 'printmaxx|claude' | head -10",
        "Checking launchd agents"
    )

def main():
    print("=" * 70)
    print("SYSTEM HEALER — FIX CYCLE")
    print("=" * 70)
    print(f"Working directory: {BASE}")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Phase 1: Diagnosis
    print("\n🔍 PHASE 1: DIAGNOSIS")
    check_python_env()
    check_launchd_status()

    # Phase 2: Fix
    print("\n🔧 PHASE 2: REMEDIATION")
    fix_research_lock()
    fix_agent_swarm()

    # Phase 3: Verify
    print("\n✅ PHASE 3: VERIFICATION")
    test_decision_engine()

    print("\n" + "=" * 70)
    print("FIX CYCLE COMPLETE")
    print("Monitor logs over next 30 min: agent_swarm.log, decision_engine.log")
    print("=" * 70)

if __name__ == "__main__":
    main()
