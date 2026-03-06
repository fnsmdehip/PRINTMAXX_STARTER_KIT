#!/bin/bash
# PRINTMAXX Automation Installer
# Installs both cron AND launchd for redundancy
# Run: bash AUTOMATIONS/install_automation.sh

set -euo pipefail

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
LAUNCHD_DIR="$HOME/Library/LaunchAgents"
PLIST_DIR="$BASE/AUTOMATIONS/launchd"

echo "=== PRINTMAXX AUTOMATION INSTALLER ==="
echo ""

# --- STEP 1: Install crontab ---
echo "[1/4] Installing crontab..."
crontab "$BASE/AUTOMATIONS/crontab_printmaxx_v2.txt"
CRON_COUNT=$(crontab -l 2>/dev/null | grep -v "^#" | grep -v "^$" | grep -v "^[A-Z]" | wc -l | tr -d ' ')
echo "  Installed: $CRON_COUNT cron jobs"

# Verify
if [ "$CRON_COUNT" -gt 10 ]; then
    echo "  Status: OK"
else
    echo "  WARNING: Only $CRON_COUNT jobs found. Expected 40+."
fi

# --- STEP 2: Install launchd agents ---
echo ""
echo "[2/4] Installing launchd agents..."
mkdir -p "$LAUNCHD_DIR"

for plist in "$PLIST_DIR"/*.plist; do
    LABEL=$(basename "$plist" .plist)

    # Unload if already loaded (ignore errors)
    launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true

    # Copy to LaunchAgents
    cp "$plist" "$LAUNCHD_DIR/"

    # Load
    launchctl bootstrap "gui/$(id -u)" "$LAUNCHD_DIR/$(basename $plist)" 2>/dev/null && \
        echo "  Loaded: $LABEL" || \
        echo "  WARNING: Failed to load $LABEL (may need Full Disk Access)"
done

# --- STEP 3: Verify ---
echo ""
echo "[3/4] Verification..."

# Check crontab
CRON_CHECK=$(crontab -l 2>/dev/null | wc -l | tr -d ' ')
echo "  Crontab: $CRON_CHECK lines"

# Check launchd
for plist in "$PLIST_DIR"/*.plist; do
    LABEL=$(basename "$plist" .plist)
    if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then
        echo "  LaunchAgent $LABEL: LOADED"
    else
        echo "  LaunchAgent $LABEL: NOT LOADED"
    fi
done

# --- STEP 4: Create persistence checker ---
echo ""
echo "[4/4] Creating persistence check..."

cat > "$BASE/AUTOMATIONS/check_automation_status.sh" << 'CHECKER'
#!/bin/bash
# Quick check: are automations actually installed and running?
echo "=== AUTOMATION STATUS ==="
echo ""

# Crontab
CRON_LINES=$(crontab -l 2>/dev/null | wc -l | tr -d ' ')
if [ "$CRON_LINES" -gt 10 ]; then
    echo "CRONTAB: INSTALLED ($CRON_LINES lines)"
else
    echo "CRONTAB: EMPTY OR MISSING ($CRON_LINES lines)"
    echo "  FIX: bash AUTOMATIONS/install_automation.sh"
fi

# LaunchAgents
echo ""
for label in com.printmaxx.scrapers com.printmaxx.claude-sessions; do
    if launchctl print "gui/$(id -u)/$label" >/dev/null 2>&1; then
        echo "LAUNCHD $label: RUNNING"
    else
        echo "LAUNCHD $label: NOT RUNNING"
        echo "  FIX: bash AUTOMATIONS/install_automation.sh"
    fi
done

# Last log activity
echo ""
echo "LAST LOG ACTIVITY:"
BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
for log in "$BASE/AUTOMATIONS/logs/"*.log; do
    if [ -f "$log" ]; then
        MOD=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$log" 2>/dev/null)
        NAME=$(basename "$log")
        echo "  $MOD  $NAME"
    fi
done | sort -r | head -10

echo ""
echo "=== END ==="
CHECKER

chmod +x "$BASE/AUTOMATIONS/check_automation_status.sh"
echo "  Created: AUTOMATIONS/check_automation_status.sh"

echo ""
echo "=== DONE ==="
echo ""
echo "To verify at any time: bash AUTOMATIONS/check_automation_status.sh"
echo "To reinstall: bash AUTOMATIONS/install_automation.sh"
echo ""
echo "NOTE: For cron/launchd to run while MacBook is closed,"
echo "you need to keep it plugged in and run:"
echo "  caffeinate -s &"
echo "Or change Energy Saver settings to prevent sleep."
