#!/bin/bash

# Ralph Loop Runner Template
# Copy this to loop_name/run.sh and customize LOOP_NAME and PROMPT

# === CUSTOMIZE THESE ===
LOOP_NAME="your_loop_name"
# === END CUSTOMIZE ===

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT"
PROMPT_FILE="$SCRIPT_DIR/prompt.md"
STATE_DIR="$SCRIPT_DIR/.ralph"
PROGRESS_FILE="$STATE_DIR/progress.md"
ERRORS_LOG="$STATE_DIR/errors.log"
ACTIVITY_LOG="$STATE_DIR/activity.log"
OUTPUT_DIR="$SCRIPT_DIR/output"

# Number of iterations (passed as arg or default)
MAX_ITERATIONS=${1:-10}

# Initialize directories
mkdir -p "$STATE_DIR" "$OUTPUT_DIR"
touch "$ERRORS_LOG" "$ACTIVITY_LOG"

echo "============================================"
echo "Ralph Loop: $LOOP_NAME"
echo "Max iterations: $MAX_ITERATIONS"
echo "Started: $(date)"
echo "============================================"
echo ""
echo "Started at: $(date)" >> "$ACTIVITY_LOG"

iteration=0

while [ $iteration -lt $MAX_ITERATIONS ]; do
  iteration=$((iteration + 1))

  echo "=== Iteration $iteration / $MAX_ITERATIONS at $(date) ===" | tee -a "$ACTIVITY_LOG"

  # Check completion if progress file exists
  if [ -f "$PROGRESS_FILE" ]; then
    pending=$(grep -c "PENDING\|pending\|TODO" "$PROGRESS_FILE" 2>/dev/null || echo "0")
    if [ "$pending" -eq 0 ]; then
      echo "All tasks complete. Exiting loop." | tee -a "$ACTIVITY_LOG"
      exit 0
    fi
  fi

  # Run Claude in print mode (non-interactive, autonomous)
  if command -v claude &> /dev/null; then
    cd "$PROJECT_DIR"

    # Claude CLI flags:
    # -p = print mode (non-interactive, exits after response)
    # --dangerously-skip-permissions = no permission prompts (for overnight runs)
    # --model sonnet = use sonnet (fast, capable)

    claude -p \
      --dangerously-skip-permissions \
      --model sonnet \
      "$(cat "$PROMPT_FILE")" \
      2>> "$ERRORS_LOG" >> "$ACTIVITY_LOG" || {
        echo "ERROR in iteration $iteration" >> "$ERRORS_LOG"
      }
  else
    echo "ERROR: claude CLI not found" | tee -a "$ERRORS_LOG"
    exit 1
  fi

  # Pause between iterations (rate limiting, cost control)
  sleep 5
done

echo ""
echo "============================================"
echo "Loop complete: $(date)"
echo "Iterations: $iteration"
echo "Check: $ACTIVITY_LOG"
echo "============================================"
