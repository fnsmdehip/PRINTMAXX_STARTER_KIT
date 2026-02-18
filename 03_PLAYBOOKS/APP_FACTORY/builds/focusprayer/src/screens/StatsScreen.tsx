/**
 * Stats Screen
 * Streak statistics and calendar view
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { useDevotionStore } from '../stores/devotionStore';
import {
  getStreakMessage,
  getNextMilestone,
  getDaysToMilestone,
  generateCalendarMonth,
} from '../services/streakService';
import { COLORS } from '../utils/constants';

export default function StatsScreen() {
  const { streak } = useDevotionStore();
  const [selectedMonth, setSelectedMonth] = useState(() => {
    const now = new Date();
    return { year: now.getFullYear(), month: now.getMonth() };
  });

  const calendarDays = generateCalendarMonth(
    selectedMonth.year,
    selectedMonth.month,
    streak.completedDates
  );

  // Get day names
  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  // Calculate first day offset
  const firstDay = new Date(selectedMonth.year, selectedMonth.month, 1).getDay();

  function changeMonth(delta: number) {
    setSelectedMonth((prev) => {
      let newMonth = prev.month + delta;
      let newYear = prev.year;

      if (newMonth < 0) {
        newMonth = 11;
        newYear--;
      } else if (newMonth > 11) {
        newMonth = 0;
        newYear++;
      }

      return { year: newYear, month: newMonth };
    });
  }

  const monthNames = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
  ];

  const nextMilestone = getNextMilestone(streak.currentStreak);
  const daysToMilestone = getDaysToMilestone(streak.currentStreak);

  // Calculate completion rate for current month
  const completedThisMonth = calendarDays.filter(
    (day) => day.completed && day.isPast
  ).length;
  const pastDaysThisMonth = calendarDays.filter((day) => day.isPast).length;
  const completionRate =
    pastDaysThisMonth > 0
      ? Math.round((completedThisMonth / pastDaysThisMonth) * 100)
      : 0;

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Current Streak Card */}
      <View style={styles.streakCard}>
        <Text style={styles.streakNumber}>{streak.currentStreak}</Text>
        <Text style={styles.streakLabel}>Current Streak</Text>
        <Text style={styles.streakMessage}>{getStreakMessage(streak)}</Text>

        {/* Milestone Progress */}
        {streak.currentStreak > 0 && (
          <View style={styles.milestoneContainer}>
            <View style={styles.milestoneBar}>
              <View
                style={[
                  styles.milestoneProgress,
                  {
                    width: `${((streak.currentStreak / nextMilestone) * 100)}%`,
                  },
                ]}
              />
            </View>
            <Text style={styles.milestoneText}>
              {daysToMilestone} day{daysToMilestone !== 1 ? 's' : ''} to{' '}
              {nextMilestone}-day milestone
            </Text>
          </View>
        )}
      </View>

      {/* Stats Grid */}
      <View style={styles.statsGrid}>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>{streak.longestStreak}</Text>
          <Text style={styles.statLabel}>Best Streak</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>{streak.totalDaysCompleted}</Text>
          <Text style={styles.statLabel}>Total Days</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>{completionRate}%</Text>
          <Text style={styles.statLabel}>This Month</Text>
        </View>
      </View>

      {/* Calendar */}
      <View style={styles.calendarContainer}>
        {/* Month Navigation */}
        <View style={styles.calendarHeader}>
          <TouchableOpacity
            onPress={() => changeMonth(-1)}
            style={styles.monthButton}
          >
            <Text style={styles.monthButtonText}>&#8249;</Text>
          </TouchableOpacity>
          <Text style={styles.monthTitle}>
            {monthNames[selectedMonth.month]} {selectedMonth.year}
          </Text>
          <TouchableOpacity
            onPress={() => changeMonth(1)}
            style={styles.monthButton}
          >
            <Text style={styles.monthButtonText}>&#8250;</Text>
          </TouchableOpacity>
        </View>

        {/* Day Names */}
        <View style={styles.dayNamesRow}>
          {dayNames.map((name) => (
            <View key={name} style={styles.dayNameCell}>
              <Text style={styles.dayNameText}>{name}</Text>
            </View>
          ))}
        </View>

        {/* Calendar Grid */}
        <View style={styles.calendarGrid}>
          {/* Empty cells for first week offset */}
          {Array.from({ length: firstDay }).map((_, i) => (
            <View key={`empty-${i}`} style={styles.dayCell} />
          ))}

          {/* Day cells */}
          {calendarDays.map((day) => (
            <View
              key={day.date}
              style={[
                styles.dayCell,
                day.isToday && styles.todayCell,
                day.completed && styles.completedCell,
              ]}
            >
              <Text
                style={[
                  styles.dayText,
                  day.isToday && styles.todayText,
                  day.completed && styles.completedText,
                  !day.isPast && !day.isToday && styles.futureText,
                ]}
              >
                {new Date(day.date).getDate()}
              </Text>
            </View>
          ))}
        </View>

        {/* Legend */}
        <View style={styles.legend}>
          <View style={styles.legendItem}>
            <View style={[styles.legendDot, { backgroundColor: COLORS.success }]} />
            <Text style={styles.legendText}>Completed</Text>
          </View>
          <View style={styles.legendItem}>
            <View
              style={[
                styles.legendDot,
                { backgroundColor: COLORS.primary, borderWidth: 2, borderColor: COLORS.primary },
              ]}
            />
            <Text style={styles.legendText}>Today</Text>
          </View>
        </View>
      </View>

      {/* Insights */}
      {streak.totalDaysCompleted > 7 && (
        <View style={styles.insightsCard}>
          <Text style={styles.insightsTitle}>Your Prayer Journey</Text>
          <Text style={styles.insightText}>
            You have prayed for {streak.totalDaysCompleted} day
            {streak.totalDaysCompleted !== 1 ? 's' : ''} since starting PrayerLock.
          </Text>
          {streak.longestStreak >= 7 && (
            <Text style={styles.insightText}>
              Your best streak of {streak.longestStreak} days shows real commitment.
            </Text>
          )}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  content: {
    padding: 20,
    paddingBottom: 40,
  },
  streakCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 24,
    alignItems: 'center',
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  streakNumber: {
    fontSize: 72,
    fontWeight: '800',
    color: COLORS.streak,
  },
  streakLabel: {
    fontSize: 18,
    color: COLORS.textSecondary,
    marginTop: -8,
  },
  streakMessage: {
    fontSize: 16,
    color: COLORS.text,
    textAlign: 'center',
    marginTop: 12,
  },
  milestoneContainer: {
    width: '100%',
    marginTop: 20,
  },
  milestoneBar: {
    height: 8,
    backgroundColor: COLORS.background,
    borderRadius: 4,
    overflow: 'hidden',
  },
  milestoneProgress: {
    height: '100%',
    backgroundColor: COLORS.primary,
    borderRadius: 4,
  },
  milestoneText: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginTop: 8,
  },
  statsGrid: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 20,
  },
  statCard: {
    flex: 1,
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
  },
  statLabel: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  calendarContainer: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
  },
  calendarHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  monthButton: {
    padding: 8,
  },
  monthButtonText: {
    fontSize: 24,
    color: COLORS.primary,
    fontWeight: '600',
  },
  monthTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
  },
  dayNamesRow: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  dayNameCell: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: 4,
  },
  dayNameText: {
    fontSize: 12,
    color: COLORS.textSecondary,
    fontWeight: '500',
  },
  calendarGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  dayCell: {
    width: '14.28%',
    aspectRatio: 1,
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 8,
  },
  todayCell: {
    borderWidth: 2,
    borderColor: COLORS.primary,
  },
  completedCell: {
    backgroundColor: COLORS.success,
  },
  dayText: {
    fontSize: 14,
    color: COLORS.text,
  },
  todayText: {
    fontWeight: '700',
    color: COLORS.primary,
  },
  completedText: {
    color: COLORS.surface,
    fontWeight: '600',
  },
  futureText: {
    color: COLORS.disabled,
  },
  legend: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 24,
    marginTop: 16,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  legendDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
  },
  legendText: {
    fontSize: 13,
    color: COLORS.textSecondary,
  },
  insightsCard: {
    backgroundColor: COLORS.primary + '10',
    borderRadius: 12,
    padding: 20,
  },
  insightsTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 12,
  },
  insightText: {
    fontSize: 15,
    color: COLORS.textSecondary,
    marginBottom: 8,
    lineHeight: 22,
  },
});
