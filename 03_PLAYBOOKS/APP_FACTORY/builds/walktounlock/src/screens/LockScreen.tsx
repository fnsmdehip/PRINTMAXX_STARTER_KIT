import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  StyleSheet,
  Text,
  SafeAreaView,
  StatusBar,
} from 'react-native';
import * as Haptics from 'expo-haptics';
import { COLORS, SPACING } from '../constants/theme';
import { ProgressRing, Button } from '../components';
import {
  subscribeToStepCount,
  getTodayStepCount,
  getMotivationalMessage,
  isPedometerAvailable,
  getPermissionStatus,
} from '../utils/pedometer';
import { unlockAchievement } from '../utils/storage';
import { useApp } from '../context/AppContext';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { RootStackParamList } from '../constants/types';

interface LockScreenProps {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Lock'>;
}

export const LockScreen: React.FC<LockScreenProps> = ({ navigation }) => {
  const { settings, completeUnlock } = useApp();
  const [currentSteps, setCurrentSteps] = useState(0);
  const [isAvailable, setIsAvailable] = useState(true);
  const [hasPermission, setHasPermission] = useState(true);
  const [unlocked, setUnlocked] = useState(false);

  const goalSteps = settings.stepGoal;
  const progress = goalSteps > 0 ? currentSteps / goalSteps : 0;
  const motivationalMessage = getMotivationalMessage(progress);

  const handleUnlock = useCallback(async () => {
    await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    setUnlocked(true);

    await completeUnlock(currentSteps);

    await unlockAchievement('first_steps');
    if (currentSteps >= 500) await unlockAchievement('step_500');
    if (currentSteps >= 1000) await unlockAchievement('step_1000');
    if (currentSteps >= 2500) await unlockAchievement('step_2500');
    if (currentSteps >= 5000) await unlockAchievement('step_5000');
    if (currentSteps >= 10000) await unlockAchievement('step_10000');

    setTimeout(() => {
      navigation.replace('Main');
    }, 1500);
  }, [currentSteps, navigation, completeUnlock]);

  useEffect(() => {
    const initPedometer = async () => {
      const available = await isPedometerAvailable();
      setIsAvailable(available);

      if (!available) return;

      const permission = await getPermissionStatus();
      setHasPermission(permission);

      if (!permission) return;

      // Start fresh counter for this lock session
      setCurrentSteps(0);
    };

    initPedometer();
  }, []);

  useEffect(() => {
    if (!isAvailable || !hasPermission) return;

    const subscription = subscribeToStepCount((result) => {
      const newSteps = result.steps;
      setCurrentSteps(newSteps);

      if (newSteps > 0 && newSteps % 50 === 0) {
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
      }
    });

    return () => {
      subscription.remove();
    };
  }, [isAvailable, hasPermission]);

  useEffect(() => {
    if (currentSteps >= goalSteps && !unlocked) {
      handleUnlock();
    }
  }, [currentSteps, goalSteps, unlocked, handleUnlock]);

  if (!isAvailable) {
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar barStyle="light-content" />
        <View style={styles.errorContainer}>
          <Text style={styles.errorIcon}>{'\u26A0'}</Text>
          <Text style={styles.errorTitle}>Pedometer Unavailable</Text>
          <Text style={styles.errorText}>
            Your device does not support step counting.
          </Text>
          <Button
            title="Continue Anyway"
            onPress={() => navigation.replace('Main')}
            style={{ marginTop: SPACING.lg }}
          />
        </View>
      </SafeAreaView>
    );
  }

  if (!hasPermission) {
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar barStyle="light-content" />
        <View style={styles.errorContainer}>
          <Text style={styles.errorIcon}>{'\u{1F512}'}</Text>
          <Text style={styles.errorTitle}>Permission Required</Text>
          <Text style={styles.errorText}>
            WalkToUnlock needs access to your motion data to count steps.
          </Text>
          <Button
            title="Grant Permission"
            onPress={async () => {
              const granted = await getPermissionStatus();
              setHasPermission(granted);
            }}
            style={{ marginTop: SPACING.lg }}
          />
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />

      <View style={styles.header}>
        <Text style={styles.appName}>WalkToUnlock</Text>
        <Text style={styles.subtitle}>Walk to unlock your phone</Text>
      </View>

      <View style={styles.progressContainer}>
        <ProgressRing
          progress={progress}
          currentSteps={currentSteps}
          goalSteps={goalSteps}
          size={280}
        />
      </View>

      <View style={styles.messageContainer}>
        <Text style={styles.motivationalMessage}>{motivationalMessage}</Text>
        {unlocked && (
          <View style={styles.unlockedBadge}>
            <Text style={styles.unlockedText}>UNLOCKED!</Text>
          </View>
        )}
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerText}>
          {unlocked ? 'Great job! Opening...' : 'Start walking to unlock'}
        </Text>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    paddingTop: SPACING.xl,
    paddingHorizontal: SPACING.lg,
    alignItems: 'center',
  },
  appName: {
    fontSize: 28,
    fontWeight: '800',
    color: COLORS.primary,
    letterSpacing: -1,
  },
  subtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    marginTop: SPACING.xs,
  },
  progressContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  messageContainer: {
    alignItems: 'center',
    paddingHorizontal: SPACING.lg,
    marginBottom: SPACING.xl,
  },
  motivationalMessage: {
    fontSize: 20,
    fontWeight: '600',
    color: COLORS.text,
    textAlign: 'center',
  },
  unlockedBadge: {
    backgroundColor: COLORS.primary,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.sm,
    borderRadius: 20,
    marginTop: SPACING.md,
  },
  unlockedText: {
    fontSize: 16,
    fontWeight: '800',
    color: COLORS.background,
    letterSpacing: 2,
  },
  footer: {
    paddingBottom: SPACING.xxl,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 14,
    color: COLORS.textMuted,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: SPACING.xl,
  },
  errorIcon: {
    fontSize: 64,
    marginBottom: SPACING.lg,
  },
  errorTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: SPACING.sm,
    textAlign: 'center',
  },
  errorText: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 24,
  },
});
