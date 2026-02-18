import React, { useMemo } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { format, isSameDay, isToday, startOfMonth, endOfMonth, eachDayOfInterval, getDay, subMonths, addMonths } from 'date-fns';
import { Card } from '../common';
import { COLORS } from '../../utils/constants';
import { formatDate } from '../../utils/dateUtils';

interface StreakCalendarProps {
  completedDates: string[];
  currentMonth?: Date;
  onMonthChange?: (date: Date) => void;
  onDayPress?: (date: string) => void;
}

const WEEKDAYS = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];

export function StreakCalendar({
  completedDates,
  currentMonth = new Date(),
  onMonthChange,
  onDayPress,
}: StreakCalendarProps) {
  const completedSet = useMemo(
    () => new Set(completedDates),
    [completedDates]
  );

  const calendarDays = useMemo(() => {
    const start = startOfMonth(currentMonth);
    const end = endOfMonth(currentMonth);
    const days = eachDayOfInterval({ start, end });

    // Add padding for days before the first of the month
    const startPadding = getDay(start);
    const paddedDays: (Date | null)[] = Array(startPadding).fill(null);

    return [...paddedDays, ...days];
  }, [currentMonth]);

  const goToPreviousMonth = () => {
    onMonthChange?.(subMonths(currentMonth, 1));
  };

  const goToNextMonth = () => {
    onMonthChange?.(addMonths(currentMonth, 1));
  };

  const handleDayPress = (date: Date) => {
    onDayPress?.(formatDate(date));
  };

  const isCompleted = (date: Date): boolean => {
    return completedSet.has(formatDate(date));
  };

  return (
    <Card style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={goToPreviousMonth} style={styles.navButton}>
          <Text style={styles.navText}>{'\u2039'}</Text>
        </TouchableOpacity>
        <Text style={styles.monthTitle}>
          {format(currentMonth, 'MMMM yyyy')}
        </Text>
        <TouchableOpacity onPress={goToNextMonth} style={styles.navButton}>
          <Text style={styles.navText}>{'\u203A'}</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.weekdaysRow}>
        {WEEKDAYS.map((day, index) => (
          <View key={index} style={styles.weekdayCell}>
            <Text style={styles.weekdayText}>{day}</Text>
          </View>
        ))}
      </View>

      <View style={styles.daysGrid}>
        {calendarDays.map((day, index) => {
          if (!day) {
            return <View key={`empty-${index}`} style={styles.dayCell} />;
          }

          const completed = isCompleted(day);
          const today = isToday(day);

          return (
            <TouchableOpacity
              key={formatDate(day)}
              style={[
                styles.dayCell,
                completed && styles.completedDay,
                today && styles.todayDay,
              ]}
              onPress={() => handleDayPress(day)}
              activeOpacity={0.7}>
              <Text
                style={[
                  styles.dayText,
                  completed && styles.completedDayText,
                  today && styles.todayDayText,
                ]}>
                {format(day, 'd')}
              </Text>
            </TouchableOpacity>
          );
        })}
      </View>

      <View style={styles.legend}>
        <View style={styles.legendItem}>
          <View style={[styles.legendDot, styles.completedDot]} />
          <Text style={styles.legendText}>Completed</Text>
        </View>
        <View style={styles.legendItem}>
          <View style={[styles.legendDot, styles.todayDot]} />
          <Text style={styles.legendText}>Today</Text>
        </View>
      </View>
    </Card>
  );
}

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
  navButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#F8FAFC',
    alignItems: 'center',
    justifyContent: 'center',
  },
  navText: {
    fontSize: 24,
    color: COLORS.text,
    fontWeight: '300',
  },
  monthTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
  },
  weekdaysRow: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  weekdayCell: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: 8,
  },
  weekdayText: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.textSecondary,
  },
  daysGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  dayCell: {
    width: `${100 / 7}%`,
    aspectRatio: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 4,
  },
  dayText: {
    fontSize: 14,
    color: COLORS.text,
    fontWeight: '500',
  },
  completedDay: {
    backgroundColor: COLORS.completed,
    borderRadius: 20,
    margin: 2,
  },
  completedDayText: {
    color: '#FFFFFF',
    fontWeight: '600',
  },
  todayDay: {
    borderWidth: 2,
    borderColor: COLORS.primary,
    borderRadius: 20,
    margin: 2,
  },
  todayDayText: {
    color: COLORS.primary,
    fontWeight: '700',
  },
  legend: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 16,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginHorizontal: 12,
  },
  legendDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 6,
  },
  completedDot: {
    backgroundColor: COLORS.completed,
  },
  todayDot: {
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: COLORS.primary,
  },
  legendText: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
});
