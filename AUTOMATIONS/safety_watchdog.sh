#!/bin/bash
# ============================================================
# PRINTMAXX SAFETY WATCHDOG
# ============================================================
# Wraps any automation command with pre/post safety checks.
# Optionally invokes Claude Code for LLM-in-the-loop validation.
#
# Usage:
#   ./AUTOMATIONS/safety_watchdog.sh <command> [args...]
#   ./AUTOMATIONS/safety_watchdog.sh printmaxx_cron.sh morning
#   ./AUTOMATIONS/safety_watchdog.sh --llm-check printmaxx_cron.sh weekly
#
# Safety layers:
#   1. Pre-flight: disk space, CSV snapshot, LEDGER integrity
#   2. Execution: timeout, output capture, error detection
#   3. Post-flight: CSV row delta, LEDGER file count, log review
#   4. (Optional) LLM check: Claude Code reviews the diff
#   5. Auto-halt if anything looks catastrophic
# ============================================================

set -uo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$PROJECT_DIR/logs"
SNAPSHOT_DIR="$PROJECT_DIR/LEDGER/.snapshots"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
WATCHDOG_LOG="$LOG_DIR/watchdog_${TIMESTAMP}.log"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

mkdir -p "$LOG_DIR" "$SNAPSHOT_DIR"

log() { echo -e "${GREEN}[WATCHDOG $(date +%H:%M:%S)]${NC} $1" | tee -a "$WATCHDOG_LOG"; }
warn() { echo -e "${YELLOW}[WATCHDOG $(date +%H:%M:%S)] WARNING:${NC} $1" | tee -a "$WATCHDOG_LOG"; }
halt() { echo -e "${RED}[WATCHDOG $(date +%H:%M:%S)] HALTED:${NC} $1" | tee -a "$WATCHDOG_LOG"; exit 1; }

# ============================================================
# Parse args
# ============================================================
LLM_CHECK=false
if [ "${1:-}" = "--llm-check" ]; then
    LLM_CHECK=true
    shift
fi

if [ $# -eq 0 ]; then
    echo "Usage: $0 [--llm-check] <command> [args...]"
    exit 1
fi

COMMAND="$@"

# ============================================================
# SAFETY THRESHOLDS
# ============================================================
MAX_CSV_ROW_CHANGE=200        # Halt if any CSV gains/loses >200 rows in one run
MIN_DISK_FREE_GB=5            # Halt if <5GB free disk space
MAX_EXECUTION_SECONDS=3600    # Timeout after 1 hour (override with WATCHDOG_TIMEOUT env var)
TIMEOUT=${WATCHDOG_TIMEOUT:-$MAX_EXECUTION_SECONDS}
MAX_LEDGER_FILES_DELETED=5    # Halt if >5 LEDGER files vanish

# ============================================================
# PRE-FLIGHT CHECKS (fast - no recursive scans)
# ============================================================
log "Starting safety watchdog for: $COMMAND"
log "Thresholds: max_csv_row_change=$MAX_CSV_ROW_CHANGE timeout=${TIMEOUT}s min_disk=${MIN_DISK_FREE_GB}GB"

# Check disk space (fast: only checks mount point)
DISK_FREE_KB=$(df -k "$PROJECT_DIR" | tail -1 | awk '{print $4}')
DISK_FREE_GB=$((DISK_FREE_KB / 1048576))
if [ "$DISK_FREE_GB" -lt "$MIN_DISK_FREE_GB" ]; then
    halt "Only ${DISK_FREE_GB}GB free disk space (minimum: ${MIN_DISK_FREE_GB}GB). Aborting to prevent disk full."
fi
log "Disk space: ${DISK_FREE_GB}GB free (OK)"

# Snapshot LEDGER CSVs (fast: only top-level LEDGER, no recursion)
PRE_CSV_DIR="$SNAPSHOT_DIR/pre_${TIMESTAMP}"
mkdir -p "$PRE_CSV_DIR"
cp "$PROJECT_DIR"/LEDGER/*.csv "$PRE_CSV_DIR/" 2>/dev/null || true

# Count LEDGER files for integrity check
PRE_LEDGER_COUNT=$(ls -1 "$PROJECT_DIR/LEDGER/" 2>/dev/null | wc -l | tr -d ' ')

# Record CSV row counts
declare -A PRE_CSV_ROWS
for csv_file in "$PRE_CSV_DIR"/*.csv; do
    if [ -f "$csv_file" ]; then
        base=$(basename "$csv_file")
        PRE_CSV_ROWS["$base"]=$(wc -l < "$csv_file" | tr -d ' ')
    fi
done

# Also snapshot MEGA_SHEET CSVs
PRE_MEGA_DIR="$SNAPSHOT_DIR/pre_mega_${TIMESTAMP}"
mkdir -p "$PRE_MEGA_DIR"
cp "$PROJECT_DIR"/LEDGER/MEGA_SHEET/*.csv "$PRE_MEGA_DIR/" 2>/dev/null || true

declare -A PRE_MEGA_ROWS
for csv_file in "$PRE_MEGA_DIR"/*.csv; do
    if [ -f "$csv_file" ]; then
        base=$(basename "$csv_file")
        PRE_MEGA_ROWS["$base"]=$(wc -l < "$csv_file" | tr -d ' ')
    fi
done

log "Pre-flight: ${PRE_LEDGER_COUNT} LEDGER items, CSVs snapshotted"

# Git safety: ensure we can rollback
if [ -d "$PROJECT_DIR/.git" ]; then
    cd "$PROJECT_DIR"
    UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    if [ "$UNCOMMITTED" -gt 50 ]; then
        warn "Large number of uncommitted changes ($UNCOMMITTED files). Consider committing first."
    fi
    log "Git status: $UNCOMMITTED uncommitted changes"
fi

# ============================================================
# EXECUTE WITH SAFETY WRAPPER
# ============================================================
log "Executing: $COMMAND"
EXEC_START=$(date +%s)

# Run with timeout
cd "$PROJECT_DIR"
timeout "$TIMEOUT" bash -c "$COMMAND" >> "$WATCHDOG_LOG" 2>&1
EXIT_CODE=$?

EXEC_END=$(date +%s)
EXEC_DURATION=$((EXEC_END - EXEC_START))

if [ "$EXIT_CODE" -eq 124 ]; then
    halt "Command timed out after ${TIMEOUT} seconds! Possible runaway process."
elif [ "$EXIT_CODE" -ne 0 ]; then
    warn "Command exited with code $EXIT_CODE (non-zero). Check log."
fi

log "Execution completed in ${EXEC_DURATION}s with exit code $EXIT_CODE"

# ============================================================
# POST-FLIGHT SAFETY CHECKS (fast, targeted)
# ============================================================
log "Running post-flight safety checks..."

# Check LEDGER file count (fast)
POST_LEDGER_COUNT=$(ls -1 "$PROJECT_DIR/LEDGER/" 2>/dev/null | wc -l | tr -d ' ')
LEDGER_DELTA=$((POST_LEDGER_COUNT - PRE_LEDGER_COUNT))

if [ "$LEDGER_DELTA" -lt "-${MAX_LEDGER_FILES_DELETED}" ]; then
    halt "CATASTROPHIC: ${LEDGER_DELTA#-} LEDGER files DELETED (threshold: $MAX_LEDGER_FILES_DELETED). Snapshots preserved at $PRE_CSV_DIR"
fi
log "LEDGER files: $PRE_LEDGER_COUNT -> $POST_LEDGER_COUNT (delta: ${LEDGER_DELTA})"

# Check CSV row count deltas (LEDGER/)
ALERT_CSVS=""
for csv_file in "$PROJECT_DIR"/LEDGER/*.csv; do
    if [ -f "$csv_file" ]; then
        base=$(basename "$csv_file")
        POST_ROWS=$(wc -l < "$csv_file" | tr -d ' ')
        PRE_ROWS=${PRE_CSV_ROWS["$base"]:-0}
        ROW_DELTA=$((POST_ROWS - PRE_ROWS))
        ABS_ROW_DELTA=${ROW_DELTA#-}
        if [ "$ABS_ROW_DELTA" -gt "$MAX_CSV_ROW_CHANGE" ]; then
            ALERT_CSVS="$ALERT_CSVS $base(${ROW_DELTA})"
            warn "CSV $base changed by $ROW_DELTA rows (threshold: $MAX_CSV_ROW_CHANGE)"
        fi
    fi
done

# Check MEGA_SHEET CSV deltas too
for csv_file in "$PROJECT_DIR"/LEDGER/MEGA_SHEET/*.csv; do
    if [ -f "$csv_file" ]; then
        base=$(basename "$csv_file")
        POST_ROWS=$(wc -l < "$csv_file" | tr -d ' ')
        PRE_ROWS=${PRE_MEGA_ROWS["$base"]:-0}
        ROW_DELTA=$((POST_ROWS - PRE_ROWS))
        ABS_ROW_DELTA=${ROW_DELTA#-}
        if [ "$ABS_ROW_DELTA" -gt "$MAX_CSV_ROW_CHANGE" ]; then
            ALERT_CSVS="$ALERT_CSVS MEGA/$base(${ROW_DELTA})"
            warn "MEGA_SHEET CSV $base changed by $ROW_DELTA rows (threshold: $MAX_CSV_ROW_CHANGE)"
        fi
    fi
done

if [ -z "$ALERT_CSVS" ]; then
    log "CSV row counts: all within threshold"
fi

# Check for error patterns in the execution log
ERROR_COUNT=$(grep -ci "error\|traceback\|exception\|fatal\|panic" "$WATCHDOG_LOG" 2>/dev/null | tr -d ' \n' || true)
ERROR_COUNT=${ERROR_COUNT:-0}
if [ "$ERROR_COUNT" -gt 5 ]; then
    warn "Detected $ERROR_COUNT error-like patterns in log output. Review $WATCHDOG_LOG"
fi

# ============================================================
# CLAUDE CODE OPUS AUTO-AUDIT (runs automatically)
# ============================================================
# Always generates audit diff. If Claude CLI is installed AND
# --llm-check flag is set OR errors were detected, runs Opus audit.
AUTO_AUDIT=false
if [ "$LLM_CHECK" = true ] || [ "$EXIT_CODE" -ne 0 ] || [ "${ERROR_COUNT:-0}" -gt 0 ] || [ -n "${ALERT_CSVS:-}" ]; then
    AUTO_AUDIT=true
fi

# Generate diff summary (always, for logging)
DIFF_SUMMARY="$LOG_DIR/watchdog_diff_${TIMESTAMP}.txt"
echo "=== PRINTMAXX WATCHDOG AUDIT ===" > "$DIFF_SUMMARY"
echo "Command: $COMMAND" >> "$DIFF_SUMMARY"
echo "Timestamp: $(date -Iseconds)" >> "$DIFF_SUMMARY"
echo "Duration: ${EXEC_DURATION}s" >> "$DIFF_SUMMARY"
echo "Exit code: $EXIT_CODE" >> "$DIFF_SUMMARY"
echo "LEDGER delta: $LEDGER_DELTA files" >> "$DIFF_SUMMARY"
echo "CSV alerts: ${ALERT_CSVS:-none}" >> "$DIFF_SUMMARY"
echo "Error patterns: ${ERROR_COUNT:-0}" >> "$DIFF_SUMMARY"
echo "" >> "$DIFF_SUMMARY"

# Append recent results from AUTOMATION_RESULTS.csv if available
RESULTS_CSV="$PROJECT_DIR/LEDGER/AUTOMATION_RESULTS.csv"
if [ -f "$RESULTS_CSV" ]; then
    echo "--- LATEST AUTOMATION RESULTS ---" >> "$DIFF_SUMMARY"
    tail -3 "$RESULTS_CSV" >> "$DIFF_SUMMARY" 2>/dev/null
    echo "" >> "$DIFF_SUMMARY"
fi

# Append last 20 lines of watchdog log for context
echo "--- EXECUTION LOG (last 20 lines) ---" >> "$DIFF_SUMMARY"
tail -20 "$WATCHDOG_LOG" >> "$DIFF_SUMMARY" 2>/dev/null
echo "" >> "$DIFF_SUMMARY"

if [ -d "$PROJECT_DIR/.git" ]; then
    cd "$PROJECT_DIR"
    echo "--- GIT DIFF STAT ---" >> "$DIFF_SUMMARY"
    git diff --stat >> "$DIFF_SUMMARY" 2>/dev/null
    echo "" >> "$DIFF_SUMMARY"
    echo "--- CHANGED FILES ---" >> "$DIFF_SUMMARY"
    git diff --name-only >> "$DIFF_SUMMARY" 2>/dev/null
fi

log "Audit diff saved: $DIFF_SUMMARY"

# Run Claude Code Opus review if triggered
if [ "$AUTO_AUDIT" = true ]; then
    log "Launching Claude Code Opus audit (errors=$ERROR_COUNT alerts=${ALERT_CSVS:-none})..."

    if command -v claude &>/dev/null; then
        AUDIT_RESULT="$LOG_DIR/watchdog_audit_${TIMESTAMP}.txt"

        # Use claude-opus-4-6 (latest Opus) with --model flag
        timeout 120 claude --model claude-opus-4-6 --print \
            "You are auditing a PRINTMAXX automation run. Review this for safety issues, data integrity, and whether the automation achieved its intended purpose. Here is the run data:

$(cat "$DIFF_SUMMARY")

Respond with exactly one of: SAFE, WARNING, or HALT
Then a brief explanation (2-3 sentences max).
If HALT: explain what went wrong and whether rollback is needed.
If WARNING: explain what to watch.
If SAFE: confirm the run looks clean." \
            > "$AUDIT_RESULT" 2>&1 || warn "Claude Opus audit timed out or failed"

        if [ -f "$AUDIT_RESULT" ] && [ -s "$AUDIT_RESULT" ]; then
            VERDICT=$(head -1 "$AUDIT_RESULT" | tr -d '[:space:]' | cut -c1-7)
            log "Claude Opus verdict: $(head -1 "$AUDIT_RESULT")"
            cat "$AUDIT_RESULT" >> "$WATCHDOG_LOG"

            # If Claude says HALT, write to a halt file so Terminal can display it
            if echo "$VERDICT" | grep -qi "HALT"; then
                echo "$(date -Iseconds) | $COMMAND | HALTED by Claude Opus: $(head -2 "$AUDIT_RESULT")" \
                    >> "$LOG_DIR/watchdog_halts.log"
                warn "CLAUDE OPUS RECOMMENDS HALT. Check $AUDIT_RESULT"
            fi

            # Update the results CSV with the verdict
            if [ -f "$RESULTS_CSV" ]; then
                python3 -c "
import csv
rows = []
with open('$RESULTS_CSV') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    rows = list(reader)
if rows:
    rows[-1]['watchdog_verdict'] = '$(head -1 "$AUDIT_RESULT" | tr -d "\"," | head -c 50)'
with open('$RESULTS_CSV', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
" 2>/dev/null || true
            fi
        fi
        log "Opus audit complete. Full review: $AUDIT_RESULT"
    else
        warn "Claude CLI not found. Install: npm install -g @anthropic-ai/claude-code"
        warn "Opus auto-audit skipped. To enable: install Claude Code CLI on your Mac."
    fi
else
    log "No errors detected, skipping Opus audit (use --llm-check to force)"
fi

# ============================================================
# FINAL SUMMARY
# ============================================================
echo ""
log "============================================"
log "  WATCHDOG SUMMARY"
log "============================================"
log "  Command:    $COMMAND"
log "  Duration:   ${EXEC_DURATION}s"
log "  Exit code:  $EXIT_CODE"
log "  LEDGER:     $PRE_LEDGER_COUNT -> $POST_LEDGER_COUNT (${LEDGER_DELTA})"
log "  CSV alerts: ${ALERT_CSVS:-none}"
log "  Errors:     $ERROR_COUNT patterns found"
log "  Log:        $WATCHDOG_LOG"
log "============================================"
