import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  StyleSheet,
  Text,
  SafeAreaView,
  ScrollView,
  RefreshControl,
  Pressable,
} from 'react-native';
import { COLORS, SPACING, BORDER_RADIUS } from '../constants/theme';
import { StepHistoryChart, AchievementCard, StatCard } from '../components';
import { getUserStats, getSettings } from '../utils/storage';
import { formatStepCount } from '../utils/pedometer';
import achievementsData from '../data/achievements.json';
import type { BottomTabNavigationProp } from '@react-navigation/bottom-tabs';
import type { MainTabParamList, UserStats, Achievement, DailySteps } from '../constants/types';

interface StatsScreenProps {
  navigation: BottomTabNavigationProp<MainTabParamList, 'Stats'>;
}

type ChartPeriod = 'week' | 'month';
type AchievementFilter = 'all' | 'unlocked' | 'locked';

export const StatsScreen: React.FC<StatsScreenProps> = ({ navigation }) => {
  const [stats, setStats] = useState<UserStats | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [chartPeriod, setChartPeriod] = useState<ChartPeriod>('week');
  const [achievementFilter, setAchievementFilter] = useState<AchievementFilter>('all');

  const loadData = useCallback(async () => {
    const userStats = await getUserStats();
    setStats(userStats);
  }, []);

  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    await loadData();
    setRefreshing(false);
  }, [loadData]);

  useEffect(() => {
    loadData();

    const unsubscribe = navigation.addListener('focus', () => {
      loadData();
    });

    return unsubscribe;
  }, [loadData, navigation]);

  const weeklyTotal = stats?.weeklySteps.reduce((sum, d) => sum + d.steps, 0) || 0;
  const weeklyAverage = stats?.weeklySteps.length
    ? Math.round(weeklyTotal / stats.weeklySteps.length)
    : 0;
  const goalsMetThisWeek = stats?.weeklySteps.filter((d) => d.goalMet).length || 0;

  const allAchievements = achievementsData.achievements as Achievement[];
  const filteredAchievements = allAchievements.filter((a) => {
    const isUnlocked = stats?.achievements.includes(a.id);
    if (achievementFilter === 'unlocked') return isUnlocked;
    if (achievementFilter === 'locked') return !isUnlocked;
    return true;
  });

  const chartData: DailySteps[] =
    chartPeriod === 'week'
      ? stats?.weeklySteps || generateEmptyData(7)
      : stats?.monthlySteps || generateEmptyData(30);

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor={COLORS.primary}
          />
        }
      >
        <Text style={styles.title}>Statistics</Text>

        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Step History</Text>
            <View style={styles.periodToggle}>
              <Pressable
                style={[
                  styles.periodButton,
                  chartPeriod === 'week' && styles.periodButtonActive,
                ]}
                onPress={() => setChartPeriod('week')}
              >
                <Text
                  style={[
                    styles.periodButtonText,
                    chartPeriod === 'week' && styles.periodButtonTextActive,
                  ]}
                >
                  Week
                </Text>
              </Pressable>
              <Pressable
                style={[
                  styles.periodButton,
                  chartPeriod === 'month' && styles.periodButtonActive,
                ]}
                onPress={() => setChartPeriod('month')}
              >
                <Text
                  style={[
                    styles.periodButtonText,
                    chartPeriod === 'month' && styles.periodButtonTextActive,
                  ]}
                >
                  Month
                </Text>
              </Pressable>
            </View>
          </View>

          <StepHistoryChart data={chartData} period={chartPeriod} />
        </View>

        <View style={styles.statsGrid}>
          <StatCard
            title="This Week"
            value={formatStepCount(weeklyTotal)}
            subtitle="total steps"
            color={COLORS.primary}
          />
          <View style={{ width: SPACING.md }} />
          <StatCard
            title="Daily Avg"
            value={formatStepCount(weeklyAverage)}
            subtitle="steps/day"
            color={COLORS.primaryLight}
          />
        </View>

        <View style={styles.statsGrid}>
          <StatCard
            title="Goals Met"
            value={`${goalsMetThisWeek}/7`}
            subtitle="this week"
            color={COLORS.success}
          />
          <View style={{ width: SPACING.md }} />
          <StatCard
            title="Best Day"
            value={formatStepCount(stats?.personalRecords.mostStepsInDay || 0)}
            subtitle="personal record"
            color={COLORS.gold}
          />
        </View>

        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Personal Records</Text>
          </View>

          <View style={styles.recordsCard}>
            <View style={styles.recordRow}>
              <Text style={styles.recordLabel}>Most steps in a day</Text>
              <Text style={styles.recordValue}>
                {formatStepCount(stats?.personalRecords.mostStepsInDay || 0)}
              </Text>
            </View>
            <View style={styles.recordDivider} />
            <View style={styles.recordRow}>
              <Text style={styles.recordLabel}>Most steps in a week</Text>
              <Text style={styles.recordValue}>
                {formatStepCount(stats?.personalRecords.mostStepsInWeek || 0)}
              </Text>
            </View>
            <View style={styles.recordDivider} />
            <View style={styles.recordRow}>
              <Text style={styles.recordLabel}>Longest streak</Text>
              <Text style={styles.recordValue}>
                {stats?.personalRecords.longestStreak || 0} days
              </Text>
            </View>
          </View>
        </View>

        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Achievements</Text>
            <Text style={styles.achievementCount}>
              {stats?.achievements.length || 0}/{allAchievements.length}
            </Text>
          </View>

          <View style={styles.filterRow}>
            {(['all', 'unlocked', 'locked'] as const).map((filter) => (
              <Pressable
                key={filter}
                style={[
                  styles.filterButton,
                  achievementFilter === filter && styles.filterButtonActive,
                ]}
                onPress={() => setAchievementFilter(filter)}
              >
                <Text
                  style={[
                    styles.filterButtonText,
                    achievementFilter === filter && styles.filterButtonTextActive,
                  ]}
                >
                  {filter.charAt(0).toUpperCase() + filter.slice(1)}
                </Text>
              </Pressable>
            ))}
          </View>

          {filteredAchievements.map((achievement) => (
            <AchievementCard
              key={achievement.id}
              achievement={achievement}
              unlocked={stats?.achievements.includes(achievement.id) || false}
              progress={getAchievementProgress(achievement, stats)}
            />
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

function generateEmptyData(days: number): DailySteps[] {
  const data: DailySteps[] = [];
  for (let i = 0; i < days; i++) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    data.push({
      date: date.toISOString().split('T')[0],
      steps: 0,
      goalMet: false,
      goal: 500,
    });
  }
  return data;
}

function getAchievementProgress(achievement: Achievement, stats: UserStats | null): number {
  if (!stats) return 0;

  switch (achievement.type) {
    case 'steps':
      const maxDailySteps = Math.max(
        ...stats.weeklySteps.map((d) => d.steps),
        0
      );
      return (maxDailySteps / achievement.requirement) * 100;
    case 'streak':
      return (stats.currentStreak / achievement.requirement) * 100;
    case 'total':
      return (stats.totalSteps / achievement.requirement) * 100;
    case 'unlock':
      return (stats.totalDaysActive / achievement.requirement) * 100;
    default:
      return 0;
  }
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
  title: {
    fontSize: 32,
    fontWeight: '800',
    color: COLORS.text,
    letterSpacing: -1,
    marginBottom: SPACING.lg,
  },
  section: {
    marginBottom: SPACING.lg,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: COLORS.text,
  },
  periodToggle: {
    flexDirection: 'row',
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.md,
    padding: 2,
  },
  periodButton: {
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.xs,
    borderRadius: BORDER_RADIUS.sm,
  },
  periodButtonActive: {
    backgroundColor: COLORS.primary,
  },
  periodButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.textSecondary,
  },
  periodButtonTextActive: {
    color: COLORS.background,
  },
  statsGrid: {
    flexDirection: 'row',
    marginBottom: SPACING.md,
  },
  recordsCard: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.lg,
  },
  recordRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  recordLabel: {
    fontSize: 15,
    color: COLORS.textSecondary,
  },
  recordValue: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.primary,
  },
  recordDivider: {
    height: 1,
    backgroundColor: COLORS.backgroundLighter,
    marginVertical: SPACING.md,
  },
  achievementCount: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  filterRow: {
    flexDirection: 'row',
    marginBottom: SPACING.md,
  },
  filterButton: {
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    borderRadius: BORDER_RADIUS.full,
    marginRight: SPACING.sm,
    backgroundColor: COLORS.surface,
  },
  filterButtonActive: {
    backgroundColor: COLORS.primary,
  },
  filterButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.textSecondary,
  },
  filterButtonTextActive: {
    color: COLORS.background,
  },
});
