import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS, TYPOGRAPHY, SPACING } from '../../utils/constants';
import { DailyStudyData } from '../../types';
import { getDayName, formatDurationShort, getTodayDateString } from '../../utils/dateUtils';

interface Props {
  weekData: DailyStudyData[];
  goalMinutes?: number; // optional daily goal line
}

const MAX_BAR_HEIGHT = 120;
const BAR_WIDTH = 36;

export function WeeklyChart({ weekData, goalMinutes = 25 }: Props) {
  // Find max value for scaling
  const maxTime = Math.max(
    ...weekData.map((d) => d.totalStudyTime),
    goalMinutes * 60 // Ensure goal line is visible
  );

  const goalHeight = (goalMinutes * 60 / maxTime) * MAX_BAR_HEIGHT;
  const today = getTodayDateString();

  return (
    <View style={styles.container}>
      <Text style={styles.title}>This Week</Text>

      <View style={styles.chartContainer}>
        {/* Goal line */}
        <View style={[styles.goalLine, { bottom: goalHeight }]}>
          <Text style={styles.goalLabel}>{goalMinutes}m goal</Text>
        </View>

        {/* Bars */}
        <View style={styles.barsContainer}>
          {weekData.map((day) => {
            const barHeight =
              maxTime > 0
                ? (day.totalStudyTime / maxTime) * MAX_BAR_HEIGHT
                : 0;

            const isToday = day.date === today;
            const hasStudied = day.totalStudyTime > 0;

            return (
              <View key={day.date} style={styles.barColumn}>
                <View style={styles.barWrapper}>
                  <View
                    style={[
                      styles.bar,
                      {
                        height: Math.max(barHeight, hasStudied ? 4 : 0),
                        backgroundColor: hasStudied
                          ? day.streakMaintained
                            ? COLORS.secondary
                            : COLORS.primary
                          : COLORS.surfaceSecondary,
                      },
                    ]}
                  />
                </View>
                <Text
                  style={[
                    styles.dayLabel,
                    isToday && styles.todayLabel,
                  ]}
                >
                  {getDayName(day.date)}
                </Text>
                {hasStudied && (
                  <Text style={styles.timeLabel}>
                    {formatDurationShort(day.totalStudyTime)}
                  </Text>
                )}
              </View>
            );
          })}
        </View>
      </View>

      <View style={styles.legend}>
        <View style={styles.legendItem}>
          <View style={[styles.legendDot, { backgroundColor: COLORS.secondary }]} />
          <Text style={styles.legendText}>Goal met (25m+)</Text>
        </View>
        <View style={styles.legendItem}>
          <View style={[styles.legendDot, { backgroundColor: COLORS.primary }]} />
          <Text style={styles.legendText}>Studied</Text>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.lg,
    shadowColor: COLORS.text,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  title: {
    ...TYPOGRAPHY.h3,
    color: COLORS.text,
    marginBottom: SPACING.lg,
  },
  chartContainer: {
    height: MAX_BAR_HEIGHT + 60,
    position: 'relative',
  },
  goalLine: {
    position: 'absolute',
    left: 0,
    right: 0,
    borderTopWidth: 1,
    borderTopColor: COLORS.warning,
    borderStyle: 'dashed',
  },
  goalLabel: {
    ...TYPOGRAPHY.caption,
    color: COLORS.warning,
    position: 'absolute',
    right: 0,
    top: -16,
  },
  barsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
    height: MAX_BAR_HEIGHT,
    paddingTop: 20,
  },
  barColumn: {
    alignItems: 'center',
    width: BAR_WIDTH,
  },
  barWrapper: {
    height: MAX_BAR_HEIGHT,
    justifyContent: 'flex-end',
  },
  bar: {
    width: BAR_WIDTH - 8,
    borderRadius: 4,
    minHeight: 0,
  },
  dayLabel: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textSecondary,
    marginTop: SPACING.sm,
  },
  todayLabel: {
    color: COLORS.primary,
    fontWeight: '600',
  },
  timeLabel: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textTertiary,
    fontSize: 10,
  },
  legend: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: SPACING.lg,
    marginTop: SPACING.lg,
    paddingTop: SPACING.md,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  legendDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: SPACING.xs,
  },
  legendText: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textSecondary,
  },
});
