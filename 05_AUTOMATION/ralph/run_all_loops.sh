#!/bin/bash
# PRINTMAXX Master Ralph Runner
# Runs all loops in parallel overnight
# Usage: ./run_all_loops.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y-%m-%d_%H%M)

echo "============================================"
echo "PRINTMAXX Overnight Ralph Run"
echo "Started: $(date)"
echo "============================================"
echo ""

# Run all loops in parallel
echo "Launching loops..."

# Content Social (15 batches)
echo "  Starting: content_social"
"$SCRIPT_DIR/loops/content_social/run.sh" 15 > "$LOG_DIR/content_social_$TIMESTAMP.log" 2>&1 &
PID1=$!

# Automation Scripts (5 tasks)
echo "  Starting: automation_scripts"
"$SCRIPT_DIR/loops/automation_scripts/run.sh" 5 > "$LOG_DIR/automation_scripts_$TIMESTAMP.log" 2>&1 &
PID2=$!

# Cold Email (5 sequences)
echo "  Starting: cold_email"
"$SCRIPT_DIR/loops/cold_email/run.sh" 6 > "$LOG_DIR/cold_email_$TIMESTAMP.log" 2>&1 &
PID3=$!

# Landing Copy (6 apps)
echo "  Starting: landing_copy"
"$SCRIPT_DIR/loops/landing_copy/run.sh" 7 > "$LOG_DIR/landing_copy_$TIMESTAMP.log" 2>&1 &
PID4=$!

# Competitor Research (5 categories)
echo "  Starting: competitor_research"
"$SCRIPT_DIR/loops/competitor_research/run.sh" 6 > "$LOG_DIR/competitor_research_$TIMESTAMP.log" 2>&1 &
PID5=$!

# App Discovery (perpetual research for new wrappers/niches)
echo "  Starting: app_discovery"
"$SCRIPT_DIR/loops/app_discovery/run.sh" 10 > "$LOG_DIR/app_discovery_$TIMESTAMP.log" 2>&1 &
PID6=$!

# Content Research (content farm opportunities)
echo "  Starting: content_research"
"$SCRIPT_DIR/loops/content_research/run.sh" 8 > "$LOG_DIR/content_research_$TIMESTAMP.log" 2>&1 &
PID7=$!

# Outbound Research (cold email/LinkedIn tactics)
echo "  Starting: outbound_research"
"$SCRIPT_DIR/loops/outbound_research/run.sh" 8 > "$LOG_DIR/outbound_research_$TIMESTAMP.log" 2>&1 &
PID8=$!

# Growth Research (platform changes, automation limits)
echo "  Starting: growth_research"
"$SCRIPT_DIR/loops/growth_research/run.sh" 8 > "$LOG_DIR/growth_research_$TIMESTAMP.log" 2>&1 &
PID9=$!

# Monetization Research (pricing, upsells, payments)
echo "  Starting: monetization_research"
"$SCRIPT_DIR/loops/monetization_research/run.sh" 8 > "$LOG_DIR/monetization_research_$TIMESTAMP.log" 2>&1 &
PID10=$!

# Comprehensive Research (all money methods, niches, tools, cross-pollination)
echo "  Starting: comprehensive_research"
"$SCRIPT_DIR/loops/comprehensive_research/run.sh" > "$LOG_DIR/comprehensive_research_$TIMESTAMP.log" 2>&1 &
PID11=$!

# ECOM Arbitrage Research (Temu/AliExpress/Etsy opportunities)
echo "  Starting: ecom_arb_research"
"$SCRIPT_DIR/loops/ecom_arb_research/run.sh" 10 > "$LOG_DIR/ecom_arb_research_$TIMESTAMP.log" 2>&1 &
PID12=$!

# Alpha Hunter (novel edge opportunities, hedge fund mindset)
echo "  Starting: alpha_hunter"
"$SCRIPT_DIR/loops/alpha_hunter/run.sh" 15 > "$LOG_DIR/alpha_hunter_$TIMESTAMP.log" 2>&1 &
PID13=$!

# Faceless Army (AI influencer scaling, platform changes, monetization)
echo "  Starting: faceless_army"
"$SCRIPT_DIR/loops/faceless_army/run.sh" 10 > "$LOG_DIR/faceless_army_$TIMESTAMP.log" 2>&1 &
PID14=$!

# Capital Genesis Intelligence (capital stacking, reinvestment timing, market signals)
echo "  Starting: capital_genesis"
"$SCRIPT_DIR/loops/capital_genesis/run.sh" 8 > "$LOG_DIR/capital_genesis_$TIMESTAMP.log" 2>&1 &
PID15=$!

echo ""
echo "All loops launched. PIDs: $PID1 $PID2 $PID3 $PID4 $PID5 $PID6 $PID7 $PID8 $PID9 $PID10 $PID11 $PID12 $PID13 $PID14 $PID15"
echo ""
echo "Monitor progress:"
echo "  tail -f $LOG_DIR/content_social_$TIMESTAMP.log"
echo "  tail -f $LOG_DIR/automation_scripts_$TIMESTAMP.log"
echo "  tail -f $LOG_DIR/cold_email_$TIMESTAMP.log"
echo "  tail -f $LOG_DIR/landing_copy_$TIMESTAMP.log"
echo "  tail -f $LOG_DIR/competitor_research_$TIMESTAMP.log"
echo "  tail -f $LOG_DIR/app_discovery_$TIMESTAMP.log"
echo "  tail -f $LOG_DIR/content_research_$TIMESTAMP.log"
echo "  tail -f $LOG_DIR/outbound_research_$TIMESTAMP.log"
echo "  tail -f $LOG_DIR/growth_research_$TIMESTAMP.log"
echo "  tail -f $LOG_DIR/monetization_research_$TIMESTAMP.log"
echo "  tail -f $LOG_DIR/comprehensive_research_$TIMESTAMP.log"
echo "  tail -f $LOG_DIR/ecom_arb_research_$TIMESTAMP.log"
echo "  tail -f $LOG_DIR/alpha_hunter_$TIMESTAMP.log"
echo "  tail -f $LOG_DIR/faceless_army_$TIMESTAMP.log"
echo "  tail -f $LOG_DIR/capital_genesis_$TIMESTAMP.log"
echo ""
echo "Or wait for all to complete..."

# Wait for all
wait $PID1 && echo "content_social: DONE" || echo "content_social: FAILED"
wait $PID2 && echo "automation_scripts: DONE" || echo "automation_scripts: FAILED"
wait $PID3 && echo "cold_email: DONE" || echo "cold_email: FAILED"
wait $PID4 && echo "landing_copy: DONE" || echo "landing_copy: FAILED"
wait $PID5 && echo "competitor_research: DONE" || echo "competitor_research: FAILED"
wait $PID6 && echo "app_discovery: DONE" || echo "app_discovery: FAILED"
wait $PID7 && echo "content_research: DONE" || echo "content_research: FAILED"
wait $PID8 && echo "outbound_research: DONE" || echo "outbound_research: FAILED"
wait $PID9 && echo "growth_research: DONE" || echo "growth_research: FAILED"
wait $PID10 && echo "monetization_research: DONE" || echo "monetization_research: FAILED"
wait $PID11 && echo "comprehensive_research: DONE" || echo "comprehensive_research: FAILED"
wait $PID12 && echo "ecom_arb_research: DONE" || echo "ecom_arb_research: FAILED"
wait $PID13 && echo "alpha_hunter: DONE" || echo "alpha_hunter: FAILED"
wait $PID14 && echo "faceless_army: DONE" || echo "faceless_army: FAILED"
wait $PID15 && echo "capital_genesis: DONE" || echo "capital_genesis: FAILED"

echo ""
echo "============================================"
echo "All loops finished: $(date)"
echo "Check logs in: $LOG_DIR"
echo "============================================"
