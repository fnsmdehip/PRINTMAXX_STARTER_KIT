import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Switch,
} from 'react-native';
import { COLORS, TYPOGRAPHY, SPACING, DEFAULT_BLOCKED_APPS } from '../../utils/constants';
import { BlockedApp } from '../../types';
import { useUserStore } from '../../stores/userStore';

interface Props {
  selectedApps: BlockedApp[];
  onToggleApp: (app: BlockedApp, enabled: boolean) => void;
}

// App icons mapping (simplified - in production use actual icons)
const APP_ICONS: Record<string, string> = {
  'TikTok': '📱',
  'Instagram': '📸',
  'Twitter': '🐦',
  'YouTube': '▶️',
  'Snapchat': '👻',
  'Discord': '💬',
  'Reddit': '📰',
  'Facebook': '👤',
};

export function AppSelector({ selectedApps, onToggleApp }: Props) {
  const selectedIds = new Set(selectedApps.map((a) => a.id));

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Apps to Block</Text>
      <Text style={styles.subtitle}>
        These apps will be blocked until you complete your study session
      </Text>

      <View style={styles.list}>
        {DEFAULT_BLOCKED_APPS.map((app) => {
          const isSelected = selectedIds.has(app.id);

          return (
            <View key={app.id} style={styles.appRow}>
              <View style={styles.appInfo}>
                <Text style={styles.appIcon}>{APP_ICONS[app.name] || '📱'}</Text>
                <Text style={styles.appName}>{app.name}</Text>
              </View>
              <Switch
                value={isSelected}
                onValueChange={(enabled) => onToggleApp(app, enabled)}
                trackColor={{
                  false: COLORS.surfaceSecondary,
                  true: COLORS.primaryLight,
                }}
                thumbColor={isSelected ? COLORS.primary : COLORS.surface}
              />
            </View>
          );
        })}
      </View>

      <View style={styles.infoBox}>
        <Text style={styles.infoIcon}>💡</Text>
        <Text style={styles.infoText}>
          You can change blocked apps anytime in Settings. We recommend blocking
          social media and games for best results.
        </Text>
      </View>
    </View>
  );
}

// Standalone component for settings screen
export function AppBlockerSettings() {
  const { blockedApps, addBlockedApp, removeBlockedApp } = useUserStore();

  const handleToggle = (app: BlockedApp, enabled: boolean) => {
    if (enabled) {
      addBlockedApp(app);
    } else {
      removeBlockedApp(app.id);
    }
  };

  return (
    <ScrollView style={styles.settingsContainer}>
      <AppSelector
        selectedApps={blockedApps}
        onToggleApp={handleToggle}
      />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.lg,
  },
  settingsContainer: {
    flex: 1,
    backgroundColor: COLORS.background,
    padding: SPACING.lg,
  },
  title: {
    ...TYPOGRAPHY.h3,
    color: COLORS.text,
    marginBottom: SPACING.xs,
  },
  subtitle: {
    ...TYPOGRAPHY.bodySmall,
    color: COLORS.textSecondary,
    marginBottom: SPACING.lg,
  },
  list: {
    gap: SPACING.sm,
  },
  appRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
    backgroundColor: COLORS.surfaceSecondary,
    borderRadius: 12,
  },
  appInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  appIcon: {
    fontSize: 24,
    marginRight: SPACING.md,
    width: 32,
    textAlign: 'center',
  },
  appName: {
    ...TYPOGRAPHY.body,
    color: COLORS.text,
  },
  infoBox: {
    flexDirection: 'row',
    backgroundColor: COLORS.primary + '10',
    borderRadius: 12,
    padding: SPACING.md,
    marginTop: SPACING.lg,
  },
  infoIcon: {
    fontSize: 16,
    marginRight: SPACING.sm,
  },
  infoText: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textSecondary,
    flex: 1,
  },
});
