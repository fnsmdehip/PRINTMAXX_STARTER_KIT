#!/bin/bash
# WAKE CATCHUP — runs missed daily crons when laptop wakes from sleep
# Installed as launchd agent that fires on system wake.
# Checks log timestamps to avoid re-running jobs that already succeeded today.

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/Library/Frameworks/Python.framework/Versions/3.12/bin:/Users/macbookpro/.local/bin"
export SHELL=/bin/bash

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
PYTHON="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
LOGDIR="$BASE/AUTOMATIONS/logs"
LOCKFILE="/tmp/printmaxx_wake_catchup.lock"
TODAY=$(date '+%Y-%m-%d')

# Prevent concurrent runs
if [ -f "$LOCKFILE" ]; then
    LOCK_AGE=$(( $(date +%s) - $(stat -f %m "$LOCKFILE") ))
    if [ "$LOCK_AGE" -lt 3600 ]; then
        echo "[$(date)] Catchup already running (lock age: ${LOCK_AGE}s). Skipping."
        exit 0
    fi
    rm -f "$LOCKFILE"
fi
touch "$LOCKFILE"
trap "rm -f $LOCKFILE" EXIT

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOGDIR/wake_catchup.log"; }
log "=== WAKE CATCHUP START ==="

# Check if a job ran today by looking for today's date in its log
ran_today() {
    local logfile="$1"
    if [ -f "$logfile" ]; then
        # Check if log was modified today
        local mod_date=$(date -r "$logfile" '+%Y-%m-%d' 2>/dev/null)
        [ "$mod_date" = "$TODAY" ] && return 0
    fi
    return 1
}

# Run a job if it hasn't run today
run_if_missed() {
    local name="$1"
    local logfile="$2"
    local cmd="$3"

    if ran_today "$logfile"; then
        log "SKIP $name (already ran today)"
    else
        log "CATCHUP $name"
        eval "cd $BASE && $cmd >> $logfile 2>&1" &
    fi
}

# === DAILY JOBS (5:00 AM batch) ===
run_if_missed "morning_dag" "$LOGDIR/morning_dag.log" "$PYTHON AUTOMATIONS/morning_intelligence_dag.py"
run_if_missed "health_check" "$LOGDIR/health_check_all.log" "$PYTHON AUTOMATIONS/health_check_all.py --check"
run_if_missed "method_discovery" "$LOGDIR/method_discovery.log" "$PYTHON AUTOMATIONS/method_discovery_crawler.py --crawl"

# === DAILY JOBS (5:10 AM batch) ===
run_if_missed "auto_approve" "$LOGDIR/auto_approve.log" "$PYTHON AUTOMATIONS/auto_approve.py"
run_if_missed "alpha_index" "$LOGDIR/alpha_index.log" "$PYTHON AUTOMATIONS/sqlite_alpha_index.py --rebuild"

# === DAILY JOBS (5:15 AM batch) ===
run_if_missed "capital_genesis" "$LOGDIR/capital_genesis_ranker.log" "$PYTHON AUTOMATIONS/capital_genesis_ranker.py --rank --report"

# === DAILY JOBS (5:20 AM batch) ===
run_if_missed "rbi_loop" "$LOGDIR/rbi_loop.log" "$PYTHON AUTOMATIONS/rbi_loop.py --full"
run_if_missed "decision_engine" "$LOGDIR/decision_engine.log" "$PYTHON AUTOMATIONS/decision_engine.py --cycle"
run_if_missed "actionable_agg" "$LOGDIR/actionable_aggregator.log" "$PYTHON AUTOMATIONS/actionable_aggregator.py"

# === DAILY JOBS (5:30 AM batch) ===
run_if_missed "daily_digest" "$LOGDIR/daily_digest.log" "$PYTHON AUTOMATIONS/daily_digest.py"
run_if_missed "session_briefing" "$LOGDIR/session_briefing.log" "$PYTHON AUTOMATIONS/session_briefing.py"

# === DAILY JOBS (6:30 AM) ===
run_if_missed "app_factory" "$BASE/AUTOMATIONS/app_factory/logs/cron_orchestrator.log" "$PYTHON AUTOMATIONS/app_factory/auto_orchestrator.py --full"

# === RESEARCH SCANNERS (all included, no skips) ===
run_if_missed "sec_edgar" "$LOGDIR/sec_edgar_scanner.log" "$PYTHON AUTOMATIONS/sec_edgar_scanner.py --scan"
run_if_missed "crunchbase" "$LOGDIR/crunchbase_scanner.log" "$PYTHON AUTOMATIONS/crunchbase_scanner.py --scan"
run_if_missed "ecom_arb" "$LOGDIR/ecom_arb_engine.log" "$PYTHON AUTOMATIONS/ecom_arb_engine.py --scan"
run_if_missed "opportunity_radar" "$LOGDIR/opportunity_radar.log" "$PYTHON AUTOMATIONS/opportunity_radar.py --scan"
run_if_missed "sam_gov" "$LOGDIR/sam_gov_monitor.log" "$PYTHON AUTOMATIONS/sam_gov_monitor.py"
run_if_missed "alpha_backlog" "$LOGDIR/alpha_backlog_scanner.log" "$PYTHON AUTOMATIONS/alpha_backlog_scanner.py --scan"
run_if_missed "perpetual_guardian" "$LOGDIR/perpetual_guardian.log" "$PYTHON AUTOMATIONS/perpetual_guardian.py --full"
run_if_missed "log_rotator" "$LOGDIR/log_rotator.log" "$PYTHON AUTOMATIONS/log_rotator.py --rotate"

# === WEEKLY JOBS — only catch up if it's been >7 days ===
WEEKLY_LOG="$LOGDIR/weekly_deploy.log"
if [ -f "$WEEKLY_LOG" ]; then
    LAST_WEEKLY=$(stat -f %m "$WEEKLY_LOG" 2>/dev/null || echo 0)
    NOW=$(date +%s)
    DAYS_AGO=$(( (NOW - LAST_WEEKLY) / 86400 ))
    if [ "$DAYS_AGO" -ge 7 ]; then
        log "CATCHUP weekly_deploy (${DAYS_AGO} days since last run)"
        bash "$BASE/AUTOMATIONS/weekly_site_deploy.sh" &
    else
        log "SKIP weekly_deploy (ran ${DAYS_AGO} days ago)"
    fi
else
    log "CATCHUP weekly_deploy (never ran)"
    bash "$BASE/AUTOMATIONS/weekly_site_deploy.sh" &
fi

# Wait for background jobs (max 5 min)
WAITED=0
while [ $(jobs -r | wc -l) -gt 0 ] && [ $WAITED -lt 300 ]; do
    sleep 10
    WAITED=$((WAITED + 10))
done

log "=== WAKE CATCHUP COMPLETE (${WAITED}s) ==="
