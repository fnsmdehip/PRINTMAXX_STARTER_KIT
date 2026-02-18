#!/bin/bash
# PRINTMAXX Session Bootstrap
# Run this ONE command at the start of every Claude session.
# Implements OpenClaw crash-recovery pattern: read state, orient, act.
#
# Usage: bash AUTOMATIONS/session_bootstrap.sh
#
# What it does (in order):
# 1. Show HEARTBEAT (<20 lines, 3 seconds to understand system state)
# 2. Show active-tasks.md (crash recovery: what was running when last session ended)
# 3. Refresh memory layers (heartbeat + active tasks + daily log)
# 4. Show venture health check
# 5. Show top priority actions
#
# After this runs, the agent knows EXACTLY what to do next.

set -euo pipefail

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
PYTHON="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"

echo "============================================"
echo "  PRINTMAXX SESSION BOOTSTRAP"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================"
echo ""

# 1. HEARTBEAT — system pulse
echo ">>> HEARTBEAT (3-second orientation)"
if [ -f "$BASE/OPS/HEARTBEAT.md" ]; then
    cat "$BASE/OPS/HEARTBEAT.md"
else
    echo "  [!] No HEARTBEAT.md — generating..."
    $PYTHON "$BASE/AUTOMATIONS/memory_manager.py" --heartbeat
fi
echo ""

# 2. ACTIVE TASKS — crash recovery
echo ">>> ACTIVE TASKS (crash recovery state)"
if [ -f "$BASE/OPS/active-tasks.md" ]; then
    cat "$BASE/OPS/active-tasks.md"
else
    echo "  [!] No active-tasks.md — clean start"
fi
echo ""

# 3. REFRESH MEMORY LAYERS
echo ">>> REFRESHING MEMORY LAYERS..."
$PYTHON "$BASE/AUTOMATIONS/memory_manager.py" --full 2>/dev/null || echo "  [!] Memory manager error (non-fatal)"
echo ""

# 4. CLOSED-LOOP PIPELINE STATUS
echo ">>> LEAD PIPELINE STATUS"
$PYTHON "$BASE/AUTOMATIONS/closed_loop_pipeline.py" --status 2>/dev/null || echo "  [!] Pipeline status error (non-fatal)"
echo ""

# 5. WHAT TO DO NEXT
echo "============================================"
echo "  READY TO EXECUTE"
echo "============================================"
echo ""
echo "Top actions (auto-ranked):"
echo "  1. Continue lead qualification:"
echo "     python3 AUTOMATIONS/closed_loop_pipeline.py --cycles 5 --batch 2000 --workers 30"
echo ""
echo "  2. Create platform accounts:"
echo "     open OPS/ACCOUNT_CREATION_NOW.md"
echo ""
echo "  3. Check daily playbook:"
echo "     cat OPS/AGENT_DAILY_PLAYBOOK.md"
echo ""
echo "  4. Ask yourself:"
echo "     'Based on what I know about the user, what workflows can I set up?"
echo "      What tools can I build on this computer to bring them closer to their goals?'"
echo ""
echo "  Then BUILD those tools. Don't ask. Execute."
echo ""
