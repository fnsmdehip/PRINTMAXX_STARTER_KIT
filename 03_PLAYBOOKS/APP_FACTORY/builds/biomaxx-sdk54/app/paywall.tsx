import { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Platform,
} from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { COLORS } from '../src/utils/constants';
import { useSubscriptionStore } from '../src/stores/subscriptionStore';
import {
  getOfferings,
  purchaseSubscription,
  restorePurchases,
} from '../src/services/subscriptionService';

type PlanType = 'monthly' | 'annual';

// ============================================
// BIOMAXX PAYWALL CONFIG
// ============================================

const PAYWALL_CONFIG = {
  headline: 'track your biohacking stack',
  subheadline: 'supplements, sleep, workouts, fasting. one app.',
  features: [
    { icon: 'flask-outline', text: 'unlimited protocol tracking' },
    { icon: 'medical-outline', text: 'supplement stack management' },
    { icon: 'analytics-outline', text: 'correlation insights' },
    { icon: 'moon-outline', text: 'sleep and energy logging' },
    { icon: 'download-outline', text: 'data export (CSV)' },
    { icon: 'build-outline', text: 'custom protocol builder' },
  ],
  monthlyPrice: '$4.99',
  annualPrice: '$29.99',
  annualSavings: 'save 50%',
  trialDays: 7,
  accentColor: COLORS.primary,
  badgeColor: '#FF6B35',
};

// ============================================
// SHARED PAYWALL LOGIC
// ============================================

export default function PaywallScreen() {
  const params = useLocalSearchParams();
  const fromOnboarding = params.from === 'onboarding';

  const [selectedPlan, setSelectedPlan] = useState<PlanType>('annual');
  const [isLoading, setIsLoading] = useState(false);
  const [offerings, setOfferings] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const { activatePremium, startTrial, setHasSeenPaywall, incrementPaywallDismiss } =
    useSubscriptionStore();

  useEffect(() => {
    setHasSeenPaywall(true);
    loadOfferings();
  }, []);

  const loadOfferings = async () => {
    try {
      const result = await getOfferings();
      if (result.offerings) {
        setOfferings(result.offerings);
      }
    } catch (err) {
      // Offerings unavailable (no network or RevenueCat not configured)
      // Paywall still renders in demo mode
    }
  };

  const handlePurchase = async () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    setIsLoading(true);
    setError(null);

    const packageId = selectedPlan === 'monthly' ? '$rc_monthly' : '$rc_annual';
    const pkg = offerings?.availablePackages?.find(
      (p: any) => p.identifier === packageId
    );

    if (!pkg) {
      // Demo mode: simulate purchase when RevenueCat not configured
      const expiresAt = new Date(
        Date.now() +
          (selectedPlan === 'monthly' ? 30 : 365) * 24 * 60 * 60 * 1000
      ).toISOString();

      if (PAYWALL_CONFIG.trialDays) {
        startTrial();
      } else {
        activatePremium(expiresAt);
      }

      setIsLoading(false);
      navigateAfterPurchase();
      return;
    }

    try {
      const result = await purchaseSubscription(pkg);
      if (result.success) {
        const expiresAt = new Date(
          Date.now() +
            (selectedPlan === 'monthly' ? 30 : 365) * 24 * 60 * 60 * 1000
        ).toISOString();
        activatePremium(expiresAt);
        navigateAfterPurchase();
      } else if (result.error === 'cancelled') {
        // User cancelled, do nothing
      } else {
        setError('purchase failed. please try again.');
      }
    } catch (err) {
      setError('something went wrong. please try again.');
    }
    setIsLoading(false);
  };

  const handleRestore = async () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    setIsLoading(true);
    setError(null);

    try {
      const result = await restorePurchases();
      if (result.success) {
        activatePremium(
          new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString()
        );
        navigateAfterPurchase();
      } else {
        setError('no active subscription found.');
      }
    } catch (err) {
      setError('restore failed. please try again.');
    }
    setIsLoading(false);
  };

  const handleClose = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    incrementPaywallDismiss();

    if (fromOnboarding) {
      // Return to onboarding to complete without premium
      router.back();
    } else {
      router.back();
    }
  };

  const navigateAfterPurchase = () => {
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

    if (fromOnboarding) {
      // Return to onboarding - it will detect subscription and complete
      router.back();
    } else {
      router.back();
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Close Button */}
        <TouchableOpacity
          style={styles.closeButton}
          onPress={handleClose}
          hitSlop={{ top: 12, bottom: 12, left: 12, right: 12 }}
        >
          <Ionicons name="close" size={24} color="#666" />
        </TouchableOpacity>

        {/* Trial Badge */}
        {PAYWALL_CONFIG.trialDays && (
          <View style={styles.trialBadge}>
            <Ionicons name="gift" size={18} color={COLORS.accent} />
            <Text style={styles.trialBadgeText}>
              {PAYWALL_CONFIG.trialDays}-DAY FREE TRIAL
            </Text>
          </View>
        )}

        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.headline}>{PAYWALL_CONFIG.headline}</Text>
          <Text style={styles.subheadline}>{PAYWALL_CONFIG.subheadline}</Text>
        </View>

        {/* Features List */}
        <View style={styles.features}>
          {PAYWALL_CONFIG.features.map((feature, index) => (
            <View key={index} style={styles.featureRow}>
              <View style={styles.featureIconContainer}>
                <Ionicons
                  name={feature.icon as any}
                  size={20}
                  color={PAYWALL_CONFIG.accentColor}
                />
              </View>
              <Text style={styles.featureText}>{feature.text}</Text>
            </View>
          ))}
        </View>

        {/* Plan Selection */}
        <View style={styles.plans}>
          {/* Annual Plan (Recommended) */}
          <TouchableOpacity
            style={[
              styles.planCard,
              selectedPlan === 'annual' && styles.planCardSelected,
            ]}
            onPress={() => {
              Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
              setSelectedPlan('annual');
            }}
            activeOpacity={0.8}
          >
            <View style={styles.planBadge}>
              <Text style={styles.planBadgeText}>
                {PAYWALL_CONFIG.annualSavings}
              </Text>
            </View>
            <View style={styles.planContent}>
              <View>
                <Text style={styles.planTitle}>annual</Text>
                <Text style={styles.planPrice}>
                  {PAYWALL_CONFIG.annualPrice}/year
                </Text>
                <Text style={styles.planSubtext}>
                  {`$${(
                    parseFloat(PAYWALL_CONFIG.annualPrice.replace('$', '')) / 12
                  ).toFixed(2)}/month`}
                </Text>
              </View>
              <View
                style={[
                  styles.radioOuter,
                  selectedPlan === 'annual' && styles.radioOuterSelected,
                ]}
              >
                {selectedPlan === 'annual' && (
                  <View style={styles.radioInner} />
                )}
              </View>
            </View>
          </TouchableOpacity>

          {/* Monthly Plan */}
          <TouchableOpacity
            style={[
              styles.planCard,
              selectedPlan === 'monthly' && styles.planCardSelected,
            ]}
            onPress={() => {
              Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
              setSelectedPlan('monthly');
            }}
            activeOpacity={0.8}
          >
            <View style={styles.planContent}>
              <View>
                <Text style={styles.planTitle}>monthly</Text>
                <Text style={styles.planPrice}>
                  {PAYWALL_CONFIG.monthlyPrice}/month
                </Text>
              </View>
              <View
                style={[
                  styles.radioOuter,
                  selectedPlan === 'monthly' && styles.radioOuterSelected,
                ]}
              >
                {selectedPlan === 'monthly' && (
                  <View style={styles.radioInner} />
                )}
              </View>
            </View>
          </TouchableOpacity>
        </View>

        {/* Trial Info */}
        {PAYWALL_CONFIG.trialDays && (
          <Text style={styles.trialInfoText}>
            {`start your ${PAYWALL_CONFIG.trialDays}-day free trial. cancel anytime.`}
          </Text>
        )}

        {/* Error Message */}
        {error && <Text style={styles.errorText}>{error}</Text>}

        {/* Purchase Button */}
        <TouchableOpacity
          style={[styles.purchaseButton, isLoading && styles.purchaseButtonDisabled]}
          onPress={handlePurchase}
          disabled={isLoading}
          activeOpacity={0.8}
        >
          {isLoading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.purchaseButtonText}>
              {PAYWALL_CONFIG.trialDays
                ? 'start free trial'
                : 'continue'}
            </Text>
          )}
        </TouchableOpacity>

        {/* Restore Purchases */}
        <TouchableOpacity
          onPress={handleRestore}
          disabled={isLoading}
          style={styles.restoreButton}
        >
          <Text style={styles.restoreText}>restore purchases</Text>
        </TouchableOpacity>

        {/* Legal */}
        <View style={styles.legal}>
          <Text style={styles.legalText}>
            {PAYWALL_CONFIG.trialDays
              ? `after the ${PAYWALL_CONFIG.trialDays}-day free trial, payment will be charged to your ${
                  Platform.OS === 'ios' ? 'Apple ID' : 'Google Play'
                } account. subscription automatically renews unless auto-renew is turned off at least 24 hours before the end of the current period.`
              : `payment will be charged to your ${
                  Platform.OS === 'ios' ? 'Apple ID' : 'Google Play'
                } account at confirmation of purchase. subscription automatically renews unless auto-renew is turned off at least 24 hours before the end of the current period.`}
          </Text>
          <View style={styles.legalLinks}>
            <TouchableOpacity>
              <Text style={styles.legalLink}>terms of use</Text>
            </TouchableOpacity>
            <Text style={styles.legalSeparator}>|</Text>
            <TouchableOpacity>
              <Text style={styles.legalLink}>privacy policy</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

// ============================================
// STYLES
// ============================================

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scrollContent: {
    padding: 24,
    paddingBottom: 48,
  },
  closeButton: {
    alignSelf: 'flex-end',
    padding: 4,
    marginBottom: 8,
  },
  trialBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: 'rgba(255, 217, 61, 0.15)',
    paddingVertical: 8,
    paddingHorizontal: 14,
    borderRadius: 20,
    alignSelf: 'flex-start',
    marginBottom: 20,
  },
  trialBadgeText: {
    fontSize: 12,
    fontWeight: '700',
    color: COLORS.accent,
    letterSpacing: 1,
  },
  header: {
    marginBottom: 28,
  },
  headline: {
    color: COLORS.text,
    fontSize: 28,
    fontWeight: '700',
    marginBottom: 8,
  },
  subheadline: {
    color: COLORS.textSecondary,
    fontSize: 16,
    lineHeight: 22,
  },
  features: {
    marginBottom: 32,
    gap: 14,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 14,
  },
  featureIconContainer: {
    width: 36,
    height: 36,
    borderRadius: 10,
    backgroundColor: COLORS.surface,
    justifyContent: 'center',
    alignItems: 'center',
  },
  featureText: {
    color: COLORS.text,
    fontSize: 16,
    flex: 1,
  },
  plans: {
    gap: 12,
    marginBottom: 20,
  },
  planCard: {
    borderWidth: 2,
    borderColor: COLORS.border,
    borderRadius: 14,
    padding: 18,
    position: 'relative',
  },
  planCardSelected: {
    borderColor: COLORS.primary,
    backgroundColor: 'rgba(16, 185, 129, 0.08)',
  },
  planBadge: {
    position: 'absolute',
    top: -12,
    right: 16,
    backgroundColor: '#FF6B35',
    borderRadius: 12,
    paddingHorizontal: 10,
    paddingVertical: 4,
  },
  planBadgeText: {
    color: '#fff',
    fontSize: 11,
    fontWeight: '700',
    textTransform: 'uppercase',
  },
  planContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  planTitle: {
    color: COLORS.text,
    fontSize: 17,
    fontWeight: '600',
    marginBottom: 2,
  },
  planPrice: {
    color: COLORS.text,
    fontSize: 22,
    fontWeight: '700',
  },
  planSubtext: {
    color: COLORS.textSecondary,
    fontSize: 13,
    marginTop: 2,
  },
  radioOuter: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: COLORS.border,
    justifyContent: 'center',
    alignItems: 'center',
  },
  radioOuterSelected: {
    borderColor: COLORS.primary,
  },
  radioInner: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: COLORS.primary,
  },
  trialInfoText: {
    color: COLORS.primary,
    fontSize: 14,
    textAlign: 'center',
    marginBottom: 20,
  },
  errorText: {
    color: COLORS.error,
    fontSize: 14,
    textAlign: 'center',
    marginBottom: 12,
  },
  purchaseButton: {
    backgroundColor: COLORS.primary,
    borderRadius: 14,
    paddingVertical: 16,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 12,
  },
  purchaseButtonDisabled: {
    opacity: 0.6,
  },
  purchaseButtonText: {
    color: COLORS.background,
    fontSize: 17,
    fontWeight: '600',
  },
  restoreButton: {
    paddingVertical: 12,
    alignItems: 'center',
  },
  restoreText: {
    color: COLORS.textMuted,
    fontSize: 14,
  },
  legal: {
    marginTop: 16,
  },
  legalText: {
    color: COLORS.textMuted,
    fontSize: 11,
    lineHeight: 16,
    textAlign: 'center',
    marginBottom: 8,
  },
  legalLinks: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 8,
  },
  legalLink: {
    color: COLORS.textSecondary,
    fontSize: 12,
    textDecorationLine: 'underline',
  },
  legalSeparator: {
    color: COLORS.textMuted,
    fontSize: 12,
  },
});
