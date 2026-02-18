import { Platform } from 'react-native';
import { BlockedApp } from '../types';

// Note: App blocking functionality requires native modules that are only available
// in development builds. In Expo Go, we use mock implementations for testing.

export interface BlockerServiceResult {
  success: boolean;
  error?: string;
}

// Track blocking state in memory for Expo Go testing
let mockBlockingEnabled = false;
let mockBlockedApps: string[] = [];

/**
 * Check if app blocking is available on this device
 */
export async function isBlockingAvailable(): Promise<boolean> {
  if (Platform.OS === 'ios') {
    // iOS requires Screen Time API (FamilyControls)
    // Available on iOS 15+
    const version = typeof Platform.Version === 'string' ? parseInt(Platform.Version, 10) : Platform.Version;
    return version >= 15;
  } else {
    // Android requires UsageStats permission
    return true;
  }
}

/**
 * Request blocking permissions
 * In Expo Go, simulates permission grant for testing
 */
export async function requestBlockingPermissions(): Promise<BlockerServiceResult> {
  try {
    console.log('[BlockerService] Requesting blocking permissions (mock in Expo Go)');

    // In Expo Go, we simulate permission being granted
    // Real implementation would use native modules
    return { success: true };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to request permissions',
    };
  }
}

/**
 * Check if blocking permissions are granted
 */
export async function hasBlockingPermissions(): Promise<boolean> {
  try {
    // In Expo Go, always return true for testing
    console.log('[BlockerService] Checking blocking permissions (mock: true)');
    return true;
  } catch {
    return false;
  }
}

/**
 * Block specified apps
 * In Expo Go, stores the state in memory for testing
 */
export async function blockApps(apps: BlockedApp[]): Promise<BlockerServiceResult> {
  try {
    const bundleIds = apps.map((app) => app.bundleId);
    mockBlockedApps = bundleIds;
    mockBlockingEnabled = true;

    console.log(`[BlockerService] Blocked ${bundleIds.length} apps (mock):`, bundleIds);
    return { success: true };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to block apps',
    };
  }
}

/**
 * Unblock all apps
 */
export async function unblockApps(): Promise<BlockerServiceResult> {
  try {
    mockBlockedApps = [];
    mockBlockingEnabled = false;

    console.log('[BlockerService] Unblocked all apps (mock)');
    return { success: true };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to unblock apps',
    };
  }
}

/**
 * Get list of installed apps that can be blocked
 * Returns sample apps for Expo Go testing
 */
export async function getBlockableApps(): Promise<BlockedApp[]> {
  try {
    // Return sample apps for testing in Expo Go
    // Real implementation would query installed apps via native module
    return [
      { id: '1', name: 'TikTok', bundleId: 'com.zhiliaoapp.musically' },
      { id: '2', name: 'Instagram', bundleId: 'com.instagram.android' },
      { id: '3', name: 'Twitter', bundleId: 'com.twitter.android' },
      { id: '4', name: 'YouTube', bundleId: 'com.google.android.youtube' },
      { id: '5', name: 'Facebook', bundleId: 'com.facebook.katana' },
      { id: '6', name: 'Reddit', bundleId: 'com.reddit.frontpage' },
      { id: '7', name: 'Snapchat', bundleId: 'com.snapchat.android' },
      { id: '8', name: 'Discord', bundleId: 'com.discord' },
      { id: '9', name: 'Netflix', bundleId: 'com.netflix.mediaclient' },
      { id: '10', name: 'Twitch', bundleId: 'tv.twitch.android.app' },
    ];
  } catch {
    return [];
  }
}

/**
 * Check if a specific app is currently blocked
 */
export async function isAppBlocked(bundleId: string): Promise<boolean> {
  try {
    return mockBlockedApps.includes(bundleId);
  } catch {
    return false;
  }
}

/**
 * Update blocking state based on step goal status
 */
export async function updateBlockingState(
  isUnlocked: boolean,
  blockedApps: BlockedApp[]
): Promise<BlockerServiceResult> {
  if (isUnlocked) {
    return await unblockApps();
  } else {
    return await blockApps(blockedApps);
  }
}

/**
 * Get current blocking status (for testing)
 */
export function getBlockingStatus(): { enabled: boolean; apps: string[] } {
  return {
    enabled: mockBlockingEnabled,
    apps: mockBlockedApps,
  };
}
