import React, { useEffect } from 'react';
import { useRouter } from 'expo-router';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { useUserStore } from '../src/stores/userStore';
import { COLORS } from '../src/utils/constants';
import HomeScreen from '../src/screens/HomeScreen';

export default function Index() {
  const router = useRouter();
  const { isOnboardingComplete, isLoading } = useUserStore();

  useEffect(() => {
    if (!isLoading && !isOnboardingComplete) {
      router.replace('/onboarding');
    }
  }, [isLoading, isOnboardingComplete]);

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  if (!isOnboardingComplete) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  return <HomeScreen />;
}

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.background,
  },
});
