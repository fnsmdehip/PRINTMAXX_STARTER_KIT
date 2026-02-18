/**
 * Feature Flags Module
 *
 * Centralized feature flag and remote configuration system.
 *
 * @example
 * ```typescript
 * // Initialize
 * import { featureFlagService, FLAGS } from './feature_flags';
 *
 * await featureFlagService.initialize({
 *   provider: 'launchdarkly',
 *   providerConfig: { mobileKey: 'mob-xxx' },
 * });
 *
 * // Use in components
 * import { useFeatureFlag, FLAGS } from './feature_flags';
 *
 * function MyComponent() {
 *   const showNewPaywall = useFeatureFlag(FLAGS.SHOW_NEW_PAYWALL, false);
 *   // ...
 * }
 * ```
 */

// Core service
export { featureFlagService, FeatureFlagService, LocalProvider } from './FeatureFlagService';

// Flag definitions
export {
  FLAGS,
  BOOLEAN_FLAGS,
  NUMERIC_FLAGS,
  STRING_FLAGS,
  JSON_FLAGS,
  DEFAULT_FLAG_VALUES,
  getDefaultValue,
  getAllFlagNames,
  getFlagsByType,
  isBooleanFlag,
  isNumericFlag,
  isStringFlag,
  isJsonFlag,
} from './flags';

export type {
  FlagName,
  BooleanFlagName,
  NumericFlagName,
  StringFlagName,
  JsonFlagName,
  FlagValueMap,
  PaywallConfig,
  OnboardingScreen,
  FeatureGate,
  PricingTier,
  NotificationConfig,
  ExperimentConfigValue,
} from './flags';

// React hooks
export {
  useFeatureFlag,
  useBooleanFlag,
  useNumericFlag,
  useStringFlag,
  useJsonFlag,
  useFlagEvaluation,
  useAsyncFeatureFlag,
  useFeatureFlags,
  useFeatureFlagContext,
  useIdentifyUser,
  useRefreshFlags,
  useFeatureGate,
  useRemoteConfig,
  useOnFlagChange,
  withFeatureFlag,
} from './useFeatureFlag';

// Provider component
export {
  RemoteConfigProvider,
  useRemoteConfigContext,
  RemoteConfigConsumer,
  FeatureGate,
  ConfigValue,
  FlagErrorBoundary,
} from './RemoteConfigProvider';

// Experiments
export {
  experimentService,
  ExperimentService,
  EXPERIMENTS,
  EXPERIMENT_DEFINITIONS,
  getExperimentFlagValue,
} from './experiments';

export type {
  Experiment,
  ExperimentVariant,
  ExperimentAssignment,
  ExperimentEvent,
  ExperimentSummary,
  AudienceFilter,
  ExperimentId,
} from './experiments';

// Types
export type {
  FlagValue,
  FeatureFlagProvider,
  FeatureFlagProviderInterface,
  ProviderConfig,
  UserAttributes,
  SubscriptionStatus,
  FlagChangeCallback,
  FlagEvaluation,
  EvaluationReason,
  FeatureFlagContext,
  FeatureFlagConfig,
  CacheStrategy,
  FlagMetadata,
  RemoteConfigValue,
  TargetingRule,
  TargetingCondition,
  RolloutConfig,
  KillSwitch,
} from './types';

// Provider helpers
export { createLaunchDarklyConfig } from './providers/launchdarkly_setup';
export { createFirebaseConfig } from './providers/firebase_remote_config';
export { createStatsigConfig } from './providers/statsig_setup';
export { createPostHogConfig } from './providers/posthog_flags';
