import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  SafeAreaView,
  Linking,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { useFocusEffect, useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Colors, Spacing, Radius, Typography } from '../constants/theme';
import { getSettings, saveSettings, clearAllData } from '../services/storage';
import { AppSettings, RootStackParamList } from '../types';

type NavProp = NativeStackNavigationProp<RootStackParamList>;

const PRIVACY_URL = 'https://printmaxx-privacy.surge.sh';
const TERMS_URL = 'https://printmaxx-tos.surge.sh';
const SUPPORT_EMAIL = 'support@printmaxx.co';

export default function SettingsScreen() {
  const navigation = useNavigation<NavProp>();
  const [settings, setSettings] = useState<AppSettings | null>(null);

  useFocusEffect(useCallback(() => {
    getSettings().then(setSettings);
  }, []));

  const toggleReminder = async () => {
    if (!settings) return;
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    const updated = { ...settings, reminderEnabled: !settings.reminderEnabled };
    await saveSettings({ reminderEnabled: updated.reminderEnabled });
    setSettings(updated);
  };

  const toggleMvd = async () => {
    if (!settings) return;
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    const updated = { ...settings, mvdMode: !settings.mvdMode };
    await saveSettings({ mvdMode: updated.mvdMode });
    setSettings(updated);
  };

  const handleClearData = () => {
    Alert.alert(
      'Clear all data?',
      'This deletes all habits, streaks, and settings. Cannot be undone.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Clear everything',
          style: 'destructive',
          onPress: async () => {
            await clearAllData();
            navigation.replace('Onboarding');
          },
        },
      ],
    );
  };

  if (!settings) return null;

  return (
    <SafeAreaView style={s.container}>
      <View style={s.header}>
        <Text style={s.headerTitle}>Settings</Text>
        {!settings.isPremium && (
          <TouchableOpacity
            style={s.upgradePill}
            onPress={() => navigation.navigate('Paywall', { source: 'settings' })}
          >
            <Text style={s.upgradePillText}>Go Pro</Text>
          </TouchableOpacity>
        )}
      </View>

      <ScrollView contentContainerStyle={s.scroll} showsVerticalScrollIndicator={false}>
        {/* Plan status */}
        <View style={[s.card, settings.isPremium ? s.cardPro : s.cardFree]}>
          <Text style={s.planEmoji}>{settings.isPremium ? '🔥' : '🌱'}</Text>
          <View style={{ flex: 1 }}>
            <Text style={s.planTitle}>{settings.isPremium ? 'Streakr Pro' : 'Free plan'}</Text>
            <Text style={s.planSub}>
              {settings.isPremium ? 'Unlimited habits, full history, streak repair.' : 'Up to 3 habits. Upgrade to unlock everything.'}
            </Text>
          </View>
          {!settings.isPremium && (
            <TouchableOpacity onPress={() => navigation.navigate('Paywall', { source: 'settings' })}>
              <Text style={s.upgradeLink}>Upgrade</Text>
            </TouchableOpacity>
          )}
        </View>

        {/* Preferences */}
        <Text style={s.sectionLabel}>Preferences</Text>
        <View style={s.section}>
          <SettingRow
            icon="notifications-outline"
            label="Daily reminder"
            sub="Get a nudge at your chosen time"
            toggle={settings.reminderEnabled}
            onToggle={toggleReminder}
          />
          <View style={s.divider} />
          <SettingRow
            icon="shield-checkmark-outline"
            label="Minimum Viable Day mode"
            sub="Define the minimum that still counts as a win"
            toggle={settings.mvdMode}
            onToggle={toggleMvd}
          />
        </View>

        {/* Support */}
        <Text style={s.sectionLabel}>Support</Text>
        <View style={s.section}>
          <SettingLink
            icon="mail-outline"
            label="Contact support"
            onPress={() => Linking.openURL(`mailto:${SUPPORT_EMAIL}?subject=Streakr Support`)}
          />
          <View style={s.divider} />
          <SettingLink
            icon="lock-closed-outline"
            label="Privacy policy"
            onPress={() => Linking.openURL(PRIVACY_URL)}
          />
          <View style={s.divider} />
          <SettingLink
            icon="document-text-outline"
            label="Terms of use"
            onPress={() => Linking.openURL(TERMS_URL)}
          />
        </View>

        {/* Danger */}
        <Text style={s.sectionLabel}>Data</Text>
        <View style={s.section}>
          <TouchableOpacity style={s.dangerRow} onPress={handleClearData}>
            <Ionicons name="trash-outline" size={20} color="#EF4444" />
            <Text style={s.dangerText}>Clear all data</Text>
          </TouchableOpacity>
        </View>

        <Text style={s.footer}>
          Streakr v1.0 · No account · Everything stored on your device · Nothing leaves.
        </Text>
      </ScrollView>
    </SafeAreaView>
  );
}

function SettingRow({
  icon,
  label,
  sub,
  toggle,
  onToggle,
}: {
  icon: string;
  label: string;
  sub: string;
  toggle: boolean;
  onToggle: () => void;
}) {
  return (
    <View style={s.settingRow}>
      <Ionicons name={icon as any} size={20} color={Colors.textMuted} style={{ marginTop: 1 }} />
      <View style={{ flex: 1 }}>
        <Text style={s.settingLabel}>{label}</Text>
        <Text style={s.settingSub}>{sub}</Text>
      </View>
      <TouchableOpacity
        style={[s.toggle, toggle && s.toggleOn]}
        onPress={onToggle}
      >
        <View style={[s.toggleThumb, toggle && s.toggleThumbOn]} />
      </TouchableOpacity>
    </View>
  );
}

function SettingLink({ icon, label, onPress }: { icon: string; label: string; onPress: () => void }) {
  return (
    <TouchableOpacity style={s.settingRow} onPress={onPress} activeOpacity={0.7}>
      <Ionicons name={icon as any} size={20} color={Colors.textMuted} />
      <Text style={[s.settingLabel, { flex: 1 }]}>{label}</Text>
      <Ionicons name="chevron-forward" size={16} color={Colors.textLight} />
    </TouchableOpacity>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.bg },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: Spacing.lg,
    paddingTop: Spacing.md,
    paddingBottom: Spacing.sm,
  },
  headerTitle: { ...Typography.h1, color: Colors.text },
  upgradePill: {
    backgroundColor: Colors.emerald,
    borderRadius: Radius.full,
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  upgradePillText: { ...Typography.captionMed, color: '#fff' },
  scroll: { padding: Spacing.lg, paddingBottom: 48 },
  // Plan card
  card: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 14,
    borderRadius: Radius.lg,
    padding: 18,
    borderWidth: 1,
    marginBottom: Spacing.md,
  },
  cardFree: { backgroundColor: Colors.bgCard, borderColor: Colors.border },
  cardPro: { backgroundColor: Colors.emeraldSubtle, borderColor: Colors.emeraldLight },
  planEmoji: { fontSize: 28 },
  planTitle: { ...Typography.bodyMed, color: Colors.text },
  planSub: { ...Typography.caption, color: Colors.textMuted, marginTop: 2, lineHeight: 18 },
  upgradeLink: { ...Typography.bodyMed, color: Colors.emerald, fontWeight: '700' },
  // Section
  sectionLabel: {
    ...Typography.captionMed,
    color: Colors.textMuted,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
    marginBottom: 8,
    marginTop: Spacing.md,
  },
  section: {
    backgroundColor: Colors.bgCard,
    borderRadius: Radius.lg,
    borderWidth: 1,
    borderColor: Colors.border,
    overflow: 'hidden',
  },
  divider: { height: 1, backgroundColor: Colors.borderLight, marginLeft: 50 },
  settingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    padding: 16,
  },
  settingLabel: { ...Typography.bodyMed, color: Colors.text },
  settingSub: { ...Typography.caption, color: Colors.textMuted, marginTop: 2 },
  // Toggle
  toggle: {
    width: 50,
    height: 28,
    borderRadius: 14,
    backgroundColor: Colors.border,
    justifyContent: 'center',
    paddingHorizontal: 3,
  },
  toggleOn: { backgroundColor: Colors.emerald },
  toggleThumb: {
    width: 22,
    height: 22,
    borderRadius: 11,
    backgroundColor: '#fff',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.15,
    shadowRadius: 2,
    elevation: 2,
  },
  toggleThumbOn: { alignSelf: 'flex-end' },
  // Danger
  dangerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    padding: 16,
  },
  dangerText: { ...Typography.bodyMed, color: '#EF4444' },
  footer: {
    ...Typography.caption,
    color: Colors.textLight,
    textAlign: 'center',
    marginTop: Spacing.xl,
    lineHeight: 18,
  },
});
