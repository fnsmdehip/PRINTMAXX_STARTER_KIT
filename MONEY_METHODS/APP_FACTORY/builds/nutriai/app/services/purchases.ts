/**
 * In-app purchases service — Stripe Payment Links integration.
 *
 * Opens Stripe Payment Links in the system browser via Linking.openURL().
 * Stores premium status in AsyncStorage after user confirms payment.
 * No RevenueCat dependency required.
 */

import { Linking, AppState, Alert, AppStateStatus } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const STRIPE_ANNUAL_LINK = 'https://buy.stripe.com/7sY6oI9XWaZTdxTdj93F60x';
const STRIPE_MONTHLY_LINK = 'https://buy.stripe.com/cNi14oc647NH8dzfrh3F60y';

const STORAGE_KEY = '@nutrisnap_premium';
const ENTITLEMENT_ID = 'premium';

export interface OfferingDetails {
  monthly: unknown | null;
  yearly: unknown | null;
  lifetime: unknown | null;
}

export interface CustomerInfoResult {
  entitlements: {
    active: Record<string, { expirationDate: string | null } | undefined>;
  };
}

/**
 * Initialize purchases. No-op for Stripe Payment Links mode.
 */
export async function initPurchases(): Promise<void> {
  console.log('[Purchases] Stripe Payment Links mode active — no SDK init needed');
}

/**
 * Return available offerings as Stripe Payment Link packages.
 */
export async function getOfferings(): Promise<any | null> {
  try {
    const annual = {
      product: { priceString: '$29.99/year' },
      __stripeUrl: STRIPE_ANNUAL_LINK,
    };
    const monthly = {
      product: { priceString: '$4.99/month' },
      __stripeUrl: STRIPE_MONTHLY_LINK,
    };
    return {
      annual,
      monthly,
      availablePackages: [annual, monthly],
    };
  } catch (error) {
    console.warn('[Purchases] Failed to build offerings:', error);
    return null;
  }
}

/**
 * Open a Stripe Payment Link in the browser, wait for user to return,
 * then confirm payment via Alert dialog.
 */
export async function purchasePackage(pkg: any): Promise<any> {
  const url: string | undefined = pkg?.__stripeUrl;
  if (!url) {
    throw new Error('[Purchases] Package missing __stripeUrl — cannot open payment link');
  }

  await Linking.openURL(url);

  // Wait for the app to come back to the foreground
  await waitForForeground();

  // Ask the user to confirm they completed payment
  const confirmed = await new Promise<boolean>((resolve) => {
    Alert.alert(
      'Confirm Purchase',
      'Did you complete your payment?',
      [
        { text: 'No', style: 'cancel', onPress: () => resolve(false) },
        { text: 'Yes I paid', style: 'default', onPress: () => resolve(true) },
      ],
      { cancelable: false },
    );
  });

  if (!confirmed) {
    throw new PurchaseCancelledError();
  }

  // Store premium status
  await AsyncStorage.setItem(STORAGE_KEY, 'true');

  return {
    entitlements: {
      active: {
        [ENTITLEMENT_ID]: {
          expirationDate: null,
        },
      },
    },
  };
}

/**
 * Restore purchases by checking AsyncStorage.
 */
export async function restorePurchases(): Promise<boolean> {
  try {
    const value = await AsyncStorage.getItem(STORAGE_KEY);
    return value === 'true';
  } catch (error) {
    console.warn('[Purchases] Restore failed:', error);
    return false;
  }
}

/**
 * Check if the user has an active premium entitlement.
 */
export async function checkEntitlements(): Promise<{
  isPremium: boolean;
  expirationDate: string | null;
}> {
  try {
    const value = await AsyncStorage.getItem(STORAGE_KEY);
    return {
      isPremium: value === 'true',
      expirationDate: null,
    };
  } catch (error) {
    console.warn('[Purchases] Entitlement check failed:', error);
    return { isPremium: false, expirationDate: null };
  }
}

/**
 * Custom error for user-cancelled purchases.
 */
export class PurchaseCancelledError extends Error {
  constructor() {
    super('Purchase was cancelled by the user');
    this.name = 'PurchaseCancelledError';
  }
}

/**
 * Returns a promise that resolves when the app transitions from
 * background/inactive back to the active foreground state.
 */
function waitForForeground(): Promise<void> {
  return new Promise<void>((resolve) => {
    const currentState = AppState.currentState;

    // If user hasn't left yet, wait for them to leave then come back
    let wentBackground = false;

    const subscription = AppState.addEventListener(
      'change',
      (nextState: AppStateStatus) => {
        if (nextState === 'background' || nextState === 'inactive') {
          wentBackground = true;
        }
        if (wentBackground && nextState === 'active') {
          subscription.remove();
          resolve();
        }
      },
    );

    // Safety timeout: if user never leaves (e.g. in-app browser),
    // resolve after 3 seconds so the confirm dialog still shows.
    setTimeout(() => {
      subscription.remove();
      resolve();
    }, 3000);
  });
}
