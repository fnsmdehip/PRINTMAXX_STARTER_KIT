import { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Dimensions,
  ScrollView,
} from 'react-native';
import { router } from 'expo-router';
import { useUserStore } from '../src/stores/userStore';

const { width } = Dimensions.get('window');

const slides = [
  {
    title: 'Start Your Day Right',
    description: 'Block distracting apps until you complete your morning devotional.',
    icon: '🙏',
  },
  {
    title: 'Build a Prayer Habit',
    description: 'Set a timer for your daily prayer and watch your streak grow.',
    icon: '⏱️',
  },
  {
    title: 'Read Scripture Daily',
    description: 'Engage with God\'s Word before the world floods your feed.',
    icon: '📖',
  },
  {
    title: 'Track Your Progress',
    description: 'See your streak, stay motivated, and grow in faith.',
    icon: '📈',
  },
];

export default function Onboarding() {
  const [currentSlide, setCurrentSlide] = useState(0);
  const setHasCompletedOnboarding = useUserStore((state) => state.setHasCompletedOnboarding);
  const startTrial = useUserStore((state) => state.startTrial);

  const handleNext = () => {
    if (currentSlide < slides.length - 1) {
      setCurrentSlide(currentSlide + 1);
    } else {
      // Start trial and complete onboarding
      startTrial();
      setHasCompletedOnboarding(true);
      router.replace('/(tabs)');
    }
  };

  const handleSkip = () => {
    startTrial();
    setHasCompletedOnboarding(true);
    router.replace('/(tabs)');
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.skipButton} onPress={handleSkip}>
        <Text style={styles.skipText}>Skip</Text>
      </TouchableOpacity>

      <View style={styles.slideContainer}>
        <Text style={styles.icon}>{slides[currentSlide].icon}</Text>
        <Text style={styles.title}>{slides[currentSlide].title}</Text>
        <Text style={styles.description}>{slides[currentSlide].description}</Text>
      </View>

      <View style={styles.pagination}>
        {slides.map((_, index) => (
          <View
            key={index}
            style={[
              styles.dot,
              index === currentSlide && styles.dotActive,
            ]}
          />
        ))}
      </View>

      <TouchableOpacity style={styles.nextButton} onPress={handleNext}>
        <Text style={styles.nextText}>
          {currentSlide === slides.length - 1 ? 'Get Started' : 'Next'}
        </Text>
      </TouchableOpacity>

      {currentSlide === slides.length - 1 && (
        <Text style={styles.trialNote}>
          Start your 3-day free trial. Cancel anytime.
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
    paddingHorizontal: 24,
    paddingTop: 60,
    paddingBottom: 40,
  },
  skipButton: {
    alignSelf: 'flex-end',
    padding: 8,
  },
  skipText: {
    color: '#8b8b9e',
    fontSize: 16,
  },
  slideContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  icon: {
    fontSize: 80,
    marginBottom: 32,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    marginBottom: 16,
  },
  description: {
    fontSize: 18,
    color: '#b0b0c0',
    textAlign: 'center',
    lineHeight: 26,
  },
  pagination: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginBottom: 32,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#3a3a5e',
    marginHorizontal: 4,
  },
  dotActive: {
    backgroundColor: '#6c63ff',
    width: 24,
  },
  nextButton: {
    backgroundColor: '#6c63ff',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 16,
  },
  nextText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  trialNote: {
    color: '#8b8b9e',
    fontSize: 14,
    textAlign: 'center',
  },
});
