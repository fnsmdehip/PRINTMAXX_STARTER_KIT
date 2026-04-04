import React, { useState, useCallback, useRef, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Alert,
  Animated,
  SafeAreaView,
} from 'react-native';
import { useFocusEffect, useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import * as StoreReview from 'expo-store-review';
import { Colors, Spacing, Radius, Typography } from '../constants/theme';
import { MODES, getMilestoneForDay, getNextMilestone } from '../constants/modes';
import { getStreakData, performCheckIn, recordRelapse, getSettings } from '../services/storage';
import { StreakData } from '../types';
import type { RootStackParamList } from '../types';

type NavProp = NativeStackNavigationProp<RootStackParamList>;

function formatDuration(days: number): { days: number; hours: number; minutes: number } {
  return { days, hours: new Date().getHours(), minutes: new Date().getMinutes() };
}

export default function TodayScreen() {
  const navigation = useNavigation<NavProp>();
  const [streak, setStreak] = useState<StreakData | null>(null);
  const [isPremium, setIsPremium] = useState(false);
  const [checkedInToday, setCheckedInToday] = useState(false);
  const celebrationScale = useRef(new Animated.Value(1)).current;
  const pulseAnim = useRef(new Animated.Value(1)).current;

  const loadData = useCallback(async () => {
    const [data, settings] = await Promise.all([getStreakData(), getSettings()]);
    if (!data) return;
    setStreak(data);
    setIsPremium(settings.isPremium);

    const today = new Date().toDateString();
    const alreadyIn = data.checkIns.some(c => new Date(c).toDateString() === today);
    setCheckedInToday(alreadyIn);
  }, []);

  useFocusEffect(useCallback(() => { loadData(); }, [loadData]));

  // Pulse the streak counter
  useEffect(() => {
    const loop = Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, { toValue: 1.04, duration: 2000, useNativeDriver: true }),
        Animated.timing(pulseAnim, { toValue: 1, duration: 2000, useNativeDriver: true }),
      ])
    );
    loop.start();
    return () => loop.stop();
  }, [pulseAnim]);

  const handleCheckIn = async () => {
    if (checkedInToday) {
      Alert.alert('Already checked in', 'You\'ve already logged today. Come back tomorrow.');
      return;
    }
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

    // Celebration animation
    Animated.sequence([
      Animated.timing(celebrationScale, { toValue: 1.15, duration: 200, useNativeDriver: true }),
      Animated.spring(celebrationScale, { toValue: 1, useNativeDriver: true }),
    ]).start();

    const { data: updated, isNewMilestone } = await performCheckIn();
    setStreak(updated);
    setCheckedInToday(true);

    if (isNewMilestone) {
      const mode = MODES[updated.mode];
      const msg = mode.milestoneMessages[updated.currentStreak];
      Alert.alert(`Day ${updated.currentStreak}`, msg || 'Another milestone. Keep going.', [
        { text: 'Thanks', style: 'default' },
      ]);

      // Fire review at day 3 or day 7 — post-value, not on app open.
      // 90-day cooldown prevents spamming. iOS system adds its own limit on top.
      if (updated.currentStreak === 3 || updated.currentStreak === 7) {
        try {
          const settings = await getSettings();
          const ninetyDaysAgo = new Date();
          ninetyDaysAgo.setDate(ninetyDaysAgo.getDate() - 90);
          const lastPrompt = settings.lastReviewPrompt;
          const cooldownOk = !lastPrompt || new Date(lastPrompt) < ninetyDaysAgo;
          if (cooldownOk && !settings.hasReviewedApp) {
            const available = await StoreReview.isAvailableAsync();
            if (available) {
              setTimeout(() => StoreReview.requestReview(), 2500);
              // Record prompt so we respect the 90-day cooldown
              const { saveSettings } = await import('../services/storage');
              await saveSettings({ lastReviewPrompt: new Date().toISOString() });
            }
          }
        } catch { /* non-critical */ }
      }
    }
  };

  const handleEmergency = () => {
    navigation.navigate('Emergency');
  };

  const handleRelapse = () => {
    Alert.alert(
      'Log a relapse?',
      'This resets your current streak. Your total clean days and history are preserved.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Yes, reset',
          style: 'destructive',
          onPress: async () => {
            Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning);
            const updated = await recordRelapse();
            setStreak(updated);
            setCheckedInToday(false);
            Alert.alert(
              'Streak reset.',
              `You had ${updated.totalCleanDays} total clean days. Every attempt makes the next one easier.`,
              [{ text: 'Start again', style: 'default' }]
            );
          },
        },
      ]
    );
  };

  if (!streak) {
    return (
      <SafeAreaView style={styles.container}>
        <Text style={styles.loading}>Loading...</Text>
      </SafeAreaView>
    );
  }

  const mode = MODES[streak.mode];
  const nextMilestone = getNextMilestone(streak.currentStreak);
  const progressToNext = streak.currentStreak / nextMilestone;
  const { hours, minutes } = formatDuration(streak.currentStreak);
  const todayIntention = mode.dailyIntentions[streak.currentStreak % mode.dailyIntentions.length];

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scroll}>

        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.modeLabel}>{mode.emoji} {mode.label}</Text>
          <View style={styles.privacyBadge}>
            <Ionicons name="shield-checkmark" size={12} color={Colors.primary} />
            <Text style={styles.privacyText}>Private</Text>
          </View>
        </View>

        {/* Streak counter */}
        <Animated.View style={[styles.streakCard, { transform: [{ scale: celebrationScale }, { scale: pulseAnim }] }]}>
          <Text style={styles.streakNumber}>{streak.currentStreak}</Text>
          <Text style={styles.streakUnit}>DAYS</Text>
          <Text style={styles.streakTime}>{hours}h {minutes}m into today</Text>
        </Animated.View>

        {/* Progress to next milestone */}
        <View style={styles.milestoneCard}>
          <View style={styles.milestoneHeader}>
            <Text style={styles.milestoneLabel}>Next milestone</Text>
            <Text style={styles.milestoneDayCount}>Day {nextMilestone}</Text>
          </View>
          <View style={styles.progressBar}>
            <View style={[styles.progressFill, { width: `${Math.min(progressToNext * 100, 100)}%` }]} />
          </View>
          <Text style={styles.milestoneRemaining}>{nextMilestone - streak.currentStreak} days to go</Text>
        </View>

        {/* Daily intention */}
        <View style={styles.intentionCard}>
          <Text style={styles.intentionLabel}>TODAY'S INTENTION</Text>
          <Text style={styles.intentionText}>"{todayIntention}"</Text>
        </View>

        {/* Stats row */}
        <View style={styles.statsRow}>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{streak.longestStreak}</Text>
            <Text style={styles.statLabel}>Best streak</Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{streak.totalCleanDays}</Text>
            <Text style={styles.statLabel}>Total clean days</Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{streak.totalAttempts}</Text>
            <Text style={styles.statLabel}>Attempts</Text>
          </View>
        </View>

        {/* Check in */}
        <TouchableOpacity
          style={[styles.checkInButton, checkedInToday && styles.checkInButtonDone]}
          onPress={handleCheckIn}
        >
          <Ionicons name={checkedInToday ? 'checkmark-circle' : 'checkmark-circle-outline'} size={24} color={checkedInToday ? Colors.success : Colors.background} />
          <Text style={[styles.checkInText, checkedInToday && styles.checkInTextDone]}>
            {checkedInToday ? 'Checked in today' : 'Check in for today'}
          </Text>
        </TouchableOpacity>

        {/* Emergency and relapse */}
        <View style={styles.actionRow}>
          <TouchableOpacity style={styles.emergencyButton} onPress={handleEmergency}>
            <Ionicons name="warning-outline" size={18} color={Colors.accentAlt} />
            <Text style={styles.emergencyText}>Emergency</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.relapseButton} onPress={handleRelapse}>
            <Ionicons name="refresh-outline" size={18} color={Colors.textTertiary} />
            <Text style={styles.relapseText}>Log relapse</Text>
          </TouchableOpacity>
        </View>

      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  scroll: { paddingHorizontal: Spacing.lg, paddingBottom: Spacing.xxl },
  loading: { ...Typography.body, textAlign: 'center', marginTop: 100 },
  header: {
    flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
    paddingVertical: Spacing.lg,
  },
  modeLabel: { ...Typography.h3 },
  privacyBadge: {
    flexDirection: 'row', alignItems: 'center', gap: 4,
    backgroundColor: Colors.privacyBadge, paddingHorizontal: Spacing.sm, paddingVertical: 4,
    borderRadius: Radius.full,
  },
  privacyText: { ...Typography.tiny, color: Colors.primary, fontWeight: '600' },
  streakCard: {
    backgroundColor: Colors.surface, borderRadius: Radius.xl, padding: Spacing.xxl,
    alignItems: 'center', marginBottom: Spacing.lg, borderWidth: 2, borderColor: Colors.primary,
  },
  streakNumber: { fontSize: 80, fontWeight: '900', color: Colors.primary, lineHeight: 88 },
  streakUnit: { fontSize: 16, fontWeight: '800', color: Colors.textSecondary, letterSpacing: 4, marginBottom: Spacing.xs },
  streakTime: { ...Typography.label },
  milestoneCard: {
    backgroundColor: Colors.surface, borderRadius: Radius.lg, padding: Spacing.lg, marginBottom: Spacing.md,
  },
  milestoneHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: Spacing.sm },
  milestoneLabel: { ...Typography.label, textTransform: 'uppercase', letterSpacing: 1 },
  milestoneDayCount: { ...Typography.label, color: Colors.primary, fontWeight: '700' },
  progressBar: { height: 6, backgroundColor: Colors.border, borderRadius: 3, marginBottom: Spacing.xs },
  progressFill: { height: 6, backgroundColor: Colors.primary, borderRadius: 3 },
  milestoneRemaining: { ...Typography.tiny, textAlign: 'right' },
  intentionCard: {
    backgroundColor: Colors.surfaceAlt, borderRadius: Radius.lg, padding: Spacing.lg, marginBottom: Spacing.md,
    borderLeftWidth: 3, borderLeftColor: Colors.primary,
  },
  intentionLabel: { ...Typography.tiny, textTransform: 'uppercase', letterSpacing: 2, marginBottom: Spacing.xs },
  intentionText: { ...Typography.body, fontStyle: 'italic', lineHeight: 24, color: Colors.text },
  statsRow: {
    flexDirection: 'row', backgroundColor: Colors.surface, borderRadius: Radius.lg,
    padding: Spacing.md, marginBottom: Spacing.lg,
  },
  statItem: { flex: 1, alignItems: 'center' },
  statDivider: { width: 1, backgroundColor: Colors.border },
  statValue: { ...Typography.h2, color: Colors.primary },
  statLabel: { ...Typography.tiny, marginTop: 4 },
  checkInButton: {
    backgroundColor: Colors.primary, flexDirection: 'row', alignItems: 'center',
    justifyContent: 'center', padding: Spacing.lg, borderRadius: Radius.lg,
    gap: Spacing.sm, marginBottom: Spacing.md,
  },
  checkInButtonDone: { backgroundColor: Colors.surface, borderWidth: 2, borderColor: Colors.success },
  checkInText: { ...Typography.body, fontWeight: '700', color: Colors.background, fontSize: 18 },
  checkInTextDone: { color: Colors.success },
  actionRow: { flexDirection: 'row', gap: Spacing.md },
  emergencyButton: {
    flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center',
    backgroundColor: Colors.surface, padding: Spacing.md, borderRadius: Radius.lg,
    borderWidth: 2, borderColor: Colors.accentAlt, gap: Spacing.xs,
  },
  emergencyText: { ...Typography.body, color: Colors.accentAlt, fontWeight: '700' },
  relapseButton: {
    flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center',
    backgroundColor: Colors.surface, padding: Spacing.md, borderRadius: Radius.lg, gap: Spacing.xs,
  },
  relapseText: { ...Typography.body, color: Colors.textTertiary },
});
