/**
 * cnsnt Sound Engine
 *
 * Provides UI sound effects. Uses expo-av.
 * Sound assets are .wav files shared from the TruthScope asset library.
 *
 * Sound categories:
 *   UI     -- button taps, toggles, swipes
 *   Action -- signature capture, record start/stop, save complete
 *   System -- permission granted, error, success, premium unlock
 */

import { Audio } from 'expo-av';

export type SoundName =
  | 'tap'
  | 'tapHeavy'
  | 'toggle'
  | 'swipe'
  | 'success'
  | 'error'
  | 'permissionGranted'
  | 'premium'
  | 'analyzeStart'
  | 'analyzeComplete'
  | 'scanLock';

const SOUND_MAP: Record<SoundName, any> = {
  tap: require('../assets/sounds/tap.wav'),
  tapHeavy: require('../assets/sounds/tap_heavy.wav'),
  toggle: require('../assets/sounds/toggle.wav'),
  swipe: require('../assets/sounds/swipe.wav'),
  success: require('../assets/sounds/success.wav'),
  error: require('../assets/sounds/error.wav'),
  permissionGranted: require('../assets/sounds/permission_granted.wav'),
  premium: require('../assets/sounds/premium.wav'),
  analyzeStart: require('../assets/sounds/analyze_start.wav'),
  analyzeComplete: require('../assets/sounds/analyze_complete.wav'),
  scanLock: require('../assets/sounds/scan_lock.wav'),
};

const soundCache: Map<SoundName, Audio.Sound> = new Map();
let isInitialized = false;
let isMuted = false;
let masterVolume = 0.7;

export async function initSounds(): Promise<void> {
  if (isInitialized) return;
  try {
    await Audio.setAudioModeAsync({
      playsInSilentModeIOS: true,
      staysActiveInBackground: false,
      shouldDuckAndroid: true,
    });
    const preloadList: SoundName[] = ['tap', 'success', 'error', 'toggle'];
    await Promise.all(
      preloadList.map(async (name) => {
        try {
          const { sound } = await Audio.Sound.createAsync(SOUND_MAP[name], {
            shouldPlay: false,
            volume: masterVolume,
          });
          soundCache.set(name, sound);
        } catch {
          // Non-critical
        }
      })
    );
    isInitialized = true;
  } catch {
    // Sound engine init failed silently
  }
}

export async function playSound(
  name: SoundName,
  options?: { volume?: number }
): Promise<void> {
  if (isMuted) return;
  const volume = (options?.volume ?? 1) * masterVolume;
  try {
    const sound = soundCache.get(name);
    if (sound) {
      await sound.setPositionAsync(0);
      await sound.setVolumeAsync(volume);
      await sound.playAsync();
    } else {
      const { sound: newSound } = await Audio.Sound.createAsync(
        SOUND_MAP[name],
        { shouldPlay: true, volume }
      );
      soundCache.set(name, newSound);
    }
  } catch {
    // Sound playback is never critical
  }
}

export function setMuted(muted: boolean): void {
  isMuted = muted;
}

export function setVolume(volume: number): void {
  masterVolume = Math.max(0, Math.min(1, volume));
}

export function getMuted(): boolean {
  return isMuted;
}

export async function cleanupSounds(): Promise<void> {
  for (const [, sound] of soundCache) {
    try {
      await sound.unloadAsync();
    } catch {}
  }
  soundCache.clear();
  isInitialized = false;
}
