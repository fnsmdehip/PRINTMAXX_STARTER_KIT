import React from 'react';
import { View, StyleSheet } from 'react-native';
import Svg, { Path, Defs, LinearGradient as SvgGradient, Stop } from 'react-native-svg';
import { colors } from '../theme';

interface PulseWaveformProps {
  data: number[];
  width: number;
  height: number;
  color?: string;
  showFill?: boolean;
}

export function PulseWaveform({
  data,
  width,
  height,
  color = colors.pulse.line,
  showFill = true,
}: PulseWaveformProps) {
  if (data.length < 2) {
    return <View style={[styles.container, { width, height }]} />;
  }

  const padding = 4;
  const drawWidth = width - padding * 2;
  const drawHeight = height - padding * 2;

  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;

  const points = data.map((value, index) => ({
    x: padding + (index / (data.length - 1)) * drawWidth,
    y: padding + drawHeight - ((value - min) / range) * drawHeight,
  }));

  let linePath = `M ${points[0].x} ${points[0].y}`;
  for (let i = 1; i < points.length; i++) {
    const prev = points[i - 1];
    const curr = points[i];
    const cpx = (prev.x + curr.x) / 2;
    linePath += ` C ${cpx} ${prev.y}, ${cpx} ${curr.y}, ${curr.x} ${curr.y}`;
  }

  const fillPath =
    linePath +
    ` L ${points[points.length - 1].x} ${height} L ${points[0].x} ${height} Z`;

  return (
    <View style={[styles.container, { width, height }]}>
      <Svg width={width} height={height}>
        <Defs>
          <SvgGradient id="fillGrad" x1="0" y1="0" x2="0" y2="1">
            <Stop offset="0" stopColor={color} stopOpacity="0.3" />
            <Stop offset="1" stopColor={color} stopOpacity="0" />
          </SvgGradient>
          <SvgGradient id="lineGrad" x1="0" y1="0" x2="1" y2="0">
            <Stop offset="0" stopColor={color} stopOpacity="0.2" />
            <Stop offset="0.3" stopColor={color} stopOpacity="1" />
            <Stop offset="1" stopColor={color} stopOpacity="1" />
          </SvgGradient>
        </Defs>
        {showFill && <Path d={fillPath} fill="url(#fillGrad)" />}
        <Path
          d={linePath}
          stroke="url(#lineGrad)"
          strokeWidth={2}
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </Svg>
    </View>
  );
}

/**
 * Generate a realistic PPG waveform for display.
 * Uses cardiac pulse shape (systolic peak + dicrotic notch).
 * NOTE: The small noise here is for VISUAL display only, not sensor data.
 */
export function generatePPGWaveform(heartRate: number, numPoints: number, phase: number): number[] {
  const data: number[] = [];
  const beatsPerSample = heartRate / 60 / 30;

  for (let i = 0; i < numPoints; i++) {
    const t = (i + phase) * beatsPerSample * Math.PI * 2;
    const systolic = Math.exp(-((t % (Math.PI * 2)) ** 2) * 2) * 0.8;
    const diastolic = Math.exp(-(((t % (Math.PI * 2)) - 1.2) ** 2) * 4) * 0.3;
    // Visual jitter for waveform rendering only, not sensor data
    const visualNoise = Math.sin(i * 7.3 + phase * 2.1) * 0.025;
    data.push(systolic + diastolic + visualNoise + 0.1);
  }
  return data;
}

/**
 * Generate voice waveform data for display from audio level.
 * Visual only, not used for scoring.
 */
export function generateVoiceWaveform(level: number, numPoints: number, phase: number): number[] {
  const data: number[] = [];
  for (let i = 0; i < numPoints; i++) {
    const t = (i + phase) * 0.15;
    const base = Math.sin(t) * level * 0.5;
    const harmonic1 = Math.sin(t * 2.5) * level * 0.3;
    const harmonic2 = Math.sin(t * 4.1) * level * 0.15;
    const visualNoise = Math.sin(i * 13.7 + phase * 3.3) * level * 0.05;
    data.push(0.5 + base + harmonic1 + harmonic2 + visualNoise);
  }
  return data;
}

const styles = StyleSheet.create({
  container: {
    overflow: 'hidden',
  },
});
