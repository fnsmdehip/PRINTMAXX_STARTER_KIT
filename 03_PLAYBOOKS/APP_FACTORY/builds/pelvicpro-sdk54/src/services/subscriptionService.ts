/**
 * Subscription Service Template - RevenueCat Integration
 *
 * Copy this to: src/services/subscriptionService.ts
 * Then update API_KEY and ENTITLEMENT_ID for your app.
 *
 * Dependencies: react-native-purchases
 * Install: npx expo install react-native-purchases
 */

import Purchases, {
  PurchasesOffering,
  CustomerInfo,
  PurchasesPackage,
} from 'react-native-purchases';
import { Platform } from 'react-native';

// UPDATE THESE FOR YOUR APP
const API_KEY = Platform.OS === 'ios'
  ? 'YOUR_REVENUECAT_IOS_API_KEY'
  : 'YOUR_REVENUECAT_ANDROID_API_KEY';

const ENTITLEMENT_ID = 'premium';

export interface SubscriptionStatus {
  isSubscribed: boolean;
  isTrialActive: boolean;
  expirationDate: string | null;
  productIdentifier: string | null;
}

class SubscriptionService {
  private initialized = false;

  async initialize(): Promise<void> {
    if (this.initialized) return;

    try {
      await Purchases.configure({ apiKey: API_KEY });
      this.initialized = true;
    } catch (error) {
      console.error('RevenueCat initialization failed:', error);
    }
  }

  async getOfferings(): Promise<PurchasesOffering | null> {
    await this.initialize();
    try {
      const offerings = await Purchases.getOfferings();
      return offerings.current;
    } catch (error) {
      console.error('Failed to fetch offerings:', error);
      return null;
    }
  }

  async purchasePackage(pkg: PurchasesPackage): Promise<boolean> {
    try {
      const { customerInfo } = await Purchases.purchasePackage(pkg);
      return this.checkEntitlement(customerInfo);
    } catch (error: any) {
      if (error.userCancelled) {
        return false;
      }
      console.error('Purchase failed:', error);
      throw error;
    }
  }

  async restorePurchases(): Promise<boolean> {
    try {
      const customerInfo = await Purchases.restorePurchases();
      return this.checkEntitlement(customerInfo);
    } catch (error) {
      console.error('Restore failed:', error);
      return false;
    }
  }

  async getSubscriptionStatus(): Promise<SubscriptionStatus> {
    await this.initialize();
    try {
      const customerInfo = await Purchases.getCustomerInfo();
      const isSubscribed = this.checkEntitlement(customerInfo);
      const entitlement = customerInfo.entitlements.active[ENTITLEMENT_ID];

      return {
        isSubscribed,
        isTrialActive: entitlement?.periodType === 'TRIAL',
        expirationDate: entitlement?.expirationDate || null,
        productIdentifier: entitlement?.productIdentifier || null,
      };
    } catch (error) {
      console.error('Failed to get subscription status:', error);
      return {
        isSubscribed: false,
        isTrialActive: false,
        expirationDate: null,
        productIdentifier: null,
      };
    }
  }

  private checkEntitlement(customerInfo: CustomerInfo): boolean {
    return ENTITLEMENT_ID in (customerInfo.entitlements.active || {});
  }
}

export const subscriptionService = new SubscriptionService();
export default subscriptionService;
