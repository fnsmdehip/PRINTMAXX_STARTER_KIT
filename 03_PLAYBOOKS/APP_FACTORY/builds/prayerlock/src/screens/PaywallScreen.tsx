import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  StatusBar,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Button } from '../components';
import { Colors, FAITH_STRINGS } from '../constants';
import { useApp } from '../context/AppContext';
import {
  getOfferings,
  purchaseSubscription,
  restorePurchases,
} from '../services/subscriptionService';

type RootStackParamList = {
  Paywall: undefined;
  Main: undefined;
};

type PaywallScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Paywall'>;
};

type PlanType = 'monthly' | 'yearly';

const FALLBACK_PLANS = {
  monthly: {
    price: '$4.99',
    period: '/month',
    savings: '',
  },
  yearly: {
    price: '$29.99',
    period: '/year',
    savings: 'Save 50%',
  },
};

const FEATURES = [
  {
    title: 'Extended Prayer Times',
    description: '30 and 60 minute sessions',
    free: false,
  },
  {
    title: 'Family Accountability',
    description: "See your family members' streaks",
    free: false,
  },
  {
    title: 'Custom Prayer Prompts',
    description: 'Create your own daily focus',
    free: false,
  },
  {
    title: 'Streak Freezes',
    description: '1 free freeze per week',
    free: false,
  },
  {
    title: 'Ad-Free Experience',
    description: 'No interruptions',
    free: false,
  },
  {
    title: 'Basic Morning Lock',
    description: '5-15 minute sessions',
    free: true,
  },
  {
    title: 'Daily Verses',
    description: '30 rotating verses',
    free: true,
  },
  {
    title: 'Streak Tracking',
    description: 'Track your consistency',
    free: true,
  },
];

export function PaywallScreen({ navigation }: PaywallScreenProps) {
  const { settings, setPremium } = useApp();
  const [selectedPlan, setSelectedPlan] = useState<PlanType>('yearly');
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingOfferings, setIsLoadingOfferings] = useState(true);
  const [offerings, setOfferings] = useState<any>(null);

  const faithStrings = FAITH_STRINGS[settings.faith];

  useEffect(() => {
    const loadOfferings = async () => {
      const result = await getOfferings();
      setOfferings(result.offerings);
      setIsLoadingOfferings(false);
    };
    loadOfferings();
  }, []);

  const getPackageForPlan = (plan: PlanType) => {
    if (!offerings || !offerings.availablePackages) return null;
    const packages = offerings.availablePackages;
    if (plan === 'yearly') {
      return packages.find((p: any) =>
        p.identifier === '$rc_annual' || p.packageType === 'ANNUAL'
      ) || packages[0];
    }
    return packages.find((p: any) =>
      p.identifier === '$rc_monthly' || p.packageType === 'MONTHLY'
    ) || packages[0];
  };

  const getPlanDisplay = (plan: PlanType) => {
    const pkg = getPackageForPlan(plan);
    if (pkg && pkg.product) {
      return {
        price: pkg.product.priceString || FALLBACK_PLANS[plan].price,
        period: plan === 'yearly' ? '/year' : '/month',
        savings: plan === 'yearly' ? 'Save 50%' : '',
      };
    }
    return FALLBACK_PLANS[plan];
  };

  const handlePurchase = async () => {
    setIsLoading(true);

    const pkg = getPackageForPlan(selectedPlan);

    if (pkg) {
      const result = await purchaseSubscription(pkg);
      setIsLoading(false);

      if (result.success) {
        await setPremium(true);
        Alert.alert(
          'Welcome to Pro!',
          'All premium features are now unlocked.',
          [{ text: 'Start Praying', onPress: () => navigation.goBack() }]
        );
      } else if (result.error === 'cancelled') {
        // User cancelled, do nothing
      } else {
        Alert.alert(
          'Purchase Failed',
          result.error || 'Something went wrong. Please try again.',
          [{ text: 'OK' }]
        );
      }
    } else {
      // RevenueCat not configured or no offerings available, activate demo
      await setPremium(true);
      setIsLoading(false);
      Alert.alert(
        'Welcome to Pro!',
        'All premium features are now unlocked.',
        [{ text: 'Start Praying', onPress: () => navigation.goBack() }]
      );
    }
  };

  const handleRestore = async () => {
    setIsLoading(true);
    const result = await restorePurchases();
    setIsLoading(false);

    if (result.success) {
      await setPremium(true);
      Alert.alert(
        'Purchase Restored',
        'Your premium access has been restored.',
        [{ text: 'OK', onPress: () => navigation.goBack() }]
      );
    } else if (result.error === 'not configured') {
      Alert.alert(
        'Not Available',
        'Purchase restoration is not available in this build.',
      );
    } else {
      Alert.alert(
        'No Previous Purchase',
        'We could not find a previous subscription. If you believe this is an error, please contact support.',
      );
    }
  };

  const yearlyPlan = getPlanDisplay('yearly');
  const monthlyPlan = getPlanDisplay('monthly');

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <LinearGradient
        colors={[Colors.gradientStart, Colors.gradientEnd]}
        style={styles.header}
      >
        <TouchableOpacity
          style={styles.closeButton}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.closeText}>Close</Text>
        </TouchableOpacity>

        <Text style={styles.headerTitle}>PrayerLock Pro</Text>
        <Text style={styles.headerSubtitle}>
          Deepen your {settings.faith === 'islam' ? 'salah' : 'prayer'} life with premium features
        </Text>
      </LinearGradient>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {isLoadingOfferings ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="small" color={Colors.primary} />
          </View>
        ) : (
          <View style={styles.plansContainer}>
            <TouchableOpacity
              style={[
                styles.planCard,
                selectedPlan === 'yearly' && styles.selectedPlan,
              ]}
              onPress={() => setSelectedPlan('yearly')}
            >
              {yearlyPlan.savings ? (
                <View style={styles.savingsBadge}>
                  <Text style={styles.savingsText}>{yearlyPlan.savings}</Text>
                </View>
              ) : null}
              <Text style={styles.planTitle}>Annual</Text>
              <View style={styles.priceRow}>
                <Text style={styles.planPrice}>{yearlyPlan.price}</Text>
                <Text style={styles.planPeriod}>{yearlyPlan.period}</Text>
              </View>
              <Text style={styles.planSubtext}>$2.50/month</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.planCard,
                selectedPlan === 'monthly' && styles.selectedPlan,
              ]}
              onPress={() => setSelectedPlan('monthly')}
            >
              <Text style={styles.planTitle}>Monthly</Text>
              <View style={styles.priceRow}>
                <Text style={styles.planPrice}>{monthlyPlan.price}</Text>
                <Text style={styles.planPeriod}>{monthlyPlan.period}</Text>
              </View>
            </TouchableOpacity>
          </View>
        )}

        <View style={styles.featuresContainer}>
          <Text style={styles.featuresTitle}>What's Included</Text>

          {FEATURES.map((feature, index) => (
            <View key={index} style={styles.featureRow}>
              <View
                style={[
                  styles.featureIcon,
                  feature.free ? styles.freeIcon : styles.proIcon,
                ]}
              >
                <Text style={styles.featureCheck}>
                  {feature.free ? '\u2713' : '\u2605'}
                </Text>
              </View>
              <View style={styles.featureInfo}>
                <Text style={styles.featureTitle}>
                  {feature.title}
                  {!feature.free && (
                    <Text style={styles.proBadge}> PRO</Text>
                  )}
                </Text>
                <Text style={styles.featureDescription}>
                  {feature.description}
                </Text>
              </View>
            </View>
          ))}
        </View>

        <View style={styles.ctaContainer}>
          <Button
            title="Start 7-Day Free Trial"
            onPress={handlePurchase}
            size="large"
            loading={isLoading}
          />
          <Text style={styles.trialNote}>
            Free for 7 days, then {selectedPlan === 'yearly' ? yearlyPlan.price : monthlyPlan.price}
            {selectedPlan === 'yearly' ? yearlyPlan.period : monthlyPlan.period}. Cancel anytime.
          </Text>

          <TouchableOpacity
            onPress={handleRestore}
            disabled={isLoading}
            style={styles.restoreButton}
          >
            <Text style={styles.restoreText}>Restore Purchase</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.legalContainer}>
          <Text style={styles.legalText}>
            Payment will be charged to your Apple ID account at confirmation of
            purchase. Subscription automatically renews unless canceled at least
            24 hours before the end of the current period. Your account will be
            charged for renewal within 24 hours prior to the end of the current
            period. You can manage and cancel your subscriptions by going to
            your account settings on the App Store.
          </Text>
          <View style={styles.legalLinks}>
            <TouchableOpacity>
              <Text style={styles.legalLink}>Terms of Service</Text>
            </TouchableOpacity>
            <Text style={styles.legalDivider}>|</Text>
            <TouchableOpacity>
              <Text style={styles.legalLink}>Privacy Policy</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 40,
  },
  closeButton: {
    alignSelf: 'flex-end',
  },
  closeText: {
    color: Colors.white,
    fontSize: 16,
    fontWeight: '500',
  },
  headerTitle: {
    fontSize: 32,
    fontWeight: '700',
    color: Colors.white,
    marginTop: 20,
    textAlign: 'center',
  },
  headerSubtitle: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.8)',
    marginTop: 8,
    textAlign: 'center',
  },
  scrollContent: {
    paddingBottom: 40,
  },
  loadingContainer: {
    paddingVertical: 40,
    alignItems: 'center',
  },
  plansContainer: {
    flexDirection: 'row',
    paddingHorizontal: 20,
    marginTop: -20,
    gap: 12,
  },
  planCard: {
    flex: 1,
    backgroundColor: Colors.white,
    borderRadius: 16,
    padding: 16,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: Colors.border,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  selectedPlan: {
    borderColor: Colors.primary,
    backgroundColor: Colors.white,
  },
  savingsBadge: {
    position: 'absolute',
    top: -10,
    backgroundColor: Colors.success,
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  savingsText: {
    color: Colors.white,
    fontSize: 12,
    fontWeight: '700',
  },
  planTitle: {
    fontSize: 14,
    color: Colors.textSecondary,
    fontWeight: '600',
    marginTop: 8,
  },
  priceRow: {
    flexDirection: 'row',
    alignItems: 'baseline',
    marginTop: 8,
  },
  planPrice: {
    fontSize: 28,
    fontWeight: '700',
    color: Colors.text,
  },
  planPeriod: {
    fontSize: 14,
    color: Colors.textSecondary,
    marginLeft: 2,
  },
  planSubtext: {
    fontSize: 12,
    color: Colors.textSecondary,
    marginTop: 4,
  },
  featuresContainer: {
    paddingHorizontal: 20,
    marginTop: 32,
  },
  featuresTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: Colors.text,
    marginBottom: 20,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  featureIcon: {
    width: 28,
    height: 28,
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
  },
  freeIcon: {
    backgroundColor: Colors.border,
  },
  proIcon: {
    backgroundColor: Colors.primary,
  },
  featureCheck: {
    color: Colors.white,
    fontSize: 14,
    fontWeight: '700',
  },
  featureInfo: {
    flex: 1,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: Colors.text,
  },
  proBadge: {
    fontSize: 10,
    color: Colors.primary,
    fontWeight: '700',
  },
  featureDescription: {
    fontSize: 14,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  ctaContainer: {
    paddingHorizontal: 20,
    marginTop: 32,
  },
  trialNote: {
    textAlign: 'center',
    fontSize: 13,
    color: Colors.textSecondary,
    marginTop: 12,
  },
  restoreButton: {
    alignItems: 'center',
    marginTop: 20,
  },
  restoreText: {
    fontSize: 14,
    color: Colors.primary,
    fontWeight: '500',
  },
  legalContainer: {
    paddingHorizontal: 20,
    marginTop: 32,
  },
  legalText: {
    fontSize: 11,
    color: Colors.textLight,
    lineHeight: 16,
  },
  legalLinks: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 16,
  },
  legalLink: {
    fontSize: 12,
    color: Colors.primary,
  },
  legalDivider: {
    fontSize: 12,
    color: Colors.textLight,
    marginHorizontal: 8,
  },
});
