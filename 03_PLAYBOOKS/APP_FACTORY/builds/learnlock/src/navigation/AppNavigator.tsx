import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Text, View, StyleSheet } from 'react-native';

import { HomeScreen } from '../screens/HomeScreen';
import { StatsScreen } from '../screens/StatsScreen';
import { SettingsScreen } from '../screens/SettingsScreen';
import { PaywallScreen } from '../components/paywall/PaywallScreen';
import { useUserStore } from '../stores/userStore';
import { RootStackParamList, MainTabParamList } from '../types';
import { COLORS, TYPOGRAPHY, SPACING } from '../utils/constants';

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<MainTabParamList>();

// Tab icon component (simplified - use actual icons in production)
function TabIcon({ name, focused }: { name: string; focused: boolean }) {
  const icons: Record<string, string> = {
    Home: '⏱️',
    Stats: '📊',
    Settings: '⚙️',
  };

  return (
    <Text style={[styles.tabIcon, focused && styles.tabIconFocused]}>
      {icons[name] || '•'}
    </Text>
  );
}

// Main tab navigator
function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused }) => (
          <TabIcon name={route.name} focused={focused} />
        ),
        tabBarActiveTintColor: COLORS.primary,
        tabBarInactiveTintColor: COLORS.textTertiary,
        tabBarStyle: styles.tabBar,
        tabBarLabelStyle: styles.tabLabel,
        headerShown: false,
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Stats" component={StatsScreen} />
      <Tab.Screen name="Settings" component={SettingsScreen} />
    </Tab.Navigator>
  );
}

// Onboarding screen (simplified - expand for production)
function OnboardingScreen({ navigation }: any) {
  const { completeOnboarding } = useUserStore();

  const handleComplete = () => {
    completeOnboarding();
    navigation.replace('Main');
  };

  return (
    <View style={styles.onboardingContainer}>
      <Text style={styles.onboardingTitle}>Welcome to StudyLock</Text>
      <Text style={styles.onboardingSubtitle}>
        Block distracting apps while you study. Build better habits. Get better
        grades.
      </Text>
      <View style={styles.onboardingFeatures}>
        <OnboardingFeature icon="⏱️" text="Pomodoro timer with customizable sessions" />
        <OnboardingFeature icon="🔒" text="Block distracting apps during focus time" />
        <OnboardingFeature icon="🔥" text="Track your study streaks" />
        <OnboardingFeature icon="📊" text="View your progress and stats" />
      </View>
      <View style={styles.onboardingButton}>
        <Text style={styles.onboardingButtonText} onPress={handleComplete}>
          Get Started
        </Text>
      </View>
    </View>
  );
}

function OnboardingFeature({ icon, text }: { icon: string; text: string }) {
  return (
    <View style={styles.featureRow}>
      <Text style={styles.featureIcon}>{icon}</Text>
      <Text style={styles.featureText}>{text}</Text>
    </View>
  );
}

// Root navigator
export function AppNavigator() {
  const { hasCompletedOnboarding, canAccessApp } = useUserStore();

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {!hasCompletedOnboarding ? (
          <Stack.Screen name="Onboarding" component={OnboardingScreen} />
        ) : !canAccessApp() ? (
          <Stack.Screen name="Paywall" component={PaywallScreen} />
        ) : (
          <Stack.Screen name="Main" component={MainTabs} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  tabBar: {
    backgroundColor: COLORS.surface,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
    paddingTop: SPACING.sm,
    paddingBottom: SPACING.md,
    height: 80,
  },
  tabLabel: {
    ...TYPOGRAPHY.caption,
    marginTop: 4,
  },
  tabIcon: {
    fontSize: 24,
  },
  tabIconFocused: {
    opacity: 1,
  },
  onboardingContainer: {
    flex: 1,
    backgroundColor: COLORS.background,
    padding: SPACING.xl,
    justifyContent: 'center',
  },
  onboardingTitle: {
    ...TYPOGRAPHY.h1,
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: SPACING.md,
  },
  onboardingSubtitle: {
    ...TYPOGRAPHY.body,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: SPACING.xxl,
  },
  onboardingFeatures: {
    marginBottom: SPACING.xxl,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  featureIcon: {
    fontSize: 24,
    marginRight: SPACING.md,
    width: 32,
  },
  featureText: {
    ...TYPOGRAPHY.body,
    color: COLORS.text,
    flex: 1,
  },
  onboardingButton: {
    backgroundColor: COLORS.primary,
    paddingVertical: SPACING.md,
    borderRadius: 12,
    alignItems: 'center',
  },
  onboardingButtonText: {
    ...TYPOGRAPHY.body,
    color: COLORS.surface,
    fontWeight: '700',
  },
});
