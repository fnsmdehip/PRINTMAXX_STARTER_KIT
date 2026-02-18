#!/bin/bash
# PRINTMAXX PWA Deploy Script
# Deploys all 7 PWA apps to Vercel in sequence
# Usage: bash AUTOMATIONS/deploy_all_apps.sh
#
# PREREQUISITE: Run `vercel login` first to authenticate
#
# All apps are static HTML PWAs (no build step needed)

set -e

BASE="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
RESULTS_FILE="$BASE/AUTOMATIONS/logs/deploy_results_$(date +%Y-%m-%d_%H%M%S).log"
mkdir -p "$BASE/AUTOMATIONS/logs"

echo "========================================" | tee "$RESULTS_FILE"
echo "PRINTMAXX PWA DEPLOYMENT" | tee -a "$RESULTS_FILE"
echo "$(date)" | tee -a "$RESULTS_FILE"
echo "========================================" | tee -a "$RESULTS_FILE"
echo "" | tee -a "$RESULTS_FILE"

# Check if logged in
if ! vercel whoami 2>/dev/null; then
    echo "ERROR: Not logged in to Vercel." | tee -a "$RESULTS_FILE"
    echo "Run: vercel login" | tee -a "$RESULTS_FILE"
    echo "Then re-run this script." | tee -a "$RESULTS_FILE"
    exit 1
fi

LOGGED_IN_AS=$(vercel whoami 2>/dev/null)
echo "Logged in as: $LOGGED_IN_AS" | tee -a "$RESULTS_FILE"
echo "" | tee -a "$RESULTS_FILE"

# App directories in priority order (Ramadan first)
declare -a APP_NAMES=(
    "ramadan-tracker"
    "sleepmaxx-web"
    "focuslock-web"
    "habitforge-web"
    "mealmaxx-web"
    "walktounlock-web"
    "prayerlock-web"
)

declare -a APP_DIRS=(
    "$BASE/ralph/loops/app_factory/output/ramadan-tracker"
    "$BASE/ralph/loops/app_factory/output/sleepmaxx-web"
    "$BASE/ralph/loops/app_factory/output/focuslock-web"
    "$BASE/ralph/loops/app_factory/output/habitforge-web"
    "$BASE/ralph/loops/app_factory/output/mealmaxx-web"
    "$BASE/ralph/loops/app_factory/output/walktounlock-web"
    "$BASE/MONEY_METHODS/APP_FACTORY/builds/prayerlock-web"
)

DEPLOYED=0
FAILED=0

for i in "${!APP_NAMES[@]}"; do
    NAME="${APP_NAMES[$i]}"
    DIR="${APP_DIRS[$i]}"

    echo "----------------------------------------" | tee -a "$RESULTS_FILE"
    echo "[$((i+1))/7] Deploying: $NAME" | tee -a "$RESULTS_FILE"
    echo "Directory: $DIR" | tee -a "$RESULTS_FILE"
    echo "" | tee -a "$RESULTS_FILE"

    if [ ! -d "$DIR" ]; then
        echo "  SKIP: Directory not found" | tee -a "$RESULTS_FILE"
        FAILED=$((FAILED + 1))
        continue
    fi

    if [ ! -f "$DIR/index.html" ]; then
        echo "  SKIP: No index.html found" | tee -a "$RESULTS_FILE"
        FAILED=$((FAILED + 1))
        continue
    fi

    # Deploy as static site
    echo "  Deploying to Vercel..." | tee -a "$RESULTS_FILE"
    DEPLOY_OUTPUT=$(cd "$DIR" && vercel deploy --prod --yes 2>&1) || true

    if echo "$DEPLOY_OUTPUT" | grep -q "https://"; then
        URL=$(echo "$DEPLOY_OUTPUT" | grep -oE "https://[^ ]+" | tail -1)
        echo "  SUCCESS: $URL" | tee -a "$RESULTS_FILE"
        DEPLOYED=$((DEPLOYED + 1))
    else
        echo "  FAILED:" | tee -a "$RESULTS_FILE"
        echo "  $DEPLOY_OUTPUT" | tee -a "$RESULTS_FILE"
        FAILED=$((FAILED + 1))
    fi
    echo "" | tee -a "$RESULTS_FILE"
done

echo "========================================" | tee -a "$RESULTS_FILE"
echo "DEPLOYMENT SUMMARY" | tee -a "$RESULTS_FILE"
echo "Deployed: $DEPLOYED / 7" | tee -a "$RESULTS_FILE"
echo "Failed: $FAILED / 7" | tee -a "$RESULTS_FILE"
echo "Results saved to: $RESULTS_FILE" | tee -a "$RESULTS_FILE"
echo "========================================" | tee -a "$RESULTS_FILE"
