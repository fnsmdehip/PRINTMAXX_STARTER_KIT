#!/bin/bash
# Live progress monitor - updates every 5 seconds

while true; do
    clear
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║       MEGA RALPH LOOPS - LIVE PROGRESS MONITOR                ║"
    echo "║       $(date)                            ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Check running processes
    MEGA_PID=$(pgrep -f "loops/mega/run.sh" | head -1)
    LOOP_COUNT=$(ps aux | grep "loops/" | grep run.sh | grep -v grep | wc -l | tr -d ' ')
    AGENT_COUNT=$(ps aux | grep "claude -p" | grep -v grep | wc -l | tr -d ' ')
    
    echo "┌─ SYSTEM STATUS ─────────────────────────────────────────────┐"
    echo "│ Running Loops: $LOOP_COUNT                                            │"
    echo "│ Active Claude Agents: $AGENT_COUNT                                    │"
    if [ -n "$MEGA_PID" ]; then
        echo "│ Mega Loop: ✅ RUNNING (PID: $MEGA_PID)                              │"
    else
        echo "│ Mega Loop: ❌ NOT RUNNING                                    │"
    fi
    echo "└─────────────────────────────────────────────────────────────┘"
    echo ""
    
    # Show mega loop current iteration
    if [ -f "loops/mega/.ralph/activity.log" ]; then
        echo "┌─ MEGA LOOP - CURRENT ITERATION ─────────────────────────────┐"
        CURRENT_ITER=$(tail -20 loops/mega/.ralph/activity.log | grep "=== Day" | tail -1)
        if [ -n "$CURRENT_ITER" ]; then
            echo "│ $CURRENT_ITER"
        else
            echo "│ Starting up...                                              │"
        fi
        echo "└─────────────────────────────────────────────────────────────┘"
        echo ""
        
        echo "┌─ RECENT FINDINGS (last 15 lines) ───────────────────────────┐"
        tail -15 loops/mega/.ralph/activity.log | sed 's/^/│ /'
        echo "└─────────────────────────────────────────────────────────────┘"
    fi
    
    echo ""
    echo "┌─ LEDGER UPDATES ────────────────────────────────────────────┐"
    echo "│ Recent file updates (last 5 min):                           │"
    find ../LEDGER -name "*.csv" -mmin -5 -exec basename {} \; 2>/dev/null | head -5 | sed 's/^/│   ✓ /' || echo "│   No recent updates"
    echo "└─────────────────────────────────────────────────────────────┘"
    
    echo ""
    echo "Press Ctrl+C to stop monitoring (loops keep running)"
    echo "Refreshing in 5 seconds..."
    
    sleep 5
done
