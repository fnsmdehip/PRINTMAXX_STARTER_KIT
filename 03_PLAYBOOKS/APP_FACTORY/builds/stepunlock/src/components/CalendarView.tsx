import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS } from '../utils/constants';
import { StreakData } from '../types';
import { getCalendarDates } from '../services/streakService';
import { getTodayDateString } from '../utils/dateUtils';

interface Props {
  streak: StreakData;
}

const DAYS_OF_WEEK = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];

export function CalendarView({ streak }: Props) {
  const calendarDates = getCalendarDates(streak);
  const today = getTodayDateString();

  // Get first day offset for proper alignment
  const firstDate = new Date(calendarDates[0].date);
  const startDayOfWeek = firstDate.getDay();

  // Pad the beginning with empty slots
  const paddedDates = [
    ...Array(startDayOfWeek).fill(null),
    ...calendarDates,
  ];

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Last 30 days</Text>

      <View style={styles.weekDaysContainer}>
        {DAYS_OF_WEEK.map((day, index) => (
          <Text key={index} style={styles.weekDay}>
            {day}
          </Text>
        ))}
      </View>

      <View style={styles.grid}>
        {paddedDates.map((item, index) => {
          if (!item) {
            return <View key={`empty-${index}`} style={styles.emptyCell} />;
          }

          const isToday = item.date === today;
          const isCompleted = item.completed;

          return (
            <View
              key={item.date}
              style={[
                styles.dayCell,
                isCompleted && styles.dayCellCompleted,
                isToday && styles.dayCellToday,
              ]}
            >
              <Text
                style={[
                  styles.dayNumber,
                  isCompleted && styles.dayNumberCompleted,
                  isToday && styles.dayNumberToday,
                ]}
              >
                {new Date(item.date).getDate()}
              </Text>
            </View>
          );
        })}
      </View>

      <View style={styles.legend}>
        <View style={styles.legendItem}>
          <View style={[styles.legendDot, styles.legendDotCompleted]} />
          <Text style={styles.legendText}>Goal met</Text>
        </View>
        <View style={styles.legendItem}>
          <View style={[styles.legendDot, styles.legendDotMissed]} />
          <Text style={styles.legendText}>Missed</Text>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 16,
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 16,
  },
  weekDaysContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 8,
  },
  weekDay: {
    width: 36,
    textAlign: 'center',
    fontSize: 12,
    fontWeight: '500',
    color: COLORS.textSecondary,
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'flex-start',
  },
  emptyCell: {
    width: 36,
    height: 36,
    margin: 2,
  },
  dayCell: {
    width: 36,
    height: 36,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    margin: 2,
    backgroundColor: '#FFEBEE',
  },
  dayCellCompleted: {
    backgroundColor: '#E8F5E9',
  },
  dayCellToday: {
    borderWidth: 2,
    borderColor: COLORS.primary,
  },
  dayNumber: {
    fontSize: 14,
    color: COLORS.error,
  },
  dayNumberCompleted: {
    color: COLORS.success,
    fontWeight: '500',
  },
  dayNumberToday: {
    fontWeight: 'bold',
  },
  legend: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 16,
    gap: 24,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  legendDot: {
    width: 12,
    height: 12,
    borderRadius: 3,
    marginRight: 6,
  },
  legendDotCompleted: {
    backgroundColor: '#E8F5E9',
  },
  legendDotMissed: {
    backgroundColor: '#FFEBEE',
  },
  legendText: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
});
