import React from 'react';
import { View, StyleSheet, Text } from 'react-native';
import { COLORS, SPACING, BORDER_RADIUS } from '../constants/theme';
import { DailySteps } from '../constants/types';

interface StepHistoryChartProps {
  data: DailySteps[];
  period: 'week' | 'month';
}

export const StepHistoryChart: React.FC<StepHistoryChartProps> = ({
  data,
  period,
}) => {
  const maxSteps = Math.max(...data.map(d => d.steps), 1);
  const displayData = period === 'week' ? data.slice(0, 7) : data.slice(0, 30);

  const getDayLabel = (dateStr: string, index: number) => {
    const date = new Date(dateStr);
    if (period === 'week') {
      return date.toLocaleDateString('en-US', { weekday: 'short' }).charAt(0);
    }
    return index % 5 === 0 ? date.getDate().toString() : '';
  };

  const getBarWidth = () => {
    if (period === 'week') return 36;
    return 8;
  };

  return (
    <View style={styles.container}>
      <View style={styles.chartContainer}>
        {displayData.reverse().map((day, index) => {
          const barHeight = (day.steps / maxSteps) * 120;
          const isGoalMet = day.goalMet;

          return (
            <View key={day.date || index} style={styles.barContainer}>
              <View style={styles.barWrapper}>
                <View
                  style={[
                    styles.bar,
                    {
                      height: Math.max(barHeight, 4),
                      width: getBarWidth(),
                      backgroundColor: isGoalMet ? COLORS.primary : COLORS.backgroundLighter,
                    },
                  ]}
                />
              </View>
              {period === 'week' && (
                <Text style={styles.dayLabel}>
                  {getDayLabel(day.date, index)}
                </Text>
              )}
            </View>
          );
        })}
      </View>
      <View style={styles.legend}>
        <View style={styles.legendItem}>
          <View style={[styles.legendDot, { backgroundColor: COLORS.primary }]} />
          <Text style={styles.legendText}>Goal met</Text>
        </View>
        <View style={styles.legendItem}>
          <View style={[styles.legendDot, { backgroundColor: COLORS.backgroundLighter }]} />
          <Text style={styles.legendText}>Below goal</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.lg,
  },
  chartContainer: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    justifyContent: 'space-between',
    height: 150,
    paddingBottom: SPACING.lg,
  },
  barContainer: {
    alignItems: 'center',
    flex: 1,
  },
  barWrapper: {
    height: 120,
    justifyContent: 'flex-end',
  },
  bar: {
    borderRadius: BORDER_RADIUS.sm,
  },
  dayLabel: {
    fontSize: 12,
    color: COLORS.textMuted,
    marginTop: SPACING.xs,
  },
  legend: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: SPACING.lg,
    borderTopWidth: 1,
    borderTopColor: COLORS.backgroundLighter,
    paddingTop: SPACING.md,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  legendDot: {
    width: 10,
    height: 10,
    borderRadius: BORDER_RADIUS.full,
    marginRight: SPACING.xs,
  },
  legendText: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
});
