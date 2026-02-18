import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Dimensions,
  TouchableOpacity,
  TextInput,
  FlatList,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { useUserStore } from '../src/stores/userStore';
import { useSubscriptionStore } from '../src/stores/subscriptionStore';
import { COLORS, SOCIAL_PROOF, ONBOARDING_GOALS } from '../src/utils/constants';

const { width } = Dimensions.get('window');

type OnboardingStep = 'welcome' | 'features' | 'goals' | 'name' | 'paywall';

const FEATURES = [
  {
    icon: 'timer-outline',
    title: 'Track Protocols',
    description: 'Log fasting, cold exposure, sleep, and more',
  },
  {
    icon: 'analytics-outline',
    title: 'See Progress',
    description: 'Daily longevity score and streaks',
  },
  {
    icon: 'book-outline',
    title: 'Learn Science',
    description: 'Evidence-based guides and tips',
  },
];

export default function Onboarding() {
  const [step, setStep] = useState<OnboardingStep>('welcome');
  const [selectedGoals, setSelectedGoals] = useState<string[]>([]);
  const [name, setName] = useState('');
  const flatListRef = useRef<FlatList>(null);

  const completeOnboarding = useUserStore((state) => state.completeOnboarding);
  const startTrial = useSubscriptionStore((state) => state.startTrial);

  const steps: OnboardingStep[] = ['welcome', 'features', 'goals', 'name', 'paywall'];
  const currentIndex = steps.indexOf(step);

  const goNext = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    const nextIndex = currentIndex + 1;
    if (nextIndex < steps.length) {
      setStep(steps[nextIndex]);
    }
  };

  const goBack = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    const prevIndex = currentIndex - 1;
    if (prevIndex >= 0) {
      setStep(steps[prevIndex]);
    }
  };

  const toggleGoal = (goalId: string) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    setSelectedGoals((prev) =>
      prev.includes(goalId)
        ? prev.filter((g) => g !== goalId)
        : [...prev, goalId]
    );
  };

  const handleOpenPaywall = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    router.push('/paywall?from=onboarding');
  };

  const handleSkipPaywall = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    completeOnboarding(name || 'Biohacker', selectedGoals);
    router.replace('/(tabs)/dashboard');
  };

  const handleComplete = () => {
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    completeOnboarding(name || 'Biohacker', selectedGoals);
    startTrial();
    router.replace('/(tabs)/dashboard');
  };

  const renderWelcome = () => (
    <View style={styles.stepContainer}>
      <View style={styles.logoContainer}>
        <View style={styles.logo}>
          <Ionicons name="leaf" size={48} color={COLORS.primary} />
        </View>
        <Text style={styles.appName}>BioMaxx</Text>
      </View>

      <Text style={styles.title}>Optimize Your Biology</Text>
      <Text style={styles.subtitle}>
        Track protocols, build habits, and unlock your full potential
      </Text>

      <View style={styles.socialProof}>
        <Ionicons name="people" size={20} color={COLORS.textSecondary} />
        <Text style={styles.socialProofText}>{SOCIAL_PROOF}</Text>
      </View>

      <TouchableOpacity style={styles.primaryButton} onPress={goNext}>
        <Text style={styles.primaryButtonText}>Get Started</Text>
        <Ionicons name="arrow-forward" size={20} color={COLORS.background} />
      </TouchableOpacity>
    </View>
  );

  const renderFeatures = () => (
    <View style={styles.stepContainer}>
      <Text style={styles.stepTitle}>What you'll get</Text>

      <View style={styles.featuresList}>
        {FEATURES.map((feature, index) => (
          <View key={index} style={styles.featureCard}>
            <View style={styles.featureIcon}>
              <Ionicons
                name={feature.icon as any}
                size={28}
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

      <TouchableOpacity style={styles.primaryButton} onPress={goNext}>
        <Text style={styles.primaryButtonText}>Continue</Text>
        <Ionicons name="arrow-forward" size={20} color={COLORS.background} />
      </TouchableOpacity>
    </View>
  );

  const renderGoals = () => (
    <View style={styles.stepContainer}>
      <Text style={styles.stepTitle}>What's your focus?</Text>
      <Text style={styles.stepSubtitle}>Select all that apply</Text>

      <View style={styles.goalsGrid}>
        {ONBOARDING_GOALS.map((goal) => {
          const isSelected = selectedGoals.includes(goal.id);
          return (
            <TouchableOpacity
              key={goal.id}
              style={[styles.goalCard, isSelected && styles.goalCardSelected]}
              onPress={() => toggleGoal(goal.id)}
              activeOpacity={0.8}
            >
              <Ionicons
                name={goal.icon as any}
                size={28}
                color={isSelected ? COLORS.primary : COLORS.textSecondary}
              />
              <Text
                style={[
                  styles.goalLabel,
                  isSelected && styles.goalLabelSelected,
                ]}
              >
                {goal.label}
              </Text>
              {isSelected && (
                <View style={styles.checkmark}>
                  <Ionicons name="checkmark" size={16} color={COLORS.background} />
                </View>
              )}
            </TouchableOpacity>
          );
        })}
      </View>

      <TouchableOpacity
        style={[
          styles.primaryButton,
          selectedGoals.length === 0 && styles.primaryButtonDisabled,
        ]}
        onPress={goNext}
        disabled={selectedGoals.length === 0}
      >
        <Text style={styles.primaryButtonText}>Continue</Text>
        <Ionicons name="arrow-forward" size={20} color={COLORS.background} />
      </TouchableOpacity>
    </View>
  );

  const renderName = () => (
    <KeyboardAvoidingView
      style={styles.stepContainer}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <Text style={styles.stepTitle}>What should we call you?</Text>
      <Text style={styles.stepSubtitle}>This helps personalize your experience</Text>

      <TextInput
        style={styles.nameInput}
        placeholder="Your name"
        placeholderTextColor={COLORS.textMuted}
        value={name}
        onChangeText={setName}
        autoCapitalize="words"
        autoCorrect={false}
        returnKeyType="done"
        onSubmitEditing={goNext}
      />

      <TouchableOpacity style={styles.primaryButton} onPress={goNext}>
        <Text style={styles.primaryButtonText}>Continue</Text>
        <Ionicons name="arrow-forward" size={20} color={COLORS.background} />
      </TouchableOpacity>

      <TouchableOpacity style={styles.skipButton} onPress={goNext}>
        <Text style={styles.skipButtonText}>Skip for now</Text>
      </TouchableOpacity>
    </KeyboardAvoidingView>
  );

  const renderPaywall = () => (
    <View style={styles.stepContainer}>
      <View style={styles.trialBadge}>
        <Ionicons name="gift" size={24} color={COLORS.accent} />
        <Text style={styles.trialBadgeText}>7-DAY FREE TRIAL</Text>
      </View>

      <Text style={styles.stepTitle}>Unlock all protocols</Text>
      <Text style={styles.stepSubtitle}>
        Try BioMaxx Premium free for 7 days
      </Text>

      <View style={styles.trialFeatures}>
        <View style={styles.trialFeature}>
          <Ionicons name="checkmark-circle" size={20} color={COLORS.primary} />
          <Text style={styles.trialFeatureText}>All 10+ biohacking protocols</Text>
        </View>
        <View style={styles.trialFeature}>
          <Ionicons name="checkmark-circle" size={20} color={COLORS.primary} />
          <Text style={styles.trialFeatureText}>Advanced analytics</Text>
        </View>
        <View style={styles.trialFeature}>
          <Ionicons name="checkmark-circle" size={20} color={COLORS.primary} />
          <Text style={styles.trialFeatureText}>Premium articles & guides</Text>
        </View>
        <View style={styles.trialFeature}>
          <Ionicons name="checkmark-circle" size={20} color={COLORS.primary} />
          <Text style={styles.trialFeatureText}>Priority support</Text>
        </View>
      </View>

      <TouchableOpacity style={styles.primaryButton} onPress={handleOpenPaywall}>
        <Text style={styles.primaryButtonText}>Start Free Trial</Text>
        <Ionicons name="arrow-forward" size={20} color={COLORS.background} />
      </TouchableOpacity>

      <TouchableOpacity style={styles.skipButton} onPress={handleSkipPaywall}>
        <Text style={styles.skipButtonText}>Continue with free version</Text>
      </TouchableOpacity>

      <Text style={styles.trialDisclaimer}>
        Cancel anytime during trial. No charge until trial ends.
      </Text>
    </View>
  );

  const renderStep = () => {
    switch (step) {
      case 'welcome':
        return renderWelcome();
      case 'features':
        return renderFeatures();
      case 'goals':
        return renderGoals();
      case 'name':
        return renderName();
      case 'paywall':
        return renderPaywall();
      default:
        return null;
    }
  };

  return (
    <View style={styles.container}>
      {/* Progress dots */}
      <View style={styles.progressContainer}>
        {steps.map((_, index) => (
          <View
            key={index}
            style={[
              styles.progressDot,
              index === currentIndex && styles.progressDotActive,
              index < currentIndex && styles.progressDotCompleted,
            ]}
          />
        ))}
      </View>

      {/* Back button */}
      {currentIndex > 0 && (
        <TouchableOpacity style={styles.backButton} onPress={goBack}>
          <Ionicons name="arrow-back" size={24} color={COLORS.text} />
        </TouchableOpacity>
      )}

      {renderStep()}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
    paddingTop: 60,
  },
  progressContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 8,
    marginBottom: 20,
  },
  progressDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: COLORS.surfaceLight,
  },
  progressDotActive: {
    width: 24,
    backgroundColor: COLORS.primary,
  },
  progressDotCompleted: {
    backgroundColor: COLORS.primaryDark,
  },
  backButton: {
    position: 'absolute',
    top: 60,
    left: 20,
    zIndex: 10,
    padding: 8,
  },
  stepContainer: {
    flex: 1,
    paddingHorizontal: 24,
    paddingTop: 40,
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: 40,
  },
  logo: {
    width: 100,
    height: 100,
    borderRadius: 24,
    backgroundColor: COLORS.surface,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  appName: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
  },
  title: {
    fontSize: 32,
    fontWeight: '700',
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: 12,
  },
  subtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 32,
  },
  socialProof: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    marginBottom: 40,
    paddingVertical: 12,
    paddingHorizontal: 20,
    backgroundColor: COLORS.surface,
    borderRadius: 20,
    alignSelf: 'center',
  },
  socialProofText: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  stepTitle: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 8,
  },
  stepSubtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    marginBottom: 32,
  },
  featuresList: {
    gap: 16,
    marginBottom: 40,
  },
  featureCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 16,
    gap: 16,
  },
  featureIcon: {
    width: 56,
    height: 56,
    borderRadius: 14,
    backgroundColor: COLORS.surfaceLight,
    justifyContent: 'center',
    alignItems: 'center',
  },
  featureContent: {
    flex: 1,
  },
  featureTitle: {
    fontSize: 17,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  featureDescription: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  goalsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
    marginBottom: 40,
  },
  goalCard: {
    width: (width - 60) / 2,
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'transparent',
  },
  goalCardSelected: {
    borderColor: COLORS.primary,
    backgroundColor: COLORS.surfaceLight,
  },
  goalLabel: {
    fontSize: 15,
    fontWeight: '500',
    color: COLORS.textSecondary,
    marginTop: 12,
  },
  goalLabelSelected: {
    color: COLORS.text,
  },
  checkmark: {
    position: 'absolute',
    top: 12,
    right: 12,
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  nameInput: {
    backgroundColor: COLORS.surface,
    borderRadius: 14,
    padding: 18,
    fontSize: 18,
    color: COLORS.text,
    borderWidth: 1,
    borderColor: COLORS.border,
    marginBottom: 24,
  },
  trialBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: 'rgba(255, 217, 61, 0.15)',
    paddingVertical: 10,
    paddingHorizontal: 16,
    borderRadius: 20,
    alignSelf: 'flex-start',
    marginBottom: 24,
  },
  trialBadgeText: {
    fontSize: 13,
    fontWeight: '700',
    color: COLORS.accent,
    letterSpacing: 1,
  },
  trialFeatures: {
    gap: 16,
    marginBottom: 40,
  },
  trialFeature: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  trialFeatureText: {
    fontSize: 16,
    color: COLORS.text,
  },
  trialDisclaimer: {
    fontSize: 12,
    color: COLORS.textMuted,
    textAlign: 'center',
    marginTop: 12,
  },
  primaryButton: {
    backgroundColor: COLORS.primary,
    borderRadius: 14,
    paddingVertical: 16,
    paddingHorizontal: 24,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
  },
  primaryButtonDisabled: {
    backgroundColor: COLORS.surfaceLight,
    opacity: 0.6,
  },
  primaryButtonText: {
    fontSize: 17,
    fontWeight: '600',
    color: COLORS.background,
  },
  skipButton: {
    paddingVertical: 16,
    alignItems: 'center',
  },
  skipButtonText: {
    fontSize: 15,
    color: COLORS.textSecondary,
  },
});
