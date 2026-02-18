/**
 * PrayerLock - App-specific configuration
 *
 * Screen time blocker requiring prayer completion to unlock.
 * Primary monetization: Subscription ($9.99/month, $49.99/year)
 */

import { createAppConfig, AppConfigType } from '../AppConfig';

// Color scheme
export const PRAYERLOCK_COLORS = {
  primary: '#6366F1', // Indigo
  secondary: '#8B5CF6', // Purple
  accent: '#F59E0B', // Amber (prayer icon)
  background: '#0F172A', // Dark slate
  surface: '#1E293B',
  text: '#F8FAFC',
  textSecondary: '#94A3B8',
  success: '#22C55E',
  error: '#EF4444',
  warning: '#F59E0B',
} as const;

// Feature flags specific to PrayerLock
export const PRAYERLOCK_FEATURES = {
  // Core features
  screenTimeBlocking: true,
  prayerTracking: true,
  dailyReminders: true,

  // Premium features
  customPrayers: false, // Premium only
  unlimitedBlockedApps: false, // Premium only
  familySharing: false, // Premium only
  prayerStreaks: true, // Free with limits

  // Paywall settings
  showPaywallOnLaunch: true,
  paywallTriggerAppBlocks: 3, // Show paywall after 3 app blocks

  // Onboarding
  requireOnboarding: true,
  onboardingSteps: 4,
} as const;

// RevenueCat product IDs
export const PRAYERLOCK_PRODUCTS = {
  monthly: 'prayerlock_monthly_999',
  annual: 'prayerlock_annual_4999',
  entitlement: 'premium',
} as const;

// App Store configuration
export const PRAYERLOCK_STORE = {
  appStoreId: 'PLACEHOLDER_APP_STORE_ID', // Set after App Store submission
  appStoreUrl: 'https://apps.apple.com/app/prayerlock/idPLACEHOLDER',
  supportEmail: 'support@printmaxx.com',
  privacyPolicyUrl: 'https://printmaxx.com/privacy',
  termsOfServiceUrl: 'https://printmaxx.com/terms',
} as const;

/**
 * Full PrayerLock configuration
 */
export const PRAYERLOCK_CONFIG: AppConfigType = createAppConfig({
  identity: {
    appName: 'PrayerLock',
    bundleId: 'com.printmaxx.prayerlock',
    appStoreId: PRAYERLOCK_STORE.appStoreId,
  },

  revenueCat: {
    iosApiKey: process.env.REVENUECAT_IOS_KEY_PRAYERLOCK || '',
    androidApiKey: process.env.REVENUECAT_ANDROID_KEY_PRAYERLOCK,
    entitlementId: PRAYERLOCK_PRODUCTS.entitlement,
  },

  features: {
    showPaywallOnLaunch: PRAYERLOCK_FEATURES.showPaywallOnLaunch,
    enablePushNotifications: true,
    enableAnalytics: true,
    enableCrashReporting: true,
    debugMode: false,
  },
});

/**
 * PrayerLock-specific utilities
 */
export const PrayerLockUtils = {
  /**
   * Get the appropriate RevenueCat product ID
   */
  getProductId(type: 'monthly' | 'annual'): string {
    return PRAYERLOCK_PRODUCTS[type];
  },

  /**
   * Check if a feature requires premium
   */
  isPremiumFeature(feature: keyof typeof PRAYERLOCK_FEATURES): boolean {
    const premiumFeatures = ['customPrayers', 'unlimitedBlockedApps', 'familySharing'];
    return premiumFeatures.includes(feature);
  },

  /**
   * Get color by name
   */
  getColor(name: keyof typeof PRAYERLOCK_COLORS): string {
    return PRAYERLOCK_COLORS[name];
  },
};

export default PRAYERLOCK_CONFIG;
