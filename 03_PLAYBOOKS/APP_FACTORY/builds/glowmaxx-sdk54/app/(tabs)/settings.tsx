import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Switch,
  Alert,
  Linking,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';

import { useUserStore } from '../../src/stores/userStore';
import { COLORS, APP_VERSION, MONTHLY_PRICE, ANNUAL_PRICE } from '../../src/utils/constants';
import {
  scheduleMewingReminder,
  cancelMewingReminders,
} from '../../src/services/notificationService';
import { MoreApps } from '../../src/components/MoreApps';

export default function SettingsScreen() {
  const { settings, subscription, updateSettings, setGender } = useUserStore();

  const handleMewingRemindersToggle = async (value: boolean) => {
    Haptics.selectionAsync();
    updateSettings({ mewingRemindersEnabled: value });

    if (value) {
      await scheduleMewingReminder(settings.mewingReminderInterval);
    } else {
      await cancelMewingReminders();
    }
  };

  const handleNotificationsToggle = (value: boolean) => {
    Haptics.selectionAsync();
    updateSettings({ notificationsEnabled: value });
  };

  const handleChangeGender = () => {
    Alert.alert('Change Gender', 'Select your gender for personalized routines', [
      { text: 'Male', onPress: () => setGender('male') },
      { text: 'Female', onPress: () => setGender('female') },
      { text: 'Other', onPress: () => setGender('other') },
      { text: 'Cancel', style: 'cancel' },
    ]);
  };

  const handleMewingInterval = () => {
    Alert.alert('Mewing Reminder Interval', 'How often should we remind you?', [
      { text: '15 minutes', onPress: () => updateSettings({ mewingReminderInterval: 15 }) },
      { text: '30 minutes', onPress: () => updateSettings({ mewingReminderInterval: 30 }) },
      { text: '60 minutes', onPress: () => updateSettings({ mewingReminderInterval: 60 }) },
      { text: '2 hours', onPress: () => updateSettings({ mewingReminderInterval: 120 }) },
      { text: 'Cancel', style: 'cancel' },
    ]);
  };

  const handleWaterGoal = () => {
    Alert.prompt(
      'Daily Water Goal',
      'Enter your daily water intake goal (ml)',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Save',
          onPress: (text: string | undefined) => {
            const ml = parseInt(text || '0', 10);
            if (ml >= 1000 && ml <= 5000) {
              updateSettings({
                dailyGoals: { ...settings.dailyGoals, waterIntake: ml },
              });
            }
          },
        },
      ],
      'plain-text',
      settings.dailyGoals.waterIntake.toString(),
      'number-pad'
    );
  };

  const handleMewingGoal = () => {
    Alert.prompt(
      'Daily Mewing Goal',
      'Enter your daily mewing goal (minutes)',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Save',
          onPress: (text: string | undefined) => {
            const minutes = parseInt(text || '0', 10);
            if (minutes >= 15 && minutes <= 480) {
              updateSettings({
                dailyGoals: { ...settings.dailyGoals, mewingMinutes: minutes },
              });
            }
          },
        },
      ],
      'plain-text',
      settings.dailyGoals.mewingMinutes.toString(),
      'number-pad'
    );
  };

  const renderSettingRow = (
    icon: keyof typeof Ionicons.glyphMap,
    title: string,
    value?: string,
    onPress?: () => void,
    showChevron = true
  ) => (
    <TouchableOpacity
      style={styles.settingRow}
      onPress={onPress}
      disabled={!onPress}
    >
      <View style={styles.settingLeft}>
        <Ionicons name={icon} size={22} color={COLORS.primary} />
        <Text style={styles.settingTitle}>{title}</Text>
      </View>
      <View style={styles.settingRight}>
        {value && <Text style={styles.settingValue}>{value}</Text>}
        {showChevron && onPress && (
          <Ionicons name="chevron-forward" size={20} color={COLORS.textLight} />
        )}
      </View>
    </TouchableOpacity>
  );

  const renderToggleRow = (
    icon: keyof typeof Ionicons.glyphMap,
    title: string,
    value: boolean,
    onToggle: (value: boolean) => void
  ) => (
    <View style={styles.settingRow}>
      <View style={styles.settingLeft}>
        <Ionicons name={icon} size={22} color={COLORS.primary} />
        <Text style={styles.settingTitle}>{title}</Text>
      </View>
      <Switch
        value={value}
        onValueChange={onToggle}
        trackColor={{ false: COLORS.border, true: COLORS.primaryLight }}
        thumbColor={value ? COLORS.primary : COLORS.disabled}
      />
    </View>
  );

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Settings</Text>
      </View>

      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Subscription Status */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Subscription</Text>
          <TouchableOpacity
            style={styles.subscriptionCard}
            onPress={() => router.push('/paywall')}
          >
            <View style={styles.subscriptionInfo}>
              <Text style={styles.subscriptionStatus}>
                {subscription.isSubscribed
                  ? 'Premium Active'
                  : subscription.isInTrial
                  ? 'Free Trial'
                  : 'Free Plan'}
              </Text>
              <Text style={styles.subscriptionDetail}>
                {subscription.isSubscribed
                  ? 'All features unlocked'
                  : subscription.isInTrial
                  ? `${subscription.trialDaysRemaining} days remaining`
                  : 'Upgrade for full access'}
              </Text>
            </View>
            <Ionicons name="chevron-forward" size={24} color={COLORS.primary} />
          </TouchableOpacity>
        </View>

        {/* Profile */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Profile</Text>
          <View style={styles.card}>
            {renderSettingRow(
              'person-outline',
              'Gender',
              settings.gender.charAt(0).toUpperCase() + settings.gender.slice(1),
              handleChangeGender
            )}
          </View>
        </View>

        {/* Goals */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Daily Goals</Text>
          <View style={styles.card}>
            {renderSettingRow(
              'water-outline',
              'Water Intake',
              `${settings.dailyGoals.waterIntake}ml`,
              handleWaterGoal
            )}
            {renderSettingRow(
              'happy-outline',
              'Mewing Time',
              `${settings.dailyGoals.mewingMinutes} min`,
              handleMewingGoal
            )}
          </View>
        </View>

        {/* Notifications */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Notifications</Text>
          <View style={styles.card}>
            {renderToggleRow(
              'notifications-outline',
              'Enable Notifications',
              settings.notificationsEnabled,
              handleNotificationsToggle
            )}
            {renderToggleRow(
              'time-outline',
              'Mewing Reminders',
              settings.mewingRemindersEnabled,
              handleMewingRemindersToggle
            )}
            {settings.mewingRemindersEnabled &&
              renderSettingRow(
                'repeat-outline',
                'Reminder Interval',
                `${settings.mewingReminderInterval} min`,
                handleMewingInterval
              )}
          </View>
        </View>

        {/* Legal */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Legal</Text>
          <View style={styles.card}>
            {renderSettingRow(
              'document-text-outline',
              'Privacy Policy',
              undefined,
              () => router.push('/privacy-policy')
            )}
            {renderSettingRow(
              'reader-outline',
              'Terms of Service',
              undefined,
              () => router.push('/terms')
            )}
          </View>
        </View>

        {/* Support */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Support</Text>
          <View style={styles.card}>
            {renderSettingRow(
              'mail-outline',
              'Contact Support',
              undefined,
              () => Linking.openURL('mailto:support@glowmaxx.app')
            )}
            {renderSettingRow(
              'star-outline',
              'Rate the App',
              undefined,
              () => Alert.alert('Coming Soon', 'Rating will be available after launch!')
            )}
          </View>
        </View>

        {/* More Apps */}
        <MoreApps />

        {/* App Info */}
        <View style={styles.appInfo}>
          <Text style={styles.appName}>GlowMaxx</Text>
          <Text style={styles.appVersion}>Version {APP_VERSION}</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 10,
    paddingBottom: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    paddingTop: 0,
    paddingBottom: 40,
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.textSecondary,
    marginBottom: 8,
    marginLeft: 4,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  card: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    overflow: 'hidden',
  },
  subscriptionCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 16,
  },
  subscriptionInfo: {
    flex: 1,
  },
  subscriptionStatus: {
    fontSize: 17,
    fontWeight: '600',
    color: COLORS.primary,
    marginBottom: 4,
  },
  subscriptionDetail: {
    fontSize: 13,
    color: COLORS.textSecondary,
  },
  settingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  settingLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  settingTitle: {
    fontSize: 16,
    color: COLORS.text,
  },
  settingRight: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  settingValue: {
    fontSize: 15,
    color: COLORS.textSecondary,
  },
  appInfo: {
    alignItems: 'center',
    marginTop: 20,
  },
  appName: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.textSecondary,
  },
  appVersion: {
    fontSize: 13,
    color: COLORS.textLight,
    marginTop: 4,
  },
});
