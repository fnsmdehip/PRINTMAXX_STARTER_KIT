# RevenueCat Quick Setup - All 4 Apps

**Created:** 2026-02-01
**Time Required:** 2-3 hours total
**Apps:** biomaxx, PrayerLock, WalkToUnlock, StudyLock

---

## Step-by-Step Setup

### Step 1: Create RevenueCat Account (5 min)

1. Go to https://app.revenuecat.com/signup
2. Sign up with email
3. Choose "Free" plan (up to $2,500 MRR)
4. Verify email

### Step 2: Create Projects (20 min - 5 min per app)

**For EACH app (biomaxx, PrayerLock, WalkToUnlock, StudyLock):**

1. Click "+ New App"
2. App name: `[AppName]`
3. Platform: iOS + Android (both)
4. Click "Create"

You should now have 4 projects in RevenueCat dashboard.

### Step 3: Configure iOS for Each App (60 min - 15 min per app)

**For EACH app:**

1. In RevenueCat → [App] → Platform Configuration → iOS
2. Bundle ID: (get from Xcode project)
   - biomaxx: `com.printmaxx.biomaxx`
   - PrayerLock: `com.printmaxx.prayerlock`
   - WalkToUnlock: `com.printmaxx.walktounlock`
   - StudyLock: `com.printmaxx.studylock`

3. Shared Secret: (from App Store Connect)
   - App Store Connect → Apps → [App] → General → App Information
   - Scroll to "App-Specific Shared Secret"
   - Click "Generate" if not exists
   - Copy and paste into RevenueCat

4. In-App Purchase Key: (from App Store Connect)
   - App Store Connect → Users & Access → Keys → In-App Purchase
   - Click "+" to generate key
   - Download `.p8` file
   - Upload to RevenueCat

5. Save iOS configuration

### Step 4: Configure Android for Each App (60 min - 15 min per app)

**For EACH app:**

1. In RevenueCat → [App] → Platform Configuration → Android
2. Package name: (get from `android/app/build.gradle`)
   - biomaxx: `com.printmaxx.biomaxx`
   - PrayerLock: `com.printmaxx.prayerlock`
   - WalkToUnlock: `com.printmaxx.walktounlock`
   - StudyLock: `com.printmaxx.studylock`

3. Service Account JSON: (from Google Play Console)
   - Play Console → Setup → API Access
   - Click "Create Service Account"
   - Follow link to Google Cloud Console
   - Create service account with "Owner" role
   - Create JSON key
   - Download and upload to RevenueCat

4. Save Android configuration

### Step 5: Create Products in App Store Connect (40 min - 10 min per app)

**For EACH app:**

1. App Store Connect → Apps → [App] → Subscriptions
2. Click "+ Create Subscription Group"
3. Reference Name: `[App] Premium`
4. Click "Create"

**Create Annual Product:**
5. Click "+ Create Subscription"
6. Reference Name: `[App] Annual`
7. Product ID: `[app]_annual` (lowercase, underscore)
   - biomaxx_annual
   - prayerlock_annual
   - walktounlock_annual
   - studylock_annual
8. Duration: 1 Year
9. Price:
   - biomaxx: $35.99
   - PrayerLock: $29.99
   - WalkToUnlock: $24.99
   - StudyLock: $29.99
10. Subscription Group: (select the one you just created)
11. Click "Create"

**Add Free Trial:**
12. Scroll to "Subscription Prices"
13. Click "Add Introductory Offer"
14. Type: Free
15. Duration: 7 Days
16. Countries: All
17. Save

**Create Monthly Product:**
18. Repeat steps 5-17 with:
    - Product ID: `[app]_monthly`
    - Duration: 1 Month
    - Price:
      - biomaxx: $9.99
      - PrayerLock: $4.99
      - WalkToUnlock: $3.99
      - StudyLock: $4.99

**Add Localization:**
19. For each product → Subscription Localization → Add Language
20. Language: English (US)
21. Subscription Display Name:
    - Annual: "Annual Plan"
    - Monthly: "Monthly Plan"
22. Description:
    - Annual: "Full access to all features"
    - Monthly: "Full access, billed monthly"
23. Save

### Step 6: Create Products in Google Play Console (40 min - 10 min per app)

**For EACH app:**

1. Play Console → [App] → Monetize → Subscriptions
2. Click "Create subscription"

**Annual Product:**
3. Product ID: `[app]_annual` (MUST match iOS exactly)
4. Name: Annual Plan
5. Description: Full access to all features
6. Billing period: Yearly (every 1 year)
7. Base plan:
   - Price: (same as iOS)
   - Free trial: 7 days
   - Auto-renewing: Yes
8. Save and activate

**Monthly Product:**
9. Repeat for `[app]_monthly`
10. Billing period: Monthly (every 1 month)
11. Price: (same as iOS)
12. Free trial: 7 days
13. Save and activate

### Step 7: Create Entitlements in RevenueCat (20 min - 5 min per app)

**For EACH app:**

1. RevenueCat → [App] → Entitlements
2. Click "+ New Entitlement"
3. Identifier: `premium` (lowercase, no spaces)
4. Description: "Full access to [App] features"
5. Attached Products:
   - Click "+ Attach Product"
   - iOS: Select `[app]_annual` and `[app]_monthly`
   - Android: Select `[app]_annual` and `[app]_monthly`
6. Save

### Step 8: Create Offerings in RevenueCat (20 min - 5 min per app)

**For EACH app:**

1. RevenueCat → [App] → Offerings
2. Click "+ New Offering"
3. Identifier: `default`
4. Description: "Default paywall offering"
5. Set as Current: ✓ (checkbox)
6. Packages:

**Package 1 (Annual):**
7. Click "+ New Package"
8. Identifier: `$rc_annual` (exactly this, case-sensitive)
9. Product:
   - iOS: `[app]_annual`
   - Android: `[app]_annual`
10. Position: 0 (shows first)
11. Save

**Package 2 (Monthly):**
12. Click "+ New Package"
13. Identifier: `$rc_monthly` (exactly this)
14. Product:
   - iOS: `[app]_monthly`
   - Android: `[app]_monthly`
15. Position: 1 (shows second)
16. Save

17. Save offering

### Step 9: Get API Keys (10 min)

**For EACH app:**

1. RevenueCat → [App] → API Keys
2. Copy the keys:
   - iOS API Key: starts with `rcb_`
   - Android API Key: also starts with `rcb_`
   - Public API Key: starts with `pk_` (optional)

3. Add to your app's `.env` file or config:
```
# biomaxx
REVENUECAT_IOS_BIOMAXX=rcb_xxx...
REVENUECAT_ANDROID_BIOMAXX=rcb_yyy...

# PrayerLock
REVENUECAT_IOS_PRAYERLOCK=rcb_xxx...
REVENUECAT_ANDROID_PRAYERLOCK=rcb_yyy...

# WalkToUnlock
REVENUECAT_IOS_WALKTOUNLOCK=rcb_xxx...
REVENUECAT_ANDROID_WALKTOUNLOCK=rcb_yyy...

# StudyLock
REVENUECAT_IOS_STUDYLOCK=rcb_xxx...
REVENUECAT_ANDROID_STUDYLOCK=rcb_yyy...
```

### Step 10: Integrate SDK in Apps (30 min total)

**1. Install SDK (once, applies to all apps if using monorepo):**
```bash
npm install react-native-purchases
cd ios && pod install && cd ..
```

**2. Configure in each app's `App.tsx`:**
```typescript
import Purchases from 'react-native-purchases';
import { Platform } from 'react-native';

// In app initialization (useEffect or componentDidMount)
async function initRevenueCat() {
  const apiKey = Platform.OS === 'ios'
    ? process.env.REVENUECAT_IOS_[APP]
    : process.env.REVENUECAT_ANDROID_[APP];

  await Purchases.configure({ apiKey });
}
```

**3. Add paywall screen** (see HARD_PAYWALL_IMPLEMENTATION_GUIDE.md for full code)

### Step 11: Test with Sandbox (30 min)

**iOS:**
1. App Store Connect → Users & Access → Sandbox Testers
2. Create test account: test@example.com (fake email, not real Apple ID)
3. On iPhone: Settings → App Store → Sandbox Account
4. Sign in with test account
5. Launch app → test purchase flow

**Android:**
1. Play Console → Setup → License Testing
2. Add your real Gmail to license testers
3. Sign in to Play Store with that Gmail
4. Install app from internal testing track
5. Test purchase

---

## Verification Checklist

After setup, verify everything works:

**RevenueCat Dashboard:**
- [ ] 4 projects created (biomaxx, PrayerLock, WalkToUnlock, StudyLock)
- [ ] Each project has iOS + Android configured
- [ ] Each project has 2 products (annual + monthly)
- [ ] Each project has 1 entitlement (`premium`)
- [ ] Each project has 1 offering (`default`)
- [ ] API keys copied to app config

**App Store Connect:**
- [ ] 4 apps exist
- [ ] Each app has 2 subscriptions (annual + monthly)
- [ ] Each subscription has 7-day free trial
- [ ] Each subscription has pricing set
- [ ] Each subscription has localization (English)
- [ ] Each subscription is approved/ready for sale

**Google Play Console:**
- [ ] 4 apps exist
- [ ] Each app has 2 subscriptions (annual + monthly)
- [ ] Product IDs match iOS exactly
- [ ] Pricing matches iOS
- [ ] Free trials configured
- [ ] Subscriptions activated

**In App:**
- [ ] SDK installed
- [ ] API keys configured
- [ ] Paywall screen implemented
- [ ] Purchase flow tested in sandbox
- [ ] Entitlement check working
- [ ] Restore purchases working

---

## Quick Reference

**Product IDs:**
```
biomaxx_annual         biomaxx_monthly
prayerlock_annual      prayerlock_monthly
walktounlock_annual    walktounlock_monthly
studylock_annual       studylock_monthly
```

**Pricing:**
```
biomaxx:        $35.99/year  $9.99/month
PrayerLock:     $29.99/year  $4.99/month
WalkToUnlock:   $24.99/year  $3.99/month
StudyLock:      $29.99/year  $4.99/month
```

**Trial:** 7 days for all products

**Entitlement ID:** `premium` (same for all apps)

**Offering ID:** `default` (same for all apps)

**Package IDs:** `$rc_annual`, `$rc_monthly` (same for all apps)

---

## Timeline

| Task | Time | When |
|------|------|------|
| Create RevenueCat account + projects | 30 min | Day 1 |
| Configure iOS (all 4 apps) | 60 min | Day 1 |
| Configure Android (all 4 apps) | 60 min | Day 1 |
| Create products in ASC | 40 min | Day 1-2 |
| Create products in Play Console | 40 min | Day 1-2 |
| Create entitlements + offerings | 40 min | Day 2 |
| Get API keys | 10 min | Day 2 |
| Integrate SDK | 30 min | Day 2-3 |
| Test in sandbox | 30 min | Day 3 |
| **Total** | **5-6 hours** | **Across 3 days** |

---

## Support

**RevenueCat Docs:**
- https://docs.revenuecat.com

**RevenueCat Community:**
- https://community.revenuecat.com

**Apple Subscriptions Guide:**
- https://developer.apple.com/app-store/subscriptions/

**Google Play Billing:**
- https://developer.android.com/google/play/billing

**Issues?**
- Check RevenueCat Community first
- RevenueCat support: support@revenuecat.com
- Response time: usually < 24 hours

---

## This is the foundation for 8x revenue. Set it up properly once, it scales forever.
