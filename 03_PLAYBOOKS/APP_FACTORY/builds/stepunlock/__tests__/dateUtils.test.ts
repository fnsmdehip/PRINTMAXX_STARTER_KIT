import {
  getTodayDateString,
  formatDateString,
  parseDateString,
  getStartOfDay,
  getEndOfDay,
  isToday,
  isYesterday,
  getDaysBetween,
  getLastNDays,
  formatTimeRemaining,
  estimateWalkingTime,
  estimateDistance,
  formatDistance,
} from '../src/utils/dateUtils';

describe('dateUtils', () => {
  describe('getTodayDateString', () => {
    it('returns date in YYYY-MM-DD format', () => {
      const result = getTodayDateString();
      expect(result).toMatch(/^\d{4}-\d{2}-\d{2}$/);
    });
  });

  describe('formatDateString', () => {
    it('formats date correctly', () => {
      const date = new Date(2025, 0, 15); // Jan 15, 2025
      expect(formatDateString(date)).toBe('2025-01-15');
    });

    it('pads single digit months and days', () => {
      const date = new Date(2025, 4, 5); // May 5, 2025
      expect(formatDateString(date)).toBe('2025-05-05');
    });
  });

  describe('parseDateString', () => {
    it('parses YYYY-MM-DD string correctly', () => {
      const result = parseDateString('2025-01-15');
      expect(result.getFullYear()).toBe(2025);
      expect(result.getMonth()).toBe(0); // January is 0
      expect(result.getDate()).toBe(15);
    });
  });

  describe('getStartOfDay', () => {
    it('returns date with time set to 00:00:00.000', () => {
      const date = new Date(2025, 0, 15, 14, 30, 45);
      const result = getStartOfDay(date);
      expect(result.getHours()).toBe(0);
      expect(result.getMinutes()).toBe(0);
      expect(result.getSeconds()).toBe(0);
      expect(result.getMilliseconds()).toBe(0);
    });
  });

  describe('getEndOfDay', () => {
    it('returns date with time set to 23:59:59.999', () => {
      const date = new Date(2025, 0, 15, 14, 30, 45);
      const result = getEndOfDay(date);
      expect(result.getHours()).toBe(23);
      expect(result.getMinutes()).toBe(59);
      expect(result.getSeconds()).toBe(59);
      expect(result.getMilliseconds()).toBe(999);
    });
  });

  describe('isToday', () => {
    it('returns true for today', () => {
      const today = new Date();
      expect(isToday(today)).toBe(true);
    });

    it('returns false for yesterday', () => {
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      expect(isToday(yesterday)).toBe(false);
    });

    it('works with string dates', () => {
      const todayString = getTodayDateString();
      expect(isToday(todayString)).toBe(true);
    });
  });

  describe('isYesterday', () => {
    it('returns true for yesterday', () => {
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      expect(isYesterday(yesterday)).toBe(true);
    });

    it('returns false for today', () => {
      const today = new Date();
      expect(isYesterday(today)).toBe(false);
    });
  });

  describe('getDaysBetween', () => {
    it('calculates days between two dates', () => {
      const date1 = '2025-01-01';
      const date2 = '2025-01-10';
      expect(getDaysBetween(date1, date2)).toBe(9);
    });

    it('works with Date objects', () => {
      const date1 = new Date(2025, 0, 1);
      const date2 = new Date(2025, 0, 10);
      expect(getDaysBetween(date1, date2)).toBe(9);
    });
  });

  describe('getLastNDays', () => {
    it('returns array of date strings', () => {
      const result = getLastNDays(7);
      expect(result).toHaveLength(7);
      expect(result[0]).toBe(getTodayDateString());
    });

    it('dates are in descending order', () => {
      const result = getLastNDays(3);
      expect(result[0] > result[1]).toBe(true);
      expect(result[1] > result[2]).toBe(true);
    });
  });

  describe('formatTimeRemaining', () => {
    it('formats minutes under 60', () => {
      expect(formatTimeRemaining(30)).toBe('30 min');
    });

    it('formats hours and minutes', () => {
      expect(formatTimeRemaining(90)).toBe('1h 30m');
    });

    it('formats exact hours without minutes', () => {
      expect(formatTimeRemaining(120)).toBe('2h');
    });
  });

  describe('estimateWalkingTime', () => {
    it('estimates ~10 minutes per 1000 steps', () => {
      expect(estimateWalkingTime(1000)).toBe(10);
      expect(estimateWalkingTime(5000)).toBe(50);
    });
  });

  describe('estimateDistance', () => {
    it('estimates ~2000 steps per mile', () => {
      expect(estimateDistance(2000)).toBe(1);
      expect(estimateDistance(10000)).toBe(5);
    });
  });

  describe('formatDistance', () => {
    it('formats distance with one decimal place', () => {
      expect(formatDistance(2.5)).toBe('2.5 mi');
      expect(formatDistance(1)).toBe('1.0 mi');
    });
  });
});
