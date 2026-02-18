/**
 * PrayerLock Core Types
 * All TypeScript interfaces for the application
 */

// User settings stored in AsyncStorage
export interface UserSettings {
  blockedApps: string[];
  devotionDurationMinutes: number;
  dailyResetTime: string;
  requireScripture: boolean;
  requireTimer: boolean;
  emergencyUnlockEnabled: boolean;
  notificationsEnabled: boolean;
  onboardingComplete: boolean;
}

// A single devotion session record
export interface DevotionSession {
  id: string;
  date: string;
  startedAt: number;
  completedAt: number | null;
  timerDuration: number;
  scriptureRead: boolean;
  scripturePassage: string;
  wasEmergencyUnlock: boolean;
}

// Streak tracking data
export interface StreakData {
  currentStreak: number;
  longestStreak: number;
  totalDaysCompleted: number;
  completedDates: string[];
  lastCompletedDate: string | null;
}

// Subscription state from RevenueCat
export interface SubscriptionState {
  isSubscribed: boolean;
  isTrialing: boolean;
  trialEndsAt: number | null;
  subscriptionType: 'monthly' | 'annual' | 'lifetime' | null;
  expiresAt: number | null;
}

// Bible API response from bible-api.com
export interface BibleVerse {
  book_id: string;
  book_name: string;
  chapter: number;
  verse: number;
  text: string;
}

export interface BiblePassage {
  reference: string;
  verses: BibleVerse[];
  text: string;
  translation_id: string;
}

// App info for blocking selection
export interface AppInfo {
  packageName: string;
  appName: string;
  isBlocked: boolean;
  category: 'social' | 'game' | 'entertainment' | 'other';
}

// Navigation types
export type RootStackParamList = {
  Onboarding: undefined;
  Main: undefined;
  Timer: undefined;
  Scripture: undefined;
  Paywall: undefined;
  EmergencyUnlock: undefined;
};

export type MainTabParamList = {
  Home: undefined;
  Stats: undefined;
  Settings: undefined;
};

// Devotion status for the day
export type DevotionStatus = 'not_started' | 'in_progress' | 'completed' | 'bypassed';
