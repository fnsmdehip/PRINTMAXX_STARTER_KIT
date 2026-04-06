import React, { useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  interpolateColor,
  Easing,
} from 'react-native-reanimated';
import { colors, typography } from '../theme';
import { Verdict } from '../utils/types';

interface ScoreGaugeProps {
  score: number;
  verdict: Verdict;
  confidence: number;
  size?: number;
}

const VERDICT_LABELS: Record<Verdict, string> = {
  truthful: 'TRUTHFUL',
  deceptive: 'DECEPTIVE',
  uncertain: 'UNCERTAIN',
  scanning: 'ANALYZING...',
};

const VERDICT_COLORS: Record<Verdict, string> = {
  truthful: colors.accent.success,
  deceptive: colors.accent.danger,
  uncertain: colors.accent.warning,
  scanning: colors.accent.primary,
};

export function ScoreGauge({ score, verdict, confidence, size = 200 }: ScoreGaugeProps) {
  const animatedScore = useSharedValue(0);
  const animatedColor = useSharedValue(0);

  useEffect(() => {
    animatedScore.value = withTiming(score / 100, {
      duration: 800,
      easing: Easing.out(Easing.cubic),
    });

    const colorIndex = verdict === 'truthful' ? 0
      : verdict === 'uncertain' ? 0.5
      : verdict === 'deceptive' ? 1
      : 0.25;
    animatedColor.value = withTiming(colorIndex, { duration: 600 });
  }, [score, verdict]);

  const ringStyle = useAnimatedStyle(() => {
    const borderColor = interpolateColor(
      animatedColor.value,
      [0, 0.25, 0.5, 1],
      [colors.accent.success, colors.accent.primary, colors.accent.warning, colors.accent.danger]
    );

    return {
      borderColor,
      borderWidth: 4,
      transform: [{ rotate: `${animatedScore.value * 360}deg` }],
    };
  });

  const progressStyle = useAnimatedStyle(() => ({
    height: `${animatedScore.value * 100}%`,
    backgroundColor: interpolateColor(
      animatedColor.value,
      [0, 0.25, 0.5, 1],
      [colors.accent.success, colors.accent.primary, colors.accent.warning, colors.accent.danger]
    ),
    opacity: 0.15,
  }));

  const verdictColor = VERDICT_COLORS[verdict];

  return (
    <View style={[styles.container, { width: size, height: size }]}>
      <Animated.View
        style={[
          styles.outerRing,
          { width: size, height: size, borderRadius: size / 2 },
          ringStyle,
        ]}
      />
      <View
        style={[
          styles.innerCircle,
          {
            width: size - 16,
            height: size - 16,
            borderRadius: (size - 16) / 2,
          },
        ]}
      >
        <View style={styles.progressContainer}>
          <Animated.View style={[styles.progressFill, progressStyle]} />
        </View>
        <Text style={[styles.score, { color: verdictColor }]}>{score}</Text>
        <Text style={[styles.verdictLabel, { color: verdictColor }]}>
          {VERDICT_LABELS[verdict]}
        </Text>
        <Text style={styles.confidence}>{confidence}% confidence</Text>
      </View>
      <View
        style={[
          styles.glow,
          {
            width: size + 40,
            height: size + 40,
            borderRadius: (size + 40) / 2,
            backgroundColor: verdictColor,
          },
        ]}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  outerRing: {
    position: 'absolute',
  },
  innerCircle: {
    backgroundColor: colors.bg.secondary,
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
    zIndex: 1,
  },
  progressContainer: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'flex-end',
  },
  progressFill: {
    width: '100%',
  },
  score: {
    fontSize: 56,
    fontWeight: '800',
    letterSpacing: -2,
    zIndex: 2,
  },
  verdictLabel: {
    fontSize: 14,
    fontWeight: '700',
    letterSpacing: 3,
    marginTop: 2,
    zIndex: 2,
  },
  confidence: {
    fontSize: 12,
    color: colors.text.tertiary,
    marginTop: 4,
    zIndex: 2,
  },
  glow: {
    position: 'absolute',
    opacity: 0.06,
    zIndex: 0,
  },
});
