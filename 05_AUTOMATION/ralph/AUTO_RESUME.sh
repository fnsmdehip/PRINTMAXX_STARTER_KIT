#!/bin/bash

# AUTO_RESUME.sh - Automatically resume ralph loops after account limit reset
# Created: 2026-02-01
# Purpose: Handle account-wide Claude usage limits by auto-resuming after reset

PROJECT_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
WAIT_TIME=15300  # 4.25 hours = 15,300 seconds

echo "=== AUTO RESUME SCRIPT STARTED ==="
echo "Time: $(date)"
echo "Will wait $WAIT_TIME seconds (4.25 hours) for account limit reset..."
echo ""

# Wait for limit reset
sleep $WAIT_TIME

echo "=== LIMIT RESET - RESUMING LOOPS ==="
echo "Time: $(date)"
echo ""

# Kill any stuck processes
echo "Cleaning up any stuck processes..."
pkill -f "claude.*mega"
pkill -f "claude.*research"
sleep 5

# Resume mega loop from where it left off
echo "Resuming mega loop..."
cd "$PROJECT_DIR/ralph"
nohup ./loops/mega/run.sh 7 > logs/mega_auto_resume_$(date +%Y%m%d_%H%M%S).log 2>&1 &
MEGA_PID=$!
echo "Mega loop restarted: PID $MEGA_PID"

# Resume individual loops
echo "Resuming individual loops..."
nohup ./run_all_loops.sh > logs/individual_auto_resume_$(date +%Y%m%d_%H%M%S).log 2>&1 &
INDIVIDUAL_PID=$!
echo "Individual loops restarted: PID $INDIVIDUAL_PID"

echo ""
echo "=== RESUME COMPLETE ==="
echo "Mega loop PID: $MEGA_PID"
echo "Individual loops PID: $INDIVIDUAL_PID"
echo "Monitor with: tail -f $PROJECT_DIR/ralph/loops/mega/.ralph/activity.log"
echo ""
echo "Auto-resume script exiting. Loops running independently."
