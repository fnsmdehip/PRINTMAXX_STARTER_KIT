// RevenueCat Integration for DevotionFlow
// Documentation: https://docs.revenuecat.com/docs/reactnative

import Purchases, {
  PurchasesPackage,
  CustomerInfo,
  LOG_LEVEL,
} from 'react-native-purchases';
import { Platform } from 'react-native';

// API Keys - Store in environment variables in production
const API_KEYS = {
  ios: 'appl_YOUR_IOS_KEY_HERE',
  android: 'goog_YOUR_ANDROID_KEY_HERE',
};

// Product Identifiers (must match App Store Connect / Google Play Console)
export const PRODUCT_IDS = {
  weekly: 'devotionflow_weekly_499',
  annual: 'devotionflow_annual_3999',
};

// Entitlement ID (set in RevenueCat dashboard)
export const ENTITLEMENT_ID = 'premium';

/**
 * Initialize RevenueCat SDK
 * Call this in app startup (e.g., in _layout.tsx useEffect)
 */
export async function initRevenueCat(): Promise<void> {
  try {
    // Enable debug logs in development
    if (__DEV__) {
      Purchases.setLogLevel(LOG_LEVEL.DEBUG);
    }

    // Configure with API key
    const apiKey = Platform.OS === 'ios' ? API_KEYS.ios : API_KEYS.android;
    await Purchases.configure({ apiKey });

    console.log('RevenueCat initialized successfully');
  } catch (error) {
    console.error('Failed to initialize RevenueCat:', error);
    throw error;
  }
}

/**
 * Get available subscription packages
 */
export async function getOfferings(): Promise<PurchasesPackage[] | null> {
  try {
    const offerings = await Purchases.getOfferings();

    if (offerings.current?.availablePackages) {
      return offerings.current.availablePackages;
    }

    return null;
  } catch (error) {
    console.error('Error fetching offerings:', error);
    return null;
  }
}

/**
 * Purchase a subscription package
 */
export async function purchasePackage(
  pkg: PurchasesPackage
): Promise<CustomerInfo | null> {
  try {
    const { customerInfo } = await Purchases.purchasePackage(pkg);
    return customerInfo;
  } catch (error: any) {
    if (error.userCancelled) {
      console.log('User cancelled purchase');
      return null;
    }
    console.error('Purchase error:', error);
    throw error;
  }
}

/**
 * Restore previous purchases
 */
export async function restorePurchases(): Promise<CustomerInfo | null> {
  try {
    const customerInfo = await Purchases.restorePurchases();
    return customerInfo;
  } catch (error) {
    console.error('Error restoring purchases:', error);
    throw error;
  }
}

/**
 * Check if user has active premium subscription
 */
export async function checkSubscriptionStatus(): Promise<boolean> {
  try {
    const customerInfo = await Purchases.getCustomerInfo();
    return !!customerInfo.entitlements.active[ENTITLEMENT_ID];
  } catch (error) {
    console.error('Error checking subscription:', error);
    return false;
  }
}

/**
 * Get customer info
 */
export async function getCustomerInfo(): Promise<CustomerInfo | null> {
  try {
    return await Purchases.getCustomerInfo();
  } catch (error) {
    console.error('Error getting customer info:', error);
    return null;
  }
}

/**
 * Identify user (for cross-device sync)
 * Call after user authenticates if using auth
 */
export async function identifyUser(userId: string): Promise<void> {
  try {
    await Purchases.logIn(userId);
  } catch (error) {
    console.error('Error identifying user:', error);
  }
}

/**
 * Listen for subscription changes
 * Note: RevenueCat SDK v5+ manages listeners internally
 */
export function addSubscriptionListener(
  callback: (customerInfo: CustomerInfo) => void
): () => void {
  // RevenueCat SDK v5+ addCustomerInfoUpdateListener returns void
  // and manages listeners internally
  Purchases.addCustomerInfoUpdateListener(callback);
  // Return no-op cleanup function since SDK handles removal
  return () => {};
}
