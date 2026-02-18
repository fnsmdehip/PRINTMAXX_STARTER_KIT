/**
 * Devotion Store
 * Manages daily devotion sessions and completion tracking
 */

import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {
  DevotionSession,
  StreakData,
  DevotionStatus,
  BiblePassage,
} from '../types';
import { STORAGE_KEYS, DEFAULT_RESET_TIME } from '../utils/constants';
import {
  getTodayString,
  getDevotionalDay,
  areConsecutiveDays,
  generateSessionId,
} from '../utils/dateUtils';

interface DevotionState {
  currentSession: DevotionSession | null;
  todayStatus: DevotionStatus;
  streak: StreakData;
  todaysPassage: BiblePassage | null;
  timerSecondsRemaining: number;
  scriptureReadComplete: boolean;
  isLoading: boolean;

  // Session actions
  loadTodayStatus: () => Promise<void>;
  startSession: (durationMinutes: number) => Promise<void>;
  updateTimer: (seconds: number) => void;
  completeTimer: () => void;
  completeScripture: (passage: BiblePassage) => void;
  completeSession: () => Promise<void>;
  emergencyUnlock: () => Promise<void>;

  // Streak actions
  loadStreak: () => Promise<void>;
  updateStreak: (completed: boolean) => Promise<void>;
  resetStreak: () => Promise<void>;

  // Scripture
  setTodaysPassage: (passage: BiblePassage) => void;
}

const defaultStreak: StreakData = {
  currentStreak: 0,
  longestStreak: 0,
  totalDaysCompleted: 0,
  completedDates: [],
  lastCompletedDate: null,
};

export const useDevotionStore = create<DevotionState>((set, get) => ({
  currentSession: null,
  todayStatus: 'not_started',
  streak: defaultStreak,
  todaysPassage: null,
  timerSecondsRemaining: 0,
  scriptureReadComplete: false,
  isLoading: true,

  loadTodayStatus: async () => {
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEYS.SESSIONS);
      if (!stored) {
        set({ todayStatus: 'not_started', isLoading: false });
        return;
      }

      const sessions: DevotionSession[] = JSON.parse(stored);
      const today = getDevotionalDay(DEFAULT_RESET_TIME);

      const todaySession = sessions.find((s) => s.date === today);

      if (!todaySession) {
        set({ todayStatus: 'not_started', isLoading: false });
        return;
      }

      if (todaySession.wasEmergencyUnlock) {
        set({
          todayStatus: 'bypassed',
          currentSession: todaySession,
          isLoading: false,
        });
        return;
      }

      if (todaySession.completedAt) {
        set({
          todayStatus: 'completed',
          currentSession: todaySession,
          isLoading: false,
        });
        return;
      }

      set({
        todayStatus: 'in_progress',
        currentSession: todaySession,
        isLoading: false,
      });
    } catch (error) {
      console.error('Failed to load today status:', error);
      set({ isLoading: false });
    }
  },

  startSession: async (durationMinutes: number) => {
    const today = getDevotionalDay(DEFAULT_RESET_TIME);
    const session: DevotionSession = {
      id: generateSessionId(),
      date: today,
      startedAt: Date.now(),
      completedAt: null,
      timerDuration: durationMinutes * 60,
      scriptureRead: false,
      scripturePassage: '',
      wasEmergencyUnlock: false,
    };

    set({
      currentSession: session,
      todayStatus: 'in_progress',
      timerSecondsRemaining: durationMinutes * 60,
      scriptureReadComplete: false,
    });

    // Save session
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEYS.SESSIONS);
      const sessions: DevotionSession[] = stored ? JSON.parse(stored) : [];
      sessions.push(session);
      await AsyncStorage.setItem(STORAGE_KEYS.SESSIONS, JSON.stringify(sessions));
    } catch (error) {
      console.error('Failed to save session:', error);
    }
  },

  updateTimer: (seconds: number) => {
    set({ timerSecondsRemaining: seconds });
  },

  completeTimer: () => {
    const { currentSession } = get();
    if (currentSession) {
      set({
        currentSession: {
          ...currentSession,
          timerDuration: currentSession.timerDuration,
        },
        timerSecondsRemaining: 0,
      });
    }
  },

  completeScripture: (passage: BiblePassage) => {
    const { currentSession } = get();
    if (currentSession) {
      set({
        currentSession: {
          ...currentSession,
          scriptureRead: true,
          scripturePassage: passage.reference,
        },
        scriptureReadComplete: true,
      });
    }
  },

  completeSession: async () => {
    const { currentSession } = get();
    if (!currentSession) return;

    const completedSession: DevotionSession = {
      ...currentSession,
      completedAt: Date.now(),
    };

    set({
      currentSession: completedSession,
      todayStatus: 'completed',
    });

    // Update stored session
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEYS.SESSIONS);
      const sessions: DevotionSession[] = stored ? JSON.parse(stored) : [];
      const index = sessions.findIndex((s) => s.id === currentSession.id);
      if (index >= 0) {
        sessions[index] = completedSession;
      } else {
        sessions.push(completedSession);
      }
      await AsyncStorage.setItem(STORAGE_KEYS.SESSIONS, JSON.stringify(sessions));
    } catch (error) {
      console.error('Failed to save completed session:', error);
    }

    // Update streak
    await get().updateStreak(true);
  },

  emergencyUnlock: async () => {
    const { currentSession } = get();

    const today = getDevotionalDay(DEFAULT_RESET_TIME);
    const bypassSession: DevotionSession = currentSession
      ? { ...currentSession, wasEmergencyUnlock: true, completedAt: Date.now() }
      : {
          id: generateSessionId(),
          date: today,
          startedAt: Date.now(),
          completedAt: Date.now(),
          timerDuration: 0,
          scriptureRead: false,
          scripturePassage: '',
          wasEmergencyUnlock: true,
        };

    set({
      currentSession: bypassSession,
      todayStatus: 'bypassed',
    });

    // Save bypass
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEYS.SESSIONS);
      const sessions: DevotionSession[] = stored ? JSON.parse(stored) : [];
      const index = sessions.findIndex((s) => s.id === bypassSession.id);
      if (index >= 0) {
        sessions[index] = bypassSession;
      } else {
        sessions.push(bypassSession);
      }
      await AsyncStorage.setItem(STORAGE_KEYS.SESSIONS, JSON.stringify(sessions));
    } catch (error) {
      console.error('Failed to save bypass session:', error);
    }

    // Reset streak on bypass
    await get().resetStreak();
  },

  loadStreak: async () => {
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEYS.STREAK_DATA);
      if (stored) {
        const streak: StreakData = JSON.parse(stored);

        // Check if streak should be broken
        const today = getDevotionalDay(DEFAULT_RESET_TIME);
        if (
          streak.lastCompletedDate &&
          streak.lastCompletedDate !== today &&
          !areConsecutiveDays(streak.lastCompletedDate, today)
        ) {
          // Streak broken
          const brokenStreak: StreakData = {
            ...streak,
            currentStreak: 0,
          };
          set({ streak: brokenStreak });
          await AsyncStorage.setItem(
            STORAGE_KEYS.STREAK_DATA,
            JSON.stringify(brokenStreak)
          );
          return;
        }

        set({ streak });
      }
    } catch (error) {
      console.error('Failed to load streak:', error);
    }
  },

  updateStreak: async (completed: boolean) => {
    const { streak } = get();
    const today = getDevotionalDay(DEFAULT_RESET_TIME);

    // Already completed today
    if (streak.completedDates.includes(today)) {
      return;
    }

    if (!completed) {
      return;
    }

    const isConsecutive =
      streak.lastCompletedDate &&
      areConsecutiveDays(streak.lastCompletedDate, today);

    const newCurrentStreak = isConsecutive ? streak.currentStreak + 1 : 1;
    const newLongestStreak = Math.max(streak.longestStreak, newCurrentStreak);

    const updatedStreak: StreakData = {
      currentStreak: newCurrentStreak,
      longestStreak: newLongestStreak,
      totalDaysCompleted: streak.totalDaysCompleted + 1,
      completedDates: [...streak.completedDates, today],
      lastCompletedDate: today,
    };

    set({ streak: updatedStreak });

    try {
      await AsyncStorage.setItem(
        STORAGE_KEYS.STREAK_DATA,
        JSON.stringify(updatedStreak)
      );
    } catch (error) {
      console.error('Failed to save streak:', error);
    }
  },

  resetStreak: async () => {
    const { streak } = get();
    const resetStreak: StreakData = {
      ...streak,
      currentStreak: 0,
    };

    set({ streak: resetStreak });

    try {
      await AsyncStorage.setItem(
        STORAGE_KEYS.STREAK_DATA,
        JSON.stringify(resetStreak)
      );
    } catch (error) {
      console.error('Failed to reset streak:', error);
    }
  },

  setTodaysPassage: (passage: BiblePassage) => {
    set({ todaysPassage: passage });
  },
}));
