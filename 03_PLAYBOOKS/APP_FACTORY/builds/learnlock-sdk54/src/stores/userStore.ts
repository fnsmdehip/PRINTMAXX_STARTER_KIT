import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { UserSettings, BlockedApp, SubscriptionState } from '../types';
import {
  STORAGE_KEYS,
  DEFAULT_WORK_DURATION,
  DEFAULT_BREAK_DURATION,
  DEFAULT_BLOCKED_APPS,
  TRIAL_DURATION_DAYS,
} from '../utils/constants';
import { getTodayDateString, getTrialDaysRemaining } from '../utils/dateUtils';

interface UserStore {
  // User settings
  workDuration: number;
  breakDuration: number;
  blockedApps: BlockedApp[];
  notificationsEnabled: boolean;
  soundEnabled: boolean;
  vibrationEnabled: boolean;
  emergencyUnlockEnabled: boolean;
  hasCompletedOnboarding: boolean;
  trialStartDate: string | null;

  // Subscription state
  isSubscribed: boolean;
  isInTrial: boolean;
  subscriptionExpirationDate: string | null;

  // App blocking state
  isBlocked: boolean;

  // Actions - Settings
  setWorkDuration: (minutes: number) => void;
  setBreakDuration: (minutes: number) => void;
  setBlockedApps: (apps: BlockedApp[]) => void;
  addBlockedApp: (app: BlockedApp) => void;
  removeBlockedApp: (appId: string) => void;
  setNotificationsEnabled: (enabled: boolean) => void;
  setSoundEnabled: (enabled: boolean) => void;
  setVibrationEnabled: (enabled: boolean) => void;
  completeOnboarding: () => void;
  setOnboardingComplete: (complete: boolean) => void;
  updateSettings: (settings: Partial<{
    workDuration: number;
    breakDuration: number;
    blockedApps: string[];
    notificationsEnabled: boolean;
  }>) => void;

  // Actions - Subscription
  startTrial: () => void;
  checkTrialStatus: () => { isValid: boolean; daysRemaining: number };
  setSubscribed: (subscribed: boolean) => void;
  restorePurchases: () => Promise<boolean>;

  // Actions - Blocking
  setBlocked: (blocked: boolean) => void;

  // Helpers
  canAccessApp: () => boolean;
  getTrialDaysRemaining: () => number;
}

export const useUserStore = create<UserStore>()(
  persist(
    (set, get) => ({
      // Initial settings
      workDuration: DEFAULT_WORK_DURATION,
      breakDuration: DEFAULT_BREAK_DURATION,
      blockedApps: DEFAULT_BLOCKED_APPS,
      notificationsEnabled: true,
      soundEnabled: true,
      vibrationEnabled: true,
      emergencyUnlockEnabled: true,
      hasCompletedOnboarding: false,
      trialStartDate: null,

      // Subscription state
      isSubscribed: false,
      isInTrial: false,
      subscriptionExpirationDate: null,

      // Blocking state
      isBlocked: false,

      // Settings actions
      setWorkDuration: (minutes) => set({ workDuration: minutes }),
      setBreakDuration: (minutes) => set({ breakDuration: minutes }),

      setBlockedApps: (apps) => set({ blockedApps: apps }),

      addBlockedApp: (app) => {
        const { blockedApps } = get();
        if (!blockedApps.find((a) => a.id === app.id)) {
          set({ blockedApps: [...blockedApps, app] });
        }
      },

      removeBlockedApp: (appId) => {
        const { blockedApps } = get();
        set({ blockedApps: blockedApps.filter((a) => a.id !== appId) });
      },

      setNotificationsEnabled: (enabled) => set({ notificationsEnabled: enabled }),
      setSoundEnabled: (enabled) => set({ soundEnabled: enabled }),
      setVibrationEnabled: (enabled) => set({ vibrationEnabled: enabled }),

      completeOnboarding: () => {
        set({ hasCompletedOnboarding: true });
        // Start trial when onboarding completes
        get().startTrial();
      },

      setOnboardingComplete: (complete: boolean) => {
        set({ hasCompletedOnboarding: complete });
      },

      updateSettings: (settings: Partial<{
        workDuration: number;
        breakDuration: number;
        blockedApps: string[];
        notificationsEnabled: boolean;
      }>) => {
        if (settings.workDuration !== undefined) {
          set({ workDuration: settings.workDuration });
        }
        if (settings.breakDuration !== undefined) {
          set({ breakDuration: settings.breakDuration });
        }
        if (settings.notificationsEnabled !== undefined) {
          set({ notificationsEnabled: settings.notificationsEnabled });
        }
      },

      // Subscription actions
      startTrial: () => {
        const { trialStartDate } = get();
        // Only start trial if not already started
        if (!trialStartDate) {
          set({
            trialStartDate: getTodayDateString(),
            isInTrial: true,
          });
        }
      },

      checkTrialStatus: () => {
        const { trialStartDate, isSubscribed } = get();

        // If subscribed, trial doesn't matter
        if (isSubscribed) {
          return { isValid: true, daysRemaining: 0 };
        }

        // If no trial started, not valid
        if (!trialStartDate) {
          return { isValid: false, daysRemaining: 0 };
        }

        const daysRemaining = getTrialDaysRemaining(trialStartDate);
        const isValid = daysRemaining > 0;

        // Update state
        set({ isInTrial: isValid });

        return { isValid, daysRemaining };
      },

      setSubscribed: (subscribed) => {
        set({
          isSubscribed: subscribed,
          isInTrial: !subscribed && get().isInTrial,
        });
      },

      restorePurchases: async () => {
        // This would integrate with RevenueCat
        // For now, just a placeholder
        try {
          // const customerInfo = await Purchases.restorePurchases();
          // const isActive = customerInfo.entitlements.active['premium'];
          // set({ isSubscribed: isActive });
          // return isActive;
          return false;
        } catch (error) {
          console.error('Error restoring purchases:', error);
          return false;
        }
      },

      // Blocking actions
      setBlocked: (blocked) => set({ isBlocked: blocked }),

      // Helpers
      canAccessApp: () => {
        const { isSubscribed, trialStartDate } = get();

        // If subscribed, always can access
        if (isSubscribed) return true;

        // Check trial
        if (trialStartDate) {
          const daysRemaining = getTrialDaysRemaining(trialStartDate);
          return daysRemaining > 0;
        }

        return false;
      },

      getTrialDaysRemaining: () => {
        const { trialStartDate, isSubscribed } = get();

        if (isSubscribed) return 0;
        if (!trialStartDate) return TRIAL_DURATION_DAYS;

        return getTrialDaysRemaining(trialStartDate);
      },
    }),
    {
      name: STORAGE_KEYS.USER_SETTINGS,
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({
        workDuration: state.workDuration,
        breakDuration: state.breakDuration,
        blockedApps: state.blockedApps,
        notificationsEnabled: state.notificationsEnabled,
        soundEnabled: state.soundEnabled,
        vibrationEnabled: state.vibrationEnabled,
        emergencyUnlockEnabled: state.emergencyUnlockEnabled,
        hasCompletedOnboarding: state.hasCompletedOnboarding,
        trialStartDate: state.trialStartDate,
        isSubscribed: state.isSubscribed,
        subscriptionExpirationDate: state.subscriptionExpirationDate,
      }),
    }
  )
);
