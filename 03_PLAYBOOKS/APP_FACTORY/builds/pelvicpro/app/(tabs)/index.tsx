import { View, Text, StyleSheet, ScrollView, Pressable } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, borderRadius, typography, shadows } from '@/constants/theme';
import { useUserStore } from '@/store/userStore';
import { useWorkoutStore } from '@/store/workoutStore';
import { getLunaMessage, getStreakMessage } from '@/constants/luna';
import Luna from '@/components/luna/Luna';

export default function HomeScreen() {
  const router = useRouter();
  const {
    profile,
    currentStreak,
    longestStreak,
    totalWorkouts,
    lunaEnabled,
    lastWorkoutDate,
  } = useUserStore();
  const { templates, startWorkout, startWorkoutFromTemplate } =
    useWorkoutStore();

  const handleStartWorkout = () => {
    startWorkout();
    router.push('/workout/active');
  };

  const handleStartFromTemplate = (templateId: string) => {
    startWorkoutFromTemplate(templateId);
    router.push('/workout/active');
  };

  const lunaMessage = currentStreak > 0
    ? getStreakMessage(currentStreak)
    : getLunaMessage('homeGreeting');

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>
              Hey{profile.name ? `, ${profile.name}` : ''}!
            </Text>
            <Text style={styles.subGreeting}>Ready to get strong?</Text>
          </View>
        </View>

        {/* Luna Section */}
        {lunaEnabled && (
          <View style={styles.lunaSection}>
            <Luna state="idle" size={100} />
            <View style={styles.lunaBubble}>
              <Text style={styles.lunaMessage}>{lunaMessage}</Text>
            </View>
          </View>
        )}

        {/* Streak Card */}
        <View style={styles.streakCard}>
          <View style={styles.streakIcon}>
            <Ionicons name="flame" size={32} color={colors.primary} />
          </View>
          <View style={styles.streakInfo}>
            <Text style={styles.streakNumber}>{currentStreak}</Text>
            <Text style={styles.streakLabel}>day streak</Text>
          </View>
          <View style={styles.streakDivider} />
          <View style={styles.streakInfo}>
            <Text style={styles.streakNumber}>{longestStreak}</Text>
            <Text style={styles.streakLabel}>longest</Text>
          </View>
          <View style={styles.streakDivider} />
          <View style={styles.streakInfo}>
            <Text style={styles.streakNumber}>{totalWorkouts}</Text>
            <Text style={styles.streakLabel}>workouts</Text>
          </View>
        </View>

        {/* Start Workout Button */}
        <Pressable
          style={({ pressed }) => [
            styles.startButton,
            pressed && styles.startButtonPressed,
          ]}
          onPress={handleStartWorkout}
        >
          <Ionicons name="add-circle" size={24} color={colors.surface} />
          <Text style={styles.startButtonText}>Start Empty Workout</Text>
        </Pressable>

        {/* Templates Section */}
        {templates.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Your Templates</Text>
            {templates.slice(0, 3).map((template) => (
              <Pressable
                key={template.id}
                style={({ pressed }) => [
                  styles.templateCard,
                  pressed && styles.templateCardPressed,
                ]}
                onPress={() => handleStartFromTemplate(template.id)}
              >
                <View style={styles.templateInfo}>
                  <Text style={styles.templateName}>{template.name}</Text>
                  <Text style={styles.templateExercises}>
                    {template.exercises.length} exercises
                  </Text>
                </View>
                <Ionicons
                  name="play-circle"
                  size={32}
                  color={colors.primary}
                />
              </Pressable>
            ))}
          </View>
        )}

        {/* Quick Start Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Quick Start</Text>
          <View style={styles.quickStartGrid}>
            {[
              { name: 'Glute Day', icon: 'fitness', color: '#FF7B7B' },
              { name: 'Upper Body', icon: 'body', color: '#B8A9C9' },
              { name: 'Leg Day', icon: 'walk', color: '#98D7C2' },
              { name: 'Full Body', icon: 'barbell', color: '#FFB366' },
            ].map((item) => (
              <Pressable
                key={item.name}
                style={({ pressed }) => [
                  styles.quickStartCard,
                  { backgroundColor: item.color + '20' },
                  pressed && styles.quickStartCardPressed,
                ]}
                onPress={() => {
                  startWorkout(item.name);
                  router.push('/workout/active');
                }}
              >
                <Ionicons
                  name={item.icon as any}
                  size={28}
                  color={item.color}
                />
                <Text style={[styles.quickStartText, { color: item.color }]}>
                  {item.name}
                </Text>
              </Pressable>
            ))}
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
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
    padding: spacing.lg,
    paddingBottom: spacing.xxl,
  },
  header: {
    marginBottom: spacing.lg,
  },
  greeting: {
    ...typography.h1,
    color: colors.text,
  },
  subGreeting: {
    ...typography.body,
    color: colors.textLight,
    marginTop: spacing.xs,
  },
  lunaSection: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.lg,
    gap: spacing.md,
  },
  lunaBubble: {
    flex: 1,
    backgroundColor: colors.surface,
    padding: spacing.md,
    borderRadius: borderRadius.lg,
    ...shadows.sm,
  },
  lunaMessage: {
    ...typography.body,
    color: colors.text,
  },
  streakCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    marginBottom: spacing.lg,
    ...shadows.md,
  },
  streakIcon: {
    marginRight: spacing.md,
  },
  streakInfo: {
    flex: 1,
    alignItems: 'center',
  },
  streakNumber: {
    ...typography.h2,
    color: colors.text,
  },
  streakLabel: {
    ...typography.caption,
    color: colors.textMuted,
  },
  streakDivider: {
    width: 1,
    height: 40,
    backgroundColor: colors.border,
  },
  startButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.primary,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    gap: spacing.sm,
    marginBottom: spacing.xl,
    ...shadows.md,
  },
  startButtonPressed: {
    opacity: 0.9,
    transform: [{ scale: 0.98 }],
  },
  startButtonText: {
    ...typography.bodyBold,
    color: colors.surface,
  },
  section: {
    marginBottom: spacing.xl,
  },
  sectionTitle: {
    ...typography.h3,
    color: colors.text,
    marginBottom: spacing.md,
  },
  templateCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.md,
    marginBottom: spacing.sm,
    ...shadows.sm,
  },
  templateCardPressed: {
    opacity: 0.9,
  },
  templateInfo: {
    flex: 1,
  },
  templateName: {
    ...typography.bodyBold,
    color: colors.text,
  },
  templateExercises: {
    ...typography.caption,
    color: colors.textMuted,
  },
  quickStartGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
  },
  quickStartCard: {
    width: '48%',
    padding: spacing.lg,
    borderRadius: borderRadius.md,
    alignItems: 'center',
    gap: spacing.sm,
  },
  quickStartCardPressed: {
    opacity: 0.8,
  },
  quickStartText: {
    ...typography.bodyBold,
  },
});
