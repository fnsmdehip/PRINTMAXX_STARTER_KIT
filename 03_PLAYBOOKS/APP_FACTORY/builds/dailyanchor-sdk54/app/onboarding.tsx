import { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import { useRouter } from 'expo-router';
import { COLORS, FOCUS_AREAS } from '../src/utils/constants';
import { useSettingsStore } from '../src/store';

const { width } = Dimensions.get('window');

type Step = 'welcome' | 'focus' | 'notifications' | 'ready';

const ONBOARDING_STEPS = [
  {
    id: 'welcome',
    emoji: '\u{1F64F}',
    title: 'Welcome to DailyAnchor',
    subtitle: 'Your daily companion for spiritual growth',
    description: 'Build consistent faith habits with daily devotionals, journaling, and habit tracking.',
  },
  {
    id: 'focus',
    emoji: '\u{1F3AF}',
    title: 'What brings you here?',
    subtitle: 'Help us personalize your experience',
    description: 'Select the area you want to focus on. You can change this later.',
  },
  {
    id: 'notifications',
    emoji: '\u{1F514}',
    title: 'Stay on track',
    subtitle: 'Daily reminders help build habits',
    description: 'Get a gentle reminder each morning to start your day anchored in faith.',
  },
  {
    id: 'ready',
    emoji: '\u{2728}',
    title: "You're all set!",
    subtitle: 'Your spiritual journey begins now',
    description: 'Start with today\'s devotional or jump into your first habit check.',
  },
];

function FeatureItem({ icon, text }: { icon: string; text: string }) {
  return (
    <View style={styles.featureItem}>
      <Text style={styles.featureIcon}>{icon}</Text>
      <Text style={styles.featureText}>{text}</Text>
    </View>
  );
}

export default function OnboardingScreen() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState<Step>('welcome');
  const [selectedFocus, setSelectedFocus] = useState<string | null>(null);
  const { updateSettings } = useSettingsStore();

  const currentStepData = ONBOARDING_STEPS.find((s) => s.id === currentStep);
  const stepIndex = ONBOARDING_STEPS.findIndex((s) => s.id === currentStep);

  const handleNext = () => {
    const steps: Step[] = ['welcome', 'focus', 'notifications', 'ready'];
    const currentIndex = steps.indexOf(currentStep);
    if (currentIndex < steps.length - 1) {
      setCurrentStep(steps[currentIndex + 1]);
    }
  };

  const handleFocusSelect = (focusId: string) => {
    setSelectedFocus(focusId);
    updateSettings({ focusArea: focusId as any });
  };

  const handleNotificationChoice = (enabled: boolean) => {
    updateSettings({ reminderEnabled: enabled });
    handleNext();
  };

  const handleComplete = () => {
    updateSettings({ onboardingCompleted: true });
    router.replace('/(tabs)');
  };

  const handleSkip = () => {
    updateSettings({ onboardingCompleted: true });
    router.replace('/(tabs)');
  };

  const renderContent = () => {
    switch (currentStep) {
      case 'welcome':
        return (
          <View style={styles.welcomeContent}>
            <View style={styles.featureList}>
              <FeatureItem icon="\u{1F4D6}" text="Daily devotional verses" />
              <FeatureItem icon="\u{1F4DD}" text="Gratitude journaling" />
              <FeatureItem icon="\u{2705}" text="Habit tracking" />
              <FeatureItem icon="\u{1F525}" text="Streak motivation" />
            </View>
            <TouchableOpacity style={styles.primaryButton} onPress={handleNext}>
              <Text style={styles.primaryButtonText}>Get started</Text>
            </TouchableOpacity>
          </View>
        );

      case 'focus':
        return (
          <View style={styles.focusContent}>
            {FOCUS_AREAS.map((area) => (
              <TouchableOpacity
                key={area.id}
                style={[
                  styles.focusOption,
                  selectedFocus === area.id && styles.focusOptionSelected,
                ]}
                onPress={() => handleFocusSelect(area.id)}
              >
                <Text
                  style={[
                    styles.focusTitle,
                    selectedFocus === area.id && styles.focusTitleSelected,
                  ]}
                >
                  {area.title}
                </Text>
                <Text style={styles.focusDescription}>{area.description}</Text>
              </TouchableOpacity>
            ))}
            <TouchableOpacity
              style={[styles.primaryButton, !selectedFocus && styles.buttonDisabled]}
              onPress={handleNext}
              disabled={!selectedFocus}
            >
              <Text style={styles.primaryButtonText}>Continue</Text>
            </TouchableOpacity>
          </View>
        );

      case 'notifications':
        return (
          <View style={styles.notificationContent}>
            <Text style={styles.notificationNote}>
              Recommended: 7:00 AM daily
            </Text>
            <TouchableOpacity
              style={styles.primaryButton}
              onPress={() => handleNotificationChoice(true)}
            >
              <Text style={styles.primaryButtonText}>Enable reminders</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.secondaryButton}
              onPress={() => handleNotificationChoice(false)}
            >
              <Text style={styles.secondaryButtonText}>Maybe later</Text>
            </TouchableOpacity>
          </View>
        );

      case 'ready':
        return (
          <View style={styles.readyContent}>
            <View style={styles.trialBadge}>
              <Text style={styles.trialText}>7-day free trial included</Text>
            </View>
            <TouchableOpacity style={styles.primaryButton} onPress={handleComplete}>
              <Text style={styles.primaryButtonText}>Start my journey</Text>
            </TouchableOpacity>
          </View>
        );
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        {stepIndex < ONBOARDING_STEPS.length - 1 && (
          <TouchableOpacity onPress={handleSkip}>
            <Text style={styles.skipText}>Skip</Text>
          </TouchableOpacity>
        )}
      </View>

      <View style={styles.content}>
        <View style={styles.stepIndicator}>
          {ONBOARDING_STEPS.map((_, index) => (
            <View
              key={index}
              style={[
                styles.stepDot,
                index === stepIndex && styles.stepDotActive,
                index < stepIndex && styles.stepDotCompleted,
              ]}
            />
          ))}
        </View>

        <Text style={styles.emoji}>{currentStepData?.emoji}</Text>
        <Text style={styles.title}>{currentStepData?.title}</Text>
        <Text style={styles.subtitle}>{currentStepData?.subtitle}</Text>
        <Text style={styles.description}>{currentStepData?.description}</Text>

        {renderContent()}
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
    padding: 16,
    minHeight: 50,
  },
  skipText: {
    fontSize: 16,
    color: COLORS.primary,
  },
  content: {
    flex: 1,
    alignItems: 'center',
    paddingHorizontal: 24,
    paddingTop: 20,
  },
  stepIndicator: {
    flexDirection: 'row',
    marginBottom: 32,
  },
  stepDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: COLORS.border,
    marginHorizontal: 4,
  },
  stepDotActive: {
    backgroundColor: COLORS.primary,
    width: 24,
  },
  stepDotCompleted: {
    backgroundColor: COLORS.primary,
  },
  emoji: {
    fontSize: 64,
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
    fontSize: 18,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 8,
  },
  description: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 32,
    paddingHorizontal: 16,
  },
  welcomeContent: {
    flex: 1,
    width: '100%',
  },
  featureList: {
    backgroundColor: COLORS.card,
    borderRadius: 16,
    padding: 20,
    marginBottom: 24,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
  },
  featureIcon: {
    fontSize: 24,
    marginRight: 16,
  },
  featureText: {
    fontSize: 16,
    color: COLORS.text,
  },
  focusContent: {
    flex: 1,
    width: '100%',
  },
  focusOption: {
    backgroundColor: COLORS.card,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  focusOptionSelected: {
    borderColor: COLORS.primary,
    backgroundColor: COLORS.primary + '10',
  },
  focusTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  focusTitleSelected: {
    color: COLORS.primary,
  },
  focusDescription: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  notificationContent: {
    flex: 1,
    width: '100%',
  },
  notificationNote: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 24,
  },
  readyContent: {
    flex: 1,
    width: '100%',
    alignItems: 'center',
  },
  trialBadge: {
    backgroundColor: COLORS.secondary + '20',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    marginBottom: 32,
  },
  trialText: {
    color: COLORS.secondary,
    fontWeight: '600',
  },
  primaryButton: {
    backgroundColor: COLORS.primary,
    paddingVertical: 16,
    paddingHorizontal: 32,
    borderRadius: 12,
    width: '100%',
    alignItems: 'center',
    marginBottom: 12,
  },
  primaryButtonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: '600',
  },
  secondaryButton: {
    paddingVertical: 16,
    paddingHorizontal: 32,
    borderRadius: 12,
    width: '100%',
    alignItems: 'center',
  },
  secondaryButtonText: {
    color: COLORS.primary,
    fontSize: 16,
  },
  buttonDisabled: {
    backgroundColor: COLORS.border,
  },
});
