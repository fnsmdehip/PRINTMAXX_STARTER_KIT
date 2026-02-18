import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

type SubscriptionTier = 'free' | 'trial' | 'premium';

interface SubscriptionState {
  tier: SubscriptionTier;
  trialStartDate: string | null;
  premiumExpiresAt: string | null;
  hasSeenPaywall: boolean;
  paywallDismissCount: number;

  // Actions
  startTrial: () => void;
  activatePremium: (expiresAt: string) => void;
  cancelSubscription: () => void;
  setHasSeenPaywall: (seen: boolean) => void;
  incrementPaywallDismiss: () => void;

  // Computed
  isPremiumActive: () => boolean;
  isTrialActive: () => boolean;
  getTrialDaysRemaining: () => number;
  canAccessPremiumContent: () => boolean;

  reset: () => void;
}

export const useSubscriptionStore = create<SubscriptionState>()(
  persist(
    (set, get) => ({
      tier: 'free',
      trialStartDate: null,
      premiumExpiresAt: null,
      hasSeenPaywall: false,
      paywallDismissCount: 0,

      startTrial: () => {
        const trialStart = new Date().toISOString().split('T')[0];
        const trialEnd = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
          .toISOString()
          .split('T')[0];

        set({
          tier: 'trial',
          trialStartDate: trialStart,
          premiumExpiresAt: trialEnd,
        });
      },

      activatePremium: (expiresAt) => {
        set({
          tier: 'premium',
          premiumExpiresAt: expiresAt,
        });
      },

      cancelSubscription: () => {
        set({
          tier: 'free',
          premiumExpiresAt: null,
        });
      },

      setHasSeenPaywall: (seen) => set({ hasSeenPaywall: seen }),

      incrementPaywallDismiss: () =>
        set((state) => ({
          paywallDismissCount: state.paywallDismissCount + 1,
        })),

      isPremiumActive: () => {
        const { tier, premiumExpiresAt } = get();
        if (tier !== 'premium') return false;
        if (!premiumExpiresAt) return false;
        return new Date(premiumExpiresAt) > new Date();
      },

      isTrialActive: () => {
        const { tier, premiumExpiresAt } = get();
        if (tier !== 'trial') return false;
        if (!premiumExpiresAt) return false;
        return new Date(premiumExpiresAt) > new Date();
      },

      getTrialDaysRemaining: () => {
        const { tier, premiumExpiresAt } = get();
        if (tier !== 'trial' || !premiumExpiresAt) return 0;

        const expiresDate = new Date(premiumExpiresAt);
        const today = new Date();
        const diffTime = expiresDate.getTime() - today.getTime();
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        return Math.max(0, diffDays);
      },

      canAccessPremiumContent: () => {
        const { isPremiumActive, isTrialActive } = get();
        return isPremiumActive() || isTrialActive();
      },

      reset: () =>
        set({
          tier: 'free',
          trialStartDate: null,
          premiumExpiresAt: null,
          hasSeenPaywall: false,
          paywallDismissCount: 0,
        }),
    }),
    {
      name: 'biomaxx-subscription-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
