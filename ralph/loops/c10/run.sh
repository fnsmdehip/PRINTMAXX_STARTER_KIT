#!/bin/bash
# Ralph Loop Runner: Meme Page Engagement Farm (C10)
# Generated: 2026-02-12T07:52:15.041137
#
# Canonical Ralph Wiggum pattern:
# - Fresh context every iteration
# - State lives in files (prd.json, progress.txt)
# - One task per iteration
# - Quality gates before marking done
# - Backpressure on quality drops

LOOP_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph/loops/c10"
PROJECT_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
MAX_ITERATIONS=${1:-20}
SLEEP_BETWEEN=${2:-5}

cd "$PROJECT_DIR"
# SAFETY: Load guardrails wrapper
source "$PROJECT_DIR/AUTOMATIONS/guardrails_wrapper.sh"


echo "=== Ralph Loop: Meme Page Engagement Farm (C10) ==="
echo "Max iterations: $MAX_ITERATIONS"
echo "Sleep between: ${SLEEP_BETWEEN}s"
echo ""

iteration=1

while [ $iteration -le $MAX_ITERATIONS ]; do
    echo "--- Iteration $iteration / $MAX_ITERATIONS ---"
    echo "$(date +%Y-%m-%dT%H:%M:%S) Starting iteration $iteration" >> "$LOOP_DIR/progress.txt"

    # Check if all tasks complete
    if python3 -c "
import json
with open('$LOOP_DIR/prd.json') as f:
    prd = json.load(f)
if all(s['passes'] for s in prd['stories']):
    print('COMPLETE')
    exit(0)
exit(1)
" 2>/dev/null; then
        echo "All tasks complete!"
        break
    fi

    # Run one iteration with fresh context
    cat "$LOOP_DIR/prompt.md" | claude --print --dangerously-skip-permissions

    echo ""
    echo "Iteration $iteration complete. Sleeping ${SLEEP_BETWEEN}s..."
    iteration=$((iteration + 1))
    sleep "$SLEEP_BETWEEN"
done

echo ""
echo "=== Loop finished after $((iteration - 1)) iterations ==="
echo "$(date +%Y-%m-%dT%H:%M:%S) Loop finished after $((iteration - 1)) iterations" >> "$LOOP_DIR/progress.txt"
