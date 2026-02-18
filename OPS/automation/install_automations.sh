#!/bin/bash
# ============================================================
# PRINTMAXX AUTOMATION INSTALLER
# ============================================================
# Installs all launchd scheduled tasks on your Mac.
# Run once from ANYWHERE:
#   bash /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/OPS/automation/install_automations.sh
#
# What gets installed:
#   Daily 6:00 AM  - Morning alpha sync (data pipeline)
#   Daily 6:30 AM  - Content generation (calendar + Buffer CSVs)
#   Daily 6:00 PM  - Evening digest (daily summary report)
#   Daily 9:00 PM  - Nightly backup (git commit + push)
#   Daily 10:00 PM - Overnight Ralph sprint (8 parallel loops)
#   Monday 9:00 AM - Weekly tasks (backtests, QA, validation)
#   1st 8:00 AM    - Monthly tasks (rebalance, P&L, audit)
#
# To uninstall: bash OPS/automation/install_automations.sh --uninstall
# ============================================================

set -euo pipefail

PLIST_DIR="$(cd "$(dirname "$0")/launchd" && pwd)"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"
PROJECT_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ============================================================
# UNINSTALL
# ============================================================
if [ "${1:-}" = "--uninstall" ]; then
    echo -e "${YELLOW}Uninstalling PRINTMAXX automations...${NC}"
    for plist in "$PLIST_DIR"/*.plist; do
        name=$(basename "$plist")
        label=$(basename "$name" .plist)
        if [ -f "$LAUNCH_AGENTS/$name" ]; then
            launchctl unload "$LAUNCH_AGENTS/$name" 2>/dev/null || true
            rm "$LAUNCH_AGENTS/$name"
            echo -e "  ${RED}Removed:${NC} $label"
        fi
    done
    echo -e "${GREEN}All PRINTMAXX automations uninstalled.${NC}"
    exit 0
fi

# ============================================================
# PRE-FLIGHT CHECKS
# ============================================================
echo "============================================================"
echo "  PRINTMAXX AUTOMATION INSTALLER"
echo "  $(date)"
echo "============================================================"
echo ""

# Check project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}ERROR: Project directory not found: $PROJECT_DIR${NC}"
    echo "Update PROJECT_DIR in this script if your project moved."
    exit 1
fi

# Check orchestrator exists
if [ ! -f "$PROJECT_DIR/printmaxx_cron.sh" ]; then
    echo -e "${RED}ERROR: printmaxx_cron.sh not found in project root${NC}"
    exit 1
fi

# Ensure orchestrator is executable
chmod +x "$PROJECT_DIR/printmaxx_cron.sh"

# Check Python deps
echo "Checking Python dependencies..."
python3 -c "import rich; import textual" 2>/dev/null || {
    echo -e "${YELLOW}Installing missing Python deps...${NC}"
    python3 -m pip install --user rich textual numpy 2>/dev/null || pip3 install --user rich textual numpy
}
echo -e "  ${GREEN}Python deps OK${NC}"

# Create log directory
mkdir -p "$PROJECT_DIR/logs"

# Create LaunchAgents directory if needed
mkdir -p "$LAUNCH_AGENTS"

# ============================================================
# INSTALL PLISTS
# ============================================================
echo ""
echo "Installing scheduled tasks..."
echo ""

for plist in "$PLIST_DIR"/*.plist; do
    name=$(basename "$plist")
    label=$(basename "$name" .plist)

    # Unload if already loaded
    if [ -f "$LAUNCH_AGENTS/$name" ]; then
        launchctl unload "$LAUNCH_AGENTS/$name" 2>/dev/null || true
    fi

    # Copy and load
    cp "$plist" "$LAUNCH_AGENTS/$name"
    launchctl load "$LAUNCH_AGENTS/$name"

    # Parse schedule from plist for display
    case "$label" in
        *morning-sync*)     schedule="Daily 6:00 AM" ;;
        *content-gen*)      schedule="Daily 6:30 AM" ;;
        *evening-digest*)   schedule="Daily 6:00 PM" ;;
        *nightly-backup*)   schedule="Daily 9:00 PM" ;;
        *overnight-sprint*) schedule="Daily 10:00 PM" ;;
        *weekly*)           schedule="Monday 9:00 AM" ;;
        *monthly*)          schedule="1st of Month 8:00 AM" ;;
        *)                  schedule="Custom" ;;
    esac

    echo -e "  ${GREEN}Installed:${NC} $label → $schedule"
done

# ============================================================
# CONFIGURE MAC WAKE FROM SLEEP
# ============================================================
echo ""
echo "Setting up wake schedule for overnight sprint..."
# Wake Mac at 5:55 AM daily so morning sync can run at 6 AM
# (launchd will fire missed tasks after wake, but this ensures timeliness)
sudo pmset repeat wakeorpoweron MTWRFSU 05:55:00 2>/dev/null && \
    echo -e "  ${GREEN}Mac will wake at 5:55 AM daily${NC}" || \
    echo -e "  ${YELLOW}Could not set wake schedule (needs sudo). Run manually:${NC}"
    echo "  sudo pmset repeat wakeorpoweron MTWRFSU 05:55:00"

echo ""
echo "============================================================"
echo -e "  ${GREEN}ALL AUTOMATIONS INSTALLED${NC}"
echo "============================================================"
echo ""
echo "Verify with: launchctl list | grep printmaxx"
echo "View logs:   ls -lt $PROJECT_DIR/logs/launchd_*.log"
echo "Run now:     bash $PROJECT_DIR/printmaxx_cron.sh morning"
echo "Uninstall:   bash $0 --uninstall"
echo ""
echo "Schedule Summary:"
echo "  6:00 AM  → Alpha sync + organize + repair"
echo "  6:30 AM  → Content calendar + Buffer CSVs"
echo "  6:00 PM  → Daily digest report"
echo "  9:00 PM  → Git backup + push"
echo "  10:00 PM → 8 Ralph loops overnight sprint"
echo "  Mon 9 AM → Weekly backtests + QA + validation"
echo "  1st 8 AM → Monthly rebalance + P&L + audit"
echo ""
