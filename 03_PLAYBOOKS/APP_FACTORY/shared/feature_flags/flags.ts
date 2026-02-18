/**
 * Feature Flag Definitions
 *
 * Centralized flag taxonomy with type-safe access.
 * All flags are typed for compile-time safety.
 */

// Boolean flags
export const BOOLEAN_FLAGS = {
  SHOW_NEW_PAYWALL: 'show_new_paywall',
  ENABLE_STREAK_SHARING: 'enable_streak_sharing',
  SHOW_ANNUAL_OPTION: 'show_annual_option',
  ENABLE_DARK_MODE: 'enable_dark_mode',
  SHOW_ONBOARDING_V2: 'show_onboarding_v2',
  ENABLE_PUSH_NOTIFICATIONS: 'enable_push_notifications',
  SHOW_REFERRAL_PROGRAM: 'show_referral_program',
  ENABLE_OFFLINE_MODE: 'enable_offline_mode',
  SHOW_RATING_PROMPT: 'show_rating_prompt',
  ENABLE_HAPTIC_FEEDBACK: 'enable_haptic_feedback',
  SHOW_PREMIUM_FEATURES: 'show_premium_features',
  ENABLE_ANALYTICS_DEBUG: 'enable_analytics_debug',
  SHOW_BETA_FEATURES: 'show_beta_features',
  ENABLE_CRASH_REPORTING: 'enable_crash_reporting',
  MAINTENANCE_MODE: 'maintenance_mode',
} as const;

// Numeric flags
export const NUMERIC_FLAGS = {
  TRIAL_LENGTH_DAYS: 'trial_length_days',
  MAX_FREE_USES: 'max_free_uses',
  PAYWALL_DELAY_SECONDS: 'paywall_delay_seconds',
  SESSION_TIMEOUT_MINUTES: 'session_timeout_minutes',
  MIN_VERSION_REQUIRED: 'min_version_required',
  RATING_PROMPT_THRESHOLD: 'rating_prompt_threshold',
  CACHE_TTL_MINUTES: 'cache_ttl_minutes',
  API_TIMEOUT_SECONDS: 'api_timeout_seconds',
  MAX_RETRY_ATTEMPTS: 'max_retry_attempts',
  NOTIFICATION_COOLDOWN_HOURS: 'notification_cooldown_hours',
} as const;

// String flags
export const STRING_FLAGS = {
  DEFAULT_CURRENCY: 'default_currency',
  SUPPORT_EMAIL: 'support_email',
  PAYWALL_VARIANT: 'paywall_variant',
  ONBOARDING_FLOW: 'onboarding_flow',
  PRICING_MODEL: 'pricing_model',
  API_BASE_URL: 'api_base_url',
  CDN_BASE_URL: 'cdn_base_url',
  FEATURE_ANNOUNCEMENT: 'feature_announcement',
  PROMO_CODE: 'promo_code',
  AB_TEST_GROUP: 'ab_test_group',
} as const;

// JSON flags (complex configurations)
export const JSON_FLAGS = {
  PAYWALL_CONFIG: 'paywall_config',
  ONBOARDING_SCREENS: 'onboarding_screens',
  FEATURE_GATES: 'feature_gates',
  PRICING_TIERS: 'pricing_tiers',
  NOTIFICATION_CONFIG: 'notification_config',
  EXPERIMENT_CONFIG: 'experiment_config',
} as const;

// Combined FLAGS object
export const FLAGS = {
  ...BOOLEAN_FLAGS,
  ...NUMERIC_FLAGS,
  ...STRING_FLAGS,
  ...JSON_FLAGS,
} as const;

// Type for flag names
export type BooleanFlagName = (typeof BOOLEAN_FLAGS)[keyof typeof BOOLEAN_FLAGS];
export type NumericFlagName = (typeof NUMERIC_FLAGS)[keyof typeof NUMERIC_FLAGS];
export type StringFlagName = (typeof STRING_FLAGS)[keyof typeof STRING_FLAGS];
export type JsonFlagName = (typeof JSON_FLAGS)[keyof typeof JSON_FLAGS];
export type FlagName = (typeof FLAGS)[keyof typeof FLAGS];

// Complex config types
export interface PaywallConfig {
  variant: 'minimal' | 'feature_list' | 'social_proof' | 'urgency';
  showAnnual: boolean;
  showLifetime: boolean;
  defaultSelection: 'monthly' | 'annual' | 'lifetime';
  trialDays: number;
  features: string[];
  testimonials?: Array<{
    name: string;
    text: string;
    rating: number;
  }>;
}

export interface OnboardingScreen {
  id: string;
  title: string;
  subtitle: string;
  image: string;
  skippable: boolean;
}

export interface FeatureGate {
  featureId: string;
  requiredPlan: 'free' | 'premium' | 'pro';
  usageLimit?: number;
}

export interface PricingTier {
  id: string;
  name: string;
  priceMonthly: number;
  priceAnnual: number;
  features: string[];
  highlighted?: boolean;
}

export interface NotificationConfig {
  streakReminder: {
    enabled: boolean;
    time: string;
  };
  weeklyDigest: {
    enabled: boolean;
    dayOfWeek: number;
  };
  promotions: {
    enabled: boolean;
    maxPerWeek: number;
  };
}

export interface ExperimentConfigValue {
  id: string;
  name: string;
  variants: string[];
  weights: number[];
  active: boolean;
}

// Flag value map
export interface FlagValueMap {
  // Boolean flags
  [BOOLEAN_FLAGS.SHOW_NEW_PAYWALL]: boolean;
  [BOOLEAN_FLAGS.ENABLE_STREAK_SHARING]: boolean;
  [BOOLEAN_FLAGS.SHOW_ANNUAL_OPTION]: boolean;
  [BOOLEAN_FLAGS.ENABLE_DARK_MODE]: boolean;
  [BOOLEAN_FLAGS.SHOW_ONBOARDING_V2]: boolean;
  [BOOLEAN_FLAGS.ENABLE_PUSH_NOTIFICATIONS]: boolean;
  [BOOLEAN_FLAGS.SHOW_REFERRAL_PROGRAM]: boolean;
  [BOOLEAN_FLAGS.ENABLE_OFFLINE_MODE]: boolean;
  [BOOLEAN_FLAGS.SHOW_RATING_PROMPT]: boolean;
  [BOOLEAN_FLAGS.ENABLE_HAPTIC_FEEDBACK]: boolean;
  [BOOLEAN_FLAGS.SHOW_PREMIUM_FEATURES]: boolean;
  [BOOLEAN_FLAGS.ENABLE_ANALYTICS_DEBUG]: boolean;
  [BOOLEAN_FLAGS.SHOW_BETA_FEATURES]: boolean;
  [BOOLEAN_FLAGS.ENABLE_CRASH_REPORTING]: boolean;
  [BOOLEAN_FLAGS.MAINTENANCE_MODE]: boolean;

  // Numeric flags
  [NUMERIC_FLAGS.TRIAL_LENGTH_DAYS]: number;
  [NUMERIC_FLAGS.MAX_FREE_USES]: number;
  [NUMERIC_FLAGS.PAYWALL_DELAY_SECONDS]: number;
  [NUMERIC_FLAGS.SESSION_TIMEOUT_MINUTES]: number;
  [NUMERIC_FLAGS.MIN_VERSION_REQUIRED]: number;
  [NUMERIC_FLAGS.RATING_PROMPT_THRESHOLD]: number;
  [NUMERIC_FLAGS.CACHE_TTL_MINUTES]: number;
  [NUMERIC_FLAGS.API_TIMEOUT_SECONDS]: number;
  [NUMERIC_FLAGS.MAX_RETRY_ATTEMPTS]: number;
  [NUMERIC_FLAGS.NOTIFICATION_COOLDOWN_HOURS]: number;

  // String flags
  [STRING_FLAGS.DEFAULT_CURRENCY]: string;
  [STRING_FLAGS.SUPPORT_EMAIL]: string;
  [STRING_FLAGS.PAYWALL_VARIANT]: string;
  [STRING_FLAGS.ONBOARDING_FLOW]: string;
  [STRING_FLAGS.PRICING_MODEL]: string;
  [STRING_FLAGS.API_BASE_URL]: string;
  [STRING_FLAGS.CDN_BASE_URL]: string;
  [STRING_FLAGS.FEATURE_ANNOUNCEMENT]: string;
  [STRING_FLAGS.PROMO_CODE]: string;
  [STRING_FLAGS.AB_TEST_GROUP]: string;

  // JSON flags
  [JSON_FLAGS.PAYWALL_CONFIG]: PaywallConfig;
  [JSON_FLAGS.ONBOARDING_SCREENS]: OnboardingScreen[];
  [JSON_FLAGS.FEATURE_GATES]: FeatureGate[];
  [JSON_FLAGS.PRICING_TIERS]: PricingTier[];
  [JSON_FLAGS.NOTIFICATION_CONFIG]: NotificationConfig;
  [JSON_FLAGS.EXPERIMENT_CONFIG]: ExperimentConfigValue;
}

// Default values for all flags
export const DEFAULT_FLAG_VALUES: FlagValueMap = {
  // Boolean flags
  [BOOLEAN_FLAGS.SHOW_NEW_PAYWALL]: false,
  [BOOLEAN_FLAGS.ENABLE_STREAK_SHARING]: false,
  [BOOLEAN_FLAGS.SHOW_ANNUAL_OPTION]: true,
  [BOOLEAN_FLAGS.ENABLE_DARK_MODE]: true,
  [BOOLEAN_FLAGS.SHOW_ONBOARDING_V2]: false,
  [BOOLEAN_FLAGS.ENABLE_PUSH_NOTIFICATIONS]: true,
  [BOOLEAN_FLAGS.SHOW_REFERRAL_PROGRAM]: false,
  [BOOLEAN_FLAGS.ENABLE_OFFLINE_MODE]: false,
  [BOOLEAN_FLAGS.SHOW_RATING_PROMPT]: true,
  [BOOLEAN_FLAGS.ENABLE_HAPTIC_FEEDBACK]: true,
  [BOOLEAN_FLAGS.SHOW_PREMIUM_FEATURES]: true,
  [BOOLEAN_FLAGS.ENABLE_ANALYTICS_DEBUG]: false,
  [BOOLEAN_FLAGS.SHOW_BETA_FEATURES]: false,
  [BOOLEAN_FLAGS.ENABLE_CRASH_REPORTING]: true,
  [BOOLEAN_FLAGS.MAINTENANCE_MODE]: false,

  // Numeric flags
  [NUMERIC_FLAGS.TRIAL_LENGTH_DAYS]: 7,
  [NUMERIC_FLAGS.MAX_FREE_USES]: 3,
  [NUMERIC_FLAGS.PAYWALL_DELAY_SECONDS]: 0,
  [NUMERIC_FLAGS.SESSION_TIMEOUT_MINUTES]: 30,
  [NUMERIC_FLAGS.MIN_VERSION_REQUIRED]: 1,
  [NUMERIC_FLAGS.RATING_PROMPT_THRESHOLD]: 5,
  [NUMERIC_FLAGS.CACHE_TTL_MINUTES]: 60,
  [NUMERIC_FLAGS.API_TIMEOUT_SECONDS]: 30,
  [NUMERIC_FLAGS.MAX_RETRY_ATTEMPTS]: 3,
  [NUMERIC_FLAGS.NOTIFICATION_COOLDOWN_HOURS]: 24,

  // String flags
  [STRING_FLAGS.DEFAULT_CURRENCY]: 'USD',
  [STRING_FLAGS.SUPPORT_EMAIL]: 'support@example.com',
  [STRING_FLAGS.PAYWALL_VARIANT]: 'default',
  [STRING_FLAGS.ONBOARDING_FLOW]: 'standard',
  [STRING_FLAGS.PRICING_MODEL]: 'subscription',
  [STRING_FLAGS.API_BASE_URL]: 'https://api.example.com',
  [STRING_FLAGS.CDN_BASE_URL]: 'https://cdn.example.com',
  [STRING_FLAGS.FEATURE_ANNOUNCEMENT]: '',
  [STRING_FLAGS.PROMO_CODE]: '',
  [STRING_FLAGS.AB_TEST_GROUP]: 'control',

  // JSON flags
  [JSON_FLAGS.PAYWALL_CONFIG]: {
    variant: 'feature_list',
    showAnnual: true,
    showLifetime: false,
    defaultSelection: 'annual',
    trialDays: 7,
    features: ['Unlimited access', 'No ads', 'Premium support'],
  },
  [JSON_FLAGS.ONBOARDING_SCREENS]: [],
  [JSON_FLAGS.FEATURE_GATES]: [],
  [JSON_FLAGS.PRICING_TIERS]: [],
  [JSON_FLAGS.NOTIFICATION_CONFIG]: {
    streakReminder: { enabled: true, time: '09:00' },
    weeklyDigest: { enabled: true, dayOfWeek: 1 },
    promotions: { enabled: false, maxPerWeek: 1 },
  },
  [JSON_FLAGS.EXPERIMENT_CONFIG]: {
    id: '',
    name: '',
    variants: ['control'],
    weights: [100],
    active: false,
  },
};

// Helper to check if a flag is a boolean flag
export function isBooleanFlag(flagName: FlagName): flagName is BooleanFlagName {
  return Object.values(BOOLEAN_FLAGS).includes(flagName as BooleanFlagName);
}

// Helper to check if a flag is a numeric flag
export function isNumericFlag(flagName: FlagName): flagName is NumericFlagName {
  return Object.values(NUMERIC_FLAGS).includes(flagName as NumericFlagName);
}

// Helper to check if a flag is a string flag
export function isStringFlag(flagName: FlagName): flagName is StringFlagName {
  return Object.values(STRING_FLAGS).includes(flagName as StringFlagName);
}

// Helper to check if a flag is a JSON flag
export function isJsonFlag(flagName: FlagName): flagName is JsonFlagName {
  return Object.values(JSON_FLAGS).includes(flagName as JsonFlagName);
}

// Get default value for a flag
export function getDefaultValue<T extends FlagName>(flagName: T): FlagValueMap[T] {
  return DEFAULT_FLAG_VALUES[flagName];
}

// Get all flag names
export function getAllFlagNames(): FlagName[] {
  return Object.values(FLAGS);
}

// Get flags by type
export function getFlagsByType(
  type: 'boolean' | 'numeric' | 'string' | 'json'
): FlagName[] {
  switch (type) {
    case 'boolean':
      return Object.values(BOOLEAN_FLAGS);
    case 'numeric':
      return Object.values(NUMERIC_FLAGS);
    case 'string':
      return Object.values(STRING_FLAGS);
    case 'json':
      return Object.values(JSON_FLAGS);
  }
}
