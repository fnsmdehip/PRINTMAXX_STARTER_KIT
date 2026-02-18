import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { UserSettings, SubscriptionState, StreakData, Gender } from '../types';
import {
  STORAGE_KEYS,
  TRIAL_DAYS,
  DEFAULT_WATER_GOAL,
  DEFAULT_MEWING_GOAL,
  DEFAULT_MEWING_REMINDER_INTERVAL,
} from '../utils/constants';
import { getTodayDateString, getDaysBetween, isYesterday } from '../utils/dateUtils';

interface UserStore {
  // Settings
  settings: UserSettings;
  updateSettings: (updates: Partial<UserSettings>) => void;
  setGender: (gender: Gender) => void;

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
  gender: 'female',
  age: 25,
  hasCompletedOnboarding: false,
  trialStartDate: null,
  notificationsEnabled: true,
  mewingRemindersEnabled: true,
  mewingReminderInterval: DEFAULT_MEWING_REMINDER_INTERVAL,
  morningRoutineTime: '07:00',
  eveningRoutineTime: '21:00',
  dailyGoals: {
    waterIntake: DEFAULT_WATER_GOAL,
    mewingMinutes: DEFAULT_MEWING_GOAL,
    routinesToComplete: ['morning_skincare', 'mewing', 'facial_exercises'],
  },
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

      setGender: (gender) =>
        set((state) => ({
          settings: { ...state.settings, gender },
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
