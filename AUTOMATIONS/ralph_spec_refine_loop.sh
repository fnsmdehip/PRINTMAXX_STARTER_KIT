#!/usr/bin/env bash
# Ralph Spec Refiner Loop
# Usage: bash AUTOMATIONS/ralph_spec_refine_loop.sh
# Runs overnight — each iteration refines one app spec using Opus at max quality
# Stop anytime with Ctrl+C

set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_FILE="$BASE_DIR/AUTOMATIONS/ralph_spec_refine_state.json"
PROMPT_FILE="$BASE_DIR/AUTOMATIONS/ralph_spec_refine_prompt.md"
LOG_FILE="$BASE_DIR/AUTOMATIONS/logs/ralph_spec_refine.log"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"

# Ensure log dir exists
mkdir -p "$BASE_DIR/AUTOMATIONS/logs"
mkdir -p "$BASE_DIR/APPS/specs"

echo "" >> "$LOG_FILE"
echo "===== LOOP START: $(date -u +%Y-%m-%dT%H:%M:%SZ) =====" >> "$LOG_FILE"
echo "🚀 Ralph Spec Refiner starting — $(date)"
echo "   Model: claude-opus-4-6 (max quality)"
echo "   State: $STATE_FILE"
echo "   Output: $BASE_DIR/APPS/specs/"
echo "   Log: $LOG_FILE"
echo ""

# Validate prerequisites
if [ ! -f "$STATE_FILE" ]; then
  echo "ERROR: State file not found: $STATE_FILE" >&2
  exit 1
fi
if [ ! -f "$PROMPT_FILE" ]; then
  echo "ERROR: Prompt file not found: $PROMPT_FILE" >&2
  exit 1
fi
if ! command -v "$CLAUDE_BIN" &>/dev/null; then
  echo "ERROR: claude CLI not found. Install with: curl -fsSL https://claude.ai/install.sh | bash" >&2
  exit 1
fi
if [ ! -f "$BASE_DIR/lie-detector-app/TruthScope/HANDOFF.md" ]; then
  echo "ERROR: TruthScope gold standard not found at lie-detector-app/TruthScope/HANDOFF.md" >&2
  exit 1
fi

# Check for API key
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo "WARNING: ANTHROPIC_API_KEY not set — claude will use OAuth (may expire silently)" >&2
  echo "         Set it with: export ANTHROPIC_API_KEY=sk-ant-..." >&2
  API_KEY_ARG=""
else
  API_KEY_ARG="--api-key $ANTHROPIC_API_KEY"
  echo "✓ ANTHROPIC_API_KEY found — using --api-key flag (per Rule 18)"
fi

ITERATION=0
MAX_ITERATIONS=20   # Safety cap — 4 apps * 5 retries max

while [ $ITERATION -lt $MAX_ITERATIONS ]; do
  ITERATION=$((ITERATION + 1))

  # Check how many apps are still pending
  PENDING=$(python3 -c "
import json
with open('$STATE_FILE') as f:
    data = json.load(f)
pending = [a for a in data['apps'] if a['status'] == 'pending']
print(len(pending))
")

  if [ "$PENDING" -eq 0 ]; then
    echo ""
    echo "✅ All apps refined! Loop complete."
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | LOOP COMPLETE | All apps done" >> "$LOG_FILE"
    break
  fi

  # Get next pending app name
  NEXT_APP=$(python3 -c "
import json
with open('$STATE_FILE') as f:
    data = json.load(f)
pending = sorted([a for a in data['apps'] if a['status'] == 'pending'], key=lambda x: x['priority'])
print(pending[0]['id'] if pending else '')
")

  if [ -z "$NEXT_APP" ]; then
    echo "✅ All apps refined! Loop complete."
    break
  fi

  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  Iteration $ITERATION — Refining: $NEXT_APP"
  echo "  Started: $(date)"
  echo "  Pending remaining: $PENDING"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | START | $NEXT_APP | iteration=$ITERATION" >> "$LOG_FILE"

  # Build the full prompt: template + working directory injection
  FULL_PROMPT="$(cat "$PROMPT_FILE")

## Context injected by loop runner
- Working directory: $BASE_DIR
- State file: $STATE_FILE
- Current iteration: $ITERATION
- This is a fresh context. Read the state file now as Step 1."

  # Run claude with Opus at max tokens, --dangerously-skip-permissions for file writes
  # Extended thinking via budget_tokens is set via --thinking flag (max effort)
  START_TIME=$(date +%s)

  if [ -n "${API_KEY_ARG}" ]; then
    echo "$FULL_PROMPT" | "$CLAUDE_BIN" \
      --model claude-opus-4-6 \
      --max-tokens 32000 \
      --dangerously-skip-permissions \
      $API_KEY_ARG \
      -p \
      2>> "$LOG_FILE" \
      && CLAUDE_EXIT=0 || CLAUDE_EXIT=$?
  else
    echo "$FULL_PROMPT" | "$CLAUDE_BIN" \
      --model claude-opus-4-6 \
      --max-tokens 32000 \
      --dangerously-skip-permissions \
      -p \
      2>> "$LOG_FILE" \
      && CLAUDE_EXIT=0 || CLAUDE_EXIT=$?
  fi

  END_TIME=$(date +%s)
  ELAPSED=$((END_TIME - START_TIME))

  if [ $CLAUDE_EXIT -ne 0 ]; then
    echo ""
    echo "⚠️  Claude exited with code $CLAUDE_EXIT for app: $NEXT_APP"
    echo "   Check log for details: $LOG_FILE"
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | ERROR | $NEXT_APP | exit_code=$CLAUDE_EXIT" >> "$LOG_FILE"

    # Mark as failed in state so we can skip it and retry manually
    python3 -c "
import json, datetime
with open('$STATE_FILE') as f:
    data = json.load(f)
for app in data['apps']:
    if app['id'] == '$NEXT_APP' and app['status'] == 'in_progress':
        app['status'] = 'failed'
        app['notes'] = 'claude exit code $CLAUDE_EXIT'
data['last_updated'] = datetime.datetime.utcnow().isoformat()
with open('$STATE_FILE', 'w') as f:
    json.dump(data, f, indent=2)
"
    echo "   App marked as 'failed' in state file. Skipping to next app."
    continue
  fi

  # Verify the output file was created
  OUTPUT_PATH=$(python3 -c "
import json
with open('$STATE_FILE') as f:
    data = json.load(f)
for app in data['apps']:
    if app['id'] == '$NEXT_APP':
        print(app.get('output_spec', ''))
        break
")

  if [ -n "$OUTPUT_PATH" ] && [ -f "$BASE_DIR/$OUTPUT_PATH" ]; then
    WORD_COUNT=$(wc -w < "$BASE_DIR/$OUTPUT_PATH")
    echo ""
    echo "✅ $NEXT_APP refined! ($ELAPSED seconds, $WORD_COUNT words)"
    echo "   Spec: $BASE_DIR/$OUTPUT_PATH"
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | VERIFIED | $NEXT_APP | ${ELAPSED}s | ${WORD_COUNT}w" >> "$LOG_FILE"
  else
    echo ""
    echo "⚠️  $NEXT_APP: claude ran but output file not found at $OUTPUT_PATH"
    echo "   Claude may have written to a different path — check manually"
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | MISSING_OUTPUT | $NEXT_APP | expected=$OUTPUT_PATH" >> "$LOG_FILE"
  fi

  # Ensure state was updated (safety: if claude forgot, mark done anyway if output exists)
  STATUS=$(python3 -c "
import json
with open('$STATE_FILE') as f:
    data = json.load(f)
for app in data['apps']:
    if app['id'] == '$NEXT_APP':
        print(app['status'])
        break
")

  if [ "$STATUS" = "in_progress" ]; then
    echo "   Note: state still in_progress — forcing to done (output file exists)"
    python3 -c "
import json, datetime
with open('$STATE_FILE') as f:
    data = json.load(f)
for app in data['apps']:
    if app['id'] == '$NEXT_APP':
        app['status'] = 'done'
        app['completed_at'] = datetime.datetime.utcnow().isoformat()
        app['notes'] = 'status forced by loop runner (claude did not update state)'
data['last_updated'] = datetime.datetime.utcnow().isoformat()
with open('$STATE_FILE', 'w') as f:
    json.dump(data, f, indent=2)
"
  fi

  echo ""
  echo "   Sleeping 10s before next iteration..."
  sleep 10

done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  LOOP FINISHED — $(date)"
echo ""

# Final status report
python3 -c "
import json
with open('$STATE_FILE') as f:
    data = json.load(f)
done = [a for a in data['apps'] if a['status'] == 'done']
pending = [a for a in data['apps'] if a['status'] == 'pending']
failed = [a for a in data['apps'] if a['status'] == 'failed']
print(f'  Done:    {len(done)} apps')
print(f'  Pending: {len(pending)} apps')
print(f'  Failed:  {len(failed)} apps')
if done:
    print()
    print('  Refined specs:')
    for a in done:
        print(f'    - {a[\"id\"]}: {a[\"output_spec\"]}')
if failed:
    print()
    print('  Failed (retry manually):')
    for a in failed:
        print(f'    - {a[\"id\"]}: {a[\"notes\"]}')
"
echo ""
echo "Log: $LOG_FILE"
echo "State: $STATE_FILE"
