import { useState, useRef, useEffect, useCallback } from 'react';
import { encrypt } from '../crypto/vault';
import { computeHmac, computeChainHash } from '../crypto/hmac';
import { saveVideo, addAuditEntry, getLastAuditHash } from '../db/store';
import type { ViewName } from '../types';

interface VideoConsentProps {
  pin: string;
  navigate: (view: ViewName) => void;
  isPremium: boolean;
}

const MAX_DURATION_SECONDS = 300; // 5 minutes

export default function VideoConsent({ pin, navigate, isPremium }: VideoConsentProps) {
  const [permissionState, setPermissionState] = useState<'pending' | 'granted' | 'denied'>('pending');
  const [isRecording, setIsRecording] = useState(false);
  const [recordedBlob, setRecordedBlob] = useState<Blob | null>(null);
  const [recordedUrl, setRecordedUrl] = useState<string | null>(null);
  const [duration, setDuration] = useState(0);
  const [gps, setGps] = useState<{ latitude: number; longitude: number } | null>(null);
  const [startTimestamp, setStartTimestamp] = useState<string>('');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [partyA, setPartyA] = useState('');
  const [partyB, setPartyB] = useState('');
  const [step, setStep] = useState<'setup' | 'camera' | 'preview'>('setup');
  const [facingMode, setFacingMode] = useState<'user' | 'environment'>('user');

  const videoRef = useRef<HTMLVideoElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const durationTimerRef = useRef<number | null>(null);
  const timestampOverlayRef = useRef<HTMLDivElement>(null);

  // Premium gate
  if (!isPremium) {
    return (
      <div className="min-h-screen bg-navy flex flex-col items-center justify-center px-4">
        <div className="text-center max-w-md">
          <div className="w-20 h-20 rounded-2xl bg-coral/20 flex items-center justify-center mx-auto mb-4">
            <svg className="w-10 h-10 text-coral" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-white mb-2">Video Consent Recording</h2>
          <p className="text-gray-400 mb-6">
            Record video consent with live timestamps, GPS coordinates, and AES-256 encryption. This is a premium feature.
          </p>
          <button
            onClick={() => navigate('paywall')}
            className="px-8 py-3 bg-coral text-white rounded-xl font-medium"
          >
            Upgrade to Pro
          </button>
          <button
            onClick={() => navigate('dashboard')}
            className="block mx-auto mt-4 text-gray-500 text-sm"
          >
            Back to Vault
          </button>
        </div>
      </div>
    );
  }

  const formatDuration = (seconds: number): string => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  const formatTimestamp = (): string => {
    return new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC';
  };

  const requestPermissions = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode }, audio: true });
      stream.getTracks().forEach(t => t.stop());
      setPermissionState('granted');
    } catch {
      setPermissionState('denied');
    }
  };

  const captureGPS = async () => {
    if (!('geolocation' in navigator)) return;
    try {
      const pos = await new Promise<GeolocationPosition>((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {
          enableHighAccuracy: true,
          timeout: 10000,
        });
      });
      setGps({
        latitude: Math.round(pos.coords.latitude * 1000000) / 1000000,
        longitude: Math.round(pos.coords.longitude * 1000000) / 1000000,
      });
    } catch {
      // GPS not available, continue without it
    }
  };

  const startCamera = async () => {
    setError('');
    await requestPermissions();
    await captureGPS();
    setStep('camera');

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode, width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: true,
      });
      streamRef.current = stream;

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.muted = true;
        await videoRef.current.play();
      }
    } catch (err) {
      setError('Failed to access camera and microphone. Please grant permissions.');
      setStep('setup');
    }
  };

  const startRecording = () => {
    if (!streamRef.current) return;

    chunksRef.current = [];
    setStartTimestamp(formatTimestamp());
    setDuration(0);

    const mimeType = MediaRecorder.isTypeSupported('video/webm;codecs=vp9,opus')
      ? 'video/webm;codecs=vp9,opus'
      : MediaRecorder.isTypeSupported('video/webm;codecs=vp8,opus')
        ? 'video/webm;codecs=vp8,opus'
        : 'video/webm';

    const recorder = new MediaRecorder(streamRef.current, {
      mimeType,
      videoBitsPerSecond: 2500000,
    });

    recorder.ondataavailable = (e) => {
      if (e.data.size > 0) {
        chunksRef.current.push(e.data);
      }
    };

    recorder.onstop = () => {
      const blob = new Blob(chunksRef.current, { type: mimeType });
      setRecordedBlob(blob);
      const url = URL.createObjectURL(blob);
      setRecordedUrl(url);
      setStep('preview');

      // Stop the live camera
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(t => t.stop());
        streamRef.current = null;
      }
    };

    mediaRecorderRef.current = recorder;
    recorder.start(1000); // collect data every second
    setIsRecording(true);

    // Duration timer
    durationTimerRef.current = window.setInterval(() => {
      setDuration(prev => {
        if (prev >= MAX_DURATION_SECONDS - 1) {
          stopRecording();
          return MAX_DURATION_SECONDS;
        }
        return prev + 1;
      });
    }, 1000);
  };

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
    if (durationTimerRef.current) {
      clearInterval(durationTimerRef.current);
      durationTimerRef.current = null;
    }
    setIsRecording(false);
  }, []);

  const handleRetake = async () => {
    if (recordedUrl) {
      URL.revokeObjectURL(recordedUrl);
    }
    setRecordedBlob(null);
    setRecordedUrl(null);
    setDuration(0);
    await startCamera();
  };

  const handleSave = async () => {
    if (!recordedBlob) return;
    setSaving(true);
    setError('');

    try {
      // Convert blob to base64
      const arrayBuffer = await recordedBlob.arrayBuffer();
      const bytes = new Uint8Array(arrayBuffer);
      let binary = '';
      for (let i = 0; i < bytes.length; i++) {
        binary += String.fromCharCode(bytes[i]);
      }
      const base64Video = btoa(binary);

      // Encrypt the video data
      const { iv, ciphertext, salt } = await encrypt(base64Video, pin);

      // Create and encrypt metadata
      const metadata = {
        type: 'video_consent',
        partyA,
        partyB,
        timestamp: startTimestamp,
        gps,
        durationSeconds: duration,
        encryptedAt: new Date().toISOString(),
      };
      const metaStr = JSON.stringify(metadata);
      const { iv: metaIv, ciphertext: metaCiphertext, salt: metaSalt } = await encrypt(metaStr, pin);

      // HMAC for integrity
      const hmac = await computeHmac(ciphertext);

      const videoId = crypto.randomUUID();

      // Save to IndexedDB
      await saveVideo({
        id: videoId,
        encryptedBlob: ciphertext,
        encryptedMeta: metaCiphertext,
        iv,
        salt,
        metaIv,
        metaSalt,
        hmac,
        timestamp: new Date().toISOString(),
        title: `Video Consent: ${partyA} & ${partyB}`,
      });

      // Audit log
      const prevHash = await getLastAuditHash();
      const auditContent = `video_recorded|${videoId}|${new Date().toISOString()}|${partyA} & ${partyB}`;
      const hash = await computeChainHash(auditContent, prevHash);
      await addAuditEntry({
        id: crypto.randomUUID(),
        action: 'video_recorded',
        recordId: videoId,
        timestamp: new Date().toISOString(),
        details: `Video consent recorded: ${partyA} & ${partyB} (${formatDuration(duration)})`,
        prevHash,
        hash,
      });

      // Cleanup
      if (recordedUrl) URL.revokeObjectURL(recordedUrl);
      navigate('dashboard');
    } catch (err) {
      setError('Failed to encrypt and save video. Please try again.');
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const toggleCamera = async () => {
    const newMode = facingMode === 'user' ? 'environment' : 'user';
    setFacingMode(newMode);

    if (streamRef.current && !isRecording) {
      streamRef.current.getTracks().forEach(t => t.stop());
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: newMode, width: { ideal: 1280 }, height: { ideal: 720 } },
          audio: true,
        });
        streamRef.current = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch {
        // Failed to switch, stay on current
      }
    }
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(t => t.stop());
      }
      if (durationTimerRef.current) {
        clearInterval(durationTimerRef.current);
      }
      if (recordedUrl) {
        URL.revokeObjectURL(recordedUrl);
      }
    };
  }, []);

  // Setup step: enter party names
  if (step === 'setup') {
    return (
      <div className="p-4 md:p-6 max-w-2xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <button onClick={() => navigate('dashboard')} className="text-gray-400 flex items-center gap-1">
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back
          </button>
        </div>

        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-coral/20 flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-coral" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </div>
          <h2 className="text-xl font-bold text-white mb-2">Video Consent Recording</h2>
          <p className="text-gray-400 text-sm">Record verbal consent with live timestamps and GPS. Encrypted with AES-256-GCM.</p>
        </div>

        <div className="space-y-4 mb-6">
          <label className="block">
            <span className="text-gray-300 text-sm font-medium">Party A Name</span>
            <input
              type="text"
              value={partyA}
              onChange={(e) => setPartyA(e.target.value)}
              placeholder="First person's full name"
              className="mt-1 w-full bg-navy-light border border-gray-700 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:border-coral focus:outline-none"
            />
          </label>
          <label className="block">
            <span className="text-gray-300 text-sm font-medium">Party B Name</span>
            <input
              type="text"
              value={partyB}
              onChange={(e) => setPartyB(e.target.value)}
              placeholder="Second person's full name"
              className="mt-1 w-full bg-navy-light border border-gray-700 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:border-coral focus:outline-none"
            />
          </label>
        </div>

        {error && <p className="text-red-400 text-sm text-center mb-4">{error}</p>}

        <button
          onClick={startCamera}
          disabled={!partyA.trim() || !partyB.trim()}
          className={`w-full py-4 rounded-xl font-medium text-lg transition-colors ${
            partyA.trim() && partyB.trim()
              ? 'bg-coral text-white'
              : 'bg-gray-700 text-gray-500 cursor-not-allowed'
          }`}
        >
          Start Camera
        </button>

        <div className="mt-6 bg-navy-light border border-gray-700 rounded-xl p-4 space-y-2">
          <p className="text-gray-300 text-sm font-medium">How it works:</p>
          <p className="text-gray-500 text-xs">1. Both parties must be visible in frame</p>
          <p className="text-gray-500 text-xs">2. Live timestamp and GPS are overlaid on the recording</p>
          <p className="text-gray-500 text-xs">3. Maximum 5 minute recording</p>
          <p className="text-gray-500 text-xs">4. Video is encrypted with AES-256-GCM before storage</p>
          <p className="text-gray-500 text-xs">5. Only you can decrypt it with your PIN</p>
        </div>
      </div>
    );
  }

  // Camera/recording step
  if (step === 'camera') {
    return (
      <div className="fixed inset-0 bg-black z-50 flex flex-col">
        {/* Video feed */}
        <div className="flex-1 relative">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="w-full h-full object-cover"
            style={{ transform: facingMode === 'user' ? 'scaleX(-1)' : 'none' }}
          />

          {/* Top overlay: party names */}
          <div className="absolute top-0 left-0 right-0 bg-black/50 px-4 py-3 pt-safe">
            <div className="flex items-center justify-center gap-3">
              <span className="text-white text-sm font-semibold">{partyA}</span>
              <svg className="w-4 h-4 text-white/60" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
              </svg>
              <span className="text-white text-sm font-semibold">{partyB}</span>
            </div>
          </div>

          {/* Timestamp + GPS overlay */}
          <div ref={timestampOverlayRef} className="absolute top-14 left-4 space-y-1">
            <div className="flex items-center gap-2 bg-black/60 px-2.5 py-1 rounded">
              {isRecording && (
                <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
              )}
              <span className="text-white text-xs font-mono">{formatTimestamp()}</span>
            </div>
            {gps && (
              <div className="bg-black/50 px-2 py-0.5 rounded self-start">
                <span className="text-white/70 text-[10px] font-mono">
                  GPS: {gps.latitude}, {gps.longitude}
                </span>
              </div>
            )}
          </div>

          {/* Duration display */}
          {isRecording && (
            <div className="absolute top-14 right-4 bg-red-600/90 px-3 py-1 rounded">
              <span className="text-white text-sm font-mono font-bold">{formatDuration(duration)}</span>
              <span className="text-white/50 text-xs font-mono"> / {formatDuration(MAX_DURATION_SECONDS)}</span>
            </div>
          )}
        </div>

        {/* Bottom controls */}
        <div className="bg-black/70 px-4 py-6 pb-safe">
          <div className="flex items-center justify-center gap-10">
            {/* Flip camera */}
            <button
              onClick={toggleCamera}
              disabled={isRecording}
              className={`w-12 h-12 rounded-full bg-white/15 flex items-center justify-center ${isRecording ? 'opacity-30' : ''}`}
            >
              <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>

            {/* Record / Stop button */}
            <button
              onClick={isRecording ? stopRecording : startRecording}
              className="w-[72px] h-[72px] rounded-full border-4 border-white flex items-center justify-center"
            >
              {isRecording ? (
                <div className="w-7 h-7 rounded bg-red-500 animate-pulse" />
              ) : (
                <div className="w-14 h-14 rounded-full bg-red-500" />
              )}
            </button>

            {/* Close button */}
            <button
              onClick={() => {
                if (streamRef.current) {
                  streamRef.current.getTracks().forEach(t => t.stop());
                  streamRef.current = null;
                }
                if (durationTimerRef.current) clearInterval(durationTimerRef.current);
                setStep('setup');
                setIsRecording(false);
              }}
              className="w-12 h-12 rounded-full bg-white/15 flex items-center justify-center"
            >
              <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <p className="text-center mt-3 text-xs text-white/60">
            {isRecording
              ? 'Recording... tap the square to stop'
              : 'Position both parties in frame, then tap record'}
          </p>
        </div>
      </div>
    );
  }

  // Preview step
  if (step === 'preview' && recordedUrl) {
    return (
      <div className="p-4 md:p-6 max-w-2xl mx-auto">
        <div className="text-center mb-6">
          <svg className="w-16 h-16 text-green-400 mx-auto mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h2 className="text-xl font-bold text-white">Recording Complete</h2>
          <p className="text-gray-400 text-lg font-mono mt-1">{formatDuration(duration)}</p>
        </div>

        {/* Video preview */}
        <div className="rounded-xl overflow-hidden mb-4 bg-black">
          <video
            src={recordedUrl}
            controls
            playsInline
            className="w-full max-h-[50vh]"
          />
        </div>

        {/* Metadata card */}
        <div className="bg-navy-light border border-gray-700 rounded-xl p-4 mb-4 space-y-3">
          <div className="flex justify-between">
            <span className="text-gray-400 text-sm">Parties</span>
            <span className="text-white text-sm font-medium">{partyA} & {partyB}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400 text-sm">Recorded At</span>
            <span className="text-white text-sm font-mono">{startTimestamp}</span>
          </div>
          {gps && (
            <div className="flex justify-between">
              <span className="text-gray-400 text-sm">GPS Coordinates</span>
              <span className="text-white text-sm font-mono">{gps.latitude}, {gps.longitude}</span>
            </div>
          )}
          <div className="flex justify-between">
            <span className="text-gray-400 text-sm">Duration</span>
            <span className="text-white text-sm font-mono">{formatDuration(duration)}</span>
          </div>
        </div>

        {/* Security badge */}
        <div className="bg-green-900/20 border border-green-800/30 rounded-xl p-3 mb-6 flex items-center gap-2">
          <svg className="w-5 h-5 text-green-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          <span className="text-green-400 text-sm">Will be encrypted with AES-256-GCM before storage</span>
        </div>

        {error && <p className="text-red-400 text-sm text-center mb-4">{error}</p>}

        {/* Actions */}
        <div className="flex gap-3">
          <button
            onClick={handleRetake}
            disabled={saving}
            className="flex-1 py-3 rounded-xl border border-gray-600 text-gray-300 font-medium disabled:opacity-50"
          >
            Retake
          </button>
          <button
            onClick={handleSave}
            disabled={saving}
            className="flex-[2] py-3 rounded-xl bg-coral text-white font-medium disabled:opacity-50"
          >
            {saving ? (
              <span className="flex items-center justify-center gap-2">
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Encrypting...
              </span>
            ) : (
              'Encrypt & Save'
            )}
          </button>
        </div>
      </div>
    );
  }

  return null;
}
