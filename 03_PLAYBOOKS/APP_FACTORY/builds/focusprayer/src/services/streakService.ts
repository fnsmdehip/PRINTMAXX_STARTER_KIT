/**
 * Streak Service
 * Handles streak calculations and notifications
 */

import { StreakData } from '../types';
import { getTodayString, areConsecutiveDays, daysBetween } from '../utils/dateUtils';

// Calculate streak status message
export function getStreakMessage(streak: StreakData): string {
  const { currentStreak, longestStreak, lastCompletedDate } = streak;

  if (currentStreak === 0 && longestStreak === 0) {
    return 'Start your prayer journey today';
  }

  if (currentStreak === 0 && longestStreak > 0) {
    return `Your best streak was ${longestStreak} day${longestStreak !== 1 ? 's' : ''}. Time to start fresh.`;
  }

  if (currentStreak === longestStreak && currentStreak > 7) {
    return `Personal best: ${currentStreak} days. Keep going.`;
  }

  if (currentStreak >= 30) {
    return `${currentStreak} days of consistent prayer. You built a habit.`;
  }

  if (currentStreak >= 7) {
    return `${currentStreak} day streak. One week down.`;
  }

  return `${currentStreak} day${currentStreak !== 1 ? 's' : ''} and counting`;
}

// Get encouragement based on streak length
export function getEncouragement(currentStreak: number): string {
  if (currentStreak === 0) {
    return 'Today is the perfect day to begin.';
  }

  if (currentStreak === 1) {
    return 'Day 1 complete. Tomorrow makes it a habit.';
  }

  if (currentStreak === 2) {
    return 'Two days in a row. Momentum is building.';
  }

  if (currentStreak === 3) {
    return 'Three days. You made it through the hardest part.';
  }

  if (currentStreak <= 7) {
    return `${currentStreak} days. Almost a full week.`;
  }

  if (currentStreak === 7) {
    return 'One full week of prayer. Well done.';
  }

  if (currentStreak <= 14) {
    return `${currentStreak} days. Two weeks is within reach.`;
  }

  if (currentStreak === 14) {
    return 'Two weeks. This is becoming routine.';
  }

  if (currentStreak <= 21) {
    return 'They say 21 days builds a habit. Keep pushing.';
  }

  if (currentStreak === 21) {
    return 'Three weeks. The habit is formed.';
  }

  if (currentStreak <= 30) {
    return 'Almost a full month of daily prayer.';
  }

  if (currentStreak === 30) {
    return 'One month. Your discipline is paying off.';
  }

  if (currentStreak <= 60) {
    return `${currentStreak} days. You are transformed by renewal.`;
  }

  if (currentStreak <= 90) {
    return `${currentStreak} days. Prayer is now part of who you are.`;
  }

  if (currentStreak === 100) {
    return '100 days. A remarkable commitment.';
  }

  if (currentStreak === 365) {
    return 'One full year of daily prayer. Extraordinary.';
  }

  return `${currentStreak} day streak. Faithful and consistent.`;
}

// Check if streak is at risk (completed yesterday but not today)
export function isStreakAtRisk(streak: StreakData): boolean {
  const today = getTodayString();
  const { lastCompletedDate, currentStreak } = streak;

  // No streak to protect
  if (currentStreak === 0) {
    return false;
  }

  // Already completed today
  if (lastCompletedDate === today) {
    return false;
  }

  // Check if yesterday was completed
  if (lastCompletedDate && areConsecutiveDays(lastCompletedDate, today)) {
    return true;
  }

  return false;
}

// Get days since last completion
export function getDaysSinceLastPrayer(lastCompletedDate: string | null): number {
  if (!lastCompletedDate) {
    return -1; // Never prayed
  }

  const today = getTodayString();
  return daysBetween(lastCompletedDate, today);
}

// Generate calendar data for stats view
export interface CalendarDay {
  date: string;
  completed: boolean;
  isToday: boolean;
  isPast: boolean;
}

export function generateCalendarMonth(
  year: number,
  month: number, // 0-indexed
  completedDates: string[]
): CalendarDay[] {
  const today = getTodayString();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const calendar: CalendarDay[] = [];

  for (let day = 1; day <= daysInMonth; day++) {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    const isToday = dateStr === today;
    const isPast = dateStr < today;
    const completed = completedDates.includes(dateStr);

    calendar.push({
      date: dateStr,
      completed,
      isToday,
      isPast,
    });
  }

  return calendar;
}

// Calculate streak milestone
export function getNextMilestone(currentStreak: number): number {
  const milestones = [3, 7, 14, 21, 30, 60, 90, 100, 180, 365];

  for (const milestone of milestones) {
    if (currentStreak < milestone) {
      return milestone;
    }
  }

  // Beyond 365, milestones are yearly
  return Math.ceil(currentStreak / 365) * 365 + 365;
}

export function getDaysToMilestone(currentStreak: number): number {
  return getNextMilestone(currentStreak) - currentStreak;
}
