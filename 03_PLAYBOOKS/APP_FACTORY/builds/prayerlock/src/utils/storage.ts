import AsyncStorage from '@react-native-async-storage/async-storage';
import { STORAGE_KEYS, DEFAULT_SETTINGS, FaithType, SalahSettings } from '../constants';

export interface UserSettings {
  lockTime: string;
  prayerDuration: number;
  notificationsEnabled: boolean;
  hapticEnabled: boolean;
  faith: FaithType;
  salahSettings: SalahSettings;
}

export interface StreakData {
  currentStreak: number;
  longestStreak: number;
  lastPrayerDate: string | null;
  totalPrayerMinutes: number;
  emergencyUnlockCount: number;
}

export interface SalahDailyStatus {
  date: string;
  fajr: boolean;
  dhuhr: boolean;
  asr: boolean;
  maghrib: boolean;
  isha: boolean;
}

// Settings
export async function getSettings(): Promise<UserSettings> {
  try {
    const data = await AsyncStorage.getItem(STORAGE_KEYS.SETTINGS);
    if (data) {
      const parsed = JSON.parse(data);
      return { ...DEFAULT_SETTINGS, ...parsed };
    }
    return DEFAULT_SETTINGS;
  } catch (error) {
    return DEFAULT_SETTINGS;
  }
}

export async function saveSettings(settings: UserSettings): Promise<void> {
  try {
    await AsyncStorage.setItem(STORAGE_KEYS.SETTINGS, JSON.stringify(settings));
  } catch (error) {
    // Settings save failed silently
  }
}

// Streak
export async function getStreakData(): Promise<StreakData> {
  try {
    const [streak, lastDate, totalTime, emergencyCount] = await Promise.all([
      AsyncStorage.getItem(STORAGE_KEYS.STREAK),
      AsyncStorage.getItem(STORAGE_KEYS.LAST_PRAYER_DATE),
      AsyncStorage.getItem(STORAGE_KEYS.TOTAL_PRAYER_TIME),
      AsyncStorage.getItem(STORAGE_KEYS.EMERGENCY_UNLOCK_COUNT),
    ]);

    return {
      currentStreak: streak ? JSON.parse(streak).current : 0,
      longestStreak: streak ? JSON.parse(streak).longest : 0,
      lastPrayerDate: lastDate,
      totalPrayerMinutes: totalTime ? parseInt(totalTime, 10) : 0,
      emergencyUnlockCount: emergencyCount ? parseInt(emergencyCount, 10) : 0,
    };
  } catch (error) {
    return {
      currentStreak: 0,
      longestStreak: 0,
      lastPrayerDate: null,
      totalPrayerMinutes: 0,
      emergencyUnlockCount: 0,
    };
  }
}

export async function updateStreak(prayerMinutes: number): Promise<StreakData> {
  try {
    const today = new Date().toISOString().split('T')[0];
    const data = await getStreakData();

    let newStreak = data.currentStreak;

    if (data.lastPrayerDate !== today) {
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const yesterdayStr = yesterday.toISOString().split('T')[0];

      if (data.lastPrayerDate === yesterdayStr) {
        newStreak = data.currentStreak + 1;
      } else if (!data.lastPrayerDate) {
        newStreak = 1;
      } else {
        newStreak = 1;
      }
    }

    const longestStreak = Math.max(newStreak, data.longestStreak);
    const totalMinutes = data.totalPrayerMinutes + prayerMinutes;

    await Promise.all([
      AsyncStorage.setItem(STORAGE_KEYS.STREAK, JSON.stringify({ current: newStreak, longest: longestStreak })),
      AsyncStorage.setItem(STORAGE_KEYS.LAST_PRAYER_DATE, today),
      AsyncStorage.setItem(STORAGE_KEYS.TOTAL_PRAYER_TIME, totalMinutes.toString()),
    ]);

    return {
      currentStreak: newStreak,
      longestStreak,
      lastPrayerDate: today,
      totalPrayerMinutes: totalMinutes,
      emergencyUnlockCount: data.emergencyUnlockCount,
    };
  } catch (error) {
    throw error;
  }
}

export async function incrementEmergencyUnlock(): Promise<number> {
  try {
    const current = await AsyncStorage.getItem(STORAGE_KEYS.EMERGENCY_UNLOCK_COUNT);
    const newCount = (current ? parseInt(current, 10) : 0) + 1;
    await AsyncStorage.setItem(STORAGE_KEYS.EMERGENCY_UNLOCK_COUNT, newCount.toString());
    return newCount;
  } catch (error) {
    return 0;
  }
}

// Lock State
export async function setLockState(isLocked: boolean): Promise<void> {
  try {
    await AsyncStorage.setItem(STORAGE_KEYS.IS_LOCKED, JSON.stringify(isLocked));
    if (isLocked) {
      await AsyncStorage.setItem(STORAGE_KEYS.LOCK_START_TIME, new Date().toISOString());
    }
  } catch (error) {
    // Lock state save failed silently
  }
}

export async function getLockState(): Promise<boolean> {
  try {
    const data = await AsyncStorage.getItem(STORAGE_KEYS.IS_LOCKED);
    return data ? JSON.parse(data) : false;
  } catch (error) {
    return false;
  }
}

// Premium Status
export async function setPremiumStatus(isPremium: boolean): Promise<void> {
  try {
    await AsyncStorage.setItem(STORAGE_KEYS.IS_PREMIUM, JSON.stringify(isPremium));
  } catch (error) {
    // Premium status save failed silently
  }
}

export async function getPremiumStatus(): Promise<boolean> {
  try {
    const data = await AsyncStorage.getItem(STORAGE_KEYS.IS_PREMIUM);
    return data ? JSON.parse(data) : false;
  } catch (error) {
    return false;
  }
}

// Salah Daily Status
export async function getSalahDailyStatus(): Promise<SalahDailyStatus> {
  try {
    const today = new Date().toISOString().split('T')[0];
    const data = await AsyncStorage.getItem(STORAGE_KEYS.SALAH_DAILY);
    if (data) {
      const parsed = JSON.parse(data);
      if (parsed.date === today) {
        return parsed;
      }
    }
    return {
      date: today,
      fajr: false,
      dhuhr: false,
      asr: false,
      maghrib: false,
      isha: false,
    };
  } catch (error) {
    const today = new Date().toISOString().split('T')[0];
    return {
      date: today,
      fajr: false,
      dhuhr: false,
      asr: false,
      maghrib: false,
      isha: false,
    };
  }
}

export async function markSalahComplete(
  salahName: 'fajr' | 'dhuhr' | 'asr' | 'maghrib' | 'isha'
): Promise<SalahDailyStatus> {
  try {
    const status = await getSalahDailyStatus();
    status[salahName] = true;
    await AsyncStorage.setItem(STORAGE_KEYS.SALAH_DAILY, JSON.stringify(status));

    const totalStr = await AsyncStorage.getItem(STORAGE_KEYS.SALAH_TOTAL_COMPLETED);
    const total = totalStr ? parseInt(totalStr, 10) : 0;
    await AsyncStorage.setItem(STORAGE_KEYS.SALAH_TOTAL_COMPLETED, (total + 1).toString());

    return status;
  } catch (error) {
    return await getSalahDailyStatus();
  }
}

export function getSalahCompletionCount(status: SalahDailyStatus): number {
  let count = 0;
  if (status.fajr) count++;
  if (status.dhuhr) count++;
  if (status.asr) count++;
  if (status.maghrib) count++;
  if (status.isha) count++;
  return count;
}

// Onboarding
export async function getOnboardingComplete(): Promise<boolean> {
  try {
    const data = await AsyncStorage.getItem(STORAGE_KEYS.ONBOARDING_COMPLETE);
    return data ? JSON.parse(data) : false;
  } catch (error) {
    return false;
  }
}

export async function setOnboardingComplete(complete: boolean): Promise<void> {
  try {
    await AsyncStorage.setItem(STORAGE_KEYS.ONBOARDING_COMPLETE, JSON.stringify(complete));
  } catch (error) {
    // Onboarding save failed silently
  }
}

// Helper to get today's verse index
export function getTodayVerseIndex(totalVerses: number): number {
  const today = new Date();
  const startOfYear = new Date(today.getFullYear(), 0, 0);
  const diff = today.getTime() - startOfYear.getTime();
  const dayOfYear = Math.floor(diff / (1000 * 60 * 60 * 24));
  return dayOfYear % totalVerses;
}

// Helper to format time
export function formatTime(minutes: number): string {
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  if (hours > 0) {
    return `${hours}h ${mins}m`;
  }
  return `${mins}m`;
}

// Helper to format timer display
export function formatTimerDisplay(seconds: number): string {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}
