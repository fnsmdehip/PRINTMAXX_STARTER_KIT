/**
 * Jest configuration for React Native
 *
 * Run tests: npm test
 * Run with coverage: npm test -- --coverage
 */

module.exports = {
  preset: 'react-native',

  // Setup files
  setupFilesAfterEnv: ['<rootDir>/testing/setup/jest.setup.ts'],

  // Module resolution
  moduleNameMapper: {
    // Path aliases - match tsconfig paths
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@components/(.*)$': '<rootDir>/src/components/$1',
    '^@screens/(.*)$': '<rootDir>/src/screens/$1',
    '^@hooks/(.*)$': '<rootDir>/src/hooks/$1',
    '^@utils/(.*)$': '<rootDir>/src/utils/$1',
    '^@services/(.*)$': '<rootDir>/src/services/$1',
    '^@constants/(.*)$': '<rootDir>/src/constants/$1',
    '^@types/(.*)$': '<rootDir>/src/types/$1',
    '^@testing/(.*)$': '<rootDir>/testing/$1',
  },

  // Transform settings
  transformIgnorePatterns: [
    'node_modules/(?!(react-native' +
      '|@react-native' +
      '|react-native-reanimated' +
      '|@react-navigation' +
      '|react-native-gesture-handler' +
      '|react-native-screens' +
      '|react-native-safe-area-context' +
      '|@react-native-async-storage/async-storage' +
      '|react-native-purchases' +
      ')/)',
  ],

  // Test file patterns
  testMatch: [
    '**/__tests__/**/*.[jt]s?(x)',
    '**/?(*.)+(spec|test).[jt]s?(x)',
  ],

  // Ignore patterns
  testPathIgnorePatterns: [
    '<rootDir>/node_modules/',
    '<rootDir>/testing/e2e/',
  ],

  // Coverage configuration
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/index.{ts,tsx}',
    '!src/**/*.stories.{ts,tsx}',
    '!src/types/**/*',
  ],

  coverageThreshold: {
    global: {
      branches: 70,
      functions: 75,
      lines: 75,
      statements: 75,
    },
  },

  coverageReporters: ['text', 'text-summary', 'lcov', 'html'],

  // Mock files
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],

  // Global mocks
  globals: {
    __DEV__: true,
  },

  // Timeout for async tests
  testTimeout: 10000,

  // Clear mocks between tests
  clearMocks: true,
  resetMocks: false,
  restoreMocks: true,

  // Verbose output in CI
  verbose: process.env.CI === 'true',

  // Max workers for parallel execution
  maxWorkers: process.env.CI === 'true' ? 2 : '50%',

  // Cache for faster subsequent runs
  cacheDirectory: '<rootDir>/.jest-cache',
};
