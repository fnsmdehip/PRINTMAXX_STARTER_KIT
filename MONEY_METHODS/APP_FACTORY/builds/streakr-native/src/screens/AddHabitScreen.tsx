import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  TextInput,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Colors, Spacing, Radius, Typography } from '../constants/theme';
import { HABIT_PRESETS } from '../constants/habits';
import { createHabit, addHabit } from '../services/storage';
import { HabitCategory, RootStackParamList } from '../types';

type NavProp = NativeStackNavigationProp<RootStackParamList>;

const CATEGORIES: { label: string; value: HabitCategory; emoji: string }[] = [
  { label: 'Fitness', value: 'fitness', emoji: '💪' },
  { label: 'Mindfulness', value: 'mindfulness', emoji: '🧘' },
  { label: 'Learning', value: 'learning', emoji: '📚' },
  { label: 'Creation', value: 'creation', emoji: '✍️' },
  { label: 'Health', value: 'health', emoji: '💚' },
  { label: 'Sobriety', value: 'sobriety', emoji: '🧠' },
  { label: 'Custom', value: 'custom', emoji: '⭐' },
];

export default function AddHabitScreen() {
  const navigation = useNavigation<NavProp>();
  const [category, setCategory] = useState<HabitCategory>('fitness');
  const [selectedPreset, setSelectedPreset] = useState<string | null>(null);
  const [customName, setCustomName] = useState('');
  const [customEmoji, setCustomEmoji] = useState('⭐');
  const [mvdEnabled, setMvdEnabled] = useState(false);
  const [mvdLabel, setMvdLabel] = useState('');
  const [saving, setSaving] = useState(false);

  const presets = HABIT_PRESETS.filter(p => p.category === category);
  const chosenPreset = HABIT_PRESETS.find(p => p.name === selectedPreset);

  const canSave = selectedPreset !== null || customName.trim().length > 0;

  const handleSave = async () => {
    if (!canSave) return;
    setSaving(true);
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

    const name = chosenPreset?.name ?? customName.trim();
    const emoji = chosenPreset?.emoji ?? customEmoji;
    const cat = chosenPreset?.category ?? category;
    const mvd = mvdEnabled ? (mvdLabel.trim() || chosenPreset?.mvdLabel || '') : '';

    const habit = createHabit(name, emoji, cat, mvdEnabled, mvd);
    await addHabit(habit);
    navigation.goBack();
  };

  return (
    <SafeAreaView style={s.container}>
      <KeyboardAvoidingView style={{ flex: 1 }} behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
        {/* Header */}
        <View style={s.header}>
          <TouchableOpacity onPress={() => navigation.goBack()}>
            <Ionicons name="chevron-back" size={24} color={Colors.text} />
          </TouchableOpacity>
          <Text style={s.headerTitle}>Add habit</Text>
          <TouchableOpacity onPress={canSave ? handleSave : undefined} disabled={!canSave || saving}>
            <Text style={[s.saveText, !canSave && s.saveTextDisabled]}>
              {saving ? 'Saving…' : 'Save'}
            </Text>
          </TouchableOpacity>
        </View>

        <ScrollView contentContainerStyle={s.scroll} showsVerticalScrollIndicator={false}>
          {/* Category picker */}
          <Text style={s.sectionLabel}>Category</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={s.catScroll}>
            {CATEGORIES.map(c => (
              <TouchableOpacity
                key={c.value}
                style={[s.catChip, category === c.value && s.catChipSelected]}
                onPress={() => { Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light); setCategory(c.value); setSelectedPreset(null); }}
              >
                <Text style={s.catChipEmoji}>{c.emoji}</Text>
                <Text style={[s.catChipLabel, category === c.value && s.catChipLabelSelected]}>{c.label}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>

          {/* Preset list */}
          {presets.length > 0 && (
            <>
              <Text style={s.sectionLabel}>Quick picks</Text>
              {presets.map(p => (
                <TouchableOpacity
                  key={p.name}
                  style={[s.presetRow, selectedPreset === p.name && s.presetRowSelected]}
                  onPress={() => {
                    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
                    setSelectedPreset(p.name);
                    setMvdLabel(p.mvdLabel);
                  }}
                  activeOpacity={0.75}
                >
                  <Text style={s.presetEmoji}>{p.emoji}</Text>
                  <View style={{ flex: 1 }}>
                    <Text style={s.presetName}>{p.name}</Text>
                    <Text style={s.presetMvd} numberOfLines={1}>MVD: {p.mvdLabel}</Text>
                  </View>
                  {selectedPreset === p.name && (
                    <Ionicons name="checkmark-circle" size={22} color={Colors.emerald} />
                  )}
                </TouchableOpacity>
              ))}
            </>
          )}

          {/* Custom name */}
          <Text style={s.sectionLabel}>Or name your own</Text>
          <TextInput
            style={s.input}
            placeholder="e.g. No scrolling in bed"
            placeholderTextColor={Colors.textLight}
            value={customName}
            onChangeText={t => { setCustomName(t); if (t) setSelectedPreset(null); }}
            maxLength={50}
          />

          {/* MVD toggle */}
          <Text style={s.sectionLabel}>Minimum Viable Day</Text>
          <View style={s.mvdCard}>
            <View style={s.mvdRow}>
              <View style={{ flex: 1 }}>
                <Text style={s.mvdTitle}>Enable MVD mode</Text>
                <Text style={s.mvdSub}>The smallest version that still counts</Text>
              </View>
              <TouchableOpacity
                style={[s.toggle, mvdEnabled && s.toggleOn]}
                onPress={() => { Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light); setMvdEnabled(v => !v); }}
              >
                <View style={[s.toggleThumb, mvdEnabled && s.toggleThumbOn]} />
              </TouchableOpacity>
            </View>
            {mvdEnabled && (
              <TextInput
                style={[s.input, { marginTop: 12, marginBottom: 0 }]}
                placeholder={chosenPreset?.mvdLabel || 'e.g. Do 5 pushups'}
                placeholderTextColor={Colors.textLight}
                value={mvdLabel}
                onChangeText={setMvdLabel}
                maxLength={80}
              />
            )}
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.bg },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: Spacing.lg,
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  headerTitle: { ...Typography.h3, color: Colors.text },
  saveText: { ...Typography.bodyMed, color: Colors.emerald, fontWeight: '700' },
  saveTextDisabled: { color: Colors.textLight },
  scroll: { padding: Spacing.lg, paddingBottom: 48 },
  sectionLabel: { ...Typography.captionMed, color: Colors.textMuted, textTransform: 'uppercase', letterSpacing: 0.5, marginBottom: 10, marginTop: Spacing.lg },
  catScroll: { marginBottom: Spacing.md },
  catChip: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 16,
    paddingVertical: 9,
    borderRadius: Radius.full,
    backgroundColor: Colors.bgCard,
    borderWidth: 1.5,
    borderColor: Colors.border,
    marginRight: 8,
  },
  catChipSelected: { borderColor: Colors.emerald, backgroundColor: Colors.emeraldSubtle },
  catChipEmoji: { fontSize: 16 },
  catChipLabel: { ...Typography.captionMed, color: Colors.textMuted },
  catChipLabelSelected: { color: Colors.emeraldDark },
  presetRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 14,
    padding: 14,
    borderRadius: Radius.md,
    borderWidth: 1.5,
    borderColor: Colors.border,
    backgroundColor: Colors.bgCard,
    marginBottom: 8,
  },
  presetRowSelected: { borderColor: Colors.emerald, backgroundColor: Colors.emeraldSubtle },
  presetEmoji: { fontSize: 26 },
  presetName: { ...Typography.bodyMed, color: Colors.text },
  presetMvd: { ...Typography.caption, color: Colors.textMuted, marginTop: 2 },
  input: {
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
  mvdCard: {
    backgroundColor: Colors.bgCard,
    borderRadius: Radius.lg,
    padding: 16,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  mvdRow: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  mvdTitle: { ...Typography.bodyMed, color: Colors.text },
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
});
