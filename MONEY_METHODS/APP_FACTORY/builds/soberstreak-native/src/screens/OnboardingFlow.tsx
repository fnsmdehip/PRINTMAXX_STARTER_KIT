import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Animated,
  Dimensions,
  SafeAreaView,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { Colors, Spacing, Radius, Typography } from '../constants/theme';
import { MODES } from '../constants/modes';
import { initStreak, saveSettings } from '../services/storage';
import { StreakMode } from '../types';
import type { RootStackParamList } from '../types';

const { width: SCREEN_WIDTH } = Dimensions.get('window');
type NavProp = NativeStackNavigationProp<RootStackParamList>;

const MODES_LIST: { id: StreakMode; label: string; emoji: string; tagline: string }[] = [
  { id: 'nofap', label: 'NoFap', emoji: '🔒', tagline: 'Reclaim energy. Rebuild confidence.' },
  { id: 'alcohol', label: 'Alcohol Free', emoji: '🧊', tagline: 'Clear mind. Better sleep.' },
  { id: 'smoking', label: 'Quit Smoking', emoji: '🫁', tagline: 'Your lungs are healing now.' },
  { id: 'gambling', label: 'Gambling Free', emoji: '🎯', tagline: 'Your money stays yours.' },
  { id: 'custom', label: 'Other habit', emoji: '⭐', tagline: 'You define your goal.' },
];

export default function OnboardingFlow() {
  const navigation = useNavigation<NavProp>();
  const [step, setStep] = useState(0);
  const [selectedMode, setSelectedMode] = useState<StreakMode | null>(null);
  const [selectedReason, setSelectedReason] = useState<string | null>(null);
  const fadeAnim = useRef(new Animated.Value(1)).current;

  const totalSteps = 8;

  const reasons = [
    { label: 'Mental clarity', icon: 'brain-outline' as const },
    { label: 'More energy', icon: 'flash-outline' as const },
    { label: 'Better relationships', icon: 'heart-outline' as const },
    { label: 'Self-respect', icon: 'shield-checkmark-outline' as const },
    { label: 'Health & fitness', icon: 'barbell-outline' as const },
    { label: 'Financial control', icon: 'wallet-outline' as const },
  ];

  const animateTransition = (nextStep: () => void) => {
    Animated.sequence([
      Animated.timing(fadeAnim, { toValue: 0, duration: 150, useNativeDriver: true }),
      Animated.timing(fadeAnim, { toValue: 1, duration: 200, useNativeDriver: true }),
    ]).start();
    setTimeout(nextStep, 150);
  };

  const next = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    animateTransition(() => setStep(s => Math.min(s + 1, totalSteps - 1)));
  };

  const handleStart = async () => {
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    if (!selectedMode) return;
    await initStreak(selectedMode);
    await saveSettings({ onboardingComplete: true });
    navigation.reset({ index: 0, routes: [{ name: 'Main' }] });
  };

  const renderProgressBar = () => (
    <View style={styles.progressBar}>
      <View style={[styles.progressFill, { width: `${((step + 1) / totalSteps) * 100}%` }]} />
    </View>
  );

  const renderStep = () => {
    switch (step) {
      case 0:
        return (
          <View style={styles.stepContainer}>
            <Text style={styles.lockEmoji}>🔒</Text>
            <Text style={styles.heading}>Your data stays{'\n'}on your device.</Text>
            <Text style={styles.subheading}>
              SoberStreak stores everything locally. No account. No server. No one can see your progress but you.
            </Text>
            <View style={styles.privacyBadge}>
              <Ionicons name="shield-checkmark" size={18} color={Colors.primary} />
              <Text style={styles.privacyText}>Zero data sent to any server. Ever.</Text>
            </View>
          </View>
        );

      case 1:
        return (
          <View style={styles.stepContainer}>
            <Text style={styles.heading}>What are you{'\n'}working on?</Text>
            <Text style={styles.subheading}>Pick the habit you want to break. You can add more later.</Text>
            <View style={styles.modeGrid}>
              {MODES_LIST.map(mode => (
                <TouchableOpacity
                  key={mode.id}
                  style={[styles.modeCard, selectedMode === mode.id && styles.modeCardSelected]}
                  onPress={() => {
                    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
                    setSelectedMode(mode.id);
                  }}
                >
                  <Text style={styles.modeEmoji}>{mode.emoji}</Text>
                  <Text style={[styles.modeLabel, selectedMode === mode.id && styles.modeLabelSelected]}>
                    {mode.label}
                  </Text>
                  <Text style={styles.modeTagline}>{mode.tagline}</Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>
        );

      case 2:
        return (
          <View style={styles.stepContainer}>
            <Text style={styles.heading}>Why does this{'\n'}matter to you?</Text>
            <Text style={styles.subheading}>Your "why" is the anchor when things get hard.</Text>
            <View style={styles.reasonGrid}>
              {reasons.map(r => (
                <TouchableOpacity
                  key={r.label}
                  style={[styles.reasonCard, selectedReason === r.label && styles.reasonCardSelected]}
                  onPress={() => {
                    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
                    setSelectedReason(r.label);
                  }}
                >
                  <Ionicons name={r.icon} size={22} color={selectedReason === r.label ? Colors.primary : Colors.textSecondary} />
                  <Text style={[styles.reasonLabel, selectedReason === r.label && styles.reasonLabelSelected]}>
                    {r.label}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>
        );

      case 3:
        return (
          <View style={styles.stepContainer}>
            <Text style={styles.statNumber}>1,240,000+</Text>
            <Text style={styles.heading}>People are working{'\n'}on the same thing.</Text>
            <Text style={styles.subheading}>
              r/NoFap has 1.24M members. Most apps in this space have betrayed their users. SoberStreak is different — your data never leaves your phone.
            </Text>
            <View style={styles.trustRow}>
              <View style={styles.trustItem}>
                <Text style={styles.trustIcon}>🔒</Text>
                <Text style={styles.trustLabel}>Local only</Text>
              </View>
              <View style={styles.trustItem}>
                <Text style={styles.trustIcon}>👤</Text>
                <Text style={styles.trustLabel}>No account</Text>
              </View>
              <View style={styles.trustItem}>
                <Text style={styles.trustIcon}>📵</Text>
                <Text style={styles.trustLabel}>No tracking</Text>
              </View>
            </View>
          </View>
        );

      case 4:
        return (
          <View style={styles.stepContainer}>
            <Text style={styles.heading}>The relapse{'\n'}button is real.</Text>
            <Text style={styles.subheading}>
              Most apps shame you for relapsing. We don't. If you slip, you log it, you reset, and you start building again. That honesty is what makes the streak meaningful.
            </Text>
            <View style={styles.relapseExample}>
              <Text style={styles.relapseDay}>Day 23</Text>
              <Text style={styles.relapseArrow}>→ Relapse → Day 0 → Day 1 → Day 2...</Text>
              <Text style={styles.relapseCaption}>Total clean days still count. Progress is not erased.</Text>
            </View>
          </View>
        );

      case 5:
        return (
          <View style={styles.stepContainer}>
            <Text style={styles.heading}>When the urge{'\n'}hits hardest</Text>
            <Text style={styles.subheading}>
              SoberStreak has an Emergency button. One tap gives you an urge-surfing prompt specifically written for your habit. It works.
            </Text>
            <View style={styles.emergencyDemo}>
              <View style={styles.emergencyButton}>
                <Ionicons name="warning-outline" size={20} color={Colors.accentAlt} />
                <Text style={styles.emergencyButtonText}>Emergency Help</Text>
              </View>
              <Text style={styles.emergencyCaption}>Available 24/7. No login required.</Text>
            </View>
          </View>
        );

      case 6:
        return (
          <View style={styles.stepContainer}>
            <Text style={styles.heading}>Milestones that{'\n'}actually mean something.</Text>
            <View style={styles.milestoneList}>
              {[1, 3, 7, 14, 30, 90].map(day => (
                <View key={day} style={styles.milestoneRow}>
                  <Text style={styles.milestoneDayBadge}>{day}d</Text>
                  <Text style={styles.milestoneDesc}>
                    {day === 1 && 'The hardest day. Your brain chemistry is already shifting.'}
                    {day === 3 && '72 hours. Dopamine receptors resetting.'}
                    {day === 7 && 'One week. Measurable change in energy and focus.'}
                    {day === 14 && 'Two weeks. Most people give up here. Not you.'}
                    {day === 30 && '30 days. The habit loop is broken.'}
                    {day === 90 && '90 days. This is who you are now.'}
                  </Text>
                </View>
              ))}
            </View>
          </View>
        );

      case 7:
        return (
          <View style={styles.stepContainer}>
            <Text style={styles.heading}>Free forever.{'\n'}Upgrade for more.</Text>
            <Text style={styles.subheading}>The core streak tracker is completely free. Upgrade for milestone celebrations, custom habit modes, and deeper insights.</Text>
            <View style={styles.pricingCard}>
              <View style={styles.pricingBadge}><Text style={styles.pricingBadgeText}>BEST VALUE</Text></View>
              <Text style={styles.pricingTitle}>Annual</Text>
              <Text style={styles.pricingPrice}>$17.99 / year</Text>
              <Text style={styles.pricingPer}>$1.50 / month</Text>
              <Text style={styles.pricingCTA}>7-day free trial</Text>
            </View>
            <TouchableOpacity style={styles.skipPricing} onPress={handleStart}>
              <Text style={styles.skipPricingText}>Start free, decide later</Text>
            </TouchableOpacity>
          </View>
        );

      default:
        return null;
    }
  };

  const canProceed = () => {
    if (step === 1) return selectedMode !== null;
    if (step === 2) return selectedReason !== null;
    return true;
  };

  return (
    <SafeAreaView style={styles.container}>
      {renderProgressBar()}
      <ScrollView contentContainerStyle={styles.scroll} showsVerticalScrollIndicator={false}>
        <Animated.View style={{ opacity: fadeAnim }}>
          {renderStep()}
        </Animated.View>
      </ScrollView>
      <View style={styles.footer}>
        {step < totalSteps - 1 ? (
          <TouchableOpacity
            style={[styles.nextButton, !canProceed() && styles.nextButtonDisabled]}
            onPress={next}
            disabled={!canProceed()}
          >
            <Text style={styles.nextButtonText}>Continue</Text>
            <Ionicons name="arrow-forward" size={20} color={Colors.background} />
          </TouchableOpacity>
        ) : (
          <TouchableOpacity style={styles.startButton} onPress={handleStart}>
            <Text style={styles.startButtonText}>Start My Streak</Text>
          </TouchableOpacity>
        )}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  progressBar: { height: 3, backgroundColor: Colors.surface, marginHorizontal: Spacing.md },
  progressFill: { height: 3, backgroundColor: Colors.primary, borderRadius: 2 },
  scroll: { flexGrow: 1, paddingHorizontal: Spacing.lg, paddingTop: Spacing.xl },
  stepContainer: { paddingBottom: Spacing.xxl },
  footer: { padding: Spacing.lg, paddingBottom: Spacing.xl },
  lockEmoji: { fontSize: 64, textAlign: 'center', marginBottom: Spacing.lg },
  heading: { ...Typography.h1, textAlign: 'center', marginBottom: Spacing.md, lineHeight: 40 },
  subheading: { ...Typography.bodySecondary, textAlign: 'center', lineHeight: 24, marginBottom: Spacing.lg },
  privacyBadge: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'center',
    backgroundColor: Colors.privacyBadge, padding: Spacing.md, borderRadius: Radius.md,
    gap: Spacing.sm, marginTop: Spacing.md,
  },
  privacyText: { ...Typography.body, color: Colors.primary, fontWeight: '600' },
  modeGrid: { gap: Spacing.md, marginTop: Spacing.md },
  modeCard: {
    backgroundColor: Colors.surface, padding: Spacing.lg, borderRadius: Radius.lg,
    borderWidth: 2, borderColor: Colors.border,
  },
  modeCardSelected: { borderColor: Colors.primary, backgroundColor: Colors.surfaceAlt },
  modeEmoji: { fontSize: 28, marginBottom: Spacing.xs },
  modeLabel: { ...Typography.h3, marginBottom: Spacing.xs },
  modeLabelSelected: { color: Colors.primary },
  modeTagline: { ...Typography.label },
  reasonGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: Spacing.sm, marginTop: Spacing.md },
  reasonCard: {
    flexDirection: 'row', alignItems: 'center', gap: Spacing.sm,
    backgroundColor: Colors.surface, paddingHorizontal: Spacing.md, paddingVertical: Spacing.sm,
    borderRadius: Radius.full, borderWidth: 2, borderColor: Colors.border,
  },
  reasonCardSelected: { borderColor: Colors.primary },
  reasonLabel: { ...Typography.body, color: Colors.textSecondary },
  reasonLabelSelected: { color: Colors.primary, fontWeight: '600' },
  statNumber: { fontSize: 48, fontWeight: '800', color: Colors.primary, textAlign: 'center', marginBottom: Spacing.md },
  trustRow: { flexDirection: 'row', justifyContent: 'space-around', marginTop: Spacing.xl },
  trustItem: { alignItems: 'center', gap: Spacing.xs },
  trustIcon: { fontSize: 28 },
  trustLabel: { ...Typography.label, color: Colors.textSecondary },
  relapseExample: {
    backgroundColor: Colors.surface, padding: Spacing.lg, borderRadius: Radius.lg, marginTop: Spacing.xl,
  },
  relapseDay: { ...Typography.h3, color: Colors.primary },
  relapseArrow: { ...Typography.body, marginVertical: Spacing.xs },
  relapseCaption: { ...Typography.label, color: Colors.textSecondary, marginTop: Spacing.sm },
  emergencyDemo: { alignItems: 'center', marginTop: Spacing.xl, gap: Spacing.md },
  emergencyButton: {
    flexDirection: 'row', alignItems: 'center', gap: Spacing.sm,
    backgroundColor: Colors.surfaceAlt, paddingHorizontal: Spacing.xl, paddingVertical: Spacing.md,
    borderRadius: Radius.full, borderWidth: 2, borderColor: Colors.accentAlt,
  },
  emergencyButtonText: { ...Typography.body, color: Colors.accentAlt, fontWeight: '700' },
  emergencyCaption: { ...Typography.label },
  milestoneList: { marginTop: Spacing.lg, gap: Spacing.md },
  milestoneRow: {
    flexDirection: 'row', alignItems: 'flex-start', gap: Spacing.md,
    backgroundColor: Colors.surface, padding: Spacing.md, borderRadius: Radius.md,
  },
  milestoneDayBadge: {
    backgroundColor: Colors.primary, color: Colors.background, fontWeight: '800',
    paddingHorizontal: Spacing.sm, paddingVertical: 2, borderRadius: Radius.sm,
    fontSize: 13, minWidth: 36, textAlign: 'center',
  },
  milestoneDesc: { ...Typography.body, flex: 1, lineHeight: 22 },
  pricingCard: {
    backgroundColor: Colors.surface, padding: Spacing.xl, borderRadius: Radius.xl,
    borderWidth: 2, borderColor: Colors.primary, alignItems: 'center', marginBottom: Spacing.lg,
  },
  pricingBadge: {
    backgroundColor: Colors.primary, paddingHorizontal: Spacing.md, paddingVertical: 4,
    borderRadius: Radius.full, marginBottom: Spacing.md,
  },
  pricingBadgeText: { color: Colors.background, fontWeight: '800', fontSize: 12, letterSpacing: 1 },
  pricingTitle: { ...Typography.h2, marginBottom: Spacing.xs },
  pricingPrice: { ...Typography.h1, color: Colors.primary },
  pricingPer: { ...Typography.label, marginBottom: Spacing.md },
  pricingCTA: { ...Typography.body, color: Colors.accent, fontWeight: '700' },
  skipPricing: { alignItems: 'center', padding: Spacing.md },
  skipPricingText: { ...Typography.body, color: Colors.textTertiary, textDecorationLine: 'underline' },
  nextButton: {
    backgroundColor: Colors.primary, flexDirection: 'row', alignItems: 'center',
    justifyContent: 'center', padding: Spacing.lg, borderRadius: Radius.lg, gap: Spacing.sm,
  },
  nextButtonDisabled: { opacity: 0.4 },
  nextButtonText: { ...Typography.body, color: Colors.background, fontWeight: '700', fontSize: 18 },
  startButton: {
    backgroundColor: Colors.primary, padding: Spacing.lg, borderRadius: Radius.lg, alignItems: 'center',
  },
  startButtonText: { ...Typography.body, color: Colors.background, fontWeight: '800', fontSize: 18 },
});
