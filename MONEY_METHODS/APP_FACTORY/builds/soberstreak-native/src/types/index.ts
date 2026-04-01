export type StreakMode = 'nofap' | 'alcohol' | 'smoking' | 'gambling' | 'custom';

export interface ModeConfig {
  id: StreakMode;
  label: string;
  emoji: string;
  tagline: string;
  milestoneMessages: Record<number, string>;
  urgePrompts: string[];
  dailyIntentions: string[];
}

export interface StreakData {
  mode: StreakMode;
  customLabel?: string;
  startDate: string;           // ISO string of the current streak start
  lastCheckIn: string | null;  // ISO string of last check-in
  currentStreak: number;       // days
  longestStreak: number;
  totalAttempts: number;
  totalCleanDays: number;
  checkIns: string[];          // ISO date strings of all check-ins
}

export interface AppSettings {
  reminderEnabled: boolean;
  reminderTime: string;        // "HH:MM"
  isPremium: boolean;
  onboardingComplete: boolean;
  hasSeenEmergencyPrompt: boolean;
}

export type RootStackParamList = {
  Splash: undefined;
  Onboarding: undefined;
  Main: undefined;
  Paywall: { source: string };
  Emergency: undefined;
};

export type MainTabParamList = {
  Today: undefined;
  Milestones: undefined;
  Settings: undefined;
};
