/**
 * DeepLinkService.ts
 * Core deep link handling service for React Native apps
 * Handles incoming deep links, parses parameters, routes to screens, and tracks attribution
 */

import { Linking, Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

import type {
  AppId,
  ParsedDeepLink,
  AttributionData,
  DeepLinkRoute,
  DeepLinkEvent,
  DeepLinkServiceConfig,
  ShareLinkParams,
  DeepLinkAction,
} from './types';
import { DEEP_LINK_SCHEMES, UNIVERSAL_LINK_DOMAINS } from './types';

// Storage keys
const STORAGE_KEYS = {
  INSTALL_ATTRIBUTION: '@deeplink_install_attribution',
  PENDING_DEEP_LINK: '@deeplink_pending',
  DEEP_LINK_HISTORY: '@deeplink_history',
  FIRST_OPEN_PROCESSED: '@deeplink_first_open_processed',
} as const;

// Maximum history entries to keep
const MAX_HISTORY_ENTRIES = 50;

/**
 * Navigation callback type - implement this to handle navigation
 */
export type NavigationCallback = (
  screen: string,
  params: Record<string, unknown>,
  stack?: string
) => void;

/**
 * Deep Link Service
 * Singleton service for handling all deep link operations
 */
class DeepLinkService {
  private config: DeepLinkServiceConfig | null = null;
  private isInitialized = false;
  private navigationCallback: NavigationCallback | null = null;
  private pendingDeepLink: ParsedDeepLink | null = null;
  private installAttribution: AttributionData | null = null;
  private linkSubscription: { remove: () => void } | null = null;

  /**
   * Initialize the deep link service
   */
  async initialize(config: DeepLinkServiceConfig): Promise<void> {
    if (this.isInitialized) {
      this.log('Service already initialized');
      return;
    }

    this.config = config;
    await this.loadStoredData();
    this.setupLinkListener();
    await this.handleInitialUrl();

    this.isInitialized = true;
    this.log('Deep link service initialized');
  }

  /**
   * Set the navigation callback for routing
   */
  setNavigationCallback(callback: NavigationCallback): void {
    this.navigationCallback = callback;
    this.log('Navigation callback set');

    // Process pending deep link if exists and navigation is now available
    if (this.pendingDeepLink) {
      this.routeDeepLink(this.pendingDeepLink);
    }
  }

  /**
   * Load stored data from AsyncStorage
   */
  private async loadStoredData(): Promise<void> {
    try {
      const [attributionJson, pendingJson] = await Promise.all([
        AsyncStorage.getItem(STORAGE_KEYS.INSTALL_ATTRIBUTION),
        AsyncStorage.getItem(STORAGE_KEYS.PENDING_DEEP_LINK),
      ]);

      if (attributionJson) {
        this.installAttribution = JSON.parse(attributionJson);
        this.log('Loaded install attribution');
      }

      if (pendingJson) {
        this.pendingDeepLink = JSON.parse(pendingJson);
        this.log('Loaded pending deep link');
      }
    } catch (error) {
      console.error('[DeepLink] Error loading stored data:', error);
    }
  }

  /**
   * Set up listener for incoming deep links
   */
  private setupLinkListener(): void {
    // Remove existing subscription if any
    this.linkSubscription?.remove();

    // Listen for deep links when app is in foreground
    this.linkSubscription = Linking.addEventListener('url', ({ url }) => {
      this.log(`Received deep link (foreground): ${url}`);
      this.processUrl(url, 'foreground');
    });
  }

  /**
   * Handle initial URL when app opens
   */
  private async handleInitialUrl(): Promise<void> {
    try {
      const url = await Linking.getInitialURL();

      if (url) {
        this.log(`Initial URL on cold start: ${url}`);
        await this.processUrl(url, 'cold_start');
      }
    } catch (error) {
      console.error('[DeepLink] Error getting initial URL:', error);
    }
  }

  /**
   * Process an incoming URL
   */
  async processUrl(
    url: string,
    source: 'cold_start' | 'foreground' | 'background'
  ): Promise<ParsedDeepLink> {
    const parsed = this.parseUrl(url);
    await this.logEvent({
      type: 'received',
      timestamp: new Date().toISOString(),
      url,
      parsed,
      route: null,
      error: null,
      source,
    });

    // Extract and store attribution if this is a fresh install
    if (parsed.attribution) {
      await this.handleAttribution(parsed.attribution, source);
    }

    // Route the deep link
    if (parsed.isValid) {
      await this.routeDeepLink(parsed);
    } else {
      this.log(`Invalid deep link: ${parsed.error}`);
    }

    return parsed;
  }

  /**
   * Parse a deep link URL
   */
  parseUrl(url: string): ParsedDeepLink {
    try {
      const parsed: ParsedDeepLink = {
        url,
        scheme: '',
        host: '',
        path: [],
        params: {},
        action: null,
        resourceId: null,
        attribution: null,
        isValid: false,
        error: null,
      };

      // Handle different URL formats
      let urlObj: URL;

      // Check if it's a custom scheme
      const customScheme = this.getCustomScheme();
      if (url.startsWith(`${customScheme}://`)) {
        // Convert custom scheme to parseable format
        const httpUrl = url.replace(`${customScheme}://`, 'https://app.local/');
        urlObj = new URL(httpUrl);
        parsed.scheme = customScheme;
        parsed.host = 'app';
      } else {
        urlObj = new URL(url);
        parsed.scheme = urlObj.protocol.replace(':', '');
        parsed.host = urlObj.hostname;
      }

      // Extract path segments
      parsed.path = urlObj.pathname
        .split('/')
        .filter((segment) => segment.length > 0);

      // Extract query parameters
      urlObj.searchParams.forEach((value, key) => {
        parsed.params[key] = value;
      });

      // Determine action from path
      parsed.action = this.extractAction(parsed.path);

      // Extract resource ID
      parsed.resourceId = this.extractResourceId(parsed.path, parsed.params);

      // Extract attribution data
      parsed.attribution = this.extractAttribution(parsed.params);

      // Validate the link
      const validationError = this.validateLink(parsed);
      parsed.isValid = validationError === null;
      parsed.error = validationError;

      return parsed;
    } catch (error) {
      return {
        url,
        scheme: '',
        host: '',
        path: [],
        params: {},
        action: null,
        resourceId: null,
        attribution: null,
        isValid: false,
        error: `Failed to parse URL: ${error instanceof Error ? error.message : 'Unknown error'}`,
      };
    }
  }

  /**
   * Extract action from path segments
   */
  private extractAction(path: string[]): DeepLinkAction | null {
    const actionMap: Record<string, DeepLinkAction> = {
      open: 'open',
      share: 'share',
      invite: 'invite',
      challenge: 'challenge',
      reward: 'reward',
      content: 'content',
      streak: 'streak',
      prayer: 'prayer',
      profile: 'profile',
      settings: 'settings',
      premium: 'premium',
      referral: 'referral',
    };

    for (const segment of path) {
      const action = actionMap[segment.toLowerCase()];
      if (action) return action;
    }

    return null;
  }

  /**
   * Extract resource ID from path and params
   */
  private extractResourceId(
    path: string[],
    params: Record<string, string>
  ): string | null {
    // Check params first
    if (params.id) return params.id;
    if (params.resourceId) return params.resourceId;

    // Check path for ID pattern (after action)
    for (let i = 0; i < path.length - 1; i++) {
      const next = path[i + 1];
      // Check if next segment looks like an ID (alphanumeric, possibly with dashes)
      if (/^[a-zA-Z0-9_-]+$/.test(next) && next.length > 5) {
        return next;
      }
    }

    return null;
  }

  /**
   * Extract attribution data from parameters
   */
  private extractAttribution(params: Record<string, string>): AttributionData {
    return {
      network: this.detectNetwork(params),
      campaign: params.campaign || params.c || null,
      adGroup: params.adgroup || params.ad_group || params.ag || null,
      creative: params.creative || params.ad || null,
      channel: params.channel || params.source || null,
      utmSource: params.utm_source || null,
      utmMedium: params.utm_medium || null,
      utmCampaign: params.utm_campaign || null,
      utmContent: params.utm_content || null,
      utmTerm: params.utm_term || null,
      referrerId: params.referrer || params.ref || params.r || null,
      clickId:
        params.click_id ||
        params.gclid ||
        params.fbclid ||
        params.ttclid ||
        null,
      rawData: params,
    };
  }

  /**
   * Detect attribution network from parameters
   */
  private detectNetwork(
    params: Record<string, string>
  ): 'adjust' | 'appsflyer' | 'branch' | 'none' {
    if (params.adjust_tracker || params.adj_tracker) return 'adjust';
    if (params.pid || params.af_status) return 'appsflyer';
    if (params['~feature'] || params['+match_guaranteed']) return 'branch';
    return 'none';
  }

  /**
   * Validate the parsed link
   */
  private validateLink(parsed: ParsedDeepLink): string | null {
    if (!this.config) {
      return 'Service not configured';
    }

    // Check scheme matches
    const validSchemes = [
      this.getCustomScheme(),
      'https',
      'http',
    ];

    if (!validSchemes.includes(parsed.scheme)) {
      return `Invalid scheme: ${parsed.scheme}`;
    }

    // For https links, check domain
    if (parsed.scheme === 'https' || parsed.scheme === 'http') {
      const validDomains = [
        this.config.universalLinkDomain ||
          UNIVERSAL_LINK_DOMAINS[this.config.appId],
        'adj.st', // Adjust
        'app.adjust.com',
        'onelink.me', // AppsFlyer
        'app.link', // Branch
      ];

      const isValidDomain = validDomains.some(
        (domain) =>
          parsed.host === domain || parsed.host.endsWith(`.${domain}`)
      );

      if (!isValidDomain) {
        return `Invalid domain: ${parsed.host}`;
      }
    }

    return null;
  }

  /**
   * Handle attribution data
   */
  private async handleAttribution(
    attribution: AttributionData,
    source: 'cold_start' | 'foreground' | 'background'
  ): Promise<void> {
    // Only store attribution on first open (cold start without existing attribution)
    if (source === 'cold_start' && !this.installAttribution) {
      const isFirstOpen = !(await AsyncStorage.getItem(
        STORAGE_KEYS.FIRST_OPEN_PROCESSED
      ));

      if (isFirstOpen) {
        this.installAttribution = attribution;
        await AsyncStorage.setItem(
          STORAGE_KEYS.INSTALL_ATTRIBUTION,
          JSON.stringify(attribution)
        );
        await AsyncStorage.setItem(STORAGE_KEYS.FIRST_OPEN_PROCESSED, 'true');
        this.log('Stored install attribution');

        // Notify attribution SDKs if configured
        this.sendToAttributionNetwork(attribution);
      }
    }
  }

  /**
   * Send attribution data to configured network
   */
  private sendToAttributionNetwork(attribution: AttributionData): void {
    // This will be handled by individual SDK integrations
    // Emit event for SDK handlers to pick up
    this.log(`Attribution to send: ${JSON.stringify(attribution)}`);
  }

  /**
   * Route a parsed deep link to the appropriate screen
   */
  private async routeDeepLink(parsed: ParsedDeepLink): Promise<void> {
    if (!this.config) {
      this.log('Cannot route - service not configured');
      return;
    }

    // Find matching route
    const matchedRoute = this.findMatchingRoute(parsed);

    if (!matchedRoute) {
      this.log('No matching route found, using fallback');
      await this.logEvent({
        type: 'failed',
        timestamp: new Date().toISOString(),
        url: parsed.url,
        parsed,
        route: null,
        error: 'No matching route',
        source: 'foreground',
      });

      // Navigate to fallback
      this.navigate(this.config.fallbackScreen, {
        deepLinkUrl: parsed.url,
      });
      return;
    }

    // Check auth requirements
    if (matchedRoute.authRequired) {
      // Store as pending until auth is complete
      this.pendingDeepLink = parsed;
      await AsyncStorage.setItem(
        STORAGE_KEYS.PENDING_DEEP_LINK,
        JSON.stringify(parsed)
      );
      this.log('Deep link requires auth, stored as pending');
      return;
    }

    // Check premium requirements
    if (matchedRoute.premiumRequired) {
      // Could store as pending or redirect to paywall
      this.log('Deep link requires premium');
      // For now, store as pending
      this.pendingDeepLink = parsed;
      return;
    }

    // Build navigation params
    const navParams = this.buildNavParams(parsed, matchedRoute);

    await this.logEvent({
      type: 'routed',
      timestamp: new Date().toISOString(),
      url: parsed.url,
      parsed,
      route: matchedRoute,
      error: null,
      source: 'foreground',
    });

    // Navigate
    this.navigate(matchedRoute.screen, navParams, matchedRoute.stack);
  }

  /**
   * Find a matching route for the parsed link
   */
  private findMatchingRoute(parsed: ParsedDeepLink): DeepLinkRoute | null {
    if (!this.config?.routes) return null;

    const pathString = '/' + parsed.path.join('/');

    for (const route of this.config.routes) {
      // Convert route pattern to regex
      const pattern = route.pattern
        .replace(/:([a-zA-Z]+)/g, '([^/]+)') // Convert :param to capture group
        .replace(/\*/g, '.*'); // Convert * to wildcard

      const regex = new RegExp(`^${pattern}$`, 'i');

      if (regex.test(pathString)) {
        return route;
      }
    }

    return null;
  }

  /**
   * Build navigation parameters from parsed link and route
   */
  private buildNavParams(
    parsed: ParsedDeepLink,
    route: DeepLinkRoute
  ): Record<string, unknown> {
    const params: Record<string, unknown> = {
      ...parsed.params,
      _deepLink: true,
      _deepLinkUrl: parsed.url,
    };

    // Extract path params based on route definition
    if (route.params) {
      const pathString = '/' + parsed.path.join('/');
      const pattern = route.pattern.replace(/:([a-zA-Z]+)/g, '(?<$1>[^/]+)');
      const regex = new RegExp(`^${pattern}$`, 'i');
      const match = pathString.match(regex);

      if (match?.groups) {
        Object.entries(match.groups).forEach(([key, value]) => {
          if (route.params?.[key]) {
            params[route.params[key]] = value;
          } else {
            params[key] = value;
          }
        });
      }
    }

    // Add resource ID if present
    if (parsed.resourceId) {
      params.id = parsed.resourceId;
    }

    // Add attribution data
    if (parsed.attribution) {
      params._attribution = parsed.attribution;
    }

    return params;
  }

  /**
   * Navigate to a screen
   */
  private navigate(
    screen: string,
    params: Record<string, unknown>,
    stack?: string
  ): void {
    if (!this.navigationCallback) {
      this.log('Navigation callback not set, queuing navigation');
      return;
    }

    this.navigationCallback(screen, params, stack);
    this.log(`Navigated to ${stack ? `${stack}/${screen}` : screen}`);
  }

  /**
   * Generate a share link
   */
  async generateShareLink(params: ShareLinkParams): Promise<string> {
    if (!this.config) {
      throw new Error('Service not configured');
    }

    const scheme = this.getCustomScheme();
    const domain =
      this.config.universalLinkDomain ||
      UNIVERSAL_LINK_DOMAINS[this.config.appId];

    // Build path
    let path = `/${params.action}`;
    if (params.resourceId) {
      path += `/${params.resourceId}`;
    }

    // Build query string
    const queryParams = new URLSearchParams();
    if (params.params) {
      Object.entries(params.params).forEach(([key, value]) => {
        queryParams.set(key, value);
      });
    }
    if (params.campaign) {
      queryParams.set('campaign', params.campaign);
    }

    const queryString = queryParams.toString();
    const fullPath = queryString ? `${path}?${queryString}` : path;

    // Return universal link format for better compatibility
    const universalLink = `https://${domain}${fullPath}`;

    // If shortening requested, use attribution network shortener
    if (params.shorten) {
      return this.shortenLink(universalLink);
    }

    return universalLink;
  }

  /**
   * Shorten a link using configured attribution network
   */
  private async shortenLink(url: string): Promise<string> {
    // Placeholder - implement with Branch/Adjust/AppsFlyer API
    this.log(`Link shortening requested for: ${url}`);
    return url;
  }

  /**
   * Process a pending deep link after auth
   */
  async processPendingDeepLink(): Promise<boolean> {
    if (!this.pendingDeepLink) {
      return false;
    }

    const pending = this.pendingDeepLink;
    this.pendingDeepLink = null;
    await AsyncStorage.removeItem(STORAGE_KEYS.PENDING_DEEP_LINK);

    await this.routeDeepLink(pending);
    return true;
  }

  /**
   * Clear pending deep link
   */
  async clearPendingDeepLink(): Promise<void> {
    this.pendingDeepLink = null;
    await AsyncStorage.removeItem(STORAGE_KEYS.PENDING_DEEP_LINK);
  }

  /**
   * Get the custom URL scheme
   */
  private getCustomScheme(): string {
    if (!this.config) return '';
    return this.config.scheme || DEEP_LINK_SCHEMES[this.config.appId] || '';
  }

  /**
   * Get install attribution data
   */
  getInstallAttribution(): AttributionData | null {
    return this.installAttribution;
  }

  /**
   * Get pending deep link
   */
  getPendingDeepLink(): ParsedDeepLink | null {
    return this.pendingDeepLink;
  }

  /**
   * Log a deep link event
   */
  private async logEvent(event: DeepLinkEvent): Promise<void> {
    try {
      const historyJson = await AsyncStorage.getItem(
        STORAGE_KEYS.DEEP_LINK_HISTORY
      );
      const history: DeepLinkEvent[] = historyJson
        ? JSON.parse(historyJson)
        : [];

      history.push(event);

      // Trim to max entries
      const trimmed = history.slice(-MAX_HISTORY_ENTRIES);

      await AsyncStorage.setItem(
        STORAGE_KEYS.DEEP_LINK_HISTORY,
        JSON.stringify(trimmed)
      );
    } catch (error) {
      console.error('[DeepLink] Error logging event:', error);
    }
  }

  /**
   * Get deep link history
   */
  async getHistory(): Promise<DeepLinkEvent[]> {
    try {
      const historyJson = await AsyncStorage.getItem(
        STORAGE_KEYS.DEEP_LINK_HISTORY
      );
      return historyJson ? JSON.parse(historyJson) : [];
    } catch {
      return [];
    }
  }

  /**
   * Log a debug message
   */
  private log(message: string): void {
    if (this.config?.debug) {
      console.log(`[DeepLink] ${message}`);
    }
  }

  /**
   * Clean up resources
   */
  destroy(): void {
    this.linkSubscription?.remove();
    this.linkSubscription = null;
    this.navigationCallback = null;
    this.isInitialized = false;
    this.log('Service destroyed');
  }
}

// Export singleton instance
export const deepLinkService = new DeepLinkService();
export default deepLinkService;
