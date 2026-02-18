#!/bin/bash

# PRINTMAXX Parallel Ralph Loops Launcher
# Runs all 5 ralph loops simultaneously in background

PROJECT_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
LOOPS_DIR="$PROJECT_DIR/ralph/loops"
LOGS_DIR="$PROJECT_DIR/ralph/logs"

# Ensure logs directory exists
mkdir -p "$LOGS_DIR"

echo "========================================"
echo "PRINTMAXX Parallel Ralph Loops Launcher"
echo "========================================"
echo ""
echo "Launching 5 ralph loops in parallel:"
echo "1. niche_meta_detection"
echo "2. comprehensive_alpha_research"
echo "3. synergy_package_builder"
echo "4. retardmaxx_execution"
echo "5. meme_coin_backtest"
echo ""

# Array to store PIDs
declare -a PIDS

# Function to launch a loop
launch_loop() {
    local loop_name=$1
    local loop_dir="$LOOPS_DIR/$loop_name"

    if [ ! -f "$loop_dir/run.sh" ]; then
        echo "ERROR: $loop_name/run.sh not found"
        return 1
    fi

    echo "Launching $loop_name..."
    cd "$loop_dir"
    nohup ./run.sh > "$LOGS_DIR/${loop_name}_master_$(date +%Y%m%d_%H%M%S).log" 2>&1 &
    local pid=$!
    PIDS+=($pid)
    echo "  → $loop_name started (PID: $pid)"
    cd "$PROJECT_DIR"
}

# Launch all loops
launch_loop "niche_meta_detection"
launch_loop "comprehensive_alpha_research"
launch_loop "synergy_package_builder"
launch_loop "retardmaxx_execution"
launch_loop "meme_coin_backtest"

echo ""
echo "========================================"
echo "All loops launched!"
echo "========================================"
echo ""
echo "PIDs: ${PIDS[@]}"
echo ""
echo "Monitor progress:"
echo "  tail -f $LOGS_DIR/niche_meta_detection_*.log"
echo "  tail -f $LOGS_DIR/comprehensive_alpha_research_*.log"
echo "  tail -f $LOGS_DIR/synergy_package_builder_*.log"
echo "  tail -f $LOGS_DIR/retardmaxx_execution_*.log"
echo "  tail -f $LOGS_DIR/meme_coin_backtest_*.log"
echo ""
echo "Check loop status:"
echo "  ps aux | grep 'run.sh'"
echo ""
echo "Stop all loops:"
echo "  kill ${PIDS[@]}"
echo ""
echo "Individual loop progress files:"
echo "  cat $LOOPS_DIR/niche_meta_detection/.ralph/progress.md"
echo "  cat $LOOPS_DIR/comprehensive_alpha_research/.ralph/progress.md"
echo "  cat $LOOPS_DIR/synergy_package_builder/.ralph/progress.md"
echo "  cat $LOOPS_DIR/retardmaxx_execution/.ralph/progress.md"
echo "  cat $LOOPS_DIR/meme_coin_backtest/.ralph/progress.md"
echo ""
echo "Loops will run until completion (max 50 iterations each)"
echo "or until you kill them manually."
echo ""
