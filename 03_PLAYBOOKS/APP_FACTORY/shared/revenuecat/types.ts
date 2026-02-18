/**
 * RevenueCat TypeScript Types
 * Shared types for subscription management across all apps
 */

// Re-export types from RevenueCat SDK for convenience
export type {
  CustomerInfo,
  PurchasesOffering,
  PurchasesOfferings,
  PurchasesPackage,
  PurchasesStoreProduct,
  PurchasesEntitlementInfo,
  PurchasesEntitlementInfos,
  PurchasesIntroPrice,
} from 'react-native-purchases';

/**
 * Subscription period types
 */
export type SubscriptionPeriod = 'monthly' | 'annual' | 'weekly' | 'lifetime';

/**
 * Entitlement identifiers used across apps
 */
export type EntitlementId = 'premium' | 'pro' | 'plus';

/**
 * Package type identifiers
 */
export type PackageType =
  | '$rc_monthly'
  | '$rc_annual'
  | '$rc_weekly'
  | '$rc_lifetime'
  | string;

/**
 * Subscription status for a user
 */
export interface SubscriptionStatus {
  /** Whether user has active premium access */
  isActive: boolean;
  /** Whether user is in a trial period */
  isInTrial: boolean;
  /** Whether subscription will renew */
  willRenew: boolean;
  /** Expiration date of current period (null if lifetime or no subscription) */
  expirationDate: Date | null;
  /** Type of current subscription period */
  periodType: 'normal' | 'trial' | 'intro' | 'none';
  /** Product ID of active subscription */
  activeProductId: string | null;
  /** Entitlement identifier */
  entitlementId: EntitlementId | null;
}

/**
 * Package display information for paywall
 */
export interface PackageDisplayInfo {
  /** Package identifier */
  identifier: string;
  /** Display title (e.g., "Monthly", "Annual") */
  title: string;
  /** Formatted price string (e.g., "$9.99") */
  priceString: string;
  /** Raw price as number */
  price: number;
  /** Currency code (e.g., "USD") */
  currencyCode: string;
  /** Duration description (e.g., "/month", "/year") */
  durationLabel: string;
  /** Per-month equivalent price for comparison */
  monthlyEquivalent: number;
  /** Savings percentage compared to monthly */
  savingsPercent: number | null;
  /** Trial information if available */
  trial: TrialInfo | null;
  /** Whether this is the recommended package */
  isRecommended: boolean;
  /** Original RevenueCat package */
  package: import('react-native-purchases').PurchasesPackage;
}

/**
 * Trial period information
 */
export interface TrialInfo {
  /** Number of trial units */
  duration: number;
  /** Unit type (day, week, month) */
  unit: 'day' | 'week' | 'month' | 'year';
  /** Formatted trial string (e.g., "7-day free trial") */
  displayString: string;
}

/**
 * Purchase result
 */
export interface PurchaseResult {
  /** Whether purchase was successful */
  success: boolean;
  /** Error message if failed */
  error?: string;
  /** Error code for programmatic handling */
  errorCode?: PurchaseErrorCode;
  /** Whether user cancelled the purchase */
  userCancelled: boolean;
  /** Updated customer info after purchase */
  customerInfo?: import('react-native-purchases').CustomerInfo;
}

/**
 * Purchase error codes
 */
export enum PurchaseErrorCode {
  Unknown = 'unknown',
  UserCancelled = 'user_cancelled',
  PaymentPending = 'payment_pending',
  PaymentInvalid = 'payment_invalid',
  NetworkError = 'network_error',
  ProductNotAvailable = 'product_not_available',
  PurchaseNotAllowed = 'purchase_not_allowed',
  AlreadyPurchased = 'already_purchased',
  ReceiptInvalid = 'receipt_invalid',
  StoreProblem = 'store_problem',
}

/**
 * Restore purchases result
 */
export interface RestoreResult {
  /** Whether restore was successful */
  success: boolean;
  /** Whether any purchases were found and restored */
  purchasesRestored: boolean;
  /** Error message if failed */
  error?: string;
  /** Updated customer info after restore */
  customerInfo?: import('react-native-purchases').CustomerInfo;
}

/**
 * Offerings state for paywall
 */
export interface OfferingsState {
  /** Current offering */
  current: import('react-native-purchases').PurchasesOffering | null;
  /** All available offerings */
  all: Record<string, import('react-native-purchases').PurchasesOffering>;
  /** Loading state */
  isLoading: boolean;
  /** Error if fetch failed */
  error: string | null;
}

/**
 * RevenueCat context value
 */
export interface RevenueCatContextValue {
  /** Whether SDK is initialized */
  isInitialized: boolean;
  /** Current customer info */
  customerInfo: import('react-native-purchases').CustomerInfo | null;
  /** Subscription status */
  subscriptionStatus: SubscriptionStatus;
  /** Offerings state */
  offerings: OfferingsState;
  /** Refresh customer info */
  refreshCustomerInfo: () => Promise<void>;
  /** Refresh offerings */
  refreshOfferings: () => Promise<void>;
}

/**
 * Paywall props
 */
export interface PaywallProps {
  /** Called when purchase completes successfully */
  onPurchaseComplete: () => void;
  /** Called when paywall is closed */
  onClose: () => void;
  /** Optional title override */
  title?: string;
  /** Optional subtitle override */
  subtitle?: string;
  /** Features to display */
  features?: string[];
  /** Whether to show restore button */
  showRestore?: boolean;
  /** Custom theme colors */
  theme?: PaywallTheme;
  /** Source for analytics */
  source?: string;
}

/**
 * Paywall theme customization
 */
export interface PaywallTheme {
  /** Background color */
  backgroundColor?: string;
  /** Primary text color */
  textColor?: string;
  /** Secondary text color */
  subtextColor?: string;
  /** Primary accent color */
  accentColor?: string;
  /** Success color (checkmarks, etc.) */
  successColor?: string;
  /** Button text color */
  buttonTextColor?: string;
  /** Border color */
  borderColor?: string;
  /** Recommended package background */
  recommendedBackground?: string;
}

/**
 * App configuration for RevenueCat
 */
export interface AppConfig {
  /** App identifier */
  appId: string;
  /** iOS API key */
  iosApiKey: string;
  /** Android API key (optional) */
  androidApiKey?: string;
  /** Default entitlement to check */
  entitlementId: EntitlementId;
  /** Product IDs */
  products: {
    monthly: string;
    annual: string;
    weekly?: string;
    lifetime?: string;
  };
}

/**
 * Webhook event types from RevenueCat
 */
export type WebhookEventType =
  | 'INITIAL_PURCHASE'
  | 'RENEWAL'
  | 'CANCELLATION'
  | 'UNCANCELLATION'
  | 'EXPIRATION'
  | 'BILLING_ISSUE'
  | 'PRODUCT_CHANGE'
  | 'SUBSCRIPTION_PAUSED'
  | 'SUBSCRIPTION_EXTENDED'
  | 'TRANSFER'
  | 'NON_RENEWING_PURCHASE'
  | 'SUBSCRIPTION_STARTED'
  | 'TRIAL_CONVERTED'
  | 'TRIAL_CANCELLED';

/**
 * Webhook event payload
 */
export interface WebhookEvent {
  /** Event type */
  type: WebhookEventType;
  /** App user ID */
  app_user_id: string;
  /** Product ID */
  product_id: string;
  /** Event timestamp in milliseconds */
  event_timestamp_ms: number;
  /** Entitlement identifiers affected */
  entitlement_ids: string[];
  /** Store (app_store, play_store, stripe) */
  store: 'app_store' | 'play_store' | 'stripe';
  /** Environment */
  environment: 'SANDBOX' | 'PRODUCTION';
  /** Expiration date if applicable */
  expiration_at_ms?: number;
  /** Price in micros */
  price_in_purchased_currency?: number;
  /** Currency code */
  currency?: string;
  /** Transaction ID */
  transaction_id?: string;
  /** Original transaction ID */
  original_transaction_id?: string;
  /** Is trial conversion */
  is_trial_conversion?: boolean;
  /** Cancellation reason */
  cancellation_reason?: string;
}
