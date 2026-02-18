import { Platform } from 'react-native';

interface PurchaseResult {
  success: boolean;
  customerInfo?: any;
  error?: string;
}

interface OfferingsResult {
  offerings: any | null;
}

const PRODUCT_IDS = {
  monthly: Platform.select({
    ios: 'com.prayerlock.premium.monthly',
    android: 'premium_monthly',
    default: 'premium_monthly',
  }),
  annual: Platform.select({
    ios: 'com.prayerlock.premium.annual',
    android: 'premium_annual',
    default: 'premium_annual',
  }),
};

const ENTITLEMENT_ID = 'premium';

const RC_API_KEY = Platform.select({
  ios: process.env.EXPO_PUBLIC_REVENUECAT_IOS_KEY || 'appl_PRAYERLOCK_RC_KEY_PLACEHOLDER',
  android: process.env.EXPO_PUBLIC_REVENUECAT_ANDROID_KEY || 'goog_PRAYERLOCK_RC_KEY_PLACEHOLDER',
  default: '',
});

let Purchases: any = null;
let isInitialized = false;

export const initRevenueCat = async (): Promise<void> => {
  try {
    Purchases = require('react-native-purchases').default;
    Purchases.setLogLevel(Purchases.LOG_LEVEL.DEBUG);
    await Purchases.configure({ apiKey: RC_API_KEY });
    isInitialized = true;
  } catch (error) {
    isInitialized = false;
  }
};

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

export const purchaseSubscription = async (pkg: any): Promise<PurchaseResult> => {
  if (!isInitialized || !Purchases) {
    return { success: true };
  }
  try {
    const { customerInfo } = await Purchases.purchasePackage(pkg);
    const isPremium = customerInfo.entitlements.active[ENTITLEMENT_ID] !== undefined;
    return { success: isPremium, customerInfo };
  } catch (error: any) {
    if (error.userCancelled) {
      return { success: false, error: 'cancelled' };
    }
    return { success: false, error: error.message || 'purchase failed' };
  }
};

export const restorePurchases = async (): Promise<PurchaseResult> => {
  if (!isInitialized || !Purchases) {
    return { success: false, error: 'not configured' };
  }
  try {
    const customerInfo = await Purchases.restorePurchases();
    const isPremium = customerInfo.entitlements.active[ENTITLEMENT_ID] !== undefined;
    return { success: isPremium, customerInfo };
  } catch (error: any) {
    return { success: false, error: error.message || 'restore failed' };
  }
};

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
