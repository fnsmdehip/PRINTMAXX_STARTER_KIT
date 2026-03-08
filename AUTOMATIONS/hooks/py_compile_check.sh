#!/bin/bash
# Hook: PostToolUse for Write|Edit — auto-compiles Python files to catch syntax errors
# Runs after every .py file write/edit

FILE_PATH="$TOOL_INPUT_FILE_PATH"

# Only check Python files
[[ "$FILE_PATH" != *.py ]] && exit 0

# Skip if file doesn't exist (deleted)
[ ! -f "$FILE_PATH" ] && exit 0

# Compile check
OUTPUT=$(python3 -c "import py_compile; py_compile.compile('$FILE_PATH', doraise=True)" 2>&1)
if [ $? -ne 0 ]; then
    echo "SYNTAX ERROR in $FILE_PATH:"
    echo "$OUTPUT"
    exit 1
fi

exit 0
