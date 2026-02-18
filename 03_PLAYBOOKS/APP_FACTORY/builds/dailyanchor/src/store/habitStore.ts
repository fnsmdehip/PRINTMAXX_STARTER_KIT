import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Habit, HabitCompletion, HabitState } from '../types';
import { STORAGE_KEYS, DEFAULT_HABITS } from '../utils/constants';
import { getToday } from '../utils/dateUtils';

function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

export const useHabitStore = create<HabitState>((set, get) => ({
  habits: [],
  completions: [],
  todayHabits: [],

  addHabit: (habitData) => {
    const habit: Habit = {
      ...habitData,
      id: generateId(),
      createdAt: new Date().toISOString(),
    };

    set((state) => {
      const newHabits = [...state.habits, habit];
      saveHabits(newHabits);
      return { habits: newHabits };
    });
  },

  removeHabit: (id) => {
    set((state) => {
      const newHabits = state.habits.filter((h) => h.id !== id);
      saveHabits(newHabits);
      return { habits: newHabits };
    });
  },

  toggleHabitCompletion: (habitId, date) => {
    set((state) => {
      const existingCompletion = state.completions.find(
        (c) => c.habitId === habitId && c.date === date
      );

      let newCompletions: HabitCompletion[];

      if (existingCompletion) {
        // Remove completion
        newCompletions = state.completions.filter(
          (c) => !(c.habitId === habitId && c.date === date)
        );
      } else {
        // Add completion
        const completion: HabitCompletion = {
          habitId,
          date,
          completedAt: new Date().toISOString(),
        };
        newCompletions = [...state.completions, completion];
      }

      saveCompletions(newCompletions);
      return { completions: newCompletions };
    });
  },

  isHabitCompleted: (habitId, date) => {
    const { completions } = get();
    return completions.some((c) => c.habitId === habitId && c.date === date);
  },

  getCompletionsForDate: (date) => {
    const { completions } = get();
    return completions.filter((c) => c.date === date);
  },

  loadFromStorage: async () => {
    try {
      const [habitsJson, completionsJson] = await Promise.all([
        AsyncStorage.getItem(STORAGE_KEYS.HABITS),
        AsyncStorage.getItem(STORAGE_KEYS.COMPLETIONS),
      ]);

      let habits: Habit[] = habitsJson ? JSON.parse(habitsJson) : [];
      const completions: HabitCompletion[] = completionsJson
        ? JSON.parse(completionsJson)
        : [];

      // Initialize with default habits if empty
      if (habits.length === 0) {
        habits = DEFAULT_HABITS.map((h) => ({
          ...h,
          id: generateId(),
          createdAt: new Date().toISOString(),
        }));
        await saveHabits(habits);
      }

      set({ habits, completions });
    } catch (error) {
      console.error('Failed to load habits from storage:', error);
    }
  },
}));

async function saveHabits(habits: Habit[]): Promise<void> {
  try {
    await AsyncStorage.setItem(STORAGE_KEYS.HABITS, JSON.stringify(habits));
  } catch (error) {
    console.error('Failed to save habits:', error);
  }
}

async function saveCompletions(completions: HabitCompletion[]): Promise<void> {
  try {
    await AsyncStorage.setItem(
      STORAGE_KEYS.COMPLETIONS,
      JSON.stringify(completions)
    );
  } catch (error) {
    console.error('Failed to save completions:', error);
  }
}
