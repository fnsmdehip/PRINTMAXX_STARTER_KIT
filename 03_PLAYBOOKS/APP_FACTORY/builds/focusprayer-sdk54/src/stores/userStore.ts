/**
 * User Store
 * Manages user settings, subscription, and onboarding state
 */

import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { APP_CONFIG } from '../utils/constants';

export interface UserSettings {
  onboardingComplete: boolean;
  blockedApps: string[];
  devotionDurationMinutes: number;
  dailyResetTime: string;
  requireScripture: boolean;
  requireTimer: boolean;
  emergencyUnlockEnabled: boolean;
  notificationsEnabled: boolean;
}

interface SubscriptionState {
  isSubscribed: boolean;
  isTrialActive: boolean;
  trialStartDate: number | null;
  trialEndDate: number | null;
  expirationDate: number | null;
}

interface UserState {
  settings: UserSettings;
  subscription: SubscriptionState;

  // Actions
  loadSettings: () => Promise<void>;
  loadSubscription: () => Promise<void>;
  updateSettings: (settings: Partial<UserSettings>) => Promise<void>;
  completeOnboarding: () => Promise<void>;
  startTrial: () => Promise<void>;
  setSubscribed: (isSubscribed: boolean, expirationDate?: number) => Promise<void>;
  checkAccess: () => boolean;
  getTrialDaysRemaining: () => number;
}

const DEFAULT_SETTINGS: UserSettings = {
  onboardingComplete: false,
  blockedApps: [],
  devotionDurationMinutes: APP_CONFIG.defaultDevotionMinutes,
  dailyResetTime: '05:00',
  requireScripture: true,
  requireTimer: true,
  emergencyUnlockEnabled: true,
  notificationsEnabled: true,
};

const DEFAULT_SUBSCRIPTION: SubscriptionState = {
  isSubscribed: false,
  isTrialActive: false,
  trialStartDate: null,
  trialEndDate: null,
  expirationDate: null,
};

export const useUserStore = create<UserState>((set, get) => ({
  settings: DEFAULT_SETTINGS,
  subscription: DEFAULT_SUBSCRIPTION,

  loadSettings: async () => {
    try {
      const stored = await AsyncStorage.getItem(APP_CONFIG.storageKeys.user);
      if (stored) {
        const parsed = JSON.parse(stored);
        set({
          settings: { ...DEFAULT_SETTINGS, ...parsed.settings },
        });
      }
    } catch (error) {
      console.error('Failed to load settings:', error);
    }
  },

  loadSubscription: async () => {
    try {
      const stored = await AsyncStorage.getItem(`${APP_CONFIG.storageKeys.user}_subscription`);
      if (stored) {
        const parsed = JSON.parse(stored);
        set({
          subscription: { ...DEFAULT_SUBSCRIPTION, ...parsed },
        });
      }
    } catch (error) {
      console.error('Failed to load subscription:', error);
    }
  },

  updateSettings: async (newSettings) => {
    const state = get();
    const updatedSettings = { ...state.settings, ...newSettings };
    set({ settings: updatedSettings });

    try {
      const stored = await AsyncStorage.getItem(APP_CONFIG.storageKeys.user);
      const existing = stored ? JSON.parse(stored) : {};
      await AsyncStorage.setItem(
        APP_CONFIG.storageKeys.user,
        JSON.stringify({ ...existing, settings: updatedSettings })
      );
    } catch (error) {
      console.error('Failed to save settings:', error);
    }
  },

  completeOnboarding: async () => {
    const { updateSettings, startTrial } = get();
    await updateSettings({ onboardingComplete: true });
    await startTrial();
  },

  startTrial: async () => {
    const now = Date.now();
    const trialEndDate = now + APP_CONFIG.trialDays * 24 * 60 * 60 * 1000;

    const subscription: SubscriptionState = {
      isSubscribed: false,
      isTrialActive: true,
      trialStartDate: now,
      trialEndDate,
      expirationDate: null,
    };

    set({ subscription });

    try {
      await AsyncStorage.setItem(
        `${APP_CONFIG.storageKeys.user}_subscription`,
        JSON.stringify(subscription)
      );
    } catch (error) {
      console.error('Failed to save subscription:', error);
    }
  },

  setSubscribed: async (isSubscribed, expirationDate) => {
    const state = get();
    const subscription: SubscriptionState = {
      ...state.subscription,
      isSubscribed,
      isTrialActive: false,
      expirationDate: expirationDate || null,
    };

    set({ subscription });

    try {
      await AsyncStorage.setItem(
        `${APP_CONFIG.storageKeys.user}_subscription`,
        JSON.stringify(subscription)
      );
    } catch (error) {
      console.error('Failed to save subscription:', error);
    }
  },

  checkAccess: () => {
    const { subscription } = get();
    const now = Date.now();

    // Subscribed users always have access
    if (subscription.isSubscribed) {
      if (subscription.expirationDate && subscription.expirationDate < now) {
        return false;
      }
      return true;
    }

    // Check trial
    if (subscription.isTrialActive && subscription.trialEndDate) {
      return subscription.trialEndDate > now;
    }

    return false;
  },

  getTrialDaysRemaining: () => {
    const { subscription } = get();
    const now = Date.now();

    if (!subscription.isTrialActive || !subscription.trialEndDate) {
      return 0;
    }

    const remaining = subscription.trialEndDate - now;
    if (remaining <= 0) {
      return 0;
    }

    return Math.ceil(remaining / (24 * 60 * 60 * 1000));
  },
}));
