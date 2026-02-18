/**
 * Scripture Screen
 * Daily Bible passage reading with scroll tracking
 */

import React, { useEffect, useRef, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  NativeSyntheticEvent,
  NativeScrollEvent,
  ActivityIndicator,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useDevotionStore } from '@/stores/devotionStore';
import { fetchDailyPassage } from '@/services/bibleService';
import { COLORS, SCRIPTURE_MIN_READ_SECONDS } from '@/utils/constants';
import { BiblePassage } from '@/types';

export default function ScriptureScreen() {
  const router = useRouter();
  const scrollViewRef = useRef<ScrollView>(null);
  const startTimeRef = useRef<number>(Date.now());

  const { todaysPassage, setTodaysPassage, completeScripture, completeSession } =
    useDevotionStore();

  const [passage, setPassage] = useState<BiblePassage | null>(todaysPassage);
  const [loading, setLoading] = useState(!todaysPassage);
  const [hasScrolledToBottom, setHasScrolledToBottom] = useState(false);
  const [hasMetTimeRequirement, setHasMetTimeRequirement] = useState(false);
  const [canComplete, setCanComplete] = useState(false);
  const [timeSpent, setTimeSpent] = useState(0);

  useEffect(() => {
    if (!todaysPassage) {
      loadPassage();
    }

    // Track time spent
    const timer = setInterval(() => {
      const elapsed = Math.floor((Date.now() - startTimeRef.current) / 1000);
      setTimeSpent(elapsed);

      if (elapsed >= SCRIPTURE_MIN_READ_SECONDS) {
        setHasMetTimeRequirement(true);
      }
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    // Can complete when scrolled to bottom AND met time requirement
    if (hasScrolledToBottom && hasMetTimeRequirement) {
      setCanComplete(true);
    }
  }, [hasScrolledToBottom, hasMetTimeRequirement]);

  async function loadPassage() {
    try {
      const fetchedPassage = await fetchDailyPassage();
      setPassage(fetchedPassage);
      setTodaysPassage(fetchedPassage);
    } catch (error) {
      console.error('Failed to load passage:', error);
    } finally {
      setLoading(false);
    }
  }

  function handleScroll(event: NativeSyntheticEvent<NativeScrollEvent>) {
    const { layoutMeasurement, contentOffset, contentSize } = event.nativeEvent;
    const paddingBottom = 40;
    const isAtBottom =
      layoutMeasurement.height + contentOffset.y >= contentSize.height - paddingBottom;

    if (isAtBottom && !hasScrolledToBottom) {
      setHasScrolledToBottom(true);
    }
  }

  async function handleComplete() {
    if (!canComplete || !passage) return;

    completeScripture(passage);
    await completeSession();
    router.replace('/(tabs)');
  }

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
        <Text style={styles.loadingText}>Loading today's passage...</Text>
      </View>
    );
  }

  const remainingTime = Math.max(0, SCRIPTURE_MIN_READ_SECONDS - timeSpent);

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Daily Scripture</Text>
        <Text style={styles.reference}>{passage?.reference}</Text>
      </View>

      {/* Scripture Content */}
      <ScrollView
        ref={scrollViewRef}
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        onScroll={handleScroll}
        scrollEventThrottle={16}
      >
        {passage?.verses && passage.verses.length > 0 ? (
          passage.verses.map((verse, index) => (
            <View key={index} style={styles.verseContainer}>
              <Text style={styles.verseNumber}>{verse.verse}</Text>
              <Text style={styles.verseText}>{verse.text}</Text>
            </View>
          ))
        ) : (
          <Text style={styles.passageText}>{passage?.text}</Text>
        )}

        {/* Scroll indicator */}
        {!hasScrolledToBottom && (
          <View style={styles.scrollIndicator}>
            <Text style={styles.scrollIndicatorText}>Scroll to continue reading</Text>
          </View>
        )}
      </ScrollView>

      {/* Footer */}
      <View style={styles.footer}>
        {/* Progress indicators */}
        <View style={styles.progressContainer}>
          <View style={styles.progressItem}>
            <View
              style={[
                styles.progressDot,
                hasScrolledToBottom && styles.progressDotComplete,
              ]}
            />
            <Text style={styles.progressText}>
              {hasScrolledToBottom ? 'Read complete' : 'Read passage'}
            </Text>
          </View>
          <View style={styles.progressItem}>
            <View
              style={[
                styles.progressDot,
                hasMetTimeRequirement && styles.progressDotComplete,
              ]}
            />
            <Text style={styles.progressText}>
              {hasMetTimeRequirement
                ? 'Time complete'
                : `${remainingTime}s remaining`}
            </Text>
          </View>
        </View>

        {/* Complete Button */}
        <TouchableOpacity
          style={[styles.completeButton, !canComplete && styles.completeButtonDisabled]}
          onPress={handleComplete}
          disabled={!canComplete}
          activeOpacity={0.8}
        >
          <Text
            style={[
              styles.completeButtonText,
              !canComplete && styles.completeButtonTextDisabled,
            ]}
          >
            {canComplete ? 'Complete Devotion' : 'Keep Reading'}
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.background,
  },
  loadingText: {
    marginTop: 12,
    color: COLORS.textSecondary,
    fontSize: 16,
  },
  header: {
    backgroundColor: COLORS.surface,
    paddingTop: 20,
    paddingBottom: 16,
    paddingHorizontal: 20,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.background,
  },
  headerTitle: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: 4,
  },
  reference: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.text,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 60,
  },
  verseContainer: {
    flexDirection: 'row',
    marginBottom: 12,
  },
  verseNumber: {
    fontSize: 12,
    color: COLORS.primary,
    fontWeight: '600',
    marginRight: 8,
    marginTop: 4,
    width: 20,
  },
  verseText: {
    flex: 1,
    fontSize: 18,
    lineHeight: 28,
    color: COLORS.text,
  },
  passageText: {
    fontSize: 18,
    lineHeight: 28,
    color: COLORS.text,
  },
  scrollIndicator: {
    marginTop: 20,
    padding: 16,
    backgroundColor: COLORS.primary + '10',
    borderRadius: 8,
    alignItems: 'center',
  },
  scrollIndicatorText: {
    color: COLORS.primary,
    fontWeight: '500',
  },
  footer: {
    backgroundColor: COLORS.surface,
    padding: 20,
    borderTopWidth: 1,
    borderTopColor: COLORS.background,
  },
  progressContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 16,
  },
  progressItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  progressDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: COLORS.disabled,
  },
  progressDotComplete: {
    backgroundColor: COLORS.success,
  },
  progressText: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  completeButton: {
    backgroundColor: COLORS.primary,
    borderRadius: 12,
    paddingVertical: 18,
    alignItems: 'center',
  },
  completeButtonDisabled: {
    backgroundColor: COLORS.disabled,
  },
  completeButtonText: {
    color: COLORS.surface,
    fontSize: 18,
    fontWeight: '700',
  },
  completeButtonTextDisabled: {
    color: COLORS.textSecondary,
  },
});
