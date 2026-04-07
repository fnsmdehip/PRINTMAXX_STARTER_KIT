/**
 * Scripture Streak Sound Engine
 * Uses expo-av for sound effects. playsInSilentModeIOS: true so sounds work even when phone is muted.
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
  | 'analyzeComplete';

const SOUND_MAP: Record<SoundName, any> = {
  tap: require('../../assets/sounds/tap.wav'),
  tapHeavy: require('../../assets/sounds/tap_heavy.wav'),
  toggle: require('../../assets/sounds/toggle.wav'),
  swipe: require('../../assets/sounds/swipe.wav'),
  success: require('../../assets/sounds/success.wav'),
  error: require('../../assets/sounds/error.wav'),
  permissionGranted: require('../../assets/sounds/permission_granted.wav'),
  premium: require('../../assets/sounds/premium.wav'),
  analyzeComplete: require('../../assets/sounds/analyze_complete.wav'),
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
    const preloadList: SoundName[] = ['tap', 'success', 'toggle'];
    await Promise.all(
      preloadList.map(async (name) => {
        try {
          const { sound } = await Audio.Sound.createAsync(SOUND_MAP[name], {
            shouldPlay: false,
            volume: masterVolume,
          });
          soundCache.set(name, sound);
        } catch {}
      })
    );
    isInitialized = true;
  } catch {}
}

export async function playSound(
  name: SoundName,
  options?: { volume?: number }
): Promise<void> {
  if (isMuted) return;
  const volume = (options?.volume ?? 1) * masterVolume;
  try {
    let sound = soundCache.get(name);
    if (sound) {
      await sound.setPositionAsync(0);
      await sound.setVolumeAsync(volume);
      await sound.playAsync();
    } else {
      const { sound: newSound } = await Audio.Sound.createAsync(SOUND_MAP[name], {
        shouldPlay: true,
        volume,
      });
      soundCache.set(name, newSound);
    }
  } catch {}
}

export function setMuted(muted: boolean): void {
  isMuted = muted;
}

export function getMuted(): boolean {
  return isMuted;
}
