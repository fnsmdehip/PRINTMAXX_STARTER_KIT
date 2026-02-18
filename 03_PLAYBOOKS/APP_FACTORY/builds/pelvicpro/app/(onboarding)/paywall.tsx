import { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Pressable,
  Alert,
  Animated,
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
import Luna from '@/components/luna/Luna';

type PlanType = 'weekly' | 'annual';

export default function OnboardingPaywallScreen() {
  const router = useRouter();
  const [selectedPlan, setSelectedPlan] = useState<PlanType>('annual');
  const [isLoading, setIsLoading] = useState(false);
  const { setSubscribed, startTrial, completeOnboarding } = useUserStore();

  // Animations
  const lunaOpacity = useRef(new Animated.Value(0)).current;
  const lunaScale = useRef(new Animated.Value(0.8)).current;
  const contentOpacity = useRef(new Animated.Value(0)).current;
  const contentTranslateY = useRef(new Animated.Value(30)).current;
  const planPulse = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    // Entrance animation
    Animated.sequence([
      Animated.parallel([
        Animated.timing(lunaOpacity, {
          toValue: 1,
          duration: 400,
          useNativeDriver: true,
        }),
        Animated.spring(lunaScale, {
          toValue: 1,
          tension: 50,
          friction: 7,
          useNativeDriver: true,
        }),
      ]),
      Animated.parallel([
        Animated.timing(contentOpacity, {
          toValue: 1,
          duration: 400,
          useNativeDriver: true,
        }),
        Animated.timing(contentTranslateY, {
          toValue: 0,
          duration: 400,
          useNativeDriver: true,
        }),
      ]),
    ]).start();

    // Pulse animation for selected plan
    Animated.loop(
      Animated.sequence([
        Animated.timing(planPulse, {
          toValue: 1.02,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(planPulse, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    ).start();
  }, []);

  const handleStartTrial = async () => {
    setIsLoading(true);

    try {
      // In production: Purchases.purchasePackage with trial
      await new Promise((resolve) => setTimeout(resolve, 1000));
      completeOnboarding();
      startTrial();
      router.replace('/(tabs)');
    } catch (error) {
      Alert.alert('Oops', 'Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handlePurchase = async () => {
    setIsLoading(true);

    try {
      // In production: Purchases.purchasePackage
      await new Promise((resolve) => setTimeout(resolve, 1500));
      completeOnboarding();
      setSubscribed(true);
      router.replace('/(tabs)');
    } catch (error) {
      Alert.alert('Oops', 'Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRestore = async () => {
    setIsLoading(true);
    try {
      // Purchases.restorePurchases()
      await new Promise((resolve) => setTimeout(resolve, 1000));
      Alert.alert('No Active Subscription', 'No previous purchases found.');
    } catch (error) {
      Alert.alert('Error', 'Could not restore purchases.');
    } finally {
      setIsLoading(false);
    }
  };

  const iconMap: Record<string, keyof typeof Ionicons.glyphMap> = {
    dumbbell: 'barbell',
    'chart-line': 'trending-up',
    fire: 'flame',
    cat: 'heart',
    'book-open': 'book',
  };

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={[colors.primary + '30', colors.secondary + '15', colors.background]}
        style={styles.gradient}
      />

      <SafeAreaView style={styles.safeArea} edges={['top']}>
        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.content}
          showsVerticalScrollIndicator={false}
        >
          {/* Luna Section */}
          <Animated.View
            style={[
              styles.lunaSection,
              {
                opacity: lunaOpacity,
                transform: [{ scale: lunaScale }],
              },
            ]}
          >
            <Luna state="excited" size={100} />
            <Text style={styles.lunaMessage}>
              Let's keep training together!
            </Text>
          </Animated.View>

          {/* Title */}
          <Animated.View
            style={[
              styles.titleSection,
              {
                opacity: contentOpacity,
                transform: [{ translateY: contentTranslateY }],
              },
            ]}
          >
            <Text style={styles.title}>Start your free trial</Text>
            <Text style={styles.subtitle}>
              3 days free, then choose your plan
            </Text>
          </Animated.View>

          {/* Features */}
          <Animated.View
            style={[
              styles.features,
              {
                opacity: contentOpacity,
                transform: [{ translateY: contentTranslateY }],
              },
            ]}
          >
            {paywallConfig.features.slice(0, 4).map((feature, index) => (
              <View key={index} style={styles.featureRow}>
                <View style={styles.featureIcon}>
                  <Ionicons
                    name={iconMap[feature.icon] || 'checkmark'}
                    size={18}
                    color={colors.primary}
                  />
                </View>
                <Text style={styles.featureText}>{feature.title}</Text>
              </View>
            ))}
          </Animated.View>

          {/* Plan Selection */}
          <Animated.View
            style={[
              styles.plans,
              {
                opacity: contentOpacity,
              },
            ]}
          >
            {/* Annual Plan - Best Value */}
            <Animated.View
              style={[
                selectedPlan === 'annual' && { transform: [{ scale: planPulse }] },
              ]}
            >
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
            </Animated.View>

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
                  {selectedPlan === 'weekly' && <View style={styles.radioInner} />}
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
          </Animated.View>

          {/* Trial info */}
          <View style={styles.trialInfo}>
            <Ionicons name="shield-checkmark" size={20} color={colors.success} />
            <Text style={styles.trialInfoText}>
              Cancel anytime during your free trial
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
            Cancel anytime. Subscription auto-renews after trial.
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
    height: 400,
  },
  safeArea: {
    flex: 1,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: spacing.lg,
    paddingTop: spacing.xl,
    paddingBottom: 220,
  },
  lunaSection: {
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  lunaMessage: {
    ...typography.bodyBold,
    color: colors.text,
    marginTop: spacing.sm,
    textAlign: 'center',
  },
  titleSection: {
    alignItems: 'center',
    marginBottom: spacing.lg,
  },
  title: {
    ...typography.h1,
    color: colors.text,
    textAlign: 'center',
    marginBottom: spacing.xs,
  },
  subtitle: {
    ...typography.body,
    color: colors.textLight,
    textAlign: 'center',
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
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: colors.primary + '15',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: spacing.md,
  },
  featureText: {
    ...typography.body,
    color: colors.text,
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
    paddingVertical: 3,
    borderRadius: borderRadius.sm,
  },
  bestValueText: {
    ...typography.small,
    color: colors.surface,
    fontWeight: '700',
    fontSize: 10,
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
  trialInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
    backgroundColor: colors.success + '10',
    padding: spacing.md,
    borderRadius: borderRadius.lg,
  },
  trialInfoText: {
    ...typography.caption,
    color: colors.success,
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
