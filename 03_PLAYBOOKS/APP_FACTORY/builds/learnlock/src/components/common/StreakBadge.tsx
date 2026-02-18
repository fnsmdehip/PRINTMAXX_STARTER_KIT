import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS, TYPOGRAPHY, SPACING } from '../../utils/constants';

interface Props {
  streak: number;
  size?: 'small' | 'medium' | 'large';
}

export function StreakBadge({ streak, size = 'medium' }: Props) {
  const sizeStyles = {
    small: {
      container: styles.containerSmall,
      icon: styles.iconSmall,
      text: styles.textSmall,
    },
    medium: {
      container: styles.containerMedium,
      icon: styles.iconMedium,
      text: styles.textMedium,
    },
    large: {
      container: styles.containerLarge,
      icon: styles.iconLarge,
      text: styles.textLarge,
    },
  };

  const { container, icon, text } = sizeStyles[size];

  if (streak === 0) {
    return (
      <View style={[styles.container, container, styles.inactive]}>
        <Text style={[styles.icon, icon]}>-</Text>
        <Text style={[styles.text, text, styles.inactiveText]}>No streak</Text>
      </View>
    );
  }

  return (
    <View style={[styles.container, container]}>
      <Text style={[styles.icon, icon]}>🔥</Text>
      <Text style={[styles.text, text]}>
        {streak} day{streak !== 1 ? 's' : ''}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.warning + '20',
    borderRadius: 20,
    paddingHorizontal: SPACING.md,
  },
  inactive: {
    backgroundColor: COLORS.surfaceSecondary,
  },
  icon: {
    marginRight: SPACING.xs,
  },
  text: {
    color: COLORS.warning,
    fontWeight: '600',
  },
  inactiveText: {
    color: COLORS.textTertiary,
  },

  // Small size
  containerSmall: {
    paddingVertical: SPACING.xs,
    paddingHorizontal: SPACING.sm,
  },
  iconSmall: {
    fontSize: 12,
  },
  textSmall: {
    ...TYPOGRAPHY.caption,
  },

  // Medium size
  containerMedium: {
    paddingVertical: SPACING.sm,
  },
  iconMedium: {
    fontSize: 16,
  },
  textMedium: {
    ...TYPOGRAPHY.bodySmall,
  },

  // Large size
  containerLarge: {
    paddingVertical: SPACING.md,
    paddingHorizontal: SPACING.lg,
  },
  iconLarge: {
    fontSize: 24,
  },
  textLarge: {
    ...TYPOGRAPHY.body,
  },
});
