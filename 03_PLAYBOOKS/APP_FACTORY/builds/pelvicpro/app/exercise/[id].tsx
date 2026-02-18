import { View, Text, StyleSheet, ScrollView, Pressable, Linking } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useLocalSearchParams, useRouter, Stack } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import {
  colors,
  spacing,
  borderRadius,
  typography,
  shadows,
} from '@/constants/theme';
import { exercises, categoryColors } from '@/constants/exercises';
import { useWorkoutStore } from '@/store/workoutStore';

const openLink = (url: string) => {
  Linking.openURL(url).catch(err => console.error('Failed to open URL:', err));
};

export default function ExerciseDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const { favoriteExercises, toggleFavorite, activeWorkout, addExerciseToWorkout } =
    useWorkoutStore();

  const exercise = exercises.find((e) => e.id === id);

  if (!exercise) {
    return (
      <SafeAreaView style={styles.container}>
        <Text style={styles.errorText}>Exercise not found</Text>
      </SafeAreaView>
    );
  }

  const isFavorite = favoriteExercises.includes(exercise.id);

  const handleAddToWorkout = () => {
    if (activeWorkout) {
      addExerciseToWorkout(exercise.id);
      router.back();
    } else {
      // Start new workout and add
      router.push('/(tabs)');
    }
  };

  return (
    <>
      <Stack.Screen
        options={{
          headerTitle: exercise.name,
          headerRight: () => (
            <Pressable onPress={() => toggleFavorite(exercise.id)} hitSlop={12}>
              <Ionicons
                name={isFavorite ? 'heart' : 'heart-outline'}
                size={24}
                color={isFavorite ? colors.primary : colors.text}
              />
            </Pressable>
          ),
        }}
      />
      <SafeAreaView style={styles.container} edges={['bottom']}>
        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.content}
          showsVerticalScrollIndicator={false}
        >
          {/* Video Tutorial Section */}
          {exercise.videoUrl ? (
            <Pressable
              style={[
                styles.videoContainer,
                { backgroundColor: categoryColors[exercise.category] + '30' },
              ]}
              onPress={() => openLink(exercise.videoUrl!)}
            >
              <View style={styles.playButton}>
                <Ionicons name="play-circle" size={64} color={colors.surface} />
              </View>
              <Text style={styles.videoText}>Watch Tutorial</Text>
              <Text style={styles.videoSubtext}>Tap to open in YouTube</Text>
            </Pressable>
          ) : (
            <View
              style={[
                styles.imagePlaceholder,
                { backgroundColor: categoryColors[exercise.category] + '30' },
              ]}
            >
              <Ionicons
                name="barbell"
                size={80}
                color={categoryColors[exercise.category]}
              />
              <Text style={styles.imagePlaceholderText}>
                Video coming soon
              </Text>
            </View>
          )}

          {/* Category Badge */}
          <View style={styles.categoryContainer}>
            <View
              style={[
                styles.categoryBadge,
                { backgroundColor: categoryColors[exercise.category] },
              ]}
            >
              <Text style={styles.categoryText}>
                {exercise.category.toUpperCase()}
              </Text>
            </View>
          </View>

          {/* Muscles */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Muscles Worked</Text>
            <View style={styles.musclesList}>
              {exercise.muscles.map((muscle, index) => (
                <View key={index} style={styles.muscleChip}>
                  <Text style={styles.muscleText}>{muscle}</Text>
                </View>
              ))}
            </View>
          </View>

          {/* Description */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>About</Text>
            <Text style={styles.description}>{exercise.description}</Text>
          </View>

          {/* Equipment */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Equipment</Text>
            <View style={styles.equipmentList}>
              {exercise.equipment.map((item, index) => (
                <View key={index} style={styles.equipmentItem}>
                  <Ionicons name="fitness" size={16} color={colors.primary} />
                  <Text style={styles.equipmentText}>{item}</Text>
                </View>
              ))}
            </View>
          </View>

          {/* Tips */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Tips</Text>
            {exercise.tips.map((tip, index) => (
              <View key={index} style={styles.tipRow}>
                <View style={styles.tipNumber}>
                  <Text style={styles.tipNumberText}>{index + 1}</Text>
                </View>
                <Text style={styles.tipText}>{tip}</Text>
              </View>
            ))}
          </View>

          {/* Recommended Products (Affiliate) */}
          {exercise.affiliateProducts && exercise.affiliateProducts.length > 0 && (
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Recommended Gear</Text>
              <Text style={styles.affiliateDisclosure}>
                We may earn commission from purchases
              </Text>
              {exercise.affiliateProducts.map((product, index) => (
                <Pressable
                  key={index}
                  style={styles.productCard}
                  onPress={() => openLink(product.url)}
                >
                  <View style={styles.productInfo}>
                    <Ionicons
                      name={
                        product.type === 'equipment'
                          ? 'fitness'
                          : product.type === 'supplement'
                          ? 'nutrition'
                          : 'shirt'
                      }
                      size={24}
                      color={colors.primary}
                    />
                    <View style={styles.productText}>
                      <Text style={styles.productName}>{product.name}</Text>
                      {product.price && (
                        <Text style={styles.productPrice}>{product.price}</Text>
                      )}
                    </View>
                  </View>
                  <Ionicons name="chevron-forward" size={20} color={colors.textMuted} />
                </Pressable>
              ))}
            </View>
          )}
        </ScrollView>

        {/* Add to Workout Button */}
        <View style={styles.footer}>
          <Pressable
            style={({ pressed }) => [
              styles.addButton,
              pressed && styles.addButtonPressed,
            ]}
            onPress={handleAddToWorkout}
          >
            <Ionicons name="add-circle" size={24} color={colors.surface} />
            <Text style={styles.addButtonText}>
              {activeWorkout ? 'Add to Workout' : 'Start Workout'}
            </Text>
          </Pressable>
        </View>
      </SafeAreaView>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    paddingBottom: 100,
  },
  errorText: {
    ...typography.body,
    color: colors.error,
    textAlign: 'center',
    marginTop: spacing.xl,
  },
  imagePlaceholder: {
    height: 240,
    alignItems: 'center',
    justifyContent: 'center',
  },
  imagePlaceholderText: {
    ...typography.caption,
    color: colors.textMuted,
    marginTop: spacing.sm,
  },
  videoContainer: {
    height: 240,
    alignItems: 'center',
    justifyContent: 'center',
  },
  playButton: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    ...shadows.lg,
  },
  videoText: {
    ...typography.bodyBold,
    color: colors.text,
    marginTop: spacing.md,
  },
  videoSubtext: {
    ...typography.caption,
    color: colors.textMuted,
    marginTop: spacing.xs,
  },
  affiliateDisclosure: {
    ...typography.small,
    color: colors.textMuted,
    fontStyle: 'italic',
    marginBottom: spacing.md,
  },
  productCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: colors.surface,
    padding: spacing.md,
    borderRadius: borderRadius.md,
    marginBottom: spacing.sm,
    ...shadows.sm,
  },
  productInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
  },
  productText: {
    gap: spacing.xs,
  },
  productName: {
    ...typography.body,
    color: colors.text,
    fontWeight: '500',
  },
  productPrice: {
    ...typography.caption,
    color: colors.primary,
    fontWeight: '600',
  },
  categoryContainer: {
    flexDirection: 'row',
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.md,
  },
  categoryBadge: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    borderRadius: borderRadius.full,
  },
  categoryText: {
    ...typography.small,
    color: colors.surface,
    fontWeight: '700',
    letterSpacing: 1,
  },
  section: {
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.lg,
  },
  sectionTitle: {
    ...typography.h3,
    color: colors.text,
    marginBottom: spacing.md,
  },
  musclesList: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
  },
  muscleChip: {
    backgroundColor: colors.surface,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: borderRadius.full,
    ...shadows.sm,
  },
  muscleText: {
    ...typography.caption,
    color: colors.text,
    fontWeight: '500',
  },
  description: {
    ...typography.body,
    color: colors.textLight,
    lineHeight: 24,
  },
  equipmentList: {
    gap: spacing.sm,
  },
  equipmentItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  equipmentText: {
    ...typography.body,
    color: colors.text,
  },
  tipRow: {
    flexDirection: 'row',
    marginBottom: spacing.md,
    gap: spacing.md,
  },
  tipNumber: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: colors.primary + '20',
    alignItems: 'center',
    justifyContent: 'center',
  },
  tipNumberText: {
    ...typography.caption,
    color: colors.primary,
    fontWeight: '700',
  },
  tipText: {
    ...typography.body,
    color: colors.textLight,
    flex: 1,
    lineHeight: 24,
  },
  footer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    padding: spacing.lg,
    paddingBottom: spacing.xl,
    backgroundColor: colors.background,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  addButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.primary,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    gap: spacing.sm,
    ...shadows.md,
  },
  addButtonPressed: {
    opacity: 0.9,
  },
  addButtonText: {
    ...typography.bodyBold,
    color: colors.surface,
  },
});
