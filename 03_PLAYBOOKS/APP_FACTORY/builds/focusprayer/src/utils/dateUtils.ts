/**
 * Date utility functions for PrayerLock
 */

// Format: YYYY-MM-DD
export function getTodayString(): string {
  const now = new Date();
  return formatDateString(now);
}

export function formatDateString(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

export function parseResetTime(resetTime: string): { hours: number; minutes: number } {
  const [hours, minutes] = resetTime.split(':').map(Number);
  return { hours, minutes };
}

// Check if current time is past the daily reset time
export function isPastResetTime(resetTime: string): boolean {
  const now = new Date();
  const { hours, minutes } = parseResetTime(resetTime);
  const currentMinutes = now.getHours() * 60 + now.getMinutes();
  const resetMinutes = hours * 60 + minutes;
  return currentMinutes >= resetMinutes;
}

// Get the "devotional day" which starts at reset time
// E.g., if reset is 5am, 3am on Jan 2 counts as Jan 1's devotional day
export function getDevotionalDay(resetTime: string): string {
  const now = new Date();

  if (!isPastResetTime(resetTime)) {
    // Before reset time, count as previous day
    const yesterday = new Date(now);
    yesterday.setDate(yesterday.getDate() - 1);
    return formatDateString(yesterday);
  }

  return formatDateString(now);
}

// Calculate days between two date strings
export function daysBetween(dateStr1: string, dateStr2: string): number {
  const date1 = new Date(dateStr1);
  const date2 = new Date(dateStr2);
  const diffTime = Math.abs(date2.getTime() - date1.getTime());
  return Math.floor(diffTime / (1000 * 60 * 60 * 24));
}

// Check if two dates are consecutive
export function areConsecutiveDays(dateStr1: string, dateStr2: string): boolean {
  return daysBetween(dateStr1, dateStr2) === 1;
}

// Generate unique session ID
export function generateSessionId(): string {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

// Format seconds into MM:SS display
export function formatTimerDisplay(totalSeconds: number): string {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

// Format seconds into human readable string
export function formatDuration(totalSeconds: number): string {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;

  if (minutes === 0) {
    return `${seconds} seconds`;
  }
  if (seconds === 0) {
    return `${minutes} minute${minutes !== 1 ? 's' : ''}`;
  }
  return `${minutes}m ${seconds}s`;
}

// Get day of year (1-365/366)
export function getDayOfYear(): number {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 0);
  const diff = now.getTime() - start.getTime();
  const oneDay = 1000 * 60 * 60 * 24;
  return Math.floor(diff / oneDay);
}

// Check if trial has expired
export function isTrialExpired(trialStartTimestamp: number, trialDays: number): boolean {
  const now = Date.now();
  const trialEndTime = trialStartTimestamp + trialDays * 24 * 60 * 60 * 1000;
  return now > trialEndTime;
}

// Get days remaining in trial
export function getTrialDaysRemaining(trialStartTimestamp: number, trialDays: number): number {
  const now = Date.now();
  const trialEndTime = trialStartTimestamp + trialDays * 24 * 60 * 60 * 1000;
  const remaining = trialEndTime - now;
  return Math.max(0, Math.ceil(remaining / (24 * 60 * 60 * 1000)));
}
