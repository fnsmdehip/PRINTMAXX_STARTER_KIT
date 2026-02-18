#!/bin/bash

# Digital Products Generation Ralph Loop

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROGRESS_DIR="$SCRIPT_DIR/.ralph"
PROJECT_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"

mkdir -p "$PROGRESS_DIR"
mkdir -p "$PROJECT_DIR/PRODUCTS/listings"

if [ ! -f "$PROGRESS_DIR/progress.md" ]; then
    cat > "$PROGRESS_DIR/progress.md" <<'EOF'
# Digital Products Progress

## Products
- [ ] 1. Funnel Teardown Guide ($7)
- [ ] 2. Cold Email Playbook ($27)
- [ ] 3. AI Automation Toolkit ($47)
- [ ] 4. Vibe Coding Playbook ($47)
- [ ] 5. Solopreneur Tech Stack Guide ($17)
- [ ] 6. Twitter Growth Playbook ($27)
- [ ] 7. Sleep YouTube Starter Kit ($17)
- [ ] 8. AI Content Farm Blueprint ($47)
- [ ] 9. Local Biz Client System ($97)
- [ ] 10. $0 to $5K Playbook ($47)

## Listings Created
Count: 0

## Total Product Value
$375 (if all sold once)

## Status
RUNNING
EOF
fi

echo "Starting digital products loop..."
cd "$PROJECT_DIR"
# SAFETY: Load guardrails wrapper
source "$PROJECT_DIR/AUTOMATIONS/guardrails_wrapper.sh"


iteration=1
max_iterations=25

while [ $iteration -le $max_iterations ]; do
    echo "=== Iteration $iteration ==="

    if grep -q "Status.*COMPLETE" "$PROGRESS_DIR/progress.md"; then
        echo "Loop complete!"
        break
    fi

    cat "$SCRIPT_DIR/prompt.md" | claude --print --dangerously-skip-permissions --model claude-opus-4-6

    echo ""
    iteration=$((iteration + 1))
    sleep 5
done

echo "Digital products loop finished after $iteration iterations"
