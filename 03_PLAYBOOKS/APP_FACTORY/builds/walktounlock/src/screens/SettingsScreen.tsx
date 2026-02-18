import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  Text,
  SafeAreaView,
  ScrollView,
  Alert,
  Modal,
  Pressable,
} from 'react-native';
import { COLORS, SPACING, BORDER_RADIUS, STEP_GOALS } from '../constants/theme';
import { SettingRow, Button } from '../components';
import { useApp } from '../context/AppContext';
import { clearAllData } from '../utils/storage';
import type { CompositeNavigationProp } from '@react-navigation/native';
import type { BottomTabNavigationProp } from '@react-navigation/bottom-tabs';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { MainTabParamList, RootStackParamList } from '../constants/types';

type SettingsNavigationProp = CompositeNavigationProp<
  BottomTabNavigationProp<MainTabParamList, 'Settings'>,
  NativeStackNavigationProp<RootStackParamList>
>;

interface SettingsScreenProps {
  navigation: SettingsNavigationProp;
}

const STEP_GOAL_OPTIONS = [
  { label: 'Easy (100 steps)', value: 100 },
  { label: 'Medium (500 steps)', value: 500 },
  { label: 'Hard (1,000 steps)', value: 1000 },
  { label: 'Extreme (2,000 steps)', value: 2000 },
];

export const SettingsScreen: React.FC<SettingsScreenProps> = ({ navigation }) => {
  const { settings, isPremium, updateSettings, refreshData } = useApp();
  const [showGoalPicker, setShowGoalPicker] = useState(false);

  const handleUpgrade = () => {
    navigation.navigate('Paywall');
  };

  const handleResetData = () => {
    Alert.alert(
      'Reset All Data',
      'This will delete all your progress, achievements, and settings. This action cannot be undone.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Reset',
          style: 'destructive',
          onPress: async () => {
            await clearAllData();
            await refreshData();
            Alert.alert('Data Reset', 'All data has been cleared.');
          },
        },
      ]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        <Text style={styles.title}>Settings</Text>

        {!isPremium && (
          <Pressable style={styles.premiumBanner} onPress={handleUpgrade}>
            <View style={styles.premiumContent}>
              <Text style={styles.premiumTitle}>Upgrade to Premium</Text>
              <Text style={styles.premiumSubtitle}>
                Unlock unlimited goals, all achievements, and more!
              </Text>
            </View>
            <Text style={styles.premiumArrow}>{'\u203A'}</Text>
          </Pressable>
        )}

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Step Goal</Text>

          <SettingRow
            title="Daily Step Goal"
            subtitle="Steps required to unlock"
            type="value"
            value={`${settings.stepGoal.toLocaleString()} steps`}
            onPress={() => setShowGoalPicker(true)}
          />

          <SettingRow
            title="Weekend Goal"
            subtitle="Different goal for weekends"
            type="value"
            value={`${settings.weekendStepGoal.toLocaleString()} steps`}
            onPress={() => {
              if (!isPremium) {
                Alert.alert(
                  'Premium Feature',
                  'Weekend goals require a premium subscription.',
                  [
                    { text: 'Cancel', style: 'cancel' },
                    { text: 'Upgrade', onPress: handleUpgrade },
                  ]
                );
              }
            }}
            disabled={!isPremium}
          />
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Lock Settings</Text>

          <SettingRow
            title="Lock Enabled"
            subtitle="Enable step-gated lock"
            type="toggle"
            value={settings.lockEnabled}
            onToggle={(value) => updateSettings({ lockEnabled: value })}
          />

          <SettingRow
            title="Lock Start Time"
            subtitle="When the lock activates"
            type="value"
            value={settings.lockStartTime}
            disabled={!isPremium}
            onPress={() => {
              if (!isPremium) {
                Alert.alert(
                  'Premium Feature',
                  'Custom lock times require a premium subscription.',
                  [
                    { text: 'Cancel', style: 'cancel' },
                    { text: 'Upgrade', onPress: handleUpgrade },
                  ]
                );
              }
            }}
          />

          <SettingRow
            title="Lock End Time"
            subtitle="When the lock deactivates"
            type="value"
            value={settings.lockEndTime}
            disabled={!isPremium}
            onPress={() => {
              if (!isPremium) {
                Alert.alert(
                  'Premium Feature',
                  'Custom lock times require a premium subscription.',
                  [
                    { text: 'Cancel', style: 'cancel' },
                    { text: 'Upgrade', onPress: handleUpgrade },
                  ]
                );
              }
            }}
          />
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Preferences</Text>

          <SettingRow
            title="Haptic Feedback"
            subtitle="Vibrate on milestones"
            type="toggle"
            value={settings.hapticFeedback}
            onToggle={(value) => updateSettings({ hapticFeedback: value })}
          />

          <SettingRow
            title="Notifications"
            subtitle="Reminders and achievements"
            type="toggle"
            value={settings.notifications}
            onToggle={(value) => updateSettings({ notifications: value })}
          />
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Data</Text>

          <SettingRow
            title="Export Data"
            subtitle="Download your step history"
            type="action"
            onPress={() => Alert.alert('Coming Soon', 'Data export will be available in a future update.')}
          />

          <SettingRow
            title="Reset All Data"
            subtitle="Delete all progress and settings"
            type="action"
            onPress={handleResetData}
          />
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>About</Text>

          <SettingRow
            title="Version"
            type="value"
            value="1.0.0"
            showArrow={false}
          />

          <SettingRow
            title="Privacy Policy"
            type="action"
            onPress={() => Alert.alert('Privacy Policy', 'Opening privacy policy...')}
          />

          <SettingRow
            title="Terms of Service"
            type="action"
            onPress={() => Alert.alert('Terms of Service', 'Opening terms of service...')}
          />

          <SettingRow
            title="Contact Support"
            type="action"
            onPress={() => Alert.alert('Support', 'Email: support@walktounlock.app')}
          />
        </View>

        <View style={styles.footer}>
          <Text style={styles.footerText}>Walk first, scroll second.</Text>
          <Text style={styles.footerSubtext}>WalkToUnlock v1.0.0</Text>
        </View>
      </ScrollView>

      <Modal
        visible={showGoalPicker}
        transparent
        animationType="slide"
        onRequestClose={() => setShowGoalPicker(false)}
      >
        <Pressable
          style={styles.modalOverlay}
          onPress={() => setShowGoalPicker(false)}
        >
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Select Step Goal</Text>

            {STEP_GOAL_OPTIONS.map((option) => {
              const isLocked = !isPremium && option.value > STEP_GOALS.easy;

              return (
                <Pressable
                  key={option.value}
                  style={[
                    styles.goalOption,
                    settings.stepGoal === option.value && styles.goalOptionSelected,
                    isLocked && styles.goalOptionLocked,
                  ]}
                  onPress={() => {
                    if (isLocked) {
                      setShowGoalPicker(false);
                      Alert.alert(
                        'Premium Feature',
                        'Higher step goals require a premium subscription.',
                        [
                          { text: 'Cancel', style: 'cancel' },
                          { text: 'Upgrade', onPress: handleUpgrade },
                        ]
                      );
                    } else {
                      updateSettings({ stepGoal: option.value });
                      setShowGoalPicker(false);
                    }
                  }}
                >
                  <Text
                    style={[
                      styles.goalOptionText,
                      settings.stepGoal === option.value &&
                        styles.goalOptionTextSelected,
                      isLocked && styles.goalOptionTextLocked,
                    ]}
                  >
                    {option.label}
                  </Text>
                  {isLocked && <Text style={styles.lockIcon}>{'\u{1F512}'}</Text>}
                  {settings.stepGoal === option.value && !isLocked && (
                    <Text style={styles.checkmark}>{'\u2713'}</Text>
                  )}
                </Pressable>
              );
            })}

            <Button
              title="Cancel"
              variant="ghost"
              fullWidth
              onPress={() => setShowGoalPicker(false)}
              style={{ marginTop: SPACING.md }}
            />
          </View>
        </Pressable>
      </Modal>
    </SafeAreaView>
  );
};

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
    fontSize: 32,
    fontWeight: '800',
    color: COLORS.text,
    letterSpacing: -1,
    marginBottom: SPACING.lg,
  },
  premiumBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.primary,
    borderRadius: BORDER_RADIUS.lg,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
  },
  premiumContent: {
    flex: 1,
  },
  premiumTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.background,
  },
  premiumSubtitle: {
    fontSize: 14,
    color: COLORS.background,
    opacity: 0.8,
    marginTop: 2,
  },
  premiumArrow: {
    fontSize: 24,
    color: COLORS.background,
    fontWeight: '300',
  },
  section: {
    marginBottom: SPACING.lg,
  },
  sectionTitle: {
    fontSize: 13,
    fontWeight: '600',
    color: COLORS.textSecondary,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
    marginBottom: SPACING.sm,
    marginLeft: SPACING.xs,
  },
  footer: {
    alignItems: 'center',
    marginTop: SPACING.xl,
    paddingTop: SPACING.lg,
    borderTopWidth: 1,
    borderTopColor: COLORS.backgroundLighter,
  },
  footerText: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  footerSubtext: {
    fontSize: 12,
    color: COLORS.textMuted,
    marginTop: SPACING.xs,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: COLORS.surface,
    borderTopLeftRadius: BORDER_RADIUS.xl,
    borderTopRightRadius: BORDER_RADIUS.xl,
    padding: SPACING.lg,
    paddingBottom: SPACING.xxl,
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: SPACING.lg,
  },
  goalOption: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: SPACING.md,
    borderRadius: BORDER_RADIUS.md,
    marginBottom: SPACING.sm,
    backgroundColor: COLORS.backgroundLight,
  },
  goalOptionSelected: {
    backgroundColor: COLORS.primary,
  },
  goalOptionLocked: {
    opacity: 0.6,
  },
  goalOptionText: {
    fontSize: 16,
    fontWeight: '500',
    color: COLORS.text,
  },
  goalOptionTextSelected: {
    color: COLORS.background,
  },
  goalOptionTextLocked: {
    color: COLORS.textMuted,
  },
  lockIcon: {
    fontSize: 14,
  },
  checkmark: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.background,
  },
});
