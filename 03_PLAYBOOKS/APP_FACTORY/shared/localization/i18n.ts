/**
 * Core i18n setup for app localization
 * Type-safe internationalization with language detection, fallbacks, and formatting
 */

import { Platform, NativeModules } from 'react-native';

// Supported language codes
export const SUPPORTED_LANGUAGES = ['en', 'es', 'pt', 'fr', 'de'] as const;
export type SupportedLanguage = (typeof SUPPORTED_LANGUAGES)[number];

export const DEFAULT_LANGUAGE: SupportedLanguage = 'en';

// Language metadata
export const LANGUAGE_META: Record<SupportedLanguage, { name: string; nativeName: string; rtl: boolean }> = {
  en: { name: 'English', nativeName: 'English', rtl: false },
  es: { name: 'Spanish', nativeName: 'Español', rtl: false },
  pt: { name: 'Portuguese', nativeName: 'Português', rtl: false },
  fr: { name: 'French', nativeName: 'Français', rtl: false },
  de: { name: 'German', nativeName: 'Deutsch', rtl: false },
};

// Translation namespaces
export type TranslationNamespace = 'common' | 'onboarding' | 'settings' | 'subscription' | 'notifications';

// Plural categories (CLDR)
export type PluralCategory = 'zero' | 'one' | 'two' | 'few' | 'many' | 'other';

// Translation value types
export type TranslationValue = string | { [K in PluralCategory]?: string };

// Nested translation object type
export interface TranslationObject {
  [key: string]: TranslationValue | TranslationObject;
}

// Translation store type
type TranslationStore = {
  [L in SupportedLanguage]?: {
    [N in TranslationNamespace]?: TranslationObject;
  };
};

// Global translation store
let translations: TranslationStore = {};
let currentLanguage: SupportedLanguage = DEFAULT_LANGUAGE;
let isInitialized = false;

/**
 * Detect device language
 * Returns the device's preferred language, falling back to default
 */
export function detectDeviceLanguage(): SupportedLanguage {
  let deviceLanguage: string | undefined;

  try {
    if (Platform.OS === 'ios') {
      deviceLanguage =
        NativeModules.SettingsManager?.settings?.AppleLocale ||
        NativeModules.SettingsManager?.settings?.AppleLanguages?.[0];
    } else if (Platform.OS === 'android') {
      deviceLanguage = NativeModules.I18nManager?.localeIdentifier;
    }
  } catch {
    // Fallback handled below
  }

  if (!deviceLanguage) {
    return DEFAULT_LANGUAGE;
  }

  // Extract language code (e.g., "en_US" -> "en", "pt-BR" -> "pt")
  const languageCode = deviceLanguage.split(/[-_]/)[0].toLowerCase();

  // Check if supported
  if (SUPPORTED_LANGUAGES.includes(languageCode as SupportedLanguage)) {
    return languageCode as SupportedLanguage;
  }

  return DEFAULT_LANGUAGE;
}

/**
 * Load translations for a specific language and namespace
 */
export async function loadTranslations(
  language: SupportedLanguage,
  namespace: TranslationNamespace
): Promise<TranslationObject> {
  try {
    // Dynamic import based on language and namespace
    const module = await import(`./translations/${language}/${namespace}.json`);
    return module.default || module;
  } catch (error) {
    console.warn(`Failed to load translations for ${language}/${namespace}:`, error);

    // Try fallback to default language
    if (language !== DEFAULT_LANGUAGE) {
      try {
        const fallbackModule = await import(`./translations/${DEFAULT_LANGUAGE}/${namespace}.json`);
        return fallbackModule.default || fallbackModule;
      } catch {
        console.error(`Failed to load fallback translations for ${DEFAULT_LANGUAGE}/${namespace}`);
      }
    }

    return {};
  }
}

/**
 * Initialize i18n with all namespaces for a language
 */
export async function initializeI18n(language?: SupportedLanguage): Promise<void> {
  const targetLanguage = language || detectDeviceLanguage();

  // Load all namespaces in parallel
  const namespaces: TranslationNamespace[] = ['common', 'onboarding', 'settings', 'subscription', 'notifications'];

  const loadPromises = namespaces.map(async (namespace) => {
    const data = await loadTranslations(targetLanguage, namespace);
    return { namespace, data };
  });

  const results = await Promise.all(loadPromises);

  // Initialize translation store for language
  if (!translations[targetLanguage]) {
    translations[targetLanguage] = {};
  }

  // Populate translations
  for (const { namespace, data } of results) {
    translations[targetLanguage]![namespace] = data;
  }

  currentLanguage = targetLanguage;
  isInitialized = true;
}

/**
 * Get current language
 */
export function getCurrentLanguage(): SupportedLanguage {
  return currentLanguage;
}

/**
 * Set current language
 */
export async function setLanguage(language: SupportedLanguage): Promise<void> {
  if (!SUPPORTED_LANGUAGES.includes(language)) {
    console.warn(`Unsupported language: ${language}, using default`);
    language = DEFAULT_LANGUAGE;
  }

  // Load translations if not already loaded
  if (!translations[language]) {
    await initializeI18n(language);
  }

  currentLanguage = language;
}

/**
 * Get plural category for a number based on language rules
 * Implements CLDR plural rules for supported languages
 */
export function getPluralCategory(count: number, language: SupportedLanguage = currentLanguage): PluralCategory {
  const absCount = Math.abs(count);

  switch (language) {
    case 'en':
    case 'de':
    case 'pt':
      // English/German/Portuguese: 1 = one, else other
      return absCount === 1 ? 'one' : 'other';

    case 'fr':
      // French: 0-1 = one, else other
      return absCount <= 1 ? 'one' : 'other';

    case 'es':
      // Spanish: 1 = one, else other
      return absCount === 1 ? 'one' : 'other';

    default:
      return absCount === 1 ? 'one' : 'other';
  }
}

/**
 * Resolve a nested key path to a translation value
 */
function resolveKeyPath(obj: TranslationObject, keyPath: string): TranslationValue | undefined {
  const keys = keyPath.split('.');
  let current: TranslationObject | TranslationValue = obj;

  for (const key of keys) {
    if (current === undefined || current === null || typeof current === 'string') {
      return undefined;
    }
    current = (current as TranslationObject)[key];
  }

  return current as TranslationValue;
}

/**
 * Interpolate variables into a translation string
 * Supports {{variable}} syntax
 */
function interpolate(text: string, variables?: Record<string, string | number>): string {
  if (!variables) return text;

  return text.replace(/\{\{(\w+)\}\}/g, (match, key) => {
    return variables[key] !== undefined ? String(variables[key]) : match;
  });
}

/**
 * Main translation function
 */
export function t(
  key: string,
  options?: {
    namespace?: TranslationNamespace;
    count?: number;
    variables?: Record<string, string | number>;
    defaultValue?: string;
  }
): string {
  const {
    namespace = 'common',
    count,
    variables,
    defaultValue = key,
  } = options || {};

  if (!isInitialized) {
    console.warn('i18n not initialized, returning key');
    return defaultValue;
  }

  const langTranslations = translations[currentLanguage];
  if (!langTranslations) {
    return interpolate(defaultValue, variables);
  }

  const nsTranslations = langTranslations[namespace];
  if (!nsTranslations) {
    return interpolate(defaultValue, variables);
  }

  const value = resolveKeyPath(nsTranslations, key);

  if (value === undefined) {
    // Try fallback language
    const fallbackTranslations = translations[DEFAULT_LANGUAGE]?.[namespace];
    if (fallbackTranslations) {
      const fallbackValue = resolveKeyPath(fallbackTranslations, key);
      if (fallbackValue !== undefined) {
        return resolveTranslationValue(fallbackValue, count, variables, defaultValue);
      }
    }
    return interpolate(defaultValue, variables);
  }

  return resolveTranslationValue(value, count, variables, defaultValue);
}

/**
 * Resolve a translation value, handling plurals
 */
function resolveTranslationValue(
  value: TranslationValue,
  count: number | undefined,
  variables: Record<string, string | number> | undefined,
  defaultValue: string
): string {
  if (typeof value === 'string') {
    return interpolate(value, variables);
  }

  // Handle plural forms
  if (count !== undefined) {
    const category = getPluralCategory(count);
    const pluralValue = value[category] || value.other;

    if (pluralValue) {
      // Auto-inject count variable
      const varsWithCount = { ...variables, count };
      return interpolate(pluralValue, varsWithCount);
    }
  }

  // Fallback to 'other' form or default
  if (value.other) {
    return interpolate(value.other, variables);
  }

  return interpolate(defaultValue, variables);
}

// Date and number formatting

/**
 * Format a date according to current language settings
 */
export function formatDate(
  date: Date,
  options?: Intl.DateTimeFormatOptions
): string {
  const locale = getLocaleCode(currentLanguage);
  return new Intl.DateTimeFormat(locale, options).format(date);
}

/**
 * Format a number according to current language settings
 */
export function formatNumber(
  value: number,
  options?: Intl.NumberFormatOptions
): string {
  const locale = getLocaleCode(currentLanguage);
  return new Intl.NumberFormat(locale, options).format(value);
}

/**
 * Format currency according to current language settings
 */
export function formatCurrency(
  value: number,
  currency: string = 'USD'
): string {
  const locale = getLocaleCode(currentLanguage);
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
  }).format(value);
}

/**
 * Format relative time (e.g., "3 days ago")
 */
export function formatRelativeTime(
  value: number,
  unit: Intl.RelativeTimeFormatUnit
): string {
  const locale = getLocaleCode(currentLanguage);
  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });
  return rtf.format(value, unit);
}

/**
 * Get the full locale code for a language
 */
function getLocaleCode(language: SupportedLanguage): string {
  const localeMap: Record<SupportedLanguage, string> = {
    en: 'en-US',
    es: 'es-ES',
    pt: 'pt-BR',
    fr: 'fr-FR',
    de: 'de-DE',
  };
  return localeMap[language];
}

/**
 * Check if current language is RTL
 */
export function isRTL(): boolean {
  return LANGUAGE_META[currentLanguage].rtl;
}

/**
 * Get all available languages with metadata
 */
export function getAvailableLanguages(): Array<{
  code: SupportedLanguage;
  name: string;
  nativeName: string;
}> {
  return SUPPORTED_LANGUAGES.map((code) => ({
    code,
    name: LANGUAGE_META[code].name,
    nativeName: LANGUAGE_META[code].nativeName,
  }));
}

// Type-safe translation key helpers for IDE support

/**
 * Create a namespace-bound translation function
 */
export function createNamespacedT(namespace: TranslationNamespace) {
  return (
    key: string,
    options?: Omit<Parameters<typeof t>[1], 'namespace'>
  ) => t(key, { ...options, namespace });
}
