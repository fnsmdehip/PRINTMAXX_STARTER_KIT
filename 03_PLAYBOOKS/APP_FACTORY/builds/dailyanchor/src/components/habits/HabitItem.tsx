import React from 'react';
import {
  TouchableOpacity,
  View,
  Text,
  StyleSheet,
  Animated,
} from 'react-native';
import { Habit } from '../../types';
import { COLORS } from '../../utils/constants';

interface HabitItemProps {
  habit: Habit;
  isCompleted: boolean;
  onToggle: () => void;
  isPremiumLocked?: boolean;
  onPremiumPress?: () => void;
}

export function HabitItem({
  habit,
  isCompleted,
  onToggle,
  isPremiumLocked = false,
  onPremiumPress,
}: HabitItemProps) {
  const handlePress = () => {
    if (isPremiumLocked && onPremiumPress) {
      onPremiumPress();
    } else {
      onToggle();
    }
  };

  const getIconEmoji = (icon: string): string => {
    const iconMap: Record<string, string> = {
      book: '\u{1F4D6}',
      hands: '\u{1F64F}',
      heart: '\u{2764}',
      moon: '\u{1F319}',
      brain: '\u{1F9E0}',
      utensils: '\u{1F374}',
      church: '\u{26EA}',
      'hand-holding-heart': '\u{1F91D}',
    };
    return iconMap[icon] || '\u{2705}';
  };

  return (
    <TouchableOpacity
      style={[
        styles.container,
        isCompleted && styles.completed,
        isPremiumLocked && styles.locked,
      ]}
      onPress={handlePress}
      activeOpacity={0.7}>
      <View style={styles.content}>
        <View
          style={[
            styles.checkbox,
            isCompleted && styles.checkboxCompleted,
          ]}>
          {isCompleted && <Text style={styles.checkmark}>{'\u2713'}</Text>}
        </View>

        <View style={styles.iconContainer}>
          <Text style={styles.icon}>{getIconEmoji(habit.icon)}</Text>
        </View>

        <View style={styles.textContainer}>
          <Text
            style={[
              styles.name,
              isCompleted && styles.nameCompleted,
              isPremiumLocked && styles.nameLocked,
            ]}>
            {habit.name}
          </Text>
          {isPremiumLocked && (
            <Text style={styles.premiumBadge}>Premium</Text>
          )}
        </View>
      </View>

      {isPremiumLocked && (
        <View style={styles.lockIcon}>
          <Text>{'\u{1F512}'}</Text>
        </View>
      )}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: COLORS.card,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  completed: {
    backgroundColor: '#F0FDF4',
    borderColor: COLORS.completed,
  },
  locked: {
    opacity: 0.7,
    backgroundColor: '#F8FAFC',
  },
  content: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  checkbox: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: COLORS.border,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
  },
  checkboxCompleted: {
    backgroundColor: COLORS.completed,
    borderColor: COLORS.completed,
  },
  checkmark: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: 'bold',
  },
  iconContainer: {
    marginRight: 12,
  },
  icon: {
    fontSize: 24,
  },
  textContainer: {
    flex: 1,
  },
  name: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
  },
  nameCompleted: {
    color: COLORS.completed,
  },
  nameLocked: {
    color: COLORS.textSecondary,
  },
  premiumBadge: {
    fontSize: 12,
    color: COLORS.primary,
    fontWeight: '500',
    marginTop: 2,
  },
  lockIcon: {
    marginLeft: 8,
  },
});
