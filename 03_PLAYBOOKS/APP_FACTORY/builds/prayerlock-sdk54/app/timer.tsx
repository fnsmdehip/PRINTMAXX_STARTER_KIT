import { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Vibration } from 'react-native';
import { router } from 'expo-router';
import * as Haptics from 'expo-haptics';
import { useUserStore } from '../src/stores/userStore';
import { useDevotionStore } from '../src/stores/devotionStore';

export default function Timer() {
  const settings = useUserStore((state) => state.settings);
  const startSession = useDevotionStore((state) => state.startSession);
  const completeSession = useDevotionStore((state) => state.completeSession);
  const currentSession = useDevotionStore((state) => state.currentSession);

  const totalSeconds = settings.devotionDurationMinutes * 60;
  const [timeLeft, setTimeLeft] = useState(totalSeconds);
  const [isRunning, setIsRunning] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (isRunning && timeLeft > 0) {
      intervalRef.current = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            handleComplete();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isRunning]);

  const handleStart = () => {
    startSession();
    setIsRunning(true);
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
  };

  const handleComplete = async () => {
    setIsRunning(false);
    setIsComplete(true);

    // Haptic feedback
    await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

    // Complete the session
    completeSession(true, false);
  };

  const handleContinue = () => {
    const requiresScripture = settings.requireScripture;
    if (requiresScripture) {
      router.replace('/scripture');
    } else {
      router.replace('/(tabs)');
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const progress = 1 - timeLeft / totalSeconds;

  return (
    <View style={styles.container}>
      {!isRunning && !isComplete && (
        <>
          <View style={styles.header}>
            <Text style={styles.title}>Prayer Time</Text>
            <Text style={styles.subtitle}>
              Set aside {settings.devotionDurationMinutes} minutes to pray
            </Text>
          </View>

          <View style={styles.timerContainer}>
            <View style={styles.timerCircle}>
              <Text style={styles.timerText}>{formatTime(timeLeft)}</Text>
            </View>
          </View>

          <TouchableOpacity style={styles.startButton} onPress={handleStart}>
            <Text style={styles.startButtonText}>Begin Prayer</Text>
          </TouchableOpacity>

          <Text style={styles.hint}>
            Find a quiet place, close your eyes, and talk to God
          </Text>
        </>
      )}

      {isRunning && (
        <>
          <View style={styles.prayingHeader}>
            <Text style={styles.prayingTitle}>In Prayer</Text>
            <Text style={styles.prayingSubtitle}>
              Stay focused. God is listening.
            </Text>
          </View>

          <View style={styles.timerContainer}>
            <View style={styles.timerCircleActive}>
              <Text style={styles.timerTextLarge}>{formatTime(timeLeft)}</Text>
              <Text style={styles.remaining}>remaining</Text>
            </View>
          </View>

          <View style={styles.progressBar}>
            <View style={[styles.progressFill, { width: `${progress * 100}%` }]} />
          </View>

          <Text style={styles.encouragement}>
            {timeLeft > totalSeconds * 0.75
              ? "You're doing great. Keep praying."
              : timeLeft > totalSeconds * 0.5
              ? "Halfway there. Stay focused."
              : timeLeft > totalSeconds * 0.25
              ? "Almost done. Finish strong."
              : "Just a little more. You've got this."}
          </Text>
        </>
      )}

      {isComplete && (
        <>
          <View style={styles.completeHeader}>
            <Text style={styles.completeEmoji}>🙏</Text>
            <Text style={styles.completeTitle}>Prayer Complete</Text>
            <Text style={styles.completeSubtitle}>
              {settings.devotionDurationMinutes} minutes with God
            </Text>
          </View>

          <TouchableOpacity style={styles.continueButton} onPress={handleContinue}>
            <Text style={styles.continueButtonText}>
              {settings.requireScripture ? 'Continue to Scripture' : 'Finish'}
            </Text>
          </TouchableOpacity>
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
    paddingHorizontal: 24,
    paddingTop: 40,
  },
  header: {
    alignItems: 'center',
    marginBottom: 48,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#8b8b9e',
    textAlign: 'center',
  },
  timerContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    flex: 1,
    marginBottom: 48,
  },
  timerCircle: {
    width: 250,
    height: 250,
    borderRadius: 125,
    backgroundColor: '#2a2a4e',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 4,
    borderColor: '#3a3a5e',
  },
  timerCircleActive: {
    width: 250,
    height: 250,
    borderRadius: 125,
    backgroundColor: '#2a2a4e',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 4,
    borderColor: '#6c63ff',
  },
  timerText: {
    fontSize: 48,
    fontWeight: '300',
    color: '#fff',
  },
  timerTextLarge: {
    fontSize: 56,
    fontWeight: '300',
    color: '#fff',
  },
  remaining: {
    fontSize: 14,
    color: '#8b8b9e',
    marginTop: 8,
  },
  startButton: {
    backgroundColor: '#6c63ff',
    paddingVertical: 18,
    borderRadius: 16,
    alignItems: 'center',
    marginBottom: 24,
  },
  startButtonText: {
    color: '#fff',
    fontSize: 20,
    fontWeight: '600',
  },
  hint: {
    color: '#8b8b9e',
    fontSize: 14,
    textAlign: 'center',
    paddingBottom: 40,
  },
  prayingHeader: {
    alignItems: 'center',
    marginBottom: 48,
  },
  prayingTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#6c63ff',
    marginBottom: 8,
  },
  prayingSubtitle: {
    fontSize: 16,
    color: '#8b8b9e',
  },
  progressBar: {
    height: 8,
    backgroundColor: '#2a2a4e',
    borderRadius: 4,
    marginBottom: 24,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#6c63ff',
    borderRadius: 4,
  },
  encouragement: {
    color: '#8b8b9e',
    fontSize: 16,
    textAlign: 'center',
    paddingBottom: 40,
  },
  completeHeader: {
    alignItems: 'center',
    flex: 1,
    justifyContent: 'center',
  },
  completeEmoji: {
    fontSize: 80,
    marginBottom: 24,
  },
  completeTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#4caf50',
    marginBottom: 8,
  },
  completeSubtitle: {
    fontSize: 18,
    color: '#8b8b9e',
  },
  continueButton: {
    backgroundColor: '#4caf50',
    paddingVertical: 18,
    borderRadius: 16,
    alignItems: 'center',
    marginBottom: 40,
  },
  continueButtonText: {
    color: '#fff',
    fontSize: 20,
    fontWeight: '600',
  },
});
