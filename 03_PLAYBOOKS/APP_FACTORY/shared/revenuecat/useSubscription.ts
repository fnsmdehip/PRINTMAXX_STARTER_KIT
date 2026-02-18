/**
 * useSubscription Hook
 * Check subscription status, entitlements, and trial information
 */

import { useMemo, useCallback } from 'react';
import { useRevenueCat } from './RevenueCatProvider';
import type { SubscriptionStatus, EntitlementId } from './types';
import {
  formatExpirationDate,
  formatTimeRemaining,
  isInGracePeriod,
} from './utils';
import { DEFAULT_ENTITLEMENT_ID } from './config';

/**
 * Subscription hook return type
 */
export interface UseSubscriptionReturn {
  /** Whether subscription is loading */
  isLoading: boolean;
  /** Whether user has active subscription */
  isSubscribed: boolean;
  /** Whether user is in trial period */
  isInTrial: boolean;
  /** Whether subscription will auto-renew */
  willRenew: boolean;
  /** Expiration date or null */
  expirationDate: Date | null;
  /** Formatted expiration date string */
  expirationDateString: string;
  /** Time remaining string (e.g., "5 days remaining") */
  timeRemaining: string;
  /** Current period type */
  periodType: SubscriptionStatus['periodType'];
  /** Active product ID if subscribed */
  activeProductId: string | null;
  /** Full subscription status object */
  status: SubscriptionStatus;
  /** Whether user is in billing grace period */
  isInGracePeriod: boolean;
  /** Check if a specific entitlement is active */
  hasEntitlement: (entitlementId: EntitlementId) => boolean;
  /** Refresh subscription status */
  refresh: () => Promise<void>;
}

/**
 * Hook to access subscription status
 *
 * @returns Subscription information and utilities
 *
 * @example
 * ```tsx
 * function MyComponent() {
 *   const {
 *     isSubscribed,
 *     isInTrial,
 *     expirationDateString,
 *     timeRemaining,
 *   } = useSubscription();
 *
 *   if (!isSubscribed) {
 *     return <UpgradePrompt />;
 *   }
 *
 *   if (isInTrial) {
 *     return (
 *       <View>
 *         <Text>Trial expires: {expirationDateString}</Text>
 *         <Text>{timeRemaining}</Text>
 *         <PremiumContent />
 *       </View>
 *     );
 *   }
 *
 *   return <PremiumContent />;
 * }
 * ```
 */
export function useSubscription(): UseSubscriptionReturn {
  const {
    isInitialized,
    customerInfo,
    subscriptionStatus,
    refreshCustomerInfo,
  } = useRevenueCat();

  /**
   * Check if specific entitlement is active
   */
  const hasEntitlement = useCallback(
    (entitlementId: EntitlementId): boolean => {
      if (!customerInfo) return false;
      return customerInfo.entitlements.active[entitlementId] !== undefined;
    },
    [customerInfo]
  );

  /**
   * Check grace period status
   */
  const gracePeriod = useMemo(() => {
    return isInGracePeriod(customerInfo, DEFAULT_ENTITLEMENT_ID);
  }, [customerInfo]);

  /**
   * Format expiration date
   */
  const expirationDateString = useMemo(() => {
    return formatExpirationDate(subscriptionStatus.expirationDate);
  }, [subscriptionStatus.expirationDate]);

  /**
   * Calculate time remaining
   */
  const timeRemaining = useMemo(() => {
    return formatTimeRemaining(subscriptionStatus.expirationDate);
  }, [subscriptionStatus.expirationDate]);

  return {
    isLoading: !isInitialized,
    isSubscribed: subscriptionStatus.isActive,
    isInTrial: subscriptionStatus.isInTrial,
    willRenew: subscriptionStatus.willRenew,
    expirationDate: subscriptionStatus.expirationDate,
    expirationDateString,
    timeRemaining,
    periodType: subscriptionStatus.periodType,
    activeProductId: subscriptionStatus.activeProductId,
    status: subscriptionStatus,
    isInGracePeriod: gracePeriod,
    hasEntitlement,
    refresh: refreshCustomerInfo,
  };
}

/**
 * Simplified hook for premium gate checks
 *
 * @returns Whether user has premium access
 *
 * @example
 * ```tsx
 * function PremiumFeature() {
 *   const isPremium = usePremiumStatus();
 *
 *   if (!isPremium) {
 *     return <LockedFeature />;
 *   }
 *
 *   return <FeatureContent />;
 * }
 * ```
 */
export function usePremiumStatus(): boolean {
  const { isSubscribed, isLoading } = useSubscription();
  // Return false while loading to prevent flash of premium content
  return !isLoading && isSubscribed;
}

/**
 * Hook for trial-specific information
 *
 * @returns Trial status and details
 *
 * @example
 * ```tsx
 * function TrialBanner() {
 *   const { isInTrial, daysRemaining, trialEndDate } = useTrialStatus();
 *
 *   if (!isInTrial) return null;
 *
 *   return (
 *     <Banner>
 *       Your trial ends in {daysRemaining} days ({trialEndDate})
 *     </Banner>
 *   );
 * }
 * ```
 */
export interface UseTrialStatusReturn {
  /** Whether user is currently in trial */
  isInTrial: boolean;
  /** Days remaining in trial */
  daysRemaining: number;
  /** Hours remaining (useful for last day) */
  hoursRemaining: number;
  /** Formatted trial end date */
  trialEndDate: string;
  /** Whether trial is expiring soon (within 2 days) */
  isExpiringSoon: boolean;
}

export function useTrialStatus(): UseTrialStatusReturn {
  const { isInTrial, expirationDate, expirationDateString } = useSubscription();

  const { daysRemaining, hoursRemaining, isExpiringSoon } = useMemo(() => {
    if (!expirationDate) {
      return { daysRemaining: 0, hoursRemaining: 0, isExpiringSoon: false };
    }

    const now = new Date();
    const diffMs = expirationDate.getTime() - now.getTime();

    if (diffMs <= 0) {
      return { daysRemaining: 0, hoursRemaining: 0, isExpiringSoon: true };
    }

    const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    const hours = Math.floor(diffMs / (1000 * 60 * 60));

    return {
      daysRemaining: days,
      hoursRemaining: hours,
      isExpiringSoon: days <= 2,
    };
  }, [expirationDate]);

  return {
    isInTrial,
    daysRemaining,
    hoursRemaining,
    trialEndDate: expirationDateString,
    isExpiringSoon: isInTrial && isExpiringSoon,
  };
}

/**
 * Hook for subscription management info
 *
 * @returns Management URLs and cancel status
 *
 * @example
 * ```tsx
 * function ManageSubscription() {
 *   const { managementUrl, canCancel, willRenew } = useSubscriptionManagement();
 *
 *   return (
 *     <View>
 *       {managementUrl && (
 *         <Button onPress={() => Linking.openURL(managementUrl)}>
 *           Manage Subscription
 *         </Button>
 *       )}
 *       {willRenew && canCancel && (
 *         <Text>Your subscription will renew automatically</Text>
 *       )}
 *       {!willRenew && (
 *         <Text>Your subscription will not renew</Text>
 *       )}
 *     </View>
 *   );
 * }
 * ```
 */
export interface UseSubscriptionManagementReturn {
  /** URL to manage subscription (App Store/Play Store) */
  managementUrl: string | null;
  /** Whether subscription will auto-renew */
  willRenew: boolean;
  /** Whether user can cancel (has active subscription) */
  canCancel: boolean;
  /** Whether user is in grace period due to billing issue */
  hasBillingIssue: boolean;
  /** Product identifier */
  productId: string | null;
  /** Store where purchase was made */
  store: 'app_store' | 'play_store' | 'stripe' | null;
}

export function useSubscriptionManagement(): UseSubscriptionManagementReturn {
  const { customerInfo, subscriptionStatus } = useRevenueCat();

  const managementInfo = useMemo(() => {
    if (!customerInfo) {
      return {
        managementUrl: null,
        store: null,
      };
    }

    return {
      managementUrl: customerInfo.managementURL || null,
      store: null, // Would need to parse from entitlement info
    };
  }, [customerInfo]);

  const hasBillingIssue = useMemo(() => {
    return isInGracePeriod(customerInfo, DEFAULT_ENTITLEMENT_ID);
  }, [customerInfo]);

  return {
    managementUrl: managementInfo.managementUrl,
    willRenew: subscriptionStatus.willRenew,
    canCancel: subscriptionStatus.isActive && subscriptionStatus.willRenew,
    hasBillingIssue,
    productId: subscriptionStatus.activeProductId,
    store: managementInfo.store,
  };
}

/**
 * Hook to check specific feature access
 *
 * Use this for feature flagging based on subscription tier.
 *
 * @param featureKey - Feature identifier
 * @param requiredEntitlement - Required entitlement for access
 * @returns Whether feature is accessible
 *
 * @example
 * ```tsx
 * function AdvancedFeature() {
 *   const hasAccess = useFeatureAccess('advanced_analytics', 'premium');
 *
 *   if (!hasAccess) {
 *     return <UpgradePrompt feature="Advanced Analytics" />;
 *   }
 *
 *   return <AnalyticsDashboard />;
 * }
 * ```
 */
export function useFeatureAccess(
  featureKey: string,
  requiredEntitlement: EntitlementId = 'premium'
): boolean {
  const { hasEntitlement, isLoading } = useSubscription();

  if (isLoading) {
    return false;
  }

  return hasEntitlement(requiredEntitlement);
}

export default useSubscription;
