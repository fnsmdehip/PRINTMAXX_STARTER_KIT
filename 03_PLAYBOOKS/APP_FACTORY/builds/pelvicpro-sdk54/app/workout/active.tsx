import { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Pressable,
  TextInput,
  Alert,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { activateKeepAwakeAsync, deactivateKeepAwake } from 'expo-keep-awake';
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
import { getLunaMessage } from '@/constants/luna';
import Luna from '@/components/luna/Luna';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

export default function ActiveWorkoutScreen() {
  const router = useRouter();
  const [elapsedTime, setElapsedTime] = useState(0);
  const [lunaState, setLunaState] = useState<'idle' | 'happy' | 'excited' | 'cheering'>('cheering');
  const [lunaMessage, setLunaMessage] = useState(getLunaMessage('workoutStart'));
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const {
    activeWorkout,
    activeExerciseIndex,
    setActiveExerciseIndex,
    addExerciseToWorkout,
    removeExerciseFromWorkout,
    addSet,
    updateSet,
    completeSet,
    removeSet,
    endWorkout,
    cancelWorkout,
    saveAsTemplate,
  } = useWorkoutStore();

  const { recordWorkout, incrementTrialWorkout, lunaEnabled } = useUserStore();

  useEffect(() => {
    // Keep screen awake during workout
    activateKeepAwakeAsync();

    // Start timer
    timerRef.current = setInterval(() => {
      setElapsedTime((prev) => prev + 1);
    }, 1000);

    return () => {
      deactivateKeepAwake();
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const formatTime = (seconds: number) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    if (hrs > 0) {
      return `${hrs}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleAddExercise = () => {
    router.push('/(tabs)/exercises');
  };

  const handleCompleteSet = (exerciseIndex: number, setIndex: number) => {
    completeSet(exerciseIndex, setIndex);
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

    // Luna reactions
    const currentSet = activeWorkout?.exercises[exerciseIndex].sets[setIndex];
    if (currentSet?.isPersonalRecord) {
      setLunaState('excited');
      setLunaMessage(getLunaMessage('prAchieved'));
    } else {
      setLunaState('happy');
      setLunaMessage(getLunaMessage('setComplete'));
    }

    // Reset Luna after delay
    setTimeout(() => {
      setLunaState('cheering');
      setLunaMessage(getLunaMessage('midWorkout'));
    }, 2000);
  };

  const handleFinishWorkout = () => {
    if (!activeWorkout || activeWorkout.exercises.length === 0) {
      Alert.alert(
        'Empty Workout',
        'Add at least one exercise before finishing.',
        [{ text: 'OK' }]
      );
      return;
    }

    Alert.alert('Finish Workout', 'Great job! Ready to save this workout?', [
      { text: 'Keep Going', style: 'cancel' },
      {
        text: 'Finish',
        onPress: () => {
          endWorkout();
          recordWorkout();
          incrementTrialWorkout();
          router.replace('/(tabs)');
        },
      },
    ]);
  };

  const handleCancelWorkout = () => {
    Alert.alert(
      'Cancel Workout',
      'Are you sure? Your progress will be lost.',
      [
        { text: 'Keep Going', style: 'cancel' },
        {
          text: 'Cancel',
          style: 'destructive',
          onPress: () => {
            cancelWorkout();
            router.replace('/(tabs)');
          },
        },
      ]
    );
  };

  const handleSaveAsTemplate = () => {
    if (!activeWorkout || activeWorkout.exercises.length === 0) return;

    Alert.prompt(
      'Save as Template',
      'Give this workout a name',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Save',
          onPress: (name: string | undefined) => {
            if (name) {
              saveAsTemplate(name);
              Alert.alert('Saved', 'Template saved successfully!');
            }
          },
        },
      ],
      'plain-text',
      activeWorkout.name
    );
  };

  const getExercise = (exerciseId: string) => {
    return exercises.find((e) => e.id === exerciseId);
  };

  if (!activeWorkout) {
    return (
      <SafeAreaView style={styles.container}>
        <Text>No active workout</Text>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <Pressable onPress={handleCancelWorkout} hitSlop={12}>
          <Ionicons name="close" size={28} color={colors.text} />
        </Pressable>
        <View style={styles.headerCenter}>
          <Text style={styles.workoutName}>{activeWorkout.name}</Text>
          <Text style={styles.timer}>{formatTime(elapsedTime)}</Text>
        </View>
        <Pressable onPress={handleSaveAsTemplate} hitSlop={12}>
          <Ionicons name="bookmark-outline" size={24} color={colors.text} />
        </Pressable>
      </View>

      {/* Luna Coach */}
      {lunaEnabled && (
        <View style={styles.lunaCoach}>
          <Luna state={lunaState} size={50} />
          <View style={styles.lunaBubble}>
            <Text style={styles.lunaText}>{lunaMessage}</Text>
          </View>
        </View>
      )}

      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Exercise Cards */}
        {activeWorkout.exercises.map((workoutExercise, exerciseIndex) => {
          const exercise = getExercise(workoutExercise.exerciseId);
          if (!exercise) return null;

          return (
            <View key={`${exercise.id}-${exerciseIndex}`} style={styles.exerciseCard}>
              <View style={styles.exerciseHeader}>
                <View>
                  <Text style={styles.exerciseName}>{exercise.name}</Text>
                  <Text style={styles.exerciseMuscles}>
                    {exercise.muscles.join(' - ')}
                  </Text>
                </View>
                <Pressable
                  onPress={() => {
                    Alert.alert('Remove Exercise', 'Remove this exercise?', [
                      { text: 'Cancel', style: 'cancel' },
                      {
                        text: 'Remove',
                        style: 'destructive',
                        onPress: () => removeExerciseFromWorkout(exerciseIndex),
                      },
                    ]);
                  }}
                  hitSlop={8}
                >
                  <Ionicons name="trash-outline" size={20} color={colors.textMuted} />
                </Pressable>
              </View>

              {/* Sets Table Header */}
              <View style={styles.setsHeader}>
                <Text style={[styles.setHeaderText, { width: 40 }]}>SET</Text>
                <Text style={[styles.setHeaderText, { flex: 1 }]}>PREV</Text>
                <Text style={[styles.setHeaderText, { width: 80 }]}>LBS</Text>
                <Text style={[styles.setHeaderText, { width: 60 }]}>REPS</Text>
                <View style={{ width: 40 }} />
              </View>

              {/* Sets */}
              {workoutExercise.sets.map((set, setIndex) => (
                <View
                  key={set.id}
                  style={[
                    styles.setRow,
                    set.completed && styles.setRowCompleted,
                    set.isPersonalRecord && styles.setRowPR,
                  ]}
                >
                  <Text style={styles.setNumber}>{setIndex + 1}</Text>
                  <Text style={styles.prevValue}>-</Text>
                  <TextInput
                    style={styles.weightInput}
                    value={set.weight > 0 ? set.weight.toString() : ''}
                    onChangeText={(text) => {
                      const weight = parseFloat(text) || 0;
                      updateSet(exerciseIndex, setIndex, { weight });
                    }}
                    keyboardType="decimal-pad"
                    placeholder="0"
                    placeholderTextColor={colors.textMuted}
                    editable={!set.completed}
                  />
                  <TextInput
                    style={styles.repsInput}
                    value={set.reps > 0 ? set.reps.toString() : ''}
                    onChangeText={(text) => {
                      const reps = parseInt(text) || 0;
                      updateSet(exerciseIndex, setIndex, { reps });
                    }}
                    keyboardType="number-pad"
                    placeholder="0"
                    placeholderTextColor={colors.textMuted}
                    editable={!set.completed}
                  />
                  <Pressable
                    style={[
                      styles.checkButton,
                      set.completed && styles.checkButtonCompleted,
                    ]}
                    onPress={() => {
                      if (!set.completed) {
                        handleCompleteSet(exerciseIndex, setIndex);
                      }
                    }}
                    disabled={set.completed}
                  >
                    <Ionicons
                      name="checkmark"
                      size={20}
                      color={set.completed ? colors.surface : colors.textMuted}
                    />
                  </Pressable>
                </View>
              ))}

              {/* Add Set Button */}
              <Pressable
                style={styles.addSetButton}
                onPress={() => addSet(exerciseIndex)}
              >
                <Ionicons name="add" size={20} color={colors.primary} />
                <Text style={styles.addSetText}>Add Set</Text>
              </Pressable>
            </View>
          );
        })}

        {/* Add Exercise Button */}
        <Pressable style={styles.addExerciseButton} onPress={handleAddExercise}>
          <Ionicons name="add-circle" size={24} color={colors.primary} />
          <Text style={styles.addExerciseText}>Add Exercise</Text>
        </Pressable>
      </ScrollView>

      {/* Finish Button */}
      <View style={styles.footer}>
        <Pressable
          style={({ pressed }) => [
            styles.finishButton,
            pressed && styles.finishButtonPressed,
          ]}
          onPress={handleFinishWorkout}
        >
          <Text style={styles.finishButtonText}>Finish Workout</Text>
        </Pressable>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  headerCenter: {
    alignItems: 'center',
  },
  workoutName: {
    ...typography.bodyBold,
    color: colors.text,
  },
  timer: {
    ...typography.mono,
    color: colors.primary,
  },
  lunaCoach: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.sm,
    backgroundColor: colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
    gap: spacing.sm,
  },
  lunaBubble: {
    flex: 1,
    backgroundColor: colors.background,
    padding: spacing.sm,
    borderRadius: borderRadius.md,
  },
  lunaText: {
    ...typography.caption,
    color: colors.text,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: spacing.lg,
    paddingBottom: 100,
  },
  exerciseCard: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    marginBottom: spacing.md,
    ...shadows.sm,
  },
  exerciseHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: spacing.md,
  },
  exerciseName: {
    ...typography.bodyBold,
    color: colors.text,
  },
  exerciseMuscles: {
    ...typography.caption,
    color: colors.textMuted,
  },
  setsHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.xs,
    marginBottom: spacing.xs,
  },
  setHeaderText: {
    ...typography.small,
    color: colors.textMuted,
    textAlign: 'center',
  },
  setRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.sm,
    borderRadius: borderRadius.sm,
    marginBottom: spacing.xs,
  },
  setRowCompleted: {
    backgroundColor: colors.success + '15',
  },
  setRowPR: {
    backgroundColor: colors.warning + '20',
  },
  setNumber: {
    ...typography.bodyBold,
    color: colors.textLight,
    width: 40,
    textAlign: 'center',
  },
  prevValue: {
    ...typography.caption,
    color: colors.textMuted,
    flex: 1,
    textAlign: 'center',
  },
  weightInput: {
    width: 80,
    height: 40,
    backgroundColor: colors.background,
    borderRadius: borderRadius.sm,
    textAlign: 'center',
    ...typography.body,
    color: colors.text,
    marginHorizontal: spacing.xs,
  },
  repsInput: {
    width: 60,
    height: 40,
    backgroundColor: colors.background,
    borderRadius: borderRadius.sm,
    textAlign: 'center',
    ...typography.body,
    color: colors.text,
    marginHorizontal: spacing.xs,
  },
  checkButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: colors.background,
    alignItems: 'center',
    justifyContent: 'center',
    marginLeft: spacing.xs,
  },
  checkButtonCompleted: {
    backgroundColor: colors.success,
  },
  addSetButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: spacing.sm,
    gap: spacing.xs,
    marginTop: spacing.sm,
  },
  addSetText: {
    ...typography.caption,
    color: colors.primary,
    fontWeight: '600',
  },
  addExerciseButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    borderWidth: 2,
    borderColor: colors.primary,
    borderStyle: 'dashed',
    gap: spacing.sm,
  },
  addExerciseText: {
    ...typography.bodyBold,
    color: colors.primary,
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
  finishButton: {
    backgroundColor: colors.primary,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    alignItems: 'center',
    ...shadows.md,
  },
  finishButtonPressed: {
    opacity: 0.9,
  },
  finishButtonText: {
    ...typography.bodyBold,
    color: colors.surface,
  },
});
