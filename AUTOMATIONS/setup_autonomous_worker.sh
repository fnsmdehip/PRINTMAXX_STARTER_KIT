#!/bin/bash
#
# PRINTMAXX Autonomous Worker — Spare Laptop Setup Script
#
# Run this on the spare M2 MacBook Pro to set up the 24/7 autonomous worker.
# This script installs security tools, configures the environment,
# and sets up the supervisor daemon with cron scheduling.
#
# Usage:
#   chmod +x AUTOMATIONS/setup_autonomous_worker.sh
#   ./AUTOMATIONS/setup_autonomous_worker.sh
#
# Prerequisites:
#   - macOS with Homebrew installed
#   - Claude Code installed and authenticated (claude login)
#   - Git configured with GitHub access
#   - This repo cloned to the spare laptop
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}  PRINTMAXX AUTONOMOUS WORKER — SPARE LAPTOP SETUP${NC}"
echo -e "${BLUE}================================================================${NC}"
echo ""

# Get project root (assumes script is in AUTOMATIONS/)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
echo -e "${GREEN}Project root:${NC} $PROJECT_ROOT"

# --- Step 1: Check prerequisites ---
echo ""
echo -e "${YELLOW}Step 1: Checking prerequisites...${NC}"

# Check macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo -e "${RED}ERROR: This script is for macOS only.${NC}"
    exit 1
fi
echo "  macOS detected: $(sw_vers -productVersion)"

# Check Homebrew
if ! command -v brew &>/dev/null; then
    echo -e "${RED}ERROR: Homebrew not found. Install it first:${NC}"
    echo '  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    exit 1
fi
echo "  Homebrew: installed"

# Check Codex CLI (PRIMARY — OpenAI, free with ChatGPT Pro)
if ! command -v codex &>/dev/null; then
    echo -e "${YELLOW}  Codex CLI: NOT FOUND — installing...${NC}"
    npm install -g @openai/codex 2>/dev/null || {
        echo -e "${YELLOW}WARNING: Could not install Codex CLI. Install manually: npm i -g @openai/codex${NC}"
    }
fi
if command -v codex &>/dev/null; then
    echo "  Codex CLI: installed (PRIMARY backend)"
else
    echo -e "${YELLOW}  Codex CLI: not installed — will use fallback backends${NC}"
fi

# Check Claude Code (FALLBACK — free with Claude Max)
if ! command -v claude &>/dev/null; then
    echo -e "${YELLOW}  Claude Code: NOT FOUND — installing...${NC}"
    npm install -g @anthropic-ai/claude-code 2>/dev/null || {
        echo -e "${YELLOW}WARNING: Could not install Claude Code.${NC}"
    }
fi
if command -v claude &>/dev/null; then
    echo "  Claude Code: $(claude --version 2>/dev/null || echo 'installed') (FALLBACK backend)"
else
    echo -e "${YELLOW}  Claude Code: not installed${NC}"
fi

# Check git
if ! command -v git &>/dev/null; then
    echo -e "${RED}ERROR: Git not found. Install via: brew install git${NC}"
    exit 1
fi
echo "  Git: installed"

# Check Python
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}ERROR: Python 3 not found. Install via: brew install python3${NC}"
    exit 1
fi
echo "  Python: $(python3 --version)"

echo -e "${GREEN}  All prerequisites met.${NC}"

# --- Step 2: Install security tools ---
echo ""
echo -e "${YELLOW}Step 2: Installing security tools...${NC}"

# LuLu firewall
if [ -d "/Applications/LuLu.app" ]; then
    echo "  LuLu: already installed"
else
    echo "  Installing LuLu firewall..."
    brew install --cask lulu 2>/dev/null || echo "  LuLu: install manually from https://objective-see.org/products/lulu.html"
fi

# BlockBlock
if [ -d "/Applications/BlockBlock Helper.app" ] || [ -d "/Library/Objective-See/BlockBlock/" ]; then
    echo "  BlockBlock: already installed"
else
    echo "  Installing BlockBlock..."
    brew install --cask blockblock 2>/dev/null || echo "  BlockBlock: install manually from https://objective-see.org/products/blockblock.html"
fi

# envchain (keychain-backed secrets)
if command -v envchain &>/dev/null; then
    echo "  envchain: already installed"
else
    echo "  Installing envchain..."
    brew install envchain 2>/dev/null || echo "  envchain: brew install envchain"
fi

# Check FileVault
FV_STATUS=$(fdesetup status 2>/dev/null || echo "unknown")
if echo "$FV_STATUS" | grep -q "On"; then
    echo "  FileVault: enabled"
else
    echo -e "  ${YELLOW}FileVault: NOT enabled. Enable in System Settings > Privacy & Security > FileVault${NC}"
fi

echo -e "${GREEN}  Security tools configured.${NC}"

# --- Step 3: Configure sleep prevention ---
echo ""
echo -e "${YELLOW}Step 3: Configuring sleep prevention...${NC}"

# Check current sleep settings
CURRENT_SLEEP=$(pmset -g | grep -i "disablesleep" | awk '{print $2}' 2>/dev/null || echo "unknown")
if [ "$CURRENT_SLEEP" = "1" ]; then
    echo "  Sleep prevention: already configured"
else
    echo "  Disabling sleep (requires sudo)..."
    echo "  Run these commands manually if needed:"
    echo "    sudo pmset -a disablesleep 1"
    echo "    sudo pmset -a sleep 0"
    echo "    sudo pmset -a displaysleep 0"
    # Try to set (will prompt for password)
    sudo pmset -a disablesleep 1 2>/dev/null || true
    sudo pmset -a sleep 0 2>/dev/null || true
    sudo pmset -a displaysleep 10 2>/dev/null || true  # Display can sleep, CPU stays on
fi

echo -e "${GREEN}  Sleep prevention configured.${NC}"

# --- Step 4: Create directory structure ---
echo ""
echo -e "${YELLOW}Step 4: Creating directory structure...${NC}"

mkdir -p "$PROJECT_ROOT/AUTOMATIONS/logs/autonomous"
mkdir -p "$PROJECT_ROOT/OPS/autonomous_output"
mkdir -p "$PROJECT_ROOT/OPS/HUMAN_NEEDED"

echo "  Created: AUTOMATIONS/logs/autonomous/"
echo "  Created: OPS/autonomous_output/"
echo "  Created: OPS/HUMAN_NEEDED/"
echo -e "${GREEN}  Directories ready.${NC}"

# --- Step 5: Seed initial task queue ---
echo ""
echo -e "${YELLOW}Step 5: Seeding initial task queue...${NC}"

cd "$PROJECT_ROOT"
python3 AUTOMATIONS/autonomous_supervisor.py --seed
echo -e "${GREEN}  Task queue seeded.${NC}"

# --- Step 6: Install crontab ---
echo ""
echo -e "${YELLOW}Step 6: Setting up cron schedule...${NC}"

# Create autonomous worker crontab entries
CRON_FILE="$PROJECT_ROOT/AUTOMATIONS/crontab_autonomous_worker.txt"

cat > "$CRON_FILE" << 'CRONTAB'
# PRINTMAXX Autonomous Worker — Cron Schedule
# Install: crontab AUTOMATIONS/crontab_autonomous_worker.txt
# WARNING: This REPLACES the existing crontab. Merge manually if needed.

SHELL=/bin/zsh
PATH=/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin
MAILTO=""

# Base directory
BASE=/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
PYTHON=/usr/bin/python3
LOG=$BASE/AUTOMATIONS/logs/autonomous

# --- RESEARCH PIPELINE (5 AM) ---
0 5 * * * cd $BASE && $PYTHON AUTOMATIONS/autonomous_supervisor.py --pipeline research >> $LOG/cron_research.log 2>&1

# --- CONTENT GENERATION (8 AM) ---
0 8 * * * cd $BASE && $PYTHON AUTOMATIONS/autonomous_supervisor.py --pipeline content >> $LOG/cron_content.log 2>&1

# --- MIDDAY PULSE (12 PM) ---
0 12 * * * cd $BASE && $PYTHON AUTOMATIONS/autonomous_supervisor.py --pipeline midday >> $LOG/cron_midday.log 2>&1

# --- CONTENT ROUND 2 (5 PM) ---
0 17 * * * cd $BASE && $PYTHON AUTOMATIONS/autonomous_supervisor.py --pipeline content >> $LOG/cron_content_pm.log 2>&1

# --- OVERNIGHT BUILDER (10 PM) ---
0 22 * * * cd $BASE && $PYTHON AUTOMATIONS/autonomous_supervisor.py --pipeline overnight >> $LOG/cron_overnight.log 2>&1

# --- HEALTH CHECK (every 2 hours) ---
0 */2 * * * cd $BASE && $PYTHON AUTOMATIONS/autonomous_supervisor.py --pipeline health >> $LOG/cron_health.log 2>&1

# --- SELF-PLANNING (every 6 hours, if queue empty) ---
0 4,10,16,22 * * * cd $BASE && $PYTHON AUTOMATIONS/autonomous_supervisor.py --plan >> $LOG/cron_plan.log 2>&1

# --- GIT SYNC (every 6 hours) ---
0 6,12,18,0 * * * cd $BASE && git add -A && git commit -m "[autonomous] $(date +\%Y-\%m-\%d_\%H:\%M) sync" --allow-empty 2>/dev/null; echo "Git sync at $(date)" >> $LOG/git_sync.log

# --- LOG ROTATION (weekly, Sunday 3 AM) ---
0 3 * * 0 find $LOG -name "*.log" -mtime +30 -delete 2>/dev/null; echo "Log rotation at $(date)" >> $LOG/maintenance.log
CRONTAB

echo "  Crontab written to: $CRON_FILE"
echo ""
echo -e "  ${YELLOW}To install crontab, run:${NC}"
echo "    crontab $CRON_FILE"
echo ""
echo -e "  ${YELLOW}Or to merge with existing crontab:${NC}"
echo "    (crontab -l 2>/dev/null; cat $CRON_FILE) | crontab -"
echo ""
echo -e "${GREEN}  Cron schedule ready.${NC}"

# --- Step 7: Create launchd plist for supervisor daemon ---
echo ""
echo -e "${YELLOW}Step 7: Creating launchd plist for auto-start...${NC}"

PLIST_DIR="$PROJECT_ROOT/AUTOMATIONS"
PLIST_FILE="$PLIST_DIR/com.printmaxx.autonomous-supervisor.plist"

cat > "$PLIST_FILE" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.printmaxx.autonomous-supervisor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>${PROJECT_ROOT}/AUTOMATIONS/autonomous_supervisor.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>${PROJECT_ROOT}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${PROJECT_ROOT}/AUTOMATIONS/logs/autonomous/supervisor_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>${PROJECT_ROOT}/AUTOMATIONS/logs/autonomous/supervisor_stderr.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin</string>
    </dict>
</dict>
</plist>
PLIST

echo "  Plist written to: $PLIST_FILE"
echo ""
echo -e "  ${YELLOW}To install as auto-starting daemon:${NC}"
echo "    cp $PLIST_FILE ~/Library/LaunchAgents/"
echo "    launchctl load ~/Library/LaunchAgents/com.printmaxx.autonomous-supervisor.plist"
echo ""
echo -e "  ${YELLOW}To start manually instead:${NC}"
echo "    caffeinate -s python3 $PROJECT_ROOT/AUTOMATIONS/autonomous_supervisor.py"
echo ""
echo -e "${GREEN}  LaunchAgent ready.${NC}"

# --- Step 8: Test supervisor ---
echo ""
echo -e "${YELLOW}Step 8: Running test...${NC}"

cd "$PROJECT_ROOT"
python3 AUTOMATIONS/autonomous_supervisor.py --status

# --- Step 9: Test Telegram (if configured) ---
echo ""
echo -e "${YELLOW}Step 9: Testing Telegram alerts...${NC}"
python3 AUTOMATIONS/autonomous_alerts.py --status

# --- Final Summary ---
echo ""
echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}  SETUP COMPLETE${NC}"
echo -e "${BLUE}================================================================${NC}"
echo ""
echo "  What was done:"
echo "    1. Prerequisites verified"
echo "    2. Security tools installed (LuLu, BlockBlock, envchain)"
echo "    3. Sleep prevention configured"
echo "    4. Directory structure created"
echo "    5. Task queue seeded with initial tasks"
echo "    6. Crontab entries written (install manually)"
echo "    7. LaunchAgent plist created (install manually)"
echo "    8. System tested"
echo ""
echo "  Next steps:"
echo ""
echo -e "    ${GREEN}1. Configure Telegram alerts:${NC}"
echo "       - Message @BotFather on Telegram, create a bot"
echo "       - Get your chat_id from https://api.telegram.org/bot<TOKEN>/getUpdates"
echo "       - Set in OPS/AUTONOMOUS_WORKER_CONFIG.yaml"
echo ""
echo -e "    ${GREEN}2. Install crontab:${NC}"
echo "       crontab AUTOMATIONS/crontab_autonomous_worker.txt"
echo ""
echo -e "    ${GREEN}3. Start the supervisor:${NC}"
echo "       caffeinate -s python3 AUTOMATIONS/autonomous_supervisor.py"
echo ""
echo -e "    ${GREEN}4. Or install as auto-start daemon:${NC}"
echo "       cp AUTOMATIONS/com.printmaxx.autonomous-supervisor.plist ~/Library/LaunchAgents/"
echo "       launchctl load ~/Library/LaunchAgents/com.printmaxx.autonomous-supervisor.plist"
echo ""
echo -e "    ${GREEN}5. Monitor:${NC}"
echo "       python3 AUTOMATIONS/autonomous_supervisor.py --status"
echo "       tail -f AUTOMATIONS/logs/autonomous/supervisor_$(date +%Y-%m-%d).log"
echo ""
echo -e "    ${GREEN}6. First supervised test (recommended):${NC}"
echo "       python3 AUTOMATIONS/autonomous_supervisor.py --once"
echo "       # Watch it run one task, verify output is good"
echo ""
echo -e "${BLUE}  The 24/7 autonomous worker is ready. Let it cook.${NC}"
echo ""
