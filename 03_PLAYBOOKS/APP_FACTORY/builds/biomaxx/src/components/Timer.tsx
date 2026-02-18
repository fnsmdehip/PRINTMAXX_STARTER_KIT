import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { COLORS } from '../utils/constants';

interface TimerProps {
  isRunning: boolean;
  isPaused: boolean;
  startTime: number;
  targetMinutes?: number;
  onPause: () => void;
  onResume: () => void;
  onEnd: () => void;
}

export function Timer({
  isRunning,
  isPaused,
  startTime,
  targetMinutes,
  onPause,
  onResume,
  onEnd,
}: TimerProps) {
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    if (!isRunning || isPaused) return;

    const interval = setInterval(() => {
      setElapsed(Math.floor((Date.now() - startTime) / 1000));
    }, 1000);

    return () => clearInterval(interval);
  }, [isRunning, isPaused, startTime]);

  const formatTime = useCallback((seconds: number) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (hrs > 0) {
      return `${hrs}:${mins.toString().padStart(2, '0')}:${secs
        .toString()
        .padStart(2, '0')}`;
    }
    return `${mins.toString().padStart(2, '0')}:${secs
      .toString()
      .padStart(2, '0')}`;
  }, []);

  const handlePauseResume = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    if (isPaused) {
      onResume();
    } else {
      onPause();
    }
  };

  const handleEnd = () => {
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    onEnd();
  };

  const progress = targetMinutes
    ? Math.min((elapsed / 60 / targetMinutes) * 100, 100)
    : 0;

  const isComplete = targetMinutes && elapsed / 60 >= targetMinutes;

  return (
    <View style={styles.container}>
      {/* Progress ring background */}
      <View style={styles.ringContainer}>
        <View style={styles.ringBackground} />
        <View
          style={[
            styles.ringProgress,
            {
              transform: [{ rotate: `${(progress / 100) * 360 - 90}deg` }],
              borderTopColor: isComplete ? COLORS.accent : COLORS.primary,
              borderRightColor:
                progress > 25
                  ? isComplete
                    ? COLORS.accent
                    : COLORS.primary
                  : 'transparent',
              borderBottomColor:
                progress > 50
                  ? isComplete
                    ? COLORS.accent
                    : COLORS.primary
                  : 'transparent',
              borderLeftColor:
                progress > 75
                  ? isComplete
                    ? COLORS.accent
                    : COLORS.primary
                  : 'transparent',
            },
          ]}
        />

        {/* Timer display */}
        <View style={styles.timerContent}>
          <Text style={[styles.time, isComplete && styles.timeComplete]}>
            {formatTime(elapsed)}
          </Text>
          {targetMinutes && (
            <Text style={styles.target}>
              / {targetMinutes < 60 ? `${targetMinutes}m` : `${targetMinutes / 60}h`}
            </Text>
          )}
          {isComplete && (
            <View style={styles.completeIndicator}>
              <Ionicons name="checkmark-circle" size={24} color={COLORS.accent} />
              <Text style={styles.completeText}>Goal reached!</Text>
            </View>
          )}
        </View>
      </View>

      {/* Controls */}
      <View style={styles.controls}>
        <TouchableOpacity
          style={[styles.controlButton, styles.pauseButton]}
          onPress={handlePauseResume}
          activeOpacity={0.8}
        >
          <Ionicons
            name={isPaused ? 'play' : 'pause'}
            size={28}
            color={COLORS.text}
          />
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.controlButton, styles.endButton]}
          onPress={handleEnd}
          activeOpacity={0.8}
        >
          <Ionicons name="stop" size={28} color={COLORS.text} />
        </TouchableOpacity>
      </View>

      {isPaused && (
        <Text style={styles.pausedText}>Paused</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    padding: 24,
  },
  ringContainer: {
    width: 220,
    height: 220,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 32,
  },
  ringBackground: {
    position: 'absolute',
    width: 220,
    height: 220,
    borderRadius: 110,
    borderWidth: 12,
    borderColor: COLORS.surfaceLight,
  },
  ringProgress: {
    position: 'absolute',
    width: 220,
    height: 220,
    borderRadius: 110,
    borderWidth: 12,
    borderColor: 'transparent',
  },
  timerContent: {
    alignItems: 'center',
  },
  time: {
    fontSize: 48,
    fontWeight: '300',
    color: COLORS.text,
    fontVariant: ['tabular-nums'],
  },
  timeComplete: {
    color: COLORS.accent,
  },
  target: {
    fontSize: 16,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  completeIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 12,
    gap: 6,
  },
  completeText: {
    fontSize: 14,
    color: COLORS.accent,
    fontWeight: '600',
  },
  controls: {
    flexDirection: 'row',
    gap: 24,
  },
  controlButton: {
    width: 64,
    height: 64,
    borderRadius: 32,
    justifyContent: 'center',
    alignItems: 'center',
  },
  pauseButton: {
    backgroundColor: COLORS.surfaceLight,
  },
  endButton: {
    backgroundColor: COLORS.error,
  },
  pausedText: {
    marginTop: 16,
    fontSize: 14,
    color: COLORS.textSecondary,
    fontStyle: 'italic',
  },
});
