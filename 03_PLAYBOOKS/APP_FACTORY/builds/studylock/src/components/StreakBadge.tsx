import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, STREAK_MILESTONES } from '../utils/constants';
import { getStreakMessage } from '../utils/timer';

interface StreakBadgeProps {
  streak: number;
  size?: 'small' | 'medium' | 'large';
  showMessage?: boolean;
}

export const StreakBadge: React.FC<StreakBadgeProps> = ({
  streak,
  size = 'medium',
  showMessage = true,
}) => {
  const getBadgeColor = () => {
    if (streak >= 100) return '#FFD700'; // Gold
    if (streak >= 30) return '#C0C0C0'; // Silver
    if (streak >= 7) return '#CD7F32'; // Bronze
    return COLORS.accent;
  };

  const getIconSize = () => {
    switch (size) {
      case 'small':
        return 16;
      case 'large':
        return 32;
      default:
        return 24;
    }
  };

  const badgeColor = getBadgeColor();
  const iconSize = getIconSize();
  const isAtMilestone = STREAK_MILESTONES.includes(streak);

  return (
    <View style={[styles.container, styles[`${size}Container`]]}>
      <View
        style={[
          styles.badge,
          styles[`${size}Badge`],
          { backgroundColor: badgeColor },
          isAtMilestone && styles.milestone,
        ]}
      >
        <Ionicons name="flame" size={iconSize} color={COLORS.white} />
        <Text style={[styles.count, styles[`${size}Count`]]}>{streak}</Text>
      </View>

      {showMessage && (
        <Text style={[styles.message, styles[`${size}Message`]]}>
          {getStreakMessage(streak)}
        </Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
  },
  smallContainer: {
    flexDirection: 'row',
    gap: 8,
  },
  mediumContainer: {},
  largeContainer: {},
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    borderRadius: 20,
    gap: 4,
  },
  smallBadge: {
    paddingVertical: 4,
    paddingHorizontal: 8,
  },
  mediumBadge: {
    paddingVertical: 8,
    paddingHorizontal: 16,
  },
  largeBadge: {
    paddingVertical: 12,
    paddingHorizontal: 24,
  },
  milestone: {
    shadowColor: '#FFD700',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.5,
    shadowRadius: 10,
    elevation: 8,
  },
  count: {
    color: COLORS.white,
    fontWeight: '700',
  },
  smallCount: {
    fontSize: 14,
  },
  mediumCount: {
    fontSize: 18,
  },
  largeCount: {
    fontSize: 24,
  },
  message: {
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  smallMessage: {
    fontSize: 12,
    marginTop: 0,
  },
  mediumMessage: {
    fontSize: 14,
  },
  largeMessage: {
    fontSize: 16,
  },
});

export default StreakBadge;
