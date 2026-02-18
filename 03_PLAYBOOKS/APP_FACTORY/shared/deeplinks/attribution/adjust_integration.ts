/**
 * Adjust SDK Integration
 * Handles Adjust initialization, event tracking, and attribution
 */

import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

import type { AppId, AdjustConfig, AttributionData } from '../types';
import { getAdjustConfig, COMMON_EVENTS, CommonEventType } from './attribution_config';

// Storage keys
const STORAGE_KEYS = {
  ADJUST_ATTRIBUTION: '@adjust_attribution',
  ADJUST_ADID: '@adjust_adid',
} as const;

/**
 * Adjust SDK wrapper interface
 * Matches react-native-adjust SDK structure
 */
interface AdjustSDK {
  create: (config: AdjustConfigSDK) => void;
  trackEvent: (event: AdjustEventSDK) => void;
  setEnabled: (enabled: boolean) => void;
  isEnabled: (callback: (enabled: boolean) => void) => void;
  getAdid: (callback: (adid: string) => void) => void;
  getAttribution: (callback: (attribution: AdjustAttributionSDK) => void) => void;
  addSessionCallbackParameter: (key: string, value: string) => void;
  addSessionPartnerParameter: (key: string, value: string) => void;
  removeSessionCallbackParameter: (key: string) => void;
  removeSessionPartnerParameter: (key: string) => void;
  resetSessionCallbackParameters: () => void;
  resetSessionPartnerParameters: () => void;
  gdprForgetMe: () => void;
  requestTrackingAuthorizationWithCompletionHandler: (
    callback: (status: number) => void
  ) => void;
}

interface AdjustConfigSDK {
  appToken: string;
  environment: string;
  logLevel?: string;
  shouldLaunchDeeplink?: boolean;
  delayStart?: number;
  sendInBackground?: boolean;
  setAttributionCallbackListener?: (attribution: AdjustAttributionSDK) => void;
  setDeferredDeeplinkCallbackListener?: (deeplink: string) => boolean;
  setSessionTrackingSucceededCallbackListener?: (session: unknown) => void;
  setSessionTrackingFailedCallbackListener?: (session: unknown) => void;
  setEventTrackingSucceededCallbackListener?: (event: unknown) => void;
  setEventTrackingFailedCallbackListener?: (event: unknown) => void;
}

interface AdjustEventSDK {
  eventToken: string;
  revenue?: number;
  currency?: string;
  transactionId?: string;
  callbackId?: string;
  callbackParameters?: Record<string, string>;
  partnerParameters?: Record<string, string>;
}

interface AdjustAttributionSDK {
  trackerToken: string;
  trackerName: string;
  network: string;
  campaign: string;
  adgroup: string;
  creative: string;
  clickLabel: string;
  adid: string;
}

// SDK reference (lazy loaded)
let Adjust: AdjustSDK | null = null;
let AdjustConfig: new (appToken: string, environment: string) => AdjustConfigSDK;
let AdjustEvent: new (eventToken: string) => AdjustEventSDK;

/**
 * Load SDK dynamically
 */
async function loadSDK(): Promise<boolean> {
  if (Adjust) return true;

  try {
    const sdk = await import('react-native-adjust');
    Adjust = sdk.Adjust;
    AdjustConfig = sdk.AdjustConfig;
    AdjustEvent = sdk.AdjustEvent;
    return true;
  } catch (error) {
    console.warn('[Adjust] SDK not installed:', error);
    return false;
  }
}

/**
 * Adjust Integration Service
 */
class AdjustIntegration {
  private config: AdjustConfig | null = null;
  private isInitialized = false;
  private attribution: AttributionData | null = null;
  private adid: string | null = null;
  private debug = false;

  /**
   * Initialize Adjust SDK
   */
  async initialize(
    appId: AppId,
    options?: {
      onAttributionChange?: (attribution: AttributionData) => void;
      onDeferredDeepLink?: (url: string) => void;
    }
  ): Promise<boolean> {
    if (this.isInitialized) {
      this.log('Already initialized');
      return true;
    }

    const sdkLoaded = await loadSDK();
    if (!sdkLoaded || !Adjust) {
      console.error('[Adjust] SDK not available');
      return false;
    }

    this.config = getAdjustConfig(appId);
    this.debug = this.config.environment === 'sandbox';

    try {
      // Create SDK config
      const adjustConfig = new AdjustConfig(
        this.config.appToken,
        this.config.environment
      );

      // Set log level
      if (this.debug) {
        (adjustConfig as any).setLogLevel = 'VERBOSE';
      }

      // Enable deferred deep linking
      if (this.config.deferredDeepLinkEnabled) {
        adjustConfig.shouldLaunchDeeplink = true;
        adjustConfig.setDeferredDeeplinkCallbackListener = (deeplink: string) => {
          this.log(`Deferred deep link received: ${deeplink}`);
          options?.onDeferredDeepLink?.(deeplink);
          return true; // Return true to open the deep link
        };
      }

      // Attribution callback
      adjustConfig.setAttributionCallbackListener = (
        attribution: AdjustAttributionSDK
      ) => {
        const parsed = this.parseAttribution(attribution);
        this.attribution = parsed;
        this.saveAttribution(parsed);
        this.log(`Attribution received: ${JSON.stringify(parsed)}`);
        options?.onAttributionChange?.(parsed);
      };

      // Event tracking callbacks for debugging
      if (this.debug) {
        adjustConfig.setEventTrackingSucceededCallbackListener = (event) => {
          this.log(`Event tracked: ${JSON.stringify(event)}`);
        };
        adjustConfig.setEventTrackingFailedCallbackListener = (event) => {
          this.log(`Event failed: ${JSON.stringify(event)}`);
        };
      }

      // Initialize SDK
      Adjust.create(adjustConfig);

      // Load stored attribution
      await this.loadStoredAttribution();

      // Get ADID
      Adjust.getAdid((adid: string) => {
        this.adid = adid;
        this.saveAdid(adid);
        this.log(`ADID: ${adid}`);
      });

      this.isInitialized = true;
      this.log('Initialized successfully');
      return true;
    } catch (error) {
      console.error('[Adjust] Initialization error:', error);
      return false;
    }
  }

  /**
   * Track an event
   */
  trackEvent(
    eventType: CommonEventType | string,
    params?: {
      revenue?: number;
      currency?: string;
      transactionId?: string;
      callbackParams?: Record<string, string>;
      partnerParams?: Record<string, string>;
    }
  ): void {
    if (!this.isInitialized || !Adjust || !this.config) {
      this.log(`Cannot track event - not initialized`);
      return;
    }

    const eventToken = this.config.eventTokens[eventType];
    if (!eventToken) {
      this.log(`No event token for: ${eventType}`);
      return;
    }

    try {
      const event = new AdjustEvent(eventToken);

      // Add revenue if applicable
      if (params?.revenue && params?.currency) {
        event.revenue = params.revenue;
        event.currency = params.currency;
      }

      // Add transaction ID for deduplication
      if (params?.transactionId) {
        event.transactionId = params.transactionId;
      }

      // Add callback parameters
      if (params?.callbackParams) {
        event.callbackParameters = params.callbackParams;
      }

      // Add partner parameters
      if (params?.partnerParams) {
        event.partnerParameters = params.partnerParams;
      }

      Adjust.trackEvent(event);
      this.log(`Tracked event: ${eventType}`);
    } catch (error) {
      console.error(`[Adjust] Error tracking event ${eventType}:`, error);
    }
  }

  /**
   * Track a purchase event
   */
  trackPurchase(params: {
    revenue: number;
    currency: string;
    transactionId: string;
    productId?: string;
  }): void {
    this.trackEvent(COMMON_EVENTS.PURCHASE, {
      revenue: params.revenue,
      currency: params.currency,
      transactionId: params.transactionId,
      partnerParams: params.productId
        ? { product_id: params.productId }
        : undefined,
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
      revenue: params.revenue,
      currency: params.currency,
      transactionId: params.transactionId,
      partnerParams: {
        product_id: params.productId,
        subscription_period: params.subscriptionPeriod || 'monthly',
      },
    });
  }

  /**
   * Add session callback parameter (persists across sessions)
   */
  addSessionParameter(key: string, value: string): void {
    if (!this.isInitialized || !Adjust) return;
    Adjust.addSessionCallbackParameter(key, value);
    this.log(`Added session param: ${key}`);
  }

  /**
   * Add partner parameter
   */
  addPartnerParameter(key: string, value: string): void {
    if (!this.isInitialized || !Adjust) return;
    Adjust.addSessionPartnerParameter(key, value);
  }

  /**
   * Set user ID for tracking
   */
  setUserId(userId: string): void {
    this.addSessionParameter('user_id', userId);
    this.addPartnerParameter('user_id', userId);
  }

  /**
   * Request iOS App Tracking Transparency authorization
   */
  async requestTrackingAuthorization(): Promise<number> {
    if (Platform.OS !== 'ios' || !Adjust) {
      return -1;
    }

    return new Promise((resolve) => {
      Adjust.requestTrackingAuthorizationWithCompletionHandler((status) => {
        this.log(`ATT status: ${status}`);
        resolve(status);
      });
    });
  }

  /**
   * Enable/disable SDK
   */
  setEnabled(enabled: boolean): void {
    if (!Adjust) return;
    Adjust.setEnabled(enabled);
    this.log(`SDK ${enabled ? 'enabled' : 'disabled'}`);
  }

  /**
   * GDPR forget me (right to be forgotten)
   */
  gdprForgetMe(): void {
    if (!Adjust) return;
    Adjust.gdprForgetMe();
    this.log('GDPR forget me called');
  }

  /**
   * Get current attribution
   */
  getAttribution(): AttributionData | null {
    return this.attribution;
  }

  /**
   * Get Adjust device ID
   */
  getAdid(): string | null {
    return this.adid;
  }

  /**
   * Parse SDK attribution to our format
   */
  private parseAttribution(raw: AdjustAttributionSDK): AttributionData {
    return {
      network: 'adjust',
      campaign: raw.campaign || null,
      adGroup: raw.adgroup || null,
      creative: raw.creative || null,
      channel: raw.network || null,
      utmSource: null,
      utmMedium: null,
      utmCampaign: raw.campaign || null,
      utmContent: raw.creative || null,
      utmTerm: null,
      referrerId: null,
      clickId: raw.clickLabel || null,
      rawData: {
        trackerToken: raw.trackerToken,
        trackerName: raw.trackerName,
        network: raw.network,
        campaign: raw.campaign,
        adgroup: raw.adgroup,
        creative: raw.creative,
        clickLabel: raw.clickLabel,
        adid: raw.adid,
      },
    };
  }

  /**
   * Save attribution to storage
   */
  private async saveAttribution(attribution: AttributionData): Promise<void> {
    try {
      await AsyncStorage.setItem(
        STORAGE_KEYS.ADJUST_ATTRIBUTION,
        JSON.stringify(attribution)
      );
    } catch (error) {
      console.error('[Adjust] Error saving attribution:', error);
    }
  }

  /**
   * Save ADID to storage
   */
  private async saveAdid(adid: string): Promise<void> {
    try {
      await AsyncStorage.setItem(STORAGE_KEYS.ADJUST_ADID, adid);
    } catch (error) {
      console.error('[Adjust] Error saving ADID:', error);
    }
  }

  /**
   * Load stored attribution
   */
  private async loadStoredAttribution(): Promise<void> {
    try {
      const [attrJson, adid] = await Promise.all([
        AsyncStorage.getItem(STORAGE_KEYS.ADJUST_ATTRIBUTION),
        AsyncStorage.getItem(STORAGE_KEYS.ADJUST_ADID),
      ]);

      if (attrJson) {
        this.attribution = JSON.parse(attrJson);
      }
      if (adid) {
        this.adid = adid;
      }
    } catch (error) {
      console.error('[Adjust] Error loading stored data:', error);
    }
  }

  /**
   * Debug log
   */
  private log(message: string): void {
    if (this.debug) {
      console.log(`[Adjust] ${message}`);
    }
  }
}

// Export singleton
export const adjustIntegration = new AdjustIntegration();
export default adjustIntegration;
