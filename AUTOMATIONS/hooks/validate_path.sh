#!/bin/bash
# Hook: PreToolUse for Write|Edit — validates file path is within project root
# Exits non-zero to BLOCK writes outside project

PROJECT_ROOT="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
FILE_PATH="$TOOL_INPUT_FILE_PATH"

# If no file path provided, allow (some tools don't have file_path)
[ -z "$FILE_PATH" ] && exit 0

# Resolve to absolute path
RESOLVED=$(python3 -c "from pathlib import Path; print(Path('$FILE_PATH').resolve())" 2>/dev/null)
[ -z "$RESOLVED" ] && exit 0

# Check if within project root
if [[ "$RESOLVED" != "$PROJECT_ROOT"* ]]; then
    echo "BLOCKED: $RESOLVED is outside project root $PROJECT_ROOT"
    exit 1
fi

exit 0
