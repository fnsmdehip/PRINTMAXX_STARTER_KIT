import 'react-native-gesture-handler/jestSetup';

jest.mock('@react-native-async-storage/async-storage', () =>
  require('@react-native-async-storage/async-storage/jest/async-storage-mock')
);

jest.mock('react-native-health', () => ({
  isAvailable: jest.fn(() => Promise.resolve(true)),
  initHealthKit: jest.fn(() => Promise.resolve()),
  getStepCount: jest.fn(() => Promise.resolve({ value: 5000 })),
}));

jest.mock('react-native-google-fit', () => ({
  authorize: jest.fn(() => Promise.resolve({ success: true })),
  getDailyStepCountSamples: jest.fn(() => Promise.resolve([{ steps: 5000 }])),
}));

jest.mock('react-native-purchases', () => ({
  configure: jest.fn(),
  getOfferings: jest.fn(() => Promise.resolve({ current: null })),
  purchasePackage: jest.fn(),
  getCustomerInfo: jest.fn(() =>
    Promise.resolve({ entitlements: { active: {} } })
  ),
}));
