import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Colors, PRAYER_DURATIONS } from '../constants';

interface DurationPickerProps {
  selectedDuration: number;
  onSelect: (duration: number) => void;
  isPremium?: boolean;
}

export function DurationPicker({
  selectedDuration,
  onSelect,
  isPremium = false,
}: DurationPickerProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.label}>Prayer Duration</Text>
      <View style={styles.options}>
        {PRAYER_DURATIONS.map((duration) => {
          const isSelected = selectedDuration === duration.value;
          const isLocked = !isPremium && duration.value > 15;

          return (
            <TouchableOpacity
              key={duration.value}
              style={[
                styles.option,
                isSelected && styles.selectedOption,
                isLocked && styles.lockedOption,
              ]}
              onPress={() => !isLocked && onSelect(duration.value)}
              disabled={isLocked}
            >
              <Text
                style={[
                  styles.optionText,
                  isSelected && styles.selectedText,
                  isLocked && styles.lockedText,
                ]}
              >
                {duration.label}
              </Text>
              {isLocked && <Text style={styles.lockIcon}>Pro</Text>}
            </TouchableOpacity>
          );
        })}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 16,
  },
  label: {
    fontSize: 14,
    color: Colors.textSecondary,
    marginBottom: 12,
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  options: {
    flexDirection: 'row',
    gap: 12,
  },
  option: {
    flex: 1,
    paddingVertical: 16,
    paddingHorizontal: 8,
    borderRadius: 12,
    backgroundColor: Colors.background,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: 'transparent',
  },
  selectedOption: {
    backgroundColor: Colors.primary,
    borderColor: Colors.primary,
  },
  lockedOption: {
    opacity: 0.6,
  },
  optionText: {
    fontSize: 16,
    fontWeight: '600',
    color: Colors.text,
  },
  selectedText: {
    color: Colors.white,
  },
  lockedText: {
    color: Colors.textSecondary,
  },
  lockIcon: {
    fontSize: 10,
    color: Colors.primary,
    fontWeight: '700',
    marginTop: 4,
    textTransform: 'uppercase',
  },
});
