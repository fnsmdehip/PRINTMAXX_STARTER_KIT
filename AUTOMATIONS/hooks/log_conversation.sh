#!/bin/bash
# Hook: log_conversation.sh — triggers conversation extraction
# Can be called on session end or manually.
# Calls conversation_logger.py --extract to process new Claude transcripts.

PROJECT_ROOT="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
PYTHON="/usr/bin/python3"
LOGFILE="${PROJECT_ROOT}/AUTOMATIONS/logs/conversation_logger.log"

# Ensure log dir exists
mkdir -p "${PROJECT_ROOT}/AUTOMATIONS/logs"

# Run extraction, append to log
echo "--- $(date '+%Y-%m-%d %H:%M:%S') --- conversation extraction triggered ---" >> "$LOGFILE"
"$PYTHON" "${PROJECT_ROOT}/AUTOMATIONS/conversation_logger.py" --extract >> "$LOGFILE" 2>&1
echo "--- extraction complete ---" >> "$LOGFILE"

exit 0
