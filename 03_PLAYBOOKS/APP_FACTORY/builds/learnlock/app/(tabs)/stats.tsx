import React from 'react';
import { View, Text, StyleSheet, SafeAreaView, ScrollView } from 'react-native';
import { DailyStats } from '../../src/components/stats/DailyStats';
import { WeeklyChart } from '../../src/components/stats/WeeklyChart';
import { StreakBadge } from '../../src/components/common/StreakBadge';
import { useStreakStore } from '../../src/stores/streakStore';
import { useTimerStore } from '../../src/stores/timerStore';
import { COLORS, TYPOGRAPHY, SPACING } from '../../src/utils/constants';
import { formatDuration, formatDurationShort } from '../../src/utils/dateUtils';

export default function StatsScreen() {
  const {
    currentStreak,
    longestStreak,
    totalDaysStudied,
    totalStudyHours,
    getWeekData,
    getWeeklyAverage,
    getMonthlyTotal,
  } = useStreakStore();

  const { todayStudyTime, todaySessions } = useTimerStore();

  const weekData = getWeekData();
  const weeklyAverage = getWeeklyAverage();
  const monthlyTotal = getMonthlyTotal();
  const sessionsCompleted = todaySessions.filter((s) => s.completed).length;

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>Your Progress</Text>
          <StreakBadge streak={currentStreak} size="large" />
        </View>

        {/* Daily stats grid */}
        <DailyStats
          todayStudyTime={todayStudyTime}
          sessionsCompleted={sessionsCompleted}
          weeklyAverage={weeklyAverage}
          currentStreak={currentStreak}
        />

        {/* Weekly chart */}
        <View style={styles.chartSection}>
          <WeeklyChart weekData={weekData} goalMinutes={25} />
        </View>

        {/* Lifetime stats */}
        <View style={styles.lifetimeSection}>
          <Text style={styles.sectionTitle}>All Time</Text>

          <View style={styles.lifetimeGrid}>
            <LifetimeStat
              label="Total Study Time"
              value={formatDuration(Math.round(totalStudyHours * 3600))}
            />
            <LifetimeStat
              label="Days Studied"
              value={totalDaysStudied.toString()}
            />
            <LifetimeStat
              label="Longest Streak"
              value={`${longestStreak} days`}
            />
            <LifetimeStat
              label="This Month"
              value={formatDurationShort(monthlyTotal)}
            />
          </View>
        </View>

        {/* Achievements preview */}
        <View style={styles.achievementsSection}>
          <Text style={styles.sectionTitle}>Milestones</Text>
          <View style={styles.milestones}>
            <MilestoneItem
              icon="🎯"
              title="First Session"
              completed={todaySessions.length > 0}
            />
            <MilestoneItem
              icon="🔥"
              title="7-Day Streak"
              completed={longestStreak >= 7}
            />
            <MilestoneItem
              icon="📚"
              title="10 Hours Total"
              completed={totalStudyHours >= 10}
            />
            <MilestoneItem
              icon="🏆"
              title="30-Day Streak"
              completed={longestStreak >= 30}
            />
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

interface LifetimeStatProps {
  label: string;
  value: string;
}

function LifetimeStat({ label, value }: LifetimeStatProps) {
  return (
    <View style={styles.lifetimeStat}>
      <Text style={styles.lifetimeValue}>{value}</Text>
      <Text style={styles.lifetimeLabel}>{label}</Text>
    </View>
  );
}

interface MilestoneItemProps {
  icon: string;
  title: string;
  completed: boolean;
}

function MilestoneItem({ icon, title, completed }: MilestoneItemProps) {
  return (
    <View style={[styles.milestone, completed && styles.milestoneCompleted]}>
      <Text style={styles.milestoneIcon}>{completed ? icon : '🔒'}</Text>
      <Text
        style={[
          styles.milestoneTitle,
          completed && styles.milestoneTitleCompleted,
        ]}
      >
        {title}
      </Text>
      {completed && <Text style={styles.milestoneCheck}>✓</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: SPACING.lg,
    paddingBottom: SPACING.xxl,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.xl,
  },
  title: {
    ...TYPOGRAPHY.h1,
    color: COLORS.text,
  },
  chartSection: {
    marginTop: SPACING.xl,
  },
  lifetimeSection: {
    marginTop: SPACING.xl,
  },
  sectionTitle: {
    ...TYPOGRAPHY.h3,
    color: COLORS.text,
    marginBottom: SPACING.md,
  },
  lifetimeGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: SPACING.md,
  },
  lifetimeStat: {
    flex: 1,
    minWidth: '45%',
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: SPACING.md,
    alignItems: 'center',
  },
  lifetimeValue: {
    ...TYPOGRAPHY.h2,
    color: COLORS.primary,
  },
  lifetimeLabel: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textSecondary,
    marginTop: SPACING.xs,
  },
  achievementsSection: {
    marginTop: SPACING.xl,
  },
  milestones: {
    gap: SPACING.sm,
  },
  milestone: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: SPACING.md,
    opacity: 0.5,
  },
  milestoneCompleted: {
    opacity: 1,
    backgroundColor: COLORS.secondary + '10',
  },
  milestoneIcon: {
    fontSize: 24,
    marginRight: SPACING.md,
    width: 32,
    textAlign: 'center',
  },
  milestoneTitle: {
    ...TYPOGRAPHY.body,
    color: COLORS.textSecondary,
    flex: 1,
  },
  milestoneTitleCompleted: {
    color: COLORS.text,
    fontWeight: '500',
  },
  milestoneCheck: {
    ...TYPOGRAPHY.body,
    color: COLORS.secondary,
    fontWeight: '600',
  },
});
