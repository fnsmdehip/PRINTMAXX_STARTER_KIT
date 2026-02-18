# RevenueCat Integration Guide

Complete setup guide for RevenueCat across all apps. Covers initial setup, per-app configuration, code integration, and analytics.

---

## 1. Initial setup

### Create RevenueCat project

1. Log into RevenueCat dashboard (app.revenuecat.com)
2. Click "Create New Project"
3. Name it "PRINTMAXX Apps" (groups all apps together)
4. Note your project ID for later

### iOS configuration

**In App Store Connect:**

1. Go to Users and Access > Integrations > In-App Purchase
2. Click "Generate In-App Purchase Key"
3. Download the .p8 file (save securely)
4. Note the Key ID and Issuer ID

**In RevenueCat:**

1. Go to Project Settings > Apps > Add App
2. Select "iOS"
3. Enter your app's Bundle ID
4. Enter App Store Connect credentials:
   - Issuer ID
   - Key ID
   - Upload the .p8 file
5. Click "Connect to App Store Connect"

**Shared secret (for receipt validation):**

1. In App Store Connect, go to your app > App Information
2. Scroll to "App-Specific Shared Secret"
3. Generate if not exists
4. Copy and paste into RevenueCat app settings

### Stripe connection (for web subscriptions)

**In Stripe:**

1. Go to Developers > Webhooks
2. Click "Add endpoint"
3. Copy the RevenueCat webhook URL (from RevenueCat > Integrations > Stripe)
4. Select events:
   - customer.subscription.created
   - customer.subscription.updated
   - customer.subscription.deleted
   - invoice.paid
   - invoice.payment_failed
   - checkout.session.completed
5. Click "Add endpoint"
6. Copy the Signing Secret

**In RevenueCat:**

1. Go to Project Settings > Integrations > Stripe
2. Click "Connect to Stripe" (OAuth flow) or enter API keys manually
3. Paste the webhook signing secret
4. Enable "Use Stripe for web subscriptions"

### Product setup in App Store Connect

For each subscription product:

1. Go to App Store Connect > Your App > Subscriptions
2. Create a Subscription Group (e.g., "Premium")
3. Add subscription products:

**Product ID naming convention:**
```
{app_prefix}_{duration}_{price_cents}
Example: prayerlock_monthly_999
Example: prayerlock_annual_4999
```

---

## 2. Per-app configuration

### PrayerLock

**App Store Connect products:**

| Product ID | Type | Price | Duration |
|------------|------|-------|----------|
| prayerlock_monthly_999 | Auto-renewable | $9.99 | 1 month |
| prayerlock_annual_4999 | Auto-renewable | $49.99 | 1 year |

**RevenueCat setup:**

1. Create entitlement: `premium`
2. Create offering: `default`
3. Create packages:
   - `$rc_monthly` -> prayerlock_monthly_999
   - `$rc_annual` -> prayerlock_annual_4999
4. Set annual as "current offering" (higher LTV)

**Trial configuration:**
- 3-day free trial on monthly
- 7-day free trial on annual

---

### WalkToUnlock

**App Store Connect products:**

| Product ID | Type | Price | Duration |
|------------|------|-------|----------|
| walktounlock_monthly_799 | Auto-renewable | $7.99 | 1 month |
| walktounlock_annual_3999 | Auto-renewable | $39.99 | 1 year |

**RevenueCat setup:**

1. Create entitlement: `premium`
2. Create offering: `default`
3. Create packages:
   - `$rc_monthly` -> walktounlock_monthly_799
   - `$rc_annual` -> walktounlock_annual_3999

**Trial configuration:**
- 3-day free trial (quick value demonstration for screen blockers)

---

### StudyLock

**App Store Connect products:**

| Product ID | Type | Price | Duration |
|------------|------|-------|----------|
| studylock_monthly_699 | Auto-renewable | $6.99 | 1 month |
| studylock_annual_3499 | Auto-renewable | $34.99 | 1 year |

**RevenueCat setup:**

1. Create entitlement: `premium`
2. Create offering: `default`
3. Create packages:
   - `$rc_monthly` -> studylock_monthly_699
   - `$rc_annual` -> studylock_annual_3499

**Trial configuration:**
- 3-day free trial

---

### PromptVault

**App Store Connect products:**

| Product ID | Type | Price | Duration |
|------------|------|-------|----------|
| promptvault_monthly_499 | Auto-renewable | $4.99 | 1 month |
| promptvault_annual_2999 | Auto-renewable | $29.99 | 1 year |

**RevenueCat setup:**

1. Create entitlement: `premium`
2. Create offering: `default`
3. Create packages:
   - `$rc_monthly` -> promptvault_monthly_499
   - `$rc_annual` -> promptvault_annual_2999

**Trial configuration:**
- 7-day free trial (needs time to show value)

---

### DailyAnchor

**App Store Connect products:**

| Product ID | Type | Price | Duration |
|------------|------|-------|----------|
| dailyanchor_monthly_499 | Auto-renewable | $4.99 | 1 month |
| dailyanchor_annual_2999 | Auto-renewable | $29.99 | 1 year |

**RevenueCat setup:**

1. Create entitlement: `premium`
2. Create offering: `default`
3. Create packages:
   - `$rc_monthly` -> dailyanchor_monthly_499
   - `$rc_annual` -> dailyanchor_annual_2999

**Trial configuration:**
- 7-day free trial (habit formation needs time)

---

### FemFit

**App Store Connect products:**

| Product ID | Type | Price | Duration |
|------------|------|-------|----------|
| femfit_monthly_799 | Auto-renewable | $7.99 | 1 month |
| femfit_annual_3999 | Auto-renewable | $39.99 | 1 year |

**RevenueCat setup:**

1. Create entitlement: `premium`
2. Create offering: `default`
3. Create packages:
   - `$rc_monthly` -> femfit_monthly_799
   - `$rc_annual` -> femfit_annual_3999

**Trial configuration:**
- 7-day free trial

---

### DailyDevotion

**App Store Connect products:**

| Product ID | Type | Price | Duration |
|------------|------|-------|----------|
| dailydevotion_monthly_499 | Auto-renewable | $4.99 | 1 month |
| dailydevotion_annual_2499 | Auto-renewable | $24.99 | 1 year |

**RevenueCat setup:**

1. Create entitlement: `premium`
2. Create offering: `default`
3. Create packages:
   - `$rc_monthly` -> dailydevotion_monthly_499
   - `$rc_annual` -> dailydevotion_annual_2499

**Trial configuration:**
- 7-day free trial (content needs sampling)

---

## 3. Code integration

### React Native SDK setup

**Install dependencies:**

```bash
npm install react-native-purchases
cd ios && pod install
```

**Initialize SDK (App.tsx or root):**

```typescript
import Purchases, { LOG_LEVEL } from 'react-native-purchases';

const REVENUECAT_API_KEY = {
  ios: 'appl_xxxxxxxxxx',
  android: 'goog_xxxxxxxxxx', // if adding Android later
};

export const initializePurchases = async () => {
  Purchases.setLogLevel(LOG_LEVEL.DEBUG); // Remove in production

  if (Platform.OS === 'ios') {
    await Purchases.configure({ apiKey: REVENUECAT_API_KEY.ios });
  } else if (Platform.OS === 'android') {
    await Purchases.configure({ apiKey: REVENUECAT_API_KEY.android });
  }
};

// Call on app start
useEffect(() => {
  initializePurchases();
}, []);
```

**Identify users (after auth):**

```typescript
// Call when user logs in or creates account
const identifyUser = async (userId: string) => {
  try {
    const { customerInfo } = await Purchases.logIn(userId);
    return customerInfo;
  } catch (error) {
    console.error('RevenueCat identify error:', error);
  }
};

// Call on logout
const logoutUser = async () => {
  try {
    await Purchases.logOut();
  } catch (error) {
    console.error('RevenueCat logout error:', error);
  }
};
```

### Paywall implementation

**Fetch offerings:**

```typescript
import Purchases, {
  PurchasesOffering,
  PurchasesPackage,
} from 'react-native-purchases';

const useOfferings = () => {
  const [offerings, setOfferings] = useState<PurchasesOffering | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOfferings = async () => {
      try {
        const offerings = await Purchases.getOfferings();
        if (offerings.current) {
          setOfferings(offerings.current);
        }
      } catch (error) {
        console.error('Error fetching offerings:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchOfferings();
  }, []);

  return { offerings, loading };
};
```

**Paywall component:**

```typescript
import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import Purchases, { PurchasesPackage } from 'react-native-purchases';

interface PaywallProps {
  onPurchaseComplete: () => void;
  onClose: () => void;
}

export const Paywall: React.FC<PaywallProps> = ({
  onPurchaseComplete,
  onClose,
}) => {
  const { offerings, loading } = useOfferings();
  const [purchasing, setPurchasing] = useState(false);

  const handlePurchase = async (pkg: PurchasesPackage) => {
    setPurchasing(true);
    try {
      const { customerInfo } = await Purchases.purchasePackage(pkg);

      if (customerInfo.entitlements.active['premium']) {
        onPurchaseComplete();
      }
    } catch (error: any) {
      if (!error.userCancelled) {
        Alert.alert('Purchase Error', 'Unable to complete purchase. Please try again.');
      }
    } finally {
      setPurchasing(false);
    }
  };

  if (loading) {
    return <ActivityIndicator />;
  }

  const monthlyPackage = offerings?.monthly;
  const annualPackage = offerings?.annual;

  // Calculate savings percentage
  const monthlyPrice = monthlyPackage?.product.price || 0;
  const annualPrice = annualPackage?.product.price || 0;
  const annualMonthlyEquivalent = annualPrice / 12;
  const savingsPercent = Math.round(
    ((monthlyPrice - annualMonthlyEquivalent) / monthlyPrice) * 100
  );

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.closeButton} onPress={onClose}>
        <Text style={styles.closeText}>X</Text>
      </TouchableOpacity>

      <Text style={styles.title}>Unlock Premium</Text>
      <Text style={styles.subtitle}>
        Get full access to all features
      </Text>

      {/* Feature list */}
      <View style={styles.features}>
        <FeatureItem text="Unlimited usage" />
        <FeatureItem text="All premium features" />
        <FeatureItem text="Priority support" />
        <FeatureItem text="No ads" />
      </View>

      {/* Package options */}
      <View style={styles.packages}>
        {annualPackage && (
          <PackageOption
            package={annualPackage}
            label="Annual"
            sublabel={`Save ${savingsPercent}%`}
            recommended
            onSelect={() => handlePurchase(annualPackage)}
            disabled={purchasing}
          />
        )}

        {monthlyPackage && (
          <PackageOption
            package={monthlyPackage}
            label="Monthly"
            onSelect={() => handlePurchase(monthlyPackage)}
            disabled={purchasing}
          />
        )}
      </View>

      {/* Trial info */}
      {annualPackage?.product.introPrice && (
        <Text style={styles.trialText}>
          Start your {annualPackage.product.introPrice.periodNumberOfUnits}-day
          free trial
        </Text>
      )}

      {/* Terms */}
      <Text style={styles.terms}>
        Cancel anytime. Subscription auto-renews.
      </Text>
    </View>
  );
};

interface PackageOptionProps {
  package: PurchasesPackage;
  label: string;
  sublabel?: string;
  recommended?: boolean;
  onSelect: () => void;
  disabled: boolean;
}

const PackageOption: React.FC<PackageOptionProps> = ({
  package: pkg,
  label,
  sublabel,
  recommended,
  onSelect,
  disabled,
}) => (
  <TouchableOpacity
    style={[
      styles.packageOption,
      recommended && styles.recommendedPackage,
    ]}
    onPress={onSelect}
    disabled={disabled}
  >
    {recommended && (
      <View style={styles.recommendedBadge}>
        <Text style={styles.recommendedText}>BEST VALUE</Text>
      </View>
    )}
    <Text style={styles.packageLabel}>{label}</Text>
    <Text style={styles.packagePrice}>
      {pkg.product.priceString}
      {pkg.packageType === 'ANNUAL' ? '/year' : '/month'}
    </Text>
    {sublabel && <Text style={styles.packageSublabel}>{sublabel}</Text>}
  </TouchableOpacity>
);

const FeatureItem: React.FC<{ text: string }> = ({ text }) => (
  <View style={styles.featureItem}>
    <Text style={styles.checkmark}>✓</Text>
    <Text style={styles.featureText}>{text}</Text>
  </View>
);

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    backgroundColor: '#fff',
  },
  closeButton: {
    position: 'absolute',
    top: 16,
    right: 16,
    padding: 8,
  },
  closeText: {
    fontSize: 18,
    fontWeight: '600',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
    marginTop: 40,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginTop: 8,
  },
  features: {
    marginTop: 32,
    marginBottom: 32,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  checkmark: {
    fontSize: 18,
    color: '#22c55e',
    marginRight: 12,
  },
  featureText: {
    fontSize: 16,
  },
  packages: {
    gap: 12,
  },
  packageOption: {
    borderWidth: 2,
    borderColor: '#e5e5e5',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  recommendedPackage: {
    borderColor: '#3b82f6',
    backgroundColor: '#eff6ff',
  },
  recommendedBadge: {
    position: 'absolute',
    top: -12,
    backgroundColor: '#3b82f6',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  recommendedText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  packageLabel: {
    fontSize: 18,
    fontWeight: '600',
  },
  packagePrice: {
    fontSize: 24,
    fontWeight: 'bold',
    marginTop: 4,
  },
  packageSublabel: {
    fontSize: 14,
    color: '#22c55e',
    marginTop: 4,
  },
  trialText: {
    textAlign: 'center',
    marginTop: 16,
    fontSize: 14,
    color: '#666',
  },
  terms: {
    textAlign: 'center',
    marginTop: 24,
    fontSize: 12,
    color: '#999',
  },
});
```

### Entitlement checking

**Hook for checking premium status:**

```typescript
import { useEffect, useState } from 'react';
import Purchases, { CustomerInfo } from 'react-native-purchases';

export const usePremiumStatus = () => {
  const [isPremium, setIsPremium] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const customerInfo = await Purchases.getCustomerInfo();
        setIsPremium(customerInfo.entitlements.active['premium'] !== undefined);
      } catch (error) {
        console.error('Error checking premium status:', error);
      } finally {
        setLoading(false);
      }
    };

    checkStatus();

    // Listen for changes
    const customerInfoUpdateListener = (info: CustomerInfo) => {
      setIsPremium(info.entitlements.active['premium'] !== undefined);
    };

    Purchases.addCustomerInfoUpdateListener(customerInfoUpdateListener);

    return () => {
      Purchases.removeCustomerInfoUpdateListener(customerInfoUpdateListener);
    };
  }, []);

  return { isPremium, loading };
};
```

**Usage in components:**

```typescript
const MyFeature = () => {
  const { isPremium, loading } = usePremiumStatus();
  const [showPaywall, setShowPaywall] = useState(false);

  if (loading) {
    return <ActivityIndicator />;
  }

  if (!isPremium) {
    return (
      <>
        <TouchableOpacity onPress={() => setShowPaywall(true)}>
          <Text>Upgrade to Premium</Text>
        </TouchableOpacity>

        <Modal visible={showPaywall}>
          <Paywall
            onPurchaseComplete={() => setShowPaywall(false)}
            onClose={() => setShowPaywall(false)}
          />
        </Modal>
      </>
    );
  }

  return <PremiumFeatureContent />;
};
```

### Restore purchases

```typescript
const RestorePurchasesButton = () => {
  const [restoring, setRestoring] = useState(false);

  const handleRestore = async () => {
    setRestoring(true);
    try {
      const customerInfo = await Purchases.restorePurchases();

      if (customerInfo.entitlements.active['premium']) {
        Alert.alert('Success', 'Your purchases have been restored.');
      } else {
        Alert.alert(
          'No Purchases Found',
          'No previous purchases were found for this account.'
        );
      }
    } catch (error) {
      Alert.alert('Error', 'Unable to restore purchases. Please try again.');
    } finally {
      setRestoring(false);
    }
  };

  return (
    <TouchableOpacity onPress={handleRestore} disabled={restoring}>
      <Text>{restoring ? 'Restoring...' : 'Restore Purchases'}</Text>
    </TouchableOpacity>
  );
};
```

### Receipt validation (server-side, optional)

For most apps, RevenueCat handles validation. If you need server-side verification:

```typescript
// Server endpoint example (Node.js/Express)
import Purchases from 'purchases-js';

const purchases = new Purchases('your_revenuecat_api_key');

app.post('/api/verify-subscription', async (req, res) => {
  const { userId } = req.body;

  try {
    const customerInfo = await purchases.getSubscriberInfo(userId);
    const isPremium = customerInfo.entitlements.active['premium'] !== undefined;

    res.json({
      isPremium,
      expiresDate: customerInfo.entitlements.active['premium']?.expirationDate,
    });
  } catch (error) {
    res.status(500).json({ error: 'Failed to verify subscription' });
  }
});
```

---

## 4. Webhook setup

### Events to track

Configure webhooks in RevenueCat > Project Settings > Webhooks:

**Revenue events:**
- INITIAL_PURCHASE - New subscription started
- RENEWAL - Subscription renewed
- CANCELLATION - User cancelled
- EXPIRATION - Subscription expired
- BILLING_ISSUE - Payment failed

**Trial events:**
- SUBSCRIPTION_STARTED - Trial started
- TRIAL_CONVERTED - Trial became paid
- TRIAL_CANCELLED - Cancelled during trial

### Server integration (Node.js example)

```typescript
import express from 'express';
import crypto from 'crypto';

const REVENUECAT_WEBHOOK_SECRET = process.env.REVENUECAT_WEBHOOK_SECRET;

// Verify webhook signature
const verifyWebhook = (req: express.Request): boolean => {
  const signature = req.headers['x-revenuecat-signature'] as string;
  const payload = JSON.stringify(req.body);

  const expectedSignature = crypto
    .createHmac('sha256', REVENUECAT_WEBHOOK_SECRET)
    .update(payload)
    .digest('hex');

  return signature === expectedSignature;
};

app.post('/webhooks/revenuecat', express.json(), async (req, res) => {
  if (!verifyWebhook(req)) {
    return res.status(401).json({ error: 'Invalid signature' });
  }

  const event = req.body;
  const { type, app_user_id, product_id, event_timestamp_ms } = event;

  switch (type) {
    case 'INITIAL_PURCHASE':
      // New subscriber
      await trackEvent('subscription_started', {
        userId: app_user_id,
        productId: product_id,
        timestamp: event_timestamp_ms,
      });
      // Send welcome email, unlock features, etc.
      break;

    case 'RENEWAL':
      // Subscription renewed
      await trackEvent('subscription_renewed', {
        userId: app_user_id,
        productId: product_id,
      });
      break;

    case 'CANCELLATION':
      // User cancelled (still has access until expiration)
      await trackEvent('subscription_cancelled', {
        userId: app_user_id,
        productId: product_id,
      });
      // Optionally trigger win-back email
      break;

    case 'EXPIRATION':
      // Access revoked
      await trackEvent('subscription_expired', {
        userId: app_user_id,
      });
      // Lock premium features
      break;

    case 'BILLING_ISSUE':
      // Payment failed
      await trackEvent('billing_issue', {
        userId: app_user_id,
      });
      // Send dunning email
      break;

    default:
      console.log('Unhandled event type:', type);
  }

  res.json({ received: true });
});
```

---

## 5. Testing

### Sandbox testing setup

**Create sandbox tester in App Store Connect:**

1. Go to Users and Access > Sandbox > Testers
2. Click "+" to add new tester
3. Enter email (can be fake but valid format)
4. Set password
5. Save

**Important:** Use a NEW email, not your real Apple ID.

### Configure device for sandbox

1. On iPhone, go to Settings > App Store
2. Scroll to bottom, tap "Sandbox Account"
3. Sign in with sandbox tester credentials
4. Your app will now use sandbox for purchases

### Test user creation in RevenueCat

For quick testing without sandbox:

1. Go to RevenueCat > Customers > Add Customer
2. Enter a test user ID (e.g., "test_user_001")
3. Grant entitlements manually
4. Test app behavior

### Purchase simulation

**Test successful purchase:**
```typescript
// In development, you can manually grant entitlements
// RevenueCat Dashboard > Customers > Find User > Grant Entitlement
```

**Test trial flow:**
1. Use sandbox account
2. Start trial
3. Check trial days remaining: `customerInfo.entitlements.active['premium']?.periodType`
4. Fast-forward time in sandbox (subscriptions renew quickly)

**Test restoration:**
1. Purchase on device A
2. Delete and reinstall app
3. Tap "Restore Purchases"
4. Verify access restored

**Test cancellation:**
1. Purchase subscription
2. Cancel in sandbox Settings
3. Wait for expiration
4. Verify access revoked

### Sandbox subscription timing

In sandbox, subscriptions renew faster:

| Real duration | Sandbox duration |
|---------------|------------------|
| 1 week | 3 minutes |
| 1 month | 5 minutes |
| 2 months | 10 minutes |
| 3 months | 15 minutes |
| 6 months | 30 minutes |
| 1 year | 1 hour |

---

## 6. Analytics

### Key metrics to track

**RevenueCat dashboard shows:**

| Metric | Target | Action if below target |
|--------|--------|------------------------|
| Trial start rate | >25% | Improve paywall design, reduce friction |
| Trial conversion | >15% | Optimize onboarding, show value faster |
| Monthly churn | <8% | Improve engagement, add features |
| MRR | Growing 10%+ | Scale acquisition |
| Realized LTV | >$30 | Reduce churn or raise prices |
| Refund rate | <2% | Improve product quality |

### Dashboard setup

**Create custom charts:**

1. Go to RevenueCat > Charts
2. Add these charts to your default view:
   - MRR over time
   - Active subscriptions by product
   - Trial conversion rate
   - Churn rate by period
   - Revenue by country

**Segment by app:**

Filter dashboard by App ID to see per-app metrics:
- PrayerLock metrics
- WalkToUnlock metrics
- etc.

### Alerts configuration

**Set up alerts in RevenueCat > Project Settings > Alerts:**

1. **Churn spike alert**
   - Trigger: Daily churn > 2x average
   - Action: Investigate immediately

2. **Revenue drop alert**
   - Trigger: Daily revenue < 50% of 7-day average
   - Action: Check for technical issues

3. **Billing issues alert**
   - Trigger: > 10 billing issues/day
   - Action: Review dunning emails

4. **Refund spike alert**
   - Trigger: Daily refunds > 5% of transactions
   - Action: Review product/messaging

### Integration with external analytics

**Mixpanel integration:**

```typescript
// RevenueCat > Integrations > Mixpanel
// Enter Mixpanel project token

// Events sent automatically:
// - $rc_initial_purchase
// - $rc_renewal
// - $rc_cancellation
// - $rc_subscription_started
```

**Custom event tracking:**

```typescript
import analytics from '@segment/analytics-react-native';

// Track paywall views
const trackPaywallView = (source: string) => {
  analytics.track('Paywall Viewed', {
    source,
    timestamp: new Date().toISOString(),
  });
};

// Track purchase attempts
const trackPurchaseAttempt = (packageType: string, success: boolean) => {
  analytics.track('Purchase Attempted', {
    packageType,
    success,
  });
};
```

---

## Quick reference

### Product IDs by app

| App | Monthly | Annual |
|-----|---------|--------|
| PrayerLock | prayerlock_monthly_999 | prayerlock_annual_4999 |
| WalkToUnlock | walktounlock_monthly_799 | walktounlock_annual_3999 |
| StudyLock | studylock_monthly_699 | studylock_annual_3499 |
| PromptVault | promptvault_monthly_499 | promptvault_annual_2999 |
| DailyAnchor | dailyanchor_monthly_499 | dailyanchor_annual_2999 |
| FemFit | femfit_monthly_799 | femfit_annual_3999 |
| DailyDevotion | dailydevotion_monthly_499 | dailydevotion_annual_2499 |

### Entitlement names

All apps use: `premium`

### RevenueCat API keys

Store in environment variables:

```bash
# .env (never commit)
REVENUECAT_IOS_KEY_PRAYERLOCK=appl_xxx
REVENUECAT_IOS_KEY_WALKTOUNLOCK=appl_xxx
REVENUECAT_IOS_KEY_STUDYLOCK=appl_xxx
REVENUECAT_IOS_KEY_PROMPTVAULT=appl_xxx
REVENUECAT_IOS_KEY_DAILYANCHOR=appl_xxx
REVENUECAT_IOS_KEY_FEMFIT=appl_xxx
REVENUECAT_IOS_KEY_DAILYDEVOTION=appl_xxx
REVENUECAT_WEBHOOK_SECRET=whsec_xxx
```

---

## Checklist

### Initial setup
- [ ] RevenueCat project created
- [ ] App Store Connect API key generated
- [ ] Shared secret configured
- [ ] Stripe integration connected (if using web)

### Per-app setup
- [ ] Products created in App Store Connect
- [ ] RevenueCat app configured
- [ ] Entitlements created
- [ ] Offerings configured
- [ ] Packages linked to products

### Code integration
- [ ] SDK installed and initialized
- [ ] User identification working
- [ ] Paywall component built
- [ ] Entitlement checking implemented
- [ ] Restore purchases working

### Testing
- [ ] Sandbox tester created
- [ ] Purchase flow tested
- [ ] Trial flow tested
- [ ] Restoration tested
- [ ] Cancellation flow tested

### Go live
- [ ] Production API keys configured
- [ ] Webhooks configured
- [ ] Alerts set up
- [ ] Analytics dashboard configured

---

Created: 2026-01-21
