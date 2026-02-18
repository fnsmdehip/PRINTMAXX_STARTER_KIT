/**
 * RevenueCat Analytics Provider
 *
 * Integration with RevenueCat for subscription analytics and revenue tracking.
 * Handles purchase events, subscription status, and revenue attribution.
 */

import Purchases, {
  PurchasesPackage,
  CustomerInfo,
  PurchasesEntitlementInfo,
  LOG_LEVEL,
} from 'react-native-purchases';
import type { ProviderConfig, RevenueData, SubscriptionStatus } from '../types';
import type { AnalyticsEventMap } from '../events';

// RevenueCat-specific configuration
export interface RevenueCatConfig extends ProviderConfig {
  apiKey: string;
  appUserID?: string;
  observerMode?: boolean;
  useAmazon?: boolean;
  userDefaultsSuiteName?: string;
}

// Subscription info type
export interface SubscriptionInfo {
  isActive: boolean;
  status: SubscriptionStatus;
  productId?: string;
  expirationDate?: Date;
  willRenew: boolean;
  isTrialPeriod: boolean;
  isSandbox: boolean;
  originalPurchaseDate?: Date;
  latestPurchaseDate?: Date;
  managementUrl?: string;
}

// Event callbacks
type EventCallback<T extends keyof RevenueCatEvents> = (
  data: RevenueCatEvents[T]
) => void;

interface RevenueCatEvents {
  purchase_completed: AnalyticsEventMap['purchase_completed'];
  trial_started: AnalyticsEventMap['trial_started'];
  subscription_renewed: AnalyticsEventMap['subscription_renewed'];
  subscription_cancelled: AnalyticsEventMap['subscription_cancelled'];
  purchase_restored: AnalyticsEventMap['purchase_restored'];
  customer_info_updated: { customerInfo: CustomerInfo };
}

// State
let isInitialized = false;
let isEnabled = true;
let debugMode = false;
let currentCustomerInfo: CustomerInfo | null = null;
const eventListeners: Map<keyof RevenueCatEvents, Set<EventCallback<never>>> = new Map();

/**
 * Initialize RevenueCat
 */
export async function initializeRevenueCat(config: RevenueCatConfig): Promise<void> {
  if (isInitialized) {
    log('RevenueCat already initialized');
    return;
  }

  if (!config.apiKey) {
    throw new Error('RevenueCat API key is required');
  }

  debugMode = config.debug ?? false;

  try {
    // Set log level
    if (config.debug) {
      Purchases.setLogLevel(LOG_LEVEL.DEBUG);
    }

    // Configure SDK
    const configOptions: {
      apiKey: string;
      appUserID?: string | null;
      observerMode?: boolean;
      useAmazon?: boolean;
      userDefaultsSuiteName?: string;
    } = {
      apiKey: config.apiKey,
    };

    if (config.appUserID) {
      configOptions.appUserID = config.appUserID;
    }
    if (config.observerMode !== undefined) {
      configOptions.observerMode = config.observerMode;
    }
    if (config.useAmazon !== undefined) {
      configOptions.useAmazon = config.useAmazon;
    }
    if (config.userDefaultsSuiteName) {
      configOptions.userDefaultsSuiteName = config.userDefaultsSuiteName;
    }

    await Purchases.configure(configOptions);

    // Set up customer info listener
    Purchases.addCustomerInfoUpdateListener((info) => {
      const previousInfo = currentCustomerInfo;
      currentCustomerInfo = info;
      handleCustomerInfoUpdate(info, previousInfo);
    });

    // Get initial customer info
    currentCustomerInfo = await Purchases.getCustomerInfo();

    isEnabled = !config.optOut;
    isInitialized = true;
    log('RevenueCat initialized successfully');
  } catch (error) {
    console.error('[RevenueCat] Initialization failed:', error);
    throw error;
  }
}

/**
 * Identify a user
 */
export async function identifyUser(userId: string): Promise<CustomerInfo> {
  if (!isInitialized) {
    throw new Error('RevenueCat not initialized');
  }

  try {
    const { customerInfo } = await Purchases.logIn(userId);
    currentCustomerInfo = customerInfo;
    log(`User identified: ${userId}`);
    return customerInfo;
  } catch (error) {
    console.error('[RevenueCat] Identify failed:', error);
    throw error;
  }
}

/**
 * Get current customer info
 */
export async function getCustomerInfo(): Promise<CustomerInfo> {
  if (!isInitialized) {
    throw new Error('RevenueCat not initialized');
  }

  try {
    const info = await Purchases.getCustomerInfo();
    currentCustomerInfo = info;
    return info;
  } catch (error) {
    console.error('[RevenueCat] Get customer info failed:', error);
    throw error;
  }
}

/**
 * Get subscription info
 */
export async function getSubscriptionInfo(
  entitlementId: string = 'premium'
): Promise<SubscriptionInfo> {
  const info = await getCustomerInfo();
  const entitlement = info.entitlements.active[entitlementId];

  if (!entitlement) {
    return {
      isActive: false,
      status: 'free',
      willRenew: false,
      isTrialPeriod: false,
      isSandbox: info.entitlements.all[entitlementId]?.isSandbox ?? false,
    };
  }

  return entitlementToSubscriptionInfo(entitlement);
}

/**
 * Get available packages
 */
export async function getPackages(): Promise<PurchasesPackage[]> {
  if (!isInitialized) {
    throw new Error('RevenueCat not initialized');
  }

  try {
    const offerings = await Purchases.getOfferings();
    return offerings.current?.availablePackages ?? [];
  } catch (error) {
    console.error('[RevenueCat] Get packages failed:', error);
    throw error;
  }
}

/**
 * Purchase a package
 */
export async function purchasePackage(
  pkg: PurchasesPackage
): Promise<{ customerInfo: CustomerInfo; productId: string }> {
  if (!isInitialized || !isEnabled) {
    throw new Error('RevenueCat not ready');
  }

  try {
    const { customerInfo } = await Purchases.purchasePackage(pkg);
    currentCustomerInfo = customerInfo;

    const productId = pkg.product.identifier;

    // Track purchase event
    const purchaseEvent: AnalyticsEventMap['purchase_completed'] = {
      product_id: productId,
      price: pkg.product.price,
      currency: pkg.product.currencyCode,
      is_trial: false, // Will be updated if trial
      transaction_id: customerInfo.originalAppUserId, // Best available
    };

    // Check if this was a trial
    const entitlement = Object.values(customerInfo.entitlements.active)[0];
    if (entitlement?.periodType === 'TRIAL') {
      purchaseEvent.is_trial = true;
      emitEvent('trial_started', {
        product_id: productId,
        trial_duration_days: 7, // Would need to get from product
        paywall_id: 'default',
      });
    } else {
      emitEvent('purchase_completed', purchaseEvent);
    }

    log(`Package purchased: ${productId}`);
    return { customerInfo, productId };
  } catch (error) {
    console.error('[RevenueCat] Purchase failed:', error);
    throw error;
  }
}

/**
 * Restore purchases
 */
export async function restorePurchases(): Promise<CustomerInfo> {
  if (!isInitialized) {
    throw new Error('RevenueCat not initialized');
  }

  try {
    const info = await Purchases.restorePurchases();
    currentCustomerInfo = info;

    // Check if any entitlements were restored
    const activeEntitlements = Object.entries(info.entitlements.active);
    if (activeEntitlements.length > 0) {
      const [, entitlement] = activeEntitlements[0];
      emitEvent('purchase_restored', {
        product_id: entitlement.productIdentifier,
        original_purchase_date: entitlement.originalPurchaseDate ?? new Date().toISOString(),
      });
    }

    log('Purchases restored');
    return info;
  } catch (error) {
    console.error('[RevenueCat] Restore failed:', error);
    throw error;
  }
}

/**
 * Check if user has active entitlement
 */
export async function hasActiveEntitlement(
  entitlementId: string = 'premium'
): Promise<boolean> {
  const info = await getCustomerInfo();
  return info.entitlements.active[entitlementId] !== undefined;
}

/**
 * Set attributes (for attribution and analytics)
 */
export async function setAttributes(
  attributes: Record<string, string | null>
): Promise<void> {
  if (!isInitialized) {
    return;
  }

  try {
    await Purchases.setAttributes(attributes);
    log('Attributes set:', attributes);
  } catch (error) {
    console.error('[RevenueCat] Set attributes failed:', error);
    throw error;
  }
}

/**
 * Set email
 */
export async function setEmail(email: string): Promise<void> {
  if (!isInitialized) {
    return;
  }

  try {
    await Purchases.setEmail(email);
    log(`Email set: ${email}`);
  } catch (error) {
    console.error('[RevenueCat] Set email failed:', error);
    throw error;
  }
}

/**
 * Set phone number
 */
export async function setPhoneNumber(phoneNumber: string): Promise<void> {
  if (!isInitialized) {
    return;
  }

  try {
    await Purchases.setPhoneNumber(phoneNumber);
    log(`Phone number set`);
  } catch (error) {
    console.error('[RevenueCat] Set phone number failed:', error);
    throw error;
  }
}

/**
 * Set display name
 */
export async function setDisplayName(displayName: string): Promise<void> {
  if (!isInitialized) {
    return;
  }

  try {
    await Purchases.setDisplayName(displayName);
    log(`Display name set: ${displayName}`);
  } catch (error) {
    console.error('[RevenueCat] Set display name failed:', error);
    throw error;
  }
}

/**
 * Set push token
 */
export async function setPushToken(pushToken: string): Promise<void> {
  if (!isInitialized) {
    return;
  }

  try {
    await Purchases.setPushToken(pushToken);
    log('Push token set');
  } catch (error) {
    console.error('[RevenueCat] Set push token failed:', error);
    throw error;
  }
}

/**
 * Set campaign
 */
export async function setCampaign(campaign: string): Promise<void> {
  if (!isInitialized) {
    return;
  }

  try {
    await Purchases.setCampaign(campaign);
    log(`Campaign set: ${campaign}`);
  } catch (error) {
    console.error('[RevenueCat] Set campaign failed:', error);
    throw error;
  }
}

/**
 * Set media source (for attribution)
 */
export async function setMediaSource(mediaSource: string): Promise<void> {
  if (!isInitialized) {
    return;
  }

  try {
    await Purchases.setMediaSource(mediaSource);
    log(`Media source set: ${mediaSource}`);
  } catch (error) {
    console.error('[RevenueCat] Set media source failed:', error);
    throw error;
  }
}

/**
 * Log out current user
 */
export async function logOut(): Promise<CustomerInfo> {
  if (!isInitialized) {
    throw new Error('RevenueCat not initialized');
  }

  try {
    const info = await Purchases.logOut();
    currentCustomerInfo = info;
    log('User logged out');
    return info;
  } catch (error) {
    console.error('[RevenueCat] Log out failed:', error);
    throw error;
  }
}

/**
 * Reset user
 */
export async function reset(): Promise<void> {
  await logOut();
}

/**
 * Add event listener
 */
export function addEventListener<T extends keyof RevenueCatEvents>(
  event: T,
  callback: EventCallback<T>
): () => void {
  if (!eventListeners.has(event)) {
    eventListeners.set(event, new Set());
  }

  const listeners = eventListeners.get(event) as Set<EventCallback<T>>;
  listeners.add(callback);

  return () => {
    listeners.delete(callback);
  };
}

/**
 * Enable/disable
 */
export function setEnabled(enabled: boolean): void {
  isEnabled = enabled;
  log(`RevenueCat ${enabled ? 'enabled' : 'disabled'}`);
}

/**
 * Check if enabled
 */
export function getIsEnabled(): boolean {
  return isEnabled && isInitialized;
}

/**
 * Get revenue data from customer info
 */
export function extractRevenueData(
  customerInfo: CustomerInfo,
  productId: string,
  price: number,
  currency: string
): RevenueData {
  const entitlement = Object.values(customerInfo.entitlements.active).find(
    (e) => e.productIdentifier === productId
  );

  return {
    amount: price,
    currency,
    product_id: productId,
    quantity: 1,
    is_trial_conversion: entitlement?.periodType === 'NORMAL' && !!entitlement,
    is_renewal:
      customerInfo.allPurchaseDates[productId] !==
      customerInfo.originalPurchaseDate,
  };
}

// Internal functions

function handleCustomerInfoUpdate(
  info: CustomerInfo,
  previousInfo: CustomerInfo | null
): void {
  emitEvent('customer_info_updated', { customerInfo: info });

  if (!previousInfo) return;

  // Check for subscription changes
  for (const [entitlementId, entitlement] of Object.entries(
    info.entitlements.active
  )) {
    const previousEntitlement = previousInfo.entitlements.active[entitlementId];

    // New subscription or renewal
    if (!previousEntitlement) {
      // This could be a renewal
      if (previousInfo.entitlements.all[entitlementId]) {
        emitEvent('subscription_renewed', {
          product_id: entitlement.productIdentifier,
          renewal_count: 1, // Would need to track this
          price: 0, // Would need product info
          currency: 'USD',
        });
      }
    }
  }

  // Check for cancelled subscriptions
  for (const [entitlementId] of Object.entries(
    previousInfo.entitlements.active
  )) {
    if (!info.entitlements.active[entitlementId]) {
      const entitlement = previousInfo.entitlements.active[entitlementId];
      const expirationDate = entitlement.expirationDate
        ? new Date(entitlement.expirationDate)
        : new Date();
      const now = new Date();
      const daysUntilExpiry = Math.ceil(
        (expirationDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24)
      );

      emitEvent('subscription_cancelled', {
        product_id: entitlement.productIdentifier,
        days_until_expiry: Math.max(0, daysUntilExpiry),
      });
    }
  }
}

function entitlementToSubscriptionInfo(
  entitlement: PurchasesEntitlementInfo
): SubscriptionInfo {
  let status: SubscriptionStatus = 'active';

  if (entitlement.periodType === 'TRIAL') {
    status = 'trial';
  } else if (!entitlement.isActive) {
    status = 'expired';
  } else if (entitlement.willRenew === false) {
    status = 'cancelled';
  }

  return {
    isActive: entitlement.isActive,
    status,
    productId: entitlement.productIdentifier,
    expirationDate: entitlement.expirationDate
      ? new Date(entitlement.expirationDate)
      : undefined,
    willRenew: entitlement.willRenew,
    isTrialPeriod: entitlement.periodType === 'TRIAL',
    isSandbox: entitlement.isSandbox,
    originalPurchaseDate: entitlement.originalPurchaseDate
      ? new Date(entitlement.originalPurchaseDate)
      : undefined,
    latestPurchaseDate: entitlement.latestPurchaseDate
      ? new Date(entitlement.latestPurchaseDate)
      : undefined,
  };
}

function emitEvent<T extends keyof RevenueCatEvents>(
  event: T,
  data: RevenueCatEvents[T]
): void {
  const listeners = eventListeners.get(event);
  if (listeners) {
    listeners.forEach((callback) => {
      try {
        (callback as EventCallback<T>)(data);
      } catch (error) {
        console.error(`[RevenueCat] Event listener error for ${event}:`, error);
      }
    });
  }
}

function log(message: string, data?: unknown): void {
  if (debugMode) {
    if (data) {
      console.log(`[RevenueCat] ${message}`, data);
    } else {
      console.log(`[RevenueCat] ${message}`);
    }
  }
}

// Export convenience object
export const revenueCatProvider = {
  name: 'revenuecat',
  initialize: initializeRevenueCat,
  identify: identifyUser,
  getCustomerInfo,
  getSubscriptionInfo,
  getPackages,
  purchasePackage,
  restorePurchases,
  hasActiveEntitlement,
  setAttributes,
  setEmail,
  setPhoneNumber,
  setDisplayName,
  setPushToken,
  setCampaign,
  setMediaSource,
  logOut,
  reset,
  addEventListener,
  isEnabled: getIsEnabled,
  setEnabled,
};

export default revenueCatProvider;
