/**
 * TruthScope Sound Engine
 *
 * Provides sound effects for the entire app. Uses expo-av for playback.
 * Sound assets are .wav files generated at build time (pure tones, no licensing).
 *
 * Sound categories:
 *   UI      — button taps, navigation, toggles
 *   Scan    — heartbeat pulse, scanning sweep, signal lock
 *   Verdict — truth reveal, deception reveal, uncertain
 *   Party   — countdown, player switch, round complete
 *   System  — calibration, permission granted, error
 */

import { Audio } from 'expo-av';

type SoundName =
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

// Map sound names to asset requires
// Using require() so Metro bundles them at build time
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

// Preloaded sound objects for instant playback
const soundCache: Map<SoundName, Audio.Sound> = new Map();

let isInitialized = false;
let isMuted = false;
let masterVolume = 0.7;

/**
 * Initialize the sound engine. Call once at app start.
 * Preloads the most-used sounds for zero-latency playback.
 */
export async function initSounds(): Promise<void> {
  if (isInitialized) return;

  try {
    await Audio.setAudioModeAsync({
      playsInSilentModeIOS: false, // Respect silent switch
      staysActiveInBackground: false,
      shouldDuckAndroid: true,
    });

    // Preload frequently-used sounds
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
          // Non-critical: sound will load on first play instead
        }
      })
    );

    isInitialized = true;
  } catch (e) {
    console.warn('Sound engine init failed:', e);
  }
}

/**
 * Play a sound effect. Non-blocking, fire-and-forget.
 * If the sound isn't preloaded, loads it on demand.
 */
export async function playSound(
  name: SoundName,
  options?: { volume?: number; rate?: number }
): Promise<void> {
  if (isMuted) return;

  const volume = (options?.volume ?? 1) * masterVolume;

  try {
    // Try cached sound first (instant playback)
    let sound = soundCache.get(name);

    if (sound) {
      await sound.setPositionAsync(0);
      await sound.setVolumeAsync(volume);
      if (options?.rate) {
        await sound.setRateAsync(options.rate, true);
      }
      await sound.playAsync();
    } else {
      // Load on demand
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
    // Sound playback is never critical, don't crash
  }
}

/**
 * Play heartbeat sound at a rate matching the detected BPM.
 * Creates the illusion of hearing your own heartbeat.
 */
export function playHeartbeatAtBPM(bpm: number): void {
  // Map BPM to playback rate: 72 BPM = normal speed (1.0)
  const rate = Math.max(0.5, Math.min(2.0, bpm / 72));
  playSound('heartbeat', { rate, volume: 0.5 });
}

/**
 * Play the verdict reveal sound with appropriate drama.
 */
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

/**
 * Cleanup all loaded sounds. Call on app unmount.
 */
export async function cleanupSounds(): Promise<void> {
  for (const [, sound] of soundCache) {
    try {
      await sound.unloadAsync();
    } catch {}
  }
  soundCache.clear();
  isInitialized = false;
}
