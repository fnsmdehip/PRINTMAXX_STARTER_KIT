# PrayerLock App Store Submission Checklist

**Last Updated:** 2026-01-28

---

## Pre-Submission Requirements

### App Configuration
- [x] Bundle ID: `com.printmaxx.prayerlock`
- [x] Android package: `com.printmaxx.prayerlock`
- [x] Version: 1.0.0
- [x] URL scheme: `prayerlock`
- [x] App icon configured (./assets/icon.png)
- [x] Splash screen (#1a1a2e dark background)
- [x] Adaptive icon (Android)
- [x] EAS build config created
- [x] Notifications plugin configured
- [ ] App icon is NOT Expo default (verify visually)

### Privacy & Legal
- [x] Privacy policy linked (printmaxx.com/privacy)
- [x] Terms of service linked (printmaxx.com/terms)
- [ ] Privacy policy page actually hosted and accessible
- [ ] Terms of service page actually hosted and accessible
- [x] Notification permission requested appropriately
- [x] No unsubstantiated claims

### Monetization
- [ ] RevenueCat SDK installed (react-native-purchases)
- [ ] RevenueCat account created
- [ ] Products created in App Store Connect:
  - Monthly: $9.99/month
  - Annual: $49.99/year
- [ ] Paywall wired to RevenueCat (currently Alert)
- [ ] Restore Purchases wired to RevenueCat
- [ ] 3-day trial configured
- [ ] Subscription terms visible
- [x] Cancel anytime messaging present

### Features Verified
- [x] Onboarding flow works (4 slides + skip)
- [x] Prayer timer starts, runs, completes
- [x] Scripture reading with minimum time gate
- [x] Emergency unlock with typed confirmation
- [x] Streak tracking persists across restarts
- [x] Settings (duration, toggles) persist
- [x] Trial countdown displays correctly
- [x] Paywall appears after trial expires
- [x] Dynamic greeting (morning/afternoon/evening)
- [x] Cross-promotion (More Apps section)
- [x] Daily notification scheduling

### Screenshots (iOS)
- [ ] iPhone 6.5" (1242 x 2688) - 5 minimum:
  - [ ] Home screen with streak card
  - [ ] Prayer timer running
  - [ ] Scripture reader with verse
  - [ ] Stats/progress calendar grid
  - [ ] Paywall with feature list
- [ ] iPad 12.9" (2048 x 2732) - if supporting tablet

### App Store Metadata
- [ ] App name: PrayerLock
- [ ] Subtitle: "Pray Before You Scroll"
- [ ] Category: Lifestyle (or Health & Fitness)
- [ ] Keywords: prayer,devotional,bible,scripture,streak,christian,faith,habit,morning,timer
- [ ] Description written
- [ ] Promotional text
- [ ] Age rating: 4+
- [ ] Support URL
- [ ] Marketing URL

### Build & Submit
- [ ] Run `eas build --platform ios --profile production`
- [ ] Upload to App Store Connect
- [ ] Submit for review
