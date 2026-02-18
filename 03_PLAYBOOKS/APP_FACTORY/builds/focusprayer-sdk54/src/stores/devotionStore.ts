/**
 * Devotion Store
 * Manages daily devotion status, streak tracking, and sessions
 */

import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { APP_CONFIG } from '../utils/constants';
import { getTodayDate, getYesterdayDate } from '../utils/dateUtils';

export type DevotionStatus = 'not_started' | 'in_progress' | 'completed' | 'bypassed';

export interface DailyPassage {
  reference: string;
  text: string;
  translation: string;
}

export interface DevotionSession {
  id: string;
  date: string;
  startedAt: number;
  completedAt: number | null;
  timerDuration: number;
  targetDuration: number;
  scriptureRead: boolean;
  passage: DailyPassage | null;
  wasEmergencyUnlock: boolean;
}

export interface StreakData {
  currentStreak: number;
  longestStreak: number;
  totalDaysCompleted: number;
  lastCompletedDate: string | null;
}

interface DevotionState {
  todayStatus: DevotionStatus;
  streak: StreakData;
  completedDates: string[];
  sessions: DevotionSession[];
  currentSession: DevotionSession | null;
  todaysPassage: DailyPassage | null;

  // Actions
  loadTodayStatus: () => Promise<void>;
  loadStreak: () => Promise<void>;
  setTodaysPassage: (passage: DailyPassage) => void;
  startSession: (durationMinutes: number) => void;
  completeTimer: (duration: number) => void;
  completeScripture: () => void;
  completeSession: () => Promise<void>;
  emergencyUnlock: () => Promise<void>;
}

const DEFAULT_STREAK: StreakData = {
  currentStreak: 0,
  longestStreak: 0,
  totalDaysCompleted: 0,
  lastCompletedDate: null,
};

const generateId = () => Math.random().toString(36).substring(2, 15);

function calculateStreak(completedDates: string[]): number {
  if (completedDates.length === 0) return 0;

  const sorted = [...completedDates].sort().reverse();
  const today = getTodayDate();
  const yesterday = getYesterdayDate();

  // Streak must include today or yesterday
  if (sorted[0] !== today && sorted[0] !== yesterday) {
    return 0;
  }

  let streak = 1;
  let currentDate = new Date(sorted[0]);

  for (let i = 1; i < sorted.length; i++) {
    const prevDate = new Date(currentDate);
    prevDate.setDate(prevDate.getDate() - 1);
    const expectedDate = prevDate.toISOString().split('T')[0];

    if (sorted[i] === expectedDate) {
      streak++;
      currentDate = prevDate;
    } else {
      break;
    }
  }

  return streak;
}

export const useDevotionStore = create<DevotionState>((set, get) => ({
  todayStatus: 'not_started',
  streak: DEFAULT_STREAK,
  completedDates: [],
  sessions: [],
  currentSession: null,
  todaysPassage: null,

  loadTodayStatus: async () => {
    try {
      const stored = await AsyncStorage.getItem(APP_CONFIG.storageKeys.devotion);
      if (stored) {
        const parsed = JSON.parse(stored);
        const today = getTodayDate();

        // Check today's status based on completed dates and sessions
        const todayCompleted = parsed.completedDates?.includes(today);
        const todayBypassed = parsed.sessions?.some(
          (s: DevotionSession) => s.date === today && s.wasEmergencyUnlock
        );

        let status: DevotionStatus = 'not_started';
        if (todayCompleted) {
          status = todayBypassed ? 'bypassed' : 'completed';
        }

        set({
          todayStatus: status,
          completedDates: parsed.completedDates || [],
          sessions: parsed.sessions || [],
        });
      }
    } catch (error) {
      console.error('Failed to load today status:', error);
    }
  },

  loadStreak: async () => {
    try {
      const stored = await AsyncStorage.getItem(APP_CONFIG.storageKeys.devotion);
      if (stored) {
        const parsed = JSON.parse(stored);
        const completedDates = parsed.completedDates || [];

        // Recalculate streak
        const currentStreak = calculateStreak(completedDates);

        set({
          streak: {
            currentStreak,
            longestStreak: parsed.longestStreak || currentStreak,
            totalDaysCompleted: completedDates.length,
            lastCompletedDate: parsed.lastCompletedDate || null,
          },
          completedDates,
        });
      }
    } catch (error) {
      console.error('Failed to load streak:', error);
    }
  },

  setTodaysPassage: (passage) => {
    set({ todaysPassage: passage });
  },

  startSession: (durationMinutes) => {
    const session: DevotionSession = {
      id: generateId(),
      date: getTodayDate(),
      startedAt: Date.now(),
      completedAt: null,
      timerDuration: 0,
      targetDuration: durationMinutes * 60,
      scriptureRead: false,
      passage: null,
      wasEmergencyUnlock: false,
    };

    set({
      currentSession: session,
      todayStatus: 'in_progress',
    });
  },

  completeTimer: (duration) => {
    const { currentSession } = get();
    if (currentSession) {
      set({
        currentSession: {
          ...currentSession,
          timerDuration: duration,
        },
      });
    }
  },

  completeScripture: () => {
    const { currentSession, todaysPassage } = get();
    if (currentSession) {
      set({
        currentSession: {
          ...currentSession,
          scriptureRead: true,
          passage: todaysPassage,
        },
      });
    }
  },

  completeSession: async () => {
    const state = get();
    const { currentSession, completedDates, streak, sessions } = state;

    if (!currentSession) return;

    const today = getTodayDate();
    const alreadyCompleted = completedDates.includes(today);

    const completedSession: DevotionSession = {
      ...currentSession,
      completedAt: Date.now(),
    };

    const newSessions = [...sessions, completedSession];
    let newCompletedDates = completedDates;
    let newStreak = { ...streak };

    if (!alreadyCompleted) {
      newCompletedDates = [...completedDates, today];
      const currentStreakValue = calculateStreak(newCompletedDates);

      newStreak = {
        currentStreak: currentStreakValue,
        longestStreak: Math.max(streak.longestStreak, currentStreakValue),
        totalDaysCompleted: streak.totalDaysCompleted + 1,
        lastCompletedDate: today,
      };
    }

    set({
      todayStatus: 'completed',
      currentSession: null,
      sessions: newSessions,
      completedDates: newCompletedDates,
      streak: newStreak,
    });

    // Persist
    try {
      await AsyncStorage.setItem(
        APP_CONFIG.storageKeys.devotion,
        JSON.stringify({
          completedDates: newCompletedDates,
          sessions: newSessions,
          longestStreak: newStreak.longestStreak,
          lastCompletedDate: newStreak.lastCompletedDate,
        })
      );
    } catch (error) {
      console.error('Failed to save devotion state:', error);
    }
  },

  emergencyUnlock: async () => {
    const state = get();
    const today = getTodayDate();

    const session: DevotionSession = {
      id: generateId(),
      date: today,
      startedAt: Date.now(),
      completedAt: Date.now(),
      timerDuration: 0,
      targetDuration: 0,
      scriptureRead: false,
      passage: null,
      wasEmergencyUnlock: true,
    };

    const newSessions = [...state.sessions, session];

    // Reset streak but mark today as handled
    set({
      todayStatus: 'bypassed',
      currentSession: null,
      sessions: newSessions,
      streak: {
        ...state.streak,
        currentStreak: 0,
        lastCompletedDate: today,
      },
    });

    // Persist
    try {
      await AsyncStorage.setItem(
        APP_CONFIG.storageKeys.devotion,
        JSON.stringify({
          completedDates: state.completedDates,
          sessions: newSessions,
          longestStreak: state.streak.longestStreak,
          lastCompletedDate: today,
        })
      );
    } catch (error) {
      console.error('Failed to save emergency unlock:', error);
    }
  },
}));
