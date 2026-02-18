/**
 * Subscription test fixtures and factory functions
 *
 * Usage:
 *   import { createSubscription, SUBSCRIPTIONS, PRODUCTS } from '@testing/fixtures/subscriptionFixtures';
 */

// ============================================================================
// Types
// ============================================================================

export type SubscriptionTier = 'free' | 'pro' | 'premium';
export type SubscriptionPeriod = 'monthly' | 'yearly' | 'lifetime';
export type SubscriptionStatus = 'active' | 'expired' | 'cancelled' | 'paused' | 'trial';

export interface Subscription {
  id: string;
  userId: string;
  tier: SubscriptionTier;
  status: SubscriptionStatus;
  period: SubscriptionPeriod | null;
  productId: string | null;
  startedAt: Date;
  expiresAt: Date | null;
  cancelledAt: Date | null;
  trialEndsAt: Date | null;
  autoRenew: boolean;
  originalTransactionId: string | null;
  platform: 'ios' | 'android' | 'web';
}

export interface Product {
  id: string;
  identifier: string;
  title: string;
  description: string;
  priceString: string;
  price: number;
  currencyCode: string;
  period: SubscriptionPeriod;
  tier: SubscriptionTier;
  introPrice: number | null;
  introPriceString: string | null;
  introPeriodDays: number | null;
}

export interface PurchaseResult {
  productId: string;
  transactionId: string;
  purchaseDate: Date;
  expirationDate: Date | null;
}

export interface Entitlement {
  identifier: string;
  isActive: boolean;
  willRenew: boolean;
  periodType: 'normal' | 'trial' | 'intro';
  latestPurchaseDate: Date;
  originalPurchaseDate: Date;
  expirationDate: Date | null;
  store: 'app_store' | 'play_store' | 'stripe';
  productIdentifier: string;
  isSandbox: boolean;
}

// ============================================================================
// Constants
// ============================================================================

export const SUBSCRIPTION_TIERS: Record<SubscriptionTier, { name: string; features: string[] }> = {
  free: {
    name: 'Free',
    features: ['Basic features', 'Limited usage', 'Community support'],
  },
  pro: {
    name: 'Pro',
    features: ['All free features', 'Unlimited usage', 'Priority support', 'Analytics'],
  },
  premium: {
    name: 'Premium',
    features: ['All pro features', 'API access', 'White label', 'Dedicated support'],
  },
};

// ============================================================================
// Factory Functions
// ============================================================================

let subscriptionIdCounter = 1;

/**
 * Create a subscription with custom overrides
 */
export function createSubscription(overrides: Partial<Subscription> = {}): Subscription {
  const id = overrides.id ?? `sub_${subscriptionIdCounter++}`;
  const now = new Date();
  const thirtyDaysFromNow = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000);

  return {
    id,
    userId: 'user_1',
    tier: 'free',
    status: 'active',
    period: null,
    productId: null,
    startedAt: now,
    expiresAt: null,
    cancelledAt: null,
    trialEndsAt: null,
    autoRenew: false,
    originalTransactionId: null,
    platform: 'ios',
    ...overrides,
  };
}

/**
 * Create an active pro subscription
 */
export function createProSubscription(overrides: Partial<Subscription> = {}): Subscription {
  const now = new Date();
  const thirtyDaysFromNow = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000);

  return createSubscription({
    tier: 'pro',
    status: 'active',
    period: 'monthly',
    productId: 'com.app.pro_monthly',
    expiresAt: thirtyDaysFromNow,
    autoRenew: true,
    originalTransactionId: `txn_${Date.now()}`,
    ...overrides,
  });
}

/**
 * Create an active premium subscription
 */
export function createPremiumSubscription(overrides: Partial<Subscription> = {}): Subscription {
  const now = new Date();
  const yearFromNow = new Date(now.getTime() + 365 * 24 * 60 * 60 * 1000);

  return createSubscription({
    tier: 'premium',
    status: 'active',
    period: 'yearly',
    productId: 'com.app.premium_yearly',
    expiresAt: yearFromNow,
    autoRenew: true,
    originalTransactionId: `txn_${Date.now()}`,
    ...overrides,
  });
}

/**
 * Create a trial subscription
 */
export function createTrialSubscription(
  daysRemaining: number = 7,
  overrides: Partial<Subscription> = {}
): Subscription {
  const now = new Date();
  const trialEnd = new Date(now.getTime() + daysRemaining * 24 * 60 * 60 * 1000);

  return createSubscription({
    tier: 'pro',
    status: 'trial',
    period: 'monthly',
    productId: 'com.app.pro_monthly',
    trialEndsAt: trialEnd,
    expiresAt: trialEnd,
    autoRenew: true,
    ...overrides,
  });
}

/**
 * Create an expired subscription
 */
export function createExpiredSubscription(overrides: Partial<Subscription> = {}): Subscription {
  const now = new Date();
  const thirtyDaysAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
  const dayAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000);

  return createSubscription({
    tier: 'pro',
    status: 'expired',
    period: 'monthly',
    productId: 'com.app.pro_monthly',
    startedAt: thirtyDaysAgo,
    expiresAt: dayAgo,
    autoRenew: false,
    ...overrides,
  });
}

/**
 * Create a cancelled subscription (still active until expiry)
 */
export function createCancelledSubscription(overrides: Partial<Subscription> = {}): Subscription {
  const now = new Date();
  const fifteenDaysFromNow = new Date(now.getTime() + 15 * 24 * 60 * 60 * 1000);

  return createSubscription({
    tier: 'pro',
    status: 'cancelled',
    period: 'monthly',
    productId: 'com.app.pro_monthly',
    expiresAt: fifteenDaysFromNow,
    cancelledAt: now,
    autoRenew: false,
    ...overrides,
  });
}

/**
 * Create a product
 */
export function createProduct(overrides: Partial<Product> = {}): Product {
  return {
    id: 'prod_1',
    identifier: 'com.app.pro_monthly',
    title: 'Pro Monthly',
    description: 'Unlock all pro features with monthly billing',
    priceString: '$9.99',
    price: 9.99,
    currencyCode: 'USD',
    period: 'monthly',
    tier: 'pro',
    introPrice: null,
    introPriceString: null,
    introPeriodDays: null,
    ...overrides,
  };
}

/**
 * Create an entitlement
 */
export function createEntitlement(overrides: Partial<Entitlement> = {}): Entitlement {
  const now = new Date();
  const thirtyDaysFromNow = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000);

  return {
    identifier: 'pro',
    isActive: true,
    willRenew: true,
    periodType: 'normal',
    latestPurchaseDate: now,
    originalPurchaseDate: now,
    expirationDate: thirtyDaysFromNow,
    store: 'app_store',
    productIdentifier: 'com.app.pro_monthly',
    isSandbox: true,
    ...overrides,
  };
}

// ============================================================================
// Static Fixtures
// ============================================================================

export const SUBSCRIPTIONS = {
  free: createSubscription({ tier: 'free' }),
  pro: createProSubscription(),
  premium: createPremiumSubscription(),
  trial: createTrialSubscription(),
  expired: createExpiredSubscription(),
  cancelled: createCancelledSubscription(),
  proYearly: createProSubscription({ period: 'yearly', productId: 'com.app.pro_yearly' }),
  premiumLifetime: createPremiumSubscription({
    period: 'lifetime',
    productId: 'com.app.premium_lifetime',
    expiresAt: null,
  }),
} as const;

export const PRODUCTS: Record<string, Product> = {
  proMonthly: createProduct({
    id: 'prod_pro_monthly',
    identifier: 'com.app.pro_monthly',
    title: 'Pro Monthly',
    priceString: '$9.99',
    price: 9.99,
    period: 'monthly',
    tier: 'pro',
  }),
  proYearly: createProduct({
    id: 'prod_pro_yearly',
    identifier: 'com.app.pro_yearly',
    title: 'Pro Yearly',
    description: 'Unlock all pro features with annual billing. Save 40%!',
    priceString: '$71.99',
    price: 71.99,
    period: 'yearly',
    tier: 'pro',
  }),
  premiumMonthly: createProduct({
    id: 'prod_premium_monthly',
    identifier: 'com.app.premium_monthly',
    title: 'Premium Monthly',
    priceString: '$19.99',
    price: 19.99,
    period: 'monthly',
    tier: 'premium',
  }),
  premiumYearly: createProduct({
    id: 'prod_premium_yearly',
    identifier: 'com.app.premium_yearly',
    title: 'Premium Yearly',
    description: 'All premium features with annual billing. Save 40%!',
    priceString: '$143.99',
    price: 143.99,
    period: 'yearly',
    tier: 'premium',
  }),
  premiumLifetime: createProduct({
    id: 'prod_premium_lifetime',
    identifier: 'com.app.premium_lifetime',
    title: 'Premium Lifetime',
    description: 'One-time purchase. All features forever.',
    priceString: '$299.99',
    price: 299.99,
    period: 'lifetime',
    tier: 'premium',
  }),
  proWithTrial: createProduct({
    id: 'prod_pro_trial',
    identifier: 'com.app.pro_monthly_trial',
    title: 'Pro Monthly (7-day trial)',
    priceString: '$9.99',
    price: 9.99,
    period: 'monthly',
    tier: 'pro',
    introPrice: 0,
    introPriceString: 'Free',
    introPeriodDays: 7,
  }),
};

export const PRODUCT_LIST = Object.values(PRODUCTS);

// ============================================================================
// RevenueCat Response Mocks
// ============================================================================

export interface CustomerInfo {
  originalAppUserId: string;
  entitlements: {
    all: Record<string, Entitlement>;
    active: Record<string, Entitlement>;
  };
  activeSubscriptions: string[];
  allPurchasedProductIdentifiers: string[];
  firstSeen: Date;
  managementURL: string | null;
}

export function createCustomerInfo(
  tier: SubscriptionTier = 'free',
  overrides: Partial<CustomerInfo> = {}
): CustomerInfo {
  const entitlement = tier !== 'free' ? createEntitlement({ identifier: tier }) : null;

  return {
    originalAppUserId: 'user_1',
    entitlements: {
      all: entitlement ? { [tier]: entitlement } : {},
      active: entitlement?.isActive ? { [tier]: entitlement } : {},
    },
    activeSubscriptions: tier !== 'free' ? [`com.app.${tier}_monthly`] : [],
    allPurchasedProductIdentifiers: tier !== 'free' ? [`com.app.${tier}_monthly`] : [],
    firstSeen: new Date('2024-01-01'),
    managementURL: 'https://apps.apple.com/account/subscriptions',
    ...overrides,
  };
}

// ============================================================================
// Reset Counter
// ============================================================================

export function resetSubscriptionIdCounter(): void {
  subscriptionIdCounter = 1;
}
