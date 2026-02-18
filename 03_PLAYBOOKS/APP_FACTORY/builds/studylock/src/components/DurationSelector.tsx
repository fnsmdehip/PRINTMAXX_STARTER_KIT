import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { COLORS, SESSION_DURATIONS } from '../utils/constants';

interface DurationSelectorProps {
  selectedDuration: number;
  onSelectDuration: (duration: number) => void;
  customDuration?: number;
  onCustomDurationChange?: (duration: number) => void;
  isPremium?: boolean;
  maxFreeDuration?: number;
}

export const DurationSelector: React.FC<DurationSelectorProps> = ({
  selectedDuration,
  onSelectDuration,
  isPremium = false,
  maxFreeDuration = 25,
}) => {
  const isLocked = (duration: number) => !isPremium && duration > maxFreeDuration;

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Session Length</Text>
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.scrollContainer}
      >
        {SESSION_DURATIONS.map((duration) => {
          const locked = isLocked(duration);
          const isSelected = selectedDuration === duration;

          return (
            <TouchableOpacity
              key={duration}
              style={[
                styles.option,
                isSelected && styles.optionSelected,
                locked && styles.optionLocked,
              ]}
              onPress={() => !locked && onSelectDuration(duration)}
              activeOpacity={locked ? 1 : 0.7}
            >
              <Text
                style={[
                  styles.duration,
                  isSelected && styles.durationSelected,
                  locked && styles.durationLocked,
                ]}
              >
                {duration}
              </Text>
              <Text
                style={[
                  styles.unit,
                  isSelected && styles.unitSelected,
                  locked && styles.unitLocked,
                ]}
              >
                min
              </Text>
              {locked && (
                <View style={styles.lockBadge}>
                  <Text style={styles.lockIcon}>PRO</Text>
                </View>
              )}
            </TouchableOpacity>
          );
        })}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginVertical: 16,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.textSecondary,
    marginBottom: 12,
    paddingHorizontal: 16,
  },
  scrollContainer: {
    paddingHorizontal: 16,
    gap: 12,
  },
  option: {
    width: 80,
    height: 80,
    borderRadius: 16,
    backgroundColor: COLORS.surface,
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
  },
  optionSelected: {
    backgroundColor: COLORS.primary,
  },
  optionLocked: {
    backgroundColor: COLORS.surfaceAlt,
    opacity: 0.7,
  },
  duration: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
  },
  durationSelected: {
    color: COLORS.white,
  },
  durationLocked: {
    color: COLORS.textMuted,
  },
  unit: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: -4,
  },
  unitSelected: {
    color: COLORS.white,
    opacity: 0.8,
  },
  unitLocked: {
    color: COLORS.textMuted,
  },
  lockBadge: {
    position: 'absolute',
    top: -4,
    right: -4,
    backgroundColor: COLORS.accent,
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 8,
  },
  lockIcon: {
    fontSize: 8,
    fontWeight: '700',
    color: COLORS.white,
  },
});

export default DurationSelector;
