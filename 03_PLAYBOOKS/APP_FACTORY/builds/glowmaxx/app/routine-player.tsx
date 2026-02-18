import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';

import { useDailyLogStore } from '../src/stores/dailyLogStore';
import { getRoutineById, getExerciseById } from '../src/data/exercises';
import { COLORS, MORNING_SKINCARE_STEPS, EVENING_SKINCARE_STEPS, MEWING_INSTRUCTIONS } from '../src/utils/constants';
import { formatDuration } from '../src/utils/dateUtils';
import { Exercise } from '../src/types';

export default function RoutinePlayerScreen() {
  const { routineId } = useLocalSearchParams<{ routineId: string }>();
  const { completeRoutine } = useDailyLogStore();

  const routine = getRoutineById(routineId || '');
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [timer, setTimer] = useState(0);

  // Get content based on routine type
  const getSteps = () => {
    if (!routine) return [];

    if (routine.type === 'morning_skincare') {
      return MORNING_SKINCARE_STEPS.map((step, i) => ({
        id: step.id,
        name: step.name,
        description: step.description,
        duration: 60,
      }));
    }

    if (routine.type === 'evening_skincare') {
      return EVENING_SKINCARE_STEPS.map((step, i) => ({
        id: step.id,
        name: step.name,
        description: step.description,
        duration: 60,
      }));
    }

    if (routine.type === 'mewing') {
      return MEWING_INSTRUCTIONS.map((instruction, i) => ({
        id: `mewing_${i}`,
        name: `Step ${i + 1}`,
        description: instruction,
        duration: 30,
      }));
    }

    // For exercise routines
    return routine.exercises.map((ex) => ({
      id: ex.id,
      name: ex.name,
      description: ex.description,
      instructions: ex.instructions,
      duration: ex.duration,
    }));
  };

  const steps = getSteps();
  const currentStepData = steps[currentStep];
  const isLastStep = currentStep === steps.length - 1;
  const progress = steps.length > 0 ? ((currentStep + 1) / steps.length) * 100 : 0;

  // Timer logic
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isPlaying && currentStepData) {
      interval = setInterval(() => {
        setTimer((t) => {
          if (t >= currentStepData.duration - 1) {
            // Auto-advance
            Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
            if (!isLastStep) {
              setCurrentStep((s) => s + 1);
              return 0;
            } else {
              setIsPlaying(false);
              return currentStepData.duration;
            }
          }
          return t + 1;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isPlaying, currentStep, currentStepData, isLastStep]);

  // Reset timer on step change
  useEffect(() => {
    setTimer(0);
  }, [currentStep]);

  const handlePlayPause = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    setIsPlaying(!isPlaying);
  };

  const handleNext = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    if (!isLastStep) {
      setCurrentStep(currentStep + 1);
      setTimer(0);
    }
  };

  const handlePrev = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
      setTimer(0);
    }
  };

  const handleComplete = () => {
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    if (routine) {
      completeRoutine(routine.id);
    }
    router.back();
  };

  if (!routine) {
    return (
      <SafeAreaView style={styles.container}>
        <Text style={styles.errorText}>Routine not found</Text>
        <TouchableOpacity onPress={() => router.back()}>
          <Text style={styles.backLink}>Go Back</Text>
        </TouchableOpacity>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container} edges={['bottom']}>
      {/* Progress bar */}
      <View style={styles.progressContainer}>
        <View style={styles.progressBar}>
          <View style={[styles.progressFill, { width: `${progress}%` }]} />
        </View>
        <Text style={styles.progressText}>
          {currentStep + 1} / {steps.length}
        </Text>
      </View>

      {/* Main content */}
      <ScrollView
        style={styles.content}
        contentContainerStyle={styles.contentContainer}
      >
        <View style={styles.stepCard}>
          <Text style={styles.stepLabel}>
            {routine.type === 'facial_exercises' ? 'Exercise' : 'Step'} {currentStep + 1}
          </Text>
          <Text style={styles.stepName}>{currentStepData?.name}</Text>
          <Text style={styles.stepDescription}>{currentStepData?.description}</Text>

          {/* Instructions if available */}
          {(currentStepData as any)?.instructions && (
            <View style={styles.instructionsList}>
              {((currentStepData as any).instructions as string[]).map(
                (instruction: string, i: number) => (
                  <View key={i} style={styles.instructionRow}>
                    <Text style={styles.instructionNumber}>{i + 1}</Text>
                    <Text style={styles.instructionText}>{instruction}</Text>
                  </View>
                )
              )}
            </View>
          )}
        </View>

        {/* Timer */}
        <View style={styles.timerContainer}>
          <View style={styles.timerCircle}>
            <Text style={styles.timerText}>{formatDuration(timer)}</Text>
            <Text style={styles.timerLabel}>
              / {formatDuration(currentStepData?.duration || 0)}
            </Text>
          </View>
        </View>
      </ScrollView>

      {/* Controls */}
      <View style={styles.controls}>
        <TouchableOpacity
          style={[styles.controlButton, currentStep === 0 && styles.controlButtonDisabled]}
          onPress={handlePrev}
          disabled={currentStep === 0}
        >
          <Ionicons
            name="play-skip-back"
            size={28}
            color={currentStep === 0 ? COLORS.disabled : COLORS.text}
          />
        </TouchableOpacity>

        <TouchableOpacity style={styles.playButton} onPress={handlePlayPause}>
          <Ionicons
            name={isPlaying ? 'pause' : 'play'}
            size={36}
            color={COLORS.surface}
          />
        </TouchableOpacity>

        {isLastStep ? (
          <TouchableOpacity style={styles.completeButton} onPress={handleComplete}>
            <Ionicons name="checkmark" size={28} color={COLORS.surface} />
          </TouchableOpacity>
        ) : (
          <TouchableOpacity style={styles.controlButton} onPress={handleNext}>
            <Ionicons name="play-skip-forward" size={28} color={COLORS.text} />
          </TouchableOpacity>
        )}
      </View>

      {/* Skip to complete */}
      <TouchableOpacity style={styles.skipButton} onPress={handleComplete}>
        <Text style={styles.skipText}>Mark as Complete</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  errorText: {
    fontSize: 16,
    color: COLORS.error,
    textAlign: 'center',
    marginTop: 40,
  },
  backLink: {
    fontSize: 16,
    color: COLORS.primary,
    textAlign: 'center',
    marginTop: 20,
  },
  progressContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
    gap: 12,
  },
  progressBar: {
    flex: 1,
    height: 4,
    backgroundColor: COLORS.border,
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: COLORS.primary,
    borderRadius: 2,
  },
  progressText: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.textSecondary,
  },
  content: {
    flex: 1,
  },
  contentContainer: {
    padding: 20,
    alignItems: 'center',
  },
  stepCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 20,
    padding: 24,
    width: '100%',
    marginBottom: 30,
  },
  stepLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.primary,
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: 8,
  },
  stepName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 12,
  },
  stepDescription: {
    fontSize: 16,
    color: COLORS.textSecondary,
    lineHeight: 24,
  },
  instructionsList: {
    marginTop: 20,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
    paddingTop: 16,
  },
  instructionRow: {
    flexDirection: 'row',
    marginBottom: 12,
    gap: 12,
  },
  instructionNumber: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: COLORS.primaryLight,
    textAlign: 'center',
    lineHeight: 24,
    fontSize: 13,
    fontWeight: '600',
    color: COLORS.primary,
  },
  instructionText: {
    flex: 1,
    fontSize: 14,
    color: COLORS.text,
    lineHeight: 20,
  },
  timerContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  timerCircle: {
    width: 160,
    height: 160,
    borderRadius: 80,
    backgroundColor: COLORS.surface,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 6,
    borderColor: COLORS.primary,
  },
  timerText: {
    fontSize: 40,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  timerLabel: {
    fontSize: 16,
    color: COLORS.textSecondary,
  },
  controls: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 20,
    gap: 30,
  },
  controlButton: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: COLORS.surface,
    alignItems: 'center',
    justifyContent: 'center',
  },
  controlButtonDisabled: {
    opacity: 0.5,
  },
  playButton: {
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: COLORS.primary,
    alignItems: 'center',
    justifyContent: 'center',
  },
  completeButton: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: COLORS.success,
    alignItems: 'center',
    justifyContent: 'center',
  },
  skipButton: {
    paddingVertical: 16,
    alignItems: 'center',
  },
  skipText: {
    fontSize: 15,
    color: COLORS.textSecondary,
    textDecorationLine: 'underline',
  },
});
