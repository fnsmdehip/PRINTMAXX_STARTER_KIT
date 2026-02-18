#!/bin/bash
# Faceless Army Research Loop Runner
# Usage: ./run.sh [max_iterations]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAX_ITERATIONS=${1:-10}
ITERATION=0

echo "Faceless Army Research Loop"
echo "Max iterations: $MAX_ITERATIONS"
echo "=========================="

while [ $ITERATION -lt $MAX_ITERATIONS ]; do
    ITERATION=$((ITERATION + 1))
    echo ""
    echo "--- Iteration $ITERATION of $MAX_ITERATIONS ---"
    echo "Started: $(date)"

    # Run claude with the prompt
    cat "$SCRIPT_DIR/prompt.md" | claude --dangerously-skip-permissions -p "Execute ONE iteration of this research loop. Pick the next category from progress.md, search for recent findings, append to relevant CSV, update progress.md, then exit." 2>&1

    EXIT_CODE=$?

    if [ $EXIT_CODE -ne 0 ]; then
        echo "Iteration $ITERATION failed with exit code $EXIT_CODE"
        echo "$(date): Iteration $ITERATION FAILED" >> "$SCRIPT_DIR/.ralph/errors.log"
    else
        echo "Iteration $ITERATION completed"
    fi

    # Small delay between iterations
    sleep 5
done

echo ""
echo "=========================="
echo "Faceless Army Loop Complete"
echo "Iterations: $ITERATION"
echo "Finished: $(date)"
