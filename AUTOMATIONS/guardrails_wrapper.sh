#!/bin/bash
# PRINTMAXX Shell Guardrails Wrapper
# Source this in any bash script for safety:
#   source "$(dirname "$0")/guardrails_wrapper.sh"
#
# Or use the safe_ prefixed functions:
#   safe_rm "file_in_project.txt"
#   safe_mv "src.txt" "dst.txt"
#   safe_cp "src.txt" "dst.txt"
#   safe_write "file.txt" "content"
#   verify_path "/some/path"
#   create_backup "reason"

set -euo pipefail

# ============================================================
# CONFIGURATION
# ============================================================

PRINTMAXX_ROOT="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
GUARDRAILS_LOG="$PRINTMAXX_ROOT/.guardrails/shell_operations.log"
BACKUP_DIR="$HOME/PRINTMAXX_BACKUPS"

# Ensure log directory exists
mkdir -p "$(dirname "$GUARDRAILS_LOG")"

# ============================================================
# LOGGING
# ============================================================

guardrail_log() {
    local level="$1"
    local msg="$2"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] [PID:$$] $msg" >> "$GUARDRAILS_LOG"
    if [ "$level" = "BLOCKED" ] || [ "$level" = "ERROR" ]; then
        echo "[GUARDRAIL] $level: $msg" >&2
    fi
}

# ============================================================
# PATH VERIFICATION (THE CORE SAFETY FUNCTION)
# ============================================================

verify_path() {
    local path="$1"
    local operation="${2:-access}"

    # Resolve to absolute path
    local resolved
    if [ -e "$path" ]; then
        resolved=$(cd "$(dirname "$path")" && pwd)/$(basename "$path")
    else
        # For non-existent paths, resolve the parent
        local parent_dir
        parent_dir=$(dirname "$path")
        if [ -d "$parent_dir" ]; then
            resolved=$(cd "$parent_dir" && pwd)/$(basename "$path")
        else
            resolved="$path"
        fi
    fi

    # Remove trailing slashes
    resolved="${resolved%/}"

    # CHECK 1: Must be within PRINTMAXX project root
    case "$resolved" in
        "$PRINTMAXX_ROOT"*)
            ;;
        /tmp/*)
            # Allow temp files
            ;;
        *)
            guardrail_log "BLOCKED" "$operation on '$resolved' - OUTSIDE project root"
            echo "GUARDRAIL BLOCKED: '$operation' on '$resolved' is outside PRINTMAXX folder" >&2
            return 1
            ;;
    esac

    # CHECK 2: Don't allow operations on system paths even via symlinks
    local real_path
    if [ -e "$resolved" ]; then
        real_path=$(python3 -c "import os; print(os.path.realpath('$resolved'))" 2>/dev/null || echo "$resolved")
    else
        real_path="$resolved"
    fi

    case "$real_path" in
        /System/*|/Library/*|/usr/*|/bin/*|/sbin/*|/etc/*|/var/*|/private/*)
            guardrail_log "BLOCKED" "$operation on '$real_path' - SYSTEM PATH"
            echo "GUARDRAIL BLOCKED: '$real_path' is a system path" >&2
            return 1
            ;;
    esac

    # CHECK 3: Don't touch user directories outside project
    local home_dir
    home_dir=$(eval echo "~")
    case "$real_path" in
        "$home_dir/Desktop"*|"$home_dir/Documents"*|"$home_dir/Pictures"*|"$home_dir/Music"*|"$home_dir/Movies"*)
            # Allow ONLY our specific project subdirectory
            case "$real_path" in
                "$PRINTMAXX_ROOT"*)
                    ;;
                *)
                    guardrail_log "BLOCKED" "$operation on '$real_path' - USER DIRECTORY"
                    echo "GUARDRAIL BLOCKED: '$real_path' is outside PRINTMAXX folder" >&2
                    return 1
                    ;;
            esac
            ;;
        "$home_dir/.ssh"*|"$home_dir/.gnupg"*|"$home_dir/.aws"*|"$home_dir/.config"*)
            guardrail_log "BLOCKED" "$operation on '$real_path' - SENSITIVE DOT DIR"
            echo "GUARDRAIL BLOCKED: '$real_path' is a sensitive system directory" >&2
            return 1
            ;;
    esac

    # CHECK 4: Protected project files (can't delete)
    if [ "$operation" = "delete" ]; then
        local rel_path
        rel_path="${resolved#$PRINTMAXX_ROOT/}"
        case "$rel_path" in
            "CLAUDE.md"|".claude/"*|"LEDGER/"*|"FINANCIALS/"*|"SECRETS/"*|"PRINTMAXX_MASTER_OPS.xlsx")
                guardrail_log "BLOCKED" "delete of protected path '$rel_path'"
                echo "GUARDRAIL BLOCKED: Cannot delete protected file '$rel_path'" >&2
                return 1
                ;;
        esac
    fi

    guardrail_log "OK" "$operation on '$resolved'"
    return 0
}

# ============================================================
# SAFE FILE OPERATIONS
# ============================================================

safe_rm() {
    local target="$1"

    if ! verify_path "$target" "delete"; then
        return 1
    fi

    # Backup before delete
    if [ -e "$target" ]; then
        local backup_dest="$PRINTMAXX_ROOT/.guardrails/file_backups/$(date +%Y%m%d_%H%M%S)_pre_delete_$(basename "$target")"
        mkdir -p "$(dirname "$backup_dest")"
        cp -a "$target" "$backup_dest" 2>/dev/null || true
        guardrail_log "BACKUP" "Backed up '$target' to '$backup_dest'"
    fi

    rm -rf "$target"
    guardrail_log "DELETE" "Deleted '$target'"
}

safe_mv() {
    local src="$1"
    local dst="$2"

    if ! verify_path "$src" "move"; then
        return 1
    fi
    if ! verify_path "$dst" "write"; then
        return 1
    fi

    # Backup source before move
    if [ -e "$src" ]; then
        local backup_dest="$PRINTMAXX_ROOT/.guardrails/file_backups/$(date +%Y%m%d_%H%M%S)_pre_move_$(basename "$src")"
        mkdir -p "$(dirname "$backup_dest")"
        cp -a "$src" "$backup_dest" 2>/dev/null || true
    fi

    mkdir -p "$(dirname "$dst")"
    mv "$src" "$dst"
    guardrail_log "MOVE" "'$src' -> '$dst'"
}

safe_cp() {
    local src="$1"
    local dst="$2"

    # Source can be read from anywhere (for downloads etc)
    if ! verify_path "$dst" "write"; then
        return 1
    fi

    mkdir -p "$(dirname "$dst")"
    cp -a "$src" "$dst"
    guardrail_log "COPY" "'$src' -> '$dst'"
}

safe_write() {
    local target="$1"
    local content="$2"

    if ! verify_path "$target" "write"; then
        return 1
    fi

    # Backup existing file
    if [ -e "$target" ]; then
        local backup_dest="$PRINTMAXX_ROOT/.guardrails/file_backups/$(date +%Y%m%d_%H%M%S)_pre_write_$(basename "$target")"
        mkdir -p "$(dirname "$backup_dest")"
        cp -a "$target" "$backup_dest" 2>/dev/null || true
    fi

    mkdir -p "$(dirname "$target")"
    echo "$content" > "$target"
    guardrail_log "WRITE" "Wrote to '$target'"
}

# ============================================================
# BACKUP HELPERS
# ============================================================

create_backup() {
    local reason="${1:-manual}"
    local python="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"

    guardrail_log "BACKUP" "Creating backup: $reason"

    if [ -f "$PRINTMAXX_ROOT/AUTOMATIONS/backup_system.py" ]; then
        $python "$PRINTMAXX_ROOT/AUTOMATIONS/backup_system.py" --auto
    else
        # Fallback: simple rsync backup
        local backup_id="shell_$(date +%Y%m%d_%H%M%S)_${reason}"
        local backup_path="$BACKUP_DIR/$backup_id"
        mkdir -p "$backup_path"

        rsync -a \
            --exclude='node_modules' \
            --exclude='.git' \
            --exclude='__pycache__' \
            --exclude='.guardrails' \
            --exclude='.next' \
            --exclude='dist' \
            --exclude='venv' \
            --exclude='app factory' \
            "$PRINTMAXX_ROOT/" "$backup_path/"

        guardrail_log "BACKUP" "Created fallback backup at $backup_path"
        echo "Backup created: $backup_path"
    fi
}

# ============================================================
# COMMAND VALIDATION
# ============================================================

validate_command() {
    local cmd="$1"

    # Block catastrophic commands
    case "$cmd" in
        *"rm -rf /"*|*"rm -rf ~"*|*"rm -rf \$HOME"*)
            guardrail_log "BLOCKED" "Catastrophic rm command: $cmd"
            echo "GUARDRAIL BLOCKED: Catastrophic rm command" >&2
            return 1
            ;;
        *"mkfs"*|*"dd if="*|*"diskutil erase"*|*"diskutil partitionDisk"*)
            guardrail_log "BLOCKED" "Disk-destroying command: $cmd"
            echo "GUARDRAIL BLOCKED: Disk-destroying command" >&2
            return 1
            ;;
        *"chmod -R 777 /"*|*"chown -R"*|*"sudo rm"*)
            guardrail_log "BLOCKED" "System-modifying command: $cmd"
            echo "GUARDRAIL BLOCKED: System-modifying command" >&2
            return 1
            ;;
    esac

    guardrail_log "OK" "Command validated: ${cmd:0:80}"
    return 0
}

# ============================================================
# INITIALIZATION
# ============================================================

# Auto-verify we're running from the right directory
_guardrails_init() {
    local cwd
    cwd=$(pwd)

    # Warn if not in project directory
    case "$cwd" in
        "$PRINTMAXX_ROOT"*)
            ;;
        *)
            guardrail_log "WARNING" "Script running from outside project: $cwd"
            ;;
    esac

    guardrail_log "INIT" "Shell guardrails loaded (PID: $$, CWD: $cwd)"
}

_guardrails_init
