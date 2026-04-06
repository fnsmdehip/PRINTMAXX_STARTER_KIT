import React, { useCallback, useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Alert,
  Dimensions,
  RefreshControl,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SoundTouchable as TouchableOpacity } from '../components/SoundTouchable';
import { LinearGradient } from 'expo-linear-gradient';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withRepeat,
  withSequence,
  withDelay,
  Easing,
  FadeInDown,
  FadeInRight,
} from 'react-native-reanimated';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { colors, spacing, radii, typography } from '../theme';
import { getSessions, getProfile } from '../store';
import { SessionData, DetectionMode, UserProfile, Verdict } from '../utils/types';

const { width: SCREEN_WIDTH } = Dimensions.get('window');
const CARD_GAP = spacing.sm;
const CARD_SIZE = (SCREEN_WIDTH - spacing.lg * 2 - CARD_GAP) / 2;

// --- Types ---

interface DetectionModeConfig {
  mode: DetectionMode;
  label: string;
  subtitle: string;
  icon: keyof typeof Ionicons.glyphMap;
  accentColor: string;
  isPremiumOnly: boolean;
}

const DETECTION_MODES: DetectionModeConfig[] = [
  {
    mode: 'finger',
    label: 'Finger Pulse',
    subtitle: 'Gold standard accuracy',
    icon: 'finger-print',
    accentColor: colors.accent.primary,
    isPremiumOnly: false,
  },
  {
    mode: 'face',
    label: 'Face Scan',
    subtitle: 'Contactless analysis',
    icon: 'scan-outline',
    accentColor: colors.accent.secondary,
    isPremiumOnly: false,
  },
  {
    mode: 'voice',
    label: 'Voice Analysis',
    subtitle: 'Stress in every word',
    icon: 'mic-outline',
    accentColor: colors.accent.tertiary,
    isPremiumOnly: false,
  },
  {
    mode: 'multi',
    label: 'Multi-Modal',
    subtitle: 'Maximum detection',
    icon: 'layers-outline',
    accentColor: colors.accent.secondary,
    isPremiumOnly: true,
  },
];

// --- Helpers ---

function formatTimestamp(ts: number): string {
  const date = new Date(ts);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);

  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  const diffHours = Math.floor(diffMins / 60);
  if (diffHours < 24) return `${diffHours}h ago`;
  const diffDays = Math.floor(diffHours / 24);
  if (diffDays < 7) return `${diffDays}d ago`;

  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

function getModeIcon(mode: DetectionMode): keyof typeof Ionicons.glyphMap {
  const map: Record<DetectionMode, keyof typeof Ionicons.glyphMap> = {
    finger: 'finger-print',
    face: 'scan-outline',
    voice: 'mic-outline',
    multi: 'layers-outline',
  };
  return map[mode];
}

function getVerdictColor(verdict: Verdict): string {
  const map: Record<Verdict, string> = {
    truthful: colors.accent.success,
    deceptive: colors.accent.tertiary,
    uncertain: colors.accent.warning,
    scanning: colors.accent.primary,
  };
  return map[verdict];
}

function getVerdictLabel(verdict: Verdict): string {
  const map: Record<Verdict, string> = {
    truthful: 'TRUTH',
    deceptive: 'DECEPTION',
    uncertain: 'UNCERTAIN',
    scanning: 'SCANNING',
  };
  return map[verdict];
}

function getLastVerdict(session: SessionData): { verdict: Verdict; score: number } {
  if (session.results.length === 0) {
    return { verdict: 'uncertain', score: 0 };
  }
  const last = session.results[session.results.length - 1];
  return { verdict: last.verdict, score: last.overallScore };
}

// --- Components ---

function LogoGlow() {
  const glowOpacity = useSharedValue(0.4);

  useEffect(() => {
    glowOpacity.value = withRepeat(
      withSequence(
        withTiming(0.8, { duration: 2000, easing: Easing.inOut(Easing.sin) }),
        withTiming(0.4, { duration: 2000, easing: Easing.inOut(Easing.sin) }),
      ),
      -1,
      false,
    );
  }, []);

  const glowStyle = useAnimatedStyle(() => ({
    opacity: glowOpacity.value,
  }));

  return (
    <Animated.View style={[styles.logoGlow, glowStyle]}>
      <LinearGradient
        colors={[colors.accent.primary, 'transparent']}
        style={styles.logoGlowGradient}
        start={{ x: 0.5, y: 0 }}
        end={{ x: 0.5, y: 1 }}
      />
    </Animated.View>
  );
}

function ModeCard({
  config,
  isPremium,
  index,
  onPress,
}: {
  config: DetectionModeConfig;
  isPremium: boolean;
  index: number;
  onPress: () => void;
}) {
  const scale = useSharedValue(1);
  const locked = config.isPremiumOnly && !isPremium;

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  const handlePressIn = () => {
    scale.value = withTiming(0.95, { duration: 100 });
  };

  const handlePressOut = () => {
    scale.value = withTiming(1, { duration: 150 });
  };

  const isMultiModal = config.mode === 'multi';

  return (
    <Animated.View
      entering={FadeInDown.delay(100 + index * 80).duration(400)}
      style={animatedStyle}
    >
      <TouchableOpacity
        onPress={onPress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        activeOpacity={0.85}
        style={[styles.modeCard, { width: CARD_SIZE }]}
      >
        {isMultiModal ? (
          <LinearGradient
            colors={[...colors.gradient.scanning]}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
            style={styles.modeCardGradientBorder}
          >
            <View style={styles.modeCardInner}>
              <ModeCardContent config={config} locked={locked} />
            </View>
          </LinearGradient>
        ) : (
          <View style={styles.modeCardContent}>
            <ModeCardContent config={config} locked={locked} />
          </View>
        )}
      </TouchableOpacity>
    </Animated.View>
  );
}

function ModeCardContent({
  config,
  locked,
}: {
  config: DetectionModeConfig;
  locked: boolean;
}) {
  return (
    <>
      <View
        style={[
          styles.modeIconContainer,
          { backgroundColor: config.accentColor + '18' },
        ]}
      >
        <Ionicons
          name={config.icon}
          size={28}
          color={locked ? colors.text.tertiary : config.accentColor}
        />
      </View>
      <Text
        style={[
          styles.modeLabel,
          locked && { color: colors.text.tertiary },
        ]}
      >
        {config.label}
      </Text>
      <Text style={styles.modeSubtitle}>{config.subtitle}</Text>
      {locked && (
        <View style={styles.premiumBadge}>
          <LinearGradient
            colors={[...colors.gradient.premium]}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.premiumBadgeGradient}
          >
            <Ionicons name="diamond" size={10} color="#FFFFFF" />
            <Text style={styles.premiumBadgeText}>PRO</Text>
          </LinearGradient>
        </View>
      )}
    </>
  );
}

function PartyModeBanner({
  index,
  onPress,
}: {
  index: number;
  onPress: () => void;
}) {
  const shimmerOffset = useSharedValue(-1);

  useEffect(() => {
    shimmerOffset.value = withRepeat(
      withTiming(1, { duration: 3000, easing: Easing.linear }),
      -1,
      false,
    );
  }, []);

  return (
    <Animated.View entering={FadeInDown.delay(100 + index * 80).duration(400)}>
      <TouchableOpacity
        onPress={onPress}
        activeOpacity={0.85}
        style={styles.partyBanner}
      >
        <LinearGradient
          colors={['#7B61FF', '#FF3D71', '#FFAA00']}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={styles.partyGradient}
        >
          <View style={styles.partyContent}>
            <View style={styles.partyTextBlock}>
              <View style={styles.partyHeaderRow}>
                <Text style={styles.partyIcon}>🎉</Text>
                <Text style={styles.partyTitle}>Party Mode</Text>
              </View>
              <Text style={styles.partySubtitle}>
                Pass the phone. Ask questions. Find the liar.
              </Text>
            </View>
            <View style={styles.partyArrow}>
              <Ionicons name="chevron-forward" size={24} color="#FFFFFF" />
            </View>
          </View>
        </LinearGradient>
      </TouchableOpacity>
    </Animated.View>
  );
}

function SessionItem({
  session,
  index,
  onPress,
}: {
  session: SessionData;
  index: number;
  onPress: () => void;
}) {
  const { verdict, score } = getLastVerdict(session);
  const verdictColor = getVerdictColor(verdict);

  return (
    <Animated.View entering={FadeInRight.delay(index * 60).duration(300)}>
      <TouchableOpacity
        onPress={onPress}
        activeOpacity={0.7}
        style={styles.sessionItem}
      >
        <View style={[styles.sessionIcon, { backgroundColor: verdictColor + '18' }]}>
          <Ionicons
            name={getModeIcon(session.mode)}
            size={20}
            color={verdictColor}
          />
        </View>
        <View style={styles.sessionInfo}>
          <Text style={styles.sessionMode}>
            {session.isPartyMode ? 'Party Mode' : DETECTION_MODES.find(m => m.mode === session.mode)?.label ?? session.mode}
          </Text>
          <Text style={styles.sessionTime}>
            {formatTimestamp(session.startTime)}
            {session.results.length > 0 && ` \u00B7 ${session.results.length} test${session.results.length > 1 ? 's' : ''}`}
          </Text>
        </View>
        <View style={styles.sessionResult}>
          <View style={[styles.verdictBadge, { backgroundColor: verdictColor + '20' }]}>
            <Text style={[styles.verdictText, { color: verdictColor }]}>
              {getVerdictLabel(verdict)}
            </Text>
          </View>
          <Text style={[styles.sessionScore, { color: verdictColor }]}>{score}</Text>
        </View>
      </TouchableOpacity>
    </Animated.View>
  );
}

function StatsCard({
  sessions,
  index,
}: {
  sessions: SessionData[];
  index: number;
}) {
  const totalSessions = sessions.length;

  const allResults = sessions.flatMap(s => s.results);
  const avgScore =
    allResults.length > 0
      ? Math.round(allResults.reduce((sum, r) => sum + r.overallScore, 0) / allResults.length)
      : 0;

  // Calculate streak: consecutive days with at least one session
  let streak = 0;
  if (sessions.length > 0) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const dayMs = 86400000;
    let checkDate = today.getTime();

    for (let d = 0; d < 365; d++) {
      const hasSession = sessions.some(s => {
        const sDate = new Date(s.startTime);
        sDate.setHours(0, 0, 0, 0);
        return sDate.getTime() === checkDate;
      });
      if (hasSession) {
        streak++;
        checkDate -= dayMs;
      } else {
        break;
      }
    }
  }

  const stats = [
    { label: 'Sessions', value: totalSessions.toString(), icon: 'analytics-outline' as keyof typeof Ionicons.glyphMap, color: colors.accent.primary },
    { label: 'Avg Score', value: avgScore.toString(), icon: 'speedometer-outline' as keyof typeof Ionicons.glyphMap, color: colors.accent.success },
    { label: 'Streak', value: `${streak}d`, icon: 'flame-outline' as keyof typeof Ionicons.glyphMap, color: colors.accent.warning },
  ];

  return (
    <Animated.View
      entering={FadeInDown.delay(100 + index * 80).duration(400)}
      style={styles.statsCard}
    >
      <Text style={styles.sectionTitle}>Your Stats</Text>
      <View style={styles.statsRow}>
        {stats.map((stat) => (
          <View key={stat.label} style={styles.statItem}>
            <View style={[styles.statIconBg, { backgroundColor: stat.color + '15' }]}>
              <Ionicons name={stat.icon} size={20} color={stat.color} />
            </View>
            <Text style={[styles.statValue, { color: stat.color }]}>{stat.value}</Text>
            <Text style={styles.statLabel}>{stat.label}</Text>
          </View>
        ))}
      </View>
    </Animated.View>
  );
}

function EmptySessionsState() {
  return (
    <View style={styles.emptyState}>
      <Ionicons name="pulse-outline" size={40} color={colors.text.tertiary} />
      <Text style={styles.emptyTitle}>No sessions yet</Text>
      <Text style={styles.emptySubtitle}>
        Start a detection to see your history here
      </Text>
    </View>
  );
}

// --- Main Screen ---

export default function HomeScreen({ navigation }: { navigation: any }) {
  const insets = useSafeAreaInsets();
  const [sessions, setSessions] = useState<SessionData[]>([]);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  const loadData = useCallback(async () => {
    const [loadedSessions, loadedProfile] = await Promise.all([
      getSessions(),
      getProfile(),
    ]);
    setSessions(loadedSessions);
    setProfile(loadedProfile);
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // Refresh when screen comes into focus
  useEffect(() => {
    const unsubscribe = navigation.addListener('focus', () => {
      loadData();
    });
    return unsubscribe;
  }, [navigation, loadData]);

  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    await loadData();
    setRefreshing(false);
  }, [loadData]);

  const handleModePress = async (mode: DetectionMode) => {
    const { getIsPremium, canStartSession } = await import('../store');
    const premium = await getIsPremium();

    // Gate premium modes (face, voice, multi) for free users
    if (!premium && (mode === 'face' || mode === 'voice' || mode === 'multi')) {
      Alert.alert(
        'Premium Feature',
        `${mode === 'multi' ? 'Multi-Modal' : mode === 'face' ? 'Face Scan' : 'Voice Analysis'} is available with TruthScope Premium. Free users can use Finger Pulse mode.`,
        [
          { text: 'Upgrade', onPress: () => navigation.navigate('Onboarding') },
          { text: 'Use Finger Pulse', onPress: () => navigation.navigate('Detection', { mode: 'finger' }) },
        ]
      );
      return;
    }

    // Check daily session limit for free users
    const { allowed, remaining } = await canStartSession();
    if (!allowed) {
      Alert.alert(
        'Daily Limit Reached',
        'Free users get 3 sessions per day. Upgrade to Premium for unlimited sessions.',
        [
          { text: 'Upgrade', onPress: () => navigation.navigate('Onboarding') },
          { text: 'OK' },
        ]
      );
      return;
    }

    navigation.navigate('Detection', { mode });
  };

  const handlePartyPress = () => {
    navigation.navigate('PartyMode');
  };

  const handleSettingsPress = () => {
    navigation.navigate('Settings');
  };

  const isPremium = profile?.isPremium ?? false;
  const recentSessions = sessions.slice(0, 5);
  let sectionIndex = 0;

  return (
    <View style={[styles.screen, { paddingTop: insets.top }]}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor={colors.accent.primary}
          />
        }
      >
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.logoContainer}>
            <LogoGlow />
            <Text style={styles.logoText}>TruthScope</Text>
          </View>
          <TouchableOpacity
            onPress={handleSettingsPress}
            hitSlop={{ top: 12, bottom: 12, left: 12, right: 12 }}
            style={styles.settingsButton}
          >
            <Ionicons name="settings-outline" size={24} color={colors.text.secondary} />
          </TouchableOpacity>
        </View>

        {/* Quick Start - 2x2 Grid */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Quick Start</Text>
          <View style={styles.modeGrid}>
            {DETECTION_MODES.map((config, i) => (
              <ModeCard
                key={config.mode}
                config={config}
                isPremium={isPremium}
                index={sectionIndex + i}
                onPress={() => handleModePress(config.mode)}
              />
            ))}
          </View>
        </View>

        {/* Party Mode Banner */}
        <View style={styles.section}>
          <PartyModeBanner
            index={(sectionIndex += 4)}
            onPress={handlePartyPress}
          />
        </View>

        {/* Recent Sessions */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Recent Sessions</Text>
          {recentSessions.length > 0 ? (
            <View style={styles.sessionsList}>
              {recentSessions.map((session, i) => (
                <SessionItem
                  key={session.id}
                  session={session}
                  index={i}
                  onPress={() => {
                    const lastResult = session.results?.[session.results.length - 1];
                    if (lastResult) {
                      navigation.navigate('Result', { result: lastResult });
                    } else {
                      navigation.navigate('Detection', { mode: session.mode });
                    }
                  }}
                />
              ))}
            </View>
          ) : (
            <EmptySessionsState />
          )}
        </View>

        {/* Stats Card */}
        <StatsCard sessions={sessions} index={(sectionIndex += 5)} />

        {/* Bottom spacer */}
        <View style={{ height: insets.bottom + spacing.xxl }} />
      </ScrollView>
    </View>
  );
}

// --- Styles ---

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: colors.bg.primary,
  },
  scrollContent: {
    paddingHorizontal: spacing.lg,
  },

  // Header
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: spacing.md,
    marginBottom: spacing.sm,
  },
  logoContainer: {
    position: 'relative',
  },
  logoText: {
    ...typography.h1,
    color: colors.text.primary,
    letterSpacing: -0.5,
  },
  logoGlow: {
    position: 'absolute',
    top: -12,
    left: -8,
    width: 180,
    height: 50,
    zIndex: -1,
  },
  logoGlowGradient: {
    flex: 1,
    borderRadius: 25,
    opacity: 0.25,
  },
  settingsButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.bg.card,
    alignItems: 'center',
    justifyContent: 'center',
  },

  // Sections
  section: {
    marginBottom: spacing.lg,
  },
  sectionTitle: {
    ...typography.bodyBold,
    color: colors.text.secondary,
    marginBottom: spacing.md,
    textTransform: 'uppercase',
    letterSpacing: 1,
    fontSize: 13,
  },

  // Mode Grid
  modeGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: CARD_GAP,
  },
  modeCard: {
    height: CARD_SIZE * 0.85,
    borderRadius: radii.lg,
    overflow: 'hidden',
  },
  modeCardGradientBorder: {
    flex: 1,
    borderRadius: radii.lg,
    padding: 1.5,
  },
  modeCardInner: {
    flex: 1,
    backgroundColor: colors.bg.card,
    borderRadius: radii.lg - 1,
    padding: spacing.md,
    justifyContent: 'space-between',
  },
  modeCardContent: {
    flex: 1,
    backgroundColor: colors.bg.card,
    borderRadius: radii.lg,
    padding: spacing.md,
    justifyContent: 'space-between',
    borderWidth: 1,
    borderColor: colors.bg.elevated,
  },
  modeIconContainer: {
    width: 48,
    height: 48,
    borderRadius: radii.md,
    alignItems: 'center',
    justifyContent: 'center',
  },
  modeLabel: {
    ...typography.bodyBold,
    color: colors.text.primary,
    marginTop: spacing.sm,
  },
  modeSubtitle: {
    ...typography.small,
    color: colors.text.tertiary,
    marginTop: 2,
  },
  premiumBadge: {
    position: 'absolute',
    top: spacing.sm,
    right: spacing.sm,
  },
  premiumBadgeGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 3,
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: radii.full,
  },
  premiumBadgeText: {
    color: '#FFFFFF',
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 0.5,
  },

  // Party Banner
  partyBanner: {
    borderRadius: radii.lg,
    overflow: 'hidden',
  },
  partyGradient: {
    padding: spacing.lg,
  },
  partyContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  partyTextBlock: {
    flex: 1,
  },
  partyHeaderRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    marginBottom: spacing.xs,
  },
  partyIcon: {
    fontSize: 24,
  },
  partyTitle: {
    ...typography.h2,
    color: '#FFFFFF',
    fontWeight: '800',
  },
  partySubtitle: {
    ...typography.body,
    color: 'rgba(255,255,255,0.85)',
    marginTop: 2,
  },
  partyArrow: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(255,255,255,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
    marginLeft: spacing.md,
  },

  // Sessions
  sessionsList: {
    gap: spacing.sm,
  },
  sessionItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.bg.card,
    borderRadius: radii.md,
    padding: spacing.md,
    gap: spacing.md,
  },
  sessionIcon: {
    width: 40,
    height: 40,
    borderRadius: radii.sm,
    alignItems: 'center',
    justifyContent: 'center',
  },
  sessionInfo: {
    flex: 1,
  },
  sessionMode: {
    ...typography.bodyBold,
    color: colors.text.primary,
    fontSize: 15,
  },
  sessionTime: {
    ...typography.small,
    color: colors.text.tertiary,
    marginTop: 2,
  },
  sessionResult: {
    alignItems: 'flex-end',
    gap: 4,
  },
  verdictBadge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: radii.full,
  },
  verdictText: {
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 0.5,
  },
  sessionScore: {
    fontSize: 20,
    fontWeight: '800',
  },

  // Stats
  statsCard: {
    backgroundColor: colors.bg.card,
    borderRadius: radii.lg,
    padding: spacing.lg,
    marginBottom: spacing.lg,
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  statItem: {
    alignItems: 'center',
    gap: spacing.xs,
  },
  statIconBg: {
    width: 44,
    height: 44,
    borderRadius: 22,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.xs,
  },
  statValue: {
    fontSize: 22,
    fontWeight: '800',
  },
  statLabel: {
    ...typography.small,
    color: colors.text.tertiary,
  },

  // Empty state
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: spacing.xxl,
    gap: spacing.sm,
  },
  emptyTitle: {
    ...typography.bodyBold,
    color: colors.text.secondary,
  },
  emptySubtitle: {
    ...typography.caption,
    color: colors.text.tertiary,
    textAlign: 'center',
  },
});
