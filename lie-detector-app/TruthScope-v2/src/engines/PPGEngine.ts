/**
 * PPG (Photoplethysmography) Engine v2
 *
 * Measures heart rate and HRV from camera feed.
 * Two modes:
 *   1. Finger mode: finger covers rear camera + flash on = gold standard PPG
 *   2. Face mode (rPPG): front camera detects subtle skin color changes
 *
 * Signal processing pipeline:
 *   Raw frames -> extract color channels -> detrend -> bandpass filter
 *   (0.7-4 Hz / 42-240 BPM) -> peak detection -> HR + HRV calculation
 *
 * ZERO simulated data. If no camera frames arrive, readings stay at 0.
 */

import { PPGReading } from '../utils/types';

const SAMPLE_RATE = 30;
const WINDOW_SIZE = 256;
const MIN_HR = 40;
const MAX_HR = 200;
const MIN_SIGNAL_QUALITY = 0.3;

interface PPGConfig {
  mode: 'finger' | 'face';
  onReading: (reading: PPGReading) => void;
  onSignalQuality: (quality: number) => void;
  onHeartbeat: () => void;
}

export class PPGEngine {
  private config: PPGConfig;
  private redBuffer: number[] = [];
  private greenBuffer: number[] = [];
  private timestamps: number[] = [];
  private peakTimestamps: number[] = [];
  private isRunning = false;
  private baselineHR: number | null = null;
  private baselineHRV: number | null = null;
  private frameCount = 0;

  constructor(config: PPGConfig) {
    this.config = config;
  }

  start(): void {
    this.isRunning = true;
    this.redBuffer = [];
    this.greenBuffer = [];
    this.timestamps = [];
    this.peakTimestamps = [];
    this.frameCount = 0;
  }

  stop(): void {
    this.isRunning = false;
  }

  setBaseline(hr: number, hrv: number): void {
    this.baselineHR = hr;
    this.baselineHRV = hrv;
  }

  processFrame(redMean: number, greenMean: number, timestamp: number): void {
    if (!this.isRunning) return;

    this.frameCount++;
    this.redBuffer.push(redMean);
    this.greenBuffer.push(greenMean);
    this.timestamps.push(timestamp);

    if (this.redBuffer.length > WINDOW_SIZE) {
      this.redBuffer.shift();
      this.greenBuffer.shift();
      this.timestamps.shift();
    }

    if (this.redBuffer.length < SAMPLE_RATE * 3) return;

    const quality = this.calculateSignalQuality();
    this.config.onSignalQuality(quality);

    if (quality < MIN_SIGNAL_QUALITY) return;

    if (this.frameCount % 5 !== 0) return;

    const signal = this.config.mode === 'finger'
      ? this.redBuffer
      : this.greenBuffer;

    const detrended = this.detrend(signal);
    const filtered = this.bandpassFilter(detrended, SAMPLE_RATE, 0.7, 4.0);
    const normalized = this.normalize(filtered);

    const peaks = this.detectPeaks(normalized, 0.3);
    const peakTimes = peaks.map(i => this.timestamps[i]);

    if (peakTimes.length > this.peakTimestamps.length) {
      this.config.onHeartbeat();
    }
    this.peakTimestamps = peakTimes;

    const hr = this.calculateHeartRate(peakTimes);
    const hrv = this.calculateHRV(peakTimes);

    if (hr >= MIN_HR && hr <= MAX_HR) {
      const reading: PPGReading = {
        timestamp,
        redChannel: redMean,
        greenChannel: greenMean,
        heartRate: Math.round(hr),
        hrv: Math.round(hrv * 10) / 10,
        signalQuality: quality,
      };
      this.config.onReading(reading);
    }
  }

  private detrend(signal: number[]): number[] {
    const n = signal.length;
    let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;
    for (let i = 0; i < n; i++) {
      sumX += i;
      sumY += signal[i];
      sumXY += i * signal[i];
      sumX2 += i * i;
    }
    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;
    return signal.map((v, i) => v - (slope * i + intercept));
  }

  private bandpassFilter(signal: number[], fs: number, lowCut: number, highCut: number): number[] {
    const highPassWindow = Math.round(fs / lowCut);
    const highPassed = this.subtractMovingAverage(signal, highPassWindow);
    const lowPassWindow = Math.max(2, Math.round(fs / highCut / 2));
    return this.movingAverage(highPassed, lowPassWindow);
  }

  private movingAverage(signal: number[], windowSize: number): number[] {
    const result: number[] = [];
    const half = Math.floor(windowSize / 2);
    for (let i = 0; i < signal.length; i++) {
      let sum = 0;
      let count = 0;
      for (let j = Math.max(0, i - half); j <= Math.min(signal.length - 1, i + half); j++) {
        sum += signal[j];
        count++;
      }
      result.push(sum / count);
    }
    return result;
  }

  private subtractMovingAverage(signal: number[], windowSize: number): number[] {
    const ma = this.movingAverage(signal, windowSize);
    return signal.map((v, i) => v - ma[i]);
  }

  private normalize(signal: number[]): number[] {
    const max = Math.max(...signal);
    const min = Math.min(...signal);
    const range = max - min;
    if (range < 0.001) return signal.map(() => 0);
    return signal.map(v => (v - min) / range);
  }

  private detectPeaks(signal: number[], threshold: number): number[] {
    const peaks: number[] = [];
    const minDistance = Math.floor(SAMPLE_RATE * 60 / MAX_HR);

    for (let i = 2; i < signal.length - 2; i++) {
      if (
        signal[i] > threshold &&
        signal[i] > signal[i - 1] &&
        signal[i] > signal[i - 2] &&
        signal[i] >= signal[i + 1] &&
        signal[i] >= signal[i + 2]
      ) {
        if (peaks.length === 0 || (i - peaks[peaks.length - 1]) >= minDistance) {
          peaks.push(i);
        }
      }
    }
    return peaks;
  }

  private calculateHeartRate(peakTimes: number[]): number {
    if (peakTimes.length < 2) return 0;

    const intervals: number[] = [];
    const recentPeaks = peakTimes.slice(-10);
    for (let i = 1; i < recentPeaks.length; i++) {
      intervals.push(recentPeaks[i] - recentPeaks[i - 1]);
    }

    if (intervals.length === 0) return 0;

    const sorted = [...intervals].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    const medianInterval = sorted.length % 2 === 0
      ? (sorted[mid - 1] + sorted[mid]) / 2
      : sorted[mid];

    return 60000 / medianInterval;
  }

  private calculateHRV(peakTimes: number[]): number {
    if (peakTimes.length < 3) return 0;

    const intervals: number[] = [];
    const recentPeaks = peakTimes.slice(-15);
    for (let i = 1; i < recentPeaks.length; i++) {
      intervals.push(recentPeaks[i] - recentPeaks[i - 1]);
    }

    if (intervals.length < 2) return 0;

    let sumSquaredDiffs = 0;
    for (let i = 1; i < intervals.length; i++) {
      const diff = intervals[i] - intervals[i - 1];
      sumSquaredDiffs += diff * diff;
    }

    return Math.sqrt(sumSquaredDiffs / (intervals.length - 1));
  }

  private calculateSignalQuality(): number {
    const signal = this.config.mode === 'finger' ? this.redBuffer : this.greenBuffer;
    if (signal.length < SAMPLE_RATE * 2) return 0;

    const recent = signal.slice(-SAMPLE_RATE * 2);

    const max = Math.max(...recent);
    const min = Math.min(...recent);
    const range = max - min;
    const mean = recent.reduce((a, b) => a + b, 0) / recent.length;

    const minRange = this.config.mode === 'finger' ? mean * 0.02 : mean * 0.002;
    if (range < minRange) return 0.1;

    const detrended = this.detrend(recent);
    const acf = this.autocorrelation(detrended);

    const minLag = Math.floor(SAMPLE_RATE * 60 / MAX_HR);
    const maxLag = Math.floor(SAMPLE_RATE * 60 / MIN_HR);
    let maxAcf = 0;
    for (let lag = minLag; lag <= Math.min(maxLag, acf.length - 1); lag++) {
      if (acf[lag] > maxAcf) maxAcf = acf[lag];
    }

    const amplitudeScore = Math.min(1, range / (minRange * 5));
    const periodicityScore = maxAcf;

    return Math.min(1, (amplitudeScore * 0.4 + periodicityScore * 0.6));
  }

  private autocorrelation(signal: number[]): number[] {
    const n = signal.length;
    const mean = signal.reduce((a, b) => a + b, 0) / n;
    const centered = signal.map(v => v - mean);
    const variance = centered.reduce((a, b) => a + b * b, 0);

    if (variance < 0.001) return new Array(n).fill(0);

    const result: number[] = [];
    const maxLag = Math.floor(n / 2);
    for (let lag = 0; lag < maxLag; lag++) {
      let sum = 0;
      for (let i = 0; i < n - lag; i++) {
        sum += centered[i] * centered[i + lag];
      }
      result.push(sum / variance);
    }
    return result;
  }

  getDeceptionScore(currentHR: number, currentHRV: number): number {
    if (!this.baselineHR || !this.baselineHRV) {
      const hrScore = Math.min(100, Math.max(0, (currentHR - 70) * 2));
      const hrvScore = Math.min(100, Math.max(0, (40 - currentHRV) * 2.5));
      return Math.round((hrScore * 0.4 + hrvScore * 0.6));
    }

    const hrDeviation = ((currentHR - this.baselineHR) / this.baselineHR) * 100;
    const hrvDeviation = ((this.baselineHRV - currentHRV) / this.baselineHRV) * 100;

    const hrScore = Math.min(100, Math.max(0, hrDeviation * 5));
    const hrvScore = Math.min(100, Math.max(0, hrvDeviation * 3));

    return Math.round(hrScore * 0.35 + hrvScore * 0.65);
  }
}
