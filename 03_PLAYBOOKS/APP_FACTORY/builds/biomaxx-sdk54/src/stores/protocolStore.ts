import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Protocol, ProtocolLog, ActiveSession, DailyLog } from '../types';
import { DEFAULT_PROTOCOLS } from '../utils/constants';
import { getToday } from '../utils/dateUtils';

interface ProtocolState {
  protocols: Protocol[];
  logs: ProtocolLog[];
  activeSession: ActiveSession | null;
  dailyLogs: Record<string, DailyLog>;

  // Protocol actions
  getProtocol: (id: string) => Protocol | undefined;
  getProtocolsByCategory: (category: string) => Protocol[];

  // Logging actions
  logProtocol: (protocolId: string, value: number, notes?: string) => void;
  getTodayLog: (protocolId: string) => number;
  getTodayProgress: (protocolId: string) => number;

  // Session actions
  startSession: (protocolId: string) => void;
  pauseSession: () => void;
  resumeSession: () => void;
  endSession: () => number;
  getSessionDuration: () => number;

  // Stats
  getDailyLongevityScore: () => number;
  getProtocolStreak: (protocolId: string) => number;
  getTotalSessionsForProtocol: (protocolId: string) => number;

  // Reset
  reset: () => void;
}

export const useProtocolStore = create<ProtocolState>()(
  persist(
    (set, get) => ({
      protocols: DEFAULT_PROTOCOLS as unknown as Protocol[],
      logs: [],
      activeSession: null,
      dailyLogs: {},

      getProtocol: (id) => {
        return get().protocols.find((p) => p.id === id);
      },

      getProtocolsByCategory: (category) => {
        return get().protocols.filter((p) => p.category === category);
      },

      logProtocol: (protocolId, value, notes) => {
        const today = getToday();
        const newLog: ProtocolLog = {
          protocolId,
          date: today,
          value,
          timestamp: Date.now(),
          notes,
        };

        set((state) => {
          const existingTodayLog = state.logs.find(
            (l) => l.protocolId === protocolId && l.date === today
          );

          let updatedLogs: ProtocolLog[];
          if (existingTodayLog) {
            updatedLogs = state.logs.map((l) =>
              l.protocolId === protocolId && l.date === today
                ? { ...l, value: l.value + value, timestamp: Date.now() }
                : l
            );
          } else {
            updatedLogs = [...state.logs, newLog];
          }

          // Update daily logs
          const protocol = state.protocols.find((p) => p.id === protocolId);
          const currentDailyLog = state.dailyLogs[today] || {
            date: today,
            protocols: {},
            longevityScore: 0,
          };

          const updatedProtocols = {
            ...currentDailyLog.protocols,
            [protocolId]: (currentDailyLog.protocols[protocolId] || 0) + value,
          };

          // Calculate longevity score
          let totalProgress = 0;
          let protocolCount = 0;
          state.protocols.forEach((p) => {
            if (updatedProtocols[p.id] !== undefined) {
              const progress = Math.min(
                (updatedProtocols[p.id] / p.dailyGoal) * 100,
                100
              );
              totalProgress += progress;
              protocolCount++;
            }
          });

          const longevityScore =
            protocolCount > 0 ? Math.round(totalProgress / protocolCount) : 0;

          return {
            logs: updatedLogs,
            dailyLogs: {
              ...state.dailyLogs,
              [today]: {
                ...currentDailyLog,
                protocols: updatedProtocols,
                longevityScore,
              },
            },
          };
        });
      },

      getTodayLog: (protocolId) => {
        const today = getToday();
        const log = get().logs.find(
          (l) => l.protocolId === protocolId && l.date === today
        );
        return log?.value || 0;
      },

      getTodayProgress: (protocolId) => {
        const protocol = get().getProtocol(protocolId);
        if (!protocol) return 0;
        const todayValue = get().getTodayLog(protocolId);
        return Math.min((todayValue / protocol.dailyGoal) * 100, 100);
      },

      startSession: (protocolId) => {
        set({
          activeSession: {
            protocolId,
            startTime: Date.now(),
            isPaused: false,
          },
        });
      },

      pauseSession: () => {
        set((state) => ({
          activeSession: state.activeSession
            ? {
                ...state.activeSession,
                isPaused: true,
                pausedTime: Date.now(),
              }
            : null,
        }));
      },

      resumeSession: () => {
        set((state) => {
          if (!state.activeSession || !state.activeSession.pausedTime) {
            return state;
          }
          const pausedDuration = Date.now() - state.activeSession.pausedTime;
          return {
            activeSession: {
              ...state.activeSession,
              startTime: state.activeSession.startTime + pausedDuration,
              isPaused: false,
              pausedTime: undefined,
            },
          };
        });
      },

      endSession: () => {
        const session = get().activeSession;
        if (!session) return 0;

        const duration = get().getSessionDuration();
        const protocol = get().getProtocol(session.protocolId);

        if (protocol) {
          const value =
            protocol.unit === 'hours'
              ? duration / 60
              : protocol.unit === 'minutes'
              ? duration
              : 1;
          get().logProtocol(session.protocolId, value);
        }

        set({ activeSession: null });
        return duration;
      },

      getSessionDuration: () => {
        const session = get().activeSession;
        if (!session) return 0;

        if (session.isPaused && session.pausedTime) {
          return Math.floor((session.pausedTime - session.startTime) / 60000);
        }
        return Math.floor((Date.now() - session.startTime) / 60000);
      },

      getDailyLongevityScore: () => {
        const today = getToday();
        const dailyLog = get().dailyLogs[today];
        if (!dailyLog) return 0;

        const protocols = get().protocols;
        let totalProgress = 0;
        let activeProtocols = 0;

        protocols.forEach((p) => {
          const value = dailyLog.protocols[p.id];
          if (value !== undefined && value > 0) {
            const progress = Math.min((value / p.dailyGoal) * 100, 100);
            totalProgress += progress;
            activeProtocols++;
          }
        });

        if (activeProtocols === 0) return 0;
        return Math.round(totalProgress / activeProtocols);
      },

      getProtocolStreak: (protocolId) => {
        const logs = get().logs.filter((l) => l.protocolId === protocolId);
        const logDates = new Set(logs.map((l) => l.date));

        let streak = 0;
        const today = new Date();

        for (let i = 0; i < 365; i++) {
          const date = new Date(today);
          date.setDate(date.getDate() - i);
          const dateStr = date.toISOString().split('T')[0];

          if (logDates.has(dateStr)) {
            streak++;
          } else if (i > 0) {
            break;
          }
        }

        return streak;
      },

      getTotalSessionsForProtocol: (protocolId) => {
        return get().logs.filter((l) => l.protocolId === protocolId).length;
      },

      reset: () =>
        set({
          protocols: DEFAULT_PROTOCOLS as unknown as Protocol[],
          logs: [],
          activeSession: null,
          dailyLogs: {},
        }),
    }),
    {
      name: 'biomaxx-protocol-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
