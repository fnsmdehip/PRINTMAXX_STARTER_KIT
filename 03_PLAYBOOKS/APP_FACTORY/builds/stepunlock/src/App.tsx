import React, { useEffect, useState } from 'react';
import { StatusBar, ActivityIndicator, View, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { GestureHandlerRootView } from 'react-native-gesture-handler';

import { OnboardingScreen } from './screens/OnboardingScreen';
import { HomeScreen } from './screens/HomeScreen';
import { ProgressScreen } from './screens/ProgressScreen';
import { SettingsScreen } from './screens/SettingsScreen';
import { PaywallScreen } from './screens/PaywallScreen';
import { EmergencyUnlockScreen } from './screens/EmergencyUnlockScreen';

import { useUserStore } from './stores/userStore';
import { useStepStore } from './stores/stepStore';
import { initializeSubscriptions } from './services/subscriptionService';
import { COLORS } from './utils/constants';
import { RootStackParamList, MainTabParamList } from './types';

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<MainTabParamList>();

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: true,
        tabBarActiveTintColor: COLORS.primary,
        tabBarInactiveTintColor: COLORS.textSecondary,
        tabBarStyle: {
          backgroundColor: COLORS.surface,
          borderTopColor: COLORS.border,
        },
        headerStyle: {
          backgroundColor: COLORS.surface,
        },
        headerTitleStyle: {
          color: COLORS.text,
          fontWeight: '600',
        },
      }}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          title: 'Today',
          tabBarIcon: ({ color }) => (
            <TabIcon icon="🚶" color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Progress"
        component={ProgressScreen}
        options={{
          title: 'Progress',
          tabBarIcon: ({ color }) => (
            <TabIcon icon="📊" color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Settings"
        component={SettingsScreen}
        options={{
          title: 'Settings',
          tabBarIcon: ({ color }) => (
            <TabIcon icon="⚙️" color={color} />
          ),
        }}
      />
    </Tab.Navigator>
  );
}

function TabIcon({ icon }: { icon: string; color: string }) {
  return <View style={styles.tabIcon}><View><>{icon}</></View></View>;
}

export default function App() {
  const [isLoading, setIsLoading] = useState(true);

  const { settings, checkTrialStatus } = useUserStore();
  const { refreshSteps } = useStepStore();

  useEffect(() => {
    async function initialize() {
      try {
        // Initialize RevenueCat
        await initializeSubscriptions();

        // Check trial status
        checkTrialStatus();

        // Refresh steps for today
        refreshSteps();
      } catch (error) {
        console.error('Initialization error:', error);
      } finally {
        setIsLoading(false);
      }
    }

    initialize();
  }, [checkTrialStatus, refreshSteps]);

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  return (
    <GestureHandlerRootView style={styles.container}>
      <SafeAreaProvider>
        <StatusBar barStyle="dark-content" backgroundColor={COLORS.background} />
        <NavigationContainer>
          <Stack.Navigator
            screenOptions={{
              headerShown: false,
            }}
          >
            {!settings.hasCompletedOnboarding ? (
              <Stack.Screen name="Onboarding">
                {(props) => (
                  <OnboardingScreen
                    {...props}
                    onComplete={() => {
                      // Navigation will automatically update when hasCompletedOnboarding changes
                    }}
                  />
                )}
              </Stack.Screen>
            ) : (
              <>
                <Stack.Screen name="Main" component={MainTabs} />
                <Stack.Screen
                  name="Paywall"
                  component={PaywallScreen}
                  options={{
                    presentation: 'modal',
                  }}
                />
                <Stack.Screen
                  name="EmergencyUnlock"
                  component={EmergencyUnlockScreen}
                  options={{
                    presentation: 'modal',
                    headerShown: true,
                    headerTitle: '',
                    headerBackTitle: 'Back',
                  }}
                />
              </>
            )}
          </Stack.Navigator>
        </NavigationContainer>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.background,
  },
  tabIcon: {
    fontSize: 20,
  },
});
