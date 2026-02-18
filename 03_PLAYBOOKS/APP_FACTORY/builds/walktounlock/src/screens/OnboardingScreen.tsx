import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  Text,
  SafeAreaView,
  Pressable,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, SPACING, BORDER_RADIUS } from '../constants/theme';
import { Button } from '../components';
import { useApp } from '../context/AppContext';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { RootStackParamList } from '../constants/types';

interface OnboardingScreenProps {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Onboarding'>;
}

type OnboardingStep = 'welcome' | 'goal';

const STEP_OPTIONS = [
  { label: 'Easy', value: 100, description: '100 steps to unlock', icon: '\u{1F6B6}' },
  { label: 'Medium', value: 500, description: '500 steps to unlock', icon: '\u{1F3C3}' },
  { label: 'Hard', value: 1000, description: '1,000 steps to unlock', icon: '\u26A1' },
  { label: 'Extreme', value: 2000, description: '2,000 steps to unlock', icon: '\u{1F525}' },
];

export const OnboardingScreen: React.FC<OnboardingScreenProps> = ({ navigation }) => {
  const [step, setStep] = useState<OnboardingStep>('welcome');
  const [selectedGoal, setSelectedGoal] = useState(500);
  const { completeOnboarding } = useApp();

  const handleGetStarted = () => {
    setStep('goal');
  };

  const handleComplete = async () => {
    await completeOnboarding(selectedGoal);
    navigation.replace('Lock');
  };

  if (step === 'welcome') {
    return (
      <LinearGradient
        colors={['#1A1A1A', '#0D0D0D']}
        style={styles.container}
      >
        <SafeAreaView style={styles.safeArea}>
          <View style={styles.welcomeContent}>
            <View style={styles.logoContainer}>
              <Text style={styles.logoIcon}>{'\u{1F6B6}'}</Text>
              <Text style={styles.logoText}>WalkToUnlock</Text>
              <Text style={styles.tagline}>Walk first, scroll second.</Text>
            </View>

            <View style={styles.featuresContainer}>
              <View style={styles.featureRow}>
                <View style={styles.featureDot} />
                <Text style={styles.featureText}>
                  Set a daily step goal to unlock your phone
                </Text>
              </View>
              <View style={styles.featureRow}>
                <View style={styles.featureDot} />
                <Text style={styles.featureText}>
                  Track your progress with streaks and achievements
                </Text>
              </View>
              <View style={styles.featureRow}>
                <View style={styles.featureDot} />
                <Text style={styles.featureText}>
                  Build a healthy walking habit, one unlock at a time
                </Text>
              </View>
            </View>

            <Button
              title="Get Started"
              onPress={handleGetStarted}
              fullWidth
              size="large"
            />
          </View>
        </SafeAreaView>
      </LinearGradient>
    );
  }

  return (
    <LinearGradient
      colors={['#1A1A1A', '#0D0D0D']}
      style={styles.container}
    >
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.goalContent}>
          <Text style={styles.goalTitle}>Choose your daily goal</Text>
          <Text style={styles.goalSubtitle}>
            How many steps do you want to walk before unlocking your phone?
          </Text>

          <View style={styles.goalOptions}>
            {STEP_OPTIONS.map((option) => (
              <Pressable
                key={option.value}
                style={[
                  styles.goalCard,
                  selectedGoal === option.value && styles.goalCardSelected,
                ]}
                onPress={() => setSelectedGoal(option.value)}
              >
                <Text style={styles.goalIcon}>{option.icon}</Text>
                <View style={styles.goalCardContent}>
                  <Text style={[
                    styles.goalLabel,
                    selectedGoal === option.value && styles.goalLabelSelected,
                  ]}>
                    {option.label}
                  </Text>
                  <Text style={styles.goalDescription}>{option.description}</Text>
                </View>
                <View style={[
                  styles.radioOuter,
                  selectedGoal === option.value && styles.radioOuterSelected,
                ]}>
                  {selectedGoal === option.value && <View style={styles.radioInner} />}
                </View>
              </Pressable>
            ))}
          </View>

          <Text style={styles.goalHint}>
            You can change this later in Settings
          </Text>

          <Button
            title="Start Walking"
            onPress={handleComplete}
            fullWidth
            size="large"
          />
        </View>
      </SafeAreaView>
    </LinearGradient>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  safeArea: {
    flex: 1,
  },
  welcomeContent: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: SPACING.xl,
    paddingBottom: SPACING.xxl,
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: SPACING.xxl,
  },
  logoIcon: {
    fontSize: 72,
    marginBottom: SPACING.md,
  },
  logoText: {
    fontSize: 36,
    fontWeight: '800',
    color: COLORS.primary,
    letterSpacing: -1,
  },
  tagline: {
    fontSize: 18,
    color: COLORS.textSecondary,
    marginTop: SPACING.sm,
  },
  featuresContainer: {
    marginBottom: SPACING.xxl,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: SPACING.lg,
  },
  featureDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: COLORS.primary,
    marginTop: 6,
    marginRight: SPACING.md,
  },
  featureText: {
    fontSize: 17,
    color: COLORS.text,
    flex: 1,
    lineHeight: 24,
  },
  goalContent: {
    flex: 1,
    paddingHorizontal: SPACING.xl,
    paddingTop: SPACING.xxl,
    paddingBottom: SPACING.xxl,
  },
  goalTitle: {
    fontSize: 28,
    fontWeight: '800',
    color: COLORS.text,
    letterSpacing: -0.5,
    marginBottom: SPACING.sm,
  },
  goalSubtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    lineHeight: 24,
    marginBottom: SPACING.xl,
  },
  goalOptions: {
    flex: 1,
    justifyContent: 'center',
  },
  goalCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.lg,
    marginBottom: SPACING.md,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  goalCardSelected: {
    borderColor: COLORS.primary,
    backgroundColor: COLORS.backgroundLight,
  },
  goalIcon: {
    fontSize: 28,
    marginRight: SPACING.md,
  },
  goalCardContent: {
    flex: 1,
  },
  goalLabel: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.text,
  },
  goalLabelSelected: {
    color: COLORS.primary,
  },
  goalDescription: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  radioOuter: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: COLORS.backgroundLighter,
    justifyContent: 'center',
    alignItems: 'center',
  },
  radioOuterSelected: {
    borderColor: COLORS.primary,
  },
  radioInner: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: COLORS.primary,
  },
  goalHint: {
    fontSize: 14,
    color: COLORS.textMuted,
    textAlign: 'center',
    marginBottom: SPACING.lg,
  },
});
