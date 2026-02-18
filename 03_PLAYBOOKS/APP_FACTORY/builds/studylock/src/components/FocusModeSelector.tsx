import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, FOCUS_MODES } from '../utils/constants';
import { FocusMode } from '../types';

interface FocusModeSelectorProps {
  selectedMode: FocusMode;
  onSelectMode: (mode: FocusMode) => void;
}

const MODE_ICONS: Record<FocusMode, keyof typeof Ionicons.glyphMap> = {
  pomodoro: 'timer-outline',
  deepWork: 'moon-outline',
  examPrep: 'school-outline',
  custom: 'settings-outline',
};

export const FocusModeSelector: React.FC<FocusModeSelectorProps> = ({
  selectedMode,
  onSelectMode,
}) => {
  const modes = Object.values(FOCUS_MODES);

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Focus Mode</Text>
      <View style={styles.grid}>
        {modes.map((mode) => {
          const isSelected = selectedMode === mode.id;

          return (
            <TouchableOpacity
              key={mode.id}
              style={[styles.card, isSelected && styles.cardSelected]}
              onPress={() => onSelectMode(mode.id)}
              activeOpacity={0.7}
            >
              <View
                style={[
                  styles.iconContainer,
                  isSelected && styles.iconContainerSelected,
                ]}
              >
                <Ionicons
                  name={MODE_ICONS[mode.id]}
                  size={24}
                  color={isSelected ? COLORS.white : COLORS.primary}
                />
              </View>
              <Text style={[styles.name, isSelected && styles.nameSelected]}>
                {mode.name}
              </Text>
              <Text
                style={[
                  styles.description,
                  isSelected && styles.descriptionSelected,
                ]}
              >
                {mode.description}
              </Text>
            </TouchableOpacity>
          );
        })}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.textSecondary,
    marginBottom: 12,
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  card: {
    width: '48%',
    padding: 16,
    borderRadius: 16,
    backgroundColor: COLORS.surface,
    alignItems: 'center',
  },
  cardSelected: {
    backgroundColor: COLORS.primary,
  },
  iconContainer: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: COLORS.primary + '15',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
  },
  iconContainerSelected: {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
  },
  name: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  nameSelected: {
    color: COLORS.white,
  },
  description: {
    fontSize: 12,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  descriptionSelected: {
    color: COLORS.white,
    opacity: 0.8,
  },
});

export default FocusModeSelector;
