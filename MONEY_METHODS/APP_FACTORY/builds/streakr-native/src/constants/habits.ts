import { HabitCategory } from '../types';

export interface HabitPreset {
  name: string;
  emoji: string;
  category: HabitCategory;
  mvdLabel: string;           // the minimum viable day version
  milestoneMessages: Record<number, string>;
}

export const HABIT_PRESETS: HabitPreset[] = [
  // Fitness
  {
    name: 'Morning workout',
    emoji: '💪',
    category: 'fitness',
    mvdLabel: 'Do 5 pushups',
    milestoneMessages: {
      3: 'Three days moving. Your body is adapting.',
      7: 'One week of movement. Habit is forming.',
      14: 'Two weeks. Your body expects this now.',
      30: '30 days. You are a person who works out.',
      90: '90 days. This is just who you are.',
    },
  },
  {
    name: 'Daily run',
    emoji: '🏃',
    category: 'fitness',
    mvdLabel: 'Walk outside for 5 minutes',
    milestoneMessages: {
      3: 'Three days running. Lungs are adapting.',
      7: 'One week. Your resting heart rate is already dropping.',
      14: 'Two weeks of runs. This is becoming automatic.',
      30: '30 days. You are a runner.',
      90: 'Three months. Your pace, your distance, your identity.',
    },
  },
  {
    name: 'Cold shower',
    emoji: '🚿',
    category: 'health',
    mvdLabel: '10 seconds cold at the end',
    milestoneMessages: {
      3: 'Three cold showers. The shock is getting smaller.',
      7: 'One week. Your nervous system is recalibrating.',
      14: 'Two weeks. You actually look forward to this now.',
      30: '30 days. You are not the same person who started.',
      90: 'Three months of cold. Hard to rattle.',
    },
  },
  // Mindfulness
  {
    name: 'Meditation',
    emoji: '🧘',
    category: 'mindfulness',
    mvdLabel: '2 minutes of deep breathing',
    milestoneMessages: {
      3: 'Three days sitting with yourself. That takes courage.',
      7: 'One week. Your reaction times are measurably slowing.',
      14: 'Two weeks. You are getting harder to provoke.',
      30: '30 days of stillness. Compounding.',
      90: 'Three months. Different brain, different responses.',
    },
  },
  {
    name: 'Daily journaling',
    emoji: '📓',
    category: 'mindfulness',
    mvdLabel: 'Write one sentence',
    milestoneMessages: {
      3: 'Three days of honesty with yourself.',
      7: 'One week. You are processing instead of suppressing.',
      14: 'Two weeks of pages. Read the first entry again.',
      30: '30 days. You have built an archive of yourself.',
      90: 'Ninety days of reflection. You think differently now.',
    },
  },
  {
    name: 'No phone first hour',
    emoji: '📵',
    category: 'mindfulness',
    mvdLabel: 'No phone for 10 minutes after waking',
    milestoneMessages: {
      3: 'Three mornings owned by you, not your feed.',
      7: 'One week. Morning baseline anxiety is dropping.',
      14: 'Two weeks. Your brain gets to wake up on its own terms.',
      30: '30 days. You choose what enters your mind first.',
      90: 'Three months. The algorithm has less power over you.',
    },
  },
  // Learning
  {
    name: 'Daily reading',
    emoji: '📚',
    category: 'learning',
    mvdLabel: 'Read one page',
    milestoneMessages: {
      3: 'Three days of pages.',
      7: 'One week. You\'ve read more than most do in a month.',
      14: 'Two weeks. A book is taking shape.',
      30: '30 days. You finished something.',
      90: 'Three months of reading. Ideas compound like interest.',
    },
  },
  {
    name: 'Skill practice',
    emoji: '🎯',
    category: 'learning',
    mvdLabel: '5 minutes of deliberate practice',
    milestoneMessages: {
      3: 'Three days of reps.',
      7: 'One week in. Skills take 20 hours to get decent.',
      14: 'Two weeks. The plateau is about to end.',
      30: '30 days. You\'re in the top 10% of people who tried.',
      90: 'Three months of deliberate practice. Real ability.',
    },
  },
  {
    name: 'Deep work block',
    emoji: '🔒',
    category: 'learning',
    mvdLabel: '25-minute Pomodoro — no notifications',
    milestoneMessages: {
      3: 'Three deep work sessions. Flow state building.',
      7: 'One week of protected focus time.',
      14: 'Two weeks. Your capacity to focus is increasing.',
      30: '30 days of deep work. The output gap between you and distracted peers is widening.',
      90: 'Three months. You do in one focused hour what others do in four.',
    },
  },
  // Creation
  {
    name: 'Create something',
    emoji: '✍️',
    category: 'creation',
    mvdLabel: 'Ship one tweet / one paragraph / one sketch',
    milestoneMessages: {
      3: 'Three days creating. Most people only consume.',
      7: 'One week of output. A body of work is beginning.',
      14: 'Two weeks. You are building a creator identity.',
      30: '30 days of creation. The reps compound.',
      90: 'Three months of shipping. Audience + skill + confidence.',
    },
  },
  // Health
  {
    name: 'Drink 2L water',
    emoji: '💧',
    category: 'health',
    mvdLabel: 'Drink a full glass of water right now',
    milestoneMessages: {
      3: 'Three days hydrated. Skin and energy are responding.',
      7: 'One week of proper hydration. Cognitive performance up.',
      14: 'Two weeks. You can feel the difference on skipped days.',
      30: '30 days. Hydration is automatic now.',
      90: 'Three months. Your baseline health shifted.',
    },
  },
  {
    name: 'Early sleep',
    emoji: '🌙',
    category: 'health',
    mvdLabel: 'In bed by 11pm, phone off',
    milestoneMessages: {
      3: 'Three nights of real rest.',
      7: 'One week. REM cycles are deepening.',
      14: 'Two weeks of consistent sleep. Inflammation is dropping.',
      30: '30 days. Your energy baseline is different.',
      90: 'Three months of sleep discipline. Compounding restoration.',
    },
  },
];

export const MILESTONE_DAYS = [3, 7, 14, 30, 60, 90, 180, 365];

export function getMilestoneMessage(preset: HabitPreset | null, days: number): string {
  if (!preset) return `${days} days. Keep going.`;
  const keys = Object.keys(preset.milestoneMessages).map(Number).sort((a, b) => b - a);
  const match = keys.find(k => k <= days);
  return match ? preset.milestoneMessages[match] : `${days} days of ${preset.name.toLowerCase()}. Keep going.`;
}

export function getNextMilestone(current: number): number {
  return MILESTONE_DAYS.find(m => m > current) ?? 365;
}

export function getCategoryEmoji(category: HabitCategory): string {
  const map: Record<HabitCategory, string> = {
    fitness: '💪',
    mindfulness: '🧘',
    learning: '📚',
    creation: '✍️',
    health: '💚',
    custom: '⭐',
  };
  return map[category];
}
