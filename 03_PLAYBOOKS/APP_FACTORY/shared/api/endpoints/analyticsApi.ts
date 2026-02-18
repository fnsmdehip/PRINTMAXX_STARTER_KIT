/**
 * analyticsApi.ts - Analytics and metrics endpoints
 */

import { apiClient } from '../ApiClient';

// ============================================================================
// Types
// ============================================================================

export type TimeRange = '1d' | '7d' | '30d' | '90d' | '1y' | 'all' | 'custom';
export type Granularity = 'hour' | 'day' | 'week' | 'month';

export interface DateRange {
  start: string;
  end: string;
}

export interface TimeSeriesPoint {
  timestamp: string;
  value: number;
}

export interface MetricValue {
  current: number;
  previous: number;
  change: number;
  changePercent: number;
  trend: 'up' | 'down' | 'flat';
}

// ============================================================================
// Dashboard Analytics
// ============================================================================

export interface DashboardOverview {
  totalUsers: MetricValue;
  activeUsers: MetricValue;
  totalRevenue: MetricValue;
  totalContent: MetricValue;
  conversionRate: MetricValue;
  churnRate: MetricValue;
}

export interface DashboardChart {
  label: string;
  data: TimeSeriesPoint[];
  total: number;
  average: number;
}

export interface DashboardResponse {
  overview: DashboardOverview;
  charts: {
    users: DashboardChart;
    revenue: DashboardChart;
    engagement: DashboardChart;
  };
  topContent: {
    id: string;
    title: string;
    views: number;
    engagement: number;
  }[];
  recentActivity: {
    type: string;
    description: string;
    timestamp: string;
  }[];
}

// ============================================================================
// User Analytics
// ============================================================================

export interface UserAnalytics {
  totalUsers: number;
  newUsers: MetricValue;
  activeUsers: MetricValue;
  retention: {
    day1: number;
    day7: number;
    day30: number;
  };
  demographics: {
    countries: { country: string; count: number; percent: number }[];
    devices: { device: string; count: number; percent: number }[];
    platforms: { platform: string; count: number; percent: number }[];
  };
  userGrowth: TimeSeriesPoint[];
  activeUsersTrend: TimeSeriesPoint[];
}

export interface CohortData {
  cohort: string;
  size: number;
  retention: number[];
}

export interface UserCohortAnalytics {
  cohorts: CohortData[];
  periods: string[];
  averageRetention: number[];
}

// ============================================================================
// Content Analytics
// ============================================================================

export interface ContentAnalytics {
  totalViews: MetricValue;
  totalEngagements: MetricValue;
  averageReadTime: MetricValue;
  bounceRate: MetricValue;
  viewsTrend: TimeSeriesPoint[];
  topContent: {
    id: string;
    title: string;
    type: string;
    views: number;
    engagement: number;
    conversionRate: number;
  }[];
  contentByType: {
    type: string;
    count: number;
    views: number;
    engagement: number;
  }[];
  engagementByHour: {
    hour: number;
    views: number;
    engagement: number;
  }[];
}

export interface ContentItemAnalytics {
  views: MetricValue;
  uniqueViews: MetricValue;
  likes: MetricValue;
  comments: MetricValue;
  shares: MetricValue;
  bookmarks: MetricValue;
  averageReadTime: MetricValue;
  scrollDepth: MetricValue;
  viewsTrend: TimeSeriesPoint[];
  trafficSources: {
    source: string;
    count: number;
    percent: number;
  }[];
  referrers: {
    url: string;
    count: number;
  }[];
}

// ============================================================================
// Revenue Analytics
// ============================================================================

export interface RevenueAnalytics {
  totalRevenue: MetricValue;
  mrr: MetricValue;
  arr: MetricValue;
  arpu: MetricValue;
  ltv: MetricValue;
  revenueTrend: TimeSeriesPoint[];
  revenueByPlan: {
    plan: string;
    revenue: number;
    subscribers: number;
    percent: number;
  }[];
  revenueBySource: {
    source: string;
    revenue: number;
    percent: number;
  }[];
  transactions: {
    total: number;
    successful: number;
    failed: number;
    refunded: number;
  };
}

export interface SubscriptionAnalytics {
  totalSubscribers: MetricValue;
  newSubscribers: MetricValue;
  churnedSubscribers: MetricValue;
  churnRate: MetricValue;
  trialConversion: MetricValue;
  subscribersTrend: TimeSeriesPoint[];
  subscribersByPlan: {
    plan: string;
    count: number;
    percent: number;
  }[];
  churnReasons: {
    reason: string;
    count: number;
    percent: number;
  }[];
}

// ============================================================================
// Funnel Analytics
// ============================================================================

export interface FunnelStep {
  name: string;
  count: number;
  conversionRate: number;
  dropoffRate: number;
}

export interface FunnelAnalytics {
  name: string;
  totalEntries: number;
  totalConversions: number;
  overallConversionRate: number;
  steps: FunnelStep[];
  trend: {
    timestamp: string;
    entries: number;
    conversions: number;
  }[];
}

// ============================================================================
// Event Tracking
// ============================================================================

export interface TrackEventRequest {
  name: string;
  properties?: Record<string, unknown>;
  timestamp?: string;
}

export interface TrackScreenViewRequest {
  screenName: string;
  properties?: Record<string, unknown>;
}

export interface TrackUserPropertyRequest {
  properties: Record<string, unknown>;
}

// ============================================================================
// Analytics API Class
// ============================================================================

class AnalyticsApi {
  private readonly basePath = '/analytics';

  // --------------------------------------------------------------------------
  // Dashboard
  // --------------------------------------------------------------------------

  /**
   * Get dashboard overview
   */
  async getDashboard(
    timeRange: TimeRange = '30d',
    dateRange?: DateRange
  ): Promise<DashboardResponse> {
    return apiClient.get(`${this.basePath}/dashboard`, {
      params: {
        timeRange,
        ...dateRange,
      },
    });
  }

  // --------------------------------------------------------------------------
  // User Analytics
  // --------------------------------------------------------------------------

  /**
   * Get user analytics
   */
  async getUserAnalytics(
    timeRange: TimeRange = '30d',
    granularity: Granularity = 'day'
  ): Promise<UserAnalytics> {
    return apiClient.get(`${this.basePath}/users`, {
      params: { timeRange, granularity },
    });
  }

  /**
   * Get cohort analysis
   */
  async getCohortAnalytics(
    cohortPeriod: 'week' | 'month' = 'week',
    retentionPeriod: number = 8
  ): Promise<UserCohortAnalytics> {
    return apiClient.get(`${this.basePath}/users/cohorts`, {
      params: { cohortPeriod, retentionPeriod },
    });
  }

  // --------------------------------------------------------------------------
  // Content Analytics
  // --------------------------------------------------------------------------

  /**
   * Get content analytics
   */
  async getContentAnalytics(
    timeRange: TimeRange = '30d',
    contentType?: string
  ): Promise<ContentAnalytics> {
    return apiClient.get(`${this.basePath}/content`, {
      params: { timeRange, type: contentType },
    });
  }

  /**
   * Get analytics for specific content
   */
  async getContentItemAnalytics(
    contentId: string,
    timeRange: TimeRange = '30d'
  ): Promise<ContentItemAnalytics> {
    return apiClient.get(`${this.basePath}/content/${contentId}`, {
      params: { timeRange },
    });
  }

  // --------------------------------------------------------------------------
  // Revenue Analytics
  // --------------------------------------------------------------------------

  /**
   * Get revenue analytics
   */
  async getRevenueAnalytics(
    timeRange: TimeRange = '30d',
    granularity: Granularity = 'day'
  ): Promise<RevenueAnalytics> {
    return apiClient.get(`${this.basePath}/revenue`, {
      params: { timeRange, granularity },
    });
  }

  /**
   * Get subscription analytics
   */
  async getSubscriptionAnalytics(
    timeRange: TimeRange = '30d'
  ): Promise<SubscriptionAnalytics> {
    return apiClient.get(`${this.basePath}/subscriptions`, {
      params: { timeRange },
    });
  }

  // --------------------------------------------------------------------------
  // Funnel Analytics
  // --------------------------------------------------------------------------

  /**
   * Get funnel analytics
   */
  async getFunnelAnalytics(
    funnelId: string,
    timeRange: TimeRange = '30d'
  ): Promise<FunnelAnalytics> {
    return apiClient.get(`${this.basePath}/funnels/${funnelId}`, {
      params: { timeRange },
    });
  }

  /**
   * Get available funnels
   */
  async getFunnels(): Promise<{ id: string; name: string; description: string }[]> {
    return apiClient.get(`${this.basePath}/funnels`);
  }

  // --------------------------------------------------------------------------
  // Event Tracking
  // --------------------------------------------------------------------------

  /**
   * Track custom event
   */
  async trackEvent(data: TrackEventRequest): Promise<void> {
    return apiClient.post(`${this.basePath}/events`, data);
  }

  /**
   * Track screen view
   */
  async trackScreenView(data: TrackScreenViewRequest): Promise<void> {
    return apiClient.post(`${this.basePath}/screen-views`, data);
  }

  /**
   * Set user properties
   */
  async setUserProperties(data: TrackUserPropertyRequest): Promise<void> {
    return apiClient.post(`${this.basePath}/user-properties`, data);
  }

  /**
   * Track batch events
   */
  async trackBatch(events: TrackEventRequest[]): Promise<void> {
    return apiClient.post(`${this.basePath}/events/batch`, { events });
  }

  // --------------------------------------------------------------------------
  // Real-time Analytics
  // --------------------------------------------------------------------------

  /**
   * Get real-time active users
   */
  async getRealtimeUsers(): Promise<{
    activeUsers: number;
    byScreen: { screen: string; count: number }[];
    byCountry: { country: string; count: number }[];
  }> {
    return apiClient.get(`${this.basePath}/realtime/users`);
  }

  /**
   * Get real-time events
   */
  async getRealtimeEvents(
    limit: number = 50
  ): Promise<{
    events: {
      name: string;
      userId: string;
      timestamp: string;
      properties: Record<string, unknown>;
    }[];
  }> {
    return apiClient.get(`${this.basePath}/realtime/events`, {
      params: { limit },
    });
  }

  // --------------------------------------------------------------------------
  // Export
  // --------------------------------------------------------------------------

  /**
   * Export analytics data
   */
  async exportData(
    type: 'users' | 'content' | 'revenue' | 'events',
    timeRange: TimeRange,
    format: 'csv' | 'json' = 'csv'
  ): Promise<{ downloadUrl: string; expiresAt: string }> {
    return apiClient.post(`${this.basePath}/export`, {
      type,
      timeRange,
      format,
    });
  }
}

// ============================================================================
// Singleton Export
// ============================================================================

export const analyticsApi = new AnalyticsApi();

export default analyticsApi;
