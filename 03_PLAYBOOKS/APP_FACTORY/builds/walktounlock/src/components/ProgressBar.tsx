import React from 'react';
import { View, StyleSheet, Text } from 'react-native';
import { COLORS, BORDER_RADIUS } from '../constants/theme';

interface ProgressBarProps {
  progress: number;
  height?: number;
  showLabel?: boolean;
  label?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  height = 12,
  showLabel = false,
  label,
}) => {
  const clampedProgress = Math.min(Math.max(progress, 0), 1);

  return (
    <View style={styles.container}>
      {showLabel && (
        <View style={styles.labelContainer}>
          <Text style={styles.label}>{label}</Text>
          <Text style={styles.percentage}>{Math.round(clampedProgress * 100)}%</Text>
        </View>
      )}
      <View style={[styles.track, { height }]}>
        <View
          style={[
            styles.fill,
            {
              width: `${clampedProgress * 100}%`,
              height,
            },
          ]}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
  },
  labelContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  label: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  percentage: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.text,
  },
  track: {
    backgroundColor: COLORS.backgroundLighter,
    borderRadius: BORDER_RADIUS.full,
    overflow: 'hidden',
  },
  fill: {
    backgroundColor: COLORS.primary,
    borderRadius: BORDER_RADIUS.full,
  },
});
