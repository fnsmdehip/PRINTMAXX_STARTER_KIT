#!/bin/bash
# PRINTMAXX Perpetual Ship Engine — 24/7 Autonomous Entrepreneurship
#
# Architecture:
#   Layer 1: Python cron scripts (ALWAYS running, no LLM needed)
#   Layer 2: Claude Code sessions (primary brain, Claude Max $200)
#   Layer 3: OpenCode/local LLM fallback (when Claude hits limits)
#   Safety:  Git backup before every run, cloned folder as failsafe
#
# Usage:
#   bash AUTOMATIONS/perpetual_ship_engine.sh start     # Start the engine
#   bash AUTOMATIONS/perpetual_ship_engine.sh status     # Check status
#   bash AUTOMATIONS/perpetual_ship_engine.sh stop       # Stop gracefully
#   bash AUTOMATIONS/perpetual_ship_engine.sh backup     # Manual backup
#   bash AUTOMATIONS/perpetual_ship_engine.sh handoff    # Force handoff to fallback

set -euo pipefail

BASE="$(cd "$(dirname "$0")/.." && pwd)"
LOGS="$BASE/AUTOMATIONS/logs"
BACKUP_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_BACKUP_LIVE"
PID_FILE="$LOGS/perpetual_engine.pid"
STATUS_FILE="$LOGS/engine_status.json"
HANDOFF_FILE="$LOGS/handoff_state.json"

mkdir -p "$LOGS" "$BACKUP_DIR"

# ============================================================
# LAYER 1: Non-Claude Scripts (run on cron, zero LLM dependency)
# These run 24/7 regardless of Claude availability
# ============================================================
run_layer1() {
    echo "[$(date)] Layer 1: Running non-Claude automation scripts..."

    # Reddit scraper (JSON API, no auth needed)
    python3 "$BASE/AUTOMATIONS/browser_scraper_daily.py" --reddit --limit 10 \
        > "$LOGS/layer1_reddit_$(date +%Y%m%d).log" 2>&1 &

    # Venture performance scoring
    python3 "$BASE/AUTOMATIONS/venture_performance_tracker.py" --recommend \
        > "$LOGS/layer1_ventures_$(date +%Y%m%d).log" 2>&1 &

    # Ecom distribution status check
    python3 "$BASE/AUTOMATIONS/ecom_distributor.py" --status \
        > "$LOGS/layer1_ecom_$(date +%Y%m%d).log" 2>&1 &

    # Daily agent runner priorities
    python3 "$BASE/AUTOMATIONS/daily_agent_runner.py" --status \
        > "$LOGS/layer1_status_$(date +%Y%m%d).log" 2>&1 &

    # RBI scanner (if exists)
    if [ -f "$BASE/AUTOMATIONS/daily_nocost_rbi_scanner.py" ]; then
        python3 "$BASE/AUTOMATIONS/daily_nocost_rbi_scanner.py" --scan \
            > "$LOGS/layer1_rbi_$(date +%Y%m%d).log" 2>&1 &
    fi

    wait
    echo "[$(date)] Layer 1 complete."
}

# ============================================================
# LAYER 2: Claude Code Session (primary brain)
# Auto-restarts, tracks token usage, hands off when near limit
# ============================================================
run_layer2() {
    echo "[$(date)] Layer 2: Starting Claude Code session..."

    # Create session prompt that focuses on SHIPPING
    SHIP_PROMPT="You are resuming PRINTMAXX. Read OPS/SHIP_NOW_HUMAN_STEPS.md and OPS/AGENT_DAILY_PLAYBOOK.md.
Run python3 AUTOMATIONS/daily_agent_runner.py --status.
Then SHIP: deploy apps, list products, post content, run scrapers.
Check AUTOMATIONS/logs/engine_status.json for what was done last session.
DO NOT build new systems. DEPLOY existing ones. SHIP SPEED."

    # Run Claude Code with auto-continue
    # --dangerously-skip-permissions for autonomous operation
    echo "$SHIP_PROMPT" | claude --dangerously-skip-permissions --print \
        > "$LOGS/layer2_claude_$(date +%Y%m%d_%H%M).log" 2>&1

    EXIT_CODE=$?

    if [ $EXIT_CODE -eq 0 ]; then
        echo "[$(date)] Layer 2: Claude session completed successfully."
    else
        echo "[$(date)] Layer 2: Claude session exited with code $EXIT_CODE"
        echo "[$(date)] Checking if token limit hit..."

        # If Claude hit limits, trigger Layer 3
        if grep -q "rate_limit\|token.*limit\|capacity\|429" "$LOGS/layer2_claude_$(date +%Y%m%d_%H%M).log" 2>/dev/null; then
            echo "[$(date)] Token limit detected. Triggering Layer 3 fallback..."
            save_handoff_state
            run_layer3
        fi
    fi
}

# ============================================================
# LAYER 3: Fallback (OpenCode / local LLM / pure Python)
# When Claude hits limits, keep the machine running
# ============================================================
run_layer3() {
    echo "[$(date)] Layer 3: Fallback mode activated..."

    # Option A: Try OpenCode (if installed)
    if command -v opencode &>/dev/null; then
        echo "[$(date)] Using OpenCode as fallback..."

        # Clone folder for safety
        create_safe_clone

        FALLBACK_PROMPT="Read AUTOMATIONS/logs/handoff_state.json for context.
Run python3 AUTOMATIONS/daily_agent_runner.py --status.
Focus on: running existing scripts, checking outputs, logging results.
DO NOT modify core files. Only create files in output/ and AUTOMATIONS/logs/."

        echo "$FALLBACK_PROMPT" | opencode \
            > "$LOGS/layer3_opencode_$(date +%Y%m%d_%H%M).log" 2>&1 || true
    fi

    # Option B: Pure Python fallback (always works, no LLM needed)
    echo "[$(date)] Running Python-only fallback tasks..."
    run_layer1  # Re-run all non-Claude scripts

    # Generate daily TODO from latest data
    if [ -f "$BASE/AUTOMATIONS/daily_todo_generator.py" ]; then
        python3 "$BASE/AUTOMATIONS/daily_todo_generator.py" \
            > "$LOGS/layer3_todo_$(date +%Y%m%d).log" 2>&1 || true
    fi

    echo "[$(date)] Layer 3 fallback complete."
}

# ============================================================
# SAFETY: Backup & Clone
# ============================================================
create_backup() {
    echo "[$(date)] Creating git backup..."
    cd "$BASE"
    git add -A 2>/dev/null || true
    git commit -m "Auto-backup $(date +%Y-%m-%d_%H:%M) by perpetual engine" 2>/dev/null || true
    echo "[$(date)] Git backup done."
}

create_safe_clone() {
    echo "[$(date)] Creating safe clone for fallback..."
    rsync -a --exclude='node_modules' --exclude='.git' --exclude='output/' \
        "$BASE/" "$BACKUP_DIR/" 2>/dev/null || true
    echo "[$(date)] Safe clone at $BACKUP_DIR"
}

save_handoff_state() {
    # Save current state for Layer 3 to pick up
    python3 -c "
import json
from datetime import datetime
state = {
    'timestamp': datetime.now().isoformat(),
    'reason': 'claude_token_limit',
    'last_action': 'check logs for details',
    'next_priorities': [
        'Run scrapers (layer1 scripts)',
        'Check venture scores',
        'Monitor ecom distribution status',
        'Generate daily TODO'
    ],
    'do_not': [
        'Modify CLAUDE.md',
        'Delete any files',
        'Create new accounts',
        'Make purchases'
    ]
}
with open('$HANDOFF_FILE', 'w') as f:
    json.dump(state, f, indent=2)
print('Handoff state saved.')
" 2>/dev/null || true
}

update_status() {
    python3 -c "
import json
from datetime import datetime
status = {
    'engine': '${1:-unknown}',
    'timestamp': datetime.now().isoformat(),
    'layer1_last': '$(ls -t $LOGS/layer1_*.log 2>/dev/null | head -1)',
    'layer2_last': '$(ls -t $LOGS/layer2_*.log 2>/dev/null | head -1)',
    'layer3_last': '$(ls -t $LOGS/layer3_*.log 2>/dev/null | head -1)',
    'pid': '$$'
}
with open('$STATUS_FILE', 'w') as f:
    json.dump(status, f, indent=2)
" 2>/dev/null || true
}

# ============================================================
# MAIN LOOP: Perpetual Ship Engine
# ============================================================
perpetual_loop() {
    echo "$$" > "$PID_FILE"
    echo "[$(date)] Perpetual Ship Engine STARTED (PID: $$)"

    ITERATION=0
    while true; do
        ITERATION=$((ITERATION + 1))
        echo ""
        echo "============================================================"
        echo "  ITERATION $ITERATION — $(date)"
        echo "============================================================"

        # Safety: backup before each iteration
        create_backup
        update_status "running_iteration_$ITERATION"

        # Layer 1: Always run Python scripts first (no LLM needed)
        run_layer1

        # Layer 2: Claude Code session
        run_layer2

        # Cool down between iterations (prevent runaway)
        COOLDOWN=300  # 5 minutes between iterations
        echo "[$(date)] Cooling down for ${COOLDOWN}s before next iteration..."
        sleep $COOLDOWN
    done
}

# ============================================================
# COMMANDS
# ============================================================
case "${1:-status}" in
    start)
        if [ -f "$PID_FILE" ] && kill -0 "$(cat $PID_FILE)" 2>/dev/null; then
            echo "Engine already running (PID: $(cat $PID_FILE))"
            exit 1
        fi
        echo "Starting Perpetual Ship Engine..."
        perpetual_loop &
        echo "Engine started in background. Check: tail -f $LOGS/layer*.log"
        ;;
    stop)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            kill "$PID" 2>/dev/null && echo "Engine stopped (PID: $PID)" || echo "Engine not running"
            rm -f "$PID_FILE"
        else
            echo "No PID file found. Engine may not be running."
        fi
        ;;
    status)
        echo ""
        echo "=== PERPETUAL SHIP ENGINE STATUS ==="
        if [ -f "$PID_FILE" ] && kill -0 "$(cat $PID_FILE)" 2>/dev/null; then
            echo "Status: RUNNING (PID: $(cat $PID_FILE))"
        else
            echo "Status: STOPPED"
        fi
        echo ""
        if [ -f "$STATUS_FILE" ]; then
            cat "$STATUS_FILE"
        fi
        echo ""
        echo "Recent logs:"
        ls -lt "$LOGS"/layer*.log 2>/dev/null | head -10
        echo ""
        echo "Backup: $BACKUP_DIR"
        echo "==================================="
        ;;
    backup)
        create_backup
        create_safe_clone
        ;;
    handoff)
        save_handoff_state
        run_layer3
        ;;
    layer1)
        run_layer1
        ;;
    layer2)
        run_layer2
        ;;
    layer3)
        save_handoff_state
        run_layer3
        ;;
    *)
        echo "Usage: perpetual_ship_engine.sh {start|stop|status|backup|handoff|layer1|layer2|layer3}"
        ;;
esac
