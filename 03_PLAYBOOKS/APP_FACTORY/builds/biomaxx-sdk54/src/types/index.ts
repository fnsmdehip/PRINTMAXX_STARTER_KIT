export type ProtocolCategory =
  | 'fasting'
  | 'cold'
  | 'heat'
  | 'light'
  | 'supplements'
  | 'movement'
  | 'sleep';

export type ProtocolUnit = 'minutes' | 'hours' | 'count' | 'boolean';

export interface Protocol {
  id: string;
  name: string;
  category: ProtocolCategory;
  icon: string;
  unit: ProtocolUnit;
  dailyGoal: number;
  description: string;
  isPremium: boolean;
}

export interface ProtocolLog {
  protocolId: string;
  date: string;
  value: number;
  timestamp: number;
  notes?: string;
}

export interface ActiveSession {
  protocolId: string;
  startTime: number;
  isPaused: boolean;
  pausedTime?: number;
}

export interface UserGoal {
  id: string;
  label: string;
}

export interface User {
  name: string;
  goals: string[];
  onboardingComplete: boolean;
  createdAt: string;
  streakDays: number;
  totalSessions: number;
  achievements: string[];
}

export interface Subscription {
  status: 'free' | 'trial' | 'premium';
  trialStartDate?: string;
  expiresAt?: string;
}

export interface LearnArticle {
  id: string;
  title: string;
  category: string;
  readTime: number;
  isPremium: boolean;
  featured: boolean;
  excerpt: string;
  content?: string;
  affiliateLink?: string;
}

export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  unlockedAt?: string;
}

export interface DailyLog {
  date: string;
  protocols: Record<string, number>;
  longevityScore: number;
}
