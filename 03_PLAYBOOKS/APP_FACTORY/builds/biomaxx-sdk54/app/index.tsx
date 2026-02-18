import { useEffect } from 'react';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { Redirect } from 'expo-router';
import { useUserStore } from '../src/stores/userStore';
import { COLORS } from '../src/utils/constants';

export default function Index() {
  const user = useUserStore((state) => state.user);
  const checkAndUpdateStreak = useUserStore((state) => state.checkAndUpdateStreak);

  useEffect(() => {
    if (user?.onboardingComplete) {
      checkAndUpdateStreak();
    }
  }, [user?.onboardingComplete, checkAndUpdateStreak]);

  // Show loading state while checking auth
  if (user === undefined) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  // Route based on onboarding status
  if (!user?.onboardingComplete) {
    return <Redirect href="/onboarding" />;
  }

  return <Redirect href="/(tabs)/dashboard" />;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.background,
  },
});
