/**
 * PrayerLock Constants
 * All app-wide configuration values
 */

// Timing defaults
export const DEFAULT_DEVOTION_MINUTES = 10;
export const MIN_DEVOTION_MINUTES = 5;
export const MAX_DEVOTION_MINUTES = 60;
export const DEFAULT_RESET_TIME = '05:00';
export const SCRIPTURE_MIN_READ_SECONDS = 60;

// Trial settings
export const TRIAL_DAYS = 3;

// Pricing (display only, actual handled by RevenueCat)
export const MONTHLY_PRICE = '$9.99';
export const ANNUAL_PRICE = '$49.99';
export const ANNUAL_MONTHLY_EQUIVALENT = '$4.17';

// RevenueCat identifiers (configure in RevenueCat dashboard)
export const REVENUECAT_IOS_KEY = 'YOUR_IOS_REVENUECAT_KEY';
export const REVENUECAT_ANDROID_KEY = 'YOUR_ANDROID_REVENUECAT_KEY';
export const ENTITLEMENT_ID = 'pro';
export const MONTHLY_PRODUCT_ID = 'prayerlock_monthly';
export const ANNUAL_PRODUCT_ID = 'prayerlock_annual';

// Storage keys for AsyncStorage
export const STORAGE_KEYS = {
  USER_SETTINGS: '@prayerlock/user_settings',
  STREAK_DATA: '@prayerlock/streak_data',
  SESSIONS: '@prayerlock/sessions',
  SUBSCRIPTION: '@prayerlock/subscription',
  TRIAL_START: '@prayerlock/trial_start',
  CACHED_PASSAGES: '@prayerlock/cached_passages',
} as const;

// Bible API
export const BIBLE_API_BASE = 'https://bible-api.com';

// Default blocked app categories
export const DEFAULT_BLOCKED_CATEGORIES = ['social', 'game', 'entertainment'] as const;

// Common social media bundle IDs
export const COMMON_SOCIAL_APPS = [
  { packageName: 'com.facebook.katana', appName: 'Facebook', category: 'social' as const },
  { packageName: 'com.instagram.android', appName: 'Instagram', category: 'social' as const },
  { packageName: 'com.twitter.android', appName: 'X (Twitter)', category: 'social' as const },
  { packageName: 'com.zhiliaoapp.musically', appName: 'TikTok', category: 'social' as const },
  { packageName: 'com.snapchat.android', appName: 'Snapchat', category: 'social' as const },
  { packageName: 'com.reddit.frontpage', appName: 'Reddit', category: 'social' as const },
  { packageName: 'com.linkedin.android', appName: 'LinkedIn', category: 'social' as const },
  { packageName: 'com.google.android.youtube', appName: 'YouTube', category: 'entertainment' as const },
  { packageName: 'com.netflix.mediaclient', appName: 'Netflix', category: 'entertainment' as const },
];

// iOS bundle IDs
export const COMMON_IOS_APPS = [
  { packageName: 'com.facebook.Facebook', appName: 'Facebook', category: 'social' as const },
  { packageName: 'com.burbn.instagram', appName: 'Instagram', category: 'social' as const },
  { packageName: 'com.atebits.Tweetie2', appName: 'X (Twitter)', category: 'social' as const },
  { packageName: 'com.zhiliaoapp.musically', appName: 'TikTok', category: 'social' as const },
  { packageName: 'com.toyopagroup.picaboo', appName: 'Snapchat', category: 'social' as const },
  { packageName: 'com.reddit.Reddit', appName: 'Reddit', category: 'social' as const },
  { packageName: 'com.google.ios.youtube', appName: 'YouTube', category: 'entertainment' as const },
  { packageName: 'com.netflix.Netflix', appName: 'Netflix', category: 'entertainment' as const },
];

// Emergency unlock phrase
export const EMERGENCY_UNLOCK_PHRASE = 'I am breaking my commitment';

// Colors
export const COLORS = {
  primary: '#4A90A4',
  primaryDark: '#2E5A6B',
  secondary: '#F5A623',
  background: '#FAFAFA',
  surface: '#FFFFFF',
  text: '#1A1A1A',
  textSecondary: '#6B6B6B',
  success: '#4CAF50',
  warning: '#FF9800',
  error: '#F44336',
  streak: '#FFD700',
  disabled: '#CCCCCC',
} as const;
