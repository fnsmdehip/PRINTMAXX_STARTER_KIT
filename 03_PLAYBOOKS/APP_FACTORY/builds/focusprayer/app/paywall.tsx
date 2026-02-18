/**
 * Paywall Screen
 * Hard paywall with subscription options
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useUserStore } from '@/stores/userStore';
import {
  getOfferings,
  purchasePackage,
  restorePurchases,
} from '@/services/subscriptionService';
import {
  COLORS,
  MONTHLY_PRICE,
  ANNUAL_PRICE,
  ANNUAL_MONTHLY_EQUIVALENT,
  MONTHLY_PRODUCT_ID,
  ANNUAL_PRODUCT_ID,
} from '@/utils/constants';

interface PlanOption {
  id: string;
  name: string;
  price: string;
  period: string;
  savings?: string;
  monthlyEquivalent?: string;
}

export default function PaywallScreen() {
  const router = useRouter();
  const { updateSubscription, startTrial, trialStart, getTrialDaysRemaining } =
    useUserStore();

  const [selectedPlan, setSelectedPlan] = useState<string>(ANNUAL_PRODUCT_ID);
  const [loading, setLoading] = useState(false);
  const [restoring, setRestoring] = useState(false);

  const plans: PlanOption[] = [
    {
      id: ANNUAL_PRODUCT_ID,
      name: 'Annual',
      price: ANNUAL_PRICE,
      period: 'per year',
      savings: 'Save 58%',
      monthlyEquivalent: ANNUAL_MONTHLY_EQUIVALENT + '/mo',
    },
    {
      id: MONTHLY_PRODUCT_ID,
      name: 'Monthly',
      price: MONTHLY_PRICE,
      period: 'per month',
    },
  ];

  const features = [
    'Block distracting apps until devotion complete',
    'Prayer timer with guided prompts',
    'Daily scripture passages',
    'Streak tracking and statistics',
    'Emergency unlock option',
    'No ads, ever',
  ];

  const hasTrialAvailable = !trialStart;
  const trialDaysRemaining = getTrialDaysRemaining();

  async function handlePurchase() {
    setLoading(true);
    try {
      const success = await purchasePackage(selectedPlan);
      if (success) {
        updateSubscription({
          isSubscribed: true,
          isTrialing: false,
          trialEndsAt: null,
          subscriptionType: selectedPlan.includes('annual') ? 'annual' : 'monthly',
          expiresAt: null, // Would come from RevenueCat
        });
        router.back();
      }
    } catch (error) {
      Alert.alert('Purchase Failed', 'There was an error processing your purchase. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  async function handleRestore() {
    setRestoring(true);
    try {
      const restored = await restorePurchases();
      if (restored) {
        Alert.alert('Success', 'Your purchases have been restored.');
        router.back();
      } else {
        Alert.alert('No Purchases Found', 'We could not find any previous purchases to restore.');
      }
    } catch (error) {
      Alert.alert('Restore Failed', 'There was an error restoring your purchases.');
    } finally {
      setRestoring(false);
    }
  }

  async function handleStartTrial() {
    await startTrial();
    router.back();
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Close Button */}
      <TouchableOpacity style={styles.closeButton} onPress={() => router.back()}>
        <Text style={styles.closeButtonText}>&#10005;</Text>
      </TouchableOpacity>

      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Unlock FocusPrayer</Text>
        <Text style={styles.subtitle}>
          Transform your mornings with consistent prayer and scripture
        </Text>
      </View>

      {/* Features */}
      <View style={styles.featuresContainer}>
        {features.map((feature, index) => (
          <View key={index} style={styles.featureRow}>
            <Text style={styles.featureCheck}>&#10003;</Text>
            <Text style={styles.featureText}>{feature}</Text>
          </View>
        ))}
      </View>

      {/* Plan Selection */}
      <View style={styles.plansContainer}>
        {plans.map((plan) => (
          <TouchableOpacity
            key={plan.id}
            style={[
              styles.planCard,
              selectedPlan === plan.id && styles.planCardSelected,
            ]}
            onPress={() => setSelectedPlan(plan.id)}
            activeOpacity={0.8}
          >
            {plan.savings && (
              <View style={styles.savingsBadge}>
                <Text style={styles.savingsText}>{plan.savings}</Text>
              </View>
            )}
            <View style={styles.planHeader}>
              <View
                style={[
                  styles.radioOuter,
                  selectedPlan === plan.id && styles.radioOuterSelected,
                ]}
              >
                {selectedPlan === plan.id && <View style={styles.radioInner} />}
              </View>
              <Text style={styles.planName}>{plan.name}</Text>
            </View>
            <View style={styles.planPricing}>
              <Text style={styles.planPrice}>{plan.price}</Text>
              <Text style={styles.planPeriod}>{plan.period}</Text>
            </View>
            {plan.monthlyEquivalent && (
              <Text style={styles.planEquivalent}>
                Just {plan.monthlyEquivalent}
              </Text>
            )}
          </TouchableOpacity>
        ))}
      </View>

      {/* Trial Button (if available) */}
      {hasTrialAvailable && (
        <TouchableOpacity
          style={styles.trialButton}
          onPress={handleStartTrial}
          activeOpacity={0.8}
        >
          <Text style={styles.trialButtonText}>Start 3-Day Free Trial</Text>
          <Text style={styles.trialButtonSubtext}>
            No payment required. Full access for 3 days.
          </Text>
        </TouchableOpacity>
      )}

      {/* Subscribe Button */}
      <TouchableOpacity
        style={[styles.subscribeButton, loading && styles.subscribeButtonDisabled]}
        onPress={handlePurchase}
        disabled={loading}
        activeOpacity={0.8}
      >
        {loading ? (
          <ActivityIndicator color={COLORS.surface} />
        ) : (
          <Text style={styles.subscribeButtonText}>
            Subscribe {selectedPlan === ANNUAL_PRODUCT_ID ? 'Annually' : 'Monthly'}
          </Text>
        )}
      </TouchableOpacity>

      {/* Trial remaining notice */}
      {!hasTrialAvailable && trialDaysRemaining > 0 && (
        <Text style={styles.trialRemaining}>
          {trialDaysRemaining} day{trialDaysRemaining !== 1 ? 's' : ''} left in your trial
        </Text>
      )}

      {/* Restore Purchases */}
      <TouchableOpacity
        style={styles.restoreButton}
        onPress={handleRestore}
        disabled={restoring}
      >
        <Text style={styles.restoreText}>
          {restoring ? 'Restoring...' : 'Restore Purchases'}
        </Text>
      </TouchableOpacity>

      {/* Legal Text */}
      <Text style={styles.legalText}>
        Payment will be charged to your App Store account at confirmation of purchase.
        Subscription automatically renews unless auto-renew is turned off at least 24 hours
        before the end of the current period. Your account will be charged for renewal within
        24 hours prior to the end of the current period. You can manage and cancel your
        subscriptions in your App Store account settings.
      </Text>

      {/* Links */}
      <View style={styles.linksContainer}>
        <TouchableOpacity onPress={() => router.push('/terms')}>
          <Text style={styles.linkText}>Terms of Service</Text>
        </TouchableOpacity>
        <Text style={styles.linkDivider}>|</Text>
        <TouchableOpacity onPress={() => router.push('/privacy-policy')}>
          <Text style={styles.linkText}>Privacy Policy</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  content: {
    padding: 20,
    paddingBottom: 40,
  },
  closeButton: {
    position: 'absolute',
    top: 20,
    right: 20,
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: COLORS.disabled,
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 10,
  },
  closeButtonText: {
    fontSize: 16,
    color: COLORS.text,
  },
  header: {
    alignItems: 'center',
    marginTop: 40,
    marginBottom: 32,
  },
  title: {
    fontSize: 28,
    fontWeight: '800',
    color: COLORS.text,
    marginBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 22,
  },
  featuresContainer: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 20,
    marginBottom: 24,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  featureCheck: {
    color: COLORS.success,
    fontSize: 16,
    fontWeight: '600',
    marginRight: 12,
  },
  featureText: {
    fontSize: 15,
    color: COLORS.text,
    flex: 1,
  },
  plansContainer: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 20,
  },
  planCard: {
    flex: 1,
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  planCardSelected: {
    borderColor: COLORS.primary,
  },
  savingsBadge: {
    position: 'absolute',
    top: -10,
    right: 10,
    backgroundColor: COLORS.secondary,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  savingsText: {
    color: COLORS.surface,
    fontSize: 11,
    fontWeight: '700',
  },
  planHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  radioOuter: {
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: COLORS.disabled,
    marginRight: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },
  radioOuterSelected: {
    borderColor: COLORS.primary,
  },
  radioInner: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: COLORS.primary,
  },
  planName: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
  },
  planPricing: {
    marginBottom: 4,
  },
  planPrice: {
    fontSize: 24,
    fontWeight: '800',
    color: COLORS.text,
  },
  planPeriod: {
    fontSize: 13,
    color: COLORS.textSecondary,
  },
  planEquivalent: {
    fontSize: 13,
    color: COLORS.primary,
    fontWeight: '500',
  },
  trialButton: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: COLORS.primary,
    paddingVertical: 16,
    alignItems: 'center',
    marginBottom: 12,
  },
  trialButtonText: {
    color: COLORS.primary,
    fontSize: 18,
    fontWeight: '700',
  },
  trialButtonSubtext: {
    color: COLORS.textSecondary,
    fontSize: 13,
    marginTop: 4,
  },
  subscribeButton: {
    backgroundColor: COLORS.primary,
    borderRadius: 12,
    paddingVertical: 18,
    alignItems: 'center',
    marginBottom: 16,
  },
  subscribeButtonDisabled: {
    opacity: 0.7,
  },
  subscribeButtonText: {
    color: COLORS.surface,
    fontSize: 18,
    fontWeight: '700',
  },
  trialRemaining: {
    textAlign: 'center',
    color: COLORS.secondary,
    fontWeight: '600',
    marginBottom: 16,
  },
  restoreButton: {
    alignItems: 'center',
    paddingVertical: 12,
    marginBottom: 20,
  },
  restoreText: {
    color: COLORS.primary,
    fontSize: 15,
  },
  legalText: {
    fontSize: 11,
    color: COLORS.disabled,
    textAlign: 'center',
    lineHeight: 16,
    marginBottom: 16,
  },
  linksContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  linkText: {
    color: COLORS.textSecondary,
    fontSize: 13,
  },
  linkDivider: {
    color: COLORS.disabled,
    marginHorizontal: 12,
  },
});
