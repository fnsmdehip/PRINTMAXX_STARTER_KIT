export type DetectionMode = 'finger' | 'face' | 'voice' | 'multi';

export type Verdict = 'truthful' | 'deceptive' | 'uncertain' | 'scanning';

export interface PPGReading {
  timestamp: number;
  redChannel: number;
  greenChannel: number;
  heartRate: number;
  hrv: number;
  signalQuality: number;
}

export interface VoiceReading {
  timestamp: number;
  fundamentalFreq: number;
  jitter: number;
  shimmer: number;
  voiceTremor: number;
  responseLatency: number;
  stressIndex: number;
}

export interface FaceReading {
  timestamp: number;
  blinkRate: number;
  gazeStability: number;
  microExpressionScore: number;
  asymmetryScore: number;
  lipCompressionDetected: boolean;
  noseWrinkleDetected: boolean;
  eyeContactPercent: number;
}

export interface DetectionResult {
  id: string;
  timestamp: number;
  mode: DetectionMode;
  verdict: Verdict;
  confidence: number;
  overallScore: number;
  breakdown: {
    physiological: number;
    vocal: number;
    facial: number;
  };
  ppgData?: PPGReading[];
  voiceData?: VoiceReading[];
  faceData?: FaceReading[];
  question?: string;
  duration: number;
}

export interface SessionData {
  id: string;
  startTime: number;
  endTime?: number;
  mode: DetectionMode;
  results: DetectionResult[];
  participants?: string[];
  isPartyMode: boolean;
}

export interface UserProfile {
  hasCompletedOnboarding: boolean;
  isPremium: boolean;
  sessionsCompleted: number;
  baselineHR?: number;
  baselineHRV?: number;
  baselineVoiceF0?: number;
}

export interface PartyQuestion {
  id: string;
  text: string;
  category: 'spicy' | 'mild' | 'random' | 'custom';
  isPremium: boolean;
}

export type OnboardingStep =
  | 'welcome'
  | 'howItWorks'
  | 'scienceBehind'
  | 'fingerDemo'
  | 'faceDemo'
  | 'voiceDemo'
  | 'multiModal'
  | 'accuracy'
  | 'disclaimer'
  | 'permissions'
  | 'baseline'
  | 'partyMode'
  | 'premium'
  | 'ready';
