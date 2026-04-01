import 'react-native-gesture-handler';
import React from 'react';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { StyleSheet } from 'react-native';
import { AppNavigator } from './src/navigation/AppNavigator';

// Note: react-native-reanimated requires a development build (not Expo Go)
// for SDK 54. Animations will be static in Expo Go but work in dev builds.
try {
  require('react-native-reanimated');
} catch {}

export default function App() {
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
