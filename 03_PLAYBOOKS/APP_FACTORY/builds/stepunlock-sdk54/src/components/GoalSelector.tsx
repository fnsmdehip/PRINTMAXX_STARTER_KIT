import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
} from 'react-native';
import Slider from '@react-native-community/slider';
import { COLORS, MIN_STEP_GOAL, MAX_STEP_GOAL, STEP_GOAL_INCREMENT } from '../utils/constants';
import { STEP_GOAL_PRESETS } from '../types';
import { estimateWalkingTime, formatTimeRemaining, estimateDistance, formatDistance } from '../utils/dateUtils';

interface Props {
  value: number;
  onChange: (value: number) => void;
}

export function GoalSelector({ value, onChange }: Props) {
  const handleSliderChange = (sliderValue: number) => {
    // Round to nearest increment
    const rounded = Math.round(sliderValue / STEP_GOAL_INCREMENT) * STEP_GOAL_INCREMENT;
    onChange(rounded);
  };

  const walkingTime = estimateWalkingTime(value);
  const distance = estimateDistance(value);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Daily step goal</Text>

      <View style={styles.valueContainer}>
        <Text style={styles.value}>{value.toLocaleString()}</Text>
        <Text style={styles.unit}>steps</Text>
      </View>

      <View style={styles.estimatesContainer}>
        <Text style={styles.estimate}>
          About {formatTimeRemaining(walkingTime)} walking
        </Text>
        <Text style={styles.estimate}>
          About {formatDistance(distance)}
        </Text>
      </View>

      <Slider
        style={styles.slider}
        minimumValue={MIN_STEP_GOAL}
        maximumValue={MAX_STEP_GOAL}
        step={STEP_GOAL_INCREMENT}
        value={value}
        onValueChange={handleSliderChange}
        minimumTrackTintColor={COLORS.primary}
        maximumTrackTintColor={COLORS.border}
        thumbTintColor={COLORS.primary}
      />

      <View style={styles.rangeLabels}>
        <Text style={styles.rangeLabel}>{MIN_STEP_GOAL.toLocaleString()}</Text>
        <Text style={styles.rangeLabel}>{MAX_STEP_GOAL.toLocaleString()}</Text>
      </View>

      <View style={styles.presetsContainer}>
        {STEP_GOAL_PRESETS.map((preset) => (
          <TouchableOpacity
            key={preset.value}
            style={[
              styles.presetButton,
              value === preset.value && styles.presetButtonActive,
            ]}
            onPress={() => onChange(preset.value)}
          >
            <Text
              style={[
                styles.presetLabel,
                value === preset.value && styles.presetLabelActive,
              ]}
            >
              {preset.label}
            </Text>
            <Text
              style={[
                styles.presetValue,
                value === preset.value && styles.presetValueActive,
              ]}
            >
              {(preset.value / 1000).toFixed(0)}k
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 16,
    textAlign: 'center',
  },
  valueContainer: {
    flexDirection: 'row',
    alignItems: 'baseline',
    justifyContent: 'center',
    marginBottom: 8,
  },
  value: {
    fontSize: 48,
    fontWeight: 'bold',
    color: COLORS.primary,
  },
  unit: {
    fontSize: 18,
    color: COLORS.textSecondary,
    marginLeft: 8,
  },
  estimatesContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 16,
    marginBottom: 24,
  },
  estimate: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  slider: {
    width: '100%',
    height: 40,
  },
  rangeLabels: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 8,
    marginBottom: 24,
  },
  rangeLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
  presetsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  presetButton: {
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 12,
    backgroundColor: COLORS.surface,
    borderWidth: 1,
    borderColor: COLORS.border,
    alignItems: 'center',
    minWidth: 70,
  },
  presetButtonActive: {
    backgroundColor: COLORS.primary,
    borderColor: COLORS.primary,
  },
  presetLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginBottom: 2,
  },
  presetLabelActive: {
    color: COLORS.surface,
  },
  presetValue: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
  },
  presetValueActive: {
    color: COLORS.surface,
  },
});
