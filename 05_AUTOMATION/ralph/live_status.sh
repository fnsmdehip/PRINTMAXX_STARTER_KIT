#!/bin/bash
# Live status updates for mega loop
# Shows updates every 15 seconds

cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph

clear
echo "======================================"
echo "MEGA RALPH LOOP - LIVE STATUS"
echo "Started monitoring at: $(date)"
echo "======================================"
echo ""

LOOP_COUNT=0
while true; do
    LOOP_COUNT=$((LOOP_COUNT + 1))

    echo "--- Update #$LOOP_COUNT at $(date +%H:%M:%S) ---"

    # Check if process running
    if [ -f "loops/mega/.ralph/mega.pid" ]; then
        PID=$(cat loops/mega/.ralph/mega.pid 2>/dev/null)
        if ps -p $PID > /dev/null 2>&1; then
            echo "✅ RUNNING (PID: $PID)"
        else
            echo "❌ NOT RUNNING (stale PID file)"
        fi
    else
        echo "❓ Status unknown (no PID file)"
    fi

    # Show current phase from main log
    CURRENT_ITER=$(tail -10 logs/mega_2026-02-01_0546.log 2>/dev/null | grep "=== Day" | tail -1)
    if [ -n "$CURRENT_ITER" ]; then
        echo "$CURRENT_ITER"
    fi

    # Show last activity
    LAST_OUTPUT=$(tail -20 loops/mega/.ralph/activity.log 2>/dev/null | grep "Token estimate" | tail -1)
    if [ -n "$LAST_OUTPUT" ]; then
        echo "Last output: $LAST_OUTPUT"
    else
        echo "No output yet..."
    fi

    # Show errors
    ERROR_COUNT=$(wc -l < loops/mega/.ralph/errors.log 2>/dev/null | tr -d ' ')
    if [ "$ERROR_COUNT" -gt 0 ]; then
        echo "⚠️  Errors: $ERROR_COUNT (check errors.log)"
    fi

    echo ""
    sleep 15
done
