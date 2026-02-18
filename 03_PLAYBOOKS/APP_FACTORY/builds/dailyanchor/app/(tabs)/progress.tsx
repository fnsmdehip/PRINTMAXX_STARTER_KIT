import { useEffect, useMemo, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
} from 'react-native';
import { StreakCounter, StreakCalendar } from '../../src/components/streaks';
import { Card } from '../../src/components/common';
import { COLORS } from '../../src/utils/constants';
import { useHabitStore, useJournalStore } from '../../src/store';
import { calculateStreak } from '../../src/utils/dateUtils';

export default function ProgressScreen() {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const { completions, habits, loadFromStorage: loadHabits } = useHabitStore();
  const { entries, loadFromStorage: loadJournal } = useJournalStore();

  useEffect(() => {
    loadHabits();
    loadJournal();
  }, [loadHabits, loadJournal]);

  // Get unique completion dates (at least one habit completed)
  const completedDates = useMemo(() => {
    return [...new Set(completions.map((c) => c.date))];
  }, [completions]);

  // Calculate stats
  const stats = useMemo(() => {
    const { currentStreak, longestStreak } = calculateStreak(completedDates);

    // Total completions
    const totalCompletions = completions.length;

    // Days with all habits completed
    const perfectDays = completedDates.filter((date) => {
      const dayCompletions = completions.filter((c) => c.date === date);
      return dayCompletions.length >= habits.length;
    }).length;

    // Journal entries
    const journalCount = entries.length;

    // This week completions
    const today = new Date();
    const weekAgo = new Date(today);
    weekAgo.setDate(weekAgo.getDate() - 7);
    const weekAgoStr = weekAgo.toISOString().split('T')[0];

    const thisWeekDays = completedDates.filter((d) => d >= weekAgoStr).length;

    return {
      currentStreak,
      longestStreak,
      totalCompletions,
      perfectDays,
      journalCount,
      thisWeekDays,
    };
  }, [completedDates, completions, habits.length, entries.length]);

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        <Text style={styles.title}>Progress</Text>

        <StreakCounter
          currentStreak={stats.currentStreak}
          longestStreak={stats.longestStreak}
        />

        <View style={styles.statsGrid}>
          <Card style={styles.statCard}>
            <Text style={styles.statValue}>{stats.thisWeekDays}</Text>
            <Text style={styles.statLabel}>Days this week</Text>
          </Card>

          <Card style={styles.statCard}>
            <Text style={styles.statValue}>{stats.perfectDays}</Text>
            <Text style={styles.statLabel}>Perfect days</Text>
          </Card>

          <Card style={styles.statCard}>
            <Text style={styles.statValue}>{stats.journalCount}</Text>
            <Text style={styles.statLabel}>Journal entries</Text>
          </Card>

          <Card style={styles.statCard}>
            <Text style={styles.statValue}>{stats.totalCompletions}</Text>
            <Text style={styles.statLabel}>Total completions</Text>
          </Card>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Calendar</Text>
          <StreakCalendar
            completedDates={completedDates}
            currentMonth={currentMonth}
            onMonthChange={setCurrentMonth}
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
  title: {
    fontSize: 28,
    fontWeight: '800',
    color: COLORS.text,
    marginBottom: 24,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginTop: 20,
    marginHorizontal: -6,
  },
  statCard: {
    width: '50%',
    paddingHorizontal: 6,
    marginBottom: 12,
  },
  statValue: {
    fontSize: 32,
    fontWeight: '800',
    color: COLORS.primary,
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 13,
    color: COLORS.textSecondary,
  },
  section: {
    marginTop: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 16,
  },
});
