/**
 * Price Testing Implementation
 *
 * RevenueCat integration for A/B testing pricing and offerings.
 * Use this module to manage remote pricing configuration and test assignment.
 */

import Purchases, {
  PurchasesOffering,
  PurchasesPackage,
  CustomerInfo,
} from 'react-native-purchases';

// ============================================================================
// Types
// ============================================================================

interface PricingVariant {
  id: string;
  name: string;
  monthlyPrice: number;
  annualPrice: number;
  trialDays: number;
  annualSavingsPercent: number;
}

interface ExperimentConfig {
  experimentId: string;
  variants: PricingVariant[];
  trafficAllocation: number[]; // Must sum to 100
  startDate: Date;
  endDate: Date | null;
  primaryMetric: string;
}

interface UserAssignment {
  experimentId: string;
  variantId: string;
  assignedAt: Date;
  userId: string;
}

interface PricingDisplayData {
  monthly: {
    price: string;
    pricePerMonth: string;
    productId: string;
  };
  annual: {
    price: string;
    pricePerMonth: string;
    savings: string;
    savingsPercent: number;
    productId: string;
  };
  trial: {
    days: number;
    available: boolean;
  };
}

// ============================================================================
// Configuration
// ============================================================================

const REVENUECAT_API_KEY_IOS = 'your_ios_api_key';
const REVENUECAT_API_KEY_ANDROID = 'your_android_api_key';

// Active experiments configuration
// In production, fetch this from your backend or RevenueCat
const ACTIVE_EXPERIMENTS: ExperimentConfig[] = [
  {
    experimentId: 'price_test_001',
    variants: [
      {
        id: 'control',
        name: 'Control - $7.99',
        monthlyPrice: 7.99,
        annualPrice: 47.99,
        trialDays: 7,
        annualSavingsPercent: 50,
      },
      {
        id: 'variant_a',
        name: 'Higher Price - $9.99',
        monthlyPrice: 9.99,
        annualPrice: 59.99,
        trialDays: 7,
        annualSavingsPercent: 50,
      },
      {
        id: 'variant_b',
        name: 'Lower Price - $4.99',
        monthlyPrice: 4.99,
        annualPrice: 29.99,
        trialDays: 7,
        annualSavingsPercent: 50,
      },
    ],
    trafficAllocation: [34, 33, 33],
    startDate: new Date('2025-01-01'),
    endDate: null,
    primaryMetric: 'revenue_per_user',
  },
];

// ============================================================================
// RevenueCat Initialization
// ============================================================================

export async function initializePurchases(userId: string): Promise<void> {
  const apiKey =
    Platform.OS === 'ios' ? REVENUECAT_API_KEY_IOS : REVENUECAT_API_KEY_ANDROID;

  await Purchases.configure({
    apiKey,
    appUserID: userId,
  });

  // Set user attributes for targeting
  await Purchases.setAttributes({
    $email: '', // Set if available
    experiment_group: await getExperimentAssignment(userId),
  });
}

// ============================================================================
// Experiment Assignment
// ============================================================================

/**
 * Deterministically assign a user to an experiment variant.
 * Uses consistent hashing to ensure same user always gets same variant.
 */
export function assignVariant(
  userId: string,
  experiment: ExperimentConfig
): string {
  const hash = simpleHash(`${userId}_${experiment.experimentId}`);
  const bucket = hash % 100;

  let cumulativeAllocation = 0;
  for (let i = 0; i < experiment.variants.length; i++) {
    cumulativeAllocation += experiment.trafficAllocation[i];
    if (bucket < cumulativeAllocation) {
      return experiment.variants[i].id;
    }
  }

  // Fallback to control
  return experiment.variants[0].id;
}

function simpleHash(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  return Math.abs(hash);
}

/**
 * Get experiment assignment for a user.
 * Checks active experiments and returns assignment string.
 */
export async function getExperimentAssignment(userId: string): Promise<string> {
  const assignments: string[] = [];

  for (const experiment of ACTIVE_EXPERIMENTS) {
    // Check if experiment is active
    const now = new Date();
    if (now < experiment.startDate) continue;
    if (experiment.endDate && now > experiment.endDate) continue;

    const variantId = assignVariant(userId, experiment);
    assignments.push(`${experiment.experimentId}:${variantId}`);
  }

  return assignments.join(',');
}

/**
 * Get the variant configuration for a user.
 */
export function getVariantConfig(
  userId: string,
  experimentId: string
): PricingVariant | null {
  const experiment = ACTIVE_EXPERIMENTS.find(
    (e) => e.experimentId === experimentId
  );
  if (!experiment) return null;

  const variantId = assignVariant(userId, experiment);
  return experiment.variants.find((v) => v.id === variantId) || null;
}

// ============================================================================
// RevenueCat Offerings
// ============================================================================

/**
 * Fetch the appropriate offering for a user based on their experiment assignment.
 * RevenueCat offerings should be named to match variant IDs.
 */
export async function getOffering(
  userId: string
): Promise<PurchasesOffering | null> {
  try {
    const offerings = await Purchases.getOfferings();

    // Get experiment assignment
    const assignment = await getExperimentAssignment(userId);

    // Try to get experiment-specific offering
    if (assignment) {
      const experimentOffering = offerings.all[assignment];
      if (experimentOffering) {
        return experimentOffering;
      }
    }

    // Fall back to current offering
    return offerings.current;
  } catch (error) {
    console.error('Error fetching offerings:', error);
    return null;
  }
}

/**
 * Get pricing display data from a RevenueCat offering.
 * Formats prices for display in paywall UI.
 */
export function getPricingDisplayData(
  offering: PurchasesOffering
): PricingDisplayData | null {
  const monthlyPackage = offering.monthly;
  const annualPackage = offering.annual;

  if (!monthlyPackage || !annualPackage) {
    console.warn('Missing monthly or annual package in offering');
    return null;
  }

  const monthlyPrice = monthlyPackage.product.price;
  const annualPrice = annualPackage.product.price;
  const annualMonthlyPrice = annualPrice / 12;
  const savingsPercent = Math.round(
    ((monthlyPrice * 12 - annualPrice) / (monthlyPrice * 12)) * 100
  );

  return {
    monthly: {
      price: monthlyPackage.product.priceString,
      pricePerMonth: monthlyPackage.product.priceString,
      productId: monthlyPackage.product.identifier,
    },
    annual: {
      price: annualPackage.product.priceString,
      pricePerMonth: formatPrice(annualMonthlyPrice, monthlyPackage.product.currencyCode),
      savings: formatPrice(
        monthlyPrice * 12 - annualPrice,
        monthlyPackage.product.currencyCode
      ),
      savingsPercent,
      productId: annualPackage.product.identifier,
    },
    trial: {
      days: annualPackage.product.introPrice?.periodNumberOfUnits || 0,
      available: !!annualPackage.product.introPrice,
    },
  };
}

function formatPrice(amount: number, currencyCode: string): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currencyCode,
  }).format(amount);
}

// ============================================================================
// Purchase Flow
// ============================================================================

/**
 * Initiate a purchase for a specific package.
 * Tracks the experiment variant in the purchase metadata.
 */
export async function purchasePackage(
  userId: string,
  packageToPurchase: PurchasesPackage
): Promise<{ success: boolean; customerInfo?: CustomerInfo; error?: string }> {
  try {
    // Set experiment metadata before purchase
    const assignment = await getExperimentAssignment(userId);
    await Purchases.setAttributes({
      experiment_assignment: assignment,
      purchase_initiated_at: new Date().toISOString(),
    });

    const { customerInfo } = await Purchases.purchasePackage(packageToPurchase);

    // Track successful purchase for experiment
    await trackPurchaseEvent(userId, packageToPurchase, assignment);

    return { success: true, customerInfo };
  } catch (error: any) {
    if (error.userCancelled) {
      return { success: false, error: 'cancelled' };
    }
    console.error('Purchase error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Restore purchases for a user.
 */
export async function restorePurchases(): Promise<CustomerInfo | null> {
  try {
    const customerInfo = await Purchases.restorePurchases();
    return customerInfo;
  } catch (error) {
    console.error('Restore error:', error);
    return null;
  }
}

// ============================================================================
// Analytics & Tracking
// ============================================================================

interface ExperimentEvent {
  eventType: 'view' | 'trial_start' | 'purchase' | 'conversion' | 'churn';
  userId: string;
  experimentId: string;
  variantId: string;
  timestamp: Date;
  metadata?: Record<string, any>;
}

/**
 * Track an experiment event for analysis.
 * Send to your analytics backend.
 */
export async function trackExperimentEvent(
  event: ExperimentEvent
): Promise<void> {
  // Send to your analytics service
  console.log('Experiment event:', event);

  // Example: Send to your backend
  // await fetch('/api/analytics/experiment', {
  //   method: 'POST',
  //   body: JSON.stringify(event),
  // });
}

/**
 * Track paywall view event.
 */
export async function trackPaywallView(
  userId: string,
  experimentId: string
): Promise<void> {
  const variant = getVariantConfig(userId, experimentId);
  if (!variant) return;

  await trackExperimentEvent({
    eventType: 'view',
    userId,
    experimentId,
    variantId: variant.id,
    timestamp: new Date(),
    metadata: {
      monthlyPrice: variant.monthlyPrice,
      annualPrice: variant.annualPrice,
    },
  });
}

/**
 * Track purchase event with experiment data.
 */
async function trackPurchaseEvent(
  userId: string,
  packagePurchased: PurchasesPackage,
  assignment: string
): Promise<void> {
  const [experimentId, variantId] = assignment.split(':');

  await trackExperimentEvent({
    eventType: 'purchase',
    userId,
    experimentId,
    variantId,
    timestamp: new Date(),
    metadata: {
      productId: packagePurchased.product.identifier,
      price: packagePurchased.product.price,
      currencyCode: packagePurchased.product.currencyCode,
      packageType: packagePurchased.packageType,
    },
  });
}

// ============================================================================
// Statistical Analysis Helpers
// ============================================================================

interface VariantResults {
  variantId: string;
  visitors: number;
  conversions: number;
  revenue: number;
}

interface ExperimentResults {
  experimentId: string;
  startDate: Date;
  endDate: Date | null;
  variants: VariantResults[];
  winner: string | null;
  confidence: number;
  significantDifference: boolean;
}

/**
 * Calculate if experiment results are statistically significant.
 * Uses two-proportion z-test.
 */
export function calculateSignificance(
  control: VariantResults,
  treatment: VariantResults
): { zScore: number; pValue: number; significant: boolean; lift: number } {
  const controlRate = control.conversions / control.visitors;
  const treatmentRate = treatment.conversions / treatment.visitors;

  // Pooled proportion
  const pooledRate =
    (control.conversions + treatment.conversions) /
    (control.visitors + treatment.visitors);

  // Standard error
  const standardError = Math.sqrt(
    pooledRate *
      (1 - pooledRate) *
      (1 / control.visitors + 1 / treatment.visitors)
  );

  // Z-score
  const zScore = (treatmentRate - controlRate) / standardError;

  // P-value (two-tailed)
  const pValue = 2 * (1 - normalCDF(Math.abs(zScore)));

  // Lift
  const lift =
    controlRate > 0 ? ((treatmentRate - controlRate) / controlRate) * 100 : 0;

  return {
    zScore,
    pValue,
    significant: pValue < 0.05,
    lift,
  };
}

/**
 * Calculate confidence interval for a conversion rate.
 */
export function calculateConfidenceInterval(
  conversions: number,
  visitors: number,
  confidenceLevel: number = 0.95
): { lower: number; upper: number } {
  const rate = conversions / visitors;
  const zScore = normalInverse((1 + confidenceLevel) / 2);
  const standardError = Math.sqrt((rate * (1 - rate)) / visitors);

  return {
    lower: Math.max(0, rate - zScore * standardError),
    upper: Math.min(1, rate + zScore * standardError),
  };
}

/**
 * Calculate minimum sample size needed for experiment.
 */
export function calculateMinimumSampleSize(
  baselineConversion: number,
  minimumDetectableEffect: number, // e.g., 0.1 for 10% lift
  power: number = 0.8,
  significanceLevel: number = 0.05
): number {
  const zAlpha = normalInverse(1 - significanceLevel / 2);
  const zBeta = normalInverse(power);

  const p1 = baselineConversion;
  const p2 = baselineConversion * (1 + minimumDetectableEffect);
  const pooledP = (p1 + p2) / 2;

  const numerator = Math.pow(
    zAlpha * Math.sqrt(2 * pooledP * (1 - pooledP)) +
      zBeta * Math.sqrt(p1 * (1 - p1) + p2 * (1 - p2)),
    2
  );
  const denominator = Math.pow(p2 - p1, 2);

  return Math.ceil(numerator / denominator);
}

// Normal distribution helpers
function normalCDF(x: number): number {
  const a1 = 0.254829592;
  const a2 = -0.284496736;
  const a3 = 1.421413741;
  const a4 = -1.453152027;
  const a5 = 1.061405429;
  const p = 0.3275911;

  const sign = x < 0 ? -1 : 1;
  x = Math.abs(x) / Math.sqrt(2);

  const t = 1.0 / (1.0 + p * x);
  const y =
    1.0 -
    ((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);

  return 0.5 * (1.0 + sign * y);
}

function normalInverse(p: number): number {
  // Approximation of inverse normal CDF
  const a = [
    -3.969683028665376e1, 2.209460984245205e2, -2.759285104469687e2,
    1.383577518672690e2, -3.066479806614716e1, 2.506628277459239e0,
  ];
  const b = [
    -5.447609879822406e1, 1.615858368580409e2, -1.556989798598866e2,
    6.680131188771972e1, -1.328068155288572e1,
  ];
  const c = [
    -7.784894002430293e-3, -3.223964580411365e-1, -2.400758277161838e0,
    -2.549732539343734e0, 4.374664141464968e0, 2.938163982698783e0,
  ];
  const d = [
    7.784695709041462e-3, 3.224671290700398e-1, 2.445134137142996e0,
    3.754408661907416e0,
  ];

  const pLow = 0.02425;
  const pHigh = 1 - pLow;

  let q, r;

  if (p < pLow) {
    q = Math.sqrt(-2 * Math.log(p));
    return (
      (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) /
      ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    );
  } else if (p <= pHigh) {
    q = p - 0.5;
    r = q * q;
    return (
      ((((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) *
        q) /
      (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)
    );
  } else {
    q = Math.sqrt(-2 * Math.log(1 - p));
    return (
      -(
        (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) /
        ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
      )
    );
  }
}

// ============================================================================
// Platform Import (would be actual import in real app)
// ============================================================================

const Platform = {
  OS: 'ios' as 'ios' | 'android',
};

// ============================================================================
// Exports
// ============================================================================

export default {
  initializePurchases,
  getExperimentAssignment,
  getVariantConfig,
  getOffering,
  getPricingDisplayData,
  purchasePackage,
  restorePurchases,
  trackPaywallView,
  calculateSignificance,
  calculateConfidenceInterval,
  calculateMinimumSampleSize,
};
