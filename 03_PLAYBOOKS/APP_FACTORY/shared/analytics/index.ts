/**
 * Analytics Module Index
 *
 * Main entry point for the analytics system.
 */

// Provider and hooks
export { AnalyticsProvider, useAnalyticsContext } from './AnalyticsProvider';
export {
  useAnalytics,
  useOnboardingAnalytics,
  useConversionAnalytics,
  useRetentionAnalytics,
  useEngagementAnalytics,
} from './useAnalytics';

// Events
export {
  EVENT_METADATA,
  getEventMetadata,
  getEventsByCategory,
  getEventsByPriority,
} from './events';
export type {
  EventCategory,
  EventPriority,
  AnalyticsEventName,
  AnalyticsEventMap,
  AnalyticsEvent,
  BaseEventProperties,
  OnboardingEvents,
  FeatureEvents,
  ConversionEvents,
  RetentionEvents,
  ErrorEvents,
  EngagementEvents,
  NavigationEvents,
} from './events';

// Types
export type {
  AnalyticsProvider as AnalyticsProviderType,
  ProviderConfig,
  UserTraits,
  UserProperties,
  SubscriptionStatus,
  RevenueData,
  SessionData,
  AnalyticsContext,
  AnalyticsConfig,
  FunnelDefinition,
  FunnelStep,
  CohortDefinition,
  CohortCriteria,
  ExperimentConfig,
  ExperimentVariant,
  ValidationResult,
  ValidationError,
} from './types';

// Providers
export {
  mixpanelProvider,
  posthogProvider,
  featureFlags,
  firebaseProvider,
  firebaseEvents,
  revenueCatProvider,
} from './providers';
export type {
  MixpanelConfig,
  PostHogConfig,
  FirebaseConfig,
  RevenueCatConfig,
  SubscriptionInfo,
} from './providers';
