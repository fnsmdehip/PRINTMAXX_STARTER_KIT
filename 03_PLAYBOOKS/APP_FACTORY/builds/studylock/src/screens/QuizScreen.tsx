import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useQuizStore } from '../stores/quizStore';
import { useUserStore } from '../stores/userStore';
import { COLORS, SUBJECTS } from '../utils/constants';
import { Subject } from '../types';
import QuizCard from '../components/QuizCard';
import Button from '../components/Button';
import SubjectPicker from '../components/SubjectPicker';

export default function QuizScreen() {
  const router = useRouter();
  const params = useLocalSearchParams<{ subject?: Subject }>();

  const {
    state,
    getRandomQuestion,
    submitAnswer,
    startQuiz,
    endQuiz,
    resetQuiz,
    loadQuestions,
  } = useQuizStore();

  const { recordQuizResult } = useUserStore();

  const [selectedSubject, setSelectedSubject] = useState<Subject>(
    params.subject || 'general'
  );
  const [quizStarted, setQuizStarted] = useState(false);
  const [quizEnded, setQuizEnded] = useState(false);
  const [results, setResults] = useState({ correct: 0, total: 0 });

  useEffect(() => {
    loadQuestions(selectedSubject);
  }, [selectedSubject]);

  const handleStartQuiz = () => {
    startQuiz();
    getRandomQuestion(selectedSubject);
    setQuizStarted(true);
  };

  const handleAnswer = async (selectedIndex: number, isCorrect: boolean) => {
    await recordQuizResult(isCorrect);

    // Wait a moment, then show next question or end quiz
    setTimeout(() => {
      if (state.questionsAnswered >= 9) {
        // End quiz after 10 questions
        const quizResults = endQuiz();
        setResults({
          correct: state.correctAnswers + (isCorrect ? 1 : 0),
          total: state.questionsAnswered + 1,
        });
        setQuizEnded(true);
      } else {
        getRandomQuestion(selectedSubject);
      }
    }, 1500);
  };

  const handleRestartQuiz = () => {
    resetQuiz();
    setQuizStarted(false);
    setQuizEnded(false);
    setResults({ correct: 0, total: 0 });
  };

  const handleGoHome = () => {
    resetQuiz();
    router.replace('/');
  };

  // Quiz Results Screen
  if (quizEnded) {
    const percentage = Math.round((results.correct / results.total) * 100);
    const isPassing = percentage >= 70;

    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.resultsContainer}>
          <View
            style={[
              styles.resultIconContainer,
              { backgroundColor: isPassing ? COLORS.success + '20' : COLORS.warning + '20' },
            ]}
          >
            <Ionicons
              name={isPassing ? 'checkmark-circle' : 'refresh-circle'}
              size={80}
              color={isPassing ? COLORS.success : COLORS.warning}
            />
          </View>

          <Text style={styles.resultsTitle}>
            {isPassing ? 'Great Job!' : 'Keep Practicing!'}
          </Text>

          <Text style={styles.scoreText}>
            {results.correct} / {results.total}
          </Text>
          <Text style={styles.percentageText}>{percentage}% Correct</Text>

          <View style={styles.resultsButtons}>
            <Button
              title="Try Again"
              onPress={handleRestartQuiz}
              variant="outline"
              size="large"
              fullWidth
            />
            <Button
              title="Back to Home"
              onPress={handleGoHome}
              size="large"
              fullWidth
            />
          </View>
        </View>
      </SafeAreaView>
    );
  }

  // Quiz Start Screen
  if (!quizStarted) {
    return (
      <SafeAreaView style={styles.container}>
        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.startContainer}
        >
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => router.back()}
          >
            <Ionicons name="arrow-back" size={24} color={COLORS.text} />
          </TouchableOpacity>

          <View style={styles.startContent}>
            <View style={styles.quizIconContainer}>
              <Ionicons name="school" size={60} color={COLORS.primary} />
            </View>

            <Text style={styles.startTitle}>Practice Quiz</Text>
            <Text style={styles.startSubtitle}>
              Test your knowledge with 10 questions
            </Text>

            <View style={styles.subjectSection}>
              <Text style={styles.sectionLabel}>Choose a Subject</Text>
              <SubjectPicker
                selectedSubject={selectedSubject}
                onSelectSubject={setSelectedSubject}
                horizontal={false}
              />
            </View>

            <View style={styles.infoBox}>
              <View style={styles.infoItem}>
                <Ionicons name="help-circle-outline" size={20} color={COLORS.textSecondary} />
                <Text style={styles.infoText}>10 questions per quiz</Text>
              </View>
              <View style={styles.infoItem}>
                <Ionicons name="time-outline" size={20} color={COLORS.textSecondary} />
                <Text style={styles.infoText}>No time limit</Text>
              </View>
              <View style={styles.infoItem}>
                <Ionicons name="checkmark-circle-outline" size={20} color={COLORS.textSecondary} />
                <Text style={styles.infoText}>Instant feedback</Text>
              </View>
            </View>

            <Button
              title="Start Quiz"
              onPress={handleStartQuiz}
              size="large"
              fullWidth
            />
          </View>
        </ScrollView>
      </SafeAreaView>
    );
  }

  // Active Quiz Screen
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={handleGoHome} style={styles.closeButton}>
          <Ionicons name="close" size={24} color={COLORS.text} />
        </TouchableOpacity>
        <Text style={styles.progressText}>
          Question {state.questionsAnswered + 1} / 10
        </Text>
        <View style={styles.scoreDisplay}>
          <Text style={styles.scoreLabel}>{state.correctAnswers} correct</Text>
        </View>
      </View>

      <View style={styles.progressBar}>
        <View
          style={[
            styles.progressFill,
            { width: `${((state.questionsAnswered + 1) / 10) * 100}%` },
          ]}
        />
      </View>

      <View style={styles.quizContent}>
        {state.currentQuestion && (
          <QuizCard
            question={state.currentQuestion}
            onAnswer={handleAnswer}
            showPenaltyWarning={false}
          />
        )}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scrollView: {
    flex: 1,
  },
  backButton: {
    position: 'absolute',
    top: 16,
    left: 16,
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: COLORS.surface,
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 10,
  },
  startContainer: {
    flexGrow: 1,
    paddingTop: 60,
  },
  startContent: {
    flex: 1,
    alignItems: 'center',
    paddingHorizontal: 24,
    paddingTop: 40,
  },
  quizIconContainer: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: COLORS.primary + '15',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
  },
  startTitle: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 8,
  },
  startSubtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    marginBottom: 32,
  },
  subjectSection: {
    width: '100%',
    marginBottom: 24,
  },
  sectionLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.textSecondary,
    marginBottom: 12,
    paddingHorizontal: 16,
  },
  infoBox: {
    width: '100%',
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 16,
    marginBottom: 24,
    gap: 12,
  },
  infoItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  infoText: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  closeButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: COLORS.surface,
    alignItems: 'center',
    justifyContent: 'center',
  },
  progressText: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
  },
  scoreDisplay: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    backgroundColor: COLORS.success + '15',
    borderRadius: 12,
  },
  scoreLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.success,
  },
  progressBar: {
    height: 4,
    backgroundColor: COLORS.surfaceAlt,
    marginHorizontal: 16,
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: COLORS.primary,
    borderRadius: 2,
  },
  quizContent: {
    flex: 1,
    justifyContent: 'center',
    paddingVertical: 24,
  },
  resultsContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 24,
  },
  resultIconContainer: {
    width: 160,
    height: 160,
    borderRadius: 80,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
  },
  resultsTitle: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 16,
  },
  scoreText: {
    fontSize: 48,
    fontWeight: '700',
    color: COLORS.primary,
  },
  percentageText: {
    fontSize: 18,
    color: COLORS.textSecondary,
    marginBottom: 40,
  },
  resultsButtons: {
    width: '100%',
    gap: 12,
  },
});
