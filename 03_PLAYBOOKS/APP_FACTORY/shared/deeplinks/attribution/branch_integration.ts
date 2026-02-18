/**
 * Branch.io SDK Integration
 * Handles Branch initialization, event tracking, deep linking, and attribution
 */

import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

import type { AppId, BranchConfig, AttributionData, ReferralLinkData } from '../types';
import { getBranchConfig, COMMON_EVENTS, CommonEventType } from './attribution_config';

// Storage keys
const STORAGE_KEYS = {
  BRANCH_ATTRIBUTION: '@branch_attribution',
  BRANCH_IDENTITY: '@branch_identity',
  BRANCH_FIRST_PARAMS: '@branch_first_params',
} as const;

/**
 * Branch SDK wrapper interface
 * Matches react-native-branch SDK structure
 */
interface BranchSDK {
  subscribe: (callback: (params: BranchParams) => void) => () => void;
  setIdentity: (userId: string) => Promise<BranchParams>;
  logout: () => Promise<void>;
  getLatestReferringParams: () => Promise<BranchParams>;
  getFirstReferringParams: () => Promise<BranchParams>;
  createBranchUniversalObject: (
    identifier: string,
    options: BranchUniversalObjectOptions
  ) => Promise<BranchUniversalObject>;
  logStandardEvent: (
    eventName: BranchStandardEvent,
    params?: BranchEventParams
  ) => Promise<void>;
  logEvent: (eventName: string, params?: Record<string, unknown>) => Promise<void>;
  disableTracking: (disable: boolean) => void;
}

interface BranchParams {
  '+is_first_session': boolean;
  '+clicked_branch_link': boolean;
  '+match_guaranteed': boolean;
  '+non_branch_link'?: string;
  '~feature'?: string;
  '~channel'?: string;
  '~campaign'?: string;
  '~stage'?: string;
  '~tags'?: string[];
  '~creation_source'?: number;
  '$deeplink_path'?: string;
  '$desktop_url'?: string;
  '$ios_url'?: string;
  '$android_url'?: string;
  referrer_id?: string;
  referral_code?: string;
  [key: string]: unknown;
}

interface BranchUniversalObjectOptions {
  locallyIndex?: boolean;
  publiclyIndex?: boolean;
  canonicalUrl?: string;
  title?: string;
  contentDescription?: string;
  contentImageUrl?: string;
  contentMetadata?: {
    customMetadata?: Record<string, string>;
    contentSchema?: string;
    quantity?: number;
    price?: number;
    currency?: string;
    sku?: string;
    productName?: string;
    productBrand?: string;
    productCategory?: string;
    productVariant?: string;
    condition?: string;
    ratingAverage?: number;
    ratingCount?: number;
    ratingMax?: number;
    addressStreet?: string;
    addressCity?: string;
    addressRegion?: string;
    addressCountry?: string;
    addressPostalCode?: string;
    latitude?: number;
    longitude?: number;
    imageCaptions?: string[];
  };
}

interface BranchUniversalObject {
  showShareSheet: (
    options: BranchShareSheetOptions,
    controlParams: BranchControlParams
  ) => Promise<{ channel: string; completed: boolean; error: Error | null }>;
  generateShortUrl: (
    linkProperties: BranchLinkProperties,
    controlParams: BranchControlParams
  ) => Promise<{ url: string }>;
  logEvent: (eventName: string, params?: Record<string, unknown>) => Promise<void>;
  release: () => void;
}

interface BranchShareSheetOptions {
  messageHeader?: string;
  messageBody?: string;
}

interface BranchLinkProperties {
  feature?: string;
  channel?: string;
  campaign?: string;
  stage?: string;
  tags?: string[];
  alias?: string;
}

interface BranchControlParams {
  $desktop_url?: string;
  $ios_url?: string;
  $android_url?: string;
  $fallback_url?: string;
  $deeplink_path?: string;
  custom_data?: Record<string, string>;
}

interface BranchEventParams {
  transactionID?: string;
  currency?: string;
  revenue?: number;
  shipping?: number;
  tax?: number;
  coupon?: string;
  affiliation?: string;
  description?: string;
  searchQuery?: string;
  customData?: Record<string, string>;
}

type BranchStandardEvent =
  | 'ADD_TO_CART'
  | 'ADD_TO_WISHLIST'
  | 'VIEW_CART'
  | 'INITIATE_PURCHASE'
  | 'ADD_PAYMENT_INFO'
  | 'PURCHASE'
  | 'SPEND_CREDITS'
  | 'SEARCH'
  | 'VIEW_ITEM'
  | 'VIEW_ITEMS'
  | 'RATE'
  | 'SHARE'
  | 'COMPLETE_REGISTRATION'
  | 'COMPLETE_TUTORIAL'
  | 'ACHIEVE_LEVEL'
  | 'UNLOCK_ACHIEVEMENT'
  | 'INVITE'
  | 'LOGIN'
  | 'SUBSCRIBE'
  | 'START_TRIAL';

// SDK reference (lazy loaded)
let branch: BranchSDK | null = null;

/**
 * Load SDK dynamically
 */
async function loadSDK(): Promise<boolean> {
  if (branch) return true;

  try {
    const sdk = await import('react-native-branch');
    branch = sdk.default;
    return true;
  } catch (error) {
    console.warn('[Branch] SDK not installed:', error);
    return false;
  }
}

/**
 * Branch Integration Service
 */
class BranchIntegration {
  private config: BranchConfig | null = null;
  private isInitialized = false;
  private attribution: AttributionData | null = null;
  private identity: string | null = null;
  private firstParams: BranchParams | null = null;
  private unsubscribe: (() => void) | null = null;
  private debug = false;

  /**
   * Initialize Branch SDK
   */
  async initialize(
    appId: AppId,
    options?: {
      onDeepLink?: (params: BranchParams, uri: string | null) => void;
      onFirstSession?: (params: BranchParams) => void;
    }
  ): Promise<boolean> {
    if (this.isInitialized) {
      this.log('Already initialized');
      return true;
    }

    const sdkLoaded = await loadSDK();
    if (!sdkLoaded || !branch) {
      console.error('[Branch] SDK not available');
      return false;
    }

    this.config = getBranchConfig(appId);
    this.debug = this.config.enableLogging;

    try {
      // Load stored data
      await this.loadStoredData();

      // Subscribe to deep links
      this.unsubscribe = branch.subscribe((params: BranchParams) => {
        this.log(`Deep link params: ${JSON.stringify(params)}`);

        // Parse attribution
        if (params['+clicked_branch_link']) {
          const parsed = this.parseParams(params);
          this.attribution = parsed;
          this.saveAttribution(parsed);
        }

        // First session handling
        if (params['+is_first_session']) {
          this.firstParams = params;
          this.saveFirstParams(params);
          options?.onFirstSession?.(params);
        }

        // Deep link callback
        const uri = params['$deeplink_path'] || null;
        options?.onDeepLink?.(params, uri as string | null);
      });

      this.isInitialized = true;
      this.log('Initialized successfully');
      return true;
    } catch (error) {
      console.error('[Branch] Initialization error:', error);
      return false;
    }
  }

  /**
   * Set user identity
   */
  async setIdentity(userId: string): Promise<void> {
    if (!branch) return;

    try {
      const params = await branch.setIdentity(userId);
      this.identity = userId;
      await this.saveIdentity(userId);
      this.log(`Identity set: ${userId}`);

      // Update attribution if returned
      if (params['+clicked_branch_link']) {
        const parsed = this.parseParams(params);
        this.attribution = parsed;
        await this.saveAttribution(parsed);
      }
    } catch (error) {
      console.error('[Branch] Error setting identity:', error);
    }
  }

  /**
   * Logout user identity
   */
  async logout(): Promise<void> {
    if (!branch) return;

    try {
      await branch.logout();
      this.identity = null;
      await AsyncStorage.removeItem(STORAGE_KEYS.BRANCH_IDENTITY);
      this.log('User logged out');
    } catch (error) {
      console.error('[Branch] Error logging out:', error);
    }
  }

  /**
   * Track an event
   */
  async trackEvent(
    eventType: CommonEventType | string,
    params?: BranchEventParams
  ): Promise<void> {
    if (!branch) {
      this.log('Cannot track event - not initialized');
      return;
    }

    // Map common events to Branch standard events
    const eventMap: Record<string, BranchStandardEvent> = {
      signup: 'COMPLETE_REGISTRATION',
      login: 'LOGIN',
      purchase: 'PURCHASE',
      subscribe: 'SUBSCRIBE',
      trial_start: 'START_TRIAL',
      share: 'SHARE',
      referral: 'INVITE',
      content_view: 'VIEW_ITEM',
      level_up: 'ACHIEVE_LEVEL',
      achievement: 'UNLOCK_ACHIEVEMENT',
    };

    const standardEvent = eventMap[eventType];

    try {
      if (standardEvent) {
        await branch.logStandardEvent(standardEvent, params);
      } else {
        await branch.logEvent(eventType, params);
      }
      this.log(`Tracked event: ${eventType}`);
    } catch (error) {
      console.error(`[Branch] Error tracking ${eventType}:`, error);
    }
  }

  /**
   * Track a purchase event
   */
  async trackPurchase(params: {
    revenue: number;
    currency: string;
    transactionId: string;
    productId?: string;
  }): Promise<void> {
    await this.trackEvent(COMMON_EVENTS.PURCHASE, {
      revenue: params.revenue,
      currency: params.currency,
      transactionID: params.transactionId,
      customData: params.productId
        ? { product_id: params.productId }
        : undefined,
    });
  }

  /**
   * Track subscription event
   */
  async trackSubscription(params: {
    revenue: number;
    currency: string;
    transactionId: string;
    productId: string;
    subscriptionPeriod?: string;
  }): Promise<void> {
    await this.trackEvent(COMMON_EVENTS.SUBSCRIBE, {
      revenue: params.revenue,
      currency: params.currency,
      transactionID: params.transactionId,
      customData: {
        product_id: params.productId,
        subscription_period: params.subscriptionPeriod || 'monthly',
      },
    });
  }

  /**
   * Generate a Branch short URL
   */
  async generateLink(params: {
    feature?: string;
    channel?: string;
    campaign?: string;
    tags?: string[];
    data?: Record<string, string>;
    title?: string;
    description?: string;
    imageUrl?: string;
  }): Promise<string> {
    if (!branch) {
      throw new Error('Branch not initialized');
    }

    try {
      const buo = await branch.createBranchUniversalObject(
        `content/${Date.now()}`,
        {
          title: params.title,
          contentDescription: params.description,
          contentImageUrl: params.imageUrl,
          contentMetadata: {
            customMetadata: params.data,
          },
        }
      );

      const { url } = await buo.generateShortUrl(
        {
          feature: params.feature || 'sharing',
          channel: params.channel,
          campaign: params.campaign,
          tags: params.tags,
        },
        {
          custom_data: params.data,
        }
      );

      buo.release();
      this.log(`Generated link: ${url}`);
      return url;
    } catch (error) {
      console.error('[Branch] Error generating link:', error);
      throw error;
    }
  }

  /**
   * Generate a referral link
   */
  async generateReferralLink(params: {
    referrerId: string;
    referrerName?: string;
    campaign?: string;
    channel?: string;
    reward?: {
      referrer: string;
      referred: string;
    };
  }): Promise<ReferralLinkData> {
    const url = await this.generateLink({
      feature: 'referral',
      channel: params.channel || 'app',
      campaign: params.campaign || 'referral_program',
      data: {
        referrer_id: params.referrerId,
        referrer_name: params.referrerName || '',
        reward_referrer: params.reward?.referrer || '',
        reward_referred: params.reward?.referred || '',
      },
      title: params.referrerName
        ? `${params.referrerName} invited you!`
        : 'You have been invited!',
    });

    return {
      referrerId: params.referrerId,
      referrerName: params.referrerName || '',
      referralCode: params.referrerId.substring(0, 8).toUpperCase(),
      campaign: params.campaign || null,
      referrerReward: params.reward?.referrer
        ? {
            type: 'custom',
            value: 0,
            displayString: params.reward.referrer,
          }
        : null,
      referredReward: params.reward?.referred
        ? {
            type: 'custom',
            value: 0,
            displayString: params.reward.referred,
          }
        : null,
      expiresAt: null,
      linkUrl: url,
      shortLinkUrl: url,
    };
  }

  /**
   * Show native share sheet
   */
  async showShareSheet(params: {
    title?: string;
    description?: string;
    imageUrl?: string;
    data?: Record<string, string>;
    messageHeader?: string;
    messageBody?: string;
  }): Promise<{ channel: string; completed: boolean }> {
    if (!branch) {
      throw new Error('Branch not initialized');
    }

    try {
      const buo = await branch.createBranchUniversalObject(
        `share/${Date.now()}`,
        {
          title: params.title,
          contentDescription: params.description,
          contentImageUrl: params.imageUrl,
          contentMetadata: {
            customMetadata: params.data,
          },
        }
      );

      const result = await buo.showShareSheet(
        {
          messageHeader: params.messageHeader,
          messageBody: params.messageBody,
        },
        {
          custom_data: params.data,
        }
      );

      buo.release();
      return { channel: result.channel, completed: result.completed };
    } catch (error) {
      console.error('[Branch] Error showing share sheet:', error);
      throw error;
    }
  }

  /**
   * Disable tracking (GDPR compliance)
   */
  disableTracking(disable: boolean): void {
    if (!branch) return;
    branch.disableTracking(disable);
    this.log(`Tracking ${disable ? 'disabled' : 'enabled'}`);
  }

  /**
   * Get latest referring params
   */
  async getLatestParams(): Promise<BranchParams | null> {
    if (!branch) return null;

    try {
      return await branch.getLatestReferringParams();
    } catch {
      return null;
    }
  }

  /**
   * Get first referring params (install attribution)
   */
  async getFirstParams(): Promise<BranchParams | null> {
    if (!branch) return this.firstParams;

    try {
      return await branch.getFirstReferringParams();
    } catch {
      return this.firstParams;
    }
  }

  /**
   * Get current attribution
   */
  getAttribution(): AttributionData | null {
    return this.attribution;
  }

  /**
   * Get user identity
   */
  getIdentity(): string | null {
    return this.identity;
  }

  /**
   * Parse Branch params to our format
   */
  private parseParams(params: BranchParams): AttributionData {
    return {
      network: 'branch',
      campaign: (params['~campaign'] as string) || null,
      adGroup: (params['~stage'] as string) || null,
      creative: null,
      channel: (params['~channel'] as string) || null,
      utmSource: (params['~channel'] as string) || null,
      utmMedium: (params['~feature'] as string) || null,
      utmCampaign: (params['~campaign'] as string) || null,
      utmContent: null,
      utmTerm: null,
      referrerId: (params.referrer_id as string) || null,
      clickId: null,
      rawData: params as unknown as Record<string, string>,
    };
  }

  /**
   * Save attribution to storage
   */
  private async saveAttribution(attribution: AttributionData): Promise<void> {
    try {
      await AsyncStorage.setItem(
        STORAGE_KEYS.BRANCH_ATTRIBUTION,
        JSON.stringify(attribution)
      );
    } catch (error) {
      console.error('[Branch] Error saving attribution:', error);
    }
  }

  /**
   * Save identity to storage
   */
  private async saveIdentity(identity: string): Promise<void> {
    try {
      await AsyncStorage.setItem(STORAGE_KEYS.BRANCH_IDENTITY, identity);
    } catch (error) {
      console.error('[Branch] Error saving identity:', error);
    }
  }

  /**
   * Save first params to storage
   */
  private async saveFirstParams(params: BranchParams): Promise<void> {
    try {
      await AsyncStorage.setItem(
        STORAGE_KEYS.BRANCH_FIRST_PARAMS,
        JSON.stringify(params)
      );
    } catch (error) {
      console.error('[Branch] Error saving first params:', error);
    }
  }

  /**
   * Load stored data
   */
  private async loadStoredData(): Promise<void> {
    try {
      const [attrJson, identity, paramsJson] = await Promise.all([
        AsyncStorage.getItem(STORAGE_KEYS.BRANCH_ATTRIBUTION),
        AsyncStorage.getItem(STORAGE_KEYS.BRANCH_IDENTITY),
        AsyncStorage.getItem(STORAGE_KEYS.BRANCH_FIRST_PARAMS),
      ]);

      if (attrJson) {
        this.attribution = JSON.parse(attrJson);
      }
      if (identity) {
        this.identity = identity;
      }
      if (paramsJson) {
        this.firstParams = JSON.parse(paramsJson);
      }
    } catch (error) {
      console.error('[Branch] Error loading stored data:', error);
    }
  }

  /**
   * Cleanup on unmount
   */
  destroy(): void {
    if (this.unsubscribe) {
      this.unsubscribe();
      this.unsubscribe = null;
    }
    this.isInitialized = false;
  }

  /**
   * Debug log
   */
  private log(message: string): void {
    if (this.debug) {
      console.log(`[Branch] ${message}`);
    }
  }
}

// Export singleton
export const branchIntegration = new BranchIntegration();
export default branchIntegration;
