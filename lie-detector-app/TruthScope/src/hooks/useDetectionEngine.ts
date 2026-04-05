/**
 * useDetectionEngine — Wires real PPG, Voice, and Face engines
 * into the Detection screen.
 *
 * When running on a real device with camera/mic access:
 *   - PPG engine processes camera frames for heart rate
 *   - Voice engine analyzes microphone audio for stress indicators
 *   - Face engine tracks facial landmarks for micro-expressions
 *
 * When running in Simulator (no camera/mic hardware):
 *   - Shows "SENSOR UNAVAILABLE" for camera-dependent readings
 *   - Voice metering may partially work (Simulator has limited mic support)
 *   - NO Math.random() fallback. Ever.
 */

import { useEffect, useRef, useState, useCallback } from 'react';
import { Platform } from 'react-native';
import { CameraView } from 'expo-camera';
import { Audio } from 'expo-av';
import { PPGEngine } from '../engines/PPGEngine';
import { VoiceEngine } from '../engines/VoiceEngine';
import { FaceEngine } from '../engines/FaceEngine';
import { DeceptionAnalyzer } from '../engines/DeceptionAnalyzer';
import { DetectionMode, Verdict } from '../utils/types';
import { getBaseline } from '../store';

export interface DetectionReadings {
  heartRate: number;
  hrv: number;
  voiceStress: number;
  faceScore: number;
  signalQuality: number;
  overallScore: number;
  verdict: Verdict;
  confidence: number;
  sensorStatus: {
    camera: 'active' | 'unavailable' | 'waiting';
    mic: 'active' | 'unavailable' | 'waiting';
    face: 'active' | 'unavailable' | 'waiting';
  };
}

const INITIAL_READINGS: DetectionReadings = {
  heartRate: 0,
  hrv: 0,
  voiceStress: 0,
  faceScore: 0,
  signalQuality: 0,
  overallScore: 0,
  verdict: 'scanning',
  confidence: 0,
  sensorStatus: {
    camera: 'waiting',
    mic: 'waiting',
    face: 'waiting',
  },
};

export function useDetectionEngine(
  isRecording: boolean,
  mode: DetectionMode,
) {
  const [readings, setReadings] = useState<DetectionReadings>(INITIAL_READINGS);
  const ppgEngine = useRef<PPGEngine | null>(null);
  const voiceEngine = useRef<VoiceEngine | null>(null);
  const faceEngine = useRef<FaceEngine | null>(null);
  const analyzer = useRef<DeceptionAnalyzer | null>(null);
  const updateTimer = useRef<ReturnType<typeof setInterval> | null>(null);

  // Latest readings from each engine (updated independently)
  const latestPPG = useRef({ hr: 0, hrv: 0, quality: 0 });
  const latestVoice = useRef({ stress: 0 });
  const latestFace = useRef({ score: 0 });

  const startEngines = useCallback(async () => {
    analyzer.current = new DeceptionAnalyzer(mode);

    // Load baseline if available
    const baseline = await getBaseline();

    // PPG Engine (finger or face rPPG mode)
    if (mode === 'finger' || mode === 'face' || mode === 'multi') {
      ppgEngine.current = new PPGEngine({
        mode: mode === 'face' ? 'face' : 'finger',
        onReading: (reading) => {
          latestPPG.current = {
            hr: reading.heartRate,
            hrv: reading.hrv,
            quality: reading.signalQuality,
          };
        },
        onSignalQuality: () => {},
        onHeartbeat: () => {},
      });

      if (baseline) {
        ppgEngine.current.setBaseline(baseline.heartRate, baseline.hrv);
      }
      ppgEngine.current.start();
    }

    // Voice Engine
    if (mode === 'voice' || mode === 'multi') {
      voiceEngine.current = new VoiceEngine({
        onReading: (reading) => {
          latestVoice.current = { stress: reading.stressIndex };
        },
        onSpeechDetected: () => {},
        onStressLevel: () => {},
      });

      if (baseline?.voiceF0) {
        voiceEngine.current.setBaseline(baseline.voiceF0);
      }

      try {
        await voiceEngine.current.start();
        setReadings(prev => ({
          ...prev,
          sensorStatus: { ...prev.sensorStatus, mic: 'active' },
        }));
      } catch {
        setReadings(prev => ({
          ...prev,
          sensorStatus: { ...prev.sensorStatus, mic: 'unavailable' },
        }));
      }
    }

    // Face Engine
    if (mode === 'face' || mode === 'multi') {
      faceEngine.current = new FaceEngine({
        onReading: (reading) => {
          latestFace.current = {
            score: (reading.microExpressionScore * 0.3 +
              (1 - reading.gazeStability) * 25 +
              reading.asymmetryScore * 0.2 +
              (reading.blinkRate > 25 ? 15 : 0)) ,
          };
        },
        onFaceDetected: (detected) => {
          setReadings(prev => ({
            ...prev,
            sensorStatus: {
              ...prev.sensorStatus,
              face: detected ? 'active' : 'waiting',
            },
          }));
        },
        onMicroExpression: () => {},
      });
      faceEngine.current.start();
    }

    // Periodic score update from real engine data
    updateTimer.current = setInterval(() => {
      if (!analyzer.current) return;

      // BUG 1 FIX: Don't score PPG when no data (HR=0 means sensor not ready)
      const physioScore = ppgEngine.current && latestPPG.current.hr > 0
        ? ppgEngine.current.getDeceptionScore(latestPPG.current.hr, latestPPG.current.hrv)
        : -1;
      const vocalScore = voiceEngine.current
        ? voiceEngine.current.getDeceptionScore()
        : -1;
      const facialScore = faceEngine.current
        ? faceEngine.current.getDeceptionScore()
        : -1;

      const result = analyzer.current.analyze({
        physiological: Math.max(0, physioScore),
        vocal: Math.max(0, vocalScore),
        facial: Math.max(0, facialScore),
      });

      setReadings(prev => ({
        heartRate: latestPPG.current.hr,
        hrv: latestPPG.current.hrv,
        voiceStress: Math.round(latestVoice.current.stress),
        faceScore: Math.round(latestFace.current.score),
        signalQuality: latestPPG.current.quality,
        overallScore: result.combined,
        verdict: result.verdict,
        confidence: result.confidence,
        sensorStatus: prev.sensorStatus,
      }));
    }, 500);
  }, [mode]);

  const stopEngines = useCallback(async () => {
    if (updateTimer.current) {
      clearInterval(updateTimer.current);
      updateTimer.current = null;
    }

    ppgEngine.current?.stop();
    ppgEngine.current = null;

    await voiceEngine.current?.stop();
    voiceEngine.current = null;

    faceEngine.current?.stop();
    faceEngine.current = null;

    analyzer.current = null;

    latestPPG.current = { hr: 0, hrv: 0, quality: 0 };
    latestVoice.current = { stress: 0 };
    latestFace.current = { score: 0 };
  }, []);

  // BUG 2 FIX: Use ref to prevent double stopEngines
  const enginesRunning = useRef(false);

  useEffect(() => {
    if (isRecording) {
      enginesRunning.current = true;
      startEngines();
    } else if (enginesRunning.current) {
      enginesRunning.current = false;
      stopEngines();
      setReadings(INITIAL_READINGS);
    }

    return () => {
      if (enginesRunning.current) {
        enginesRunning.current = false;
        stopEngines();
      }
    };
  }, [isRecording, startEngines, stopEngines]);

  // Camera frame callback - call this from the CameraView onFrame
  const processCameraFrame = useCallback((redMean: number, greenMean: number) => {
    if (ppgEngine.current) {
      ppgEngine.current.processFrame(redMean, greenMean, Date.now());
      setReadings(prev => ({
        ...prev,
        sensorStatus: { ...prev.sensorStatus, camera: 'active' },
      }));
    }
  }, []);

  // Face detection callback - call this from CameraView onFacesDetected
  const processFaceData = useCallback((faceData: any) => {
    if (faceEngine.current && faceData) {
      faceEngine.current.processFace(faceData);
    }
  }, []);

  // Mark question timestamp
  const markQuestion = useCallback(() => {
    analyzer.current?.markQuestion();
    voiceEngine.current?.markQuestionStart();
  }, []);

  return {
    readings,
    processCameraFrame,
    processFaceData,
    markQuestion,
  };
}
