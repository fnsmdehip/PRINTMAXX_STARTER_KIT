import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  SafeAreaView,
} from 'react-native';
import { COLORS, TYPOGRAPHY, SPACING, PRICING } from '../../utils/constants';
import { useUserStore } from '../../stores/userStore';

interface Props {
  onClose?: () => void;
  onSubscribe?: () => void;
}

type PlanType = 'monthly' | 'annual';

export function PaywallScreen({ onClose, onSubscribe }: Props) {
  const [selectedPlan, setSelectedPlan] = useState<PlanType>('annual');
  const [isLoading, setIsLoading] = useState(false);

  const { setSubscribed, restorePurchases, getTrialDaysRemaining } = useUserStore();
  const trialDaysRemaining = getTrialDaysRemaining();

  const handleSubscribe = async () => {
    setIsLoading(true);
    try {
      // In production, this would integrate with RevenueCat
      // await Purchases.purchasePackage(package);
      setSubscribed(true);
      onSubscribe?.();
    } catch (error) {
      console.error('Purchase error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRestore = async () => {
    setIsLoading(true);
    const restored = await restorePurchases();
    setIsLoading(false);
    if (restored) {
      onSubscribe?.();
    }
  };

  const features = [
    'Unlimited study sessions',
    'App blocking during focus time',
    'Streak tracking and stats',
    'Custom timer durations',
    'Daily and weekly insights',
    'No ads, ever',
  ];

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>Unlock Your Focus</Text>
          <Text style={styles.subtitle}>
            Join thousands of students improving their grades with StudyLock
          </Text>
        </View>

        {/* Trial Badge */}
        {trialDaysRemaining > 0 && (
          <View style={styles.trialBadge}>
            <Text style={styles.trialText}>
              {trialDaysRemaining} days left in trial
            </Text>
          </View>
        )}

        {/* Features */}
        <View style={styles.featuresContainer}>
          {features.map((feature, index) => (
            <View key={index} style={styles.featureRow}>
              <Text style={styles.checkmark}>✓</Text>
              <Text style={styles.featureText}>{feature}</Text>
            </View>
          ))}
        </View>

        {/* Pricing Cards */}
        <View style={styles.plansContainer}>
          {/* Annual Plan */}
          <TouchableOpacity
            style={[
              styles.planCard,
              selectedPlan === 'annual' && styles.planCardSelected,
            ]}
            onPress={() => setSelectedPlan('annual')}
            activeOpacity={0.8}
          >
            <View style={styles.saveBadge}>
              <Text style={styles.saveBadgeText}>BEST VALUE</Text>
            </View>
            <Text style={styles.planName}>Annual</Text>
            <View style={styles.priceRow}>
              <Text style={styles.price}>${PRICING.annual.price}</Text>
              <Text style={styles.period}>/year</Text>
            </View>
            <Text style={styles.perMonth}>
              ${(PRICING.annual.price / 12).toFixed(2)}/month
            </Text>
            <Text style={styles.savings}>Save {PRICING.annual.savings}</Text>
          </TouchableOpacity>

          {/* Monthly Plan */}
          <TouchableOpacity
            style={[
              styles.planCard,
              selectedPlan === 'monthly' && styles.planCardSelected,
            ]}
            onPress={() => setSelectedPlan('monthly')}
            activeOpacity={0.8}
          >
            <Text style={styles.planName}>Monthly</Text>
            <View style={styles.priceRow}>
              <Text style={styles.price}>${PRICING.monthly.price}</Text>
              <Text style={styles.period}>/month</Text>
            </View>
            <Text style={styles.flexibility}>Flexible billing</Text>
          </TouchableOpacity>
        </View>

        {/* Subscribe Button */}
        <TouchableOpacity
          style={[styles.subscribeButton, isLoading && styles.buttonDisabled]}
          onPress={handleSubscribe}
          disabled={isLoading}
          activeOpacity={0.8}
        >
          <Text style={styles.subscribeButtonText}>
            {isLoading ? 'Processing...' : 'Start 7-Day Free Trial'}
          </Text>
        </TouchableOpacity>

        <Text style={styles.trialNote}>
          7 days free, then ${selectedPlan === 'annual' ? PRICING.annual.price : PRICING.monthly.price}/
          {selectedPlan === 'annual' ? 'year' : 'month'}. Cancel anytime.
        </Text>

        {/* Social Proof */}
        <View style={styles.socialProof}>
          <Text style={styles.rating}>★★★★★</Text>
          <Text style={styles.ratingText}>See what students are saying</Text>
        </View>

        {/* Testimonial */}
        <View style={styles.testimonial}>
          <Text style={styles.testimonialText}>
            "My screen time dropped from 6 hours to 2 hours. My grades improved
            significantly. This app changed how I study."
          </Text>
          <Text style={styles.testimonialAuthor}>— Verified User</Text>
        </View>

        {/* Restore Purchases */}
        <TouchableOpacity onPress={handleRestore} style={styles.restoreButton}>
          <Text style={styles.restoreText}>Restore Purchases</Text>
        </TouchableOpacity>

        {/* Terms */}
        <Text style={styles.terms}>
          By subscribing, you agree to our Terms of Service and Privacy Policy.
          Subscriptions auto-renew unless cancelled 24 hours before the end of
          the period.
        </Text>
      </ScrollView>

      {/* Close button */}
      {onClose && (
        <TouchableOpacity style={styles.closeButton} onPress={onClose}>
          <Text style={styles.closeText}>×</Text>
        </TouchableOpacity>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: SPACING.lg,
    paddingTop: SPACING.xl,
  },
  header: {
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  title: {
    ...TYPOGRAPHY.h1,
    color: COLORS.text,
    textAlign: 'center',
  },
  subtitle: {
    ...TYPOGRAPHY.body,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginTop: SPACING.sm,
  },
  trialBadge: {
    backgroundColor: COLORS.warning + '20',
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
    borderRadius: 20,
    alignSelf: 'center',
    marginBottom: SPACING.lg,
  },
  trialText: {
    ...TYPOGRAPHY.bodySmall,
    color: COLORS.warning,
    fontWeight: '600',
  },
  featuresContainer: {
    marginBottom: SPACING.xl,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  checkmark: {
    color: COLORS.secondary,
    fontSize: 18,
    fontWeight: '600',
    marginRight: SPACING.sm,
    width: 24,
  },
  featureText: {
    ...TYPOGRAPHY.body,
    color: COLORS.text,
    flex: 1,
  },
  plansContainer: {
    flexDirection: 'row',
    gap: SPACING.md,
    marginBottom: SPACING.lg,
  },
  planCard: {
    flex: 1,
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.md,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: COLORS.border,
  },
  planCardSelected: {
    borderColor: COLORS.primary,
    backgroundColor: COLORS.primary + '08',
  },
  saveBadge: {
    backgroundColor: COLORS.secondary,
    paddingVertical: 4,
    paddingHorizontal: SPACING.sm,
    borderRadius: 4,
    marginBottom: SPACING.sm,
  },
  saveBadgeText: {
    ...TYPOGRAPHY.caption,
    color: COLORS.surface,
    fontWeight: '700',
  },
  planName: {
    ...TYPOGRAPHY.h3,
    color: COLORS.text,
    marginBottom: SPACING.xs,
  },
  priceRow: {
    flexDirection: 'row',
    alignItems: 'baseline',
  },
  price: {
    ...TYPOGRAPHY.h1,
    color: COLORS.text,
  },
  period: {
    ...TYPOGRAPHY.body,
    color: COLORS.textSecondary,
  },
  perMonth: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textSecondary,
    marginTop: SPACING.xs,
  },
  savings: {
    ...TYPOGRAPHY.caption,
    color: COLORS.secondary,
    fontWeight: '600',
    marginTop: SPACING.xs,
  },
  flexibility: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textSecondary,
    marginTop: SPACING.sm,
  },
  subscribeButton: {
    backgroundColor: COLORS.primary,
    paddingVertical: SPACING.md,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  buttonDisabled: {
    opacity: 0.7,
  },
  subscribeButtonText: {
    ...TYPOGRAPHY.body,
    color: COLORS.surface,
    fontWeight: '700',
  },
  trialNote: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: SPACING.xl,
  },
  socialProof: {
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  rating: {
    fontSize: 20,
    color: COLORS.warning,
  },
  ratingText: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textSecondary,
    marginTop: SPACING.xs,
  },
  testimonial: {
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.lg,
  },
  testimonialText: {
    ...TYPOGRAPHY.bodySmall,
    color: COLORS.text,
    fontStyle: 'italic',
  },
  testimonialAuthor: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textSecondary,
    marginTop: SPACING.sm,
  },
  restoreButton: {
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  restoreText: {
    ...TYPOGRAPHY.bodySmall,
    color: COLORS.primary,
  },
  terms: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textTertiary,
    textAlign: 'center',
    lineHeight: 16,
  },
  closeButton: {
    position: 'absolute',
    top: SPACING.xl,
    right: SPACING.lg,
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: COLORS.surfaceSecondary,
    alignItems: 'center',
    justifyContent: 'center',
  },
  closeText: {
    fontSize: 24,
    color: COLORS.textSecondary,
    lineHeight: 28,
  },
});
