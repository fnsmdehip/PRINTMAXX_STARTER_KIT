/**
 * Cross-Promotion Component Template
 *
 * Copy this to: src/components/MoreApps.tsx
 * Update the APP_LIST for your specific app (remove self from list).
 *
 * Shows other PRINTMAXX apps to drive cross-installs.
 */

import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  Linking,
  StyleSheet,
  Platform,
} from 'react-native';

interface AppItem {
  name: string;
  tagline: string;
  iosUrl: string;
  androidUrl: string;
  icon: string; // Emoji fallback until real icons
}

// UPDATE: Remove the current app from this list
const APP_LIST: AppItem[] = [
  {
    name: 'PrayerLock',
    tagline: 'Faith-powered focus timer',
    iosUrl: 'https://apps.apple.com/app/prayerlock/id0000000000',
    androidUrl: 'https://play.google.com/store/apps/details?id=com.printmaxx.prayerlock',
    icon: '\u{1F64F}',
  },
  {
    name: 'BioMaxx',
    tagline: 'Biohacking protocols tracker',
    iosUrl: 'https://apps.apple.com/app/biomaxx/id0000000000',
    androidUrl: 'https://play.google.com/store/apps/details?id=com.printmaxx.biomaxx',
    icon: '\u{1F9EC}',
  },
  {
    name: 'StepUnlock',
    tagline: 'Walk to unlock your phone',
    iosUrl: 'https://apps.apple.com/app/stepunlock/id0000000000',
    androidUrl: 'https://play.google.com/store/apps/details?id=com.stepunlock.app',
    icon: '\u{1F6B6}',
  },
  {
    name: 'GlowMaxx',
    tagline: 'Skincare routine tracker',
    iosUrl: 'https://apps.apple.com/app/glowmaxx/id0000000000',
    androidUrl: 'https://play.google.com/store/apps/details?id=com.glowmaxx.app',
    icon: '\u{2728}',
  },
  {
    name: 'LearnLock',
    tagline: 'Study timer with focus lock',
    iosUrl: 'https://apps.apple.com/app/learnlock/id0000000000',
    androidUrl: 'https://play.google.com/store/apps/details?id=com.printmaxx.learnlock',
    icon: '\u{1F4DA}',
  },
  {
    name: 'PelvicPro',
    tagline: 'Pelvic floor exercise guide',
    iosUrl: 'https://apps.apple.com/app/pelvicpro/id0000000000',
    androidUrl: 'https://play.google.com/store/apps/details?id=com.printmaxx.pelvicpro',
    icon: '\u{1F4AA}',
  },
];

interface MoreAppsProps {
  excludeApp?: string; // Name of current app to exclude
}

export function MoreApps({ excludeApp }: MoreAppsProps) {
  const apps = APP_LIST.filter((app) => app.name !== excludeApp);

  const openApp = (app: AppItem) => {
    const url = Platform.OS === 'ios' ? app.iosUrl : app.androidUrl;
    Linking.openURL(url).catch(() => {
      // Fallback to website
      Linking.openURL('https://printmaxx.com');
    });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>More from PRINTMAXX</Text>
      {apps.map((app) => (
        <TouchableOpacity
          key={app.name}
          style={styles.appRow}
          onPress={() => openApp(app)}
        >
          <Text style={styles.icon}>{app.icon}</Text>
          <View style={styles.appInfo}>
            <Text style={styles.appName}>{app.name}</Text>
            <Text style={styles.appTagline}>{app.tagline}</Text>
          </View>
          <Text style={styles.arrow}>{'\u{203A}'}</Text>
        </TouchableOpacity>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginTop: 24,
    paddingHorizontal: 16,
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
    color: '#666',
    marginBottom: 12,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  appRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: '#E0E0E0',
  },
  icon: {
    fontSize: 28,
    marginRight: 12,
  },
  appInfo: {
    flex: 1,
  },
  appName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1A1A1A',
  },
  appTagline: {
    fontSize: 13,
    color: '#888',
    marginTop: 2,
  },
  arrow: {
    fontSize: 22,
    color: '#CCC',
    marginLeft: 8,
  },
});

export default MoreApps;
