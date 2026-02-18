#!/bin/bash
# MASTER OPS BUILD LOOP — RALPH WIGGUM + AGENT SWARMS
# Each iteration: read state → pick task → spawn agent swarm → write state → exit
# Memory = filesystem. Fresh context each iteration.

cd "$(dirname "$0")"
ROOT="$(cd ../../.. && pwd)"
MAX_ITERS="${1:-10}"
LOG="$ROOT/ralph/logs/master_ops_build_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$ROOT/ralph/logs"

echo "=== MASTER OPS BUILD LOOP ===" | tee "$LOG"
echo "Max iterations: $MAX_ITERS" | tee -a "$LOG"
echo "Started: $(date)" | tee -a "$LOG"

for i in $(seq 1 $MAX_ITERS); do
  echo "" | tee -a "$LOG"
  echo "--- Iteration $i / $MAX_ITERS — $(date) ---" | tee -a "$LOG"

  # Check if all tasks done
  if grep -q '"passes": false' prd.json 2>/dev/null; then
    echo "Tasks remaining. Executing..." | tee -a "$LOG"
  else
    echo "ALL TASKS COMPLETE. Exiting loop." | tee -a "$LOG"
    break
  fi

  # Execute iteration
  cat PROMPT.md | claude --dangerously-skip-permissions --print 2>&1 | tee -a "$LOG"

  echo "--- Iteration $i complete — $(date) ---" | tee -a "$LOG"
  sleep 3
done

echo "" | tee -a "$LOG"
echo "=== LOOP COMPLETE ===" | tee -a "$LOG"
echo "Ended: $(date)" | tee -a "$LOG"
echo "Log: $LOG"
