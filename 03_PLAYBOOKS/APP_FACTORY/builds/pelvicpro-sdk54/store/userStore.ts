import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { differenceInDays, isToday, isYesterday, parseISO } from 'date-fns';

interface UserProfile {
  name: string;
  goals: string[];
  weeklyGoal: number;
  unit: 'lb' | 'kg';
}

interface UserState {
  // Profile
  profile: UserProfile;

  // Onboarding
  hasCompletedOnboarding: boolean;

  // Subscription
  isSubscribed: boolean;
  trialStartDate: string | null;
  workoutCountInTrial: number;

  // Streaks
  currentStreak: number;
  longestStreak: number;
  lastWorkoutDate: string | null;

  // Stats
  totalWorkouts: number;
  totalPRs: number;
  joinedDate: string;

  // Luna
  lunaEnabled: boolean;

  // Actions
  setProfile: (profile: Partial<UserProfile>) => void;
  completeOnboarding: () => void;
  setSubscribed: (status: boolean) => void;
  startTrial: () => void;
  incrementTrialWorkout: () => void;
  recordWorkout: () => void;
  incrementPR: () => void;
  toggleLuna: () => void;

  // Helpers
  canAccessApp: () => boolean;
  isTrialActive: () => boolean;
  isTrialExpired: () => boolean;
  getTrialDaysRemaining: () => number;
}

export const useUserStore = create<UserState>()(
  persist(
    (set, get) => ({
      // Initial state
      profile: {
        name: '',
        goals: [],
        weeklyGoal: 4,
        unit: 'lb',
      },
      hasCompletedOnboarding: false,
      isSubscribed: false,
      trialStartDate: null,
      workoutCountInTrial: 0,
      currentStreak: 0,
      longestStreak: 0,
      lastWorkoutDate: null,
      totalWorkouts: 0,
      totalPRs: 0,
      joinedDate: new Date().toISOString(),
      lunaEnabled: true,

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
          workoutCountInTrial: 0,
        });
      },

      incrementTrialWorkout: () => {
        set((state) => ({
          workoutCountInTrial: state.workoutCountInTrial + 1,
        }));
      },

      recordWorkout: () => {
        const { lastWorkoutDate, currentStreak, longestStreak, totalWorkouts } =
          get();
        const today = new Date().toISOString();

        let newStreak = currentStreak;

        if (!lastWorkoutDate) {
          // First workout ever
          newStreak = 1;
        } else if (isToday(parseISO(lastWorkoutDate))) {
          // Already worked out today, dont increment streak
          newStreak = currentStreak;
        } else if (isYesterday(parseISO(lastWorkoutDate))) {
          // Worked out yesterday, continue streak
          newStreak = currentStreak + 1;
        } else {
          // Streak broken, start fresh
          newStreak = 1;
        }

        set({
          lastWorkoutDate: today,
          currentStreak: newStreak,
          longestStreak: Math.max(longestStreak, newStreak),
          totalWorkouts: totalWorkouts + 1,
        });
      },

      incrementPR: () => {
        set((state) => ({
          totalPRs: state.totalPRs + 1,
        }));
      },

      toggleLuna: () => {
        set((state) => ({
          lunaEnabled: !state.lunaEnabled,
        }));
      },

      // Helpers
      canAccessApp: () => {
        const { isSubscribed, isTrialActive, isTrialExpired } = get();
        if (isSubscribed) return true;
        if (isTrialActive()) return true;
        return false;
      },

      isTrialActive: () => {
        const { trialStartDate, workoutCountInTrial, isSubscribed } = get();
        if (isSubscribed) return false;
        if (!trialStartDate) return false;

        const daysSinceTrialStart = differenceInDays(
          new Date(),
          parseISO(trialStartDate)
        );

        // Trial is 3 days OR 3 workouts, whichever comes first
        return daysSinceTrialStart < 3 && workoutCountInTrial < 3;
      },

      isTrialExpired: () => {
        const { trialStartDate, workoutCountInTrial, isSubscribed } = get();
        if (isSubscribed) return false;
        if (!trialStartDate) return false;

        const daysSinceTrialStart = differenceInDays(
          new Date(),
          parseISO(trialStartDate)
        );

        return daysSinceTrialStart >= 3 || workoutCountInTrial >= 3;
      },

      getTrialDaysRemaining: () => {
        const { trialStartDate } = get();
        if (!trialStartDate) return 3;

        const daysSinceTrialStart = differenceInDays(
          new Date(),
          parseISO(trialStartDate)
        );

        return Math.max(0, 3 - daysSinceTrialStart);
      },
    }),
    {
      name: 'femfit-user-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
