/**
 * React hook for localization
 * Provides access to translations, current language, and language switching
 */

import { useState, useEffect, useCallback, createContext, useContext, useMemo, ReactNode } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {
  t,
  initializeI18n,
  setLanguage,
  getCurrentLanguage,
  getAvailableLanguages,
  formatDate,
  formatNumber,
  formatCurrency,
  formatRelativeTime,
  isRTL,
  createNamespacedT,
  SupportedLanguage,
  TranslationNamespace,
  LANGUAGE_META,
} from './i18n';

const LANGUAGE_STORAGE_KEY = '@printmaxx_app_language';

// Localization context type
interface LocalizationContextValue {
  // Current state
  language: SupportedLanguage;
  isLoading: boolean;
  isRTL: boolean;

  // Translation functions
  t: typeof t;
  tn: (namespace: TranslationNamespace) => ReturnType<typeof createNamespacedT>;

  // Formatting functions
  formatDate: typeof formatDate;
  formatNumber: typeof formatNumber;
  formatCurrency: typeof formatCurrency;
  formatRelativeTime: typeof formatRelativeTime;

  // Language management
  changeLanguage: (language: SupportedLanguage) => Promise<void>;
  availableLanguages: ReturnType<typeof getAvailableLanguages>;
  getLanguageName: (code: SupportedLanguage) => string;
  getNativeLanguageName: (code: SupportedLanguage) => string;
}

// Create context with undefined default
const LocalizationContext = createContext<LocalizationContextValue | undefined>(undefined);

// Provider props
interface LocalizationProviderProps {
  children: ReactNode;
  initialLanguage?: SupportedLanguage;
  onLanguageChange?: (language: SupportedLanguage) => void;
}

/**
 * Localization Provider component
 * Wrap your app with this to enable localization
 */
export function LocalizationProvider({
  children,
  initialLanguage,
  onLanguageChange,
}: LocalizationProviderProps) {
  const [language, setCurrentLanguage] = useState<SupportedLanguage>(getCurrentLanguage());
  const [isLoading, setIsLoading] = useState(true);

  // Initialize i18n on mount
  useEffect(() => {
    const initialize = async () => {
      try {
        // Try to load saved language preference
        let savedLanguage: SupportedLanguage | null = null;

        try {
          const stored = await AsyncStorage.getItem(LANGUAGE_STORAGE_KEY);
          if (stored) {
            savedLanguage = stored as SupportedLanguage;
          }
        } catch {
          // Storage not available, continue with detection
        }

        // Use saved language, initial prop, or detect
        const targetLanguage = savedLanguage || initialLanguage;
        await initializeI18n(targetLanguage);

        setCurrentLanguage(getCurrentLanguage());
      } catch (error) {
        console.error('Failed to initialize i18n:', error);
      } finally {
        setIsLoading(false);
      }
    };

    initialize();
  }, [initialLanguage]);

  // Language change handler
  const changeLanguage = useCallback(
    async (newLanguage: SupportedLanguage) => {
      try {
        setIsLoading(true);
        await setLanguage(newLanguage);

        // Persist language preference
        try {
          await AsyncStorage.setItem(LANGUAGE_STORAGE_KEY, newLanguage);
        } catch {
          // Storage not available, language change still works
        }

        setCurrentLanguage(newLanguage);
        onLanguageChange?.(newLanguage);
      } catch (error) {
        console.error('Failed to change language:', error);
      } finally {
        setIsLoading(false);
      }
    },
    [onLanguageChange]
  );

  // Create namespaced translation function
  const tn = useCallback(
    (namespace: TranslationNamespace) => createNamespacedT(namespace),
    [language] // Re-create when language changes
  );

  // Helper functions
  const getLanguageName = useCallback((code: SupportedLanguage) => {
    return LANGUAGE_META[code].name;
  }, []);

  const getNativeLanguageName = useCallback((code: SupportedLanguage) => {
    return LANGUAGE_META[code].nativeName;
  }, []);

  // Memoized context value
  const contextValue = useMemo<LocalizationContextValue>(
    () => ({
      language,
      isLoading,
      isRTL: isRTL(),
      t,
      tn,
      formatDate,
      formatNumber,
      formatCurrency,
      formatRelativeTime,
      changeLanguage,
      availableLanguages: getAvailableLanguages(),
      getLanguageName,
      getNativeLanguageName,
    }),
    [language, isLoading, changeLanguage, tn, getLanguageName, getNativeLanguageName]
  );

  return (
    <LocalizationContext.Provider value={contextValue}>
      {children}
    </LocalizationContext.Provider>
  );
}

/**
 * Main hook for accessing localization
 */
export function useLocalization(): LocalizationContextValue {
  const context = useContext(LocalizationContext);

  if (!context) {
    throw new Error('useLocalization must be used within a LocalizationProvider');
  }

  return context;
}

/**
 * Hook for translations with a specific namespace
 */
export function useTranslation(namespace: TranslationNamespace = 'common') {
  const { t, language, isLoading } = useLocalization();

  // Create a namespace-bound translation function
  const translate = useCallback(
    (
      key: string,
      options?: {
        count?: number;
        variables?: Record<string, string | number>;
        defaultValue?: string;
      }
    ) => t(key, { ...options, namespace }),
    [t, namespace, language]
  );

  return {
    t: translate,
    language,
    isLoading,
  };
}

/**
 * Hook specifically for onboarding translations
 */
export function useOnboardingTranslation() {
  return useTranslation('onboarding');
}

/**
 * Hook specifically for settings translations
 */
export function useSettingsTranslation() {
  return useTranslation('settings');
}

/**
 * Hook specifically for subscription/paywall translations
 */
export function useSubscriptionTranslation() {
  return useTranslation('subscription');
}

/**
 * Hook specifically for notification translations
 */
export function useNotificationTranslation() {
  return useTranslation('notifications');
}

/**
 * Hook for number formatting with current locale
 */
export function useNumberFormat() {
  const { formatNumber, formatCurrency, language } = useLocalization();

  const format = useCallback(
    (value: number, options?: Intl.NumberFormatOptions) => formatNumber(value, options),
    [formatNumber, language]
  );

  const currency = useCallback(
    (value: number, currencyCode: string = 'USD') => formatCurrency(value, currencyCode),
    [formatCurrency, language]
  );

  const percent = useCallback(
    (value: number) =>
      formatNumber(value, { style: 'percent', maximumFractionDigits: 1 }),
    [formatNumber, language]
  );

  const compact = useCallback(
    (value: number) =>
      formatNumber(value, { notation: 'compact', maximumFractionDigits: 1 }),
    [formatNumber, language]
  );

  return { format, currency, percent, compact };
}

/**
 * Hook for date formatting with current locale
 */
export function useDateFormat() {
  const { formatDate, formatRelativeTime, language } = useLocalization();

  const date = useCallback(
    (value: Date, options?: Intl.DateTimeFormatOptions) => formatDate(value, options),
    [formatDate, language]
  );

  const shortDate = useCallback(
    (value: Date) =>
      formatDate(value, { month: 'short', day: 'numeric', year: 'numeric' }),
    [formatDate, language]
  );

  const longDate = useCallback(
    (value: Date) =>
      formatDate(value, { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' }),
    [formatDate, language]
  );

  const time = useCallback(
    (value: Date) =>
      formatDate(value, { hour: 'numeric', minute: 'numeric' }),
    [formatDate, language]
  );

  const relative = useCallback(
    (value: number, unit: Intl.RelativeTimeFormatUnit) => formatRelativeTime(value, unit),
    [formatRelativeTime, language]
  );

  const relativeFromDate = useCallback(
    (date: Date) => {
      const now = new Date();
      const diffMs = date.getTime() - now.getTime();
      const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));

      if (Math.abs(diffDays) < 1) {
        const diffHours = Math.round(diffMs / (1000 * 60 * 60));
        if (Math.abs(diffHours) < 1) {
          const diffMinutes = Math.round(diffMs / (1000 * 60));
          return formatRelativeTime(diffMinutes, 'minute');
        }
        return formatRelativeTime(diffHours, 'hour');
      }

      if (Math.abs(diffDays) < 30) {
        return formatRelativeTime(diffDays, 'day');
      }

      const diffMonths = Math.round(diffDays / 30);
      if (Math.abs(diffMonths) < 12) {
        return formatRelativeTime(diffMonths, 'month');
      }

      const diffYears = Math.round(diffDays / 365);
      return formatRelativeTime(diffYears, 'year');
    },
    [formatRelativeTime, language]
  );

  return { date, shortDate, longDate, time, relative, relativeFromDate };
}

/**
 * Hook for language switching UI
 */
export function useLanguageSwitcher() {
  const {
    language,
    availableLanguages,
    changeLanguage,
    isLoading,
    getLanguageName,
    getNativeLanguageName,
  } = useLocalization();

  return {
    currentLanguage: language,
    currentLanguageName: getLanguageName(language),
    currentNativeName: getNativeLanguageName(language),
    availableLanguages,
    changeLanguage,
    isLoading,
  };
}

// Re-export types for convenience
export type { SupportedLanguage, TranslationNamespace } from './i18n';
