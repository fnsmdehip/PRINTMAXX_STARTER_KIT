import AsyncStorage from '@react-native-async-storage/async-storage';
import { StreakData, AppSettings, StreakMode } from '../types';

const KEYS = {
  STREAK: 'soberstreak:streak',
  SETTINGS: 'soberstreak:settings',
};

const DEFAULT_SETTINGS: AppSettings = {
  reminderEnabled: false,
  reminderTime: '09:00',
  isPremium: false,
  onboardingComplete: false,
  hasSeenEmergencyPrompt: false,
};

export async function getStreakData(): Promise<StreakData | null> {
  const raw = await AsyncStorage.getItem(KEYS.STREAK);
  if (!raw) return null;
  return JSON.parse(raw) as StreakData;
}

export async function saveStreakData(data: StreakData): Promise<void> {
  await AsyncStorage.setItem(KEYS.STREAK, JSON.stringify(data));
}

export async function initStreak(mode: StreakMode, customLabel?: string): Promise<StreakData> {
  const now = new Date().toISOString();
  const data: StreakData = {
    mode,
    customLabel,
    startDate: now,
    lastCheckIn: null,
    currentStreak: 0,
    longestStreak: 0,
    totalAttempts: 1,
    totalCleanDays: 0,
    checkIns: [],
  };
  await saveStreakData(data);
  return data;
}

export async function performCheckIn(): Promise<{ data: StreakData; isNewMilestone: boolean }> {
  const data = await getStreakData();
  if (!data) throw new Error('No streak data');

  const today = new Date().toDateString();
  const alreadyCheckedIn = data.checkIns.some(c => new Date(c).toDateString() === today);
  if (alreadyCheckedIn) return { data, isNewMilestone: false };

  const now = new Date().toISOString();
  const updated: StreakData = {
    ...data,
    lastCheckIn: now,
    checkIns: [...data.checkIns, now],
    currentStreak: data.currentStreak + 1,
    totalCleanDays: data.totalCleanDays + 1,
    longestStreak: Math.max(data.longestStreak, data.currentStreak + 1),
  };

  const MILESTONE_DAYS = [1, 3, 7, 14, 30, 60, 90, 180, 365];
  const isNewMilestone = MILESTONE_DAYS.includes(updated.currentStreak);

  await saveStreakData(updated);
  return { data: updated, isNewMilestone };
}

export async function recordRelapse(): Promise<StreakData> {
  const data = await getStreakData();
  if (!data) throw new Error('No streak data');

  const now = new Date().toISOString();
  const updated: StreakData = {
    ...data,
    startDate: now,
    lastCheckIn: null,
    currentStreak: 0,
    totalAttempts: data.totalAttempts + 1,
    checkIns: [],
  };
  await saveStreakData(updated);
  return updated;
}

export async function getSettings(): Promise<AppSettings> {
  const raw = await AsyncStorage.getItem(KEYS.SETTINGS);
  if (!raw) return { ...DEFAULT_SETTINGS };
  return { ...DEFAULT_SETTINGS, ...JSON.parse(raw) } as AppSettings;
}

export async function saveSettings(partial: Partial<AppSettings>): Promise<void> {
  const current = await getSettings();
  await AsyncStorage.setItem(KEYS.SETTINGS, JSON.stringify({ ...current, ...partial }));
}

export async function clearAllData(): Promise<void> {
  await AsyncStorage.multiRemove([KEYS.STREAK, KEYS.SETTINGS]);
}
