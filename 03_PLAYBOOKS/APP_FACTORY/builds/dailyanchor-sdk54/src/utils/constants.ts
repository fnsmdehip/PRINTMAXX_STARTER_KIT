import { Habit } from '../types';

export const STORAGE_KEYS = {
  HABITS: '@dailyanchor/habits',
  COMPLETIONS: '@dailyanchor/completions',
  JOURNAL: '@dailyanchor/journal',
  STREAK: '@dailyanchor/streak',
  SETTINGS: '@dailyanchor/settings',
  VERSE_CACHE: '@dailyanchor/verse_cache',
} as const;

export const DEFAULT_HABITS: Omit<Habit, 'id' | 'createdAt'>[] = [
  {
    name: 'Read Bible',
    icon: 'book',
    isDefault: true,
    isPremium: false,
  },
  {
    name: 'Pray',
    icon: 'hands',
    isDefault: true,
    isPremium: false,
  },
  {
    name: 'Gratitude',
    icon: 'heart',
    isDefault: true,
    isPremium: false,
  },
];

export const PREMIUM_HABITS: Omit<Habit, 'id' | 'createdAt'>[] = [
  {
    name: 'Meditation',
    icon: 'moon',
    isDefault: false,
    isPremium: true,
  },
  {
    name: 'Scripture Memory',
    icon: 'brain',
    isDefault: false,
    isPremium: true,
  },
  {
    name: 'Fasting',
    icon: 'utensils',
    isDefault: false,
    isPremium: true,
  },
  {
    name: 'Church Attendance',
    icon: 'church',
    isDefault: false,
    isPremium: true,
  },
  {
    name: 'Serving Others',
    icon: 'hand-holding-heart',
    isDefault: false,
    isPremium: true,
  },
];

export const COLORS = {
  primary: '#6366F1', // Indigo
  primaryDark: '#4F46E5',
  secondary: '#10B981', // Emerald
  background: '#F8FAFC',
  card: '#FFFFFF',
  text: '#1E293B',
  textSecondary: '#64748B',
  border: '#E2E8F0',
  success: '#22C55E',
  warning: '#F59E0B',
  error: '#EF4444',
  streak: '#F59E0B',
  completed: '#22C55E',
} as const;

export const REVENUECAT_API_KEY = {
  ios: 'appl_XXXXX', // Replace with real key
  android: 'goog_XXXXX', // Replace with real key
} as const;

export const BIBLE_API_BASE = 'https://bible-api.com';

export const FOCUS_AREAS = [
  {
    id: 'building_habit',
    title: 'Building a daily habit',
    description: 'For new believers or returning to faith',
  },
  {
    id: 'deepening_prayer',
    title: 'Deepening my prayer life',
    description: 'For consistent believers wanting more',
  },
  {
    id: 'finding_peace',
    title: 'Finding peace in a busy season',
    description: 'For stressed or anxious times',
  },
  {
    id: 'growing_community',
    title: 'Growing with my church community',
    description: 'For church-connected believers',
  },
] as const;

export const DEFAULT_REMINDER_TIME = '07:00';
