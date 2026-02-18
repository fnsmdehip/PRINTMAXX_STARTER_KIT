import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';

export interface DevotionSession {
  id: string;
  date: string;
  startedAt: number;
  completedAt: number | null;
  timerDuration: number;
  scriptureRead: boolean;
  scripturePassage: string | null;
  wasEmergencyUnlock: boolean;
}

interface DevotionState {
  currentStreak: number;
  longestStreak: number;
  totalDaysCompleted: number;
  completedDates: string[];
  lastCompletedDate: string | null;
  sessions: DevotionSession[];
  currentSession: DevotionSession | null;

  // Actions
  startSession: () => void;
  completeSession: (timerCompleted: boolean, scriptureRead: boolean, passage?: string) => void;
  emergencyUnlock: () => void;
  isTodayCompleted: () => boolean;
  hydrate: () => Promise<void>;
}

const STORAGE_KEY = 'prayerlock_devotion';

const getTodayDate = () => new Date().toISOString().split('T')[0];

const generateId = () => Math.random().toString(36).substring(2, 15);

export const useDevotionStore = create<DevotionState>((set, get) => ({
  currentStreak: 0,
  longestStreak: 0,
  totalDaysCompleted: 0,
  completedDates: [],
  lastCompletedDate: null,
  sessions: [],
  currentSession: null,

  startSession: () => {
    const session: DevotionSession = {
      id: generateId(),
      date: getTodayDate(),
      startedAt: Date.now(),
      completedAt: null,
      timerDuration: 0,
      scriptureRead: false,
      scripturePassage: null,
      wasEmergencyUnlock: false,
    };
    set({ currentSession: session });
  },

  completeSession: (timerCompleted, scriptureRead, passage) => {
    const state = get();
    const today = getTodayDate();

    if (!state.currentSession) {
      // Start a new session if none exists
      const session: DevotionSession = {
        id: generateId(),
        date: today,
        startedAt: Date.now(),
        completedAt: Date.now(),
        timerDuration: 0,
        scriptureRead,
        scripturePassage: passage || null,
        wasEmergencyUnlock: false,
      };

      const alreadyCompleted = state.completedDates.includes(today);

      if (!alreadyCompleted) {
        const newCompletedDates = [...state.completedDates, today];
        const newStreak = calculateStreak(newCompletedDates);
        const newLongest = Math.max(state.longestStreak, newStreak);

        set({
          sessions: [...state.sessions, session],
          currentSession: null,
          completedDates: newCompletedDates,
          lastCompletedDate: today,
          currentStreak: newStreak,
          longestStreak: newLongest,
          totalDaysCompleted: state.totalDaysCompleted + 1,
        });
      } else {
        set({
          sessions: [...state.sessions, session],
          currentSession: null,
        });
      }
    } else {
      const completedSession: DevotionSession = {
        ...state.currentSession,
        completedAt: Date.now(),
        timerDuration: Math.floor((Date.now() - state.currentSession.startedAt) / 1000),
        scriptureRead,
        scripturePassage: passage || null,
      };

      const alreadyCompleted = state.completedDates.includes(today);

      if (!alreadyCompleted) {
        const newCompletedDates = [...state.completedDates, today];
        const newStreak = calculateStreak(newCompletedDates);
        const newLongest = Math.max(state.longestStreak, newStreak);

        set({
          sessions: [...state.sessions, completedSession],
          currentSession: null,
          completedDates: newCompletedDates,
          lastCompletedDate: today,
          currentStreak: newStreak,
          longestStreak: newLongest,
          totalDaysCompleted: state.totalDaysCompleted + 1,
        });
      } else {
        set({
          sessions: [...state.sessions, completedSession],
          currentSession: null,
        });
      }
    }

    persistState(get());
  },

  emergencyUnlock: () => {
    const state = get();
    const today = getTodayDate();

    const session: DevotionSession = {
      id: generateId(),
      date: today,
      startedAt: Date.now(),
      completedAt: Date.now(),
      timerDuration: 0,
      scriptureRead: false,
      scripturePassage: null,
      wasEmergencyUnlock: true,
    };

    // Reset streak but keep other stats
    set({
      sessions: [...state.sessions, session],
      currentSession: null,
      currentStreak: 0,
      lastCompletedDate: today,
    });

    persistState(get());
  },

  isTodayCompleted: () => {
    const state = get();
    const today = getTodayDate();
    return state.completedDates.includes(today);
  },

  hydrate: async () => {
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);

        // Recalculate streak based on stored dates
        const newStreak = calculateStreak(parsed.completedDates || []);

        set({
          currentStreak: newStreak,
          longestStreak: parsed.longestStreak ?? 0,
          totalDaysCompleted: parsed.totalDaysCompleted ?? 0,
          completedDates: parsed.completedDates ?? [],
          lastCompletedDate: parsed.lastCompletedDate ?? null,
          sessions: parsed.sessions ?? [],
          currentSession: null,
        });
      }
    } catch (error) {
      console.error('Failed to hydrate devotion store:', error);
    }
  },
}));

function calculateStreak(completedDates: string[]): number {
  if (completedDates.length === 0) return 0;

  const sorted = [...completedDates].sort().reverse();
  const today = getTodayDate();
  const yesterday = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString().split('T')[0];

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

async function persistState(state: DevotionState) {
  try {
    const toStore = {
      currentStreak: state.currentStreak,
      longestStreak: state.longestStreak,
      totalDaysCompleted: state.totalDaysCompleted,
      completedDates: state.completedDates,
      lastCompletedDate: state.lastCompletedDate,
      sessions: state.sessions,
    };
    await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(toStore));
  } catch (error) {
    console.error('Failed to persist devotion store:', error);
  }
}
