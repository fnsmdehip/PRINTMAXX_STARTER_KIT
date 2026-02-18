import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  Alert,
} from 'react-native';
import { COLORS } from '../utils/constants';
import { Button } from '../components/Button';
import { GoalSelector } from '../components/GoalSelector';
import { AppSelector } from '../components/AppSelector';
import { useUserStore } from '../stores/userStore';
import { BlockedApp } from '../types';
import { requestHealthPermissions } from '../services/stepService';
import { requestBlockingPermissions } from '../services/blockerService';

interface Props {
  onComplete: () => void;
}

type Step = 'welcome' | 'health' | 'goal' | 'apps' | 'blocking' | 'complete';

export function OnboardingScreen({ onComplete }: Props) {
  const [currentStep, setCurrentStep] = useState<Step>('welcome');
  const [isLoading, setIsLoading] = useState(false);

  const {
    settings,
    setStepGoal,
    updateSettings,
    startTrial,
    completeOnboarding,
  } = useUserStore();

  const handleHealthPermission = async () => {
    setIsLoading(true);
    const result = await requestHealthPermissions();
    setIsLoading(false);

    if (result.granted) {
      setCurrentStep('goal');
    } else {
      Alert.alert(
        'Permission needed',
        'WalkToUnlock needs access to your step data to track your progress. Please enable this in Settings.',
        [
          { text: 'Skip for now', onPress: () => setCurrentStep('goal') },
          { text: 'Try again', onPress: handleHealthPermission },
        ]
      );
    }
  };

  const handleGoalSet = () => {
    setCurrentStep('apps');
  };

  const handleAppsSelected = (apps: BlockedApp[]) => {
    updateSettings({ blockedApps: apps });
  };

  const handleAppsConfirm = () => {
    setCurrentStep('blocking');
  };

  const handleBlockingPermission = async () => {
    setIsLoading(true);
    const result = await requestBlockingPermissions();
    setIsLoading(false);

    if (result.success) {
      setCurrentStep('complete');
    } else {
      Alert.alert(
        'Permission needed',
        'App blocking requires additional permissions. You can set this up later in Settings.',
        [
          { text: 'Skip for now', onPress: () => setCurrentStep('complete') },
          { text: 'Try again', onPress: handleBlockingPermission },
        ]
      );
    }
  };

  const handleComplete = () => {
    startTrial();
    completeOnboarding();
    onComplete();
  };

  const renderStep = () => {
    switch (currentStep) {
      case 'welcome':
        return (
          <View style={styles.stepContainer}>
            <Text style={styles.emoji}>🚶</Text>
            <Text style={styles.title}>WalkToUnlock</Text>
            <Text style={styles.subtitle}>
              Block distracting apps until you hit your daily step goal.
            </Text>
            <Text style={styles.description}>
              No steps, no scrolling. It's that simple.
            </Text>
            <View style={styles.features}>
              <Text style={styles.feature}>
                • Set your daily step target
              </Text>
              <Text style={styles.feature}>
                • Choose which apps to block
              </Text>
              <Text style={styles.feature}>
                • Apps unlock when you hit your goal
              </Text>
              <Text style={styles.feature}>
                • Track your streak and progress
              </Text>
            </View>
            <Button
              title="Get started"
              onPress={() => setCurrentStep('health')}
              size="large"
              style={styles.button}
            />
          </View>
        );

      case 'health':
        return (
          <View style={styles.stepContainer}>
            <Text style={styles.emoji}>❤️</Text>
            <Text style={styles.title}>Connect your steps</Text>
            <Text style={styles.description}>
              We need access to your step count to track your progress.
              Your data stays on your device.
            </Text>
            <Button
              title="Allow step access"
              onPress={handleHealthPermission}
              loading={isLoading}
              size="large"
              style={styles.button}
            />
          </View>
        );

      case 'goal':
        return (
          <View style={styles.stepContainer}>
            <Text style={styles.title}>Set your goal</Text>
            <Text style={styles.description}>
              Pick a daily step target. Start lower and increase it as you build the habit.
            </Text>
            <GoalSelector
              value={settings.stepGoal}
              onChange={setStepGoal}
            />
            <Button
              title="Continue"
              onPress={handleGoalSet}
              size="large"
              style={styles.button}
            />
          </View>
        );

      case 'apps':
        return (
          <View style={[styles.stepContainer, styles.appsContainer]}>
            <AppSelector
              selectedApps={settings.blockedApps}
              onSelectionChange={handleAppsSelected}
            />
            <Button
              title={`Block ${settings.blockedApps.length} app${settings.blockedApps.length !== 1 ? 's' : ''}`}
              onPress={handleAppsConfirm}
              size="large"
              style={styles.button}
              disabled={settings.blockedApps.length === 0}
            />
          </View>
        );

      case 'blocking':
        return (
          <View style={styles.stepContainer}>
            <Text style={styles.emoji}>🔒</Text>
            <Text style={styles.title}>Enable app blocking</Text>
            <Text style={styles.description}>
              For app blocking to work, we need permission to monitor app usage.
              This is required to lock and unlock your selected apps.
            </Text>
            <Button
              title="Enable blocking"
              onPress={handleBlockingPermission}
              loading={isLoading}
              size="large"
              style={styles.button}
            />
            <Button
              title="Skip for now"
              onPress={() => setCurrentStep('complete')}
              variant="text"
              style={styles.skipButton}
            />
          </View>
        );

      case 'complete':
        return (
          <View style={styles.stepContainer}>
            <Text style={styles.emoji}>🎉</Text>
            <Text style={styles.title}>You're all set!</Text>
            <Text style={styles.description}>
              Your {settings.stepGoal.toLocaleString()} step goal is locked in.
              {settings.blockedApps.length > 0
                ? ` ${settings.blockedApps.length} apps are blocked until you walk.`
                : ' Add apps to block in settings.'}
            </Text>
            <Text style={styles.trialNote}>
              You have 3 days to try all features free. Then $7.99/month.
            </Text>
            <Button
              title="Start walking"
              onPress={handleComplete}
              size="large"
              style={styles.button}
            />
          </View>
        );
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {renderStep()}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scrollContent: {
    flexGrow: 1,
    padding: 24,
  },
  stepContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  appsContainer: {
    justifyContent: 'flex-start',
    paddingTop: 20,
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
    marginBottom: 12,
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
    marginBottom: 24,
    paddingHorizontal: 16,
  },
  features: {
    alignSelf: 'stretch',
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 20,
    marginBottom: 32,
  },
  feature: {
    fontSize: 16,
    color: COLORS.text,
    lineHeight: 28,
  },
  button: {
    width: '100%',
    marginTop: 16,
  },
  skipButton: {
    marginTop: 12,
  },
  trialNote: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 16,
  },
});
