import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  SafeAreaView,
  Linking,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { useNavigation, useRoute, RouteProp } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Colors, Spacing, Radius, Typography } from '../constants/theme';
import { saveSettings } from '../services/storage';
import { RootStackParamList } from '../types';

// Stripe Payment Links (replace with real links once created)
const STRIPE_ANNUAL = 'https://buy.stripe.com/streakr-annual-2499';   // $24.99/yr
const STRIPE_MONTHLY = 'https://buy.stripe.com/streakr-monthly-499';  // $4.99/mo
const PRIVACY_URL = 'https://printmaxx-privacy.surge.sh';
const TERMS_URL = 'https://printmaxx-tos.surge.sh';

type NavProp = NativeStackNavigationProp<RootStackParamList>;
type RouteType = RouteProp<RootStackParamList, 'Paywall'>;

const FEATURES_FREE = [
  { label: 'Up to 3 habits', included: true },
  { label: 'Swipe-to-complete', included: true },
  { label: 'Basic streak tracking', included: true },
  { label: 'Daily reminder', included: true },
  { label: 'Unlimited habits', included: false },
  { label: 'MVD full history', included: false },
  { label: 'Streak repair (1/month)', included: false },
  { label: 'Share milestone cards', included: false },
];

const FEATURES_PRO = [
  { label: 'Unlimited habits', included: true },
  { label: 'Swipe-to-complete', included: true },
  { label: 'Full streak history & heatmap', included: true },
  { label: 'MVD full history', included: true },
  { label: 'Streak repair (1/month)', included: true },
  { label: 'Share milestone cards', included: true },
  { label: 'Daily reminder', included: true },
  { label: 'CSV export', included: true },
];

export default function PaywallScreen() {
  const navigation = useNavigation<NavProp>();
  const route = useRoute<RouteType>();
  const [selectedPlan, setSelectedPlan] = useState<'annual' | 'monthly'>('annual');
  const [loading, setLoading] = useState(false);

  const sourceHeadlines: Record<string, { title: string; sub: string }> = {
    habit_limit: {
      title: 'Unlock unlimited habits.',
      sub: 'Free tier is 3 habits. You're building momentum — don't cap it.',
    },
    mvd_history: {
      title: 'See your full MVD history.',
      sub: 'Which days did you hit the full goal vs the minimum? That data matters.',
    },
    streak_repair: {
      title: 'One slip doesn't have to end it.',
      sub: 'Streak repair forgives one missed day per month. For when life happens.',
    },
    share: {
      title: 'Share your milestones.',
      sub: '30-day streak? That's worth sharing. Unlock shareable milestone cards.',
    },
    settings: {
      title: 'Go unlimited.',
      sub: 'Every feature, unlimited habits, streak repair. One price.',
    },
  };

  const { title, sub } = sourceHeadlines[route.params.source] ?? sourceHeadlines.settings;

  const handleSubscribe = async () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    setLoading(true);
    const url = selectedPlan === 'annual' ? STRIPE_ANNUAL : STRIPE_MONTHLY;

    // In production: use Stripe Checkout or RevenueCat
    // For now: open Stripe Payment Link in browser
    const supported = await Linking.canOpenURL(url);
    if (supported) {
      await Linking.openURL(url);
      // Optimistically unlock after redirect (replace with webhook/receipt check in production)
      await saveSettings({ isPremium: true });
    }
    setLoading(false);
  };

  const handleRestore = () => {
    // Restore purchases via RevenueCat when integrated
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  };

  return (
    <SafeAreaView style={s.container}>
      <TouchableOpacity style={s.closeBtn} onPress={() => navigation.goBack()}>
        <Ionicons name="close" size={22} color={Colors.textMuted} />
      </TouchableOpacity>

      <ScrollView contentContainerStyle={s.scroll} showsVerticalScrollIndicator={false}>
        {/* Hero */}
        <View style={s.hero}>
          <Text style={s.heroEmoji}>🔥</Text>
          <Text style={s.heroTitle}>{title}</Text>
          <Text style={s.heroSub}>{sub}</Text>
        </View>

        {/* Plan selector */}
        <View style={s.planRow}>
          <TouchableOpacity
            style={[s.planCard, selectedPlan === 'annual' && s.planCardSelected]}
            onPress={() => { Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light); setSelectedPlan('annual'); }}
            activeOpacity={0.85}
          >
            <View style={s.planBadge}>
              <Text style={s.planBadgeText}>BEST VALUE</Text>
            </View>
            <Text style={s.planPrice}>$24.99</Text>
            <Text style={s.planPeriod}>per year</Text>
            <Text style={s.planNote}>~$2.08/mo · 7-day free trial</Text>
            {selectedPlan === 'annual' && (
              <View style={s.planCheck}>
                <Ionicons name="checkmark-circle" size={20} color={Colors.emerald} />
              </View>
            )}
          </TouchableOpacity>

          <TouchableOpacity
            style={[s.planCard, selectedPlan === 'monthly' && s.planCardSelected]}
            onPress={() => { Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light); setSelectedPlan('monthly'); }}
            activeOpacity={0.85}
          >
            <Text style={s.planPrice}>$4.99</Text>
            <Text style={s.planPeriod}>per month</Text>
            <Text style={s.planNote}>Cancel anytime</Text>
            {selectedPlan === 'monthly' && (
              <View style={s.planCheck}>
                <Ionicons name="checkmark-circle" size={20} color={Colors.emerald} />
              </View>
            )}
          </TouchableOpacity>
        </View>

        {/* Trial timeline */}
        {selectedPlan === 'annual' && (
          <View style={s.trialTimeline}>
            <TimelineItem emoji="✅" label="Today" sub="Trial starts. No charge." />
            <TimelineDash />
            <TimelineItem emoji="📅" label="Day 5" sub="Reminder before trial ends." />
            <TimelineDash />
            <TimelineItem emoji="💳" label="Day 7" sub="$24.99 billed if not cancelled." />
          </View>
        )}

        {/* CTA */}
        <TouchableOpacity
          style={[s.ctaBtn, loading && s.ctaBtnDisabled]}
          onPress={loading ? undefined : handleSubscribe}
          activeOpacity={0.9}
        >
          <Text style={s.ctaBtnText}>
            {loading ? 'Opening checkout…' : selectedPlan === 'annual' ? 'Start 7-day free trial' : 'Subscribe monthly'}
          </Text>
        </TouchableOpacity>
        <Text style={s.ctaNote}>No payment due today{selectedPlan === 'annual' ? ' · Cancel anytime in Settings' : ''}</Text>

        {/* Feature list */}
        <View style={s.featureList}>
          <Text style={s.featureListTitle}>Everything included</Text>
          {FEATURES_PRO.map(f => (
            <View key={f.label} style={s.featureRow}>
              <Ionicons name="checkmark-circle" size={18} color={Colors.emerald} />
              <Text style={s.featureLabel}>{f.label}</Text>
            </View>
          ))}
        </View>

        {/* Legal */}
        <View style={s.legalRow}>
          <TouchableOpacity onPress={handleRestore}>
            <Text style={s.legalLink}>Restore purchase</Text>
          </TouchableOpacity>
          <Text style={s.legalDot}>·</Text>
          <TouchableOpacity onPress={() => Linking.openURL(PRIVACY_URL)}>
            <Text style={s.legalLink}>Privacy</Text>
          </TouchableOpacity>
          <Text style={s.legalDot}>·</Text>
          <TouchableOpacity onPress={() => Linking.openURL(TERMS_URL)}>
            <Text style={s.legalLink}>Terms</Text>
          </TouchableOpacity>
        </View>

        <Text style={s.subscriptionTerms}>
          Subscriptions automatically renew unless cancelled at least 24 hours before the current period ends.
          Manage or cancel in your device Settings → Apple ID → Subscriptions.
        </Text>
      </ScrollView>
    </SafeAreaView>
  );
}

function TimelineItem({ emoji, label, sub }: { emoji: string; label: string; sub: string }) {
  return (
    <View style={s.timelineItem}>
      <Text style={s.timelineEmoji}>{emoji}</Text>
      <Text style={s.timelineLabel}>{label}</Text>
      <Text style={s.timelineSub}>{sub}</Text>
    </View>
  );
}

function TimelineDash() {
  return <View style={s.timelineDash} />;
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.bg },
  closeBtn: {
    position: 'absolute',
    top: 54,
    right: 20,
    zIndex: 10,
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: Colors.bgCard,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: Colors.border,
  },
  scroll: { paddingHorizontal: Spacing.lg, paddingTop: Spacing.xl, paddingBottom: 48 },
  hero: { alignItems: 'center', marginBottom: Spacing.xl },
  heroEmoji: { fontSize: 48, marginBottom: 12 },
  heroTitle: { ...Typography.h1, color: Colors.text, textAlign: 'center', marginBottom: 8 },
  heroSub: { ...Typography.body, color: Colors.textMuted, textAlign: 'center', lineHeight: 24 },
  // Plan cards
  planRow: { flexDirection: 'row', gap: 12, marginBottom: Spacing.lg },
  planCard: {
    flex: 1,
    backgroundColor: Colors.bgCard,
    borderRadius: Radius.lg,
    padding: 18,
    borderWidth: 2,
    borderColor: Colors.border,
    alignItems: 'center',
    gap: 4,
    position: 'relative',
  },
  planCardSelected: { borderColor: Colors.emerald },
  planBadge: {
    position: 'absolute',
    top: -10,
    backgroundColor: Colors.emerald,
    borderRadius: Radius.full,
    paddingHorizontal: 10,
    paddingVertical: 3,
  },
  planBadgeText: { ...Typography.label, color: '#fff' },
  planPrice: { ...Typography.h2, color: Colors.text, marginTop: 8 },
  planPeriod: { ...Typography.caption, color: Colors.textMuted },
  planNote: { ...Typography.label, color: Colors.textLight, textAlign: 'center' },
  planCheck: { position: 'absolute', top: 8, right: 8 },
  // Trial timeline
  trialTimeline: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.bgCard,
    borderRadius: Radius.lg,
    padding: 16,
    marginBottom: Spacing.lg,
    gap: 0,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  timelineItem: { flex: 1, alignItems: 'center', gap: 2 },
  timelineEmoji: { fontSize: 20 },
  timelineLabel: { ...Typography.captionMed, color: Colors.text },
  timelineSub: { ...Typography.label, color: Colors.textMuted, textAlign: 'center' },
  timelineDash: { width: 20, height: 1, backgroundColor: Colors.border },
  // CTA
  ctaBtn: {
    backgroundColor: Colors.emerald,
    borderRadius: Radius.full,
    paddingVertical: 18,
    alignItems: 'center',
    marginBottom: 8,
  },
  ctaBtnDisabled: { opacity: 0.6 },
  ctaBtnText: { ...Typography.bodyMed, color: '#fff', fontWeight: '800', fontSize: 17 },
  ctaNote: { ...Typography.caption, color: Colors.textMuted, textAlign: 'center', marginBottom: Spacing.xl },
  // Feature list
  featureList: {
    backgroundColor: Colors.bgCard,
    borderRadius: Radius.lg,
    padding: 20,
    gap: 12,
    borderWidth: 1,
    borderColor: Colors.border,
    marginBottom: Spacing.lg,
  },
  featureListTitle: { ...Typography.h3, color: Colors.text, marginBottom: 4 },
  featureRow: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  featureLabel: { ...Typography.body, color: Colors.text },
  // Legal
  legalRow: { flexDirection: 'row', justifyContent: 'center', alignItems: 'center', gap: 6, marginBottom: 12 },
  legalLink: { ...Typography.caption, color: Colors.textMuted, textDecorationLine: 'underline' },
  legalDot: { ...Typography.caption, color: Colors.textLight },
  subscriptionTerms: {
    ...Typography.label,
    color: Colors.textLight,
    textAlign: 'center',
    lineHeight: 18,
    paddingHorizontal: 8,
  },
});
