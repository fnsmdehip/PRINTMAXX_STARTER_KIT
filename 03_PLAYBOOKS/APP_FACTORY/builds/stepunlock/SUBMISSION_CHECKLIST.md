# WalkToUnlock Submission Checklist

Manual steps required before the app can be built and submitted.

## Pre-Development Setup

### 1. React Native Environment
- [ ] Install Node.js 18+
- [ ] Install Watchman: `brew install watchman`
- [ ] Install CocoaPods: `sudo gem install cocoapods`
- [ ] Install Xcode (latest from App Store)
- [ ] Install Android Studio with SDK

### 2. Project Initialization
- [ ] Run `npm install` in the walktounlock directory
- [ ] Run `npx pod-install` for iOS dependencies
- [ ] Create `ios/` and `android/` folders using: `npx react-native init WalkToUnlock --template react-native-template-typescript`
- [ ] Copy the src files into the initialized project

## API Keys and Configuration

### 3. RevenueCat Setup
- [ ] Create RevenueCat account at https://www.revenuecat.com
- [ ] Create new project "WalkToUnlock"
- [ ] Add iOS app with bundle ID: `com.yourname.walktounlock`
- [ ] Add Android app with package name: `com.yourname.walktounlock`
- [ ] Create entitlement: `premium`
- [ ] Create offerings with monthly ($7.99) and annual ($39.99) packages
- [ ] Copy iOS API key to `src/utils/constants.ts` (REVENUECAT_API_KEY_IOS)
- [ ] Copy Android API key to `src/utils/constants.ts` (REVENUECAT_API_KEY_ANDROID)

### 4. App Store Connect Setup (iOS)
- [ ] Create new app in App Store Connect
- [ ] Set bundle ID: `com.yourname.walktounlock`
- [ ] Create App Store Connect API key for Fastlane
- [ ] Enable HealthKit capability in Xcode
- [ ] Enable Background Modes (Background fetch)
- [ ] Add FamilyControls capability for app blocking

### 5. Google Play Console Setup (Android)
- [ ] Create new app in Google Play Console
- [ ] Set package name: `com.yourname.walktounlock`
- [ ] Create service account for Fastlane
- [ ] Enable Google Fit API in Google Cloud Console
- [ ] Create OAuth consent screen

## iOS Configuration

### 6. Info.plist Additions
Add these to `ios/WalkToUnlock/Info.plist`:
```xml
<key>NSHealthShareUsageDescription</key>
<string>WalkToUnlock needs access to your step count to track your daily walking progress.</string>

<key>UIBackgroundModes</key>
<array>
    <string>fetch</string>
</array>

<key>NSFamilyControlsUsageDescription</key>
<string>WalkToUnlock uses Screen Time to block distracting apps until you hit your step goal.</string>
```

### 7. Xcode Capabilities
- [ ] Sign in with Apple Developer account
- [ ] Enable HealthKit
- [ ] Enable Background Modes > Background fetch
- [ ] Enable Family Controls (requires Apple approval)

### 8. Native Module Integration
- [ ] Add Swift files from `src/native/ios/` to Xcode project
- [ ] Create bridging header if needed
- [ ] Link HealthKit framework

## Android Configuration

### 9. AndroidManifest.xml Additions
Add to `android/app/src/main/AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.ACTIVITY_RECOGNITION" />
<uses-permission android:name="android.permission.PACKAGE_USAGE_STATS" tools:ignore="ProtectedPermissions" />
<uses-permission android:name="android.permission.BIND_ACCESSIBILITY_SERVICE" tools:ignore="ProtectedPermissions" />
```

### 10. Google Fit OAuth
- [ ] Configure OAuth consent screen in Google Cloud Console
- [ ] Add Fitness API scope: `https://www.googleapis.com/auth/fitness.activity.read`
- [ ] Add SHA-1 certificate fingerprint for debug and release

### 11. Native Module Integration
- [ ] Add Kotlin files from `src/native/android/` to project
- [ ] Register modules in MainApplication.kt
- [ ] Add Google Play Services Fitness dependency to build.gradle

## Testing

### 12. Local Testing
- [ ] Run `npm test` to verify unit tests pass
- [ ] Run on iOS Simulator: `npm run ios`
- [ ] Run on Android Emulator: `npm run android`
- [ ] Test HealthKit permissions flow on real iOS device
- [ ] Test Google Fit permissions flow on real Android device
- [ ] Verify step counting works in background
- [ ] Test subscription purchase flow with sandbox accounts

### 13. Beta Testing
- [ ] Upload to TestFlight
- [ ] Add 20+ beta testers
- [ ] Collect feedback for 1 week minimum
- [ ] Upload to Google Play Internal Testing track
- [ ] Test on multiple device sizes

## App Store Submission

### 14. App Store Screenshots
- [ ] Create 6.7" iPhone screenshots (1290 x 2796)
- [ ] Create 6.5" iPhone screenshots (1284 x 2778)
- [ ] Create 12.9" iPad screenshots if supporting iPad
- [ ] Create Android phone screenshots (varies by device)
- [ ] Create feature graphic for Google Play (1024 x 500)

### 15. App Store Listing
- [ ] Write app description (no promotional language)
- [ ] List key features
- [ ] Add privacy policy URL
- [ ] Add support URL
- [ ] Set age rating (4+)
- [ ] Select Health & Fitness category
- [ ] Add relevant keywords

### 16. Privacy Policy
- [ ] Create privacy policy covering:
  - Step data collection (stays on device)
  - No third-party data sharing
  - Subscription information
  - Contact information
- [ ] Host at accessible URL
- [ ] Add URL to app stores and app settings

### 17. Review Notes for Apple
Include in App Store Connect review notes:
```
Demo Account: Not required (app works without account)

Testing Steps:
1. Allow HealthKit access when prompted
2. Set a step goal (try 100 steps for easy testing)
3. Walk to generate steps
4. When goal is reached, blocked apps unlock automatically

Note: App blocking uses FamilyControls. We request authorization during onboarding.
The 3-day free trial is automatic and does not require credit card.
```

### 18. Submit for Review
- [ ] Verify all metadata is complete
- [ ] Submit iOS build to App Store review
- [ ] Submit Android build to Google Play review
- [ ] Monitor review status
- [ ] Respond to any rejection issues

## Post-Launch

### 19. Marketing Setup
- [ ] Create TikTok account (@walktounlock)
- [ ] Record 5 launch videos showing app in use
- [ ] Set up website/landing page
- [ ] Prepare launch day posts

### 20. Analytics Configuration
- [ ] Verify Mixpanel events are firing
- [ ] Set up RevenueCat charts dashboard
- [ ] Configure crash reporting (Sentry/Crashlytics)
- [ ] Set up custom events for key actions

### 21. Support Infrastructure
- [ ] Set up support email (support@walktounlock.com)
- [ ] Create FAQ document
- [ ] Set up app review monitoring

## Important Notes

### FamilyControls Approval (iOS)
Apple requires special approval to use the Screen Time API (FamilyControls). You must:
1. Apply at https://developer.apple.com/contact/request/family-controls-distribution
2. Explain your use case clearly
3. Wait for approval before submitting to App Store
4. This can take 1-4 weeks

### Google Fit API Approval (Android)
Google requires OAuth verification for fitness apps:
1. Submit OAuth consent screen for verification
2. Provide privacy policy and homepage
3. Wait for verification (can take days to weeks)

### App Blocking Limitations
- iOS: FamilyControls only works on iOS 16+
- Android: Requires accessibility service which may trigger Play Store review
- Consider alternative: "soft blocking" with overlay screens instead of true app blocking

---

## Quick Commands

```bash
# Install dependencies
npm install

# Run tests
npm test

# Start Metro bundler
npm start

# Run iOS
npm run ios

# Run Android
npm run android

# Type check
npm run typecheck

# Lint
npm run lint
```

## File Structure Summary

```
walktounlock/
├── src/
│   ├── components/     # UI components
│   ├── screens/        # App screens
│   ├── services/       # Business logic
│   ├── stores/         # Zustand state
│   ├── native/         # Native module code
│   ├── types/          # TypeScript types
│   ├── utils/          # Utilities
│   └── App.tsx         # Main entry
├── __tests__/          # Test files
├── package.json
├── tsconfig.json
└── SUBMISSION_CHECKLIST.md
```

## Estimated Timeline

| Phase | Duration |
|-------|----------|
| Environment setup | 1-2 hours |
| API configuration | 2-4 hours |
| Native module integration | 4-8 hours |
| Local testing | 2-4 hours |
| Beta testing | 1 week |
| App Store prep | 2-4 hours |
| Review process | 1-5 days (iOS), 1-3 days (Android) |
| **Total** | **2-3 weeks** |

## Support

If you encounter issues:
1. Check React Native docs: https://reactnative.dev/docs/getting-started
2. Check RevenueCat docs: https://docs.revenuecat.com
3. Check HealthKit docs: https://developer.apple.com/documentation/healthkit
4. Check Google Fit docs: https://developers.google.com/fit
