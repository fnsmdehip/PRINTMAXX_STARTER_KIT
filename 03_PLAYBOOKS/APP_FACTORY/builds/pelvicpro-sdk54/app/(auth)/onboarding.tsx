import { useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Pressable,
  Dimensions,
  FlatList,
  TextInput,
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
} from '@/constants/theme';
import { useUserStore } from '@/store/userStore';
import Luna from '@/components/luna/Luna';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

interface OnboardingSlide {
  id: string;
  type: 'intro' | 'goals' | 'frequency' | 'name' | 'ready';
  title: string;
  subtitle?: string;
  lunaState: 'waving' | 'idle' | 'happy' | 'excited' | 'celebrating';
}

const slides: OnboardingSlide[] = [
  {
    id: '1',
    type: 'intro',
    title: 'Meet Luna',
    subtitle: "Your workout bestie. She's here to cheer you on!",
    lunaState: 'waving',
  },
  {
    id: '2',
    type: 'goals',
    title: "What's your goal?",
    subtitle: 'Pick what matters most to you',
    lunaState: 'idle',
  },
  {
    id: '3',
    type: 'frequency',
    title: 'How often do you work out?',
    subtitle: "We'll set your weekly goal",
    lunaState: 'happy',
  },
  {
    id: '4',
    type: 'name',
    title: "What's your name?",
    subtitle: 'So Luna knows what to call you',
    lunaState: 'excited',
  },
  {
    id: '5',
    type: 'ready',
    title: "You're all set!",
    subtitle: "Let's start your fitness journey together",
    lunaState: 'celebrating',
  },
];

const goals = [
  { id: 'glutes', label: 'Build glutes', icon: 'fitness' },
  { id: 'tone', label: 'Tone up', icon: 'body' },
  { id: 'strength', label: 'Get stronger', icon: 'barbell' },
  { id: 'general', label: 'General fitness', icon: 'heart' },
];

const frequencies = [
  { id: 2, label: '1-2 times', description: 'Just getting started' },
  { id: 4, label: '3-4 times', description: 'Building consistency' },
  { id: 6, label: '5+ times', description: 'Serious about gains' },
];

export default function OnboardingScreen() {
  const router = useRouter();
  const flatListRef = useRef<FlatList>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedGoals, setSelectedGoals] = useState<string[]>([]);
  const [weeklyGoal, setWeeklyGoal] = useState(4);
  const [name, setName] = useState('');

  const { setProfile, completeOnboarding, startTrial } = useUserStore();

  const goToNext = () => {
    if (currentIndex < slides.length - 1) {
      flatListRef.current?.scrollToIndex({ index: currentIndex + 1 });
      setCurrentIndex(currentIndex + 1);
    }
  };

  const handleGoalToggle = (goalId: string) => {
    setSelectedGoals((prev) =>
      prev.includes(goalId)
        ? prev.filter((g) => g !== goalId)
        : [...prev, goalId]
    );
  };

  const handleComplete = () => {
    setProfile({
      name: name.trim(),
      goals: selectedGoals,
      weeklyGoal,
    });
    completeOnboarding();
    startTrial();
    router.replace('/paywall');
  };

  const canProceed = () => {
    const slide = slides[currentIndex];
    switch (slide.type) {
      case 'goals':
        return selectedGoals.length > 0;
      case 'name':
        return true; // Name is optional
      default:
        return true;
    }
  };

  const renderSlide = ({ item }: { item: OnboardingSlide }) => {
    return (
      <View style={styles.slide}>
        <View style={styles.lunaContainer}>
          <Luna state={item.lunaState} size={120} />
        </View>

        <Text style={styles.title}>{item.title}</Text>
        {item.subtitle && <Text style={styles.subtitle}>{item.subtitle}</Text>}

        {/* Goals Selection */}
        {item.type === 'goals' && (
          <View style={styles.optionsContainer}>
            {goals.map((goal) => {
              const isSelected = selectedGoals.includes(goal.id);
              return (
                <Pressable
                  key={goal.id}
                  style={[
                    styles.optionCard,
                    isSelected && styles.optionCardSelected,
                  ]}
                  onPress={() => handleGoalToggle(goal.id)}
                >
                  <Ionicons
                    name={goal.icon as any}
                    size={24}
                    color={isSelected ? colors.primary : colors.textLight}
                  />
                  <Text
                    style={[
                      styles.optionLabel,
                      isSelected && styles.optionLabelSelected,
                    ]}
                  >
                    {goal.label}
                  </Text>
                  {isSelected && (
                    <Ionicons
                      name="checkmark-circle"
                      size={24}
                      color={colors.primary}
                    />
                  )}
                </Pressable>
              );
            })}
          </View>
        )}

        {/* Frequency Selection */}
        {item.type === 'frequency' && (
          <View style={styles.optionsContainer}>
            {frequencies.map((freq) => {
              const isSelected = weeklyGoal === freq.id;
              return (
                <Pressable
                  key={freq.id}
                  style={[
                    styles.optionCard,
                    isSelected && styles.optionCardSelected,
                  ]}
                  onPress={() => setWeeklyGoal(freq.id)}
                >
                  <View style={styles.freqInfo}>
                    <Text
                      style={[
                        styles.optionLabel,
                        isSelected && styles.optionLabelSelected,
                      ]}
                    >
                      {freq.label}
                    </Text>
                    <Text style={styles.freqDescription}>{freq.description}</Text>
                  </View>
                  {isSelected && (
                    <Ionicons
                      name="checkmark-circle"
                      size={24}
                      color={colors.primary}
                    />
                  )}
                </Pressable>
              );
            })}
          </View>
        )}

        {/* Name Input */}
        {item.type === 'name' && (
          <View style={styles.nameContainer}>
            <TextInput
              style={styles.nameInput}
              placeholder="Enter your name"
              placeholderTextColor={colors.textMuted}
              value={name}
              onChangeText={setName}
              autoCapitalize="words"
              autoCorrect={false}
            />
            <Text style={styles.nameHint}>Or skip and stay mysterious</Text>
          </View>
        )}

        {/* Ready Screen */}
        {item.type === 'ready' && (
          <View style={styles.readyContainer}>
            <View style={styles.readyStat}>
              <Ionicons name="flag" size={24} color={colors.primary} />
              <Text style={styles.readyStatText}>
                Goal: {weeklyGoal}x per week
              </Text>
            </View>
            {selectedGoals.length > 0 && (
              <View style={styles.readyStat}>
                <Ionicons name="star" size={24} color={colors.warning} />
                <Text style={styles.readyStatText}>
                  Focus:{' '}
                  {selectedGoals
                    .map((g) => goals.find((goal) => goal.id === g)?.label)
                    .join(', ')}
                </Text>
              </View>
            )}
          </View>
        )}
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={[colors.primary + '20', colors.background]}
        style={styles.gradient}
      />

      <SafeAreaView style={styles.safeArea}>
        {/* Progress Dots */}
        <View style={styles.progressContainer}>
          {slides.map((_, index) => (
            <View
              key={index}
              style={[
                styles.progressDot,
                index === currentIndex && styles.progressDotActive,
                index < currentIndex && styles.progressDotComplete,
              ]}
            />
          ))}
        </View>

        {/* Slides */}
        <FlatList
          ref={flatListRef}
          data={slides}
          renderItem={renderSlide}
          horizontal
          pagingEnabled
          scrollEnabled={false}
          showsHorizontalScrollIndicator={false}
          keyExtractor={(item) => item.id}
          onMomentumScrollEnd={(e) => {
            const index = Math.round(
              e.nativeEvent.contentOffset.x / SCREEN_WIDTH
            );
            setCurrentIndex(index);
          }}
        />

        {/* CTA Button */}
        <View style={styles.ctaContainer}>
          <Pressable
            style={({ pressed }) => [
              styles.ctaButton,
              pressed && styles.ctaButtonPressed,
              !canProceed() && styles.ctaButtonDisabled,
            ]}
            onPress={
              currentIndex === slides.length - 1 ? handleComplete : goToNext
            }
            disabled={!canProceed()}
          >
            <Text style={styles.ctaText}>
              {currentIndex === slides.length - 1 ? "Let's Go!" : 'Continue'}
            </Text>
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
    height: 400,
  },
  safeArea: {
    flex: 1,
  },
  progressContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    paddingVertical: spacing.lg,
    gap: spacing.sm,
  },
  progressDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: colors.border,
  },
  progressDotActive: {
    width: 24,
    backgroundColor: colors.primary,
  },
  progressDotComplete: {
    backgroundColor: colors.primary,
  },
  slide: {
    width: SCREEN_WIDTH,
    paddingHorizontal: spacing.lg,
    alignItems: 'center',
  },
  lunaContainer: {
    marginVertical: spacing.xl,
  },
  title: {
    ...typography.h1,
    color: colors.text,
    textAlign: 'center',
    marginBottom: spacing.sm,
  },
  subtitle: {
    ...typography.body,
    color: colors.textLight,
    textAlign: 'center',
    marginBottom: spacing.xl,
  },
  optionsContainer: {
    width: '100%',
    gap: spacing.sm,
  },
  optionCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    borderWidth: 2,
    borderColor: colors.border,
    gap: spacing.md,
  },
  optionCardSelected: {
    borderColor: colors.primary,
    backgroundColor: colors.primary + '08',
  },
  optionLabel: {
    ...typography.bodyBold,
    color: colors.text,
    flex: 1,
  },
  optionLabelSelected: {
    color: colors.primary,
  },
  freqInfo: {
    flex: 1,
  },
  freqDescription: {
    ...typography.caption,
    color: colors.textMuted,
    marginTop: 2,
  },
  nameContainer: {
    width: '100%',
    alignItems: 'center',
  },
  nameInput: {
    width: '100%',
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    borderWidth: 2,
    borderColor: colors.border,
    ...typography.body,
    color: colors.text,
    textAlign: 'center',
  },
  nameHint: {
    ...typography.caption,
    color: colors.textMuted,
    marginTop: spacing.sm,
  },
  readyContainer: {
    width: '100%',
    gap: spacing.md,
  },
  readyStat: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    gap: spacing.md,
  },
  readyStatText: {
    ...typography.body,
    color: colors.text,
    flex: 1,
  },
  ctaContainer: {
    padding: spacing.lg,
    paddingBottom: spacing.xl,
  },
  ctaButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.primary,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    gap: spacing.sm,
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
