import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

import { useUserStore } from '../../src/stores/userStore';
import { useDailyLogStore } from '../../src/stores/dailyLogStore';
import { RoutineCard } from '../../src/components/RoutineCard';
import { getRoutinesForGender, ROUTINES } from '../../src/data/exercises';
import { COLORS } from '../../src/utils/constants';

export default function RoutinesScreen() {
  const { settings } = useUserStore();
  const { getTodayLog } = useDailyLogStore();

  const todayLog = getTodayLog();
  const routines = getRoutinesForGender(settings.gender);

  // Group by type
  const skincare = routines.filter((r) =>
    ['morning_skincare', 'evening_skincare'].includes(r.type)
  );
  const exercises = routines.filter((r) => r.type === 'facial_exercises');
  const other = routines.filter((r) =>
    ['mewing', 'debloating', 'posture'].includes(r.type)
  );

  const renderSection = (title: string, sectionRoutines: typeof routines) => {
    if (sectionRoutines.length === 0) return null;

    return (
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>{title}</Text>
        {sectionRoutines.map((routine) => (
          <View key={routine.id} style={styles.cardWrapper}>
            <RoutineCard
              routine={routine}
              isCompleted={todayLog.completedRoutines.includes(routine.id)}
              onPress={() =>
                router.push({
                  pathname: '/routine-player',
                  params: { routineId: routine.id },
                })
              }
            />
          </View>
        ))}
      </View>
    );
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Routines</Text>
        <Text style={styles.subtitle}>
          {todayLog.completedRoutines.length} of{' '}
          {settings.dailyGoals.routinesToComplete.length} completed today
        </Text>
      </View>

      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Progress Summary */}
        <View style={styles.summaryCard}>
          <View style={styles.summaryRow}>
            <View style={styles.summaryItem}>
              <Text style={styles.summaryValue}>
                {todayLog.completedRoutines.length}
              </Text>
              <Text style={styles.summaryLabel}>Completed</Text>
            </View>
            <View style={styles.summaryDivider} />
            <View style={styles.summaryItem}>
              <Text style={styles.summaryValue}>
                {settings.dailyGoals.routinesToComplete.length -
                  todayLog.completedRoutines.length}
              </Text>
              <Text style={styles.summaryLabel}>Remaining</Text>
            </View>
            <View style={styles.summaryDivider} />
            <View style={styles.summaryItem}>
              <Text style={styles.summaryValue}>{routines.length}</Text>
              <Text style={styles.summaryLabel}>Total</Text>
            </View>
          </View>
        </View>

        {renderSection('Skincare', skincare)}
        {renderSection('Facial Exercises', exercises)}
        {renderSection('Other', other)}

        {/* Tips */}
        <View style={styles.tipsCard}>
          <View style={styles.tipsHeader}>
            <Ionicons name="bulb-outline" size={20} color={COLORS.warning} />
            <Text style={styles.tipsTitle}>Pro Tips</Text>
          </View>
          <Text style={styles.tipsText}>
            For best results, complete morning routines within 1 hour of waking.
            Evening routines should be done at least 30 minutes before sleep.
          </Text>
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
  header: {
    paddingHorizontal: 20,
    paddingTop: 10,
    paddingBottom: 16,
    backgroundColor: COLORS.background,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    paddingTop: 0,
    paddingBottom: 40,
  },
  summaryCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 20,
    marginBottom: 24,
  },
  summaryRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  summaryItem: {
    flex: 1,
    alignItems: 'center',
  },
  summaryValue: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.primary,
  },
  summaryLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  summaryDivider: {
    width: 1,
    height: 40,
    backgroundColor: COLORS.border,
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 12,
  },
  cardWrapper: {
    marginBottom: 12,
  },
  tipsCard: {
    backgroundColor: '#FFF8E1',
    borderRadius: 16,
    padding: 16,
    marginTop: 8,
  },
  tipsHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 8,
  },
  tipsTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
  },
  tipsText: {
    fontSize: 14,
    color: COLORS.text,
    lineHeight: 20,
  },
});
