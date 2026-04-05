import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,

  Alert,
  Linking,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SoundTouchable as TouchableOpacity } from '../components/SoundTouchable';
import { colors, spacing, radii, typography } from '../theme';
import { getProfile, getSessions, saveProfile } from '../store';
import { UserProfile } from '../utils/types';
import { PRIVACY_POLICY_URL, TERMS_URL } from '../legal/disclaimer';

export function SettingsScreen({ navigation }: { navigation: any }) {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [sessionCount, setSessionCount] = useState(0);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const p = await getProfile();
    const s = await getSessions();
    setProfile(p);
    setSessionCount(s.length);
  };

  const handleResetBaseline = () => {
    Alert.alert(
      'Reset Baseline',
      'This will clear your calibration data. You\'ll need to recalibrate for accurate results.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Reset',
          style: 'destructive',
          onPress: async () => {
            await saveProfile({
              baselineHR: undefined,
              baselineHRV: undefined,
              baselineVoiceF0: undefined,
            });
            loadData();
          },
        },
      ]
    );
  };

  const handleRestorePurchases = () => {
    Alert.alert('Restore Purchases', 'Purchase restoration will be available when the app is published to the App Store.');
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color={colors.text.primary} />
        </TouchableOpacity>
        <Text style={styles.title}>Settings</Text>
        <View style={{ width: 40 }} />
      </View>

      {/* Account */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Account</Text>
        <View style={styles.card}>
          <SettingRow
            icon="shield-checkmark"
            label="Subscription"
            value={profile?.isPremium ? 'Premium' : 'Free'}
            valueColor={profile?.isPremium ? colors.accent.secondary : colors.text.tertiary}
          />
          <SettingRow icon="analytics" label="Sessions" value={`${sessionCount}`} />
          <TouchableOpacity onPress={handleRestorePurchases}>
            <SettingRow icon="refresh" label="Restore Purchases" chevron />
          </TouchableOpacity>
        </View>
      </View>

      {/* Calibration */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Calibration</Text>
        <View style={styles.card}>
          <SettingRow
            icon="heart"
            label="Baseline HR"
            value={profile?.baselineHR ? `${profile.baselineHR} BPM` : 'Not set'}
          />
          <SettingRow
            icon="pulse"
            label="Baseline HRV"
            value={profile?.baselineHRV ? `${profile.baselineHRV} ms` : 'Not set'}
          />
          <TouchableOpacity onPress={handleResetBaseline}>
            <SettingRow icon="refresh-circle" label="Reset Baseline" chevron />
          </TouchableOpacity>
          <TouchableOpacity onPress={() => navigation.navigate('Detection', { mode: 'finger' })}>
            <SettingRow icon="finger-print" label="Recalibrate" chevron />
          </TouchableOpacity>
        </View>
      </View>

      {/* About */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>About</Text>
        <View style={styles.card}>
          <SettingRow icon="information-circle" label="Version" value="1.0.0" />
          <TouchableOpacity onPress={() => Linking.openURL(PRIVACY_POLICY_URL)}>
            <SettingRow icon="lock-closed" label="Privacy Policy" chevron />
          </TouchableOpacity>
          <TouchableOpacity onPress={() => Linking.openURL(TERMS_URL)}>
            <SettingRow icon="document-text" label="Terms of Service" chevron />
          </TouchableOpacity>
        </View>
      </View>

      {/* Science */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>The Science</Text>
        <View style={styles.scienceCard}>
          <Text style={styles.scienceText}>
            TruthScope uses three evidence-based biometric analysis techniques:
          </Text>
          <View style={styles.scienceItem}>
            <Text style={styles.scienceLabel}>Photoplethysmography (PPG)</Text>
            <Text style={styles.scienceDesc}>
              Measures heart rate and variability through light absorption changes in blood vessels.
              The same principle used in medical pulse oximeters.
            </Text>
          </View>
          <View style={styles.scienceItem}>
            <Text style={styles.scienceLabel}>Voice Stress Analysis</Text>
            <Text style={styles.scienceDesc}>
              Analyzes micro-tremors, pitch variation, and vocal quality changes associated with
              cognitive load and emotional arousal.
            </Text>
          </View>
          <View style={styles.scienceItem}>
            <Text style={styles.scienceLabel}>Facial Behavior Analysis</Text>
            <Text style={styles.scienceDesc}>
              Tracks blink rate, gaze patterns, micro-expressions, and facial asymmetry based on
              Paul Ekman's Facial Action Coding System research.
            </Text>
          </View>
        </View>
      </View>

      <Text style={styles.footer}>
        TruthScope is for entertainment and educational purposes only.
        {'\n'}Not a replacement for professional lie detection.
      </Text>
    </ScrollView>
  );
}

function SettingRow({
  icon,
  label,
  value,
  valueColor,
  chevron,
}: {
  icon: keyof typeof Ionicons.glyphMap;
  label: string;
  value?: string;
  valueColor?: string;
  chevron?: boolean;
}) {
  return (
    <View style={styles.settingRow}>
      <Ionicons name={icon} size={20} color={colors.accent.primary} />
      <Text style={styles.settingLabel}>{label}</Text>
      {value && (
        <Text style={[styles.settingValue, valueColor ? { color: valueColor } : undefined]}>
          {value}
        </Text>
      )}
      {chevron && (
        <Ionicons name="chevron-forward" size={16} color={colors.text.tertiary} />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.bg.primary,
  },
  content: {
    padding: spacing.lg,
    paddingTop: 60,
    paddingBottom: 40,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: spacing.xl,
  },
  backButton: {
    padding: 8,
  },
  title: {
    ...typography.h1,
    color: colors.text.primary,
  },
  section: {
    marginBottom: spacing.lg,
  },
  sectionTitle: {
    ...typography.caption,
    color: colors.text.tertiary,
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: spacing.sm,
    marginLeft: spacing.xs,
  },
  card: {
    backgroundColor: colors.bg.card,
    borderRadius: radii.md,
    padding: spacing.sm,
    gap: 2,
  },
  settingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    padding: spacing.sm,
    borderRadius: radii.sm,
  },
  settingLabel: {
    ...typography.body,
    color: colors.text.primary,
    flex: 1,
  },
  settingValue: {
    ...typography.caption,
    color: colors.text.secondary,
  },
  scienceCard: {
    backgroundColor: colors.bg.card,
    borderRadius: radii.md,
    padding: spacing.md,
    gap: spacing.md,
  },
  scienceText: {
    ...typography.body,
    color: colors.text.secondary,
  },
  scienceItem: {
    gap: 4,
  },
  scienceLabel: {
    ...typography.bodyBold,
    color: colors.accent.primary,
    fontSize: 14,
  },
  scienceDesc: {
    ...typography.small,
    color: colors.text.tertiary,
    lineHeight: 18,
  },
  footer: {
    ...typography.small,
    color: colors.text.tertiary,
    textAlign: 'center',
    lineHeight: 18,
    marginTop: spacing.lg,
  },
});
