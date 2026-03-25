/**
 * In-app purchases service -- Stripe Payment Links implementation.
 *
 * Free tier:  browse all 10 categories, download/read first 10 books,
 *             basic reader (night theme only), bookmarks, progress tracking
 * Premium:    all 156 books, highlights, notes, daily quotes,
 *             all reader themes (night/sepia/day), offline reading
 */

import { Linking, AppState, Alert, AppStateStatus } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const STRIPE_ANNUAL_URL =
  'https://buy.stripe.com/6oU5kE4DC5Fz1Pbdj93F60B';
const STRIPE_MONTHLY_URL =
  'https://buy.stripe.com/dRm4gA7PO8RLalH5QH3F60C';

const PREMIUM_CACHE_KEY = '@pocket_alexandria_premium';

/** Number of free books available without premium (book IDs 1-10). */
export const FREE_BOOK_LIMIT = 10;

// ---------------------------------------------------------------------------
// Initialisation
// ---------------------------------------------------------------------------

/**
 * Initialize purchases service. Call once at app startup (_layout.tsx).
 * With Stripe Payment Links there is no SDK to configure, so this is a no-op
 * that resolves immediately.
 */
export async function initPurchases(): Promise<void> {
  // No SDK to configure -- Stripe Payment Links are opened in the browser.
}

// ---------------------------------------------------------------------------
// Offerings
// ---------------------------------------------------------------------------

/**
 * Return the available purchase offerings.
 * Mimics the RevenueCat offering shape so callers don't need changes.
 */
export async function getOfferings(): Promise<any | null> {
  try {
    const annual = {
      identifier: 'annual',
      product: {
        title: 'Pocket Alexandria Premium (Annual)',
        description: 'Unlock every book for a full year',
        priceString: '$9.99',
        price: 9.99,
      },
      packageType: 'ANNUAL',
      __stripeUrl: STRIPE_ANNUAL_URL,
    };

    const monthly = {
      identifier: 'monthly',
      product: {
        title: 'Pocket Alexandria Premium (Monthly)',
        description: 'Unlock every book, billed monthly',
        priceString: '$1.99',
        price: 1.99,
      },
      packageType: 'MONTHLY',
      __stripeUrl: STRIPE_MONTHLY_URL,
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

// ---------------------------------------------------------------------------
// Purchase
// ---------------------------------------------------------------------------

/**
 * Open the Stripe Payment Link for the chosen package in the system browser,
 * wait for the user to return to the app, then confirm via Alert and persist
 * premium status in AsyncStorage.
 */
export async function purchasePackage(pkg: any): Promise<any> {
  const url: string | undefined = pkg?.__stripeUrl;
  if (!url) {
    throw new Error('[Purchases] Package is missing __stripeUrl');
  }

  // Open the Stripe checkout in the external browser
  await Linking.openURL(url);

  // Wait for the app to come back to the foreground
  await new Promise<void>((resolve) => {
    const handleChange = (nextState: AppStateStatus) => {
      if (nextState === 'active') {
        subscription.remove();
        resolve();
      }
    };
    const subscription = AppState.addEventListener('change', handleChange);
  });

  // Confirm with the user
  const confirmed = await new Promise<boolean>((resolve) => {
    Alert.alert(
      'Complete your purchase',
      'Did you finish the payment successfully?',
      [
        { text: 'No', style: 'cancel', onPress: () => resolve(false) },
        { text: 'Yes', style: 'default', onPress: () => resolve(true) },
      ],
      { cancelable: false },
    );
  });

  if (!confirmed) {
    throw new Error('Purchase cancelled by user');
  }

  // Persist premium status
  await AsyncStorage.setItem(PREMIUM_CACHE_KEY, 'true');

  return {
    entitlements: {
      active: {
        premium: {
          expirationDate: null,
        },
      },
    },
  };
}

// ---------------------------------------------------------------------------
// Restore
// ---------------------------------------------------------------------------

/**
 * Restore previous purchases.
 * With Stripe Payment Links there is no server-side entitlement lookup on
 * device, so we prompt the user and trust their confirmation.
 * Returns true when the user confirms they have an active subscription.
 */
export async function restorePurchases(): Promise<boolean> {
  try {
    const confirmed = await new Promise<boolean>((resolve) => {
      Alert.alert(
        'Restore purchases',
        'Do you have an active Pocket Alexandria subscription?',
        [
          { text: 'No', style: 'cancel', onPress: () => resolve(false) },
          { text: 'Yes', style: 'default', onPress: () => resolve(true) },
        ],
        { cancelable: false },
      );
    });

    await AsyncStorage.setItem(PREMIUM_CACHE_KEY, confirmed ? 'true' : 'false');
    return confirmed;
  } catch (error) {
    console.warn('[Purchases] Restore failed:', error);
    return false;
  }
}

// ---------------------------------------------------------------------------
// Entitlement checks
// ---------------------------------------------------------------------------

/**
 * Check current entitlements from AsyncStorage.
 */
export async function checkEntitlements(): Promise<boolean> {
  try {
    const cached = await AsyncStorage.getItem(PREMIUM_CACHE_KEY);
    return cached === 'true';
  } catch {
    return false;
  }
}

/**
 * Quick check from AsyncStorage (no network round-trip).
 * Use this in render paths where you need an instant answer.
 */
export async function isPremiumCached(): Promise<boolean> {
  try {
    const cached = await AsyncStorage.getItem(PREMIUM_CACHE_KEY);
    return cached === 'true';
  } catch {
    return false;
  }
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Returns true when a book (by numeric ID) is within the free tier.
 */
export function isBookFree(bookId: string): boolean {
  const num = parseInt(bookId, 10);
  return !isNaN(num) && num <= FREE_BOOK_LIMIT;
}
