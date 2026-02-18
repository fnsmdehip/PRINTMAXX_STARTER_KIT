import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { COLORS, MEWING_INSTRUCTIONS } from '../utils/constants';
import { formatDuration } from '../utils/dateUtils';

interface MewingTimerProps {
  isActive: boolean;
  onStart: () => void;
  onStop: () => void;
  todayMinutes: number;
  goalMinutes: number;
}

export function MewingTimer({
  isActive,
  onStart,
  onStop,
  todayMinutes,
  goalMinutes,
}: MewingTimerProps) {
  const [seconds, setSeconds] = useState(0);
  const [currentTip, setCurrentTip] = useState(0);

  // Timer logic
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isActive) {
      interval = setInterval(() => {
        setSeconds((s) => s + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isActive]);

  // Rotate tips every 30 seconds
  useEffect(() => {
    if (isActive && seconds > 0 && seconds % 30 === 0) {
      setCurrentTip((tip) => (tip + 1) % MEWING_INSTRUCTIONS.length);
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }
  }, [seconds, isActive]);

  const handleToggle = useCallback(() => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    if (isActive) {
      onStop();
      setSeconds(0);
    } else {
      onStart();
    }
  }, [isActive, onStart, onStop]);

  const progress = Math.min(todayMinutes / goalMinutes, 1);
  const progressPercent = Math.round(progress * 100);

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Mewing Timer</Text>
        <View style={styles.goalBadge}>
          <Text style={styles.goalText}>
            {todayMinutes} / {goalMinutes} min
          </Text>
        </View>
      </View>

      {/* Timer circle */}
      <View style={styles.timerContainer}>
        <View
          style={[
            styles.timerCircle,
            isActive && styles.timerCircleActive,
          ]}
        >
          <Text style={styles.timerText}>
            {formatDuration(seconds)}
          </Text>
          <Text style={styles.sessionLabel}>
            {isActive ? 'Session active' : 'Tap to start'}
          </Text>
        </View>
      </View>

      {/* Current tip */}
      {isActive && (
        <View style={styles.tipContainer}>
          <Ionicons name="bulb-outline" size={16} color={COLORS.warning} />
          <Text style={styles.tipText}>{MEWING_INSTRUCTIONS[currentTip]}</Text>
        </View>
      )}

      {/* Progress bar */}
      <View style={styles.progressContainer}>
        <View style={styles.progressBackground}>
          <View
            style={[
              styles.progressFill,
              { width: `${progressPercent}%` },
            ]}
          />
        </View>
        <Text style={styles.progressText}>{progressPercent}%</Text>
      </View>

      {/* Start/Stop button */}
      <TouchableOpacity
        style={[
          styles.button,
          isActive ? styles.buttonStop : styles.buttonStart,
        ]}
        onPress={handleToggle}
      >
        <Ionicons
          name={isActive ? 'stop' : 'play'}
          size={24}
          color={COLORS.surface}
        />
        <Text style={styles.buttonText}>
          {isActive ? 'End Session' : 'Start Mewing'}
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
  },
  goalBadge: {
    backgroundColor: COLORS.primaryLight,
    paddingVertical: 4,
    paddingHorizontal: 12,
    borderRadius: 12,
  },
  goalText: {
    fontSize: 13,
    fontWeight: '600',
    color: COLORS.primary,
  },
  timerContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  timerCircle: {
    width: 160,
    height: 160,
    borderRadius: 80,
    backgroundColor: COLORS.background,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 4,
    borderColor: COLORS.border,
  },
  timerCircleActive: {
    borderColor: COLORS.primary,
    backgroundColor: '#FFF0F5',
  },
  timerText: {
    fontSize: 36,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  sessionLabel: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  tipContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFF8E1',
    padding: 12,
    borderRadius: 12,
    marginBottom: 20,
    gap: 8,
  },
  tipText: {
    flex: 1,
    fontSize: 13,
    color: COLORS.text,
    lineHeight: 18,
  },
  progressContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginBottom: 20,
  },
  progressBackground: {
    flex: 1,
    height: 8,
    backgroundColor: COLORS.border,
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: COLORS.primary,
    borderRadius: 4,
  },
  progressText: {
    fontSize: 13,
    fontWeight: '600',
    color: COLORS.textSecondary,
    width: 40,
    textAlign: 'right',
  },
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    borderRadius: 12,
    gap: 8,
  },
  buttonStart: {
    backgroundColor: COLORS.primary,
  },
  buttonStop: {
    backgroundColor: COLORS.error,
  },
  buttonText: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.surface,
  },
});
