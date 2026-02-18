export { Colors } from './colors';

export type FaithType = 'christianity' | 'islam' | 'general';

export const PRAYER_DURATIONS = [
  { label: '5 min', value: 5 },
  { label: '10 min', value: 10 },
  { label: '15 min', value: 15 },
  { label: '30 min', value: 30 },
];

export interface SalahSettings {
  calculationMethod: 'MWL' | 'ISNA' | 'Egypt' | 'Makkah' | 'Karachi';
  madhab: 'Shafi' | 'Hanafi';
  fajrEnabled: boolean;
  dhuhrEnabled: boolean;
  asrEnabled: boolean;
  maghribEnabled: boolean;
  ishaEnabled: boolean;
  lockWindowMinutes: number;
  city: string;
  country: string;
  streakThreshold: 'strict' | 'moderate' | 'lenient';
}

export const DEFAULT_SALAH_SETTINGS: SalahSettings = {
  calculationMethod: 'ISNA',
  madhab: 'Shafi',
  fajrEnabled: true,
  dhuhrEnabled: true,
  asrEnabled: true,
  maghribEnabled: true,
  ishaEnabled: true,
  lockWindowMinutes: 30,
  city: 'New York',
  country: 'US',
  streakThreshold: 'moderate',
};

export const DEFAULT_SETTINGS = {
  lockTime: '06:00',
  prayerDuration: 5,
  notificationsEnabled: true,
  hapticEnabled: true,
  faith: 'christianity' as FaithType,
  salahSettings: DEFAULT_SALAH_SETTINGS,
};

export const STORAGE_KEYS = {
  STREAK: '@prayerlock_streak',
  LAST_PRAYER_DATE: '@prayerlock_last_prayer',
  TOTAL_PRAYER_TIME: '@prayerlock_total_time',
  SETTINGS: '@prayerlock_settings',
  EMERGENCY_UNLOCK_COUNT: '@prayerlock_emergency_count',
  IS_LOCKED: '@prayerlock_is_locked',
  LOCK_START_TIME: '@prayerlock_lock_start',
  IS_PREMIUM: '@prayerlock_is_premium',
  FAITH: '@prayerlock_faith',
  SALAH_DAILY: '@prayerlock_salah_daily',
  SALAH_TOTAL_COMPLETED: '@prayerlock_salah_total',
  SALAH_TOTAL_MISSED: '@prayerlock_salah_missed',
  ONBOARDING_COMPLETE: '@prayerlock_onboarding_done',
};

export const FAITH_STRINGS = {
  christianity: {
    lockMessage: 'Pray First, Phone Second',
    timerLabel: 'Prayer Time',
    streakLabel: 'Prayer Streak',
    completionMessage: 'Prayer complete. God bless your day.',
    emergencyLabel: 'Skip Prayer',
    greeting: 'Good Morning',
  },
  islam: {
    lockMessage: 'Salah Time. Phone Locked.',
    timerLabel: 'Salah Time',
    streakLabel: 'Salah Streak',
    completionMessage: 'May Allah accept your prayer.',
    emergencyLabel: 'Skip Salah (marks as missed)',
    greeting: 'Assalamu Alaikum',
  },
  general: {
    lockMessage: 'Reflection First, Phone Second',
    timerLabel: 'Meditation Time',
    streakLabel: 'Mindfulness Streak',
    completionMessage: 'Well done. Start your day with intention.',
    emergencyLabel: 'Skip Session',
    greeting: 'Good Morning',
  },
};
