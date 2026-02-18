import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Animated,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import { useRouter } from 'expo-router';
import * as SecureStore from 'expo-secure-store';
import * as Haptics from 'expo-haptics';
import { Ionicons } from '@expo/vector-icons';
import { useStore } from '../../src/lib/store';

const { width, height } = Dimensions.get('window');

interface OnboardingSlide {
  icon: keyof typeof Ionicons.glyphMap;
  iconColor: string;
  bgGradient: string[];
  title: string;
  subtitle: string;
}

const slides: OnboardingSlide[] = [
  { 
    icon: 'book',
    iconColor: '#e94560',
    bgGradient: ['#e9456020', '#e9456005'],
    title: 'Welcome to\nScripture Streak', 
    subtitle: 'Build your daily Bible reading habit and grow closer to God' 
  },
  { 
    icon: 'sunny',
    iconColor: '#fbbf24',
    bgGradient: ['#fbbf2420', '#fbbf2405'],
    title: 'Daily Inspiration', 
    subtitle: 'Receive a handpicked verse every morning to start your day' 
  },
  { 
    icon: 'flame',
    iconColor: '#f97316',
    bgGradient: ['#f9731620', '#f9731605'],
    title: 'Build Your Streak', 
    subtitle: "Stay consistent and watch your streak grow. Don't break the chain!" 
  },
  { 
    icon: 'rocket',
    iconColor: '#4ade80',
    bgGradient: ['#4ade8020', '#4ade8005'],
    title: "Let's Begin", 
    subtitle: 'Start your spiritual journey today. Your future self will thank you.' 
  },
];

export default function OnboardingScreen() {
  const router = useRouter();
  const { setHasCompletedOnboarding } = useStore();
  const [step, setStep] = useState(0);
  
  // Animations
  const fadeAnim = useRef(new Animated.Value(1)).current;
  const scaleAnim = useRef(new Animated.Value(1)).current;
  const iconAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(0)).current;
  
  useEffect(() => {
    // Initial icon animation
    Animated.spring(iconAnim, {
      toValue: 1,
      tension: 50,
      friction: 5,
      useNativeDriver: true,
    }).start();
  }, []);

  const animateTransition = (callback: () => void) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 0,
        duration: 150,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: -50,
        duration: 150,
        useNativeDriver: true,
      }),
    ]).start(() => {
      callback();
      slideAnim.setValue(50);
      Animated.parallel([
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 200,
          useNativeDriver: true,
        }),
        Animated.spring(slideAnim, {
          toValue: 0,
          tension: 50,
          friction: 8,
          useNativeDriver: true,
        }),
        Animated.spring(iconAnim, {
          toValue: 1,
          tension: 50,
          friction: 5,
          useNativeDriver: true,
        }),
      ]).start();
    });
  };

  const handleContinue = async () => {
    if (step < slides.length - 1) {
      iconAnim.setValue(0);
      animateTransition(() => setStep(step + 1));
    } else {
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      
      // Pulse animation before navigating
      Animated.sequence([
        Animated.timing(scaleAnim, { toValue: 0.95, duration: 100, useNativeDriver: true }),
        Animated.timing(scaleAnim, { toValue: 1, duration: 100, useNativeDriver: true }),
      ]).start(async () => {
        try {
          await SecureStore.setItemAsync('onboarding_completed', 'true');
        } catch (e) {
          console.log('Storage error:', e);
        }
        setHasCompletedOnboarding(true);
        router.replace('/paywall');
      });
    }
  };

  const handleSkip = async () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    try {
      await SecureStore.setItemAsync('onboarding_completed', 'true');
    } catch (e) {
      console.log('Storage error:', e);
    }
    setHasCompletedOnboarding(true);
    router.replace('/paywall');
  };

  const current = slides[step];

  return (
    <LinearGradient
      colors={['#1a1a2e', '#0f0f23', '#1a1a2e']}
      style={styles.container}
    >
      <SafeAreaView style={styles.safeArea}>
        {/* Skip button */}
        <TouchableOpacity style={styles.skipButton} onPress={handleSkip}>
          <Text style={styles.skipText}>Skip</Text>
        </TouchableOpacity>

        {/* Content */}
        <Animated.View 
          style={[
            styles.content,
            { 
              opacity: fadeAnim,
              transform: [{ translateX: slideAnim }],
            }
          ]}
        >
          {/* Icon container with gradient background */}
          <Animated.View 
            style={[
              styles.iconWrapper,
              {
                transform: [
                  { 
                    scale: iconAnim.interpolate({
                      inputRange: [0, 1],
                      outputRange: [0.5, 1],
                    })
                  },
                  {
                    rotate: iconAnim.interpolate({
                      inputRange: [0, 1],
                      outputRange: ['-15deg', '0deg'],
                    })
                  },
                ],
              }
            ]}
          >
            <LinearGradient
              colors={current.bgGradient}
              style={styles.iconGradient}
            >
              <Ionicons name={current.icon} size={80} color={current.iconColor} />
            </LinearGradient>
          </Animated.View>

          <Text style={styles.title}>{current.title}</Text>
          <Text style={styles.subtitle}>{current.subtitle}</Text>
        </Animated.View>

        {/* Progress dots */}
        <View style={styles.dotsContainer}>
          {slides.map((_, i) => (
            <Animated.View
              key={i}
              style={[
                styles.dot,
                i === step && styles.dotActive,
                i === step && { backgroundColor: current.iconColor },
              ]}
            />
          ))}
        </View>

        {/* Continue button */}
        <Animated.View style={{ transform: [{ scale: scaleAnim }] }}>
          <TouchableOpacity
            style={styles.continueButton}
            onPress={handleContinue}
            activeOpacity={0.8}
          >
            <LinearGradient
              colors={['#e94560', '#c23a51']}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
              style={styles.continueGradient}
            >
              <Text style={styles.continueText}>
                {step === slides.length - 1 ? "Let's Go!" : 'Continue'}
              </Text>
              <Ionicons 
                name={step === slides.length - 1 ? "rocket" : "arrow-forward"} 
                size={22} 
                color="#ffffff" 
              />
            </LinearGradient>
          </TouchableOpacity>
        </Animated.View>

        {/* Step counter */}
        <Text style={styles.stepCounter}>{step + 1} of {slides.length}</Text>
      </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  safeArea: {
    flex: 1,
    paddingHorizontal: 24,
  },
  skipButton: {
    alignSelf: 'flex-end',
    paddingHorizontal: 20,
    paddingVertical: 12,
    backgroundColor: 'rgba(255,255,255,0.08)',
    borderRadius: 24,
    marginTop: 10,
  },
  skipText: {
    color: '#ffffff80',
    fontSize: 16,
    fontWeight: '600',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  iconWrapper: {
    marginBottom: 40,
  },
  iconGradient: {
    width: 160,
    height: 160,
    borderRadius: 80,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'rgba(255,255,255,0.1)',
  },
  title: {
    fontSize: 34,
    fontWeight: '800',
    color: '#ffffff',
    textAlign: 'center',
    marginBottom: 16,
    lineHeight: 42,
  },
  subtitle: {
    fontSize: 17,
    color: 'rgba(255,255,255,0.6)',
    textAlign: 'center',
    lineHeight: 26,
    paddingHorizontal: 10,
  },
  dotsContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginBottom: 32,
    gap: 10,
  },
  dot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: 'rgba(255,255,255,0.2)',
  },
  dotActive: {
    width: 32,
  },
  continueButton: {
    borderRadius: 18,
    overflow: 'hidden',
    marginBottom: 16,
  },
  continueGradient: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 20,
    gap: 10,
  },
  continueText: {
    color: '#ffffff',
    fontSize: 19,
    fontWeight: '700',
  },
  stepCounter: {
    color: 'rgba(255,255,255,0.3)',
    textAlign: 'center',
    fontSize: 13,
    marginBottom: 20,
    fontWeight: '600',
  },
});
