import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { StepData, AppState } from '../types';
import { STORAGE_KEYS, DEFAULT_STEP_GOAL } from '../utils/constants';
import { getTodayDateString } from '../utils/dateUtils';

interface StepStore {
  // Current state
  currentSteps: number;
  stepGoal: number;
  isUnlocked: boolean;
  lastUpdated: number;
  todayCompleted: boolean;
  isLoading: boolean;
  error: string | null;

  // Step history (last 30 days)
  stepHistory: Record<string, StepData>;

  // Actions
  setCurrentSteps: (steps: number) => void;
  setStepGoal: (goal: number) => void;
  setUnlocked: (unlocked: boolean) => void;
  markTodayCompleted: (wasEmergencyUnlock?: boolean) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  refreshSteps: () => void;

  // History actions
  getStepDataForDate: (date: string) => StepData | undefined;
  getWeeklyAverage: () => number;
  getMonthlyTotal: () => number;
}

const defaultStepData: StepData = {
  date: getTodayDateString(),
  steps: 0,
  goalMet: false,
  unlockedAt: null,
  wasEmergencyUnlock: false,
};

export const useStepStore = create<StepStore>()(
  persist(
    (set, get) => ({
      // Current state
      currentSteps: 0,
      stepGoal: DEFAULT_STEP_GOAL,
      isUnlocked: false,
      lastUpdated: 0,
      todayCompleted: false,
      isLoading: false,
      error: null,

      // Step history
      stepHistory: {},

      // Actions
      setCurrentSteps: (steps) => {
        const { stepGoal, todayCompleted, stepHistory } = get();
        const today = getTodayDateString();

        // Update today's step data
        const todayData = stepHistory[today] || { ...defaultStepData, date: today };
        todayData.steps = steps;

        // Check if goal just met (not already completed)
        const goalJustMet = !todayCompleted && steps >= stepGoal;

        set({
          currentSteps: steps,
          lastUpdated: Date.now(),
          stepHistory: { ...stepHistory, [today]: todayData },
          isUnlocked: todayCompleted || goalJustMet,
        });
      },

      setStepGoal: (goal) => set({ stepGoal: goal }),

      setUnlocked: (unlocked) => set({ isUnlocked: unlocked }),

      markTodayCompleted: (wasEmergencyUnlock = false) => {
        const { stepHistory, currentSteps, stepGoal } = get();
        const today = getTodayDateString();
        const now = Date.now();

        const todayData: StepData = {
          date: today,
          steps: currentSteps,
          goalMet: wasEmergencyUnlock || currentSteps >= stepGoal,
          unlockedAt: now,
          wasEmergencyUnlock,
        };

        set({
          todayCompleted: true,
          isUnlocked: true,
          stepHistory: { ...stepHistory, [today]: todayData },
        });
      },

      setLoading: (loading) => set({ isLoading: loading }),

      setError: (error) => set({ error }),

      refreshSteps: () => {
        // Check if it's a new day
        const today = getTodayDateString();
        const { stepHistory } = get();
        const todayData = stepHistory[today];

        // Reset daily state if new day
        if (!todayData || !todayData.goalMet) {
          set({
            todayCompleted: false,
            isUnlocked: false,
          });
        }
      },

      // History helpers
      getStepDataForDate: (date) => {
        const { stepHistory } = get();
        return stepHistory[date];
      },

      getWeeklyAverage: () => {
        const { stepHistory } = get();
        const dates = Object.keys(stepHistory).slice(-7);
        if (dates.length === 0) return 0;

        const total = dates.reduce((sum, date) => {
          return sum + (stepHistory[date]?.steps || 0);
        }, 0);

        return Math.round(total / dates.length);
      },

      getMonthlyTotal: () => {
        const { stepHistory } = get();
        const dates = Object.keys(stepHistory).slice(-30);

        return dates.reduce((sum, date) => {
          return sum + (stepHistory[date]?.steps || 0);
        }, 0);
      },
    }),
    {
      name: STORAGE_KEYS.STEP_DATA,
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({
        stepHistory: state.stepHistory,
        stepGoal: state.stepGoal,
      }),
    }
  )
);
