import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Habit } from '../../types';
import { HabitItem } from './HabitItem';
import { Card } from '../common';
import { COLORS } from '../../utils/constants';
import { useHabitStore, useSettingsStore } from '../../store';
import { getToday } from '../../utils/dateUtils';

interface HabitChecklistProps {
  date?: string;
  onPremiumRequired?: () => void;
}

export function HabitChecklist({
  date = getToday(),
  onPremiumRequired,
}: HabitChecklistProps) {
  const { habits, toggleHabitCompletion, isHabitCompleted } = useHabitStore();
  const { isPremium } = useSettingsStore();

  const completedCount = habits.filter((h) =>
    isHabitCompleted(h.id, date)
  ).length;

  const progressPercent =
    habits.length > 0 ? (completedCount / habits.length) * 100 : 0;

  const handleToggle = (habit: Habit) => {
    if (habit.isPremium && !isPremium) {
      onPremiumRequired?.();
      return;
    }
    toggleHabitCompletion(habit.id, date);
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Daily habits</Text>
        <Text style={styles.progress}>
          {completedCount}/{habits.length}
        </Text>
      </View>

      <View style={styles.progressBar}>
        <View
          style={[styles.progressFill, { width: `${progressPercent}%` }]}
        />
      </View>

      <View style={styles.list}>
        {habits.map((habit) => (
          <HabitItem
            key={habit.id}
            habit={habit}
            isCompleted={isHabitCompleted(habit.id, date)}
            onToggle={() => handleToggle(habit)}
            isPremiumLocked={habit.isPremium && !isPremium}
            onPremiumPress={onPremiumRequired}
          />
        ))}
      </View>

      {progressPercent === 100 && (
        <View style={styles.completedBanner}>
          <Text style={styles.completedEmoji}>{'\u{1F389}'}</Text>
          <Text style={styles.completedText}>All done for today</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {},
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  title: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.text,
  },
  progress: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.textSecondary,
  },
  progressBar: {
    height: 6,
    backgroundColor: COLORS.border,
    borderRadius: 3,
    marginBottom: 20,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: COLORS.completed,
    borderRadius: 3,
  },
  list: {},
  completedBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#F0FDF4',
    borderRadius: 12,
    padding: 16,
    marginTop: 8,
  },
  completedEmoji: {
    fontSize: 24,
    marginRight: 8,
  },
  completedText: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.completed,
  },
});
