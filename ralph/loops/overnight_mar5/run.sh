#!/bin/bash
# Overnight Ralph Loop - Mar 5, 2026
# Run with: nohup bash ralph/loops/overnight_mar5/run.sh &

cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
unset CLAUDECODE
LOG="ralph/loops/overnight_mar5/run.log"

echo "=== OVERNIGHT RALPH LOOP STARTED $(date) ===" >> "$LOG"

for i in 1 2 3 4 5 6 7 8; do
  echo "" >> "$LOG"
  echo "=== ITERATION $i STARTED $(date) ===" >> "$LOG"

  cat ralph/loops/overnight_mar5/PROMPT.md | claude --dangerously-skip-permissions --print --mcp-config ralph/empty_mcp.json --strict-mcp-config >> "$LOG" 2>&1

  echo "=== ITERATION $i ENDED $(date) ===" >> "$LOG"
  sleep 5
done

echo "=== OVERNIGHT RALPH LOOP FINISHED $(date) ===" >> "$LOG"
