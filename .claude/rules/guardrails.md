# Guardrails Rules (NON-NEGOTIABLE SAFETY)

## The ONE Rule: Stay In Your Lane

**ALL file operations (read, write, delete, move) MUST stay within the PRINTMAXX project folder:**
```
/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/
```

**DO NOT touch, modify, read, or interact with files in ANY other location. Period.**

## What You CAN Do

1. **Read/write/delete files** inside the PRINTMAXX project folder
2. **Launch apps** using `open -a "App Name"` (browsers, Simulator, Xcode, Finder)
3. **Open URLs** using `open "https://..."` (opens in default browser)
4. **Run scripts** (Python, Node, bash) that operate on project files
5. **Run CLI tools** (git, gh, npm, npx, surge, vercel, brew, curl, pip3)
6. **Run iOS Simulator** via xcrun/xcodebuild
7. **Install packages** via pip3/npm (these go to system package dirs, that's fine)
8. **Copy FROM ~/Downloads** into the project (use guardrails.safe_download_move)
9. **Query APIs** (curl, Python requests, etc.)
10. **Manage crontab** (crontab command)

## What You CANNOT Do

1. **Write to ~/Desktop** - BLOCKED
2. **Write to ~/Documents** (except our project subfolder) - BLOCKED
3. **Write to ~/Pictures, ~/Music, ~/Movies** - BLOCKED
4. **Write to ~/.ssh, ~/.aws, ~/.gnupg** - BLOCKED
5. **Write to ~/.zshrc, ~/.bashrc, ~/.gitconfig** - BLOCKED
6. **Write to ~/Library** - BLOCKED
7. **Write to /System, /Library, /usr, /bin, /etc, /var** - BLOCKED
8. **Delete CLAUDE.md, LEDGER/, FINANCIALS/, SECRETS/, XLSX files** - BLOCKED
9. **Run rm -rf /, fork bombs, dd, diskutil erase** - BLOCKED
10. **Browse/modify files in other project folders** - BLOCKED
11. **Access other users' directories** - BLOCKED

## How To Use Guardrails In Scripts

### Python scripts:
```python
from guardrails import GuardRails
gr = GuardRails()
gr.safe_write("path/in/project.txt", content)  # Safe
gr.safe_delete("path/in/project.txt")           # Safe, auto-backed up
gr.verify_path("/some/external/path", "write")  # Raises if outside project
```

### Bash scripts:
```bash
source "$BASE_DIR/AUTOMATIONS/guardrails_wrapper.sh"
safe_rm "file_in_project.txt"    # Safe, auto-backed up
safe_mv "src.txt" "dst.txt"     # Safe
verify_path "/some/path" "write" # Returns 1 if outside project
```

## Backup System

- Full backup: `python3 AUTOMATIONS/backup_system.py --full`
- Incremental: `python3 AUTOMATIONS/backup_system.py --incremental`
- Restore: `python3 AUTOMATIONS/backup_system.py --restore <id>`
- Backups stored at: `~/PRINTMAXX_BACKUPS/` (outside project for safety)
- Auto-backup runs nightly at 9:15 PM and before overnight runner
- Full backup runs weekly (Sunday 3 AM)

## Safety Test

Run anytime to verify all guardrails are working:
```bash
python3 AUTOMATIONS/guardrails.py --test
```
Must show: `ALL TESTS PASSED`

## Downloads Folder Policy

**~/Downloads is READ-ONLY and ONLY when explicitly moving a specific file INTO the project.**
- NEVER browse ~/Downloads
- NEVER delete files in ~/Downloads
- NEVER write to ~/Downloads
- ONLY access a specific file path in ~/Downloads if the user explicitly says "move X from Downloads"
- If a script downloads something, it downloads directly to the project folder, NOT to ~/Downloads

## Autonomous Loop Safety

**Prevents runaway autonomous loops from causing damage:**
1. **All file operations MUST validate paths** against the project root before executing
2. **No recursive deletion** of any directory containing more than 100 files without explicit user confirmation
3. **Lock files** prevent double-runs of pipeline, orchestrator, and batch processes
4. **Timeouts on everything**: 30 min per task, 3 hours per orchestration run, 10 min per pipeline cycle
5. **Append-only logging** — logs are NEVER deleted, only appended to
6. **No `os.system()` calls** with user-controllable input (command injection prevention)
7. **Every destructive operation** (delete, overwrite, rmtree) MUST first verify the target path starts with the project root
8. **Cron jobs** only run scripts inside AUTOMATIONS/ — no external paths
9. **Background processes** are tracked by PID in active-tasks.md for manual kill if needed

## Path Validation (Required in ALL New Scripts)

Every new Python script that writes files MUST use this pattern:
```python
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # or appropriate level
def safe_path(target: Path) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved
```

## Why This Exists

The user said: "i dont want my laptop bricked or lost data i havent backed up. dont want u working directly in folders other than printmaxx folder. u can activate like certain apps like browsers and system stuff but dont like actively go into folders and fuck with files and data other than the printmaxx folder"

The user also said: "i dont want my files outside of this specific project folder affected read or written or deleted. i dont want accidents and losing unbacked up data. no touching downloads folder. i dont want claude code accident autonomous hard drive wipe or anything from faulty autonomous loop"

This is permanent. No exceptions. No workarounds.
