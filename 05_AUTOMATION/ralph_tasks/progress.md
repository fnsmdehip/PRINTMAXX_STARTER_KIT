# Ralph Loop Progress Log

## 2025-01-21 Session

### Completed Tasks

#### Task 001: Generate app icons
- Generated 9 high-quality app icons using Gemini browser
- Icons saved to: `MONEY_METHODS/APP_FACTORY/assets/icons/`
- Copied to: `LANDING/printmaxx-site/public/icons/`
- Copied to: `builds/{app}/assets/icon.png`

#### Task 002: Render intro videos
- Rendered 10 intro videos (PrayerLock, WalkToUnlock, StudyLock, etc.)
- Output: `LANDING/printmaxx-site/out/` (~1MB each)

#### Task 003: Render promo videos with icons
- Fixed staticFile paths for Remotion icon loading
- Rendered 8 promo videos with actual app icons
- Output: `LANDING/printmaxx-site/out/promos/` (~550-610KB each)
- Distributed to: `builds/{app}/marketing/videos/`

### Blocked Tasks

#### Task 004: iOS Simulator EMFILE error
- **Error:** `EMFILE: too many open files, watch`
- **Cause:** System file descriptor limit reached (~17k open files)
- **Top consumers:** Brave Browser (2974), Google Chrome (1266)
- **Attempted fixes:**
  - Killed Metro/Expo/Watchman processes
  - Cleared caches
  - Set CHOKIDAR_USEPOLLING=true
- **Solution needed:** Close browser tabs, restart laptop, or increase system limits via launchd

#### Task 005: Expo Go version mismatch
- **Error:** "Project is incompatible with this version of Expo Go"
- **Required:** Expo Go 2.31.6 for SDK 51.0.0
- **Installed:** Expo Go 2.30.10
- **Solution:** Update Expo Go in simulator (requires iOS Simulator working first)

### Learnings

1. **Remotion staticFile()** - Must use `staticFile('path')` for public folder assets, not `/path`
2. **EMFILE prevention** - Keep browser tabs minimal during Expo development
3. **Expo Go updates** - Need matching SDK version between project and Expo Go app
4. **React Native 0.74 + Xcode 18.4** - Build issues with std::char_traits, may need RN update

### Next Actions (Auto-execute)

1. When EMFILE resolved, run: `cd builds/biomaxx && npx expo start --ios`
2. Take screenshots of each running app
3. Generate App Store screenshots using Remotion
4. Set up RevenueCat subscriptions
