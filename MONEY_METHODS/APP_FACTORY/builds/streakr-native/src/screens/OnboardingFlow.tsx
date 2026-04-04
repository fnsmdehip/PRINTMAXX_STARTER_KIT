import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Animated,
  ScrollView,
  TextInput,
  KeyboardAvoidingView,
  Platform,
  Dimensions,
  SafeAreaView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Colors, Spacing, Radius, Typography } from '../constants/theme';
import { HABIT_PRESETS, HabitPreset } from '../constants/habits';
import { createHabit, addHabit, saveSettings } from '../services/storage';
import { RootStackParamList, HabitCategory } from '../types';

type NavProp = NativeStackNavigationProp<RootStackParamList>;

const { width } = Dimensions.get('window');

const ONBOARDING_STEPS = 5;

const CATEGORY_TABS: { label: string; value: HabitCategory; emoji: string }[] = [
  { label: 'Fitness', value: 'fitness', emoji: '💪' },
  { label: 'Mind', value: 'mindfulness', emoji: '🧘' },
  { label: 'Learn', value: 'learning', emoji: '📚' },
  { label: 'Create', value: 'creation', emoji: '✍️' },
  { label: 'Health', value: 'health', emoji: '💚' },
];

export default function OnboardingFlow() {
  const navigation = useNavigation<NavProp>();
  const [step, setStep] = useState(0);
  const [selectedCategory, setSelectedCategory] = useState<HabitCategory>('fitness');
  const [selectedPreset, setSelectedPreset] = useState<HabitPreset | null>(null);
  const [customName, setCustomName] = useState('');
  const [customEmoji, setCustomEmoji] = useState('⭐');
  const [customMvd, setCustomMvd] = useState('');
  const [useMvd, setUseMvd] = useState(false);
  const [saving, setSaving] = useState(false);

  const fadeAnim = useRef(new Animated.Value(1)).current;
  const swipeCardScale = useRef(new Animated.Value(1)).current;
  const swipeCardY = useRef(new Animated.Value(0)).current;

  const presetsForCategory = HABIT_PRESETS.filter(p => p.category === selectedCategory);

  const goNext = () => {
    Animated.sequence([
      Animated.timing(fadeAnim, { toValue: 0, duration: 150, useNativeDriver: true }),
      Animated.timing(fadeAnim, { toValue: 1, duration: 200, useNativeDriver: true }),
    ]).start();
    setStep(s => s + 1);
  };

  const handleSelectPreset = (preset: HabitPreset) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    setSelectedPreset(preset);
    setCustomMvd(preset.mvdLabel);
  };

  const handleDemoSwipe = () => {
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    Animated.sequence([
      Animated.parallel([
        Animated.timing(swipeCardY, { toValue: -80, duration: 300, useNativeDriver: true }),
        Animated.timing(swipeCardScale, { toValue: 0.9, duration: 300, useNativeDriver: true }),
      ]),
      Animated.delay(400),
      Animated.parallel([
        Animated.timing(swipeCardY, { toValue: 0, duration: 300, useNativeDriver: true }),
        Animated.timing(swipeCardScale, { toValue: 1, duration: 300, useNativeDriver: true }),
      ]),
    ]).start();
  };

  const handleFinish = async () => {
    setSaving(true);
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

    const name = selectedPreset?.name ?? customName || 'My habit';
    const emoji = selectedPreset?.emoji ?? customEmoji;
    const category = selectedPreset?.category ?? 'custom';
    const mvdLabel = useMvd
      ? (customMvd || selectedPreset?.mvdLabel || 'Do the minimum version')
      : '';

    const habit = createHabit(name, emoji, category, useMvd, mvdLabel);
    await addHabit(habit);
    await saveSettings({ onboardingComplete: true });

    navigation.replace('Main');
  };

  return (
    <SafeAreaView style={s.container}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        {/* Progress dots */}
        <View style={s.dotsRow}>
          {Array.from({ length: ONBOARDING_STEPS }).map((_, i) => (
            <View key={i} style={[s.dot, i === step && s.dotActive, i < step && s.dotDone]} />
          ))}
        </View>

        <Animated.View style={[s.stepWrap, { opacity: fadeAnim }]}>
          {step === 0 && <StepWelcome onNext={goNext} onDemoSwipe={handleDemoSwipe} swipeCardY={swipeCardY} swipeCardScale={swipeCardScale} />}
          {step === 1 && (
            <StepPickCategory
              selectedCategory={selectedCategory}
              onSelect={c => { setSelectedCategory(c); setSelectedPreset(null); }}
              onNext={goNext}
            />
          )}
          {step === 2 && (
            <StepPickHabit
              presets={presetsForCategory}
              selected={selectedPreset}
              onSelect={handleSelectPreset}
              customName={customName}
              onCustomName={setCustomName}
              onNext={goNext}
            />
          )}
          {step === 3 && (
            <StepMVD
              enabled={useMvd}
              onToggle={() => setUseMvd(v => !v)}
              mvdText={customMvd}
              onMvdText={setCustomMvd}
              onNext={goNext}
            />
          )}
          {step === 4 && (
            <StepFirstCheckIn
              habitName={selectedPreset?.name ?? customName || 'your habit'}
              habitEmoji={selectedPreset?.emoji ?? customEmoji}
              onFinish={handleFinish}
              saving={saving}
            />
          )}
        </Animated.View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

// ─── Step sub-components ──────────────────────────────────────────────────────

function StepWelcome({
  onNext,
  onDemoSwipe,
  swipeCardY,
  swipeCardScale,
}: {
  onNext: () => void;
  onDemoSwipe: () => void;
  swipeCardY: Animated.Value;
  swipeCardScale: Animated.Value;
}) {
  return (
    <View style={s.stepContent}>
      <Text style={s.headline}>Track fewer things.{'\n'}Actually keep them.</Text>
      <Text style={s.sub}>One habit. One swipe. That's a win.</Text>

      <TouchableOpacity onPress={onDemoSwipe} activeOpacity={0.9}>
        <Animated.View
          style={[
            s.demoCard,
            { transform: [{ translateY: swipeCardY }, { scale: swipeCardScale }] },
          ]}
        >
          <Text style={s.demoCardEmoji}>💪</Text>
          <View style={{ flex: 1 }}>
            <Text style={s.demoCardName}>Morning workout</Text>
            <Text style={s.demoCardStreak}>🔥 7-day streak</Text>
          </View>
          <View style={s.demoSwipeHint}>
            <Ionicons name="arrow-up" size={16} color={Colors.emerald} />
            <Text style={s.demoSwipeText}>swipe</Text>
          </View>
        </Animated.View>
      </TouchableOpacity>

      <Text style={s.tapHint}>Tap the card to try</Text>

      <View style={s.trustRow}>
        <TrustPill emoji="🔒" label="No account" />
        <TrustPill emoji="📴" label="100% offline" />
        <TrustPill emoji="❌" label="No ads" />
      </View>

      <TouchableOpacity style={s.primaryBtn} onPress={onNext}>
        <Text style={s.primaryBtnText}>Start your first streak</Text>
      </TouchableOpacity>
    </View>
  );
}

function TrustPill({ emoji, label }: { emoji: string; label: string }) {
  return (
    <View style={s.trustPill}>
      <Text style={s.trustEmoji}>{emoji}</Text>
      <Text style={s.trustLabel}>{label}</Text>
    </View>
  );
}

function StepPickCategory({
  selectedCategory,
  onSelect,
  onNext,
}: {
  selectedCategory: HabitCategory;
  onSelect: (c: HabitCategory) => void;
  onNext: () => void;
}) {
  return (
    <View style={s.stepContent}>
      <Text style={s.headline}>What area of life?</Text>
      <Text style={s.sub}>Pick one to start. You can add more later.</Text>

      <View style={s.categoryGrid}>
        {CATEGORY_TABS.map(c => (
          <TouchableOpacity
            key={c.value}
            style={[s.categoryTile, selectedCategory === c.value && s.categoryTileSelected]}
            onPress={() => { Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light); onSelect(c.value); }}
            activeOpacity={0.7}
          >
            <Text style={s.categoryTileEmoji}>{c.emoji}</Text>
            <Text style={[s.categoryTileLabel, selectedCategory === c.value && s.categoryTileLabelSelected]}>
              {c.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <TouchableOpacity style={s.primaryBtn} onPress={onNext}>
        <Text style={s.primaryBtnText}>Continue</Text>
      </TouchableOpacity>
    </View>
  );
}

function StepPickHabit({
  presets,
  selected,
  onSelect,
  customName,
  onCustomName,
  onNext,
}: {
  presets: HabitPreset[];
  selected: HabitPreset | null;
  onSelect: (p: HabitPreset) => void;
  customName: string;
  onCustomName: (s: string) => void;
  onNext: () => void;
}) {
  const canProceed = selected !== null || customName.trim().length > 0;

  return (
    <View style={s.stepContent}>
      <Text style={s.headline}>Pick your habit</Text>
      <Text style={s.sub}>Start with one. You can always add more.</Text>

      <ScrollView style={s.presetList} showsVerticalScrollIndicator={false}>
        {presets.map(p => (
          <TouchableOpacity
            key={p.name}
            style={[s.presetRow, selected?.name === p.name && s.presetRowSelected]}
            onPress={() => onSelect(p)}
            activeOpacity={0.7}
          >
            <Text style={s.presetEmoji}>{p.emoji}</Text>
            <View style={{ flex: 1 }}>
              <Text style={s.presetName}>{p.name}</Text>
              <Text style={s.presetMvd} numberOfLines={1}>MVD: {p.mvdLabel}</Text>
            </View>
            {selected?.name === p.name && (
              <Ionicons name="checkmark-circle" size={22} color={Colors.emerald} />
            )}
          </TouchableOpacity>
        ))}

        <View style={s.divider} />

        <Text style={[s.sub, { marginBottom: 8 }]}>Or type your own:</Text>
        <TextInput
          style={s.customInput}
          placeholder="e.g. No social media before noon"
          placeholderTextColor={Colors.textLight}
          value={customName}
          onChangeText={t => { onCustomName(t); }}
          maxLength={50}
        />
      </ScrollView>

      <TouchableOpacity
        style={[s.primaryBtn, !canProceed && s.primaryBtnDisabled]}
        onPress={canProceed ? onNext : undefined}
        activeOpacity={canProceed ? 0.8 : 1}
      >
        <Text style={s.primaryBtnText}>This is my habit</Text>
      </TouchableOpacity>
    </View>
  );
}

function StepMVD({
  enabled,
  onToggle,
  mvdText,
  onMvdText,
  onNext,
}: {
  enabled: boolean;
  onToggle: () => void;
  mvdText: string;
  onMvdText: (s: string) => void;
  onNext: () => void;
}) {
  return (
    <View style={s.stepContent}>
      <Text style={s.headline}>Minimum Viable Day</Text>
      <Text style={s.sub}>
        The version of your habit so small it feels almost too easy. You do it even on your worst day. The streak stays alive.
      </Text>

      <View style={s.mvdCard}>
        <View style={s.mvdRow}>
          <View style={{ flex: 1 }}>
            <Text style={s.mvdLabel}>Enable MVD mode</Text>
            <Text style={s.mvdSub}>Define the minimum that still counts as a win</Text>
          </View>
          <TouchableOpacity
            style={[s.toggle, enabled && s.toggleOn]}
            onPress={() => { Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light); onToggle(); }}
          >
            <View style={[s.toggleThumb, enabled && s.toggleThumbOn]} />
          </TouchableOpacity>
        </View>

        {enabled && (
          <TextInput
            style={[s.customInput, { marginTop: 16 }]}
            placeholder="e.g. Do 5 pushups"
            placeholderTextColor={Colors.textLight}
            value={mvdText}
            onChangeText={onMvdText}
            maxLength={80}
          />
        )}
      </View>

      <View style={s.exampleBox}>
        <Text style={s.exampleTitle}>Why this works</Text>
        <Text style={s.exampleText}>
          "I said my habit was 'go to the gym.' But some days I just put on my shoes and walked out the door. I counted it. 47-day streak."
        </Text>
      </View>

      <TouchableOpacity style={s.primaryBtn} onPress={onNext}>
        <Text style={s.primaryBtnText}>Got it</Text>
      </TouchableOpacity>
      <TouchableOpacity onPress={onNext} style={s.skipBtn}>
        <Text style={s.skipBtnText}>Skip for now</Text>
      </TouchableOpacity>
    </View>
  );
}

function StepFirstCheckIn({
  habitName,
  habitEmoji,
  onFinish,
  saving,
}: {
  habitName: string;
  habitEmoji: string;
  onFinish: () => void;
  saving: boolean;
}) {
  const scaleAnim = useRef(new Animated.Value(1)).current;

  const handlePress = () => {
    Animated.sequence([
      Animated.timing(scaleAnim, { toValue: 0.93, duration: 100, useNativeDriver: true }),
      Animated.spring(scaleAnim, { toValue: 1, useNativeDriver: true }),
    ]).start(onFinish);
  };

  return (
    <View style={[s.stepContent, { alignItems: 'center' }]}>
      <Text style={s.headline}>Day 1 starts now.</Text>
      <Text style={s.sub}>Complete your habit once to lock in Day 1.</Text>

      <Animated.View style={[s.firstCheckCard, { transform: [{ scale: scaleAnim }] }]}>
        <Text style={s.firstCheckEmoji}>{habitEmoji}</Text>
        <Text style={s.firstCheckName}>{habitName}</Text>
        <Text style={s.firstCheckSub}>Tap to complete Day 1</Text>
      </Animated.View>

      <TouchableOpacity
        style={[s.primaryBtn, saving && s.primaryBtnDisabled]}
        onPress={saving ? undefined : handlePress}
        activeOpacity={0.85}
      >
        <Text style={s.primaryBtnText}>{saving ? 'Starting streak…' : 'Done — Day 1 locked in ✓'}</Text>
      </TouchableOpacity>
    </View>
  );
}

// ─── Styles ───────────────────────────────────────────────────────────────────

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.bg },
  dotsRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 6,
    paddingTop: 16,
    paddingBottom: 8,
  },
  dot: { width: 6, height: 6, borderRadius: 3, backgroundColor: Colors.border },
  dotActive: { width: 20, backgroundColor: Colors.emerald },
  dotDone: { backgroundColor: Colors.emeraldLight },
  stepWrap: { flex: 1, paddingHorizontal: Spacing.lg },
  stepContent: { flex: 1, paddingTop: Spacing.xl },
  headline: {
    ...Typography.h1,
    color: Colors.text,
    marginBottom: 10,
  },
  sub: {
    ...Typography.body,
    color: Colors.textMuted,
    lineHeight: 24,
    marginBottom: Spacing.xl,
  },
  // Demo card
  demoCard: {
    backgroundColor: Colors.bgCard,
    borderRadius: Radius.lg,
    padding: 20,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 14,
    marginBottom: Spacing.md,
    shadowColor: Colors.shadow,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 1,
    shadowRadius: 12,
    elevation: 4,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  demoCardEmoji: { fontSize: 32 },
  demoCardName: { ...Typography.bodyMed, color: Colors.text },
  demoCardStreak: { ...Typography.caption, color: Colors.textMuted, marginTop: 2 },
  demoSwipeHint: { alignItems: 'center', gap: 2 },
  demoSwipeText: { ...Typography.label, color: Colors.emerald, textTransform: 'uppercase' },
  tapHint: { ...Typography.caption, color: Colors.textLight, textAlign: 'center', marginBottom: Spacing.lg },
  // Trust pills
  trustRow: { flexDirection: 'row', gap: 10, marginBottom: Spacing.xl, justifyContent: 'center' },
  trustPill: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 5,
    backgroundColor: Colors.bgDeep,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: Radius.full,
  },
  trustEmoji: { fontSize: 13 },
  trustLabel: { ...Typography.captionMed, color: Colors.emeraldDark },
  // Category grid
  categoryGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
    marginBottom: Spacing.xl,
  },
  categoryTile: {
    width: (width - Spacing.lg * 2 - 12 * 2) / 3,
    backgroundColor: Colors.bgCard,
    borderRadius: Radius.md,
    paddingVertical: 16,
    alignItems: 'center',
    gap: 6,
    borderWidth: 2,
    borderColor: Colors.border,
  },
  categoryTileSelected: { borderColor: Colors.emerald, backgroundColor: Colors.emeraldSubtle },
  categoryTileEmoji: { fontSize: 28 },
  categoryTileLabel: { ...Typography.captionMed, color: Colors.textMuted },
  categoryTileLabelSelected: { color: Colors.emeraldDark },
  // Preset list
  presetList: { flex: 1, marginBottom: Spacing.md },
  presetRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 14,
    paddingVertical: 14,
    paddingHorizontal: 16,
    borderRadius: Radius.md,
    marginBottom: 8,
    backgroundColor: Colors.bgCard,
    borderWidth: 1.5,
    borderColor: Colors.border,
  },
  presetRowSelected: { borderColor: Colors.emerald, backgroundColor: Colors.emeraldSubtle },
  presetEmoji: { fontSize: 26 },
  presetName: { ...Typography.bodyMed, color: Colors.text },
  presetMvd: { ...Typography.caption, color: Colors.textMuted, marginTop: 2 },
  divider: { height: 1, backgroundColor: Colors.border, marginVertical: 16 },
  customInput: {
    backgroundColor: Colors.bgCard,
    borderWidth: 1.5,
    borderColor: Colors.border,
    borderRadius: Radius.md,
    paddingHorizontal: 16,
    paddingVertical: 14,
    ...Typography.body,
    color: Colors.text,
    marginBottom: 8,
  },
  // MVD
  mvdCard: {
    backgroundColor: Colors.bgCard,
    borderRadius: Radius.lg,
    padding: 20,
    marginBottom: Spacing.lg,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  mvdRow: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  mvdLabel: { ...Typography.bodyMed, color: Colors.text },
  mvdSub: { ...Typography.caption, color: Colors.textMuted, marginTop: 2 },
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
  exampleBox: {
    backgroundColor: Colors.goldLight,
    borderRadius: Radius.md,
    padding: 16,
    marginBottom: Spacing.xl,
  },
  exampleTitle: { ...Typography.captionMed, color: Colors.gold, marginBottom: 6, textTransform: 'uppercase' },
  exampleText: { ...Typography.caption, color: Colors.text, lineHeight: 20, fontStyle: 'italic' },
  // First check-in
  firstCheckCard: {
    backgroundColor: Colors.bgCard,
    borderRadius: Radius.lg,
    padding: 40,
    alignItems: 'center',
    gap: 10,
    marginBottom: Spacing.xl,
    borderWidth: 2,
    borderColor: Colors.emeraldLight,
    shadowColor: Colors.emerald,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 16,
    elevation: 4,
    width: '100%',
  },
  firstCheckEmoji: { fontSize: 52 },
  firstCheckName: { ...Typography.h2, color: Colors.text, textAlign: 'center' },
  firstCheckSub: { ...Typography.body, color: Colors.textMuted },
  // Buttons
  primaryBtn: {
    backgroundColor: Colors.emerald,
    borderRadius: Radius.full,
    paddingVertical: 18,
    alignItems: 'center',
    marginBottom: 12,
  },
  primaryBtnDisabled: { opacity: 0.5 },
  primaryBtnText: { ...Typography.bodyMed, color: '#fff', fontWeight: '700' },
  skipBtn: { alignItems: 'center', paddingVertical: 10 },
  skipBtnText: { ...Typography.body, color: Colors.textMuted },
});
