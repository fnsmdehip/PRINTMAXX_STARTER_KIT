'use client';

/**
 * ThemeProvider
 * React context provider for theme management
 * Supports light/dark modes with system preference detection
 */

import React, {
  createContext,
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react';
import { lightTheme } from './themes/light';
import { darkTheme } from './themes/dark';
import type { Theme, ThemeMode } from './themes';

// Storage key for persisting theme preference
const THEME_STORAGE_KEY = 'app-theme-mode';

// Media query for system dark mode preference
const DARK_MODE_MEDIA_QUERY = '(prefers-color-scheme: dark)';

interface ThemeContextValue {
  /** Current resolved theme object */
  theme: Theme;
  /** Current theme mode setting (light, dark, or system) */
  mode: ThemeMode;
  /** Resolved mode after system preference (only light or dark) */
  resolvedMode: 'light' | 'dark';
  /** Set theme mode */
  setMode: (mode: ThemeMode) => void;
  /** Toggle between light and dark (ignores system) */
  toggleTheme: () => void;
  /** Whether theme is ready (hydration complete) */
  isReady: boolean;
}

export const ThemeContext = createContext<ThemeContextValue | null>(null);

interface ThemeProviderProps {
  /** Child components */
  children: ReactNode;
  /** Initial theme mode (defaults to system) */
  defaultMode?: ThemeMode;
  /** Custom light theme (for app-specific overrides) */
  lightThemeOverride?: Theme;
  /** Custom dark theme (for app-specific overrides) */
  darkThemeOverride?: Theme;
  /** Storage key for persistence (allows multiple apps) */
  storageKey?: string;
  /** Disable persistence */
  disablePersistence?: boolean;
  /** Attribute to set on document element */
  attribute?: 'class' | 'data-theme';
  /** Enable smooth transitions on theme change */
  enableTransitions?: boolean;
}

/**
 * Get system color scheme preference
 */
function getSystemPreference(): 'light' | 'dark' {
  if (typeof window === 'undefined') return 'light';
  return window.matchMedia(DARK_MODE_MEDIA_QUERY).matches ? 'dark' : 'light';
}

/**
 * Get stored theme preference
 */
function getStoredMode(key: string): ThemeMode | null {
  if (typeof window === 'undefined') return null;
  try {
    const stored = localStorage.getItem(key);
    if (stored === 'light' || stored === 'dark' || stored === 'system') {
      return stored;
    }
  } catch {
    // localStorage unavailable
  }
  return null;
}

/**
 * Store theme preference
 */
function storeMode(key: string, mode: ThemeMode): void {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(key, mode);
  } catch {
    // localStorage unavailable
  }
}

/**
 * Apply theme to document
 */
function applyThemeToDocument(
  mode: 'light' | 'dark',
  attribute: 'class' | 'data-theme',
  enableTransitions: boolean
): void {
  if (typeof window === 'undefined') return;

  const root = document.documentElement;

  // Disable transitions during theme change to prevent flash
  if (!enableTransitions) {
    root.style.setProperty('transition', 'none');
  }

  if (attribute === 'class') {
    root.classList.remove('light', 'dark');
    root.classList.add(mode);
  } else {
    root.setAttribute('data-theme', mode);
  }

  // Set color-scheme for native element styling
  root.style.colorScheme = mode;

  // Re-enable transitions
  if (!enableTransitions) {
    // Force reflow
    root.offsetHeight;
    root.style.removeProperty('transition');
  }
}

export function ThemeProvider({
  children,
  defaultMode = 'system',
  lightThemeOverride,
  darkThemeOverride,
  storageKey = THEME_STORAGE_KEY,
  disablePersistence = false,
  attribute = 'class',
  enableTransitions = false,
}: ThemeProviderProps) {
  // Initialize with default to avoid hydration mismatch
  const [mode, setModeState] = useState<ThemeMode>(defaultMode);
  const [systemPreference, setSystemPreference] = useState<'light' | 'dark'>('light');
  const [isReady, setIsReady] = useState(false);

  // Resolve the actual mode (light or dark)
  const resolvedMode = useMemo<'light' | 'dark'>(() => {
    if (mode === 'system') {
      return systemPreference;
    }
    return mode;
  }, [mode, systemPreference]);

  // Get the theme object
  const theme = useMemo(() => {
    if (resolvedMode === 'dark') {
      return darkThemeOverride ?? darkTheme;
    }
    return lightThemeOverride ?? lightTheme;
  }, [resolvedMode, lightThemeOverride, darkThemeOverride]);

  // Initialize on mount
  useEffect(() => {
    // Get system preference
    const systemPref = getSystemPreference();
    setSystemPreference(systemPref);

    // Get stored preference
    if (!disablePersistence) {
      const stored = getStoredMode(storageKey);
      if (stored) {
        setModeState(stored);
      }
    }

    setIsReady(true);
  }, [disablePersistence, storageKey]);

  // Listen for system preference changes
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const mediaQuery = window.matchMedia(DARK_MODE_MEDIA_QUERY);

    const handleChange = (e: MediaQueryListEvent) => {
      setSystemPreference(e.matches ? 'dark' : 'light');
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  // Apply theme to document when resolved mode changes
  useEffect(() => {
    if (!isReady) return;
    applyThemeToDocument(resolvedMode, attribute, enableTransitions);
  }, [resolvedMode, attribute, enableTransitions, isReady]);

  // Set mode with persistence
  const setMode = useCallback(
    (newMode: ThemeMode) => {
      setModeState(newMode);
      if (!disablePersistence) {
        storeMode(storageKey, newMode);
      }
    },
    [disablePersistence, storageKey]
  );

  // Toggle between light and dark
  const toggleTheme = useCallback(() => {
    const newMode = resolvedMode === 'light' ? 'dark' : 'light';
    setMode(newMode);
  }, [resolvedMode, setMode]);

  const value = useMemo<ThemeContextValue>(
    () => ({
      theme,
      mode,
      resolvedMode,
      setMode,
      toggleTheme,
      isReady,
    }),
    [theme, mode, resolvedMode, setMode, toggleTheme, isReady]
  );

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

/**
 * Script to prevent flash of wrong theme
 * Add this to your HTML head before any stylesheets
 */
export function getThemeScript(
  storageKey = THEME_STORAGE_KEY,
  attribute: 'class' | 'data-theme' = 'class'
): string {
  return `
(function() {
  try {
    var mode = localStorage.getItem('${storageKey}');
    var resolved = mode;
    if (!mode || mode === 'system') {
      resolved = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    var root = document.documentElement;
    if ('${attribute}' === 'class') {
      root.classList.add(resolved);
    } else {
      root.setAttribute('data-theme', resolved);
    }
    root.style.colorScheme = resolved;
  } catch (e) {}
})();
`.trim();
}

/**
 * Component to inject theme script in head
 */
export function ThemeScript({
  storageKey,
  attribute,
}: {
  storageKey?: string;
  attribute?: 'class' | 'data-theme';
}) {
  return (
    <script
      dangerouslySetInnerHTML={{
        __html: getThemeScript(storageKey, attribute),
      }}
    />
  );
}
