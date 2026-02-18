#!/bin/bash
# PRINTMAXX Auto-Resume Monitor
# Checks if Claude Code session was interrupted and triggers a finishing run
# Runs via cron every 30 minutes during overnight hours
#
# Logic:
# 1. Check if any agent output files were recently modified (indicates active session)
# 2. If session appears interrupted (no recent activity but incomplete tasks), trigger resume
# 3. Log all activity for morning review

BASE_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
LOG_DIR="$BASE_DIR/AUTOMATIONS/logs"
CLAUDE="/Users/macbookpro/.local/bin/claude"
PYTHON="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
RESUME_LOG="$LOG_DIR/auto_resume.log"
LOCK_FILE="/tmp/printmaxx_auto_resume.lock"

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$RESUME_LOG"
}

# Prevent concurrent runs
if [ -f "$LOCK_FILE" ]; then
    lock_age=$(( $(date +%s) - $(stat -f %m "$LOCK_FILE") ))
    if [ $lock_age -lt 1800 ]; then
        log "SKIP: Lock file exists (${lock_age}s old)"
        exit 0
    fi
    log "WARN: Stale lock file (${lock_age}s old), removing"
    rm -f "$LOCK_FILE"
fi

trap 'rm -f "$LOCK_FILE"' EXIT
touch "$LOCK_FILE"

log "=== Auto-Resume Check ==="

# Check 1: Is overnight runner still going?
if pgrep -f "overnight_master_runner" > /dev/null 2>&1; then
    log "Overnight runner still active, skipping"
    exit 0
fi

# Check 2: Is a Claude session still active?
if pgrep -f "claude" > /dev/null 2>&1; then
    log "Claude session still active, skipping"
    exit 0
fi

# Check 3: Are there incomplete overnight tasks?
TODAY=$(date +%Y-%m-%d)
STATUS_FILE="$LOG_DIR/overnight_status_${TODAY}.json"

if [ ! -f "$STATUS_FILE" ]; then
    log "No overnight status file for today, running overnight master"
    cd "$BASE_DIR" && bash AUTOMATIONS/overnight_master_runner.sh >> "$RESUME_LOG" 2>&1 &
    exit 0
fi

# Check 4: Did the overnight runner complete?
if ! grep -q "OVERNIGHT RUN COMPLETE" "$LOG_DIR/overnight_${TODAY}.log" 2>/dev/null; then
    log "Overnight run appears interrupted, restarting"
    cd "$BASE_DIR" && bash AUTOMATIONS/overnight_master_runner.sh >> "$RESUME_LOG" 2>&1 &
    exit 0
fi

# Check 5: Were there failures worth retrying?
FAIL_COUNT=$(grep -c '"FAILED"' "$STATUS_FILE" 2>/dev/null || echo 0)
if [ "$FAIL_COUNT" -gt 5 ]; then
    log "Many failures ($FAIL_COUNT), attempting retry of failed scripts"

    # Extract failed script names and retry them
    grep '"FAILED"' "$STATUS_FILE" | while IFS= read -r line; do
        script=$(echo "$line" | grep -o '"script":"[^"]*"' | cut -d'"' -f4)
        log "Retrying failed: $script"
    done

    # Re-run the overnight runner (it'll re-attempt everything)
    cd "$BASE_DIR" && bash AUTOMATIONS/overnight_master_runner.sh >> "$RESUME_LOG" 2>&1 &
    exit 0
fi

log "Everything looks good, no resume needed"
