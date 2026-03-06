#!/bin/bash
# Full Spreadsheet Buildout Ralph Loop
# Runs through ALL 181 operations in the master ops spreadsheet
# Launch: nohup bash ralph/loops/spreadsheet_buildout/run.sh &

cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt

# CRITICAL: Unset CLAUDECODE env var to allow nested sessions
unset CLAUDECODE

LOG="ralph/loops/spreadsheet_buildout/run.log"
OUTPUT="ralph/loops/spreadsheet_buildout/output"

mkdir -p "$OUTPUT"

echo "=== FULL SPREADSHEET BUILDOUT STARTED $(date) ===" >> "$LOG"
echo "Working dir: $(pwd)" >> "$LOG"

# Run 41 iterations (one per task batch)
for i in $(seq 1 41); do
  echo "" >> "$LOG"
  echo "========================================" >> "$LOG"
  echo "=== ITERATION $i / 41 STARTED $(date) ===" >> "$LOG"
  echo "========================================" >> "$LOG"

  # Combine the prompt with progress tracking instruction
  PROMPT="$(cat ralph/loops/spreadsheet_buildout/PROMPT.md)

IMPORTANT SAFETY:
- ALL file writes MUST be within /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/
- Do NOT touch files outside this directory
- Do NOT delete any existing files
- Create new files ONLY in ralph/loops/spreadsheet_buildout/output/
- Follow .claude/rules/guardrails.md strictly

CURRENT PROGRESS:
$(cat ralph/loops/spreadsheet_buildout/progress.md)

DO THE NEXT UNCOMPLETED TASK. Write all output files. Then update progress.md marking the task as done with [x]. Exit cleanly."

  echo "$PROMPT" | claude --dangerously-skip-permissions --print --mcp-config ralph/empty_mcp.json --strict-mcp-config >> "$LOG" 2>&1

  echo "=== ITERATION $i / 41 ENDED $(date) ===" >> "$LOG"

  # Brief pause between iterations
  sleep 10
done

echo "=== FULL SPREADSHEET BUILDOUT FINISHED $(date) ===" >> "$LOG"
