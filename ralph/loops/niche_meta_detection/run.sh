#!/bin/bash

# Niche Meta Detection Ralph Loop
# Runs iteratively until all niches scanned

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROGRESS_DIR="$SCRIPT_DIR/.ralph"

# Create .ralph directory if not exists
mkdir -p "$PROGRESS_DIR"

# Initialize progress.md if not exists
if [ ! -f "$PROGRESS_DIR/progress.md" ]; then
    cat > "$PROGRESS_DIR/progress.md" <<'EOF'
# Niche Meta Detection Progress

## Niches Scanned
(none yet)

## Metas Detected
Count: 0

## Pattern Matches
- Ghibli pattern: 0
- Routine pattern: 0
- Tool arbitrage pattern: 0
- Controversy pattern: 0

## Next Niche to Scan
N001 (Faith)

## Status
RUNNING
EOF
fi

# Initialize guardrails.md if not exists
if [ ! -f "$PROGRESS_DIR/guardrails.md" ]; then
    cat > "$PROGRESS_DIR/guardrails.md" <<'EOF'
# Guardrails

## Learned Constraints
(none yet)

## Blocked Patterns
(none yet)
EOF
fi

echo "Starting niche meta detection loop..."
echo "Working directory: $SCRIPT_DIR"
echo "Progress: $PROGRESS_DIR/progress.md"
echo ""

# Change to script directory so file operations work correctly
cd "$SCRIPT_DIR"

# Run loop (max 50 iterations)
iteration=1
max_iterations=50

while [ $iteration -le $max_iterations ]; do
    echo "=== Iteration $iteration ==="

    # Check if we're done
    if grep -q "Status.*COMPLETE" "$PROGRESS_DIR/progress.md"; then
        echo "Loop complete! All niches scanned."
        break
    fi

    # Run the agent with the static prompt (simple ralph pattern)
    cat prompt.md | claude --print --dangerously-skip-permissions --model claude-opus-4-6

    echo ""
    iteration=$((iteration + 1))
    sleep 2
done

echo "Niche meta detection loop finished after $iteration iterations"
