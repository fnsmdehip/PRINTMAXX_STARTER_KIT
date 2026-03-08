#!/bin/bash
# Hook: PostToolUse for Write|Edit — detects leaked secrets in written files
# Warns (doesn't block) if potential credentials found

FILE_PATH="$TOOL_INPUT_FILE_PATH"

# Only check code files
[[ "$FILE_PATH" != *.py && "$FILE_PATH" != *.js && "$FILE_PATH" != *.ts && "$FILE_PATH" != *.json && "$FILE_PATH" != *.sh && "$FILE_PATH" != *.md ]] && exit 0

# Skip credential files (they're supposed to have secrets)
[[ "$FILE_PATH" == *CREDENTIALS* || "$FILE_PATH" == *SECRETS* || "$FILE_PATH" == *.env* ]] && exit 0

[ ! -f "$FILE_PATH" ] && exit 0

# Check for common secret patterns
FOUND=$(grep -nE '(sk-[a-zA-Z0-9]{20,}|sk_live_|sk_test_|AKIA[A-Z0-9]{16}|ghp_[a-zA-Z0-9]{36}|password\s*=\s*["\x27][^"\x27]{8,})' "$FILE_PATH" 2>/dev/null | head -5)

if [ -n "$FOUND" ]; then
    echo "WARNING: Potential secrets detected in $FILE_PATH:"
    echo "$FOUND"
    echo "Move credentials to SECRETS/CREDENTIALS.env and use env vars instead."
fi

# Don't block, just warn
exit 0
