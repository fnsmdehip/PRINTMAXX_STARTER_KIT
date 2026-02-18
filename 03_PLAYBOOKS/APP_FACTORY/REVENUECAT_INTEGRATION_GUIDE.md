# RevenueCat Integration Guide

Step-by-step guide to integrate RevenueCat into PRINTMAXX apps. Follows the existing app architecture (prayerlock as reference).

---

## 1. RevenueCat Setup Checklist

### Create RevenueCat Project

1. Go to [app.revenuecat.com](https://app.revenuecat.com)
2. Click "Create New Project"
3. Name: `PRINTMAXX Apps`
4. Save the Project ID

### iOS App Configuration

**App Store Connect Setup:**

1. Go to Users and Access > Integrations > In-App Purchase
2. Click "Generate In-App Purchase Key"
3. Download the `.p8` file (store securely, you only get one download)
4. Note the Key ID and Issuer ID

**RevenueCat iOS App:**

1. Go to Project Settings > Apps > Add New App
2. Select iOS
3. Enter Bundle ID: `com.printmaxx.prayerlock`
4. Enter credentials:
   - Issuer ID from App Store Connect
   - Key ID from App Store Connect
   - Upload the `.p8` file
5. Click "Connect to App Store Connect"

**Get Shared Secret:**

1. App Store Connect > Your App > App Information
2. Scroll to "App-Specific Shared Secret"
3. Generate if needed
4. Copy to RevenueCat app settings

### Android App Configuration

**Google Play Console:**

1. Go to Setup > API access
2. Link or create a Google Cloud project
3. Create a service account with "View financial data" permission
4. Download JSON key file

**RevenueCat Android App:**

1. Add New App > Android
2. Enter Package Name: `com.printmaxx.prayerlock`
3. Upload service account JSON
4. Click "Connect to Google Play"

### API Key Management

RevenueCat generates separate keys per platform:

```bash
# .env (never commit)
REVENUECAT_IOS_API_KEY=appl_xxxxxxxxxx
REVENUECAT_ANDROID_API_KEY=goog_xxxxxxxxxx
```

For React Native, store in `src/config/revenuecat.ts`:

```typescript
import { Platform } from 'react-native';

export const REVENUECAT_API_KEY = Platform.select({
  ios: 'appl_xxxxxxxxxx',
  android: 'goog_xxxxxxxxxx',
}) as string;

export const ENTITLEMENT_ID = 'premium';
```

---

## 2. Product Configuration

### Subscription Tiers

| App | Monthly | Annual | Product ID Prefix |
|-----|---------|--------|-------------------|
| PrayerLock | $9.99/mo | $49.99/yr | `prayerlock_` |
| WalkToUnlock | $7.99/mo | $39.99/yr | `walktounlock_` |
| StudyLock | $6.99/mo | $34.99/yr | `studylock_` |

### Product ID Naming Convention

```
{app_prefix}_{duration}_{price_cents}
```

**Examples:**
- `prayerlock_monthly_999`
- `prayerlock_annual_4999`
- `walktounlock_monthly_799`
- `studylock_annual_3499`

### Create Products in App Store Connect

1. Go to App Store Connect > Your App > Subscriptions
2. Create Subscription Group: `Premium`
3. Add products:

**PrayerLock:**

| Product ID | Reference Name | Duration | Price |
|------------|----------------|----------|-------|
| `prayerlock_monthly_999` | PrayerLock Monthly | 1 Month | $9.99 |
| `prayerlock_annual_4999` | PrayerLock Annual | 1 Year | $49.99 |

**WalkToUnlock:**

| Product ID | Reference Name | Duration | Price |
|------------|----------------|----------|-------|
| `walktounlock_monthly_799` | WalkToUnlock Monthly | 1 Month | $7.99 |
| `walktounlock_annual_3999` | WalkToUnlock Annual | 1 Year | $39.99 |

**StudyLock:**

| Product ID | Reference Name | Duration | Price |
|------------|----------------|----------|-------|
| `studylock_monthly_699` | StudyLock Monthly | 1 Month | $6.99 |
| `studylock_annual_3499` | StudyLock Annual | 1 Year | $34.99 |

### RevenueCat Entitlements Setup

1. Go to RevenueCat > Project > Entitlements
2. Create entitlement: `premium`
3. This single entitlement works for all apps

### Offerings Configuration

For each app in RevenueCat:

1. Go to App > Offerings
2. Create offering: `default`
3. Create packages:
   - Identifier: `$rc_monthly` -> Link to monthly product
   - Identifier: `$rc_annual` -> Link to annual product
4. Set `default` as current offering

### Trial Configuration

Set in App Store Connect when creating products:

| App | Monthly Trial | Annual Trial |
|-----|---------------|--------------|
| PrayerLock | 3 days | 7 days |
| WalkToUnlock | 3 days | 7 days |
| StudyLock | 3 days | 7 days |

---

## 3. React Native Implementation

### Install SDK

```bash
npm install react-native-purchases
cd ios && pod install && cd ..
```

### SDK Initialization

Create `src/services/purchases.ts`:

```typescript
import Purchases, {
  LOG_LEVEL,
  CustomerInfo,
  PurchasesOffering,
  PurchasesPackage,
} from 'react-native-purchases';
import { Platform } from 'react-native';

const API_KEYS = {
  ios: 'appl_XXXXXXXXXX', // Replace with your key
  android: 'goog_XXXXXXXXXX', // Replace with your key
};

const ENTITLEMENT_ID = 'premium';

export async function initializePurchases(): Promise<void> {
  if (__DEV__) {
    Purchases.setLogLevel(LOG_LEVEL.DEBUG);
  }

  const apiKey = Platform.OS === 'ios' ? API_KEYS.ios : API_KEYS.android;
  await Purchases.configure({ apiKey });
}

export async function getOfferings(): Promise<PurchasesOffering | null> {
  try {
    const offerings = await Purchases.getOfferings();
    return offerings.current;
  } catch (error) {
    console.error('Error fetching offerings:', error);
    return null;
  }
}

export async function purchasePackage(pkg: PurchasesPackage): Promise<{
  success: boolean;
  customerInfo?: CustomerInfo;
  error?: string;
}> {
  try {
    const { customerInfo } = await Purchases.purchasePackage(pkg);
    const isPremium = customerInfo.entitlements.active[ENTITLEMENT_ID] !== undefined;
    return { success: isPremium, customerInfo };
  } catch (error: any) {
    if (error.userCancelled) {
      return { success: false, error: 'cancelled' };
    }
    return { success: false, error: error.message };
  }
}

export async function checkPremiumStatus(): Promise<boolean> {
  try {
    const customerInfo = await Purchases.getCustomerInfo();
    return customerInfo.entitlements.active[ENTITLEMENT_ID] !== undefined;
  } catch (error) {
    console.error('Error checking premium status:', error);
    return false;
  }
}

export async function restorePurchases(): Promise<{
  success: boolean;
  error?: string;
}> {
  try {
    const customerInfo = await Purchases.restorePurchases();
    const isPremium = customerInfo.entitlements.active[ENTITLEMENT_ID] !== undefined;
    return { success: isPremium };
  } catch (error: any) {
    return { success: false, error: error.message };
  }
}

export async function identifyUser(userId: string): Promise<void> {
  try {
    await Purchases.logIn(userId);
  } catch (error) {
    console.error('Error identifying user:', error);
  }
}

export function addPurchaseListener(
  callback: (customerInfo: CustomerInfo) => void
): () => void {
  Purchases.addCustomerInfoUpdateListener(callback);
  return () => {
    Purchases.removeCustomerInfoUpdateListener(callback);
  };
}
```

### Initialize in App Entry Point

Update `App.tsx`:

```typescript
import React, { useEffect } from 'react';
import { StatusBar } from 'expo-status-bar';
import { AppProvider } from './src/context/AppContext';
import { Navigation } from './src/navigation';
import { initializePurchases } from './src/services/purchases';

export default function App() {
  useEffect(() => {
    initializePurchases();
  }, []);

  return (
    <AppProvider>
      <Navigation />
      <StatusBar style="auto" />
    </AppProvider>
  );
}
```

### Premium Status Hook

Create `src/hooks/usePremium.ts`:

```typescript
import { useState, useEffect, useCallback } from 'react';
import { CustomerInfo } from 'react-native-purchases';
import {
  checkPremiumStatus,
  addPurchaseListener,
} from '../services/purchases';

export function usePremium() {
  const [isPremium, setIsPremium] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const refresh = useCallback(async () => {
    setIsLoading(true);
    const status = await checkPremiumStatus();
    setIsPremium(status);
    setIsLoading(false);
  }, []);

  useEffect(() => {
    refresh();

    const unsubscribe = addPurchaseListener((info: CustomerInfo) => {
      const hasEntitlement = info.entitlements.active['premium'] !== undefined;
      setIsPremium(hasEntitlement);
    });

    return unsubscribe;
  }, [refresh]);

  return { isPremium, isLoading, refresh };
}
```

### Offerings Hook

Create `src/hooks/useOfferings.ts`:

```typescript
import { useState, useEffect } from 'react';
import { PurchasesOffering } from 'react-native-purchases';
import { getOfferings } from '../services/purchases';

export function useOfferings() {
  const [offerings, setOfferings] = useState<PurchasesOffering | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchOfferings() {
      try {
        const result = await getOfferings();
        setOfferings(result);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    }

    fetchOfferings();
  }, []);

  return { offerings, isLoading, error };
}
```

---

## 4. Paywall Component Template

Replace the simulated paywall in `src/screens/PaywallScreen.tsx`:

```typescript
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  StatusBar,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { PurchasesPackage } from 'react-native-purchases';
import { Button } from '../components';
import { Colors } from '../constants';
import { useOfferings } from '../hooks/useOfferings';
import { purchasePackage, restorePurchases } from '../services/purchases';

type RootStackParamList = {
  Paywall: undefined;
  Main: undefined;
};

type PaywallScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Paywall'>;
};

const FEATURES = [
  { title: 'Extended Prayer Times', description: '30 and 60 minute sessions', free: false },
  { title: 'Family Accountability', description: "See your family members' streaks", free: false },
  { title: 'Custom Prayer Prompts', description: 'Create your own daily focus', free: false },
  { title: 'Streak Freezes', description: '1 free freeze per week', free: false },
  { title: 'Ad-Free Experience', description: 'No interruptions', free: false },
  { title: 'Basic Morning Lock', description: '5-15 minute sessions', free: true },
  { title: 'Daily Verses', description: '30 rotating verses', free: true },
  { title: 'Streak Tracking', description: 'Track your consistency', free: true },
];

export function PaywallScreen({ navigation }: PaywallScreenProps) {
  const { offerings, isLoading: loadingOfferings } = useOfferings();
  const [selectedPackage, setSelectedPackage] = useState<PurchasesPackage | null>(null);
  const [isPurchasing, setIsPurchasing] = useState(false);
  const [isRestoring, setIsRestoring] = useState(false);

  const monthlyPackage = offerings?.monthly;
  const annualPackage = offerings?.annual;

  // Auto-select annual when loaded
  React.useEffect(() => {
    if (annualPackage && !selectedPackage) {
      setSelectedPackage(annualPackage);
    }
  }, [annualPackage, selectedPackage]);

  const handlePurchase = async () => {
    if (!selectedPackage) return;

    setIsPurchasing(true);
    const result = await purchasePackage(selectedPackage);
    setIsPurchasing(false);

    if (result.success) {
      navigation.goBack();
    } else if (result.error && result.error !== 'cancelled') {
      Alert.alert('Purchase Failed', result.error);
    }
  };

  const handleRestore = async () => {
    setIsRestoring(true);
    const result = await restorePurchases();
    setIsRestoring(false);

    if (result.success) {
      Alert.alert('Success', 'Your purchases have been restored.', [
        { text: 'OK', onPress: () => navigation.goBack() },
      ]);
    } else {
      Alert.alert(
        'No Purchases Found',
        'We could not find any previous purchases for this account.'
      );
    }
  };

  // Calculate savings
  const monthlyPrice = monthlyPackage?.product.price || 0;
  const annualPrice = annualPackage?.product.price || 0;
  const monthlyCostIfAnnual = annualPrice / 12;
  const savingsPercent = monthlyPrice > 0
    ? Math.round(((monthlyPrice - monthlyCostIfAnnual) / monthlyPrice) * 100)
    : 0;

  if (loadingOfferings) {
    return (
      <SafeAreaView style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={Colors.primary} />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <LinearGradient
        colors={[Colors.gradientStart, Colors.gradientEnd]}
        style={styles.header}
      >
        <TouchableOpacity
          style={styles.closeButton}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.closeText}>Close</Text>
        </TouchableOpacity>

        <Text style={styles.headerTitle}>PrayerLock Pro</Text>
        <Text style={styles.headerSubtitle}>
          Deepen your prayer life with premium features
        </Text>
      </LinearGradient>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Plan Selection */}
        <View style={styles.plansContainer}>
          {annualPackage && (
            <TouchableOpacity
              style={[
                styles.planCard,
                selectedPackage?.identifier === annualPackage.identifier && styles.selectedPlan,
              ]}
              onPress={() => setSelectedPackage(annualPackage)}
            >
              {savingsPercent > 0 && (
                <View style={styles.savingsBadge}>
                  <Text style={styles.savingsText}>Save {savingsPercent}%</Text>
                </View>
              )}
              <Text style={styles.planTitle}>Annual</Text>
              <View style={styles.priceRow}>
                <Text style={styles.planPrice}>{annualPackage.product.priceString}</Text>
                <Text style={styles.planPeriod}>/year</Text>
              </View>
              <Text style={styles.planSubtext}>
                {(annualPrice / 12).toFixed(2)}/month
              </Text>
            </TouchableOpacity>
          )}

          {monthlyPackage && (
            <TouchableOpacity
              style={[
                styles.planCard,
                selectedPackage?.identifier === monthlyPackage.identifier && styles.selectedPlan,
              ]}
              onPress={() => setSelectedPackage(monthlyPackage)}
            >
              <Text style={styles.planTitle}>Monthly</Text>
              <View style={styles.priceRow}>
                <Text style={styles.planPrice}>{monthlyPackage.product.priceString}</Text>
                <Text style={styles.planPeriod}>/month</Text>
              </View>
            </TouchableOpacity>
          )}
        </View>

        {/* Features List */}
        <View style={styles.featuresContainer}>
          <Text style={styles.featuresTitle}>What's Included</Text>
          {FEATURES.map((feature, index) => (
            <View key={index} style={styles.featureRow}>
              <View style={[styles.featureIcon, feature.free ? styles.freeIcon : styles.proIcon]}>
                <Text style={styles.featureCheck}>{feature.free ? '✓' : '★'}</Text>
              </View>
              <View style={styles.featureInfo}>
                <Text style={styles.featureTitle}>
                  {feature.title}
                  {!feature.free && <Text style={styles.proBadge}> PRO</Text>}
                </Text>
                <Text style={styles.featureDescription}>{feature.description}</Text>
              </View>
            </View>
          ))}
        </View>

        {/* CTA */}
        <View style={styles.ctaContainer}>
          <Button
            title={
              selectedPackage?.product.introPrice
                ? `Start ${selectedPackage.product.introPrice.periodNumberOfUnits}-Day Free Trial`
                : 'Subscribe Now'
            }
            onPress={handlePurchase}
            size="large"
            loading={isPurchasing}
            disabled={!selectedPackage}
          />
          <Text style={styles.trialNote}>
            {selectedPackage?.product.introPrice
              ? `Free for ${selectedPackage.product.introPrice.periodNumberOfUnits} days, then ${selectedPackage.product.priceString}. Cancel anytime.`
              : `${selectedPackage?.product.priceString || ''} Cancel anytime.`}
          </Text>

          <TouchableOpacity
            onPress={handleRestore}
            disabled={isRestoring}
            style={styles.restoreButton}
          >
            <Text style={styles.restoreText}>
              {isRestoring ? 'Restoring...' : 'Restore Purchase'}
            </Text>
          </TouchableOpacity>
        </View>

        {/* Legal */}
        <View style={styles.legalContainer}>
          <Text style={styles.legalText}>
            Payment will be charged to your Apple ID account at confirmation of
            purchase. Subscription automatically renews unless canceled at least
            24 hours before the end of the current period. You can manage and
            cancel your subscriptions in your account settings on the App Store.
          </Text>
          <View style={styles.legalLinks}>
            <TouchableOpacity>
              <Text style={styles.legalLink}>Terms of Service</Text>
            </TouchableOpacity>
            <Text style={styles.legalDivider}>|</Text>
            <TouchableOpacity>
              <Text style={styles.legalLink}>Privacy Policy</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: Colors.background,
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 40,
  },
  closeButton: {
    alignSelf: 'flex-end',
  },
  closeText: {
    color: Colors.white,
    fontSize: 16,
    fontWeight: '500',
  },
  headerTitle: {
    fontSize: 32,
    fontWeight: '700',
    color: Colors.white,
    marginTop: 20,
    textAlign: 'center',
  },
  headerSubtitle: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.8)',
    marginTop: 8,
    textAlign: 'center',
  },
  scrollContent: {
    paddingBottom: 40,
  },
  plansContainer: {
    flexDirection: 'row',
    paddingHorizontal: 20,
    marginTop: -20,
    gap: 12,
  },
  planCard: {
    flex: 1,
    backgroundColor: Colors.white,
    borderRadius: 16,
    padding: 16,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: Colors.border,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  selectedPlan: {
    borderColor: Colors.primary,
  },
  savingsBadge: {
    position: 'absolute',
    top: -10,
    backgroundColor: Colors.success,
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  savingsText: {
    color: Colors.white,
    fontSize: 12,
    fontWeight: '700',
  },
  planTitle: {
    fontSize: 14,
    color: Colors.textSecondary,
    fontWeight: '600',
    marginTop: 8,
  },
  priceRow: {
    flexDirection: 'row',
    alignItems: 'baseline',
    marginTop: 8,
  },
  planPrice: {
    fontSize: 28,
    fontWeight: '700',
    color: Colors.text,
  },
  planPeriod: {
    fontSize: 14,
    color: Colors.textSecondary,
    marginLeft: 2,
  },
  planSubtext: {
    fontSize: 12,
    color: Colors.textSecondary,
    marginTop: 4,
  },
  featuresContainer: {
    paddingHorizontal: 20,
    marginTop: 32,
  },
  featuresTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: Colors.text,
    marginBottom: 20,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  featureIcon: {
    width: 28,
    height: 28,
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
  },
  freeIcon: {
    backgroundColor: Colors.border,
  },
  proIcon: {
    backgroundColor: Colors.primary,
  },
  featureCheck: {
    color: Colors.white,
    fontSize: 14,
    fontWeight: '700',
  },
  featureInfo: {
    flex: 1,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: Colors.text,
  },
  proBadge: {
    fontSize: 10,
    color: Colors.primary,
    fontWeight: '700',
  },
  featureDescription: {
    fontSize: 14,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  ctaContainer: {
    paddingHorizontal: 20,
    marginTop: 32,
  },
  trialNote: {
    textAlign: 'center',
    fontSize: 13,
    color: Colors.textSecondary,
    marginTop: 12,
  },
  restoreButton: {
    alignItems: 'center',
    marginTop: 20,
  },
  restoreText: {
    fontSize: 14,
    color: Colors.primary,
    fontWeight: '500',
  },
  legalContainer: {
    paddingHorizontal: 20,
    marginTop: 32,
  },
  legalText: {
    fontSize: 11,
    color: Colors.textLight,
    lineHeight: 16,
  },
  legalLinks: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 16,
  },
  legalLink: {
    fontSize: 12,
    color: Colors.primary,
  },
  legalDivider: {
    fontSize: 12,
    color: Colors.textLight,
    marginHorizontal: 8,
  },
});
```

---

## 5. Paywall Strategy

### When to Show Paywall

**Session-based triggers:**

```typescript
// In AppContext or a dedicated hook
const SESSION_THRESHOLD = 3;

async function checkPaywallTrigger(): Promise<boolean> {
  const sessionCount = await AsyncStorage.getItem('session_count');
  const count = sessionCount ? parseInt(sessionCount, 10) : 0;

  if (count >= SESSION_THRESHOLD) {
    return true; // Show paywall
  }

  await AsyncStorage.setItem('session_count', (count + 1).toString());
  return false;
}
```

**Feature-gated triggers:**

```typescript
// Gate premium features
function FeatureGate({
  children,
  onShowPaywall
}: {
  children: React.ReactNode;
  onShowPaywall: () => void;
}) {
  const { isPremium } = usePremium();

  if (!isPremium) {
    return (
      <TouchableOpacity onPress={onShowPaywall}>
        <View style={styles.lockedFeature}>
          <Text>Unlock with Pro</Text>
        </View>
      </TouchableOpacity>
    );
  }

  return <>{children}</>;
}
```

**Recommended trigger points:**

| Trigger | When | Conversion Impact |
|---------|------|-------------------|
| After onboarding | First app open | Medium |
| After 3rd session | Returning user | High |
| Feature tap | User wants something | Highest |
| After completing task | Positive moment | High |
| Settings page | User exploring | Low |

### A/B Testing Setup

RevenueCat supports A/B testing via Offerings:

1. Create multiple offerings:
   - `control` - Current pricing
   - `high_price` - 20% higher
   - `low_price` - 20% lower

2. In RevenueCat > Experiments:
   - Create experiment
   - Set traffic split (e.g., 33/33/33)
   - Define success metric (usually trial conversion)

3. Code handles automatically:

```typescript
// RevenueCat returns the assigned offering
const offerings = await Purchases.getOfferings();
const assignedOffering = offerings.current; // User's test variant
```

### Pricing Display Best Practices

1. **Lead with annual** - Higher LTV, set as default selection
2. **Show monthly equivalent** - "$4.99/month" under annual price
3. **Calculate savings** - "Save 40%" badge on annual
4. **Trial emphasis** - "Start 7-Day Free Trial" as CTA
5. **Social proof** - "Join 10,000+ users" if applicable

---

## 6. Testing

### Sandbox Testing Setup

**Create sandbox tester (App Store Connect):**

1. Go to Users and Access > Sandbox > Testers
2. Click "+" to add tester
3. Enter email (fake but valid format: `test1@example.com`)
4. Set password
5. Select country

**Configure device:**

1. On iPhone: Settings > App Store
2. Scroll to bottom, tap "Sandbox Account"
3. Sign in with sandbox tester credentials

### Sandbox Subscription Timing

Subscriptions renew faster in sandbox:

| Real Duration | Sandbox Duration |
|---------------|------------------|
| 1 week | 3 minutes |
| 1 month | 5 minutes |
| 3 months | 15 minutes |
| 6 months | 30 minutes |
| 1 year | 1 hour |

### Test Accounts in RevenueCat

For quick testing without actual sandbox purchases:

1. Go to RevenueCat > Customers
2. Click "Create Customer"
3. Enter test user ID
4. Grant entitlement manually
5. Test app behavior

### Common Issues and Solutions

**Issue: "No offerings found"**
- Check API key is correct (ios vs android)
- Verify products are in "Ready to Submit" status in App Store Connect
- Confirm products are linked to offerings in RevenueCat
- Wait 15-30 minutes after creating products

**Issue: "Invalid product identifier"**
- Product ID in code must exactly match App Store Connect
- Products must be approved or in sandbox review

**Issue: Purchase completes but entitlement not active**
- Check entitlement name matches code (`premium` vs `PREMIUM`)
- Verify products are linked to entitlement in RevenueCat

**Issue: Restore not finding purchase**
- User must be signed into same Apple ID
- In sandbox, check sandbox account is active
- Purchases made on other apps in same account won't restore

### Testing Checklist

```
[ ] SDK initializes without errors
[ ] Offerings load correctly
[ ] Prices display in user's currency
[ ] Monthly purchase completes
[ ] Annual purchase completes
[ ] Trial starts correctly
[ ] Entitlement active after purchase
[ ] Entitlement persists across app restart
[ ] Restore finds previous purchase
[ ] Restore handles no-purchase case
[ ] Paywall dismisses on purchase
[ ] Premium features unlock
[ ] Subscription renews in sandbox
[ ] Cancellation expires entitlement
```

---

## 7. Update AppContext for RevenueCat

Replace the AsyncStorage-based premium check with RevenueCat:

```typescript
// In src/context/AppContext.tsx

import {
  checkPremiumStatus,
  addPurchaseListener
} from '../services/purchases';

// In AppProvider:
useEffect(() => {
  const loadData = async () => {
    const [
      loadedSettings,
      loadedStreak,
      locked,
      // Use RevenueCat instead of AsyncStorage
    ] = await Promise.all([
      getSettings(),
      getStreakData(),
      getLockState(),
    ]);

    // Check RevenueCat for premium status
    const premium = await checkPremiumStatus();

    setSettings(loadedSettings);
    setStreakData(loadedStreak);
    setIsLocked(locked);
    setIsPremium(premium);
    setIsLoading(false);
  };

  loadData();

  // Listen for subscription changes
  const unsubscribe = addPurchaseListener((info) => {
    const isPremium = info.entitlements.active['premium'] !== undefined;
    setIsPremium(isPremium);
  });

  return unsubscribe;
}, []);
```

---

## 8. File Structure Summary

After integration, your app should have:

```
src/
├── services/
│   └── purchases.ts          # RevenueCat API wrapper
├── hooks/
│   ├── usePremium.ts         # Premium status hook
│   ├── useOfferings.ts       # Offerings hook
│   └── useTimer.ts           # Existing
├── screens/
│   ├── PaywallScreen.tsx     # Updated with RevenueCat
│   └── ...
├── context/
│   └── AppContext.tsx        # Updated to use RevenueCat
└── config/
    └── revenuecat.ts         # API keys and config
```

---

## 9. Quick Reference

### Product IDs

| App | Monthly | Annual |
|-----|---------|--------|
| PrayerLock | `prayerlock_monthly_999` | `prayerlock_annual_4999` |
| WalkToUnlock | `walktounlock_monthly_799` | `walktounlock_annual_3999` |
| StudyLock | `studylock_monthly_699` | `studylock_annual_3499` |

### Entitlement

All apps use: `premium`

### Package Identifiers

- Monthly: `$rc_monthly`
- Annual: `$rc_annual`

---

## 10. Go-Live Checklist

```
[ ] Production API keys configured
[ ] Products approved in App Store Connect
[ ] Entitlements linked to products
[ ] Offerings set as "current"
[ ] Debug logging disabled
[ ] Webhook endpoint configured (if using server)
[ ] Privacy policy updated with subscription terms
[ ] App Store description includes subscription details
[ ] Price displayed matches App Store Connect
```

---

Created: 2026-01-24
