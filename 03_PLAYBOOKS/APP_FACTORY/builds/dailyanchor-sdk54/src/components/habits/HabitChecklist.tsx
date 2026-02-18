import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { COLORS } from '../../utils/constants';
import { useHabitStore } from '../../store';
import { Card } from '../common';

interface HabitChecklistProps {
  date: string;
  onPremiumRequired: () => void;
}

export function HabitChecklist({ date, onPremiumRequired }: HabitChecklistProps) {
  const { habits, toggleHabitCompletion, isHabitCompleted } = useHabitStore();

  const handleToggle = (habitId: string) => {
    toggleHabitCompletion(habitId, date);
  };

  return (
    <Card>
      <Text style={styles.title}>Today's Habits</Text>
      {habits.map((habit) => {
        const completed = isHabitCompleted(habit.id, date);
        return (
          <TouchableOpacity
            key={habit.id}
            style={styles.habitItem}
            onPress={() => {
              if (habit.isPremium) {
                onPremiumRequired();
              } else {
                handleToggle(habit.id);
              }
            }}
          >
            <Text style={styles.checkbox}>
              {completed ? '✓' : '○'}
            </Text>
            <Text style={[styles.name, completed && styles.completed]}>
              {habit.name}
            </Text>
            {habit.isPremium && <Text style={styles.premium}>✨</Text>}
          </TouchableOpacity>
        );
      })}
    </Card>
  );
}

const styles = StyleSheet.create({
  title: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 12,
  },
  habitItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  checkbox: {
    fontSize: 20,
    marginRight: 12,
    color: COLORS.primary,
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
