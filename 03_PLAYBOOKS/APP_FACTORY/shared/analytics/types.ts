/**
 * Analytics Types
 *
 * Shared type definitions for the analytics system.
 */

import type { AnalyticsEventName, AnalyticsEventMap } from './events';

// Analytics provider interface
export interface AnalyticsProvider {
  name: string;
  initialize(config: ProviderConfig): Promise<void>;
  identify(userId: string, traits?: UserTraits): Promise<void>;
  track<T extends AnalyticsEventName>(
    event: T,
    properties: AnalyticsEventMap[T]
  ): Promise<void>;
  setUserProperties(properties: UserProperties): Promise<void>;
  reset(): Promise<void>;
  flush(): Promise<void>;
  isEnabled(): boolean;
  setEnabled(enabled: boolean): void;
}

// Provider configuration
export interface ProviderConfig {
  apiKey?: string;
  projectId?: string;
  debug?: boolean;
  flushInterval?: number;
  batchSize?: number;
  optOut?: boolean;
}

// User traits for identification
export interface UserTraits {
  email?: string;
  name?: string;
  created_at?: string;
  plan?: string;
  subscription_status?: SubscriptionStatus;
  trial_end_date?: string;
  lifetime_value?: number;
  install_source?: string;
  referral_code?: string;
  [key: string]: unknown;
}

// User properties that can be set independently
export interface UserProperties {
  app_version?: string;
  device_model?: string;
  os_version?: string;
  locale?: string;
  timezone?: string;
  notifications_enabled?: boolean;
  tracking_enabled?: boolean;
  subscription_status?: SubscriptionStatus;
  subscription_product?: string;
  trial_active?: boolean;
  days_since_install?: number;
  session_count?: number;
  total_events?: number;
  last_active_at?: string;
  features_used?: string[];
  [key: string]: unknown;
}

// Subscription status
export type SubscriptionStatus =
  | 'free'
  | 'trial'
  | 'active'
  | 'cancelled'
  | 'expired'
  | 'grace_period';

// Revenue data for tracking purchases
export interface RevenueData {
  amount: number;
  currency: string;
  product_id: string;
  quantity?: number;
  receipt?: string;
  is_trial_conversion?: boolean;
  is_renewal?: boolean;
}

// Session data
export interface SessionData {
  session_id: string;
  started_at: string;
  ended_at?: string;
  duration_ms?: number;
  screens_visited: string[];
  events: Array<{
    name: string;
    timestamp: string;
  }>;
  is_first_session: boolean;
  session_number: number;
}

// Analytics context available throughout the app
export interface AnalyticsContext {
  userId?: string;
  anonymousId: string;
  sessionId: string;
  sessionNumber: number;
  deviceId: string;
  appVersion: string;
  buildNumber: string;
  platform: 'ios' | 'android';
  osVersion: string;
  deviceModel: string;
  locale: string;
  timezone: string;
  isFirstSession: boolean;
  daysSinceInstall: number;
  installSource?: string;
}

// Analytics configuration
export interface AnalyticsConfig {
  providers: {
    mixpanel?: ProviderConfig;
    posthog?: ProviderConfig;
    firebase?: ProviderConfig;
    revenuecat?: ProviderConfig;
  };
  debug?: boolean;
  enabled?: boolean;
  sessionTimeout?: number; // ms
  flushInterval?: number; // ms
  batchSize?: number;
  anonymizeIp?: boolean;
  trackScreenViews?: boolean;
  trackAppLifecycle?: boolean;
}

// Funnel definition
export interface FunnelDefinition {
  name: string;
  steps: FunnelStep[];
  conversionWindow?: number; // hours
}

export interface FunnelStep {
  event: AnalyticsEventName;
  filters?: Record<string, unknown>;
  optional?: boolean;
}

// Cohort definition
export interface CohortDefinition {
  name: string;
  criteria: CohortCriteria[];
  combine: 'and' | 'or';
}

export interface CohortCriteria {
  type: 'event' | 'property' | 'date';
  event?: AnalyticsEventName;
  property?: string;
  operator: 'equals' | 'not_equals' | 'contains' | 'gt' | 'lt' | 'gte' | 'lte' | 'exists';
  value?: unknown;
  within_days?: number;
}

// A/B test configuration
export interface ExperimentConfig {
  id: string;
  name: string;
  variants: ExperimentVariant[];
  allocation?: Record<string, number>; // variant_id -> percentage
  active: boolean;
}

export interface ExperimentVariant {
  id: string;
  name: string;
  payload?: Record<string, unknown>;
}

// Event validation result
export interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
}

export interface ValidationError {
  field: string;
  message: string;
  received: unknown;
  expected: string;
}
