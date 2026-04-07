import React, { useState, useRef, useCallback, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Dimensions,
  Animated,
  ScrollView,
  Platform,
  Linking,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { colors, fonts, spacing, borderRadius, shadows, APP_CONFIG } from '../constants/theme';
import { categories, categoryIcons, getBooksByCategory, books } from '../data/catalog';
import { completeOnboarding, saveOnboardingState } from '../services/storage';
import { playSound } from '../sounds/SoundEngine';
import {
  getOfferings,
  purchasePackage,
  restorePurchases,
} from '../services/purchases';
import BookCover from '../components/BookCover';
import { Book } from '../types';
// PurchasesPackage type defined locally (no RevenueCat dependency)
type PurchasesPackage = { identifier: string; product: { priceString: string; title: string }; __stripeUrl?: string };

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');
const TOTAL_STEPS = 12;
const ONBOARDING_PREFS_KEY = '@pa_onboarding_prefs';

// --------------------------------------------------------------------------
// Genre mapping for the onboarding (simpler labels -> catalog categories)
// --------------------------------------------------------------------------
const GENRE_MAP: Record<string, { label: string; icon: string; categories: string[] }> = {
  fiction: { label: 'Fiction & Literature', icon: 'book-outline', categories: ['Sacred Texts'] },
  philosophy: { label: 'Philosophy', icon: 'school-outline', categories: ['Philosophy'] },
  science: { label: 'Science & Mind', icon: 'flask-outline', categories: ['Psychology'] },
  poetry: { label: 'Poetry & Verse', icon: 'musical-notes-outline', categories: ['Eastern Wisdom'] },
  history: { label: 'History & Civilization', icon: 'time-outline', categories: ['Secret Societies', 'Forbidden / Controversial'] },
  adventure: { label: 'Adventure & Strategy', icon: 'compass-outline', categories: ['Philosophy'] },
  mysticism: { label: 'Mysticism & Occult', icon: 'eye-outline', categories: ['Hermetic / Occult', 'Alchemy / Mysticism'] },
  divination: { label: 'Astrology & Divination', icon: 'star-outline', categories: ['Astrology / Divination', 'Apocrypha'] },
};

interface OnboardingFlowProps {
  onComplete: () => void;
}

export default function OnboardingFlow({ onComplete }: OnboardingFlowProps) {
  // ---------- state ----------
  const [step, setStep] = useState(0);

  // Screen 2: Reading goal
  const [readingGoal, setReadingGoal] = useState('');
  // Screen 3: Genres
  const [selectedGenres, setSelectedGenres] = useState<string[]>([]);
  // Screen 4: Reading speed
  const [readingSpeed, setReadingSpeed] = useState('');
  // Screen 5: Daily time
  const [dailyTime, setDailyTime] = useState('');
  // Screen 10: Notification permission
  const [notifGranted, setNotifGranted] = useState(false);

  // Paywall state
  const [selectedPlan, setSelectedPlan] = useState<'annual' | 'monthly'>('annual');
  const [purchasing, setPurchasing] = useState(false);
  const [restoring, setRestoring] = useState(false);
  const [annualPackage, setAnnualPackage] = useState<PurchasesPackage | null>(null);
  const [monthlyPackage, setMonthlyPackage] = useState<PurchasesPackage | null>(null);
  const [showRescue, setShowRescue] = useState(false);

  // Animation
  const fadeAnim = useRef(new Animated.Value(1)).current;
  const slideAnim = useRef(new Animated.Value(0)).current;

  // ---------- derived ----------
  const mappedCategories = selectedGenres.flatMap(g => GENRE_MAP[g]?.categories ?? []);
  const recommendedBooks = getRecommendedBooks(mappedCategories);
  const projection = getReadingProjection(readingSpeed, dailyTime);

  // ---------- load offerings on paywall step ----------
  useEffect(() => {
    if (step === 11) {
      (async () => {
        try {
          const offering = await getOfferings();
          if (offering) {
            setAnnualPackage(offering.annual ?? null);
            setMonthlyPackage(offering.monthly ?? null);
          }
        } catch (err) {
          console.warn('[Onboarding] Could not load offerings:', err);
        }
      })();
    }
  }, [step]);

  // ---------- animations ----------
  const animateTransition = useCallback((nextStep: number) => {
    Animated.parallel([
      Animated.timing(fadeAnim, { toValue: 0, duration: 150, useNativeDriver: true }),
      Animated.timing(slideAnim, { toValue: -40, duration: 150, useNativeDriver: true }),
    ]).start(() => {
      setStep(nextStep);
      slideAnim.setValue(40);
      Animated.parallel([
        Animated.timing(fadeAnim, { toValue: 1, duration: 250, useNativeDriver: true }),
        Animated.timing(slideAnim, { toValue: 0, duration: 250, useNativeDriver: true }),
      ]).start();
    });
  }, [fadeAnim, slideAnim]);

  const goNext = () => {
    if (step < TOTAL_STEPS - 1) {
      playSound('swipe');
      animateTransition(step + 1);
    }
  };

  const goBack = () => {
    if (step > 0) {
      playSound('swipe');
      animateTransition(step - 1);
    }
  };

  // ---------- save preferences ----------
  const savePrefs = async () => {
    try {
      await AsyncStorage.setItem(ONBOARDING_PREFS_KEY, JSON.stringify({
        readingGoal,
        selectedGenres,
        readingSpeed,
        dailyTime,
        notifGranted,
        savedAt: new Date().toISOString(),
      }));
    } catch {}
  };

  // ---------- genre toggle ----------
  const toggleGenre = (key: string) => {
    setSelectedGenres(prev =>
      prev.includes(key) ? prev.filter(g => g !== key) : [...prev, key]
    );
  };

  // ---------- finish handlers ----------
  const handleFinish = async () => {
    playSound('success');
    await savePrefs();
    const cats = mappedCategories.length > 0 ? [...new Set(mappedCategories)] : [];
    await completeOnboarding(cats);
    onComplete();
  };

  const handlePurchase = async () => {
    const pkg = selectedPlan === 'annual' ? annualPackage : monthlyPackage;
    if (!pkg) {
      Alert.alert(
        'Purchase Unavailable',
        'Could not connect to the App Store right now. You can subscribe later from Settings.',
        [{ text: 'OK', onPress: handleFinish }],
      );
      return;
    }
    try {
      setPurchasing(true);
      await purchasePackage(pkg);
      await saveOnboardingState({ isPremium: true });
      playSound('premium');
      await savePrefs();
      const cats = mappedCategories.length > 0 ? [...new Set(mappedCategories)] : [];
      await completeOnboarding(cats);
      onComplete();
    } catch (err: any) {
      if (!err?.userCancelled) {
        Alert.alert('Purchase Failed', err?.message || 'Something went wrong. Please try again.');
      }
    } finally {
      setPurchasing(false);
    }
  };

  const handleRestore = async () => {
    try {
      setRestoring(true);
      const restored = await restorePurchases();
      if (restored) {
        await saveOnboardingState({ isPremium: true });
        Alert.alert('Restored', 'Your premium access has been restored!', [
          { text: 'Continue', onPress: handleFinish },
        ]);
      } else {
        Alert.alert('No Subscription Found', 'We could not find an active subscription for this account.');
      }
    } catch {
      Alert.alert('Restore Failed', 'Please check your connection and try again.');
    } finally {
      setRestoring(false);
    }
  };

  const handleDeclinePaywall = () => {
    if (!showRescue) {
      setShowRescue(true);
    } else {
      handleFinish();
    }
  };

  // ---------- progress bar ----------
  const renderProgressBar = () => (
    <View style={styles.progressBarContainer}>
      <View style={[styles.progressBarFill, { width: `${((step + 1) / TOTAL_STEPS) * 100}%` }]} />
    </View>
  );

  // ---------- header with back button ----------
  const renderHeader = () => (
    <View style={styles.header}>
      {step > 0 ? (
        <TouchableOpacity onPress={goBack} style={styles.backBtn} hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}>
          <Ionicons name="chevron-back" size={24} color={colors.textSecondary} />
        </TouchableOpacity>
      ) : (
        <View style={styles.backPlaceholder} />
      )}
      <Text style={styles.stepCounter}>{step + 1} of {TOTAL_STEPS}</Text>
      {step < TOTAL_STEPS - 1 ? (
        <View style={styles.backPlaceholder} />
      ) : (
        <View style={styles.backPlaceholder} />
      )}
    </View>
  );

  // ======================================================================
  // SCREEN 1: Welcome
  // ======================================================================
  const renderWelcome = () => (
    <View style={styles.screenContainer}>
      <View style={styles.centeredContent}>
        <View style={styles.bookStackIllustration}>
          <View style={[styles.stackBook, styles.stackBook1]}>
            <Ionicons name="book" size={20} color={colors.accentDim} />
          </View>
          <View style={[styles.stackBook, styles.stackBook2]}>
            <Ionicons name="book" size={24} color={colors.accent} />
          </View>
          <View style={[styles.stackBook, styles.stackBook3]}>
            <Ionicons name="book" size={28} color={colors.parchment} />
          </View>
          <View style={styles.stackGlow} />
        </View>
        <View style={styles.welcomeIconContainer}>
          <Ionicons name="library" size={56} color={colors.accent} />
          <View style={styles.welcomeIconRing} />
        </View>
        <Text style={styles.welcomeTitle}>Your Personal Library{'\n'}of Classics</Text>
        <View style={styles.ornamentRow}>
          <View style={styles.ornamentDash} />
          <Ionicons name="sparkles" size={12} color={colors.accent} style={{ marginHorizontal: 10, opacity: 0.6 }} />
          <View style={styles.ornamentDash} />
        </View>
        <Text style={styles.welcomeSubtitle}>
          156 timeless texts from philosophy, sacred traditions,{'\n'}psychology, and the mysteries. All in your pocket.
        </Text>
      </View>
      <View style={styles.bottomActions}>
        <TouchableOpacity style={styles.primaryBtn} onPress={goNext}>
          <Text style={styles.primaryBtnText}>Begin Your Journey</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  // ======================================================================
  // SCREEN 2: Reading Goal
  // ======================================================================
  const GOALS = [
    { key: 'classics', label: 'Read more classics', icon: 'library-outline' as const },
    { key: 'habit', label: 'Build a daily reading habit', icon: 'calendar-outline' as const },
    { key: 'explore', label: 'Explore new genres', icon: 'compass-outline' as const },
    { key: 'finish', label: 'Finish books I\'ve started', icon: 'checkmark-done-outline' as const },
  ];

  const renderReadingGoal = () => (
    <View style={styles.screenContainer}>
      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        <Text style={styles.screenTitle}>What do you want to achieve?</Text>
        <Text style={styles.screenSubtitle}>This helps us personalize your experience</Text>
        <View style={styles.optionsList}>
          {GOALS.map(g => {
            const selected = readingGoal === g.key;
            return (
              <TouchableOpacity
                key={g.key}
                style={[styles.optionCard, selected && styles.optionCardSelected]}
                onPress={() => setReadingGoal(g.key)}
                activeOpacity={0.7}
              >
                <View style={[styles.optionIconWrap, selected && styles.optionIconWrapSelected]}>
                  <Ionicons name={g.icon} size={22} color={selected ? colors.accent : colors.textMuted} />
                </View>
                <Text style={[styles.optionLabel, selected && styles.optionLabelSelected]}>{g.label}</Text>
                <View style={[styles.radioOuter, selected && styles.radioOuterSelected]}>
                  {selected && <View style={styles.radioInner} />}
                </View>
              </TouchableOpacity>
            );
          })}
        </View>
      </ScrollView>
      <View style={styles.bottomActions}>
        <TouchableOpacity
          style={[styles.primaryBtn, !readingGoal && styles.primaryBtnDisabled]}
          onPress={goNext}
          disabled={!readingGoal}
        >
          <Text style={styles.primaryBtnText}>Continue</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  // ======================================================================
  // SCREEN 3: Favorite Genres (multi-select)
  // ======================================================================
  const renderGenres = () => (
    <View style={styles.screenContainer}>
      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        <Text style={styles.screenTitle}>What genres interest you?</Text>
        <Text style={styles.screenSubtitle}>Select all that apply</Text>
        <View style={styles.genreGrid}>
          {Object.entries(GENRE_MAP).map(([key, val]) => {
            const selected = selectedGenres.includes(key);
            return (
              <TouchableOpacity
                key={key}
                style={[styles.genreChip, selected && styles.genreChipSelected]}
                onPress={() => toggleGenre(key)}
                activeOpacity={0.7}
              >
                <Ionicons
                  name={val.icon as any}
                  size={26}
                  color={selected ? colors.accent : colors.textMuted}
                  style={{ marginBottom: 6 }}
                />
                <Text style={[styles.genreChipLabel, selected && styles.genreChipLabelSelected]}>
                  {val.label}
                </Text>
              </TouchableOpacity>
            );
          })}
        </View>
      </ScrollView>
      <View style={styles.bottomActions}>
        <TouchableOpacity
          style={[styles.primaryBtn, selectedGenres.length === 0 && styles.primaryBtnDisabled]}
          onPress={goNext}
          disabled={selectedGenres.length === 0}
        >
          <Text style={styles.primaryBtnText}>
            {selectedGenres.length > 0
              ? `Continue with ${selectedGenres.length} selected`
              : 'Select at least one'}
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  // ======================================================================
  // SCREEN 4: Reading Speed
  // ======================================================================
  const SPEEDS = [
    { key: 'casual', label: 'Casual reader', desc: 'A few pages when I have time', icon: 'leaf-outline' as const },
    { key: 'regular', label: 'Regular reader', desc: 'I read most days', icon: 'book-outline' as const },
    { key: 'fast', label: 'Fast reader', desc: 'I finish books quickly', icon: 'flash-outline' as const },
  ];

  const renderReadingSpeed = () => (
    <View style={styles.screenContainer}>
      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        <Text style={styles.screenTitle}>How would you describe{'\n'}your reading pace?</Text>
        <Text style={styles.screenSubtitle}>No wrong answer here</Text>
        <View style={styles.optionsList}>
          {SPEEDS.map(s => {
            const selected = readingSpeed === s.key;
            return (
              <TouchableOpacity
                key={s.key}
                style={[styles.optionCard, selected && styles.optionCardSelected]}
                onPress={() => setReadingSpeed(s.key)}
                activeOpacity={0.7}
              >
                <View style={[styles.optionIconWrap, selected && styles.optionIconWrapSelected]}>
                  <Ionicons name={s.icon} size={22} color={selected ? colors.accent : colors.textMuted} />
                </View>
                <View style={{ flex: 1 }}>
                  <Text style={[styles.optionLabel, selected && styles.optionLabelSelected]}>{s.label}</Text>
                  <Text style={styles.optionDesc}>{s.desc}</Text>
                </View>
                <View style={[styles.radioOuter, selected && styles.radioOuterSelected]}>
                  {selected && <View style={styles.radioInner} />}
                </View>
              </TouchableOpacity>
            );
          })}
        </View>
      </ScrollView>
      <View style={styles.bottomActions}>
        <TouchableOpacity
          style={[styles.primaryBtn, !readingSpeed && styles.primaryBtnDisabled]}
          onPress={goNext}
          disabled={!readingSpeed}
        >
          <Text style={styles.primaryBtnText}>Continue</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  // ======================================================================
  // SCREEN 5: Daily Time
  // ======================================================================
  const TIMES = [
    { key: '15', label: '15 minutes', icon: 'timer-outline' as const },
    { key: '30', label: '30 minutes', icon: 'time-outline' as const },
    { key: '45', label: '45 minutes', icon: 'hourglass-outline' as const },
    { key: '60', label: '1 hour+', icon: 'infinite-outline' as const },
  ];

  const renderDailyTime = () => (
    <View style={styles.screenContainer}>
      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        <Text style={styles.screenTitle}>How much time can you{'\n'}dedicate daily?</Text>
        <Text style={styles.screenSubtitle}>We'll build your reading plan around this</Text>
        <View style={styles.optionsList}>
          {TIMES.map(t => {
            const selected = dailyTime === t.key;
            return (
              <TouchableOpacity
                key={t.key}
                style={[styles.optionCard, selected && styles.optionCardSelected]}
                onPress={() => setDailyTime(t.key)}
                activeOpacity={0.7}
              >
                <View style={[styles.optionIconWrap, selected && styles.optionIconWrapSelected]}>
                  <Ionicons name={t.icon} size={22} color={selected ? colors.accent : colors.textMuted} />
                </View>
                <Text style={[styles.optionLabel, selected && styles.optionLabelSelected]}>{t.label}</Text>
                <View style={[styles.radioOuter, selected && styles.radioOuterSelected]}>
                  {selected && <View style={styles.radioInner} />}
                </View>
              </TouchableOpacity>
            );
          })}
        </View>
      </ScrollView>
      <View style={styles.bottomActions}>
        <TouchableOpacity
          style={[styles.primaryBtn, !dailyTime && styles.primaryBtnDisabled]}
          onPress={goNext}
          disabled={!dailyTime}
        >
          <Text style={styles.primaryBtnText}>Continue</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  // ======================================================================
  // SCREEN 6: Validation / Projection
  // ======================================================================
  const renderValidation = () => {
    const booksPerYear = projection.booksPerYear;
    const barData = [
      { month: 'Jan', count: Math.ceil(booksPerYear / 12) },
      { month: 'Mar', count: Math.ceil((booksPerYear / 12) * 3) },
      { month: 'Jun', count: Math.ceil((booksPerYear / 12) * 6) },
      { month: 'Sep', count: Math.ceil((booksPerYear / 12) * 9) },
      { month: 'Dec', count: booksPerYear },
    ];
    const maxCount = booksPerYear || 1;

    return (
      <View style={styles.screenContainer}>
        <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
          <View style={styles.validationBadge}>
            <Ionicons name="checkmark-circle" size={20} color={colors.success} />
            <Text style={styles.validationBadgeText}>Your goal is achievable</Text>
          </View>
          <Text style={styles.screenTitle}>
            At your pace, you'll finish
          </Text>
          <Text style={styles.projectionNumber}>{booksPerYear} classics</Text>
          <Text style={styles.screenTitle}>this year</Text>

          {/* Simple bar chart */}
          <View style={styles.chartContainer}>
            {barData.map((bar, i) => (
              <View key={bar.month} style={styles.chartBarWrap}>
                <Text style={styles.chartBarCount}>{bar.count}</Text>
                <View style={styles.chartBarTrack}>
                  <Animated.View
                    style={[
                      styles.chartBarFill,
                      { height: `${(bar.count / maxCount) * 100}%` },
                    ]}
                  />
                </View>
                <Text style={styles.chartBarLabel}>{bar.month}</Text>
              </View>
            ))}
          </View>

          <View style={styles.projectionDetails}>
            <View style={styles.projectionRow}>
              <Ionicons name="time-outline" size={18} color={colors.accent} />
              <Text style={styles.projectionText}>{dailyTime || '30'} min/day reading time</Text>
            </View>
            <View style={styles.projectionRow}>
              <Ionicons name="book-outline" size={18} color={colors.accent} />
              <Text style={styles.projectionText}>~{projection.pagesPerDay} pages per day</Text>
            </View>
            <View style={styles.projectionRow}>
              <Ionicons name="calendar-outline" size={18} color={colors.accent} />
              <Text style={styles.projectionText}>~{projection.daysPerBook} days per book</Text>
            </View>
          </View>
        </ScrollView>
        <View style={styles.bottomActions}>
          <TouchableOpacity style={styles.primaryBtn} onPress={goNext}>
            <Text style={styles.primaryBtnText}>See My Recommendations</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  };

  // ======================================================================
  // SCREEN 7: Book Preview (recommended)
  // ======================================================================
  const renderBookPreview = () => {
    const booksToShow = recommendedBooks.slice(0, 6);
    return (
      <View style={styles.screenContainer}>
        <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
          <Text style={styles.screenTitle}>Recommended for you</Text>
          <Text style={styles.screenSubtitle}>Based on your genre picks</Text>
          <View style={styles.bookGrid}>
            {booksToShow.map(book => (
              <View key={book.id} style={styles.bookGridItem}>
                <BookCover book={book} size="small" />
              </View>
            ))}
          </View>
          {booksToShow.length > 0 && (
            <View style={styles.firstBookHighlight}>
              <Text style={styles.firstBookLabel}>Start with</Text>
              <Text style={styles.firstBookTitle}>{booksToShow[0].title}</Text>
              <Text style={styles.firstBookAuthor}>by {booksToShow[0].author}</Text>
              <Text style={styles.firstBookDesc} numberOfLines={3}>{booksToShow[0].description}</Text>
            </View>
          )}
        </ScrollView>
        <View style={styles.bottomActions}>
          <TouchableOpacity style={styles.primaryBtn} onPress={goNext}>
            <Text style={styles.primaryBtnText}>Continue</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  };

  // ======================================================================
  // SCREEN 8: Social Proof
  // ======================================================================
  const TESTIMONIALS = [
    { name: 'Sarah M.', text: 'I finally read Meditations by Marcus Aurelius. This app made it so easy to get through classical texts.', stars: 5 },
    { name: 'James K.', text: 'Having all these philosophy and sacred texts in one place with a beautiful reader changed my daily routine.', stars: 5 },
    { name: 'Aisha R.', text: 'The night mode reader is perfect for my evening reading sessions. I look forward to my 30 minutes every day.', stars: 5 },
  ];

  const renderSocialProof = () => (
    <View style={styles.screenContainer}>
      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        <View style={styles.socialBadge}>
          <Ionicons name="people" size={28} color={colors.accent} />
        </View>
        <Text style={styles.screenTitle}>Join 8,000+ classic{'\n'}literature readers</Text>
        <Text style={styles.screenSubtitle}>See what our community says</Text>

        <View style={styles.starRowCenter}>
          {[1, 2, 3, 4, 5].map(i => (
            <Ionicons key={i} name="star" size={20} color={colors.accent} style={{ marginHorizontal: 2 }} />
          ))}
          <Text style={styles.starRatingText}>4.7 average rating</Text>
        </View>

        {TESTIMONIALS.map((t, i) => (
          <View key={i} style={styles.testimonialCard}>
            <View style={styles.testimonialHeader}>
              <View style={styles.testimonialAvatar}>
                <Text style={styles.testimonialAvatarText}>{t.name[0]}</Text>
              </View>
              <View>
                <Text style={styles.testimonialName}>{t.name}</Text>
                <View style={styles.testimonialStars}>
                  {Array.from({ length: t.stars }, (_, j) => (
                    <Ionicons key={j} name="star" size={12} color={colors.accent} />
                  ))}
                </View>
              </View>
            </View>
            <Text style={styles.testimonialText}>{t.text}</Text>
          </View>
        ))}
      </ScrollView>
      <View style={styles.bottomActions}>
        <TouchableOpacity style={styles.primaryBtn} onPress={goNext}>
          <Text style={styles.primaryBtnText}>Continue</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  // ======================================================================
  // SCREEN 9: Feature Showcase
  // ======================================================================
  const FEATURES = [
    { icon: 'moon-outline' as const, title: 'Night Mode Reader', desc: 'Easy on the eyes for late-night reading sessions' },
    { icon: 'bookmark-outline' as const, title: 'Bookmarks & Progress', desc: 'Never lose your place across any book' },
    { icon: 'analytics-outline' as const, title: 'Reading Tracker', desc: 'Track pages read, books completed, streaks' },
    { icon: 'cloud-download-outline' as const, title: 'Offline Reading', desc: 'Download books for reading anywhere' },
    { icon: 'color-palette-outline' as const, title: 'Multiple Themes', desc: 'Night, Sepia, and Day reading themes' },
  ];

  const renderFeatureShowcase = () => (
    <View style={styles.screenContainer}>
      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        <Text style={styles.screenTitle}>A beautiful reading{'\n'}experience</Text>
        <Text style={styles.screenSubtitle}>Designed for deep, focused reading</Text>

        {/* Mini reader mock */}
        <View style={styles.miniReader}>
          <View style={styles.miniReaderInner}>
            <Text style={styles.miniReaderText}>
              The lips of wisdom are closed, except to the ears of Understanding.
            </Text>
            <Text style={styles.miniReaderAttr}>-- The Kybalion</Text>
          </View>
        </View>

        <View style={styles.featureList}>
          {FEATURES.map((f, i) => (
            <View key={i} style={styles.featureRow}>
              <View style={styles.featureIconCircle}>
                <Ionicons name={f.icon} size={20} color={colors.accent} />
              </View>
              <View style={styles.featureInfo}>
                <Text style={styles.featureTitle}>{f.title}</Text>
                <Text style={styles.featureDesc}>{f.desc}</Text>
              </View>
            </View>
          ))}
        </View>
      </ScrollView>
      <View style={styles.bottomActions}>
        <TouchableOpacity style={styles.primaryBtn} onPress={goNext}>
          <Text style={styles.primaryBtnText}>Continue</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  // ======================================================================
  // SCREEN 10: Notification Permission
  // ======================================================================
  const renderNotifPermission = () => (
    <View style={styles.screenContainer}>
      <View style={styles.centeredContent}>
        <View style={styles.notifIconWrap}>
          <Ionicons name="notifications" size={48} color={colors.accent} />
        </View>
        <Text style={styles.screenTitle}>Get daily reading{'\n'}reminders</Text>
        <Text style={styles.screenSubtitle}>
          We'll send a gentle nudge at your preferred time so you never miss your reading session.
        </Text>
        <View style={styles.notifPreview}>
          <View style={styles.notifPreviewCard}>
            <Ionicons name="library" size={18} color={colors.accent} />
            <View style={{ flex: 1, marginLeft: 10 }}>
              <Text style={styles.notifPreviewTitle}>Time to read</Text>
              <Text style={styles.notifPreviewBody}>Your daily 30 minutes with Meditations awaits.</Text>
            </View>
          </View>
        </View>
      </View>
      <View style={styles.bottomActions}>
        <TouchableOpacity
          style={styles.primaryBtn}
          onPress={() => { setNotifGranted(true); goNext(); }}
        >
          <Text style={styles.primaryBtnText}>Enable Reminders</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.skipBtn} onPress={goNext}>
          <Text style={styles.skipBtnText}>Maybe Later</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  // ======================================================================
  // SCREEN 11: Plan Ready
  // ======================================================================
  const renderPlanReady = () => {
    const firstBook = recommendedBooks.length > 0 ? recommendedBooks[0] : null;
    return (
      <View style={styles.screenContainer}>
        <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
          <View style={styles.planReadyBadge}>
            <Ionicons name="checkmark-circle" size={48} color={colors.success} />
          </View>
          <Text style={styles.screenTitle}>Your reading journey{'\n'}is ready!</Text>

          <View style={styles.planSummaryCard}>
            {firstBook && (
              <View style={styles.planSummaryRow}>
                <Ionicons name="book" size={18} color={colors.accent} />
                <View style={{ flex: 1, marginLeft: 12 }}>
                  <Text style={styles.planSummaryLabel}>First book</Text>
                  <Text style={styles.planSummaryValue}>{firstBook.title}</Text>
                </View>
              </View>
            )}
            <View style={styles.planSummaryDivider} />
            <View style={styles.planSummaryRow}>
              <Ionicons name="time" size={18} color={colors.accent} />
              <View style={{ flex: 1, marginLeft: 12 }}>
                <Text style={styles.planSummaryLabel}>Daily goal</Text>
                <Text style={styles.planSummaryValue}>{dailyTime || '30'} minutes per day</Text>
              </View>
            </View>
            <View style={styles.planSummaryDivider} />
            <View style={styles.planSummaryRow}>
              <Ionicons name="trophy" size={18} color={colors.accent} />
              <View style={{ flex: 1, marginLeft: 12 }}>
                <Text style={styles.planSummaryLabel}>Projected this year</Text>
                <Text style={styles.planSummaryValue}>{projection.booksPerYear} books completed</Text>
              </View>
            </View>
            <View style={styles.planSummaryDivider} />
            <View style={styles.planSummaryRow}>
              <Ionicons name="grid" size={18} color={colors.accent} />
              <View style={{ flex: 1, marginLeft: 12 }}>
                <Text style={styles.planSummaryLabel}>Genres selected</Text>
                <Text style={styles.planSummaryValue}>
                  {selectedGenres.map(g => GENRE_MAP[g]?.label).join(', ') || 'All genres'}
                </Text>
              </View>
            </View>
          </View>
        </ScrollView>
        <View style={styles.bottomActions}>
          <TouchableOpacity style={styles.primaryBtn} onPress={goNext}>
            <Text style={styles.primaryBtnText}>Unlock My Library</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  };

  // ======================================================================
  // SCREEN 12: Paywall
  // ======================================================================
  const renderPaywall = () => {
    if (showRescue) {
      return renderRescueOffer();
    }

    return (
      <View style={styles.screenContainer}>
        <ScrollView contentContainerStyle={styles.paywallScroll} showsVerticalScrollIndicator={false}>
          {/* Trial Timeline */}
          <View style={styles.trialTimeline}>
            <View style={styles.timelineStep}>
              <View style={[styles.timelineDot, styles.timelineDotActive]} />
              <Text style={styles.timelineLabel}>Today</Text>
              <Text style={styles.timelineDesc}>Free access</Text>
            </View>
            <View style={styles.timelineLine} />
            <View style={styles.timelineStep}>
              <View style={styles.timelineDot} />
              <Text style={styles.timelineLabel}>Day 2</Text>
              <Text style={styles.timelineDesc}>Reminder</Text>
            </View>
            <View style={styles.timelineLine} />
            <View style={styles.timelineStep}>
              <View style={styles.timelineDot} />
              <Text style={styles.timelineLabel}>Day 3</Text>
              <Text style={styles.timelineDesc}>Billing starts</Text>
            </View>
          </View>

          <Text style={styles.noPaymentText}>No payment due now</Text>

          {/* Free tier note */}
          <View style={styles.freeTierNote}>
            <Text style={styles.freeTierNoteTitle}>Free plan includes:</Text>
            <Text style={styles.freeTierNoteText}>10 books, night theme only</Text>
          </View>

          {/* Plan: Monthly (anchor) */}
          <TouchableOpacity
            style={[styles.planCard, selectedPlan === 'monthly' && styles.planCardSelected]}
            onPress={() => setSelectedPlan('monthly')}
            activeOpacity={0.7}
          >
            <View style={styles.planRadio}>
              <View style={[styles.planRadioInner, selectedPlan === 'monthly' && styles.planRadioActive]} />
            </View>
            <View style={styles.planCardInfo}>
              <Text style={[styles.planCardName, selectedPlan === 'monthly' && styles.planCardNameActive]}>Monthly</Text>
              <Text style={[styles.planCardPrice, selectedPlan === 'monthly' && styles.planCardPriceActive]}>
                {monthlyPackage?.product?.priceString ?? '$3.99/month'}
              </Text>
            </View>
          </TouchableOpacity>

          {/* Plan: Annual (best value) */}
          <TouchableOpacity
            style={[styles.planCard, styles.planCardBest, selectedPlan === 'annual' && styles.planCardSelected]}
            onPress={() => setSelectedPlan('annual')}
            activeOpacity={0.7}
          >
            <View style={styles.bestValueBadge}>
              <Text style={styles.bestValueBadgeText}>BEST VALUE</Text>
            </View>
            <View style={styles.planRadio}>
              <View style={[styles.planRadioInner, selectedPlan === 'annual' && styles.planRadioActive]} />
            </View>
            <View style={styles.planCardInfo}>
              <View style={styles.planCardNameRow}>
                <Text style={[styles.planCardName, selectedPlan === 'annual' && styles.planCardNameActive]}>Annual</Text>
                <View style={styles.saveBadge}>
                  <Text style={styles.saveBadgeText}>Save 83%</Text>
                </View>
              </View>
              <Text style={[styles.planCardPrice, selectedPlan === 'annual' && styles.planCardPriceActive]}>
                {annualPackage?.product?.priceString ?? '$9.99/year'}
              </Text>
              <Text style={styles.planCardDetail}>$0.83/month after free trial</Text>
            </View>
          </TouchableOpacity>

          {/* Benefits */}
          <View style={styles.benefitsList}>
            <Text style={styles.benefitsTitle}>Premium includes:</Text>
            {[
              'Full 50+ book library',
              'All reader themes (Night, Sepia, Day)',
              'Personalized reading plans',
              'Offline downloads',
              'Bookmarks, highlights & notes',
            ].map((b, i) => (
              <View key={i} style={styles.benefitRow}>
                <Ionicons name="checkmark-circle" size={16} color={colors.accent} />
                <Text style={styles.benefitText}>{b}</Text>
              </View>
            ))}
          </View>

          {/* Social proof */}
          <View style={styles.paywallSocial}>
            <View style={styles.paywallStars}>
              {[1, 2, 3, 4, 5].map(i => (
                <Ionicons key={i} name="star" size={14} color={colors.accent} style={{ marginRight: 2 }} />
              ))}
            </View>
            <Text style={styles.paywallSocialText}>4.7 stars  |  8,000+ readers</Text>
          </View>
        </ScrollView>

        <View style={styles.bottomActions}>
          <TouchableOpacity
            style={[styles.primaryBtn, styles.premiumBtn, purchasing && styles.primaryBtnDisabled]}
            onPress={handlePurchase}
            disabled={purchasing || restoring}
          >
            {purchasing ? (
              <ActivityIndicator size="small" color={colors.background} />
            ) : (
              <Text style={styles.primaryBtnText}>Start My Free Trial</Text>
            )}
          </TouchableOpacity>

          <Text style={styles.cancelText}>Cancel anytime. No commitment.</Text>

          <TouchableOpacity style={styles.skipBtn} onPress={handleDeclinePaywall} disabled={purchasing || restoring}>
            <Text style={styles.skipBtnText}>Continue with Free</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.restoreBtn} onPress={handleRestore} disabled={purchasing || restoring}>
            {restoring ? (
              <ActivityIndicator size="small" color={colors.textMuted} />
            ) : (
              <Text style={styles.restoreBtnText}>Restore Purchases</Text>
            )}
          </TouchableOpacity>

          <Text style={styles.legalText}>
            3-day free trial, then {selectedPlan === 'annual' ? '$9.99/year' : '$3.99/month'}.{'\n'}Subscription automatically renews unless canceled at least 24 hours before the end of the current period. Manage subscriptions in your Apple ID account settings. Cancel anytime.
          </Text>
          <View style={styles.legalLinks}>
            <TouchableOpacity onPress={() => Linking.openURL(APP_CONFIG.PRIVACY_POLICY_URL)}>
              <Text style={styles.legalLinkText}>Privacy</Text>
            </TouchableOpacity>
            <Text style={styles.legalSep}>{'\u00B7'}</Text>
            <TouchableOpacity onPress={() => Linking.openURL(APP_CONFIG.TERMS_URL)}>
              <Text style={styles.legalLinkText}>Terms</Text>
            </TouchableOpacity>
            <Text style={styles.legalSep}>{'\u00B7'}</Text>
            <TouchableOpacity onPress={() => Linking.openURL(APP_CONFIG.SUPPORT_URL)}>
              <Text style={styles.legalLinkText}>Support</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    );
  };

  // ======================================================================
  // RESCUE OFFER (shown on decline)
  // ======================================================================
  const renderRescueOffer = () => (
    <View style={styles.screenContainer}>
      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        <View style={styles.rescueIconWrap}>
          <Ionicons name="gift-outline" size={48} color={colors.accent} />
        </View>
        <Text style={styles.screenTitle}>Wait! Special offer{'\n'}just for you</Text>
        <Text style={styles.screenSubtitle}>
          Get full access to all 156 texts at a special introductory price
        </Text>

        <View style={styles.rescueCard}>
          <Text style={styles.rescuePriceOld}>$9.99/year</Text>
          <Text style={styles.rescuePrice}>$6.99/year</Text>
          <Text style={styles.rescueSaving}>You save 30%</Text>
          <View style={styles.rescueDivider} />
          <Text style={styles.rescueDetail}>That's just $0.58/month for 156 classic texts</Text>
        </View>
      </ScrollView>
      <View style={styles.bottomActions}>
        <TouchableOpacity
          style={[styles.primaryBtn, styles.premiumBtn, purchasing && styles.primaryBtnDisabled]}
          onPress={handlePurchase}
          disabled={purchasing || restoring}
        >
          {purchasing ? (
            <ActivityIndicator size="small" color={colors.background} />
          ) : (
            <Text style={styles.primaryBtnText}>Claim This Offer</Text>
          )}
        </TouchableOpacity>
        <TouchableOpacity style={styles.skipBtn} onPress={handleFinish} disabled={purchasing}>
          <Text style={styles.skipBtnText}>No thanks, continue free</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  // ======================================================================
  // MAIN RENDER
  // ======================================================================
  const renderStep = () => {
    switch (step) {
      case 0: return renderWelcome();
      case 1: return renderReadingGoal();
      case 2: return renderGenres();
      case 3: return renderReadingSpeed();
      case 4: return renderDailyTime();
      case 5: return renderValidation();
      case 6: return renderBookPreview();
      case 7: return renderSocialProof();
      case 8: return renderFeatureShowcase();
      case 9: return renderNotifPermission();
      case 10: return renderPlanReady();
      case 11: return renderPaywall();
      default: return null;
    }
  };

  return (
    <SafeAreaView style={styles.screen} edges={['top', 'bottom']}>
      {renderProgressBar()}
      {renderHeader()}
      <Animated.View
        style={[
          styles.animatedContainer,
          { opacity: fadeAnim, transform: [{ translateY: slideAnim }] },
        ]}
      >
        {renderStep()}
      </Animated.View>
    </SafeAreaView>
  );
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

function getRecommendedBooks(cats: string[]): Book[] {
  if (cats.length === 0) return books.slice(0, 6);
  const uniqueCats = [...new Set(cats)];
  const result: Book[] = [];
  for (const cat of uniqueCats) {
    const catBooks = getBooksByCategory(cat);
    for (const b of catBooks) {
      if (!result.find(r => r.id === b.id)) {
        result.push(b);
      }
      if (result.length >= 6) break;
    }
    if (result.length >= 6) break;
  }
  // Fill remaining with popular picks if needed
  if (result.length < 6) {
    const popular = [
      books.find(b => b.title.includes('Meditations')),
      books.find(b => b.title.includes('Kybalion')),
      books.find(b => b.title.includes('Art of War')),
      books.find(b => b.title.includes('Republic')),
      books.find(b => b.title.includes('Tao Te Ching')),
      books.find(b => b.title.includes('Bhagavad')),
    ].filter(Boolean) as Book[];
    for (const p of popular) {
      if (!result.find(r => r.id === p.id)) {
        result.push(p);
      }
      if (result.length >= 6) break;
    }
  }
  return result;
}

function getReadingProjection(speed: string, time: string): { booksPerYear: number; pagesPerDay: number; daysPerBook: number } {
  // Pages per minute by speed
  const ppm = speed === 'fast' ? 1.5 : speed === 'regular' ? 1.0 : 0.7;
  const minutes = parseInt(time, 10) || 30;
  const pagesPerDay = Math.round(ppm * minutes);
  const avgBookPages = 200; // average classic text length
  const daysPerBook = Math.max(1, Math.round(avgBookPages / pagesPerDay));
  const booksPerYear = Math.min(156, Math.round(365 / daysPerBook));
  return { booksPerYear, pagesPerDay, daysPerBook };
}

// ============================================================================
// STYLES
// ============================================================================

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: colors.background,
  },
  animatedContainer: {
    flex: 1,
  },
  screenContainer: {
    flex: 1,
    justifyContent: 'space-between',
  },

  // ---- Progress Bar ----
  progressBarContainer: {
    height: 3,
    backgroundColor: colors.surfaceBorder,
    marginHorizontal: spacing.xl,
    borderRadius: 2,
    marginTop: spacing.sm,
  },
  progressBarFill: {
    height: 3,
    backgroundColor: colors.accent,
    borderRadius: 2,
  },

  // ---- Header ----
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.sm,
    height: 44,
  },
  backBtn: {
    width: 36,
    height: 36,
    alignItems: 'center',
    justifyContent: 'center',
  },
  backPlaceholder: {
    width: 36,
    height: 36,
  },
  stepCounter: {
    ...fonts.sansRegular,
    fontSize: 13,
    color: colors.textMuted,
  },

  // ---- Scroll Content ----
  scrollContent: {
    paddingHorizontal: spacing.xl,
    paddingTop: 16,
    paddingBottom: 20,
  },

  // ---- Centered Content ----
  centeredContent: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 32,
  },

  // ---- Screen titles ----
  screenTitle: {
    ...fonts.serifBold,
    fontSize: 26,
    color: colors.parchment,
    textAlign: 'center',
    lineHeight: 34,
    marginBottom: 8,
  },
  screenSubtitle: {
    ...fonts.sansRegular,
    fontSize: 14,
    color: colors.textSecondary,
    textAlign: 'center',
    lineHeight: 22,
    marginBottom: 24,
  },

  // ---- Welcome ----
  bookStackIllustration: {
    width: 120,
    height: 80,
    alignItems: 'center',
    justifyContent: 'flex-end',
    marginBottom: 12,
  },
  stackBook: {
    position: 'absolute',
    backgroundColor: colors.surface,
    borderRadius: 4,
    borderWidth: 1,
    borderColor: colors.surfaceBorder,
    alignItems: 'center',
    justifyContent: 'center',
  },
  stackBook1: {
    width: 50,
    height: 18,
    bottom: 0,
    transform: [{ rotate: '-5deg' }],
  },
  stackBook2: {
    width: 56,
    height: 20,
    bottom: 16,
    transform: [{ rotate: '3deg' }],
  },
  stackBook3: {
    width: 60,
    height: 22,
    bottom: 34,
    transform: [{ rotate: '-2deg' }],
  },
  stackGlow: {
    position: 'absolute',
    bottom: 10,
    width: 80,
    height: 40,
    borderRadius: 40,
    backgroundColor: colors.accentGlow,
  },
  welcomeIconContainer: {
    width: 100,
    height: 100,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20,
  },
  welcomeIconRing: {
    position: 'absolute',
    width: 100,
    height: 100,
    borderRadius: 50,
    borderWidth: 1,
    borderColor: 'rgba(201, 169, 110, 0.2)',
  },
  welcomeTitle: {
    ...fonts.serifBold,
    fontSize: 30,
    color: colors.parchment,
    textAlign: 'center',
    lineHeight: 40,
  },
  ornamentRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 14,
  },
  ornamentDash: {
    width: 24,
    height: 1,
    backgroundColor: colors.accent,
    opacity: 0.4,
  },
  welcomeSubtitle: {
    ...fonts.sansRegular,
    fontSize: 15,
    color: colors.textSecondary,
    textAlign: 'center',
    lineHeight: 24,
  },

  // ---- Bottom Actions ----
  bottomActions: {
    paddingHorizontal: spacing.xl,
    paddingBottom: Platform.OS === 'ios' ? 8 : 20,
  },
  primaryBtn: {
    backgroundColor: colors.accent,
    borderRadius: borderRadius.md,
    paddingVertical: 16,
    alignItems: 'center',
    minHeight: 52,
    justifyContent: 'center',
  },
  primaryBtnDisabled: {
    backgroundColor: colors.surfaceBorder,
  },
  primaryBtnText: {
    ...fonts.sansBold,
    fontSize: 16,
    color: colors.background,
  },
  premiumBtn: {
    backgroundColor: colors.accent,
  },
  skipBtn: {
    paddingVertical: 12,
    alignItems: 'center',
    minHeight: 40,
    justifyContent: 'center',
  },
  skipBtnText: {
    ...fonts.sansRegular,
    fontSize: 15,
    color: colors.textSecondary,
  },

  // ---- Option Cards (goals, speed, time) ----
  optionsList: {
    gap: 12,
  },
  optionCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    borderWidth: 1.5,
    borderColor: colors.surfaceBorder,
    padding: spacing.lg,
  },
  optionCardSelected: {
    borderColor: colors.accent,
    backgroundColor: 'rgba(201, 169, 110, 0.06)',
  },
  optionIconWrap: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: colors.surfaceLight,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 14,
  },
  optionIconWrapSelected: {
    backgroundColor: 'rgba(201, 169, 110, 0.12)',
  },
  optionLabel: {
    ...fonts.sansBold,
    fontSize: 15,
    color: colors.textSecondary,
    flex: 1,
  },
  optionLabelSelected: {
    color: colors.parchment,
  },
  optionDesc: {
    ...fonts.sansRegular,
    fontSize: 12,
    color: colors.textMuted,
    marginTop: 2,
  },
  radioOuter: {
    width: 22,
    height: 22,
    borderRadius: 11,
    borderWidth: 2,
    borderColor: colors.surfaceBorder,
    alignItems: 'center',
    justifyContent: 'center',
    marginLeft: 10,
  },
  radioOuterSelected: {
    borderColor: colors.accent,
  },
  radioInner: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: colors.accent,
  },

  // ---- Genre Grid ----
  genreGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    gap: 10,
  },
  genreChip: {
    width: (SCREEN_WIDTH - 60) / 2,
    backgroundColor: colors.surface,
    borderRadius: borderRadius.md,
    borderWidth: 1.5,
    borderColor: colors.surfaceBorder,
    paddingVertical: 18,
    paddingHorizontal: 12,
    alignItems: 'center',
  },
  genreChipSelected: {
    borderColor: colors.accent,
    backgroundColor: 'rgba(201, 169, 110, 0.08)',
  },
  genreChipLabel: {
    ...fonts.sansBold,
    fontSize: 13,
    color: colors.textSecondary,
    textAlign: 'center',
  },
  genreChipLabelSelected: {
    color: colors.parchment,
  },

  // ---- Validation / Projection ----
  validationBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
  },
  validationBadgeText: {
    ...fonts.sansBold,
    fontSize: 14,
    color: colors.success,
    marginLeft: 8,
  },
  projectionNumber: {
    ...fonts.serifBold,
    fontSize: 48,
    color: colors.accent,
    textAlign: 'center',
    lineHeight: 56,
  },
  chartContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'flex-end',
    height: 160,
    marginTop: 28,
    marginBottom: 28,
    paddingHorizontal: 10,
  },
  chartBarWrap: {
    alignItems: 'center',
    flex: 1,
  },
  chartBarCount: {
    ...fonts.sansBold,
    fontSize: 12,
    color: colors.accent,
    marginBottom: 6,
  },
  chartBarTrack: {
    width: 28,
    height: 100,
    backgroundColor: colors.surface,
    borderRadius: 6,
    overflow: 'hidden',
    justifyContent: 'flex-end',
  },
  chartBarFill: {
    backgroundColor: colors.accent,
    borderRadius: 6,
    minHeight: 4,
  },
  chartBarLabel: {
    ...fonts.sansRegular,
    fontSize: 11,
    color: colors.textMuted,
    marginTop: 6,
  },
  projectionDetails: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    gap: 14,
    borderWidth: 1,
    borderColor: colors.surfaceBorder,
  },
  projectionRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  projectionText: {
    ...fonts.sansRegular,
    fontSize: 14,
    color: colors.textPrimary,
    marginLeft: 12,
  },

  // ---- Book Grid ----
  bookGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
  },
  bookGridItem: {
    marginBottom: 4,
  },
  firstBookHighlight: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    borderWidth: 1,
    borderColor: colors.surfaceBorder,
    marginTop: 16,
  },
  firstBookLabel: {
    ...fonts.sansBold,
    fontSize: 11,
    color: colors.accent,
    letterSpacing: 1,
    textTransform: 'uppercase',
    marginBottom: 8,
  },
  firstBookTitle: {
    ...fonts.serifBold,
    fontSize: 18,
    color: colors.parchment,
    marginBottom: 4,
  },
  firstBookAuthor: {
    ...fonts.sansRegular,
    fontSize: 13,
    color: colors.textSecondary,
    marginBottom: 8,
  },
  firstBookDesc: {
    ...fonts.sansRegular,
    fontSize: 13,
    color: colors.textMuted,
    lineHeight: 20,
  },

  // ---- Social Proof ----
  socialBadge: {
    alignSelf: 'center',
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: 'rgba(201, 169, 110, 0.1)',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
  },
  starRowCenter: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
  },
  starRatingText: {
    ...fonts.sansRegular,
    fontSize: 14,
    color: colors.textSecondary,
    marginLeft: 10,
  },
  testimonialCard: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    borderWidth: 1,
    borderColor: colors.surfaceBorder,
    marginBottom: 12,
  },
  testimonialHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  testimonialAvatar: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: 'rgba(201, 169, 110, 0.15)',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 10,
  },
  testimonialAvatarText: {
    ...fonts.sansBold,
    fontSize: 14,
    color: colors.accent,
  },
  testimonialName: {
    ...fonts.sansBold,
    fontSize: 14,
    color: colors.textPrimary,
  },
  testimonialStars: {
    flexDirection: 'row',
    marginTop: 2,
  },
  testimonialText: {
    ...fonts.sansRegular,
    fontSize: 13,
    color: colors.textSecondary,
    lineHeight: 20,
  },

  // ---- Feature Showcase ----
  miniReader: {
    backgroundColor: '#0D0D1A',
    borderRadius: borderRadius.lg,
    borderWidth: 1,
    borderColor: colors.surfaceBorder,
    marginBottom: 24,
    overflow: 'hidden',
  },
  miniReaderInner: {
    padding: 20,
  },
  miniReaderText: {
    fontFamily: 'Georgia',
    fontSize: 16,
    lineHeight: 28,
    color: '#C8C0B0',
  },
  miniReaderAttr: {
    fontFamily: 'Georgia',
    fontStyle: 'italic',
    fontSize: 12,
    color: colors.accent,
    textAlign: 'right',
    marginTop: 10,
  },
  featureList: {
    gap: 16,
  },
  featureRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  featureIconCircle: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.surfaceBorder,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 14,
  },
  featureInfo: {
    flex: 1,
  },
  featureTitle: {
    ...fonts.sansBold,
    fontSize: 15,
    color: colors.textPrimary,
  },
  featureDesc: {
    ...fonts.sansRegular,
    fontSize: 13,
    color: colors.textSecondary,
    marginTop: 2,
  },

  // ---- Notification Permission ----
  notifIconWrap: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: 'rgba(201, 169, 110, 0.1)',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20,
  },
  notifPreview: {
    marginTop: 28,
    width: '100%',
  },
  notifPreviewCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    borderWidth: 1,
    borderColor: colors.surfaceBorder,
  },
  notifPreviewTitle: {
    ...fonts.sansBold,
    fontSize: 14,
    color: colors.textPrimary,
  },
  notifPreviewBody: {
    ...fonts.sansRegular,
    fontSize: 12,
    color: colors.textSecondary,
    marginTop: 2,
  },

  // ---- Plan Ready ----
  planReadyBadge: {
    alignSelf: 'center',
    marginBottom: 16,
  },
  planSummaryCard: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.xl,
    borderWidth: 1,
    borderColor: colors.surfaceBorder,
    marginTop: 8,
  },
  planSummaryRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
  },
  planSummaryDivider: {
    height: 1,
    backgroundColor: colors.surfaceBorder,
  },
  planSummaryLabel: {
    ...fonts.sansRegular,
    fontSize: 12,
    color: colors.textMuted,
  },
  planSummaryValue: {
    ...fonts.sansBold,
    fontSize: 15,
    color: colors.parchment,
    marginTop: 2,
  },

  // ---- Paywall ----
  paywallScroll: {
    paddingHorizontal: spacing.xl,
    paddingTop: 8,
    paddingBottom: 12,
  },
  trialTimeline: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
    paddingVertical: 12,
  },
  timelineStep: {
    alignItems: 'center',
    width: 80,
  },
  timelineDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: colors.surfaceBorder,
    marginBottom: 6,
  },
  timelineDotActive: {
    backgroundColor: colors.accent,
  },
  timelineLine: {
    flex: 1,
    height: 2,
    backgroundColor: colors.surfaceBorder,
    marginBottom: 20,
    maxWidth: 40,
  },
  timelineLabel: {
    ...fonts.sansBold,
    fontSize: 12,
    color: colors.textPrimary,
  },
  timelineDesc: {
    ...fonts.sansRegular,
    fontSize: 11,
    color: colors.textMuted,
    marginTop: 2,
  },
  noPaymentText: {
    ...fonts.sansBold,
    fontSize: 16,
    color: colors.success,
    textAlign: 'center',
    marginBottom: 16,
  },
  freeTierNote: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.md,
    padding: spacing.md,
    borderWidth: 1,
    borderColor: colors.surfaceBorder,
    marginBottom: 16,
    flexDirection: 'row',
    alignItems: 'center',
  },
  freeTierNoteTitle: {
    ...fonts.sansBold,
    fontSize: 12,
    color: colors.textSecondary,
    marginRight: 6,
  },
  freeTierNoteText: {
    ...fonts.sansRegular,
    fontSize: 12,
    color: colors.textMuted,
  },

  // Plan cards
  planCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    borderWidth: 1.5,
    borderColor: colors.surfaceBorder,
    padding: spacing.lg,
    marginBottom: spacing.md,
  },
  planCardBest: {
    borderColor: colors.accentDim,
    position: 'relative',
    paddingTop: spacing.xl,
  },
  planCardSelected: {
    borderColor: colors.accent,
    backgroundColor: 'rgba(201, 169, 110, 0.06)',
  },
  bestValueBadge: {
    position: 'absolute',
    top: -12,
    alignSelf: 'center',
    left: '50%',
    marginLeft: -45,
    backgroundColor: colors.accent,
    borderRadius: borderRadius.round,
    paddingHorizontal: 14,
    paddingVertical: 4,
  },
  bestValueBadgeText: {
    ...fonts.sansBold,
    fontSize: 11,
    color: colors.background,
    letterSpacing: 0.8,
  },
  planRadio: {
    width: 22,
    height: 22,
    borderRadius: 11,
    borderWidth: 2,
    borderColor: colors.surfaceBorder,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: spacing.md,
  },
  planRadioInner: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: 'transparent',
  },
  planRadioActive: {
    backgroundColor: colors.accent,
  },
  planCardInfo: {
    flex: 1,
  },
  planCardNameRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  planCardName: {
    ...fonts.sansBold,
    fontSize: 16,
    color: colors.textSecondary,
  },
  planCardNameActive: {
    color: colors.parchment,
  },
  planCardPrice: {
    ...fonts.serifBold,
    fontSize: 18,
    color: colors.textSecondary,
    marginTop: 2,
  },
  planCardPriceActive: {
    color: colors.accent,
  },
  planCardDetail: {
    ...fonts.sansRegular,
    fontSize: 12,
    color: colors.textMuted,
    marginTop: 2,
  },
  saveBadge: {
    backgroundColor: colors.accent,
    borderRadius: borderRadius.round,
    paddingHorizontal: 8,
    paddingVertical: 2,
    marginLeft: 8,
  },
  saveBadgeText: {
    ...fonts.sansBold,
    fontSize: 10,
    color: colors.background,
    letterSpacing: 0.5,
  },

  // Benefits
  benefitsList: {
    marginTop: spacing.lg,
    gap: spacing.sm,
  },
  benefitsTitle: {
    ...fonts.sansBold,
    fontSize: 14,
    color: colors.textPrimary,
    marginBottom: spacing.xs,
  },
  benefitRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  benefitText: {
    ...fonts.sansRegular,
    fontSize: 14,
    color: colors.parchment,
    marginLeft: 10,
    flex: 1,
  },

  // Social on paywall
  paywallSocial: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: spacing.xl,
    marginBottom: spacing.sm,
  },
  paywallStars: {
    flexDirection: 'row',
    marginRight: 8,
  },
  paywallSocialText: {
    ...fonts.sansRegular,
    fontSize: 13,
    color: colors.textSecondary,
  },

  // Cancel text
  cancelText: {
    ...fonts.sansRegular,
    fontSize: 13,
    color: colors.textSecondary,
    textAlign: 'center',
    marginTop: 8,
    marginBottom: 4,
  },

  // Restore
  restoreBtn: {
    paddingVertical: 6,
    alignItems: 'center',
    minHeight: 32,
    justifyContent: 'center',
  },
  restoreBtnText: {
    ...fonts.sansRegular,
    fontSize: 13,
    color: colors.textMuted,
    textDecorationLine: 'underline',
  },

  // Legal
  legalText: {
    ...fonts.sansLight,
    fontSize: 11,
    color: colors.textMuted,
    textAlign: 'center',
    marginTop: 4,
    lineHeight: 16,
  },
  legalLinks: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 6,
  },
  legalLinkText: {
    ...fonts.sansRegular,
    fontSize: 11,
    color: colors.textMuted,
    textDecorationLine: 'underline',
  },
  legalSep: {
    fontSize: 11,
    color: colors.textMuted,
    marginHorizontal: 8,
  },

  // ---- Rescue Offer ----
  rescueIconWrap: {
    alignSelf: 'center',
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: 'rgba(201, 169, 110, 0.1)',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
  },
  rescueCard: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    borderWidth: 2,
    borderColor: colors.accent,
    padding: spacing.xl,
    alignItems: 'center',
    marginTop: 8,
  },
  rescuePriceOld: {
    ...fonts.sansRegular,
    fontSize: 16,
    color: colors.textMuted,
    textDecorationLine: 'line-through',
    marginBottom: 4,
  },
  rescuePrice: {
    ...fonts.serifBold,
    fontSize: 36,
    color: colors.accent,
    marginBottom: 4,
  },
  rescueSaving: {
    ...fonts.sansBold,
    fontSize: 14,
    color: colors.success,
    marginBottom: 12,
  },
  rescueDivider: {
    width: 40,
    height: 1,
    backgroundColor: colors.surfaceBorder,
    marginBottom: 12,
  },
  rescueDetail: {
    ...fonts.sansRegular,
    fontSize: 13,
    color: colors.textSecondary,
    textAlign: 'center',
  },
});
