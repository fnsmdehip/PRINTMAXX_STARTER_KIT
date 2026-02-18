/**
 * Onboarding Screen
 * First-time user setup flow
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Dimensions,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useUserStore } from '@/stores/userStore';
import { requestBlockingPermission } from '@/services/blockerService';
import {
  COLORS,
  COMMON_SOCIAL_APPS,
  DEFAULT_DEVOTION_MINUTES,
} from '@/utils/constants';
import { AppInfo } from '@/types';

const { width } = Dimensions.get('window');

type OnboardingStep = 'welcome' | 'apps' | 'duration' | 'permissions' | 'complete';

export default function OnboardingScreen() {
  const router = useRouter();
  const { updateSettings, updateBlockedApps, setOnboardingComplete, startTrial } =
    useUserStore();

  const [step, setStep] = useState<OnboardingStep>('welcome');
  const [selectedApps, setSelectedApps] = useState<string[]>([]);
  const [duration, setDuration] = useState(DEFAULT_DEVOTION_MINUTES);

  const availableApps: AppInfo[] = COMMON_SOCIAL_APPS.map((app) => ({
    ...app,
    isBlocked: false,
  }));

  function toggleApp(packageName: string) {
    setSelectedApps((prev) =>
      prev.includes(packageName)
        ? prev.filter((p) => p !== packageName)
        : [...prev, packageName]
    );
  }

  function selectAllApps() {
    setSelectedApps(availableApps.map((app) => app.packageName));
  }

  async function handlePermissions() {
    const granted = await requestBlockingPermission();
    if (granted) {
      setStep('complete');
    }
  }

  async function handleComplete() {
    await updateBlockedApps(selectedApps);
    await updateSettings({ devotionDurationMinutes: duration });
    await setOnboardingComplete();
    await startTrial();
    router.replace('/(tabs)');
  }

  function renderWelcome() {
    return (
      <View style={styles.stepContainer}>
        <View style={styles.iconContainer}>
          <Text style={styles.icon}>&#128591;</Text>
        </View>
        <Text style={styles.title}>Welcome to FocusPrayer</Text>
        <Text style={styles.description}>
          Start your day with prayer and scripture before distractions take over.
        </Text>
        <View style={styles.features}>
          <View style={styles.feature}>
            <Text style={styles.featureIcon}>&#128274;</Text>
            <Text style={styles.featureText}>Block distracting apps</Text>
          </View>
          <View style={styles.feature}>
            <Text style={styles.featureIcon}>&#9201;</Text>
            <Text style={styles.featureText}>Prayer timer</Text>
          </View>
          <View style={styles.feature}>
            <Text style={styles.featureIcon}>&#128214;</Text>
            <Text style={styles.featureText}>Daily scripture</Text>
          </View>
          <View style={styles.feature}>
            <Text style={styles.featureIcon}>&#128293;</Text>
            <Text style={styles.featureText}>Streak tracking</Text>
          </View>
        </View>
        <TouchableOpacity
          style={styles.primaryButton}
          onPress={() => setStep('apps')}
        >
          <Text style={styles.primaryButtonText}>Get Started</Text>
        </TouchableOpacity>
      </View>
    );
  }

  function renderApps() {
    return (
      <View style={styles.stepContainer}>
        <Text style={styles.stepTitle}>Select Apps to Block</Text>
        <Text style={styles.stepDescription}>
          These apps will be locked until you complete your morning devotion.
        </Text>

        <TouchableOpacity style={styles.selectAllButton} onPress={selectAllApps}>
          <Text style={styles.selectAllText}>Select All</Text>
        </TouchableOpacity>

        <ScrollView style={styles.appList} showsVerticalScrollIndicator={false}>
          {availableApps.map((app) => (
            <TouchableOpacity
              key={app.packageName}
              style={[
                styles.appItem,
                selectedApps.includes(app.packageName) && styles.appItemSelected,
              ]}
              onPress={() => toggleApp(app.packageName)}
            >
              <Text style={styles.appName}>{app.appName}</Text>
              <View
                style={[
                  styles.checkbox,
                  selectedApps.includes(app.packageName) && styles.checkboxChecked,
                ]}
              >
                {selectedApps.includes(app.packageName) && (
                  <Text style={styles.checkmark}>&#10003;</Text>
                )}
              </View>
            </TouchableOpacity>
          ))}
        </ScrollView>

        <View style={styles.buttonRow}>
          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={() => setStep('welcome')}
          >
            <Text style={styles.secondaryButtonText}>Back</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[
              styles.primaryButton,
              styles.flexButton,
              selectedApps.length === 0 && styles.buttonDisabled,
            ]}
            onPress={() => setStep('duration')}
            disabled={selectedApps.length === 0}
          >
            <Text style={styles.primaryButtonText}>Continue</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  function renderDuration() {
    const durations = [5, 10, 15, 20, 30];

    return (
      <View style={styles.stepContainer}>
        <Text style={styles.stepTitle}>Prayer Duration</Text>
        <Text style={styles.stepDescription}>
          How long would you like to spend in prayer each morning?
        </Text>

        <View style={styles.durationOptions}>
          {durations.map((mins) => (
            <TouchableOpacity
              key={mins}
              style={[
                styles.durationOption,
                duration === mins && styles.durationOptionSelected,
              ]}
              onPress={() => setDuration(mins)}
            >
              <Text
                style={[
                  styles.durationText,
                  duration === mins && styles.durationTextSelected,
                ]}
              >
                {mins}
              </Text>
              <Text
                style={[
                  styles.durationLabel,
                  duration === mins && styles.durationLabelSelected,
                ]}
              >
                min
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        <Text style={styles.recommendation}>
          We recommend starting with 10 minutes. You can adjust this later.
        </Text>

        <View style={styles.buttonRow}>
          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={() => setStep('apps')}
          >
            <Text style={styles.secondaryButtonText}>Back</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.primaryButton, styles.flexButton]}
            onPress={() => setStep('permissions')}
          >
            <Text style={styles.primaryButtonText}>Continue</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  function renderPermissions() {
    return (
      <View style={styles.stepContainer}>
        <View style={styles.iconContainer}>
          <Text style={styles.icon}>&#128272;</Text>
        </View>
        <Text style={styles.stepTitle}>Enable App Blocking</Text>
        <Text style={styles.stepDescription}>
          FocusPrayer needs permission to block apps on your device. We only use
          this permission to help you stay focused during your devotion time.
        </Text>

        <View style={styles.permissionInfo}>
          <Text style={styles.permissionTitle}>What we access:</Text>
          <Text style={styles.permissionItem}>
            &#8226; Screen Time API (iOS) or Usage Stats (Android)
          </Text>
          <Text style={styles.permissionItem}>
            &#8226; Only to detect and block selected apps
          </Text>
          <Text style={styles.permissionItem}>
            &#8226; Your data never leaves your device
          </Text>
        </View>

        <View style={styles.buttonRow}>
          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={() => setStep('duration')}
          >
            <Text style={styles.secondaryButtonText}>Back</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.primaryButton, styles.flexButton]}
            onPress={handlePermissions}
          >
            <Text style={styles.primaryButtonText}>Grant Permission</Text>
          </TouchableOpacity>
        </View>

        <TouchableOpacity
          style={styles.skipButton}
          onPress={() => setStep('complete')}
        >
          <Text style={styles.skipText}>Skip for now</Text>
        </TouchableOpacity>
      </View>
    );
  }

  function renderComplete() {
    return (
      <View style={styles.stepContainer}>
        <View style={styles.iconContainer}>
          <Text style={styles.icon}>&#10003;</Text>
        </View>
        <Text style={styles.stepTitle}>You're All Set</Text>
        <Text style={styles.stepDescription}>
          Your 3-day free trial starts now. {selectedApps.length} apps will be
          blocked each morning until you complete your {duration}-minute devotion.
        </Text>

        <View style={styles.summaryCard}>
          <View style={styles.summaryRow}>
            <Text style={styles.summaryLabel}>Prayer time</Text>
            <Text style={styles.summaryValue}>{duration} minutes</Text>
          </View>
          <View style={styles.summaryRow}>
            <Text style={styles.summaryLabel}>Apps blocked</Text>
            <Text style={styles.summaryValue}>{selectedApps.length}</Text>
          </View>
          <View style={styles.summaryRow}>
            <Text style={styles.summaryLabel}>Scripture</Text>
            <Text style={styles.summaryValue}>Daily passage</Text>
          </View>
        </View>

        <TouchableOpacity style={styles.primaryButton} onPress={handleComplete}>
          <Text style={styles.primaryButtonText}>Start My Journey</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {step === 'welcome' && renderWelcome()}
      {step === 'apps' && renderApps()}
      {step === 'duration' && renderDuration()}
      {step === 'permissions' && renderPermissions()}
      {step === 'complete' && renderComplete()}

      {/* Progress dots */}
      <View style={styles.progress}>
        {['welcome', 'apps', 'duration', 'permissions', 'complete'].map(
          (s, i) => (
            <View
              key={s}
              style={[
                styles.dot,
                ['welcome', 'apps', 'duration', 'permissions', 'complete'].indexOf(
                  step
                ) >= i && styles.dotActive,
              ]}
            />
          )
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  stepContainer: {
    flex: 1,
    padding: 24,
    paddingTop: 60,
  },
  iconContainer: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: COLORS.primary + '20',
    justifyContent: 'center',
    alignItems: 'center',
    alignSelf: 'center',
    marginBottom: 24,
  },
  icon: {
    fontSize: 50,
  },
  title: {
    fontSize: 32,
    fontWeight: '800',
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: 16,
  },
  stepTitle: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 12,
  },
  description: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 32,
  },
  stepDescription: {
    fontSize: 16,
    color: COLORS.textSecondary,
    lineHeight: 24,
    marginBottom: 24,
  },
  features: {
    marginBottom: 40,
  },
  feature: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 20,
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    marginBottom: 12,
  },
  featureIcon: {
    fontSize: 24,
    marginRight: 16,
  },
  featureText: {
    fontSize: 16,
    color: COLORS.text,
  },
  selectAllButton: {
    alignSelf: 'flex-end',
    marginBottom: 12,
  },
  selectAllText: {
    color: COLORS.primary,
    fontWeight: '600',
  },
  appList: {
    flex: 1,
    marginBottom: 20,
  },
  appItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    marginBottom: 8,
  },
  appItemSelected: {
    borderWidth: 2,
    borderColor: COLORS.primary,
  },
  appName: {
    fontSize: 16,
    color: COLORS.text,
  },
  checkbox: {
    width: 24,
    height: 24,
    borderRadius: 6,
    borderWidth: 2,
    borderColor: COLORS.disabled,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkboxChecked: {
    backgroundColor: COLORS.primary,
    borderColor: COLORS.primary,
  },
  checkmark: {
    color: COLORS.surface,
    fontSize: 14,
    fontWeight: '600',
  },
  durationOptions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  durationOption: {
    width: (width - 80) / 5,
    aspectRatio: 1,
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'transparent',
  },
  durationOptionSelected: {
    borderColor: COLORS.primary,
    backgroundColor: COLORS.primary + '10',
  },
  durationText: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.text,
  },
  durationTextSelected: {
    color: COLORS.primary,
  },
  durationLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
  durationLabelSelected: {
    color: COLORS.primary,
  },
  recommendation: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 40,
  },
  permissionInfo: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 20,
    marginBottom: 32,
  },
  permissionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 12,
  },
  permissionItem: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 8,
  },
  summaryCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 20,
    marginBottom: 32,
  },
  summaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.background,
  },
  summaryLabel: {
    fontSize: 15,
    color: COLORS.textSecondary,
  },
  summaryValue: {
    fontSize: 15,
    fontWeight: '600',
    color: COLORS.text,
  },
  buttonRow: {
    flexDirection: 'row',
    gap: 12,
    marginTop: 'auto',
  },
  primaryButton: {
    backgroundColor: COLORS.primary,
    borderRadius: 12,
    paddingVertical: 18,
    paddingHorizontal: 32,
    alignItems: 'center',
  },
  primaryButtonText: {
    color: COLORS.surface,
    fontSize: 18,
    fontWeight: '700',
  },
  secondaryButton: {
    borderWidth: 2,
    borderColor: COLORS.primary,
    borderRadius: 12,
    paddingVertical: 16,
    paddingHorizontal: 24,
  },
  secondaryButtonText: {
    color: COLORS.primary,
    fontSize: 16,
    fontWeight: '600',
  },
  flexButton: {
    flex: 1,
  },
  buttonDisabled: {
    backgroundColor: COLORS.disabled,
  },
  skipButton: {
    alignItems: 'center',
    paddingVertical: 16,
  },
  skipText: {
    color: COLORS.textSecondary,
    fontSize: 15,
  },
  progress: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 8,
    paddingBottom: 40,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: COLORS.disabled,
  },
  dotActive: {
    backgroundColor: COLORS.primary,
  },
});
