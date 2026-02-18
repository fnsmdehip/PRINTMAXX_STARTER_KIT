#!/bin/bash
# MEGA RALPH - Quick launcher
# Replaces run_all_loops.sh with ONE unified loop
# Usage: ./run_mega.sh [days]
#
# Default: 1 day = 21 iterations (OVERNIGHT RUN)
#   Day cycle: 3 research + 1 reflection + 6 content + 5 execution + 5 intelligence + 1 checkpoint
#
# Examples:
#   ./run_mega.sh        # 1 day overnight (default)
#   ./run_mega.sh 3      # 3 days = 63 iterations
#   ./run_mega.sh 5      # 5 days = 105 iterations
#   ./run_mega.sh 7      # Full week = 147 iterations

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DAYS=${1:-1}
TIMESTAMP=$(date +%Y-%m-%d_%H%M)
LOG_DIR="$SCRIPT_DIR/logs"
MEGA_DIR="$SCRIPT_DIR/loops/mega"
PROJECT_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"

mkdir -p "$LOG_DIR"

ITERATIONS_PER_DAY=21
TOTAL_ITERATIONS=$((DAYS * ITERATIONS_PER_DAY))

echo "============================================"
echo "MEGA RALPH LOOP - Launching"
echo "============================================"
echo ""
echo "  Days:             $DAYS"
echo "  Iterations/day:   $ITERATIONS_PER_DAY"
echo "  Total iterations: $TOTAL_ITERATIONS"
echo "  Sleep between:    10s"
echo "  Model:            opus (maximum quality)"
echo "  Mode:             AUTONOMOUS (no human approval needed)"
echo "  Safety:           No Bash, No delete, Project folder only"
echo "  Scraping:         Chrome MCP only"
echo ""
echo "  Day Cycle:"
echo "    1-3:   DAILY_RESEARCH"
echo "    4:     REFLECTION"
echo "    5-10:  CONTENT_GENERATION"
echo "    11-15: EXECUTION"
echo "    16-20: INTELLIGENCE"
echo "    21:    CHECKPOINT"
echo ""
echo "  Log: $LOG_DIR/mega_$TIMESTAMP.log"
echo ""
echo "============================================"
echo ""

# Launch in background with nohup
nohup "$MEGA_DIR/run.sh" "$DAYS" > "$LOG_DIR/mega_$TIMESTAMP.log" 2>&1 &
PID=$!

echo "Launched! PID: $PID"
echo ""
echo "--- Monitor ---"
echo ""
echo "  Live log:"
echo "    tail -f $LOG_DIR/mega_$TIMESTAMP.log"
echo ""
echo "  Progress file:"
echo "    cat $MEGA_DIR/.ralph/progress.md"
echo ""
echo "  Activity log:"
echo "    tail -100 $MEGA_DIR/.ralph/activity.log"
echo ""
echo "  Errors:"
echo "    cat $MEGA_DIR/.ralph/errors.log"
echo ""
echo "  Tracker:"
echo "    head -50 $PROJECT_DIR/LEDGER/MEGA_RALPH_TRACKER.csv"
echo ""
echo "  Checkpoints (human review):"
echo "    ls $MEGA_DIR/checkpoints/"
echo ""
echo "  Output:"
echo "    ls $MEGA_DIR/output/"
echo ""
echo "--- Control ---"
echo ""
echo "  Stop:"
echo "    kill $PID"
echo ""
echo "  Check if running:"
echo "    ps -p $PID"
echo ""
echo "  PID saved to: $MEGA_DIR/.ralph/mega.pid"

# Save PID for later reference
echo "$PID" > "$MEGA_DIR/.ralph/mega.pid"
echo "$TIMESTAMP" > "$MEGA_DIR/.ralph/mega.timestamp"
