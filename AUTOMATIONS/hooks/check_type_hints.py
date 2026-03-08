#!/usr/bin/env python3
"""
PostToolUse hook: Check that new Python files include type hints.

Issue: Type hints were added to 6 files but not to the 3 new files created
in the same session. This hook catches new files that lack type hints.

Only triggers on Write (new file creation), not Edit.
Only warns if the file has functions/methods without ANY type annotations.

Exit code 0 = pass (always - this is advisory only)
"""

import json
import os
import re
import sys


def main():
    tool_input_raw = os.environ.get("CLAUDE_TOOL_INPUT", "{}")
    tool_name = os.environ.get("CLAUDE_TOOL_NAME", "")
    try:
        tool_input = json.loads(tool_input_raw)
    except json.JSONDecodeError:
        sys.exit(0)

    # Only check Write (new file creation), not Edit
    if tool_name != "Write":
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not file_path.endswith(".py"):
        sys.exit(0)

    content = tool_input.get("content", "")
    if not content:
        sys.exit(0)

    # Find all function/method definitions
    func_pattern = re.compile(r"^\s*def\s+(\w+)\s*\(([^)]*)\)", re.MULTILINE)
    funcs = func_pattern.findall(content)

    if not funcs:
        sys.exit(0)

    # Check for return type annotations
    return_type_pattern = re.compile(r"^\s*def\s+\w+\s*\([^)]*\)\s*->", re.MULTILINE)
    has_return_types = bool(return_type_pattern.search(content))

    # Check for parameter type annotations (look for ': type' in params)
    param_type_pattern = re.compile(r"def\s+\w+\s*\([^)]*:\s*\w+", re.MULTILINE)
    has_param_types = bool(param_type_pattern.search(content))

    # Check for 'from __future__ import annotations' or 'from typing import'
    has_typing_imports = bool(
        re.search(r"from\s+__future__\s+import\s+annotations", content)
        or re.search(r"from\s+typing\s+import", content)
    )

    untyped_funcs = []
    for name, params in funcs:
        if name.startswith("_") and name != "__init__":
            continue  # skip private helpers for now
        # Check if this specific function has type hints
        specific = re.search(
            rf"def\s+{re.escape(name)}\s*\([^)]*:\s*\w+[^)]*\)\s*->",
            content,
        )
        if not specific:
            untyped_funcs.append(name)

    if untyped_funcs and not has_typing_imports and not has_return_types:
        print("HOOK ADVISORY: New Python file has no type hints.")
        print(f"File: {file_path}")
        print(f"Functions without type annotations: {', '.join(untyped_funcs[:10])}")
        print("")
        print("Other files in this project use type hints. For consistency, add:")
        print("  from __future__ import annotations")
        print("  def my_func(param: str) -> bool:")
        print("")
        print("This is advisory only -- not blocking the write.")

    sys.exit(0)


if __name__ == "__main__":
    main()
