/**
 * subscriptionApi.ts - Subscription and billing endpoints
 */

import { apiClient } from '../ApiClient';
import type { SuccessResponse } from '../types/ApiResponse';

// ============================================================================
// Types
// ============================================================================

export type SubscriptionStatus =
  | 'active'
  | 'trialing'
  | 'past_due'
  | 'canceled'
  | 'unpaid'
  | 'expired';

export type BillingInterval = 'month' | 'year' | 'week' | 'lifetime';

export interface Plan {
  id: string;
  name: string;
  description: string;
  features: string[];
  pricing: {
    monthly: PriceTier;
    yearly: PriceTier;
  };
  limits: {
    [key: string]: number;
  };
  popular?: boolean;
  order: number;
}

export interface PriceTier {
  amount: number;
  currency: string;
  interval: BillingInterval;
  trialDays?: number;
  productId: string; // RevenueCat/Stripe product ID
}

export interface Subscription {
  id: string;
  planId: string;
  plan: Plan;
  status: SubscriptionStatus;
  currentPeriodStart: string;
  currentPeriodEnd: string;
  cancelAtPeriodEnd: boolean;
  canceledAt: string | null;
  trialStart: string | null;
  trialEnd: string | null;
  billing: {
    interval: BillingInterval;
    amount: number;
    currency: string;
    nextBillingDate: string | null;
  };
  createdAt: string;
  updatedAt: string;
}

export interface SubscriptionEntitlements {
  plan: string;
  features: string[];
  limits: {
    [key: string]: {
      limit: number;
      used: number;
      remaining: number;
    };
  };
  isActive: boolean;
  isPremium: boolean;
  isTrial: boolean;
  daysRemaining: number;
}

export interface PaymentMethod {
  id: string;
  type: 'card' | 'paypal' | 'apple_pay' | 'google_pay';
  isDefault: boolean;
  card?: {
    brand: string;
    last4: string;
    expiryMonth: number;
    expiryYear: number;
  };
  createdAt: string;
}

export interface Invoice {
  id: string;
  number: string;
  status: 'draft' | 'open' | 'paid' | 'void' | 'uncollectible';
  amount: number;
  currency: string;
  description: string;
  periodStart: string;
  periodEnd: string;
  pdfUrl: string | null;
  createdAt: string;
  paidAt: string | null;
}

export interface UsageRecord {
  feature: string;
  used: number;
  limit: number;
  periodStart: string;
  periodEnd: string;
}

export interface PromoCode {
  code: string;
  discount: {
    type: 'percent' | 'fixed';
    amount: number;
  };
  validUntil: string | null;
  applicablePlans: string[];
}

// ============================================================================
// Request Types
// ============================================================================

export interface CreateSubscriptionRequest {
  planId: string;
  interval: BillingInterval;
  promoCode?: string;
  paymentMethodId?: string;
}

export interface UpdateSubscriptionRequest {
  planId?: string;
  interval?: BillingInterval;
}

export interface AddPaymentMethodRequest {
  type: PaymentMethod['type'];
  token: string; // Payment processor token
  setDefault?: boolean;
}

// ============================================================================
// Subscription API Class
// ============================================================================

class SubscriptionApi {
  private readonly basePath = '/subscriptions';

  // --------------------------------------------------------------------------
  // Plans
  // --------------------------------------------------------------------------

  /**
   * Get available plans
   */
  async getPlans(): Promise<Plan[]> {
    return apiClient.get(`${this.basePath}/plans`, { skipAuth: true });
  }

  /**
   * Get plan by ID
   */
  async getPlanById(planId: string): Promise<Plan> {
    return apiClient.get(`${this.basePath}/plans/${planId}`, { skipAuth: true });
  }

  // --------------------------------------------------------------------------
  // Subscription Management
  // --------------------------------------------------------------------------

  /**
   * Get current subscription
   */
  async getCurrentSubscription(): Promise<Subscription | null> {
    return apiClient.get(`${this.basePath}/current`);
  }

  /**
   * Get subscription entitlements
   */
  async getEntitlements(): Promise<SubscriptionEntitlements> {
    return apiClient.get(`${this.basePath}/entitlements`);
  }

  /**
   * Create new subscription
   */
  async createSubscription(data: CreateSubscriptionRequest): Promise<Subscription> {
    return apiClient.post(this.basePath, data);
  }

  /**
   * Update subscription (change plan/interval)
   */
  async updateSubscription(data: UpdateSubscriptionRequest): Promise<Subscription> {
    return apiClient.patch(`${this.basePath}/current`, data);
  }

  /**
   * Cancel subscription
   */
  async cancelSubscription(
    immediately: boolean = false
  ): Promise<Subscription> {
    return apiClient.post(`${this.basePath}/current/cancel`, { immediately });
  }

  /**
   * Resume canceled subscription
   */
  async resumeSubscription(): Promise<Subscription> {
    return apiClient.post(`${this.basePath}/current/resume`);
  }

  /**
   * Pause subscription (if supported)
   */
  async pauseSubscription(
    resumeAt?: string
  ): Promise<Subscription> {
    return apiClient.post(`${this.basePath}/current/pause`, { resumeAt });
  }

  // --------------------------------------------------------------------------
  // Payment Methods
  // --------------------------------------------------------------------------

  /**
   * Get payment methods
   */
  async getPaymentMethods(): Promise<PaymentMethod[]> {
    return apiClient.get(`${this.basePath}/payment-methods`);
  }

  /**
   * Add payment method
   */
  async addPaymentMethod(data: AddPaymentMethodRequest): Promise<PaymentMethod> {
    return apiClient.post(`${this.basePath}/payment-methods`, data);
  }

  /**
   * Set default payment method
   */
  async setDefaultPaymentMethod(methodId: string): Promise<SuccessResponse> {
    return apiClient.post(`${this.basePath}/payment-methods/${methodId}/default`);
  }

  /**
   * Delete payment method
   */
  async deletePaymentMethod(methodId: string): Promise<SuccessResponse> {
    return apiClient.delete(`${this.basePath}/payment-methods/${methodId}`);
  }

  // --------------------------------------------------------------------------
  // Billing History
  // --------------------------------------------------------------------------

  /**
   * Get invoices
   */
  async getInvoices(
    params?: { page?: number; limit?: number }
  ): Promise<{ invoices: Invoice[]; total: number }> {
    return apiClient.get(`${this.basePath}/invoices`, { params });
  }

  /**
   * Get invoice by ID
   */
  async getInvoiceById(invoiceId: string): Promise<Invoice> {
    return apiClient.get(`${this.basePath}/invoices/${invoiceId}`);
  }

  /**
   * Download invoice PDF
   */
  async getInvoiceDownloadUrl(invoiceId: string): Promise<{ url: string }> {
    return apiClient.get(`${this.basePath}/invoices/${invoiceId}/download`);
  }

  // --------------------------------------------------------------------------
  // Usage & Limits
  // --------------------------------------------------------------------------

  /**
   * Get usage records
   */
  async getUsage(): Promise<UsageRecord[]> {
    return apiClient.get(`${this.basePath}/usage`);
  }

  /**
   * Check if feature is available
   */
  async checkFeature(feature: string): Promise<{
    available: boolean;
    limit?: number;
    used?: number;
    requiresUpgrade?: boolean;
    suggestedPlan?: string;
  }> {
    return apiClient.get(`${this.basePath}/check-feature/${feature}`);
  }

  // --------------------------------------------------------------------------
  // Promo Codes
  // --------------------------------------------------------------------------

  /**
   * Validate promo code
   */
  async validatePromoCode(
    code: string,
    planId?: string
  ): Promise<{ valid: boolean; promo?: PromoCode; error?: string }> {
    return apiClient.post(`${this.basePath}/promo/validate`, { code, planId });
  }

  /**
   * Apply promo code to subscription
   */
  async applyPromoCode(code: string): Promise<Subscription> {
    return apiClient.post(`${this.basePath}/promo/apply`, { code });
  }

  // --------------------------------------------------------------------------
  // RevenueCat Integration
  // --------------------------------------------------------------------------

  /**
   * Sync RevenueCat purchase
   */
  async syncRevenueCatPurchase(purchaseInfo: {
    productId: string;
    transactionId: string;
    receipt?: string;
  }): Promise<Subscription> {
    return apiClient.post(`${this.basePath}/revenuecat/sync`, purchaseInfo);
  }

  /**
   * Restore purchases (iOS)
   */
  async restorePurchases(): Promise<Subscription | null> {
    return apiClient.post(`${this.basePath}/restore`);
  }

  // --------------------------------------------------------------------------
  // Webhooks (for backend to verify)
  // --------------------------------------------------------------------------

  /**
   * Get webhook events (admin)
   */
  async getWebhookEvents(
    params?: { page?: number; limit?: number }
  ): Promise<{ events: unknown[]; total: number }> {
    return apiClient.get(`${this.basePath}/webhooks`, { params });
  }
}

// ============================================================================
// Singleton Export
// ============================================================================

export const subscriptionApi = new SubscriptionApi();

export default subscriptionApi;
