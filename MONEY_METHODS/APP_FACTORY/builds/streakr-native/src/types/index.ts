// ─── Core domain types ───────────────────────────────────────────────────────

export type HabitCategory =
  | 'fitness'
  | 'mindfulness'
  | 'learning'
  | 'creation'
  | 'health'
  | 'sobriety'
  | 'custom';

export interface Habit {
  id: string;                 // uuid-like: habit_<timestamp>
  name: string;               // "Morning run"
  emoji: string;              // "🏃"
  category: HabitCategory;
  createdAt: string;          // ISO string
  // Streak tracking
  currentStreak: number;
  longestStreak: number;
  totalCompletions: number;
  checkIns: string[];         // ISO date strings (one per day)
  lastCheckIn: string | null; // ISO string
  // MVD (Minimum Viable Day) config
  mvdEnabled: boolean;
  mvdLabel: string;           // "Just put on shoes and do 1 pushup"
  // Streak repair (premium)
  repairedDays: string[];     // days that were repaired, not to be counted as broken
}

export interface AppSettings {
  onboardingComplete: boolean;
  isPremium: boolean;
  reminderEnabled: boolean;
  reminderTime: string;       // "HH:MM"
  mvdMode: boolean;           // global MVD toggle
  hasReviewedApp: boolean;
  lastReviewPrompt: string | null; // ISO date
}

// ─── Navigation ──────────────────────────────────────────────────────────────

export type RootStackParamList = {
  Splash: undefined;
  Onboarding: undefined;
  Main: undefined;
  Paywall: { source: 'habit_limit' | 'mvd_history' | 'streak_repair' | 'share' | 'settings' };
  HabitDetail: { habitId: string };
  AddHabit: undefined;
};

export type MainTabParamList = {
  Today: undefined;
  Progress: undefined;
  Settings: undefined;
};
