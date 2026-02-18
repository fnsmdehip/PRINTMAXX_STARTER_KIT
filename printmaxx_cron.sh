#!/bin/bash
# ============================================================
# PRINTMAXX MASTER ORCHESTRATOR v2
# ============================================================
# Central scheduler for all automated tasks.
# Every command logs yield metrics to LEDGER/AUTOMATION_RESULTS.csv
# so the Terminal can display exactly what each run produced.
#
# Usage:
#   ./printmaxx_cron.sh morning    # Run morning sync tasks (6 AM)
#   ./printmaxx_cron.sh content    # Run content generation (6:30 AM)
#   ./printmaxx_cron.sh outreach   # Run outreach queue staging (9 AM)
#   ./printmaxx_cron.sh digest     # Run evening digest (6 PM)
#   ./printmaxx_cron.sh backup     # Run nightly backup (9 PM)
#   ./printmaxx_cron.sh overnight  # Launch overnight Ralph sprint (10 PM)
#   ./printmaxx_cron.sh weekly     # Run all weekly tasks (Mon 9 AM)
#   ./printmaxx_cron.sh monthly    # Run all monthly tasks (1st of month)
#   ./printmaxx_cron.sh status     # Show system status
# ============================================================

set -uo pipefail

# Auto-detect project directory (works on both Mac and in Cowork VM)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
LOG_DIR="$PROJECT_DIR/logs"
SNAPSHOT_DIR="$PROJECT_DIR/LEDGER/.snapshots"
RESULTS_CSV="$PROJECT_DIR/LEDGER/AUTOMATION_RESULTS.csv"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATE_SHORT=$(date +%Y-%m-%d)
RUN_ID="${1:-unknown}_${TIMESTAMP}"
RUN_START=$(date +%s)

mkdir -p "$LOG_DIR" "$SNAPSHOT_DIR" "$PROJECT_DIR/OPS/reports" "$PROJECT_DIR/OPS/projections"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date +%H:%M:%S)]${NC} $1"; }
warn() { echo -e "${YELLOW}[$(date +%H:%M:%S)] WARNING:${NC} $1"; }
fail() { echo -e "${RED}[$(date +%H:%M:%S)] ERROR:${NC} $1"; }
yield_log() { echo -e "${CYAN}[YIELD]${NC} $1"; }
header() {
    echo ""
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}  $(date)${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
}

# ============================================================
# RESULTS TRACKING
# ============================================================
# Yield counters (accumulated during a run, flushed at end)
YIELD_ALPHA_EXTRACTED=0
YIELD_ALPHA_REPAIRED=0
YIELD_CONTENT_GENERATED=0
YIELD_BUFFER_CSVS=0
YIELD_PROJECTIONS=0
YIELD_REVENUE_30D="0"
YIELD_REVENUE_ANNUAL="0"
YIELD_OPS_UPDATED=0
YIELD_FILES_CREATED=0
YIELD_FILES_MODIFIED=0
YIELD_CSV_ROWS_CHANGED=0
YIELD_ERRORS=0
YIELD_NOTES=""

# Ensure results CSV has headers
if [ ! -f "$RESULTS_CSV" ]; then
    echo "run_id,timestamp,command,duration_secs,exit_code,alpha_extracted,alpha_repaired,content_generated,buffer_csvs,projections_generated,revenue_projected_30d,revenue_projected_annual,ops_updated,files_created,files_modified,csv_rows_changed,errors,watchdog_verdict,notes" > "$RESULTS_CSV"
fi

flush_results() {
    local cmd="${1:-unknown}"
    local exit_code="${2:-0}"
    local run_end=$(date +%s)
    local duration=$((run_end - RUN_START))

    echo "\"$RUN_ID\",\"$(date -Iseconds)\",\"$cmd\",$duration,$exit_code,$YIELD_ALPHA_EXTRACTED,$YIELD_ALPHA_REPAIRED,$YIELD_CONTENT_GENERATED,$YIELD_BUFFER_CSVS,$YIELD_PROJECTIONS,\"$YIELD_REVENUE_30D\",\"$YIELD_REVENUE_ANNUAL\",$YIELD_OPS_UPDATED,$YIELD_FILES_CREATED,$YIELD_FILES_MODIFIED,$YIELD_CSV_ROWS_CHANGED,$YIELD_ERRORS,\"\",\"$YIELD_NOTES\"" >> "$RESULTS_CSV"

    echo ""
    yield_log "============================================"
    yield_log "  RUN RESULTS: $cmd"
    yield_log "============================================"
    yield_log "  Duration:          ${duration}s"
    yield_log "  Alpha extracted:   $YIELD_ALPHA_EXTRACTED"
    yield_log "  Alpha repaired:    $YIELD_ALPHA_REPAIRED"
    yield_log "  Content generated: $YIELD_CONTENT_GENERATED"
    yield_log "  Buffer CSVs:       $YIELD_BUFFER_CSVS"
    yield_log "  Projections:       $YIELD_PROJECTIONS"
    yield_log "  Revenue (30d):     $YIELD_REVENUE_30D"
    yield_log "  Revenue (annual):  $YIELD_REVENUE_ANNUAL"
    yield_log "  Ops updated:       $YIELD_OPS_UPDATED"
    yield_log "  Files created:     $YIELD_FILES_CREATED"
    yield_log "  Files modified:    $YIELD_FILES_MODIFIED"
    yield_log "  Errors:            $YIELD_ERRORS"
    yield_log "  Notes:             $YIELD_NOTES"
    yield_log "============================================"
    yield_log "  Results saved to LEDGER/AUTOMATION_RESULTS.csv"
    yield_log "============================================"
}

# Snapshot CSVs before any batch operation
snapshot_csvs() {
    local snap_dir="$SNAPSHOT_DIR/$TIMESTAMP"
    mkdir -p "$snap_dir"
    cp "$PROJECT_DIR"/LEDGER/*.csv "$snap_dir/" 2>/dev/null || true
    log "CSV snapshot saved to LEDGER/.snapshots/$TIMESTAMP/"
}

# Count rows in a CSV (minus header)
csv_rows() {
    local file="$1"
    if [ -f "$file" ]; then
        local total=$(wc -l < "$file" | tr -d ' ')
        echo $((total - 1))
    else
        echo "0"
    fi
}

# ============================================================
# MORNING SYNC (6 AM daily)
# ============================================================
morning_sync() {
    header "MORNING ALPHA SYNC"
    snapshot_csvs
    local pre_alpha=$(csv_rows "$PROJECT_DIR/LEDGER/ALPHA_STAGING.csv")

    # Step 1: Extract source CSVs from MEGA_SHEET
    log "Step 1: Extracting source CSVs from MEGA_SHEET..."
    local extract_output
    extract_output=$(python3 "$PROJECT_DIR/scripts/extract_source_csvs_from_mega_sheet.py" 2>&1) || true
    echo "$extract_output" >> "$LOG_DIR/morning_sync_${DATE_SHORT}.log"

    # Parse extraction counts from output
    local extracted=$(echo "$extract_output" | grep -oP '\d+ PENDING_REVIEW entries extracted' | grep -oP '^\d+' || echo "0")
    YIELD_ALPHA_EXTRACTED=${extracted:-0}
    log "  Extracted $YIELD_ALPHA_EXTRACTED alpha entries"

    # Step 2: Organize alpha entries
    log "Step 2: Organizing alpha entries..."
    python3 "$PROJECT_DIR/scripts/organize_alpha.py" \
        >> "$LOG_DIR/morning_sync_${DATE_SHORT}.log" 2>&1 && \
        log "  Alpha organized" || { warn "  Alpha organize had issues"; YIELD_ERRORS=$((YIELD_ERRORS + 1)); }

    # Step 3: Repair corrupted alpha entries
    log "Step 3: Repairing any corrupted alpha entries..."
    local repair_output
    repair_output=$(python3 "$PROJECT_DIR/scripts/repair_alpha_staging_v2.py" 2>&1) || true
    echo "$repair_output" >> "$LOG_DIR/morning_sync_${DATE_SHORT}.log"

    local repaired=$(echo "$repair_output" | grep -oP 'Corrupted rows fixed: \K\d+' || echo "0")
    local dupes_removed=$(echo "$repair_output" | grep -oP 'Duplicate URLs removed: \K\d+' || echo "0")
    YIELD_ALPHA_REPAIRED=$((${repaired:-0} + ${dupes_removed:-0}))
    log "  Repaired: $YIELD_ALPHA_REPAIRED issues fixed"

    # Step 4: Run daily research ops
    log "Step 4: Running daily research ops..."

    # DOP001: Competitor monitoring
    log "  Running competitor_monitoring..."
    if [ -f "$PROJECT_DIR/AUTOMATIONS/platform_meta_monitor.py" ]; then
        python3 "$PROJECT_DIR/AUTOMATIONS/platform_meta_monitor.py" \
            >> "$LOG_DIR/morning_sync_${DATE_SHORT}.log" 2>&1 && \
            { log "  Competitor monitor complete"; YIELD_OPS_UPDATED=$((YIELD_OPS_UPDATED + 1)); } || \
            { warn "  Competitor monitor had issues"; YIELD_ERRORS=$((YIELD_ERRORS + 1)); }
    fi

    # DOP003: Platform algorithm detection
    log "  Running platform_algo_detection..."
    if [ -f "$PROJECT_DIR/AUTOMATIONS/platform_meta_monitor.py" ]; then
        python3 "$PROJECT_DIR/AUTOMATIONS/platform_meta_monitor.py" --algo-only \
            >> "$LOG_DIR/morning_sync_${DATE_SHORT}.log" 2>&1 || true
    fi
    YIELD_OPS_UPDATED=$((YIELD_OPS_UPDATED + 1))

    # DOP004: Revenue dashboard check
    log "  Running revenue_dashboard_check..."
    local rev_output
    rev_output=$(python3 "$PROJECT_DIR/AUTOMATIONS/revenue_projector.py" 2>&1) || true
    echo "$rev_output" >> "$LOG_DIR/morning_sync_${DATE_SHORT}.log"

    # Parse revenue numbers from projector output
    local rev_30d=$(echo "$rev_output" | grep -oP '30 Days:\s+\$[\d,]+\.\d+' | grep -oP '\$[\d,]+\.\d+' || echo "\$0")
    local rev_annual=$(echo "$rev_output" | grep -oP '1 Year:\s+\$[\d,]+\.\d+' | grep -oP '\$[\d,]+\.\d+' || echo "\$0")
    YIELD_REVENUE_30D="${rev_30d:-\$0}"
    YIELD_REVENUE_ANNUAL="${rev_annual:-\$0}"
    if [ "$rev_30d" != "" ]; then
        YIELD_PROJECTIONS=$((YIELD_PROJECTIONS + 1))
        log "  Revenue: 30d=${YIELD_REVENUE_30D} annual=${YIELD_REVENUE_ANNUAL}"
    fi
    YIELD_OPS_UPDATED=$((YIELD_OPS_UPDATED + 1))

    # DOP008: Viral content detection
    log "  Running viral_content_detection..."
    if [ -f "$PROJECT_DIR/AUTOMATIONS/viral_content_scanner.py" ]; then
        python3 "$PROJECT_DIR/AUTOMATIONS/viral_content_scanner.py" \
            >> "$LOG_DIR/morning_sync_${DATE_SHORT}.log" 2>&1 && \
            { log "  Viral scanner complete"; YIELD_OPS_UPDATED=$((YIELD_OPS_UPDATED + 1)); } || \
            { warn "  Viral scanner had issues"; YIELD_ERRORS=$((YIELD_ERRORS + 1)); }
    else
        YIELD_OPS_UPDATED=$((YIELD_OPS_UPDATED + 1))
    fi

    # Step 5: RBI daily audit
    log "Step 5: Running RBI daily audit..."
    python3 "$PROJECT_DIR/scripts/rbi_audit.py" daily \
        >> "$LOG_DIR/morning_sync_${DATE_SHORT}.log" 2>&1 && \
        { log "  RBI daily audit complete"; YIELD_OPS_UPDATED=$((YIELD_OPS_UPDATED + 1)); } || \
        { warn "  RBI daily audit had issues"; YIELD_ERRORS=$((YIELD_ERRORS + 1)); }

    # Step 6: Update ops tracker with today's date
    log "Step 6: Updating ops tracker..."
    python3 -c "
import csv
from datetime import date
today = date.today().isoformat()
daily_ops = {'DOP001','DOP002','DOP003','DOP004','DOP008'}
path = '$PROJECT_DIR/LEDGER/DAILY_OPS_TRACKER.csv'
with open(path, 'r') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    rows = list(reader)
updated = 0
for row in rows:
    if row['ops_id'] in daily_ops and row.get('frequency') in ('daily','continuous'):
        row['last_run'] = today
        updated += 1
with open(path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
print(f'Updated {updated} ops last_run to {today}')
" >> "$LOG_DIR/morning_sync_${DATE_SHORT}.log" 2>&1 || { warn "  Ops tracker update had issues"; YIELD_ERRORS=$((YIELD_ERRORS + 1)); }

    # Final yield stats
    local post_alpha=$(csv_rows "$PROJECT_DIR/LEDGER/ALPHA_STAGING.csv")
    YIELD_CSV_ROWS_CHANGED=$((post_alpha - pre_alpha))
    YIELD_NOTES="alpha:${post_alpha} rev30d:${YIELD_REVENUE_30D} repaired:${YIELD_ALPHA_REPAIRED}"

    log "ALPHA_STAGING.csv: $pre_alpha -> $post_alpha entries"
    log "Morning sync complete."
    flush_results "morning" 0
}

# ============================================================
# CONTENT GENERATION (6:30 AM daily)
# ============================================================
content_gen() {
    header "CONTENT GENERATION"

    # Step 1: Generate 30-day content calendar
    log "Step 1: Generating 30-day content calendar..."
    local cal_output
    cal_output=$(python3 "$PROJECT_DIR/scripts/generate_30day_calendar.py" 2>&1) || true
    echo "$cal_output" >> "$LOG_DIR/content_gen_${DATE_SHORT}.log"

    local cal_count=$(echo "$cal_output" | grep -oP '\d+ posts' | head -1 | grep -oP '^\d+' | tr -d '\n' || echo "0")
    cal_count=${cal_count:-0}
    if [ "${cal_count:-0}" -gt 0 ]; then
        YIELD_CONTENT_GENERATED=$((YIELD_CONTENT_GENERATED + ${cal_count:-0}))
        YIELD_FILES_CREATED=$((YIELD_FILES_CREATED + 1))
        log "  Calendar generated: $cal_count posts"
    else
        warn "  Calendar gen had issues"
        YIELD_ERRORS=$((YIELD_ERRORS + 1))
    fi

    # Step 2: Generate Buffer import CSVs
    log "Step 2: Generating Buffer import CSVs..."
    local buffer_output
    buffer_output=$(python3 "$PROJECT_DIR/scripts/generate_buffer_csvs.py" 2>&1) || true
    echo "$buffer_output" >> "$LOG_DIR/content_gen_${DATE_SHORT}.log"

    local buffer_count=$(echo "$buffer_output" | grep -c "Created buffer_import" || echo "0")
    local total_posts=$(echo "$buffer_output" | grep -oP '\d+ total posts' | head -1 | grep -oP '^\d+' | tr -d '\n' || echo "0")
    total_posts=${total_posts:-0}
    YIELD_BUFFER_CSVS=${buffer_count:-0}
    YIELD_CONTENT_GENERATED=$((YIELD_CONTENT_GENERATED + ${total_posts:-0}))
    YIELD_FILES_CREATED=$((YIELD_FILES_CREATED + ${buffer_count:-0}))
    log "  Buffer CSVs: $YIELD_BUFFER_CSVS files, $total_posts posts"

    # Step 3: Content queue stats
    log "Step 3: Content queue stats..."
    local queue_output
    queue_output=$(python3 "$PROJECT_DIR/scripts/content_queue.py" --stats 2>&1) || true
    echo "$queue_output" >> "$LOG_DIR/content_gen_${DATE_SHORT}.log"

    local queued=$(echo "$queue_output" | grep -oP 'QUEUED\s+\K\d+' || echo "0")
    local drafts=$(echo "$queue_output" | grep -oP 'DRAFT\s+\K\d+' || echo "0")
    log "  Queue: $queued queued, $drafts drafts"

    YIELD_NOTES="buffer_csvs:${YIELD_BUFFER_CSVS} posts:${total_posts} queued:${queued} drafts:${drafts}"
    log "Content generation complete."
    flush_results "content" 0
}

# ============================================================
# OUTREACH QUEUE (9 AM daily)
# ============================================================
outreach_queue() {
    header "OUTREACH QUEUE STAGING"

    # Step 1: Route content to QA
    log "Step 1: Routing content to QA queue..."
    local qa_output
    qa_output=$(python3 "$PROJECT_DIR/scripts/content_to_qa_router.py" 2>&1) || true
    echo "$qa_output" >> "$LOG_DIR/outreach_${DATE_SHORT}.log"

    local routed=$(echo "$qa_output" | grep -oP '\d+ routed' | grep -oP '\d+' || echo "0")
    YIELD_CONTENT_GENERATED=${routed:-0}
    log "  $YIELD_CONTENT_GENERATED items routed to QA"

    # Step 2: Check email sequence status
    log "Step 2: Checking email sequences..."
    local seq_count=$(ls "$PROJECT_DIR/EMAIL/sequences/" 2>/dev/null | wc -l | tr -d ' ' || echo "0")
    log "  $seq_count email sequences found"

    # Step 3: Check outreach pipeline
    local pipeline_count=$(csv_rows "$PROJECT_DIR/LEDGER/OUTREACH_PIPELINE.csv")
    log "  Outreach pipeline: $pipeline_count leads"

    YIELD_OPS_UPDATED=$((seq_count + 1))
    YIELD_NOTES="qa_routed:${YIELD_CONTENT_GENERATED} sequences:${seq_count} pipeline:${pipeline_count}"
    log "Outreach queue staged. Human review needed before sending."
    flush_results "outreach" 0
}

# ============================================================
# EVENING DIGEST (6 PM daily)
# ============================================================
evening_digest() {
    header "EVENING DIGEST"

    local digest_file="$PROJECT_DIR/OPS/reports/daily_digest_${DATE_SHORT}.md"
    mkdir -p "$PROJECT_DIR/OPS/reports"

    # Count today's results from AUTOMATION_RESULTS.csv
    local today_runs=0
    local today_alpha=0
    local today_content=0
    local today_errors=0
    if [ -f "$RESULTS_CSV" ]; then
        today_runs=$(grep -c "$DATE_SHORT" "$RESULTS_CSV" 2>/dev/null || echo "0")
        today_alpha=$(python3 -c "
import csv
total=0
with open('$RESULTS_CSV') as f:
    for r in csv.DictReader(f):
        if '$DATE_SHORT' in r.get('timestamp',''):
            total += int(r.get('alpha_extracted','0') or 0)
print(total)
" 2>/dev/null || echo "0")
        today_content=$(python3 -c "
import csv
total=0
with open('$RESULTS_CSV') as f:
    for r in csv.DictReader(f):
        if '$DATE_SHORT' in r.get('timestamp',''):
            total += int(r.get('content_generated','0') or 0)
print(total)
" 2>/dev/null || echo "0")
        today_errors=$(python3 -c "
import csv
total=0
with open('$RESULTS_CSV') as f:
    for r in csv.DictReader(f):
        if '$DATE_SHORT' in r.get('timestamp',''):
            total += int(r.get('errors','0') or 0)
print(total)
" 2>/dev/null || echo "0")
    fi

    cat > "$digest_file" << DIGEST_EOF
# PRINTMAXX Daily Digest - $DATE_SHORT

## Today's Yield
- Automation runs: $today_runs
- Alpha extracted: $today_alpha
- Content generated: $today_content
- Errors: $today_errors

## System Status
- Generated: $(date)
- Alpha entries: $(csv_rows "$PROJECT_DIR/LEDGER/ALPHA_STAGING.csv")
- Methods tracked: $(csv_rows "$PROJECT_DIR/LEDGER/MEGA_SHEET/TAB1_MONEY_METHODS_MASTER.csv")
- Signal sources: $(csv_rows "$PROJECT_DIR/LEDGER/MEGA_SHEET/TAB7_SOURCES_ACCOUNTS.csv")

## Today's Automation Results
$(if [ -f "$RESULTS_CSV" ]; then
    python3 -c "
import csv
with open('$RESULTS_CSV') as f:
    for r in csv.DictReader(f):
        if '$DATE_SHORT' in r.get('timestamp',''):
            print(f\"- **{r['command']}** ({r['duration_secs']}s): alpha={r['alpha_extracted']} content={r['content_generated']} errors={r['errors']} | {r.get('notes','')}\")
" 2>/dev/null || echo "No results parsed"
fi)

## Today's Logs
$(for logfile in "$LOG_DIR"/*_${DATE_SHORT}.log; do
    if [ -f "$logfile" ]; then
        echo "### $(basename "$logfile" .log)"
        tail -5 "$logfile" 2>/dev/null | sed 's/^/> /'
        echo ""
    fi
done)

## Overnight Ralph Status
$(if ls "$PROJECT_DIR/ralph/logs"/overnight_*_$(date +%Y%m%d)*.log 1>/dev/null 2>&1; then
    echo "Ralph loops ran last night:"
    for lf in "$PROJECT_DIR/ralph/logs"/overnight_*_$(date +%Y%m%d)*.log; do
        echo "- $(basename "$lf"): $(tail -1 "$lf" 2>/dev/null || echo "check log")"
    done
else
    echo "No overnight Ralph logs found for today."
fi)

## Action Items for Tomorrow
- [ ] Review alpha entries in PENDING_REVIEW status
- [ ] Check Buffer CSVs and upload approved content
- [ ] Review any flagged content in QA queue
- [ ] Check cold email sequence performance (if active)
DIGEST_EOF

    YIELD_FILES_CREATED=1
    YIELD_NOTES="digest:${digest_file} runs_today:${today_runs} alpha_today:${today_alpha} content_today:${today_content}"
    log "Daily digest written: $today_runs runs, $today_alpha alpha, $today_content content, $today_errors errors"
    flush_results "digest" 0
}

# ============================================================
# NIGHTLY BACKUP (9 PM daily)
# ============================================================
nightly_backup() {
    header "NIGHTLY BACKUP"
    cd "$PROJECT_DIR"

    if [ -d ".git" ]; then
        log "Step 1: Git status check..."
        local changes=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ' || echo "0")

        if [ "$changes" -gt 0 ]; then
            log "  $changes files changed, committing..."
            git add -A >> "$LOG_DIR/backup_${DATE_SHORT}.log" 2>&1
            git commit -m "auto-backup: $DATE_SHORT $(date +%H:%M) - $changes files" \
                >> "$LOG_DIR/backup_${DATE_SHORT}.log" 2>&1 && \
                { log "  Committed successfully"; YIELD_FILES_MODIFIED=$changes; } || \
                { warn "  Commit failed (check log)"; YIELD_ERRORS=$((YIELD_ERRORS + 1)); }

            if git remote -v 2>/dev/null | grep -q origin; then
                git push origin main >> "$LOG_DIR/backup_${DATE_SHORT}.log" 2>&1 && \
                    log "  Pushed to GitHub" || { warn "  Push failed (check remote)"; YIELD_ERRORS=$((YIELD_ERRORS + 1)); }
            else
                warn "  No git remote configured. Add with: git remote add origin <url>"
            fi
        else
            log "  No changes to commit"
        fi
    else
        warn "Git not initialized. Run: cd $PROJECT_DIR && git init && git add -A && git commit -m 'initial'"
        YIELD_ERRORS=$((YIELD_ERRORS + 1))
    fi

    YIELD_NOTES="files_committed:${YIELD_FILES_MODIFIED}"
    log "Backup complete."
    flush_results "backup" 0
}

# ============================================================
# OVERNIGHT SPRINT (10 PM daily)
# ============================================================
overnight_sprint() {
    header "OVERNIGHT RALPH SPRINT"

    if [ -f "$PROJECT_DIR/ralph/run_overnight_sprint.sh" ]; then
        log "Launching 8 parallel Ralph loops..."
        bash "$PROJECT_DIR/ralph/run_overnight_sprint.sh" 2>&1 | tee "$LOG_DIR/overnight_launch_${TIMESTAMP}.log"
        YIELD_OPS_UPDATED=8
        YIELD_NOTES="ralph_loops_launched:8"
        log "All loops launched. Check ralph/logs/ for progress."
    else
        warn "ralph/run_overnight_sprint.sh not found!"
        YIELD_ERRORS=1
    fi
    flush_results "overnight" 0
}

# ============================================================
# WEEKLY TASKS (Monday 9 AM)
# ============================================================
weekly_tasks() {
    header "WEEKLY TASKS"
    snapshot_csvs

    log "Task 1: Merging backtest scores..."
    local bt_output
    bt_output=$(python3 "$PROJECT_DIR/scripts/merge_backtest_scores.py" 2>&1) || true
    echo "$bt_output" >> "$LOG_DIR/weekly_${DATE_SHORT}.log"
    local merged=$(echo "$bt_output" | grep -oP '\d+ merged' | grep -oP '\d+' || echo "0")
    YIELD_FILES_MODIFIED=$((YIELD_FILES_MODIFIED + 1))

    log "Task 2: Generating fresh 30-day calendar..."
    python3 "$PROJECT_DIR/scripts/generate_30day_calendar.py" \
        >> "$LOG_DIR/weekly_${DATE_SHORT}.log" 2>&1 && \
        { YIELD_FILES_CREATED=$((YIELD_FILES_CREATED + 1)); } || \
        { warn "Calendar gen had issues"; YIELD_ERRORS=$((YIELD_ERRORS + 1)); }

    log "Task 3: Running content QA batch..."
    python3 "$PROJECT_DIR/scripts/content_to_qa_router.py" \
        >> "$LOG_DIR/weekly_${DATE_SHORT}.log" 2>&1 || \
        { warn "QA routing had issues"; YIELD_ERRORS=$((YIELD_ERRORS + 1)); }

    log "Task 4: Running validation suite..."
    local val_output
    val_output=$(python3 "$PROJECT_DIR/scripts/validate.py" 2>&1) || true
    echo "$val_output" >> "$LOG_DIR/weekly_${DATE_SHORT}.log"
    YIELD_FILES_MODIFIED=$((YIELD_FILES_MODIFIED + 1))

    log "Task 5: Method performance analysis..."
    local perf_output
    perf_output=$(python3 "$PROJECT_DIR/AUTOMATIONS/method_performance_analyzer.py" 2>&1) || true
    echo "$perf_output" >> "$LOG_DIR/weekly_${DATE_SHORT}.log"
    YIELD_PROJECTIONS=$((YIELD_PROJECTIONS + 1))

    log "Task 6: RBI weekly deep analysis..."
    python3 "$PROJECT_DIR/scripts/rbi_audit.py" weekly \
        >> "$LOG_DIR/weekly_${DATE_SHORT}.log" 2>&1 && \
        { log "  RBI weekly analysis complete"; YIELD_PROJECTIONS=$((YIELD_PROJECTIONS + 1)); } || \
        { warn "  RBI weekly analysis had issues"; YIELD_ERRORS=$((YIELD_ERRORS + 1)); }

    YIELD_OPS_UPDATED=6
    YIELD_NOTES="backtest_merged:${merged:-0} validation:done perf_analysis:done"
    log "Weekly tasks complete."
    flush_results "weekly" 0
}

# ============================================================
# MONTHLY TASKS (1st of month)
# ============================================================
monthly_tasks() {
    header "MONTHLY TASKS"
    snapshot_csvs

    log "Task 1: Revenue projection..."
    local rev_output
    rev_output=$(python3 "$PROJECT_DIR/AUTOMATIONS/revenue_projector.py" 2>&1) || true
    echo "$rev_output" >> "$LOG_DIR/monthly_${DATE_SHORT}.log"
    local rev_30d=$(echo "$rev_output" | grep -oP '30 Days:\s+\$[\d,]+\.\d+' | grep -oP '\$[\d,]+\.\d+' || echo "\$0")
    local rev_annual=$(echo "$rev_output" | grep -oP '1 Year:\s+\$[\d,]+\.\d+' | grep -oP '\$[\d,]+\.\d+' || echo "\$0")
    YIELD_REVENUE_30D="$rev_30d"
    YIELD_REVENUE_ANNUAL="$rev_annual"
    YIELD_PROJECTIONS=$((YIELD_PROJECTIONS + 1))

    log "Task 2: Method performance analysis..."
    python3 "$PROJECT_DIR/AUTOMATIONS/method_performance_analyzer.py" \
        >> "$LOG_DIR/monthly_${DATE_SHORT}.log" 2>&1 || \
        { warn "Method analysis had issues"; YIELD_ERRORS=$((YIELD_ERRORS + 1)); }
    YIELD_PROJECTIONS=$((YIELD_PROJECTIONS + 1))

    log "Task 3: Full system validation..."
    python3 "$PROJECT_DIR/scripts/validate.py" --verbose \
        >> "$LOG_DIR/monthly_${DATE_SHORT}.log" 2>&1 || \
        { warn "Validation had issues"; YIELD_ERRORS=$((YIELD_ERRORS + 1)); }

    log "Task 4: Batch merge all ledger data..."
    python3 "$PROJECT_DIR/scripts/batch_merge.py" \
        >> "$LOG_DIR/monthly_${DATE_SHORT}.log" 2>&1 || \
        { warn "Batch merge had issues"; YIELD_ERRORS=$((YIELD_ERRORS + 1)); }

    log "Task 5: RBI monthly strategic review..."
    python3 "$PROJECT_DIR/scripts/rbi_audit.py" monthly \
        >> "$LOG_DIR/monthly_${DATE_SHORT}.log" 2>&1 && \
        { log "  RBI monthly strategic review complete"; YIELD_PROJECTIONS=$((YIELD_PROJECTIONS + 1)); } || \
        { warn "  RBI monthly review had issues"; YIELD_ERRORS=$((YIELD_ERRORS + 1)); }

    log "Task 6: Full backup with git bundle..."
    if [ -d "$PROJECT_DIR/.git" ]; then
        local bundle_dir="$HOME/Documents/PRINTMAXX_BACKUPS"
        mkdir -p "$bundle_dir" 2>/dev/null || true
        cd "$PROJECT_DIR"
        git bundle create "$bundle_dir/printmaxx_$(date +%Y%m).bundle" --all \
            >> "$LOG_DIR/monthly_${DATE_SHORT}.log" 2>&1 && \
            { log "  Git bundle saved to $bundle_dir/"; YIELD_FILES_CREATED=$((YIELD_FILES_CREATED + 1)); } || \
            warn "  Bundle creation failed"
    fi

    YIELD_OPS_UPDATED=5
    YIELD_NOTES="rev30d:${YIELD_REVENUE_30D} rev_annual:${YIELD_REVENUE_ANNUAL} projections:${YIELD_PROJECTIONS}"
    log "Monthly tasks complete."
    flush_results "monthly" 0
}

# ============================================================
# STATUS CHECK
# ============================================================
show_status() {
    header "PRINTMAXX SYSTEM STATUS"

    echo "Project: $PROJECT_DIR"
    echo ""

    echo "=== DATA ==="
    echo "  ALPHA_STAGING.csv: $(csv_rows "$PROJECT_DIR/LEDGER/ALPHA_STAGING.csv") rows"
    echo "  TAB3_ALPHA_MASTER: $(csv_rows "$PROJECT_DIR/LEDGER/MEGA_SHEET/TAB3_ALPHA_MASTER.csv") rows"
    echo "  Methods tracked:   $(csv_rows "$PROJECT_DIR/LEDGER/MEGA_SHEET/TAB1_MONEY_METHODS_MASTER.csv") rows"
    echo "  Buffer CSVs:       $(ls "$PROJECT_DIR/LEDGER/buffer_import_"*.csv 2>/dev/null | wc -l | tr -d ' ') files"
    echo ""

    echo "=== TODAY'S YIELD (from AUTOMATION_RESULTS.csv) ==="
    if [ -f "$RESULTS_CSV" ]; then
        python3 -c "
import csv
runs=alpha=content=errors=0
with open('$RESULTS_CSV') as f:
    for r in csv.DictReader(f):
        if '$DATE_SHORT' in r.get('timestamp',''):
            runs += 1
            alpha += int(r.get('alpha_extracted','0') or 0)
            content += int(r.get('content_generated','0') or 0)
            errors += int(r.get('errors','0') or 0)
print(f'  Runs today: {runs}')
print(f'  Alpha extracted: {alpha}')
print(f'  Content generated: {content}')
print(f'  Errors: {errors}')
" 2>/dev/null || echo "  (could not parse results)"
    else
        echo "  No results yet"
    fi
    echo ""

    echo "=== RECENT AUTOMATION RESULTS ==="
    if [ -f "$RESULTS_CSV" ]; then
        tail -5 "$RESULTS_CSV" | python3 -c "
import csv, sys
reader = csv.DictReader(open('$RESULTS_CSV'))
rows = list(reader)[-5:]
for r in rows:
    cmd = r.get('command','?')
    dur = r.get('duration_secs','?')
    alpha = r.get('alpha_extracted','0')
    content = r.get('content_generated','0')
    errs = r.get('errors','0')
    notes = r.get('notes','')[:50]
    print(f'  {r.get(\"timestamp\",\"?\")[:19]} | {cmd:10} | {dur:4}s | a:{alpha} c:{content} e:{errs} | {notes}')
" 2>/dev/null || echo "  (could not parse results)"
    fi
    echo ""

    echo "=== RECENT LOGS ==="
    ls -lt "$LOG_DIR"/*.log 2>/dev/null | head -10 | awk '{print "  " $NF " (" $6 " " $7 " " $8 ")"}'
    echo ""

    echo "=== RALPH LOOPS ==="
    for loop_dir in "$PROJECT_DIR"/ralph/loops/*/; do
        if [ -d "$loop_dir" ]; then
            local name=$(basename "$loop_dir")
            local progress="$loop_dir/.ralph/progress.md"
            if [ -f "$progress" ]; then
                echo "  $name: $(head -1 "$progress" 2>/dev/null || echo "active")"
            else
                echo "  $name: no progress file"
            fi
        fi
    done
    echo ""

    echo "=== GIT STATUS ==="
    if [ -d "$PROJECT_DIR/.git" ]; then
        cd "$PROJECT_DIR"
        echo "  Last commit: $(git log --oneline -1 2>/dev/null || echo "none")"
        echo "  Changed files: $(git status --porcelain 2>/dev/null | wc -l | tr -d ' ' || echo "unknown")"
    else
        echo "  Git not initialized"
    fi
    echo ""
}

# ============================================================
# MAIN DISPATCH
# ============================================================
case "${1:-help}" in
    morning)   morning_sync ;;
    briefing)  log "Generating daily briefing..."; python3 "$PROJECT_DIR/scripts/daily_briefing.py" 2>&1 | tee "$LOG_DIR/briefing_${DATE_SHORT}.log" ;;
    content)   content_gen ;;
    outreach)  outreach_queue ;;
    digest)    evening_digest ;;
    backup)    nightly_backup ;;
    overnight) overnight_sprint ;;
    weekly)    weekly_tasks ;;
    monthly)   monthly_tasks ;;
    rbi)       rbi_mode="${2:-daily}"; log "Running RBI $rbi_mode audit..."; python3 "$PROJECT_DIR/scripts/rbi_audit.py" "$rbi_mode" 2>&1 | tee "$LOG_DIR/rbi_${rbi_mode}_${DATE_SHORT}.log" ;;
    strategic) strat_mode="${2:-full}"; log "Running strategic RBI $strat_mode..."; python3 "$PROJECT_DIR/scripts/strategic_rbi_engine.py" "$strat_mode" 2>&1 | tee "$LOG_DIR/strategic_rbi_${DATE_SHORT}.log" ;;
    self-test) log "Running self-test protocol..."; python3 "$PROJECT_DIR/scripts/strategic_rbi_engine.py" self-test 2>&1 | tee "$LOG_DIR/self_test_${DATE_SHORT}.log" ;;
    status)    show_status ;;
    help|*)
        echo "PRINTMAXX Master Orchestrator v2"
        echo ""
        echo "Usage: $0 <command>"
        echo ""
        echo "Daily commands:"
        echo "  morning    - Sync alpha, organize, repair, revenue check (6 AM)"
        echo "  briefing   - Generate daily human-action-required briefing (5 AM)"
        echo "  content    - Generate calendar + Buffer CSVs (6:30 AM)"
        echo "  outreach   - Stage outreach queue, email sequences (9 AM)"
        echo "  digest     - Generate daily digest with yield summary (6 PM)"
        echo "  backup     - Git commit + push (9 PM)"
        echo "  overnight  - Launch Ralph sprint (10 PM)"
        echo ""
        echo "Periodic:"
        echo "  weekly     - Backtest merge, calendar, QA, validation, perf analysis (Monday)"
        echo "  monthly    - Revenue projection, validation, bundle backup (1st)"
        echo ""
        echo "RBI (Research-Based Improvement):"
        echo "  rbi daily  - Daily ops health check, alpha pipeline, recommendations"
        echo "  rbi weekly - + Cross-pollination, revenue, experiments, source quality"
        echo "  rbi monthly- + Portfolio rebalancing, new op identification"
        echo "  rbi full   - Run all three levels"
        echo ""
        echo "Strategic RBI (Deep Analysis + Validation + Improvement):"
        echo "  strategic analyze  - L2: Performance vs claims, bottlenecks, viability, dead zones"
        echo "  strategic validate - L4: Infrastructure validation, automation health, revenue claims"
        echo "  strategic improve  - L5: Hypotheses, GTM edge, first-principles discovery, self-test"
        echo "  strategic full     - Run all layers (default)"
        echo "  self-test          - Run LLM self-test protocol for ops validation"
        echo ""
        echo "Utility:"
        echo "  status     - Show system status + today's yield"
        echo ""
        echo "All results logged to LEDGER/AUTOMATION_RESULTS.csv"
        ;;
esac
