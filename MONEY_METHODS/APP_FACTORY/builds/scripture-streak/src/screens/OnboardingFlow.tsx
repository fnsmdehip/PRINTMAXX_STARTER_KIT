import React, { useState, useRef, useCallback, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Animated,
  Dimensions,
  TouchableOpacity,
  Platform,
  Linking,
  ScrollView,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Colors, Spacing, BorderRadius } from '../constants/theme';
import { StorageService } from '../services/storage';
import { NotificationService } from '../services/notifications';
import { getOfferings, purchasePackage, restorePurchases } from '../services/purchases';
import { playSound } from '../sounds/SoundEngine';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');
const TOTAL_STEPS = 12;

const ONBOARDING_COMPLETE_KEY = '@ss_onboarding_v2_complete';
const ONBOARDING_ANSWERS_KEY = '@ss_onboarding_v2_answers';

const PRIVACY_URL = 'https://printmaxx-privacy.surge.sh';
const TERMS_URL = 'https://printmaxx-tos.surge.sh';

// ── Data for selection screens ──

const GOALS = [
  { id: 'deepen', label: 'Deepen my faith', icon: 'heart-outline' as const, desc: 'Grow closer to God through His Word' },
  { id: 'habit', label: 'Build a daily habit', icon: 'flame-outline' as const, desc: 'Make Scripture part of every day' },
  { id: 'whole', label: 'Read the whole Bible', icon: 'book-outline' as const, desc: 'Cover Genesis to Revelation' },
  { id: 'peace', label: 'Find peace & comfort', icon: 'leaf-outline' as const, desc: 'Let God\'s promises calm your heart' },
];

const EXPERIENCE_LEVELS = [
  { id: 'new', label: 'New to the Bible', icon: 'sparkles-outline' as const, desc: 'Just getting started' },
  { id: 'some', label: 'Read some passages', icon: 'layers-outline' as const, desc: 'Familiar with key stories' },
  { id: 'regular', label: 'Read regularly', icon: 'library-outline' as const, desc: 'Have a reading practice' },
  { id: 'deep', label: 'Know it well', icon: 'school-outline' as const, desc: 'Years of study' },
];

const FREQUENCIES = [
  { id: 'daily', label: 'Every day', days: 7, icon: 'sunny-outline' as const },
  { id: '5x', label: '5 days / week', days: 5, icon: 'calendar-outline' as const },
  { id: '3x', label: '3 days / week', days: 3, icon: 'time-outline' as const },
];

const TIMES = [
  { id: 'morning', label: 'Morning', icon: 'sunny-outline' as const, time: '07:00', desc: 'Start your day with Scripture' },
  { id: 'afternoon', label: 'Afternoon', icon: 'partly-sunny-outline' as const, time: '12:00', desc: 'A midday moment of peace' },
  { id: 'evening', label: 'Evening', icon: 'moon-outline' as const, time: '18:00', desc: 'Wind down with God\'s Word' },
  { id: 'bed', label: 'Before bed', icon: 'bed-outline' as const, time: '21:00', desc: 'End the day in faith' },
];

const DURATIONS = [
  { id: '5', label: '5 min', minutes: 5, desc: 'Quick and focused' },
  { id: '10', label: '10 min', minutes: 10, desc: 'Steady and thoughtful' },
  { id: '15', label: '15 min', minutes: 15, desc: 'Deep and meaningful' },
  { id: '20', label: '20+ min', minutes: 20, desc: 'Immersive study' },
];

const TESTIMONIALS = [
  { name: 'Sarah M.', text: 'I\'ve never been so consistent with my Bible reading. 90 days and counting!', streak: 90 },
  { name: 'James K.', text: 'The daily reminders keep me accountable. My faith has grown so much.', streak: 45 },
  { name: 'Maria L.', text: 'I love how it tracks my progress. Makes reading feel achievable.', streak: 120 },
];

const FEATURES_SHOWCASE = [
  { icon: 'flame-outline' as const, title: 'Streak Tracking', desc: 'Stay motivated with daily streaks and milestone badges' },
  { icon: 'book-outline' as const, title: 'Daily Readings', desc: 'Curated verses with beautiful typography and context' },
  { icon: 'language-outline' as const, title: 'Multiple Translations', desc: 'NIV, ESV, KJV, NLT, and more at your fingertips' },
  { icon: 'map-outline' as const, title: 'Reading Plans', desc: 'Guided journeys through books of the Bible' },
];

// ── Types ──

interface OnboardingAnswers {
  goal: string;
  experience: string;
  frequency: string;
  time: string;
  duration: string;
}

interface OnboardingFlowProps {
  onComplete: () => void;
}

// ── Helper: compute projected reading completion ──

function computeProjection(answers: OnboardingAnswers): { chapters: number; days: number; milestone: string } {
  const daysPerWeek = answers.frequency === 'daily' ? 7 : answers.frequency === '5x' ? 5 : 3;
  const minutesPerSession = parseInt(answers.duration) || 10;
  // Average Bible chapter takes ~4 minutes to read
  const chaptersPerSession = Math.max(1, Math.round(minutesPerSession / 4));
  const chaptersPerWeek = chaptersPerSession * daysPerWeek;
  // Bible has 1,189 chapters total
  const totalChapters = 1189;
  const weeksToComplete = Math.ceil(totalChapters / chaptersPerWeek);
  const daysToComplete = weeksToComplete * 7;

  let milestone = 'the entire Bible';
  if (answers.goal === 'peace') {
    milestone = 'Psalms & Proverbs';
    return { chapters: 181, days: Math.ceil(181 / chaptersPerSession / daysPerWeek * 7), milestone };
  }
  if (answers.goal === 'whole') {
    return { chapters: totalChapters, days: daysToComplete, milestone };
  }
  // For deepening faith or building habit, show New Testament (260 chapters)
  const ntChapters = 260;
  return {
    chapters: ntChapters,
    days: Math.ceil(ntChapters / chaptersPerSession / daysPerWeek * 7),
    milestone: 'the New Testament',
  };
}

// ── Main Component ──

export function OnboardingFlow({ onComplete }: OnboardingFlowProps) {
  const insets = useSafeAreaInsets();
  const [step, setStep] = useState(0);
  const slideAnim = useRef(new Animated.Value(0)).current;
  const fadeAnim = useRef(new Animated.Value(1)).current;
  const progressAnim = useRef(new Animated.Value(0)).current;

  // Paywall state
  const [selectedPlan, setSelectedPlan] = useState<'yearly' | 'monthly'>('yearly');
  const [isPurchasing, setIsPurchasing] = useState(false);
  const [showRescue, setShowRescue] = useState(false);

  const [answers, setAnswers] = useState<OnboardingAnswers>({
    goal: '',
    experience: '',
    frequency: 'daily',
    time: 'morning',
    duration: '10',
  });

  // Animate progress bar
  useEffect(() => {
    Animated.timing(progressAnim, {
      toValue: (step + 1) / TOTAL_STEPS,
      duration: 300,
      useNativeDriver: false,
    }).start();
  }, [step]);

  const animateToStep = useCallback((nextStep: number) => {
    const forward = nextStep > step;
    // Fade out
    Animated.timing(fadeAnim, {
      toValue: 0,
      duration: 150,
      useNativeDriver: true,
    }).start(() => {
      setStep(nextStep);
      // Slide in from direction
      slideAnim.setValue(forward ? 60 : -60);
      Animated.parallel([
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 250,
          useNativeDriver: true,
        }),
        Animated.timing(slideAnim, {
          toValue: 0,
          duration: 250,
          useNativeDriver: true,
        }),
      ]).start();
    });
  }, [step, slideAnim, fadeAnim]);

  const goNext = useCallback(() => {
    if (step < TOTAL_STEPS - 1) {
      playSound('swipe');
      animateToStep(step + 1);
    }
  }, [step, animateToStep]);

  const goBack = useCallback(() => {
    if (showRescue) {
      setShowRescue(false);
      return;
    }
    if (step > 0) {
      playSound('swipe');
      animateToStep(step - 1);
    }
  }, [step, showRescue, animateToStep]);

  const updateAnswer = useCallback((key: keyof OnboardingAnswers, value: string) => {
    playSound('toggle');
    setAnswers(prev => ({ ...prev, [key]: value }));
  }, []);

  const saveAndComplete = useCallback(async () => {
    try {
      playSound('success');
      await AsyncStorage.setItem(ONBOARDING_COMPLETE_KEY, 'true');
      await AsyncStorage.setItem(ONBOARDING_ANSWERS_KEY, JSON.stringify(answers));
      // Save settings based on answers
      const timeOption = TIMES.find(t => t.id === answers.time);
      await StorageService.completeOnboarding({
        completed: true,
        translation: 'NIV',
        dailyGoal: 'chapter',
        customGoalCount: Math.max(1, Math.round(parseInt(answers.duration) / 4)),
        notificationTime: timeOption?.time || '08:00',
        notificationsEnabled: true,
      });
    } catch {
      // continue anyway
    }
    onComplete();
  }, [answers, onComplete]);

  const handlePurchase = useCallback(async () => {
    try {
      setIsPurchasing(true);
      const offering = await getOfferings();
      if (!offering) {
        Alert.alert('Error', 'Unable to load subscription options. Please try again.');
        return;
      }
      const pkg = selectedPlan === 'yearly'
        ? offering.annual ?? offering.availablePackages[0]
        : offering.monthly ?? offering.availablePackages[0];
      if (!pkg) return;

      const customerInfo = await purchasePackage(pkg);
      if (customerInfo?.entitlements?.active?.['premium']) {
        const settings = await StorageService.getUserSettings();
        await StorageService.saveUserSettings({ ...settings, isPremium: true });
      }
      await saveAndComplete();
    } catch {
      // User cancelled
    } finally {
      setIsPurchasing(false);
    }
  }, [selectedPlan, saveAndComplete]);

  const handleDeclinePaywall = useCallback(() => {
    if (!showRescue) {
      setShowRescue(true);
    } else {
      // Declined rescue too, continue free
      saveAndComplete();
    }
  }, [showRescue, saveAndComplete]);

  const handleRestore = useCallback(async () => {
    try {
      setIsPurchasing(true);
      const restored = await restorePurchases();
      if (restored) {
        const settings = await StorageService.getUserSettings();
        await StorageService.saveUserSettings({ ...settings, isPremium: true });
        await saveAndComplete();
      } else {
        Alert.alert('No Purchase Found', 'No active subscription was found.');
      }
    } catch {
      Alert.alert('Error', 'Failed to restore purchases. Please try again.');
    } finally {
      setIsPurchasing(false);
    }
  }, [saveAndComplete]);

  const requestNotifications = useCallback(async () => {
    try {
      const granted = await NotificationService.requestPermissions();
      if (granted) {
        const timeOption = TIMES.find(t => t.id === answers.time);
        await NotificationService.scheduleDailyReminder(timeOption?.time || '08:00');
      }
    } catch {
      // silently continue
    }
    goNext();
  }, [answers.time, goNext]);

  // ── Screen canAdvance logic ──
  const canAdvance = useCallback((): boolean => {
    switch (step) {
      case 0: return true; // Welcome
      case 1: return answers.goal !== ''; // Goal
      case 2: return answers.experience !== ''; // Experience
      case 3: return true; // Frequency (has default)
      case 4: return true; // Time (has default)
      case 5: return true; // Duration (has default)
      case 6: return true; // Validation
      case 7: return true; // Social proof
      case 8: return true; // Features
      case 9: return true; // Notifications
      case 10: return true; // Plan Ready
      case 11: return true; // Paywall
      default: return true;
    }
  }, [step, answers]);

  // ── Skip logic: only non-critical screens ──
  const canSkip = useCallback((): boolean => {
    return step === 2 || step === 7 || step === 8; // Experience, Social Proof, Features
  }, [step]);

  // ── Projection data (computed once answers exist) ──
  const projection = computeProjection(answers);

  // ══════════════════════════════════════════
  // SCREEN 1: Welcome
  // ══════════════════════════════════════════
  const renderWelcome = () => (
    <View style={s.screenCenter}>
      {/* Cross icon */}
      <View style={s.welcomeGlow}>
        <Text style={s.welcomeCross}>{'\u271E'}</Text>
      </View>
      <Text style={s.heroTitle}>Your Daily Scripture{'\n'}Journey Starts Here</Text>
      <Text style={s.heroSub}>
        Build a life-changing habit of daily Bible reading with personalized plans, streak tracking, and daily inspiration.
      </Text>
      <View style={s.welcomeFeats}>
        {[
          { icon: 'flame-outline', text: 'Track your daily reading streak' },
          { icon: 'book-outline', text: 'Beautiful daily readings & plans' },
          { icon: 'notifications-outline', text: 'Gentle daily reminders' },
        ].map((f, i) => (
          <View key={i} style={s.welcomeFeatRow}>
            <View style={s.welcomeFeatIcon}>
              <Ionicons name={f.icon as any} size={20} color={Colors.gold} />
            </View>
            <Text style={s.welcomeFeatText}>{f.text}</Text>
          </View>
        ))}
      </View>
    </View>
  );

  // ══════════════════════════════════════════
  // SCREEN 2: Goal
  // ══════════════════════════════════════════
  const renderGoal = () => (
    <View style={s.screenPadded}>
      <Text style={s.screenTitle}>What's your spiritual goal?</Text>
      <Text style={s.screenSub}>This helps us personalize your reading journey.</Text>
      <View style={s.optionList}>
        {GOALS.map(g => (
          <TouchableOpacity
            key={g.id}
            style={[s.optionCard, answers.goal === g.id && s.optionCardActive]}
            onPress={() => { updateAnswer('goal', g.id); }}
            activeOpacity={0.7}
          >
            <View style={[s.optionIcon, answers.goal === g.id && s.optionIconActive]}>
              <Ionicons name={g.icon} size={24} color={answers.goal === g.id ? Colors.navy : Colors.gold} />
            </View>
            <View style={s.optionInfo}>
              <Text style={[s.optionLabel, answers.goal === g.id && s.optionLabelActive]}>{g.label}</Text>
              <Text style={s.optionDesc}>{g.desc}</Text>
            </View>
            <View style={[s.radio, answers.goal === g.id && s.radioActive]}>
              {answers.goal === g.id && <View style={s.radioDot} />}
            </View>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );

  // ══════════════════════════════════════════
  // SCREEN 3: Experience
  // ══════════════════════════════════════════
  const renderExperience = () => (
    <View style={s.screenPadded}>
      <Text style={s.screenTitle}>How familiar are you{'\n'}with the Bible?</Text>
      <Text style={s.screenSub}>No wrong answers here. We meet you where you are.</Text>
      <View style={s.optionList}>
        {EXPERIENCE_LEVELS.map(e => (
          <TouchableOpacity
            key={e.id}
            style={[s.optionCard, answers.experience === e.id && s.optionCardActive]}
            onPress={() => { updateAnswer('experience', e.id); }}
            activeOpacity={0.7}
          >
            <View style={[s.optionIcon, answers.experience === e.id && s.optionIconActive]}>
              <Ionicons name={e.icon} size={24} color={answers.experience === e.id ? Colors.navy : Colors.gold} />
            </View>
            <View style={s.optionInfo}>
              <Text style={[s.optionLabel, answers.experience === e.id && s.optionLabelActive]}>{e.label}</Text>
              <Text style={s.optionDesc}>{e.desc}</Text>
            </View>
            <View style={[s.radio, answers.experience === e.id && s.radioActive]}>
              {answers.experience === e.id && <View style={s.radioDot} />}
            </View>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );

  // ══════════════════════════════════════════
  // SCREEN 4: Frequency
  // ══════════════════════════════════════════
  const renderFrequency = () => (
    <View style={s.screenPadded}>
      <Text style={s.screenTitle}>How often do you{'\n'}want to read?</Text>
      <Text style={s.screenSub}>Consistency matters more than quantity.</Text>
      <View style={s.optionList}>
        {FREQUENCIES.map(f => (
          <TouchableOpacity
            key={f.id}
            style={[s.optionCard, answers.frequency === f.id && s.optionCardActive]}
            onPress={() => { updateAnswer('frequency', f.id); }}
            activeOpacity={0.7}
          >
            <View style={[s.optionIcon, answers.frequency === f.id && s.optionIconActive]}>
              <Ionicons name={f.icon} size={24} color={answers.frequency === f.id ? Colors.navy : Colors.gold} />
            </View>
            <View style={s.optionInfo}>
              <Text style={[s.optionLabel, answers.frequency === f.id && s.optionLabelActive]}>{f.label}</Text>
              <Text style={s.optionDesc}>{f.days} days per week</Text>
            </View>
            <View style={[s.radio, answers.frequency === f.id && s.radioActive]}>
              {answers.frequency === f.id && <View style={s.radioDot} />}
            </View>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );

  // ══════════════════════════════════════════
  // SCREEN 5: Time of Day
  // ══════════════════════════════════════════
  const renderTime = () => (
    <View style={s.screenPadded}>
      <Text style={s.screenTitle}>When works best{'\n'}for you?</Text>
      <Text style={s.screenSub}>We'll send a gentle reminder at this time.</Text>
      <View style={s.timeGrid}>
        {TIMES.map(t => (
          <TouchableOpacity
            key={t.id}
            style={[s.timeCard, answers.time === t.id && s.timeCardActive]}
            onPress={() => { updateAnswer('time', t.id); }}
            activeOpacity={0.7}
          >
            <Ionicons
              name={t.icon}
              size={32}
              color={answers.time === t.id ? Colors.navy : Colors.gold}
              style={{ marginBottom: 8 }}
            />
            <Text style={[s.timeLabel, answers.time === t.id && s.timeLabelActive]}>{t.label}</Text>
            <Text style={[s.timeDesc, answers.time === t.id && s.timeDescActive]}>{t.desc}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );

  // ══════════════════════════════════════════
  // SCREEN 6: Duration
  // ══════════════════════════════════════════
  const renderDuration = () => (
    <View style={s.screenPadded}>
      <Text style={s.screenTitle}>How long per session?</Text>
      <Text style={s.screenSub}>Even 5 minutes a day can transform your faith.</Text>
      <View style={s.durationRow}>
        {DURATIONS.map(d => (
          <TouchableOpacity
            key={d.id}
            style={[s.durationCard, answers.duration === d.id && s.durationCardActive]}
            onPress={() => { updateAnswer('duration', d.id); }}
            activeOpacity={0.7}
          >
            <Text style={[s.durationNumber, answers.duration === d.id && s.durationNumberActive]}>{d.label}</Text>
            <Text style={[s.durationDesc, answers.duration === d.id && s.durationDescActive]}>{d.desc}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );

  // ══════════════════════════════════════════
  // SCREEN 7: Validation / Projection
  // ══════════════════════════════════════════
  const renderValidation = () => {
    const { chapters, days, milestone } = projection;
    const goalLabel = GOALS.find(g => g.id === answers.goal)?.label || 'your goal';
    const label = milestone || (answers.goal === 'whole' ? 'the entire Bible' : 'the New Testament');
    const months = Math.round(days / 30);

    // Progress graph bars
    const barHeights = [0.15, 0.25, 0.4, 0.55, 0.7, 0.85, 1.0];
    const barLabels = ['W1', 'W2', 'M1', 'M2', 'M3', months > 6 ? 'M6' : `M${months}`, 'Done'];

    return (
      <View style={s.screenCenter}>
        <View style={s.validationBadge}>
          <Ionicons name="checkmark-circle" size={20} color={Colors.navy} />
          <Text style={s.validationBadgeText}>YOUR PLAN IS ACHIEVABLE</Text>
        </View>
        <Text style={s.heroTitle}>Based on your answers...</Text>
        <View style={s.projectionCard}>
          <Text style={s.projectionHighlight}>You'll read through</Text>
          <Text style={s.projectionTarget}>{label}</Text>
          <Text style={s.projectionHighlight}>in approximately</Text>
          <Text style={s.projectionDays}>{months > 1 ? `${months} months` : `${days} days`}</Text>
          <Text style={s.projectionChapters}>{chapters} chapters total</Text>
        </View>

        {/* Visual progress graph */}
        <View style={s.graphContainer}>
          <View style={s.graphBars}>
            {barHeights.map((h, i) => (
              <View key={i} style={s.graphCol}>
                <View style={[s.graphBar, { height: h * 100 }]}>
                  <View style={[s.graphBarFill, i === barHeights.length - 1 && s.graphBarFillDone]} />
                </View>
                <Text style={s.graphLabel}>{barLabels[i]}</Text>
              </View>
            ))}
          </View>
          <Text style={s.graphCaption}>Your projected reading progress</Text>
        </View>
      </View>
    );
  };

  // ══════════════════════════════════════════
  // SCREEN 8: Social Proof
  // ══════════════════════════════════════════
  const renderSocialProof = () => (
    <View style={s.screenCenter}>
      <Text style={s.socialCounter}>12,000+</Text>
      <Text style={s.socialLabel}>daily readers and growing</Text>
      <View style={s.starsRow}>
        {[1, 2, 3, 4, 5].map(i => (
          <Ionicons key={i} name="star" size={22} color={Colors.gold} style={{ marginHorizontal: 2 }} />
        ))}
        <Text style={s.starsText}>4.8 average rating</Text>
      </View>

      <View style={s.testimonialList}>
        {TESTIMONIALS.map((t, i) => (
          <View key={i} style={s.testimonialCard}>
            <View style={s.testimonialHeader}>
              <View style={s.testimonialAvatar}>
                <Text style={s.testimonialAvatarText}>{t.name.charAt(0)}</Text>
              </View>
              <View>
                <Text style={s.testimonialName}>{t.name}</Text>
                <View style={s.testimonialStreakRow}>
                  <Ionicons name="flame" size={14} color={Colors.streakFire} />
                  <Text style={s.testimonialStreak}>{t.streak}-day streak</Text>
                </View>
              </View>
            </View>
            <Text style={s.testimonialText}>"{t.text}"</Text>
          </View>
        ))}
      </View>
    </View>
  );

  // ══════════════════════════════════════════
  // SCREEN 9: Feature Showcase
  // ══════════════════════════════════════════
  const renderFeatures = () => (
    <View style={s.screenPadded}>
      <Text style={s.screenTitle}>Everything you need{'\n'}for daily reading</Text>
      <Text style={s.screenSub}>Built to keep you consistent and growing.</Text>
      <View style={s.featureGrid}>
        {FEATURES_SHOWCASE.map((f, i) => (
          <View key={i} style={s.featureCard}>
            <View style={s.featureIconWrap}>
              <Ionicons name={f.icon} size={28} color={Colors.gold} />
            </View>
            <Text style={s.featureTitle}>{f.title}</Text>
            <Text style={s.featureDesc}>{f.desc}</Text>
          </View>
        ))}
      </View>
    </View>
  );

  // ══════════════════════════════════════════
  // SCREEN 10: Notification Permission
  // ══════════════════════════════════════════
  const renderNotificationPermission = () => (
    <View style={s.screenCenter}>
      <View style={s.notifIconWrap}>
        <Ionicons name="notifications" size={48} color={Colors.navy} />
      </View>
      <Text style={s.heroTitle}>Never miss your{'\n'}daily reading</Text>
      <Text style={s.heroSub}>
        A gentle reminder at your chosen time helps build the habit. 80% of users with notifications enabled maintain their streak.
      </Text>
      <View style={s.notifPreview}>
        <View style={s.notifPreviewHeader}>
          <View style={s.notifPreviewIcon}>
            <Text style={{ fontSize: 16 }}>{'\u271E'}</Text>
          </View>
          <View style={{ flex: 1 }}>
            <Text style={s.notifPreviewApp}>SCRIPTURE STREAK</Text>
            <Text style={s.notifPreviewTitle}>Today's Verse: Psalm 23:1</Text>
          </View>
          <Text style={s.notifPreviewTime}>now</Text>
        </View>
        <Text style={s.notifPreviewBody}>"The Lord is my shepherd, I shall not want."</Text>
      </View>
    </View>
  );

  // ══════════════════════════════════════════
  // SCREEN 11: Plan Ready
  // ══════════════════════════════════════════
  const renderPlanReady = () => {
    const goalLabel = GOALS.find(g => g.id === answers.goal)?.label || 'Grow in faith';
    const freqLabel = FREQUENCIES.find(f => f.id === answers.frequency)?.label || 'Daily';
    const timeLabel = TIMES.find(t => t.id === answers.time)?.label || 'Morning';
    const durLabel = DURATIONS.find(d => d.id === answers.duration)?.label || '10 min';

    return (
      <View style={s.screenCenter}>
        <View style={s.planReadyCheck}>
          <Ionicons name="checkmark-circle" size={56} color={Colors.gold} />
        </View>
        <Text style={s.heroTitle}>Your personalized{'\n'}reading plan is ready!</Text>
        <View style={s.planSummary}>
          {[
            { label: 'Goal', value: goalLabel, icon: 'heart' as const },
            { label: 'Schedule', value: freqLabel, icon: 'calendar' as const },
            { label: 'Time', value: timeLabel, icon: 'time' as const },
            { label: 'Duration', value: durLabel, icon: 'hourglass' as const },
          ].map((item, i) => (
            <View key={i} style={s.planSummaryRow}>
              <View style={s.planSummaryIcon}>
                <Ionicons name={item.icon} size={18} color={Colors.gold} />
              </View>
              <Text style={s.planSummaryLabel}>{item.label}</Text>
              <Text style={s.planSummaryValue}>{item.value}</Text>
            </View>
          ))}
        </View>
      </View>
    );
  };

  // ══════════════════════════════════════════
  // SCREEN 12: Paywall
  // ══════════════════════════════════════════
  const renderPaywall = () => {
    if (showRescue) {
      return renderRescueOffer();
    }

    return (
      <ScrollView
        style={{ flex: 1 }}
        contentContainerStyle={s.paywallScroll}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={s.paywallHeader}>
          <View style={s.premiumBadge}>
            <Text style={s.premiumBadgeText}>PREMIUM</Text>
          </View>
          <Text style={s.paywallTitle}>Start Your{'\n'}Scripture Journey</Text>
        </View>

        {/* Trial timeline */}
        <View style={s.timeline}>
          <View style={s.timelineRow}>
            <View style={[s.timelineDot, s.timelineDotActive]}>
              <Ionicons name="checkmark" size={14} color={Colors.navy} />
            </View>
            <View style={s.timelineLine} />
            <View style={s.timelineDot}>
              <Ionicons name="notifications-outline" size={12} color="#FFFFFF99" />
            </View>
            <View style={s.timelineLine} />
            <View style={s.timelineDot}>
              <Ionicons name="card-outline" size={12} color="#FFFFFF99" />
            </View>
          </View>
          <View style={s.timelineLabels}>
            <Text style={[s.timelineLabel, s.timelineLabelActive]}>Today{'\n'}Full Access</Text>
            <Text style={s.timelineLabel}>Day 2{'\n'}Reminder</Text>
            <Text style={s.timelineLabel}>Day 3{'\n'}Billing</Text>
          </View>
        </View>

        <Text style={s.noPayment}>No payment due now</Text>

        {/* Plans */}
        <View style={s.plansContainer}>
          {/* Monthly - Anchor */}
          <TouchableOpacity
            style={[s.planCard, selectedPlan === 'monthly' && s.planCardActive]}
            onPress={() => setSelectedPlan('monthly')}
            activeOpacity={0.7}
          >
            <View style={[s.planRadio, selectedPlan === 'monthly' && s.planRadioActive]}>
              {selectedPlan === 'monthly' && <View style={s.planRadioDot} />}
            </View>
            <View style={s.planInfo}>
              <Text style={[s.planName, selectedPlan === 'monthly' && s.planNameActive]}>Monthly</Text>
              <Text style={s.planPrice}>$6.99 / month</Text>
            </View>
          </TouchableOpacity>

          {/* Yearly - Best Value */}
          <TouchableOpacity
            style={[s.planCard, s.planCardYearly, selectedPlan === 'yearly' && s.planCardActive]}
            onPress={() => setSelectedPlan('yearly')}
            activeOpacity={0.7}
          >
            <View style={s.bestValueBadge}>
              <Text style={s.bestValueText}>BEST VALUE</Text>
            </View>
            <View style={[s.planRadio, selectedPlan === 'yearly' && s.planRadioActive]}>
              {selectedPlan === 'yearly' && <View style={s.planRadioDot} />}
            </View>
            <View style={s.planInfo}>
              <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                <Text style={[s.planName, selectedPlan === 'yearly' && s.planNameActive]}>Yearly</Text>
                <View style={s.saveBadge}>
                  <Text style={s.saveBadgeText}>Save 70%</Text>
                </View>
              </View>
              <Text style={s.planPrice}>$29.99 / year</Text>
              <Text style={s.planPriceMonthly}>Just $2.50 / month</Text>
            </View>
          </TouchableOpacity>
        </View>

        {/* Benefits */}
        <View style={s.benefitsList}>
          {[
            { icon: 'language-outline', text: 'All translations unlocked' },
            { icon: 'map-outline', text: 'Guided reading plans' },
            { icon: 'trophy-outline', text: 'Streak rewards & badges' },
            { icon: 'cloud-offline-outline', text: 'Offline access' },
          ].map((b, i) => (
            <View key={i} style={s.benefitRow}>
              <Ionicons name={b.icon as any} size={20} color={Colors.gold} />
              <Text style={s.benefitText}>{b.text}</Text>
            </View>
          ))}
        </View>

        {/* Social proof */}
        <View style={s.paywallSocial}>
          <View style={s.paywallStars}>
            {[1, 2, 3, 4, 5].map(i => (
              <Ionicons key={i} name="star" size={16} color={Colors.gold} />
            ))}
          </View>
          <Text style={s.paywallSocialText}>4.8 stars  |  12,000+ readers</Text>
        </View>
      </ScrollView>
    );
  };

  // ══════════════════════════════════════════
  // RESCUE OFFER (shown on paywall decline)
  // ══════════════════════════════════════════
  const renderRescueOffer = () => (
    <View style={s.screenCenter}>
      <Text style={s.rescueTitle}>Wait! Special offer{'\n'}just for you</Text>
      <Text style={s.rescueSub}>
        We don't want cost to stand between you and God's Word.
      </Text>

      <View style={s.rescueCard}>
        <View style={s.rescueOriginal}>
          <Text style={s.rescueOriginalPrice}>$29.99/yr</Text>
          <View style={s.rescueStrike} />
        </View>
        <Text style={s.rescueNewPrice}>$19.99/yr</Text>
        <Text style={s.rescueSave}>Save an additional 33%</Text>
        <Text style={s.rescuePerDay}>Just $0.05 per day</Text>
      </View>

      <TouchableOpacity
        style={s.rescueBtn}
        onPress={handlePurchase}
        activeOpacity={0.8}
        disabled={isPurchasing}
      >
        <Text style={s.rescueBtnText}>
          {isPurchasing ? 'Processing...' : 'Claim This Offer'}
        </Text>
      </TouchableOpacity>

      <Text style={s.rescueTrialNote}>Includes 7-day free trial</Text>

      <TouchableOpacity
        style={s.rescueDecline}
        onPress={() => saveAndComplete()}
        activeOpacity={0.7}
      >
        <Text style={s.rescueDeclineText}>No thanks, continue free</Text>
      </TouchableOpacity>
    </View>
  );

  // ══════════════════════════════════════════
  // Render dispatcher
  // ══════════════════════════════════════════
  const screens = [
    renderWelcome,       // 0
    renderGoal,          // 1
    renderExperience,    // 2
    renderFrequency,     // 3
    renderTime,          // 4
    renderDuration,      // 5
    renderValidation,    // 6
    renderSocialProof,   // 7
    renderFeatures,      // 8
    renderNotificationPermission, // 9
    renderPlanReady,     // 10
    renderPaywall,       // 11
  ];

  const isPaywall = step === 11;
  const isNotifScreen = step === 9;

  // Determine CTA text
  const getCTAText = (): string => {
    if (step === 0) return 'Get Started';
    if (step === 9) return 'Enable Notifications';
    if (step === 10) return 'See My Plan';
    if (step === 11 && !showRescue) return isPurchasing ? 'Processing...' : 'Start My Free Trial';
    if (step === 11 && showRescue) return ''; // CTA is inline in rescue
    return 'Continue';
  };

  // Whether to show bottom button
  const showBottomCTA = !isPaywall || !showRescue;

  return (
    <View style={[s.container, { paddingTop: insets.top, paddingBottom: Math.max(insets.bottom, 16) }]}>
      {/* ── Progress Bar ── */}
      {!isPaywall && (
        <View style={s.progressBarContainer}>
          {step > 0 && (
            <TouchableOpacity
              onPress={goBack}
              style={s.backBtn}
              hitSlop={{ top: 12, bottom: 12, left: 12, right: 12 }}
            >
              <Ionicons name="chevron-back" size={24} color={Colors.gold} />
            </TouchableOpacity>
          )}
          <View style={s.progressBarTrack}>
            <Animated.View
              style={[
                s.progressBarFill,
                {
                  width: progressAnim.interpolate({
                    inputRange: [0, 1],
                    outputRange: ['0%', '100%'],
                  }),
                },
              ]}
            />
          </View>
          {canSkip() ? (
            <TouchableOpacity onPress={goNext} style={s.skipBtn}>
              <Text style={s.skipText}>Skip</Text>
            </TouchableOpacity>
          ) : (
            <View style={s.skipBtn} />
          )}
        </View>
      )}

      {/* Paywall top bar */}
      {isPaywall && (
        <View style={s.paywallTopBar}>
          <TouchableOpacity onPress={goBack} style={s.backBtn} hitSlop={{ top: 12, bottom: 12, left: 12, right: 12 }}>
            <Ionicons name="chevron-back" size={24} color={Colors.gold} />
          </TouchableOpacity>
          <View style={{ flex: 1 }} />
          <TouchableOpacity
            onPress={handleDeclinePaywall}
            style={s.closePaywallBtn}
            hitSlop={{ top: 12, bottom: 12, left: 12, right: 12 }}
          >
            <Text style={s.closePaywallText}>{'\u2715'}</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* ── Screen Content ── */}
      <Animated.View
        style={[
          s.screenContent,
          {
            opacity: fadeAnim,
            transform: [{ translateX: slideAnim }],
          },
        ]}
      >
        {screens[step]()}
      </Animated.View>

      {/* ── Bottom CTA ── */}
      {showBottomCTA && (
        <View style={s.bottomArea}>
          {isPaywall && !showRescue ? (
            <>
              <TouchableOpacity
                style={[s.ctaButton, isPurchasing && { opacity: 0.6 }]}
                onPress={handlePurchase}
                activeOpacity={0.8}
                disabled={isPurchasing}
              >
                <Text style={s.ctaButtonText}>{getCTAText()}</Text>
                <Text style={s.ctaButtonSub}>
                  3 days free, then {selectedPlan === 'yearly' ? '$29.99/year' : '$6.99/month'}
                </Text>
              </TouchableOpacity>
              <Text style={s.cancelAnytime}>Subscription automatically renews unless canceled at least 24 hours before the end of the current period. Manage subscriptions in your Apple ID account settings. Cancel anytime.</Text>
              <View style={s.legalLinks}>
                <TouchableOpacity onPress={() => Linking.openURL(TERMS_URL)}>
                  <Text style={s.legalLink}>Terms</Text>
                </TouchableOpacity>
                <Text style={s.legalSep}> | </Text>
                <TouchableOpacity onPress={() => Linking.openURL(PRIVACY_URL)}>
                  <Text style={s.legalLink}>Privacy</Text>
                </TouchableOpacity>
                <Text style={s.legalSep}> | </Text>
                <TouchableOpacity onPress={handleRestore}>
                  <Text style={s.legalLink}>Restore</Text>
                </TouchableOpacity>
              </View>
            </>
          ) : isNotifScreen ? (
            <>
              <TouchableOpacity
                style={s.ctaButton}
                onPress={requestNotifications}
                activeOpacity={0.8}
              >
                <Text style={s.ctaButtonText}>Enable Notifications</Text>
              </TouchableOpacity>
              <TouchableOpacity onPress={goNext} style={{ paddingVertical: 12 }}>
                <Text style={s.skipNotifText}>Maybe later</Text>
              </TouchableOpacity>
            </>
          ) : !showRescue ? (
            <TouchableOpacity
              style={[s.ctaButton, !canAdvance() && s.ctaButtonDisabled]}
              onPress={goNext}
              activeOpacity={0.8}
              disabled={!canAdvance()}
            >
              <Text style={s.ctaButtonText}>{getCTAText()}</Text>
            </TouchableOpacity>
          ) : null}

          {step === 0 && (
            <View style={s.termsRow}>
              <Text style={s.termsText}>By continuing, you agree to our </Text>
              <TouchableOpacity onPress={() => Linking.openURL(TERMS_URL)}>
                <Text style={s.termsLink}>Terms</Text>
              </TouchableOpacity>
              <Text style={s.termsText}> & </Text>
              <TouchableOpacity onPress={() => Linking.openURL(PRIVACY_URL)}>
                <Text style={s.termsLink}>Privacy Policy</Text>
              </TouchableOpacity>
            </View>
          )}
        </View>
      )}
    </View>
  );
}

// ══════════════════════════════════════════════
// Helper: check if onboarding is complete
// ══════════════════════════════════════════════
export async function isOnboardingComplete(): Promise<boolean> {
  try {
    const val = await AsyncStorage.getItem(ONBOARDING_COMPLETE_KEY);
    return val === 'true';
  } catch {
    return false;
  }
}

// ══════════════════════════════════════════════
// STYLES
// ══════════════════════════════════════════════
const s = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.navy,
  },

  // ── Progress Bar ──
  progressBarContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: Spacing.md,
    paddingTop: Spacing.sm,
    paddingBottom: Spacing.sm,
    gap: 12,
  },
  backBtn: {
    width: 40,
    height: 40,
    alignItems: 'center',
    justifyContent: 'center',
  },
  progressBarTrack: {
    flex: 1,
    height: 4,
    backgroundColor: '#FFFFFF20',
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: '100%',
    backgroundColor: Colors.gold,
    borderRadius: 2,
  },
  skipBtn: {
    width: 50,
    alignItems: 'flex-end',
  },
  skipText: {
    fontSize: 15,
    fontWeight: '600',
    color: '#FFFFFF66',
  },

  // ── Paywall top bar ──
  paywallTopBar: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: Spacing.md,
    paddingTop: Spacing.sm,
  },
  closePaywallBtn: {
    width: 40,
    height: 40,
    alignItems: 'center',
    justifyContent: 'center',
  },
  closePaywallText: {
    fontSize: 18,
    color: '#FFFFFF55',
    fontWeight: '600',
  },

  // ── Screen Content ──
  screenContent: {
    flex: 1,
  },
  screenCenter: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: Spacing.xl,
  },
  screenPadded: {
    flex: 1,
    paddingHorizontal: Spacing.xl,
    paddingTop: Spacing.lg,
  },

  // ── Common text ──
  heroTitle: {
    fontSize: 28,
    fontWeight: '700',
    color: '#FFFBF5',
    textAlign: 'center',
    letterSpacing: -0.5,
    lineHeight: 36,
    marginBottom: Spacing.md,
  },
  heroSub: {
    fontSize: 16,
    color: '#FFFFFF99',
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: Spacing.xl,
    paddingHorizontal: Spacing.sm,
  },
  screenTitle: {
    fontSize: 26,
    fontWeight: '700',
    color: '#FFFBF5',
    letterSpacing: -0.5,
    lineHeight: 34,
    marginBottom: Spacing.sm,
  },
  screenSub: {
    fontSize: 16,
    color: '#FFFFFF88',
    lineHeight: 24,
    marginBottom: Spacing.xl,
  },

  // ── Welcome ──
  welcomeGlow: {
    width: 88,
    height: 88,
    borderRadius: 44,
    backgroundColor: Colors.gold,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: Spacing.xl,
    shadowColor: Colors.gold,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.5,
    shadowRadius: 24,
    elevation: 8,
  },
  welcomeCross: {
    fontSize: 40,
    color: Colors.navy,
  },
  welcomeFeats: {
    alignSelf: 'stretch',
    gap: 12,
  },
  welcomeFeatRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF0D',
    borderRadius: BorderRadius.md,
    padding: 14,
    borderWidth: 1,
    borderColor: '#FFFFFF08',
  },
  welcomeFeatIcon: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#E2B53F15',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 14,
  },
  welcomeFeatText: {
    flex: 1,
    fontSize: 15,
    color: '#FFFFFFCC',
    lineHeight: 22,
  },

  // ── Option Cards (Goal, Experience, Frequency) ──
  optionList: {
    gap: 10,
  },
  optionCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF0D',
    borderRadius: BorderRadius.lg,
    padding: 16,
    borderWidth: 1.5,
    borderColor: '#FFFFFF15',
  },
  optionCardActive: {
    borderColor: Colors.gold,
    backgroundColor: '#E2B53F12',
  },
  optionIcon: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: '#E2B53F15',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 14,
  },
  optionIconActive: {
    backgroundColor: Colors.gold,
  },
  optionInfo: {
    flex: 1,
  },
  optionLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFFFFFDD',
    marginBottom: 2,
  },
  optionLabelActive: {
    color: Colors.gold,
  },
  optionDesc: {
    fontSize: 13,
    color: '#FFFFFF66',
    lineHeight: 18,
  },
  radio: {
    width: 22,
    height: 22,
    borderRadius: 11,
    borderWidth: 2,
    borderColor: '#FFFFFF30',
    alignItems: 'center',
    justifyContent: 'center',
    marginLeft: 10,
  },
  radioActive: {
    borderColor: Colors.gold,
  },
  radioDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: Colors.gold,
  },

  // ── Time Grid ──
  timeGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  timeCard: {
    width: (SCREEN_WIDTH - Spacing.xl * 2 - 12) / 2,
    backgroundColor: '#FFFFFF0D',
    borderRadius: BorderRadius.lg,
    padding: 18,
    alignItems: 'center',
    borderWidth: 1.5,
    borderColor: '#FFFFFF15',
  },
  timeCardActive: {
    borderColor: Colors.gold,
    backgroundColor: '#E2B53F15',
  },
  timeLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFFFFFDD',
    marginBottom: 4,
  },
  timeLabelActive: {
    color: Colors.gold,
  },
  timeDesc: {
    fontSize: 12,
    color: '#FFFFFF66',
    textAlign: 'center',
  },
  timeDescActive: {
    color: '#FFFFFFAA',
  },

  // ── Duration ──
  durationRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
    justifyContent: 'center',
  },
  durationCard: {
    width: (SCREEN_WIDTH - Spacing.xl * 2 - 12) / 2,
    backgroundColor: '#FFFFFF0D',
    borderRadius: BorderRadius.lg,
    paddingVertical: 24,
    paddingHorizontal: 16,
    alignItems: 'center',
    borderWidth: 1.5,
    borderColor: '#FFFFFF15',
  },
  durationCardActive: {
    borderColor: Colors.gold,
    backgroundColor: '#E2B53F15',
  },
  durationNumber: {
    fontSize: 24,
    fontWeight: '700',
    color: '#FFFFFFDD',
    marginBottom: 4,
  },
  durationNumberActive: {
    color: Colors.gold,
  },
  durationDesc: {
    fontSize: 13,
    color: '#FFFFFF66',
  },
  durationDescActive: {
    color: '#FFFFFFAA',
  },

  // ── Validation / Projection ──
  validationBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.gold,
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: BorderRadius.full,
    marginBottom: Spacing.lg,
    gap: 6,
  },
  validationBadgeText: {
    fontSize: 12,
    fontWeight: '800',
    color: Colors.navy,
    letterSpacing: 1,
  },
  projectionCard: {
    backgroundColor: '#FFFFFF0D',
    borderRadius: BorderRadius.xl,
    paddingVertical: 24,
    paddingHorizontal: 20,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#E2B53F30',
    marginBottom: Spacing.xl,
    alignSelf: 'stretch',
  },
  projectionHighlight: {
    fontSize: 15,
    color: '#FFFFFF99',
    marginBottom: 4,
  },
  projectionTarget: {
    fontSize: 22,
    fontWeight: '700',
    color: Colors.gold,
    marginBottom: 12,
    textAlign: 'center',
  },
  projectionDays: {
    fontSize: 28,
    fontWeight: '700',
    color: '#FFFBF5',
    marginBottom: 4,
  },
  projectionChapters: {
    fontSize: 14,
    color: '#FFFFFF66',
    marginTop: 4,
  },
  graphContainer: {
    alignSelf: 'stretch',
    alignItems: 'center',
  },
  graphBars: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    justifyContent: 'space-around',
    height: 110,
    alignSelf: 'stretch',
    marginBottom: 8,
  },
  graphCol: {
    alignItems: 'center',
    flex: 1,
  },
  graphBar: {
    width: 28,
    borderRadius: 4,
    backgroundColor: '#E2B53F30',
    overflow: 'hidden',
    justifyContent: 'flex-end',
  },
  graphBarFill: {
    width: '100%',
    height: '100%',
    backgroundColor: Colors.gold,
    borderRadius: 4,
    opacity: 0.6,
  },
  graphBarFillDone: {
    opacity: 1.0,
  },
  graphLabel: {
    fontSize: 11,
    color: '#FFFFFF66',
    marginTop: 6,
    fontWeight: '600',
  },
  graphCaption: {
    fontSize: 12,
    color: '#FFFFFF44',
    marginTop: 8,
  },

  // ── Social Proof ──
  socialCounter: {
    fontSize: 48,
    fontWeight: '200',
    color: Colors.gold,
    letterSpacing: -2,
    marginBottom: 4,
    fontVariant: ['tabular-nums'],
  },
  socialLabel: {
    fontSize: 17,
    color: '#FFFFFFCC',
    marginBottom: Spacing.md,
  },
  starsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: Spacing.xl,
  },
  starsText: {
    fontSize: 14,
    color: '#FFFFFF88',
    marginLeft: 8,
  },
  testimonialList: {
    alignSelf: 'stretch',
    gap: 12,
  },
  testimonialCard: {
    backgroundColor: '#FFFFFF0D',
    borderRadius: BorderRadius.lg,
    padding: 16,
    borderWidth: 1,
    borderColor: '#FFFFFF10',
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
    backgroundColor: Colors.gold,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 10,
  },
  testimonialAvatarText: {
    fontSize: 16,
    fontWeight: '700',
    color: Colors.navy,
  },
  testimonialName: {
    fontSize: 14,
    fontWeight: '600',
    color: '#FFFFFFDD',
  },
  testimonialStreakRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  testimonialStreak: {
    fontSize: 12,
    color: Colors.streakFire,
    fontWeight: '600',
  },
  testimonialText: {
    fontSize: 15,
    color: '#FFFFFFAA',
    lineHeight: 22,
    fontStyle: 'italic',
  },

  // ── Feature Showcase ──
  featureGrid: {
    gap: 12,
  },
  featureCard: {
    backgroundColor: '#FFFFFF0D',
    borderRadius: BorderRadius.lg,
    padding: 18,
    borderWidth: 1,
    borderColor: '#FFFFFF10',
  },
  featureIconWrap: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: '#E2B53F15',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 10,
  },
  featureTitle: {
    fontSize: 17,
    fontWeight: '600',
    color: '#FFFBF5',
    marginBottom: 4,
  },
  featureDesc: {
    fontSize: 14,
    color: '#FFFFFF88',
    lineHeight: 20,
  },

  // ── Notification Permission ──
  notifIconWrap: {
    width: 88,
    height: 88,
    borderRadius: 44,
    backgroundColor: Colors.gold,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: Spacing.xl,
    shadowColor: Colors.gold,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.5,
    shadowRadius: 24,
    elevation: 8,
  },
  notifPreview: {
    alignSelf: 'stretch',
    backgroundColor: '#FFFFFF12',
    borderRadius: BorderRadius.lg,
    padding: 14,
    borderWidth: 1,
    borderColor: '#FFFFFF15',
  },
  notifPreviewHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  notifPreviewIcon: {
    width: 32,
    height: 32,
    borderRadius: 8,
    backgroundColor: Colors.gold,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 10,
  },
  notifPreviewApp: {
    fontSize: 11,
    fontWeight: '700',
    color: '#FFFFFF66',
    letterSpacing: 0.5,
  },
  notifPreviewTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#FFFBF5',
  },
  notifPreviewTime: {
    fontSize: 12,
    color: '#FFFFFF55',
  },
  notifPreviewBody: {
    fontSize: 14,
    color: '#FFFFFF99',
    lineHeight: 20,
    fontStyle: 'italic',
    fontFamily: Platform.OS === 'ios' ? 'Georgia' : 'serif',
  },
  skipNotifText: {
    fontSize: 15,
    color: '#FFFFFF55',
    textAlign: 'center',
  },

  // ── Plan Ready ──
  planReadyCheck: {
    marginBottom: Spacing.lg,
  },
  planSummary: {
    alignSelf: 'stretch',
    backgroundColor: '#FFFFFF0D',
    borderRadius: BorderRadius.xl,
    padding: 20,
    borderWidth: 1,
    borderColor: '#E2B53F20',
    gap: 14,
  },
  planSummaryRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  planSummaryIcon: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#E2B53F15',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 14,
  },
  planSummaryLabel: {
    fontSize: 14,
    color: '#FFFFFF88',
    width: 80,
  },
  planSummaryValue: {
    flex: 1,
    fontSize: 16,
    fontWeight: '600',
    color: '#FFFBF5',
  },

  // ── Paywall ──
  paywallScroll: {
    paddingHorizontal: Spacing.lg,
    paddingTop: Spacing.md,
    paddingBottom: Spacing.md,
  },
  paywallHeader: {
    alignItems: 'center',
    marginBottom: Spacing.lg,
  },
  premiumBadge: {
    backgroundColor: Colors.gold,
    paddingVertical: 6,
    paddingHorizontal: 14,
    borderRadius: BorderRadius.full,
    marginBottom: Spacing.md,
  },
  premiumBadgeText: {
    fontSize: 11,
    fontWeight: '800',
    color: Colors.navy,
    letterSpacing: 1.5,
  },
  paywallTitle: {
    fontSize: 26,
    fontWeight: '700',
    color: '#FFFBF5',
    textAlign: 'center',
    lineHeight: 34,
    letterSpacing: -0.5,
  },

  // Trial timeline
  timeline: {
    alignSelf: 'stretch',
    marginBottom: Spacing.md,
  },
  timelineRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
  },
  timelineDot: {
    width: 32,
    height: 32,
    borderRadius: 16,
    borderWidth: 2,
    borderColor: '#FFFFFF30',
    alignItems: 'center',
    justifyContent: 'center',
  },
  timelineDotActive: {
    backgroundColor: Colors.gold,
    borderColor: Colors.gold,
  },
  timelineLine: {
    flex: 1,
    height: 2,
    backgroundColor: '#FFFFFF20',
    maxWidth: 80,
  },
  timelineLabels: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
  },
  timelineLabel: {
    fontSize: 12,
    color: '#FFFFFF66',
    textAlign: 'center',
    lineHeight: 16,
    width: 70,
  },
  timelineLabelActive: {
    color: Colors.gold,
    fontWeight: '600',
  },

  noPayment: {
    fontSize: 16,
    fontWeight: '700',
    color: Colors.gold,
    textAlign: 'center',
    marginBottom: Spacing.lg,
  },

  // Plans
  plansContainer: {
    gap: 10,
    marginBottom: Spacing.lg,
  },
  planCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF0D',
    borderRadius: BorderRadius.lg,
    padding: 16,
    borderWidth: 2,
    borderColor: '#FFFFFF15',
  },
  planCardYearly: {
    // extra bottom margin or special handling
  },
  planCardActive: {
    borderColor: Colors.gold,
    backgroundColor: '#E2B53F10',
  },
  bestValueBadge: {
    position: 'absolute',
    top: -10,
    right: 16,
    backgroundColor: Colors.gold,
    paddingVertical: 3,
    paddingHorizontal: 10,
    borderRadius: BorderRadius.full,
  },
  bestValueText: {
    fontSize: 10,
    fontWeight: '800',
    color: Colors.navy,
    letterSpacing: 0.8,
  },
  planRadio: {
    width: 22,
    height: 22,
    borderRadius: 11,
    borderWidth: 2,
    borderColor: '#FFFFFF30',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 14,
  },
  planRadioActive: {
    borderColor: Colors.gold,
  },
  planRadioDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: Colors.gold,
  },
  planInfo: {
    flex: 1,
  },
  planName: {
    fontSize: 17,
    fontWeight: '600',
    color: '#FFFFFFCC',
    marginBottom: 2,
  },
  planNameActive: {
    color: Colors.gold,
  },
  planPrice: {
    fontSize: 15,
    color: '#FFFFFF99',
  },
  planPriceMonthly: {
    fontSize: 13,
    color: Colors.gold,
    fontWeight: '600',
    marginTop: 2,
  },
  saveBadge: {
    backgroundColor: '#FF6B3520',
    borderRadius: BorderRadius.full,
    paddingHorizontal: 8,
    paddingVertical: 2,
    marginLeft: 8,
  },
  saveBadgeText: {
    fontSize: 11,
    fontWeight: '700',
    color: Colors.streakFire,
  },

  // Benefits
  benefitsList: {
    gap: 10,
    marginBottom: Spacing.md,
  },
  benefitRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  benefitText: {
    fontSize: 15,
    color: '#FFFFFFCC',
  },

  // Paywall social proof
  paywallSocial: {
    alignItems: 'center',
    marginTop: Spacing.sm,
  },
  paywallStars: {
    flexDirection: 'row',
    marginBottom: 4,
  },
  paywallSocialText: {
    fontSize: 13,
    color: '#FFFFFF66',
  },

  // ── Rescue Offer ──
  rescueTitle: {
    fontSize: 28,
    fontWeight: '700',
    color: '#FFFBF5',
    textAlign: 'center',
    lineHeight: 36,
    letterSpacing: -0.5,
    marginBottom: Spacing.md,
  },
  rescueSub: {
    fontSize: 16,
    color: '#FFFFFF99',
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: Spacing.xl,
    paddingHorizontal: Spacing.md,
  },
  rescueCard: {
    alignSelf: 'stretch',
    backgroundColor: '#FFFFFF0D',
    borderRadius: BorderRadius.xl,
    padding: 24,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: Colors.gold,
    marginBottom: Spacing.xl,
  },
  rescueOriginal: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  rescueOriginalPrice: {
    fontSize: 18,
    color: '#FFFFFF55',
    fontWeight: '500',
  },
  rescueStrike: {
    position: 'absolute',
    height: 2,
    backgroundColor: '#FF6B35',
    width: '100%',
    top: '50%',
  },
  rescueNewPrice: {
    fontSize: 36,
    fontWeight: '700',
    color: Colors.gold,
    marginBottom: 4,
  },
  rescueSave: {
    fontSize: 15,
    color: Colors.streakFire,
    fontWeight: '600',
    marginBottom: 4,
  },
  rescuePerDay: {
    fontSize: 14,
    color: '#FFFFFF88',
  },
  rescueBtn: {
    alignSelf: 'stretch',
    backgroundColor: Colors.gold,
    borderRadius: BorderRadius.lg,
    paddingVertical: 16,
    alignItems: 'center',
    marginBottom: Spacing.sm,
    shadowColor: Colors.gold,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 6,
  },
  rescueBtnText: {
    fontSize: 17,
    fontWeight: '700',
    color: Colors.navy,
  },
  rescueTrialNote: {
    fontSize: 13,
    color: '#FFFFFF88',
    textAlign: 'center',
    marginBottom: Spacing.md,
  },
  rescueDecline: {
    paddingVertical: 12,
  },
  rescueDeclineText: {
    fontSize: 15,
    color: '#FFFFFF44',
    textAlign: 'center',
  },

  // ── Bottom CTA ──
  bottomArea: {
    paddingHorizontal: Spacing.xl,
    paddingTop: Spacing.sm,
    paddingBottom: Spacing.sm,
  },
  ctaButton: {
    backgroundColor: Colors.gold,
    borderRadius: BorderRadius.lg,
    paddingVertical: 16,
    alignItems: 'center',
    shadowColor: Colors.gold,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 6,
  },
  ctaButtonDisabled: {
    opacity: 0.4,
  },
  ctaButtonText: {
    fontSize: 17,
    fontWeight: '700',
    color: Colors.navy,
    letterSpacing: 0.3,
  },
  ctaButtonSub: {
    fontSize: 12,
    color: '#1A1A2E99',
    marginTop: 2,
  },
  cancelAnytime: {
    fontSize: 13,
    color: '#FFFFFF66',
    textAlign: 'center',
    marginTop: 10,
  },
  legalLinks: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 6,
  },
  legalLink: {
    fontSize: 11,
    color: '#FFFFFF55',
    textDecorationLine: 'underline',
  },
  legalSep: {
    fontSize: 11,
    color: '#FFFFFF33',
  },
  termsRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    marginTop: Spacing.sm,
  },
  termsText: {
    fontSize: 12,
    color: '#FFFFFF44',
  },
  termsLink: {
    fontSize: 12,
    color: '#FFFFFF88',
    textDecorationLine: 'underline',
  },
});
