import {
  calculateStreakAfterCompletion,
  shouldResetStreak,
  getStreakMessage,
  isCloseToRecord,
  daysUntilRecord,
  getWeeklyCompletionRate,
  getCalendarDates,
} from '../src/services/streakService';
import { StreakData } from '../src/types';
import { getTodayDateString, formatDateString } from '../src/utils/dateUtils';

describe('streakService', () => {
  const emptyStreak: StreakData = {
    currentStreak: 0,
    longestStreak: 0,
    totalDaysCompleted: 0,
    completedDates: [],
    lastCompletedDate: null,
  };

  const getYesterdayString = () => {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    return formatDateString(yesterday);
  };

  describe('calculateStreakAfterCompletion', () => {
    it('starts new streak at 1 for first completion', () => {
      const result = calculateStreakAfterCompletion(emptyStreak);
      expect(result.currentStreak).toBe(1);
      expect(result.longestStreak).toBe(1);
      expect(result.totalDaysCompleted).toBe(1);
    });

    it('continues streak when yesterday was completed', () => {
      const yesterday = getYesterdayString();
      const streakWithYesterday: StreakData = {
        currentStreak: 5,
        longestStreak: 10,
        totalDaysCompleted: 15,
        completedDates: [yesterday],
        lastCompletedDate: yesterday,
      };

      const result = calculateStreakAfterCompletion(streakWithYesterday);
      expect(result.currentStreak).toBe(6);
      expect(result.totalDaysCompleted).toBe(16);
    });

    it('resets streak when yesterday was not completed', () => {
      const twoDaysAgo = new Date();
      twoDaysAgo.setDate(twoDaysAgo.getDate() - 2);
      const twoDaysAgoStr = formatDateString(twoDaysAgo);

      const brokenStreak: StreakData = {
        currentStreak: 5,
        longestStreak: 10,
        totalDaysCompleted: 15,
        completedDates: [twoDaysAgoStr],
        lastCompletedDate: twoDaysAgoStr,
      };

      const result = calculateStreakAfterCompletion(brokenStreak);
      expect(result.currentStreak).toBe(1);
    });

    it('does not double-count same day completion', () => {
      const today = getTodayDateString();
      const alreadyCompletedToday: StreakData = {
        currentStreak: 5,
        longestStreak: 10,
        totalDaysCompleted: 15,
        completedDates: [today],
        lastCompletedDate: today,
      };

      const result = calculateStreakAfterCompletion(alreadyCompletedToday);
      expect(result.currentStreak).toBe(5);
      expect(result.totalDaysCompleted).toBe(15);
    });

    it('updates longest streak when current exceeds it', () => {
      const yesterday = getYesterdayString();
      const streakAboutToBreakRecord: StreakData = {
        currentStreak: 10,
        longestStreak: 10,
        totalDaysCompleted: 50,
        completedDates: [yesterday],
        lastCompletedDate: yesterday,
      };

      const result = calculateStreakAfterCompletion(streakAboutToBreakRecord);
      expect(result.currentStreak).toBe(11);
      expect(result.longestStreak).toBe(11);
    });
  });

  describe('shouldResetStreak', () => {
    it('returns false for empty streak', () => {
      expect(shouldResetStreak(emptyStreak)).toBe(false);
    });

    it('returns false when completed today', () => {
      const today = getTodayDateString();
      const streak: StreakData = {
        ...emptyStreak,
        currentStreak: 5,
        completedDates: [today],
        lastCompletedDate: today,
      };
      expect(shouldResetStreak(streak)).toBe(false);
    });

    it('returns false when yesterday was completed', () => {
      const yesterday = getYesterdayString();
      const streak: StreakData = {
        ...emptyStreak,
        currentStreak: 5,
        completedDates: [yesterday],
        lastCompletedDate: yesterday,
      };
      expect(shouldResetStreak(streak)).toBe(false);
    });

    it('returns true when more than one day gap', () => {
      const twoDaysAgo = new Date();
      twoDaysAgo.setDate(twoDaysAgo.getDate() - 2);
      const twoDaysAgoStr = formatDateString(twoDaysAgo);

      const streak: StreakData = {
        ...emptyStreak,
        currentStreak: 5,
        completedDates: [twoDaysAgoStr],
        lastCompletedDate: twoDaysAgoStr,
      };
      expect(shouldResetStreak(streak)).toBe(true);
    });
  });

  describe('getStreakMessage', () => {
    it('returns starting message for zero streak', () => {
      expect(getStreakMessage(emptyStreak)).toBe('Start your streak today!');
    });

    it('returns appropriate message for 1 day', () => {
      const streak = { ...emptyStreak, currentStreak: 1 };
      expect(getStreakMessage(streak)).toBe('1 day streak. Keep it going!');
    });

    it('returns building momentum for short streaks', () => {
      const streak = { ...emptyStreak, currentStreak: 5 };
      expect(getStreakMessage(streak)).toContain('Building momentum');
    });

    it('returns on fire for week-long streaks', () => {
      const streak = { ...emptyStreak, currentStreak: 15 };
      expect(getStreakMessage(streak)).toContain('on fire');
    });

    it('returns incredible commitment for month-long streaks', () => {
      const streak = { ...emptyStreak, currentStreak: 45 };
      expect(getStreakMessage(streak)).toContain('Incredible commitment');
    });
  });

  describe('isCloseToRecord', () => {
    it('returns false when no record exists', () => {
      expect(isCloseToRecord(emptyStreak)).toBe(false);
    });

    it('returns false when far from record', () => {
      const streak: StreakData = {
        ...emptyStreak,
        currentStreak: 5,
        longestStreak: 20,
      };
      expect(isCloseToRecord(streak)).toBe(false);
    });

    it('returns true when within 3 days of record', () => {
      const streak: StreakData = {
        ...emptyStreak,
        currentStreak: 8,
        longestStreak: 10,
      };
      expect(isCloseToRecord(streak)).toBe(true);
    });

    it('returns false when already at record', () => {
      const streak: StreakData = {
        ...emptyStreak,
        currentStreak: 10,
        longestStreak: 10,
      };
      expect(isCloseToRecord(streak)).toBe(false);
    });
  });

  describe('daysUntilRecord', () => {
    it('returns correct days to beat record', () => {
      const streak: StreakData = {
        ...emptyStreak,
        currentStreak: 7,
        longestStreak: 10,
      };
      expect(daysUntilRecord(streak)).toBe(4);
    });

    it('returns 0 when already past record', () => {
      const streak: StreakData = {
        ...emptyStreak,
        currentStreak: 12,
        longestStreak: 10,
      };
      expect(daysUntilRecord(streak)).toBe(0);
    });
  });

  describe('getCalendarDates', () => {
    it('returns 30 days of calendar data', () => {
      const result = getCalendarDates(emptyStreak);
      expect(result).toHaveLength(30);
    });

    it('marks completed dates correctly', () => {
      const today = getTodayDateString();
      const streak: StreakData = {
        ...emptyStreak,
        completedDates: [today],
      };

      const result = getCalendarDates(streak);
      const todayEntry = result.find((d) => d.date === today);
      expect(todayEntry?.completed).toBe(true);
    });

    it('marks uncompleted dates correctly', () => {
      const result = getCalendarDates(emptyStreak);
      expect(result.every((d) => d.completed === false)).toBe(true);
    });
  });
});
