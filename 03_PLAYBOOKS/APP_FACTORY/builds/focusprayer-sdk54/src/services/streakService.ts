/**
 * Streak Service
 * Provides streak-related messages and encouragement
 */

import { StreakData } from '../stores/devotionStore';

/**
 * Get a message based on current streak
 */
export function getStreakMessage(streak: StreakData): string {
  const { currentStreak } = streak;

  if (currentStreak === 0) {
    return 'Start your streak today!';
  } else if (currentStreak === 1) {
    return 'Great start! Keep it going tomorrow.';
  } else if (currentStreak < 7) {
    return `${currentStreak} days strong! Building the habit.`;
  } else if (currentStreak < 14) {
    return `A full week! You're on fire.`;
  } else if (currentStreak < 30) {
    return `${currentStreak} days! Consistency is key.`;
  } else if (currentStreak < 60) {
    return `${currentStreak} days! You're transformed.`;
  } else if (currentStreak < 100) {
    return `${currentStreak} days! Incredible discipline.`;
  } else {
    return `${currentStreak} days! You're a prayer warrior!`;
  }
}

/**
 * Get encouragement message based on streak length
 */
export function getEncouragement(streakDays: number): string {
  const encouragements = [
    // 0 days
    [
      '"Seek first the kingdom of God." - Matthew 6:33',
      '"Draw near to God and He will draw near to you." - James 4:8',
      '"This is the day the Lord has made." - Psalm 118:24',
    ],
    // 1-3 days
    [
      'Every journey begins with a single step.',
      "You're planting seeds of faith.",
      'God honors your commitment.',
    ],
    // 4-7 days
    [
      "Habits form through repetition. You're doing it!",
      'Your dedication is inspiring.',
      'Prayer is changing you from the inside out.',
    ],
    // 8-14 days
    [
      "You've proven you can do this!",
      'Your consistency speaks volumes.',
      "Two weeks of devotion - that's powerful!",
    ],
    // 15-30 days
    [
      "A month of faithfulness is within reach!",
      "You're building something beautiful.",
      'Your prayer life is transforming.',
    ],
    // 31+ days
    [
      "You've made prayer a lifestyle.",
      'Your faithfulness is remarkable.',
      "You're an example to others.",
    ],
  ];

  let bracket = 0;
  if (streakDays >= 1 && streakDays <= 3) bracket = 1;
  else if (streakDays >= 4 && streakDays <= 7) bracket = 2;
  else if (streakDays >= 8 && streakDays <= 14) bracket = 3;
  else if (streakDays >= 15 && streakDays <= 30) bracket = 4;
  else if (streakDays > 30) bracket = 5;

  const options = encouragements[bracket];
  const index = Math.floor(Math.random() * options.length);
  return options[index];
}

/**
 * Check if streak is at risk (hasn't completed today and had a streak yesterday)
 */
export function isStreakAtRisk(streak: StreakData): boolean {
  return streak.currentStreak > 0;
}

/**
 * Get milestone for streak (returns null if not a milestone)
 */
export function getStreakMilestone(days: number): string | null {
  const milestones: Record<number, string> = {
    7: '1 Week',
    14: '2 Weeks',
    21: '3 Weeks',
    30: '1 Month',
    60: '2 Months',
    90: '3 Months',
    100: '100 Days',
    180: '6 Months',
    365: '1 Year',
  };

  return milestones[days] || null;
}

/**
 * Get celebration message for milestone
 */
export function getMilestoneCelebration(milestone: string): string {
  const celebrations: Record<string, string> = {
    '1 Week': 'A full week of faithfulness! Keep going!',
    '2 Weeks': 'Two weeks strong! This is becoming a habit.',
    '3 Weeks': 'Three weeks! Science says habits form in 21 days.',
    '1 Month': 'A whole month of daily devotion! Incredible!',
    '2 Months': 'Two months! Prayer is now part of who you are.',
    '3 Months': 'A quarter year of dedication. You inspire us!',
    '100 Days': '100 DAYS! A true prayer warrior!',
    '6 Months': 'Half a year of faithfulness. Remarkable!',
    '1 Year': 'ONE YEAR! What an incredible journey of faith!',
  };

  return celebrations[milestone] || `Congratulations on reaching ${milestone}!`;
}
