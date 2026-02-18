#!/bin/bash
# Capital Genesis Intelligence Loop
# Hedge fund-grade intelligence on capital stacking + revenue multiplication
# GUARDRAILS: No delete, no Bash, safe whitelist only

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
MAX_ITERATIONS=${1:-8}
LOOP_NAME=$(basename "$SCRIPT_DIR")

mkdir -p "$SCRIPT_DIR/.ralph" "$SCRIPT_DIR/output"
touch "$SCRIPT_DIR/.ralph/errors.log" "$SCRIPT_DIR/.ralph/activity.log"

echo "=========================================="
echo "Ralph Loop: $LOOP_NAME"
echo "Mode: SAFE (No Bash, No delete)"
echo "Max iterations: $MAX_ITERATIONS"
echo "Started: $(date)"
echo "=========================================="

# Safety rules prepended to every prompt
SAFETY_RULES="
## CRITICAL SAFETY RULES - ALWAYS FOLLOW

1. ONLY operate within: /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/
2. NEVER delete files (you don't have Bash access anyway)
3. ONLY append to CSV files - read first, then append new rows
4. READ existing files before modifying them
5. For browser: use mcp__Claude_in_Chrome__* tools only
6. Create new files freely, but don't overwrite without reading first

If blocked by safety constraints, output: <promise>BLOCKED: [reason]</promise>

---
"

for i in $(seq 1 $MAX_ITERATIONS); do
  echo ""
  echo "=== Iteration $i of $MAX_ITERATIONS ===" | tee -a "$SCRIPT_DIR/.ralph/activity.log"

  cd "$PROJECT_DIR"

  FULL_PROMPT="${SAFETY_RULES}
$(cat "$SCRIPT_DIR/prompt.md")"

  # SAFE WHITELIST - NO BASH TOOL
  OUTPUT=$(claude -p \
    --permission-mode dontAsk \
    --model sonnet \
    --allowedTools "Read,Grep,Glob,Write,Edit,WebSearch,WebFetch,TodoWrite,mcp__Claude_in_Chrome__computer,mcp__Claude_in_Chrome__read_page,mcp__Claude_in_Chrome__navigate,mcp__Claude_in_Chrome__find,mcp__Claude_in_Chrome__javascript_tool,mcp__Claude_in_Chrome__tabs_context_mcp,mcp__Claude_in_Chrome__tabs_create_mcp,mcp__Claude_in_Chrome__get_page_text" \
    << EOF
$FULL_PROMPT
EOF
  2>> "$SCRIPT_DIR/.ralph/errors.log") || true

  echo "$OUTPUT" >> "$SCRIPT_DIR/.ralph/activity.log"

  if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
    echo "All intelligence categories complete at iteration $i"
    exit 0
  fi

  if echo "$OUTPUT" | grep -q "<promise>BLOCKED"; then
    echo "Blocked by safety at iteration $i"
    exit 1
  fi

  echo "Iteration $i done. Sleeping 5s..."
  sleep 5
done

echo "Reached max iterations ($MAX_ITERATIONS)"
exit 1
