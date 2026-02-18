import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  TouchableOpacity,
} from 'react-native';
import { router } from 'expo-router';
import { COLORS, SPACING, TYPOGRAPHY, DEFAULT_BLOCKED_APPS } from '../src/utils/constants';
import { useUserStore } from '../src/stores/userStore';

type Step = 'welcome' | 'timer' | 'apps' | 'notifications' | 'ready';

export default function OnboardingScreen() {
  const [currentStep, setCurrentStep] = useState<Step>('welcome');
  const [workDuration, setWorkDuration] = useState(25);
  const [breakDuration, setBreakDuration] = useState(5);
  const [selectedApps, setSelectedApps] = useState<string[]>([
    DEFAULT_BLOCKED_APPS[0].bundleId,
    DEFAULT_BLOCKED_APPS[1].bundleId,
    DEFAULT_BLOCKED_APPS[2].bundleId,
  ]);

  const { setWorkDuration: setUserWorkDuration, setBreakDuration: setUserBreakDuration, setBlockedApps, startTrial, completeOnboarding, setNotificationsEnabled } = useUserStore();

  const handleNext = () => {
    const steps: Step[] = ['welcome', 'timer', 'apps', 'notifications', 'ready'];
    const currentIndex = steps.indexOf(currentStep);
    if (currentIndex < steps.length - 1) {
      setCurrentStep(steps[currentIndex + 1]);
    }
  };

  const toggleApp = (bundleId: string) => {
    setSelectedApps((prev) =>
      prev.includes(bundleId)
        ? prev.filter((id) => id !== bundleId)
        : [...prev, bundleId]
    );
  };

  const handleNotifications = async (enabled: boolean) => {
    setNotificationsEnabled(enabled);
    handleNext();
  };

  const handleComplete = () => {
    setUserWorkDuration(workDuration);
    setUserBreakDuration(breakDuration);
    const blockedAppsToSet = DEFAULT_BLOCKED_APPS.filter(app => selectedApps.includes(app.bundleId));
    setBlockedApps(blockedAppsToSet);
    startTrial();
    completeOnboarding();
    router.replace('/(tabs)');
  };

  const handleSkip = () => {
    startTrial();
    completeOnboarding();
    router.replace('/(tabs)');
  };

  const renderContent = () => {
    switch (currentStep) {
      case 'welcome':
        return (
          <View style={styles.stepContent}>
            <Text style={styles.emoji}>{'\u{1F4DA}'}</Text>
            <Text style={styles.title}>Welcome to LearnLock</Text>
            <Text style={styles.subtitle}>Focus better. Study smarter.</Text>
            <Text style={styles.description}>
              Block distracting apps during study sessions. Stay focused with our Pomodoro timer.
            </Text>
            <View style={styles.featureList}>
              <FeatureItem icon={'\u{23F1}'} text="Pomodoro-style timer" />
              <FeatureItem icon={'\u{1F6AB}'} text="App blocking during sessions" />
              <FeatureItem icon={'\u{1F525}'} text="Streak tracking" />
              <FeatureItem icon={'\u{1F4CA}'} text="Study statistics" />
            </View>
            <TouchableOpacity style={styles.primaryButton} onPress={handleNext}>
              <Text style={styles.primaryButtonText}>Get started</Text>
            </TouchableOpacity>
          </View>
        );

      case 'timer':
        return (
          <View style={styles.stepContent}>
            <Text style={styles.emoji}>{'\u{23F1}'}</Text>
            <Text style={styles.title}>Set your timer</Text>
            <Text style={styles.description}>
              Choose how long you want to focus and how long your breaks should be.
            </Text>
            <View style={styles.timerSetting}>
              <Text style={styles.settingLabel}>Focus time</Text>
              <View style={styles.durationControl}>
                <TouchableOpacity
                  style={styles.durationButton}
                  onPress={() => setWorkDuration(Math.max(5, workDuration - 5))}
                >
                  <Text style={styles.durationButtonText}>-</Text>
                </TouchableOpacity>
                <Text style={styles.durationValue}>{workDuration} min</Text>
                <TouchableOpacity
                  style={styles.durationButton}
                  onPress={() => setWorkDuration(Math.min(60, workDuration + 5))}
                >
                  <Text style={styles.durationButtonText}>+</Text>
                </TouchableOpacity>
              </View>
            </View>
            <View style={styles.timerSetting}>
              <Text style={styles.settingLabel}>Break time</Text>
              <View style={styles.durationControl}>
                <TouchableOpacity
                  style={[styles.durationButton, styles.breakButton]}
                  onPress={() => setBreakDuration(Math.max(1, breakDuration - 1))}
                >
                  <Text style={styles.durationButtonText}>-</Text>
                </TouchableOpacity>
                <Text style={styles.durationValue}>{breakDuration} min</Text>
                <TouchableOpacity
                  style={[styles.durationButton, styles.breakButton]}
                  onPress={() => setBreakDuration(Math.min(15, breakDuration + 1))}
                >
                  <Text style={styles.durationButtonText}>+</Text>
                </TouchableOpacity>
              </View>
            </View>
            <TouchableOpacity style={styles.primaryButton} onPress={handleNext}>
              <Text style={styles.primaryButtonText}>Continue</Text>
            </TouchableOpacity>
          </View>
        );

      case 'apps':
        return (
          <View style={styles.stepContent}>
            <Text style={styles.emoji}>{'\u{1F6AB}'}</Text>
            <Text style={styles.title}>Block distracting apps</Text>
            <Text style={styles.description}>
              Select apps to block during your study sessions. You can change this later.
            </Text>
            <View style={styles.appList}>
              {DEFAULT_BLOCKED_APPS.map((app) => (
                <TouchableOpacity
                  key={app.bundleId}
                  style={[
                    styles.appItem,
                    selectedApps.includes(app.bundleId) && styles.appItemSelected,
                  ]}
                  onPress={() => toggleApp(app.bundleId)}
                >
                  <Text style={styles.appName}>{app.name}</Text>
                  {selectedApps.includes(app.bundleId) && (
                    <Text style={styles.checkmark}>{'\u{2713}'}</Text>
                  )}
                </TouchableOpacity>
              ))}
            </View>
            <TouchableOpacity
              style={[styles.primaryButton, selectedApps.length === 0 && styles.buttonDisabled]}
              onPress={handleNext}
              disabled={selectedApps.length === 0}
            >
              <Text style={styles.primaryButtonText}>
                Block {selectedApps.length} apps
              </Text>
            </TouchableOpacity>
          </View>
        );

      case 'notifications':
        return (
          <View style={styles.stepContent}>
            <Text style={styles.emoji}>{'\u{1F514}'}</Text>
            <Text style={styles.title}>Stay on track</Text>
            <Text style={styles.description}>
              Get reminders to study and notifications when your timer is complete.
            </Text>
            <TouchableOpacity
              style={styles.primaryButton}
              onPress={() => handleNotifications(true)}
            >
              <Text style={styles.primaryButtonText}>Enable notifications</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.secondaryButton}
              onPress={() => handleNotifications(false)}
            >
              <Text style={styles.secondaryButtonText}>Maybe later</Text>
            </TouchableOpacity>
          </View>
        );

      case 'ready':
        return (
          <View style={styles.stepContent}>
            <Text style={styles.emoji}>{'\u{1F3C6}'}</Text>
            <Text style={styles.title}>You're ready!</Text>
            <Text style={styles.description}>
              Your {workDuration}-minute focus sessions are set up. {selectedApps.length} apps will be blocked.
            </Text>
            <View style={styles.trialBadge}>
              <Text style={styles.trialText}>7-day free trial included</Text>
            </View>
            <TouchableOpacity style={styles.primaryButton} onPress={handleComplete}>
              <Text style={styles.primaryButtonText}>Start studying</Text>
            </TouchableOpacity>
          </View>
        );
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={handleSkip}>
          <Text style={styles.skipText}>Skip</Text>
        </TouchableOpacity>
      </View>
      {renderContent()}
    </SafeAreaView>
  );
}

function FeatureItem({ icon, text }: { icon: string; text: string }) {
  return (
    <View style={styles.featureItem}>
      <Text style={styles.featureIcon}>{icon}</Text>
      <Text style={styles.featureText}>{text}</Text>
    </View>
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
    padding: SPACING.lg,
  },
  skipText: {
    ...TYPOGRAPHY.body,
    color: COLORS.primary,
  },
  stepContent: {
    flex: 1,
    alignItems: 'center',
    paddingHorizontal: SPACING.lg,
    paddingTop: SPACING.xl,
  },
  emoji: {
    fontSize: 64,
    marginBottom: SPACING.lg,
  },
  title: {
    ...TYPOGRAPHY.h1,
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: SPACING.sm,
  },
  subtitle: {
    ...TYPOGRAPHY.h3,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: SPACING.sm,
  },
  description: {
    ...TYPOGRAPHY.body,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: SPACING.xl,
    paddingHorizontal: SPACING.md,
  },
  featureList: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.lg,
    width: '100%',
    marginBottom: SPACING.xl,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: SPACING.sm,
  },
  featureIcon: {
    fontSize: 24,
    marginRight: SPACING.md,
  },
  featureText: {
    ...TYPOGRAPHY.body,
    color: COLORS.text,
  },
  timerSetting: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.lg,
    width: '100%',
    marginBottom: SPACING.md,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  settingLabel: {
    ...TYPOGRAPHY.body,
    color: COLORS.text,
    fontWeight: '500',
  },
  durationControl: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: SPACING.md,
  },
  durationButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  breakButton: {
    backgroundColor: COLORS.secondary,
  },
  durationButtonText: {
    color: '#FFFFFF',
    fontSize: 24,
    fontWeight: '600',
  },
  durationValue: {
    ...TYPOGRAPHY.h3,
    color: COLORS.text,
    minWidth: 70,
    textAlign: 'center',
  },
  appList: {
    width: '100%',
    marginBottom: SPACING.xl,
  },
  appItem: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'transparent',
  },
  appItemSelected: {
    borderColor: COLORS.primary,
    backgroundColor: COLORS.primary + '10',
  },
  appName: {
    ...TYPOGRAPHY.body,
    color: COLORS.text,
  },
  checkmark: {
    color: COLORS.primary,
    fontSize: 18,
    fontWeight: '600',
  },
  trialBadge: {
    backgroundColor: COLORS.secondary + '20',
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.sm,
    borderRadius: 20,
    marginBottom: SPACING.xl,
  },
  trialText: {
    ...TYPOGRAPHY.bodySmall,
    color: COLORS.secondary,
    fontWeight: '600',
  },
  primaryButton: {
    backgroundColor: COLORS.primary,
    paddingVertical: SPACING.md,
    paddingHorizontal: SPACING.xl,
    borderRadius: 12,
    width: '100%',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  primaryButtonText: {
    ...TYPOGRAPHY.body,
    color: '#FFFFFF',
    fontWeight: '600',
  },
  secondaryButton: {
    paddingVertical: SPACING.md,
    paddingHorizontal: SPACING.xl,
    borderRadius: 12,
    width: '100%',
    alignItems: 'center',
  },
  secondaryButtonText: {
    ...TYPOGRAPHY.body,
    color: COLORS.primary,
  },
  buttonDisabled: {
    backgroundColor: COLORS.border,
  },
});
