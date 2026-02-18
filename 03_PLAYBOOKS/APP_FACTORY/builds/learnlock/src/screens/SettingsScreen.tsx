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
import Slider from '@react-native-community/slider';
import { COLORS, TYPOGRAPHY, SPACING, TIMER_PRESETS, EMERGENCY_UNLOCK_PHRASE } from '../utils/constants';
import { useUserStore } from '../stores/userStore';
import { useTimerStore } from '../stores/timerStore';
import { useStreakStore } from '../stores/streakStore';

interface Props {
  navigation?: any;
}

export function SettingsScreen({ navigation }: Props) {
  const {
    workDuration,
    breakDuration,
    notificationsEnabled,
    soundEnabled,
    vibrationEnabled,
    blockedApps,
    isSubscribed,
    setNotificationsEnabled,
    setSoundEnabled,
    setVibrationEnabled,
    getTrialDaysRemaining,
  } = useUserStore();

  const { setWorkDuration, setBreakDuration } = useTimerStore();
  const { resetStreak } = useStreakStore();

  const trialDaysRemaining = getTrialDaysRemaining();

  const handleWorkDurationChange = (value: number) => {
    setWorkDuration(Math.round(value));
  };

  const handleBreakDurationChange = (value: number) => {
    setBreakDuration(Math.round(value));
  };

  const applyPreset = (preset: typeof TIMER_PRESETS[0]) => {
    setWorkDuration(preset.workMinutes);
    setBreakDuration(preset.breakMinutes);
  };

  const handleEmergencyUnlock = () => {
    Alert.prompt(
      'Emergency Unlock',
      `Type "${EMERGENCY_UNLOCK_PHRASE}" to unlock.\n\nThis will end your current session and reset your streak.`,
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Unlock',
          style: 'destructive',
          onPress: (text) => {
            if (text === EMERGENCY_UNLOCK_PHRASE) {
              resetStreak();
              Alert.alert('Unlocked', 'Your session has been ended.');
            } else {
              Alert.alert('Error', 'Phrase did not match. Please try again.');
            }
          },
        },
      ],
      'plain-text'
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <Text style={styles.title}>Settings</Text>

        {/* Subscription Status */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Subscription</Text>
          <View style={styles.subscriptionCard}>
            {isSubscribed ? (
              <>
                <Text style={styles.subscriptionStatus}>Premium Active</Text>
                <Text style={styles.subscriptionDetail}>
                  All features unlocked
                </Text>
              </>
            ) : trialDaysRemaining > 0 ? (
              <>
                <Text style={styles.subscriptionStatus}>Free Trial</Text>
                <Text style={styles.subscriptionDetail}>
                  {trialDaysRemaining} days remaining
                </Text>
                <TouchableOpacity style={styles.upgradeButton}>
                  <Text style={styles.upgradeButtonText}>Upgrade Now</Text>
                </TouchableOpacity>
              </>
            ) : (
              <>
                <Text style={styles.subscriptionStatus}>Trial Expired</Text>
                <TouchableOpacity style={styles.upgradeButton}>
                  <Text style={styles.upgradeButtonText}>Subscribe</Text>
                </TouchableOpacity>
              </>
            )}
          </View>
        </View>

        {/* Timer Settings */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Timer</Text>

          {/* Presets */}
          <Text style={styles.label}>Quick Presets</Text>
          <View style={styles.presetsContainer}>
            {TIMER_PRESETS.map((preset) => (
              <TouchableOpacity
                key={preset.id}
                style={[
                  styles.presetButton,
                  workDuration === preset.workMinutes &&
                    breakDuration === preset.breakMinutes &&
                    styles.presetButtonActive,
                ]}
                onPress={() => applyPreset(preset)}
              >
                <Text
                  style={[
                    styles.presetName,
                    workDuration === preset.workMinutes &&
                      breakDuration === preset.breakMinutes &&
                      styles.presetNameActive,
                  ]}
                >
                  {preset.name}
                </Text>
                <Text style={styles.presetTime}>
                  {preset.workMinutes}/{preset.breakMinutes}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          {/* Work Duration Slider */}
          <View style={styles.sliderContainer}>
            <Text style={styles.label}>Work Duration</Text>
            <Text style={styles.sliderValue}>{workDuration} minutes</Text>
            <Slider
              style={styles.slider}
              minimumValue={5}
              maximumValue={60}
              step={5}
              value={workDuration}
              onValueChange={handleWorkDurationChange}
              minimumTrackTintColor={COLORS.primary}
              maximumTrackTintColor={COLORS.surfaceSecondary}
              thumbTintColor={COLORS.primary}
            />
          </View>

          {/* Break Duration Slider */}
          <View style={styles.sliderContainer}>
            <Text style={styles.label}>Break Duration</Text>
            <Text style={styles.sliderValue}>{breakDuration} minutes</Text>
            <Slider
              style={styles.slider}
              minimumValue={1}
              maximumValue={15}
              step={1}
              value={breakDuration}
              onValueChange={handleBreakDurationChange}
              minimumTrackTintColor={COLORS.secondary}
              maximumTrackTintColor={COLORS.surfaceSecondary}
              thumbTintColor={COLORS.secondary}
            />
          </View>
        </View>

        {/* Blocked Apps */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Blocked Apps</Text>
          <TouchableOpacity style={styles.row}>
            <Text style={styles.rowLabel}>Manage Blocked Apps</Text>
            <View style={styles.rowRight}>
              <Text style={styles.rowValue}>{blockedApps.length} apps</Text>
              <Text style={styles.chevron}>›</Text>
            </View>
          </TouchableOpacity>
        </View>

        {/* Notifications */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Notifications</Text>

          <View style={styles.row}>
            <Text style={styles.rowLabel}>Push Notifications</Text>
            <Switch
              value={notificationsEnabled}
              onValueChange={setNotificationsEnabled}
              trackColor={{
                false: COLORS.surfaceSecondary,
                true: COLORS.primaryLight,
              }}
              thumbColor={notificationsEnabled ? COLORS.primary : COLORS.surface}
            />
          </View>

          <View style={styles.row}>
            <Text style={styles.rowLabel}>Sound</Text>
            <Switch
              value={soundEnabled}
              onValueChange={setSoundEnabled}
              trackColor={{
                false: COLORS.surfaceSecondary,
                true: COLORS.primaryLight,
              }}
              thumbColor={soundEnabled ? COLORS.primary : COLORS.surface}
            />
          </View>

          <View style={styles.row}>
            <Text style={styles.rowLabel}>Vibration</Text>
            <Switch
              value={vibrationEnabled}
              onValueChange={setVibrationEnabled}
              trackColor={{
                false: COLORS.surfaceSecondary,
                true: COLORS.primaryLight,
              }}
              thumbColor={vibrationEnabled ? COLORS.primary : COLORS.surface}
            />
          </View>
        </View>

        {/* Emergency */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Emergency</Text>
          <TouchableOpacity
            style={styles.emergencyButton}
            onPress={handleEmergencyUnlock}
          >
            <Text style={styles.emergencyButtonText}>Emergency Unlock</Text>
          </TouchableOpacity>
          <Text style={styles.emergencyNote}>
            Use only in genuine emergencies. This will end your session and reset
            your streak.
          </Text>
        </View>

        {/* About */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>About</Text>
          <TouchableOpacity style={styles.row}>
            <Text style={styles.rowLabel}>Privacy Policy</Text>
            <Text style={styles.chevron}>›</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.row}>
            <Text style={styles.rowLabel}>Terms of Service</Text>
            <Text style={styles.chevron}>›</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.row}>
            <Text style={styles.rowLabel}>Contact Support</Text>
            <Text style={styles.chevron}>›</Text>
          </TouchableOpacity>
          <View style={styles.row}>
            <Text style={styles.rowLabel}>Version</Text>
            <Text style={styles.rowValue}>1.0.0</Text>
          </View>
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
  scrollView: {
    flex: 1,
  },
  content: {
    padding: SPACING.lg,
    paddingBottom: SPACING.xxl,
  },
  title: {
    ...TYPOGRAPHY.h1,
    color: COLORS.text,
    marginBottom: SPACING.xl,
  },
  section: {
    marginBottom: SPACING.xl,
  },
  sectionTitle: {
    ...TYPOGRAPHY.h3,
    color: COLORS.text,
    marginBottom: SPACING.md,
  },
  subscriptionCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.lg,
    alignItems: 'center',
  },
  subscriptionStatus: {
    ...TYPOGRAPHY.h3,
    color: COLORS.primary,
  },
  subscriptionDetail: {
    ...TYPOGRAPHY.bodySmall,
    color: COLORS.textSecondary,
    marginTop: SPACING.xs,
  },
  upgradeButton: {
    backgroundColor: COLORS.primary,
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.lg,
    borderRadius: 8,
    marginTop: SPACING.md,
  },
  upgradeButtonText: {
    ...TYPOGRAPHY.bodySmall,
    color: COLORS.surface,
    fontWeight: '600',
  },
  label: {
    ...TYPOGRAPHY.bodySmall,
    color: COLORS.textSecondary,
    marginBottom: SPACING.sm,
  },
  presetsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: SPACING.sm,
    marginBottom: SPACING.lg,
  },
  presetButton: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: SPACING.sm,
    paddingHorizontal: SPACING.md,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  presetButtonActive: {
    borderColor: COLORS.primary,
    backgroundColor: COLORS.primary + '10',
  },
  presetName: {
    ...TYPOGRAPHY.bodySmall,
    color: COLORS.text,
    fontWeight: '500',
  },
  presetNameActive: {
    color: COLORS.primary,
  },
  presetTime: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textTertiary,
  },
  sliderContainer: {
    marginBottom: SPACING.lg,
  },
  sliderValue: {
    ...TYPOGRAPHY.h3,
    color: COLORS.text,
    marginBottom: SPACING.sm,
  },
  slider: {
    width: '100%',
    height: 40,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
  },
  rowLabel: {
    ...TYPOGRAPHY.body,
    color: COLORS.text,
  },
  rowRight: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  rowValue: {
    ...TYPOGRAPHY.body,
    color: COLORS.textSecondary,
  },
  chevron: {
    ...TYPOGRAPHY.h2,
    color: COLORS.textTertiary,
    marginLeft: SPACING.sm,
  },
  emergencyButton: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: SPACING.md,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.error,
  },
  emergencyButtonText: {
    ...TYPOGRAPHY.body,
    color: COLORS.error,
    fontWeight: '500',
  },
  emergencyNote: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textTertiary,
    textAlign: 'center',
    marginTop: SPACING.sm,
  },
});
