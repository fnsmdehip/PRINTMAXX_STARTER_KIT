import { useEffect, useState } from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import * as SplashScreen from 'expo-splash-screen';
import { useSettingsStore, useHabitStore, useJournalStore } from '../src/store';
import { COLORS } from '../src/utils/constants';

// Prevent the splash screen from auto-hiding before asset loading is complete
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const [isReady, setIsReady] = useState(false);
  const { loadFromStorage: loadSettings } = useSettingsStore();
  const { loadFromStorage: loadHabits } = useHabitStore();
  const { loadFromStorage: loadJournal } = useJournalStore();

  useEffect(() => {
    async function prepare() {
      try {
        // Load all stored data
        await Promise.all([loadSettings(), loadHabits(), loadJournal()]);
      } catch (e) {
        console.warn('Error loading data:', e);
      } finally {
        setIsReady(true);
        await SplashScreen.hideAsync();
      }
    }

    prepare();
  }, [loadSettings, loadHabits, loadJournal]);

  if (!isReady) {
    return null;
  }

  return (
    <SafeAreaProvider>
      <StatusBar style="dark" backgroundColor={COLORS.background} />
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="(tabs)" />
        <Stack.Screen name="onboarding" options={{ presentation: 'modal' }} />
        <Stack.Screen name="paywall" options={{ presentation: 'modal' }} />
        <Stack.Screen name="privacy" />
        <Stack.Screen name="terms" />
      </Stack>
    </SafeAreaProvider>
  );
}
