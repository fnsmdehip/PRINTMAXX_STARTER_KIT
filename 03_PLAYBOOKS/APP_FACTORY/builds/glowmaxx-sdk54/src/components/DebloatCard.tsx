import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../utils/constants';

interface DebloatCardProps {
  sleepHours: number;
  sodiumLevel: 'low' | 'medium' | 'high';
  onSleepPress: () => void;
  onSodiumPress: () => void;
}

const SODIUM_CONFIG = {
  low: { label: 'Low', color: COLORS.success, icon: 'checkmark-circle' as const },
  medium: { label: 'Medium', color: COLORS.warning, icon: 'alert-circle' as const },
  high: { label: 'High', color: COLORS.error, icon: 'close-circle' as const },
};

export function DebloatCard({
  sleepHours,
  sodiumLevel,
  onSleepPress,
  onSodiumPress,
}: DebloatCardProps) {
  const sodiumConfig = SODIUM_CONFIG[sodiumLevel];
  const sleepQuality =
    sleepHours >= 7 ? 'Good' : sleepHours >= 5 ? 'Fair' : 'Poor';
  const sleepColor =
    sleepHours >= 7
      ? COLORS.success
      : sleepHours >= 5
      ? COLORS.warning
      : COLORS.error;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Debloat Tracker</Text>
      <Text style={styles.subtitle}>
        Track factors that affect facial puffiness
      </Text>

      <View style={styles.grid}>
        {/* Sleep */}
        <TouchableOpacity style={styles.card} onPress={onSleepPress}>
          <View style={[styles.iconContainer, { backgroundColor: '#E8F5E9' }]}>
            <Ionicons name="bed-outline" size={24} color={sleepColor} />
          </View>
          <Text style={styles.cardLabel}>Sleep</Text>
          <Text style={[styles.cardValue, { color: sleepColor }]}>
            {sleepHours > 0 ? `${sleepHours}h` : '--'}
          </Text>
          <Text style={styles.cardQuality}>{sleepHours > 0 ? sleepQuality : 'Tap to log'}</Text>
        </TouchableOpacity>

        {/* Sodium */}
        <TouchableOpacity style={styles.card} onPress={onSodiumPress}>
          <View style={[styles.iconContainer, { backgroundColor: '#FFF3E0' }]}>
            <Ionicons
              name={sodiumConfig.icon}
              size={24}
              color={sodiumConfig.color}
            />
          </View>
          <Text style={styles.cardLabel}>Sodium</Text>
          <Text style={[styles.cardValue, { color: sodiumConfig.color }]}>
            {sodiumConfig.label}
          </Text>
          <Text style={styles.cardQuality}>Today's intake</Text>
        </TouchableOpacity>
      </View>

      {/* Tips based on current values */}
      <View style={styles.tipContainer}>
        <Ionicons name="bulb-outline" size={16} color={COLORS.warning} />
        <Text style={styles.tipText}>
          {sleepHours < 7 && sodiumLevel !== 'low'
            ? 'Low sleep + high sodium = max bloat. Prioritize both.'
            : sleepHours < 7
            ? 'Aim for 7-9 hours. Sleep affects face puffiness directly.'
            : sodiumLevel !== 'low'
            ? 'High sodium holds water. Keep under 2000mg for definition.'
            : 'Great job! Keep it up for a leaner face.'}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginBottom: 16,
  },
  grid: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 16,
  },
  card: {
    flex: 1,
    backgroundColor: COLORS.background,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  iconContainer: {
    width: 48,
    height: 48,
    borderRadius: 24,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
  },
  cardLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginBottom: 4,
  },
  cardValue: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  cardQuality: {
    fontSize: 11,
    color: COLORS.textLight,
    marginTop: 2,
  },
  tipContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    backgroundColor: '#FFF8E1',
    padding: 12,
    borderRadius: 12,
    gap: 8,
  },
  tipText: {
    flex: 1,
    fontSize: 13,
    color: COLORS.text,
    lineHeight: 18,
  },
});
