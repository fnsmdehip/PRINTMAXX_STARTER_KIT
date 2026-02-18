/**
 * usePurchase Hook
 * Handle purchases, restores, and package management
 */

import { useState, useCallback, useMemo } from 'react';
import Purchases, {
  PurchasesPackage,
  PurchasesOffering,
  PURCHASES_ERROR_CODE,
} from 'react-native-purchases';
import { useRevenueCat } from './RevenueCatProvider';
import type {
  PurchaseResult,
  RestoreResult,
  PackageDisplayInfo,
  PurchaseErrorCode,
} from './types';
import {
  packageToDisplayInfo,
  sortPackagesByValue,
  withTimeout,
} from './utils';
import { TIMEOUTS, FEATURE_FLAGS, DEFAULT_ENTITLEMENT_ID } from './config';

/**
 * Purchase hook return type
 */
export interface UsePurchaseReturn {
  /** Available packages from current offering */
  packages: PackageDisplayInfo[];
  /** Monthly package if available */
  monthlyPackage: PackageDisplayInfo | null;
  /** Annual package if available */
  annualPackage: PackageDisplayInfo | null;
  /** Lifetime package if available */
  lifetimePackage: PackageDisplayInfo | null;
  /** Whether offerings are loading */
  isLoadingPackages: boolean;
  /** Error loading packages */
  packagesError: string | null;
  /** Purchase a package */
  purchasePackage: (pkg: PurchasesPackage) => Promise<PurchaseResult>;
  /** Purchase by package identifier */
  purchaseByIdentifier: (identifier: string) => Promise<PurchaseResult>;
  /** Restore previous purchases */
  restorePurchases: () => Promise<RestoreResult>;
  /** Whether a purchase is in progress */
  isPurchasing: boolean;
  /** Whether a restore is in progress */
  isRestoring: boolean;
  /** Refresh available packages */
  refreshPackages: () => Promise<void>;
}

/**
 * Map RevenueCat error codes to our error codes
 */
function mapErrorCode(error: any): PurchaseErrorCode {
  const code = error?.code;

  switch (code) {
    case PURCHASES_ERROR_CODE.PURCHASE_CANCELLED_ERROR:
      return 'user_cancelled' as PurchaseErrorCode;
    case PURCHASES_ERROR_CODE.PAYMENT_PENDING_ERROR:
      return 'payment_pending' as PurchaseErrorCode;
    case PURCHASES_ERROR_CODE.INVALID_RECEIPT_ERROR:
      return 'receipt_invalid' as PurchaseErrorCode;
    case PURCHASES_ERROR_CODE.NETWORK_ERROR:
      return 'network_error' as PurchaseErrorCode;
    case PURCHASES_ERROR_CODE.PRODUCT_NOT_AVAILABLE_FOR_PURCHASE_ERROR:
      return 'product_not_available' as PurchaseErrorCode;
    case PURCHASES_ERROR_CODE.PURCHASE_NOT_ALLOWED_ERROR:
      return 'purchase_not_allowed' as PurchaseErrorCode;
    case PURCHASES_ERROR_CODE.PRODUCT_ALREADY_PURCHASED_ERROR:
      return 'already_purchased' as PurchaseErrorCode;
    case PURCHASES_ERROR_CODE.STORE_PROBLEM_ERROR:
      return 'store_problem' as PurchaseErrorCode;
    default:
      return 'unknown' as PurchaseErrorCode;
  }
}

/**
 * Get user-friendly error message
 */
function getErrorMessage(errorCode: PurchaseErrorCode): string {
  switch (errorCode) {
    case 'user_cancelled':
      return 'Purchase was cancelled.';
    case 'payment_pending':
      return 'Payment is pending. Please wait for confirmation.';
    case 'receipt_invalid':
      return 'Could not verify purchase. Please try again.';
    case 'network_error':
      return 'Network error. Please check your connection and try again.';
    case 'product_not_available':
      return 'This product is not available for purchase.';
    case 'purchase_not_allowed':
      return 'Purchases are not allowed on this device.';
    case 'already_purchased':
      return 'You already own this product. Try restoring purchases.';
    case 'store_problem':
      return 'There was a problem with the App Store. Please try again later.';
    default:
      return 'An error occurred. Please try again.';
  }
}

/**
 * Hook for purchasing subscriptions
 *
 * @returns Purchase utilities and package information
 *
 * @example
 * ```tsx
 * function PaywallScreen() {
 *   const {
 *     packages,
 *     annualPackage,
 *     monthlyPackage,
 *     purchasePackage,
 *     isPurchasing,
 *     restorePurchases,
 *     isRestoring,
 *   } = usePurchase();
 *
 *   const handlePurchase = async (pkg: PurchasesPackage) => {
 *     const result = await purchasePackage(pkg);
 *     if (result.success) {
 *       // Navigate to success screen or close paywall
 *     } else if (!result.userCancelled) {
 *       Alert.alert('Error', result.error);
 *     }
 *   };
 *
 *   return (
 *     <View>
 *       {packages.map((pkg) => (
 *         <PackageButton
 *           key={pkg.identifier}
 *           package={pkg}
 *           onPress={() => handlePurchase(pkg.package)}
 *           disabled={isPurchasing}
 *         />
 *       ))}
 *       <Button
 *         title="Restore Purchases"
 *         onPress={restorePurchases}
 *         disabled={isRestoring}
 *       />
 *     </View>
 *   );
 * }
 * ```
 */
export function usePurchase(): UsePurchaseReturn {
  const {
    offerings,
    refreshOfferings,
    refreshCustomerInfo,
  } = useRevenueCat();

  const [isPurchasing, setIsPurchasing] = useState(false);
  const [isRestoring, setIsRestoring] = useState(false);

  /**
   * Convert packages to display info
   */
  const packages = useMemo<PackageDisplayInfo[]>(() => {
    if (!offerings.current?.availablePackages) {
      return [];
    }

    const sortedPackages = sortPackagesByValue(
      offerings.current.availablePackages
    );

    // Find monthly price for savings calculation
    const monthlyPkg = sortedPackages.find(
      (p) => p.packageType === 'MONTHLY' || p.identifier === '$rc_monthly'
    );
    const monthlyPrice = monthlyPkg?.product.price;

    // Mark annual as recommended by default
    return sortedPackages.map((pkg) => {
      const isAnnual =
        pkg.packageType === 'ANNUAL' || pkg.identifier === '$rc_annual';
      return packageToDisplayInfo(pkg, monthlyPrice, isAnnual);
    });
  }, [offerings.current]);

  /**
   * Get specific package types
   */
  const monthlyPackage = useMemo(() => {
    return packages.find((p) => p.title === 'Monthly') || null;
  }, [packages]);

  const annualPackage = useMemo(() => {
    return packages.find((p) => p.title === 'Annual') || null;
  }, [packages]);

  const lifetimePackage = useMemo(() => {
    return packages.find((p) => p.title === 'Lifetime') || null;
  }, [packages]);

  /**
   * Purchase a package
   */
  const purchasePackage = useCallback(
    async (pkg: PurchasesPackage): Promise<PurchaseResult> => {
      if (isPurchasing) {
        return {
          success: false,
          error: 'A purchase is already in progress.',
          userCancelled: false,
        };
      }

      setIsPurchasing(true);

      try {
        if (FEATURE_FLAGS.enableDebugLogs) {
          console.log('[RevenueCat] Starting purchase:', pkg.identifier);
        }

        const { customerInfo } = await withTimeout(
          Purchases.purchasePackage(pkg),
          TIMEOUTS.purchase,
          'Purchase'
        );

        // Check if entitlement is now active
        const isActive =
          customerInfo.entitlements.active[DEFAULT_ENTITLEMENT_ID] !== undefined;

        if (FEATURE_FLAGS.enableDebugLogs) {
          console.log('[RevenueCat] Purchase result:', {
            isActive,
            package: pkg.identifier,
          });
        }

        return {
          success: isActive,
          userCancelled: false,
          customerInfo,
        };
      } catch (error: any) {
        const errorCode = mapErrorCode(error);
        const userCancelled = errorCode === 'user_cancelled';

        if (FEATURE_FLAGS.enableDebugLogs && !userCancelled) {
          console.error('[RevenueCat] Purchase error:', error);
        }

        return {
          success: false,
          error: getErrorMessage(errorCode),
          errorCode,
          userCancelled,
        };
      } finally {
        setIsPurchasing(false);
      }
    },
    [isPurchasing]
  );

  /**
   * Purchase by identifier
   */
  const purchaseByIdentifier = useCallback(
    async (identifier: string): Promise<PurchaseResult> => {
      const pkg = offerings.current?.availablePackages.find(
        (p) => p.identifier === identifier
      );

      if (!pkg) {
        return {
          success: false,
          error: `Package not found: ${identifier}`,
          userCancelled: false,
        };
      }

      return purchasePackage(pkg);
    },
    [offerings.current, purchasePackage]
  );

  /**
   * Restore purchases
   */
  const restorePurchases = useCallback(async (): Promise<RestoreResult> => {
    if (isRestoring) {
      return {
        success: false,
        purchasesRestored: false,
        error: 'A restore is already in progress.',
      };
    }

    setIsRestoring(true);

    try {
      if (FEATURE_FLAGS.enableDebugLogs) {
        console.log('[RevenueCat] Starting restore...');
      }

      const customerInfo = await withTimeout(
        Purchases.restorePurchases(),
        TIMEOUTS.restore,
        'Restore purchases'
      );

      const hasActiveEntitlement =
        customerInfo.entitlements.active[DEFAULT_ENTITLEMENT_ID] !== undefined;

      if (FEATURE_FLAGS.enableDebugLogs) {
        console.log('[RevenueCat] Restore result:', {
          hasActiveEntitlement,
          entitlements: Object.keys(customerInfo.entitlements.active),
        });
      }

      return {
        success: true,
        purchasesRestored: hasActiveEntitlement,
        customerInfo,
      };
    } catch (error: any) {
      const errorMessage =
        error instanceof Error ? error.message : 'Failed to restore purchases.';

      if (FEATURE_FLAGS.enableDebugLogs) {
        console.error('[RevenueCat] Restore error:', error);
      }

      return {
        success: false,
        purchasesRestored: false,
        error: errorMessage,
      };
    } finally {
      setIsRestoring(false);
    }
  }, [isRestoring]);

  return {
    packages,
    monthlyPackage,
    annualPackage,
    lifetimePackage,
    isLoadingPackages: offerings.isLoading,
    packagesError: offerings.error,
    purchasePackage,
    purchaseByIdentifier,
    restorePurchases,
    isPurchasing,
    isRestoring,
    refreshPackages: refreshOfferings,
  };
}

/**
 * Hook for just restoring purchases
 *
 * @example
 * ```tsx
 * function SettingsScreen() {
 *   const { restore, isRestoring, result } = useRestorePurchases();
 *
 *   return (
 *     <Button
 *       title={isRestoring ? 'Restoring...' : 'Restore Purchases'}
 *       onPress={restore}
 *       disabled={isRestoring}
 *     />
 *   );
 * }
 * ```
 */
export interface UseRestorePurchasesReturn {
  /** Trigger restore */
  restore: () => Promise<RestoreResult>;
  /** Whether restore is in progress */
  isRestoring: boolean;
  /** Last restore result */
  result: RestoreResult | null;
}

export function useRestorePurchases(): UseRestorePurchasesReturn {
  const { restorePurchases, isRestoring } = usePurchase();
  const [result, setResult] = useState<RestoreResult | null>(null);

  const restore = useCallback(async (): Promise<RestoreResult> => {
    const restoreResult = await restorePurchases();
    setResult(restoreResult);
    return restoreResult;
  }, [restorePurchases]);

  return {
    restore,
    isRestoring,
    result,
  };
}

/**
 * Hook for promotional offers
 *
 * Note: Promotional offers require additional setup in App Store Connect
 * and RevenueCat dashboard.
 *
 * @param offerId - Promotional offer identifier
 * @returns Promotional offer utilities
 */
export interface UsePromotionalOfferReturn {
  /** Whether promo offer is available */
  isAvailable: boolean;
  /** Discounted price string */
  discountedPrice: string | null;
  /** Apply promotional offer */
  applyOffer: () => Promise<PurchaseResult>;
  /** Loading state */
  isLoading: boolean;
}

export function usePromotionalOffer(
  offerId: string
): UsePromotionalOfferReturn {
  // Promotional offers require more complex setup
  // This is a placeholder for future implementation
  return {
    isAvailable: false,
    discountedPrice: null,
    applyOffer: async () => ({
      success: false,
      error: 'Promotional offers not configured.',
      userCancelled: false,
    }),
    isLoading: false,
  };
}

/**
 * Hook for checking purchase eligibility
 *
 * @param productId - Product identifier to check
 * @returns Eligibility status
 */
export interface UsePurchaseEligibilityReturn {
  /** Whether user can purchase this product */
  canPurchase: boolean;
  /** Reason if cannot purchase */
  reason: string | null;
  /** Whether eligibility is being checked */
  isChecking: boolean;
}

export function usePurchaseEligibility(
  productId: string
): UsePurchaseEligibilityReturn {
  const { packages, isLoadingPackages } = usePurchase();
  const { subscriptionStatus } = useRevenueCat();

  const eligibility = useMemo(() => {
    // Already subscribed to this product
    if (subscriptionStatus.activeProductId === productId) {
      return {
        canPurchase: false,
        reason: 'You are already subscribed to this product.',
      };
    }

    // Product not available
    const isProductAvailable = packages.some(
      (p) => p.package.product.identifier === productId
    );
    if (!isProductAvailable && !isLoadingPackages) {
      return {
        canPurchase: false,
        reason: 'This product is not available.',
      };
    }

    return {
      canPurchase: true,
      reason: null,
    };
  }, [productId, packages, subscriptionStatus, isLoadingPackages]);

  return {
    ...eligibility,
    isChecking: isLoadingPackages,
  };
}

export default usePurchase;
