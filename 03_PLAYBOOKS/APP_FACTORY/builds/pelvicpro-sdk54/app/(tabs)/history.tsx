import { View, Text, StyleSheet, ScrollView, Pressable } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { format, parseISO } from 'date-fns';
import {
  colors,
  spacing,
  borderRadius,
  typography,
  shadows,
} from '@/constants/theme';
import { useWorkoutStore } from '@/store/workoutStore';
import { exercises } from '@/constants/exercises';

export default function HistoryScreen() {
  const { workoutHistory } = useWorkoutStore();

  const getExerciseName = (exerciseId: string) => {
    return exercises.find((e) => e.id === exerciseId)?.name || 'Unknown';
  };

  const getTotalVolume = (workout: (typeof workoutHistory)[0]) => {
    let total = 0;
    workout.exercises.forEach((ex) => {
      ex.sets.forEach((set) => {
        if (set.completed) {
          total += set.weight * set.reps;
        }
      });
    });
    return total;
  };

  const getTotalSets = (workout: (typeof workoutHistory)[0]) => {
    return workout.exercises.reduce(
      (acc, ex) => acc + ex.sets.filter((s) => s.completed).length,
      0
    );
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <View style={styles.header}>
        <Text style={styles.title}>History</Text>
        <Text style={styles.subtitle}>
          {workoutHistory.length} workouts logged
        </Text>
      </View>

      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {workoutHistory.length === 0 ? (
          <View style={styles.emptyState}>
            <Ionicons name="calendar-outline" size={64} color={colors.textMuted} />
            <Text style={styles.emptyTitle}>No workouts yet</Text>
            <Text style={styles.emptyText}>
              Start your first workout and it will show up here!
            </Text>
          </View>
        ) : (
          workoutHistory.map((workout) => (
            <Pressable
              key={workout.id}
              style={({ pressed }) => [
                styles.workoutCard,
                pressed && styles.workoutCardPressed,
              ]}
            >
              <View style={styles.workoutHeader}>
                <View>
                  <Text style={styles.workoutName}>{workout.name}</Text>
                  <Text style={styles.workoutDate}>
                    {format(parseISO(workout.date), 'EEEE, MMM d')}
                  </Text>
                </View>
                <View style={styles.workoutDuration}>
                  <Ionicons name="time-outline" size={16} color={colors.textMuted} />
                  <Text style={styles.durationText}>{workout.duration} min</Text>
                </View>
              </View>

              <View style={styles.workoutStats}>
                <View style={styles.stat}>
                  <Text style={styles.statValue}>{workout.exercises.length}</Text>
                  <Text style={styles.statLabel}>exercises</Text>
                </View>
                <View style={styles.stat}>
                  <Text style={styles.statValue}>{getTotalSets(workout)}</Text>
                  <Text style={styles.statLabel}>sets</Text>
                </View>
                <View style={styles.stat}>
                  <Text style={styles.statValue}>
                    {getTotalVolume(workout).toLocaleString()}
                  </Text>
                  <Text style={styles.statLabel}>lbs</Text>
                </View>
              </View>

              <View style={styles.exerciseList}>
                {workout.exercises.slice(0, 4).map((ex, index) => (
                  <Text key={index} style={styles.exerciseItem}>
                    {getExerciseName(ex.exerciseId)} -{' '}
                    {ex.sets.filter((s) => s.completed).length} sets
                  </Text>
                ))}
                {workout.exercises.length > 4 && (
                  <Text style={styles.moreExercises}>
                    +{workout.exercises.length - 4} more
                  </Text>
                )}
              </View>
            </Pressable>
          ))
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
    paddingBottom: spacing.md,
  },
  title: {
    ...typography.h1,
    color: colors.text,
  },
  subtitle: {
    ...typography.caption,
    color: colors.textMuted,
    marginTop: spacing.xs,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.xxl,
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: spacing.xxl * 2,
  },
  emptyTitle: {
    ...typography.h3,
    color: colors.text,
    marginTop: spacing.lg,
  },
  emptyText: {
    ...typography.body,
    color: colors.textMuted,
    textAlign: 'center',
    marginTop: spacing.sm,
    paddingHorizontal: spacing.xl,
  },
  workoutCard: {
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    marginBottom: spacing.md,
    ...shadows.sm,
  },
  workoutCardPressed: {
    opacity: 0.95,
  },
  workoutHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: spacing.md,
  },
  workoutName: {
    ...typography.bodyBold,
    color: colors.text,
  },
  workoutDate: {
    ...typography.caption,
    color: colors.textMuted,
    marginTop: 2,
  },
  workoutDuration: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  durationText: {
    ...typography.caption,
    color: colors.textMuted,
  },
  workoutStats: {
    flexDirection: 'row',
    backgroundColor: colors.background,
    borderRadius: borderRadius.md,
    padding: spacing.md,
    marginBottom: spacing.md,
  },
  stat: {
    flex: 1,
    alignItems: 'center',
  },
  statValue: {
    ...typography.h3,
    color: colors.primary,
  },
  statLabel: {
    ...typography.small,
    color: colors.textMuted,
  },
  exerciseList: {
    gap: spacing.xs,
  },
  exerciseItem: {
    ...typography.caption,
    color: colors.textLight,
  },
  moreExercises: {
    ...typography.caption,
    color: colors.textMuted,
    fontStyle: 'italic',
  },
});
