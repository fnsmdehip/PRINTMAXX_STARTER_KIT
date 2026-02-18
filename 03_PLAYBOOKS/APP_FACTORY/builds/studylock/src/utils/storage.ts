import AsyncStorage from '@react-native-async-storage/async-storage';
import { StudySession, DailyStats, UserSettings, UserProgress } from '../types';
import { STORAGE_KEYS, DEFAULT_SETTINGS } from './constants';

// Generic storage helpers
export const storage = {
  async get<T>(key: string): Promise<T | null> {
    try {
      const value = await AsyncStorage.getItem(key);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.error(`Failed to get ${key}:`, error);
      return null;
    }
  },

  async set<T>(key: string, value: T): Promise<boolean> {
    try {
      await AsyncStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (error) {
      console.error(`Failed to set ${key}:`, error);
      return false;
    }
  },

  async remove(key: string): Promise<boolean> {
    try {
      await AsyncStorage.removeItem(key);
      return true;
    } catch (error) {
      console.error(`Failed to remove ${key}:`, error);
      return false;
    }
  },

  async clear(): Promise<boolean> {
    try {
      await AsyncStorage.clear();
      return true;
    } catch (error) {
      console.error('Failed to clear storage:', error);
      return false;
    }
  },
};

// Session-specific storage
export const sessionStorage = {
  async saveSessions(sessions: StudySession[]): Promise<boolean> {
    return storage.set(STORAGE_KEYS.studySessions, sessions);
  },

  async getSessions(): Promise<StudySession[]> {
    const sessions = await storage.get<StudySession[]>(STORAGE_KEYS.studySessions);
    return sessions || [];
  },

  async addSession(session: StudySession): Promise<boolean> {
    const sessions = await this.getSessions();
    sessions.unshift(session);
    // Keep only last 100 sessions
    const trimmed = sessions.slice(0, 100);
    return this.saveSessions(trimmed);
  },

  async getSessionsByDate(date: string): Promise<StudySession[]> {
    const sessions = await this.getSessions();
    return sessions.filter((s) => {
      const sessionDate = new Date(s.startTime).toISOString().split('T')[0];
      return sessionDate === date;
    });
  },

  async getTodaySessions(): Promise<StudySession[]> {
    const today = new Date().toISOString().split('T')[0];
    return this.getSessionsByDate(today);
  },

  async getWeekSessions(): Promise<StudySession[]> {
    const sessions = await this.getSessions();
    const weekAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
    return sessions.filter((s) => s.startTime >= weekAgo);
  },
};

// Stats storage helpers
export const statsStorage = {
  async getDailyStats(): Promise<DailyStats[]> {
    const stats = await storage.get<DailyStats[]>(STORAGE_KEYS.dailyStats);
    return stats || [];
  },

  async getStatsForDate(date: string): Promise<DailyStats | null> {
    const stats = await this.getDailyStats();
    return stats.find((s) => s.date === date) || null;
  },

  async getWeeklyStats(): Promise<DailyStats[]> {
    const stats = await this.getDailyStats();
    const today = new Date();
    const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);

    return stats
      .filter((s) => new Date(s.date) >= weekAgo)
      .sort((a, b) => a.date.localeCompare(b.date));
  },

  async getMonthlyStats(): Promise<DailyStats[]> {
    const stats = await this.getDailyStats();
    const today = new Date();
    const monthAgo = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());

    return stats
      .filter((s) => new Date(s.date) >= monthAgo)
      .sort((a, b) => a.date.localeCompare(b.date));
  },
};

// Settings storage helpers
export const settingsStorage = {
  async getSettings(): Promise<UserSettings> {
    const settings = await storage.get<UserSettings>(STORAGE_KEYS.userSettings);
    return settings || DEFAULT_SETTINGS;
  },

  async saveSettings(settings: UserSettings): Promise<boolean> {
    return storage.set(STORAGE_KEYS.userSettings, settings);
  },
};

// Progress storage helpers
export const progressStorage = {
  async getProgress(): Promise<UserProgress | null> {
    return storage.get<UserProgress>(STORAGE_KEYS.userProgress);
  },

  async saveProgress(progress: UserProgress): Promise<boolean> {
    return storage.set(STORAGE_KEYS.userProgress, progress);
  },
};

// Onboarding storage
export const onboardingStorage = {
  async isComplete(): Promise<boolean> {
    const value = await AsyncStorage.getItem(STORAGE_KEYS.onboardingComplete);
    return value === 'true';
  },

  async setComplete(): Promise<boolean> {
    try {
      await AsyncStorage.setItem(STORAGE_KEYS.onboardingComplete, 'true');
      return true;
    } catch {
      return false;
    }
  },
};
