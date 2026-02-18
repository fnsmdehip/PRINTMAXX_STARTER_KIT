import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Linking } from 'react-native';

interface AppPromo {
  name: string;
  tagline: string;
  icon: string;
  storeUrl: string;
}

const OTHER_APPS: AppPromo[] = [
  {
    name: 'BioMaxx',
    tagline: 'Biohacking protocol tracker',
    icon: '🧬',
    storeUrl: 'https://apps.apple.com/app/biomaxx/id0000000000',
  },
  {
    name: 'StepUnlock',
    tagline: 'Walk to unlock your phone',
    icon: '🚶',
    storeUrl: 'https://apps.apple.com/app/stepunlock/id0000000000',
  },
  {
    name: 'LearnLock',
    tagline: 'Study to unlock your apps',
    icon: '📚',
    storeUrl: 'https://apps.apple.com/app/learnlock/id0000000000',
  },
];

export function MoreApps() {
  const handlePress = async (url: string) => {
    try {
      await Linking.openURL(url);
    } catch (error) {
      console.error('Failed to open store link:', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>More from PrintMaxx</Text>
      {OTHER_APPS.map((app, index) => (
        <TouchableOpacity
          key={index}
          style={styles.appRow}
          onPress={() => handlePress(app.storeUrl)}
          activeOpacity={0.7}
        >
          <Text style={styles.appIcon}>{app.icon}</Text>
          <View style={styles.appInfo}>
            <Text style={styles.appName}>{app.name}</Text>
            <Text style={styles.appTagline}>{app.tagline}</Text>
          </View>
          <Text style={styles.arrow}>{'>'}</Text>
        </TouchableOpacity>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginTop: 8,
    marginBottom: 24,
  },
  title: {
    fontSize: 14,
    fontWeight: '600',
    color: '#8b8b9e',
    marginBottom: 12,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  appRow: {
    backgroundColor: '#2a2a4e',
    borderRadius: 12,
    padding: 14,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  appIcon: {
    fontSize: 28,
    marginRight: 12,
  },
  appInfo: {
    flex: 1,
  },
  appName: {
    fontSize: 16,
    color: '#fff',
    fontWeight: '500',
  },
  appTagline: {
    fontSize: 13,
    color: '#8b8b9e',
    marginTop: 2,
  },
  arrow: {
    fontSize: 18,
    color: '#6c63ff',
    fontWeight: '600',
  },
});
