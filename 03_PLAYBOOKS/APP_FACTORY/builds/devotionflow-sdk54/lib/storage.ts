// Local Storage utilities for DevotionFlow
// Uses AsyncStorage for persistence

import AsyncStorage from '@react-native-async-storage/async-storage';

// Storage keys
export const STORAGE_KEYS = {
  HAS_LAUNCHED: 'has_launched',
  ONBOARDING_COMPLETE: 'onboarding_complete',
  TRIAL_START_DATE: 'trial_start_date',
  DEVOTION_COUNT: 'devotion_count',
  LAST_DEVOTION_DATE: 'last_devotion_date',
  CURRENT_STREAK: 'current_streak',
  USER_PREFERENCES: 'user_preferences',
  PRAYER_JOURNAL: 'prayer_journal',
  NOTIFICATION_TIME: 'notification_time',
  FAITH_BACKGROUND: 'faith_background',
} as const;

// Generic storage helpers
export const localStore = {
  // String
  getString: async (key: string): Promise<string | null> => {
    try {
      return await AsyncStorage.getItem(key);
    } catch (error) {
      console.error(`Error getting string from storage: ${key}`, error);
      return null;
    }
  },

  setString: async (key: string, value: string): Promise<void> => {
    try {
      await AsyncStorage.setItem(key, value);
    } catch (error) {
      console.error(`Error setting string in storage: ${key}`, error);
    }
  },

  // Number
  getNumber: async (key: string): Promise<number | null> => {
    try {
      const value = await AsyncStorage.getItem(key);
      return value ? parseFloat(value) : null;
    } catch (error) {
      console.error(`Error getting number from storage: ${key}`, error);
      return null;
    }
  },

  setNumber: async (key: string, value: number): Promise<void> => {
    try {
      await AsyncStorage.setItem(key, value.toString());
    } catch (error) {
      console.error(`Error setting number in storage: ${key}`, error);
    }
  },

  // Boolean
  getBoolean: async (key: string): Promise<boolean | null> => {
    try {
      const value = await AsyncStorage.getItem(key);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.error(`Error getting boolean from storage: ${key}`, error);
      return null;
    }
  },

  setBoolean: async (key: string, value: boolean): Promise<void> => {
    try {
      await AsyncStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(`Error setting boolean in storage: ${key}`, error);
    }
  },

  // Object (JSON)
  getObject: async <T>(key: string): Promise<T | null> => {
    try {
      const json = await AsyncStorage.getItem(key);
      if (!json) return null;
      return JSON.parse(json) as T;
    } catch (error) {
      console.error(`Error getting object from storage: ${key}`, error);
      return null;
    }
  },

  setObject: async <T>(key: string, value: T): Promise<void> => {
    try {
      await AsyncStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(`Error setting object in storage: ${key}`, error);
    }
  },

  // Delete
  delete: async (key: string): Promise<void> => {
    try {
      await AsyncStorage.removeItem(key);
    } catch (error) {
      console.error(`Error deleting from storage: ${key}`, error);
    }
  },

  // Clear all
  clearAll: async (): Promise<void> => {
    try {
      await AsyncStorage.clear();
    } catch (error) {
      console.error('Error clearing storage:', error);
    }
  },

  // Check if key exists
  contains: async (key: string): Promise<boolean> => {
    try {
      const value = await AsyncStorage.getItem(key);
      return value !== null;
    } catch (error) {
      console.error(`Error checking storage: ${key}`, error);
      return false;
    }
  },
};
