import { Platform } from 'react-native';
import Purchases, { CustomerInfo, PurchasesOffering } from 'react-native-purchases';
import {
  REVENUECAT_API_KEY_IOS,
  REVENUECAT_API_KEY_ANDROID,
  ENTITLEMENT_ID,
} from '../utils/constants';

export interface SubscriptionServiceResult {
  success: boolean;
  error?: string;
}

export interface OfferingsResult {
  offerings: PurchasesOffering | null;
  error?: string;
}

let isConfigured = false;

/**
 * Initialize RevenueCat SDK
 */
export async function initializeSubscriptions(): Promise<void> {
  if (isConfigured) return;

  const apiKey =
    Platform.OS === 'ios' ? REVENUECAT_API_KEY_IOS : REVENUECAT_API_KEY_ANDROID;

  // Skip if API key not set
  if (apiKey.startsWith('YOUR_')) {
    console.warn('RevenueCat API key not configured');
    return;
  }

  await Purchases.configure({ apiKey });
  isConfigured = true;
}

/**
 * Get available subscription offerings
 */
export async function getOfferings(): Promise<OfferingsResult> {
  try {
    if (!isConfigured) {
      await initializeSubscriptions();
    }

    const offerings = await Purchases.getOfferings();
    return { offerings: offerings.current };
  } catch (error) {
    return {
      offerings: null,
      error: error instanceof Error ? error.message : 'Failed to get offerings',
    };
  }
}

/**
 * Purchase a subscription package
 */
export async function purchaseSubscription(
  packageToPurchase: any
): Promise<SubscriptionServiceResult> {
  try {
    if (!isConfigured) {
      await initializeSubscriptions();
    }

    await Purchases.purchasePackage(packageToPurchase);
    return { success: true };
  } catch (error: any) {
    // Check if user cancelled
    if (error.userCancelled) {
      return { success: false, error: 'Purchase cancelled' };
    }
    return {
      success: false,
      error: error.message || 'Purchase failed',
    };
  }
}

/**
 * Check if user has active subscription
 */
export async function checkSubscriptionStatus(): Promise<{
  isSubscribed: boolean;
  expirationDate: string | null;
}> {
  try {
    if (!isConfigured) {
      await initializeSubscriptions();
    }

    const customerInfo = await Purchases.getCustomerInfo();
    const entitlement = customerInfo.entitlements.active[ENTITLEMENT_ID];

    return {
      isSubscribed: !!entitlement,
      expirationDate: entitlement?.expirationDate || null,
    };
  } catch {
    return { isSubscribed: false, expirationDate: null };
  }
}

/**
 * Restore previous purchases
 */
export async function restorePurchases(): Promise<SubscriptionServiceResult> {
  try {
    if (!isConfigured) {
      await initializeSubscriptions();
    }

    const customerInfo = await Purchases.restorePurchases();
    const hasEntitlement = !!customerInfo.entitlements.active[ENTITLEMENT_ID];

    if (hasEntitlement) {
      return { success: true };
    } else {
      return { success: false, error: 'No active subscription found' };
    }
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Restore failed',
    };
  }
}

/**
 * Set user ID for attribution
 */
export async function setUserId(userId: string): Promise<void> {
  try {
    if (!isConfigured) {
      await initializeSubscriptions();
    }
    await Purchases.logIn(userId);
  } catch {
    // Ignore errors
  }
}

/**
 * Get customer info (for debugging)
 */
export async function getCustomerInfo(): Promise<CustomerInfo | null> {
  try {
    if (!isConfigured) {
      await initializeSubscriptions();
    }
    return await Purchases.getCustomerInfo();
  } catch {
    return null;
  }
}
