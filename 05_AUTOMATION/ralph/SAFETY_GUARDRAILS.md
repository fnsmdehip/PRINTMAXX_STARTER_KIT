# Ralph Loop Safety Guardrails

## Current Configuration (SAFE MODE)

All ralph loops now run with these restrictions:

### What's ALLOWED
- **Read/Grep/Glob**: Read files in project
- **Write/Edit**: Create/modify files in project
- **WebSearch/WebFetch**: Research on the web
- **TodoWrite**: Task tracking
- **Chrome MCP**: Browser automation via `mcp__Claude_in_Chrome__*` tools

### What's BLOCKED
- **Bash tool**: Completely disabled (no shell commands)
- **Delete operations**: Cannot rm, unlink, or delete anything
- **Outside project**: Cannot access files outside PRINTMAXX folder
- **Direct file overwrites**: Safety rules require reading first

### Why No Bash?

Without Bash tool, the AI literally cannot run:
- `rm -rf /` or any delete
- `mv` to move files destructively
- `chmod` to change permissions
- `sudo` for root access
- Any shell command at all

The only file operations available are:
- **Read**: Read file contents
- **Write**: Create new file OR overwrite (but rules say read first)
- **Edit**: Modify specific parts of file

## Tool Whitelist

```bash
--allowedTools "Read,Grep,Glob,Write,Edit,WebSearch,WebFetch,TodoWrite,mcp__Claude_in_Chrome__computer,mcp__Claude_in_Chrome__read_page,mcp__Claude_in_Chrome__navigate,mcp__Claude_in_Chrome__find,mcp__Claude_in_Chrome__javascript_tool,mcp__Claude_in_Chrome__tabs_context_mcp,mcp__Claude_in_Chrome__tabs_create_mcp,mcp__Claude_in_Chrome__get_page_text"
```

## Safety Rules in Every Prompt

Every loop prepends these rules:

```
## CRITICAL SAFETY RULES - ALWAYS FOLLOW

1. ONLY operate within: /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/
2. NEVER delete files (you don't have Bash access anyway)
3. ONLY append to CSV files - read first, then append new rows
4. READ existing files before modifying them
5. For browser: use mcp__Claude_in_Chrome__* tools only
6. Create new files freely, but don't overwrite without reading first
```

## Risk Assessment

| Risk | Mitigation | Status |
|------|------------|--------|
| Delete files | No Bash tool | BLOCKED |
| System access | Project folder only | BLOCKED |
| Overwrite important files | Rules require read first | MITIGATED |
| Run malicious commands | No Bash tool | BLOCKED |
| Access other projects | Prompt rules | MITIGATED |

## Testing Before Overnight Run

```bash
# Test single iteration
./ralph/loops/content_social/run.sh 1

# Check for errors
cat ralph/loops/content_social/.ralph/errors.log

# Review activity
cat ralph/loops/content_social/.ralph/activity.log | tail -50
```

## If You Need Bash (Build Tasks)

For loops that genuinely need npm/git, create a separate `run_with_bash.sh`:

```bash
# Only for build tasks that need it
--allowedTools "Read,Grep,Glob,Write,Edit,Bash(npm:*),Bash(git:status),Bash(git:add),Bash(git:commit),Bash(ls:*)"
```

**But the default safe runner has no Bash at all.**

## Summary

Your drive is safe because:
1. **No Bash** = No shell commands = No rm/mv/chmod/sudo
2. **Project folder only** = Cannot access ~/Desktop, /etc, etc
3. **Append-only CSV** = Preserves existing data
4. **Read-first rule** = Won't blindly overwrite

Sleep well.
