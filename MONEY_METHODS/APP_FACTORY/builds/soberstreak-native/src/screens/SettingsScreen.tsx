import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Switch,
  ScrollView,
  Alert,
  SafeAreaView,
  Linking,
} from 'react-native';
import { useFocusEffect, useNavigation } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';
import * as StoreReview from 'expo-store-review';
import { Colors, Spacing, Radius, Typography } from '../constants/theme';
import { getSettings, saveSettings, clearAllData } from '../services/storage';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { RootStackParamList } from '../types';

type NavProp = NativeStackNavigationProp<RootStackParamList>;

export default function SettingsScreen() {
  const navigation = useNavigation<NavProp>();
  const [reminderEnabled, setReminderEnabled] = useState(false);
  const [isPremium, setIsPremium] = useState(false);

  useFocusEffect(useCallback(() => {
    getSettings().then(s => {
      setReminderEnabled(s.reminderEnabled);
      setIsPremium(s.isPremium);
    });
  }, []));

  const toggleReminder = async (val: boolean) => {
    setReminderEnabled(val);
    await saveSettings({ reminderEnabled: val });
  };

  const handleUpgrade = () => {
    navigation.navigate('Paywall', { source: 'settings' });
  };

  const handleReview = async () => {
    const available = await StoreReview.isAvailableAsync();
    if (available) {
      await StoreReview.requestReview();
    } else {
      Linking.openURL('https://apps.apple.com/app/id_soberstreak');
    }
  };

  const handleResetData = () => {
    Alert.alert(
      'Reset all data?',
      'This permanently deletes your streak history. This cannot be undone.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete everything',
          style: 'destructive',
          onPress: async () => {
            await clearAllData();
            navigation.reset({ index: 0, routes: [{ name: 'Onboarding' }] });
          },
        },
      ]
    );
  };

  const Row = ({ icon, label, right, onPress }: { icon: string; label: string; right?: React.ReactNode; onPress?: () => void }) => (
    <TouchableOpacity style={styles.row} onPress={onPress} disabled={!onPress}>
      <View style={styles.rowLeft}>
        <Ionicons name={icon as any} size={20} color={Colors.textSecondary} />
        <Text style={styles.rowLabel}>{label}</Text>
      </View>
      {right ?? <Ionicons name="chevron-forward" size={16} color={Colors.textTertiary} />}
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scroll}>
        <Text style={styles.heading}>Settings</Text>

        {/* Privacy section */}
        <Text style={styles.sectionLabel}>PRIVACY</Text>
        <View style={styles.card}>
          <View style={styles.privacyInfo}>
            <Ionicons name="shield-checkmark" size={36} color={Colors.primary} />
            <View style={styles.privacyText}>
              <Text style={styles.privacyTitle}>100% Private</Text>
              <Text style={styles.privacyDesc}>All data is stored locally on your device. We don't have a server. We can't see your streak.</Text>
            </View>
          </View>
        </View>

        {/* Premium */}
        {!isPremium && (
          <>
            <Text style={[styles.sectionLabel, { marginTop: Spacing.xl }]}>PREMIUM</Text>
            <TouchableOpacity style={styles.upgradeCard} onPress={handleUpgrade}>
              <View>
                <Text style={styles.upgradeTitle}>Unlock SoberStreak Premium</Text>
                <Text style={styles.upgradeDesc}>Milestone celebrations, custom habits, and detailed insights.</Text>
                <Text style={styles.upgradePrice}>$17.99 / year — 7-day free trial</Text>
              </View>
              <Ionicons name="arrow-forward-circle" size={32} color={Colors.primary} />
            </TouchableOpacity>
          </>
        )}

        {/* Notifications */}
        <Text style={[styles.sectionLabel, { marginTop: Spacing.xl }]}>NOTIFICATIONS</Text>
        <View style={styles.card}>
          <Row
            icon="notifications-outline"
            label="Daily check-in reminder"
            right={
              <Switch
                value={reminderEnabled}
                onValueChange={toggleReminder}
                trackColor={{ false: Colors.border, true: Colors.primary }}
                thumbColor={Colors.white}
              />
            }
          />
        </View>

        {/* Support */}
        <Text style={[styles.sectionLabel, { marginTop: Spacing.xl }]}>SUPPORT</Text>
        <View style={styles.card}>
          <Row icon="star-outline" label="Rate SoberStreak" onPress={handleReview} />
          <View style={styles.divider} />
          <Row icon="lock-closed-outline" label="Privacy Policy" onPress={() => Linking.openURL('https://printmaxx-privacy.surge.sh')} />
          <View style={styles.divider} />
          <Row icon="document-text-outline" label="Terms of Service" onPress={() => Linking.openURL('https://printmaxx-tos.surge.sh')} />
        </View>

        {/* Danger zone */}
        <Text style={[styles.sectionLabel, { marginTop: Spacing.xl }]}>DATA</Text>
        <View style={styles.card}>
          <Row icon="trash-outline" label="Reset all data" onPress={handleResetData} right={<Ionicons name="chevron-forward" size={16} color={Colors.accentAlt} />} />
        </View>

        <Text style={styles.version}>SoberStreak 1.0  •  Your data never leaves this device</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  scroll: { paddingHorizontal: Spacing.lg, paddingBottom: Spacing.xxl },
  heading: { ...Typography.h1, paddingVertical: Spacing.lg },
  sectionLabel: { ...Typography.tiny, textTransform: 'uppercase', letterSpacing: 2, color: Colors.textTertiary, marginBottom: Spacing.sm },
  card: { backgroundColor: Colors.surface, borderRadius: Radius.lg, overflow: 'hidden' },
  row: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between',
    paddingHorizontal: Spacing.md, paddingVertical: Spacing.md,
  },
  rowLeft: { flexDirection: 'row', alignItems: 'center', gap: Spacing.md },
  rowLabel: { ...Typography.body },
  divider: { height: 1, backgroundColor: Colors.border, marginLeft: Spacing.md },
  privacyInfo: { flexDirection: 'row', gap: Spacing.md, padding: Spacing.md, alignItems: 'flex-start' },
  privacyText: { flex: 1 },
  privacyTitle: { ...Typography.body, fontWeight: '700', color: Colors.primary, marginBottom: 4 },
  privacyDesc: { ...Typography.label, lineHeight: 20 },
  upgradeCard: {
    backgroundColor: Colors.surfaceAlt, borderRadius: Radius.lg, padding: Spacing.lg,
    flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between',
    borderWidth: 2, borderColor: Colors.primary, gap: Spacing.md,
  },
  upgradeTitle: { ...Typography.body, fontWeight: '700', color: Colors.text, marginBottom: 4 },
  upgradeDesc: { ...Typography.label, color: Colors.textSecondary, marginBottom: 4 },
  upgradePrice: { ...Typography.label, color: Colors.primary, fontWeight: '600' },
  version: { ...Typography.tiny, textAlign: 'center', marginTop: Spacing.xl, color: Colors.textTertiary },
});
