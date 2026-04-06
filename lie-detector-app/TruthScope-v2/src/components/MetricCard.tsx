import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, radii, typography } from '../theme';

interface MetricCardProps {
  label: string;
  value: string;
  unit?: string;
  icon: keyof typeof Ionicons.glyphMap;
  trend?: 'up' | 'down' | 'stable';
  color?: string;
  compact?: boolean;
}

export function MetricCard({
  label,
  value,
  unit,
  icon,
  trend,
  color = colors.accent.primary,
  compact = false,
}: MetricCardProps) {
  const trendIcon = trend === 'up' ? 'arrow-up' : trend === 'down' ? 'arrow-down' : 'remove';
  const trendColor = trend === 'up' ? colors.accent.danger : trend === 'down' ? colors.accent.success : colors.text.tertiary;

  if (compact) {
    return (
      <View style={styles.compactContainer}>
        <Ionicons name={icon} size={14} color={color} />
        <Text style={styles.compactLabel}>{label}</Text>
        <Text style={[styles.compactValue, { color }]}>{value}</Text>
        {unit && <Text style={styles.compactUnit}>{unit}</Text>}
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Ionicons name={icon} size={16} color={color} />
        <Text style={styles.label}>{label}</Text>
        {trend && (
          <Ionicons name={trendIcon} size={12} color={trendColor} style={styles.trendIcon} />
        )}
      </View>
      <View style={styles.valueRow}>
        <Text style={[styles.value, { color }]}>{value}</Text>
        {unit && <Text style={styles.unit}>{unit}</Text>}
      </View>
    </View>
  );
}

interface SignalQualityProps {
  quality: number;
}

export function SignalQuality({ quality }: SignalQualityProps) {
  const dotColor =
    quality > 0.7 ? colors.accent.success :
    quality > 0.3 ? colors.accent.warning :
    colors.accent.danger;

  const label =
    quality > 0.7 ? 'Strong' :
    quality > 0.3 ? 'Fair' :
    'Weak';

  return (
    <View style={styles.signalContainer}>
      <View style={[styles.signalDot, { backgroundColor: dotColor }]} />
      <Text style={[styles.signalLabel, { color: dotColor }]}>{label}</Text>
    </View>
  );
}

interface StressBarProps {
  level: number;
  label: string;
}

export function StressBar({ level, label }: StressBarProps) {
  const barColor =
    level < 30 ? colors.accent.success :
    level < 60 ? colors.accent.warning :
    colors.accent.danger;

  return (
    <View style={styles.stressContainer}>
      <View style={styles.stressHeader}>
        <Text style={styles.stressLabel}>{label}</Text>
        <Text style={[styles.stressValue, { color: barColor }]}>{Math.round(level)}%</Text>
      </View>
      <View style={styles.stressTrack}>
        <View
          style={[
            styles.stressFill,
            { width: `${Math.min(100, level)}%`, backgroundColor: barColor },
          ]}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: colors.bg.card,
    borderRadius: radii.md,
    padding: spacing.md,
    minWidth: 100,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginBottom: 6,
  },
  label: {
    ...typography.caption,
    color: colors.text.secondary,
    flex: 1,
  },
  trendIcon: {
    marginLeft: 4,
  },
  valueRow: {
    flexDirection: 'row',
    alignItems: 'baseline',
    gap: 4,
  },
  value: {
    fontSize: 24,
    fontWeight: '700',
  },
  unit: {
    ...typography.caption,
    color: colors.text.tertiary,
  },
  compactContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingVertical: 4,
    paddingHorizontal: 8,
    backgroundColor: colors.bg.card,
    borderRadius: radii.sm,
  },
  compactLabel: {
    ...typography.small,
    color: colors.text.tertiary,
  },
  compactValue: {
    ...typography.bodyBold,
    fontSize: 14,
  },
  compactUnit: {
    ...typography.small,
    color: colors.text.tertiary,
  },
  signalContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  signalDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  signalLabel: {
    ...typography.small,
  },
  stressContainer: {
    gap: 4,
  },
  stressHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  stressLabel: {
    ...typography.caption,
    color: colors.text.secondary,
  },
  stressValue: {
    ...typography.caption,
    fontWeight: '700',
  },
  stressTrack: {
    height: 4,
    backgroundColor: colors.bg.tertiary,
    borderRadius: 2,
    overflow: 'hidden',
  },
  stressFill: {
    height: '100%',
    borderRadius: 2,
  },
});
