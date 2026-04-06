/**
 * Voice Stress Analysis Engine v2
 *
 * Analyzes vocal features that change under deception/stress using REAL mic data:
 * 1. Audio metering levels from expo-av Recording API
 * 2. Statistical analysis of level patterns for stress indicators
 * 3. Response latency tracking
 *
 * ZERO Math.random(). All values derived from actual microphone metering data.
 */

import { Audio } from 'expo-av';
import { VoiceReading } from '../utils/types';

const ANALYSIS_INTERVAL_MS = 500;

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
  private questionStartTime: number | null = null;
  private lastSpeechTime = 0;
  private readings: VoiceReading[] = [];
  private audioLevels: number[] = [];

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

      this.recording.setOnRecordingStatusUpdate((status) => {
        if (status.isRecording && status.metering !== undefined) {
          this.processAudioLevel(status.metering);
        }
      });

      await this.recording.startAsync();

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
    const normalizedLevel = Math.max(0, (metering + 60) / 60);
    this.audioLevels.push(normalizedLevel);

    const maxSamples = 50;
    if (this.audioLevels.length > maxSamples) {
      this.audioLevels.shift();
    }

    const isSpeaking = normalizedLevel > 0.15;
    if (isSpeaking) {
      this.lastSpeechTime = Date.now();
    }
    this.config.onSpeechDetected(isSpeaking);
  }

  private analyzeVoice(): void {
    if (!this.isRunning || this.audioLevels.length < 5) return;

    const now = Date.now();
    const recentLevels = this.audioLevels.slice(-20);
    const isSpeaking = recentLevels.some(l => l > 0.15);

    if (!isSpeaking) return;

    const features = this.extractVocalFeatures(recentLevels);

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

  private extractVocalFeatures(levels: number[]): {
    estimatedF0: number;
    jitter: number;
    shimmer: number;
    tremor: number;
  } {
    const mean = levels.reduce((a, b) => a + b, 0) / levels.length;
    const variance = levels.reduce((a, b) => a + (b - mean) ** 2, 0) / levels.length;
    const shimmer = Math.min(1, Math.sqrt(variance) / (mean + 0.01));

    let totalChange = 0;
    for (let i = 1; i < levels.length; i++) {
      totalChange += Math.abs(levels[i] - levels[i - 1]);
    }
    const jitter = Math.min(1, totalChange / (levels.length * (mean + 0.01)));

    const tremor = this.detectLowFreqModulation(levels);

    const estimatedF0 = 100 + mean * 200;

    return { estimatedF0, jitter, shimmer, tremor };
  }

  private detectLowFreqModulation(signal: number[]): number {
    if (signal.length < 6) return 0;

    let peaks = 0;
    for (let i = 1; i < signal.length - 1; i++) {
      if (signal[i] > signal[i - 1] && signal[i] > signal[i + 1]) {
        peaks++;
      }
    }

    const modulationRate = peaks / (signal.length / 10);
    const tremorLikelihood = 1 - Math.min(1, Math.abs(modulationRate - 1));
    return Math.max(0, tremorLikelihood);
  }

  private calculateStressIndex(
    features: { estimatedF0: number; jitter: number; shimmer: number; tremor: number },
    responseLatency: number,
  ): number {
    const scores: number[] = [];

    if (this.baselineF0) {
      const pitchDeviation = Math.abs(features.estimatedF0 - this.baselineF0) / this.baselineF0;
      scores.push(Math.min(100, pitchDeviation * 200));
    }

    scores.push(Math.min(100, features.jitter * 150));
    scores.push(Math.min(100, features.shimmer * 120));
    scores.push(Math.min(100, features.tremor * 100));

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
