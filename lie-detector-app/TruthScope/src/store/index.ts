import AsyncStorage from '@react-native-async-storage/async-storage';
import { DetectionResult, SessionData, UserProfile } from '../utils/types';

const KEYS = {
  PROFILE: 'truthscope_profile',
  SESSIONS: 'truthscope_sessions',
  BASELINE: 'truthscope_baseline',
} as const;

const defaultProfile: UserProfile = {
  hasCompletedOnboarding: false,
  isPremium: false,
  sessionsCompleted: 0,
};

export async function getProfile(): Promise<UserProfile> {
  try {
    const raw = await AsyncStorage.getItem(KEYS.PROFILE);
    return raw ? { ...defaultProfile, ...JSON.parse(raw) } : defaultProfile;
  } catch {
    return defaultProfile;
  }
}

export async function saveProfile(profile: Partial<UserProfile>): Promise<void> {
  const current = await getProfile();
  await AsyncStorage.setItem(KEYS.PROFILE, JSON.stringify({ ...current, ...profile }));
}

export async function getSessions(): Promise<SessionData[]> {
  try {
    const raw = await AsyncStorage.getItem(KEYS.SESSIONS);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export async function saveSession(session: SessionData): Promise<void> {
  const sessions = await getSessions();
  sessions.unshift(session);
  if (sessions.length > 100) sessions.length = 100;
  await AsyncStorage.setItem(KEYS.SESSIONS, JSON.stringify(sessions));
  await saveProfile({ sessionsCompleted: sessions.length });
}

export async function saveBaseline(data: {
  heartRate: number;
  hrv: number;
  voiceF0: number;
}): Promise<void> {
  await AsyncStorage.setItem(KEYS.BASELINE, JSON.stringify(data));
  await saveProfile({
    baselineHR: data.heartRate,
    baselineHRV: data.hrv,
    baselineVoiceF0: data.voiceF0,
  });
}

export async function getBaseline(): Promise<{
  heartRate: number;
  hrv: number;
  voiceF0: number;
} | null> {
  try {
    const raw = await AsyncStorage.getItem(KEYS.BASELINE);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).substring(2, 8);
}

// Premium status check
export async function getIsPremium(): Promise<boolean> {
  const profile = await getProfile();
  return profile.isPremium;
}

// Daily session limit enforcement
const DAILY_FREE_LIMIT = 3;

export async function canStartSession(): Promise<{ allowed: boolean; remaining: number }> {
  const profile = await getProfile();
  if (profile.isPremium) return { allowed: true, remaining: 999 };
  
  const sessions = await getSessions();
  const today = new Date().toDateString();
  const todaySessions = sessions.filter(
    s => new Date(s.startTime).toDateString() === today
  );
  
  const remaining = Math.max(0, DAILY_FREE_LIMIT - todaySessions.length);
  return { allowed: remaining > 0, remaining };
}

export async function setPremium(isPremium: boolean): Promise<void> {
  await saveProfile({ isPremium });
}
