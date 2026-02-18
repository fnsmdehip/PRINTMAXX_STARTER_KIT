// User Settings
export interface UserSettings {
  workDuration: number; // minutes (5-60)
  breakDuration: number; // minutes (1-15)
  blockedApps: BlockedApp[];
  dailyResetTime: string; // "00:00" (midnight default)
  notificationsEnabled: boolean;
  soundEnabled: boolean;
  vibrationEnabled: boolean;
  emergencyUnlockEnabled: boolean;
  hasCompletedOnboarding: boolean;
  trialStartDate: string | null; // ISO date string
}

export interface BlockedApp {
  id: string;
  name: string;
  bundleId: string;
  icon?: string;
}

// Timer State
export type TimerState = 'idle' | 'studying' | 'break' | 'paused';

export interface TimerData {
  state: TimerState;
  remainingSeconds: number;
  totalSeconds: number;
  sessionStartTime: number | null; // timestamp
  currentSessionType: 'work' | 'break';
}

// Session Data
export interface StudySession {
  id: string;
  date: string; // YYYY-MM-DD
  startTime: number; // timestamp
  endTime: number | null; // timestamp
  duration: number; // seconds
  completed: boolean;
  wasInterrupted: boolean;
}

// Daily Study Data
export interface DailyStudyData {
  date: string; // YYYY-MM-DD
  totalStudyTime: number; // seconds
  sessionsCompleted: number;
  streakMaintained: boolean;
  sessions: StudySession[];
}

// Streak Data
export interface StreakData {
  currentStreak: number;
  longestStreak: number;
  totalDaysStudied: number;
  totalStudyHours: number;
  completedDates: string[];
  lastStudyDate: string | null;
}

// App State
export interface AppState {
  isBlocked: boolean;
  currentTimer: TimerData;
  todayStudyTime: number; // seconds
  todaySessionsCompleted: number;
}

// Subscription State
export interface SubscriptionState {
  isSubscribed: boolean;
  isInTrial: boolean;
  trialDaysRemaining: number;
  expirationDate: string | null;
}

// Navigation Types
export type RootStackParamList = {
  Onboarding: undefined;
  Main: undefined;
  Paywall: undefined;
  ActiveSession: undefined;
  EmergencyUnlock: undefined;
};

export type MainTabParamList = {
  Home: undefined;
  Stats: undefined;
  Settings: undefined;
};

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

// Stats Time Ranges
export type StatsTimeRange = 'today' | 'week' | 'month' | 'all';

// Study Stats
export interface StudyStats {
  totalStudyTime: number; // seconds
  sessionsCompleted: number;
  averageSessionLength: number; // seconds
  longestSession: number; // seconds
  currentStreak: number;
  longestStreak: number;
}

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
