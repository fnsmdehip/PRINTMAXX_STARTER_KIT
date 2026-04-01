import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Share,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { colors, spacing, radii, typography } from '../theme';
import { ScoreGauge } from '../components/ScoreGauge';
import { StressBar } from '../components/MetricCard';
import { DetectionResult, Verdict } from '../utils/types';
import { DISCLAIMER_SHORT } from '../legal/disclaimer';

const MODE_LABELS = {
  finger: 'Finger Pulse',
  face: 'Face Scan',
  voice: 'Voice Analysis',
  multi: 'Multi-Modal',
};

const VERDICT_DESCRIPTIONS: Record<Verdict, string> = {
  truthful: 'Biometric signals suggest low stress and stable physiological responses, consistent with truthful behavior.',
  deceptive: 'Elevated stress indicators detected across monitored channels. This may indicate deception, but could also reflect anxiety or emotional arousal.',
  uncertain: 'Mixed signals detected. Some indicators elevated while others remain stable. Insufficient data for a clear assessment.',
  scanning: 'Analysis in progress...',
};

export function ResultScreen({ route, navigation }: { route: any; navigation: any }) {
  const result: DetectionResult = route.params?.result ?? {
    id: 'demo',
    timestamp: Date.now(),
    mode: 'finger',
    verdict: 'uncertain',
    confidence: 0,
    overallScore: 50,
    breakdown: { physiological: 0, vocal: 0, facial: 0 },
    duration: 0,
  };

  const verdictGradient = result.verdict === 'truthful'
    ? colors.gradient.truthful
    : result.verdict === 'deceptive'
    ? colors.gradient.deceptive
    : colors.gradient.uncertain;

  const handleShare = async () => {
    const text = `TruthScope Result: ${result.verdict.toUpperCase()} (Score: ${result.overallScore}/100, Confidence: ${result.confidence}%)${
      result.question ? `\nQuestion: "${result.question}"` : ''
    }\n\nDownload TruthScope - the real lie detector app.`;

    try {
      await Share.share({ message: text });
    } catch {}
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color={colors.text.primary} />
        </TouchableOpacity>
        <Text style={styles.title}>Analysis Result</Text>
        <TouchableOpacity onPress={handleShare} style={styles.shareButton}>
          <Ionicons name="share-outline" size={24} color={colors.accent.primary} />
        </TouchableOpacity>
      </View>

      {/* Question */}
      {result.question && (
        <View style={styles.questionCard}>
          <Ionicons name="help-circle" size={20} color={colors.accent.primary} />
          <Text style={styles.questionText}>{result.question}</Text>
        </View>
      )}

      {/* Main Score */}
      <View style={styles.gaugeContainer}>
        <ScoreGauge
          score={result.overallScore}
          verdict={result.verdict}
          confidence={result.confidence}
          size={220}
        />
      </View>

      {/* Verdict Banner */}
      <LinearGradient
        colors={[...verdictGradient]}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 0 }}
        style={styles.verdictBanner}
      >
        <Text style={styles.verdictText}>{result.verdict.toUpperCase()}</Text>
      </LinearGradient>

      <Text style={styles.verdictDescription}>
        {VERDICT_DESCRIPTIONS[result.verdict]}
      </Text>

      {/* Breakdown */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Signal Breakdown</Text>
        <View style={styles.breakdownCard}>
          {result.breakdown.physiological > 0 && (
            <StressBar level={result.breakdown.physiological} label="Physiological Stress" />
          )}
          {result.breakdown.vocal > 0 && (
            <StressBar level={result.breakdown.vocal} label="Vocal Stress" />
          )}
          {result.breakdown.facial > 0 && (
            <StressBar level={result.breakdown.facial} label="Facial Indicators" />
          )}
        </View>
      </View>

      {/* Session Info */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Session Details</Text>
        <View style={styles.infoCard}>
          <InfoRow icon="pulse" label="Mode" value={MODE_LABELS[result.mode]} />
          <InfoRow icon="time" label="Duration" value={`${Math.round(result.duration)}s`} />
          <InfoRow icon="analytics" label="Confidence" value={`${result.confidence}%`} />
          <InfoRow
            icon="calendar"
            label="Time"
            value={new Date(result.timestamp).toLocaleTimeString()}
          />
        </View>
      </View>

      {/* Disclaimer */}
      <View style={styles.disclaimerCard}>
        <Ionicons name="information-circle" size={16} color={colors.text.tertiary} />
        <Text style={styles.disclaimerText}>{DISCLAIMER_SHORT}</Text>
      </View>

      {/* Actions */}
      <View style={styles.actions}>
        <TouchableOpacity
          style={styles.primaryButton}
          onPress={() => navigation.navigate('Detection', { mode: result.mode })}
        >
          <LinearGradient
            colors={[...colors.gradient.scanning]}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.buttonGradient}
          >
            <Ionicons name="refresh" size={20} color={colors.text.primary} />
            <Text style={styles.buttonText}>New Session</Text>
          </LinearGradient>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.secondaryButton}
          onPress={() => navigation.navigate('Home')}
        >
          <Text style={styles.secondaryButtonText}>Back to Home</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

function InfoRow({ icon, label, value }: {
  icon: keyof typeof Ionicons.glyphMap;
  label: string;
  value: string;
}) {
  return (
    <View style={styles.infoRow}>
      <Ionicons name={icon} size={16} color={colors.text.tertiary} />
      <Text style={styles.infoLabel}>{label}</Text>
      <Text style={styles.infoValue}>{value}</Text>
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
    marginBottom: spacing.lg,
  },
  backButton: {
    padding: 8,
  },
  title: {
    ...typography.h2,
    color: colors.text.primary,
  },
  shareButton: {
    padding: 8,
  },
  questionCard: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    backgroundColor: colors.bg.card,
    borderRadius: radii.md,
    padding: spacing.md,
    marginBottom: spacing.lg,
  },
  questionText: {
    ...typography.body,
    color: colors.text.primary,
    flex: 1,
    fontStyle: 'italic',
  },
  gaugeContainer: {
    alignItems: 'center',
    marginVertical: spacing.xl,
  },
  verdictBanner: {
    borderRadius: radii.lg,
    padding: spacing.md,
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  verdictText: {
    ...typography.h2,
    color: colors.text.primary,
    letterSpacing: 6,
  },
  verdictDescription: {
    ...typography.body,
    color: colors.text.secondary,
    textAlign: 'center',
    lineHeight: 22,
    marginBottom: spacing.xl,
  },
  section: {
    marginBottom: spacing.lg,
  },
  sectionTitle: {
    ...typography.h3,
    color: colors.text.primary,
    marginBottom: spacing.sm,
  },
  breakdownCard: {
    backgroundColor: colors.bg.card,
    borderRadius: radii.md,
    padding: spacing.md,
    gap: spacing.md,
  },
  infoCard: {
    backgroundColor: colors.bg.card,
    borderRadius: radii.md,
    padding: spacing.md,
    gap: spacing.sm,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  infoLabel: {
    ...typography.caption,
    color: colors.text.secondary,
    flex: 1,
  },
  infoValue: {
    ...typography.bodyBold,
    color: colors.text.primary,
    fontSize: 14,
  },
  disclaimerCard: {
    flexDirection: 'row',
    gap: 8,
    backgroundColor: colors.bg.tertiary,
    borderRadius: radii.sm,
    padding: spacing.md,
    marginBottom: spacing.xl,
  },
  disclaimerText: {
    ...typography.small,
    color: colors.text.tertiary,
    flex: 1,
    lineHeight: 16,
  },
  actions: {
    gap: spacing.md,
  },
  primaryButton: {
    borderRadius: radii.lg,
    overflow: 'hidden',
  },
  buttonGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    padding: spacing.md,
  },
  buttonText: {
    ...typography.bodyBold,
    color: colors.text.primary,
  },
  secondaryButton: {
    alignItems: 'center',
    padding: spacing.md,
  },
  secondaryButtonText: {
    ...typography.body,
    color: colors.text.secondary,
  },
});
