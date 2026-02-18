# RevenueCat Configuration Guide (All Apps)

**Created:** 2026-02-01
**Purpose:** Step-by-step RevenueCat setup for biomaxx, PrayerLock, WalkToUnlock, StudyLock
**Prerequisites:** Apple Developer account ($99/yr), Google Play Console ($25 one-time)

---

## Quick Setup Checklist

Per app:
- [ ] Create RevenueCat project
- [ ] Configure iOS products in App Store Connect
- [ ] Configure Android products in Google Play Console
- [ ] Link stores to RevenueCat
- [ ] Create entitlements
- [ ] Create offerings
- [ ] Set up webhooks (optional but recommended)
- [ ] Test purchases in sandbox
- [ ] Install SDK in app

**Time per app:** 30-45 minutes first time, 15 minutes after.

---

## Step 1: Create RevenueCat Account

1. Go to https://www.revenuecat.com
2. Sign up (free tier: up to $2,500 MTR - Monthly Tracked Revenue)
3. Create organization: "PRINTMAXX"

---

## Step 2: Create Projects (One Per App)

### Project 1: biomaxx

1. Dashboard → Create New Project
2. Name: "biomaxx"
3. Platform: iOS + Android
4. Save

### Project 2: PrayerLock

Same process, name "PrayerLock"

### Project 3: WalkToUnlock

Same process, name "WalkToUnlock"

### Project 4: StudyLock

Same process, name "StudyLock"

---

## Step 3: Configure Products in App Store Connect

For EACH app:

### 3.1: Create App in App Store Connect

1. Go to https://appstoreconnect.apple.com
2. My Apps → + → New App
3. Bundle ID: `com.printmaxx.biomaxx` (or prayerlock, walktounlock, studylock)
4. SKU: `biomaxx_ios`
5. Save

### 3.2: Create Subscription Group

1. In app settings → Features → In-App Purchases
2. Create Subscription Group: "Premium"
3. Reference Name: "biomaxx Premium Subscriptions"

### 3.3: Create Monthly Subscription

1. In subscription group → + (add product)
2. Product Type: Auto-Renewable Subscription
3. Reference Name: "biomaxx Premium Monthly"
4. Product ID: `com.printmaxx.biomaxx.monthly`
5. Subscription Duration: 1 Month
6. Price: $6.99 USD (Tier 29)
7. Free Trial: 7 days
8. Subscription Localizations:
   - Display Name: "Premium Monthly"
   - Description: "Monthly subscription to biomaxx Premium"
9. Review Information:
   - Screenshot: (upload screenshot of premium features)
   - Review Notes: "7-day free trial, auto-renews at $6.99/mo"
10. Save

### 3.4: Create Annual Subscription

Same process:
- Product ID: `com.printmaxx.biomaxx.annual`
- Duration: 1 Year
- Price: $59.99 USD (Tier 299)
- Free Trial: 7 days
- Display Name: "Premium Annual"

### 3.5: Submit for Review

Once products created:
1. App Store Connect → In-App Purchases → Submit
2. Wait for approval (~24-48 hours)

**Repeat Steps 3.1-3.5 for all 4 apps.**

---

## Step 4: Configure Products in Google Play Console

For EACH app:

### 4.1: Create App in Google Play Console

1. Go to https://play.google.com/console
2. Create app → Name: biomaxx
3. Package name: `com.printmaxx.biomaxx`
4. Save

### 4.2: Create Monthly Subscription

1. Monetize → Products → Subscriptions → Create subscription
2. Product ID: `com.printmaxx.biomaxx.monthly`
3. Name: "Premium Monthly"
4. Description: "Monthly subscription to biomaxx Premium"
5. Billing period: 1 month
6. Price: $6.99 USD
7. Free trial: 7 days
8. Save and activate

### 4.3: Create Annual Subscription

Same process:
- Product ID: `com.printmaxx.biomaxx.annual`
- Billing period: 1 year
- Price: $59.99 USD
- Free trial: 7 days

**Repeat Steps 4.1-4.3 for all 4 apps.**

---

## Step 5: Link Stores to RevenueCat

### 5.1: Link iOS (App Store Connect)

Per app in RevenueCat:

1. Project Settings → Apple App Store
2. App Store Connect → API → Keys
3. Generate API Key:
   - Name: "RevenueCat biomaxx"
   - Access: App Manager
   - Download .p8 file
4. Copy:
   - Issuer ID
   - Key ID
   - .p8 file contents
5. Paste into RevenueCat project settings
6. Bundle ID: `com.printmaxx.biomaxx`
7. Test Connection → Should see green checkmark

### 5.2: Link Android (Google Play)

Per app in RevenueCat:

1. Project Settings → Google Play Store
2. Google Play Console → Setup → API access
3. Create service account:
   - Name: "RevenueCat biomaxx"
   - Role: Finance → Admin
4. Download JSON key file
5. Upload to RevenueCat
6. Package name: `com.printmaxx.biomaxx`
7. Test Connection → Green checkmark

**Repeat for all 4 apps.**

---

## Step 6: Create Entitlements (RevenueCat)

For EACH project:

1. RevenueCat Dashboard → Entitlements
2. Create Entitlement → ID: `premium`
3. Display Name: "Premium Access"
4. Description: "Full access to all premium features"
5. Save

This entitlement will gate all premium features.

---

## Step 7: Create Offerings (RevenueCat)

For EACH project:

### 7.1: Create Current Offering

1. RevenueCat Dashboard → Offerings
2. Create Offering → Identifier: `default`
3. Display Name: "Premium Plans"
4. Make this the Current Offering: ✓
5. Save

### 7.2: Add Packages to Offering

**Monthly Package:**
1. In `default` offering → Add Package
2. Identifier: `monthly`
3. iOS Product: `com.printmaxx.biomaxx.monthly`
4. Android Product: `com.printmaxx.biomaxx.monthly`
5. Save

**Annual Package:**
1. Add Package
2. Identifier: `annual`
3. iOS Product: `com.printmaxx.biomaxx.annual`
4. Android Product: `com.printmaxx.biomaxx.annual`
5. Save

### 7.3: Package Display Order

Drag to reorder:
1. `annual` (shows first - we want this)
2. `monthly` (shows second)

**Repeat for all 4 apps.**

---

## Step 8: Get API Keys for Each App

For EACH project:

1. RevenueCat Dashboard → Project Settings → API Keys
2. Copy **Public App-Specific API Key** for:
   - iOS: `appl_XXXXXXXXXXXXXXXX`
   - Android: `goog_YYYYYYYYYYYYYYYY`

You'll need these in your app code.

**Save to .env file:**

```
# biomaxx
REVENUECAT_IOS_BIOMAXX=appl_XXXXXXXXXXXXXXXX
REVENUECAT_ANDROID_BIOMAXX=goog_YYYYYYYYYYYYYYYY

# PrayerLock
REVENUECAT_IOS_PRAYERLOCK=appl_XXXXXXXXXXXXXXXX
REVENUECAT_ANDROID_PRAYERLOCK=goog_YYYYYYYYYYYYYYYY

# WalkToUnlock
REVENUECAT_IOS_WALKTOUNLOCK=appl_XXXXXXXXXXXXXXXX
REVENUECAT_ANDROID_WALKTOUNLOCK=goog_YYYYYYYYYYYYYYYY

# StudyLock
REVENUECAT_IOS_STUDYLOCK=appl_XXXXXXXXXXXXXXXX
REVENUECAT_ANDROID_STUDYLOCK=goog_YYYYYYYYYYYYYYYY
```

---

## Step 9: Configure Webhooks (Optional but Recommended)

Webhooks notify your backend when subscription events happen.

### 9.1: Create Webhook Endpoint

You need a server endpoint to receive webhooks. Options:

**Option A: n8n Workflow (Recommended)**
1. Create n8n workflow with Webhook trigger
2. Copy webhook URL: `https://your-n8n.app.n8n.cloud/webhook/revenuecat`
3. Save events to Google Sheets or Airtable

**Option B: Zapier**
1. Zapier → Webhooks by Zapier → Catch Hook
2. Copy webhook URL
3. Send to Google Sheets

**Option C: Custom Backend**
If you have a server, create POST endpoint.

### 9.2: Add Webhook to RevenueCat

Per project:

1. RevenueCat Dashboard → Integrations → Webhooks
2. URL: `https://your-endpoint/revenuecat`
3. Events to send:
   - ✓ Initial Purchase
   - ✓ Renewal
   - ✓ Cancellation
   - ✓ Billing Issue
   - ✓ Uncancellation
4. Test Webhook → Should receive test event
5. Save

**Repeat for all 4 apps.**

---

## Step 10: Install SDK in Apps

### 10.1: Install Package

In each app directory:

```bash
cd MONEY_METHODS/APP_FACTORY/builds/biomaxx-sdk54
npx expo install react-native-purchases
```

Repeat for prayerlock, walktounlock, studylock.

### 10.2: Configure in App.tsx

```typescript
// app/App.tsx or app/_layout.tsx

import { useEffect } from 'react';
import { Purchases, LOG_LEVEL } from 'react-native-purchases';
import { Platform } from 'react-native';
import Constants from 'expo-constants';

export default function App() {
  useEffect(() => {
    async function setupRevenueCat() {
      // Only initialize on real devices (iOS/Android)
      if (Platform.OS !== 'ios' && Platform.OS !== 'android') {
        return;
      }

      // Set log level (DEBUG for development, INFO for production)
      Purchases.setLogLevel(__DEV__ ? LOG_LEVEL.DEBUG : LOG_LEVEL.INFO);

      // Get API key from .env
      const apiKey = Platform.select({
        ios: Constants.expoConfig?.extra?.revenueCatIOS,
        android: Constants.expoConfig?.extra?.revenueCatAndroid,
      });

      if (!apiKey) {
        console.error('RevenueCat API key not found');
        return;
      }

      // Configure RevenueCat
      await Purchases.configure({ apiKey });

      console.log('RevenueCat configured');
    }

    setupRevenueCat();
  }, []);

  return (
    // Your app navigation
  );
}
```

### 10.3: Add to app.json

```json
{
  "expo": {
    "extra": {
      "revenueCatIOS": process.env.REVENUECAT_IOS_BIOMAXX,
      "revenueCatAndroid": process.env.REVENUECAT_ANDROID_BIOMAXX
    }
  }
}
```

---

## Step 11: Test in Sandbox

### 11.1: Create Sandbox Test Account (iOS)

1. App Store Connect → Users and Access → Sandbox Testers
2. + → Create sandbox tester
3. Email: `test1@printmaxx.com` (doesn't need to be real)
4. Password: Strong password
5. Country: United States
6. Save

### 11.2: Test on iOS Device

1. Build app with `npx expo run:ios --device`
2. Device Settings → App Store → Sandbox Account
3. Sign in with test account
4. Open app → Go through onboarding
5. At paywall → Tap "Start Free Trial"
6. Enter password when prompted
7. Should see "[Sandbox] Purchase Complete"

### 11.3: Verify in RevenueCat Dashboard

1. RevenueCat → Customers
2. Find test account
3. Should see:
   - Active subscription: `premium`
   - Product: `com.printmaxx.biomaxx.annual` or `monthly`
   - Status: Trial

### 11.4: Test on Android

Same process:
1. Google Play Console → Setup → License testing
2. Add test email
3. Build with `npx expo run:android --device`
4. Test purchase flow

**Repeat for all 4 apps.**

---

## Step 12: Configure A/B Testing (RevenueCat Experiments)

Per project (after apps are live):

### 12.1: Create Experiment

1. RevenueCat Dashboard → Experiments
2. Create Experiment
3. Name: "Paywall Test 1 - Annual vs Monthly Default"
4. Hypothesis: "Highlighting annual increases annual selection"
5. Control (50%): Show current paywall (annual highlighted)
6. Treatment (50%): Show monthly highlighted
7. Metric: % choosing annual
8. Duration: 2 weeks
9. Start Experiment

### 12.2: Implement in App

```typescript
import { Purchases } from 'react-native-purchases';

async function getPaywallVariant() {
  const customerInfo = await Purchases.getCustomerInfo();
  const experiments = customerInfo.activeExperiments;

  // Check if user is in experiment
  if (experiments['paywall_test_1']) {
    return experiments['paywall_test_1']; // 'control' or 'treatment'
  }

  return 'control'; // Default
}

// In PaywallScreen:
const variant = await getPaywallVariant();

if (variant === 'treatment') {
  // Show monthly highlighted
} else {
  // Show annual highlighted (default)
}
```

### 12.3: Tests to Run (Sequential, 2 weeks each)

**Test 1:** Annual vs Monthly default (which highlighted)
**Test 2:** 7-day vs 3-day trial
**Test 3:** $6.99 vs $7.99 monthly price
**Test 4:** Slide-in vs fade-in animation
**Test 5:** "Save $25" vs "58% off" discount framing

---

## Step 13: Monitor Metrics

### Key Metrics in RevenueCat Dashboard

**Active Subscriptions:**
- Total active subscriptions
- Monthly vs Annual split
- Churn rate

**Revenue:**
- MRR (Monthly Recurring Revenue)
- ARR (Annual Recurring Revenue)
- ARPU (Average Revenue Per User)

**Conversion:**
- Trial starts
- Trial-to-paid conversion %
- Paywall abandonment rate

**Goal:**
- 80% paywall conversion (trial starts)
- 40-50% trial-to-paid conversion
- <5% monthly churn

---

## Pricing Summary (All Apps)

| Product | iOS ID | Android ID | Price | Trial |
|---------|--------|------------|-------|-------|
| biomaxx Monthly | `com.printmaxx.biomaxx.monthly` | Same | $6.99/mo | 7 days |
| biomaxx Annual | `com.printmaxx.biomaxx.annual` | Same | $59.99/yr | 7 days |
| PrayerLock Monthly | `com.printmaxx.prayerlock.monthly` | Same | $6.99/mo | 7 days |
| PrayerLock Annual | `com.printmaxx.prayerlock.annual` | Same | $59.99/yr | 7 days |
| WalkToUnlock Monthly | `com.printmaxx.walktounlock.monthly` | Same | $6.99/mo | 7 days |
| WalkToUnlock Annual | `com.printmaxx.walktounlock.annual` | Same | $59.99/yr | 7 days |
| StudyLock Monthly | `com.printmaxx.studylock.monthly` | Same | $6.99/mo | 7 days |
| StudyLock Annual | `com.printmaxx.studylock.annual` | Same | $59.99/yr | 7 days |

**Entitlement ID (All Apps):** `premium`

---

## RevenueCat Free Tier Limits

- $2,500 MTR (Monthly Tracked Revenue) free
- After $2,500 MTR: $100/mo + 1% of revenue
- No limit on API calls or active subscriptions
- All features available on free tier

**Projected timeline:**
- Month 1-3: Under free tier ($2,470/mo per app × 4 = $9,880 MTR)
- Month 4+: Paid plan ($100/mo) - worth it at this revenue

---

## Troubleshooting

### "Product not found" error

**Cause:** Products not synced yet
**Fix:** Wait 24 hours after creating products. Test in sandbox mode first.

### "Failed to purchase"

**Cause:** Sandbox account not signed in
**Fix:** Device Settings → App Store → Sandbox Account → Sign in

### "Invalid API key"

**Cause:** Wrong API key for platform
**Fix:** iOS needs `appl_` key, Android needs `goog_` key. Check .env.

### Webhook not receiving events

**Cause:** Wrong URL or endpoint not responding
**Fix:** Test webhook in RevenueCat dashboard. Endpoint must return 200 OK.

---

## Next Actions

1. [ ] Create RevenueCat account
2. [ ] Set up 4 projects (biomaxx, PrayerLock, WalkToUnlock, StudyLock)
3. [ ] Configure iOS products in App Store Connect (all 4 apps)
4. [ ] Configure Android products in Google Play (all 4 apps)
5. [ ] Link stores to RevenueCat
6. [ ] Create entitlements and offerings
7. [ ] Install SDK in all 4 apps
8. [ ] Test in sandbox (iOS + Android)
9. [ ] Ship biomaxx first
10. [ ] Monitor metrics, start A/B tests

**Estimated time:** 3-4 hours for all 4 apps.

---

## Support Resources

- RevenueCat Docs: https://docs.revenuecat.com
- Community Slack: https://community.revenuecat.com
- React Native SDK: https://docs.revenuecat.com/docs/reactnative
- Expo Integration: https://docs.revenuecat.com/docs/expo

**This completes RevenueCat setup. Hard paywall = 8x revenue. Worth the setup time.**
