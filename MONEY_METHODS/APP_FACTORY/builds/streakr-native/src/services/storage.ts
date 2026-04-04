import AsyncStorage from '@react-native-async-storage/async-storage';
import { Habit, AppSettings, HabitCategory } from '../types';
import { MILESTONE_DAYS } from '../constants/habits';

const KEYS = {
  HABITS: 'streakr:habits',
  SETTINGS: 'streakr:settings',
};

const DEFAULT_SETTINGS: AppSettings = {
  onboardingComplete: false,
  isPremium: false,
  reminderEnabled: false,
  reminderTime: '08:00',
  mvdMode: false,
  hasReviewedApp: false,
  lastReviewPrompt: null,
};

// ─── Habit CRUD ───────────────────────────────────────────────────────────────

export async function getHabits(): Promise<Habit[]> {
  const raw = await AsyncStorage.getItem(KEYS.HABITS);
  if (!raw) return [];
  return JSON.parse(raw) as Habit[];
}

export async function saveHabits(habits: Habit[]): Promise<void> {
  await AsyncStorage.setItem(KEYS.HABITS, JSON.stringify(habits));
}

export function createHabit(
  name: string,
  emoji: string,
  category: HabitCategory,
  mvdEnabled: boolean,
  mvdLabel: string,
): Habit {
  return {
    id: `habit_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`,
    name,
    emoji,
    category,
    createdAt: new Date().toISOString(),
    currentStreak: 0,
    longestStreak: 0,
    totalCompletions: 0,
    checkIns: [],
    lastCheckIn: null,
    mvdEnabled,
    mvdLabel,
    repairedDays: [],
  };
}

export async function addHabit(habit: Habit): Promise<Habit[]> {
  const habits = await getHabits();
  const updated = [...habits, habit];
  await saveHabits(updated);
  return updated;
}

export async function deleteHabit(id: string): Promise<Habit[]> {
  const habits = await getHabits();
  const updated = habits.filter(h => h.id !== id);
  await saveHabits(updated);
  return updated;
}

// ─── Check-in ─────────────────────────────────────────────────────────────────

export interface CheckInResult {
  habits: Habit[];
  habit: Habit;
  isNewMilestone: boolean;
  milestoneDay: number | null;
  shouldPromptReview: boolean;
}

export async function checkInHabit(habitId: string): Promise<CheckInResult> {
  const habits = await getHabits();
  const idx = habits.findIndex(h => h.id === habitId);
  if (idx === -1) throw new Error(`Habit not found: ${habitId}`);

  const habit = habits[idx];
  const today = new Date().toDateString();
  const alreadyCheckedIn = habit.checkIns.some(c => new Date(c).toDateString() === today);

  if (alreadyCheckedIn) {
    return { habits, habit, isNewMilestone: false, milestoneDay: null, shouldPromptReview: false };
  }

  // Determine if streak continues or restarts
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const checkedYesterday = habit.checkIns.some(
    c => new Date(c).toDateString() === yesterday.toDateString(),
  );

  const newStreak = checkedYesterday || habit.currentStreak === 0
    ? habit.currentStreak + 1
    : 1;

  const now = new Date().toISOString();
  const updated: Habit = {
    ...habit,
    currentStreak: newStreak,
    longestStreak: Math.max(habit.longestStreak, newStreak),
    totalCompletions: habit.totalCompletions + 1,
    checkIns: [...habit.checkIns, now],
    lastCheckIn: now,
  };

  const isNewMilestone = MILESTONE_DAYS.includes(newStreak);
  const milestoneDay = isNewMilestone ? newStreak : null;

  const updatedHabits = [...habits];
  updatedHabits[idx] = updated;
  await saveHabits(updatedHabits);

  // Review prompt eligibility: day 3 or day 7 on any habit, 90-day cooldown
  const settings = await getSettings();
  let shouldPromptReview = false;
  if (!settings.hasReviewedApp && (newStreak === 3 || newStreak === 7)) {
    const lastPrompt = settings.lastReviewPrompt;
    const ninetyDaysAgo = new Date();
    ninetyDaysAgo.setDate(ninetyDaysAgo.getDate() - 90);
    if (!lastPrompt || new Date(lastPrompt) < ninetyDaysAgo) {
      shouldPromptReview = true;
      await saveSettings({ lastReviewPrompt: now });
    }
  }

  return { habits: updatedHabits, habit: updated, isNewMilestone, milestoneDay, shouldPromptReview };
}

// ─── Settings ─────────────────────────────────────────────────────────────────

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
  await AsyncStorage.multiRemove([KEYS.HABITS, KEYS.SETTINGS]);
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

export function isCheckedInToday(habit: Habit): boolean {
  const today = new Date().toDateString();
  return habit.checkIns.some(c => new Date(c).toDateString() === today);
}

export function getCompletionRate(habit: Habit, days = 30): number {
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - days);
  const recent = habit.checkIns.filter(c => new Date(c) >= cutoff);
  return Math.round((recent.length / days) * 100);
}

export function getCalendarData(habit: Habit): Set<string> {
  return new Set(habit.checkIns.map(c => new Date(c).toDateString()));
}
