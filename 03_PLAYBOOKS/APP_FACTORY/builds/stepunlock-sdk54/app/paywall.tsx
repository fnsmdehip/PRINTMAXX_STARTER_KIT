import { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { router } from 'expo-router';

import { COLORS, MONTHLY_PRICE, ANNUAL_PRICE } from '../src/utils/constants';
import { Button } from '../src/components/Button';
import { useUserStore } from '../src/stores/userStore';
import {
  getOfferings,
  purchaseSubscription,
  restorePurchases,
} from '../src/services/subscriptionService';

type PlanType = 'monthly' | 'annual';

export default function PaywallScreen() {
  const [selectedPlan, setSelectedPlan] = useState<PlanType>('annual');
  const [isLoading, setIsLoading] = useState(false);
  const [offerings, setOfferings] = useState<any>(null);

  const { updateSubscription } = useUserStore();

  useEffect(() => {
    loadOfferings();
  }, []);

  const loadOfferings = async () => {
    const result = await getOfferings();
    if (result.offerings) {
      setOfferings(result.offerings);
    }
  };

  const handlePurchase = async () => {
    setIsLoading(true);

    // Get the appropriate package
    const packageId = selectedPlan === 'monthly' ? '$rc_monthly' : '$rc_annual';
    const pkg = offerings?.availablePackages?.find(
      (p: any) => p.identifier === packageId
    );

    if (!pkg) {
      // Fallback: simulate purchase for demo
      updateSubscription({
        isSubscribed: true,
        isInTrial: false,
        expirationDate: new Date(
          Date.now() + (selectedPlan === 'monthly' ? 30 : 365) * 24 * 60 * 60 * 1000
        ).toISOString(),
      });
      setIsLoading(false);
      router.back();
      return;
    }

    const result = await purchaseSubscription(pkg);
    setIsLoading(false);

    if (result.success) {
      updateSubscription({
        isSubscribed: true,
        isInTrial: false,
      });
      router.back();
    }
  };

  const handleRestore = async () => {
    setIsLoading(true);
    const result = await restorePurchases();
    setIsLoading(false);

    if (result.success) {
      updateSubscription({
        isSubscribed: true,
        isInTrial: false,
      });
      router.back();
    }
  };

  const handleClose = () => {
    router.back();
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Close Button */}
        <TouchableOpacity style={styles.closeButton} onPress={handleClose}>
          <Text style={styles.closeButtonText}>x</Text>
        </TouchableOpacity>

        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.emoji}>🚶</Text>
          <Text style={styles.title}>Unlock StepUnlock</Text>
          <Text style={styles.subtitle}>
            Get unlimited access to all features
          </Text>
        </View>

        {/* Features */}
        <View style={styles.features}>
          <FeatureItem text="Block unlimited apps" />
          <FeatureItem text="Unlimited step goals" />
          <FeatureItem text="Detailed progress stats" />
          <FeatureItem text="Streak tracking" />
          <FeatureItem text="Emergency unlock" />
          <FeatureItem text="Priority support" />
        </View>

        {/* Plan Selection */}
        <View style={styles.plans}>
          <TouchableOpacity
            style={[
              styles.planCard,
              selectedPlan === 'annual' && styles.planCardSelected,
            ]}
            onPress={() => setSelectedPlan('annual')}
          >
            {selectedPlan === 'annual' && (
              <View style={styles.bestValueBadge}>
                <Text style={styles.bestValueText}>Best value</Text>
              </View>
            )}
            <Text style={styles.planName}>Annual</Text>
            <Text style={styles.planPrice}>{ANNUAL_PRICE}/year</Text>
            <Text style={styles.planSavings}>Save 58%</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.planCard,
              selectedPlan === 'monthly' && styles.planCardSelected,
            ]}
            onPress={() => setSelectedPlan('monthly')}
          >
            <Text style={styles.planName}>Monthly</Text>
            <Text style={styles.planPrice}>{MONTHLY_PRICE}/month</Text>
            <Text style={styles.planSavings}> </Text>
          </TouchableOpacity>
        </View>

        {/* Purchase Button */}
        <Button
          title={isLoading ? 'Processing...' : 'Continue'}
          onPress={handlePurchase}
          disabled={isLoading}
          size="large"
          style={styles.purchaseButton}
        />

        {/* Restore */}
        <TouchableOpacity onPress={handleRestore} disabled={isLoading}>
          <Text style={styles.restoreLink}>Restore purchases</Text>
        </TouchableOpacity>

        {/* Legal */}
        <Text style={styles.legal}>
          Payment will be charged to your Apple/Google account.
          Subscriptions automatically renew unless cancelled at least
          24 hours before the end of the current period.
        </Text>

        <View style={styles.legalLinks}>
          <TouchableOpacity onPress={() => router.push('/terms')}>
            <Text style={styles.legalLink}>Terms</Text>
          </TouchableOpacity>
          <Text style={styles.legalDot}>*</Text>
          <TouchableOpacity onPress={() => router.push('/privacy-policy')}>
            <Text style={styles.legalLink}>Privacy</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

function FeatureItem({ text }: { text: string }) {
  return (
    <View style={styles.featureItem}>
      <Text style={styles.featureCheck}>✓</Text>
      <Text style={styles.featureText}>{text}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scrollContent: {
    padding: 24,
  },
  closeButton: {
    alignSelf: 'flex-end',
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: COLORS.border,
    justifyContent: 'center',
    alignItems: 'center',
  },
  closeButtonText: {
    fontSize: 24,
    color: COLORS.textSecondary,
    lineHeight: 26,
  },
  header: {
    alignItems: 'center',
    marginVertical: 24,
  },
  emoji: {
    fontSize: 64,
    marginBottom: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
  },
  features: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 20,
    marginBottom: 24,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  featureCheck: {
    fontSize: 16,
    color: COLORS.success,
    marginRight: 12,
    fontWeight: 'bold',
  },
  featureText: {
    fontSize: 16,
    color: COLORS.text,
  },
  plans: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 24,
  },
  planCard: {
    flex: 1,
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: COLORS.border,
  },
  planCardSelected: {
    borderColor: COLORS.primary,
  },
  bestValueBadge: {
    position: 'absolute',
    top: -10,
    backgroundColor: COLORS.primary,
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  bestValueText: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.surface,
  },
  planName: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
    marginTop: 8,
  },
  planPrice: {
    fontSize: 20,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 4,
  },
  planSavings: {
    fontSize: 14,
    color: COLORS.success,
    fontWeight: '500',
  },
  purchaseButton: {
    marginBottom: 16,
  },
  restoreLink: {
    fontSize: 14,
    color: COLORS.primary,
    textAlign: 'center',
    marginBottom: 24,
  },
  legal: {
    fontSize: 12,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 18,
    marginBottom: 12,
  },
  legalLinks: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  legalLink: {
    fontSize: 12,
    color: COLORS.primary,
  },
  legalDot: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginHorizontal: 8,
  },
});
