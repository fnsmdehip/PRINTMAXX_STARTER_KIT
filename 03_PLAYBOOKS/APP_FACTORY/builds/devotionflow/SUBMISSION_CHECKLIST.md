# DailyDevotion Submission Checklist

**App:** DailyDevotion
**Target:** Google Play Store (Android)
**Status:** PRE-SUBMISSION

---

## Human Actions Required

These steps require human intervention and cannot be automated.

### 1. Developer Account Setup

- [ ] Create Google Play Developer account ($25 one-time fee)
  - URL: https://play.google.com/console
  - Requires Google account
  - Takes 24-48 hours for approval

- [ ] Set up developer profile
  - Developer name: [Your Name/Company]
  - Contact email: support@dailydevotion.app
  - Physical address (required for monetized apps)

### 2. RevenueCat Setup

- [ ] Create RevenueCat account (free tier)
  - URL: https://app.revenuecat.com
  - Connect to Google Play Console

- [ ] Create app in RevenueCat
  - App name: DailyDevotion
  - Platform: Android

- [ ] Configure products in RevenueCat
  - `dailydevotion_monthly` - $4.99/month
  - `dailydevotion_yearly` - $29.99/year
  - `dailydevotion_lifetime` - $79.99 (optional)

- [ ] Get RevenueCat API key
  - Add to: `config/revenuecat.json`
  - Add to: app build config

### 3. Google Play Products

- [ ] Create in-app products in Play Console
  - Product ID: `dailydevotion_monthly`
  - Product ID: `dailydevotion_yearly`
  - Match pricing to RevenueCat config

- [ ] Set up subscription groups
  - Group: DailyDevotion Premium
  - Base plan: Monthly
  - Base plan: Annual

### 4. Signing Configuration

- [ ] Generate release keystore
  ```bash
  keytool -genkey -v -keystore dailydevotion-release.keystore \
    -alias dailydevotion -keyalg RSA -keysize 2048 -validity 10000
  ```

- [ ] Store keystore securely (NOT in git)
  - Save to password manager
  - Backup in secure location

- [ ] Configure signing in build.gradle
  - Add keystore path
  - Add key alias
  - Use environment variables for passwords

### 5. Asset Generation

- [ ] Commission dove mascot (or use AI generation)
  - Main app icon (512x512)
  - Mascot variants for animations
  - Simple, recognizable silhouette

- [ ] Generate app icons (all sizes)
  - Use Android Studio Image Asset tool
  - Or: https://icon.kitchen

- [ ] Create store screenshots
  - 2 phone screenshots minimum
  - Use real device or emulator
  - Add marketing text overlays

- [ ] Create feature graphic (1024x500)
  - App name prominent
  - Dove mascot
  - Key features visible

### 6. Build & Test

- [ ] Build release APK/AAB
  ```bash
  ./gradlew bundleRelease
  ```

- [ ] Test on real device
  - Test all features
  - Test subscription flow (sandbox)
  - Test offline behavior

- [ ] Run pre-launch report
  - Upload to Play Console
  - Review automated tests
  - Fix any critical issues

### 7. Store Listing

- [ ] Upload app bundle (.aab)

- [ ] Fill in store listing
  - Title: DailyDevotion: Faith Habit Tracker
  - Short description: (from store_listing/description.md)
  - Full description: (from store_listing/description.md)

- [ ] Add graphics
  - App icon
  - Feature graphic
  - Screenshots (2-8)
  - Video (optional)

- [ ] Set categorization
  - Application type: App
  - Category: Lifestyle
  - Tags: Faith, Habits, Prayer

- [ ] Set content rating
  - Complete questionnaire
  - Expected rating: Everyone

- [ ] Add contact details
  - Support email
  - Privacy policy URL

### 8. Compliance

- [ ] Upload privacy policy
  - Host at: dailydevotion.app/privacy
  - Link in Play Console

- [ ] Complete data safety form
  - Data collected: Habits, preferences
  - Data shared: None
  - Data encrypted: Yes (if applicable)

- [ ] Declare permissions usage
  - Notifications: For habit reminders
  - Internet: For daily verses

### 9. Release

- [ ] Set pricing
  - Free (with in-app purchases)

- [ ] Select countries
  - All countries (recommended)
  - Or specific regions

- [ ] Choose release track
  - Internal testing (first)
  - Closed testing (beta)
  - Production (public)

- [ ] Submit for review
  - Review typically takes 1-3 days
  - May take longer for new accounts

---

## Post-Submission

- [ ] Monitor review status
- [ ] Respond to any rejection reasons
- [ ] Check for policy violation emails
- [ ] Set up crash monitoring alerts

---

## Firebase Setup (Optional but Recommended)

- [ ] Create Firebase project
- [ ] Enable Crashlytics
- [ ] Enable Analytics
- [ ] Add google-services.json to app

---

## Domain & Website Setup

- [ ] Register domain: dailydevotion.app
- [ ] Create simple landing page
- [ ] Host privacy policy
- [ ] Set up support email

---

## Launch Day Checklist

- [ ] App approved and live
- [ ] Test download from Play Store
- [ ] Test subscription purchase
- [ ] Post launch announcement
- [ ] Monitor reviews and ratings
- [ ] Respond to first reviews

---

## Notes

- First submission review may take longer (3-7 days)
- Having complete store listing speeds up review
- Subscriptions require additional review time
- Keep keystore backup secure - losing it means new app listing

---

Created: 2026-01-21
Status: AWAITING HUMAN ACTION
