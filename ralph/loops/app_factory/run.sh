#!/bin/bash
# APP FACTORY LOOP — RALPH WIGGUM + AGENT SWARMS
cd "$(dirname "$0")"
ROOT="$(cd ../../.. && pwd)"
MAX_ITERS="${1:-5}"
LOG="$ROOT/ralph/logs/app_factory_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$ROOT/ralph/logs"

echo "=== APP FACTORY LOOP ===" | tee "$LOG"
echo "Max iterations: $MAX_ITERS" | tee -a "$LOG"
echo "Started: $(date)" | tee -a "$LOG"

for i in $(seq 1 $MAX_ITERS); do
  echo "" | tee -a "$LOG"
  echo "--- Iteration $i / $MAX_ITERS — $(date) ---" | tee -a "$LOG"

  if grep -q '"passes": false' prd.json 2>/dev/null; then
    echo "Tasks remaining. Building app..." | tee -a "$LOG"
  else
    echo "ALL APPS BUILT. Exiting loop." | tee -a "$LOG"
    break
  fi

  cat PROMPT.md | claude --dangerously-skip-permissions --print 2>&1 | tee -a "$LOG"
  echo "--- Iteration $i complete — $(date) ---" | tee -a "$LOG"
  sleep 3
done

echo "=== LOOP COMPLETE ===" | tee -a "$LOG"
echo "Ended: $(date)" | tee -a "$LOG"
