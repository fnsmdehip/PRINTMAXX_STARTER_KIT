/**
 * StudyLock - App-specific configuration
 *
 * Screen time blocker for students with focus sessions.
 * Primary monetization: Subscription ($6.99/month, $34.99/year)
 */

import { createAppConfig, AppConfigType } from '../AppConfig';

// Color scheme
export const STUDYLOCK_COLORS = {
  primary: '#3B82F6', // Blue
  secondary: '#1D4ED8', // Darker blue
  accent: '#FBBF24', // Yellow (highlighter)
  background: '#FEFCE8', // Warm white
  surface: '#FFFFFF',
  text: '#1F2937',
  textSecondary: '#6B7280',
  success: '#22C55E',
  error: '#EF4444',
  warning: '#F59E0B',
} as const;

// Feature flags specific to StudyLock
export const STUDYLOCK_FEATURES = {
  // Core features
  screenTimeBlocking: true,
  pomodoroTimer: true,
  focusSessions: true,
  breakReminders: true,

  // Premium features
  customSessionLengths: false, // Premium only
  unlimitedBlockedApps: false, // Premium only
  studyStats: false, // Premium only
  subjectTracking: false, // Premium only

  // Paywall settings
  showPaywallOnLaunch: false, // Let them experience first
  paywallTriggerSessions: 5, // Show after 5 study sessions

  // Onboarding
  requireOnboarding: true,
  onboardingSteps: 4,
} as const;

// RevenueCat product IDs
export const STUDYLOCK_PRODUCTS = {
  monthly: 'studylock_monthly_699',
  annual: 'studylock_annual_3499',
  entitlement: 'premium',
} as const;

// App Store configuration
export const STUDYLOCK_STORE = {
  appStoreId: 'PLACEHOLDER_APP_STORE_ID',
  appStoreUrl: 'https://apps.apple.com/app/studylock/idPLACEHOLDER',
  supportEmail: 'support@printmaxx.com',
  privacyPolicyUrl: 'https://printmaxx.com/privacy',
  termsOfServiceUrl: 'https://printmaxx.com/terms',
} as const;

// Default session settings
export const STUDYLOCK_DEFAULTS = {
  defaultSessionMinutes: 25, // Pomodoro
  defaultBreakMinutes: 5,
  defaultLongBreakMinutes: 15,
  sessionsBeforeLongBreak: 4,
  freeBlockedAppsLimit: 3,
  freeSessionsPerDay: 5,
} as const;

/**
 * Full StudyLock configuration
 */
export const STUDYLOCK_CONFIG: AppConfigType = createAppConfig({
  identity: {
    appName: 'StudyLock',
    bundleId: 'com.printmaxx.studylock',
    appStoreId: STUDYLOCK_STORE.appStoreId,
  },

  revenueCat: {
    iosApiKey: process.env.REVENUECAT_IOS_KEY_STUDYLOCK || '',
    androidApiKey: process.env.REVENUECAT_ANDROID_KEY_STUDYLOCK,
    entitlementId: STUDYLOCK_PRODUCTS.entitlement,
  },

  features: {
    showPaywallOnLaunch: STUDYLOCK_FEATURES.showPaywallOnLaunch,
    enablePushNotifications: true,
    enableAnalytics: true,
    enableCrashReporting: true,
    debugMode: false,
  },
});

/**
 * StudyLock-specific utilities
 */
export const StudyLockUtils = {
  getProductId(type: 'monthly' | 'annual'): string {
    return STUDYLOCK_PRODUCTS[type];
  },

  isPremiumFeature(feature: keyof typeof STUDYLOCK_FEATURES): boolean {
    const premiumFeatures = ['customSessionLengths', 'unlimitedBlockedApps', 'studyStats', 'subjectTracking'];
    return premiumFeatures.includes(feature);
  },

  getColor(name: keyof typeof STUDYLOCK_COLORS): string {
    return STUDYLOCK_COLORS[name];
  },

  getDefaultSessionLength(): number {
    return STUDYLOCK_DEFAULTS.defaultSessionMinutes;
  },
};

export default STUDYLOCK_CONFIG;
