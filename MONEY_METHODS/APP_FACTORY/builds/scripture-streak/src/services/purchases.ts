/**
 * In-app purchases service — Stripe Payment Links integration.
 *
 * Free: daily verse, basic streak, KJV only
 * Premium: all translations, reading plans, advanced stats, streak freeze
 *
 * Flow: open Stripe Payment Link in browser -> user completes purchase ->
 * returns to app -> confirm via Alert -> store premium status in AsyncStorage.
 */

import { Linking, AppState, Alert, AppStateStatus } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const STRIPE_ANNUAL_URL = 'https://buy.stripe.com/00weVe7POd81dxT2Ev3F60z';
const STRIPE_MONTHLY_URL = 'https://buy.stripe.com/aFa28s3zyfg9alH4MD3F60A';
const STRIPE_CUSTOMER_PORTAL = 'https://billing.stripe.com/p/login/printmaxx';

const STORAGE_KEY = '@scripture_streak_premium';

/**
 * Initialize purchases service. No-op for Stripe Payment Links
 * (no SDK to configure), but kept for API compatibility.
 */
export async function initPurchases(): Promise<void> {
  // Stripe Payment Links require no client-side SDK initialization.
  // Premium status is persisted in AsyncStorage.
}

/**
 * Fetch available offerings. Returns a structure matching the shape
 * consumers expect: .annual, .monthly, .availablePackages.
 */
export async function getOfferings(): Promise<any | null> {
  try {
    const annual = {
      __stripeUrl: STRIPE_ANNUAL_URL,
      identifier: 'annual',
      packageType: 'ANNUAL',
      product: {
        title: 'Scripture Streak Premium (Annual)',
        description: 'Full access to all premium features',
        priceString: '$19.99/year',
        price: 19.99,
      },
    };

    const monthly = {
      __stripeUrl: STRIPE_MONTHLY_URL,
      identifier: 'monthly',
      packageType: 'MONTHLY',
      product: {
        title: 'Scripture Streak Premium (Monthly)',
        description: 'Full access to all premium features',
        priceString: '$2.99/month',
        price: 2.99,
      },
    };

    return {
      annual,
      monthly,
      availablePackages: [annual, monthly],
    };
  } catch (error) {
    console.warn('[Purchases] Failed to get offerings:', error);
    return null;
  }
}

/**
 * Purchase a package by opening its Stripe Payment Link in the browser.
 * Waits for the user to return to the app, then confirms via Alert.
 * On confirmation, stores premium status in AsyncStorage.
 */
export async function purchasePackage(pkg: any): Promise<any> {
  const stripeUrl: string | undefined = pkg?.__stripeUrl;
  if (!stripeUrl) {
    throw new Error('Invalid package: missing Stripe URL');
  }

  // Open the Stripe checkout in the browser
  const supported = await Linking.canOpenURL(stripeUrl);
  if (!supported) {
    throw new Error('Cannot open Stripe checkout URL');
  }

  await Linking.openURL(stripeUrl);

  // Wait for the app to come back to the foreground
  const didReturn = await new Promise<boolean>((resolve) => {
    const handleAppState = (nextState: AppStateStatus) => {
      if (nextState === 'active') {
        subscription.remove();
        resolve(true);
      }
    };
    const subscription = AppState.addEventListener('change', handleAppState);

    // Safety timeout after 10 minutes — user may have abandoned
    setTimeout(() => {
      subscription.remove();
      resolve(false);
    }, 10 * 60 * 1000);
  });

  if (!didReturn) {
    throw new Error('Purchase flow timed out');
  }

  // Confirm purchase with user
  const confirmed = await new Promise<boolean>((resolve) => {
    Alert.alert(
      'Complete Purchase',
      'Did you complete your purchase on the Stripe checkout page?',
      [
        { text: 'No', style: 'cancel', onPress: () => resolve(false) },
        { text: 'Yes, I purchased', style: 'default', onPress: () => resolve(true) },
      ],
      { cancelable: false },
    );
  });

  if (!confirmed) {
    throw new Error('Purchase not confirmed by user');
  }

  // Store premium status
  await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify({
    isPremium: true,
    purchasedAt: new Date().toISOString(),
    plan: pkg.identifier || 'unknown',
  }));

  return {
    entitlements: {
      active: {
        premium: {
          expirationDate: null,
          isActive: true,
          identifier: 'premium',
        },
      },
    },
  };
}

/**
 * Restore previous purchases. For Stripe Payment Links, this checks
 * AsyncStorage for a stored premium flag. Returns true if premium.
 */
export async function restorePurchases(): Promise<boolean> {
  try {
    const stored = await AsyncStorage.getItem(STORAGE_KEY);
    if (stored) {
      const parsed = JSON.parse(stored);
      return parsed.isPremium === true;
    }
    return false;
  } catch (error) {
    console.warn('[Purchases] Restore failed:', error);
    return false;
  }
}

/**
 * Check if the user currently has an active premium entitlement.
 * Reads from AsyncStorage.
 */
export async function checkEntitlements(): Promise<boolean> {
  try {
    const stored = await AsyncStorage.getItem(STORAGE_KEY);
    if (stored) {
      const parsed = JSON.parse(stored);
      return parsed.isPremium === true;
    }
    return false;
  } catch (error) {
    console.warn('[Purchases] Entitlement check failed:', error);
    return false;
  }
}

/**
 * Full subscription check. For Stripe Payment Links, this reads
 * AsyncStorage. Returns the premium status.
 */
export async function checkSubscription(): Promise<boolean> {
  try {
    const stored = await AsyncStorage.getItem(STORAGE_KEY);
    if (stored) {
      const parsed = JSON.parse(stored);
      return parsed.isPremium === true;
    }
    return false;
  } catch (error) {
    console.warn('[Purchases] Subscription check failed:', error);
    return false;
  }
}

/**
 * Returns the Stripe customer portal URL for managing subscriptions.
 */
export function getManageSubscriptionsUrl(): string {
  return STRIPE_CUSTOMER_PORTAL;
}
