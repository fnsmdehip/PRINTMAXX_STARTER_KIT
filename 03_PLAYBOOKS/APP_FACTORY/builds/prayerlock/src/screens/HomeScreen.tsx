import React, { useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  StatusBar,
  RefreshControl,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Button, StatCard, VerseCard, SalahTracker } from '../components';
import { Colors, FAITH_STRINGS } from '../constants';
import { useApp } from '../context/AppContext';
import { formatTime, getTodayVerseIndex } from '../utils/storage';
import versesData from '../data/verses.json';

type RootStackParamList = {
  Home: undefined;
  Settings: undefined;
  Paywall: undefined;
  Lock: undefined;
  Timer: { duration: number; salahName?: string };
};

type HomeScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Home'>;
};

export function HomeScreen({ navigation }: HomeScreenProps) {
  const { streakData, settings, isPremium, triggerLock, refreshData } = useApp();
  const [refreshing, setRefreshing] = React.useState(false);

  const faithStrings = FAITH_STRINGS[settings.faith];
  const isIslam = settings.faith === 'islam';

  const todayVerse = versesData.verses[getTodayVerseIndex(versesData.verses.length)];

  let quranVerses: { text: string; arabic?: string; reference: string }[] = [];
  try {
    const quranData = require('../data/quran_verses.json');
    quranVerses = quranData.verses || [];
  } catch {
    quranVerses = [];
  }

  const todayQuranVerse = quranVerses.length > 0
    ? quranVerses[getTodayVerseIndex(quranVerses.length)]
    : null;

  const displayVerse = isIslam && todayQuranVerse ? todayQuranVerse : todayVerse;

  useFocusEffect(
    useCallback(() => {
      refreshData();
    }, [refreshData])
  );

  const onRefresh = async () => {
    setRefreshing(true);
    await refreshData();
    setRefreshing(false);
  };

  const handleTestLock = async () => {
    await triggerLock();
    navigation.navigate('Lock');
  };

  const handleSalahPress = (salahName: 'fajr' | 'dhuhr' | 'asr' | 'maghrib' | 'isha') => {
    const { SALAH_PRAYERS } = require('../services/salahTimes');
    const prayer = SALAH_PRAYERS.find((p: any) => p.name === salahName);
    const duration = prayer ? prayer.defaultMinutes : 5;
    navigation.navigate('Timer', { duration, salahName });
  };

  const getGreeting = () => {
    if (isIslam) return faithStrings.greeting;
    const hour = new Date().getHours();
    if (hour < 12) return 'Good Morning';
    if (hour < 18) return 'Good Afternoon';
    return 'Good Evening';
  };

  const getTitle = () => {
    if (isIslam) return 'Your Salah Today';
    if (settings.faith === 'general') return 'Your Mindfulness Practice';
    return 'Your Prayer Life';
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        <View style={styles.header}>
          <Text style={styles.greeting}>{getGreeting()}</Text>
          <Text style={styles.title}>{getTitle()}</Text>
        </View>

        <View style={styles.statsRow}>
          <StatCard
            value={streakData.currentStreak}
            label="Day Streak"
            highlight
          />
          <StatCard
            value={streakData.longestStreak}
            label="Best Streak"
          />
          <StatCard
            value={formatTime(streakData.totalPrayerMinutes)}
            label="Total Time"
          />
        </View>

        {isIslam && (
          <View style={styles.salahSection}>
            <SalahTracker onPrayerPress={handleSalahPress} />
          </View>
        )}

        <View style={styles.verseSection}>
          <Text style={styles.sectionTitle}>
            {isIslam ? "Today's Ayah" : "Today's Verse"}
          </Text>
          {isIslam && displayVerse && 'arabic' in displayVerse && displayVerse.arabic ? (
            <View>
              <VerseCard
                text={displayVerse.arabic}
                reference=""
              />
              <VerseCard
                text={displayVerse.text}
                reference={displayVerse.reference}
              />
            </View>
          ) : (
            <VerseCard text={displayVerse.text} reference={displayVerse.reference} />
          )}
        </View>

        {!isIslam && (
          <View style={styles.infoSection}>
            <View style={styles.infoCard}>
              <Text style={styles.infoTitle}>How PrayerLock Works</Text>
              <View style={styles.infoItem}>
                <Text style={styles.infoNumber}>1</Text>
                <Text style={styles.infoText}>
                  Set your wake-up time in settings
                </Text>
              </View>
              <View style={styles.infoItem}>
                <Text style={styles.infoNumber}>2</Text>
                <Text style={styles.infoText}>
                  When you wake, complete your {settings.faith === 'general' ? 'meditation' : 'prayer'} timer
                </Text>
              </View>
              <View style={styles.infoItem}>
                <Text style={styles.infoNumber}>3</Text>
                <Text style={styles.infoText}>
                  Unlock your phone and start your day with intention
                </Text>
              </View>
            </View>
          </View>
        )}

        {streakData.emergencyUnlockCount > 0 && (
          <View style={styles.shameCounter}>
            <Text style={styles.shameTitle}>
              {isIslam ? 'Missed Prayers' : 'Emergency Unlocks'}
            </Text>
            <Text style={styles.shameCount}>{streakData.emergencyUnlockCount}</Text>
            <Text style={styles.shameSubtitle}>
              {isIslam
                ? 'May Allah forgive and guide you'
                : "God's mercies are new every morning"}
            </Text>
          </View>
        )}

        {!isPremium && (
          <View style={styles.promoCard}>
            <Text style={styles.promoTitle}>Unlock Pro Features</Text>
            <Text style={styles.promoText}>
              Extended {isIslam ? 'salah' : 'prayer'} times, family accountability, streak freezes, and more.
            </Text>
            <Button
              title="View Pro Plans"
              onPress={() => navigation.navigate('Paywall')}
              size="medium"
              style={styles.promoButton}
            />
          </View>
        )}

        <View style={styles.testSection}>
          <Button
            title={isIslam ? 'Test Salah Lock' : 'Test Lock Screen'}
            onPress={handleTestLock}
            variant="outline"
            size="medium"
          />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  scrollContent: {
    paddingBottom: 100,
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 24,
  },
  greeting: {
    fontSize: 16,
    color: Colors.textSecondary,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: Colors.text,
    marginTop: 4,
  },
  statsRow: {
    flexDirection: 'row',
    paddingHorizontal: 20,
    gap: 12,
  },
  salahSection: {
    marginTop: 24,
  },
  verseSection: {
    marginTop: 32,
  },
  sectionTitle: {
    fontSize: 14,
    color: Colors.textSecondary,
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: 1,
    paddingHorizontal: 20,
    marginBottom: 12,
  },
  infoSection: {
    paddingHorizontal: 20,
    marginTop: 32,
  },
  infoCard: {
    backgroundColor: Colors.white,
    borderRadius: 16,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  infoTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: Colors.text,
    marginBottom: 16,
  },
  infoItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  infoNumber: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: Colors.primary,
    color: Colors.white,
    textAlign: 'center',
    lineHeight: 24,
    fontWeight: '600',
    fontSize: 14,
    marginRight: 12,
  },
  infoText: {
    flex: 1,
    fontSize: 15,
    color: Colors.textSecondary,
    lineHeight: 22,
  },
  shameCounter: {
    marginHorizontal: 20,
    marginTop: 32,
    backgroundColor: Colors.white,
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: Colors.warning,
  },
  shameTitle: {
    fontSize: 12,
    color: Colors.warning,
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  shameCount: {
    fontSize: 36,
    fontWeight: '700',
    color: Colors.warning,
    marginVertical: 8,
  },
  shameSubtitle: {
    fontSize: 14,
    color: Colors.textSecondary,
    fontStyle: 'italic',
  },
  promoCard: {
    marginHorizontal: 20,
    marginTop: 32,
    backgroundColor: Colors.secondary,
    borderRadius: 16,
    padding: 24,
  },
  promoTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: Colors.white,
    marginBottom: 8,
  },
  promoText: {
    fontSize: 15,
    color: 'rgba(255, 255, 255, 0.8)',
    lineHeight: 22,
    marginBottom: 16,
  },
  promoButton: {
    backgroundColor: Colors.primary,
  },
  testSection: {
    paddingHorizontal: 20,
    marginTop: 32,
  },
});
