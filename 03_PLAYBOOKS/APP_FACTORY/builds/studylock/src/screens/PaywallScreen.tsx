import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useUserStore } from '../stores/userStore';
import { COLORS, PREMIUM_PRICING } from '../utils/constants';
import Button from '../components/Button';
import Card from '../components/Card';

const PREMIUM_FEATURES = [
  {
    icon: 'infinite-outline',
    title: 'Unlimited Sessions',
    description: 'No limit on session length or daily sessions',
  },
  {
    icon: 'library-outline',
    title: 'All Subjects',
    description: 'Access all quiz categories and subjects',
  },
  {
    icon: 'cloud-upload-outline',
    title: 'Quizlet Import',
    description: 'Import your own flashcards and study sets',
  },
  {
    icon: 'people-outline',
    title: 'Study Groups',
    description: 'Join or create study groups with friends',
  },
  {
    icon: 'analytics-outline',
    title: 'Advanced Analytics',
    description: 'Detailed insights into your study habits',
  },
  {
    icon: 'snow-outline',
    title: 'Streak Freeze',
    description: 'Protect your streak when you miss a day',
  },
  {
    icon: 'remove-circle-outline',
    title: 'No Ads',
    description: 'Completely ad-free experience',
  },
];

export default function PaywallScreen() {
  const router = useRouter();
  const { setPremiumStatus, progress } = useUserStore();
  const [selectedPlan, setSelectedPlan] = useState<'monthly' | 'yearly'>('yearly');
  const [isLoading, setIsLoading] = useState(false);

  const handlePurchase = async () => {
    setIsLoading(true);

    // Simulate purchase flow
    // In production, this would use RevenueCat
    setTimeout(() => {
      setIsLoading(false);
      Alert.alert(
        'RevenueCat Integration',
        'In production, this would connect to RevenueCat for in-app purchases. For now, simulating a successful purchase.',
        [
          {
            text: 'Simulate Purchase',
            onPress: () => {
              const expiresAt = new Date();
              expiresAt.setFullYear(expiresAt.getFullYear() + 1);
              setPremiumStatus(true, expiresAt.toISOString());
              router.replace('/');
            },
          },
          { text: 'Cancel', style: 'cancel' },
        ]
      );
    }, 1000);
  };

  const handleRestore = () => {
    Alert.alert(
      'Restore Purchases',
      'Checking for previous purchases...',
      [{ text: 'OK' }]
    );
  };

  if (progress.isPremium) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.closeButton}
            onPress={() => router.back()}
          >
            <Ionicons name="close" size={24} color={COLORS.text} />
          </TouchableOpacity>
        </View>

        <View style={styles.premiumActiveContainer}>
          <View style={styles.premiumBadge}>
            <Ionicons name="star" size={48} color={COLORS.accent} />
          </View>
          <Text style={styles.premiumActiveTitle}>You're a Pro!</Text>
          <Text style={styles.premiumActiveSubtitle}>
            Thank you for supporting StudyLock. You have access to all premium features.
          </Text>
          <Button
            title="Back to Home"
            onPress={() => router.replace('/')}
            size="large"
            style={{ marginTop: 32 }}
          />
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.closeButton}
          onPress={() => router.back()}
        >
          <Ionicons name="close" size={24} color={COLORS.text} />
        </TouchableOpacity>
      </View>

      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Hero */}
        <View style={styles.hero}>
          <View style={styles.iconBadge}>
            <Ionicons name="star" size={40} color={COLORS.white} />
          </View>
          <Text style={styles.title}>Unlock StudyLock Pro</Text>
          <Text style={styles.subtitle}>
            Supercharge your studying with unlimited features
          </Text>
        </View>

        {/* Features */}
        <View style={styles.features}>
          {PREMIUM_FEATURES.map((feature, index) => (
            <View key={index} style={styles.featureRow}>
              <View style={styles.featureIcon}>
                <Ionicons
                  name={feature.icon as keyof typeof Ionicons.glyphMap}
                  size={24}
                  color={COLORS.primary}
                />
              </View>
              <View style={styles.featureContent}>
                <Text style={styles.featureTitle}>{feature.title}</Text>
                <Text style={styles.featureDescription}>{feature.description}</Text>
              </View>
            </View>
          ))}
        </View>

        {/* Pricing Options */}
        <View style={styles.pricing}>
          <TouchableOpacity
            style={[
              styles.priceCard,
              selectedPlan === 'yearly' && styles.priceCardSelected,
            ]}
            onPress={() => setSelectedPlan('yearly')}
          >
            <View style={styles.savingsBadge}>
              <Text style={styles.savingsText}>SAVE {PREMIUM_PRICING.yearly.savings}</Text>
            </View>
            <Text style={styles.priceLabel}>Yearly</Text>
            <Text style={styles.price}>{PREMIUM_PRICING.yearly.price}</Text>
            <Text style={styles.pricePeriod}>per year</Text>
            <Text style={styles.priceBreakdown}>
              {(parseFloat(PREMIUM_PRICING.yearly.price.replace('$', '')) / 12).toFixed(2)}/mo
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.priceCard,
              selectedPlan === 'monthly' && styles.priceCardSelected,
            ]}
            onPress={() => setSelectedPlan('monthly')}
          >
            <Text style={styles.priceLabel}>Monthly</Text>
            <Text style={styles.price}>{PREMIUM_PRICING.monthly.price}</Text>
            <Text style={styles.pricePeriod}>per month</Text>
          </TouchableOpacity>
        </View>

        {/* CTA */}
        <View style={styles.ctaContainer}>
          <Button
            title={isLoading ? 'Processing...' : 'Start Free Trial'}
            onPress={handlePurchase}
            size="large"
            fullWidth
            loading={isLoading}
          />
          <Text style={styles.trialText}>
            7-day free trial, then {selectedPlan === 'yearly' ? PREMIUM_PRICING.yearly.price + '/year' : PREMIUM_PRICING.monthly.price + '/month'}
          </Text>

          <TouchableOpacity style={styles.restoreButton} onPress={handleRestore}>
            <Text style={styles.restoreText}>Restore Purchases</Text>
          </TouchableOpacity>
        </View>

        {/* Legal */}
        <Text style={styles.legal}>
          Payment will be charged to your Apple ID account at confirmation of purchase.
          Subscription automatically renews unless canceled at least 24 hours before
          the end of the current period. Your account will be charged for renewal
          within 24 hours prior to the end of the current period.
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
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  closeButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: COLORS.surface,
    alignItems: 'center',
    justifyContent: 'center',
  },
  scrollView: {
    flex: 1,
  },
  content: {
    paddingHorizontal: 24,
    paddingBottom: 40,
  },
  hero: {
    alignItems: 'center',
    marginBottom: 32,
  },
  iconBadge: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: COLORS.accent,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
    shadowColor: COLORS.accent,
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.4,
    shadowRadius: 16,
    elevation: 8,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  features: {
    gap: 16,
    marginBottom: 32,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  featureIcon: {
    width: 48,
    height: 48,
    borderRadius: 12,
    backgroundColor: COLORS.primary + '15',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 16,
  },
  featureContent: {
    flex: 1,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
  },
  featureDescription: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  pricing: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 24,
  },
  priceCard: {
    flex: 1,
    padding: 20,
    borderRadius: 16,
    backgroundColor: COLORS.surface,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: COLORS.surface,
    position: 'relative',
  },
  priceCardSelected: {
    borderColor: COLORS.primary,
    backgroundColor: COLORS.primary + '08',
  },
  savingsBadge: {
    position: 'absolute',
    top: -10,
    backgroundColor: COLORS.secondary,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  savingsText: {
    fontSize: 10,
    fontWeight: '700',
    color: COLORS.white,
  },
  priceLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.textSecondary,
    marginBottom: 4,
  },
  price: {
    fontSize: 32,
    fontWeight: '700',
    color: COLORS.text,
  },
  pricePeriod: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
  priceBreakdown: {
    fontSize: 11,
    color: COLORS.primary,
    fontWeight: '600',
    marginTop: 4,
  },
  ctaContainer: {
    alignItems: 'center',
    marginBottom: 24,
  },
  trialText: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginTop: 12,
  },
  restoreButton: {
    marginTop: 16,
    paddingVertical: 8,
  },
  restoreText: {
    fontSize: 14,
    color: COLORS.primary,
    fontWeight: '500',
  },
  legal: {
    fontSize: 10,
    color: COLORS.textMuted,
    textAlign: 'center',
    lineHeight: 14,
    marginBottom: 12,
  },
  legalLinks: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 8,
  },
  legalLink: {
    fontSize: 12,
    color: COLORS.primary,
  },
  legalDivider: {
    fontSize: 12,
    color: COLORS.textMuted,
  },
  premiumActiveContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 32,
  },
  premiumBadge: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: COLORS.accent + '20',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
  },
  premiumActiveTitle: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 8,
  },
  premiumActiveSubtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 24,
  },
});
