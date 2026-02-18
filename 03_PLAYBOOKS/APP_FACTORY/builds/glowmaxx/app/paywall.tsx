import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { router } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { PurchasesPackage } from 'react-native-purchases';

import { useUserStore } from '../src/stores/userStore';
import {
  getOfferings,
  purchasePackage,
  restorePurchases,
} from '../src/services/subscriptionService';
import { COLORS, MONTHLY_PRICE, ANNUAL_PRICE } from '../src/utils/constants';

const FEATURES = [
  { icon: 'happy-outline', text: 'Mewing timer with guidance' },
  { icon: 'fitness-outline', text: 'Facial exercise routines' },
  { icon: 'water-outline', text: 'Debloat tracking' },
  { icon: 'camera-outline', text: 'Progress photo comparison' },
  { icon: 'notifications-outline', text: 'Smart reminders' },
  { icon: 'book-outline', text: 'Expert guides library' },
];

export default function PaywallScreen() {
  const [packages, setPackages] = useState<PurchasesPackage[]>([]);
  const [selectedPackage, setSelectedPackage] = useState<PurchasesPackage | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isPurchasing, setIsPurchasing] = useState(false);

  const { updateSubscription, subscription } = useUserStore();

  useEffect(() => {
    loadOfferings();
  }, []);

  const loadOfferings = async () => {
    try {
      const offerings = await getOfferings();
      setPackages(offerings);
      // Select annual by default (better value)
      const annual = offerings.find((p) => p.packageType === 'ANNUAL');
      setSelectedPackage(annual || offerings[0] || null);
    } catch (error) {
      console.error('Failed to load offerings:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePurchase = async () => {
    if (!selectedPackage) return;

    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    setIsPurchasing(true);

    try {
      const result = await purchasePackage(selectedPackage);

      if (result.success) {
        updateSubscription({ isSubscribed: true });
        router.replace('/(tabs)/home');
      } else if (result.error && result.error !== 'Purchase cancelled') {
        Alert.alert('Purchase Failed', result.error);
      }
    } catch (error) {
      console.error('Purchase error:', error);
      Alert.alert('Error', 'Something went wrong. Please try again.');
    } finally {
      setIsPurchasing(false);
    }
  };

  const handleRestore = async () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    setIsPurchasing(true);

    try {
      const result = await restorePurchases();

      if (result.success) {
        updateSubscription({ isSubscribed: true });
        Alert.alert('Success', 'Your purchase has been restored!', [
          { text: 'OK', onPress: () => router.replace('/(tabs)/home') },
        ]);
      } else {
        Alert.alert('No Purchases Found', 'We could not find any previous purchases.');
      }
    } catch (error) {
      console.error('Restore error:', error);
      Alert.alert('Error', 'Failed to restore purchases. Please try again.');
    } finally {
      setIsPurchasing(false);
    }
  };

  const handleClose = () => {
    // If user has trial, let them continue
    if (subscription.isInTrial) {
      router.replace('/(tabs)/home');
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Close button (only if in trial) */}
        {subscription.isInTrial && (
          <TouchableOpacity style={styles.closeButton} onPress={handleClose}>
            <Ionicons name="close" size={28} color={COLORS.text} />
          </TouchableOpacity>
        )}

        {/* Header */}
        <View style={styles.header}>
          <View style={styles.iconContainer}>
            <Ionicons name="sparkles" size={48} color={COLORS.primary} />
          </View>
          <Text style={styles.title}>Unlock Your Glow</Text>
          <Text style={styles.subtitle}>
            Get full access to all features and start your transformation
          </Text>
        </View>

        {/* Features */}
        <View style={styles.featuresContainer}>
          {FEATURES.map((feature, index) => (
            <View key={index} style={styles.featureRow}>
              <View style={styles.featureIconContainer}>
                <Ionicons
                  name={feature.icon as keyof typeof Ionicons.glyphMap}
                  size={20}
                  color={COLORS.primary}
                />
              </View>
              <Text style={styles.featureText}>{feature.text}</Text>
            </View>
          ))}
        </View>

        {/* Pricing options */}
        {isLoading ? (
          <ActivityIndicator size="large" color={COLORS.primary} style={styles.loader} />
        ) : (
          <View style={styles.pricingContainer}>
            {/* Annual option */}
            <TouchableOpacity
              style={[
                styles.priceOption,
                selectedPackage?.packageType === 'ANNUAL' && styles.priceOptionSelected,
              ]}
              onPress={() => {
                const annual = packages.find((p) => p.packageType === 'ANNUAL');
                if (annual) {
                  Haptics.selectionAsync();
                  setSelectedPackage(annual);
                }
              }}
            >
              <View style={styles.saveBadge}>
                <Text style={styles.saveBadgeText}>SAVE 58%</Text>
              </View>
              <Text style={styles.priceLabel}>Annual</Text>
              <Text style={styles.priceAmount}>{ANNUAL_PRICE}/year</Text>
              <Text style={styles.priceNote}>$4.17/month</Text>
            </TouchableOpacity>

            {/* Monthly option */}
            <TouchableOpacity
              style={[
                styles.priceOption,
                selectedPackage?.packageType === 'MONTHLY' && styles.priceOptionSelected,
              ]}
              onPress={() => {
                const monthly = packages.find((p) => p.packageType === 'MONTHLY');
                if (monthly) {
                  Haptics.selectionAsync();
                  setSelectedPackage(monthly);
                }
              }}
            >
              <Text style={styles.priceLabel}>Monthly</Text>
              <Text style={styles.priceAmount}>{MONTHLY_PRICE}/month</Text>
              <Text style={styles.priceNote}>Billed monthly</Text>
            </TouchableOpacity>
          </View>
        )}

        {/* Trial info */}
        {subscription.isInTrial && (
          <View style={styles.trialInfo}>
            <Ionicons name="time-outline" size={16} color={COLORS.warning} />
            <Text style={styles.trialText}>
              {subscription.trialDaysRemaining} days left in your free trial
            </Text>
          </View>
        )}
      </ScrollView>

      {/* Footer */}
      <View style={styles.footer}>
        <TouchableOpacity
          style={[styles.purchaseButton, isPurchasing && styles.purchaseButtonDisabled]}
          onPress={handlePurchase}
          disabled={isPurchasing || !selectedPackage}
        >
          {isPurchasing ? (
            <ActivityIndicator size="small" color={COLORS.surface} />
          ) : (
            <Text style={styles.purchaseButtonText}>
              {subscription.isInTrial ? 'Subscribe Now' : 'Start 7-Day Free Trial'}
            </Text>
          )}
        </TouchableOpacity>

        <TouchableOpacity onPress={handleRestore} disabled={isPurchasing}>
          <Text style={styles.restoreText}>Restore Purchases</Text>
        </TouchableOpacity>

        <Text style={styles.legalText}>
          Cancel anytime. Subscription auto-renews until cancelled.
        </Text>

        <View style={styles.legalLinks}>
          <TouchableOpacity onPress={() => router.push('/privacy-policy')}>
            <Text style={styles.legalLinkText}>Privacy Policy</Text>
          </TouchableOpacity>
          <Text style={styles.legalSeparator}>|</Text>
          <TouchableOpacity onPress={() => router.push('/terms')}>
            <Text style={styles.legalLinkText}>Terms of Service</Text>
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scrollContent: {
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 20,
  },
  closeButton: {
    position: 'absolute',
    top: 10,
    right: 0,
    padding: 10,
    zIndex: 10,
  },
  header: {
    alignItems: 'center',
    marginBottom: 30,
    marginTop: 20,
  },
  iconContainer: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: COLORS.primaryLight,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20,
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
    textAlign: 'center',
  },
  featuresContainer: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 20,
    marginBottom: 24,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  featureIconContainer: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: COLORS.primaryLight,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
  },
  featureText: {
    fontSize: 15,
    color: COLORS.text,
    flex: 1,
  },
  loader: {
    marginVertical: 40,
  },
  pricingContainer: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 20,
  },
  priceOption: {
    flex: 1,
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: COLORS.border,
    position: 'relative',
  },
  priceOptionSelected: {
    borderColor: COLORS.primary,
    backgroundColor: '#FFF0F5',
  },
  saveBadge: {
    position: 'absolute',
    top: -10,
    backgroundColor: COLORS.success,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 10,
  },
  saveBadgeText: {
    fontSize: 11,
    fontWeight: 'bold',
    color: COLORS.surface,
  },
  priceLabel: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 4,
    marginTop: 8,
  },
  priceAmount: {
    fontSize: 20,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 4,
  },
  priceNote: {
    fontSize: 12,
    color: COLORS.textLight,
  },
  trialInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: '#FFF8E1',
    padding: 12,
    borderRadius: 12,
  },
  trialText: {
    fontSize: 14,
    color: COLORS.text,
  },
  footer: {
    paddingHorizontal: 20,
    paddingVertical: 16,
    backgroundColor: COLORS.surface,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
  },
  purchaseButton: {
    backgroundColor: COLORS.primary,
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 12,
  },
  purchaseButtonDisabled: {
    opacity: 0.7,
  },
  purchaseButtonText: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.surface,
  },
  restoreText: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 12,
  },
  legalText: {
    fontSize: 12,
    color: COLORS.textLight,
    textAlign: 'center',
    marginBottom: 8,
  },
  legalLinks: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  legalLinkText: {
    fontSize: 12,
    color: COLORS.textSecondary,
    textDecorationLine: 'underline',
  },
  legalSeparator: {
    fontSize: 12,
    color: COLORS.textLight,
    marginHorizontal: 8,
  },
});
