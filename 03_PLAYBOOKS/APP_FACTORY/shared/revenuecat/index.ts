/**
 * RevenueCat Integration
 * Shared subscription management for React Native apps
 *
 * @example
 * ```tsx
 * import {
 *   RevenueCatProvider,
 *   getAppConfig,
 *   useSubscription,
 *   usePurchase,
 *   Paywall,
 * } from './revenuecat';
 *
 * function App() {
 *   return (
 *     <RevenueCatProvider config={getAppConfig('myapp')}>
 *       <MainApp />
 *     </RevenueCatProvider>
 *   );
 * }
 * ```
 */

// Provider and context
export {
  RevenueCatProvider,
  useRevenueCat,
  useRevenueCatReady,
  useCustomerInfo,
  logoutRevenueCat,
  setUserAttributes,
  setUserEmail,
  setUserDisplayName,
} from './RevenueCatProvider';

// Subscription hooks
export {
  useSubscription,
  usePremiumStatus,
  useTrialStatus,
  useSubscriptionManagement,
  useFeatureAccess,
} from './useSubscription';

export type {
  UseSubscriptionReturn,
  UseTrialStatusReturn,
  UseSubscriptionManagementReturn,
} from './useSubscription';

// Purchase hooks
export {
  usePurchase,
  useRestorePurchases,
  usePromotionalOffer,
  usePurchaseEligibility,
} from './usePurchase';

export type {
  UsePurchaseReturn,
  UseRestorePurchasesReturn,
  UsePromotionalOfferReturn,
  UsePurchaseEligibilityReturn,
} from './usePurchase';

// Components
export { Paywall, default as PaywallComponent } from './PaywallComponent';

// Configuration
export {
  APP_CONFIGS,
  PRODUCT_IDS,
  PACKAGE_IDS,
  OFFERING_IDS,
  DEFAULT_ENTITLEMENT_ID,
  ENV_KEYS,
  FEATURE_FLAGS,
  TIMEOUTS,
  ANALYTICS_EVENTS,
  getApiKey,
  getAppConfig,
  isValidApiKey,
  getLogLevel,
} from './config';

// Utilities
export {
  formatPrice,
  formatPricePerPeriod,
  calculateSavingsPercent,
  calculateMonthlyEquivalent,
  formatTrialPeriod,
  formatTrialString,
  getDurationLabel,
  getPackageTitle,
  packageToDisplayInfo,
  parseSubscriptionStatus,
  formatExpirationDate,
  formatTimeRemaining,
  isInGracePeriod,
  sortPackagesByValue,
  withTimeout,
  withRetry,
} from './utils';

// Types
export type {
  // Re-exported from RevenueCat
  CustomerInfo,
  PurchasesOffering,
  PurchasesOfferings,
  PurchasesPackage,
  PurchasesStoreProduct,
  PurchasesEntitlementInfo,
  PurchasesEntitlementInfos,
  PurchasesIntroPrice,
  // Custom types
  SubscriptionPeriod,
  EntitlementId,
  PackageType,
  SubscriptionStatus,
  PackageDisplayInfo,
  TrialInfo,
  PurchaseResult,
  PurchaseErrorCode,
  RestoreResult,
  OfferingsState,
  RevenueCatContextValue,
  PaywallProps,
  PaywallTheme,
  AppConfig,
  WebhookEventType,
  WebhookEvent,
} from './types';
