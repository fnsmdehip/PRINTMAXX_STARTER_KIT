/**
 * Mock implementation of react-native-purchases (RevenueCat)
 *
 * Usage in tests:
 *   import mockRevenueCat, { setMockCustomerInfo } from '@testing/mocks/mockRevenueCat';
 *
 *   test('shows pro features for pro users', async () => {
 *     setMockCustomerInfo('pro');
 *     // ... test pro user experience
 *   });
 */

import {
  createCustomerInfo,
  createEntitlement,
  createProduct,
  PRODUCTS,
  PRODUCT_LIST,
  type CustomerInfo,
  type Product,
  type SubscriptionTier,
} from '../fixtures/subscriptionFixtures';

// ============================================================================
// Types
// ============================================================================

interface PurchaseResult {
  customerInfo: CustomerInfo;
  productIdentifier: string;
}

interface LogInResult {
  customerInfo: CustomerInfo;
  created: boolean;
}

interface OfferingsResponse {
  current: {
    identifier: string;
    serverDescription: string;
    availablePackages: Package[];
    lifetime: Package | null;
    annual: Package | null;
    sixMonth: Package | null;
    threeMonth: Package | null;
    twoMonth: Package | null;
    monthly: Package | null;
    weekly: Package | null;
  } | null;
  all: Record<string, Offering>;
}

interface Offering {
  identifier: string;
  serverDescription: string;
  availablePackages: Package[];
}

interface Package {
  identifier: string;
  packageType: string;
  product: Product;
  offeringIdentifier: string;
}

// ============================================================================
// Mock State
// ============================================================================

let mockCustomerInfo: CustomerInfo = createCustomerInfo('free');
let mockOfferings: OfferingsResponse | null = null;
let mockIsConfigured = false;
let mockAppUserId = 'anonymous';

// ============================================================================
// Mock Configuration
// ============================================================================

/**
 * Set the mock customer info for testing different subscription states
 */
export function setMockCustomerInfo(tier: SubscriptionTier): void {
  mockCustomerInfo = createCustomerInfo(tier);
}

/**
 * Set a custom customer info object
 */
export function setCustomCustomerInfo(customerInfo: CustomerInfo): void {
  mockCustomerInfo = customerInfo;
}

/**
 * Reset to default (free) state
 */
export function resetMockRevenueCat(): void {
  mockCustomerInfo = createCustomerInfo('free');
  mockOfferings = null;
  mockIsConfigured = false;
  mockAppUserId = 'anonymous';
}

/**
 * Simulate a purchase error
 */
let purchaseError: Error | null = null;
export function simulatePurchaseError(error: Error | null): void {
  purchaseError = error;
}

/**
 * Simulate offerings fetch error
 */
let offeringsError: Error | null = null;
export function simulateOfferingsError(error: Error | null): void {
  offeringsError = error;
}

// ============================================================================
// Mock Implementation
// ============================================================================

const createMockOfferings = (): OfferingsResponse => {
  const proMonthlyPackage: Package = {
    identifier: '$rc_monthly',
    packageType: 'MONTHLY',
    product: PRODUCTS.proMonthly,
    offeringIdentifier: 'default',
  };

  const proYearlyPackage: Package = {
    identifier: '$rc_annual',
    packageType: 'ANNUAL',
    product: PRODUCTS.proYearly,
    offeringIdentifier: 'default',
  };

  const premiumMonthlyPackage: Package = {
    identifier: 'premium_monthly',
    packageType: 'MONTHLY',
    product: PRODUCTS.premiumMonthly,
    offeringIdentifier: 'premium',
  };

  const premiumYearlyPackage: Package = {
    identifier: 'premium_annual',
    packageType: 'ANNUAL',
    product: PRODUCTS.premiumYearly,
    offeringIdentifier: 'premium',
  };

  const defaultOffering: Offering = {
    identifier: 'default',
    serverDescription: 'Default offering with pro plans',
    availablePackages: [proMonthlyPackage, proYearlyPackage],
  };

  const premiumOffering: Offering = {
    identifier: 'premium',
    serverDescription: 'Premium offering',
    availablePackages: [premiumMonthlyPackage, premiumYearlyPackage],
  };

  return {
    current: {
      ...defaultOffering,
      lifetime: null,
      annual: proYearlyPackage,
      sixMonth: null,
      threeMonth: null,
      twoMonth: null,
      monthly: proMonthlyPackage,
      weekly: null,
    },
    all: {
      default: defaultOffering,
      premium: premiumOffering,
    },
  };
};

const mockPurchases = {
  // Configuration
  configure: jest.fn(async (options: { apiKey: string; appUserID?: string }): Promise<void> => {
    mockIsConfigured = true;
    if (options.appUserID) {
      mockAppUserId = options.appUserID;
    }
  }),

  setDebugLogsEnabled: jest.fn(async (enabled: boolean): Promise<void> => {
    // No-op in mock
  }),

  setLogLevel: jest.fn((level: string): void => {
    // No-op in mock
  }),

  isConfigured: jest.fn((): boolean => mockIsConfigured),

  // User identification
  logIn: jest.fn(async (appUserID: string): Promise<LogInResult> => {
    mockAppUserId = appUserID;
    return {
      customerInfo: mockCustomerInfo,
      created: false,
    };
  }),

  logOut: jest.fn(async (): Promise<CustomerInfo> => {
    mockAppUserId = 'anonymous';
    mockCustomerInfo = createCustomerInfo('free');
    return mockCustomerInfo;
  }),

  getAppUserID: jest.fn(async (): Promise<string> => mockAppUserId),

  isAnonymous: jest.fn(async (): Promise<boolean> => mockAppUserId === 'anonymous'),

  // Customer info
  getCustomerInfo: jest.fn(async (): Promise<CustomerInfo> => mockCustomerInfo),

  // Offerings and products
  getOfferings: jest.fn(async (): Promise<OfferingsResponse> => {
    if (offeringsError) {
      const error = offeringsError;
      offeringsError = null;
      throw error;
    }
    if (!mockOfferings) {
      mockOfferings = createMockOfferings();
    }
    return mockOfferings;
  }),

  getProducts: jest.fn(
    async (productIdentifiers: string[]): Promise<Product[]> => {
      return PRODUCT_LIST.filter((p) => productIdentifiers.includes(p.identifier));
    }
  ),

  // Purchasing
  purchasePackage: jest.fn(
    async (packageToPurchase: Package): Promise<PurchaseResult> => {
      if (purchaseError) {
        const error = purchaseError;
        purchaseError = null;
        throw error;
      }

      // Simulate successful purchase by updating customer info
      const tier = packageToPurchase.product.tier;
      mockCustomerInfo = createCustomerInfo(tier);

      return {
        customerInfo: mockCustomerInfo,
        productIdentifier: packageToPurchase.product.identifier,
      };
    }
  ),

  purchaseProduct: jest.fn(
    async (productIdentifier: string): Promise<PurchaseResult> => {
      if (purchaseError) {
        const error = purchaseError;
        purchaseError = null;
        throw error;
      }

      const product = PRODUCT_LIST.find((p) => p.identifier === productIdentifier);
      if (!product) {
        throw new Error(`Product not found: ${productIdentifier}`);
      }

      mockCustomerInfo = createCustomerInfo(product.tier);

      return {
        customerInfo: mockCustomerInfo,
        productIdentifier,
      };
    }
  ),

  // Restore purchases
  restorePurchases: jest.fn(async (): Promise<CustomerInfo> => {
    // Return current customer info (no change in mock)
    return mockCustomerInfo;
  }),

  // Syncing
  syncPurchases: jest.fn(async (): Promise<CustomerInfo> => mockCustomerInfo),

  // Subscription management
  getManagementURL: jest.fn(
    async (): Promise<string | null> => 'https://apps.apple.com/account/subscriptions'
  ),

  // Promo offers
  checkTrialOrIntroductoryPriceEligibility: jest.fn(
    async (productIdentifiers: string[]): Promise<Record<string, { status: string }>> => {
      const result: Record<string, { status: string }> = {};
      productIdentifiers.forEach((id) => {
        result[id] = { status: 'ELIGIBLE' };
      });
      return result;
    }
  ),

  // Event listeners
  addCustomerInfoUpdateListener: jest.fn(
    (listener: (customerInfo: CustomerInfo) => void): (() => void) => {
      // Return unsubscribe function
      return () => {};
    }
  ),

  // Attributes
  setAttributes: jest.fn(async (attributes: Record<string, string>): Promise<void> => {}),
  setEmail: jest.fn(async (email: string): Promise<void> => {}),
  setPhoneNumber: jest.fn(async (phoneNumber: string): Promise<void> => {}),
  setDisplayName: jest.fn(async (displayName: string): Promise<void> => {}),
  setPushToken: jest.fn(async (pushToken: string): Promise<void> => {}),

  // Constants
  PURCHASES_ERROR_CODE: {
    UNKNOWN_ERROR: 0,
    PURCHASE_CANCELLED_ERROR: 1,
    STORE_PROBLEM_ERROR: 2,
    PURCHASE_NOT_ALLOWED_ERROR: 3,
    PURCHASE_INVALID_ERROR: 4,
    PRODUCT_NOT_AVAILABLE_FOR_PURCHASE_ERROR: 5,
    PRODUCT_ALREADY_PURCHASED_ERROR: 6,
    RECEIPT_ALREADY_IN_USE_ERROR: 7,
    INVALID_RECEIPT_ERROR: 8,
    MISSING_RECEIPT_FILE_ERROR: 9,
    NETWORK_ERROR: 10,
    INVALID_CREDENTIALS_ERROR: 11,
    UNEXPECTED_BACKEND_RESPONSE_ERROR: 12,
    INVALID_APP_USER_ID_ERROR: 14,
    OPERATION_ALREADY_IN_PROGRESS_ERROR: 15,
    UNKNOWN_BACKEND_ERROR: 16,
    CONFIGURATION_ERROR: 24,
  },

  PACKAGE_TYPE: {
    UNKNOWN: 'UNKNOWN',
    CUSTOM: 'CUSTOM',
    LIFETIME: 'LIFETIME',
    ANNUAL: 'ANNUAL',
    SIX_MONTH: 'SIX_MONTH',
    THREE_MONTH: 'THREE_MONTH',
    TWO_MONTH: 'TWO_MONTH',
    MONTHLY: 'MONTHLY',
    WEEKLY: 'WEEKLY',
  },

  INTRO_ELIGIBILITY_STATUS: {
    INTRO_ELIGIBILITY_STATUS_UNKNOWN: 0,
    INTRO_ELIGIBILITY_STATUS_INELIGIBLE: 1,
    INTRO_ELIGIBILITY_STATUS_ELIGIBLE: 2,
  },
};

export default mockPurchases;

// ============================================================================
// Error Helpers
// ============================================================================

export class PurchasesError extends Error {
  code: number;
  underlyingErrorMessage: string;

  constructor(code: number, message: string) {
    super(message);
    this.name = 'PurchasesError';
    this.code = code;
    this.underlyingErrorMessage = message;
  }
}

export function createPurchaseCancelledError(): PurchasesError {
  return new PurchasesError(1, 'Purchase was cancelled');
}

export function createNetworkError(): PurchasesError {
  return new PurchasesError(10, 'Network error occurred');
}

export function createProductNotFoundError(): PurchasesError {
  return new PurchasesError(5, 'Product not available for purchase');
}

export function createAlreadyPurchasedError(): PurchasesError {
  return new PurchasesError(6, 'Product already purchased');
}
