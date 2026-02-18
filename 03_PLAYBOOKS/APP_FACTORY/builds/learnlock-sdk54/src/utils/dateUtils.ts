/**
 * Get today's date as YYYY-MM-DD string
 */
export function getTodayDateString(): string {
  return formatDate(new Date());
}

/**
 * Format a Date object to YYYY-MM-DD string
 */
export function formatDate(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * Parse YYYY-MM-DD string to Date object
 */
export function parseDate(dateString: string): Date {
  const [year, month, day] = dateString.split('-').map(Number);
  return new Date(year, month - 1, day);
}

/**
 * Get the start of day timestamp
 */
export function getStartOfDay(date: Date = new Date()): number {
  const start = new Date(date);
  start.setHours(0, 0, 0, 0);
  return start.getTime();
}

/**
 * Get the end of day timestamp
 */
export function getEndOfDay(date: Date = new Date()): number {
  const end = new Date(date);
  end.setHours(23, 59, 59, 999);
  return end.getTime();
}

/**
 * Check if a date string is today
 */
export function isToday(dateString: string): boolean {
  return dateString === getTodayDateString();
}

/**
 * Check if a date string is yesterday
 */
export function isYesterday(dateString: string): boolean {
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  return dateString === formatDate(yesterday);
}

/**
 * Get array of date strings for the last N days
 */
export function getLastNDays(n: number): string[] {
  const dates: string[] = [];
  for (let i = 0; i < n; i++) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    dates.push(formatDate(date));
  }
  return dates;
}

/**
 * Get the start of the current week (Sunday)
 */
export function getStartOfWeek(): string {
  const now = new Date();
  const dayOfWeek = now.getDay();
  const startOfWeek = new Date(now);
  startOfWeek.setDate(now.getDate() - dayOfWeek);
  return formatDate(startOfWeek);
}

/**
 * Get dates for current week
 */
export function getCurrentWeekDates(): string[] {
  const dates: string[] = [];
  const now = new Date();
  const dayOfWeek = now.getDay();

  for (let i = 0; i < 7; i++) {
    const date = new Date(now);
    date.setDate(now.getDate() - dayOfWeek + i);
    dates.push(formatDate(date));
  }

  return dates;
}

/**
 * Format seconds to MM:SS string
 */
export function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

/**
 * Format seconds to human readable duration
 * e.g., "1h 25m" or "45m" or "2h"
 */
export function formatDuration(seconds: number): string {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);

  if (hours === 0) {
    return `${minutes}m`;
  }

  if (minutes === 0) {
    return `${hours}h`;
  }

  return `${hours}h ${minutes}m`;
}

/**
 * Format seconds to short duration (for stats)
 * e.g., "1.5h" or "45m"
 */
export function formatDurationShort(seconds: number): string {
  const hours = seconds / 3600;

  if (hours >= 1) {
    return `${hours.toFixed(1)}h`;
  }

  const minutes = Math.floor(seconds / 60);
  return `${minutes}m`;
}

/**
 * Calculate consecutive days from an array of date strings
 */
export function calculateStreak(dates: string[]): number {
  if (dates.length === 0) return 0;

  // Sort dates in descending order
  const sortedDates = [...dates].sort().reverse();

  // Check if streak is still active (includes today or yesterday)
  const today = getTodayDateString();
  const yesterday = formatDate(new Date(Date.now() - 86400000));

  if (sortedDates[0] !== today && sortedDates[0] !== yesterday) {
    return 0;
  }

  let streak = 1;
  let currentDate = parseDate(sortedDates[0]);

  for (let i = 1; i < sortedDates.length; i++) {
    const prevDate = new Date(currentDate);
    prevDate.setDate(prevDate.getDate() - 1);

    if (formatDate(prevDate) === sortedDates[i]) {
      streak++;
      currentDate = prevDate;
    } else {
      break;
    }
  }

  return streak;
}

/**
 * Get day of week name
 */
export function getDayName(dateString: string): string {
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const date = parseDate(dateString);
  return days[date.getDay()];
}

/**
 * Get relative date description
 */
export function getRelativeDateString(dateString: string): string {
  if (isToday(dateString)) return 'Today';
  if (isYesterday(dateString)) return 'Yesterday';
  return getDayName(dateString);
}

/**
 * Calculate days remaining in trial
 */
export function getTrialDaysRemaining(trialStartDate: string): number {
  const start = parseDate(trialStartDate);
  const now = new Date();
  const diffMs = now.getTime() - start.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  const remaining = 7 - diffDays;
  return Math.max(0, remaining);
}
