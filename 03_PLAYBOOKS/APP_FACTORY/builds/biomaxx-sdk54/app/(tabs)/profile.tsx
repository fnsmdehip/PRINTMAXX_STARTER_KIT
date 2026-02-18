import React, { useMemo } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  Switch,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import * as Haptics from 'expo-haptics';
import { useUserStore } from '../../src/stores/userStore';
import { useSubscriptionStore } from '../../src/stores/subscriptionStore';
import { useProtocolStore } from '../../src/stores/protocolStore';
import { StreakBadge } from '../../src/components';
import { MoreApps } from '../../src/components/MoreApps';
import { COLORS, ACHIEVEMENTS } from '../../src/utils/constants';
import { getDaysSinceDate } from '../../src/utils/dateUtils';

export default function Profile() {
  const user = useUserStore((state) => state.user);
  const subscription = useSubscriptionStore((state) => state);
  const protocolLogs = useProtocolStore((state) => state.logs);

  const isPremium = subscription.canAccessPremiumContent();
  const trialDaysRemaining = subscription.getTrialDaysRemaining();

  const stats = useMemo(() => {
    const uniqueDates = new Set(protocolLogs.map((l) => l.date));
    return {
      totalSessions: protocolLogs.length,
      currentStreak: user?.streakDays || 0,
      daysActive: uniqueDates.size,
      daysSinceJoin: user?.createdAt ? getDaysSinceDate(user.createdAt) : 0,
    };
  }, [protocolLogs, user]);

  const unlockedAchievements = useMemo(() => {
    const unlocked: string[] = [];

    // First log
    if (protocolLogs.length > 0) unlocked.push('first-log');

    // Week streak
    if ((user?.streakDays || 0) >= 7) unlocked.push('week-streak');

    // Month streak
    if ((user?.streakDays || 0) >= 30) unlocked.push('month-streak');

    // Cold sessions (10+)
    const coldSessions = protocolLogs.filter((l) => l.protocolId === 'cold').length;
    if (coldSessions >= 10) unlocked.push('cold-beginner');

    // Fasting sessions (50+)
    const fastingSessions = protocolLogs.filter((l) => l.protocolId === 'fasting').length;
    if (fastingSessions >= 50) unlocked.push('fasting-pro');

    // All protocols tried
    const uniqueProtocols = new Set(protocolLogs.map((l) => l.protocolId));
    if (uniqueProtocols.size >= 6) unlocked.push('all-protocols');

    return unlocked;
  }, [protocolLogs, user?.streakDays]);

  const handleUpgrade = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    router.push('/paywall');
  };

  const handleSetting = (setting: string) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    Alert.alert(setting, `${setting} settings would open here.`);
  };

  const handleExportData = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    Alert.alert(
      'Export Data',
      'Your data would be exported as a JSON file.',
      [{ text: 'OK' }]
    );
  };

  const handleResetApp = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
    Alert.alert(
      'Reset App',
      'This will delete all your data including protocols, streaks, and settings. This cannot be undone.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Reset',
          style: 'destructive',
          onPress: () => {
            useUserStore.getState().reset();
            useSubscriptionStore.getState().reset();
            useProtocolStore.getState().reset();
            Alert.alert('App Reset', 'All data has been cleared.');
          },
        },
      ]
    );
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Profile Header */}
        <View style={styles.header}>
          <View style={styles.avatarContainer}>
            <Text style={styles.avatarText}>
              {(user?.name || 'B').charAt(0).toUpperCase()}
            </Text>
          </View>
          <Text style={styles.name}>{user?.name || 'Biohacker'}</Text>
          <View style={styles.memberBadge}>
            <Ionicons
              name={isPremium ? 'diamond' : 'person'}
              size={14}
              color={isPremium ? COLORS.accent : COLORS.textSecondary}
            />
            <Text
              style={[styles.memberBadgeText, isPremium && styles.premiumText]}
            >
              {subscription.tier === 'premium'
                ? 'Premium Member'
                : subscription.tier === 'trial'
                ? `Trial (${trialDaysRemaining} days left)`
                : 'Free Plan'}
            </Text>
          </View>
        </View>

        {/* Stats */}
        <View style={styles.statsGrid}>
          <View style={styles.statCard}>
            <Text style={styles.statValue}>{stats.totalSessions}</Text>
            <Text style={styles.statLabel}>Sessions</Text>
          </View>
          <View style={styles.statCard}>
            <View style={styles.streakStatContainer}>
              {stats.currentStreak > 0 ? (
                <StreakBadge streak={stats.currentStreak} size="large" />
              ) : (
                <Text style={styles.statValue}>0</Text>
              )}
            </View>
            <Text style={styles.statLabel}>Day Streak</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statValue}>{stats.daysActive}</Text>
            <Text style={styles.statLabel}>Active Days</Text>
          </View>
        </View>

        {/* Achievements */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Achievements</Text>
          <View style={styles.achievementsGrid}>
            {ACHIEVEMENTS.map((achievement) => {
              const isUnlocked = unlockedAchievements.includes(achievement.id);
              return (
                <View
                  key={achievement.id}
                  style={[
                    styles.achievementCard,
                    !isUnlocked && styles.achievementLocked,
                  ]}
                >
                  <View
                    style={[
                      styles.achievementIcon,
                      isUnlocked && styles.achievementIconUnlocked,
                    ]}
                  >
                    <Ionicons
                      name={achievement.icon as any}
                      size={24}
                      color={isUnlocked ? COLORS.accent : COLORS.textMuted}
                    />
                  </View>
                  <Text
                    style={[
                      styles.achievementName,
                      !isUnlocked && styles.achievementTextLocked,
                    ]}
                    numberOfLines={1}
                  >
                    {achievement.name}
                  </Text>
                  <Text
                    style={styles.achievementDesc}
                    numberOfLines={2}
                  >
                    {achievement.description}
                  </Text>
                </View>
              );
            })}
          </View>
        </View>

        {/* Upgrade CTA */}
        {!isPremium && (
          <TouchableOpacity
            style={styles.upgradeCard}
            onPress={handleUpgrade}
            activeOpacity={0.9}
          >
            <View style={styles.upgradeIcon}>
              <Ionicons name="diamond" size={28} color={COLORS.accent} />
            </View>
            <View style={styles.upgradeContent}>
              <Text style={styles.upgradeTitle}>Upgrade to Premium</Text>
              <Text style={styles.upgradeSubtitle}>
                Unlock all protocols, analytics, and content
              </Text>
            </View>
            <Ionicons name="arrow-forward" size={20} color={COLORS.text} />
          </TouchableOpacity>
        )}

        {/* Settings */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Settings</Text>

          <View style={styles.settingsGroup}>
            <TouchableOpacity
              style={styles.settingRow}
              onPress={() => handleSetting('Notifications')}
            >
              <View style={styles.settingLeft}>
                <View style={styles.settingIcon}>
                  <Ionicons name="notifications-outline" size={20} color={COLORS.text} />
                </View>
                <Text style={styles.settingLabel}>Notifications</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color={COLORS.textMuted} />
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.settingRow}
              onPress={() => handleSetting('Units')}
            >
              <View style={styles.settingLeft}>
                <View style={styles.settingIcon}>
                  <Ionicons name="options-outline" size={20} color={COLORS.text} />
                </View>
                <Text style={styles.settingLabel}>Units & Preferences</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color={COLORS.textMuted} />
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.settingRow}
              onPress={handleExportData}
            >
              <View style={styles.settingLeft}>
                <View style={styles.settingIcon}>
                  <Ionicons name="download-outline" size={20} color={COLORS.text} />
                </View>
                <Text style={styles.settingLabel}>Export Data</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color={COLORS.textMuted} />
            </TouchableOpacity>
          </View>

          <View style={styles.settingsGroup}>
            <TouchableOpacity
              style={styles.settingRow}
              onPress={() => handleSetting('About')}
            >
              <View style={styles.settingLeft}>
                <View style={styles.settingIcon}>
                  <Ionicons name="information-circle-outline" size={20} color={COLORS.text} />
                </View>
                <Text style={styles.settingLabel}>About BioMaxx</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color={COLORS.textMuted} />
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.settingRow}
              onPress={() => handleSetting('Privacy Policy')}
            >
              <View style={styles.settingLeft}>
                <View style={styles.settingIcon}>
                  <Ionicons name="shield-outline" size={20} color={COLORS.text} />
                </View>
                <Text style={styles.settingLabel}>Privacy Policy</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color={COLORS.textMuted} />
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.settingRow}
              onPress={() => handleSetting('Terms of Service')}
            >
              <View style={styles.settingLeft}>
                <View style={styles.settingIcon}>
                  <Ionicons name="document-text-outline" size={20} color={COLORS.text} />
                </View>
                <Text style={styles.settingLabel}>Terms of Service</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color={COLORS.textMuted} />
            </TouchableOpacity>
          </View>

          <View style={styles.settingsGroup}>
            <TouchableOpacity
              style={styles.settingRow}
              onPress={handleResetApp}
            >
              <View style={styles.settingLeft}>
                <View style={[styles.settingIcon, styles.dangerIcon]}>
                  <Ionicons name="trash-outline" size={20} color={COLORS.error} />
                </View>
                <Text style={[styles.settingLabel, styles.dangerText]}>
                  Reset App
                </Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color={COLORS.error} />
            </TouchableOpacity>
          </View>
        </View>

        {/* More Apps */}
        <MoreApps />

        {/* Disclaimer */}
        <Text style={styles.disclaimer}>
          BioMaxx is for educational purposes only and does not provide medical
          advice. Always consult with healthcare professionals before starting
          any new health protocol.
        </Text>

        <Text style={styles.version}>Version 1.0.0</Text>
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
    alignItems: 'center',
    marginBottom: 24,
  },
  avatarContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  avatarText: {
    fontSize: 32,
    fontWeight: '700',
    color: COLORS.background,
  },
  name: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 8,
  },
  memberBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    backgroundColor: COLORS.surface,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  memberBadgeText: {
    fontSize: 13,
    color: COLORS.textSecondary,
    fontWeight: '500',
  },
  premiumText: {
    color: COLORS.accent,
  },
  statsGrid: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 24,
  },
  statCard: {
    flex: 1,
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 16,
    alignItems: 'center',
  },
  statValue: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
  },
  statLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  streakStatContainer: {
    height: 40,
    justifyContent: 'center',
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 16,
  },
  achievementsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  achievementCard: {
    width: '31%',
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 12,
    alignItems: 'center',
  },
  achievementLocked: {
    opacity: 0.5,
  },
  achievementIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: COLORS.surfaceLight,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },
  achievementIconUnlocked: {
    backgroundColor: 'rgba(255, 217, 61, 0.2)',
  },
  achievementName: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: 4,
  },
  achievementTextLocked: {
    color: COLORS.textMuted,
  },
  achievementDesc: {
    fontSize: 10,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 14,
  },
  upgradeCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 24,
    borderWidth: 1,
    borderColor: COLORS.accent,
  },
  upgradeIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: 'rgba(255, 217, 61, 0.15)',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  upgradeContent: {
    flex: 1,
  },
  upgradeTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 2,
  },
  upgradeSubtitle: {
    fontSize: 13,
    color: COLORS.textSecondary,
  },
  settingsGroup: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    marginBottom: 16,
    overflow: 'hidden',
  },
  settingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  settingLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  settingIcon: {
    width: 36,
    height: 36,
    borderRadius: 10,
    backgroundColor: COLORS.surfaceLight,
    justifyContent: 'center',
    alignItems: 'center',
  },
  dangerIcon: {
    backgroundColor: 'rgba(239, 68, 68, 0.15)',
  },
  settingLabel: {
    fontSize: 15,
    color: COLORS.text,
  },
  dangerText: {
    color: COLORS.error,
  },
  disclaimer: {
    fontSize: 12,
    color: COLORS.textMuted,
    textAlign: 'center',
    lineHeight: 18,
    marginBottom: 16,
  },
  version: {
    fontSize: 12,
    color: COLORS.textMuted,
    textAlign: 'center',
  },
});
