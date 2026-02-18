import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';

export interface UserSettings {
  blockedApps: string[];
  devotionDurationMinutes: number;
  dailyResetTime: string;
  requireScripture: boolean;
  requireTimer: boolean;
  emergencyUnlockEnabled: boolean;
  notificationsEnabled: boolean;
}

interface UserState {
  hasCompletedOnboarding: boolean;
  isSubscribed: boolean;
  isTrialActive: boolean;
  trialEndsAt: number | null;
  settings: UserSettings;

  // Actions
  setHasCompletedOnboarding: (value: boolean) => void;
  setIsSubscribed: (value: boolean) => void;
  startTrial: () => void;
  updateSettings: (settings: Partial<UserSettings>) => void;
  hydrate: () => Promise<void>;
}

const DEFAULT_SETTINGS: UserSettings = {
  blockedApps: [],
  devotionDurationMinutes: 10,
  dailyResetTime: '05:00',
  requireScripture: true,
  requireTimer: true,
  emergencyUnlockEnabled: true,
  notificationsEnabled: true,
};

const STORAGE_KEY = 'prayerlock_user';

export const useUserStore = create<UserState>((set, get) => ({
  hasCompletedOnboarding: false,
  isSubscribed: false,
  isTrialActive: false,
  trialEndsAt: null,
  settings: DEFAULT_SETTINGS,

  setHasCompletedOnboarding: (value) => {
    set({ hasCompletedOnboarding: value });
    persistState(get());
  },

  setIsSubscribed: (value) => {
    set({ isSubscribed: value });
    persistState(get());
  },

  startTrial: () => {
    const trialEndsAt = Date.now() + 3 * 24 * 60 * 60 * 1000; // 3 days
    set({ isTrialActive: true, trialEndsAt });
    persistState(get());
  },

  updateSettings: (newSettings) => {
    set((state) => ({
      settings: { ...state.settings, ...newSettings },
    }));
    persistState(get());
  },

  hydrate: async () => {
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        set({
          hasCompletedOnboarding: parsed.hasCompletedOnboarding ?? false,
          isSubscribed: parsed.isSubscribed ?? false,
          isTrialActive: parsed.isTrialActive ?? false,
          trialEndsAt: parsed.trialEndsAt ?? null,
          settings: { ...DEFAULT_SETTINGS, ...parsed.settings },
        });
      }
    } catch (error) {
      console.error('Failed to hydrate user store:', error);
    }
  },
}));

async function persistState(state: UserState) {
  try {
    const toStore = {
      hasCompletedOnboarding: state.hasCompletedOnboarding,
      isSubscribed: state.isSubscribed,
      isTrialActive: state.isTrialActive,
      trialEndsAt: state.trialEndsAt,
      settings: state.settings,
    };
    await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(toStore));
  } catch (error) {
    console.error('Failed to persist user store:', error);
  }
}
