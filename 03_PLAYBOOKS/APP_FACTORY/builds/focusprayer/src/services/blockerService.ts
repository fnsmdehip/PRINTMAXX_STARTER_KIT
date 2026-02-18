/**
 * Blocker Service
 * Native app blocking placeholder
 * Requires native module implementation for actual blocking
 */

import { Platform, NativeModules } from 'react-native';
import { AppInfo } from '../types';
import { COMMON_SOCIAL_APPS, COMMON_IOS_APPS } from '../utils/constants';

// Get the native module (will be undefined until native code is added)
const { ScreenTimeManager, AppBlocker } = NativeModules;

// Check if blocking is available on this platform
export function isBlockingSupported(): boolean {
  if (Platform.OS === 'ios') {
    // iOS 15+ required for Screen Time API
    const majorVersion = parseInt(Platform.Version as string, 10);
    return majorVersion >= 15;
  }

  if (Platform.OS === 'android') {
    // Android 5.0+ required for UsageStats
    return Platform.Version >= 21;
  }

  return false;
}

// Request permission to block apps
export async function requestBlockingPermission(): Promise<boolean> {
  if (Platform.OS === 'ios') {
    // TODO: Implement when native module is added
    /*
    try {
      const granted = await ScreenTimeManager.requestAuthorization();
      return granted;
    } catch (error) {
      console.error('Failed to request iOS permission:', error);
      return false;
    }
    */
    console.log('Would request iOS Screen Time authorization');
    return true;
  }

  if (Platform.OS === 'android') {
    // TODO: Implement when native module is added
    /*
    try {
      const granted = await AppBlocker.requestPermissions();
      return granted;
    } catch (error) {
      console.error('Failed to request Android permissions:', error);
      return false;
    }
    */
    console.log('Would request Android UsageStats + Overlay permissions');
    return true;
  }

  return false;
}

// Check if permission is already granted
export async function checkBlockingPermission(): Promise<boolean> {
  if (Platform.OS === 'ios') {
    // TODO: Implement when native module is added
    /*
    try {
      return await ScreenTimeManager.checkAuthorization();
    } catch (error) {
      return false;
    }
    */
    return true;
  }

  if (Platform.OS === 'android') {
    // TODO: Implement when native module is added
    /*
    try {
      return await AppBlocker.checkPermissions();
    } catch (error) {
      return false;
    }
    */
    return true;
  }

  return false;
}

// Get list of installed apps that can be blocked
export async function getBlockableApps(): Promise<AppInfo[]> {
  // TODO: Implement native module to get actual installed apps
  /*
  if (Platform.OS === 'ios') {
    try {
      const apps = await ScreenTimeManager.getInstalledApps();
      return apps;
    } catch (error) {
      console.error('Failed to get iOS apps:', error);
    }
  }

  if (Platform.OS === 'android') {
    try {
      const apps = await AppBlocker.getInstalledApps();
      return apps;
    } catch (error) {
      console.error('Failed to get Android apps:', error);
    }
  }
  */

  // Return common apps as placeholder
  const commonApps = Platform.OS === 'ios' ? COMMON_IOS_APPS : COMMON_SOCIAL_APPS;

  return commonApps.map((app) => ({
    ...app,
    isBlocked: false,
  }));
}

// Enable blocking for selected apps
export async function enableBlocking(packageNames: string[]): Promise<boolean> {
  if (Platform.OS === 'ios') {
    // TODO: Implement when native module is added
    /*
    try {
      await ScreenTimeManager.blockApps(packageNames);
      return true;
    } catch (error) {
      console.error('Failed to block iOS apps:', error);
      return false;
    }
    */
    console.log('Would block iOS apps:', packageNames);
    return true;
  }

  if (Platform.OS === 'android') {
    // TODO: Implement when native module is added
    /*
    try {
      await AppBlocker.blockApps(packageNames);
      return true;
    } catch (error) {
      console.error('Failed to block Android apps:', error);
      return false;
    }
    */
    console.log('Would block Android apps:', packageNames);
    return true;
  }

  return false;
}

// Disable all blocking
export async function disableBlocking(): Promise<boolean> {
  if (Platform.OS === 'ios') {
    // TODO: Implement when native module is added
    /*
    try {
      await ScreenTimeManager.unblockApps();
      return true;
    } catch (error) {
      console.error('Failed to unblock iOS apps:', error);
      return false;
    }
    */
    console.log('Would unblock all iOS apps');
    return true;
  }

  if (Platform.OS === 'android') {
    // TODO: Implement when native module is added
    /*
    try {
      await AppBlocker.unblockApps();
      return true;
    } catch (error) {
      console.error('Failed to unblock Android apps:', error);
      return false;
    }
    */
    console.log('Would unblock all Android apps');
    return true;
  }

  return false;
}

// Check if apps are currently blocked
export async function isBlockingActive(): Promise<boolean> {
  // TODO: Implement when native modules are added
  return false;
}

// Get blocking status message for display
export function getBlockingStatusMessage(
  isBlocking: boolean,
  blockedCount: number
): string {
  if (!isBlocking) {
    return 'Apps unlocked';
  }

  if (blockedCount === 0) {
    return 'No apps selected for blocking';
  }

  if (blockedCount === 1) {
    return '1 app blocked until devotion complete';
  }

  return `${blockedCount} apps blocked until devotion complete`;
}
