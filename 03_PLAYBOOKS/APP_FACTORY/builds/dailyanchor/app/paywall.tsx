import { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  SafeAreaView,
} from 'react-native';
import { useRouter } from 'expo-router';
import { PremiumFeatureCard } from '../src/components/paywall/PremiumFeatureCard';
import { PricingOption } from '../src/components/paywall/PricingOption';
import { Button } from '../src/components/common';
import { COLORS } from '../src/utils/constants';
import { useSettingsStore } from '../src/store';

const PREMIUM_FEATURES = [
  {
    icon: '\u{1F9D8}',
    title: 'Unlimited habits',
    description: 'Track meditation, fasting, scripture memory, and more',
  },
  {
    icon: '\u{1F4D6}',
    title: 'Reading plans',
    description: 'Follow guided plans for gratitude, peace, and purpose',
  },
  {
    icon: '\u{1F4CA}',
    title: 'Advanced stats',
    description: 'See your progress over weeks and months',
  },
  {
    icon: '\u{1F50A}',
    title: 'Audio devotionals',
    description: 'Listen during your commute or workout',
  },
  {
    icon: '\u{2601}',
    title: 'Cloud sync',
    description: 'Keep your journal backed up and synced',
  },
];

type PricingPlan = 'monthly' | 'yearly';

export default function PaywallScreen() {
  const router = useRouter();
  const [selectedPlan, setSelectedPlan] = useState<PricingPlan>('yearly');
  const [isLoading, setIsLoading] = useState(false);
  const { updateSettings } = useSettingsStore();

  const handleClose = () => {
    router.back();
  };

  const handlePurchase = async () => {
    setIsLoading(true);

    // TODO: Integrate RevenueCat purchase flow
    // For now, simulate a purchase
    try {
      // In production:
      // const purchaserInfo = await Purchases.purchasePackage(selectedPackage);
      // if (purchaserInfo.entitlements.active['premium']) {
      //   updateSettings({ isPremium: true });
      //   router.back();
      // }

      // Simulate delay
      await new Promise((resolve) => setTimeout(resolve, 1500));

      updateSettings({ isPremium: true });
      router.back();
    } catch (error) {
      console.error('Purchase failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRestore = async () => {
    setIsLoading(true);

    try {
      // TODO: Integrate RevenueCat restore
      // const purchaserInfo = await Purchases.restorePurchases();
      // if (purchaserInfo.entitlements.active['premium']) {
      //   updateSettings({ isPremium: true });
      //   router.back();
      // }

      await new Promise((resolve) => setTimeout(resolve, 1000));
    } catch (error) {
      console.error('Restore failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={handleClose} style={styles.closeButton}>
          <Text style={styles.closeText}>{'\u2715'}</Text>
        </TouchableOpacity>
      </View>

      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.hero}>
          <Text style={styles.heroEmoji}>{'\u{2728}'}</Text>
          <Text style={styles.heroTitle}>Unlock DailyAnchor Premium</Text>
          <Text style={styles.heroSubtitle}>
            Go deeper in your faith journey
          </Text>
        </View>

        <View style={styles.features}>
          {PREMIUM_FEATURES.map((feature, index) => (
            <PremiumFeatureCard
              key={index}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
            />
          ))}
        </View>

        <View style={styles.pricing}>
          <Text style={styles.pricingTitle}>Choose your plan</Text>

          <PricingOption
            title="Yearly"
            price="$49.99"
            period="year"
            savings="Save 58% ($70/year)"
            isPopular={true}
            isSelected={selectedPlan === 'yearly'}
            onSelect={() => setSelectedPlan('yearly')}
          />

          <PricingOption
            title="Monthly"
            price="$9.99"
            period="month"
            isSelected={selectedPlan === 'monthly'}
            onSelect={() => setSelectedPlan('monthly')}
          />
        </View>

        <View style={styles.cta}>
          <Button
            title={
              selectedPlan === 'yearly'
                ? 'Start 7-day free trial'
                : 'Subscribe now'
            }
            onPress={handlePurchase}
            loading={isLoading}
            size="large"
          />

          <Text style={styles.trialNote}>
            {selectedPlan === 'yearly'
              ? '7-day free trial, then $49.99/year. Cancel anytime.'
              : '$9.99/month. Cancel anytime.'}
          </Text>

          <TouchableOpacity onPress={handleRestore} style={styles.restoreButton}>
            <Text style={styles.restoreText}>Restore purchases</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.legal}>
          <Text style={styles.legalText}>
            Payment will be charged to your Apple ID account at confirmation of
            purchase. Subscription automatically renews unless it is canceled at
            least 24 hours before the end of the current period. You can manage
            and cancel your subscriptions in your App Store account settings.
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    padding: 16,
  },
  closeButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: COLORS.border,
    alignItems: 'center',
    justifyContent: 'center',
  },
  closeText: {
    fontSize: 18,
    color: COLORS.textSecondary,
  },
  scroll: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 40,
  },
  hero: {
    alignItems: 'center',
    marginBottom: 32,
  },
  heroEmoji: {
    fontSize: 56,
    marginBottom: 16,
  },
  heroTitle: {
    fontSize: 28,
    fontWeight: '800',
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: 8,
  },
  heroSubtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  features: {
    marginBottom: 32,
  },
  pricing: {
    marginBottom: 24,
  },
  pricingTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 16,
  },
  cta: {
    alignItems: 'center',
    marginBottom: 24,
  },
  trialNote: {
    fontSize: 13,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginTop: 12,
  },
  restoreButton: {
    marginTop: 16,
    padding: 8,
  },
  restoreText: {
    fontSize: 14,
    color: COLORS.primary,
    fontWeight: '600',
  },
  legal: {
    marginTop: 16,
  },
  legalText: {
    fontSize: 11,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 16,
  },
});
