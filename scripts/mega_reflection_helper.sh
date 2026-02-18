#!/bin/bash
# MEGA RALPH LOOP - Reflection Phase Helper Script
# Runs all reflection tasks in sequence: backtest alpha, route content, update priorities

set -e  # Exit on error

PROJECT_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
LOG_FILE="$PROJECT_DIR/ralph/loops/mega/.ralph/reflection.log"

# Ensure we're in the right directory
cd "$PROJECT_DIR"

echo "========================================" | tee -a "$LOG_FILE"
echo "MEGA RALPH REFLECTION HELPER" | tee -a "$LOG_FILE"
echo "Started: $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# Step 1: Backtest pending alpha
echo "" | tee -a "$LOG_FILE"
echo "[1/3] Running backtest on PENDING_REVIEW alpha..." | tee -a "$LOG_FILE"
if python3 AUTOMATIONS/backtest_alpha.py --pending >> "$LOG_FILE" 2>&1; then
    echo "✅ Backtest complete" | tee -a "$LOG_FILE"
else
    echo "⚠️  Backtest failed or no pending entries" | tee -a "$LOG_FILE"
fi

# Step 2: Route content to QA queue
echo "" | tee -a "$LOG_FILE"
echo "[2/3] Routing generated content to QA queue..." | tee -a "$LOG_FILE"
if [ -f "scripts/content_to_qa_router.py" ]; then
    if python3 scripts/content_to_qa_router.py >> "$LOG_FILE" 2>&1; then
        echo "✅ Content routing complete" | tee -a "$LOG_FILE"
    else
        echo "⚠️  Content routing failed or no new content" | tee -a "$LOG_FILE"
    fi
else
    echo "⚠️  Content router script not found (scripts/content_to_qa_router.py)" | tee -a "$LOG_FILE"
    echo "   Creating manual placeholder in checkpoints/" | tee -a "$LOG_FILE"
    echo "Content routing skipped - manual review needed" > "$PROJECT_DIR/ralph/loops/mega/checkpoints/PENDING_CONTENT_QA_ROUTING.md"
fi

# Step 3: Update priorities based on backtest results
echo "" | tee -a "$LOG_FILE"
echo "[3/3] Updating priorities.md based on backtest scores..." | tee -a "$LOG_FILE"

PRIORITIES_FILE="$PROJECT_DIR/ralph/loops/mega/.ralph/priorities.md"
BACKTEST_RESULTS="$PROJECT_DIR/LEDGER/BACKTESTS/BACKTEST_RESULTS.csv"
PRIORITY_QUEUE="$PROJECT_DIR/LEDGER/BACKTEST_PRIORITY_QUEUE.csv"

if [ -f "$PRIORITY_QUEUE" ]; then
    # Count entries by decision
    SCALE_COUNT=$(grep -c "SCALE" "$PRIORITY_QUEUE" 2>/dev/null || echo 0)
    PAPER_TRADE_COUNT=$(grep -c "PAPER_TRADE" "$PRIORITY_QUEUE" 2>/dev/null || echo 0)
    KILL_COUNT=$(grep -c "KILL" "$PRIORITY_QUEUE" 2>/dev/null || echo 0)

    echo "   SCALE-scored alpha: $SCALE_COUNT entries" | tee -a "$LOG_FILE"
    echo "   PAPER_TRADE-scored alpha: $PAPER_TRADE_COUNT entries" | tee -a "$LOG_FILE"
    echo "   KILL-scored alpha: $KILL_COUNT entries" | tee -a "$LOG_FILE"

    # Append note to priorities.md
    {
        echo ""
        echo "## Backtest Update ($(date +%Y-%m-%d))"
        echo ""
        echo "### SCALE Priority (Deploy Immediately)"
        echo "- $SCALE_COUNT alpha entries scored >= 70"
        echo "- Check LEDGER/BACKTEST_PRIORITY_QUEUE.csv for alpha IDs"
        echo ""
        echo "### PAPER_TRADE Queue"
        echo "- $PAPER_TRADE_COUNT alpha entries scored 50-69"
        echo "- Start with \$50-100, 14 day test"
        echo ""
        echo "### KILLED (Deprioritized)"
        echo "- $KILL_COUNT alpha entries scored < 50"
        echo "- Do not allocate resources"
        echo ""
    } >> "$PRIORITIES_FILE"

    echo "✅ Priorities updated" | tee -a "$LOG_FILE"
else
    echo "⚠️  No priority queue found ($PRIORITY_QUEUE)" | tee -a "$LOG_FILE"
    echo "   Backtest may have found no entries or failed" | tee -a "$LOG_FILE"
fi

# Summary
echo "" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "REFLECTION HELPER COMPLETE" | tee -a "$LOG_FILE"
echo "Finished: $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "Next steps:" | tee -a "$LOG_FILE"
echo "1. Review LEDGER/BACKTEST_PRIORITY_QUEUE.csv for SCALE-scored alpha" | tee -a "$LOG_FILE"
echo "2. Check OPS/CONTENT_QA_QUEUE/ for content needing review" | tee -a "$LOG_FILE"
echo "3. Continue to CONTENT_GENERATION phase" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

exit 0
