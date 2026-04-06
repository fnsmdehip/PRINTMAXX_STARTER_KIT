import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, Alert, Linking } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SoundTouchable as TouchableOpacity } from '../components/SoundTouchable';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { playSound } from '../sounds/SoundEngine';
import { colors, spacing, radii, typography } from '../theme';
import { getProfile, getSessions, saveProfile } from '../store';
import { UserProfile } from '../utils/types';
import { PRIVACY_POLICY_URL, TERMS_URL } from '../legal/disclaimer';

function SettingRow({ icon, label, value, valueColor, chevron }: {
  icon: keyof typeof Ionicons.glyphMap; label: string; value?: string; valueColor?: string; chevron?: boolean;
}) {
  return (
    <View style={styles.settingRow}>
      <Ionicons name={icon} size={20} color={colors.accent.primary} />
      <Text style={styles.settingLabel}>{label}</Text>
      {value && <Text style={[styles.settingValue, valueColor ? { color: valueColor } : undefined]}>{value}</Text>}
      {chevron && <Ionicons name="chevron-forward" size={16} color={colors.text.tertiary} />}
    </View>
  );
}

export function SettingsScreen({ navigation }: { navigation: any }) {
  const insets = useSafeAreaInsets();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [sessionCount, setSessionCount] = useState(0);

  useEffect(() => { loadData(); }, []);

  const loadData = async () => {
    const [p, s] = await Promise.all([getProfile(), getSessions()]);
    setProfile(p);
    setSessionCount(s.length);
  };

  const handleResetBaseline = () => {
    playSound('error');
    Alert.alert('Reset Baseline', "This will clear your calibration data. You'll need to recalibrate for accurate results.", [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Reset', style: 'destructive', onPress: async () => {
        await saveProfile({ baselineHR: undefined, baselineHRV: undefined, baselineVoiceF0: undefined });
        playSound('success');
        loadData();
      }},
    ]);
  };

  const handleRestorePurchases = () => {
    playSound('premium');
    Alert.alert('Restore Purchases', 'Purchase restoration will be available when the app is published to the App Store.');
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={[styles.content, { paddingTop: insets.top + spacing.md }]}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => { playSound('swipe'); navigation.goBack(); }} style={styles.backButton} sound="tap">
          <Ionicons name="arrow-back" size={24} color={colors.text.primary} />
        </TouchableOpacity>
        <Text style={styles.title}>Settings</Text>
        <View style={{ width: 40 }} />
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Account</Text>
        <View style={styles.card}>
          <SettingRow icon="shield-checkmark" label="Subscription"
            value={profile?.isPremium ? 'Premium' : 'Free'}
            valueColor={profile?.isPremium ? colors.accent.secondary : colors.text.tertiary} />
          <SettingRow icon="analytics" label="Sessions" value={`${sessionCount}`} />
          <TouchableOpacity onPress={handleRestorePurchases} sound="tap">
            <SettingRow icon="refresh" label="Restore Purchases" chevron />
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Calibration</Text>
        <View style={styles.card}>
          <SettingRow icon="heart" label="Baseline HR" value={profile?.baselineHR ? `${profile.baselineHR} BPM` : 'Not set'} />
          <SettingRow icon="pulse" label="Baseline HRV" value={profile?.baselineHRV ? `${profile.baselineHRV} ms` : 'Not set'} />
          <TouchableOpacity onPress={handleResetBaseline} sound="tap">
            <SettingRow icon="refresh-circle" label="Reset Baseline" chevron />
          </TouchableOpacity>
          <TouchableOpacity onPress={() => { playSound('calibrateStart'); navigation.navigate('Detection', { mode: 'finger' }); }} sound="tap">
            <SettingRow icon="finger-print" label="Recalibrate" chevron />
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>About</Text>
        <View style={styles.card}>
          <SettingRow icon="information-circle" label="Version" value="2.0.0" />
          <TouchableOpacity onPress={() => Linking.openURL(PRIVACY_POLICY_URL)} sound="tap">
            <SettingRow icon="lock-closed" label="Privacy Policy" chevron />
          </TouchableOpacity>
          <TouchableOpacity onPress={() => Linking.openURL(TERMS_URL)} sound="tap">
            <SettingRow icon="document-text" label="Terms of Service" chevron />
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>The Science</Text>
        <View style={styles.scienceCard}>
          <Text style={styles.scienceText}>TruthScope uses three evidence-based biometric analysis techniques:</Text>
          {[
            { label: 'Photoplethysmography (PPG)', desc: 'Measures heart rate and variability through light absorption changes. Same principle used in medical pulse oximeters. Phone accuracy: 55-65%.' },
            { label: 'Voice Stress Analysis', desc: 'Analyzes micro-tremors, pitch variation, and vocal quality changes associated with cognitive load. Phone accuracy: ~60%.' },
            { label: 'Facial Behavior Analysis', desc: 'Tracks blink rate, gaze patterns, and expression changes. Based on Paul Ekman\'s FACS research. Phone accuracy: ~55%.' },
          ].map((item) => (
            <View key={item.label} style={styles.scienceItem}>
              <Text style={styles.scienceLabel}>{item.label}</Text>
              <Text style={styles.scienceDesc}>{item.desc}</Text>
            </View>
          ))}
        </View>
      </View>

      <Text style={styles.footer}>
        TruthScope is for entertainment and educational purposes only.{'\n'}Not a replacement for professional lie detection.
      </Text>

      <View style={{ height: insets.bottom + spacing.xl }} />
    </ScrollView>
  );
}

export default SettingsScreen;

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.bg.primary },
  content: { padding: spacing.lg, paddingBottom: 40 },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: spacing.xl },
  backButton: { padding: 8 },
  title: { ...typography.h1, color: colors.text.primary },
  section: { marginBottom: spacing.lg },
  sectionTitle: { ...typography.caption, color: colors.text.tertiary, textTransform: 'uppercase', letterSpacing: 1, marginBottom: spacing.sm, marginLeft: spacing.xs },
  card: { backgroundColor: colors.bg.card, borderRadius: radii.md, padding: spacing.sm, gap: 2 },
  settingRow: { flexDirection: 'row', alignItems: 'center', gap: 12, padding: spacing.sm, borderRadius: radii.sm },
  settingLabel: { ...typography.body, color: colors.text.primary, flex: 1 },
  settingValue: { ...typography.caption, color: colors.text.secondary },
  scienceCard: { backgroundColor: colors.bg.card, borderRadius: radii.md, padding: spacing.md, gap: spacing.md },
  scienceText: { ...typography.body, color: colors.text.secondary },
  scienceItem: { gap: 4 },
  scienceLabel: { ...typography.bodyBold, color: colors.accent.primary, fontSize: 14 },
  scienceDesc: { ...typography.small, color: colors.text.tertiary, lineHeight: 18 },
  footer: { ...typography.small, color: colors.text.tertiary, textAlign: 'center', lineHeight: 18, marginTop: spacing.lg },
});
