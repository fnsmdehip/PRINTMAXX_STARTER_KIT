/**
 * Facial Analysis Engine
 *
 * Detects deception indicators from facial behavior:
 *
 * 1. Micro-expressions - Brief involuntary expressions (1/25th second)
 *    that reveal concealed emotions (Ekman's FACS research)
 * 2. Blink rate - Increases under cognitive load
 * 3. Gaze patterns - Eye contact avoidance, specific gaze directions
 * 4. Facial asymmetry - Genuine emotions are more symmetric
 * 5. Lip compression - Common suppression behavior
 * 6. Nose wrinkle (AU9) - Disgust/contempt micro-expression
 *
 * Uses device camera for face tracking. On iOS, this leverages
 * Apple's Vision framework for facial landmark detection.
 *
 * Note: Without ARKit (requires bare React Native), we use
 * camera-based analysis with periodic snapshot processing.
 */

import { FaceReading } from '../utils/types';

interface FaceConfig {
  onReading: (reading: FaceReading) => void;
  onFaceDetected: (detected: boolean) => void;
  onMicroExpression: (type: string) => void;
}

interface FaceData {
  bounds: { x: number; y: number; width: number; height: number };
  rollAngle?: number;
  yawAngle?: number;
  smilingProbability?: number;
  leftEyeOpenProbability?: number;
  rightEyeOpenProbability?: number;
  faceID?: number;
}

export class FaceEngine {
  private config: FaceConfig;
  private isRunning = false;
  private readings: FaceReading[] = [];
  private blinkTimestamps: number[] = [];
  private lastEyeState: 'open' | 'closed' = 'open';
  private gazeHistory: { x: number; y: number; timestamp: number }[] = [];
  private expressionHistory: {
    timestamp: number;
    smile: number;
    leftEye: number;
    rightEye: number;
    headRoll: number;
    headYaw: number;
  }[] = [];
  private baselineBlinkRate: number | null = null;
  private baselineGazeStability: number | null = null;

  constructor(config: FaceConfig) {
    this.config = config;
  }

  start(): void {
    this.isRunning = true;
    this.readings = [];
    this.blinkTimestamps = [];
    this.gazeHistory = [];
    this.expressionHistory = [];
  }

  stop(): void {
    this.isRunning = false;
  }

  setBaseline(blinkRate: number, gazeStability: number): void {
    this.baselineBlinkRate = blinkRate;
    this.baselineGazeStability = gazeStability;
  }

  /**
   * Process face detection data from camera.
   * Called with each frame's face detection results.
   */
  processFace(faceData: FaceData): void {
    if (!this.isRunning) return;

    const now = Date.now();
    this.config.onFaceDetected(true);

    const smile = faceData.smilingProbability ?? 0;
    const leftEye = faceData.leftEyeOpenProbability ?? 1;
    const rightEye = faceData.rightEyeOpenProbability ?? 1;
    const headRoll = faceData.rollAngle ?? 0;
    const headYaw = faceData.yawAngle ?? 0;

    // Track expression history
    this.expressionHistory.push({
      timestamp: now,
      smile,
      leftEye,
      rightEye,
      headRoll,
      headYaw,
    });

    // Keep last 30 seconds
    const cutoff = now - 30000;
    this.expressionHistory = this.expressionHistory.filter(e => e.timestamp > cutoff);

    // Blink detection
    const avgEyeOpen = (leftEye + rightEye) / 2;
    if (avgEyeOpen < 0.3 && this.lastEyeState === 'open') {
      this.blinkTimestamps.push(now);
      this.lastEyeState = 'closed';
    } else if (avgEyeOpen > 0.6) {
      this.lastEyeState = 'open';
    }
    this.blinkTimestamps = this.blinkTimestamps.filter(t => t > cutoff);

    // Gaze tracking (approximate from face bounds center + head angle)
    const gazeX = faceData.bounds.x + faceData.bounds.width / 2 + (headYaw * 2);
    const gazeY = faceData.bounds.y + faceData.bounds.height / 2 + (headRoll * 2);
    this.gazeHistory.push({ x: gazeX, y: gazeY, timestamp: now });
    this.gazeHistory = this.gazeHistory.filter(g => g.timestamp > cutoff);

    // Micro-expression detection
    this.detectMicroExpressions(now);

    // Generate reading every 500ms
    if (this.readings.length === 0 || now - this.readings[this.readings.length - 1].timestamp > 500) {
      const reading = this.generateReading(now);
      this.readings.push(reading);
      this.config.onReading(reading);
    }
  }

  onFaceLost(): void {
    this.config.onFaceDetected(false);
  }

  /**
   * Detect micro-expressions by looking for rapid emotional changes.
   * A micro-expression lasts 1/25 to 1/5 of a second (40-200ms).
   */
  private detectMicroExpressions(now: number): void {
    const recent = this.expressionHistory.filter(
      e => e.timestamp > now - 500 && e.timestamp <= now
    );
    if (recent.length < 3) return;

    // Check for rapid smile change (duping delight or suppressed emotion)
    const smiles = recent.map(e => e.smile);
    const maxSmile = Math.max(...smiles);
    const minSmile = Math.min(...smiles);
    if (maxSmile - minSmile > 0.4) {
      // Rapid smile change detected
      const duration = recent[recent.length - 1].timestamp - recent[0].timestamp;
      if (duration < 300) {
        this.config.onMicroExpression('suppressed_smile');
      }
    }

    // Check for asymmetric expression (one eye more closed/open)
    const asymmetry = recent.map(e => Math.abs(e.leftEye - e.rightEye));
    const maxAsymmetry = Math.max(...asymmetry);
    if (maxAsymmetry > 0.3) {
      this.config.onMicroExpression('facial_asymmetry');
    }

    // Check for rapid head movement (aversion)
    if (recent.length >= 2) {
      const first = recent[0];
      const last = recent[recent.length - 1];
      const yawChange = Math.abs(last.headYaw - first.headYaw);
      if (yawChange > 15) {
        this.config.onMicroExpression('gaze_aversion');
      }
    }
  }

  private generateReading(now: number): FaceReading {
    // Blink rate (blinks per minute)
    const recentBlinks = this.blinkTimestamps.filter(t => t > now - 60000);
    const blinkRate = recentBlinks.length;

    // Gaze stability (lower = more unstable = more stress)
    const gazeStability = this.calculateGazeStability();

    // Micro-expression score
    const microScore = this.calculateMicroExpressionScore(now);

    // Asymmetry score
    const asymmetryScore = this.calculateAsymmetryScore();

    // Lip compression (approximated from smile probability patterns)
    const lipCompression = this.detectLipCompression();

    // Eye contact percentage
    const eyeContact = this.calculateEyeContactPercent();

    // Nose wrinkle detection (approximated from expression patterns)
    const noseWrinkle = this.detectNoseWrinkle();

    return {
      timestamp: now,
      blinkRate,
      gazeStability,
      microExpressionScore: microScore,
      asymmetryScore,
      lipCompressionDetected: lipCompression,
      noseWrinkleDetected: noseWrinkle,
      eyeContactPercent: eyeContact,
    };
  }

  private calculateGazeStability(): number {
    if (this.gazeHistory.length < 5) return 1;

    const recent = this.gazeHistory.slice(-30);
    const meanX = recent.reduce((a, b) => a + b.x, 0) / recent.length;
    const meanY = recent.reduce((a, b) => a + b.y, 0) / recent.length;

    const variance = recent.reduce((a, b) => {
      return a + (b.x - meanX) ** 2 + (b.y - meanY) ** 2;
    }, 0) / recent.length;

    // Normalize: lower variance = higher stability
    return Math.max(0, Math.min(1, 1 - Math.sqrt(variance) / 100));
  }

  private calculateMicroExpressionScore(now: number): number {
    // Count rapid expression changes in recent history
    const recent = this.expressionHistory.filter(e => e.timestamp > now - 10000);
    if (recent.length < 3) return 0;

    let rapidChanges = 0;
    for (let i = 2; i < recent.length; i++) {
      const smileChange = Math.abs(recent[i].smile - recent[i - 1].smile);
      const eyeChange = Math.abs(
        (recent[i].leftEye + recent[i].rightEye) / 2 -
        (recent[i - 1].leftEye + recent[i - 1].rightEye) / 2
      );
      const timeDelta = recent[i].timestamp - recent[i - 1].timestamp;

      if (timeDelta < 300 && (smileChange > 0.2 || eyeChange > 0.2)) {
        rapidChanges++;
      }
    }

    return Math.min(100, rapidChanges * 15);
  }

  private calculateAsymmetryScore(): number {
    const recent = this.expressionHistory.slice(-20);
    if (recent.length === 0) return 0;

    const avgAsymmetry = recent.reduce((a, e) => {
      return a + Math.abs(e.leftEye - e.rightEye);
    }, 0) / recent.length;

    return Math.min(100, avgAsymmetry * 200);
  }

  private detectLipCompression(): boolean {
    const recent = this.expressionHistory.slice(-10);
    if (recent.length < 3) return false;

    // Lip compression often manifests as sustained low smile probability
    // with brief moments of tension (smile = 0, very flat)
    const avgSmile = recent.reduce((a, e) => a + e.smile, 0) / recent.length;
    const smileVariance = recent.reduce((a, e) => a + (e.smile - avgSmile) ** 2, 0) / recent.length;

    return avgSmile < 0.1 && smileVariance < 0.01;
  }

  private detectNoseWrinkle(): boolean {
    // Without specific AU9 detection, approximate from expression patterns
    // Nose wrinkle often co-occurs with asymmetric expression and low smile
    const recent = this.expressionHistory.slice(-5);
    if (recent.length < 3) return false;

    const hasAsymmetry = recent.some(e => Math.abs(e.leftEye - e.rightEye) > 0.2);
    const hasLowSmile = recent.every(e => e.smile < 0.15);
    return hasAsymmetry && hasLowSmile;
  }

  private calculateEyeContactPercent(): number {
    if (this.gazeHistory.length < 5) return 100;

    const recent = this.gazeHistory.slice(-60); // ~2 seconds
    // "Eye contact" = face roughly centered and stable
    const centered = recent.filter(g => {
      // Assuming ~180x320 normalized face position, center is contact
      return Math.abs(g.x - 180) < 60 && Math.abs(g.y - 320) < 80;
    });

    return Math.round((centered.length / recent.length) * 100);
  }

  /**
   * Get overall deception score from facial analysis.
   * Returns 0-100 where higher = more deception indicators.
   */
  getDeceptionScore(): number {
    if (this.readings.length === 0) return 0;

    const recent = this.readings.slice(-5);
    const scores: number[] = [];

    for (const r of recent) {
      let score = 0;

      // Elevated blink rate (normal: 15-20/min, stressed: >25/min)
      const baselineBlink = this.baselineBlinkRate ?? 17;
      if (r.blinkRate > baselineBlink * 1.3) {
        score += Math.min(30, (r.blinkRate - baselineBlink) * 2);
      }

      // Low gaze stability
      score += (1 - r.gazeStability) * 25;

      // Micro-expression detections
      score += r.microExpressionScore * 0.3;

      // Facial asymmetry
      score += r.asymmetryScore * 0.2;

      // Lip compression
      if (r.lipCompressionDetected) score += 10;

      // Low eye contact
      if (r.eyeContactPercent < 50) {
        score += (50 - r.eyeContactPercent) * 0.4;
      }

      scores.push(Math.min(100, score));
    }

    return Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
  }
}
