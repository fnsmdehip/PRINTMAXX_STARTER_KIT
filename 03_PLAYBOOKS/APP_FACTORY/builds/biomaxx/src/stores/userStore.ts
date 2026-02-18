import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { User, Subscription } from '../types';
import { getToday } from '../utils/dateUtils';

interface UserState {
  user: User | null;
  subscription: Subscription;
  lastActiveDate: string | null;
  setUser: (user: User) => void;
  updateUser: (updates: Partial<User>) => void;
  completeOnboarding: (name: string, goals: string[]) => void;
  startTrial: () => void;
  upgradeToPremium: () => void;
  incrementStreak: () => void;
  incrementSessions: () => void;
  addAchievement: (achievementId: string) => void;
  checkAndUpdateStreak: () => void;
  isPremium: () => boolean;
  reset: () => void;
}

const initialSubscription: Subscription = {
  status: 'free',
};

export const useUserStore = create<UserState>()(
  persist(
    (set, get) => ({
      user: null,
      subscription: initialSubscription,
      lastActiveDate: null,

      setUser: (user) => set({ user }),

      updateUser: (updates) =>
        set((state) => ({
          user: state.user ? { ...state.user, ...updates } : null,
        })),

      completeOnboarding: (name, goals) =>
        set({
          user: {
            name,
            goals,
            onboardingComplete: true,
            createdAt: getToday(),
            streakDays: 0,
            totalSessions: 0,
            achievements: [],
          },
          lastActiveDate: getToday(),
        }),

      startTrial: () =>
        set({
          subscription: {
            status: 'trial',
            trialStartDate: getToday(),
            expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
              .toISOString()
              .split('T')[0],
          },
        }),

      upgradeToPremium: () =>
        set({
          subscription: {
            status: 'premium',
            expiresAt: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000)
              .toISOString()
              .split('T')[0],
          },
        }),

      incrementStreak: () =>
        set((state) => ({
          user: state.user
            ? { ...state.user, streakDays: state.user.streakDays + 1 }
            : null,
        })),

      incrementSessions: () =>
        set((state) => ({
          user: state.user
            ? { ...state.user, totalSessions: state.user.totalSessions + 1 }
            : null,
        })),

      addAchievement: (achievementId) =>
        set((state) => ({
          user: state.user
            ? {
                ...state.user,
                achievements: state.user.achievements.includes(achievementId)
                  ? state.user.achievements
                  : [...state.user.achievements, achievementId],
              }
            : null,
        })),

      checkAndUpdateStreak: () => {
        const { user, lastActiveDate } = get();
        if (!user || !lastActiveDate) return;

        const today = getToday();
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        const yesterdayStr = yesterday.toISOString().split('T')[0];

        if (lastActiveDate === today) {
          return;
        } else if (lastActiveDate === yesterdayStr) {
          set({
            user: { ...user, streakDays: user.streakDays + 1 },
            lastActiveDate: today,
          });
        } else {
          set({
            user: { ...user, streakDays: 1 },
            lastActiveDate: today,
          });
        }
      },

      isPremium: () => {
        const { subscription } = get();
        if (subscription.status === 'premium') return true;
        if (subscription.status === 'trial' && subscription.expiresAt) {
          return new Date(subscription.expiresAt) > new Date();
        }
        return false;
      },

      reset: () =>
        set({
          user: null,
          subscription: initialSubscription,
          lastActiveDate: null,
        }),
    }),
    {
      name: 'biomaxx-user-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
