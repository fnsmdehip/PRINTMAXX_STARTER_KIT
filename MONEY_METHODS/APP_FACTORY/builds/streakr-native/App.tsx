import React, { useEffect, useState } from 'react';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import * as SplashScreen from 'expo-splash-screen';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { StatusBar } from 'expo-status-bar';
import { getSettings } from './src/services/storage';
import { Colors } from './src/constants/theme';

// Keep splash visible while loading
SplashScreen.preventAutoHideAsync();

// Lazy-load navigation to avoid initialization errors during splash
const Navigation = React.lazy(() => import('./src/navigation'));

export default function App() {
  const [ready, setReady] = useState(false);
  const [initialRoute, setInitialRoute] = useState<'Onboarding' | 'Main'>('Onboarding');

  useEffect(() => {
    async function init() {
      try {
        const settings = await getSettings();
        setInitialRoute(settings.onboardingComplete ? 'Main' : 'Onboarding');
      } catch {
        setInitialRoute('Onboarding');
      } finally {
        setReady(true);
        await SplashScreen.hideAsync();
      }
    }
    init();
  }, []);

  if (!ready) {
    return (
      <View style={s.splash}>
        <ActivityIndicator color={Colors.emerald} />
      </View>
    );
  }

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <StatusBar style="dark" />
      <React.Suspense fallback={<View style={s.splash} />}>
        <Navigation />
      </React.Suspense>
    </GestureHandlerRootView>
  );
}

const s = StyleSheet.create({
  splash: { flex: 1, backgroundColor: Colors.bgDeep, alignItems: 'center', justifyContent: 'center' },
});
