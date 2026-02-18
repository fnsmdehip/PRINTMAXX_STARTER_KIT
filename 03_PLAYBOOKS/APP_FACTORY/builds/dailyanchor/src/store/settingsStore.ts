import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { SettingsState, UserSettings } from '../types';
import { STORAGE_KEYS, DEFAULT_REMINDER_TIME } from '../utils/constants';

const DEFAULT_SETTINGS: UserSettings = {
  reminderTime: DEFAULT_REMINDER_TIME,
  reminderEnabled: true,
  focusArea: null,
  isPremium: false,
  onboardingCompleted: false,
};

export const useSettingsStore = create<SettingsState>((set, get) => ({
  ...DEFAULT_SETTINGS,

  updateSettings: (updates) => {
    set((state) => {
      const newSettings = { ...state, ...updates };
      saveSettings(newSettings);
      return updates;
    });
  },

  setOnboardingComplete: (completed: boolean) => {
    set({ onboardingCompleted: completed });
    saveSettings({ onboardingCompleted: completed });
  },

  loadFromStorage: async () => {
    try {
      const settingsJson = await AsyncStorage.getItem(STORAGE_KEYS.SETTINGS);
      if (settingsJson) {
        const settings: UserSettings = JSON.parse(settingsJson);
        set(settings);
      }
    } catch (error) {
      console.error('Failed to load settings from storage:', error);
    }
  },
}));

async function saveSettings(settings: Partial<SettingsState>): Promise<void> {
  try {
    const currentSettings = await AsyncStorage.getItem(STORAGE_KEYS.SETTINGS);
    const merged = currentSettings
      ? { ...JSON.parse(currentSettings), ...settings }
      : settings;

    // Remove functions before saving
    const toSave: UserSettings = {
      reminderTime: merged.reminderTime,
      reminderEnabled: merged.reminderEnabled,
      focusArea: merged.focusArea,
      isPremium: merged.isPremium,
      onboardingCompleted: merged.onboardingCompleted,
    };

    await AsyncStorage.setItem(STORAGE_KEYS.SETTINGS, JSON.stringify(toSave));
  } catch (error) {
    console.error('Failed to save settings:', error);
  }
}
