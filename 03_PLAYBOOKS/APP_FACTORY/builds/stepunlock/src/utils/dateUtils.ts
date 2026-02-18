// Date utility functions

/**
 * Get today's date in YYYY-MM-DD format
 */
export function getTodayDateString(): string {
  return formatDateString(new Date());
}

/**
 * Format a date to YYYY-MM-DD string
 */
export function formatDateString(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * Parse YYYY-MM-DD string to Date
 */
export function parseDateString(dateString: string): Date {
  const [year, month, day] = dateString.split('-').map(Number);
  return new Date(year, month - 1, day);
}

/**
 * Get start of day timestamp
 */
export function getStartOfDay(date: Date = new Date()): Date {
  const result = new Date(date);
  result.setHours(0, 0, 0, 0);
  return result;
}

/**
 * Get end of day timestamp
 */
export function getEndOfDay(date: Date = new Date()): Date {
  const result = new Date(date);
  result.setHours(23, 59, 59, 999);
  return result;
}

/**
 * Check if a date is today
 */
export function isToday(date: Date | string): boolean {
  const dateToCheck = typeof date === 'string' ? parseDateString(date) : date;
  return formatDateString(dateToCheck) === getTodayDateString();
}

/**
 * Check if a date is yesterday
 */
export function isYesterday(date: Date | string): boolean {
  const dateToCheck = typeof date === 'string' ? parseDateString(date) : date;
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  return formatDateString(dateToCheck) === formatDateString(yesterday);
}

/**
 * Get days between two dates
 */
export function getDaysBetween(date1: Date | string, date2: Date | string): number {
  const d1 = typeof date1 === 'string' ? parseDateString(date1) : date1;
  const d2 = typeof date2 === 'string' ? parseDateString(date2) : date2;
  const diffTime = Math.abs(d2.getTime() - d1.getTime());
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}

/**
 * Get an array of date strings for the last N days
 */
export function getLastNDays(n: number): string[] {
  const dates: string[] = [];
  const today = new Date();
  for (let i = 0; i < n; i++) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    dates.push(formatDateString(date));
  }
  return dates;
}

/**
 * Format time remaining (e.g., "2h 30m")
 */
export function formatTimeRemaining(minutes: number): string {
  if (minutes < 60) {
    return `${Math.round(minutes)} min`;
  }
  const hours = Math.floor(minutes / 60);
  const mins = Math.round(minutes % 60);
  if (mins === 0) {
    return `${hours}h`;
  }
  return `${hours}h ${mins}m`;
}

/**
 * Calculate estimated walking time for steps
 * Assumes ~1000 steps per 10 minutes (leisurely pace)
 */
export function estimateWalkingTime(steps: number): number {
  return Math.ceil(steps / 100); // minutes
}

/**
 * Calculate estimated distance for steps
 * Assumes ~2000 steps per mile
 */
export function estimateDistance(steps: number): number {
  return steps / 2000; // miles
}

/**
 * Format distance (e.g., "2.5 mi")
 */
export function formatDistance(miles: number): string {
  return `${miles.toFixed(1)} mi`;
}
