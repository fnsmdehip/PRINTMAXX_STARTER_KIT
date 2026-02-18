import { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Pressable,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import {
  colors,
  spacing,
  borderRadius,
  typography,
  shadows,
} from '@/constants/theme';
import { paywallConfig } from '@/constants/paywall';
import { useUserStore } from '@/store/userStore';

type PlanType = 'weekly' | 'annual';

export default function PaywallScreen() {
  const router = useRouter();
  const [selectedPlan, setSelectedPlan] = useState<PlanType>('annual');
  const [isLoading, setIsLoading] = useState(false);
  const { setSubscribed, startTrial, isTrialActive, getTrialDaysRemaining } = useUserStore();

  const handlePurchase = async () => {
    setIsLoading(true);

    try {
      // In production, this would call RevenueCat
      await new Promise((resolve) => setTimeout(resolve, 1500));
      setSubscribed(true);
      Alert.alert('Welcome to DevotionFlow!', "You now have full access.", [
        { text: 'Continue', onPress: () => router.replace('/(tabs)') },
      ]);
    } catch (error) {
      Alert.alert('Oops', 'Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartTrial = async () => {
    setIsLoading(true);

    try {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      startTrial();
      Alert.alert(
        'Trial Started!',
        'You have 7 days of full access. Enjoy!',
        [{ text: "Let's Go!", onPress: () => router.replace('/(tabs)') }]
      );
    } catch (error) {
      Alert.alert('Oops', 'Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRestore = async () => {
    setIsLoading(true);
    try {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      Alert.alert('No Active Subscription', 'No previous purchases found.');
    } catch (error) {
      Alert.alert('Error', 'Could not restore purchases.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = () => {
    if (isTrialActive()) {
      router.back();
    } else {
      Alert.alert(
        'Continue Your Journey',
        'Unlock DevotionFlow to continue your spiritual journey!',
        [{ text: 'OK' }]
      );
    }
  };

  const iconMap: Record<string, keyof typeof Ionicons.glyphMap> = {
    book: 'book',
    heart: 'heart',
    sunny: 'sunny',
    flame: 'flame',
    notifications: 'notifications',
  };

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={[colors.sunriseStart + '30', colors.background]}
        style={styles.gradient}
      />

      <SafeAreaView style={styles.safeArea} edges={['top']}>
        {/* Close Button */}
        {isTrialActive() && (
          <Pressable style={styles.closeButton} onPress={handleClose}>
            <Ionicons name="close" size={28} color={colors.text} />
          </Pressable>
        )}

        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.content}
          showsVerticalScrollIndicator={false}
        >
          {/* Header */}
          <View style={styles.header}>
            <Ionicons name="sparkles" size={48} color={colors.secondary} />
            <Text style={styles.title}>Unlock DevotionFlow</Text>
            <Text style={styles.subtitle}>
              Deepen your faith with daily devotionals, prayer tracking, and more
            </Text>
          </View>

          {/* Features */}
          <View style={styles.features}>
            {paywallConfig.features.map((feature, index) => (
              <View key={index} style={styles.featureRow}>
                <View style={styles.featureIcon}>
                  <Ionicons
                    name={iconMap[feature.icon] || 'checkmark'}
                    size={20}
                    color={colors.primary}
                  />
                </View>
                <View style={styles.featureText}>
                  <Text style={styles.featureTitle}>{feature.title}</Text>
                  <Text style={styles.featureDescription}>
                    {feature.description}
                  </Text>
                </View>
              </View>
            ))}
          </View>

          {/* Plan Selection */}
          <View style={styles.plans}>
            {/* Annual Plan */}
            <Pressable
              style={[
                styles.planCard,
                selectedPlan === 'annual' && styles.planCardSelected,
              ]}
              onPress={() => setSelectedPlan('annual')}
            >
              <View style={styles.bestValueBadge}>
                <Text style={styles.bestValueText}>BEST VALUE</Text>
              </View>
              <View style={styles.planRadio}>
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
              <View style={styles.planInfo}>
                <Text style={styles.planName}>Annual</Text>
                <Text style={styles.planPrice}>
                  {paywallConfig.pricing.annual.price}/year
                </Text>
                <Text style={styles.planSavings}>
                  Just {paywallConfig.pricing.annual.pricePerWeek}/week - Save{' '}
                  {paywallConfig.pricing.annual.savings}
                </Text>
              </View>
            </Pressable>

            {/* Weekly Plan */}
            <Pressable
              style={[
                styles.planCard,
                selectedPlan === 'weekly' && styles.planCardSelected,
              ]}
              onPress={() => setSelectedPlan('weekly')}
            >
              <View style={styles.planRadio}>
                <View
                  style={[
                    styles.radioOuter,
                    selectedPlan === 'weekly' && styles.radioOuterSelected,
                  ]}
                >
                  {selectedPlan === 'weekly' && (
                    <View style={styles.radioInner} />
                  )}
                </View>
              </View>
              <View style={styles.planInfo}>
                <Text style={styles.planName}>Weekly</Text>
                <Text style={styles.planPrice}>
                  {paywallConfig.pricing.weekly.price}/week
                </Text>
                <Text style={styles.planSavings}>
                  {paywallConfig.pricing.weekly.trialDays}-day free trial
                </Text>
              </View>
            </Pressable>
          </View>

          {/* Review */}
          <View style={styles.review}>
            <View style={styles.stars}>
              {[1, 2, 3, 4, 5].map((star) => (
                <Ionicons key={star} name="star" size={16} color={colors.warning} />
              ))}
            </View>
            <Text style={styles.reviewText}>
              "{paywallConfig.reviews[0].text}"
            </Text>
            <Text style={styles.reviewAuthor}>
              - {paywallConfig.reviews[0].name}
            </Text>
          </View>
        </ScrollView>

        {/* CTA Section */}
        <View style={styles.ctaSection}>
          <Pressable
            style={({ pressed }) => [
              styles.ctaButton,
              pressed && styles.ctaButtonPressed,
              isLoading && styles.ctaButtonDisabled,
            ]}
            onPress={selectedPlan === 'weekly' ? handleStartTrial : handlePurchase}
            disabled={isLoading}
          >
            <Text style={styles.ctaText}>
              {isLoading
                ? 'Processing...'
                : selectedPlan === 'weekly'
                ? paywallConfig.cta.trial
                : 'Continue with Annual'}
            </Text>
          </Pressable>

          <Pressable style={styles.restoreButton} onPress={handleRestore}>
            <Text style={styles.restoreText}>{paywallConfig.cta.restore}</Text>
          </Pressable>

          <Text style={styles.legalText}>
            Cancel anytime. Subscription auto-renews.
          </Text>
        </View>
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  gradient: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: 300,
  },
  safeArea: {
    flex: 1,
  },
  closeButton: {
    position: 'absolute',
    top: 60,
    right: spacing.lg,
    zIndex: 10,
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.surface,
    alignItems: 'center',
    justifyContent: 'center',
    ...shadows.sm,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: spacing.lg,
    paddingTop: spacing.xxl,
    paddingBottom: 200,
  },
  header: {
    alignItems: 'center',
    marginBottom: spacing.xl,
  },
  title: {
    ...typography.h1,
    color: colors.text,
    textAlign: 'center',
    marginTop: spacing.md,
    marginBottom: spacing.sm,
  },
  subtitle: {
    ...typography.body,
    color: colors.textLight,
    textAlign: 'center',
    paddingHorizontal: spacing.lg,
  },
  features: {
    marginBottom: spacing.xl,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  featureIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.primary + '15',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: spacing.md,
  },
  featureText: {
    flex: 1,
  },
  featureTitle: {
    ...typography.bodyBold,
    color: colors.text,
  },
  featureDescription: {
    ...typography.caption,
    color: colors.textMuted,
  },
  plans: {
    gap: spacing.sm,
    marginBottom: spacing.lg,
  },
  planCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    borderWidth: 2,
    borderColor: colors.border,
    ...shadows.sm,
  },
  planCardSelected: {
    borderColor: colors.primary,
    backgroundColor: colors.primary + '08',
  },
  bestValueBadge: {
    position: 'absolute',
    top: -10,
    right: spacing.md,
    backgroundColor: colors.primary,
    paddingHorizontal: spacing.sm,
    paddingVertical: 2,
    borderRadius: borderRadius.sm,
  },
  bestValueText: {
    ...typography.small,
    color: colors.surface,
    fontWeight: '700',
  },
  planRadio: {
    marginRight: spacing.md,
  },
  radioOuter: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: colors.border,
    alignItems: 'center',
    justifyContent: 'center',
  },
  radioOuterSelected: {
    borderColor: colors.primary,
  },
  radioInner: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: colors.primary,
  },
  planInfo: {
    flex: 1,
  },
  planName: {
    ...typography.bodyBold,
    color: colors.text,
  },
  planPrice: {
    ...typography.h3,
    color: colors.primary,
  },
  planSavings: {
    ...typography.caption,
    color: colors.textMuted,
  },
  review: {
    alignItems: 'center',
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    ...shadows.sm,
  },
  stars: {
    flexDirection: 'row',
    marginBottom: spacing.sm,
  },
  reviewText: {
    ...typography.body,
    color: colors.text,
    textAlign: 'center',
    fontStyle: 'italic',
  },
  reviewAuthor: {
    ...typography.caption,
    color: colors.textMuted,
    marginTop: spacing.xs,
  },
  ctaSection: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    padding: spacing.lg,
    paddingBottom: spacing.xl,
    backgroundColor: colors.background,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  ctaButton: {
    backgroundColor: colors.primary,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    alignItems: 'center',
    ...shadows.md,
  },
  ctaButtonPressed: {
    opacity: 0.9,
  },
  ctaButtonDisabled: {
    opacity: 0.7,
  },
  ctaText: {
    ...typography.bodyBold,
    color: colors.surface,
    fontSize: 18,
  },
  restoreButton: {
    alignItems: 'center',
    paddingVertical: spacing.md,
  },
  restoreText: {
    ...typography.caption,
    color: colors.textMuted,
  },
  legalText: {
    ...typography.small,
    color: colors.textMuted,
    textAlign: 'center',
  },
});
