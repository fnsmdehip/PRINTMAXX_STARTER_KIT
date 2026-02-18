#!/bin/bash

# RETARDMAXX OVERNIGHT SPRINT LAUNCHER
# Runs ALL ralph loops in parallel for maximum overnight production
#
# Usage: ./ralph/run_overnight_sprint.sh
# Logs: ralph/logs/overnight_*.log
#
# This launches 8 loops simultaneously. Each loop runs on its own
# Claude instance with --dangerously-skip-permissions.
# Claude Max plan = unlimited, so go nuts.

PROJECT_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
LOG_DIR="$PROJECT_DIR/ralph/logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$LOG_DIR"

echo "============================================"
echo "  RETARDMAXX OVERNIGHT SPRINT"
echo "  $(date)"
echo "============================================"
echo ""
echo "Launching 8 ralph loops in parallel..."
echo "Logs: $LOG_DIR/overnight_*.log"
echo ""

# Loop 1: Social Branding (9 tasks, ~15 iterations)
echo "[1/8] Launching social_branding loop..."
nohup bash "$PROJECT_DIR/ralph/loops/social_branding/run.sh" \
    > "$LOG_DIR/overnight_social_branding_${TIMESTAMP}.log" 2>&1 &
echo "  PID: $!"

# Loop 2: Full PRINTMAXX Audit (27 tasks, ~50 iterations)
echo "[2/8] Launching full_printmaxx_audit loop..."
nohup bash "$PROJECT_DIR/ralph/loops/full_printmaxx_audit/run.sh" \
    > "$LOG_DIR/overnight_full_audit_${TIMESTAMP}.log" 2>&1 &
echo "  PID: $!"

# Loop 3: Digital Products (10 products, ~25 iterations)
echo "[3/8] Launching digital_products loop..."
nohup bash "$PROJECT_DIR/ralph/loops/digital_products/run.sh" \
    > "$LOG_DIR/overnight_digital_products_${TIMESTAMP}.log" 2>&1 &
echo "  PID: $!"

# Loop 4: Content Machine (15 batches, ~25 iterations)
echo "[4/8] Launching content_machine loop..."
nohup bash "$PROJECT_DIR/ralph/loops/content_machine/run.sh" \
    > "$LOG_DIR/overnight_content_machine_${TIMESTAMP}.log" 2>&1 &
echo "  PID: $!"

# Loop 5: Retardmaxx Execution (existing - 12 deliverables)
echo "[5/8] Launching retardmaxx_execution loop..."
nohup bash "$PROJECT_DIR/ralph/loops/retardmaxx_execution/run.sh" \
    > "$LOG_DIR/overnight_retardmaxx_exec_${TIMESTAMP}.log" 2>&1 &
echo "  PID: $!"

# Loop 6: Comprehensive Alpha Research (existing - scan sources)
echo "[6/8] Launching comprehensive_alpha_research loop..."
nohup bash "$PROJECT_DIR/ralph/loops/comprehensive_alpha_research/run.sh" \
    > "$LOG_DIR/overnight_alpha_research_${TIMESTAMP}.log" 2>&1 &
echo "  PID: $!"

# Loop 7: Synergy Package Builder (existing)
echo "[7/8] Launching synergy_package_builder loop..."
nohup bash "$PROJECT_DIR/ralph/loops/synergy_package_builder/run.sh" \
    > "$LOG_DIR/overnight_synergy_${TIMESTAMP}.log" 2>&1 &
echo "  PID: $!"

# Loop 8: Niche Meta Detection (existing)
echo "[8/8] Launching niche_meta_detection loop..."
nohup bash "$PROJECT_DIR/ralph/loops/niche_meta_detection/run.sh" \
    > "$LOG_DIR/overnight_niche_meta_${TIMESTAMP}.log" 2>&1 &
echo "  PID: $!"

echo ""
echo "============================================"
echo "  ALL 8 LOOPS LAUNCHED"
echo "============================================"
echo ""
echo "Monitor progress:"
echo "  tail -f $LOG_DIR/overnight_*_${TIMESTAMP}.log"
echo ""
echo "Check individual loops:"
echo "  tail -f $LOG_DIR/overnight_social_branding_${TIMESTAMP}.log"
echo "  tail -f $LOG_DIR/overnight_full_audit_${TIMESTAMP}.log"
echo "  tail -f $LOG_DIR/overnight_digital_products_${TIMESTAMP}.log"
echo "  tail -f $LOG_DIR/overnight_content_machine_${TIMESTAMP}.log"
echo "  tail -f $LOG_DIR/overnight_retardmaxx_exec_${TIMESTAMP}.log"
echo "  tail -f $LOG_DIR/overnight_alpha_research_${TIMESTAMP}.log"
echo "  tail -f $LOG_DIR/overnight_synergy_${TIMESTAMP}.log"
echo "  tail -f $LOG_DIR/overnight_niche_meta_${TIMESTAMP}.log"
echo ""
echo "Check progress files:"
echo "  cat ralph/loops/social_branding/.ralph/progress.md"
echo "  cat ralph/loops/full_printmaxx_audit/.ralph/progress.md"
echo "  cat ralph/loops/digital_products/.ralph/progress.md"
echo "  cat ralph/loops/content_machine/.ralph/progress.md"
echo ""
echo "Stop all loops:"
echo "  pkill -f 'ralph/loops'"
echo ""
echo "Go to sleep. Wake up to shipped artifacts."
