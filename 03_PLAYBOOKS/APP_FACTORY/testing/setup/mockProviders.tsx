/**
 * Mock providers for testing
 *
 * Wraps components with necessary context providers for testing.
 */

import React, { ReactNode, createContext, useContext, useState } from 'react';
import { NavigationContainer, NavigationState } from '@react-navigation/native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// ============================================================================
// Auth Context Mock
// ============================================================================

interface AuthState {
  user: { id: string; email: string } | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

interface AuthContextValue extends AuthState {
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

interface MockAuthProviderProps {
  children: ReactNode;
  initialUser?: AuthState['user'];
  isLoading?: boolean;
}

export function MockAuthProvider({
  children,
  initialUser = null,
  isLoading = false,
}: MockAuthProviderProps) {
  const [user, setUser] = useState<AuthState['user']>(initialUser);
  const [loading, setLoading] = useState(isLoading);

  const value: AuthContextValue = {
    user,
    isAuthenticated: !!user,
    isLoading: loading,
    signIn: async (email: string) => {
      setUser({ id: '1', email });
    },
    signOut: async () => {
      setUser(null);
    },
    signUp: async (email: string) => {
      setUser({ id: '1', email });
    },
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

// ============================================================================
// Subscription Context Mock
// ============================================================================

interface SubscriptionState {
  tier: 'free' | 'pro' | 'premium';
  isActive: boolean;
  expiresAt: Date | null;
  isLoading: boolean;
}

interface SubscriptionContextValue extends SubscriptionState {
  purchase: (productId: string) => Promise<void>;
  restore: () => Promise<void>;
  checkStatus: () => Promise<void>;
}

const SubscriptionContext = createContext<SubscriptionContextValue | null>(null);

interface MockSubscriptionProviderProps {
  children: ReactNode;
  initialTier?: SubscriptionState['tier'];
  isActive?: boolean;
  isLoading?: boolean;
}

export function MockSubscriptionProvider({
  children,
  initialTier = 'free',
  isActive = true,
  isLoading = false,
}: MockSubscriptionProviderProps) {
  const [tier, setTier] = useState<SubscriptionState['tier']>(initialTier);
  const [active, setActive] = useState(isActive);
  const [loading, setLoading] = useState(isLoading);

  const value: SubscriptionContextValue = {
    tier,
    isActive: active,
    expiresAt: active ? new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) : null,
    isLoading: loading,
    purchase: async (productId: string) => {
      if (productId.includes('premium')) {
        setTier('premium');
      } else {
        setTier('pro');
      }
      setActive(true);
    },
    restore: async () => {
      // No-op in mock
    },
    checkStatus: async () => {
      // No-op in mock
    },
  };

  return (
    <SubscriptionContext.Provider value={value}>
      {children}
    </SubscriptionContext.Provider>
  );
}

export function useSubscription(): SubscriptionContextValue {
  const context = useContext(SubscriptionContext);
  if (!context) {
    throw new Error('useSubscription must be used within a SubscriptionProvider');
  }
  return context;
}

// ============================================================================
// Theme Context Mock
// ============================================================================

interface ThemeContextValue {
  isDark: boolean;
  toggle: () => void;
  colors: {
    background: string;
    text: string;
    primary: string;
    secondary: string;
    error: string;
    success: string;
  };
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

interface MockThemeProviderProps {
  children: ReactNode;
  isDark?: boolean;
}

export function MockThemeProvider({
  children,
  isDark: initialDark = false,
}: MockThemeProviderProps) {
  const [isDark, setIsDark] = useState(initialDark);

  const colors = isDark
    ? {
        background: '#000000',
        text: '#FFFFFF',
        primary: '#0A84FF',
        secondary: '#5E5CE6',
        error: '#FF453A',
        success: '#30D158',
      }
    : {
        background: '#FFFFFF',
        text: '#000000',
        primary: '#007AFF',
        secondary: '#5856D6',
        error: '#FF3B30',
        success: '#34C759',
      };

  const value: ThemeContextValue = {
    isDark,
    toggle: () => setIsDark((prev) => !prev),
    colors,
  };

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme(): ThemeContextValue {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}

// ============================================================================
// Analytics Context Mock
// ============================================================================

interface AnalyticsContextValue {
  track: (event: string, properties?: Record<string, unknown>) => void;
  identify: (userId: string, traits?: Record<string, unknown>) => void;
  screen: (name: string, properties?: Record<string, unknown>) => void;
}

const AnalyticsContext = createContext<AnalyticsContextValue | null>(null);

interface MockAnalyticsProviderProps {
  children: ReactNode;
  onTrack?: (event: string, properties?: Record<string, unknown>) => void;
  onIdentify?: (userId: string, traits?: Record<string, unknown>) => void;
  onScreen?: (name: string, properties?: Record<string, unknown>) => void;
}

export function MockAnalyticsProvider({
  children,
  onTrack = jest.fn(),
  onIdentify = jest.fn(),
  onScreen = jest.fn(),
}: MockAnalyticsProviderProps) {
  const value: AnalyticsContextValue = {
    track: onTrack,
    identify: onIdentify,
    screen: onScreen,
  };

  return (
    <AnalyticsContext.Provider value={value}>{children}</AnalyticsContext.Provider>
  );
}

export function useAnalytics(): AnalyticsContextValue {
  const context = useContext(AnalyticsContext);
  if (!context) {
    throw new Error('useAnalytics must be used within an AnalyticsProvider');
  }
  return context;
}

// ============================================================================
// Combined Provider
// ============================================================================

interface AllProvidersProps {
  children: ReactNode;
  queryClient?: QueryClient;
  navigationState?: Partial<NavigationState>;
  authUser?: AuthState['user'];
  subscriptionTier?: SubscriptionState['tier'];
  isDarkTheme?: boolean;
}

export function AllProviders({
  children,
  queryClient,
  navigationState,
  authUser = null,
  subscriptionTier = 'free',
  isDarkTheme = false,
}: AllProvidersProps) {
  const client =
    queryClient ??
    new QueryClient({
      defaultOptions: {
        queries: { retry: false, gcTime: 0 },
        mutations: { retry: false },
      },
    });

  return (
    <QueryClientProvider client={client}>
      <SafeAreaProvider>
        <NavigationContainer initialState={navigationState as NavigationState}>
          <MockAuthProvider initialUser={authUser}>
            <MockSubscriptionProvider initialTier={subscriptionTier}>
              <MockThemeProvider isDark={isDarkTheme}>
                <MockAnalyticsProvider>{children}</MockAnalyticsProvider>
              </MockThemeProvider>
            </MockSubscriptionProvider>
          </MockAuthProvider>
        </NavigationContainer>
      </SafeAreaProvider>
    </QueryClientProvider>
  );
}

// ============================================================================
// Provider Utilities
// ============================================================================

/**
 * Create a custom provider wrapper for specific test scenarios
 */
export function createProviderWrapper(options: Omit<AllProvidersProps, 'children'> = {}) {
  return function ProviderWrapper({ children }: { children: ReactNode }) {
    return <AllProviders {...options}>{children}</AllProviders>;
  };
}

/**
 * Create isolated provider for hook testing
 */
export function createHookWrapper<T>(
  Provider: React.ComponentType<{ children: ReactNode } & T>,
  props: T
) {
  return function HookWrapper({ children }: { children: ReactNode }) {
    return <Provider {...props}>{children}</Provider>;
  };
}
