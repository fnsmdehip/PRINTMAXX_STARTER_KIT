import React from 'react';
import { View, Text, StyleSheet, ScrollView, Share } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SoundTouchable as TouchableOpacity } from '../components/SoundTouchable';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { playSound } from '../sounds/SoundEngine';
import { colors, spacing, radii, typography } from '../theme';
import { ScoreGauge } from '../components/ScoreGauge';
import { StressBar } from '../components/MetricCard';
import { DetectionResult, Verdict } from '../utils/types';
import { DISCLAIMER_SHORT } from '../legal/disclaimer';

const MODE_LABELS: Record<string, string> = {
  finger: 'Finger Pulse', face: 'Face Scan', voice: 'Voice Analysis', multi: 'Multi-Modal',
};

const VERDICT_DESCRIPTIONS: Record<Verdict, string> = {
  truthful: 'Biometric signals suggest low stress and stable physiological responses, consistent with truthful behavior.',
  deceptive: 'Elevated stress indicators detected across monitored channels. This may indicate deception, but could also reflect anxiety or emotional arousal.',
  uncertain: 'Mixed signals detected. Some indicators elevated while others remain stable. Insufficient data for a clear assessment.',
  scanning: 'Analysis in progress...',
};

export function ResultScreen({ route, navigation }: { route: any; navigation: any }) {
  const insets = useSafeAreaInsets();
  const result: DetectionResult = route.params?.result ?? {
    id: 'demo', timestamp: Date.now(), mode: 'finger', verdict: 'uncertain',
    confidence: 0, overallScore: 50, breakdown: { physiological: 0, vocal: 0, facial: 0 }, duration: 0,
  };

  const verdictGradient = result.verdict === 'truthful'
    ? colors.gradient.truthful : result.verdict === 'deceptive'
    ? colors.gradient.deceptive : colors.gradient.uncertain;

  const handleShare = async () => {
    playSound('success');
    const text = `TruthScope Result: ${result.verdict.toUpperCase()} (Score: ${result.overallScore}/100, Confidence: ${result.confidence}%)${
      result.question ? `\nQuestion: "${result.question}"` : ''
    }\n\nDownload TruthScope - the real lie detector app.`;
    try { await Share.share({ message: text }); } catch {}
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={[styles.content, { paddingTop: insets.top + spacing.md }]}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => { playSound('swipe'); navigation.goBack(); }} style={styles.backButton} sound="tap">
          <Ionicons name="arrow-back" size={24} color={colors.text.primary} />
        </TouchableOpacity>
        <Text style={styles.title}>Analysis Result</Text>
        <TouchableOpacity onPress={handleShare} style={styles.shareButton} sound="tap">
          <Ionicons name="share-outline" size={24} color={colors.accent.primary} />
        </TouchableOpacity>
      </View>

      {result.question && (
        <View style={styles.questionCard}>
          <Ionicons name="help-circle" size={20} color={colors.accent.primary} />
          <Text style={styles.questionText}>{result.question}</Text>
        </View>
      )}

      <View style={styles.gaugeContainer}>
        <ScoreGauge score={result.overallScore} verdict={result.verdict} confidence={result.confidence} size={220} />
      </View>

      <LinearGradient colors={[...verdictGradient]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }} style={styles.verdictBanner}>
        <Text style={styles.verdictText}>{result.verdict.toUpperCase()}</Text>
      </LinearGradient>

      <Text style={styles.verdictDescription}>{VERDICT_DESCRIPTIONS[result.verdict]}</Text>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Signal Breakdown</Text>
        <View style={styles.breakdownCard}>
          {result.breakdown.physiological > 0 && <StressBar level={result.breakdown.physiological} label="Physiological Stress" />}
          {result.breakdown.vocal > 0 && <StressBar level={result.breakdown.vocal} label="Vocal Stress" />}
          {result.breakdown.facial > 0 && <StressBar level={result.breakdown.facial} label="Facial Indicators" />}
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Session Details</Text>
        <View style={styles.infoCard}>
          {[
            { icon: 'pulse' as keyof typeof Ionicons.glyphMap, label: 'Mode', value: MODE_LABELS[result.mode] ?? result.mode },
            { icon: 'time' as keyof typeof Ionicons.glyphMap, label: 'Duration', value: `${Math.round(result.duration)}s` },
            { icon: 'analytics' as keyof typeof Ionicons.glyphMap, label: 'Confidence', value: `${result.confidence}%` },
            { icon: 'calendar' as keyof typeof Ionicons.glyphMap, label: 'Time', value: new Date(result.timestamp).toLocaleTimeString() },
          ].map((row) => (
            <View key={row.label} style={styles.infoRow}>
              <Ionicons name={row.icon} size={16} color={colors.text.tertiary} />
              <Text style={styles.infoLabel}>{row.label}</Text>
              <Text style={styles.infoValue}>{row.value}</Text>
            </View>
          ))}
        </View>
      </View>

      <View style={styles.disclaimerCard}>
        <Ionicons name="information-circle" size={16} color={colors.text.tertiary} />
        <Text style={styles.disclaimerText}>{DISCLAIMER_SHORT}</Text>
      </View>

      <View style={styles.actions}>
        <TouchableOpacity style={styles.primaryButton} sound="scanStart" haptic="medium"
          onPress={() => navigation.navigate('Detection', { mode: result.mode })}>
          <LinearGradient colors={[...colors.gradient.scanning]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }} style={styles.buttonGradient}>
            <Ionicons name="refresh" size={20} color={colors.text.primary} />
            <Text style={styles.buttonText}>New Session</Text>
          </LinearGradient>
        </TouchableOpacity>
        <TouchableOpacity style={styles.secondaryButton} sound="tap"
          onPress={() => navigation.navigate('Home')}>
          <Text style={styles.secondaryButtonText}>Back to Home</Text>
        </TouchableOpacity>
      </View>

      <View style={{ height: insets.bottom + spacing.lg }} />
    </ScrollView>
  );
}

export default ResultScreen;

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.bg.primary },
  content: { padding: spacing.lg, paddingBottom: 40 },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: spacing.lg },
  backButton: { padding: 8 },
  title: { ...typography.h2, color: colors.text.primary },
  shareButton: { padding: 8 },
  questionCard: { flexDirection: 'row', alignItems: 'center', gap: 10, backgroundColor: colors.bg.card, borderRadius: radii.md, padding: spacing.md, marginBottom: spacing.lg },
  questionText: { ...typography.body, color: colors.text.primary, flex: 1, fontStyle: 'italic' },
  gaugeContainer: { alignItems: 'center', marginVertical: spacing.xl },
  verdictBanner: { borderRadius: radii.lg, padding: spacing.md, alignItems: 'center', marginBottom: spacing.md },
  verdictText: { ...typography.h2, color: colors.text.primary, letterSpacing: 6 },
  verdictDescription: { ...typography.body, color: colors.text.secondary, textAlign: 'center', lineHeight: 22, marginBottom: spacing.xl },
  section: { marginBottom: spacing.lg },
  sectionTitle: { ...typography.h3, color: colors.text.primary, marginBottom: spacing.sm },
  breakdownCard: { backgroundColor: colors.bg.card, borderRadius: radii.md, padding: spacing.md, gap: spacing.md },
  infoCard: { backgroundColor: colors.bg.card, borderRadius: radii.md, padding: spacing.md, gap: spacing.sm },
  infoRow: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  infoLabel: { ...typography.caption, color: colors.text.secondary, flex: 1 },
  infoValue: { ...typography.bodyBold, color: colors.text.primary, fontSize: 14 },
  disclaimerCard: { flexDirection: 'row', gap: 8, backgroundColor: colors.bg.card, borderRadius: radii.md, padding: spacing.md, marginBottom: spacing.lg },
  disclaimerText: { ...typography.small, color: colors.text.tertiary, flex: 1, lineHeight: 16 },
  actions: { gap: spacing.sm },
  primaryButton: { borderRadius: radii.lg, overflow: 'hidden' },
  buttonGradient: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: spacing.sm, paddingVertical: spacing.md },
  buttonText: { ...typography.bodyBold, color: colors.text.primary },
  secondaryButton: { alignItems: 'center', paddingVertical: spacing.md },
  secondaryButtonText: { ...typography.body, color: colors.text.secondary },
});
