import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
  Switch,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useUserStore } from '../stores/userStore';
import { COLORS, SESSION_DURATIONS, DEFAULT_SETTINGS } from '../utils/constants';
import Card from '../components/Card';

export default function SettingsScreen() {
  const router = useRouter();
  const { settings, updateSettings, progress, resetProgress } = useUserStore();

  const handleToggle = (key: keyof typeof settings) => {
    updateSettings({ [key]: !settings[key] });
  };

  const handleDurationChange = () => {
    Alert.alert(
      'Default Session Length',
      'Choose your default session duration',
      SESSION_DURATIONS.map((duration) => ({
        text: `${duration} minutes`,
        onPress: () => updateSettings({ defaultSessionLength: duration }),
      })).concat([{ text: 'Cancel', style: 'cancel' }])
    );
  };

  const handlePenaltyChange = () => {
    Alert.alert(
      'Quiz Penalty',
      'Minutes added for wrong answers',
      [0, 2, 5, 10].map((penalty) => ({
        text: penalty === 0 ? 'No penalty' : `${penalty} minutes`,
        onPress: () => updateSettings({ penaltyMinutes: penalty }),
      })).concat([{ text: 'Cancel', style: 'cancel' }])
    );
  };

  const handleResetProgress = () => {
    Alert.alert(
      'Reset Progress',
      'This will delete all your study history, stats, and streak. This cannot be undone.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Reset',
          style: 'destructive',
          onPress: () => {
            resetProgress();
            Alert.alert('Done', 'Your progress has been reset.');
          },
        },
      ]
    );
  };

  const handleRestoreDefaults = () => {
    Alert.alert(
      'Restore Defaults',
      'This will reset all settings to their default values.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Restore',
          onPress: () => updateSettings(DEFAULT_SETTINGS),
        },
      ]
    );
  };

  const SettingRow: React.FC<{
    icon: keyof typeof Ionicons.glyphMap;
    title: string;
    subtitle?: string;
    value?: string;
    onPress?: () => void;
    toggle?: boolean;
    toggleValue?: boolean;
    onToggle?: () => void;
  }> = ({ icon, title, subtitle, value, onPress, toggle, toggleValue, onToggle }) => (
    <TouchableOpacity
      style={styles.settingRow}
      onPress={onPress}
      disabled={toggle || !onPress}
      activeOpacity={onPress ? 0.7 : 1}
    >
      <View style={styles.settingIconContainer}>
        <Ionicons name={icon} size={20} color={COLORS.primary} />
      </View>
      <View style={styles.settingContent}>
        <Text style={styles.settingTitle}>{title}</Text>
        {subtitle && <Text style={styles.settingSubtitle}>{subtitle}</Text>}
      </View>
      {toggle ? (
        <Switch
          value={toggleValue}
          onValueChange={onToggle}
          trackColor={{ false: COLORS.surfaceAlt, true: COLORS.primary + '60' }}
          thumbColor={toggleValue ? COLORS.primary : COLORS.textMuted}
        />
      ) : value ? (
        <View style={styles.settingValueContainer}>
          <Text style={styles.settingValue}>{value}</Text>
          <Ionicons name="chevron-forward" size={16} color={COLORS.textMuted} />
        </View>
      ) : onPress ? (
        <Ionicons name="chevron-forward" size={20} color={COLORS.textMuted} />
      ) : null}
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => router.back()}
        >
          <Ionicons name="arrow-back" size={24} color={COLORS.text} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Settings</Text>
        <View style={styles.headerSpacer} />
      </View>

      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Session Settings */}
        <Text style={styles.sectionTitle}>Session</Text>
        <Card variant="outlined" padding="none" style={styles.card}>
          <SettingRow
            icon="time-outline"
            title="Default Duration"
            subtitle="Starting session length"
            value={`${settings.defaultSessionLength} min`}
            onPress={handleDurationChange}
          />
          <View style={styles.divider} />
          <SettingRow
            icon="help-circle-outline"
            title="Quiz During Session"
            subtitle="Show questions while studying"
            toggle
            toggleValue={settings.quizDuringSession}
            onToggle={() => handleToggle('quizDuringSession')}
          />
          <View style={styles.divider} />
          <SettingRow
            icon="checkmark-circle-outline"
            title="Quiz After Session"
            subtitle="Review quiz at session end"
            toggle
            toggleValue={settings.quizAfterSession}
            onToggle={() => handleToggle('quizAfterSession')}
          />
          <View style={styles.divider} />
          <SettingRow
            icon="warning-outline"
            title="Wrong Answer Penalty"
            subtitle="Time added for mistakes"
            value={settings.penaltyMinutes === 0 ? 'None' : `${settings.penaltyMinutes} min`}
            onPress={handlePenaltyChange}
          />
        </Card>

        {/* Feedback Settings */}
        <Text style={styles.sectionTitle}>Feedback</Text>
        <Card variant="outlined" padding="none" style={styles.card}>
          <SettingRow
            icon="notifications-outline"
            title="Notifications"
            subtitle="Session reminders and streaks"
            toggle
            toggleValue={settings.notifications}
            onToggle={() => handleToggle('notifications')}
          />
          <View style={styles.divider} />
          <SettingRow
            icon="phone-portrait-outline"
            title="Haptics"
            subtitle="Vibration feedback"
            toggle
            toggleValue={settings.haptics}
            onToggle={() => handleToggle('haptics')}
          />
          <View style={styles.divider} />
          <SettingRow
            icon="volume-high-outline"
            title="Sound Effects"
            subtitle="Audio feedback"
            toggle
            toggleValue={settings.soundEnabled}
            onToggle={() => handleToggle('soundEnabled')}
          />
        </Card>

        {/* Account */}
        <Text style={styles.sectionTitle}>Account</Text>
        <Card variant="outlined" padding="none" style={styles.card}>
          <SettingRow
            icon="star-outline"
            title="StudyLock Pro"
            subtitle={progress.isPremium ? 'Active' : 'Unlock unlimited features'}
            onPress={() => router.push('/paywall')}
          />
          <View style={styles.divider} />
          <SettingRow
            icon="sync-outline"
            title="Restore Purchases"
            subtitle="Restore previous subscriptions"
            onPress={() => Alert.alert('Restore', 'Checking for previous purchases...')}
          />
        </Card>

        {/* Data */}
        <Text style={styles.sectionTitle}>Data</Text>
        <Card variant="outlined" padding="none" style={styles.card}>
          <SettingRow
            icon="refresh-outline"
            title="Restore Defaults"
            subtitle="Reset settings to default"
            onPress={handleRestoreDefaults}
          />
          <View style={styles.divider} />
          <SettingRow
            icon="trash-outline"
            title="Reset Progress"
            subtitle="Delete all study history"
            onPress={handleResetProgress}
          />
        </Card>

        {/* About */}
        <Text style={styles.sectionTitle}>About</Text>
        <Card variant="outlined" padding="none" style={styles.card}>
          <SettingRow
            icon="document-text-outline"
            title="Privacy Policy"
            onPress={() => {}}
          />
          <View style={styles.divider} />
          <SettingRow
            icon="shield-checkmark-outline"
            title="Terms of Service"
            onPress={() => {}}
          />
          <View style={styles.divider} />
          <SettingRow
            icon="information-circle-outline"
            title="Version"
            value="1.0.0"
          />
        </Card>

        <View style={styles.footer}>
          <Text style={styles.footerText}>StudyLock</Text>
          <Text style={styles.footerSubtext}>Study First, Scroll Later</Text>
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
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  backButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
  },
  headerSpacer: {
    width: 40,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: 16,
    paddingBottom: 40,
  },
  sectionTitle: {
    fontSize: 13,
    fontWeight: '600',
    color: COLORS.textSecondary,
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginTop: 24,
    marginBottom: 8,
    marginLeft: 4,
  },
  card: {
    overflow: 'hidden',
  },
  settingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
  },
  settingIconContainer: {
    width: 36,
    height: 36,
    borderRadius: 10,
    backgroundColor: COLORS.primary + '15',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
  },
  settingContent: {
    flex: 1,
  },
  settingTitle: {
    fontSize: 16,
    fontWeight: '500',
    color: COLORS.text,
  },
  settingSubtitle: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  settingValueContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  settingValue: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  divider: {
    height: 1,
    backgroundColor: COLORS.border,
    marginLeft: 64,
  },
  footer: {
    alignItems: 'center',
    marginTop: 40,
  },
  footerText: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.primary,
  },
  footerSubtext: {
    fontSize: 12,
    color: COLORS.textMuted,
    marginTop: 4,
  },
});
