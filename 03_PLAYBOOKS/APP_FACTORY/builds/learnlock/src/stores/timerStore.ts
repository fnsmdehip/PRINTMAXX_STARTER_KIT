import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { TimerState, TimerData, StudySession } from '../types';
import { STORAGE_KEYS, DEFAULT_WORK_DURATION, DEFAULT_BREAK_DURATION } from '../utils/constants';
import { getTodayDateString } from '../utils/dateUtils';

interface TimerStore {
  // Timer state
  timerState: TimerState;
  remainingSeconds: number;
  totalSeconds: number;
  currentSessionType: 'work' | 'break';
  sessionStartTime: number | null;

  // Settings
  workDuration: number; // minutes
  breakDuration: number; // minutes

  // Today's sessions
  todaySessions: StudySession[];
  todayStudyTime: number; // seconds

  // Actions
  startSession: () => void;
  pauseSession: () => void;
  resumeSession: () => void;
  endSession: (completed: boolean) => void;
  startBreak: () => void;
  skipBreak: () => void;
  tick: () => void;
  setWorkDuration: (minutes: number) => void;
  setBreakDuration: (minutes: number) => void;
  resetDaily: () => void;

  // Helpers
  getCurrentSession: () => StudySession | null;
  getProgress: () => number;
}

const generateSessionId = (): string => {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};

export const useTimerStore = create<TimerStore>()(
  persist(
    (set, get) => ({
      // Initial state
      timerState: 'idle',
      remainingSeconds: DEFAULT_WORK_DURATION * 60,
      totalSeconds: DEFAULT_WORK_DURATION * 60,
      currentSessionType: 'work',
      sessionStartTime: null,

      workDuration: DEFAULT_WORK_DURATION,
      breakDuration: DEFAULT_BREAK_DURATION,

      todaySessions: [],
      todayStudyTime: 0,

      // Start a new study session
      startSession: () => {
        const { workDuration } = get();
        const totalSeconds = workDuration * 60;

        const newSession: StudySession = {
          id: generateSessionId(),
          date: getTodayDateString(),
          startTime: Date.now(),
          endTime: null,
          duration: 0,
          completed: false,
          wasInterrupted: false,
        };

        set({
          timerState: 'studying',
          remainingSeconds: totalSeconds,
          totalSeconds,
          currentSessionType: 'work',
          sessionStartTime: Date.now(),
          todaySessions: [...get().todaySessions, newSession],
        });
      },

      // Pause current session
      pauseSession: () => {
        const { timerState } = get();
        if (timerState !== 'studying') return;

        set({ timerState: 'paused' });
      },

      // Resume paused session
      resumeSession: () => {
        const { timerState } = get();
        if (timerState !== 'paused') return;

        set({ timerState: 'studying' });
      },

      // End session (either completed or interrupted)
      endSession: (completed: boolean) => {
        const { todaySessions, sessionStartTime, totalSeconds, remainingSeconds } = get();

        if (todaySessions.length === 0) return;

        const currentSession = todaySessions[todaySessions.length - 1];
        const duration = sessionStartTime
          ? Math.floor((Date.now() - sessionStartTime) / 1000)
          : totalSeconds - remainingSeconds;

        const updatedSession: StudySession = {
          ...currentSession,
          endTime: Date.now(),
          duration,
          completed,
          wasInterrupted: !completed,
        };

        const updatedSessions = [...todaySessions.slice(0, -1), updatedSession];
        const todayStudyTime = updatedSessions
          .filter((s) => s.date === getTodayDateString())
          .reduce((sum, s) => sum + s.duration, 0);

        set({
          timerState: 'idle',
          todaySessions: updatedSessions,
          todayStudyTime,
          sessionStartTime: null,
        });
      },

      // Start break timer
      startBreak: () => {
        const { breakDuration } = get();
        const totalSeconds = breakDuration * 60;

        set({
          timerState: 'break',
          remainingSeconds: totalSeconds,
          totalSeconds,
          currentSessionType: 'break',
        });
      },

      // Skip break and return to idle
      skipBreak: () => {
        const { workDuration } = get();
        set({
          timerState: 'idle',
          remainingSeconds: workDuration * 60,
          totalSeconds: workDuration * 60,
          currentSessionType: 'work',
        });
      },

      // Called every second by timer
      tick: () => {
        const { timerState, remainingSeconds, currentSessionType } = get();

        if (timerState !== 'studying' && timerState !== 'break') return;
        if (remainingSeconds <= 0) return;

        const newRemaining = remainingSeconds - 1;

        if (newRemaining <= 0) {
          if (currentSessionType === 'work') {
            // Work session complete
            get().endSession(true);
          } else {
            // Break complete
            get().skipBreak();
          }
          return;
        }

        set({ remainingSeconds: newRemaining });
      },

      // Update work duration
      setWorkDuration: (minutes: number) => {
        const { timerState, currentSessionType } = get();
        const newTotalSeconds = minutes * 60;

        set({
          workDuration: minutes,
          // Only update current timer if idle and on work session
          ...(timerState === 'idle' && currentSessionType === 'work'
            ? { remainingSeconds: newTotalSeconds, totalSeconds: newTotalSeconds }
            : {}),
        });
      },

      // Update break duration
      setBreakDuration: (minutes: number) => {
        set({ breakDuration: minutes });
      },

      // Reset daily data (call at midnight or app launch on new day)
      resetDaily: () => {
        const { todaySessions, workDuration } = get();
        const today = getTodayDateString();

        // Filter to only today's sessions
        const todayOnly = todaySessions.filter((s) => s.date === today);
        const todayStudyTime = todayOnly.reduce((sum, s) => sum + s.duration, 0);

        set({
          todaySessions: todayOnly,
          todayStudyTime,
          timerState: 'idle',
          remainingSeconds: workDuration * 60,
          totalSeconds: workDuration * 60,
          currentSessionType: 'work',
          sessionStartTime: null,
        });
      },

      // Get current session
      getCurrentSession: () => {
        const { todaySessions, timerState } = get();
        if (timerState === 'idle' || todaySessions.length === 0) return null;
        return todaySessions[todaySessions.length - 1];
      },

      // Get progress (0-1)
      getProgress: () => {
        const { remainingSeconds, totalSeconds } = get();
        if (totalSeconds === 0) return 0;
        return (totalSeconds - remainingSeconds) / totalSeconds;
      },
    }),
    {
      name: STORAGE_KEYS.TIMER_DATA,
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({
        workDuration: state.workDuration,
        breakDuration: state.breakDuration,
        todaySessions: state.todaySessions,
        todayStudyTime: state.todayStudyTime,
      }),
    }
  )
);
