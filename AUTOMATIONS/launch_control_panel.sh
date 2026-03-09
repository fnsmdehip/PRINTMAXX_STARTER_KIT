#!/bin/bash
# Launch PRINTMAXX Control Panel if not already running
# Called as SessionStart hook — must be fast and silent

PORT=9999
PROJECT="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
PYTHON="$(which python3)"
LOG="$PROJECT/AUTOMATIONS/logs/control_panel.log"

# Check if already running on port 9999
if lsof -i :$PORT -sTCP:LISTEN >/dev/null 2>&1; then
    exit 0
fi

# Launch in background, detached from terminal
nohup "$PYTHON" "$PROJECT/AUTOMATIONS/control_panel.py" >> "$LOG" 2>&1 &

# Brief wait to verify it started
sleep 1
if lsof -i :$PORT -sTCP:LISTEN >/dev/null 2>&1; then
    echo "Control Panel launched at http://localhost:$PORT"
else
    echo "Control Panel failed to start — check $LOG"
fi

exit 0
