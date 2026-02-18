import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Routine } from '../types';
import { COLORS } from '../utils/constants';
import { formatDuration } from '../utils/dateUtils';

interface RoutineCardProps {
  routine: Routine;
  isCompleted: boolean;
  onPress: () => void;
}

const ROUTINE_ICONS: Record<string, keyof typeof Ionicons.glyphMap> = {
  morning_skincare: 'sunny-outline',
  evening_skincare: 'moon-outline',
  mewing: 'happy-outline',
  facial_exercises: 'fitness-outline',
  debloating: 'water-outline',
  posture: 'body-outline',
};

export function RoutineCard({ routine, isCompleted, onPress }: RoutineCardProps) {
  const icon = ROUTINE_ICONS[routine.type] || 'checkmark-circle-outline';

  return (
    <TouchableOpacity
      style={[styles.container, isCompleted && styles.completed]}
      onPress={onPress}
      disabled={isCompleted}
    >
      <View
        style={[
          styles.iconContainer,
          isCompleted && styles.iconCompleted,
        ]}
      >
        {isCompleted ? (
          <Ionicons name="checkmark" size={24} color={COLORS.surface} />
        ) : (
          <Ionicons name={icon} size={24} color={COLORS.primary} />
        )}
      </View>

      <View style={styles.content}>
        <Text
          style={[
            styles.title,
            isCompleted && styles.titleCompleted,
          ]}
        >
          {routine.name}
        </Text>
        <Text style={styles.description}>{routine.description}</Text>
        <View style={styles.meta}>
          <Ionicons name="time-outline" size={14} color={COLORS.textSecondary} />
          <Text style={styles.duration}>
            {formatDuration(routine.totalDuration)}
          </Text>
          {routine.exercises.length > 0 && (
            <>
              <Text style={styles.separator}>|</Text>
              <Text style={styles.exercises}>
                {routine.exercises.length} exercises
              </Text>
            </>
          )}
        </View>
      </View>

      <Ionicons
        name={isCompleted ? 'checkmark-circle' : 'chevron-forward'}
        size={24}
        color={isCompleted ? COLORS.success : COLORS.textLight}
      />
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  completed: {
    backgroundColor: '#F0FFF4',
    borderWidth: 1,
    borderColor: COLORS.success,
  },
  iconContainer: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: COLORS.primaryLight,
    alignItems: 'center',
    justifyContent: 'center',
  },
  iconCompleted: {
    backgroundColor: COLORS.success,
  },
  content: {
    flex: 1,
    marginHorizontal: 12,
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  titleCompleted: {
    textDecorationLine: 'line-through',
    color: COLORS.textSecondary,
  },
  description: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginBottom: 6,
  },
  meta: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  duration: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
  separator: {
    color: COLORS.textLight,
    marginHorizontal: 4,
  },
  exercises: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
});
