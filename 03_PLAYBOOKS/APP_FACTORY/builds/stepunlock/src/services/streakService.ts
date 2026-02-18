import { StreakData } from '../types';
import { getTodayDateString, isYesterday, parseDateString } from '../utils/dateUtils';

/**
 * Calculate updated streak data after completing today's goal
 */
export function calculateStreakAfterCompletion(
  currentStreak: StreakData
): StreakData {
  const today = getTodayDateString();

  // Already completed today
  if (currentStreak.completedDates.includes(today)) {
    return currentStreak;
  }

  // Check if streak continues from yesterday
  const streakContinues =
    currentStreak.lastCompletedDate &&
    isYesterday(currentStreak.lastCompletedDate);

  const newCurrentStreak = streakContinues
    ? currentStreak.currentStreak + 1
    : 1;

  return {
    currentStreak: newCurrentStreak,
    longestStreak: Math.max(currentStreak.longestStreak, newCurrentStreak),
    totalDaysCompleted: currentStreak.totalDaysCompleted + 1,
    completedDates: [...currentStreak.completedDates, today],
    lastCompletedDate: today,
  };
}

/**
 * Check if streak should be reset (missed a day)
 */
export function shouldResetStreak(currentStreak: StreakData): boolean {
  if (!currentStreak.lastCompletedDate) {
    return false;
  }

  const today = getTodayDateString();

  // Already completed today, no reset needed
  if (currentStreak.completedDates.includes(today)) {
    return false;
  }

  // Check if yesterday was completed
  if (isYesterday(currentStreak.lastCompletedDate)) {
    return false;
  }

  // More than one day gap, streak should reset
  return true;
}

/**
 * Get streak status message
 */
export function getStreakMessage(streak: StreakData): string {
  if (streak.currentStreak === 0) {
    return 'Start your streak today!';
  }

  if (streak.currentStreak === 1) {
    return '1 day streak. Keep it going!';
  }

  if (streak.currentStreak < 7) {
    return `${streak.currentStreak} day streak. Building momentum!`;
  }

  if (streak.currentStreak < 30) {
    return `${streak.currentStreak} day streak. You're on fire!`;
  }

  return `${streak.currentStreak} day streak. Incredible commitment!`;
}

/**
 * Check if user is close to breaking their record
 */
export function isCloseToRecord(streak: StreakData): boolean {
  if (streak.longestStreak === 0) return false;

  const daysToRecord = streak.longestStreak - streak.currentStreak;
  return daysToRecord > 0 && daysToRecord <= 3;
}

/**
 * Get days until record is broken
 */
export function daysUntilRecord(streak: StreakData): number {
  return Math.max(0, streak.longestStreak - streak.currentStreak + 1);
}

/**
 * Calculate completion percentage for current week
 */
export function getWeeklyCompletionRate(streak: StreakData): number {
  const today = new Date();
  const weekStart = new Date(today);
  weekStart.setDate(today.getDate() - today.getDay()); // Start of week (Sunday)

  let completedDays = 0;
  let totalDays = today.getDay() + 1; // Days so far this week (including today)

  for (const dateStr of streak.completedDates) {
    const date = parseDateString(dateStr);
    if (date >= weekStart && date <= today) {
      completedDays++;
    }
  }

  return totalDays > 0 ? Math.round((completedDays / totalDays) * 100) : 0;
}

/**
 * Get array of dates for calendar display (last 30 days)
 */
export function getCalendarDates(streak: StreakData): {
  date: string;
  completed: boolean;
}[] {
  const dates: { date: string; completed: boolean }[] = [];
  const today = new Date();

  for (let i = 29; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    const dateStr =
      date.getFullYear() +
      '-' +
      String(date.getMonth() + 1).padStart(2, '0') +
      '-' +
      String(date.getDate()).padStart(2, '0');

    dates.push({
      date: dateStr,
      completed: streak.completedDates.includes(dateStr),
    });
  }

  return dates;
}
