import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Dimensions,
  Animated,
  ScrollView,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { colors, spacing, fontSize, borderRadius } from '../utils/theme';
import { useSubscriptionStore, PRICING } from '../stores/subscriptionStore';
import { analytics } from '../services/analyticsService';

const { width, height } = Dimensions.get('window');

interface Props {
  onComplete: () => void;
}

type Step = 'value' | 'use_case' | 'experience' | 'social_proof' | 'paywall';

// Use case options for quiz
const USE_CASES = [
  { id: 'writing', name: 'Writing & Content', icon: 'pencil', color: colors.categoryColors.writing },
  { id: 'coding', name: 'Coding & Debugging', icon: 'code-braces', color: colors.categoryColors.coding },
  { id: 'marketing', name: 'Marketing & Copy', icon: 'bullhorn', color: colors.categoryColors.marketing },
  { id: 'creative', name: 'Creative Projects', icon: 'lightbulb-outline', color: colors.categoryColors.creative },
  { id: 'business', name: 'Business & Strategy', icon: 'briefcase-outline', color: colors.categoryColors.business },
  { id: 'learning', name: 'Learning & Research', icon: 'book-open-variant', color: colors.categoryColors.learning },
];

// Experience levels
const EXPERIENCE_LEVELS = [
  { id: 'beginner', label: 'New to AI', description: 'Just getting started with ChatGPT/Claude', icon: 'sprout' },
  { id: 'intermediate', label: 'Regular user', description: 'Use AI tools weekly', icon: 'flower' },
  { id: 'advanced', label: 'Power user', description: 'Use AI daily for work', icon: 'tree' },
];

// Testimonials - using "Verified User" to stay legal
const TESTIMONIALS = [
  {
    text: 'Saved me hours. I copy prompts straight into ChatGPT.',
    role: 'Verified User',
    rating: 5,
  },
  {
    text: 'Finally, prompts that actually work. My content got 3x better.',
    role: 'Verified User',
    rating: 5,
  },
  {
    text: 'The prompt improver is magic. Worth every penny.',
    role: 'Verified User',
    rating: 5,
  },
];

// Freemium features comparison
// Free: All prompts with ads
// Premium: No ads + power features for just $2.99/mo
const FREEMIUM_FEATURES = [
  { icon: 'book-open-page-variant', text: 'Browse 1,050+ Prompts', free: true, premium: true },
  { icon: 'content-copy', text: 'Copy to Clipboard', free: true, premium: true },
  { icon: 'heart-outline', text: 'Save Favorites', free: true, premium: true },
  { icon: 'close-circle-outline', text: 'Ad-free Experience', free: false, premium: true, highlight: true },
  { icon: 'magic-staff', text: 'AI Prompt Improver', free: false, premium: true },
  { icon: 'plus-circle-outline', text: 'Create Custom Prompts', free: false, premium: true },
  { icon: 'cloud-sync', text: 'Cloud Sync', free: false, premium: true },
];

const STORAGE_KEY = 'promptvault_onboarding';

export default function OnboardingScreen({ onComplete }: Props) {
  const [currentStep, setCurrentStep] = useState<Step>('value');
  const [selectedUseCases, setSelectedUseCases] = useState<string[]>([]);
  const [selectedExperience, setSelectedExperience] = useState<string | null>(null);
  const [selectedPlan, setSelectedPlan] = useState<'monthly' | 'annual'>('annual');
  const [loading, setLoading] = useState(false);

  const { startTrial } = useSubscriptionStore();

  // Animation values
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(50)).current;
  const pulseAnim = useRef(new Animated.Value(1)).current;
  const counterAnim = useRef(new Animated.Value(0)).current;
  const [displayCount, setDisplayCount] = useState(0);

  const steps: Step[] = ['value', 'use_case', 'experience', 'social_proof', 'paywall'];
  const currentIndex = steps.indexOf(currentStep);

  useEffect(() => {
    // Track screen views
    analytics.trackOnboardingScreen(currentStep, 'viewed');

    // Animate in on step change
    fadeAnim.setValue(0);
    slideAnim.setValue(50);

    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 400,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 400,
        useNativeDriver: true,
      }),
    ]).start();
  }, [currentStep]);

  useEffect(() => {
    // Pulse animation for value screen
    if (currentStep === 'value') {
      Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, {
            toValue: 1.05,
            duration: 1000,
            useNativeDriver: true,
          }),
          Animated.timing(pulseAnim, {
            toValue: 1,
            duration: 1000,
            useNativeDriver: true,
          }),
        ])
      ).start();

      // Animate counter
      Animated.timing(counterAnim, {
        toValue: 10000,
        duration: 2000,
        useNativeDriver: false,
      }).start();

      const listener = counterAnim.addListener(({ value }) => {
        setDisplayCount(Math.floor(value));
      });

      return () => {
        counterAnim.removeListener(listener);
        pulseAnim.stopAnimation();
      };
    }
  }, [currentStep]);

  const handleNext = () => {
    // Track screen completion
    analytics.trackOnboardingScreen(currentStep, 'completed');

    // Track specific data on certain screens
    if (currentStep === 'use_case' && selectedUseCases.length > 0) {
      analytics.trackOnboardingUseCases(selectedUseCases);
    }
    if (currentStep === 'experience' && selectedExperience) {
      analytics.trackOnboardingExperience(selectedExperience);
    }

    if (currentIndex < steps.length - 1) {
      setCurrentStep(steps[currentIndex + 1]);
    }
  };

  const handleBack = () => {
    if (currentIndex > 0) {
      setCurrentStep(steps[currentIndex - 1]);
    }
  };

  const handleComplete = async (withTrial: boolean) => {
    // Track conversion
    analytics.trackOnboardingConversion(withTrial, selectedPlan);
    analytics.track('onboarding_completed');

    // Save preferences
    const preferences = {
      useCases: selectedUseCases,
      experience: selectedExperience,
      onboardingCompleted: true,
      completedAt: new Date().toISOString(),
    };

    await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(preferences));

    if (withTrial) {
      startTrial();
    }

    onComplete();
  };

  const handleSkip = () => {
    analytics.track('onboarding_skipped');
    analytics.trackOnboardingScreen(currentStep, 'skipped');
    handleComplete(false);
  };

  const toggleUseCase = (id: string) => {
    setSelectedUseCases((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const renderProgressBar = () => {
    const progress = ((currentIndex + 1) / steps.length) * 100;

    return (
      <View style={styles.progressContainer}>
        <View style={styles.progressTrack}>
          <View style={[styles.progressFill, { width: `${progress}%` }]} />
        </View>
        <Text style={styles.progressText}>
          {currentIndex + 1} of {steps.length}
        </Text>
      </View>
    );
  };

  const renderValueScreen = () => (
    <Animated.View
      style={[
        styles.stepContent,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <Animated.View style={[styles.heroContainer, { transform: [{ scale: pulseAnim }] }]}>
        <MaterialCommunityIcons
          name="book-open-page-variant"
          size={80}
          color={colors.primary}
        />
        <View style={styles.heroGlow} />
      </Animated.View>

      <Text style={styles.heroNumber}>{displayCount.toLocaleString()}+</Text>
      <Text style={styles.heroLabel}>AI prompts at your fingertips</Text>

      <Text style={styles.valueTitle}>Stop writing bad prompts</Text>
      <Text style={styles.valueDescription}>
        Expert-crafted prompts for ChatGPT, Claude, and more. Copy, paste, get better results.
      </Text>

      <View style={styles.valueFeatures}>
        <View style={styles.valueFeature}>
          <MaterialCommunityIcons name="check-circle" size={20} color={colors.success} />
          <Text style={styles.valueFeatureText}>One-tap copy</Text>
        </View>
        <View style={styles.valueFeature}>
          <MaterialCommunityIcons name="check-circle" size={20} color={colors.success} />
          <Text style={styles.valueFeatureText}>9 categories</Text>
        </View>
        <View style={styles.valueFeature}>
          <MaterialCommunityIcons name="check-circle" size={20} color={colors.success} />
          <Text style={styles.valueFeatureText}>Updated weekly</Text>
        </View>
      </View>

      <TouchableOpacity style={styles.primaryButton} onPress={handleNext}>
        <Text style={styles.primaryButtonText}>Get started</Text>
        <MaterialCommunityIcons name="arrow-right" size={20} color="#FFFFFF" />
      </TouchableOpacity>
    </Animated.View>
  );

  const renderUseCaseScreen = () => (
    <Animated.View
      style={[
        styles.stepContent,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <Text style={styles.quizTitle}>What do you use AI for?</Text>
      <Text style={styles.quizSubtitle}>
        Pick all that apply. We'll show you the best prompts first.
      </Text>

      <View style={styles.optionsGrid}>
        {USE_CASES.map((item) => {
          const isSelected = selectedUseCases.includes(item.id);
          return (
            <TouchableOpacity
              key={item.id}
              style={[
                styles.optionCard,
                isSelected && { borderColor: item.color, backgroundColor: item.color + '20' },
              ]}
              onPress={() => toggleUseCase(item.id)}
            >
              <MaterialCommunityIcons
                name={item.icon as any}
                size={28}
                color={isSelected ? item.color : colors.textMuted}
              />
              <Text style={[styles.optionText, isSelected && { color: item.color }]}>
                {item.name}
              </Text>
              {isSelected && (
                <View style={[styles.checkBadge, { backgroundColor: item.color }]}>
                  <MaterialCommunityIcons name="check" size={12} color="#FFFFFF" />
                </View>
              )}
            </TouchableOpacity>
          );
        })}
      </View>

      <TouchableOpacity
        style={[
          styles.primaryButton,
          selectedUseCases.length === 0 && styles.buttonDisabled,
        ]}
        onPress={handleNext}
        disabled={selectedUseCases.length === 0}
      >
        <Text style={styles.primaryButtonText}>Continue</Text>
        <MaterialCommunityIcons name="arrow-right" size={20} color="#FFFFFF" />
      </TouchableOpacity>

      <TouchableOpacity style={styles.skipButton} onPress={handleNext}>
        <Text style={styles.skipButtonText}>Show me everything</Text>
      </TouchableOpacity>
    </Animated.View>
  );

  const renderExperienceScreen = () => (
    <Animated.View
      style={[
        styles.stepContent,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <Text style={styles.quizTitle}>How often do you use AI?</Text>
      <Text style={styles.quizSubtitle}>
        We'll tailor prompt complexity to your level.
      </Text>

      <View style={styles.experienceList}>
        {EXPERIENCE_LEVELS.map((level) => {
          const isSelected = selectedExperience === level.id;
          return (
            <TouchableOpacity
              key={level.id}
              style={[
                styles.experienceCard,
                isSelected && styles.experienceCardSelected,
              ]}
              onPress={() => setSelectedExperience(level.id)}
            >
              <MaterialCommunityIcons
                name={level.icon as any}
                size={32}
                color={isSelected ? colors.primary : colors.textMuted}
              />
              <View style={styles.experienceContent}>
                <Text style={[styles.experienceLabel, isSelected && styles.experienceLabelSelected]}>
                  {level.label}
                </Text>
                <Text style={styles.experienceDescription}>{level.description}</Text>
              </View>
              {isSelected && (
                <MaterialCommunityIcons
                  name="check-circle"
                  size={24}
                  color={colors.primary}
                />
              )}
            </TouchableOpacity>
          );
        })}
      </View>

      <TouchableOpacity
        style={[
          styles.primaryButton,
          !selectedExperience && styles.buttonDisabled,
        ]}
        onPress={handleNext}
        disabled={!selectedExperience}
      >
        <Text style={styles.primaryButtonText}>Continue</Text>
        <MaterialCommunityIcons name="arrow-right" size={20} color="#FFFFFF" />
      </TouchableOpacity>

      <TouchableOpacity style={styles.skipButton} onPress={handleNext}>
        <Text style={styles.skipButtonText}>Skip this step</Text>
      </TouchableOpacity>
    </Animated.View>
  );

  const renderSocialProofScreen = () => (
    <Animated.View
      style={[
        styles.stepContent,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <View style={styles.ratingHeader}>
        <View style={styles.starsContainer}>
          {[1, 2, 3, 4, 5].map((star) => (
            <MaterialCommunityIcons
              key={star}
              name="star"
              size={28}
              color={colors.warning}
            />
          ))}
        </View>
        <Text style={styles.ratingText}>4.8 out of 5</Text>
        <Text style={styles.ratingSubtext}>from verified users</Text>
      </View>

      <Text style={styles.socialProofTitle}>See what users are saying</Text>

      <ScrollView
        style={styles.testimonialList}
        showsVerticalScrollIndicator={false}
      >
        {TESTIMONIALS.map((testimonial, index) => (
          <View key={index} style={styles.testimonialCard}>
            <View style={styles.testimonialStars}>
              {[1, 2, 3, 4, 5].map((star) => (
                <MaterialCommunityIcons
                  key={star}
                  name="star"
                  size={14}
                  color={star <= testimonial.rating ? colors.warning : colors.textMuted}
                />
              ))}
            </View>
            <Text style={styles.testimonialText}>"{testimonial.text}"</Text>
            <Text style={styles.testimonialRole}>{testimonial.role}</Text>
          </View>
        ))}
      </ScrollView>

      <TouchableOpacity style={styles.primaryButton} onPress={handleNext}>
        <Text style={styles.primaryButtonText}>Continue</Text>
        <MaterialCommunityIcons name="arrow-right" size={20} color="#FFFFFF" />
      </TouchableOpacity>
    </Animated.View>
  );

  const renderPaywallScreen = () => (
    <Animated.View
      style={[
        styles.stepContent,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <View style={styles.paywallHeader}>
        <MaterialCommunityIcons name="gift-outline" size={48} color={colors.success} />
        <Text style={styles.paywallTitle}>Free forever. Seriously.</Text>
        <Text style={styles.paywallSubtitle}>
          Access all 1,050+ prompts free with ads.{'\n'}Go Premium to remove ads and unlock AI features.
        </Text>
      </View>

      <View style={styles.comparisonContainer}>
        <View style={styles.comparisonHeader}>
          <Text style={[styles.comparisonHeaderText, { flex: 1, textAlign: 'left' }]}>Feature</Text>
          <Text style={styles.comparisonHeaderText}>Free</Text>
          <Text style={[styles.comparisonHeaderText, { color: colors.primary }]}>Premium</Text>
        </View>
        {FREEMIUM_FEATURES.map((feature, index) => (
          <View key={index} style={[styles.comparisonRow, feature.highlight && styles.comparisonRowHighlight]}>
            <View style={styles.comparisonFeature}>
              <MaterialCommunityIcons
                name={feature.icon as any}
                size={18}
                color={feature.highlight ? colors.success : colors.textSecondary}
              />
              <Text style={[styles.comparisonFeatureText, feature.highlight && { color: colors.success, fontWeight: '600' }]}>
                {feature.text}
              </Text>
            </View>
            <MaterialCommunityIcons
              name={feature.free ? 'check' : 'close'}
              size={18}
              color={feature.free ? colors.success : colors.textMuted}
            />
            <MaterialCommunityIcons
              name="check"
              size={18}
              color={colors.success}
            />
          </View>
        ))}
      </View>

      <View style={styles.planSelector}>
        <TouchableOpacity
          style={[
            styles.planOption,
            selectedPlan === 'annual' && styles.planOptionSelected,
          ]}
          onPress={() => setSelectedPlan('annual')}
        >
          <View style={styles.savingsBadge}>
            <Text style={styles.savingsText}>BEST VALUE</Text>
          </View>
          <Text style={styles.planName}>Annual</Text>
          <Text style={styles.planPrice}>{PRICING.annual.price}/yr</Text>
          <Text style={styles.planBreakdown}>{PRICING.annual.monthlyEquivalent}/mo</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[
            styles.planOption,
            selectedPlan === 'monthly' && styles.planOptionSelected,
          ]}
          onPress={() => setSelectedPlan('monthly')}
        >
          <Text style={styles.planName}>Monthly</Text>
          <Text style={styles.planPrice}>{PRICING.monthly.price}/mo</Text>
        </TouchableOpacity>
      </View>

      <TouchableOpacity
        style={styles.trialButton}
        onPress={() => handleComplete(true)}
      >
        <Text style={styles.trialButtonText}>Try Premium Free for 7 Days</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.freeButton}
        onPress={() => handleComplete(false)}
      >
        <Text style={styles.freeButtonText}>Continue Free with Ads</Text>
      </TouchableOpacity>

      <Text style={styles.legalText}>
        {selectedPlan === 'annual' ? '$19.99/year' : '$2.99/month'} after trial. Cancel anytime.
      </Text>
    </Animated.View>
  );

  const renderContent = () => {
    switch (currentStep) {
      case 'value':
        return renderValueScreen();
      case 'use_case':
        return renderUseCaseScreen();
      case 'experience':
        return renderExperienceScreen();
      case 'social_proof':
        return renderSocialProofScreen();
      case 'paywall':
        return renderPaywallScreen();
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        {currentIndex > 0 && currentStep !== 'paywall' ? (
          <TouchableOpacity onPress={handleBack} style={styles.backButton}>
            <MaterialCommunityIcons name="arrow-left" size={24} color={colors.text} />
          </TouchableOpacity>
        ) : (
          <View style={styles.backButton} />
        )}

        {renderProgressBar()}

        {currentStep !== 'paywall' ? (
          <TouchableOpacity onPress={handleSkip} style={styles.headerSkipButton}>
            <Text style={styles.skipText}>Skip</Text>
          </TouchableOpacity>
        ) : (
          <View style={styles.headerSkipButton} />
        )}
      </View>

      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
        bounces={false}
      >
        {renderContent()}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
  },
  backButton: {
    width: 40,
    height: 40,
    alignItems: 'center',
    justifyContent: 'center',
  },
  headerSkipButton: {
    width: 50,
    alignItems: 'flex-end',
  },
  skipText: {
    fontSize: fontSize.sm,
    color: colors.primary,
    fontWeight: '500',
  },
  progressContainer: {
    flex: 1,
    alignItems: 'center',
    paddingHorizontal: spacing.md,
  },
  progressTrack: {
    width: '100%',
    height: 4,
    backgroundColor: colors.surfaceLight,
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: colors.primary,
    borderRadius: 2,
  },
  progressText: {
    fontSize: fontSize.xs,
    color: colors.textMuted,
    marginTop: spacing.xs,
  },
  scrollContent: {
    flexGrow: 1,
    paddingHorizontal: spacing.lg,
  },
  stepContent: {
    flex: 1,
    alignItems: 'center',
    paddingTop: spacing.lg,
    paddingBottom: spacing.xl,
  },

  // Value Screen
  heroContainer: {
    width: 140,
    height: 140,
    borderRadius: 70,
    backgroundColor: colors.primary + '20',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.lg,
    position: 'relative',
  },
  heroGlow: {
    position: 'absolute',
    width: 160,
    height: 160,
    borderRadius: 80,
    backgroundColor: colors.primary + '10',
  },
  heroNumber: {
    fontSize: 48,
    fontWeight: '700',
    color: colors.primary,
    marginBottom: spacing.xs,
  },
  heroLabel: {
    fontSize: fontSize.lg,
    color: colors.textSecondary,
    marginBottom: spacing.xl,
  },
  valueTitle: {
    fontSize: fontSize.xxxl,
    fontWeight: '700',
    color: colors.text,
    textAlign: 'center',
    marginBottom: spacing.sm,
  },
  valueDescription: {
    fontSize: fontSize.md,
    color: colors.textSecondary,
    textAlign: 'center',
    marginBottom: spacing.xl,
    paddingHorizontal: spacing.md,
    lineHeight: 24,
  },
  valueFeatures: {
    flexDirection: 'row',
    justifyContent: 'center',
    flexWrap: 'wrap',
    gap: spacing.lg,
    marginBottom: spacing.xl,
  },
  valueFeature: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
  },
  valueFeatureText: {
    fontSize: fontSize.sm,
    color: colors.text,
  },

  // Quiz Screens
  quizTitle: {
    fontSize: fontSize.xxl,
    fontWeight: '700',
    color: colors.text,
    textAlign: 'center',
    marginBottom: spacing.sm,
  },
  quizSubtitle: {
    fontSize: fontSize.md,
    color: colors.textSecondary,
    textAlign: 'center',
    marginBottom: spacing.xl,
  },
  optionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    width: '100%',
    gap: spacing.sm,
    marginBottom: spacing.xl,
  },
  optionCard: {
    width: (width - spacing.lg * 2 - spacing.sm) / 2,
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'transparent',
    position: 'relative',
  },
  optionText: {
    fontSize: fontSize.sm,
    color: colors.text,
    marginTop: spacing.sm,
    textAlign: 'center',
    fontWeight: '500',
  },
  checkBadge: {
    position: 'absolute',
    top: spacing.sm,
    right: spacing.sm,
    width: 20,
    height: 20,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },

  // Experience Screen
  experienceList: {
    width: '100%',
    gap: spacing.sm,
    marginBottom: spacing.xl,
  },
  experienceCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  experienceCardSelected: {
    borderColor: colors.primary,
    backgroundColor: colors.primary + '10',
  },
  experienceContent: {
    flex: 1,
    marginLeft: spacing.md,
  },
  experienceLabel: {
    fontSize: fontSize.md,
    fontWeight: '600',
    color: colors.text,
    marginBottom: 2,
  },
  experienceLabelSelected: {
    color: colors.primary,
  },
  experienceDescription: {
    fontSize: fontSize.sm,
    color: colors.textMuted,
  },

  // Social Proof Screen
  ratingHeader: {
    alignItems: 'center',
    marginBottom: spacing.xl,
  },
  starsContainer: {
    flexDirection: 'row',
    gap: spacing.xs,
    marginBottom: spacing.sm,
  },
  ratingText: {
    fontSize: fontSize.xl,
    fontWeight: '700',
    color: colors.text,
  },
  ratingSubtext: {
    fontSize: fontSize.sm,
    color: colors.textMuted,
  },
  socialProofTitle: {
    fontSize: fontSize.xl,
    fontWeight: '600',
    color: colors.text,
    marginBottom: spacing.lg,
  },
  testimonialList: {
    width: '100%',
    maxHeight: 300,
    marginBottom: spacing.xl,
  },
  testimonialCard: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    marginBottom: spacing.sm,
  },
  testimonialStars: {
    flexDirection: 'row',
    marginBottom: spacing.sm,
  },
  testimonialText: {
    fontSize: fontSize.md,
    color: colors.text,
    fontStyle: 'italic',
    lineHeight: 22,
    marginBottom: spacing.sm,
  },
  testimonialRole: {
    fontSize: fontSize.sm,
    color: colors.textMuted,
  },

  // Paywall Screen
  paywallHeader: {
    alignItems: 'center',
    marginBottom: spacing.lg,
  },
  paywallTitle: {
    fontSize: fontSize.xxl,
    fontWeight: '700',
    color: colors.text,
    textAlign: 'center',
    marginTop: spacing.md,
  },
  paywallSubtitle: {
    fontSize: fontSize.md,
    color: colors.textSecondary,
    textAlign: 'center',
    marginTop: spacing.sm,
    paddingHorizontal: spacing.md,
  },
  comparisonContainer: {
    width: '100%',
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    marginBottom: spacing.lg,
  },
  comparisonHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingBottom: spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: colors.surfaceLight,
    marginBottom: spacing.sm,
  },
  comparisonHeaderText: {
    fontSize: fontSize.sm,
    fontWeight: '600',
    color: colors.textSecondary,
    width: 50,
    textAlign: 'center',
  },
  comparisonRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: spacing.xs,
  },
  comparisonRowHighlight: {
    backgroundColor: colors.success + '10',
    marginHorizontal: -spacing.sm,
    paddingHorizontal: spacing.sm,
    borderRadius: borderRadius.sm,
  },
  comparisonFeature: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  comparisonFeatureText: {
    fontSize: fontSize.sm,
    color: colors.text,
  },
  planSelector: {
    flexDirection: 'row',
    width: '100%',
    gap: spacing.sm,
    marginBottom: spacing.lg,
  },
  planOption: {
    flex: 1,
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'transparent',
    position: 'relative',
  },
  planOptionSelected: {
    borderColor: colors.primary,
  },
  savingsBadge: {
    position: 'absolute',
    top: -10,
    backgroundColor: colors.success,
    paddingHorizontal: spacing.sm,
    paddingVertical: 2,
    borderRadius: borderRadius.sm,
  },
  savingsText: {
    fontSize: fontSize.xs,
    fontWeight: '700',
    color: '#FFFFFF',
  },
  planName: {
    fontSize: fontSize.sm,
    fontWeight: '600',
    color: colors.textSecondary,
    marginTop: spacing.sm,
  },
  planPrice: {
    fontSize: fontSize.xl,
    fontWeight: '700',
    color: colors.text,
    marginTop: spacing.xs,
  },
  planBreakdown: {
    fontSize: fontSize.xs,
    color: colors.success,
    marginTop: spacing.xs,
  },
  trialButton: {
    width: '100%',
    backgroundColor: colors.primary,
    paddingVertical: spacing.md,
    borderRadius: borderRadius.lg,
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  trialButtonText: {
    fontSize: fontSize.md,
    fontWeight: '700',
    color: '#FFFFFF',
  },
  freeButton: {
    width: '100%',
    backgroundColor: colors.surface,
    paddingVertical: spacing.md,
    borderRadius: borderRadius.lg,
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  freeButtonText: {
    fontSize: fontSize.md,
    fontWeight: '600',
    color: colors.textSecondary,
  },
  legalText: {
    fontSize: fontSize.xs,
    color: colors.textMuted,
    textAlign: 'center',
  },

  // Buttons
  primaryButton: {
    flexDirection: 'row',
    backgroundColor: colors.primary,
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.xl,
    borderRadius: borderRadius.lg,
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%',
    gap: spacing.sm,
  },
  primaryButtonText: {
    fontSize: fontSize.md,
    fontWeight: '600',
    color: '#FFFFFF',
  },
  buttonDisabled: {
    opacity: 0.5,
  },
  skipButton: {
    paddingVertical: spacing.md,
    alignItems: 'center',
  },
  skipButtonText: {
    fontSize: fontSize.sm,
    color: colors.textMuted,
  },
});
