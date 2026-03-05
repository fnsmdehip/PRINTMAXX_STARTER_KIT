#!/bin/bash
# PRINTMAXX Claude Subconscious Setup
# ====================================
# Wires letta-ai/claude-subconscious for persistent memory across interactive sessions.
# Your cron-driven autonomous sessions (schedule_claude.sh) are unaffected.
#
# REQUIREMENTS:
#   1. Letta API key from https://app.letta.com (free tier available)
#   2. Node.js >= 18 (you have v25.6.1)
#   3. Claude Code installed
#
# Usage:
#   bash AUTOMATIONS/setup_subconscious.sh           # Install + enable
#   bash AUTOMATIONS/setup_subconscious.sh --status   # Check if configured
#   bash AUTOMATIONS/setup_subconscious.sh --disable   # Disable hooks

set -uo pipefail

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
INSTALL_DIR="$HOME/.claude/plugins/cache/claude-subconscious"
REPO_URL="https://github.com/letta-ai/claude-subconscious.git"

log() { echo "[subconscious] $1"; }

cmd_status() {
    log "Checking claude-subconscious status..."

    if [ -d "$INSTALL_DIR" ]; then
        log "Installed at: $INSTALL_DIR"
    else
        log "NOT installed"
    fi

    if [ -n "${LETTA_API_KEY:-}" ]; then
        log "LETTA_API_KEY: set (${#LETTA_API_KEY} chars)"
    else
        log "LETTA_API_KEY: NOT SET"
        log "  Get one at: https://app.letta.com"
        log "  Then add to ~/.zshrc: export LETTA_API_KEY=\"your-key\""
    fi

    if [ -f "$HOME/.letta/claude-subconscious/config.json" ]; then
        log "Agent config: exists"
    else
        log "Agent config: not yet created (auto-creates on first run)"
    fi
}

cmd_install() {
    # Check for API key
    if [ -z "${LETTA_API_KEY:-}" ]; then
        log ""
        log "LETTA_API_KEY not set. Two steps needed:"
        log ""
        log "  1. Get a free API key at: https://app.letta.com"
        log "  2. Add to your shell:"
        log "     echo 'export LETTA_API_KEY=\"your-key-here\"' >> ~/.zshrc"
        log "     source ~/.zshrc"
        log ""
        log "  3. Then run this script again."
        log ""
        exit 1
    fi

    # Clone or update
    if [ -d "$INSTALL_DIR" ]; then
        log "Updating existing installation..."
        cd "$INSTALL_DIR" && git pull 2>/dev/null || true
    else
        log "Cloning claude-subconscious..."
        git clone "$REPO_URL" "$INSTALL_DIR" 2>&1
    fi

    # Install deps
    log "Installing dependencies..."
    cd "$INSTALL_DIR" && npm install 2>&1 | tail -3

    log ""
    log "Installation complete at: $INSTALL_DIR"
    log ""
    log "To activate, run this IN Claude Code:"
    log "  /plugin enable $INSTALL_DIR"
    log ""
    log "Or install from marketplace (if available):"
    log "  /plugin marketplace add letta-ai/claude-subconscious"
    log "  /plugin install claude-subconscious@claude-subconscious"
    log ""
    log "The plugin activates 4 hooks:"
    log "  SessionStart     - Initializes Letta conversation"
    log "  UserPromptSubmit - Injects memory before each prompt"
    log "  PreToolUse       - Mid-workflow context updates"
    log "  Stop             - Sends session transcript to Letta (background)"
    log ""
    log "Mode options (set LETTA_MODE env var):"
    log "  whisper (default) - Messages only, lightweight"
    log "  full              - Memory blocks + messages"
    log "  off               - Temporarily disable"
}

cmd_disable() {
    log "To disable, run in Claude Code:"
    log "  /plugin disable claude-subconscious"
    log ""
    log "Or set: export LETTA_MODE=off"
}

case "${1:-}" in
    --status)  cmd_status ;;
    --disable) cmd_disable ;;
    *)         cmd_install ;;
esac
