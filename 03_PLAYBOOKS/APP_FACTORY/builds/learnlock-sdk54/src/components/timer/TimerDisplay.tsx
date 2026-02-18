import React from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import Svg, { Circle } from 'react-native-svg';
import { COLORS, TYPOGRAPHY, SPACING } from '../../utils/constants';
import { formatTime } from '../../utils/dateUtils';

interface Props {
  remainingSeconds: number;
  totalSeconds: number;
  isStudying: boolean;
  isBreak: boolean;
}

const { width } = Dimensions.get('window');
const RING_SIZE = width * 0.75;
const STROKE_WIDTH = 12;
const RADIUS = (RING_SIZE - STROKE_WIDTH) / 2;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

export function TimerDisplay({ remainingSeconds, totalSeconds, isStudying, isBreak }: Props) {
  const progress = totalSeconds > 0 ? (totalSeconds - remainingSeconds) / totalSeconds : 0;
  const progressOffset = CIRCUMFERENCE * (1 - progress);

  const activeColor = isBreak ? COLORS.timerBreak : COLORS.timerWork;
  const label = isBreak ? 'Break Time' : isStudying ? 'Focus Time' : 'Ready';

  return (
    <View style={styles.container}>
      <Svg width={RING_SIZE} height={RING_SIZE} style={styles.svg}>
        {/* Background circle */}
        <Circle
          cx={RING_SIZE / 2}
          cy={RING_SIZE / 2}
          r={RADIUS}
          stroke={COLORS.timerBackground}
          strokeWidth={STROKE_WIDTH}
          fill="none"
        />
        {/* Progress circle */}
        <Circle
          cx={RING_SIZE / 2}
          cy={RING_SIZE / 2}
          r={RADIUS}
          stroke={activeColor}
          strokeWidth={STROKE_WIDTH}
          fill="none"
          strokeDasharray={CIRCUMFERENCE}
          strokeDashoffset={progressOffset}
          strokeLinecap="round"
          transform={`rotate(-90 ${RING_SIZE / 2} ${RING_SIZE / 2})`}
        />
      </Svg>

      <View style={styles.textContainer}>
        <Text style={styles.label}>{label}</Text>
        <Text style={[styles.time, { color: activeColor }]}>
          {formatTime(remainingSeconds)}
        </Text>
        {(isStudying || isBreak) && (
          <Text style={styles.remaining}>
            {Math.ceil(remainingSeconds / 60)} min remaining
          </Text>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  svg: {
    position: 'absolute',
  },
  textContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    width: RING_SIZE,
    height: RING_SIZE,
  },
  label: {
    ...TYPOGRAPHY.bodySmall,
    color: COLORS.textSecondary,
    marginBottom: SPACING.xs,
  },
  time: {
    ...TYPOGRAPHY.timer,
    fontVariant: ['tabular-nums'],
  },
  remaining: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textTertiary,
    marginTop: SPACING.xs,
  },
});
