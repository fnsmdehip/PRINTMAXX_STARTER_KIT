import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import * as Haptics from 'expo-haptics';
import Animated, {
  useAnimatedStyle,
  withSequence,
  withTiming,
  withSpring,
} from 'react-native-reanimated';
import { COLORS } from '../utils/constants';
import { QuizQuestion } from '../types';
import Card from './Card';
import Button from './Button';

interface QuizCardProps {
  question: QuizQuestion;
  onAnswer: (selectedIndex: number, isCorrect: boolean) => void;
  showPenaltyWarning?: boolean;
  penaltyMinutes?: number;
}

export const QuizCard: React.FC<QuizCardProps> = ({
  question,
  onAnswer,
  showPenaltyWarning = true,
  penaltyMinutes = 5,
}) => {
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);
  const [hasAnswered, setHasAnswered] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);

  const handleSelectOption = (index: number) => {
    if (hasAnswered) return;
    setSelectedIndex(index);
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  };

  const handleSubmit = () => {
    if (selectedIndex === null || hasAnswered) return;

    const correct = selectedIndex === question.correctAnswer;
    setIsCorrect(correct);
    setHasAnswered(true);

    if (correct) {
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    } else {
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    }

    // Small delay before calling onAnswer to show result
    setTimeout(() => {
      onAnswer(selectedIndex, correct);
    }, 1500);
  };

  const getOptionStyle = (index: number) => {
    if (!hasAnswered) {
      return selectedIndex === index ? styles.optionSelected : styles.option;
    }

    if (index === question.correctAnswer) {
      return [styles.option, styles.optionCorrect];
    }

    if (index === selectedIndex && !isCorrect) {
      return [styles.option, styles.optionIncorrect];
    }

    return styles.option;
  };

  const getOptionTextStyle = (index: number) => {
    if (!hasAnswered) {
      return selectedIndex === index ? styles.optionTextSelected : styles.optionText;
    }

    if (index === question.correctAnswer || (index === selectedIndex && !isCorrect)) {
      return [styles.optionText, styles.optionTextResult];
    }

    return styles.optionText;
  };

  return (
    <Card variant="elevated" padding="large" style={styles.card}>
      {showPenaltyWarning && (
        <View style={styles.warningBanner}>
          <Text style={styles.warningText}>
            Wrong answer adds {penaltyMinutes} minutes!
          </Text>
        </View>
      )}

      <Text style={styles.questionLabel}>Knowledge Check</Text>
      <Text style={styles.question}>{question.question}</Text>

      <View style={styles.options}>
        {question.options.map((option, index) => (
          <TouchableOpacity
            key={index}
            style={getOptionStyle(index)}
            onPress={() => handleSelectOption(index)}
            disabled={hasAnswered}
            activeOpacity={0.8}
          >
            <View style={styles.optionIndicator}>
              <Text style={styles.optionLetter}>
                {String.fromCharCode(65 + index)}
              </Text>
            </View>
            <Text style={getOptionTextStyle(index)}>{option}</Text>
          </TouchableOpacity>
        ))}
      </View>

      {hasAnswered ? (
        <View style={[styles.resultBanner, isCorrect ? styles.correctBanner : styles.incorrectBanner]}>
          <Text style={styles.resultText}>
            {isCorrect ? 'Correct!' : `Incorrect! +${penaltyMinutes} minutes added`}
          </Text>
        </View>
      ) : (
        <Button
          title="Submit Answer"
          onPress={handleSubmit}
          disabled={selectedIndex === null}
          fullWidth
          size="large"
        />
      )}
    </Card>
  );
};

const styles = StyleSheet.create({
  card: {
    marginHorizontal: 16,
  },
  warningBanner: {
    backgroundColor: COLORS.warning + '20',
    padding: 8,
    borderRadius: 8,
    marginBottom: 16,
  },
  warningText: {
    color: COLORS.warning,
    fontSize: 13,
    fontWeight: '600',
    textAlign: 'center',
  },
  questionLabel: {
    fontSize: 12,
    color: COLORS.primary,
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: 8,
  },
  question: {
    fontSize: 20,
    fontWeight: '600',
    color: COLORS.text,
    lineHeight: 28,
    marginBottom: 24,
  },
  options: {
    gap: 12,
    marginBottom: 24,
  },
  option: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    borderRadius: 12,
    backgroundColor: COLORS.surface,
    borderWidth: 2,
    borderColor: COLORS.surface,
  },
  optionSelected: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    borderRadius: 12,
    backgroundColor: COLORS.primary + '10',
    borderWidth: 2,
    borderColor: COLORS.primary,
  },
  optionCorrect: {
    backgroundColor: COLORS.success + '15',
    borderColor: COLORS.success,
  },
  optionIncorrect: {
    backgroundColor: COLORS.error + '15',
    borderColor: COLORS.error,
  },
  optionIndicator: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: COLORS.surfaceAlt,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
  },
  optionLetter: {
    fontSize: 14,
    fontWeight: '700',
    color: COLORS.textSecondary,
  },
  optionText: {
    flex: 1,
    fontSize: 16,
    color: COLORS.text,
  },
  optionTextSelected: {
    flex: 1,
    fontSize: 16,
    color: COLORS.primary,
    fontWeight: '600',
  },
  optionTextResult: {
    fontWeight: '600',
    color: COLORS.white,
  },
  resultBanner: {
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  correctBanner: {
    backgroundColor: COLORS.success,
  },
  incorrectBanner: {
    backgroundColor: COLORS.error,
  },
  resultText: {
    color: COLORS.white,
    fontSize: 16,
    fontWeight: '700',
  },
});

export default QuizCard;
