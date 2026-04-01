import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  SafeAreaView,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { Colors, Spacing, Radius, Typography } from '../constants/theme';
import { MODES } from '../constants/modes';
import { getStreakData } from '../services/storage';
import { useFocusEffect } from '@react-navigation/native';
import { useCallback } from 'react';

export default function EmergencyScreen() {
  const navigation = useNavigation();
  const [promptIndex, setPromptIndex] = useState(0);
  const [mode, setMode] = useState<keyof typeof MODES>('nofap');
  const [breathPhase, setBreathPhase] = useState<'inhale' | 'hold' | 'exhale' | null>(null);
  const [breathCount, setBreathCount] = useState(0);

  useFocusEffect(useCallback(() => {
    getStreakData().then(data => {
      if (data) setMode(data.mode);
    });
  }, []));

  const prompts = MODES[mode].urgePrompts;

  const nextPrompt = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    setPromptIndex(i => (i + 1) % prompts.length);
  };

  const startBreathing = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    setBreathPhase('inhale');
    setBreathCount(0);

    const runCycle = (cycleNum: number) => {
      if (cycleNum >= 3) { setBreathPhase(null); return; }
      setBreathPhase('inhale');
      setTimeout(() => setBreathPhase('hold'), 4000);
      setTimeout(() => setBreathPhase('exhale'), 11000);
      setTimeout(() => runCycle(cycleNum + 1), 19000);
    };
    runCycle(0);
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Ionicons name="close" size={28} color={Colors.text} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Emergency Help</Text>
        <View style={{ width: 28 }} />
      </View>

      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scroll}>

        {/* Urge surfing prompt */}
        <View style={styles.section}>
          <Text style={styles.sectionLabel}>URGE SURFING</Text>
          <View style={styles.promptCard}>
            <Text style={styles.promptText}>{prompts[promptIndex]}</Text>
          </View>
          <TouchableOpacity style={styles.nextPromptBtn} onPress={nextPrompt}>
            <Text style={styles.nextPromptText}>Different prompt</Text>
            <Ionicons name="refresh-outline" size={16} color={Colors.primary} />
          </TouchableOpacity>
        </View>

        {/* Box breathing */}
        <View style={styles.section}>
          <Text style={styles.sectionLabel}>BOX BREATHING</Text>
          <Text style={styles.sectionDesc}>4 counts in, 7 hold, 8 out. Activates your parasympathetic system instantly.</Text>
          {breathPhase ? (
            <View style={styles.breathCard}>
              <Text style={styles.breathPhaseText}>
                {breathPhase === 'inhale' && 'Breathe in...'}
                {breathPhase === 'hold' && 'Hold...'}
                {breathPhase === 'exhale' && 'Breathe out...'}
              </Text>
              <Text style={styles.breathSubText}>
                {breathPhase === 'inhale' && '4 seconds'}
                {breathPhase === 'hold' && '7 seconds'}
                {breathPhase === 'exhale' && '8 seconds'}
              </Text>
            </View>
          ) : (
            <TouchableOpacity style={styles.breathButton} onPress={startBreathing}>
              <Ionicons name="fitness-outline" size={22} color={Colors.background} />
              <Text style={styles.breathButtonText}>Start 3-Cycle Breathing</Text>
            </TouchableOpacity>
          )}
        </View>

        {/* Cold water reminder */}
        <View style={styles.section}>
          <Text style={styles.sectionLabel}>QUICK INTERRUPTS</Text>
          {['Splash cold water on your face right now.', 'Do 20 pushups. Your body chemistry changes.', 'Text or call one person. Break isolation.', 'Step outside. Sunlight and fresh air shift your state.'].map(action => (
            <View key={action} style={styles.actionItem}>
              <Ionicons name="checkmark-circle-outline" size={20} color={Colors.primary} />
              <Text style={styles.actionText}>{action}</Text>
            </View>
          ))}
        </View>

        {/* Streak reminder */}
        <View style={styles.streakReminder}>
          <Text style={styles.streakReminderText}>
            Your streak is the answer. If you act now, you lose everything you built. If you wait 20 minutes, the urge will pass.
          </Text>
        </View>

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
  section: { marginBottom: Spacing.xl },
  sectionLabel: { ...Typography.tiny, textTransform: 'uppercase', letterSpacing: 2, color: Colors.textTertiary, marginBottom: Spacing.sm },
  sectionDesc: { ...Typography.bodySecondary, marginBottom: Spacing.md },
  promptCard: {
    backgroundColor: Colors.surfaceAlt, padding: Spacing.lg, borderRadius: Radius.lg,
    borderLeftWidth: 4, borderLeftColor: Colors.primary,
  },
  promptText: { ...Typography.body, lineHeight: 26 },
  nextPromptBtn: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'flex-end', gap: Spacing.xs, marginTop: Spacing.sm,
  },
  nextPromptText: { ...Typography.body, color: Colors.primary },
  breathCard: {
    backgroundColor: Colors.surface, padding: Spacing.xl, borderRadius: Radius.xl, alignItems: 'center',
    borderWidth: 2, borderColor: Colors.primary,
  },
  breathPhaseText: { ...Typography.h2, marginBottom: Spacing.xs },
  breathSubText: { ...Typography.bodySecondary },
  breathButton: {
    backgroundColor: Colors.primary, flexDirection: 'row', alignItems: 'center',
    justifyContent: 'center', padding: Spacing.lg, borderRadius: Radius.lg, gap: Spacing.sm,
  },
  breathButtonText: { ...Typography.body, color: Colors.background, fontWeight: '700' },
  actionItem: {
    flexDirection: 'row', alignItems: 'flex-start', gap: Spacing.sm,
    paddingVertical: Spacing.sm,
  },
  actionText: { ...Typography.body, flex: 1, lineHeight: 22 },
  streakReminder: {
    backgroundColor: Colors.surface, padding: Spacing.lg, borderRadius: Radius.lg,
    borderWidth: 2, borderColor: Colors.accent, marginBottom: Spacing.xl,
  },
  streakReminderText: { ...Typography.body, fontWeight: '600', lineHeight: 24, color: Colors.accent },
});
