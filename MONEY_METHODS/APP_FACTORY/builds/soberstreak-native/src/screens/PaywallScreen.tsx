import React, { useState } from 'react';
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
import { useNavigation, useRoute } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Ionicons } from '@expo/vector-icons';
import Constants from 'expo-constants';
import { Colors, Spacing, Radius, Typography } from '../constants/theme';
import { saveSettings } from '../services/storage';
import type { RootStackParamList } from '../types';

type NavProp = NativeStackNavigationProp<RootStackParamList>;

const ANNUAL_LINK: string = Constants.expoConfig?.extra?.paymentLinkAnnual ?? '';
const MONTHLY_LINK: string = Constants.expoConfig?.extra?.paymentLinkMonthly ?? '';

const FEATURES = [
  { icon: 'trophy-outline' as const, text: 'Milestone celebrations with personalized messages' },
  { icon: 'bar-chart-outline' as const, text: 'Detailed insights and streak analytics' },
  { icon: 'add-circle-outline' as const, text: 'Track multiple habits simultaneously' },
  { icon: 'notifications-outline' as const, text: 'Smart reminders at your custom time' },
  { icon: 'shield-checkmark-outline' as const, text: 'Still 100% private. No server. No account.' },
];

export default function PaywallScreen() {
  const navigation = useNavigation<NavProp>();
  const [selectedPlan, setSelectedPlan] = useState<'annual' | 'monthly'>('annual');

  const handlePurchase = async () => {
    const url = selectedPlan === 'annual' ? ANNUAL_LINK : MONTHLY_LINK;
    if (!url || url.includes('placeholder')) {
      Alert.alert('Coming soon', 'Payment will be enabled when the app launches on the App Store.');
      return;
    }
    try {
      await Linking.openURL(url);
      // After returning from Stripe, verify purchase server-side
      // For now, mark premium locally (production: verify via webhook)
      await saveSettings({ isPremium: true });
      navigation.goBack();
    } catch {
      Alert.alert('Error', 'Could not open payment page.');
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Ionicons name="close" size={28} color={Colors.textSecondary} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Upgrade</Text>
        <View style={{ width: 28 }} />
      </View>

      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scroll}>
        <Text style={styles.heading}>Your streak deserves{'\n'}full support.</Text>
        <Text style={styles.subheading}>The core streak tracker is free forever. Premium unlocks everything else.</Text>

        {/* Features */}
        <View style={styles.featureList}>
          {FEATURES.map(f => (
            <View key={f.text} style={styles.featureRow}>
              <Ionicons name={f.icon} size={20} color={Colors.primary} />
              <Text style={styles.featureText}>{f.text}</Text>
            </View>
          ))}
        </View>

        {/* Plans */}
        <TouchableOpacity
          style={[styles.planCard, selectedPlan === 'annual' && styles.planCardSelected]}
          onPress={() => setSelectedPlan('annual')}
        >
          <View style={styles.planLeft}>
            <View style={[styles.radio, selectedPlan === 'annual' && styles.radioSelected]} />
            <View>
              <View style={styles.planTitleRow}>
                <Text style={styles.planTitle}>Annual</Text>
                <View style={styles.bestValueBadge}>
                  <Text style={styles.bestValueText}>SAVE 70%</Text>
                </View>
              </View>
              <Text style={styles.planPrice}>$17.99 / year</Text>
              <Text style={styles.planPer}>$1.50 per month</Text>
            </View>
          </View>
          <Text style={styles.planTrial}>7-day free trial</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.planCard, selectedPlan === 'monthly' && styles.planCardSelected]}
          onPress={() => setSelectedPlan('monthly')}
        >
          <View style={styles.planLeft}>
            <View style={[styles.radio, selectedPlan === 'monthly' && styles.radioSelected]} />
            <View>
              <Text style={styles.planTitle}>Monthly</Text>
              <Text style={styles.planPrice}>$4.99 / month</Text>
            </View>
          </View>
        </TouchableOpacity>

        <TouchableOpacity style={styles.ctaButton} onPress={handlePurchase}>
          <Text style={styles.ctaText}>
            {selectedPlan === 'annual' ? 'Start 7-Day Free Trial' : 'Subscribe Monthly'}
          </Text>
        </TouchableOpacity>

        <Text style={styles.legal}>
          Cancel anytime. {selectedPlan === 'annual' ? 'No charge during trial.' : ''} By subscribing, you agree to our Terms of Service and Privacy Policy.
        </Text>

        <TouchableOpacity style={styles.skipButton} onPress={() => navigation.goBack()}>
          <Text style={styles.skipText}>Continue with free version</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  header: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between',
    paddingHorizontal: Spacing.lg, paddingVertical: Spacing.md,
  },
  headerTitle: { ...Typography.h3 },
  scroll: { paddingHorizontal: Spacing.lg, paddingBottom: Spacing.xxl },
  heading: { ...Typography.h1, marginBottom: Spacing.sm, lineHeight: 40 },
  subheading: { ...Typography.bodySecondary, marginBottom: Spacing.xl, lineHeight: 24 },
  featureList: { gap: Spacing.md, marginBottom: Spacing.xl },
  featureRow: { flexDirection: 'row', gap: Spacing.md, alignItems: 'flex-start' },
  featureText: { ...Typography.body, flex: 1, lineHeight: 22 },
  planCard: {
    backgroundColor: Colors.surface, borderRadius: Radius.lg, padding: Spacing.lg,
    marginBottom: Spacing.md, borderWidth: 2, borderColor: Colors.border,
    flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between',
  },
  planCardSelected: { borderColor: Colors.primary },
  planLeft: { flexDirection: 'row', gap: Spacing.md, alignItems: 'center' },
  radio: { width: 22, height: 22, borderRadius: 11, borderWidth: 2, borderColor: Colors.border },
  radioSelected: { borderColor: Colors.primary, backgroundColor: Colors.primary },
  planTitleRow: { flexDirection: 'row', alignItems: 'center', gap: Spacing.sm },
  planTitle: { ...Typography.body, fontWeight: '700' },
  bestValueBadge: {
    backgroundColor: Colors.primary, paddingHorizontal: 8, paddingVertical: 2, borderRadius: Radius.full,
  },
  bestValueText: { color: Colors.background, fontWeight: '800', fontSize: 10, letterSpacing: 1 },
  planPrice: { ...Typography.h3, color: Colors.primary },
  planPer: { ...Typography.tiny },
  planTrial: { ...Typography.label, color: Colors.accent, fontWeight: '700' },
  ctaButton: {
    backgroundColor: Colors.primary, padding: Spacing.lg, borderRadius: Radius.lg,
    alignItems: 'center', marginBottom: Spacing.md,
  },
  ctaText: { ...Typography.body, color: Colors.background, fontWeight: '800', fontSize: 18 },
  legal: { ...Typography.tiny, textAlign: 'center', marginBottom: Spacing.lg, lineHeight: 18 },
  skipButton: { alignItems: 'center', padding: Spacing.md },
  skipText: { ...Typography.body, color: Colors.textTertiary, textDecorationLine: 'underline' },
});
