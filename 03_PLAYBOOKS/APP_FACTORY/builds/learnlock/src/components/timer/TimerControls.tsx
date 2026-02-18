import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { COLORS, TYPOGRAPHY, SPACING } from '../../utils/constants';
import { TimerState } from '../../types';

interface Props {
  timerState: TimerState;
  currentSessionType: 'work' | 'break';
  onStart: () => void;
  onPause: () => void;
  onResume: () => void;
  onEnd: () => void;
  onStartBreak: () => void;
  onSkipBreak: () => void;
}

export function TimerControls({
  timerState,
  currentSessionType,
  onStart,
  onPause,
  onResume,
  onEnd,
  onStartBreak,
  onSkipBreak,
}: Props) {
  const renderIdleControls = () => (
    <TouchableOpacity style={styles.primaryButton} onPress={onStart} activeOpacity={0.8}>
      <Text style={styles.primaryButtonText}>Start Session</Text>
    </TouchableOpacity>
  );

  const renderStudyingControls = () => (
    <View style={styles.buttonRow}>
      <TouchableOpacity
        style={styles.secondaryButton}
        onPress={onPause}
        activeOpacity={0.8}
      >
        <Text style={styles.secondaryButtonText}>Pause</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={styles.dangerButton}
        onPress={onEnd}
        activeOpacity={0.8}
      >
        <Text style={styles.dangerButtonText}>End Early</Text>
      </TouchableOpacity>
    </View>
  );

  const renderPausedControls = () => (
    <View style={styles.buttonRow}>
      <TouchableOpacity
        style={styles.primaryButton}
        onPress={onResume}
        activeOpacity={0.8}
      >
        <Text style={styles.primaryButtonText}>Resume</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={styles.dangerButton}
        onPress={onEnd}
        activeOpacity={0.8}
      >
        <Text style={styles.dangerButtonText}>Give Up</Text>
      </TouchableOpacity>
    </View>
  );

  const renderBreakControls = () => (
    <View style={styles.buttonRow}>
      <TouchableOpacity
        style={styles.breakButton}
        onPress={onSkipBreak}
        activeOpacity={0.8}
      >
        <Text style={styles.breakButtonText}>Skip Break</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={styles.primaryButton}
        onPress={onStart}
        activeOpacity={0.8}
      >
        <Text style={styles.primaryButtonText}>Start Next</Text>
      </TouchableOpacity>
    </View>
  );

  // After session completes, show break prompt
  const renderCompletedControls = () => (
    <View style={styles.completedContainer}>
      <Text style={styles.completedText}>Session complete!</Text>
      <View style={styles.buttonRow}>
        <TouchableOpacity
          style={styles.breakButton}
          onPress={onStartBreak}
          activeOpacity={0.8}
        >
          <Text style={styles.breakButtonText}>Take Break</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.primaryButton}
          onPress={onStart}
          activeOpacity={0.8}
        >
          <Text style={styles.primaryButtonText}>Continue</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  switch (timerState) {
    case 'idle':
      return renderIdleControls();
    case 'studying':
      return renderStudyingControls();
    case 'paused':
      return renderPausedControls();
    case 'break':
      return renderBreakControls();
    default:
      return renderIdleControls();
  }
}

const styles = StyleSheet.create({
  buttonRow: {
    flexDirection: 'row',
    gap: SPACING.md,
    width: '100%',
    paddingHorizontal: SPACING.lg,
  },
  primaryButton: {
    flex: 1,
    backgroundColor: COLORS.primary,
    paddingVertical: SPACING.md,
    paddingHorizontal: SPACING.lg,
    borderRadius: 12,
    alignItems: 'center',
  },
  primaryButtonText: {
    ...TYPOGRAPHY.body,
    color: COLORS.surface,
    fontWeight: '600',
  },
  secondaryButton: {
    flex: 1,
    backgroundColor: COLORS.surfaceSecondary,
    paddingVertical: SPACING.md,
    paddingHorizontal: SPACING.lg,
    borderRadius: 12,
    alignItems: 'center',
  },
  secondaryButtonText: {
    ...TYPOGRAPHY.body,
    color: COLORS.text,
    fontWeight: '600',
  },
  dangerButton: {
    flex: 1,
    backgroundColor: COLORS.surface,
    paddingVertical: SPACING.md,
    paddingHorizontal: SPACING.lg,
    borderRadius: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.error,
  },
  dangerButtonText: {
    ...TYPOGRAPHY.body,
    color: COLORS.error,
    fontWeight: '600',
  },
  breakButton: {
    flex: 1,
    backgroundColor: COLORS.secondaryLight,
    paddingVertical: SPACING.md,
    paddingHorizontal: SPACING.lg,
    borderRadius: 12,
    alignItems: 'center',
  },
  breakButtonText: {
    ...TYPOGRAPHY.body,
    color: COLORS.surface,
    fontWeight: '600',
  },
  completedContainer: {
    alignItems: 'center',
    width: '100%',
  },
  completedText: {
    ...TYPOGRAPHY.h3,
    color: COLORS.secondary,
    marginBottom: SPACING.lg,
  },
});
