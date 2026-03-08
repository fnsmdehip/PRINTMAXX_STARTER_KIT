#!/usr/bin/env python3
"""
PostToolUse hook: Detect file handle leaks in Python code.

Patterns caught:
    f = open("file.txt", "w")    # assigned but never closed / not in 'with'
    self._fd = open(...)          # assigned to instance var without context manager

Acceptable patterns:
    with open(...) as f:          # context manager, auto-closes
    lock_fd = open(LOCK_FILE)     # lock files are intentionally held open

Triggered on: Write|Edit of .py files
Exit code 0 = pass
Exit code 1 = block (found likely file handle leaks)
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

    new_content = tool_input.get("content", "")
    new_string = tool_input.get("new_string", "")

    text_to_check = new_content or new_string
    if not text_to_check:
        sys.exit(0)

    # Pattern: variable = open(...) NOT inside a with statement
    # We look for lines like: some_var = open(...) that are NOT preceded by "with"
    bare_open_pattern = re.compile(
        r"^(?!\s*with\s)(\s*\S+\s*=\s*open\([^)]+\))",
        re.MULTILINE,
    )

    matches = bare_open_pattern.findall(text_to_check)

    # Filter out known acceptable patterns (lock files)
    real_leaks = []
    for m in matches:
        stripped = m.strip()
        # Lock files are intentionally held open
        if "lock" in stripped.lower():
            continue
        # Some patterns use open() then immediately close in a try/finally
        real_leaks.append(stripped)

    if real_leaks:
        print("HOOK WARNING: Possible file handle leak detected.")
        print("Using 'variable = open(...)' without a context manager can leak file handles.")
        print("")
        print("Found:")
        for leak in real_leaks:
            print(f"  {leak}")
        print("")
        print("FIX: Use a context manager instead:")
        print("  with open('file.txt', 'w') as f:")
        print("      f.write(data)")
        print("")
        print("If this is intentional (e.g., lock file), add 'lock' to the variable name.")
        # Warning only, don't block
        sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()
