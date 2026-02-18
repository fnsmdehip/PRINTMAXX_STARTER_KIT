import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  Text,
  SafeAreaView,
  ScrollView,
  Pressable,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { COLORS, SPACING, BORDER_RADIUS } from '../constants/theme';
import { Button } from '../components';
import { useApp } from '../context/AppContext';
import {
  getOfferings,
  purchaseSubscription,
  restorePurchases,
} from '../services/subscriptionService';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { RootStackParamList } from '../constants/types';

interface PaywallScreenProps {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Paywall'>;
}

type PlanType = 'monthly' | 'yearly';

const FEATURES = [
  {
    icon: '\u{1F3AF}',
    title: 'Unlimited Step Goals',
    description: 'Set any step goal from 100 to 10,000+',
  },
  {
    icon: '\u{1F3C6}',
    title: 'All Achievements',
    description: 'Unlock 25+ achievements and badges',
  },
  {
    icon: '\u{1F4C5}',
    title: 'Custom Lock Times',
    description: 'Set when your phone locks and unlocks',
  },
  {
    icon: '\u{1F4CA}',
    title: 'Detailed Analytics',
    description: 'Weekly and monthly step reports',
  },
  {
    icon: '\u{1F525}',
    title: 'Streak Freezes',
    description: 'Protect your streak on rest days',
  },
  {
    icon: '\u{1F46B}',
    title: 'Friends Leaderboard',
    description: 'Compete with friends (coming soon)',
  },
];

export const PaywallScreen: React.FC<PaywallScreenProps> = ({ navigation }) => {
  const { setPremium } = useApp();
  const [selectedPlan, setSelectedPlan] = useState<PlanType>('yearly');
  const [loading, setLoading] = useState(false);
  const [loadingOfferings, setLoadingOfferings] = useState(true);
  const [offerings, setOfferings] = useState<any>(null);

  useEffect(() => {
    const loadOfferings = async () => {
      const result = await getOfferings();
      setOfferings(result.offerings);
      setLoadingOfferings(false);
    };
    loadOfferings();
  }, []);

  const handlePurchase = async () => {
    setLoading(true);

    if (offerings) {
      const packages = offerings.availablePackages || [];
      const targetId = selectedPlan === 'yearly' ? '$rc_annual' : '$rc_monthly';
      const pkg = packages.find((p: any) => p.identifier === targetId) || packages[0];

      if (pkg) {
        const result = await purchaseSubscription(pkg);
        setLoading(false);

        if (result.success) {
          await setPremium(true);
          navigation.goBack();
        } else if (result.error !== 'cancelled') {
          Alert.alert('Purchase Failed', result.error || 'Something went wrong.');
        }
        return;
      }
    }

    // Demo mode fallback when RevenueCat not configured
    setLoading(false);
    Alert.alert(
      'Demo Mode',
      'RevenueCat is not configured yet. Enable premium for testing?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Enable Premium',
          onPress: async () => {
            await setPremium(true);
            navigation.goBack();
          },
        },
      ]
    );
  };

  const handleRestore = async () => {
    setLoading(true);
    const result = await restorePurchases();
    setLoading(false);

    if (result.success) {
      await setPremium(true);
      Alert.alert('Restored', 'Your premium access has been restored.');
      navigation.goBack();
    } else {
      Alert.alert('No Purchases Found', 'We could not find any previous purchases to restore.');
    }
  };

  const monthlyPrice = '$4.99';
  const yearlyPrice = '$29.99';
  const yearlySavings = '50%';

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        <Pressable style={styles.closeButton} onPress={() => navigation.goBack()}>
          <Text style={styles.closeText}>{'\u00D7'}</Text>
        </Pressable>

        <View style={styles.header}>
          <Text style={styles.headerIcon}>{'\u{1F680}'}</Text>
          <Text style={styles.title}>Upgrade to Premium</Text>
          <Text style={styles.subtitle}>
            Walk more. Achieve more. Unlock your full potential.
          </Text>
        </View>

        <View style={styles.featuresSection}>
          {FEATURES.map((feature, index) => (
            <View key={index} style={styles.featureRow}>
              <Text style={styles.featureIcon}>{feature.icon}</Text>
              <View style={styles.featureContent}>
                <Text style={styles.featureTitle}>{feature.title}</Text>
                <Text style={styles.featureDescription}>{feature.description}</Text>
              </View>
              <Text style={styles.checkmark}>{'\u2713'}</Text>
            </View>
          ))}
        </View>

        {loadingOfferings ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="small" color={COLORS.primary} />
            <Text style={styles.loadingText}>Loading plans...</Text>
          </View>
        ) : (
          <View style={styles.plansSection}>
            <Pressable
              style={[
                styles.planCard,
                selectedPlan === 'yearly' && styles.planCardSelected,
              ]}
              onPress={() => setSelectedPlan('yearly')}
            >
              <View style={styles.savingsBadge}>
                <Text style={styles.savingsText}>SAVE {yearlySavings}</Text>
              </View>
              <View style={styles.planHeader}>
                <Text style={styles.planName}>Annual</Text>
                <View
                  style={[
                    styles.radioOuter,
                    selectedPlan === 'yearly' && styles.radioOuterSelected,
                  ]}
                >
                  {selectedPlan === 'yearly' && <View style={styles.radioInner} />}
                </View>
              </View>
              <Text style={styles.planPrice}>{yearlyPrice}</Text>
              <Text style={styles.planPeriod}>per year</Text>
              <Text style={styles.planMonthly}>
                Just {(29.99 / 12).toFixed(2)}/month
              </Text>
            </Pressable>

            <Pressable
              style={[
                styles.planCard,
                selectedPlan === 'monthly' && styles.planCardSelected,
              ]}
              onPress={() => setSelectedPlan('monthly')}
            >
              <View style={styles.planHeader}>
                <Text style={styles.planName}>Monthly</Text>
                <View
                  style={[
                    styles.radioOuter,
                    selectedPlan === 'monthly' && styles.radioOuterSelected,
                  ]}
                >
                  {selectedPlan === 'monthly' && <View style={styles.radioInner} />}
                </View>
              </View>
              <Text style={styles.planPrice}>{monthlyPrice}</Text>
              <Text style={styles.planPeriod}>per month</Text>
            </Pressable>
          </View>
        )}

        <Button
          title={loading ? 'Processing...' : 'Start Premium'}
          onPress={handlePurchase}
          fullWidth
          size="large"
          loading={loading}
          disabled={loading}
        />

        <Pressable
          style={styles.restoreButton}
          onPress={handleRestore}
          disabled={loading}
        >
          <Text style={styles.restoreText}>Restore Purchases</Text>
        </Pressable>

        <View style={styles.legalSection}>
          <Text style={styles.legalText}>
            By subscribing, you agree to our Terms of Service and Privacy Policy.
            Subscriptions automatically renew unless cancelled at least 24 hours
            before the end of the current period. Manage subscriptions in your
            App Store settings.
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

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
    paddingBottom: SPACING.xxl,
  },
  closeButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: COLORS.surface,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  closeText: {
    fontSize: 24,
    color: COLORS.textSecondary,
    marginTop: -2,
  },
  header: {
    alignItems: 'center',
    marginBottom: SPACING.xl,
  },
  headerIcon: {
    fontSize: 64,
    marginBottom: SPACING.md,
  },
  title: {
    fontSize: 28,
    fontWeight: '800',
    color: COLORS.text,
    textAlign: 'center',
    letterSpacing: -0.5,
  },
  subtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginTop: SPACING.xs,
  },
  featuresSection: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: SPACING.sm,
  },
  featureIcon: {
    fontSize: 24,
    marginRight: SPACING.md,
  },
  featureContent: {
    flex: 1,
  },
  featureTitle: {
    fontSize: 15,
    fontWeight: '600',
    color: COLORS.text,
  },
  featureDescription: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginTop: 1,
  },
  checkmark: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.primary,
    marginLeft: SPACING.sm,
  },
  loadingContainer: {
    alignItems: 'center',
    paddingVertical: SPACING.xl,
  },
  loadingText: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginTop: SPACING.sm,
  },
  plansSection: {
    marginBottom: SPACING.lg,
  },
  planCard: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.lg,
    marginBottom: SPACING.sm,
    borderWidth: 2,
    borderColor: 'transparent',
    position: 'relative',
    overflow: 'hidden',
  },
  planCardSelected: {
    borderColor: COLORS.primary,
  },
  savingsBadge: {
    position: 'absolute',
    top: 0,
    right: 0,
    backgroundColor: COLORS.primary,
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.xs,
    borderBottomLeftRadius: BORDER_RADIUS.md,
  },
  savingsText: {
    fontSize: 11,
    fontWeight: '700',
    color: COLORS.background,
    letterSpacing: 0.5,
  },
  planHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  planName: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.text,
  },
  radioOuter: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: COLORS.backgroundLighter,
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
  planPrice: {
    fontSize: 32,
    fontWeight: '800',
    color: COLORS.primary,
    letterSpacing: -1,
  },
  planPeriod: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  planMonthly: {
    fontSize: 13,
    color: COLORS.textMuted,
    marginTop: SPACING.xs,
  },
  restoreButton: {
    alignItems: 'center',
    paddingVertical: SPACING.md,
    marginTop: SPACING.sm,
  },
  restoreText: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textDecorationLine: 'underline',
  },
  legalSection: {
    marginTop: SPACING.lg,
    paddingTop: SPACING.lg,
    borderTopWidth: 1,
    borderTopColor: COLORS.backgroundLighter,
  },
  legalText: {
    fontSize: 11,
    color: COLORS.textMuted,
    textAlign: 'center',
    lineHeight: 16,
  },
});
