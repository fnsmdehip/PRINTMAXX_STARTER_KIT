import { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Pressable,
  Animated,
  Dimensions,
  ScrollView,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import {
  colors,
  spacing,
  borderRadius,
  typography,
  shadows,
} from '@/constants/theme';
import { useUserStore } from '@/store/userStore';
import Luna from '@/components/luna/Luna';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

interface GoalOption {
  id: string;
  label: string;
  description: string;
  icon: keyof typeof Ionicons.glyphMap;
}

interface FrequencyOption {
  id: string;
  label: string;
  description: string;
  weeklyGoal: number;
}

const goalOptions: GoalOption[] = [
  {
    id: 'tone',
    label: 'Tone up',
    description: 'Build lean muscle and definition',
    icon: 'body',
  },
  {
    id: 'strength',
    label: 'Build strength',
    description: 'Get stronger and more powerful',
    icon: 'barbell',
  },
  {
    id: 'active',
    label: 'Stay active',
    description: 'Maintain fitness and energy',
    icon: 'walk',
  },
  {
    id: 'weight',
    label: 'Lose weight',
    description: 'Burn calories and slim down',
    icon: 'flame',
  },
];

const frequencyOptions: FrequencyOption[] = [
  {
    id: 'new',
    label: 'New to fitness',
    description: 'Just getting started',
    weeklyGoal: 2,
  },
  {
    id: 'light',
    label: '1-2x per week',
    description: 'Casual workouts',
    weeklyGoal: 2,
  },
  {
    id: 'moderate',
    label: '3-4x per week',
    description: 'Building consistency',
    weeklyGoal: 4,
  },
  {
    id: 'daily',
    label: 'Daily',
    description: 'Committed athlete',
    weeklyGoal: 6,
  },
];

export default function GoalsScreen() {
  const router = useRouter();
  const { setProfile } = useUserStore();

  // Quiz state
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedGoal, setSelectedGoal] = useState<string | null>(null);
  const [selectedFrequency, setSelectedFrequency] = useState<string | null>(null);

  // Animation values
  const questionOpacity = useRef(new Animated.Value(1)).current;
  const questionTranslateX = useRef(new Animated.Value(0)).current;
  const progressWidth = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    // Animate progress bar
    Animated.timing(progressWidth, {
      toValue: ((currentQuestion + 1) / 2) * 100,
      duration: 300,
      useNativeDriver: false,
    }).start();
  }, [currentQuestion]);

  const animateToNextQuestion = () => {
    Animated.sequence([
      Animated.parallel([
        Animated.timing(questionOpacity, {
          toValue: 0,
          duration: 200,
          useNativeDriver: true,
        }),
        Animated.timing(questionTranslateX, {
          toValue: -50,
          duration: 200,
          useNativeDriver: true,
        }),
      ]),
    ]).start(() => {
      setCurrentQuestion(1);
      questionTranslateX.setValue(50);
      Animated.parallel([
        Animated.timing(questionOpacity, {
          toValue: 1,
          duration: 200,
          useNativeDriver: true,
        }),
        Animated.timing(questionTranslateX, {
          toValue: 0,
          duration: 200,
          useNativeDriver: true,
        }),
      ]).start();
    });
  };

  const handleGoalSelect = (goalId: string) => {
    setSelectedGoal(goalId);
  };

  const handleFrequencySelect = (frequencyId: string) => {
    setSelectedFrequency(frequencyId);
  };

  const handleContinue = () => {
    if (currentQuestion === 0 && selectedGoal) {
      animateToNextQuestion();
    } else if (currentQuestion === 1 && selectedFrequency) {
      // Save to store
      const frequency = frequencyOptions.find((f) => f.id === selectedFrequency);
      setProfile({
        goals: selectedGoal ? [selectedGoal] : [],
        weeklyGoal: frequency?.weeklyGoal || 4,
      });
      router.push('/(onboarding)/social-proof');
    }
  };

  const canContinue =
    (currentQuestion === 0 && selectedGoal) ||
    (currentQuestion === 1 && selectedFrequency);

  const getLunaState = () => {
    if (currentQuestion === 0) {
      return selectedGoal ? 'happy' : 'idle';
    }
    return selectedFrequency ? 'excited' : 'happy';
  };

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={[colors.primary + '20', colors.background]}
        style={styles.gradient}
      />

      <SafeAreaView style={styles.safeArea}>
        {/* Progress bar */}
        <View style={styles.progressContainer}>
          <View style={styles.progressTrack}>
            <Animated.View
              style={[
                styles.progressFill,
                {
                  width: progressWidth.interpolate({
                    inputRange: [0, 100],
                    outputRange: ['0%', '100%'],
                  }),
                },
              ]}
            />
          </View>
          <Text style={styles.progressText}>
            Question {currentQuestion + 1} of 2
          </Text>
        </View>

        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.content}
          showsVerticalScrollIndicator={false}
        >
          {/* Luna */}
          <View style={styles.lunaContainer}>
            <Luna state={getLunaState()} size={100} />
          </View>

          {/* Question content */}
          <Animated.View
            style={[
              styles.questionContainer,
              {
                opacity: questionOpacity,
                transform: [{ translateX: questionTranslateX }],
              },
            ]}
          >
            {currentQuestion === 0 ? (
              <>
                <Text style={styles.questionTitle}>What's your main goal?</Text>
                <Text style={styles.questionSubtitle}>
                  Pick what matters most to you
                </Text>

                <View style={styles.optionsGrid}>
                  {goalOptions.map((goal) => {
                    const isSelected = selectedGoal === goal.id;
                    return (
                      <Pressable
                        key={goal.id}
                        style={[
                          styles.optionCard,
                          isSelected && styles.optionCardSelected,
                        ]}
                        onPress={() => handleGoalSelect(goal.id)}
                      >
                        <View
                          style={[
                            styles.optionIconContainer,
                            isSelected && styles.optionIconContainerSelected,
                          ]}
                        >
                          <Ionicons
                            name={goal.icon}
                            size={28}
                            color={isSelected ? colors.surface : colors.primary}
                          />
                        </View>
                        <Text
                          style={[
                            styles.optionLabel,
                            isSelected && styles.optionLabelSelected,
                          ]}
                        >
                          {goal.label}
                        </Text>
                        <Text style={styles.optionDescription}>
                          {goal.description}
                        </Text>
                        {isSelected && (
                          <View style={styles.checkmark}>
                            <Ionicons
                              name="checkmark-circle"
                              size={24}
                              color={colors.primary}
                            />
                          </View>
                        )}
                      </Pressable>
                    );
                  })}
                </View>
              </>
            ) : (
              <>
                <Text style={styles.questionTitle}>
                  How often do you work out?
                </Text>
                <Text style={styles.questionSubtitle}>
                  We'll personalize your experience
                </Text>

                <View style={styles.optionsList}>
                  {frequencyOptions.map((freq) => {
                    const isSelected = selectedFrequency === freq.id;
                    return (
                      <Pressable
                        key={freq.id}
                        style={[
                          styles.frequencyCard,
                          isSelected && styles.frequencyCardSelected,
                        ]}
                        onPress={() => handleFrequencySelect(freq.id)}
                      >
                        <View style={styles.frequencyContent}>
                          <Text
                            style={[
                              styles.frequencyLabel,
                              isSelected && styles.frequencyLabelSelected,
                            ]}
                          >
                            {freq.label}
                          </Text>
                          <Text style={styles.frequencyDescription}>
                            {freq.description}
                          </Text>
                        </View>
                        <View
                          style={[
                            styles.radioOuter,
                            isSelected && styles.radioOuterSelected,
                          ]}
                        >
                          {isSelected && <View style={styles.radioInner} />}
                        </View>
                      </Pressable>
                    );
                  })}
                </View>
              </>
            )}
          </Animated.View>
        </ScrollView>

        {/* CTA Button */}
        <View style={styles.ctaContainer}>
          <Pressable
            style={({ pressed }) => [
              styles.ctaButton,
              pressed && styles.ctaButtonPressed,
              !canContinue && styles.ctaButtonDisabled,
            ]}
            onPress={handleContinue}
            disabled={!canContinue}
          >
            <Text style={styles.ctaText}>Continue</Text>
            <Ionicons name="arrow-forward" size={20} color={colors.surface} />
          </Pressable>
        </View>
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  gradient: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: 300,
  },
  safeArea: {
    flex: 1,
  },
  progressContainer: {
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.md,
    alignItems: 'center',
  },
  progressTrack: {
    width: '100%',
    height: 6,
    backgroundColor: colors.border,
    borderRadius: 3,
    overflow: 'hidden',
    marginBottom: spacing.sm,
  },
  progressFill: {
    height: '100%',
    backgroundColor: colors.primary,
    borderRadius: 3,
  },
  progressText: {
    ...typography.small,
    color: colors.textMuted,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    paddingHorizontal: spacing.lg,
    paddingBottom: 120,
  },
  lunaContainer: {
    alignItems: 'center',
    marginVertical: spacing.lg,
  },
  questionContainer: {
    alignItems: 'center',
  },
  questionTitle: {
    ...typography.h1,
    color: colors.text,
    textAlign: 'center',
    marginBottom: spacing.sm,
  },
  questionSubtitle: {
    ...typography.body,
    color: colors.textLight,
    textAlign: 'center',
    marginBottom: spacing.xl,
  },
  optionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.md,
    justifyContent: 'center',
  },
  optionCard: {
    width: (SCREEN_WIDTH - spacing.lg * 2 - spacing.md) / 2,
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    borderWidth: 2,
    borderColor: colors.border,
    alignItems: 'center',
    ...shadows.sm,
  },
  optionCardSelected: {
    borderColor: colors.primary,
    backgroundColor: colors.primary + '08',
  },
  optionIconContainer: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: colors.primary + '15',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.sm,
  },
  optionIconContainerSelected: {
    backgroundColor: colors.primary,
  },
  optionLabel: {
    ...typography.bodyBold,
    color: colors.text,
    textAlign: 'center',
    marginBottom: spacing.xs,
  },
  optionLabelSelected: {
    color: colors.primary,
  },
  optionDescription: {
    ...typography.small,
    color: colors.textMuted,
    textAlign: 'center',
  },
  checkmark: {
    position: 'absolute',
    top: spacing.sm,
    right: spacing.sm,
  },
  optionsList: {
    width: '100%',
    gap: spacing.sm,
  },
  frequencyCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    borderWidth: 2,
    borderColor: colors.border,
    ...shadows.sm,
  },
  frequencyCardSelected: {
    borderColor: colors.primary,
    backgroundColor: colors.primary + '08',
  },
  frequencyContent: {
    flex: 1,
  },
  frequencyLabel: {
    ...typography.bodyBold,
    color: colors.text,
  },
  frequencyLabelSelected: {
    color: colors.primary,
  },
  frequencyDescription: {
    ...typography.caption,
    color: colors.textMuted,
    marginTop: 2,
  },
  radioOuter: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: colors.border,
    alignItems: 'center',
    justifyContent: 'center',
  },
  radioOuterSelected: {
    borderColor: colors.primary,
  },
  radioInner: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: colors.primary,
  },
  ctaContainer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    padding: spacing.lg,
    paddingBottom: spacing.xl,
    backgroundColor: colors.background,
  },
  ctaButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.primary,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    gap: spacing.sm,
    ...shadows.md,
  },
  ctaButtonPressed: {
    opacity: 0.9,
  },
  ctaButtonDisabled: {
    opacity: 0.5,
  },
  ctaText: {
    ...typography.bodyBold,
    color: colors.surface,
    fontSize: 18,
  },
});
