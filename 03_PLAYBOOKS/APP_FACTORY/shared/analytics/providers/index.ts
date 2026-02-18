/**
 * Analytics Providers Index
 *
 * Re-exports all analytics providers for easy imports.
 */

export { mixpanelProvider, default as Mixpanel } from './mixpanel';
export type { MixpanelConfig } from './mixpanel';

export { posthogProvider, featureFlags, default as PostHog } from './posthog';
export type { PostHogConfig } from './posthog';

export { firebaseProvider, firebaseEvents, default as Firebase } from './firebase';
export type { FirebaseConfig } from './firebase';

export { revenueCatProvider, default as RevenueCat } from './revenuecat';
export type { RevenueCatConfig, SubscriptionInfo } from './revenuecat';
