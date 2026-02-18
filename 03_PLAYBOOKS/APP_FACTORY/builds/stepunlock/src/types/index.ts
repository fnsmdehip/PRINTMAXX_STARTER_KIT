// User Settings
export interface UserSettings {
  stepGoal: number; // 1000-20000
  blockedApps: BlockedApp[];
  dailyResetTime: string; // "00:00" (midnight default)
  notificationsEnabled: boolean;
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

// Step Data
export interface StepData {
  date: string; // YYYY-MM-DD
  steps: number;
  goalMet: boolean;
  unlockedAt: number | null; // timestamp
  wasEmergencyUnlock: boolean;
}

// Streak Data
export interface StreakData {
  currentStreak: number;
  longestStreak: number;
  totalDaysCompleted: number;
  completedDates: string[];
  lastCompletedDate: string | null;
}

// App State
export interface AppState {
  currentSteps: number;
  stepGoal: number;
  isUnlocked: boolean;
  lastUpdated: number; // timestamp
  todayCompleted: boolean;
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
  EmergencyUnlock: undefined;
};

export type MainTabParamList = {
  Home: undefined;
  Progress: undefined;
  Settings: undefined;
};

// Health Data Types
export interface HealthPermissionStatus {
  steps: boolean;
}

// Step Goal Presets
export interface StepGoalPreset {
  value: number;
  label: string;
  description: string;
  time: string;
  distance: string;
}

export const STEP_GOAL_PRESETS: StepGoalPreset[] = [
  {
    value: 3000,
    label: 'Light',
    description: 'Good starting point',
    time: '30 min',
    distance: '1.5 mi',
  },
  {
    value: 5000,
    label: 'Moderate',
    description: 'Recommended for most',
    time: '50 min',
    distance: '2.5 mi',
  },
  {
    value: 8000,
    label: 'Active',
    description: 'For daily walkers',
    time: '80 min',
    distance: '4 mi',
  },
  {
    value: 10000,
    label: 'Very Active',
    description: 'Classic goal',
    time: '100 min',
    distance: '5 mi',
  },
];
