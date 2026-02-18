import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';

import { useUserStore } from '../../src/stores/userStore';
import { useDailyLogStore } from '../../src/stores/dailyLogStore';
import { StreakBadge } from '../../src/components/StreakBadge';
import { ProgressRing } from '../../src/components/ProgressRing';
import { WaterTracker } from '../../src/components/WaterTracker';
import { MewingTimer } from '../../src/components/MewingTimer';
import { DebloatCard } from '../../src/components/DebloatCard';
import { COLORS, DEFAULT_WATER_GOAL, DEFAULT_MEWING_GOAL } from '../../src/utils/constants';
import { getRoutinesForGender, ROUTINES } from '../../src/data/exercises';

export default function HomeScreen() {
  const { settings, streak, subscription } = useUserStore();
  const {
    getTodayLog,
    addWater,
    setSleepHours,
    setSodiumLevel,
    startMewingSession,
    endMewingSession,
    getTodayMewingMinutes,
    currentMewingSession,
  } = useDailyLogStore();

  const todayLog = getTodayLog();
  const mewingMinutes = getTodayMewingMinutes();
  const dailyRoutines = getRoutinesForGender(settings.gender).slice(0, 3);

  // Calculate daily progress
  const waterProgress = Math.min(todayLog.waterIntake / settings.dailyGoals.waterIntake, 1) * 100;
  const mewingProgress = Math.min(mewingMinutes / settings.dailyGoals.mewingMinutes, 1) * 100;
  const routineProgress =
    (todayLog.completedRoutines.length / settings.dailyGoals.routinesToComplete.length) * 100;
  const overallProgress = Math.round((waterProgress + mewingProgress + routineProgress) / 3);

  const handleSleepPress = () => {
    Alert.prompt(
      'Log Sleep',
      'How many hours did you sleep last night?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Save',
          onPress: (text: string | undefined) => {
            const hours = parseFloat(text || '0');
            if (hours > 0 && hours <= 24) {
              Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
              setSleepHours(hours);
            }
          },
        },
      ],
      'plain-text',
      todayLog.sleepHours > 0 ? todayLog.sleepHours.toString() : '',
      'number-pad'
    );
  };

  const handleSodiumPress = () => {
    Alert.alert(
      'Sodium Intake',
      'How was your sodium intake today?',
      [
        {
          text: 'Low (<1500mg)',
          onPress: () => {
            Haptics.selectionAsync();
            setSodiumLevel('low');
          },
        },
        {
          text: 'Medium (1500-2500mg)',
          onPress: () => {
            Haptics.selectionAsync();
            setSodiumLevel('medium');
          },
        },
        {
          text: 'High (>2500mg)',
          onPress: () => {
            Haptics.selectionAsync();
            setSodiumLevel('high');
          },
        },
      ],
      { cancelable: true }
    );
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>Good morning</Text>
            <Text style={styles.title}>Your Daily Glow</Text>
          </View>
          <StreakBadge streak={streak.currentStreak} />
        </View>

        {/* Trial banner */}
        {subscription.isInTrial && !subscription.isSubscribed && (
          <TouchableOpacity
            style={styles.trialBanner}
            onPress={() => router.push('/paywall')}
          >
            <Ionicons name="time-outline" size={18} color={COLORS.warning} />
            <Text style={styles.trialText}>
              {subscription.trialDaysRemaining} days left in trial
            </Text>
            <Ionicons name="chevron-forward" size={18} color={COLORS.warning} />
          </TouchableOpacity>
        )}

        {/* Daily Progress Overview */}
        <View style={styles.progressCard}>
          <View style={styles.progressHeader}>
            <Text style={styles.sectionTitle}>Today's Progress</Text>
            <Text style={styles.progressPercent}>{overallProgress}%</Text>
          </View>
          <View style={styles.progressRings}>
            <View style={styles.progressRingItem}>
              <ProgressRing
                progress={waterProgress}
                size={70}
                strokeWidth={6}
                color={COLORS.secondary}
                value={`${Math.round(todayLog.waterIntake / 1000 * 10) / 10}L`}
              />
              <Text style={styles.ringLabel}>Water</Text>
            </View>
            <View style={styles.progressRingItem}>
              <ProgressRing
                progress={mewingProgress}
                size={70}
                strokeWidth={6}
                color={COLORS.primary}
                value={`${mewingMinutes}m`}
              />
              <Text style={styles.ringLabel}>Mewing</Text>
            </View>
            <View style={styles.progressRingItem}>
              <ProgressRing
                progress={routineProgress}
                size={70}
                strokeWidth={6}
                color={COLORS.success}
                value={`${todayLog.completedRoutines.length}/${settings.dailyGoals.routinesToComplete.length}`}
              />
              <Text style={styles.ringLabel}>Routines</Text>
            </View>
          </View>
        </View>

        {/* Mewing Timer */}
        <MewingTimer
          isActive={!!currentMewingSession}
          onStart={startMewingSession}
          onStop={endMewingSession}
          todayMinutes={mewingMinutes}
          goalMinutes={settings.dailyGoals.mewingMinutes}
        />

        {/* Water Tracker */}
        <View style={styles.section}>
          <WaterTracker
            current={todayLog.waterIntake}
            goal={settings.dailyGoals.waterIntake}
            onAdd={(ml) => {
              Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
              addWater(ml);
            }}
          />
        </View>

        {/* Debloat Tracker */}
        <View style={styles.section}>
          <DebloatCard
            sleepHours={todayLog.sleepHours}
            sodiumLevel={todayLog.sodiumLevel}
            onSleepPress={handleSleepPress}
            onSodiumPress={handleSodiumPress}
          />
        </View>

        {/* Quick Routines */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Today's Routines</Text>
            <TouchableOpacity onPress={() => router.push('/(tabs)/routines')}>
              <Text style={styles.seeAllText}>See all</Text>
            </TouchableOpacity>
          </View>
          {dailyRoutines.map((routine) => (
            <TouchableOpacity
              key={routine.id}
              style={styles.quickRoutineCard}
              onPress={() =>
                router.push({
                  pathname: '/routine-player',
                  params: { routineId: routine.id },
                })
              }
            >
              <View style={styles.quickRoutineLeft}>
                <Text style={styles.quickRoutineName}>{routine.name}</Text>
                <Text style={styles.quickRoutineDuration}>
                  {Math.round(routine.totalDuration / 60)} min
                </Text>
              </View>
              {todayLog.completedRoutines.includes(routine.id) ? (
                <Ionicons name="checkmark-circle" size={24} color={COLORS.success} />
              ) : (
                <Ionicons name="play-circle-outline" size={24} color={COLORS.primary} />
              )}
            </TouchableOpacity>
          ))}
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
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 40,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  greeting: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  trialBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFF8E1',
    padding: 12,
    borderRadius: 12,
    marginBottom: 20,
    gap: 8,
  },
  trialText: {
    flex: 1,
    fontSize: 14,
    color: COLORS.text,
  },
  progressCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  progressHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  progressPercent: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.primary,
  },
  progressRings: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  progressRingItem: {
    alignItems: 'center',
  },
  ringLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: 8,
  },
  section: {
    marginBottom: 16,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
  },
  seeAllText: {
    fontSize: 14,
    color: COLORS.primary,
    fontWeight: '500',
  },
  quickRoutineCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: COLORS.surface,
    padding: 16,
    borderRadius: 12,
    marginBottom: 8,
  },
  quickRoutineLeft: {},
  quickRoutineName: {
    fontSize: 15,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  quickRoutineDuration: {
    fontSize: 13,
    color: COLORS.textSecondary,
  },
});
