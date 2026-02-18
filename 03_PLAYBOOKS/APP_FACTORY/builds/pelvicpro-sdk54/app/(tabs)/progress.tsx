import { useState, useMemo } from 'react';
import { View, Text, StyleSheet, ScrollView, Pressable, Dimensions } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { format, parseISO, subDays, isAfter } from 'date-fns';
import {
  colors,
  spacing,
  borderRadius,
  typography,
  shadows,
} from '@/constants/theme';
import { useWorkoutStore } from '@/store/workoutStore';
import { useUserStore } from '@/store/userStore';
import { exercises } from '@/constants/exercises';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

type TimeRange = '7d' | '30d' | '90d' | 'all';

export default function ProgressScreen() {
  const [timeRange, setTimeRange] = useState<TimeRange>('30d');
  const { workoutHistory, personalRecords } = useWorkoutStore();
  const { totalWorkouts, totalPRs, currentStreak, longestStreak } = useUserStore();

  const filteredWorkouts = useMemo(() => {
    if (timeRange === 'all') return workoutHistory;

    const daysMap: Record<TimeRange, number> = {
      '7d': 7,
      '30d': 30,
      '90d': 90,
      all: 9999,
    };

    const cutoffDate = subDays(new Date(), daysMap[timeRange]);
    return workoutHistory.filter((w) =>
      isAfter(parseISO(w.date), cutoffDate)
    );
  }, [workoutHistory, timeRange]);

  // Calculate stats
  const totalVolume = useMemo(() => {
    let volume = 0;
    filteredWorkouts.forEach((workout) => {
      workout.exercises.forEach((ex) => {
        ex.sets.forEach((set) => {
          if (set.completed) {
            volume += set.weight * set.reps;
          }
        });
      });
    });
    return volume;
  }, [filteredWorkouts]);

  const avgWorkoutDuration = useMemo(() => {
    if (filteredWorkouts.length === 0) return 0;
    const total = filteredWorkouts.reduce((acc, w) => acc + w.duration, 0);
    return Math.round(total / filteredWorkouts.length);
  }, [filteredWorkouts]);

  // Get top exercises by volume
  const topExercises = useMemo(() => {
    const exerciseVolumes: Record<string, number> = {};

    filteredWorkouts.forEach((workout) => {
      workout.exercises.forEach((ex) => {
        if (!exerciseVolumes[ex.exerciseId]) {
          exerciseVolumes[ex.exerciseId] = 0;
        }
        ex.sets.forEach((set) => {
          if (set.completed) {
            exerciseVolumes[ex.exerciseId] += set.weight * set.reps;
          }
        });
      });
    });

    return Object.entries(exerciseVolumes)
      .map(([id, volume]) => ({
        id,
        name: exercises.find((e) => e.id === id)?.name || 'Unknown',
        volume,
      }))
      .sort((a, b) => b.volume - a.volume)
      .slice(0, 5);
  }, [filteredWorkouts]);

  // Weekly activity chart data
  const weeklyActivity = useMemo(() => {
    const days = Array.from({ length: 7 }, (_, i) => {
      const date = subDays(new Date(), 6 - i);
      const workoutsOnDay = workoutHistory.filter(
        (w) => format(parseISO(w.date), 'yyyy-MM-dd') === format(date, 'yyyy-MM-dd')
      ).length;
      return {
        day: format(date, 'EEE'),
        count: workoutsOnDay,
      };
    });
    return days;
  }, [workoutHistory]);

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <Text style={styles.title}>Progress</Text>
      </View>

      {/* Time Range Selector */}
      <View style={styles.timeRangeContainer}>
        {(['7d', '30d', '90d', 'all'] as TimeRange[]).map((range) => (
          <Pressable
            key={range}
            style={[
              styles.timeRangePill,
              timeRange === range && styles.timeRangePillActive,
            ]}
            onPress={() => setTimeRange(range)}
          >
            <Text
              style={[
                styles.timeRangeText,
                timeRange === range && styles.timeRangeTextActive,
              ]}
            >
              {range === 'all' ? 'All' : range.toUpperCase()}
            </Text>
          </Pressable>
        ))}
      </View>

      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Overview Stats */}
        <View style={styles.statsGrid}>
          <View style={styles.statCard}>
            <Ionicons name="barbell" size={24} color={colors.primary} />
            <Text style={styles.statValue}>{filteredWorkouts.length}</Text>
            <Text style={styles.statLabel}>Workouts</Text>
          </View>
          <View style={styles.statCard}>
            <Ionicons name="trending-up" size={24} color={colors.accent} />
            <Text style={styles.statValue}>
              {totalVolume >= 1000
                ? `${(totalVolume / 1000).toFixed(1)}k`
                : totalVolume}
            </Text>
            <Text style={styles.statLabel}>Total Volume (lbs)</Text>
          </View>
          <View style={styles.statCard}>
            <Ionicons name="time" size={24} color={colors.secondary} />
            <Text style={styles.statValue}>{avgWorkoutDuration}</Text>
            <Text style={styles.statLabel}>Avg Duration (min)</Text>
          </View>
          <View style={styles.statCard}>
            <Ionicons name="trophy" size={24} color={colors.warning} />
            <Text style={styles.statValue}>{Object.keys(personalRecords).length}</Text>
            <Text style={styles.statLabel}>Personal Records</Text>
          </View>
        </View>

        {/* Streak Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Streaks</Text>
          <View style={styles.streakContainer}>
            <View style={styles.streakBox}>
              <Ionicons name="flame" size={32} color={colors.primary} />
              <Text style={styles.streakValue}>{currentStreak}</Text>
              <Text style={styles.streakLabel}>Current Streak</Text>
            </View>
            <View style={styles.streakDivider} />
            <View style={styles.streakBox}>
              <Ionicons name="star" size={32} color={colors.warning} />
              <Text style={styles.streakValue}>{longestStreak}</Text>
              <Text style={styles.streakLabel}>Longest Streak</Text>
            </View>
          </View>
        </View>

        {/* Weekly Activity */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>This Week</Text>
          <View style={styles.activityChart}>
            {weeklyActivity.map((day, index) => (
              <View key={index} style={styles.activityDay}>
                <View
                  style={[
                    styles.activityBar,
                    {
                      height: day.count > 0 ? 40 + day.count * 20 : 8,
                      backgroundColor:
                        day.count > 0 ? colors.primary : colors.border,
                    },
                  ]}
                />
                <Text style={styles.activityDayLabel}>{day.day}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* Top Exercises */}
        {topExercises.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Top Exercises</Text>
            {topExercises.map((exercise, index) => (
              <View key={exercise.id} style={styles.topExerciseRow}>
                <Text style={styles.topExerciseRank}>#{index + 1}</Text>
                <Text style={styles.topExerciseName}>{exercise.name}</Text>
                <Text style={styles.topExerciseVolume}>
                  {exercise.volume.toLocaleString()} lbs
                </Text>
              </View>
            ))}
          </View>
        )}

        {/* Personal Records List */}
        {Object.keys(personalRecords).length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Recent PRs</Text>
            {Object.values(personalRecords)
              .sort(
                (a, b) =>
                  new Date(b.date).getTime() - new Date(a.date).getTime()
              )
              .slice(0, 5)
              .map((pr) => {
                const exercise = exercises.find((e) => e.id === pr.exerciseId);
                return (
                  <View key={pr.exerciseId} style={styles.prRow}>
                    <Ionicons name="trophy" size={20} color={colors.warning} />
                    <View style={styles.prInfo}>
                      <Text style={styles.prExercise}>
                        {exercise?.name || 'Unknown'}
                      </Text>
                      <Text style={styles.prDate}>
                        {format(parseISO(pr.date), 'MMM d, yyyy')}
                      </Text>
                    </View>
                    <Text style={styles.prValue}>
                      {pr.weight} lbs x {pr.reps}
                    </Text>
                  </View>
                );
              })}
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
  },
  title: {
    ...typography.h1,
    color: colors.text,
  },
  timeRangeContainer: {
    flexDirection: 'row',
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.sm,
    gap: spacing.sm,
  },
  timeRangePill: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: borderRadius.full,
    backgroundColor: colors.surface,
  },
  timeRangePillActive: {
    backgroundColor: colors.primary,
  },
  timeRangeText: {
    ...typography.caption,
    color: colors.textLight,
    fontWeight: '600',
  },
  timeRangeTextActive: {
    color: colors.surface,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: spacing.lg,
    paddingBottom: spacing.xxl,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
    marginBottom: spacing.xl,
  },
  statCard: {
    width: (SCREEN_WIDTH - spacing.lg * 2 - spacing.sm) / 2,
    backgroundColor: colors.surface,
    padding: spacing.md,
    borderRadius: borderRadius.md,
    alignItems: 'center',
    ...shadows.sm,
  },
  statValue: {
    ...typography.h2,
    color: colors.text,
    marginTop: spacing.sm,
  },
  statLabel: {
    ...typography.small,
    color: colors.textMuted,
    textAlign: 'center',
  },
  section: {
    marginBottom: spacing.xl,
  },
  sectionTitle: {
    ...typography.h3,
    color: colors.text,
    marginBottom: spacing.md,
  },
  streakContainer: {
    flexDirection: 'row',
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    ...shadows.sm,
  },
  streakBox: {
    flex: 1,
    alignItems: 'center',
  },
  streakDivider: {
    width: 1,
    backgroundColor: colors.border,
    marginHorizontal: spacing.md,
  },
  streakValue: {
    ...typography.h1,
    color: colors.text,
    marginTop: spacing.sm,
  },
  streakLabel: {
    ...typography.caption,
    color: colors.textMuted,
  },
  activityChart: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    height: 140,
    ...shadows.sm,
  },
  activityDay: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'flex-end',
  },
  activityBar: {
    width: 24,
    borderRadius: borderRadius.sm,
    marginBottom: spacing.sm,
  },
  activityDayLabel: {
    ...typography.small,
    color: colors.textMuted,
  },
  topExerciseRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    padding: spacing.md,
    borderRadius: borderRadius.md,
    marginBottom: spacing.sm,
    ...shadows.sm,
  },
  topExerciseRank: {
    ...typography.bodyBold,
    color: colors.primary,
    width: 32,
  },
  topExerciseName: {
    ...typography.body,
    color: colors.text,
    flex: 1,
  },
  topExerciseVolume: {
    ...typography.caption,
    color: colors.textMuted,
  },
  prRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    padding: spacing.md,
    borderRadius: borderRadius.md,
    marginBottom: spacing.sm,
    gap: spacing.md,
    ...shadows.sm,
  },
  prInfo: {
    flex: 1,
  },
  prExercise: {
    ...typography.bodyBold,
    color: colors.text,
  },
  prDate: {
    ...typography.small,
    color: colors.textMuted,
  },
  prValue: {
    ...typography.bodyBold,
    color: colors.primary,
  },
});
