import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  SafeAreaView,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation, useRoute, RouteProp, useFocusEffect } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Colors, Spacing, Radius, Typography, CATEGORY_COLORS } from '../constants/theme';
import { getHabits, deleteHabit, getCompletionRate, getCalendarData } from '../services/storage';
import { Habit, RootStackParamList } from '../types';
import { getNextMilestone, MILESTONE_DAYS } from '../constants/habits';

type NavProp = NativeStackNavigationProp<RootStackParamList>;
type RouteType = RouteProp<RootStackParamList, 'HabitDetail'>;

export default function HabitDetailScreen() {
  const navigation = useNavigation<NavProp>();
  const route = useRoute<RouteType>();
  const [habit, setHabit] = useState<Habit | null>(null);

  useFocusEffect(useCallback(() => {
    getHabits().then(all => {
      const found = all.find(h => h.id === route.params.habitId);
      setHabit(found ?? null);
    });
  }, [route.params.habitId]));

  const handleDelete = () => {
    Alert.alert(
      'Delete habit?',
      `This will delete "${habit?.name}" and all its streak history. This cannot be undone.`,
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: async () => {
            if (habit) {
              await deleteHabit(habit.id);
              navigation.goBack();
            }
          },
        },
      ],
    );
  };

  if (!habit) return null;

  const completionRate = getCompletionRate(habit, 30);
  const calData = getCalendarData(habit);
  const nextMilestone = getNextMilestone(habit.currentStreak);
  const categoryColor = CATEGORY_COLORS[habit.category] ?? Colors.emerald;

  return (
    <SafeAreaView style={s.container}>
      <View style={s.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Ionicons name="chevron-back" size={24} color={Colors.text} />
        </TouchableOpacity>
        <Text style={s.headerTitle} numberOfLines={1}>{habit.name}</Text>
        <TouchableOpacity onPress={handleDelete}>
          <Ionicons name="trash-outline" size={20} color={Colors.textMuted} />
        </TouchableOpacity>
      </View>

      <ScrollView contentContainerStyle={s.scroll} showsVerticalScrollIndicator={false}>
        {/* Emoji + streak hero */}
        <View style={[s.heroCard, { borderColor: categoryColor + '40' }]}>
          <Text style={s.heroEmoji}>{habit.emoji}</Text>
          <Text style={s.heroStreak}>{habit.currentStreak}</Text>
          <Text style={s.heroStreakLabel}>day streak</Text>
          {habit.currentStreak > 0 && (
            <Text style={s.heroNext}>Next milestone: {nextMilestone} days</Text>
          )}
        </View>

        {/* Stats row */}
        <View style={s.statsRow}>
          <StatCard label="Longest" value={`${habit.longestStreak}d`} />
          <StatCard label="Total" value={`${habit.totalCompletions}`} />
          <StatCard label="30d rate" value={`${completionRate}%`} />
        </View>

        {/* MVD */}
        {habit.mvdEnabled && (
          <View style={s.mvdCard}>
            <Text style={s.mvdTitle}>Minimum Viable Day</Text>
            <Text style={s.mvdText}>"{habit.mvdLabel}"</Text>
          </View>
        )}

        {/* Milestones */}
        <Text style={s.sectionLabel}>Milestones</Text>
        <View style={s.milestonesGrid}>
          {MILESTONE_DAYS.map(m => {
            const reached = habit.longestStreak >= m;
            return (
              <View key={m} style={[s.milestonePill, reached && s.milestonePillReached]}>
                <Text style={[s.milestoneDays, reached && s.milestoneDaysReached]}>{m}d</Text>
                {reached && <Ionicons name="checkmark" size={12} color={Colors.emerald} />}
              </View>
            );
          })}
        </View>

        {/* 30-day calendar */}
        <Text style={s.sectionLabel}>Last 30 days</Text>
        <MiniCalendar calData={calData} />
      </ScrollView>
    </SafeAreaView>
  );
}

function StatCard({ label, value }: { label: string; value: string }) {
  return (
    <View style={s.statCard}>
      <Text style={s.statValue}>{value}</Text>
      <Text style={s.statLabel}>{label}</Text>
    </View>
  );
}

function MiniCalendar({ calData }: { calData: Set<string> }) {
  const days: Date[] = [];
  for (let i = 29; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    days.push(d);
  }

  return (
    <View style={s.calendar}>
      {days.map(d => {
        const key = d.toDateString();
        const done = calData.has(key);
        const isToday = key === new Date().toDateString();
        return (
          <View
            key={key}
            style={[s.calDay, done && s.calDayDone, isToday && s.calDayToday]}
          />
        );
      })}
    </View>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.bg },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: Spacing.lg,
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  headerTitle: { ...Typography.h3, color: Colors.text, flex: 1, textAlign: 'center' },
  scroll: { padding: Spacing.lg, paddingBottom: 48 },
  // Hero
  heroCard: {
    backgroundColor: Colors.bgCard,
    borderRadius: Radius.lg,
    padding: 32,
    alignItems: 'center',
    marginBottom: Spacing.md,
    borderWidth: 2,
    gap: 4,
  },
  heroEmoji: { fontSize: 52, marginBottom: 8 },
  heroStreak: { ...Typography.hero, color: Colors.text },
  heroStreakLabel: { ...Typography.body, color: Colors.textMuted },
  heroNext: { ...Typography.caption, color: Colors.textLight, marginTop: 4 },
  // Stats
  statsRow: { flexDirection: 'row', gap: 10, marginBottom: Spacing.md },
  statCard: {
    flex: 1,
    backgroundColor: Colors.bgCard,
    borderRadius: Radius.md,
    padding: 16,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: Colors.border,
    gap: 4,
  },
  statValue: { ...Typography.h2, color: Colors.text },
  statLabel: { ...Typography.caption, color: Colors.textMuted },
  // MVD
  mvdCard: {
    backgroundColor: Colors.goldLight,
    borderRadius: Radius.md,
    padding: 16,
    marginBottom: Spacing.md,
    gap: 4,
  },
  mvdTitle: { ...Typography.captionMed, color: Colors.gold, textTransform: 'uppercase' },
  mvdText: { ...Typography.body, color: Colors.text, fontStyle: 'italic' },
  // Milestones
  sectionLabel: { ...Typography.captionMed, color: Colors.textMuted, textTransform: 'uppercase', letterSpacing: 0.5, marginBottom: 10, marginTop: Spacing.md },
  milestonesGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: Spacing.md },
  milestonePill: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingHorizontal: 14,
    paddingVertical: 7,
    borderRadius: Radius.full,
    backgroundColor: Colors.bgCard,
    borderWidth: 1.5,
    borderColor: Colors.border,
  },
  milestonePillReached: { borderColor: Colors.emerald, backgroundColor: Colors.emeraldSubtle },
  milestoneDays: { ...Typography.captionMed, color: Colors.textMuted },
  milestoneDaysReached: { color: Colors.emeraldDark },
  // Calendar
  calendar: { flexDirection: 'row', flexWrap: 'wrap', gap: 5 },
  calDay: {
    width: 28,
    height: 28,
    borderRadius: 6,
    backgroundColor: Colors.border,
  },
  calDayDone: { backgroundColor: Colors.emerald },
  calDayToday: { borderWidth: 2, borderColor: Colors.emeraldDark },
});
