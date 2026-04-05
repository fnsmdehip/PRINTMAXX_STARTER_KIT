import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import {
  View,
  Text,
  StyleSheet,

  Dimensions,
  Platform,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { SoundTouchable as TouchableOpacity } from '../components/SoundTouchable';
import { CameraView, useCameraPermissions } from 'expo-camera';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  useAnimatedProps,
  withTiming,
  withRepeat,
  withSequence,
  withSpring,
  withDelay,
  Easing,
  interpolate,
  interpolateColor,
  runOnJS,
} from 'react-native-reanimated';
import Svg, { Path, Circle, Line, Defs, RadialGradient, Stop } from 'react-native-svg';
import * as Haptics from 'expo-haptics';

import { colors, spacing, typography, radii } from '../theme';
import { DetectionMode, Verdict } from '../utils/types';
import { useDetectionEngine, DetectionReadings } from '../hooks/useDetectionEngine';
import { playSound, playVerdictReveal } from '../sounds/SoundEngine';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

// DetectionReadings type imported from useDetectionEngine hook

type RouteParams = { mode?: DetectionMode };

interface Props {
  navigation: any;
  route: { params?: RouteParams };
}

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const { width: SCREEN_W, height: SCREEN_H } = Dimensions.get('window');
const CAMERA_HEIGHT = SCREEN_H * 0.36;
const GAUGE_SIZE = 160;
const GAUGE_STROKE = 10;
const GAUGE_RADIUS = (GAUGE_SIZE - GAUGE_STROKE) / 2;
const GAUGE_CIRCUMFERENCE = 2 * Math.PI * GAUGE_RADIUS;

const MODE_TABS: { key: DetectionMode; label: string; icon: string }[] = [
  { key: 'finger', label: 'Finger', icon: 'finger-print' },
  { key: 'face', label: 'Face', icon: 'scan' },
  { key: 'voice', label: 'Voice', icon: 'mic' },
  { key: 'multi', label: 'Multi', icon: 'layers' },
];

const VERDICT_CONFIG: Record<
  Verdict,
  { label: string; colors: readonly [string, string]; glow: string }
> = {
  truthful: {
    label: 'TRUTHFUL',
    colors: colors.gradient.truthful,
    glow: colors.accent.success,
  },
  deceptive: {
    label: 'DECEPTIVE',
    colors: colors.gradient.deceptive,
    glow: colors.accent.danger,
  },
  uncertain: {
    label: 'UNCERTAIN',
    colors: colors.gradient.uncertain,
    glow: colors.accent.warning,
  },
  scanning: {
    label: 'ANALYZING...',
    colors: colors.gradient.scanning,
    glow: colors.accent.primary,
  },
};

// ---------------------------------------------------------------------------
// Animated SVG wrappers
// ---------------------------------------------------------------------------

const AnimatedCircle = Animated.createAnimatedComponent(Circle);
const AnimatedPath = Animated.createAnimatedComponent(Path);

// ---------------------------------------------------------------------------
// REMOVED: Simulated data hook — replaced by useDetectionEngine (real sensors)
// See src/hooks/useDetectionEngine.ts
// ---------------------------------------------------------------------------

// Simulated data hook DELETED. Real sensor hook: useDetectionEngine in src/hooks/

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

/** Mode selection tabs */
function ModeSelector({
  current,
  onSelect,
  isPremium,
}: {
  current: DetectionMode;
  onSelect: (m: DetectionMode) => void;
  isPremium: boolean;
}) {
  return (
    <View style={styles.modeTabs}>
      {MODE_TABS.map((tab) => {
        const active = current === tab.key;
        const locked = tab.key === 'multi' && !isPremium;
        return (
          <TouchableOpacity
            key={tab.key}
            style={[styles.modeTab, active && styles.modeTabActive]}
            onPress={() => {
              if (!locked) onSelect(tab.key);
            }}
            activeOpacity={locked ? 1 : 0.7}
          >
            <Ionicons
              name={tab.icon as any}
              size={18}
              color={active ? colors.accent.primary : locked ? colors.text.tertiary : colors.text.secondary}
            />
            <Text
              style={[
                styles.modeTabLabel,
                active && styles.modeTabLabelActive,
                locked && { color: colors.text.tertiary },
              ]}
            >
              {tab.label}
            </Text>
            {locked && (
              <Ionicons
                name="lock-closed"
                size={10}
                color={colors.text.tertiary}
                style={{ marginLeft: 2, marginTop: -2 }}
              />
            )}
          </TouchableOpacity>
        );
      })}
    </View>
  );
}

/** Scanning grid overlay for camera views */
function ScanOverlay({ variant }: { variant: 'finger' | 'face' }) {
  const scanLine = useSharedValue(0);

  useEffect(() => {
    scanLine.value = withRepeat(
      withTiming(1, { duration: 2400, easing: Easing.inOut(Easing.ease) }),
      -1,
      true,
    );
  }, []);

  const lineStyle = useAnimatedStyle(() => ({
    position: 'absolute' as const,
    left: 0,
    right: 0,
    height: 2,
    top: interpolate(scanLine.value, [0, 1], [0, CAMERA_HEIGHT]),
    backgroundColor: colors.accent.primary,
    opacity: 0.6,
    shadowColor: colors.accent.primary,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.8,
    shadowRadius: 8,
  }));

  return (
    <View style={StyleSheet.absoluteFill} pointerEvents="none">
      {/* Grid lines */}
      <Svg width="100%" height="100%" style={StyleSheet.absoluteFill}>
        {/* Vertical grid lines */}
        {[0.25, 0.5, 0.75].map((pct) => (
          <Line
            key={`v-${pct}`}
            x1={`${pct * 100}%`}
            y1="0"
            x2={`${pct * 100}%`}
            y2="100%"
            stroke={colors.accent.primary}
            strokeOpacity={0.12}
            strokeWidth={0.5}
          />
        ))}
        {/* Horizontal grid lines */}
        {[0.25, 0.5, 0.75].map((pct) => (
          <Line
            key={`h-${pct}`}
            x1="0"
            y1={`${pct * 100}%`}
            x2="100%"
            y2={`${pct * 100}%`}
            stroke={colors.accent.primary}
            strokeOpacity={0.12}
            strokeWidth={0.5}
          />
        ))}
        {/* Corner brackets */}
        {variant === 'face' && (
          <>
            {/* Top-left */}
            <Path d="M 30 10 L 10 10 L 10 30" stroke={colors.accent.primary} strokeWidth={2} fill="none" strokeOpacity={0.5} />
            {/* Top-right */}
            <Path d={`M ${SCREEN_W - 30} 10 L ${SCREEN_W - 10} 10 L ${SCREEN_W - 10} 30`} stroke={colors.accent.primary} strokeWidth={2} fill="none" strokeOpacity={0.5} />
            {/* Bottom-left */}
            <Path d={`M 30 ${CAMERA_HEIGHT - 10} L 10 ${CAMERA_HEIGHT - 10} L 10 ${CAMERA_HEIGHT - 30}`} stroke={colors.accent.primary} strokeWidth={2} fill="none" strokeOpacity={0.5} />
            {/* Bottom-right */}
            <Path d={`M ${SCREEN_W - 30} ${CAMERA_HEIGHT - 10} L ${SCREEN_W - 10} ${CAMERA_HEIGHT - 10} L ${SCREEN_W - 10} ${CAMERA_HEIGHT - 30}`} stroke={colors.accent.primary} strokeWidth={2} fill="none" strokeOpacity={0.5} />
          </>
        )}
      </Svg>

      {/* Scanning line */}
      <Animated.View style={lineStyle} />

      {/* Instruction overlay */}
      {variant === 'finger' && (
        <View style={styles.cameraInstructionContainer}>
          <View style={styles.fingerCircle}>
            <Ionicons name="finger-print" size={40} color={colors.accent.primary} />
          </View>
          <Text style={styles.cameraInstruction}>Place finger over camera lens</Text>
          <Text style={styles.cameraSubInstruction}>Cover completely with light pressure</Text>
        </View>
      )}
      {variant === 'face' && (
        <View style={styles.faceInstructionContainer}>
          <Text style={styles.cameraInstruction}>Position face in frame</Text>
          <Text style={styles.cameraSubInstruction}>Look directly at camera</Text>
        </View>
      )}
    </View>
  );
}

/** Voice waveform visualization */
function VoiceWaveform({
  isActive,
  stressLevel,
}: {
  isActive: boolean;
  stressLevel: number;
}) {
  const phase = useSharedValue(0);
  const amplitude = useSharedValue(0);

  useEffect(() => {
    if (isActive) {
      phase.value = withRepeat(
        withTiming(2 * Math.PI, { duration: 1600, easing: Easing.linear }),
        -1,
        false,
      );
      amplitude.value = withTiming(1, { duration: 800 });
    } else {
      amplitude.value = withTiming(0, { duration: 400 });
    }
  }, [isActive]);

  // Update amplitude based on stress
  useEffect(() => {
    if (isActive) {
      amplitude.value = withTiming(0.3 + (stressLevel / 100) * 0.7, { duration: 300 });
    }
  }, [stressLevel, isActive]);

  const waveWidth = SCREEN_W - spacing.lg * 2;
  const waveHeight = CAMERA_HEIGHT - 60;
  const centerY = waveHeight / 2;
  const numPoints = 100;

  const animatedProps = useAnimatedProps(() => {
    const points: string[] = [];
    const amp = amplitude.value;
    const ph = phase.value;
    for (let i = 0; i <= numPoints; i++) {
      const x = (i / numPoints) * waveWidth;
      const normalizedX = (i / numPoints) * Math.PI * 4;
      const y =
        centerY +
        Math.sin(normalizedX + ph) * centerY * 0.35 * amp +
        Math.sin(normalizedX * 2.3 + ph * 1.4) * centerY * 0.15 * amp +
        Math.sin(normalizedX * 3.7 + ph * 0.7) * centerY * 0.08 * amp;
      points.push(`${i === 0 ? 'M' : 'L'} ${x.toFixed(1)} ${y.toFixed(1)}`);
    }
    return { d: points.join(' ') };
  });

  // Secondary wave (echo effect)
  const animatedProps2 = useAnimatedProps(() => {
    const points: string[] = [];
    const amp = amplitude.value * 0.5;
    const ph = phase.value + 0.5;
    for (let i = 0; i <= numPoints; i++) {
      const x = (i / numPoints) * waveWidth;
      const normalizedX = (i / numPoints) * Math.PI * 4;
      const y =
        centerY +
        Math.sin(normalizedX + ph) * centerY * 0.35 * amp +
        Math.sin(normalizedX * 2.3 + ph * 1.4) * centerY * 0.15 * amp;
      points.push(`${i === 0 ? 'M' : 'L'} ${x.toFixed(1)} ${y.toFixed(1)}`);
    }
    return { d: points.join(' ') };
  });

  return (
    <View style={[styles.waveformContainer, { height: CAMERA_HEIGHT }]}>
      {/* Background gradient */}
      <LinearGradient
        colors={[colors.bg.secondary, colors.bg.primary]}
        style={StyleSheet.absoluteFill}
      />
      {/* Center line */}
      <View style={[styles.waveformCenterLine, { top: centerY + 30 }]} />

      <Svg
        width={waveWidth}
        height={waveHeight}
        style={{ marginTop: 30, marginHorizontal: spacing.lg }}
      >
        {/* Echo wave */}
        <AnimatedPath
          animatedProps={animatedProps2}
          stroke={colors.accent.secondary}
          strokeWidth={1.5}
          fill="none"
          opacity={0.3}
        />
        {/* Main wave */}
        <AnimatedPath
          animatedProps={animatedProps}
          stroke={colors.accent.primary}
          strokeWidth={2.5}
          fill="none"
          opacity={0.9}
        />
      </Svg>

      {/* Mic icon */}
      <View style={styles.micIconContainer}>
        <View style={[styles.micIcon, isActive && styles.micIconActive]}>
          <Ionicons
            name="mic"
            size={28}
            color={isActive ? colors.accent.primary : colors.text.tertiary}
          />
        </View>
        <Text style={styles.cameraInstruction}>
          {isActive ? 'Listening...' : 'Tap Start to begin'}
        </Text>
      </View>
    </View>
  );
}

/** Real-time metrics panel */
function MetricsPanel({
  readings,
  mode,
}: {
  readings: DetectionReadings;
  mode: DetectionMode;
}) {
  const showHR = mode === 'finger' || mode === 'multi';
  const showVoice = mode === 'voice' || mode === 'multi';
  const showFace = mode === 'face' || mode === 'multi';

  return (
    <View style={styles.metricsPanel}>
      {showHR && (
        <>
          <MetricItem
            icon="heart"
            label="HR"
            value={readings.heartRate > 0 ? `${readings.heartRate}` : '--'}
            unit="BPM"
            accentColor={colors.accent.tertiary}
          />
          <MetricDivider />
          <MetricItem
            icon="pulse"
            label="HRV"
            value={readings.hrv > 0 ? `${readings.hrv}` : '--'}
            unit="ms"
            accentColor={colors.accent.primary}
          />
          <MetricDivider />
        </>
      )}
      {showVoice && (
        <>
          <MetricBar
            icon="mic"
            label="Voice"
            value={readings.voiceStress}
            accentColor={colors.accent.secondary}
          />
          <MetricDivider />
        </>
      )}
      {showFace && (
        <>
          <MetricBar
            icon="scan"
            label="Face"
            value={readings.faceScore}
            accentColor={colors.accent.warning}
          />
          <MetricDivider />
        </>
      )}
      <SignalDot quality={readings.signalQuality} />
    </View>
  );
}

function MetricItem({
  icon,
  label,
  value,
  unit,
  accentColor,
}: {
  icon: string;
  label: string;
  value: string;
  unit: string;
  accentColor: string;
}) {
  return (
    <View style={styles.metricItem}>
      <View style={styles.metricHeader}>
        <Ionicons name={icon as any} size={12} color={accentColor} />
        <Text style={[styles.metricLabel, { color: accentColor }]}>{label}</Text>
      </View>
      <View style={styles.metricValueRow}>
        <Text style={styles.metricValue}>{value}</Text>
        <Text style={styles.metricUnit}>{unit}</Text>
      </View>
    </View>
  );
}

function MetricBar({
  icon,
  label,
  value,
  accentColor,
}: {
  icon: string;
  label: string;
  value: number;
  accentColor: string;
}) {
  return (
    <View style={styles.metricItem}>
      <View style={styles.metricHeader}>
        <Ionicons name={icon as any} size={12} color={accentColor} />
        <Text style={[styles.metricLabel, { color: accentColor }]}>{label}</Text>
      </View>
      <View style={styles.metricBarTrack}>
        <View
          style={[
            styles.metricBarFill,
            {
              width: `${Math.min(100, value)}%`,
              backgroundColor: accentColor,
            },
          ]}
        />
      </View>
    </View>
  );
}

function MetricDivider() {
  return <View style={styles.metricDivider} />;
}

function SignalDot({ quality }: { quality: number }) {
  const dotColor =
    quality > 0.7
      ? colors.accent.success
      : quality > 0.4
        ? colors.accent.warning
        : colors.accent.danger;
  const label = quality > 0.7 ? 'Good' : quality > 0.4 ? 'Fair' : 'Low';

  return (
    <View style={styles.metricItem}>
      <View style={styles.metricHeader}>
        <Ionicons name="radio" size={12} color={colors.text.secondary} />
        <Text style={[styles.metricLabel, { color: colors.text.secondary }]}>Signal</Text>
      </View>
      <View style={styles.signalRow}>
        <View style={[styles.signalDot, { backgroundColor: dotColor }]} />
        <Text style={[styles.metricUnit, { color: dotColor }]}>{label}</Text>
      </View>
    </View>
  );
}

/** Circular score gauge */
function ScoreGauge({
  score,
  verdict,
  confidence,
  isActive,
}: {
  score: number;
  verdict: Verdict;
  confidence: number;
  isActive: boolean;
}) {
  const progress = useSharedValue(0);
  const glowPulse = useSharedValue(0);
  const config = VERDICT_CONFIG[verdict];

  useEffect(() => {
    progress.value = withTiming(isActive ? score / 100 : 0, {
      duration: 800,
      easing: Easing.out(Easing.cubic),
    });
  }, [score, isActive]);

  useEffect(() => {
    if (isActive) {
      glowPulse.value = withRepeat(
        withSequence(
          withTiming(1, { duration: 1200, easing: Easing.inOut(Easing.ease) }),
          withTiming(0.3, { duration: 1200, easing: Easing.inOut(Easing.ease) }),
        ),
        -1,
        false,
      );
    } else {
      glowPulse.value = withTiming(0, { duration: 300 });
    }
  }, [isActive]);

  const animatedCircleProps = useAnimatedProps(() => ({
    strokeDashoffset: GAUGE_CIRCUMFERENCE * (1 - progress.value),
  }));

  const glowStyle = useAnimatedStyle(() => ({
    opacity: interpolate(glowPulse.value, [0, 1], [0.1, 0.35]),
    transform: [{ scale: interpolate(glowPulse.value, [0, 1], [0.95, 1.05]) }],
  }));

  return (
    <View style={styles.gaugeContainer}>
      {/* Glow backdrop */}
      <Animated.View
        style={[
          styles.gaugeGlow,
          {
            backgroundColor: config.glow,
            width: GAUGE_SIZE + 40,
            height: GAUGE_SIZE + 40,
            borderRadius: (GAUGE_SIZE + 40) / 2,
          },
          glowStyle,
        ]}
      />

      <Svg
        width={GAUGE_SIZE}
        height={GAUGE_SIZE}
        style={{ transform: [{ rotate: '-90deg' }] }}
      >
        {/* Track */}
        <Circle
          cx={GAUGE_SIZE / 2}
          cy={GAUGE_SIZE / 2}
          r={GAUGE_RADIUS}
          stroke={colors.bg.elevated}
          strokeWidth={GAUGE_STROKE}
          fill="none"
        />
        {/* Progress arc */}
        <AnimatedCircle
          cx={GAUGE_SIZE / 2}
          cy={GAUGE_SIZE / 2}
          r={GAUGE_RADIUS}
          stroke={config.colors[0]}
          strokeWidth={GAUGE_STROKE}
          fill="none"
          strokeDasharray={`${GAUGE_CIRCUMFERENCE}`}
          animatedProps={animatedCircleProps}
          strokeLinecap="round"
        />
      </Svg>

      {/* Center content */}
      <View style={styles.gaugeCenter}>
        <Text style={styles.gaugeScore}>{isActive ? score : '--'}</Text>
        <Text style={[styles.gaugeVerdict, { color: config.colors[0] }]}>
          {isActive ? config.label : 'READY'}
        </Text>
        {isActive && confidence > 0 && (
          <Text style={styles.gaugeConfidence}>{confidence}% confidence</Text>
        )}
      </View>
    </View>
  );
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

export default function DetectionScreen({ navigation, route }: Props) {
  const initialMode = route.params?.mode ?? 'finger';
  const [mode, setMode] = useState<DetectionMode>(initialMode);
  const [isRecording, setIsRecording] = useState(false);
  const [isPremium] = useState(false); // Will come from store later
  const [cameraPermission, requestCameraPermission] = useCameraPermissions();

  const { readings, processCameraFrame, processFaceData, markQuestion } = useDetectionEngine(isRecording, mode);

  // Request camera permission on mount
  useEffect(() => {
    if (!cameraPermission?.granted) {
      requestCameraPermission();
    }
  }, []);

  const handleModeChange = useCallback(
    (newMode: DetectionMode) => {
      if (newMode === 'multi' && !isPremium) return;
      if (isRecording) setIsRecording(false);
      setMode(newMode);
    },
    [isRecording, isPremium],
  );

  const handleToggleRecording = useCallback(() => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    setIsRecording((prev) => {
      if (!prev) {
        playSound('analyzeStart');
      } else {
        playSound('analyzeComplete');
      }
      return !prev;
    });
  }, []);

  const handleMarkQuestion = useCallback(() => {
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    playSound('scanPulse');
    markQuestion();
  }, [markQuestion]);

  const handlePartyMode = useCallback(() => {
    navigation.navigate('PartyMode');
  }, [navigation]);

  // Camera configuration
  const showCamera = mode === 'finger' || mode === 'face' || mode === 'multi';
  const cameraFacing = mode === 'finger' ? 'back' : 'front';
  const enableTorch = mode === 'finger' && isRecording;

  // Recording pulse animation
  const recordPulse = useSharedValue(1);
  useEffect(() => {
    if (isRecording) {
      recordPulse.value = withRepeat(
        withSequence(
          withTiming(1.15, { duration: 600, easing: Easing.inOut(Easing.ease) }),
          withTiming(1, { duration: 600, easing: Easing.inOut(Easing.ease) }),
        ),
        -1,
        false,
      );
    } else {
      recordPulse.value = withTiming(1, { duration: 200 });
    }
  }, [isRecording]);

  const recordBtnStyle = useAnimatedStyle(() => ({
    transform: [{ scale: recordPulse.value }],
  }));

  return (
    <View style={styles.container}>
      {/* Back button */}
      <TouchableOpacity
        style={{ position: 'absolute', top: 50, left: 16, zIndex: 100, padding: 8 }}
        onPress={() => { if (isRecording) setIsRecording(false); navigation.goBack(); }}
        sound="swipe"
      >
        <Ionicons name="arrow-back" size={24} color={colors.text.primary} />
      </TouchableOpacity>

      {/* Mode selector */}
      <ModeSelector
        current={mode}
        onSelect={handleModeChange}
        isPremium={isPremium}
      />

      {/* Camera / Waveform area */}
      <View style={styles.cameraArea}>
        {mode === 'voice' ? (
          <VoiceWaveform
            isActive={isRecording}
            stressLevel={readings.voiceStress}
          />
        ) : mode === 'multi' ? (
          <View style={styles.multiContainer}>
            {/* Face camera takes 60% */}
            <View style={styles.multiFace}>
              {cameraPermission?.granted ? (
                <CameraView
                  style={StyleSheet.absoluteFill}
                  facing="front"
                />
              ) : (
                <View style={[StyleSheet.absoluteFill, styles.cameraPlaceholder]}>
                  <Ionicons name="camera-outline" size={32} color={colors.text.tertiary} />
                </View>
              )}
              <ScanOverlay variant="face" />
              <View style={styles.multiLabel}>
                <Text style={styles.multiLabelText}>FACE</Text>
              </View>
            </View>
            {/* Side panel: mini pulse + voice level */}
            <View style={styles.multiSide}>
              <View style={styles.miniPanel}>
                <Text style={styles.miniPanelLabel}>PULSE</Text>
                <MiniPulseGraph heartRate={readings.heartRate} isActive={isRecording} />
              </View>
              <View style={styles.miniPanel}>
                <Text style={styles.miniPanelLabel}>VOICE</Text>
                <MiniVoiceLevel level={readings.voiceStress} isActive={isRecording} />
              </View>
            </View>
          </View>
        ) : (
          <View style={{ flex: 1 }}>
            {cameraPermission?.granted ? (
              <CameraView
                style={StyleSheet.absoluteFill}
                facing={cameraFacing}
                enableTorch={enableTorch}
              />
            ) : (
              <View style={[StyleSheet.absoluteFill, styles.cameraPlaceholder]}>
                <Ionicons name="camera-outline" size={40} color={colors.text.tertiary} />
                <Text style={styles.cameraPermText}>Camera access required</Text>
              </View>
            )}
            <ScanOverlay variant={mode === 'finger' ? 'finger' : 'face'} />
          </View>
        )}

        {/* Top-right recording indicator */}
        {isRecording && (
          <View style={styles.recordingBadge}>
            <View style={styles.recordingDot} />
            <Text style={styles.recordingText}>REC</Text>
          </View>
        )}
      </View>

      {/* Metrics panel */}
      <MetricsPanel readings={readings} mode={mode} />

      {/* Score gauge */}
      <ScoreGauge
        score={readings.overallScore}
        verdict={readings.verdict}
        confidence={readings.confidence}
        isActive={isRecording}
      />

      {/* Control buttons */}
      <View style={styles.controls}>
        {/* Ask Question button */}
        <TouchableOpacity
          style={styles.secondaryBtn}
          onPress={handleMarkQuestion}
          disabled={!isRecording}
        >
          <Ionicons
            name="help-circle"
            size={22}
            color={isRecording ? colors.accent.secondary : colors.text.tertiary}
          />
          <Text
            style={[
              styles.secondaryBtnText,
              !isRecording && { color: colors.text.tertiary },
            ]}
          >
            Question
          </Text>
        </TouchableOpacity>

        {/* Start / Stop button */}
        <Animated.View style={recordBtnStyle}>
          <TouchableOpacity
            style={[styles.mainBtn, isRecording && styles.mainBtnRecording]}
            onPress={handleToggleRecording}
            activeOpacity={0.8}
          >
            <LinearGradient
              colors={
                isRecording
                  ? [colors.accent.danger, '#CC0033']
                  : [colors.accent.primary, colors.accent.secondary]
              }
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
              style={styles.mainBtnGradient}
            >
              <Ionicons
                name={isRecording ? 'stop' : 'play'}
                size={28}
                color="#FFFFFF"
              />
            </LinearGradient>
          </TouchableOpacity>
        </Animated.View>

        {/* Party mode shortcut */}
        <TouchableOpacity style={styles.secondaryBtn} onPress={handlePartyMode}>
          <Ionicons name="people" size={22} color={colors.accent.warning} />
          <Text style={styles.secondaryBtnText}>Party</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

// ---------------------------------------------------------------------------
// Mini widgets for Multi mode
// ---------------------------------------------------------------------------

function MiniPulseGraph({
  heartRate,
  isActive,
}: {
  heartRate: number;
  isActive: boolean;
}) {
  const [points, setPoints] = useState<number[]>([]);

  useEffect(() => {
    if (!isActive) {
      setPoints([]);
      return;
    }
    const interval = setInterval(() => {
      setPoints((prev) => {
        const next = [...prev, heartRate > 0 ? heartRate : 0]; // No fake data - show 0 when no sensor
        if (next.length > 20) next.shift();
        return next;
      });
    }, 400);
    return () => clearInterval(interval);
  }, [isActive, heartRate]);

  const width = (SCREEN_W * 0.4) - spacing.md * 2;
  const height = 40;

  const pathD = useMemo(() => {
    if (points.length < 2) return '';
    const minV = Math.min(...points) - 5;
    const maxV = Math.max(...points) + 5;
    const range = maxV - minV || 1;
    return points
      .map((p, i) => {
        const x = (i / (points.length - 1)) * width;
        const y = height - ((p - minV) / range) * height;
        return `${i === 0 ? 'M' : 'L'} ${x.toFixed(1)} ${y.toFixed(1)}`;
      })
      .join(' ');
  }, [points, width, height]);

  return (
    <View style={{ width, height }}>
      <Svg width={width} height={height}>
        {pathD.length > 0 && (
          <Path d={pathD} stroke={colors.accent.primary} strokeWidth={1.5} fill="none" />
        )}
      </Svg>
      {heartRate > 0 && (
        <Text style={styles.miniValue}>{heartRate} BPM</Text>
      )}
    </View>
  );
}

function MiniVoiceLevel({
  level,
  isActive,
}: {
  level: number;
  isActive: boolean;
}) {
  const barCount = 8;
  const width = (SCREEN_W * 0.4) - spacing.md * 2;
  const barWidth = (width - (barCount - 1) * 3) / barCount;
  const height = 40;

  return (
    <View style={{ width, height, flexDirection: 'row', alignItems: 'flex-end', gap: 3 }}>
      {Array.from({ length: barCount }).map((_, i) => {
        const threshold = (i / barCount) * 100;
        const active = isActive && level > threshold;
        const barHeight = ((i + 1) / barCount) * height;
        return (
          <View
            key={i}
            style={{
              width: barWidth,
              height: barHeight,
              borderRadius: 2,
              backgroundColor: active
                ? i < barCount * 0.5
                  ? colors.accent.success
                  : i < barCount * 0.75
                    ? colors.accent.warning
                    : colors.accent.danger
                : colors.bg.elevated,
            }}
          />
        );
      })}
    </View>
  );
}

// ---------------------------------------------------------------------------
// Styles
// ---------------------------------------------------------------------------

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.bg.primary,
  },

  // Mode tabs
  modeTabs: {
    flexDirection: 'row',
    paddingHorizontal: spacing.md,
    paddingTop: Platform.OS === 'ios' ? 8 : spacing.sm,
    paddingBottom: spacing.sm,
    gap: spacing.sm,
  },
  modeTab: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: spacing.sm,
    borderRadius: radii.md,
    backgroundColor: colors.bg.secondary,
    gap: 4,
  },
  modeTabActive: {
    backgroundColor: 'rgba(0, 229, 255, 0.12)',
    borderWidth: 1,
    borderColor: 'rgba(0, 229, 255, 0.3)',
  },
  modeTabLabel: {
    ...typography.caption,
    color: colors.text.secondary,
  },
  modeTabLabelActive: {
    color: colors.accent.primary,
  },

  // Camera area
  cameraArea: {
    height: CAMERA_HEIGHT,
    marginHorizontal: spacing.md,
    borderRadius: radii.lg,
    overflow: 'hidden',
    backgroundColor: colors.bg.card,
  },
  cameraPlaceholder: {
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.bg.secondary,
  },
  cameraPermText: {
    ...typography.caption,
    color: colors.text.tertiary,
    marginTop: spacing.sm,
  },
  cameraInstructionContainer: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'center',
    alignItems: 'center',
  },
  faceInstructionContainer: {
    position: 'absolute',
    bottom: spacing.lg,
    left: 0,
    right: 0,
    alignItems: 'center',
  },
  fingerCircle: {
    width: 80,
    height: 80,
    borderRadius: 40,
    borderWidth: 2,
    borderColor: 'rgba(0, 229, 255, 0.4)',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: spacing.md,
    backgroundColor: 'rgba(0, 229, 255, 0.05)',
  },
  cameraInstruction: {
    ...typography.bodyBold,
    color: colors.text.primary,
    textAlign: 'center',
    textShadowColor: 'rgba(0, 0, 0, 0.8)',
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 4,
  },
  cameraSubInstruction: {
    ...typography.caption,
    color: colors.text.secondary,
    textAlign: 'center',
    marginTop: 4,
    textShadowColor: 'rgba(0, 0, 0, 0.8)',
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 4,
  },

  // Recording badge
  recordingBadge: {
    position: 'absolute',
    top: spacing.sm,
    right: spacing.sm,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
    paddingHorizontal: spacing.sm,
    paddingVertical: 4,
    borderRadius: radii.full,
    gap: 4,
  },
  recordingDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: colors.accent.danger,
  },
  recordingText: {
    ...typography.small,
    color: colors.accent.danger,
    fontWeight: '700',
  },

  // Waveform
  waveformContainer: {
    overflow: 'hidden',
  },
  waveformCenterLine: {
    position: 'absolute',
    left: spacing.lg,
    right: spacing.lg,
    height: 1,
    backgroundColor: 'rgba(0, 229, 255, 0.1)',
  },
  micIconContainer: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'center',
    alignItems: 'center',
  },
  micIcon: {
    width: 56,
    height: 56,
    borderRadius: 28,
    borderWidth: 2,
    borderColor: colors.bg.elevated,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: spacing.sm,
    backgroundColor: colors.bg.card,
  },
  micIconActive: {
    borderColor: 'rgba(0, 229, 255, 0.4)',
    backgroundColor: 'rgba(0, 229, 255, 0.08)',
  },

  // Multi mode
  multiContainer: {
    flex: 1,
    flexDirection: 'row',
  },
  multiFace: {
    flex: 0.6,
    position: 'relative',
  },
  multiSide: {
    flex: 0.4,
    backgroundColor: colors.bg.secondary,
    padding: spacing.sm,
    justifyContent: 'space-around',
  },
  multiLabel: {
    position: 'absolute',
    top: spacing.xs,
    left: spacing.xs,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    paddingHorizontal: spacing.xs,
    paddingVertical: 2,
    borderRadius: radii.sm,
  },
  multiLabelText: {
    ...typography.small,
    color: colors.accent.primary,
    fontWeight: '700',
    letterSpacing: 1,
  },
  miniPanel: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: spacing.xs,
  },
  miniPanelLabel: {
    ...typography.small,
    color: colors.text.tertiary,
    letterSpacing: 1.5,
    marginBottom: 4,
    fontWeight: '600',
  },
  miniValue: {
    ...typography.small,
    color: colors.accent.primary,
    position: 'absolute',
    right: 0,
    bottom: 0,
  },

  // Metrics panel
  metricsPanel: {
    flexDirection: 'row',
    alignItems: 'center',
    marginHorizontal: spacing.md,
    marginTop: spacing.sm,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    backgroundColor: colors.bg.card,
    borderRadius: radii.md,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.04)',
  },
  metricItem: {
    flex: 1,
    alignItems: 'center',
  },
  metricHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 3,
    marginBottom: 4,
  },
  metricLabel: {
    ...typography.small,
    fontWeight: '600',
    letterSpacing: 0.5,
  },
  metricValueRow: {
    flexDirection: 'row',
    alignItems: 'baseline',
    gap: 2,
  },
  metricValue: {
    ...typography.h3,
    color: colors.text.primary,
    fontVariant: ['tabular-nums'],
  },
  metricUnit: {
    ...typography.small,
    color: colors.text.tertiary,
  },
  metricBarTrack: {
    width: '80%',
    height: 4,
    backgroundColor: colors.bg.elevated,
    borderRadius: 2,
    overflow: 'hidden',
  },
  metricBarFill: {
    height: '100%',
    borderRadius: 2,
  },
  metricDivider: {
    width: 1,
    height: 28,
    backgroundColor: 'rgba(255, 255, 255, 0.06)',
  },
  signalRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  signalDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },

  // Score gauge
  gaugeContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: spacing.md,
    height: GAUGE_SIZE + 20,
  },
  gaugeGlow: {
    position: 'absolute',
  },
  gaugeCenter: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'center',
    alignItems: 'center',
  },
  gaugeScore: {
    fontSize: 40,
    fontWeight: '800',
    color: colors.text.primary,
    fontVariant: ['tabular-nums'],
    letterSpacing: -1,
  },
  gaugeVerdict: {
    ...typography.caption,
    fontWeight: '700',
    letterSpacing: 2,
    marginTop: 2,
  },
  gaugeConfidence: {
    ...typography.small,
    color: colors.text.tertiary,
    marginTop: 2,
  },

  // Controls
  controls: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.md,
    paddingBottom: Platform.OS === 'ios' ? spacing.xl : spacing.lg,
  },
  mainBtn: {
    width: 68,
    height: 68,
    borderRadius: 34,
    overflow: 'hidden',
    shadowColor: colors.accent.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4,
    shadowRadius: 12,
    elevation: 8,
  },
  mainBtnRecording: {
    shadowColor: colors.accent.danger,
  },
  mainBtnGradient: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  secondaryBtn: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.md,
    gap: 4,
  },
  secondaryBtnText: {
    ...typography.small,
    color: colors.text.secondary,
    fontWeight: '600',
  },
});
