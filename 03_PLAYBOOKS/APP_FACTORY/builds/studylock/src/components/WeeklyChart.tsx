import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS } from '../utils/constants';
import { DailyStats } from '../types';
import { getLast7Days, getDayOfWeek } from '../utils/timer';

interface WeeklyChartProps {
  dailyStats: DailyStats[];
  height?: number;
}

export const WeeklyChart: React.FC<WeeklyChartProps> = ({
  dailyStats,
  height = 120,
}) => {
  const days = getLast7Days();

  // Create a map for quick lookup
  const statsMap = new Map<string, DailyStats>();
  dailyStats.forEach((stat) => {
    statsMap.set(stat.date, stat);
  });

  // Get data for each day
  const data = days.map((date) => {
    const stat = statsMap.get(date);
    return {
      date,
      dayLabel: getDayOfWeek(date),
      minutes: stat?.totalMinutes || 0,
    };
  });

  // Calculate max for scaling
  const maxMinutes = Math.max(...data.map((d) => d.minutes), 60);

  const renderBar = (day: (typeof data)[0], index: number) => {
    const barHeight = day.minutes > 0 ? (day.minutes / maxMinutes) * height : 4;
    const isToday = index === data.length - 1;

    return (
      <View key={day.date} style={styles.barContainer}>
        <View style={styles.barWrapper}>
          <View
            style={[
              styles.bar,
              {
                height: barHeight,
                backgroundColor: isToday ? COLORS.primary : COLORS.primaryLight,
              },
            ]}
          />
        </View>
        <Text style={[styles.dayLabel, isToday && styles.dayLabelToday]}>
          {day.dayLabel}
        </Text>
        {day.minutes > 0 && (
          <Text style={styles.minuteLabel}>{day.minutes}m</Text>
        )}
      </View>
    );
  };

  const totalWeek = data.reduce((sum, d) => sum + d.minutes, 0);
  const avgPerDay = Math.round(totalWeek / 7);

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>This Week</Text>
        <Text style={styles.summary}>
          {totalWeek}m total, {avgPerDay}m avg/day
        </Text>
      </View>

      <View style={[styles.chartContainer, { height: height + 40 }]}>
        {data.map((day, index) => renderBar(day, index))}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
  },
  summary: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
  chartContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
  },
  barContainer: {
    flex: 1,
    alignItems: 'center',
  },
  barWrapper: {
    flex: 1,
    justifyContent: 'flex-end',
    marginBottom: 8,
  },
  bar: {
    width: 24,
    borderRadius: 6,
    minHeight: 4,
  },
  dayLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    fontWeight: '500',
  },
  dayLabelToday: {
    color: COLORS.primary,
    fontWeight: '700',
  },
  minuteLabel: {
    fontSize: 10,
    color: COLORS.textMuted,
    marginTop: 2,
  },
});

export default WeeklyChart;
