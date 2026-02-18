#!/bin/bash
# Master Ops Maintenance Ralph Loop Runner
# Keeps PRINTMAXX_MASTER_OPS.xlsx and operational tracking systems current.
#
# Usage:
#   ./run.sh          # Run until all 8 tasks complete
#   ./run.sh 3        # Run max 3 iterations

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
PROGRESS_DIR="$SCRIPT_DIR/.ralph"
LOG_DIR="$PROJECT_DIR/ralph/logs"
OUTPUT_DIR="$SCRIPT_DIR/output"

# Create directories
mkdir -p "$PROGRESS_DIR" "$LOG_DIR" "$OUTPUT_DIR"

# Max iterations (default 10 = 8 tasks + 2 buffer for retries)
MAX_ITERATIONS=${1:-10}

# Timestamp for log file
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/master_ops_${TIMESTAMP}.log"

echo "Starting Master Ops Ralph Loop at $(date)" | tee "$LOG_FILE"
echo "Max iterations: $MAX_ITERATIONS" | tee -a "$LOG_FILE"
echo "Log file: $LOG_FILE"
echo ""

iteration=1

while [ $iteration -le $MAX_ITERATIONS ]; do
    echo "========================================" | tee -a "$LOG_FILE"
    echo "Iteration $iteration of $MAX_ITERATIONS - $(date)" | tee -a "$LOG_FILE"
    echo "========================================" | tee -a "$LOG_FILE"

    # Check if all tasks are done
    if grep -q "ALL TASKS COMPLETE" "$PROGRESS_DIR/progress.md" 2>/dev/null; then
        echo "All tasks complete. Exiting loop." | tee -a "$LOG_FILE"
        break
    fi

    # Check if any tasks remain with passes: false
    if ! grep -q '"passes": false' "$SCRIPT_DIR/prd.json" 2>/dev/null; then
        echo "No remaining tasks with passes: false. Exiting loop." | tee -a "$LOG_FILE"
        break
    fi

    # Run claude with the prompt from project root
    cd "$PROJECT_DIR"
# SAFETY: Load guardrails wrapper
source "$PROJECT_DIR/AUTOMATIONS/guardrails_wrapper.sh"

    cat "$SCRIPT_DIR/PROMPT.md" | claude --print --dangerously-skip-permissions \
        --model claude-opus-4-6 \
        2>&1 | tee -a "$LOG_FILE"

    echo "" | tee -a "$LOG_FILE"
    iteration=$((iteration + 1))

    # Brief pause between iterations to avoid hammering API
    sleep 5
done

echo "" | tee -a "$LOG_FILE"
echo "Master Ops Loop finished at $(date)" | tee -a "$LOG_FILE"
echo "Total iterations run: $((iteration - 1))" | tee -a "$LOG_FILE"
echo "Log saved to: $LOG_FILE"
