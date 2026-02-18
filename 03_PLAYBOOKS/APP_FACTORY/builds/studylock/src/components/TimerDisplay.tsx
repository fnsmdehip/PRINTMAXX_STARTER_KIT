import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import Svg, { Circle } from 'react-native-svg';
import Animated, {
  useAnimatedProps,
  withTiming,
  Easing,
} from 'react-native-reanimated';
import { COLORS } from '../utils/constants';
import { formatTime, calculateTimeProgress } from '../utils/timer';

const AnimatedCircle = Animated.createAnimatedComponent(Circle);

interface TimerDisplayProps {
  timeRemaining: number;
  totalTime: number;
  isBreak?: boolean;
  size?: number;
  strokeWidth?: number;
}

export const TimerDisplay: React.FC<TimerDisplayProps> = ({
  timeRemaining,
  totalTime,
  isBreak = false,
  size = 280,
  strokeWidth = 12,
}) => {
  const center = size / 2;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = calculateTimeProgress(timeRemaining, totalTime);

  const animatedProps = useAnimatedProps(() => {
    const strokeDashoffset = withTiming(circumference * (1 - progress), {
      duration: 300,
      easing: Easing.linear,
    });

    return {
      strokeDashoffset,
    };
  });

  const primaryColor = isBreak ? COLORS.secondary : COLORS.primary;
  const timeString = formatTime(timeRemaining);

  return (
    <View style={[styles.container, { width: size, height: size }]}>
      <Svg width={size} height={size} style={styles.svg}>
        {/* Background circle */}
        <Circle
          cx={center}
          cy={center}
          r={radius}
          stroke={COLORS.surfaceAlt}
          strokeWidth={strokeWidth}
          fill="none"
        />
        {/* Progress circle */}
        <AnimatedCircle
          cx={center}
          cy={center}
          r={radius}
          stroke={primaryColor}
          strokeWidth={strokeWidth}
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          animatedProps={animatedProps}
          transform={`rotate(-90 ${center} ${center})`}
        />
      </Svg>

      <View style={styles.timeContainer}>
        <Text style={[styles.time, { color: primaryColor }]}>{timeString}</Text>
        <Text style={styles.label}>{isBreak ? 'Break Time' : 'Focus Time'}</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    position: 'relative',
    alignItems: 'center',
    justifyContent: 'center',
  },
  svg: {
    position: 'absolute',
  },
  timeContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  time: {
    fontSize: 56,
    fontWeight: '700',
    letterSpacing: 2,
  },
  label: {
    fontSize: 16,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
});

export default TimerDisplay;
