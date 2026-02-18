import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { COLORS } from '../../utils/constants';
import type { Habit } from '../../types';

interface HabitItemProps {
  habit: Habit;
  completed: boolean;
  onPress: () => void;
}

export function HabitItem({ habit, completed, onPress }: HabitItemProps) {
  return (
    <TouchableOpacity style={styles.container} onPress={onPress}>
      <Text style={styles.checkbox}>
        {completed ? '✓' : '○'}
      </Text>
      <Text style={[styles.name, completed && styles.completed]}>
        {habit.name}
      </Text>
      {habit.isPremium && <Text style={styles.premium}>✨</Text>}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
  },
  checkbox: {
    fontSize: 20,
    marginRight: 12,
    color: '#4F46E5',
    width: 24,
  },
  name: {
    fontSize: 16,
    color: COLORS.text,
    flex: 1,
  },
  completed: {
    color: COLORS.textSecondary,
    textDecorationLine: 'line-through',
  },
  premium: {
    marginLeft: 8,
  },
});
