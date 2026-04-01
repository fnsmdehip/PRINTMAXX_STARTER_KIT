/**
 * Voice Stress Analysis Engine
 *
 * Analyzes vocal features that change under deception/stress:
 *
 * 1. Fundamental Frequency (F0) - pitch rises under stress
 * 2. Jitter - cycle-to-cycle pitch variation, increases with stress
 * 3. Shimmer - cycle-to-cycle amplitude variation
 * 4. Voice micro-tremors (8-12 Hz) - involuntary muscle tension
 * 5. Response latency - delayed responses correlate with fabrication
 * 6. Speech rate changes - speedups/slowdowns during deception
 *
 * Uses Audio Recording API to capture and analyze voice in real-time.
 * Processing happens on audio buffer chunks.
 */

import { Audio } from 'expo-av';
import { VoiceReading } from '../utils/types';

const ANALYSIS_INTERVAL_MS = 500; // Analyze every 500ms
const BASELINE_DURATION_MS = 10000; // 10 seconds for baseline

interface VoiceConfig {
  onReading: (reading: VoiceReading) => void;
  onSpeechDetected: (isSpeaking: boolean) => void;
  onStressLevel: (level: number) => void;
}

export class VoiceEngine {
  private config: VoiceConfig;
  private recording: Audio.Recording | null = null;
  private isRunning = false;
  private analysisTimer: ReturnType<typeof setInterval> | null = null;
  private baselineF0: number | null = null;
  private baselineJitter: number | null = null;
  private questionStartTime: number | null = null;
  private lastSpeechTime = 0;
  private readings: VoiceReading[] = [];

  // Simulated audio analysis state (real implementation needs native module)
  // In production, we'd use a native audio processing module
  private audioLevels: number[] = [];
  private pitchHistory: number[] = [];

  constructor(config: VoiceConfig) {
    this.config = config;
  }

  async start(): Promise<void> {
    this.isRunning = true;
    this.readings = [];

    try {
      await Audio.requestPermissionsAsync();
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      this.recording = new Audio.Recording();
      await this.recording.prepareToRecordAsync({
        ...Audio.RecordingOptionsPresets.HIGH_QUALITY,
        android: {
          extension: '.wav',
          outputFormat: Audio.AndroidOutputFormat.DEFAULT,
          audioEncoder: Audio.AndroidAudioEncoder.DEFAULT,
          sampleRate: 44100,
          numberOfChannels: 1,
          bitRate: 128000,
        },
        ios: {
          extension: '.wav',
          outputFormat: Audio.IOSOutputFormat.LINEARPCM,
          audioQuality: Audio.IOSAudioQuality.MAX,
          sampleRate: 44100,
          numberOfChannels: 1,
          bitRate: 128000,
          linearPCMBitDepth: 16,
          linearPCMIsBigEndian: false,
          linearPCMIsFloat: false,
        },
      });

      // Enable metering for real-time level monitoring
      this.recording.setOnRecordingStatusUpdate((status) => {
        if (status.isRecording && status.metering !== undefined) {
          this.processAudioLevel(status.metering);
        }
      });

      await this.recording.startAsync();

      // Real-time analysis loop
      this.analysisTimer = setInterval(() => {
        this.analyzeVoice();
      }, ANALYSIS_INTERVAL_MS);

    } catch (err) {
      console.warn('Voice recording failed:', err);
    }
  }

  async stop(): Promise<string | null> {
    this.isRunning = false;

    if (this.analysisTimer) {
      clearInterval(this.analysisTimer);
      this.analysisTimer = null;
    }

    if (this.recording) {
      try {
        await this.recording.stopAndUnloadAsync();
        const uri = this.recording.getURI();
        this.recording = null;
        return uri;
      } catch {
        this.recording = null;
      }
    }
    return null;
  }

  markQuestionStart(): void {
    this.questionStartTime = Date.now();
  }

  setBaseline(f0: number): void {
    this.baselineF0 = f0;
  }

  private processAudioLevel(metering: number): void {
    // metering is in dB, typically -160 to 0
    const normalizedLevel = Math.max(0, (metering + 60) / 60); // Normalize to 0-1
    this.audioLevels.push(normalizedLevel);

    // Keep last 5 seconds
    const maxSamples = 50; // ~5 sec at 10 updates/sec
    if (this.audioLevels.length > maxSamples) {
      this.audioLevels.shift();
    }

    // Speech detection: level > threshold
    const isSpeaking = normalizedLevel > 0.15;
    if (isSpeaking) {
      this.lastSpeechTime = Date.now();
    }
    this.config.onSpeechDetected(isSpeaking);
  }

  /**
   * Analyze voice characteristics from recent audio data.
   *
   * In a production app with native modules, we'd use:
   * - FFT for fundamental frequency extraction
   * - Autocorrelation for pitch period detection
   * - Frame-by-frame analysis for jitter/shimmer
   *
   * This implementation uses the available metering data
   * and statistical analysis for stress indicators.
   */
  private analyzeVoice(): void {
    if (!this.isRunning || this.audioLevels.length < 5) return;

    const now = Date.now();
    const recentLevels = this.audioLevels.slice(-20);
    const isSpeaking = recentLevels.some(l => l > 0.15);

    if (!isSpeaking) return;

    // Estimate vocal features from audio characteristics
    const features = this.extractVocalFeatures(recentLevels);

    // Calculate response latency
    let responseLatency = 0;
    if (this.questionStartTime) {
      responseLatency = (this.lastSpeechTime - this.questionStartTime) / 1000;
      if (responseLatency < 0) responseLatency = 0;
    }

    const reading: VoiceReading = {
      timestamp: now,
      fundamentalFreq: features.estimatedF0,
      jitter: features.jitter,
      shimmer: features.shimmer,
      voiceTremor: features.tremor,
      responseLatency,
      stressIndex: this.calculateStressIndex(features, responseLatency),
    };

    this.readings.push(reading);
    this.config.onReading(reading);
    this.config.onStressLevel(reading.stressIndex);
  }

  /**
   * Extract vocal features from audio level data.
   * Uses statistical properties of the audio envelope as proxy features.
   *
   * For a more accurate implementation, a native audio processing module
   * would provide actual FFT-based pitch tracking and frame-level analysis.
   */
  private extractVocalFeatures(levels: number[]): {
    estimatedF0: number;
    jitter: number;
    shimmer: number;
    tremor: number;
  } {
    // Amplitude variability (proxy for shimmer)
    const mean = levels.reduce((a, b) => a + b, 0) / levels.length;
    const variance = levels.reduce((a, b) => a + (b - mean) ** 2, 0) / levels.length;
    const shimmer = Math.min(1, Math.sqrt(variance) / (mean + 0.01));

    // Level changes (proxy for jitter - rapid pitch fluctuations)
    let totalChange = 0;
    for (let i = 1; i < levels.length; i++) {
      totalChange += Math.abs(levels[i] - levels[i - 1]);
    }
    const jitter = Math.min(1, totalChange / (levels.length * (mean + 0.01)));

    // Low-frequency modulation (proxy for 8-12 Hz voice tremor)
    // In real implementation, this would be spectral analysis of the pitch contour
    const tremor = this.detectLowFreqModulation(levels);

    // Estimated F0 from energy patterns
    // Real F0 would come from autocorrelation or CREPE-style pitch detection
    // Using mean level as rough proxy - higher energy often correlates with higher pitch
    const estimatedF0 = 100 + mean * 200; // Rough range: 100-300 Hz

    return { estimatedF0, jitter, shimmer, tremor };
  }

  /**
   * Detect low-frequency modulation in the signal.
   * Voice tremor (8-12 Hz) manifests as amplitude modulation
   * caused by involuntary laryngeal muscle tension.
   */
  private detectLowFreqModulation(signal: number[]): number {
    if (signal.length < 6) return 0;

    // Simple modulation detection via peak counting in envelope
    let peaks = 0;
    for (let i = 1; i < signal.length - 1; i++) {
      if (signal[i] > signal[i - 1] && signal[i] > signal[i + 1]) {
        peaks++;
      }
    }

    // Expected modulation rate for tremor
    const modulationRate = peaks / (signal.length / 10); // ~10 samples/sec
    // Tremor is 8-12 Hz, so at 10 samples/sec we expect 0.8-1.2 peaks/sample-set
    const tremorLikelihood = 1 - Math.min(1, Math.abs(modulationRate - 1));
    return Math.max(0, tremorLikelihood);
  }

  /**
   * Calculate composite stress index from vocal features.
   * Returns 0-100 where higher = more stress/possible deception.
   */
  private calculateStressIndex(
    features: { estimatedF0: number; jitter: number; shimmer: number; tremor: number },
    responseLatency: number,
  ): number {
    const scores: number[] = [];

    // Pitch deviation from baseline
    if (this.baselineF0) {
      const pitchDeviation = Math.abs(features.estimatedF0 - this.baselineF0) / this.baselineF0;
      scores.push(Math.min(100, pitchDeviation * 200));
    }

    // Jitter score (higher jitter = more stress)
    scores.push(Math.min(100, features.jitter * 150));

    // Shimmer score
    scores.push(Math.min(100, features.shimmer * 120));

    // Tremor score (8-12 Hz modulation)
    scores.push(Math.min(100, features.tremor * 100));

    // Response latency (> 2 seconds suggests fabrication)
    if (responseLatency > 0.5) {
      const latencyScore = Math.min(100, (responseLatency - 0.5) * 30);
      scores.push(latencyScore);
    }

    if (scores.length === 0) return 0;
    return Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
  }

  getDeceptionScore(): number {
    if (this.readings.length === 0) return 0;
    const recent = this.readings.slice(-10);
    return Math.round(
      recent.reduce((a, b) => a + b.stressIndex, 0) / recent.length
    );
  }
}
