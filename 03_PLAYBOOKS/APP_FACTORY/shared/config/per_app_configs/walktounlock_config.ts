/**
 * WalkToUnlock - App-specific configuration
 *
 * Screen time blocker requiring step count to unlock.
 * Primary monetization: Subscription ($7.99/month, $39.99/year)
 */

import { createAppConfig, AppConfigType } from '../AppConfig';

// Color scheme
export const WALKTOUNLOCK_COLORS = {
  primary: '#10B981', // Emerald
  secondary: '#059669', // Darker emerald
  accent: '#F97316', // Orange (energy)
  background: '#FFFFFF',
  surface: '#F3F4F6',
  text: '#111827',
  textSecondary: '#6B7280',
  success: '#22C55E',
  error: '#EF4444',
  warning: '#F59E0B',
} as const;

// Feature flags specific to WalkToUnlock
export const WALKTOUNLOCK_FEATURES = {
  // Core features
  screenTimeBlocking: true,
  stepTracking: true,
  healthKitIntegration: true,

  // Premium features
  customStepGoals: false, // Premium only
  unlimitedBlockedApps: false, // Premium only
  stepHistory: false, // Premium only
  challenges: false, // Premium only

  // Paywall settings
  showPaywallOnLaunch: true,
  paywallTriggerAppBlocks: 2, // Show paywall quickly

  // Onboarding
  requireOnboarding: true,
  onboardingSteps: 3,
  requireHealthKitPermission: true,
} as const;

// RevenueCat product IDs
export const WALKTOUNLOCK_PRODUCTS = {
  monthly: 'walktounlock_monthly_799',
  annual: 'walktounlock_annual_3999',
  entitlement: 'premium',
} as const;

// App Store configuration
export const WALKTOUNLOCK_STORE = {
  appStoreId: 'PLACEHOLDER_APP_STORE_ID',
  appStoreUrl: 'https://apps.apple.com/app/walktounlock/idPLACEHOLDER',
  supportEmail: 'support@printmaxx.com',
  privacyPolicyUrl: 'https://printmaxx.com/privacy',
  termsOfServiceUrl: 'https://printmaxx.com/terms',
} as const;

// Default step requirements
export const WALKTOUNLOCK_DEFAULTS = {
  defaultStepsRequired: 1000,
  minStepsRequired: 100,
  maxStepsRequired: 10000,
  freeBlockedAppsLimit: 3,
  premiumBlockedAppsLimit: -1, // Unlimited
} as const;

/**
 * Full WalkToUnlock configuration
 */
export const WALKTOUNLOCK_CONFIG: AppConfigType = createAppConfig({
  identity: {
    appName: 'WalkToUnlock',
    bundleId: 'com.printmaxx.walktounlock',
    appStoreId: WALKTOUNLOCK_STORE.appStoreId,
  },

  revenueCat: {
    iosApiKey: process.env.REVENUECAT_IOS_KEY_WALKTOUNLOCK || '',
    androidApiKey: process.env.REVENUECAT_ANDROID_KEY_WALKTOUNLOCK,
    entitlementId: WALKTOUNLOCK_PRODUCTS.entitlement,
  },

  features: {
    showPaywallOnLaunch: WALKTOUNLOCK_FEATURES.showPaywallOnLaunch,
    enablePushNotifications: true,
    enableAnalytics: true,
    enableCrashReporting: true,
    debugMode: false,
  },
});

/**
 * WalkToUnlock-specific utilities
 */
export const WalkToUnlockUtils = {
  getProductId(type: 'monthly' | 'annual'): string {
    return WALKTOUNLOCK_PRODUCTS[type];
  },

  isPremiumFeature(feature: keyof typeof WALKTOUNLOCK_FEATURES): boolean {
    const premiumFeatures = ['customStepGoals', 'unlimitedBlockedApps', 'stepHistory', 'challenges'];
    return premiumFeatures.includes(feature);
  },

  getColor(name: keyof typeof WALKTOUNLOCK_COLORS): string {
    return WALKTOUNLOCK_COLORS[name];
  },

  getDefaultSteps(): number {
    return WALKTOUNLOCK_DEFAULTS.defaultStepsRequired;
  },
};

export default WALKTOUNLOCK_CONFIG;
