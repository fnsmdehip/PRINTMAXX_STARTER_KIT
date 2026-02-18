import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS, TYPOGRAPHY, SPACING } from '../../utils/constants';
import { formatDuration } from '../../utils/dateUtils';

interface Props {
  todayStudyTime: number; // seconds
  sessionsCompleted: number;
  weeklyAverage: number; // seconds
  currentStreak: number;
}

export function DailyStats({
  todayStudyTime,
  sessionsCompleted,
  weeklyAverage,
  currentStreak,
}: Props) {
  return (
    <View style={styles.container}>
      <View style={styles.row}>
        <StatCard
          label="Today"
          value={formatDuration(todayStudyTime)}
          sublabel="study time"
          color={COLORS.primary}
        />
        <StatCard
          label="Sessions"
          value={String(sessionsCompleted)}
          sublabel="completed"
          color={COLORS.secondary}
        />
      </View>
      <View style={styles.row}>
        <StatCard
          label="Daily Avg"
          value={formatDuration(weeklyAverage)}
          sublabel="this week"
          color={COLORS.primaryLight}
        />
        <StatCard
          label="Streak"
          value={`${currentStreak}`}
          sublabel={currentStreak === 1 ? 'day' : 'days'}
          color={COLORS.warning}
          icon="🔥"
        />
      </View>
    </View>
  );
}

interface StatCardProps {
  label: string;
  value: string;
  sublabel: string;
  color: string;
  icon?: string;
}

function StatCard({ label, value, sublabel, color, icon }: StatCardProps) {
  return (
    <View style={styles.card}>
      <Text style={styles.cardLabel}>{label}</Text>
      <View style={styles.valueRow}>
        {icon && <Text style={styles.icon}>{icon}</Text>}
        <Text style={[styles.cardValue, { color }]}>{value}</Text>
      </View>
      <Text style={styles.cardSublabel}>{sublabel}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    gap: SPACING.md,
  },
  row: {
    flexDirection: 'row',
    gap: SPACING.md,
  },
  card: {
    flex: 1,
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.md,
    alignItems: 'center',
    shadowColor: COLORS.text,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  cardLabel: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textSecondary,
    marginBottom: SPACING.xs,
  },
  valueRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  icon: {
    fontSize: 20,
    marginRight: SPACING.xs,
  },
  cardValue: {
    ...TYPOGRAPHY.h2,
    fontVariant: ['tabular-nums'],
  },
  cardSublabel: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textTertiary,
    marginTop: SPACING.xs,
  },
});
