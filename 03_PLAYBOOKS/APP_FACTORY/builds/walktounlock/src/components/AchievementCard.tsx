import React from 'react';
import { View, StyleSheet, Text, Pressable } from 'react-native';
import { COLORS, SPACING, BORDER_RADIUS } from '../constants/theme';
import { Achievement } from '../constants/types';

interface AchievementCardProps {
  achievement: Achievement;
  unlocked: boolean;
  progress?: number;
  onPress?: () => void;
}

const TIER_COLORS = {
  bronze: COLORS.bronze,
  silver: COLORS.silver,
  gold: COLORS.gold,
};

const TIER_ICONS: Record<string, string> = {
  'shoe-prints': '👟',
  'sun': '☀️',
  'walking': '🚶',
  'crown': '👑',
  'fire': '🔥',
  'fire-alt': '🔥',
  'medal': '🏅',
  'trophy': '🏆',
  'gem': '💎',
  'running': '🏃',
  'bolt': '⚡',
  'star': '⭐',
  'chart-line': '📈',
  'mountain': '⛰️',
  'award': '🎖️',
  'globe': '🌍',
  'infinity': '♾️',
};

export const AchievementCard: React.FC<AchievementCardProps> = ({
  achievement,
  unlocked,
  progress = 0,
  onPress,
}) => {
  const tierColor = TIER_COLORS[achievement.tier];
  const icon = TIER_ICONS[achievement.icon] || '🎯';

  return (
    <Pressable
      style={({ pressed }) => [
        styles.card,
        !unlocked && styles.cardLocked,
        pressed && styles.cardPressed,
      ]}
      onPress={onPress}
    >
      <View
        style={[
          styles.iconContainer,
          { borderColor: unlocked ? tierColor : COLORS.backgroundLighter },
        ]}
      >
        <Text style={[styles.icon, !unlocked && styles.iconLocked]}>{icon}</Text>
      </View>
      <View style={styles.content}>
        <Text style={[styles.title, !unlocked && styles.textLocked]}>
          {achievement.title}
        </Text>
        <Text style={[styles.description, !unlocked && styles.textLocked]}>
          {achievement.description}
        </Text>
        {!unlocked && progress > 0 && (
          <View style={styles.progressContainer}>
            <View style={styles.progressTrack}>
              <View
                style={[styles.progressFill, { width: `${Math.min(progress, 100)}%` }]}
              />
            </View>
            <Text style={styles.progressText}>{Math.round(progress)}%</Text>
          </View>
        )}
      </View>
      {unlocked && (
        <View style={[styles.badge, { backgroundColor: tierColor }]}>
          <Text style={styles.badgeText}>✓</Text>
        </View>
      )}
    </Pressable>
  );
};

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
  },
  cardLocked: {
    opacity: 0.6,
  },
  cardPressed: {
    opacity: 0.8,
    transform: [{ scale: 0.98 }],
  },
  iconContainer: {
    width: 56,
    height: 56,
    borderRadius: BORDER_RADIUS.full,
    backgroundColor: COLORS.backgroundLight,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    marginRight: SPACING.md,
  },
  icon: {
    fontSize: 24,
  },
  iconLocked: {
    opacity: 0.5,
  },
  content: {
    flex: 1,
  },
  title: {
    fontSize: 16,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 2,
  },
  description: {
    fontSize: 13,
    color: COLORS.textSecondary,
  },
  textLocked: {
    color: COLORS.textMuted,
  },
  progressContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: SPACING.sm,
  },
  progressTrack: {
    flex: 1,
    height: 4,
    backgroundColor: COLORS.backgroundLighter,
    borderRadius: BORDER_RADIUS.full,
    marginRight: SPACING.sm,
  },
  progressFill: {
    height: '100%',
    backgroundColor: COLORS.primary,
    borderRadius: BORDER_RADIUS.full,
  },
  progressText: {
    fontSize: 11,
    color: COLORS.textMuted,
    width: 36,
  },
  badge: {
    width: 24,
    height: 24,
    borderRadius: BORDER_RADIUS.full,
    justifyContent: 'center',
    alignItems: 'center',
  },
  badgeText: {
    fontSize: 12,
    fontWeight: '700',
    color: COLORS.background,
  },
});
