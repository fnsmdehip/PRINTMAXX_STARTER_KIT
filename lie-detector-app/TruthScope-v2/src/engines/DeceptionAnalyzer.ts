/**
 * Deception Analyzer v2 - Multi-Modal Fusion Engine
 *
 * Combines signals from PPG, Voice, and Face engines into
 * a single deception probability score.
 *
 * Weighting based on published meta-analyses:
 * - Physiological (PPG/HR/HRV): ~65% accuracy alone
 * - Vocal analysis: ~60% accuracy alone
 * - Facial cues: ~55% accuracy alone
 * - Combined multi-modal: ~70% accuracy (DePaulo et al., 2003)
 */

import { DetectionMode, DetectionResult, Verdict } from '../utils/types';
import { generateId } from '../store';

interface EngineScores {
  physiological: number;
  vocal: number;
  facial: number;
}

const MODE_WEIGHTS: Record<DetectionMode, { physio: number; vocal: number; facial: number }> = {
  finger: { physio: 1.0, vocal: 0.0, facial: 0.0 },
  face:   { physio: 0.3, vocal: 0.0, facial: 0.7 },
  voice:  { physio: 0.0, vocal: 1.0, facial: 0.0 },
  multi:  { physio: 0.40, vocal: 0.30, facial: 0.30 },
};

const THRESHOLDS = {
  truthful: 30,
  deceptive: 55,
};

export class DeceptionAnalyzer {
  private mode: DetectionMode;
  private scoreHistory: { timestamp: number; scores: EngineScores; combined: number }[] = [];
  private questionTimestamps: number[] = [];
  private sessionStartTime: number;

  constructor(mode: DetectionMode) {
    this.mode = mode;
    this.sessionStartTime = Date.now();
  }

  analyze(scores: EngineScores): {
    combined: number;
    verdict: Verdict;
    confidence: number;
    breakdown: EngineScores;
  } {
    const weights = MODE_WEIGHTS[this.mode];
    const now = Date.now();

    let combined = 0;
    let totalWeight = 0;

    if (weights.physio > 0 && scores.physiological >= 0) {
      combined += scores.physiological * weights.physio;
      totalWeight += weights.physio;
    }
    if (weights.vocal > 0 && scores.vocal >= 0) {
      combined += scores.vocal * weights.vocal;
      totalWeight += weights.vocal;
    }
    if (weights.facial > 0 && scores.facial >= 0) {
      combined += scores.facial * weights.facial;
      totalWeight += weights.facial;
    }

    if (totalWeight > 0) {
      combined = combined / totalWeight;
    }

    combined = this.applyTemporalContext(combined, now);
    combined = Math.max(0, Math.min(100, Math.round(combined)));

    this.scoreHistory.push({ timestamp: now, scores, combined });
    if (this.scoreHistory.length > 600) this.scoreHistory.shift();

    const verdict = this.getVerdict(combined);
    const confidence = this.calculateConfidence(scores);

    return { combined, verdict, confidence, breakdown: scores };
  }

  private applyTemporalContext(rawScore: number, now: number): number {
    if (this.scoreHistory.length < 5) return rawScore;

    const recent = this.scoreHistory.slice(-10);
    const avgRecent = recent.reduce((a, b) => a + b.combined, 0) / recent.length;

    const lastQuestion = this.questionTimestamps[this.questionTimestamps.length - 1];
    if (lastQuestion && now - lastQuestion < 5000) {
      return rawScore * 0.8 + avgRecent * 0.2;
    }

    return rawScore * 0.6 + avgRecent * 0.4;
  }

  markQuestion(): void {
    this.questionTimestamps.push(Date.now());
  }

  private getVerdict(score: number): Verdict {
    if (score < THRESHOLDS.truthful) return 'truthful';
    if (score < THRESHOLDS.deceptive) return 'uncertain';
    return 'deceptive';
  }

  private calculateConfidence(scores: EngineScores): number {
    let confidence = 0;
    const weights = MODE_WEIGHTS[this.mode];

    let activeSources = 0;
    if (weights.physio > 0 && scores.physiological >= 0) activeSources++;
    if (weights.vocal > 0 && scores.vocal >= 0) activeSources++;
    if (weights.facial > 0 && scores.facial >= 0) activeSources++;

    const maxSources = Object.values(weights).filter(w => w > 0).length;
    confidence += (activeSources / Math.max(1, maxSources)) * 40;

    if (this.scoreHistory.length >= 5) {
      const recent = this.scoreHistory.slice(-10).map(s => s.combined);
      const mean = recent.reduce((a, b) => a + b, 0) / recent.length;
      const variance = recent.reduce((a, b) => a + (b - mean) ** 2, 0) / recent.length;
      const consistency = Math.max(0, 1 - Math.sqrt(variance) / 30);
      confidence += consistency * 30;
    }

    const duration = (Date.now() - this.sessionStartTime) / 1000;
    confidence += Math.min(30, duration / 2);

    return Math.min(95, Math.round(confidence));
  }

  generateResult(question?: string): DetectionResult {
    const recent = this.scoreHistory.slice(-20);
    if (recent.length === 0) {
      return {
        id: generateId(),
        timestamp: Date.now(),
        mode: this.mode,
        verdict: 'uncertain',
        confidence: 0,
        overallScore: 50,
        breakdown: { physiological: 0, vocal: 0, facial: 0 },
        question,
        duration: (Date.now() - this.sessionStartTime) / 1000,
      };
    }

    const avgScore = recent.reduce((a, b) => a + b.combined, 0) / recent.length;
    const lastResult = recent[recent.length - 1];

    return {
      id: generateId(),
      timestamp: Date.now(),
      mode: this.mode,
      verdict: this.getVerdict(avgScore),
      confidence: this.calculateConfidence(lastResult.scores),
      overallScore: Math.round(avgScore),
      breakdown: {
        physiological: Math.round(
          recent.reduce((a, b) => a + b.scores.physiological, 0) / recent.length
        ),
        vocal: Math.round(
          recent.reduce((a, b) => a + b.scores.vocal, 0) / recent.length
        ),
        facial: Math.round(
          recent.reduce((a, b) => a + b.scores.facial, 0) / recent.length
        ),
      },
      question,
      duration: (Date.now() - this.sessionStartTime) / 1000,
    };
  }

  getTrend(): 'rising' | 'stable' | 'falling' {
    if (this.scoreHistory.length < 10) return 'stable';

    const older = this.scoreHistory.slice(-20, -10);
    const newer = this.scoreHistory.slice(-10);

    if (older.length === 0) return 'stable';

    const olderAvg = older.reduce((a, b) => a + b.combined, 0) / older.length;
    const newerAvg = newer.reduce((a, b) => a + b.combined, 0) / newer.length;

    const diff = newerAvg - olderAvg;
    if (diff > 5) return 'rising';
    if (diff < -5) return 'falling';
    return 'stable';
  }
}
