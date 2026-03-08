#!/usr/bin/env python3
"""
PostToolUse hook: Detect safe_path() calls where the return value is discarded.

Pattern caught:
    safe_path(some_file)           # validates but discards resolved path
    some_file.write_text(...)      # uses the ORIGINAL un-resolved path

Should be:
    resolved = safe_path(some_file)
    resolved.write_text(...)

Triggered on: Write|Edit of .py files
Exit code 0 = pass (no issues or not a .py file)
Exit code 1 = block (found discarded safe_path return values)
"""

import json
import os
import re
import sys


def main():
    tool_input_raw = os.environ.get("CLAUDE_TOOL_INPUT", "{}")
    try:
        tool_input = json.loads(tool_input_raw)
    except json.JSONDecodeError:
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not file_path.endswith(".py"):
        sys.exit(0)

    # For Edit, check both old_string and new_string
    # For Write, check content
    new_content = tool_input.get("content", "")
    new_string = tool_input.get("new_string", "")

    text_to_check = new_content or new_string
    if not text_to_check:
        sys.exit(0)

    # Pattern: standalone safe_path() call on its own line (not assigned, not chained)
    # Matches:  "    safe_path(SOME_VAR)"  but NOT  "x = safe_path(...)" or "safe_path(...).mkdir(...)"
    pattern = re.compile(
        r"^\s+safe_path\([^)]+\)\s*$",
        re.MULTILINE,
    )

    matches = pattern.findall(text_to_check)
    if matches:
        print("HOOK BLOCK: safe_path() return value is being discarded.")
        print("The path is validated but the resolved path is NOT used for the actual file operation.")
        print("")
        print("Found these discarded calls:")
        for m in matches:
            print(f"  {m.strip()}")
        print("")
        print("FIX: Assign the return value and use it:")
        print("  resolved = safe_path(some_path)")
        print("  resolved.write_text(...)  # use resolved, not original")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
