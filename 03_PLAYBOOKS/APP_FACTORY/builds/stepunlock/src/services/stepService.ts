import { Platform } from 'react-native';
import { getStartOfDay, getEndOfDay } from '../utils/dateUtils';

// Note: In Expo managed workflow, HealthKit/Google Fit requires a development build
// with expo-apple-health-kit or react-native-health configured via config plugins.
// For development/testing in Expo Go, we use mock data.

export interface StepServiceResult {
  steps: number;
  error?: string;
}

export interface HealthPermissions {
  granted: boolean;
  error?: string;
}

// Flag to detect if we're in Expo Go (can't use native health modules)
const isExpoGo = (): boolean => {
  try {
    // In Expo Go, native modules won't be available
    // This is a simple check that will be true in Expo Go
    return !global.__turboModuleProxy;
  } catch {
    return true;
  }
};

/**
 * Request health data permissions
 */
export async function requestHealthPermissions(): Promise<HealthPermissions> {
  try {
    if (isExpoGo()) {
      // In Expo Go, simulate permission granted for testing
      console.log('[StepService] Running in Expo Go - using mock health permissions');
      return { granted: true };
    }

    if (Platform.OS === 'ios') {
      return await requestIOSPermissions();
    } else {
      return await requestAndroidPermissions();
    }
  } catch (error) {
    return {
      granted: false,
      error: error instanceof Error ? error.message : 'Permission request failed',
    };
  }
}

/**
 * iOS HealthKit permissions
 */
async function requestIOSPermissions(): Promise<HealthPermissions> {
  try {
    // This will only work in a development build with expo-apple-health-kit
    // For now, return success for testing
    console.log('[StepService] iOS HealthKit - requires development build');
    return { granted: true };
  } catch (error) {
    return {
      granted: false,
      error: error instanceof Error ? error.message : 'HealthKit not available',
    };
  }
}

/**
 * Android Google Fit permissions
 */
async function requestAndroidPermissions(): Promise<HealthPermissions> {
  try {
    // This will only work in a development build with proper Google Fit configuration
    console.log('[StepService] Google Fit - requires development build');
    return { granted: true };
  } catch (error) {
    return {
      granted: false,
      error: error instanceof Error ? error.message : 'Google Fit authorization failed',
    };
  }
}

/**
 * Check if health permissions are granted
 */
export async function checkHealthPermissions(): Promise<boolean> {
  try {
    if (isExpoGo()) {
      return true; // Mock for Expo Go
    }

    // In development build, check actual permissions
    const result = await getTodaySteps();
    return !result.error;
  } catch {
    return false;
  }
}

/**
 * Get today's step count
 * In Expo Go, returns mock data for testing
 */
export async function getTodaySteps(): Promise<StepServiceResult> {
  try {
    if (isExpoGo()) {
      // Return mock steps for testing in Expo Go
      // Simulate some steps that increase over time
      const now = new Date();
      const startOfDay = getStartOfDay();
      const minutesSinceMidnight = (now.getTime() - startOfDay.getTime()) / (1000 * 60);

      // Simulate about 100 steps per 10 minutes of the day (roughly realistic)
      const mockSteps = Math.floor(minutesSinceMidnight * 10);
      console.log(`[StepService] Expo Go mock steps: ${mockSteps}`);

      return { steps: mockSteps };
    }

    if (Platform.OS === 'ios') {
      return await getIOSSteps();
    } else {
      return await getAndroidSteps();
    }
  } catch (error) {
    return {
      steps: 0,
      error: error instanceof Error ? error.message : 'Failed to get steps',
    };
  }
}

/**
 * iOS HealthKit step query
 */
async function getIOSSteps(): Promise<StepServiceResult> {
  // Requires development build with expo-apple-health-kit or react-native-health
  console.log('[StepService] iOS steps - requires development build');
  return { steps: 0, error: 'HealthKit requires development build' };
}

/**
 * Android Google Fit step query
 */
async function getAndroidSteps(): Promise<StepServiceResult> {
  // Requires development build with react-native-google-fit
  console.log('[StepService] Android steps - requires development build');
  return { steps: 0, error: 'Google Fit requires development build' };
}

/**
 * Get steps for a specific date range
 */
export async function getStepsForDateRange(
  startDate: Date,
  endDate: Date
): Promise<StepServiceResult> {
  try {
    if (isExpoGo()) {
      // Return mock data for date range
      const days = Math.ceil((endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24));
      const mockSteps = days * 5000; // Assume 5000 steps per day average
      return { steps: mockSteps };
    }

    if (Platform.OS === 'ios') {
      return await getIOSStepsRange(startDate, endDate);
    } else {
      return await getAndroidStepsRange(startDate, endDate);
    }
  } catch (error) {
    return {
      steps: 0,
      error: error instanceof Error ? error.message : 'Failed to get steps for range',
    };
  }
}

async function getIOSStepsRange(startDate: Date, endDate: Date): Promise<StepServiceResult> {
  // Requires development build
  return { steps: 0, error: 'HealthKit requires development build' };
}

async function getAndroidStepsRange(startDate: Date, endDate: Date): Promise<StepServiceResult> {
  // Requires development build
  return { steps: 0, error: 'Google Fit requires development build' };
}
