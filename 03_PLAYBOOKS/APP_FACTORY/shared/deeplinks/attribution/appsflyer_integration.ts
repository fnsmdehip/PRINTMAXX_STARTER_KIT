/**
 * AppsFlyer SDK Integration
 * Handles AppsFlyer initialization, event tracking, and attribution
 */

import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

import type { AppId, AppsFlyerConfig, AttributionData } from '../types';
import { getAppsFlyerConfig, COMMON_EVENTS, CommonEventType } from './attribution_config';

// Storage keys
const STORAGE_KEYS = {
  APPSFLYER_ATTRIBUTION: '@appsflyer_attribution',
  APPSFLYER_UID: '@appsflyer_uid',
} as const;

/**
 * AppsFlyer SDK wrapper interface
 * Matches react-native-appsflyer SDK structure
 */
interface AppsFlyerSDK {
  initSdk: (
    options: AppsFlyerInitOptions,
    successCallback?: (result: unknown) => void,
    errorCallback?: (error: unknown) => void
  ) => void;
  logEvent: (
    eventName: string,
    eventValues: Record<string, unknown>,
    successCallback?: (result: unknown) => void,
    errorCallback?: (error: unknown) => void
  ) => void;
  setCustomerUserId: (userId: string) => void;
  getAppsFlyerUID: (callback: (error: Error | null, uid: string) => void) => void;
  onInstallConversionData: (callback: (data: ConversionData) => void) => void;
  onAppOpenAttribution: (callback: (data: unknown) => void) => void;
  onDeepLink: (callback: (data: DeepLinkData) => void) => void;
  setAdditionalData: (data: Record<string, string>) => void;
  stop: (shouldStop: boolean) => void;
  anonymizeUser: (shouldAnonymize: boolean) => void;
  generateInviteLink: (
    params: GenerateLinkParams,
    successCallback: (url: string) => void,
    errorCallback: (error: Error) => void
  ) => void;
}

interface AppsFlyerInitOptions {
  devKey: string;
  isDebug: boolean;
  appId: string;
  onInstallConversionDataListener?: boolean;
  onDeepLinkListener?: boolean;
  timeToWaitForATTUserAuthorization?: number;
}

interface ConversionData {
  status: string;
  type: string;
  data: {
    af_status: string;
    af_message?: string;
    media_source?: string;
    campaign?: string;
    campaign_id?: string;
    adset?: string;
    adset_id?: string;
    ad?: string;
    ad_id?: string;
    click_time?: string;
    install_time?: string;
    clickid?: string;
    af_referrer_uid?: string;
    af_referrer_customer_id?: string;
    [key: string]: unknown;
  };
}

interface DeepLinkData {
  status: string;
  deepLinkValue?: string;
  deepLinkSubValues?: Record<string, string>;
  isDeferred?: boolean;
  clickEvent?: Record<string, unknown>;
}

interface GenerateLinkParams {
  channel: string;
  campaign?: string;
  referrerName?: string;
  referrerImageURL?: string;
  customerID?: string;
  baseDeepLink?: string;
  brandDomain?: string;
}

// SDK reference (lazy loaded)
let appsflyer: AppsFlyerSDK | null = null;

/**
 * Load SDK dynamically
 */
async function loadSDK(): Promise<boolean> {
  if (appsflyer) return true;

  try {
    const sdk = await import('react-native-appsflyer');
    appsflyer = sdk.default;
    return true;
  } catch (error) {
    console.warn('[AppsFlyer] SDK not installed:', error);
    return false;
  }
}

/**
 * AppsFlyer Integration Service
 */
class AppsFlyerIntegration {
  private config: AppsFlyerConfig | null = null;
  private isInitialized = false;
  private attribution: AttributionData | null = null;
  private uid: string | null = null;
  private debug = false;

  /**
   * Initialize AppsFlyer SDK
   */
  async initialize(
    appId: AppId,
    options?: {
      onConversionData?: (data: AttributionData) => void;
      onDeepLink?: (url: string, data: Record<string, unknown>) => void;
    }
  ): Promise<boolean> {
    if (this.isInitialized) {
      this.log('Already initialized');
      return true;
    }

    const sdkLoaded = await loadSDK();
    if (!sdkLoaded || !appsflyer) {
      console.error('[AppsFlyer] SDK not available');
      return false;
    }

    this.config = getAppsFlyerConfig(appId);
    this.debug = this.config.isDebug;

    try {
      // Set up conversion data listener before init
      appsflyer.onInstallConversionData((data: ConversionData) => {
        this.log(`Conversion data: ${JSON.stringify(data)}`);

        if (data.status === 'success') {
          const parsed = this.parseConversionData(data);
          this.attribution = parsed;
          this.saveAttribution(parsed);
          options?.onConversionData?.(parsed);
        }
      });

      // Set up deep link listener
      appsflyer.onDeepLink((data: DeepLinkData) => {
        this.log(`Deep link: ${JSON.stringify(data)}`);

        if (data.deepLinkValue) {
          options?.onDeepLink?.(data.deepLinkValue, data.clickEvent || {});
        }
      });

      // Initialize SDK
      return new Promise((resolve) => {
        appsflyer!.initSdk(
          {
            devKey: this.config!.devKey,
            isDebug: this.debug,
            appId: Platform.OS === 'ios' ? this.config!.appId : '',
            onInstallConversionDataListener: true,
            onDeepLinkListener: true,
            timeToWaitForATTUserAuthorization:
              this.config!.timeToWaitForATTUserAuthorization,
          },
          (result) => {
            this.log(`Initialized: ${JSON.stringify(result)}`);
            this.isInitialized = true;
            this.fetchUid();
            this.loadStoredAttribution();
            resolve(true);
          },
          (error) => {
            console.error('[AppsFlyer] Init error:', error);
            resolve(false);
          }
        );
      });
    } catch (error) {
      console.error('[AppsFlyer] Initialization error:', error);
      return false;
    }
  }

  /**
   * Track an event
   */
  trackEvent(
    eventType: CommonEventType | string,
    params?: Record<string, unknown>
  ): void {
    if (!this.isInitialized || !appsflyer) {
      this.log('Cannot track event - not initialized');
      return;
    }

    // Map common events to AppsFlyer event names
    const eventNameMap: Record<string, string> = {
      install: 'af_install',
      signup: 'af_complete_registration',
      login: 'af_login',
      purchase: 'af_purchase',
      subscribe: 'af_subscribe',
      trial_start: 'af_start_trial',
      share: 'af_share',
      referral: 'af_invite',
      content_view: 'af_content_view',
      level_up: 'af_level_achieved',
      achievement: 'af_achievement_unlocked',
    };

    const eventName = eventNameMap[eventType] || eventType;

    appsflyer.logEvent(
      eventName,
      params || {},
      (result) => {
        this.log(`Tracked event ${eventName}: ${JSON.stringify(result)}`);
      },
      (error) => {
        console.error(`[AppsFlyer] Error tracking ${eventName}:`, error);
      }
    );
  }

  /**
   * Track a purchase event
   */
  trackPurchase(params: {
    revenue: number;
    currency: string;
    transactionId: string;
    productId?: string;
    quantity?: number;
  }): void {
    this.trackEvent(COMMON_EVENTS.PURCHASE, {
      af_revenue: params.revenue,
      af_currency: params.currency,
      af_order_id: params.transactionId,
      af_content_id: params.productId,
      af_quantity: params.quantity || 1,
    });
  }

  /**
   * Track subscription event
   */
  trackSubscription(params: {
    revenue: number;
    currency: string;
    transactionId: string;
    productId: string;
    subscriptionPeriod?: string;
  }): void {
    this.trackEvent(COMMON_EVENTS.SUBSCRIBE, {
      af_revenue: params.revenue,
      af_currency: params.currency,
      af_order_id: params.transactionId,
      af_subscription_id: params.productId,
      af_subscription_period: params.subscriptionPeriod || 'monthly',
    });
  }

  /**
   * Set customer user ID
   */
  setUserId(userId: string): void {
    if (!appsflyer) return;
    appsflyer.setCustomerUserId(userId);
    this.log(`Set user ID: ${userId}`);
  }

  /**
   * Add additional data to be sent with events
   */
  setAdditionalData(data: Record<string, string>): void {
    if (!appsflyer) return;
    appsflyer.setAdditionalData(data);
  }

  /**
   * Generate invite/referral link
   */
  async generateInviteLink(params: {
    channel: string;
    campaign?: string;
    referrerId: string;
    referrerName?: string;
    deepLinkValue?: string;
  }): Promise<string> {
    if (!appsflyer || !this.config) {
      throw new Error('AppsFlyer not initialized');
    }

    return new Promise((resolve, reject) => {
      appsflyer!.generateInviteLink(
        {
          channel: params.channel,
          campaign: params.campaign,
          customerID: params.referrerId,
          referrerName: params.referrerName,
          baseDeepLink: params.deepLinkValue,
        },
        (url: string) => {
          this.log(`Generated invite link: ${url}`);
          resolve(url);
        },
        (error: Error) => {
          console.error('[AppsFlyer] Error generating link:', error);
          reject(error);
        }
      );
    });
  }

  /**
   * Stop SDK tracking (for GDPR compliance)
   */
  stop(): void {
    if (!appsflyer) return;
    appsflyer.stop(true);
    this.log('SDK stopped');
  }

  /**
   * Resume SDK tracking
   */
  start(): void {
    if (!appsflyer) return;
    appsflyer.stop(false);
    this.log('SDK resumed');
  }

  /**
   * Anonymize user data (GDPR)
   */
  anonymizeUser(shouldAnonymize: boolean): void {
    if (!appsflyer) return;
    appsflyer.anonymizeUser(shouldAnonymize);
    this.log(`User anonymization: ${shouldAnonymize}`);
  }

  /**
   * Get current attribution
   */
  getAttribution(): AttributionData | null {
    return this.attribution;
  }

  /**
   * Get AppsFlyer UID
   */
  getUid(): string | null {
    return this.uid;
  }

  /**
   * Fetch AppsFlyer UID
   */
  private fetchUid(): void {
    if (!appsflyer) return;

    appsflyer.getAppsFlyerUID((error, uid) => {
      if (error) {
        console.error('[AppsFlyer] Error getting UID:', error);
        return;
      }
      this.uid = uid;
      this.saveUid(uid);
      this.log(`UID: ${uid}`);
    });
  }

  /**
   * Parse conversion data to our format
   */
  private parseConversionData(raw: ConversionData): AttributionData {
    const data = raw.data;

    return {
      network: 'appsflyer',
      campaign: data.campaign || null,
      adGroup: data.adset || null,
      creative: data.ad || null,
      channel: data.media_source || null,
      utmSource: data.media_source || null,
      utmMedium: null,
      utmCampaign: data.campaign || null,
      utmContent: data.ad || null,
      utmTerm: null,
      referrerId: data.af_referrer_customer_id || data.af_referrer_uid || null,
      clickId: data.clickid || null,
      rawData: data as Record<string, string>,
    };
  }

  /**
   * Save attribution to storage
   */
  private async saveAttribution(attribution: AttributionData): Promise<void> {
    try {
      await AsyncStorage.setItem(
        STORAGE_KEYS.APPSFLYER_ATTRIBUTION,
        JSON.stringify(attribution)
      );
    } catch (error) {
      console.error('[AppsFlyer] Error saving attribution:', error);
    }
  }

  /**
   * Save UID to storage
   */
  private async saveUid(uid: string): Promise<void> {
    try {
      await AsyncStorage.setItem(STORAGE_KEYS.APPSFLYER_UID, uid);
    } catch (error) {
      console.error('[AppsFlyer] Error saving UID:', error);
    }
  }

  /**
   * Load stored attribution
   */
  private async loadStoredAttribution(): Promise<void> {
    try {
      const [attrJson, uid] = await Promise.all([
        AsyncStorage.getItem(STORAGE_KEYS.APPSFLYER_ATTRIBUTION),
        AsyncStorage.getItem(STORAGE_KEYS.APPSFLYER_UID),
      ]);

      if (attrJson) {
        this.attribution = JSON.parse(attrJson);
      }
      if (uid) {
        this.uid = uid;
      }
    } catch (error) {
      console.error('[AppsFlyer] Error loading stored data:', error);
    }
  }

  /**
   * Debug log
   */
  private log(message: string): void {
    if (this.debug) {
      console.log(`[AppsFlyer] ${message}`);
    }
  }
}

// Export singleton
export const appsFlyerIntegration = new AppsFlyerIntegration();
export default appsFlyerIntegration;
