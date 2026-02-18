#!/bin/bash
# ============================================================
# Broken LaunchD Agent Cleaner
# ============================================================
# All 7 com.printmaxx.* launchd agents are BROKEN on macOS Sequoia
# with "Operation not permitted" errors. Crontab covers all the
# same jobs and is working fine.
#
# This script safely unloads all broken agents.
#
# Usage:
#   bash AUTOMATIONS/cleanup_broken_launchd.sh              # Unload all
#   bash AUTOMATIONS/cleanup_broken_launchd.sh --dry-run    # Preview only
#   bash AUTOMATIONS/cleanup_broken_launchd.sh --status     # Check status
#
# ============================================================

set -euo pipefail

BASE_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
LOG_DIR="$BASE_DIR/AUTOMATIONS/logs"
LOG_FILE="$LOG_DIR/cleanup_launchd.log"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
ARCHIVE_DIR="$BASE_DIR/AUTOMATIONS/_archive/broken_launchd"

mkdir -p "$LOG_DIR"

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$msg"
    echo "$msg" >> "$LOG_FILE"
}

DRY_RUN=false
STATUS_ONLY=false

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --status) STATUS_ONLY=true ;;
    esac
done

# All known broken PrintMAXX launchd agents
AGENTS=(
    "com.printmaxx.morning-sync"
    "com.printmaxx.content-gen"
    "com.printmaxx.evening-digest"
    "com.printmaxx.nightly-backup"
    "com.printmaxx.overnight-sprint"
    "com.printmaxx.weekly-tasks"
    "com.printmaxx.monthly-tasks"
)

if $STATUS_ONLY; then
    log "=== LaunchD Agent Status ==="
    for agent in "${AGENTS[@]}"; do
        plist="$LAUNCH_AGENTS_DIR/${agent}.plist"
        if [ -f "$plist" ]; then
            # Check if loaded
            if launchctl list 2>/dev/null | grep -q "$agent"; then
                log "  LOADED (BROKEN): $agent"
            else
                log "  UNLOADED: $agent (plist exists but not loaded)"
            fi
        else
            log "  REMOVED: $agent (no plist)"
        fi
    done
    exit 0
fi

log "=== Broken LaunchD Agent Cleanup ==="
log "Reason: All 7 agents fail with 'Operation not permitted' on macOS Sequoia"
log "Impact: NONE -- crontab covers all the same jobs and is working"
log ""

if $DRY_RUN; then
    log "[DRY RUN MODE - no changes will be made]"
    log ""
fi

# Create archive directory for plist backups
if ! $DRY_RUN; then
    mkdir -p "$ARCHIVE_DIR"
fi

unloaded=0
archived=0
skipped=0

for agent in "${AGENTS[@]}"; do
    plist="$LAUNCH_AGENTS_DIR/${agent}.plist"

    if [ ! -f "$plist" ]; then
        log "  SKIP: $agent (plist not found)"
        skipped=$((skipped + 1))
        continue
    fi

    # Unload if currently loaded
    if launchctl list 2>/dev/null | grep -q "$agent"; then
        log "  UNLOADING: $agent"
        if ! $DRY_RUN; then
            launchctl unload "$plist" 2>/dev/null || true
            unloaded=$((unloaded + 1))
        fi
    else
        log "  NOT LOADED: $agent (will still archive plist)"
    fi

    # Archive the plist file (move out of LaunchAgents)
    log "  ARCHIVING: $plist -> $ARCHIVE_DIR/"
    if ! $DRY_RUN; then
        cp "$plist" "$ARCHIVE_DIR/" 2>/dev/null || true
        rm "$plist" 2>/dev/null || true
        archived=$((archived + 1))
    fi
done

log ""
log "=== Summary ==="
log "  Unloaded: $unloaded"
log "  Archived: $archived"
log "  Skipped: $skipped"
log "  Archive location: $ARCHIVE_DIR/"
log ""
log "To restore (if ever needed):"
log "  cp $ARCHIVE_DIR/*.plist ~/Library/LaunchAgents/"
log "  launchctl load ~/Library/LaunchAgents/com.printmaxx.*.plist"
log ""
log "Note: Restoration will still fail unless Full Disk Access"
log "is granted to /bin/bash in System Preferences."

if $DRY_RUN; then
    log ""
    log "[DRY RUN - no changes were made]"
fi

log "Cleanup complete."
