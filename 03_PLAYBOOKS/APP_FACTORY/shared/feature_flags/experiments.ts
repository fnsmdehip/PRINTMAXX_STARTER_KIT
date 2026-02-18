/**
 * Experiments
 *
 * A/B test assignment, tracking, and result logging.
 */

import type { FlagName } from './flags';
import type { UserAttributes } from './types';
import { featureFlagService } from './FeatureFlagService';

// Experiment variant type
export interface ExperimentVariant {
  id: string;
  name: string;
  weight: number;
  payload?: Record<string, unknown>;
}

// Experiment definition
export interface Experiment {
  id: string;
  name: string;
  description: string;
  hypothesis: string;
  primaryMetric: string;
  secondaryMetrics?: string[];
  variants: ExperimentVariant[];
  active: boolean;
  startDate: string;
  endDate?: string;
  targetAudience?: AudienceFilter;
  minimumSampleSize?: number;
  owner: string;
}

// Audience targeting filter
export interface AudienceFilter {
  include?: Partial<UserAttributes>;
  exclude?: Partial<UserAttributes>;
  percentage?: number;
}

// Experiment assignment
export interface ExperimentAssignment {
  experimentId: string;
  variantId: string;
  variantName: string;
  assignedAt: number;
  userId: string;
  payload?: Record<string, unknown>;
}

// Experiment result event
export interface ExperimentEvent {
  experimentId: string;
  variantId: string;
  eventType: 'exposure' | 'conversion' | 'custom';
  eventName: string;
  value?: number;
  metadata?: Record<string, unknown>;
  timestamp: number;
  userId: string;
  sessionId?: string;
}

// Experiment analytics summary
export interface ExperimentSummary {
  experimentId: string;
  totalExposures: number;
  variantStats: Record<
    string,
    {
      exposures: number;
      conversions: number;
      conversionRate: number;
      averageValue?: number;
    }
  >;
  significance?: number;
  winner?: string;
}

// Storage interface for experiment data
interface ExperimentStorage {
  getAssignment(experimentId: string): ExperimentAssignment | null;
  setAssignment(assignment: ExperimentAssignment): void;
  getAllAssignments(): ExperimentAssignment[];
  clearAssignments(): void;
}

// In-memory storage implementation
class MemoryExperimentStorage implements ExperimentStorage {
  private assignments: Map<string, ExperimentAssignment> = new Map();

  getAssignment(experimentId: string): ExperimentAssignment | null {
    return this.assignments.get(experimentId) ?? null;
  }

  setAssignment(assignment: ExperimentAssignment): void {
    this.assignments.set(assignment.experimentId, assignment);
  }

  getAllAssignments(): ExperimentAssignment[] {
    return Array.from(this.assignments.values());
  }

  clearAssignments(): void {
    this.assignments.clear();
  }
}

// Event tracking callback type
type EventTrackingCallback = (event: ExperimentEvent) => void;

class ExperimentService {
  private static instance: ExperimentService;
  private experiments: Map<string, Experiment> = new Map();
  private storage: ExperimentStorage = new MemoryExperimentStorage();
  private userId: string = '';
  private userAttributes: UserAttributes = {};
  private trackingCallback?: EventTrackingCallback;
  private debug = false;

  private constructor() {}

  static getInstance(): ExperimentService {
    if (!ExperimentService.instance) {
      ExperimentService.instance = new ExperimentService();
    }
    return ExperimentService.instance;
  }

  /**
   * Initialize the experiment service
   */
  initialize(config: {
    userId: string;
    userAttributes?: UserAttributes;
    onTrack?: EventTrackingCallback;
    debug?: boolean;
    storage?: ExperimentStorage;
  }): void {
    this.userId = config.userId;
    this.userAttributes = config.userAttributes ?? {};
    this.trackingCallback = config.onTrack;
    this.debug = config.debug ?? false;

    if (config.storage) {
      this.storage = config.storage;
    }

    if (this.debug) {
      console.log('ExperimentService initialized', { userId: this.userId });
    }
  }

  /**
   * Update user context
   */
  setUser(userId: string, attributes?: UserAttributes): void {
    this.userId = userId;
    this.userAttributes = attributes ?? {};
    // Clear assignments when user changes
    this.storage.clearAssignments();
  }

  /**
   * Register an experiment
   */
  registerExperiment(experiment: Experiment): void {
    this.experiments.set(experiment.id, experiment);

    if (this.debug) {
      console.log('Experiment registered:', experiment.id);
    }
  }

  /**
   * Register multiple experiments
   */
  registerExperiments(experiments: Experiment[]): void {
    for (const experiment of experiments) {
      this.registerExperiment(experiment);
    }
  }

  /**
   * Get variant assignment for an experiment
   */
  getVariant(experimentId: string): ExperimentVariant | null {
    const experiment = this.experiments.get(experimentId);

    if (!experiment) {
      if (this.debug) {
        console.warn('Experiment not found:', experimentId);
      }
      return null;
    }

    if (!experiment.active) {
      if (this.debug) {
        console.log('Experiment not active:', experimentId);
      }
      return null;
    }

    // Check audience targeting
    if (!this.isUserEligible(experiment)) {
      if (this.debug) {
        console.log('User not eligible for experiment:', experimentId);
      }
      return null;
    }

    // Check for existing assignment
    const existingAssignment = this.storage.getAssignment(experimentId);
    if (existingAssignment) {
      const variant = experiment.variants.find((v) => v.id === existingAssignment.variantId);
      if (variant) {
        return variant;
      }
    }

    // Assign new variant
    const variant = this.assignVariant(experiment);
    if (variant) {
      const assignment: ExperimentAssignment = {
        experimentId,
        variantId: variant.id,
        variantName: variant.name,
        assignedAt: Date.now(),
        userId: this.userId,
        payload: variant.payload,
      };
      this.storage.setAssignment(assignment);

      // Track exposure
      this.trackExposure(experimentId, variant.id);
    }

    return variant;
  }

  /**
   * Get variant ID only
   */
  getVariantId(experimentId: string): string | null {
    const variant = this.getVariant(experimentId);
    return variant?.id ?? null;
  }

  /**
   * Check if user is in a specific variant
   */
  isInVariant(experimentId: string, variantId: string): boolean {
    const variant = this.getVariant(experimentId);
    return variant?.id === variantId;
  }

  /**
   * Check if user is in control group
   */
  isInControl(experimentId: string): boolean {
    return this.isInVariant(experimentId, 'control');
  }

  /**
   * Get experiment-backed feature flag value
   */
  getExperimentFlag<T>(
    experimentId: string,
    flagKey: string,
    defaultValue: T
  ): T {
    const variant = this.getVariant(experimentId);

    if (!variant?.payload) {
      return defaultValue;
    }

    return (variant.payload[flagKey] as T) ?? defaultValue;
  }

  /**
   * Track an exposure event
   */
  trackExposure(experimentId: string, variantId: string): void {
    this.trackEvent({
      experimentId,
      variantId,
      eventType: 'exposure',
      eventName: 'experiment_exposure',
      timestamp: Date.now(),
      userId: this.userId,
    });
  }

  /**
   * Track a conversion event
   */
  trackConversion(
    experimentId: string,
    eventName: string,
    value?: number,
    metadata?: Record<string, unknown>
  ): void {
    const assignment = this.storage.getAssignment(experimentId);

    if (!assignment) {
      if (this.debug) {
        console.warn('No assignment found for conversion tracking:', experimentId);
      }
      return;
    }

    this.trackEvent({
      experimentId,
      variantId: assignment.variantId,
      eventType: 'conversion',
      eventName,
      value,
      metadata,
      timestamp: Date.now(),
      userId: this.userId,
    });
  }

  /**
   * Track a custom experiment event
   */
  trackCustomEvent(
    experimentId: string,
    eventName: string,
    metadata?: Record<string, unknown>
  ): void {
    const assignment = this.storage.getAssignment(experimentId);

    if (!assignment) {
      return;
    }

    this.trackEvent({
      experimentId,
      variantId: assignment.variantId,
      eventType: 'custom',
      eventName,
      metadata,
      timestamp: Date.now(),
      userId: this.userId,
    });
  }

  /**
   * Get all active experiments for the user
   */
  getActiveExperiments(): Experiment[] {
    return Array.from(this.experiments.values()).filter(
      (exp) => exp.active && this.isUserEligible(exp)
    );
  }

  /**
   * Get all assignments for the user
   */
  getAssignments(): ExperimentAssignment[] {
    return this.storage.getAllAssignments();
  }

  /**
   * Override variant for testing
   */
  overrideVariant(experimentId: string, variantId: string): void {
    const experiment = this.experiments.get(experimentId);
    const variant = experiment?.variants.find((v) => v.id === variantId);

    if (experiment && variant) {
      const assignment: ExperimentAssignment = {
        experimentId,
        variantId: variant.id,
        variantName: variant.name,
        assignedAt: Date.now(),
        userId: this.userId,
        payload: variant.payload,
      };
      this.storage.setAssignment(assignment);

      if (this.debug) {
        console.log('Variant overridden:', experimentId, variantId);
      }
    }
  }

  /**
   * Clear all experiment overrides
   */
  clearOverrides(): void {
    this.storage.clearAssignments();
  }

  // Private helper methods

  private isUserEligible(experiment: Experiment): boolean {
    if (!experiment.targetAudience) {
      return true;
    }

    const { include, exclude, percentage } = experiment.targetAudience;

    // Check percentage-based targeting
    if (percentage !== undefined) {
      const hash = this.hashUserId(this.userId + experiment.id);
      if (hash > percentage) {
        return false;
      }
    }

    // Check include filters
    if (include) {
      for (const [key, value] of Object.entries(include)) {
        if (this.userAttributes[key as keyof UserAttributes] !== value) {
          return false;
        }
      }
    }

    // Check exclude filters
    if (exclude) {
      for (const [key, value] of Object.entries(exclude)) {
        if (this.userAttributes[key as keyof UserAttributes] === value) {
          return false;
        }
      }
    }

    return true;
  }

  private assignVariant(experiment: Experiment): ExperimentVariant | null {
    const { variants } = experiment;

    if (variants.length === 0) {
      return null;
    }

    // Calculate total weight
    const totalWeight = variants.reduce((sum, v) => sum + v.weight, 0);

    // Get deterministic random value based on user ID
    const hash = this.hashUserId(this.userId + experiment.id);
    const randomValue = (hash % 100) / 100;

    // Select variant based on weighted distribution
    let cumulativeWeight = 0;
    for (const variant of variants) {
      cumulativeWeight += variant.weight / totalWeight;
      if (randomValue < cumulativeWeight) {
        return variant;
      }
    }

    // Fallback to first variant
    return variants[0];
  }

  private hashUserId(input: string): number {
    // Simple deterministic hash function
    let hash = 0;
    for (let i = 0; i < input.length; i++) {
      const char = input.charCodeAt(i);
      hash = (hash << 5) - hash + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash);
  }

  private trackEvent(event: ExperimentEvent): void {
    if (this.debug) {
      console.log('Experiment event:', event);
    }

    this.trackingCallback?.(event);
  }
}

// Export singleton instance
export const experimentService = ExperimentService.getInstance();

// Export class for testing
export { ExperimentService };

// Predefined experiments registry
export const EXPERIMENTS = {
  PAYWALL_REDESIGN: 'paywall_redesign',
  ONBOARDING_LENGTH: 'onboarding_length',
  TRIAL_DURATION: 'trial_duration',
  PRICING_TEST: 'pricing_test',
  NOTIFICATION_TIMING: 'notification_timing',
  SOCIAL_PROOF_COPY: 'social_proof_copy',
} as const;

export type ExperimentId = (typeof EXPERIMENTS)[keyof typeof EXPERIMENTS];

// Example experiment definitions
export const EXPERIMENT_DEFINITIONS: Experiment[] = [
  {
    id: EXPERIMENTS.PAYWALL_REDESIGN,
    name: 'Paywall Redesign Test',
    description: 'Test new paywall design against control',
    hypothesis: 'New design will increase conversion by 15%',
    primaryMetric: 'purchase_completed',
    secondaryMetrics: ['paywall_dismissed', 'trial_started'],
    variants: [
      { id: 'control', name: 'Control', weight: 50 },
      { id: 'variant_a', name: 'New Design', weight: 50 },
    ],
    active: true,
    startDate: '2024-01-15',
    owner: 'product',
  },
  {
    id: EXPERIMENTS.TRIAL_DURATION,
    name: 'Trial Duration Test',
    description: 'Test different trial lengths',
    hypothesis: '14-day trial will convert better than 7-day',
    primaryMetric: 'trial_to_paid_conversion',
    variants: [
      { id: 'control', name: '7 Days', weight: 33, payload: { trialDays: 7 } },
      { id: '14_days', name: '14 Days', weight: 34, payload: { trialDays: 14 } },
      { id: '3_days', name: '3 Days', weight: 33, payload: { trialDays: 3 } },
    ],
    active: true,
    startDate: '2024-01-20',
    owner: 'growth',
  },
];

// Helper to integrate experiments with feature flags
export function getExperimentFlagValue<T extends FlagName>(
  experimentId: ExperimentId,
  flagName: T,
  defaultValue: unknown
): unknown {
  // First try experiment variant
  const variant = experimentService.getVariant(experimentId);
  if (variant?.payload?.[flagName] !== undefined) {
    return variant.payload[flagName];
  }

  // Fall back to feature flag
  return featureFlagService.getFlag(flagName, defaultValue as never);
}
