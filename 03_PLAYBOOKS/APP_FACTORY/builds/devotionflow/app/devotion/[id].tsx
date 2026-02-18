import { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Pressable,
  TextInput,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useLocalSearchParams, useRouter, Stack } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { colors, spacing, borderRadius, typography, shadows } from '@/constants/theme';
import { getDevotionalById, getTodaysDevotional } from '@/constants/devotions';
import { useUserStore } from '@/store/userStore';
import { useJournalStore } from '@/store/journalStore';

export default function DevotionDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const { recordDevotion, saveVerse, isVerseSaved, unsaveVerse, isDevotionCompleted } = useUserStore();
  const { addJournalEntry, getJournalEntryByDevotionId } = useJournalStore();

  // Get devotional - fallback to today's if id not found
  const devotional = id ? getDevotionalById(id) : getTodaysDevotional();

  if (!devotional) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.errorContainer}>
          <Ionicons name="alert-circle" size={64} color={colors.error} />
          <Text style={styles.errorText}>Devotional not found</Text>
          <Pressable style={styles.backButton} onPress={() => router.back()}>
            <Text style={styles.backButtonText}>Go Back</Text>
          </Pressable>
        </View>
      </SafeAreaView>
    );
  }

  const [showJournal, setShowJournal] = useState(false);
  const [journalEntry, setJournalEntry] = useState('');
  const [reflectionAnswers, setReflectionAnswers] = useState<string[]>(
    new Array(devotional.reflection.length).fill('')
  );

  const isCompleted = isDevotionCompleted(devotional.id);
  const existingJournalEntry = getJournalEntryByDevotionId(devotional.id);
  const verseSaved = isVerseSaved(devotional.id);

  const handleComplete = () => {
    recordDevotion(devotional.id);
    Alert.alert(
      'Devotional Complete',
      'Great job staying consistent in your faith journey!',
      [{ text: 'Continue', onPress: () => setShowJournal(true) }]
    );
  };

  const handleSaveJournal = () => {
    if (!journalEntry.trim() && reflectionAnswers.every(a => !a.trim())) {
      Alert.alert('Add some reflections', 'Write down your thoughts before saving.');
      return;
    }

    addJournalEntry({
      devotionId: devotional.id,
      content: journalEntry.trim(),
      reflections: reflectionAnswers.filter(a => a.trim()),
      verse: devotional.verse,
      verseReference: devotional.verseReference,
    });

    Alert.alert('Journal Saved', 'Your reflections have been saved.', [
      { text: 'Done', onPress: () => router.back() },
    ]);
  };

  const handleToggleVerse = () => {
    if (verseSaved) {
      unsaveVerse(devotional.id);
    } else {
      saveVerse(devotional.id);
    }
  };

  return (
    <>
      <Stack.Screen
        options={{
          headerTitle: devotional.theme.charAt(0).toUpperCase() + devotional.theme.slice(1),
        }}
      />
      <SafeAreaView style={styles.container} edges={['bottom']}>
        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.content}
          showsVerticalScrollIndicator={false}
        >
          {/* Header Card */}
          <View style={styles.headerCard}>
            <LinearGradient
              colors={[colors.sunriseStart + '30', colors.sunriseEnd]}
              style={styles.headerGradient}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
            />
            <Text style={styles.title}>{devotional.title}</Text>
            <View style={styles.themeTag}>
              <Text style={styles.themeTagText}>
                {devotional.theme.charAt(0).toUpperCase() + devotional.theme.slice(1)}
              </Text>
            </View>
            {isCompleted && (
              <View style={styles.completedBadge}>
                <Ionicons name="checkmark-circle" size={16} color={colors.success} />
                <Text style={styles.completedText}>Completed</Text>
              </View>
            )}
          </View>

          {/* Scripture Card */}
          <View style={styles.verseCard}>
            <View style={styles.verseHeader}>
              <Ionicons name="book-outline" size={18} color={colors.versePrimary} />
              <Text style={styles.verseLabel}>Today's Scripture</Text>
              <Pressable style={styles.saveVerseButton} onPress={handleToggleVerse}>
                <Ionicons
                  name={verseSaved ? 'bookmark' : 'bookmark-outline'}
                  size={20}
                  color={verseSaved ? colors.primary : colors.textMuted}
                />
              </Pressable>
            </View>
            <Text style={styles.verseText}>"{devotional.verse}"</Text>
            <Text style={styles.verseReference}>{devotional.verseReference}</Text>
          </View>

          {/* Devotional Content */}
          <View style={styles.devotionalContent}>
            {devotional.content.split('\n\n').map((paragraph, index) => (
              <Text key={index} style={styles.paragraph}>
                {paragraph}
              </Text>
            ))}
          </View>

          {/* Prayer */}
          <View style={styles.prayerCard}>
            <View style={styles.prayerHeader}>
              <Ionicons name="heart" size={20} color={colors.prayerPrimary} />
              <Text style={styles.prayerLabel}>Prayer</Text>
            </View>
            <Text style={styles.prayerText}>{devotional.prayer}</Text>
          </View>

          {/* Reflection Questions */}
          <View style={styles.reflectionSection}>
            <View style={styles.reflectionHeader}>
              <Ionicons name="chatbubble-ellipses" size={20} color={colors.primary} />
              <Text style={styles.reflectionLabel}>Reflection Questions</Text>
            </View>
            {devotional.reflection.map((question, index) => (
              <View key={index} style={styles.reflectionItem}>
                <Text style={styles.reflectionQuestion}>{index + 1}. {question}</Text>
                {showJournal && (
                  <TextInput
                    style={styles.reflectionInput}
                    placeholder="Your thoughts..."
                    placeholderTextColor={colors.textMuted}
                    value={reflectionAnswers[index]}
                    onChangeText={(text) => {
                      const newAnswers = [...reflectionAnswers];
                      newAnswers[index] = text;
                      setReflectionAnswers(newAnswers);
                    }}
                    multiline
                  />
                )}
              </View>
            ))}
          </View>

          {/* Journal Section */}
          {showJournal && (
            <View style={styles.journalSection}>
              <Text style={styles.journalLabel}>Additional Notes</Text>
              <TextInput
                style={styles.journalInput}
                placeholder="Write your thoughts, prayers, or insights..."
                placeholderTextColor={colors.textMuted}
                value={journalEntry}
                onChangeText={setJournalEntry}
                multiline
                numberOfLines={6}
                textAlignVertical="top"
              />
            </View>
          )}
        </ScrollView>

        {/* Bottom Action */}
        <View style={styles.bottomAction}>
          {!isCompleted ? (
            <Pressable
              style={({ pressed }) => [
                styles.completeButton,
                pressed && styles.buttonPressed,
              ]}
              onPress={handleComplete}
            >
              <Ionicons name="checkmark-circle" size={24} color={colors.surface} />
              <Text style={styles.completeButtonText}>Mark as Complete</Text>
            </Pressable>
          ) : showJournal ? (
            <Pressable
              style={({ pressed }) => [
                styles.saveButton,
                pressed && styles.buttonPressed,
              ]}
              onPress={handleSaveJournal}
            >
              <Ionicons name="save" size={24} color={colors.surface} />
              <Text style={styles.saveButtonText}>Save Journal Entry</Text>
            </Pressable>
          ) : (
            <Pressable
              style={({ pressed }) => [
                styles.journalButton,
                pressed && styles.buttonPressed,
              ]}
              onPress={() => setShowJournal(true)}
            >
              <Ionicons name="create" size={24} color={colors.primary} />
              <Text style={styles.journalButtonText}>Add Journal Entry</Text>
            </Pressable>
          )}
        </View>
      </SafeAreaView>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  errorContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: spacing.xl,
  },
  errorText: {
    ...typography.h3,
    color: colors.text,
    marginTop: spacing.lg,
    marginBottom: spacing.lg,
  },
  backButton: {
    backgroundColor: colors.primary,
    paddingHorizontal: spacing.xl,
    paddingVertical: spacing.md,
    borderRadius: borderRadius.md,
  },
  backButtonText: {
    ...typography.bodyBold,
    color: colors.surface,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: spacing.lg,
    paddingBottom: 120,
  },
  headerCard: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    marginBottom: spacing.lg,
    overflow: 'hidden',
    ...shadows.md,
  },
  headerGradient: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
  },
  title: {
    ...typography.h1,
    color: colors.text,
    marginBottom: spacing.sm,
  },
  themeTag: {
    alignSelf: 'flex-start',
    backgroundColor: colors.primary + '20',
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: borderRadius.sm,
  },
  themeTagText: {
    ...typography.caption,
    color: colors.primary,
    fontWeight: '600',
  },
  completedBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    marginTop: spacing.md,
  },
  completedText: {
    ...typography.caption,
    color: colors.success,
    fontWeight: '600',
  },
  verseCard: {
    backgroundColor: colors.verseSecondary,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    marginBottom: spacing.lg,
    borderLeftWidth: 4,
    borderLeftColor: colors.versePrimary,
  },
  verseHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  verseLabel: {
    ...typography.caption,
    color: colors.versePrimary,
    fontWeight: '600',
    marginLeft: spacing.sm,
    flex: 1,
  },
  saveVerseButton: {
    padding: spacing.xs,
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
  devotionalContent: {
    marginBottom: spacing.lg,
  },
  paragraph: {
    ...typography.body,
    color: colors.text,
    marginBottom: spacing.md,
    lineHeight: 26,
  },
  prayerCard: {
    backgroundColor: colors.prayerSecondary,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    marginBottom: spacing.lg,
    borderLeftWidth: 4,
    borderLeftColor: colors.prayerPrimary,
  },
  prayerHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  prayerLabel: {
    ...typography.caption,
    color: colors.prayerPrimary,
    fontWeight: '600',
    marginLeft: spacing.sm,
  },
  prayerText: {
    ...typography.body,
    color: colors.text,
    fontStyle: 'italic',
    lineHeight: 26,
  },
  reflectionSection: {
    marginBottom: spacing.lg,
  },
  reflectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  reflectionLabel: {
    ...typography.bodyBold,
    color: colors.text,
    marginLeft: spacing.sm,
  },
  reflectionItem: {
    marginBottom: spacing.md,
  },
  reflectionQuestion: {
    ...typography.body,
    color: colors.text,
    marginBottom: spacing.sm,
  },
  reflectionInput: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.md,
    padding: spacing.md,
    ...typography.body,
    color: colors.text,
    borderWidth: 1,
    borderColor: colors.border,
    minHeight: 80,
  },
  journalSection: {
    marginBottom: spacing.lg,
  },
  journalLabel: {
    ...typography.bodyBold,
    color: colors.text,
    marginBottom: spacing.sm,
  },
  journalInput: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.md,
    padding: spacing.md,
    ...typography.body,
    color: colors.text,
    borderWidth: 1,
    borderColor: colors.border,
    minHeight: 120,
  },
  bottomAction: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    padding: spacing.lg,
    backgroundColor: colors.background,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  completeButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.primary,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    gap: spacing.sm,
    ...shadows.md,
  },
  completeButtonText: {
    ...typography.bodyBold,
    color: colors.surface,
    fontSize: 18,
  },
  saveButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.success,
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    gap: spacing.sm,
    ...shadows.md,
  },
  saveButtonText: {
    ...typography.bodyBold,
    color: colors.surface,
    fontSize: 18,
  },
  journalButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.primary + '15',
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    gap: spacing.sm,
    borderWidth: 1,
    borderColor: colors.primary,
  },
  journalButtonText: {
    ...typography.bodyBold,
    color: colors.primary,
    fontSize: 18,
  },
  buttonPressed: {
    opacity: 0.9,
    transform: [{ scale: 0.98 }],
  },
});
