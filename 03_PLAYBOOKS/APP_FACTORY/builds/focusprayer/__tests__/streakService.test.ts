/**
 * Streak Service Tests
 */

import {
  getStreakMessage,
  getEncouragement,
  isStreakAtRisk,
  getDaysSinceLastPrayer,
  generateCalendarMonth,
  getNextMilestone,
  getDaysToMilestone,
} from '../src/services/streakService';
import { StreakData } from '../src/types';

// Mock the dateUtils
jest.mock('../src/utils/dateUtils', () => ({
  getTodayString: jest.fn(() => '2024-01-15'),
  areConsecutiveDays: jest.fn((d1, d2) => {
    const diff = Math.abs(
      new Date(d1).getTime() - new Date(d2).getTime()
    );
    return Math.round(diff / (1000 * 60 * 60 * 24)) === 1;
  }),
  daysBetween: jest.fn((d1, d2) => {
    const diff = Math.abs(
      new Date(d1).getTime() - new Date(d2).getTime()
    );
    return Math.floor(diff / (1000 * 60 * 60 * 24));
  }),
}));

describe('streakService', () => {
  describe('getStreakMessage', () => {
    it('returns start message for zero streak', () => {
      const streak: StreakData = {
        currentStreak: 0,
        longestStreak: 0,
        totalDaysCompleted: 0,
        completedDates: [],
        lastCompletedDate: null,
      };
      expect(getStreakMessage(streak)).toBe('Start your prayer journey today');
    });

    it('returns restart message after broken streak', () => {
      const streak: StreakData = {
        currentStreak: 0,
        longestStreak: 7,
        totalDaysCompleted: 10,
        completedDates: [],
        lastCompletedDate: '2024-01-10',
      };
      expect(getStreakMessage(streak)).toContain('best streak was 7 day');
    });

    it('returns personal best message', () => {
      const streak: StreakData = {
        currentStreak: 10,
        longestStreak: 10,
        totalDaysCompleted: 10,
        completedDates: [],
        lastCompletedDate: '2024-01-15',
      };
      expect(getStreakMessage(streak)).toContain('Personal best');
    });
  });

  describe('getEncouragement', () => {
    it('returns appropriate message for day 1', () => {
      expect(getEncouragement(1)).toContain('Day 1');
    });

    it('returns week message at day 7', () => {
      expect(getEncouragement(7)).toContain('week');
    });

    it('returns habit message at day 21', () => {
      expect(getEncouragement(21)).toContain('habit');
    });

    it('returns month message at day 30', () => {
      expect(getEncouragement(30)).toContain('month');
    });

    it('returns year message at day 365', () => {
      expect(getEncouragement(365)).toContain('year');
    });
  });

  describe('isStreakAtRisk', () => {
    it('returns false when no streak', () => {
      const streak: StreakData = {
        currentStreak: 0,
        longestStreak: 0,
        totalDaysCompleted: 0,
        completedDates: [],
        lastCompletedDate: null,
      };
      expect(isStreakAtRisk(streak)).toBe(false);
    });

    it('returns false when completed today', () => {
      const streak: StreakData = {
        currentStreak: 5,
        longestStreak: 5,
        totalDaysCompleted: 5,
        completedDates: ['2024-01-15'],
        lastCompletedDate: '2024-01-15', // Today
      };
      expect(isStreakAtRisk(streak)).toBe(false);
    });

    it('returns true when yesterday was completed but not today', () => {
      const streak: StreakData = {
        currentStreak: 5,
        longestStreak: 5,
        totalDaysCompleted: 5,
        completedDates: ['2024-01-14'],
        lastCompletedDate: '2024-01-14', // Yesterday
      };
      expect(isStreakAtRisk(streak)).toBe(true);
    });
  });

  describe('getDaysSinceLastPrayer', () => {
    it('returns -1 when never prayed', () => {
      expect(getDaysSinceLastPrayer(null)).toBe(-1);
    });

    it('returns 0 when prayed today', () => {
      expect(getDaysSinceLastPrayer('2024-01-15')).toBe(0);
    });

    it('returns correct days since last prayer', () => {
      expect(getDaysSinceLastPrayer('2024-01-10')).toBe(5);
    });
  });

  describe('generateCalendarMonth', () => {
    it('generates correct number of days', () => {
      const calendar = generateCalendarMonth(2024, 0, []); // January 2024
      expect(calendar.length).toBe(31);
    });

    it('marks completed dates', () => {
      const completedDates = ['2024-01-10', '2024-01-11'];
      const calendar = generateCalendarMonth(2024, 0, completedDates);

      const day10 = calendar.find(d => d.date === '2024-01-10');
      const day12 = calendar.find(d => d.date === '2024-01-12');

      expect(day10?.completed).toBe(true);
      expect(day12?.completed).toBe(false);
    });

    it('marks today correctly', () => {
      const calendar = generateCalendarMonth(2024, 0, []);
      const today = calendar.find(d => d.date === '2024-01-15');
      expect(today?.isToday).toBe(true);
    });
  });

  describe('getNextMilestone', () => {
    it('returns correct next milestone', () => {
      expect(getNextMilestone(0)).toBe(3);
      expect(getNextMilestone(2)).toBe(3);
      expect(getNextMilestone(3)).toBe(7);
      expect(getNextMilestone(7)).toBe(14);
      expect(getNextMilestone(90)).toBe(100);
      expect(getNextMilestone(100)).toBe(180);
    });
  });

  describe('getDaysToMilestone', () => {
    it('returns correct days remaining', () => {
      expect(getDaysToMilestone(5)).toBe(2); // Next is 7
      expect(getDaysToMilestone(20)).toBe(1); // Next is 21
      expect(getDaysToMilestone(99)).toBe(1); // Next is 100
    });
  });
});
