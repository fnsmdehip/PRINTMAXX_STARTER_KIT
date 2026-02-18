import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Alert,
  SafeAreaView,
  StatusBar,
  AppState,
  AppStateStatus,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import * as Haptics from 'expo-haptics';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RouteProp } from '@react-navigation/native';
import { Button, CircularProgress, VerseCard } from '../components';
import { Colors, FAITH_STRINGS } from '../constants';
import { useApp } from '../context/AppContext';
import { formatTimerDisplay, getTodayVerseIndex } from '../utils/storage';
import versesData from '../data/verses.json';

type RootStackParamList = {
  Lock: undefined;
  Timer: { duration: number; salahName?: string };
  Main: undefined;
};

type TimerScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Timer'>;
  route: RouteProp<RootStackParamList, 'Timer'>;
};

export function TimerScreen({ navigation, route }: TimerScreenProps) {
  const { duration, salahName } = route.params;
  const { settings, completePrayer, completeSalah } = useApp();
  const totalSeconds = duration * 60;

  const faithStrings = FAITH_STRINGS[settings.faith];
  const isIslam = settings.faith === 'islam';

  const [secondsRemaining, setSecondsRemaining] = useState(totalSeconds);
  const [isPaused, setIsPaused] = useState(false);
  const [isComplete, setIsComplete] = useState(false);

  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const startTimeRef = useRef<number>(Date.now());
  const pausedTimeRef = useRef<number>(0);
  const appState = useRef(AppState.currentState);

  const todayVerse = versesData.verses[getTodayVerseIndex(versesData.verses.length)];

  let displayVerse = todayVerse;
  if (isIslam) {
    try {
      const quranData = require('../data/quran_verses.json');
      const quranVerses = quranData.verses || [];
      if (quranVerses.length > 0) {
        displayVerse = quranVerses[getTodayVerseIndex(quranVerses.length)];
      }
    } catch {
      // Quran data not available
    }
  }

  const progress = 1 - secondsRemaining / totalSeconds;

  const handleComplete = useCallback(async () => {
    setIsComplete(true);

    if (settings.hapticEnabled) {
      await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    }

    if (salahName && isIslam) {
      await completeSalah(salahName as 'fajr' | 'dhuhr' | 'asr' | 'maghrib' | 'isha', duration);
    } else {
      await completePrayer(duration);
    }

    const salahDisplayNames: Record<string, string> = {
      fajr: 'Fajr',
      dhuhr: 'Dhuhr',
      asr: 'Asr',
      maghrib: 'Maghrib',
      isha: 'Isha',
    };

    const completionTitle = salahName
      ? `${salahDisplayNames[salahName]} Complete`
      : isIslam
        ? 'Salah Complete'
        : settings.faith === 'general'
          ? 'Session Complete'
          : 'Prayer Complete';

    Alert.alert(
      completionTitle,
      faithStrings.completionMessage,
      [
        {
          text: isIslam ? 'Ameen' : settings.faith === 'general' ? 'Continue' : 'Amen',
          onPress: () => navigation.navigate('Main'),
        },
      ]
    );
  }, [settings.hapticEnabled, completePrayer, completeSalah, duration, navigation, salahName, isIslam, faithStrings, settings.faith]);

  useEffect(() => {
    const subscription = AppState.addEventListener('change', (nextAppState: AppStateStatus) => {
      if (appState.current === 'active' && nextAppState.match(/inactive|background/)) {
        pausedTimeRef.current = Date.now() - startTimeRef.current;
      } else if (appState.current.match(/inactive|background/) && nextAppState === 'active') {
        if (!isPaused && !isComplete) {
          const totalElapsed = Date.now() - startTimeRef.current;
          const newRemaining = Math.max(0, totalSeconds - Math.floor(totalElapsed / 1000));
          setSecondsRemaining(newRemaining);
        }
      }
      appState.current = nextAppState;
    });

    return () => subscription.remove();
  }, [isPaused, isComplete, totalSeconds]);

  useEffect(() => {
    if (!isPaused && !isComplete) {
      timerRef.current = setInterval(() => {
        setSecondsRemaining((prev) => {
          if (prev <= 1) {
            if (timerRef.current) clearInterval(timerRef.current);
            handleComplete();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isPaused, isComplete, handleComplete]);

  const handlePause = () => {
    setIsPaused(true);
    pausedTimeRef.current = Date.now() - startTimeRef.current;
    if (timerRef.current) clearInterval(timerRef.current);

    if (settings.hapticEnabled) {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }
  };

  const handleResume = () => {
    startTimeRef.current = Date.now() - pausedTimeRef.current;
    setIsPaused(false);

    if (settings.hapticEnabled) {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }
  };

  const handleCancel = () => {
    Alert.alert(
      isIslam ? 'Cancel Salah?' : 'Cancel Prayer?',
      isIslam
        ? 'Are you sure you want to stop your salah time? This will not unlock your phone.'
        : 'Are you sure you want to stop your prayer time? This will not unlock your phone.',
      [
        { text: isIslam ? 'Keep Praying' : 'Keep Praying', style: 'cancel' },
        {
          text: 'Cancel',
          style: 'destructive',
          onPress: () => navigation.goBack(),
        },
      ]
    );
  };

  const getSubtitle = () => {
    if (isPaused) return 'Paused';
    if (isIslam) return 'Stay present with Allah';
    if (settings.faith === 'general') return 'Stay present and mindful';
    return 'Stay present with God';
  };

  return (
    <LinearGradient
      colors={[Colors.gradientStart, Colors.gradientEnd]}
      style={styles.container}
    >
      <StatusBar barStyle="light-content" />
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <Text style={styles.title}>{faithStrings.timerLabel}</Text>
          <Text style={styles.subtitle}>{getSubtitle()}</Text>
        </View>

        <View style={styles.timerContainer}>
          <CircularProgress
            progress={progress}
            timeDisplay={formatTimerDisplay(secondsRemaining)}
            subtitle={isPaused ? 'Tap Resume' : 'remaining'}
          />
        </View>

        <VerseCard
          text={displayVerse.text}
          reference={displayVerse.reference}
          variant="dark"
        />

        <View style={styles.actions}>
          {isPaused ? (
            <Button
              title="Resume"
              onPress={handleResume}
              size="large"
            />
          ) : (
            <Button
              title="Pause"
              onPress={handlePause}
              variant="outline"
              size="large"
              textStyle={styles.pauseButtonText}
              style={styles.pauseButton}
            />
          )}

          <Button
            title="Cancel"
            onPress={handleCancel}
            variant="ghost"
            size="small"
            textStyle={styles.cancelText}
          />
        </View>
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
    paddingHorizontal: 20,
  },
  header: {
    alignItems: 'center',
    marginTop: 40,
    marginBottom: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: Colors.white,
  },
  subtitle: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.7)',
    marginTop: 8,
  },
  timerContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    marginVertical: 40,
  },
  actions: {
    marginTop: 'auto',
    marginBottom: 40,
    gap: 16,
  },
  pauseButton: {
    borderColor: 'rgba(255, 255, 255, 0.3)',
  },
  pauseButtonText: {
    color: Colors.white,
  },
  cancelText: {
    color: 'rgba(255, 255, 255, 0.5)',
    fontSize: 14,
  },
});
