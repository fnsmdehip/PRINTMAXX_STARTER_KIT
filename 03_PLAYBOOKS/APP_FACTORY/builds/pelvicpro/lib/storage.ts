// Local Storage utilities for FemFit
// Uses MMKV for performance, falls back to AsyncStorage

import { MMKV } from 'react-native-mmkv';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Initialize MMKV instance
export const storage = new MMKV({
  id: 'femfit-storage',
});

// Storage keys
export const STORAGE_KEYS = {
  HAS_LAUNCHED: 'has_launched',
  ONBOARDING_COMPLETE: 'onboarding_complete',
  TRIAL_START_DATE: 'trial_start_date',
  WORKOUT_COUNT: 'workout_count',
  LAST_WORKOUT_DATE: 'last_workout_date',
  CURRENT_STREAK: 'current_streak',
  USER_PREFERENCES: 'user_preferences',
} as const;

// Generic storage helpers
export const localStore = {
  // String
  getString: (key: string): string | undefined => {
    return storage.getString(key);
  },

  setString: (key: string, value: string): void => {
    storage.set(key, value);
  },

  // Number
  getNumber: (key: string): number | undefined => {
    return storage.getNumber(key);
  },

  setNumber: (key: string, value: number): void => {
    storage.set(key, value);
  },

  // Boolean
  getBoolean: (key: string): boolean | undefined => {
    return storage.getBoolean(key);
  },

  setBoolean: (key: string, value: boolean): void => {
    storage.set(key, value);
  },

  // Object (JSON)
  getObject: <T>(key: string): T | undefined => {
    const json = storage.getString(key);
    if (!json) return undefined;
    try {
      return JSON.parse(json) as T;
    } catch {
      return undefined;
    }
  },

  setObject: <T>(key: string, value: T): void => {
    storage.set(key, JSON.stringify(value));
  },

  // Delete
  delete: (key: string): void => {
    storage.delete(key);
  },

  // Clear all
  clearAll: (): void => {
    storage.clearAll();
  },

  // Check if key exists
  contains: (key: string): boolean => {
    return storage.contains(key);
  },
};

// Zustand persist storage adapter for MMKV
export const zustandStorage = {
  getItem: (name: string): string | null => {
    const value = storage.getString(name);
    return value ?? null;
  },
  setItem: (name: string, value: string): void => {
    storage.set(name, value);
  },
  removeItem: (name: string): void => {
    storage.delete(name);
  },
};

// Migration helper: Move data from AsyncStorage to MMKV
export async function migrateFromAsyncStorage(): Promise<void> {
  try {
    const keys = await AsyncStorage.getAllKeys();

    for (const key of keys) {
      // Skip if already migrated
      if (storage.contains(key)) continue;

      const value = await AsyncStorage.getItem(key);
      if (value) {
        storage.set(key, value);
        // Optionally remove from AsyncStorage after migration
        // await AsyncStorage.removeItem(key);
      }
    }

    console.log('Migration from AsyncStorage complete');
  } catch (error) {
    console.error('Migration error:', error);
  }
}
