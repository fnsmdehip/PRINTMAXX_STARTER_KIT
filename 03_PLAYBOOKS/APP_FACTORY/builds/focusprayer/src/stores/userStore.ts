/**
 * User Settings Store
 * Manages user preferences and configuration
 */

import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {
  UserSettings,
  SubscriptionState,
  DevotionStatus,
} from '../types';
import {
  STORAGE_KEYS,
  DEFAULT_DEVOTION_MINUTES,
  DEFAULT_RESET_TIME,
  TRIAL_DAYS,
} from '../utils/constants';
import { isTrialExpired, getTrialDaysRemaining } from '../utils/dateUtils';

interface UserState {
  settings: UserSettings;
  subscription: SubscriptionState;
  trialStart: number | null;
  isLoading: boolean;

  // Actions
  loadSettings: () => Promise<void>;
  updateSettings: (updates: Partial<UserSettings>) => Promise<void>;
  updateBlockedApps: (apps: string[]) => Promise<void>;
  setOnboardingComplete: () => Promise<void>;

  // Subscription
  loadSubscription: () => Promise<void>;
  updateSubscription: (subscription: SubscriptionState) => Promise<void>;
  startTrial: () => Promise<void>;
  checkAccess: () => boolean;
  getTrialDaysRemaining: () => number;
}

const defaultSettings: UserSettings = {
  blockedApps: [],
  devotionDurationMinutes: DEFAULT_DEVOTION_MINUTES,
  dailyResetTime: DEFAULT_RESET_TIME,
  requireScripture: true,
  requireTimer: true,
  emergencyUnlockEnabled: true,
  notificationsEnabled: true,
  onboardingComplete: false,
};

const defaultSubscription: SubscriptionState = {
  isSubscribed: false,
  isTrialing: false,
  trialEndsAt: null,
  subscriptionType: null,
  expiresAt: null,
};

export const useUserStore = create<UserState>((set, get) => ({
  settings: defaultSettings,
  subscription: defaultSubscription,
  trialStart: null,
  isLoading: true,

  loadSettings: async () => {
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEYS.USER_SETTINGS);
      if (stored) {
        const parsed = JSON.parse(stored) as UserSettings;
        set({ settings: { ...defaultSettings, ...parsed } });
      }
    } catch (error) {
      console.error('Failed to load settings:', error);
    } finally {
      set({ isLoading: false });
    }
  },

  updateSettings: async (updates: Partial<UserSettings>) => {
    const current = get().settings;
    const newSettings = { ...current, ...updates };
    set({ settings: newSettings });
    try {
      await AsyncStorage.setItem(
        STORAGE_KEYS.USER_SETTINGS,
        JSON.stringify(newSettings)
      );
    } catch (error) {
      console.error('Failed to save settings:', error);
    }
  },

  updateBlockedApps: async (apps: string[]) => {
    await get().updateSettings({ blockedApps: apps });
  },

  setOnboardingComplete: async () => {
    await get().updateSettings({ onboardingComplete: true });
  },

  loadSubscription: async () => {
    try {
      const [subData, trialData] = await Promise.all([
        AsyncStorage.getItem(STORAGE_KEYS.SUBSCRIPTION),
        AsyncStorage.getItem(STORAGE_KEYS.TRIAL_START),
      ]);

      let subscription = defaultSubscription;
      let trialStart: number | null = null;

      if (subData) {
        subscription = JSON.parse(subData);
      }

      if (trialData) {
        trialStart = JSON.parse(trialData);
        // Check if still in trial
        if (trialStart && !isTrialExpired(trialStart, TRIAL_DAYS)) {
          subscription = {
            ...subscription,
            isTrialing: true,
            trialEndsAt: trialStart + TRIAL_DAYS * 24 * 60 * 60 * 1000,
          };
        }
      }

      set({ subscription, trialStart });
    } catch (error) {
      console.error('Failed to load subscription:', error);
    }
  },

  updateSubscription: async (subscription: SubscriptionState) => {
    set({ subscription });
    try {
      await AsyncStorage.setItem(
        STORAGE_KEYS.SUBSCRIPTION,
        JSON.stringify(subscription)
      );
    } catch (error) {
      console.error('Failed to save subscription:', error);
    }
  },

  startTrial: async () => {
    const now = Date.now();
    set({
      trialStart: now,
      subscription: {
        isSubscribed: false,
        isTrialing: true,
        trialEndsAt: now + TRIAL_DAYS * 24 * 60 * 60 * 1000,
        subscriptionType: null,
        expiresAt: null,
      },
    });
    try {
      await AsyncStorage.setItem(STORAGE_KEYS.TRIAL_START, JSON.stringify(now));
    } catch (error) {
      console.error('Failed to save trial start:', error);
    }
  },

  checkAccess: () => {
    const { subscription, trialStart } = get();

    // Has active subscription
    if (subscription.isSubscribed) {
      return true;
    }

    // In valid trial period
    if (trialStart && !isTrialExpired(trialStart, TRIAL_DAYS)) {
      return true;
    }

    return false;
  },

  getTrialDaysRemaining: () => {
    const { trialStart } = get();
    if (!trialStart) return 0;
    return getTrialDaysRemaining(trialStart, TRIAL_DAYS);
  },
}));
