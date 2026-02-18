# RevenueCat Integration Guide

Complete setup guide for integrating RevenueCat subscriptions into React Native apps.

---

## 1. Installation

### Install the SDK

```bash
# Using npm
npm install react-native-purchases

# Using yarn
yarn add react-native-purchases
```

### iOS setup

```bash
cd ios && pod install && cd ..
```

Add to your `ios/YourApp/Info.plist`:

```xml
<key>SKAdNetworkItems</key>
<array>
  <dict>
    <key>SKAdNetworkIdentifier</key>
    <string>cstr6suwn9.skadnetwork</string>
  </dict>
</array>
```

### Android setup (if applicable)

Add to `android/app/build.gradle`:

```gradle
dependencies {
    implementation 'com.revenuecat.purchases:purchases:6.+'
}
```

---

## 2. RevenueCat dashboard setup

### Create a project

1. Go to [app.revenuecat.com](https://app.revenuecat.com)
2. Click "Create New Project"
3. Name it (e.g., "MyApp")
4. Note your project ID

### Add your app

1. Go to Project Settings > Apps > Add App
2. Select platform (iOS/Android)
3. Enter your Bundle ID (iOS) or Package Name (Android)

### Configure App Store Connect (iOS)

1. In App Store Connect, go to Users and Access > Integrations > In-App Purchase
2. Click "Generate In-App Purchase Key"
3. Download the `.p8` file
4. Note the Key ID and Issuer ID
5. In RevenueCat, enter these credentials to connect

### Get your shared secret

1. In App Store Connect, go to your app > App Information
2. Scroll to "App-Specific Shared Secret"
3. Generate if needed
4. Copy to RevenueCat app settings

---

## 3. App Store Connect product setup

### Create a subscription group

1. Go to App Store Connect > Your App > Subscriptions
2. Click "+" to create a Subscription Group (e.g., "Premium")

### Create products

Add subscription products with this naming convention:

```
{app_prefix}_{duration}_{price_cents}

Examples:
- myapp_monthly_999    ($9.99/month)
- myapp_annual_4999    ($49.99/year)
```

For each product:
- Set the duration
- Set the price
- Add localized descriptions
- Configure free trial (optional)

---

## 4. RevenueCat entitlements and offerings

### Create an entitlement

1. Go to Project > Entitlements
2. Click "New"
3. Name it `premium` (or your preference)
4. This is what you check in code to gate features

### Create an offering

1. Go to Project > Offerings
2. Click "New"
3. Name it `default`
4. Mark as "Current Offering"

### Add packages to offering

1. In the offering, click "Add Package"
2. Create `$rc_monthly` -> link to your monthly product
3. Create `$rc_annual` -> link to your annual product

---

## 5. Code integration

### Copy shared files

Copy the entire `shared/revenuecat/` folder to your app:

```
your-app/
  src/
    revenuecat/
      types.ts
      config.ts
      utils.ts
      RevenueCatProvider.tsx
      useSubscription.ts
      usePurchase.ts
      PaywallComponent.tsx
```

### Configure your app

Edit `config.ts` with your app's details:

```typescript
// In config.ts, update APP_CONFIGS
export const APP_CONFIGS: Record<string, AppConfig> = {
  myapp: {
    appId: 'myapp',
    iosApiKey: process.env.REVENUECAT_IOS_KEY || 'appl_YOUR_KEY_HERE',
    androidApiKey: process.env.REVENUECAT_ANDROID_KEY,
    entitlementId: 'premium',
    products: {
      monthly: 'myapp_monthly_999',
      annual: 'myapp_annual_4999',
    },
  },
};
```

### Wrap your app with the provider

```tsx
// App.tsx
import React from 'react';
import { RevenueCatProvider, getAppConfig } from './revenuecat';
import { MainApp } from './MainApp';

export default function App() {
  return (
    <RevenueCatProvider
      config={getAppConfig('myapp')}
      onInitialized={() => console.log('RevenueCat ready')}
      onError={(error) => console.error('RevenueCat error:', error)}
    >
      <MainApp />
    </RevenueCatProvider>
  );
}
```

### Check subscription status

```tsx
import { useSubscription } from './revenuecat';

function MyScreen() {
  const { isSubscribed, isInTrial, isLoading } = useSubscription();

  if (isLoading) {
    return <ActivityIndicator />;
  }

  if (!isSubscribed) {
    return <UpgradePrompt />;
  }

  if (isInTrial) {
    return (
      <View>
        <TrialBanner />
        <PremiumContent />
      </View>
    );
  }

  return <PremiumContent />;
}
```

### Simple premium gate

```tsx
import { usePremiumStatus } from './revenuecat';

function PremiumFeature() {
  const isPremium = usePremiumStatus();

  if (!isPremium) {
    return <LockedFeature />;
  }

  return <FeatureContent />;
}
```

### Show the paywall

```tsx
import { useState } from 'react';
import { Modal } from 'react-native';
import { Paywall } from './revenuecat';

function MyComponent() {
  const [showPaywall, setShowPaywall] = useState(false);

  return (
    <>
      <Button title="Upgrade" onPress={() => setShowPaywall(true)} />

      <Modal visible={showPaywall} animationType="slide">
        <Paywall
          onPurchaseComplete={() => {
            setShowPaywall(false);
            // User now has premium access
          }}
          onClose={() => setShowPaywall(false)}
          title="Unlock Premium"
          subtitle="Get full access to all features"
          features={[
            'Unlimited usage',
            'All premium features',
            'No ads',
            'Priority support',
          ]}
        />
      </Modal>
    </>
  );
}
```

### Custom purchase flow

```tsx
import { usePurchase } from './revenuecat';

function CustomPaywall() {
  const {
    packages,
    purchasePackage,
    restorePurchases,
    isPurchasing,
    isRestoring,
  } = usePurchase();

  const handlePurchase = async (pkg) => {
    const result = await purchasePackage(pkg.package);

    if (result.success) {
      Alert.alert('Success', 'Thank you for subscribing!');
      navigation.goBack();
    } else if (!result.userCancelled) {
      Alert.alert('Error', result.error);
    }
  };

  return (
    <View>
      {packages.map((pkg) => (
        <TouchableOpacity
          key={pkg.identifier}
          onPress={() => handlePurchase(pkg)}
          disabled={isPurchasing}
        >
          <Text>{pkg.title}</Text>
          <Text>{pkg.priceString}{pkg.durationLabel}</Text>
          {pkg.savingsPercent && (
            <Text>Save {pkg.savingsPercent}%</Text>
          )}
          {pkg.trial && (
            <Text>{pkg.trial.displayString}</Text>
          )}
        </TouchableOpacity>
      ))}

      <Button
        title="Restore Purchases"
        onPress={restorePurchases}
        disabled={isRestoring}
      />
    </View>
  );
}
```

### User identification (for cross-device sync)

```tsx
import { RevenueCatProvider, getAppConfig } from './revenuecat';
import { useAuth } from './auth'; // Your auth system

function App() {
  const { user } = useAuth();

  return (
    <RevenueCatProvider
      config={getAppConfig('myapp')}
      userId={user?.id} // Pass user ID when available
    >
      <MainApp />
    </RevenueCatProvider>
  );
}
```

### Handle logout

```tsx
import { logoutRevenueCat } from './revenuecat';

async function handleLogout() {
  await logoutRevenueCat();
  // Continue with your app's logout flow
}
```

---

## 6. Testing

### Create sandbox tester

1. In App Store Connect, go to Users and Access > Sandbox > Testers
2. Click "+" to add a tester
3. Enter a new email (not your Apple ID)
4. Set a password

### Configure device for sandbox

1. On your test device, go to Settings > App Store
2. Scroll to bottom, tap "Sandbox Account"
3. Sign in with sandbox credentials

### Test purchase flow

1. Run your app in development
2. Trigger the paywall
3. Complete purchase with sandbox account
4. Verify entitlement is granted

### Test restore

1. Delete and reinstall app
2. Trigger restore purchases
3. Verify access is restored

### Sandbox timing

Subscriptions renew faster in sandbox:

| Real Duration | Sandbox Duration |
|---------------|------------------|
| 1 week        | 3 minutes        |
| 1 month       | 5 minutes        |
| 1 year        | 1 hour           |

### RevenueCat debugging

In development, you can:

1. Go to RevenueCat dashboard > Customers
2. Find your test user
3. View their subscription status
4. Manually grant/revoke entitlements for testing

---

## 7. Environment variables

Store API keys in environment variables. Never commit them to git.

Create `.env` file:

```bash
REVENUECAT_IOS_KEY=appl_your_actual_key
REVENUECAT_ANDROID_KEY=goog_your_actual_key
```

Add to `.gitignore`:

```
.env
.env.*
```

### React Native dotenv setup

```bash
npm install react-native-dotenv
```

Add to `babel.config.js`:

```javascript
module.exports = {
  presets: ['module:@react-native/babel-preset'],
  plugins: [
    ['module:react-native-dotenv', {
      moduleName: '@env',
      path: '.env',
    }],
  ],
};
```

---

## 8. Production checklist

Before going live:

- [ ] API keys are in environment variables (not hardcoded)
- [ ] Products are created and approved in App Store Connect
- [ ] Entitlements are configured in RevenueCat
- [ ] Offerings are set up with correct packages
- [ ] App Store Connect shared secret is configured
- [ ] Tested purchase flow with sandbox account
- [ ] Tested restore purchases
- [ ] Tested subscription expiration
- [ ] Debug logging disabled in production
- [ ] Paywall UI reviewed and approved
- [ ] Terms of Service and Privacy Policy linked
- [ ] FTC compliance (clear pricing, easy cancellation info)

---

## 9. Common issues

### Purchases not loading

- Check API key is correct
- Verify bundle ID matches App Store Connect
- Ensure products are "Ready to Submit" in App Store Connect

### Purchase fails immediately

- Check sandbox tester is signed in on device
- Try signing out and back in to sandbox account
- Clear App Store cache (Settings > App Store > sign out/in)

### Entitlement not granted after purchase

- Verify entitlement name matches exactly
- Check product is linked to entitlement in RevenueCat
- Check shared secret is configured

### Restore not working

- Ensure same sandbox account used for original purchase
- Verify entitlement configuration in RevenueCat
- Check logs for specific error messages

---

## 10. Analytics and monitoring

### RevenueCat dashboard

Monitor these metrics:

- MRR (Monthly Recurring Revenue)
- Active subscriptions
- Trial conversion rate
- Churn rate
- Revenue by product

### Set up alerts

In RevenueCat > Project Settings > Alerts:

- Churn spike alert
- Revenue drop alert
- Billing issues alert

### Track custom events

```typescript
import { ANALYTICS_EVENTS } from './revenuecat/config';

// Track paywall view
analytics.track(ANALYTICS_EVENTS.PAYWALL_VIEWED, {
  source: 'settings_screen',
});

// Track purchase completion
analytics.track(ANALYTICS_EVENTS.PURCHASE_COMPLETED, {
  product_id: 'myapp_annual_4999',
  price: 49.99,
});
```

---

## Quick reference

### File structure

```
revenuecat/
  types.ts          - TypeScript types
  config.ts         - API keys, product IDs, feature flags
  utils.ts          - Helper functions
  RevenueCatProvider.tsx - Context provider
  useSubscription.ts     - Subscription status hook
  usePurchase.ts         - Purchase flow hook
  PaywallComponent.tsx   - Ready-to-use paywall UI
```

### Main exports

```typescript
// Provider
import { RevenueCatProvider, getAppConfig } from './revenuecat';

// Hooks
import {
  useSubscription,
  usePremiumStatus,
  useTrialStatus,
  usePurchase,
  useRestorePurchases,
} from './revenuecat';

// Components
import { Paywall } from './revenuecat';

// Utilities
import {
  formatPrice,
  formatExpirationDate,
  logoutRevenueCat,
  setUserEmail,
} from './revenuecat';
```

---

## Support

- RevenueCat docs: https://docs.revenuecat.com
- RevenueCat community: https://community.revenuecat.com
- GitHub issues: https://github.com/RevenueCat/react-native-purchases/issues
