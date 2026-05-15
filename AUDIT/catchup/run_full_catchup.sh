#!/bin/bash
# Full v9 pipeline catch-up — fires every active stage in correct phase order.
# Mirrors the crontab so we know exactly what each phase touches.
# Output: AUDIT/catchup/run_<ts>.log with per-script timing + exit codes.

set -uo pipefail

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
PYTHON="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
TS=$(date +%Y%m%d_%H%M%S)
RUNLOG="$BASE/AUDIT/catchup/run_${TS}.log"
SUMMARY="$BASE/AUDIT/catchup/SUMMARY_${TS}.md"

cd "$BASE"
mkdir -p AUDIT/catchup AUTOMATIONS/logs

exec > >(tee -a "$RUNLOG") 2>&1

echo "=========================================================="
echo "  CATCHUP RUN  $(date '+%Y-%m-%d %H:%M:%S')"
echo "  Log: $RUNLOG"
echo "=========================================================="

run_one() {
  local name="$1"; shift
  local start=$(date +%s)
  echo ""
  echo "--- [$(date '+%H:%M:%S')] START: $name ---"
  ( "$@" ) ; local rc=$?
  local end=$(date +%s)
  local dur=$((end-start))
  echo "--- [$(date '+%H:%M:%S')] END:   $name (rc=$rc dur=${dur}s) ---"
  echo "$name,$rc,$dur" >> "$BASE/AUDIT/catchup/results_${TS}.csv"
}

# Wrapper so we can run python jobs in parallel from bash arrays
py() { run_one "$1" "$PYTHON" "$2" "${@:3}"; }

echo "name,exit_code,duration_secs" > "$BASE/AUDIT/catchup/results_${TS}.csv"

# ════════════════════════════════════════════════════════════
# PHASE 1: SCAN (parallel)
# ════════════════════════════════════════════════════════════
echo ""
echo "############ PHASE 1: SCAN ############"
py "sec_edgar_scanner"       AUTOMATIONS/sec_edgar_scanner.py       --scan &
py "crunchbase_scanner"      AUTOMATIONS/crunchbase_scanner.py      --scan &
py "ecom_arb_engine"         AUTOMATIONS/ecom_arb_engine.py         --scan &
py "method_discovery"        AUTOMATIONS/method_discovery_crawler.py --crawl &
py "opportunity_radar"       AUTOMATIONS/opportunity_radar.py       --scan &
py "sam_gov_monitor"         AUTOMATIONS/sam_gov_monitor.py                 &
py "morning_intelligence"    AUTOMATIONS/morning_intelligence_dag.py        &
py "health_check_all"        AUTOMATIONS/health_check_all.py        --check &
wait
echo "PHASE 1 complete."

# ════════════════════════════════════════════════════════════
# PHASE 2: PROCESS (parallel)
# ════════════════════════════════════════════════════════════
echo ""
echo "############ PHASE 2: PROCESS ############"
py "auto_approve"            AUTOMATIONS/auto_approve.py                       &
py "sqlite_alpha_index"      AUTOMATIONS/sqlite_alpha_index.py     --rebuild   &
py "alpha_backlog_scanner"   AUTOMATIONS/alpha_backlog_scanner.py  --scan      &
wait
echo "PHASE 2 complete."

# ════════════════════════════════════════════════════════════
# PHASE 3: RANK
# ════════════════════════════════════════════════════════════
echo ""
echo "############ PHASE 3: RANK ############"
py "capital_genesis_ranker"  AUTOMATIONS/capital_genesis_ranker.py --rank --report
echo "PHASE 3 complete."

# ════════════════════════════════════════════════════════════
# PHASE 4: DECIDE / EXECUTE (parallel)
# ════════════════════════════════════════════════════════════
echo ""
echo "############ PHASE 4: DECIDE / EXECUTE ############"
py "rbi_loop"                AUTOMATIONS/rbi_loop.py               --full &
py "actionable_aggregator"   AUTOMATIONS/actionable_aggregator.py         &
py "decision_engine"         AUTOMATIONS/decision_engine.py        --cycle &
wait
echo "PHASE 4 complete."

# ════════════════════════════════════════════════════════════
# PHASE 5: REPORT (parallel)
# ════════════════════════════════════════════════════════════
echo ""
echo "############ PHASE 5: REPORT ############"
py "daily_digest"            AUTOMATIONS/daily_digest.py        &
py "session_briefing"        AUTOMATIONS/session_briefing.py    &
wait
echo "PHASE 5 complete."

# ════════════════════════════════════════════════════════════
# CONTINUOUS + WEEKLY CATCHUP (run if overdue)
# ════════════════════════════════════════════════════════════
echo ""
echo "############ CONTINUOUS + WEEKLY CATCHUP ############"
py "log_rotator"             AUTOMATIONS/log_rotator.py            --rotate          &
py "system_health_monitor"   AUTOMATIONS/system_health_monitor.py  --quick           &
py "usage_optimizer"         AUTOMATIONS/usage_optimizer.py        --optimize        &
py "perpetual_guardian"      AUTOMATIONS/perpetual_guardian.py     --full            &
py "cross_pollinator_v2"     AUTOMATIONS/cross_pollinator_v2.py    --cycle           &
wait

# Weekly jobs — fire them once since they may be overdue
py "backup_system_full"      AUTOMATIONS/backup_system.py          --incremental     &
py "cognitive_engine"        AUTOMATIONS/cognitive_engine.py       --build-model     &
py "security_audit"          AUTOMATIONS/security_audit.py         --quick           &
py "orphan_doc_scanner"      AUTOMATIONS/orphan_doc_scanner.py     --scan            &
py "gov_tenders_scraper"     AUTOMATIONS/gov_tenders_scraper.py                      &
py "saas_opportunity_engine" AUTOMATIONS/saas_opportunity_engine.py --scan           &
wait

echo ""
echo "=========================================================="
echo "  CATCHUP COMPLETE  $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================================="

# ════════════════════════════════════════════════════════════
# WRITE SUMMARY MARKDOWN
# ════════════════════════════════════════════════════════════
{
  echo "# Catchup Run Summary"
  echo ""
  echo "**Started**: ${TS}"
  echo "**Finished**: $(date '+%Y-%m-%d %H:%M:%S')"
  echo "**Log**: \`AUDIT/catchup/run_${TS}.log\`"
  echo ""
  echo "## Per-script results"
  echo ""
  echo "| script | exit | seconds |"
  echo "|---|---|---|"
  tail -n +2 "$BASE/AUDIT/catchup/results_${TS}.csv" | awk -F, '{printf "| %s | %s | %s |\n", $1, $2, $3}'
  echo ""
  echo "## Failures (non-zero exits)"
  echo ""
  fails=$(tail -n +2 "$BASE/AUDIT/catchup/results_${TS}.csv" | awk -F, '$2 != "0"')
  if [ -z "$fails" ]; then echo "_None._"; else echo "$fails" | awk -F, '{printf "- **%s** rc=%s (%ss)\n", $1, $2, $3}'; fi
} > "$SUMMARY"

echo "Summary written: $SUMMARY"
