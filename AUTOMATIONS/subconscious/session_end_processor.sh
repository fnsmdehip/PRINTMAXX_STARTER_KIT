#!/bin/bash
# PRINTMAXX Subconscious — Session End Processor
# ================================================
# Runs as a Stop hook. Saves session transcript, then launches a BACKGROUND
# Claude Code session (using your Max plan) to extract memories.
# 100% TOS-friendly — just running Claude Code normally.

set -uo pipefail

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
SUBCONSCIOUS_DIR="$BASE/AUTOMATIONS/subconscious"
MEMORY_DIR="$SUBCONSCIOUS_DIR/memories"
TRANSCRIPTS_DIR="$SUBCONSCIOUS_DIR/transcripts"
LOCK_FILE="$SUBCONSCIOUS_DIR/.processing.lock"
LOG_FILE="$SUBCONSCIOUS_DIR/subconscious.log"

mkdir -p "$MEMORY_DIR" "$TRANSCRIPTS_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Read hook input from stdin
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('session_id','unknown'))" 2>/dev/null || echo "unknown")
TRANSCRIPT_FILE=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('transcript_path',''))" 2>/dev/null || echo "")

log "Stop hook fired. Session: $SESSION_ID"

# Get the conversation transcript from Claude's session file
# Claude Code stores conversations in ~/.claude/projects/*/SESSION_ID.jsonl
CONV_FILE="$HOME/.claude/projects/-Users-macbookpro/${SESSION_ID}.jsonl"

if [ ! -f "$CONV_FILE" ]; then
    # Try finding it
    CONV_FILE=$(find "$HOME/.claude/projects" -name "${SESSION_ID}.jsonl" 2>/dev/null | head -1)
fi

if [ -z "$CONV_FILE" ] || [ ! -f "$CONV_FILE" ]; then
    log "No conversation file found for session $SESSION_ID"
    exit 0
fi

# Extract a summary of the conversation (last 200 lines to stay manageable)
TRANSCRIPT_OUT="$TRANSCRIPTS_DIR/session_${SESSION_ID}_$(date +%Y%m%d_%H%M%S).txt"

# Extract human and assistant messages from the JSONL
python3 -c "
import json, sys

messages = []
try:
    with open('$CONV_FILE', 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                role = entry.get('role', '')
                content = entry.get('content', '')
                if role in ('human', 'assistant') and isinstance(content, str) and len(content) > 20:
                    # Truncate very long messages
                    if len(content) > 2000:
                        content = content[:2000] + '... [truncated]'
                    messages.append(f'[{role.upper()}] {content}')
            except json.JSONDecodeError:
                continue
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)

# Keep last 50 meaningful exchanges
for msg in messages[-50:]:
    print(msg)
    print()
" > "$TRANSCRIPT_OUT" 2>/dev/null

TRANSCRIPT_SIZE=$(wc -c < "$TRANSCRIPT_OUT" 2>/dev/null || echo "0")
if [ "$TRANSCRIPT_SIZE" -lt 100 ]; then
    log "Transcript too small ($TRANSCRIPT_SIZE bytes), skipping processing"
    rm -f "$TRANSCRIPT_OUT"
    exit 0
fi

log "Saved transcript ($TRANSCRIPT_SIZE bytes): $TRANSCRIPT_OUT"

# Don't stack multiple processors
if [ -f "$LOCK_FILE" ]; then
    LOCK_AGE=$(( $(date +%s) - $(stat -f %m "$LOCK_FILE" 2>/dev/null || echo "0") ))
    if [ "$LOCK_AGE" -lt 300 ]; then
        log "Another processor is running (age: ${LOCK_AGE}s), skipping"
        exit 0
    fi
    log "Stale lock file (age: ${LOCK_AGE}s), removing"
    rm -f "$LOCK_FILE"
fi

# Launch background Claude Code session to process the transcript
# This uses your Max plan — just a normal Claude Code invocation
touch "$LOCK_FILE"
log "Launching background memory extraction..."

nohup bash -c "
    cd '$BASE'

    # Build the prompt
    PROMPT=\"You are the PRINTMAXX subconscious memory processor. Read the session transcript below and extract key memories.

RULES:
1. Extract ONLY genuinely important information (decisions, new files created, bugs found, user preferences, strategic changes)
2. Skip routine tool calls, file reads, and mechanical operations
3. Be CONCISE — each memory should be 1-2 sentences max
4. Categorize each memory as: DECISION, CREATED, LEARNED, PREFERENCE, STRATEGIC, BLOCKER, or COMPLETED
5. Output in this exact format, one per line:
   CATEGORY|memory text|confidence(0-100)

Example:
DECISION|User chose self-hosted Letta over cloud API for privacy|95
CREATED|Built quality_gate.py with 5 scoring dimensions (apps/content/email/listing/scripts)|90
PREFERENCE|User explicitly does NOT want persistent_memory.py, wants subconscious system instead|100

SESSION TRANSCRIPT:
\$(cat '$TRANSCRIPT_OUT')

Extract the key memories now. Output ONLY the CATEGORY|memory|confidence lines, nothing else.\"

    # Run Claude Code to extract memories
    RESULT=\$(echo \"\$PROMPT\" | claude -p 2>/dev/null || echo 'EXTRACTION_FAILED')

    if [ \"\$RESULT\" = 'EXTRACTION_FAILED' ] || [ -z \"\$RESULT\" ]; then
        echo '[$(date)] Memory extraction failed' >> '$LOG_FILE'
        rm -f '$LOCK_FILE'
        exit 1
    fi

    # Append new memories to the memory file
    MEMORY_FILE='$MEMORY_DIR/memories.jsonl'
    TIMESTAMP=\$(date -u +%Y-%m-%dT%H:%M:%SZ)

    echo \"\$RESULT\" | while IFS='|' read -r category memory confidence; do
        # Skip empty lines and malformed entries
        [ -z \"\$category\" ] && continue
        [ -z \"\$memory\" ] && continue

        # Validate category
        case \"\$category\" in
            DECISION|CREATED|LEARNED|PREFERENCE|STRATEGIC|BLOCKER|COMPLETED) ;;
            *) continue ;;
        esac

        # Default confidence
        confidence=\${confidence:-50}

        # Write as JSONL
        python3 -c \"
import json, sys
entry = {
    'timestamp': '$TIMESTAMP',
    'session_id': '$SESSION_ID',
    'category': sys.argv[1].strip(),
    'memory': sys.argv[2].strip(),
    'confidence': int(sys.argv[3].strip() if sys.argv[3].strip().isdigit() else '50'),
    'active': True
}
print(json.dumps(entry))
\" \"\$category\" \"\$memory\" \"\$confidence\" >> \"\$MEMORY_FILE\"
    done

    # Count new memories
    NEW_COUNT=\$(echo \"\$RESULT\" | grep -c '|' || echo '0')
    echo \"[$(date)] Extracted \$NEW_COUNT memories from session $SESSION_ID\" >> '$LOG_FILE'

    # Prune old memories (keep last 500)
    if [ -f \"\$MEMORY_FILE\" ]; then
        TOTAL=\$(wc -l < \"\$MEMORY_FILE\")
        if [ \"\$TOTAL\" -gt 500 ]; then
            tail -500 \"\$MEMORY_FILE\" > \"\${MEMORY_FILE}.tmp\"
            mv \"\${MEMORY_FILE}.tmp\" \"\$MEMORY_FILE\"
            echo '[$(date)] Pruned memories to 500 entries' >> '$LOG_FILE'
        fi
    fi

    # Clean up old transcripts (keep last 20)
    ls -t '$TRANSCRIPTS_DIR'/session_*.txt 2>/dev/null | tail -n +21 | xargs rm -f 2>/dev/null

    rm -f '$LOCK_FILE'
" >> "$LOG_FILE" 2>&1 &

log "Background processor launched (PID: $!)"
exit 0
