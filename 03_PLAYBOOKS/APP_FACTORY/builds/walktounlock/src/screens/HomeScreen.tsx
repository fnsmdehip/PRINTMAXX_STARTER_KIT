import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  StyleSheet,
  Text,
  SafeAreaView,
  ScrollView,
  RefreshControl,
} from 'react-native';
import { COLORS, SPACING, BORDER_RADIUS } from '../constants/theme';
import { StatCard, ProgressBar, AchievementCard, Button } from '../components';
import { useApp } from '../context/AppContext';
import { getTodayStepCount, formatStepCount, calculateCaloriesBurned, calculateDistanceWalked } from '../utils/pedometer';
import achievementsData from '../data/achievements.json';
import type { BottomTabNavigationProp } from '@react-navigation/bottom-tabs';
import type { MainTabParamList, UserStats, Achievement } from '../constants/types';

interface HomeScreenProps {
  navigation: BottomTabNavigationProp<MainTabParamList, 'Home'>;
}

export const HomeScreen: React.FC<HomeScreenProps> = ({ navigation }) => {
  const { stats, settings, refreshData } = useApp();
  const [todaySteps, setTodaySteps] = useState(0);
  const [refreshing, setRefreshing] = useState(false);

  const loadSteps = useCallback(async () => {
    const steps = await getTodayStepCount();
    setTodaySteps(steps);
  }, []);

  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    await Promise.all([loadSteps(), refreshData()]);
    setRefreshing(false);
  }, [loadSteps, refreshData]);

  useEffect(() => {
    loadSteps();

    const unsubscribe = navigation.addListener('focus', () => {
      loadSteps();
      refreshData();
    });

    return unsubscribe;
  }, [loadSteps, navigation, refreshData]);

  const goalSteps = settings.stepGoal;
  const progress = goalSteps > 0 ? todaySteps / goalSteps : 0;
  const calories = calculateCaloriesBurned(todaySteps);
  const distance = calculateDistanceWalked(todaySteps);

  const recentAchievements = (achievementsData.achievements as Achievement[])
    .filter((a) => stats.achievements.includes(a.id))
    .slice(0, 3);

  const nextAchievement = (achievementsData.achievements as Achievement[]).find(
    (a) => !stats.achievements.includes(a.id)
  );

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
        <View style={styles.header}>
          <Text style={styles.greeting}>Welcome back!</Text>
          <Text style={styles.appName}>WalkToUnlock</Text>
        </View>

        <View style={styles.todayCard}>
          <View style={styles.todayHeader}>
            <Text style={styles.todayTitle}>Today's Progress</Text>
            <Text style={styles.todayDate}>
              {new Date().toLocaleDateString('en-US', {
                weekday: 'long',
                month: 'short',
                day: 'numeric',
              })}
            </Text>
          </View>

          <View style={styles.stepDisplay}>
            <Text style={styles.stepCount}>{formatStepCount(todaySteps)}</Text>
            <Text style={styles.stepLabel}>steps today</Text>
          </View>

          <ProgressBar
            progress={progress}
            height={16}
            showLabel
            label={`Goal: ${goalSteps.toLocaleString()} steps`}
          />

          <View style={styles.metricsRow}>
            <View style={styles.metric}>
              <Text style={styles.metricValue}>{calories}</Text>
              <Text style={styles.metricLabel}>calories</Text>
            </View>
            <View style={styles.metricDivider} />
            <View style={styles.metric}>
              <Text style={styles.metricValue}>{distance}</Text>
              <Text style={styles.metricLabel}>km</Text>
            </View>
            <View style={styles.metricDivider} />
            <View style={styles.metric}>
              <Text style={styles.metricValue}>
                {Math.min(Math.round(progress * 100), 100)}%
              </Text>
              <Text style={styles.metricLabel}>complete</Text>
            </View>
          </View>
        </View>

        <View style={styles.statsRow}>
          <StatCard
            title="Streak"
            value={stats.currentStreak || 0}
            subtitle="days"
            color={COLORS.warning}
          />
          <View style={{ width: SPACING.md }} />
          <StatCard
            title="Total"
            value={formatStepCount(stats.totalSteps || 0)}
            subtitle="steps"
            color={COLORS.primary}
          />
        </View>

        <View style={styles.statsRow}>
          <StatCard
            title="Best Streak"
            value={stats.longestStreak || 0}
            subtitle="days"
            color={COLORS.gold}
          />
          <View style={{ width: SPACING.md }} />
          <StatCard
            title="Days Active"
            value={stats.totalDaysActive || 0}
            subtitle="total"
            color={COLORS.primaryLight}
          />
        </View>

        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Achievements</Text>
            <Text style={styles.sectionCount}>
              {stats.achievements.length || 0}/{achievementsData.achievements.length}
            </Text>
          </View>

          {nextAchievement && (
            <View style={styles.nextAchievement}>
              <Text style={styles.nextLabel}>Next up</Text>
              <AchievementCard
                achievement={nextAchievement}
                unlocked={false}
                progress={getAchievementProgress(nextAchievement, stats, todaySteps)}
              />
            </View>
          )}

          {recentAchievements.length > 0 && (
            <View style={styles.recentAchievements}>
              <Text style={styles.recentLabel}>Recently Unlocked</Text>
              {recentAchievements.map((achievement) => (
                <AchievementCard
                  key={achievement.id}
                  achievement={achievement}
                  unlocked
                />
              ))}
            </View>
          )}

          <Button
            title="View All Achievements"
            variant="outline"
            fullWidth
            onPress={() => navigation.navigate('Stats')}
          />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

function getAchievementProgress(
  achievement: Achievement,
  stats: UserStats,
  todaySteps: number
): number {
  switch (achievement.type) {
    case 'steps':
      return (todaySteps / achievement.requirement) * 100;
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
  header: {
    marginBottom: SPACING.lg,
  },
  greeting: {
    fontSize: 16,
    color: COLORS.textSecondary,
  },
  appName: {
    fontSize: 32,
    fontWeight: '800',
    color: COLORS.primary,
    letterSpacing: -1,
  },
  todayCard: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.xl,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
  },
  todayHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  todayTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.text,
  },
  todayDate: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  stepDisplay: {
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  stepCount: {
    fontSize: 72,
    fontWeight: '800',
    color: COLORS.primary,
    letterSpacing: -3,
  },
  stepLabel: {
    fontSize: 16,
    color: COLORS.textSecondary,
    marginTop: -SPACING.xs,
  },
  metricsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: SPACING.lg,
    paddingTop: SPACING.md,
    borderTopWidth: 1,
    borderTopColor: COLORS.backgroundLighter,
  },
  metric: {
    alignItems: 'center',
    flex: 1,
  },
  metricValue: {
    fontSize: 20,
    fontWeight: '700',
    color: COLORS.text,
  },
  metricLabel: {
    fontSize: 12,
    color: COLORS.textMuted,
    marginTop: 2,
  },
  metricDivider: {
    width: 1,
    height: '100%',
    backgroundColor: COLORS.backgroundLighter,
  },
  statsRow: {
    flexDirection: 'row',
    marginBottom: SPACING.md,
  },
  section: {
    marginTop: SPACING.lg,
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
  sectionCount: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  nextAchievement: {
    marginBottom: SPACING.md,
  },
  nextLabel: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginBottom: SPACING.sm,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  recentAchievements: {
    marginBottom: SPACING.md,
  },
  recentLabel: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginBottom: SPACING.sm,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
});
