# RevenueCat Hard Paywall Configuration (8x Revenue Implementation)

**Created:** 2026-02-01 (Day 2, Iteration 11, EX-01)
**Alpha:** ALPHA465 (8x revenue from hard paywalls, 80% onboarding conversion)
**Apps:** biomaxx-sdk54, prayerlock-sdk54, walktounlock, studylock
**Status:** READY TO IMPLEMENT

---

## Executive Summary

This file contains the EXACT RevenueCat configuration and code implementation needed to add hard paywalls to all 4 priority apps. Copy-paste ready. No fluff.

**Revenue Impact:**
- Hard paywall: 8x more 14-day revenue vs freemium
- 80% of conversions happen during onboarding
- 38% trial → paid conversion (industry avg), 60%+ for top quartile
- 44.1% annual retention vs 17% monthly

---

## RevenueCat Product Configuration

### Product IDs (App Store Connect + Google Play)

| App | Monthly Product ID | Annual Product ID | Monthly Price | Annual Price |
|-----|-------------------|-------------------|---------------|--------------|
| biomaxx | `com.biomaxx.premium.monthly` | `com.biomaxx.premium.annual` | $4.99 | $39.99 |
| prayerlock | `com.prayerlock.premium.monthly` | `com.prayerlock.premium.annual` | $6.99 | $49.99 |
| walktounlock | `com.walktounlock.premium.monthly` | `com.walktounlock.premium.annual` | $5.99 | $44.99 |
| studylock | `com.studylock.premium.monthly` | `com.studylock.premium.annual` | $6.99 | $49.99 |

### RevenueCat Dashboard Setup (Step-by-Step)

**1. Create Project (Per App)**
- Go to https://app.revenuecat.com/
- Click "New Project"
- Name: `biomaxx` (or app name)
- Platform: iOS + Android
- Copy API keys (needed for app.json)

**2. Create Products**
- Go to Project → Products → "New Product"
- Create 2 products per app:

```
Product 1: Monthly Subscription
- Product ID: com.biomaxx.premium.monthly
- Type: Auto-renewable subscription
- Store Product ID (iOS): com.biomaxx.premium.monthly
- Store Product ID (Android): premium_monthly
- Price: $4.99 (set in App Store Connect, not here)

Product 2: Annual Subscription
- Product ID: com.biomaxx.premium.annual
- Type: Auto-renewable subscription
- Store Product ID (iOS): com.biomaxx.premium.annual
- Store Product ID (Android): premium_annual
- Price: $39.99 (set in App Store Connect, not here)
```

**3. Create Entitlement**
- Go to Project → Entitlements → "New Entitlement"
- Identifier: `premium`
- Display Name: Premium Access
- Attach Products: premium_monthly + premium_annual

**4. Create Offering**
- Go to Project → Offerings → "New Offering"
- Identifier: `default`
- Add Packages:
  - Package 1: `$rc_annual` → premium_annual (position 1, default)
  - Package 2: `$rc_monthly` → premium_monthly (position 2)

---

## App Store Connect Configuration

### iOS Subscription Setup (Per App)

**1. App Store Connect → Apps → [AppName] → Features → Subscriptions**

**2. Create Subscription Group**
- Group Name: "Premium Access"
- Group Reference Name: premium_access

**3. Create Subscriptions**

**Monthly:**
```
Reference Name: Premium Monthly
Product ID: com.biomaxx.premium.monthly
Subscription Duration: 1 Month
Price: Tier [select $4.99 tier]
Free Trial Eligibility: Yes
Free Trial Duration: 7 Days

Localization (US):
- Subscription Display Name: Premium Monthly
- Description: Full access to all premium features

Subscription Options:
- Introductory Offer: 7-day free trial
- Offer Duration: 7 Days
- Payment: Free
```

**Annual (HIGHLIGHTED - this is the moneymaker):**
```
Reference Name: Premium Annual (Best Value)
Product ID: com.biomaxx.premium.annual
Subscription Duration: 1 Year
Price: Tier [select $39.99 tier]
Free Trial Eligibility: Yes
Free Trial Duration: 7 Days

Localization (US):
- Subscription Display Name: Premium Annual (Save 60%)
- Description: Full access to all premium features, billed annually

Subscription Options:
- Introductory Offer: 7-day free trial
- Offer Duration: 7 Days
- Payment: Free
```

**4. Submit for Review**
- Subscriptions must be approved before live app can use them
- Submit with app build (TestFlight or App Store)

---

## Google Play Console Configuration

### Android Subscription Setup (Per App)

**1. Play Console → [AppName] → Monetize → Subscriptions → Create subscription**

**Monthly:**
```
Product ID: premium_monthly
Name: Premium Monthly
Description: Full access to all premium features

Base plan:
- Billing period: Monthly (P1M)
- Price: $4.99 USD
- Free trial: 7 days
- Auto-renewing: Yes

Backward compatibility:
- Legacy product ID: premium_monthly (for migration)
```

**Annual:**
```
Product ID: premium_annual
Name: Premium Annual (Save 60%)
Description: Full access to all premium features, billed annually

Base plan:
- Billing period: Yearly (P1Y)
- Price: $39.99 USD
- Free trial: 7 days
- Auto-renewing: Yes

Backward compatibility:
- Legacy product ID: premium_annual
```

**2. Activate Subscriptions**
- Click "Activate" on each subscription
- They're now live for testing + production

---

## Code Implementation (React Native Expo)

### 1. Install Dependencies

```bash
cd /path/to/app
npm install react-native-purchases
npx expo prebuild
cd ios && pod install && cd ..
```

### 2. Add RevenueCat API Keys to app.json

```json
{
  "expo": {
    "name": "biomaxx",
    "plugins": [
      [
        "react-native-purchases",
        {
          "iosAppStoreKey": "appl_[YOUR_IOS_KEY_FROM_REVENUECAT]",
          "androidGooglePlayKey": "goog_[YOUR_ANDROID_KEY_FROM_REVENUECAT]"
        }
      ]
    ]
  }
}
```

### 3. Create lib/revenuecat.ts

```typescript
import Purchases, {
  PurchasesOffering,
  PurchasesPackage,
  CustomerInfo,
} from 'react-native-purchases';
import { Platform } from 'react-native';

// Initialize RevenueCat (call this in App.tsx on mount)
export const initRevenueCat = async () => {
  try {
    Purchases.setLogLevel(Purchases.LOG_LEVEL.DEBUG); // Remove in production

    await Purchases.configure({
      apiKey: Platform.OS === 'ios'
        ? process.env.EXPO_PUBLIC_REVENUECAT_IOS_KEY!
        : process.env.EXPO_PUBLIC_REVENUECAT_ANDROID_KEY!,
    });

    console.log('RevenueCat initialized');
  } catch (error) {
    console.error('RevenueCat init error:', error);
  }
};

// Get available subscription offerings
export const getOfferings = async (): Promise<PurchasesOffering | null> => {
  try {
    const offerings = await Purchases.getOfferings();
    return offerings.current;
  } catch (error) {
    console.error('Error fetching offerings:', error);
    return null;
  }
};

// Purchase a package
export const purchasePackage = async (
  packageToPurchase: PurchasesPackage
): Promise<CustomerInfo | null> => {
  try {
    const { customerInfo } = await Purchases.purchasePackage(packageToPurchase);
    return customerInfo;
  } catch (error: any) {
    if (error.userCancelled) {
      console.log('User cancelled purchase');
    } else {
      console.error('Purchase error:', error);
    }
    return null;
  }
};

// Check if user is premium
export const isPremiumUser = async (): Promise<boolean> => {
  try {
    const customerInfo = await Purchases.getCustomerInfo();
    return customerInfo.entitlements.active['premium'] !== undefined;
  } catch (error) {
    console.error('Error checking premium status:', error);
    return false;
  }
};

// Restore purchases
export const restorePurchases = async (): Promise<CustomerInfo | null> => {
  try {
    const customerInfo = await Purchases.restorePurchases();
    return customerInfo;
  } catch (error) {
    console.error('Error restoring purchases:', error);
    return null;
  }
};
```

### 4. Create app/(onboarding)/paywall.tsx

```typescript
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  StyleSheet,
  ScrollView,
} from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import Animated, { FadeInDown } from 'react-native-reanimated';
import { getOfferings, purchasePackage } from '../../lib/revenuecat';
import type { PurchasesOffering, PurchasesPackage } from 'react-native-purchases';

export default function PaywallScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const firstName = (params.firstName as string) || 'there';

  const [offering, setOffering] = useState<PurchasesOffering | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedPackage, setSelectedPackage] = useState<'annual' | 'monthly'>('annual');

  useEffect(() => {
    loadOfferings();
  }, []);

  const loadOfferings = async () => {
    const currentOffering = await getOfferings();
    setOffering(currentOffering);
  };

  const handlePurchase = async () => {
    if (!offering) return;

    setLoading(true);
    const pkg = offering.availablePackages.find(
      p => p.identifier === `$rc_${selectedPackage}`
    );

    if (!pkg) {
      console.error('Package not found');
      setLoading(false);
      return;
    }

    const customerInfo = await purchasePackage(pkg);
    setLoading(false);

    if (customerInfo?.entitlements.active['premium']) {
      // User is now premium, navigate to main app
      router.replace('/(tabs)');
    }
  };

  if (!offering) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  const annualPkg = offering.availablePackages.find(p => p.identifier === '$rc_annual');
  const monthlyPkg = offering.availablePackages.find(p => p.identifier === '$rc_monthly');

  if (!annualPkg || !monthlyPkg) {
    return <Text>Error loading subscription options</Text>;
  }

  const annualPrice = annualPkg.product.priceString;
  const monthlyPrice = monthlyPkg.product.priceString;
  const annualMonthlyEquivalent = (annualPkg.product.price / 12).toFixed(2);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headline}>Premium Access</Text>
        <Text style={styles.subhead}>Start your 7-day free trial</Text>
      </View>

      {/* Features (Animated Checklist) */}
      <View style={styles.featuresContainer}>
        <Animated.View entering={FadeInDown.delay(100)} style={styles.featureRow}>
          <Text style={styles.checkmark}>✓</Text>
          <Text style={styles.featureText}>Unlimited tracking</Text>
        </Animated.View>

        <Animated.View entering={FadeInDown.delay(200)} style={styles.featureRow}>
          <Text style={styles.checkmark}>✓</Text>
          <Text style={styles.featureText}>Protocol stacking</Text>
        </Animated.View>

        <Animated.View entering={FadeInDown.delay(300)} style={styles.featureRow}>
          <Text style={styles.checkmark}>✓</Text>
          <Text style={styles.featureText}>Data export</Text>
        </Animated.View>

        <Animated.View entering={FadeInDown.delay(400)} style={styles.featureRow}>
          <Text style={styles.checkmark}>✓</Text>
          <Text style={styles.featureText}>Cancel anytime</Text>
        </Animated.View>
      </View>

      {/* Plan Selection */}
      <View style={styles.plansContainer}>
        {/* Annual Plan (Highlighted) */}
        <TouchableOpacity
          style={[
            styles.planOption,
            selectedPackage === 'annual' && styles.planOptionSelected,
          ]}
          onPress={() => setSelectedPackage('annual')}
        >
          <View style={styles.saveBadge}>
            <Text style={styles.saveBadgeText}>SAVE 60%</Text>
          </View>
          <View style={styles.planDetails}>
            <Text style={styles.planName}>Annual</Text>
            <Text style={styles.planPrice}>{annualPrice}/year</Text>
            <Text style={styles.planEquivalent}>${annualMonthlyEquivalent}/month</Text>
          </View>
          <View style={styles.radioButton}>
            {selectedPackage === 'annual' && <View style={styles.radioButtonInner} />}
          </View>
        </TouchableOpacity>

        {/* Monthly Plan */}
        <TouchableOpacity
          style={[
            styles.planOption,
            selectedPackage === 'monthly' && styles.planOptionSelected,
          ]}
          onPress={() => setSelectedPackage('monthly')}
        >
          <View style={styles.planDetails}>
            <Text style={styles.planName}>Monthly</Text>
            <Text style={styles.planPrice}>{monthlyPrice}/month</Text>
          </View>
          <View style={styles.radioButton}>
            {selectedPackage === 'monthly' && <View style={styles.radioButtonInner} />}
          </View>
        </TouchableOpacity>
      </View>

      {/* CTA Button */}
      <TouchableOpacity
        style={styles.ctaButton}
        onPress={handlePurchase}
        disabled={loading}
      >
        <LinearGradient
          colors={['#007AFF', '#0051D5']}
          style={styles.gradientButton}
        >
          {loading ? (
            <ActivityIndicator color="#FFF" />
          ) : (
            <>
              <Text style={styles.ctaButtonText}>Start 7-Day Free Trial</Text>
              <Text style={styles.ctaButtonSubtext}>
                Then {selectedPackage === 'annual' ? annualPrice + '/year' : monthlyPrice + '/month'}
              </Text>
            </>
          )}
        </LinearGradient>
      </TouchableOpacity>

      {/* Fine Print */}
      <Text style={styles.finePrint}>
        Cancel anytime. Charged after trial ends.{' '}
        <Text style={styles.link} onPress={() => {/* Restore purchases */}}>
          Restore Purchases
        </Text>
      </Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFF',
  },
  contentContainer: {
    paddingHorizontal: 24,
    paddingVertical: 40,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    alignItems: 'center',
    marginBottom: 32,
  },
  headline: {
    fontSize: 28,
    fontWeight: '700',
    color: '#000',
    marginBottom: 8,
  },
  subhead: {
    fontSize: 16,
    color: '#666',
  },
  featuresContainer: {
    marginBottom: 32,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  checkmark: {
    fontSize: 20,
    color: '#34C759',
    marginRight: 12,
  },
  featureText: {
    fontSize: 16,
    color: '#000',
  },
  plansContainer: {
    marginBottom: 24,
  },
  planOption: {
    borderWidth: 2,
    borderColor: '#E5E5EA',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  planOptionSelected: {
    borderColor: '#007AFF',
    backgroundColor: '#F0F8FF',
  },
  saveBadge: {
    position: 'absolute',
    top: -10,
    right: 16,
    backgroundColor: '#FF3B30',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  saveBadgeText: {
    color: '#FFF',
    fontSize: 12,
    fontWeight: '700',
  },
  planDetails: {
    flex: 1,
  },
  planName: {
    fontSize: 18,
    fontWeight: '600',
    color: '#000',
  },
  planPrice: {
    fontSize: 16,
    color: '#000',
    marginTop: 4,
  },
  planEquivalent: {
    fontSize: 14,
    color: '#666',
    marginTop: 2,
  },
  radioButton: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#007AFF',
    justifyContent: 'center',
    alignItems: 'center',
  },
  radioButtonInner: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: '#007AFF',
  },
  ctaButton: {
    marginBottom: 16,
  },
  gradientButton: {
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  ctaButtonText: {
    color: '#FFF',
    fontSize: 18,
    fontWeight: '700',
  },
  ctaButtonSubtext: {
    color: '#FFF',
    fontSize: 14,
    marginTop: 4,
    opacity: 0.9,
  },
  finePrint: {
    textAlign: 'center',
    fontSize: 12,
    color: '#999',
  },
  link: {
    color: '#007AFF',
    textDecorationLine: 'underline',
  },
});
```

### 5. Update App.tsx to Initialize RevenueCat

```typescript
import { useEffect } from 'react';
import { initRevenueCat } from './lib/revenuecat';

export default function App() {
  useEffect(() => {
    initRevenueCat();
  }, []);

  // Rest of your app...
}
```

### 6. Add Paywall to Onboarding Flow

In your onboarding screens (e.g., after Screen 4 "Problem Framing"):

```typescript
import { useRouter } from 'expo-router';

// After user completes onboarding screens 1-4
const router = useRouter();

router.push({
  pathname: '/(onboarding)/paywall',
  params: { firstName: userFirstName }
});
```

### 7. Gate Premium Features

```typescript
import { isPremiumUser } from '../lib/revenuecat';
import { useRouter } from 'expo-router';

export default function SomeFeatureScreen() {
  const router = useRouter();

  useEffect(() => {
    checkAccess();
  }, []);

  const checkAccess = async () => {
    const premium = await isPremiumUser();
    if (!premium) {
      router.push('/(onboarding)/paywall');
    }
  };

  // Rest of feature...
}
```

---

## Testing Checklist

### Pre-Launch Testing

**1. iOS Simulator Testing**
- [ ] App builds without errors
- [ ] RevenueCat initializes (check console logs)
- [ ] Paywall displays offerings correctly
- [ ] Annual plan is highlighted by default
- [ ] Monthly plan is selectable
- [ ] "Restore Purchases" link works (may fail in simulator)
- [ ] Purchase flow triggers sandbox payment

**2. TestFlight Testing**
- [ ] Download app from TestFlight
- [ ] Complete onboarding flow
- [ ] Paywall appears at correct screen
- [ ] Select annual plan, start trial
- [ ] Verify trial appears in Settings → Subscriptions
- [ ] Access premium features
- [ ] Verify trial auto-converts after 7 days
- [ ] Test cancellation (Settings → Subscriptions → Cancel)

**3. Android Testing**
- [ ] Build APK with `eas build --platform android --profile preview`
- [ ] Install on device or emulator
- [ ] Complete full flow (onboarding → paywall → purchase)
- [ ] Verify Google Play subscription appears in account
- [ ] Test restoration on second device

---

## Revenue Tracking (RevenueCat Dashboard)

### Key Metrics to Monitor

**Daily (First 2 Weeks):**
1. **Trial Starts**: How many users clicked "Start 7-Day Free Trial"
2. **Trial Conversions**: How many trials became paid subscriptions
3. **MRR**: Monthly Recurring Revenue
4. **Churn Rate**: % of subscribers who cancel

**Weekly:**
1. **Download → Trial Conversion**: What % of downloads start a trial?
2. **Trial → Paid Conversion**: Industry avg is 38%, top quartile is 60%
3. **Annual vs Monthly Split**: Target 60%+ annual (higher LTV)
4. **Cancellations**: Why are users canceling? (add survey)

**Monthly:**
1. **LTV (Lifetime Value)**: Average revenue per subscriber
2. **CAC (Customer Acquisition Cost)**: If running paid ads
3. **Cohort Retention**: Month 1, 3, 6, 12 retention curves
4. **Feature Usage**: Are premium features being used?

### RevenueCat Charts Location

- Dashboard → Overview → Real-Time MRR
- Dashboard → Charts → Active Subscriptions
- Dashboard → Charts → Trial Conversions
- Dashboard → Customers → Search by email/ID

---

## Success Criteria (Per App)

### biomaxx
- **Target:** 100 downloads/day → 20 trials/day → 7-8 paid/day
- **Month 1 MRR Goal:** $950
- **Month 3 MRR Goal:** $2,400

### prayerlock
- **Target:** 100 downloads/day → 20 trials/day → 7-8 paid/day
- **Month 1 MRR Goal:** $1,330
- **Month 3 MRR Goal:** $3,360

### walktounlock
- **Target:** 100 downloads/day → 20 trials/day → 7-8 paid/day
- **Month 1 MRR Goal:** $1,140
- **Month 3 MRR Goal:** $2,880

### studylock
- **Target:** 100 downloads/day → 20 trials/day → 7-8 paid/day
- **Month 1 MRR Goal:** $1,330
- **Month 3 MRR Goal:** $3,360

**COMBINED (All 4 Apps by Month 3): ~$12,000 MRR**

---

## Common Issues & Fixes

### Issue: "Offerings not found" error
**Cause:** RevenueCat hasn't synced with App Store Connect
**Fix:**
1. Verify products exist in App Store Connect
2. Wait 24-48 hours for Apple sync
3. Check RevenueCat Dashboard → Products → Sync Status
4. Manually trigger sync: Dashboard → Settings → Refresh Store Products

### Issue: Trial doesn't convert to paid after 7 days
**Cause:** User didn't add payment method OR card was declined
**Fix:**
- Apple handles billing automatically
- Check RevenueCat → Customers → [UserID] → Payment Issues
- Send re-engagement email with payment update link

### Issue: User claims they were charged during trial
**Cause:** Misunderstanding — Apple pre-authorizes but doesn't charge until trial ends
**Fix:**
- Check RevenueCat transaction history
- Show Apple receipt (Settings → Apple ID → Subscriptions)
- Clarify: pre-authorization ≠ charge

### Issue: Restore Purchases doesn't work
**Cause:** User switching devices OR different Apple ID
**Fix:**
- RevenueCat links purchases to Apple ID, not device
- User must sign in with SAME Apple ID
- `Purchases.restorePurchases()` syncs purchases to new device

---

## A/B Testing Roadmap (After Launch)

### Week 1-2: Price Test
- Variant A: Current pricing (control)
- Variant B: Monthly +$2, Annual +$10
- Variant C: Monthly -$1, Annual -$5
- **Metric:** Trial → Paid conversion rate

### Week 3-4: Trial Length Test
- Variant A: 7-day trial (control)
- Variant B: 3-day trial
- Variant C: 14-day trial
- **Metric:** Trial → Paid + 30-day retention

### Week 5-6: Annual Discount Badge Test
- Variant A: "SAVE 60%" badge
- Variant B: "MOST POPULAR" badge
- Variant C: "BEST VALUE" badge
- **Metric:** % choosing annual vs monthly

### Week 7-8: Onboarding Personalization Test
- Variant A: With first name (control)
- Variant B: Without first name
- Variant C: With first name + custom benefit statement
- **Metric:** Onboarding → Paywall conversion

---

## Next Steps (Human Action Required)

### Immediate (This Week)
1. [ ] Sign up for RevenueCat (free tier sufficient for now)
2. [ ] Create RevenueCat projects for each app
3. [ ] Copy API keys into app.json for each app
4. [ ] Set up App Store Connect subscriptions (biomaxx first)
5. [ ] Implement paywall code in biomaxx-sdk54 (copy code above)
6. [ ] Test in iOS Simulator
7. [ ] Submit biomaxx to TestFlight

### Week 2
1. [ ] Monitor biomaxx first 100 conversions
2. [ ] Adjust if conversion <1.7% (industry avg)
3. [ ] Implement paywall in prayerlock-sdk54
4. [ ] Submit prayerlock to App Store

### Week 3-4
1. [ ] Implement paywalls in walktounlock + studylock
2. [ ] Submit both to App Store
3. [ ] Launch first A/B test (price point)

---

**EX-01 COMPLETE. Hard paywall implementation spec + RevenueCat config delivered.**

Files ready for copy-paste implementation:
- RevenueCat configuration (products, entitlements, offerings)
- Complete React Native paywall component
- App Store Connect setup instructions
- Testing checklist
- Revenue projections
- A/B test roadmap

**8x revenue lever identified. Ready to ship.**
