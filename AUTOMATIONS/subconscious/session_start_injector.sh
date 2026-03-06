#!/bin/bash
# PRINTMAXX Subconscious — Session Start Injector
# ================================================
# Runs as a SessionStart hook. Reads memories from memories.jsonl
# and outputs relevant context for the new session.

set -uo pipefail

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
SUBCONSCIOUS_DIR="$BASE/AUTOMATIONS/subconscious"
MEMORY_FILE="$SUBCONSCIOUS_DIR/memories/memories.jsonl"
LOG_FILE="$SUBCONSCIOUS_DIR/subconscious.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# No memories yet? Skip silently
if [ ! -f "$MEMORY_FILE" ] || [ ! -s "$MEMORY_FILE" ]; then
    log "SessionStart: No memories file found, skipping injection"
    exit 0
fi

# Extract and format recent high-confidence memories
CONTEXT=$(python3 -c "
import json, sys
from datetime import datetime, timedelta

memories = []
try:
    with open('$MEMORY_FILE', 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if entry.get('active', True):
                    memories.append(entry)
            except json.JSONDecodeError:
                continue
except Exception as e:
    print(f'Error reading memories: {e}', file=sys.stderr)
    sys.exit(0)

if not memories:
    sys.exit(0)

# Sort by confidence (highest first), then by timestamp (newest first)
memories.sort(key=lambda m: (-m.get('confidence', 50), m.get('timestamp', '')))

# Take top 30 memories (keep context budget reasonable)
top = memories[:30]

# Group by category
categories = {}
for m in top:
    cat = m.get('category', 'GENERAL')
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(m)

# Format output
lines = []
lines.append('=== SUBCONSCIOUS MEMORY (auto-injected) ===')
lines.append('')

# Priority order for categories
cat_order = ['PREFERENCE', 'DECISION', 'STRATEGIC', 'BLOCKER', 'LEARNED', 'CREATED', 'COMPLETED']
seen_cats = set()

for cat in cat_order:
    if cat in categories:
        seen_cats.add(cat)
        lines.append(f'[{cat}]')
        for m in categories[cat][:5]:  # Max 5 per category
            conf = m.get('confidence', 50)
            text = m.get('memory', '').strip()
            if text:
                lines.append(f'  - {text} (conf:{conf})')
        lines.append('')

# Any remaining categories
for cat in sorted(categories.keys()):
    if cat not in seen_cats:
        lines.append(f'[{cat}]')
        for m in categories[cat][:3]:
            conf = m.get('confidence', 50)
            text = m.get('memory', '').strip()
            if text:
                lines.append(f'  - {text} (conf:{conf})')
        lines.append('')

lines.append('=== END SUBCONSCIOUS MEMORY ===')

print('\n'.join(lines))
" 2>/dev/null)

if [ -z "$CONTEXT" ]; then
    log "SessionStart: No memories to inject"
    exit 0
fi

MEMORY_COUNT=$(echo "$CONTEXT" | grep -c "^  -" || echo "0")
log "SessionStart: Injecting $MEMORY_COUNT memories"

# Output the context — Claude Code hook system captures stdout
echo "$CONTEXT"
exit 0
