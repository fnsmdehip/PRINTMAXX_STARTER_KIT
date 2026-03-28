import { useState, useEffect } from 'react';
import { decrypt } from '../crypto/vault';
import { verifyHmac, computeChainHash } from '../crypto/hmac';
import { getVideo, addAuditEntry, getLastAuditHash } from '../db/store';
import type { ViewName, VideoConsentRecord } from '../types';

interface VideoPlayerProps {
  videoId: string;
  pin: string;
  navigate: (view: ViewName) => void;
}

export default function VideoPlayer({ videoId, pin, navigate }: VideoPlayerProps) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [metadata, setMetadata] = useState<VideoConsentRecord | null>(null);
  const [integrityOk, setIntegrityOk] = useState<boolean | null>(null);

  useEffect(() => {
    loadAndDecrypt();
    return () => {
      if (videoUrl) URL.revokeObjectURL(videoUrl);
    };
  }, [videoId]); // eslint-disable-line react-hooks/exhaustive-deps

  const loadAndDecrypt = async () => {
    setLoading(true);
    setError('');

    try {
      const stored = await getVideo(videoId);
      if (!stored) {
        setError('Video not found.');
        setLoading(false);
        return;
      }

      // Verify HMAC integrity
      const valid = await verifyHmac(stored.encryptedBlob, stored.hmac);
      setIntegrityOk(valid);

      // Decrypt metadata
      const metaJson = await decrypt(stored.encryptedMeta, stored.metaIv, stored.metaSalt, pin);
      const meta = JSON.parse(metaJson) as VideoConsentRecord;
      setMetadata(meta);

      // Decrypt video
      const videoBase64 = await decrypt(stored.encryptedBlob, stored.iv, stored.salt, pin);

      // Convert base64 back to blob
      const binary = atob(videoBase64);
      const bytes = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i++) {
        bytes[i] = binary.charCodeAt(i);
      }
      const blob = new Blob([bytes], { type: 'video/webm' });
      const url = URL.createObjectURL(blob);
      setVideoUrl(url);

      // Audit: video viewed
      const prevHash = await getLastAuditHash();
      const content = `video_viewed|${videoId}|${new Date().toISOString()}`;
      const hash = await computeChainHash(content, prevHash);
      await addAuditEntry({
        id: crypto.randomUUID(),
        action: 'video_viewed',
        recordId: videoId,
        timestamp: new Date().toISOString(),
        details: `Viewed video: ${stored.title}`,
        prevHash,
        hash,
      });
    } catch (err) {
      setError('Failed to decrypt video. Your PIN may have changed since this recording.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    if (!videoUrl || !metadata) return;

    try {
      // Download the decrypted video
      const a = document.createElement('a');
      a.href = videoUrl;
      a.download = `cnsnt-video-${metadata.partyA}-${metadata.partyB}-${new Date().toISOString().split('T')[0]}.webm`;
      a.click();

      // Audit: video exported
      const prevHash = await getLastAuditHash();
      const content = `video_exported|${videoId}|${new Date().toISOString()}`;
      const hash = await computeChainHash(content, prevHash);
      await addAuditEntry({
        id: crypto.randomUUID(),
        action: 'video_exported',
        recordId: videoId,
        timestamp: new Date().toISOString(),
        details: `Exported video: ${metadata.partyA} & ${metadata.partyB}`,
        prevHash,
        hash,
      });
    } catch {
      setError('Failed to export video.');
    }
  };

  const formatDuration = (seconds: number): string => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <div className="w-8 h-8 border-2 border-coral border-t-transparent rounded-full animate-spin" />
        <p className="text-gray-400 text-sm">Decrypting video...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 max-w-2xl mx-auto text-center py-16">
        <svg className="w-12 h-12 text-red-400 mx-auto mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
        <p className="text-red-400 text-lg">{error}</p>
        <button
          onClick={() => navigate('dashboard')}
          className="mt-4 px-6 py-3 bg-navy-light border border-gray-700 rounded-xl text-white"
        >
          Back to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-6 max-w-2xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <button onClick={() => navigate('dashboard')} className="text-gray-400 flex items-center gap-1">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back
        </button>
        <button
          onClick={handleExport}
          className="px-4 py-2 bg-ocean text-white rounded-lg text-sm font-medium"
        >
          Export Video
        </button>
      </div>

      {/* Integrity badge */}
      {integrityOk !== null && (
        <div className={`mb-4 p-3 rounded-xl flex items-center gap-2 ${
          integrityOk
            ? 'bg-green-900/20 border border-green-800/30'
            : 'bg-red-900/20 border border-red-800/30'
        }`}>
          <svg className={`w-5 h-5 ${integrityOk ? 'text-green-400' : 'text-red-400'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
            {integrityOk ? (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            ) : (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.834-1.964-.834-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
            )}
          </svg>
          <span className={`text-sm font-medium ${integrityOk ? 'text-green-400' : 'text-red-400'}`}>
            {integrityOk ? 'Integrity verified (HMAC-SHA-256)' : 'Integrity check FAILED - video may be tampered'}
          </span>
        </div>
      )}

      {/* Video player */}
      {videoUrl && (
        <div className="rounded-xl overflow-hidden mb-4 bg-black">
          <video
            src={videoUrl}
            controls
            playsInline
            className="w-full max-h-[50vh]"
          />
        </div>
      )}

      {/* Metadata */}
      {metadata && (
        <div className="bg-navy-light border border-gray-700 rounded-xl p-5 space-y-3">
          <h3 className="text-coral text-xs font-semibold uppercase tracking-wide mb-2">Recording Details</h3>
          <div className="flex justify-between">
            <span className="text-gray-400 text-sm">Parties</span>
            <span className="text-white text-sm font-medium">{metadata.partyA} & {metadata.partyB}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400 text-sm">Recorded</span>
            <span className="text-white text-sm font-mono">{metadata.timestamp}</span>
          </div>
          {metadata.gps && (
            <div className="flex justify-between">
              <span className="text-gray-400 text-sm">GPS</span>
              <span className="text-white text-sm font-mono">{metadata.gps.latitude}, {metadata.gps.longitude}</span>
            </div>
          )}
          <div className="flex justify-between">
            <span className="text-gray-400 text-sm">Duration</span>
            <span className="text-white text-sm font-mono">{formatDuration(metadata.durationSeconds)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400 text-sm">Encrypted</span>
            <span className="text-white text-sm font-mono">{metadata.encryptedAt?.split('T')[0] || 'N/A'}</span>
          </div>
        </div>
      )}

      {/* Crypto footer */}
      <div className="mt-4 bg-navy-light border border-gray-700 rounded-xl p-3 text-center">
        <p className="text-gray-500 text-xs">
          Encrypted with AES-256-GCM | Integrity: HMAC-SHA-256 | Video ID: {videoId.slice(0, 8)}...
        </p>
      </div>
    </div>
  );
}
