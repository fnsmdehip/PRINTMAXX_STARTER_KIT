#!/bin/bash
# Safe Ralph Loop Runner
# GUARDRAILS:
# - Only works in PRINTMAXX folder
# - NO delete operations
# - NO destructive bash commands
# - Browser only via MCP tools

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT"
MAX_ITERATIONS=${1:-10}
LOOP_NAME=$(basename "$SCRIPT_DIR")

mkdir -p "$SCRIPT_DIR/.ralph" "$SCRIPT_DIR/output"
touch "$SCRIPT_DIR/.ralph/errors.log" "$SCRIPT_DIR/.ralph/activity.log"

echo "=========================================="
echo "Ralph Loop: $LOOP_NAME"
echo "Mode: SAFE (No delete, project-only)"
echo "Max iterations: $MAX_ITERATIONS"
echo "Started: $(date)"
echo "=========================================="
echo ""

# Safety prompt prepended to all requests
SAFETY_PROMPT="
CRITICAL SAFETY RULES - MUST FOLLOW:
1. ONLY operate within: /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/
2. NEVER delete files or directories (no rm, no unlink, no delete operations)
3. NEVER use destructive bash commands (rm, mv to outside project, chmod, sudo)
4. ONLY append to existing CSV files, never overwrite
5. For browser automation, ONLY use MCP tools: mcp__Claude_in_Chrome__*
6. If a file exists, READ IT FIRST before any modifications
7. Create new files or append - NEVER replace existing content without reading

If you cannot complete a task safely within these rules, output:
<promise>BLOCKED: [reason]</promise>

Now proceed with the task:
"

for i in $(seq 1 $MAX_ITERATIONS); do
  echo ""
  echo "=== Iteration $i of $MAX_ITERATIONS ===" | tee -a "$SCRIPT_DIR/.ralph/activity.log"

  cd "$PROJECT_DIR"
  
  # Combine safety prompt with task prompt
  FULL_PROMPT="${SAFETY_PROMPT}
$(cat "$SCRIPT_DIR/prompt.md")"
  
  # SAFE TOOL WHITELIST:
  # - Read/Grep/Glob: Read-only file operations
  # - Write/Edit: Can create/modify (prompt rules prevent delete)
  # - WebSearch/WebFetch: Web research
  # - TodoWrite: Task tracking
  # - MCP browser tools: Chrome automation
  # NO Bash tool = no shell commands = no rm/mv/etc
  
  OUTPUT=$(claude -p \
    --model sonnet \
    --allowedTools "Read,Grep,Glob,Write,Edit,WebSearch,WebFetch,TodoWrite,mcp__Claude_in_Chrome__computer,mcp__Claude_in_Chrome__read_page,mcp__Claude_in_Chrome__navigate,mcp__Claude_in_Chrome__find,mcp__Claude_in_Chrome__javascript_tool,mcp__Claude_in_Chrome__tabs_context_mcp,mcp__Claude_in_Chrome__tabs_create_mcp" \
    << EOF
$FULL_PROMPT
EOF
  2>> "$SCRIPT_DIR/.ralph/errors.log") || true

  echo "$OUTPUT" >> "$SCRIPT_DIR/.ralph/activity.log"

  if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
    echo ""
    echo "All tasks complete at iteration $i"
    exit 0
  fi
  
  if echo "$OUTPUT" | grep -q "<promise>BLOCKED"; then
    echo ""
    echo "Loop blocked by safety rules at iteration $i"
    echo "$OUTPUT" | grep "<promise>BLOCKED"
    exit 1
  fi

  echo "Iteration $i done. Sleeping 5s..."
  sleep 5
done

echo ""
echo "Reached max iterations ($MAX_ITERATIONS)"
exit 1
