import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../utils/constants';

interface StreakBadgeProps {
  streak: number;
  size?: 'small' | 'medium' | 'large';
  showLabel?: boolean;
}

export function StreakBadge({
  streak,
  size = 'medium',
  showLabel = false,
}: StreakBadgeProps) {
  const getFlameColor = () => {
    if (streak >= 30) return '#FF4500'; // Deep orange-red for 30+ days
    if (streak >= 14) return '#FF6B35'; // Orange for 14+ days
    if (streak >= 7) return COLORS.secondary; // Amber for 7+ days
    return COLORS.accent; // Gold for < 7 days
  };

  const getSizeStyles = () => {
    switch (size) {
      case 'small':
        return {
          container: { paddingHorizontal: 8, paddingVertical: 4 },
          icon: 14,
          text: 12,
        };
      case 'large':
        return {
          container: { paddingHorizontal: 16, paddingVertical: 10 },
          icon: 24,
          text: 20,
        };
      default:
        return {
          container: { paddingHorizontal: 12, paddingVertical: 6 },
          icon: 18,
          text: 16,
        };
    }
  };

  const sizeStyles = getSizeStyles();
  const flameColor = getFlameColor();

  if (streak === 0) {
    return null;
  }

  return (
    <View style={[styles.container, sizeStyles.container]}>
      <Ionicons name="flame" size={sizeStyles.icon} color={flameColor} />
      <Text style={[styles.text, { fontSize: sizeStyles.text, color: flameColor }]}>
        {streak}
      </Text>
      {showLabel && (
        <Text style={[styles.label, { fontSize: sizeStyles.text * 0.7 }]}>
          {streak === 1 ? 'day' : 'days'}
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 217, 61, 0.15)',
    borderRadius: 20,
    gap: 4,
  },
  text: {
    fontWeight: '700',
  },
  label: {
    color: COLORS.textSecondary,
    marginLeft: 2,
  },
});
