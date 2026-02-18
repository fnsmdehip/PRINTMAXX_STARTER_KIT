#!/bin/bash

# Comprehensive Alpha Research Ralph Loop

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROGRESS_DIR="$SCRIPT_DIR/.ralph"

mkdir -p "$PROGRESS_DIR"

if [ ! -f "$PROGRESS_DIR/progress.md" ]; then
    cat > "$PROGRESS_DIR/progress.md" <<'EOF'
# Comprehensive Alpha Research Progress

## Sources Scanned
(none yet)

## Alpha Entries Added
Count: 0

## Categories Covered
(none yet)

## Next Source
@pipelineabuser (S-tier)

## Status
RUNNING
EOF
fi

echo "Starting comprehensive alpha research loop..."
cd "$SCRIPT_DIR"

iteration=1
max_iterations=50

while [ $iteration -le $max_iterations ]; do
    echo "=== Iteration $iteration ==="

    if grep -q "Status.*COMPLETE" "$PROGRESS_DIR/progress.md"; then
        echo "Loop complete!"
        break
    fi

    cat prompt.md | claude --print --dangerously-skip-permissions --model claude-opus-4-6

    echo ""
    iteration=$((iteration + 1))
    sleep 2
done

echo "Alpha research loop finished after $iteration iterations"
