#!/bin/bash
# Wrap all PWA apps with Capacitor and prepare for submission
# Usage: bash scripts/wrap_and_submit_all.sh [ios|android|both]
# Prereqs: npm install -g @capacitor/cli @capacitor/core

set -e

PLATFORM=${1:-both}
BASE_DIR="/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph/loops/app_factory/output"

APPS=(
  "focuslock-web:FocusLock:com.printmaxx.focuslock"
  "habitforge-web:HabitForge:com.printmaxx.habitforge"
  "mealmaxx-web:MealMaxx:com.printmaxx.mealmaxx"
  "ramadan-tracker:Hilal:com.printmaxx.hilal"
  "sleepmaxx-web:SleepMaxx:com.printmaxx.sleepmaxx"
  "walktounlock-web:WalkToUnlock:com.printmaxx.walktounlock"
)

SUCCESS=0
FAIL=0

for entry in "${APPS[@]}"; do
  IFS=':' read -r dir name bundle <<< "$entry"
  echo "=== Wrapping $name ($bundle) ==="

  APP_DIR="$BASE_DIR/$dir"

  if [ ! -d "$APP_DIR" ]; then
    echo "  SKIP: Directory not found: $APP_DIR"
    FAIL=$((FAIL + 1))
    continue
  fi

  cd "$APP_DIR"

  # Init npm if needed
  if [ ! -f package.json ]; then
    echo "  Initializing package.json..."
    npm init -y > /dev/null 2>&1
  fi

  # Install Capacitor if needed
  if [ ! -d node_modules/@capacitor ]; then
    echo "  Installing Capacitor..."
    npm install @capacitor/core @capacitor/cli > /dev/null 2>&1
  fi

  # Init Capacitor if needed
  if [ ! -f capacitor.config.ts ] && [ ! -f capacitor.config.json ]; then
    echo "  Initializing Capacitor project..."
    npx cap init "$name" "$bundle" --web-dir . > /dev/null 2>&1
  fi

  # Add iOS
  if [ "$PLATFORM" = "ios" ] || [ "$PLATFORM" = "both" ]; then
    if [ ! -d ios ]; then
      echo "  Adding iOS platform..."
      npx cap add ios > /dev/null 2>&1
    fi
    npx cap copy ios > /dev/null 2>&1
    echo "  iOS project ready at $dir/ios/"
  fi

  # Add Android
  if [ "$PLATFORM" = "android" ] || [ "$PLATFORM" = "both" ]; then
    if [ ! -d android ]; then
      echo "  Adding Android platform..."
      npx cap add android > /dev/null 2>&1
    fi
    npx cap copy android > /dev/null 2>&1
    echo "  Android project ready at $dir/android/"
  fi

  SUCCESS=$((SUCCESS + 1))
  echo "  Done."
  echo ""
done

echo "=== Summary ==="
echo "Wrapped: $SUCCESS / ${#APPS[@]}"
if [ $FAIL -gt 0 ]; then
  echo "Failed: $FAIL"
fi
echo ""
echo "Next steps:"
echo "  iOS: cd <app-dir> && npx cap open ios"
echo "  Android: cd <app-dir> && npx cap open android"
echo "  TestFlight: cd <app-dir>/ios/App && fastlane beta"
echo "  App Store: cd <app-dir>/ios/App && fastlane release"
