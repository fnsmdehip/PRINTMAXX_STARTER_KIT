import AsyncStorage from '@react-native-async-storage/async-storage';
import { UserStats, Settings, DailySteps, LockState } from '../constants/types';
import { DEFAULT_SETTINGS } from '../constants/theme';

const STORAGE_KEYS = {
  USER_STATS: '@walktounlock_user_stats',
  SETTINGS: '@walktounlock_settings',
  LOCK_STATE: '@walktounlock_lock_state',
  DAILY_STEPS: '@walktounlock_daily_steps',
  LAST_RESET_DATE: '@walktounlock_last_reset',
};

const getDefaultStats = (): UserStats => ({
  totalSteps: 0,
  currentStreak: 0,
  longestStreak: 0,
  totalDaysActive: 0,
  lastActiveDate: '',
  achievements: [],
  weeklySteps: [],
  monthlySteps: [],
  personalRecords: {
    mostStepsInDay: 0,
    mostStepsInWeek: 0,
    longestStreak: 0,
    fastestUnlock: 0,
  },
});

const getDefaultSettings = (): Settings => ({
  ...DEFAULT_SETTINGS,
  isPremium: false,
  whitelistedApps: [],
});

export const getUserStats = async (): Promise<UserStats> => {
  try {
    const data = await AsyncStorage.getItem(STORAGE_KEYS.USER_STATS);
    if (data) {
      return JSON.parse(data);
    }
    return getDefaultStats();
  } catch (error) {
    console.error('Error loading user stats:', error);
    return getDefaultStats();
  }
};

export const saveUserStats = async (stats: UserStats): Promise<void> => {
  try {
    await AsyncStorage.setItem(STORAGE_KEYS.USER_STATS, JSON.stringify(stats));
  } catch (error) {
    console.error('Error saving user stats:', error);
  }
};

export const getSettings = async (): Promise<Settings> => {
  try {
    const data = await AsyncStorage.getItem(STORAGE_KEYS.SETTINGS);
    if (data) {
      return { ...getDefaultSettings(), ...JSON.parse(data) };
    }
    return getDefaultSettings();
  } catch (error) {
    console.error('Error loading settings:', error);
    return getDefaultSettings();
  }
};

export const saveSettings = async (settings: Settings): Promise<void> => {
  try {
    await AsyncStorage.setItem(STORAGE_KEYS.SETTINGS, JSON.stringify(settings));
  } catch (error) {
    console.error('Error saving settings:', error);
  }
};

export const getLockState = async (): Promise<LockState> => {
  try {
    const data = await AsyncStorage.getItem(STORAGE_KEYS.LOCK_STATE);
    if (data) {
      return JSON.parse(data);
    }
    return {
      isLocked: false,
      currentSteps: 0,
      requiredSteps: 500,
    };
  } catch (error) {
    console.error('Error loading lock state:', error);
    return {
      isLocked: false,
      currentSteps: 0,
      requiredSteps: 500,
    };
  }
};

export const saveLockState = async (state: LockState): Promise<void> => {
  try {
    await AsyncStorage.setItem(STORAGE_KEYS.LOCK_STATE, JSON.stringify(state));
  } catch (error) {
    console.error('Error saving lock state:', error);
  }
};

export const getTodaySteps = async (): Promise<number> => {
  try {
    const today = new Date().toISOString().split('T')[0];
    const data = await AsyncStorage.getItem(`${STORAGE_KEYS.DAILY_STEPS}_${today}`);
    return data ? parseInt(data, 10) : 0;
  } catch (error) {
    console.error('Error loading today steps:', error);
    return 0;
  }
};

export const saveTodaySteps = async (steps: number): Promise<void> => {
  try {
    const today = new Date().toISOString().split('T')[0];
    await AsyncStorage.setItem(`${STORAGE_KEYS.DAILY_STEPS}_${today}`, steps.toString());
  } catch (error) {
    console.error('Error saving today steps:', error);
  }
};

export const updateStreak = async (): Promise<number> => {
  try {
    const stats = await getUserStats();
    const today = new Date().toISOString().split('T')[0];
    const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];

    if (stats.lastActiveDate === today) {
      return stats.currentStreak;
    }

    let newStreak = 1;
    if (stats.lastActiveDate === yesterday) {
      newStreak = stats.currentStreak + 1;
    }

    const updatedStats: UserStats = {
      ...stats,
      currentStreak: newStreak,
      longestStreak: Math.max(stats.longestStreak, newStreak),
      lastActiveDate: today,
      totalDaysActive: stats.totalDaysActive + 1,
      personalRecords: {
        ...stats.personalRecords,
        longestStreak: Math.max(stats.personalRecords.longestStreak, newStreak),
      },
    };

    await saveUserStats(updatedStats);
    return newStreak;
  } catch (error) {
    console.error('Error updating streak:', error);
    return 0;
  }
};

export const addDailyStepsToHistory = async (steps: number, goal: number): Promise<void> => {
  try {
    const stats = await getUserStats();
    const today = new Date().toISOString().split('T')[0];

    const dailyEntry: DailySteps = {
      date: today,
      steps,
      goalMet: steps >= goal,
      goal,
    };

    const existingIndex = stats.weeklySteps.findIndex(d => d.date === today);
    if (existingIndex >= 0) {
      stats.weeklySteps[existingIndex] = dailyEntry;
    } else {
      stats.weeklySteps.unshift(dailyEntry);
    }

    stats.weeklySteps = stats.weeklySteps.slice(0, 7);

    const monthlyIndex = stats.monthlySteps.findIndex(d => d.date === today);
    if (monthlyIndex >= 0) {
      stats.monthlySteps[monthlyIndex] = dailyEntry;
    } else {
      stats.monthlySteps.unshift(dailyEntry);
    }

    stats.monthlySteps = stats.monthlySteps.slice(0, 30);

    stats.totalSteps += steps;

    if (steps > stats.personalRecords.mostStepsInDay) {
      stats.personalRecords.mostStepsInDay = steps;
    }

    const weeklyTotal = stats.weeklySteps.reduce((sum, d) => sum + d.steps, 0);
    if (weeklyTotal > stats.personalRecords.mostStepsInWeek) {
      stats.personalRecords.mostStepsInWeek = weeklyTotal;
    }

    await saveUserStats(stats);
  } catch (error) {
    console.error('Error adding daily steps to history:', error);
  }
};

export const unlockAchievement = async (achievementId: string): Promise<boolean> => {
  try {
    const stats = await getUserStats();

    if (stats.achievements.includes(achievementId)) {
      return false;
    }

    stats.achievements.push(achievementId);
    await saveUserStats(stats);
    return true;
  } catch (error) {
    console.error('Error unlocking achievement:', error);
    return false;
  }
};

export const clearAllData = async (): Promise<void> => {
  try {
    const keys = await AsyncStorage.getAllKeys();
    const walktounlockKeys = keys.filter(key => key.startsWith('@walktounlock'));
    await AsyncStorage.multiRemove(walktounlockKeys);
  } catch (error) {
    console.error('Error clearing data:', error);
  }
};
