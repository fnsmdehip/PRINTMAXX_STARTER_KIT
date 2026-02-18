import React, { useMemo } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { useUserStore } from '../../src/stores/userStore';
import { useProtocolStore } from '../../src/stores/protocolStore';
import { useSubscriptionStore } from '../../src/stores/subscriptionStore';
import { ProtocolRing, StreakBadge } from '../../src/components';
import { COLORS, TIPS_OF_THE_DAY, DEFAULT_PROTOCOLS } from '../../src/utils/constants';
import { getGreeting } from '../../src/utils/dateUtils';

const { width } = Dimensions.get('window');
const RING_SIZE = (width - 72) / 3;

export default function Dashboard() {
  const user = useUserStore((state) => state.user);
  const getDailyLongevityScore = useProtocolStore((state) => state.getDailyLongevityScore);
  const getTodayProgress = useProtocolStore((state) => state.getTodayProgress);
  const getTodayLog = useProtocolStore((state) => state.getTodayLog);
  const getProtocolStreak = useProtocolStore((state) => state.getProtocolStreak);
  const canAccessPremiumContent = useSubscriptionStore((state) => state.canAccessPremiumContent);

  const longevityScore = getDailyLongevityScore();
  const greeting = getGreeting();

  // Get free protocols for dashboard display
  const dashboardProtocols = useMemo(() => {
    return DEFAULT_PROTOCOLS.filter((p) => !p.isPremium).slice(0, 6);
  }, []);

  const tipOfTheDay = useMemo(() => {
    const dayOfYear = Math.floor(
      (Date.now() - new Date(new Date().getFullYear(), 0, 0).getTime()) /
        (1000 * 60 * 60 * 24)
    );
    return TIPS_OF_THE_DAY[dayOfYear % TIPS_OF_THE_DAY.length];
  }, []);

  const handleProtocolPress = (protocolId: string) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    router.push('/protocols');
  };

  const formatValue = (protocolId: string, value: number, unit: string) => {
    if (unit === 'hours') return `${value.toFixed(1)}h`;
    if (unit === 'minutes') return `${Math.round(value)}m`;
    return `${value}`;
  };

  const getScoreColor = () => {
    if (longevityScore >= 80) return COLORS.accent;
    if (longevityScore >= 50) return COLORS.primary;
    if (longevityScore >= 25) return COLORS.secondary;
    return COLORS.textMuted;
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>{greeting}</Text>
            <Text style={styles.name}>{user?.name || 'Biohacker'}</Text>
          </View>
          {user && user.streakDays > 0 && (
            <StreakBadge streak={user.streakDays} size="medium" showLabel />
          )}
        </View>

        {/* Longevity Score Card */}
        <View style={styles.scoreCard}>
          <View style={styles.scoreHeader}>
            <Text style={styles.scoreLabel}>Daily Longevity Score</Text>
            <Ionicons name="information-circle-outline" size={18} color={COLORS.textMuted} />
          </View>
          <View style={styles.scoreContent}>
            <Text style={[styles.scoreValue, { color: getScoreColor() }]}>
              {longevityScore}
            </Text>
            <Text style={styles.scorePercent}>%</Text>
          </View>
          <View style={styles.scoreBar}>
            <View
              style={[
                styles.scoreBarFill,
                {
                  width: `${longevityScore}%`,
                  backgroundColor: getScoreColor(),
                },
              ]}
            />
          </View>
          <Text style={styles.scoreHint}>
            {longevityScore >= 80
              ? 'Excellent! Keep it up!'
              : longevityScore >= 50
              ? 'Good progress today'
              : 'Complete more protocols to boost your score'}
          </Text>
        </View>

        {/* Protocol Rings Grid */}
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Today's Protocols</Text>
          <TouchableOpacity
            onPress={() => {
              Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
              router.push('/protocols');
            }}
          >
            <Text style={styles.seeAllText}>See All</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.ringsGrid}>
          {dashboardProtocols.map((protocol) => {
            const progress = getTodayProgress(protocol.id);
            const value = getTodayLog(protocol.id);

            return (
              <TouchableOpacity
                key={protocol.id}
                style={styles.ringContainer}
                onPress={() => handleProtocolPress(protocol.id)}
                activeOpacity={0.7}
              >
                <ProtocolRing
                  progress={progress}
                  icon={protocol.icon}
                  label={protocol.name.split(' ')[0]}
                  value={formatValue(protocol.id, value, protocol.unit)}
                  size={RING_SIZE}
                  color={progress >= 100 ? COLORS.accent : COLORS.primary}
                />
              </TouchableOpacity>
            );
          })}
        </View>

        {/* Quick Actions */}
        <View style={styles.quickActions}>
          <TouchableOpacity
            style={styles.quickAction}
            onPress={() => {
              Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
              router.push('/protocols');
            }}
            activeOpacity={0.8}
          >
            <Ionicons name="timer-outline" size={24} color={COLORS.text} />
            <Text style={styles.quickActionText}>Start Fasting</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.quickAction}
            onPress={() => {
              Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
              router.push('/protocols');
            }}
            activeOpacity={0.8}
          >
            <Ionicons name="snow-outline" size={24} color={COLORS.text} />
            <Text style={styles.quickActionText}>Cold Session</Text>
          </TouchableOpacity>
        </View>

        {/* Tip of the Day */}
        <View style={styles.tipCard}>
          <View style={styles.tipHeader}>
            <Ionicons name="bulb-outline" size={20} color={COLORS.secondary} />
            <Text style={styles.tipLabel}>Tip of the Day</Text>
          </View>
          <Text style={styles.tipText}>{tipOfTheDay}</Text>
        </View>

        {/* Upgrade CTA for free users */}
        {!canAccessPremiumContent() && (
          <TouchableOpacity
            style={styles.upgradeCard}
            onPress={() => {
              Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
              router.push('/profile');
            }}
            activeOpacity={0.9}
          >
            <View style={styles.upgradeContent}>
              <Ionicons name="lock-open-outline" size={24} color={COLORS.primary} />
              <View style={styles.upgradeText}>
                <Text style={styles.upgradeTitle}>Unlock Premium</Text>
                <Text style={styles.upgradeSubtitle}>
                  Access all 10+ protocols and guides
                </Text>
              </View>
            </View>
            <Ionicons name="arrow-forward" size={20} color={COLORS.primary} />
          </TouchableOpacity>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: 20,
    paddingBottom: 100,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24,
  },
  greeting: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 4,
  },
  name: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.text,
  },
  scoreCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 20,
    padding: 20,
    marginBottom: 24,
  },
  scoreHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  scoreLabel: {
    fontSize: 14,
    color: COLORS.textSecondary,
    fontWeight: '500',
  },
  scoreContent: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    marginBottom: 12,
  },
  scoreValue: {
    fontSize: 56,
    fontWeight: '700',
    lineHeight: 60,
  },
  scorePercent: {
    fontSize: 24,
    fontWeight: '600',
    color: COLORS.textMuted,
    marginBottom: 8,
    marginLeft: 4,
  },
  scoreBar: {
    height: 8,
    backgroundColor: COLORS.surfaceLight,
    borderRadius: 4,
    marginBottom: 12,
    overflow: 'hidden',
  },
  scoreBarFill: {
    height: '100%',
    borderRadius: 4,
  },
  scoreHint: {
    fontSize: 13,
    color: COLORS.textSecondary,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
  },
  seeAllText: {
    fontSize: 14,
    color: COLORS.primary,
    fontWeight: '500',
  },
  ringsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 24,
  },
  ringContainer: {
    width: RING_SIZE,
    height: RING_SIZE + 20,
    marginBottom: 16,
    alignItems: 'center',
  },
  quickActions: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 24,
  },
  quickAction: {
    flex: 1,
    backgroundColor: COLORS.surface,
    borderRadius: 14,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  quickActionText: {
    fontSize: 14,
    fontWeight: '500',
    color: COLORS.text,
  },
  tipCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
    borderLeftWidth: 3,
    borderLeftColor: COLORS.secondary,
  },
  tipHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 8,
  },
  tipLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.secondary,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  tipText: {
    fontSize: 14,
    color: COLORS.text,
    lineHeight: 20,
  },
  upgradeCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    borderWidth: 1,
    borderColor: COLORS.primaryDark,
  },
  upgradeContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    flex: 1,
  },
  upgradeText: {
    flex: 1,
  },
  upgradeTitle: {
    fontSize: 15,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 2,
  },
  upgradeSubtitle: {
    fontSize: 13,
    color: COLORS.textSecondary,
  },
});
