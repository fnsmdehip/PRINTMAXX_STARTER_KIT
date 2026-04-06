import React, { useEffect, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StatusBar } from 'expo-status-bar';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { colors } from '../theme';
import { getProfile } from '../store';
import { DetectionMode, DetectionResult } from '../utils/types';

import OnboardingScreen from '../screens/OnboardingScreen';
import HomeScreen from '../screens/HomeScreen';
import DetectionScreen from '../screens/DetectionScreen';
import { ResultScreen } from '../screens/ResultScreen';
import { SettingsScreen } from '../screens/SettingsScreen';
import PartyModeScreen from '../screens/PartyModeScreen';

export type RootStackParamList = {
  Onboarding: undefined;
  Home: undefined;
  Detection: { mode?: DetectionMode };
  Result: { result: DetectionResult };
  Settings: undefined;
  PartyMode: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export function AppNavigator() {
  const [isLoading, setIsLoading] = useState(true);
  const [hasOnboarded, setHasOnboarded] = useState(false);

  useEffect(() => {
    checkOnboarding();
  }, []);

  const checkOnboarding = async () => {
    try {
      const profile = await getProfile();
      setHasOnboarded(profile.hasCompletedOnboarding);
    } catch {
      setHasOnboarded(false);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator size="large" color={colors.accent.primary} />
        <StatusBar style="light" />
      </View>
    );
  }

  const linking = {
    prefixes: ['truthscope://'],
    config: {
      screens: {
        Onboarding: 'onboarding',
        Home: 'home',
        Detection: 'detection/:mode?',
        Result: 'result',
        Settings: 'settings',
        PartyMode: 'party',
      },
    },
  };

  return (
    <NavigationContainer linking={linking}>
      <StatusBar style="light" />
      <Stack.Navigator
        initialRouteName={hasOnboarded ? 'Home' : 'Onboarding'}
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: colors.bg.primary },
          animation: 'slide_from_right',
        }}
      >
        <Stack.Screen name="Onboarding" component={OnboardingScreen} />
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Detection" component={DetectionScreen} />
        <Stack.Screen name="Result" component={ResultScreen} />
        <Stack.Screen name="Settings" component={SettingsScreen} />
        <Stack.Screen
          name="PartyMode"
          component={PartyModeScreen}
          options={{ animation: 'slide_from_bottom' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  loading: {
    flex: 1,
    backgroundColor: colors.bg.primary,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
