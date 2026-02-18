/**
 * Date Utilities Tests
 */

import {
  getTodayString,
  formatDateString,
  parseResetTime,
  isPastResetTime,
  getDevotionalDay,
  daysBetween,
  areConsecutiveDays,
  formatTimerDisplay,
  formatDuration,
  getDayOfYear,
  isTrialExpired,
  getTrialDaysRemaining,
} from '../src/utils/dateUtils';

describe('dateUtils', () => {
  describe('formatDateString', () => {
    it('formats date correctly with padding', () => {
      const date = new Date(2024, 0, 5); // Jan 5, 2024
      expect(formatDateString(date)).toBe('2024-01-05');
    });

    it('formats double-digit months and days', () => {
      const date = new Date(2024, 11, 25); // Dec 25, 2024
      expect(formatDateString(date)).toBe('2024-12-25');
    });
  });

  describe('parseResetTime', () => {
    it('parses time string correctly', () => {
      expect(parseResetTime('05:00')).toEqual({ hours: 5, minutes: 0 });
      expect(parseResetTime('23:45')).toEqual({ hours: 23, minutes: 45 });
    });
  });

  describe('daysBetween', () => {
    it('calculates days between two dates', () => {
      expect(daysBetween('2024-01-01', '2024-01-05')).toBe(4);
      expect(daysBetween('2024-01-05', '2024-01-01')).toBe(4);
    });

    it('returns 0 for same date', () => {
      expect(daysBetween('2024-01-01', '2024-01-01')).toBe(0);
    });
  });

  describe('areConsecutiveDays', () => {
    it('returns true for consecutive days', () => {
      expect(areConsecutiveDays('2024-01-01', '2024-01-02')).toBe(true);
      expect(areConsecutiveDays('2024-01-31', '2024-02-01')).toBe(true);
    });

    it('returns false for non-consecutive days', () => {
      expect(areConsecutiveDays('2024-01-01', '2024-01-03')).toBe(false);
      expect(areConsecutiveDays('2024-01-01', '2024-01-01')).toBe(false);
    });
  });

  describe('formatTimerDisplay', () => {
    it('formats seconds to MM:SS', () => {
      expect(formatTimerDisplay(0)).toBe('00:00');
      expect(formatTimerDisplay(60)).toBe('01:00');
      expect(formatTimerDisplay(90)).toBe('01:30');
      expect(formatTimerDisplay(600)).toBe('10:00');
      expect(formatTimerDisplay(3661)).toBe('61:01');
    });
  });

  describe('formatDuration', () => {
    it('formats duration in human readable form', () => {
      expect(formatDuration(30)).toBe('30 seconds');
      expect(formatDuration(60)).toBe('1 minute');
      expect(formatDuration(120)).toBe('2 minutes');
      expect(formatDuration(90)).toBe('1m 30s');
      expect(formatDuration(600)).toBe('10 minutes');
    });
  });

  describe('isTrialExpired', () => {
    it('returns false when trial is active', () => {
      const now = Date.now();
      expect(isTrialExpired(now, 3)).toBe(false);
    });

    it('returns true when trial has expired', () => {
      const fourDaysAgo = Date.now() - 4 * 24 * 60 * 60 * 1000;
      expect(isTrialExpired(fourDaysAgo, 3)).toBe(true);
    });
  });

  describe('getTrialDaysRemaining', () => {
    it('returns correct days remaining', () => {
      const now = Date.now();
      expect(getTrialDaysRemaining(now, 3)).toBe(3);
    });

    it('returns 0 when trial expired', () => {
      const longAgo = Date.now() - 10 * 24 * 60 * 60 * 1000;
      expect(getTrialDaysRemaining(longAgo, 3)).toBe(0);
    });
  });
});
