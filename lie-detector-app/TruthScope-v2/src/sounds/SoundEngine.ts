/**
 * TruthScope v2 Sound Engine
 *
 * Professional sound effects for the entire app. Uses expo-av for playback.
 * All sounds are .wav files from professional CC0/CC-BY libraries (Octave, Kenney).
 */

import { Audio } from 'expo-av';

export type SoundName =
  | 'tap'
  | 'tapHeavy'
  | 'toggle'
  | 'swipe'
  | 'heartbeat'
  | 'scanStart'
  | 'scanPulse'
  | 'scanLock'
  | 'verdictTruth'
  | 'verdictDeception'
  | 'verdictUncertain'
  | 'countdown'
  | 'playerSwitch'
  | 'roundComplete'
  | 'analyzeStart'
  | 'analyzeComplete'
  | 'calibrateStart'
  | 'calibrateDone'
  | 'permissionGranted'
  | 'error'
  | 'success'
  | 'premium';

const SOUND_MAP: Record<SoundName, any> = {
  tap: require('../../assets/sounds/tap.wav'),
  tapHeavy: require('../../assets/sounds/tap_heavy.wav'),
  toggle: require('../../assets/sounds/toggle.wav'),
  swipe: require('../../assets/sounds/swipe.wav'),
  heartbeat: require('../../assets/sounds/heartbeat.wav'),
  scanStart: require('../../assets/sounds/scan_start.wav'),
  scanPulse: require('../../assets/sounds/scan_pulse.wav'),
  scanLock: require('../../assets/sounds/scan_lock.wav'),
  verdictTruth: require('../../assets/sounds/verdict_truth.wav'),
  verdictDeception: require('../../assets/sounds/verdict_deception.wav'),
  verdictUncertain: require('../../assets/sounds/verdict_uncertain.wav'),
  countdown: require('../../assets/sounds/countdown.wav'),
  playerSwitch: require('../../assets/sounds/player_switch.wav'),
  roundComplete: require('../../assets/sounds/round_complete.wav'),
  analyzeStart: require('../../assets/sounds/analyze_start.wav'),
  analyzeComplete: require('../../assets/sounds/analyze_complete.wav'),
  calibrateStart: require('../../assets/sounds/calibrate_start.wav'),
  calibrateDone: require('../../assets/sounds/calibrate_done.wav'),
  permissionGranted: require('../../assets/sounds/permission_granted.wav'),
  error: require('../../assets/sounds/error.wav'),
  success: require('../../assets/sounds/success.wav'),
  premium: require('../../assets/sounds/premium.wav'),
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

    const preloadList: SoundName[] = [
      'tap', 'heartbeat', 'scanPulse', 'verdictTruth',
      'verdictDeception', 'countdown', 'analyzeStart',
    ];

    await Promise.all(
      preloadList.map(async (name) => {
        try {
          const { sound } = await Audio.Sound.createAsync(SOUND_MAP[name], {
            shouldPlay: false,
            volume: masterVolume,
          });
          soundCache.set(name, sound);
        } catch (e) {
          // Non-critical: will load on first play
        }
      })
    );

    isInitialized = true;
  } catch (e) {
    console.warn('Sound engine init failed:', e);
  }
}

export async function playSound(
  name: SoundName,
  options?: { volume?: number; rate?: number }
): Promise<void> {
  if (isMuted) return;

  const volume = (options?.volume ?? 1) * masterVolume;

  try {
    let sound = soundCache.get(name);

    if (sound) {
      await sound.setPositionAsync(0);
      await sound.setVolumeAsync(volume);
      if (options?.rate) {
        await sound.setRateAsync(options.rate, true);
      }
      await sound.playAsync();
    } else {
      const { sound: newSound } = await Audio.Sound.createAsync(
        SOUND_MAP[name],
        {
          shouldPlay: true,
          volume,
          rate: options?.rate ?? 1,
        }
      );
      soundCache.set(name, newSound);
    }
  } catch (e) {
    // Sound playback is never critical
  }
}

export function playHeartbeatAtBPM(bpm: number): void {
  const rate = Math.max(0.5, Math.min(2.0, bpm / 72));
  playSound('heartbeat', { rate, volume: 0.5 });
}

export function playVerdictReveal(verdict: 'truthful' | 'deceptive' | 'uncertain'): void {
  switch (verdict) {
    case 'truthful':
      playSound('verdictTruth', { volume: 0.9 });
      break;
    case 'deceptive':
      playSound('verdictDeception', { volume: 1.0 });
      break;
    case 'uncertain':
      playSound('verdictUncertain', { volume: 0.7 });
      break;
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
