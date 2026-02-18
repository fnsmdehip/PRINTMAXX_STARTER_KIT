#!/bin/bash
# PRINTMAXX Overnight Master Runner
# Runs all research, scraping, and analysis tools in sequence
# Designed to be called by cron or manually before sleep
# Logs everything to AUTOMATIONS/logs/overnight_YYYY-MM-DD.log

set -euo pipefail

BASE_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
LOG_DIR="$BASE_DIR/AUTOMATIONS/logs"
PYTHON="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
CLAUDE="/Users/macbookpro/.local/bin/claude"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/overnight_${DATE}.log"
STATUS_FILE="$LOG_DIR/overnight_status_${DATE}.json"

mkdir -p "$LOG_DIR"

# SAFETY: Load guardrails wrapper
source "$BASE_DIR/AUTOMATIONS/guardrails_wrapper.sh"

# SAFETY: Create incremental backup before overnight run
log_msg="Pre-overnight backup"
if [ -f "$BASE_DIR/AUTOMATIONS/backup_system.py" ]; then
    $PYTHON "$BASE_DIR/AUTOMATIONS/backup_system.py" --auto >> "$LOG_DIR/backup_overnight.log" 2>&1 || true
fi

log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

update_status() {
    local script=$1
    local status=$2
    local details=$3
    # Append to status JSON-lines file
    echo "{\"script\":\"$script\",\"status\":\"$status\",\"details\":\"$details\",\"time\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" >> "$STATUS_FILE"
}

run_script() {
    local name=$1
    local cmd=$2
    local max_time=${3:-600}  # default 10 min (increased from 5 min to reduce timeouts)

    log "=== STARTING: $name ==="

    # macOS-compatible timeout using background process + wait
    bash -c "cd '$BASE_DIR' && $cmd" >> "$LOG_FILE" 2>&1 &
    local pid=$!

    local elapsed=0
    while kill -0 $pid 2>/dev/null; do
        sleep 5
        elapsed=$((elapsed + 5))
        if [ $elapsed -ge $max_time ]; then
            kill $pid 2>/dev/null
            wait $pid 2>/dev/null
            log "=== TIMEOUT: $name (>${max_time}s) ==="
            update_status "$name" "TIMEOUT" "exceeded ${max_time}s"
            return 1
        fi
    done

    wait $pid
    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        log "=== COMPLETED: $name ==="
        update_status "$name" "SUCCESS" "completed"
        return 0
    else
        log "=== FAILED: $name (exit $exit_code) ==="
        update_status "$name" "FAILED" "exit code $exit_code"
        return 1
    fi
}

# ============================================================
log "============================================"
log "PRINTMAXX OVERNIGHT RUNNER - $DATE"
log "============================================"
echo "[]" > "$STATUS_FILE"

# PHASE 1: Daily Research Scrapers (public APIs, no auth needed)
log ""
log ">>> PHASE 1: DAILY RESEARCH SCRAPERS"

run_script "daily_nocost_rbi_scanner" \
    "$PYTHON AUTOMATIONS/daily_nocost_rbi_scanner.py --scan --next-actions" 120 || true

run_script "platform_meta_monitor" \
    "$PYTHON AUTOMATIONS/platform_meta_monitor.py" 120 || true

run_script "niche_meta_detector" \
    "$PYTHON AUTOMATIONS/niche_meta_detector.py" 120 || true

run_script "viral_content_scanner" \
    "$PYTHON AUTOMATIONS/viral_content_scanner.py --scan --limit 20" 120 || true

# PHASE 2: Lead Generation Scrapers
log ""
log ">>> PHASE 2: LEAD GEN SCRAPERS"

run_script "gov_tenders_refresh" \
    "$PYTHON AUTOMATIONS/gov_tenders_scraper.py --all-sources --days 7 --top 30" 600 || true

run_script "usaspending_refresh" \
    "$PYTHON AUTOMATIONS/usaspending_scraper.py" 600 || true

run_script "sam_gov_monitor" \
    "$PYTHON AUTOMATIONS/sam_gov_monitor.py" 300 || true

# REPLACED: City-by-city scraping replaced with bulk Overture Maps download
# Old approach: 3 cities/night x 4 categories = 12 scrapes, 2+ hours, ~120 leads
# New approach: download_bulk_leads.py gets 100K+ leads from Overture Maps in one shot
# The bulk download only needs to run weekly (data updates monthly)
# Weekly refresh runs Sunday via cron; daily overnight just does incremental scoring
run_script "bulk_lead_refresh_weekly" \
    "$PYTHON AUTOMATIONS/download_bulk_leads.py --status" 30 || true

# PHASE 3: Ecom & Product Scanners
log ""
log ">>> PHASE 3: ECOM & PRODUCT SCANNERS"

run_script "ecom_arb_scanner" \
    "$PYTHON AUTOMATIONS/ecom_arb_scanner.py" 180 || true

run_script "trending_products" \
    "$PYTHON AUTOMATIONS/trending_products_scanner.py" 180 || true

run_script "viral_product_scanner" \
    "$PYTHON AUTOMATIONS/viral_product_scanner.py --report" 60 || true

# PHASE 4: Alpha Analysis
log ""
log ">>> PHASE 4: ALPHA ANALYSIS"

run_script "alpha_screening" \
    "$PYTHON AUTOMATIONS/alpha_screening.py --pending" 120 || true

run_script "alpha_validator" \
    "$PYTHON AUTOMATIONS/alpha_validator.py" 120 || true

# PHASE 5: New Research Ops (built this session)
log ""
log ">>> PHASE 5: NEW RESEARCH OPS"

[ -f "$BASE_DIR/AUTOMATIONS/platform_algo_detection.py" ] && \
    run_script "platform_algo_detection" \
        "$PYTHON AUTOMATIONS/platform_algo_detection.py" 180 || true

[ -f "$BASE_DIR/AUTOMATIONS/hashtag_audio_tracking.py" ] && \
    run_script "hashtag_audio_tracking" \
        "$PYTHON AUTOMATIONS/hashtag_audio_tracking.py" 180 || true

[ -f "$BASE_DIR/AUTOMATIONS/platform_rpm_tracking.py" ] && \
    run_script "platform_rpm_tracking" \
        "$PYTHON AUTOMATIONS/platform_rpm_tracking.py" 180 || true

[ -f "$BASE_DIR/AUTOMATIONS/creator_program_monitoring.py" ] && \
    run_script "creator_program_monitoring" \
        "$PYTHON AUTOMATIONS/creator_program_monitoring.py" 180 || true

[ -f "$BASE_DIR/AUTOMATIONS/aso_keyword_research.py" ] && \
    run_script "aso_keyword_research" \
        "$PYTHON AUTOMATIONS/aso_keyword_research.py" 180 || true

[ -f "$BASE_DIR/AUTOMATIONS/run_all_research_ops.py" ] && \
    run_script "run_all_research_ops" \
        "$PYTHON AUTOMATIONS/run_all_research_ops.py" 600 || true

# PHASE 6: New lead source scrapers (built this session)
log ""
log ">>> PHASE 6: NEW LEAD SOURCES"

[ -f "$BASE_DIR/AUTOMATIONS/linkedin_events_scraper.py" ] && \
    run_script "linkedin_events" \
        "$PYTHON AUTOMATIONS/linkedin_events_scraper.py" 600 || true

[ -f "$BASE_DIR/AUTOMATIONS/g2_reviewer_scraper.py" ] && \
    run_script "g2_reviewers" \
        "$PYTHON AUTOMATIONS/g2_reviewer_scraper.py" 600 || true

[ -f "$BASE_DIR/AUTOMATIONS/indeed_hiring_monitor.py" ] && \
    run_script "indeed_hiring" \
        "$PYTHON AUTOMATIONS/indeed_hiring_monitor.py" 600 || true

[ -f "$BASE_DIR/AUTOMATIONS/nordic_ecom_arb.py" ] && \
    run_script "nordic_ecom" \
        "$PYTHON AUTOMATIONS/nordic_ecom_arb.py" 600 || true

[ -f "$BASE_DIR/AUTOMATIONS/app_clone_finder.py" ] && \
    run_script "app_clone_finder" \
        "$PYTHON AUTOMATIONS/app_clone_finder.py" 600 || true

# PHASE 7: Brain Integration (signal fusion + orchestration)
log ""
log ">>> PHASE 7: BRAIN INTEGRATION"

[ -f "$BASE_DIR/AUTOMATIONS/signal_aggregator.py" ] && \
    run_script "signal_aggregation" \
        "$PYTHON AUTOMATIONS/signal_aggregator.py --scan" 300 || true

[ -f "$BASE_DIR/AUTOMATIONS/ops_orchestrator.py" ] && \
    run_script "ops_orchestrator" \
        "$PYTHON AUTOMATIONS/ops_orchestrator.py --run" 600 || true

[ -f "$BASE_DIR/AUTOMATIONS/performance_optimizer.py" ] && \
    run_script "performance_health" \
        "$PYTHON AUTOMATIONS/performance_optimizer.py --health" 60 || true

[ -f "$BASE_DIR/AUTOMATIONS/printmaxx_brain.py" ] && \
    run_script "brain_heal" \
        "$PYTHON AUTOMATIONS/printmaxx_brain.py --heal" 120 || true

# PHASE 8: Summary
log ""
log "============================================"
log "OVERNIGHT RUN COMPLETE - $DATE"
log "============================================"

# Count successes and failures
SUCCESS_COUNT=$(grep -c '"SUCCESS"' "$STATUS_FILE" 2>/dev/null || echo 0)
FAIL_COUNT=$(grep -c '"FAILED"' "$STATUS_FILE" 2>/dev/null || echo 0)
TIMEOUT_COUNT=$(grep -c '"TIMEOUT"' "$STATUS_FILE" 2>/dev/null || echo 0)

log "Results: $SUCCESS_COUNT succeeded, $FAIL_COUNT failed, $TIMEOUT_COUNT timed out"
log "Full log: $LOG_FILE"
log "Status: $STATUS_FILE"

# Count new lead data
LEAD_FILES=$(find "$BASE_DIR/AUTOMATIONS/leads" -name "*.csv" -newer "$STATUS_FILE" 2>/dev/null | wc -l | tr -d ' ')
log "New/updated lead files: $LEAD_FILES"

echo ""
echo "OVERNIGHT RUN COMPLETE: $SUCCESS_COUNT/$((SUCCESS_COUNT + FAIL_COUNT + TIMEOUT_COUNT)) scripts succeeded"
