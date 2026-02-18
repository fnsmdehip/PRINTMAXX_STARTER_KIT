import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { differenceInDays, isToday, isYesterday, parseISO } from 'date-fns';

export type FaithBackground = 'new' | 'growing' | 'mature' | 'returning';

interface UserProfile {
  name: string;
  faithBackground: FaithBackground | null;
  notificationTime: { hour: number; minute: number } | null;
  notificationsEnabled: boolean;
}

interface UserState {
  // Profile
  profile: UserProfile;

  // Onboarding
  hasCompletedOnboarding: boolean;

  // Subscription
  isSubscribed: boolean;
  trialStartDate: string | null;
  devotionCountInTrial: number;

  // Streaks
  currentStreak: number;
  longestStreak: number;
  lastDevotionDate: string | null;

  // Stats
  totalDevotions: number;
  totalPrayers: number;
  joinedDate: string;

  // Devotion tracking
  completedDevotions: string[]; // IDs of completed devotions
  savedVerses: string[]; // IDs of saved verses

  // Actions
  setProfile: (profile: Partial<UserProfile>) => void;
  completeOnboarding: () => void;
  setSubscribed: (status: boolean) => void;
  startTrial: () => void;
  incrementTrialDevotion: () => void;
  recordDevotion: (devotionId?: string) => void;
  recordPrayer: () => void;
  saveVerse: (verseId: string) => void;
  unsaveVerse: (verseId: string) => void;

  // Helpers
  canAccessApp: () => boolean;
  isTrialActive: () => boolean;
  isTrialExpired: () => boolean;
  getTrialDaysRemaining: () => number;
  isDevotionCompleted: (devotionId: string) => boolean;
  isVerseSaved: (verseId: string) => boolean;
}

export const useUserStore = create<UserState>()(
  persist(
    (set, get) => ({
      // Initial state
      profile: {
        name: '',
        faithBackground: null,
        notificationTime: { hour: 7, minute: 0 },
        notificationsEnabled: true,
      },
      hasCompletedOnboarding: false,
      isSubscribed: false,
      trialStartDate: null,
      devotionCountInTrial: 0,
      currentStreak: 0,
      longestStreak: 0,
      lastDevotionDate: null,
      totalDevotions: 0,
      totalPrayers: 0,
      joinedDate: new Date().toISOString(),
      completedDevotions: [],
      savedVerses: [],

      // Actions
      setProfile: (updates) => {
        set((state) => ({
          profile: { ...state.profile, ...updates },
        }));
      },

      completeOnboarding: () => {
        set({ hasCompletedOnboarding: true });
      },

      setSubscribed: (status) => {
        set({ isSubscribed: status });
      },

      startTrial: () => {
        set({
          trialStartDate: new Date().toISOString(),
          devotionCountInTrial: 0,
        });
      },

      incrementTrialDevotion: () => {
        set((state) => ({
          devotionCountInTrial: state.devotionCountInTrial + 1,
        }));
      },

      recordDevotion: (devotionId?: string) => {
        const { lastDevotionDate, currentStreak, longestStreak, totalDevotions, completedDevotions } =
          get();
        const today = new Date().toISOString();

        let newStreak = currentStreak;

        if (!lastDevotionDate) {
          // First devotion ever
          newStreak = 1;
        } else if (isToday(parseISO(lastDevotionDate))) {
          // Already did devotion today, dont increment streak
          newStreak = currentStreak;
        } else if (isYesterday(parseISO(lastDevotionDate))) {
          // Did devotion yesterday, continue streak
          newStreak = currentStreak + 1;
        } else {
          // Streak broken, start fresh
          newStreak = 1;
        }

        const newCompletedDevotions = devotionId && !completedDevotions.includes(devotionId)
          ? [...completedDevotions, devotionId]
          : completedDevotions;

        set({
          lastDevotionDate: today,
          currentStreak: newStreak,
          longestStreak: Math.max(longestStreak, newStreak),
          totalDevotions: totalDevotions + 1,
          completedDevotions: newCompletedDevotions,
        });
      },

      recordPrayer: () => {
        set((state) => ({
          totalPrayers: state.totalPrayers + 1,
        }));
      },

      saveVerse: (verseId: string) => {
        set((state) => ({
          savedVerses: state.savedVerses.includes(verseId)
            ? state.savedVerses
            : [...state.savedVerses, verseId],
        }));
      },

      unsaveVerse: (verseId: string) => {
        set((state) => ({
          savedVerses: state.savedVerses.filter((id) => id !== verseId),
        }));
      },

      // Helpers
      canAccessApp: () => {
        const { isSubscribed, isTrialActive } = get();
        if (isSubscribed) return true;
        if (isTrialActive()) return true;
        return false;
      },

      isTrialActive: () => {
        const { trialStartDate, devotionCountInTrial, isSubscribed } = get();
        if (isSubscribed) return false;
        if (!trialStartDate) return false;

        const daysSinceTrialStart = differenceInDays(
          new Date(),
          parseISO(trialStartDate)
        );

        // Trial is 7 days OR 5 devotions, whichever comes first
        return daysSinceTrialStart < 7 && devotionCountInTrial < 5;
      },

      isTrialExpired: () => {
        const { trialStartDate, devotionCountInTrial, isSubscribed } = get();
        if (isSubscribed) return false;
        if (!trialStartDate) return false;

        const daysSinceTrialStart = differenceInDays(
          new Date(),
          parseISO(trialStartDate)
        );

        return daysSinceTrialStart >= 7 || devotionCountInTrial >= 5;
      },

      getTrialDaysRemaining: () => {
        const { trialStartDate } = get();
        if (!trialStartDate) return 7;

        const daysSinceTrialStart = differenceInDays(
          new Date(),
          parseISO(trialStartDate)
        );

        return Math.max(0, 7 - daysSinceTrialStart);
      },

      isDevotionCompleted: (devotionId: string) => {
        return get().completedDevotions.includes(devotionId);
      },

      isVerseSaved: (verseId: string) => {
        return get().savedVerses.includes(verseId);
      },
    }),
    {
      name: 'devotionflow-user-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
