import { Pedometer } from 'expo-sensors';

export interface PedometerResult {
  steps: number;
}

export interface PedometerSubscription {
  remove: () => void;
}

export const isPedometerAvailable = async (): Promise<boolean> => {
  try {
    const result = await Pedometer.isAvailableAsync();
    return result;
  } catch (error) {
    console.error('Error checking pedometer availability:', error);
    return false;
  }
};

export const getPermissionStatus = async (): Promise<boolean> => {
  try {
    const { status } = await Pedometer.requestPermissionsAsync();
    return status === 'granted';
  } catch (error) {
    console.error('Error requesting pedometer permissions:', error);
    return false;
  }
};

export const getStepCountFromDate = async (startDate: Date, endDate: Date): Promise<number> => {
  try {
    const result = await Pedometer.getStepCountAsync(startDate, endDate);
    return result.steps;
  } catch (error) {
    console.error('Error getting step count:', error);
    return 0;
  }
};

export const getTodayStepCount = async (): Promise<number> => {
  try {
    const now = new Date();
    const startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const result = await Pedometer.getStepCountAsync(startOfDay, now);
    return result.steps;
  } catch (error) {
    console.error('Error getting today step count:', error);
    return 0;
  }
};

export const subscribeToStepCount = (
  callback: (result: PedometerResult) => void
): PedometerSubscription => {
  return Pedometer.watchStepCount(callback);
};

export const getStepsForLastNDays = async (days: number): Promise<{ date: Date; steps: number }[]> => {
  const results: { date: Date; steps: number }[] = [];

  for (let i = 0; i < days; i++) {
    const date = new Date();
    date.setDate(date.getDate() - i);

    const startOfDay = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    const endOfDay = new Date(date.getFullYear(), date.getMonth(), date.getDate(), 23, 59, 59);

    try {
      const result = await Pedometer.getStepCountAsync(startOfDay, endOfDay);
      results.push({ date: startOfDay, steps: result.steps });
    } catch (error) {
      results.push({ date: startOfDay, steps: 0 });
    }
  }

  return results;
};

export const formatStepCount = (steps: number): string => {
  if (steps >= 10000) {
    return `${(steps / 1000).toFixed(1)}k`;
  }
  return steps.toLocaleString();
};

export const calculateCaloriesBurned = (steps: number): number => {
  const caloriesPerStep = 0.04;
  return Math.round(steps * caloriesPerStep);
};

export const calculateDistanceWalked = (steps: number): number => {
  const averageStrideLength = 0.762;
  const distanceInMeters = steps * averageStrideLength;
  const distanceInKm = distanceInMeters / 1000;
  return Math.round(distanceInKm * 100) / 100;
};

export const getMotivationalMessage = (progress: number): string => {
  if (progress === 0) {
    return "Let's get moving!";
  } else if (progress < 0.25) {
    return 'Great start! Keep going!';
  } else if (progress < 0.5) {
    return "You're making progress!";
  } else if (progress < 0.75) {
    return 'Halfway there! Push through!';
  } else if (progress < 1) {
    return 'Almost there! Final stretch!';
  } else {
    return 'Goal crushed! You did it!';
  }
};
