import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  View, Text, StyleSheet, Dimensions, Platform,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { SoundTouchable as TouchableOpacity } from '../components/SoundTouchable';
import { CameraView, useCameraPermissions } from 'expo-camera';
import Animated, {
  useSharedValue, useAnimatedStyle, useAnimatedProps, withTiming,
  withRepeat, withSequence, Easing, interpolate, runOnJS,
} from 'react-native-reanimated';
import Svg, { Path, Circle, Line } from 'react-native-svg';
import * as Haptics from 'expo-haptics';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { colors, spacing, typography, radii } from '../theme';
import { DetectionMode, Verdict, DetectionResult } from '../utils/types';
import { useDetectionEngine, DetectionReadings } from '../hooks/useDetectionEngine';
import { playSound, playVerdictReveal } from '../sounds/SoundEngine';
import { DeceptionAnalyzer } from '../engines/DeceptionAnalyzer';
import { saveSession, generateId } from '../store';

const { width: SCREEN_W, height: SCREEN_H } = Dimensions.get('window');
const CAMERA_HEIGHT = SCREEN_H * 0.36;
const GAUGE_SIZE = 160;
const GAUGE_STROKE = 10;
const GAUGE_RADIUS = (GAUGE_SIZE - GAUGE_STROKE) / 2;
const GAUGE_CIRCUMFERENCE = 2 * Math.PI * GAUGE_RADIUS;

const AnimatedCircle = Animated.createAnimatedComponent(Circle);
const AnimatedPath = Animated.createAnimatedComponent(Path);

const MODE_TABS: { key: DetectionMode; label: string; icon: string }[] = [
  { key: 'finger', label: 'Finger', icon: 'finger-print' },
  { key: 'face', label: 'Face', icon: 'scan' },
  { key: 'voice', label: 'Voice', icon: 'mic' },
  { key: 'multi', label: 'Multi', icon: 'layers' },
];

const VERDICT_CONFIG: Record<Verdict, { label: string; colors: readonly [string, string]; glow: string }> = {
  truthful: { label: 'TRUTHFUL', colors: colors.gradient.truthful, glow: colors.accent.success },
  deceptive: { label: 'DECEPTIVE', colors: colors.gradient.deceptive, glow: colors.accent.danger },
  uncertain: { label: 'UNCERTAIN', colors: colors.gradient.uncertain, glow: colors.accent.warning },
  scanning: { label: 'ANALYZING...', colors: colors.gradient.scanning, glow: colors.accent.primary },
};

function ScanOverlay({ variant }: { variant: 'finger' | 'face' }) {
  const scanLine = useSharedValue(0);
  useEffect(() => {
    scanLine.value = withRepeat(withTiming(1, { duration: 2400, easing: Easing.inOut(Easing.ease) }), -1, true);
  }, []);

  const lineStyle = useAnimatedStyle(() => ({
    position: 'absolute' as const, left: 0, right: 0, height: 2,
    top: interpolate(scanLine.value, [0, 1], [0, CAMERA_HEIGHT]),
    backgroundColor: colors.accent.primary, opacity: 0.6,
    shadowColor: colors.accent.primary, shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.8, shadowRadius: 8,
  }));

  return (
    <View style={StyleSheet.absoluteFill} pointerEvents="none">
      <Svg width="100%" height="100%" style={StyleSheet.absoluteFill}>
        {[0.25, 0.5, 0.75].map((pct) => (
          <Line key={`v-${pct}`} x1={`${pct * 100}%`} y1="0" x2={`${pct * 100}%`} y2="100%"
            stroke={colors.accent.primary} strokeOpacity={0.12} strokeWidth={0.5} />
        ))}
        {[0.25, 0.5, 0.75].map((pct) => (
          <Line key={`h-${pct}`} x1="0" y1={`${pct * 100}%`} x2="100%" y2={`${pct * 100}%`}
            stroke={colors.accent.primary} strokeOpacity={0.12} strokeWidth={0.5} />
        ))}
      </Svg>
      <Animated.View style={lineStyle} />
      {variant === 'finger' && (
        <View style={styles.cameraInstructionContainer}>
          <View style={styles.fingerCircle}><Ionicons name="finger-print" size={40} color={colors.accent.primary} /></View>
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

function VoiceWaveform({ isActive, stressLevel }: { isActive: boolean; stressLevel: number }) {
  const phase = useSharedValue(0);
  const amplitude = useSharedValue(0);

  useEffect(() => {
    if (isActive) {
      phase.value = withRepeat(withTiming(2 * Math.PI, { duration: 1600, easing: Easing.linear }), -1, false);
      amplitude.value = withTiming(1, { duration: 800 });
    } else {
      amplitude.value = withTiming(0, { duration: 400 });
    }
  }, [isActive]);

  useEffect(() => {
    if (isActive) {
      amplitude.value = withTiming(0.3 + (stressLevel / 100) * 0.7, { duration: 300 });
    }
  }, [stressLevel, isActive]);

  const waveWidth = SCREEN_W - spacing.lg * 2;
  const waveHeight = CAMERA_HEIGHT - 60;
  const centerY = waveHeight / 2;

  const animatedProps = useAnimatedProps(() => {
    const points: string[] = [];
    const amp = amplitude.value;
    const ph = phase.value;
    for (let i = 0; i <= 100; i++) {
      const x = (i / 100) * waveWidth;
      const nx = (i / 100) * Math.PI * 4;
      const y = centerY + Math.sin(nx + ph) * centerY * 0.35 * amp +
        Math.sin(nx * 2.3 + ph * 1.4) * centerY * 0.15 * amp +
        Math.sin(nx * 3.7 + ph * 0.7) * centerY * 0.08 * amp;
      points.push(`${i === 0 ? 'M' : 'L'} ${x.toFixed(1)} ${y.toFixed(1)}`);
    }
    return { d: points.join(' ') };
  });

  return (
    <View style={[styles.waveformContainer, { height: CAMERA_HEIGHT }]}>
      <LinearGradient colors={[colors.bg.secondary, colors.bg.primary]} style={StyleSheet.absoluteFill} />
      <Svg width={waveWidth} height={waveHeight} style={{ marginTop: 30, marginHorizontal: spacing.lg }}>
        <AnimatedPath animatedProps={animatedProps} stroke={colors.accent.primary} strokeWidth={2.5} fill="none" opacity={0.9} />
      </Svg>
      <View style={styles.micIconContainer}>
        <View style={[styles.micIcon, isActive && styles.micIconActive]}>
          <Ionicons name="mic" size={28} color={isActive ? colors.accent.primary : colors.text.tertiary} />
        </View>
        <Text style={styles.cameraInstruction}>{isActive ? 'Listening...' : 'Tap Start to begin'}</Text>
      </View>
    </View>
  );
}

function MetricsPanel({ readings, mode }: { readings: DetectionReadings; mode: DetectionMode }) {
  const showHR = mode === 'finger' || mode === 'multi';
  const showVoice = mode === 'voice' || mode === 'multi';
  const showFace = mode === 'face' || mode === 'multi';

  return (
    <View style={styles.metricsPanel}>
      {showHR && (
        <>
          <View style={styles.metricItem}>
            <View style={styles.metricHeader}><Ionicons name="heart" size={12} color={colors.accent.tertiary} />
              <Text style={[styles.metricLabel, { color: colors.accent.tertiary }]}>HR</Text></View>
            <Text style={styles.metricValue}>{readings.heartRate > 0 ? `${readings.heartRate}` : '--'}</Text>
          </View>
          <View style={styles.metricDivider} />
          <View style={styles.metricItem}>
            <View style={styles.metricHeader}><Ionicons name="pulse" size={12} color={colors.accent.primary} />
              <Text style={[styles.metricLabel, { color: colors.accent.primary }]}>HRV</Text></View>
            <Text style={styles.metricValue}>{readings.hrv > 0 ? `${readings.hrv}` : '--'}</Text>
          </View>
          <View style={styles.metricDivider} />
        </>
      )}
      {showVoice && (
        <>
          <View style={styles.metricItem}>
            <View style={styles.metricHeader}><Ionicons name="mic" size={12} color={colors.accent.secondary} />
              <Text style={[styles.metricLabel, { color: colors.accent.secondary }]}>Voice</Text></View>
            <View style={styles.metricBarTrack}>
              <View style={[styles.metricBarFill, { width: `${Math.min(100, readings.voiceStress)}%`, backgroundColor: colors.accent.secondary }]} />
            </View>
          </View>
          <View style={styles.metricDivider} />
        </>
      )}
      {showFace && (
        <>
          <View style={styles.metricItem}>
            <View style={styles.metricHeader}><Ionicons name="scan" size={12} color={colors.accent.warning} />
              <Text style={[styles.metricLabel, { color: colors.accent.warning }]}>Face</Text></View>
            <View style={styles.metricBarTrack}>
              <View style={[styles.metricBarFill, { width: `${Math.min(100, readings.faceScore)}%`, backgroundColor: colors.accent.warning }]} />
            </View>
          </View>
          <View style={styles.metricDivider} />
        </>
      )}
      <View style={styles.metricItem}>
        <View style={styles.metricHeader}><Ionicons name="radio" size={12} color={colors.text.secondary} />
          <Text style={[styles.metricLabel, { color: colors.text.secondary }]}>Signal</Text></View>
        <View style={styles.signalRow}>
          <View style={[styles.signalDot, {
            backgroundColor: readings.signalQuality > 0.7 ? colors.accent.success : readings.signalQuality > 0.4 ? colors.accent.warning : colors.accent.danger
          }]} />
        </View>
      </View>
    </View>
  );
}

export default function DetectionScreen({ navigation, route }: { navigation: any; route: any }) {
  const insets = useSafeAreaInsets();
  const initialMode = (route.params?.mode as DetectionMode) ?? 'finger';
  const [mode, setMode] = useState<DetectionMode>(initialMode);
  const [isActive, setIsActive] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const [permission, requestPermission] = useCameraPermissions();

  const { readings, processCameraFrame, processFaceData, markQuestion } = useDetectionEngine(isActive, mode);
  const analyzerRef = useRef<DeceptionAnalyzer | null>(null);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (!permission?.granted) {
      requestPermission();
    }
  }, []);

  const handleStart = useCallback(() => {
    playSound('scanStart');
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    setIsActive(true);
    setElapsed(0);
    analyzerRef.current = new DeceptionAnalyzer(mode);
    timerRef.current = setInterval(() => {
      setElapsed(prev => prev + 1);
    }, 1000);
  }, [mode]);

  const handleStop = useCallback(() => {
    playSound('analyzeComplete');
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    setIsActive(false);
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }

    const result: DetectionResult = {
      id: generateId(),
      timestamp: Date.now(),
      mode,
      verdict: readings.verdict === 'scanning' ? 'uncertain' : readings.verdict,
      confidence: readings.confidence,
      overallScore: readings.overallScore,
      breakdown: {
        physiological: readings.heartRate > 0 ? readings.overallScore : 0,
        vocal: readings.voiceStress,
        facial: readings.faceScore,
      },
      duration: elapsed,
    };

    playVerdictReveal(result.verdict === 'scanning' ? 'uncertain' : result.verdict);

    saveSession({
      id: generateId(),
      startTime: Date.now() - elapsed * 1000,
      endTime: Date.now(),
      mode,
      results: [result],
      isPartyMode: false,
    });

    navigation.navigate('Result', { result });
  }, [readings, elapsed, mode, navigation]);

  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const needsCamera = mode === 'finger' || mode === 'face' || mode === 'multi';
  const cameraFacing = mode === 'finger' ? 'back' : 'front';
  const config = VERDICT_CONFIG[readings.verdict];

  return (
    <View style={[styles.screen, { paddingTop: insets.top }]}>
      {/* Top Bar */}
      <View style={styles.topBar}>
        <TouchableOpacity onPress={() => { playSound('swipe'); navigation.goBack(); }} style={styles.backButton} sound="tap">
          <Ionicons name="arrow-back" size={24} color={colors.text.primary} />
        </TouchableOpacity>
        <Text style={styles.elapsedText}>{Math.floor(elapsed / 60)}:{String(elapsed % 60).padStart(2, '0')}</Text>
        <View style={{ width: 40 }} />
      </View>

      {/* Mode Tabs */}
      <View style={styles.modeTabs}>
        {MODE_TABS.map((tab) => {
          const active = mode === tab.key;
          return (
            <TouchableOpacity key={tab.key} style={[styles.modeTab, active && styles.modeTabActive]}
              onPress={() => { if (!isActive) setMode(tab.key); }} activeOpacity={isActive ? 1 : 0.7} sound="toggle">
              <Ionicons name={tab.icon as any} size={18}
                color={active ? colors.accent.primary : colors.text.secondary} />
              <Text style={[styles.modeTabLabel, active && styles.modeTabLabelActive]}>{tab.label}</Text>
            </TouchableOpacity>
          );
        })}
      </View>

      {/* Camera / Waveform Area */}
      {mode === 'voice' ? (
        <VoiceWaveform isActive={isActive} stressLevel={readings.voiceStress} />
      ) : needsCamera && permission?.granted ? (
        <View style={styles.cameraContainer}>
          <CameraView style={styles.camera} facing={cameraFacing}
            enableTorch={mode === 'finger' && isActive} />
          <ScanOverlay variant={mode === 'finger' ? 'finger' : 'face'} />
        </View>
      ) : (
        <View style={[styles.cameraContainer, { backgroundColor: colors.bg.secondary, alignItems: 'center', justifyContent: 'center' }]}>
          <Ionicons name="camera-outline" size={48} color={colors.text.tertiary} />
          <Text style={styles.cameraInstruction}>Camera permission required</Text>
          <TouchableOpacity onPress={requestPermission} sound="tap">
            <Text style={[styles.cameraInstruction, { color: colors.accent.primary }]}>Grant Permission</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Metrics */}
      <MetricsPanel readings={readings} mode={mode} />

      {/* Score Display */}
      <View style={styles.scoreSection}>
        <View style={styles.gaugeContainer}>
          <Svg width={GAUGE_SIZE} height={GAUGE_SIZE}>
            <Circle cx={GAUGE_SIZE / 2} cy={GAUGE_SIZE / 2} r={GAUGE_RADIUS}
              stroke={colors.bg.tertiary} strokeWidth={GAUGE_STROKE} fill="none" />
            <Circle cx={GAUGE_SIZE / 2} cy={GAUGE_SIZE / 2} r={GAUGE_RADIUS}
              stroke={config.glow} strokeWidth={GAUGE_STROKE} fill="none"
              strokeDasharray={GAUGE_CIRCUMFERENCE}
              strokeDashoffset={GAUGE_CIRCUMFERENCE * (1 - (isActive ? readings.overallScore / 100 : 0))}
              strokeLinecap="round" rotation="-90" origin={`${GAUGE_SIZE / 2}, ${GAUGE_SIZE / 2}`} />
          </Svg>
          <View style={styles.gaugeCenter}>
            <Text style={[styles.gaugeScore, { color: config.glow }]}>
              {isActive ? readings.overallScore : '--'}
            </Text>
            <Text style={[styles.gaugeLabel, { color: config.glow }]}>
              {isActive ? config.label : 'READY'}
            </Text>
          </View>
        </View>
      </View>

      {/* Start/Stop Button */}
      <View style={[styles.buttonContainer, { paddingBottom: insets.bottom + spacing.md }]}>
        <TouchableOpacity onPress={isActive ? handleStop : handleStart}
          style={styles.actionButton} sound={isActive ? 'analyzeComplete' : 'scanStart'} haptic="heavy">
          <LinearGradient colors={isActive ? [...colors.gradient.deceptive] : [...colors.gradient.scanning]}
            start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }} style={styles.actionButtonGradient}>
            <Ionicons name={isActive ? 'stop' : 'play'} size={24} color="#FFFFFF" />
            <Text style={styles.actionButtonText}>{isActive ? 'Stop & Analyze' : 'Start Detection'}</Text>
          </LinearGradient>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg.primary },
  topBar: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: spacing.lg, paddingVertical: spacing.sm },
  backButton: { width: 40, height: 40, borderRadius: 20, backgroundColor: colors.bg.card, alignItems: 'center', justifyContent: 'center' },
  elapsedText: { ...typography.mono, color: colors.text.secondary, fontSize: 16 },
  modeTabs: { flexDirection: 'row', paddingHorizontal: spacing.lg, marginBottom: spacing.sm, gap: spacing.xs },
  modeTab: { flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 4, paddingVertical: spacing.sm, borderRadius: radii.sm, backgroundColor: colors.bg.card },
  modeTabActive: { backgroundColor: colors.accent.primary + '18' },
  modeTabLabel: { ...typography.small, color: colors.text.secondary },
  modeTabLabelActive: { color: colors.accent.primary },
  cameraContainer: { height: CAMERA_HEIGHT, overflow: 'hidden' },
  camera: { flex: 1 },
  waveformContainer: { overflow: 'hidden', position: 'relative' },
  cameraInstructionContainer: { ...StyleSheet.absoluteFillObject, alignItems: 'center', justifyContent: 'center', gap: spacing.sm },
  faceInstructionContainer: { position: 'absolute', bottom: spacing.lg, left: 0, right: 0, alignItems: 'center', gap: 4 },
  fingerCircle: { width: 80, height: 80, borderRadius: 40, borderWidth: 2, borderColor: colors.accent.primary, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.accent.primary + '10' },
  cameraInstruction: { ...typography.bodyBold, color: colors.text.primary, textAlign: 'center' },
  cameraSubInstruction: { ...typography.small, color: colors.text.secondary, textAlign: 'center' },
  micIconContainer: { ...StyleSheet.absoluteFillObject, alignItems: 'center', justifyContent: 'center', gap: spacing.sm },
  micIcon: { width: 56, height: 56, borderRadius: 28, backgroundColor: colors.bg.card, alignItems: 'center', justifyContent: 'center' },
  micIconActive: { backgroundColor: colors.accent.primary + '20' },
  metricsPanel: { flexDirection: 'row', paddingHorizontal: spacing.lg, paddingVertical: spacing.sm, gap: spacing.xs, alignItems: 'center' },
  metricItem: { flex: 1, gap: 4 },
  metricHeader: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  metricLabel: { ...typography.small, fontWeight: '600' },
  metricValue: { ...typography.bodyBold, color: colors.text.primary, fontSize: 18 },
  metricBarTrack: { height: 4, backgroundColor: colors.bg.tertiary, borderRadius: 2, overflow: 'hidden' },
  metricBarFill: { height: '100%', borderRadius: 2 },
  metricDivider: { width: 1, height: 30, backgroundColor: colors.bg.elevated },
  signalRow: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  signalDot: { width: 8, height: 8, borderRadius: 4 },
  scoreSection: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  gaugeContainer: { width: GAUGE_SIZE, height: GAUGE_SIZE, alignItems: 'center', justifyContent: 'center' },
  gaugeCenter: { ...StyleSheet.absoluteFillObject, alignItems: 'center', justifyContent: 'center' },
  gaugeScore: { fontSize: 44, fontWeight: '800', letterSpacing: -2 },
  gaugeLabel: { fontSize: 11, fontWeight: '700', letterSpacing: 2, marginTop: 2 },
  buttonContainer: { paddingHorizontal: spacing.lg },
  actionButton: { borderRadius: radii.lg, overflow: 'hidden' },
  actionButtonGradient: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, paddingVertical: spacing.md },
  actionButtonText: { ...typography.bodyBold, color: '#FFFFFF', fontSize: 17 },
});
