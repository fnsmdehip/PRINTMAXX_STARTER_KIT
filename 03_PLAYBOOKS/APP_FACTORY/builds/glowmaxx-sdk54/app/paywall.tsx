import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import { useUserStore } from '../src/stores/userStore';
import { COLORS } from '../src/utils/constants';

export default function PaywallScreen() {
  const { subscription } = useUserStore();

  const handlePurchase = () => {
    // RevenueCat integration would go here
    router.back();
  };

  const handleRestore = () => {
    // RevenueCat restore purchases
    router.back();
  };

  return (
    <SafeAreaView style={styles.container} edges={['top', 'bottom']}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()}>
            <Ionicons name="close" size={28} color={COLORS.text} />
          </TouchableOpacity>
        </View>

        <View style={styles.content}>
          <View style={styles.iconContainer}>
            <Ionicons name="lock-open" size={64} color={COLORS.primary} />
          </View>

          <Text style={styles.title}>Unlock Your Full Potential</Text>
          <Text style={styles.subtitle}>
            Get access to premium routines, advanced tracking, and exclusive content
          </Text>

          <View style={styles.features}>
            {['Advanced Routines', 'AI Progress Analysis', 'Custom Nutrition Plans', 'Priority Support'].map((feature) => (
              <View key={feature} style={styles.featureRow}>
                <Ionicons name="checkmark-circle" size={20} color={COLORS.success} />
                <Text style={styles.featureText}>{feature}</Text>
              </View>
            ))}
          </View>

          <View style={styles.pricing}>
            <TouchableOpacity style={styles.pricingCard} onPress={handlePurchase}>
              <Text style={styles.pricingTitle}>Monthly</Text>
              <Text style={styles.pricingPrice}>$9.99</Text>
              <Text style={styles.pricingPeriod}>/month</Text>
            </TouchableOpacity>

            <TouchableOpacity style={[styles.pricingCard, styles.pricingCardFeatured]} onPress={handlePurchase}>
              <View style={styles.badge}>
                <Text style={styles.badgeText}>Save 58%</Text>
              </View>
              <Text style={styles.pricingTitle}>Annual</Text>
              <Text style={styles.pricingPrice}>$49.99</Text>
              <Text style={styles.pricingPeriod}>/year</Text>
            </TouchableOpacity>
          </View>

          <TouchableOpacity style={styles.purchaseButton} onPress={handlePurchase}>
            <Text style={styles.purchaseButtonText}>Start 7-Day Free Trial</Text>
          </TouchableOpacity>

          <Text style={styles.trialText}>
            Then $9.99/month. Cancel anytime, no questions asked.
          </Text>

          <TouchableOpacity onPress={handleRestore}>
            <Text style={styles.restoreText}>Restore Purchase</Text>
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
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    marginBottom: 20,
  },
  content: {
    alignItems: 'center',
  },
  iconContainer: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: COLORS.primaryLight,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 32,
    lineHeight: 24,
  },
  features: {
    width: '100%',
    marginBottom: 40,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
    gap: 12,
  },
  featureText: {
    fontSize: 16,
    color: COLORS.text,
  },
  pricing: {
    width: '100%',
    marginBottom: 32,
    gap: 12,
  },
  pricingCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 24,
    borderWidth: 2,
    borderColor: COLORS.border,
    alignItems: 'center',
  },
  pricingCardFeatured: {
    borderColor: COLORS.primary,
    backgroundColor: COLORS.primaryLight,
  },
  badge: {
    backgroundColor: COLORS.primary,
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
    marginBottom: 8,
  },
  badgeText: {
    color: COLORS.surface,
    fontSize: 12,
    fontWeight: '600',
  },
  pricingTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 8,
  },
  pricingPrice: {
    fontSize: 32,
    fontWeight: 'bold',
    color: COLORS.primary,
  },
  pricingPeriod: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  purchaseButton: {
    width: '100%',
    backgroundColor: COLORS.primary,
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 16,
  },
  purchaseButtonText: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.surface,
  },
  trialText: {
    fontSize: 13,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 16,
  },
  restoreText: {
    fontSize: 14,
    color: COLORS.primary,
    fontWeight: '600',
  },
});
