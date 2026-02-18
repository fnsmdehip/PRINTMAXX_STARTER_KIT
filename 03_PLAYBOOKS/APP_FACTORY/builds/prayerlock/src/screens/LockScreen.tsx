import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Alert,
  SafeAreaView,
  StatusBar,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import * as Haptics from 'expo-haptics';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Button, VerseCard, DurationPicker } from '../components';
import { Colors, FAITH_STRINGS } from '../constants';
import { useApp } from '../context/AppContext';
import { getTodayVerseIndex } from '../utils/storage';
import versesData from '../data/verses.json';

type RootStackParamList = {
  Lock: undefined;
  Timer: { duration: number; salahName?: string };
  Main: undefined;
};

type LockScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Lock'>;
};

export function LockScreen({ navigation }: LockScreenProps) {
  const { settings, isPremium, emergencyUnlock, streakData } = useApp();
  const [selectedDuration, setSelectedDuration] = useState(settings.prayerDuration);

  const faithStrings = FAITH_STRINGS[settings.faith];
  const isIslam = settings.faith === 'islam';

  const todayVerse = versesData.verses[getTodayVerseIndex(versesData.verses.length)];

  let displayVerse = todayVerse;
  let displayPrompt = versesData.prayerPrompts[getTodayVerseIndex(versesData.prayerPrompts.length)];

  if (isIslam) {
    try {
      const quranData = require('../data/quran_verses.json');
      const quranVerses = quranData.verses || [];
      if (quranVerses.length > 0) {
        displayVerse = quranVerses[getTodayVerseIndex(quranVerses.length)];
      }
      const quranPrompts = quranData.prayerPrompts || [];
      if (quranPrompts.length > 0) {
        displayPrompt = quranPrompts[getTodayVerseIndex(quranPrompts.length)];
      }
    } catch {
      // Quran data not available, fall back to generic
    }
  }

  const handleStartPrayer = async () => {
    if (settings.hapticEnabled) {
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    }
    navigation.navigate('Timer', { duration: selectedDuration });
  };

  const handleEmergencyUnlock = () => {
    Alert.alert(
      isIslam ? 'Skip Salah' : 'Emergency Unlock',
      isIslam
        ? `This will mark this salah as missed and add to your missed prayer count (current: ${streakData.emergencyUnlockCount}).\n\nAre you sure?`
        : `This will skip your morning prayer and add to your shame counter (current: ${streakData.emergencyUnlockCount}). Your streak will not be broken, but the counter tracks skipped prayers.\n\nAre you sure?`,
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: faithStrings.emergencyLabel,
          style: 'destructive',
          onPress: async () => {
            const count = await emergencyUnlock();
            if (settings.hapticEnabled) {
              await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning);
            }
            Alert.alert(
              'Phone Unlocked',
              isIslam
                ? `Missed prayers: ${count}\n\nMay Allah forgive and guide you.`
                : `Emergency unlocks: ${count}\n\nRemember, God's mercies are new every morning.`,
              [{ text: 'OK', onPress: () => navigation.navigate('Main') }]
            );
          },
        },
      ]
    );
  };

  const getGreeting = () => {
    if (isIslam) return faithStrings.greeting;
    const hour = new Date().getHours();
    if (hour < 12) return 'Good Morning';
    if (hour < 18) return 'Good Afternoon';
    return 'Good Evening';
  };

  return (
    <LinearGradient
      colors={[Colors.gradientStart, Colors.gradientEnd]}
      style={styles.container}
    >
      <StatusBar barStyle="light-content" />
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <Text style={styles.greeting}>{getGreeting()}</Text>
          <Text style={styles.title}>{faithStrings.lockMessage}</Text>
        </View>

        <VerseCard
          text={displayVerse.text}
          reference={displayVerse.reference}
          variant="dark"
        />

        <View style={styles.promptSection}>
          <Text style={styles.promptLabel}>
            {isIslam ? "Today's Du'a Focus" : "Today's Prayer Focus"}
          </Text>
          <Text style={styles.promptText}>{displayPrompt}</Text>
        </View>

        <View style={styles.durationSection}>
          <DurationPicker
            selectedDuration={selectedDuration}
            onSelect={setSelectedDuration}
            isPremium={isPremium}
          />
        </View>

        <View style={styles.actions}>
          <Button
            title={`Start ${selectedDuration} min ${isIslam ? 'Salah' : settings.faith === 'general' ? 'Session' : 'Prayer'}`}
            onPress={handleStartPrayer}
            size="large"
          />

          <Button
            title={faithStrings.emergencyLabel}
            onPress={handleEmergencyUnlock}
            variant="ghost"
            size="small"
            textStyle={styles.emergencyText}
          />
        </View>

        {streakData.currentStreak > 0 && (
          <View style={styles.streakBadge}>
            <Text style={styles.streakText}>
              {streakData.currentStreak} day streak
            </Text>
          </View>
        )}
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
    marginBottom: 30,
  },
  greeting: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.7)',
    marginBottom: 8,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: Colors.white,
    textAlign: 'center',
  },
  promptSection: {
    marginTop: 24,
    paddingHorizontal: 20,
    alignItems: 'center',
  },
  promptLabel: {
    fontSize: 12,
    color: 'rgba(255, 255, 255, 0.6)',
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: 8,
  },
  promptText: {
    fontSize: 18,
    color: Colors.white,
    textAlign: 'center',
    lineHeight: 26,
  },
  durationSection: {
    marginTop: 32,
    paddingHorizontal: 10,
  },
  actions: {
    marginTop: 'auto',
    marginBottom: 40,
    gap: 16,
  },
  emergencyText: {
    color: 'rgba(255, 255, 255, 0.5)',
    fontSize: 14,
  },
  streakBadge: {
    position: 'absolute',
    top: 60,
    right: 20,
    backgroundColor: Colors.primary,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  streakText: {
    color: Colors.white,
    fontWeight: '600',
    fontSize: 12,
  },
});
