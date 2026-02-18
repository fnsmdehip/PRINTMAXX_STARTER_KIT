/**
 * Settings Screen
 * App configuration and blocked apps selection
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Switch,
  Linking,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useUserStore } from '@/stores/userStore';
import { getManageSubscriptionUrl } from '@/services/subscriptionService';
import {
  COLORS,
  MIN_DEVOTION_MINUTES,
  MAX_DEVOTION_MINUTES,
  COMMON_SOCIAL_APPS,
} from '@/utils/constants';
import { AppInfo } from '@/types';

export default function SettingsScreen() {
  const router = useRouter();
  const { settings, updateSettings, subscription, checkAccess } = useUserStore();
  const [showAppSelector, setShowAppSelector] = useState(false);

  // Mock app list (in production, fetch from native module)
  const availableApps: AppInfo[] = COMMON_SOCIAL_APPS.map((app) => ({
    ...app,
    isBlocked: settings.blockedApps.includes(app.packageName),
  }));

  function handleDurationChange(delta: number) {
    const newDuration = Math.min(
      MAX_DEVOTION_MINUTES,
      Math.max(MIN_DEVOTION_MINUTES, settings.devotionDurationMinutes + delta)
    );
    updateSettings({ devotionDurationMinutes: newDuration });
  }

  function toggleAppBlocked(packageName: string) {
    const isCurrentlyBlocked = settings.blockedApps.includes(packageName);
    const newBlockedApps = isCurrentlyBlocked
      ? settings.blockedApps.filter((p) => p !== packageName)
      : [...settings.blockedApps, packageName];
    updateSettings({ blockedApps: newBlockedApps });
  }

  function openManageSubscription() {
    Linking.openURL(getManageSubscriptionUrl());
  }

  const hasAccess = checkAccess();

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Subscription Status */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Subscription</Text>
        <View style={styles.subscriptionCard}>
          <View>
            <Text style={styles.subscriptionStatus}>
              {subscription.isSubscribed
                ? 'Active'
                : subscription.isTrialing
                  ? 'Free Trial'
                  : 'Inactive'}
            </Text>
            {subscription.subscriptionType && (
              <Text style={styles.subscriptionType}>
                {subscription.subscriptionType === 'annual' ? 'Annual Plan' : 'Monthly Plan'}
              </Text>
            )}
          </View>
          {subscription.isSubscribed ? (
            <TouchableOpacity
              style={styles.manageButton}
              onPress={openManageSubscription}
            >
              <Text style={styles.manageButtonText}>Manage</Text>
            </TouchableOpacity>
          ) : (
            <TouchableOpacity
              style={styles.upgradeButton}
              onPress={() => router.push('/paywall')}
            >
              <Text style={styles.upgradeButtonText}>Upgrade</Text>
            </TouchableOpacity>
          )}
        </View>
      </View>

      {/* Devotion Settings */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Devotion Settings</Text>

        {/* Duration */}
        <View style={styles.settingRow}>
          <View>
            <Text style={styles.settingLabel}>Prayer Duration</Text>
            <Text style={styles.settingDescription}>
              Time required for prayer timer
            </Text>
          </View>
          <View style={styles.durationControl}>
            <TouchableOpacity
              style={styles.durationButton}
              onPress={() => handleDurationChange(-5)}
              disabled={settings.devotionDurationMinutes <= MIN_DEVOTION_MINUTES}
            >
              <Text style={styles.durationButtonText}>-</Text>
            </TouchableOpacity>
            <Text style={styles.durationValue}>
              {settings.devotionDurationMinutes} min
            </Text>
            <TouchableOpacity
              style={styles.durationButton}
              onPress={() => handleDurationChange(5)}
              disabled={settings.devotionDurationMinutes >= MAX_DEVOTION_MINUTES}
            >
              <Text style={styles.durationButtonText}>+</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Require Timer */}
        <View style={styles.settingRow}>
          <View style={styles.settingTextContainer}>
            <Text style={styles.settingLabel}>Require Prayer Timer</Text>
            <Text style={styles.settingDescription}>
              Must complete timer to unlock
            </Text>
          </View>
          <Switch
            value={settings.requireTimer}
            onValueChange={(value) => updateSettings({ requireTimer: value })}
            trackColor={{ false: COLORS.disabled, true: COLORS.primary }}
          />
        </View>

        {/* Require Scripture */}
        <View style={styles.settingRow}>
          <View style={styles.settingTextContainer}>
            <Text style={styles.settingLabel}>Require Scripture Reading</Text>
            <Text style={styles.settingDescription}>
              Must read daily passage to unlock
            </Text>
          </View>
          <Switch
            value={settings.requireScripture}
            onValueChange={(value) => updateSettings({ requireScripture: value })}
            trackColor={{ false: COLORS.disabled, true: COLORS.primary }}
          />
        </View>

        {/* Emergency Unlock */}
        <View style={styles.settingRow}>
          <View style={styles.settingTextContainer}>
            <Text style={styles.settingLabel}>Enable Emergency Unlock</Text>
            <Text style={styles.settingDescription}>
              Allow bypass option (resets streak)
            </Text>
          </View>
          <Switch
            value={settings.emergencyUnlockEnabled}
            onValueChange={(value) =>
              updateSettings({ emergencyUnlockEnabled: value })
            }
            trackColor={{ false: COLORS.disabled, true: COLORS.primary }}
          />
        </View>
      </View>

      {/* Blocked Apps */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Blocked Apps</Text>
          <TouchableOpacity onPress={() => setShowAppSelector(!showAppSelector)}>
            <Text style={styles.editLink}>
              {showAppSelector ? 'Done' : 'Edit'}
            </Text>
          </TouchableOpacity>
        </View>

        {showAppSelector ? (
          <View style={styles.appList}>
            {availableApps.map((app) => (
              <TouchableOpacity
                key={app.packageName}
                style={styles.appItem}
                onPress={() => toggleAppBlocked(app.packageName)}
              >
                <Text style={styles.appName}>{app.appName}</Text>
                <View
                  style={[
                    styles.checkbox,
                    settings.blockedApps.includes(app.packageName) &&
                      styles.checkboxChecked,
                  ]}
                >
                  {settings.blockedApps.includes(app.packageName) && (
                    <Text style={styles.checkmark}>&#10003;</Text>
                  )}
                </View>
              </TouchableOpacity>
            ))}
          </View>
        ) : (
          <View style={styles.blockedSummary}>
            {settings.blockedApps.length === 0 ? (
              <Text style={styles.noAppsText}>
                No apps selected for blocking
              </Text>
            ) : (
              <Text style={styles.blockedCount}>
                {settings.blockedApps.length} app
                {settings.blockedApps.length !== 1 ? 's' : ''} will be blocked until
                devotion is complete
              </Text>
            )}
          </View>
        )}
      </View>

      {/* Notifications */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Notifications</Text>
        <View style={styles.settingRow}>
          <View style={styles.settingTextContainer}>
            <Text style={styles.settingLabel}>Daily Reminders</Text>
            <Text style={styles.settingDescription}>
              Get notified to start your devotion
            </Text>
          </View>
          <Switch
            value={settings.notificationsEnabled}
            onValueChange={(value) =>
              updateSettings({ notificationsEnabled: value })
            }
            trackColor={{ false: COLORS.disabled, true: COLORS.primary }}
          />
        </View>
      </View>

      {/* Legal Links */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Legal</Text>
        <TouchableOpacity
          style={styles.linkRow}
          onPress={() => router.push('/privacy-policy')}
        >
          <Text style={styles.linkText}>Privacy Policy</Text>
          <Text style={styles.linkArrow}>&#8250;</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.linkRow}
          onPress={() => router.push('/terms')}
        >
          <Text style={styles.linkText}>Terms of Service</Text>
          <Text style={styles.linkArrow}>&#8250;</Text>
        </TouchableOpacity>
      </View>

      {/* Version */}
      <Text style={styles.versionText}>FocusPrayer v1.0.0</Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  content: {
    padding: 20,
    paddingBottom: 40,
  },
  section: {
    marginBottom: 24,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 12,
  },
  editLink: {
    color: COLORS.primary,
    fontWeight: '600',
    marginBottom: 12,
  },
  subscriptionCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  subscriptionStatus: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
  },
  subscriptionType: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  manageButton: {
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: COLORS.primary,
  },
  manageButtonText: {
    color: COLORS.primary,
    fontWeight: '600',
  },
  upgradeButton: {
    backgroundColor: COLORS.primary,
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
  },
  upgradeButtonText: {
    color: COLORS.surface,
    fontWeight: '600',
  },
  settingRow: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  settingTextContainer: {
    flex: 1,
    marginRight: 16,
  },
  settingLabel: {
    fontSize: 16,
    fontWeight: '500',
    color: COLORS.text,
  },
  settingDescription: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  durationControl: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  durationButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  durationButtonText: {
    color: COLORS.surface,
    fontSize: 20,
    fontWeight: '600',
  },
  durationValue: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    minWidth: 60,
    textAlign: 'center',
  },
  appList: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    overflow: 'hidden',
  },
  appItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.background,
  },
  appName: {
    fontSize: 16,
    color: COLORS.text,
  },
  checkbox: {
    width: 24,
    height: 24,
    borderRadius: 6,
    borderWidth: 2,
    borderColor: COLORS.disabled,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkboxChecked: {
    backgroundColor: COLORS.primary,
    borderColor: COLORS.primary,
  },
  checkmark: {
    color: COLORS.surface,
    fontSize: 14,
    fontWeight: '600',
  },
  blockedSummary: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
  },
  noAppsText: {
    color: COLORS.textSecondary,
  },
  blockedCount: {
    color: COLORS.text,
  },
  linkRow: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  linkText: {
    fontSize: 16,
    color: COLORS.text,
  },
  linkArrow: {
    fontSize: 20,
    color: COLORS.textSecondary,
  },
  versionText: {
    textAlign: 'center',
    color: COLORS.disabled,
    fontSize: 13,
    marginTop: 20,
  },
});
