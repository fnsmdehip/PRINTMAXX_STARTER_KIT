import React, { useEffect, useState } from 'react';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import * as SplashScreen from 'expo-splash-screen';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { StatusBar } from 'expo-status-bar';
import { getSettings } from './src/services/storage';
import { Colors } from './src/constants/theme';
import Navigation from './src/navigation';

// Keep splash visible while loading
SplashScreen.preventAutoHideAsync();

export default function App() {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    async function init() {
      try {
        await getSettings(); // warm storage cache
      } catch { /* non-critical */ } finally {
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
      <Navigation />
    </GestureHandlerRootView>
  );
}

const s = StyleSheet.create({
  splash: { flex: 1, backgroundColor: Colors.bgDeep, alignItems: 'center', justifyContent: 'center' },
});
