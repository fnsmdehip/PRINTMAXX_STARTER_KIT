import React, { useEffect, useState, useCallback } from 'react';
import { StatusBar, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { Provider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import { Ionicons } from '@expo/vector-icons';

import { store, persistor } from './store';
import { Theme } from './utils/theme';
import { haptics } from './utils/haptics';

import SplashScreen from './screens/SplashScreen';
import OnboardingFlow from './screens/OnboardingFlow';
import HomeScreen from './screens/Home';
import AnalyticsScreen from './screens/Analytics';
import SettingsScreen from './screens/Settings';
import CameraScreen from './screens/Camera';
import PaywallScreen from './screens/Paywall';

import { setPremiumStatus } from './store/subscriptionSlice';
import { useAppSelector } from './store/hooks';
import { initPurchases, checkEntitlements } from './services/purchases';

type TabParamList = {
  Home: undefined;
  Camera: undefined;
  Analytics: undefined;
  Settings: undefined;
};

type RootStackParamList = {
  Main: undefined;
  Paywall: undefined;
};

const Tab = createBottomTabNavigator<TabParamList>();
const Stack = createStackNavigator<RootStackParamList>();

function getTabBarIcon(
  routeName: string,
  focused: boolean,
  color: string,
  size: number,
): React.ReactNode {
  let iconName: keyof typeof Ionicons.glyphMap;

  switch (routeName) {
    case 'Home':
      iconName = focused ? 'home' : 'home-outline';
      break;
    case 'Camera':
      iconName = focused ? 'camera' : 'camera-outline';
      break;
    case 'Analytics':
      iconName = focused ? 'bar-chart' : 'bar-chart-outline';
      break;
    case 'Settings':
      iconName = focused ? 'settings' : 'settings-outline';
      break;
    default:
      iconName = 'home-outline';
  }

  return <Ionicons name={iconName} size={size} color={color} />;
}

function MainTabs(): React.JSX.Element {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => getTabBarIcon(route.name, focused, color, size),
        tabBarActiveTintColor: '#2ED573',
        tabBarInactiveTintColor: '#6B7280',
        tabBarStyle: {
          backgroundColor: Theme.colors.surface,
          borderTopWidth: 1,
          borderTopColor: 'rgba(255,255,255,0.04)',
          elevation: 0,
          height: 88,
          paddingBottom: 28,
          paddingTop: 8,
        },
        tabBarLabelStyle: {
          fontSize: 11,
          fontWeight: '600' as const,
          marginTop: 2,
        },
        headerShown: false,
      })}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{ tabBarLabel: 'Today' }}
        listeners={{
          tabPress: () => haptics.light(),
        }}
      />
      <Tab.Screen
        name="Camera"
        component={CameraScreen}
        options={{ tabBarLabel: 'Scan' }}
        listeners={{
          tabPress: () => haptics.light(),
        }}
      />
      <Tab.Screen
        name="Analytics"
        component={AnalyticsScreen}
        options={{ tabBarLabel: 'Insights' }}
        listeners={{
          tabPress: () => haptics.light(),
        }}
      />
      <Tab.Screen
        name="Settings"
        component={SettingsScreen}
        options={{ tabBarLabel: 'Settings' }}
        listeners={{
          tabPress: () => haptics.light(),
        }}
      />
    </Tab.Navigator>
  );
}

function AppNavigator(): React.JSX.Element {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="Main" component={MainTabs} />
      <Stack.Screen name="Paywall" component={PaywallScreen} options={{ presentation: 'modal' }} />
    </Stack.Navigator>
  );
}

type AppPhase = 'splash' | 'onboarding' | 'app';

function AppContent(): React.JSX.Element {
  const hasCompletedOnboarding = useAppSelector(state => state.user.hasCompletedOnboarding);
  const [phase, setPhase] = useState<AppPhase>('splash');

  useEffect(() => {
    (async () => {
      try {
        await initPurchases();
        const { isPremium } = await checkEntitlements();
        store.dispatch(setPremiumStatus(isPremium));
      } catch {
        store.dispatch(setPremiumStatus(false));
      }
    })();
  }, []);

  const handleSplashFinish = useCallback(() => {
    if (hasCompletedOnboarding) {
      setPhase('app');
    } else {
      setPhase('onboarding');
    }
  }, [hasCompletedOnboarding]);

  const handleOnboardingComplete = useCallback(() => {
    setPhase('app');
  }, []);

  switch (phase) {
    case 'splash':
      return <SplashScreen onFinish={handleSplashFinish} />;
    case 'onboarding':
      return <OnboardingFlow onComplete={handleOnboardingComplete} />;
    case 'app':
      return (
        <NavigationContainer>
          <AppNavigator />
        </NavigationContainer>
      );
    default:
      return <SplashScreen onFinish={handleSplashFinish} />;
  }
}


const App = (): React.JSX.Element => {
  return (
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <SafeAreaProvider>
          <StatusBar barStyle="light-content" backgroundColor={Theme.colors.background} />
          <AppContent />
        </SafeAreaProvider>
      </PersistGate>
    </Provider>
  );
};

const styles = StyleSheet.create({});

export default App;
