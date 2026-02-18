/**
 * Timer Screen
 * Prayer timer with countdown and completion handling
 */

import React, { useEffect, useRef, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Vibration,
  AppState,
  AppStateStatus,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { useUserStore } from '../stores/userStore';
import { useDevotionStore } from '../stores/devotionStore';
import { COLORS } from '../utils/constants';
import { formatTimerDisplay } from '../utils/dateUtils';
import { RootStackParamList } from '../types';

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

export default function TimerScreen() {
  const navigation = useNavigation<NavigationProp>();
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const startTimeRef = useRef<number>(Date.now());
  const appStateRef = useRef<AppStateStatus>(AppState.currentState);

  const { settings } = useUserStore();
  const {
    timerSecondsRemaining,
    updateTimer,
    completeTimer,
    completeSession,
  } = useDevotionStore();

  const [isComplete, setIsComplete] = useState(false);
  const [isPaused, setIsPaused] = useState(false);

  useEffect(() => {
    // Handle app state changes (background/foreground)
    const subscription = AppState.addEventListener('change', handleAppStateChange);

    startTimer();

    return () => {
      subscription.remove();
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  function handleAppStateChange(nextAppState: AppStateStatus) {
    if (
      appStateRef.current.match(/inactive|background/) &&
      nextAppState === 'active'
    ) {
      // App came to foreground, recalculate remaining time
      const elapsed = Math.floor((Date.now() - startTimeRef.current) / 1000);
      const totalDuration = settings.devotionDurationMinutes * 60;
      const remaining = Math.max(0, totalDuration - elapsed);
      updateTimer(remaining);

      if (remaining === 0) {
        handleTimerComplete();
      }
    }
    appStateRef.current = nextAppState;
  }

  function startTimer() {
    startTimeRef.current = Date.now();

    timerRef.current = setInterval(() => {
      const elapsed = Math.floor((Date.now() - startTimeRef.current) / 1000);
      const totalDuration = settings.devotionDurationMinutes * 60;
      const remaining = Math.max(0, totalDuration - elapsed);

      updateTimer(remaining);

      if (remaining === 0) {
        handleTimerComplete();
      }
    }, 1000);
  }

  function handleTimerComplete() {
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }

    // Vibrate to notify completion
    Vibration.vibrate([0, 500, 200, 500]);

    setIsComplete(true);
    completeTimer();
  }

  async function handleContinue() {
    if (settings.requireScripture) {
      // Scripture also required, navigate there
      navigation.navigate('Scripture');
    } else {
      // Only timer required, complete the session
      await completeSession();
      navigation.navigate('Main');
    }
  }

  // Calculate progress percentage for circle
  const totalSeconds = settings.devotionDurationMinutes * 60;
  const progress = 1 - timerSecondsRemaining / totalSeconds;
  const progressDegrees = progress * 360;

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Prayer Time</Text>
        <Text style={styles.headerSubtitle}>
          {isComplete
            ? 'Well done'
            : 'Spend this time in prayer and reflection'}
        </Text>
      </View>

      {/* Timer Circle */}
      <View style={styles.timerContainer}>
        <View style={styles.timerCircle}>
          <View
            style={[
              styles.timerProgress,
              {
                transform: [{ rotate: `${progressDegrees}deg` }],
              },
            ]}
          />
          <View style={styles.timerInner}>
            <Text style={styles.timerText}>
              {formatTimerDisplay(timerSecondsRemaining)}
            </Text>
            <Text style={styles.timerLabel}>
              {isComplete ? 'Complete' : 'remaining'}
            </Text>
          </View>
        </View>
      </View>

      {/* Prayer Prompts */}
      {!isComplete && (
        <View style={styles.promptsContainer}>
          <Text style={styles.promptTitle}>Prayer prompts</Text>
          <View style={styles.prompt}>
            <Text style={styles.promptText}>
              Praise God for who He is
            </Text>
          </View>
          <View style={styles.prompt}>
            <Text style={styles.promptText}>
              Confess and ask for forgiveness
            </Text>
          </View>
          <View style={styles.prompt}>
            <Text style={styles.promptText}>
              Thank Him for His blessings
            </Text>
          </View>
          <View style={styles.prompt}>
            <Text style={styles.promptText}>
              Bring your requests to Him
            </Text>
          </View>
        </View>
      )}

      {/* Completion Section */}
      {isComplete && (
        <View style={styles.completeSection}>
          <Text style={styles.completeText}>
            Prayer time complete
          </Text>

          <TouchableOpacity
            style={styles.continueButton}
            onPress={handleContinue}
            activeOpacity={0.8}
          >
            <Text style={styles.continueButtonText}>
              {settings.requireScripture ? 'Continue to Scripture' : 'Finish'}
            </Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Emergency Unlock */}
      {!isComplete && settings.emergencyUnlockEnabled && (
        <TouchableOpacity
          style={styles.emergencyLink}
          onPress={() => navigation.navigate('EmergencyUnlock')}
        >
          <Text style={styles.emergencyText}>Emergency? Unlock here</Text>
        </TouchableOpacity>
      )}

      {/* Info Text */}
      <Text style={styles.infoText}>
        Leaving this screen will pause your timer
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
    padding: 20,
  },
  header: {
    alignItems: 'center',
    marginTop: 20,
    marginBottom: 40,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 8,
  },
  headerSubtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  timerContainer: {
    alignItems: 'center',
    marginBottom: 40,
  },
  timerCircle: {
    width: 240,
    height: 240,
    borderRadius: 120,
    backgroundColor: COLORS.surface,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 8,
    borderColor: COLORS.primary + '30',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 5,
  },
  timerProgress: {
    position: 'absolute',
    width: 240,
    height: 240,
    borderRadius: 120,
    borderWidth: 8,
    borderColor: 'transparent',
    borderTopColor: COLORS.primary,
  },
  timerInner: {
    alignItems: 'center',
  },
  timerText: {
    fontSize: 56,
    fontWeight: '800',
    color: COLORS.text,
    fontVariant: ['tabular-nums'],
  },
  timerLabel: {
    fontSize: 16,
    color: COLORS.textSecondary,
    marginTop: -4,
  },
  promptsContainer: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 20,
    marginBottom: 20,
  },
  promptTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 16,
  },
  prompt: {
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.background,
  },
  promptText: {
    fontSize: 15,
    color: COLORS.textSecondary,
  },
  completeSection: {
    alignItems: 'center',
    marginTop: 20,
  },
  completeText: {
    fontSize: 20,
    fontWeight: '600',
    color: COLORS.success,
    marginBottom: 24,
  },
  continueButton: {
    backgroundColor: COLORS.primary,
    borderRadius: 12,
    paddingVertical: 18,
    paddingHorizontal: 40,
  },
  continueButtonText: {
    color: COLORS.surface,
    fontSize: 18,
    fontWeight: '700',
  },
  emergencyLink: {
    alignItems: 'center',
    paddingVertical: 16,
  },
  emergencyText: {
    color: COLORS.textSecondary,
    fontSize: 14,
    textDecorationLine: 'underline',
  },
  infoText: {
    textAlign: 'center',
    color: COLORS.disabled,
    fontSize: 13,
    marginTop: 'auto',
    marginBottom: 20,
  },
});
