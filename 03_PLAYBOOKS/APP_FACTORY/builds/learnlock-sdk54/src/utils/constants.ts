// Storage Keys
export const STORAGE_KEYS = {
  USER_SETTINGS: '@studylock/user_settings',
  TIMER_DATA: '@studylock/timer_data',
  STUDY_HISTORY: '@studylock/study_history',
  STREAK_DATA: '@studylock/streak_data',
  SUBSCRIPTION: '@studylock/subscription',
  ONBOARDING_COMPLETE: '@studylock/onboarding_complete',
  TRIAL_START: '@studylock/trial_start',
};

// Timer Defaults
export const DEFAULT_WORK_DURATION = 25; // minutes
export const DEFAULT_BREAK_DURATION = 5; // minutes
export const MIN_WORK_DURATION = 5;
export const MAX_WORK_DURATION = 60;
export const MIN_BREAK_DURATION = 1;
export const MAX_BREAK_DURATION = 15;

// Streak Requirements
export const MIN_STUDY_TIME_FOR_STREAK = 25 * 60; // 25 minutes in seconds

// Trial Duration
export const TRIAL_DURATION_DAYS = 7;

// Pricing
export const PRICING = {
  monthly: {
    price: 6.99,
    period: 'month',
    productId: 'studylock_monthly',
  },
  annual: {
    price: 34.99,
    period: 'year',
    productId: 'studylock_annual',
    savings: '58%',
  },
  lifetime: {
    price: 69.99,
    period: 'lifetime',
    productId: 'studylock_lifetime',
  },
};

// Colors
export const COLORS = {
  primary: '#4F46E5', // Indigo
  primaryLight: '#818CF8',
  primaryDark: '#3730A3',
  secondary: '#10B981', // Emerald (for success/streaks)
  secondaryLight: '#34D399',
  background: '#F9FAFB',
  surface: '#FFFFFF',
  surfaceSecondary: '#F3F4F6',
  text: '#111827',
  textSecondary: '#6B7280',
  textTertiary: '#9CA3AF',
  error: '#EF4444',
  warning: '#F59E0B',
  border: '#E5E7EB',
  // Timer specific
  timerWork: '#4F46E5',
  timerBreak: '#10B981',
  timerBackground: '#E0E7FF',
};

// Typography
export const TYPOGRAPHY = {
  h1: {
    fontSize: 32,
    fontWeight: '700' as const,
    lineHeight: 40,
  },
  h2: {
    fontSize: 24,
    fontWeight: '600' as const,
    lineHeight: 32,
  },
  h3: {
    fontSize: 20,
    fontWeight: '600' as const,
    lineHeight: 28,
  },
  body: {
    fontSize: 16,
    fontWeight: '400' as const,
    lineHeight: 24,
  },
  bodySmall: {
    fontSize: 14,
    fontWeight: '400' as const,
    lineHeight: 20,
  },
  caption: {
    fontSize: 12,
    fontWeight: '400' as const,
    lineHeight: 16,
  },
  timer: {
    fontSize: 64,
    fontWeight: '700' as const,
    lineHeight: 72,
  },
};

// Spacing
export const SPACING = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

// Default Blocked Apps (bundle IDs)
export const DEFAULT_BLOCKED_APPS = [
  { id: '1', name: 'TikTok', bundleId: 'com.zhiliaoapp.musically' },
  { id: '2', name: 'Instagram', bundleId: 'com.burbn.instagram' },
  { id: '3', name: 'Twitter', bundleId: 'com.twitter.android' },
  { id: '4', name: 'YouTube', bundleId: 'com.google.android.youtube' },
  { id: '5', name: 'Snapchat', bundleId: 'com.snapchat.android' },
  { id: '6', name: 'Discord', bundleId: 'com.discord' },
  { id: '7', name: 'Reddit', bundleId: 'com.reddit.frontpage' },
  { id: '8', name: 'Facebook', bundleId: 'com.facebook.katana' },
];

// Emergency Unlock Phrase
export const EMERGENCY_UNLOCK_PHRASE = 'I am quitting my study session';

// App Store Links (for sharing)
export const APP_STORE_LINK = 'https://apps.apple.com/app/learnlock/id123456789';
export const PLAY_STORE_LINK = 'https://play.google.com/store/apps/details?id=com.printmaxx.learnlock';

// Timer Presets
export interface TimerPreset {
  id: string;
  name: string;
  workMinutes: number;
  breakMinutes: number;
  description: string;
}

export const TIMER_PRESETS: TimerPreset[] = [
  {
    id: 'quick',
    name: 'Quick Focus',
    workMinutes: 15,
    breakMinutes: 3,
    description: 'Short bursts for light tasks',
  },
  {
    id: 'classic',
    name: 'Classic Pomodoro',
    workMinutes: 25,
    breakMinutes: 5,
    description: 'Proven effective technique',
  },
  {
    id: 'deep',
    name: 'Deep Work',
    workMinutes: 45,
    breakMinutes: 10,
    description: 'For intensive studying',
  },
  {
    id: 'marathon',
    name: 'Marathon',
    workMinutes: 60,
    breakMinutes: 15,
    description: 'Extended focus sessions',
  },
];

// Motivational Quotes (shown during sessions)
export const STUDY_QUOTES: string[] = [
  'The secret of getting ahead is getting started.',
  'Small progress is still progress.',
  'Your future self will thank you.',
  'Focus on progress, not perfection.',
  'Every expert was once a beginner.',
  'The only way to do great work is to love what you do.',
  'Success is the sum of small efforts repeated.',
  'Stay focused. Your goals are closer than they appear.',
  'Discipline is choosing between what you want now and what you want most.',
  'The harder you work, the luckier you get.',
];
