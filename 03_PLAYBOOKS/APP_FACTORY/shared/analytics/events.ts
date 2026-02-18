/**
 * Analytics Event Definitions
 *
 * Centralized event taxonomy for React Native apps.
 * All events are typed for compile-time safety.
 */

// Event Categories
export type EventCategory =
  | 'onboarding'
  | 'feature'
  | 'conversion'
  | 'retention'
  | 'error'
  | 'engagement'
  | 'navigation';

// Priority levels for event importance
export type EventPriority = 'critical' | 'high' | 'medium' | 'low';

// Base event properties present on all events
export interface BaseEventProperties {
  timestamp: string;
  session_id: string;
  user_id?: string;
  app_version: string;
  platform: 'ios' | 'android';
  device_type: string;
}

// Onboarding Events
export interface OnboardingEvents {
  onboarding_started: {
    source: 'organic' | 'paid' | 'referral' | 'unknown';
    campaign_id?: string;
  };
  onboarding_screen_viewed: {
    screen_index: number;
    screen_name: string;
    time_on_previous_screen_ms?: number;
  };
  onboarding_screen_skipped: {
    screen_index: number;
    screen_name: string;
  };
  onboarding_completed: {
    total_screens: number;
    total_time_ms: number;
    screens_skipped: number;
  };
  onboarding_abandoned: {
    last_screen_index: number;
    last_screen_name: string;
    total_time_ms: number;
  };
  permission_requested: {
    permission_type: 'notifications' | 'tracking' | 'camera' | 'photos' | 'location';
    screen_name: string;
  };
  permission_granted: {
    permission_type: 'notifications' | 'tracking' | 'camera' | 'photos' | 'location';
  };
  permission_denied: {
    permission_type: 'notifications' | 'tracking' | 'camera' | 'photos' | 'location';
  };
}

// Feature Usage Events
export interface FeatureEvents {
  feature_discovered: {
    feature_name: string;
    discovery_method: 'organic' | 'tooltip' | 'onboarding' | 'notification';
  };
  feature_used: {
    feature_name: string;
    usage_count: number;
    duration_ms?: number;
  };
  feature_completed: {
    feature_name: string;
    success: boolean;
    duration_ms: number;
  };
  content_created: {
    content_type: string;
    content_length?: number;
    used_template: boolean;
    template_id?: string;
  };
  content_saved: {
    content_type: string;
    save_location: 'local' | 'cloud' | 'export';
  };
  content_shared: {
    content_type: string;
    share_destination: string;
  };
  search_performed: {
    query_length: number;
    results_count: number;
    filters_applied: string[];
  };
  settings_changed: {
    setting_name: string;
    old_value: string;
    new_value: string;
  };
}

// Conversion Events
export interface ConversionEvents {
  paywall_viewed: {
    paywall_id: string;
    trigger: 'feature_gate' | 'settings' | 'onboarding' | 'prompt' | 'deeplink';
    products_shown: string[];
  };
  paywall_dismissed: {
    paywall_id: string;
    time_on_paywall_ms: number;
    scroll_depth_percent: number;
  };
  product_selected: {
    product_id: string;
    product_type: 'subscription' | 'lifetime' | 'consumable';
    price: number;
    currency: string;
  };
  trial_started: {
    product_id: string;
    trial_duration_days: number;
    paywall_id: string;
  };
  purchase_initiated: {
    product_id: string;
    price: number;
    currency: string;
  };
  purchase_completed: {
    product_id: string;
    price: number;
    currency: string;
    is_trial: boolean;
    transaction_id: string;
  };
  purchase_failed: {
    product_id: string;
    error_code: string;
    error_message: string;
  };
  purchase_restored: {
    product_id: string;
    original_purchase_date: string;
  };
  subscription_renewed: {
    product_id: string;
    renewal_count: number;
    price: number;
    currency: string;
  };
  subscription_cancelled: {
    product_id: string;
    cancellation_reason?: string;
    days_until_expiry: number;
  };
  refund_requested: {
    product_id: string;
    transaction_id: string;
    reason?: string;
  };
}

// Retention Events
export interface RetentionEvents {
  app_opened: {
    open_type: 'cold' | 'warm' | 'notification' | 'deeplink';
    days_since_last_open: number;
    notification_id?: string;
    deeplink_path?: string;
  };
  app_backgrounded: {
    session_duration_ms: number;
    screens_visited: number;
    actions_taken: number;
  };
  session_started: {
    session_number: number;
    days_since_install: number;
    is_first_session_today: boolean;
  };
  session_ended: {
    duration_ms: number;
    screens_visited: number;
    features_used: string[];
    events_count: number;
  };
  streak_achieved: {
    streak_type: string;
    streak_count: number;
    previous_best: number;
  };
  streak_broken: {
    streak_type: string;
    streak_count: number;
    days_missed: number;
  };
  milestone_reached: {
    milestone_type: string;
    milestone_value: number;
    days_to_achieve: number;
  };
  notification_received: {
    notification_id: string;
    notification_type: string;
    is_app_active: boolean;
  };
  notification_opened: {
    notification_id: string;
    notification_type: string;
    time_to_open_ms: number;
  };
  notification_dismissed: {
    notification_id: string;
    notification_type: string;
  };
  widget_interaction: {
    widget_type: string;
    action: string;
  };
}

// Error Events
export interface ErrorEvents {
  error_occurred: {
    error_type: 'crash' | 'network' | 'validation' | 'permission' | 'unknown';
    error_code: string;
    error_message: string;
    screen_name: string;
    stack_trace?: string;
  };
  network_error: {
    endpoint: string;
    status_code: number;
    error_message: string;
    retry_count: number;
  };
  validation_error: {
    field_name: string;
    validation_type: string;
    error_message: string;
  };
  crash_detected: {
    crash_type: string;
    screen_name: string;
    previous_events: string[];
  };
}

// Engagement Events
export interface EngagementEvents {
  rating_prompt_shown: {
    trigger: string;
    session_count: number;
    days_since_install: number;
  };
  rating_submitted: {
    rating: number;
    trigger: string;
  };
  rating_dismissed: {
    trigger: string;
  };
  feedback_submitted: {
    feedback_type: 'bug' | 'feature' | 'general';
    feedback_length: number;
    includes_screenshot: boolean;
  };
  share_app_tapped: {
    source: string;
  };
  referral_code_generated: {
    code: string;
  };
  referral_code_used: {
    code: string;
    referrer_id: string;
  };
}

// Navigation Events
export interface NavigationEvents {
  screen_viewed: {
    screen_name: string;
    screen_class: string;
    previous_screen?: string;
    navigation_method: 'tap' | 'swipe' | 'deeplink' | 'notification';
  };
  tab_changed: {
    from_tab: string;
    to_tab: string;
  };
  modal_opened: {
    modal_name: string;
    trigger: string;
  };
  modal_closed: {
    modal_name: string;
    action_taken?: string;
    time_open_ms: number;
  };
  deeplink_opened: {
    path: string;
    params: Record<string, string>;
    source: string;
  };
}

// Combined event map
export interface AnalyticsEventMap
  extends OnboardingEvents,
    FeatureEvents,
    ConversionEvents,
    RetentionEvents,
    ErrorEvents,
    EngagementEvents,
    NavigationEvents {}

// Event names type
export type AnalyticsEventName = keyof AnalyticsEventMap;

// Event with properties
export type AnalyticsEvent<T extends AnalyticsEventName> = {
  name: T;
  properties: AnalyticsEventMap[T] & Partial<BaseEventProperties>;
  category: EventCategory;
  priority: EventPriority;
};

// Event metadata for documentation and validation
export const EVENT_METADATA: Record<
  AnalyticsEventName,
  { category: EventCategory; priority: EventPriority; description: string }
> = {
  // Onboarding
  onboarding_started: {
    category: 'onboarding',
    priority: 'critical',
    description: 'User begins onboarding flow',
  },
  onboarding_screen_viewed: {
    category: 'onboarding',
    priority: 'high',
    description: 'User views an onboarding screen',
  },
  onboarding_screen_skipped: {
    category: 'onboarding',
    priority: 'medium',
    description: 'User skips an onboarding screen',
  },
  onboarding_completed: {
    category: 'onboarding',
    priority: 'critical',
    description: 'User completes onboarding flow',
  },
  onboarding_abandoned: {
    category: 'onboarding',
    priority: 'critical',
    description: 'User abandons onboarding flow',
  },
  permission_requested: {
    category: 'onboarding',
    priority: 'high',
    description: 'App requests a permission',
  },
  permission_granted: {
    category: 'onboarding',
    priority: 'high',
    description: 'User grants a permission',
  },
  permission_denied: {
    category: 'onboarding',
    priority: 'high',
    description: 'User denies a permission',
  },

  // Feature
  feature_discovered: {
    category: 'feature',
    priority: 'medium',
    description: 'User discovers a feature for the first time',
  },
  feature_used: {
    category: 'feature',
    priority: 'high',
    description: 'User uses a feature',
  },
  feature_completed: {
    category: 'feature',
    priority: 'high',
    description: 'User completes a feature action',
  },
  content_created: {
    category: 'feature',
    priority: 'high',
    description: 'User creates content',
  },
  content_saved: {
    category: 'feature',
    priority: 'medium',
    description: 'User saves content',
  },
  content_shared: {
    category: 'feature',
    priority: 'high',
    description: 'User shares content',
  },
  search_performed: {
    category: 'feature',
    priority: 'medium',
    description: 'User performs a search',
  },
  settings_changed: {
    category: 'feature',
    priority: 'low',
    description: 'User changes a setting',
  },

  // Conversion
  paywall_viewed: {
    category: 'conversion',
    priority: 'critical',
    description: 'User views a paywall',
  },
  paywall_dismissed: {
    category: 'conversion',
    priority: 'critical',
    description: 'User dismisses a paywall',
  },
  product_selected: {
    category: 'conversion',
    priority: 'critical',
    description: 'User selects a product on paywall',
  },
  trial_started: {
    category: 'conversion',
    priority: 'critical',
    description: 'User starts a free trial',
  },
  purchase_initiated: {
    category: 'conversion',
    priority: 'critical',
    description: 'User initiates purchase',
  },
  purchase_completed: {
    category: 'conversion',
    priority: 'critical',
    description: 'User completes purchase',
  },
  purchase_failed: {
    category: 'conversion',
    priority: 'critical',
    description: 'Purchase fails',
  },
  purchase_restored: {
    category: 'conversion',
    priority: 'high',
    description: 'User restores purchases',
  },
  subscription_renewed: {
    category: 'conversion',
    priority: 'critical',
    description: 'Subscription renews',
  },
  subscription_cancelled: {
    category: 'conversion',
    priority: 'critical',
    description: 'Subscription cancelled',
  },
  refund_requested: {
    category: 'conversion',
    priority: 'critical',
    description: 'User requests refund',
  },

  // Retention
  app_opened: {
    category: 'retention',
    priority: 'critical',
    description: 'App is opened',
  },
  app_backgrounded: {
    category: 'retention',
    priority: 'high',
    description: 'App goes to background',
  },
  session_started: {
    category: 'retention',
    priority: 'critical',
    description: 'New session starts',
  },
  session_ended: {
    category: 'retention',
    priority: 'critical',
    description: 'Session ends',
  },
  streak_achieved: {
    category: 'retention',
    priority: 'high',
    description: 'User achieves a streak',
  },
  streak_broken: {
    category: 'retention',
    priority: 'high',
    description: 'User breaks a streak',
  },
  milestone_reached: {
    category: 'retention',
    priority: 'high',
    description: 'User reaches a milestone',
  },
  notification_received: {
    category: 'retention',
    priority: 'medium',
    description: 'Push notification received',
  },
  notification_opened: {
    category: 'retention',
    priority: 'high',
    description: 'Push notification opened',
  },
  notification_dismissed: {
    category: 'retention',
    priority: 'medium',
    description: 'Push notification dismissed',
  },
  widget_interaction: {
    category: 'retention',
    priority: 'medium',
    description: 'User interacts with widget',
  },

  // Error
  error_occurred: {
    category: 'error',
    priority: 'critical',
    description: 'Error occurs in app',
  },
  network_error: {
    category: 'error',
    priority: 'high',
    description: 'Network request fails',
  },
  validation_error: {
    category: 'error',
    priority: 'medium',
    description: 'Validation fails',
  },
  crash_detected: {
    category: 'error',
    priority: 'critical',
    description: 'App crash detected',
  },

  // Engagement
  rating_prompt_shown: {
    category: 'engagement',
    priority: 'high',
    description: 'Rating prompt shown',
  },
  rating_submitted: {
    category: 'engagement',
    priority: 'high',
    description: 'User submits rating',
  },
  rating_dismissed: {
    category: 'engagement',
    priority: 'medium',
    description: 'User dismisses rating prompt',
  },
  feedback_submitted: {
    category: 'engagement',
    priority: 'high',
    description: 'User submits feedback',
  },
  share_app_tapped: {
    category: 'engagement',
    priority: 'medium',
    description: 'User taps share app',
  },
  referral_code_generated: {
    category: 'engagement',
    priority: 'high',
    description: 'Referral code generated',
  },
  referral_code_used: {
    category: 'engagement',
    priority: 'high',
    description: 'Referral code redeemed',
  },

  // Navigation
  screen_viewed: {
    category: 'navigation',
    priority: 'high',
    description: 'User views a screen',
  },
  tab_changed: {
    category: 'navigation',
    priority: 'medium',
    description: 'User changes tab',
  },
  modal_opened: {
    category: 'navigation',
    priority: 'medium',
    description: 'Modal opens',
  },
  modal_closed: {
    category: 'navigation',
    priority: 'medium',
    description: 'Modal closes',
  },
  deeplink_opened: {
    category: 'navigation',
    priority: 'high',
    description: 'Deeplink opened',
  },
};

// Helper to get event metadata
export function getEventMetadata(eventName: AnalyticsEventName) {
  return EVENT_METADATA[eventName];
}

// Helper to filter events by category
export function getEventsByCategory(category: EventCategory): AnalyticsEventName[] {
  return (Object.keys(EVENT_METADATA) as AnalyticsEventName[]).filter(
    (name) => EVENT_METADATA[name].category === category
  );
}

// Helper to filter events by priority
export function getEventsByPriority(priority: EventPriority): AnalyticsEventName[] {
  return (Object.keys(EVENT_METADATA) as AnalyticsEventName[]).filter(
    (name) => EVENT_METADATA[name].priority === priority
  );
}
