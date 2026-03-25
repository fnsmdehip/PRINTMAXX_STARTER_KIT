/**
 * Stripe Payment Links integration for cnsnt app.
 *
 * Free tier: 5 consent records, no PDF export, no cloud backup
 * Pro tier: unlimited records, PDF export, cloud backup
 *   - Monthly: $4.99/mo
 *   - Annual: $29.99/yr
 *
 * Uses Linking.openURL to launch Stripe Payment Links in the browser.
 * After returning to the app, confirms upgrade via Alert and stores
 * entitlement in AsyncStorage.
 */

import { Alert, AppState, Linking } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { FREE_TIER_LIMIT } from '../constants/theme';
import type { Entitlement, PurchaseState } from '../types';

const STRIPE_PAYMENT_LINKS = {
  annual: 'https://buy.stripe.com/5kQcN60nm8RL9hDgvl3F60D',
  monthly: 'https://buy.stripe.com/5kQ14o6LK7NH51nend3F60E',
} as const;

const ENTITLEMENT_CACHE_KEY = 'cnsnt_entitlement';
const RECORD_COUNT_KEY = 'cnsnt_record_count';

class PurchaseService {
  private initialized: boolean = false;

  /**
   * Initialize the purchase service. Reads cached entitlement.
   */
  async initialize(): Promise<void> {
    if (this.initialized) return;
    this.initialized = true;
    await this.syncEntitlement();
  }

  /**
   * Sync entitlement from AsyncStorage cache.
   * With Stripe Payment Links there is no server-side SDK to query,
   * so entitlement is user-confirmed after checkout and cached locally.
   */
  private async syncEntitlement(): Promise<Entitlement> {
    return this.getCachedEntitlement();
  }

  /**
   * Get cached entitlement (no network).
   */
  private async getCachedEntitlement(): Promise<Entitlement> {
    const cached = await AsyncStorage.getItem(ENTITLEMENT_CACHE_KEY);
    if (cached === 'pro') return 'pro';
    return 'free';
  }

  /**
   * Get the current entitlement level.
   */
  async getEntitlement(): Promise<Entitlement> {
    return this.getCachedEntitlement();
  }

  /**
   * Get the current record count from cache.
   */
  async getRecordCount(): Promise<number> {
    const count = await AsyncStorage.getItem(RECORD_COUNT_KEY);
    return count ? parseInt(count, 10) : 0;
  }

  /**
   * Update the record count cache.
   */
  async updateRecordCount(count: number): Promise<void> {
    await AsyncStorage.setItem(RECORD_COUNT_KEY, count.toString());
  }

  /**
   * Get full purchase state for UI gating.
   */
  async getPurchaseState(): Promise<PurchaseState> {
    const entitlement = await this.getEntitlement();
    const recordCount = await this.getRecordCount();
    const isPro = entitlement === 'pro';

    return {
      entitlement,
      recordCount,
      canCreateRecord: isPro || recordCount < FREE_TIER_LIMIT,
      canRecord: isPro,
      canUseTemplates: isPro,
    };
  }

  /**
   * Check if a specific feature is available.
   */
  async canAccess(feature: 'recording' | 'templates' | 'create_record' | 'export_pdf'): Promise<boolean> {
    const state = await this.getPurchaseState();
    switch (feature) {
      case 'recording':
        return state.canRecord;
      case 'templates':
        return state.canUseTemplates;
      case 'create_record':
        return state.canCreateRecord;
      case 'export_pdf':
        return state.entitlement === 'pro';
      default:
        return false;
    }
  }

  /**
   * Check current entitlement.
   * Returns true if user has active pro entitlement.
   */
  async checkEntitlements(): Promise<boolean> {
    const cached = await this.getCachedEntitlement();
    return cached === 'pro';
  }

  /**
   * Purchase Pro subscription via Stripe Payment Link (monthly).
   * Opens the link in the system browser, waits for the user to return
   * to the app, then confirms the purchase via Alert.
   */
  async purchasePro(): Promise<boolean> {
    return this.purchasePackage('monthly');
  }

  /**
   * Purchase a specific plan via Stripe Payment Link.
   * @param plan - 'monthly' or 'yearly'
   */
  async purchasePackage(plan: 'monthly' | 'yearly'): Promise<boolean> {
    const url = plan === 'yearly' ? STRIPE_PAYMENT_LINKS.annual : STRIPE_PAYMENT_LINKS.monthly;

    const canOpen = await Linking.canOpenURL(url);
    if (!canOpen) {
      Alert.alert('Error', 'Unable to open the payment page. Please try again later.');
      return false;
    }

    return new Promise<boolean>((resolve) => {
      const handleAppState = (nextState: string) => {
        if (nextState === 'active') {
          subscription.remove();
          Alert.alert(
            'Confirm Purchase',
            'Did you complete your cnsnt Pro subscription?',
            [
              {
                text: 'No',
                style: 'cancel',
                onPress: () => resolve(false),
              },
              {
                text: 'Yes, I subscribed',
                style: 'default',
                onPress: async () => {
                  await AsyncStorage.setItem(ENTITLEMENT_CACHE_KEY, 'pro');
                  resolve(true);
                },
              },
            ],
            { cancelable: false },
          );
        }
      };

      const subscription = AppState.addEventListener('change', handleAppState);

      Linking.openURL(url).catch(() => {
        subscription.remove();
        Alert.alert('Error', 'Could not open payment page.');
        resolve(false);
      });
    });
  }

  /**
   * Restore purchases. With Stripe Payment Links, this prompts the user
   * to confirm they have an active subscription.
   */
  async restorePurchases(): Promise<Entitlement> {
    return new Promise<Entitlement>((resolve) => {
      Alert.alert(
        'Restore Purchase',
        'Do you have an active cnsnt Pro subscription through Stripe?',
        [
          {
            text: 'No',
            style: 'cancel',
            onPress: () => resolve('free'),
          },
          {
            text: 'Yes, restore Pro',
            style: 'default',
            onPress: async () => {
              await AsyncStorage.setItem(ENTITLEMENT_CACHE_KEY, 'pro');
              resolve('pro');
            },
          },
        ],
        { cancelable: false },
      );
    });
  }

  /**
   * Get available plans for display in paywall UI.
   */
  async getOfferings(): Promise<{
    proMonthly: { price: string; identifier: string } | null;
    proAnnual: { price: string; identifier: string } | null;
  }> {
    return {
      proMonthly: { price: '$4.99/mo', identifier: 'cnsnt_pro_monthly' },
      proAnnual: { price: '$29.99/yr', identifier: 'cnsnt_pro_annual' },
    };
  }

  /**
   * Check if user is in free tier and at limit.
   */
  async isAtFreeLimit(): Promise<boolean> {
    const state = await this.getPurchaseState();
    return state.entitlement === 'free' && state.recordCount >= FREE_TIER_LIMIT;
  }
}

export const purchaseService = new PurchaseService();
export default purchaseService;
