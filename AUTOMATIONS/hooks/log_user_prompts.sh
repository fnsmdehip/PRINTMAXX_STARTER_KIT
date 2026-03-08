#!/bin/bash
# Hook: UserPromptSubmit -- logs every user prompt to LEDGER/USER_PROMPTS.jsonl
# Must be extremely fast (<1s). Receives JSON on stdin with "message" field.

PROJECT_ROOT="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
OUT="${PROJECT_ROOT}/LEDGER/USER_PROMPTS.jsonl"

# Pipe stdin directly to python3 for safe JSON handling
python3 -c "
import json, sys, os
from datetime import datetime

try:
    raw = sys.stdin.read()
    data = json.loads(raw) if raw.strip() else {}
except Exception:
    sys.exit(0)

msg = data.get('message', '') or data.get('prompt', '') or ''
if not msg:
    sys.exit(0)

sid = os.environ.get('CLAUDE_SESSION_ID', '')
if not sid:
    sid = 'session_' + str(os.getppid()) + '_' + datetime.now().strftime('%Y%m%d')

entry = {
    'ts': datetime.now().isoformat(timespec='seconds'),
    'prompt': msg[:10000],
    'session_id': sid
}

outpath = '${OUT}'
with open(outpath, 'a') as f:
    f.write(json.dumps(entry, ensure_ascii=False) + '\n')
" 2>/dev/null

exit 0
