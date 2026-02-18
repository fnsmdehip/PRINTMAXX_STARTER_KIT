import React, { useState, useEffect } from 'react';
import { View, ActivityIndicator } from 'react-native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { colors } from '../utils/theme';

// Screens
import HomeScreen from '../screens/HomeScreen';
import FavoritesScreen from '../screens/FavoritesScreen';
import ImproveScreen from '../screens/ImproveScreen';
import SettingsScreen from '../screens/SettingsScreen';
import PromptDetailScreen from '../screens/PromptDetailScreen';
import OnboardingScreen from '../screens/OnboardingScreen';

// Types
export type RootStackParamList = {
  Onboarding: undefined;
  MainTabs: undefined;
  PromptDetail: { promptId: string };
};

export type TabParamList = {
  Home: undefined;
  Favorites: undefined;
  Improve: undefined;
  Settings: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<TabParamList>();

const ONBOARDING_KEY = 'promptvault_onboarding';

function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarStyle: {
          backgroundColor: colors.surface,
          borderTopColor: colors.surfaceLight,
          borderTopWidth: 1,
          paddingTop: 8,
          paddingBottom: 8,
          height: 60,
        },
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.textMuted,
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '500',
        },
      }}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          tabBarLabel: 'Library',
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons
              name="book-open-variant"
              size={size}
              color={color}
            />
          ),
        }}
      />
      <Tab.Screen
        name="Favorites"
        component={FavoritesScreen}
        options={{
          tabBarLabel: 'Favorites',
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="heart" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Improve"
        component={ImproveScreen}
        options={{
          tabBarLabel: 'Improve',
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons
              name="magic-staff"
              size={size}
              color={color}
            />
          ),
        }}
      />
      <Tab.Screen
        name="Settings"
        component={SettingsScreen}
        options={{
          tabBarLabel: 'Settings',
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="cog" size={size} color={color} />
          ),
        }}
      />
    </Tab.Navigator>
  );
}

// Onboarding wrapper component that handles completion
function OnboardingWrapper({
  navigation,
}: {
  navigation: any;
}) {
  const handleComplete = () => {
    navigation.reset({
      index: 0,
      routes: [{ name: 'MainTabs' }],
    });
  };

  return <OnboardingScreen onComplete={handleComplete} />;
}

export default function RootNavigator() {
  const [isLoading, setIsLoading] = useState(true);
  const [showOnboarding, setShowOnboarding] = useState(false);

  useEffect(() => {
    checkOnboardingStatus();
  }, []);

  const checkOnboardingStatus = async () => {
    try {
      const onboardingData = await AsyncStorage.getItem(ONBOARDING_KEY);

      if (onboardingData) {
        const parsed = JSON.parse(onboardingData);
        setShowOnboarding(!parsed.onboardingCompleted);
      } else {
        // First launch - show onboarding
        setShowOnboarding(true);
      }
    } catch (error) {
      // Error reading storage - default to showing onboarding
      console.error('Error checking onboarding status:', error);
      setShowOnboarding(true);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <View
        style={{
          flex: 1,
          justifyContent: 'center',
          alignItems: 'center',
          backgroundColor: colors.background,
        }}
      >
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
        contentStyle: { backgroundColor: colors.background },
      }}
      initialRouteName={showOnboarding ? 'Onboarding' : 'MainTabs'}
    >
      <Stack.Screen
        name="Onboarding"
        component={OnboardingWrapper}
        options={{
          gestureEnabled: false,
          animation: 'fade',
        }}
      />
      <Stack.Screen name="MainTabs" component={TabNavigator} />
      <Stack.Screen
        name="PromptDetail"
        component={PromptDetailScreen}
        options={{
          presentation: 'card',
          animation: 'slide_from_right',
        }}
      />
    </Stack.Navigator>
  );
}
