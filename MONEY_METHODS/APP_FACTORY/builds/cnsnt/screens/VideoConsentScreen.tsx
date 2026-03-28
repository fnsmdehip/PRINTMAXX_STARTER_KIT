/**
 * VideoConsentScreen - Record video consent with timestamp and GPS.
 *
 * Features:
 * - expo-camera for video recording (front + rear toggle)
 * - Live timestamp overlay
 * - GPS coordinates captured at start via expo-location
 * - Both party names displayed at top
 * - Max 5 minute recording
 * - After recording: preview, retake, or save
 * - On save: encrypt video with vault's AES-256 encryption
 * - Store encrypted video reference alongside consent record
 * - Premium-only: checks entitlement before allowing recording
 */

import React, { useState, useRef, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Pressable,
  Alert,
  Animated,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { CameraView, useCameraPermissions, useMicrophonePermissions } from 'expo-camera';
import * as Location from 'expo-location';
import * as FileSystem from 'expo-file-system';
import { Ionicons } from '@expo/vector-icons';
import ErrorBoundary from '../components/ErrorBoundary';
import PaywallGate from '../components/PaywallGate';
import usePurchases from '../hooks/usePurchases';
import vault from '../services/encryption';
import { Colors, Typography, Spacing, BorderRadius, Shadows } from '../constants/theme';

const MAX_DURATION_SECONDS = 300; // 5 minutes

interface VideoConsentScreenProps {
  navigation: {
    goBack: () => void;
    navigate: (screen: string, params?: any) => void;
  };
  route: {
    params?: {
      consentId?: string;
      partyA?: string;
      partyB?: string;
    };
  };
}

const VideoConsentScreen: React.FC<VideoConsentScreenProps> = ({ navigation, route }) => {
  const { canRecord } = usePurchases();
  const [cameraPermission, requestCameraPermission] = useCameraPermissions();
  const [micPermission, requestMicPermission] = useMicrophonePermissions();

  const [isRecording, setIsRecording] = useState(false);
  const [videoUri, setVideoUri] = useState<string | null>(null);
  const [duration, setDuration] = useState(0);
  const [facing, setFacing] = useState<'front' | 'back'>('front');
  const [gpsCoords, setGpsCoords] = useState<{ lat: number; lng: number } | null>(null);
  const [startTimestamp, setStartTimestamp] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const cameraRef = useRef<CameraView>(null);
  const durationTimer = useRef<ReturnType<typeof setInterval> | null>(null);
  const pulseAnim = useRef(new Animated.Value(1)).current;

  const partyA = route.params?.partyA || 'Party A';
  const partyB = route.params?.partyB || 'Party B';
  const consentId = route.params?.consentId;

  // Request permissions on mount
  useEffect(() => {
    (async () => {
      if (!cameraPermission?.granted) {
        await requestCameraPermission();
      }
      if (!micPermission?.granted) {
        await requestMicPermission();
      }
    })();

    return () => {
      if (durationTimer.current) clearInterval(durationTimer.current);
    };
  }, []);

  // Pulse animation while recording
  useEffect(() => {
    if (isRecording) {
      const pulse = Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, {
            toValue: 1.2,
            duration: 600,
            useNativeDriver: true,
          }),
          Animated.timing(pulseAnim, {
            toValue: 1,
            duration: 600,
            useNativeDriver: true,
          }),
        ])
      );
      pulse.start();
      return () => pulse.stop();
    } else {
      pulseAnim.setValue(1);
    }
  }, [isRecording]);

  const formatDuration = (seconds: number): string => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  const formatTimestamp = (): string => {
    const now = new Date();
    return now.toISOString().replace('T', ' ').substring(0, 19) + ' UTC';
  };

  const captureGPS = async () => {
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        Alert.alert('GPS Permission', 'Location access is needed to stamp consent recordings with GPS coordinates.');
        return null;
      }
      const location = await Location.getCurrentPositionAsync({
        accuracy: Location.Accuracy.High,
      });
      return {
        lat: Math.round(location.coords.latitude * 1000000) / 1000000,
        lng: Math.round(location.coords.longitude * 1000000) / 1000000,
      };
    } catch {
      return null;
    }
  };

  const startRecording = async () => {
    if (!cameraRef.current) return;

    const coords = await captureGPS();
    setGpsCoords(coords);
    setStartTimestamp(formatTimestamp());
    setDuration(0);

    try {
      const video = await cameraRef.current.recordAsync({
        maxDuration: MAX_DURATION_SECONDS,
      });

      if (video?.uri) {
        setVideoUri(video.uri);
      }
    } catch (err) {
      Alert.alert('Recording Error', 'Failed to start video recording. Please try again.');
    }

    setIsRecording(false);
    if (durationTimer.current) clearInterval(durationTimer.current);
  };

  const handleStartRecording = async () => {
    setIsRecording(true);
    setVideoUri(null);

    durationTimer.current = setInterval(() => {
      setDuration((prev) => {
        if (prev >= MAX_DURATION_SECONDS - 1) {
          stopRecording();
          return MAX_DURATION_SECONDS;
        }
        return prev + 1;
      });
    }, 1000);

    await startRecording();
  };

  const stopRecording = useCallback(() => {
    if (cameraRef.current && isRecording) {
      cameraRef.current.stopRecording();
    }
    if (durationTimer.current) {
      clearInterval(durationTimer.current);
      durationTimer.current = null;
    }
    setIsRecording(false);
  }, [isRecording]);

  const handleRetake = () => {
    setVideoUri(null);
    setDuration(0);
    setGpsCoords(null);
    setStartTimestamp(null);
  };

  const handleSave = async () => {
    if (!videoUri) return;

    setSaving(true);
    try {
      // Read the video file as base64
      const videoBase64 = await FileSystem.readAsStringAsync(videoUri, {
        encoding: FileSystem.EncodingType.Base64,
      });

      // Encrypt the video data using the vault
      const encryptedVideo = await vault.encrypt(videoBase64);

      // Create metadata
      const metadata = {
        type: 'video_consent',
        consentId: consentId || `vc_${Date.now()}`,
        partyA,
        partyB,
        timestamp: startTimestamp,
        gps: gpsCoords,
        durationSeconds: duration,
        encryptedAt: new Date().toISOString(),
      };

      // Store encrypted video
      const videoId = `video_${Date.now()}`;
      const videoDir = `${FileSystem.documentDirectory}cnsnt_videos/`;
      await FileSystem.makeDirectoryAsync(videoDir, { intermediates: true });
      await FileSystem.writeAsStringAsync(`${videoDir}${videoId}.enc`, encryptedVideo);

      // Store metadata
      const metaEncrypted = await vault.encrypt(JSON.stringify(metadata));
      await FileSystem.writeAsStringAsync(`${videoDir}${videoId}.meta.enc`, metaEncrypted);

      // Clean up temp video
      await FileSystem.deleteAsync(videoUri, { idempotent: true });

      Alert.alert(
        'Saved',
        'Video consent recording encrypted and saved.',
        [{ text: 'OK', onPress: () => navigation.goBack() }]
      );
    } catch (err) {
      Alert.alert('Save Error', 'Failed to encrypt and save the video. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const toggleFacing = () => {
    setFacing((prev) => (prev === 'front' ? 'back' : 'front'));
  };

  // Entitlement check
  if (!canRecord) {
    return (
      <SafeAreaView style={s.container}>
        <PaywallGate feature="video_recording" />
      </SafeAreaView>
    );
  }

  // Permission check
  if (!cameraPermission?.granted || !micPermission?.granted) {
    return (
      <SafeAreaView style={s.container}>
        <View style={s.permissionContainer}>
          <Ionicons name="videocam-off-outline" size={64} color={Colors.textSecondary} />
          <Text style={s.permissionTitle}>Camera & Microphone Required</Text>
          <Text style={s.permissionDesc}>
            Video consent recording needs camera and microphone access to capture both parties and their verbal agreement.
          </Text>
          <Pressable
            style={s.permissionBtn}
            onPress={async () => {
              await requestCameraPermission();
              await requestMicPermission();
            }}
          >
            <Text style={s.permissionBtnText}>Grant Permissions</Text>
          </Pressable>
        </View>
      </SafeAreaView>
    );
  }

  // Preview state (after recording, before saving)
  if (videoUri) {
    return (
      <SafeAreaView style={s.container}>
        <View style={s.previewContainer}>
          <Ionicons name="checkmark-circle" size={72} color={Colors.success} />
          <Text style={s.previewTitle}>Recording Complete</Text>
          <Text style={s.previewDuration}>{formatDuration(duration)}</Text>

          <View style={s.metadataCard}>
            <Text style={s.metadataLabel}>Parties</Text>
            <Text style={s.metadataValue}>{partyA} & {partyB}</Text>
            <Text style={s.metadataLabel}>Recorded At</Text>
            <Text style={s.metadataValue}>{startTimestamp}</Text>
            {gpsCoords && (
              <>
                <Text style={s.metadataLabel}>GPS Coordinates</Text>
                <Text style={s.metadataValue}>{gpsCoords.lat}, {gpsCoords.lng}</Text>
              </>
            )}
          </View>

          <View style={s.previewActions}>
            <Pressable style={s.retakeBtn} onPress={handleRetake}>
              <Ionicons name="refresh-outline" size={20} color={Colors.textPrimary} />
              <Text style={s.retakeBtnText}>Retake</Text>
            </Pressable>
            <Pressable
              style={[s.saveBtn, saving && s.saveBtnDisabled]}
              onPress={handleSave}
              disabled={saving}
            >
              <Ionicons name="lock-closed" size={20} color="#FFF" />
              <Text style={s.saveBtnText}>
                {saving ? 'Encrypting...' : 'Encrypt & Save'}
              </Text>
            </Pressable>
          </View>
        </View>
      </SafeAreaView>
    );
  }

  // Camera / recording state
  return (
    <ErrorBoundary>
      <View style={s.cameraContainer}>
        <CameraView
          ref={cameraRef}
          style={s.camera}
          facing={facing}
          mode="video"
        >
          {/* Top overlay: party names */}
          <View style={s.topOverlay}>
            <SafeAreaView>
              <View style={s.partyRow}>
                <Text style={s.partyName}>{partyA}</Text>
                <Ionicons name="swap-horizontal" size={16} color="rgba(255,255,255,0.6)" />
                <Text style={s.partyName}>{partyB}</Text>
              </View>
            </SafeAreaView>
          </View>

          {/* Timestamp overlay */}
          <View style={s.timestampOverlay}>
            <View style={s.timestampBadge}>
              {isRecording && (
                <Animated.View style={[s.recordDot, { transform: [{ scale: pulseAnim }] }]} />
              )}
              <Text style={s.timestampText}>{formatTimestamp()}</Text>
            </View>
            {gpsCoords && (
              <Text style={s.gpsText}>
                GPS: {gpsCoords.lat}, {gpsCoords.lng}
              </Text>
            )}
          </View>

          {/* Bottom controls */}
          <View style={s.bottomOverlay}>
            <View style={s.controls}>
              {/* Flip camera */}
              <Pressable
                style={s.controlBtn}
                onPress={toggleFacing}
                disabled={isRecording}
              >
                <Ionicons
                  name="camera-reverse-outline"
                  size={28}
                  color={isRecording ? 'rgba(255,255,255,0.3)' : '#FFF'}
                />
              </Pressable>

              {/* Record / Stop */}
              <Pressable
                style={s.recordBtnOuter}
                onPress={isRecording ? stopRecording : handleStartRecording}
              >
                <Animated.View
                  style={[
                    isRecording ? s.stopBtnInner : s.recordBtnInner,
                    isRecording && { transform: [{ scale: pulseAnim }] },
                  ]}
                />
              </Pressable>

              {/* Duration */}
              <View style={s.durationContainer}>
                <Text style={s.durationText}>{formatDuration(duration)}</Text>
                <Text style={s.maxDurationText}>/ {formatDuration(MAX_DURATION_SECONDS)}</Text>
              </View>
            </View>

            {!isRecording && (
              <Text style={s.instructionText}>
                Position both parties in frame, then tap record
              </Text>
            )}
            {isRecording && (
              <Text style={s.recordingText}>
                Recording... tap the square to stop
              </Text>
            )}
          </View>
        </CameraView>
      </View>
    </ErrorBoundary>
  );
};

const s = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  cameraContainer: {
    flex: 1,
    backgroundColor: '#000',
  },
  camera: {
    flex: 1,
  },

  // Top overlay
  topOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    backgroundColor: 'rgba(0,0,0,0.5)',
    paddingBottom: Spacing.sm,
  },
  partyRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: Spacing.md,
    paddingHorizontal: Spacing.lg,
    paddingTop: Spacing.sm,
  },
  partyName: {
    color: '#FFF',
    fontSize: 15,
    fontWeight: '600',
  },

  // Timestamp overlay
  timestampOverlay: {
    position: 'absolute',
    top: Platform.OS === 'ios' ? 100 : 70,
    left: Spacing.lg,
    gap: 4,
  },
  timestampBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.6)',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 6,
    gap: 6,
  },
  recordDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#EF4444',
  },
  timestampText: {
    color: '#FFF',
    fontSize: 12,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    fontWeight: '500',
  },
  gpsText: {
    color: 'rgba(255,255,255,0.7)',
    fontSize: 11,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    backgroundColor: 'rgba(0,0,0,0.5)',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
    alignSelf: 'flex-start',
  },

  // Bottom overlay
  bottomOverlay: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: 'rgba(0,0,0,0.6)',
    paddingTop: Spacing.lg,
    paddingBottom: Platform.OS === 'ios' ? 48 : 24,
    alignItems: 'center',
  },
  controls: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 40,
  },
  controlBtn: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: 'rgba(255,255,255,0.15)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  recordBtnOuter: {
    width: 72,
    height: 72,
    borderRadius: 36,
    borderWidth: 4,
    borderColor: '#FFF',
    justifyContent: 'center',
    alignItems: 'center',
  },
  recordBtnInner: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: '#EF4444',
  },
  stopBtnInner: {
    width: 28,
    height: 28,
    borderRadius: 4,
    backgroundColor: '#EF4444',
  },
  durationContainer: {
    width: 48,
    alignItems: 'center',
  },
  durationText: {
    color: '#FFF',
    fontSize: 15,
    fontWeight: '700',
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  maxDurationText: {
    color: 'rgba(255,255,255,0.4)',
    fontSize: 10,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  instructionText: {
    color: 'rgba(255,255,255,0.7)',
    fontSize: 13,
    marginTop: Spacing.md,
    textAlign: 'center',
  },
  recordingText: {
    color: '#EF4444',
    fontSize: 13,
    fontWeight: '600',
    marginTop: Spacing.md,
    textAlign: 'center',
  },

  // Permission screen
  permissionContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: Spacing.xxl,
    gap: Spacing.lg,
  },
  permissionTitle: {
    ...Typography.h2,
    color: Colors.textPrimary,
    textAlign: 'center',
  },
  permissionDesc: {
    ...Typography.body,
    color: Colors.textSecondary,
    textAlign: 'center',
    lineHeight: 24,
  },
  permissionBtn: {
    backgroundColor: Colors.primary,
    paddingHorizontal: 32,
    paddingVertical: 14,
    borderRadius: BorderRadius.lg,
    marginTop: Spacing.lg,
  },
  permissionBtnText: {
    color: '#FFF',
    fontSize: 17,
    fontWeight: '600',
  },

  // Preview screen
  previewContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: Spacing.xxl,
    gap: Spacing.lg,
  },
  previewTitle: {
    ...Typography.h1,
    color: Colors.textPrimary,
  },
  previewDuration: {
    fontSize: 36,
    fontWeight: '200',
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    color: Colors.textPrimary,
    letterSpacing: 2,
  },
  metadataCard: {
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    padding: Spacing.xl,
    width: '100%',
    ...Shadows.md,
    borderWidth: 1,
    borderColor: Colors.border,
    gap: 4,
  },
  metadataLabel: {
    fontSize: 11,
    fontWeight: '600',
    color: Colors.textTertiary,
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginTop: Spacing.sm,
  },
  metadataValue: {
    ...Typography.body,
    color: Colors.textPrimary,
    fontWeight: '500',
  },
  previewActions: {
    flexDirection: 'row',
    gap: Spacing.md,
    width: '100%',
    marginTop: Spacing.lg,
  },
  retakeBtn: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 14,
    borderRadius: BorderRadius.lg,
    backgroundColor: Colors.surfaceElevated,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  retakeBtnText: {
    ...Typography.button,
    color: Colors.textPrimary,
  },
  saveBtn: {
    flex: 2,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 14,
    borderRadius: BorderRadius.lg,
    backgroundColor: Colors.primary,
  },
  saveBtnDisabled: {
    opacity: 0.6,
  },
  saveBtnText: {
    ...Typography.button,
    color: '#FFF',
  },
});

export default VideoConsentScreen;
