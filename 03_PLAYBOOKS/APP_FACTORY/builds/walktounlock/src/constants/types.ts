export interface UserStats {
  totalSteps: number;
  currentStreak: number;
  longestStreak: number;
  totalDaysActive: number;
  lastActiveDate: string;
  achievements: string[];
  weeklySteps: DailySteps[];
  monthlySteps: DailySteps[];
  personalRecords: PersonalRecords;
}

export interface DailySteps {
  date: string;
  steps: number;
  goalMet: boolean;
  goal: number;
}

export interface PersonalRecords {
  mostStepsInDay: number;
  mostStepsInWeek: number;
  longestStreak: number;
  fastestUnlock: number;
}

export interface Settings {
  stepGoal: number;
  lockEnabled: boolean;
  lockStartTime: string;
  lockEndTime: string;
  weekendStepGoal: number;
  hapticFeedback: boolean;
  notifications: boolean;
  isPremium: boolean;
  whitelistedApps: string[];
}

export interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  requirement: number;
  type: 'steps' | 'streak' | 'unlock' | 'total';
  tier: 'bronze' | 'silver' | 'gold';
  unlockedAt?: string;
}

export interface LockState {
  isLocked: boolean;
  currentSteps: number;
  requiredSteps: number;
  unlockTime?: string;
}

export type RootStackParamList = {
  Onboarding: undefined;
  Main: undefined;
  Lock: undefined;
  Paywall: undefined;
};

export type MainTabParamList = {
  Home: undefined;
  Stats: undefined;
  Settings: undefined;
};
