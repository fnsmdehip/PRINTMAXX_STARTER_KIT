import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, DEFAULT_WATER_GOAL } from '../utils/constants';

interface WaterTrackerProps {
  current: number;
  goal?: number;
  onAdd: (ml: number) => void;
}

const QUICK_ADD_OPTIONS = [250, 500, 750];

export function WaterTracker({
  current,
  goal = DEFAULT_WATER_GOAL,
  onAdd,
}: WaterTrackerProps) {
  const progress = Math.min(current / goal, 1);
  const progressPercent = Math.round(progress * 100);
  const remaining = Math.max(goal - current, 0);

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View style={styles.iconContainer}>
          <Ionicons name="water" size={24} color={COLORS.secondary} />
        </View>
        <View style={styles.headerText}>
          <Text style={styles.title}>Water Intake</Text>
          <Text style={styles.subtitle}>
            {current >= goal
              ? 'Goal reached!'
              : `${remaining}ml remaining`}
          </Text>
        </View>
        <Text style={styles.amount}>
          {current / 1000}L / {goal / 1000}L
        </Text>
      </View>

      {/* Progress bar */}
      <View style={styles.progressContainer}>
        <View style={styles.progressBackground}>
          <View
            style={[
              styles.progressFill,
              { width: `${progressPercent}%` },
              current >= goal && styles.progressComplete,
            ]}
          />
        </View>
        <Text style={styles.progressText}>{progressPercent}%</Text>
      </View>

      {/* Quick add buttons */}
      <View style={styles.quickAddContainer}>
        {QUICK_ADD_OPTIONS.map((ml) => (
          <TouchableOpacity
            key={ml}
            style={styles.quickAddButton}
            onPress={() => onAdd(ml)}
          >
            <Ionicons name="add" size={16} color={COLORS.secondary} />
            <Text style={styles.quickAddText}>{ml}ml</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  iconContainer: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#E3F2FD',
    alignItems: 'center',
    justifyContent: 'center',
  },
  headerText: {
    flex: 1,
    marginLeft: 12,
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
  },
  subtitle: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  amount: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.secondary,
  },
  progressContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  progressBackground: {
    flex: 1,
    height: 8,
    backgroundColor: COLORS.border,
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: COLORS.secondary,
    borderRadius: 4,
  },
  progressComplete: {
    backgroundColor: COLORS.success,
  },
  progressText: {
    fontSize: 13,
    fontWeight: '600',
    color: COLORS.textSecondary,
    width: 40,
    textAlign: 'right',
  },
  quickAddContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 16,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
  },
  quickAddButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#E3F2FD',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 20,
    gap: 4,
  },
  quickAddText: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.secondary,
  },
});
