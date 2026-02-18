import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { UserProgress, UserSettings, DailyStats, Subject } from '../types';
import { DEFAULT_SETTINGS, STORAGE_KEYS } from '../utils/constants';

interface UserStore {
  settings: UserSettings;
  progress: UserProgress;
  dailyStats: DailyStats[];
  isLoading: boolean;
  isOnboardingComplete: boolean;

  // Actions
  loadUserData: () => Promise<void>;
  updateSettings: (settings: Partial<UserSettings>) => Promise<void>;
  updateProgress: (progress: Partial<UserProgress>) => Promise<void>;
  addStudyTime: (minutes: number, subject: Subject) => Promise<void>;
  updateStreak: () => Promise<void>;
  recordQuizResult: (correct: boolean) => Promise<void>;
  setOnboardingComplete: () => Promise<void>;
  setPremiumStatus: (isPremium: boolean, expiresAt?: string) => Promise<void>;
  resetProgress: () => Promise<void>;
}

const initialProgress: UserProgress = {
  totalStudyMinutes: 0,
  totalSessions: 0,
  currentStreak: 0,
  longestStreak: 0,
  lastStudyDate: null,
  questionsAnswered: 0,
  correctAnswers: 0,
  isPremium: false,
  premiumExpiresAt: null,
};

const getEmptyDailyStats = (date: string): DailyStats => ({
  date,
  totalMinutes: 0,
  sessions: 0,
  questionsAnswered: 0,
  correctAnswers: 0,
  subjectBreakdown: {
    general: 0,
    math: 0,
    science: 0,
    history: 0,
    geography: 0,
    literature: 0,
    vocabulary: 0,
    logic: 0,
  },
});

const getTodayDateString = () => new Date().toISOString().split('T')[0];

export const useUserStore = create<UserStore>((set, get) => ({
  settings: DEFAULT_SETTINGS,
  progress: initialProgress,
  dailyStats: [],
  isLoading: true,
  isOnboardingComplete: false,

  loadUserData: async () => {
    try {
      const [settingsJson, progressJson, statsJson, onboardingJson] = await Promise.all([
        AsyncStorage.getItem(STORAGE_KEYS.userSettings),
        AsyncStorage.getItem(STORAGE_KEYS.userProgress),
        AsyncStorage.getItem(STORAGE_KEYS.dailyStats),
        AsyncStorage.getItem(STORAGE_KEYS.onboardingComplete),
      ]);

      const settings = settingsJson ? JSON.parse(settingsJson) : DEFAULT_SETTINGS;
      const progress = progressJson ? JSON.parse(progressJson) : initialProgress;
      const dailyStats = statsJson ? JSON.parse(statsJson) : [];
      const isOnboardingComplete = onboardingJson === 'true';

      set({
        settings,
        progress,
        dailyStats,
        isOnboardingComplete,
        isLoading: false,
      });
    } catch (error) {
      console.error('Failed to load user data:', error);
      set({ isLoading: false });
    }
  },

  updateSettings: async (newSettings) => {
    const { settings } = get();
    const updatedSettings = { ...settings, ...newSettings };

    set({ settings: updatedSettings });
    await AsyncStorage.setItem(STORAGE_KEYS.userSettings, JSON.stringify(updatedSettings));
  },

  updateProgress: async (newProgress) => {
    const { progress } = get();
    const updatedProgress = { ...progress, ...newProgress };

    set({ progress: updatedProgress });
    await AsyncStorage.setItem(STORAGE_KEYS.userProgress, JSON.stringify(updatedProgress));
  },

  addStudyTime: async (minutes, subject) => {
    const { progress, dailyStats } = get();
    const today = getTodayDateString();

    // Update overall progress
    const updatedProgress = {
      ...progress,
      totalStudyMinutes: progress.totalStudyMinutes + minutes,
      totalSessions: progress.totalSessions + 1,
      lastStudyDate: today,
    };

    // Update daily stats
    let todayStats = dailyStats.find((s) => s.date === today);
    if (!todayStats) {
      todayStats = getEmptyDailyStats(today);
    }

    const updatedTodayStats: DailyStats = {
      ...todayStats,
      totalMinutes: todayStats.totalMinutes + minutes,
      sessions: todayStats.sessions + 1,
      subjectBreakdown: {
        ...todayStats.subjectBreakdown,
        [subject]: todayStats.subjectBreakdown[subject] + minutes,
      },
    };

    const updatedDailyStats = [
      ...dailyStats.filter((s) => s.date !== today),
      updatedTodayStats,
    ].sort((a, b) => b.date.localeCompare(a.date));

    set({ progress: updatedProgress, dailyStats: updatedDailyStats });

    await Promise.all([
      AsyncStorage.setItem(STORAGE_KEYS.userProgress, JSON.stringify(updatedProgress)),
      AsyncStorage.setItem(STORAGE_KEYS.dailyStats, JSON.stringify(updatedDailyStats)),
    ]);
  },

  updateStreak: async () => {
    const { progress } = get();
    const today = getTodayDateString();
    const lastDate = progress.lastStudyDate;

    if (!lastDate) {
      // First study session
      const updatedProgress = {
        ...progress,
        currentStreak: 1,
        longestStreak: Math.max(1, progress.longestStreak),
        lastStudyDate: today,
      };
      set({ progress: updatedProgress });
      await AsyncStorage.setItem(STORAGE_KEYS.userProgress, JSON.stringify(updatedProgress));
      return;
    }

    const lastDateObj = new Date(lastDate);
    const todayObj = new Date(today);
    const diffTime = todayObj.getTime() - lastDateObj.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    let newStreak = progress.currentStreak;

    if (diffDays === 0) {
      // Same day, no streak change
      return;
    } else if (diffDays === 1) {
      // Consecutive day
      newStreak = progress.currentStreak + 1;
    } else {
      // Streak broken
      newStreak = 1;
    }

    const updatedProgress = {
      ...progress,
      currentStreak: newStreak,
      longestStreak: Math.max(newStreak, progress.longestStreak),
      lastStudyDate: today,
    };

    set({ progress: updatedProgress });
    await AsyncStorage.setItem(STORAGE_KEYS.userProgress, JSON.stringify(updatedProgress));
  },

  recordQuizResult: async (correct) => {
    const { progress, dailyStats } = get();
    const today = getTodayDateString();

    const updatedProgress = {
      ...progress,
      questionsAnswered: progress.questionsAnswered + 1,
      correctAnswers: progress.correctAnswers + (correct ? 1 : 0),
    };

    let todayStats = dailyStats.find((s) => s.date === today);
    if (todayStats) {
      const updatedTodayStats: DailyStats = {
        ...todayStats,
        questionsAnswered: todayStats.questionsAnswered + 1,
        correctAnswers: todayStats.correctAnswers + (correct ? 1 : 0),
      };

      const updatedDailyStats = [
        ...dailyStats.filter((s) => s.date !== today),
        updatedTodayStats,
      ].sort((a, b) => b.date.localeCompare(a.date));

      set({ progress: updatedProgress, dailyStats: updatedDailyStats });
      await AsyncStorage.setItem(STORAGE_KEYS.dailyStats, JSON.stringify(updatedDailyStats));
    } else {
      set({ progress: updatedProgress });
    }

    await AsyncStorage.setItem(STORAGE_KEYS.userProgress, JSON.stringify(updatedProgress));
  },

  setOnboardingComplete: async () => {
    set({ isOnboardingComplete: true });
    await AsyncStorage.setItem(STORAGE_KEYS.onboardingComplete, 'true');
  },

  setPremiumStatus: async (isPremium, expiresAt) => {
    const { progress } = get();
    const updatedProgress = {
      ...progress,
      isPremium,
      premiumExpiresAt: expiresAt || null,
    };

    set({ progress: updatedProgress });
    await AsyncStorage.setItem(STORAGE_KEYS.userProgress, JSON.stringify(updatedProgress));
  },

  resetProgress: async () => {
    set({
      progress: initialProgress,
      dailyStats: [],
    });

    await Promise.all([
      AsyncStorage.removeItem(STORAGE_KEYS.userProgress),
      AsyncStorage.removeItem(STORAGE_KEYS.dailyStats),
      AsyncStorage.removeItem(STORAGE_KEYS.studySessions),
    ]);
  },
}));
