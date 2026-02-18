/**
 * Feature Flag Types
 *
 * Shared type definitions for the feature flag system.
 */

import type { FlagName, FlagValueMap } from './flags';

// Feature flag value types
export type FlagValue = boolean | string | number | Record<string, unknown>;

// Provider names
export type FeatureFlagProvider =
  | 'launchdarkly'
  | 'firebase'
  | 'statsig'
  | 'posthog'
  | 'local';

// Provider interface that all flag providers must implement
export interface FeatureFlagProviderInterface {
  name: FeatureFlagProvider;
  initialize(config: ProviderConfig): Promise<void>;
  identify(userId: string, attributes?: UserAttributes): Promise<void>;
  getFlag<T extends FlagName>(flagName: T, defaultValue: FlagValueMap[T]): FlagValueMap[T];
  getFlagAsync<T extends FlagName>(
    flagName: T,
    defaultValue: FlagValueMap[T]
  ): Promise<FlagValueMap[T]>;
  getAllFlags(): Promise<Partial<FlagValueMap>>;
  refresh(): Promise<void>;
  close(): Promise<void>;
  isReady(): boolean;
  onFlagChange(callback: FlagChangeCallback): () => void;
}

// Provider configuration
export interface ProviderConfig {
  apiKey?: string;
  mobileKey?: string;
  clientKey?: string;
  projectId?: string;
  environment?: 'development' | 'staging' | 'production';
  debug?: boolean;
  offline?: boolean;
  refreshInterval?: number; // ms
  connectionTimeout?: number; // ms
  evaluationTimeout?: number; // ms
  cacheExpiration?: number; // ms
}

// User attributes for targeting
export interface UserAttributes {
  email?: string;
  name?: string;
  country?: string;
  app_version?: string;
  platform?: 'ios' | 'android';
  os_version?: string;
  device_type?: string;
  subscription_status?: SubscriptionStatus;
  plan?: string;
  is_beta_tester?: boolean;
  install_date?: string;
  days_since_install?: number;
  session_count?: number;
  custom?: Record<string, string | number | boolean>;
}

// Subscription status
export type SubscriptionStatus =
  | 'free'
  | 'trial'
  | 'active'
  | 'cancelled'
  | 'expired'
  | 'grace_period';

// Flag change callback
export type FlagChangeCallback = (
  flagName: FlagName,
  oldValue: FlagValue,
  newValue: FlagValue
) => void;

// Feature flag evaluation result with metadata
export interface FlagEvaluation<T extends FlagValue = FlagValue> {
  value: T;
  source: 'provider' | 'cache' | 'default';
  reason: EvaluationReason;
  timestamp: number;
  flagName: string;
}

// Evaluation reason
export type EvaluationReason =
  | 'match'
  | 'default'
  | 'off'
  | 'error'
  | 'prerequisite_failed'
  | 'target_match'
  | 'rule_match'
  | 'fallthrough'
  | 'stale_cache';

// Feature flag context for the app
export interface FeatureFlagContext {
  isReady: boolean;
  isLoading: boolean;
  error: Error | null;
  userId?: string;
  lastRefresh?: number;
  provider: FeatureFlagProvider;
}

// Feature flag configuration
export interface FeatureFlagConfig {
  provider: FeatureFlagProvider;
  providerConfig: ProviderConfig;
  defaultFlags?: Partial<FlagValueMap>;
  cacheStrategy?: CacheStrategy;
  refreshOnForeground?: boolean;
  refreshOnReconnect?: boolean;
  logEvaluations?: boolean;
  onError?: (error: Error) => void;
}

// Cache strategy
export interface CacheStrategy {
  enabled: boolean;
  storage: 'memory' | 'async_storage' | 'mmkv';
  ttl: number; // ms
  staleWhileRevalidate?: boolean;
}

// Flag metadata for documentation
export interface FlagMetadata {
  name: FlagName;
  type: 'boolean' | 'string' | 'number' | 'json';
  defaultValue: FlagValue;
  description: string;
  owner: string;
  createdDate: string;
  expiryDate?: string;
  tags?: string[];
  jiraTicket?: string;
  permanent?: boolean;
}

// Remote config specific types
export interface RemoteConfigValue {
  value: FlagValue;
  source: 'default' | 'remote' | 'static';
  fetchTime?: number;
}

// Targeting rule
export interface TargetingRule {
  id: string;
  conditions: TargetingCondition[];
  variation: FlagValue;
  percentage?: number;
}

export interface TargetingCondition {
  attribute: keyof UserAttributes | string;
  operator: 'equals' | 'not_equals' | 'contains' | 'starts_with' | 'ends_with' | 'gt' | 'lt' | 'gte' | 'lte' | 'in' | 'not_in';
  value: string | number | boolean | string[] | number[];
}

// Rollout configuration
export interface RolloutConfig {
  percentage: number;
  salt?: string;
  sticky?: boolean;
}

// Kill switch configuration
export interface KillSwitch {
  flagName: FlagName;
  reason: string;
  activatedAt: number;
  activatedBy: string;
  autoRevert?: {
    enabled: boolean;
    revertAfter: number; // ms
  };
}
