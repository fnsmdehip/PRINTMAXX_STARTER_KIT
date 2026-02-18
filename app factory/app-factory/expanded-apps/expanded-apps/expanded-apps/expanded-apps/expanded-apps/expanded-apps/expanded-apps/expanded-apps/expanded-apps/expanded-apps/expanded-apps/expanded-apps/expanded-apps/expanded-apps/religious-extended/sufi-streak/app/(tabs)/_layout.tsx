import { Tabs, useRouter } from 'expo-router';
import { View, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { AdBanner } from '../../src/components/AdBanner';

export default function TabsLayout() {
  console.log('🔍 DEBUG: TabsLayout component loaded');
  console.log('🔍 DEBUG: TabsLayout file path:', __filename);

  const router = useRouter();
  console.log('🔍 DEBUG: TabsLayout router created:', typeof router);

  const handleUpgradePress = () => {
    console.log('🔍 DEBUG: handleUpgradePress called');
    router.push('/paywall');
  };

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <Tabs
          screenOptions={{
            headerShown: false,
            tabBarStyle: styles.tabBar,
            tabBarActiveTintColor: '#e94560',
            tabBarInactiveTintColor: '#ffffff50',
            tabBarLabelStyle: styles.tabLabel,
          }}
        >
          <Tabs.Screen
            name="index"
            options={{
              title: 'Today',
              tabBarIcon: ({ color, focused }) => (
                <Ionicons 
                  name={focused ? 'sunny' : 'sunny-outline'} 
                  size={24} 
                  color={color} 
                />
              ),
            }}
          />
          <Tabs.Screen
            name="bible"
            options={{
              title: 'Bible',
              tabBarIcon: ({ color, focused }) => (
                <Ionicons 
                  name={focused ? 'book' : 'book-outline'} 
                  size={24} 
                  color={color} 
                />
              ),
            }}
          />
          <Tabs.Screen
            name="progress"
            options={{
              title: 'Progress',
              tabBarIcon: ({ color, focused }) => (
                <Ionicons 
                  name={focused ? 'stats-chart' : 'stats-chart-outline'} 
                  size={24} 
                  color={color} 
                />
              ),
            }}
          />
          <Tabs.Screen
            name="community"
            options={{
              title: 'Community',
              tabBarIcon: ({ color, focused }) => (
                <Ionicons 
                  name={focused ? 'people' : 'people-outline'} 
                  size={24} 
                  color={color} 
                />
              ),
            }}
          />
          <Tabs.Screen
            name="settings"
            options={{
              title: 'Settings',
              tabBarIcon: ({ color, focused }) => (
                <Ionicons
                  name={focused ? 'settings' : 'settings-outline'}
                  size={24}
                  color={color}
                />
              ),
            }}
          />
        </Tabs>
      </View>
      <AdBanner onUpgradePress={handleUpgradePress} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
  },
  content: {
    flex: 1,
  },
  tabBar: {
    backgroundColor: '#0f0f23',
    borderTopWidth: 1,
    borderTopColor: '#ffffff08',
    paddingTop: 8,
    paddingBottom: 28,
    height: 90,
  },
  tabLabel: {
    fontSize: 11,
    fontWeight: '600',
    marginTop: 4,
  },
});
