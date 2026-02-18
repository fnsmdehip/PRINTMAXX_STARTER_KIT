import { useState, useMemo } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Pressable,
  TextInput,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import {
  colors,
  spacing,
  borderRadius,
  typography,
  shadows,
} from '@/constants/theme';
import {
  exercises,
  exercisesByCategory,
  categoryLabels,
  categoryColors,
  type MuscleGroup,
} from '@/constants/exercises';
import { useWorkoutStore } from '@/store/workoutStore';

const categories: MuscleGroup[] = [
  'glutes',
  'legs',
  'arms',
  'back',
  'chest',
  'shoulders',
  'core',
];

export default function ExercisesScreen() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<MuscleGroup | 'all'>(
    'all'
  );
  const { favoriteExercises, toggleFavorite, activeWorkout, addExerciseToWorkout } =
    useWorkoutStore();

  const filteredExercises = useMemo(() => {
    let result = exercises;

    // Filter by category
    if (selectedCategory !== 'all') {
      result = exercisesByCategory[selectedCategory] || [];
    }

    // Filter by search
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      result = result.filter(
        (e) =>
          e.name.toLowerCase().includes(query) ||
          e.muscles.some((m) => m.toLowerCase().includes(query))
      );
    }

    return result;
  }, [selectedCategory, searchQuery]);

  const handleExercisePress = (exerciseId: string) => {
    if (activeWorkout) {
      addExerciseToWorkout(exerciseId);
      router.back();
    } else {
      router.push(`/exercise/${exerciseId}`);
    }
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Exercises</Text>
        {activeWorkout && (
          <Text style={styles.subtitle}>Tap to add to workout</Text>
        )}
      </View>

      {/* Search */}
      <View style={styles.searchContainer}>
        <Ionicons name="search" size={20} color={colors.textMuted} />
        <TextInput
          style={styles.searchInput}
          placeholder="Search exercises..."
          placeholderTextColor={colors.textMuted}
          value={searchQuery}
          onChangeText={setSearchQuery}
          autoCapitalize="none"
          autoCorrect={false}
        />
        {searchQuery.length > 0 && (
          <Pressable onPress={() => setSearchQuery('')}>
            <Ionicons name="close-circle" size={20} color={colors.textMuted} />
          </Pressable>
        )}
      </View>

      {/* Category Pills */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.categoryContainer}
      >
        <Pressable
          style={[
            styles.categoryPill,
            selectedCategory === 'all' && styles.categoryPillActive,
          ]}
          onPress={() => setSelectedCategory('all')}
        >
          <Text
            style={[
              styles.categoryText,
              selectedCategory === 'all' && styles.categoryTextActive,
            ]}
          >
            All
          </Text>
        </Pressable>
        {categories.map((category) => (
          <Pressable
            key={category}
            style={[
              styles.categoryPill,
              selectedCategory === category && {
                backgroundColor: categoryColors[category],
              },
            ]}
            onPress={() => setSelectedCategory(category)}
          >
            <Text
              style={[
                styles.categoryText,
                selectedCategory === category && styles.categoryTextActive,
              ]}
            >
              {categoryLabels[category]}
            </Text>
          </Pressable>
        ))}
      </ScrollView>

      {/* Exercise List */}
      <ScrollView
        style={styles.exerciseList}
        contentContainerStyle={styles.exerciseListContent}
        showsVerticalScrollIndicator={false}
      >
        {filteredExercises.length === 0 ? (
          <View style={styles.emptyState}>
            <Ionicons name="search" size={48} color={colors.textMuted} />
            <Text style={styles.emptyText}>No exercises found</Text>
          </View>
        ) : (
          filteredExercises.map((exercise) => {
            const isFavorite = favoriteExercises.includes(exercise.id);
            return (
              <Pressable
                key={exercise.id}
                style={({ pressed }) => [
                  styles.exerciseCard,
                  pressed && styles.exerciseCardPressed,
                ]}
                onPress={() => handleExercisePress(exercise.id)}
              >
                <View
                  style={[
                    styles.exerciseIndicator,
                    { backgroundColor: categoryColors[exercise.category] },
                  ]}
                />
                <View style={styles.exerciseInfo}>
                  <Text style={styles.exerciseName}>{exercise.name}</Text>
                  <Text style={styles.exerciseMuscles}>
                    {exercise.muscles.join(' • ')}
                  </Text>
                </View>
                <Pressable
                  onPress={() => toggleFavorite(exercise.id)}
                  hitSlop={8}
                >
                  <Ionicons
                    name={isFavorite ? 'heart' : 'heart-outline'}
                    size={24}
                    color={isFavorite ? colors.primary : colors.textMuted}
                  />
                </Pressable>
              </Pressable>
            );
          })
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
  subtitle: {
    ...typography.caption,
    color: colors.primary,
    marginTop: spacing.xs,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    marginHorizontal: spacing.lg,
    paddingHorizontal: spacing.md,
    borderRadius: borderRadius.md,
    height: 48,
    gap: spacing.sm,
    ...shadows.sm,
  },
  searchInput: {
    flex: 1,
    ...typography.body,
    color: colors.text,
  },
  categoryContainer: {
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
    gap: spacing.sm,
  },
  categoryPill: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: borderRadius.full,
    backgroundColor: colors.surface,
    marginRight: spacing.sm,
  },
  categoryPillActive: {
    backgroundColor: colors.primary,
  },
  categoryText: {
    ...typography.caption,
    color: colors.textLight,
    fontWeight: '600',
  },
  categoryTextActive: {
    color: colors.surface,
  },
  exerciseList: {
    flex: 1,
  },
  exerciseListContent: {
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.xxl,
  },
  exerciseCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    padding: spacing.md,
    borderRadius: borderRadius.md,
    marginBottom: spacing.sm,
    ...shadows.sm,
  },
  exerciseCardPressed: {
    opacity: 0.9,
    transform: [{ scale: 0.99 }],
  },
  exerciseIndicator: {
    width: 4,
    height: 40,
    borderRadius: 2,
    marginRight: spacing.md,
  },
  exerciseInfo: {
    flex: 1,
  },
  exerciseName: {
    ...typography.bodyBold,
    color: colors.text,
  },
  exerciseMuscles: {
    ...typography.caption,
    color: colors.textMuted,
    marginTop: 2,
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: spacing.xxl,
  },
  emptyText: {
    ...typography.body,
    color: colors.textMuted,
    marginTop: spacing.md,
  },
});
