import { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  TouchableOpacity,
  Switch,
  Alert,
  Linking,
} from 'react-native';
import { useRouter } from 'expo-router';
import { Card, Button } from '../../src/components/common';
import { COLORS, PREMIUM_HABITS } from '../../src/utils/constants';
import { useSettingsStore, useHabitStore } from '../../src/store';

export default function SettingsScreen() {
  const router = useRouter();
  const {
    reminderTime,
    reminderEnabled,
    isPremium,
    updateSettings,
  } = useSettingsStore();
  const { addHabit, habits } = useHabitStore();

  const handleToggleReminder = () => {
    updateSettings({ reminderEnabled: !reminderEnabled });
  };

  const handleChangeTime = () => {
    // In production, show a time picker
    Alert.alert(
      'Set reminder time',
      'Time picker would open here',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: '6:00 AM',
          onPress: () => updateSettings({ reminderTime: '06:00' }),
        },
        {
          text: '7:00 AM',
          onPress: () => updateSettings({ reminderTime: '07:00' }),
        },
        {
          text: '8:00 AM',
          onPress: () => updateSettings({ reminderTime: '08:00' }),
        },
      ]
    );
  };

  const handleAddPremiumHabit = () => {
    if (!isPremium) {
      router.push('/paywall');
      return;
    }

    const availableHabits = PREMIUM_HABITS.filter(
      (ph) => !habits.some((h) => h.name === ph.name)
    );

    if (availableHabits.length === 0) {
      Alert.alert('All habits added', 'You have added all available habits.');
      return;
    }

    Alert.alert(
      'Add habit',
      'Choose a habit to add:',
      [
        { text: 'Cancel', style: 'cancel' },
        ...availableHabits.slice(0, 4).map((h) => ({
          text: h.name,
          onPress: () => addHabit(h),
        })),
      ]
    );
  };

  const handleContact = () => {
    Linking.openURL('mailto:support@dailyanchor.app');
  };

  const handlePrivacy = () => {
    router.push('/privacy');
  };

  const handleTerms = () => {
    router.push('/terms');
  };

  const handleUpgrade = () => {
    router.push('/paywall');
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        <Text style={styles.title}>Settings</Text>

        {!isPremium && (
          <TouchableOpacity
            style={styles.premiumBanner}
            onPress={handleUpgrade}
            activeOpacity={0.8}
          >
            <View style={styles.premiumContent}>
              <Text style={styles.premiumEmoji}>{'\u{2728}'}</Text>
              <View style={styles.premiumText}>
                <Text style={styles.premiumTitle}>Upgrade to Premium</Text>
                <Text style={styles.premiumSubtitle}>
                  Unlock all habits and features
                </Text>
              </View>
            </View>
            <Text style={styles.premiumArrow}>{'\u{203A}'}</Text>
          </TouchableOpacity>
        )}

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Reminders</Text>
          <Card>
            <View style={styles.settingRow}>
              <View>
                <Text style={styles.settingLabel}>Daily reminder</Text>
                <Text style={styles.settingValue}>
                  {reminderEnabled ? `At ${reminderTime}` : 'Disabled'}
                </Text>
              </View>
              <Switch
                value={reminderEnabled}
                onValueChange={handleToggleReminder}
                trackColor={{ true: COLORS.primary }}
              />
            </View>

            {reminderEnabled && (
              <TouchableOpacity
                style={styles.settingRow}
                onPress={handleChangeTime}
              >
                <Text style={styles.settingLabel}>Time</Text>
                <View style={styles.settingAction}>
                  <Text style={styles.settingValue}>{reminderTime}</Text>
                  <Text style={styles.chevron}>{'\u{203A}'}</Text>
                </View>
              </TouchableOpacity>
            )}
          </Card>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Habits</Text>
          <Card>
            <TouchableOpacity
              style={styles.settingRow}
              onPress={handleAddPremiumHabit}
            >
              <View>
                <Text style={styles.settingLabel}>Add habit</Text>
                <Text style={styles.settingValue}>
                  {isPremium ? 'Choose from premium habits' : 'Premium feature'}
                </Text>
              </View>
              <View style={styles.settingAction}>
                {!isPremium && (
                  <View style={styles.premiumBadge}>
                    <Text style={styles.premiumBadgeText}>PRO</Text>
                  </View>
                )}
                <Text style={styles.chevron}>{'\u{203A}'}</Text>
              </View>
            </TouchableOpacity>
          </Card>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Support</Text>
          <Card>
            <TouchableOpacity style={styles.settingRow} onPress={handleContact}>
              <Text style={styles.settingLabel}>Contact us</Text>
              <Text style={styles.chevron}>{'\u{203A}'}</Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.settingRow} onPress={handlePrivacy}>
              <Text style={styles.settingLabel}>Privacy policy</Text>
              <Text style={styles.chevron}>{'\u{203A}'}</Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.settingRow} onPress={handleTerms}>
              <Text style={styles.settingLabel}>Terms of service</Text>
              <Text style={styles.chevron}>{'\u{203A}'}</Text>
            </TouchableOpacity>
          </Card>
        </View>

        <View style={styles.footer}>
          <Text style={styles.version}>DailyAnchor v1.0.0</Text>
          {isPremium && (
            <View style={styles.premiumStatus}>
              <Text style={styles.premiumStatusText}>
                {'\u{2728}'} Premium active
              </Text>
            </View>
          )}
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
  scroll: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 40,
  },
  title: {
    fontSize: 28,
    fontWeight: '800',
    color: COLORS.text,
    marginBottom: 24,
  },
  premiumBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#EEF2FF',
    borderRadius: 16,
    padding: 16,
    marginBottom: 24,
    borderWidth: 2,
    borderColor: COLORS.primary,
  },
  premiumContent: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  premiumEmoji: {
    fontSize: 32,
    marginRight: 12,
  },
  premiumText: {},
  premiumTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 2,
  },
  premiumSubtitle: {
    fontSize: 13,
    color: COLORS.textSecondary,
  },
  premiumArrow: {
    fontSize: 24,
    color: COLORS.primary,
    fontWeight: 'bold',
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.textSecondary,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
    marginBottom: 12,
  },
  settingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  settingLabel: {
    fontSize: 16,
    color: COLORS.text,
  },
  settingValue: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  settingAction: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  chevron: {
    fontSize: 20,
    color: COLORS.textSecondary,
    marginLeft: 8,
  },
  premiumBadge: {
    backgroundColor: COLORS.primary,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
  },
  premiumBadgeText: {
    fontSize: 10,
    fontWeight: '700',
    color: '#FFFFFF',
  },
  footer: {
    alignItems: 'center',
    marginTop: 32,
  },
  version: {
    fontSize: 13,
    color: COLORS.textSecondary,
  },
  premiumStatus: {
    marginTop: 8,
  },
  premiumStatusText: {
    fontSize: 14,
    color: COLORS.primary,
    fontWeight: '600',
  },
});
