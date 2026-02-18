import { useEffect, useState, useCallback } from 'react';
import {
  AccessibilityInfo,
  useWindowDimensions,
  Appearance,
  Platform,
  NativeEventSubscription,
} from 'react-native';

interface AccessibilityState {
  // Screen reader
  screenReaderEnabled: boolean;

  // Motion preferences
  reduceMotionEnabled: boolean;

  // Visual preferences
  boldTextEnabled: boolean;
  grayscaleEnabled: boolean;
  invertColorsEnabled: boolean;
  reduceTransparencyEnabled: boolean;

  // Font scaling
  fontScale: number;
  isLargeFontScale: boolean; // > 1.3
  isExtraLargeFontScale: boolean; // > 1.5

  // Color scheme
  colorScheme: 'light' | 'dark' | null;
  prefersHighContrast: boolean;

  // Platform
  isIOS: boolean;
  isAndroid: boolean;
}

interface AccessibilityActions {
  // Focus management
  setFocus: (nodeHandle: number | null) => void;

  // Announcements
  announce: (message: string) => void;
  announceUrgent: (message: string) => void;
}

interface UseAccessibilityReturn extends AccessibilityState, AccessibilityActions {
  // Loading state
  isLoading: boolean;
}

export function useAccessibility(): UseAccessibilityReturn {
  const { fontScale } = useWindowDimensions();

  const [isLoading, setIsLoading] = useState(true);
  const [screenReaderEnabled, setScreenReaderEnabled] = useState(false);
  const [reduceMotionEnabled, setReduceMotionEnabled] = useState(false);
  const [boldTextEnabled, setBoldTextEnabled] = useState(false);
  const [grayscaleEnabled, setGrayscaleEnabled] = useState(false);
  const [invertColorsEnabled, setInvertColorsEnabled] = useState(false);
  const [reduceTransparencyEnabled, setReduceTransparencyEnabled] = useState(false);
  const [colorScheme, setColorScheme] = useState<'light' | 'dark' | null>(
    Appearance.getColorScheme()
  );

  // Initial load of all accessibility settings
  useEffect(() => {
    async function loadAccessibilitySettings() {
      try {
        const [
          screenReader,
          reduceMotion,
          boldText,
          grayscale,
          invertColors,
          reduceTransparency,
        ] = await Promise.all([
          AccessibilityInfo.isScreenReaderEnabled(),
          AccessibilityInfo.isReduceMotionEnabled(),
          Platform.OS === 'ios'
            ? AccessibilityInfo.isBoldTextEnabled()
            : Promise.resolve(false),
          Platform.OS === 'ios'
            ? AccessibilityInfo.isGrayscaleEnabled()
            : Promise.resolve(false),
          Platform.OS === 'ios'
            ? AccessibilityInfo.isInvertColorsEnabled()
            : Promise.resolve(false),
          Platform.OS === 'ios'
            ? AccessibilityInfo.isReduceTransparencyEnabled()
            : Promise.resolve(false),
        ]);

        setScreenReaderEnabled(screenReader);
        setReduceMotionEnabled(reduceMotion);
        setBoldTextEnabled(boldText);
        setGrayscaleEnabled(grayscale);
        setInvertColorsEnabled(invertColors);
        setReduceTransparencyEnabled(reduceTransparency);
      } catch (error) {
        console.warn('Failed to load accessibility settings:', error);
      } finally {
        setIsLoading(false);
      }
    }

    loadAccessibilitySettings();
  }, []);

  // Subscribe to accessibility changes
  useEffect(() => {
    const subscriptions: NativeEventSubscription[] = [];

    // Screen reader changes
    subscriptions.push(
      AccessibilityInfo.addEventListener(
        'screenReaderChanged',
        setScreenReaderEnabled
      )
    );

    // Reduce motion changes
    subscriptions.push(
      AccessibilityInfo.addEventListener(
        'reduceMotionChanged',
        setReduceMotionEnabled
      )
    );

    // iOS-only listeners
    if (Platform.OS === 'ios') {
      subscriptions.push(
        AccessibilityInfo.addEventListener(
          'boldTextChanged',
          setBoldTextEnabled
        )
      );

      subscriptions.push(
        AccessibilityInfo.addEventListener(
          'grayscaleChanged',
          setGrayscaleEnabled
        )
      );

      subscriptions.push(
        AccessibilityInfo.addEventListener(
          'invertColorsChanged',
          setInvertColorsEnabled
        )
      );

      subscriptions.push(
        AccessibilityInfo.addEventListener(
          'reduceTransparencyChanged',
          setReduceTransparencyEnabled
        )
      );
    }

    // Color scheme changes
    const colorSchemeSubscription = Appearance.addChangeListener(
      ({ colorScheme: newColorScheme }) => {
        setColorScheme(newColorScheme);
      }
    );

    return () => {
      subscriptions.forEach((sub) => sub.remove());
      colorSchemeSubscription.remove();
    };
  }, []);

  // Focus management
  const setFocus = useCallback((nodeHandle: number | null) => {
    if (nodeHandle) {
      AccessibilityInfo.setAccessibilityFocus(nodeHandle);
    }
  }, []);

  // Announcement helpers
  const announce = useCallback((message: string) => {
    AccessibilityInfo.announceForAccessibility(message);
  }, []);

  const announceUrgent = useCallback((message: string) => {
    // Use queue: false to interrupt current speech (iOS 16+)
    if (Platform.OS === 'ios') {
      AccessibilityInfo.announceForAccessibilityWithOptions?.(message, {
        queue: false,
      }) || AccessibilityInfo.announceForAccessibility(message);
    } else {
      AccessibilityInfo.announceForAccessibility(message);
    }
  }, []);

  return {
    // Loading
    isLoading,

    // Screen reader
    screenReaderEnabled,

    // Motion
    reduceMotionEnabled,

    // Visual
    boldTextEnabled,
    grayscaleEnabled,
    invertColorsEnabled,
    reduceTransparencyEnabled,

    // Font scale
    fontScale,
    isLargeFontScale: fontScale > 1.3,
    isExtraLargeFontScale: fontScale > 1.5,

    // Color scheme
    colorScheme,
    prefersHighContrast: colorScheme === 'dark' || invertColorsEnabled,

    // Platform
    isIOS: Platform.OS === 'ios',
    isAndroid: Platform.OS === 'android',

    // Actions
    setFocus,
    announce,
    announceUrgent,
  };
}

// Simplified hooks for specific features

export function useScreenReader(): boolean {
  const [enabled, setEnabled] = useState(false);

  useEffect(() => {
    AccessibilityInfo.isScreenReaderEnabled().then(setEnabled);

    const subscription = AccessibilityInfo.addEventListener(
      'screenReaderChanged',
      setEnabled
    );

    return () => subscription.remove();
  }, []);

  return enabled;
}

export function useReduceMotion(): boolean {
  const [enabled, setEnabled] = useState(false);

  useEffect(() => {
    AccessibilityInfo.isReduceMotionEnabled().then(setEnabled);

    const subscription = AccessibilityInfo.addEventListener(
      'reduceMotionChanged',
      setEnabled
    );

    return () => subscription.remove();
  }, []);

  return enabled;
}

export function useFontScale(): {
  fontScale: number;
  isLarge: boolean;
  isExtraLarge: boolean;
} {
  const { fontScale } = useWindowDimensions();

  return {
    fontScale,
    isLarge: fontScale > 1.3,
    isExtraLarge: fontScale > 1.5,
  };
}

// Usage examples:
/*
function MyComponent() {
  const {
    screenReaderEnabled,
    reduceMotionEnabled,
    fontScale,
    isLargeFontScale,
    announce,
  } = useAccessibility();

  // Adapt animations
  const animationDuration = reduceMotionEnabled ? 0 : 300;

  // Adapt layout for large fonts
  const layout = isLargeFontScale ? 'stacked' : 'horizontal';

  // Announce dynamic changes
  const handleAddToCart = () => {
    addItemToCart();
    announce('Item added to cart');
  };

  // Show more content for screen reader users
  if (screenReaderEnabled) {
    return <DetailedView />;
  }

  return <CompactView />;
}

// Using simplified hooks
function AnimatedComponent() {
  const reduceMotion = useReduceMotion();

  return (
    <Animated.View
      style={{
        transform: reduceMotion
          ? []
          : [{ translateY: animatedValue }],
      }}
    />
  );
}
*/
