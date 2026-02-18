import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../utils/constants';

interface StreakBadgeProps {
  streak: number;
  size?: 'small' | 'medium' | 'large';
}

export function StreakBadge({ streak, size = 'medium' }: StreakBadgeProps) {
  const sizeConfig = {
    small: { icon: 16, text: 14, padding: 6 },
    medium: { icon: 20, text: 18, padding: 10 },
    large: { icon: 28, text: 24, padding: 14 },
  };

  const config = sizeConfig[size];
  const isActive = streak > 0;

  return (
    <View
      style={[
        styles.container,
        { padding: config.padding },
        isActive ? styles.active : styles.inactive,
      ]}
    >
      <Ionicons
        name="flame"
        size={config.icon}
        color={isActive ? COLORS.warning : COLORS.disabled}
      />
      <Text
        style={[
          styles.text,
          { fontSize: config.text },
          isActive ? styles.activeText : styles.inactiveText,
        ]}
      >
        {streak}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    borderRadius: 20,
    gap: 4,
  },
  active: {
    backgroundColor: '#FFF3E0',
  },
  inactive: {
    backgroundColor: COLORS.border,
  },
  text: {
    fontWeight: 'bold',
  },
  activeText: {
    color: COLORS.warning,
  },
  inactiveText: {
    color: COLORS.disabled,
  },
});
