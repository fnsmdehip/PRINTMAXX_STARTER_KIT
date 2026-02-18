import { Platform } from 'react-native';

// RevenueCat types (inline to avoid import issues before package install)
interface PurchaseResult {
  success: boolean;
  customerInfo?: any;
  error?: string;
}

interface OfferingsResult {
  offerings: any | null;
}

// Product IDs per convention: {appname}_{frequency}_{pricecents}
const PRODUCT_IDS = {
  monthly: Platform.select({
    ios: 'com.biomaxx.premium.monthly',
    android: 'premium_monthly',
    default: 'premium_monthly',
  }),
  annual: Platform.select({
    ios: 'com.biomaxx.premium.annual',
    android: 'premium_annual',
    default: 'premium_annual',
  }),
};

const ENTITLEMENT_ID = 'premium';

// RevenueCat API key placeholder
// Replace with actual keys from RevenueCat dashboard
const RC_API_KEY = Platform.select({
  ios: process.env.EXPO_PUBLIC_REVENUECAT_IOS_KEY || 'appl_BIOMAXX_RC_KEY_PLACEHOLDER',
  android: process.env.EXPO_PUBLIC_REVENUECAT_ANDROID_KEY || 'goog_BIOMAXX_RC_KEY_PLACEHOLDER',
  default: '',
});

let Purchases: any = null;
let isInitialized = false;

/**
 * Initialize RevenueCat SDK.
 * Call once in root layout on app mount.
 * Gracefully handles missing SDK (demo mode).
 */
export const initRevenueCat = async (): Promise<void> => {
  try {
    Purchases = require('react-native-purchases').default;
    Purchases.setLogLevel(Purchases.LOG_LEVEL.DEBUG);

    await Purchases.configure({
      apiKey: RC_API_KEY,
    });

    isInitialized = true;
  } catch (error) {
    // RevenueCat not installed or not configured
    // App runs in demo mode - paywall still renders
    isInitialized = false;
  }
};

/**
 * Get available subscription offerings from RevenueCat.
 * Returns null in demo mode.
 */
export const getOfferings = async (): Promise<OfferingsResult> => {
  if (!isInitialized || !Purchases) {
    return { offerings: null };
  }

  try {
    const offerings = await Purchases.getOfferings();
    return { offerings: offerings.current };
  } catch (error) {
    return { offerings: null };
  }
};

/**
 * Purchase a subscription package.
 * In demo mode, returns simulated success.
 */
export const purchaseSubscription = async (
  pkg: any
): Promise<PurchaseResult> => {
  if (!isInitialized || !Purchases) {
    // Demo mode: simulate successful purchase
    return { success: true };
  }

  try {
    const { customerInfo } = await Purchases.purchasePackage(pkg);
    const isPremium =
      customerInfo.entitlements.active[ENTITLEMENT_ID] !== undefined;

    return {
      success: isPremium,
      customerInfo,
    };
  } catch (error: any) {
    if (error.userCancelled) {
      return { success: false, error: 'cancelled' };
    }
    return { success: false, error: error.message || 'purchase failed' };
  }
};

/**
 * Restore previous purchases.
 */
export const restorePurchases = async (): Promise<PurchaseResult> => {
  if (!isInitialized || !Purchases) {
    return { success: false, error: 'not configured' };
  }

  try {
    const customerInfo = await Purchases.restorePurchases();
    const isPremium =
      customerInfo.entitlements.active[ENTITLEMENT_ID] !== undefined;

    return {
      success: isPremium,
      customerInfo,
    };
  } catch (error: any) {
    return { success: false, error: error.message || 'restore failed' };
  }
};

/**
 * Check if user currently has premium access.
 */
export const checkPremiumStatus = async (): Promise<boolean> => {
  if (!isInitialized || !Purchases) {
    return false;
  }

  try {
    const customerInfo = await Purchases.getCustomerInfo();
    return customerInfo.entitlements.active[ENTITLEMENT_ID] !== undefined;
  } catch (error) {
    return false;
  }
};

export { PRODUCT_IDS, ENTITLEMENT_ID };
