import 'react-native-reanimated';
import 'react-native-gesture-handler';
import React, { useEffect } from 'react';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { StyleSheet } from 'react-native';
import { AppNavigator } from './src/navigation/AppNavigator';
import { initSounds, cleanupSounds } from './src/sounds/SoundEngine';

export default function App() {
  useEffect(() => {
    initSounds();
    return () => { cleanupSounds(); };
  }, []);

  return (
    <GestureHandlerRootView style={styles.root}>
      <AppNavigator />
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
  },
});
