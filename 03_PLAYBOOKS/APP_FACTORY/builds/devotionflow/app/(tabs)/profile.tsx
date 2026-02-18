import { View, Text, StyleSheet, ScrollView, Pressable, Switch, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, borderRadius, typography, shadows } from '@/constants/theme';
import { useUserStore } from '@/store/userStore';
import { useJournalStore } from '@/store/journalStore';
import { format, differenceInDays } from 'date-fns';
import { scheduleDailyReminder, cancelAllReminders, notificationPresets } from '@/lib/notifications';

export default function ProfileScreen() {
  const router = useRouter();
  const {
    profile,
    currentStreak,
    longestStreak,
    totalDevotions,
    totalPrayers,
    savedVerses,
    joinedDate,
    isSubscribed,
    isTrialActive,
    getTrialDaysRemaining,
    setProfile,
  } = useUserStore();
  const { getPrayerStats } = useJournalStore();

  const prayerStats = getPrayerStats();
  const daysOnApp = differenceInDays(new Date(), new Date(joinedDate)) + 1;

  const handleToggleNotifications = async (enabled: boolean) => {
    if (enabled) {
      const time = profile.notificationTime || { hour: 7, minute: 0 };
      await scheduleDailyReminder(time.hour, time.minute);
    } else {
      await cancelAllReminders();
    }
    setProfile({ notificationsEnabled: enabled });
  };

  const handleChangeNotificationTime = () => {
    Alert.alert(
      'Change Reminder Time',
      'Choose when you want to receive your daily devotional reminder',
      [
        ...notificationPresets.map((preset) => ({
          text: preset.label,
          onPress: async () => {
            setProfile({ notificationTime: { hour: preset.hour, minute: preset.minute } });
            if (profile.notificationsEnabled) {
              await scheduleDailyReminder(preset.hour, preset.minute);
            }
          },
        })),
        { text: 'Cancel', style: 'cancel' },
      ]
    );
  };

  const handleManageSubscription = () => {
    router.push('/paywall');
  };

  const handleOpenPrivacy = () => {
    router.push('/privacy');
  };

  const handleOpenTerms = () => {
    router.push('/terms');
  };

  const formatNotificationTime = () => {
    if (!profile.notificationTime) return 'Not set';
    const { hour, minute } = profile.notificationTime;
    const period = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minute.toString().padStart(2, '0')} ${period}`;
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
          <Text style={styles.title}>Profile</Text>
        </View>

        {/* User Card */}
        <View style={styles.userCard}>
          <View style={styles.avatarContainer}>
            <Ionicons name="person" size={32} color={colors.primary} />
          </View>
          <View style={styles.userInfo}>
            <Text style={styles.userName}>{profile.name || 'Fellow Believer'}</Text>
            <Text style={styles.userSubtext}>
              Member for {daysOnApp} day{daysOnApp !== 1 ? 's' : ''}
            </Text>
          </View>
          {isSubscribed ? (
            <View style={styles.premiumBadge}>
              <Ionicons name="star" size={14} color={colors.surface} />
              <Text style={styles.premiumText}>Premium</Text>
            </View>
          ) : isTrialActive() ? (
            <View style={styles.trialBadge}>
              <Text style={styles.trialText}>{getTrialDaysRemaining()} days left</Text>
            </View>
          ) : null}
        </View>

        {/* Stats Grid */}
        <View style={styles.statsGrid}>
          <View style={styles.statItem}>
            <Ionicons name="flame" size={24} color={colors.warning} />
            <Text style={styles.statValue}>{currentStreak}</Text>
            <Text style={styles.statLabel}>Current Streak</Text>
          </View>
          <View style={styles.statItem}>
            <Ionicons name="trophy" size={24} color={colors.secondary} />
            <Text style={styles.statValue}>{longestStreak}</Text>
            <Text style={styles.statLabel}>Longest Streak</Text>
          </View>
          <View style={styles.statItem}>
            <Ionicons name="book" size={24} color={colors.primary} />
            <Text style={styles.statValue}>{totalDevotions}</Text>
            <Text style={styles.statLabel}>Devotions</Text>
          </View>
          <View style={styles.statItem}>
            <Ionicons name="heart" size={24} color={colors.prayerPrimary} />
            <Text style={styles.statValue}>{prayerStats.answered}</Text>
            <Text style={styles.statLabel}>Answered</Text>
          </View>
        </View>

        {/* Notifications Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Notifications</Text>
          <View style={styles.settingCard}>
            <View style={styles.settingRow}>
              <View style={styles.settingInfo}>
                <Ionicons name="notifications" size={22} color={colors.primary} />
                <Text style={styles.settingText}>Daily Reminders</Text>
              </View>
              <Switch
                value={profile.notificationsEnabled}
                onValueChange={handleToggleNotifications}
                trackColor={{ false: colors.border, true: colors.primary + '60' }}
                thumbColor={profile.notificationsEnabled ? colors.primary : colors.textMuted}
              />
            </View>
            {profile.notificationsEnabled && (
              <Pressable
                style={styles.timeSettingRow}
                onPress={handleChangeNotificationTime}
              >
                <View style={styles.settingInfo}>
                  <Ionicons name="time" size={22} color={colors.textMuted} />
                  <Text style={styles.settingText}>Reminder Time</Text>
                </View>
                <View style={styles.timeValue}>
                  <Text style={styles.timeValueText}>{formatNotificationTime()}</Text>
                  <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
                </View>
              </Pressable>
            )}
          </View>
        </View>

        {/* Subscription Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Subscription</Text>
          <Pressable style={styles.settingCard} onPress={handleManageSubscription}>
            <View style={styles.settingRow}>
              <View style={styles.settingInfo}>
                <Ionicons name="card" size={22} color={colors.primary} />
                <View>
                  <Text style={styles.settingText}>
                    {isSubscribed ? 'Premium Subscription' : 'Upgrade to Premium'}
                  </Text>
                  <Text style={styles.settingSubtext}>
                    {isSubscribed
                      ? 'Manage your subscription'
                      : 'Unlock all features'}
                  </Text>
                </View>
              </View>
              <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
            </View>
          </Pressable>
        </View>

        {/* About Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>About</Text>
          <View style={styles.settingCard}>
            <Pressable style={styles.settingRow} onPress={handleOpenPrivacy}>
              <View style={styles.settingInfo}>
                <Ionicons name="shield-checkmark" size={22} color={colors.textMuted} />
                <Text style={styles.settingText}>Privacy Policy</Text>
              </View>
              <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
            </Pressable>
            <View style={styles.divider} />
            <Pressable style={styles.settingRow} onPress={handleOpenTerms}>
              <View style={styles.settingInfo}>
                <Ionicons name="document-text" size={22} color={colors.textMuted} />
                <Text style={styles.settingText}>Terms of Service</Text>
              </View>
              <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
            </Pressable>
            <View style={styles.divider} />
            <View style={styles.settingRow}>
              <View style={styles.settingInfo}>
                <Ionicons name="information-circle" size={22} color={colors.textMuted} />
                <Text style={styles.settingText}>Version</Text>
              </View>
              <Text style={styles.versionText}>1.0.0</Text>
            </View>
          </View>
        </View>

        {/* Footer */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>Made with faith and love</Text>
          <Ionicons name="heart" size={16} color={colors.primary} />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: spacing.lg,
    paddingBottom: spacing.xxl,
  },
  header: {
    marginBottom: spacing.lg,
  },
  title: {
    ...typography.h1,
    color: colors.text,
  },
  userCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    marginBottom: spacing.lg,
    ...shadows.md,
  },
  avatarContainer: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: colors.primary + '15',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: spacing.md,
  },
  userInfo: {
    flex: 1,
  },
  userName: {
    ...typography.h3,
    color: colors.text,
  },
  userSubtext: {
    ...typography.caption,
    color: colors.textMuted,
  },
  premiumBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.secondary,
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: borderRadius.full,
    gap: spacing.xs,
  },
  premiumText: {
    ...typography.small,
    color: colors.surface,
    fontWeight: '600',
  },
  trialBadge: {
    backgroundColor: colors.primary + '15',
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: borderRadius.full,
  },
  trialText: {
    ...typography.small,
    color: colors.primary,
    fontWeight: '600',
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
    marginBottom: spacing.lg,
  },
  statItem: {
    width: '48%',
    backgroundColor: colors.surface,
    borderRadius: borderRadius.md,
    padding: spacing.lg,
    alignItems: 'center',
    ...shadows.sm,
  },
  statValue: {
    ...typography.h2,
    color: colors.text,
    marginTop: spacing.sm,
  },
  statLabel: {
    ...typography.small,
    color: colors.textMuted,
    marginTop: spacing.xs,
  },
  section: {
    marginBottom: spacing.lg,
  },
  sectionTitle: {
    ...typography.bodyBold,
    color: colors.textMuted,
    marginBottom: spacing.sm,
    marginLeft: spacing.xs,
  },
  settingCard: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    overflow: 'hidden',
    ...shadows.sm,
  },
  settingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: spacing.lg,
  },
  timeSettingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: spacing.lg,
    paddingTop: 0,
  },
  settingInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    flex: 1,
  },
  settingText: {
    ...typography.body,
    color: colors.text,
  },
  settingSubtext: {
    ...typography.caption,
    color: colors.textMuted,
  },
  timeValue: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
  },
  timeValueText: {
    ...typography.body,
    color: colors.primary,
  },
  divider: {
    height: 1,
    backgroundColor: colors.border,
    marginHorizontal: spacing.lg,
  },
  versionText: {
    ...typography.body,
    color: colors.textMuted,
  },
  footer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.xs,
    paddingTop: spacing.lg,
  },
  footerText: {
    ...typography.caption,
    color: colors.textMuted,
  },
});
