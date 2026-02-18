/**
 * Mock implementation for React Navigation
 *
 * Usage in tests:
 *   import { createMockNavigation, mockNavigationModule } from '@testing/mocks/mockNavigation';
 *
 *   test('navigates to settings', () => {
 *     const navigation = createMockNavigation();
 *     render(<Screen navigation={navigation} />);
 *     // ... trigger navigation
 *     expect(navigation.navigate).toHaveBeenCalledWith('Settings');
 *   });
 */

import type { ParamListBase, NavigationState } from '@react-navigation/native';

// ============================================================================
// Types
// ============================================================================

export interface MockNavigation {
  navigate: jest.Mock;
  goBack: jest.Mock;
  reset: jest.Mock;
  setOptions: jest.Mock;
  setParams: jest.Mock;
  dispatch: jest.Mock;
  addListener: jest.Mock;
  removeListener: jest.Mock;
  isFocused: jest.Mock;
  canGoBack: jest.Mock;
  getParent: jest.Mock;
  getState: jest.Mock;
  getId: jest.Mock;
  push: jest.Mock;
  pop: jest.Mock;
  popToTop: jest.Mock;
  replace: jest.Mock;
}

export interface MockRoute<T extends Record<string, unknown> = Record<string, unknown>> {
  key: string;
  name: string;
  params: T;
  path?: string;
}

export interface NavigationCall {
  type: 'navigate' | 'goBack' | 'reset' | 'push' | 'pop' | 'replace';
  screen?: string;
  params?: Record<string, unknown>;
  timestamp: Date;
}

// ============================================================================
// Mock State
// ============================================================================

let navigationHistory: NavigationCall[] = [];
let currentRoute: MockRoute = {
  key: 'test-route-0',
  name: 'TestScreen',
  params: {},
};
let canGoBackValue = true;
let isFocusedValue = true;

// ============================================================================
// Test Utilities
// ============================================================================

/**
 * Get navigation history
 */
export function getNavigationHistory(): NavigationCall[] {
  return [...navigationHistory];
}

/**
 * Check if navigation occurred
 */
export function wasNavigatedTo(screen: string, params?: Record<string, unknown>): boolean {
  return navigationHistory.some((call) => {
    if (call.screen !== screen) return false;
    if (!params) return true;
    return Object.entries(params).every(
      ([key, value]) => call.params?.[key] === value
    );
  });
}

/**
 * Get last navigation call
 */
export function getLastNavigation(): NavigationCall | undefined {
  return navigationHistory[navigationHistory.length - 1];
}

/**
 * Reset navigation mock state
 */
export function resetMockNavigation(): void {
  navigationHistory = [];
  currentRoute = {
    key: 'test-route-0',
    name: 'TestScreen',
    params: {},
  };
  canGoBackValue = true;
  isFocusedValue = true;
}

/**
 * Set the current route
 */
export function setCurrentRoute<T extends Record<string, unknown>>(
  name: string,
  params: T = {} as T
): void {
  currentRoute = {
    key: `${name}-${Date.now()}`,
    name,
    params,
  };
}

/**
 * Set canGoBack return value
 */
export function setCanGoBack(value: boolean): void {
  canGoBackValue = value;
}

/**
 * Set isFocused return value
 */
export function setIsFocused(value: boolean): void {
  isFocusedValue = value;
}

// ============================================================================
// Factory Functions
// ============================================================================

let routeKeyCounter = 0;

/**
 * Create a mock navigation object
 */
export function createMockNavigation(): MockNavigation {
  const listeners: Map<string, Set<() => void>> = new Map();

  const navigation: MockNavigation = {
    navigate: jest.fn((screenOrOptions: string | object, params?: Record<string, unknown>) => {
      const screen = typeof screenOrOptions === 'string' ? screenOrOptions : (screenOrOptions as { name: string }).name;
      const navParams = typeof screenOrOptions === 'string' ? params : (screenOrOptions as { params?: Record<string, unknown> }).params;

      navigationHistory.push({
        type: 'navigate',
        screen,
        params: navParams,
        timestamp: new Date(),
      });
    }),

    goBack: jest.fn(() => {
      navigationHistory.push({
        type: 'goBack',
        timestamp: new Date(),
      });
    }),

    reset: jest.fn((state: Partial<NavigationState>) => {
      navigationHistory.push({
        type: 'reset',
        timestamp: new Date(),
      });
    }),

    setOptions: jest.fn((options: Record<string, unknown>) => {}),

    setParams: jest.fn((params: Record<string, unknown>) => {
      currentRoute = { ...currentRoute, params: { ...currentRoute.params, ...params } };
    }),

    dispatch: jest.fn((action: unknown) => {}),

    addListener: jest.fn((event: string, callback: () => void) => {
      if (!listeners.has(event)) {
        listeners.set(event, new Set());
      }
      listeners.get(event)!.add(callback);

      // Return unsubscribe function
      return () => {
        listeners.get(event)?.delete(callback);
      };
    }),

    removeListener: jest.fn((event: string, callback: () => void) => {
      listeners.get(event)?.delete(callback);
    }),

    isFocused: jest.fn(() => isFocusedValue),

    canGoBack: jest.fn(() => canGoBackValue),

    getParent: jest.fn(() => null),

    getState: jest.fn(() => ({
      index: 0,
      routes: [currentRoute],
      key: 'stack-0',
      routeNames: [currentRoute.name],
      type: 'stack',
      stale: false,
    })),

    getId: jest.fn(() => 'navigator-id'),

    // Stack navigator specific
    push: jest.fn((screen: string, params?: Record<string, unknown>) => {
      navigationHistory.push({
        type: 'push',
        screen,
        params,
        timestamp: new Date(),
      });
    }),

    pop: jest.fn((count?: number) => {
      navigationHistory.push({
        type: 'pop',
        timestamp: new Date(),
      });
    }),

    popToTop: jest.fn(() => {
      navigationHistory.push({
        type: 'pop',
        timestamp: new Date(),
      });
    }),

    replace: jest.fn((screen: string, params?: Record<string, unknown>) => {
      navigationHistory.push({
        type: 'replace',
        screen,
        params,
        timestamp: new Date(),
      });
    }),
  };

  return navigation;
}

/**
 * Create a mock route object
 */
export function createMockRoute<T extends Record<string, unknown>>(
  name: string = 'TestScreen',
  params: T = {} as T
): MockRoute<T> {
  return {
    key: `${name}-${routeKeyCounter++}`,
    name,
    params,
  };
}

// ============================================================================
// Navigation Module Mock
// ============================================================================

/**
 * Full mock of @react-navigation/native module
 */
export const mockNavigationModule = {
  NavigationContainer: ({ children }: { children: React.ReactNode }) => children,

  useNavigation: () => createMockNavigation(),

  useRoute: () => currentRoute,

  useFocusEffect: (callback: () => void | (() => void)) => {
    // Execute callback immediately in tests
    const cleanup = callback();
    // Return cleanup if provided
    if (typeof cleanup === 'function') {
      cleanup();
    }
  },

  useIsFocused: () => isFocusedValue,

  useNavigationState: <T,>(selector: (state: NavigationState) => T): T => {
    const state: NavigationState = {
      index: 0,
      routes: [currentRoute as any],
      key: 'stack-0',
      routeNames: [currentRoute.name],
      type: 'stack',
      stale: false,
    };
    return selector(state);
  },

  useNavigationContainerRef: () => ({
    current: {
      navigate: jest.fn(),
      goBack: jest.fn(),
      reset: jest.fn(),
      isReady: jest.fn(() => true),
      getCurrentRoute: jest.fn(() => currentRoute),
    },
  }),

  useLinkTo: () => jest.fn((path: string) => {
    navigationHistory.push({
      type: 'navigate',
      screen: path,
      timestamp: new Date(),
    });
  }),

  useScrollToTop: jest.fn(),

  CommonActions: {
    navigate: (options: { name: string; params?: Record<string, unknown> }) => ({
      type: 'NAVIGATE',
      payload: options,
    }),
    reset: (state: Partial<NavigationState>) => ({
      type: 'RESET',
      payload: state,
    }),
    goBack: () => ({ type: 'GO_BACK' }),
    setParams: (params: Record<string, unknown>) => ({
      type: 'SET_PARAMS',
      payload: { params },
    }),
  },

  StackActions: {
    push: (name: string, params?: Record<string, unknown>) => ({
      type: 'PUSH',
      payload: { name, params },
    }),
    pop: (count?: number) => ({
      type: 'POP',
      payload: { count: count ?? 1 },
    }),
    popToTop: () => ({ type: 'POP_TO_TOP' }),
    replace: (name: string, params?: Record<string, unknown>) => ({
      type: 'REPLACE',
      payload: { name, params },
    }),
  },

  TabActions: {
    jumpTo: (name: string, params?: Record<string, unknown>) => ({
      type: 'JUMP_TO',
      payload: { name, params },
    }),
  },

  DrawerActions: {
    openDrawer: () => ({ type: 'OPEN_DRAWER' }),
    closeDrawer: () => ({ type: 'CLOSE_DRAWER' }),
    toggleDrawer: () => ({ type: 'TOGGLE_DRAWER' }),
  },
};

export default mockNavigationModule;

// ============================================================================
// Assertion Helpers
// ============================================================================

/**
 * Assert navigation to screen occurred
 */
export function expectNavigation(screen: string, params?: Record<string, unknown>): void {
  expect(wasNavigatedTo(screen, params)).toBe(true);
}

/**
 * Assert goBack was called
 */
export function expectGoBack(): void {
  expect(navigationHistory.some((c) => c.type === 'goBack')).toBe(true);
}

/**
 * Assert reset was called
 */
export function expectReset(): void {
  expect(navigationHistory.some((c) => c.type === 'reset')).toBe(true);
}
