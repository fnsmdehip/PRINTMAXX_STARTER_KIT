import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS } from '../utils/constants';
import { StreakData } from '../types';
import { getStreakMessage, isCloseToRecord, daysUntilRecord } from '../services/streakService';

interface Props {
  streak: StreakData;
  compact?: boolean;
}

export function StreakBadge({ streak, compact = false }: Props) {
  const closeToRecord = isCloseToRecord(streak);
  const daysToRecord = daysUntilRecord(streak);

  if (compact) {
    return (
      <View style={styles.compactContainer}>
        <Text style={styles.fireEmoji}>🔥</Text>
        <Text style={styles.compactNumber}>{streak.currentStreak}</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.mainStreak}>
        <Text style={styles.fireEmoji}>🔥</Text>
        <View style={styles.streakInfo}>
          <Text style={styles.streakNumber}>{streak.currentStreak}</Text>
          <Text style={styles.streakLabel}>day streak</Text>
        </View>
      </View>

      <Text style={styles.message}>{getStreakMessage(streak)}</Text>

      {closeToRecord && (
        <View style={styles.recordAlert}>
          <Text style={styles.recordAlertText}>
            {daysToRecord} day{daysToRecord !== 1 ? 's' : ''} to beat your record!
          </Text>
        </View>
      )}

      <View style={styles.stats}>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{streak.longestStreak}</Text>
          <Text style={styles.statLabel}>Best streak</Text>
        </View>
        <View style={styles.statDivider} />
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{streak.totalDaysCompleted}</Text>
          <Text style={styles.statLabel}>Total days</Text>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
  },
  compactContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFF3E0',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  fireEmoji: {
    fontSize: 24,
  },
  compactNumber: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FF6D00',
    marginLeft: 4,
  },
  mainStreak: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  streakInfo: {
    marginLeft: 12,
  },
  streakNumber: {
    fontSize: 48,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  streakLabel: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginTop: -4,
  },
  message: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 16,
  },
  recordAlert: {
    backgroundColor: '#FFF8E1',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    marginBottom: 16,
  },
  recordAlertText: {
    fontSize: 14,
    color: '#FF6D00',
    fontWeight: '500',
  },
  stats: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
    width: '100%',
  },
  statItem: {
    flex: 1,
    alignItems: 'center',
  },
  statDivider: {
    width: 1,
    height: 40,
    backgroundColor: COLORS.border,
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  statLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
});
