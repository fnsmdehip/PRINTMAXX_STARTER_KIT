#!/bin/bash
# PRINTMAXX Ralph Overnight Loop
# Launches Claude Code in autonomous mode for overnight research + building
# Uses the Ralph Wiggum pattern: fresh context each iteration, state in files
#
# Usage: bash ralph_overnight_loop.sh [max_iterations] [sleep_seconds]
# Default: 5 iterations, 60s between each

BASE_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
CLAUDE="/Users/macbookpro/.local/bin/claude"
MAX_ITERATIONS=${1:-5}
SLEEP_BETWEEN=${2:-60}
LOG_DIR="$BASE_DIR/AUTOMATIONS/logs"
DATE=$(date +%Y-%m-%d)
RALPH_LOG="$LOG_DIR/ralph_overnight_${DATE}.log"
PROGRESS_FILE="$BASE_DIR/ralph/overnight_progress.md"

mkdir -p "$LOG_DIR"
mkdir -p "$BASE_DIR/ralph"

log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$RALPH_LOG"
}

# Initialize progress file
cat > "$PROGRESS_FILE" << 'PROGRESS'
# Ralph Overnight Progress

## Status: RUNNING
## Started: $(date)

### Completed Iterations:
PROGRESS

RALPH_PROMPT="You are PRINTMAXX Ralph Overnight Agent. Read .claude/CLAUDE.md for full context.

YOUR MISSION: Do the highest-value work possible in this iteration. You have ~15 min.

## Priority Order:
1. Check ralph/overnight_progress.md for what previous iterations completed
2. Check OPS/FULL_REQUEST_AUDIT.md for unfinished user requests
3. Check LEDGER/ALPHA_STAGING.csv for PENDING_REVIEW entries - auto-vet them
4. Run any scrapers that haven't run today (check AUTOMATIONS/logs/)
5. Generate content from approved alpha (Zero Waste Protocol)
6. Build any partially-built systems that need finishing

## Rules:
- Write what you did to ralph/overnight_progress.md (APPEND, don't overwrite)
- Auto-approve alpha that has specific numbers + clear method
- Auto-reject alpha that is pure hype with no specifics
- Generate 5+ social posts from any approved alpha
- Run scrapers against real APIs (not mock data)
- If you hit errors, log them and move to next task

## Key Files:
- LEDGER/ALPHA_STAGING.csv - alpha to vet
- AUTOMATIONS/leads/ - lead data
- OPS/FULL_REQUEST_AUDIT.md - user request audit
- .claude/rules/alpha-review.md - vetting rules
- .claude/rules/copy-style.md - content voice

DO NOT ask questions. Just execute the highest-value task and write results."

log "============================================"
log "RALPH OVERNIGHT LOOP - $DATE"
log "Max iterations: $MAX_ITERATIONS"
log "============================================"

for i in $(seq 1 $MAX_ITERATIONS); do
    log ""
    log "--- Iteration $i/$MAX_ITERATIONS ---"

    # Check if we should stop (token limit file)
    if [ -f "/tmp/printmaxx_stop_ralph" ]; then
        log "Stop file found, ending loop"
        rm -f "/tmp/printmaxx_stop_ralph"
        break
    fi

    # Run Claude with the ralph prompt
    echo "$RALPH_PROMPT" | timeout 900 "$CLAUDE" \
        --dangerously-skip-permissions \
        --print \
        -p "$BASE_DIR" \
        >> "$RALPH_LOG" 2>&1 || {
        log "Iteration $i ended (timeout or error)"
    }

    # Append iteration completion to progress
    echo "- Iteration $i completed at $(date '+%H:%M:%S')" >> "$PROGRESS_FILE"

    log "Iteration $i complete, sleeping ${SLEEP_BETWEEN}s"
    sleep "$SLEEP_BETWEEN"
done

log ""
log "============================================"
log "RALPH OVERNIGHT LOOP COMPLETE"
log "Iterations: $MAX_ITERATIONS"
log "============================================"

# Update progress file
echo "" >> "$PROGRESS_FILE"
echo "## Status: COMPLETED" >> "$PROGRESS_FILE"
echo "## Finished: $(date)" >> "$PROGRESS_FILE"
