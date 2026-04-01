/**
 * PPG (Photoplethysmography) Engine
 *
 * Measures heart rate and HRV from camera feed.
 * Two modes:
 *   1. Finger mode: finger covers rear camera + flash on = gold standard PPG
 *   2. Face mode (rPPG): front camera detects subtle skin color changes
 *
 * Signal processing pipeline:
 *   Raw frames -> extract color channels -> moving average filter ->
 *   bandpass filter (0.7-4 Hz / 42-240 BPM) -> peak detection ->
 *   HR + HRV calculation
 *
 * Science: Blood volume changes cause measurable absorption differences
 * in red/green light. The pulsatile component (AC) riding on the DC
 * signal gives us the cardiac rhythm.
 */

import { PPGReading } from '../utils/types';

const SAMPLE_RATE = 30; // Camera FPS target
const WINDOW_SIZE = 256; // ~8.5 seconds at 30fps
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

  /**
   * Process a single camera frame.
   * For finger mode: extract average red channel intensity from frame.
   * For face mode: extract green channel from forehead/cheek ROI.
   *
   * @param redMean - Average red channel value (0-255)
   * @param greenMean - Average green channel value (0-255)
   * @param timestamp - Frame timestamp in ms
   */
  processFrame(redMean: number, greenMean: number, timestamp: number): void {
    if (!this.isRunning) return;

    this.frameCount++;
    this.redBuffer.push(redMean);
    this.greenBuffer.push(greenMean);
    this.timestamps.push(timestamp);

    // Keep buffer at window size
    if (this.redBuffer.length > WINDOW_SIZE) {
      this.redBuffer.shift();
      this.greenBuffer.shift();
      this.timestamps.shift();
    }

    // Need at least 3 seconds of data before processing
    if (this.redBuffer.length < SAMPLE_RATE * 3) return;

    // Signal quality check
    const quality = this.calculateSignalQuality();
    this.config.onSignalQuality(quality);

    if (quality < MIN_SIGNAL_QUALITY) return;

    // Process every 5 frames for performance
    if (this.frameCount % 5 !== 0) return;

    const signal = this.config.mode === 'finger'
      ? this.redBuffer
      : this.greenBuffer; // rPPG uses green channel

    // Apply processing pipeline
    const detrended = this.detrend(signal);
    const filtered = this.bandpassFilter(detrended, SAMPLE_RATE, 0.7, 4.0);
    const normalized = this.normalize(filtered);

    // Peak detection
    const peaks = this.detectPeaks(normalized, 0.3);
    const peakTimes = peaks.map(i => this.timestamps[i]);

    // Detect new heartbeat
    if (peakTimes.length > this.peakTimestamps.length) {
      this.config.onHeartbeat();
    }
    this.peakTimestamps = peakTimes;

    // Calculate HR from inter-beat intervals
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

  /**
   * Remove linear trend from signal (DC component removal).
   * Uses simple linear regression detrending.
   */
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

  /**
   * Simple bandpass filter using cascaded moving averages.
   * Not as precise as a true Butterworth, but works for real-time mobile.
   *
   * @param signal - Input signal
   * @param fs - Sampling frequency
   * @param lowCut - Low cutoff frequency (Hz)
   * @param highCut - High cutoff frequency (Hz)
   */
  private bandpassFilter(signal: number[], fs: number, lowCut: number, highCut: number): number[] {
    // High-pass: subtract smoothed version (removes DC and slow drift)
    const highPassWindow = Math.round(fs / lowCut);
    const highPassed = this.subtractMovingAverage(signal, highPassWindow);

    // Low-pass: smooth to remove high-frequency noise
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

  /**
   * Peak detection with minimum distance and threshold.
   * Finds local maxima that exceed the threshold.
   */
  private detectPeaks(signal: number[], threshold: number): number[] {
    const peaks: number[] = [];
    const minDistance = Math.floor(SAMPLE_RATE * 60 / MAX_HR); // Min samples between peaks

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

  /**
   * Calculate heart rate from peak timestamps.
   * Uses median of recent inter-beat intervals for robustness.
   */
  private calculateHeartRate(peakTimes: number[]): number {
    if (peakTimes.length < 2) return 0;

    const intervals: number[] = [];
    const recentPeaks = peakTimes.slice(-10); // Last 10 beats
    for (let i = 1; i < recentPeaks.length; i++) {
      intervals.push(recentPeaks[i] - recentPeaks[i - 1]);
    }

    if (intervals.length === 0) return 0;

    // Use median for robustness against outliers
    const sorted = [...intervals].sort((a, b) => a - b);
    const medianInterval = sorted[Math.floor(sorted.length / 2)];

    return 60000 / medianInterval; // Convert ms interval to BPM
  }

  /**
   * Calculate Heart Rate Variability (HRV).
   * Uses RMSSD (Root Mean Square of Successive Differences) -
   * the gold standard time-domain HRV metric.
   *
   * Higher HRV = relaxed/truthful. Lower HRV = stressed/possibly deceptive.
   */
  private calculateHRV(peakTimes: number[]): number {
    if (peakTimes.length < 3) return 0;

    const intervals: number[] = [];
    const recentPeaks = peakTimes.slice(-15);
    for (let i = 1; i < recentPeaks.length; i++) {
      intervals.push(recentPeaks[i] - recentPeaks[i - 1]);
    }

    if (intervals.length < 2) return 0;

    // RMSSD calculation
    let sumSquaredDiffs = 0;
    for (let i = 1; i < intervals.length; i++) {
      const diff = intervals[i] - intervals[i - 1];
      sumSquaredDiffs += diff * diff;
    }

    return Math.sqrt(sumSquaredDiffs / (intervals.length - 1));
  }

  /**
   * Assess signal quality based on:
   * - Amplitude variation (should have clear pulsatile component)
   * - Periodicity (cardiac signal is quasi-periodic)
   * - Noise level
   */
  private calculateSignalQuality(): number {
    const signal = this.config.mode === 'finger' ? this.redBuffer : this.greenBuffer;
    if (signal.length < SAMPLE_RATE * 2) return 0;

    const recent = signal.slice(-SAMPLE_RATE * 2);

    // Check amplitude range
    const max = Math.max(...recent);
    const min = Math.min(...recent);
    const range = max - min;
    const mean = recent.reduce((a, b) => a + b, 0) / recent.length;

    // For finger mode, good signal has range > 2% of mean
    // For face mode, signal is much weaker, >0.2% of mean
    const minRange = this.config.mode === 'finger' ? mean * 0.02 : mean * 0.002;
    if (range < minRange) return 0.1;

    // Check periodicity via autocorrelation at expected HR range
    const detrended = this.detrend(recent);
    const acf = this.autocorrelation(detrended);

    // Find peak in autocorrelation at HR-plausible lags
    const minLag = Math.floor(SAMPLE_RATE * 60 / MAX_HR);
    const maxLag = Math.floor(SAMPLE_RATE * 60 / MIN_HR);
    let maxAcf = 0;
    for (let lag = minLag; lag <= Math.min(maxLag, acf.length - 1); lag++) {
      if (acf[lag] > maxAcf) maxAcf = acf[lag];
    }

    // Combine metrics
    const amplitudeScore = Math.min(1, range / (minRange * 5));
    const periodicityScore = maxAcf;

    return Math.min(1, (amplitudeScore * 0.4 + periodicityScore * 0.6));
  }

  /**
   * Normalized autocorrelation for periodicity detection.
   */
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

  /**
   * Get deception score based on PPG metrics.
   * Compares current HR/HRV to baseline.
   *
   * Returns 0-100 where:
   *   0-30 = likely truthful (stable, matches baseline)
   *   30-60 = uncertain
   *   60-100 = elevated stress (possible deception)
   */
  getDeceptionScore(currentHR: number, currentHRV: number): number {
    if (!this.baselineHR || !this.baselineHRV) {
      // Without baseline, use population norms
      // Average resting HR: 60-100 BPM
      // Average HRV (RMSSD): 20-60ms
      const hrScore = Math.min(100, Math.max(0, (currentHR - 70) * 2));
      const hrvScore = Math.min(100, Math.max(0, (40 - currentHRV) * 2.5));
      return Math.round((hrScore * 0.4 + hrvScore * 0.6));
    }

    // Compare to personal baseline
    const hrDeviation = ((currentHR - this.baselineHR) / this.baselineHR) * 100;
    const hrvDeviation = ((this.baselineHRV - currentHRV) / this.baselineHRV) * 100;

    // HR increase > 10% from baseline = stress signal
    const hrScore = Math.min(100, Math.max(0, hrDeviation * 5));
    // HRV decrease > 20% from baseline = strong stress signal
    const hrvScore = Math.min(100, Math.max(0, hrvDeviation * 3));

    return Math.round(hrScore * 0.35 + hrvScore * 0.65);
  }
}
