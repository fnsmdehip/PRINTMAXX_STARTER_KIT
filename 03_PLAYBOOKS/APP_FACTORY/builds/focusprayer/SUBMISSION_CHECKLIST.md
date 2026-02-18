# PrayerLock Submission Checklist

This checklist covers what needs to be done manually to complete and launch PrayerLock.

## Before You Can Run the App

### 1. Environment Setup (15 min)

- [ ] Install Node.js 18+ (if not already installed)
- [ ] Install Xcode (iOS) or Android Studio (Android)
- [ ] Install CocoaPods: `sudo gem install cocoapods`
- [ ] Install React Native CLI: `npm install -g react-native-cli`

### 2. Initialize React Native Project (30 min)

The code provided is a complete React Native app structure. To run it:

```bash
cd /path/to/prayerlock

# Install dependencies
npm install

# iOS only: Install pods
cd ios && pod install && cd ..

# Start the app
npm run ios    # or npm run android
```

**Note:** You may need to initialize the native iOS/Android folders using:
```bash
npx react-native init PrayerLock --template react-native-template-typescript
```
Then copy the src/ folder and other files over.

## Native Module Implementation Required

### 3. iOS Screen Time API (2-4 hours)

The iOS native module requires implementation in Swift. Key file: `ios/ScreenTimeManager.swift`

Steps:
- [ ] Add FamilyControls capability in Xcode
- [ ] Add ManagedSettings capability in Xcode
- [ ] Add DeviceActivity capability in Xcode
- [ ] Request Screen Time API access from Apple (may take days/weeks)
- [ ] Implement the native bridge following the skeleton in the code

Reference: https://developer.apple.com/documentation/familycontrols

### 4. Android App Blocker (2-4 hours)

The Android native module requires implementation in Kotlin.

Steps:
- [ ] Add UsageStatsManager permissions to AndroidManifest.xml
- [ ] Add SYSTEM_ALERT_WINDOW permission for overlay
- [ ] Create AccessibilityService implementation
- [ ] Implement the native bridge following the skeleton

Required permissions in AndroidManifest.xml:
```xml
<uses-permission android:name="android.permission.PACKAGE_USAGE_STATS" />
<uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW" />
```

## Third-Party Service Setup

### 5. RevenueCat Setup (1 hour)

- [ ] Create account at https://www.revenuecat.com
- [ ] Create a new project "PrayerLock"
- [ ] Add iOS app with bundle ID
- [ ] Add Android app with package name
- [ ] Get API keys and update `src/utils/constants.ts`:
  - `REVENUECAT_IOS_KEY`
  - `REVENUECAT_ANDROID_KEY`
- [ ] Create products in App Store Connect:
  - `prayerlock_monthly` ($9.99/month)
  - `prayerlock_annual` ($49.99/year)
- [ ] Create products in Google Play Console (same IDs)
- [ ] Link products to RevenueCat
- [ ] Create "pro" entitlement

### 6. Firebase Setup (30 min) - Optional for MVP

- [ ] Create Firebase project
- [ ] Add iOS app (GoogleService-Info.plist)
- [ ] Add Android app (google-services.json)
- [ ] Enable Cloud Messaging
- [ ] Install @react-native-firebase packages

## App Store Preparation

### 7. iOS App Store (1-2 hours)

- [ ] Create App Store Connect listing
- [ ] Write app description (use copy from PRD)
- [ ] Create screenshots (6.5" and 5.5" sizes minimum)
- [ ] Create app preview video (optional but recommended)
- [ ] Set age rating (4+)
- [ ] Write privacy policy
- [ ] Write terms of service
- [ ] Configure in-app purchases
- [ ] Submit for review

**App Store Rejection Risks:**
- Screen Time API requires justification
- Clear explanation of app blocking required
- Emergency unlock must be documented
- Subscription terms must be clear

### 8. Google Play Store (1-2 hours)

- [ ] Create Google Play Console listing
- [ ] Write store description
- [ ] Create feature graphic (1024x500)
- [ ] Create screenshots for different device sizes
- [ ] Complete Data Safety section
- [ ] Configure in-app purchases
- [ ] Set content rating
- [ ] Submit for review

**Google Play Rejection Risks:**
- Accessibility Service usage requires justification
- Privacy policy must cover usage data access
- Overlay permission usage must be explained

## Marketing Setup

### 9. Pre-Launch Marketing

- [ ] Create landing page (simple Carrd or Framer page)
- [ ] Set up email collection (ConvertKit or similar)
- [ ] Create TikTok account @prayerlock
- [ ] Create Instagram account @prayerlock
- [ ] Create 5 launch TikToks showing the app
- [ ] Draft launch day email to list
- [ ] Identify 10 Christian influencers to contact

### 10. Post-Launch

- [ ] Monitor App Store reviews daily
- [ ] Respond to all reviews
- [ ] Post 3 TikToks per day minimum
- [ ] Track metrics in RevenueCat dashboard
- [ ] Set up analytics (Mixpanel or Amplitude)

## Legal Documents Required

### 11. Legal (30 min)

- [ ] Privacy Policy - must cover:
  - App usage data collection
  - No data leaves device for MVP
  - Screen Time/Accessibility API usage
  - No sale of user data

- [ ] Terms of Service - must cover:
  - Subscription terms and cancellation
  - Emergency unlock feature
  - App blocking limitations
  - Liability limitations

Use templates from:
- https://www.termsfeed.com
- https://www.iubenda.com

## Testing Before Launch

### 12. Test Checklist

- [ ] Complete onboarding flow
- [ ] Select apps to block
- [ ] Start and complete prayer timer
- [ ] Read scripture passage
- [ ] Verify streak increments
- [ ] Test emergency unlock
- [ ] Test paywall appears after trial
- [ ] Test subscription purchase (sandbox)
- [ ] Test restore purchases
- [ ] Test app blocking works (native module)
- [ ] Test daily reset behavior
- [ ] Test background behavior
- [ ] Test across multiple devices

## Quick Start for Manual Testing

The app can run without native modules for UI testing:

```bash
# Install and run
npm install
npm run ios

# The app will function but won't actually block apps
# Native module stubs return placeholder data
```

## Timeline Estimate

| Task | Time |
|------|------|
| Environment setup | 15 min |
| Project initialization | 30 min |
| iOS native module | 2-4 hours |
| Android native module | 2-4 hours |
| RevenueCat setup | 1 hour |
| App Store submission | 1-2 hours |
| Google Play submission | 1-2 hours |
| Marketing setup | 2-3 hours |
| Legal documents | 30 min |
| Testing | 2-3 hours |
| **Total** | **12-20 hours** |

## Files You Need to Create Manually

1. `ios/` folder - Generated by React Native CLI
2. `android/` folder - Generated by React Native CLI
3. `ios/ScreenTimeManager.swift` - Native module
4. `android/.../AppBlockerModule.kt` - Native module
5. Privacy Policy document
6. Terms of Service document
7. App Store screenshots
8. Marketing assets

## Support

For questions about the React Native code, refer to:
- React Native docs: https://reactnative.dev
- RevenueCat docs: https://docs.revenuecat.com
- Apple Screen Time API: https://developer.apple.com/documentation/familycontrols

The code structure follows standard React Native patterns. Each screen is self-contained with its own styles. The Zustand stores manage all state. Services handle external API calls.
