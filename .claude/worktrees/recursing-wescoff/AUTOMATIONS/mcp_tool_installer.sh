#!/bin/bash
# ============================================================
# MCP Tool Installer
# ============================================================
# Installs high-value MCP tools identified in the alpha scan.
# Estimated value: $2,392/mo in automation capability unlocked.
#
# Tools identified from AUDIT/ALPHA_INTEGRATION_GAP_ANALYSIS.md:
# - Playwright MCP (browser automation from Claude)
# - Firecrawl (web scraping)
# - Google Sheets API (CSV management)
# - Notion API (knowledge base)
# - Buffer API (content posting)
#
# Usage:
#   bash AUTOMATIONS/mcp_tool_installer.sh              # Install all
#   bash AUTOMATIONS/mcp_tool_installer.sh --verify     # Verify only
#   bash AUTOMATIONS/mcp_tool_installer.sh --dry-run    # Preview only
#
# ============================================================

set -euo pipefail

BASE_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
LOG_DIR="$BASE_DIR/AUTOMATIONS/logs"
LOG_FILE="$LOG_DIR/mcp_tool_installer.log"

mkdir -p "$LOG_DIR"

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$msg"
    echo "$msg" >> "$LOG_FILE"
}

DRY_RUN=false
VERIFY_ONLY=false

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --verify) VERIFY_ONLY=true ;;
    esac
done

log "=== MCP Tool Installer ==="
log ""

# Check prerequisites
check_prereqs() {
    local missing=0

    if ! command -v npx &>/dev/null; then
        log "ERROR: npx not found. Install Node.js first."
        missing=1
    fi

    if ! command -v node &>/dev/null; then
        log "ERROR: node not found. Install Node.js first."
        missing=1
    fi

    if ! command -v claude &>/dev/null; then
        log "WARNING: claude CLI not found in PATH. MCP tools need Claude CLI."
    fi

    if [ $missing -eq 1 ]; then
        log "Fix prerequisites before installing MCP tools."
        exit 1
    fi

    log "Prerequisites OK (node $(node --version), npx available)"
}

# MCP tools to install with descriptions
# Format: "package_name|display_name|description|monthly_value"
MCP_TOOLS=(
    "@anthropic-ai/mcp-server-playwright|Playwright MCP|Browser automation from Claude context. Automate signups, form fills, screenshots.|800"
    "@anthropic-ai/mcp-server-filesystem|Filesystem MCP|Direct file operations from Claude. Enhanced file management.|200"
    "firecrawl-mcp|Firecrawl MCP|Structured web scraping from Claude. Extract data from any page.|500"
    "@anthropic-ai/mcp-server-fetch|Fetch MCP|HTTP requests from Claude context. API calls, webhooks.|300"
    "@anthropic-ai/mcp-server-memory|Memory MCP|Persistent memory for Claude across sessions.|192"
)

# Additional tools that need API keys (install but note key requirement)
MCP_TOOLS_WITH_KEYS=(
    "google-sheets-mcp|Google Sheets MCP|Replace manual CSV management with Sheets API. Needs GOOGLE_API_KEY.|300"
    "notion-mcp|Notion MCP|Knowledge base management from Claude. Needs NOTION_TOKEN.|200"
)

install_tool() {
    local package=$1
    local display_name=$2
    local description=$3
    local value=$4

    log "  Installing: $display_name ($package)"
    log "    Value: ~\$$value/mo"
    log "    Purpose: $description"

    if $DRY_RUN; then
        log "    [DRY RUN - skipping install]"
        return 0
    fi

    # Try to install via npx
    if npx -y "$package" --help &>/dev/null 2>&1; then
        log "    STATUS: OK (package accessible)"
        return 0
    fi

    # Try npm install globally as fallback
    if npm install -g "$package" &>/dev/null 2>&1; then
        log "    STATUS: OK (installed globally)"
        return 0
    fi

    log "    STATUS: FAILED (may need manual install or API key)"
    return 1
}

verify_tool() {
    local package=$1
    local display_name=$2

    if npx -y "$package" --help &>/dev/null 2>&1; then
        log "  OK: $display_name"
        return 0
    elif command -v "${package##*/}" &>/dev/null 2>&1; then
        log "  OK: $display_name (found in PATH)"
        return 0
    else
        log "  MISSING: $display_name ($package)"
        return 1
    fi
}

# Check Claude MCP config file
check_mcp_config() {
    local config_file="$HOME/.claude/claude_desktop_config.json"
    if [ -f "$config_file" ]; then
        log "MCP config file exists: $config_file"
        return 0
    fi

    local alt_config="$HOME/.config/claude/claude_desktop_config.json"
    if [ -f "$alt_config" ]; then
        log "MCP config file exists: $alt_config"
        return 0
    fi

    log "WARNING: No MCP config file found."
    log "  MCP tools need to be configured in Claude's settings."
    log "  See: https://docs.anthropic.com/en/docs/agents-and-tools/mcp"
    return 1
}

generate_mcp_config() {
    log ""
    log "=== MCP Configuration Template ==="
    log "Add the following to your Claude MCP config (~/.claude/claude_desktop_config.json):"
    log ""

    cat <<'CONFIG_EOF'
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-playwright"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-filesystem", "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-fetch"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-memory"]
    }
  }
}
CONFIG_EOF

    log ""
    log "Note: firecrawl-mcp, google-sheets-mcp, and notion-mcp need API keys."
    log "Add them to the config once you have the keys."
}

# Main execution
check_prereqs

if $VERIFY_ONLY; then
    log "=== Verification Mode ==="
    ok=0
    fail=0
    for tool_spec in "${MCP_TOOLS[@]}"; do
        IFS='|' read -r package display_name description value <<< "$tool_spec"
        if verify_tool "$package" "$display_name"; then
            ok=$((ok + 1))
        else
            fail=$((fail + 1))
        fi
    done
    log ""
    log "Verified: $ok OK, $fail missing"
    check_mcp_config
    exit 0
fi

log ""
log "--- Core MCP Tools (no API keys needed) ---"
installed=0
failed=0
total_value=0

for tool_spec in "${MCP_TOOLS[@]}"; do
    IFS='|' read -r package display_name description value <<< "$tool_spec"
    if install_tool "$package" "$display_name" "$description" "$value"; then
        installed=$((installed + 1))
        total_value=$((total_value + value))
    else
        failed=$((failed + 1))
    fi
    log ""
done

log ""
log "--- MCP Tools Requiring API Keys (info only) ---"
for tool_spec in "${MCP_TOOLS_WITH_KEYS[@]}"; do
    IFS='|' read -r package display_name description value <<< "$tool_spec"
    log "  NEEDS KEY: $display_name"
    log "    Package: $package"
    log "    Value: ~\$$value/mo"
    log "    Setup: Install package, then add API key to MCP config"
    log ""
done

log "=== Summary ==="
log "  Installed: $installed"
log "  Failed: $failed"
log "  Estimated monthly value unlocked: ~\$$total_value/mo"
log ""

check_mcp_config
generate_mcp_config

if $DRY_RUN; then
    log ""
    log "[DRY RUN - no packages were actually installed]"
fi

log ""
log "MCP Tool Installer complete."
log "Next step: Configure tools in Claude's MCP settings."
