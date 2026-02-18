import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import Svg, { Circle } from 'react-native-svg';
import { COLORS } from '../utils/constants';

interface Props {
  progress: number; // 0-1
  steps: number;
  goal: number;
  size?: number;
  strokeWidth?: number;
}

export function ProgressRing({
  progress,
  steps,
  goal,
  size = 250,
  strokeWidth = 15,
}: Props) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const progressOffset = circumference * (1 - Math.min(progress, 1));
  const center = size / 2;

  const remaining = Math.max(0, goal - steps);
  const isComplete = steps >= goal;

  return (
    <View style={[styles.container, { width: size, height: size }]}>
      <Svg width={size} height={size}>
        {/* Background circle */}
        <Circle
          cx={center}
          cy={center}
          r={radius}
          stroke={COLORS.border}
          strokeWidth={strokeWidth}
          fill="none"
        />
        {/* Progress circle */}
        <Circle
          cx={center}
          cy={center}
          r={radius}
          stroke={isComplete ? COLORS.success : COLORS.primary}
          strokeWidth={strokeWidth}
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={progressOffset}
          strokeLinecap="round"
          transform={`rotate(-90 ${center} ${center})`}
        />
      </Svg>
      <View style={styles.textContainer}>
        <Text style={styles.steps}>{steps.toLocaleString()}</Text>
        <Text style={styles.goal}>/ {goal.toLocaleString()}</Text>
        {!isComplete && (
          <Text style={styles.remaining}>
            {remaining.toLocaleString()} to go
          </Text>
        )}
        {isComplete && (
          <Text style={styles.complete}>Goal reached!</Text>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  textContainer: {
    position: 'absolute',
    justifyContent: 'center',
    alignItems: 'center',
  },
  steps: {
    fontSize: 48,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  goal: {
    fontSize: 18,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  remaining: {
    fontSize: 16,
    color: COLORS.textSecondary,
    marginTop: 8,
  },
  complete: {
    fontSize: 16,
    color: COLORS.success,
    fontWeight: '600',
    marginTop: 8,
  },
});
