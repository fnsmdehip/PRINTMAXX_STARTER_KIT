#!/bin/bash
# Content Machine Ralph Loop - Overnight
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
unset CLAUDECODE
LOG="ralph/loops/content_machine/overnight.log"

echo "=== CONTENT MACHINE STARTED $(date) ===" >> "$LOG"

for i in 1 2 3 4 5; do
  echo "" >> "$LOG"
  echo "=== ITERATION $i STARTED $(date) ===" >> "$LOG"
  cat ralph/loops/content_machine/PROMPT.md | claude --dangerously-skip-permissions --print --mcp-config ralph/empty_mcp.json --strict-mcp-config >> "$LOG" 2>&1
  echo "=== ITERATION $i ENDED $(date) ===" >> "$LOG"
  sleep 10
done

echo "=== CONTENT MACHINE FINISHED $(date) ===" >> "$LOG"
