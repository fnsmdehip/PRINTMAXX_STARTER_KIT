import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Card } from '../common';
import { COLORS } from '../../utils/constants';

interface StreakCounterProps {
  currentStreak: number;
  longestStreak: number;
  showLongest?: boolean;
}

export function StreakCounter({
  currentStreak,
  longestStreak,
  showLongest = true,
}: StreakCounterProps) {
  const getStreakEmoji = (streak: number): string => {
    if (streak === 0) return '\u{1F331}'; // seedling
    if (streak < 7) return '\u{1F525}'; // fire
    if (streak < 30) return '\u{2B50}'; // star
    if (streak < 100) return '\u{1F3C6}'; // trophy
    return '\u{1F451}'; // crown
  };

  const getStreakMessage = (streak: number): string => {
    if (streak === 0) return 'Start your streak today';
    if (streak === 1) return 'Day 1! Keep going';
    if (streak < 7) return `${streak} days strong`;
    if (streak < 14) return 'One week down!';
    if (streak < 30) return 'Building a habit';
    if (streak < 100) return 'This is who you are now';
    return 'Legendary streak';
  };

  return (
    <Card style={styles.container}>
      <View style={styles.mainStreak}>
        <Text style={styles.emoji}>{getStreakEmoji(currentStreak)}</Text>
        <View style={styles.streakInfo}>
          <Text style={styles.count}>{currentStreak}</Text>
          <Text style={styles.label}>day streak</Text>
        </View>
      </View>

      <Text style={styles.message}>{getStreakMessage(currentStreak)}</Text>

      {showLongest && longestStreak > currentStreak && (
        <View style={styles.longestStreak}>
          <Text style={styles.longestLabel}>Personal best:</Text>
          <Text style={styles.longestValue}>{longestStreak} days</Text>
        </View>
      )}
    </Card>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    paddingVertical: 24,
  },
  mainStreak: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  emoji: {
    fontSize: 48,
    marginRight: 16,
  },
  streakInfo: {
    alignItems: 'flex-start',
  },
  count: {
    fontSize: 48,
    fontWeight: '800',
    color: COLORS.streak,
    lineHeight: 52,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.textSecondary,
    marginTop: -4,
  },
  message: {
    fontSize: 16,
    color: COLORS.text,
    textAlign: 'center',
    marginTop: 8,
  },
  longestStreak: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 16,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
    width: '100%',
    justifyContent: 'center',
  },
  longestLabel: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginRight: 8,
  },
  longestValue: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.primary,
  },
});
