import React, { useState, useRef, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Animated,
  PanResponder,
  SafeAreaView,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import * as StoreReview from 'expo-store-review';
import { useFocusEffect, useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Colors, Spacing, Radius, Typography } from '../constants/theme';
import { getHabits, getSettings, isCheckedInToday, checkInHabit } from '../services/storage';
import { Habit, AppSettings, RootStackParamList } from '../types';
import { getNextMilestone, MILESTONE_DAYS } from '../constants/habits';

type NavProp = NativeStackNavigationProp<RootStackParamList>;

const FREE_HABIT_LIMIT = 3;
// Swipe threshold: 45px up to trigger check-in, max 40px horizontal drift
const SWIPE_UP_THRESHOLD = 45;
const SWIPE_DRIFT_MAX = 40;

export default function TodayScreen() {
  const navigation = useNavigation<NavProp>();
  const [habits, setHabits] = useState<Habit[]>([]);
  const [settings, setSettings] = useState<AppSettings | null>(null);
  const [celebratingId, setCelebratingId] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    const [h, s] = await Promise.all([getHabits(), getSettings()]);
    setHabits(h);
    setSettings(s);
  }, []);

  useFocusEffect(useCallback(() => { loadData(); }, [loadData]));

  const allDoneToday = habits.length > 0 && habits.every(h => isCheckedInToday(h));

  const handleCheckIn = async (habitId: string) => {
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    setCelebratingId(habitId);

    const result = await checkInHabit(habitId);
    setHabits(result.habits);

    // Milestone alert
    if (result.isNewMilestone && result.milestoneDay) {
      setTimeout(() => {
        Alert.alert(
          `${result.milestoneDay}-day streak! 🔥`,
          result.habit.name,
          [{ text: 'Keep going', style: 'default' }],
        );
      }, 600);
    }

    // Post-value review prompt (day 3 or day 7, 90-day cooldown)
    if (result.shouldPromptReview) {
      setTimeout(async () => {
        const available = await StoreReview.isAvailableAsync();
        if (available) StoreReview.requestReview();
      }, 1500);
    }

    setTimeout(() => setCelebratingId(null), 800);
  };

  const handleAddHabit = () => {
    if (!settings?.isPremium && habits.length >= FREE_HABIT_LIMIT) {
      navigation.navigate('Paywall', { source: 'habit_limit' });
      return;
    }
    navigation.navigate('AddHabit');
  };

  return (
    <SafeAreaView style={s.container}>
      <View style={s.header}>
        <View>
          <Text style={s.headerDate}>{formatDate()}</Text>
          <Text style={s.headerTitle}>Today</Text>
        </View>
        <TouchableOpacity style={s.addBtn} onPress={handleAddHabit}>
          <Ionicons name="add" size={22} color={Colors.emerald} />
        </TouchableOpacity>
      </View>

      {habits.length === 0 ? (
        <EmptyState onAdd={handleAddHabit} />
      ) : (
        <ScrollView
          style={s.scroll}
          contentContainerStyle={s.scrollContent}
          showsVerticalScrollIndicator={false}
        >
          {allDoneToday && <AllDoneBanner />}

          {habits.map(habit => (
            <SwipeHabitCard
              key={habit.id}
              habit={habit}
              celebrating={celebratingId === habit.id}
              onCheckIn={() => handleCheckIn(habit.id)}
              onPress={() => navigation.navigate('HabitDetail', { habitId: habit.id })}
            />
          ))}

          {!settings?.isPremium && habits.length < FREE_HABIT_LIMIT && (
            <TouchableOpacity style={s.addHabitRow} onPress={handleAddHabit}>
              <Ionicons name="add-circle-outline" size={22} color={Colors.emerald} />
              <Text style={s.addHabitText}>Add habit ({habits.length}/{FREE_HABIT_LIMIT} free)</Text>
            </TouchableOpacity>
          )}
          {settings?.isPremium && (
            <TouchableOpacity style={s.addHabitRow} onPress={handleAddHabit}>
              <Ionicons name="add-circle-outline" size={22} color={Colors.emerald} />
              <Text style={s.addHabitText}>Add habit</Text>
            </TouchableOpacity>
          )}
        </ScrollView>
      )}
    </SafeAreaView>
  );
}

// ─── Swipe card ───────────────────────────────────────────────────────────────

function SwipeHabitCard({
  habit,
  celebrating,
  onCheckIn,
  onPress,
}: {
  habit: Habit;
  celebrating: boolean;
  onCheckIn: () => void;
  onPress: () => void;
}) {
  const done = isCheckedInToday(habit);
  const translateY = useRef(new Animated.Value(0)).current;
  const opacity = useRef(new Animated.Value(1)).current;
  const scale = useRef(new Animated.Value(1)).current;
  const checkScale = useRef(new Animated.Value(done ? 1 : 0)).current;

  const panResponder = useRef(
    PanResponder.create({
      onStartShouldSetPanResponder: () => !done,
      onMoveShouldSetPanResponder: (_, g) =>
        !done && Math.abs(g.dy) > 5 && Math.abs(g.dy) > Math.abs(g.dx),
      onPanResponderMove: (_, g) => {
        if (g.dy < 0 && Math.abs(g.dx) <= SWIPE_DRIFT_MAX) {
          translateY.setValue(g.dy * 0.4);
        }
      },
      onPanResponderRelease: (_, g) => {
        if (g.dy < -SWIPE_UP_THRESHOLD && Math.abs(g.dx) <= SWIPE_DRIFT_MAX) {
          // Check-in animation
          Animated.parallel([
            Animated.timing(translateY, { toValue: -120, duration: 250, useNativeDriver: true }),
            Animated.timing(opacity, { toValue: 0, duration: 250, useNativeDriver: true }),
          ]).start(() => {
            onCheckIn();
            // Bounce back
            translateY.setValue(0);
            opacity.setValue(1);
            Animated.spring(checkScale, { toValue: 1, useNativeDriver: true }).start();
          });
        } else {
          Animated.spring(translateY, { toValue: 0, useNativeDriver: true }).start();
        }
      },
    }),
  ).current;

  const nextMilestone = getNextMilestone(habit.currentStreak);
  const progress = habit.currentStreak / nextMilestone;

  return (
    <Animated.View
      style={[s.card, done && s.cardDone, { transform: [{ translateY }, { scale }], opacity }]}
      {...(!done ? panResponder.panHandlers : {})}
    >
      <TouchableOpacity style={s.cardInner} onPress={onPress} activeOpacity={0.9}>
        <View style={s.cardLeft}>
          <Text style={s.cardEmoji}>{habit.emoji}</Text>
        </View>
        <View style={s.cardCenter}>
          <Text style={[s.cardName, done && s.cardNameDone]}>{habit.name}</Text>
          <View style={s.streakRow}>
            {habit.currentStreak > 0 && (
              <Text style={s.streakText}>🔥 {habit.currentStreak} day{habit.currentStreak !== 1 ? 's' : ''}</Text>
            )}
            {habit.mvdEnabled && !done && (
              <View style={s.mvdPill}>
                <Text style={s.mvdPillText}>MVD: {habit.mvdLabel}</Text>
              </View>
            )}
          </View>
          {!done && (
            <View style={s.progressBarBg}>
              <View style={[s.progressBarFill, { width: `${Math.min(progress * 100, 100)}%` }]} />
            </View>
          )}
        </View>
        <View style={s.cardRight}>
          {done ? (
            <Animated.View style={[s.checkCircle, { transform: [{ scale: checkScale }] }]}>
              <Ionicons name="checkmark" size={18} color="#fff" />
            </Animated.View>
          ) : (
            <View style={s.swipeHint}>
              <Ionicons name="arrow-up" size={14} color={Colors.textLight} />
            </View>
          )}
        </View>
      </TouchableOpacity>
    </Animated.View>
  );
}

// ─── Empty + All Done states ──────────────────────────────────────────────────

function EmptyState({ onAdd }: { onAdd: () => void }) {
  return (
    <View style={s.emptyState}>
      <Text style={s.emptyEmoji}>🌱</Text>
      <Text style={s.emptyTitle}>No habits yet</Text>
      <Text style={s.emptySub}>Add your first habit. Track fewer things. Actually keep them.</Text>
      <TouchableOpacity style={s.emptyBtn} onPress={onAdd}>
        <Text style={s.emptyBtnText}>Add first habit</Text>
      </TouchableOpacity>
    </View>
  );
}

function AllDoneBanner() {
  return (
    <View style={s.allDoneBanner}>
      <Text style={s.allDoneEmoji}>✅</Text>
      <Text style={s.allDoneTitle}>Day complete.</Text>
      <Text style={s.allDoneSub}>All habits done. Come back tomorrow.</Text>
    </View>
  );
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatDate(): string {
  return new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  });
}

// ─── Styles ───────────────────────────────────────────────────────────────────

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.bg },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: Spacing.lg,
    paddingTop: Spacing.md,
    paddingBottom: Spacing.sm,
  },
  headerDate: { ...Typography.caption, color: Colors.textMuted, textTransform: 'uppercase', letterSpacing: 0.5 },
  headerTitle: { ...Typography.h1, color: Colors.text },
  addBtn: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: Colors.emeraldSubtle,
    alignItems: 'center',
    justifyContent: 'center',
  },
  scroll: { flex: 1 },
  scrollContent: { paddingHorizontal: Spacing.lg, paddingBottom: Spacing.xxl },
  // Card
  card: {
    backgroundColor: Colors.bgCard,
    borderRadius: Radius.lg,
    marginBottom: 12,
    shadowColor: Colors.shadow,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 1,
    shadowRadius: 8,
    elevation: 2,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  cardDone: { borderColor: Colors.emeraldLight, backgroundColor: Colors.emeraldSubtle },
  cardInner: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 18,
    paddingHorizontal: 16,
    gap: 12,
  },
  cardLeft: {},
  cardEmoji: { fontSize: 30 },
  cardCenter: { flex: 1, gap: 4 },
  cardName: { ...Typography.bodyMed, color: Colors.text },
  cardNameDone: { color: Colors.emeraldDark },
  streakRow: { flexDirection: 'row', alignItems: 'center', gap: 8, flexWrap: 'wrap' },
  streakText: { ...Typography.caption, color: Colors.textMuted },
  mvdPill: {
    backgroundColor: Colors.goldLight,
    borderRadius: Radius.full,
    paddingHorizontal: 8,
    paddingVertical: 2,
  },
  mvdPillText: { ...Typography.label, color: Colors.gold },
  progressBarBg: {
    height: 3,
    backgroundColor: Colors.borderLight,
    borderRadius: 2,
    overflow: 'hidden',
    marginTop: 4,
  },
  progressBarFill: {
    height: '100%',
    backgroundColor: Colors.emerald,
    borderRadius: 2,
  },
  cardRight: { alignItems: 'center', justifyContent: 'center' },
  checkCircle: {
    width: 34,
    height: 34,
    borderRadius: 17,
    backgroundColor: Colors.emerald,
    alignItems: 'center',
    justifyContent: 'center',
  },
  swipeHint: {
    width: 34,
    height: 34,
    borderRadius: 17,
    borderWidth: 1.5,
    borderColor: Colors.border,
    alignItems: 'center',
    justifyContent: 'center',
  },
  // Add row
  addHabitRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    paddingVertical: 16,
    paddingHorizontal: 4,
  },
  addHabitText: { ...Typography.bodyMed, color: Colors.emerald },
  // All done banner
  allDoneBanner: {
    backgroundColor: Colors.emeraldSubtle,
    borderRadius: Radius.lg,
    padding: 20,
    alignItems: 'center',
    marginBottom: 16,
    gap: 4,
  },
  allDoneEmoji: { fontSize: 28 },
  allDoneTitle: { ...Typography.h3, color: Colors.emeraldDark },
  allDoneSub: { ...Typography.caption, color: Colors.emeraldDark, opacity: 0.8 },
  // Empty state
  emptyState: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: Spacing.xl },
  emptyEmoji: { fontSize: 52, marginBottom: 16 },
  emptyTitle: { ...Typography.h2, color: Colors.text, marginBottom: 8 },
  emptySub: { ...Typography.body, color: Colors.textMuted, textAlign: 'center', lineHeight: 24, marginBottom: Spacing.xl },
  emptyBtn: {
    backgroundColor: Colors.emerald,
    borderRadius: Radius.full,
    paddingHorizontal: 32,
    paddingVertical: 16,
  },
  emptyBtnText: { ...Typography.bodyMed, color: '#fff', fontWeight: '700' },
});
