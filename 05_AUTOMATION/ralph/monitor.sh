#!/bin/bash
# Live monitoring script for mega ralph loop
# Usage: ./monitor.sh

echo "======================================"
echo "MEGA RALPH LOOP - LIVE MONITOR"
echo "======================================"
echo ""

while true; do
    clear
    echo "=== MEGA RALPH LOOP STATUS ==="
    echo "Time: $(date)"
    echo ""

    # Check if running
    if pgrep -f "run_mega.sh" > /dev/null; then
        echo "✅ STATUS: RUNNING"
        PID=$(pgrep -f "run_mega.sh")
        echo "   PID: $PID"
    else
        echo "❌ STATUS: NOT RUNNING"
    fi
    echo ""

    # Show current progress
    if [ -f "loops/mega/.ralph/progress.md" ]; then
        echo "=== CURRENT PROGRESS ==="
        grep -A 5 "## Current State" loops/mega/.ralph/progress.md | tail -7
        echo ""
        grep -A 3 "## Last Completed Task" loops/mega/.ralph/progress.md | tail -4
        echo ""
    fi

    # Show recent activity (last 10 lines)
    if [ -f "loops/mega/.ralph/activity.log" ]; then
        echo "=== RECENT ACTIVITY (last 10 lines) ==="
        tail -10 loops/mega/.ralph/activity.log
        echo ""
    fi

    # Show checkpoint count
    if [ -d "loops/mega/checkpoints" ]; then
        CHECKPOINT_COUNT=$(find loops/mega/checkpoints -name "PENDING_*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
        echo "=== CHECKPOINTS ==="
        echo "Pending items: $CHECKPOINT_COUNT"
        if [ $CHECKPOINT_COUNT -gt 0 ]; then
            find loops/mega/checkpoints -name "PENDING_*.md" -type f -exec basename {} \;
        fi
        echo ""
    fi

    # Show tracker stats
    if [ -f "../LEDGER/MEGA_RALPH_TRACKER.csv" ]; then
        echo "=== TRACKER STATS ==="
        TOTAL_TASKS=$(tail -n +2 ../LEDGER/MEGA_RALPH_TRACKER.csv 2>/dev/null | wc -l | tr -d ' ')
        COMPLETED=$(tail -n +2 ../LEDGER/MEGA_RALPH_TRACKER.csv 2>/dev/null | grep -c ",completed," || echo "0")
        IN_PROGRESS=$(tail -n +2 ../LEDGER/MEGA_RALPH_TRACKER.csv 2>/dev/null | grep -c ",in_progress," || echo "0")
        echo "Total tasks: $TOTAL_TASKS"
        echo "Completed: $COMPLETED"
        echo "In progress: $IN_PROGRESS"
        echo ""
    fi

    echo "=== COMMANDS ==="
    echo "Ctrl+C to stop monitoring (loop keeps running)"
    echo "To stop loop: pkill -f run_mega.sh"
    echo ""
    echo "Refreshing in 10 seconds..."

    sleep 10
done
