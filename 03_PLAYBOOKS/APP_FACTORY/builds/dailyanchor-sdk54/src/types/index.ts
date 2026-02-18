// Core habit types
export interface Habit {
  id: string;
  name: string;
  icon: string;
  isDefault: boolean;
  isPremium: boolean;
  createdAt: string;
}

export interface HabitCompletion {
  habitId: string;
  date: string; // YYYY-MM-DD
  completedAt: string;
}

// Journal types
export interface JournalEntry {
  id: string;
  date: string; // YYYY-MM-DD
  gratitude: string[];
  prayerRequest: string;
  reflection: string;
  createdAt: string;
  updatedAt: string;
}

// Streak types
export interface StreakData {
  currentStreak: number;
  longestStreak: number;
  lastCompletedDate: string | null;
  totalCompletions: number;
}

// Daily verse types
export interface DailyVerse {
  reference: string;
  text: string;
  translation: string;
  date: string;
}

// User types
export interface UserSettings {
  reminderTime: string; // HH:mm
  reminderEnabled: boolean;
  focusArea: FocusArea | null;
  isPremium: boolean;
  onboardingCompleted: boolean;
}

export type FocusArea =
  | 'building_habit'
  | 'deepening_prayer'
  | 'finding_peace'
  | 'growing_community';

// Store state types
export interface HabitState {
  habits: Habit[];
  completions: HabitCompletion[];
  todayHabits: Habit[];
  addHabit: (habit: Omit<Habit, 'id' | 'createdAt'>) => void;
  removeHabit: (id: string) => void;
  toggleHabitCompletion: (habitId: string, date: string) => void;
  isHabitCompleted: (habitId: string, date: string) => boolean;
  getCompletionsForDate: (date: string) => HabitCompletion[];
  loadFromStorage: () => Promise<void>;
}

export interface JournalState {
  entries: JournalEntry[];
  addEntry: (entry: Omit<JournalEntry, 'id' | 'createdAt' | 'updatedAt'>) => void;
  updateEntry: (id: string, entry: Partial<JournalEntry>) => void;
  getEntryForDate: (date: string) => JournalEntry | undefined;
  loadFromStorage: () => Promise<void>;
}

export interface StreakState extends StreakData {
  updateStreak: (completions: HabitCompletion[]) => void;
  loadFromStorage: () => Promise<void>;
}

export interface SettingsState extends UserSettings {
  updateSettings: (settings: Partial<UserSettings>) => void;
  setOnboardingComplete: (completed: boolean) => void;
  loadFromStorage: () => Promise<void>;
}

export interface VerseState {
  verse: DailyVerse | null;
  isLoading: boolean;
  error: string | null;
  fetchVerse: () => Promise<void>;
}

// Navigation types
export type RootStackParamList = {
  Main: undefined;
  Onboarding: undefined;
  Paywall: undefined;
};

export type MainTabParamList = {
  Today: undefined;
  Journal: undefined;
  Progress: undefined;
  Settings: undefined;
};

// Paywall types
export interface PaywallProduct {
  identifier: string;
  title: string;
  description: string;
  price: string;
  priceValue: number;
  currencyCode: string;
}
