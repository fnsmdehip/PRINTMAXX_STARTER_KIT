import {
  format,
  parseISO,
  isToday,
  isYesterday,
  differenceInDays,
  startOfDay,
  addDays,
  subDays,
  isSameDay,
} from 'date-fns';

export function formatDate(date: Date | string): string {
  const d = typeof date === 'string' ? parseISO(date) : date;
  return format(d, 'yyyy-MM-dd');
}

export function formatDisplayDate(date: Date | string): string {
  const d = typeof date === 'string' ? parseISO(date) : date;

  if (isToday(d)) {
    return 'Today';
  }
  if (isYesterday(d)) {
    return 'Yesterday';
  }
  return format(d, 'MMMM d, yyyy');
}

export function formatShortDate(date: Date | string): string {
  const d = typeof date === 'string' ? parseISO(date) : date;
  return format(d, 'MMM d');
}

export function getToday(): string {
  return formatDate(new Date());
}

export function getYesterday(): string {
  return formatDate(subDays(new Date(), 1));
}

export function getDaysAgo(days: number): string {
  return formatDate(subDays(new Date(), days));
}

export function getDaysFromNow(days: number): string {
  return formatDate(addDays(new Date(), days));
}

export function calculateStreak(completionDates: string[]): {
  currentStreak: number;
  longestStreak: number;
} {
  if (completionDates.length === 0) {
    return { currentStreak: 0, longestStreak: 0 };
  }

  // Sort dates in descending order
  const sortedDates = [...completionDates].sort().reverse();
  const uniqueDates = [...new Set(sortedDates)];

  const today = getToday();
  const yesterday = getYesterday();

  // Check if streak is still active
  const lastDate = uniqueDates[0];
  if (lastDate !== today && lastDate !== yesterday) {
    // Streak is broken
    return {
      currentStreak: 0,
      longestStreak: calculateLongestStreak(uniqueDates),
    };
  }

  // Count current streak
  let currentStreak = 1;
  for (let i = 1; i < uniqueDates.length; i++) {
    const prevDate = parseISO(uniqueDates[i - 1]);
    const currDate = parseISO(uniqueDates[i]);
    const diff = differenceInDays(prevDate, currDate);

    if (diff === 1) {
      currentStreak++;
    } else {
      break;
    }
  }

  return {
    currentStreak,
    longestStreak: calculateLongestStreak(uniqueDates),
  };
}

function calculateLongestStreak(sortedDates: string[]): number {
  if (sortedDates.length === 0) return 0;

  let longest = 1;
  let current = 1;

  // Dates are in descending order, we need to process them
  const dates = [...sortedDates].sort(); // ascending

  for (let i = 1; i < dates.length; i++) {
    const prevDate = parseISO(dates[i - 1]);
    const currDate = parseISO(dates[i]);
    const diff = differenceInDays(currDate, prevDate);

    if (diff === 1) {
      current++;
      longest = Math.max(longest, current);
    } else if (diff > 1) {
      current = 1;
    }
    // diff === 0 means same day, skip
  }

  return longest;
}

export function getWeekDates(centerDate: Date = new Date()): Date[] {
  const dates: Date[] = [];
  const start = startOfDay(centerDate);

  // Get 3 days before and 3 days after
  for (let i = -3; i <= 3; i++) {
    dates.push(addDays(start, i));
  }

  return dates;
}

export function getMonthDates(year: number, month: number): Date[] {
  const dates: Date[] = [];
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);

  for (let d = new Date(firstDay); d <= lastDay; d.setDate(d.getDate() + 1)) {
    dates.push(new Date(d));
  }

  return dates;
}

export function isSameDateString(date1: string, date2: string): boolean {
  return date1 === date2;
}

export function isDateInRange(
  date: string,
  startDate: string,
  endDate: string
): boolean {
  return date >= startDate && date <= endDate;
}
