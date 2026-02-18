/**
 * RevenueCat Utility Functions
 * Helper functions for formatting and calculations
 */

import type {
  PurchasesPackage,
  PurchasesIntroPrice,
  CustomerInfo,
} from 'react-native-purchases';
import type {
  PackageDisplayInfo,
  TrialInfo,
  SubscriptionStatus,
  EntitlementId,
} from './types';
import { DEFAULT_ENTITLEMENT_ID } from './config';

/**
 * Format price with currency symbol
 *
 * @param price - Price as number
 * @param currencyCode - ISO currency code (e.g., "USD")
 * @returns Formatted price string (e.g., "$9.99")
 */
export function formatPrice(price: number, currencyCode: string): string {
  try {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currencyCode,
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(price);
  } catch {
    // Fallback for unsupported currency codes
    return `${currencyCode} ${price.toFixed(2)}`;
  }
}

/**
 * Format price per period
 *
 * @param price - Price as number
 * @param currencyCode - ISO currency code
 * @param period - Subscription period
 * @returns Formatted string (e.g., "$9.99/month")
 */
export function formatPricePerPeriod(
  price: number,
  currencyCode: string,
  period: 'month' | 'year' | 'week' | 'lifetime'
): string {
  const formattedPrice = formatPrice(price, currencyCode);
  if (period === 'lifetime') {
    return formattedPrice;
  }
  return `${formattedPrice}/${period}`;
}

/**
 * Calculate savings percentage between two prices
 *
 * @param regularPrice - Regular (e.g., monthly) price
 * @param discountedMonthlyEquivalent - Equivalent monthly price after discount
 * @returns Savings percentage (0-100) or null if no savings
 */
export function calculateSavingsPercent(
  regularPrice: number,
  discountedMonthlyEquivalent: number
): number | null {
  if (regularPrice <= 0 || discountedMonthlyEquivalent >= regularPrice) {
    return null;
  }
  const savings = ((regularPrice - discountedMonthlyEquivalent) / regularPrice) * 100;
  return Math.round(savings);
}

/**
 * Calculate monthly equivalent price from annual
 *
 * @param annualPrice - Annual subscription price
 * @returns Monthly equivalent price
 */
export function calculateMonthlyEquivalent(annualPrice: number): number {
  return annualPrice / 12;
}

/**
 * Format trial period information
 *
 * @param introPrice - RevenueCat intro price object
 * @returns Trial info object or null
 */
export function formatTrialPeriod(
  introPrice: PurchasesIntroPrice | null | undefined
): TrialInfo | null {
  if (!introPrice || introPrice.price !== 0) {
    return null;
  }

  const duration = introPrice.periodNumberOfUnits;
  const unit = mapPeriodUnit(introPrice.periodUnit);

  return {
    duration,
    unit,
    displayString: formatTrialString(duration, unit),
  };
}

/**
 * Map RevenueCat period unit to readable format
 */
function mapPeriodUnit(
  unit: string
): 'day' | 'week' | 'month' | 'year' {
  switch (unit.toUpperCase()) {
    case 'DAY':
      return 'day';
    case 'WEEK':
      return 'week';
    case 'MONTH':
      return 'month';
    case 'YEAR':
      return 'year';
    default:
      return 'day';
  }
}

/**
 * Format trial string for display
 *
 * @param duration - Number of units
 * @param unit - Time unit
 * @returns Formatted string (e.g., "7-day free trial")
 */
export function formatTrialString(
  duration: number,
  unit: 'day' | 'week' | 'month' | 'year'
): string {
  const plural = duration !== 1 ? 's' : '';
  return `${duration}-${unit}${plural === 's' ? '' : ''} free trial`;
}

/**
 * Get duration label for package
 *
 * @param packageType - Package type identifier
 * @returns Duration label (e.g., "/month", "/year")
 */
export function getDurationLabel(packageType: string): string {
  switch (packageType) {
    case '$rc_monthly':
    case 'MONTHLY':
      return '/month';
    case '$rc_annual':
    case 'ANNUAL':
      return '/year';
    case '$rc_weekly':
    case 'WEEKLY':
      return '/week';
    case '$rc_lifetime':
    case 'LIFETIME':
      return ' one-time';
    default:
      return '';
  }
}

/**
 * Get readable title for package type
 *
 * @param packageType - Package type identifier
 * @returns Readable title (e.g., "Monthly", "Annual")
 */
export function getPackageTitle(packageType: string): string {
  switch (packageType) {
    case '$rc_monthly':
    case 'MONTHLY':
      return 'Monthly';
    case '$rc_annual':
    case 'ANNUAL':
      return 'Annual';
    case '$rc_weekly':
    case 'WEEKLY':
      return 'Weekly';
    case '$rc_lifetime':
    case 'LIFETIME':
      return 'Lifetime';
    default:
      return 'Subscription';
  }
}

/**
 * Convert RevenueCat package to display info
 *
 * @param pkg - RevenueCat package
 * @param monthlyPrice - Monthly price for savings calculation (optional)
 * @param isRecommended - Whether this is the recommended package
 * @returns Package display info
 */
export function packageToDisplayInfo(
  pkg: PurchasesPackage,
  monthlyPrice?: number,
  isRecommended: boolean = false
): PackageDisplayInfo {
  const { product, packageType, identifier } = pkg;
  const price = product.price;
  const currencyCode = product.currencyCode;

  // Calculate monthly equivalent for annual packages
  let monthlyEquivalent = price;
  if (packageType === 'ANNUAL' || identifier === '$rc_annual') {
    monthlyEquivalent = calculateMonthlyEquivalent(price);
  }

  // Calculate savings if monthly price provided
  let savingsPercent: number | null = null;
  if (monthlyPrice && monthlyPrice > 0) {
    savingsPercent = calculateSavingsPercent(monthlyPrice, monthlyEquivalent);
  }

  // Get trial info
  const trial = formatTrialPeriod(product.introPrice);

  return {
    identifier,
    title: getPackageTitle(packageType),
    priceString: product.priceString,
    price,
    currencyCode,
    durationLabel: getDurationLabel(packageType),
    monthlyEquivalent,
    savingsPercent,
    trial,
    isRecommended,
    package: pkg,
  };
}

/**
 * Parse subscription status from customer info
 *
 * @param customerInfo - RevenueCat customer info
 * @param entitlementId - Entitlement ID to check
 * @returns Subscription status object
 */
export function parseSubscriptionStatus(
  customerInfo: CustomerInfo | null,
  entitlementId: EntitlementId = DEFAULT_ENTITLEMENT_ID
): SubscriptionStatus {
  const defaultStatus: SubscriptionStatus = {
    isActive: false,
    isInTrial: false,
    willRenew: false,
    expirationDate: null,
    periodType: 'none',
    activeProductId: null,
    entitlementId: null,
  };

  if (!customerInfo) {
    return defaultStatus;
  }

  const entitlement = customerInfo.entitlements.active[entitlementId];

  if (!entitlement) {
    return defaultStatus;
  }

  // Parse expiration date
  let expirationDate: Date | null = null;
  if (entitlement.expirationDate) {
    expirationDate = new Date(entitlement.expirationDate);
  }

  // Determine period type
  let periodType: SubscriptionStatus['periodType'] = 'normal';
  if (entitlement.periodType === 'TRIAL') {
    periodType = 'trial';
  } else if (entitlement.periodType === 'INTRO') {
    periodType = 'intro';
  }

  return {
    isActive: true,
    isInTrial: periodType === 'trial',
    willRenew: entitlement.willRenew,
    expirationDate,
    periodType,
    activeProductId: entitlement.productIdentifier,
    entitlementId,
  };
}

/**
 * Format expiration date for display
 *
 * @param date - Expiration date
 * @returns Formatted date string
 */
export function formatExpirationDate(date: Date | null): string {
  if (!date) {
    return 'Never';
  }

  const now = new Date();
  const diffMs = date.getTime() - now.getTime();
  const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24));

  if (diffDays < 0) {
    return 'Expired';
  }

  if (diffDays === 0) {
    return 'Today';
  }

  if (diffDays === 1) {
    return 'Tomorrow';
  }

  if (diffDays <= 7) {
    return `${diffDays} days`;
  }

  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined,
  });
}

/**
 * Format time remaining in trial or subscription
 *
 * @param expirationDate - Expiration date
 * @returns Formatted time remaining string
 */
export function formatTimeRemaining(expirationDate: Date | null): string {
  if (!expirationDate) {
    return '';
  }

  const now = new Date();
  const diffMs = expirationDate.getTime() - now.getTime();

  if (diffMs <= 0) {
    return 'Expired';
  }

  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  const diffHours = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));

  if (diffDays > 0) {
    return `${diffDays} day${diffDays !== 1 ? 's' : ''} remaining`;
  }

  if (diffHours > 0) {
    return `${diffHours} hour${diffHours !== 1 ? 's' : ''} remaining`;
  }

  return 'Less than an hour remaining';
}

/**
 * Check if user is in grace period (billing issue but still has access)
 *
 * @param customerInfo - RevenueCat customer info
 * @param entitlementId - Entitlement ID to check
 * @returns True if in grace period
 */
export function isInGracePeriod(
  customerInfo: CustomerInfo | null,
  entitlementId: EntitlementId = DEFAULT_ENTITLEMENT_ID
): boolean {
  if (!customerInfo) {
    return false;
  }

  const entitlement = customerInfo.entitlements.active[entitlementId];
  if (!entitlement) {
    return false;
  }

  // Check if there's a billing issue but entitlement is still active
  return entitlement.isActive && entitlement.billingIssueDetectedAt !== null;
}

/**
 * Sort packages by value (annual first, then monthly)
 *
 * @param packages - Array of packages
 * @returns Sorted packages array
 */
export function sortPackagesByValue(
  packages: PurchasesPackage[]
): PurchasesPackage[] {
  const order = ['LIFETIME', 'ANNUAL', 'SIX_MONTH', 'THREE_MONTH', 'TWO_MONTH', 'MONTHLY', 'WEEKLY'];

  return [...packages].sort((a, b) => {
    const aIndex = order.indexOf(a.packageType);
    const bIndex = order.indexOf(b.packageType);
    return (aIndex === -1 ? 999 : aIndex) - (bIndex === -1 ? 999 : bIndex);
  });
}

/**
 * Create a timeout promise for operations
 *
 * @param ms - Timeout in milliseconds
 * @param operation - Name of operation for error message
 * @returns Promise that rejects after timeout
 */
export function createTimeout<T>(ms: number, operation: string): Promise<T> {
  return new Promise((_, reject) => {
    setTimeout(() => {
      reject(new Error(`${operation} timed out after ${ms}ms`));
    }, ms);
  });
}

/**
 * Execute with timeout
 *
 * @param promise - Promise to execute
 * @param ms - Timeout in milliseconds
 * @param operation - Name of operation for error message
 * @returns Promise result or timeout error
 */
export async function withTimeout<T>(
  promise: Promise<T>,
  ms: number,
  operation: string
): Promise<T> {
  return Promise.race([promise, createTimeout<T>(ms, operation)]);
}

/**
 * Retry an operation with exponential backoff
 *
 * @param fn - Function to retry
 * @param maxRetries - Maximum number of retries
 * @param baseDelay - Base delay in milliseconds
 * @returns Result of function
 */
export async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  let lastError: Error | null = null;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));

      if (attempt < maxRetries) {
        const delay = baseDelay * Math.pow(2, attempt);
        await new Promise((resolve) => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError;
}
