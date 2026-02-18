// App Constants
export const APP_NAME = 'StepUnlock';
export const APP_VERSION = '1.0.0';

// Step Goal Limits
export const MIN_STEP_GOAL = 1000;
export const MAX_STEP_GOAL = 20000;
export const DEFAULT_STEP_GOAL = 5000;
export const STEP_GOAL_INCREMENT = 500;

// Trial
export const TRIAL_DAYS = 3;

// Subscription
export const MONTHLY_PRICE = '$7.99';
export const ANNUAL_PRICE = '$39.99';
export const REVENUECAT_API_KEY_IOS = 'YOUR_IOS_API_KEY';
export const REVENUECAT_API_KEY_ANDROID = 'YOUR_ANDROID_API_KEY';
export const ENTITLEMENT_ID = 'premium';

// Background Refresh
export const BACKGROUND_REFRESH_INTERVAL_MS = 5 * 60 * 1000; // 5 minutes

// Storage Keys
export const STORAGE_KEYS = {
  USER_SETTINGS: '@walktounlock/user_settings',
  STEP_DATA: '@walktounlock/step_data',
  STREAK_DATA: '@walktounlock/streak_data',
  APP_STATE: '@walktounlock/app_state',
  SUBSCRIPTION_STATE: '@walktounlock/subscription_state',
} as const;

// Colors
export const COLORS = {
  primary: '#4CAF50',
  primaryDark: '#388E3C',
  secondary: '#2196F3',
  background: '#F5F5F5',
  surface: '#FFFFFF',
  text: '#212121',
  textSecondary: '#757575',
  error: '#F44336',
  warning: '#FF9800',
  success: '#4CAF50',
  border: '#E0E0E0',
  disabled: '#BDBDBD',
  locked: '#F44336',
  unlocked: '#4CAF50',
} as const;

// Typography
export const FONTS = {
  regular: 'System',
  medium: 'System',
  bold: 'System',
} as const;

// Default Apps to Block (suggested)
export const DEFAULT_BLOCKED_APPS = [
  { id: '1', name: 'TikTok', bundleId: 'com.zhiliaoapp.musically' },
  { id: '2', name: 'Instagram', bundleId: 'com.instagram.android' },
  { id: '3', name: 'Twitter', bundleId: 'com.twitter.android' },
  { id: '4', name: 'YouTube', bundleId: 'com.google.android.youtube' },
  { id: '5', name: 'Facebook', bundleId: 'com.facebook.katana' },
  { id: '6', name: 'Reddit', bundleId: 'com.reddit.frontpage' },
];

// Essential Apps (never block)
export const ESSENTIAL_APPS = [
  'com.apple.mobilephone',
  'com.apple.MobileSMS',
  'com.apple.Maps',
  'com.google.android.dialer',
  'com.google.android.apps.messaging',
  'com.google.android.apps.maps',
];
