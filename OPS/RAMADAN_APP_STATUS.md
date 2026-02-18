# Ramadan App (Hilal) - iOS Submission Status

Updated: 2026-02-12
Ramadan starts: 2026-02-28 (16 days away)

## Current status: BUILDS AND RUNS IN iOS SIMULATOR

### What's done
- [x] Capacitor CLI installed globally
- [x] npm dependencies installed (capacitor/core, ios, push-notifications, geolocation, local-notifications)
- [x] iOS platform added and synced
- [x] Web assets copied to ios/App/App/public/
- [x] Xcode project compiles (BUILD SUCCEEDED)
- [x] App installs and runs in iPhone 16 Simulator
- [x] Onboarding screen verified: bilingual EN/AR, crescent logo, language selector, pagination dots
- [x] Pod dependencies resolved (CapacitorPushNotifications, CapacitorGeolocation, CapacitorLocalNotifications)

### What's needed for App Store submission
- [ ] Apple Developer account ($99/yr) - BLOCKER
- [ ] App icon: replace SVG data URI with proper 1024x1024 PNG (AppIcon.appiconset)
- [ ] Launch screen: replace default Capacitor splash with branded Hilal splash
- [ ] Privacy policy URL (hosted, required by App Store)
- [ ] App Store screenshots (6.7" and 6.1" required)
- [ ] App Store metadata (description, keywords, category)
- [ ] Bundle signing with distribution certificate
- [ ] TestFlight beta upload
- [ ] App Review submission

### App details
- Bundle ID: com.hilal.ramadan
- App name: Hilal
- Display name: Hilal - Ramadan Companion
- Category: Lifestyle / Health & Fitness
- Languages: English, Arabic
- Min iOS version: 13.0 (Capacitor default)

### File locations
- Web source: ralph/loops/app_factory/output/ramadan-tracker/
- Capacitor project: ralph/loops/app_factory/output/ramadan-tracker/native-wrapper/
- iOS Xcode project: ralph/loops/app_factory/output/ramadan-tracker/native-wrapper/ios/App/
- Capacitor config: ralph/loops/app_factory/output/ramadan-tracker/native-wrapper/capacitor.config.ts
- ASO content: ralph/loops/app_factory/output/ramadan-tracker/ASO_CONTENT.md
- Marketing: ralph/loops/app_factory/output/ramadan-tracker/MARKETING_BLITZ.md
- Privacy policy: ralph/loops/app_factory/output/ramadan-tracker/native-wrapper/PRIVACY_POLICY.md
- Terms of service: ralph/loops/app_factory/output/ramadan-tracker/native-wrapper/TERMS_OF_SERVICE.md

### Fixes applied
- Changed webDir from `../` to `www` (Capacitor 6 rejects relative parent paths)
- Created www/ directory with copies of index.html, manifest.json, sw.js
- Removed deprecated `bundledWebRuntime` config option

### To open in Xcode
```bash
cd ralph/loops/app_factory/output/ramadan-tracker/native-wrapper
npx cap open ios
```

### To rebuild after web changes
```bash
cd ralph/loops/app_factory/output/ramadan-tracker/native-wrapper
cp ../index.html www/
cp ../manifest.json www/
cp ../sw.js www/
npx cap sync ios
```

### Apple 4.2 rejection prevention
The app already has native plugin support for:
- Push notifications (prayer time reminders)
- Local notifications (iftar/suhoor alerts)
- Geolocation (automatic prayer time calculation)

These native features justify the app beyond a simple web wrapper.
Additional features to consider before submission:
- Haptic feedback on fasting timer completion
- HealthKit integration (fasting hours tracking)
- Widget for home screen (daily countdown)
