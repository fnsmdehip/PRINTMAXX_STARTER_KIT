import React, { useEffect, useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  Alert,
  BackHandler,
} from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import * as Haptics from 'expo-haptics';
import { Ionicons } from '@expo/vector-icons';
import { useStudyStore } from '../stores/studyStore';
import { useUserStore } from '../stores/userStore';
import { useQuizStore } from '../stores/quizStore';
import { useTimer } from '../hooks/useTimer';
import { COLORS, FOCUS_MODES } from '../utils/constants';
import { getMotivationalMessage } from '../utils/timer';
import { FocusMode, Subject } from '../types';
import TimerDisplay from '../components/TimerDisplay';
import Button from '../components/Button';
import QuizCard from '../components/QuizCard';

export default function TimerScreen() {
  const router = useRouter();
  const params = useLocalSearchParams<{
    mode: FocusMode;
    duration: string;
    subject: Subject;
  }>();

  const {
    startSession,
    pauseSession,
    resumeSession,
    endSession,
    addPenaltyTime,
    shouldShowQuiz,
    recordQuizTime,
    currentSession,
  } = useStudyStore();

  const { addStudyTime, updateStreak, recordQuizResult, settings } = useUserStore();
  const { getRandomQuestion, submitAnswer, state: quizState } = useQuizStore();

  const {
    timeRemaining,
    totalTime,
    isRunning,
    isPaused,
    isBreak,
    currentCycle,
    focusMode,
  } = useTimer();

  const [showQuiz, setShowQuiz] = useState(false);
  const [sessionStarted, setSessionStarted] = useState(false);

  // Initialize session on mount
  useEffect(() => {
    if (!sessionStarted && params.mode && params.duration && params.subject) {
      startSession(
        params.mode,
        params.subject,
        parseInt(params.duration, 10)
      );
      setSessionStarted(true);
    }
  }, [params, sessionStarted]);

  // Check for quiz display
  useEffect(() => {
    if (settings.quizDuringSession && shouldShowQuiz() && !showQuiz && !isBreak) {
      pauseSession();
      getRandomQuestion(params.subject);
      setShowQuiz(true);
    }
  }, [timeRemaining, shouldShowQuiz, showQuiz, isBreak]);

  // Handle timer completion
  useEffect(() => {
    if (timeRemaining === 0 && isRunning === false && !isPaused && sessionStarted) {
      handleSessionComplete();
    }
  }, [timeRemaining, isRunning, isPaused, sessionStarted]);

  // Prevent back navigation during session
  useEffect(() => {
    const backHandler = BackHandler.addEventListener('hardwareBackPress', () => {
      handleQuit();
      return true;
    });

    return () => backHandler.remove();
  }, []);

  const handleSessionComplete = async () => {
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

    const session = endSession(true);
    if (session) {
      await addStudyTime(session.duration, session.subject);
      await updateStreak();
    }

    Alert.alert(
      'Session Complete!',
      'Great work! You completed your study session.',
      [
        {
          text: 'View Stats',
          onPress: () => router.replace('/stats'),
        },
        {
          text: 'Done',
          onPress: () => router.replace('/'),
        },
      ]
    );
  };

  const handlePauseResume = () => {
    if (isPaused) {
      resumeSession();
    } else {
      pauseSession();
    }
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
  };

  const handleQuit = () => {
    Alert.alert(
      'End Session?',
      'Are you sure you want to end this session early? Progress will still be saved.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'End Session',
          style: 'destructive',
          onPress: async () => {
            const session = endSession(false);
            if (session && session.duration > 0) {
              await addStudyTime(session.duration, session.subject);
            }
            router.replace('/');
          },
        },
      ]
    );
  };

  const handleQuizAnswer = async (selectedIndex: number, isCorrect: boolean) => {
    await recordQuizResult(isCorrect);

    if (!isCorrect && settings.penaltyMinutes > 0) {
      addPenaltyTime(settings.penaltyMinutes);
    }

    recordQuizTime();

    // Small delay before resuming
    setTimeout(() => {
      setShowQuiz(false);
      resumeSession();
    }, 1500);
  };

  const mode = FOCUS_MODES[focusMode];
  const progress = totalTime > 0 ? (totalTime - timeRemaining) / totalTime : 0;

  if (showQuiz && quizState.currentQuestion) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.quizContainer}>
          <Text style={styles.quizTitle}>Time for a Knowledge Check!</Text>
          <QuizCard
            question={quizState.currentQuestion}
            onAnswer={handleQuizAnswer}
            showPenaltyWarning={settings.penaltyMinutes > 0}
            penaltyMinutes={settings.penaltyMinutes}
          />
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        {/* Mode indicator */}
        <View style={styles.modeIndicator}>
          <Text style={styles.modeName}>{mode?.name || 'Study'}</Text>
          {mode?.cycles > 1 && (
            <Text style={styles.cycleText}>
              Cycle {currentCycle} of {mode.cycles}
            </Text>
          )}
        </View>

        {/* Timer */}
        <View style={styles.timerContainer}>
          <TimerDisplay
            timeRemaining={timeRemaining}
            totalTime={totalTime}
            isBreak={isBreak}
          />
        </View>

        {/* Motivational Message */}
        <Text style={styles.motivationText}>
          {getMotivationalMessage(progress)}
        </Text>

        {/* Status indicator */}
        {isPaused && (
          <View style={styles.pausedIndicator}>
            <Ionicons name="pause-circle" size={20} color={COLORS.warning} />
            <Text style={styles.pausedText}>Paused</Text>
          </View>
        )}

        {/* Controls */}
        <View style={styles.controls}>
          <Button
            title={isPaused ? 'Resume' : 'Pause'}
            onPress={handlePauseResume}
            variant="outline"
            size="large"
            style={styles.controlButton}
          />
          <Button
            title="End Session"
            onPress={handleQuit}
            variant="ghost"
            size="large"
            style={styles.controlButton}
          />
        </View>

        {/* Session info */}
        <View style={styles.sessionInfo}>
          <View style={styles.infoItem}>
            <Text style={styles.infoLabel}>Subject</Text>
            <Text style={styles.infoValue}>{params.subject}</Text>
          </View>
          {currentSession && currentSession.penaltyMinutesAdded > 0 && (
            <View style={styles.infoItem}>
              <Text style={styles.infoLabel}>Penalty Added</Text>
              <Text style={[styles.infoValue, { color: COLORS.error }]}>
                +{currentSession.penaltyMinutesAdded}min
              </Text>
            </View>
          )}
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  content: {
    flex: 1,
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  modeIndicator: {
    alignItems: 'center',
    marginTop: 40,
  },
  modeName: {
    fontSize: 20,
    fontWeight: '600',
    color: COLORS.primary,
  },
  cycleText: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  timerContainer: {
    marginVertical: 40,
  },
  motivationText: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 20,
  },
  pausedIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingVertical: 8,
    paddingHorizontal: 16,
    backgroundColor: COLORS.warning + '20',
    borderRadius: 20,
    marginBottom: 20,
  },
  pausedText: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.warning,
  },
  controls: {
    width: '100%',
    gap: 12,
    marginTop: 20,
  },
  controlButton: {
    width: '100%',
  },
  sessionInfo: {
    flexDirection: 'row',
    gap: 24,
    marginTop: 40,
  },
  infoItem: {
    alignItems: 'center',
  },
  infoLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  infoValue: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginTop: 4,
    textTransform: 'capitalize',
  },
  quizContainer: {
    flex: 1,
    justifyContent: 'center',
    paddingVertical: 20,
  },
  quizTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: 24,
  },
});
