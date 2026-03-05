#!/bin/bash
# PRINTMAXX Claude Code Session Scheduler
# ========================================
# Called by cron to run autonomous Claude sessions.
# Handles: disk guard, caffeinate, prompt generation, Claude execution, output routing.
#
# Usage:
#   bash schedule_claude.sh morning     # Morning briefing (7 AM)
#   bash schedule_claude.sh midday      # Midday analysis (1 PM)
#   bash schedule_claude.sh evening     # Evening summary (6 PM)
#
# Cron entries (add to crontab):
#   0 7 * * * bash /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/schedule_claude.sh morning
#   0 13 * * * bash /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/schedule_claude.sh midday
#   0 18 * * * bash /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/schedule_claude.sh evening

set -uo pipefail

SESSION_TYPE="${1:-morning}"
BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
PYTHON="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
CLAUDE="/Users/macbookpro/.local/bin/claude"
LOG_DIR="$BASE/AUTOMATIONS/logs/sessions"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG="$LOG_DIR/${SESSION_TYPE}_${TIMESTAMP}.log"
LOCK_FILE="$BASE/AUTOMATIONS/logs/.session_lock"

mkdir -p "$LOG_DIR"

log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG"; }

# ── SAFETY: Disk space guard ──
AVAIL_KB=$(df -k "$BASE" | tail -1 | awk '{print $4}')
if [ "$AVAIL_KB" -lt 2097152 ]; then
    log "ABORT: Only $((AVAIL_KB / 1024))MB free (<2GB)"
    exit 1
fi

# ── SAFETY: Lock file (prevent double-runs, PID liveness check) ──
if [ -f "$LOCK_FILE" ]; then
    LOCK_PID=$(cat "$LOCK_FILE" 2>/dev/null)
    if [ -n "$LOCK_PID" ] && kill -0 "$LOCK_PID" 2>/dev/null; then
        log "SKIP: Session already running (PID $LOCK_PID alive)"
        exit 0
    fi
    log "WARNING: Dead lock (PID $LOCK_PID gone), removing"
    rm -f "$LOCK_FILE"
fi
echo "$$" > "$LOCK_FILE"
trap "rm -f '$LOCK_FILE'" EXIT

# ── Load guardrails ──
source "$BASE/AUTOMATIONS/guardrails_wrapper.sh" 2>/dev/null || true

ACTIVE_TASKS="$BASE/OPS/active-tasks.md"

log "=== PRINTMAXX SESSION: $SESSION_TYPE ==="
log "Date: $DATE | PID: $$ | Disk: $((AVAIL_KB / 1024))MB free"

# ── Step 0: Refresh memory (heartbeat + active-tasks + daily log) ──
log "Step 0: Refreshing memory layer..."
$PYTHON "$BASE/AUTOMATIONS/memory_manager.py" --full >> "$LOG" 2>&1 || true

# ── Step 1: Generate session prompt ──
log "Step 1: Generating $SESSION_TYPE prompt..."
$PYTHON "$BASE/AUTOMATIONS/autonomous_orchestrator.py" --prep "$SESSION_TYPE" >> "$LOG" 2>&1
PREP_EXIT=$?

PROMPT="$BASE/AUTOMATIONS/session_prompts/session_${SESSION_TYPE}.md"
if [ $PREP_EXIT -ne 0 ] || [ ! -f "$PROMPT" ]; then
    log "ERROR: Prompt generation failed (exit $PREP_EXIT)"
    exit 1
fi
log "Prompt ready: $(wc -l < "$PROMPT") lines"

# ── Step 2: Keep Mac awake ──
caffeinate -dims -t 2400 &
CAFE_PID=$!
log "Caffeinate started (PID $CAFE_PID, 40min)"

# ── Step 3: Run Claude Code ──
log "Step 3: Launching Claude Code..."
CLAUDE_LOG="$LOG_DIR/claude_${SESSION_TYPE}_${TIMESTAMP}.log"

# Crash recovery: write to active-tasks.md before Claude launch
echo "SESSION_IN_FLIGHT: $SESSION_TYPE started at $(date '+%Y-%m-%d %H:%M:%S') PID $$" >> "$ACTIVE_TASKS"

if [ ! -f "$CLAUDE" ]; then
    log "WARNING: Claude CLI not at $CLAUDE"
    # Try PATH
    CLAUDE=$(which claude 2>/dev/null || echo "")
    if [ -z "$CLAUDE" ]; then
        log "ERROR: Claude CLI not found. Prompt ready at: $PROMPT"
        log "Run manually: cat $PROMPT | claude --print --dangerously-skip-permissions"
        kill $CAFE_PID 2>/dev/null || true
        exit 1
    fi
fi

# 30 minute timeout
timeout 1800 bash -c "cd '$BASE' && cat '$PROMPT' | '$CLAUDE' --print --dangerously-skip-permissions" > "$CLAUDE_LOG" 2>&1
CLAUDE_EXIT=$?

case $CLAUDE_EXIT in
    0)   log "Claude session completed successfully" ;;
    124) log "Claude session timed out (30 min limit)" ;;
    *)   log "Claude session exited with code $CLAUDE_EXIT" ;;
esac

# ── Step 4: Post-process ──
log "Step 4: Routing outputs..."
$PYTHON "$BASE/AUTOMATIONS/autonomous_orchestrator.py" --post "$CLAUDE_LOG" >> "$LOG" 2>&1

# Crash recovery: clear session-in-flight marker
sed -i '' '/SESSION_IN_FLIGHT/d' "$ACTIVE_TASKS" 2>/dev/null || true

# ── Step 5: Run rebalancer (evening only) ──
if [ "$SESSION_TYPE" = "evening" ]; then
    log "Step 5: Running rebalancer..."
    $PYTHON "$BASE/AUTOMATIONS/auto_rebalancer.py" --check >> "$LOG" 2>&1 || true
fi

# ── Step 6: Generate checkpoint summary ──
PENDING_COUNT=$(ls "$BASE/OPS/checkpoints/pending/" 2>/dev/null | wc -l | tr -d ' ')
if [ "$PENDING_COUNT" -gt 0 ]; then
    log "Generating checkpoint summary ($PENDING_COUNT pending)..."
    $PYTHON "$BASE/AUTOMATIONS/checkpoint_manager.py" --summary >> "$LOG" 2>&1 || true
fi

# ── Cleanup ──
kill $CAFE_PID 2>/dev/null || true
rm -f "$LOCK_FILE"

# ── Summary ──
CLAUDE_LINES=$(wc -l < "$CLAUDE_LOG" 2>/dev/null || echo 0)
log "=== SESSION COMPLETE: $SESSION_TYPE ==="
log "Claude output: $CLAUDE_LINES lines"
log "Session log: $LOG"
log "Claude log: $CLAUDE_LOG"
