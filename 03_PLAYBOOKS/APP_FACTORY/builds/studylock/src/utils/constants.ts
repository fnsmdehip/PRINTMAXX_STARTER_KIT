import { FocusModeConfig, Subject, UserSettings } from '../types';

// Brand Colors
export const COLORS = {
  primary: '#0066FF',
  primaryDark: '#0052CC',
  primaryLight: '#4D94FF',
  secondary: '#00C853',
  accent: '#FF6B00',
  background: '#FFFFFF',
  surface: '#F5F7FA',
  surfaceAlt: '#E8ECF0',
  text: '#1A1A2E',
  textSecondary: '#6B7280',
  textMuted: '#9CA3AF',
  border: '#E5E7EB',
  error: '#EF4444',
  success: '#10B981',
  warning: '#F59E0B',
  white: '#FFFFFF',
  black: '#000000',
  overlay: 'rgba(0, 0, 0, 0.5)',
};

// Session Durations (in minutes)
export const SESSION_DURATIONS = [15, 25, 45, 60, 90];

// Focus Mode Configurations
export const FOCUS_MODES: Record<string, FocusModeConfig> = {
  pomodoro: {
    id: 'pomodoro',
    name: 'Pomodoro',
    description: '25 min work, 5 min break',
    workMinutes: 25,
    breakMinutes: 5,
    cycles: 4,
    quizFrequency: 'medium',
  },
  deepWork: {
    id: 'deepWork',
    name: 'Deep Work',
    description: '90 min continuous focus',
    workMinutes: 90,
    breakMinutes: 15,
    cycles: 1,
    quizFrequency: 'low',
  },
  examPrep: {
    id: 'examPrep',
    name: 'Exam Prep',
    description: 'Custom duration, quiz heavy',
    workMinutes: 45,
    breakMinutes: 0,
    cycles: 1,
    quizFrequency: 'high',
  },
  custom: {
    id: 'custom',
    name: 'Custom',
    description: 'Set your own duration',
    workMinutes: 30,
    breakMinutes: 5,
    cycles: 1,
    quizFrequency: 'medium',
  },
};

// Subject Options
export const SUBJECTS: { id: Subject; label: string; emoji: string }[] = [
  { id: 'general', label: 'General', emoji: '📚' },
  { id: 'math', label: 'Math', emoji: '🔢' },
  { id: 'science', label: 'Science', emoji: '🔬' },
  { id: 'history', label: 'History', emoji: '📜' },
  { id: 'geography', label: 'Geography', emoji: '🌍' },
  { id: 'literature', label: 'Literature', emoji: '📖' },
  { id: 'vocabulary', label: 'Vocabulary', emoji: '🔤' },
  { id: 'logic', label: 'Logic', emoji: '🧩' },
];

// Default User Settings
export const DEFAULT_SETTINGS: UserSettings = {
  defaultSessionLength: 25,
  defaultFocusMode: 'pomodoro',
  quizDuringSession: true,
  quizAfterSession: true,
  penaltyMinutes: 5,
  notifications: true,
  haptics: true,
  soundEnabled: true,
};

// Free tier limits
export const FREE_TIER_LIMITS = {
  maxSessionMinutes: 25,
  sessionsPerDay: 3,
  quizQuestionsAccess: 20,
};

// Premium pricing
export const PREMIUM_PRICING = {
  monthly: {
    price: '$4.99',
    period: 'month',
    identifier: 'studylock_premium_monthly',
  },
  yearly: {
    price: '$29.99',
    period: 'year',
    savings: '50%',
    identifier: 'studylock_premium_yearly',
  },
};

// Quiz intervals (in seconds)
export const QUIZ_INTERVALS = {
  none: 0,
  low: 900, // 15 minutes
  medium: 600, // 10 minutes
  high: 300, // 5 minutes
};

// Storage Keys
export const STORAGE_KEYS = {
  userSettings: '@studylock_settings',
  userProgress: '@studylock_progress',
  studySessions: '@studylock_sessions',
  dailyStats: '@studylock_daily_stats',
  onboardingComplete: '@studylock_onboarding_complete',
  lastSessionDate: '@studylock_last_session_date',
};

// Animation Durations
export const ANIMATION = {
  fast: 150,
  normal: 300,
  slow: 500,
};

// Streak Thresholds for Achievements
export const STREAK_MILESTONES = [3, 7, 14, 30, 60, 100, 365];
