import { ModeConfig, StreakMode } from '../types';

export const MODES: Record<StreakMode, ModeConfig> = {
  nofap: {
    id: 'nofap',
    label: 'NoFap',
    emoji: '🔒',
    tagline: 'Reclaim your energy. Rebuild your life.',
    milestoneMessages: {
      1: 'Day 1. The hardest step is the one you already took.',
      3: '72 hours. Dopamine is starting to reset.',
      7: 'One week. Your brain chemistry is measurably changing.',
      14: 'Two weeks. Most people quit before this. You didn\'t.',
      30: '30 days. Your testosterone is at its highest in years.',
      60: '60 days. You are in the top 5% of attempts. Keep going.',
      90: '90 days. You\'ve completed the reboot. This is who you are now.',
    },
    urgePrompts: [
      'Urge surfing: Close your eyes. The urge is a wave — it peaks in 10-20 minutes and passes. You don\'t have to act on it.',
      'Your streak is your answer. Every day you add to it is proof of who you\'re becoming.',
      'The urge is a signal — something is missing. What is it really? Stress? Loneliness? Boredom? Address that.',
      'Cold water. Right now. Splash your face or take a 30-second cold shower. It works.',
      'Call or text one person right now. The urge loses power when you break isolation.',
    ],
    dailyIntentions: [
      'Today I choose clarity over comfort.',
      'My energy belongs to things that build me up.',
      'I am not the urge. I am the one who chooses.',
      'Every clean day compounds. I am investing in myself.',
      'What I resist today makes me stronger tomorrow.',
    ],
  },
  alcohol: {
    id: 'alcohol',
    label: 'Alcohol Free',
    emoji: '🧊',
    tagline: 'Clear mind. Better sleep. Real energy.',
    milestoneMessages: {
      1: 'Day 1. Your body already started healing.',
      3: '72 hours. Sleep quality improving. Brain fog lifting.',
      7: 'One week. Liver enzymes normalizing. Skin clearing.',
      14: 'Two weeks. Blood pressure measurably lower.',
      30: '30 days. You\'ve broken the habit loop.',
      60: '60 days. Cognitive function at its best in years.',
      90: '90 days. Your relationship with alcohol has changed permanently.',
    },
    urgePrompts: [
      'Delay by 15 minutes. Drink sparkling water with ice right now. The craving will pass.',
      'Name why you started. Read your reason from day one.',
      'Your streak is the answer. One drink ends all of it.',
      'Walk outside for 5 minutes. Fresh air changes your state immediately.',
    ],
    dailyIntentions: [
      'Today I choose presence over escape.',
      'I deserve to wake up clear-headed.',
      'My habits are building the life I want.',
      'I don\'t need a drink to deal with this.',
    ],
  },
  smoking: {
    id: 'smoking',
    label: 'Quit Smoking',
    emoji: '🫁',
    tagline: 'Your lungs are healing right now.',
    milestoneMessages: {
      1: 'Day 1. Carbon monoxide in your blood is already dropping.',
      3: '72 hours. Nicotine is fully cleared from your body.',
      7: 'One week. Taste and smell are returning.',
      14: 'Two weeks. Circulation improving, walking gets easier.',
      30: '30 days. Lung function increasing.',
      60: '60 days. Risk of heart attack already declining.',
      90: 'Three months. Coughing and shortness of breath reduced by half.',
    },
    urgePrompts: [
      'The craving lasts 3-5 minutes. Set a timer. Do something physical.',
      'Drink cold water slowly. It helps.',
      'Deep breath in for 4 counts, hold 7, out for 8. Do it twice.',
      'The cigarette will not solve what\'s bothering you. What will?',
    ],
    dailyIntentions: [
      'Today I breathe freely.',
      'I am not a smoker. That is the past.',
      'My body is healing every hour I stay clean.',
      'I don\'t smoke anymore.',
    ],
  },
  gambling: {
    id: 'gambling',
    label: 'Gambling Free',
    emoji: '🎯',
    tagline: 'Your money. Your future. Your call.',
    milestoneMessages: {
      1: 'Day 1. The hardest day. You made it.',
      7: 'One week. Money stayed in your account.',
      14: 'Two weeks. The chase is not controlling you.',
      30: '30 days. Your financial health is recovering.',
      60: '60 days. You are proving it is possible.',
      90: '90 days. The pattern is broken.',
    },
    urgePrompts: [
      'Delay by 30 minutes. The urge will subside.',
      'Calculate what this streak has saved you. Real money.',
      'Call your support person. Not later — now.',
      'Block the apps/sites right now if you haven\'t.',
    ],
    dailyIntentions: [
      'Today I keep what I earn.',
      'My future self is counting on today\'s choices.',
      'I don\'t need the rush. I need the peace.',
      'Control over money is control over my life.',
    ],
  },
  custom: {
    id: 'custom',
    label: 'Custom',
    emoji: '⭐',
    tagline: 'Your journey. Your rules.',
    milestoneMessages: {
      1: 'Day 1. You committed. That matters.',
      7: 'One week of choice.',
      14: 'Two weeks strong.',
      30: '30 days. Real change takes root here.',
      60: '60 days. You are not the same person.',
      90: '90 days. You proved it to yourself.',
    },
    urgePrompts: [
      'Pause. Breathe. You have been here before and you made it through.',
      'Your streak is the answer. Remember why you started.',
      'What would future-you say right now?',
    ],
    dailyIntentions: [
      'Today I choose my commitment.',
      'Progress over perfection.',
      'Every day I stick to this is a win.',
    ],
  },
};

export const MILESTONE_DAYS = [1, 3, 7, 14, 30, 60, 90, 180, 365];

export function getMilestoneForDay(day: number): number | null {
  return MILESTONE_DAYS.find(m => m === day) ?? null;
}

export function getNextMilestone(currentDay: number): number {
  return MILESTONE_DAYS.find(m => m > currentDay) ?? 365;
}
