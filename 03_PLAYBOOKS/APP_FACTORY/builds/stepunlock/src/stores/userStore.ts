import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {
  UserSettings,
  SubscriptionState,
  StreakData,
  BlockedApp,
} from '../types';
import {
  DEFAULT_STEP_GOAL,
  STORAGE_KEYS,
  DEFAULT_BLOCKED_APPS,
  TRIAL_DAYS,
} from '../utils/constants';
import { getTodayDateString, getDaysBetween, isYesterday } from '../utils/dateUtils';

interface UserStore {
  // Settings
  settings: UserSettings;
  updateSettings: (updates: Partial<UserSettings>) => void;
  setStepGoal: (goal: number) => void;
  addBlockedApp: (app: BlockedApp) => void;
  removeBlockedApp: (appId: string) => void;

  // Subscription
  subscription: SubscriptionState;
  updateSubscription: (updates: Partial<SubscriptionState>) => void;
  checkTrialStatus: () => void;
  startTrial: () => void;

  // Streak
  streak: StreakData;
  updateStreak: (goalMet: boolean) => void;
  resetStreak: () => void;

  // Onboarding
  completeOnboarding: () => void;
  resetOnboarding: () => void;
}

const defaultSettings: UserSettings = {
  stepGoal: DEFAULT_STEP_GOAL,
  blockedApps: DEFAULT_BLOCKED_APPS,
  dailyResetTime: '00:00',
  notificationsEnabled: true,
  emergencyUnlockEnabled: true,
  hasCompletedOnboarding: false,
  trialStartDate: null,
};

const defaultSubscription: SubscriptionState = {
  isSubscribed: false,
  isInTrial: false,
  trialDaysRemaining: TRIAL_DAYS,
  expirationDate: null,
};

const defaultStreak: StreakData = {
  currentStreak: 0,
  longestStreak: 0,
  totalDaysCompleted: 0,
  completedDates: [],
  lastCompletedDate: null,
};

export const useUserStore = create<UserStore>()(
  persist(
    (set, get) => ({
      // Settings
      settings: defaultSettings,

      updateSettings: (updates) =>
        set((state) => ({
          settings: { ...state.settings, ...updates },
        })),

      setStepGoal: (goal) =>
        set((state) => ({
          settings: { ...state.settings, stepGoal: goal },
        })),

      addBlockedApp: (app) =>
        set((state) => ({
          settings: {
            ...state.settings,
            blockedApps: [...state.settings.blockedApps, app],
          },
        })),

      removeBlockedApp: (appId) =>
        set((state) => ({
          settings: {
            ...state.settings,
            blockedApps: state.settings.blockedApps.filter(
              (app) => app.id !== appId
            ),
          },
        })),

      // Subscription
      subscription: defaultSubscription,

      updateSubscription: (updates) =>
        set((state) => ({
          subscription: { ...state.subscription, ...updates },
        })),

      startTrial: () => {
        const trialStartDate = getTodayDateString();
        set((state) => ({
          settings: { ...state.settings, trialStartDate },
          subscription: {
            ...state.subscription,
            isInTrial: true,
            trialDaysRemaining: TRIAL_DAYS,
          },
        }));
      },

      checkTrialStatus: () => {
        const { settings, subscription } = get();

        // Already subscribed, no need to check trial
        if (subscription.isSubscribed) {
          return;
        }

        // No trial started
        if (!settings.trialStartDate) {
          set((state) => ({
            subscription: {
              ...state.subscription,
              isInTrial: false,
              trialDaysRemaining: TRIAL_DAYS,
            },
          }));
          return;
        }

        // Calculate trial days remaining
        const daysSinceTrialStart = getDaysBetween(
          settings.trialStartDate,
          getTodayDateString()
        );
        const trialDaysRemaining = Math.max(0, TRIAL_DAYS - daysSinceTrialStart);
        const isInTrial = trialDaysRemaining > 0;

        set((state) => ({
          subscription: {
            ...state.subscription,
            isInTrial,
            trialDaysRemaining,
          },
        }));
      },

      // Streak
      streak: defaultStreak,

      updateStreak: (goalMet) => {
        const { streak } = get();
        const today = getTodayDateString();

        // Already recorded today
        if (streak.completedDates.includes(today)) {
          return;
        }

        if (!goalMet) {
          // Check if streak should be broken (missed yesterday)
          if (streak.lastCompletedDate && !isYesterday(streak.lastCompletedDate)) {
            set({ streak: { ...streak, currentStreak: 0 } });
          }
          return;
        }

        // Goal met today
        const wasYesterdayCompleted =
          streak.lastCompletedDate && isYesterday(streak.lastCompletedDate);

        const newCurrentStreak = wasYesterdayCompleted
          ? streak.currentStreak + 1
          : 1;

        const newLongestStreak = Math.max(streak.longestStreak, newCurrentStreak);

        set({
          streak: {
            currentStreak: newCurrentStreak,
            longestStreak: newLongestStreak,
            totalDaysCompleted: streak.totalDaysCompleted + 1,
            completedDates: [...streak.completedDates, today],
            lastCompletedDate: today,
          },
        });
      },

      resetStreak: () => {
        set((state) => ({
          streak: {
            ...state.streak,
            currentStreak: 0,
          },
        }));
      },

      // Onboarding
      completeOnboarding: () =>
        set((state) => ({
          settings: { ...state.settings, hasCompletedOnboarding: true },
        })),

      resetOnboarding: () =>
        set((state) => ({
          settings: { ...state.settings, hasCompletedOnboarding: false },
        })),
    }),
    {
      name: STORAGE_KEYS.USER_SETTINGS,
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
