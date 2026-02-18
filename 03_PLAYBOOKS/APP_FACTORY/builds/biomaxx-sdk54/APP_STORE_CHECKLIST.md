# BioMaxx App Store Submission Checklist

**Last Updated:** 2026-01-28

---

## Pre-Submission Requirements

### App Configuration
- [x] Bundle ID set: `com.printmaxx.biomaxx`
- [x] Android package: `com.printmaxx.biomaxx`
- [x] Version: 1.0.0
- [x] App icon configured (./assets/icon.png)
- [x] Splash screen configured with correct background (#0F172A)
- [x] Adaptive icon configured (Android)
- [x] EAS build config created (eas.json)
- [x] Dark theme splash (no white flash)
- [ ] App icon is NOT a placeholder (verify it's a real designed icon)

### Privacy & Legal
- [ ] Privacy policy URL hosted and accessible
- [ ] Terms of service URL hosted and accessible
- [ ] Privacy policy linked in Settings screen (currently placeholder Alert)
- [ ] Terms of service linked in Settings screen (currently placeholder Alert)
- [ ] Health data usage descriptions in Info.plist (added)
- [ ] No unsubstantiated health claims in app
- [x] Medical disclaimer present in Profile screen
- [x] FTC affiliate disclosure on recommendations

### Monetization
- [ ] RevenueCat SDK installed (react-native-purchases)
- [ ] RevenueCat account created and configured
- [ ] Subscription products created in App Store Connect:
  - Monthly: $9.99/month
  - Annual: $79.99/year
- [ ] Paywall screen shows real products (not Alert placeholder)
- [ ] Restore purchases functionality works
- [ ] Subscription terms visible on paywall
- [ ] Cancel instructions provided

### Content
- [ ] All Learn articles have real content (currently excerpts only)
- [ ] Article content reviewed for accuracy
- [ ] No copyrighted content

### Screenshots (iOS)
- [ ] iPhone 6.5" (1242 x 2688) - 5 screenshots minimum
  - [ ] Dashboard with daily progress
  - [ ] Protocol tracking with timer
  - [ ] Learn section with articles
  - [ ] Profile with achievements
  - [ ] Paywall/Premium features
- [ ] iPad 12.9" (2048 x 2732) - if supporting tablet
- [ ] App Preview video (15-30 sec, optional but recommended)

### App Store Metadata
- [ ] App name: BioMaxx
- [ ] Subtitle (30 chars): "Biohacking Protocol Tracker"
- [ ] Category: Health & Fitness
- [ ] Keywords (100 chars): biohacking,longevity,fasting,cold,exposure,protocol,health,tracker,sauna,supplements
- [ ] Description (4000 chars) written
- [ ] Promotional text (170 chars)
- [ ] Support URL
- [ ] Marketing URL (optional)
- [ ] Age rating: 4+

### Testing
- [ ] npm install completed successfully
- [ ] App launches in iOS Simulator
- [ ] Onboarding flow completes
- [ ] Can log a protocol
- [ ] Timer starts, pauses, and ends correctly
- [ ] Streak increments on daily use
- [ ] Achievements unlock correctly
- [ ] Profile shows correct stats
- [ ] Learn articles display
- [ ] Premium gating works (locked protocols show lock icon)
- [ ] App persists data after restart
- [ ] Dark mode displays correctly (no white elements)
- [ ] All haptic feedback triggers

### Build & Submit
- [ ] Run `eas build --platform ios --profile production`
- [ ] Upload to App Store Connect
- [ ] Fill in all metadata
- [ ] Submit for review
- [ ] Monitor review status

---

## Post-Launch
- [ ] Monitor crash reports
- [ ] Respond to reviews within 24 hours
- [ ] A/B test screenshots after 2 weeks
- [ ] Track conversion rate by keyword
