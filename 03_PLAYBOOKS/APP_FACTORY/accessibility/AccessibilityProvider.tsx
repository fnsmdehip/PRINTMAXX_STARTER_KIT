import React, {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
  useMemo,
  ReactNode,
} from 'react';
import {
  AccessibilityInfo,
  useWindowDimensions,
  Appearance,
  ColorSchemeName,
  Platform,
  StyleSheet,
} from 'react-native';

// Types
interface AccessibilityContextValue {
  // Screen reader
  screenReaderEnabled: boolean;

  // Motion
  reduceMotionEnabled: boolean;

  // Font scaling
  fontScale: number;
  isLargeFontScale: boolean;
  isExtraLargeFontScale: boolean;

  // Visual preferences
  boldTextEnabled: boolean;
  highContrastEnabled: boolean;

  // Color scheme
  colorScheme: ColorSchemeName;
  isDarkMode: boolean;

  // Computed styles
  animationDuration: number;
  shouldAnimate: boolean;

  // Actions
  announce: (message: string) => void;
  announceUrgent: (message: string) => void;
}

interface AccessibilityProviderProps {
  children: ReactNode;

  // Optional overrides for testing
  forceReduceMotion?: boolean;
  forceHighContrast?: boolean;
  forceDarkMode?: boolean;
}

// Default context value
const defaultValue: AccessibilityContextValue = {
  screenReaderEnabled: false,
  reduceMotionEnabled: false,
  fontScale: 1,
  isLargeFontScale: false,
  isExtraLargeFontScale: false,
  boldTextEnabled: false,
  highContrastEnabled: false,
  colorScheme: 'light',
  isDarkMode: false,
  animationDuration: 300,
  shouldAnimate: true,
  announce: () => {},
  announceUrgent: () => {},
};

// Context
const AccessibilityContext = createContext<AccessibilityContextValue>(defaultValue);

// Provider component
export function AccessibilityProvider({
  children,
  forceReduceMotion,
  forceHighContrast,
  forceDarkMode,
}: AccessibilityProviderProps) {
  const { fontScale } = useWindowDimensions();

  // State
  const [screenReaderEnabled, setScreenReaderEnabled] = useState(false);
  const [reduceMotionEnabled, setReduceMotionEnabled] = useState(forceReduceMotion ?? false);
  const [boldTextEnabled, setBoldTextEnabled] = useState(false);
  const [colorScheme, setColorScheme] = useState<ColorSchemeName>(
    forceDarkMode ? 'dark' : Appearance.getColorScheme()
  );

  // Load initial values
  useEffect(() => {
    async function loadSettings() {
      const [screenReader, reduceMotion, boldText] = await Promise.all([
        AccessibilityInfo.isScreenReaderEnabled(),
        AccessibilityInfo.isReduceMotionEnabled(),
        Platform.OS === 'ios'
          ? AccessibilityInfo.isBoldTextEnabled()
          : Promise.resolve(false),
      ]);

      setScreenReaderEnabled(screenReader);
      if (forceReduceMotion === undefined) {
        setReduceMotionEnabled(reduceMotion);
      }
      setBoldTextEnabled(boldText);
    }

    loadSettings();
  }, [forceReduceMotion]);

  // Subscribe to changes
  useEffect(() => {
    const subscriptions = [
      AccessibilityInfo.addEventListener('screenReaderChanged', setScreenReaderEnabled),
      AccessibilityInfo.addEventListener('reduceMotionChanged', (enabled) => {
        if (forceReduceMotion === undefined) {
          setReduceMotionEnabled(enabled);
        }
      }),
    ];

    if (Platform.OS === 'ios') {
      subscriptions.push(
        AccessibilityInfo.addEventListener('boldTextChanged', setBoldTextEnabled)
      );
    }

    const colorSchemeSubscription = Appearance.addChangeListener(({ colorScheme: scheme }) => {
      if (forceDarkMode === undefined) {
        setColorScheme(scheme);
      }
    });

    return () => {
      subscriptions.forEach((sub) => sub.remove());
      colorSchemeSubscription.remove();
    };
  }, [forceReduceMotion, forceDarkMode]);

  // Announcement helpers
  const announce = useCallback((message: string) => {
    AccessibilityInfo.announceForAccessibility(message);
  }, []);

  const announceUrgent = useCallback((message: string) => {
    if (Platform.OS === 'ios') {
      AccessibilityInfo.announceForAccessibilityWithOptions?.(message, {
        queue: false,
      }) || AccessibilityInfo.announceForAccessibility(message);
    } else {
      AccessibilityInfo.announceForAccessibility(message);
    }
  }, []);

  // Computed values
  const value = useMemo<AccessibilityContextValue>(() => {
    const effectiveReduceMotion = forceReduceMotion ?? reduceMotionEnabled;
    const effectiveHighContrast = forceHighContrast ?? false;
    const effectiveDarkMode = forceDarkMode ?? colorScheme === 'dark';

    return {
      screenReaderEnabled,
      reduceMotionEnabled: effectiveReduceMotion,
      fontScale,
      isLargeFontScale: fontScale > 1.3,
      isExtraLargeFontScale: fontScale > 1.5,
      boldTextEnabled,
      highContrastEnabled: effectiveHighContrast,
      colorScheme: effectiveDarkMode ? 'dark' : 'light',
      isDarkMode: effectiveDarkMode,
      animationDuration: effectiveReduceMotion ? 0 : 300,
      shouldAnimate: !effectiveReduceMotion,
      announce,
      announceUrgent,
    };
  }, [
    screenReaderEnabled,
    reduceMotionEnabled,
    fontScale,
    boldTextEnabled,
    colorScheme,
    forceReduceMotion,
    forceHighContrast,
    forceDarkMode,
    announce,
    announceUrgent,
  ]);

  return (
    <AccessibilityContext.Provider value={value}>
      {children}
    </AccessibilityContext.Provider>
  );
}

// Hook to use accessibility context
export function useAccessibilityContext(): AccessibilityContextValue {
  const context = useContext(AccessibilityContext);

  if (context === undefined) {
    throw new Error('useAccessibilityContext must be used within AccessibilityProvider');
  }

  return context;
}

// Convenience hooks
export function useReduceMotion(): boolean {
  const { reduceMotionEnabled } = useAccessibilityContext();
  return reduceMotionEnabled;
}

export function useAnimationDuration(defaultDuration: number = 300): number {
  const { shouldAnimate } = useAccessibilityContext();
  return shouldAnimate ? defaultDuration : 0;
}

export function useAccessibleFontSize(baseSize: number): number {
  const { fontScale, isExtraLargeFontScale } = useAccessibilityContext();

  // Cap at 1.5x for layout stability, but still scale somewhat
  const cappedScale = isExtraLargeFontScale ? 1.5 : fontScale;
  return baseSize * cappedScale;
}

// Higher-order component for class components
export function withAccessibility<P extends object>(
  WrappedComponent: React.ComponentType<P & { accessibility: AccessibilityContextValue }>
) {
  return function WithAccessibilityComponent(props: P) {
    const accessibility = useAccessibilityContext();
    return <WrappedComponent {...props} accessibility={accessibility} />;
  };
}

// Utility: Generate responsive styles based on accessibility settings
export function useAccessibleStyles<T extends StyleSheet.NamedStyles<T>>(
  stylesFn: (context: AccessibilityContextValue) => T
): T {
  const context = useAccessibilityContext();
  return useMemo(() => stylesFn(context), [stylesFn, context]);
}

// Usage examples and documentation
/*
// 1. Wrap your app with the provider
function App() {
  return (
    <AccessibilityProvider>
      <NavigationContainer>
        <RootNavigator />
      </NavigationContainer>
    </AccessibilityProvider>
  );
}

// 2. Use the context in components
function AnimatedCard() {
  const { shouldAnimate, animationDuration, announce } = useAccessibilityContext();

  const handlePress = () => {
    // Do something
    announce('Item added to cart');
  };

  return (
    <Animated.View
      style={{
        transform: shouldAnimate
          ? [{ scale: animatedValue }]
          : [],
      }}
    />
  );
}

// 3. Use convenience hooks
function MyComponent() {
  const reduceMotion = useReduceMotion();
  const duration = useAnimationDuration(500);

  return (
    <View>
      <Animated.View
        style={{
          opacity: reduceMotion ? 1 : animatedOpacity,
        }}
      />
    </View>
  );
}

// 4. Responsive font sizes
function TextComponent() {
  const fontSize = useAccessibleFontSize(16);

  return (
    <Text style={{ fontSize }}>
      This text scales with system font size
    </Text>
  );
}

// 5. Dynamic styles
function StyledComponent() {
  const styles = useAccessibleStyles(({ isDarkMode, boldTextEnabled }) =>
    StyleSheet.create({
      container: {
        backgroundColor: isDarkMode ? '#1C1C1E' : '#FFFFFF',
      },
      text: {
        fontWeight: boldTextEnabled ? '700' : '400',
      },
    })
  );

  return (
    <View style={styles.container}>
      <Text style={styles.text}>Dynamic styles</Text>
    </View>
  );
}

// 6. Testing with forced settings
function TestApp() {
  return (
    <AccessibilityProvider
      forceReduceMotion={true}
      forceHighContrast={true}
      forceDarkMode={true}
    >
      <App />
    </AccessibilityProvider>
  );
}
*/
