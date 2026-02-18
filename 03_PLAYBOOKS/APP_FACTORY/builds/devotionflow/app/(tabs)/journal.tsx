import { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Pressable,
  TextInput,
  Alert,
  Modal,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { colors, spacing, borderRadius, typography, shadows } from '@/constants/theme';
import { useJournalStore, prayerCategories, PrayerEntry } from '@/store/journalStore';
import { useUserStore } from '@/store/userStore';
import { format } from 'date-fns';

type TabType = 'prayers' | 'journal';
type FilterType = 'active' | 'answered' | 'all';

export default function JournalScreen() {
  const [activeTab, setActiveTab] = useState<TabType>('prayers');
  const [prayerFilter, setPrayerFilter] = useState<FilterType>('active');
  const [showAddModal, setShowAddModal] = useState(false);
  const [newPrayerTitle, setNewPrayerTitle] = useState('');
  const [newPrayerContent, setNewPrayerContent] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | undefined>();

  const {
    prayers,
    journalEntries,
    addPrayer,
    deletePrayer,
    markPrayerAnswered,
    archivePrayer,
    togglePrayerFavorite,
    getPrayerStats,
    getActivePrayers,
    getAnsweredPrayers,
  } = useJournalStore();
  const { recordPrayer } = useUserStore();

  const prayerStats = getPrayerStats();

  const getFilteredPrayers = (): PrayerEntry[] => {
    switch (prayerFilter) {
      case 'active':
        return getActivePrayers();
      case 'answered':
        return getAnsweredPrayers();
      default:
        return prayers;
    }
  };

  const handleAddPrayer = () => {
    if (!newPrayerTitle.trim()) {
      Alert.alert('Please enter a prayer title');
      return;
    }

    addPrayer(newPrayerTitle.trim(), newPrayerContent.trim(), selectedCategory);
    recordPrayer();
    setNewPrayerTitle('');
    setNewPrayerContent('');
    setSelectedCategory(undefined);
    setShowAddModal(false);
  };

  const handleMarkAnswered = (id: string) => {
    Alert.alert(
      'Mark as Answered',
      'Has this prayer been answered?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Yes, Answered!',
          onPress: () => markPrayerAnswered(id),
        },
      ]
    );
  };

  const handleDeletePrayer = (id: string) => {
    Alert.alert(
      'Delete Prayer',
      'Are you sure you want to delete this prayer?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: () => deletePrayer(id),
        },
      ]
    );
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Journal</Text>
        <Pressable
          style={styles.addButton}
          onPress={() => setShowAddModal(true)}
        >
          <Ionicons name="add" size={24} color={colors.surface} />
        </Pressable>
      </View>

      {/* Tab Selector */}
      <View style={styles.tabContainer}>
        <Pressable
          style={[styles.tab, activeTab === 'prayers' && styles.tabActive]}
          onPress={() => setActiveTab('prayers')}
        >
          <Ionicons
            name="heart"
            size={18}
            color={activeTab === 'prayers' ? colors.primary : colors.textMuted}
          />
          <Text style={[styles.tabText, activeTab === 'prayers' && styles.tabTextActive]}>
            Prayers ({prayerStats.total})
          </Text>
        </Pressable>
        <Pressable
          style={[styles.tab, activeTab === 'journal' && styles.tabActive]}
          onPress={() => setActiveTab('journal')}
        >
          <Ionicons
            name="document-text"
            size={18}
            color={activeTab === 'journal' ? colors.primary : colors.textMuted}
          />
          <Text style={[styles.tabText, activeTab === 'journal' && styles.tabTextActive]}>
            Reflections ({journalEntries.length})
          </Text>
        </Pressable>
      </View>

      {activeTab === 'prayers' ? (
        <>
          {/* Prayer Stats */}
          <View style={styles.statsRow}>
            <Pressable
              style={[styles.statChip, prayerFilter === 'active' && styles.statChipActive]}
              onPress={() => setPrayerFilter('active')}
            >
              <Text style={[styles.statChipText, prayerFilter === 'active' && styles.statChipTextActive]}>
                Active ({prayerStats.active})
              </Text>
            </Pressable>
            <Pressable
              style={[styles.statChip, prayerFilter === 'answered' && styles.statChipActive]}
              onPress={() => setPrayerFilter('answered')}
            >
              <Ionicons
                name="checkmark-circle"
                size={14}
                color={prayerFilter === 'answered' ? colors.surface : colors.success}
              />
              <Text style={[styles.statChipText, prayerFilter === 'answered' && styles.statChipTextActive]}>
                Answered ({prayerStats.answered})
              </Text>
            </Pressable>
            <Pressable
              style={[styles.statChip, prayerFilter === 'all' && styles.statChipActive]}
              onPress={() => setPrayerFilter('all')}
            >
              <Text style={[styles.statChipText, prayerFilter === 'all' && styles.statChipTextActive]}>
                All
              </Text>
            </Pressable>
          </View>

          <ScrollView
            style={styles.scrollView}
            contentContainerStyle={styles.content}
            showsVerticalScrollIndicator={false}
          >
            {getFilteredPrayers().length === 0 ? (
              <View style={styles.emptyState}>
                <Ionicons name="heart-outline" size={64} color={colors.border} />
                <Text style={styles.emptyTitle}>
                  {prayerFilter === 'answered' ? 'No answered prayers yet' : 'No prayers yet'}
                </Text>
                <Text style={styles.emptyText}>
                  {prayerFilter === 'answered'
                    ? 'When prayers are answered, they will appear here.'
                    : 'Start recording your prayers to track your spiritual journey.'}
                </Text>
                {prayerFilter !== 'answered' && (
                  <Pressable
                    style={styles.emptyButton}
                    onPress={() => setShowAddModal(true)}
                  >
                    <Text style={styles.emptyButtonText}>Add First Prayer</Text>
                  </Pressable>
                )}
              </View>
            ) : (
              getFilteredPrayers().map((prayer) => (
                <View key={prayer.id} style={styles.prayerCard}>
                  <View style={styles.prayerHeader}>
                    <Pressable
                      onPress={() => togglePrayerFavorite(prayer.id)}
                      style={styles.favoriteButton}
                    >
                      <Ionicons
                        name={prayer.isFavorite ? 'heart' : 'heart-outline'}
                        size={20}
                        color={prayer.isFavorite ? colors.error : colors.textMuted}
                      />
                    </Pressable>
                    <View style={styles.prayerTitleRow}>
                      <Text style={styles.prayerTitle}>{prayer.title}</Text>
                      {prayer.status === 'answered' && (
                        <View style={styles.answeredBadge}>
                          <Ionicons name="checkmark" size={12} color={colors.surface} />
                        </View>
                      )}
                    </View>
                  </View>
                  {prayer.content && (
                    <Text style={styles.prayerContent} numberOfLines={3}>
                      {prayer.content}
                    </Text>
                  )}
                  <View style={styles.prayerFooter}>
                    <Text style={styles.prayerDate}>
                      {format(new Date(prayer.createdAt), 'MMM d, yyyy')}
                    </Text>
                    {prayer.category && (
                      <View style={styles.categoryTag}>
                        <Text style={styles.categoryTagText}>{prayer.category}</Text>
                      </View>
                    )}
                  </View>
                  <View style={styles.prayerActions}>
                    {prayer.status === 'active' && (
                      <Pressable
                        style={styles.actionButton}
                        onPress={() => handleMarkAnswered(prayer.id)}
                      >
                        <Ionicons name="checkmark-circle-outline" size={18} color={colors.success} />
                        <Text style={[styles.actionText, { color: colors.success }]}>Answered</Text>
                      </Pressable>
                    )}
                    <Pressable
                      style={styles.actionButton}
                      onPress={() => handleDeletePrayer(prayer.id)}
                    >
                      <Ionicons name="trash-outline" size={18} color={colors.error} />
                      <Text style={[styles.actionText, { color: colors.error }]}>Delete</Text>
                    </Pressable>
                  </View>
                </View>
              ))
            )}
          </ScrollView>
        </>
      ) : (
        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.content}
          showsVerticalScrollIndicator={false}
        >
          {journalEntries.length === 0 ? (
            <View style={styles.emptyState}>
              <Ionicons name="document-text-outline" size={64} color={colors.border} />
              <Text style={styles.emptyTitle}>No journal entries yet</Text>
              <Text style={styles.emptyText}>
                Complete a devotional to add reflections to your journal.
              </Text>
            </View>
          ) : (
            journalEntries.map((entry) => (
              <View key={entry.id} style={styles.journalCard}>
                <Text style={styles.journalDate}>
                  {format(new Date(entry.createdAt), 'EEEE, MMMM d, yyyy')}
                </Text>
                {entry.verse && (
                  <View style={styles.journalVerse}>
                    <Text style={styles.journalVerseText}>"{entry.verse}"</Text>
                    {entry.verseReference && (
                      <Text style={styles.journalVerseRef}>{entry.verseReference}</Text>
                    )}
                  </View>
                )}
                <Text style={styles.journalContent}>{entry.content}</Text>
                {entry.reflections.length > 0 && (
                  <View style={styles.reflections}>
                    <Text style={styles.reflectionsLabel}>Reflections:</Text>
                    {entry.reflections.map((reflection, index) => (
                      <Text key={index} style={styles.reflectionItem}>
                        {reflection}
                      </Text>
                    ))}
                  </View>
                )}
              </View>
            ))
          )}
        </ScrollView>
      )}

      {/* Add Prayer Modal */}
      <Modal
        visible={showAddModal}
        animationType="slide"
        presentationStyle="pageSheet"
      >
        <SafeAreaView style={styles.modalContainer}>
          <View style={styles.modalHeader}>
            <Pressable onPress={() => setShowAddModal(false)}>
              <Text style={styles.modalCancel}>Cancel</Text>
            </Pressable>
            <Text style={styles.modalTitle}>New Prayer</Text>
            <Pressable onPress={handleAddPrayer}>
              <Text style={styles.modalSave}>Save</Text>
            </Pressable>
          </View>

          <ScrollView style={styles.modalContent}>
            <Text style={styles.inputLabel}>Prayer Title</Text>
            <TextInput
              style={styles.titleInput}
              placeholder="What are you praying for?"
              placeholderTextColor={colors.textMuted}
              value={newPrayerTitle}
              onChangeText={setNewPrayerTitle}
            />

            <Text style={styles.inputLabel}>Details (optional)</Text>
            <TextInput
              style={styles.contentInput}
              placeholder="Add more details about your prayer..."
              placeholderTextColor={colors.textMuted}
              value={newPrayerContent}
              onChangeText={setNewPrayerContent}
              multiline
              numberOfLines={4}
              textAlignVertical="top"
            />

            <Text style={styles.inputLabel}>Category (optional)</Text>
            <View style={styles.categoryGrid}>
              {prayerCategories.map((cat) => (
                <Pressable
                  key={cat.id}
                  style={[
                    styles.categoryChip,
                    selectedCategory === cat.id && styles.categoryChipActive,
                  ]}
                  onPress={() =>
                    setSelectedCategory(selectedCategory === cat.id ? undefined : cat.id)
                  }
                >
                  <Ionicons
                    name={cat.icon as any}
                    size={16}
                    color={selectedCategory === cat.id ? colors.surface : colors.textMuted}
                  />
                  <Text
                    style={[
                      styles.categoryChipText,
                      selectedCategory === cat.id && styles.categoryChipTextActive,
                    ]}
                  >
                    {cat.label}
                  </Text>
                </Pressable>
              ))}
            </View>
          </ScrollView>
        </SafeAreaView>
      </Modal>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: spacing.lg,
    paddingBottom: spacing.md,
  },
  title: {
    ...typography.h1,
    color: colors.text,
  },
  addButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    ...shadows.md,
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
  statsRow: {
    flexDirection: 'row',
    paddingHorizontal: spacing.lg,
    gap: spacing.sm,
    marginBottom: spacing.md,
  },
  statChip: {
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
  statChipActive: {
    backgroundColor: colors.primary,
    borderColor: colors.primary,
  },
  statChipText: {
    ...typography.caption,
    color: colors.textMuted,
  },
  statChipTextActive: {
    color: colors.surface,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: spacing.lg,
    paddingBottom: spacing.xxl,
  },
  emptyState: {
    alignItems: 'center',
    paddingTop: spacing.xxl,
  },
  emptyTitle: {
    ...typography.h3,
    color: colors.text,
    marginTop: spacing.lg,
    marginBottom: spacing.sm,
  },
  emptyText: {
    ...typography.body,
    color: colors.textMuted,
    textAlign: 'center',
    paddingHorizontal: spacing.xl,
  },
  emptyButton: {
    marginTop: spacing.lg,
    backgroundColor: colors.primary,
    paddingHorizontal: spacing.xl,
    paddingVertical: spacing.md,
    borderRadius: borderRadius.md,
  },
  emptyButtonText: {
    ...typography.bodyBold,
    color: colors.surface,
  },
  prayerCard: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    marginBottom: spacing.md,
    ...shadows.sm,
  },
  prayerHeader: {
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  favoriteButton: {
    marginRight: spacing.sm,
    paddingTop: 2,
  },
  prayerTitleRow: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  prayerTitle: {
    ...typography.bodyBold,
    color: colors.text,
    flex: 1,
  },
  answeredBadge: {
    width: 20,
    height: 20,
    borderRadius: 10,
    backgroundColor: colors.success,
    alignItems: 'center',
    justifyContent: 'center',
  },
  prayerContent: {
    ...typography.body,
    color: colors.textLight,
    marginTop: spacing.sm,
    marginLeft: 28,
  },
  prayerFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: spacing.md,
    marginLeft: 28,
    gap: spacing.sm,
  },
  prayerDate: {
    ...typography.small,
    color: colors.textMuted,
  },
  categoryTag: {
    backgroundColor: colors.prayerPrimary + '15',
    paddingHorizontal: spacing.sm,
    paddingVertical: 2,
    borderRadius: borderRadius.sm,
  },
  categoryTagText: {
    ...typography.small,
    color: colors.prayerPrimary,
  },
  prayerActions: {
    flexDirection: 'row',
    marginTop: spacing.md,
    paddingTop: spacing.md,
    borderTopWidth: 1,
    borderTopColor: colors.border,
    gap: spacing.lg,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
  },
  actionText: {
    ...typography.caption,
  },
  journalCard: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    marginBottom: spacing.md,
    ...shadows.sm,
  },
  journalDate: {
    ...typography.caption,
    color: colors.primary,
    fontWeight: '600',
    marginBottom: spacing.sm,
  },
  journalVerse: {
    backgroundColor: colors.versePrimary + '10',
    padding: spacing.md,
    borderRadius: borderRadius.md,
    marginBottom: spacing.md,
  },
  journalVerseText: {
    ...typography.verse,
    color: colors.text,
    fontSize: 14,
  },
  journalVerseRef: {
    ...typography.small,
    color: colors.versePrimary,
    marginTop: spacing.xs,
  },
  journalContent: {
    ...typography.body,
    color: colors.text,
  },
  reflections: {
    marginTop: spacing.md,
    paddingTop: spacing.md,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  reflectionsLabel: {
    ...typography.caption,
    color: colors.textMuted,
    marginBottom: spacing.sm,
  },
  reflectionItem: {
    ...typography.body,
    color: colors.textLight,
    marginBottom: spacing.xs,
    paddingLeft: spacing.md,
  },
  modalContainer: {
    flex: 1,
    backgroundColor: colors.background,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: spacing.lg,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  modalCancel: {
    ...typography.body,
    color: colors.textMuted,
  },
  modalTitle: {
    ...typography.bodyBold,
    color: colors.text,
  },
  modalSave: {
    ...typography.bodyBold,
    color: colors.primary,
  },
  modalContent: {
    padding: spacing.lg,
  },
  inputLabel: {
    ...typography.caption,
    color: colors.textMuted,
    marginBottom: spacing.sm,
    marginTop: spacing.md,
  },
  titleInput: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.md,
    padding: spacing.md,
    ...typography.body,
    color: colors.text,
    borderWidth: 1,
    borderColor: colors.border,
  },
  contentInput: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.md,
    padding: spacing.md,
    ...typography.body,
    color: colors.text,
    borderWidth: 1,
    borderColor: colors.border,
    minHeight: 120,
  },
  categoryGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
  },
  categoryChip: {
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
  categoryChipActive: {
    backgroundColor: colors.prayerPrimary,
    borderColor: colors.prayerPrimary,
  },
  categoryChipText: {
    ...typography.caption,
    color: colors.textMuted,
  },
  categoryChipTextActive: {
    color: colors.surface,
  },
});
