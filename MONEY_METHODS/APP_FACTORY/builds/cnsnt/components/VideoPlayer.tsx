/**
 * VideoPlayer - Decrypted video playback for saved video consent records.
 *
 * Features:
 * - Decrypts encrypted video file from vault storage
 * - Plays back with expo-av Video component
 * - Shows timestamp and GPS overlay
 * - Export option via share sheet (decrypts then shares)
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Pressable,
  Alert,
  ActivityIndicator,
  Platform,
} from 'react-native';
import { Video, ResizeMode } from 'expo-av';
import * as FileSystem from 'expo-file-system';
import * as Sharing from 'expo-sharing';
import { Ionicons } from '@expo/vector-icons';
import vault from '../services/encryption';
import { Colors, Typography, Spacing, BorderRadius, Shadows } from '../constants/theme';

interface VideoPlayerProps {
  videoId: string;
  onClose?: () => void;
}

interface VideoMetadata {
  type: string;
  consentId: string;
  partyA: string;
  partyB: string;
  timestamp: string;
  gps: { lat: number; lng: number } | null;
  durationSeconds: number;
  encryptedAt: string;
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ videoId, onClose }) => {
  const [loading, setLoading] = useState(true);
  const [decryptedUri, setDecryptedUri] = useState<string | null>(null);
  const [metadata, setMetadata] = useState<VideoMetadata | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showOverlay, setShowOverlay] = useState(true);
  const videoRef = useRef<Video>(null);

  useEffect(() => {
    decryptVideo();
    return () => {
      // Clean up decrypted temp file
      if (decryptedUri) {
        FileSystem.deleteAsync(decryptedUri, { idempotent: true });
      }
    };
  }, [videoId]);

  const decryptVideo = async () => {
    setLoading(true);
    setError(null);

    try {
      const videoDir = `${FileSystem.documentDirectory}cnsnt_videos/`;

      // Decrypt metadata
      const metaEncrypted = await FileSystem.readAsStringAsync(
        `${videoDir}${videoId}.meta.enc`
      );
      const metaJson = await vault.decrypt(metaEncrypted);
      const meta: VideoMetadata = JSON.parse(metaJson);
      setMetadata(meta);

      // Decrypt video
      const videoEncrypted = await FileSystem.readAsStringAsync(
        `${videoDir}${videoId}.enc`
      );
      const videoBase64 = await vault.decrypt(videoEncrypted);

      // Write decrypted video to temp file
      const tempUri = `${FileSystem.cacheDirectory}cnsnt_temp_${Date.now()}.mp4`;
      await FileSystem.writeAsStringAsync(tempUri, videoBase64, {
        encoding: FileSystem.EncodingType.Base64,
      });

      setDecryptedUri(tempUri);
    } catch (err) {
      setError('Failed to decrypt video. Your PIN may have changed since this recording.');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    if (!decryptedUri) return;

    const canShare = await Sharing.isAvailableAsync();
    if (!canShare) {
      Alert.alert('Sharing Unavailable', 'Sharing is not available on this device.');
      return;
    }

    try {
      await Sharing.shareAsync(decryptedUri, {
        mimeType: 'video/mp4',
        dialogTitle: 'Export Video Consent Recording',
        UTI: 'public.mpeg-4',
      });
    } catch {
      Alert.alert('Export Error', 'Failed to export the video.');
    }
  };

  if (loading) {
    return (
      <View style={s.container}>
        <View style={s.loadingContainer}>
          <ActivityIndicator size="large" color={Colors.primary} />
          <Text style={s.loadingText}>Decrypting video...</Text>
        </View>
      </View>
    );
  }

  if (error) {
    return (
      <View style={s.container}>
        <View style={s.errorContainer}>
          <Ionicons name="lock-closed" size={48} color={Colors.error} />
          <Text style={s.errorText}>{error}</Text>
          <Pressable style={s.retryBtn} onPress={decryptVideo}>
            <Text style={s.retryBtnText}>Retry</Text>
          </Pressable>
          {onClose && (
            <Pressable style={s.closeBtn} onPress={onClose}>
              <Text style={s.closeBtnText}>Close</Text>
            </Pressable>
          )}
        </View>
      </View>
    );
  }

  return (
    <View style={s.container}>
      {/* Video */}
      {decryptedUri && (
        <Pressable style={s.videoWrapper} onPress={() => setShowOverlay(!showOverlay)}>
          <Video
            ref={videoRef}
            source={{ uri: decryptedUri }}
            style={s.video}
            resizeMode={ResizeMode.CONTAIN}
            useNativeControls
            shouldPlay={false}
          />

          {/* Metadata overlay */}
          {showOverlay && metadata && (
            <View style={s.overlay}>
              <View style={s.overlayBadge}>
                <Text style={s.overlayTimestamp}>{metadata.timestamp}</Text>
              </View>
              {metadata.gps && (
                <View style={s.overlayBadge}>
                  <Ionicons name="location" size={12} color="#FFF" />
                  <Text style={s.overlayGps}>
                    {metadata.gps.lat}, {metadata.gps.lng}
                  </Text>
                </View>
              )}
            </View>
          )}
        </Pressable>
      )}

      {/* Metadata card */}
      {metadata && (
        <View style={s.metadataCard}>
          <View style={s.metaRow}>
            <Text style={s.metaLabel}>Parties</Text>
            <Text style={s.metaValue}>{metadata.partyA} & {metadata.partyB}</Text>
          </View>
          <View style={s.metaRow}>
            <Text style={s.metaLabel}>Recorded</Text>
            <Text style={s.metaValue}>{metadata.timestamp}</Text>
          </View>
          {metadata.gps && (
            <View style={s.metaRow}>
              <Text style={s.metaLabel}>Location</Text>
              <Text style={s.metaValue}>{metadata.gps.lat}, {metadata.gps.lng}</Text>
            </View>
          )}
          <View style={s.metaRow}>
            <Text style={s.metaLabel}>Duration</Text>
            <Text style={s.metaValue}>
              {Math.floor(metadata.durationSeconds / 60)}:{(metadata.durationSeconds % 60).toString().padStart(2, '0')}
            </Text>
          </View>
        </View>
      )}

      {/* Actions */}
      <View style={s.actions}>
        <Pressable style={s.exportBtn} onPress={handleExport}>
          <Ionicons name="share-outline" size={20} color="#FFF" />
          <Text style={s.exportBtnText}>Export Video</Text>
        </Pressable>
        {onClose && (
          <Pressable style={s.dismissBtn} onPress={onClose}>
            <Text style={s.dismissBtnText}>Close</Text>
          </Pressable>
        )}
      </View>
    </View>
  );
};

const s = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    gap: Spacing.lg,
  },
  loadingText: {
    ...Typography.body,
    color: Colors.textSecondary,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: Spacing.xxl,
    gap: Spacing.lg,
  },
  errorText: {
    ...Typography.body,
    color: Colors.textSecondary,
    textAlign: 'center',
  },
  retryBtn: {
    backgroundColor: Colors.primary,
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: BorderRadius.md,
  },
  retryBtnText: {
    color: '#FFF',
    fontWeight: '600',
    fontSize: 15,
  },
  closeBtn: {
    paddingHorizontal: 24,
    paddingVertical: 12,
  },
  closeBtnText: {
    color: Colors.textSecondary,
    fontSize: 15,
  },

  // Video
  videoWrapper: {
    width: '100%',
    aspectRatio: 16 / 9,
    backgroundColor: '#000',
    position: 'relative',
  },
  video: {
    width: '100%',
    height: '100%',
  },

  // Overlay
  overlay: {
    position: 'absolute',
    top: Spacing.md,
    left: Spacing.md,
    gap: 4,
  },
  overlayBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: 'rgba(0,0,0,0.6)',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 4,
    alignSelf: 'flex-start',
  },
  overlayTimestamp: {
    color: '#FFF',
    fontSize: 11,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  overlayGps: {
    color: '#FFF',
    fontSize: 10,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },

  // Metadata card
  metadataCard: {
    margin: Spacing.lg,
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    padding: Spacing.lg,
    ...Shadows.sm,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  metaRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: Spacing.sm,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: Colors.divider,
  },
  metaLabel: {
    fontSize: 13,
    fontWeight: '500',
    color: Colors.textTertiary,
  },
  metaValue: {
    fontSize: 14,
    fontWeight: '600',
    color: Colors.textPrimary,
  },

  // Actions
  actions: {
    padding: Spacing.lg,
    gap: Spacing.md,
  },
  exportBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: Colors.primary,
    paddingVertical: 14,
    borderRadius: BorderRadius.lg,
  },
  exportBtnText: {
    color: '#FFF',
    fontSize: 17,
    fontWeight: '600',
  },
  dismissBtn: {
    alignItems: 'center',
    paddingVertical: 12,
  },
  dismissBtnText: {
    color: Colors.textSecondary,
    fontSize: 15,
  },
});

export default VideoPlayer;
