import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Dimensions,
  ScrollView,
} from 'react-native';
import { router } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';

import { useUserStore } from '../src/stores/userStore';
import { COLORS, SOCIAL_PROOF } from '../src/utils/constants';
import { Gender } from '../src/types';

const { width } = Dimensions.get('window');

interface OnboardingStep {
  id: string;
  title: string;
  subtitle: string;
  icon: keyof typeof Ionicons.glyphMap;
  showSocialProof?: boolean;
}

const ONBOARDING_STEPS: OnboardingStep[] = [
  {
    id: 'welcome',
    title: 'Welcome to GlowMaxx',
    subtitle: 'Your daily companion for facial optimization and self-improvement',
    icon: 'sparkles',
    showSocialProof: true, // Show "Trusted by 50,000+" on first screen
  },
  {
    id: 'mewing',
    title: 'Master Mewing',
    subtitle: 'Track and improve your tongue posture for better facial structure',
    icon: 'happy-outline',
  },
  {
    id: 'routines',
    title: 'Daily Routines',
    subtitle: 'Skincare, facial exercises, and debloating protocols',
    icon: 'calendar-outline',
  },
  {
    id: 'progress',
    title: 'Track Progress',
    subtitle: 'Before/after photos to visualize your glow-up journey',
    icon: 'camera-outline',
  },
];

const GENDER_OPTIONS: { value: Gender; label: string; icon: keyof typeof Ionicons.glyphMap }[] = [
  { value: 'male', label: 'Male', icon: 'male' },
  { value: 'female', label: 'Female', icon: 'female' },
  { value: 'other', label: 'Other', icon: 'person-outline' },
];

export default function OnboardingScreen() {
  const [currentStep, setCurrentStep] = useState(0);
  const [selectedGender, setSelectedGender] = useState<Gender>('female');

  const { setGender, completeOnboarding, startTrial } = useUserStore();

  const isLastStep = currentStep === ONBOARDING_STEPS.length;
  const step = ONBOARDING_STEPS[currentStep];

  const handleNext = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    if (currentStep < ONBOARDING_STEPS.length) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleComplete = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    setGender(selectedGender);
    startTrial();
    completeOnboarding();
    router.replace('/(tabs)/home');
  };

  const handleGenderSelect = (gender: Gender) => {
    Haptics.selectionAsync();
    setSelectedGender(gender);
  };

  if (isLastStep) {
    // Gender selection screen
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.content}>
          <View style={styles.iconContainer}>
            <Ionicons name="person-outline" size={64} color={COLORS.primary} />
          </View>

          <Text style={styles.title}>Personalize Your Experience</Text>
          <Text style={styles.subtitle}>
            Select your gender to get tailored routines and exercises
          </Text>

          <View style={styles.genderGrid}>
            {GENDER_OPTIONS.map((option) => (
              <TouchableOpacity
                key={option.value}
                style={[
                  styles.genderOption,
                  selectedGender === option.value && styles.genderOptionSelected,
                ]}
                onPress={() => handleGenderSelect(option.value)}
              >
                <Ionicons
                  name={option.icon}
                  size={32}
                  color={
                    selectedGender === option.value ? COLORS.surface : COLORS.primary
                  }
                />
                <Text
                  style={[
                    styles.genderLabel,
                    selectedGender === option.value && styles.genderLabelSelected,
                  ]}
                >
                  {option.label}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        <View style={styles.footer}>
          <TouchableOpacity style={styles.startButton} onPress={handleComplete}>
            <Text style={styles.startButtonText}>Start 7-Day Free Trial</Text>
            <Ionicons name="arrow-forward" size={20} color={COLORS.surface} />
          </TouchableOpacity>

          <Text style={styles.trialNote}>
            Then $9.99/month. Cancel anytime.
          </Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      {/* Skip button */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => setCurrentStep(ONBOARDING_STEPS.length)}>
          <Text style={styles.skipText}>Skip</Text>
        </TouchableOpacity>
      </View>

      {/* Main content */}
      <View style={styles.content}>
        <View style={styles.iconContainer}>
          <Ionicons name={step.icon} size={80} color={COLORS.primary} />
        </View>

        <Text style={styles.title}>{step.title}</Text>
        <Text style={styles.subtitle}>{step.subtitle}</Text>

        {/* Social proof on first screen (like UMAX) */}
        {step.showSocialProof && (
          <View style={styles.socialProof}>
            <View style={styles.socialProofRow}>
              <Ionicons name="people" size={18} color={COLORS.success} />
              <Text style={styles.socialProofText}>{SOCIAL_PROOF.tagline}</Text>
            </View>
            <View style={styles.socialProofRow}>
              <Ionicons name="star" size={18} color={COLORS.accent} />
              <Text style={styles.socialProofText}>
                {SOCIAL_PROOF.rating} stars ({SOCIAL_PROOF.ratingCount} reviews)
              </Text>
            </View>
          </View>
        )}
      </View>

      {/* Pagination dots */}
      <View style={styles.pagination}>
        {ONBOARDING_STEPS.map((_, index) => (
          <View
            key={index}
            style={[
              styles.dot,
              index === currentStep && styles.dotActive,
            ]}
          />
        ))}
      </View>

      {/* Next button */}
      <View style={styles.footer}>
        <TouchableOpacity style={styles.nextButton} onPress={handleNext}>
          <Text style={styles.nextButtonText}>Next</Text>
          <Ionicons name="arrow-forward" size={20} color={COLORS.surface} />
        </TouchableOpacity>
      </View>
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
    paddingHorizontal: 20,
    paddingTop: 10,
  },
  skipText: {
    fontSize: 16,
    color: COLORS.textSecondary,
  },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 40,
  },
  iconContainer: {
    width: 140,
    height: 140,
    borderRadius: 70,
    backgroundColor: COLORS.primaryLight,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 40,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: 12,
  },
  subtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 24,
  },
  pagination: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 8,
    marginBottom: 40,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: COLORS.border,
  },
  dotActive: {
    width: 24,
    backgroundColor: COLORS.primary,
  },
  footer: {
    paddingHorizontal: 20,
    paddingBottom: 20,
  },
  nextButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.primary,
    paddingVertical: 16,
    borderRadius: 12,
    gap: 8,
  },
  nextButtonText: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.surface,
  },
  startButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.primary,
    paddingVertical: 16,
    borderRadius: 12,
    gap: 8,
  },
  startButtonText: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.surface,
  },
  trialNote: {
    fontSize: 13,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginTop: 12,
  },
  genderGrid: {
    flexDirection: 'row',
    gap: 16,
    marginTop: 40,
  },
  genderOption: {
    width: 100,
    height: 100,
    borderRadius: 16,
    backgroundColor: COLORS.surface,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: COLORS.border,
  },
  genderOptionSelected: {
    backgroundColor: COLORS.primary,
    borderColor: COLORS.primary,
  },
  genderLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.text,
    marginTop: 8,
  },
  genderLabelSelected: {
    color: COLORS.surface,
  },
  socialProof: {
    marginTop: 32,
    alignItems: 'center',
    gap: 8,
  },
  socialProofRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  socialProofText: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
});
