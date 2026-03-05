#!/bin/bash
# PRINTMAXX Weekly System Clone
# ===============================
# Creates a FULL mirror clone of the entire project at a separate location.
# Purges the previous clone BEFORE creating the new one (no storage stacking).
# This is the nuclear safety net - if main gets corrupted, clone is clean.
#
# USAGE:
#   bash AUTOMATIONS/weekly_system_clone.sh              # Full clone
#   bash AUTOMATIONS/weekly_system_clone.sh --status     # Show clone info
#   bash AUTOMATIONS/weekly_system_clone.sh --verify     # Verify clone integrity
#   bash AUTOMATIONS/weekly_system_clone.sh --restore    # Restore main from clone
#
# SCHEDULE: Sunday 4 AM via cron (after full backup at 3 AM)
# LOCATION: ~/PRINTMAXX_WEEKLY_CLONE/ (separate from ~/PRINTMAXX_BACKUPS/)

set -euo pipefail

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
CLONE_DIR="/Users/macbookpro/PRINTMAXX_WEEKLY_CLONE"
CLONE_TARGET="$CLONE_DIR/PRINTMAXX_STARTER_KITttttt"
LOG_DIR="$BASE/AUTOMATIONS/logs"
LOG_FILE="$LOG_DIR/weekly_clone_$(date +%Y%m%d_%H%M%S).log"
LOCK_FILE="$LOG_DIR/weekly_clone.lock"
META_FILE="$CLONE_DIR/_clone_meta.json"

mkdir -p "$LOG_DIR"

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$msg"
    echo "$msg" >> "$LOG_FILE"
}

error_exit() {
    log "ERROR: $1"
    rm -f "$LOCK_FILE"
    exit 1
}

# Lock to prevent double-runs
if [ -f "$LOCK_FILE" ]; then
    pid=$(cat "$LOCK_FILE" 2>/dev/null || echo "")
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
        echo "Clone already running (PID $pid). Exiting."
        exit 0
    fi
    log "Stale lock file found. Removing."
    rm -f "$LOCK_FILE"
fi
echo $$ > "$LOCK_FILE"
trap 'rm -f "$LOCK_FILE"' EXIT

# Disk space check (need at least 5GB free)
check_disk() {
    local avail_kb
    avail_kb=$(df -k "$HOME" | tail -1 | awk '{print $4}')
    local avail_gb=$((avail_kb / 1024 / 1024))
    if [ "$avail_gb" -lt 5 ]; then
        error_exit "Only ${avail_gb}GB free. Need at least 5GB for clone. Aborting."
    fi
    log "Disk check: ${avail_gb}GB available. OK."
}

# Get project size (excluding heavy dirs)
get_project_size() {
    du -sh "$BASE" --exclude="node_modules" --exclude=".git" --exclude="__pycache__" --exclude=".next" --exclude="venv" 2>/dev/null | awk '{print $1}' || \
    du -sh "$BASE" 2>/dev/null | awk '{print $1}' || echo "unknown"
}

# Rsync exclusions
RSYNC_EXCLUDES=(
    --exclude='node_modules'
    --exclude='.git'
    --exclude='__pycache__'
    --exclude='.next'
    --exclude='.vercel'
    --exclude='venv'
    --exclude='.venv'
    --exclude='dist'
    --exclude='.DS_Store'
    --exclude='.Trash'
    --exclude='app factory'
    --exclude='cal ai'
    --exclude='*.pyc'
    --exclude='*.pyo'
    --exclude='*.so'
    --exclude='*.dylib'
    --exclude='.claude/worktrees'
)

do_clone() {
    log "========== WEEKLY SYSTEM CLONE START =========="
    check_disk

    # Step 1: Git commit any uncommitted changes in main first
    log "Step 1: Safety git commit before clone..."
    cd "$BASE"
    if git diff --quiet 2>/dev/null && git diff --cached --quiet 2>/dev/null; then
        log "  No uncommitted changes. Skipping git commit."
    else
        git add -A 2>/dev/null || true
        git commit -m "Pre-clone safety commit $(date +%Y-%m-%d_%H:%M)" 2>/dev/null || log "  Git commit failed (non-fatal)"
        log "  Safety commit done."
    fi

    # Step 2: Record old clone size for comparison
    local old_size="none"
    if [ -d "$CLONE_TARGET" ]; then
        old_size=$(du -sh "$CLONE_TARGET" 2>/dev/null | awk '{print $1}' || echo "unknown")
        log "Step 2: Previous clone exists (${old_size}). Will purge before creating new."
    else
        log "Step 2: No previous clone found. Fresh clone."
    fi

    # Step 3: PURGE old clone (the user's requirement: purge before new)
    if [ -d "$CLONE_DIR" ]; then
        log "Step 3: Purging old clone at $CLONE_DIR..."
        rm -rf "$CLONE_DIR"
        log "  Old clone purged."
    fi

    # Step 4: Create fresh clone directory
    mkdir -p "$CLONE_DIR"

    # Step 5: Rsync the full project
    log "Step 4: Cloning project via rsync..."
    local start_time=$(date +%s)

    rsync -a --delete \
        "${RSYNC_EXCLUDES[@]}" \
        "$BASE/" "$CLONE_TARGET/" \
        2>> "$LOG_FILE"

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    local new_size=$(du -sh "$CLONE_TARGET" 2>/dev/null | awk '{print $1}' || echo "unknown")

    log "  Clone complete in ${duration}s. Size: ${new_size}"

    # Step 6: Write metadata
    local file_count
    file_count=$(find "$CLONE_TARGET" -type f 2>/dev/null | wc -l | tr -d ' ')

    cat > "$META_FILE" << METAEOF
{
    "clone_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "clone_date_local": "$(date '+%Y-%m-%d %H:%M:%S')",
    "source": "$BASE",
    "destination": "$CLONE_TARGET",
    "size": "$new_size",
    "previous_size": "$old_size",
    "file_count": $file_count,
    "duration_seconds": $duration,
    "git_branch": "$(cd "$BASE" && git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')",
    "git_commit": "$(cd "$BASE" && git rev-parse --short HEAD 2>/dev/null || echo 'unknown')",
    "git_commit_full": "$(cd "$BASE" && git rev-parse HEAD 2>/dev/null || echo 'unknown')"
}
METAEOF

    log "Step 5: Metadata written to $META_FILE"

    # Step 7: Verify clone integrity (spot check)
    log "Step 6: Verifying clone integrity..."
    local verify_ok=true
    for check_file in "AUTOMATIONS/printmaxx_desktop.py" "OPS/HEARTBEAT.md" "LEDGER/ALPHA_STAGING.csv"; do
        if [ -f "$BASE/$check_file" ] && [ ! -f "$CLONE_TARGET/$check_file" ]; then
            log "  WARNING: $check_file missing from clone!"
            verify_ok=false
        fi
    done

    if [ "$verify_ok" = true ]; then
        log "  Integrity check: PASSED"
    else
        log "  Integrity check: WARNINGS (some files missing)"
    fi

    # Step 8: macOS notification
    osascript -e "display notification \"Weekly clone complete. ${new_size}, ${file_count} files, ${duration}s\" with title \"PRINTMAXX Clone\" sound name \"Glass\"" 2>/dev/null || true

    log "========== WEEKLY SYSTEM CLONE COMPLETE =========="
    log "Clone at: $CLONE_TARGET"
    log "Files: $file_count | Size: $new_size | Duration: ${duration}s"
    log "To restore: bash AUTOMATIONS/weekly_system_clone.sh --restore"
}

do_status() {
    if [ ! -f "$META_FILE" ]; then
        echo "No clone found. Run: bash AUTOMATIONS/weekly_system_clone.sh"
        exit 0
    fi

    echo "=== PRINTMAXX WEEKLY CLONE STATUS ==="
    cat "$META_FILE" | python3 -m json.tool 2>/dev/null || cat "$META_FILE"
    echo ""

    if [ -d "$CLONE_TARGET" ]; then
        local current_size
        current_size=$(du -sh "$CLONE_TARGET" 2>/dev/null | awk '{print $1}')
        echo "Current clone size: $current_size"
        echo "Clone location: $CLONE_TARGET"
    else
        echo "WARNING: Clone directory missing!"
    fi
}

do_verify() {
    if [ ! -d "$CLONE_TARGET" ]; then
        echo "No clone found. Nothing to verify."
        exit 1
    fi

    echo "=== VERIFYING CLONE INTEGRITY ==="
    local errors=0

    # Check key directories
    for dir in AUTOMATIONS OPS LEDGER CONTENT PRODUCTS MONEY_METHODS FINANCIALS; do
        if [ -d "$BASE/$dir" ] && [ ! -d "$CLONE_TARGET/$dir" ]; then
            echo "MISSING DIR: $dir"
            errors=$((errors + 1))
        fi
    done

    # Check key files
    for f in ".claude/CLAUDE.md" "AUTOMATIONS/printmaxx_desktop.py" "OPS/PERSISTENT_TASK_TRACKER.md"; do
        if [ -f "$BASE/$f" ] && [ ! -f "$CLONE_TARGET/$f" ]; then
            echo "MISSING FILE: $f"
            errors=$((errors + 1))
        fi
    done

    # Compare file counts
    local main_count clone_count
    main_count=$(find "$BASE" -type f -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/__pycache__/*" -not -path "*/.next/*" 2>/dev/null | wc -l | tr -d ' ')
    clone_count=$(find "$CLONE_TARGET" -type f 2>/dev/null | wc -l | tr -d ' ')

    echo "Main files: $main_count"
    echo "Clone files: $clone_count"

    if [ "$errors" -eq 0 ]; then
        echo "VERIFICATION: PASSED"
    else
        echo "VERIFICATION: $errors ISSUES FOUND"
    fi
}

do_restore() {
    if [ ! -d "$CLONE_TARGET" ]; then
        echo "ERROR: No clone found at $CLONE_TARGET"
        echo "Cannot restore. Use backup_system.py instead."
        exit 1
    fi

    echo "=== RESTORE FROM WEEKLY CLONE ==="
    echo ""
    echo "WARNING: This will OVERWRITE the main project with the clone."
    echo "Source: $CLONE_TARGET"
    echo "Target: $BASE"
    echo ""
    echo "Clone metadata:"
    cat "$META_FILE" 2>/dev/null || echo "(no metadata)"
    echo ""
    echo "To proceed, run:"
    echo "  rsync -a --delete '$CLONE_TARGET/' '$BASE/'"
    echo ""
    echo "For safety, this script does NOT auto-restore."
    echo "Copy and run the rsync command above manually."
}

# Main
case "${1:-}" in
    --status|-s)
        do_status
        ;;
    --verify|-v)
        do_verify
        ;;
    --restore|-r)
        do_restore
        ;;
    *)
        do_clone
        ;;
esac
