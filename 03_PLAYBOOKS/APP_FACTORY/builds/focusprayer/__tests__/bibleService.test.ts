/**
 * Bible Service Tests
 */

import { getPassageForDay, DAILY_PASSAGES } from '../src/services/bibleService';

describe('bibleService', () => {
  describe('DAILY_PASSAGES', () => {
    it('has 365 passages defined', () => {
      expect(DAILY_PASSAGES.length).toBeGreaterThanOrEqual(365);
    });

    it('all passages are non-empty strings', () => {
      DAILY_PASSAGES.forEach((passage, index) => {
        expect(typeof passage).toBe('string');
        expect(passage.length).toBeGreaterThan(0);
      });
    });

    it('contains expected passages', () => {
      expect(DAILY_PASSAGES).toContain('Psalm 23');
      expect(DAILY_PASSAGES).toContain('John 3:16-17');
      expect(DAILY_PASSAGES).toContain('Philippians 4:13');
    });
  });

  describe('getPassageForDay', () => {
    it('returns first passage for day 1', () => {
      const passage = getPassageForDay(1);
      expect(passage).toBe(DAILY_PASSAGES[0]);
    });

    it('wraps around after 365 days', () => {
      const passage366 = getPassageForDay(366);
      expect(passage366).toBe(DAILY_PASSAGES[0]);
    });

    it('returns correct passage for specific day', () => {
      const passage = getPassageForDay(100);
      expect(passage).toBe(DAILY_PASSAGES[99]);
    });
  });
});
