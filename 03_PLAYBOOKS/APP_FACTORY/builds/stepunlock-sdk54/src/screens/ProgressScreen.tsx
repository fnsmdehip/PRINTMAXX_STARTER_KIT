import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
} from 'react-native';
import { COLORS } from '../utils/constants';
import { StreakBadge } from '../components/StreakBadge';
import { CalendarView } from '../components/CalendarView';
import { useUserStore } from '../stores/userStore';
import { useStepStore } from '../stores/stepStore';
import { getWeeklyCompletionRate } from '../services/streakService';

export function ProgressScreen() {
  const { streak } = useUserStore();
  const { getWeeklyAverage, getMonthlyTotal } = useStepStore();

  const weeklyAverage = getWeeklyAverage();
  const monthlyTotal = getMonthlyTotal();
  const weeklyCompletion = getWeeklyCompletionRate(streak);

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Streak Section */}
        <StreakBadge streak={streak} />

        {/* Stats Grid */}
        <View style={styles.statsGrid}>
          <View style={styles.statCard}>
            <Text style={styles.statValue}>
              {weeklyAverage.toLocaleString()}
            </Text>
            <Text style={styles.statLabel}>Weekly avg</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statValue}>
              {monthlyTotal.toLocaleString()}
            </Text>
            <Text style={styles.statLabel}>Monthly total</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statValue}>{weeklyCompletion}%</Text>
            <Text style={styles.statLabel}>This week</Text>
          </View>
        </View>

        {/* Calendar */}
        <CalendarView streak={streak} />

        {/* Milestones */}
        <View style={styles.milestonesCard}>
          <Text style={styles.milestonesTitle}>Milestones</Text>
          <View style={styles.milestonesList}>
            <MilestoneItem
              title="First goal"
              achieved={streak.totalDaysCompleted >= 1}
            />
            <MilestoneItem
              title="3-day streak"
              achieved={streak.longestStreak >= 3}
            />
            <MilestoneItem
              title="7-day streak"
              achieved={streak.longestStreak >= 7}
            />
            <MilestoneItem
              title="14-day streak"
              achieved={streak.longestStreak >= 14}
            />
            <MilestoneItem
              title="30-day streak"
              achieved={streak.longestStreak >= 30}
            />
            <MilestoneItem
              title="100 total days"
              achieved={streak.totalDaysCompleted >= 100}
            />
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

function MilestoneItem({
  title,
  achieved,
}: {
  title: string;
  achieved: boolean;
}) {
  return (
    <View style={styles.milestoneItem}>
      <View
        style={[
          styles.milestoneCheck,
          achieved && styles.milestoneCheckAchieved,
        ]}
      >
        {achieved && <Text style={styles.milestoneCheckmark}>✓</Text>}
      </View>
      <Text
        style={[
          styles.milestoneText,
          achieved && styles.milestoneTextAchieved,
        ]}
      >
        {title}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scrollContent: {
    padding: 20,
  },
  statsGrid: {
    flexDirection: 'row',
    marginVertical: 16,
    gap: 12,
  },
  statCard: {
    flex: 1,
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  statLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  milestonesCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 20,
    marginTop: 16,
  },
  milestonesTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 16,
  },
  milestonesList: {},
  milestoneItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  milestoneCheck: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: COLORS.border,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  milestoneCheckAchieved: {
    backgroundColor: COLORS.success,
    borderColor: COLORS.success,
  },
  milestoneCheckmark: {
    color: COLORS.surface,
    fontWeight: 'bold',
    fontSize: 14,
  },
  milestoneText: {
    fontSize: 16,
    color: COLORS.textSecondary,
  },
  milestoneTextAchieved: {
    color: COLORS.text,
    fontWeight: '500',
  },
});
