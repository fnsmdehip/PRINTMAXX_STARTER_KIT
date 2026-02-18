import { View, Text, StyleSheet, ScrollView, Pressable } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, borderRadius, typography, shadows } from '@/constants/theme';
import { useUserStore } from '@/store/userStore';
import { useJournalStore } from '@/store/journalStore';
import { getTodaysVerse, getTodaysDevotional } from '@/constants/devotions';
import { format } from 'date-fns';

export default function HomeScreen() {
  const router = useRouter();
  const {
    profile,
    currentStreak,
    longestStreak,
    totalDevotions,
    totalPrayers,
    recordDevotion,
    isDevotionCompleted,
  } = useUserStore();
  const { getActivePrayers, getPrayerStats } = useJournalStore();

  const todaysVerse = getTodaysVerse();
  const todaysDevotional = getTodaysDevotional();
  const activePrayers = getActivePrayers();
  const prayerStats = getPrayerStats();
  const today = format(new Date(), 'EEEE, MMMM d');
  const isTodayCompleted = isDevotionCompleted(todaysDevotional.id);

  const handleStartDevotion = () => {
    router.push(`/devotion/${todaysDevotional.id}`);
  };

  const handleViewPrayers = () => {
    router.push('/(tabs)/journal');
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
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
            <Text style={styles.greeting}>
              {getGreeting()}{profile.name ? `, ${profile.name}` : ''}
            </Text>
            <Text style={styles.date}>{today}</Text>
          </View>
          <View style={styles.streakBadge}>
            <Ionicons name="flame" size={20} color={colors.warning} />
            <Text style={styles.streakText}>{currentStreak}</Text>
          </View>
        </View>

        {/* Verse of the Day Card */}
        <View style={styles.verseCard}>
          <LinearGradient
            colors={[colors.versePrimary + '15', colors.verseSecondary]}
            style={styles.verseGradient}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
          />
          <View style={styles.verseHeader}>
            <Ionicons name="book-outline" size={20} color={colors.versePrimary} />
            <Text style={styles.verseLabel}>Verse of the Day</Text>
          </View>
          <Text style={styles.verseText}>"{todaysVerse.verse}"</Text>
          <Text style={styles.verseReference}>{todaysVerse.reference}</Text>
        </View>

        {/* Today's Devotional */}
        <View style={styles.devotionalCard}>
          <View style={styles.devotionalHeader}>
            <View style={styles.devotionalInfo}>
              <Text style={styles.devotionalLabel}>Today's Devotional</Text>
              <Text style={styles.devotionalTitle}>{todaysDevotional.title}</Text>
              <Text style={styles.devotionalTheme}>
                Theme: {todaysDevotional.theme.charAt(0).toUpperCase() + todaysDevotional.theme.slice(1)}
              </Text>
            </View>
            {isTodayCompleted && (
              <View style={styles.completedBadge}>
                <Ionicons name="checkmark-circle" size={24} color={colors.success} />
              </View>
            )}
          </View>
          <Pressable
            style={({ pressed }) => [
              styles.devotionalButton,
              pressed && styles.devotionalButtonPressed,
              isTodayCompleted && styles.devotionalButtonCompleted,
            ]}
            onPress={handleStartDevotion}
          >
            <Text style={[
              styles.devotionalButtonText,
              isTodayCompleted && styles.devotionalButtonTextCompleted,
            ]}>
              {isTodayCompleted ? 'Read Again' : 'Begin Devotional'}
            </Text>
            <Ionicons
              name="arrow-forward"
              size={20}
              color={isTodayCompleted ? colors.primary : colors.surface}
            />
          </Pressable>
        </View>

        {/* Stats Row */}
        <View style={styles.statsRow}>
          <View style={styles.statCard}>
            <View style={[styles.statIcon, { backgroundColor: colors.warning + '20' }]}>
              <Ionicons name="flame" size={24} color={colors.warning} />
            </View>
            <Text style={styles.statNumber}>{currentStreak}</Text>
            <Text style={styles.statLabel}>Day streak</Text>
          </View>
          <View style={styles.statCard}>
            <View style={[styles.statIcon, { backgroundColor: colors.primary + '20' }]}>
              <Ionicons name="book" size={24} color={colors.primary} />
            </View>
            <Text style={styles.statNumber}>{totalDevotions}</Text>
            <Text style={styles.statLabel}>Devotions</Text>
          </View>
          <View style={styles.statCard}>
            <View style={[styles.statIcon, { backgroundColor: colors.prayerPrimary + '20' }]}>
              <Ionicons name="heart" size={24} color={colors.prayerPrimary} />
            </View>
            <Text style={styles.statNumber}>{totalPrayers}</Text>
            <Text style={styles.statLabel}>Prayers</Text>
          </View>
        </View>

        {/* Active Prayers Preview */}
        {activePrayers.length > 0 && (
          <View style={styles.prayersSection}>
            <View style={styles.sectionHeader}>
              <Text style={styles.sectionTitle}>Active Prayers</Text>
              <Pressable onPress={handleViewPrayers}>
                <Text style={styles.seeAllText}>See all</Text>
              </Pressable>
            </View>
            {activePrayers.slice(0, 3).map((prayer) => (
              <View key={prayer.id} style={styles.prayerItem}>
                <Ionicons name="heart-outline" size={18} color={colors.prayerPrimary} />
                <Text style={styles.prayerText} numberOfLines={1}>
                  {prayer.title}
                </Text>
              </View>
            ))}
            {prayerStats.answered > 0 && (
              <View style={styles.answeredNote}>
                <Ionicons name="checkmark-circle" size={16} color={colors.success} />
                <Text style={styles.answeredText}>
                  {prayerStats.answered} prayer{prayerStats.answered !== 1 ? 's' : ''} answered
                </Text>
              </View>
            )}
          </View>
        )}

        {/* Encouragement */}
        <View style={styles.encouragementCard}>
          <Ionicons name="sparkles" size={24} color={colors.secondary} />
          <Text style={styles.encouragementText}>
            {currentStreak === 0
              ? "Every journey begins with a single step. Start today."
              : currentStreak === 1
              ? "Great start! Keep the momentum going tomorrow."
              : currentStreak < 7
              ? `${currentStreak} days strong! You're building a beautiful habit.`
              : currentStreak < 30
              ? `${currentStreak} day streak! Your consistency is inspiring.`
              : `${currentStreak} days! Your dedication to faith is remarkable.`}
          </Text>
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
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: spacing.lg,
  },
  greeting: {
    ...typography.h1,
    color: colors.text,
  },
  date: {
    ...typography.body,
    color: colors.textLight,
    marginTop: spacing.xs,
  },
  streakBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.warning + '20',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: borderRadius.full,
    gap: spacing.xs,
  },
  streakText: {
    ...typography.bodyBold,
    color: colors.warning,
  },
  verseCard: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    marginBottom: spacing.lg,
    overflow: 'hidden',
    ...shadows.md,
  },
  verseGradient: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
  },
  verseHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    marginBottom: spacing.md,
  },
  verseLabel: {
    ...typography.caption,
    color: colors.versePrimary,
    fontWeight: '600',
  },
  verseText: {
    ...typography.verse,
    color: colors.text,
    marginBottom: spacing.sm,
  },
  verseReference: {
    ...typography.verseReference,
    color: colors.versePrimary,
  },
  devotionalCard: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    marginBottom: spacing.lg,
    ...shadows.md,
  },
  devotionalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: spacing.md,
  },
  devotionalInfo: {
    flex: 1,
  },
  devotionalLabel: {
    ...typography.caption,
    color: colors.primary,
    fontWeight: '600',
    marginBottom: spacing.xs,
  },
  devotionalTitle: {
    ...typography.h3,
    color: colors.text,
    marginBottom: spacing.xs,
  },
  devotionalTheme: {
    ...typography.caption,
    color: colors.textMuted,
  },
  completedBadge: {
    marginLeft: spacing.sm,
  },
  devotionalButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.primary,
    padding: spacing.md,
    borderRadius: borderRadius.md,
    gap: spacing.sm,
  },
  devotionalButtonPressed: {
    opacity: 0.9,
  },
  devotionalButtonCompleted: {
    backgroundColor: colors.primary + '15',
    borderWidth: 1,
    borderColor: colors.primary,
  },
  devotionalButtonText: {
    ...typography.bodyBold,
    color: colors.surface,
  },
  devotionalButtonTextCompleted: {
    color: colors.primary,
  },
  statsRow: {
    flexDirection: 'row',
    gap: spacing.sm,
    marginBottom: spacing.lg,
  },
  statCard: {
    flex: 1,
    backgroundColor: colors.surface,
    borderRadius: borderRadius.md,
    padding: spacing.md,
    alignItems: 'center',
    ...shadows.sm,
  },
  statIcon: {
    width: 44,
    height: 44,
    borderRadius: 22,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.sm,
  },
  statNumber: {
    ...typography.h2,
    color: colors.text,
  },
  statLabel: {
    ...typography.small,
    color: colors.textMuted,
  },
  prayersSection: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    marginBottom: spacing.lg,
    ...shadows.sm,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  sectionTitle: {
    ...typography.bodyBold,
    color: colors.text,
  },
  seeAllText: {
    ...typography.caption,
    color: colors.primary,
  },
  prayerItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    paddingVertical: spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  prayerText: {
    ...typography.body,
    color: colors.text,
    flex: 1,
  },
  answeredNote: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    marginTop: spacing.md,
    paddingTop: spacing.sm,
  },
  answeredText: {
    ...typography.caption,
    color: colors.success,
  },
  encouragementCard: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    backgroundColor: colors.secondary + '15',
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
  },
  encouragementText: {
    ...typography.body,
    color: colors.text,
    flex: 1,
    lineHeight: 22,
  },
});
