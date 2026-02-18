/**
 * Deep Linking Types
 * Shared types for deep linking and attribution across all apps
 */

/**
 * App identifiers for deep link schemes
 */
export type AppId = 'prayerlock' | 'walktounlock' | 'faithstreak' | 'stepbet';

/**
 * Deep link URL schemes per app
 */
export const DEEP_LINK_SCHEMES: Record<AppId, string> = {
  prayerlock: 'prayerlock',
  walktounlock: 'walktounlock',
  faithstreak: 'faithstreak',
  stepbet: 'stepbet',
} as const;

/**
 * Universal link domains per app
 */
export const UNIVERSAL_LINK_DOMAINS: Record<AppId, string> = {
  prayerlock: 'prayerlock.app',
  walktounlock: 'walktounlock.app',
  faithstreak: 'faithstreak.app',
  stepbet: 'stepbet.app',
} as const;

/**
 * Supported deep link actions
 */
export type DeepLinkAction =
  | 'open'
  | 'share'
  | 'invite'
  | 'challenge'
  | 'reward'
  | 'content'
  | 'streak'
  | 'prayer'
  | 'profile'
  | 'settings'
  | 'premium'
  | 'referral';

/**
 * Parsed deep link data
 */
export interface ParsedDeepLink {
  /** Raw URL string */
  url: string;
  /** Scheme used (custom or https) */
  scheme: string;
  /** Host/domain */
  host: string;
  /** Path segments */
  path: string[];
  /** Query parameters */
  params: Record<string, string>;
  /** Detected action */
  action: DeepLinkAction | null;
  /** Target resource ID if applicable */
  resourceId: string | null;
  /** Attribution data extracted from link */
  attribution: AttributionData | null;
  /** Whether link is valid for this app */
  isValid: boolean;
  /** Error message if invalid */
  error: string | null;
}

/**
 * Attribution data from deep links
 */
export interface AttributionData {
  /** Attribution network (adjust, appsflyer, branch) */
  network: AttributionNetwork | null;
  /** Campaign identifier */
  campaign: string | null;
  /** Ad group identifier */
  adGroup: string | null;
  /** Ad creative identifier */
  creative: string | null;
  /** Channel (facebook, google, tiktok, etc.) */
  channel: string | null;
  /** UTM source */
  utmSource: string | null;
  /** UTM medium */
  utmMedium: string | null;
  /** UTM campaign */
  utmCampaign: string | null;
  /** UTM content */
  utmContent: string | null;
  /** UTM term */
  utmTerm: string | null;
  /** Referrer user ID */
  referrerId: string | null;
  /** Click ID for tracking */
  clickId: string | null;
  /** Raw deep link data */
  rawData: Record<string, string>;
}

/**
 * Supported attribution networks
 */
export type AttributionNetwork = 'adjust' | 'appsflyer' | 'branch' | 'none';

/**
 * Attribution SDK configuration
 */
export interface AttributionConfig {
  /** App identifier */
  appId: AppId;
  /** Primary attribution network */
  primaryNetwork: AttributionNetwork;
  /** Adjust configuration */
  adjust?: AdjustConfig;
  /** AppsFlyer configuration */
  appsflyer?: AppsFlyerConfig;
  /** Branch configuration */
  branch?: BranchConfig;
  /** Enable debug logging */
  debug: boolean;
}

/**
 * Adjust SDK configuration
 */
export interface AdjustConfig {
  /** Adjust app token */
  appToken: string;
  /** Environment (sandbox or production) */
  environment: 'sandbox' | 'production';
  /** Event tokens for tracking */
  eventTokens: {
    install: string;
    purchase: string;
    subscribe: string;
    share: string;
    referral: string;
    [key: string]: string;
  };
  /** Enable deferred deep linking */
  deferredDeepLinkEnabled: boolean;
  /** URL strategy */
  urlStrategy: 'default' | 'china' | 'india';
}

/**
 * AppsFlyer SDK configuration
 */
export interface AppsFlyerConfig {
  /** Dev key */
  devKey: string;
  /** iOS App ID */
  appId: string;
  /** Enable debug mode */
  isDebug: boolean;
  /** OneLink template ID */
  oneLinkId: string;
  /** Time to wait for ATT prompt (iOS) */
  timeToWaitForATTUserAuthorization: number;
}

/**
 * Branch SDK configuration
 */
export interface BranchConfig {
  /** Branch key */
  key: string;
  /** Use test key */
  useTestKey: boolean;
  /** Enable logging */
  enableLogging: boolean;
  /** Default link domain */
  linkDomain: string;
}

/**
 * Deep link route mapping
 */
export interface DeepLinkRoute {
  /** Pattern to match (regex or path template) */
  pattern: string;
  /** Screen name to navigate to */
  screen: string;
  /** Stack/navigator name if nested */
  stack?: string;
  /** Parameter extraction rules */
  params?: Record<string, string>;
  /** Auth required to access */
  authRequired: boolean;
  /** Premium required to access */
  premiumRequired: boolean;
}

/**
 * Deep link event for tracking
 */
export interface DeepLinkEvent {
  /** Event type */
  type: 'received' | 'parsed' | 'routed' | 'failed';
  /** Timestamp */
  timestamp: string;
  /** URL received */
  url: string;
  /** Parsed data */
  parsed: ParsedDeepLink | null;
  /** Route matched */
  route: DeepLinkRoute | null;
  /** Error if failed */
  error: string | null;
  /** Source (cold_start, foreground, background) */
  source: 'cold_start' | 'foreground' | 'background';
}

/**
 * Referral link data
 */
export interface ReferralLinkData {
  /** Referrer user ID */
  referrerId: string;
  /** Referrer display name */
  referrerName: string;
  /** Referral code */
  referralCode: string;
  /** Campaign associated with referral */
  campaign: string | null;
  /** Reward for referrer */
  referrerReward: ReferralReward | null;
  /** Reward for referred user */
  referredReward: ReferralReward | null;
  /** Expiration date */
  expiresAt: string | null;
  /** Generated link URL */
  linkUrl: string;
  /** Short link URL */
  shortLinkUrl: string | null;
}

/**
 * Referral reward configuration
 */
export interface ReferralReward {
  /** Reward type */
  type: 'premium_days' | 'credits' | 'discount_percent' | 'custom';
  /** Reward value */
  value: number;
  /** Display string */
  displayString: string;
}

/**
 * Referral conversion tracking
 */
export interface ReferralConversion {
  /** Referred user ID */
  referredUserId: string;
  /** Referrer user ID */
  referrerId: string;
  /** Referral code used */
  referralCode: string;
  /** Conversion timestamp */
  convertedAt: string;
  /** Install attribution source */
  source: 'deep_link' | 'code_entry' | 'share';
  /** Whether referrer was rewarded */
  referrerRewarded: boolean;
  /** Whether referred user was rewarded */
  referredRewarded: boolean;
}

/**
 * Campaign link template
 */
export interface CampaignLink {
  /** Campaign name */
  campaignName: string;
  /** Platform (facebook, tiktok, google, etc.) */
  platform: string;
  /** Full tracking link */
  link: string;
  /** UTM source */
  utmSource: string;
  /** UTM medium */
  utmMedium: string;
  /** UTM campaign */
  utmCampaign: string;
  /** UTM content */
  utmContent?: string;
  /** UTM term */
  utmTerm?: string;
  /** Start date */
  startDate?: string;
  /** End date */
  endDate?: string;
  /** Notes */
  notes?: string;
}

/**
 * Deep link service configuration
 */
export interface DeepLinkServiceConfig {
  /** App configuration */
  appId: AppId;
  /** Custom scheme (defaults to appId) */
  scheme?: string;
  /** Universal link domain */
  universalLinkDomain?: string;
  /** Route definitions */
  routes: DeepLinkRoute[];
  /** Attribution configuration */
  attribution?: AttributionConfig;
  /** Fallback screen if no route matches */
  fallbackScreen: string;
  /** Enable debug logging */
  debug: boolean;
}

/**
 * Deep link context value for React
 */
export interface DeepLinkContextValue {
  /** Whether service is initialized */
  isInitialized: boolean;
  /** Last processed deep link */
  lastDeepLink: ParsedDeepLink | null;
  /** Pending deep link waiting for auth */
  pendingDeepLink: ParsedDeepLink | null;
  /** Attribution data from install */
  installAttribution: AttributionData | null;
  /** Process a deep link URL */
  processDeepLink: (url: string) => Promise<void>;
  /** Clear pending deep link */
  clearPendingDeepLink: () => void;
  /** Generate a sharing link */
  generateShareLink: (params: ShareLinkParams) => Promise<string>;
  /** Generate a referral link */
  generateReferralLink: (userId: string) => Promise<ReferralLinkData>;
}

/**
 * Parameters for generating share links
 */
export interface ShareLinkParams {
  /** Action/screen to link to */
  action: DeepLinkAction;
  /** Resource ID if applicable */
  resourceId?: string;
  /** Additional parameters */
  params?: Record<string, string>;
  /** Campaign for tracking */
  campaign?: string;
  /** Generate short link */
  shorten?: boolean;
}
