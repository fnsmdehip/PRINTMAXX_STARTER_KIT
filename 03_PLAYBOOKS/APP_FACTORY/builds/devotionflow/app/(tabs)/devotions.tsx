import { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, Pressable } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, borderRadius, typography, shadows } from '@/constants/theme';
import { useUserStore } from '@/store/userStore';
import { devotionals, dailyVerses, devotionalThemes, getTodaysDevotional } from '@/constants/devotions';

type FilterType = 'all' | string;

export default function DevotionsScreen() {
  const router = useRouter();
  const { isDevotionCompleted, savedVerses, isVerseSaved, saveVerse, unsaveVerse } = useUserStore();
  const [activeFilter, setActiveFilter] = useState<FilterType>('all');
  const [activeTab, setActiveTab] = useState<'devotions' | 'verses'>('devotions');

  const todaysDevotional = getTodaysDevotional();

  const filteredDevotionals = activeFilter === 'all'
    ? devotionals
    : devotionals.filter(d => d.theme === activeFilter);

  const handleDevotionPress = (id: string) => {
    router.push(`/devotion/${id}`);
  };

  const handleVerseToggle = (verseId: string) => {
    if (isVerseSaved(verseId)) {
      unsaveVerse(verseId);
    } else {
      saveVerse(verseId);
    }
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Devotions</Text>
        <Text style={styles.subtitle}>Scripture and reflection for your journey</Text>
      </View>

      {/* Tab Selector */}
      <View style={styles.tabContainer}>
        <Pressable
          style={[styles.tab, activeTab === 'devotions' && styles.tabActive]}
          onPress={() => setActiveTab('devotions')}
        >
          <Ionicons
            name="book"
            size={18}
            color={activeTab === 'devotions' ? colors.primary : colors.textMuted}
          />
          <Text style={[styles.tabText, activeTab === 'devotions' && styles.tabTextActive]}>
            Devotionals
          </Text>
        </Pressable>
        <Pressable
          style={[styles.tab, activeTab === 'verses' && styles.tabActive]}
          onPress={() => setActiveTab('verses')}
        >
          <Ionicons
            name="bookmark"
            size={18}
            color={activeTab === 'verses' ? colors.primary : colors.textMuted}
          />
          <Text style={[styles.tabText, activeTab === 'verses' && styles.tabTextActive]}>
            Verses
          </Text>
        </Pressable>
      </View>

      {activeTab === 'devotions' ? (
        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.content}
          showsVerticalScrollIndicator={false}
        >
          {/* Theme Filters */}
          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            style={styles.filterScroll}
            contentContainerStyle={styles.filters}
          >
            <Pressable
              style={[styles.filterChip, activeFilter === 'all' && styles.filterChipActive]}
              onPress={() => setActiveFilter('all')}
            >
              <Text style={[styles.filterText, activeFilter === 'all' && styles.filterTextActive]}>
                All
              </Text>
            </Pressable>
            {devotionalThemes.map((theme) => (
              <Pressable
                key={theme.id}
                style={[styles.filterChip, activeFilter === theme.id && styles.filterChipActive]}
                onPress={() => setActiveFilter(theme.id)}
              >
                <Ionicons
                  name={theme.icon as any}
                  size={14}
                  color={activeFilter === theme.id ? colors.surface : colors.textMuted}
                />
                <Text style={[styles.filterText, activeFilter === theme.id && styles.filterTextActive]}>
                  {theme.label}
                </Text>
              </Pressable>
            ))}
          </ScrollView>

          {/* Today's Devotional Highlight */}
          <Pressable
            style={styles.todayCard}
            onPress={() => handleDevotionPress(todaysDevotional.id)}
          >
            <View style={styles.todayBadge}>
              <Text style={styles.todayBadgeText}>TODAY</Text>
            </View>
            <Text style={styles.todayTitle}>{todaysDevotional.title}</Text>
            <Text style={styles.todayVerse} numberOfLines={2}>
              "{todaysDevotional.verse}"
            </Text>
            <Text style={styles.todayReference}>{todaysDevotional.verseReference}</Text>
            {isDevotionCompleted(todaysDevotional.id) && (
              <View style={styles.completedTag}>
                <Ionicons name="checkmark-circle" size={16} color={colors.success} />
                <Text style={styles.completedTagText}>Completed</Text>
              </View>
            )}
          </Pressable>

          {/* Devotional List */}
          <View style={styles.devotionalList}>
            {filteredDevotionals.filter(d => d.id !== todaysDevotional.id).map((devotion) => (
              <Pressable
                key={devotion.id}
                style={({ pressed }) => [
                  styles.devotionalCard,
                  pressed && styles.devotionalCardPressed,
                ]}
                onPress={() => handleDevotionPress(devotion.id)}
              >
                <View style={styles.devotionalContent}>
                  <Text style={styles.devotionalTitle}>{devotion.title}</Text>
                  <Text style={styles.devotionalExcerpt} numberOfLines={2}>
                    {devotion.content.substring(0, 100)}...
                  </Text>
                  <View style={styles.devotionalMeta}>
                    <View style={styles.themeTag}>
                      <Text style={styles.themeTagText}>
                        {devotion.theme.charAt(0).toUpperCase() + devotion.theme.slice(1)}
                      </Text>
                    </View>
                    <Text style={styles.verseRef}>{devotion.verseReference}</Text>
                  </View>
                </View>
                {isDevotionCompleted(devotion.id) && (
                  <Ionicons name="checkmark-circle" size={24} color={colors.success} />
                )}
              </Pressable>
            ))}
          </View>
        </ScrollView>
      ) : (
        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.content}
          showsVerticalScrollIndicator={false}
        >
          {/* Saved Verses Section */}
          {savedVerses.length > 0 && (
            <View style={styles.savedSection}>
              <Text style={styles.sectionTitle}>Saved Verses</Text>
              {dailyVerses
                .filter((v) => savedVerses.includes(v.id))
                .map((verse) => (
                  <View key={verse.id} style={styles.verseCard}>
                    <Pressable
                      style={styles.saveButton}
                      onPress={() => handleVerseToggle(verse.id)}
                    >
                      <Ionicons name="bookmark" size={20} color={colors.primary} />
                    </Pressable>
                    <Text style={styles.verseCardText}>"{verse.verse}"</Text>
                    <Text style={styles.verseCardRef}>{verse.reference}</Text>
                  </View>
                ))}
            </View>
          )}

          {/* All Verses */}
          <View style={styles.allVersesSection}>
            <Text style={styles.sectionTitle}>All Verses</Text>
            {dailyVerses.map((verse) => (
              <View key={verse.id} style={styles.verseCard}>
                <Pressable
                  style={styles.saveButton}
                  onPress={() => handleVerseToggle(verse.id)}
                >
                  <Ionicons
                    name={isVerseSaved(verse.id) ? 'bookmark' : 'bookmark-outline'}
                    size={20}
                    color={isVerseSaved(verse.id) ? colors.primary : colors.textMuted}
                  />
                </Pressable>
                <Text style={styles.verseCardText}>"{verse.verse}"</Text>
                <Text style={styles.verseCardRef}>{verse.reference}</Text>
                <View style={styles.verseThemeTag}>
                  <Text style={styles.verseThemeText}>
                    {verse.theme.charAt(0).toUpperCase() + verse.theme.slice(1)}
                  </Text>
                </View>
              </View>
            ))}
          </View>
        </ScrollView>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    padding: spacing.lg,
    paddingBottom: spacing.md,
  },
  title: {
    ...typography.h1,
    color: colors.text,
  },
  subtitle: {
    ...typography.body,
    color: colors.textLight,
    marginTop: spacing.xs,
  },
  tabContainer: {
    flexDirection: 'row',
    marginHorizontal: spacing.lg,
    backgroundColor: colors.border,
    borderRadius: borderRadius.md,
    padding: 4,
    marginBottom: spacing.md,
  },
  tab: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: spacing.sm,
    borderRadius: borderRadius.sm,
    gap: spacing.xs,
  },
  tabActive: {
    backgroundColor: colors.surface,
    ...shadows.sm,
  },
  tabText: {
    ...typography.caption,
    color: colors.textMuted,
    fontWeight: '600',
  },
  tabTextActive: {
    color: colors.primary,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.xxl,
  },
  filterScroll: {
    marginBottom: spacing.lg,
    marginHorizontal: -spacing.lg,
  },
  filters: {
    paddingHorizontal: spacing.lg,
    gap: spacing.sm,
    flexDirection: 'row',
  },
  filterChip: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: borderRadius.full,
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
    gap: spacing.xs,
  },
  filterChipActive: {
    backgroundColor: colors.primary,
    borderColor: colors.primary,
  },
  filterText: {
    ...typography.caption,
    color: colors.textMuted,
  },
  filterTextActive: {
    color: colors.surface,
  },
  todayCard: {
    backgroundColor: colors.primary + '10',
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    marginBottom: spacing.lg,
    borderWidth: 1,
    borderColor: colors.primary + '30',
  },
  todayBadge: {
    alignSelf: 'flex-start',
    backgroundColor: colors.primary,
    paddingHorizontal: spacing.sm,
    paddingVertical: 2,
    borderRadius: borderRadius.sm,
    marginBottom: spacing.sm,
  },
  todayBadgeText: {
    ...typography.small,
    color: colors.surface,
    fontWeight: '700',
  },
  todayTitle: {
    ...typography.h2,
    color: colors.text,
    marginBottom: spacing.sm,
  },
  todayVerse: {
    ...typography.body,
    color: colors.textLight,
    fontStyle: 'italic',
    marginBottom: spacing.xs,
  },
  todayReference: {
    ...typography.caption,
    color: colors.primary,
    fontWeight: '600',
  },
  completedTag: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    marginTop: spacing.md,
  },
  completedTagText: {
    ...typography.caption,
    color: colors.success,
  },
  devotionalList: {
    gap: spacing.md,
  },
  devotionalCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderRadius: borderRadius.md,
    padding: spacing.lg,
    ...shadows.sm,
  },
  devotionalCardPressed: {
    opacity: 0.9,
  },
  devotionalContent: {
    flex: 1,
  },
  devotionalTitle: {
    ...typography.bodyBold,
    color: colors.text,
    marginBottom: spacing.xs,
  },
  devotionalExcerpt: {
    ...typography.caption,
    color: colors.textMuted,
    marginBottom: spacing.sm,
  },
  devotionalMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  themeTag: {
    backgroundColor: colors.primary + '15',
    paddingHorizontal: spacing.sm,
    paddingVertical: 2,
    borderRadius: borderRadius.sm,
  },
  themeTagText: {
    ...typography.small,
    color: colors.primary,
  },
  verseRef: {
    ...typography.small,
    color: colors.textMuted,
  },
  savedSection: {
    marginBottom: spacing.xl,
  },
  sectionTitle: {
    ...typography.h3,
    color: colors.text,
    marginBottom: spacing.md,
  },
  allVersesSection: {
    marginBottom: spacing.xl,
  },
  verseCard: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.md,
    padding: spacing.lg,
    marginBottom: spacing.md,
    ...shadows.sm,
  },
  saveButton: {
    position: 'absolute',
    top: spacing.md,
    right: spacing.md,
    padding: spacing.xs,
  },
  verseCardText: {
    ...typography.verse,
    color: colors.text,
    marginBottom: spacing.sm,
    paddingRight: spacing.xl,
  },
  verseCardRef: {
    ...typography.verseReference,
    color: colors.versePrimary,
    marginBottom: spacing.sm,
  },
  verseThemeTag: {
    alignSelf: 'flex-start',
    backgroundColor: colors.versePrimary + '15',
    paddingHorizontal: spacing.sm,
    paddingVertical: 2,
    borderRadius: borderRadius.sm,
  },
  verseThemeText: {
    ...typography.small,
    color: colors.versePrimary,
  },
});
