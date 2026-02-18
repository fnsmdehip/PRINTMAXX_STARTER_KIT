#!/bin/bash
# MEGA RALPH LOOP - Unified Automation System
# Replaces all 17 individual ralph loops with ONE orchestrated loop
# Usage: ./run.sh [days] (default: 3 days = 63 iterations)
#
# GUARDRAILS:
# - Only works in PRINTMAXX folder
# - NO delete operations (Bash tool disabled)
# - NO destructive commands
# - Browser only via MCP tools
# - FTC compliant, human-in-loop for publishing
#
# Day Cycle (21 iterations):
#   Iterations 1-3:   DAILY_RESEARCH    (alpha scanning, source monitoring, web research)
#   Iteration 4:      REFLECTION        (synthesize findings, update priorities, cross-pollinate)
#   Iterations 5-10:  CONTENT_GENERATION (social posts, longtail pages, email sequences)
#   Iterations 11-15: EXECUTION         (app builds, landing pages, automation scripts)
#   Iterations 16-20: INTELLIGENCE      (competitor intel, platform changes, tool alpha)
#   Iteration 21:     CHECKPOINT        (human review items, progress summary, next day plan)
#
# Completion Signals:
#   <promise>DAY_COMPLETE</promise>   - Skip remaining iterations in current day
#   <promise>BLOCKED</promise>        - Log block, continue to next iteration
#   <promise>COMPLETE</promise>       - All work done, exit loop entirely

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
DAYS=${1:-3}
ITERATIONS_PER_DAY=21
MAX_ITERATIONS=$((DAYS * ITERATIONS_PER_DAY))
LOOP_NAME="mega"
SLEEP_BETWEEN=10
MODEL="opus"  # MAXIMUM QUALITY - we have token budget

# Ensure all directories exist
mkdir -p "$SCRIPT_DIR/.ralph" "$SCRIPT_DIR/output" "$SCRIPT_DIR/checkpoints"
touch "$SCRIPT_DIR/.ralph/errors.log" "$SCRIPT_DIR/.ralph/activity.log"

echo "============================================"
echo "MEGA RALPH LOOP - Unified Automation"
echo "Mode: AUTONOMOUS OPUS (Max Quality)"
echo "Model: $MODEL (best available)"
echo "Days planned: $DAYS"
echo "Iterations per day: $ITERATIONS_PER_DAY"
echo "Total max iterations: $MAX_ITERATIONS"
echo "Sleep between iterations: ${SLEEP_BETWEEN}s"
echo "Guardrails: Project folder only, Chrome MCP only, No Bash"
echo "Started: $(date)"
echo "============================================"
echo ""

# Log start to activity log
echo "" >> "$SCRIPT_DIR/.ralph/activity.log"
echo "============================================" >> "$SCRIPT_DIR/.ralph/activity.log"
echo "MEGA RALPH LOOP STARTED: $(date)" >> "$SCRIPT_DIR/.ralph/activity.log"
echo "Days: $DAYS | Max Iterations: $MAX_ITERATIONS" >> "$SCRIPT_DIR/.ralph/activity.log"
echo "============================================" >> "$SCRIPT_DIR/.ralph/activity.log"

# Safety rules prepended to every prompt
SAFETY_RULES="
## CRITICAL SAFETY RULES - AUTONOMOUS OVERNIGHT MODE

1. ONLY operate within: /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/
2. NEVER delete files (you don't have Bash access anyway)
3. ONLY append to CSV files - read first, then append new rows
4. READ existing files before modifying them
5. For browser scraping: use mcp__Claude_in_Chrome__* tools ONLY (Chrome MCP)
6. Create new files freely, but don't overwrite without reading first
7. Follow .claude/rules/copy-style.md for ALL content generation
8. FTC compliant always - disclosures, no fake testimonials
9. Human-in-loop items go to checkpoints/ folder (DO NOT WAIT FOR APPROVAL - just flag and continue)
10. Update LEDGER/MEGA_RALPH_TRACKER.csv after EVERY task
11. Deduplicate before appending to any CSV (grep for existing entries)
12. Log what you did to ralph/loops/mega/.ralph/progress.md
13. AUTONOMOUS MODE: Run overnight without human intervention. Flag items in checkpoints/, don't wait.
14. AGGRESSIVE: Use full token budget. Deep research. Comprehensive outputs. No basic thinking.

If blocked by safety constraints, output: <promise>BLOCKED: [reason]</promise>
When all tasks for the current day are done: <promise>DAY_COMPLETE</promise>
When ALL work across all days is done: <promise>COMPLETE</promise>

---
"

# Track stats
TOTAL_BLOCKED=0
TOTAL_COMPLETED=0
DAYS_COMPLETED=0

# Main loop - use while instead of for to support day-skipping
i=1
while [ $i -le $MAX_ITERATIONS ]; do
  ITERATION_IN_DAY=$(( ((i - 1) % ITERATIONS_PER_DAY) + 1 ))
  DAY=$(( ((i - 1) / ITERATIONS_PER_DAY) + 1 ))

  # Determine current phase based on iteration within day
  if [ $ITERATION_IN_DAY -le 3 ]; then
    PHASE="DAILY_RESEARCH"
    PHASE_DESC="Alpha scanning, HIGH_SIGNAL_SOURCES monitoring, web research across all 10 categories"
  elif [ $ITERATION_IN_DAY -eq 4 ]; then
    PHASE="REFLECTION"
    PHASE_DESC="Synthesize research findings, update CROSS_POLLINATION_MATRIX, reprioritize GTM_OPTIMIZATION_PRIORITIES, identify highest-ROI opportunities"
  elif [ $ITERATION_IN_DAY -le 10 ]; then
    PHASE="CONTENT_GENERATION"
    PHASE_DESC="Generate social posts, longtail SEO pages, email sequences, landing copy, niche account content"
  elif [ $ITERATION_IN_DAY -le 15 ]; then
    PHASE="EXECUTION"
    PHASE_DESC="App builds, landing pages, automation scripts, cold email infrastructure, technical implementation"
  elif [ $ITERATION_IN_DAY -le 20 ]; then
    PHASE="INTELLIGENCE"
    PHASE_DESC="Competitor monitoring, platform algorithm changes, tool alpha discovery, edge growth tactics audit"
  else
    PHASE="CHECKPOINT"
    PHASE_DESC="Summarize day progress, create human review items in checkpoints/, plan next day priorities"
  fi

  echo ""
  echo "=== Day $DAY | Iteration $ITERATION_IN_DAY/21 (Global: $i/$MAX_ITERATIONS) | Phase: $PHASE ===" | tee -a "$SCRIPT_DIR/.ralph/activity.log"
  echo "Timestamp: $(date)" | tee -a "$SCRIPT_DIR/.ralph/activity.log"
  echo "Phase: $PHASE_DESC" | tee -a "$SCRIPT_DIR/.ralph/activity.log"

  cd "$PROJECT_DIR"

  # Inject current phase and context into prompt
  PHASE_HINT="
## CURRENT ITERATION CONTEXT
- Day Cycle: $DAY of $DAYS
- Iteration in Day: $ITERATION_IN_DAY of 21
- Global Iteration: $i of $MAX_ITERATIONS
- CURRENT PHASE: $PHASE
- Phase Description: $PHASE_DESC
- Iterations blocked so far: $TOTAL_BLOCKED
- Days completed so far: $DAYS_COMPLETED

Execute ONE focused task from the $PHASE phase.
Read .ralph/progress.md first to avoid repeating work.
After completing your task, update .ralph/progress.md with what you did.

---
"

  FULL_PROMPT="${SAFETY_RULES}${PHASE_HINT}
$(cat "$SCRIPT_DIR/prompt.md")"

  # AUTONOMOUS MODE - NO BASH TOOL, CHROME MCP FOR SCRAPING, OPUS FOR MAX QUALITY
  # --permission-mode dontAsk auto-approves all operations so it runs unattended
  OUTPUT=$(claude -p \
    --model $MODEL \
    --allowedTools "Read,Grep,Glob,Write,Edit,WebSearch,WebFetch,TodoWrite,mcp__Claude_in_Chrome__computer,mcp__Claude_in_Chrome__read_page,mcp__Claude_in_Chrome__navigate,mcp__Claude_in_Chrome__find,mcp__Claude_in_Chrome__javascript_tool,mcp__Claude_in_Chrome__tabs_context_mcp,mcp__Claude_in_Chrome__tabs_create_mcp,mcp__Claude_in_Chrome__get_page_text" \
    --permission-mode dontAsk \
    << EOF
$FULL_PROMPT
EOF
  2>> "$SCRIPT_DIR/.ralph/errors.log") || true

  # Log output with separator
  echo "" >> "$SCRIPT_DIR/.ralph/activity.log"
  echo "--- OUTPUT Day $DAY Iter $ITERATION_IN_DAY ($PHASE) ---" >> "$SCRIPT_DIR/.ralph/activity.log"
  echo "$OUTPUT" >> "$SCRIPT_DIR/.ralph/activity.log"
  echo "--- END Day $DAY Iter $ITERATION_IN_DAY ---" >> "$SCRIPT_DIR/.ralph/activity.log"

  # Track token usage estimate (rough: 4 chars per token)
  OUTPUT_LEN=${#OUTPUT}
  TOKEN_EST=$((OUTPUT_LEN / 4))
  echo "Token estimate (output): ~$TOKEN_EST" >> "$SCRIPT_DIR/.ralph/activity.log"

  # Check for completion signals
  if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
    echo ""
    echo "ALL TASKS COMPLETE at Day $DAY, Iteration $ITERATION_IN_DAY (Global: $i)" | tee -a "$SCRIPT_DIR/.ralph/activity.log"
    echo "COMPLETE at $(date)" >> "$SCRIPT_DIR/.ralph/activity.log"
    echo ""
    echo "============================================"
    echo "MEGA RALPH LOOP - COMPLETED EARLY"
    echo "Days used: $DAY of $DAYS"
    echo "Total iterations used: $i of $MAX_ITERATIONS"
    echo "Blocked iterations: $TOTAL_BLOCKED"
    echo "Finished: $(date)"
    echo "============================================"
    exit 0
  fi

  if echo "$OUTPUT" | grep -q "<promise>DAY_COMPLETE</promise>"; then
    DAYS_COMPLETED=$((DAYS_COMPLETED + 1))
    echo "Day $DAY complete at iteration $ITERATION_IN_DAY" | tee -a "$SCRIPT_DIR/.ralph/activity.log"
    echo "DAY $DAY COMPLETE at $(date)" >> "$SCRIPT_DIR/.ralph/activity.log"
    # Jump to next day by advancing i to the start of next day
    NEXT_DAY_START=$((DAY * ITERATIONS_PER_DAY + 1))
    REMAINING=$((NEXT_DAY_START - i - 1))
    if [ $REMAINING -gt 0 ]; then
      echo "Skipping $REMAINING remaining iterations in day $DAY"
      i=$NEXT_DAY_START
      echo "Sleeping ${SLEEP_BETWEEN}s before starting day $((DAY + 1))..."
      sleep $SLEEP_BETWEEN
      continue
    fi
  fi

  if echo "$OUTPUT" | grep -q "<promise>BLOCKED"; then
    TOTAL_BLOCKED=$((TOTAL_BLOCKED + 1))
    BLOCK_REASON=$(echo "$OUTPUT" | grep -o "<promise>BLOCKED:.*</promise>" | head -1)
    echo "BLOCKED at Day $DAY, Iteration $ITERATION_IN_DAY: $BLOCK_REASON" | tee -a "$SCRIPT_DIR/.ralph/activity.log"
    echo "BLOCKED: $BLOCK_REASON at $(date)" >> "$SCRIPT_DIR/.ralph/errors.log"
    # Don't exit on block - continue to next iteration
    echo "Continuing to next iteration..."
  else
    TOTAL_COMPLETED=$((TOTAL_COMPLETED + 1))
  fi

  # Track day completion at end of day cycle
  if [ $ITERATION_IN_DAY -eq $ITERATIONS_PER_DAY ]; then
    DAYS_COMPLETED=$((DAYS_COMPLETED + 1))
    echo "Day $DAY cycle finished naturally" | tee -a "$SCRIPT_DIR/.ralph/activity.log"
  fi

  echo "Day $DAY, Iteration $ITERATION_IN_DAY ($PHASE) done. Sleeping ${SLEEP_BETWEEN}s..."
  sleep $SLEEP_BETWEEN

  i=$((i + 1))
done

echo ""
echo "============================================"
echo "MEGA RALPH LOOP - FINISHED"
echo "Days completed: $DAYS_COMPLETED of $DAYS"
echo "Total iterations run: $MAX_ITERATIONS"
echo "Successful iterations: $TOTAL_COMPLETED"
echo "Blocked iterations: $TOTAL_BLOCKED"
echo "Finished: $(date)"
echo "============================================"
echo ""
echo "Review:"
echo "  Logs:        $SCRIPT_DIR/.ralph/activity.log"
echo "  Errors:      $SCRIPT_DIR/.ralph/errors.log"
echo "  Progress:    $SCRIPT_DIR/.ralph/progress.md"
echo "  Checkpoints: $SCRIPT_DIR/checkpoints/"
echo "  Tracker:     $PROJECT_DIR/LEDGER/MEGA_RALPH_TRACKER.csv"
echo "  Output:      $SCRIPT_DIR/output/"
