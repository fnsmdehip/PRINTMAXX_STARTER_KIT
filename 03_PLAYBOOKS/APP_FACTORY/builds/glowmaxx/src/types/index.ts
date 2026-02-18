// User Gender
export type Gender = 'male' | 'female' | 'other';

// Routine Types
export type RoutineType =
  | 'morning_skincare'
  | 'evening_skincare'
  | 'mewing'
  | 'facial_exercises'
  | 'debloating'
  | 'posture';

// Exercise Categories
export type ExerciseCategory =
  | 'jawline'
  | 'cheekbones'
  | 'neck'
  | 'eyes'
  | 'forehead'
  | 'overall';

// Single Exercise
export interface Exercise {
  id: string;
  name: string;
  description: string;
  duration: number; // seconds
  category: ExerciseCategory;
  instructions: string[];
  forGender: Gender | 'all';
  imageUrl?: string;
}

// Routine
export interface Routine {
  id: string;
  name: string;
  type: RoutineType;
  description: string;
  exercises: Exercise[];
  totalDuration: number; // seconds
  forGender: Gender | 'all';
}

// Progress Photo
export interface ProgressPhoto {
  id: string;
  uri: string;
  date: string; // ISO date
  angle: 'front' | 'left' | 'right' | 'below';
  notes?: string;
}

// Daily Log
export interface DailyLog {
  date: string; // ISO date
  waterIntake: number; // ml
  sodiumLevel: 'low' | 'medium' | 'high';
  sleepHours: number;
  completedRoutines: string[]; // routine IDs
  mewingMinutes: number;
  notes?: string;
}

// Streak Data
export interface StreakData {
  currentStreak: number;
  longestStreak: number;
  totalDaysCompleted: number;
  completedDates: string[];
  lastCompletedDate: string | null;
}

// User Settings
export interface UserSettings {
  gender: Gender;
  age: number;
  hasCompletedOnboarding: boolean;
  trialStartDate: string | null;
  notificationsEnabled: boolean;
  mewingRemindersEnabled: boolean;
  mewingReminderInterval: number; // minutes
  morningRoutineTime: string; // HH:mm
  eveningRoutineTime: string; // HH:mm
  dailyGoals: {
    waterIntake: number; // ml
    mewingMinutes: number;
    routinesToComplete: string[]; // routine IDs
  };
}

// Subscription State
export interface SubscriptionState {
  isSubscribed: boolean;
  isInTrial: boolean;
  trialDaysRemaining: number;
  expirationDate: string | null;
}

// Mewing Session
export interface MewingSession {
  id: string;
  startTime: string;
  endTime: string;
  duration: number; // seconds
  date: string;
}

// Achievement
export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  unlockedAt: string | null;
  requirement: {
    type: 'streak' | 'total_days' | 'mewing_minutes' | 'photos' | 'routines';
    value: number;
  };
}

// Guide Content
export interface GuideSection {
  id: string;
  title: string;
  content: string;
  category: 'softmaxxing' | 'hardmaxxing' | 'leanmaxxing' | 'debloating' | 'mewing' | 'skincare';
  isPremium: boolean;
}
