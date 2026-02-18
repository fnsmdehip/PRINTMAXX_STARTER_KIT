import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  TouchableOpacity,
} from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../utils/constants';
import { useStudyStore } from '../stores/studyStore';
import { useTimer } from '../hooks/useTimer';
import { formatTime } from '../utils/timer';
import Button from '../components/Button';

export default function LockScreen() {
  const router = useRouter();
  const { timeRemaining, isRunning, isBreak } = useTimer();
  const { currentSession } = useStudyStore();

  const handleUnlockAttempt = () => {
    // In a real app, this would check if the session is complete
    // For now, just redirect to timer
    router.replace('/timer');
  };

  const handleEmergencyUnlock = () => {
    // Navigate to emergency unlock (with penalty)
    router.push('/emergency-unlock');
  };

  if (!currentSession) {
    // No active session, redirect home
    router.replace('/');
    return null;
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        {/* Lock Icon */}
        <View style={styles.lockIconContainer}>
          <Ionicons name="lock-closed" size={80} color={COLORS.primary} />
        </View>

        {/* Title */}
        <Text style={styles.title}>Phone Locked</Text>
        <Text style={styles.subtitle}>
          Complete your study session to unlock
        </Text>

        {/* Timer Display */}
        <View style={styles.timerBox}>
          <Text style={styles.timerLabel}>
            {isBreak ? 'Break Time Remaining' : 'Study Time Remaining'}
          </Text>
          <Text style={[styles.timer, isBreak && styles.timerBreak]}>
            {formatTime(timeRemaining)}
          </Text>
        </View>

        {/* Return to Session */}
        <Button
          title="Return to Session"
          onPress={handleUnlockAttempt}
          size="large"
          fullWidth
          style={styles.returnButton}
        />

        {/* Emergency Unlock */}
        <TouchableOpacity
          style={styles.emergencyButton}
          onPress={handleEmergencyUnlock}
        >
          <Ionicons name="warning-outline" size={20} color={COLORS.error} />
          <Text style={styles.emergencyText}>Emergency Unlock</Text>
        </TouchableOpacity>

        {/* Info Text */}
        <Text style={styles.infoText}>
          Need to access your phone urgently? Emergency unlock will end your
          session without saving progress.
        </Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 32,
  },
  lockIconContainer: {
    width: 160,
    height: 160,
    borderRadius: 80,
    backgroundColor: COLORS.primary + '15',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 32,
  },
  title: {
    fontSize: 32,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 40,
  },
  timerBox: {
    alignItems: 'center',
    padding: 24,
    backgroundColor: COLORS.surface,
    borderRadius: 20,
    marginBottom: 40,
    width: '100%',
  },
  timerLabel: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 8,
  },
  timer: {
    fontSize: 48,
    fontWeight: '700',
    color: COLORS.primary,
    letterSpacing: 2,
  },
  timerBreak: {
    color: COLORS.secondary,
  },
  returnButton: {
    marginBottom: 20,
  },
  emergencyButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingVertical: 12,
    paddingHorizontal: 20,
  },
  emergencyText: {
    fontSize: 14,
    color: COLORS.error,
    fontWeight: '500',
  },
  infoText: {
    fontSize: 12,
    color: COLORS.textMuted,
    textAlign: 'center',
    marginTop: 20,
    paddingHorizontal: 20,
    lineHeight: 18,
  },
});
