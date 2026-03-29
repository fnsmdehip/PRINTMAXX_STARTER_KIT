export interface ConsentRecord {
  id: string;
  templateId: string | null;
  title: string;
  parties: Party[];
  terms: string;
  details: string;
  signatures: Signature[];
  timestamp: string;
  geolocation: GeoData | null;
  isPremium: boolean;
}

export interface Party {
  name: string;
  role: string;
  email?: string;
}

export interface Signature {
  partyName: string;
  dataUrl: string;
  timestamp: string;
}

export interface GeoData {
  latitude: number;
  longitude: number;
  accuracy: number;
}

export interface EncryptedRecord {
  id: string;
  iv: string;
  ciphertext: string;
  hmac: string;
  salt: string;
  createdAt: string;
  title: string;
}

export interface AuditEntry {
  id: string;
  action: 'create' | 'view' | 'export' | 'delete' | 'backup_export' | 'backup_import' | 'login' | 'login_failed' | 'lockout' | 'video_recorded' | 'video_viewed' | 'video_exported';
  recordId?: string;
  timestamp: string;
  details: string;
  prevHash: string;
  hash: string;
}

export interface VideoConsentRecord {
  id: string;
  consentRecordId?: string;
  partyA: string;
  partyB: string;
  timestamp: string;
  gps: { latitude: number; longitude: number } | null;
  durationSeconds: number;
  encryptedAt: string;
}

export interface Template {
  id: string;
  name: string;
  description: string;
  category: string;
  isPremium: boolean;
  parties: { role: string; placeholder: string }[];
  termsTemplate: string;
  detailsPrompts: string[];
}

export interface AppState {
  isUnlocked: boolean;
  isPinSet: boolean;
  isPremium: boolean;
  currentView: ViewName;
  selectedRecord: string | null;
  selectedTemplate: string | null;
}

export type ViewName =
  | 'pin'
  | 'pin-setup'
  | 'dashboard'
  | 'create'
  | 'templates'
  | 'viewer'
  | 'audit'
  | 'backup'
  | 'settings'
  | 'paywall'
  | 'video-consent'
  | 'video-player';
