#!/bin/bash
# Daily Ops Ralph Loop Runner

PROJECT_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
LOOP_DIR="$PROJECT_DIR/ralph/loops/daily_ops"
LOG_DIR="$PROJECT_DIR/ralph/logs"

# Create log directory if needed
mkdir -p "$LOG_DIR"

# Timestamp for log file
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/daily_ops_${TIMESTAMP}.log"

echo "Starting Daily Ops Loop at $(date)" | tee "$LOG_FILE"
echo "Log file: $LOG_FILE"

# Run 7 iterations (one per task)
ITERATIONS=7
for i in $(seq 1 $ITERATIONS); do
    echo "" | tee -a "$LOG_FILE"
    echo "========================================" | tee -a "$LOG_FILE"
    echo "Iteration $i of $ITERATIONS - $(date)" | tee -a "$LOG_FILE"
    echo "========================================" | tee -a "$LOG_FILE"

    # Run claude with the prompt
    cd "$PROJECT_DIR"
# SAFETY: Load guardrails wrapper
source "$PROJECT_DIR/AUTOMATIONS/guardrails_wrapper.sh"

    cat "$LOOP_DIR/prompt.md" | claude --print --dangerously-skip-permissions \
        --model claude-opus-4-6 \
        --allowedTools "Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,TodoWrite" \
        2>&1 | tee -a "$LOG_FILE"

    # Brief pause between iterations
    sleep 5
done

echo "" | tee -a "$LOG_FILE"
echo "Daily Ops Loop completed at $(date)" | tee -a "$LOG_FILE"
echo "Total iterations: $ITERATIONS"
