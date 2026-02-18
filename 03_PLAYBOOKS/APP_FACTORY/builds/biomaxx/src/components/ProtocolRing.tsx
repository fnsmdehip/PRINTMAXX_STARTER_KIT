import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../utils/constants';

interface ProtocolRingProps {
  progress: number;
  icon: string;
  label: string;
  value: string;
  size?: number;
  strokeWidth?: number;
  color?: string;
}

export function ProtocolRing({
  progress,
  icon,
  label,
  value,
  size = 100,
  strokeWidth = 8,
  color = COLORS.primary,
}: ProtocolRingProps) {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const progressValue = Math.min(Math.max(progress, 0), 100);
  const strokeDashoffset = circumference - (progressValue / 100) * circumference;

  return (
    <View style={[styles.container, { width: size, height: size }]}>
      {/* Background ring */}
      <View
        style={[
          styles.ring,
          {
            width: size,
            height: size,
            borderRadius: size / 2,
            borderWidth: strokeWidth,
            borderColor: COLORS.surfaceLight,
          },
        ]}
      />

      {/* Progress ring - using a simpler approach without SVG */}
      <View
        style={[
          styles.progressRing,
          {
            width: size,
            height: size,
            borderRadius: size / 2,
            borderWidth: strokeWidth,
            borderColor: 'transparent',
            borderTopColor: color,
            borderRightColor: progressValue > 25 ? color : 'transparent',
            borderBottomColor: progressValue > 50 ? color : 'transparent',
            borderLeftColor: progressValue > 75 ? color : 'transparent',
            transform: [{ rotate: '-90deg' }],
          },
        ]}
      />

      {/* Inner content */}
      <View style={styles.innerContent}>
        <Ionicons
          name={icon as any}
          size={size * 0.24}
          color={progress >= 100 ? COLORS.accent : COLORS.text}
        />
        <Text
          style={[
            styles.value,
            { fontSize: size * 0.14 },
            progress >= 100 && styles.valueComplete,
          ]}
          numberOfLines={1}
        >
          {value}
        </Text>
        <Text
          style={[styles.label, { fontSize: size * 0.1 }]}
          numberOfLines={1}
        >
          {label}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  ring: {
    position: 'absolute',
  },
  progressRing: {
    position: 'absolute',
  },
  innerContent: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 8,
  },
  value: {
    color: COLORS.text,
    fontWeight: '600',
    marginTop: 2,
  },
  valueComplete: {
    color: COLORS.accent,
  },
  label: {
    color: COLORS.textMuted,
    marginTop: 1,
  },
});
