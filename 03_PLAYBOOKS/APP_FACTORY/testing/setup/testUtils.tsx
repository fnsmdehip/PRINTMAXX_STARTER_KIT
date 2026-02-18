/**
 * Test utilities and render helpers
 *
 * Usage:
 *   import { render, screen, fireEvent } from '@testing/setup/testUtils';
 */

import React, { ReactElement, ReactNode } from 'react';
import { render, RenderOptions, RenderResult } from '@testing-library/react-native';
import { NavigationContainer } from '@react-navigation/native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import { AllProviders } from './mockProviders';

// Re-export everything from testing library
export * from '@testing-library/react-native';

// Create a fresh query client for each test
function createTestQueryClient(): QueryClient {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        gcTime: 0,
        staleTime: 0,
      },
      mutations: {
        retry: false,
      },
    },
  });
}

/**
 * Custom render with all providers
 */
interface CustomRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  initialRoute?: string;
  navigationState?: object;
  queryClient?: QueryClient;
  providers?: React.ComponentType<{ children: ReactNode }>[];
}

function customRender(
  ui: ReactElement,
  options: CustomRenderOptions = {}
): RenderResult {
  const {
    initialRoute,
    navigationState,
    queryClient = createTestQueryClient(),
    providers = [],
    ...renderOptions
  } = options;

  function Wrapper({ children }: { children: ReactNode }) {
    // Compose additional providers
    const composed = providers.reduce(
      (acc, Provider) => <Provider>{acc}</Provider>,
      children
    );

    return (
      <AllProviders queryClient={queryClient} navigationState={navigationState}>
        {composed}
      </AllProviders>
    );
  }

  return render(ui, { wrapper: Wrapper, ...renderOptions });
}

/**
 * Render with navigation context only
 */
function renderWithNavigation(
  ui: ReactElement,
  options: Omit<CustomRenderOptions, 'providers'> = {}
): RenderResult {
  function Wrapper({ children }: { children: ReactNode }) {
    return (
      <SafeAreaProvider>
        <NavigationContainer>
          {children}
        </NavigationContainer>
      </SafeAreaProvider>
    );
  }

  return render(ui, { wrapper: Wrapper, ...options });
}

/**
 * Render with query client only
 */
function renderWithQuery(
  ui: ReactElement,
  options: Omit<CustomRenderOptions, 'providers' | 'navigationState'> = {}
): RenderResult {
  const { queryClient = createTestQueryClient(), ...renderOptions } = options;

  function Wrapper({ children }: { children: ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    );
  }

  return render(ui, { wrapper: Wrapper, ...renderOptions });
}

/**
 * Render without any providers (pure component testing)
 */
function renderPure(
  ui: ReactElement,
  options: Omit<RenderOptions, 'wrapper'> = {}
): RenderResult {
  return render(ui, options);
}

/**
 * Wait for all pending promises to resolve
 */
async function flushPromises(): Promise<void> {
  return new Promise((resolve) => setImmediate(resolve));
}

/**
 * Wait for a specific amount of time
 */
function wait(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Create a mock navigation object
 */
function createMockNavigation() {
  return {
    navigate: jest.fn(),
    goBack: jest.fn(),
    setOptions: jest.fn(),
    addListener: jest.fn(() => jest.fn()),
    removeListener: jest.fn(),
    reset: jest.fn(),
    isFocused: jest.fn(() => true),
    canGoBack: jest.fn(() => true),
    dispatch: jest.fn(),
    setParams: jest.fn(),
    getParent: jest.fn(() => null),
    getState: jest.fn(() => ({
      index: 0,
      routes: [{ name: 'Test', params: {} }],
    })),
  };
}

/**
 * Create a mock route object
 */
function createMockRoute<T extends Record<string, unknown>>(params: T = {} as T) {
  return {
    key: 'test-route-key',
    name: 'TestScreen',
    params,
  };
}

/**
 * Simulate text input change
 */
function typeText(
  element: ReactElement | ReturnType<typeof customRender>['getByTestId'] extends (id: string) => infer R ? R : never,
  text: string
): void {
  const { fireEvent } = require('@testing-library/react-native');
  fireEvent.changeText(element, text);
}

/**
 * Simulate button press
 */
function pressButton(
  element: ReactElement | ReturnType<typeof customRender>['getByTestId'] extends (id: string) => infer R ? R : never
): void {
  const { fireEvent } = require('@testing-library/react-native');
  fireEvent.press(element);
}

/**
 * Assert element is visible on screen
 */
function expectVisible(element: unknown): void {
  expect(element).toBeOnTheScreen();
}

/**
 * Assert element is not visible on screen
 */
function expectNotVisible(element: unknown): void {
  expect(element).not.toBeOnTheScreen();
}

// Override default render with custom render
export {
  customRender as render,
  renderWithNavigation,
  renderWithQuery,
  renderPure,
  flushPromises,
  wait,
  createMockNavigation,
  createMockRoute,
  typeText,
  pressButton,
  expectVisible,
  expectNotVisible,
  createTestQueryClient,
};
