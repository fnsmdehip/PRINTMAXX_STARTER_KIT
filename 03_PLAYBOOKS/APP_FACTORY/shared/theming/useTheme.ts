'use client';

/**
 * useTheme Hook
 * Access theme values and controls within components
 */

import { useContext, useMemo } from 'react';
import { ThemeContext } from './ThemeProvider';
import type { Theme, ThemeMode } from './themes';

// Type-safe path accessor for nested objects
type PathValue<T, P extends string> = P extends `${infer K}.${infer R}`
  ? K extends keyof T
    ? PathValue<T[K], R>
    : never
  : P extends keyof T
  ? T[P]
  : never;

/**
 * Main theme hook
 * Provides access to theme values and controls
 */
export function useTheme() {
  const context = useContext(ThemeContext);

  if (!context) {
    throw new Error(
      'useTheme must be used within a ThemeProvider. ' +
        'Wrap your app with <ThemeProvider> to use theme features.'
    );
  }

  return context;
}

/**
 * Hook to get the current theme object only
 * Useful when you only need values, not controls
 */
export function useThemeValue(): Theme {
  const { theme } = useTheme();
  return theme;
}

/**
 * Hook to get the current theme mode
 */
export function useThemeMode(): {
  mode: ThemeMode;
  resolvedMode: 'light' | 'dark';
  isDark: boolean;
  isLight: boolean;
  isSystem: boolean;
} {
  const { mode, resolvedMode } = useTheme();

  return useMemo(
    () => ({
      mode,
      resolvedMode,
      isDark: resolvedMode === 'dark',
      isLight: resolvedMode === 'light',
      isSystem: mode === 'system',
    }),
    [mode, resolvedMode]
  );
}

/**
 * Hook to get theme toggle controls
 */
export function useThemeControls(): {
  setMode: (mode: ThemeMode) => void;
  toggleTheme: () => void;
  setLight: () => void;
  setDark: () => void;
  setSystem: () => void;
} {
  const { setMode, toggleTheme } = useTheme();

  return useMemo(
    () => ({
      setMode,
      toggleTheme,
      setLight: () => setMode('light'),
      setDark: () => setMode('dark'),
      setSystem: () => setMode('system'),
    }),
    [setMode, toggleTheme]
  );
}

/**
 * Hook to get a specific color from the theme
 */
export function useColor<P extends string>(
  path: P
): PathValue<Theme['colors'], P> | undefined {
  const { theme } = useTheme();

  return useMemo(() => {
    const parts = path.split('.');
    let value: unknown = theme.colors;

    for (const part of parts) {
      if (value && typeof value === 'object' && part in value) {
        value = (value as Record<string, unknown>)[part];
      } else {
        return undefined;
      }
    }

    return value as PathValue<Theme['colors'], P>;
  }, [theme.colors, path]);
}

/**
 * Hook to get spacing value
 */
export function useSpacing(
  key: keyof Theme['spacing']
): string {
  const { theme } = useTheme();
  return theme.spacing[key];
}

/**
 * Hook to get shadow value
 */
export function useShadow(
  key: keyof Theme['shadows']
): string {
  const { theme } = useTheme();
  return theme.shadows[key];
}

/**
 * Hook to check if theme is ready (after hydration)
 */
export function useThemeReady(): boolean {
  const { isReady } = useTheme();
  return isReady;
}

/**
 * Hook to create mode-aware styles
 * Returns different values based on current mode
 */
export function useModeValue<T>(lightValue: T, darkValue: T): T {
  const { resolvedMode } = useTheme();
  return resolvedMode === 'light' ? lightValue : darkValue;
}

/**
 * Hook to get multiple theme values at once
 */
export function useThemeValues<K extends keyof Theme>(
  ...keys: K[]
): Pick<Theme, K> {
  const { theme } = useTheme();

  return useMemo(() => {
    const result = {} as Pick<Theme, K>;
    for (const key of keys) {
      result[key] = theme[key];
    }
    return result;
  }, [theme, keys]);
}

/**
 * Hook to create responsive styles based on breakpoints
 */
export function useBreakpoint(): {
  isMobile: boolean;
  isTablet: boolean;
  isDesktop: boolean;
  isLargeDesktop: boolean;
} {
  // This is a simplified version. For full responsive behavior,
  // you would use window.matchMedia with useEffect
  // This returns desktop defaults for SSR
  return useMemo(
    () => ({
      isMobile: false,
      isTablet: false,
      isDesktop: true,
      isLargeDesktop: false,
    }),
    []
  );
}
