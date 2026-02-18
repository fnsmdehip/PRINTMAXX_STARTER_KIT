import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { DailyLog, MewingSession } from '../types';
import { STORAGE_KEYS } from '../utils/constants';
import { getTodayDateString } from '../utils/dateUtils';

interface DailyLogStore {
  // Daily logs
  logs: Record<string, DailyLog>;
  getTodayLog: () => DailyLog;
  updateTodayLog: (updates: Partial<DailyLog>) => void;
  addWater: (ml: number) => void;
  setSodiumLevel: (level: 'low' | 'medium' | 'high') => void;
  setSleepHours: (hours: number) => void;
  completeRoutine: (routineId: string) => void;

  // Mewing sessions
  mewingSessions: MewingSession[];
  currentMewingSession: MewingSession | null;
  startMewingSession: () => void;
  endMewingSession: () => void;
  getTodayMewingMinutes: () => number;
  getTotalMewingMinutes: () => number;
}

const createEmptyLog = (date: string): DailyLog => ({
  date,
  waterIntake: 0,
  sodiumLevel: 'medium',
  sleepHours: 0,
  completedRoutines: [],
  mewingMinutes: 0,
  notes: '',
});

export const useDailyLogStore = create<DailyLogStore>()(
  persist(
    (set, get) => ({
      logs: {},

      getTodayLog: () => {
        const today = getTodayDateString();
        const { logs } = get();
        return logs[today] || createEmptyLog(today);
      },

      updateTodayLog: (updates) => {
        const today = getTodayDateString();
        set((state) => ({
          logs: {
            ...state.logs,
            [today]: {
              ...state.getTodayLog(),
              ...updates,
            },
          },
        }));
      },

      addWater: (ml) => {
        const todayLog = get().getTodayLog();
        get().updateTodayLog({ waterIntake: todayLog.waterIntake + ml });
      },

      setSodiumLevel: (level) => {
        get().updateTodayLog({ sodiumLevel: level });
      },

      setSleepHours: (hours) => {
        get().updateTodayLog({ sleepHours: hours });
      },

      completeRoutine: (routineId) => {
        const todayLog = get().getTodayLog();
        if (!todayLog.completedRoutines.includes(routineId)) {
          get().updateTodayLog({
            completedRoutines: [...todayLog.completedRoutines, routineId],
          });
        }
      },

      // Mewing sessions
      mewingSessions: [],
      currentMewingSession: null,

      startMewingSession: () => {
        const now = new Date();
        set({
          currentMewingSession: {
            id: now.getTime().toString(),
            startTime: now.toISOString(),
            endTime: '',
            duration: 0,
            date: getTodayDateString(),
          },
        });
      },

      endMewingSession: () => {
        const { currentMewingSession, mewingSessions, getTodayLog, updateTodayLog } = get();
        if (!currentMewingSession) return;

        const endTime = new Date();
        const startTime = new Date(currentMewingSession.startTime);
        const duration = Math.floor((endTime.getTime() - startTime.getTime()) / 1000);

        const completedSession: MewingSession = {
          ...currentMewingSession,
          endTime: endTime.toISOString(),
          duration,
        };

        // Update today's mewing minutes
        const todayLog = getTodayLog();
        const additionalMinutes = Math.floor(duration / 60);
        updateTodayLog({ mewingMinutes: todayLog.mewingMinutes + additionalMinutes });

        set({
          mewingSessions: [...mewingSessions, completedSession],
          currentMewingSession: null,
        });
      },

      getTodayMewingMinutes: () => {
        const todayLog = get().getTodayLog();
        return todayLog.mewingMinutes;
      },

      getTotalMewingMinutes: () => {
        const { logs } = get();
        return Object.values(logs).reduce((total, log) => total + log.mewingMinutes, 0);
      },
    }),
    {
      name: STORAGE_KEYS.DAILY_LOGS,
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
