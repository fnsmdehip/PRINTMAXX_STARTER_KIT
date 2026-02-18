import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { SubscriptionState } from '../types';

interface SubscriptionStore extends SubscriptionState {
  // Actions
  startTrial: () => void;
  endTrial: () => void;
  upgradeToPro: (expiresAt: string) => void;
  cancelSubscription: () => void;
  restorePurchases: () => Promise<boolean>;
  checkTrialStatus: () => void;
}

const TRIAL_DURATION_DAYS = 7;

export const useSubscriptionStore = create<SubscriptionStore>()(
  persist(
    (set, get) => ({
      isPro: false,
      expiresAt: undefined,
      trialActive: false,
      trialEndsAt: undefined,

      startTrial: () => {
        const trialEnd = new Date();
        trialEnd.setDate(trialEnd.getDate() + TRIAL_DURATION_DAYS);
        set({
          isPro: true,
          trialActive: true,
          trialEndsAt: trialEnd.toISOString(),
        });
      },

      endTrial: () => {
        set({
          isPro: false,
          trialActive: false,
          trialEndsAt: undefined,
        });
      },

      upgradeToPro: (expiresAt) => {
        set({
          isPro: true,
          expiresAt,
          trialActive: false,
          trialEndsAt: undefined,
        });
      },

      cancelSubscription: () => {
        set({
          isPro: false,
          expiresAt: undefined,
          trialActive: false,
          trialEndsAt: undefined,
        });
      },

      restorePurchases: async () => {
        // Placeholder for RevenueCat integration
        // In production, this would call RevenueCat.restorePurchases()
        console.log('Restore purchases called - RevenueCat integration needed');

        // Simulate checking for purchases
        // Replace with actual RevenueCat code:
        // const customerInfo = await Purchases.restorePurchases();
        // const isPro = customerInfo.entitlements.active['pro'] !== undefined;

        return false;
      },

      checkTrialStatus: () => {
        const { trialActive, trialEndsAt, expiresAt } = get();

        // Check if trial has expired
        if (trialActive && trialEndsAt) {
          const trialEndDate = new Date(trialEndsAt);
          if (new Date() > trialEndDate) {
            set({
              isPro: false,
              trialActive: false,
              trialEndsAt: undefined,
            });
          }
        }

        // Check if subscription has expired
        if (expiresAt) {
          const expireDate = new Date(expiresAt);
          if (new Date() > expireDate) {
            set({
              isPro: false,
              expiresAt: undefined,
            });
          }
        }
      },
    }),
    {
      name: 'promptvault-subscription',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);

// Pricing configuration - Freemium model
// Free tier: Access to all prompts with ads
// Premium tier: No ads + AI features + cloud sync
export const PRICING = {
  monthly: {
    id: 'promptvault_premium_monthly',
    price: '$2.99',
    priceValue: 2.99,
    period: 'month',
    savings: null,
  },
  annual: {
    id: 'promptvault_premium_annual',
    price: '$19.99',
    priceValue: 19.99,
    period: 'year',
    savings: '44%',
    monthlyEquivalent: '$1.67',
  },
} as const;

// Ad configuration
// TODO: Replace with your actual AdMob unit IDs
// Test IDs for development:
// Banner: ca-app-pub-3940256099942544/6300978111
// Interstitial: ca-app-pub-3940256099942544/1033173712
export const AD_CONFIG = {
  banner: {
    ios: 'ca-app-pub-XXXXX/XXXXX', // Replace with real iOS banner ID
    android: 'ca-app-pub-XXXXX/XXXXX', // Replace with real Android banner ID
    testId: 'ca-app-pub-3940256099942544/6300978111',
  },
  interstitial: {
    ios: 'ca-app-pub-XXXXX/XXXXX', // Replace with real iOS interstitial ID
    android: 'ca-app-pub-XXXXX/XXXXX', // Replace with real Android interstitial ID
    testId: 'ca-app-pub-3940256099942544/1033173712',
  },
  // Show interstitial every N category switches
  interstitialFrequency: 3,
} as const;
