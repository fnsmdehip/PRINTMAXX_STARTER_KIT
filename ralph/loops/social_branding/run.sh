#!/bin/bash

# Social Branding Ralph Loop

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROGRESS_DIR="$SCRIPT_DIR/.ralph"
PROJECT_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"

mkdir -p "$PROGRESS_DIR"
mkdir -p "$PROJECT_DIR/PRODUCTS/branding"

if [ ! -f "$PROGRESS_DIR/progress.md" ]; then
    cat > "$PROGRESS_DIR/progress.md" <<'EOF'
# Social Branding Progress

## Tasks
- [ ] 1. @PRINTMAXXER Brand Identity
- [ ] 2. Findom Persona Brand Identities (3 personas)
- [ ] 3. Faith Niche Accounts (2 accounts)
- [ ] 4. Fitness Niche Accounts (2 accounts)
- [ ] 5. Meme/Engagement Farm Accounts (3 accounts)
- [ ] 6. Business/Service Pages (2 accounts)
- [ ] 7. Content Farm Channel Names (5 channels)
- [ ] 8. Newsletter Brand Identities (3 newsletters)
- [ ] 9. Master Account Portfolio CSV

## Deliverables Created
Count: 0

## Status
RUNNING
EOF
fi

echo "Starting social branding loop..."
cd "$PROJECT_DIR"
# SAFETY: Load guardrails wrapper
source "$PROJECT_DIR/AUTOMATIONS/guardrails_wrapper.sh"


iteration=1
max_iterations=15

while [ $iteration -le $max_iterations ]; do
    echo "=== Iteration $iteration ==="

    if grep -q "Status.*COMPLETE" "$PROGRESS_DIR/progress.md"; then
        echo "Loop complete!"
        break
    fi

    cat "$SCRIPT_DIR/prompt.md" | claude --print --dangerously-skip-permissions --model claude-opus-4-6

    echo ""
    iteration=$((iteration + 1))
    sleep 2
done

echo "Social branding loop finished after $iteration iterations"
