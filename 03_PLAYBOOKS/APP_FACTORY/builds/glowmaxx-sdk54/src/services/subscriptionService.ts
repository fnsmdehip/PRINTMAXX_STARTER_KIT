import Purchases, { PurchasesPackage, CustomerInfo } from 'react-native-purchases';
import { Platform } from 'react-native';
import {
  REVENUECAT_API_KEY_IOS,
  REVENUECAT_API_KEY_ANDROID,
  ENTITLEMENT_ID,
} from '../utils/constants';

/**
 * Initialize RevenueCat SDK
 */
export async function initializeSubscriptions(): Promise<void> {
  const apiKey = Platform.OS === 'ios' ? REVENUECAT_API_KEY_IOS : REVENUECAT_API_KEY_ANDROID;

  try {
    await Purchases.configure({ apiKey });
    console.log('RevenueCat initialized');
  } catch (error) {
    console.error('Failed to initialize RevenueCat:', error);
  }
}

/**
 * Check if user has premium entitlement
 */
export async function checkPremiumStatus(): Promise<boolean> {
  try {
    const customerInfo = await Purchases.getCustomerInfo();
    return customerInfo.entitlements.active[ENTITLEMENT_ID] !== undefined;
  } catch (error) {
    console.error('Failed to check premium status:', error);
    return false;
  }
}

/**
 * Get available subscription packages
 */
export async function getOfferings(): Promise<PurchasesPackage[]> {
  try {
    const offerings = await Purchases.getOfferings();
    if (offerings.current && offerings.current.availablePackages.length > 0) {
      return offerings.current.availablePackages;
    }
    return [];
  } catch (error) {
    console.error('Failed to get offerings:', error);
    return [];
  }
}

/**
 * Purchase a subscription package
 */
export async function purchasePackage(
  packageToPurchase: PurchasesPackage
): Promise<{ success: boolean; customerInfo?: CustomerInfo; error?: string }> {
  try {
    const { customerInfo } = await Purchases.purchasePackage(packageToPurchase);
    const isPremium = customerInfo.entitlements.active[ENTITLEMENT_ID] !== undefined;

    return {
      success: isPremium,
      customerInfo,
    };
  } catch (error: any) {
    // Check if user cancelled
    if (error.userCancelled) {
      return { success: false, error: 'Purchase cancelled' };
    }
    console.error('Purchase failed:', error);
    return { success: false, error: error.message || 'Purchase failed' };
  }
}

/**
 * Restore previous purchases
 */
export async function restorePurchases(): Promise<{
  success: boolean;
  customerInfo?: CustomerInfo;
  error?: string;
}> {
  try {
    const customerInfo = await Purchases.restorePurchases();
    const isPremium = customerInfo.entitlements.active[ENTITLEMENT_ID] !== undefined;

    return {
      success: isPremium,
      customerInfo,
    };
  } catch (error: any) {
    console.error('Restore failed:', error);
    return { success: false, error: error.message || 'Restore failed' };
  }
}

/**
 * Get customer info
 */
export async function getCustomerInfo(): Promise<CustomerInfo | null> {
  try {
    return await Purchases.getCustomerInfo();
  } catch (error) {
    console.error('Failed to get customer info:', error);
    return null;
  }
}

/**
 * Log in user (for user identification)
 */
export async function logInUser(userId: string): Promise<void> {
  try {
    await Purchases.logIn(userId);
  } catch (error) {
    console.error('Failed to log in user:', error);
  }
}

/**
 * Log out user
 */
export async function logOutUser(): Promise<void> {
  try {
    await Purchases.logOut();
  } catch (error) {
    console.error('Failed to log out user:', error);
  }
}
