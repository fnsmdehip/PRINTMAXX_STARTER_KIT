import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Spacing, Radius, Typography } from '../constants/theme';
import { MODES, MILESTONE_DAYS } from '../constants/modes';
import { getStreakData } from '../services/storage';
import { StreakData } from '../types';

export default function MilestonesScreen() {
  const [streak, setStreak] = useState<StreakData | null>(null);

  useFocusEffect(useCallback(() => {
    getStreakData().then(data => {
      if (data) setStreak(data);
    });
  }, []));

  if (!streak) return null;

  const mode = MODES[streak.mode];
  const totalCheckIns = streak.checkIns.length;

  const getMilestoneStatus = (day: number): 'achieved' | 'next' | 'locked' => {
    if (streak.currentStreak >= day) return 'achieved';
    const nextMilestoneDay = MILESTONE_DAYS.find(m => m > streak.currentStreak);
    if (nextMilestoneDay === day) return 'next';
    return 'locked';
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scroll}>

        <Text style={styles.heading}>Your Progress</Text>

        {/* Summary stats */}
        <View style={styles.summaryGrid}>
          <View style={styles.summaryItem}>
            <Text style={styles.summaryValue}>{streak.currentStreak}</Text>
            <Text style={styles.summaryLabel}>Current streak</Text>
          </View>
          <View style={styles.summaryItem}>
            <Text style={styles.summaryValue}>{streak.longestStreak}</Text>
            <Text style={styles.summaryLabel}>Best streak</Text>
          </View>
          <View style={styles.summaryItem}>
            <Text style={styles.summaryValue}>{streak.totalCleanDays}</Text>
            <Text style={styles.summaryLabel}>Total clean days</Text>
          </View>
          <View style={styles.summaryItem}>
            <Text style={styles.summaryValue}>{streak.totalAttempts}</Text>
            <Text style={styles.summaryLabel}>Attempts</Text>
          </View>
        </View>

        <Text style={styles.sectionLabel}>MILESTONES</Text>
        {MILESTONE_DAYS.map(day => {
          const status = getMilestoneStatus(day);
          const msg = mode.milestoneMessages[day];
          return (
            <View
              key={day}
              style={[
                styles.milestoneRow,
                status === 'achieved' && styles.milestoneRowAchieved,
                status === 'next' && styles.milestoneRowNext,
              ]}
            >
              <View style={[styles.milestoneBadge, status === 'achieved' && styles.milestoneBadgeAchieved, status === 'next' && styles.milestoneBadgeNext]}>
                {status === 'achieved' ? (
                  <Ionicons name="checkmark" size={16} color={Colors.background} />
                ) : (
                  <Text style={[styles.milestoneDayText, status === 'next' && styles.milestoneDayTextNext]}>{day}d</Text>
                )}
              </View>
              <View style={styles.milestoneContent}>
                <Text style={[styles.milestoneDayLabel, status === 'achieved' && styles.milestoneTextAchieved]}>
                  Day {day}
                </Text>
                {msg && (
                  <Text style={[styles.milestoneMsg, status === 'locked' && styles.milestoneMsgLocked]}>
                    {status === 'locked' ? `Unlock at day ${day}` : msg}
                  </Text>
                )}
              </View>
              {status === 'next' && (
                <View style={styles.nextBadge}>
                  <Text style={styles.nextBadgeText}>NEXT</Text>
                </View>
              )}
            </View>
          );
        })}

        {/* Calendar heat map (simple check-in history) */}
        <Text style={[styles.sectionLabel, { marginTop: Spacing.xl }]}>CHECK-IN HISTORY</Text>
        <View style={styles.heatMap}>
          {Array.from({ length: 30 }).map((_, i) => {
            const d = new Date();
            d.setDate(d.getDate() - (29 - i));
            const dayStr = d.toDateString();
            const checked = streak.checkIns.some(c => new Date(c).toDateString() === dayStr);
            return (
              <View
                key={i}
                style={[styles.heatCell, checked && styles.heatCellActive]}
              />
            );
          })}
        </View>
        <Text style={styles.heatLabel}>Last 30 days  ({totalCheckIns} total check-ins)</Text>

      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  scroll: { paddingHorizontal: Spacing.lg, paddingBottom: Spacing.xxl },
  heading: { ...Typography.h1, paddingVertical: Spacing.lg },
  summaryGrid: {
    flexDirection: 'row', flexWrap: 'wrap', gap: Spacing.sm, marginBottom: Spacing.xl,
  },
  summaryItem: {
    flex: 1, minWidth: '40%', backgroundColor: Colors.surface, padding: Spacing.lg,
    borderRadius: Radius.lg, alignItems: 'center',
  },
  summaryValue: { ...Typography.h1, color: Colors.primary },
  summaryLabel: { ...Typography.tiny, marginTop: 4 },
  sectionLabel: { ...Typography.tiny, textTransform: 'uppercase', letterSpacing: 2, color: Colors.textTertiary, marginBottom: Spacing.md },
  milestoneRow: {
    flexDirection: 'row', alignItems: 'center', gap: Spacing.md,
    backgroundColor: Colors.surface, padding: Spacing.md, borderRadius: Radius.lg,
    marginBottom: Spacing.sm, borderWidth: 1, borderColor: Colors.border,
  },
  milestoneRowAchieved: { borderColor: Colors.success, opacity: 0.85 },
  milestoneRowNext: { borderColor: Colors.primary, borderWidth: 2 },
  milestoneBadge: {
    width: 40, height: 40, borderRadius: 20, backgroundColor: Colors.border,
    alignItems: 'center', justifyContent: 'center',
  },
  milestoneBadgeAchieved: { backgroundColor: Colors.success },
  milestoneBadgeNext: { backgroundColor: Colors.primary },
  milestoneDayText: { ...Typography.label, fontWeight: '700', color: Colors.textSecondary },
  milestoneDayTextNext: { color: Colors.background },
  milestoneContent: { flex: 1 },
  milestoneDayLabel: { ...Typography.body, fontWeight: '600' },
  milestoneTextAchieved: { color: Colors.success },
  milestoneMsg: { ...Typography.label, color: Colors.textSecondary, marginTop: 2 },
  milestoneMsgLocked: { color: Colors.textTertiary },
  nextBadge: {
    backgroundColor: Colors.primary, paddingHorizontal: Spacing.sm, paddingVertical: 3, borderRadius: Radius.full,
  },
  nextBadgeText: { color: Colors.background, fontWeight: '800', fontSize: 10, letterSpacing: 1 },
  heatMap: { flexDirection: 'row', flexWrap: 'wrap', gap: 4 },
  heatCell: { width: 20, height: 20, borderRadius: 4, backgroundColor: Colors.surface },
  heatCellActive: { backgroundColor: Colors.primary },
  heatLabel: { ...Typography.tiny, marginTop: Spacing.sm, color: Colors.textTertiary },
});
