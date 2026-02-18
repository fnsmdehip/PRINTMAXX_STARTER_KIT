/**
 * Mock implementation of @react-native-async-storage/async-storage
 *
 * Usage in tests:
 *   import mockAsyncStorage from '@testing/mocks/mockAsyncStorage';
 *
 *   beforeEach(() => {
 *     mockAsyncStorage.clear();
 *   });
 *
 *   test('stores value', async () => {
 *     await AsyncStorage.setItem('key', 'value');
 *     expect(mockAsyncStorage.store['key']).toBe('value');
 *   });
 */

type StorageValue = string | null;
type MultiGetResult = readonly [string, StorageValue][];
type MultiSetInput = readonly [string, string][];

interface MockAsyncStorage {
  store: Record<string, StorageValue>;
  getItem: jest.Mock<Promise<StorageValue>, [string]>;
  setItem: jest.Mock<Promise<void>, [string, string]>;
  removeItem: jest.Mock<Promise<void>, [string]>;
  mergeItem: jest.Mock<Promise<void>, [string, string]>;
  clear: jest.Mock<Promise<void>, []>;
  getAllKeys: jest.Mock<Promise<readonly string[]>, []>;
  multiGet: jest.Mock<Promise<MultiGetResult>, [readonly string[]]>;
  multiSet: jest.Mock<Promise<void>, [MultiSetInput]>;
  multiRemove: jest.Mock<Promise<void>, [readonly string[]]>;
  multiMerge: jest.Mock<Promise<void>, [MultiSetInput]>;
  flushGetRequests: jest.Mock<void, []>;
  useAsyncStorage: (key: string) => {
    getItem: () => Promise<StorageValue>;
    setItem: (value: string) => Promise<void>;
    removeItem: () => Promise<void>;
    mergeItem: (value: string) => Promise<void>;
  };
}

const createMockAsyncStorage = (): MockAsyncStorage => {
  const store: Record<string, StorageValue> = {};

  const mockAsyncStorage: MockAsyncStorage = {
    store,

    getItem: jest.fn(async (key: string): Promise<StorageValue> => {
      return store[key] ?? null;
    }),

    setItem: jest.fn(async (key: string, value: string): Promise<void> => {
      store[key] = value;
    }),

    removeItem: jest.fn(async (key: string): Promise<void> => {
      delete store[key];
    }),

    mergeItem: jest.fn(async (key: string, value: string): Promise<void> => {
      const existing = store[key];
      if (existing) {
        try {
          const existingObj = JSON.parse(existing);
          const valueObj = JSON.parse(value);
          store[key] = JSON.stringify({ ...existingObj, ...valueObj });
        } catch {
          store[key] = value;
        }
      } else {
        store[key] = value;
      }
    }),

    clear: jest.fn(async (): Promise<void> => {
      Object.keys(store).forEach((key) => {
        delete store[key];
      });
    }),

    getAllKeys: jest.fn(async (): Promise<readonly string[]> => {
      return Object.keys(store);
    }),

    multiGet: jest.fn(async (keys: readonly string[]): Promise<MultiGetResult> => {
      return keys.map((key) => [key, store[key] ?? null] as const);
    }),

    multiSet: jest.fn(async (keyValuePairs: MultiSetInput): Promise<void> => {
      keyValuePairs.forEach(([key, value]) => {
        store[key] = value;
      });
    }),

    multiRemove: jest.fn(async (keys: readonly string[]): Promise<void> => {
      keys.forEach((key) => {
        delete store[key];
      });
    }),

    multiMerge: jest.fn(async (keyValuePairs: MultiSetInput): Promise<void> => {
      keyValuePairs.forEach(([key, value]) => {
        const existing = store[key];
        if (existing) {
          try {
            const existingObj = JSON.parse(existing);
            const valueObj = JSON.parse(value);
            store[key] = JSON.stringify({ ...existingObj, ...valueObj });
          } catch {
            store[key] = value;
          }
        } else {
          store[key] = value;
        }
      });
    }),

    flushGetRequests: jest.fn((): void => {
      // No-op in mock
    }),

    useAsyncStorage: (key: string) => ({
      getItem: async () => store[key] ?? null,
      setItem: async (value: string) => {
        store[key] = value;
      },
      removeItem: async () => {
        delete store[key];
      },
      mergeItem: async (value: string) => {
        const existing = store[key];
        if (existing) {
          try {
            const existingObj = JSON.parse(existing);
            const valueObj = JSON.parse(value);
            store[key] = JSON.stringify({ ...existingObj, ...valueObj });
          } catch {
            store[key] = value;
          }
        } else {
          store[key] = value;
        }
      },
    }),
  };

  return mockAsyncStorage;
};

const mockAsyncStorage = createMockAsyncStorage();

export default mockAsyncStorage;

// ============================================================================
// Test Utilities
// ============================================================================

/**
 * Pre-populate storage with test data
 */
export function seedStorage(data: Record<string, unknown>): void {
  Object.entries(data).forEach(([key, value]) => {
    mockAsyncStorage.store[key] = typeof value === 'string' ? value : JSON.stringify(value);
  });
}

/**
 * Get all stored data as parsed objects
 */
export function getStoredData(): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  Object.entries(mockAsyncStorage.store).forEach(([key, value]) => {
    if (value) {
      try {
        result[key] = JSON.parse(value);
      } catch {
        result[key] = value;
      }
    }
  });
  return result;
}

/**
 * Reset mock to initial state
 */
export function resetMockAsyncStorage(): void {
  mockAsyncStorage.clear();
  mockAsyncStorage.getItem.mockClear();
  mockAsyncStorage.setItem.mockClear();
  mockAsyncStorage.removeItem.mockClear();
  mockAsyncStorage.mergeItem.mockClear();
  mockAsyncStorage.getAllKeys.mockClear();
  mockAsyncStorage.multiGet.mockClear();
  mockAsyncStorage.multiSet.mockClear();
  mockAsyncStorage.multiRemove.mockClear();
  mockAsyncStorage.multiMerge.mockClear();
}

/**
 * Simulate storage errors
 */
export function simulateStorageError(method: keyof MockAsyncStorage, error: Error): void {
  const mockMethod = mockAsyncStorage[method];
  if (typeof mockMethod === 'function' && 'mockRejectedValueOnce' in mockMethod) {
    (mockMethod as jest.Mock).mockRejectedValueOnce(error);
  }
}

/**
 * Common storage keys used in the app
 */
export const STORAGE_KEYS = {
  AUTH_TOKEN: '@auth_token',
  USER_DATA: '@user_data',
  ONBOARDING_COMPLETE: '@onboarding_complete',
  THEME_PREFERENCE: '@theme_preference',
  NOTIFICATION_SETTINGS: '@notification_settings',
  CACHED_DATA: '@cached_data',
  LAST_SYNC: '@last_sync',
} as const;
