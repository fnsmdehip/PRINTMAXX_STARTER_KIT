import { useEffect, useMemo, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  RefreshControl,
} from 'react-native';
import { useRouter } from 'expo-router';
import { HabitChecklist } from '../../src/components/habits';
import { StreakCounter } from '../../src/components/streaks';
import { DailyVerse } from '../../src/components/common';
import { COLORS } from '../../src/utils/constants';
import { useHabitStore, useVerseStore } from '../../src/store';
import { getToday, formatDisplayDate, calculateStreak } from '../../src/utils/dateUtils';

export default function TodayScreen() {
  const router = useRouter();
  const [refreshing, setRefreshing] = useState(false);
  const { completions, loadFromStorage } = useHabitStore();
  const { fetchVerse } = useVerseStore();

  const today = getToday();

  // Calculate streak from completions
  const streakData = useMemo(() => {
    const completedDates = [...new Set(completions.map((c) => c.date))];
    return calculateStreak(completedDates);
  }, [completions]);

  const onRefresh = async () => {
    setRefreshing(true);
    await Promise.all([loadFromStorage(), fetchVerse()]);
    setRefreshing(false);
  };

  useEffect(() => {
    loadFromStorage();
  }, [loadFromStorage]);

  const handlePremiumRequired = () => {
    router.push('/paywall');
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.header}>
          <Text style={styles.greeting}>Good morning</Text>
          <Text style={styles.date}>{formatDisplayDate(today)}</Text>
        </View>

        <StreakCounter
          currentStreak={streakData.currentStreak}
          longestStreak={streakData.longestStreak}
        />

        <View style={styles.section}>
          <DailyVerse />
        </View>

        <View style={styles.section}>
          <HabitChecklist
            date={today}
            onPremiumRequired={handlePremiumRequired}
          />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scroll: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 40,
  },
  header: {
    marginBottom: 24,
  },
  greeting: {
    fontSize: 28,
    fontWeight: '800',
    color: COLORS.text,
    marginBottom: 4,
  },
  date: {
    fontSize: 16,
    color: COLORS.textSecondary,
  },
  section: {
    marginTop: 24,
  },
});
