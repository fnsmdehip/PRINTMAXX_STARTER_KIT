import { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { router } from 'expo-router';
import * as Haptics from 'expo-haptics';
import { useDevotionStore } from '../src/stores/devotionStore';
import { bibleService, DailyVerse } from '../src/services/bibleService';

const { height } = Dimensions.get('window');
const MIN_READING_TIME = 30; // 30 seconds minimum

export default function Scripture() {
  const [verse, setVerse] = useState<DailyVerse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [hasScrolledToBottom, setHasScrolledToBottom] = useState(false);
  const [readingTime, setReadingTime] = useState(0);
  const [canComplete, setCanComplete] = useState(false);
  const scrollViewRef = useRef<ScrollView>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const completeSession = useDevotionStore((state) => state.completeSession);

  useEffect(() => {
    loadVerse();
    startReadingTimer();

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  useEffect(() => {
    if (hasScrolledToBottom && readingTime >= MIN_READING_TIME) {
      setCanComplete(true);
    }
  }, [hasScrolledToBottom, readingTime]);

  const loadVerse = async () => {
    try {
      setLoading(true);
      const dailyVerse = await bibleService.getDailyVerse();
      setVerse(dailyVerse);
      setError(null);
    } catch (err) {
      setError('Unable to load scripture. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const startReadingTimer = () => {
    timerRef.current = setInterval(() => {
      setReadingTime((prev) => prev + 1);
    }, 1000);
  };

  const handleScroll = (event: any) => {
    const { layoutMeasurement, contentOffset, contentSize } = event.nativeEvent;
    const isAtBottom = layoutMeasurement.height + contentOffset.y >= contentSize.height - 50;

    if (isAtBottom && !hasScrolledToBottom) {
      setHasScrolledToBottom(true);
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }
  };

  const handleComplete = async () => {
    await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    completeSession(false, true, verse?.reference);
    router.replace('/(tabs)');
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#6c63ff" />
        <Text style={styles.loadingText}>Loading today's scripture...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorEmoji}>📖</Text>
        <Text style={styles.errorText}>{error}</Text>
        <TouchableOpacity style={styles.retryButton} onPress={loadVerse}>
          <Text style={styles.retryText}>Try Again</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Daily Scripture</Text>
        <Text style={styles.headerSubtitle}>
          Read and meditate on God's Word
        </Text>
      </View>

      <ScrollView
        ref={scrollViewRef}
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        onScroll={handleScroll}
        scrollEventThrottle={16}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.verseCard}>
          <Text style={styles.reference}>{verse?.reference}</Text>
          <Text style={styles.verseText}>{verse?.text}</Text>
        </View>

        <View style={styles.reflectionSection}>
          <Text style={styles.reflectionTitle}>Reflect</Text>
          <Text style={styles.reflectionPrompt}>
            As you read this passage, consider:
          </Text>
          <View style={styles.promptList}>
            <Text style={styles.promptItem}>
              What is God saying to you today?
            </Text>
            <Text style={styles.promptItem}>
              How does this apply to your life?
            </Text>
            <Text style={styles.promptItem}>
              What action can you take based on this truth?
            </Text>
          </View>
        </View>

        <View style={styles.spacer} />
      </ScrollView>

      <View style={styles.footer}>
        {!canComplete && (
          <View style={styles.progressInfo}>
            <Text style={styles.progressText}>
              {!hasScrolledToBottom
                ? 'Scroll down to read the full passage'
                : `Reading... ${Math.max(0, MIN_READING_TIME - readingTime)}s remaining`}
            </Text>
          </View>
        )}

        <TouchableOpacity
          style={[styles.completeButton, !canComplete && styles.completeButtonDisabled]}
          onPress={handleComplete}
          disabled={!canComplete}
        >
          <Text style={styles.completeButtonText}>
            {canComplete ? 'Complete Reading' : 'Reading...'}
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
  },
  loadingContainer: {
    flex: 1,
    backgroundColor: '#1a1a2e',
    alignItems: 'center',
    justifyContent: 'center',
  },
  loadingText: {
    color: '#8b8b9e',
    fontSize: 16,
    marginTop: 16,
  },
  errorContainer: {
    flex: 1,
    backgroundColor: '#1a1a2e',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 24,
  },
  errorEmoji: {
    fontSize: 64,
    marginBottom: 16,
  },
  errorText: {
    color: '#8b8b9e',
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 24,
  },
  retryButton: {
    backgroundColor: '#6c63ff',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  },
  retryText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  header: {
    paddingHorizontal: 24,
    paddingTop: 20,
    paddingBottom: 16,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#8b8b9e',
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: 24,
    paddingBottom: 24,
  },
  verseCard: {
    backgroundColor: '#2a2a4e',
    borderRadius: 16,
    padding: 24,
    marginBottom: 24,
  },
  reference: {
    fontSize: 14,
    color: '#6c63ff',
    fontWeight: '600',
    marginBottom: 16,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  verseText: {
    fontSize: 20,
    color: '#fff',
    lineHeight: 32,
    fontStyle: 'italic',
  },
  reflectionSection: {
    backgroundColor: '#2a2a4e',
    borderRadius: 16,
    padding: 24,
  },
  reflectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 12,
  },
  reflectionPrompt: {
    fontSize: 14,
    color: '#8b8b9e',
    marginBottom: 16,
  },
  promptList: {
    gap: 12,
  },
  promptItem: {
    fontSize: 16,
    color: '#b0b0c0',
    lineHeight: 24,
    paddingLeft: 16,
    borderLeftWidth: 2,
    borderLeftColor: '#6c63ff',
  },
  spacer: {
    height: 100,
  },
  footer: {
    paddingHorizontal: 24,
    paddingBottom: 40,
    paddingTop: 16,
    backgroundColor: '#1a1a2e',
  },
  progressInfo: {
    marginBottom: 12,
  },
  progressText: {
    color: '#8b8b9e',
    fontSize: 14,
    textAlign: 'center',
  },
  completeButton: {
    backgroundColor: '#6c63ff',
    paddingVertical: 18,
    borderRadius: 16,
    alignItems: 'center',
  },
  completeButtonDisabled: {
    backgroundColor: '#3a3a5e',
  },
  completeButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
});
