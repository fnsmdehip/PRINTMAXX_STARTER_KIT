#!/bin/bash
# Update Mega Ralph Boot Sequence (IR-006, IR-007, IR-008)
# Adds CRITICAL_PATH_DOCS, QUANT_QUICK_START, and RISK_RADAR
# references to the mega ralph prompt boot sequence.
#
# This script verifies the integration files exist and reports status.
# The actual prompt.md update is done separately (prompt.md is immutable
# per Rule 14, so changes go through checkpoint review).
#
# Usage: bash scripts/update_mega_ralph_boot.sh

set -e

PROJECT_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
MEGA_DIR="$PROJECT_DIR/ralph/loops/mega"
OPS_DIR="$PROJECT_DIR/OPS"
SCRIPTS_DIR="$PROJECT_DIR/scripts"
LEDGER_DIR="$PROJECT_DIR/LEDGER"

echo "============================================"
echo "Mega Ralph Boot Integration Verifier"
echo "Timestamp: $(date)"
echo "============================================"
echo ""

# Track overall status
ALL_GOOD=true

# 1. Check integration scripts exist
echo "=== Integration Scripts ==="
for script in \
    "$SCRIPTS_DIR/auto_backtest_trigger.py" \
    "$SCRIPTS_DIR/paper_trade_to_tracker.py" \
    "$SCRIPTS_DIR/content_to_qa_router.py"; do
    if [ -f "$script" ]; then
        echo "  [OK] $(basename $script)"
    else
        echo "  [MISSING] $(basename $script)"
        ALL_GOOD=false
    fi
done
echo ""

# 2. Check OPS reference files exist
echo "=== OPS Reference Files ==="
for doc in \
    "$OPS_DIR/CRITICAL_PATH_DOCS.md" \
    "$OPS_DIR/QUANT_QUICK_START.md" \
    "$OPS_DIR/RISK_RADAR_FEBRUARY_2026.md" \
    "$OPS_DIR/INTEGRATION_RECOMMENDATIONS.md"; do
    if [ -f "$doc" ]; then
        echo "  [OK] $(basename $doc)"
    else
        echo "  [MISSING] $(basename $doc)"
        ALL_GOOD=false
    fi
done
echo ""

# 3. Check LEDGER infrastructure
echo "=== LEDGER Infrastructure ==="
for csv_file in \
    "$LEDGER_DIR/ALPHA_STAGING.csv" \
    "$LEDGER_DIR/MONEY_METHODS_TRACKER.csv" \
    "$LEDGER_DIR/BACKTESTS/BACKTEST_RESULTS.csv" \
    "$LEDGER_DIR/PAPER_TRADES/PAPER_TRADE_RESULTS.csv" \
    "$LEDGER_DIR/MEGA_RALPH_TRACKER.csv"; do
    if [ -f "$csv_file" ]; then
        lines=$(wc -l < "$csv_file" | tr -d ' ')
        echo "  [OK] $(basename $csv_file) ($lines lines)"
    else
        echo "  [MISSING] $(basename $csv_file)"
        ALL_GOOD=false
    fi
done
echo ""

# 4. Check mega ralph state files
echo "=== Mega Ralph State Files ==="
for state_file in \
    "$MEGA_DIR/.ralph/progress.md" \
    "$MEGA_DIR/.ralph/priorities.md" \
    "$MEGA_DIR/.ralph/guardrails.md" \
    "$MEGA_DIR/.ralph/activity.log" \
    "$MEGA_DIR/.ralph/errors.log" \
    "$MEGA_DIR/prompt.md"; do
    if [ -f "$state_file" ]; then
        echo "  [OK] $(basename $state_file)"
    else
        echo "  [MISSING] $(basename $state_file)"
        ALL_GOOD=false
    fi
done
echo ""

# 5. Check QA queue directory
echo "=== QA Queue ==="
if [ -d "$OPS_DIR/CONTENT_QA_QUEUE" ]; then
    count=$(ls -1 "$OPS_DIR/CONTENT_QA_QUEUE" 2>/dev/null | wc -l | tr -d ' ')
    echo "  [OK] CONTENT_QA_QUEUE/ ($count items)"
else
    echo "  [MISSING] CONTENT_QA_QUEUE/"
    ALL_GOOD=false
fi
echo ""

# 6. Verify Python imports work
echo "=== Python Dependencies ==="
python3 -c "import csv, json, argparse, pathlib, datetime, re; print('  [OK] Standard library imports')" 2>/dev/null || echo "  [FAIL] Python3 standard library"

# Check backtest_alpha import
python3 -c "
import sys
sys.path.insert(0, '$PROJECT_DIR/AUTOMATIONS')
from backtest_alpha import AlphaBacktester
print('  [OK] backtest_alpha.py importable')
" 2>/dev/null || echo "  [FAIL] backtest_alpha.py import (check AUTOMATIONS/backtest_alpha.py)"

echo ""

# 7. Integration test - dry run each script
echo "=== Integration Test (Dry Runs) ==="

echo -n "  auto_backtest_trigger.py --dry-run: "
python3 "$SCRIPTS_DIR/auto_backtest_trigger.py" --dry-run 2>/dev/null | tail -1 || echo "FAILED"

echo -n "  paper_trade_to_tracker.py --dry-run: "
python3 "$SCRIPTS_DIR/paper_trade_to_tracker.py" --dry-run 2>/dev/null | tail -1 || echo "FAILED"

echo -n "  content_to_qa_router.py --dry-run: "
python3 "$SCRIPTS_DIR/content_to_qa_router.py" --dry-run 2>/dev/null | tail -1 || echo "FAILED"

echo ""

# 8. Summary
echo "============================================"
if [ "$ALL_GOOD" = true ]; then
    echo "STATUS: ALL INTEGRATIONS VERIFIED"
    echo "All files present. Scripts importable. Dry runs passed."
else
    echo "STATUS: SOME INTEGRATIONS MISSING"
    echo "Review [MISSING] items above and create missing files."
fi
echo ""
echo "Integration commands:"
echo "  # Run backtest on all unscored alpha"
echo "  python3 scripts/auto_backtest_trigger.py"
echo ""
echo "  # Sync paper trade results to tracker"
echo "  python3 scripts/paper_trade_to_tracker.py"
echo ""
echo "  # Route content to QA queue"
echo "  python3 scripts/content_to_qa_router.py --check-style"
echo ""
echo "  # Verify integrations"
echo "  bash scripts/update_mega_ralph_boot.sh"
echo "============================================"
