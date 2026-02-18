/**
 * Attribution Configuration
 * Central configuration for attribution SDKs across all apps
 */

import type {
  AppId,
  AttributionConfig,
  AdjustConfig,
  AppsFlyerConfig,
  BranchConfig,
  AttributionNetwork,
} from '../types';

/**
 * Environment detection
 */
const isDev = __DEV__ || process.env.NODE_ENV === 'development';

/**
 * Adjust configuration per app
 */
const ADJUST_CONFIGS: Record<AppId, AdjustConfig> = {
  prayerlock: {
    appToken: process.env.ADJUST_PRAYERLOCK_TOKEN || 'YOUR_ADJUST_TOKEN',
    environment: isDev ? 'sandbox' : 'production',
    eventTokens: {
      install: process.env.ADJUST_EVENT_INSTALL || 'abc123',
      purchase: process.env.ADJUST_EVENT_PURCHASE || 'def456',
      subscribe: process.env.ADJUST_EVENT_SUBSCRIBE || 'ghi789',
      share: process.env.ADJUST_EVENT_SHARE || 'jkl012',
      referral: process.env.ADJUST_EVENT_REFERRAL || 'mno345',
      trial_start: process.env.ADJUST_EVENT_TRIAL || 'pqr678',
      signup: process.env.ADJUST_EVENT_SIGNUP || 'stu901',
    },
    deferredDeepLinkEnabled: true,
    urlStrategy: 'default',
  },
  walktounlock: {
    appToken: process.env.ADJUST_WALKTOUNLOCK_TOKEN || 'YOUR_ADJUST_TOKEN',
    environment: isDev ? 'sandbox' : 'production',
    eventTokens: {
      install: 'evt_install',
      purchase: 'evt_purchase',
      subscribe: 'evt_subscribe',
      share: 'evt_share',
      referral: 'evt_referral',
      challenge_complete: 'evt_challenge',
      steps_milestone: 'evt_steps',
    },
    deferredDeepLinkEnabled: true,
    urlStrategy: 'default',
  },
  faithstreak: {
    appToken: process.env.ADJUST_FAITHSTREAK_TOKEN || 'YOUR_ADJUST_TOKEN',
    environment: isDev ? 'sandbox' : 'production',
    eventTokens: {
      install: 'evt_install',
      purchase: 'evt_purchase',
      subscribe: 'evt_subscribe',
      share: 'evt_share',
      referral: 'evt_referral',
      streak_milestone: 'evt_streak',
      reading_complete: 'evt_reading',
    },
    deferredDeepLinkEnabled: true,
    urlStrategy: 'default',
  },
  stepbet: {
    appToken: process.env.ADJUST_STEPBET_TOKEN || 'YOUR_ADJUST_TOKEN',
    environment: isDev ? 'sandbox' : 'production',
    eventTokens: {
      install: 'evt_install',
      purchase: 'evt_purchase',
      subscribe: 'evt_subscribe',
      share: 'evt_share',
      referral: 'evt_referral',
      bet_placed: 'evt_bet',
      bet_won: 'evt_won',
    },
    deferredDeepLinkEnabled: true,
    urlStrategy: 'default',
  },
};

/**
 * AppsFlyer configuration per app
 */
const APPSFLYER_CONFIGS: Record<AppId, AppsFlyerConfig> = {
  prayerlock: {
    devKey: process.env.APPSFLYER_DEV_KEY || 'YOUR_DEV_KEY',
    appId: process.env.APPSFLYER_PRAYERLOCK_APP_ID || 'com.yourcompany.prayerlock',
    isDebug: isDev,
    oneLinkId: process.env.APPSFLYER_ONELINK_ID || 'YOUR_ONELINK_ID',
    timeToWaitForATTUserAuthorization: 60,
  },
  walktounlock: {
    devKey: process.env.APPSFLYER_DEV_KEY || 'YOUR_DEV_KEY',
    appId: process.env.APPSFLYER_WALKTOUNLOCK_APP_ID || 'com.yourcompany.walktounlock',
    isDebug: isDev,
    oneLinkId: process.env.APPSFLYER_ONELINK_ID || 'YOUR_ONELINK_ID',
    timeToWaitForATTUserAuthorization: 60,
  },
  faithstreak: {
    devKey: process.env.APPSFLYER_DEV_KEY || 'YOUR_DEV_KEY',
    appId: process.env.APPSFLYER_FAITHSTREAK_APP_ID || 'com.yourcompany.faithstreak',
    isDebug: isDev,
    oneLinkId: process.env.APPSFLYER_ONELINK_ID || 'YOUR_ONELINK_ID',
    timeToWaitForATTUserAuthorization: 60,
  },
  stepbet: {
    devKey: process.env.APPSFLYER_DEV_KEY || 'YOUR_DEV_KEY',
    appId: process.env.APPSFLYER_STEPBET_APP_ID || 'com.yourcompany.stepbet',
    isDebug: isDev,
    oneLinkId: process.env.APPSFLYER_ONELINK_ID || 'YOUR_ONELINK_ID',
    timeToWaitForATTUserAuthorization: 60,
  },
};

/**
 * Branch configuration per app
 */
const BRANCH_CONFIGS: Record<AppId, BranchConfig> = {
  prayerlock: {
    key: process.env.BRANCH_PRAYERLOCK_KEY || 'YOUR_BRANCH_KEY',
    useTestKey: isDev,
    enableLogging: isDev,
    linkDomain: 'prayerlock.app.link',
  },
  walktounlock: {
    key: process.env.BRANCH_WALKTOUNLOCK_KEY || 'YOUR_BRANCH_KEY',
    useTestKey: isDev,
    enableLogging: isDev,
    linkDomain: 'walktounlock.app.link',
  },
  faithstreak: {
    key: process.env.BRANCH_FAITHSTREAK_KEY || 'YOUR_BRANCH_KEY',
    useTestKey: isDev,
    enableLogging: isDev,
    linkDomain: 'faithstreak.app.link',
  },
  stepbet: {
    key: process.env.BRANCH_STEPBET_KEY || 'YOUR_BRANCH_KEY',
    useTestKey: isDev,
    enableLogging: isDev,
    linkDomain: 'stepbet.app.link',
  },
};

/**
 * Primary attribution network per app
 * Change this to switch which SDK is primary
 */
const PRIMARY_NETWORKS: Record<AppId, AttributionNetwork> = {
  prayerlock: 'adjust',
  walktounlock: 'adjust',
  faithstreak: 'branch',
  stepbet: 'appsflyer',
};

/**
 * Get attribution configuration for an app
 */
export function getAttributionConfig(appId: AppId): AttributionConfig {
  return {
    appId,
    primaryNetwork: PRIMARY_NETWORKS[appId],
    adjust: ADJUST_CONFIGS[appId],
    appsflyer: APPSFLYER_CONFIGS[appId],
    branch: BRANCH_CONFIGS[appId],
    debug: isDev,
  };
}

/**
 * Get specific SDK config
 */
export function getAdjustConfig(appId: AppId): AdjustConfig {
  return ADJUST_CONFIGS[appId];
}

export function getAppsFlyerConfig(appId: AppId): AppsFlyerConfig {
  return APPSFLYER_CONFIGS[appId];
}

export function getBranchConfig(appId: AppId): BranchConfig {
  return BRANCH_CONFIGS[appId];
}

/**
 * Event token mapping for common events
 */
export const COMMON_EVENTS = {
  INSTALL: 'install',
  FIRST_OPEN: 'first_open',
  REGISTRATION: 'signup',
  LOGIN: 'login',
  PURCHASE: 'purchase',
  SUBSCRIBE: 'subscribe',
  TRIAL_START: 'trial_start',
  SHARE: 'share',
  REFERRAL_SENT: 'referral',
  REFERRAL_CONVERTED: 'referral_converted',
  CONTENT_VIEW: 'content_view',
  LEVEL_UP: 'level_up',
  ACHIEVEMENT: 'achievement',
} as const;

export type CommonEventType = (typeof COMMON_EVENTS)[keyof typeof COMMON_EVENTS];

/**
 * UTM parameter keys
 */
export const UTM_PARAMS = {
  SOURCE: 'utm_source',
  MEDIUM: 'utm_medium',
  CAMPAIGN: 'utm_campaign',
  CONTENT: 'utm_content',
  TERM: 'utm_term',
} as const;

/**
 * Click ID parameter keys by platform
 */
export const CLICK_ID_PARAMS = {
  GOOGLE: 'gclid',
  FACEBOOK: 'fbclid',
  TIKTOK: 'ttclid',
  SNAPCHAT: 'sclid',
  TWITTER: 'twclid',
  PINTEREST: 'epik',
} as const;

/**
 * Check if a click ID is from a specific platform
 */
export function detectClickPlatform(
  params: Record<string, string>
): string | null {
  if (params.gclid) return 'google';
  if (params.fbclid) return 'facebook';
  if (params.ttclid) return 'tiktok';
  if (params.sclid) return 'snapchat';
  if (params.twclid) return 'twitter';
  if (params.epik) return 'pinterest';
  return null;
}

export default getAttributionConfig;
