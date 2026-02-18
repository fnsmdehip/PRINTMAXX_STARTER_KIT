import { useEffect } from 'react';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { Redirect } from 'expo-router';
import { useOnboardingStore } from '../src/stores/onboardingStore';
import { colors } from '../src/utils/theme';

export default function Index() {
  const onboardingCompleted = useOnboardingStore((state) => state.onboardingCompleted);

  // Show loading state while checking onboarding status
  if (onboardingCompleted === undefined) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  // Route based on onboarding status
  if (!onboardingCompleted) {
    return <Redirect href="/onboarding" />;
  }

  return <Redirect href="/(tabs)/home" />;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.background,
  },
});
