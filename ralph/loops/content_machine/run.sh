#!/bin/bash

# Content Machine Ralph Loop

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROGRESS_DIR="$SCRIPT_DIR/.ralph"
PROJECT_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"

mkdir -p "$PROGRESS_DIR"
mkdir -p "$PROJECT_DIR/CONTENT/social/threads"
mkdir -p "$PROJECT_DIR/CONTENT/social/findom"
mkdir -p "$PROJECT_DIR/CONTENT/social/faith"
mkdir -p "$PROJECT_DIR/CONTENT/social/fitness"
mkdir -p "$PROJECT_DIR/CONTENT/social/memes"
mkdir -p "$PROJECT_DIR/CONTENT/social/linkedin"
mkdir -p "$PROJECT_DIR/CONTENT/social/reddit"
mkdir -p "$PROJECT_DIR/CONTENT/social/pinterest"
mkdir -p "$PROJECT_DIR/CONTENT/video"
mkdir -p "$PROJECT_DIR/CONTENT/newsletters"
mkdir -p "$PROJECT_DIR/CONTENT/medium_articles"
mkdir -p "$PROJECT_DIR/CONTENT/email_sequences/cold"
mkdir -p "$PROJECT_DIR/PRODUCTS/descriptions"

if [ ! -f "$PROGRESS_DIR/progress.md" ]; then
    cat > "$PROGRESS_DIR/progress.md" <<'EOF'
# Content Machine Progress

## Batches
- [ ] 1. Twitter Threads x20
- [ ] 2. Findom 30-Day Calendar
- [ ] 3. Faith Content x50
- [ ] 4. Fitness Content x50
- [ ] 5. Meme Content x100
- [ ] 6. LinkedIn Posts x30
- [ ] 7. Reddit Posts x30
- [ ] 8. YouTube Shorts Scripts x20
- [ ] 9. Newsletter Issues x10
- [ ] 10. Medium Articles x10
- [ ] 11. Cold Email Sequences x5
- [ ] 12. Pinterest Pins x50
- [ ] 13. TikTok Scripts x20
- [ ] 14. Reply Templates x100
- [ ] 15. Product Descriptions x20

## Total Content Pieces Generated
Count: 0

## Status
RUNNING
EOF
fi

echo "Starting content machine loop..."
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

echo "Content machine loop finished after $iteration iterations"
