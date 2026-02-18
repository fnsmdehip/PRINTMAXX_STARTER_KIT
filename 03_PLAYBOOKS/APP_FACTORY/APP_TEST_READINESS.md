# App Test Readiness Report

Generated: 2026-01-21

## Summary

| App | Type | Build Ready | Simulator Ready | Blocking Issues |
|-----|------|-------------|-----------------|-----------------|
| promptvault | Expo | Yes | Yes | Minor - missing assets folder |
| pelvicpro | Expo Router | Yes | Yes | Minor - missing assets folder |
| learnlock | React Native CLI | Partial | No | Missing iOS folder, needs native init |
| focusprayer | React Native CLI | Partial | No | Missing iOS folder, needs native init |
| stepunlock | React Native CLI | Partial | No | Missing iOS folder, needs native init |
| dailyanchor | React Native CLI | Partial | No | Missing iOS folder, needs native init |
| devotionflow | Android (Kotlin) | No | N/A | Fork project, Android only |

## Environment

- Node.js: v20.19.2
- npm: 10.8.2
- Xcode: Installed (confirmed at /Applications/Xcode.app)

---

## Detailed Analysis

### 1. PromptVault (Expo)

**Status: READY FOR TESTING**

**Type:** Expo SDK 50 app

**Configuration:**
- package.json: Complete with expo deps
- app.json: Full Expo config with bundleIdentifier
- Main entry: expo/AppEntry.js

**Source Structure:**
```
src/
  components/
  data/
  navigation/
  screens/
  stores/
  types/
  utils/
```

**Build Commands:**
```bash
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/MONEY_METHODS/APP_FACTORY/builds/promptvault
npm install
npx expo start --ios
```

**Minor Issues:**
- Missing assets/ folder (icon.png, splash.png referenced in app.json)

**Fix Required:**
```bash
mkdir -p assets
# Add placeholder assets or generate with AI
```

**Dependencies:** 13 production deps, well-structured
- expo, expo-clipboard, expo-haptics
- react-navigation stack
- zustand for state
- fuse.js for search

---

### 2. PelvicPro (Expo Router)

**Status: READY FOR TESTING**

**Type:** Expo SDK 51 with expo-router

**Configuration:**
- package.json: Complete with expo-router deps
- app.json: Full Expo config with expo-router plugin
- Main entry: expo-router/entry

**Source Structure:**
```
app/
  (auth)/
  (tabs)/
  _layout.tsx
  exercise/
  paywall.tsx
  workout/
components/
constants/
lib/
store/
```

**Build Commands:**
```bash
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/MONEY_METHODS/APP_FACTORY/builds/pelvicpro
npm install
npx expo start --ios
```

**Minor Issues:**
- Missing assets/images/ folder (icon.png, splash.png, adaptive-icon.png)

**Fix Required:**
```bash
mkdir -p assets/images
# Add placeholder assets
```

**Dependencies:** 17 production deps
- expo-router for file-based routing
- lottie-react-native for animations
- victory-native for charts
- react-native-purchases for subscriptions
- react-native-reanimated for gestures

---

### 3. LearnLock (React Native CLI)

**Status: NEEDS NATIVE SETUP**

**Type:** React Native 0.73.2 CLI project (NOT Expo, despite app.json having expo config)

**Configuration:**
- package.json: React Native CLI scripts (react-native run-ios)
- app.json: Has Expo config but uses CLI
- babel.config.js: react-native specific

**Missing for iOS Build:**
- No ios/ folder (needs `npx react-native init`)
- No Podfile for CocoaPods
- No Xcode project

**Source Structure:**
```
src/
  components/
  hooks/
  navigation/
  screens/
  stores/
  types/
  utils/
App.tsx
```

**Setup Commands:**
```bash
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/MONEY_METHODS/APP_FACTORY/builds/learnlock
npm install

# Initialize native folders
npx react-native init LearnLockTemp --version 0.73.2
cp -r LearnLockTemp/ios ./ios
cp -r LearnLockTemp/android ./android
rm -rf LearnLockTemp

# Install pods
cd ios && pod install && cd ..

# Run
npx react-native run-ios
```

**Dependencies:** 14 production deps
- react-native-background-timer (needs native linking)
- react-native-push-notification (needs native config)
- react-native-purchases

**Blocking Issues:**
1. No iOS folder - cannot build
2. Native modules require linking
3. Push notifications require entitlements

---

### 4. FocusPrayer (React Native CLI)

**Status: NEEDS NATIVE SETUP**

**Type:** React Native 0.73.2 CLI project

**Configuration:**
- package.json: React Native CLI scripts
- app.json: Minimal (name, displayName, slug)
- Has index.js entry point

**Missing for iOS Build:**
- No ios/ folder
- No Podfile
- No Xcode project

**Source Structure:**
```
src/
  native/
  screens/
  services/
  stores/
  types/
  utils/
App.tsx
__tests__/
```

**Setup Commands:**
```bash
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/MONEY_METHODS/APP_FACTORY/builds/focusprayer
npm install

# Initialize native folders
npx react-native init FocusPrayerTemp --version 0.73.2
cp -r FocusPrayerTemp/ios ./ios
cp -r FocusPrayerTemp/android ./android
rm -rf FocusPrayerTemp

# Install pods
cd ios && pod install && cd ..

# Run
npx react-native run-ios
```

**Dependencies:** 11 production deps
- react-native-purchases (RevenueCat)
- react-navigation stack
- zustand

**Blocking Issues:**
1. No iOS folder

---

### 5. StepUnlock (React Native CLI)

**Status: NEEDS NATIVE SETUP**

**Type:** React Native 0.73.2 CLI project

**Configuration:**
- package.json: React Native CLI scripts
- app.json: Minimal
- Has index.js entry point

**Missing for iOS Build:**
- No ios/ folder
- No Podfile
- No Xcode project

**Source Structure:**
```
src/
  App.tsx
  components/
  hooks/
  native/
  screens/
  services/
  stores/
  types/
  utils/
__tests__/
```

**Setup Commands:**
```bash
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/MONEY_METHODS/APP_FACTORY/builds/stepunlock
npm install

# Initialize native folders
npx react-native init StepUnlockTemp --version 0.73.2
cp -r StepUnlockTemp/ios ./ios
cp -r StepUnlockTemp/android ./android
rm -rf StepUnlockTemp

# Configure HealthKit in ios/
# Install pods
cd ios && pod install && cd ..

# Run
npx react-native run-ios
```

**Dependencies:** 15 production deps
- react-native-health (HealthKit - needs entitlements)
- react-native-google-fit (Android)
- react-native-gesture-handler
- react-native-svg

**Blocking Issues:**
1. No iOS folder
2. HealthKit requires entitlements and capabilities
3. Health data requires privacy descriptions

---

### 6. DailyAnchor (React Native CLI)

**Status: NEEDS NATIVE SETUP**

**Type:** React Native 0.73.2 CLI project

**Configuration:**
- package.json: React Native CLI scripts
- app.json: Minimal
- Has index.js entry point

**Missing for iOS Build:**
- No ios/ folder
- No Podfile
- No Xcode project

**Source Structure:**
```
src/
  components/
  hooks/ (empty)
  navigation/
  screens/
  services/ (empty)
  store/
  types/
  utils/
App.tsx
```

**Setup Commands:**
```bash
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/MONEY_METHODS/APP_FACTORY/builds/dailyanchor
npm install

# Initialize native folders
npx react-native init DailyAnchorTemp --version 0.73.2
cp -r DailyAnchorTemp/ios ./ios
cp -r DailyAnchorTemp/android ./android
rm -rf DailyAnchorTemp

# Install pods
cd ios && pod install && cd ..

# Run
npx react-native run-ios
```

**Dependencies:** 11 production deps
- date-fns for date handling
- react-native-purchases
- Standard navigation stack

**Blocking Issues:**
1. No iOS folder
2. Some folders empty (hooks, services)

---

### 7. DevotionFlow (Android Only - Fork Project)

**Status: NOT BUILDABLE IN CURRENT STATE**

**Type:** Android Kotlin project (fork of Loop Habit Tracker)

**Configuration:**
- No package.json (not a JS project)
- No app.json
- Kotlin source files only

**Current Structure:**
```
README.md
SUBMISSION_CHECKLIST.md
config/
src/main/
  java/com/dailydevotion/app/core/
    mascot/DoveMascot.kt
    models/Models.kt
    templates/FaithTemplates.kt, HabitTemplate.kt
    verse/BibleApiService.kt, VerseOfDayService.kt
  res/
    layout/
    values/
store_listing/
```

**Build Process (Per README):**
```bash
# 1. Clone base repo
git clone https://github.com/iSoron/uhabits.git
cd uhabits

# 2. Copy modification files
cp -r ../devotionflow/src/* uhabits-android/src/

# 3. Update package names
# 4. Build
./gradlew assembleDebug
```

**Blocking Issues:**
1. Android only - no iOS simulator testing possible
2. Requires cloning separate repo
3. Requires manual package name changes
4. No React Native - pure Android Kotlin

---

## Priority Order for Testing

### Tier 1: Ready Now
1. **PromptVault** - Just needs npm install + asset placeholders
2. **PelvicPro** - Just needs npm install + asset placeholders

### Tier 2: Needs Native Init (30 min setup each)
3. **FocusPrayer** - Simplest native setup
4. **DailyAnchor** - Standard setup
5. **LearnLock** - Needs push notification config
6. **StepUnlock** - Needs HealthKit entitlements

### Tier 3: Not iOS Testable
7. **DevotionFlow** - Android only fork project

---

## Quick Start Commands

### Test PromptVault Now:
```bash
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/MONEY_METHODS/APP_FACTORY/builds/promptvault
mkdir -p assets
npm install
npx expo start --ios
```

### Test PelvicPro Now:
```bash
cd /Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/MONEY_METHODS/APP_FACTORY/builds/pelvicpro
mkdir -p assets/images
npm install
npx expo start --ios
```

---

## Required Manual Steps Summary

| Step | Apps Affected | Time Estimate |
|------|---------------|---------------|
| Create placeholder assets | promptvault, pelvicpro | 5 min |
| Initialize iOS folders | focusprayer, stepunlock, learnlock, dailyanchor | 10 min each |
| Pod install | All React Native CLI | 5 min each |
| HealthKit entitlements | stepunlock | 15 min |
| Push notification config | learnlock | 15 min |
| Clone Loop Habit Tracker | devotionflow | 30 min |

---

## Recommendations

1. **Start with Expo apps** (promptvault, pelvicpro) - they can run in simulator immediately after npm install

2. **Batch the React Native CLI setup** - All 4 apps need the same iOS folder initialization

3. **Skip devotionflow for now** - Android-only fork requires separate tooling

4. **Create a shared assets script** - Generate placeholder icons/splash for all apps at once

5. **Consider converting RN CLI to Expo** - Would simplify builds significantly
