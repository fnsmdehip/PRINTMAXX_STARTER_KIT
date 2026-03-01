# Mobile App Submission Pipeline

Created: 2026-02-12
Status: Ready to execute once developer accounts are created

## System status

| Component | Status | Notes |
|-----------|--------|-------|
| Xcode CLI | INSTALLED | /Applications/Xcode.app/Contents/Developer |
| Capacitor CLI | NOT INSTALLED | `npm install -g @capacitor/cli` |
| Android SDK | NOT INSTALLED | Need Android Studio or standalone SDK |
| fastlane | NOT INSTALLED | `gem install fastlane` or `brew install fastlane` |
| Ruby | INSTALLED | 2.6.10 (system) |
| Node.js | INSTALLED | Required for Capacitor |
| Apple Developer | NOT ENROLLED | $99/yr required |
| Google Play Console | NOT ENROLLED | $25 one-time required |

## PWA app inventory

All 6 PWA apps confirmed with manifest.json + sw.js:

| App | Location | manifest.json | sw.js | Ready |
|-----|----------|---------------|-------|-------|
| FocusLock | ralph/loops/app_factory/output/focuslock-web/ | YES | YES | YES |
| HabitForge | ralph/loops/app_factory/output/habitforge-web/ | YES | YES | YES |
| MealMaxx | ralph/loops/app_factory/output/mealmaxx-web/ | YES | YES | YES |
| Ramadan (Hilal) | ralph/loops/app_factory/output/ramadan-tracker/ | YES | YES | YES |
| SleepMaxx | ralph/loops/app_factory/output/sleepmaxx-web/ | YES | YES | YES |
| WalkToUnlock | ralph/loops/app_factory/output/walktounlock-web/ | YES | YES | YES |

Additional apps in MONEY_METHODS/APP_FACTORY/builds/:
- PrayerLock (manifest + sw.js)
- FocusLock, SleepMaxx, WalkToUnlock (duplicates/older copies, manifest only, no sw.js)
- BioMaxx (native Expo SDK54, not PWA - has its own submission checklist)

---

## Phase 0: Install tooling (no accounts needed, do today)

### 1. Install Capacitor CLI

```bash
npm install -g @capacitor/cli @capacitor/core
```

### 2. Install fastlane

```bash
# Option A: Homebrew (recommended)
brew install fastlane

# Option B: RubyGems
gem install fastlane

# Verify
fastlane --version
```

### 3. Install Android Studio (optional, for Android builds)

Download from https://developer.android.com/studio
After install, add to shell profile:
```bash
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

### 4. Install CocoaPods (for iOS native dependencies)

```bash
sudo gem install cocoapods
# or
brew install cocoapods
```

---

## Phase 1: PWA to Capacitor wrapping

Capacitor wraps any web app (HTML/CSS/JS or framework) into a native iOS/Android shell. Since all 6 apps are static PWAs with manifest.json and sw.js, the wrapping is straightforward.

### Per-app setup (repeat for each of the 6 apps)

```bash
# 1. Navigate to app directory
cd ralph/loops/app_factory/output/ramadan-tracker/

# 2. Initialize npm if no package.json
npm init -y

# 3. Install Capacitor
npm install @capacitor/core @capacitor/cli

# 4. Initialize Capacitor
npx cap init "Hilal" "com.printmaxx.hilal" --web-dir .

# 5. Add platforms
npx cap add ios
npx cap add android

# 6. Copy web assets to native projects
npx cap copy

# 7. Open in Xcode (for iOS)
npx cap open ios

# 8. Open in Android Studio (for Android)
npx cap open android
```

### App ID mapping (reverse domain notation)

| App | Bundle ID (iOS) | Package Name (Android) |
|-----|-----------------|----------------------|
| FocusLock | com.printmaxx.focuslock | com.printmaxx.focuslock |
| HabitForge | com.printmaxx.habitforge | com.printmaxx.habitforge |
| MealMaxx | com.printmaxx.mealmaxx | com.printmaxx.mealmaxx |
| Hilal (Ramadan) | com.printmaxx.hilal | com.printmaxx.hilal |
| SleepMaxx | com.printmaxx.sleepmaxx | com.printmaxx.sleepmaxx |
| WalkToUnlock | com.printmaxx.walktounlock | com.printmaxx.walktounlock |

### Adding native plugins (optional per app)

```bash
# Push notifications
npm install @capacitor/push-notifications
npx cap sync

# Local notifications (prayer times, habit reminders)
npm install @capacitor/local-notifications
npx cap sync

# Haptics (for WalkToUnlock step counter feedback)
npm install @capacitor/haptics
npx cap sync

# Status bar customization
npm install @capacitor/status-bar
npx cap sync

# Splash screen
npm install @capacitor/splash-screen
npx cap sync

# In-app purchases (RevenueCat)
npm install @revenuecat/purchases-capacitor
npx cap sync

# AdMob
npm install @capacitor-community/admob
npx cap sync
```

---

## Phase 2: Apple Developer enrollment ($99/yr)

### Signup process

1. Go to https://developer.apple.com/enroll/
2. Sign in with Apple ID (or create one)
3. Agree to Apple Developer Agreement
4. Pay $99/year
5. Wait for enrollment approval (usually 24-48 hours, sometimes instant)
6. After approval, access App Store Connect at https://appstoreconnect.apple.com

### What you get
- Submit apps to App Store
- TestFlight beta distribution (up to 10,000 external testers)
- Access to all Apple frameworks and APIs
- Up to 100 test devices for development
- App analytics and sales data

### Save credentials to SECRETS/PAYMENT_INFO.md
```
APPLE_ID=your@email.com
APPLE_TEAM_ID=XXXXXXXXXX  (found in Membership tab)
```

---

## Phase 3: Google Play Console enrollment ($25 one-time)

### Signup process

1. Go to https://play.google.com/console/signup
2. Sign in with Google Account
3. Accept Developer Distribution Agreement
4. Pay $25 one-time fee
5. Complete account details (developer name, address, phone)
6. Identity verification may take 2-7 days

### What you get
- Submit apps to Google Play Store
- Internal/closed/open testing tracks
- Pre-launch reports (automated testing on real devices)
- Store listing experiments (A/B test icons, screenshots, descriptions)
- Revenue and analytics dashboard

---

## Phase 4: iOS submission with fastlane

### Initial fastlane setup (per app)

```bash
cd ralph/loops/app_factory/output/ramadan-tracker/ios/App

# Initialize fastlane
fastlane init

# Choose option 4: Manual setup
```

### Fastfile template

Create `ios/App/fastlane/Fastfile`:

```ruby
default_platform(:ios)

platform :ios do
  desc "Push a new beta build to TestFlight"
  lane :beta do
    increment_build_number
    build_app(
      workspace: "App.xcworkspace",
      scheme: "App",
      export_method: "app-store"
    )
    upload_to_testflight
  end

  desc "Push a new release to the App Store"
  lane :release do
    increment_build_number
    build_app(
      workspace: "App.xcworkspace",
      scheme: "App",
      export_method: "app-store"
    )
    upload_to_app_store(
      skip_metadata: false,
      skip_screenshots: false,
      force: true
    )
  end
end
```

### App Store Connect API key (for CI/CD)

1. Go to https://appstoreconnect.apple.com/access/api
2. Generate a new API key with "App Manager" role
3. Download the .p8 file
4. Save to SECRETS/ and update PAYMENT_INFO.md:
```
APP_STORE_CONNECT_API_KEY_ID=XXXXXXXXXX
APP_STORE_CONNECT_ISSUER_ID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
APP_STORE_CONNECT_API_KEY_PATH=SECRETS/AuthKey_XXXXXXXXXX.p8
```

### One-command submission

```bash
# TestFlight beta
fastlane beta

# App Store release
fastlane release
```

---

## Phase 5: Android submission with fastlane

### Setup

```bash
cd ralph/loops/app_factory/output/ramadan-tracker/android

fastlane init
```

### Fastfile template

Create `android/fastlane/Fastfile`:

```ruby
default_platform(:android)

platform :android do
  desc "Build and upload to Google Play internal testing"
  lane :internal do
    gradle(
      task: "clean assembleRelease",
      project_dir: "."
    )
    upload_to_play_store(
      track: "internal",
      aab: "app/build/outputs/bundle/release/app-release.aab"
    )
  end

  desc "Promote internal to production"
  lane :release do
    upload_to_play_store(
      track: "production",
      aab: "app/build/outputs/bundle/release/app-release.aab"
    )
  end
end
```

### Google Play service account (for automated uploads)

1. Go to Google Cloud Console > IAM & Admin > Service Accounts
2. Create service account with "Service Account User" role
3. Generate JSON key, save to SECRETS/google_play_service_account.json
4. In Google Play Console > Settings > API access, link the service account
5. Grant "Release Manager" permission

---

## Phase 6: Ad integration

### AdMob setup (free)

1. Sign up at https://admob.google.com
2. Create an app for each submission
3. Create ad units: banner + interstitial per app
4. Copy App ID and Ad Unit IDs to SECRETS/PAYMENT_INFO.md

### Capacitor AdMob integration

```bash
npm install @capacitor-community/admob
npx cap sync
```

```typescript
import { AdMob, BannerAdSize, BannerAdPosition } from '@capacitor-community/admob';

// Initialize
await AdMob.initialize({
  initializeForTesting: false,
});

// Show banner
await AdMob.showBanner({
  adId: 'ca-app-pub-XXXXXXXXXXXXXXXX/YYYYYYYYYY',
  adSize: BannerAdSize.ADAPTIVE_BANNER,
  position: BannerAdPosition.BOTTOM_CENTER,
});

// Show interstitial (between screens)
await AdMob.prepareInterstitial({ adId: 'ca-app-pub-XXXXXXXXXXXXXXXX/YYYYYYYYYY' });
await AdMob.showInterstitial();
```

### Unity Ads setup (free, higher CPM for gamified apps)

Good for: WalkToUnlock (step challenges), HabitForge (streak rewards), FocusLock (timer completion)

1. Sign up at https://dashboard.unity3d.com
2. Create project per app
3. Enable ads, get Game ID per platform
4. Install: `npm install capacitor-unity-ads` (community plugin)

### Ad strategy per app

| App | Primary ads | Secondary | Notes |
|-----|-------------|-----------|-------|
| Ramadan (Hilal) | AdMob banner | None | Respectful placement, not during prayer |
| FocusLock | Interstitial on timer complete | Banner on stats | Rewarded video to unlock themes |
| HabitForge | Banner on dashboard | Interstitial weekly | Rewarded video for streak shields |
| MealMaxx | Banner on meal log | Interstitial | Affiliate links for meal prep (higher rev than ads) |
| SleepMaxx | Banner on dashboard | None | Affiliate links for mattress/supplements > ads |
| WalkToUnlock | Rewarded video for bonus steps | Banner | Unity Ads (gamified = higher CPM) |

### RevenueCat for subscriptions

```bash
npm install @revenuecat/purchases-capacitor
npx cap sync
```

RevenueCat handles:
- Apple IAP + Google Play Billing in one SDK
- Subscription management, trials, promotions
- Cross-platform receipt validation
- Analytics dashboard

Setup: https://www.revenuecat.com (free up to $2,500 MTR)

---

## Phase 7: Automated submission script

### Bulk wrapper script

Save as `scripts/wrap_and_submit_all.sh`:

```bash
#!/bin/bash
# Wrap all PWA apps with Capacitor and prepare for submission
# Usage: bash scripts/wrap_and_submit_all.sh [ios|android|both]

PLATFORM=${1:-both}
BASE_DIR="ralph/loops/app_factory/output"

APPS=(
  "focuslock-web:FocusLock:com.printmaxx.focuslock"
  "habitforge-web:HabitForge:com.printmaxx.habitforge"
  "mealmaxx-web:MealMaxx:com.printmaxx.mealmaxx"
  "ramadan-tracker:Hilal:com.printmaxx.hilal"
  "sleepmaxx-web:SleepMaxx:com.printmaxx.sleepmaxx"
  "walktounlock-web:WalkToUnlock:com.printmaxx.walktounlock"
)

for entry in "${APPS[@]}"; do
  IFS=':' read -r dir name bundle <<< "$entry"
  echo "=== Wrapping $name ($bundle) ==="

  cd "$BASE_DIR/$dir"

  # Init npm if needed
  if [ ! -f package.json ]; then
    npm init -y
  fi

  # Install Capacitor if needed
  if [ ! -d node_modules/@capacitor ]; then
    npm install @capacitor/core @capacitor/cli
  fi

  # Init Capacitor if needed
  if [ ! -f capacitor.config.ts ] && [ ! -f capacitor.config.json ]; then
    npx cap init "$name" "$bundle" --web-dir .
  fi

  # Add platforms
  if [ "$PLATFORM" = "ios" ] || [ "$PLATFORM" = "both" ]; then
    npx cap add ios 2>/dev/null
    npx cap copy ios
    echo "  iOS project ready at $dir/ios/"
  fi

  if [ "$PLATFORM" = "android" ] || [ "$PLATFORM" = "both" ]; then
    npx cap add android 2>/dev/null
    npx cap copy android
    echo "  Android project ready at $dir/android/"
  fi

  cd - > /dev/null
  echo ""
done

echo "All apps wrapped. Next steps:"
echo "  iOS: npx cap open ios (in each app dir)"
echo "  Android: npx cap open android (in each app dir)"
echo "  Submit: fastlane beta (TestFlight) or fastlane release (App Store)"
```

---

## Timeline: what to do when

### Today (no accounts needed)
- [x] Install Capacitor CLI: `npm install -g @capacitor/cli @capacitor/core`
- [ ] Install fastlane: `brew install fastlane`
- [ ] Install CocoaPods: `brew install cocoapods`
- [ ] Run Capacitor init on all 6 apps (creates ios/ and android/ folders)
- [ ] Test Xcode build on one app (Ramadan first - most urgent)
- [ ] Generate proper app icons (replace SVG data URIs with real PNGs)

### After Apple Developer enrollment ($99)
- [ ] Create App Store Connect entries for all 6 apps
- [ ] Set up App Store Connect API key
- [ ] Configure fastlane with API key
- [ ] Submit Ramadan tracker to TestFlight immediately
- [ ] Submit remaining 5 apps within 48 hours

### After Google Play enrollment ($25)
- [ ] Create Google Play listings for all 6 apps
- [ ] Set up service account for automated uploads
- [ ] Submit all 6 apps to internal testing track
- [ ] Promote to production after 3-day review

### After AdMob setup (free)
- [ ] Create ad units for all 6 apps
- [ ] Integrate AdMob plugin in each Capacitor project
- [ ] Test ads in development before submission
- [ ] Configure mediation (optional: add Unity Ads for higher fill)

### After RevenueCat setup (free up to $2,500 MTR)
- [ ] Create products in App Store Connect + Google Play
- [ ] Configure offerings in RevenueCat dashboard
- [ ] Integrate paywall in each app
- [ ] A/B test subscription vs one-time purchase

---

## Common Apple rejection reasons (prevent before submitting)

1. **4.3 Spam** - Apps too similar to each other. Differentiate UI/purpose clearly.
2. **Guideline 2.1 Performance** - App crashes or has bugs. Test on real device first.
3. **Guideline 2.3 Metadata** - Screenshots don't match actual app. Use real screenshots.
4. **Guideline 5.1.1 Data Collection** - Missing privacy policy. Add one to each app.
5. **Guideline 4.2 Minimum Functionality** - "This could be a website." Add native features (notifications, haptics, offline mode) to justify native wrapper.

### How to avoid 4.2 (the PWA killer)

Apple rejects thin PWA wrappers. Add at least 2 native features per app:
- Push notifications (prayer times, habit reminders, focus timer)
- Haptic feedback (step completion, streak milestones)
- Widget support (daily summary on home screen)
- HealthKit integration (WalkToUnlock steps, SleepMaxx sleep data)
- Siri Shortcuts ("Start my focus timer")

### Privacy policy
Every app needs one. Host at `https://printmaxx.com/privacy/{app-name}` or use a free generator. Must cover:
- What data is collected
- How data is used
- Third-party sharing (ad networks)
- Contact info for data deletion requests

---

## Quick reference commands

```bash
# Install all tooling
npm install -g @capacitor/cli @capacitor/core && brew install fastlane cocoapods

# Wrap one app (example: Ramadan)
cd ralph/loops/app_factory/output/ramadan-tracker
npm init -y && npm install @capacitor/core @capacitor/cli
npx cap init "Hilal" "com.printmaxx.hilal" --web-dir .
npx cap add ios && npx cap copy ios
npx cap open ios

# Submit to TestFlight
cd ios/App && fastlane beta

# Submit to App Store
cd ios/App && fastlane release

# Wrap all 6 apps at once
bash scripts/wrap_and_submit_all.sh ios
```

---

## Alpha Insights (Auto-Appended)

_Insights auto-appended by playbook_enhancer.py. Review and integrate as needed._

### Alpha Insight: ALPHA540 — 2026-02-28
**Source:** CNBC ([link](https://www.cnbc.com/2026/01/15/ai-startup-replit-launches-feature-to-vibe-code-mobile-apps.html))
**Category:** APP_FACTORY
**Method:** Replit mobile builder: describe app -> get iOS/Android. Skip Xcode entirely.
**Insight:** Replit mobile app vibe coding launched Jan 2026. Build iOS/Android with natural language. No Xcode needed.
**Potential:** ROI: HIGHEST | Synergy: 95

